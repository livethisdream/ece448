#!/usr/bin/env python3
"""L8 figures (FSK).

  L08-burst-sim : what an FSK burst from a 433.92 MHz remote looks like on a
                  waterfall: two tones, a 1010 preamble, then data. The tone
                  spacing gives the deviation and the shortest dwell gives the
                  symbol rate. SIMULATED -- labeled so on the figure.

The GNU Radio screenshots (L08-grc-*.png, L08-tx-*.png, L08-link-*.png) are
not generated here: they are taken from the real flowgraphs in
book/extras/grc/ running under Xvfb (see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l08_figures.py
"""

from __future__ import annotations

import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, RED, GRAY, INK, RULE = "#004a85", "#8a5a00", "#b01e24", "#5b6573", "#15202b", "#cddce9"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})
RNG = np.random.default_rng(8)


def write(name, fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = apply_font_stack(buf.getvalue()[buf.getvalue().index("<svg"):])
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


def burst_sim():
    fs, baud, dev = 250e3, 1e3, 20e3                 # S/s, symbols/s, Hz
    sps = int(fs / baud)
    bits = np.r_[np.tile([1, 0], 4), RNG.integers(0, 2, 16)]
    nrz = np.repeat(2 * bits - 1, sps).astype(float)
    pad = np.zeros(int(2e-3 * fs))                     # quiet air before and after
    phase = 2 * np.pi * dev / fs * np.cumsum(nrz)
    x = np.r_[pad, np.exp(1j * phase), pad].astype(complex)
    on = np.r_[pad, np.ones_like(nrz), pad]
    x = 3.0 * x * on + (RNG.normal(size=x.size) + 1j * RNG.normal(size=x.size)) / np.sqrt(2)
    # A waterfall row is one short FFT; 128 points at 250 kS/s is 0.5 ms, half a bit.
    n, hop = 128, 32
    w = np.hanning(n)
    rows = np.array([np.fft.fftshift(np.abs(np.fft.fft(w * x[i:i + n])) ** 2)
                     for i in range(0, x.size - n, hop)])
    db = 10 * np.log10(rows / rows.max())
    f = np.fft.fftshift(np.fft.fftfreq(n, 1 / fs)) / 1e3
    t_end = x.size / fs * 1e3
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.imshow(db, aspect="auto", origin="upper", cmap="viridis", vmin=-45, vmax=0,
              extent=[f[0], f[-1], t_end, 0], interpolation="nearest")
    ax.set_xlabel("frequency offset from 433.92 MHz (kHz)")
    ax.set_ylabel("time (ms)")
    ax.set_xlim(-60, 60)
    ax.set_title("Simulated: an FSK burst on a waterfall", color=AMBER, fontsize=11.5, loc="left")
    # The two marks a reader measures: tone spacing and one bit's dwell.
    t0 = 2.0
    ax.annotate("", xy=(dev / 1e3, t0 - 0.8), xytext=(-dev / 1e3, t0 - 0.8),
                arrowprops=dict(arrowstyle="<->", color="white", lw=1.4))
    ax.text(0, t0 - 1.0, "40 kHz", color="white", ha="center", va="bottom", fontsize=10.5, fontweight="bold")
    ax.annotate("", xy=(-34, t0 + 1 / baud * 1e3), xytext=(-34, t0),
                arrowprops=dict(arrowstyle="<->", color="white", lw=1.4))
    ax.text(-36, t0 + 0.5, "1 ms", color="white", ha="right", va="center", fontsize=10.5, fontweight="bold")
    ax.text(42, t0 + 4.0, "preamble", color="white", ha="center", fontsize=10.5)
    ax.text(42, t0 + 16.0, "data", color="white", ha="center", fontsize=10.5)
    write("L08-burst-sim", fig)


if __name__ == "__main__":
    burst_sim()
