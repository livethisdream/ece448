#!/usr/bin/env python3
"""L9 figures (PAM theory).

  L09-pam-levels   : eight bits sent as 2-PAM and as Gray-coded 4-PAM, with
                     rectangular pulses, so the symbol rate halves for 4-PAM.
  L09-rc-pulses    : three raised-cosine pulses one symbol apart and their sum;
                     each pulse is zero at every other symbol instant.
  L09-rc-spectrum  : the raised-cosine spectrum for alpha = 0, 0.35, and 1, in
                     units of the symbol rate.
  L09-eye-anatomy  : a noiseless raised-cosine 2-PAM eye with the sampling
                     instant and the eye opening marked. About 70 traces keep the SVG
                     small enough to inline in the deck.
  L09-pam-noise    : received samples, one per symbol, for 2-PAM with a little
                     and with more noise, and for 4-PAM at the same power with a
                     little noise; the decision thresholds are dashed and every
                     wrong decision is red. No error-rate numbers: noise is
                     something to watch (ROADMAP, "Sources and noise").
  L09-constellations : 2-PAM, Gray-coded 4-PAM, Gray-coded QPSK, and unlabeled
                     8-PSK on the I/Q plane, as on the 2025 deck's constellation
                     slides; the 8-PSK Gray code is left for the class to fill in.

The GNU Radio screenshots (L09-grc-*.png, L09-pulse-shaping.png,
L09-matched-filter.png, L09-timing.png) are not generated here: they are taken
from the real flowgraphs in book/extras/grc/ running under Xvfb (see
CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l09_figures.py
"""

from __future__ import annotations

import io
import re
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
RNG = np.random.default_rng(9)


def write(name, fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = apply_font_stack(buf.getvalue()[buf.getvalue().index("<svg"):])
    # Path data to 0.1 pt, finer than any screen, keeps the deck DOM small; text is untouched.
    s = re.sub(r' d="([^"]*)"', lambda m: ' d="' + re.sub(r"(\d+\.\d)\d+", r"\1", m.group(1)) + '"', s)
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


def rc(t, a):
    """Raised-cosine pulse, t in symbol periods."""
    t = np.asarray(t, float)
    out = np.sinc(t) * np.cos(np.pi * a * t)
    den = 1 - (2 * a * t) ** 2
    sing = np.abs(den) < 1e-8
    out[~sing] /= den[~sing]
    out[sing] = np.pi / 4 * np.sinc(1 / (2 * a))
    return out


def pam_levels():
    bits = [1, 0, 1, 1, 0, 0, 1, 0]
    gray = {(0, 0): -3, (0, 1): -1, (1, 1): 1, (1, 0): 3}
    s2 = [1 if b else -1 for b in bits]
    s4 = [gray[(bits[i], bits[i + 1])] for i in range(0, 8, 2)]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 4.2), sharex=True)
    for ax, s, T, lab in ((a1, s2, 1, "2-PAM: 1 bit per symbol"), (a2, s4, 2, "4-PAM: 2 bits per symbol")):
        x = np.repeat(np.arange(len(s) + 1) * T, 2)[1:-1]
        y = np.repeat(s, 2)
        ax.plot(x, y, color=NAVY, lw=2)
        ax.axhline(0, color=RULE, lw=1)
        for k in range(len(s) + 1):
            ax.axvline(k * T, color=RULE, lw=0.8, ls=":")
        ax.set_title(lab, loc="left", fontsize=11, color=INK)
        ax.set_yticks(sorted(set(s)) if T == 1 else [-3, -1, 1, 3])
        ax.set_ylim(-3.9 if T == 2 else -1.8, 3.9 if T == 2 else 1.8)
    for k, b in enumerate(bits):
        a1.text(k + 0.5, 1.25, str(b), ha="center", color=AMBER, fontsize=11, fontweight="bold")
    for k in range(4):
        a2.text(2 * k + 1, 3.25 if s4[k] < 2 else -3.6, f"{bits[2*k]}{bits[2*k+1]}", ha="center",
                color=AMBER, fontsize=11, fontweight="bold")
    a2.set_xlabel("time (bit periods)")
    a2.set_xticks(range(9))
    fig.tight_layout()
    write("L09-pam-levels", fig)


def rc_pulses():
    t = np.linspace(-4, 6, 2001)
    a = 0.35
    syms = [1, -1, 1]
    fig, ax = plt.subplots(figsize=(8, 3.4))
    total = np.zeros_like(t)
    for k, s in enumerate(syms):
        p = s * rc(t - k, a)
        total += p
        ax.plot(t, p, color=[NAVY, AMBER, GRAY][k], lw=1.4, ls="--")
    ax.plot(t, total, color=RED, lw=2.2, label="sum")
    for k, s in enumerate(syms):
        ax.plot(k, s, "o", color=RED, ms=7, zorder=5)
    ax.axhline(0, color=RULE, lw=1)
    for k in range(-4, 7):
        ax.axvline(k, color=RULE, lw=0.8, ls=":")
    ax.set_xlabel("time (symbol periods)")
    ax.set_xlim(-4, 6)
    ax.set_ylim(-1.5, 1.5)
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    write("L09-rc-pulses", fig)


def rc_spectrum():
    f = np.linspace(-1.2, 1.2, 2001)

    def H(f, a):
        af = np.abs(f)
        h = np.zeros_like(f)
        h[af <= (1 - a) / 2] = 1
        band = (af > (1 - a) / 2) & (af <= (1 + a) / 2)
        if a > 0:
            h[band] = 0.5 * (1 + np.cos(np.pi / a * (af[band] - (1 - a) / 2)))
        return h

    fig, ax = plt.subplots(figsize=(8, 3.2))
    for a, col in ((0.0, GRAY), (0.35, NAVY), (1.0, AMBER)):
        ax.plot(f, H(f, a), color=col, lw=2, label=f"α = {a:g}")
    ax.axvline(0.675, color=NAVY, lw=1, ls=":")
    ax.axvline(-0.675, color=NAVY, lw=1, ls=":")
    ax.set_xlabel("frequency (multiples of the symbol rate $R_s$)")
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(0, 1.15)
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    write("L09-rc-spectrum", fig)


def eye_anatomy():
    sps, a, n = 16, 0.35, 94
    sym = RNG.choice([-1, 1], n)
    tp = np.arange(-8 * sps, 8 * sps + 1) / sps
    h = rc(tp, a)
    up = np.zeros(n * sps)
    up[::sps] = sym
    y = np.convolve(up, h)
    d = 8 * sps
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for k in range(12, n - 12):
        c = d + k * sps
        ax.plot(np.arange(-sps, sps + 1) / sps, y[c - sps:c + sps + 1], color=NAVY, lw=0.8, alpha=0.35)
    lo = min(y[d + k * sps] for k in range(12, n - 12) if sym[k] > 0)
    ax.axvline(0, color=AMBER, lw=1.6, ls="--")
    ax.text(0.03, 1.55, "sample here", color=AMBER, fontsize=11, fontweight="bold")
    ax.annotate("", xy=(0, -lo), xytext=(0, lo), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
    ax.text(0.05, 0.0, "eye opening", color=RED, fontsize=11, va="center", fontweight="bold")
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xticklabels(["−T", "−T/2", "0", "T/2", "T"])
    ax.set_xlabel("time from the symbol instant")
    ax.set_ylim(-1.8, 1.8)
    ax.set_xlim(-1, 1)
    fig.tight_layout()
    write("L09-eye-anatomy", fig)


def pam_noise():
    rng = np.random.default_rng(448)
    n = 160
    l4 = np.array([-3, -1, 1, 3]) / np.sqrt(5)          # 4-PAM at the same average power as 2-PAM
    cases = (("2-PAM, a little noise", np.array([-1.0, 1.0]), 0.25),
             ("2-PAM, more noise", np.array([-1.0, 1.0]), 0.6),
             ("4-PAM, the same little noise", l4, 0.25))
    fig, axes = plt.subplots(3, 1, figsize=(8, 5.6), sharex=True)
    for ax, (title, lev, sig) in zip(axes, cases):
        tx = rng.choice(lev, n)
        rx = tx + rng.normal(0, sig, n)
        dec = lev[np.argmin(np.abs(rx[:, None] - lev[None, :]), axis=1)]
        bad = dec != tx
        ax.plot(np.arange(n)[~bad], rx[~bad], "o", color=NAVY, ms=3.2)
        ax.plot(np.arange(n)[bad], rx[bad], "o", color=RED, ms=5.5)
        for t in (lev[1:] + lev[:-1]) / 2:
            ax.axhline(t, color=AMBER, lw=1.3, ls="--")
        ax.set_yticks(np.round(lev, 2))
        ax.set_ylim(-2.4, 2.4)
        ax.set_title(f"{title}: {bad.sum()} wrong of {n}", loc="left", fontsize=11, color=INK)
    axes[-1].set_xlabel("symbol number")
    fig.tight_layout()
    write("L09-pam-noise", fig)


def constellations():
    fig, axes = plt.subplots(1, 4, figsize=(10, 2.9))
    l4 = np.array([-3, -1, 1, 3]) / np.sqrt(5)
    sets = (("2-PAM", [(-1, 0, "0"), (1, 0, "1")]),
            ("4-PAM, Gray coded", [(x, 0, b) for x, b in zip(l4, ["00", "01", "11", "10"])]),
            ("QPSK, Gray coded", [(np.cos(a), np.sin(a), b) for a, b in
                                  zip(np.pi / 4 * np.array([1, 3, 5, 7]), ["00", "01", "11", "10"])]),
            ("8-PSK: label it", [(np.cos(a), np.sin(a), "") for a in np.pi / 4 * np.arange(8)]))
    for ax, (title, pts) in zip(axes, sets):
        ax.axhline(0, color=RULE, lw=1)
        ax.axvline(0, color=RULE, lw=1)
        for x, y, b in pts:
            ax.plot(x, y, "o", color=NAVY, ms=9)
            ax.text(x, y + 0.22, b, ha="center", color=AMBER, fontsize=11, fontweight="bold")
        ax.set_title(title, fontsize=11, color=INK)
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("I (real)")
        ax.set_ylabel("Q (imag)")
    fig.tight_layout()
    write("L09-constellations", fig)


if __name__ == "__main__":
    pam_levels()
    rc_pulses()
    rc_spectrum()
    eye_anatomy()
    pam_noise()
    constellations()
