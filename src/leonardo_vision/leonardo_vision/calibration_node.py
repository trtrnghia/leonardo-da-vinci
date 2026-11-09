#!/usr/bin/env python3
"""
Camera Calibration Node for Leonardo da Vinci Robot.
Publishes camera intrinsics and lens distortion parameters.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo
from leonardo_vision.camera_calibrator import CameraCalibrator


class CalibrationNode(Node):
    def __init__(self):
        super().__init__('leonardo_calibration')

        self.calibrator = CameraCalibrator()
        self.info_pub = self.create_publisher(CameraInfo, '/camera/camera_info', 10)
        self.timer = self.create_timer(1.0, self.publish_camera_info)

        self.get_logger().info('Leonardo Calibration node ready.')

    def publish_camera_info(self):
        now = self.get_clock().now()
        info = CameraInfo()
        info.header.stamp = now.to_msg()
        info.header.frame_id = 'camera_optical_link'
        info.width = 640
        info.height = 480
        info.distortion_model = 'plumb_bob'
        info.d = [0.0, 0.0, 0.0, 0.0, 0.0]

        K, _ = self.calibrator.get_intrinsics()
        info.k = [float(val) for val in K.flatten()]
        info.p = [
            K[0, 0], 0.0, K[0, 2], 0.0,
            0.0, K[1, 1], K[1, 2], 0.0,
            0.0, 0.0, 1.0, 0.0
        ]
        self.info_pub.publish(info)


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
