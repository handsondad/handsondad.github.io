"""Self-host the homepage fonts as Google Fonts' unicode-range WOFF2 slices.

Ma Shan Zheng as a single TTF is ~5.8 MB. Google Fonts splits it into ~90
frequency-ordered WOFF2 slices; with matching `unicode-range` declarations the
browser only downloads the slices whose characters appear on the page.
Both fonts are SIL OFL 1.1, so the slices may be redistributed (licenses are
kept in assets/fonts/).

Usage: python tools/fetch_landing_fonts.py           # re-download slices
       python tools/fetch_landing_fonts.py --check   # only verify homepage glyph coverage
"""

from __future__ import annotations

import re
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts" / "landing"
CSS_OUT = ROOT / "assets" / "css" / "landing-fonts.css"
CSS_URL = "https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&family=Ma+Shan+Zheng&display=swap"
# Google only serves unicode-range WOFF2 slices to browsers it recognises.
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
SLUGS = {"Comic Neue": "comic-neue", "Ma Shan Zheng": "ma-shan-zheng"}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def parse_ranges(text: str) -> list[tuple[int, int]]:
    ranges = []
    for part in text.split(","):
        part = part.strip().upper().removeprefix("U+")
        start, _, end = part.partition("-")
        ranges.append((int(start, 16), int(end or start, 16)))
    return ranges


def covered(char: str, ranges: list[tuple[int, int]]) -> bool:
    code = ord(char)
    return any(start <= code <= end for start, end in ranges)


def homepage_chars() -> set[str]:
    text = (ROOT / "index.html").read_text(encoding="utf-8") + (ROOT / "_data" / "projects.yml").read_text(encoding="utf-8")
    return {c for c in text if "\u4e00" <= c <= "\u9fff"}


def check_existing() -> None:
    css = CSS_OUT.read_text(encoding="utf-8")
    ranges = [r for m in re.finditer(r'font-family:"Ma Shan Zheng".*?unicode-range:([^}]+)\}', css) for r in parse_ranges(m.group(1))]
    for name in re.findall(r'url\("\.\./fonts/landing/([^"]+)"\)', css):
        assert (FONT_DIR / name).exists(), f"缺少字体分片 {name}"
    missing = sorted(c for c in homepage_chars() if not covered(c, ranges))
    assert not missing, f"首页用到但字体分片不含的字：{''.join(missing)}"
    print(f"首页 {len(homepage_chars())} 个汉字全部有字形，分片文件齐全")


def main() -> None:
    if "--check" in sys.argv:
        check_existing()
        return
    css = fetch(CSS_URL).decode("utf-8")
    blocks = re.findall(r"@font-face\s*\{(.*?)\}", css, flags=re.S)
    assert blocks, "Google Fonts 返回的 CSS 里没有 @font-face"

    if FONT_DIR.exists():
        shutil.rmtree(FONT_DIR)
    FONT_DIR.mkdir(parents=True)

    out = ["/* 由 tools/fetch_landing_fonts.py 生成，请勿手改。字体均为 SIL OFL 1.1，授权见 assets/fonts/。 */"]
    counts: dict[str, int] = {}
    total_bytes = 0
    cjk_ranges: list[tuple[int, int]] = []
    for block in blocks:
        family = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
        unicode_range = re.search(r"unicode-range:\s*([^;]+);", block).group(1).strip()
        index = counts.get(family, 0)
        counts[family] = index + 1
        name = f"{SLUGS[family]}-{weight}-{index:03d}.woff2"
        data = fetch(url)
        assert data[:4] == b"wOF2", f"{url} 不是 WOFF2"
        (FONT_DIR / name).write_bytes(data)
        total_bytes += len(data)
        if family == "Ma Shan Zheng":
            cjk_ranges += parse_ranges(unicode_range)
        out.append(
            "@font-face{"
            f"font-family:\"{family}\";font-style:normal;font-weight:{weight};font-display:swap;"
            f"src:url(\"../fonts/landing/{name}\") format(\"woff2\");unicode-range:{unicode_range}}}"
        )

    assert counts.get("Comic Neue", 0) >= 2, counts
    assert counts.get("Ma Shan Zheng", 0) >= 80, f"马善政分片异常少：{counts}"
    missing = sorted(c for c in homepage_chars() if not covered(c, cjk_ranges))
    assert not missing, f"首页用到但字体分片不含的字：{''.join(missing)}"

    CSS_OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{sum(counts.values())} 个分片，合计 {total_bytes / 1024:.0f} KB -> {FONT_DIR.relative_to(ROOT)}")
    print(f"首页 {len(homepage_chars())} 个汉字全部有字形；CSS -> {CSS_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
