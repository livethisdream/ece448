#!/usr/bin/env python3
"""L3 figures (signal space).

  L03-constellations : BPSK, 4-PAM, QPSK, 8-PSK, and 16-QAM at the same
                       average symbol energy
  L03-noise-clouds   : QPSK received through AWGN at three values of Es/N0,
                       with the decision boundaries and the errors marked
  L03-ber-curves     : bit error rate against Eb/N0 for the same five
                       modulations, with the 1e-5 line
  L03-gray-8psk      : 8-PSK with Gray-coded labels
  L03-impairments    : what four receiver problems do to a QPSK constellation

Every plotted number is computed here and printed for checking against the
lesson text. Words and numbers only, no equations, so one SVG serves both the
deck and the page.

    python3 scripts/graphics/l03_figures.py
    -> book/extras/slides/fig/L03-*.svg  and  book/extras/viz/img/L03-*.svg
"""

from __future__ import annotations

import io
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")

NAVY, BLUE, AMBER, RED, GREEN = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#3f7d34"
GRAY, INK, RULE = "#5b6573", "#15202b", "#cddce9"

plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
    "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
    "axes.spines.top": False, "axes.spines.right": False,
})
RNG = np.random.default_rng(448)


def write(name: str, fig) -> None:
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = buf.getvalue()
    s = apply_font_stack(s[s.index("<svg"):])
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


# ------------------------------------------------------------- the shapes ---
def constellation(name: str) -> np.ndarray:
    """Unit average symbol energy."""
    if name == "BPSK":
        c = np.array([-1, 1], complex)
    elif name == "4-PAM":
        c = np.array([-3, -1, 1, 3], complex)
    elif name == "QPSK":
        c = np.exp(1j * (np.pi / 4 + np.pi / 2 * np.arange(4)))
    elif name == "8-PSK":
        c = np.exp(1j * np.pi / 4 * np.arange(8))
    elif name == "16-QAM":
        a = np.array([-3, -1, 1, 3])
        c = (a[:, None] + 1j * a[None, :]).ravel()
    else:
        raise ValueError(name)
    return c / np.sqrt(np.mean(np.abs(c) ** 2))


MODS = ["BPSK", "4-PAM", "QPSK", "8-PSK", "16-QAM"]
BITS = {"BPSK": 1, "4-PAM": 2, "QPSK": 2, "8-PSK": 3, "16-QAM": 4}


def iq_axes(ax, lim=1.6, label=True):
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axhline(0, color=RULE, lw=1, zorder=0)
    ax.axvline(0, color=RULE, lw=1, zorder=0)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if label:
        ax.text(lim, -0.12, "I", color=GRAY, ha="right", va="top", fontsize=10)
        ax.text(0.06, lim, "Q", color=GRAY, ha="left", va="top", fontsize=10)


def constellations() -> None:
    fig, axs = plt.subplots(1, 5, figsize=(11.5, 2.9))
    for ax, m in zip(axs, MODS):
        c = constellation(m)
        iq_axes(ax)
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(th), np.sin(th), color=RULE, lw=1, ls=(0, (3, 3)), zorder=0)
        ax.scatter(c.real, c.imag, s=42, color=NAVY, zorder=3)
        d = min(abs(a - b) for i, a in enumerate(c) for b in c[i + 1:])
        ax.set_title(m, color=NAVY, fontsize=13, fontweight="bold", pad=4)
        ax.text(0, -1.95, f"{BITS[m]} bit{'s' if BITS[m] > 1 else ''}/symbol", ha="center", color=INK, fontsize=11)
        ax.text(0, -2.3, f"closest spacing {d:.2f}", ha="center", color=GRAY, fontsize=10)
        print(f"  {m:7s} bits {BITS[m]}  min distance {d:.3f} (unit average energy)")
    write("L03-constellations", fig)


# ------------------------------------------------------------ noise clouds ---
def awgn(n: int, esn0_db: float) -> np.ndarray:
    """Complex noise for unit-energy symbols: N0 = 1/(Es/N0), N0/2 per axis."""
    n0 = 10 ** (-esn0_db / 10)
    return np.sqrt(n0 / 2) * (RNG.standard_normal(n) + 1j * RNG.standard_normal(n))


def noise_clouds() -> None:
    c = constellation("QPSK")
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.6))
    for ax, esn0 in zip(axs, (20.0, 10.0, 4.0)):
        n = 600
        tx = RNG.integers(0, 4, n)
        r = c[tx] + awgn(n, esn0)
        dec = np.argmin(np.abs(r[:, None] - c[None, :]), axis=1)
        err = dec != tx
        iq_axes(ax, lim=2.0)
        ax.axhline(0, color=AMBER, lw=1.6, zorder=1)
        ax.axvline(0, color=AMBER, lw=1.6, zorder=1)
        ax.scatter(r[~err].real, r[~err].imag, s=5, color=BLUE, alpha=0.55, lw=0, zorder=2)
        ax.scatter(r[err].real, r[err].imag, s=11, color=RED, lw=0, zorder=4)
        ax.scatter(c.real, c.imag, s=50, color=NAVY, edgecolor="white", lw=1.2, zorder=5)
        ax.set_title(f"Es/N0 = {esn0:.0f} dB", color=NAVY, fontsize=13, fontweight="bold", pad=4)
        ax.text(0, -2.35, f"{err.sum()} of {n} symbols in the wrong region", ha="center", color=RED if err.sum() else GREEN, fontsize=11)
        print(f"  QPSK Es/N0 {esn0:4.1f} dB: {err.sum()} errors in {n}")
    write("L03-noise-clouds", fig)


# --------------------------------------------------------------- BER curves ---
def Q(x):
    from math import erfc
    return 0.5 * np.vectorize(erfc)(np.asarray(x) / np.sqrt(2))


def ber(mod: str, ebn0_db):
    g = 10 ** (np.asarray(ebn0_db) / 10)
    k = BITS[mod]
    es = g * k
    if mod in ("BPSK", "QPSK"):
        return Q(np.sqrt(2 * g))
    if mod == "8-PSK":
        return 2 * Q(np.sqrt(2 * es) * np.sin(np.pi / 8)) / k
    if mod == "16-QAM":
        p = 2 * (1 - 1 / 4) * Q(np.sqrt(3 * es / 15))
        return (1 - (1 - p) ** 2) / k
    if mod == "4-PAM":
        return 2 * 3 / 4 * Q(np.sqrt(6 * es / 15)) / k
    raise ValueError(mod)


def ebn0_for(mod: str, target: float) -> float:
    lo, hi = -5.0, 40.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if ber(mod, mid) > target:
            lo = mid
        else:
            hi = mid
    return mid


def ber_curves() -> None:
    x = np.linspace(0, 20, 400)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    # Gray-coded 16-QAM is two 4-PAM signals on I and Q, so their bit error
    # rates are the same curve; one line carries both labels.
    styles = {"BPSK": (NAVY, "-"), "8-PSK": (AMBER, "-"), "16-QAM": (RED, "-")}
    names = {"BPSK": "BPSK and QPSK", "8-PSK": "8-PSK", "16-QAM": "16-QAM and 4-PAM"}
    for m, (col, ls) in styles.items():
        lab = names[m]
        ax.semilogy(x, ber(m, x), color=col, ls=ls, lw=2.2, label=lab)
    ax.axhline(1e-5, color=GREEN, lw=1.2, ls=(0, (4, 3)))
    ax.text(0.3, 1.5e-5, "bit error rate 1 in 100,000", color=GREEN, fontsize=10.5)
    for m in ("BPSK", "8-PSK", "16-QAM"):
        e = ebn0_for(m, 1e-5)
        col = styles[m][0]
        ax.plot([e], [1e-5], "o", color=col, ms=6)
        off = {"BPSK": (-46, -16), "8-PSK": (-48, 6), "16-QAM": (8, -16)}[m]
        ax.annotate(f"{e:.1f} dB", (e, 1e-5), xytext=off, textcoords="offset points", color=col, fontsize=10.5, fontweight="bold")
    for m in MODS:
        k = BITS[m]
        e = ebn0_for(m, 1e-5)
        print(f"  {m:7s} BER 1e-5 at Eb/N0 {e:5.2f} dB, Es/N0 {e + 10 * math.log10(k):5.2f} dB")
    ax.set_ylim(1e-7, 0.5)
    ax.set_xlim(0, 20)
    ax.set_xlabel("Eb/N0 (dB)")
    ax.set_ylabel("bit error rate")
    ax.grid(True, which="major", color=RULE, lw=0.8)
    ax.legend(frameon=False, loc="upper right")
    write("L03-ber-curves", fig)


# --------------------------------------------------------------- Gray 8-PSK ---
def gray_8psk() -> None:
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    iq_axes(ax, lim=1.55)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color=RULE, lw=1, ls=(0, (3, 3)), zorder=0)
    gray = [i ^ (i >> 1) for i in range(8)]
    for i in range(8):
        a = np.pi / 4 * i
        ax.scatter([np.cos(a)], [np.sin(a)], s=60, color=NAVY, zorder=3)
        ax.text(1.27 * np.cos(a), 1.27 * np.sin(a), f"{gray[i]:03b}", ha="center", va="center",
                color=NAVY, fontsize=13, fontweight="bold", family="monospace")
    print("  8-PSK Gray labels around the circle:", [f"{g:03b}" for g in gray])
    write("L03-gray-8psk", fig)


# ------------------------------------------------------------- impairments ---
def rc_pulse(t, beta=0.35):
    t = np.asarray(t, float)
    out = np.sinc(t) * np.cos(np.pi * beta * t)
    den = 1 - (2 * beta * t) ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.where(np.abs(den) < 1e-9, np.pi / 4 * np.sinc(1 / (2 * beta)), out / den)
    return out


def impairments() -> None:
    c = constellation("QPSK")
    n = 500
    tx = c[RNG.integers(0, 4, n)]
    panels = []
    panels.append(("noise", tx + awgn(n, 14)))
    panels.append(("phase offset, 25°", tx * np.exp(1j * np.radians(25)) + awgn(n, 24)))
    panels.append(("frequency offset", tx * np.exp(1j * 2 * np.pi * 0.004 * np.arange(n)) + awgn(n, 24)))
    # Timing: raised-cosine pulses sampled 0.3 symbol away from their peaks.
    k = np.arange(-8, 9)
    taps = rc_pulse(k + 0.3)
    timing = np.convolve(tx, taps, mode="same")
    panels.append(("timing offset, 0.3 symbol", timing + awgn(n, 24)))
    fig, axs = plt.subplots(1, 4, figsize=(11.5, 3.3))
    for ax, (title, r) in zip(axs, panels):
        iq_axes(ax, lim=1.9, label=False)
        ax.scatter(r.real, r.imag, s=5, color=BLUE, alpha=0.6, lw=0)
        ax.scatter(c.real, c.imag, s=36, facecolor="none", edgecolor=NAVY, lw=1.4, zorder=4)
        ax.set_title(title, color=NAVY, fontsize=12, fontweight="bold", pad=4)
    write("L03-impairments", fig)


if __name__ == "__main__":
    constellations()
    noise_clouds()
    ber_curves()
    gray_8psk()
    impairments()
