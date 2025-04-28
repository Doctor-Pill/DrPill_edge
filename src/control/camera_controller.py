# 📍 DrPill_edge/src/control/camera_controller.py

import cv2
import subprocess

cap = None
stream_proc = None

def open_camera_usb():
    global cap
    close_camera()
    print("📷 USB 웹캠 오픈 중...")
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("✅ USB 웹캠 오픈 성공")
    else:
        print("❌ USB 웹캠 오픈 실패")

def open_camera_pi():
    global cap
    close_camera()
    print("📷 PiCamera 오픈 중...")
    gst_pipeline = (
        "libcamerasrc ! "
        "video/x-raw,width=640,height=480,framerate=30/1 ! "
        "videoconvert ! "
        "appsink"
    )
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if cap.isOpened():
        print("✅ PiCamera 오픈 성공")
    else:
        print("❌ PiCamera 오픈 실패")

def start_monitor_and_stream():
    global cap, stream_proc
    if cap is None or not cap.isOpened():
        print("⚠️ 카메라가 열려있지 않습니다. 먼저 open 명령을 실행하세요.")
        return

    print("🚀 스트리밍 및 모니터 시작")
    stream_cmd = [
        "ffmpeg",
        "-f", "v4l2",
        "-framerate", "30",
        "-video_size", "640x480",
        "-i", "/dev/video0",  # PiCam일 때는 다른 장치 경로 필요
        "-f", "mpegts",
        "udp://192.168.0.10:5000"  # 서버 IP에 맞게 수정
    ]
    stream_proc = subprocess.Popen(stream_cmd,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)

def stop_monitor_and_stream():
    global cap, stream_proc
    print("🛑 스트리밍 및 모니터 중단")

    if stream_proc:
        stream_proc.terminate()
        stream_proc = None

    close_camera()

def close_camera():
    global cap
    if cap:
        cap.release()
        cap = None
        print("✅ 카메라 연결 종료")