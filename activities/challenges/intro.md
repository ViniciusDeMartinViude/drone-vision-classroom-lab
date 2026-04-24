# Introduction to the Drone Vision Challenges

In this unit, students will work with prerecorded drone videos as if they were connected to a real drone camera. The goal is to practice computer vision, basic control, and robotics software structure using only Python, OpenCV, and NumPy.

Even though ROS 2 is not being used yet, the class will follow a ROS 2 way of thinking:

- one module per responsibility
- message-like data structures
- a pipeline of sensing, perception, control, and decision making

This helps students build habits that will transfer naturally to ROS 2 later.

## Scenario

Imagine the class has been asked to design the software for a small autonomous drone. The real drone is not available yet, so the team uses video recordings from earlier flights as a simulated camera feed.

Each challenge asks students to complete part of the drone software:

1. read the camera feed
2. display flight information
3. detect a target
4. generate control commands
5. create mission logic

## Tools

Students will use:

- Python
- OpenCV
- NumPy
- prerecorded drone videos from the folder chosen by the teacher

## Teacher setup

Before class, the teacher should define the video folder in one of these two ways:

1. Edit [video_config.py](/F:/dev/drone/activities/challenges/video_config.py) and set `TEACHER_VIDEO_DIR`
2. Set the environment variable `DRONE_VIDEO_DIR` before running the scripts

Example:

```powershell
$env:DRONE_VIDEO_DIR = "D:\course_materials\drone_videos"
```

## Recommended video order

- First lessons: `Bluemlisalphutte Flyover.mp4`
- Then: `Stockflue Flyaround.mp4`
- Later with telemetry: `DJI_0574.MP4`
- Longer integration work: `DJI_0790.MOV`

## Teacher framing

You can introduce the unit with a question such as:

"If we do not have a drone in the classroom, what parts of a drone system can we still design, test, and improve?"

Expected student answers:

- the camera pipeline
- telemetry parsing
- object detection
- control logic
- autonomy/state machines

## End goal

By the end of the sequence, students should be able to explain:

- how a drone camera feed is processed frame by frame
- how perception becomes control commands
- how a mission manager chooses actions
- how the same software could later become a set of ROS 2 nodes
