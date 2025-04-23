import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("🌐 서버에 WebSocket으로 연결되었습니다.")

@sio.event
def disconnect():
    print("🔌 서버와의 연결이 끊어졌습니다.")

@sio.event
def connect_error(data):
    print("❌ 서버 연결 중 오류 발생:", data)

def connect_to_server():
    try:
        sio.connect("http://192.168.0.10:5000")
        print("✅ WebSocket 연결 시도 완료")
    except Exception as e:
        print(f"❌ 서버 접속 실패: {e}")
