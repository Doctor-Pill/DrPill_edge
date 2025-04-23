from src.signal.sender import send_signal
from src.utils.recorder import record_audio

if __name__ == '__main__':
    # print("📡 서버에 신호 전송 시도 중...")
    # send_signal()

    record_audio(filename='my_voice.wav', duration=4)