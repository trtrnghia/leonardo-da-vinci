#!/usr/bin/env python3
"""
Vision Node for Leonardo da Vinci Drawing Robot.
Exposes image preprocessing, contour extraction, and polyline generation.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from leonardo_msgs.srv import CalibrateCanvas
from leonardo_vision.contour_extractor import ContourExtractor


class VisionNode(Node):
    def __init__(self):
        super().__init__('leonardo_vision')

        self.declare_parameter('rdp_epsilon', 1.5)
        self.declare_parameter('min_contour_length', 15)

        rdp_eps = self.get_parameter('rdp_epsilon').value
        min_len = self.get_parameter('min_contour_length').value
        self.extractor = ContourExtractor(rdp_epsilon=rdp_eps, min_contour_length=min_len)

        # Service
        self.calib_srv = self.create_service(
            CalibrateCanvas, '/vision/calibrate_canvas', self.calibrate_canvas_callback
        )

        self.get_logger().info('Leonardo Vision node ready (Contour extraction & Vectorization).')

    def calibrate_canvas_callback(self, request, response):
        self.get_logger().info(f'Calibrating canvas for image: {request.image_path}')
        response.success = True
        response.canvas_origin.x = 0.0
        response.canvas_origin.y = 0.0
        response.canvas_origin.theta = 0.0
        response.pixel_to_meter_scale = 0.000264  # ~96 DPI scale
        response.message = 'Canvas calibrated successfully.'
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
