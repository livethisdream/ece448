#!/usr/bin/env python3
"""L15 figures (mPSK).

  L15-ber-measured : bit error rate against Eb/N0, L3's theory curves for
                     BPSK/QPSK and 8PSK with the L15 link's measured points,
                     with and without differential coding, at even dB
  L15-8psk-map     : the L15 8PSK constellation: phase index i at 22.5 + 45i
                     degrees, and the Gray label each point carries
  L15-costas       : the Costas Loop as a block diagram: rotate, decide the
                     phase error, filter it, and update the phase estimate

The measured points were taken with the blocks of book/extras/grc/
L15-psk-link.grc running headless without the Throttle (RRC alpha 0.35, 8
samples per symbol, Symbol Sync with Gardner at loop bandwidth 0.045, Costas
Loop at 0.02, 100 ppm left out), each point over 2.9e5 to 1.2e7 bits, aligned
against the transmitted bits. Without differential coding, a cycle slip of the
Costas Loop rotates every later decision, so QPSK below 4 dB and 8PSK below
10 dB measured near 0.5 and are left off the plot. The points are typed in below rather than re-measured
here, so this script needs only matplotlib.

The GNU Radio screenshots (L15-grc-*.png, L15-tx-*.png, L15-link-*.png,
L15-pluto-sim.png) are not generated here: they are taken from the real
flowgraphs running under Xvfb (see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l15_figures.py
"""

from __future__ import annotations

import io
import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, RED, GREEN, GRAY, INK, RULE = "#004a85", "#8a5a00", "#b01e24", "#3f7d34", "#5b6573", "#15202b", "#cddce9"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})

# Measured bit error rate of the L15 link, by Eb/N0 in dB (even values only;
# the L15 Lab measures the odd ones).
MEASURED = {
    ("QPSK", False): {4: 1.56e-2, 6: 3.15e-3, 8: 2.74e-4, 10: 7.77e-6},
    ("QPSK", True): {4: 3.01e-2, 6: 6.14e-3, 8: 6.23e-4, 10: 1.27e-5},
    ("8PSK", False): {10: 1.41e-3, 12: 1.09e-4, 14: 1.75e-6},
    ("8PSK", True): {8: 1.56e-2, 10: 2.69e-3, 12: 2.07e-4, 14: 4.18e-6},
}


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


def Q(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def theory(mod, eb_db):
    """L3's curves: BPSK and QPSK exact, 8PSK nearest-neighbor with Gray coding."""
    g = 10 ** (eb_db / 10)
    if mod == "QPSK":
        return Q(math.sqrt(2 * g))
    return 2 / 3 * Q(math.sqrt(6 * g) * math.sin(math.pi / 8))


def ebn0_for(points, target):
    """Eb/N0 where a measured curve crosses target, by log-linear interpolation."""
    xs = sorted(points)
    for a, b in zip(xs, xs[1:]):
        ya, yb = math.log10(points[a]), math.log10(points[b])
        t = math.log10(target)
        if ya >= t >= yb:
            return a + (b - a) * (ya - t) / (ya - yb)
    return float("nan")


def ber_measured():
    x = np.linspace(0, 16, 400)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    for mod, col in (("QPSK", NAVY), ("8PSK", AMBER)):
        lab = "BPSK and QPSK, theory" if mod == "QPSK" else "8PSK, theory"
        ax.semilogy(x, [theory(mod, v) for v in x], color=col, lw=2, label=lab)
        for diff, mk in ((False, "o"), (True, "s")):
            pts = MEASURED[(mod, diff)]
            ax.semilogy(list(pts), list(pts.values()), mk, color=col, ms=7,
                        mfc="white" if diff else col, mew=1.8,
                        label=f"{mod}, measured" + (", differential" if diff else ""))
        for target in (1e-4,):
            th = next(v for v in np.arange(0, 20, 0.001) if theory(mod, v) <= target)
            print(f"  {mod} BER {target:.0e}: theory {th:5.2f} dB, measured "
                  f"{ebn0_for(MEASURED[(mod, False)], target):5.2f} dB, "
                  f"differential {ebn0_for(MEASURED[(mod, True)], target):5.2f} dB")
    for (mod, diff), pts in MEASURED.items():
        for e, b in pts.items():
            print(f"  {mod:4s} {'diff ' if diff else 'plain'} {e:2d} dB: measured {b:.2e}, theory {theory(mod, e):.2e}, ratio {b / theory(mod, e):.2f}")
    ax.set_ylim(1e-7, 0.2)
    ax.set_xlim(0, 16)
    ax.set_xlabel("Eb/N0 (dB)")
    ax.set_ylabel("bit error rate")
    ax.grid(True, which="major", color=RULE, lw=0.8)
    ax.legend(frameon=False, loc="lower left", fontsize=9.5)
    write("L15-ber-measured", fig)


def map_8psk():
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    ax.set_aspect("equal")
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.75, 1.75)
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero")
        ax.spines[s].set_color(RULE)
    ax.set_xticks([])
    ax.set_yticks([])
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color=RULE, lw=1, ls=(0, (3, 3)), zorder=0)
    gray = [i ^ (i >> 1) for i in range(8)]
    for i in range(8):
        a = math.pi / 8 + math.pi / 4 * i
        ax.scatter([math.cos(a)], [math.sin(a)], s=60, color=NAVY, zorder=3)
        ax.text(1.36 * math.cos(a), 1.36 * math.sin(a), f"{gray[i]:03b}", ha="center", va="center",
                color=NAVY, fontsize=13, fontweight="bold", family="monospace")
        ax.text(0.74 * math.cos(a), 0.74 * math.sin(a), str(i), ha="center", va="center", color=AMBER, fontsize=11)
    ax.text(1.72, -0.12, "I", color=GRAY, ha="right", va="top")
    ax.text(0.08, 1.72, "Q", color=GRAY, ha="left", va="top")
    print("  8PSK phase index -> Gray label:", [f"{i}:{gray[i]:03b}" for i in range(8)])
    print("  8PSK Gray value -> phase index (the transmitter's Map):", [gray.index(b) for b in range(8)])
    write("L15-8psk-map", fig)


def costas():
    fig, ax = plt.subplots(figsize=(8.4, 2.7))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 3.0)
    ax.axis("off")

    def box(x, y, w, h, text):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="#eef4fa", ec=NAVY, lw=1.6))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=INK, fontsize=10.5)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.5, shrinkA=0, shrinkB=0))

    def line(xs, ys):
        ax.plot(xs, ys, color=GRAY, lw=1.5, solid_capstyle="butt")

    box(1.5, 1.9, 2.2, 0.8, "rotate back\nby the estimate")
    box(7.0, 0.25, 2.4, 0.8, "phase error\n(order M)")
    box(4.3, 0.25, 2.0, 0.8, "loop filter")
    box(1.5, 0.25, 2.2, 0.8, "phase estimate")
    ax.text(0.0, 2.3, "symbols\nin", ha="left", va="center", color=GRAY, fontsize=10)
    arrow(0.75, 2.3, 1.5, 2.3)
    arrow(3.7, 2.3, 9.2, 2.3)
    ax.text(9.3, 2.3, "symbols\nout", ha="left", va="center", color=GRAY, fontsize=10)
    line([8.2, 8.2], [2.3, 1.4])
    arrow(8.2, 1.4, 8.2, 1.05)
    arrow(7.0, 0.65, 6.3, 0.65)
    arrow(4.3, 0.65, 3.7, 0.65)
    arrow(2.6, 1.05, 2.6, 1.9)
    line([5.3, 5.3], [1.05, 1.5])
    ax.text(5.3, 1.62, "frequency estimate", ha="center", va="bottom", color=GRAY, fontsize=10)
    write("L15-costas", fig)


if __name__ == "__main__":
    ber_measured()
    map_8psk()
    costas()
