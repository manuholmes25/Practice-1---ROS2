import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'py_pubsub1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='manuel',
    maintainer_email='manuel@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pub = py_pubsub1.pub:main',
            'planner = py_pubsub1.planner:main',
            'logger = py_pubsub1.logger:main',
            'filter = py_pubsub1.filter:main',
            'controller = py_pubsub1.controller:main'
        ],
    },
)
