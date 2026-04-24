"""Teacher reference solution for Challenge 1."""

from pathlib import Path

import cv2
from video_config import get_video_path


VIDEO_PATH = get_video_path("Bluemlisalphutte Flyover.mp4")
SCALE = 0.60


class DroneVideoPlayer:
    def __init__(self, video_path: Path, scale: float) -> None:
        self.video_path = video_path
        self.scale = scale
        self.cap = cv2.VideoCapture(str(video_path))
        self.fps = 30.0
        self.frame_index = 0

    def open(self) -> bool:
        if not self.cap.isOpened():
            return False
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        return True

    def draw_overlay(self, frame, timestamp_s: float):
        cv2.putText(frame, f"frame: {self.frame_index}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"time: {timestamp_s:5.2f}s", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        return frame

    def run(self) -> None:
        if not self.open():
            print(f"Could not open video: {self.video_path}")
            return

        while True:
            ok, frame = self.cap.read()
            if not ok:
                break

            frame = cv2.resize(frame, dsize=None, fx=self.scale, fy=self.scale)
            timestamp_s = self.frame_index / self.fps
            frame = self.draw_overlay(frame, timestamp_s)
            cv2.imshow("challenge_01", frame)

            key = cv2.waitKey(20) & 0xFF
            if key == ord("q"):
                break

            self.frame_index += 1

        self.cap.release()
        cv2.destroyAllWindows()


def main() -> None:
    player = DroneVideoPlayer(VIDEO_PATH, SCALE)
    player.run()


if __name__ == "__main__":
    main()
