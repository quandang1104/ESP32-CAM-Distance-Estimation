import cv2
import requests
import numpy as np

STREAM_URL = "http://192.168.2.41:81/stream"  
DISTANCE_API = "http://192.168.2.41/distance"

# 2. Khởi tạo
car_cascade = cv2.CascadeClassifier('cars.xml')

# 3. Kết nối Camera ESP32
cap = cv2.VideoCapture(STREAM_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) 

print("Connecting to ESP32 Camera and HC SR04 ")

while True:
    # 1. Lấy ảnh từ luồng Camera
    ret, frame = cap.read()
    if not ret: continue
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in cars:
       
        try:
            response = requests.get(DISTANCE_API, timeout=0.15)
            real_distance_cm = float(response.text)
            
            if real_distance_cm > 0:
                text_to_show = f"Khoang cach: {real_distance_cm:.1f} cm"
            else:
                text_to_show = "Ngoai tam do!"
        except Exception as e:
            text_to_show = "Dang do..." 
            
        # 3. Vẽ khung và in kết quả
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, text_to_show, (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("ESP32-CAM Sensor Fusion", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
