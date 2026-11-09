#!/usr/bin/env python3
"""
Homography Localization Node Skeleton for Leonardo da Vinci Robot.
"""

import rclpy
from rclpy.node import Node
from leonardo_msgs.msg import CanvasPose


class HomographyNode(Node):
    def __init__(self):
        super().__init__('leonardo_homography')
        # TODO: Setup parameters, TF broadcaster, pose publisher, timer
        self.pose_pub = self.create_publisher(CanvasPose, '/canvas_pose', 10)
        self.get_logger().info('Leonardo Homography node initialized (skeleton).')

    def timer_callback(self):
        # TODO: Estimate homography and broadcast canvas -> odom transform
        pass


def main(args=None):
    rclpy.init(args=args)
    node = HomographyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
