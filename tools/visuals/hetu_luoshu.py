"""Hetu & Luoshu (河图洛书) classical number diagrams, combinatorics proofs, and history timeline."""

from html import escape
import itertools
import math

from .core import (
    BG,
    BLUE,
    BLUE_LINE,
    BLUE_SOFT,
    BODY,
    BORDER,
    CARD_BG,
    GREEN,
    GREEN_SOFT,
    HAIRLINE,
    INK,
    LABEL_SIZE,
    MUTED,
    NOTE_SIZE,
    ORANGE,
    ORANGE_SOFT,
    PANEL_TITLE,
    PURPLE,
    PURPLE_SOFT,
    SLATE,
    SLATE_SOFT,
    WIDTH,
    card,
    figure,
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

CRIMSON = "#b91c1c"
CRIMSON_SOFT = "#fef2f2"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
GOLD_LINE = "#d97706"


# Canonical Hetu directional pairs: (direction_cn, element_cn, inner_sheng, outer_cheng)
# Traditional Chinese map orientation: South=Top, North=Bottom, East=Left, West=Right
HETU_DIRS = [
    ("下北", "水", 1, 6),
    ("上南", "火", 2, 7),
    ("左东", "木", 3, 8),
    ("右西", "金", 4, 9),
    ("中宫", "土", 5, 10),
]

# Canonical Luoshu 3x3 matrix (Zhu Xi / Yang Hui orientation: 左三右七，二四为肩，六八为足，戴九履一)
LUOSHU_GRID = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

# Mingtang (大戴礼记·明堂) orientation (left-right mirror of LUOSHU_GRID)
MINGTANG_GRID = [
    [2, 9, 4],
    [7, 5, 3],
    [6, 1, 8],
]


def _verify_hetu_luoshu_math():
    """Exhaustively verify all arithmetic, combinatorial, and geometric claims."""
    # 1. Hetu (1..10):的天地之数 25 + 30 = 55 & mod-5 congruence
    odds_10 = [k for k in range(1, 11) if k % 2 == 1]
    evens_10 = [k for k in range(1, 11) if k % 2 == 0]
    assert sum(odds_10) == 25
    assert sum(evens_10) == 30
    assert sum(odds_10) + sum(evens_10) == 55

    for _, _, sheng, cheng in HETU_DIRS:
        assert 1 <= sheng <= 5
        assert cheng - sheng == 5
        assert sheng % 5 == cheng % 5
        assert (sheng % 2) != (cheng % 2)  # exact 1 odd (Yang) + 1 even (Yin) per direction!

    # Outer Hetu parity balance (excluding center 5 and 10): both outer Yang and outer Yin sum to 20
    outer_nums = [n for d, _, s, c in HETU_DIRS if d != "中宫" for n in (s, c)]
    outer_odd_sum = sum(n for n in outer_nums if n % 2 == 1)   # 1 + 7 + 3 + 9 = 20
    outer_even_sum = sum(n for n in outer_nums if n % 2 == 0)  # 6 + 2 + 8 + 4 = 20
    assert outer_odd_sum == 20 and outer_even_sum == 20

    # 2. Luoshu (1..9): exhaustive verification over all 9! = 362,880 permutations
    assert math.factorial(9) == 362880
    valid_squares = []
    for p in itertools.permutations(range(1, 10)):
        if (
            p[0] + p[1] + p[2] == 15
            and p[3] + p[4] + p[5] == 15
            and p[6] + p[7] + p[8] == 15
            and p[0] + p[3] + p[6] == 15
            and p[1] + p[4] + p[7] == 15
            and p[2] + p[5] + p[8] == 15
            and p[0] + p[4] + p[8] == 15
            and p[2] + p[4] + p[6] == 15
        ):
            valid_squares.append(p)

    # Exact 8 valid 3x3 magic squares exist (= 1 unique solution up to D4 dihedral group of order 8!)
    assert len(valid_squares) == 8
    for sq in valid_squares:
        assert sq[4] == 5  # center is ALWAYS 5
        corners = {sq[0], sq[2], sq[6], sq[8]}
        edges = {sq[1], sq[3], sq[5], sq[7]}
        assert corners == {2, 4, 6, 8}  # corners are ALWAYS even
        assert edges == {1, 3, 7, 9}    # edges are ALWAYS odd

    assert tuple(n for row in LUOSHU_GRID for n in row) in valid_squares
    assert tuple(n for row in MINGTANG_GRID for n in row) in valid_squares

    # 3. Exact 8 three-element subsets of {1..9} summing to 15 (Tic-Tac-Toe isomorphism)
    triples_15 = [
        comb for comb in itertools.combinations(range(1, 10), 3) if sum(comb) == 15
    ]
    assert len(triples_15) == 8
    freq = {k: sum(1 for t in triples_15 if k in t) for k in range(1, 10)}
    assert freq[5] == 4
    for k in (2, 4, 6, 8):
        assert freq[k] == 3
    for k in (1, 3, 7, 9):
        assert freq[k] == 2

    # 4. Yang Hui's 1275 "九子斜排，上下对易，左右相更，四维挺出" construction check
    # Start with 3 diagonal rows of 1..9:
    diag_rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # Diamond coordinates (u = col - row, v = col + row):
    # Top=(0,0)->1; ( -1,1 )->4, (1,1)->2; (-2,2)->7, (0,2)->5, (2,2)->3; (-1,3)->8, (1,3)->6; (0,4)->9
    top, bot = diag_rows[0][0], diag_rows[2][2]      # 1, 9
    left, right = diag_rows[2][0], diag_rows[0][2]   # 7, 3
    nw, ne = diag_rows[1][0], diag_rows[0][1]        # 4, 2
    sw, se = diag_rows[2][1], diag_rows[1][2]        # 8, 6
    center = diag_rows[1][1]                         # 5
    # Swap top<->bot and left<->right, push 4 corners out:
    top, bot = bot, top
    left, right = right, left
    built = [
        [nw, top, ne],
        [left, center, right],
        [sw, bot, se],
    ]
    assert built == LUOSHU_GRID

    # 5. Square-sum & multi-digit identities on Luoshu
    assert sum(x * x for x in LUOSHU_GRID[0]) == 101
    assert sum(x * x for x in LUOSHU_GRID[2]) == 101
    assert sum(LUOSHU_GRID[r][0] ** 2 for r in range(3)) == 89
    assert sum(LUOSHU_GRID[r][2] ** 2 for r in range(3)) == 89
    lhs_3digit = 492 ** 2 + 357 ** 2 + 816 ** 2
    rhs_3digit = 294 ** 2 + 753 ** 2 + 618 ** 2
    assert lhs_3digit == rhs_3digit == 1035369


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{extra}{mk}/>'
    )


def _knot_chain(pts, is_yang, r=3.8, stroke_line="#64748b"):
    """Render connected traditional knot-dots (白圈阳数 ○ / 黑点阴数 ●) and return SVG string."""
    out = []
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        out.append(_line(x1, y1, x2, y2, color=stroke_line, sw=1.5))
    for x, y in pts:
        if is_yang:
            out.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#ffffff" '
                f'stroke="{INK}" stroke-width="1.8"/>'
            )
        else:
            out.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{INK}" '
                f'stroke="#ffffff" stroke-width="0.9"/>'
            )
    return "\n  ".join(out)


def _purple_marker_def():
    return """<marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#6d28d9"/>
  </marker>"""


def _build_dot_blueprints():
    """SVG 1: Side-by-side authentic knot-dot blueprints of Hetu (55 dots) and Luoshu (45 dots)."""
    h = 492
    body = []
    body.extend(
        header(
            "一眼分清河图与洛书：五十五点“十数配对图” vs 四十五点“九宫幻方图”",
            "白圈 ○ 表奇数（天数/阳），黑点 ● 表偶数（地数/阴）；古图方位皆为“上南下北、左东右西”",
        )
    )

    # Left Card: Hetu (河图, 55 dots)
    body.append(card(16, 68, 358, 408))
    body.append(pill(28, 80, "河图 · 1~10 共 55 点", fg=BLUE, bg=BLUE_SOFT, w=156, h=24))
    body.append(txt(194, 96, "五方奇偶相合（外减内恒为 5）", size=11.5, color=MUTED))

    cx, cy = 195.0, 266.0
    # Subtle cross axes & center box
    body.append(
        f'<rect x="{cx - 38:.1f}" y="{cy - 38:.1f}" width="76" height="76" rx="10" '
        f'fill="{AMBER_SOFT}" stroke="#fcd34d" stroke-width="1.2"/>'
    )
    body.append(_line(cx, cy - 86, cx, cy - 42, color="#e2e8f0", sw=1.2, dash="3 3"))
    body.append(_line(cx, cy + 42, cx, cy + 86, color="#e2e8f0", sw=1.2, dash="3 3"))
    body.append(_line(cx - 94, cy, cx - 42, cy, color="#e2e8f0", sw=1.2, dash="3 3"))
    body.append(_line(cx + 42, cy, cx + 94, cy, color="#e2e8f0", sw=1.2, dash="3 3"))

    hetu_groups = []
    # Center: 5 Yang + 10 Yin (two 5-dot bars top & bottom of center)
    pts_5 = [(cx, cy), (cx, cy - 11), (cx, cy + 11), (cx - 11, cy), (cx + 11, cy)]
    pts_10a = [(cx + k * 11.0, cy - 27.0) for k in (-2, -1, 0, 1, 2)]
    pts_10b = [(cx + k * 11.0, cy + 27.0) for k in (-2, -1, 0, 1, 2)]
    hetu_groups.extend([(pts_5, True), (pts_10a, False), (pts_10b, False)])
    # Center cross lines for 5
    body.append(_line(cx - 11, cy, cx + 11, cy, color="#64748b", sw=1.5))
    body.append(_line(cx, cy - 11, cx, cy + 11, color="#64748b", sw=1.5))
    for px, py in pts_5:
        body.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.7" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>'
        )
    body.append(_knot_chain(pts_10a, is_yang=False, r=3.5))
    body.append(_knot_chain(pts_10b, is_yang=False, r=3.5))

    # Top (South / Fire): inner 2 Yin, outer 7 Yang
    pts_2 = [(cx - 6.5, cy - 56.0), (cx + 6.5, cy - 56.0)]
    pts_7 = [(cx + k * 11.5, cy - 77.0) for k in range(-3, 4)]
    hetu_groups.extend([(pts_2, False), (pts_7, True)])
    body.append(_knot_chain(pts_2, is_yang=False, r=3.7))
    body.append(_knot_chain(pts_7, is_yang=True, r=3.7))

    # Bottom (North / Water): inner 1 Yang, outer 6 Yin
    pts_1 = [(cx, cy + 56.0)]
    pts_6 = [(cx + (k - 2.5) * 11.5, cy + 77.0) for k in range(6)]
    hetu_groups.extend([(pts_1, True), (pts_6, False)])
    body.append(_knot_chain(pts_1, is_yang=True, r=3.7))
    body.append(_knot_chain(pts_6, is_yang=False, r=3.7))

    # Left (East / Wood): inner 3 Yang, outer 8 Yin
    pts_3 = [(cx - 58.0, cy + k * 12.0) for k in (-1, 0, 1)]
    pts_8 = [(cx - 82.0, cy + (k - 3.5) * 11.0) for k in range(8)]
    hetu_groups.extend([(pts_3, True), (pts_8, False)])
    body.append(_knot_chain(pts_3, is_yang=True, r=3.7))
    body.append(_knot_chain(pts_8, is_yang=False, r=3.7))

    # Right (West / Metal): inner 4 Yin, outer 9 Yang
    pts_4 = [(cx + 58.0, cy + (k - 1.5) * 12.0) for k in range(4)]
    pts_9 = [(cx + 82.0, cy + k * 10.6) for k in range(-4, 5)]
    hetu_groups.extend([(pts_4, False), (pts_9, True)])
    body.append(_knot_chain(pts_4, is_yang=False, r=3.7))
    body.append(_knot_chain(pts_9, is_yang=True, r=3.7))

    # Assert exact dot counts in rendered Hetu
    yang_cnt_h = sum(len(pts) for pts, y in hetu_groups if y)
    yin_cnt_h = sum(len(pts) for pts, y in hetu_groups if not y)
    assert yang_cnt_h == 25 and yin_cnt_h == 30

    # Hetu directional callouts (carefully spaced clear of all dots)
    body.append(txt(cx, 134, "上南 · 火", size=12.5, color=CRIMSON, anchor="middle", weight="700"))
    body.append(txt(cx, 151, "外 7○ · 内 2●", size=11.5, color=BODY, anchor="middle"))

    body.append(txt(cx, 368, "内 1○ · 外 6●", size=11.5, color=BODY, anchor="middle"))
    body.append(txt(cx, 386, "下北 · 水", size=12.5, color=BLUE, anchor="middle", weight="700"))

    body.append(txt(64, cy - 10, "左东·木", size=12.5, color=GREEN, anchor="middle", weight="700"))
    body.append(txt(64, cy + 8, "外8● 内3○", size=11.5, color=BODY, anchor="middle"))

    body.append(txt(326, cy - 10, "右西·金", size=12.5, color=AMBER, anchor="middle", weight="700"))
    body.append(txt(326, cy + 8, "内4● 外9○", size=11.5, color=BODY, anchor="middle"))

    body.append(txt(cx, cy + 49, "中土 5○·10●", size=11, color=AMBER, anchor="middle", weight="700", halo=True))

    # Hetu bottom summary strip
    body.append(
        f'<rect x="28" y="404" width="334" height="58" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    body.append(txt(40, 425, "天数（5 奇 ○）：1 + 3 + 5 + 7 + 9 = 25", size=11.5, color=INK, weight="600"))
    body.append(txt(40, 446, "地数（5 偶 ●）：2 + 4 + 6 + 8 + 10 = 30（总和 55）", size=11.5, color=BODY))

    # Right Card: Luoshu (洛书, 45 dots)
    body.append(card(386, 68, 358, 408))
    body.append(pill(398, 80, "洛书 · 1~9 共 45 点", fg=ORANGE, bg=ORANGE_SOFT, w=152, h=24))
    body.append(txt(560, 96, "三阶幻方（横竖斜 8 线皆 = 15）", size=11.5, color=MUTED))

    gx0, gy0 = 420.0, 136.0
    cw, ch = 88.0, 78.0

    # Sum indicators on right & bottom margins of 3x3 grid
    for r_idx in range(3):
        ry = gy0 + r_idx * ch + ch / 2.0 + 4.0
        body.append(txt(gx0 + 3 * cw + 12, ry, "→15", size=11.5, color=ORANGE, weight="700"))
    for c_idx in range(3):
        rcx = gx0 + c_idx * cw + cw / 2.0
        body.append(txt(rcx, gy0 + 3 * ch + 18, "↓15", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    body.append(txt(gx0 + 3 * cw + 12, gy0 - 8, "↙15", size=11.5, color=PURPLE, weight="700"))
    body.append(txt(gx0 + 3 * cw + 12, gy0 + 3 * ch + 18, "↘15", size=11.5, color=PURPLE, weight="700"))

    luoshu_yang_cnt = 0
    luoshu_yin_cnt = 0

    for r_idx in range(3):
        for c_idx in range(3):
            val = LUOSHU_GRID[r_idx][c_idx]
            is_yang = val % 2 == 1
            x0 = gx0 + c_idx * cw
            y0 = gy0 + r_idx * ch
            mcx = x0 + cw / 2.0
            mcy = y0 + ch / 2.0 + 7.0

            if val == 5:
                bg_cell, bd_cell = AMBER_SOFT, "#f59e0b"
            elif is_yang:
                bg_cell, bd_cell = BLUE_SOFT, "#93c5fd"
            else:
                bg_cell, bd_cell = "#f8fafc", BORDER

            body.append(
                f'<rect x="{x0 + 2:.1f}" y="{y0 + 2:.1f}" width="{cw - 4:.1f}" height="{ch - 4:.1f}" '
                f'rx="8" fill="{bg_cell}" stroke="{bd_cell}" stroke-width="1.3"/>'
            )
            tag_color = AMBER if val == 5 else (BLUE if is_yang else SLATE)
            parity_str = "中五○" if val == 5 else ("奇○" if is_yang else "偶●")
            body.append(txt(x0 + 9, y0 + 18, f"{val}", size=13, color=tag_color, weight="700"))
            body.append(txt(x0 + cw - 9, y0 + 17, parity_str, size=10.5, color=MUTED, anchor="end"))

            # Exact authentic knot pattern per digit 1..9
            chains = []
            if val == 1:
                chains = [[(mcx, mcy)]]
            elif val == 2:
                chains = [[(mcx - 8, mcy), (mcx + 8, mcy)]]
            elif val == 3:
                chains = [[(mcx, mcy - 13), (mcx, mcy), (mcx, mcy + 13)]]
            elif val == 4:
                chains = [
                    [(mcx - 8, mcy - 8), (mcx + 8, mcy - 8)],
                    [(mcx - 8, mcy + 8), (mcx + 8, mcy + 8)],
                ]
            elif val == 5:
                # 5-dot cross
                body.append(_line(mcx - 11, mcy, mcx + 11, mcy, color="#64748b", sw=1.5))
                body.append(_line(mcx, mcy - 11, mcx, mcy + 11, color="#64748b", sw=1.5))
                pts5 = [(mcx, mcy), (mcx - 11, mcy), (mcx + 11, mcy), (mcx, mcy - 11), (mcx, mcy + 11)]
                for px, py in pts5:
                    body.append(
                        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="#ffffff" '
                        f'stroke="{INK}" stroke-width="1.8"/>'
                    )
                luoshu_yang_cnt += 5
                continue
            elif val == 6:
                chains = [
                    [(mcx - 12, mcy - 7), (mcx, mcy - 7), (mcx + 12, mcy - 7)],
                    [(mcx - 12, mcy + 7), (mcx, mcy + 7), (mcx + 12, mcy + 7)],
                ]
            elif val == 7:
                chains = [
                    [(mcx - 11, mcy - 12), (mcx - 11, mcy), (mcx - 11, mcy + 12)],
                    [(mcx, mcy - 12)],
                    [(mcx + 11, mcy - 12), (mcx + 11, mcy), (mcx + 11, mcy + 12)],
                ]
                body.append(_line(mcx - 11, mcy - 12, mcx + 11, mcy - 12, color="#64748b", sw=1.5))
            elif val == 8:
                chains = [
                    [(mcx - 16.5 + k * 11.0, mcy - 7) for k in range(4)],
                    [(mcx - 16.5 + k * 11.0, mcy + 7) for k in range(4)],
                ]
            elif val == 9:
                chains = [
                    [(mcx - 13, mcy - 10), (mcx, mcy - 10), (mcx + 13, mcy - 10)],
                    [(mcx - 13, mcy), (mcx, mcy), (mcx + 13, mcy)],
                    [(mcx - 13, mcy + 10), (mcx, mcy + 10), (mcx + 13, mcy + 10)],
                ]

            cnt_cell = sum(len(ch_pts) for ch_pts in chains)
            assert cnt_cell == val
            if is_yang:
                luoshu_yang_cnt += cnt_cell
            else:
                luoshu_yin_cnt += cnt_cell

            for ch_pts in chains:
                body.append(_knot_chain(ch_pts, is_yang=is_yang, r=3.5))

    assert luoshu_yang_cnt == 25 and luoshu_yin_cnt == 20

    # Luoshu bottom summary strip
    body.append(
        f'<rect x="398" y="404" width="334" height="58" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    body.append(txt(410, 425, "口诀：戴九履一，左三右七，二四为肩，六八为足", size=11.5, color=INK, weight="600"))
    body.append(txt(410, 446, "阳居四正中五（和 25）· 阴居四角（和 20，总和 45）", size=11.5, color=BODY))

    write_svg(
        "hetu-luoshu",
        "hetu-luoshu-dot-blueprints.svg",
        figure(
            h,
            "河图（左，55点十数同余配对图）与洛书（右，45点三阶幻方九宫图）的绳结黑白点阵及数字对照图",
            "左图展示河图上南火2与7、下北水1与6、左东木3与8、右西金4与9、中宫土5与10的黑白点阵；右图展示洛书492、357、816九宫幻方黑白点阵，横竖斜8条线之和均为15。",
            body,
            extra_defs=_purple_marker_def(),
        ),
    )


def _build_hetu_mod5():
    """SVG 2: Mathematical structure of Hetu — mod 5 residue classes, +5 shift, and outer parity balance."""
    h = 456
    body = []
    body.extend(
        header(
            "河图的数理内核：模 5 同余（a ≡ b mod 5）与奇偶严格平分",
            "《系辞》“五位相得而各有合”用现代算术翻译：内圈生数 k 加上中宫 5，自动翻转奇偶生成外圈成数 k+5",
        )
    )

    # Left Card: Mod-5 mapping table
    body.append(card(16, 68, 378, 372))
    body.append(pill(28, 80, "规律一：模 5 同余映射器", fg=BLUE, bg=BLUE_SOFT, w=174, h=24))
    body.append(txt(212, 96, "成数 = 生数 + 5（奇偶必互补）", size=11.5, color=MUTED))

    rows_meta = [
        ("下北 · 水", BLUE, BLUE_SOFT, 1, "奇○", 6, "偶●", "余 1"),
        ("上南 · 火", CRIMSON, CRIMSON_SOFT, 2, "偶●", 7, "奇○", "余 2"),
        ("左东 · 木", GREEN, GREEN_SOFT, 3, "奇○", 8, "偶●", "余 3"),
        ("右西 · 金", AMBER, AMBER_SOFT, 4, "偶●", 9, "奇○", "余 4"),
        ("中宫 · 土", PURPLE, PURPLE_SOFT, 5, "奇○", 10, "偶●", "余 0"),
    ]

    # Column headers
    body.append(txt(64, 126, "方位五行", size=11.5, color=MUTED, anchor="middle", weight="600"))
    body.append(txt(154, 126, "内圈生数", size=11.5, color=MUTED, anchor="middle", weight="600"))
    body.append(txt(218, 126, "加中五", size=11.5, color=MUTED, anchor="middle", weight="600"))
    body.append(txt(284, 126, "外圈成数", size=11.5, color=MUTED, anchor="middle", weight="600"))
    body.append(txt(354, 126, "mod 5", size=11.5, color=MUTED, anchor="middle", weight="600"))

    for idx, (label, fg, bg, s_num, s_par, c_num, c_par, mod_str) in enumerate(rows_meta):
        ry = 140 + idx * 46
        body.append(pill(28, ry, label, fg=fg, bg=bg, w=76, h=30))
        body.append(
            f'<rect x="116" y="{ry}" width="74" height="30" rx="7" fill="#ffffff" stroke="{BORDER}"/>'
        )
        body.append(txt(153, ry + 20, f"{s_num} ({s_par})", size=12, color=INK, anchor="middle", weight="700"))

        body.append(_line(194, ry + 15, 240, ry + 15, color=ORANGE, sw=1.8, marker="arr-orange"))
        body.append(txt(217, ry + 10, "+5", size=11, color=ORANGE, anchor="middle", weight="700"))

        body.append(
            f'<rect x="246" y="{ry}" width="76" height="30" rx="7" fill="#ffffff" stroke="{BORDER}"/>'
        )
        body.append(txt(284, ry + 20, f"{c_num} ({c_par})", size=12, color=INK, anchor="middle", weight="700"))

        body.append(pill(330, ry + 3, mod_str, fg=SLATE, bg=SLATE_SOFT, w=52, h=24))

    body.append(
        f'<rect x="28" y="374" width="354" height="54" rx="8" fill="{ORANGE_SOFT}" stroke="#fdba74"/>'
    )
    body.append(txt(40, 395, "为什么每一方都恰好“一阴一阳”？", size=12, color=ORANGE, weight="700"))
    body.append(txt(40, 415, "因为 5 是奇数：奇数 + 5 = 偶数，偶数 + 5 = 奇数，绝无同性相斥！", size=11.5, color=BODY))

    # Right Card: Compass symmetry & Wuxing clockwise cycle
    body.append(card(408, 68, 336, 372))
    body.append(pill(420, 80, "规律二：外围奇偶恒等于 20", fg=GREEN, bg=GREEN_SOFT, w=186, h=24))
    body.append(txt(614, 96, "顺时针相生回路", size=11.5, color=MUTED))

    rcx, rcy = 576.0, 232.0
    # Clockwise Wuxing cycle circle
    body.append(
        f'<circle cx="{rcx:.1f}" cy="{rcy:.1f}" r="84" fill="none" stroke="#cbd5e1" '
        f'stroke-width="1.6" stroke-dasharray="5 4"/>'
    )

    # Nodes: South (top), West (right), North (bottom), East (left), Center
    # Clockwise arrows: North(bottom) -> East(left) -> South(top) -> Center -> West(right) -> North(bottom)
    body.append(
        f'<path d="M {rcx - 42:.1f} {rcy + 72:.1f} A 84 84 0 0 1 {rcx - 78:.1f} {rcy + 30:.1f}" '
        f'fill="none" stroke="{GREEN}" stroke-width="2" marker-end="url(#arr-green)"/>'
    )
    body.append(txt(rcx - 86, rcy + 62, "水生木", size=11, color=GREEN, anchor="middle", weight="600"))

    body.append(
        f'<path d="M {rcx - 78:.1f} {rcy - 30:.1f} A 84 84 0 0 1 {rcx - 42:.1f} {rcy - 72:.1f}" '
        f'fill="none" stroke="{CRIMSON}" stroke-width="2" marker-end="url(#arr-orange)"/>'
    )
    body.append(txt(rcx - 86, rcy - 54, "木生火", size=11, color=CRIMSON, anchor="middle", weight="600"))

    body.append(_line(rcx, rcy - 58, rcx, rcy - 26, color=AMBER, sw=2.0, marker="arr-orange"))
    body.append(txt(rcx + 28, rcy - 40, "火生土", size=11, color=AMBER, weight="600"))

    body.append(_line(rcx + 36, rcy, rcx + 50, rcy, color=AMBER, sw=2.0, marker="arr-orange"))

    body.append(
        f'<path d="M {rcx + 78:.1f} {rcy + 30:.1f} A 84 84 0 0 1 {rcx + 42:.1f} {rcy + 72:.1f}" '
        f'fill="none" stroke="{BLUE}" stroke-width="2" marker-end="url(#arr-blue)"/>'
    )
    body.append(txt(rcx + 88, rcy + 62, "金生水", size=11, color=BLUE, anchor="middle", weight="600"))

    # Five node boxes
    nodes = [
        (rcx, rcy - 84, "南火 2●·7○", CRIMSON, CRIMSON_SOFT),
        (rcx - 88, rcy, "东木 3○·8●", GREEN, GREEN_SOFT),
        (rcx, rcy, "中土 5·10", PURPLE, PURPLE_SOFT),
        (rcx + 88, rcy, "西金 4●·9○", AMBER, AMBER_SOFT),
        (rcx, rcy + 84, "北水 1○·6●", BLUE, BLUE_SOFT),
    ]
    for nx, ny, nlabel, nfg, nbg in nodes:
        bw = 88 if "中土" not in nlabel else 74
        body.append(pill(nx - bw / 2.0, ny - 14, nlabel, fg=nfg, bg=nbg, w=bw, h=28, size=11.5))

    body.append(txt(rcx + 48, rcy - 18, "土生金", size=11, color=AMBER, weight="600"))

    # Bottom symmetry box in Right Card
    body.append(
        f'<rect x="420" y="346" width="312" height="82" rx="8" fill="{GREEN_SOFT}" stroke="#86efac"/>'
    )
    body.append(txt(432, 367, "拿掉中宫（5 与 10）后，四方奇偶不偏不倚：", size=12, color=GREEN, weight="700"))
    body.append(txt(432, 389, "• 四方阳数和 = 1(北) + 7(南) + 3(东) + 9(西) = 20", size=11.5, color=INK))
    body.append(txt(432, 411, "• 四方阴数和 = 6(北) + 2(南) + 8(东) + 4(西) = 20", size=11.5, color=INK))

    write_svg(
        "hetu-luoshu",
        "hetu-mod5-wuxing-pairing.svg",
        figure(
            h,
            "河图的模5同余映射（成数=生数+5）与四方奇偶和等于20的对称结构图",
            "左面板展示北1与6、南2与7、东3与8、西4与9、中5与10按加5同余配对并自动翻转奇偶；右面板展示顺时针五行相生回路及外围奇偶和同为20。",
            body,
            extra_defs=_purple_marker_def(),
        ),
    )


def _build_luoshu_uniqueness():
    """SVG 3: Three-step mathematical uniqueness proof of the 3x3 Luoshu magic square."""
    h = 482
    body = []
    body.extend(
        header(
            "362,880 种填法里为什么只有“唯一”一个洛书？三步纯数学证明",
            "无需穷举试错：仅靠加法不变量与凑 15 频次统计，就能把中五、四正奇数、四维偶数全部锁死",
        )
    )

    # Step 1 Card (Left)
    body.append(card(16, 68, 234, 294))
    body.append(step_badge(36, 92, 1, fg=BLUE, bg=BLUE_SOFT))
    body.append(txt(56, 97, "定幻和与锁死中五", size=PANEL_TITLE, color=INK, weight="700"))

    body.append(
        f'<rect x="28" y="114" width="210" height="54" rx="8" fill="{BLUE_SOFT}" stroke="#93c5fd"/>'
    )
    body.append(txt(133, 134, "三行不重叠覆盖 1~9（总和 45）", size=11.5, color=BODY, anchor="middle"))
    body.append(txt(133, 155, "⇒ 每条线幻和 M = 45 ÷ 3 = 15", size=12, color=BLUE, anchor="middle", weight="700"))

    # Mini 3x3 grid with 4 lines piercing center c
    mcx, mcy = 133.0, 232.0
    gs = 34.0
    for r in range(3):
        for c in range(3):
            x0 = mcx - 1.5 * gs + c * gs
            y0 = mcy - 1.5 * gs + r * gs
            fill_c = AMBER_SOFT if (r == 1 and c == 1) else "#ffffff"
            body.append(
                f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{gs:.1f}" height="{gs:.1f}" '
                f'fill="{fill_c}" stroke="{BORDER}" stroke-width="1.2"/>'
            )
    # 4 lines piercing center
    body.append(_line(mcx - 56, mcy, mcx + 56, mcy, color=ORANGE, sw=2.0))
    body.append(_line(mcx, mcy - 56, mcx, mcy + 56, color=ORANGE, sw=2.0))
    body.append(_line(mcx - 52, mcy - 52, mcx + 52, mcy + 52, color=ORANGE, sw=2.0))
    body.append(_line(mcx - 52, mcy + 52, mcx + 52, mcy - 52, color=ORANGE, sw=2.0))
    body.append(
        f'<circle cx="{mcx:.1f}" cy="{mcy:.1f}" r="13" fill="{AMBER_SOFT}" stroke="#d97706" stroke-width="2"/>'
    )
    body.append(txt(mcx, mcy + 4.5, "c=5", size=11.5, color=AMBER, anchor="middle", weight="700"))

    body.append(txt(133, 308, "4 条过中心线之和 = 4×15 = 60", size=11.5, color=BODY, anchor="middle"))
    body.append(txt(133, 328, "全图 45 + 中心多算 3 次：45+3c=60", size=11.5, color=BODY, anchor="middle"))
    body.append(txt(133, 348, "⇒ 中心格唯一解 c = 5！", size=12, color=ORANGE, anchor="middle", weight="700"))

    # Step 2 Card (Middle)
    body.append(card(263, 68, 234, 294))
    body.append(step_badge(283, 92, 2, fg=PURPLE, bg=PURPLE_SOFT))
    body.append(txt(303, 97, "穷尽 8 组“三数和=15”", size=PANEL_TITLE, color=INK, weight="700"))

    triples_left = ["9 + 5 + 1", "9 + 4 + 2", "8 + 5 + 2", "8 + 6 + 1"]
    triples_right = ["8 + 4 + 3", "7 + 5 + 3", "7 + 6 + 2", "6 + 5 + 4"]
    for i in range(4):
        ry = 116 + i * 26
        body.append(pill(275, ry, triples_left[i], fg=BODY, bg=SLATE_SOFT, w=100, h=22, size=11.5))
        body.append(pill(385, ry, triples_right[i], fg=BODY, bg=SLATE_SOFT, w=100, h=22, size=11.5))

    body.append(
        f'<rect x="275" y="228" width="210" height="122" rx="8" fill="{PURPLE_SOFT}" stroke="#d8b4fe"/>'
    )
    body.append(txt(287, 249, "统计每个数字登场的线数：", size=12, color=PURPLE, weight="700"))
    body.append(txt(287, 272, "• 中五 {5}：登场 4 次（米字中心）", size=11.5, color=INK))
    body.append(txt(287, 295, "• 偶数 {2,4,6,8}：各登场 3 次！", size=11.5, color=GREEN, weight="700"))
    body.append(txt(287, 318, "• 奇数 {1,3,7,9}：各只登场 2 次！", size=11.5, color=CRIMSON, weight="700"))
    body.append(txt(287, 340, "（例：含 9 的组合仅 951、942 两组）", size=11, color=MUTED))

    # Step 3 Card (Right)
    body.append(card(510, 68, 234, 294))
    body.append(step_badge(530, 92, 3, fg=GREEN, bg=GREEN_SOFT))
    body.append(txt(550, 97, "线数对号入座即唯一", size=PANEL_TITLE, color=INK, weight="700"))

    rcx, rcy = 627.0, 196.0
    cs = 44.0
    role_grid = [
        [("角·3线", "必偶", GREEN_SOFT, GREEN), ("边·2线", "必奇", BLUE_SOFT, BLUE), ("角·3线", "必偶", GREEN_SOFT, GREEN)],
        [("边·2线", "必奇", BLUE_SOFT, BLUE), ("中·4线", "必 5", AMBER_SOFT, AMBER), ("边·2线", "必奇", BLUE_SOFT, BLUE)],
        [("角·3线", "必偶", GREEN_SOFT, GREEN), ("边·2线", "必奇", BLUE_SOFT, BLUE), ("角·3线", "必偶", GREEN_SOFT, GREEN)],
    ]
    for r in range(3):
        for c in range(3):
            t1, t2, bg_c, fg_c = role_grid[r][c]
            x0 = rcx - 1.5 * cs + c * cs
            y0 = rcy - 1.5 * cs + r * cs
            body.append(
                f'<rect x="{x0 + 1.5:.1f}" y="{y0 + 1.5:.1f}" width="{cs - 3:.1f}" height="{cs - 3:.1f}" '
                f'rx="6" fill="{bg_c}" stroke="{fg_c}" stroke-width="1.2"/>'
            )
            body.append(txt(x0 + cs / 2.0, y0 + 18, t1, size=10.5, color=BODY, anchor="middle"))
            body.append(txt(x0 + cs / 2.0, y0 + 34, t2, size=11.5, color=fg_c, anchor="middle", weight="700"))

    body.append(txt(522, 286, "• 角格横+竖+斜过 3 线 ⇒ 必填偶数", size=11.5, color=GREEN, weight="600"))
    body.append(txt(522, 308, "• 边格仅横+竖过 2 线 ⇒ 必填奇数", size=11.5, color=BLUE, weight="600"))
    body.append(txt(522, 330, "• “阳居四正、阴居四维”并非玄学，", size=11.5, color=BODY))
    body.append(txt(522, 348, "  而是线性方程组唯一允许的解！", size=11.5, color=INK, weight="700"))

    # Bottom Card: D4 Symmetry Equivalence Class (8 solutions = 1 Luoshu)
    body.append(card(16, 374, 728, 92))
    body.append(pill(28, 386, "结论：9! = 362,880 种填法中仅 8 解", fg=ORANGE, bg=ORANGE_SOFT, w=216, h=24))
    body.append(
        txt(
            254,
            402,
            "这 8 个解在正方形二面体群 D₄（4 次旋转 × 2 次镜像翻转）下完全同构，本质只有 1 个洛书！",
            size=11.5,
            color=INK,
            weight="600",
        )
    )
    body.append(
        txt(
            28,
            430,
            "• 为什么古籍有两种写法？《大戴礼记·明堂》记作“2 9 4 / 7 5 3 / 6 1 8”，朱熹《周易本义》画作“4 9 2 / 3 5 7 / 8 1 6”：",
            size=11.5,
            color=BODY,
        )
    )
    body.append(
        txt(
            28,
            451,
            "  两者只是左右镜像（人面南而坐时的自身左右 vs 读者看图时的纸面左右），在群论里属于同一个对称轨道。",
            size=11.5,
            color=MUTED,
        )
    )

    write_svg(
        "hetu-luoshu",
        "luoshu-uniqueness-proof.svg",
        figure(
            h,
            "三阶幻方（洛书）在362,880种排列中唯一性的三步数学证明与D4对称群说明图",
            "第一步由4条中心线和60=45+3c推出中心必为5；第二步列出全部8组和为15的三元组，偶数各出现3次、奇数各出现2次；第三步对照角格过3线、边格过2线锁死奇偶位置，在D4群8种对称下唯一。",
            body,
            extra_defs=_purple_marker_def(),
        ),
    )


def _build_yang_hui_algorithm():
    """SVG 4: Yang Hui's 1275 16-character construction with 4 static steps + 1-shot accessible CSS animation."""
    h = 482
    anim_css = """
      @keyframes yh-t1 {
        0%, 18%   { transform: translate(0px, -116px); }
        31%       { transform: translate(-18px, -58px); }
        44%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes yh-t9 {
        0%, 18%   { transform: translate(0px, 116px); }
        31%       { transform: translate(18px, 58px); }
        44%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes yh-t7 {
        0%, 44%   { transform: translate(-116px, 0px); }
        57%       { transform: translate(-58px, -18px); }
        70%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes yh-t3 {
        0%, 44%   { transform: translate(116px, 0px); }
        57%       { transform: translate(58px, 18px); }
        70%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes yh-t4 {
        0%, 70%   { transform: translate(14px, 14px); }
        88%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes yh-t2 {
        0%, 70%   { transform: translate(-14px, 14px); }
        88%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes yh-t8 {
        0%, 70%   { transform: translate(14px, -14px); }
        88%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes yh-t6 {
        0%, 70%   { transform: translate(-14px, -14px); }
        88%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes yh-grid-fade {
        0%, 76%   { opacity: 0.15; }
        92%, 100% { opacity: 1; }
      }
      .yh-1 { animation: yh-t1 8s ease-in-out 0.4s 1 forwards; }
      .yh-9 { animation: yh-t9 8s ease-in-out 0.4s 1 forwards; }
      .yh-7 { animation: yh-t7 8s ease-in-out 0.4s 1 forwards; }
      .yh-3 { animation: yh-t3 8s ease-in-out 0.4s 1 forwards; }
      .yh-4 { animation: yh-t4 8s ease-in-out 0.4s 1 forwards; }
      .yh-2 { animation: yh-t2 8s ease-in-out 0.4s 1 forwards; }
      .yh-8 { animation: yh-t8 8s ease-in-out 0.4s 1 forwards; }
      .yh-6 { animation: yh-t6 8s ease-in-out 0.4s 1 forwards; }
      .yh-done { animation: yh-grid-fade 8s ease-in-out 0.4s 1 forwards; }
      @media (prefers-reduced-motion: reduce) {
        .yh-1, .yh-9, .yh-7, .yh-3, .yh-4, .yh-2, .yh-8, .yh-6, .yh-done {
          animation: none !important;
          transform: none !important;
          opacity: 1 !important;
        }
      }
    """

    body = []
    body.extend(
        header(
            "南宋杨辉十六字构造术：四步把 1~9 排成洛书（1275《续古摘奇算法》）",
            "“九子斜排，上下对易，左右相更，四维挺出”——左侧保留完整静态四步，右侧单次动画自动归位定格",
        )
    )

    # Left 2x2 static step cards (x=16..464, y=68..466)
    mini_cards = [
        (16, 68, 1, "九子斜排", "按 45° 斜行依次写 1~9", BLUE, BLUE_SOFT),
        (244, 68, 2, "上下对易", "顶角 1 与底角 9 互换", ORANGE, ORANGE_SOFT),
        (16, 272, 3, "左右相更", "左角 7 与右角 3 互换", PURPLE, PURPLE_SOFT),
        (244, 272, 4, "四维挺出", "4、2、8、6 推出四角成方", GREEN, GREEN_SOFT),
    ]
    for cx0, cy0, s_num, s_title, s_sub, s_col, s_bg in mini_cards:
        body.append(card(cx0, cy0, 218, 194))
        body.append(step_badge(cx0 + 20, cy0 + 21, s_num, fg=s_col, bg=s_bg))
        body.append(txt(cx0 + 38, cy0 + 25, s_title, size=13, color=INK, weight="700"))
        body.append(txt(cx0 + 16, cy0 + 45, s_sub, size=11, color=MUTED))

    def _mini_node(x, y, val, fg=INK, bg="#ffffff", bd=BORDER):
        return (
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11.0" fill="{bg}" stroke="{bd}" stroke-width="1.4"/>'
            + txt(x, y + 4.0, str(val), size=11.5, color=fg, anchor="middle", weight="700")
        )

    # Mini Step 1: 45-deg diamond (shifted down cleanly clear of subtitle)
    m1x, m1y, md = 125.0, 182.0, 22.0
    # 3 diagonal guide lines: (1-2-3), (4-5-6), (7-8-9)
    body.append(_line(m1x, m1y - 2 * md, m1x + 2 * md, m1y, color="#93c5fd", sw=1.4, dash="3 2"))
    body.append(_line(m1x - md, m1y - md, m1x + md, m1y + md, color="#93c5fd", sw=1.4, dash="3 2"))
    body.append(_line(m1x - 2 * md, m1y, m1x, m1y + 2 * md, color="#93c5fd", sw=1.4, dash="3 2"))
    s1_pts = [
        (0, -2, 1), (-1, -1, 4), (1, -1, 2),
        (-2, 0, 7), (0, 0, 5), (2, 0, 3),
        (-1, 1, 8), (1, 1, 6), (0, 2, 9),
    ]
    for du, dv, v in s1_pts:
        body.append(_mini_node(m1x + du * md, m1y + dv * md, v, fg=BLUE if v in (1, 2, 3) else INK))

    # Mini Step 2: Swap 1 <-> 9
    m2x, m2y = 353.0, 182.0
    s2_pts = [
        (0, -1.6, 9, True), (-1, -1, 4, False), (1, -1, 2, False),
        (-2, 0, 7, False), (0, 0, 5, False), (2, 0, 3, False),
        (-1, 1, 8, False), (1, 1, 6, False), (0, 1.6, 1, True),
    ]
    body.append(
        f'<path d="M {m2x + 14:.1f} {m2y - 34:.1f} Q {m2x + 33:.1f} {m2y:.1f} {m2x + 14:.1f} {m2y + 34:.1f}" '
        f'fill="none" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>'
    )
    body.append(
        f'<path d="M {m2x - 14:.1f} {m2y + 34:.1f} Q {m2x - 33:.1f} {m2y:.1f} {m2x - 14:.1f} {m2y - 34:.1f}" '
        f'fill="none" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>'
    )
    for du, dv, v, hi in s2_pts:
        body.append(
            _mini_node(
                m2x + du * md,
                m2y + dv * md,
                v,
                fg=ORANGE if hi else INK,
                bg=ORANGE_SOFT if hi else "#ffffff",
                bd=ORANGE if hi else BORDER,
            )
        )

    # Mini Step 3: Swap 7 <-> 3
    m3x, m3y = 125.0, 386.0
    s3_pts = [
        (0, -1.5, 9, False), (-1, -1, 4, False), (1, -1, 2, False),
        (-1.5, 0, 3, True), (0, 0, 5, False), (1.5, 0, 7, True),
        (-1, 1, 8, False), (1, 1, 6, False), (0, 1.5, 1, False),
    ]
    body.append(
        f'<path d="M {m3x - 30:.1f} {m3y - 13:.1f} Q {m3x:.1f} {m3y - 29:.1f} {m3x + 30:.1f} {m3y - 13:.1f}" '
        f'fill="none" stroke="{PURPLE}" stroke-width="1.6" marker-end="url(#arr-purple)"/>'
    )
    body.append(
        f'<path d="M {m3x + 30:.1f} {m3y + 13:.1f} Q {m3x:.1f} {m3y + 29:.1f} {m3x - 30:.1f} {m3y + 13:.1f}" '
        f'fill="none" stroke="{PURPLE}" stroke-width="1.6" marker-end="url(#arr-purple)"/>'
    )
    for du, dv, v, hi in s3_pts:
        body.append(
            _mini_node(
                m3x + du * md,
                m3y + dv * md,
                v,
                fg=PURPLE if hi else INK,
                bg=PURPLE_SOFT if hi else "#ffffff",
                bd=PURPLE if hi else BORDER,
            )
        )

    # Mini Step 4: Push 4,2,8,6 out to square corners
    m4x, m4y, ms = 353.0, 386.0, 33.0
    body.append(
        f'<rect x="{m4x - 1.5 * ms:.1f}" y="{m4y - 1.5 * ms:.1f}" width="{3 * ms:.1f}" height="{3 * ms:.1f}" '
        f'rx="8" fill="{GREEN_SOFT}" stroke="#86efac" stroke-width="1.3"/>'
    )
    for r in range(3):
        for c in range(3):
            v = LUOSHU_GRID[r][c]
            hi = v in (4, 2, 8, 6)
            nx = m4x + (c - 1) * ms
            ny = m4y + (r - 1) * ms
            body.append(
                _mini_node(
                    nx,
                    ny,
                    v,
                    fg=GREEN if hi else INK,
                    bg="#ffffff",
                    bd=GREEN if hi else BORDER,
                )
            )

    # Right Animated Stage Card (x=476..744, y=68..466)
    body.append(card(476, 68, 268, 398))
    body.append(pill(488, 80, "单次归位演示 · 终态定格", fg=GREEN, bg=GREEN_SOFT, w=178, h=24))
    body.append(txt(488, 122, "浅色虚线为初始 45° 斜排菱形：", size=11.5, color=MUTED))

    acx, acy, astep = 610.0, 262.0, 48.0
    # Static ghost diamond showing initial 九子斜排 envelope (d = 34px, apex at ±68px)
    body.append(
        f'<polygon points="{acx:.1f},{acy - 68:.1f} {acx + 68:.1f},{acy:.1f} '
        f'{acx:.1f},{acy + 68:.1f} {acx - 68:.1f},{acy:.1f}" '
        f'fill="none" stroke="#cbd5e1" stroke-width="1.4" stroke-dasharray="4 4"/>'
    )

    # Final 3x3 grid frame & =15 badges (fade to full opacity as tiles lock)
    grid_grp = [
        f'<g class="yh-done">',
        f'<rect x="{acx - 1.5 * astep:.1f}" y="{acy - 1.5 * astep:.1f}" '
        f'width="{3 * astep:.1f}" height="{3 * astep:.1f}" rx="10" fill="none" stroke="{GREEN}" stroke-width="1.8"/>',
    ]
    for k in (-0.5, 0.5):
        grid_grp.append(_line(acx - 1.5 * astep, acy + k * astep, acx + 1.5 * astep, acy + k * astep, color="#bbf7d0", sw=1.2))
        grid_grp.append(_line(acx + k * astep, acy - 1.5 * astep, acx + k * astep, acy + 1.5 * astep, color="#bbf7d0", sw=1.2))
    for r in (-1, 0, 1):
        grid_grp.append(txt(acx + 1.5 * astep + 8, acy + r * astep + 4, "=15", size=11, color=GREEN, weight="700"))
    grid_grp.append("</g>")
    body.append("\n  ".join(grid_grp))

    # Render the 9 tiles at their FINAL 3x3 coordinates (so reduced-motion & final state are 100% accurate!)
    for r in range(3):
        for c in range(3):
            v = LUOSHU_GRID[r][c]
            tx = acx + (c - 1) * astep
            ty = acy + (r - 1) * astep
            cls_attr = f' class="yh-{v}"' if v != 5 else ""
            if v == 5:
                bg_t, bd_t, fg_t = AMBER_SOFT, "#d97706", AMBER
            elif v in (1, 9):
                bg_t, bd_t, fg_t = ORANGE_SOFT, ORANGE, ORANGE
            elif v in (3, 7):
                bg_t, bd_t, fg_t = PURPLE_SOFT, PURPLE, PURPLE
            else:
                bg_t, bd_t, fg_t = GREEN_SOFT, GREEN, GREEN

            body.append(
                f'<g{cls_attr}>'
                f'<rect x="{tx - 17:.1f}" y="{ty - 17:.1f}" width="34" height="34" rx="8" '
                f'fill="{bg_t}" stroke="{bd_t}" stroke-width="1.6"/>'
                + txt(tx, ty + 5, str(v), size=14, color=fg_t, anchor="middle", weight="700")
                + "</g>"
            )

    body.append(
        f'<rect x="488" y="372" width="244" height="74" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    body.append(txt(500, 393, "几何真相：为什么叫“四维挺出”？", size=11.5, color=INK, weight="700"))
    body.append(txt(500, 413, "斜排菱形里 4,2,8,6 距中心仅 48/√2≈34，", size=11, color=BODY))
    body.append(txt(500, 432, "向外推出 14 像素才与边中点齐平！", size=11, color=GREEN, weight="600"))

    write_svg(
        "hetu-luoshu",
        "yang-hui-jiuzi-xiepai.svg",
        figure(
            h,
            "南宋杨辉《续古摘奇算法》九子斜排四步构造洛书幻方的分步图解与单次归位动画",
            "左侧四格静态展示①九子斜排、②上下对易(1与9换)、③左右相更(7与3换)、④四维挺出(4,2,8,6推出四角)；右侧演示同一变换并停留在492/357/816终态，支持减少动态效果。",
            body,
            extra_css=anim_css,
            extra_defs=_purple_marker_def(),
        ),
    )


def _build_fifteen_game_and_squares():
    """SVG 5: Game isomorphism ('Pick-3-to-Sum-15' == Tic-Tac-Toe on Luoshu) & Square-Sum Magic."""
    h = 460
    body = []
    body.extend(
        header(
            "洛书的两大隐藏彩蛋：“凑 15 纸牌博弈”同构井字棋 & 平方和惊人守恒",
            "换个视角看幻方：心算抢牌瞬间降维成三子连线；连把每行数字正读、倒读求平方和都分毫不差",
        )
    )

    # Left Card: Pick-15 Game == Tic-Tac-Toe
    body.append(card(16, 68, 358, 376))
    body.append(pill(28, 80, "彩蛋一：“抢 15” = 洛书井字棋", fg=BLUE, bg=BLUE_SOFT, w=202, h=24))
    body.append(txt(28, 121, "规则：9 张牌 1~9 轮流拿，谁先凑齐任意三张和=15 获胜", size=11.5, color=BODY))

    # 9 cards strip at top of left card: A={5,4,2} (Blue ●), B={1,6} (Orange ×)
    a_cards = {5, 4, 2}
    b_cards = {1, 6}
    for idx, num in enumerate(range(1, 10)):
        kx = 28 + idx * 37.5
        ky = 134
        if num in a_cards:
            bg_k, bd_k, fg_k, mk_s = BLUE_SOFT, BLUE, BLUE, "先●"
        elif num in b_cards:
            bg_k, bd_k, fg_k, mk_s = ORANGE_SOFT, ORANGE, ORANGE, "后×"
        else:
            bg_k, bd_k, fg_k, mk_s = "#ffffff", BORDER, BODY, "空"
        body.append(
            f'<rect x="{kx:.1f}" y="{ky}" width="33" height="40" rx="6" fill="{bg_k}" stroke="{bd_k}" stroke-width="1.3"/>'
        )
        body.append(txt(kx + 16.5, ky + 17, str(num), size=12.5, color=fg_k, anchor="middle", weight="700"))
        body.append(txt(kx + 16.5, ky + 33, mk_s, size=9.5, color=fg_k if mk_s != "空" else MUTED, anchor="middle"))

    # Luoshu Tic-Tac-Toe board below
    bx0, by0, bs = 64.0, 192.0, 56.0
    for r in range(3):
        for c in range(3):
            v = LUOSHU_GRID[r][c]
            x0 = bx0 + c * bs
            y0 = by0 + r * bs
            if v in a_cards:
                bg_b, bd_b = BLUE_SOFT, BLUE
            elif v in b_cards:
                bg_b, bd_b = ORANGE_SOFT, ORANGE
            elif v in (9, 8):
                bg_b, bd_b = GREEN_SOFT, GREEN
            else:
                bg_b, bd_b = "#ffffff", BORDER

            body.append(
                f'<rect x="{x0 + 2:.1f}" y="{y0 + 2:.1f}" width="{bs - 4:.1f}" height="{bs - 4:.1f}" '
                f'rx="8" fill="{bg_b}" stroke="{bd_b}" stroke-width="1.4"/>'
            )
            body.append(txt(x0 + 11, y0 + 17, str(v), size=11.5, color=MUTED, weight="700"))
            if v in a_cards:
                body.append(
                    f'<circle cx="{x0 + bs / 2:.1f}" cy="{y0 + bs / 2 + 5:.1f}" r="11" '
                    f'fill="none" stroke="{BLUE}" stroke-width="2.6"/>'
                )
            elif v in b_cards:
                cxm, cym = x0 + bs / 2.0, y0 + bs / 2.0 + 5.0
                body.append(_line(cxm - 9, cym - 9, cxm + 9, cym + 9, color=ORANGE, sw=2.6))
                body.append(_line(cxm + 9, cym - 9, cxm - 9, cym + 9, color=ORANGE, sw=2.6))
            elif v in (9, 8):
                body.append(txt(x0 + bs / 2.0, y0 + bs / 2.0 + 9, "双杀!", size=11, color=GREEN, anchor="middle", weight="700"))

    # Highlight the 2 simultaneous winning lines for A: top row (4-9-2) and anti-diag (2-5-8)
    body.append(_line(bx0 + 10, by0 + bs / 2.0, bx0 + 3 * bs - 10, by0 + bs / 2.0, color=GREEN, sw=1.8, dash="4 3"))
    body.append(_line(bx0 + 2.7 * bs, by0 + 0.3 * bs, bx0 + 0.3 * bs, by0 + 2.7 * bs, color=GREEN, sw=1.8, dash="4 3"))

    # Explanation beside the board
    body.append(txt(244, 212, "同构揭秘：", size=12.5, color=INK, weight="700"))
    body.append(txt(244, 234, "先手●拿 {5, 4, 2}", size=11.5, color=BLUE, weight="700"))
    body.append(txt(244, 254, "后手×拿 {1, 6} 堵斜线", size=11.5, color=ORANGE, weight="600"))
    body.append(txt(244, 280, "此时●同时听两张牌：", size=11.5, color=BODY))
    body.append(txt(244, 300, "• 顶行 4+2+9 = 15", size=11.5, color=GREEN, weight="700"))
    body.append(txt(244, 320, "• 斜线 2+5+8 = 15", size=11.5, color=GREEN, weight="700"))
    body.append(txt(244, 344, "后手堵不住双杀必败！", size=11.5, color=INK, weight="600"))

    body.append(
        f'<rect x="28" y="372" width="334" height="58" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    body.append(txt(40, 393, "数学同构（Isomorphism）：8 组和为 15 的三元数组", size=11.5, color=INK, weight="700"))
    body.append(txt(40, 414, "一一对应井字棋 8 条连线；双方最优策略必成平局！", size=11.5, color=BODY))

    # Right Card: Square-Sum & Reversed-3-Digit Magic
    body.append(card(386, 68, 358, 376))
    body.append(pill(398, 80, "彩蛋二：平方和与正反三位数恒等", fg=PURPLE, bg=PURPLE_SOFT, w=216, h=24))
    body.append(txt(398, 121, "洛书不仅一次方和 = 15，连二次方和也暗藏精妙对称：", size=11.5, color=BODY))

    # Identity Box 1: Top row vs Bottom row squares = 101
    body.append(
        f'<rect x="398" y="136" width="334" height="68" rx="8" fill="{BLUE_SOFT}" stroke="#93c5fd"/>'
    )
    body.append(txt(410, 157, "① 顶行平方和 ＝ 底行平方和 ＝ 101", size=12, color=BLUE, weight="700"))
    body.append(txt(410, 179, "4² + 9² + 2² = 16 + 81 + 4 = 101", size=11.5, color=INK))
    body.append(txt(410, 196, "8² + 1² + 6² = 64 +  1 + 36 = 101", size=11.5, color=INK))

    # Identity Box 2: Left col vs Right col squares = 89
    body.append(
        f'<rect x="398" y="214" width="334" height="68" rx="8" fill="{GREEN_SOFT}" stroke="#86efac"/>'
    )
    body.append(txt(410, 235, "② 左列平方和 ＝ 右列平方和 ＝ 89", size=12, color=GREEN, weight="700"))
    body.append(txt(410, 257, "4² + 3² + 8² = 16 +  9 + 64 = 89", size=11.5, color=INK))
    body.append(txt(410, 274, "2² + 7² + 6² =  4 + 49 + 36 = 89", size=11.5, color=INK))

    # Identity Box 3: 3-digit concatenation forward vs backward!
    body.append(
        f'<rect x="398" y="292" width="334" height="72" rx="8" fill="{PURPLE_SOFT}" stroke="#d8b4fe"/>'
    )
    body.append(txt(410, 313, "③ 把三行连成三位数，正着读 vs 倒着读平方和相等！", size=12, color=PURPLE, weight="700"))
    body.append(txt(410, 335, "正读：492² + 357² + 816² = 1,035,369", size=11.5, color=INK, weight="600"))
    body.append(txt(410, 354, "倒读：294² + 753² + 618² = 1,035,369", size=11.5, color=INK, weight="600"))

    body.append(
        f'<rect x="398" y="372" width="334" height="58" rx="8" fill="{AMBER_SOFT}" stroke="#fcd34d"/>'
    )
    body.append(txt(410, 393, "为什么不是巧合？", size=11.5, color=AMBER, weight="700"))
    body.append(txt(410, 414, "因为每对中心对称格满足 a + a' = 10，展开二次项恰好对消！", size=11.5, color=BODY))

    write_svg(
        "hetu-luoshu",
        "luoshu-fifteen-game-tictactoe.svg",
        figure(
            h,
            "洛书幻方与抢15纸牌博弈的井字棋同构及行平方和、正反三位数平方和恒等式图解",
            "左面板展示从1至9轮流抽牌凑15等价于在洛书上玩井字棋（先手拿5,4,2形成9与8双杀）；右面板验证顶底行平方和均为101、左右列平方和均为89，且492²+357²+816²=294²+753²+618²=1,035,369。",
            body,
            extra_defs=_purple_marker_def(),
        ),
    )


def _build_history_timeline():
    """SVG 6: Evidence-graded 5-stage historical & archaeological timeline of Hetu and Luoshu."""
    h = 492
    body = []
    body.extend(
        header(
            "河图洛书三千年证据链全史：考古实物、先秦文献与宋代“名字大对调”",
            "严格区分“新石器宇宙观假说 → 先秦礼器文献 → 西汉出土九宫铁证 → 宋儒黑白点重构”四级史料",
        )
    )
    body.append(card(16, 68, 728, 408))

    # Vertical spine at x = 118
    spine_x = 118.0
    body.append(_line(spine_x, 96, spine_x, 444, color="#94a3b8", sw=2.4))

    stages = [
        (
            106,
            "约前 3300 年",
            "新石器假说·谨慎界定",
            AMBER,
            AMBER_SOFT,
            "安徽含山凌家滩出土“玉龟 + 八角星纹玉版”",
            "证实 5300 年前已有“天圆地方、八方中宫”宇宙观；但玉版无 1~9/1~10 数字，属思想前驱假说。",
        ),
        (
            184,
            "西周至战国",
            "先秦文献·礼器与数理",
            BLUE,
            BLUE_SOFT,
            "《尚书·顾命》“河图在东序”·《周易·系辞》“河出图，洛出书”",
            "西周将“河图”与大玉并列东序（礼器/古图籍）；《系辞》载“天地之数五十五”，尚无黑白点图。",
        ),
        (
            262,
            "公元前 173 年",
            "考古铁证·最早幻方",
            GREEN,
            GREEN_SOFT,
            "1977 阜阳西汉汝阴侯墓出土“太乙九宫占盘” + 《大戴礼记·明堂》",
            "占盘按九宫刻戴九履一、左三右七、二四为肩、六八为足；《明堂》载 294/753/618，系最早实物铁证！",
        ),
        (
            340,
            "北宋 → 南宋",
            "黑白点与名字大对调",
            ORANGE,
            ORANGE_SOFT,
            "刘牧《易数钩隐图》（九河十洛）→ 朱熹《周易本义》（1177，十河九洛）",
            "北宋刘牧首创黑白连珠图却以九宫为河图；南宋朱熹、蔡元定对调为“十河九洛”；1275 杨辉创纵横图数学。",
        ),
        (
            418,
            "清代考据至今",
            "辨伪祛魅与数学新生",
            PURPLE,
            PURPLE_SOFT,
            "黄宗羲、胡渭《易图明辨》（1706）考辨源流 → 现代组合与群论",
            "清儒考证黑白点图系宋儒据《系辞》与九宫重构；剥去神学外衣后，模 5 同余与幻方结构成数学史瑰宝。",
        ),
    ]

    for cy_s, era_str, grade_tag, fg, bg, title_s, desc_s in stages:
        # Era label on left of spine
        body.append(txt(spine_x - 14, cy_s + 5, era_str, size=11.5, color=fg, anchor="end", weight="700"))
        # Node dot on spine
        body.append(
            f'<circle cx="{spine_x:.1f}" cy="{cy_s:.1f}" r="6.5" fill="{fg}" stroke="#ffffff" stroke-width="2"/>'
        )
        # Content box on right of spine (x=136..732, width=596, height=66)
        by_box = cy_s - 22
        body.append(
            f'<rect x="136" y="{by_box:.1f}" width="596" height="66" rx="8" fill="{bg}" stroke="{BORDER}"/>'
        )
        body.append(pill(146, by_box + 8, grade_tag, fg=fg, bg="#ffffff", w=136, h=21, size=10.5))
        body.append(txt(292, by_box + 23, title_s, size=11.5, color=INK, weight="700"))
        body.append(txt(146, by_box + 49, desc_s, size=11, color=BODY))

    write_svg(
        "hetu-luoshu",
        "history-archaeology-timeline.svg",
        figure(
            h,
            "河图洛书三千年历史与考古证据分级时间轴（从凌家滩假说、阜阳汉墓太乙九宫占盘到宋代刘牧朱熹易名）",
            "按证据等级排列五个阶段：前3300年凌家滩玉龟玉版思想假说、先秦尚书与周易文献、前173年阜阳西汉太乙九宫占盘实物铁证、宋代刘牧首绘黑白点与朱熹对调十河九洛、清代胡渭考辨及现代数学。",
            body,
            extra_defs=_purple_marker_def(),
        ),
    )


@register("hetu-luoshu", "Hetu & Luoshu dot blueprints, mod-5 & magic-square math, Yang Hui animation, and timeline", "humanities")
def build_hetu_luoshu():
    _verify_hetu_luoshu_math()
    _build_dot_blueprints()
    _build_hetu_mod5()
    _build_luoshu_uniqueness()
    _build_yang_hui_algorithm()
    _build_fifteen_game_and_squares()
    _build_history_timeline()
