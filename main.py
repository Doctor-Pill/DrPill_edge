# 📍 DrPill_edge/main.py
import atexit

from src.connection.socket_client import connect_to_server
from src.control.browser_controller import open_browser, close_browser

open_browser()
atexit.register(close_browser)

if __name__ == "__main__":
    connect_to_server()
