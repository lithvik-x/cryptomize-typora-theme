#!/usr/bin/env python3
"""Exact OKLCH -> sRGB hex converter (Björn Ottosson's OkLab matrices) for deriving
the CryptoMize Typora theme palette from the brand's oklch design tokens."""
import math
import sys


def oklch_to_srgb(L, C, h_deg, alpha=None):
    h = math.radians(h_deg)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b2 = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def gamma(v):
        v = min(max(v, 0.0), 1.0)
        return 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055

    r8, g8, b8 = round(gamma(r) * 255), round(gamma(g) * 255), round(gamma(b2) * 255)
    if alpha is None:
        return f"#{r8:02x}{g8:02x}{b8:02x}"
    return f"rgba({r8}, {g8}, {b8}, {alpha})"


BRAND = {
    # light mode (from cryptomize.com/src/styles/global.css, .light-equivalent root)
    "background": (0.978, 0.004, 250),
    "foreground": (0.170, 0.020, 262),
    "card": (1, 0, 0),
    "primary": (0.55, 0.235, 27),
    "primary-bright": (0.577, 0.245, 27.325),
    "primary-foreground": (0.990, 0.005, 20),
    "secondary-fg": (0.230, 0.012, 250),
    "muted": (0.955, 0.006, 250),
    "muted-fg": (0.415, 0.022, 260),
    "accent-blush": (0.940, 0.018, 25),
    "border": (0.890, 0.010, 255),
    "sidebar": (0.965, 0.005, 250),
    "info": (0.511, 0.262, 276.966),
    "success": (0.596, 0.145, 163.225),
    "warning": (0.655, 0.162, 81),
    "chart-2-purple": (0.558, 0.288, 302.321),
    "chart-3-sky": (0.715, 0.143, 215.221),
    "chart-4-gold": (0.738, 0.168, 86),
    "chart-5-violet": (0.585, 0.233, 277.117),
    # dark mode
    "dark-background": (0.130, 0.022, 262),
    "dark-foreground": (0.940, 0.008, 250),
    "dark-card": (0.175, 0.030, 262),
    "dark-popover": (0.185, 0.032, 262),
    "dark-secondary": (0.240, 0.032, 262),
    "dark-muted": (0.230, 0.030, 262),
    "dark-muted-fg": (0.690, 0.020, 255),
    "dark-accent": (0.265, 0.038, 262),
    "dark-info": (0.673, 0.182, 276.935),
    "dark-success": (0.765, 0.177, 163.223),
    "dark-warning": (0.798, 0.155, 88),
    "dark-ring": (0.704, 0.191, 22.216),
    "dark-destructive": (0.637, 0.237, 25.331),
}

if __name__ == "__main__":
    for name, (L, C, h) in BRAND.items():
        print(f"{name:22s} oklch({L} {C} {h}) = {oklch_to_srgb(L, C, h)}")
