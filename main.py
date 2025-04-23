from src.utils.recorder import record_audio
from src.utils.uploader import upload_audio_file

FILENAME = "my_voice.wav"

print("🎙 5초 동안 녹음을 시작합니다...")
record_audio(FILENAME)
print(f"✅ 녹음 완료: {FILENAME}")

print("📡 서버로 파일 전송 중...")
res = upload_audio_file(FILENAME)
print("✅ 서버 응답:", res.status_code)
