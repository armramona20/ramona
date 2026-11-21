# URTHE – INTOXICATING SHIRTS · code animation clip (9:16, with Thai voiceover)

**Output:** `urthe-intoxicating-shirts.mp4` – 1080x1920, 30fps, ~60s, Thai voiceover + original beat. No prices shown (they change often).

## Rebuild
```
pip install edge-tts numpy
python3 build.py              # TTS -> timeline -> render frames -> music -> mix
python3 build.py --no-video   # only redo voice/music mix (scene lengths must stay the same)
```
- `voiceover.json` – the script, voice (`th-TH-PremwadeeNeural`; male: `th-TH-NiwatNeural`), speed. Each scene stretches to fit its line (min length per scene, rounded to 0.5s so beats hit every cut).
- `index.html` – the animation (HTML/CSS/JS, reads scene times from generated `timeline.js`). Serve the folder (`python3 -m http.server`) to watch it live; `?t=12.5` shows one frame.
- `render.js` – Playwright frame-by-frame renderer; `stills.js` – preview PNGs.
- `music.py` – original 120 BPM beat synced to `timeline.json`.
- `vo/` – generated voice lines. `assets/` – product photos, fonts, cropped model footage.

Scenes: hook · brand/title · 01 fabric · 02 metal tag · 03 back embroidery + pleat · 4 colors · size · best seller 1,000+ · CTA.
