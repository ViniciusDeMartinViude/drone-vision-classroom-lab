# Drone Vision Lab with OpenCV and NumPy

This project turns prerecorded drone videos into a classroom-friendly drone lab. Students work with OpenCV and NumPy now, while using a structure that mirrors how the same system would later be split into ROS 2 nodes, topics, and control loops.

The videos live in `F:\datasets\drone` and are treated as the drone's camera feed. Some DJI clips also include `.SRT` telemetry files, which we use as mock sensor data.

## Learning goals

- Read and process drone video streams with OpenCV.
- Represent drone data using message-like Python dataclasses.
- Simulate ROS 2-style nodes, topics, and timers without ROS 2 installed.
- Design perception, control, and mission logic as separate modules.
- Prepare students for later migration to ROS 2 with minimal redesign.

## Suggested conda environment

The examples were prepared for the conda environment:

- `cardd-paper-demo`

It already contains:

- `opencv-python 4.13.0`
- `numpy 2.2.6`

Run commands with:

```powershell
& C:\Users\Vinicius\anaconda3\envs\cardd-paper-demo\python.exe -m drone_lab.main --help
```

Or activate the env first:

```powershell
conda activate cardd-paper-demo
python -m drone_lab.main --help
```

## Project layout

```text
src/drone_lab/
  core/         # ROS 2-like bus, messages, and node base class
  nodes/        # camera, telemetry, tracker, controller, HUD
  main.py       # entry point for demos
activities/
  sequence.md   # classroom activity sequence
```

## Quick start

1. Add `src` to the Python path.
2. Run one of the scenarios below.

PowerShell:

```powershell
$env:PYTHONPATH = "F:\dev\drone\src"
conda activate cardd-paper-demo
python -m drone_lab.main --scenario teleop --video "F:\datasets\drone\DJI_0790.MOV"
```

### Scenarios

- `teleop`: keyboard-driven mock piloting with a flight HUD
- `tracker`: virtual target detection and proportional control
- `mission`: state-machine mission manager with telemetry and closed-loop target centering

## Keyboard controls

In `teleop` and `mission` modes:

- `w` / `s`: pitch forward / back
- `a` / `d`: roll left / right
- `j` / `l`: yaw left / right
- `i` / `k`: altitude up / down
- `space`: zero all velocity commands
- `q`: quit

## How this maps to ROS 2 later

Current module to future ROS 2 role:

- `CameraNode` -> camera publisher node
- `TelemetryNode` -> telemetry subscriber/publisher node
- `TargetDetectorNode` -> perception node
- `PControllerNode` -> controller node
- `MissionNode` -> behavior/state machine node
- `HudNode` -> visualization/debug node

Current topic-style channels to future ROS 2 topics:

- `camera/frame`
- `telemetry/srt`
- `perception/target`
- `control/cmd_vel`
- `debug/hud`

## Video notes

The dataset includes short and long flights, with a mix of 720p, vertical video, and 4K DJI clips. A few helpful examples:

- `Bluemlisalphutte Flyover.mp4`: short 720p clip, good for first exercises
- `DJI_0574.MP4`: 4K DJI clip with SRT telemetry
- `DJI_0790.MOV`: longer 4K clip for mission exercises
- `VerticalFlyOver.mp4`: vertical framing, useful for discussing camera assumptions

## Teaching flow

The detailed classroom sequence is in [activities/sequence.md](/F:/dev/drone/activities/sequence.md).
The classroom challenge pack is in [activities/challenges/challenge_sequence.md](/F:/dev/drone/activities/challenges/challenge_sequence.md).
