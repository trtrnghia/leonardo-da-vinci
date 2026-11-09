import math
import numpy as np
import pytest
from leonardo_kinematics.kinematics import OmniKinematics3Wheel


def test_inverse_forward_consistency():
    kin = OmniKinematics3Wheel(robot_radius=0.15, wheel_radius=0.029)
    test_cases = [
        (0.2, 0.0, 0.0),    # pure X forward
        (0.0, 0.2, 0.0),    # pure Y left
        (0.0, 0.0, 1.0),    # pure Z rotation
        (0.1, -0.15, 0.5),  # mixed motion
    ]

    for vx, vy, wz in test_cases:
        v_in = np.array([vx, vy, wz], dtype=np.float64)
        w_wheels = kin.inverse_kinematics(vx, vy, wz)
        v_out = kin.forward_kinematics(w_wheels[0], w_wheels[1], w_wheels[2])
        np.testing.assert_allclose(v_out, v_in, atol=1e-6)


def test_pure_rotation():
    R = 0.15
    r = 0.029
    kin = OmniKinematics3Wheel(robot_radius=R, wheel_radius=r)
    wz = 2.0
    w_wheels = kin.inverse_kinematics(0.0, 0.0, wz)
    # In pure rotation, all 3 wheels spin at identical speed: w_i = (R / r) * wz
    expected_w = (R / r) * wz
    np.testing.assert_allclose(w_wheels, [expected_w, expected_w, expected_w], atol=1e-6)
