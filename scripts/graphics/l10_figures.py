#!/usr/bin/env python3
"""L10 figures (ASCII over PAM).

  L10-ascii-bits : the characters U, S, A as ASCII bytes, as bits sent most
                   significant first, and as 2-PAM levels.
  L10-byte-slip  : the same 24 bits grouped into bytes from the right bit and
                   from one bit late; the late grouping reads 0xAA, 0xA6, 0x82,
                   none of which is a printable ASCII character.
  L10-packet     : one packet of the L10 link to scale: a 64-bit access code,
                   a 32-bit header holding the length twice, and 31 bytes of
                   text, 344 bits in all, or 86 ms at 4 kbaud.

The GNU Radio screenshots (L10-grc-*.png, L10-tx-packet.png, L10-link-*.png)
are not generated here: they are taken from the real flowgraphs in
book/extras/grc/ running under Xvfb (see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l10_figures.py
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

MSG = "USAFA ECE 448: ASCII over PAM."


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


def bits_of(text):
    return [int(b) for c in text.encode() for b in f"{c:08b}"]


def ascii_bits():
    chars = "USA"
    bits = bits_of(chars)
    fig, ax = plt.subplots(figsize=(8.4, 3.3))
    ax.set_xlim(-0.2, 24.2)
    ax.set_ylim(-1.9, 4.6)
    ax.axis("off")
    for k, ch in enumerate(chars):
        x0 = 8 * k
        ax.add_patch(Rectangle((x0 + 0.08, 3.45), 7.84, 0.95, fc="#eef4fa", ec=NAVY, lw=1))
        ax.text(x0 + 4, 3.92, f"'{ch}'  =  0x{ord(ch):02X}", ha="center", va="center", color=NAVY,
                fontsize=12, fontweight="bold")
        for i in range(8):
            ax.text(x0 + i + 0.5, 2.55, str(bits[x0 + i]), ha="center", va="center", fontsize=12, color=INK)
        ax.plot([x0, x0], [-1.6, 3.0], color=GRAY, lw=1, ls=(0, (3, 3)))
    ax.plot([24, 24], [-1.6, 3.0], color=GRAY, lw=1, ls=(0, (3, 3)))
    x = [0]
    y = []
    for i, b in enumerate(bits):
        v = 1 if b else -1
        y += [v, v]
        x += [i + 1, i + 1]
    ax.plot(x[:-1], y, color=NAVY, lw=2)
    ax.axhline(0, xmin=0.008, xmax=0.992, color=RULE, lw=1)
    ax.text(-0.35, 1, "+1", ha="right", va="center", color=GRAY, fontsize=10)
    ax.text(-0.35, -1, "−1", ha="right", va="center", color=GRAY, fontsize=10)
    ax.text(0.05, 1.75, "first bit sent: most significant", ha="left", va="center", color=AMBER, fontsize=10)
    write("L10-ascii-bits", fig)


def byte_slip():
    bits = bits_of("USA")
    fig, ax = plt.subplots(figsize=(8.4, 2.9))
    ax.set_xlim(-0.2, 26.6)
    ax.set_ylim(-0.6, 4.3)
    ax.axis("off")
    for y in (2.75, 1.05):
        for i, b in enumerate(bits):
            ax.text(i + 0.5, y, str(b), ha="center", va="center", fontsize=12, color=INK)

    def groups(start, y, col, labels):
        for k, lab in enumerate(labels):
            x0 = start + 8 * k
            w = min(8, 24 - x0) if x0 < 24 else 0
            if w <= 0:
                break
            ax.add_patch(Rectangle((x0 + 0.06, y - 0.42), w - 0.12, 0.84, fc="none", ec=col, lw=1.4,
                                   ls="-" if w == 8 else (0, (3, 2))))
            ax.text(x0 + w / 2, y + (0.8 if y > 2 else -0.8), lab, ha="center", va="center", color=col,
                    fontsize=11.5, fontweight="bold")

    groups(0, 2.75, NAVY, ["0x55  'U'", "0x53  'S'", "0x41  'A'"])
    groups(1, 1.05, RED, ["0xAA  (not ASCII)", "0xA6  (not ASCII)", "0x82…"])
    ax.text(24.5, 2.75, "from bit 0", ha="left", va="center", color=NAVY, fontsize=10)
    ax.text(24.5, 1.05, "one bit late", ha="left", va="center", color=RED, fontsize=10)
    write("L10-byte-slip", fig)


def packet():
    nbytes = len(MSG) + 1
    parts = [("access code", 64, AMBER), ("header", 32, GREEN), (f"payload: {nbytes} bytes of text", 8 * nbytes, NAVY)]
    total = sum(n for _, n, _ in parts)
    fig, ax = plt.subplots(figsize=(8.4, 1.9))
    ax.set_xlim(-2, total + 2)
    ax.set_ylim(-1.25, 1.5)
    ax.axis("off")
    x = 0
    for name, n, col in parts:
        ax.add_patch(Rectangle((x, 0), n, 0.8, fc=col, ec="white", lw=2, alpha=0.9))
        ax.text(x + n / 2, 0.4, name, ha="center", va="center", color="white", fontsize=11, fontweight="bold")
        ax.text(x + n / 2, -0.32, f"{n} bits", ha="center", va="center", color=INK, fontsize=10.5)
        ax.text(x + n / 2, -0.78, f"{n / 4:g} ms", ha="center", va="center", color=GRAY, fontsize=10)
        x += n
    ax.text(0, 1.18, f"one packet: {total} bits, {total / 4:g} ms at 4 kbaud", ha="left", va="center",
            color=INK, fontsize=11)
    write("L10-packet", fig)


if __name__ == "__main__":
    ascii_bits()
    byte_slip()
    packet()
