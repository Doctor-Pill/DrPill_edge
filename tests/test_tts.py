from src.stt.stt_engine import listen

def test_stt():
    print("🎙️ 말해주세요. 인식 결과를 출력합니다.")
    result = listen()
    if result:
        print(f"📝 인식된 문장: {result}")
    else:
        print("🤔 아무 것도 인식되지 않았습니다.")

if __name__ == "__main__":
    test_stt()