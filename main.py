# 📍 DrPill_edge/main.py

from src.connection.socket_client import connect_to_server
from src.control.browser_controller import open_browser

if __name__ == "__main__":
    open_browser()  # 부팅되면 항상 브라우저 오픈
    connect_to_server()  # 서버 연결 및 명령 대기
