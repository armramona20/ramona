# ประวัติ ซองดูฮี · code animation clip (9:16, 99.5s)

**Output:** `songduhee-bio.mp4` – 1080x1920, 30fps, the supplied voiceover (`voiceover.wav`) + an original documentary-style score (`music.py`).

20 scenes, each cut and text pop timed to word timestamps from the voiceover (see `SC` and the `data-in` times in `index.html`):
hook (เช็กเกลียว) · COVID van · เขาคือใคร · profile (ศุกล เครือเสน / ปั่น / เด็กอีสาน) · บวชเรียน · ทำทุกงาน · Korea map · new Korean name · reveal ซองดูฮี ·
taxi / ambulance / exec driver · durian son-in-law clip · viral + MV "นกเจ่า" + 100M views · "แก๋ว" catchphrase · free COVID rides to Isan · influencer + foundation ·
ยิ่งดังยิ่งร้อน · อุดรธานี night (footage) · แจ้งความ · two sides (ฮีโร่ / ตัวต้นเรื่อง) · question to the viewer.

Footage frames in `assets/footA` (incident clip) and `assets/footB` (event clip) come from the supplied TikTok clips (original audio not used). Photos in `assets/photos`.
Cover: `node cover.js` (cover.html -> cover.jpg).
Rebuild: `./build.sh` (node + playwright, ffmpeg, numpy). Live preview: serve the folder and open `index.html` (click to play with sound); `?t=12.5` shows one frame.
