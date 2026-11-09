#!/usr/bin/env bash
# Launch script for 3D visualization and simulation in RViz2

source /opt/ros/jazzy/setup.bash
if [ -f "install/setup.bash" ]; then
    source install/setup.bash
else
    echo "Running build first..."
    colcon build --symlink-install
    source install/setup.bash
fi

echo "Launching Leonardo Robot Model and RViz2..."
ros2 launch leonardo_bringup view_robot.launch.py
