#!/usr/bin/env python3
"""L14 figures (HD Radio).

  L14-hybrid      : where a hybrid HD Radio station puts its signals: the analog
                    FM host around the channel center, and the two primary main
                    OFDM sidebands from subcarrier 356 to 546 on each side,
                    129,361 to 198,402 Hz, with their ten frequency partitions.
                    A layout of NRSC-5 (SY_IDD_1011s, Table 5-1), not a
                    measurement, so the levels are schematic and the axis
                    carries none.

The GNU Radio screenshots are taken from the real flowgraphs in
book/extras/grc/ running under Xvfb (see CLAUDE.md, "Flowgraphs"); this script
only crops them, stamps "Simulated: L14 test file" on every one that shows the
test file, and reduces them to a palette so they stay small. Make the raw
shots first, in one folder:

    grcc -o DIR book/extras/grc/L14-hd-test-tx.grc book/extras/grc/L14-hd-find.grc
    (cd DIR && python3.12 L14_hd_test_tx.py)               # writes L14-hd-test.cu8
    (cd DIR && xvfb-run python3.12 scripts/grc/grc_shot.py --size 1060x1000 L14_hd_find.py find.png 12)
    # find_noise.png: the same, on a test file written with noise_amp = 0.15
    scripts/grc/grc_canvas.sh book/extras/grc/L14-hd-find.grc DIR/canvas_find.png 1800x1000
    scripts/grc/grc_canvas.sh book/extras/grc/L14-hd-test-tx.grc DIR/canvas_tx.png 1800x1000

GQRX (apt install gqrx-sdr) plays the same test file, converted to complex
float, through its file input, device string
"file=hd.cf32,rate=1488375,freq=100300000,repeat=true,throttle=true", in WFM
mode with DSP started; its window at 1060x666 is DIR/gqrx.png. GQRX needs a
PulseAudio server, so run it under xvfb-run with pulseaudio and a null sink.

    python3 scripts/graphics/l14_figures.py [DIR]
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
SHOTS = (ROOT / "book/extras/viz/img", ROOT / "book/extras/slides/img/14-hd-radio")
NAVY, BLUE, AMBER, RED, GREEN = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#3f7d34"
GRAY, INK, RULE, PALE = "#5b6573", "#15202b", "#cddce9", "#eef4fa"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False})

DF = 1488375 / 4096          # OFDM subcarrier spacing, Hz


def write(name, fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = apply_font_stack(buf.getvalue()[buf.getvalue().index("<svg"):])
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


def hybrid():
    fig, ax = plt.subplots(figsize=(8.4, 3.1))
    # analog FM host: most of its power within about 100 kHz of center
    xs = [x / 2 for x in range(-220, 221)]
    ys = [0.92 * 2.718 ** (-(x / 42) ** 2) for x in xs]
    ax.fill_between(xs, ys, color=NAVY, alpha=0.85, lw=0)
    ax.text(0, 0.36, "analog FM\nhost", ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
    lo, hi = 356 * DF / 1e3, 546 * DF / 1e3
    for sgn in (1, -1):
        a, b = sorted((sgn * lo, sgn * hi))
        ax.add_patch(Rectangle((a, 0), b - a, 0.2, color=BLUE, alpha=0.6, lw=0))
        for p in range(1, 10):   # ten frequency partitions of 19 subcarriers
            x = sgn * (356 + 19 * p) * DF / 1e3
            ax.plot([x, x], [0, 0.2], color="white", lw=0.8)
        ax.text((a + b) / 2, 0.27, "OFDM sideband\n10 partitions", ha="center", va="bottom", color=NAVY, fontsize=10)
        ax.annotate("", xy=(a, 0.62), xytext=(b, 0.62), arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1))
        ax.text((a + b) / 2, 0.65, "69 kHz", ha="center", va="bottom", color=GRAY, fontsize=9.5)
    ax.text(lo, -0.17, "#356", ha="center", va="top", color=BLUE, fontsize=9)
    ax.text(hi, -0.17, "#546", ha="center", va="top", color=BLUE, fontsize=9)
    ax.text(-lo, -0.17, "#−356", ha="center", va="top", color=BLUE, fontsize=9)
    ax.text(-hi, -0.17, "#−546", ha="center", va="top", color=BLUE, fontsize=9)
    ax.set_xlim(-215, 215)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([])
    ax.set_xticks([-198.4, -129.4, 0, 129.4, 198.4])
    ax.set_xticklabels(["−198.4", "−129.4", "0", "129.4", "198.4"])
    ax.set_xlabel("frequency from the channel center (kHz)", labelpad=16)
    write("L14-hybrid", fig)


def shots(raw: Path):
    from PIL import Image, ImageDraw, ImageFont

    def font(size):
        for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",):
            if Path(f).exists():
                return ImageFont.truetype(f, size)
        return ImageFont.load_default()

    def stamp(im, xy, text="Simulated: L14 test file"):
        d = ImageDraw.Draw(im)
        f = font(17)
        x0, y0, x1, y1 = d.textbbox(xy, text, font=f, anchor="ra")
        d.rectangle((x0 - 6, y0 - 4, x1 + 6, y1 + 4), fill="#fdf0d5")
        d.text(xy, text, font=f, fill=AMBER, anchor="ra")
        return im

    def save(im, name, colors=96):
        im = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        for out in SHOTS:
            out.mkdir(parents=True, exist_ok=True)
            im.save(out / f"{name}.png", optimize=True)
        print(f"wrote {name}.png ({(SHOTS[0] / f'{name}.png').stat().st_size // 1024} KB)")

    find = Image.open(raw / "find.png").convert("RGB")
    save(stamp(find.copy(), (1020, 412)), "L14-hd-find", colors=16)
    save(stamp(find.crop((0, 0, 1060, 362)), (1020, 70)), "L14-hd-meters", colors=32)
    noisy = Image.open(raw / "find_noise.png").convert("RGB")
    save(stamp(noisy, (1020, 412), "Simulated: test file, noise_amp 0.15"), "L14-hd-noise", colors=12)
    gq = Image.open(raw / "gqrx.png").convert("RGB").crop((0, 0, 1060, 666))
    save(stamp(gq, (745, 128)).resize((848, 533)), "L14-gqrx", colors=32)
    save(Image.open(raw / "canvas_find.png").crop((0, 68, 1700, 1000)), "L14-grc-find", colors=64)
    save(Image.open(raw / "canvas_tx.png").crop((0, 68, 1760, 940)), "L14-grc-test-tx", colors=64)


if __name__ == "__main__":
    hybrid()
    if len(sys.argv) > 1:
        shots(Path(sys.argv[1]))
