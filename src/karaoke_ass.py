# src/karaoke_ass.py
import re

def _clean_word(w: str) -> str:
    return re.sub(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]+", "", w)

def build_karaoke_ass(text: str, duration_s: int, out_path: str,
                      fontname: str = "Inter", fontsize: int = 54, margin_v: int = 190):
    words = text.strip().split()
    if not words:
        raise ValueError("Texto vacío para karaoke")

    total_cs = int(duration_s * 100)

    weights = []
    for w in words:
        core = _clean_word(w)
        base = max(1, len(core))
        if w.endswith((",", ";", ":")):
            base += 6
        if w.endswith((".", "!", "?", "…")):
            base += 10
        weights.append(base)

    s = sum(weights)
    durs = [max(1, round(total_cs * w / s)) for w in weights]
    durs[-1] += (total_cs - sum(durs))

    max_line_chars = 26
    line_len = 0
    parts = []
    for w, cs in zip(words, durs):
        plain_len = len(_clean_word(w)) + 1
        if line_len + plain_len > max_line_chars:
            parts.append(r"\N")
            line_len = 0
        parts.append(f"{{\\k{int(cs)}}}{w}")
        line_len += plain_len

    karaoke_text = " ".join(parts).replace(" \\N ", r"\N")

    primary_yellow = "&H0000FFFF"
    secondary_white = "&H00FFFFFF"
    outline_black = "&H00000000"

    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{fontname},{fontsize},{primary_yellow},{secondary_white},{outline_black},&H64000000,1,0,0,0,100,100,0,0,1,3,1,2,60,60,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:{duration_s:02d}.00,Default,,0,0,0,,{karaoke_text}
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ass)
