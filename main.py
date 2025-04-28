# 📍 DrPill_edge/main.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 🔥 추가!

from src.connection.socket_client import connect_to_server
from src.control.browser_controller import open_browser

if __name__ == "__main__":
    open_browser()
    connect_to_server()
