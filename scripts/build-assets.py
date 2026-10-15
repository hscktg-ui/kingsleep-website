"""Build web assets: official logos (brand-source/), optimized photos, OG image.

Run from the repo root:  python scripts/build-assets.py
Logo sources are the client's transparent files delivered 2026-09-11 (홈페이지자료); they are
cropped and resized only, never redrawn.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand-source"
ASSETS = ROOT / "assets"
IMAGES = ASSETS / "images"

NAVY = (13, 27, 42)
GOLD = (197, 160, 89)
GOLD_LIGHT = (212, 184, 122)
IVORY = (236, 228, 212)


def crop_alpha(im: Image.Image, pad: int = 0) -> Image.Image:
    box = im.getbbox()
    if not box:
        return im
    l, t, r, b = box
    return im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))


def resize_h(im: Image.Image, height: int) -> Image.Image:
    w = round(im.width * height / im.height)
    return im.resize((w, height), Image.Resampling.LANCZOS)


def build_logos() -> None:
    jobs = [
        ("logo-navy-horizontal.png", "logo-ks-navy.webp", 104),
        ("logo-gold-horizontal.png", "logo-ks-gold.webp", 120),
        ("logo-gold-stacked.png", "logo-ks-gold-stacked.webp", 520),
    ]
    for src, dst, height in jobs:
        im = resize_h(crop_alpha(Image.open(SRC / src).convert("RGBA")), height)
        im.save(ASSETS / dst, "WEBP", quality=90, method=6)
        print(f"logo  {dst:28s} {im.width}x{im.height}  {(ASSETS / dst).stat().st_size // 1024}KB")

    # Square-ish PNG for structured data (Google/Naver logo field).
    im = resize_h(crop_alpha(Image.open(SRC / "logo-navy-stacked.png").convert("RGBA"), pad=24), 600)
    im.save(ASSETS / "logo-ks-navy-stacked.png", optimize=True)
    print(f"logo  logo-ks-navy-stacked.png    {im.width}x{im.height}  {(ASSETS / 'logo-ks-navy-stacked.png').stat().st_size // 1024}KB")


def save_jpeg(im: Image.Image, path: Path, quality: int) -> None:
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def build_photos(long_edge: int = 1600) -> None:
    for path in sorted(IMAGES.glob("*.jpg")):
        if path.stem.endswith("-1200"):
            continue
        im = Image.open(path).convert("RGB")
        target = 2000 if path.stem == "hero-bedroom" else long_edge
        if max(im.size) > target:
            scale = target / max(im.size)
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        before = path.stat().st_size
        save_jpeg(im, path, 78 if path.stem != "hero-bedroom" else 76)
        print(f"photo {path.name:28s} {im.width}x{im.height}  {before // 1024}KB -> {path.stat().st_size // 1024}KB")
        if path.stem == "hero-bedroom":
            small = im.resize((1200, round(im.height * 1200 / im.width)), Image.Resampling.LANCZOS)
            save_jpeg(small, IMAGES / "hero-bedroom-1200.jpg", 78)
            print(f"photo hero-bedroom-1200.jpg       {small.width}x{small.height}  {(IMAGES / 'hero-bedroom-1200.jpg').stat().st_size // 1024}KB")


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def build_og() -> None:
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), NAVY)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 5), fill=GOLD)
    draw.rectangle((0, h - 5, w, h), fill=GOLD)

    logo = resize_h(crop_alpha(Image.open(SRC / "logo-gold-stacked.png").convert("RGBA")), 430)
    lx, ly = 110, (h - logo.height) // 2
    img.paste(logo, (lx, ly), logo)

    tx = lx + logo.width + 84
    slogan = font("C:/Windows/Fonts/georgia.ttf", 25)
    tagline = font("C:/Windows/Fonts/NotoSerifCJKkr-Regular.otf", 44)
    sub = font("C:/Windows/Fonts/NotoSansCJKkr-Regular.otf", 26)
    url = font("C:/Windows/Fonts/georgia.ttf", 22)

    draw.text((tx, 196), "PREMIUM COMFORT, ROYAL QUALITY", font=slogan, fill=GOLD_LIGHT)
    draw.line((tx, 246, tx + 470, 246), fill=GOLD, width=2)
    draw.text((tx, 270), "좋은 잠이", font=tagline, fill=IVORY)
    draw.text((tx, 330), "좋은 하루를 만듭니다", font=tagline, fill=IVORY)
    draw.text((tx, 414), "국내 제작 프리미엄 매트리스 · 킹슬립", font=sub, fill=(160, 168, 178))
    draw.text((tx, 470), "kingsleep.co.kr", font=url, fill=GOLD)

    img.save(ASSETS / "og-image.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    print(f"og    og-image.jpg                 {w}x{h}  {(ASSETS / 'og-image.jpg').stat().st_size // 1024}KB")


if __name__ == "__main__":
    build_logos()
    build_photos()
    build_og()
