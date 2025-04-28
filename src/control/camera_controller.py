import cv2
import threading
import time
import subprocess
from src.config.settings import CAMERA_INDEX

cap = None
streaming = False
stream_thread = None

# 기본 카메라 열기 함수
def open_camera_usb():
    global cap
    close_camera()
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("📷 USB 웹캠 열림 (/dev/video0)")
    else:
        print("❌ USB 웹캠 열기 실패")

def open_camera_pi():
    global cap
    close_camera()
    # PiCamera를 GStreamer 파이프라인으로 열기
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

def start_streaming():
    global streaming, stream_thread
    if cap is None or not cap.isOpened():
        print("⚠️ 카메라가 열려 있지 않습니다. 먼저 open_camera 명령 필요")
        return
    if not streaming:
        streaming = True
        stream_thread = threading.Thread(target=stream_loop)
        stream_thread.start()
        print("▶️ 스트리밍 시작")

def stream_loop():
    while streaming:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera", frame)
            # TODO: 서버로 전송 코드 추가 가능
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stop_streaming()

def stop_streaming():
    global streaming
    if streaming:
        streaming = False
        time.sleep(0.5)
        cv2.destroyAllWindows()
        print("⏹️ 스트리밍 중단")

def close_camera():
    global cap
    if cap:
        cap.release()
        cap = None
        print("🛑 카메라 닫힘")
    cv2.destroyAllWindows()
