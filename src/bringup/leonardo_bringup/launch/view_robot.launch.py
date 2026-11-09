"""Launch description for visualizing Leonardo robot in RViz2."""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import Command

from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description for RViz2 robot visualization."""
    pkg_bringup = get_package_share_directory('leonardo_bringup')
    xacro_file = os.path.join(pkg_bringup, 'urdf', 'leonardo.urdf.xacro')
    rviz_config = os.path.join(pkg_bringup, 'rviz', 'leonardo.rviz')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command(['xacro ', xacro_file])
        }]
    )

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz_node
    ])
