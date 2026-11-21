#!/usr/bin/env python3
"""L5 figures (GNU Radio introduction).

  L05-fm-band-sim : what the broadcast FM band looks like on the L5 flowgraph's
                    QT GUI Sink: four stations, the receiver's own DC spike at
                    the center, and the noise floor, as a spectrum over a
                    waterfall, with the f_c +/- f_s/2 span bracketed.
                    SIMULATED -- labeled so on the figure.
  L05-gain-three  : the same band at too little, about the right, and too much
                    RF gain. SIMULATED -- labeled so on the figure.
  L05-iq-bytes    : the byte layout of a cf32_le recording and its meta file.
  L05-pluto-ports : the PlutoSDR's two ends: TX and RX SMA, data and power USB.
  L05-big-picture : the L5 Lab's three runs (tone flowgraph, FM band, PSD of
                    the recording) as one strip; PNG, from the screenshots.

The lab figures use the lesson's settings (32 kHz, 100.1 MHz) or the L7
simulated recording (100.0 MHz), never the lab's, so none shows a Part 1
answer. L05-psd-sim.png is L05-psd.py's own plot of L07-fm-test.sigmf-data,
written by L07-fm-test-tx.grc, with "Simulated" added.

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


STATIONS = [(99.3, -62), (99.9, -48), (100.3, -38), (100.9, -55)]   # MHz, peak dB


def band(fc, fs, n, gain_db=0.0, floor_db=-95.0, clip=None, rows=1):
    """Rows of a simulated FM band spectrum, in dB, at a relative RF gain."""
    f = fc + np.linspace(-fs / 2, fs / 2, n)
    out = np.empty((rows, n))
    for r in range(rows):
        p = 10 ** (floor_db / 10) * np.ones(n)
        for f0, pk in STATIONS:
            w = 0.07 + 0.015 * np.sin(r / 9 + f0)
            c = f0 + 0.02 * np.sin(r / 5 + 3 * f0)
            p += 10 ** ((pk + gain_db) / 10) * np.exp(-0.5 * ((f - c) / w) ** 6)
        p[np.argmin(np.abs(f - fc)) + np.arange(-1, 2)] += 10 ** (-60 / 10)
        out[r] = 10 * np.log10(p * RNG.exponential(1.0, n))
    return f, out


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
    a1.set_ylim(-112, -20)
    a1.grid(True, color=RULE, lw=0.8)
    for f0, pk in stations:
        a1.text(f0, pk + 4, f"{f0:.1f}", ha="center", color=NAVY, fontsize=10.5, fontweight="bold")
    a1.annotate("DC spike", (fc, -60), xytext=(fc - 0.22, -27), color=RED, fontsize=10.5, ha="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    a1.text(f[0] + 0.02, -91, "noise floor", color=GRAY, fontsize=10, va="bottom")
    a1.annotate("", (f[0], -106), (f[-1], -106), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.0))
    a1.text(fc + 0.55, -105.5, r"display span: $f_c - f_s/2$  to  $f_c + f_s/2$", color=GRAY, fontsize=10, ha="center", va="bottom")
    a1.set_title("Simulated: the FM band around 100.1 MHz, sampled at 2.4 MS/s", color=AMBER, fontsize=11.5, loc="left")
    a2.imshow(wf, aspect="auto", extent=[f[0], f[-1], rows, 0], cmap="viridis", vmin=-100, vmax=-35)
    a2.set_ylabel("time (newest at top)")
    a2.set_yticks([])
    a2.set_xlabel("frequency (MHz)")
    write("L05-fm-band-sim", fig)


def gain_three():
    """Too little, about right, too much: the floor, the stations, and spurs."""
    fc, fs, n = 100.1, 2.4, 1024
    adc = -88.0                                     # the converter's own floor, dBFS
    panels = [("Too little gain", -25.0, -114.0), ("About right", 5.0, -84.0), ("Too much gain", 35.0, -54.0)]
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    for ax, (title, g, ant) in zip(axs, panels):
        f, sp = band(fc, fs, n, gain_db=g, floor_db=10 * np.log10(10 ** (adc / 10) + 10 ** (ant / 10)), rows=40)
        spec = 10 * np.log10(np.mean(10 ** (sp / 10), axis=0))
        if g > 20:
            spec = np.minimum(spec, -6 + 0.6 * RNG.standard_normal(n))      # clipped tops
            # copies of strong stations where nothing transmits (intermodulation)
            for f0, lvl in [(99.5, -40), (100.7, -44), (101.1, -50), (99.1, -52)]:
                spec = np.maximum(spec, lvl - 2 + 10 * np.log10(np.exp(-0.5 * ((f - f0) / 0.05) ** 4) + 1e-9))
            spec += 6 * np.exp(-0.5 * ((f - 100.3) / 0.6) ** 2)               # raised, uneven floor
        ax.plot(f, spec, color=NAVY, lw=1.1)
        ax.axhline(adc, color=GRAY, lw=0.8, ls=":")
        ax.set_title(title, color=INK, fontsize=11.5, fontweight="bold")
        ax.set_ylim(-100, 0)
        ax.grid(True, color=RULE, lw=0.8)
        ax.set_xlabel("frequency (MHz)")
    axs[0].set_ylabel("power (dBFS)")
    axs[0].text(f[0] + 0.03, adc + 1.5, "converter floor", color=GRAY, fontsize=9.5, va="bottom")
    axs[2].text(99.55, -70, "spurs", color=RED, fontsize=10, ha="center", fontweight="bold")
    fig.suptitle("Simulated: the FM band around 100.1 MHz at three RF gains", color=AMBER, fontsize=11.5, x=0.01, ha="left")
    fig.tight_layout()
    write("L05-gain-three", fig)


def iq_bytes():
    """cf32_le: I then Q, 4 bytes each, no header; the meta file says how to read it."""
    from matplotlib.patches import FancyBboxPatch, Rectangle
    fig, ax = plt.subplots(figsize=(8, 2.4))
    ax.set_xlim(0, 16); ax.set_ylim(0, 4.4); ax.axis("off")
    for k in range(5):
        x = 0.2 + 2.0 * k
        for j, (lab, col) in enumerate([("I", NAVY), ("Q", "#3f7d34")]):
            ax.add_patch(Rectangle((x + j, 2.0), 1.0, 1.0, fc="white", ec=col, lw=1.6))
            ax.text(x + j + 0.5, 2.5, f"{lab}$_{k}$", ha="center", va="center", color=col, fontsize=12)
    ax.text(10.5, 2.5, "...", ha="left", va="center", color=GRAY, fontsize=14)
    ax.annotate("", (0.2, 1.7), (2.2, 1.7), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text(1.2, 1.25, "one sample: 8 bytes", ha="center", color=INK, fontsize=10.5)
    ax.text(0.2, 3.45, "fm_capture.sigmf-data: no header", color=INK, fontsize=11)
    ax.add_patch(FancyBboxPatch((12.0, 0.9), 3.8, 2.7, boxstyle="round,pad=0.08", fc="#f5f9fc", ec=AMBER, lw=1.4))
    ax.text(13.8, 3.25, "fm_capture.sigmf-meta", ha="center", color=AMBER, fontsize=10.5, fontweight="bold")
    for i, t in enumerate(["datatype: cf32_le", "sample_rate", "frequency"]):
        ax.text(12.25, 2.55 - 0.55 * i, t, color=INK, fontsize=10.5, family="monospace")
    write("L05-iq-bytes", fig)


def pluto_ports():
    """The PlutoSDR's two ends, labeled; a line drawing, not to scale."""
    from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 2.8))
    for ax, title in [(a1, "SMA end"), (a2, "USB end")]:
        ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off"); ax.set_aspect("equal")
        ax.add_patch(FancyBboxPatch((0.6, 1.4), 8.8, 3.2, boxstyle="round,pad=0.15", fc="#eef4fa", ec=GRAY, lw=1.4))
        ax.text(5, 5.35, title, ha="center", color=INK, fontsize=11.5, fontweight="bold")
    for x, lab, col in [(3.0, "TX", GRAY), (7.0, "RX", NAVY)]:
        a1.add_patch(Circle((x, 3.0), 0.75, fc="#d8c38a", ec=INK, lw=1.2))
        a1.add_patch(Circle((x, 3.0), 0.25, fc="white", ec=INK, lw=1.0))
        a1.text(x, 0.6, lab, ha="center", color=col, fontsize=12, fontweight="bold")
    a1.text(7.0, 0.05, "antenna here", ha="center", color=NAVY, fontsize=9.5)
    for x, lab, col in [(3.0, "data + power", NAVY), (7.0, "power only", GRAY)]:
        a2.add_patch(Rectangle((x - 0.6, 2.7), 1.2, 0.55, fc="white", ec=INK, lw=1.2))
        a2.text(x, 0.6, lab, ha="center", color=col, fontsize=11, fontweight="bold")
    a2.text(3.0, 0.05, "laptop here", ha="center", color=NAVY, fontsize=9.5)
    write("L05-pluto-ports", fig)


def big_picture():
    """The lab's three runs as one strip. PNG: two panels are screenshots."""
    img = ROOT / "book/extras/viz/img"
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.3), gridspec_kw={"width_ratios": [1.15, 1, 1]})
    axs[0].imshow(plt.imread(img / "L05-grc-tone.png")); axs[0].axis("off")
    f, sp = band(100.1, 2.4, 1024, rows=40)
    axs[1].plot(f, 10 * np.log10(np.mean(10 ** (sp / 10), axis=0)), color=NAVY, lw=1.0)
    axs[1].set_ylim(-100, -25); axs[1].set_yticks([]); axs[1].set_xlabel("frequency (MHz)", fontsize=9.5)
    axs[1].tick_params(labelsize=9); axs[1].text(0.02, 0.95, "Simulated", transform=axs[1].transAxes, color=AMBER, fontsize=10, fontweight="bold", va="top")
    axs[2].imshow(plt.imread(img / "L05-psd-sim.png")); axs[2].axis("off")
    for ax, t in zip(axs, ["Steps 1-7: build a tone flowgraph", "Steps 8-12: receive the FM band", "Steps 13-17: record and plot it"]):
        ax.set_title(t, color=INK, fontsize=11.5, fontweight="bold")
    for x in (0.395, 0.69):
        fig.text(x, 0.5, "\u2192", fontsize=22, color=GRAY, ha="center", va="center")
    fig.tight_layout(w_pad=2.5)
    fig.savefig(img / "L05-big-picture.png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    print("wrote L05-big-picture.png")


if __name__ == "__main__":
    fm_band_sim()
    gain_three()
    iq_bytes()
    pluto_ports()
    big_picture()
