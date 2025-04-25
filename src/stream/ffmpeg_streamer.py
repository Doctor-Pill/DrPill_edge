import subprocess
from .config import SERVER_IP, SERVER_PORT, WIDTH, HEIGHT, FRAMERATE, BRIGHTNESS, CONTRAST, SHARPNESS, USE_H264


def start_streaming():
    """
    Pi Camera V3에서 영상을 캡처하고, ffmpeg를 통해 UDP 스트림 전송.
    설정은 config.py에서 모두 관리.
    """

    if USE_H264:
        # H.264 하드웨어 인코딩 (CPU 부담 적고 화질 좋음)
        camera_cmd = (
            f"libcamera-vid -t 0 "
            f"--width {WIDTH} --height {HEIGHT} --framerate {FRAMERATE} "
            f"--codec h264 --profile high --inline --flush --nopreview "
            f"--brightness {BRIGHTNESS} --contrast {CONTRAST} --sharpness {SHARPNESS} "
            f"-o -"
        )

        ffmpeg_cmd = (
            f"ffmpeg -f h264 -i - "
            f"-f mpegts udp://{SERVER_IP}:{SERVER_PORT}"
        )

    else:
        # raw yuv420 방식 (CPU 부담 크지만 고급 튜닝 가능)
        camera_cmd = (
            f"libcamera-vid -t 0 "
            f"--width {WIDTH} --height {HEIGHT} --framerate {FRAMERATE} "
            f"--codec yuv420 --inline --flush --nopreview "
            f"--brightness {BRIGHTNESS} --contrast {CONTRAST} --sharpness {SHARPNESS} "
            f"-o -"
        )

        ffmpeg_cmd = (
            f"ffmpeg -f rawvideo -pix_fmt yuv420p -s {WIDTH}x{HEIGHT} -r {FRAMERATE} -i - "
            f"-fflags nobuffer -flags low_delay "
            f"-f mpegts udp://{SERVER_IP}:{SERVER_PORT}"
        )

    # 파이프라인 조합
    full_command = f"{camera_cmd} | {ffmpeg_cmd}"

    print(f"[INFO] Streaming started → udp://{SERVER_IP}:{SERVER_PORT} ({WIDTH}x{HEIGHT}@{FRAMERATE}fps)")
    process = subprocess.Popen(full_command, shell=True, executable="/bin/bash")

    return process
