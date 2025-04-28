# 📍 DrPill_edge/src/connection/socket_client.py

import socketio
from src.config.settings import SERVER_URL
from src.control.command_handler import handle_command
from src.control.browser_controller import close_browser

# 비동기 Socket.IO 클라이언트
sio = socketio.Client()

@sio.event
def connect():
    print("✅ 서버에 연결되었습니다.")

@sio.event
def disconnect():
    print("❌ 서버 연결이 끊겼습니다. 브라우저 종료 후 프로그램 종료.")
    close_browser()
    exit(0)

@sio.on('command')
def on_command(data):
    print(f"📩 서버 명령 수신: {data}")
    handle_command(data)

def connect_to_server():
    try:
        sio.connect(SERVER_URL)
        sio.wait()
    except Exception as e:
        print(f"⚠️ 서버 연결 실패: {e}")
