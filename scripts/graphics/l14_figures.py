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
    (cd DIR && python3.12 L14_hd_test_tx.py)               # writes L14-hd-test.sigmf-data and .sigmf-meta
    (cd DIR && xvfb-run python3.12 scripts/grc/grc_shot.py --size 1060x1000 L14_hd_find.py find.png 12)
    # find_noise.png: the same, on a test file written with noise_amp = 0.15
    scripts/grc/grc_canvas.sh book/extras/grc/L14-hd-find.grc DIR/canvas_find.png 1800x1100
    scripts/grc/grc_canvas.sh book/extras/grc/L14-hd-test-tx.grc DIR/canvas_tx.png 1800x1000

L14-hd-scan is the spectrum and waterfall half of find.png, the first look at
the band that opens the lesson.

The demodulation figures come from L14-hd-demod.grc and L14-hd-rx.grc. Their
recording is nrsc5's sample capture of KUT 90.5 (support/sample.xz in the nrsc5
repository, unpacked as sample), a real station, so only the runs on the test
file or with added noise carry a stamp. Take the GUI shots at twice the size:

    grcc -o DIR book/extras/grc/L14-hd-demod.grc     # set iq_file per run
    QT_SCALE_FACTOR=2 xvfb-run -s "-screen 0 3000x1800x24" python3.12 \
        scripts/grc/grc_shot.py --size 1400x820 L14_hd_demod.py demod_kut.png 10
    # demod_noise.png: the same with noise_amp=0.015
    scripts/grc/grc_canvas.sh book/extras/grc/L14-hd-demod.grc DIR/canvas_demod.png 1880x1060
    scripts/grc/grc_canvas.sh book/extras/grc/L14-hd-rx.grc DIR/canvas_rx.png 1880x1060

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
    save(stamp(find.crop((0, 362, 1060, 1000)), (1020, 50)), "L14-hd-scan", colors=16)
    save(Image.open(raw / "canvas_find.png").crop((0, 68, 1700, 1100)), "L14-grc-find", colors=64)
    save(Image.open(raw / "canvas_tx.png").crop((0, 68, 1790, 940)), "L14-grc-test-tx", colors=64)


def demod_shots(raw: Path):
    """Panels of L14-hd-demod.grc, from shots at twice the window size."""
    from PIL import Image, ImageDraw, ImageFont

    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    box = {"spectrum": (20, 20, 1130, 790), "prefix": (1130, 20, 1950, 790),
           "score": (1950, 20, 2750, 790), "bpsk": (20, 790, 1120, 1630),
           "qpsk": (1130, 790, 1950, 1630)}

    def row(shot, panels, label=None):
        im = Image.open(raw / shot).convert("RGB")
        parts = [im.crop(box[p]) for p in panels]
        out = Image.new("RGB", (sum(p.size[0] for p in parts), max(p.size[1] for p in parts)), "white")
        x = 0
        for p in parts:
            out.paste(p, (x, 0))
            x += p.size[0]
        if label:  # in a strip of its own, clear of the plot titles
            framed = Image.new("RGB", (out.size[0], out.size[1] + 64), "white")
            framed.paste(out, (0, 64))
            out = framed
            d = ImageDraw.Draw(out)
            xy = (out.size[0] - 30, 14)
            x0, y0, x1, y1 = d.textbbox(xy, label, font=f, anchor="ra")
            d.rectangle((x0 - 12, y0 - 8, x1 + 12, y1 + 8), fill="#fdf0d5")
            d.text(xy, label, font=f, fill=AMBER, anchor="ra")
        return out

    def save(im, name, colors=48):
        im = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        for out in SHOTS:
            out.mkdir(parents=True, exist_ok=True)
            im.save(out / f"{name}.png", optimize=True)
        print(f"wrote {name}.png ({(SHOTS[0] / f'{name}.png').stat().st_size // 1024} KB)")

    save(row("demod_kut.png", ["spectrum", "prefix"]), "L14-demod-symbols")
    save(row("demod_kut.png", ["score", "bpsk"]), "L14-demod-refs")
    save(row("demod_kut.png", ["qpsk"]), "L14-demod-qpsk")
    save(row("demod_noise.png", ["score", "qpsk"], "Added noise 0.015"), "L14-demod-noise")
    for name in ("demod", "rx"):
        canvas = Image.open(raw / f"canvas_{name}.png").convert("RGB")
        save(canvas.crop((0, 68, canvas.size[0], canvas.size[1])), f"L14-grc-{name}", colors=64)


if __name__ == "__main__":
    hybrid()
    if len(sys.argv) > 1:
        raw = Path(sys.argv[1])
        if (raw / "find.png").exists():
            shots(raw)
        if (raw / "demod_kut.png").exists():
            demod_shots(raw)
