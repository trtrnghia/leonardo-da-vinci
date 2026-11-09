#!/usr/bin/env python3
"""Vision Node Skeleton for Leonardo da Vinci Robot."""

from leonardo_msgs.srv import CalibrateCanvas

import rclpy
from rclpy.node import Node


class VisionNode(Node):
    """Computer vision node extracting strokes and handling calibration."""

    def __init__(self):
        """Initialize the vision node."""
        super().__init__('leonardo_vision')
        self.calib_srv = self.create_service(
            CalibrateCanvas,
            '/vision/calibrate_canvas',
            self.calibrate_canvas_callback
        )
        self.get_logger().info('Leonardo Vision node initialized (skeleton).')

    def calibrate_canvas_callback(self, request, response):
        """Process canvas image calibration request."""
        _ = request
        response.success = True
        response.message = 'Skeleton response'
        return response


def main(args=None):
    """Run vision node main loop."""
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
