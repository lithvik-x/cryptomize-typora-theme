# CryptoMize Typora Theme — brand provenance

Every design decision in this theme traces to the CryptoMize brand design system as implemented on **cryptomize.com** (canonical repo `~/Projects/forge/cryptomize.com/`, branch `forge`, `src/styles/global.css` + site components). Nothing is borrowed from third-party themes.

## Extraction map

| Theme element | Brand source (cryptomize.com) |
|---|---|
| Red primary `#d9000b` (headings, markers, table bands, selection) | `--primary oklch(0.55 0.235 27)` — the site's WCAG-tuned primary (5.17:1 with white) |
| Bright reds (dark-mode accents, hover glow) | `--ring oklch(0.704 0.191 22.2)` / `--destructive oklch(0.637 0.237 25.3)` |
| Blue links `#4f39f6` light / `#7c86ff` dark | `--info` semantic token, both modes |
| Paper/ink neutrals | `--background`/`--foreground` (Obsidian primitive family, both modes) |
| Panel/surface/frame tones | `--card`, `--muted`, `--secondary`, `--sidebar` per mode |
| GFM alert palette | `--info`, `--success`, chart-2 purple, `--warning` gold, `--primary` red |
| Syntax palette | Brand vivid set (purple/green/red/cyan/blue/gold/violet chart + semantic tokens), WCAG-adjusted in-hue on the code surface |
| Ambient paper wash | `body::before` ambient radial gradients (red/purple/cyan), tuned down for a reading surface |
| Radius scale (0.75rem base, 0.6×–1.8×) | `--radius` + the site's multiplier scale |
| Soft layered shadows + red glow | `--shadow-sm/md/lg`, `--shadow-glow-red` |
| Motion (`cubic-bezier(0.22,1,0.36,1)`, 200ms) | `--ease-smooth`, `--duration-fast` |
| Typography: Rajdhani everywhere | The site's font law ("Rajdhani everywhere, for everything; mono and serif axes neutralized") |
| Headings 600 / −0.01em / 1.12 leading | Site `h1–h6` base styles |
| Body 1.65 leading / 0.008em tracking | Site `body` base styles |
| Solid-red selection with light text | Site `::selection` |
| Pill scrollbar, hairline thumb, red hover | Site scrollbar recipe |
| Focus ring 2px + 2px offset | Site `:focus-visible` |
| Mono grammar (uppercase micro-labels, wide tracking, tabular-nums) | The site's codified mono-as-treatment law |
| Masked-SVG external-link mark, HR diamond | Original work in the brand idiom (no font assets) |

## Conversion + verification tooling

- `scripts/oklch.py` — exact OKLab→sRGB conversion of the brand's oklch tokens (Björn Ottosson matrices)
- `scripts/gen-tokens.py` — emits `src/tokens/{light,dark}.css` from those anchors with in-hue WCAG lightness adjustment; the generator is the source of truth for every color
- `scripts/wcag-audit.py` — computes contrast ratios for every painted pair (34 pairs × 2 modes); CI-style gate, all PASS at AA (4.5:1 body, 3:1 large/UI)
- `scripts/harness.py` (Chromium parse + screenshots), `scripts/pdf-check.py` (print/PDF render), `scripts/v2-coverage.py` (selector/var contract)
