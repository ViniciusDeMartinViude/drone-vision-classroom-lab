from __future__ import annotations

import os
from pathlib import Path


# Edit this path once for the classroom machine, or set DRONE_VIDEO_DIR.
TEACHER_VIDEO_DIR = Path(r"F:\path\to\drone_videos")


def get_video_dir() -> Path:
    raw = os.environ.get("DRONE_VIDEO_DIR")
    if raw:
        return Path(raw)
    return TEACHER_VIDEO_DIR


def get_video_path(filename: str) -> Path:
    return get_video_dir() / filename
