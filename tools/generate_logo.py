"""Generate the “遇见孩子” brand logo (SVG + PNG + favicon).

The four characters are outlined from Ma Shan Zheng (SIL OFL 1.1, already
self-hosted in assets/fonts/landing/), so the SVG needs no font at render time.
Colours follow the homepage: the title's rainbow gradient for the characters,
the small-planet stage gradient for the tile, warm brown ink for shadows.

Rasterising uses headless Microsoft Edge (or Chrome) and Pillow.
Usage: python tools/generate_logo.py
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts" / "landing"
SVG_OUT = ROOT / "assets" / "images" / "logo.svg"
PNG_OUT = ROOT / "assets" / "images" / "logo.png"
AVATAR_OUT = ROOT / "assets" / "images" / "logo-avatar.png"
SOCIAL_OUT = ROOT / "assets" / "images" / "social-preview.png"
ICO_OUT = ROOT / "favicon.ico"
FAVICON_DIR = ROOT / "assets" / "img" / "favicons"

SIZE = 512
# (character, fill colour, cell centre, tilt in degrees)
CELLS = [
    ("遇", "#f26b4f", (152, 154), -5),
    ("见", "#f28c25", (350, 160), 4),
    ("孩", "#3da5e8", (156, 360), 3),
    ("子", "#9b6cf0", (352, 356), -4),
]
GLYPH_BOX = 196  # longest side of each character, in viewBox units
HALO = 26        # white sticker border width
SHADOW_DY = 9
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def find_glyphs(chars: str) -> dict[str, tuple[TTFont, str]]:
    found = {}
    for path in sorted(FONT_DIR.glob("ma-shan-zheng-400-*.woff2")):
        font = TTFont(path)
        cmap = font.getBestCmap()
        for char in chars:
            if char not in found and ord(char) in cmap:
                found[char] = (font, cmap[ord(char)])
    missing = [c for c in chars if c not in found]
    assert not missing, f"字体分片里找不到：{missing}，先运行 tools/fetch_landing_fonts.py"
    return found


def glyph_path(font: TTFont, name: str, centre: tuple[float, float], box: float) -> tuple[str, float, float]:
    glyphs = font.getGlyphSet()
    bounds = BoundsPen(glyphs)
    glyphs[name].draw(bounds)
    x0, y0, x1, y1 = bounds.bounds
    scale = box / max(x1 - x0, y1 - y0)
    cx, cy = centre
    # Font units are y-up; flip and centre the glyph's ink box on the cell.
    dx = cx - (x0 + x1) / 2 * scale
    dy = cy + (y0 + y1) / 2 * scale
    pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, dx, dy)))
    return pen.getCommands(), (x1 - x0) * scale / 2, (y1 - y0) * scale / 2


# shape: (character shrink, halo factor, radius the ink must stay inside or None for the square-margin check)
SHAPES = {
    "tile": (1.0, 1.0, None),             # rounded square: homepage, favicon
    "round": (0.8, 0.85, SIZE / 2 - 8),   # Chirpy crops the sidebar avatar to a circle
    "full": (0.64, 0.8, SIZE * 0.4),      # opaque square for iOS / Android; maskable safe zone is the central 80% circle
}


def build_svg(shape: str = "tile") -> str:
    glyphs = find_glyphs("".join(c for c, *_ in CELLS))
    shrink, halo_factor, safe_radius = SHAPES[shape]
    halo = HALO * halo_factor
    mid = SIZE / 2
    parts = []
    for char, colour, (x, y), tilt in CELLS:
        cx, cy = mid + (x - mid) * shrink, mid + (y - mid) * shrink
        d, half_w, half_h = glyph_path(*glyphs[char], (cx, cy), GLYPH_BOX * shrink)
        pad = halo / 2
        if safe_radius:
            far = max(((cx + sx * (half_w + pad) - mid) ** 2 + (cy + sy * (half_h + pad) + max(sy, 0) * SHADOW_DY - mid) ** 2) ** 0.5
                      for sx in (-1, 1) for sy in (-1, 1))
            assert far < safe_radius, f"{shape}：“{char}”的角距圆心 {far:.0f}，超出安全半径 {safe_radius:.0f}"
        else:
            assert cx - half_w - pad > 14 and cx + half_w + pad < SIZE - 14, f"“{char}”超出左右边界"
            assert cy - half_h - pad > 14 and cy + half_h + pad + SHADOW_DY < SIZE - 10, f"“{char}”超出上下边界"
        parts.append(
            f'  <g transform="rotate({tilt} {cx:g} {cy:g})">\n'
            f'    <path d="{d}" fill="#e9a882" stroke="#e9a882" stroke-width="{halo:g}" stroke-linejoin="round" transform="translate(0 {SHADOW_DY})"/>\n'
            f'    <path d="{d}" fill="#fff" stroke="#fff" stroke-width="{halo:g}" stroke-linejoin="round"/>\n'
            f'    <path d="{d}" fill="{colour}"/>\n'
            f'  </g>'
        )
    backdrop, shape_name = {
        "tile": (f'<rect x="8" y="8" width="{SIZE - 16}" height="{SIZE - 16}" rx="124" fill="url(#tile)" stroke="#ffcfb2" stroke-width="10"/>', "圆角方块"),
        "round": (f'<circle cx="{mid:g}" cy="{mid:g}" r="{mid - 6:g}" fill="url(#tile)" stroke="#ffcfb2" stroke-width="10"/>', "圆形"),
        "full": (f'<rect width="{SIZE}" height="{SIZE}" fill="url(#tile)"/>', "方形底"),
    }[shape]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}" role="img" aria-labelledby="logo-title logo-desc">
  <title id="logo-title">遇见孩子</title>
  <desc id="logo-desc">Hands-on Dad 标志：奶油桃色{shape_name}上，“遇见孩子”四个手写字排成两行，分别是珊瑚红、橙、天蓝和薰衣草紫，带白色贴纸描边。</desc>
  <defs>
    <radialGradient id="tile" cx="50%" cy="38%" r="70%">
      <stop offset="0" stop-color="#fffaf3"/>
      <stop offset=".65" stop-color="#ffe6d6"/>
      <stop offset="1" stop-color="#ffd4c4"/>
    </radialGradient>
  </defs>
  {backdrop}
{chr(10).join(parts)}
</svg>
"""


def rasterise(svg: Path, png: Path) -> None:
    browser = next((b for b in BROWSERS if Path(b).exists()), None) or shutil.which("msedge") or shutil.which("chrome")
    assert browser, "需要 Microsoft Edge 或 Chrome 来把 SVG 转成 PNG"
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "logo.html"
        page.write_text(f'<html><body style="margin:0;background:transparent"><img src="{svg.as_uri()}" width="{SIZE}" height="{SIZE}"></body></html>', encoding="utf-8")
        subprocess.run([
            browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            "--default-background-color=00000000", f"--window-size={SIZE},{SIZE}",
            f"--user-data-dir={Path(tmp) / 'profile'}", f"--screenshot={png}", page.as_uri(),
        ], check=True, capture_output=True, timeout=60)
    assert png.exists(), "浏览器没有生成截图"


def render(shape: str) -> Image.Image:
    with tempfile.TemporaryDirectory() as tmp:
        svg = Path(tmp) / "logo.svg"
        svg.write_text(build_svg(shape), encoding="utf-8")
        shot = Path(tmp) / "shot.png"
        rasterise(svg, shot)
        image = Image.open(shot).convert("RGBA").crop((0, 0, SIZE, SIZE))
    assert image.getpixel((1, 1))[3] == (255 if shape == "full" else 0), f"{shape}：外角透明度不对"
    assert image.getpixel((SIZE // 2, 30))[3] == 255, f"{shape}：底板内部应不透明"
    return image


def save_png(image: Image.Image, path: Path, size: int, opaque: bool = False) -> None:
    resized = image.resize((size, size), Image.LANCZOS)
    (resized.convert("RGB") if opaque else resized).save(path, optimize=True)


def render_social_preview() -> None:
    """Render a 1200x630 OpenGraph / social share banner matching the homepage aesthetic."""
    browser = next((b for b in BROWSERS if Path(b).exists()), None) or shutil.which("msedge") or shutil.which("chrome")
    assert browser, "需要 Microsoft Edge 或 Chrome 来生成社交分享预览图"
    w, h = 1200, 630
    fonts_css = (ROOT / "assets" / "css" / "landing-fonts.css").as_uri()
    logo_uri = SVG_OUT.as_uri()
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="{fonts_css}">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: {w}px; height: {h}px; overflow: hidden;
    font-family: "Comic Neue", "Ma Shan Zheng", "KaiTi", "Microsoft YaHei", cursive;
    background:
      radial-gradient(circle at 14% 20%, #ff8a6b24 0%, transparent 45%),
      radial-gradient(circle at 86% 22%, #6cc4ff29 0%, transparent 46%),
      radial-gradient(circle at 82% 84%, #b48cff24 0%, transparent 45%),
      linear-gradient(135deg, #fff8f0 0%, #f4f9ff 52%, #fff0e6 100%);
    color: #5d4e37;
    display: grid;
    place-items: center;
  }}
  .card {{
    width: 1104px; height: 534px;
    border-radius: 40px;
    border: 4px solid #ffd4b8;
    background: linear-gradient(145deg, rgba(255,255,255,0.92) 45%, rgba(255,243,232,0.92) 100%);
    box-shadow: 0 18px 44px rgba(255, 111, 107, 0.14);
    padding: 48px 56px;
    display: grid;
    grid-template-columns: 224px 1fr;
    align-items: center;
    gap: 44px;
  }}
  .logo-wrap {{
    display: grid;
    place-items: center;
  }}
  .logo-wrap img {{
    width: 220px; height: 220px;
    filter: drop-shadow(0 10px 0 #ffd4b8);
  }}
  .eyebrow {{
    display: inline-block;
    padding: 6px 18px;
    border-radius: 999px;
    border: 2px solid #ffe0cc;
    background: #fff8f0;
    color: #b8622a;
    font-size: 21px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 18px;
  }}
  h1 {{
    font-size: 54px;
    line-height: 1.25;
    letter-spacing: 2px;
    white-space: nowrap;
    margin-bottom: 14px;
    background: linear-gradient(90deg, #ff7a5c, #ff9f43 36%, #4da8f0 72%, #9b6cf0);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }}
  .sub {{
    font-size: 25px;
    color: #7a684d;
    white-space: nowrap;
    margin-bottom: 28px;
  }}
  .pills {{
    display: flex;
    gap: 12px;
    flex-wrap: nowrap;
  }}
  .pill {{
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 19px;
    font-weight: 700;
    white-space: nowrap;
  }}
  .pill.p1 {{ background: #fff0e6; border: 2px solid #ffd4b8; color: #c8662c; }}
  .pill.p2 {{ background: #edf5ff; border: 2px solid #b8d7ff; color: #3a6fc0; }}
  .pill.p3 {{ background: #edf9ee; border: 2px solid #bce7c1; color: #3f8a4b; }}
</style>
</head>
<body>
  <div class="card">
    <div class="logo-wrap"><img src="{logo_uri}" alt="遇见孩子"></div>
    <div>
      <span class="eyebrow">Hands-on Dad · 专为奶爸打造的育儿宝库</span>
      <h1>大手牵小手，世界有意思</h1>
      <p class="sub">把孩子的每一个「为什么」，变成我们一起探索的起点</p>
      <div class="pills">
        <span class="pill p1">🎮 亲子探索互动小站</span>
        <span class="pill p2">🔬 原创分步图解科普</span>
        <span class="pill p3">🌱 育儿与学习好内容收藏</span>
      </div>
    </div>
  </div>
</body>
</html>"""
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "social.html"
        shot = Path(tmp) / "social.png"
        page.write_text(html, encoding="utf-8")
        subprocess.run([
            browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            "--virtual-time-budget=2500", f"--window-size={w},{h}",
            f"--user-data-dir={Path(tmp) / 'profile'}", f"--screenshot={shot}", page.as_uri(),
        ], check=True, capture_output=True, timeout=60)
        img = Image.open(shot).convert("RGB").crop((0, 0, w, h))
    assert img.size == (w, h), f"社交分享图尺寸不对：{img.size}"
    colours = img.getcolors(maxcolors=2048)
    assert colours is None or len(colours) > 500, "社交分享图颜色异常单一"
    img.save(SOCIAL_OUT, optimize=True)


def main() -> None:
    SVG_OUT.write_text(build_svg("tile"), encoding="utf-8")
    tile, badge, full = render("tile"), render("round"), render("full")
    ico_sizes = [(16, 16), (32, 32), (48, 48)]

    save_png(tile, PNG_OUT, 256)
    save_png(badge, AVATAR_OUT, 256)
    tile.save(ICO_OUT, sizes=ico_sizes)
    # Chirpy reads these names from assets/img/favicons/ (repo files override the theme's defaults).
    FAVICON_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SVG_OUT, FAVICON_DIR / "favicon.svg")
    tile.save(FAVICON_DIR / "favicon.ico", sizes=ico_sizes)
    save_png(tile, FAVICON_DIR / "favicon-96x96.png", 96)
    save_png(full, FAVICON_DIR / "apple-touch-icon.png", 180, opaque=True)
    save_png(full, FAVICON_DIR / "web-app-manifest-192x192.png", 192, opaque=True)
    save_png(full, FAVICON_DIR / "web-app-manifest-512x512.png", 512, opaque=True)
    render_social_preview()

    for path in [SVG_OUT, PNG_OUT, AVATAR_OUT, SOCIAL_OUT, ICO_OUT, *sorted(FAVICON_DIR.iterdir())]:
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
