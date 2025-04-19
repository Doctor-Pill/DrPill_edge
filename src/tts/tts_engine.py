from gtts import gTTS
import tempfile
import os
import subprocess

def speak(text: str, lang: str = "ko"):
    print(f"[gTTS] 말하기: {text}")
    tts = gTTS(text=text, lang=lang)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        subprocess.run(["mpg123", fp.name])
        os.remove(fp.name)
