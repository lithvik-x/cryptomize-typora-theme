# Changelog

## 1.0.0 — 2026-11-20

Initial release.

- CryptoMize brand palette in light and dark modes, derived from the cryptomize.com design tokens (oklch → sRGB, exact conversion).
- Rajdhani typography across text, headings, UI, and code; weights 400/500/600/700 bundled (SIL OFL).
- Brand system: 0.75rem radius scale, layered soft shadows, red glow, ease-smooth motion, solid-red selection, pill scrollbar, focus rings, ambient paper wash.
- Full-width flow with opt-in `--file-line-width` cap.
- WCAG AA verified across all painted pairs (34 × 2 modes, scripted audit).
- Markdown coverage: headings with descending rules, links with masked-SVG external mark, inline-code chips, kbd keycaps, editorial blockquotes, glyphed rules, lists, round checkboxes with done states, rounded tables with banded headers, footnotes, boxed TOC, front matter, math, images, GFM alerts in the brand semantic palette.
- Code: three-surface CodeMirror coverage (fence/mock-cm/source) with brand syntax palette and language chips.
- Chrome: sidebar/outline/footer/menus/megamenu/modals/tooltips/search/scrollbars.
- Print/PDF: A4 design with pagination rules; dark export flips to light.
