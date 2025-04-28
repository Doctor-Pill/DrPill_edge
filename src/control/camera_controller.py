# 📍 DrPill_edge/src/control/camera_controller.py

import subprocess

# 글로벌 변수로 관리
usb_monitor_proc = None
usb_stream_proc = None

picam_monitor_proc = None
picam_stream_proc = None

def stop_all_streaming():
    global usb_monitor_proc, usb_stream_proc
    global picam_monitor_proc, picam_stream_proc

    for proc in [usb_monitor_proc, usb_stream_proc, picam_monitor_proc, picam_stream_proc]:
        if proc:
            proc.terminate()

    print("🛑 모든 스트리밍 및 모니터 중단")

    usb_monitor_proc = None
    usb_stream_proc = None
    picam_monitor_proc = None
    picam_stream_proc = None

def start_usb_streaming():
    global usb_monitor_proc, usb_stream_proc
    stop_all_streaming()

    print("🚀 USB캠 송출 시작")

    # 모니터 띄우기
    usb_monitor_proc = subprocess.Popen([
        "ffplay",
        "-fflags", "nobuffer",
        "-flags", "low_delay",
        "-framedrop",
        "-strict", "experimental",
        "-vf", "scale=640:480",
        "/dev/video0"  # USB캠
    ])
    # ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    

    # 서버 송출
    usb_stream_proc = subprocess.Popen([
        "ffmpeg",
        "-f", "v4l2",
        "-framerate", "30",
        "-video_size", "640x480",
        "-i", "/dev/video0",
        "-f", "mpegts",
        "udp://192.168.0.10:5000"  # 서버 IP
    ])

def start_picam_streaming():
    global picam_monitor_proc, picam_stream_proc
    stop_all_streaming()

    print("🚀 PiCam 송출 시작")

    # 모니터 띄우기
    picam_monitor_proc = subprocess.Popen([
        "ffplay",
        "-fflags", "nobuffer",
        "-flags", "low_delay",
        "-framedrop",
        "-strict", "experimental",
        "-vf", "scale=640:480",
        "/dev/video2"  # PiCam
    ])

    # 서버 송출
    picam_stream_proc = subprocess.Popen([
        "ffmpeg",
        "-f", "v4l2",
        "-framerate", "30",
        "-video_size", "640x480",
        "-i", "/dev/video2",
        "-f", "mpegts",
        "udp://192.168.0.10:5000"  # 서버 IP
    ])
