#!/usr/bin/env python3
"""Every display equation fits its column on a phone, without scrolling.

check_shell.py catches a page that scrolls sideways, but a wide equation does
not make the page scroll: MathJax gives it its own horizontal scroller, so the
page passes and the reader swipes the equation instead. Found on L2's noise
floor frame (2026-10-18, Neil, on a phone). This renders every page at three
phone widths with the vendored MathJax and lists each display equation wider
than its container, with its TeX, so the fix is to break it across aligned
lines.

    scripts/verify/check_math.py                     # every built page
    scripts/verify/check_math.py module01/L02-noise-figure-link-budget/index.html
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _common import launch, make_cdn_router, require_vendored, serve  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2] / "book" / "_build" / "html"
SKIP_DIRS = {"slides", "viz", "_static", "legacy", "practice", "_sources"}
WIDTHS = (320, 360, 390)

PROBE = """() => [...document.querySelectorAll('mjx-container[display="true"]')]
  .map(e => {
    const items = MathJax.startup.document.getMathItemsWithin(e);
    return { over: e.scrollWidth - e.clientWidth,
             tex: items.length ? items[0].math.replace(/\\s+/g, ' ').slice(0, 100) : '' };
  })
  .filter(x => x.over > 1)"""


def main() -> int:
    require_vendored()
    pages = sys.argv[1:] or sorted(
        str(p.relative_to(ROOT)) for p in ROOT.rglob("*.html")
        if not SKIP_DIRS.intersection(p.relative_to(ROOT).parts))
    httpd, port = serve(ROOT)
    bad = []
    with sync_playwright() as p:
        browser = launch(p)
        for w in WIDTHS:
            page = browser.new_page(viewport={"width": w, "height": 844})
            page.route("**/*", make_cdn_router())
            for u in pages:
                page.goto(f"http://127.0.0.1:{port}/{u}")
                page.wait_for_function("() => !window.MathJax || (MathJax.startup && MathJax.startup.document)", timeout=15000)
                page.evaluate("() => window.MathJax && MathJax.startup.promise")
                if not page.evaluate("() => !!window.MathJax"):
                    continue
                for x in page.evaluate(PROBE):
                    bad.append((w, u, x["over"], x["tex"]))
            page.close()
        browser.close()
    httpd.shutdown()
    print(f"checked {len(pages)} pages at {', '.join(map(str, WIDTHS))} px")
    if not bad:
        print("every display equation fits its column")
        return 0
    print(f"\n{len(bad)} EQUATION(S) SCROLL SIDEWAYS (break them across aligned lines):")
    for w, u, over, tex in bad:
        print(f"  {w}px {u}: {over}px too wide: {tex}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
