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

  L10-carrier    : the spectrum and the two constellation sinks of
                   L10-pam-sim.grc, and whether the line arrived, for four runs
                   at Polarity normal: one frequency (phase 0.6 rad), one
                   frequency from another start (phase 0.6 + pi, so the loop
                   locks upside down), 300 Hz apart, and 1.1 kHz apart (TX
                   error fixed at 1100 Hz; RX tuning 800 Hz leaves 300 Hz).
                   Cropped from grc_shot.py screenshots. SIMULATED -- labeled
                   so on the figure. Build with
                   python3 scripts/graphics/l10_figures.py --carrier DIR, where
                   DIR holds c_same.png, c_flip.png, c_300.png, c_1100.png.
  L10-cabling    : the L10 Lab's two hookups: the PlutoSDR's TX port through an
                   SMA cable and the inline 30 dB attenuator to its RX port, and
                   the over-the-air version with an antenna on each port.
  L10-big-picture: the running window of L10-pam-pluto.grc, the one flowgraph
                   every step of the L10 Lab runs, as a map of its controls and
                   displays, each marked with the procedure blocks that use it.

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


def big_picture():
    """The running window of L10-pam-pluto.grc as a map: each control and display, with
    chips for the procedure blocks that use it."""
    from matplotlib.patches import FancyBboxPatch
    img = ROOT / "book/extras/viz/img"
    blocks = [("Steps 1-4", NAVY), ("Steps 5-6", GREEN), ("Steps 7-9", RED), ("Steps 10-13", AMBER)]
    # (label, kind, x, y, w, h, block indices); the window's grid, top to bottom.
    tiles = [("Pluto TX attenuation (dB)", "slider", 0, 5.6, 5, 0.8, [0, 3]),
             ("Pluto RX gain (dB)", "slider", 5, 5.6, 5, 0.8, [3]),
             ("Polarity", "switch", 0, 4.8, 5, 0.8, [0, 1, 2]),
             ("TX oscillator", "switch", 5, 4.8, 5, 0.8, [2, 3]),
             ("RX tuning (Hz)", "slider", 0, 4.0, 10, 0.8, [2, 3]),
             ("Received spectrum", "plot", 0, 2.2, 5, 1.8, [0, 2, 3]),
             ("Received samples", "plot", 5, 2.2, 5, 1.8, [0, 3]),
             ("Before carrier recovery", "plot", 0, 0.4, 5, 1.8, [0, 2]),
             ("After carrier recovery", "plot", 5, 0.4, 5, 1.8, [0, 1, 2]),
             ("Received and Lines labels", "label", 0, -0.4, 10, 0.8, [0, 1, 2, 3])]
    fig, ax = plt.subplots(figsize=(10, 7.6))
    ax.set_xlim(-0.1, 10.1); ax.set_ylim(-0.55, 7.25); ax.axis("off")
    for i, (name, col) in enumerate(blocks):
        x = 0.1 + 2.5 * i
        ax.add_patch(FancyBboxPatch((x, 6.75), 2.2, 0.36, boxstyle="round,pad=0.02,rounding_size=0.12", fc=col, ec=col))
        ax.text(x + 1.1, 6.93, f"{i + 1}  {name}", ha="center", va="center", color="white", fontsize=11, fontweight="bold")
    fill = {"slider": "#f5f9fc", "switch": "#f5f9fc", "plot": "#fbfdff", "label": "#f5f9fc"}
    for name, kind, x, y, w, h, use in tiles:
        ax.add_patch(FancyBboxPatch((x + 0.08, y + 0.06), w - 0.16, h - 0.12,
                                    boxstyle="round,pad=0.0,rounding_size=0.08", fc=fill[kind], ec=RULE, lw=1.4))
        ty = y + h - 0.3 if kind == "plot" else y + h / 2
        ax.text(x + 0.3, ty, name, ha="left", va="center", color=INK, fontsize=11.5,
                fontweight="bold" if kind != "label" else "normal")
        for j, k in enumerate(use):
            cx = x + w - 0.35 - 0.42 * (len(use) - 1 - j)
            ax.add_patch(plt.Circle((cx, ty), 0.15, color=blocks[k][1]))
            ax.text(cx, ty, str(k + 1), ha="center", va="center", color="white", fontsize=10, fontweight="bold")
        if kind == "plot":
            ax.plot([x + 0.4, x + w - 0.4], [y + 0.45, y + 0.45], color=RULE, lw=1)
            ax.plot([x + 0.4, x + 0.4], [y + 0.45, y + h - 0.55], color=RULE, lw=1)
    fig.tight_layout()
    fig.savefig(img / "L10-big-picture.png", dpi=110, facecolor="white")
    plt.close(fig)
    print("wrote L10-big-picture.png")


def cabling():
    """The PlutoSDR cabled TX to RX through the 30 dB attenuator, and with two antennas."""
    from matplotlib.patches import FancyBboxPatch
    img = ROOT / "book/extras/viz/img"
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    for ax, title in zip(axs, ["Every lab day: cable and 30 dB attenuator", "Only when I say so: over the air"]):
        ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
        ax.set_title(title, color=INK, fontsize=12.5, fontweight="bold", loc="left")
        ax.add_patch(FancyBboxPatch((1.0, 0.4), 8.0, 1.6, boxstyle="round,pad=0.05,rounding_size=0.25",
                                    fc="#eef4fa", ec=NAVY, lw=1.6))
        ax.text(5.0, 1.0, "PlutoSDR", ha="center", va="center", color=NAVY, fontsize=13, fontweight="bold")
        for x, lab in ((2.4, "TX"), (7.6, "RX")):
            ax.add_patch(Rectangle((x - 0.3, 2.0), 0.6, 0.45, fc=GRAY, ec=INK, lw=1))
            ax.text(x, 1.65, lab, ha="center", va="center", color=INK, fontsize=12, fontweight="bold")
    ax = axs[0]
    ax.plot([2.4, 2.4, 3.8], [2.45, 3.6, 3.6], color=INK, lw=2.4, solid_capstyle="round")
    ax.add_patch(FancyBboxPatch((3.8, 3.0), 2.4, 1.2, boxstyle="round,pad=0.03,rounding_size=0.15",
                                fc="#fff6e5", ec=AMBER, lw=1.8))
    ax.text(5.0, 3.6, "30 dB\nattenuator", ha="center", va="center", color=AMBER, fontsize=11, fontweight="bold")
    ax.plot([6.2, 7.6, 7.6], [3.6, 3.6, 2.45], color=INK, lw=2.4, solid_capstyle="round")
    ax.text(2.25, 3.0, "SMA cable", ha="right", va="center", color=GRAY, fontsize=10.5)
    ax = axs[1]
    for x in (2.4, 7.6):
        ax.plot([x, x], [2.45, 4.4], color=INK, lw=3.0, solid_capstyle="round")
    ax.text(5.0, 3.6, "TX attenuation\n60 dB or more", ha="center", va="center", color=AMBER, fontsize=11.5, fontweight="bold")
    fig.tight_layout(w_pad=3)
    fig.savefig(img / "L10-cabling.png", dpi=110, facecolor="white")
    plt.close(fig)
    print("wrote L10-cabling.png")


def carrier(shots: Path):
    """Spectrum and constellations before and after the Costas Loop, and the Received
    label, for four runs of L10-pam-sim.grc."""
    img = ROOT / "book/extras/viz/img"
    cols = [("c_same.png", "One frequency"), ("c_flip.png", "One frequency,\nanother start"),
            ("c_300.png", "300 Hz apart"), ("c_1100.png", "1.1 kHz apart")]
    fig = plt.figure(figsize=(10.4, 8.4))
    gs = fig.add_gridspec(4, 4, height_ratios=[0.62, 1, 1, 0.16], hspace=0.12, wspace=0.16)
    rows = ["Spectrum\n(kHz)", "Before the\nCostas Loop", "After the\nCostas Loop", "Received"]
    axes_left = {}
    for c, (f, label) in enumerate(cols):
        im = plt.imread(shots / f)
        # Spectrum sink: -16..+16 kHz over x 92..545; keep -4..+4 kHz around 0 Hz (x 318.5).
        ax = fig.add_subplot(gs[0, c])
        k = 4 * 453 / 32
        ax.imshow(im[228:432, int(318.5 - k):int(318.5 + k)], aspect="auto")
        ax.axvline(k, color=AMBER, lw=1.3, ls="--")
        off = {"c_300.png": 0.3, "c_1100.png": 1.1}.get(f)
        if off:
            ax.axvline(k + off * 453 / 32, color=RED, lw=1.3)
        ax.set_xticks([0, k, 2 * k]); ax.set_xticklabels(["-4", "0", "+4"], fontsize=9)
        ax.set_yticks([])
        ax.set_title(label, color=INK, fontsize=12, fontweight="bold")
        axes_left.setdefault(0, ax)
        # Constellation sinks: -2..2 over 453 px; keep about +-1.2 around each origin.
        for r, x0 in ((1, 318), (2, 851)):
            ax = fig.add_subplot(gs[r, c])
            ax.imshow(im[690 - 140:690 + 140, x0 - 140:x0 + 140])
            ax.axhline(140, color=GRAY, lw=1.0); ax.axvline(140, color=GRAY, lw=1.0)
            ax.text(272, 128, "I", color=INK, fontsize=10, ha="right", va="bottom")
            ax.text(148, 10, "Q", color=INK, fontsize=10, ha="left", va="top")
            ax.set_xticks([]); ax.set_yticks([])
            axes_left.setdefault(r, ax)
        ax = fig.add_subplot(gs[3, c]); ax.axis("off")
        axes_left.setdefault(3, ax)
        ok = "waiting" not in f and "1100" not in f and "flip" not in f
        ax.text(0.5, 0.5, "your line" if ok else "nothing", ha="center", va="center",
                color=NAVY if ok else RED, fontsize=11, fontweight="bold", transform=ax.transAxes)
    fig.subplots_adjust(left=0.13, right=0.99, top=0.93, bottom=0.03)
    for r, t in enumerate(rows):
        bb = axes_left[r].get_position()
        fig.text(0.015, (bb.y0 + bb.y1) / 2, t, ha="left", va="center", color=INK, fontsize=11)
    fig.text(0.99, 0.005, "Simulated: L10-pam-sim.grc, Polarity normal", ha="right", va="bottom", color=GRAY, fontsize=10)
    fig.savefig(img / "L10-carrier.png", dpi=110, facecolor="white")
    plt.close(fig)
    print("wrote L10-carrier.png")


if __name__ == "__main__":
    import sys
    if "--cabling" in sys.argv:
        cabling()
        raise SystemExit
    if "--carrier" in sys.argv:
        carrier(Path(sys.argv[sys.argv.index("--carrier") + 1]))
        raise SystemExit
    if "--big-picture" not in sys.argv:
        ascii_bits()
        byte_slip()
        packet()
    big_picture()
