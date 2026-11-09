# Leonardo da Vinci - 3-Wheel Omni AGV Drawing Robot
[![ROS 2 Jazzy CI](https://github.com/trtrnghia/leonardo-da-vinci/actions/workflows/ros2_ci.yml/badge.svg)](https://github.com/trtrnghia/leonardo-da-vinci/actions/workflows/ros2_ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Dự án robot vẽ tranh tự hành 3 bánh omni (120°) chuyên nghiệp trên nền tảng **ROS 2 Jazzy** kết hợp thị giác máy tính OpenCV, biến đổi Homography $H$, ước lượng Odometry từ ESP32-S3, định vị thị giác sâu SuperPoint + LightGlue và cảm biến an toàn LiDAR 2D.

Tài liệu thiết kế kỹ thuật chi tiết: [docs/2026-11-09-leonardo-da-vinci-robot-design.md](docs/2026-11-09-leonardo-da-vinci-robot-design.md)

---

## 🏛 Kiến trúc Hệ thống & Cấu trúc Workspace

```
.
├── .github/workflows/
│   └── ros2_ci.yml             # Tự động hóa CI/CD build & test trên nền container ROS 2 Jazzy
├── .vscode/                     # Thiết lập IDE VS Code (include paths, settings, tasks)
├── docs/                        # Báo cáo kỹ thuật và hồ sơ thiết kế hệ thống
├── Makefile                     # Tập lệnh quản lý thao tác nhanh (build, test, launch, view, firmware)
└── src/
    ├── leonardo_msgs/           # Custom Interfaces (Messages, Services, Actions)
    │   ├── action/DrawArtwork.action
    │   ├── srv/SetPen.srv, CalibrateCanvas.srv, EmergencyStop.srv
    │   └── msg/PenCommand.msg, WheelSpeeds.msg, CanvasPose.msg, DrawStatus.msg, StrokeTrajectory.msg
    │
    ├── leonardo_kinematics/     # Động học Omni 120° & Ước lượng Odometry
    │   ├── kinematics.py        # Thư viện toán học thuần túy (IK, FK, tích phân Odometry)
    │   ├── kinematics_node.py   # Node ROS 2 chuyển đổi Twist -> WheelSpeeds, phát /odom & TF
    │   └── test/                # Unit test toán học động học với pytest
    │
    ├── leonardo_vision/         # Thị giác máy tính & Định vị Canvas
    │   ├── contour_extractor.py # Canny edge, Ramer-Douglas-Peucker (RDP), tối ưu hóa hành trình bút
    │   ├── homography_tracker.py# Biến đổi phối cảnh Homography H qua SIFT/ORB + RANSAC
    │   ├── camera_calibrator.py # Hiệu chuẩn thông số nội tại và khử méo thấu kính (K, D)
    │   ├── vision_node.py       # Node trích xuất nét vẽ và xử lý ảnh
    │   ├── homography_node.py   # Node phát tọa độ canvas và broadcast TF canvas -> odom
    │   └── calibration_node.py  # Node phát thông tin hiệu chuẩn camera
    │
    ├── leonardo_controller/     # Điều khiển Quỹ đạo & An toàn Chống va chạm
    │   ├── trajectory_generator.py # Nội suy không gian và profile vận tốc
    │   ├── drawing_controller_node.py # Action Server thực thi chuỗi nét vẽ, quản lý Pen UP/DOWN
    │   └── safety_node.py       # Giám sát LiDAR 2D (/scan), dừng khẩn cấp và nhấc bút khi có vật cản < 0.3m
    │
    ├── leonardo_bringup/        # Cấu hình Khởi chạy & Mô hình Robot
    │   ├── urdf/leonardo.urdf.xacro # Mô hình 3D URDF chuẩn xác (3 bánh omni, cụm bút, LiDAR, camera)
    │   ├── rviz/leonardo.rviz   # Cấu hình hiển thị trực quan RViz2
    │   ├── launch/bringup.launch.py # File launch đồng loạt toàn bộ hệ thống
    │   ├── launch/view_robot.launch.py # File launch kiểm tra mô hình robot 3D trên RViz2
    │   ├── config/robot_params.yaml # Toàn bộ thông số vật lý và cấu hình các node
    │   └── esp32_bridge_node.py # Cầu nối USB CDC Serial 115200 bps kết nối ESP32-S3
    │
    └── leonardo_firmware/       # Mã nguồn C++ PlatformIO nhúng cho ESP32-S3
        ├── platformio.ini       # File cấu hình PlatformIO cho ESP32-S3 DevKit
        ├── include/config.h     # Sơ đồ chân GPIO (3x Motor PWM/DIR, 3x Encoders, 1x Servo)
        ├── include/pid_controller.h # Thuật toán PID vận tốc với cơ chế chống bão hòa tích phân (Anti-windup)
        ├── include/motor_driver.h   # Driver cầu H điều khiển PWM động cơ
        ├── include/encoder_reader.h # Bộ giải mã xung Encoder hai kênh vuông pha (Quadrature)
        ├── include/serial_protocol.h# Parser tập lệnh ASCII và bộ phát định dạng telemetry 50Hz
        └── src/main.cpp         # Vòng lặp điều khiển thời gian thực và Watchdog bảo vệ 500ms
```

---

## 🚀 Hướng dẫn Cài đặt & Vận hành

### 1. Biên dịch Workspace
```bash
make build
# Hoặc:
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
```

### 2. Chạy Kiểm thử Đơn vị (Unit Tests)
```bash
make test
```

### 3. Xem Mô hình 3D Robot trên RViz2
```bash
make view
```

### 4. Khởi động Toàn bộ Hệ thống Robot
```bash
make launch
```

### 5. Biên dịch & Nạp Firmware cho ESP32-S3
```bash
# Biên dịch firmware
make firmware-build

# Nạp trực tiếp qua cổng USB
make firmware-upload
```
