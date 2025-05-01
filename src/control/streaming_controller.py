import subprocess

ffmpeg_proc = None

def start_mpeg_stream(device_path, port):
    global ffmpeg_proc
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
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_mpeg_stream():
    global ffmpeg_proc
    if ffmpeg_proc and ffmpeg_proc.poll() is None:
        print("🛑 FFmpeg 송신 종료")
        ffmpeg_proc.terminate()
        ffmpeg_proc.wait()
    ffmpeg_proc = None
