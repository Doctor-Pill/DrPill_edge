# 📍 DrPill_edge/src/connection/socket_client.py

import socketio
from src.command_handler import handle_command

SERVER_URL = "http://192.168.0.10:5000"  # 서버 IP 주소 맞춰줘야 함

sio = socketio.Client()

@sio.event
def connect():
    print("✅ 서버에 연결되었습니다.")

@sio.event
def disconnect():
    print("❌ 서버 연결이 끊어졌습니다.")

@sio.on('server_command')
def on_server_command(data):
    command = data.get("command")
    print(f"📩 서버로부터 명령 수신: {command}")
    handle_command(command)

def connect_to_server():
    try:
        sio.connect(SERVER_URL)
        sio.wait()  # 연결 유지
    except Exception as e:
        print(f"❗ 서버 연결 실패: {e}")
