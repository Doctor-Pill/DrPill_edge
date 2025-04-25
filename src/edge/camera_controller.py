import subprocess
import os
import signal
import atexit

from src.config.settings import SERVER_IP, SERVER_PORT, WIDTH, HEIGHT, FRAMERATE, USE_H264

vid_proc = None
ffmpeg_proc = None

def start_streaming():
    global vid_proc, ffmpeg_proc

    if ffmpeg_proc is not None:
        print("ℹ️ 이미 스트리밍이 진행 중입니다.")
        return

    print("📸 스트리밍 시작...")

    if USE_H264:
        vid_cmd = [
            "libcamera-vid", "-t", "0",
            "--width", str(WIDTH), "--height", str(HEIGHT),
            "--framerate", str(FRAMERATE),
            "--codec", "h264", "--profile", "high",
            "--inline", "--flush", "--nopreview",
            "-o", "-"
        ]
        ffmpeg_cmd = [
            "ffmpeg", "-f", "h264", "-i", "-",
            "-f", "mpegts", f"udp://{SERVER_IP}:{SERVER_PORT}"
        ]
    else:
        vid_cmd = [
            "libcamera-vid", "-t", "0",
            "--width", str(WIDTH), "--height", str(HEIGHT),
            "--framerate", str(FRAMERATE),
            "--codec", "yuv420",
            "--inline", "--flush", "--nopreview",
            "-o", "-"
        ]
        ffmpeg_cmd = [
            "ffmpeg", "-f", "rawvideo", "-pix_fmt", "yuv420p",
            "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FRAMERATE), "-i", "-",
            "-fflags", "nobuffer", "-flags", "low_delay",
            "-f", "mpegts", f"udp://{SERVER_IP}:{SERVER_PORT}"
        ]

    vid_proc = subprocess.Popen(vid_cmd, stdout=subprocess.PIPE)
    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=vid_proc.stdout)

def stop_streaming():
    global vid_proc, ffmpeg_proc

    if ffmpeg_proc is not None:
        print("🛑 스트리밍 중단...")
        try:
            ffmpeg_proc.terminate()
            ffmpeg_proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            ffmpeg_proc.kill()

        if vid_proc:
            try:
                vid_proc.terminate()
                vid_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                vid_proc.kill()

        vid_proc = None
        ffmpeg_proc = None
    else:
        print("ℹ️ 현재 스트리밍이 진행 중이지 않습니다.")

atexit.register(stop_streaming)
