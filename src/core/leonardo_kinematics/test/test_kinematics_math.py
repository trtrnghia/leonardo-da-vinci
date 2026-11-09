"""
Kinematics Unit Tests Skeleton.
"""

from leonardo_kinematics.kinematics import OmniKinematics3Wheel


def test_kinematics_skeleton():
    kin = OmniKinematics3Wheel(robot_radius=0.15, wheel_radius=0.029)
    assert kin.R == 0.15
    assert kin.r == 0.029
