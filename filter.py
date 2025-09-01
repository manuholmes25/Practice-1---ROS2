import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from collections import deque

class MinimalSubscriber(Node):

    def _init_(self):
        super()._init_('subscriber')
        self.subscription = self.create_subscription(PoseStamped,'/pose',self.listener_callback,10)
        self.publisher_ = self.create_publisher(PoseStamped, '/pose', 10)
        self.window_size = 5
        self.data_window_x = deque(maxlen=self.window_size)
        self.data_window_y = deque(maxlen=self.window_size)

    def filter(self,dato,window):
        window.append(dato)
        return sum(window) / len(window)

    def listener_callback(self, msg):
        x_fil=self.filter(msg.pose.position.x, self.data_window_x)
        y_fil=self.filter(msg.pose.position.y, self.data_window_y)
        msg_env = PoseStamped()
        msg_env.header.stamp = self.get_clock().now().to_msg()
        msg_env.header.frame_id = msg.header.frame_id
        msg_env.pose.position.x = x_fil
        msg_env.pose.position.y = y_fil 

        self.get_logger().info(f'Recibido: x={msg.pose.position.x:.2f}, y={msg.pose.position.y:.2f} , Filtrado: x={x_fil:.2f}, y={y_fil:.2f}')
        self.publisher_.publish(msg_env)

def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
