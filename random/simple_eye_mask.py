#!/usr/bin/env python3
"""
Eye Mask - Anti-Flicker Edition (Fixed)
"""

# Suppress warnings
import os
os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'
os.environ['GST_DEBUG'] = '0'
os.environ['OPENCV_VIDEOIO_PRIORITY_LIST'] = 'V4L2'

import cv2
import numpy as np
import sys
import argparse
from collections import deque
import time

# ===== YOUR CUSTOM DEFAULTS =====
HORIZONTAL_PADDING = 2.1    # Width setting
VERTICAL_PADDING = 0.6       # Height setting
VERTICAL_OFFSET = -2         # Vertical offset
# ================================

# Anti-flicker settings (will be managed in main)
DEFAULT_SMOOTHING_FRAMES = 10
DEFAULT_POSITION_SMOOTHING = 0.3
DEFAULT_SIZE_SMOOTHING = 0.2
DEFAULT_MAX_FRAME_SKIP = 2
MIN_EYE_DISTANCE = 20
MAX_EYE_DISTANCE = 150

# Find cascade files
cascade_paths = [
    '/usr/share/opencv4/haarcascades/',
    '/usr/local/share/opencv4/haarcascades/',
    '/usr/share/OpenCV/haarcascades/',
]

face_cascade = None
eye_cascade = None

for path in cascade_paths:
    face_file = os.path.join(path, 'haarcascade_frontalface_default.xml')
    eye_file = os.path.join(path, 'haarcascade_eye.xml')
    if os.path.exists(face_file) and os.path.exists(eye_file):
        face_cascade = cv2.CascadeClassifier(face_file)
        eye_cascade = cv2.CascadeClassifier(eye_file)
        print(f"✓ Found cascades in: {path}")
        break

if face_cascade is None:
    print("✗ ERROR: Could not find Haar cascade files!")
    print("  Run: sudo pacman -S opencv")
    sys.exit(1)

class SmoothingFilter:
    """Exponential moving average filter for smooth transitions"""
    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.value = None
    
    def update(self, new_value):
        if self.value is None:
            self.value = new_value
        else:
            self.value = self.alpha * new_value + (1 - self.alpha) * self.value
        return self.value
    
    def reset(self):
        self.value = None

def setup_virtual_camera(device='/dev/video10', width=640, height=480):
    """Setup FFmpeg process for virtual camera output"""
    try:
        import subprocess
        cmd = [
            'ffmpeg', '-y', '-f', 'rawvideo',
            '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24',
            '-s', f'{width}x{height}', '-r', '30',
            '-i', '-', '-vf', 'format=yuv420p',
            '-f', 'v4l2', device
        ]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        print(f"✓ Streaming to virtual camera: {device}")
        return process
    except Exception as e:
        print(f"✗ Failed to setup virtual camera: {e}")
        print("  Make sure v4l2loopback is loaded: sudo modprobe v4l2loopback exclusive_caps=1")
        return None

def main():
    parser = argparse.ArgumentParser(description='Eye Mask Camera')
    parser.add_argument('--output', '-o', type=str, 
                       help='Output to virtual camera (e.g., /dev/video10)')
    parser.add_argument('--resolution', '-r', type=str, default='640x480',
                       help='Resolution (e.g., 640x480, 1280x720)')
    parser.add_argument('--camera', '-c', type=int, default=0,
                       help='Camera device ID (default: 0)')
    parser.add_argument('--no-preview', action='store_true',
                       help='Disable preview window (headless mode)')
    parser.add_argument('--aggressive-smooth', action='store_true',
                       help='Extra smoothing (slower response but less flicker)')
    args = parser.parse_args()
    
    # Parse resolution
    try:
        width, height = map(int, args.resolution.split('x'))
    except:
        print("✗ Invalid resolution format. Using 640x480")
        width, height = 640, 480
    
    print("\n" + "="*50)
    print("EYE MASK - ANTI-FLICKER EDITION")
    print("="*50)
    print(f"Default settings: Width={HORIZONTAL_PADDING}, Height={VERTICAL_PADDING}, Offset={VERTICAL_OFFSET}")
    
    # Open webcam with V4L2 backend
    cap = cv2.VideoCapture(args.camera, cv2.CAP_V4L2)
    if not cap.isOpened():
        print(f"✗ Could not open camera {args.camera}")
        sys.exit(1)
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    # Get actual resolution
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"✓ Camera {args.camera} opened at {actual_width}x{actual_height}")
    
    # Setup virtual camera if requested
    ffmpeg_process = None
    if args.output:
        ffmpeg_process = setup_virtual_camera(args.output, actual_width, actual_height)
    
    print("\nControls:")
    print("  q - Quit")
    print("  + / - : Adjust width")
    print("  ] / [ : Adjust height")
    print("  ↑ / ↓ : Move rectangle")
    print("  r - Reset smoothing")
    print("  d - Toggle debug view")
    print("  f - Toggle aggressive smoothing")
    print("="*50 + "\n")
    
    # Interactive variables
    h_padding = HORIZONTAL_PADDING
    v_padding = VERTICAL_PADDING
    v_offset = VERTICAL_OFFSET
    show_debug = True
    aggressive_smooth = args.aggressive_smooth
    
    # Set smoothing parameters based on mode
    if aggressive_smooth:
        position_smoothing = 0.15
        size_smoothing = 0.1
        max_frame_skip = 3
    else:
        position_smoothing = DEFAULT_POSITION_SMOOTHING
        size_smoothing = DEFAULT_SIZE_SMOOTHING
        max_frame_skip = DEFAULT_MAX_FRAME_SKIP
    
    # Smoothing filters
    center_x_filter = SmoothingFilter(position_smoothing)
    center_y_filter = SmoothingFilter(position_smoothing)
    width_filter = SmoothingFilter(size_smoothing)
    height_filter = SmoothingFilter(size_smoothing)
    
    # Detection tracking
    last_good_bbox = None
    frames_since_detection = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("✗ Failed to grab frame")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mask = np.zeros_like(frame)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)
            
            detection_success = False
            
            for (x, y, w, h) in faces:
                # Only use faces in the upper half of frame
                if y > actual_height // 2:
                    continue
                    
                # Detect eyes in face region
                roi_gray = gray[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                
                if len(eyes) >= 2:
                    # Filter eye candidates
                    valid_eyes = []
                    for (ex, ey, ew, eh) in eyes:
                        if ey < h // 2:
                            valid_eyes.append((ex, ey, ew, eh))
                    
                    if len(valid_eyes) >= 2:
                        valid_eyes = sorted(valid_eyes, key=lambda e: e[0])
                        
                        # Check if eye distance is plausible
                        eye_distance_px = abs((valid_eyes[1][0] - valid_eyes[0][0]))
                        if MIN_EYE_DISTANCE < eye_distance_px < MAX_EYE_DISTANCE:
                            
                            eye_coords = []
                            for (ex, ey, ew, eh) in valid_eyes[:2]:
                                eye_coords.append((x + ex + ew//2, y + ey + eh//2))
                            
                            center_x = (eye_coords[0][0] + eye_coords[1][0]) // 2
                            center_y = (eye_coords[0][1] + eye_coords[1][1]) // 2
                            
                            # Apply smoothing
                            smooth_center_x = int(center_x_filter.update(center_x))
                            smooth_center_y = int(center_y_filter.update(center_y))
                            
                            eye_distance = abs(eye_coords[1][0] - eye_coords[0][0])
                            raw_width = eye_distance * h_padding
                            raw_height = eye_distance * v_padding
                            
                            smooth_width = width_filter.update(raw_width)
                            smooth_height = height_filter.update(raw_height)
                            
                            x1 = max(0, int(smooth_center_x - smooth_width//2))
                            y1 = max(0, int(smooth_center_y - smooth_height//2 + v_offset))
                            x2 = min(frame.shape[1], int(smooth_center_x + smooth_width//2))
                            y2 = min(frame.shape[0], int(smooth_center_y + smooth_height//2 + v_offset))
                            
                            last_good_bbox = (x1, y1, x2, y2)
                            frames_since_detection = 0
                            detection_success = True
                            break
                
                if detection_success:
                    break
            
            # Use last good position if detection failed
            if not detection_success and last_good_bbox and frames_since_detection < max_frame_skip:
                x1, y1, x2, y2 = last_good_bbox
                frames_since_detection += 1
                detection_success = True
            
            # Apply mask if we have a valid rectangle
            if detection_success and last_good_bbox:
                x1, y1, x2, y2 = last_good_bbox
                # Ensure coordinates are within frame bounds
                x1 = max(0, min(x1, actual_width))
                y1 = max(0, min(y1, actual_height))
                x2 = max(0, min(x2, actual_width))
                y2 = max(0, min(y2, actual_height))
                
                if x2 > x1 and y2 > y1:  # Only copy if rectangle has positive dimensions
                    mask[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                
                if show_debug:
                    color = (0, 255, 0) if frames_since_detection == 0 else (0, 165, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            else:
                if show_debug:
                    cv2.putText(frame, "NO FACE DETECTED", (10, 90), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Send to virtual camera if enabled
            if ffmpeg_process and ffmpeg_process.stdin:
                try:
                    ffmpeg_process.stdin.write(mask.tobytes())
                except (BrokenPipeError, AttributeError):
                    print("✗ Virtual camera pipe broken")
                    ffmpeg_process = None
            
            # Show preview unless disabled
            if not args.no_preview:
                if show_debug:
                    # Show current settings on debug frame
                    y_pos = 30
                    cv2.putText(frame, f"W:{h_padding:.1f} H:{v_padding:.1f} Off:{v_offset}", 
                               (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    y_pos += 30
                    status = "TRACKING" if frames_since_detection == 0 else f"HOLDING ({frames_since_detection}/{max_frame_skip})"
                    color = (0, 255, 0) if frames_since_detection == 0 else (0, 165, 255)
                    cv2.putText(frame, status, (10, y_pos), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    y_pos += 30
                    smooth_mode = "AGGRESSIVE" if aggressive_smooth else "NORMAL"
                    cv2.putText(frame, f"Smooth: {smooth_mode}", 
                               (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    cv2.imshow('Debug - Eye Tracking', frame)
                
                # Show mask
                window_title = 'Eye Mask - ' + ('Streaming' if args.output else 'Preview')
                cv2.imshow(window_title, mask)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('+') or key == ord('='):
                h_padding = min(3.0, h_padding + 0.1)
                print(f"Width: {h_padding:.1f}")
            elif key == ord('-') or key == ord('_'):
                h_padding = max(0.8, h_padding - 0.1)
                print(f"Width: {h_padding:.1f}")
            elif key == ord(']'):
                v_padding = min(2.0, v_padding + 0.1)
                print(f"Height: {v_padding:.1f}")
            elif key == ord('['):
                v_padding = max(0.4, v_padding - 0.1)
                print(f"Height: {v_padding:.1f}")
            elif key == 82:  # Up arrow
                v_offset -= 2
                print(f"Offset: {v_offset}")
            elif key == 84:  # Down arrow
                v_offset += 2
                print(f"Offset: {v_offset}")
            elif key == ord('r'):
                center_x_filter.reset()
                center_y_filter.reset()
                width_filter.reset()
                height_filter.reset()
                frames_since_detection = 0
                print("Smoothing reset")
            elif key == ord('d'):
                show_debug = not show_debug
                if not show_debug and not args.no_preview:
                    cv2.destroyWindow('Debug - Eye Tracking')
            elif key == ord('f'):
                aggressive_smooth = not aggressive_smooth
                # Update smoothing parameters
                if aggressive_smooth:
                    center_x_filter.alpha = 0.15
                    center_y_filter.alpha = 0.15
                    width_filter.alpha = 0.1
                    height_filter.alpha = 0.1
                    max_frame_skip = 3
                    print("Aggressive smoothing ON")
                else:
                    center_x_filter.alpha = DEFAULT_POSITION_SMOOTHING
                    center_y_filter.alpha = DEFAULT_POSITION_SMOOTHING
                    width_filter.alpha = DEFAULT_SIZE_SMOOTHING
                    height_filter.alpha = DEFAULT_SIZE_SMOOTHING
                    max_frame_skip = DEFAULT_MAX_FRAME_SKIP
                    print("Normal smoothing")
    
    except KeyboardInterrupt:
        print("\n✓ Interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        # Clean up
        if ffmpeg_process:
            try:
                ffmpeg_process.stdin.close()
                ffmpeg_process.wait()
            except:
                pass
        
        cap.release()
        cv2.destroyAllWindows()
        print("✓ Done!")

if __name__ == "__main__":
    main()
