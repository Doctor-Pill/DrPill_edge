from src.control.camera_controller import (
    open_camera_usb,
    open_camera_pi,
    start_monitor_and_stream,
    stop_monitor_and_stream
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
    elif command == "start_monitor_and_stream":
        start_monitor_and_stream()
    elif command == "stop_monitor_and_stream":
        stop_monitor_and_stream()
    else:
        print(f"⚠️ 알 수 없는 명령: {command}")