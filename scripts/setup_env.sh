#!/usr/bin/env bash
# Environment setup script for Leonardo da Vinci Robot Workspace

echo "Setting up ROS 2 Jazzy environment..."
source /opt/ros/jazzy/setup.bash

if [ -f "install/setup.bash" ]; then
    echo "Sourcing workspace overlay..."
    source install/setup.bash
else
    echo "Workspace not built yet. Run 'make build' first."
fi

export ROS_DOMAIN_ID=42
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
echo "Environment configured: ROS_DOMAIN_ID=$ROS_DOMAIN_ID, RMW=$RMW_IMPLEMENTATION"
