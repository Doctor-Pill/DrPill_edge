import cv2
import websocket
import threading
import time

def send_video(ws):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("🚫 카메라 열기 실패")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            _, buffer = cv2.imencode('.jpg', frame)
            ws.send(buffer.tobytes(), opcode=websocket.ABNF.OPCODE_BINARY)
            time.sleep(0.05)  # 20 FPS
    except Exception as e:
        print(f"❌ 전송 중 오류: {e}")
    finally:
        cap.release()
        ws.close()
        print("📷 스트리밍 종료됨")

def start_video_streaming():
    try:
        ws = websocket.WebSocket()
        ws.connect("ws://192.168.0.10:8765")
        print("📡 WebSocket 연결됨")
        threading.Thread(target=send_video, args=(ws,), daemon=True).start()
    except Exception as e:
        print(f"❌ WebSocket 연결 실패: {e}")
