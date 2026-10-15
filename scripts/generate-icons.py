"""Generate favicon set and app icons from the flat logo mark.

The social preview image (og-image.jpg) is built by build-assets.py; the manifest is edited by hand.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parent.parent / "assets"
NAVY = (13, 27, 42, 255)


def load_mark(gold: bool = False) -> Image.Image:
    name = "logo-mark-gold.png" if gold else "logo-mark.png"
    return Image.open(ASSETS / name).convert("RGBA")


def fit_mark(mark: Image.Image, box: int, pad_ratio: float = 0.14) -> Image.Image:
    """Scale mark to fit inside box with padding, keep aspect."""
    inner = int(box * (1 - pad_ratio * 2))
    w, h = mark.size
    scale = min(inner / w, inner / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    return mark.resize((nw, nh), Image.Resampling.LANCZOS)


def icon_on_navy(size: int, radius_ratio: float = 0.22, gold: bool = True) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    r = int(size * radius_ratio)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=NAVY)
    mark = fit_mark(load_mark(gold=gold), size, pad_ratio=0.16)
    x = (size - mark.width) // 2
    y = (size - mark.height) // 2
    canvas.alpha_composite(mark, (x, y))
    return canvas


def icon_transparent(size: int, gold: bool = False) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mark = fit_mark(load_mark(gold=gold), size, pad_ratio=0.08)
    x = (size - mark.width) // 2
    y = (size - mark.height) // 2
    canvas.alpha_composite(mark, (x, y))
    return canvas


def save_png(im: Image.Image, name: str) -> None:
    path = ASSETS / name
    im.save(path, optimize=True)
    print(f"saved {name} {im.size}")


def main() -> None:
    # Browser favicons (transparent mark works on light tabs)
    save_png(icon_transparent(16, gold=False), "favicon-16x16.png")
    save_png(icon_transparent(32, gold=False), "favicon-32x32.png")
    icon_transparent(48, gold=False).save(ASSETS / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("saved favicon.ico")

    # Apple / Android (navy rounded tile + gold mark)
    save_png(icon_on_navy(180, radius_ratio=0.22), "apple-touch-icon.png")
    save_png(icon_on_navy(192, radius_ratio=0.22), "android-chrome-192x192.png")
    save_png(icon_on_navy(512, radius_ratio=0.22), "android-chrome-512x512.png")
    print("done")


if __name__ == "__main__":
    main()
