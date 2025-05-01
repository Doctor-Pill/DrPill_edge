# 📍 src/streaming/mjpeg_streamer.py
from flask import Flask, Response
import cv2
import sys

app = Flask(__name__)

device_path = sys.argv[1] if len(sys.argv) > 1 else "/dev/video0"
cap = cv2.VideoCapture(device_path)

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/stream.mjpg')
def stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8001
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
