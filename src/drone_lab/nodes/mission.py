from __future__ import annotations

from drone_lab.core.messages import DroneState, TargetDetection, TwistCommand


class MissionNode:
    def __init__(self) -> None:
        self.state = "SEARCH"
        self.hold_frames = 0

    def step(self, target: TargetDetection | None, auto_cmd: TwistCommand) -> tuple[str, TwistCommand]:
        if target is None or not target.found:
            self.state = "SEARCH"
            self.hold_frames = 0
            return self.state, TwistCommand(yaw=0.2)

        if abs(target.error_x) > 0.08 or abs(target.error_y) > 0.08:
            self.state = "ALIGN"
            self.hold_frames = 0
            return self.state, auto_cmd

        self.hold_frames += 1
        if self.hold_frames < 20:
            self.state = "HOLD"
            return self.state, TwistCommand()

        self.state = "LAND"
        return self.state, TwistCommand(throttle=-0.25)

    def update_state(self, drone_state: DroneState, target: TargetDetection | None, cmd: TwistCommand) -> DroneState:
        drone_state.mode = self.state
        drone_state.target = target
        drone_state.cmd = cmd
        return drone_state
