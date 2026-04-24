from __future__ import annotations

import math

import cv2
import numpy as np

from drone_lab.core.messages import FrameMessage, TargetDetection


class VirtualTargetNode:
    def __init__(self, radius_px: int = 18) -> None:
        self.radius_px = radius_px

    def annotate(self, frame_msg: FrameMessage) -> FrameMessage:
        frame = frame_msg.image.copy()
        h, w = frame.shape[:2]
        t = frame_msg.timestamp_s
        cx = int(w * (0.5 + 0.22 * math.sin(0.55 * t)))
        cy = int(h * (0.5 + 0.18 * math.cos(0.70 * t)))
        cv2.circle(frame, (cx, cy), self.radius_px, (0, 0, 255), -1)
        frame_msg.image = frame
        return frame_msg


class TargetDetectorNode:
    def __init__(self) -> None:
        self.lower = np.array([0, 140, 120], dtype=np.uint8)
        self.upper = np.array([10, 255, 255], dtype=np.uint8)

    def detect(self, frame_msg: FrameMessage) -> tuple[TargetDetection, np.ndarray]:
        frame = frame_msg.image
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)
        ys, xs = np.where(mask > 0)
        h, w = frame.shape[:2]
        if xs.size == 0:
            return TargetDetection(found=False), mask

        cx = float(xs.mean())
        cy = float(ys.mean())
        area = float(xs.size)
        return (
            TargetDetection(
                found=True,
                cx=cx,
                cy=cy,
                area=area,
                error_x=(cx - w / 2.0) / (w / 2.0),
                error_y=(cy - h / 2.0) / (h / 2.0),
            ),
            mask,
        )
