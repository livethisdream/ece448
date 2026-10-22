#!/usr/bin/env python3
"""L16 figures (frequency hopping).

  L16-hop-frame : one hop of the L16 link to scale: 16 guard bits, the 64-bit
                  access code, the 32-bit header, the 112-bit payload, and 16
                  more guard bits, 240 bits or 240 ms at 1000 baud.
  L16-acquire   : sync on a known hop: the transmitter's channel hop by hop,
                  and the receiver parked on the sync channel until hop 0
                  arrives there, then hopping with it.

The GNU Radio screenshots (L16-grc-*.png, L16-tx-*.png, L16-link-*.png,
L16-pluto-sim.png) are not generated here: they are taken from the real
flowgraphs in book/extras/grc/ running under Xvfb (see CLAUDE.md,
"Flowgraphs").

    python3 scripts/graphics/l16_figures.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, RED, GREEN, GRAY, INK, RULE = "#004a85", "#8a5a00", "#b01e24", "#3f7d34", "#5b6573", "#15202b", "#cddce9"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})

SEQ = [7, 2, 0, 6, 4, 1, 3, 5]      # key 448, as the flowgraphs draw it


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


def hop_frame():
    parts = [("guard", 16, GRAY), ("access code", 64, NAVY), ("header", 32, AMBER),
             ("payload: USAFA ECE 448 + newline", 112, GREEN), ("guard", 16, GRAY)]
    fig, ax = plt.subplots(figsize=(9.0, 1.9))
    ax.set_xlim(-2, 242)
    ax.set_ylim(-1.3, 1.6)
    ax.axis("off")
    x = 0
    for name, n, col in parts:
        ax.add_patch(Rectangle((x, 0), n, 1, fc=col, ec="white", lw=1.5, alpha=0.85))
        ax.text(x + n / 2, 0.5, str(n), ha="center", va="center", color="white", fontsize=11, fontweight="bold")
        ax.text(x + n / 2, 1.3, name, ha="center", va="center", color=col if col != GRAY else INK, fontsize=10)
        x += n
    ax.annotate("", xy=(0, -0.45), xytext=(240, -0.45),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.1, shrinkA=0, shrinkB=0))
    ax.text(120, -0.95, "one hop: 240 bits = 240 ms at 1000 baud", ha="center", va="center", color=INK, fontsize=10.5)
    write("L16-hop-frame", fig)


def acquire():
    n_hops, start, park = 14, 3, SEQ[0]
    fig, ax = plt.subplots(figsize=(9.0, 3.1))
    ax.set_xlim(0, n_hops)
    ax.set_ylim(-0.5, 9.0)
    ax.set_yticks(range(8))
    ax.spines['left'].set_bounds(-0.5, 7.5)
    ax.set_xticks(range(0, n_hops + 1, 2))
    ax.set_xlabel("time (hops of 240 ms)", fontsize=10, color=GRAY)
    ax.set_ylabel("channel", fontsize=10, color=GRAY)
    for c in range(8):
        ax.axhline(c, color=RULE, lw=0.6, zorder=0)
    lock = None
    for h in range(n_hops):
        k = (start + h) % 8
        if lock is None and k == 0:
            lock = h
        ax.add_patch(Rectangle((h + 0.06, SEQ[k] - 0.32), 0.88, 0.64, fc=NAVY, ec="none", alpha=0.85))
        rx = park if lock is None else SEQ[k]
        ax.add_patch(Rectangle((h + 0.02, rx - 0.42), 0.96, 0.84, fc="none", ec=AMBER, lw=1.8,
                               ls=(0, (3, 2)) if lock is None else "-"))
    ax.annotate("receiver parked on the sync channel", xy=(2.5, park + 0.45), xytext=(0.2, 8.5),
                fontsize=10, color=AMBER, arrowprops=dict(arrowstyle="->", color=AMBER, lw=1))
    ax.annotate("hop 0 arrives: lock", xy=(lock + 0.5, park + 0.45), xytext=(lock + 1.4, 8.5),
                fontsize=10, color=AMBER, arrowprops=dict(arrowstyle="->", color=AMBER, lw=1))
    ax.text(n_hops - 2.6, -1.9, "filled: transmitter", ha="right", va="center", fontsize=10, color=NAVY)
    ax.text(n_hops - 0.1, -1.9, "box: receiver", ha="right", va="center", fontsize=10, color=AMBER)
    write("L16-acquire", fig)


if __name__ == "__main__":
    hop_frame()
    acquire()
