from setuptools import find_packages, setup

package_name = 'py_pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='eduardex',
    maintainer_email='HBKEduardex@users.noreply.github.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sender = py_pubsub.pub_angles:main',
            'receiver = py_pubsub.sub_angles:main',
            'server = py_pubsub.server_angles:main',
            'client = py_pubsub.client_angles:main',
            
        ],
    },
)
