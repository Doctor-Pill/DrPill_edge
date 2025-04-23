import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def record_audio(filename='recorded.wav', duration=5, samplerate=16000):
    """
    마이크로부터 오디오를 녹음하고 WAV 파일로 저장합니다.

    :param filename: 저장할 파일명
    :param duration: 녹음 길이 (초)
    :param samplerate: 샘플링 레이트 (Hz)
    """
    print(f"🎙 {duration}초 동안 녹음을 시작합니다...")
    try:
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()  # 녹음 완료까지 대기
        write(filename, samplerate, audio)
        print(f"✅ 녹음 완료: {filename}")
    except Exception as e:
        print(f"❌ 녹음 중 오류 발생: {e}")


record_audio(filename='my_voice.wav', duration=4)
