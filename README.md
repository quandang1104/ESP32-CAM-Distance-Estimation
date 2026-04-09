# 🏎️ ESP32-CAM Hotwheels Distance Tracker

Dự án nhận diện và đo khoảng cách xe mô hình (Hotwheels) theo thời gian thực sử dụng **ESP32-CAM** và **OpenCV (Haar Cascade)**. 

Thay vì sử dụng các mô hình Deep Learning nặng nề (như YOLOv8) gây trễ hình (lag) và quá tải bộ đệm, dự án này áp dụng phương pháp tối ưu hóa luồng video (stream) thô từ ESP32-CAM kết hợp với thuật toán Haar Cascade siêu nhẹ trên Python. Kết quả mang lại tốc độ khung hình (FPS) mượt mà ngay cả trên máy tính cấu hình thấp.

---

## 🚀 Tính năng nổi bật
* **Web Server siêu mượt:** Sử dụng C++ gốc của Espressif để tối ưu hóa việc phát luồng MJPEG.
* **Nhận diện siêu nhẹ:** Sử dụng `haarcascade_car.xml` không cần GPU, không cần PyTorch/TensorFlow.
* **Đo khoảng cách thực tế:** Tính toán khoảng cách từ camera đến xe dựa trên nguyên lý Tam giác đồng dạng (Quang học).
* **Độ trễ thấp (Low Latency):** Xử lý triệt để hiện tượng kẹt bộ đệm (Buffer Lag) của OpenCV.

---

## 🛠️ Yêu cầu phần cứng & Phần mềm

### Phần cứng:
* 1x Mạch ESP32-CAM (Loại AI Thinker).
* 1x Đế nạp ESP32-CAM-MB (hoặc module FTDI).
* Nguồn điện: Khuyến nghị dùng nguồn 5V-2A (như sạc dự phòng) để chip WiFi hoạt động ổn định nhất, chống sụt áp.
* 1x Chiếc xe mô hình (ví dụ: Hotwheels).

### Phần mềm:
* **VS Code** với extension **PlatformIO**.
* **Python 3.x**
* Thư viện Python: `opencv-python`, `numpy`.

---

## ⚙️ Hướng dẫn Cài đặt & Sử dụng

### Phần 1: Cài đặt mạch ESP32-CAM (C++)
1. Mở thư mục dự án bằng PlatformIO.
2. Mở file `src/main.cpp`.
3. Thay đổi thông tin mạng WiFi của bạn:
   ```cpp
   const char* ssid = "YOUR_WIFI_NAME";
   const char* password = "YOUR_WIFI_PASSWORD";
   ```
   *(Lưu ý: Không bao giờ push mật khẩu thật của bạn lên Github!)*
4. Kết nối mạch vào máy tính và bấm **Upload**.
5. Mở Serial Monitor, copy địa chỉ IP của mạch (ví dụ: `http://192.168.2.41`).

### Phần 2: Khởi chạy Trí tuệ nhân tạo (Python)
1. Mở Terminal và cài đặt thư viện yêu cầu:
   ```bash
   pip install opencv-python numpy
   ```
2. Đảm bảo file `cars.xml` nằm cùng thư mục với file `main.py`.
3. Mở file `main.py` và dán IP của ESP32 vào biến `STREAM_URL` (nhớ giữ lại đuôi `:81/stream`):
   ```python
   STREAM_URL = "[http://192.168.2.41:81/stream](http://192.168.2.41:81/stream)"
   ```
4. Chạy file Python:
   ```bash
   python main.py
   ```

---

## 📐 Hướng dẫn Hiệu chỉnh (Calibration)
Để hệ thống đo khoảng cách chính xác, bạn cần hiệu chỉnh **Tiêu cự (Focal Length)** cho camera của mình:
1. Đặt chiếc xe cách camera đúng **30 cm (0.3m)**.
2. Chạy file Python và quan sát màn hình.
3. Trong file `main.py`, điều chỉnh biến `FOCAL_LENGTH`:
   * Nếu màn hình hiển thị > 0.3m: **Giảm** số này xuống.
   * Nếu màn hình hiển thị < 0.3m: **Tăng** số này lên.
4. Điều chỉnh cho đến khi khoảng cách hiển thị đúng `0.30 m`. Hệ thống của bạn đã được hiệu chuẩn!

---

## 📝 Lưu ý phát triển
* Để thuật toán Haar Cascade hoạt động tốt nhất, hãy chĩa camera trực diện vào phần **đầu xe** hoặc **đuôi xe**.
* Nếu bị báo lỗi `Stream timeout triggered`, hãy kiểm tra xem có tab trình duyệt Web nào đang chiếm dụng luồng Camera của mạch không. ESP32-CAM chỉ phục vụ 1 luồng duy nhất tại 1 thời điểm.
