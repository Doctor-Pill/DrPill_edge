import requests

def send_audio(filepath: str):
    url = 'http://192.168.0.10:5000/upload_audio'  # 서버 주소에 맞게 수정
    print(f"📡 서버로 파일 전송 중: {filepath}")
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (filepath, f, 'audio/wav')}
            response = requests.post(url, files=files)
        print(f"✅ 서버 응답: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")
