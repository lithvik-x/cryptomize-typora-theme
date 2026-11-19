#!/usr/bin/env python3
"""WCAG contrast audit for the ITS Typora themes.

Computes the contrast ratio for every fg/bg pair the themes actually paint, using the
RESOLVED values from each dist file (vars resolved via the extraction in build.py).
AA thresholds: 4.5:1 for body-size text, 3:1 for large text (>=24px, or >=18.66px bold —
all ITS headings at 700 qualify). The v2 overrides land in src/shared.css; this audit
is the acceptance gate for them.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def srgb_to_lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 * 255.0 / 255.0 and c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_or_rgb):
    if isinstance(hex_or_rgb, str):
        h = hex_or_rgb.strip().lstrip("#")
        if len(h) == 3:
            h = "".join(x * 2 for x in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    else:
        r, g, b = hex_or_rgb
    def lin(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def parse_color(v, tokens, depth=0):
    """Resolve a token value to an rgb triple or hex string, following var() chains."""
    if depth > 8:
        return None
    v = v.strip()
    if v.startswith("var("):
        name = re.match(r"var\((--[A-Za-z0-9_-]+)", v).group(1)
        if name not in tokens:
            return None
        return parse_color(tokens[name], tokens, depth + 1)
    if v.startswith("#"):
        return v
    m = re.match(r"rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)", v)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"rgba?\(\s*var\((--[A-Za-z0-9_-]+)\)", v)
    if m and m.group(1) in tokens:
        trip = tokens[m.group(1)]
        mm = re.match(r"^\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)", trip)
        if mm:
            return (int(mm.group(1)), int(mm.group(2)), int(mm.group(3)))
    return None


def blend(fg, bg, alpha):
    """Composite an rgba fg over bg -> solid rgb."""
    if isinstance(fg, str):
        h = fg.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    else:
        r, g, b = fg
    if isinstance(bg, str):
        h = bg.lstrip("#")
        br, bg_, bb = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    else:
        br, bg_, bb = bg
    return (round(r * alpha + br * (1 - alpha)), round(g * alpha + bg_ * (1 - alpha)), round(b * alpha + bb * (1 - alpha)))


def extract_alpha(v, tokens):
    m = re.match(r"^rgba?\([^)]*?,\s*([\d.]+)\)\s*$", v.strip()) if not v.strip().startswith("var") else None
    return float(m.group(1)) if m else None


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def get_tokens(css_text):
    """First-wins token map: the file's opening :root block is the mode's real palette
    (the dark file's LAST :root is the print-flip light block — must not win)."""
    toks = {}
    m = re.search(r":root\s*\{([^}]*)\}", css_text)
    if m:
        for name, value in re.findall(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;]+);", m.group(1)):
            toks[name] = value.strip()
    # overlay any later non-@media :root blocks (mapped-token sections come after)
    idx = css_text.find("@media print")
    scope = css_text[: idx if idx > 0 else len(css_text)]
    for m in re.finditer(r":root\s*\{([^}]*)\}", scope):
        for name, value in re.findall(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;]+);", m.group(1)):
            toks[name] = value.strip()
    return toks


# pairs: (label, fg-token, bg-token, threshold)
PAIRS = [
    ("body text", "--ink", "--paper", 4.5),
    ("soft text (TOC/footnote/UI)", "--ink-soft", "--paper", 4.5),
    ("faint text (ghost syntax)", "--ink-faint", "--paper", 4.5),
    ("headings", "--heading", "--paper", 3.0),
    ("links", "--link", "--paper", 4.5),
    ("links hover", "--link-hover", "--paper", 4.5),
    ("inline code text", "--code-ink", "--code-bg", 4.5),
    ("code block base", "--ink", "--code-bg", 4.5),
    ("table header text", "--th-ink", "--th-band", 4.5),
    ("blockquote text", "--ink", "--paper", 4.5),
    ("footnote text", "--ink-soft", "--paper", 4.5),
    ("front matter text", "--ink-soft", "--panel", 4.5),
    ("marker (bullets/checkbox)", "--marker", "--paper", 3.0),
    ("brand accent (UI)", "--brand", "--paper", 3.0),
    ("numbered list marker", "--heading", "--paper", 3.0),
    ("math", "--math", "--paper", 4.5),
    ("on-brand text (buttons/band)", "--on-brand", "--brand", 4.5),
    ("sidebar text", "--ink-soft", "--frame", 4.5),
    ("control text (menus)", "--ink-soft", "--panel", 4.5),
    ("alert note label", "--gfm-note", "--panel", 4.5),
    ("alert tip label", "--gfm-tip", "--panel", 4.5),
    ("alert important label", "--gfm-important", "--panel", 4.5),
    ("alert warning label", "--gfm-warning", "--panel", 4.5),
    ("alert caution label", "--gfm-caution", "--panel", 4.5),
    ("cm keyword", "--cm-keyword", "--code-bg", 4.5),
    ("cm string", "--cm-string", "--code-bg", 4.5),
    ("cm tag", "--cm-tag", "--code-bg", 4.5),
    ("cm property", "--cm-property", "--code-bg", 4.5),
    ("cm atom", "--cm-atom", "--code-bg", 4.5),
    ("cm number", "--cm-number", "--code-bg", 4.5),
    ("cm builtin", "--cm-builtin", "--code-bg", 4.5),
    ("cm def", "--cm-def", "--code-bg", 4.5),
]


def main():
    ok = True
    for fname in ("cryptomize.css", "cryptomize-dark.css"):
        text = (DIST / fname).read_text()
        toks = get_tokens(text)
        fails = []
        print(f"\n=== {fname} ===")
        for label, fg, bg, thr in PAIRS:
            fgv = fg if fg.startswith("#") else toks.get(fg)
            bgv = bg if bg.startswith("#") else toks.get(bg)
            if fgv is None or bgv is None:
                print(f"  SKIP {label}: token missing ({fg}/{bg})")
                continue
            fr = parse_color(fgv, toks)
            br = parse_color(bgv, toks)
            if fr is None or br is None:
                print(f"  SKIP {label}: unparseable ({fgv} / {bgv})")
                continue
            # composite alpha fg over bg
            alpha = extract_alpha(fgv, toks) if not isinstance(fgv, str) or fgv.startswith("rgba") else None
            if isinstance(fgv, str) and re.match(r"^rgba?\(\s*\d", fgv):
                m = re.match(r"^rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)[,\s/]+([\d.]+)", fgv)
                if m:
                    fr = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
                    alpha = float(m.group(4))
            if alpha is not None:
                fr = blend(fr, br, alpha)
            r = ratio(fr, br)
            status = "PASS" if r >= thr else "FAIL"
            if status == "FAIL":
                ok = False
                fails.append(label)
            print(f"  {status} {label}: {r:.2f}:1 (need {thr}:1)  [{str(fr)} on {str(br)}]")
    print("\nWCAG:", "PASS" if ok else "FAIL — " + ", ".join(fails))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
