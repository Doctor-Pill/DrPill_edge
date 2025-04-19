import speech_recognition as sr

def listen(timeout: int = 5, phrase_time_limit: int = 5) -> str | None:
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 말해주세요 (녹음 중)...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        print("🧠 인식 중...")
        text = recognizer.recognize_google(audio, language="ko-KR")
        print("📝 인식된 내용:", text)
        return text

    except sr.UnknownValueError:
        print("❌ 인식 실패: 말을 이해하지 못했어요.")
    except sr.RequestError as e:
        print(f"❌ 요청 실패: {e}")
    except Exception as e:
        print(f"❌ 예외 발생: {e}")
    
    return None
