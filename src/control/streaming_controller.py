import subprocess
import threading
import time

import socketio

sio = socketio.Client()
sio.connect('http://192.168.0.10:5000')  # 서버 IP와 포트에 맞게 수정

def notify_streaming_ready(name):
    sio.emit(f"{name.lower()}_streaming_ready")

ffmpeg_proc = None
monitor_thread = None
monitor_stop = False

def start_mpeg_stream(device_path, port):
    global ffmpeg_proc, monitor_thread, monitor_stop
    stop_mpeg_stream()
    print(f"📤 FFmpeg 송신 시작: {device_path} → 포트 {port}")
    ffmpeg_proc = subprocess.Popen([
        "ffmpeg",
        "-f", "v4l2",
        "-i", device_path,
        "-vcodec", "libx264",
        "-tune", "zerolatency",
        "-f", "mpegts",
        f"udp://192.168.0.10:{port}"
    # ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ])


    notify_streaming_ready("USB")

    # 상태 감시 시작
    monitor_stop = False
    monitor_thread = threading.Thread(target=_monitor_streaming, args=(port,), daemon=True)
    monitor_thread.start()

def _monitor_streaming(port):
    while not monitor_stop:
        print(f"📡 FFmpeg 송신 중... (→ 포트 {port})")
        time.sleep(1)  # 3초마다 출력

def stop_mpeg_stream():
    global ffmpeg_proc, monitor_thread, monitor_stop
    monitor_stop = True
    if monitor_thread:
        monitor_thread.join()
        monitor_thread = None

    if ffmpeg_proc and ffmpeg_proc.poll() is None:
        print("🛑 FFmpeg 송신 종료")
        ffmpeg_proc.terminate()
        ffmpeg_proc.wait()
    ffmpeg_proc = None
