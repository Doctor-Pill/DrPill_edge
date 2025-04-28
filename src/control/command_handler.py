# 📍 DrPill_edge/src/command_handler.py

from src.control.browser_controller import open_browser, close_browser
from src.control.camera_controller import (
    open_cameras,
    close_cameras,
    start_usb_streaming,
    start_picam_streaming,
    stop_all_streaming
)

def handle_command(command):
    if command == "open_browser":
        open_browser()
    elif command == "close_browser":
        close_browser()
    elif command == "open_cameras":
        open_cameras()
    elif command == "close_cameras":
        close_cameras()
    elif command == "start_usb_streaming":
        start_usb_streaming()
    elif command == "start_picam_streaming":
        start_picam_streaming()
    elif command == "stop_streaming":
        stop_all_streaming()
    else:
        print(f"⚠️ 알 수 없는 명령: {command}")
