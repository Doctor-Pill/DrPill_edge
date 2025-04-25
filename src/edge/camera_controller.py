# 📍 DRPILL_EDGE/src/edge/camera_controller.py

import subprocess
from src.config.settings import SERVER_IP, SERVER_PORT, WIDTH, HEIGHT, FRAMERATE, USE_H264

# 글로벌 변수로 ffmpeg 프로세스를 관리
streaming_proc = None

def start_streaming():
    """
    ffmpeg를 이용하여 Pi Camera 스트리밍 시작
    """
    global streaming_proc

    if streaming_proc is not None:
        print("ℹ️ 이미 스트리밍이 진행 중입니다.")
        return

    if USE_H264:
        camera_cmd = (
            f"libcamera-vid -t 0 "
            f"--width {WIDTH} --height {HEIGHT} --framerate {FRAMERATE} "
            f"--codec h264 --profile high --inline --flush --nopreview "
            f"-o -"
        )

        ffmpeg_cmd = (
            f"ffmpeg -f h264 -i - "
            f"-f mpegts udp://{SERVER_IP}:{SERVER_PORT}"
        )

    else:
        camera_cmd = (
            f"libcamera-vid -t 0 "
            f"--width {WIDTH} --height {HEIGHT} --framerate {FRAMERATE} "
            f"--codec yuv420 --inline --flush --nopreview "
            f"-o -"
        )

        ffmpeg_cmd = (
            f"ffmpeg -f rawvideo -pix_fmt yuv420p -s {WIDTH}x{HEIGHT} -r {FRAMERATE} -i - "
            f"-fflags nobuffer -flags low_delay "
            f"-f mpegts udp://{SERVER_IP}:{SERVER_PORT}"
        )

    full_cmd = f"{camera_cmd} | {ffmpeg_cmd}"

    print("📸 스트리밍 시작...")
    streaming_proc = subprocess.Popen(full_cmd, shell=True, executable='/bin/bash')

def stop_streaming():
    """
    스트리밍 중지
    """
    global streaming_proc

    if streaming_proc is not None:
        print("🛑 스트리밍 중단...")
        streaming_proc.terminate()
        streaming_proc = None
    else:
        print("ℹ️ 현재 스트리밍이 진행 중이지 않습니다.")
