#!/usr/bin/env python3
"""L2 figures (noise figure and link budget).

  L02-link-ledger   : the drone link as a level diagram, transmitter to
                      receiver, against the noise floor and the sensitivity
  L02-ism-bands     : the US ISM bands on a log frequency axis, against the
                      tuning ranges of the course SDRs
  L02-noise-cascade : the same three parts in two orders, with the system
                      noise figure of each
  L02-antenna-patterns : an omnidirectional and a directional antenna's
                      gain patterns, with the half-power beamwidth marked
  L02-atmosphere    : sea-level attenuation by oxygen and water vapor,
                      1 to 350 GHz (ITU-R P.676, through the itur package)

Every plotted number is computed here and printed for checking against the
lesson text. Words and numbers only, no equations, so one SVG serves both the
deck and the page.

    python3 scripts/graphics/l02_figures.py
    -> book/extras/slides/fig/L02-*.svg  and  book/extras/viz/img/L02-*.svg
"""

from __future__ import annotations

import math
from pathlib import Path

from svg_font_stack import apply_font_stack

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")

NAVY, BLUE, AMBER, RED, GREEN = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#3f7d34"
GRAY, INK, RULE, PALE = "#5b6573", "#15202b", "#cddce9", "#eef4fa"

C = 299_792_458.0


def write(name: str, svg: str) -> None:
    svg = apply_font_stack(svg)
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
    print(f"wrote {name}.svg")


def db(x: float) -> float:
    return 10 * math.log10(x)


def fspl(d_m: float, f_hz: float) -> float:
    return 20 * math.log10(4 * math.pi * d_m * f_hz / C)


def M(v: float, nd: int = 1) -> str:
    """A signed level with a typographic minus."""
    s = f"{v:+.{nd}f}" if v else f"{v:.{nd}f}"
    return s.replace("-", "−")


# ---------------------------------------------------------------- the link ---
# The drone link of the lesson: 630 mW at 2.45 GHz over 3 km, 1.5 dB of cable
# on each side, 4 dBi and 1 dBi antennas, 3 dB of pointing loss at the edge of
# the beam, and a receiver whose datasheet sensitivity is -93 dBm (the 2025
# slides' P_rx,min).
PT = db(630)                      # dBm
LINK = [
    ("Transmitter", None, PT),
    ("Tx cable", -1.5, None),
    ("Tx antenna", +4.0, None),
    ("Path, 3 km", -fspl(3000, 2.45e9), None),
    ("Pointing", -3.0, None),
    ("Rx antenna", +1.0, None),
    ("Rx cable", -1.5, None),
]
SENS = -93.0                      # dBm, datasheet sensitivity


def link_ledger() -> None:
    levels, x = [], 0.0
    for name, d, start in LINK:
        x = start if start is not None else x + d
        levels.append((name, d, x))
    pr = levels[-1][2]
    for name, d, lv in levels:
        print(f"  {name:12s} {'' if d is None else f'{d:+7.2f}'} -> {lv:7.2f} dBm")
    print(f"  sensitivity {SENS:.1f}  margin {pr - SENS:.1f}")

    W, H = 900, 440
    x0, x1, y0, y1 = 96, 740, 40, 380           # plot box; margin bracket to the right
    top, bot = 40.0, -120.0                     # dBm range
    Y = lambda v: y0 + (top - v) / (top - bot) * (y1 - y0)
    n = len(levels)
    step = (x1 - x0) / n
    parts = []
    # grid
    for v in range(-120, 41, 20):
        parts.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        parts.append(f'<text x="{x0 - 10}" y="{Y(v) + 4:.1f}" font-size="13" fill="{GRAY}" text-anchor="end">{M(v, 0) if v else "0"}</text>')
    parts.append(f'<text x="22" y="{(y0 + y1) / 2:.0f}" font-size="13" fill="{GRAY}" text-anchor="middle" transform="rotate(-90 22 {(y0 + y1) / 2:.0f})">level (dBm)</text>')
    # sensitivity
    parts.append(f'<line x1="{x0}" y1="{Y(SENS):.1f}" x2="{x1}" y2="{Y(SENS):.1f}" stroke="{AMBER}" stroke-width="2" stroke-dasharray="3 4"/>')
    parts.append(f'<text x="{x0 + 8}" y="{Y(SENS) - 8:.1f}" font-size="13" fill="{AMBER}">sensitivity {M(SENS)} dBm (datasheet)</text>')
    # staircase
    prev = None
    for i, (name, d, lv) in enumerate(levels):
        xa, xb = x0 + i * step + 8, x0 + (i + 1) * step - 8
        col = NAVY if (d is None or d >= 0) else BLUE
        if d is not None and d < -10:
            col = AMBER
        parts.append(f'<line x1="{xa:.1f}" y1="{Y(lv):.1f}" x2="{xb:.1f}" y2="{Y(lv):.1f}" stroke="{col}" stroke-width="4" stroke-linecap="round"/>')
        if prev is not None:
            parts.append(f'<line x1="{xa - 16:.1f}" y1="{Y(prev):.1f}" x2="{xa:.1f}" y2="{Y(lv):.1f}" stroke="{GRAY}" stroke-width="1.4"/>')
        lab = f"{lv:.1f} dBm" if d is None else f"{M(d)} dB"
        ly = Y(lv) - 10 if (d is None or d >= 0 or lv > 0) else Y(lv) - 10
        parts.append(f'<text x="{(xa + xb) / 2:.1f}" y="{ly:.1f}" font-size="13" font-weight="700" fill="{col}" text-anchor="middle">{lab}</text>')
        parts.append(f'<text x="{(xa + xb) / 2:.1f}" y="{y1 + 22}" font-size="12.5" fill="{INK}" text-anchor="middle">{name}</text>')
        prev = lv
    # result and margin bracket
    xr = x1 - step / 2
    parts.append(f'<line x1="{x1}" y1="{Y(pr):.1f}" x2="{x1 + 22}" y2="{Y(pr):.1f}" stroke="{NAVY}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    parts.append(f'<text x="{x1 + 30}" y="{Y(pr) - 26:.1f}" font-size="13" font-weight="700" fill="{NAVY}">received</text>')
    parts.append(f'<text x="{x1 + 30}" y="{Y(pr) - 10:.1f}" font-size="13" font-weight="700" fill="{NAVY}">{M(pr)} dBm</text>')
    xm = x1 + 22
    parts.append(f'<line x1="{xm}" y1="{Y(pr):.1f}" x2="{xm}" y2="{Y(SENS):.1f}" stroke="{GREEN}" stroke-width="3"/>')
    parts.append(f'<text x="{xm + 8}" y="{(Y(pr) + Y(SENS)) / 2 + 5:.1f}" font-size="13" font-weight="700" fill="{GREEN}">margin {pr - SENS:.1f} dB</text>')
    svg = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="Level diagram of a 2.45 GHz drone link: 28.0 dBm leaves the transmitter, the 3 km path removes '
           f'{-LINK[3][1]:.1f} dB, and {M(pr)} dBm reaches the receiver, {pr - SENS:.1f} dB above the receiver\'s {M(SENS)} dBm datasheet sensitivity">'
           + "".join(parts) + "</svg>")
    write("L02-link-ledger", svg)


# ------------------------------------------------------------- ISM bands ---
ISM = [  # (low MHz, high MHz, label) -- US ISM allocations, 47 CFR 18.301
    (6.765, 6.795, "6.78"), (13.553, 13.567, "13.56"), (26.957, 27.283, "27.12"),
    (40.66, 40.70, "40.68"), (902, 928, "915"), (2400, 2500, "2450"),
    (5725, 5875, "5800"),
]
SDRS = [  # (name, low MHz, high MHz) -- the course PlutoSDRs run in extended-frequency
    # (AD9364) mode; the HackRF and RTL-SDR are optional extras at their stock ranges
    ("PlutoSDR", 70, 6000),
    ("HackRF One", 1, 6000),
    ("RTL-SDR", 24, 1766),
]


def ism_bands() -> None:
    W, H = 880, 262
    x0, x1 = 150, 850
    fmin, fmax = 1.0, 10000.0
    X = lambda f: x0 + (math.log10(f) - math.log10(fmin)) / (math.log10(fmax) - math.log10(fmin)) * (x1 - x0)
    parts = []
    ya = 230
    parts.append(f'<line x1="{x0}" y1="{ya}" x2="{x1}" y2="{ya}" stroke="{GRAY}" stroke-width="1.4"/>')
    for f, lab in [(1, "1 MHz"), (10, "10 MHz"), (100, "100 MHz"), (1000, "1 GHz"), (10000, "10 GHz")]:
        parts.append(f'<line x1="{X(f):.1f}" y1="{ya}" x2="{X(f):.1f}" y2="{ya + 6}" stroke="{GRAY}" stroke-width="1.4"/>')
        parts.append(f'<text x="{X(f):.1f}" y="{ya + 22}" font-size="13" fill="{GRAY}" text-anchor="middle">{lab}</text>')
    parts.append(f'<text x="{x0 - 12}" y="44" font-size="13" font-weight="700" fill="{AMBER}" text-anchor="end">ISM bands (MHz)</text>')
    for lo, hi, lab in ISM:
        xa, xb = X(lo), X(hi)
        if xb - xa < 4:
            xa, xb = (xa + xb) / 2 - 2, (xa + xb) / 2 + 2
        parts.append(f'<rect x="{xa:.1f}" y="30" width="{xb - xa:.1f}" height="{ya - 30}" fill="{AMBER}" opacity="0.14"/>')
        parts.append(f'<rect x="{xa:.1f}" y="30" width="{xb - xa:.1f}" height="18" fill="{AMBER}"/>')
        ly = 8 if lab == "40.68" else 22
        parts.append(f'<text x="{(xa + xb) / 2:.1f}" y="{ly + 6}" font-size="12" font-weight="700" fill="{AMBER}" text-anchor="middle">{lab}</text>')
    for i, (name, lo, hi) in enumerate(SDRS):
        y = 90 + i * 44
        parts.append(f'<rect x="{X(lo):.1f}" y="{y}" width="{X(hi) - X(lo):.1f}" height="22" rx="4" fill="{NAVY}" opacity="0.85"/>')
        parts.append(f'<text x="{x0 - 12}" y="{y + 16}" font-size="13.5" font-weight="700" fill="{NAVY}" text-anchor="end">{name}</text>')
        rng = f"{lo:g} MHz to {hi / 1000:g} GHz" if hi >= 1000 else f"{lo:g} to {hi:g} MHz"
        parts.append(f'<text x="{X(hi) + 8:.1f}" y="{y + 16}" font-size="12" fill="{GRAY}">{rng}</text>' if X(hi) + 150 < W
                     else f'<text x="{X(lo) + 8:.1f}" y="{y + 16}" font-size="12" fill="#fff">{rng}</text>')
    svg = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="The US ISM bands at 6.78, 13.56, 27.12, and 40.68 MHz and at 915, 2450, and 5800 MHz on a log frequency axis, '
           f'with the tuning ranges of the course PlutoSDR, 70 MHz to 6 GHz in extended-frequency mode, and of two optional radios, the HackRF One, 1 MHz to 6 GHz, and the RTL-SDR, 24 MHz to 1.766 GHz">'
           + "".join(parts) + "</svg>")
    write("L02-ism-bands", svg)


# ---------------------------------------------------------- noise cascade ---
STAGES = {"LNA": (1.0, 20.0), "Cable": (3.0, -3.0), "SDR": (8.0, 0.0)}   # (NF dB, gain dB)


def cascade(order: list[str]) -> float:
    F, G = 0.0, 1.0
    for i, s in enumerate(order):
        nf, g = STAGES[s]
        f = 10 ** (nf / 10)
        F = f if i == 0 else F + (f - 1) / G
        G *= 10 ** (g / 10)
    return db(F)


def noise_cascade() -> None:
    rows = [(["LNA", "Cable", "SDR"], "LNA at the antenna"),
            (["Cable", "LNA", "SDR"], "LNA at the radio"),
            (["Cable", "SDR"], "no LNA")]
    W, H = 880, 290
    parts = []
    bw, bh, gap = 128, 52, 40
    for r, (order, title) in enumerate(rows):
        y = 26 + r * 100
        nf = cascade(order)
        print(f"  {title:20s} {' -> '.join(order):20s} NF = {nf:.2f} dB")
        parts.append(f'<text x="20" y="{y + bh / 2 + 5}" font-size="14" font-weight="700" fill="{INK}">{title}</text>')
        x = 230
        parts.append(f'<path d="M {x - 50} {y + 4} l 13 16 l 13 -16 M {x - 37} {y + 20} V {y + bh / 2}" fill="none" stroke="{NAVY}" stroke-width="2"/>')
        parts.append(f'<line x1="{x - 37}" y1="{y + bh / 2}" x2="{x}" y2="{y + bh / 2}" stroke="{GRAY}" stroke-width="1.6"/>')
        for s in order:
            nfs, g = STAGES[s]
            col = GREEN if s == "LNA" else (AMBER if s == "Cable" else NAVY)
            parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{PALE}" stroke="{col}" stroke-width="2"/>')
            parts.append(f'<text x="{x + bw / 2}" y="{y + 21}" font-size="14" font-weight="700" fill="{col}" text-anchor="middle">{s}</text>')
            gtxt = f"G {M(g, 0)} dB" if g else "G 0 dB"
            parts.append(f'<text x="{x + bw / 2}" y="{y + 40}" font-size="12" fill="{GRAY}" text-anchor="middle">NF {nfs:g} dB, {gtxt}</text>')
            x += bw
            parts.append(f'<line x1="{x}" y1="{y + bh / 2}" x2="{x + gap}" y2="{y + bh / 2}" stroke="{GRAY}" stroke-width="1.6"/>')
            x += gap
        parts.append(f'<text x="{x + 4}" y="{y + bh / 2 + 6}" font-size="17" font-weight="700" fill="{RED if nf > 5 else (GREEN if nf < 2 else AMBER)}">NF {nf:.1f} dB</text>')
    svg = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="The same LNA, 3 dB cable, and SDR in three arrangements. With the LNA at the antenna the system noise figure is '
           f'{cascade(["LNA", "Cable", "SDR"]):.1f} dB; with the cable ahead of the LNA it is {cascade(["Cable", "LNA", "SDR"]):.1f} dB; '
           f'with no LNA it is {cascade(["Cable", "SDR"]):.1f} dB">' + "".join(parts) + "</svg>")
    write("L02-noise-cascade", svg)


# --------------------------------------------------------- antenna patterns ---
def _polar(ax, th, g_db, title, col, floor=-30):
    """Plot a pattern in dB, normalized to its peak, on a polar axis."""
    import numpy as np
    r = np.clip(g_db - g_db.max(), floor, 0) - floor
    ax.plot(th, r, color=col, lw=2)
    ax.set_ylim(0, -floor)
    ax.set_yticks([-floor - 3, -floor - 10, -floor - 20])
    ax.set_yticklabels(["−3", "−10", "−20"], fontsize=8, color=GRAY)
    ax.set_xticks(np.radians(range(0, 360, 45)))
    ax.set_xticklabels([f"{a}°" for a in range(0, 360, 45)], fontsize=8, color=GRAY)
    ax.set_rlabel_position(112)
    ax.grid(color=RULE, lw=0.8)
    ax.spines["polar"].set_color(RULE)
    ax.set_title(title, color=NAVY, fontsize=11.5, fontweight="bold", pad=12)


def antenna_patterns() -> None:
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif"})
    th = np.linspace(0, 2 * np.pi, 721)
    # Half-wave dipole, vertical: elevation cut, angle from the horizon.
    el = th
    c = np.cos(el)
    with np.errstate(divide="ignore", invalid="ignore"):
        e = np.where(np.abs(c) < 1e-6, 0.0, np.cos(np.pi / 2 * np.sin(el)) / c)
    e = np.abs(e)
    dip = 20 * np.log10(np.maximum(e, 1e-4))
    # A directional antenna with a 20 degree half-power beamwidth: a Gaussian
    # main beam with a -25 dB back and side level.
    hpbw = 20.0
    off = np.degrees(np.angle(np.exp(1j * th)))
    beam = 10 * np.log10(np.maximum(np.exp(-4 * np.log(2) * (off / hpbw) ** 2), 10 ** -2.5))
    fig, axs = plt.subplots(1, 3, figsize=(11.0, 3.8), subplot_kw={"projection": "polar"})
    fig.subplots_adjust(wspace=0.45)
    _polar(axs[0], th, dip, "omni: vertical cut", NAVY)
    _polar(axs[1], th, np.zeros_like(th), "omni: horizontal cut", NAVY)
    _polar(axs[2], th, beam, f"directional: {hpbw:.0f}° beamwidth", NAVY)
    for a in (-hpbw / 2, hpbw / 2):
        axs[2].plot([np.radians(a)] * 2, [0, 30], color=AMBER, lw=1.4, ls=(0, (4, 3)))
    axs[2].text(np.radians(28), 31, "−3 dB", color=AMBER, fontsize=10, fontweight="bold")
    print(f"  directional HPBW {hpbw:.0f} deg; dipole HPBW 78 deg (vertical cut)")
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    t = buf.getvalue()
    write("L02-antenna-patterns", t[t.index("<svg"):])


# ------------------------------------------------------------- atmosphere ---
def atmosphere() -> None:
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import itur
    plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif",
                         "axes.spines.top": False, "axes.spines.right": False})
    f = np.logspace(0, np.log10(350), 700)
    # Sea level: 1013.25 hPa, 15 C, 7.5 g/m^3 of water vapor (ITU-R P.835 mean).
    o2 = np.asarray(itur.models.itu676.gamma0_exact(f, 1013.25, 7.5, 288.15).value)
    h2o = np.asarray(itur.models.itu676.gammaw_exact(f, 1013.25, 7.5, 288.15).value)
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.loglog(f, o2, color=GREEN, lw=2.2, label="oxygen")
    ax.loglog(f, h2o, color=RED, lw=2.2, ls=(0, (5, 2)), label="water vapor")
    ax.axvspan(1, 6, color=PALE, zorder=0)
    ax.text(2.45, 2e-3, "course SDRs", color=NAVY, fontsize=10.5, ha="center")
    i60 = np.argmax(o2 * (f < 70))
    ax.text(f[i60], 35, f"{o2[i60]:.0f} dB/km at {f[i60]:.0f} GHz", ha="center",
            color=GREEN, fontsize=10.5, fontweight="bold")
    ax.set_xlim(1, 350)
    ax.set_ylim(1e-3, 100)
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("attenuation (dB/km)")
    ax.grid(True, which="major", color=RULE, lw=0.8)
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.32, 1.0))
    for fx in (2.45, 10, 22.2, 60, 183):
        k = np.argmin(abs(f - fx))
        print(f"  {fx:6.2f} GHz: O2 {o2[k]:.4f}  H2O {h2o[k]:.4f} dB/km")
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    t = buf.getvalue()
    write("L02-atmosphere", t[t.index("<svg"):])


if __name__ == "__main__":
    link_ledger()
    ism_bands()
    noise_cascade()
    antenna_patterns()
    atmosphere()
