import subprocess
from datetime import datetime
import os

ms = "2000"
REMOTE_USER = "piai"                # ← 로컬 PC 사용자명
REMOTE_IP = "192.168.0.10"          # ← 로컬 PC IP 주소
REMOTE_PATH = "/home/piai/pic"      # ← 저장할 디렉터리

def generate_filename():
    now = datetime.now()
    return now.strftime("pic/snapshot_%Y%m%d_%H%M%S.jpg")

def take_photo(filename):
    print(f"📸 사진 촬영 중... → {filename}")
    subprocess.run([
        "libcamera-still",
        "--autofocus-mode", "auto",
        "--autofocus-on-capture", "1",
        "-t", ms,                 # 5초 미리보기 + 초점 조정
        "-o", filename
    ], env={**os.environ, "DISPLAY": ":0"})
    print(f"✅ 사진 저장 완료: {filename}")

def send_photo(filename):
    print(f"📤 {filename} 를 {REMOTE_USER}@{REMOTE_IP}로 전송 중...")
    subprocess.run([
        "scp", filename, f"{REMOTE_USER}@{REMOTE_IP}:{REMOTE_PATH}"
    ])
    print("✅ 전송 완료")

def main():
    filename = generate_filename()
    take_photo(filename)
    # send_photo(filename)

if __name__ == "__main__":
    main()
