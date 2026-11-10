# Đặc Tả Kỹ Thuật Cơ Khí (Mechanical Specifications)

Tài liệu này định nghĩa đầy đủ các thông số kích thước hình học, tải trọng, vật liệu chế tạo và cơ cấu truyền động của Robot vẽ tranh tự hành 3 bánh Omni **Leonardo da Vinci**.

---

## 1. Thông Số Hình Học & Kích Thước Tổng Thể

| Thông số | Giá trị danh định | Dung sai cho phép | Đơn vị | Ghi chú |
| :--- | :--- | :--- | :--- | :--- |
| **Đường kính thân xe ($\varnothing_{\text{chassis}}$)** | 300 | $\pm 0.5$ | mm | Kết cấu đĩa tròn 2 tầng |
| **Bán kính phân bố bánh xe ($R$)** | 150 | $\pm 0.2$ | mm | Khoảng cách từ tâm quay đến tâm bánh xe |
| **Đường kính bánh xe Omni ($2r$)** | 58 | $\pm 0.2$ | mm | Bánh Omni nhôm có con lăn cao su bám giấy |
| **Bán kính bánh xe ($r$)** | 29 | $\pm 0.1$ | mm | Thông số đưa vào ma trận động học |
| **Bề rộng bánh xe** | 25 | $\pm 0.2$ | mm | Chiều rộng tiếp xúc con lăn |
| **Góc phân bố 3 bánh xe ($\alpha_i$)** | $0^\circ, 120^\circ, 240^\circ$ | $\pm 0.1^\circ$ | deg | Đối xứng đều qua tâm |
| **Chiều cao khung robot** | 60 | $\pm 1.0$ | mm | Khoảng cách từ sàn đến mặt nóc |
| **Khoảng sáng gầm xe** | 20 | $\pm 0.5$ | mm | Khoảng hở đáy xe so với mặt giấy vẽ |
| **Trọng lượng tổng thể ($m$)** | 2.50 | $\pm 0.1$ | kg | Đã bao gồm pin LiPo 3S và cảm biến |

---

## 2. Đặc Tính Khối Lượng & Quán Tính (Mass & Inertia Properties)

Tâm khối lượng (Center of Mass - CoM) được thiết kế nằm sát trục trung tâm đối xứng ($x \approx 0, y \approx 0$) ở độ cao $z = +0.02\text{ m}$ so với mặt phẳng đế để đảm bảo tính ổn định chống lật khi gia tốc:

- **Khối lượng thân xe ($m_{\text{base}}$)**: $2.5\text{ kg}$
- **Tenxơ quán tính khối lượng (Inertia Tensor)** tính tại trọng tâm:
  $$
  I = \begin{bmatrix}
  I_{xx} & I_{xy} & I_{xz} \\
  I_{yx} & I_{yy} & I_{yz} \\
  I_{zx} & I_{zy} & I_{zz}
  \end{bmatrix}
  = \begin{bmatrix}
  0.0148 & 0 & 0 \\
  0 & 0.0148 & 0 \\
  0 & 0 & 0.0281
  \end{bmatrix} \quad (\text{kg}\cdot\text{m}^2)
  $$

---

## 3. Cơ Cấu Bút Vẽ (Pen Lift Mechanism)

Cơ cấu kẹp và nâng/hạ bút vẽ là bộ phận cơ khí chấp hành cốt lõi:
- **Cơ chế dẫn hướng**: Ray trượt tuyến tính mini (Linear guide slide) độ ma sát thấp.
- **Cơ chế đàn hồi tì bút**: Lò xo nén tinh chỉnh lực tì nhằm duy trì lực đè ngòi bút ổn định trong khoảng **$0.5\text{ N} - 1.2\text{ N}$**, phù hợp cho cả bút bi, bút lông kim và bút chì nghệ thuật mà không làm rách hay mòn giấy.
- **Động cơ chấp hành nâng hạ**: Động cơ Micro Servo 9g kim loại (MG90S):
  - Góc nâng bút (Pen UP - không vẽ): $30^\circ$ (ngòi bút nâng cách mặt giấy $8 - 10\text{ mm}$).
  - Góc hạ bút (Pen DOWN - vẽ): $90^\circ$ (ngòi bút tiếp xúc thẳng đứng với mặt giấy).
- **Độ trễ phản hồi cơ học**:
  - Thời gian chuyển trạng thái: $< 80\text{ ms}$.
  - Thời gian ổn định tiếp xúc mực (Damping settling time): $250\text{ ms}$ trước khi bắt đầu dịch chuyển xe.

---

## 4. Hệ Thống Dẫn Động & Bánh Xe Omni (3-Wheel Omni Drive)

- **Động cơ DC giảm tốc**: 3x Động cơ DC kèm hộp số kim loại tỉ số truyền 1:30.
- **Encoder tích hợp**: Bộ mã hóa góc quay từ tính đĩa Hall 11 PPR (xung/vòng trước hộp số), tương đương **334 CPR (Counts Per Revolution)** ở trục đầu ra của bánh xe.
- **Tốc độ di chuyển tối đa danh định**:
  - Vận tốc thẳng $v_{\max} = 0.25\text{ m/s}$ (tối ưu hóa nét vẽ mượt mà không văng mực).
  - Vận tốc góc $\omega_{\max} = 1.5\text{ rad/s}$.
- **Vật liệu bánh xe**: Hợp kim nhôm cắt CNC, 10 con lăn phụ bằng cao su dẻo tổng hợp Nitrile (NBR) chống trượt trên bề mặt giấy A4/A3/A2.

---

## 5. Bố Trí Cảm Biến (Sensor Placement)

1. **Cảm biến LiDAR 2D 360°**:
   - Vị trí: Đặt trên tầng nóc trung tâm ở tọa độ $(x=0.0, y=0.0, z=+0.08\text{ m})$.
   - Trường quan sát: Quét ngang góc $360^\circ$ không bị che khuất.
   - Nhiệm vụ: Giám sát vùng an toàn, phát hiện chướng ngại vật trong bán kính $< 0.3\text{ m}$ để kích hoạt phanh khẩn cấp và nhấc bút.
2. **Camera Thị giác Hướng Sàn (Down-facing Vision Sensor)**:
   - Vị trí: Gá dưới gầm xe hướng thẳng đứng xuống mặt giấy $(x=0.06, y=0.0, z=+0.03\text{ m})$.
   - Độ phân giải: Full HD $1920 \times 1080$, góc nhìn ngang $90^\circ$ (FOV).
   - Khử rung: Vòng đệm silicon cách ly rung động từ khung gầm động cơ truyền vào ống kính.
