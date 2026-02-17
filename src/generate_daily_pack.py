# src/generate_daily_pack.py
# Crea un pack diario para subir y programar en Meta Business Suite (sin publicar por API).
# Salida: out/YYYY-MM-DD/ (MX) con:
# - 3 piezas (6am/12pm/7pm): 2 imágenes + 1 video (si ElevenLabs está configurado)
# - manifest.json y captions.txt para copiar/pegar

import os
import json
import datetime
from zoneinfo import ZoneInfo
import random
import subprocess

from src.verses import pick
from src.render_image import make_image, make_background
from src.daily_video_slot import pick_video_slot
from src.media_utils import audio_duration_seconds
from src.karaoke_ass import build_karaoke_ass

# ElevenLabs es opcional: si no hay secrets, el pack sale solo con imágenes
try:
    from src.tts_elevenlabs import synthesize_to_mp3
except Exception:
    synthesize_to_mp3 = None  # type: ignore

MX = ZoneInfo("America/Mexico_City")

SLOT_TIME = {
    "morning": "06:00",
    "noon": "12:00",
    "night": "19:00",
}

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def build_hook(slot: str) -> str:
    hooks = {
        "morning": [
            "Dios te dio este día por una razón…",
            "Antes de empezar tu día, escucha esto…",
            "Hoy Dios te habla: no te rindas."
        ],
        "noon": [
            "Si hoy te estás apagando, vuelve a Dios…",
            "Todavía estás a tiempo de retomar el camino.",
            "No es tarde. Dios te levanta hoy."
        ],
        "night": [
            "Antes de dormir, entrega tu carga a Dios…",
            "Dios cuidó de ti hoy. Descansa.",
            "Haz paz con Dios esta noche…"
        ],
    }
    return random.choice(hooks[slot])

def normalize_audio_to_duration(in_mp3: str, out_m4a: str, target: int, tempo: float):
    # atempo soporta 0.5-2.0; aquí solo lo usamos con cambios leves
    subprocess.run([
        "ffmpeg", "-y", "-i", in_mp3,
        "-af", f"atempo={tempo:.4f},apad",
        "-t", str(target),
        out_m4a
    ], check=True)

def caption_for(payload: dict) -> str:
    return (
        f"{payload['headline']}\n\n"
        f"“{payload['verse']}”\n"
        f"{payload['ref']}\n\n"
        f"{payload['reflection']}\n\n"
        f"{payload['cta']}\n"
        f"#Dios #Fe #Cristo #Biblia #Oración"
    )

def eleven_ready() -> bool:
    return bool(os.getenv("ELEVENLABS_API_KEY")) and bool(os.getenv("ELEVENLABS_VOICE_ID")) and (synthesize_to_mp3 is not None)

def main():
    today_mx = datetime.datetime.now(MX).date()
    date_str = today_mx.isoformat()
    out_dir = os.path.join("out", date_str)
    os.makedirs(out_dir, exist_ok=True)

    slots = ["morning", "noon", "night"]

    enable_video = eleven_ready()
    video_slot = pick_video_slot(today_mx) if enable_video else None

    manifest = {
        "date_mx": date_str,
        "timezone": "America/Mexico_City",
        "video_enabled": enable_video,
        "video_slot": video_slot,
        "posts": []
    }

    for slot in slots:
        payload = pick(slot)
        caption = caption_for(payload)

        if enable_video and slot == video_slot:
            # VIDEO: fondo + voz + karaoke
            hook = build_hook(slot)
            voice_text = (
                f"{hook} "
                f"Palabra de Dios: {payload['verse']} {payload['ref']}. "
                f"{payload['reflection']} "
                f"{payload['cta']}"
            )

            bg = os.path.join(out_dir, f"{slot}_video_bg.jpg")
            make_background(bg, "assets/backgrounds")

            mp3 = os.path.join(out_dir, f"{slot}_voice.mp3")
            synthesize_to_mp3(voice_text, mp3)  # type: ignore

            dur = audio_duration_seconds(mp3)
            target = int(round(clamp(dur, 20, 35)))

            tempo = 1.0
            if dur > 35:
                tempo = dur / 35.0
                target = 35

            audio_fixed = os.path.join(out_dir, f"{slot}_voice_fixed.m4a")
            normalize_audio_to_duration(mp3, audio_fixed, target, tempo)

            ass_path = os.path.join(out_dir, f"{slot}_karaoke.ass")
            build_karaoke_ass(
                text=voice_text,
                duration_s=target,
                out_path=ass_path,
                fontname="Inter",
                fontsize=54,
                margin_v=190
            )

            mp4 = os.path.join(out_dir, f"{slot}_VIDEO_{target}s.mp4")
            subprocess.run(
                ["bash", "src/render_video.sh", bg, audio_fixed, mp4, str(target), hook, ass_path],
                check=True
            )

            manifest["posts"].append({
                "slot": slot,
                "type": "video",
                "recommended_time_mx": SLOT_TIME[slot],
                "file": os.path.basename(mp4),
                "caption": caption
            })
        else:
            # IMAGEN
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

    print("✅ Pack diario generado:", out_dir)
    print("🎬 Video habilitado:", enable_video, "| Video slot:", video_slot)

if __name__ == "__main__":
    main()
