import cv2
import base64
import socketio
import time

class CameraStreamer:
    def __init__(self, server_url):
        self.server_url = server_url
        self.sio = socketio.Client()
        self.video_active = False

        @self.sio.event
        def connect():
            print("✅ 서버에 연결됨")

        @self.sio.event
        def disconnect():
            print("❌ 서버와의 연결 끊김")

        @self.sio.on('start_video')
        def start_video():
            print("▶️ 영상 시작 신호 수신")
            self.video_active = True

        @self.sio.on('stop_video')
        def stop_video():
            print("⏹️ 영상 중단 신호 수신")
            self.video_active = False

    def run_forever(self):
        self.sio.connect(self.server_url)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("🚫 카메라를 열 수 없습니다.")
            return

        try:
            while True:
                if self.video_active:
                    ret, frame = cap.read()
                    if not ret:
                        continue

                    _, buffer = cv2.imencode('.jpg', frame)
                    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                    self.sio.emit('video_frame', jpg_as_text)

                time.sleep(0.2)  # 약 5 fps

        except KeyboardInterrupt:
            print("🧹 종료됨")
        finally:
            cap.release()
            self.sio.disconnect()
