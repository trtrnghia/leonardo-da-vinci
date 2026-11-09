"""Camera Calibration and Lens Distortion Correction Engine Skeleton."""

from typing import Tuple

import numpy as np


class CameraCalibrator:
    """Computes camera matrix K and distortion coefficients D."""

    def __init__(
        self,
        fx: float = 600.0,
        fy: float = 600.0,
        cx: float = 320.0,
        cy: float = 240.0
    ):
        """Initialize camera intrinsic default matrices."""
        _ = (fx, fy, cx, cy)
        self.K = np.eye(3, dtype=np.float64)
        self.D = np.zeros(5, dtype=np.float64)

    def calibrate(self, images_list) -> Tuple[np.ndarray, np.ndarray]:
        """Calibrate camera intrinsics K and D from checkerboard images."""
        # TODO: Implement checkerboard corner detection and camera calibration
        _ = images_list
        return (self.K, self.D)

    def undistort(self, frame) -> np.ndarray:
        """Rectify radial and tangential distortion from input frame."""
        # TODO: Implement cv2.undistort
        return frame
