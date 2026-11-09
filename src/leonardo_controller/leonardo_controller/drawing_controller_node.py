#!/usr/bin/env python3
"""
Drawing Controller Node Skeleton for Leonardo da Vinci Robot.
Coordinates drawing state transitions (Pen UP / DOWN) and stroke trajectory tracking.
"""

import rclpy
from rclpy.node import Node


class DrawingControllerNode(Node):
    def __init__(self):
        super().__init__('leonardo_drawing_controller')
        self.get_logger().info('Leonardo Drawing Controller node initialized (skeleton).')


def main(args=None):
    rclpy.init(args=args)
    node = DrawingControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
