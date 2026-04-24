"""Challenge 8: integrate the full mock drone pipeline."""

from dataclasses import dataclass
from pathlib import Path
import math

import cv2
import numpy as np
from video_config import get_video_path


VIDEO_PATH = get_video_path("DJI_0790.MOV")


@dataclass
class TargetDetection:
    found: bool
    cx: float = 0.0
    cy: float = 0.0
    error_x: float = 0.0
    error_y: float = 0.0
    area: float = 0.0


@dataclass
class TwistCommand:
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    throttle: float = 0.0


class DronePipeline:
    def add_target(self, frame: np.ndarray, time_s: float) -> np.ndarray:
        # TODO 1:
        # Add a red moving target to the image.
        return frame

    def detect_target(self, frame: np.ndarray) -> TargetDetection:
        # TODO 2:
        # Detect the red target and compute normalized error.
        return TargetDetection(False)

    def compute_command(self, detection: TargetDetection) -> TwistCommand:
        # TODO 3:
        # Reuse proportional control ideas from Challenge 6.
        return TwistCommand()

    def draw_hud(self, frame: np.ndarray, detection: TargetDetection, cmd: TwistCommand) -> np.ndarray:
        # TODO 4:
        # Draw target and command information on the image.
        return frame


def main() -> None:
    pipe = DronePipeline()
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_index = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.resize(frame, dsize=None, fx=0.3, fy=0.3)
        time_s = frame_index / fps
        frame = pipe.add_target(frame, time_s)
        detection = pipe.detect_target(frame)
        cmd = pipe.compute_command(detection)
        frame = pipe.draw_hud(frame, detection, cmd)

        cv2.imshow("challenge_08", frame)
        if (cv2.waitKey(20) & 0xFF) == ord("q"):
            break
        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
