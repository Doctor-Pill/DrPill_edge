# 📁 DrPill_edge/src/signal/video_streaming.py

import cv2
import socketio
import time
import numpy as np

def run(device_path="/dev/video0", is_picam=False):
    print(f"🎥 디바이스 열기 시도: {device_path} (is_picam={is_picam})")

    # 카메라 열기
    if is_picam:
        gst_str = (
            "libcamerasrc ! "
            "video/x-raw,width=640,height=480,framerate=30/1 ! "
            "videoconvert ! "
            "appsink"
        )
        cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
    else:
        cap = cv2.VideoCapture(device_path)

    if not cap.isOpened():
        print(f"❌ 카메라 열기 실패: {device_path}")
        return
    print(f"✅ 카메라 열기 성공: {device_path}")

    # SocketIO 연결
    sio = socketio.Client()
    try:
        sio.connect("http://192.168.0.10:5000", namespaces=["/client"])
        print("✅ SocketIO 서버 연결 완료 (/client)")
    except Exception as e:
        print(f"❌ SocketIO 연결 실패: {e}")
        cap.release()
        return

    # MJPEG 디스플레이 설정
    cv2.namedWindow("Camera Stream", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Camera Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ 프레임 읽기 실패")
            time.sleep(0.1)
            continue

        # 화면 출력
        flipped = cv2.flip(frame, 1)
        cv2.imshow("Camera Stream", flipped)

        # 서버 전송
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        sio.emit("frame", buffer.tobytes(), namespace="/client")

        frame_count += 1
        if frame_count % 10 == 0:
            print(f"📤 전송된 프레임 수: {frame_count}")

        if cv2.waitKey(1) & 0xFF == 27:  # ESC 누르면 종료
            print("🛑 ESC 입력 → 종료")
            break

    cap.release()
    cv2.destroyAllWindows()
    sio.disconnect()
    print("✅ 카메라 및 서버 연결 종료 완료")
