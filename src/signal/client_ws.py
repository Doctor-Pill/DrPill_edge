import websocket
import threading

ws = None

def connect_to_server():
    global ws

    def on_open(ws):
        print("🌐 서버에 WebSocket 연결됨")

    def on_close(ws, close_status_code, close_msg):
        print("🔌 서버 연결 종료")

    def on_error(ws, error):
        print(f"❌ WebSocket 오류: {error}")

    try:
        ws = websocket.WebSocketApp(
            "ws://192.168.0.10:8765",
            on_open=on_open,
            on_close=on_close,
            on_error=on_error
        )
        threading.Thread(target=ws.run_forever, daemon=True).start()
    except Exception as e:
        print(f"❌ WebSocket 연결 실패: {e}")
