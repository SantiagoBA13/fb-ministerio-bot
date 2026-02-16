# src/daily_video_slot.py
import datetime

def pick_video_slot(date_utc: datetime.date | None = None) -> str:
    if date_utc is None:
        date_utc = datetime.datetime.utcnow().date()
    s = date_utc.isoformat()  # YYYY-MM-DD
    total = sum(ord(c) for c in s)
    return ["morning", "noon", "night"][total % 3]
