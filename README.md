# ECE 448 — Software Defined Radios

Course site for ECE 448 (USAFA, Spring 2027): a Jupyter Book under `book/`,
built and published to GitHub Pages at
[livethisdream.github.io/ece448](https://livethisdream.github.io/ece448/) on
every push to `main`. It uses the ECE 444 site's shell and checks; see
[`CLAUDE.md`](CLAUDE.md) for the conventions and
[`project/ROADMAP.md`](project/ROADMAP.md) for the plan.

## Build and view

```sh
pip install -r requirements.txt
jupyter-book build book/ --all
python -m http.server -d book/_build/html 8000   # then open localhost:8000
```

## Add or change a lesson

Edit the `LESSONS` (or `LABS`) manifest in `scripts/scaffold_lessons.py`, then:

```sh
python scripts/scaffold_lessons.py
```

It writes any missing lesson pages and regenerates the module pages and the
table of contents.
