#!/usr/bin/env python3
"""Every flowgraph a cadet downloads compiles under GNU Radio 3.10.

A .grc file that GRC cannot load reaches the class as an error dialog. This
compiles every book/extras/grc/*.grc with grcc, the same code generator GRC's
run button uses, and fails on any that does not produce a Python file. It does
not run them: a flowgraph with an SDR source needs the hardware. Run the ones
that need none with scripts/grc/grc_shot.py under xvfb-run.

GNU Radio must be installed (apt install gnuradio on Ubuntu 24.04 gives
3.10.9). Its Python bindings are built for the system Python, so this calls
grcc through /usr/bin/python3.12 rather than whatever python3 is first on PATH.

    scripts/verify/check_grc.py
"""
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
PY = "/usr/bin/python3.12"


def main() -> int:
    files = sorted((ROOT / "book/extras/grc").glob("*.grc"))
    if not files:
        print("no flowgraphs in book/extras/grc")
        return 0
    bad = []
    with tempfile.TemporaryDirectory() as out:
        for f in files:
            r = subprocess.run([PY, "/usr/bin/grcc", "-o", out, str(f)], capture_output=True, text=True)
            ok = r.returncode == 0 and "Generating" in r.stdout + r.stderr
            print(f"  {'PASS' if ok else 'FAIL'}  {f.name}")
            if not ok:
                bad.append((f.name, (r.stdout + r.stderr).strip().splitlines()[-3:]))
    if bad:
        for name, tail in bad:
            print(f"\n{name}:\n    " + "\n    ".join(tail))
        return 1
    print(f"all {len(files)} flowgraph(s) compile")
    return 0


if __name__ == "__main__":
    sys.exit(main())
