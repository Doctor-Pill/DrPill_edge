# 📍 command_handler.py

from src.control.camera_controller import (
    open_camera_usb,
    open_camera_pi,
    start_streaming,
    stop_streaming,
    close_camera
)
from src.control.browser_controller import open_browser, close_browser

def handle_command(command):
    if command == "open_browser":
        open_browser()
    elif command == "close_browser":
        close_browser()
    elif command == "open_camera_usb":
        open_camera_usb()
    elif command == "open_camera_pi":
        open_camera_pi()
    elif command == "start_streaming":
        start_streaming()
    elif command == "stop_streaming":
        stop_streaming()
    elif command == "close_camera":
        close_camera()
    else:
        print(f"⚠️ 알 수 없는 명령: {command}")
