# 📁 DrPill_edge/src/signal/video_streaming.py

import cv2
import socketio
import time
import numpy as np

def run(device_path="/dev/video0"):
    print(f"🎥 디바이스 열기: {device_path}")
    cap = cv2.VideoCapture(device_path)
    if not cap.isOpened():
        print(f"❌ 카메라 열기 실패: {device_path}")
        return

    print("🌐 서버에 SocketIO 연결 시도 중...")
    sio = socketio.Client()
    try:
        sio.connect("http://192.168.0.10:5000", namespaces=["/client"])
        print("✅ SocketIO 서버 연결 완료 (/client)")
    except Exception as e:
        print(f"❌ SocketIO 연결 실패: {e}")
        return

    cv2.namedWindow("Camera Stream", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Camera Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ 프레임 읽기 실패")
            continue

        # 로컬 디스플레이
        flipped = cv2.flip(frame, 1)
        cv2.imshow("Camera Stream", flipped)

        # 서버 전송
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        sio.emit("frame", buffer.tobytes(), namespace="/client")

        frame_count += 1
        if frame_count % 10 == 0:
            print(f"📤 전송된 프레임 수: {frame_count}")

        if cv2.waitKey(1) & 0xFF == 27:  # ESC로 종료
            print("🛑 ESC 입력, 스트리밍 종료")
            break

    cap.release()
    cv2.destroyAllWindows()
    sio.disconnect()
    print("✅ 스트리밍 및 서버 연결 종료 완료")
