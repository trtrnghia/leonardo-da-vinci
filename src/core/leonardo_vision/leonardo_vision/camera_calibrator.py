"""
Camera Calibration and Lens Distortion Correction Engine Skeleton.
"""

from typing import Tuple
import numpy as np


class CameraCalibrator:
    def __init__(self, fx: float = 600.0, fy: float = 600.0, cx: float = 320.0, cy: float = 240.0):
        self.K = np.eye(3, dtype=np.float64)
        self.D = np.zeros(5, dtype=np.float64)

    def calibrate(self, images_list) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calibrate camera intrinsics K and distortion coefficients D using checkerboard frames.
        """
        # TODO: cv2.calibrateCamera implementation
        pass

    def undistort(self, frame) -> np.ndarray:
        """
        Rectify lens distortion on input frame.
        """
        # TODO: cv2.undistort implementation
        pass
