from src.tts.tts_engine import speak

def test_tts():
    text = input("🗣️ 읽을 문장을 입력하세요: ")
    speak(text)

if __name__ == "__main__":
    test_tts()