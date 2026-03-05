#!/usr/bin/env python3
"""
Eye Mask - With your custom defaults
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

# ===== YOUR CUSTOM DEFAULTS =====
HORIZONTAL_PADDING = 2.1    # Width setting (was 1.2)
VERTICAL_PADDING = 0.6       # Height setting (was 0.6)
VERTICAL_OFFSET = -2         # Vertical offset (was -10)
# ================================

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
    args = parser.parse_args()
    
    # Parse resolution
    try:
        width, height = map(int, args.resolution.split('x'))
    except:
        print("✗ Invalid resolution format. Using 640x480")
        width, height = 640, 480
    
    print("\n" + "="*50)
    print("EYE MASK - REAL-TIME")
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
    print("="*50 + "\n")
    
    # Interactive variables (start with your custom defaults)
    h_padding = HORIZONTAL_PADDING
    v_padding = VERTICAL_PADDING
    v_offset = VERTICAL_OFFSET
    show_debug = True
    
    # Smoothing buffers
    from collections import deque
    center_buffer = deque(maxlen=5)

    # Smooth tracking
    smooth_x = None
    smooth_y = None
    SMOOTHING = 0.75

# Face tracking optimization
    frame_count = 0
    last_face = None
# Eye loss handling
    last_center = None
    lost_frames = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("✗ Failed to grab frame")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(frame)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Detect eyes in face region
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            if len(eyes) >= 2:
                # Sort eyes by x position
                eyes = sorted(eyes, key=lambda e: e[0])[:2]
                
                # Calculate eye centers
                eye_coords = []
                for (ex, ey, ew, eh) in eyes:
                    eye_coords.append((x + ex + ew//2, y + ey + eh//2))
                
                # Calculate eye distance and center
                eye_distance = abs(eye_coords[0][0] - eye_coords[1][0])
                center_x = (eye_coords[0][0] + eye_coords[1][0]) // 2
                center_y = (eye_coords[0][1] + eye_coords[1][1]) // 2
                
                # Add to smoothing buffer
                center_buffer.append((center_x, center_y))
                avg_center = np.mean(center_buffer, axis=0).astype(int)
                
                # Calculate rectangle using your custom defaults
                rect_width = int(eye_distance * h_padding)
                rect_height = int(eye_distance * v_padding)
                
                x1 = max(0, avg_center[0] - rect_width//2)
                y1 = max(0, avg_center[1] - rect_height//2 + v_offset)
                x2 = min(frame.shape[1], avg_center[0] + rect_width//2)
                y2 = min(frame.shape[0], avg_center[1] + rect_height//2 + v_offset)
                
                # Copy eye region to mask
                mask[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
                
                if show_debug:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Send to virtual camera if enabled
        if ffmpeg_process and ffmpeg_process.stdin:
            try:
                ffmpeg_process.stdin.write(mask.tobytes())
            except BrokenPipeError:
                print("✗ Virtual camera pipe broken")
                ffmpeg_process = None
        
        # Show preview unless disabled
        if not args.no_preview:
            if show_debug:
                # Show current settings on debug frame
                cv2.putText(frame, f"W:{h_padding:.1f} H:{v_padding:.1f} Off:{v_offset}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('Debug - Eye Tracking', frame)
            cv2.imshow('Eye Mask - ' + ('Streaming' if args.output else 'Preview'), mask)
        
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
            center_buffer.clear()
            print("Smoothing reset")
        elif key == ord('d'):
            show_debug = not show_debug
            if not show_debug and not args.no_preview:
                cv2.destroyWindow('Debug - Eye Tracking')
    
    # Clean up
    if ffmpeg_process:
        ffmpeg_process.stdin.close()
        ffmpeg_process.wait()
    
    cap.release()
    cv2.destroyAllWindows()
    print("✓ Done!")

if __name__ == "__main__":
    main()
