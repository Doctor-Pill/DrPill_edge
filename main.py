from src.utils.recorder import record_audio
from src.signal.sender import send_audio

if __name__ == '__main__':
    filename = 'my_voice.wav'
    record_audio(filename=filename, duration=5)
    send_audio(filename)
