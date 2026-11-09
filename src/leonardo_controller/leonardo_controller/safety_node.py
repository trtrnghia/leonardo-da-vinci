#!/usr/bin/env python3
"""
LiDAR Safety Supervisor Node for Leonardo da Vinci Robot.
Monitors 2D LaserScan, detects intrusion within safety radius (< 0.30m),
and triggers immediate velocity halt and pen lift.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from leonardo_msgs.msg import PenCommand


class SafetyNode(Node):
    def __init__(self):
        super().__init__('leonardo_safety')

        self.declare_parameter('safety_radius_m', 0.30)
        self.declare_parameter('clearance_time_sec', 2.0)

        self.safety_radius = self.get_parameter('safety_radius_m').value
        self.clearance_time = self.get_parameter('clearance_time_sec').value

        self.is_halted = False
        self.clear_start_time = None

        # Publishers
        self.safety_pub = self.create_publisher(Bool, '/safety_status', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pen_cmd_pub = self.create_publisher(PenCommand, '/pen_cmd', 10)

        # Subscriber
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        self.get_logger().info(
            f'Leonardo Safety Node active. Monitoring /scan within {self.safety_radius}m.'
        )

    def scan_callback(self, msg: LaserScan):
        now = self.get_clock().now()
        ranges = [r for r in msg.ranges if msg.range_min < r < msg.range_max]

        min_dist = min(ranges) if ranges else float('inf')
        obstacle_detected = min_dist < self.safety_radius

        if obstacle_detected:
            self.clear_start_time = None
            if not self.is_halted:
                self.get_logger().warn(f'OBSTACLE INTRUSION ({min_dist:.2f}m < {self.safety_radius}m)! HALTING!')
                self.is_halted = True

                # Immediately stop wheels and lift pen
                self.cmd_vel_pub.publish(Twist())
                pen_up = PenCommand()
                pen_up.pen_down = False
                self.pen_cmd_pub.publish(pen_up)
        else:
            if self.is_halted:
                if self.clear_start_time is None:
                    self.clear_start_time = now
                else:
                    elapsed = (now - self.clear_start_time).nanoseconds * 1e-9
                    if elapsed >= self.clearance_time:
                        self.get_logger().info(f'Area cleared for {self.clearance_time}s. RESUMING.')
                        self.is_halted = False
                        self.clear_start_time = None

        status_msg = Bool()
        status_msg.data = self.is_halted
        self.safety_pub.publish(status_msg)


def main(args=None):
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
