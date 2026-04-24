from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_PATH = Path(r"F:\dev\drone\activities\challenges\Teacher_Step_by_Step_Tutorial.pdf")


SETUP_COMMANDS = [
    r"cd F:\dev\drone",
    r"git switch teachers",
    r"conda activate cardd-paper-demo",
    '$env:PYTHONPATH = "F:\\dev\\drone\\src"',
    '$env:DRONE_VIDEO_DIR = "D:\\course_materials\\drone_videos"',
]


CHALLENGES = [
    {
        "title": "Challenge 1: Camera Viewer Class",
        "time": "30 minutes",
        "files": [
            "activities/challenges/challenge_01_camera_student.py",
            "activities/challenges/challenge_01_camera_teacher.py",
        ],
        "video": "Bluemlisalphutte Flyover.mp4",
        "teacher_goal": "Help students understand that a drone camera pipeline is a loop over frames plus metadata such as time and frame index.",
        "before": [
            "Confirm the teacher branch is checked out.",
            "Confirm DRONE_VIDEO_DIR points to the folder that contains Bluemlisalphutte Flyover.mp4.",
            "Open the student starter file before class so the TODOs are visible.",
        ],
        "run_demo": [
            r"python F:\dev\drone\activities\challenges\challenge_01_camera_teacher.py",
        ],
        "say": [
            "Today we are treating a prerecorded drone video as if it were the live camera of a real robot.",
            "Every later perception and control module depends on a reliable frame loop.",
            "In ROS 2 this would become a camera node publishing images on a topic.",
        ],
        "student_steps": [
            "Ask students to find where the video should be opened.",
            "Ask them to check whether the video opened successfully.",
            "Ask them to read one frame at a time and stop when the video ends.",
            "Ask them to resize the frame and overlay frame number and timestamp.",
            "Ask them to display the frame and close the window with q.",
        ],
        "checkpoints": [
            "The video window opens.",
            "The frame count changes.",
            "The timestamp increases steadily.",
            "The script exits cleanly when q is pressed.",
        ],
        "common_issues": [
            "Students forget str(video_path) when opening cv2.VideoCapture.",
            "Students do not stop when cap.read() fails at the end of the file.",
            "Students forget cap.release() or cv2.destroyAllWindows().",
        ],
        "debrief": [
            "Ask: what does each loop iteration represent?",
            "Ask: why is FPS needed to estimate timestamp?",
            "Connect this to the future ROS 2 camera publisher.",
        ],
    },
    {
        "title": "Challenge 2: Frame Packet Class",
        "time": "35 minutes",
        "files": [
            "activities/challenges/challenge_02_packet_student.py",
            "activities/challenges/challenge_02_packet_teacher.py",
        ],
        "video": "Stockflue Flyaround.mp4",
        "teacher_goal": "Introduce structured frame data and show that NumPy can turn raw images into measurements.",
        "before": [
            "Confirm Stockflue Flyaround.mp4 exists in the selected video directory.",
            "Remind students that image arrays are numeric data, not just pictures.",
        ],
        "run_demo": [
            r"python F:\dev\drone\activities\challenges\challenge_02_packet_teacher.py",
        ],
        "say": [
            "A robotics system rarely passes around raw images alone.",
            "We often package the image together with timing, index, and derived measurements.",
            "This FramePacket dataclass is the classroom version of a future message object.",
        ],
        "student_steps": [
            "Ask students to validate the camera stream in open().",
            "Ask them to return None when the video ends.",
            "Ask them to convert the frame to grayscale.",
            "Ask them to compute average brightness using np.mean.",
            "Ask them to build and return a FramePacket object.",
        ],
        "checkpoints": [
            "Brightness values appear on screen.",
            "Students use a dataclass rather than a loose tuple.",
            "The program stops cleanly when the video ends.",
        ],
        "common_issues": [
            "Students compute np.mean on the original color frame and get confusing results.",
            "Students forget to increment frame_index.",
            "Students forget to return the FramePacket object.",
        ],
        "debrief": [
            "Ask: why is brightness useful as a simple derived feature?",
            "Ask: why is a dataclass helpful for larger robotics systems?",
        ],
    },
    {
        "title": "Challenge 3: Manual Pilot Class",
        "time": "40 minutes",
        "files": [
            "activities/challenges/challenge_03_teleop_student.py",
            "activities/challenges/challenge_03_teleop_teacher.py",
        ],
        "video": "Bluemlisalphutte Flyover.mp4",
        "teacher_goal": "Connect the video to manual flight concepts: roll, pitch, yaw, and throttle.",
        "before": [
            "Review the meaning of roll, pitch, yaw, and throttle before coding.",
            "Tell students that these are simulated commands, not real aircraft commands.",
        ],
        "run_demo": [
            r"python F:\dev\drone\activities\challenges\challenge_03_teleop_teacher.py",
        ],
        "say": [
            "Now we add the idea of piloting.",
            "The camera feed is still prerecorded, but the control layer is live and interactive.",
            "Later, this same idea will become a ROS 2 command publisher.",
        ],
        "student_steps": [
            "Ask students to map a/d to roll.",
            "Ask students to map w/s to pitch.",
            "Ask students to map j/l to yaw and i/k to throttle.",
            "Ask them to add a space-bar reset.",
            "Ask them to clamp every axis to the range [-1, 1].",
            "Ask them to draw all four values on the frame.",
        ],
        "checkpoints": [
            "Each key changes exactly one control axis.",
            "The numbers on the HUD respond immediately.",
            "The emergency stop resets all values.",
        ],
        "common_issues": [
            "Students mix up yaw and roll.",
            "Students let the values grow without bounds.",
            "Students update commands before reading the key correctly.",
        ],
        "debrief": [
            "Ask students which axis would rotate the drone left-right versus turn its heading.",
            "Connect the HUD to the idea of telemetry and operator feedback.",
        ],
    },
    {
        "title": "Challenge 4: Telemetry Parser Class",
        "time": "45 minutes",
        "files": [
            "activities/challenges/challenge_04_telemetry_student.py",
            "activities/challenges/challenge_04_telemetry_teacher.py",
        ],
        "video": "DJI_0574.MP4 and DJI_0574.SRT",
        "teacher_goal": "Show that the drone has more sensors than just the camera and that multiple data streams must be aligned by time.",
        "before": [
            "Verify that both DJI_0574.MP4 and DJI_0574.SRT are present in the chosen folder.",
            "Explain that the SRT file contains time-stamped telemetry text.",
        ],
        "run_demo": [
            r"python F:\dev\drone\activities\challenges\challenge_04_telemetry_teacher.py",
        ],
        "say": [
            "Real robots rarely operate from vision alone.",
            "Here we align a camera stream with a telemetry stream.",
            "This is a small step toward sensor fusion thinking.",
        ],
        "student_steps": [
            "Ask students to locate the matching SRT file using video_path.with_suffix('.SRT').",
            "Ask them to split the file into subtitle blocks.",
            "Ask them to parse the start time of each block.",
            "Ask them to extract GPS and barometer values with regular expressions.",
            "Ask them to return the latest sample at or before the current video time.",
            "Ask them to draw telemetry values on the frame.",
        ],
        "checkpoints": [
            "Telemetry appears only for the DJI video with SRT data.",
            "Values update as the video time increases.",
            "Students can explain why a latest-sample lookup is needed.",
        ],
        "common_issues": [
            "Students reverse latitude and longitude.",
            "Students assume every video has a matching SRT.",
            "Students use the wrong subtitle line for the timestamp.",
        ],
        "debrief": [
            "Ask: why do we align by time rather than frame index alone?",
            "Ask: what other sensors might a real drone publish?",
        ],
    },
    {
        "title": "Challenge 5: Virtual Target Tracker Class",
        "time": "50 minutes",
        "files": [
            "activities/challenges/challenge_05_target_student.py",
            "activities/challenges/challenge_05_target_teacher.py",
        ],
        "video": "DJI_0596.MP4",
        "teacher_goal": "Build a complete perception step: target creation, segmentation, centroid extraction, and visualization.",
        "before": [
            "Explain why a virtual target makes the exercise reliable for every student.",
            "Review the difference between BGR and HSV color spaces.",
        ],
        "run_demo": [
            r"python F:\dev\drone\activities\challenges\challenge_05_target_teacher.py",
        ],
        "say": [
            "We now create the target that the drone should eventually track.",
            "First we create a clean perception problem, then we solve it.",
            "The output of this stage is no longer an image alone; it is a measurement of target position.",
        ],
        "student_steps": [
            "Ask students to draw a moving red circle onto each frame.",
            "Ask them to convert the image from BGR to HSV.",
            "Ask them to threshold the red target color.",
            "Ask them to use np.where to find mask coordinates.",
            "Ask them to compute centroid and area.",
            "Ask them to draw the centroid and display the mask.",
        ],
        "checkpoints": [
            "A red target is visible on the video.",
            "The mask window isolates the target.",
            "The centroid marker follows the target.",
        ],
        "common_issues": [
            "Students use only one red hue range and miss some pixels.",
            "Students forget to handle the no-detection case.",
            "Students draw on the mask instead of the video frame.",
        ],
        "debrief": [
            "Ask: why is HSV often easier for color segmentation?",
            "Ask: what information would a controller need from this detector?",
        ],
    },
    {
        "title": "Challenge 6: Proportional Controller Class",
        "time": "35 minutes",
        "files": [
            "activities/challenges/challenge_06_controller_student.py",
            "activities/challenges/challenge_06_controller_teacher.py",
        ],
        "video": "Uses example detections rather than a video loop",
        "teacher_goal": "Translate perception error into corrective action with a proportional controller.",
        "before": [
            "Review the idea of error: measured position minus desired position.",
            "Tell students that the center of the image is the desired target position.",
        ],
        "run_demo": [
            r"python F:\dev\drone\activities\challenges\challenge_06_controller_teacher.py",
        ],
        "say": [
            "The detector gives us a target position; the controller turns that into action.",
            "Today we start with a proportional controller because it is easy to understand and debug.",
            "The sign of the feedback matters more than the exact gain at first.",
        ],
        "student_steps": [
            "Ask students to implement clamp().",
            "Ask them to define behavior when the target is not found.",
            "Ask them to convert error_x into roll and yaw corrections.",
            "Ask them to convert error_y into throttle correction.",
            "Ask them to add forward pitch only when the target area is small.",
        ],
        "checkpoints": [
            "Outputs remain inside the defined limits.",
            "The command signs point in the corrective direction.",
            "Students can explain search behavior when the target is missing.",
        ],
        "common_issues": [
            "Students implement positive feedback instead of negative feedback.",
            "Students forget to clamp one of the outputs.",
            "Students ignore the missing-target case.",
        ],
        "debrief": [
            "Ask: what happens if the gains are too large?",
            "Ask: why does the controller need normalized error rather than raw pixel values?",
        ],
    },
    {
        "title": "Challenge 7: Mission Manager Class",
        "time": "35 minutes",
        "files": [
            "activities/challenges/challenge_07_mission_student.py",
            "activities/challenges/challenge_07_mission_teacher.py",
        ],
        "video": "Uses a target-state sequence rather than a video loop",
        "teacher_goal": "Separate high-level mission decisions from low-level control.",
        "before": [
            "Introduce SEARCH, ALIGN, HOLD, and LAND as mission-level states.",
            "Explain that state machines help us reason about autonomy step by step.",
        ],
        "run_demo": [
            r"python F:\dev\drone\activities\challenges\challenge_07_mission_teacher.py",
        ],
        "say": [
            "A controller answers how to move; a mission manager answers what mode the robot should be in.",
            "This is the first layer of autonomy above direct control.",
            "We want state transitions that are explainable and stable.",
        ],
        "student_steps": [
            "Ask students to return a search command when the target is missing.",
            "Ask them to switch to ALIGN when the target is visible but off-center.",
            "Ask them to count centered steps in HOLD.",
            "Ask them to transition to LAND only after a stable hold period.",
        ],
        "checkpoints": [
            "The printed state progression makes sense.",
            "The hold counter prevents immediate landing.",
            "Students separate state logic from controller math.",
        ],
        "common_issues": [
            "Students forget to reset hold_counter when the target is lost.",
            "Students jump to LAND too early.",
            "Students mix target-centering logic with state transitions in one unreadable block.",
        ],
        "debrief": [
            "Ask: why is state memory important?",
            "Ask: what other drone mission states could exist in a real system?",
        ],
    },
    {
        "title": "Challenge 8: Full Pipeline Integration",
        "time": "60 minutes",
        "files": [
            "activities/challenges/challenge_08_integration_student.py",
            "activities/challenges/challenge_08_integration_teacher.py",
        ],
        "video": "DJI_0790.MOV",
        "teacher_goal": "Bring together sensing, perception, control, and visualization into one coherent mock drone pipeline.",
        "before": [
            "Tell students this is the capstone challenge of the sequence.",
            "Ask them to reuse ideas from the earlier challenges rather than invent everything again.",
        ],
        "run_demo": [
            r"python F:\dev\drone\activities\challenges\challenge_08_integration_teacher.py",
        ],
        "say": [
            "Now we combine the building blocks into one mini autonomy stack.",
            "Even without ROS 2, we already have the key architecture: sensing, perception, control, and display.",
            "The purpose of this challenge is integration, not novelty.",
        ],
        "student_steps": [
            "Ask students to add the virtual target to each frame.",
            "Ask them to detect the target and compute normalized error.",
            "Ask them to compute roll, pitch, yaw, and throttle from the detection.",
            "Ask them to draw a complete HUD with crosshairs, target, and command values.",
        ],
        "checkpoints": [
            "The target is detected consistently.",
            "The command values react to target motion.",
            "The HUD clearly shows the state of the pipeline.",
            "Students can describe data flow from image to action.",
        ],
        "common_issues": [
            "Students mix raw pixel offsets with normalized error.",
            "Students forget to compute commands when detection is missing.",
            "Students draw too much on the frame and make the display hard to read.",
        ],
        "debrief": [
            "Ask students which parts would become separate ROS 2 nodes.",
            "Ask them which topics they would define between those nodes.",
            "Close by reviewing the full path: camera -> perception -> controller -> mission.",
        ],
    },
]


def styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=s["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#1a3653"),
            spaceAfter=10,
        )
    )
    s.add(
        ParagraphStyle(
            name="SubTitleCenter",
            parent=s["Heading2"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#3a6a8c"),
            spaceAfter=16,
        )
    )
    s.add(
        ParagraphStyle(
            name="Section",
            parent=s["Heading1"],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#1a3653"),
            spaceBefore=8,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            name="Section2",
            parent=s["Heading2"],
            fontSize=12.5,
            leading=15,
            textColor=colors.HexColor("#2e5f7b"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="BodySmall",
            parent=s["BodyText"],
            fontSize=9.2,
            leading=12.2,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="MiniLabel",
            parent=s["BodyText"],
            fontSize=9.5,
            leading=11,
            textColor=colors.HexColor("#1a3653"),
            spaceBefore=4,
            spaceAfter=2,
        )
    )
    s.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=s["Code"],
            fontName="Courier",
            fontSize=8.7,
            leading=10.5,
            backColor=colors.HexColor("#f4f7fa"),
            borderColor=colors.HexColor("#d3dde8"),
            borderWidth=0.5,
            borderPadding=6,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    return s


def bullets(items: list[str], s) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(item, s["BodySmall"])) for item in items],
        bulletType="bullet",
        leftIndent=14,
    )


def code_block(lines: list[str], s) -> Preformatted:
    return Preformatted("\n".join(lines), s["CodeBlock"])


def add_challenge(story: list, challenge: dict, s) -> None:
    story.append(Paragraph(challenge["title"], s["Section"]))
    story.append(Paragraph(f"<b>Recommended time:</b> {challenge['time']}", s["BodySmall"]))
    story.append(Paragraph(f"<b>Video or input:</b> {challenge['video']}", s["BodySmall"]))
    story.append(
        Paragraph(
            "<b>Files:</b> " + ", ".join(challenge["files"]),
            s["BodySmall"],
        )
    )
    story.append(Paragraph(f"<b>Teacher goal:</b> {challenge['teacher_goal']}", s["BodySmall"]))

    story.append(Paragraph("Before class", s["Section2"]))
    story.append(bullets(challenge["before"], s))

    story.append(Paragraph("Run this demo first", s["Section2"]))
    story.append(code_block(challenge["run_demo"], s))

    story.append(Paragraph("Suggested explanation to students", s["Section2"]))
    story.append(bullets(challenge["say"], s))

    story.append(Paragraph("Step-by-step classroom flow", s["Section2"]))
    numbered = [f"{idx}. {item}" for idx, item in enumerate(challenge["student_steps"], start=1)]
    story.append(bullets(numbered, s))

    story.append(Paragraph("What to check while students work", s["Section2"]))
    story.append(bullets(challenge["checkpoints"], s))

    story.append(Paragraph("Common issues to watch for", s["Section2"]))
    story.append(bullets(challenge["common_issues"], s))

    story.append(Paragraph("Closing discussion", s["Section2"]))
    story.append(bullets(challenge["debrief"], s))

    story.append(PageBreak())


def build() -> None:
    s = styles()
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title="Teacher Step-by-Step Tutorial",
        author="OpenAI Codex",
    )

    story: list = []
    story.append(Paragraph("Teacher Step-by-Step Tutorial", s["TitleCenter"]))
    story.append(Paragraph("Drone Vision Challenges with OpenCV, NumPy, and Class-Based Design", s["SubTitleCenter"]))
    story.append(
        Paragraph(
            "This document is a classroom guide for the teacher branch of the repository. "
            "It is designed to be followed live during class and includes setup, pacing, commands, "
            "lesson prompts, student checkpoints, and troubleshooting for all 8 challenges.",
            s["BodyText"],
        )
    )
    story.append(Spacer(1, 8))

    info = [
        ["Repository", r"F:\dev\drone"],
        ["Branch for class", "teachers"],
        ["Student branch", "students"],
        ["Challenge folder", r"F:\dev\drone\activities\challenges"],
        ["Video folder", "Set by TEACHER_VIDEO_DIR in video_config.py or DRONE_VIDEO_DIR"],
    ]
    table = Table(info, colWidths=[4.3 * cm, 11.8 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e7f0f7")),
                ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.3),
                ("LEADING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Before Students Arrive", s["Section"]))
    story.append(
        Paragraph(
            "Use the following checklist before the lesson starts. This prevents most class-time problems.",
            s["BodySmall"],
        )
    )
    story.append(
        bullets(
            [
                "Open a terminal in F:\\dev\\drone.",
                "Switch to the teachers branch so the reference solutions are available.",
                "Activate the conda environment cardd-paper-demo.",
                "Set PYTHONPATH to F:\\dev\\drone\\src.",
                "Set DRONE_VIDEO_DIR or edit video_config.py so the scripts can find the videos.",
                "Run one teacher solution before class to confirm the machine can open OpenCV windows.",
                "Open the starter file for the first challenge in your editor.",
            ],
            s,
        )
    )
    story.append(code_block(SETUP_COMMANDS, s))

    story.append(Paragraph("2. Suggested Teaching Rhythm", s["Section"]))
    story.append(
        bullets(
            [
                "Begin each challenge by showing the teacher solution briefly so students know the target behavior.",
                "Then switch to the student starter file and focus on the TODOs only.",
                "Let students work in pairs for 10 to 20 minutes depending on the challenge.",
                "Pause the room when a common bug appears and explain it once for everyone.",
                "End each challenge with a 2 to 5 minute debrief that connects the code to future ROS 2 ideas.",
            ],
            s,
        )
    )

    story.append(Paragraph("3. How to Use the Branches", s["Section"]))
    story.append(
        bullets(
            [
                "Use the teachers branch on the classroom machine when you need reference solutions.",
                "Distribute the students branch to learners so they receive only the starter files.",
                "If you project code in class, make sure you are displaying the correct branch before opening a file.",
            ],
            s,
        )
    )
    story.append(
        code_block(
            [
                r"git switch teachers",
                r"git switch students",
            ],
            s,
        )
    )

    story.append(PageBreak())

    for challenge in CHALLENGES:
        add_challenge(story, challenge, s)

    story.append(Paragraph("Final Wrap-Up Discussion", s["Section"]))
    story.append(
        bullets(
            [
                "Ask students to name the main layers they built: camera, message, control, telemetry, perception, mission, integration.",
                "Ask which parts would become ROS 2 nodes in the future.",
                "Ask what messages or topics would connect those nodes.",
                "Ask what would need to change when moving from prerecorded video to a real drone camera.",
            ],
            s,
        )
    )

    story.append(Paragraph("Quick Troubleshooting Reference", s["Section"]))
    story.append(
        bullets(
            [
                "If no window opens, verify the conda environment and OpenCV installation.",
                "If the video does not load, verify DRONE_VIDEO_DIR and the exact filename.",
                "If telemetry does not appear, confirm the matching SRT file is present.",
                "If imports fail, set PYTHONPATH to F:\\dev\\drone\\src before running examples from the repo root.",
                "If a student gets lost, point them to the next TODO only rather than explaining the whole solution.",
            ],
            s,
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build()
