# Machine Design and Modeling - Leonardo da Vinci Robot

Phần này chứa toàn bộ tài liệu kỹ thuật, mô hình hóa toán học, mô hình 3D URDF/Xacro, thông số cơ khí CAD, sơ đồ mạch điện và đấu nối phần cứng của Robot vẽ tranh tự hành 3 bánh Omni **Leonardo da Vinci**.

---

## 📐 Cấu trúc Thư mục

```
machine_design_and_modeling/
├── README.md                            # Tổng quan phần Thiết kế Cơ khí & Mô hình hóa
│
├── cad/                                 # Thiết kế Cơ khí & Thông số Kỹ thuật
│   ├── SPECIFICATIONS.md                # Kích thước hình học, vật liệu, kết cấu tải trọng
│   ├── BOM.md                           # Bảng thống kê vật tư & linh kiện phần cứng (Bill of Materials)
│   └── models/                          # Danh mục file CAD 3D (STEP, STL, bản vẽ chế tạo)
│       └── README.md
│
├── urdf/                                # Mô hình hóa 3D Robot trong ROS 2 & Gazebo
│   ├── leonardo.urdf.xacro              # File mô tả robot chuẩn (kinematic chain, visual, collision, inertial)
│   └── README.md                        # Hướng dẫn kiểm tra cây khớp nối & visualizer
│
├── kinematics_and_dynamics/             # Cơ sở Toán học & Mô hình Động học - Động lực học
│   └── KINEMATICS_AND_DYNAMICS.md       # Động học Omni 120°, Dead Reckoning, Homography, TF Tree
│
├── electrical_and_wiring/               # Sơ đồ Điện tử & Đấu nối Phần cứng
│   ├── PINOUT.md                        # Bảng phân bổ chân GPIO ESP32-S3 & cổng giao tiếp Raspberry Pi 4
│   └── POWER_AND_WIRING.md              # Sơ đồ khối cấp nguồn LiPo, mạch hạ áp buck kép & an toàn
│
└── docs/                                # Báo cáo Thiết kế Kỹ thuật Toàn diện
    └── 2026-11-09-leonardo-da-vinci-robot-design.md # Báo cáo kiến trúc hệ thống gốc
```

---

## 🛠 1. Thiết kế Cơ khí (Mechanical & CAD Design)

- **Cấu hình dẫn động**: 3 bánh xe Omni nhôm $\varnothing 58\text{ mm}$ với con lăn cao su bố trí đối xứng góc $120^\circ$.
- **Khung thân robot (Chassis)**: Thân tròn 2 tầng nhôm 6061/Mica cắt CNC bán kính $R = 150\text{ mm}$ ($\varnothing 300\text{ mm}$), chiều cao thân xe $60\text{ mm}$, khoảng sáng gầm $50\text{ mm}$.
- **Cơ cấu nâng/hạ bút (Pen Mechanism)**:
  - Thanh trượt dẫn hướng thẳng đứng có lò xo giảm chấn lực tì ($0.5\text{ N} - 1.2\text{ N}$).
  - Động cơ RC Micro Servo 9g (SG90/MG90S) điều khiển quay góc $30^\circ$ (Pen UP) và $90^\circ$ (Pen DOWN).
  - Vị trí ngòi bút đặt đồng tâm với tâm quay hình học robot ($x = 0, y = 0$).
- **Gá lắp cảm biến**:
  - Gá camera Full HD hướng sàn vuông góc với mặt giấy, tích hợp đệm cao su giảm rung chấn từ động cơ.
  - Cụm LiDAR 2D đặt trên tầng nóc cao nhất nhằm quét quét góc $360^\circ$ không bị che khuất bởi bánh xe hoặc dây cáp.

Chi tiết xem tại: [`cad/SPECIFICATIONS.md`](cad/SPECIFICATIONS.md) và [`cad/BOM.md`](cad/BOM.md).

---

## 🤖 2. Mô hình hóa 3D URDF/Xacro (Kinematic & Dynamic Modeling)

File mô hình gốc: [`urdf/leonardo.urdf.xacro`](urdf/leonardo.urdf.xacro)

### Các Khâu (Links) và Khớp nối (Joints):
1. **`base_footprint`**: Hình chiếu trọng tâm robot lên mặt phẳng sàn/giấy ($z = 0$).
2. **`base_link`**: Tâm khung gầm robot tại độ cao $z = +0.05\text{ m}$, khối lượng $2.5\text{ kg}$, ma trận quán tính $I_{xx} = I_{yy} = 0.0148\text{ kg}\cdot\text{m}^2, I_{zz} = 0.0281\text{ kg}\cdot\text{m}^2$.
3. **`wheel_1_link`, `wheel_2_link`, `wheel_3_link`**: 3 bánh xe Omni quay quanh trục quay riêng với các góc $\alpha_1 = 0^\circ, \alpha_2 = 120^\circ, \alpha_3 = 240^\circ$.
4. **`pen_tip_link`**: Điểm tiếp xúc của ngòi bút với mặt giấy.
5. **`camera_link`**: Vị trí quang tâm của camera thị giác hướng sàn.
6. **`laser_link`**: Mặt phẳng quét của cảm biến LiDAR 2D.

Kiểm tra mô hình trên RViz2:
```bash
ros2 launch leonardo_bringup view_robot.launch.py
```

---

## 📐 3. Mô hình Toán học Động học & Động lực học (Kinematics & Dynamics)

Chi tiết công thức xem tại: [`kinematics_and_dynamics/KINEMATICS_AND_DYNAMICS.md`](kinematics_and_dynamics/KINEMATICS_AND_DYNAMICS.md)

- **Động học ngược (Inverse Kinematics)**:
  $$\begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \end{bmatrix} = \frac{1}{r} \begin{bmatrix} 0 & 1 & R \\ -\frac{\sqrt{3}}{2} & -\frac{1}{2} & R \\ \frac{\sqrt{3}}{2} & -\frac{1}{2} & R \end{bmatrix} \begin{bmatrix} v_x \\ v_y \\ \omega_z \end{bmatrix}$$
- **Động học thuận (Forward Kinematics & Odometry)**:
  $$\begin{bmatrix} v_x \\ v_y \\ \omega_z \end{bmatrix} = r \begin{bmatrix} 0 & -\frac{1}{\sqrt{3}} & \frac{1}{\sqrt{3}} \\ \frac{2}{3} & -\frac{1}{3} & -\frac{1}{3} \\ \frac{1}{3R} & \frac{1}{3R} & \frac{1}{3R} \end{bmatrix} \begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \end{bmatrix}$$
- **Biến đổi Phối cảnh Homography ($H$)**: Ánh xạ từ tọa độ camera $(u, v)$ về tọa độ giấy $(X, Y)$ chuẩn milimet nhằm khử sai số trượt của bánh xe Omni.

---

## ⚡ 4. Thiết kế Mạch Điện & Sơ đồ Cấp Nguồn (Electrical & Wiring)

- **Sơ đồ chân GPIO**: [`electrical_and_wiring/PINOUT.md`](electrical_and_wiring/PINOUT.md)
- **Kiến trúc cấp nguồn**: [`electrical_and_wiring/POWER_AND_WIRING.md`](electrical_and_wiring/POWER_AND_WIRING.md)
  - Pin LiPo 3S 11.1V 2200mAh 25C.
  - Mạch Buck DC-DC 1: $11.1\text{V} \to 5\text{V}/5\text{A}$ cấp riêng cho Raspberry Pi 4B.
  - Mạch Buck DC-DC 2: $11.1\text{V} \to 5\text{V}/3\text{A}$ cấp riêng cho ESP32-S3, Servo ngòi bút và cảm biến LiDAR để cách ly sụt áp xung động cơ.
