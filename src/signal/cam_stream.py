import cv2
import websocket
import threading
import time

ws = None
stream_thread = None
is_streaming = False

def send_video():
    global is_streaming, ws
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("🚫 카메라 열기 실패")
        return
    
    print("📸 카메라 송신 루프 시작")  # 이거 추가
    try:
        while is_streaming:
            ret, frame = cap.read()
            if not ret:
                print("🚫 프레임 캡처 실패")
                continue
            _, buffer = cv2.imencode('.jpg', frame)
            ws.send(buffer.tobytes(), opcode=websocket.ABNF.OPCODE_BINARY)
            print("➡️ 프레임 전송됨")  # 추가
            time.sleep(0.05)

    except Exception as e:
        print(f"❌ 전송 중 오류: {e}")
    finally:
        cap.release()
        if ws:
            ws.close()
        print("📷 스트리밍 종료됨")

def start_video_streaming():
    global is_streaming, ws, stream_thread
    if is_streaming:
        print("⚠️ 이미 스트리밍 중")
        return
    try:
        ws = websocket.WebSocket()
        ws.connect("ws://192.168.0.10:8765")
        is_streaming = True
        print("📡 WebSocket 연결됨")
        stream_thread = threading.Thread(target=send_video, daemon=True)
        stream_thread.start()
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
        is_streaming = False

def stop_video_streaming():
    global is_streaming
    if not is_streaming:
        print("⚠️ 스트리밍이 시작되지 않았습니다")
        return
    is_streaming = False
    print("🛑 스트리밍 중지 요청됨")
