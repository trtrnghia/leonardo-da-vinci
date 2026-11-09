"""
Homography Estimator and Visual Pose Tracker Skeleton.
"""

from typing import Tuple
import numpy as np


class HomographyTracker:
    def __init__(self, reprojection_threshold: float = 3.0):
        self.reprojection_threshold = reprojection_threshold
        # TODO: Initialize feature detector / matcher (SIFT, ORB, SuperPoint)

    def estimate_canvas_homography(self, camera_frame, canvas_reference) -> np.ndarray:
        """
        Estimate 3x3 Homography matrix between current camera frame and reference canvas.
        """
        # TODO: Feature matching & RANSAC homography estimation
        pass

    def decompose_homography_to_pose(self, H: np.ndarray) -> Tuple[float, float, float]:
        """
        Decompose 3x3 homography matrix into 2D metric pose (x, y, theta).
        """
        # TODO: Pose extraction
        pass
