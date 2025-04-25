from picamera2 import Picamera2
import cv2, base64, websocket, time
import numpy as np
from src.config import SERVER_URL

class CameraStreamer:
    def __init__(self):
        self.camera = Picamera2()
        self.camera.preview_configuration.main.size = (640, 480)
        self.camera.preview_configuration.main.format = "RGB888"
        self.camera.configure("preview")
        self.ws = None
        self.running = False

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(SERVER_URL)

    def encode_frame(self, frame: np.ndarray) -> str:
        _, jpeg = cv2.imencode('.jpg', frame)
        return base64.b64encode(jpeg.tobytes()).decode('utf-8')

    def send_frames(self):
        self.camera.start()
        self.running = True
        try:
            while self.running:
                frame = self.camera.capture_array()
                base64_img = self.encode_frame(frame)
                self.ws.send(f'42[\"video_frame\",\"{base64_img}\"]')
                time.sleep(0.2)
        finally:
            self.camera.stop()
            self.ws.close()

    def stop(self):
        self.running = False
