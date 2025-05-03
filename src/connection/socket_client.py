# 📍 DrPill_edge/src/connection/socket_client.py

import socketio
from control.command_handler import handle_command

SERVER_URL = "http://192.168.0.10:5000"

sio = socketio.Client()

@sio.event(namespace='/admin')
def connect():
    print("✅ 서버(/admin)에 연결되었습니다.")

@sio.event(namespace='/admin')
def disconnect():
    print("❌ 서버(/admin) 연결이 끊어졌습니다.")

@sio.on('edge_command', namespace='/admin')
def on_server_command(command_data):
    print(f"📩 서버로부터 명령 수신: {command_data}")
    handle_command(command_data)

def connect_to_server():
    try:
        sio.connect(SERVER_URL, namespaces=["/admin"])
        sio.wait()
    except Exception as e:
        print(f"❗ 서버 연결 실패: {e}")
