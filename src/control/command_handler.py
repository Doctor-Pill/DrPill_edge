# 📍 DrPill_edge/src/command_handler.py

from src.control.browser_controller import (
    open_browser,
    close_browser
)
from src.control.camera_controller import (
    start_usb_streaming,
    start_picam_streaming,
    stop_all_streaming
)
from src.control.pill_drop_and_capture import drop_pill_and_capture

def handle_command(data):
    print(data)
    command = data.get("command")

    if command == "open_browser":
        open_browser()
    elif command == "close_browser":
        close_browser()
    elif command == "start_usb_streaming":
        start_usb_streaming()
    elif command == "start_picam_streaming":
        start_picam_streaming()
    elif command == "stop_streaming":
        stop_all_streaming()
    elif command == "operate_servo":
        drop_pill_and_capture(
        delay_before_servo=2500,
        delay_after_servo=2000,
        send=False
    )

    else:
        print(f"⚠️ 알 수 없는 명령: {command}")