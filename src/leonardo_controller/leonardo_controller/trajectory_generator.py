"""
Trajectory Generator and Waypoint Interpolator for Leonardo da Vinci Robot.
Generates smooth velocity setpoints along polyline segments.
"""

import math
from typing import List, Tuple


class TrajectoryGenerator:
    def __init__(self, default_draw_speed: float = 0.05, transit_speed: float = 0.12):
        self.default_draw_speed = default_draw_speed
        self.transit_speed = transit_speed

    def interpolate_segment(
        self, p1: Tuple[float, float], p2: Tuple[float, float], step_size: float = 0.005
    ) -> List[Tuple[float, float]]:
        """
        Interpolates intermediate waypoints along a straight segment with fixed spatial resolution.
        """
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = math.hypot(dx, dy)

        if dist < 1e-6:
            return [p1]

        steps = max(1, int(math.ceil(dist / step_size)))
        waypoints = []
        for i in range(steps + 1):
            ratio = float(i) / float(steps)
            waypoints.append((p1[0] + dx * ratio, p1[1] + dy * ratio))
        return waypoints
