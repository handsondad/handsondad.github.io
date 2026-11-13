"""Core SVG design system, shared primitives, topic registry, and UX auditor.

All blog SVG diagrams share this single design system instead of duplicating
per-article helper scripts:
- Wide/dual-panel editorial figures: width=760 (1:1 with Chirpy's ~760px prose
  column), 16px bold header, 11.5–13px labels, 10.5–11.5px notes.
- Classic vertical-stack figures: 720-unit layout scaled cleanly via
  <g transform="scale(0.75)"> to 540px centered cards so rendered text stays
  11.5–15.9px and all geometric tangents/animations remain invariant.
"""

from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parents[2]
IMAGES_ROOT = REPO_ROOT / "assets" / "images"

# Topic registry: slug -> {"fn": callable, "summary": str, "domain": str}
TOPICS = {}


def register(slug, summary, domain):
    """Register a topic diagram builder in the unified toolkit catalog."""
    def decorator(fn):
        if slug in TOPICS:
            raise ValueError(f"Duplicate visual topic slug: {slug}")
        TOPICS[slug] = {"fn": fn, "summary": summary, "domain": domain}
        return fn
    return decorator


# ---------------------------------------------------------------------------
# 1. Modern 760px Editorial Design System
# ---------------------------------------------------------------------------
WIDTH = 760

BG = "#fbfcfd"
CARD_BG = "#ffffff"
BORDER = "#e2e8f0"
HAIRLINE = "#cbd5e1"

INK = "#0f172a"
BODY = "#1e293b"
MUTED = "#64748b"

BLUE = "#1d6fa5"
BLUE_SOFT = "#eaf4fb"
BLUE_LINE = "#93c5fd"

ORANGE = "#c25014"
ORANGE_SOFT = "#fef1e8"

GREEN = "#18794e"
GREEN_SOFT = "#e7f6ee"

PURPLE = "#6d28d9"
PURPLE_SOFT = "#f3e8ff"

SLATE = "#475569"
SLATE_SOFT = "#f1f5f9"

TITLE_SIZE = 16
SUB_SIZE = 12.5
PANEL_TITLE = 13.5
LABEL_SIZE = 13
NOTE_SIZE = 11.5


def txt(
    x,
    y,
    value,
    size=LABEL_SIZE,
    color=BODY,
    anchor="start",
    weight=None,
    halo=False,
    cls=None,
):
    attrs = [
        f'x="{x:.1f}"' if isinstance(x, float) else f'x="{x}"',
        f'y="{y:.1f}"' if isinstance(y, float) else f'y="{y}"',
        f'font-size="{size}"',
        f'fill="{color}"',
        f'text-anchor="{anchor}"',
    ]
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if halo:
        attrs.append('class="halo"' if not cls else f'class="halo {cls}"')
    elif cls:
        attrs.append(f'class="{cls}"')
    return f'<text {" ".join(attrs)}>{escape(str(value))}</text>'


def card(x, y, w, h, rx=10, fill=CARD_BG, stroke=BORDER, sw=1, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'
    )


def pill(x, y, label, fg=BLUE, bg=BLUE_SOFT, border=None, w=None, h=22, size=12):
    bw = w if w is not None else max(42, int(len(str(label)) * 8.5 + 18))
    bstroke = border or fg
    return "\n".join(
        [
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{h}" rx="{h / 2:.1f}" '
            f'fill="{bg}" stroke="{bstroke}" stroke-width="1" stroke-opacity="0.35"/>',
            txt(x + bw / 2, y + h * 0.68, label, size=size, color=fg, anchor="middle", weight="600"),
        ]
    )


def step_badge(cx, cy, num, fg=BLUE, bg=BLUE_SOFT, r=10.5):
    return "\n".join(
        [
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="{fg}" stroke-width="1.2"/>',
            txt(cx, cy + 4, str(num), size=11.5, color=fg, anchor="middle", weight="700"),
        ]
    )


def header(title, subtitle=None, x=24, y=28):
    out = [txt(x, y, title, size=TITLE_SIZE, color=INK, weight="700")]
    if subtitle:
        out.append(txt(x, y + 20, subtitle, size=SUB_SIZE, color=MUTED))
    return out


def std_defs(extra_css="", extra_defs=""):
    ed = f"\n  {extra_defs.strip()}" if extra_defs.strip() else ""
    ec = f"\n  {extra_css.strip()}" if extra_css.strip() else ""
    return f"""<defs>
  <marker id="arr-blue" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{BLUE}"/>
  </marker>
  <marker id="arr-orange" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{ORANGE}"/>
  </marker>
  <marker id="arr-green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{GREEN}"/>
  </marker>
  <marker id="arr-muted" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{MUTED}"/>
  </marker>{ed}
</defs>
<style>
  text {{
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", system-ui, sans-serif;
    letter-spacing: 0.01em;
  }}
  .mono {{
    font-family: ui-monospace, "Cascadia Mono", "Consolas", monospace;
  }}
  .halo {{
    paint-order: stroke;
    stroke: #ffffff;
    stroke-width: 3.5px;
    stroke-linejoin: round;
  }}{ec}
</style>"""


def figure(height, title, description, elements, extra_css="", extra_defs="", width=WIDTH):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" lang="zh-CN">\n'
        f'<title id="title">{escape(title)}</title>\n'
        f'<desc id="desc">{escape(description)}</desc>\n'
        + std_defs(extra_css=extra_css, extra_defs=extra_defs)
        + "\n"
        + f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1"/>\n'
        + "\n".join(elements)
        + "\n</svg>\n"
    )
    ET.fromstring(svg)
    return svg


def write_svg(subdir, name, content):
    out_dir = IMAGES_ROOT / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = name if name.endswith(".svg") else f"{name}.svg"
    (out_dir / fname).write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# 2. Shared 720->540 Scaled Portrait Primitives (Kepler / Bernoulli / Archive)
# ---------------------------------------------------------------------------
K_INK, K_BLUE, K_RED, K_GOLD = "#172b45", "#176786", "#b34039", "#b77a09"
K_MUTED, K_ORANGE = "#41576a", "#ad4f16"
DISP_SCALE = 0.75


def _k_scaled_font(size, value):
    s = str(value).strip()
    if size >= 38 and len(s) <= 2:
        return 28.0, "700"
    if size >= 27.5:
        return min(size * 0.72, 21.2), "700"
    if size >= 25.5:
        return size * 0.74, "600"
    return max(15.2, size * 0.76), None


def k_text(x, y, value, size=24, color=K_INK, anchor="start"):
    new_size, weight = _k_scaled_font(size, value)
    adj_y = y - 0.28 * (size - new_size)
    w_attr = f' font-weight="{weight}"' if weight else ""
    return (
        f'<text x="{x}" y="{adj_y:.2f}" font-size="{new_size:.1f}" fill="{color}" '
        f'text-anchor="{anchor}"{w_attr}>{escape(str(value))}</text>'
    )


def k_line(x1, y1, x2, y2, color=K_INK, dash=False, arrow=False):
    return (
        f'<path d="M{x1:.3f},{y1:.3f} L{x2:.3f},{y2:.3f}" fill="none" '
        f'stroke="{color}" stroke-width="2.4"'
        + (' stroke-dasharray="7 6"' if dash else "")
        + (' marker-end="url(#arrow)"' if arrow else "")
        + "/>"
    )


def k_dot(x, y, r=6, color=K_BLUE):
    return f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{color}"/>'


def k_path(points, color=K_BLUE, width=3, dash=False):
    w_adj = width if width >= 8 else max(1.6, width * 0.82)
    d = "M" + " L".join(f"{x:.3f},{y:.3f}" for x, y in points)
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w_adj:g}"'
        + (' stroke-dasharray="8 6"' if dash else "")
        + "/>"
    )


def k_panel(y, height):
    return (
        f'<rect x="24" y="{y}" width="672" height="{height}" rx="14" '
        'fill="#ffffff" stroke="#dde6ee" stroke-width="1.5"/>'
    )


def k_save(name, height, title, description, body, css="", output_directory=None):
    nw = int(round(720 * DISP_SCALE))
    nh = round(height * DISP_SCALE, 2)
    nh_s = str(int(nh)) if float(nh).is_integer() else f"{nh:g}"
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{nw}" height="{nh_s}" '
        f'viewBox="0 0 {nw} {nh_s}" role="img" aria-labelledby="title desc" lang="zh-CN">'
        f'<title id="title">{escape(title)}</title>'
        f'<desc id="desc">{escape(description)}</desc>'
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto-start-reverse"><path d="M0 0L8 4L0 8Z" '
        'fill="context-stroke"/></marker></defs>'
        '<style>text{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif}'
        + css
        + "</style>"
        f'<rect x="0.75" y="0.75" width="{nw - 1.5:g}" height="{nh - 1.5:g}" rx="12" '
        'fill="#fbfcfd" stroke="#dde6ee" stroke-width="1.2"/>'
        f'<g transform="scale({DISP_SCALE:g})">'
        + body
        + "</g></svg>\n"
    )
    root = ET.fromstring(svg)
    assert root.attrib["viewBox"] == f'0 0 {root.attrib["width"]} {root.attrib["height"]}'
    output_directory.mkdir(parents=True, exist_ok=True)
    fname = name if name.endswith(".svg") else f"{name}.svg"
    (output_directory / fname).write_text(svg, encoding="utf-8")


def b_document(height, title, description, elements, scale=DISP_SCALE):
    nw = int(round(720 * scale))
    nh = round(height * scale, 2)
    nh_s = str(int(nh)) if float(nh).is_integer() else f"{nh:g}"
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{nw}" height="{nh_s}" '
        f'viewBox="0 0 {nw} {nh_s}" role="img" aria-labelledby="title desc" lang="zh-CN">\n'
        f'<title id="title">{escape(title)}</title>\n'
        f'<desc id="desc">{escape(description)}</desc>\n'
        '<style>text{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif}</style>\n'
        f'<rect x="0.75" y="0.75" width="{nw - 1.5:g}" height="{nh - 1.5:g}" rx="12" fill="#fbfcfd" stroke="#dde6ee" stroke-width="1.2"/>\n'
        f'<g transform="scale({scale:g})">\n'
        + "\n".join(elements)
        + "\n</g>\n</svg>\n"
    )
    ET.fromstring(svg)
    return svg


# ---------------------------------------------------------------------------
# 3. Repository-Wide UX & Accessibility Auditor
# ---------------------------------------------------------------------------
def audit_all_svgs(images_root=IMAGES_ROOT):
    """Validate XML, aspect ratio, title/desc, and rendered font sizes across all SVGs."""
    checked = 0
    ns = "{http://www.w3.org/2000/svg}"
    for svg in sorted(images_root.rglob("*.svg")):
        if svg.parent == images_root:
            continue
        raw = svg.read_text(encoding="utf-8")
        root = ET.fromstring(raw)
        w, h, vb = root.get("width"), root.get("height"), root.get("viewBox")
        if not (w and h and vb):
            raise AssertionError(f"Missing width/height/viewBox in {svg}")
        _, _, vw, vh = [float(x) for x in vb.split()]
        if abs((float(w) / float(h)) - (vw / vh)) > 0.01:
            raise AssertionError(f"Aspect ratio mismatch in {svg}: {w}x{h} vs {vb}")
        if root.find(f"{ns}title") is None or root.find(f"{ns}desc") is None:
            raise AssertionError(f"Missing <title> or <desc> in {svg}")
        mg = re.search(r'<g transform="scale\(([0-9.]+)\)">', raw)
        g_scale = float(mg.group(1)) if mg else 1.0
        eff_scale = (min(float(w), 760.0) / vw) * g_scale
        sizes = [float(x) * eff_scale for x in re.findall(r'font-size="([0-9.]+)"', raw)]
        sizes += [float(x) * eff_scale for x in re.findall(r'font-size:\s*([0-9.]+)', raw)]
        sizes += [float(x) * eff_scale for x in re.findall(r'font:\s*(?:[a-zA-Z0-9-]+\s+)*([0-9.]+)px', raw)]
        if sizes:
            med = sorted(sizes)[len(sizes) // 2]
            if med > 18.2 or max(sizes) > 22.0:
                raise AssertionError(f"Oversized rendered font in {svg}: median={med:.1f}px max={max(sizes):.1f}px")
        checked += 1
    return checked
