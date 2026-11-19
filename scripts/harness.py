#!/usr/bin/env python3
"""Chromium harness for the ITS Typora themes.

V1 (parse gate): load each dist css in real Chromium (Typora's own parser family),
count parsed cssRules vs expected top-level rules, surface console errors.

V5 (visual): render a Typora-DOM replica page under each theme at multiple widths,
screenshot to test/shots/.

Usage: python3 scripts/harness.py v1|v5
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SHOTS = ROOT / "test" / "shots"


def expected_rule_count(css_text: str) -> int:
    """Count top-level rules + nested @media inner rules the way Chromium parses."""
    depth = 0
    rules = 0
    in_comment = False
    for i, ch in enumerate(css_text):
        if in_comment:
            if css_text[i - 1 : i + 1] == "*/":
                in_comment = False
            continue
        if css_text[i : i + 2] == "/*":
            in_comment = True
            continue
        if ch == "{":
            if depth == 0:
                rules += 1
            depth += 1
        elif ch == "}":
            depth -= 1
    return rules


def v1():
    from playwright.sync_api import sync_playwright

    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name in ("cryptomize.css", "cryptomize-dark.css"):
            page = browser.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.goto("about:blank")
            css_path = DIST / name
            parsed = page.evaluate(
                """(cssText) => {
                    const style = document.createElement('style');
                    style.textContent = cssText;
                    document.head.appendChild(style);
                    return document.styleSheets[0].cssRules.length;
                }""",
                css_path.read_text(),
            )
            expected = expected_rule_count(css_path.read_text())
            results[name] = {"parsed_rules": parsed, "expected_rules": expected, "console_errors": errors}
            page.close()
        browser.close()
    ok = True
    for name, r in results.items():
        ratio = r["parsed_rules"] / r["expected_rules"] if r["expected_rules"] else 0
        status = "PASS" if r["parsed_rules"] > 0 and ratio >= 0.98 and not r["console_errors"] else "FAIL"
        if status == "FAIL":
            ok = False
        print(f"V1 [{name}]: {status} — parsed {r['parsed_rules']}/{r['expected_rules']} rules, console errors: {r['console_errors']}")
    sys.exit(0 if ok else 1)


def v5():
    from playwright.sync_api import sync_playwright

    SHOTS.mkdir(parents=True, exist_ok=True)
    page_path = ROOT / "test" / "harness" / "page.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--allow-file-access-from-files"])
        for theme in ("cryptomize", "cryptomize-dark"):
            for width in (390, 1280, 1800):
                page = browser.new_page(viewport={"width": width, "height": 1000})
                page.goto(page_path.as_uri())
                page.evaluate(
                    """(href) => { document.getElementById('theme').href = href; }""",
                    (DIST / f"{theme}.css").as_uri(),
                )
                page.evaluate("() => document.fonts.ready")
                page.wait_for_timeout(150)
                out = SHOTS / f"{theme}-{width}.png"
                page.screenshot(path=str(out), full_page=True)
                print(f"shot: {out.name}")
                page.close()
        browser.close()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "v1"
    if mode == "v1":
        v1()
    elif mode == "v5":
        v5()
    else:
        print("modes: v1 | v5")
