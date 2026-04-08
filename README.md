# 🚗 AI-Powered Vehicle Distance Estimation (ESP32-CAM & YOLOv8)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![C++](https://img.shields.io/badge/C++-Embedded-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32--CAM-PlatformIO-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Computer_Vision-FF9900?style=for-the-badge&logo=yolo&logoColor=white)

A real-time monitoring system combining IoT (Edge device) and AI. This project utilizes an **ESP32-CAM** to broadcast a live video stream (MJPEG) over a local WiFi network, coupled with a **YOLOv8** model running on a PC to detect vehicles and dynamically estimate their physical distance.

---

## ✨ Key Features

* **Live Video Streaming:** Built a lightweight asynchronous HTTP Web Server on the ESP32 using C/C++, optimized for memory and low latency to stream continuous frames.
* **Real-time Object Detection:** Integrated the YOLOv8 Deep Learning model (via the Ultralytics library) to accurately detect vehicles and draw bounding boxes.
* **Distance Estimation:** Implemented a Triangle Similarity mathematical algorithm to convert pixel coordinates into actual physical distance (meters).

## 🛠️ Hardware & Tech Stack

### Hardware
* AI-Thinker ESP32-CAM Development Board (OV2640 Camera module).
* USB-to-TTL Programmer/Converter (FT232RL/CH340).

### Software
* **Edge Firmware:** Arduino Framework, PlatformIO (VS Code).
* **AI Client:** Python, OpenCV (Image processing), Ultralytics (YOLO inference).

---

## 🚀 Setup & Usage Guide

### 1. Flashing the Firmware (C++)
1. Open the `firmware` directory using PlatformIO in VS Code.
2. Update your WiFi credentials (`ssid` and `password`) in the `src/main.cpp` file.
3. Connect **GPIO 0** to **GND** on the ESP32-CAM to enter Flash Mode.
4. Build and Upload the code. Once successful, disconnect GPIO 0, press the Reset button, and open the Serial Monitor to retrieve the stream's IP address.

### 2. Running the AI Client (Python)
1. Open a terminal and navigate to the `software` directory.
2. Open `main.py` and update the `ESP32_IP` variable with the IP address obtained from the Serial Monitor.
3. Activate your virtual environment and install the required dependencies:
   ```bash
   pip install opencv-python ultralytics requests
