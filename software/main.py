import cv2

STREAM_URL = "http://192.168.2.41:81/stream"  
REAL_WIDTH = 0.03  # Chiều rộng thực tế của xe Hotwheels (Mét). 3cm = 0.03m
FOCAL_LENGTH = 450 # Tiêu cự ước lượng 

# 2. Khởi tạo "Bộ não" nhận diện
car_cascade = cv2.CascadeClassifier('cars.xml')

# 3. Kết nối Camera ESP32
cap = cv2.VideoCapture(STREAM_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # Ép chạy mượt thời gian thực

print("Đang kết nối với ESP32 Camera...")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Chuyển ảnh sang trắng đen để Haar Cascade chạy nhanh hơn gấp 3 lần
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 4. Tìm kiếm ô tô trong khung hình
    # scaleFactor và minNeighbors là độ nhạy.
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    for (x, y, w, h) in cars:
        distance = (REAL_WIDTH * FOCAL_LENGTH) / w
        
        # Vẽ khung màu xanh lá bao quanh xe
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Ghi chữ lên màn hình
        text = f"Khoang cach: {distance:.2f} m"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Hiển thị
    cv2.imshow("Hotwheels Tracker", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()