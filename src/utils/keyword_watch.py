# src/utils/keyword_watch.py

import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import threading
from src.utils.recorder import record_audio
from src.utils.uploader import upload_audio_file

class KeywordWatcher:
    def __init__(self, model_path="model-en", rate=16000):
        self.q = queue.Queue()
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, rate)
        self.running = threading.Event()
        self.thread = None
        self.rate = rate

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def _watch_loop(self):
        with sd.RawInputStream(samplerate=self.rate, blocksize=2000, dtype='int16',
                               channels=1, callback=self._callback):
            print("🎧 '닥터필' 키워드 감지 시작 (실시간)...")
            while self.running.is_set():
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").replace(" ", "").lower()
                    print("🎤 인식된 텍스트:", text)
                    if "doctorpill" in text:
                        print("🎯 'doctorpill' 감지! 녹음 실행")
                        record_audio("triggered.wav")
                        upload_audio_file("triggered.wav")


    def start(self):
        if self.thread and self.thread.is_alive():
            print("⚠️ 이미 감지 루프가 실행 중입니다.")
            return
        self.running.set()
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()

    def stop(self):
        if self.running.is_set():
            print("🛑 키워드 감지 루프 중단 중...")
            self.running.clear()
            self.thread.join()
        else:
            print("🔕 감지 루프는 이미 멈춰 있습니다.")
