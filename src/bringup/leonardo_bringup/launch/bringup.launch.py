import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg_bringup = get_package_share_directory('leonardo_bringup')

    # Path to URDF
    xacro_file = os.path.join(pkg_bringup, 'urdf', 'leonardo.urdf.xacro')
    params_file = os.path.join(pkg_bringup, 'config', 'robot_params.yaml')

    # Launch Configurations
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': Command(['xacro ', xacro_file])
        }]
    )

    # ESP32 Bridge Node
    esp32_bridge_node = Node(
        package='leonardo_bringup',
        executable='esp32_bridge_node',
        name='leonardo_esp32_bridge',
        output='screen',
        parameters=[params_file]
    )

    # Kinematics Node
    kinematics_node = Node(
        package='leonardo_kinematics',
        executable='kinematics_node',
        name='leonardo_kinematics',
        output='screen',
        parameters=[params_file]
    )

    # Controller Node
    controller_node = Node(
        package='leonardo_controller',
        executable='drawing_controller_node',
        name='leonardo_drawing_controller',
        output='screen',
        parameters=[params_file]
    )

    # Safety Node
    safety_node = Node(
        package='leonardo_controller',
        executable='safety_node',
        name='leonardo_safety',
        output='screen',
        parameters=[params_file]
    )

    # Vision Node
    vision_node = Node(
        package='leonardo_vision',
        executable='vision_node',
        name='leonardo_vision',
        output='screen',
        parameters=[params_file]
    )

    # Homography Node
    homography_node = Node(
        package='leonardo_vision',
        executable='homography_node',
        name='leonardo_homography',
        output='screen',
        parameters=[params_file]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use simulation clock'),
        robot_state_publisher_node,
        esp32_bridge_node,
        kinematics_node,
        controller_node,
        safety_node,
        vision_node,
        homography_node,
    ])
