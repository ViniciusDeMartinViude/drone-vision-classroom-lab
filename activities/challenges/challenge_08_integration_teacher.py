"""Teacher reference solution for Challenge 8."""

from dataclasses import dataclass
from pathlib import Path
import math

import cv2
import numpy as np
from video_config import get_video_path


VIDEO_PATH = get_video_path("DJI_0790.MOV")


@dataclass
class TargetDetection:
    found: bool
    cx: float = 0.0
    cy: float = 0.0
    error_x: float = 0.0
    error_y: float = 0.0
    area: float = 0.0


@dataclass
class TwistCommand:
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    throttle: float = 0.0


class DronePipeline:
    def add_target(self, frame: np.ndarray, time_s: float) -> np.ndarray:
        h, w = frame.shape[:2]
        cx = int(w * (0.5 + 0.18 * math.sin(0.5 * time_s)))
        cy = int(h * (0.5 + 0.14 * math.cos(0.7 * time_s)))
        cv2.circle(frame, (cx, cy), 16, (0, 0, 255), -1)
        return frame

    def detect_target(self, frame: np.ndarray) -> TargetDetection:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, np.array([0, 140, 120]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 140, 120]), np.array([180, 255, 255]))
        mask = cv2.bitwise_or(mask1, mask2)
        ys, xs = np.where(mask > 0)
        h, w = frame.shape[:2]
        if xs.size == 0:
            return TargetDetection(False)
        cx = float(xs.mean())
        cy = float(ys.mean())
        return TargetDetection(True, cx, cy, (cx - w / 2.0) / (w / 2.0), (cy - h / 2.0) / (h / 2.0), float(xs.size))

    def compute_command(self, detection: TargetDetection) -> TwistCommand:
        if not detection.found:
            return TwistCommand(yaw=0.15)
        return TwistCommand(
            roll=max(-1.0, min(1.0, -0.7 * detection.error_x)),
            pitch=0.25 if detection.area < 700 else 0.0,
            yaw=max(-0.8, min(0.8, -0.4 * detection.error_x)),
            throttle=max(-0.8, min(0.8, -0.6 * detection.error_y)),
        )

    def draw_hud(self, frame: np.ndarray, detection: TargetDetection, cmd: TwistCommand) -> np.ndarray:
        h, w = frame.shape[:2]
        cv2.line(frame, (w // 2, 0), (w // 2, h), (255, 255, 255), 1)
        cv2.line(frame, (0, h // 2), (w, h // 2), (255, 255, 255), 1)
        if detection.found:
            cv2.circle(frame, (int(detection.cx), int(detection.cy)), 20, (0, 255, 255), 2)
        lines = [
            f"roll={cmd.roll:+.2f}",
            f"pitch={cmd.pitch:+.2f}",
            f"yaw={cmd.yaw:+.2f}",
            f"thr={cmd.throttle:+.2f}",
        ]
        y = 30
        for line in lines:
            cv2.putText(frame, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 50), 2)
            y += 28
        return frame


def main() -> None:
    pipe = DronePipeline()
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_index = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.resize(frame, dsize=None, fx=0.3, fy=0.3)
        time_s = frame_index / fps
        frame = pipe.add_target(frame, time_s)
        detection = pipe.detect_target(frame)
        cmd = pipe.compute_command(detection)
        frame = pipe.draw_hud(frame, detection, cmd)

        cv2.imshow("challenge_08", frame)
        if (cv2.waitKey(20) & 0xFF) == ord("q"):
            break
        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
