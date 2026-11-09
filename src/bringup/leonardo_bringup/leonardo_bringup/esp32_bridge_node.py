#!/usr/bin/env python3
"""ESP32 Serial Bridge Node Skeleton for Leonardo da Vinci Robot."""

from leonardo_msgs.msg import PenCommand, WheelSpeeds

import rclpy
from rclpy.node import Node


class ESP32BridgeNode(Node):
    """Bridges ROS 2 topics to ESP32 microcontroller over USB serial."""

    def __init__(self):
        """Initialize serial bridge node, publishers and subscribers."""
        super().__init__('leonardo_esp32_bridge')
        self.wheel_status_pub = self.create_publisher(
            WheelSpeeds, '/wheel_status', 20
        )
        self.wheel_cmd_sub = self.create_subscription(
            WheelSpeeds, '/wheel_cmd', self.wheel_cmd_callback, 10
        )
        self.pen_cmd_sub = self.create_subscription(
            PenCommand, '/pen_cmd', self.pen_cmd_callback, 10
        )
        self.get_logger().info(
            'Leonardo ESP32 Bridge node initialized (skeleton).'
        )

    def wheel_cmd_callback(self, msg: WheelSpeeds):
        """Send wheel setpoints to ESP32 over serial."""
        # TODO: Implement serial transmission of wheel speeds
        _ = msg

    def pen_cmd_callback(self, msg: PenCommand):
        """Send pen UP/DOWN commands to ESP32 over serial."""
        # TODO: Implement serial transmission of pen state
        _ = msg

    def parse_telemetry(self, line: str):
        """Parse incoming ASCII status string from ESP32."""
        # TODO: Parse status telemetry
        _ = line


def main(args=None):
    """Run ESP32 bridge node main loop."""
    rclpy.init(args=args)
    node = ESP32BridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
