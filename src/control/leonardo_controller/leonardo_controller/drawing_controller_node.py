#!/usr/bin/env python3
"""
Drawing Controller Action Server Skeleton for Leonardo da Vinci Robot.
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from leonardo_msgs.msg import PenCommand, DrawStatus
from leonardo_msgs.srv import SetPen
from leonardo_msgs.action import DrawArtwork


class DrawingControllerNode(Node):
    def __init__(self):
        super().__init__('leonardo_drawing_controller')
        # TODO: Setup ActionServer for DrawArtwork, publishers, subscribers, services
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pen_cmd_pub = self.create_publisher(PenCommand, '/pen_cmd', 10)
        self.status_pub = self.create_publisher(DrawStatus, '/draw_status', 10)
        self.set_pen_srv = self.create_service(SetPen, '/controller/set_pen', self.set_pen_callback)

        self.get_logger().info('Leonardo Drawing Controller node initialized (skeleton).')

    def set_pen_callback(self, request, response):
        # TODO: Pen actuation command
        response.success = True
        return response

    async def execute_callback(self, goal_handle):
        # TODO: Execute sequential drawing strokes with feedback
        pass


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
