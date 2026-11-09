#!/usr/bin/env python3
"""
LiDAR Safety Node Skeleton for Leonardo da Vinci Robot.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from leonardo_msgs.msg import PenCommand


class SafetyNode(Node):
    def __init__(self):
        super().__init__('leonardo_safety')
        # TODO: Setup /scan subscriber, safety publishers
        self.safety_pub = self.create_publisher(Bool, '/safety_status', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pen_cmd_pub = self.create_publisher(PenCommand, '/pen_cmd', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        self.get_logger().info('Leonardo Safety node initialized (skeleton).')

    def scan_callback(self, msg: LaserScan):
        # TODO: Detect obstacle intrusion within safety distance and trigger halt
        pass


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
