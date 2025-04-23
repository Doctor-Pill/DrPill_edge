import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="my_voice.wav", duration=5, fs=44100):
    print("🎙 녹음 시작...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    write(filename, fs, audio)
    print(f"✅ 녹음 완료: {filename}")
