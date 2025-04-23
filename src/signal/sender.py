import requests
from src.utils.timestamp import current_timestamp

def send_signal():
    url = 'http://192.168.0.10:5000/signal'  # 워크스테이션 IP로 수정
    data = {
        'event': 'user_arrived',
        'timestamp': current_timestamp()
    }

    try:
        response = requests.post(url, json=data)
        print(f"✅ 응답 코드: {response.status_code}")
        print(f"📨 응답 내용: {response.text}")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")
