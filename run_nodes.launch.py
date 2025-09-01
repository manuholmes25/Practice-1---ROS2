from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([            
        Node(
            package='py_pubsub1',
            namespace='py_pubsub1',
            executable='pub',
        ),
        Node(
            package='py_pubsub1',
            namespace='py_pubsub1',
            executable='planner',
        ),
        Node(
            package='py_pubsub1',
            namespace='py_pubsub1',
            executable='filter',
        ),
        Node(
            package='py_pubsub1',
            namespace='py_pubsub1',
            executable='logger',
        ),
        Node(
            package='py_pubsub1',
            namespace='py_pubsub1',
            executable='controller',
        )
    ])