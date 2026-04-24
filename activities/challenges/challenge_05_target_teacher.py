"""Teacher reference solution for Challenge 5."""

from dataclasses import dataclass
from pathlib import Path
import math

import cv2
import numpy as np
from video_config import get_video_path


VIDEO_PATH = get_video_path("DJI_0596.MP4")


@dataclass
class TargetDetection:
    found: bool
    cx: float = 0.0
    cy: float = 0.0
    area: float = 0.0


class VirtualTargetTracker:
    def add_target(self, frame: np.ndarray, time_s: float) -> np.ndarray:
        h, w = frame.shape[:2]
        cx = int(w * (0.5 + 0.2 * math.sin(0.8 * time_s)))
        cy = int(h * (0.5 + 0.2 * math.cos(0.6 * time_s)))
        cv2.circle(frame, (cx, cy), 18, (0, 0, 255), -1)
        return frame

    def detect(self, frame: np.ndarray) -> tuple[TargetDetection, np.ndarray]:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, np.array([0, 140, 120]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 140, 120]), np.array([180, 255, 255]))
        mask = cv2.bitwise_or(mask1, mask2)
        ys, xs = np.where(mask > 0)
        if xs.size == 0:
            return TargetDetection(False), mask
        return TargetDetection(True, float(xs.mean()), float(ys.mean()), float(xs.size)), mask


def main() -> None:
    tracker = VirtualTargetTracker()
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_index = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.resize(frame, dsize=None, fx=0.4, fy=0.4)
        time_s = frame_index / fps
        frame = tracker.add_target(frame, time_s)
        detection, mask = tracker.detect(frame)

        if detection.found:
            cv2.circle(frame, (int(detection.cx), int(detection.cy)), 20, (0, 255, 255), 2)
            cv2.putText(frame, f"area: {detection.area:.0f}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("challenge_05", frame)
        cv2.imshow("challenge_05_mask", mask)
        if (cv2.waitKey(20) & 0xFF) == ord("q"):
            break
        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
