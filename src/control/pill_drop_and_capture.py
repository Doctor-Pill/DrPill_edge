import RPi.GPIO as GPIO
import subprocess
import time
import threading
import os
from datetime import datetime

# ========== 설정 ==========
SERVO_PIN = 18
REMOTE_USER = "piai"
REMOTE_IP = "192.168.0.10"
REMOTE_PATH = "/home/piai/pic"

# ========== 초기화 ==========
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

# ========== 유틸 함수 ==========
def set_angle(angle):
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)

def operate_servo():
    print("▶️ 서보모터 작동")
    set_angle(60)
    time.sleep(1)
    set_angle(105)
    time.sleep(0.5)
    set_angle(60)
    print("✅ 서보모터 작동 완료")

def cleanup():
    pwm.stop()
    GPIO.cleanup()
    print("🧹 GPIO 정리 완료")

def generate_filename():
    now = datetime.now()
    return now.strftime("pic/snapshot_%Y%m%d_%H%M%S.jpg")

def take_photo(filename, preview_time_ms):
    print(f"📸 {preview_time_ms}ms 미리보기 후 사진 촬영 → {filename}")
    subprocess.run([
        "libcamera-still",
        "--autofocus-mode", "auto",
        "--autofocus-on-capture", "1",
        "-t", str(preview_time_ms),
        "-o", filename
    ], env={**os.environ, "DISPLAY": ":0"})
    print("✅ 사진 저장 완료")

def send_photo(filename):
    print(f"📤 {filename} 전송 중...")
    subprocess.run([
        "scp", filename, f"{REMOTE_USER}@{REMOTE_IP}:{REMOTE_PATH}"
    ])
    print("✅ 전송 완료")

# ========== 핵심 함수 ==========
def drop_pill_and_capture(delay_before_servo=1000, delay_after_servo=1000, send=False):
    """
    :param delay_before_servo: 사진 미리보기 시작 후 → 서보모터 작동까지 기다릴 시간 (ms)
    :param delay_after_servo: 서보모터 작동 후 → 사진 촬영까지 기다릴 시간 (ms)
    :param send: True이면 촬영한 사진을 전송
    """
    filename = generate_filename()
    total_preview_time = delay_before_servo + delay_after_servo + 2000

    def servo_sequence():
        time.sleep(delay_before_servo / 1000.0)
        operate_servo()
        time.sleep(delay_after_servo / 1000.0)

    thread = threading.Thread(target=servo_sequence)
    thread.start()

    take_photo(filename, total_preview_time)

    thread.join()

    if send:
        send_photo(filename)
    return filename

# ========== 실행 예시 ==========
if __name__ == "__main__":
    try:
        drop_pill_and_capture(
            delay_before_servo=2500,  # 미리보기 후 2.5초 뒤 서보 작동
            delay_after_servo=2000,   # 서보 작동 후 2초 뒤 사진 촬영
            send=True
        )
    finally:
        cleanup()
