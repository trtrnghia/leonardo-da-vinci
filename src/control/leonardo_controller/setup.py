from setuptools import find_packages, setup

package_name = 'leonardo_controller'

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
    maintainer='davinci',
    maintainer_email='davinci@todo.todo',
    description='Drawing state machine, trajectory follower, and LiDAR safety monitor',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'drawing_controller_node = leonardo_controller.drawing_controller_node:main',
            'safety_node = leonardo_controller.safety_node:main',
        ],
    },
)
