import speech_recognition as sr

def listen(timeout: int = 5, phrase_time_limit: int = 5) -> str | None:
    """
    실시간으로 마이크 입력을 받아 음성을 텍스트로 변환합니다.

    :param timeout: 말을 시작할 때까지 대기 시간 (초)
    :param phrase_time_limit: 말할 수 있는 최대 시간 (초)
    :return: 인식된 텍스트 또는 None
    """
    recognizer = sr.Recognizer()

    try:
        # 디바이스 인덱스를 명시하고 싶다면:
        # with sr.Microphone(device_index=3) as source:
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
