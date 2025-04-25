import subprocess
from .config import SERVER_IP, SERVER_PORT, WIDTH, HEIGHT, FRAMERATE

def start_streaming():
    """
    libcamera-vid + ffmpeg 조합으로 영상 스트리밍 시작
    """

    command = (
        f"libcamera-vid -t 0 --width {WIDTH} --height {HEIGHT} --framerate {FRAMERATE} "
        f"--inline --codec yuv420 --flush --nopreview -o - | "
        f"ffmpeg -f rawvideo -pix_fmt yuv420p -s {WIDTH}x{HEIGHT} -r {FRAMERATE} -i - "
        f"-fflags nobuffer -flags low_delay -f mpegts udp://{SERVER_IP}:{SERVER_PORT}"
    )

    process = subprocess.Popen(command, shell=True, executable='/bin/bash')
    print(f"[INFO] Streaming to udp://{SERVER_IP}:{SERVER_PORT} with {WIDTH}x{HEIGHT}@{FRAMERATE}fps")
    return process
