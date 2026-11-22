#!/usr/bin/env bash
# Render frames -> music -> mix with voiceover.wav  =>  songduhee-bio.mp4
set -euo pipefail
cd "$(dirname "$0")"
[ -f build-silent.mp4 ] || node render.js build-silent.mp4 30
python3 music.py build-music.wav timeline.json
ffmpeg -y -v error -i build-silent.mp4 -i build-music.wav -i voiceover.wav -filter_complex \
 "[2:a]aresample=44100,aformat=channel_layouts=stereo,volume=1.4,apad=whole_dur=99.5,asplit=2[vo][sc];\
  [1:a]volume=0.35[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=400[duck];\
  [duck][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]" \
 -map 0:v -map "[a]" -c:v libx264 -preset slow -crf 23 -maxrate 8M -bufsize 16M -pix_fmt yuv420p \
 -c:a aac -b:a 192k -shortest -movflags +faststart songduhee-bio.mp4
rm -f build-music.wav build-silent.mp4
echo "done -> songduhee-bio.mp4"
