"""Challenge 4: parse DJI telemetry."""

from dataclasses import dataclass
from pathlib import Path
import re

import cv2
from video_config import get_video_path


VIDEO_PATH = get_video_path("DJI_0574.MP4")


@dataclass
class TelemetrySample:
    time_s: float
    latitude: float | None = None
    longitude: float | None = None
    altitude_m: float | None = None
    barometer_m: float | None = None


class TelemetryParser:
    def __init__(self, video_path: Path) -> None:
        self.video_path = video_path
        self.samples: list[TelemetrySample] = []

    def load(self) -> None:
        srt_path = self.video_path.with_suffix(".SRT")
        # TODO 1:
        # Read the SRT file and split it into subtitle blocks.

        # TODO 2:
        # Parse time, GPS and barometer data into TelemetrySample objects.

    def latest(self, time_s: float) -> TelemetrySample | None:
        latest_sample = None
        # TODO 3:
        # Return the latest sample at or before time_s.
        return latest_sample


def parse_timecode(text: str) -> float:
    hh, mm, rest = text.split(":")
    ss, ms = rest.split(",")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0


def main() -> None:
    parser = TelemetryParser(VIDEO_PATH)
    parser.load()
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_index = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.resize(frame, dsize=None, fx=0.4, fy=0.4)
        current_time = frame_index / fps
        sample = parser.latest(current_time)

        # TODO 4:
        # Draw telemetry text on the frame if a sample exists.

        cv2.imshow("challenge_04", frame)
        if (cv2.waitKey(20) & 0xFF) == ord("q"):
            break
        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
