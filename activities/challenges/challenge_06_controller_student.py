"""Challenge 6: proportional controller from image error."""

from dataclasses import dataclass


@dataclass
class TargetDetection:
    found: bool
    error_x: float = 0.0
    error_y: float = 0.0
    area: float = 0.0


@dataclass
class TwistCommand:
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    throttle: float = 0.0


class PController:
    def __init__(self, k_roll: float, k_yaw: float, k_throttle: float) -> None:
        self.k_roll = k_roll
        self.k_yaw = k_yaw
        self.k_throttle = k_throttle

    def clamp(self, value: float, limit: float) -> float:
        # TODO 1:
        # Limit value to [-limit, +limit].
        return value

    def compute(self, target: TargetDetection) -> TwistCommand:
        if not target.found:
            # TODO 2:
            # Return a search command when the target is missing.
            return TwistCommand()

        # TODO 3:
        # Convert image error into roll, yaw, and throttle.
        # Add forward pitch only when the target area is small.
        return TwistCommand()


def main() -> None:
    controller = PController(k_roll=0.7, k_yaw=0.4, k_throttle=0.6)
    examples = [
        TargetDetection(True, error_x=0.30, error_y=-0.20, area=500),
        TargetDetection(True, error_x=-0.10, error_y=0.05, area=1200),
        TargetDetection(False),
    ]
    for example in examples:
        print(example, "->", controller.compute(example))


if __name__ == "__main__":
    main()
