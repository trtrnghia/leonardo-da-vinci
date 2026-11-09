#!/usr/bin/env python3
"""
Vision Node Skeleton for Leonardo da Vinci Robot.
"""

import rclpy
from rclpy.node import Node
from leonardo_msgs.srv import CalibrateCanvas


class VisionNode(Node):
    def __init__(self):
        super().__init__('leonardo_vision')
        # TODO: Setup parameters, subscribers, publishers, services
        self.calib_srv = self.create_service(
            CalibrateCanvas, '/vision/calibrate_canvas', self.calibrate_canvas_callback
        )
        self.get_logger().info('Leonardo Vision node initialized (skeleton).')

    def calibrate_canvas_callback(self, request, response):
        # TODO: Process canvas image calibration
        response.success = True
        response.message = 'Skeleton response'
        return response


def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
