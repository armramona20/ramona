"""Generate an original beat (120 BPM) synced to the clip's scene cuts.
Usage: python3 music.py out.wav [timeline.json]
Needs only numpy. Scene cuts are on half-beat grid (0.5s), so hits land exactly on cuts.
"""
import sys, wave
import numpy as np

SR = 44100
BPM = 120
BEAT = 60 / BPM                      # 0.5s
# scene timing comes from timeline.json (written by build.py); falls back to the original 45s cut
if len(sys.argv) > 2:
    import json
    _tl = json.load(open(sys.argv[2]))
    DUR = float(_tl["duration"])
    CUTS = [v[0] for k, v in sorted(_tl["scenes"].items()) if v[0] > 0]
    RISE_FROM, HIT = _tl["scenes"]["s7"][0], _tl["scenes"]["s8"][0] + 0.7
else:
    DUR = 45.0
    CUTS = [4.5, 10, 15.5, 21, 26.5, 32, 36.5, 41.5]
    RISE_FROM, HIT = 32.0, 37.2
PRICE_SLAM = HIT                     # big number lands (S8 start + 0.7s)
N = int(SR * DUR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)


def t_(d):
    return np.arange(int(SR * d)) / SR


def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    buf[i:i + len(sig)] += sig * gain


def both(start, sig, gain=1.0, pan=0.0):
    add(L, start, sig, gain * (1 - max(pan, 0)))
    add(R, start, sig, gain * (1 + min(pan, 0)))


def lowpass(x, k):
    k = max(1, int(k))
    return np.convolve(x, np.ones(k) / k, mode="same")


def highpass(x, k):
    return x - lowpass(x, k)


# ---------- instruments ----------
def kick():
    t = t_(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7) + 0.3 * np.exp(-t * 200) * rng.standard_normal(len(t)) * 0.3


def clap():
    t = t_(0.25)
    n = highpass(rng.standard_normal(len(t)), 6)
    env = np.exp(-t * 22)
    for d in (0.0, 0.012, 0.024):  # flam
        env += (t >= d) * np.exp(-np.clip(t - d, 0, None) * 90) * 0.6
    return lowpass(n, 3) * env * 0.5


def hat(open_=False):
    t = t_(0.18 if open_ else 0.05)
    n = highpass(rng.standard_normal(len(t)), 2)
    return n * np.exp(-t * (18 if open_ else 80)) * 0.35


def bass(freq, d):
    t = t_(d)
    saw = 2 * ((t * freq) % 1) - 1
    sub = np.sin(2 * np.pi * freq * t)
    s = lowpass(saw, 30) * 0.5 + sub * 0.8
    env = np.minimum(1, t / 0.005) * np.exp(-t * 3.5)
    return s * env


def pad(freqs, d):
    t = t_(d)
    s = np.zeros(len(t))
    for f in freqs:
        for det in (-0.6, 0.6):
            s += np.abs(((t * (f + det)) % 1) * 4 - 2) - 1   # triangle
    env = np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.4)
    return lowpass(s, 8) * env / len(freqs) * 0.22


def whoosh(d=0.45):
    t = t_(d)
    n = rng.standard_normal(len(t))
    k = np.linspace(40, 2, len(t))         # sweep from dark to bright
    out = np.zeros(len(t)); seg = 2048
    for i in range(0, len(t), seg):
        out[i:i + seg] = highpass(n[i:i + seg], 3) if k[i] < 4 else lowpass(n[i:i + seg], k[i])
    env = (t / d) ** 2.2
    return out * env * 0.55


def impact():
    t = t_(1.2)
    boom = np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 10)) * t) * np.exp(-t * 3.2)
    crash = highpass(rng.standard_normal(len(t)), 2) * np.exp(-t * 4) * 0.25
    return boom * 0.9 + crash


def ding():
    t = t_(1.0)
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((1568, 1), (2093, .6), (3136, .3)))
    return s * np.exp(-t * 4) * 0.25


def riser(d):
    t = t_(d)
    f = 200 * (8 ** (t / d))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * (t / d) ** 2 * 0.15 + highpass(rng.standard_normal(len(t)), 3) * (t / d) ** 3 * 0.2


# ---------- arrangement ----------
# Am - F - C - G, one chord per bar (2s)
PROG = [(110.0, [220, 261.63, 329.63]), (87.31, [174.61, 220, 261.63]),
        (130.81, [261.63, 329.63, 392.0]), (98.0, [196.0, 246.94, 293.66])]
BAR = 4 * BEAT
nbars = int(np.ceil(DUR / BAR))

for b in range(nbars):
    t0 = b * BAR
    root, chord = PROG[b % 4]
    both(t0, pad(chord, BAR), 1.0)
    # bass: 8th notes, octave jump on the "and" of 4
    for e in range(8):
        f = root * (2 if e == 7 else 1)
        both(t0 + e * BEAT / 2, bass(f, BEAT / 2), 0.32)
    for q in range(4):
        tb = t0 + q * BEAT
        both(tb, kick(), 0.9)
        if q in (1, 3):
            both(tb, clap(), 0.55)
        both(tb + BEAT / 2, hat(open_=(q == 3)), 0.6, pan=0.3)
        both(tb, hat(), 0.35, pan=-0.3)

# transitions: whoosh into every cut + hit on the cut
for c in CUTS:
    both(c - 0.42, whoosh(0.45), 0.7)
    both(c, impact(), 0.35)

# build-up into the Flash Sale scene, then slam + cash ding
both(RISE_FROM, riser(CUTS[CUTS.index(next(c for c in CUTS if c > RISE_FROM))] - RISE_FROM), 1.0)
both(PRICE_SLAM, impact(), 0.8)
both(PRICE_SLAM + 0.05, ding(), 1.0)

# mix: sidechain-ish duck on each beat, master fade, normalize
beat_phase = (np.arange(N) / SR) % BEAT
duck = 1 - 0.35 * np.exp(-beat_phase * 12)
fade = np.ones(N)
fi, fo = int(0.05 * SR), int(1.2 * SR)
fade[:fi] = np.linspace(0, 1, fi)
fade[-fo:] = np.linspace(1, 0, fo)
mix = np.stack([L, R], 1) * fade[:, None]
mix[:, 0] *= 0.85 + 0.15 * duck
mix[:, 1] *= 0.85 + 0.15 * duck
mix = np.tanh(mix / np.max(np.abs(mix)) * 1.6) * 0.89   # soft clip / loudness

out = sys.argv[1] if len(sys.argv) > 1 else "music.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("wrote", out)
