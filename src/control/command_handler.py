# 📍 DrPill_edge/src/control/command_handler.py

from src.control.camera_controller import start_camera, stop_camera, capture_photo
from src.control.browser_controller import open_browser, close_browser

def handle_command(command):
    if command == "open_browser":
        open_browser()
    elif command == "close_browser":
        close_browser()
    elif command == "start_camera":
        start_camera()
    elif command == "stop_camera":
        stop_camera()
    elif command == "capture_photo":
        capture_photo()
    else:
        print(f"⚠️ 알 수 없는 명령: {command}")
