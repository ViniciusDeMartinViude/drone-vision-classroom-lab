from __future__ import annotations

from drone_lab.core.messages import TargetDetection, TwistCommand


def clamp(value: float, limit: float) -> float:
    return max(-limit, min(limit, value))


class PControllerNode:
    def __init__(self, k_roll: float = 0.7, k_throttle: float = 0.6, k_yaw: float = 0.4) -> None:
        self.k_roll = k_roll
        self.k_throttle = k_throttle
        self.k_yaw = k_yaw

    def compute(self, target: TargetDetection | None) -> TwistCommand:
        if target is None or not target.found:
            return TwistCommand(yaw=0.15)
        return TwistCommand(
            roll=clamp(-self.k_roll * target.error_x, 1.0),
            pitch=0.25 if target.area < 900 else 0.0,
            yaw=clamp(-self.k_yaw * target.error_x, 0.8),
            throttle=clamp(-self.k_throttle * target.error_y, 0.8),
        )
