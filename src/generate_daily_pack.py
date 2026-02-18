# src/generate_daily_pack.py
# Pack diario SOLO IMÁGENES para programar en Meta Business Suite.
# Salida: out/YYYY-MM-DD/ (MX) con:
# - 3 imágenes (6am/12pm/7pm)
# - manifest.json y captions.txt para copiar/pegar

import os
import json
import datetime
from zoneinfo import ZoneInfo

from src.verses import pick
from src.render_image import make_image

MX = ZoneInfo("America/Mexico_City")

SLOT_TIME = {
    "morning": "06:00",
    "noon": "12:00",
    "night": "19:00",
}

def caption_for(payload: dict) -> str:
    return (
        f"{payload['headline']}\n\n"
        f"“{payload['verse']}”\n"
        f"{payload['ref']}\n\n"
        f"{payload['reflection']}\n\n"
        f"{payload['cta']}\n"
        f"#Dios #Fe #Cristo #Biblia #Oración"
    )

def main():
    today_mx = datetime.datetime.now(MX).date()
    date_str = today_mx.isoformat()
    out_dir = os.path.join("out", date_str)
    os.makedirs(out_dir, exist_ok=True)

    slots = ["morning", "noon", "night"]

    manifest = {
        "date_mx": date_str,
        "timezone": "America/Mexico_City",
        "video_enabled": False,
        "posts": []
    }

    for slot in slots:
        payload = pick(slot)
        caption = caption_for(payload)

        img = os.path.join(out_dir, f"{slot}_IMAGE.jpg")
        make_image(payload, img, "assets/backgrounds", "assets/fonts")

        manifest["posts"].append({
            "slot": slot,
            "type": "image",
            "recommended_time_mx": SLOT_TIME[slot],
            "file": os.path.basename(img),
            "caption": caption
        })

    # Guardar manifest + captions.txt
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    lines = []
    for p in manifest["posts"]:
        lines.append(f"=== {p['slot'].upper()} ({p['type']}) {p['recommended_time_mx']} MX ===")
        lines.append(p["caption"])
        lines.append("")
    with open(os.path.join(out_dir, "captions.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("✅ Pack diario (solo imágenes) generado:", out_dir)

if __name__ == "__main__":
    main()
