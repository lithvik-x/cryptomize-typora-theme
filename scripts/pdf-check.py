#!/usr/bin/env python3
"""PDF export verification: render the harness page through Chromium's print engine
(page.pdf with print media — the same engine family Typora uses), then rasterize
pages for vision review. Usage: python3 scripts/pdf-check.py"""
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SHOTS = ROOT / "test" / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--allow-file-access-from-files"])
        for theme in ("cryptomize", "cryptomize-dark"):
            page = browser.new_page(viewport={"width": 1280, "height": 1000})
            page.goto((ROOT / "test" / "harness" / "page.html").as_uri())
            page.evaluate(
                """(href) => { document.getElementById('theme').href = href; }""",
                (DIST / f"{theme}.css").as_uri(),
            )
            page.evaluate("() => document.fonts.ready")
            page.wait_for_timeout(150)
            page.emulate_media(media="print")
            pdf_path = SHOTS / f"{theme}-export.pdf"
            page.pdf(path=str(pdf_path), format="A4", print_background=True)
            print(f"pdf: {pdf_path.name} ({pdf_path.stat().st_size:,} bytes)")
            page.close()
        browser.close()
    for theme in ("cryptomize", "cryptomize-dark"):
        pdf = SHOTS / f"{theme}-export.pdf"
        out = SHOTS / f"{theme}-export"
        subprocess.run(
            ["pdftoppm", "-png", "-r", "80", "-f", "1", "-l", "2", str(pdf), str(out)],
            check=True,
        )
        print("rasterized:", sorted(f.name for f in SHOTS.glob(f"{theme}-export-*.png")))


if __name__ == "__main__":
    main()
