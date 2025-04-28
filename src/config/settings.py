# 📍 DrPill_edge/src/config/settings.py

SERVER_IP = '192.168.0.10'
SERVER_PORT = 5000
SERVER_URL = f"ws://{SERVER_IP}:{SERVER_PORT}/client"

CAMERA_INDEX = 0  # 0번 USB 웹캠
USE_PI_CAMERA = False  # Pi Camera 사용할 경우 True로 설정 (향후 확장)
