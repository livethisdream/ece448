---
name: "#ece448"
dateCreated: 2026-08-01
dateModified: 2026-08-12
container: cdocker
---
# Overview

ECE 448 — **Software Defined Radios** — is Neil's **Spring 2026** course. The course site is a **Jupyter Book** at `~/projects/ece448/`, patterned exactly on the ECE 444 migration (which was in turn patterned on usafa-ece/ece215-book). It publishes to **https://livethisdream.github.io/ece448/** from the `livethisdream/ece448` GitHub repo.

Grading is **25% Engagement / 35% Midterm / 40% Final Project**. The book was migrated off the Chirpy `_ece448/` collection on 2026-07-31 to preempt a 404 once the umbrella SPA migration retires the Chirpy site — the SPA landing card links to `/ece448/`, and the Chirpy `/ece448/` tab was the only thing serving it before.

# Special Instructions

- The authoritative tree is `~/projects/ece448` (this repo). Older copies at `C:\...\USAFA\ece448` (OneDrive) and `~/src/ece448` (WSL) are stale — do not commit to either. `livethisdream.github.io` (Chirpy) is historical.
- Keep reveal.js decks; same shared `course-slides.css` and reveal 5.1.0 shell as ECE 444.
- Author lessons **as they get taught during the semester**, not all up-front. The 22–27-line `_TBD` placeholders in the old Chirpy tree are not worth carrying over.

# Decisions

- **2026-08-16** — **Migrated to `~/projects/ece448/` (WSL-native).** OneDrive clone at `.../USAFA/ece448` remains as historical fallback; don't commit to it. Rebuilt `.venv/` in-repo on CPython 3.10.20 (matches CI per `deploy.yml`, pinned via new `.python-version`). Renamed the in-repo project note to `ece448_PROJECT.md` at repo root.
- **2026-08-16** — **Course figures moved to `figures/` at repo root** (104 files / 30 MB, from `latex-tools/figures/ECE448/`). New LaTeX convention: `\graphicspath{{./figures/}}` — LaTeX-native, no absolute paths, no shared-tool coupling. The old central-figures pattern was a workaround for a relative-path issue; this is the fix.
- **2026-08-16** — **Private faculty repo (`livethisdream/ECE448-faculty`) nested at `faculty/ECE448-Spring-2025/`.** Public repo's `.gitignore` has `/faculty/`, so nothing under it ever lands in the public tree. Per-semester subdirs each get their own clone. LaTeX inside `faculty/<semester>/` reaches public figures via `\graphicspath{{./figures/}{../../figures/}}`. Fixed the local remote pointer (was aiming at the redirected `ECE448` public repo — a footgun before the fix).
- **2026-08-16** — **latex-tools relocated from OneDrive to `~/projects/latex-tools/` (WSL-native git repo).** `sync.py`'s `LATEX_TOOLS_HOST` and the `~/texmf/tex/latex/` symlinks updated. Container-side `kpsewhich myShortcuts.tex` verified against the new path. The comma-in-path kpathsea workaround is no longer needed (new path is comma-free). Remote `Neil-Rogers_adi/latex-tools` currently returns "Repository not found" — pending fix or replacement before any push.
- **2026-07-31** — Migrated ECE 448 off the Chirpy `_ece448/` collection onto a standalone Jupyter Book at `~/src/ece448/`. Reason: the umbrella SPA cutover will retire the Chirpy site, so `livethisdream.github.io/ece448/` needed a new home before the SPA landing card 404s.
- **2026-07-31** — Renamed GitHub repo from `ECE448` → lowercase `ece448`. Reason: same URL case-mismatch trap avoided on ECE 444.
- **2026-07-31** — Intentionally *did not* migrate L2–L40 stub content or the 4 phantom "built-out" decks. Reason: they were never real content, and prior git inspection showed the "built 5 legacy decks" commit (`8bdc6c9`) was a scaffold-of-stubs — only L1's deck actually existed.

# Plan

**Phase (current): Author lessons in-semester as they get taught.**

- L1 Course Introduction — done (128 lines, 11 bio photos).
- L2–L40 — author each into `book/moduleXX/` as it hits the schedule.

**Later:**
- Port the 5 legacy Beamer decks (L4, L7, L8, L13, L31) to reveal.js if/when those lessons come up.
- Rebuild the built-out reveal decks that the Chirpy repo never actually shipped.

# Status

- Full book scaffold shipped: `_config.yml`, `_toc.yml`, `intro.md` (hero + 7 module cards + 3 deliverable cards), `syllabus.md` (390 lines), `materials.md` (51 lines).
- Module 1 seeded — `book/module01/index.md` + L1 with 11 bio photos in `book/module01/L01-course-intro/img/`.
- L1 reveal.js deck live at `book/extras/slides/01-course-intro.md` on the shared `course-slides.css`.
- All 13 legacy Beamer PDFs (26 MB) shipped under `book/_static/legacy-slides/` (+ `refs/` subdir) as a reference until each lesson is ported.
- Deploy live at `https://livethisdream.github.io/ece448/`.

# ToDo

- [ ] Author L2 lesson notes + deck when L2 hits the schedule.
- [ ] Continue L3+ authoring lesson-by-lesson through the semester.
- [ ] Port each legacy Beamer PDF to a reveal.js deck as its lesson is authored.
