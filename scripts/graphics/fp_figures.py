#!/usr/bin/env python3
"""Final Project figures.

  FP-levels : the worked success-level example, an ADS-B generator, as three
              setups that each end at gr-adsb: C from a SigMF recording, B
              from the Pluto's TX port through a 30 dB attenuator and a cable
              into its RX port at 915 MHz, and A over the air at 915 MHz at
              low power.

    python3 scripts/graphics/fp_figures.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, GREEN, GRAY, INK = "#004a85", "#8a5a00", "#3f7d34", "#5b6573", "#15202b"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11})


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


def box(ax, x, y, w, text, color):
    ax.add_patch(FancyBboxPatch((x, y - 0.3), w, 0.6, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc="none", ec=color, lw=1.6))
    ax.text(x + w / 2, y, text, ha="center", va="center", color=color, fontsize=10.5)


def arrow(ax, x0, x1, y, label=None, dashed=False):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.4, linestyle=(0, (4, 3)) if dashed else "-"))
    if label:
        ax.text((x0 + x1) / 2, y + 0.38, label, ha="center", va="bottom", color=GRAY, fontsize=9.5)


def levels():
    fig, ax = plt.subplots(figsize=(9.2, 3.4))
    ax.set_xlim(-0.9, 9.6)
    ax.set_ylim(-0.6, 3.6)
    ax.axis("off")
    rows = [(3.0, "C", GREEN, "SigMF recording", None, False),
            (1.7, "B", AMBER, "Pluto TX", "30 dB pad, cable", False),
            (0.4, "A", NAVY, "Pluto TX", "air, low power", True)]
    for y, lvl, color, src, link, air in rows:
        ax.text(-0.5, y, lvl, ha="center", va="center", color=color, fontsize=16, fontweight="bold")
        box(ax, 0.0, y, 2.0, "ADS-B generator", color)
        if link is None:
            arrow(ax, 2.0, 2.6, y)
            box(ax, 2.6, y, 2.2, src, color)
            arrow(ax, 4.8, 7.0, y)
        else:
            arrow(ax, 2.0, 2.6, y)
            box(ax, 2.6, y, 1.4, src, color)
            arrow(ax, 4.0, 5.2, y, link, dashed=air)
            box(ax, 5.2, y, 1.4, "Pluto RX", color)
            arrow(ax, 6.6, 7.0, y)
        box(ax, 7.0, y, 1.6, "gr-adsb", color)
    ax.text(4.6, -0.35, "B and A at 915 MHz", ha="center", va="center", color=GRAY, fontsize=9.5)
    write("FP-levels", fig)


if __name__ == "__main__":
    levels()
