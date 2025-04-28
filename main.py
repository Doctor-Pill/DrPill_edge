# 📍 DrPill_edge/main.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))  # 🔥 수정!

from connection.socket_client import connect_to_server
from control.browser_controller import open_browser

if __name__ == "__main__":
    open_browser()
    connect_to_server()
