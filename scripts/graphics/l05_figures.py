#!/usr/bin/env python3
"""L5 figures (GNU Radio introduction).

  L05-fm-band-sim : what the broadcast FM band looks like on the L5 flowgraph's
                    QT GUI Sink: four stations, the receiver's own DC spike at
                    the center, and the noise floor, as a spectrum over a
                    waterfall. SIMULATED -- labeled so on the figure.

The GNU Radio screenshots (L05-grc-*.png, L05-tone-*.png) are not generated
here: they are taken from the real flowgraphs in book/extras/grc/ running
under Xvfb (see project/ROADMAP.md, "Flowgraphs").

    python3 scripts/graphics/l05_figures.py
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
RNG = np.random.default_rng(5)


def write(name, fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = apply_font_stack(buf.getvalue()[buf.getvalue().index("<svg"):])
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


def fm_band_sim():
    fc, fs, n = 100.1, 2.4, 1024
    f = fc + np.linspace(-fs / 2, fs / 2, n)
    stations = [(99.3, -62), (99.9, -48), (100.3, -38), (100.9, -55)]   # MHz, peak dB
    rows = 120
    wf = np.empty((rows, n))
    for r in range(rows):
        p = 10 ** (-95 / 10) * np.ones(n)                                 # noise floor
        for f0, pk in stations:
            # A wideband FM station is about 200 kHz wide and its shape moves
            # with the program audio; model that as a wandering bump.
            w = 0.07 + 0.015 * np.sin(r / 9 + f0)
            c = f0 + 0.02 * np.sin(r / 5 + 3 * f0)
            p += 10 ** (pk / 10) * np.exp(-0.5 * ((f - c) / w) ** 6)
        p[np.argmin(np.abs(f - fc)) + np.arange(-1, 2)] += 10 ** (-60 / 10)  # DC spike
        wf[r] = 10 * np.log10(p * RNG.exponential(1.0, n))
    spec = 10 * np.log10(np.mean(10 ** (wf / 10), axis=0))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True, gridspec_kw={"height_ratios": [1, 1.1]})
    a1.plot(f, spec, color=NAVY, lw=1.2)
    a1.set_ylabel("power (dB)")
    a1.set_ylim(-100, -20)
    a1.grid(True, color=RULE, lw=0.8)
    for f0, pk in stations:
        a1.text(f0, pk + 4, f"{f0:.1f}", ha="center", color=NAVY, fontsize=10.5, fontweight="bold")
    a1.annotate("DC spike", (fc, -60), xytext=(fc - 0.22, -27), color=RED, fontsize=10.5, ha="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    a1.text(f[0] + 0.02, -91, "noise floor", color=GRAY, fontsize=10, va="bottom")
    a1.set_title("Simulated: the FM band around 100.1 MHz, sampled at 2.4 MS/s", color=AMBER, fontsize=11.5, loc="left")
    a2.imshow(wf, aspect="auto", extent=[f[0], f[-1], rows, 0], cmap="viridis", vmin=-100, vmax=-35)
    a2.set_ylabel("time (newest at top)")
    a2.set_yticks([])
    a2.set_xlabel("frequency (MHz)")
    write("L05-fm-band-sim", fig)


if __name__ == "__main__":
    fm_band_sim()
