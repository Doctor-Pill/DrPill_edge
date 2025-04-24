from src.utils.keyword_watch import KeywordWatcher
from src.signal.cam_stream import start_video_streaming
import time

if __name__ == "__main__":
    watcher = KeywordWatcher()

    def on_detected():
        print("📸 영상 전송 시작")
        start_video_streaming()

    watcher.set_callback(on_detected)
    watcher.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()
        print("🛑 종료됨")


    # connect_to_server()
    # watcher = KeywordWatcher()

    # watcher.start()   # 감지 시작
    # time.sleep(60)    # 20초 동안 감지 유지
    # watcher.stop()    # 감지 종료

    # # time.sleep(10)
    # # watcher.start()   # 다시 시작도 가능
    # # time.sleep(60)
