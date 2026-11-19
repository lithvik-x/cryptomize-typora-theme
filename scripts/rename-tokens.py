#!/usr/bin/env python3
"""One-time transform: port the authored section CSS into the CryptoMize clean-room
vocabulary — ITS-ish variable names -> brand-neutral names, Obsidian spacing scale ->
literal px, ITS icon-font glyph usages -> original CSS/SVG treatments."""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"

# old name -> new name (or literal replacement handled below)
RENAME = {
    "--note": "--paper",
    "--surface-old-bg": "--surface",  # (guard, see literal map for --bg)
    "--outer-bar": "--frame",
    "--dark-sidebar": "--panel",
    "--embed-bg": "--panel",
    "--text-dl": "--on-brand",
    "--soft-text": "--ink-soft",
    "--faint-text": "--ink-faint",
    "--headers": "--heading",
    "--lite-accent": "--brand-bright",
    "--dark-accent": "--brand-deep",
    "--accent2-lite": "--link",
    "--accent-color": "--brand-rgb",
    "--ui-marker": "--marker",
    "--latex-color": "--math",
    "--code-text": "--code-ink",
    "--code-normal": "--code-ink",
    "--code-background": "--code-bg",
    "--code-shadow": "--code-shadow",
    "--lines": "--edge",
    "--table": "--grid",
    "--th-text": "--th-ink",
    "--td": "--row-tint",
    "--th": "--th-band",
    "--hr": "--rule",
    "--highlight": "--selection",
    "--hvr-active": "--hover-bg",
    "--hvr": "--mark-bg",
    "--footnote": "--ink-soft",
    "--inactive": "--ink-dim",
    "--list-marker-color": "--marker",
    "--list-numbered-color": "--heading",
    "--text-highlight-bg": "--mark-bg",
    "--link-color-hover": "--link-hover",
    "--link-color": "--link",
    "--blockquote-border-thickness": "--quote-bar",
    "--blockquote-color": "--ink",
}

# var(--x) -> literal (Obsidian spacing scale, ITS radii, ITS-only knobs)
LITERALS = {
    "--bg": "var(--surface)",          # frame/surface fill
    "--text": "var(--ink)",
    "--accent": "var(--brand)",
    "--size-4-1": "4px",
    "--size-4-2": "8px",
    "--size-4-3": "12px",
    "--size-4-4": "16px",
    "--size-4-6": "24px",
    "--size-2-2": "4px",
    "--radius-s": "0px",
    "--radius-m": "0px",
    "--radius-h": "0px",
    "--checkbox-radius": "0px",
    "--image-radius": "0px",
    "--checkbox-size": "1em",
    "--checkbox-border-color": "var(--marker)",
    "--table-header-weight": "700",
    "--table-header-color": "var(--th-ink)",
    "--table-header-background": "var(--th-band)",
    "--table-header-background-hover": "var(--brand-deep)",
    "--table-header-padding-y": "6px",
    "--table-header-padding-x": "10px",
    "--table-cell-padding-y": "6px",
    "--table-cell-padding-x": "10px",
    "--table-row-alt-background": "var(--row-tint)",
    "--table-row-background-hover": "var(--hover-bg)",
    "--table-row-alt-background-hover": "var(--hover-bg)",
    "--table-border-color": "var(--grid)",
    "--table-header-text-color": "var(--link)",
    "--header-weight": "700",
    "--line-height-tight": "1.3",
    "--heading-spacing-top": "10px",
    "--heading-spacing-bottom": "10px",
    "--bold-weight": "700",  # Rajdhani tops at 700
    "--bold-color": "inherit",
    "--italic-color": "inherit",
    "--blockquote-background-color": "transparent",
    "--blockquote-border-color": "var(--marker)",
    "--blockquote-font-style": "inherit",
    "--blockquote-padding": "4px 0 4px 16px",
    "--hr-thickness": "2px",
    "--hr-color": "var(--rule)",
    "--list-indent": "25px",
    "--list-spacing": "2px",
    "--root-list-spacing": "10px",
    "--font-smallest": "0.85em",
    "--font-text-size": "1em",
    "--shadow-s": "2px 2px 0 var(--edge-strong)",
    "--shadow-m": "3px 3px 0 var(--edge-strong)",
    "--box-border-s": "1px solid var(--edge-strong)",
    "--box-border": "2px solid var(--edge-strong)",
    "--scroll-size": "10px",
    "--input-bg": "var(--surface)",
    "--bttn": "var(--brand-deep)",
    "--drop-shadow": "var(--edge-strong)",
    "--collapse-icon-color": "var(--ink-faint)",
    "--search-select-bg-color": "var(--mark-bg)",
    "--search-select-text-color": "var(--on-brand)",
    "--item-hover-text-color": "var(--ink)",
    "--control-text-hover-color": "var(--ink)",
    "--primary-color": "var(--brand)",
    "--primary-btn-border-color": "var(--brand)",
    "--primary-btn-text-color": "var(--on-brand)",
    "--active-file-bg-color": "rgba(var(--brand-rgb), 0.18)",
    "--active-file-text-color": "var(--ink)",
    "--active-file-border-color": "var(--marker)",
    "--active-toggle-btn-color": "var(--brand)",
    "--focus-ring-color": "var(--marker)",
    "--side-bar-menu-active-tint": "var(--brand-deep)",
    "--item-hover-bg-color": "var(--hover-bg)",
    "--md-char-color": "var(--ink-faint)",
    "--meta-content-color": "var(--ink-soft)",
    "--heading-char-color": "var(--ink-faint)",
    "--blur-text-color": "var(--ink-faint)",
    "--drag-placeholder-color": "var(--hover-bg)",
    "--panel-border-color": "var(--edge)",
    "--rawblock-edit-panel-bd": "var(--code-bg)",
    "--color-popover-bg-color": "var(--panel)",
    "--side-bar-bg-color": "var(--frame)",
    "--bg-color": "var(--frame)",
    "--text-color": "var(--ink)",
    "--select-text-bg-color": "var(--selection)",
    "--select-text-font-color": "inherit",
    "--window-border": "1px solid var(--edge-strong)",
    "--file-line-width": "none",
    "--font-default": "var(--font-body)",
    "--its": "REMOVED-ITS-FONT",
}

GLYPH_BLOCKS = [
    # (old block fragment, replacement)
    (
        """#write a::after {
  content: "\\e809";
  font-family: var(--its);
  padding-left: 2px;
  display: inline-block;
  opacity: 0.5;
  font-weight: 100 !important;
  font-style: normal !important;
}""",
        """#write a::after {
  content: "";
  display: inline-block;
  width: 0.6em;
  height: 0.6em;
  margin-left: 2px;
  vertical-align: 0.05em;
  background-color: currentColor;
  opacity: 0.6;
  -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4.5 11.5 L11 5 M6 4.2 h5.3 v5.3' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='square'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4.5 11.5 L11 5 M6 4.2 h5.3 v5.3' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='square'/%3E%3C/svg%3E");
  -webkit-mask-size: contain;
  mask-size: contain;
}""",
    ),
    (
        """#write hr::after, #write div.hr::after {
  content: var(--hr-icon-symbol);
  font-family: var(--hr-icon-font);
  font-size: var(--font-text-size);
  display: inline-block;
  position: absolute;
  left: 50%;
  top: 0;
  transform: translate(-50%, -50%);
  color: transparent;
  text-shadow: 0 0 0 var(--hr-icon-color);
  padding: 0 var(--hr-icon-padding-x);
  background-color: var(--note);
  line-height: 1;
}""",
        """#write hr::after, #write div.hr::after {
  content: "";
  display: inline-block;
  position: absolute;
  left: 50%;
  top: 0;
  width: 8px;
  height: 8px;
  transform: translate(-50%, -50%) rotate(45deg);
  background: var(--marker);
}""",
    ),
    (
        """#write ul > li::marker {
  color: var(--ui-marker);
  font-family: var(--its);
  font-weight: 100;
}""",
        """#write ul > li::marker {
  color: var(--marker);
}""",
    ),
]


def transform(text: str, fname: str) -> str:
    for old, new in GLYPH_BLOCKS:
        if old in text:
            text = text.replace(old, new)
    # order matters: longest names first to avoid prefix collisions
    names = sorted(set(RENAME) | set(LITERALS), key=len, reverse=True)
    for name in names:
        if name in RENAME:
            new = RENAME[name]
            text = re.sub(re.escape(f"var({name})"), f"var({new})", text)
            text = re.sub(re.escape(f"{name}: "), f"{new}: ", text)  # definitions in mapping blocks
        else:
            lit = LITERALS[name]
            text = re.sub(re.escape(f"var({name})"), lit, text)
    # drop declarations that defined literal-mapped vars (now dead) inside :root mapping
    return text


def main():
    for f in ("shared.css", "codemirror.css", "alerts.css", "print.css"):
        p = SRC / f
        t = p.read_text()
        t = transform(t, f)
        p.write_text(t)
    # verify: no ITS-era names, no its-font references remain
    bad = []
    for f in ("shared.css", "codemirror.css", "alerts.css", "print.css"):
        t = (SRC / f).read_text()
        for pat in ("--its", "REMOVED-ITS-FONT", "--note", "--outer-bar", "--embed-bg", "--text-dl",
                    "--soft-text", "--faint-text", "--headers", "--ui-marker", "--latex-color",
                    "--size-4-", "--size-2-2", "--accent2", "--hr-icon", "--text-normal"):
            if pat in t:
                bad.append((f, pat))
    print("remaining old-vocabulary refs:", bad if bad else "NONE")
    # list every var() the sections now use -> tokens files must define these
    used = set()
    for f in ("shared.css", "codemirror.css", "alerts.css", "print.css"):
        used |= set(re.findall(r"var\((--[A-Za-z0-9_-]+)", (SRC / f).read_text()))
    used -= {"--font-body"}  # defined in tokens as alias
    print(f"{len(used)} distinct vars used:")
    for v in sorted(used):
        print("   ", v)


if __name__ == "__main__":
    main()
