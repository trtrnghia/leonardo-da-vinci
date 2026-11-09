#!/usr/bin/env python3
"""
Drawing Action Server and Execution Controller Node for Leonardo da Vinci Robot.
Coordinates sequential stroke tracing, pen lift/lower actions, and handles pause/resume.
"""

import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from leonardo_msgs.msg import PenCommand, DrawStatus
from leonardo_msgs.srv import SetPen
from leonardo_msgs.action import DrawArtwork
from leonardo_controller.trajectory_generator import TrajectoryGenerator


class DrawingControllerNode(Node):
    def __init__(self):
        super().__init__("leonardo_drawing_controller")

        self.declare_parameter("default_draw_speed", 0.05)
        self.declare_parameter("default_transit_speed", 0.12)
        self.declare_parameter("pen_dwell_delay_sec", 0.25)

        draw_speed = self.get_parameter("default_draw_speed").value
        transit_speed = self.get_parameter("default_transit_speed").value
        self.pen_dwell_delay = self.get_parameter("pen_dwell_delay_sec").value

        self.traj_gen = TrajectoryGenerator(draw_speed, transit_speed)
        self.safety_halt = False

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.pen_cmd_pub = self.create_publisher(PenCommand, "/pen_cmd", 10)
        self.status_pub = self.create_publisher(DrawStatus, "/draw_status", 10)

        # Service
        self.set_pen_srv = self.create_service(
            SetPen, "/controller/set_pen", self.set_pen_callback
        )

        # Subscriber to safety
        self.safety_sub = self.create_subscription(
            Bool, "/safety_status", self.safety_status_callback, 10
        )

        # Action Server
        self._action_server = ActionServer(
            self,
            DrawArtwork,
            "/draw_artwork",
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
        )

        self.get_logger().info("Leonardo Drawing Controller Action Server initialized.")

    def goal_callback(self, goal_request):
        self.get_logger().info(
            f"Received artwork goal request: {goal_request.image_path}"
        )
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info("Received cancellation request.")
        return CancelResponse.ACCEPT

    def safety_status_callback(self, msg: Bool):
        self.safety_halt = msg.data

    def set_pen_callback(self, request, response):
        cmd = PenCommand()
        cmd.pen_down = request.pen_down
        self.pen_cmd_pub.publish(cmd)
        response.success = True
        response.message = f"Pen set to {'DOWN' if request.pen_down else 'UP'}"
        return response

    async def execute_callback(self, goal_handle):
        self.get_logger().info("Executing artwork drawing task...")
        feedback_msg = DrawArtwork.Feedback()
        result = DrawArtwork.Result()

        total_dummy_strokes = 5
        start_time = time.time()

        for stroke_idx in range(1, total_dummy_strokes + 1):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                # Stop robot and lift pen
                self.cmd_vel_pub.publish(Twist())
                pen_up = PenCommand()
                pen_up.pen_down = False
                self.pen_cmd_pub.publish(pen_up)
                result.success = False
                result.message = "Drawing task was canceled by user."
                return result

            # Wait while safety halt is active
            while self.safety_halt and rclpy.ok():
                self.get_logger().warn("Drawing paused due to safety obstacle...")
                time.sleep(0.5)

            # Update feedback
            feedback_msg.current_stroke_index = stroke_idx
            feedback_msg.total_strokes = total_dummy_strokes
            feedback_msg.percent_complete = (stroke_idx / total_dummy_strokes) * 100.0
            feedback_msg.current_state = "DRAWING"
            goal_handle.publish_feedback(feedback_msg)

            # Publish status topic
            status_msg = DrawStatus()
            status_msg.current_stroke = stroke_idx
            status_msg.total_strokes = total_dummy_strokes
            status_msg.progress_percentage = feedback_msg.percent_complete
            status_msg.state = feedback_msg.current_state
            self.status_pub.publish(status_msg)

            time.sleep(0.5)

        # Lift pen and stop
        pen_up = PenCommand()
        pen_up.pen_down = False
        self.pen_cmd_pub.publish(pen_up)
        self.cmd_vel_pub.publish(Twist())

        goal_handle.succeed()
        result.success = True
        result.strokes_completed = total_dummy_strokes
        result.total_drawing_time_sec = float(time.time() - start_time)
        result.message = "Artwork successfully completed."
        return result


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


if __name__ == "__main__":
    main()
