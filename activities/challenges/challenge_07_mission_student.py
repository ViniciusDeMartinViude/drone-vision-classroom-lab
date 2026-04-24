"""Challenge 7: mission state machine."""

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
        # TODO 1:
        # If the target is missing, SEARCH by yawing slowly.

        # TODO 2:
        # If the target is visible but not centered, switch to ALIGN.

        # TODO 3:
        # If centered for several steps, HOLD and then LAND.
        return TwistCommand()


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
