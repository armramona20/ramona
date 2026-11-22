"""Original documentary-style score for the clip, built from numpy synthesis.
Usage: python3 music.py out.wav timeline.json
Moods follow the story: tense intro -> warm story -> upbeat viral -> hopeful -> dark drama -> open question.
"""
import sys, json, wave
import numpy as np

SR = 44100
tl = json.load(open(sys.argv[2]))
DUR = float(tl["duration"])
CUTS = sorted(v[0] for v in tl["scenes"].values() if v[0] > 0)
SEC = tl["sections"]          # [start, end, mood]
HITS = tl["hits"]             # big impacts
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(3)
BPM = 96; BEAT = 60 / BPM


def ar(n):
    return np.arange(n) / SR


def add(start, sig, g=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N or i + len(sig) <= 0:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * g * (1 - pan) ** .5
    R[i:i + len(sig)] += sig * g * (1 + pan) ** .5


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def env(n, a=.01, d=.3, s=.0, rel=.0):
    t = ar(n); e = np.minimum(t / max(a, 1e-4), 1) * (s + (1 - s) * np.exp(-t / d))
    if rel:
        k = int(rel * SR); e[-k:] *= np.linspace(1, 0, k)
    return e


def pad(m, dur, g=.05):
    n = int(dur * SR); t = ar(n); x = np.zeros(n)
    for dt in (-.08, 0, .07):
        f = hz(m) * 2 ** (dt / 12); x += np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)
    a = min(int(.8 * SR), n // 2); e = np.ones(n); e[:a] = np.linspace(0, 1, a); e[-a:] *= np.linspace(1, 0, a)
    return x * e * g


def pluck(m, dur=1.2, g=.12):
    n = int(dur * SR); t = ar(n); f = hz(m)
    x = np.sin(2 * np.pi * f * t) + .5 * np.sin(4 * np.pi * f * t) * np.exp(-t * 6) + .25 * np.sin(6 * np.pi * f * t) * np.exp(-t * 9)
    return x * env(n, .004, .45) * g


def kick(g=.5):
    n = int(.35 * SR); t = ar(n); f = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * g


def hat(g=.05):
    n = int(.06 * SR); x = rng.standard_normal(n); x = np.diff(x, prepend=0)
    return x * np.exp(-ar(n) * 70) * g


def clap(g=.12):
    n = int(.2 * SR); x = rng.standard_normal(n); x = np.convolve(x, [1, -.6], 'same')
    return x * np.exp(-ar(n) * 22) * g


def boom(g=.6):
    n = int(2.5 * SR); t = ar(n); f = 38 + 60 * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    nz = rng.standard_normal(n) * np.exp(-t * 5) * .25
    nz = np.convolve(nz, np.ones(40) / 40, 'same')
    return (s + nz) * g


def whoosh(d=.5, g=.08):
    n = int(d * SR); x = rng.standard_normal(n); k = np.linspace(0, 1, n)
    x = np.convolve(x, np.ones(25) / 25, 'same')
    return x * np.sin(np.pi * k) ** 2 * g


def tick(g=.05):
    n = int(.03 * SR); return np.sin(2 * np.pi * 2400 * ar(n)) * np.exp(-ar(n) * 200) * g


CH_MIN = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]   # Am F C G
CH_MAJ = [(48, 52, 55), (55, 59, 62), (57, 60, 64), (53, 57, 60)]   # C G Am F
CH_DARK = [(45, 48, 52), (41, 45, 48), (44, 48, 51), (45, 48, 52)]  # Am F Ab Am

for s0, s1, mood in SEC:
    bar = BEAT * 4
    t = s0; i = 0
    while t < s1 - .05:
        d = min(bar, s1 - t)
        ch = {'warm': CH_MIN, 'tense': CH_DARK, 'up': CH_MAJ, 'hope': CH_MAJ, 'dark': CH_DARK, 'open': CH_MIN}[mood][i % 4]
        gpad = {'tense': .035, 'warm': .03, 'up': .022, 'hope': .035, 'dark': .04, 'open': .035}[mood]
        for m in ch:
            add(t, pad(m - (12 if mood in ('dark', 'tense') else 0), d + .6, gpad), pan=(m % 3 - 1) * .3)
        add(t, pad(ch[0] - 24, d + .6, .05))
        for b in range(8):
            bt = t + b * BEAT / 2
            if bt >= s1 - .05:
                break
            if mood in ('warm', 'hope', 'up', 'open'):
                arp = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]][b] + 12
                add(bt, pluck(arp, g=.07 if mood != 'open' else .05), pan=.4 if b % 2 else -.4)
            if mood == 'up':
                if b % 4 == 0: add(bt, kick(.45))
                if b % 4 == 2: add(bt, clap(.1))
                add(bt, hat(.035), pan=.3)
            if mood == 'hope' and b % 4 == 0:
                add(bt, kick(.25))
            if mood in ('dark', 'tense'):
                add(bt, tick(.04 if mood == 'dark' else .025), pan=.5)
                if mood == 'dark' and b in (0, 1):
                    add(bt, kick(.3 if b == 0 else .18))   # heartbeat
        t += bar; i += 1

for c in CUTS:
    add(c - .3, whoosh(.5, .05), pan=-.2)
for h in HITS:
    add(h - .45, whoosh(.5, .09))
    add(h, boom(.55))

# fades + soft limiter
fi, fo = int(.3 * SR), int(2.0 * SR)
for b in (L, R):
    b[:fi] *= np.linspace(0, 1, fi); b[-fo:] *= np.linspace(1, 0, fo)
mx = max(np.abs(L).max(), np.abs(R).max())
out = np.tanh(np.stack([L, R], 1) / mx * 1.4) * .85
with wave.open(sys.argv[1], 'w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print('music ->', sys.argv[1], f'{DUR}s')
