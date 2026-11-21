# URTHE – INTOXICATING SHIRTS · code animation clip (45s, 9:16)

- `index.html` – the animation (HTML/CSS/JS, deterministic timeline). Open via a local server (`python3 -m http.server`) to watch it loop live; `?t=12.5` shows a single frame.
- `render.js` – renders it frame-by-frame to MP4 (1080x1920, 30fps): `node render.js out.mp4`
- `stills.js` – quick preview PNGs: `node stills.js outdir 2 10 20`
- `music.py` – generates an original 120 BPM beat synced to the scene cuts (whooshes, riser, price slam + ding). Needs numpy.
- `urthe-intoxicating-shirts-45s.mp4` – rendered clip with music.

Rebuild with sound:
```
node render.js silent.mp4 && python3 music.py music.wav
ffmpeg -i silent.mp4 -i music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af loudnorm=I=-14:TP=-1.5 -shortest urthe-intoxicating-shirts-45s.mp4
```

Timeline: 0–4.5 hook · 4.5–10 brand/title · 10–15.5 fabric · 15.5–21 metal tag · 21–26.5 back embroidery + pleat · 26.5–32 4 colors · 32–36.5 size · 36.5–41.5 Flash Sale ฿360 · 41.5–45 CTA.
Price/sales info is from the Shopee screen recording of 21 Nov 2026 — update in `index.html` if it changes.
