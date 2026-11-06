#!/usr/bin/env python3
"""L5: read a SigMF IQ recording and plot its power spectrum.

A SigMF recording is a pair: fm_capture.sigmf-data holds the samples, and
fm_capture.sigmf-meta, a small text file, says how to read them: the datatype,
the sample rate, and the center frequency. The script reads the meta file, so
it needs no numbers from you:

    python L05-psd.py fm_capture.sigmf-data

GNU Radio's SigMF Sink writes complex samples as interleaved 32-bit floats
(I, Q, I, Q, ..., datatype cf32_le), which NumPy reads directly as complex64.
The script estimates the power spectral density by averaging FFTs, the same
thing the frequency sink does. A raw file with no meta still works if you give
the numbers yourself: python L05-psd.py fm.cfile --fs 2.4e6 --fc 100.1e6
"""
import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("file", help="the .sigmf-data (or .sigmf-meta) file of a recording")
ap.add_argument("--fs", type=float, help="sample rate, Hz (default: from the .sigmf-meta)")
ap.add_argument("--fc", type=float, help="center frequency, Hz (default: from the .sigmf-meta)")
ap.add_argument("--nfft", type=int, default=2048, help="FFT size")
args = ap.parse_args()

path = Path(args.file)
if path.suffix in (".sigmf-data", ".sigmf-meta", ".sigmf"):
    path = path.with_suffix("")
data = path.with_name(path.name + ".sigmf-data")
meta_file = path.with_name(path.name + ".sigmf-meta")
if not data.exists():                  # a raw file such as fm.cfile
    data, meta_file = Path(args.file), None

fs, fc = args.fs, args.fc
if meta_file is not None and meta_file.exists():
    meta = json.loads(meta_file.read_text())
    datatype = meta["global"]["core:datatype"]
    if datatype != "cf32_le":
        raise SystemExit(f"{meta_file} says {datatype}; this script reads cf32_le only")
    fs = fs or meta["global"]["core:sample_rate"]
    fc = fc if fc is not None else meta["captures"][0].get("core:frequency", 0.0)
    print(f"from {meta_file.name}: {datatype}, {fs / 1e6:.3f} MS/s, center {fc / 1e6:.3f} MHz")
if fs is None:
    raise SystemExit(f"no .sigmf-meta beside {data}; give the sample rate with --fs")
fc = fc or 0.0

x = np.fromfile(data, dtype=np.complex64)
print(f"{x.size} samples = {x.size / fs:.2f} s at {fs / 1e6:.2f} MS/s")
print(f"average power {10 * np.log10(np.mean(np.abs(x) ** 2)):.1f} dBFS")

# Average the power of many FFTs, windowed to keep a strong signal from
# leaking into its neighbors' bins.
n = args.nfft
frames = x[: (x.size // n) * n].reshape(-1, n)
win = np.hanning(n)
spec = np.fft.fftshift(np.fft.fft(frames * win, axis=1), axes=1)
psd = np.mean(np.abs(spec) ** 2, axis=0) / (fs * np.sum(win ** 2))
f = (fc + np.fft.fftshift(np.fft.fftfreq(n, 1 / fs))) / 1e6

plt.plot(f, 10 * np.log10(psd))
plt.xlabel("frequency (MHz)")
plt.ylabel("power spectral density (dB/Hz, relative to full scale)")
plt.title(f"{data.name}: {frames.shape[0]} averaged FFTs of {n} points")
plt.grid(True)
plt.show()
