SHELL := /bin/bash
ROS_DISTRO := jazzy

.PHONY: all build test clean launch view firmware-build firmware-upload help

all: build

help:
	@echo "Available commands for Leonardo da Vinci Robot:"
	@echo "  make build           - Build all ROS 2 packages (in software/src) using colcon"
	@echo "  make test            - Run all unit tests with colcon test"
	@echo "  make launch          - Launch full system with bringup.launch.py"
	@echo "  make view            - Visualize robot model and TF in RViz2"
	@echo "  make firmware-build  - Compile ESP32-S3 PlatformIO firmware"
	@echo "  make firmware-upload - Upload firmware to ESP32-S3"
	@echo "  make clean           - Remove build, install, and log directories"

build:
	source /opt/ros/$(ROS_DISTRO)/setup.bash && colcon build --base-paths software/src --symlink-install

test:
	source /opt/ros/$(ROS_DISTRO)/setup.bash && source install/setup.bash && colcon test --base-paths software/src && colcon test-result --verbose

launch:
	source /opt/ros/$(ROS_DISTRO)/setup.bash && source install/setup.bash && ros2 launch leonardo_bringup bringup.launch.py

view:
	source /opt/ros/$(ROS_DISTRO)/setup.bash && source install/setup.bash && ros2 launch leonardo_bringup view_robot.launch.py

firmware-build:
	cd software/firmware && pio run

firmware-upload:
	cd software/firmware && pio run --target upload

clean:
	rm -rf build install log software/firmware/.pio
