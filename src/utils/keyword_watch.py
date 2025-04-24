import queue
import sounddevice as sd
import vosk
import json
import threading

class KeywordWatcher:
    def __init__(self, keywords=None, rate=16000):
        if keywords is None:
            keywords = ["hello"]
        self.keywords = [k.lower().replace(" ", "") for k in keywords]
        self.model = vosk.Model("model-en")
        self.recognizer = vosk.KaldiRecognizer(self.model, rate)
        self.q = queue.Queue()
        self.running = threading.Event()
        self.callback = None
        self.rate = rate


    def set_callback(self, callback):
        self.callback = callback

    def _callback_func(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def _watch_loop(self):
        with sd.RawInputStream(samplerate=self.rate, blocksize=2000, dtype='int16',
                               channels=1, callback=self._callback_func):
            print(f"🎧 '{self.keyword}' 감지 대기 중...")
            while self.running.is_set():
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").replace(" ", "").lower()
                    print("🗣 인식된 텍스트:", text)

                    if any(kw in text for kw in self.keywords):
                        print("🎯 키워드 감지됨!")
                        if self.callback:
                            self.callback()


    def start(self):
        self.running.set()
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running.clear()
        self.thread.join()
