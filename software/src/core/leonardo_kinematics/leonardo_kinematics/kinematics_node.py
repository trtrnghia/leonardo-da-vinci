#!/usr/bin/env python3
"""Kinematics ROS 2 Node Skeleton for Leonardo da Vinci Robot."""

from geometry_msgs.msg import Twist

from leonardo_msgs.msg import WheelSpeeds

from nav_msgs.msg import Odometry

import rclpy
from rclpy.node import Node


class KinematicsNode(Node):
    """Bridges Twist velocity commands to wheel setpoints and odometry."""

    def __init__(self):
        """Initialize publishers, subscribers and parameters."""
        super().__init__('leonardo_kinematics')
        self.wheel_cmd_pub = self.create_publisher(
            WheelSpeeds, '/wheel_cmd', 10
        )
        self.odom_pub = self.create_publisher(Odometry, '/odom', 20)
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10
        )
        self.wheel_status_sub = self.create_subscription(
            WheelSpeeds, '/wheel_status', self.wheel_status_callback, 20
        )
        self.get_logger().info(
            'Leonardo Kinematics node initialized (skeleton).'
        )

    def cmd_vel_callback(self, msg: Twist):
        """Convert Twist velocity to individual wheel angular speeds."""
        # TODO: Compute IK and publish to /wheel_cmd
        _ = msg

    def wheel_status_callback(self, msg: WheelSpeeds):
        """Compute FK and publish odometry from measured wheel speeds."""
        # TODO: Compute FK, update odometry, and broadcast TF
        _ = msg


def main(args=None):
    """Run kinematics node main loop."""
    rclpy.init(args=args)
    node = KinematicsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
