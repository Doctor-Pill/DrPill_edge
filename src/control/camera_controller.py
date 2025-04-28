# 📍 DrPill_edge/src/control/camera_controller.py

import subprocess

usb_stream_proc = None
picam_stream_proc = None
def start_usb_streaming():
    global usb_stream_proc
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

def start_picam_streaming():
    global picam_stream_proc
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

def stop_all_streaming():
    global usb_stream_proc, picam_stream_proc
    if usb_stream_proc:
        print("🛑 USB캠 송출 중단")
        usb_stream_proc.terminate()
        usb_stream_proc = None
    if picam_stream_proc:
        print("🛑 PiCam 송출 중단")
        picam_stream_proc.terminate()
        picam_stream_proc = None

def cleanup_all():
    stop_all_streaming()
    print("✅ 모든 카메라 자원 정리 완료")