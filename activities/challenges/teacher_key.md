# Teacher Key

This key summarizes the goal, expected outcome, and common errors for all 8 challenges. Teacher reference solutions are provided as matching `*_teacher.py` files in the same folder.

Before class, set the dataset location in [video_config.py](/F:/dev/drone/activities/challenges/video_config.py) or with the `DRONE_VIDEO_DIR` environment variable.

## Challenge 1: Camera Viewer Class

Objective:

- introduce frame-by-frame processing and class structure

Students complete:

- `DroneVideoPlayer.__init__`
- `open`
- `draw_overlay`
- `run`

Check for:

- correct `cv2.VideoCapture`
- frame/time overlay
- clean exit with `q`

Common mistakes:

- not converting `Path` to `str`
- forgetting to release the capture

## Challenge 2: Frame Packet Class

Objective:

- introduce message-like objects and NumPy image statistics

Students complete:

- capture validation
- `read_packet`
- brightness calculation

Check for:

- use of a dataclass
- use of `np.mean`
- correct `None` at end of video

Common mistakes:

- not incrementing `frame_index`
- computing mean on `None`

## Challenge 3: Manual Pilot Class

Objective:

- connect keyboard input to drone command concepts

Students complete:

- command mapping
- reset behavior
- clamping
- HUD drawing

Check for:

- distinct roll/pitch/yaw/throttle values
- correct keys
- values remain bounded

Common mistakes:

- swapped yaw and roll
- forgetting emergency stop

## Challenge 4: Telemetry Parser Class

Objective:

- parse a second sensor stream from DJI subtitle data

Students complete:

- SRT loading
- regex parsing
- time lookup
- HUD display

Check for:

- GPS and barometer extraction
- latest sample lookup by timestamp

Common mistakes:

- assuming every clip has telemetry
- misreading longitude and latitude order

## Challenge 5: Virtual Target Tracker Class

Objective:

- build a perception stage with OpenCV and NumPy

Students complete:

- target drawing
- HSV thresholding
- centroid and area
- visualization

Check for:

- a visible red target
- mask window
- centroid based on NumPy arrays

Common mistakes:

- using BGR thresholds directly
- not handling empty detections

## Challenge 6: Proportional Controller Class

Objective:

- translate perception errors into flight commands

Students complete:

- `clamp`
- missing-target behavior
- control law

Check for:

- negative feedback signs
- output saturation
- forward pitch only when target is far

Common mistakes:

- positive feedback instead of negative feedback
- unlimited commands

## Challenge 7: Mission Manager Class

Objective:

- introduce autonomy above the controller layer

Students complete:

- search logic
- align logic
- hold counter
- landing trigger

Check for:

- stable state transitions
- state stored inside the class

Common mistakes:

- landing immediately
- not resetting the hold counter

## Challenge 8: Full Pipeline Integration

Objective:

- connect sensing, perception, and control into one class-based script

Students complete:

- target creation
- detection
- control
- HUD

Check for:

- all previous ideas appear together
- commands react to detection
- interface remains readable

Common mistakes:

- forgetting normalized error
- mixing pixel coordinates with control values

## Suggested pacing

- Challenge 1: 30 minutes
- Challenge 2: 35 minutes
- Challenge 3: 40 minutes
- Challenge 4: 45 minutes
- Challenge 5: 50 minutes
- Challenge 6: 35 minutes
- Challenge 7: 35 minutes
- Challenge 8: 60 minutes
