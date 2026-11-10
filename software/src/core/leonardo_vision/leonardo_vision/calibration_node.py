#!/usr/bin/env python3
"""Camera Calibration Node Skeleton for Leonardo da Vinci Robot."""

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import CameraInfo


class CalibrationNode(Node):
    """Publishes calibrated camera intrinsics and distortion parameters."""

    def __init__(self):
        """Initialize the camera calibration publisher node."""
        super().__init__('leonardo_calibration')
        self.info_pub = self.create_publisher(
            CameraInfo, '/camera/camera_info', 10
        )
        self.timer = self.create_timer(1.0, self.publish_camera_info)
        self.get_logger().info(
            'Leonardo Calibration node initialized (skeleton).'
        )

    def publish_camera_info(self):
        """Publish periodic camera info metadata."""
        # TODO: Implement camera info message population
        pass


def main(args=None):
    """Run calibration node main loop."""
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
