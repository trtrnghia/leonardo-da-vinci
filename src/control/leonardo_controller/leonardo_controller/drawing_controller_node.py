#!/usr/bin/env python3
"""Drawing Controller Action Server Skeleton for Leonardo da Vinci Robot."""

from geometry_msgs.msg import Twist

from leonardo_msgs.action import DrawArtwork
from leonardo_msgs.msg import DrawStatus, PenCommand
from leonardo_msgs.srv import SetPen

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node


class DrawingControllerNode(Node):
    """Action Server node coordinating artwork stroke execution."""

    def __init__(self):
        """Initialize the drawing controller node."""
        super().__init__('leonardo_drawing_controller')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pen_cmd_pub = self.create_publisher(PenCommand, '/pen_cmd', 10)
        self.status_pub = self.create_publisher(DrawStatus, '/draw_status', 10)
        self.set_pen_srv = self.create_service(
            SetPen, '/controller/set_pen', self.set_pen_callback
        )
        self._action_server = ActionServer(
            self,
            DrawArtwork,
            '/draw_artwork',
            self.execute_callback
        )
        self.get_logger().info(
            'Leonardo Drawing Controller node initialized (skeleton).'
        )

    def set_pen_callback(self, request, response):
        """Handle pen actuation service request."""
        # TODO: Implement physical pen actuation
        _ = request
        response.success = True
        response.message = 'Pen command processed'
        return response

    async def execute_callback(self, goal_handle):
        """Execute drawing artwork action goal."""
        # TODO: Implement sequential stroke execution with feedback
        goal_handle.succeed()
        result = DrawArtwork.Result()
        result.success = True
        return result


def main(args=None):
    """Run the drawing controller node main loop."""
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
