# Hướng Dẫn Khởi Động Nhanh (Quickstart Guide)

Tài liệu này giúp lập trình viên nhanh chóng tiếp cận, biên dịch, kiểm thử và vận hành hệ thống robot Leonardo da Vinci.

---

## 1. Yêu cầu Môi trường (Prerequisites)
- Hệ điều hành: **Ubuntu 24.04 LTS (x86_64 hoặc aarch64)**
- Nền tảng ROS: **ROS 2 Jazzy Jalisco (Base hoặc Desktop)**
- Công cụ phát triển: `colcon`, `git`, `python3-pip`, `python3-pytest`, `PlatformIO CLI`

---

## 2. Các Bước Thao tác Cơ bản

### Bước 1: Thiết lập môi trường
```bash
source scripts/setup_env.sh
```

### Bước 2: Biên dịch toàn bộ các gói ROS 2
```bash
make build
```

### Bước 3: Chạy kiểm thử tự động (Unit Tests)
```bash
make test
```

### Bước 4: Kiểm tra trực quan Robot 3D trên RViz2
```bash
make view
```

### Bước 5: Nạp Firmware cho ESP32-S3
Kết nối bo mạch ESP32-S3 qua cổng USB Type-C:
```bash
make firmware-upload
```

### Bước 6: Kiểm tra giao tiếp Serial độc lập
```bash
python3 scripts/test_serial.py /dev/ttyACM0
```

### Bước 7: Khởi chạy toàn bộ hệ thống Robot
```bash
make launch
```
