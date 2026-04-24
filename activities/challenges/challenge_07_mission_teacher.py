"""Teacher reference solution for Challenge 7."""

from dataclasses import dataclass


@dataclass
class TargetDetection:
    found: bool
    error_x: float = 0.0
    error_y: float = 0.0


@dataclass
class TwistCommand:
    yaw: float = 0.0
    throttle: float = 0.0


class MissionManager:
    def __init__(self) -> None:
        self.state = "SEARCH"
        self.hold_counter = 0

    def step(self, target: TargetDetection) -> TwistCommand:
        if not target.found:
            self.state = "SEARCH"
            self.hold_counter = 0
            return TwistCommand(yaw=0.2)

        if abs(target.error_x) > 0.08 or abs(target.error_y) > 0.08:
            self.state = "ALIGN"
            self.hold_counter = 0
            return TwistCommand()

        self.hold_counter += 1
        if self.hold_counter < 3:
            self.state = "HOLD"
            return TwistCommand()

        self.state = "LAND"
        return TwistCommand(throttle=-0.25)


def main() -> None:
    manager = MissionManager()
    sequence = [
        TargetDetection(False),
        TargetDetection(True, 0.30, -0.10),
        TargetDetection(True, 0.04, 0.03),
        TargetDetection(True, 0.02, 0.01),
        TargetDetection(True, 0.01, 0.01),
    ]
    for step_id, target in enumerate(sequence):
        cmd = manager.step(target)
        print(step_id, manager.state, cmd)


if __name__ == "__main__":
    main()
