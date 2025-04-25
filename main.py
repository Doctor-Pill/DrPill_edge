from src.camera.camera_streamer import CameraStreamer

# 서버 주소 설정 (워크스테이션 IP)
SERVER_URL = "http://192.168.0.10:5000"

# 실행
if __name__ == '__main__':
    streamer = CameraStreamer(server_url=SERVER_URL)
    streamer.run_forever()
