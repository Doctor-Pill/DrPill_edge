import socketio
from control.command_handler import handle_command

SERVER_URL = "http://192.168.0.10:5000"

sio = socketio.Client()

@sio.event
def connect():
    print("✅ 서버에 연결되었습니다.")

@sio.event
def disconnect():
    print("❌ 서버 연결이 끊어졌습니다.")

@sio.on('edge_command')  # ✅ namespace 생략 (기본 / 로 연결됨)
def on_server_command(command_data):
    print(f"📩 서버로부터 명령 수신: {command_data}")
    handle_command(command_data)

def connect_to_server():
    try:
        sio.connect(SERVER_URL)  # ✅ namespace 명시 생략
        sio.wait()
    except Exception as e:
        print(f"❗ 서버 연결 실패: {e}")
