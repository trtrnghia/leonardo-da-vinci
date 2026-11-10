#!/usr/bin/env bash
# Environment setup script for Leonardo da Vinci Robot Workspace

echo "Setting up ROS 2 Jazzy environment..."
if [ -f "/opt/ros/jazzy/setup.bash" ]; then
    source /opt/ros/jazzy/setup.bash
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -f "$REPO_ROOT/install/setup.bash" ]; then
    echo "Sourcing workspace overlay from $REPO_ROOT/install/setup.bash..."
    source "$REPO_ROOT/install/setup.bash"
else
    echo "Workspace not built yet. Run 'make build' from repository root."
fi

export ROS_DOMAIN_ID=42
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
echo "Environment configured: ROS_DOMAIN_ID=$ROS_DOMAIN_ID, RMW=$RMW_IMPLEMENTATION"
