#!/usr/bin/env python3
"""
Safety Node Skeleton for Leonardo da Vinci Robot.
Monitors 2D LiDAR /scan topic and triggers emergency stop / pen lift on obstacle intrusion.
"""

import rclpy
from rclpy.node import Node


class SafetyNode(Node):
    def __init__(self):
        super().__init__('leonardo_safety')
        self.get_logger().info('Leonardo Safety node initialized (skeleton).')


def main(args=None):
    rclpy.init(args=args)
    node = SafetyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
