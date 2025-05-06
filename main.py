# 📍 DrPill_edge/main.py

import sys
import os
import src.control.pill_drop_and_capture as sc

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from connection.socket_client import connect_to_server
from control.browser_controller import open_browser, close_browser
import atexit

def main():
    open_browser()
    atexit.register(cleanup)
    connect_to_server()

def cleanup():
    close_browser()
    from control.camera_controller import cleanup_all
    cleanup_all()
    sc.cleanup()

if __name__ == "__main__":
    main()
