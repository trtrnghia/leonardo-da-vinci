# Sơ Đồ Đấu Dây Phần Cứng (Hardware Wiring & Pinout)

## 1. Kết nối Vi điều khiển ESP32-S3 DevKitC-1

| Thiết bị Ngoại vi | Chân ESP32-S3 | Chức năng Kỹ thuật | Ghi chú |
| :--- | :--- | :--- | :--- |
| **Servo Nâng Bút** | `GPIO 4` | PWM Tín hiệu Điều khiển góc | Nguồn 5V từ mạch hạ áp riêng |
| **Động cơ 1 (Wheel 1 - 0°)** | `GPIO 5` | PWM Tốc độ | Kênh Timer LEDC 0 |
| | `GPIO 6` | DIR Chiều quay | LOW: Tiến, HIGH: Lùi |
| | `GPIO 11` | Encoder Kênh A (Interrupt) | Ngắt sườn `CHANGE` |
| | `GPIO 12` | Encoder Kênh B | Đọc chiều quay quadrature |
| **Động cơ 2 (Wheel 2 - 120°)**| `GPIO 7` | PWM Tốc độ | Kênh Timer LEDC 1 |
| | `GPIO 8` | DIR Chiều quay | |
| | `GPIO 13` | Encoder Kênh A (Interrupt) | Ngắt sườn `CHANGE` |
| | `GPIO 14` | Encoder Kênh B | |
| **Động cơ 3 (Wheel 3 - 240°)**| `GPIO 9` | PWM Tốc độ | Kênh Timer LEDC 2 |
| | `GPIO 10` | DIR Chiều quay | |
| | `GPIO 15` | Encoder Kênh A (Interrupt) | Ngắt sườn `CHANGE` |
| | `GPIO 16` | Encoder Kênh B | |

---

## 2. Kết nối Máy tính Nhúng Raspberry Pi 4B

| Cổng Giao tiếp | Thiết bị Ngoại vi Kết nối | Thông số Truyền thông |
| :--- | :--- | :--- |
| **USB Type-C / USB 3.0** | Cáp dữ liệu USB sang ESP32-S3 | Serial CDC `/dev/ttyACM0`, 115200 bps |
| **USB 2.0 Port** | Cảm biến 2D LiDAR (RPLiDAR / LDLiDAR) | Serial `/dev/ttyUSB0`, 115200 / 230400 bps |
| **USB 2.0 / CSI** | Camera Full HD hướng sàn | V4L2 device `/dev/video0` (640x480 @ 30fps) |
| **Nguồn DC Jack** | Mạch hạ áp Buck DC-DC 5V / 5A | Nguồn điện độc lập chống sụt áp |
