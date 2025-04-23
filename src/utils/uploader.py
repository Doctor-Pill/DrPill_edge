import requests

def upload_audio_file(filepath: str) -> requests.Response:
    url = "http://192.168.0.10:5000/upload"
    with open(filepath, "rb") as f:
        files = {"file": (filepath, f, "audio/wav")}
        response = requests.post(url, files=files)
    return response
