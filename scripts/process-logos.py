"""Regenerate transparent King Sleep logo assets with clean crops."""
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def color_dist(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])) ** 0.5


def flood_remove_bg(im: Image.Image, threshold: float = 42) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    visited = [[False] * w for _ in range(h)]
    q: deque[tuple[int, int]] = deque()

    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))

    samples = [
        im.getpixel((2, 2))[:3],
        im.getpixel((w // 2, 2))[:3],
        im.getpixel((w - 3, 2))[:3],
        im.getpixel((2, h // 2))[:3],
        im.getpixel((w - 3, h // 2))[:3],
    ]
    bg = tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))

    while q:
        x, y = q.popleft()
        if x < 0 or x >= w or y < 0 or y >= h or visited[y][x]:
            continue
        visited[y][x] = True
        r, g, b, a = px[x, y]
        if color_dist((r, g, b), bg) <= threshold:
            px[x, y] = (r, g, b, 0)
            q.append((x + 1, y))
            q.append((x - 1, y))
            q.append((x, y + 1))
            q.append((x, y - 1))
    return im


def soften_alpha(im: Image.Image, radius: float = 0.8) -> Image.Image:
    alpha = im.split()[3].filter(ImageFilter.GaussianBlur(radius))
    out = im.copy()
    out.putalpha(alpha)
    return out


def content_bbox(im: Image.Image, alpha_min: int = 12):
    px = im.load()
    w, h = im.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] >= alpha_min:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def trim_alpha(im: Image.Image, pad: int = 24) -> Image.Image:
    bbox = content_bbox(im)
    if not bbox:
        return im
    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(im.width, right + pad)
    bottom = min(im.height, bottom + pad)
    return im.crop((left, top, right, bottom))


def square_pad(im: Image.Image, pad_ratio: float = 0.12) -> Image.Image:
    im = trim_alpha(im, pad=0)
    w, h = im.size
    side = int(max(w, h) * (1 + pad_ratio * 2))
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2), im)
    return canvas


def extract_icon(full: Image.Image) -> Image.Image:
    """
    Isolate the moon/crown/Z emblem above the KING SLEEP wordmark.
    Strategy: take the upper band of opaque content and stop before the wordmark row.
    """
    bbox = content_bbox(full)
    if not bbox:
        return full
    left, top, right, bottom = bbox
    band = full.crop((left, top, right, bottom))
    bw, bh = band.size

    # Scan rows: icon occupies top ~42% of the stacked logo content height.
    # Cut before the large serif wordmark (wide dense horizontal band).
    px = band.load()
    row_density = []
    for y in range(bh):
        count = sum(1 for x in range(bw) if px[x, y][3] > 20)
        row_density.append(count / bw)

    # Icon sits above a clear sparse gap before the KING SLEEP wordmark (~y 510–555).
    cut_y = int(bh * 0.58)
    search_start = int(bh * 0.40)
    search_end = int(bh * 0.70)
    gap = None
    for y in range(search_start, search_end):
        if row_density[y] < 0.02:
            y2 = y
            while y2 < search_end and row_density[y2] < 0.04:
                y2 += 1
            if y2 - y >= 6:
                gap = (y + y2) // 2
                break
    if gap is not None:
        cut_y = gap

    icon = band.crop((0, 0, bw, cut_y))
    return trim_alpha(icon, pad=4)


def save_rgba(im: Image.Image, name: str) -> None:
    path = ASSETS / name
    im.save(path, optimize=True)
    print(f"saved {name} {im.size}")


def preview(stem: str, im: Image.Image) -> None:
    for bgname, color in [("white", (255, 255, 255, 255)), ("navy", (10, 28, 58, 255))]:
        bg = Image.new("RGBA", im.size, color)
        Image.alpha_composite(bg, im.convert("RGBA")).convert("RGB").save(
            ASSETS / f"_prev_{stem}_{bgname}.jpg", quality=92
        )


def main() -> None:
    light_src = Image.open(ASSETS / "logo.png").convert("RGBA")
    dark_src = Image.open(ASSETS / "logo-dark.png").convert("RGBA")

    logo_light = soften_alpha(flood_remove_bg(light_src, threshold=38), 0.6)
    logo_gold = soften_alpha(flood_remove_bg(dark_src, threshold=58), 0.6)

    logo_light_trim = trim_alpha(logo_light, pad=40)
    logo_gold_trim = trim_alpha(logo_gold, pad=40)
    save_rgba(logo_light_trim, "logo-light.png")
    save_rgba(logo_gold_trim, "logo-gold.png")

    # Compact: icon + wordmark + english slogan (exclude Korean line roughly)
    for src, name in [(logo_light_trim, "logo-compact.png")]:
        bw, bh = src.size
        # Cut near bottom Korean line — keep ~78% height
        compact = trim_alpha(src.crop((0, 0, bw, int(bh * 0.78))), pad=16)
        save_rgba(compact, name)

    mark = square_pad(extract_icon(logo_light), pad_ratio=0.14)
    mark_gold = square_pad(extract_icon(logo_gold), pad_ratio=0.14)
    mark = mark.resize((640, 640), Image.Resampling.LANCZOS)
    mark_gold = mark_gold.resize((640, 640), Image.Resampling.LANCZOS)
    save_rgba(mark, "logo-mark.png")
    save_rgba(mark_gold, "logo-mark-gold.png")

    preview("logo-mark", mark)
    preview("logo-mark-gold", mark_gold)
    preview("logo-light", logo_light_trim)
    preview("logo-gold", logo_gold_trim)
    print("done")


if __name__ == "__main__":
    main()
