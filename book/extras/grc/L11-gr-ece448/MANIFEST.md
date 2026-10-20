title: The ECE448 OOT Module
brief: ECE 448 course blocks: an Energy Detector for keyed and on-off signals
tags: # Tags are arbitrary, but look at CGRAN what other authors are using
  - sdr
author:
  - ECE 448, USAF Academy
copyright_owner:
  - USAFA ECE 448
license: GPL-3.0-or-later
gr_supported_version: v3.10
#repo: # Put the URL of the repository here, or leave blank for default
#website: <module_website> # If you have a separate project website, put it here
#icon: <icon_url> # Put a URL to a square image here that will be used as an icon on CGRAN
---
The ECE 448 out-of-tree module, built with gr_modtool in Lesson 11. It holds
one Python block, the Energy Detector, which averages the power of a complex
stream and keys on and off with a threshold and hysteresis.
