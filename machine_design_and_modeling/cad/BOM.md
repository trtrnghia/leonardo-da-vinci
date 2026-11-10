# Bảng Thống Kê Vật Tư & Linh Kiện Phần Cứng (Bill of Materials - BOM)

Dự án: **Leonardo da Vinci - 3-Wheel Omni AGV Drawing Robot**  
Mã dự án: `LEONARDO-AGV-2026`

---

## 1. Cơ Khí & Khung Vỏ (Mechanical & Structural Components)

| STT | Tên linh kiện / Chi tiết | Mã hiệu / Quy cách | Số lượng | Vật liệu / Nhà sản xuất | Vai trò chức năng |
| :---: | :--- | :--- | :---: | :--- | :--- |
| 1 | Khung đĩa gầm chính (Base Plate) | $\varnothing 300\text{ mm} \times 3\text{ mm}$ | 1 | Nhôm 6061 Anodized / Cắt CNC | Tấm gầm liên kết động cơ và ngòi bút |
| 2 | Khung đĩa nóc (Top Plate) | $\varnothing 300\text{ mm} \times 2.5\text{ mm}$ | 1 | Mica đục / Cắt Laser CNC | Tầng gá Raspberry Pi, ESP32 và LiDAR |
| 3 | Trụ nhôm giằng khung | Chiều dài $50\text{ mm}$, ren M3 | 6 | Hợp kim nhôm lục giác | Giằng cố định 2 tầng đĩa gầm |
| 4 | Bánh xe Omni đa hướng | Đường kính $58\text{ mm}$, cốt $4\text{ mm}$ | 3 | Nhôm + Con lăn cao su Nitrile | Dẫn động 3 bậc tự do 120° |
| 5 | Gá nhôm động cơ DC | Bracket chữ L cho DC Gear Motor | 3 | Nhôm dập uốn $2\text{ mm}$ | Cố định động cơ vào khung đĩa gầm |
| 6 | Ray trượt mini dẫn hướng bút | MGN7C hoặc Linear Shaft $\varnothing 4\text{ mm}$ | 1 | Thép chịu lực chống gỉ | Dẫn hướng tì ngòi bút thẳng đứng |
| 7 | Cụm ngàm kẹp bút đa năng | Kẹp bút $\varnothing 8 - 14\text{ mm}$ kèm lò xo | 1 | Nhựa in 3D PETG / ABS | Giữ cố định bút vẽ mỹ thuật |
| 8 | Lò xo nén lực tì bút | Chiều dài tự do $25\text{ mm}$, $k = 0.08\text{ N/mm}$ | 2 | Thép lò xo chống biến dạng | Giảm chấn và phân bổ lực tì mực |
| 9 | Bộ ốc vít, bu lông, đệm cao su | Vít lục giác chìm M3 (dài 6, 10, 16mm) | 1 bộ | Thép đen cấp bền 8.8 + Silicone | Liên kết cơ khí toàn bộ robot |

---

## 2. Thiết Bị Điện & Cơ Cấu Chấp Hành (Electromechanical & Actuators)

| STT | Tên linh kiện / Thiết bị | Mã hiệu / Quy cách | Số lượng | Điện áp hoạt động | Vai trò chức năng |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | Động cơ DC giảm tốc kèm Encoder | Động cơ DC chổi than tỉ số 1:30 | 3 | $12\text{V DC}$ | Dẫn động 3 bánh xe Omni |
| 2 | Đĩa đếm xung Encoder Hall | 11 PPR (334 CPR ở trục ra) | 3 | $3.3\text{V} - 5\text{V DC}$ | Đọc phản hồi vận tốc góc bánh xe |
| 3 | Mạch công suất cầu H đôi | TB6612FNG / L298N Mini Dual H-Bridge| 2 | $12\text{V}$ (Động cơ), $5\text{V}$ (Logic)| Điều chế PWM và đổi chiều động cơ |
| 4 | Động cơ Micro Servo nâng/hạ bút | MG90S kim loại (Mô-men $1.8\text{ kg}\cdot\text{cm}$) | 1 | $4.8\text{V} - 6\text{V DC}$ | Kéo nhấc và tì ngòi bút vẽ |

---

## 3. Máy Tính Điều Khiển & Cảm Biến (Compute & Sensing)

| STT | Tên linh kiện / Module | Mã hiệu / Quy cách | Số lượng | Giao tiếp truyền thông | Vai trò chức năng |
| :---: | :--- | :--- | :---: | :--- | :--- |
| 1 | Máy tính nhúng Single-Board Computer | Raspberry Pi 4 Model B (RAM 8GB) | 1 | Ethernet, Wi-Fi, USB 3.0 | Chạy ROS 2 Jazzy, xử lý ảnh, LiDAR |
| 2 | Bo mạch Vi điều khiển | ESP32-S3-DevKitC-1 (8MB PSRAM) | 1 | USB CDC Serial 115200 bps | PID vòng kín thời gian thực, Servo |
| 3 | Cảm biến Laser 2D LiDAR | RPLiDAR A1 / LDLiDAR D300 (360°) | 1 | UART / USB Serial | Quét an toàn chống va chạm |
| 4 | Cảm biến Thị giác góc rộng | Full HD 1080p CMOS, Lens FOV 90° | 1 | USB 2.0 V4L2 | Chụp bề mặt giấy giải ma trận Homography |

---

## 4. Nguồn Điện & Mạch Phụ Trợ (Power Supply & Management)

| STT | Tên linh kiện / Thiết bị | Mã hiệu / Quy cách | Số lượng | Thông số định mức | Vai trò chức năng |
| :---: | :--- | :--- | :---: | :--- | :--- |
| 1 | Khối pin nguồn Li-Po | Pin Li-Po 3S 11.1V (Max 12.6V) | 1 | Dung lượng 2200mAh, dòng xả 25C | Cung cấp toàn bộ năng lượng hệ thống |
| 2 | Mạch giảm áp xung Buck DC-DC 1 | Mạch Buck 5V / 5A (XL4015 / LM2596 HV) | 1 | Đầu vào 12V $\to$ Đầu ra 5.1V / 5A | Cấp nguồn riêng cho Raspberry Pi 4B |
| 3 | Mạch giảm áp xung Buck DC-DC 2 | Mạch Buck 5V / 3A | 1 | Đầu vào 12V $\to$ Đầu ra 5.0V / 3A | Cấp nguồn riêng ESP32-S3, Servo & LiDAR |
| 4 | Công tắc nguồn chính (Power Switch) | Công tắc gạt kim loại chịu dòng cao | 1 | $250\text{V AC} / 10\text{A}$ | Đóng ngắt nguồn pin tổng |
| 5 | Nút dừng khẩn cấp (E-Stop) | Nút ấn cơ khí nấm đỏ tự giữ | 1 | Cắt trực tiếp nguồn mạch cầu H | Ngắt nguồn động cơ tức thì khi sự cố |
