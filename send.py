# 📍 src/stream/capture_and_send.py

import cv2
import socket
import struct
import threading

# 설정
DEVICE_USB = "/dev/video0"
DEVICE_PI = "/dev/video2"
TARGET_IP = "192.168.0.10"
TARGET_PORT = 5000

# UDP 소켓 열기
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def capture_and_send(device_path):
    cap = cv2.VideoCapture(device_path)

    if not cap.isOpened():
        print(f"❌ 카메라 열기 실패: {device_path}")
        return

    print(f"✅ 카메라 열림: {device_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ 프레임 읽기 실패")
            break

        # 화면 표시
        cv2.imshow('Camera Stream', frame)

        # 프레임을 인코딩 (jpg 압축)
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ret:
            continue

        # 서버로 전송
        data = buffer.tobytes()
        # UDP 전송 (주의: 큰 프레임은 쪼개야 함, 지금은 간단히 전송)
        try:
            sock.sendto(data, (TARGET_IP, TARGET_PORT))
        except Exception as e:
            print(f"❗ 송신 에러: {e}")

        # 키보드 'q' 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 예시: 웹캠 스트림 시작
if __name__ == "__main__":
    capture_and_send(DEVICE_USB)
