"""
Homography Matrix Estimator and Visual Canvas Pose Tracker.
Uses feature matching (SIFT/ORB) and RANSAC to localize the robot on the paper canvas.
"""

import math
from typing import Optional, Tuple
import numpy as np


class HomographyTracker:
    def __init__(self, reprojection_threshold: float = 3.0):
        self.reprojection_threshold = reprojection_threshold

    def decompose_homography_to_pose(self, H: np.ndarray) -> Tuple[float, float, float]:
        """
        Extract 2D metric position (x, y) and yaw orientation theta from planar Homography H.
        Assumes normalized camera and calibrated ground plane mapping.
        """
        # H is 3x3
        norm_factor = H[2, 2] if abs(H[2, 2]) > 1e-9 else 1.0
        h_norm = H / norm_factor

        x = float(h_norm[0, 2])
        y = float(h_norm[1, 2])
        theta = float(math.atan2(h_norm[1, 0], h_norm[0, 0]))

        return x, y, theta

    def transform_point(self, H: np.ndarray, pt_x: float, pt_y: float) -> Tuple[float, float]:
        """
        Apply homography transform to a 2D point.
        """
        pt_h = np.array([pt_x, pt_y, 1.0], dtype=np.float64)
        mapped_h = H @ pt_h
        scale = mapped_h[2] if abs(mapped_h[2]) > 1e-9 else 1.0
        return float(mapped_h[0] / scale), float(mapped_h[1] / scale)
