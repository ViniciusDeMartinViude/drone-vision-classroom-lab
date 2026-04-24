from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from drone_lab.core.bus import MessageBus
from drone_lab.core.messages import DroneState, TwistCommand
from drone_lab.nodes.camera import CameraNode
from drone_lab.nodes.control import PControllerNode
from drone_lab.nodes.hud import HudNode
from drone_lab.nodes.mission import MissionNode
from drone_lab.nodes.target import TargetDetectorNode, VirtualTargetNode
from drone_lab.nodes.telemetry import TelemetryNode

DATASET_ROOT = Path(r"F:\datasets\drone")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Drone video lab")
    parser.add_argument("--scenario", choices=["teleop", "tracker", "mission"], default="teleop")
    parser.add_argument("--video", default=str(DATASET_ROOT / "DJI_0574.MP4"))
    parser.add_argument("--scale", type=float, default=0.5, help="Resize factor for large videos")
    parser.add_argument("--show-mask", action="store_true")
    return parser.parse_args()


def teleop_key_to_cmd(key: int, current: TwistCommand) -> tuple[TwistCommand, bool]:
    step = 0.1
    quit_requested = False
    if key == ord("a"):
        current.roll -= step
    elif key == ord("d"):
        current.roll += step
    elif key == ord("w"):
        current.pitch += step
    elif key == ord("s"):
        current.pitch -= step
    elif key == ord("j"):
        current.yaw -= step
    elif key == ord("l"):
        current.yaw += step
    elif key == ord("i"):
        current.throttle += step
    elif key == ord("k"):
        current.throttle -= step
    elif key == ord(" "):
        current = TwistCommand()
    elif key == ord("q"):
        quit_requested = True

    current.roll = max(-1.0, min(1.0, current.roll))
    current.pitch = max(-1.0, min(1.0, current.pitch))
    current.yaw = max(-1.0, min(1.0, current.yaw))
    current.throttle = max(-1.0, min(1.0, current.throttle))
    return current, quit_requested


def run() -> None:
    args = parse_args()
    bus = MessageBus()
    camera = CameraNode(bus, args.video, scale=args.scale)
    hud = HudNode(show_mask=args.show_mask)
    telemetry = TelemetryNode(args.video)
    virtual_target = VirtualTargetNode()
    detector = TargetDetectorNode()
    controller = PControllerNode()
    mission = MissionNode()
    state = DroneState(mode="MANUAL" if args.scenario == "teleop" else "AUTO")

    frame_index = 0
    while True:
        frame_msg = camera.read(frame_index)
        if frame_msg is None:
            break

        telemetry_msg = telemetry.latest_for(frame_msg.timestamp_s)
        target = None
        mask = None

        if args.scenario in {"tracker", "mission"}:
            frame_msg = virtual_target.annotate(frame_msg)
            target, mask = detector.detect(frame_msg)
            auto_cmd = controller.compute(target)
            if args.scenario == "tracker":
                state.mode = "TRACK"
                state.target = target
                state.cmd = auto_cmd
            else:
                mode, mission_cmd = mission.step(target, auto_cmd)
                state.mode = mode
                state.target = target
                state.cmd = mission_cmd

        frame = hud.draw(frame_msg, state, target=target, telemetry=telemetry_msg, mask=mask)
        cv2.imshow("drone_lab", frame)
        key = cv2.waitKey(15) & 0xFF

        if args.scenario == "teleop":
            state.cmd, quit_requested = teleop_key_to_cmd(key, state.cmd)
            if quit_requested:
                break
        elif key == ord("q"):
            break

        frame_index += 1

    camera.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
