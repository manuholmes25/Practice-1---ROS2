import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
import math

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.subscription = self.create_subscription(Twist,'/cmd_vel',self.cmd_vel_callback,10)
        self.publisher = self.create_publisher(PoseStamped, '/pose', 10)

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.v = 0.0
        self.w = 0.0
        self.dt = 0.05
        self.timer = self.create_timer(self.dt, self.update_pose)

        self.get_logger().info("Escucha /cmd_vel y publica /pose")

    def cmd_vel_callback(self, msg: Twist):
        self.v = msg.linear.x
        self.w = msg.angular.z
        self.get_logger().info(f"Recibido /cmd_vel: v={self.v:.2f}, w={self.w:.2f}")

    def update_pose(self):
        self.x += self.v * math.cos(self.theta) * self.dt
        self.y += self.v * math.sin(self.theta) * self.dt
        self.theta += self.w * self.dt
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = self.x
        msg.pose.position.y = self.y

        qz = math.sin(self.theta / 2.0)
        qw = math.cos(self.theta / 2.0)
        msg.pose.orientation.z = qz
        msg.pose.orientation.w = qw

        self.publisher.publish(msg)
        self.get_logger().info(f"Pose controlada: x={self.x:.2f}, y={self.y:.2f}, θ={math.degrees(self.theta):.1f}°")

def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
