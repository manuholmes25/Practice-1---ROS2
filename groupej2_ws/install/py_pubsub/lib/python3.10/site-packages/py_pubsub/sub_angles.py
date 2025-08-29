import rclpy
from rclpy.node import Node
import numpy as np

from std_msgs.msg import Int8

def rotacion2D(theta_deg, punto):
    """
    Aplica una rotación en 2D a un punto.
    theta_deg: ángulo en grados
    punto: np.array([x, y])
    """
    theta = np.deg2rad(theta_deg)
    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    return R @ punto

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('receiver')
        self.subscription = self.create_subscription(
            Int8,
            'angles',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        angle = np.deg2rad(msg.data)
        m = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)]
        ])
        print(m)

        self.get_logger().info('I heard: "%s"' % msg.data)


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