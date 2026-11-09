#!/usr/bin/env python3
"""
Camera Calibration Node Skeleton for Leonardo da Vinci Robot.
Computes intrinsic camera matrix and lens distortion coefficients.
"""

import rclpy
from rclpy.node import Node


class CalibrationNode(Node):
    def __init__(self):
        super().__init__('leonardo_calibration')
        self.get_logger().info('Leonardo Calibration node initialized (skeleton).')


def main(args=None):
    rclpy.init(args=args)
    node = CalibrationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
