# Drone Challenge Sequence

This is the student-facing sequence of 8 challenges. Every challenge uses drone videos, OpenCV, NumPy or message-style data, and at least one class.

Before running the scripts, the teacher should configure the dataset folder in [video_config.py](/F:/dev/drone/activities/challenges/video_config.py) or set `DRONE_VIDEO_DIR`.

## Challenge 1: Camera Viewer Class

Files:

- [challenge_01_camera_student.py](/F:/dev/drone/activities/challenges/challenge_01_camera_student.py)

Goal:

- build a `DroneVideoPlayer` class
- open a drone video
- add frame and time overlays

Recommended video:

- `Bluemlisalphutte Flyover.mp4`

## Challenge 2: Frame Packet Class

Files:

- [challenge_02_packet_student.py](/F:/dev/drone/activities/challenges/challenge_02_packet_student.py)

Goal:

- create a `FramePacket` dataclass
- compute image brightness with NumPy
- return structured camera data

Recommended video:

- `Stockflue Flyaround.mp4`

## Challenge 3: Manual Pilot Class

Files:

- [challenge_03_teleop_student.py](/F:/dev/drone/activities/challenges/challenge_03_teleop_student.py)

Goal:

- build a `ManualPilot` class
- map keyboard inputs to roll, pitch, yaw, and throttle
- display a control HUD

Recommended video:

- `Bluemlisalphutte Flyover.mp4`

## Challenge 4: Telemetry Parser Class

Files:

- [challenge_04_telemetry_student.py](/F:/dev/drone/activities/challenges/challenge_04_telemetry_student.py)

Goal:

- build a `TelemetryParser` class
- parse DJI SRT telemetry
- align telemetry with video time

Recommended video:

- `DJI_0574.MP4`

## Challenge 5: Virtual Target Tracker Class

Files:

- [challenge_05_target_student.py](/F:/dev/drone/activities/challenges/challenge_05_target_student.py)

Goal:

- create a moving target
- detect it with HSV thresholding
- compute centroid with NumPy

Recommended video:

- `DJI_0596.MP4`

## Challenge 6: Proportional Controller Class

Files:

- [challenge_06_controller_student.py](/F:/dev/drone/activities/challenges/challenge_06_controller_student.py)

Goal:

- write a `PController` class
- convert image error into drone commands
- clamp outputs safely

## Challenge 7: Mission Manager Class

Files:

- [challenge_07_mission_student.py](/F:/dev/drone/activities/challenges/challenge_07_mission_student.py)

Goal:

- create a mission state machine
- move between `SEARCH`, `ALIGN`, `HOLD`, and `LAND`
- separate behavior logic from low-level control

## Challenge 8: Full Pipeline Integration

Files:

- [challenge_08_integration_student.py](/F:/dev/drone/activities/challenges/challenge_08_integration_student.py)

Goal:

- integrate camera, target detection, and control
- display a complete mock drone autonomy pipeline

Recommended video:

- `DJI_0790.MOV`

## Common success criteria

- each program runs on a drone video
- each program uses classes rather than only loose functions
- students finish the TODOs themselves
- the final challenge feels like a miniature ROS 2-style system
