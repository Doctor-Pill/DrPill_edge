# 📍 DrPill_edge/src/control/camera_controller.py

import cv2
import socket
import threading

# 설정
device_usb = "/dev/video0"
device_pi = "/dev/video2"
target_ip = "192.168.0.10"
target_port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 스트리밍용 스레드 핸들러
tx_thread = None
stop_event = threading.Event()


def start_usb_streaming():
    start_streaming(device_usb)

def start_picam_streaming():
    start_streaming(device_pi)

def start_streaming(device_path):
    global tx_thread, stop_event

    stop_all_streaming()

    stop_event.clear()

    def streaming_loop():
        cap = cv2.VideoCapture(device_path)
        if not cap.isOpened():
            print(f"❌ 카메라 열기 실패: {device_path}")
            return

        print(f"✅ 카메라 열림: {device_path}")

        while not stop_event.is_set():
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
            try:
                sock.sendto(data, (target_ip, target_port))
            except Exception as e:
                print(f"❗ 송신 에러: {e}")

            # 'q' 눌러 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("🛑 카메라 스트리밍 종료")

    tx_thread = threading.Thread(target=streaming_loop)
    tx_thread.start()


def stop_all_streaming():
    global tx_thread, stop_event

    if tx_thread and tx_thread.is_alive():
        print("🛑 스트리밍 중단 요청")
        stop_event.set()
        tx_thread.join()

    tx_thread = None
    stop_event.clear()
