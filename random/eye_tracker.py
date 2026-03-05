#!/usr/bin/env python3
"""
Stabilized Eye Mask - With tracking error fixes
"""

import cv2
import numpy as np
import os
from collections import deque

# Configuration
HORIZONTAL_PADDING = 1.2
VERTICAL_PADDING = 0.6
VERTICAL_OFFSET = -10

# Smoothing - reduces jumping
SMOOTHING_FRAMES = 5  # Average over last 5 frames
MIN_EYE_DISTANCE = 30  # Ignore detections that are too close (nostrils)
MAX_EYE_DISTANCE = 120  # Ignore detections that are too far (errors)

class StabilizedEyeMask:
    def __init__(self):
        # Find cascade files
        cascade_paths = [
            '/usr/share/opencv4/haarcascades/',
            '/usr/local/share/opencv4/haarcascades/',
            '/usr/share/OpenCV/haarcascades/',
        ]
        
        self.face_cascade = self.eye_cascade = None
        for path in cascade_paths:
            face_file = os.path.join(path, 'haarcascade_frontalface_default.xml')
            eye_file = os.path.join(path, 'haarcascade_eye.xml')
            if os.path.exists(face_file) and os.path.exists(eye_file):
                self.face_cascade = cv2.CascadeClassifier(face_file)
                self.eye_cascade = cv2.CascadeClassifier(eye_file)
                print(f"Found cascades in: {path}")
                break
        
        # Smoothing buffers
        self.center_buffer = deque(maxlen=SMOOTHING_FRAMES)
        self.width_buffer = deque(maxlen=SMOOTHING_FRAMES)
        self.height_buffer = deque(maxlen=SMOOTHING_FRAMES)
        
        # Error tracking
        self.last_good_bbox = None
        self.error_frames = 0
    
    def get_eyes(self, frame):
        """Enhanced eye detection with filtering"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return None
        
        # Use largest face
        face = max(faces, key=lambda f: f[2] * f[3])
        fx, fy, fw, fh = face
        
        # Detect eyes in face region
        roi_gray = gray[fy:fy+fh, fx:fx+fw]
        eyes = self.eye_cascade.detectMultiScale(roi_gray)
        
        if len(eyes) < 2:
            return None
        
        # Convert to full frame coordinates and filter
        eye_coords = []
        for (ex, ey, ew, eh) in eyes:
            # Calculate eye center
            eye_x = fx + ex + ew//2
            eye_y = fy + ey + eh//2
            
            # Filter out detections that are too low (mouth area)
            face_center_y = fy + fh//2
            if eye_y < face_center_y:  # Only keep detections in upper half of face
                eye_coords.append((eye_x, eye_y))
        
        if len(eye_coords) < 2:
            return None
        
        # Sort by x position and take two most plausible eyes
        eye_coords = sorted(eye_coords, key=lambda c: c[0])
        
        # Check if the two eyes are plausibly spaced
        eye_distance = abs(eye_coords[1][0] - eye_coords[0][0])
        if eye_distance < MIN_EYE_DISTANCE or eye_distance > MAX_EYE_DISTANCE:
            return None
        
        return eye_coords[:2], eye_distance
    
    def process_frame(self, frame, h_padding, v_padding, v_offset):
        """Process frame with stabilization"""
        result = self.get_eyes(frame)
        
        if result is None:
            self.error_frames += 1
            
            # If we've lost tracking, use last known good position for a few frames
            if self.last_good_bbox and self.error_frames < 10:
                return self.last_good_bbox, False
            return None, False
        
        self.error_frames = 0
        eye_coords, eye_distance = result
        
        # Calculate current frame's rectangle
        center_x = (eye_coords[0][0] + eye_coords[1][0]) // 2
        center_y = (eye_coords[0][1] + eye_coords[1][1]) // 2
        
        # Add to smoothing buffers
        self.center_buffer.append((center_x, center_y))
        self.width_buffer.append(eye_distance * h_padding)
        self.height_buffer.append(eye_distance * v_padding)
        
        # Use averaged values
        avg_center = np.mean(self.center_buffer, axis=0).astype(int)
        avg_width = np.mean(self.width_buffer)
        avg_height = np.mean(self.height_buffer)
        
        # Calculate rectangle
        x1 = max(0, avg_center[0] - int(avg_width//2))
        y1 = max(0, avg_center[1] - int(avg_height//2) + v_offset)
        x2 = min(frame.shape[1], avg_center[0] + int(avg_width//2))
        y2 = min(frame.shape[0], avg_center[1] + int(avg_height//2) + v_offset)
        
        bbox = (x1, y1, x2, y2)
        self.last_good_bbox = bbox
        return bbox, True

def main():
    # Initialize
    stabilizer = StabilizedEyeMask()
    
    if stabilizer.face_cascade is None:
        print("ERROR: Could not find Haar cascade files!")
        return
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return
    
    print("\n" + "="*60)
    print("STABILIZED EYE MASK")
    print("="*60)
    print("Controls:")
    print("  + / -      : Adjust width")
    print("  ] / [      : Adjust height")
    print("  Up/Down    : Move rectangle up/down")
    print("  r          : Reset smoothing")
    print("  d          : Toggle debug info")
    print("  q          : Quit")
    print("="*60 + "\n")
    
    h_padding = HORIZONTAL_PADDING
    v_padding = VERTICAL_PADDING
    v_offset = VERTICAL_OFFSET
    show_debug = True
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame
        result = stabilizer.process_frame(frame, h_padding, v_padding, v_offset)
        
        # Create mask
        mask = np.zeros_like(frame)
        
        if result:
            bbox, tracking = result
            x1, y1, x2, y2 = bbox
            mask[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
            
            if show_debug:
                # Green = tracking, Red = using last known position
                color = (0, 255, 0) if tracking else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Show tracking status
                status = "TRACKING" if tracking else "PREDICTING"
                cv2.putText(frame, status, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        if show_debug:
            # Show current settings
            cv2.putText(frame, f"W:{h_padding:.1f} H:{v_padding:.1f} Off:{v_offset}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Show windows
        cv2.imshow('Eye Mask', mask)
        if show_debug:
            cv2.imshow('Debug - Eye Tracking', frame)
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('+') or key == ord('='):
            h_padding = min(3.0, h_padding + 0.1)
        elif key == ord('-') or key == ord('_'):
            h_padding = max(0.8, h_padding - 0.1)
        elif key == ord(']'):
            v_padding = min(2.0, v_padding + 0.1)
        elif key == ord('['):
            v_padding = max(0.4, v_padding - 0.1)
        elif key == 82:  # Up arrow
            v_offset -= 2
        elif key == 84:  # Down arrow
            v_offset += 2
        elif key == ord('r'):
            # Reset smoothing
            stabilizer.center_buffer.clear()
            stabilizer.width_buffer.clear()
            stabilizer.height_buffer.clear()
            print("Smoothing reset")
        elif key == ord('d'):
            show_debug = not show_debug
            if not show_debug:
                cv2.destroyWindow('Debug - Eye Tracking')
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
