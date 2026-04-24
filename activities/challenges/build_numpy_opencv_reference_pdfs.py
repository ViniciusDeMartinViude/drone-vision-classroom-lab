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


BASE_DIR = Path(r"F:\dev\drone\activities\challenges")
STUDENT_PDF = BASE_DIR / "Student_NumPy_OpenCV_Reference.pdf"
TEACHER_PDF = BASE_DIR / "Teacher_NumPy_OpenCV_Reference.pdf"


OPENCV_ITEMS = [
    {
        "name": "cv2.VideoCapture(path)",
        "kind": "Method / constructor",
        "what": "Opens a video file so frames can be read one by one.",
        "why": "It is the starting point for treating a prerecorded drone video as a simulated onboard camera.",
        "example": "cap = cv2.VideoCapture(str(VIDEO_PATH))",
        "useful": "Used in the camera, teleop, telemetry, target-tracking, and integration challenges to load the drone footage.",
        "teacher_notes": [
            "Students often forget to convert a Path object to str.",
            "This is a good moment to explain that a robot camera is conceptually a continuous stream of images.",
        ],
    },
    {
        "name": "cap.isOpened()",
        "kind": "Method",
        "what": "Checks whether the video source opened successfully.",
        "why": "Prevents confusing errors later in the loop when students try to read from an invalid capture object.",
        "example": "if not cap.isOpened():\n    print('Could not open video')",
        "useful": "Useful whenever the teacher changes the video folder or a filename is wrong.",
        "teacher_notes": [
            "Ask students why error checking should happen early.",
            "This connects well to defensive programming in robotics.",
        ],
    },
    {
        "name": "cap.read()",
        "kind": "Method",
        "what": "Reads the next frame from the video and returns two values: a success flag and the image.",
        "why": "It drives the frame-processing loop.",
        "example": "ok, frame = cap.read()\nif not ok:\n    break",
        "useful": "This is the heartbeat of the whole lab, because every perception and control step begins from the current frame.",
        "teacher_notes": [
            "Students should understand that the loop ends when ok becomes False.",
            "A helpful question is: what does one loop iteration represent in a robot?",
        ],
    },
    {
        "name": "cap.get(cv2.CAP_PROP_FPS)",
        "kind": "Method + property constant",
        "what": "Retrieves the frames-per-second value stored in the video metadata.",
        "why": "Lets us estimate time using frame_index / fps.",
        "example": "fps = cap.get(cv2.CAP_PROP_FPS) or 30.0",
        "useful": "Important in telemetry alignment and when turning frame number into a timestamp.",
        "teacher_notes": [
            "Useful for discussing why time matters more than frame count alone when matching sensors.",
            "Students may need the fallback value when metadata is missing.",
        ],
    },
    {
        "name": "cap.release()",
        "kind": "Method",
        "what": "Closes the video file and releases the capture resource.",
        "why": "Good cleanup prevents locked files and inconsistent behavior.",
        "example": "cap.release()",
        "useful": "Always call it at the end of a challenge script.",
        "teacher_notes": [
            "Pair this with destroyAllWindows to reinforce tidy program shutdown.",
        ],
    },
    {
        "name": "cv2.resize(image, dsize=None, fx=..., fy=...)",
        "kind": "Method",
        "what": "Resizes an image to a different scale.",
        "why": "Drone videos can be 4K, which is too large for comfortable classroom processing.",
        "example": "frame = cv2.resize(frame, dsize=None, fx=0.4, fy=0.4)",
        "useful": "Makes the exercises faster, keeps windows manageable, and reduces computation.",
        "teacher_notes": [
            "This is a practical chance to discuss the trade-off between resolution and speed.",
        ],
    },
    {
        "name": "cv2.putText(...)",
        "kind": "Method",
        "what": "Draws text directly on an image.",
        "why": "Lets students build HUD overlays for time, brightness, commands, telemetry, and target area.",
        "example": "cv2.putText(frame, 'frame: 10', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)",
        "useful": "Vital for turning raw processing into interpretable output during class.",
        "teacher_notes": [
            "A useful prompt is: what information should an operator see first?",
        ],
    },
    {
        "name": "cv2.FONT_HERSHEY_SIMPLEX",
        "kind": "Constant",
        "what": "A built-in OpenCV font used when drawing text.",
        "why": "Required by putText to choose a text style.",
        "example": "cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)",
        "useful": "Keeps on-screen information readable with a minimal setup.",
        "teacher_notes": [
            "This is a constant, not a function.",
        ],
    },
    {
        "name": "cv2.imshow(window_name, image)",
        "kind": "Method",
        "what": "Displays an image in a named window.",
        "why": "Allows students to see the current camera frame, target mask, and HUD.",
        "example": "cv2.imshow('challenge_05', frame)",
        "useful": "Makes the lab interactive and visually testable.",
        "teacher_notes": [
            "If windows do not appear, the environment or GUI backend is usually the problem.",
        ],
    },
    {
        "name": "cv2.waitKey(delay_ms)",
        "kind": "Method",
        "what": "Waits briefly for a keyboard press and keeps the window responsive.",
        "why": "Needed both for playback timing and for keyboard control.",
        "example": "key = cv2.waitKey(20) & 0xFF",
        "useful": "Used for quitting with q and for teleoperation keys.",
        "teacher_notes": [
            "Explain why the bit mask & 0xFF is commonly used in OpenCV keyboard loops.",
        ],
    },
    {
        "name": "cv2.destroyAllWindows()",
        "kind": "Method",
        "what": "Closes all OpenCV windows created by the script.",
        "why": "Completes cleanup at the end of a program.",
        "example": "cv2.destroyAllWindows()",
        "useful": "Prevents stray windows between challenge runs.",
        "teacher_notes": [
            "Useful to reinforce good shutdown habits.",
        ],
    },
    {
        "name": "cv2.cvtColor(image, code)",
        "kind": "Method",
        "what": "Converts an image from one color representation to another.",
        "why": "Used when moving from BGR camera images into grayscale or HSV for analysis.",
        "example": "gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\nhsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)",
        "useful": "Central to brightness measurement, color thresholding, and mask display.",
        "teacher_notes": [
            "Many students assume the image is RGB; explain that OpenCV uses BGR by default.",
        ],
    },
    {
        "name": "cv2.COLOR_BGR2GRAY",
        "kind": "Constant",
        "what": "Conversion code from a color image to grayscale.",
        "why": "Needed before computing brightness with one intensity channel.",
        "example": "gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)",
        "useful": "Simplifies measurements when color is not needed.",
        "teacher_notes": [
            "A nice question is why brightness is easier to compute on grayscale than on a 3-channel image.",
        ],
    },
    {
        "name": "cv2.COLOR_BGR2HSV",
        "kind": "Constant",
        "what": "Conversion code from BGR to HSV color space.",
        "why": "HSV is often easier for color-based segmentation than BGR.",
        "example": "hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)",
        "useful": "Used for red target detection in the perception challenges.",
        "teacher_notes": [
            "This is the key place to compare hue-based segmentation to direct BGR thresholding.",
        ],
    },
    {
        "name": "cv2.COLOR_GRAY2BGR",
        "kind": "Constant",
        "what": "Conversion code from a grayscale image into a 3-channel BGR image.",
        "why": "Lets a mask be displayed inside a color frame overlay.",
        "example": "mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)",
        "useful": "Helpful when showing a mask inset on top of the main camera image.",
        "teacher_notes": [
            "Good for explaining that display formatting sometimes differs from analysis formatting.",
        ],
    },
    {
        "name": "cv2.inRange(image, lower, upper)",
        "kind": "Method",
        "what": "Creates a binary mask where pixels inside the chosen range become white and the rest become black.",
        "why": "This is the main segmentation step for the virtual red target.",
        "example": "mask = cv2.inRange(hsv, lower, upper)",
        "useful": "Turns a color problem into a simple binary detection problem.",
        "teacher_notes": [
            "Students should understand that the output is a mask, not a cropped image.",
        ],
    },
    {
        "name": "cv2.bitwise_or(mask1, mask2)",
        "kind": "Method",
        "what": "Combines two binary masks into one.",
        "why": "Red often wraps around the HSV hue scale, so two ranges are combined.",
        "example": "mask = cv2.bitwise_or(mask1, mask2)",
        "useful": "Improves red target detection robustness.",
        "teacher_notes": [
            "This is a good place to explain why one color may need multiple thresholds.",
        ],
    },
    {
        "name": "cv2.circle(image, center, radius, color, thickness)",
        "kind": "Method",
        "what": "Draws a circle on the image.",
        "why": "Used both to create the virtual target and to draw the detected centroid marker.",
        "example": "cv2.circle(frame, (cx, cy), 18, (0, 0, 255), -1)",
        "useful": "Lets students both inject a target and visualize a detection result.",
        "teacher_notes": [
            "The thickness value -1 means filled circle, which students often discover for the first time here.",
        ],
    },
    {
        "name": "cv2.line(image, pt1, pt2, color, thickness)",
        "kind": "Method",
        "what": "Draws a line between two points.",
        "why": "Used to draw crosshairs in the HUD.",
        "example": "cv2.line(frame, (w // 2, 0), (w // 2, h), (255, 255, 255), 1)",
        "useful": "Helps students visually compare target position to the desired image center.",
        "teacher_notes": [
            "This supports the later concept of image error for control.",
        ],
    },
]


NUMPY_ITEMS = [
    {
        "name": "np.ndarray",
        "kind": "Array type / core object",
        "what": "The main NumPy array type used to store images and masks.",
        "why": "OpenCV frames are represented as NumPy arrays, so every image operation depends on understanding this object.",
        "example": "image: np.ndarray",
        "useful": "Images, masks, and overlays all live as arrays in memory.",
        "teacher_notes": [
            "A frame is data first and a picture second. This idea unlocks perception and control.",
        ],
    },
    {
        "name": "array.shape",
        "kind": "Property",
        "what": "Returns the size of an array along each dimension.",
        "why": "For images, shape helps us find height, width, and sometimes channels.",
        "example": "h, w = frame.shape[:2]",
        "useful": "Used to place targets, draw crosshairs, compute image center, and build inset displays.",
        "teacher_notes": [
            "A very useful question is: why do we use shape[:2] instead of shape?",
        ],
    },
    {
        "name": "np.array([...], dtype=np.uint8)",
        "kind": "Method",
        "what": "Creates a NumPy array from a list of values.",
        "why": "Used to define HSV lower and upper threshold bounds.",
        "example": "lower = np.array([0, 140, 120], dtype=np.uint8)",
        "useful": "Makes threshold values compatible with OpenCV image operations.",
        "teacher_notes": [
            "Students should notice the dtype matters when interfacing with image-processing libraries.",
        ],
    },
    {
        "name": "np.uint8",
        "kind": "Data type",
        "what": "Unsigned 8-bit integer type with values from 0 to 255.",
        "why": "Standard image channel values are usually stored in this type.",
        "example": "np.array([255, 0, 0], dtype=np.uint8)",
        "useful": "Important for masks, color thresholds, and image buffers.",
        "teacher_notes": [
            "This is a good link back to how pixel intensities are represented numerically.",
        ],
    },
    {
        "name": "np.mean(array)",
        "kind": "Method",
        "what": "Computes the average value of the array.",
        "why": "Used to estimate frame brightness from grayscale images.",
        "example": "brightness = float(np.mean(gray))",
        "useful": "Shows how a full image can be reduced to a single measurement.",
        "teacher_notes": [
            "A helpful discussion prompt is: what information is lost when we reduce an image to one average number?",
        ],
    },
    {
        "name": "np.where(condition)",
        "kind": "Method",
        "what": "Returns the positions where a condition is true.",
        "why": "Used to find all white pixels in a mask after thresholding.",
        "example": "ys, xs = np.where(mask > 0)",
        "useful": "This is how the lab moves from a binary mask to a target centroid and area.",
        "teacher_notes": [
            "Students often need a reminder that ys comes before xs because array indexing is row, column.",
        ],
    },
    {
        "name": "np.zeros(shape, dtype=np.uint8)",
        "kind": "Method",
        "what": "Creates an array filled with zeros.",
        "why": "Used as a placeholder mask in starter files.",
        "example": "mask = np.zeros(frame.shape[:2], dtype=np.uint8)",
        "useful": "Good for initializing blank grayscale images and masks.",
        "teacher_notes": [
            "This is a good chance to explain why mask images are often single-channel.",
        ],
    },
    {
        "name": "Array slicing and assignment",
        "kind": "Property / syntax pattern",
        "what": "Selects and updates a rectangular region inside an array.",
        "why": "Used to place the mask inset inside the main frame.",
        "example": "frame[y0:y1, x0:x1] = mask_bgr",
        "useful": "Shows students that overlays can be done by writing directly into an image array.",
        "teacher_notes": [
            "Students should understand that this changes the original array in place.",
        ],
    },
]


def make_styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=s["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#16324a"),
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            name="SubTitleCenter",
            parent=s["Heading2"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#406b87"),
            spaceAfter=14,
        )
    )
    s.add(
        ParagraphStyle(
            name="Section",
            parent=s["Heading1"],
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#16324a"),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            name="Entry",
            parent=s["Heading2"],
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#245775"),
            spaceBefore=6,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="BodySmall",
            parent=s["BodyText"],
            fontSize=9.2,
            leading=12.2,
            spaceAfter=3,
        )
    )
    s.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=s["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=10.5,
            backColor=colors.HexColor("#f4f7fa"),
            borderColor=colors.HexColor("#d5e0ea"),
            borderWidth=0.5,
            borderPadding=6,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            name="SmallLabel",
            parent=s["BodyText"],
            fontSize=9.3,
            leading=11,
            textColor=colors.HexColor("#16324a"),
            spaceBefore=2,
            spaceAfter=2,
        )
    )
    return s


def bullets(items: list[str], styles) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BodySmall"])) for item in items],
        bulletType="bullet",
        leftIndent=14,
    )


def code_block(text: str, styles) -> Preformatted:
    return Preformatted(text, styles["CodeBlock"])


def add_intro(story: list, styles, audience: str) -> None:
    story.append(Paragraph(f"{audience} Reference", styles["TitleCenter"]))
    story.append(Paragraph("OpenCV and NumPy Used in the Drone Vision Lab", styles["SubTitleCenter"]))
    if audience == "Student":
        intro = (
            "This reference explains the OpenCV methods, OpenCV constants, NumPy methods, "
            "NumPy properties, and NumPy data structures used in the drone classroom exercises. "
            "The goal is to help you understand what each tool does, why it appears in the code, "
            "and how it helps with drone-video perception, telemetry, HUD drawing, and control."
        )
    else:
        intro = (
            "This teacher reference explains the OpenCV methods, constants, NumPy methods, properties, "
            "and array concepts used in the drone classroom exercises. It includes classroom interpretations, "
            "common misconceptions, and prompts that connect each API call to robotics thinking."
        )
    story.append(Paragraph(intro, styles["BodyText"]))
    story.append(Spacer(1, 8))
    summary = [
        ["Context", "Prerecorded drone videos used as a simulated onboard camera"],
        ["Main uses", "Video input, image display, HUD overlays, color detection, brightness measurement, image-based control"],
        ["Libraries", "OpenCV for image/video operations, NumPy for arrays and measurements"],
        ["Audience", "Student" if audience == "Student" else "Teacher and instructor use"],
    ]
    table = Table(summary, colWidths=[3.8 * cm, 12.2 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e9f1f7")),
                ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("FONTSIZE", (0, 0), (-1, -1), 9.1),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 8))
    story.append(Paragraph("How to read this document", styles["Section"]))
    story.append(
        bullets(
            [
                "What it is: the purpose of the method, property, constant, or data type.",
                "Why it is used: the reason it appears in the drone lab.",
                "Example: a short code fragment similar to the classroom code.",
                "Useful in this context: how it helps with the drone-video activities.",
            ],
            styles,
        )
    )
    if audience == "Teacher":
        story.append(
            bullets(
                [
                    "Teacher notes: common student mistakes and useful prompts are included for each entry.",
                ],
                styles,
            )
        )


def add_items(story: list, styles, title: str, items: list[dict], audience: str) -> None:
    story.append(PageBreak())
    story.append(Paragraph(title, styles["Section"]))
    for item in items:
        story.append(Paragraph(item["name"], styles["Entry"]))
        story.append(Paragraph(f"<b>Type:</b> {item['kind']}", styles["BodySmall"]))
        story.append(Paragraph(f"<b>What it is:</b> {item['what']}", styles["BodySmall"]))
        story.append(Paragraph(f"<b>Why it is used:</b> {item['why']}", styles["BodySmall"]))
        story.append(Paragraph(f"<b>Useful in this context:</b> {item['useful']}", styles["BodySmall"]))
        story.append(Paragraph("Example", styles["SmallLabel"]))
        story.append(code_block(item["example"], styles))
        if audience == "Teacher":
            story.append(Paragraph("Teacher notes", styles["SmallLabel"]))
            story.append(bullets(item["teacher_notes"], styles))


def add_context_examples(story: list, styles, audience: str) -> None:
    story.append(PageBreak())
    story.append(Paragraph("Worked Context Examples", styles["Section"]))
    examples = [
        (
            "Example 1: Reading a drone video like a camera stream",
            "cap = cv2.VideoCapture(str(VIDEO_PATH))\n"
            "fps = cap.get(cv2.CAP_PROP_FPS) or 30.0\n"
            "frame_index = 0\n"
            "ok, frame = cap.read()\n"
            "timestamp_s = frame_index / fps",
            "This example combines VideoCapture, CAP_PROP_FPS, read, and a timestamp computation. "
            "It shows how prerecorded video becomes a time-based sensor stream.",
        ),
        (
            "Example 2: Measuring brightness",
            "gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\n"
            "brightness = float(np.mean(gray))",
            "This example shows how cvtColor and np.mean reduce a full image to a simple numeric measurement.",
        ),
        (
            "Example 3: Detecting the virtual red target",
            "hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)\n"
            "mask1 = cv2.inRange(hsv, np.array([0, 140, 120], dtype=np.uint8), np.array([10, 255, 255], dtype=np.uint8))\n"
            "mask2 = cv2.inRange(hsv, np.array([170, 140, 120], dtype=np.uint8), np.array([180, 255, 255], dtype=np.uint8))\n"
            "mask = cv2.bitwise_or(mask1, mask2)\n"
            "ys, xs = np.where(mask > 0)",
            "This example shows how OpenCV and NumPy work together: OpenCV builds the mask, and NumPy extracts the pixel positions.",
        ),
        (
            "Example 4: Drawing a HUD",
            "h, w = frame.shape[:2]\n"
            "cv2.line(frame, (w // 2, 0), (w // 2, h), (255, 255, 255), 1)\n"
            "cv2.circle(frame, (int(cx), int(cy)), 20, (0, 255, 255), 2)\n"
            "cv2.putText(frame, 'mode: TRACK', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 50), 2)",
            "This example shows how image dimensions, line drawing, circles, and text create an explainable operator display.",
        ),
    ]
    for title, code, body in examples:
        story.append(Paragraph(title, styles["Entry"]))
        story.append(code_block(code, styles))
        story.append(Paragraph(body, styles["BodySmall"]))
        if audience == "Teacher":
            story.append(
                Paragraph(
                    "Teaching angle: ask students not only what the code does, but what information it produces for the next stage of the pipeline.",
                    styles["BodySmall"],
                )
            )


def build_pdf(output_path: Path, audience: str) -> None:
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title=f"{audience} NumPy and OpenCV Reference",
        author="OpenAI Codex",
    )
    story: list = []
    add_intro(story, styles, audience)
    add_items(story, styles, "OpenCV Reference", OPENCV_ITEMS, audience)
    add_items(story, styles, "NumPy Reference", NUMPY_ITEMS, audience)
    add_context_examples(story, styles, audience)
    doc.build(story)


if __name__ == "__main__":
    build_pdf(STUDENT_PDF, "Student")
    build_pdf(TEACHER_PDF, "Teacher")
