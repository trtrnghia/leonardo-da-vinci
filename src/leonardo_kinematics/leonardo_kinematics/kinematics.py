"""
Core mathematical kinematics engine for 3-Wheel Omni AGV (120-degree symmetry).
Provides inverse kinematics, forward kinematics, and dead-reckoning odometry integration.
"""

import math
import numpy as np


class OmniKinematics3Wheel:
    """
    3-Wheel 120-degree Omni robot kinematics model.

    Coordinate system:
      - X forward, Y left, Z up.
      - Wheel 1 at angle 0 deg (aligned along Y).
      - Wheel 2 at angle 120 deg.
      - Wheel 3 at angle 240 deg.
    """

    def __init__(self, robot_radius: float = 0.15, wheel_radius: float = 0.029):
        """
        :param robot_radius: Distance from robot center to each wheel contact point in meters (R).
        :param wheel_radius: Radius of each omni-wheel in meters (r).
        """
        self.R = float(robot_radius)
        self.r = float(wheel_radius)

        # Inverse Kinematics matrix: (w1, w2, w3)^T = (1/r) * M_ik * (vx, vy, wz)^T
        # Rows:
        # Wheel 1 (0 deg):   [ 0,             1,    R ]
        # Wheel 2 (120 deg): [-sqrt(3)/2,  -1/2,    R ]
        # Wheel 3 (240 deg): [ sqrt(3)/2,  -1/2,    R ]
        sqrt3_2 = math.sqrt(3.0) / 2.0
        self.M_ik = np.array([
            [0.0, 1.0, self.R],
            [-sqrt3_2, -0.5, self.R],
            [sqrt3_2, -0.5, self.R]
        ], dtype=np.float64) / self.r

        # Forward Kinematics matrix: (vx, vy, wz)^T = r * M_fk * (w1, w2, w3)^T
        # M_fk = pinv(M_ik * r)
        self.M_fk = self.r * np.array([
            [0.0, -1.0 / math.sqrt(3.0), 1.0 / math.sqrt(3.0)],
            [2.0 / 3.0, -1.0 / 3.0, -1.0 / 3.0],
            [1.0 / (3.0 * self.R), 1.0 / (3.0 * self.R), 1.0 / (3.0 * self.R)]
        ], dtype=np.float64)

    def inverse_kinematics(self, vx: float, vy: float, wz: float) -> np.ndarray:
        """
        Compute required wheel angular velocities from robot body velocities.
        :param vx: Linear velocity along X (forward) in m/s.
        :param vy: Linear velocity along Y (left) in m/s.
        :param wz: Angular velocity around Z (counter-clockwise) in rad/s.
        :return: np.ndarray of shape (3,) containing [w1, w2, w3] in rad/s.
        """
        vel_body = np.array([vx, vy, wz], dtype=np.float64)
        return self.M_ik @ vel_body

    def forward_kinematics(self, w1: float, w2: float, w3: float) -> np.ndarray:
        """
        Compute robot body velocities from wheel angular velocities.
        :param w1, w2, w3: Wheel angular velocities in rad/s.
        :return: np.ndarray of shape (3,) containing [vx, vy, wz] in body frame.
        """
        wheels = np.array([w1, w2, w3], dtype=np.float64)
        return self.M_fk @ wheels

    def integrate_odometry(self, current_x: float, current_y: float, current_theta: float,
                           w1: float, w2: float, w3: float, dt: float):
        """
        Integrate dead-reckoning odometry over time step dt.
        :return: tuple (new_x, new_y, new_theta, vx_body, vy_body, wz_body)
        """
        body_vel = self.forward_kinematics(w1, w2, w3)
        vx, vy, wz = body_vel[0], body_vel[1], body_vel[2]

        delta_theta = wz * dt
        mid_theta = current_theta + delta_theta * 0.5

        delta_x = (vx * math.cos(mid_theta) - vy * math.sin(mid_theta)) * dt
        delta_y = (vx * math.sin(mid_theta) + vy * math.cos(mid_theta)) * dt

        new_x = current_x + delta_x
        new_y = current_y + delta_y
        new_theta = (current_theta + delta_theta + math.pi) % (2.0 * math.pi) - math.pi

        return new_x, new_y, new_theta, vx, vy, wz
