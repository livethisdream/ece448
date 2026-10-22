#!/usr/bin/env python3
"""L3 figures (signal space).

  L03-binary-pam     : a binary PAM waveform, its samples, and the threshold
  L03-pam-noise      : received binary PAM samples at two SNRs, with the
                       samples that land on the wrong side of zero marked
  L03-antipodal-orthogonal : antipodal and orthogonal binary signals at the
                       same energy and the same noise
  L03-constellations : BPSK (2-PAM), 4-PAM, QPSK, and 8-PSK at the same
                       average symbol energy
  L03-noise-clouds   : QPSK received through noise at three SNRs, with the
                       decision boundaries and the wrong decisions marked
  L03-gray-8psk      : 8-PSK with Gray-coded labels
  L03-impairments    : what four receiver problems do to a QPSK constellation

SNR is signal power over noise power, as an SDR display reads it. Every
plotted number is computed here and printed for checking against the lesson
text. Words and numbers only, no equations, so one SVG serves both the
deck and the page.

    python3 scripts/graphics/l03_figures.py
    -> book/extras/slides/fig/L03-*.svg  and  book/extras/viz/img/L03-*.svg
"""

from __future__ import annotations

import io
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
    else:
        raise ValueError(name)
    return c / np.sqrt(np.mean(np.abs(c) ** 2))


MODS = ["BPSK", "4-PAM", "QPSK", "8-PSK"]
BITS = {"BPSK": 1, "4-PAM": 2, "QPSK": 2, "8-PSK": 3}


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
    fig, axs = plt.subplots(1, 4, figsize=(9.4, 2.9))
    for ax, m in zip(axs, MODS):
        c = constellation(m)
        iq_axes(ax)
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(th), np.sin(th), color=RULE, lw=1, ls=(0, (3, 3)), zorder=0)
        ax.scatter(c.real, c.imag, s=42, color=NAVY, zorder=3)
        ax.set_title("BPSK (2-PAM)" if m == "BPSK" else m, color=NAVY, fontsize=13, fontweight="bold", pad=4)
        ax.text(0, -1.95, f"{BITS[m]} bit{'s' if BITS[m] > 1 else ''}/symbol", ha="center", color=INK, fontsize=11)
        print(f"  {m:7s} bits {BITS[m]}")
    write("L03-constellations", fig)


# ------------------------------------------------------------ noise clouds ---
def awgn(n: int, snr_db: float) -> np.ndarray:
    """Complex noise for unit-power symbols: total noise power 1/SNR, half per axis."""
    p = 10 ** (-snr_db / 10)
    return np.sqrt(p / 2) * (RNG.standard_normal(n) + 1j * RNG.standard_normal(n))


# -------------------------------------------------------------- binary PAM ---
def binary_pam() -> None:
    bits = np.array([1, 0, 1, 1, 0, 0, 1, 0])
    a = 2 * bits - 1
    sps = 40
    t = np.arange(len(bits) * sps) / sps
    s = np.repeat(a, sps).astype(float)
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.0, 2.9), gridspec_kw={"width_ratios": [3.2, 1]})
    ax.plot(t, s, color=NAVY, lw=2)
    mid = np.arange(len(bits)) + 0.5
    ax.scatter(mid, a, s=40, color=AMBER, zorder=4)
    for m, b in zip(mid, bits):
        ax.text(m, 1.35, str(b), ha="center", color=INK, fontsize=12, fontweight="bold")
    ax.axhline(0, color=RULE, lw=1, zorder=0)
    ax.set_xlim(0, len(bits))
    ax.set_ylim(-1.6, 1.75)
    ax.set_yticks([-1, 0, 1], ["−A", "0", "+A"])
    ax.set_xticks(range(len(bits) + 1))
    ax.set_xlabel("time (symbols)")
    ax.set_title("binary PAM: one pulse per bit", color=NAVY, fontsize=12, fontweight="bold", loc="left")
    ax2.axvline(0, color=AMBER, lw=1.6)
    ax2.axhline(0, color=RULE, lw=1)
    ax2.scatter([-1, 1], [0, 0], s=60, color=NAVY, zorder=3)
    ax2.text(-1, 0.25, "0", ha="center", color=NAVY, fontsize=12, fontweight="bold")
    ax2.text(1, 0.25, "1", ha="center", color=NAVY, fontsize=12, fontweight="bold")
    ax2.text(0.06, -0.45, "threshold", color=AMBER, fontsize=10)
    ax2.set_xlim(-1.6, 1.6)
    ax2.set_ylim(-0.8, 0.8)
    ax2.set_xticks([-1, 0, 1], ["−A", "0", "+A"])
    ax2.set_yticks([])
    ax2.spines["left"].set_visible(False)
    ax2.set_title("the samples", color=NAVY, fontsize=12, fontweight="bold")
    write("L03-binary-pam", fig)


def pam_noise() -> None:
    # Each received sample is a dot at its value, spread up and down at random
    # so the dots do not pile on one another; the height means nothing.
    n = 1500
    fig, axs = plt.subplots(1, 2, figsize=(10.0, 2.9), sharey=True)
    for ax, snr in zip(axs, (14.0, 4.0)):
        tx = 2 * RNG.integers(0, 2, n) - 1
        r = (tx + awgn(n, snr)).real
        wrong = np.sign(r) != tx
        y = RNG.uniform(-1, 1, n)
        ax.scatter(r[~wrong], y[~wrong], s=5, color=BLUE, alpha=0.5, lw=0, zorder=2)
        ax.scatter(r[wrong], y[wrong], s=12, color=RED, lw=0, zorder=4)
        ax.scatter([-1, 1], [0, 0], s=60, color=NAVY, edgecolor="white", lw=1.2, zorder=5)
        ax.axvline(0, color=AMBER, lw=1.6, zorder=3)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_xticks([-1, 0, 1], ["−A", "0", "+A"])
        ax.set_xlabel("received sample")
        ax.set_title(f"SNR = {snr:.0f} dB", color=NAVY, fontsize=13, fontweight="bold", pad=4)
        ax.text(0.5, -0.42, f"{wrong.sum()} of {n} samples on the wrong side", transform=ax.transAxes,
                ha="center", color=RED if wrong.sum() else GREEN, fontsize=11)
        print(f"  binary PAM SNR {snr:4.1f} dB: {wrong.sum()} wrong in {n}")
    write("L03-pam-noise", fig)


def antipodal_orthogonal() -> None:
    n, snr = 600, 6.0
    sets = (("antipodal (2-PAM)", np.array([-1, 1], complex)),
            ("orthogonal (2-FSK)", np.array([1, 1j], complex)))
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.8))
    for ax, (title, c) in zip(axs, sets):
        tx = RNG.integers(0, 2, n)
        r = c[tx] + awgn(n, snr)
        dec = np.argmin(np.abs(r[:, None] - c[None, :]), axis=1)
        err = dec != tx
        iq_axes(ax, lim=2.0, label=False)
        if c[1] == 1j:
            ax.plot([-2, 2], [-2, 2], color=AMBER, lw=1.6, zorder=1)
        else:
            ax.axvline(0, color=AMBER, lw=1.6, zorder=1)
        ax.scatter(r[~err].real, r[~err].imag, s=5, color=BLUE, alpha=0.55, lw=0, zorder=2)
        ax.scatter(r[err].real, r[err].imag, s=11, color=RED, lw=0, zorder=4)
        ax.scatter(c.real, c.imag, s=50, color=NAVY, edgecolor="white", lw=1.2, zorder=5)
        ax.set_title(title, color=NAVY, fontsize=13, fontweight="bold", pad=4)
        ax.text(0, -2.35, f"{err.sum()} of {n} wrong", ha="center", color=RED if err.sum() else GREEN, fontsize=11)
        print(f"  {title} SNR {snr} dB: {err.sum()} wrong in {n}")
    write("L03-antipodal-orthogonal", fig)


def noise_clouds() -> None:
    c = constellation("QPSK")
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.6))
    for ax, snr in zip(axs, (20.0, 10.0, 4.0)):
        n = 600
        tx = RNG.integers(0, 4, n)
        r = c[tx] + awgn(n, snr)
        dec = np.argmin(np.abs(r[:, None] - c[None, :]), axis=1)
        err = dec != tx
        iq_axes(ax, lim=2.0)
        ax.axhline(0, color=AMBER, lw=1.6, zorder=1)
        ax.axvline(0, color=AMBER, lw=1.6, zorder=1)
        ax.scatter(r[~err].real, r[~err].imag, s=5, color=BLUE, alpha=0.55, lw=0, zorder=2)
        ax.scatter(r[err].real, r[err].imag, s=11, color=RED, lw=0, zorder=4)
        ax.scatter(c.real, c.imag, s=50, color=NAVY, edgecolor="white", lw=1.2, zorder=5)
        ax.set_title(f"SNR = {snr:.0f} dB", color=NAVY, fontsize=13, fontweight="bold", pad=4)
        ax.text(0, -2.35, f"{err.sum()} of {n} symbols in the wrong region", ha="center", color=RED if err.sum() else GREEN, fontsize=11)
        print(f"  QPSK SNR {snr:4.1f} dB: {err.sum()} wrong in {n}")
    write("L03-noise-clouds", fig)


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
    binary_pam()
    pam_noise()
    antipodal_orthogonal()
    constellations()
    noise_clouds()
    gray_8psk()
    impairments()
