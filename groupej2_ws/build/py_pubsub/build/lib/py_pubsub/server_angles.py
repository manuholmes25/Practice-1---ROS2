from ucb_interfaces.srv import Rot                                                           # CHANGE

import rclpy
from rclpy.node import Node
import numpy as np

class MinimalService(Node):

    def __init__(self):
        super().__init__('server')
        self.srv = self.create_service(Rot, 'transform', self.transform_angles)       # CHANGE

    def transform_angles(self, request, response):
        ang = request.angle 
        ang2 = request.angle2
        ang3 = request.angle3
        p_i=np.array([[request.px],[request.py],[request.pz],[1]])
        angle = np.deg2rad(ang)
        angle2 = np.deg2rad(ang2)
        angle3 = np.deg2rad(ang3)
        rX= np.array([
        [1, 0,            0,           0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle),  np.cos(angle), 0],
        [0, 0,            0,           1]
        ])
        rY= np.array([
        [ np.cos(angle2), 0, np.sin(angle2), 0],
        [ 0,           1, 0,           0],
        [-np.sin(angle2), 0, np.cos(angle2), 0],
        [ 0,           0, 0,           1]
        ])
        rY2 = np.array([
        [ np.cos(angle3), 0, np.sin(angle3), 0],
        [ 0,           1, 0,           0],
        [-np.sin(angle3), 0, np.cos(angle3), 0],
        [ 0,           0, 0,           1]
        ])
        Iden1 = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, -69.5],
        [0, 0, 0, 1]
        ])
        Iden2 = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, -71.5],
        [0, 0, 0, 1]
        ])
        M = rX @ rY @ Iden1 @ rY2 @ Iden2
        print("Puntos finales:")
        print(M[0, -1])   
        print(M[1, -1])   
        print(M[2, -1])  
        print("Matriz de transformacion:")
        print(M)
        response.fx = float(M[0, -1])
        response.fy = float(M[1, -1])
        response.fz = float(M[2, -1])

        return response

def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()

if __name__ == '__main__':
    main()