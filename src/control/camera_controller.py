# 📍 DrPill_edge/src/control/camera_controller.py
import cv2
import subprocess

usb_stream_proc = None
picam_stream_proc = None
monitor_proc = None
usb_cap = None
picam_cap = None

def open_cameras():
    global usb_cap, picam_cap
    close_cameras()

    print("📷 USB 캠 오픈 중...")
    usb_cap = cv2.VideoCapture(0)
    if usb_cap.isOpened():
        print("✅ USB 캠 오픈 성공")
    else:
        print("❌ USB 캠 오픈 실패")

    print("📷 PiCam 오픈 중...")
    picam_cap = cv2.VideoCapture(2)
    if picam_cap.isOpened():
        print("✅ PiCam 오픈 성공")
    else:
        print("❌ PiCam 오픈 실패")

def close_cameras():
    global usb_cap, picam_cap
    if usb_cap is not None:
        usb_cap.release()
        usb_cap = None
        print("✅ USB 캠 해제")
    if picam_cap is not None:
        picam_cap.release()
        picam_cap = None
        print("✅ PiCam 해제")

def start_usb_streaming():
    global usb_stream_proc, monitor_proc
    stop_all_streaming()
    print("🚀 USB캠 송출 시작")
    usb_stream_proc = subprocess.Popen([
        "ffmpeg",
        "-f", "v4l2",
        "-framerate", "30",
        "-video_size", "640x480",
        "-i", "/dev/video0",
        "-f", "mpegts",
        "udp://192.168.0.10:5000"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    monitor_proc = subprocess.Popen([
        "ffplay",
        "-fflags", "nobuffer",
        "-flags", "low_delay",
        "-framedrop",
        "-strict", "experimental",
        "-vf", "setpts=PTS/1.0",
        "-i", "/dev/video0"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_picam_streaming():
    global picam_stream_proc, monitor_proc
    stop_all_streaming()
    print("🚀 PiCam 송출 시작")
    picam_stream_proc = subprocess.Popen([
        "ffmpeg",
        "-f", "v4l2",
        "-framerate", "30",
        "-video_size", "640x480",
        "-i", "/dev/video2",
        "-f", "mpegts",
        "udp://192.168.0.10:5000"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    monitor_proc = subprocess.Popen([
        "ffplay",
        "-fflags", "nobuffer",
        "-flags", "low_delay",
        "-framedrop",
        "-strict", "experimental",
        "-vf", "setpts=PTS/1.0",
        "-i", "/dev/video2"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_all_streaming():
    global usb_stream_proc, picam_stream_proc, monitor_proc
    print("🛑 모든 스트리밍 및 모니터 중단")
    for proc in [usb_stream_proc, picam_stream_proc, monitor_proc]:
        if proc:
            proc.terminate()
    usb_stream_proc = None
    picam_stream_proc = None
    monitor_proc = None
    close_cameras()
