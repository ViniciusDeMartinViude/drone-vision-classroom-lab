"""Challenge 2: frame packets with NumPy statistics."""

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
        # TODO 1:
        # Validate the capture and read FPS.
        return False

    def read_packet(self) -> FramePacket | None:
        # TODO 2:
        # Read a frame. Return None at the end of the video.
        ok, frame = False, None

        # TODO 3:
        # Resize the image.

        # TODO 4:
        # Compute brightness using NumPy on a grayscale image.
        brightness = 0.0
        timestamp_s = self.frame_index / self.fps

        # TODO 5:
        # Build and return a FramePacket instance.
        return None


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
        cv2.imshow("challenge_02", packet.image)
        if (cv2.waitKey(20) & 0xFF) == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
