# Software Architecture - Leonardo da Vinci Robot

Thư mục này chứa toàn bộ ngăn xếp phần mềm (Software Stack) của Robot vẽ tranh tự hành 3 bánh Omni **Leonardo da Vinci**, bao gồm các gói ROS 2 Jazzy trên Raspberry Pi 4B và firmware nhúng C++ thời gian thực trên vi điều khiển ESP32-S3.

---

## 🏛 Cấu Trúc Thư Mục Phần Mềm

```
software/
├── README.md                            # Tổng quan ngăn xếp phần mềm
│
├── src/                                 # Không gian làm việc ROS 2 (ROS 2 Workspace Packages)
│   ├── interfaces/                      # Tầng định nghĩa giao diện (Action, Service, Message)
│   │   └── leonardo_msgs/               # Giao diện thông điệp tuỳ biến
│   │       ├── action/DrawArtwork.action
│   │       ├── srv/SetPen.srv, CalibrateCanvas.srv, EmergencyStop.srv
│   │       └── msg/PenCommand.msg, WheelSpeeds.msg, CanvasPose.msg, DrawStatus.msg, StrokeTrajectory.msg
│   │
│   ├── core/                            # Tầng tính toán lõi và thuật toán
│   │   ├── leonardo_kinematics/         # Động học ngược/thuận Omni 120° & Dead Reckoning Odometry
│   │   │   ├── kinematics.py            # Giải thuật toán học thuần tuý (IK, FK, Dead Reckoning)
│   │   │   ├── kinematics_node.py       # Node ROS 2 xử lý /cmd_vel <-> /wheel_cmd, phát /odom & TF
│   │   │   └── test/                    # Unit test động học với pytest
│   │   └── leonardo_vision/             # Xử lý ảnh & Biến đổi phối cảnh Homography
│   │       ├── contour_extractor.py     # Canny Edge, nén RDP và tối ưu đường chạy bút TSP
│   │       ├── homography_tracker.py    # Ước lượng ma trận H qua SIFT/ORB + RANSAC
│   │       ├── camera_calibrator.py     # Khử méo thấu kính K, D
│   │       ├── vision_node.py           # Node trích xuất nét vẽ và xử lý ảnh
│   │       ├── homography_node.py       # Node phát /canvas_pose và broadcast TF canvas -> odom
│   │       └── calibration_node.py      # Node phát thông tin hiệu chuẩn camera
│   │
│   ├── control/                         # Tầng điều khiển chấp hành & an toàn
│   │   └── leonardo_controller/         # Máy trạng thái vẽ tranh & giám sát LiDAR
│   │       ├── drawing_controller_node.py # Action Server thực thi từng nét vẽ, quản lý Pen UP/DOWN
│   │       ├── trajectory_generator.py  # Bộ tạo quỹ đạo và nội suy điểm vẽ mịn
│   │       └── safety_node.py           # Giám sát LiDAR 2D (/scan), dừng khẩn cấp khi vật cản < 0.3m
│   │
│   └── bringup/                         # Tầng tích hợp và khởi chạy toàn hệ thống
│       └── leonardo_bringup/            # Launch files, cấu hình RViz2, file tham số YAML
│           ├── launch/bringup.launch.py # Khởi động đồng loạt toàn bộ các node ROS 2
│           ├── launch/view_robot.launch.py # Khởi chạy mô hình 3D trên RViz2
│           ├── config/robot_params.yaml # Toàn bộ thông số vật lý và cấu hình các node
│           ├── rviz/leonardo.rviz       # Cấu hình giao diện quan sát RViz2
│           ├── urdf/leonardo.urdf.xacro # Mô hình 3D robot tích hợp cho ROS 2
│           └── esp32_bridge_node.py     # Cầu nối USB Serial 115200 bps kết nối ESP32-S3
│
├── firmware/                            # Mã nguồn nhúng C++ PlatformIO cho ESP32-S3
│   ├── platformio.ini                   # Cấu hình biên dịch và nạp PlatformIO
│   ├── include/
│   │   ├── config.h                     # Cấu hình chân GPIO, hằng số cơ khí & thông số PID
│   │   ├── pid_controller.h             # Thuật toán PID vận tốc kèm Anti-windup
│   │   ├── motor_driver.h               # Trình điều khiển PWM/DIR mạch cầu H cho 3 động cơ
│   │   ├── encoder_reader.h             # Bộ giải mã ngắt Quadrature Encoder 334 CPR
│   │   └── serial_protocol.h            # Bộ phân tích lệnh ASCII & phát Telemetry 50Hz
│   └── src/
│       └── main.cpp                     # Vòng lặp điều khiển thời gian thực (100Hz) & Watchdog Timer
│
├── scripts/                             # Tập lệnh shell & python tiện ích
│   ├── setup_env.sh                     # Cấu hình môi trường ROS 2 & nạp overlay
│   ├── run_sim.sh                       # Khởi chạy mô hình 3D và RViz2 trực quan
│   └── test_serial.py                   # Script chẩn đoán kết nối Serial phần cứng độc lập
│
└── assets/                              # Dữ liệu hình ảnh mẫu và file vẽ vector
    └── sample_drawings/                 # File vector SVG mẫu (star.svg, square.svg)
```

---

## 🚀 Hướng Dẫn Thao Tác Nhanh

### 1. Thiết lập Môi trường ROS 2
```bash
source software/scripts/setup_env.sh
```

### 2. Biên dịch Các Gói ROS 2
Tại thư mục gốc của repository:
```bash
make build
# hoặc trực tiếp:
colcon build --base-paths software/src --symlink-install
```

### 3. Chạy Kiểm Thử Tự Động (Unit Tests)
```bash
make test
# hoặc kiểm tra nhanh kinematics math bằng pytest:
PYTHONPATH=software/src/core/leonardo_kinematics pytest software/src/core/leonardo_kinematics/test/test_kinematics_math.py
```

### 4. Khởi Chạy Toàn Bộ Hệ Thống
```bash
make launch
# hoặc:
ros2 launch leonardo_bringup bringup.launch.py
```

### 5. Biên dịch & Nạp Firmware ESP32-S3
```bash
make firmware-build
make firmware-upload
```
