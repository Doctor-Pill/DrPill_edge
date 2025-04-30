# 📍 DrPill_edge/src/control/camera_controller.py

import cv2
import socket
import subprocess
import os
import signal
import time
import multiprocessing

# ========== 설정 ==========
TARGET_IP = "192.168.0.10"  # 워크스테이션 IP
TARGET_PORT = 5000
DEVICE_USB = "/dev/video0"

# 환경 변수 설정 (GUI 디스플레이용)
os.environ["DISPLAY"] = ":0"

# ========== 통신 소켓 ==========
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ========== 점유 해제 유틸 ==========
def free_device(device_path):
    """다른 프로세스가 카메라 점유 중이면 강제 종료"""
    try:
        result = subprocess.check_output(["fuser", device_path])
        pids = result.decode().strip().split()
        for pid in pids:
            pid = int(pid)
            if pid == os.getpid():
                continue
            try:
                os.kill(pid, signal.SIGKILL)
                print(f"⚡ {device_path} 점유 중인 프로세스 {pid} 종료")
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ 종료 실패: {e}")
    except subprocess.CalledProcessError:
        print(f"✅ {device_path}는 점유되지 않음")

# ========== 카메라 열기 (재시도 포함) ==========
def try_open_camera(device_path, retries=2):
    for i in range(retries):
        cap = cv2.VideoCapture(device_path, cv2.CAP_V4L2)
        time.sleep(0.5)
        if cap.isOpened():
            print(f"✅ 카메라 열기 성공: {device_path}")
            return cap
        if i == 0:
            print(f"⚠️ 첫 시도 실패 → 점유 해제 시도: {device_path}")
            free_device(device_path)
    print(f"❌ 카메라 열기 실패: {device_path}")
    return None

# ========== 스트리밍 루프 (프로세스) ==========
def streaming_loop(device_path):
    print("🧪 스트리밍 프로세스 시작")
    cap = try_open_camera(device_path)
    if not cap or not cap.isOpened():
        print("❌ cap 열기 실패 후 루프 종료")
        return

    cv2.namedWindow("Camera Stream", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Camera Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ 프레임 읽기 실패")
            break

        frame = cv2.flip(frame, 1)  # 거울 모드
        cv2.imshow("Camera Stream", frame)

        # 영상 송신
        try:
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            sock.sendto(buffer.tobytes(), (TARGET_IP, TARGET_PORT))
        except Exception as e:
            print(f"❗ 송신 에러: {e}")

        key = cv2.waitKey(1)
        if key == 27:  # ESC
            print("🛑 ESC 눌림")
            break

    cap.release()
    cv2.destroyAllWindows()
    for _ in range(5):
        cv2.waitKey(1)
    time.sleep(0.5)
    print("🧊 스트리밍 프로세스 종료")

# ========== 프로세스 관리 ==========
stream_proc = None

def start_usb_streaming():
    global stream_proc
    stop_all_streaming()
    stream_proc = multiprocessing.Process(target=streaming_loop, args=(DEVICE_USB,))
    stream_proc.start()
    print("🚀 USB 스트리밍 시작됨")

def start_picam_streaming():
    print("⚠️ PiCam 스트리밍은 아직 구현되지 않았습니다.")

def stop_all_streaming():
    global stream_proc
    if stream_proc and stream_proc.is_alive():
        print("🛑 스트리밍 중단 요청")
        stream_proc.terminate()
        stream_proc.join()
        print("🧹 스트리밍 프로세스 종료됨")
    stream_proc = None
