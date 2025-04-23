import socketio
import subprocess

sio = socketio.Client()

@sio.event
def connect():
    print("🌐 서버에 WebSocket으로 연결되었습니다.")

@sio.event
def disconnect():
    print("🔌 서버와의 연결이 끊어졌습니다.")

def connect_to_server():
    try:
        sio.connect("http://192.168.0.10:5000")
        print("✅ WebSocket 연결 시도 완료")

        # 브라우저도 띄우기 (백그라운드)
        subprocess.Popen([
            "chromium-browser", "--kiosk", "http://192.168.0.10:5000", "--no-sandbox"
        ])
        print("🌐 브라우저 띄우기 완료")

    except Exception as e:
        print(f"❌ 서버 접속 실패: {e}")
