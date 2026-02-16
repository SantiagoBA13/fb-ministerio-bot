#!/usr/bin/env bash
set -euo pipefail

BG="$1"
AUDIO="$2"
OUT="$3"
DUR="$4"
HOOK="$5"
ASSFILE="$6"

FONT="assets/fonts/Inter-Bold.ttf"

HOOK_ESCAPED=$(python -c "import sys; print(sys.argv[1].replace(':','\\:').replace(\"'\",\"\\\u2019\"))" "$HOOK")

ffmpeg -y \
  -loop 1 -i "$BG" \
  -i "$AUDIO" \
  -t "$DUR" \
  -vf "
    scale=1080:1920,
    format=yuv420p,
    zoompan=z='min(zoom+0.0009,1.08)':d=1:s=1080x1920,
    drawbox=x=0:y=0:w=iw:h=ih:color=black@0.20:t=fill,
    drawtext=fontfile=$FONT:text='$HOOK_ESCAPED':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=210:shadowx=3:shadowy=3:shadowcolor=black@0.9:enable='between(t,0,3.5)',
    ass=$ASSFILE:fontsdir=assets/fonts
  " \
  -c:v libx264 -preset veryfast -crf 20 \
  -c:a aac -b:a 160k \
  "$OUT"
