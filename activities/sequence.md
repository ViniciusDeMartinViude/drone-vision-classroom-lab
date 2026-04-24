# Student Activity Sequence

These activities use prerecorded drone videos as if they were the live camera from a real UAV. The architecture follows a ROS 2 mindset:

- each capability is isolated in a node-like module
- data is exchanged as messages
- the full system is built as a pipeline

The goal is that students can later replace the mock bus with ROS 2 publishers/subscribers and keep almost the same decomposition.

## Dataset overview

Recommended clips by stage:

- Activity 1-2: `Bluemlisalphutte Flyover.mp4`, `Stockflue Flyaround.mp4`
- Activity 3-4: `DJI_0574.MP4`, `DJI_0596.MP4`
- Activity 5-6: `DJI_0790.MOV`, `DJI_0862.MOV`
- Extension: `VerticalFlyOver.mp4`, `Surenen Pass Trail Running.mp4`

## Activity 1: Camera Node and Frame Messages

Objective:
Build a node that reads a video frame-by-frame and publishes a `FrameMessage`.

Student tasks:

1. Open a video with `cv2.VideoCapture`.
2. Resize large 4K frames for interactive work.
3. Attach timestamps, frame index, and image shape to a message object.
4. Display the stream with `cv2.imshow`.

ROS 2 concept introduced:

- sensor publisher node
- topic: `camera/frame`

Expected outputs:

- frame counter
- FPS estimate
- consistent playback loop

## Activity 2: Teleop and Velocity Commands

Objective:
Simulate manual piloting by publishing velocity commands with the keyboard.

Student tasks:

1. Create a `TwistCommand` message with roll, pitch, yaw, and altitude rates.
2. Map keys to velocity commands.
3. Show the current command as a HUD overlay.
4. Add an emergency stop that zeros all commands.

ROS 2 concept introduced:

- command publisher
- topic: `control/cmd_vel`

Expected outputs:

- visible command HUD
- clear separation between operator input and vehicle state

## Activity 3: Mock State Estimation

Objective:
Estimate drone state from telemetry and video-derived cues.

Student tasks:

1. Parse DJI `.SRT` files into telemetry messages.
2. Extract GPS and barometer values when available.
3. Maintain a `DroneState` object with mode, altitude, and velocity command history.
4. Compare "sensed" telemetry with "commanded" motion.

ROS 2 concept introduced:

- state estimator node
- topic: `telemetry/srt`

Expected outputs:

- telemetry overlay
- timeline plots or printed logs
- discussion of sensor fusion vs direct measurement

## Activity 4: Target Perception

Objective:
Detect and localize a target in the image.

This project uses a virtual target overlay so students can practice control even when the original video has no convenient object to follow.

Student tasks:

1. Draw a colored circular target onto each frame.
2. Convert to HSV.
3. Threshold the target color.
4. Compute centroid and area with NumPy/OpenCV.
5. Publish a `TargetDetection`.

ROS 2 concept introduced:

- perception node
- topic: `perception/target`

Expected outputs:

- mask visualization
- centroid marker
- target confidence estimate

## Activity 5: Closed-Loop Control

Objective:
Use the target position to generate velocity commands that keep the target centered.

Student tasks:

1. Compute pixel error from image center.
2. Convert error into roll, pitch, and yaw commands.
3. Add command saturation.
4. Tune proportional gains.
5. Compare stable and unstable tuning.

ROS 2 concept introduced:

- controller node
- topic input: `perception/target`
- topic output: `control/cmd_vel`

Expected outputs:

- centered target
- logged control commands
- tuning discussion

## Activity 6: Mission State Machine

Objective:
Create a higher-level autonomy layer that changes behavior by mode.

Suggested states:

1. `SEARCH`
2. `ALIGN`
3. `HOLD`
4. `LAND`

Student tasks:

1. Implement mode transitions based on target visibility and alignment quality.
2. Publish mode changes to the HUD.
3. Hold the target centered for a time threshold before switching states.
4. Simulate landing by reducing the altitude command near the end.

ROS 2 concept introduced:

- behavior tree or mission manager precursor
- future ROS 2 action/state-machine integration

Expected outputs:

- clear state transitions
- deterministic mission logic
- explainable autonomy behavior

## Activity 7: ROS 2 Migration Discussion

Objective:
Map the Python lab into a future ROS 2 package structure.

Student tasks:

1. Decide which modules become ROS 2 nodes.
2. List messages that should become ROS 2 interfaces.
3. Identify timer callbacks and topic frequencies.
4. Define launch-file behavior.

Suggested mapping:

- `camera.py` -> `drone_camera_node.py`
- `telemetry.py` -> `drone_telemetry_node.py`
- `target_detector.py` -> `target_detector_node.py`
- `controller.py` -> `target_controller_node.py`
- `mission.py` -> `mission_manager_node.py`

## Assessment ideas

- Can the student explain the data flow from camera to controller?
- Can the student separate perception errors from control errors?
- Can the student justify a gain choice?
- Can the student explain how the same system would be split into ROS 2 executables?

## Extension ideas

- Replace the virtual target with a real feature detector.
- Use optical flow to estimate camera motion.
- Add lane/path following on trails or roads visible in the videos.
- Compare horizontal and vertical camera geometries.
- Export message logs to CSV for offline analysis.
