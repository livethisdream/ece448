# gr-ece448

The ECE 448 out-of-tree module from Lesson 11. `gr_modtool newmod ece448`
made the tree, and `gr_modtool add` added one Python block, the **Energy
Detector**. Three files hold the block:

| File | What it holds |
| :-- | :-- |
| `python/ece448/energy_detector.py` | the block: one complex input, two float outputs (power in dB, key) |
| `grc/ece448_energy_detector.block.yml` | how GRC shows it: label, parameters, ports, callbacks |
| `python/ece448/qa_energy_detector.py` | the unit test that `ctest` runs |

## Build, test, and install (Linux and macOS, radioconda)

From the radioconda prompt, once per laptop:

```sh
conda install -c conda-forge gnuradio-build-deps
```

macOS also needs Apple's command-line tools (`xcode-select --install`). Then,
from this directory:

```sh
mkdir build
cd build
cmake -G Ninja -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} -DCMAKE_PREFIX_PATH=${CONDA_PREFIX} ..
cmake --build .
ctest --output-on-failure
cmake --install .
```

Restart GRC. The block is in the **ECE 448** category of the block library.

## Ubuntu's own GNU Radio package

```sh
sudo apt install gnuradio-dev cmake g++
mkdir build && cd build
cmake ..
make
ctest --output-on-failure
sudo make install
```

## Windows

A Python-only module still runs CMake, and CMake needs a C++ compiler. On
Windows, conda-forge's `gnuradio-build-deps` finds the compiler only in an
existing Visual Studio 2022 Build Tools install, which this course has not
tested. Use one of these instead, in this order:

1. WSL2 with Ubuntu 24.04: inside it, follow the Ubuntu steps above. WSLg
   opens GRC in a window.
2. Paste `python/ece448/energy_detector.py` into an Embedded Python Block,
   renaming the class `blk`, as `L11-keyed-carrier-epy.grc` does.

The Lesson 11 page has the details.
