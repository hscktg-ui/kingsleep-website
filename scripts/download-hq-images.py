"""Download curated luxury hotel/bedroom Unsplash images and encode HQ JPEGs."""
from pathlib import Path
from io import BytesIO
import urllib.request
from PIL import Image, ImageFilter, ImageEnhance

OUT = Path(r"C:\Users\user\Projects\kingsleep-website\assets\images")

# Curated: white/neutral luxury beds + one dark interior (navy mood)
SOURCES = {
    "hero-bedroom.jpg": "1618773928121-c32242e63f39",
    "mattress-royal.jpg": "1629140727571-9b5c6f6267b4",
    "mattress-cloud.jpg": "1566665797739-1674de7a421a",
    "mattress-detail.jpg": "1630660664869-c9d3cc676880",
    "bedding-deep.jpg": "1605346434674-a440ca4dc4c0",
    "headboard-royal.jpg": "1731336478850-6bce7235e320",
    "interior-navy.jpg": "1615874959474-d609969a20ed",
    "collection-mattress.jpg": "1690935986319-c11e6cae84f7",
    "collection-bedding.jpg": "1445991842772-097fea258e7b",
}


def fetch(photo_id: str) -> bytes:
    url = f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=2800&q=95"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def enhance(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    max_side = 2400
    if max(w, h) > max_side:
        if w >= h:
            im = im.resize((max_side, int(h * max_side / w)), Image.Resampling.LANCZOS)
        else:
            im = im.resize((int(w * max_side / h), max_side), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = ImageEnhance.Color(im).enhance(1.04)
    im = ImageEnhance.Sharpness(im).enhance(1.2)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=55, threshold=2))
    return im


def main():
    for name, pid in SOURCES.items():
        print(f"→ {name}")
        try:
            data = fetch(pid)
            im = enhance(Image.open(BytesIO(data)))
            out = OUT / name
            im.save(out, "JPEG", quality=92, optimize=True, progressive=True)
            print(f"  OK {im.size} {out.stat().st_size // 1024}KB")
        except Exception as e:
            print(f"  FAIL {e}")


if __name__ == "__main__":
    main()
