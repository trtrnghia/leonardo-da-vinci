#!/usr/bin/env python3
"""
ESP32-S3 Bridge Node Skeleton for Leonardo da Vinci Robot.
Handles USB serial communication (115200 baud) for motor setpoints and pen actuation.
"""

import rclpy
from rclpy.node import Node


class ESP32BridgeNode(Node):
    def __init__(self):
        super().__init__('leonardo_esp32_bridge')
        self.get_logger().info('Leonardo ESP32-S3 Bridge node initialized (skeleton).')


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
