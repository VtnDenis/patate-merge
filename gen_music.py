"""Génère une boucle musicale (4 mesures, 124 BPM) pour le repli HTML audio."""
import numpy as np, wave, subprocess, math
from pathlib import Path

SR = 44100
BPM = 124
BEAT = 60 / BPM
BAR = 4 * BEAT
BARS = 4
DUR = BARS * BAR
N = int(DUR * SR)
rng = np.random.default_rng(7)


def env(n, a=0.005, d=0.12):
    e = np.ones(n)
    na, nd = int(a * SR), int(d * SR)
    e[:na] = np.linspace(0, 1, na)
    e[-nd:] *= np.linspace(1, 0, nd)
    return e


def kick(t0, gain=0.9):
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    f = 150 * np.exp(-t * 22) + 45
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t * 12)
    add(t0, x * gain)


def snare(t0, gain=0.35):
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    noise = rng.normal(0, 1, n)
    # bandpass grossier
    noise = np.diff(noise, prepend=0)
    x = noise * np.exp(-t * 26)
    add(t0, x * gain)


def hat(t0, gain=0.08):
    n = int(0.035 * SR)
    t = np.arange(n) / SR
    x = rng.normal(0, 1, n) * np.exp(-t * 90)
    add(t0, np.diff(x, prepend=0) * gain)


def bass(t0, midi, dur, gain=0.30):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 440 * 2 ** ((midi - 69) / 12)
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + 0.5 * np.sin(2 * np.pi * f * 2 * t)
    # lowpass simple
    x = np.convolve(x, np.ones(24) / 24, mode="same")
    add(t0, x * env(n, 0.004, 0.05) * gain)


def lead(t0, midi, dur, gain=0.10):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 440 * 2 ** ((midi - 69) / 12)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2 * t)
    add(t0, x * np.exp(-t * 9) * gain)


buf = np.zeros(N + SR)


def add(t0, x):
    i = int(t0 * SR)
    buf[i:i + len(x)] += x


bassline = [45, 45, 57, 45, 48, 48, 55, 48, 45, 45, 57, 45, 43, 43, 50, 43]
leadmot = [0, 0, 0, 0, 72, 0, 74, 0, 0, 76, 0, 74, 72, 0, 0, 0]

for bar in range(BARS):
    b0 = bar * BAR
    for beat in range(4):
        kick(b0 + beat * BEAT)
        if beat in (1, 3):
            snare(b0 + beat * BEAT)
    for s in range(8):
        hat(b0 + s * BEAT / 2, 0.09 if s % 2 else 0.05)
    for s in range(16):
        step = bar * 16 + s
        bass(b0 + s * BEAT / 4, bassline[step % 16] + (2 if bar == 3 else 0), BEAT / 2.6)
        if leadmot[step % 16]:
            lead(b0 + s * BEAT / 4, leadmot[step % 16] + (0 if bar < 3 else -2), BEAT / 2, 0.09)

buf = buf[:N]
# léger écho
delay = int(BEAT / 4 * SR)
echo = np.zeros_like(buf)
echo[delay:] = buf[:-delay] * 0.22
buf = buf + echo
# normalisation douce
buf = np.tanh(buf * 0.9) * 0.85
peak = np.max(np.abs(buf)) or 1
buf = buf / peak * 0.9

# fade aux extrémités pour une boucle propre
f = int(0.02 * SR)
buf[:f] *= np.linspace(0, 1, f)
buf[-f:] *= np.linspace(1, 0, f)

pcm = (np.stack([buf, buf], axis=1) * 32767).astype("<i2")
out = Path(__file__).resolve().parent / "audio" / "music_loop.wav"
with wave.open(str(out), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())

mp3 = out.with_suffix(".mp3")
subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(out),
                "-codec:a", "libmp3lame", "-b:a", "112k", str(mp3)], check=True)
out.unlink()
print("ok", mp3, round(mp3.stat().st_size / 1024), "Ko", round(DUR, 2), "s")
