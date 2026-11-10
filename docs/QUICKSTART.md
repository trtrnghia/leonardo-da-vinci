# Hướng Dẫn Khởi Động Nhanh (Quickstart Guide)

Tài liệu này giúp các kỹ sư và lập trình viên nhanh chóng tiếp cận, biên dịch, kiểm thử mô hình và vận hành hệ thống robot **Leonardo da Vinci**.

---

## 1. Yêu Cầu Môi Trường (Prerequisites)
- Hệ điều hành: **Ubuntu 24.04 LTS (x86_64 hoặc aarch64)**
- Nền tảng ROS: **ROS 2 Jazzy Jalisco (Base hoặc Desktop)**
- Công cụ phát triển: `colcon`, `git`, `python3-pip`, `python3-pytest`, `PlatformIO CLI`

---

## 2. Cấu Trúc Dự Án (2 Phần Chính)

Repository được tổ chức thành 2 phần chuyên biệt:
1. **`software/`**: Toàn bộ mã nguồn phần mềm ROS 2 (`software/src`), firmware nhúng ESP32-S3 (`software/firmware`), kịch bản tiện ích (`software/scripts`) và dữ liệu vẽ mẫu (`software/assets`).
2. **`machine_design_and_modeling/`**: Thiết kế cơ khí CAD & thông số kỹ thuật (`cad/`), mô hình 3D URDF/Xacro (`urdf/`), cơ sở toán học động học & động lực học (`kinematics_and_dynamics/`), sơ đồ điện & đấu dây (`electrical_and_wiring/`) và tài liệu thiết kế (`docs/`).

---

## 3. Các Bước Vận Hành Cơ Bản

### Bước 1: Thiết lập môi trường ROS 2
```bash
source scripts/setup_env.sh
# hoặc:
source software/scripts/setup_env.sh
```

### Bước 2: Biên dịch các gói phần mềm ROS 2
```bash
make build
# Lệnh tương đương:
colcon build --base-paths software/src --symlink-install
```

### Bước 3: Chạy kiểm thử tự động (Unit Tests)
```bash
make test
# hoặc kiểm tra nhanh mô hình động học:
PYTHONPATH=software/src/core/leonardo_kinematics pytest software/src/core/leonardo_kinematics/test/test_kinematics_math.py
```

### Bước 4: Kiểm tra trực quan Mô hình Robot 3D trên RViz2
```bash
make view
# Lệnh tương đương:
ros2 launch leonardo_bringup view_robot.launch.py
```

### Bước 5: Biên dịch & Nạp Firmware cho ESP32-S3
Kết nối bo mạch ESP32-S3 qua cổng USB Type-C:
```bash
make firmware-build
make firmware-upload
```

### Bước 6: Kiểm tra giao tiếp Serial phần cứng độc lập
```bash
python3 scripts/test_serial.py /dev/ttyACM0
```

### Bước 7: Khởi chạy toàn bộ hệ thống Robot
```bash
make launch
# Lệnh tương đương:
ros2 launch leonardo_bringup bringup.launch.py
```
