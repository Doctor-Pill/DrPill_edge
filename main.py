from src.camera.camera_streamer import CameraStreamer

def main():
    streamer = CameraStreamer()
    streamer.run_forever()

if __name__ == "__main__":
    main()
