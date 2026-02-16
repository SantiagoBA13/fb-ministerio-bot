# src/render_image.py
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, random, textwrap

W, H = 1080, 1920

def _fit_cover(img: Image.Image) -> Image.Image:
    iw, ih = img.size
    target_ratio = W / H
    img_ratio = iw / ih
    if img_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))
    return img.resize((W, H), Image.LANCZOS)

def _center_x(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    return (W - tw) // 2

def _draw_center(draw, text, font, y, fill, shadow=True):
    x = _center_x(draw, text, font)
    if shadow:
        draw.text((x+2, y+2), text, font=font, fill=(0,0,0,150))
    draw.text((x, y), text, font=font, fill=fill)

def _pick_bg(backgrounds_dir: str) -> Image.Image:
    bgs = [os.path.join(backgrounds_dir, f) for f in os.listdir(backgrounds_dir)
           if f.lower().endswith((".jpg",".jpeg",".png",".webp"))]
    if not bgs:
        raise RuntimeError("No hay fondos en assets/backgrounds/")
    img = Image.open(random.choice(bgs)).convert("RGB")
    return _fit_cover(img)

def make_background(out_path: str, backgrounds_dir: str):
    img = _pick_bg(backgrounds_dir)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.02)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 110))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(out_path, quality=95, optimize=True)

def make_image(payload: dict, out_path: str, backgrounds_dir: str, fonts_dir: str):
    img = _pick_bg(backgrounds_dir)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.02)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 115))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    font_tag = ImageFont.truetype(os.path.join(fonts_dir, "Inter-Bold.ttf"), 40)
    font_verse = ImageFont.truetype(os.path.join(fonts_dir, "PlayfairDisplay-Bold.ttf"), 66)
    font_ref = ImageFont.truetype(os.path.join(fonts_dir, "Inter-Bold.ttf"), 44)

    tag = payload["tag"].upper()
    verse_wrapped = "\n".join(textwrap.wrap(payload["verse"], width=26))
    ref = payload["ref"]

    _draw_center(draw, tag, font_tag, 210, (255,255,255,235))
    y0 = 900
    for i, line in enumerate(verse_wrapped.split("\n")):
        _draw_center(draw, line, font_verse, y0 + i*78, (255,255,255,245))
    _draw_center(draw, ref, font_ref, y0 + (len(verse_wrapped.split("\n"))*78) + 55, (255,255,255,220))

    img.convert("RGB").save(out_path, quality=95, optimize=True)
