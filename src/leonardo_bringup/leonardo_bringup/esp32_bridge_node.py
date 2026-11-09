#!/usr/bin/env python3
"""
Production USB Serial Bridge Node for Leonardo da Vinci Robot.
Interfaces ROS 2 topics (/wheel_cmd, /pen_cmd) with ESP32-S3 firmware via ASCII serial.
"""

import time
import threading
import rclpy
from rclpy.node import Node
from leonardo_msgs.msg import WheelSpeeds, PenCommand


class ESP32BridgeNode(Node):
    def __init__(self):
        super().__init__('leonardo_esp32_bridge')

        # Parameters
        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('reconnect_interval_sec', 2.0)

        self.port = self.get_parameter('serial_port').value
        self.baud = self.get_parameter('baud_rate').value
        self.reconnect_interval = self.get_parameter('reconnect_interval_sec').value

        # Publishers & Subscribers
        self.wheel_status_pub = self.create_publisher(WheelSpeeds, '/wheel_status', 20)
        self.wheel_cmd_sub = self.create_subscription(
            WheelSpeeds, '/wheel_cmd', self.wheel_cmd_callback, 10
        )
        self.pen_cmd_sub = self.create_subscription(
            PenCommand, '/pen_cmd', self.pen_cmd_callback, 10
        )

        self.serial_handle = None
        self.lock = threading.Lock()
        self.running = True

        # Background worker thread for serial communication
        self.worker_thread = threading.Thread(target=self.serial_loop, daemon=True)
        self.worker_thread.start()

        self.get_logger().info(
            f'ESP32 Serial Bridge configured for port: {self.port} @ {self.baud} baud.'
        )

    def wheel_cmd_callback(self, msg: WheelSpeeds):
        cmd = f"M {msg.w1:.3f} {msg.w2:.3f} {msg.w3:.3f}\n"
        self.send_serial(cmd)

    def pen_cmd_callback(self, msg: PenCommand):
        cmd = "P1\n" if msg.pen_down else "P0\n"
        self.send_serial(cmd)

    def send_serial(self, data_str: str):
        with self.lock:
            if self.serial_handle and self.serial_handle.is_open:
                try:
                    self.serial_handle.write(data_str.encode('ascii'))
                except Exception as e:
                    self.get_logger().error(f'Error writing to serial: {e}')

    def parse_telemetry(self, line: str):
        parts = line.strip().split()
        if not parts:
            return

        if parts[0] == 'STATUS' and len(parts) >= 5:
            try:
                msg = WheelSpeeds()
                msg.w1 = float(parts[2])
                msg.w2 = float(parts[3])
                msg.w3 = float(parts[4])
                self.wheel_status_pub.publish(msg)
            except ValueError:
                pass
        elif parts[0] == 'ACK':
            self.get_logger().debug(f'ESP32 ACK: {line.strip()}')

    def serial_loop(self):
        try:
            import serial
        except ImportError:
            self.get_logger().warn('pyserial not installed. Bridge running in mock mode.')
            return

        while self.running and rclpy.ok():
            try:
                if self.serial_handle is None or not self.serial_handle.is_open:
                    try:
                        self.serial_handle = serial.Serial(self.port, self.baud, timeout=0.1)
                        self.get_logger().info(f'Connected to ESP32-S3 on {self.port}')
                    except serial.SerialException:
                        time.sleep(self.reconnect_interval)
                        continue

                line = self.serial_handle.readline().decode('ascii', errors='ignore')
                if line:
                    self.parse_telemetry(line)

            except Exception as e:
                self.get_logger().error(f'Serial exception: {e}')
                time.sleep(1.0)

    def destroy_node(self):
        self.running = False
        if self.serial_handle and self.serial_handle.is_open:
            self.serial_handle.close()
        super().destroy_node()


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
