from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass(slots=True)
class FrameMessage:
    topic: str
    frame_index: int
    timestamp_s: float
    image: np.ndarray
    source_name: str


@dataclass(slots=True)
class TwistCommand:
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    throttle: float = 0.0


@dataclass(slots=True)
class TelemetryMessage:
    timestamp_s: float
    gps_lon: Optional[float] = None
    gps_lat: Optional[float] = None
    gps_alt_m: Optional[float] = None
    barometer_m: Optional[float] = None


@dataclass(slots=True)
class TargetDetection:
    found: bool
    cx: float = 0.0
    cy: float = 0.0
    area: float = 0.0
    error_x: float = 0.0
    error_y: float = 0.0


@dataclass(slots=True)
class DroneState:
    mode: str = "IDLE"
    cmd: TwistCommand = field(default_factory=TwistCommand)
    target: Optional[TargetDetection] = None
    telemetry: Optional[TelemetryMessage] = None
