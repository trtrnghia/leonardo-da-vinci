#!/usr/bin/env python3
"""
ROS 2 Kinematics Node for Leonardo da Vinci Drawing Robot.
Bridges Twist (/cmd_vel) to WheelSpeeds (/wheel_cmd) and publishes /odom & TF.
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped, Quaternion
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from leonardo_msgs.msg import WheelSpeeds
from leonardo_kinematics.kinematics import OmniKinematics3Wheel


def euler_to_quaternion(yaw: float) -> Quaternion:
    q = Quaternion()
    q.x = 0.0
    q.y = 0.0
    q.z = math.sin(yaw * 0.5)
    q.w = math.cos(yaw * 0.5)
    return q


class KinematicsNode(Node):
    def __init__(self):
        super().__init__('leonardo_kinematics')

        # Parameters
        self.declare_parameter('robot_radius_m', 0.15)
        self.declare_parameter('wheel_radius_m', 0.029)
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('base_frame', 'base_footprint')
        self.declare_parameter('publish_tf', True)

        robot_radius = self.get_parameter('robot_radius_m').value
        wheel_radius = self.get_parameter('wheel_radius_m').value
        self.odom_frame = self.get_parameter('odom_frame').value
        self.base_frame = self.get_parameter('base_frame').value
        self.publish_tf = self.get_parameter('publish_tf').value

        self.kinematics = OmniKinematics3Wheel(robot_radius, wheel_radius)

        # Odometry state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = self.get_clock().now()

        # Publishers & Subscribers
        self.wheel_cmd_pub = self.create_publisher(WheelSpeeds, '/wheel_cmd', 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 20)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.wheel_status_sub = self.create_subscription(
            WheelSpeeds, '/wheel_status', self.wheel_status_callback, 20
        )

        self.get_logger().info(
            f'Kinematics node active. R={robot_radius}m, r={wheel_radius}m. '
            f'Subscribing /cmd_vel, publishing /wheel_cmd and /odom.'
        )

    def cmd_vel_callback(self, msg: Twist):
        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z

        w_wheels = self.kinematics.inverse_kinematics(vx, vy, wz)

        wheel_msg = WheelSpeeds()
        wheel_msg.w1 = float(w_wheels[0])
        wheel_msg.w2 = float(w_wheels[1])
        wheel_msg.w3 = float(w_wheels[2])
        self.wheel_cmd_pub.publish(wheel_msg)

    def wheel_status_callback(self, msg: WheelSpeeds):
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds * 1e-9
        self.last_time = now

        if dt <= 0.0 or dt > 0.5:
            return

        self.x, self.y, self.theta, vx, vy, wz = self.kinematics.integrate_odometry(
            self.x, self.y, self.theta, msg.w1, msg.w2, msg.w3, dt
        )

        orientation_q = euler_to_quaternion(self.theta)

        # Publish Odometry
        odom_msg = Odometry()
        odom_msg.header.stamp = now.to_msg()
        odom_msg.header.frame_id = self.odom_frame
        odom_msg.child_frame_id = self.base_frame
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0
        odom_msg.pose.pose.orientation = orientation_q
        odom_msg.twist.twist.linear.x = vx
        odom_msg.twist.twist.linear.y = vy
        odom_msg.twist.twist.angular.z = wz
        self.odom_pub.publish(odom_msg)

        # Broadcast TF
        if self.publish_tf:
            t = TransformStamped()
            t.header.stamp = now.to_msg()
            t.header.frame_id = self.odom_frame
            t.child_frame_id = self.base_frame
            t.transform.translation.x = self.x
            t.transform.translation.y = self.y
            t.transform.translation.z = 0.0
            t.transform.rotation = orientation_q
            self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = KinematicsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
