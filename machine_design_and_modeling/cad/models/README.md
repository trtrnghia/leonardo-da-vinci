# 3D CAD Models & Manufacturing Assets

Thư mục này lưu trữ các tệp thiết kế mô hình 3D SolidWorks / Fusion 360 / STEP và tệp lưới in 3D STL dùng cho việc chế tạo gia công robot **Leonardo da Vinci**.

---

## Danh mục tệp mô hình tiêu chuẩn

1. **`chassis_base_plate.dxf / .step`**:
   - Bản vẽ 2D cắt laser tấm nhôm đế $\varnothing 300\text{ mm}$ dày $3\text{ mm}$.
   - Chứa các lỗ bắt ốc ren M3 cho 3 gá động cơ đối xứng góc $120^\circ$, lỗ thoát trục ngòi bút trung tâm và rãnh đi dây nguồn.

2. **`chassis_top_plate.dxf / .step`**:
   - Bản vẽ tấm nóc mica $2.5\text{ mm}$ bảo vệ và gá cảm biến LiDAR 2D.

3. **`pen_mechanism_slider.stl`**:
   - File lưới in 3D cụm ngàm kẹp bút bằng vật liệu PETG/ABS với độ điền (infill) $60\%$.
   - Tích hợp khoang chứa lò xo nén chống sốc và ngàm gắn tay đòn Micro Servo MG90S.

4. **`camera_mount_bracket.stl`**:
   - Gá đỡ camera hướng sàn góc nhìn vuông góc mặt phẳng giấy, có khoang gắn đệm cao su giảm chấn rung.

5. **`omni_wheel_adapter_4mm.stl`**:
   - Khớp nối trục động cơ D-shaft $4\text{ mm}$ sang đĩa bắt ốc của bánh Omni 58mm.

---

## Hướng dẫn Xuất & Chuyển đổi sang Mô hình Robot ROS:
- Định dạng xuất trực quan cho ROS 2 RViz / Gazebo: `.stl` hoặc `.dae` (Collada).
- Đơn vị đo tiêu chuẩn khi xuất: **Mét (Meters)** hoặc **Milimet (mm kèm tỉ lệ scale 0.001)** để khớp chính xác với tọa độ trong [`urdf/leonardo.urdf.xacro`](../urdf/leonardo.urdf.xacro).
