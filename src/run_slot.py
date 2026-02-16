# src/run_slot.py
import os
import random
import subprocess

from src.verses import pick
from src.render_image import make_image, make_background
from src.post_facebook import post_photo
from src.post_video import post_video
from src.daily_video_slot import pick_video_slot
from src.tts_elevenlabs import synthesize_to_mp3
from src.media_utils import audio_duration_seconds
from src.karaoke_ass import build_karaoke_ass

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
    subprocess.run([
        "ffmpeg", "-y", "-i", in_mp3,
        "-af", f"atempo={tempo:.4f},apad",
        "-t", str(target),
        out_m4a
    ], check=True)

def main():
    slot = os.environ.get("SLOT", "morning").strip()
    video_slot_today = pick_video_slot()  # morning/noon/night (1 por día)

    payload = pick(slot)

    caption = (
        f"{payload['headline']}\n\n"
        f"“{payload['verse']}”\n"
        f"{payload['ref']}\n\n"
        f"{payload['reflection']}\n\n"
        f"{payload['cta']}\n"
        f"#Dios #Fe #Cristo #Biblia #Oración"
    )

    page_id = os.environ["FB_PAGE_ID"]
    token = os.environ["FB_PAGE_ACCESS_TOKEN"]

    if slot == video_slot_today:
        hook = build_hook(slot)

        # Texto hablado (viral, directo)
        voice_text = (
            f"{hook} "
            f"Palabra de Dios: {payload['verse']} {payload['ref']}. "
            f"{payload['reflection']} "
            f"{payload['cta']}"
        )

        # Fondo para video (solo paisaje + overlay, sin versículo impreso)
        bg = "video_bg.jpg"
        make_background(bg, "assets/backgrounds")

        # Voz ElevenLabs
        audio = "voice.mp3"
        synthesize_to_mp3(voice_text, audio)

        dur = audio_duration_seconds(audio)
        target = int(round(clamp(dur, 20, 35)))

        tempo = 1.0
        if dur > 35:
            tempo = dur / 35.0
            target = 35

        audio_fixed = "voice_fixed.m4a"
        normalize_audio_to_duration(audio, audio_fixed, target, tempo)

        # Karaoke subtitles (ASS)
        ass_path = "karaoke.ass"
        build_karaoke_ass(
            text=voice_text,
            duration_s=target,
            out_path=ass_path,
            fontname="Inter",
            fontsize=54,
            margin_v=190
        )

        out = "video.mp4"
        subprocess.run(
            ["bash", "src/render_video.sh", bg, audio_fixed, out, str(target), hook, ass_path],
            check=True
        )

        res = post_video(page_id, token, out, caption)
        print("VIDEO publicado:", res)

    else:
        out_img = "post.jpg"
        make_image(payload, out_img, "assets/backgrounds", "assets/fonts")
        res = post_photo(page_id, token, out_img, caption)
        print("IMAGEN publicada:", res)

if __name__ == "__main__":
    main()
