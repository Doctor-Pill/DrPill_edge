# 📍 DrPill_edge/src/control/browser_controller.py

import subprocess

browser_proc = None

def open_browser():
    global browser_proc
    try:
        browser_proc = subprocess.Popen([
            "chromium-browser",
            "--noerrdialogs",
            "--kiosk",
            "http://192.168.0.10:5000/client"
        ])
        print("🚀 엣지 브라우저 실행 (키오스크 모드)")
    except Exception as e:
        print(f"❌ 브라우저 실행 실패: {e}")

def close_browser():
    global browser_proc
    if browser_proc:
        try:
            browser_proc.terminate()
            subprocess.run(["pkill", "-f", "chromium.*kiosk"], stdout=subprocess.DEVNULL)
            print("🛑 엣지 브라우저 종료 완료")
        except Exception as e:
            print(f"❌ 브라우저 종료 실패: {e}")
