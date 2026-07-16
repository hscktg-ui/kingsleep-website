from PIL import Image, ImageFilter
import os
from collections import deque

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")


def color_dist(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])) ** 0.5


def flood_remove_bg(im, threshold=48):
    """Remove background connected to image edges by color distance."""
    px = im.load()
    w, h = im.size
    visited = [[False] * w for _ in range(h)]
    q = deque()

    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))

    corner = im.getpixel((0, 0))[:3]

    while q:
        x, y = q.popleft()
        if x < 0 or x >= w or y < 0 or y >= h or visited[y][x]:
            continue
        visited[y][x] = True
        r, g, b, a = px[x, y]
        if color_dist((r, g, b), corner) <= threshold:
            px[x, y] = (r, g, b, 0)
            q.append((x + 1, y))
            q.append((x - 1, y))
            q.append((x, y + 1))
            q.append((x, y - 1))

    return im


def soften_alpha(im, radius=1):
    alpha = im.split()[3]
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius))
    im.putalpha(alpha)
    return im


def main():
    # Light logo: flood from white corners
    light_src = Image.open(os.path.join(ASSETS, "logo.png")).convert("RGBA")
    logo_light = flood_remove_bg(light_src.copy(), threshold=36)
    logo_light.save(os.path.join(ASSETS, "logo-light.png"), optimize=True)

    # Gold logo: flood from navy corners
    gold_src = Image.open(os.path.join(ASSETS, "logo-dark.png")).convert("RGBA")
    logo_gold = flood_remove_bg(gold_src.copy(), threshold=52)
    logo_gold = soften_alpha(logo_gold, radius=0.6)
    logo_gold.save(os.path.join(ASSETS, "logo-gold.png"), optimize=True)

    w, h = logo_light.size
    mark = logo_light.crop((int(w * 0.28), int(h * 0.02), int(w * 0.72), int(h * 0.42)))
    bbox = mark.getbbox()
    if bbox:
        mark = mark.crop(bbox)
    mark.save(os.path.join(ASSETS, "logo-mark.png"), optimize=True)

    compact = logo_light.crop((int(w * 0.18), int(h * 0.02), int(w * 0.82), int(h * 0.52)))
    bbox = compact.getbbox()
    if bbox:
        compact = compact.crop(bbox)
    compact.save(os.path.join(ASSETS, "logo-compact.png"), optimize=True)

    print("done")


if __name__ == "__main__":
    main()
