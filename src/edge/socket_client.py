# 📍 DRPILL_EDGE/src/edge/socket_client.py

import socketio
from src.config.settings import SERVER_IP, SERVER_PORT
from src.edge.camera_controller import start_streaming, stop_streaming

# SocketIO 클라이언트 생성
sio = socketio.Client()

# 서버 연결 완료 시
@sio.event
def connect():
    print("📡 서버에 연결되었습니다.")

# 서버로부터 start_video 이벤트 수신 시
@sio.on('start_video')
def on_start_video():
    print("▶️ 서버로부터 start_video 명령 수신 → 스트리밍 시작")
    start_streaming()

# 서버로부터 stop_video 이벤트 수신 시
@sio.on('stop_video')
def on_stop_video():
    print("⏹️ 서버로부터 stop_video 명령 수신 → 스트리밍 중단")
    stop_streaming()

# 서버 연결 끊겼을 때
@sio.event
def disconnect():
    print("❌ 서버와 연결이 끊어졌습니다.")

def connect_to_server():
    """
    서버에 연결하는 함수
    """
    try:
        sio.connect(f'http://{SERVER_IP}:{SERVER_PORT}')
        sio.wait()
    except Exception as e:
        print(f"⚠️ 서버 연결 실패: {e}")
