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
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_PATH = Path(r"F:\dev\drone\activities\challenges\Drone_Vision_Challenges_Handout.pdf")


CHALLENGES = [
    {
        "title": "Challenge 1: Camera Viewer Class",
        "video": "Bluemlisalphutte Flyover.mp4 from the teacher-selected video folder",
        "student_file": "challenge_01_camera_student.py",
        "teacher_file": "challenge_01_camera_teacher.py",
        "goal": "Build a class that opens a drone video, reads frames, and overlays frame number and timestamp.",
        "student_tasks": [
            "Complete the DroneVideoPlayer class.",
            "Open the video with cv2.VideoCapture.",
            "Resize frames for classroom use.",
            "Draw frame and time overlays.",
            "Quit cleanly with the q key.",
        ],
        "success": [
            "The video plays smoothly.",
            "Overlay values update every frame.",
            "The program closes without errors.",
        ],
        "teacher_notes": [
            "This is the first camera-node style exercise.",
            "Watch for missing str(video_path) when opening the file.",
            "Ask students why FPS is needed for timestamps.",
        ],
    },
    {
        "title": "Challenge 2: Frame Packet Class",
        "video": "Stockflue Flyaround.mp4 from the teacher-selected video folder",
        "student_file": "challenge_02_packet_student.py",
        "teacher_file": "challenge_02_packet_teacher.py",
        "goal": "Create a message-like dataclass that carries the frame plus NumPy-derived brightness statistics.",
        "student_tasks": [
            "Validate the camera stream.",
            "Create and return FramePacket objects.",
            "Convert frames to grayscale with OpenCV.",
            "Compute average brightness using NumPy.",
            "Display the brightness on the image.",
        ],
        "success": [
            "Students use a dataclass to structure data.",
            "Brightness values change with the scene.",
            "The packet acts like a future ROS 2 message.",
        ],
        "teacher_notes": [
            "This introduces structured messages before ROS 2.",
            "A common mistake is forgetting to increment frame_index.",
            "Students should explain why np.mean is useful here.",
        ],
    },
    {
        "title": "Challenge 3: Manual Pilot Class",
        "video": "Bluemlisalphutte Flyover.mp4 from the teacher-selected video folder",
        "student_file": "challenge_03_teleop_student.py",
        "teacher_file": "challenge_03_teleop_teacher.py",
        "goal": "Simulate manual flight control with keyboard commands for roll, pitch, yaw, and throttle.",
        "student_tasks": [
            "Map keys to each command axis.",
            "Clamp the values to a safe interval.",
            "Add a reset on the space key.",
            "Draw the command HUD on the video.",
        ],
        "success": [
            "Each key updates the correct axis.",
            "Values stay in the safe range.",
            "Students can explain the difference between roll, pitch, yaw, and throttle.",
        ],
        "teacher_notes": [
            "This works like a future cmd_vel publisher.",
            "Students often swap yaw and roll at first.",
            "Ask how they would stop the drone in an emergency.",
        ],
    },
    {
        "title": "Challenge 4: Telemetry Parser Class",
        "video": "DJI_0574.MP4 from the teacher-selected video folder",
        "student_file": "challenge_04_telemetry_student.py",
        "teacher_file": "challenge_04_telemetry_teacher.py",
        "goal": "Parse DJI subtitle telemetry and align the sensor data with the video timeline.",
        "student_tasks": [
            "Open the matching SRT file.",
            "Parse time, GPS, altitude, and barometer values.",
            "Find the latest telemetry sample for the current video time.",
            "Overlay telemetry data on the video.",
        ],
        "success": [
            "Telemetry appears only when a matching sample exists.",
            "Values update with time as the video plays.",
            "Students see that drones use multiple sensing sources.",
        ],
        "teacher_notes": [
            "This is a good place to discuss sensor fusion.",
            "Latitude and longitude order is a frequent source of confusion.",
            "Remind students not every clip has telemetry.",
        ],
    },
    {
        "title": "Challenge 5: Virtual Target Tracker Class",
        "video": "DJI_0596.MP4 from the teacher-selected video folder",
        "student_file": "challenge_05_target_student.py",
        "teacher_file": "challenge_05_target_teacher.py",
        "goal": "Add a virtual target to the frame, detect it with HSV thresholding, and compute its centroid with NumPy.",
        "student_tasks": [
            "Draw a moving red target onto each frame.",
            "Convert the image to HSV.",
            "Threshold the red color range.",
            "Use NumPy to compute centroid and area.",
            "Visualize the target and mask.",
        ],
        "success": [
            "The mask isolates the target clearly.",
            "The centroid follows the target motion.",
            "Students connect vision to measurable target state.",
        ],
        "teacher_notes": [
            "This is the perception stage of the pipeline.",
            "Students often try BGR thresholds first; steer them toward HSV.",
            "Make sure they handle the no-detection case.",
        ],
    },
    {
        "title": "Challenge 6: Proportional Controller Class",
        "video": "No live video required; uses example detections",
        "student_file": "challenge_06_controller_student.py",
        "teacher_file": "challenge_06_controller_teacher.py",
        "goal": "Convert perception error into roll, pitch, yaw, and throttle commands using a proportional controller.",
        "student_tasks": [
            "Implement a clamp helper.",
            "Define behavior when the target is missing.",
            "Use negative feedback from image error.",
            "Add forward pitch only when the target appears far away.",
        ],
        "success": [
            "Commands point in the corrective direction.",
            "Outputs stay within limits.",
            "Students can explain why sign matters in feedback control.",
        ],
        "teacher_notes": [
            "This challenge is ideal for debugging on paper first.",
            "A common error is positive feedback instead of negative feedback.",
            "Ask what happens if gains are too high.",
        ],
    },
    {
        "title": "Challenge 7: Mission Manager Class",
        "video": "No live video required; uses target state sequence",
        "student_file": "challenge_07_mission_student.py",
        "teacher_file": "challenge_07_mission_teacher.py",
        "goal": "Create a high-level mission state machine with SEARCH, ALIGN, HOLD, and LAND states.",
        "student_tasks": [
            "Search by yawing when the target is missing.",
            "Align when the target is visible but off-center.",
            "Hold position when centered.",
            "Land after a stable hold period.",
        ],
        "success": [
            "The state progression is explainable and stable.",
            "Students separate mission logic from low-level control.",
            "The hold counter prevents immediate landing.",
        ],
        "teacher_notes": [
            "This prepares students for behavior trees or state machines in ROS 2.",
            "Students often forget to reset the hold counter.",
            "Ask them which transitions are safety critical.",
        ],
    },
    {
        "title": "Challenge 8: Full Pipeline Integration",
        "video": "DJI_0790.MOV from the teacher-selected video folder",
        "student_file": "challenge_08_integration_student.py",
        "teacher_file": "challenge_08_integration_teacher.py",
        "goal": "Integrate camera, target injection, detection, control, and HUD into one class-based mock autonomy pipeline.",
        "student_tasks": [
            "Add the virtual target.",
            "Detect it and compute normalized image error.",
            "Generate commands from the detection.",
            "Draw a complete HUD with target and command data.",
        ],
        "success": [
            "The final script behaves like a miniature autonomous drone stack.",
            "Students can trace data from sensing to action.",
            "The design is easy to map to future ROS 2 nodes.",
        ],
        "teacher_notes": [
            "This is the capstone exercise of the sequence.",
            "Encourage students to identify what would become separate ROS 2 nodes later.",
            "Normalized error is the key concept to verify here.",
        ],
    },
]


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#17324d"),
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#17324d"),
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ChallengeTitle",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1f5a7a"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodySmall",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=13,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Label",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor("#17324d"),
            spaceAfter=2,
        )
    )
    return styles


def bullet_list(items: list[str], styles) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodySmall"])) for item in items],
        bulletType="bullet",
        leftIndent=14,
    )


def build_pdf() -> None:
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Drone Vision Challenges Handout",
        author="OpenAI Codex",
    )

    story = []
    story.append(Paragraph("Drone Vision Challenges", styles["TitleCenter"]))
    story.append(Paragraph("Student Handout and Teacher Appendix", styles["TitleCenter"]))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "This handout uses prerecorded drone videos as a simulated UAV camera feed. "
            "Students practice OpenCV, NumPy, class design, telemetry parsing, target tracking, "
            "control, and mission logic in a sequence that mirrors a future ROS 2 architecture.",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 10))

    overview_data = [
        ["Course tools", "Python, OpenCV, NumPy, class-based design"],
        ["Dataset", "Teacher-selected folder configured in video_config.py or DRONE_VIDEO_DIR"],
        ["Project files", r"F:\dev\drone\activities\challenges"],
        ["End goal", "Build a miniature perception-control-mission pipeline from prerecorded flights"],
    ]
    table = Table(overview_data, colWidths=[4.0 * cm, 12.0 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e8f1f7")),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Sequence Overview", styles["Section"]))
    story.append(
        Paragraph(
            "Teacher setup: choose the dataset folder once in video_config.py or set the DRONE_VIDEO_DIR environment variable before class.",
            styles["BodySmall"],
        )
    )
    story.append(
        bullet_list(
            [
                "Challenge 1-2: camera feed and structured frame data",
                "Challenge 3: manual piloting commands and HUD",
                "Challenge 4: telemetry parsing from DJI subtitle files",
                "Challenge 5: target perception with OpenCV and NumPy",
                "Challenge 6: proportional control",
                "Challenge 7: mission state machine",
                "Challenge 8: full pipeline integration",
            ],
            styles,
        )
    )

    for challenge in CHALLENGES:
        story.append(Spacer(1, 10))
        story.append(Paragraph(challenge["title"], styles["ChallengeTitle"]))
        story.append(Paragraph(f"<b>Goal:</b> {challenge['goal']}", styles["BodySmall"]))
        story.append(Paragraph(f"<b>Video:</b> {challenge['video']}", styles["BodySmall"]))
        story.append(
            Paragraph(
                f"<b>Starter files:</b> {challenge['student_file']} and {challenge['teacher_file']}",
                styles["BodySmall"],
            )
        )
        story.append(Paragraph("Student tasks", styles["Label"]))
        story.append(bullet_list(challenge["student_tasks"], styles))
        story.append(Paragraph("Success criteria", styles["Label"]))
        story.append(bullet_list(challenge["success"], styles))

    story.append(PageBreak())
    story.append(Paragraph("Teacher Appendix", styles["Section"]))
    story.append(
        Paragraph(
            "Use this appendix while circulating in class. It highlights what to check, what students often confuse, "
            "and which ideas are worth discussing before they move to the next challenge.",
            styles["BodyText"],
        )
    )

    for challenge in CHALLENGES:
        story.append(Spacer(1, 8))
        story.append(Paragraph(challenge["title"], styles["ChallengeTitle"]))
        story.append(Paragraph("Teacher prompts and checks", styles["Label"]))
        story.append(bullet_list(challenge["teacher_notes"], styles))

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
