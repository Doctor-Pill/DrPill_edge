# 📍 DrPill_edge/src/control/streaming_controller.py

import subprocess

stream_proc = None

def start_streaming():
    global stream_proc
    stop_streaming()
    try:
        stream_proc = subprocess.Popen([
            "ffmpeg",
            "-f", "v4l2",
            "-framerate", "30",
            "-video_size", "640x480",
            "-i", "/dev/video0",
            "-f", "mpegts",
            "udp://192.168.0.10:5000"  # 서버 IP 주소
        ])
        print("🚀 스트리밍 시작")
    except Exception as e:
        print(f"❌ 스트리밍 시작 실패: {e}")

def stop_streaming():
    global stream_proc
    if stream_proc:
        stream_proc.terminate()
        stream_proc = None
        print("🛑 스트리밍 중단")
