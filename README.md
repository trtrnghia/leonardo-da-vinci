# Leonardo da Vinci - 3-Wheel Omni AGV Drawing Robot
[![ROS 2 Jazzy CI](https://github.com/trtrnghia/leonardo-da-vinci/actions/workflows/ros2_ci.yml/badge.svg)](https://github.com/trtrnghia/leonardo-da-vinci/actions/workflows/ros2_ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Dự án robot vẽ tranh tự hành 3 bánh omni (120°) chuyên nghiệp trên nền tảng **ROS 2 Jazzy** kết hợp thị giác máy tính OpenCV, biến đổi Homography $H$, ước lượng Odometry từ ESP32-S3, định vị thị giác sâu SuperPoint + LightGlue và cảm biến an toàn LiDAR 2D.

- 📖 **Báo cáo Thiết kế Kỹ thuật Toàn diện**: [docs/2026-11-09-leonardo-da-vinci-robot-design.md](docs/2026-11-09-leonardo-da-vinci-robot-design.md)
- ⚡ **Hướng dẫn Khởi động Nhanh**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- 🔌 **Sơ đồ Đấu dây & Pinout**: [assets/schematics/PINOUT.md](assets/schematics/PINOUT.md)

---

## 🏛 Cấu trúc Thư mục Khoa học & Dễ Truy cập

Dự án được cấu trúc theo mô hình **Domain-Driven Robotics Monorepo**, phân tách rành mạch giữa **Embedded Firmware**, **Tài liệu Kỹ thuật**, **Tập lệnh Tiện ích (Scripts)**, **Dữ liệu Mẫu (Assets)** và các **Tầng ROS 2 Packages**:

```
leonardo-da-vinci/
├── assets/                          # Dữ liệu hình ảnh mẫu, file vector SVG và sơ đồ nguyên lý
│   ├── sample_drawings/             # File vector vẽ thử nghiệm (star.svg, square.svg, ...)
│   └── schematics/                  # Sơ đồ mạch điện & bảng chân đấu nối PINOUT.md
│
├── ci/                              # Tự động hóa CI/CD kiểm thử tự động trên ROS 2 Jazzy Docker
│   └── ros2_ci.yml
│
├── docs/                            # Tài liệu kỹ thuật, báo cáo thiết kế & cẩm nang vận hành
│   ├── 2026-11-09-leonardo-da-vinci-robot-design.md # Báo cáo kỹ thuật chi tiết toàn diện
│   └── QUICKSTART.md                # Hướng dẫn thao tác nhanh cho lập trình viên
│
├── firmware/                        # Toàn bộ mã nguồn nhúng C++ PlatformIO cho ESP32-S3 (Tách riêng khỏi ROS)
│   ├── platformio.ini               # Cấu hình biên dịch & nạp firmware PlatformIO
│   ├── include/
│   │   ├── config.h                 # Cấu hình chân GPIO, hằng số cơ khí & thông số PID
│   │   ├── pid_controller.h         # Thuật toán PID vận tốc kèm cơ chế chống bão hòa (Anti-windup)
│   │   ├── motor_driver.h           # Trình điều khiển PWM/DIR mạch cầu H cho 3 động cơ DC
│   │   ├── encoder_reader.h         # Bộ giải mã xung ngắt Quadrature Encoder 334 CPR
│   │   └── serial_protocol.h        # Bộ phân tích lệnh ASCII & phát Telemetry 50Hz
│   └── src/
│       └── main.cpp                 # Vòng lặp điều khiển thời gian thực (100Hz) & Watchdog Timer 500ms
│
├── scripts/                         # Các tập lệnh shell & python tiện ích cho nhà phát triển
│   ├── setup_env.sh                 # Cấu hình môi trường ROS 2 & nạp biến overlay
│   ├── run_sim.sh                   # Khởi chạy mô hình 3D và RViz2 trực quan
│   └── test_serial.py               # Script chuẩn đoán kết nối Serial phần cứng độc lập
│
├── src/                             # Tầng ROS 2 Packages (Được nhóm theo phân tầng chức năng)
│   ├── interfaces/                  # Tầng Giao diện (Interfaces)
│   │   └── leonardo_msgs/           # Định nghĩa Custom Action, Service & Message
│   │       ├── action/DrawArtwork.action
│   │       ├── srv/SetPen.srv, CalibrateCanvas.srv, EmergencyStop.srv
│   │       └── msg/PenCommand.msg, WheelSpeeds.msg, CanvasPose.msg, DrawStatus.msg, StrokeTrajectory.msg
│   │
│   ├── core/                        # Tầng Xử lý Lõi & Thuật toán Toán học
│   │   ├── leonardo_kinematics/     # Động học Omni 120° & Ước lượng Odometry Dead Reckoning
│   │   │   ├── kinematics.py        # Thư viện toán thuần túy (IK, FK, tích phân Odometry)
│   │   │   ├── kinematics_node.py   # Node ROS 2 chuyển đổi Twist -> WheelSpeeds, phát /odom & TF
│   │   │   └── test/                # Unit test toán học động học với pytest
│   │   └── leonardo_vision/         # Thị giác máy tính & Phép biến đổi Phối cảnh Homography
│   │       ├── contour_extractor.py # Canny edge, nén RDP và tối ưu hóa đường đi của bút (TSP)
│   │       ├── homography_tracker.py# Biến đổi phối cảnh Homography H qua SIFT/ORB + RANSAC
│   │       ├── camera_calibrator.py # Hiệu chuẩn thông số nội tại và khử méo thấu kính (K, D)
│   │       ├── vision_node.py       # Node trích xuất nét vẽ và xử lý ảnh
│   │       ├── homography_node.py   # Node phát tọa độ canvas và broadcast TF canvas -> odom
│   │       └── calibration_node.py  # Node phát thông tin hiệu chuẩn camera
│   │
│   ├── control/                     # Tầng Điều khiển Chấp hành & An toàn
│   │   └── leonardo_controller/     # Máy trạng thái vẽ tranh, Action Server & Giám sát LiDAR
│   │       ├── trajectory_generator.py # Bộ tạo quỹ đạo và nội suy điểm vẽ mịn
│   │       ├── drawing_controller_node.py # Action Server thực thi chuỗi nét vẽ, quản lý Pen UP/DOWN
│   │       └── safety_node.py       # Giám sát LiDAR 2D (/scan), phanh khẩn cấp & nhấc bút khi có vật cản < 0.3m
│   │
│   └── bringup/                     # Tầng Tích hợp Hệ thống & Khởi chạy Toàn diện
│       └── leonardo_bringup/        # URDF xacro, RViz config, launch files, parameter YAML
│           ├── urdf/leonardo.urdf.xacro # Mô hình 3D URDF chuẩn xác (3 bánh omni, cụm bút, LiDAR, camera)
│           ├── rviz/leonardo.rviz   # Cấu hình giao diện RViz2
│           ├── launch/bringup.launch.py # File launch đồng loạt toàn bộ hệ thống
│           ├── launch/view_robot.launch.py # File launch kiểm tra mô hình robot 3D trên RViz2
│           ├── config/robot_params.yaml # Toàn bộ thông số vật lý và cấu hình các node
│           └── esp32_bridge_node.py # Cầu nối USB CDC Serial 115200 bps kết nối ESP32-S3
│
├── Makefile                         # Tập lệnh quản lý thao tác nhanh cho toàn bộ vòng đời dự án
├── README.md                        # Hướng dẫn tổng quan
└── .gitignore                       # Danh sách loại trừ tệp biên dịch và tạm
```

---

## 🚀 Thao tác Nhanh (Cheat Sheet)

Dự án cung cấp tập lệnh `Makefile` giúp bạn thực hiện mọi thao tác phát triển chỉ với 1 dòng lệnh:

| Lệnh thao tác | Chức năng thực hiện |
| :--- | :--- |
| `make build` | Biên dịch toàn bộ các gói ROS 2 với `colcon build --symlink-install` |
| `make test` | Chạy toàn bộ unit test (kinematics math, linter) |
| `make view` | Mở mô hình robot 3D trực quan trên RViz2 |
| `make launch` | Khởi động toàn bộ phần mềm robot (bringup stack) |
| `make firmware-build` | Biên dịch firmware ESP32-S3 PlatformIO |
| `make firmware-upload` | Nạp firmware qua cổng USB xuống ESP32-S3 |
| `make clean` | Xóa sạch các thư mục build cache (`build/`, `install/`, `log/`) |
