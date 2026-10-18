#!/usr/bin/env python3
"""L5: read an IQ capture from GNU Radio's File Sink and plot its power spectrum.

GNU Radio writes complex samples as interleaved 32-bit floats (I, Q, I, Q, ...),
which NumPy reads directly as complex64. This script estimates the power
spectral density by averaging FFTs, the same thing the frequency sink does.

    python L05-psd.py fm_capture.cfile --fs 2.4e6 --fc 100.1e6
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("file", help="IQ capture written by a GNU Radio File Sink (complex)")
ap.add_argument("--fs", type=float, default=2.4e6, help="sample rate, Hz")
ap.add_argument("--fc", type=float, default=0.0, help="center frequency the SDR was tuned to, Hz")
ap.add_argument("--nfft", type=int, default=2048, help="FFT size")
args = ap.parse_args()

x = np.fromfile(args.file, dtype=np.complex64)
print(f"{x.size} samples = {x.size / args.fs:.2f} s at {args.fs / 1e6:.2f} MS/s")
print(f"average power {10 * np.log10(np.mean(np.abs(x) ** 2)):.1f} dBFS")

# Average the power of many FFTs, windowed to keep a strong signal from
# leaking into its neighbors' bins.
n = args.nfft
frames = x[: (x.size // n) * n].reshape(-1, n)
win = np.hanning(n)
spec = np.fft.fftshift(np.fft.fft(frames * win, axis=1), axes=1)
psd = np.mean(np.abs(spec) ** 2, axis=0) / (args.fs * np.sum(win ** 2))
f = (args.fc + np.fft.fftshift(np.fft.fftfreq(n, 1 / args.fs))) / 1e6

plt.plot(f, 10 * np.log10(psd))
plt.xlabel("frequency (MHz)")
plt.ylabel("power spectral density (dB/Hz, relative to full scale)")
plt.title(f"{args.file}: {frames.shape[0]} averaged FFTs of {n} points")
plt.grid(True)
plt.show()
