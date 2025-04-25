# 스트리밍 설정값을 모은 config 파일

# 서버(워크스테이션) 정보
SERVER_IP = "192.168.0.10"   # 영상 수신 서버 IP
SERVER_PORT = 5000           # 영상 수신 서버 포트 (UDP)

# 영상 캡처 설정 (Pi Camera용)
WIDTH = 1280                 # 영상 가로 해상도
HEIGHT = 720                 # 영상 세로 해상도
FRAMERATE = 30               # 초당 프레임 수

# 영상 품질 관련 설정
BRIGHTNESS = 0.0             # 밝기 조절 (-1.0 ~ 1.0)
CONTRAST = 1.0               # 대비 (1.0은 기본)
SHARPNESS = 1.0              # 선명도 (1.0은 기본)

# 인코딩 설정
USE_H264 = True              # True면 Pi Camera에서 h264 인코딩, False면 raw 스트림
