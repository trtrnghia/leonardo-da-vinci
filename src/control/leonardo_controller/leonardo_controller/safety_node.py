#!/usr/bin/env python3
"""LiDAR Safety Node Skeleton for Leonardo da Vinci Robot."""

from geometry_msgs.msg import Twist

from leonardo_msgs.msg import PenCommand

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan

from std_msgs.msg import Bool


class SafetyNode(Node):
    """LiDAR Safety supervisor node protecting robot from collisions."""

    def __init__(self):
        """Initialize the safety supervisor node."""
        super().__init__('leonardo_safety')
        self.safety_pub = self.create_publisher(Bool, '/safety_status', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pen_cmd_pub = self.create_publisher(PenCommand, '/pen_cmd', 10)
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )
        self.get_logger().info(
            'Leonardo Safety node initialized (skeleton).'
        )

    def scan_callback(self, msg: LaserScan):
        """Process incoming 2D LaserScan message."""
        # TODO: Detect obstacle intrusion and trigger emergency halt
        _ = msg


def main(args=None):
    """Run safety supervisor node main loop."""
    rclpy.init(args=args)
    node = SafetyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
