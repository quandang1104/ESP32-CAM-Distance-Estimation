import cv2
from ultralytics import YOLO

# 1. Cấu hình các thông số (Bạn sẽ tinh chỉnh sau)
ESP32_IP = "192.168.2.41" # Thay bằng IP hiện trên Serial Monitor của ESP32
STREAM_URL = f"http://192.168.2.41:81/stream"

# Thông số để tính khoảng cách
REAL_WIDTH = 1.8   # Chiều rộng thực tế ô tô (mét)
FOCAL_LENGTH = 700 # Tiêu cự (Sẽ calibrate sau)

# 2. Tải model AI (Lần đầu chạy sẽ hơi lâu vì nó tự tải model về)
model = YOLO('yolov8n.pt') 

# cap = cv2.VideoCapture(STREAM_URL)
cap = cv2.VideoCapture(STREAM_URL, cv2.CAP_FFMPEG)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Waiting for ESP32...")
        continue

    # 3. Nhận diện ô tô (Class 2 là xe con, 7 là xe tải)
    results = model(frame, classes=[2, 7], conf=0.5)

    for r in results:
        for box in r.boxes:
            # Lấy tọa độ và vẽ khung
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w_pixel = x2 - x1
            
            # 4. Tính khoảng cách
            distance = (REAL_WIDTH * FOCAL_LENGTH) / w_pixel
            
            # Vẽ lên màn hình
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{distance:.2f}m", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("AI system CAM", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()