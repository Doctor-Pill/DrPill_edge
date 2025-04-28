# 📍 DrPill_edge/src/control/camera_controller.py

import subprocess

# 프로세스 핸들 저장용
usb_stream_proc = None
picam_stream_proc = None
monitor_proc = None

# 안전하게 기존 libcamera 관련 프로세스 종료
import os
def kill_libcamera_processes():
    try:
        subprocess.run(["sudo", "killall", "-q", "libcamera-still", "libcamera-vid", "libcamera-raw", "libcamera-jpeg"], check=False)
    except Exception as e:
        print(f"⚠️ libcamera 프로세스 정리 실패: {e}")

# 모든 스트리밍 및 모니터 중단
def stop_all_streaming():
    global usb_stream_proc, picam_stream_proc, monitor_proc
    print("🛑 모든 스트리밍 및 모니터 중단")

    if usb_stream_proc:
        usb_stream_proc.terminate()
        usb_stream_proc = None

    if picam_stream_proc:
        picam_stream_proc.terminate()
        picam_stream_proc = None

    if monitor_proc:
        monitor_proc.terminate()
        monitor_proc = None

# USB캠 송출 시작
def start_usb_streaming():
    global usb_stream_proc, monitor_proc
    stop_all_streaming()
    kill_libcamera_processes()
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
        "-f", "v4l2",
        "-framerate", "30",
        "-video_size", "640x480",
        "-i", "/dev/video0"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# PiCam 송출 시작
def start_picam_streaming():
    global picam_stream_proc, monitor_proc
    stop_all_streaming()
    kill_libcamera_processes()
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
        "-f", "v4l2",
        "-framerate", "30",
        "-video_size", "640x480",
        "-i", "/dev/video2"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
