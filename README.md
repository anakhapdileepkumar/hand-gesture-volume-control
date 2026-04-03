# Hand Gesture Volume Control

## 📌 Overview
This project uses computer vision to control system volume using hand gestures in real-time.

## 🚀 Features
- Hand tracking using MediaPipe
- Volume control using finger distance
- Smooth volume adjustment
- On-screen volume bar and percentage
- Mute gesture using finger pinch

## 🛠️ Technologies Used
- Python
- OpenCV
- MediaPipe
- Pycaw
- NumPy

## ▶️ How it works
- Webcam captures hand
- Thumb & index finger distance is calculated
- Distance is mapped to system volume
- Pinch gesture mutes audio

## ▶️ Run the project
```bash
pip install -r requirements.txt
py -3.10 main.py
