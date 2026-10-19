#!/bin/bash
# usage: grc_canvas.sh file.grc out.png [WxH]  -- screenshot GNU Radio Companion with the flowgraph open
# Bare Xvfb has no window manager, so xdotool cannot resize GRC; the window size
# and hidden side panels go into ~/.gnuradio/grc.conf before GRC starts instead.
# Run it under an Xvfb screen at least WxH (default 1280x820).
GRC="$1"; OUT="$2"; SIZE="${3:-1280x820}"; GW="${SIZE%x*}"; GH="${SIZE#*x}"
export NO_AT_BRIDGE=1
/usr/bin/python3.12 - "$GW" "$GH" <<'PY'
import configparser, os, sys
path = os.path.expanduser('~/.gnuradio/grc.conf'); os.makedirs(os.path.dirname(path), exist_ok=True)
c = configparser.ConfigParser(); c.optionxform = str; c.read(path)
if not c.has_section('main'): c.add_section('main')
for k, v in {'main_window_width': sys.argv[1], 'main_window_height': sys.argv[2],
             'console_window_visible': 'False', 'blocks_window_visible': 'False',
             'variable_editor_visable': 'False'}.items():
    c.set('main', k, v)
with open(path, 'w') as f: c.write(f)
PY
/usr/bin/python3.12 /usr/bin/gnuradio-companion "$GRC" >/dev/null 2>&1 &
PID=$!
for i in $(seq 1 40); do sleep 0.5; W=$(xdotool search --name "GNU Radio Companion" 2>/dev/null | head -1); [ -n "$W" ] && break; done
sleep 4
xdotool windowmove "$W" 0 0 2>/dev/null; sleep 1
xwd -root -silent | convert xwd:- -crop "${GW}x${GH}+0+0" "$OUT"
kill $PID 2>/dev/null
