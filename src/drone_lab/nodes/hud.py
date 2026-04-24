from __future__ import annotations

import cv2
import numpy as np

from drone_lab.core.messages import DroneState, FrameMessage, TargetDetection, TelemetryMessage


class HudNode:
    def __init__(self, show_mask: bool = False) -> None:
        self.show_mask = show_mask

    def draw(
        self,
        frame_msg: FrameMessage,
        state: DroneState,
        target: TargetDetection | None = None,
        telemetry: TelemetryMessage | None = None,
        mask: np.ndarray | None = None,
    ) -> np.ndarray:
        frame = frame_msg.image.copy()
        h, w = frame.shape[:2]
        cv2.line(frame, (w // 2, 0), (w // 2, h), (255, 255, 255), 1)
        cv2.line(frame, (0, h // 2), (w, h // 2), (255, 255, 255), 1)

        if target and target.found:
            cv2.circle(frame, (int(target.cx), int(target.cy)), 20, (0, 255, 255), 2)
            cv2.putText(
                frame,
                f"target ex={target.error_x:+.2f} ey={target.error_y:+.2f}",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

        lines = [
            f"src: {frame_msg.source_name}",
            f"frame: {frame_msg.frame_index}  t={frame_msg.timestamp_s:6.2f}s",
            f"mode: {state.mode}",
            (
                "cmd "
                f"roll={state.cmd.roll:+.2f} pitch={state.cmd.pitch:+.2f} "
                f"yaw={state.cmd.yaw:+.2f} thr={state.cmd.throttle:+.2f}"
            ),
        ]

        if telemetry:
            lines.append(
                "telemetry "
                f"lat={telemetry.gps_lat if telemetry.gps_lat is not None else 'n/a'} "
                f"lon={telemetry.gps_lon if telemetry.gps_lon is not None else 'n/a'} "
                f"baro={telemetry.barometer_m if telemetry.barometer_m is not None else 'n/a'}"
            )

        y = 25
        for line in lines:
            cv2.putText(frame, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (50, 255, 50), 2)
            y += 24

        if self.show_mask and mask is not None:
            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            mask_bgr = cv2.resize(mask_bgr, (w // 4, h // 4))
            frame[10 : 10 + mask_bgr.shape[0], w - mask_bgr.shape[1] - 10 : w - 10] = mask_bgr

        return frame
