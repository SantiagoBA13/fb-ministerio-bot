# src/post_video.py
import requests

GRAPH = "https://graph.facebook.com/v19.0"

def post_video(page_id: str, access_token: str, video_path: str, description: str) -> dict:
    url = f"{GRAPH}/{page_id}/videos"
    with open(video_path, "rb") as f:
        files = {"source": f}
        data = {"access_token": access_token, "description": description}
        r = requests.post(url, files=files, data=data, timeout=600)
    r.raise_for_status()
    return r.json()
