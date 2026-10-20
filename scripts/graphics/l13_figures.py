#!/usr/bin/env python3
"""L13 figures (DTMF).

  L13-keypad     : the 4 x 4 DTMF keypad with its row and column frequencies.
  L13-goertzel   : the response of the four row bins of a Goertzel decoder with
                   N = 205 at 8 kHz, against frequency, with the four row tones
                   marked; neighboring rows are 73 to 89 Hz apart and each bin
                   is 78 Hz wide between its first nulls.
  L13-capture    : the spectrogram of book/extras/grc/L13-capture.wav, the
                   synthetic capture that L13-dtmf-capture.grc writes, with
                   each digit labeled. It is labeled "Simulated" on the figure.

The GNU Radio screenshots (L13-grc-*.png, L13-keypad-run.png, L13-rx-*.png,
L13-link-*.png) are not generated here: they come from the flowgraphs in
book/extras/grc/ running under Xvfb (see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l13_figures.py
"""

from __future__ import annotations

import io
import re
import wave
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, RED, GREEN, GRAY, INK, RULE = "#004a85", "#8a5a00", "#b01e24", "#3f7d34", "#5b6573", "#15202b", "#cddce9"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})

ROWS = (697, 770, 852, 941)
COLS = (1209, 1336, 1477, 1633)
KEYS = ("123A", "456B", "789C", "*0#D")
FS, N = 8000, 205


def write(name, fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = apply_font_stack(buf.getvalue()[buf.getvalue().index("<svg"):])
    s = re.sub(r' d="([^"]*)"', lambda m: ' d="' + re.sub(r"(\d+\.\d)\d+", r"\1", m.group(1)) + '"', s)
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


def keypad():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.set_xlim(-1.6, 4.3)
    ax.set_ylim(-0.2, 5.25)
    ax.axis("off")
    for c, f in enumerate(COLS):
        ax.text(c + 0.5, 4.55, f"{f}\nHz", ha="center", va="center", color=AMBER, fontsize=10.5, fontweight="bold", linespacing=1.0)
    for r, f in enumerate(ROWS):
        y = 3.5 - r
        ax.text(-0.15, y, f"{f} Hz", ha="right", va="center", color=NAVY, fontsize=11, fontweight="bold")
        for c in range(4):
            extra = c == 3
            ax.add_patch(FancyBboxPatch((c + 0.08, y - 0.42), 0.84, 0.84, boxstyle="round,pad=0,rounding_size=0.12",
                                        fc="#f5f9fc" if extra else "#eef4fa", ec=GRAY if extra else NAVY,
                                        lw=1, ls=(0, (3, 2)) if extra else "-"))
            ax.text(c + 0.5, y, KEYS[r][c], ha="center", va="center", fontsize=17, fontweight="bold",
                    color=GRAY if extra else INK)
    ax.text(2.0, 5.1, "column (high group)", ha="center", va="center", color=AMBER, fontsize=10)
    ax.text(-1.55, 4.05, "row (low group)", ha="left", va="center", color=NAVY, fontsize=10)
    write("L13-keypad", fig)


def goertzel():
    f = np.linspace(620, 1010, 2000)
    fig, ax = plt.subplots(figsize=(8.4, 3.4))
    cols = [NAVY, RED, GREEN, INK]
    for fk, col in zip(ROWS, cols):
        d = np.pi * (f - fk) / FS
        h = np.abs(np.sin(N * d) / (N * np.sin(d) + 1e-30))
        h[np.abs(d) < 1e-12] = 1
        ax.plot(f, 20 * np.log10(np.maximum(h, 1e-4)), color=col, lw=1.6, label=f"bin at {fk} Hz")
    for fk in ROWS:
        ax.axvline(fk, color=GRAY, lw=0.8, ls=(0, (3, 3)))
    ax.annotate("", xy=(697, 4), xytext=(770, 4), arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.2))
    ax.text(733.5, 5.5, "73 Hz", ha="center", va="bottom", color=AMBER, fontsize=10,
            bbox=dict(fc="white", ec="none", pad=1))
    ax.annotate("", xy=(697 - 39, -37), xytext=(697 + 39, -37), arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.2))
    ax.text(697, -39.5, "78 Hz", ha="center", va="top", color=NAVY, fontsize=10,
            bbox=dict(fc="white", ec="none", pad=1))
    ax.set_xlim(620, 1010)
    ax.set_ylim(-46, 10)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("bin response (dB)")
    ax.legend(loc="upper right", fontsize=9, frameon=False, ncol=4, bbox_to_anchor=(1.0, 1.16))
    write("L13-goertzel", fig)


def capture():
    with wave.open(str(ROOT / "book/extras/grc/L13-capture.wav")) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768
    nfft, hop = 256, 32
    win = np.hanning(nfft)
    frames = np.array([x[i:i + nfft] * win for i in range(0, len(x) - nfft, hop)])
    s = 20 * np.log10(np.abs(np.fft.rfft(frames, axis=1)) + 1e-6)
    t = (np.arange(len(frames)) * hop + nfft / 2) / FS
    fr = np.fft.rfftfreq(nfft, 1 / FS)
    fig, ax = plt.subplots(figsize=(8.4, 3.6))
    ax.pcolormesh(t, fr, s.T, shading="auto", cmap="Blues", vmin=s.max() - 50, vmax=s.max())
    ax.set_ylim(500, 1800)
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("frequency (Hz)")
    for f in ROWS + COLS:
        ax.axhline(f, color=RULE, lw=0.6, zorder=0)
    for k, d in enumerate("7195550148"):
        ax.text(0.025 + 0.1 * k, 1745, d, ha="center", va="center", color=RED, fontsize=12, fontweight="bold")
    ax.text(1.04, 560, "Simulated capture", ha="right", va="center", color=GRAY, fontsize=10, style="italic")
    write("L13-capture", fig)


if __name__ == "__main__":
    keypad()
    goertzel()
    capture()
