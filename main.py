from src.utils.keyword_watch import KeywordWatcher
from src.signal.cam_stream import start_video_streaming, stop_video_streaming
import time

if __name__ == "__main__":
    watcher = KeywordWatcher()
    watcher.on_start = start_video_streaming
    watcher.on_stop = stop_video_streaming
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
