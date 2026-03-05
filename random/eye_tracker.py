#!/usr/bin/env python3
"""
Simple stabilized eye mask using Haar cascades.
"""

import cv2
from collections import deque

# Tunables
H_PADDING = 1.2
V_PADDING = 0.6
V_OFFSET = -10

SMOOTH_FRAMES = 5
MIN_EYE_DIST = 30
MAX_EYE_DIST = 120


class EyeTracker:
    def __init__(self):
        base = cv2.data.haarcascades
        self.face = cv2.CascadeClassifier(base + "haarcascade_frontalface_default.xml")
        self.eye = cv2.CascadeClassifier(base + "haarcascade_eye.xml")

        self.centers = deque(maxlen=SMOOTH_FRAMES)
        self.widths = deque(maxlen=SMOOTH_FRAMES)
        self.heights = deque(maxlen=SMOOTH_FRAMES)

        self.last_box = None
        self.lost_frames = 0

    def _avg(self, buf):
        return sum(buf) / len(buf) if buf else 0

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return None

        fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])
        roi = gray[fy:fy+fh, fx:fx+fw]

        eyes = self.eye.detectMultiScale(roi)

        pts = []
        mid_y = fy + fh // 2

        for ex, ey, ew, eh in eyes:
            cx = fx + ex + ew // 2
            cy = fy + ey + eh // 2
            if cy < mid_y:
                pts.append((cx, cy))

        if len(pts) < 2:
            return None

        pts.sort()
        d = abs(pts[1][0] - pts[0][0])

        if d < MIN_EYE_DIST or d > MAX_EYE_DIST:
            return None

        return pts[:2], d

    def update(self, frame, hp, vp, vo):
        result = self.detect(frame)

        if result is None:
            self.lost_frames += 1
            if self.last_box and self.lost_frames < 10:
                return self.last_box, False
            return None, False

        self.lost_frames = 0
        (x1, y1), (x2, y2), = result[0]
        dist = result[1]

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        self.centers.append((cx, cy))
        self.widths.append(dist * hp)
        self.heights.append(dist * vp)

        ax = int(self._avg([c[0] for c in self.centers]))
        ay = int(self._avg([c[1] for c in self.centers]))
        aw = int(self._avg(self.widths))
        ah = int(self._avg(self.heights))

        x1 = max(0, ax - aw // 2)
        y1 = max(0, ay - ah // 2 + vo)
        x2 = min(frame.shape[1], ax + aw // 2)
        y2 = min(frame.shape[0], ay + ah // 2 + vo)

        self.last_box = (x1, y1, x2, y2)
        return self.last_box, True


def main():
    tracker = EyeTracker()
    cam = cv2.VideoCapture(0)

    hp, vp, vo = H_PADDING, V_PADDING, V_OFFSET
    debug = True

    print("Eye mask running. Press q to quit.")

    while True:
        ok, frame = cam.read()
        if not ok:
            break

        result = tracker.update(frame, hp, vp, vo)

        mask = frame * 0

        if result[0]:
            x1, y1, x2, y2 = result[0]
            mask[y1:y2, x1:x2] = frame[y1:y2, x1:x2]

            if debug:
                color = (0, 255, 0) if result[1] else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        if debug:
            cv2.imshow("debug", frame)

        cv2.imshow("mask", mask)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key in (ord('+'), ord('=')):
            hp = min(3.0, hp + 0.1)
        elif key in (ord('-'), ord('_')):
            hp = max(0.8, hp - 0.1)
        elif key == ord(']'):
            vp = min(2.0, vp + 0.1)
        elif key == ord('['):
            vp = max(0.4, vp - 0.1)
        elif key == 82:
            vo -= 2
        elif key == 84:
            vo += 2
        elif key == ord('d'):
            debug = not debug

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
