from __future__ import annotations

import re
from pathlib import Path

from drone_lab.core.messages import TelemetryMessage

GPS_RE = re.compile(r"GPS\(([-0-9.]+),([-0-9.]+),([-0-9.]+)\)")
BARO_RE = re.compile(r"BAROMETER:([-0-9.]+)")


class TelemetryNode:
    def __init__(self, video_path: str) -> None:
        self.entries = self._load_entries(video_path)

    def _load_entries(self, video_path: str) -> list[TelemetryMessage]:
        path = Path(video_path)
        srt_path = path.with_suffix(".SRT")
        if not srt_path.exists():
            return []

        entries: list[TelemetryMessage] = []
        text = srt_path.read_text(encoding="utf-8", errors="ignore")
        blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
        for block in blocks:
            lines = block.splitlines()
            if len(lines) < 4:
                continue
            timing_line = lines[1]
            payload = " ".join(lines[2:])
            gps_match = GPS_RE.search(payload)
            baro_match = BARO_RE.search(payload)
            timestamp_s = self._parse_timecode(timing_line.split(" --> ")[0])
            msg = TelemetryMessage(timestamp_s=timestamp_s)
            if gps_match:
                msg.gps_lon = float(gps_match.group(1))
                msg.gps_lat = float(gps_match.group(2))
                msg.gps_alt_m = float(gps_match.group(3))
            if baro_match:
                msg.barometer_m = float(baro_match.group(1))
            entries.append(msg)
        return entries

    @staticmethod
    def _parse_timecode(text: str) -> float:
        hh, mm, rest = text.split(":")
        ss, ms = rest.split(",")
        return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0

    def latest_for(self, timestamp_s: float) -> TelemetryMessage | None:
        latest = None
        for entry in self.entries:
            if entry.timestamp_s <= timestamp_s:
                latest = entry
            else:
                break
        return latest
