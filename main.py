from src.stream.ffmpeg_streamer import start_streaming

def main():
    process = start_streaming()

    try:
        # 스트리밍 유지
        process.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping streaming...")
        process.terminate()

if __name__ == "__main__":
    main()
