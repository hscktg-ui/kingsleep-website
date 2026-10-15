"""Pre-deploy gate for kingsleep.co.kr. Run from anywhere:  python scripts/predeploy-check.py

Fails (exit 1) on placeholder facts, inconsistent business info, broken local links,
missing SEO tags, or deploy-hygiene problems. Facts come from js/data.js (company / contact).
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://kingsleep.co.kr"
PAGES = sorted(ROOT.glob("*.html"))
PUBLIC_TEXT = PAGES + sorted((ROOT / "css").glob("*.css")) + sorted((ROOT / "js").glob("*.js")) + [
    ROOT / "site.webmanifest", ROOT / "robots.txt", ROOT / "sitemap.xml"]
JS_RENDERED_IDS = {"products.html": {"lineup-mattress", "lineup-bedding", "lineup-headboard"}}

BANNED = {
    "시안 예시 전화번호": ["070-1234", "07012345678"],
    "시안 예시 사업자 정보": ["홍길동", "123-45-67890", "(주)킹슬립", "테헤란로", "2024-서울강남"],
    "지어낸 매장·연혁·리뷰": ["판교역로", "센텀동로", "동성로", "체험관", "351+", "재구매 의향", "2018", "BEST SELLER"],
    "지어낸 정책·가격": ["10년 품질 보증", "10년 보증", "무료 배송", "무이자", "15% OFF", "참고가", "₩"],
    "가짜 성적서·인증": ["KS-2025-0526", "kotiti-qr", "KATRI", "ISO 9001", "FIRA", "E0 등급", "KOTITI 인증"],
    "미개설 연락 수단": ["quality@kingsleep", "data-kakao", "카카오톡"],
    "경쟁사 이름": ["시몬스", "Simmons", "에이스", "지누스", "Zinus", "Lykke", "리케", "Oblique", "Flat Point",
                "플랫포인트", "Jackson", "잭슨", "King Koil", "킹코일", "포터리반", "Pottery"],
    "이전 도메인": ["kingsleep-website.vercel.app"],
    "대표 개인정보(생년월일)": ["1979-05-27", "1979.05.27", "1979년 05월 27일", "1979년 5월 27일", "790527"],
}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.meta: dict[str, list[str]] = {}
        self.canonical: list[str] = []
        self.h1 = 0
        self.titles = 0
        self.lang = None
        self.tels: list[str] = []
        self.smartstore: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.titles += 1
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta.setdefault(key, []).append(a.get("content", ""))
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a.get("href", ""))
        for attr in ("href", "src"):
            if a.get(attr):
                self.links.append((attr, a[attr]))
        if a.get("srcset"):
            for part in a["srcset"].split(","):
                self.links.append(("srcset", part.strip().split(" ")[0]))
        href = a.get("href", "")
        if href.startswith("tel:"):
            self.tels.append(href[4:])
        if "data-smartstore" in a:
            self.smartstore.append(href)


def data_value(key: str) -> str:
    m = re.search(rf'{key}:\s*"([^"]+)"', (ROOT / "js" / "data.js").read_text(encoding="utf-8"))
    if not m:
        err(f"data.js: '{key}' 값을 찾을 수 없음")
        return ""
    return m.group(1)


def main() -> int:
    facts = {k: data_value(k) for k in ("name", "ceo", "bizNumber", "address")}
    tel, phone, store = data_value("tel"), data_value("phone"), data_value("smartstoreUrl")

    for path in PUBLIC_TEXT:
        if not path.exists():
            err(f"{path.name}: 파일 없음")
            continue
        text = path.read_text(encoding="utf-8")
        for label, needles in BANNED.items():
            for n in needles:
                if n in text:
                    err(f"{path.relative_to(ROOT)}: {label} '{n}'")

    parsed: dict[str, Page] = {}
    for path in PAGES:
        p = Page()
        p.feed(path.read_text(encoding="utf-8"))
        parsed[path.name] = p

    for name, p in parsed.items():
        if p.lang != "ko":
            err(f"{name}: <html lang=\"ko\"> 아님")
        if p.titles != 1:
            err(f"{name}: <title> {p.titles}개")
        if p.h1 != 1:
            err(f"{name}: <h1> {p.h1}개 (1개여야 함)")
        desc = p.meta.get("description", [""])[0]
        if not 40 <= len(desc) <= 160:
            err(f"{name}: meta description 길이 {len(desc)}자 (40~160)")
        if len(p.canonical) != 1 or not p.canonical[0].startswith(SITE + "/"):
            err(f"{name}: canonical 이상 {p.canonical}")
        elif p.meta.get("og:url", [""])[0] != p.canonical[0]:
            err(f"{name}: og:url ≠ canonical")
        if not p.meta.get("og:image", [""])[0].startswith(SITE + "/"):
            err(f"{name}: og:image가 {SITE} 절대주소 아님")
        if "viewport" not in p.meta:
            err(f"{name}: viewport 없음")
        page_text = re.sub(r"<[^>]+>", "", (ROOT / name).read_text(encoding="utf-8"))
        for label, value in facts.items():
            if value not in page_text:
                err(f"{name}: 푸터 사업자 정보 누락 ({label}: {value})")
        for t in p.tels:
            if t != tel:
                err(f"{name}: tel:{t} ≠ data.js {tel}")
        if phone not in page_text:
            err(f"{name}: 고객센터 번호 {phone} 표기 없음")
        for s in p.smartstore:
            if s != store:
                err(f"{name}: 스마트스토어 링크 {s} ≠ {store}")

        for attr, url in p.links:
            if url.startswith(("http://", "https://", "tel:", "mailto:", "data:")):
                continue
            parts = urlsplit(url)
            target = parts.path or name
            if target in ("./", "/"):
                target = "index.html"
            if not (ROOT / target).exists():
                err(f"{name}: 깨진 링크 {attr}='{url}'")
                continue
            if parts.fragment and target.endswith(".html"):
                ids = parsed.get(target, Page()).ids | JS_RENDERED_IDS.get(target, set())
                if parts.fragment not in ids:
                    err(f"{name}: 없는 앵커 '{url}'")

    if "naver-site-verification" not in parsed["index.html"].meta:
        err("index.html: naver-site-verification 메타 없음")

    def read(name: str) -> str:
        path = ROOT / name
        return path.read_text(encoding="utf-8") if path.exists() else ""

    for loc in re.findall(r"<loc>(.*?)</loc>", read("sitemap.xml")):
        path = urlsplit(loc).path.lstrip("/") or "index.html"
        if not loc.startswith(SITE + "/") or not (ROOT / path).exists():
            err(f"sitemap.xml: 잘못된 주소 {loc}")
    if f"Sitemap: {SITE}/sitemap.xml" not in read("robots.txt"):
        err("robots.txt: Sitemap 줄 없음")

    ignore = read(".vercelignore").split()
    for must in (".cursor", "scripts", "brand-source"):
        if must not in ignore:
            err(f".vercelignore: '{must}' 제외 안 됨 (공개 배포됨)")

    for img in sorted((ROOT / "assets" / "images").glob("*.jpg")):
        kb = img.stat().st_size // 1024
        if kb > 400:
            warnings.append(f"{img.name}: {kb}KB (400KB 초과)")

    for w in warnings:
        print(f"  주의  {w}")
    for e in errors:
        print(f"  실패  {e}")
    print(f"\n{len(PAGES)}개 페이지 점검 — 실패 {len(errors)}건, 주의 {len(warnings)}건")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
