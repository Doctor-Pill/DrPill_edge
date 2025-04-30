import cv2
import socket
import os

# ===== 설정 =====
DEVICE_PATH = "/dev/video0"
TARGET_IP = "192.168.0.10"
TARGET_PORT = 5000

# GUI 출력 위해 설정
os.environ["DISPLAY"] = ":0"

# UDP 소켓 준비
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 카메라 열기
cap = cv2.VideoCapture(DEVICE_PATH)
if not cap.isOpened():
    print(f"❌ 카메라 열기 실패: {DEVICE_PATH}")
    exit(1)

cv2.namedWindow('Camera Stream', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Camera Stream', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

print("🚀 스트리밍 시작")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ 프레임 읽기 실패")
        break

    # 좌우 반전 + 해상도 고정
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (800, 480))

    # 화면 표시
    cv2.imshow("Camera Stream", frame)

    # UDP 전송
    ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    if ret:
        sock.sendto(buffer.tobytes(), (TARGET_IP, TARGET_PORT))

    # ESC 키 누르면 종료
    if cv2.waitKey(10) == 27:
        print("🛑 ESC 입력으로 종료")
        break

cap.release()
cv2.destroyAllWindows()
sock.close()
print("🧊 종료 완료")
