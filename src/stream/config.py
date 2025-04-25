# 스트리밍 설정값을 모은 config 파일

# 서버(워크스테이션) 정보
SERVER_IP = "192.168.0.10"   # 영상 수신 서버 IP
SERVER_PORT = 5000           # 영상 수신 서버 포트 (UDP)

# 영상 캡처 설정 (Pi Camera용)
WIDTH = 1920                 # 영상 가로 해상도 (1920/2304)
HEIGHT = 1080                 # 영상 세로 해상도 (1080/1296)
FRAMERATE = 30               # 초당 프레임 수 (30)

# 영상 품질 관련 설정
BRIGHTNESS = 0.0             # 밝기 조절 (-1.0 ~ 1.0)
CONTRAST = 1.0               # 대비 (1.0은 기본)
SHARPNESS = 1.0              # 선명도 (1.0은 기본)

# 인코딩 설정
USE_H264 = True              # Pi 카메라에서 하드웨어 인코딩 사용 여부

# 낮은 지연을 위한 추가 ffmpeg 송신 설정
FFMPEG_PROBESIZE = 32        # 분석 버퍼 크기 줄이기 (기본: 5MB → 32 byte)
FFMPEG_ANALYZE_DURATION = 0  # 분석 시간 제거
