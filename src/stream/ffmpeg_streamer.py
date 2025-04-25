import subprocess
from .config import SERVER_IP, SERVER_PORT, WIDTH, HEIGHT, FRAMERATE, CAMERA_INDEX

def start_streaming():
    """
    라즈베리파이의 카메라를 캡처해서 ffmpeg를 통해 서버로 스트리밍하는 함수
    """

    command = [
        'ffmpeg',
        '-f', 'v4l2',              # 비디오 캡처 장치 포맷
        '-framerate', str(FRAMERATE),
        '-video_size', f'{WIDTH}x{HEIGHT}',
        '-i', f'/dev/video{CAMERA_INDEX}',  # 라즈베리파이 카메라 장치
        '-f', 'mpegts',            # 전송할 포맷: MPEG-TS (빠르고 손쉬움)
        f'udp://{SERVER_IP}:{SERVER_PORT}'  # UDP로 서버로 전송
    ]

    print(f"[INFO] Starting FFmpeg streaming to udp://{SERVER_IP}:{SERVER_PORT}...")
    process = subprocess.Popen(command)

    return process
