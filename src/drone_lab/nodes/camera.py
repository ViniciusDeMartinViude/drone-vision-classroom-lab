from __future__ import annotations

from pathlib import Path

import cv2

from drone_lab.core.bus import MessageBus
from drone_lab.core.messages import FrameMessage
from drone_lab.core.node import Node


class CameraNode(Node):
    def __init__(self, bus: MessageBus, video_path: str, scale: float = 0.5) -> None:
        super().__init__("camera_node", bus)
        self.video_path = Path(video_path)
        self.scale = scale
        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            raise FileNotFoundError(f"Could not open video: {self.video_path}")
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0

    def read(self, frame_index: int) -> FrameMessage | None:
        ok, frame = self.cap.read()
        if not ok:
            return None
        if self.scale != 1.0:
            frame = cv2.resize(frame, dsize=None, fx=self.scale, fy=self.scale)
        return FrameMessage(
            topic="camera/frame",
            frame_index=frame_index,
            timestamp_s=frame_index / self.fps,
            image=frame,
            source_name=self.video_path.name,
        )

    def close(self) -> None:
        self.cap.release()
