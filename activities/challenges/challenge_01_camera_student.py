"""Challenge 1: camera viewer with a class."""

from pathlib import Path

import cv2
from video_config import get_video_path


VIDEO_PATH = get_video_path("Bluemlisalphutte Flyover.mp4")
SCALE = 0.60


class DroneVideoPlayer:
    def __init__(self, video_path: Path, scale: float) -> None:
        self.video_path = video_path
        self.scale = scale
        # TODO 1:
        # Open the video with cv2.VideoCapture.
        self.cap = None
        self.fps = 30.0
        self.frame_index = 0

    def open(self) -> bool:
        # TODO 2:
        # Check whether the video opened correctly.
        # Return True if it worked, False otherwise.
        return False

    def draw_overlay(self, frame, timestamp_s: float):
        # TODO 3:
        # Draw the frame number on the image.

        # TODO 4:
        # Draw the timestamp on the image.
        return frame

    def run(self) -> None:
        if not self.open():
            print(f"Could not open video: {self.video_path}")
            return

        while True:
            # TODO 5:
            # Read the next frame from the video.
            ok, frame = False, None

            # TODO 6:
            # If the video ended, break the loop.

            # TODO 7:
            # Resize the frame using self.scale.

            timestamp_s = self.frame_index / self.fps
            frame = self.draw_overlay(frame, timestamp_s)

            # TODO 8:
            # Show the image in a window named "challenge_01".

            key = cv2.waitKey(20) & 0xFF
            if key == ord("q"):
                break

            self.frame_index += 1

        # TODO 9:
        # Release the video and close OpenCV windows.


def main() -> None:
    player = DroneVideoPlayer(VIDEO_PATH, SCALE)
    player.run()


if __name__ == "__main__":
    main()
