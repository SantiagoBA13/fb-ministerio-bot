# src/post_facebook.py
import requests

GRAPH = "https://graph.facebook.com/v19.0"

def post_photo(page_id: str, access_token: str, image_path: str, caption: str) -> dict:
    url = f"{GRAPH}/{page_id}/photos"
    with open(image_path, "rb") as f:
        files = {"source": f}
        data = {"caption": caption, "access_token": access_token}
        r = requests.post(url, files=files, data=data, timeout=120)
    r.raise_for_status()
    return r.json()
