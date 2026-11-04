---
name: write-lesson
description: Write a new ECE 448 lesson or lab page (or rewrite most of one) to the course's voice, "why", and illustration rules from the first draft, then run one parallel three-lens review and stop once for Neil's pick. Use it whenever a lesson thread creates or substantially rewrites a page under book/module*/; it replaces running the three sweeps afterwards.
argument-hint: <lesson number, e.g. 25>
---

# Write a lesson to the rules, then review it once

Neil, 2026-11-04: "Why do I have to do 3 separate sweeps after a lesson is
run? Why not just build those rules into the creation of lessons?" This skill
is that answer. The rules the voice, why, and illustration sweeps enforce are
applied while you write. One review pass at the end, three lenses in
parallel, replaces the three sweeps in sequence, with one stop for Neil
instead of three. The sweep skills stay for pages written before this one
existed.

The lesson is `$ARGUMENTS`. Read `CLAUDE.md` and `project/ROADMAP.md` first,
as for any work. This skill came from ECE 444, which this course follows
("Follow ECE 444" in CLAUDE.md), so its budgets, gotchas and checks are 444's.
This course's own rules, in its `CLAUDE.md` and `project/ROADMAP.md`,
override 444's where they differ. The ones that matter most here: **only
enough theory to get by** (Neil, 2026-10-17), so where 444 would put a
derivation on screen, 448 puts a flowgraph; **noise is shown, not
calculated** (no Eb/N0, BER, or probability-of-error math anywhere a cadet
sees); Neil's 2025 slides are the primary source, then the GNU Radio wiki
and tutorials, then PySDR.org.

## 1. Before you write a word

- Read `VOICE.md` in full, every time. It grows, and the newest rules (25,
  first person; 26, every sentence earns its place) are the ones most often
  missed.
- Read the earlier lessons this one builds on and note their notation and
  their flowgraphs with `grep -n`. A link to an earlier lesson names it.
- Plan the figures and widgets with the outline, not after it. Candidates,
  strongest first (the illustration sweep's list): a mechanism the reader has
  to imagine; a trade with an optimum; a number chain; a rule of thumb against
  its data; a comparison stated in prose; the lesson's central idea, if it
  has no picture. Check `book/extras/viz/` and `viz/img/` for something to
  reuse first. A widget frame is a present beat; count it in the budget
  (`scripts/verify/budgets.py`).
- Every flowgraph the page ships follows CLAUDE.md "Flowgraphs": normalize
  it, compile it with `check_grc.py`, and run it headless for its screenshot
  if it needs no hardware. The PlutoSDR is the radio and GNU Radio is the
  tool; a signal the course generates goes out at 915 MHz, never on its real
  frequency. Recordings are SigMF.

## 2. While you write

Every sentence, as you write it:

- **Earns its place.** Ask what a cadet does or understands differently
  because of it. If nothing, leave it out; if something, say that thing.
  Build anecdotes, history, asides and repeated caveats are the usual
  offenders (VOICE 26).
- **Is in voice.** Complete sentences, active voice with the agent named,
  plain verbs, no kickers, no figurative or money framing, "we" for the
  lesson's own reasoning, first person for Neil and never "the instructor",
  bold on terms not claims, Title Case noun-phrase frame titles, American
  spelling (VOICE.md, all of it).
- **Says where a result comes from**, as far as the flowgraph needs it: a
  block, a plot the cadet can make, or one physical reason, not a
  derivation. Define every term the course has not; grep the earlier lessons
  before calling one undefined.
- **Has its numbers recomputed.** Compute every number in Python as you
  write it, not afterwards. Past sweeps found 0.01λ that should have been
  0.15λ, and 20 dB that should have been 23.
- **Agrees with the rest of the lesson.** One value per quantity, everywhere
  it appears.

Every frame:

- A present block is two to four short bullets, a figure, a table, an
  equation chain, or a callout: 40 words at most, and it states the point,
  never a teaser for it. The connective prose goes outside the present
  blocks, where read mode shows it.
- A non-trivial equation gets its own display line, and a derivation runs
  general to specific as one chain aligned on the equals signs.
- The frame title is a directive argument, fences nest (`::::` frame, `:::`
  inside), and the frame fits one screen in present mode.
- No math in the raw-HTML objectives list, `\vert` not `|` in table math,
  `\ ` not `\,` or `\;`, no thin spaces (CLAUDE.md gotchas).

Figures and widgets as you go: generators in `scripts/graphics/` through
`apply_font_stack()`, widgets from an existing widget in `book/extras/viz/` as
the template and inside `check_widget.py`'s budgets; the illustration
sweep's "Phase 2" section has the details and the screenshot list.

## 3. Check the draft yourself

```sh
python3 scripts/verify/check_voice.py L<NN>        # 0 FAIL; read every WARN
python3 scripts/verify/check_density.py L<NN>      # beats and words
jupyter-book build book/ --all                     # 0 warnings
python3 scripts/verify/check_frames.py L<NN>       # every frame fits
TEXINPUTS=/workspace/latex-tools/tex/latex//: scripts/verify/mech_check.sh <NN> <slug>
python3 scripts/verify/check_math.py                # no display equation scrolls at 320-390
python3 scripts/verify/check_grc.py                 # every flowgraph compiles
```

`check_voice.py` runs in CI on every page, so a FAIL there blocks the PR
anyway; a WARN (passive, money words) is a sentence to read and usually
rewrite.

## 4. One review, three lenses, in parallel

Start three `reviewer` subagents in one message, so they run at once. Give
each the page(s), the practice source if there is one, the earlier lessons the
page links to, and exactly one lens:

| Prefix | Lens | Give it |
| :-- | :-- | :-- |
| `VOI` | voice | `VOICE.md`, and the reading list in `.claude/skills/voice-sweep/SKILL.md` phase 1 |
| `WHY` | why | the "Look for" list in `.claude/skills/why-sweep/SKILL.md` phase 1, including recomputing every number |
| `ILL` | illustration | the ranking list in `.claude/skills/illustration-sweep/SKILL.md` phase 1, and the beat budget |

Merge their findings into one table: rank by student impact, drop
duplicates, and put each finding's proposed fix in one line. Then **stop
and wait for Neil's pick**, once, for all three lenses. Fix what he picks,
rerun section 3, and look at the present-mode screenshot of every frame you
changed at 390 and 1280.

## 5. Finish

The PR body lists the review findings fixed and the ones Neil left, every
number corrected, and anything outside the lesson's files under "For the
Integrator". A lesson thread does not edit `project/ECE448_PROJECT.md` or the ROADMAP; report status in the PR body.

After the lesson is taught, what the cadets actually tripped over is the one
thing no draft review can catch: when Neil reports it, fix the page in a
short follow-up PR.
