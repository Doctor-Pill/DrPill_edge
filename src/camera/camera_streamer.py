from picamera2 import Picamera2
import cv2, base64, time
import numpy as np
import socketio
from src.config import SERVER_URL

class CameraStreamer:
    def __init__(self):
        self.camera = Picamera2()
        self.camera.preview_configuration.main.size = (640, 480)
        self.camera.preview_configuration.main.format = "RGB888"
        self.camera.configure("preview")

        self.running = False
        self.sio = socketio.Client()
        self._bind_events()

    def _bind_events(self):
        @self.sio.event
        def connect():
            print("🔌 서버에 연결됨")

        @self.sio.event
        def disconnect():
            print("🛑 서버와 연결 종료")

        @self.sio.on('start_video')
        def on_start(data=None):
            print("▶️ 영상 전송 시작 명령 수신")
            self.running = True

        @self.sio.on('stop_video')
        def on_stop(data=None):
            print("⏹️ 영상 전송 중단 명령 수신")
            self.running = False

    def run_forever(self):
        self.sio.connect(SERVER_URL)
        self.camera.start()
        try:
            while True:
                if self.running:
                    frame = self.camera.capture_array()
                    encoded = self.encode_frame(frame)
                    self.sio.emit('video_frame', encoded)
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("🛑 종료 요청")
        finally:
            self.camera.stop()
            self.sio.disconnect()

    def encode_frame(self, frame: np.ndarray) -> str:
        _, jpeg = cv2.imencode('.jpg', frame)
        return base64.b64encode(jpeg.tobytes()).decode('utf-8')
