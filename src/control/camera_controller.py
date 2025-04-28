# 📍 DrPill_edge/src/control/camera_controller.py

import cv2

cap = None

def open_camera_usb():
    global cap
    close_camera()
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("📷 USB 카메라 열림 (/dev/video0)")
    else:
        print("❌ USB 카메라 열기 실패")

def open_camera_pi():
    global cap
    close_camera()
    gst_pipeline = (
        "libcamerasrc ! "
        "video/x-raw,width=640,height=480,framerate=30/1 ! "
        "videoconvert ! "
        "appsink"
    )
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if cap.isOpened():
        print("📷 Pi Camera 열림 (libcamera)")
    else:
        print("❌ Pi Camera 열기 실패")

def close_camera():
    global cap
    if cap:
        cap.release()
        cap = None
        print("🛑 카메라 닫힘")
