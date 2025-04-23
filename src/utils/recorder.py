import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename='recorded.wav', duration=5, samplerate=16000):
    print(f"🎙 {duration}초 동안 녹음을 시작합니다...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    write(filename, samplerate, audio)
    print(f"✅ 녹음 완료: {filename}")
