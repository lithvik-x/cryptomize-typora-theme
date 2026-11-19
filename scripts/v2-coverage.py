#!/usr/bin/env python3
"""V2 coverage gate: every CONTRACT.md selector family + native var present in BOTH dist files.
Substring presence check (structural, not computed-style) — the visual harness (V5) and the
owner in-app check (C2/C3) carry the semantic verification."""
import re
import sys
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"

NATIVE_VARS = [
    "--bg-color", "--side-bar-bg-color", "--text-color", "--primary-color",
    "--primary-btn-border-color", "--primary-btn-text-color", "--active-file-bg-color",
    "--active-file-text-color", "--active-file-border-color", "--item-hover-bg-color",
    "--item-hover-text-color", "--control-text-color", "--control-text-hover-color",
    "--select-text-bg-color", "--select-text-font-color", "--search-select-bg-color",
    "--search-select-text-color", "--md-char-color", "--meta-content-color",
    "--heading-char-color", "--blur-text-color", "--drag-placeholder-color",
    "--table-border-color", "--panel-border-color", "--rawblock-edit-panel-bd",
    "--color-popover-bg-color", "--focus-ring-color", "--active-toggle-btn-color",
    "--side-bar-menu-active-tint", "--monospace", "--window-border",
]

SELECTORS = [
    "html", "body", "content", "#write",
    "#write h1", "#write h6", "#write h1::after",
    "#write a", "#write strong", "#write mark",
    "#write code", "#write kbd",
    "pre.md-fences", ".md-fences.mock-cm", "fences-no-line-wrapping",
    ":is(#write, #typora-source) .cm-keyword", ".cm-s-inner",
    ".cm-s-typora-default", ".CodeMirror-gutters", ".CodeMirror-cursor",
    ".code-tooltip",
    "#write blockquote", "#write table", "#write table th", "#write table td",
    "nth-child(2n)", ".md-grid-board", ".md-table-resize",
    ".task-list-item input", ":checked",
    "#write hr", "div.hr",
    "sup.md-footnote", ".footnotes", ".md-def-footnote",
    ".md-toc", ".md-toc-item",
    "pre.md-meta-block",
    ".md-math-container", "mjx-container",
    "#write img",
    ".md-alert", ".md-alert-note", ".md-alert-tip", ".md-alert-important",
    ".md-alert-warning", ".md-alert-caution", ".md-alert-text",
    ".md-hover-tip", ".md-comment", ".md-meta",
    "#top-titlebar", "#typora-sidebar", "#file-library", ".file-node-content",
    ".file-library-node.active", ".sidebar-tabs",
    ".outline-content", ".outline-item", ".outline-item-active",
    "#md-searchpanel", "#typora-quick-open", "#ty-autosuggest",
    "footer.ty-footer", "#footer-word-count-info",
    "#megamenu-content", "#megamenu-menu-sidebar", ".megamenu-menu-list",
    ".dropdown-menu", ".context-menu",
    ".modal-content", ".modal-backdrop",
    ".btn-default", ".btn-primary",
    ".ty-tooltip", ".ty-popover", "#md-notification",
    "::-webkit-scrollbar", "::-webkit-scrollbar-thumb",
    "@media print", "typora-export", "print-color-adjust",
    ".on-focus-mode",
]

DARK_ONLY = [":root", "@media print"]  # sanity: both files must have :root; dark must have print-flip
LIGHT_MARKER = "--paper: #f6f8fa"
DARK_MARKER = "--paper: #040710"


def main():
    ok = True
    texts = {}
    for name in ("cryptomize.css", "cryptomize-dark.css"):
        texts[name] = (DIST / name).read_text()
    for name, text in texts.items():
        missing = [v for v in NATIVE_VARS if f"{v}:" not in text]
        miss_sel = [s for s in SELECTORS if s not in text]
        mode_marker_ok = LIGHT_MARKER in texts["cryptomize.css"] and DARK_MARKER in texts["cryptomize-dark.css"]
        print(f"V2 [{name}]: vars {len(NATIVE_VARS) - len(missing)}/{len(NATIVE_VARS)}, selectors {len(SELECTORS) - len(miss_sel)}/{len(SELECTORS)}")
        for m in missing:
            print(f"  MISSING VAR: {m}")
            ok = False
        for s in miss_sel:
            print(f"  MISSING SELECTOR: {s}")
            ok = False
        if not mode_marker_ok:
            print("  MISSING mode palette marker")
            ok = False
    print("V2:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
