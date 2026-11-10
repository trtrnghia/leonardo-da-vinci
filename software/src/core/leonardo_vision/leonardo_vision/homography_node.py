#!/usr/bin/env python3
"""Homography Localization Node Skeleton for Leonardo da Vinci Robot."""

from leonardo_msgs.msg import CanvasPose

import rclpy
from rclpy.node import Node


class HomographyNode(Node):
    """Visual homography localization and canvas frame publisher."""

    def __init__(self):
        """Initialize the homography localization node."""
        super().__init__('leonardo_homography')
        self.pose_pub = self.create_publisher(CanvasPose, '/canvas_pose', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info(
            'Leonardo Homography node initialized (skeleton).'
        )

    def timer_callback(self):
        """Estimate homography and broadcast canvas to odom transform."""
        # TODO: Implement visual homography localization
        pass


def main(args=None):
    """Run homography node main loop."""
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
