import os
import cv2
import subprocess
import signal
import time
import multiprocessing

from src.signal import video_sender  # ✅ SocketIO 프레임 전송용

# ========== 설정 ==========
DEVICE_USB = "/dev/video2"
DEVICE_PICAM = "/dev/video0"

PICAM_PREVIEW_COMMAND = [
    "libcamera-vid",
    "--fullscreen",
    "--hflip",
    "--width", "800",
    "--height", "480",
    "-t", "0"
]

os.environ["DISPLAY"] = ":0"

# ========== 전역 프로세스 ==========
stream_proc = None
picam_proc = None
socket_stream_proc = None  # ✅ SocketIO 스트리밍용 프로세스

# ========== 유틸 ==========
def free_device(device_path):
    try:
        result = subprocess.check_output(["fuser", device_path])
        pids = result.decode().strip().split()
        for pid in pids:
            if int(pid) != os.getpid():
                os.kill(int(pid), signal.SIGKILL)
                print(f"⚡ {device_path} 점유 중인 프로세스 {pid} 종료")
                time.sleep(1)
    except subprocess.CalledProcessError:
        print(f"✅ {device_path}는 점유되지 않음")

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

# ========== 로컬 스트리밍 루프 ==========
def streaming_loop(device_path):
    print("🧪 MJPEG 스트리밍 프로세스 시작")
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

        frame = cv2.flip(frame, 1)
        cv2.imshow("Camera Stream", frame)

        if cv2.waitKey(1) == 27:
            print("🛑 ESC 눌림")
            break

    cap.release()
    cv2.destroyAllWindows()
    time.sleep(0.5)
    print("🧊 스트리밍 루프 종료")

# ========== 스트리밍 시작/중지 ==========
def start_streaming(device_path, label, is_picam=False):
    global stream_proc, picam_proc, socket_stream_proc
    stop_all_streaming()

    print(f"🚀 {label} 로컬 MJPEG 디스플레이 시작")
    stream_proc = multiprocessing.Process(target=streaming_loop, args=(device_path,))
    stream_proc.start()

    print(f"📤 {label} SocketIO 영상 송신 시작")
    socket_stream_proc = multiprocessing.Process(target=video_sender.run, args=(device_path,))
    socket_stream_proc.start()

    if is_picam:
        print(f"🚀 {label} libcamera 미리보기 실행")
        picam_proc = subprocess.Popen(
            PICAM_PREVIEW_COMMAND,
            env={
                "DISPLAY": ":0",
                "XAUTHORITY": f"/home/{os.getlogin()}/.Xauthority",
                **os.environ
            }
        )

def start_usb_streaming():
    start_streaming(DEVICE_USB, "USB")

def start_picam_streaming():
    start_streaming(DEVICE_PICAM, "PiCam", is_picam=True)

def stop_all_streaming():
    global stream_proc, picam_proc, socket_stream_proc

    print("🛑 스트리밍 종료 요청")

    if stream_proc and stream_proc.is_alive():
        stream_proc.terminate()
        stream_proc.join()
        print("🛑 로컬 스트리밍 중단")
    stream_proc = None

    if socket_stream_proc and socket_stream_proc.is_alive():
        socket_stream_proc.terminate()
        socket_stream_proc.join()
        print("🛑 SocketIO 송신 중단")
    socket_stream_proc = None

    if picam_proc and picam_proc.poll() is None:
        picam_proc.terminate()
        picam_proc.wait()
        print("🛑 PiCam 미리보기 중단")
    picam_proc = None
