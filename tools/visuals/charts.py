"""Reusable declarative diagram templates for blog posts.

New blog posts should compose diagrams using these reusable builders inside one
of the four domain modules (`algebra_logic`, `geometry_analysis`, `mechanics_sky`,
`science_tech`) rather than creating one standalone `.py` script per article.
"""

from .core import (
    BLUE,
    BLUE_SOFT,
    BODY,
    BORDER,
    GREEN,
    GREEN_SOFT,
    HAIRLINE,
    INK,
    MUTED,
    ORANGE,
    ORANGE_SOFT,
    SLATE_SOFT,
    card,
    figure,
    header,
    pill,
    step_badge,
    txt,
)

PALETTE_CYCLE = (
    (BLUE, BLUE_SOFT),
    (GREEN, GREEN_SOFT),
    (ORANGE, ORANGE_SOFT),
)


def timeline_figure(title, subtitle, milestones, description, footer=None):
    """Build a clean vertical milestone roadmap figure on a 760px card.

    `milestones`: sequence of `(year_or_tag, heading_text, detail_text)`.
    """
    els = header(title, subtitle)
    y0 = 64
    row_h = 54
    for idx, (tag, head_t, body_t) in enumerate(milestones):
        fg, bg = PALETTE_CYCLE[idx % len(PALETTE_CYCLE)]
        ry = y0 + idx * (row_h + 10)
        els.append(card(24, ry, 712, row_h, rx=8))
        els.append(pill(38, ry + 16, tag, fg=fg, bg=bg, w=76, h=22, size=11.5))
        els.append(txt(128, ry + 22, head_t, 13, INK, weight="600"))
        els.append(txt(128, ry + 41, body_t, 11.8, BODY))
        if idx < len(milestones) - 1:
            els.append(f'<line x1="76" y1="{ry + row_h}" x2="76" y2="{ry + row_h + 10}" stroke="{HAIRLINE}" stroke-width="1.4"/>')
    total_h = y0 + len(milestones) * (row_h + 10) + (28 if footer else 10)
    if footer:
        els.append(txt(24, total_h - 12, footer, 11.5, MUTED))
    return figure(total_h, title, description, els)


def dual_panel_figure(title, subtitle, left_title, left_els, right_title, right_els, panel_h, description):
    """Build a standard side-by-side 760px two-card comparison figure."""
    els = header(title, subtitle)
    els.append(card(20, 62, 352, panel_h))
    els.append(txt(36, 84, left_title, 13, INK, weight="600"))
    els.extend(left_els)
    els.append(card(388, 62, 352, panel_h))
    els.append(txt(404, 84, right_title, 13, INK, weight="600"))
    els.extend(right_els)
    return figure(panel_h + 80, title, description, els)


def xy_axes(ox, oy, width, height, x_ticks=(), y_ticks=(), x_max=1.0, y_max=1.0):
    """Draw crisp 2D coordinate axes with optional gridlines and tick labels."""
    els = []
    for yv, ylbl in y_ticks:
        py = oy - (yv / y_max) * height
        els.append(f'<line x1="{ox}" y1="{py:.1f}" x2="{ox + width:.1f}" y2="{py:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
        els.append(txt(ox - 7, py + 4, ylbl, 10.5, MUTED, "end"))
    els.append(f'<path d="M{ox},{oy - height:.1f} V{oy} H{ox + width:.1f}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')
    for xv, xlbl in x_ticks:
        px = ox + (xv / x_max) * width
        els.append(txt(px, oy + 15, xlbl, 10.5, MUTED, "middle"))
    return els


def step_flow_cards(x, y0, width, steps, gap=10):
    """Render numbered vertical step cards inside a panel."""
    els = []
    for i, (st_title, st_detail, fg, bg) in enumerate(steps):
        ry = y0 + i * (44 + gap)
        els.append(card(x, ry, width, 44, rx=7, fill=bg, stroke=fg))
        els.append(step_badge(x + 18, ry + 22, i + 1, fg=fg, bg="#ffffff", r=9.5))
        els.append(txt(x + 35, ry + 18, st_title, 11.8, INK, weight="600"))
        els.append(txt(x + 35, ry + 35, st_detail, 11.2, BODY))
    return els
