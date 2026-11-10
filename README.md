# Leonardo da Vinci - 3-Wheel Omni AGV Drawing Robot
[![ROS 2 Jazzy CI](https://github.com/trtrnghia/leonardo-da-vinci/actions/workflows/ros2_ci.yml/badge.svg)](https://github.com/trtrnghia/leonardo-da-vinci/actions/workflows/ros2_ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Dự án robot vẽ tranh tự hành 3 bánh omni (120°) chuyên nghiệp trên nền tảng **ROS 2 Jazzy** kết hợp thị giác máy tính OpenCV, biến đổi Homography $H$, ước lượng Odometry từ ESP32-S3, định vị thị giác sâu SuperPoint + LightGlue và cảm biến an toàn LiDAR 2D.

- 📖 **Báo cáo Thiết kế Kỹ thuật Toàn diện**: [machine_design_and_modeling/docs/2026-11-09-leonardo-da-vinci-robot-design.md](machine_design_and_modeling/docs/2026-11-09-leonardo-da-vinci-robot-design.md)
- ⚡ **Hướng dẫn Khởi động Nhanh**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- 🔌 **Sơ đồ Đấu dây & Pinout**: [machine_design_and_modeling/electrical_and_wiring/PINOUT.md](machine_design_and_modeling/electrical_and_wiring/PINOUT.md)
- 📐 **Mô hình Hóa 3D & Động học**: [machine_design_and_modeling/README.md](machine_design_and_modeling/README.md)
- 💻 **Ngăn xếp Phần mềm (Software Stack)**: [software/README.md](software/README.md)

---

## 🏛 Cấu Trúc Dự Án (2 Phần Chuyên Biệt)

Dự án được phân tách rành mạch thành 2 phần độc lập theo chuẩn công nghệ: **Software** và **Machine Design and Modeling**:

```
leonardo-da-vinci/
├── Makefile                                 # Tập lệnh quản lý thao tác nhanh toàn dự án
├── README.md                                # Tài liệu tổng quan dự án
├── .gitignore                               # Quy tắc loại trừ tệp biên dịch và tạm
│
├── ci/                                      # CI/CD tự động hóa kiểm thử
│   └── ros2_ci.yml
│
├── docs/                                    # Cẩm nang vận hành chung
│   └── QUICKSTART.md                        # Hướng dẫn thao tác nhanh cho lập trình viên & kỹ sư
│
├── scripts/                                 # Tập lệnh điều phối gốc (Forwarding wrappers)
│   ├── setup_env.sh                         # Thiết lập môi trường ROS 2 Jazzy
│   ├── run_sim.sh                           # Khởi chạy mô hình RViz2
│   └── test_serial.py                       # Kiểm tra kết nối Serial độc lập
│
├── software/                                # [PHẦN 1] TOÀN BỘ NGĂN XẾP PHẦN MỀM (SOFTWARE)
│   ├── README.md                            # Tổng quan kiến trúc phần mềm
│   ├── firmware/                            # Mã nguồn nhúng C++ PlatformIO cho ESP32-S3 (PID, Encoder, Servo)
│   │   ├── platformio.ini                   # Cấu hình biên dịch PlatformIO
│   │   ├── include/                         # Header files (PID, Motor, Encoder, Protocol, Config)
│   │   └── src/main.cpp                     # Vòng lặp điều khiển thời gian thực (100Hz) & Watchdog
│   ├── scripts/                             # Tập lệnh tiện ích nội bộ của software
│   ├── assets/                              # Dữ liệu phục vụ phần mềm
│   │   └── sample_drawings/                 # File vector SVG mẫu (star.svg, square.svg)
│   └── src/                                 # Không gian làm việc ROS 2 (ROS 2 Jazzy Workspace)
│       ├── interfaces/                      # Tầng định nghĩa giao diện (leonardo_msgs)
│       ├── core/                            # Tầng xử lý thuật toán (leonardo_kinematics, leonardo_vision)
│       ├── control/                         # Tầng điều khiển & an toàn (leonardo_controller)
│       └── bringup/                         # Tầng tích hợp khởi chạy (leonardo_bringup)
│
└── machine_design_and_modeling/             # [PHẦN 2] THIẾT KẾ CƠ KHÍ & MÔ HÌNH HÓA (MACHINE DESIGN & MODELING)
    ├── README.md                            # Tổng quan cơ khí, mô hình hóa & điện tử
    ├── cad/                                 # Thiết kế cơ khí & Thông số vật lý
    │   ├── SPECIFICATIONS.md                # Kích thước khung gầm, tải trọng, vật liệu, cơ cấu bút
    │   ├── BOM.md                           # Bảng kê vật tư & linh kiện chi tiết (Bill of Materials)
    │   └── models/README.md                 # Hướng dẫn định dạng file CAD 3D (STEP, STL, DXF)
    ├── urdf/                                # Mô hình hóa động học 3D URDF / Xacro
    │   ├── leonardo.urdf.xacro              # Định nghĩa cây khớp, liên kết, quán tính và va chạm
    │   └── README.md                        # Cấu trúc TF và kiểm tra mô hình
    ├── kinematics_and_dynamics/             # Cơ sở toán học Động học & Động lực học
    │   └── KINEMATICS_AND_DYNAMICS.md       # Ma trận IK/FK Omni 120°, Dead Reckoning, Homography H
    ├── electrical_and_wiring/               # Sơ đồ mạch điện & Đấu nối phần cứng
    │   ├── PINOUT.md                        # Bảng phân bổ chân GPIO ESP32-S3 & Raspberry Pi 4
    │   └── POWER_AND_WIRING.md              # Sơ đồ khối cấp nguồn LiPo, mạch Buck kép & E-Stop
    └── docs/                                # Báo cáo thiết kế kỹ thuật toàn diện
        └── 2026-11-09-leonardo-da-vinci-robot-design.md
```

---

## 🚀 Thao Tác Nhanh (Cheat Sheet)

Dự án cung cấp tập lệnh `Makefile` tại thư mục gốc giúp bạn thực hiện mọi thao tác phát triển chỉ với 1 dòng lệnh:

| Lệnh thao tác | Chức năng thực hiện |
| :--- | :--- |
| `make build` | Biên dịch toàn bộ các gói ROS 2 trong `software/src` với `colcon build --symlink-install` |
| `make test` | Chạy toàn bộ unit test (kinematics math, linter) |
| `make view` | Mở mô hình robot 3D trực quan trên RViz2 |
| `make launch` | Khởi động toàn bộ phần mềm robot (bringup stack) |
| `make firmware-build` | Biên dịch firmware ESP32-S3 PlatformIO |
| `make firmware-upload` | Nạp firmware qua cổng USB xuống ESP32-S3 |
| `make clean` | Xóa sạch các thư mục build cache (`build/`, `install/`, `log/`, `.pio/`) |

---

## 📌 Phân Định Rõ Ràng Giữa 2 Phần

### 1. Phần Software (`software/`)
- Quản lý toàn bộ mã nguồn có thể thực thi (Executable Source Code): ROS 2 Jazzy C++/Python nodes, Custom Interfaces (Actions, Services, Messages), và ESP32-S3 Embedded Firmware (C++ PlatformIO).
- Xử lý các thuật toán điều khiển, xử lý ảnh thị giác máy tính OpenCV, biến đổi Homography, nén vector RDP, quỹ đạo nội suy điểm vẽ, máy trạng thái State Machine và cơ chế an toàn LiDAR.

### 2. Phần Machine Design and Modeling (`machine_design_and_modeling/`)
- Quản lý toàn bộ thiết kế phần cứng, cơ sở toán học và mô hình hóa hình học:
  - **Cơ khí & Kích thước**: Khung gầm $\varnothing 300\text{ mm}$, phân bố 3 bánh Omni 120°, cơ cấu trượt nâng/hạ ngòi bút tích hợp lò xo chống sốc, bảng BOM chi tiết.
  - **Mô hình hóa 3D**: File URDF/Xacro hoàn chỉnh định nghĩa đầy đủ quán tính, khối lượng, liên kết và khớp nối cho RViz2 và Gazebo.
  - **Toán học Động học & Động lực học**: Hệ phương trình động học thuận/nghịch, ma trận Jacobian, ước lượng Odometry từ Encoder, mô hình biến đổi phối cảnh Homography $H$, và cây biến đổi tọa độ TF.
  - **Điện tử & Đấu dây**: Sơ đồ cấp nguồn pin LiPo 3S, mạch hạ áp kép 5V chống sụt áp, bảng chân đấu nối GPIO và nút dừng khẩn cấp E-Stop.
