from src.stt.stt_engine import listen

if __name__ == '__main__':
    result = listen()
    if result:
        print("✅ 최종 인식 결과:", result)
