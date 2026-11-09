#!/usr/bin/env python3
"""
Camera Calibration Node Skeleton for Leonardo da Vinci Robot.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo


class CalibrationNode(Node):
    def __init__(self):
        super().__init__('leonardo_calibration')
        # TODO: Setup camera_info publisher and calibration parameters
        self.info_pub = self.create_publisher(CameraInfo, '/camera/camera_info', 10)
        self.get_logger().info('Leonardo Calibration node initialized (skeleton).')

    def publish_camera_info(self):
        # TODO: Publish calibrated CameraInfo message
        pass


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
