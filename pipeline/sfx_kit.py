#!/usr/bin/env python3
"""Kit de SFX sintetizados (numpy/scipy) — eventos amarrados ao NÚMERO DO QUADRO.
Uso típico:
    from sfx_kit import Track
    tr = Track(dur_s=14.05, seed=7)
    tr.pop(158, vol=0.16)          # clique/pop no quadro 158
    tr.tick(205, freq=2100)        # tick de digitação
    tr.whoosh(356, vol=0.11)       # transição
    tr.shimmer(548)                # confirmação
    tr.pad([110, 164.81, 246.94], 0.0, 7.6)   # cama harmônica
    tr.save("sfx.wav")
Volumes pensados para ficar SOB uma narração (mixar a trilha a ~0.5).
"""
import numpy as np
from scipy.io import wavfile

SR = 48000

class Track:
    def __init__(self, dur_s, seed=7, fps=60):
        self.buf = np.zeros(int(SR * dur_s))
        self.rng = np.random.default_rng(seed)
        self.fps = fps

    def _place(self, frame, sig):
        i = int(frame / self.fps * SR)
        j = min(len(self.buf), i + len(sig))
        if i < len(self.buf):
            self.buf[i:j] += sig[:j - i]

    @staticmethod
    def _env(n, tau):
        return np.exp(-np.arange(n) / (tau * SR))

    def pop(self, frame, vol=0.22, f0=640, f1=210, dur=0.09):
        """Clique elástico: pitch cai rápido. Botões, cards, palavras-chave."""
        n = int(dur * SR); t = np.arange(n) / SR
        freq = f1 + (f0 - f1) * np.exp(-t * 46)
        self._place(frame, np.sin(np.cumsum(freq) / SR * 2 * np.pi) * self._env(n, 0.02) * vol)

    def tick(self, frame, vol=0.05, freq=2200):
        """Tick curto e seco: digitação, contadores, barras subindo."""
        n = int(0.022 * SR); t = np.arange(n) / SR
        self._place(frame, np.sin(2 * np.pi * freq * t) * self._env(n, 0.005) * vol)

    def whoosh(self, frame, vol=0.11, dur=0.36):
        """Ruído filtrado varrendo: transições, zooms, morphs."""
        n = int(dur * SR); noise = self.rng.standard_normal(n)
        sweep = 0.5 - 0.5 * np.cos(np.linspace(0, 2 * np.pi, n)); alpha = 0.02 + 0.3 * sweep
        out = np.zeros(n); acc = 0.0
        for i in range(n):
            acc += alpha[i] * (noise[i] - acc); out[i] = acc
        self._place(frame, out * (np.sin(np.linspace(0, np.pi, n)) ** 1.5) * vol * 3.2)

    def shimmer(self, frame, vol=0.05, freqs=(1568, 2093), dur=0.5):
        """Brilho de confirmação: senos agudos com decay longo."""
        n = int(dur * SR); t = np.arange(n) / SR
        sig = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
        self._place(frame, sig * self._env(n, 0.16) * vol)

    def tone(self, frame, freq, dur, vol, tau=0.24):
        n = int(dur * SR); t = np.arange(n) / SR
        self._place(frame, (np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * freq * 2 * t)) * self._env(n, tau) * vol)

    def pad(self, freqs, start_s, dur_s, vol=0.05):
        """Cama harmônica com fade in/out — fundo musical discreto."""
        n = int(dur_s * SR); t = np.arange(n) / SR
        env = np.minimum(1, t / 1.4) * np.minimum(1, (dur_s - t) / 1.6); env = np.clip(env, 0, 1) ** 1.5
        sig = sum((np.sin(2 * np.pi * f * t) + 0.22 * np.sin(2 * np.pi * f * 2 * t) + 0.08 * np.sin(2 * np.pi * f * 3 * t)) for f in freqs) / len(freqs)
        i = int(start_s * SR); j = min(len(self.buf), i + n)
        self.buf[i:j] += (sig * env * vol)[:j - i]

    def save(self, path, peak=0.82):
        tr = np.tanh(self.buf * 1.15)
        tr = tr / max(1e-9, np.max(np.abs(tr))) * peak
        wavfile.write(path, SR, (tr * 32767).astype(np.int16))
        print(f"{path} ok")
