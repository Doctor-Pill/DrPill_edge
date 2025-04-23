from src.utils.keyword_watch import KeywordWatcher
from src.signal.client_ws import connect_to_server
import time

if __name__ == "__main__":
    connect_to_server()
    watcher = KeywordWatcher()

    watcher.start()   # 감지 시작
    time.sleep(30)    # 30초 동안 감지 유지
    watcher.stop()    # 감지 종료

    time.sleep(5)
    watcher.start()   # 다시 시작도 가능
