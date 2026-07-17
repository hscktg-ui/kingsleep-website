"""Generate favicon set, app icons, and social preview image."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent.parent / "assets"
NAVY = (47, 74, 106, 255)
GOLD = (199, 151, 50, 255)
WHITE = (255, 255, 255, 255)


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


def try_font(size: int, bold: bool = False, korean: bool = False) -> ImageFont.ImageFont:
    if korean:
        candidates = [
            "C:/Windows/Fonts/malgun.ttf",
            "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf",
            "C:/Windows/Fonts/NanumGothic.ttf",
            "C:/Windows/Fonts/gulim.ttc",
        ]
    elif bold:
        candidates = [
            "C:/Windows/Fonts/georgiab.ttf",
            "C:/Windows/Fonts/timesbd.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/georgia.ttf",
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_og_image() -> Image.Image:
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), NAVY[:3])
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, w, 6), fill=GOLD[:3])
    draw.rectangle((0, h - 6, w, h), fill=GOLD[:3])

    mark = fit_mark(load_mark(gold=True), 280, pad_ratio=0.06)
    mark_x, mark_y = 96, (h - mark.height) // 2 - 10
    img.paste(mark, (mark_x, mark_y), mark)

    text_x = mark_x + mark.width + 48
    title_font = try_font(72, bold=True)
    slogan_font = try_font(26)
    tag_font = try_font(28, korean=True)

    draw.text((text_x, h // 2 - 86), "KING SLEEP", font=title_font, fill=GOLD[:3])
    draw.text(
        (text_x, h // 2 - 4),
        "PREMIUM COMFORT, ROYAL QUALITY",
        font=slogan_font,
        fill=(220, 210, 190),
    )
    draw.line((text_x, h // 2 + 42, text_x + 420, h // 2 + 42), fill=GOLD[:3], width=2)
    draw.ellipse((text_x + 204, h // 2 + 36, text_x + 216, h // 2 + 48), fill=GOLD[:3])
    draw.text(
        (text_x, h // 2 + 60),
        "좋은 잠이 좋은 하루를 만듭니다",
        font=tag_font,
        fill=(230, 220, 200),
    )
    return img


def save_png(im: Image.Image, name: str) -> None:
    path = ASSETS / name
    im.save(path, optimize=True)
    print(f"saved {name} {im.size}")


def main() -> None:
    # Browser favicons (transparent mark works on light tabs)
    fav16 = icon_transparent(16, gold=False)
    fav32 = icon_transparent(32, gold=False)
    fav48 = icon_transparent(48, gold=False)
    save_png(fav16, "favicon-16x16.png")
    save_png(fav32, "favicon-32x32.png")

    # ICO multi-size
    ico_path = ASSETS / "favicon.ico"
    fav48.save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    print(f"saved favicon.ico")

    # Apple / Android (navy rounded tile + gold mark)
    save_png(icon_on_navy(180, radius_ratio=0.22), "apple-touch-icon.png")
    save_png(icon_on_navy(192, radius_ratio=0.22), "android-chrome-192x192.png")
    save_png(icon_on_navy(512, radius_ratio=0.22), "android-chrome-512x512.png")

    # Social preview
    og = make_og_image()
    og_path = ASSETS / "og-image.jpg"
    og.save(og_path, quality=92, optimize=True)
    print(f"saved og-image.jpg {og.size}")

    # Web manifest
    manifest = ASSETS.parent / "site.webmanifest"
    manifest.write_text(
        """{
  "name": "KING SLEEP",
  "short_name": "KING SLEEP",
  "description": "프리미엄 수면 가구 — 좋은 잠이 좋은 하루를 만듭니다",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#2F4A6A",
  "theme_color": "#2F4A6A",
  "lang": "ko",
  "icons": [
    {
      "src": "assets/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "assets/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
""",
        encoding="utf-8",
    )
    print("saved site.webmanifest")
    print("done")


if __name__ == "__main__":
    main()
