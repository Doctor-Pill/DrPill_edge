import subprocess
from .config import (
    SERVER_IP, SERVER_PORT,
    WIDTH, HEIGHT, FRAMERATE,
    BRIGHTNESS, CONTRAST, SHARPNESS,
    USE_H264, FFMPEG_PROBESIZE, FFMPEG_ANALYZE_DURATION
)

def start_streaming():
    """
    Pi Camera → ffmpeg 송출까지의 초저지연 스트리밍 실행
    """

    if USE_H264:
        camera_cmd = (
            f"libcamera-vid -t 0 "
            f"--width {WIDTH} --height {HEIGHT} --framerate {FRAMERATE} "
            f"--codec h264 --profile high --inline --flush --nopreview "
            f"--brightness {BRIGHTNESS} --contrast {CONTRAST} --sharpness {SHARPNESS} "
            f"-o -"
        )

        ffmpeg_cmd = (
            f"ffmpeg -f h264 -probesize {FFMPEG_PROBESIZE} -analyzeduration {FFMPEG_ANALYZE_DURATION} "
            f"-i - -fflags nobuffer -flags low_delay "
            f"-f mpegts udp://{SERVER_IP}:{SERVER_PORT}"
        )

    else:
        camera_cmd = (
            f"libcamera-vid -t 0 "
            f"--width {WIDTH} --height {HEIGHT} --framerate {FRAMERATE} "
            f"--codec yuv420 --inline --flush --nopreview "
            f"--brightness {BRIGHTNESS} --contrast {CONTRAST} --sharpness {SHARPNESS} "
            f"-o -"
        )

        ffmpeg_cmd = (
            f"ffmpeg -f rawvideo -pix_fmt yuv420p -s {WIDTH}x{HEIGHT} -r {FRAMERATE} "
            f"-probesize {FFMPEG_PROBESIZE} -analyzeduration {FFMPEG_ANALYZE_DURATION} "
            f"-i - -fflags nobuffer -flags low_delay "
            f"-f mpegts udp://{SERVER_IP}:{SERVER_PORT}"
        )

    full_cmd = f"{camera_cmd} | {ffmpeg_cmd}"
    print(f"[INFO] Streaming to udp://{SERVER_IP}:{SERVER_PORT} ({WIDTH}x{HEIGHT}@{FRAMERATE}fps)")
    process = subprocess.Popen(full_cmd, shell=True, executable="/bin/bash")
    return process
