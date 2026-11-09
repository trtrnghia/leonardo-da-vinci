#!/usr/bin/env python3
"""
ESP32 Serial Bridge Node Skeleton for Leonardo da Vinci Robot.
"""

import rclpy
from rclpy.node import Node
from leonardo_msgs.msg import WheelSpeeds, PenCommand


class ESP32BridgeNode(Node):
    def __init__(self):
        super().__init__('leonardo_esp32_bridge')
        # TODO: Setup serial communication, publishers and subscribers
        self.wheel_status_pub = self.create_publisher(WheelSpeeds, '/wheel_status', 20)
        self.wheel_cmd_sub = self.create_subscription(
            WheelSpeeds, '/wheel_cmd', self.wheel_cmd_callback, 10
        )
        self.pen_cmd_sub = self.create_subscription(
            PenCommand, '/pen_cmd', self.pen_cmd_callback, 10
        )
        self.get_logger().info('Leonardo ESP32 Bridge node initialized (skeleton).')

    def wheel_cmd_callback(self, msg: WheelSpeeds):
        # TODO: Send wheel velocity setpoints to ESP32 over serial
        pass

    def pen_cmd_callback(self, msg: PenCommand):
        # TODO: Send pen UP/DOWN commands to ESP32 over serial
        pass

    def parse_telemetry(self, line: str):
        # TODO: Parse incoming telemetry from ESP32
        pass


def main(args=None):
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
