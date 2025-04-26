# # 📍 DRPILL_EDGE/src/config/settings.py

# # 서버 연결 정보
# SERVER_IP = '192.168.0.10'    # 워크스테이션(서버) IP
# SERVER_PORT = 5000            # 워크스테이션(서버) 포트

# # 스트리밍 설정
# WIDTH = 1280                 # 영상 가로 해상도
# HEIGHT = 720                 # 영상 세로 해상도
# FRAMERATE = 30               # 프레임레이트

# # Pi Camera H264 인코딩 사용 여부
# USE_H264 = True


# 📍 DRPILL_EDGE/src/config/settings.py

# 서버 연결 정보
SERVER_IP = '192.168.0.10'    # 워크스테이션(서버) IP
SERVER_PORT = 5000            # 워크스테이션(서버) 포트

# 스트리밍 설정
WIDTH = 1920                 # 🔥 Full HD 영상 가로 해상도
HEIGHT = 1080                # 🔥 Full HD 영상 세로 해상도
FRAMERATE = 30               # 🔥 초당 30프레임 (최고 화질 안정)

# Pi Camera H264 인코딩 사용 여부
USE_H264 = True              # 🔥 Pi Camera H264 인코딩 사용 (압축률 & 품질 최적화)
