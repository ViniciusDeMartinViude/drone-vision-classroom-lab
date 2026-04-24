"""Challenge 5: create and detect a virtual target."""

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
        # TODO 1:
        # Draw a moving red circle on the frame.
        return frame

    def detect(self, frame: np.ndarray) -> tuple[TargetDetection, np.ndarray]:
        # TODO 2:
        # Convert to HSV and threshold a red target.
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)

        # TODO 3:
        # Use NumPy to compute centroid and area.
        return TargetDetection(False), mask


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

        # TODO 4:
        # Draw centroid and area if the target is found.

        cv2.imshow("challenge_05", frame)
        cv2.imshow("challenge_05_mask", mask)
        if (cv2.waitKey(20) & 0xFF) == ord("q"):
            break
        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
