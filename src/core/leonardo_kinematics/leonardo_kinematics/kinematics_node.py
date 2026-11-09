#!/usr/bin/env python3
"""
Kinematics ROS 2 Node Skeleton for Leonardo da Vinci Robot.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from leonardo_msgs.msg import WheelSpeeds


class KinematicsNode(Node):
    def __init__(self):
        super().__init__('leonardo_kinematics')
        # TODO: Declare parameters, publishers, subscribers, TF broadcasters
        self.get_logger().info('Leonardo Kinematics node initialized (skeleton).')

    def cmd_vel_callback(self, msg: Twist):
        # TODO: Convert cmd_vel Twist to wheel speeds via IK
        pass

    def wheel_status_callback(self, msg: WheelSpeeds):
        # TODO: Compute FK, update odometry, publish /odom and broadcast TF
        pass


def main(args=None):
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
