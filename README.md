# fb-ministerio-bot (Business Suite)

Este repo genera **packs de publicaciones** (imágenes + 1 video diario con voz ElevenLabs y subtítulos karaoke) para que los subas y programes desde **Meta Business Suite**.

## Qué genera cada día
Salida en: `out/YYYY-MM-DD/` (fecha de México)

- `morning_IMAGE.jpg`  (06:00 MX)
- `noon_IMAGE.jpg`     (12:00 MX)
- `night_IMAGE.jpg`    (19:00 MX)
- **1 solo video al día**: `*_VIDEO_20s.mp4` … `*_VIDEO_35s.mp4` (slot del día)
- `captions.txt` (copiar/pegar captions)
- `manifest.json` (detalle estructurado)

## Secrets necesarios (para habilitar video)
En GitHub → Settings → Secrets and variables → Actions:

- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`

Si NO agregas estos secrets, el pack se genera igual, pero **solo con imágenes**.
- (opcional) `ELEVENLABS_MODEL_ID` = `eleven_multilingual_v2`

> Los secretos de Facebook **no son necesarios** si solo usarás Business Suite.

## Cómo usar desde el teléfono (Business Suite)
1. GitHub → **Actions** → workflow **Generate Daily Pack (Business Suite)**.
2. Abre el run del día y descarga el **Artifact** `daily-pack` (ZIP).
3. Descomprime y entra a `out/YYYY-MM-DD/`.
4. Abre `captions.txt` y copia el texto del slot.
5. En **Meta Business Suite** programa:
   - 06:00 → archivo `morning_*`
   - 12:00 → archivo `noon_*`
   - 19:00 → archivo `night_*`

## Workflows
- **Generate Daily Pack (Business Suite)**: automático diario + manual.
- **Generate Week Pack (Images + 1 Video/Day)**: manual, genera 7 días (consume más cuota de ElevenLabs).
- **Publish to Facebook (API) - manual only**: desactivado para no fallar sin tokens (solo manual).
