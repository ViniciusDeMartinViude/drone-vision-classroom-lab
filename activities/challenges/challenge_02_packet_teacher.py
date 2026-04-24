"""Teacher reference solution for Challenge 2."""

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from video_config import get_video_path


VIDEO_PATH = get_video_path("Stockflue Flyaround.mp4")


@dataclass
class FramePacket:
    frame_index: int
    timestamp_s: float
    image: np.ndarray
    brightness: float


class CameraNode:
    def __init__(self, video_path: Path, scale: float = 0.5) -> None:
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

    def read_packet(self) -> FramePacket | None:
        ok, frame = self.cap.read()
        if not ok:
            return None

        frame = cv2.resize(frame, dsize=None, fx=self.scale, fy=self.scale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))
        timestamp_s = self.frame_index / self.fps
        packet = FramePacket(self.frame_index, timestamp_s, frame, brightness)
        self.frame_index += 1
        return packet


def main() -> None:
    node = CameraNode(VIDEO_PATH, scale=0.5)
    if not node.open():
        print(f"Could not open video: {VIDEO_PATH}")
        return

    while True:
        packet = node.read_packet()
        if packet is None:
            break

        cv2.putText(packet.image, f"brightness: {packet.brightness:6.1f}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(packet.image, f"frame: {packet.frame_index}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("challenge_02", packet.image)
        if (cv2.waitKey(20) & 0xFF) == ord("q"):
            break

    node.cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
