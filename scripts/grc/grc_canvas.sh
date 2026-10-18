#!/bin/bash
# usage: grc_canvas.sh file.grc out.png  -- screenshot GNU Radio Companion with the flowgraph open
GRC="$1"; OUT="$2"
export NO_AT_BRIDGE=1
/usr/bin/python3.12 /usr/bin/gnuradio-companion "$GRC" >/dev/null 2>&1 &
PID=$!
for i in $(seq 1 40); do sleep 0.5; W=$(xdotool search --name "GNU Radio Companion" 2>/dev/null | head -1); [ -n "$W" ] && break; done
sleep 4
xdotool windowsize "$W" 1280 820 2>/dev/null; xdotool windowmove "$W" 0 0 2>/dev/null; sleep 2
xwd -root -silent | convert xwd:- -crop 1280x820+0+0 "$OUT"
kill $PID 2>/dev/null
