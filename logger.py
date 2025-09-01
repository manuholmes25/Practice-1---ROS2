import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose
import csv
import os
from datetime import datetime

class LoggerNode(Node):
    def __init__(self):
        super().__init__('logger_node')

        self.sub_cmd = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        self.sub_pose = self.create_subscription(Pose, '/pose', self.pose_callback, 10)

        filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.filepath = os.path.join(os.getcwd(), filename)

        self.get_logger().info(f"Registrando datos en: {self.filepath}")

        self.csvfile = open(self.filepath, 'w', newline='')
        self.writer = csv.writer(self.csvfile)
        self.writer.writerow([
            "timestamp",
            "cmd_vel.linear.x", "cmd_vel.linear.y", "cmd_vel.linear.z",
            "cmd_vel.angular.x", "cmd_vel.angular.y", "cmd_vel.angular.z",
            "pose.position.x", "pose.position.y", "pose.position.z",
            "pose.orientation.x", "pose.orientation.y", "pose.orientation.z", "pose.orientation.w"
        ])

        self.last_cmd = None
        self.last_pose = None

    def cmd_callback(self, msg):
        self.last_cmd = msg
        self.log_data()

    def pose_callback(self, msg):
        self.last_pose = msg
        self.log_data()

    def log_data(self):
        if self.last_cmd is not None and self.last_pose is not None:
            row = [
                self.get_clock().now().to_msg().sec + self.get_clock().now().to_msg().nanosec * 1e-9,
                self.last_cmd.linear.x, self.last_cmd.linear.y, self.last_cmd.linear.z,
                self.last_cmd.angular.x, self.last_cmd.angular.y, self.last_cmd.angular.z,
                self.last_pose.position.x, self.last_pose.position.y, self.last_pose.position.z,
                self.last_pose.orientation.x, self.last_pose.orientation.y,
                self.last_pose.orientation.z, self.last_pose.orientation.w
            ]
            self.writer.writerow(row)
            self.csvfile.flush()
            self.get_logger().info("Dato registrado en CSV")

    def destroy_node(self):
        self.csvfile.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
