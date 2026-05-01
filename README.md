# 🚗 ESP32-CAM Sensor Fusion: Vehicle Detection & Distance Measurement

Dự án này kết hợp khả năng xử lý hình ảnh (Computer Vision) và phần cứng cảm biến (IoT) để tạo ra một hệ thống theo dõi khoảng cách xe theo thời gian thực. Hệ thống sử dụng mạch **ESP32-CAM** làm biên (Edge Device) và thuật toán **Haar Cascade** trên Python để nhận diện, kết hợp với cảm biến siêu âm **HC-SR04** để cung cấp độ chính xác tuyệt đối.

## 🌟 Tính năng nổi bật (Features)
*   **Edge Computing:** Vi điều khiển ESP32 xử lý đồng thời 2 luồng dữ liệu: Phát luồng Video MJPEG (Port 81) và cung cấp API RESTful trả về khoảng cách vật lý (Port 80).
*   **Sensor Fusion (Dung hợp cảm biến):** Khắc phục hoàn toàn điểm yếu đo lường quang học (Pinhole Camera model) bằng cách lấy tọa độ nhận diện từ AI (Camera) đối chiếu với dữ liệu độ sâu từ Cảm biến (Siêu âm).
*   **Real-time Processing:** Xử lý luồng video độ trễ thấp với thư viện OpenCV.

## 🛠️ Cấu trúc phần cứng (Hardware Setup)
Do hạn chế về chân GPIO trên mạch ESP32-CAM, dự án này đã vô hiệu hóa khe cắm thẻ nhớ SD để lấy chân giao tiếp cho cảm biến siêu âm HC-SR04.

**Sơ đồ đấu dây (Wiring Diagram):**

| Cảm biến HC-SR04 | Mạch ESP32-CAM | Chức năng |
| :--- | :--- | :--- |
| **VCC** | 5V | Cấp nguồn |
| **GND** | GND | Nối đất |
| **Trig** | GPIO 14 | Phát sóng siêu âm |
| **Echo** | GPIO 15 | Thu sóng siêu âm |

*(Lưu ý: Khi nạp code, vui lòng tháo các chân cảm biến ra khỏi ESP32-CAM hoặc sử dụng dây jumper để kết nối mạch nạp (TX/RX/5V/GND) nhằm tránh xung đột).*

## 💻 Yêu cầu phần mềm (Software Requirements)
*   **Firmware:** PlatformIO hoặc Arduino IDE (Đã cài đặt package ESP32).
*   **Software:** Python 3.x
*   **Thư viện Python:** `opencv-python`, `numpy`, `requests`, `urllib`

## 🚀 Hướng dẫn chạy dự án (How to Run)

### Bước 1: Nạp Firmware cho ESP32-CAM
1. Mở thư mục `firmware` bằng VS Code (PlatformIO).
2. Mở file `main.cpp`, cấu hình lại thông tin mạng WiFi của bạn:
   ```cpp
   const char* ssid = "TEN_WIFI_CUA_BAN";
   const char* password = "MAT_KHAU_WIFI";
   ```
3. Cắm mạch ESP32-CAM vào máy tính và nhấn **Upload**.
4. Mở Serial Monitor (Baud rate 115200) để lấy địa chỉ IP của mạch (Ví dụ: `192.168.1.100`).

### Bước 2: Chạy hệ thống AI trên máy tính
1. Cấp nguồn ngoài cho ESP32-CAM và kết nối cảm biến HC-SR04 theo sơ đồ phía trên.
2. Mở thư mục `software`, cài đặt các thư viện cần thiết:
   ```bash
   pip install opencv-python numpy requests
   ```
3. Mở file `main.py` và cập nhật lại địa chỉ IP vừa lấy được:
   ```python
   STREAM_URL = "[http://192.168.](http://192.168.)x.x:81/stream"  
   DISTANCE_API = "[http://192.168.](http://192.168.)x.x/distance" 
   ```
4. Chạy file Python:
   ```bash
   python main.py
   ```

## 🧠 Luồng hoạt động của hệ thống
1. Thấu kính Camera thu nhận hình ảnh xe thực tế và đẩy qua luồng WiFi (`/stream`).
2. Thuật toán `Haar Cascade` trên Python quét mảng Grayscale để tìm ra khung tọa độ (Bounding Box) của chiếc xe.
3. Ngay khi bắt được xe, Python kích hoạt một request HTTP GET siêu tốc tới ESP32-CAM (`/distance`).
4. ESP32-CAM đọc sóng siêu âm HC-SR04, tính toán khoảng cách thực tế (cm) và trả về cho Python in lên màn hình.