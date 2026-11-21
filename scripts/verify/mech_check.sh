#!/usr/bin/env bash
# Mechanical checks (REVIEW.md section A) for one lesson.
#
#   scripts/verify/mech_check.sh <NN> <slug>
#   e.g. scripts/verify/mech_check.sh 07 simple-resonant-antennas
#
# Lessons only. A lab child page (LNN-lab-<slug>, 2026-10-13) is a procedure
# page with no deck gate of its own, as the L04 lab never had one;
# check_density.py and check_frames.py still measure it.
#
# Everything here is scripted because it is decidable: files present, LaTeX
# compiles, decks and widgets render. Substance
# -- physics, derivations, difficulty -- is not checked here and never should
# be; that is the orchestrator's job (REVIEW.md section B).
#
# Requires the vendored render harness (cd scripts/verify && npm install).
#
# No lesson has a practice set (Neil, 2026-11-21: "I don't really need
# practice sets. The labs are the main thing"). A lesson with a lab carries a
# read-only "Preparing for the Lab" frame that links its lab packet (gate 7);
# a lesson without one links nothing in its place. The practice sources and
# PDFs stay in the repo, unlinked, and are not checked here.
#
# This gate is per-lesson. Two sweeps are site-wide and belong at the END of a
# batch, not here -- run them once when the batch is done:
#   scripts/verify/check_shell.py    every page, two widths
#   scripts/verify/check_bar.py      the HUD's geometry on both shells
set -u

if [ $# -lt 2 ]; then
  echo "usage: $0 <NN> <slug>   e.g. $0 07 simple-resonant-antennas" >&2
  exit 2
fi

NN="$1"; SLUG="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
LNN="L${NN}-${SLUG}"

# A lab page has no deck or required widget, so the lesson gate
# below would report those as failures. Say so instead of failing.
case "$SLUG" in
  lab-*)
    echo "$LNN is a lab page; mech_check is for lessons. Run" >&2
    echo "  scripts/verify/check_density.py L$NN and scripts/verify/check_frames.py L$NN" >&2
    exit 2 ;;
esac

fails=0
ok(){ echo "  PASS  $1"; }
bad(){ echo "  FAIL  $1"; fails=$((fails+1)); }

echo "== ${LNN} =="

# Locate the lesson page, and take the module number from where it actually
# lives rather than assuming a lesson-to-module mapping.
page="$(ls -d "$REPO"/book/module*/"$LNN"/index.md 2>/dev/null | head -1)"
if [ -z "$page" ]; then
  bad "lesson page not found under book/module*/$LNN/"
  echo "== ${LNN}: $fails failure(s) =="
  exit $fails
fi
MOD="$(basename "$(dirname "$(dirname "$page")")" | sed 's/^module0*//')"

# 1. files exist, page is not a stub
[ -s "$page" ] && ! grep -q "under construction" "$page" \
  && ok "lesson page non-stub (module $MOD)" || bad "lesson page missing/stub"
[ -s "$REPO/book/extras/slides/$LNN.md" ] && ok "deck md" || bad "deck md missing"
[ -s "$REPO/book/extras/slides/$LNN.html" ] && ok "deck html" || bad "deck html missing"

widgets="$(grep -oE 'viz/[a-z0-9-]+\.html' "$page" 2>/dev/null | sed 's|viz/||' | sort -u)"
for w in $widgets; do
  [ -s "$REPO/book/extras/viz/$w" ] && ok "widget $w exists" \
    || bad "widget $w referenced but missing"
done
[ -n "$widgets" ] && ok "page references $(echo "$widgets" | wc -w) widget(s)" \
  || bad "page references no interactive graphic"

# 3a. deck separators -- must run before the render check, because a dead
# separator merges two slides and then shows up as a bogus "slide too tall"
# rather than as what it is.
if sep=$(python3 "$HERE/check_separators.py" "$LNN" 2>&1); then
  ok "deck separators: all '---' live"
else
  bad "deck separators: $(echo "$sep" | grep -c 'line ') dead -- two slides are merged"
  echo "$sep" | grep '  line ' | sed 's/^/        /'
fi

# 3b. deck render
if python3 "$HERE/check_deck.py" "$LNN" >"/tmp/mc_deck_$NN.log" 2>&1; then
  ok "deck render: $(grep -m1 -E '^[A-Za-z0-9._-]+: [0-9]+ slides' "/tmp/mc_deck_$NN.log")"
else
  bad "deck render (see /tmp/mc_deck_$NN.log)"
fi

# 3c. frame budget -- only for a lesson that has opted into the frame view.
# A frame taller than the viewport is the deck's "slide too tall" defect in a
# new place: the build is happy and the bottom of the frame is simply gone when
# you present it. It has shipped that way before, so it is a gate, not a sweep.
if grep -qE '^frame_view:' "$page"; then
  if fr=$(python3 "$HERE/check_frames.py" "$LNN" 2>&1); then
    ok "frame budget: $(echo "$fr" | head -1)"
  else
    bad "frames over budget"
    echo "$fr" | sed 's/^/        /'
  fi
else
  ok "not a frame page (no frame_view in front matter)"
fi

# 3c2. phone-width math -- a display equation wider than the column does not
# scroll the page, so check_shell misses it; MathJax scrolls it in place and
# the reader swipes the equation. Found on L2 on a phone (Neil, 2026-10-18).
rel="${page#$REPO/book/}"; rel="${rel%.md}.html"
if mw=$(python3 "$HERE/check_math.py" "$rel" 2>&1); then
  ok "phone math: $(echo "$mw" | tail -1)"
else
  bad "display equations scroll sideways on a phone"
  echo "$mw" | sed -n '/SCROLL/,$p' | sed 's/^/        /'
fi

# 3d. present-mode density -- what the class sees, counted from the source.
# Forty words a frame and thirty frames a lesson (Neil, 2026-09-03). A lesson
# that has not been cut yet (no :::{present} block) is reported, not failed:
# the gate bites once the lesson opts in. Static, so it costs nothing.
if grep -qE '^frame_view:' "$page"; then
  if dn=$(python3 "$HERE/check_density.py" "$LNN" 2>&1); then
    ok "present density: $(echo "$dn" | head -1 | sed 's/  */ /g')"
  else
    bad "present density over budget"
    echo "$dn" | grep -E '^\s+(!!|LO)' | sed 's/^/        /'
  fi
fi

# 4. widget render, height, overflow, aspect
for w in $widgets; do
  if python3 "$HERE/check_widget.py" "$REPO/book/extras/viz/$w" \
       >"/tmp/mc_w_${NN}_$w.log" 2>&1; then
    ok "widget $w: $(grep -m1 'worst-case height' "/tmp/mc_w_${NN}_$w.log")"
  else
    bad "widget $w (see /tmp/mc_w_${NN}_$w.log)"
  fi
done

# 5. greps for the gotchas that ship silently
files="$page $REPO/book/extras/slides/$LNN.md"
grep -lP '\x{2009}' $files 2>/dev/null | grep -q . \
  && bad "U+2009 thin space found" || ok "no thin spaces"
grep -nE '\\[,;]' "$REPO/book/extras/slides/$LNN.md" 2>/dev/null \
  | grep -v '\\lbrace\|\\rbrace' | head -3 | grep -q . \
  && bad "deck has \\, or \; in math" || ok "deck free of \\, \;"
if python3 "$HERE/check_tables.py" "$page" "$REPO/book/extras/slides/$LNN.md"; then
  ok "no | inside table math"
else
  bad "raw | inside \$..\$ splits a table cell (use \\vert)"
fi
grep -q 'class="lo-list"' "$page" && grep -q -- "--module: '$MOD'" "$page" \
  && ok "LO markup, course objective, module $MOD" || bad "LO markup wrong for module $MOD"

# 6. voice self-check (VOICE.md) -- self-praise words, never in course prose
if grep -nEi '\b(honest|genuinely|rigorous|no hand-waving|is the price)\b' \
     "$page" "$REPO/book/extras/slides/$LNN.md" 2>/dev/null | head -5 | grep -q .; then
  bad "VOICE.md: self-vouching wording found"
  grep -nEi '\b(honest|genuinely|rigorous|no hand-waving|is the price)\b' \
    "$page" "$REPO/book/extras/slides/$LNN.md" 2>/dev/null | head -5 | sed 's/^/          /'
else
  ok "VOICE.md: no self-vouching wording"
fi

# 7. the lab packet link. A lesson with a lab (a sibling LNN-lab-* page, or
# a shared one such as L18-L19-lab-*) links that lab's blank packet from its
# read-only "Preparing for the Lab" frame, and the PDF must be committed. A
# lesson without a lab links nothing in its place. No lesson links a practice
# set any more (Neil, 2026-11-21).
lab=""
for d in "$REPO"/book/module*/L*-lab-*/; do
  [ -d "$d" ] || continue
  pre="$(basename "$d")"; pre="${pre%%-lab-*}"
  case "-$pre-" in *"-L$NN-"*) lab="$(basename "$d")" ;; esac
done
packet="$(grep -oE 'class="doc-link" href="\.\./\.\./labs/ECE448_Lab_[A-Za-z0-9_]+_blank\.pdf"' "$page" \
  | head -1 | sed -E 's|.*labs/||; s|"$||')"
if grep -qE 'Practice_(blank|SOLUTIONS)\.pdf' "$page"; then
  bad "lesson page still links a practice set (retired 2026-11-21)"
fi
if [ -n "$lab" ]; then
  if [ -z "$packet" ]; then
    bad "lesson has a lab ($lab) but links no lab packet"
  elif [ -s "$REPO/book/extras/labs/$packet" ]; then
    grep -q '{frame} Preparing for the Lab' "$page" \
      && ok "Preparing for the Lab links $packet" \
      || bad "lab packet linked, but no 'Preparing for the Lab' frame"
  else
    bad "lab packet $packet linked but not built"
  fi
else
  ok "no lab, so no lab packet to link"
fi

echo "== ${LNN}: $fails failure(s) =="
exit $fails
