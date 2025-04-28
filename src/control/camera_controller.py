# 📍 DrPill_edge/src/control/camera_controller.py

import cv2
import threading
import time
from src.config.settings import CAMERA_INDEX

camera_running = False
cap = None
thread = None

def camera_loop():
    global cap
    while camera_running:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Camera', frame)
            # TODO: 서버로 frame 전송 가능 (추후 확장)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stop_camera()

def start_camera():
    global cap, camera_running, thread
    if not camera_running:
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            print("❌ 카메라 열기 실패")
            return
        camera_running = True
        thread = threading.Thread(target=camera_loop)
        thread.start()
        print("📷 카메라 시작")

def stop_camera():
    global cap, camera_running
    camera_running = False
    time.sleep(0.5)
    if cap:
        cap.release()
    cv2.destroyAllWindows()
    print("🛑 카메라 중지")

def capture_photo():
    global cap
    if cap and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # TODO: 서버로 frame 전송
            print("📸 사진 캡처")
        else:
            print("⚠️ 사진 캡처 실패")
    else:
        print("⚠️ 카메라가 열려있지 않습니다.")
