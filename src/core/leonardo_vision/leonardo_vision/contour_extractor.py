"""
Vectorization and Contour Extraction Engine for Leonardo da Vinci Robot.
Implements Canny edge detection, Ramer-Douglas-Peucker (RDP) polyline simplification,
and travel optimization for pen strokes.
"""

import math
from typing import List, Tuple
import numpy as np


def rdp_simplify(points: List[Tuple[float, float]], epsilon: float) -> List[Tuple[float, float]]:
    """
    Ramer-Douglas-Peucker algorithm for polyline decimation.
    :param points: List of (x, y) coordinates.
    :param epsilon: Maximum distance tolerance.
    """
    if len(points) <= 2:
        return points

    # Find point with maximum distance from line between first and last
    first_pt = np.array(points[0], dtype=np.float64)
    last_pt = np.array(points[-1], dtype=np.float64)
    line_vec = last_pt - first_pt
    line_len = np.linalg.norm(line_vec)

    dmax = 0.0
    index = 0

    for i in range(1, len(points) - 1):
        pt = np.array(points[i], dtype=np.float64)
        if line_len > 1e-9:
            d = abs(np.cross(line_vec, first_pt - pt)) / line_len
        else:
            d = np.linalg.norm(pt - first_pt)

        if d > dmax:
            index = i
            dmax = d

    if dmax > epsilon:
        rec_results1 = rdp_simplify(points[:index + 1], epsilon)
        rec_results2 = rdp_simplify(points[index:], epsilon)
        return rec_results1[:-1] + rec_results2
    else:
        return [points[0], points[-1]]


class ContourExtractor:
    def __init__(self, rdp_epsilon: float = 1.5, min_contour_length: int = 10):
        self.rdp_epsilon = rdp_epsilon
        self.min_contour_length = min_contour_length

    def optimize_stroke_order(
        self, strokes: List[List[Tuple[float, float]]]
    ) -> List[List[Tuple[float, float]]]:
        """
        Greedy Nearest-Neighbor heuristic to minimize Pen UP travel distance between strokes.
        """
        if not strokes:
            return []

        unvisited = list(strokes)
        ordered = [unvisited.pop(0)]

        while unvisited:
            last_pt = ordered[-1][-1]
            best_idx = 0
            best_dist = float('inf')
            reverse_needed = False

            for i, stroke in enumerate(unvisited):
                d_start = math.hypot(stroke[0][0] - last_pt[0], stroke[0][1] - last_pt[1])
                d_end = math.hypot(stroke[-1][0] - last_pt[0], stroke[-1][1] - last_pt[1])

                if d_start < best_dist:
                    best_dist = d_start
                    best_idx = i
                    reverse_needed = False
                if d_end < best_dist:
                    best_dist = d_end
                    best_idx = i
                    reverse_needed = True

            next_stroke = unvisited.pop(best_idx)
            if reverse_needed:
                next_stroke.reverse()
            ordered.append(next_stroke)

        return ordered
