"""Teacher reference solution for Challenge 3."""

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
        if key == ord("a"):
            self.cmd.roll -= step
        elif key == ord("d"):
            self.cmd.roll += step
        elif key == ord("w"):
            self.cmd.pitch += step
        elif key == ord("s"):
            self.cmd.pitch -= step
        elif key == ord("j"):
            self.cmd.yaw -= step
        elif key == ord("l"):
            self.cmd.yaw += step
        elif key == ord("i"):
            self.cmd.throttle += step
        elif key == ord("k"):
            self.cmd.throttle -= step
        elif key == ord(" "):
            self.cmd = TwistCommand()

        self.cmd.roll = max(-1.0, min(1.0, self.cmd.roll))
        self.cmd.pitch = max(-1.0, min(1.0, self.cmd.pitch))
        self.cmd.yaw = max(-1.0, min(1.0, self.cmd.yaw))
        self.cmd.throttle = max(-1.0, min(1.0, self.cmd.throttle))

    def draw(self, frame):
        lines = [
            f"roll: {self.cmd.roll:+.2f}",
            f"pitch: {self.cmd.pitch:+.2f}",
            f"yaw: {self.cmd.yaw:+.2f}",
            f"throttle: {self.cmd.throttle:+.2f}",
        ]
        y = 30
        for line in lines:
            cv2.putText(frame, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 50), 2)
            y += 30
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
