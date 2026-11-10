#!/usr/bin/env bash
# Launch script for 3D visualization and simulation in RViz2

# Locate workspace root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT" || exit 1

if [ -f "/opt/ros/jazzy/setup.bash" ]; then
    source /opt/ros/jazzy/setup.bash
fi

if [ -f "install/setup.bash" ]; then
    source install/setup.bash
else
    echo "Running build first..."
    colcon build --base-paths software/src --symlink-install
    source install/setup.bash
fi

echo "Launching Leonardo Robot Model and RViz2..."
ros2 launch leonardo_bringup view_robot.launch.py
