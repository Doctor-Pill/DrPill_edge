from src.camera.camera_streamer import CameraStreamer

def main():
    streamer = CameraStreamer()
    print("🔌 서버 연결 중...")
    streamer.connect()
    print("📸 프레임 전송 시작...")
    try:
        streamer.send_frames()
    except KeyboardInterrupt:
        print("🛑 전송 중단")
    finally:
        streamer.stop()

if __name__ == "__main__":
    main()
