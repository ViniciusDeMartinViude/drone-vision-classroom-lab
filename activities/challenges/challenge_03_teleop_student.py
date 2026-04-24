"""Challenge 3: manual piloting HUD."""

from dataclasses import dataclass
from pathlib import Path

import cv2
from video_config import get_video_path


VIDEO_PATH = get_video_path("Bluemlisalphutte Flyover.mp4")


@dataclass
class TwistCommand:
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    throttle: float = 0.0


class ManualPilot:
    def __init__(self) -> None:
        self.cmd = TwistCommand()

    def update_from_key(self, key: int) -> None:
        step = 0.1
        # TODO 1:
        # Map keys a/d to roll, w/s to pitch, j/l to yaw, i/k to throttle.

        # TODO 2:
        # Use space to reset all values to zero.

        # TODO 3:
        # Clamp each command to [-1.0, 1.0].

    def draw(self, frame):
        # TODO 4:
        # Draw roll, pitch, yaw, and throttle on the image.
        return frame


def main() -> None:
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    pilot = ManualPilot()
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.resize(frame, dsize=None, fx=0.6, fy=0.6)
        frame = pilot.draw(frame)
        cv2.imshow("challenge_03", frame)
        key = cv2.waitKey(20) & 0xFF
        if key == ord("q"):
            break
        pilot.update_from_key(key)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
