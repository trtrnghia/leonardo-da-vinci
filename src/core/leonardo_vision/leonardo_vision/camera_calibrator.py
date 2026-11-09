"""
Camera Calibration and Lens Distortion Correction Engine.
Maintains intrinsic matrix (K) and distortion parameters (D).
"""

from typing import Tuple
import numpy as np


class CameraCalibrator:
    def __init__(self, fx: float = 600.0, fy: float = 600.0, cx: float = 320.0, cy: float = 240.0):
        self.K = np.array([
            [fx, 0.0, cx],
            [0.0, fy, cy],
            [0.0, 0.0, 1.0]
        ], dtype=np.float64)
        self.D = np.zeros(5, dtype=np.float64)  # k1, k2, p1, p2, k3

    def set_intrinsics(self, K: np.ndarray, D: np.ndarray):
        self.K = np.array(K, dtype=np.float64)
        self.D = np.array(D, dtype=np.float64)

    def get_intrinsics(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.K, self.D
