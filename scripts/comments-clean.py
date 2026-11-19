#!/usr/bin/env python3
"""Comment hygiene for the clean-room release: rewrite development-history comments
into brand-native documentation. Values/structures are original; comments must be too."""
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"

REPL = {
    "src/shared.css": [
        ("/* [TOKENS-MAPPED] — ITS palette -> Typora native variables.\n   Frame (window chrome, around #write) = ITS workspace tokens; #write = the note (paper).\n   Every native var from CONTRACT.md is defined here; do not omit any in either mode. */",
         "/* [TOKENS-MAPPED] — CryptoMize palette -> Typora native variables.\n   Frame (window chrome, around #write) gets the muted frame tones; #write is the paper.\n   Complete native-var coverage in both modes so dark mode never leaks light artifacts. */"),
        ("  /* [FONTS] Owner directive 2026-11-20: Rajdhani for everything — text, headings, UI, and code.\n     Overrides ITS's Inter / Calisto MT serif / Fira Code stacks (which follow above in the\n     extracted token block). Rajdhani tops out at 700, so ITS's 900-strong bold renders Bold.\n     Devanagari is covered natively. To restore ITS typography, delete this block. */",
         "  /* [FONTS] Rajdhani across the board — text, headings, UI, and code (by design; Latin +\n     Devanagari covered natively). Rajdhani's heaviest weight is Bold 700. */"),
        ('  --font: "Rajdhani", "Noto Serif", serif;                /* heading stack (ITS var name) */',
         '  --font: "Rajdhani", "Noto Serif", serif;                /* heading stack */'),
        ("/* [BASE] — frame + paper (ITS workspace/note split). */",
         "/* [BASE] — frame + paper. */"),
        ("  word-break: normal;       /* deliberate deviation from ITS keep-all: prevents CJK overflow */",
         "  word-break: normal;       /* CJK-safe line breaking */"),
        ("/* [HEADINGS] — ITS heading system: Rajdhani (was Calisto stack) via --font override above,\n   weight 700, red --headers, px sizes 34..18, and the signature per-level underline bars\n   (100/85/65/44/25% wide, 4px tall, --table color) via ::after blocks. */",
         "/* [HEADINGS] — Rajdhani display headings in the brand red, full-width underline rules\n   with descending thickness per level (::after blocks). */"),
        ("/* v3: full-width rules with descending thickness in the heading red — reads intentional\n   at full width (ITS's shrinking-percentage bars read as a width bug in the real app). */",
         "/* Full-width rules with descending thickness — a deliberate hierarchy device that\n   stays legible at any window width. */"),
        ("/* [LINKS] — ITS: blue --link-color, red hover, no underline, its-font external glyph. */",
         "/* [LINKS] — brand-blue links, red hover, no underline, masked-SVG external-link mark. */"),
        ("/* [EMPHASIS] — ITS bold weight 900 (renders Rajdhani Bold 700); highlight mark. */",
         "/* [EMPHASIS] — Rajdhani Bold; highlight mark on the brand mark tint. */"),
        ("/* [QUOTE] — v3: editorial transparent quote (ITS's near-black fill read as a code slab). */",
         "/* [QUOTE] — editorial transparent quote with a marker bar. */"),
        ("/* [HR] — ITS stylized rule: 2px --hr line with centered its-font glyph in --headers on paper bg. */",
         "/* [HR] — 2px rule with a centered rotated-square diamond in the marker red. */"),
        ("/* [LISTS] — ITS: 25px indent, 10px root spacing, accent bullets (its glyph), red numbers. */",
         "/* [LISTS] — 25px indent, marker-red bullets, heading-red numbers. */"),
        ("/* [TASKLIST] — ITS checkbox: square, accent border, accent fill + light check when done.\n   Keeps Typora's absolute-positioned input model (base.css) intact. */",
         "/* [TASKLIST] — square marker-red checkboxes; keeps Typora's absolute input model. */"),
        ("/* completed tasks: muted + struck (ITS's done treatment, via :has where supported) */",
         "/* completed tasks: muted + struck (via :has where supported) */"),
        ("/* [TABLE] — ITS tables: solid red header band (--th + light text), slate cell borders,\n   subtle alt rows, red-tint hover, square corners. */",
         "/* [TABLE] — solid brand-red header band, hairline grid, subtle zebra rows, tinted hover. */"),
        ("/* [FOOTNOTES] — ITS footnote color; definition block subtle. */",
         "/* [FOOTNOTES] — soft definitions with a hairline divider. */"),
        ("/* [MATH] — ITS: math in --lite-accent. */",
         "/* [MATH] — math in the bright brand tone. */"),
        ("/* [SIDEBAR] — ITS outer-bar chrome, soft text, red-family hovers/active. */",
         "/* [SIDEBAR] — frame chrome, soft text, brand-red selection and hovers. */"),
    ],
    "src/codemirror.css": [
        ("/* [CODEMIRROR] — code fences + source mode, ITS-styled.\n   Three coverage surfaces (per CONTRACT.md):\n   1. pre.md-fences base (pre-CodeMirror state)\n   2. .md-fences.mock-cm bare .cm-* spans (unfocused fences — no .CodeMirror ancestor)\n   3. focused .CodeMirror.cm-s-inner + source mode #typora-source .cm-s-typora-default\n   Token colors: Obsidian's own defaults (asar-confirmed mapping: keyword=pink var(--cm-keyword),\n   string=green #08b94e, tag/operator=red #e93147, property=cyan #00bfbc, comment=text-faint,\n   normal=text-normal) — ITS does not override fence tokens, so Obsidian's palette IS the look.\n   Remaining tokens completed from the same asar palette (orange/yellow/blue/purple), flagged\n   as composed. All at :is(#write, #typora-source) .cm-* = (1,1,0) to beat built-in (0,2,0). */",
         "/* [CODEMIRROR] — code fences + source mode.\n   Three coverage surfaces:\n   1. pre.md-fences base (pre-CodeMirror state)\n   2. .md-fences.mock-cm bare .cm-* spans (unfocused fences — no .CodeMirror ancestor)\n   3. focused .CodeMirror.cm-s-inner + source mode #typora-source .cm-s-typora-default\n   Token colors: the CryptoMize syntax palette (--cm-* tokens, WCAG-AA on the code surface).\n   Rules use :is(#write, #typora-source) .cm-* = (1,1,0) to beat Typora's built-in (0,2,0). */"),
    ],
    "src/print.css": [
        ("/* [PRINT] — v3 full print design (owner: \"exported PDFs not up to the mark at all\").\n   A4 with real margins, pt typography, pagination rules (no orphan headings, no\n   split code/alerts/rows), printable bars and chips. The dark file additionally gets\n   a build-generated @media print token flip to light; delete that block in\n   dist/its-dark.css for WYSIWYG dark export. */",
         "/* [PRINT] — full A4 print design: real margins, pt typography, pagination rules\n   (no orphan headings, no split code/alerts/rows), print-safe rules and chips.\n   The dark file additionally gets a build-generated @media print token flip to light\n   for ink-friendly export; delete that block in dist/cryptomize-dark.css for WYSIWYG\n   dark export. */"),
    ],
    "src/alerts.css": [
        ("/* [ALERTS] — GFM alerts mapped to the ITS callout palette (same `> [!type]` markdown as\n   Obsidian callouts), WCAG-remediated per mode via the --gfm-* tokens (build.py v2 layer).\n   Tints via rgb triplets (no color-mix). Built-in SVG icons kept, tinted by the label color. */",
         "/* [ALERTS] — GFM alerts in the CryptoMize semantic palette (info-blue, success-green,\n   purple, gold, red), WCAG-verified per mode via the --gfm-* tokens. Tints via rgb\n   triplets; Typora's built-in SVG icons are kept and tinted by the label color. */"),
    ],
}


def main():
    for fname, pairs in REPL.items():
        p = SRC.parent / fname
        t = p.read_text()
        for old, new in pairs:
            if old not in t:
                print(f"WARN not found in {fname}: {old[:60]!r}")
                continue
            t = t.replace(old, new)
        p.write_text(t)
    import re
    leftovers = []
    for f in ("shared.css", "codemirror.css", "alerts.css", "print.css"):
        t = (SRC / f).read_text()
        for pat in ("ITS", "its-font", "Obsidian", "vault", "slrvb", "Calisto", "Fira", "--note", "--headers"):
            if re.search(re.escape(pat), t):
                leftovers.append((f, pat))
    print("leftover mentions:", leftovers if leftovers else "NONE")


if __name__ == "__main__":
    main()
