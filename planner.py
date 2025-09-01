import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import math
import numpy as np  
from sensor_msgs.msg import LaserScan

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('planner_node')
        self.min_distance = 0.6  # umbral de “cerca” en metros
        self.subscription = self.create_subscription(PoseStamped,'/pose', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10) 
        self.get_logger().info('usando /pose -> /cmd_vel | min_distance={min_distance}')

    def listener_callback(self, msg:PoseStamped):

        x=msg.pose.position.x
        y=msg.pose.position.y

        d = math.hypot(x, y)

        cmd = Twist()
        if d <= self.min_distance:
            cmd.linear.x = 0.0   # no avanza
            cmd.angular.z = 0.5  # gira para evadir
            estado = "EVADIR"
        else:
            cmd.linear.x = 0.5   # avanza
            cmd.angular.z = 0.0  # no gira
            estado = "AVANZAR"

        self.publisher_.publish(cmd)
        self.get_logger().info(
            f'[planner_node] d={d:.2f} m <=({self.min_distance:.2f}) -> {estado} | '
            f'cmd: lin.x={cmd.linear.x:.2f}, ang.z={cmd.angular.z:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()