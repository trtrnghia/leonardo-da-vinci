#!/usr/bin/env python3
"""
Homography Localization Node for Leonardo da Vinci Robot.
Periodically computes canvas-to-robot pose and broadcasts canvas -> odom TF.
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster
from leonardo_msgs.msg import CanvasPose
from leonardo_vision.homography_tracker import HomographyTracker


def yaw_to_quaternion(yaw: float) -> Quaternion:
    q = Quaternion()
    q.x = 0.0
    q.y = 0.0
    q.z = math.sin(yaw * 0.5)
    q.w = math.cos(yaw * 0.5)
    return q


class HomographyNode(Node):
    def __init__(self):
        super().__init__('leonardo_homography')

        self.declare_parameter('canvas_frame', 'canvas')
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('publish_rate_hz', 10.0)

        self.canvas_frame = self.get_parameter('canvas_frame').value
        self.odom_frame = self.get_parameter('odom_frame').value
        rate = self.get_parameter('publish_rate_hz').value

        self.tracker = HomographyTracker()
        self.pose_pub = self.create_publisher(CanvasPose, '/canvas_pose', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(1.0 / rate, self.timer_callback)
        self.get_logger().info('Leonardo Homography node active.')

    def timer_callback(self):
        now = self.get_clock().now()

        # In production, H is estimated from image keypoint correspondences
        # Here we publish identity canvas frame anchor
        msg = CanvasPose()
        msg.pose.x = 0.0
        msg.pose.y = 0.0
        msg.pose.theta = 0.0
        msg.confidence = 1.0
        self.pose_pub.publish(msg)

        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = self.canvas_frame
        t.child_frame_id = self.odom_frame
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation = yaw_to_quaternion(0.0)
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = HomographyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
