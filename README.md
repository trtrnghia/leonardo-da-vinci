# Leonardo da Vinci - 3-Wheel Omni AGV Drawing Robot

Dự án robot vẽ tranh tự hành 3 bánh omni (120°) kết hợp thị giác máy tính OpenCV, biến đổi Homography, ước lượng Odometry từ ESP32-S3 và cảm biến an toàn LiDAR 2D.

Tài liệu thiết kế chi tiết: [docs/2026-11-09-leonardo-da-vinci-robot-design.md](file:///home/davinci/Leonardo%20da%20Vinci/docs/2026-11-09-leonardo-da-vinci-robot-design.md)

---

## Cấu trúc Packages trong `src/`

1. **`leonardo_msgs`** (ament_cmake): Định nghĩa các ROS 2 Interface custom:
   - `PenCommand.msg`: Lệnh nâng/hạ bút vẽ (`pen_down`).
   - `WheelSpeeds.msg`: Vận tốc góc 3 bánh omni (`w1, w2, w3`).
   - `CanvasPose.msg`: Tọa độ 2D của robot trên khổ giấy vẽ (`pose`, `confidence`).
   - `DrawStatus.msg`: Trạng thái máy trạng thái vẽ tranh (`current_stroke`, `total_strokes`, `state`).

2. **`leonardo_kinematics`** (ament_python):
   - `kinematics_node.py`: Động học thuận/nghịch cho AGV 3 bánh omni 120° & phát tán `/odom` (`odom -> base_link`).

3. **`leonardo_vision`** (ament_python):
   - `vision_node.py`: Xử lý ảnh, trích xuất biên (Canny), vector hóa đường nét (RDP algorithm).
   - `homography_node.py`: Tính ma trận biến đổi phối cảnh Homography $H$ và định vị robot trên mặt phẳng giấy vẽ.
   - `calibration_node.py`: Hiệu chuẩn ma trận nội tại và khử méo camera $(K, D)$.

4. **`leonardo_controller`** (ament_python):
   - `drawing_controller_node.py`: Điều phối quỹ đạo nét vẽ và trạng thái Pen UP / Pen DOWN.
   - `safety_node.py`: Giám sát LiDAR 2D (`/scan`), dừng robot và nhấc bút khi có vật cản < 30 cm.

5. **`leonardo_bringup`** (ament_python):
   - `esp32_bridge_node.py`: Cầu nối Serial USB CDC giao tiếp với vi điều khiển ESP32-S3.
   - `launch/bringup.launch.py`: File launch toàn bộ hệ thống.
   - `config/robot_params.yaml`: File cấu hình thông số vật lý và ngưỡng an toàn.
   - `urdf/leonardo.urdf.xacro`: Mô tả mô hình robot TF / URDF.

6. **`leonardo_firmware`** (PlatformIO / Arduino ESP32-S3):
   - `platformio.ini`: Cấu hình PlatformIO cho ESP32-S3 DevKit.
   - `src/main.cpp`: Khung code firmware điều khiển PWM động cơ, đọc encoder và servo nâng bút.
   - `include/config.h`: Định nghĩa sơ đồ chân GPIO.
