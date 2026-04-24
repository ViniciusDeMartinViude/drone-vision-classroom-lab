"""Teacher reference solution for Challenge 4."""

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
    gps_pattern = re.compile(r"GPS\(([-0-9.]+),([-0-9.]+),([-0-9.]+)\)")
    baro_pattern = re.compile(r"BAROMETER:([-0-9.]+)")

    def __init__(self, video_path: Path) -> None:
        self.video_path = video_path
        self.samples: list[TelemetrySample] = []

    def load(self) -> None:
        srt_path = self.video_path.with_suffix(".SRT")
        if not srt_path.exists():
            return
        blocks = [block.strip() for block in srt_path.read_text(encoding="utf-8", errors="ignore").split("\n\n") if block.strip()]
        for block in blocks:
            lines = block.splitlines()
            if len(lines) < 4:
                continue
            time_s = parse_timecode(lines[1].split(" --> ")[0])
            payload = " ".join(lines[2:])
            gps_match = self.gps_pattern.search(payload)
            baro_match = self.baro_pattern.search(payload)
            sample = TelemetrySample(time_s)
            if gps_match:
                sample.longitude = float(gps_match.group(1))
                sample.latitude = float(gps_match.group(2))
                sample.altitude_m = float(gps_match.group(3))
            if baro_match:
                sample.barometer_m = float(baro_match.group(1))
            self.samples.append(sample)

    def latest(self, time_s: float) -> TelemetrySample | None:
        latest_sample = None
        for sample in self.samples:
            if sample.time_s <= time_s:
                latest_sample = sample
            else:
                break
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

        if sample is not None:
            lines = [
                f"lat: {sample.latitude}",
                f"lon: {sample.longitude}",
                f"alt: {sample.altitude_m}",
                f"baro: {sample.barometer_m}",
            ]
            y = 30
            for line in lines:
                cv2.putText(frame, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                y += 28

        cv2.imshow("challenge_04", frame)
        if (cv2.waitKey(20) & 0xFF) == ord("q"):
            break
        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
