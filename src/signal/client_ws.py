import socketio

def connect_to_server():
    sio = socketio.Client()

    @sio.event
    def connect():
        print("🌐 서버에 WebSocket으로 연결되었습니다.")

    @sio.event
    def disconnect():
        print("🔌 서버와의 연결이 끊어졌습니다.")

    try:
        sio.connect("http://192.168.0.10:5000")
    except Exception as e:
        print(f"❌ 서버 접속 실패: {e}")
