"""Algebra, Number Theory, Set Theory & Theory of Computation visual builders."""

import cmath
import math
from pathlib import Path
from fractions import Fraction
from itertools import permutations
import xml.etree.ElementTree as ET
from itertools import combinations
import itertools
from html import escape
from math import exp, hypot
from xml.etree import ElementTree as ET

from .core import (
    BG,
    BLUE,
    BLUE_LINE,
    BLUE_SOFT,
    BODY,
    BORDER,
    CARD_BG,
    DISP_SCALE,
    GREEN,
    GREEN_SOFT,
    HAIRLINE,
    IMAGES_ROOT,
    INK,
    K_BLUE,
    K_GOLD,
    K_INK,
    K_MUTED,
    K_ORANGE,
    K_RED,
    LABEL_SIZE,
    MUTED,
    NOTE_SIZE,
    ORANGE,
    ORANGE_SOFT,
    PANEL_TITLE,
    PURPLE,
    PURPLE_SOFT,
    REPO_ROOT,
    SLATE,
    SLATE_SOFT,
    SUB_SIZE,
    TITLE_SIZE,
    WIDTH,
    b_document,
    card,
    figure,
    header,
    k_dot,
    k_line,
    k_panel,
    k_path,
    k_save,
    k_text,
    pill,
    register,
    step_badge,
    txt,
)


@register("gauss", "高斯：配对求和、同余循环、正十七边形与最小二乘", "algebra_logic")
def build_gauss():
    OUT = REPO_ROOT / "assets" / "images" / "gauss"

    def pairing():
        n = 10
        pairs = [(i, n + 1 - i) for i in range(1, n // 2 + 1)]
        assert all(a + b == n + 1 for a, b in pairs)
        assert len(pairs) * (n + 1) == sum(range(1, n + 1)) == 55
        assert 50 * 101 == sum(range(1, 101)) == 5050
        assert 5 * 6 // 2 == sum(range(1, 6)) == 15

        els = header(
            "求和不用硬加：头尾配对，或倒扣成整块长方形",
            "左：偶数项头尾配成 5 对；右：奇数项（1 到 5）复制一份倒扣，拼成 5×6 长方形再除以 2。",
        )

        # Left card: 1..10 head-tail arcs
        els.append(card(20, 64, 386, 256))
        els.append(step_badge(38, 84, 1))
        els.append(txt(55, 88, "偶数项：1 到 10 头尾配成 5 对，每对都是 11", 13, INK, weight="600"))

        x0, y0, cell, gap = 36, 106, 29, 6
        for i in range(1, n + 1):
            x = x0 + (i - 1) * (cell + gap)
            left_half = i <= 5
            els.append(
                f'<rect x="{x}" y="{y0}" width="{cell}" height="{cell}" rx="6" '
                f'fill="{BLUE_SOFT if left_half else ORANGE_SOFT}" '
                f'stroke="{BLUE if left_half else ORANGE}" stroke-width="1.2"/>'
            )
            els.append(txt(x + cell / 2, y0 + 19.5, i, 13, INK, "middle", weight="600"))

        for idx, (a, b) in enumerate(pairs):
            xa = x0 + (a - 1) * (cell + gap) + cell / 2
            xb = x0 + (b - 1) * (cell + gap) + cell / 2
            top = y0 + cell + 4
            depth = 18 + (4 - idx) * 23
            els.append(
                f'<path d="M{xa:.1f},{top} C{xa:.1f},{top + depth:.1f} {xb:.1f},{top + depth:.1f} {xb:.1f},{top}" '
                f'fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-opacity="0.82"/>'
            )
            els.append(
                txt((xa + xb) / 2, top + depth * 0.75 + 11, f"{a}+{b}=11", 11, BLUE, "middle", halo=True)
            )

        els.append(txt(36, 298, "5 对 × 11 = 55；同理 1 到 100 是 50 对 × 101 = 5050", 12, MUTED))

        # Right card: 1..5 staircase + inverted staircase = 5 x 6 rectangle
        els.append(card(420, 64, 320, 256))
        els.append(step_badge(438, 84, 2, fg=ORANGE, bg=ORANGE_SOFT))
        els.append(txt(455, 88, "奇数项怎么办？复制一份倒扣成矩形", 13, INK, weight="600"))

        gx, gy, s = 486, 114, 24
        for r in range(5):  # row 0..4: blue has r+1 blocks, orange has 5-r blocks -> total 6 cols
            blue_cnt = r + 1
            for c in range(6):
                cx = gx + c * s
                cy = gy + r * s
                is_blue = c < blue_cnt
                els.append(
                    f'<rect x="{cx}" y="{cy}" width="{s - 2}" height="{s - 2}" rx="4" '
                    f'fill="{BLUE_SOFT if is_blue else ORANGE_SOFT}" '
                    f'stroke="{BLUE if is_blue else ORANGE}" stroke-width="1.1" '
                    f'{"stroke-dasharray=\"3 2\"" if not is_blue else ""}/>'
                )
        # Dimension annotations
        els.append(txt(gx + 3 * s, gy + 5 * s + 17, "宽 = n + 1 = 6 格", 12, INK, "middle", weight="600"))
        els.append(txt(gx - 10, gy + 2.5 * s + 4, "高 n=5", 12, INK, "end", weight="600"))
        els.append(pill(444, 260, "蓝色原和 = 15", fg=BLUE, bg=BLUE_SOFT, w=122, h=22, size=11.5))
        els.append(pill(578, 260, "虚线倒扣 = 15", fg=ORANGE, bg=ORANGE_SOFT, w=122, h=22, size=11.5))
        els.append(txt(444, 300, "总面积 5×6 = 30，分一半就是 1+2+3+4+5 = 15", 12, MUTED))

        return figure(
            338,
            "高斯配对求和与阶梯拼矩形",
            "左侧把1到10头尾配成5对，每对11，总和55；右侧把1到5的阶梯复制一份倒扣，拼成5乘6矩形，说明无论奇偶都有1+…+n=n(n+1)/2。",
            els,
        )

    def clock():
        m = 7
        assert 100 % m == 2
        assert pow(2, 1, m) == 2 and pow(2, 2, m) == 4 and pow(2, 3, m) == 1
        assert 100 == 3 * 33 + 1 and pow(2, 100, m) == 2

        els = header(
            "同余的真正威力：把 31 位大数压缩成 3 步小循环",
            "问：今天周日，2¹⁰⁰ 天后是星期几？不用算 31 位大数，只跟踪“除以 7 的余数”。",
        )

        # Left panel: 7-day modulo wheel
        els.append(card(20, 64, 326, 266))
        els.append(txt(38, 88, "① 模 7 时钟：逢 7 归 0", 13.5, INK, weight="600"))
        names = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
        cx, cy, r = 183, 198, 86
        els.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{HAIRLINE}" stroke-width="1.5"/>')
        for k in range(m):
            ang = -math.pi / 2 + 2 * math.pi * k / m
            px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
            hit = k == 2
            els.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="22" '
                f'fill="{ORANGE_SOFT if hit else BLUE_SOFT}" '
                f'stroke="{ORANGE if hit else BLUE}" stroke-width="{2.0 if hit else 1.2}"/>'
            )
            els.append(txt(px, py - 2, k, 13, INK, "middle", weight="700"))
            els.append(txt(px, py + 12, names[k], 10.5, ORANGE if hit else MUTED, "middle"))
        els.append(txt(cx, cy - 4, "mod 7", 13, BLUE, "middle", weight="600"))
        els.append(txt(cx, cy + 13, "余 2 → 周二", 11.5, ORANGE, "middle", weight="600"))
        els.append(txt(183, 314, "所有相差 7 的倍数的天数，都落在同一格", 11.5, MUTED, "middle"))

        # Right panel: 2^k mod 7 cycle
        els.append(card(362, 64, 378, 266))
        els.append(txt(380, 88, "② 每次乘 2 只留余数：3 步就回到 1", 13.5, INK, weight="600"))

        nodes = [(432, 168, "1", "2⁰, 2³, 2⁶…"), (552, 126, "2", "2¹, 2⁴…(终点)"), (656, 196, "4", "2², 2⁵…")]
        for idx, (nx, ny, val, sub) in enumerate(nodes):
            is_target = idx == 1
            els.append(
                f'<circle cx="{nx}" cy="{ny}" r="26" '
                f'fill="{ORANGE_SOFT if is_target else GREEN_SOFT}" '
                f'stroke="{ORANGE if is_target else GREEN}" stroke-width="{2.0 if is_target else 1.4}"/>'
            )
            els.append(txt(nx, ny + 5, f"余 {val}", 13.5, INK, "middle", weight="700"))
            els.append(txt(nx, ny + 42, sub, 11, ORANGE if is_target else MUTED, "middle"))

        # Curved arrows 1 -> 2 -> 4 -> 1
        els.append(
            f'<path d="M456,156 Q496,126 524,129" fill="none" stroke="{GREEN}" stroke-width="1.7" marker-end="url(#arr-green)"/>'
        )
        els.append(txt(490, 128, "×2", 11.5, GREEN, "middle", weight="600", halo=True))
        els.append(
            f'<path d="M576,138 Q622,152 640,173" fill="none" stroke="{GREEN}" stroke-width="1.7" marker-end="url(#arr-green)"/>'
        )
        els.append(txt(618, 150, "×2", 11.5, GREEN, "middle", weight="600", halo=True))
        els.append(
            f'<path d="M632,208 Q536,248 452,188" fill="none" stroke="{GREEN}" stroke-width="1.7" stroke-dasharray="4 3" marker-end="url(#arr-green)"/>'
        )
        els.append(txt(522, 239, "4×2=8≡1，归零循环", 11.5, GREEN, "middle", weight="600", halo=True))

        els.append(card(380, 256, 342, 58, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(394, 278, "拆解指数：100 = 3 × 33 + 1（转满 33 圈，再多走 1 步）", 12, BODY))
        els.append(txt(394, 299, "2¹⁰⁰ = (2³)³³ × 2¹ ≡ 1³³ × 2 ≡ 2 (mod 7)  →  周二", 12.5, ORANGE, weight="700"))

        return figure(
            348,
            "同余时钟与幂次循环：心算 2 的 100 次方模 7",
            "左图展示星期0到6的模7圆盘；右图展示2的幂模7在余数1、2、4之间每3步循环一次，2的100次方转33圈余1步，落在余数2即周二。",
            els,
        )

    def heptadecagon():
        c = math.cos(2 * math.pi / 17)
        s17 = math.sqrt(17)
        t = math.sqrt(34 - 2 * s17)
        formula = (-1 + s17 + t + 2 * math.sqrt(17 + 3 * s17 - t - 2 * math.sqrt(34 + 2 * s17))) / 16
        assert abs(c - formula) < 1e-12
        assert 17 == 2 ** (2 ** 2) + 1

        # Verify Gauss's actual first period split using primitive root g = 3 (mod 17)
        powers = [pow(3, k, 17) for k in range(16)]
        assert sorted(powers) == list(range(1, 17))
        zeta = lambda r: cmath.exp(2j * math.pi * r / 17)
        eta0 = sum(zeta(powers[k]) for k in range(0, 16, 2)).real
        eta1 = sum(zeta(powers[k]) for k in range(1, 16, 2)).real
        assert abs((eta0 + eta1) - (-1.0)) < 1e-11
        assert abs((eta0 * eta1) - (-4.0)) < 1e-11
        assert abs(eta0 - (-1 + math.sqrt(17)) / 2) < 1e-11

        els = header(
            "正十七边形为什么能用尺规画出：16 个复根连续四次“对折”",
            "尺规交点最多解二次方程（只出平方根 √）。17 − 1 = 16 = 2⁴，恰好能对折 4 次，每次只解一个二次方程。",
        )

        # Left panel: 17-gon with vertical conjugate chords
        els.append(card(20, 64, 316, 292))
        els.append(txt(38, 88, "① 圆周 17 等分：上下对称配成余弦", 13, INK, weight="600"))
        cx, cy, r = 178, 202, 80
        pts = [
            (cx + r * math.cos(2 * math.pi * k / 17), cy - r * math.sin(2 * math.pi * k / 17))
            for k in range(17)
        ]
        els.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{HAIRLINE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        # Axis
        els.append(f'<line x1="{cx - r - 12}" y1="{cy}" x2="{cx + r + 14}" y2="{cy}" stroke="{HAIRLINE}" stroke-width="1"/>')
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        els.append(f'<polygon points="{poly}" fill="{BLUE_SOFT}" fill-opacity="0.65" stroke="{BLUE}" stroke-width="1.6"/>')
        # Highlight conjugate chord (1, 16) giving 2 cos(2pi/17)
        p1, p16 = pts[1], pts[16]
        els.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p16[0]:.1f}" y2="{p16[1]:.1f}" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="3 2"/>')
        els.append(f'<line x1="{cx}" y1="{cy}" x2="{p1[0]:.1f}" y2="{cy}" stroke="{ORANGE}" stroke-width="2.2"/>')
        for k, (x, y) in enumerate(pts):
            special = k in (0, 1, 16)
            els.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4.2 if special else 2.8}" '
                f'fill="{ORANGE if special else BLUE}"/>'
            )
            if k in (0, 1, 4, 8, 9, 13, 16):
                ox = (x - cx) / r * 15
                oy = (y - cy) / r * 15
                els.append(txt(x + ox, y + oy + 4, k, 11, ORANGE if special else MUTED, "middle", weight="600" if special else None))

        els.append(txt(178, 326, "目标：造出横坐标 cos(2π/17)（橙色水平段）", 11.5, ORANGE, "middle", weight="600"))
        els.append(txt(178, 344, "本图为精确坐标示意，右侧展示高斯的代数拆法", 11, MUTED, "middle"))

        # Right panel: 4-step period halving ladder
        els.append(card(350, 64, 390, 292))
        els.append(txt(368, 88, "② 高斯周期拆解法：把 16 次方程拆成 4 层二次方程", 13, INK, weight="600"))

        stages = [
            ("去掉顶点 0，剩 16 个对称顶点", "按 3ᵏ mod 17 重排顺序", "16 项", SLATE_SOFT, BODY),
            ("第 1 次对折：分成两组各 8 项", "t² + t − 4 = 0  →  出现 √17", "8 + 8", BLUE_SOFT, BLUE),
            ("第 2 次对折：再拆成各 4 项", "解二次方程  →  出现 √(34 − 2√17)", "4 + 4", BLUE_SOFT, BLUE),
            ("第 3 次对折：拆成各 2 项", "再解二次方程  →  套上第 3 层 √", "2 + 2", GREEN_SOFT, GREEN),
            ("第 4 次定位：锁定顶点 1 与 16", "得到 cos(2π/17)，尺规即可作出！", "1 + 1", ORANGE_SOFT, ORANGE),
        ]
        for i, (title_s, eq_s, tag_s, bg_c, fg_c) in enumerate(stages):
            sy = 102 + i * 44
            els.append(card(368, sy, 354, 36, rx=7, fill=bg_c, stroke=fg_c, sw=1))
            els.append(txt(380, sy + 15, title_s, 11.8, INK, weight="600"))
            els.append(txt(380, sy + 29, eq_s, 11, fg_c if i > 0 else MUTED))
            els.append(pill(660, sy + 7, tag_s, fg=fg_c, bg="#ffffff", w=52, h=21, size=11))
            if i < len(stages) - 1:
                els.append(f'<line x1="545" y1="{sy + 36}" x2="545" y2="{sy + 44}" stroke="{MUTED}" stroke-width="1.2"/>')

        els.append(txt(368, 341, "反例：正七边形 7−1 = 6 = 2×3，卡在因子 3（需开立方），尺规无解", 11.5, MUTED))

        return figure(
            374,
            "正十七边形与高斯的四次对折降次思路",
            "左图展示圆周17等分及顶点1与16对应的余弦线段；右图展示高斯将16个虚根按3的幂次重排后连续对折4次（16→8→4→2→1），每次仅解二次方程，从而只用四层平方根写出cos(2π/17)。",
            els,
        )

    DATA = [(1, 2.0), (2, 2.9), (3, 4.4), (4, 4.6), (5, 6.3), (6, 6.6)]

    CANDIDATE = (0.62, 2.15)

    def sse(a, b):
        return sum((y - (a * x + b)) ** 2 for x, y in DATA)

    def fit():
        n = len(DATA)
        sx = sum(x for x, _ in DATA)
        sy = sum(y for _, y in DATA)
        sxx = sum(x * x for x, _ in DATA)
        sxy = sum(x * y for x, y in DATA)
        a = (n * sxy - sx * sy) / (n * sxx - sx * sx)
        b = (sy - a * sx) / n
        assert abs(a * sx / n + b - sy / n) < 1e-12
        assert sse(a, b) < sse(*CANDIDATE)
        for d in (-0.02, 0.02):
            assert sse(a, b) < sse(a + d, b) and sse(a, b) < sse(a, b + d)
        return a, b

    def draw_ls_panel(x_card, title_str, params, accent, soft_fill, badge_txt):
        a, b = params
        total_sq = sse(a, b)
        # Equal aspect scale: 1 data unit = 26.5 px on BOTH x and y axes so squares are true squares!
        scale = 26.5
        ox = x_card + 74
        oy = 302  # y = 0 baseline
        w_axis = 6.8 * scale
        h_axis = 7.3 * scale

        def X(v):
            return ox + v * scale

        def Y(v):
            return oy - v * scale

        els = [
            card(x_card, 64, 352, 294),
            txt(x_card + 16, 86, title_str, 13, INK, weight="600"),
            # Grid hairlines
        ]
        for g in range(1, 8):
            els.append(f'<line x1="{ox}" y1="{Y(g):.1f}" x2="{ox + w_axis:.1f}" y2="{Y(g):.1f}" stroke="#f1f5f9" stroke-width="1"/>')
        # Axes
        els.append(f'<path d="M{ox},{oy - h_axis:.1f} V{oy} H{ox + w_axis:.1f}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')
        for tick in range(1, 7):
            els.append(txt(X(tick), oy + 15, tick, 10.5, MUTED, "middle"))
        for tick in (2, 4, 6):
            els.append(txt(ox - 8, Y(tick) + 4, tick, 10.5, MUTED, "end"))

        # Draw true geometric error squares first (behind line and points)
        for x, y in DATA:
            yh = a * x + b
            err = abs(y - yh)
            side = err * scale
            if side > 0.5:
                top_y = min(Y(y), Y(yh))
                # Place square to the right of x (or left on last point if tight)
                sq_x = X(x) if x < 6 else X(x) - side
                els.append(
                    f'<rect x="{sq_x:.1f}" y="{top_y:.1f}" width="{side:.1f}" height="{side:.1f}" '
                    f'fill="{soft_fill}" fill-opacity="0.85" stroke="{accent}" stroke-width="1"/>'
                )

        # Fitted line
        els.append(
            f'<line x1="{X(0.4):.1f}" y1="{Y(a * 0.4 + b):.1f}" x2="{X(6.4):.1f}" y2="{Y(a * 6.4 + b):.1f}" '
            f'stroke="{accent}" stroke-width="2.0"/>'
        )

        # Residual segments & data points
        for x, y in DATA:
            yh = a * x + b
            els.append(
                f'<line x1="{X(x):.1f}" y1="{Y(y):.1f}" x2="{X(x):.1f}" y2="{Y(yh):.1f}" '
                f'stroke="{accent}" stroke-width="1.8"/>'
            )
            els.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3.8" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')

        els.append(pill(x_card + 16, 328, f"{badge_txt}：正方形总面积 = {total_sq:.2f}", fg=accent, bg=soft_fill, w=224, h=22, size=11.5))
        els.append(txt(x_card + 336, 343, f"y={a:.2f}x+{b:.2f}", 11, MUTED, "end", cls="mono"))
        return els

    def least_squares():
        a, b = fit()
        els = header(
            "最小二乘法的几何直觉：把竖直误差变成“小正方形”，让总面积最小",
            "横纵轴采用 1:1 等比例刻度，每个方块的真实面积严格等于该点误差的平方 eᵢ²（正负不再抵消）。",
        )
        els += draw_ls_panel(20, "① 随手画一条偏斜直线：方块面积很大", CANDIDATE, ORANGE, ORANGE_SOFT, "偏斜线")
        els += draw_ls_panel(388, "② 最小二乘最优直线：方块总面积压到最小", (a, b), BLUE, BLUE_SOFT, "最优线")

        return figure(
            374,
            "最小二乘法的误差正方形面积对比",
            "左右两图使用同一组6个观测点与1比1等比例坐标轴。左图偏斜直线的6个误差正方形总面积为2.56；右图最小二乘直线的误差正方形总面积缩小到0.54。",
            els,
        )

    def curvature():
        # Verify Gaussian curvature K = k1 * k2 on three surfaces: plane (0*0=0), cylinder ((1/R)*0=0), sphere ((1/R)*(1/R)>0)
        r = 2.0
        k_plane = 0.0 * 0.0
        k_cylinder = (1.0 / r) * 0.0
        k_sphere = (1.0 / r) * (1.0 / r)
        assert k_plane == k_cylinder == 0.0 and k_sphere > 0.0

        els = header(
            "高斯的“绝妙定理”：为什么披萨弯着拿不塌，橘子皮却按不平？",
            "不拉伸、不撕裂地弯曲薄片时，两个主方向弯曲程度的乘积（高斯曲率 K = k₁ × k₂）保持不变。",
        )

        # Panel 1: Flat pizza / paper
        els.append(card(20, 64, 230, 212))
        els.append(txt(36, 86, "① 平摊薄片：K = 0 × 0 = 0", 12.8, INK, weight="600"))
        els.append(
            f'<polygon points="62,158 198,136 220,188 84,210" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>'
        )
        els.append(f'<line x1="94" y1="168" x2="186" y2="153" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="132" y1="149" x2="150" y2="195" stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(txt(135, 240, "横向 k₁ = 0，纵向 k₂ = 0", 11.5, BODY, "middle"))
        els.append(txt(135, 260, "软披萨直接端：纵向一弯就塌", 11.5, MUTED, "middle"))

        # Panel 2: Curved pizza / cylinder
        els.append(card(265, 64, 230, 212))
        els.append(txt(281, 86, "② 左右卷起：K = k₁ × 0 = 0", 12.8, INK, weight="600"))
        els.append(
            f'<path d="M302,164 Q340,126 378,164 L448,194 Q415,168 386,194 Z" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>'
        )
        els.append(f'<path d="M312,172 Q342,140 374,172" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(f'<line x1="342" y1="150" x2="416" y2="181" stroke="{GREEN}" stroke-width="1.8"/>')
        els.append(txt(380, 240, "横向弯了 k₁≠0  ⇒  纵向必保持 k₂=0", 11.5, GREEN, "middle", weight="600"))
        els.append(txt(380, 260, "所以尖端挺直不塌！（无需拉伸饼皮）", 11.5, MUTED, "middle"))

        # Panel 3: Sphere / Orange peel
        els.append(card(510, 64, 230, 212))
        els.append(txt(526, 86, "③ 球面（地球）：K = 1/R² > 0", 12.8, INK, weight="600"))
        cx, cy, sr = 625, 166, 46
        els.append(f'<circle cx="{cx}" cy="{cy}" r="{sr}" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{sr}" ry="15" fill="none" stroke="{ORANGE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append(f'<ellipse cx="{cx}" cy="{cy}" rx="15" ry="{sr}" fill="none" stroke="{ORANGE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append(txt(625, 240, "两个方向都弯：K > 0 ≠ 平面的 0", 11.5, ORANGE, "middle", weight="600"))
        els.append(txt(625, 260, "绝不可能无变形摊成平面地图", 11.5, MUTED, "middle"))

        return figure(
            294,
            "高斯绝妙定理：曲率乘积决定能否无拉伸展平",
            "平纸片与卷起的披萨高斯曲率均为0，因此卷起横向可迫使纵向挺直；球面高斯曲率大于0，故地球表面无法无拉伸地摊平为地图。",
            els,
        )

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        for name, content in (
            ("sum-pairs", pairing()),
            ("mod-clock", clock()),
            ("heptadecagon", heptadecagon()),
            ("least-squares", least_squares()),
            ("pizza-curvature", curvature()),
        ):
            (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
            print(f"Wrote {name}.svg")

    main()


@register("group-set", "群论与集合论：对称复合、伽罗瓦、可数配对与对角线", "algebra_logic")
def build_group_set():
    OUT = REPO_ROOT / "assets" / "images" / "group-set"

    IDENTITY = (0, 1, 2)

    ROT = (2, 0, 1)  # 120 deg counter-clockwise: top->left, left->right, right->top

    NAMES = {
        (0, 1, 2): "e",
        (2, 0, 1): "r",
        (1, 2, 0): "r²",
        (0, 2, 1): "a",  # reflect across FIXED vertical axis (through top slot)
        (2, 1, 0): "b",  # reflect across FIXED bottom-left slot axis
        (1, 0, 2): "c",  # reflect across FIXED bottom-right slot axis
    }

    ORDER = [(0, 1, 2), (2, 0, 1), (1, 2, 0), (0, 2, 1), (2, 1, 0), (1, 0, 2)]

    LETTERS = "ABC"

    def compose(x, y):
        """Apply symmetry y first, then symmetry x (with axes fixed on the table)."""
        return tuple(y[x[i]] for i in range(3))

    def check_group():
        elems = set(permutations(range(3)))
        assert elems == set(ORDER) and len(ORDER) == 6
        for x in ORDER:
            for y in ORDER:
                assert compose(x, y) in elems
            assert compose(x, IDENTITY) == x == compose(IDENTITY, x)
            assert any(compose(x, y) == IDENTITY for y in ORDER)
        for x in ORDER:
            for y in ORDER:
                for z in ORDER:
                    assert compose(compose(x, y), z) == compose(x, compose(y, z))
        assert compose(ROT, ROT) == (1, 2, 0)
        assert compose(ROT, compose(ROT, ROT)) == IDENTITY
        noncomm = [(x, y) for x in ORDER for y in ORDER if compose(x, y) != compose(y, x)]
        assert len(noncomm) == 18
        # Flip a (vertical desk axis) first: (A,B,C)->(A,C,B); then CCW 120 r -> (B,A,C) = c
        assert NAMES[compose(ROT, (0, 2, 1))] == "c"
        # CCW 120 r first: (A,B,C)->(C,A,B); then flip vertical desk axis a -> (C,B,A) = b
        assert NAMES[compose((0, 2, 1), ROT)] == "b"
        return noncomm

    def mini_tri(cx, cy, r_tri, arrangement, axis_kind=None, rot_deg=0):
        # Equilateral triangle centered at centroid (cx, cy)
        verts = [
            (cx, cy - r_tri),
            (cx - r_tri * math.sqrt(3) / 2, cy + r_tri / 2),
            (cx + r_tri * math.sqrt(3) / 2, cy + r_tri / 2),
        ]
        pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in verts)
        out = [f'<polygon points="{pts}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>']

        # Optional fixed mirror axis etched on the desk
        if axis_kind is not None:
            ang = (-math.pi / 2, 5 * math.pi / 6, math.pi / 6)[axis_kind]
            L = r_tri * 1.15
            out.append(
                f'<line x1="{cx - L * math.cos(ang):.1f}" y1="{cy - L * math.sin(ang):.1f}" '
                f'x2="{cx + L * math.cos(ang):.1f}" y2="{cy + L * math.sin(ang):.1f}" '
                f'stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="4 3"/>'
            )

        # Optional rotation arc cue
        if rot_deg:
            ar = r_tri * 0.42
            out.append(
                f'<path d="M{cx + ar:.1f},{cy:.1f} A{ar:.1f},{ar:.1f} 0 0,0 {cx - ar * 0.5:.1f},{cy - ar * 0.866:.1f}" '
                f'fill="none" stroke="{GREEN}" stroke-width="1.4" marker-end="url(#arr-green)"/>'
            )

        offsets = [(0, -10), (-11, 10), (11, 10)]
        for (vx, vy), (ox, oy), idx in zip(verts, offsets, arrangement):
            col = ORANGE if LETTERS[idx] == "A" else INK
            out.append(txt(vx + ox, vy + oy + 4, LETTERS[idx], 12.5, col, "middle", weight="700", halo=True))
        return out

    def triangles():
        check_group()
        els = header(
            "正三角形的 6 种对称动作，以及为什么“先后顺序”不能乱换",
            "关键约定：三条虚线翻折轴画死在桌面上（不跟着字母跑）！橙色字母 A 用来追踪纸片怎么动。",
        )

        specs = [
            ((0, 1, 2), "e：原样不动", None, 0),
            ((2, 0, 1), "r：逆时针转 120°", None, 120),
            ((1, 2, 0), "r²：逆时针转 240°", None, 240),
            ((0, 2, 1), "a：沿桌面竖直轴翻折", 0, 0),
            ((2, 1, 0), "b：沿桌面左下轴翻折", 1, 0),
            ((1, 0, 2), "c：沿桌面右下轴翻折", 2, 0),
        ]
        for i, (arr, cap, ax_k, rdeg) in enumerate(specs):
            col_i, row_i = i % 3, i // 3
            bx = 20 + col_i * 244
            by = 62 + row_i * 136
            els.append(card(bx, by, 232, 124))
            els += mini_tri(bx + 116, by + 58, 34, arr, axis_kind=ax_k, rot_deg=rdeg)
            els.append(txt(bx + 116, by + 113, cap, 12, BODY, "middle", weight="600"))

        # Bottom worked comparison strip: why (a then r) != (r then a)
        els.append(card(20, 340, 720, 166, fill="#ffffff", stroke=BORDER))
        els.append(txt(36, 362, "亲手验证“不可交换”：同样是动作 a 和动作 r，颠倒先后顺序，终点完全不同", 13, INK, weight="600"))

        # Row 1: a first, then r -> c
        y1 = 404
        els.append(pill(36, y1 - 11, "路线 ①", fg=BLUE, bg=BLUE_SOFT, w=62, h=22, size=11.5))
        els += mini_tri(142, y1 + 4, 17, (0, 1, 2))
        els.append(f'<line x1="176" y1="{y1}" x2="254" y2="{y1}" stroke="{ORANGE}" stroke-width="1.5" marker-end="url(#arr-orange)"/>')
        els.append(txt(215, y1 - 6, "先翻折 a", 11.5, ORANGE, "middle", weight="600"))
        els += mini_tri(296, y1 + 4, 17, (0, 2, 1), axis_kind=0)
        els.append(f'<line x1="330" y1="{y1}" x2="414" y2="{y1}" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arr-green)"/>')
        els.append(txt(372, y1 - 6, "再逆时针转 r", 11.5, GREEN, "middle", weight="600"))
        els += mini_tri(456, y1 + 4, 17, (1, 0, 2))
        els.append(pill(504, y1 - 11, "结果 = c（顶B 左A 右C）", fg=INK, bg=SLATE_SOFT, w=190, h=22, size=11.5))

        # Row 2: r first, then a -> b
        y2 = 472
        els.append(pill(36, y2 - 11, "路线 ②", fg=ORANGE, bg=ORANGE_SOFT, w=62, h=22, size=11.5))
        els += mini_tri(142, y2 + 4, 17, (0, 1, 2))
        els.append(f'<line x1="176" y1="{y2}" x2="254" y2="{y2}" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arr-green)"/>')
        els.append(txt(215, y2 - 6, "先逆时针转 r", 11.5, GREEN, "middle", weight="600"))
        els += mini_tri(296, y2 + 4, 17, (2, 0, 1))
        els.append(f'<line x1="330" y1="{y2}" x2="414" y2="{y2}" stroke="{ORANGE}" stroke-width="1.5" marker-end="url(#arr-orange)"/>')
        els.append(txt(372, y2 - 6, "再沿桌面竖直轴 a 翻", 11.5, ORANGE, "middle", weight="600"))
        els += mini_tri(456, y2 + 4, 17, (2, 1, 0), axis_kind=0)
        els.append(pill(504, y2 - 11, "结果 = b（顶C 左B 右A）", fg=ORANGE, bg=ORANGE_SOFT, w=190, h=22, size=11.5))

        return figure(
            522,
            "正三角形的六种对称动作与不可交换实验",
            "上方展示正三角形的3种旋转和沿桌面固定轴的3种翻折；下方分步对比先翻折a再转r得到c，而先转r再沿桌面竖直轴a翻折得到b。",
            els,
        )

    def cayley_table():
        noncomm = set(check_group())
        els = header(
            "六个动作的“乘法表”（凯莱表），以及伽罗瓦看到的方程根对称",
            "查表口诀：先找上方的【第一步动作（列）】，再找左侧的【第二步动作（行）】，交叉格就是总结果。",
        )

        # Left card: 6x6 Cayley table with explicit highlight on (r, a)=c vs (a, r)=b
        els.append(card(20, 62, 366, 294))
        els.append(txt(36, 84, "① 三角形对称群 S₃ 复合表（共 36 格）", 13, INK, weight="600"))
        x0, y0, cell = 78, 118, 32
        els.append(txt(x0 + 3 * cell, y0 - 20, "第一步先做（列） →", 11, MUTED, "middle"))
        els.append(txt(x0 - 38, y0 - 5, "后做↓", 11, MUTED, "start"))

        for j, y in enumerate(ORDER):
            els.append(txt(x0 + j * cell + cell / 2, y0 - 5, NAMES[y], 12, BLUE, "middle", weight="700"))
        for i, x in enumerate(ORDER):
            els.append(txt(x0 - 10, y0 + i * cell + 21, NAMES[x], 12, BLUE, "end", weight="700"))
            for j, y in enumerate(ORDER):
                gx, gy = x0 + j * cell, y0 + i * cell
                res = NAMES[compose(x, y)]
                special_c = i == 1 and j == 3  # first a (col 3), then r (row 1) -> c
                special_b = i == 3 and j == 1  # first r (col 1), then a (row 3) -> b
                if special_c:
                    bg_f, st_c, sw = GREEN_SOFT, GREEN, 2.0
                elif special_b:
                    bg_f, st_c, sw = ORANGE_SOFT, ORANGE, 2.0
                elif (x, y) in noncomm:
                    bg_f, st_c, sw = "#fff7ed", "#cbd5e1", 1.0
                else:
                    bg_f, st_c, sw = "#ffffff", "#cbd5e1", 1.0
                els.append(f'<rect x="{gx}" y="{gy}" width="{cell}" height="{cell}" fill="{bg_f}" stroke="{st_c}" stroke-width="{sw}"/>')
                els.append(
                    txt(
                        gx + cell / 2,
                        gy + 21,
                        res,
                        12,
                        GREEN if special_c else (ORANGE if special_b else INK),
                        "middle",
                        weight="700" if (special_c or special_b) else None,
                    )
                )

        els.append(txt(278, 171, "← 先a后r = c", 11.5, GREEN, weight="600"))
        els.append(txt(278, 235, "← 先r后a = b", 11.5, ORANGE, weight="600"))
        els.append(
            f'<rect x="36" y="319" width="11" height="11" rx="2" fill="#fff7ed" stroke="#cbd5e1" stroke-width="1"/>'
        )
        els.append(txt(52, 329, "浅橙底 18 格：颠倒顺序结果不同", 11, MUTED))
        els.append(txt(36, 346, "每行每列 6 个符号各出现 1 次（必有唯一撤销键）", 11, MUTED))

        # Right card: Why Galois cared — roots symmetry of x^2 - 2 = 0 vs quintic
        els.append(card(400, 62, 340, 294))
        els.append(txt(416, 84, "② 伽罗瓦的绝招：方程的“根”也有对称群！", 13, INK, weight="600"))

        els.append(card(416, 98, 308, 114, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1))
        els.append(txt(428, 118, "小样品：方程 x² − 2 = 0 的两个根  +√2  与  −√2", 12, INK, weight="600"))
        els.append(txt(428, 140, "• 原样不动 e：(+√2) + (−√2) = 0，乘积 = −2", 11.5, BODY))
        els.append(txt(428, 160, "• 互换两根 s：(−√2) + (+√2) = 0，乘积 = −2", 11.5, BLUE, weight="600"))
        els.append(txt(428, 182, "只靠有理数加减乘除，根本分不清 +√2 和 −√2！", 11.5, BODY))
        els.append(txt(428, 200, "⇒ 对称群只有 {e, s} 两个动作，一步开平方就能解开。", 11.5, GREEN, weight="600"))

        els.append(card(416, 222, 308, 112, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1))
        els.append(txt(428, 242, "一般五次方程：5 个根最多有 5! = 120 种置换（S₅）", 12, INK, weight="600"))
        els.append(txt(428, 264, "• 每开一次 n 次方根，只能削掉一层“可交换”的对称", 11.5, BODY))
        els.append(txt(428, 284, "• 伽罗瓦发现：S₅ 里藏着 60 个动作的“硬核” A₅，", 11.5, BODY))
        els.append(txt(428, 302, "  它的动作高度不可交换，永远拆不成可交换的碎片！", 11.5, ORANGE, weight="600"))
        els.append(txt(428, 322, "⇒ 所以一般五次方程绝不存在只靠根号的求根公式。", 11.5, INK, weight="600"))

        return figure(
            374,
            "三角形对称群凯莱表与伽罗瓦方程根对称",
            "左侧6乘6复合表标出先a后r得c、先r后a得b的查表位置，并展示每行每列无重复；右侧用x²−2=0的两根互换对比五次方程120种置换，解释伽罗瓦如何用群判别根式可解性。",
            [e for e in els if e],
        )

    def countable_pairing():
        # Verify Cantor's snake enumeration visits all reduced positive fractions p/q with p+q <= 5
        snake_cells = [
            (1, 1),
            (1, 2), (2, 1),
            (3, 1), (2, 2), (1, 3),
            (1, 4), (2, 3), (3, 2), (4, 1),
        ]
        seen = set()
        order_num = {}
        for p, q in snake_cells:
            val = Fraction(p, q)
            if val not in seen:
                seen.add(val)
                order_num[(p, q)] = len(seen)
        assert len(order_num) == 9  # only (2,2)=1/1 is duplicate in first 4 diagonals!

        els = header(
            "康托尔的第一层震撼：无限怎么比大小？不数总数，只看“能不能一一牵手”",
            "有限集合里“部分一定小于整体”；但在无限集合里，偶数、甚至密密麻麻的全体正分数，都能和自然数排成一队！",
        )

        # Left panel: Natural numbers <-> Even numbers
        els.append(card(20, 62, 336, 278))
        els.append(txt(36, 84, "① 正偶数明明少了一半，却和自然数“一样多”", 12.8, INK, weight="600"))

        for k in range(1, 6):
            cx = 56 + (k - 1) * 54
            els.append(f'<rect x="{cx - 19}" y="106" width="38" height="32" rx="7" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.2"/>')
            els.append(txt(cx, 127, k, 13, INK, "middle", weight="700"))
            els.append(f'<line x1="{cx}" y1="140" x2="{cx}" y2="184" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arr-green)"/>')
            els.append(txt(cx + 12, 166, "×2", 10.5, GREEN))
            els.append(f'<rect x="{cx - 19}" y="188" width="38" height="32" rx="7" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.2"/>')
            els.append(txt(cx, 209, 2 * k, 13, INK, "middle", weight="700"))
        els.append(txt(322, 127, "… n", 12.5, BLUE, weight="600"))
        els.append(txt(322, 209, "… 2n", 12.5, GREEN, weight="600"))
        els.append(card(36, 238, 304, 84, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(48, 260, "• 每一个自然数 n，都有唯一的偶数 2n 配对", 11.5, BODY))
        els.append(txt(48, 281, "• 每一个正偶数，也都有唯一的座位号 n/2", 11.5, BODY))
        els.append(txt(48, 303, "⇒ 双方谁也没剩下：它们同属“可数无限”！", 11.5, GREEN, weight="600"))

        # Right panel: Snake traversal over p/q grid
        els.append(card(370, 62, 370, 278))
        els.append(txt(386, 84, "② 分数密密麻麻？斜着走“蛇形路线”就能编号", 12.8, INK, weight="600"))

        gx0, gy0, step = 434, 118, 52
        # Snake polyline through snake_cells
        pts_poly = " ".join(f"{gx0 + (q - 1) * step},{gy0 + (p - 1) * step}" for p, q in snake_cells)
        els.append(f'<polyline points="{pts_poly}" fill="none" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="4 3"/>')

        for p in range(1, 5):
            for q in range(1, 5):
                cx = gx0 + (q - 1) * step
                cy = gy0 + (p - 1) * step
                dup = (p == 2 and q == 2) or (p == 2 and q == 4) or (p == 4 and q == 2) or (p == 3 and q == 3) or (p == 4 and q == 4)
                visited = (p, q) in order_num
                fill_c = "#f1f5f9" if dup else (ORANGE_SOFT if visited else "#ffffff")
                str_c = "#94a3b8" if dup else (ORANGE if visited else HAIRLINE)
                els.append(f'<rect x="{cx - 21}" y="{cy - 14}" width="42" height="28" rx="6" fill="{fill_c}" stroke="{str_c}" stroke-width="1.2"/>')
                els.append(txt(cx, cy + 4, f"{p}/{q}", 11.5, MUTED if dup else INK, "middle", weight="600" if visited else None))
                if visited:
                    els.append(f'<circle cx="{cx + 18}" cy="{cy - 12}" r="8" fill="{BLUE}"/>')
                    els.append(txt(cx + 18, cy - 8.5, order_num[(p, q)], 9.5, "#ffffff", "middle", weight="700"))
                elif p == 2 and q == 2:
                    els.append(txt(cx, cy + 23, "重复跳过", 9.5, MUTED, "middle", halo=True))

        els.append(txt(650, gy0 + 3 * step + 4, "…", 15, MUTED))
        els.append(txt(386, 314, "沿斜对角线依次扫描（跳过约分相等的重复项），", 11, MUTED))
        els.append(txt(386, 330, "哪怕任何两个分数之间还有无穷多个分数，也能排成一队！", 11, MUTED))

        return figure(
            356,
            "康托尔的一一对应：正偶数配对与有理数蛇形编号",
            "左图把自然数n与正偶数2n逐一连线配对；右图在4乘4分数网格上沿斜对角蛇形路线依次编号1到9，遇到2/2等于1/1时跳过重复，说明全体正有理数也可数。",
            els,
        )

    ROWS = ["010110", "111000", "001011", "100101", "011011", "000111"]

    def diagonal():
        flipped = "".join("1" if row[i] == "0" else "0" for i, row in enumerate(ROWS))
        assert all(flipped[i] != row[i] for i, row in enumerate(ROWS))
        assert flipped not in ROWS

        els = header(
            "康托尔的第二层震撼（对角线法）：为什么无限 0-1 序列绝对排不进一张清单？",
            "假设有人交出一份号称“一个不漏”的无限清单。只要沿着对角线逐位取反，就能当场造出一条漏网之鱼。",
        )

        # Left: 6x6 matrix + flipped row
        els.append(card(20, 62, 412, 290))
        els.append(txt(36, 84, "① 揪出对角线（橙格），逐位 0↔1 翻转造新序列", 12.8, INK, weight="600"))
        x0, y0, cell = 122, 100, 32
        for i, row in enumerate(ROWS):
            y = y0 + i * cell
            els.append(txt(x0 - 12, y + 21, f"第 {i + 1} 行", 11.5, MUTED, "end"))
            for j, ch in enumerate(row):
                on = i == j
                els.append(
                    f'<rect x="{x0 + j * cell}" y="{y}" width="{cell}" height="{cell}" '
                    f'fill="{ORANGE_SOFT if on else "#ffffff"}" stroke="{ORANGE if on else "#cbd5e1"}" '
                    f'stroke-width="{1.8 if on else 1.0}"/>'
                )
                els.append(txt(x0 + j * cell + cell / 2, y + 21, ch, 13, ORANGE if on else BODY, "middle", weight="700" if on else None, cls="mono"))
            els.append(txt(x0 + 6 * cell + 10, y + 21, "…", 13, MUTED))

        # Arrow down to new escape sequence
        yn = y0 + 6 * cell + 22
        els.append(txt(x0 - 12, yn + 21, "逃逸序列", 12, BLUE, "end", weight="700"))
        for j, ch in enumerate(flipped):
            els.append(
                f'<rect x="{x0 + j * cell}" y="{yn}" width="{cell}" height="{cell}" rx="4" '
                f'fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>'
            )
            els.append(txt(x0 + j * cell + cell / 2, yn + 21, ch, 13.5, BLUE, "middle", weight="700", cls="mono"))
            els.append(txt(x0 + j * cell + cell / 2, yn - 5, "↓反", 9.5, ORANGE, "middle"))
        els.append(txt(x0 + 6 * cell + 10, yn + 21, "…", 13, BLUE, weight="700"))

        # Right: Why it CANNOT be anywhere on the infinite list
        els.append(card(446, 62, 294, 290))
        els.append(txt(462, 84, "② 它为什么不可能躲在清单后面？", 12.8, INK, weight="600"))
        reasons = [
            ("和第 1 行比", "第 1 位故意相反（0 ≠ 1）→ 排除！"),
            ("和第 2 行比", "第 2 位故意相反（1 ≠ 0）→ 排除！"),
            ("和第 3 行比", "第 3 位故意相反（1 ≠ 0）→ 排除！"),
            ("……", "……"),
            ("和第 n 行比", "第 n 位故意相反 → 永远不相等！"),
        ]
        for idx, (r_head, r_body) in enumerate(reasons):
            ry = 104 + idx * 38
            els.append(card(462, ry, 262, 31, rx=6, fill=SLATE_SOFT if idx < 4 else GREEN_SOFT, stroke=GREEN if idx == 4 else BORDER))
            els.append(txt(472, ry + 20, f"{r_head}：{r_body}", 11.3, GREEN if idx == 4 else BODY, weight="600" if idx == 4 else None))

        els.append(txt(462, 314, "结论：实数（无限小数）的“无限”，比自然数", 11.5, INK, weight="600"))
        els.append(txt(462, 333, "和分数的“可数无限”整整高出一个等级！", 11.5, BLUE, weight="600"))

        return figure(
            368,
            "康托尔对角线法：构造逃出任意无限清单的新序列",
            "左侧6乘6二进制矩阵标出橙色对角线011111，逐位取反得到蓝色逃逸序列100000；右侧逐行说明该序列在第n位必与第n行不同，证明全体无限0-1序列不可数。",
            els,
        )

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        for name, content in (
            ("triangle-symmetries", triangles()),
            ("s3-table", cayley_table()),
            ("countable-pairing", countable_pairing()),
            ("cantor-diagonal", diagonal()),
        ):
            (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
            print(f"Wrote {name}.svg")

    main()


@register("busy-beaver", "忙碌海狸：增长层级、上箭头、停机自指与状态支配", "algebra_logic")
def build_busy_beaver():
    OUT = REPO_ROOT / "assets" / "images" / "busy-beaver"

    def ackermann(m, n, memo=None):
        if memo is None:
            memo = {}
        key = (m, n)
        if key in memo:
            return memo[key]
        if m == 0:
            value = n + 1
        elif n == 0:
            value = ackermann(m - 1, 1, memo)
        else:
            value = ackermann(m - 1, ackermann(m, n - 1, memo), memo)
        memo[key] = value
        return value

    def up_arrow(a, arrows, b, memo=None):
        if memo is None:
            memo = {}
        key = (a, arrows, b)
        if key in memo:
            return memo[key]
        if arrows == 1:
            value = a**b
        elif b == 1:
            value = a
        else:
            value = up_arrow(a, arrows - 1, up_arrow(a, arrows, b - 1, memo), memo)
        memo[key] = value
        return value

    RULES = {
        ("A", 0): (1, 1, "B"),
        ("A", 1): (1, -1, "B"),
        ("B", 0): (1, -1, "A"),
        ("B", 1): (1, 1, "H"),
    }

    def run_beaver():
        tape = {}
        position = 0
        state = "A"
        frames = []
        for step in range(1, 8):
            symbol = tape.get(position, 0)
            write, move, nxt = RULES[(state, symbol)]
            tape[position] = write
            position += move
            state = nxt
            frames.append(
                {
                    "step": step,
                    "tape": dict(tape),
                    "head": position,
                    "state": state,
                    "ones": sum(1 for value in tape.values() if value == 1),
                }
            )
            if state == "H":
                break
        return frames

    def facts():
        assert (3**3) ** 3 == 19683
        assert 3 ** (3**3) == 3**27 == 7625597484987
        assert up_arrow(3, 2, 2) == 27
        assert up_arrow(3, 2, 3) == 7625597484987
        assert up_arrow(2, 2, 3) == 16
        assert up_arrow(2, 2, 4) == 65536
        memo = {}
        table = {(m, n): ackermann(m, n, memo) for m in range(4) for n in range(4)}
        assert table[(1, 3)] == 5 and table[(2, 3)] == 9 and table[(3, 3)] == 61
        assert ackermann(3, 4, memo) == 125
        for n in range(5):
            assert ackermann(3, n, memo) == 2 ** (n + 3) - 3
        assert 2 ** (13 + 3) - 3 == 65533
        last_poly = max(n for n in range(1, 1200) if n**100 >= 2**n)
        assert last_poly == 996
        assert all(2**n > n**100 for n in range(997, 1100))
        frames = run_beaver()
        assert len(frames) == 6 and frames[-1]["state"] == "H" and frames[-1]["ones"] == 4
        assert [frame["head"] for frame in frames] == [1, 0, -1, -2, -1, 0]
        assert 21**10 == 16679880978201
        return {"crossover": last_poly + 1, "frames": frames, "ackermann": table}

    def growth(crossover):
        rows = [(n, n * n, 2**n, math.factorial(n)) for n in range(1, 9)]
        els = header(
            "三种常规增长的精确对比，以及为什么指数迟早反超 n¹⁰⁰",
            "左：n 从 1 到 8 的精确值；右：取对数位数（log₁₀）看大趋势——n¹⁰⁰ 越走越平，2ⁿ 按固定斜率一路笔直爬升。",
        )

        # Left panel: exact table
        els.append(card(20, 62, 354, 276))
        els.append(txt(36, 84, "① 前 8 项精确表：n=4 起阶乘反超，n=5 起指数超平方", 12.2, INK, weight="600"))
        cols_x = (56, 126, 214, 314)
        for x, lbl in zip(cols_x, ("n", "n²", "2ⁿ", "n!")):
            els.append(txt(x, 108, lbl, 11.8, MUTED, "middle", weight="700"))
        els.append(f'<line x1="36" y1="115" x2="354" y2="115" stroke="{HAIRLINE}" stroke-width="1"/>')

        for idx, (n, sq, pw, fac) in enumerate(rows):
            ry = 134 + idx * 24
            if n in (4, 5):
                els.append(f'<rect x="34" y="{ry - 15}" width="322" height="21" rx="4" fill="{BLUE_SOFT if n == 5 else GREEN_SOFT}"/>')
            els.append(txt(cols_x[0], ry, n, 12, INK, "middle", weight="600", cls="mono"))
            els.append(txt(cols_x[1], ry, f"{sq:,}", 12, BODY, "middle", cls="mono"))
            els.append(txt(cols_x[2], ry, f"{pw:,}", 12, BLUE if pw > sq else BODY, "middle", weight="600" if n == 5 else None, cls="mono"))
            els.append(txt(cols_x[3], ry, f"{fac:,}", 12, GREEN if fac > pw else BODY, "middle", weight="600" if n == 4 else None, cls="mono"))

        # Right panel: log10 curve showing n^100 vs 2^n crossing at n=997!
        els.append(card(388, 62, 352, 276))
        els.append(txt(404, 84, f"② 对数坐标（位数对比）：n={crossover} 起 2ⁿ 永久反超 n¹⁰⁰", 12.2, INK, weight="600"))
        ox, oy, pw_w, pw_h = 434.0, 272.0, 282.0, 160.0
        els.append(f'<path d="M{ox},{oy - pw_h} V{oy} H{ox + pw_w}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')
        for xtick in (0, 500, 1000, 1200):
            tx = ox + (xtick / 1200.0) * pw_w
            els.append(txt(tx, oy + 15, xtick, 10.5, MUTED, "middle"))
        for ytick in (100, 200, 300):
            ty = oy - (ytick / 370.0) * pw_h
            els.append(f'<line x1="{ox}" y1="{ty:.1f}" x2="{ox + pw_w}" y2="{ty:.1f}" stroke="#f1f5f9" stroke-width="1"/>')
            els.append(txt(ox - 6, ty + 4, f"10^{ytick}", 10, MUTED, "end"))

        pts_poly = []
        pts_exp = []
        for n in range(10, 1201, 20):
            px = ox + (n / 1200.0) * pw_w
            py_p = oy - (100.0 * math.log10(n) / 370.0) * pw_h
            py_e = oy - (n * math.log10(2.0) / 370.0) * pw_h
            pts_poly.append(f"{px:.1f},{py_p:.1f}")
            pts_exp.append(f"{px:.1f},{py_e:.1f}")
        els.append(f'<polyline points="{" ".join(pts_poly)}" fill="none" stroke="{ORANGE}" stroke-width="1.9" stroke-dasharray="5 3"/>')
        els.append(f'<polyline points="{" ".join(pts_exp)}" fill="none" stroke="{BLUE}" stroke-width="2.1"/>')

        cx_cross = ox + (crossover / 1200.0) * pw_w
        cy_cross = oy - (crossover * math.log10(2.0) / 370.0) * pw_h
        els.append(f'<circle cx="{cx_cross:.1f}" cy="{cy_cross:.1f}" r="4.5" fill="{BLUE}"/>')
        els.append(txt(cx_cross - 8, cy_cross - 10, f"交点 n≈{crossover}（约 300 位数）", 10.8, BLUE, "end", weight="700", halo=True))
        els.append(txt(ox + 95, oy - 115, "n¹⁰⁰（对数越走越缓）", 11, ORANGE, weight="600", halo=True))
        els.append(txt(ox + 185, oy - 62, "2ⁿ（对数直线上升）", 11, BLUE, weight="600", halo=True))
        els.append(txt(404, 310, "直觉：n 每翻一倍，n¹⁰⁰ 只乘固定的 2¹⁰⁰；而 2ⁿ 直接变成自己的平方！", 11, BODY))
        els.append(txt(404, 327, "注：右图纵轴为十进制对数坐标（log₁₀ 值），以便同屏展示几百位大数。", 10.5, MUTED))

        return figure(
            354,
            "平方、指数、阶乘精确表与指数反超高次多项式的对数图",
            f"左表列出n从1到8的n²、2ⁿ、n!精确值；右图在对数坐标下展示2ⁿ的直线增长在n={crossover}处反超弯曲放缓的n¹⁰⁰。",
            els,
        )

    def arrows():
        height = 7625597484987
        assert height == 3**27
        els = header(
            "高德纳上箭头（↑）：每多一支箭头，就把“前一种运算”再叠成一座塔",
            "注意幂塔必须【从最顶层往下算】！多一支箭头不是多乘一次，而是让幂塔的“层数”本身爆炸。",
        )

        # Left panel: Bottom-up vs Top-down visual tree
        els.append(card(20, 62, 344, 266))
        els.append(txt(36, 84, "① 同样三个 3，从哪边先算差出 3.8 亿倍", 12.6, INK, weight="600"))

        els.append(card(36, 100, 312, 86, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(48, 122, "从底下先算：(3³)³ = 27³ = 19,683", 12.2, BODY, weight="600"))
        els.append(txt(48, 144, "本质只是指数相乘 3^(3×3) = 3⁹，威力很温和，", 11.3, MUTED))
        els.append(txt(48, 164, "所以高德纳箭头不采用这种顺序。", 11.3, MUTED))

        els.append(card(36, 198, 312, 114, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(48, 220, "从塔顶往下算（双箭头 3 ↑↑ 3）：", 12.2, BLUE, weight="700"))
        # Stacked power boxes
        els.append(f'<rect x="52" y="264" width="28" height="28" rx="5" fill="#ffffff" stroke="{BLUE}" stroke-width="1.4"/>')
        els.append(txt(66, 283, "3", 14, INK, "middle", weight="700"))
        els.append(f'<rect x="82" y="247" width="26" height="26" rx="5" fill="#ffffff" stroke="{BLUE}" stroke-width="1.4"/>')
        els.append(txt(95, 265, "3", 13, INK, "middle", weight="700"))
        els.append(f'<rect x="110" y="232" width="24" height="24" rx="5" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append(txt(122, 249, "3", 12, ORANGE, "middle", weight="700"))
        els.append(txt(148, 254, "先算顶上两层 3³ = 27", 11.3, ORANGE, weight="600"))
        els.append(txt(148, 276, "再算底数 3²⁷ = 7,625,597,484,987", 11.3, INK, weight="700"))
        els.append(txt(52, 304, "约 7.63 万亿！这就是 3 ↑↑ 3（3 层高的 3 幂塔）。", 11.2, BODY))

        # Right panel: Visual Power-Tower Brace for 3 ↑↑↑ 3 & Graham G = g_64
        els.append(card(378, 62, 362, 266))
        els.append(txt(394, 84, "② 三支箭头 3 ↑↑↑ 3：层数本身等于 7.63 万亿！", 12.6, INK, weight="600"))

        # Draw visual vertical tower of 3s on left of right card
        tx, ty_bot = 420, 266
        tower_lvls = [("3", 0), ("3", 1), ("⋮", 2), ("3", 3), ("3", 4)]
        for sym, lv in tower_lvls:
            bx = tx + lv * 14
            by = ty_bot - lv * 32
            if sym == "⋮":
                els.append(txt(bx + 12, by + 16, "⋰", 16, ORANGE, "middle", weight="700"))
            else:
                els.append(f'<rect x="{bx}" y="{by}" width="24" height="24" rx="5" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.3"/>')
                els.append(txt(bx + 12, by + 17, sym, 12.5, INK, "middle", weight="700"))

        # Dimension brace for height = 3^^3 = 7.63 trillion levels!
        els.append(f'<path d="M512,136 H520 V290 H512" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(txt(530, 198, "幂塔总层数 = 3 ↑↑ 3", 12, ORANGE, weight="700"))
        els.append(txt(530, 217, "= 7,625,597,484,987 层！", 11.8, INK, weight="700"))
        els.append(txt(530, 236, "（光把塔画出来就装不下宇宙）", 11, MUTED))

        els.append(card(394, 290, 330, 30, rx=6, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(559, 309, "葛立恒数 G：g₁=3↑↑↑↑3，前项值作后项箭头数，套64轮", 10.8, GREEN, "middle", weight="600"))

        return figure(
            344,
            "高德纳上箭头与幂塔层数爆炸图解",
            "左侧对比自底向上(3³)³=19683与自顶向下3↑↑3=3²⁷≈7.63万亿；右侧画出3↑↑↑3对应的7.63万亿层幂塔示意及葛立恒数箭头数递推规则。",
            els,
        )

    def beaver(frames):
        cells = (-2, -1, 0, 1)
        anim_css = """
      .scan { animation: scan 5.4s linear 1 forwards; }
      @keyframes scan {
        0%, 14% { transform: translateY(0); }
        18%, 31% { transform: translateY(34px); }
        35%, 48% { transform: translateY(68px); }
        52%, 65% { transform: translateY(102px); }
        69%, 82% { transform: translateY(136px); }
        86%, 100% { transform: translateY(170px); }
      }
      @media (prefers-reduced-motion: reduce) {
        .scan { animation: none; transform: translateY(170px); }
      }"""

        els = header(
            "两状态“忙碌海狸”冠军机：左边看状态说明书，右边一步步跟完 6 步停机",
            "纸带起初全为 0，从状态 A 出发。橙框依次扫过 6 步并停在最后一行（最终留下 4 个 1，恰为两状态理论上限）。",
        )

        # Left panel: State Transition Graph (A <-> B -> H)
        els.append(card(20, 62, 312, 272))
        els.append(txt(36, 84, "① 状态转移图（共 4 条指令）", 12.6, INK, weight="600"))

        # Nodes A, B, H
        els.append(f'<circle cx="88" cy="158" r="24" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(txt(88, 163, "A", 14, BLUE, "middle", weight="700"))
        els.append(txt(88, 124, "起点↓", 10.5, BLUE, "middle", weight="600"))

        els.append(f'<circle cx="246" cy="158" r="24" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(txt(246, 163, "B", 14, BLUE, "middle", weight="700"))

        els.append(f'<circle cx="167" cy="268" r="24" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2.0"/>')
        els.append(f'<circle cx="167" cy="268" r="20" fill="none" stroke="{ORANGE}" stroke-width="1.0"/>')
        els.append(txt(167, 273, "停机", 12.5, ORANGE, "middle", weight="700"))

        # Curved transitions
        els.append(f'<path d="M110,145 Q167,108 222,145" fill="none" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#arr-blue)"/>')
        els.append(txt(167, 118, "A读0→写1,右移", 10.5, BLUE, "middle", weight="600", halo=True))
        els.append(txt(167, 132, "A读1→写1,左移", 10.5, BLUE, "middle", halo=True))

        els.append(f'<path d="M224,172 Q167,208 112,172" fill="none" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arr-green)"/>')
        els.append(txt(167, 204, "B读0 → 写1,左移回A", 10.5, GREEN, "middle", weight="600", halo=True))

        els.append(f'<path d="M236,181 Q222,232 192,256" fill="none" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')
        els.append(txt(248, 232, "B读1 → 写1,右移停机!", 10.5, ORANGE, "middle", weight="700", halo=True))

        els.append(txt(176, 318, "手指顺着圆圈跳，就能算出右边每一步", 11, MUTED, "middle"))

        # Right panel: 6-step tape execution
        els.append(card(346, 62, 394, 272))
        els.append(txt(362, 84, "② 纸带逐步记录（橙格 = 本步结束时读写头位置）", 12.4, INK, weight="600"))
        els.append(txt(374, 106, "步", 11, MUTED, "middle"))
        els.append(txt(488, 106, "纸带四格（格号 −2, −1, 0, +1）", 11, MUTED, "middle"))
        els.append(txt(668, 106, "转入状态", 11, MUTED, "middle"))

        for idx, frame in enumerate(frames):
            ry = 114 + idx * 34
            els.append(f'<rect x="358" y="{ry}" width="368" height="28" rx="6" fill="#f8fafc" stroke="{BORDER}" stroke-width="1"/>')
            els.append(txt(374, ry + 18.5, frame["step"], 12, BLUE, "middle", weight="700", cls="mono"))
            for off, cpos in enumerate(cells):
                cx = 408 + off * 46
                sym = frame["tape"].get(cpos, 0)
                is_head = frame["head"] == cpos
                fill_c = ORANGE_SOFT if is_head else (BLUE_SOFT if sym else "#ffffff")
                str_c = ORANGE if is_head else (BLUE if sym else HAIRLINE)
                els.append(
                    f'<rect x="{cx}" y="{ry + 3}" width="38" height="22" rx="4" '
                    f'fill="{fill_c}" stroke="{str_c}" stroke-width="{1.7 if is_head else 1.1}"/>'
                )
                els.append(txt(cx + 19, ry + 18.5, sym, 12, INK, "middle", weight="700" if sym else None, cls="mono"))
            st_lbl = "H（停机）" if frame["state"] == "H" else f"状态 {frame['state']}"
            els.append(txt(668, ry + 18.5, st_lbl, 11.5, ORANGE if frame["state"] == "H" else BODY, "middle", weight="700" if frame["state"] == "H" else None))

        els.append(f'<rect class="scan" x="356" y="113" width="372" height="30" rx="7" fill="none" stroke="{ORANGE}" stroke-width="2.0"/>')
        return figure(
            350,
            "两状态忙碌海狸状态机与六步纸带运行图",
            "左侧画出状态A、B与停机的4条转移箭头；右侧列出第1至第6步结束时的纸带内容与读写头橙色位置，最终走6步留下4个1后停机。",
            els,
            extra_css=anim_css,
        )

    def halt_argument():
        els = header(
            "图灵停机问题的自指死结：如果真有“万能停机预言家 H”，把它装进杠精机器 D 里会怎样？",
            "对角机器 D 专门跟预言家 H 拧着干：H 猜会停它就死循环，H 猜不停它就立刻停——然后把 D 自己的图纸喂给 D！",
        )

        # Outer frame of Diagonal Machine D
        els.append(card(148, 72, 464, 206, rx=12, fill="#ffffff", stroke=BLUE, sw=1.8, dash="6 4"))
        els.append(pill(162, 82, "对角“杠精”机器 D 的内部电路", fg=BLUE, bg=BLUE_SOFT, w=198, h=22, size=11.5))

        # Input: D's own blueprint <D>
        els.append(card(20, 146, 106, 58, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.5))
        els.append(txt(73, 170, "喂入图纸 ⟨D⟩", 12, ORANGE, "middle", weight="700"))
        els.append(txt(73, 189, "（D自己的代码）", 10.5, BODY, "middle"))
        els.append(f'<line x1="126" y1="175" x2="180" y2="175" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')

        # H box inside D
        els.append(card(184, 134, 156, 82, rx=9, fill=BLUE_SOFT, stroke=BLUE, sw=1.6))
        els.append(txt(262, 160, "假想的万能判定器 H", 12.2, BLUE, "middle", weight="700"))
        els.append(txt(262, 180, "先预测：D 读 ⟨D⟩", 11.2, BODY, "middle"))
        els.append(txt(262, 198, "最终会不会停机？", 11.2, BODY, "middle"))

        # Upper branch: H says HALTS -> D loops forever -> CONTRADICTION!
        els.append(f'<path d="M340,155 L418,122" fill="none" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')
        els.append(txt(376, 126, "若 H 答“会停”", 10.8, ORANGE, "middle", weight="600", halo=True))
        els.append(card(422, 96, 170, 50, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(507, 118, "D 故意走进死循环 ∞", 11.8, INK, "middle", weight="700"))
        els.append(txt(507, 136, "实际结果：永不停机！", 11, ORANGE, "middle", weight="600"))
        els.append(f'<line x1="592" y1="121" x2="626" y2="121" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')
        els.append(pill(630, 108, "打脸矛盾 ✗", fg=ORANGE, bg=ORANGE_SOFT, w=108, h=26, size=12))

        # Lower branch: H says LOOPS -> D halts immediately -> CONTRADICTION!
        els.append(f'<path d="M340,195 L418,228" fill="none" stroke="{GREEN}" stroke-width="1.6" marker-end="url(#arr-green)"/>')
        els.append(txt(376, 228, "若 H 答“不停”", 10.8, GREEN, "middle", weight="600", halo=True))
        els.append(card(422, 204, 170, 50, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(507, 226, "D 当场踩刹车停机！", 11.8, INK, "middle", weight="700"))
        els.append(txt(507, 244, "实际结果：立刻停了！", 11, GREEN, "middle", weight="600"))
        els.append(f'<line x1="592" y1="229" x2="626" y2="229" stroke="{GREEN}" stroke-width="1.6" marker-end="url(#arr-green)"/>')
        els.append(pill(630, 216, "打脸矛盾 ✗", fg=ORANGE, bg=ORANGE_SOFT, w=108, h=26, size=12))

        els.append(txt(24, 304, "结论：无论 H 回答“会停”还是“不停”都当场自相矛盾 ⇒ 世上绝不存在通杀所有程序的停机判定器 H。", 11.8, INK, weight="600"))

        return figure(
            322,
            "停机问题自指反证流程图",
            "将对角机器D自身的图纸喂入D，内部的假想停机判定器H若预测会停则D进入死循环，若预测不停则D立刻停机，两条分支均导出矛盾。",
            els,
        )

    def domination():
        els = header(
            "忙碌海狸 S(n) 为什么能超过一切可计算函数 f(n)？拼装一台“三段式合成机器”",
            "关键账本：算出巨大数值 F(n) 并不需要很多状态——写下输入 n 只要约 log₂n 个状态，程序本身更是固定常数 c！",
        )

        # Top pipeline: 3 modules chained left-to-right
        els.append(card(20, 66, 720, 128))
        els.append(txt(36, 88, "① 从全 0 空白纸带出发，把三个模块串成一台一定会停的图灵机：", 12.6, INK, weight="600"))

        boxes = [
            (36, "模块 A：写数器", "在空白纸带上印出二进制 n", "状态开销 ≈ log₂ n", BLUE_SOFT, BLUE),
            (274, "模块 B：运行 F 的程序", "算出 F(n) = max{f(0)…f(n)}", "状态开销 = 固定常数 c", GREEN_SOFT, GREEN),
            (512, "模块 C：倒计时空转", "照着算出的 F(n) 多空转几步再停", "总运行步数严格 > F(n)", ORANGE_SOFT, ORANGE),
        ]
        for bx, b_title, b_line1, b_cost, bg_c, fg_c in boxes:
            els.append(card(bx, 102, 210, 78, rx=8, fill=bg_c, stroke=fg_c, sw=1.3))
            els.append(txt(bx + 12, 122, b_title, 12, INK, weight="700"))
            els.append(txt(bx + 12, 142, b_line1, 11.2, BODY))
            els.append(txt(bx + 12, 164, b_cost, 11.2, fg_c, weight="700"))

        els.append(f'<line x1="246" y1="141" x2="270" y2="141" stroke="{MUTED}" stroke-width="1.6" marker-end="url(#arr-muted)"/>')
        els.append(f'<line x1="484" y1="141" x2="508" y2="141" stroke="{MUTED}" stroke-width="1.6" marker-end="url(#arr-muted)"/>')

        # Bottom budget comparison bar
        els.append(card(20, 206, 720, 114))
        els.append(txt(36, 228, "② 算一算状态预算：当 n 足够大时，c + O(log₂ n) 远远小于可用配额 n！", 12.6, INK, weight="600"))

        # Budget bar k(n) vs n
        els.append(txt(36, 257, "合成机器状态数 k(n)", 11.5, BODY, weight="600"))
        els.append(f'<rect x="176" y="242" width="110" height="22" rx="4" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.2"/>')
        els.append(txt(231, 257, "固定程序 c", 11, GREEN, "middle", weight="600"))
        els.append(f'<rect x="288" y="242" width="96" height="22" rx="4" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.2"/>')
        els.append(txt(336, 257, "+ O(log₂ n)", 11, BLUE, "middle", weight="600"))

        els.append(txt(36, 290, "忙碌海狸总配额 n", 11.5, BODY, weight="600"))
        els.append(f'<rect x="176" y="275" width="364" height="22" rx="4" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.3"/>')
        els.append(txt(358, 290, "n 越大，富余状态越多（k(n) ≤ n 永远成立）", 11.2, ORANGE, "middle", weight="600"))

        els.append(pill(552, 254, "S(n) ≥ S(k(n)) > F(n) ≥ f(n)", fg=INK, bg=SLATE_SOFT, w=174, h=30, size=11))

        return figure(
            336,
            "三段式合成图灵机证明忙碌海狸最终支配一切可计算函数",
            "上方串联写数器（约log₂n状态）、计算F(n)的固定程序（c状态）与空转模块，使总步数大于F(n)；下方对比状态预算k(n)=c+O(log₂n)在大n时小于总配额n，推出S(n)>f(n)。",
            els,
        )

    def main():
        data = facts()
        OUT.mkdir(parents=True, exist_ok=True)
        pictures = {
            "growth": growth(data["crossover"]),
            "arrows": arrows(),
            "beaver": beaver(data["frames"]),
            "halt": halt_argument(),
            "dominate": domination(),
        }
        for name, content in pictures.items():
            root = ET.fromstring(content)
            assert root.get("width") == str(WIDTH)
            assert root.get("viewBox") == f'0 0 {WIDTH} {root.get("height")}'
            (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
            print(name, root.get("height"))
        print("crossover", data["crossover"])

    main()


@register("game-value", "博弈必胜：逆向归纳、尼姆糖袋、六贯棋与 α-β 剪枝", "algebra_logic")
def build_game_value():
    OUT = REPO_ROOT / "assets" / "images" / "game-value"

    WIN_FILL = BLUE_SOFT

    LOSS_FILL = ORANGE_SOFT

    LINES = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    )

    def winner(board):
        for a, b, c in LINES:
            if board[a] and board[a] == board[b] == board[c]:
                return board[a]
        return 0

    def ttt_value(board, turn, memo):
        found = winner(board)
        if found == 1:
            return 1
        if found == 2:
            return -1
        if all(board):
            return 0
        key = (board, turn)
        if key in memo:
            return memo[key]
        scores = []
        for index, cell in enumerate(board):
            if cell:
                continue
            nxt = list(board)
            nxt[index] = turn
            scores.append(ttt_value(tuple(nxt), 3 - turn, memo))
        result = max(scores) if turn == 1 else min(scores)
        memo[key] = result
        return result

    def count_games(board=(0,) * 9, turn=1):
        found = winner(board)
        if found == 1:
            return 1, 0, 0
        if found == 2:
            return 0, 1, 0
        if all(board):
            return 0, 0, 1
        wins = draws = losses = 0
        for index, cell in enumerate(board):
            if cell:
                continue
            nxt = list(board)
            nxt[index] = turn
            w, l, d = count_games(tuple(nxt), 3 - turn)
            wins += w
            losses += l
            draws += d
        return wins, losses, draws

    def reachable_positions():
        seen = set()

        def walk(board, turn):
            seen.add(board)
            if winner(board) or all(board):
                return
            for index, cell in enumerate(board):
                if cell:
                    continue
                nxt = list(board)
                nxt[index] = turn
                walk(tuple(nxt), 3 - turn)

        walk((0,) * 9, 1)
        return seen

    def choose_ttt(memo):
        chosen = None
        for cross_cells in combinations(range(9), 3):
            remaining = [cell for cell in range(9) if cell not in cross_cells]
            for circle_cells in combinations(remaining, 3):
                board_list = [0] * 9
                for cell in cross_cells:
                    board_list[cell] = 1
                for cell in circle_cells:
                    board_list[cell] = 2
                board = tuple(board_list)
                if winner(board) or ttt_value(board, 1, memo) != 0:
                    continue
                traps, safe = [], []
                for index, cell in enumerate(board):
                    if cell:
                        continue
                    nxt = list(board)
                    nxt[index] = 1
                    nxt_t = tuple(nxt)
                    if winner(nxt_t) == 1:
                        continue
                    score = ttt_value(nxt_t, 2, memo)
                    if score == 0:
                        safe.append(index)
                    elif score == -1:
                        for reply, mark in enumerate(nxt):
                            if mark:
                                continue
                            answered = list(nxt)
                            answered[reply] = 2
                            if winner(tuple(answered)) == 2:
                                traps.append((index, reply))
                                break
                if traps and safe:
                    candidate = (board, traps[0], safe[0])
                    if chosen is None or candidate < chosen:
                        chosen = candidate
        if chosen is None:
            raise RuntimeError("no illustrative tic-tac-toe position")
        return chosen

    def subtraction_loss(n, memo):
        if n in memo:
            return memo[n]
        if n == 0:
            memo[n] = True
            return True
        loss = all(not subtraction_loss(n - take, memo) for take in (1, 2, 3) if take <= n)
        memo[n] = loss
        return loss

    def two_pile_loss(a, b, memo):
        key = (a, b) if a <= b else (b, a)
        if key in memo:
            return memo[key]
        if a == 0 and b == 0:
            memo[key] = True
            return True
        loss = True
        for take in range(1, a + 1):
            if two_pile_loss(a - take, b, memo):
                loss = False
                break
        if loss:
            for take in range(1, b + 1):
                if two_pile_loss(a, b - take, memo):
                    loss = False
                    break
        memo[key] = loss
        return loss

    def nim_loss(heaps, memo):
        key = tuple(sorted(heaps))
        if key in memo:
            return memo[key]
        if all(heap == 0 for heap in heaps):
            memo[key] = True
            return True
        loss = True
        for index, heap in enumerate(heaps):
            for left in range(heap):
                nxt = list(heaps)
                nxt[index] = left
                if nim_loss(nxt, memo):
                    loss = False
                    break
            if not loss:
                break
        memo[key] = loss
        return loss

    def xor_move(heaps):
        total = 0
        for heap in heaps:
            total ^= heap
        moves = []
        if total == 0:
            return moves
        for index, heap in enumerate(heaps):
            target = heap ^ total
            if target < heap:
                nxt = list(heaps)
                nxt[index] = target
                moves.append(tuple(nxt))
        return moves

    def bite(pos, i, j):
        return frozenset(cell for cell in pos if not (cell[0] >= i and cell[1] >= j))

    def rectangle(rows, cols):
        return frozenset((r, c) for r in range(rows) for c in range(cols))

    def ell(n):
        return frozenset({(r, 0) for r in range(n)} | {(0, c) for c in range(n)})

    def chomp_win(pos, memo):
        if pos in memo:
            return memo[pos]
        win = False
        for i, j in pos:
            if (i, j) == (0, 0):
                continue
            if not chomp_win(bite(pos, i, j), memo):
                win = True
                break
        memo[pos] = win
        return win

    def mirror_defends(n):
        def holds(pos):
            if pos == frozenset({(0, 0)}):
                return True
            for i, j in pos:
                if (i, j) == (0, 0):
                    continue
                after = bite(pos, i, j)
                reply = (j, i)
                if reply not in after:
                    return False
                if not holds(bite(after, reply[0], reply[1])):
                    return False
            return True

        return holds(ell(n))

    def solve_games():
        sub_memo = {}
        for n in range(51):
            assert subtraction_loss(n, sub_memo) == (n % 4 == 0)
            if n % 4:
                good = n % 4
                assert all(
                    subtraction_loss(n - take, sub_memo) == (take == good)
                    for take in (1, 2, 3) if take <= n
                )
        assert subtraction_loss(50, sub_memo) is False and 50 % 4 == 2

        pile_memo = {}
        for a in range(9):
            for b in range(9):
                assert two_pile_loss(a, b, pile_memo) == (a == b)
        assert two_pile_loss(5, 2, pile_memo) is False
        assert two_pile_loss(2, 2, pile_memo) is True
        assert two_pile_loss(1, 2, pile_memo) is False
        assert two_pile_loss(1, 1, pile_memo) is True

        nim_memo = {}
        for a in range(9):
            for b in range(9):
                for c in range(9):
                    heaps = (a, b, c)
                    assert nim_loss(heaps, nim_memo) == ((a ^ b ^ c) == 0)
                    moves = xor_move(heaps)
                    if a ^ b ^ c == 0:
                        assert moves == []
                    else:
                        assert moves
                        assert all(x ^ y ^ z == 0 for x, y, z in moves)
                        assert all(nim_loss(move, nim_memo) for move in moves)
        assert (9 ^ 5 ^ 12) == 0
        assert xor_move((3, 4, 5)) == [(1, 4, 5)]
        assert (1 ^ 4 ^ 5) == 0

        memo = {}
        assert ttt_value((0,) * 9, 1, memo) == 0
        x_wins, o_wins, draws = count_games()
        assert (x_wins, o_wins, draws) == (131184, 77904, 46080)
        assert x_wins + o_wins + draws == 255168
        positions = reachable_positions()
        assert len(positions) == 5478
        lesson = choose_ttt(memo)
        board, (trap, reply), safe = lesson
        assert ttt_value(board, 1, memo) == 0
        trap_board = list(board)
        trap_board[trap] = 1
        answered = list(trap_board)
        answered[reply] = 2
        assert winner(tuple(answered)) == 2
        safe_board = list(board)
        safe_board[safe] = 1
        assert ttt_value(tuple(safe_board), 2, memo) == 0

        chomp_memo = {}
        assert chomp_win(rectangle(1, 1), chomp_memo) is False
        for n in (2, 3, 4):
            assert chomp_win(rectangle(n, n), chomp_memo) is True
            assert chomp_win(ell(n), chomp_memo) is False
            assert mirror_defends(n)
            assert bite(rectangle(n, n), 1, 1) == ell(n)
        corner = bite(rectangle(3, 3), 2, 2)
        assert chomp_win(corner, chomp_memo) is True
        assert bite(corner, 1, 1) == ell(3)
        winning_23 = []
        start_23 = rectangle(2, 3)
        for cell in sorted(start_23):
            if cell == (0, 0):
                continue
            if not chomp_win(bite(start_23, *cell), chomp_memo):
                winning_23.append(cell)
        assert winning_23 == [(1, 2)]

        tree = ("max", (("min", (5, 6)), ("min", (3, 7)), ("min", (4, 9))))
        assert minimax(tree, True) == 5
        seen = []
        assert alphabeta(tree, -10**9, 10**9, True, seen) == 5
        assert seen == [5, 6, 3, 4]
        worse = ("max", (("min", (5, 6)), ("min", (7, 3)), ("min", (4, 9))))
        seen_worse = []
        assert alphabeta(worse, -10**9, 10**9, True, seen_worse) == 5
        assert seen_worse == [5, 6, 7, 3, 4]

        pair = 30 * 30
        assert 10**2 < pair < 10**3
        assert 118.1 < 80 * math.log10(30) < 118.2
        assert 123.5 < 80 * math.log10(35) < 123.6
        assert 359.6 < 150 * math.log10(250) < 359.7
        year = 365.25 * 24 * 3600
        shannon_years = 10**120 * 10**(-6) / year
        assert 10**106 < shannon_years < 10**107
        position_log = (
            sum(math.log10(i) for i in range(1, 65))
            - sum(math.log10(i) for i in range(1, 33))
            - 2 * sum(math.log10(i) for i in range(1, 9))
            - 6 * math.log10(2)
        )
        assert 42 < position_log < 43
        legal_go = int(
            "208168199381979984699478633344862770286522453884530548425639456820927419612738015378525648451698519643907259916015628128546089888314427129715319317557736620397247064840935"
        )
        assert len(str(legal_go)) == 171
        assert math.isclose(legal_go / 10**170, 2.081681994, rel_tol=1e-9)
        assert 0.011 < legal_go / 3**361 < 0.013

        return {
            "lesson": lesson,
            "winning_23": winning_23,
            "shannon_years": shannon_years,
            "position_log": position_log,
            "positions": len(positions),
        }

    def minimax(node, maximizing):
        if isinstance(node, int):
            return node
        _, children = node
        scores = [minimax(child, not maximizing) for child in children]
        return max(scores) if maximizing else min(scores)

    def alphabeta(node, alpha, beta, maximizing, seen):
        if isinstance(node, int):
            seen.append(node)
            return node
        _, children = node
        if maximizing:
            value = -10**9
            for child in children:
                value = max(value, alphabeta(child, alpha, beta, False, seen))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        value = 10**9
        for child in children:
            value = min(value, alphabeta(child, alpha, beta, True, seen))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    def candy_row():
        labels = [(n, n % 4 == 0, "无好手" if n % 4 == 0 else f"拿 {n % 4}") for n in range(9)]
        xs = [28 + n * 79 for n in range(9)]
        frames = []
        for n in range(9):
            start = 100 * n / 9
            stop = 100 * (n + 0.78) / 9
            dx = xs[n] - xs[0]
            frames.append(f"{start:.2f}%{{opacity:1;transform:translateX({dx}px)}}")
            frames.append(f"{stop:.2f}%{{opacity:1;transform:translateX({dx}px)}}")
        frames.append(f"100%{{opacity:0;transform:translateX({xs[-1] - xs[0]}px)}}")

        anim_css = (
            ".walker{opacity:0;animation:walk 7.5s linear 1}"
            f"@keyframes walk{{{''.join(frames)}}}"
            "@media(prefers-reduced-motion:reduce){.walker{animation:none;opacity:0}}"
        )
        els = header(
            "单堆拿糖（每次 1～3 颗）：从 0 颗往回贴标签，4 的倍数全是必败格",
            "橙虚线格 = 轮到谁走谁必败；蓝实线格 = 有唯一一步把对手推进虚线格。动画橙框演示从 0 到 8 的倒推顺序。",
        )
        els.append(card(20, 62, 720, 186))
        for n, (count, loss, action) in enumerate(labels):
            x = xs[n]
            els += [
                f'<rect x="{x}" y="82" width="68" height="106" rx="9" '
                f'fill="{LOSS_FILL if loss else WIN_FILL}" '
                f'stroke="{ORANGE if loss else BLUE}" stroke-width="1.5"'
                + (' stroke-dasharray="4 3"' if loss else "")
                + "/>",
                txt(x + 34, 112, f"{count}颗", 13.5, INK, "middle", weight="700"),
                txt(x + 34, 140, "必败" if loss else "必胜", 12.5, ORANGE if loss else BLUE, "middle", weight="700"),
                txt(x + 34, 168, action, 11.2, MUTED, "middle"),
            ]
        els.append(
            f'<rect class="walker" x="{xs[0]}" y="79" width="68" height="112" rx="10" '
            f'fill="none" stroke="{ORANGE}" stroke-width="2.6"/>'
        )
        els.append(f'<line x1="36" y1="210" x2="718" y2="210" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#arr-blue)"/>')
        els.append(txt(380, 232, "倒推规律：50 = 4×12 + 2  ⇒  开局先手唯一胜着是拿 2 颗（留给对手 48），之后对手拿 r 你就拿 4−r", 11.8, INK, "middle", weight="600"))
        return figure(
            264,
            "单堆拿糖从零颗倒推到八颗的胜负表",
            "零到八颗糖每次拿一到三颗，零、四、八为橙色虚线必败格，其余为蓝色实线必胜格并标出唯一必胜拿法。",
            els,
            extra_css=anim_css,
        )

    def two_piles():
        els = header(
            "两堆拿糖：只有“两堆一样多”的对角线必败，其余全靠对称模仿获胜",
            "左图：甲堆、乙堆各 0～5 颗的完整倒推表；右图：开局 (5, 2) 先削平差额变成 (2, 2)，此后镜像模仿。",
        )
        els.append(card(20, 62, 366, 290))
        els.append(txt(36, 84, "① 0～5 倒推网格（列=甲堆，行=乙堆）", 12.8, INK, weight="600"))

        ox, oy, sz = 78, 110, 38
        for a in range(6):
            els.append(txt(ox + a * sz + sz / 2, oy - 6, f"甲{a}", 10.5, MUTED, "middle"))
            els.append(txt(ox - 8, oy + a * sz + 23, f"乙{a}", 10.5, MUTED, "end"))
            for b in range(6):
                loss = a == b
                x, y = ox + a * sz, oy + b * sz
                els.append(
                    f'<rect x="{x + 2}" y="{y + 2}" width="{sz - 4}" height="{sz - 4}" rx="5" '
                    f'fill="{LOSS_FILL if loss else WIN_FILL}" '
                    f'stroke="{ORANGE if loss else BLUE}" stroke-width="1.2"'
                    + (' stroke-dasharray="3 2"' if loss else "")
                    + "/>"
                )
                els.append(txt(x + sz / 2, y + 15.5, f"{a},{b}", 9.6, MUTED, "middle"))
                els.append(txt(x + sz / 2, y + 29, "败" if loss else "胜", 10.5, ORANGE if loss else BLUE, "middle", weight="700"))

        # Right panel: Mirror strategy walkthrough
        els.append(card(400, 62, 340, 290))
        els.append(txt(416, 84, "② 实战演示：把“相等”像烫手山芋扔回去", 12.8, INK, weight="600"))
        steps = [
            ("开局 (5, 2) 不相等", "先手从甲堆拿走差额 3 颗 → 变成 (2, 2)", BLUE_SOFT, BLUE),
            ("对手面对 (2, 2) 必败格", "无论拿哪堆都会打破平衡，例：甲拿 1 → (1, 2)", ORANGE_SOFT, ORANGE),
            ("先手启动“照镜子”", "对手刚在哪堆拿 t，你就在另一堆也拿 t → (1, 1)", GREEN_SOFT, GREEN),
            ("终局对手拿完一堆 → (0, 1)", "先手拿走另一堆最后一颗 → (0, 0)，先手胜！", SLATE_SOFT, INK),
        ]
        for i, (sh, sb, bg_c, fg_c) in enumerate(steps):
            sy = 100 + i * 56
            els.append(card(416, sy, 308, 46, rx=7, fill=bg_c, stroke=fg_c if i < 3 else BORDER))
            els.append(txt(428, sy + 18, sh, 11.6, INK, weight="600"))
            els.append(txt(428, sy + 36, sb, 11.2, fg_c, weight="600" if i in (0, 2) else None))

        return figure(
            368,
            "两堆拿糖胜负网格与镜像模仿策略",
            "左侧6乘6网格展示两堆相等的对角线为必败格；右侧分四步演示从5比2削平为2比2后镜像模仿获胜。",
            els,
        )

    def three_piles():
        els = header(
            "三堆尼姆游戏（Nim）为什么突然冒出二进制？把它想成“按 8、4、2、1 分袋配对”！",
            "把每堆糖拆成 8、4、2、1 颗的小袋子：每种规格的袋子如果是偶数个，就能两两配对玩刚才的“照镜子”！",
        )

        # Left panel: (9, 5, 12) all paired!
        els.append(card(20, 62, 352, 272))
        els.append(txt(36, 84, "① 安全必败局 (9, 5, 12)：所有规格袋子全都成双！", 12.4, INK, weight="600"))
        cols = (132, 184, 236, 288)
        for cx, h_lbl in zip(cols, ("8颗袋", "4颗袋", "2颗袋", "1颗袋")):
            els.append(txt(cx, 110, h_lbl, 11, MUTED, "middle", weight="600"))

        rows_1 = [("甲=9", (1, 0, 0, 1)), ("乙=5", (0, 1, 0, 1)), ("丙=12", (1, 1, 0, 0))]
        for r_i, (r_lbl, bits) in enumerate(rows_1):
            ry = 122 + r_i * 38
            els.append(txt(44, ry + 19, r_lbl, 12, INK, weight="600"))
            for c_i, b in enumerate(bits):
                cx = cols[c_i]
                els.append(
                    f'<rect x="{cx - 18}" y="{ry}" width="36" height="28" rx="6" '
                    f'fill="{GREEN_SOFT if b else "#f8fafc"}" stroke="{GREEN if b else HAIRLINE}" stroke-width="1.2"/>'
                )
                els.append(txt(cx, ry + 19, b, 12.5, GREEN if b else MUTED, "middle", weight="700" if b else None, cls="mono"))

        els.append(f'<line x1="40" y1="242" x2="344" y2="242" stroke="{HAIRLINE}" stroke-width="1"/>')
        els.append(txt(44, 262, "竖列袋数", 11.2, MUTED))
        for cx, cnt in zip(cols, ("2个(偶)", "2个(偶)", "0个(偶)", "2个(偶)")):
            els.append(txt(cx, 262, cnt, 10.8, GREEN, "middle", weight="700"))
        els.append(pill(36, 284, "异或和 9⊕5⊕12 = 0：谁先拿都会拆散一对，必败", fg=ORANGE, bg=ORANGE_SOFT, w=320, h=24, size=11.2))

        # Right panel: (3, 4, 5) -> lonely 2-bag in heap 3 -> take 2 to make (1, 4, 5)!
        els.append(card(388, 62, 352, 272))
        els.append(txt(404, 84, "② 必胜局 (3, 4, 5)：揪出落单的“2颗袋”拿走！", 12.4, INK, weight="600"))
        cols2 = (496, 560, 624)
        for cx, h_lbl in zip(cols2, ("4颗袋", "2颗袋", "1颗袋")):
            els.append(txt(cx, 110, h_lbl, 11, MUTED, "middle", weight="600"))

        rows_2 = [("甲=3 → 改1", (0, 1, 1)), ("乙=4", (1, 0, 0)), ("丙=5", (1, 0, 1))]
        for r_i, (r_lbl, bits) in enumerate(rows_2):
            ry = 122 + r_i * 38
            els.append(txt(406, ry + 19, r_lbl, 11.8, ORANGE if r_i == 0 else INK, weight="600"))
            for c_i, b in enumerate(bits):
                cx = cols2[c_i]
                lonely = r_i == 0 and c_i == 1
                fill_c = ORANGE_SOFT if lonely else (GREEN_SOFT if b else "#f8fafc")
                str_c = ORANGE if lonely else (GREEN if b else HAIRLINE)
                els.append(
                    f'<rect x="{cx - 20}" y="{ry}" width="40" height="28" rx="6" '
                    f'fill="{fill_c}" stroke="{str_c}" stroke-width="{1.9 if lonely else 1.2}"/>'
                )
                els.append(txt(cx, ry + 19, "1→0" if lonely else b, 11.5 if lonely else 12.5, ORANGE if lonely else (GREEN if b else MUTED), "middle", weight="700", cls="mono"))

        els.append(f'<line x1="404" y1="242" x2="716" y2="242" stroke="{HAIRLINE}" stroke-width="1"/>')
        els.append(txt(406, 262, "原本袋数", 11.2, MUTED))
        els.append(txt(cols2[0], 262, "2个(成对)", 10.8, GREEN, "middle", weight="600"))
        els.append(txt(cols2[1], 262, "1个(落单!)", 10.8, ORANGE, "middle", weight="700"))
        els.append(txt(cols2[2], 262, "2个(成对)", 10.8, GREEN, "middle", weight="600"))
        els.append(pill(404, 284, "唯一胜着：从甲堆拿走 2 颗变成 (1, 4, 5)，恢复全偶！", fg=BLUE, bg=BLUE_SOFT, w=320, h=24, size=11.2))

        return figure(
            350,
            "三堆尼姆游戏的二进制糖袋配对图解",
            "左图将9、5、12拆为8、4、2、1袋，每列均为偶数个；右图展示3、4、5中2颗袋落单，从3中拿走2变为1、4、5即可恢复全列成对。",
            els,
        )

    def tic_tac_toe(lesson):
        board, (trap, reply), safe = lesson
        assert board == (0, 0, 0, 1, 2, 2, 2, 1, 1)
        assert (trap, reply, safe) == (0, 2, 2)
        trap_board = list(board)
        trap_board[trap] = 1
        answered = list(trap_board)
        answered[reply] = 2
        safe_board = list(board)
        safe_board[safe] = 1

        def draw(board_state, x, y, highlight, win_line=None):
            sz = 44
            parts = []
            for row in range(3):
                for col in range(3):
                    idx = row * 3 + col
                    px, py = x + col * sz, y + row * sz
                    hi = idx in highlight
                    parts.append(
                        f'<rect x="{px}" y="{py}" width="40" height="40" rx="6" '
                        f'fill="{ORANGE_SOFT if hi else "#ffffff"}" '
                        f'stroke="{ORANGE if hi else HAIRLINE}" stroke-width="{1.7 if hi else 1.2}"/>'
                    )
                    mark = {0: "", 1: "×", 2: "○"}[board_state[idx]]
                    if mark:
                        col_m = BLUE if mark == "×" else ORANGE
                        parts.append(txt(px + 20, py + 26, mark, 18, col_m, "middle", weight="700"))
            if win_line:
                (r1, c1), (r2, c2) = win_line
                parts.append(
                    f'<line x1="{x + c1 * sz + 20}" y1="{y + r1 * sz + 20}" '
                    f'x2="{x + c2 * sz + 20}" y2="{y + r2 * sz + 20}" '
                    f'stroke="{ORANGE}" stroke-width="2.4" stroke-dasharray="4 2"/>'
                )
            return parts

        els = header(
            "井字棋残局样品：理论值是“和棋”，但三个空位里只有唯一一格能守住！",
            "当前轮到 × 落子。下错左上角会被 ○ 斜线绝杀；只有抢占右上角才能守和（正中空位同样必败）。",
        )
        cards_cfg = [
            (20, "① 当前局面（轮到 ×）", board, set(), None, "完整搜索值 = 和棋", SLATE_SOFT, BODY),
            (268, "② 误占左上 → 被斜连绝杀", answered, {trap, reply}, ((0, 2), (2, 0)), "× 下左上，○ 占右上即赢", ORANGE_SOFT, ORANGE),
            (516, "③ 唯一正解：抢占右上", tuple(safe_board), {safe}, None, "堵住斜线，稳稳守住和棋", GREEN_SOFT, GREEN),
        ]
        for bx, btitle, bstate, bhi, wline, bfoot, bg_c, fg_c in cards_cfg:
            els.append(card(bx, 62, 224, 224))
            els.append(txt(bx + 112, 84, btitle, 12.4, INK, "middle", weight="600"))
            els += draw(bstate, bx + 48, 100, bhi, win_line=wline)
            els.append(pill(bx + 14, 248, bfoot, fg=fg_c, bg=bg_c, w=196, h=24, size=11))

        return figure(
            302,
            "井字棋一步陷阱与唯一守和着法对比",
            "左盘轮到×落子，理论值为和棋；中盘×误下左上角被○占右上角连成斜线获胜；右盘×占右上角成为三个空位中唯一守和选择。",
            els,
        )

    def chocolate():
        def squares(ox, oy, removed):
            parts = []
            sz = 30
            for row in range(2, -1, -1):
                for col in range(3):
                    x, y = ox + col * sz, oy + (2 - row) * sz
                    if (row, col) in removed:
                        parts.append(
                            f'<rect x="{x}" y="{y}" width="27" height="27" rx="4" '
                            'fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.1" stroke-dasharray="3 2"/>'
                        )
                        continue
                    poison = (row, col) == (0, 0)
                    parts.append(
                        f'<rect x="{x}" y="{y}" width="27" height="27" rx="4" '
                        f'fill="{"#7c2d12" if poison else "#eab676"}" stroke="#9a5b25" stroke-width="1.2"/>'
                    )
                    if poison:
                        parts.append(txt(x + 13.5, y + 18, "毒", 11, "#ffffff", "middle", weight="700"))
            return parts

        gone_corner = {(2, 2)}
        gone_ell = {(1, 1), (2, 1), (1, 2), (2, 2)}
        gone_reply = gone_ell | {(2, 0), (0, 2)}

        els = header(
            "有毒巧克力（Chomp）与“策略窃取”：试探的那一口，不等于真正该下的第一口",
            "左下角有毒，每次咬掉一格及其右上方所有格。虚线格表示已被吃掉。",
        )

        # Left card: Tempting corner bite loses!
        els.append(card(20, 62, 352, 232))
        els.append(txt(36, 84, "① 假想试探：先手只咬右上角，反而送对手赢", 12.4, INK, weight="600"))
        els += squares(54, 108, gone_corner)
        els.append(txt(99, 214, "先手只咬右上角", 11, MUTED, "middle"))
        els.append(f'<line x1="156" y1="152" x2="206" y2="152" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')
        els.append(txt(181, 144, "后手惩罚", 10.5, ORANGE, "middle", weight="600"))
        els += squares(222, 108, gone_ell)
        els.append(txt(267, 214, "后手咬中心留 L 形", 11, ORANGE, "middle", weight="600"))
        els.append(pill(36, 254, "精髓：后手这招“留 L 形”，先手开局就能直接偷来用！", fg=ORANGE, bg=ORANGE_SOFT, w=320, h=24, size=11))

        # Right card: Stealing the L move directly on move 1!
        els.append(card(388, 62, 352, 232))
        els.append(txt(404, 84, "② 真正必胜着：第一口直接咬出等臂 L 形！", 12.4, INK, weight="600"))
        els += squares(422, 108, gone_ell)
        els.append(txt(467, 214, "先手开局直接留 L", 11, BLUE, "middle", weight="600"))
        els.append(f'<line x1="524" y1="152" x2="574" y2="152" stroke="{GREEN}" stroke-width="1.6" marker-end="url(#arr-green)"/>')
        els.append(txt(549, 144, "对称回应", 10.5, GREEN, "middle", weight="600"))
        els += squares(590, 108, gone_reply)
        els.append(txt(635, 214, "对手咬右端→你咬上端", 11, GREEN, "middle", weight="600"))
        els.append(pill(404, 254, "注意：2×3 矩形的必胜第一口却变回“只咬右上角”", fg=BLUE, bg=BLUE_SOFT, w=320, h=24, size=11))

        return figure(
            310,
            "三乘三有毒巧克力的试探反证与对称必胜法",
            "左图先手只吃右上角会被后手吃掉中心留下对称L形而落败；右图先手开局直接吃成对称L形并镜像回应获胜。",
            els,
        )

    def hex_board():
        # 5x5 Hex board! Verify BFS connectivity on the concrete filled position:
        # 1 = Blue (connects Top row r=0 to Bottom row r=4), 2 = Orange (connects Left col c=0 to Right col c=4).
        grid = [
            [2, 2, 1, 2, 1],
            [1, 2, 1, 1, 2],
            [2, 1, 2, 1, 2],
            [2, 1, 1, 2, 1],
            [1, 2, 2, 1, 2],
        ]
        # Check Blue 6-neighbor hex connectivity from row 0 to row 4:
        # Hex neighbors of (r, c): (r-1,c), (r-1,c+1), (r,c-1), (r,c+1), (r+1,c-1), (r+1,c)
        def connected(player):
            starts = [(0, c) for c in range(5) if grid[0][c] == 1] if player == 1 else [(r, 0) for r in range(5) if grid[r][0] == 2]
            seen = set(starts)
            stack = list(starts)
            while stack:
                r, c = stack.pop()
                for dr, dc in ((-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 5 and 0 <= nc < 5 and grid[nr][nc] == player and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            return any(r == 4 for r, _ in seen) if player == 1 else any(c == 4 for _, c in seen)

        assert connected(1) is True and connected(2) is False

        els = header(
            "六贯棋（Hex）：棋盘长什么样？为什么下满时绝不可能出现“和棋”？",
            "蓝方要把上下两条蓝边连成通路，橙方要把左右两条橙边连成通路（六边形相邻格共边即相连）。",
        )

        els.append(card(20, 62, 396, 248))
        els.append(txt(36, 84, "① 5×5 六贯棋盘：通水 vs 筑坝，必有一方贯通！", 12.6, INK, weight="600"))

        R = 16.5  # hex circumradius (pointy-top)
        dx = math.sqrt(3) * R
        dy = 1.5 * R
        ox, oy = 112.0, 128.0

        def hex_pts(cx, cy, rad):
            return " ".join(
                f"{cx + rad * math.cos(math.radians(30 + 60 * k)):.1f},{cy + rad * math.sin(math.radians(30 + 60 * k)):.1f}"
                for k in range(6)
            )

        # Colored goal edge bars
        els.append(txt(218, 104, "蓝方北岸目标边", 10.8, BLUE, "middle", weight="700"))
        els.append(txt(254, 294, "蓝方南岸目标边", 10.8, BLUE, "middle", weight="700"))
        els.append(txt(64, 206, "橙西岸", 10.8, ORANGE, "middle", weight="700"))
        els.append(txt(368, 186, "橙东岸", 10.8, ORANGE, "middle", weight="700"))

        win_path = [(0, 2), (1, 2), (2, 1), (3, 1), (4, 0)]
        for r in range(5):
            for c in range(5):
                cx = ox + c * dx + r * (dx / 2)
                cy = oy + r * dy
                is_blue = grid[r][c] == 1
                on_win = (r, c) in win_path
                els.append(
                    f'<polygon points="{hex_pts(cx, cy, R - 1.0)}" '
                    f'fill="{BLUE_SOFT if is_blue else ORANGE_SOFT}" '
                    f'stroke="{BLUE if is_blue else ORANGE}" stroke-width="{2.1 if on_win else 1.2}"/>'
                )
                els.append(
                    f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{5.2 if on_win else 4.0}" '
                    f'fill="{BLUE if is_blue else ORANGE}" fill-opacity="{1.0 if on_win else 0.55}"/>'
                )

        # Draw bright connecting line along Blue's winning chain
        chain_xy = " ".join(f"{ox + c * dx + r * (dx / 2):.1f},{oy + r * dy:.1f}" for r, c in win_path)
        els.append(f'<polyline points="{chain_xy}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')

        # Right panel: Why Nash's Strategy Stealing proves First Player Wins!
        els.append(card(430, 62, 310, 248))
        els.append(txt(446, 84, "② 纳什的“两步绝杀”存在性证明", 12.6, INK, weight="600"))

        els.append(card(446, 100, 278, 86, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(458, 120, "第一步：为什么不可能和棋？（通水定理）", 11.6, INK, weight="700"))
        els.append(txt(458, 140, "把蓝格当河道、橙格当堤坝。从北岸放水，", 11.2, BODY))
        els.append(txt(458, 158, "水若流不到南岸，唯一可能是西到东被橙坝", 11.2, BODY))
        els.append(txt(458, 176, "彻底堵死——堵死恰恰说明橙方连赢了！", 11.2, BLUE, weight="600"))

        els.append(card(446, 198, 278, 96, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(458, 218, "第二步：策略窃取 ⇒ 先手必胜！", 11.6, INK, weight="700"))
        els.append(txt(458, 238, "• 棋盘上多一枚己方棋子永远不会帮倒忙；", 11.2, BODY))
        els.append(txt(458, 256, "• 假如后手有必胜秘籍，先手随便下一子再", 11.2, BODY))
        els.append(txt(458, 274, "  假装自己是后手就能偷走秘籍；又无和棋，", 11.2, BODY))
        els.append(txt(458, 289, "⇒ 11×11 标准六贯棋必是先手胜（但没人算得出谱）", 10.8, GREEN, weight="700"))

        return figure(
            326,
            "六贯棋盘结构、无和棋通水直觉与纳什先手必胜证明",
            "左图展示5乘5菱形六边形六贯棋盘，蓝色实线连接上下北南两岸获胜并阻断橙色东西连线；右图总结无和棋定理加策略窃取如何推出先手必胜。",
            els,
        )

    def alpha_beta():
        els = header(
            "极小化极大（Minimax）与 α-β 剪枝：我挑最高分、对手挑最低分，废枝直接剪掉",
            "先手（MAX）想要大数字，后手（MIN）专挑小数字坑你。一旦某分支上限还不如手头保底分，后面叶子全免检！",
        )
        els.append(card(20, 62, 720, 266))

        root = (380, 106)
        mins = ((156, 186), (380, 186), (604, 186))
        leaves = (
            ((106, 272, "5", "①读"), (206, 272, "6", "②读")),
            ((330, 272, "3", "③读"), (430, 272, "7", "✂剪掉")),
            ((554, 272, "4", "④读"), (654, 272, "9", "✂剪掉")),
        )

        for (cx, cy), pairs in zip(mins, leaves):
            els.append(f'<line x1="{root[0]}" y1="{root[1] + 22}" x2="{cx}" y2="{cy - 22}" stroke="{BLUE}" stroke-width="1.6"/>')
            for lx, ly, _, tag in pairs:
                pruned = "剪" in tag
                els.append(
                    f'<line x1="{cx}" y1="{cy + 22}" x2="{lx}" y2="{ly - 20}" '
                    f'stroke="{ORANGE if pruned else BLUE}" stroke-width="1.5"'
                    + (' stroke-dasharray="4 3"' if pruned else "")
                    + "/>"
                )

        # Root MAX node
        els.append(card(root[0] - 92, root[1] - 22, 184, 44, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.7))
        els.append(txt(root[0], root[1] - 3, "先手 MAX（挑最大）", 12, BLUE, "middle", weight="700"))
        els.append(txt(root[0], root[1] + 14, "最终敲定得分 = 5", 11.5, INK, "middle", weight="600"))

        # MIN nodes
        min_notes = ("后手选 min(5,6)=5", "看到 3 ≤ 5，立刻停！", "看到 4 ≤ 5，立刻停！")
        for (cx, cy), mnote in zip(mins, min_notes):
            els.append(card(cx - 78, cy - 22, 156, 44, rx=8, fill="#ffffff", stroke=INK, sw=1.3))
            els.append(txt(cx, cy - 3, "后手 MIN（压最小）", 11.5, INK, "middle", weight="600"))
            els.append(txt(cx, cy + 14, mnote, 10.8, ORANGE if "停" in mnote else GREEN, "middle", weight="600"))

        # Leaf nodes
        for pairs in leaves:
            for lx, ly, val, tag in pairs:
                pruned = "剪" in tag
                els.append(
                    card(
                        lx - 36,
                        ly - 20,
                        72,
                        40,
                        rx=7,
                        fill=SLATE_SOFT if pruned else GREEN_SOFT,
                        stroke=HAIRLINE if pruned else GREEN,
                        sw=1.3,
                        dash="4 3" if pruned else None,
                    )
                )
                els.append(txt(lx, ly - 2, f"估分 {val}", 12, MUTED if pruned else INK, "middle", weight="700"))
                els.append(txt(lx, ly + 14, tag, 10.5, ORANGE if pruned else GREEN, "middle", weight="600"))

        els.append(txt(36, 316, "读左支拿到保底 5 分后，中支刚翻开 3 就知道后手绝不会给超过 3 分，旁边的 7 哪怕是 100 分也轮不到你，直接剪掉！", 11.2, BODY))

        return figure(
            344,
            "极小化极大博弈树与 α-β 剪枝步骤图",
            "根节点先手MAX取最大，第二层后手MIN取最小。左支得出保底5分后，中支读到3、右支读到4均不超过5，直接剪去叶子7与9。",
            els,
        )

    def main():
        report = solve_games()
        board, (trap, reply), safe = report["lesson"]
        OUT.mkdir(parents=True, exist_ok=True)
        pictures = (
            ("candy-row", candy_row()),
            ("two-piles", two_piles()),
            ("three-piles", three_piles()),
            ("tic-tac-toe", tic_tac_toe(report["lesson"])),
            ("chocolate", chocolate()),
            ("hex-board", hex_board()),
            ("alpha-beta", alpha_beta()),
        )
        for name, content in pictures:
            root = ET.fromstring(content)
            assert root.get("width") == str(WIDTH)
            assert root.get("viewBox") == f'0 0 {WIDTH} {root.get("height")}'
            assert root.find("{http://www.w3.org/2000/svg}title") is not None or root.find("title") is not None
            (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
            print(f"Wrote {name}.svg")

    main()


@register("p-np", "P 与 NP：证书验证、指数枚举与归约流程", "algebra_logic")
def build_p_np():
    INK, MUTED, BLUE, ORANGE = K_INK, K_MUTED, K_BLUE, K_ORANGE

    text, document = k_text, b_document

    OUT = REPO_ROOT / "assets" / "images" / "p-np"

    def panel(y, height):
        return (
            f'<rect x="24" y="{y}" width="672" height="{height}" rx="16" '
            'fill="#fff" stroke="#c9d6df" stroke-width="2"/>'
        )

    def certificate():
        coins = (3, 5, 6, 9, 12)
        target = 17
        valid, invalid = (1, 4), (0, 2, 3)
        assert sum(coins[i] for i in valid) == target
        assert sum(coins[i] for i in invalid) == 18
        subsets = [[i for i in range(len(coins)) if mask >> i & 1] for mask in range(2 ** len(coins))]
        solutions = [subset for subset in subsets if sum(coins[i] for i in subset) == target]
        assert solutions == [[0, 1, 3], [1, 4]]
        elements = [
            text(36, 48, "找到一个组合，与检查一份清单", 32),
            text(36, 88, "每枚最多用一次；目标：恰好凑出 17。", 25, MUTED),
            panel(120, 172),
        ]
        for i, value in enumerate(coins):
            x = 100 + i * 130
            elements += [
                f'<circle cx="{x}" cy="189" r="36" fill="#e1f0f5" stroke="{BLUE}" stroke-width="2"/>',
                text(x, 201, str(value), 32, BLUE, "middle"),
                text(x, 267, f"第 {i+1} 枚", 24, MUTED, "middle"),
            ]
        elements += [
            panel(320, 218),
            text(44, 364, "① 证书：选第 2、5 枚", 29),
            text(44, 413, "核对：编号合法，没有重复。", 26),
            text(44, 461, "求和：5 + 12 = 17。", 28, BLUE),
            text(44, 509, "结论：存在，回答“是”。", 27, BLUE),
            panel(565, 218),
            text(44, 609, "② 另一份证书：选第 1、3、4 枚", 28),
            text(44, 658, "求和：3 + 6 + 9 = 18，不是 17。", 27, ORANGE),
            text(44, 706, "只能排除这一份组合。", 27),
            text(44, 754, "不能由此推出：所有组合都不行。", 27),
            text(36, 832, "5 枚 → 2⁵ = 32 个候选；检查一份不必枚举全部。", 24, MUTED),
        ]
        return document(
            870, "子集和的证书与验证",
            "五枚硬币面值三、五、六、九、十二，每枚最多使用一次，目标十七。"
            "选择第二和第五枚得到十七，是有效证书；第一、三、四枚得到十八，"
            "只能排除该组合，不能据此认定无解。共三十二个候选子集。",
            elements,
        )

    def enumeration():
        rate = 10**9
        seconds_per_year = 365.25 * 24 * 60 * 60
        entries = [
            (30, "约 10.7 亿个", "约 1.07 秒"),
            (60, "约 1.15 × 10¹⁸ 个", "约 36.5 年"),
            (100, "约 1.27 × 10³⁰ 个", "约 4.02 × 10¹³ 年"),
        ]
        assert math.isclose(2**30 / rate, 1.073741824)
        assert 36.5 < 2**60 / rate / seconds_per_year < 36.6
        assert 4.01e13 < 2**100 / rate / seconds_per_year < 4.03e13
        elements = [
            text(36, 48, "每多一个选／不选，候选数就翻倍", 32),
            text(36, 88, "乐观假设：每秒检查 10 亿个候选，忽略其他成本。", 24, MUTED),
        ]
        for index, (n, count, duration) in enumerate(entries):
            top = 120 + index * 205
            elements += [
                panel(top, 180),
                text(44, top + 42, f"{n} 个物品 → 2 的 {n} 次方个候选", 28),
                text(44, top + 91, count, 29, BLUE),
                text(44, top + 143, f"全部检查：{duration}", 29, ORANGE),
            ]
        elements += [
            text(36, 787, "这是完整穷举的算账，不是任意算法的时间下界。", 25),
            text(36, 831, "实际可能提前找到解；聪明算法也可能避开完整枚举。", 24, MUTED),
        ]
        return document(
            870, "子集候选数的指数增长",
            "三十、六十和一百个物品，分别有二的对应次方个候选子集。"
            "假设每秒检查十亿个，完整枚举约需一点零七秒、三十六点五年、"
            "四点零二乘十的十三次方年。这是枚举估算，不是复杂性下界。",
            elements,
        )

    def reduction_flow():
        elements = [
            text(36, 48, "A ≤ₚ B：把 A 的输入交给 B", 32),
            text(36, 88, "输入沿箭头流动；描边提示次序，不表示耗时。", 24, MUTED),
            '<style>.stage{animation:focus 2s linear 1 forwards}.s2{animation-delay:2s}'
            '.s3{animation-delay:4s}@keyframes focus{0%,90%{stroke:#ad4f16;stroke-width:6}'
            '100%{stroke:#176786;stroke-width:2}}'
            '@media(prefers-reduced-motion:reduce){.stage{animation:none}}</style>',
        ]
        stages = [
            (120, "① A 的输入 x → 多项式时间翻译", "得到 B 的输入 f(x)，不能偷偷先解出 A。"),
            (355, "② 假设有一台 B 的快速判定器", "把 f(x) 交进去；此处是假设，不是已实现。"),
            (590, "③ 返回同一个“是／否”答案", "A 的原输入为“是” ⇔ B 的新输入为“是”。"),
        ]
        for i, (top, heading, detail) in enumerate(stages):
            elements += [
                f'<rect class="stage s{i+1}" x="24" y="{top}" width="672" height="160" '
                f'rx="16" fill="#fff" stroke="{BLUE}" stroke-width="2"/>',
                text(44, top + 51, heading, 28),
                text(44, top + 108, detail, 24, MUTED),
            ]
            if i < 2:
                elements += [
                    f'<path d="M360 {top+174}V{top+218}" stroke="{BLUE}" stroke-width="4"/>',
                    f'<path d="M360 {top+225}L349 {top+209}H371Z" fill="{BLUE}"/>',
                ]
        elements += [
            text(36, 807, "如果 B 能快速判定，A 就也能快速判定。", 27, BLUE),
            text(36, 854, "要证明 B 很难：从已知难的 A，归约到 B。", 27),
            text(36, 899, "一次转换、一个新实例：本文只用多对一归约。", 24, MUTED),
        ]
        return document(
            935, "多项式时间多对一归约的方向",
            "从问题A的输入出发，多项式时间转换成B的输入，交给假设存在的快速判定器，"
            "把其是或否答案作为A的答案。转换保留两个方向。三个步骤一直可读，"
            "描边依次提示流程，播放一次后保持完整静态信息；减少动态效果时不播放。",
            elements,
        )

    def cycle_cost(order, weights):
        return sum(weights[a][b] for a, b in zip(order, order[1:] + order[:1]))

    def tours(n):
        return [(0,) + rest for rest in itertools.permutations(range(1, n))]

    def encoded_distances(n, edges):
        return [
            [0 if i == j else 1 if tuple(sorted((i, j))) in edges else 2 for j in range(n)]
            for i in range(n)
        ]

    def check_reduction():
        count = 0
        for n in (3, 4, 5):
            pairs = list(itertools.combinations(range(n), 2))
            orders = tours(n)
            for mask in range(2 ** len(pairs)):
                edges = {edge for i, edge in enumerate(pairs) if mask >> i & 1}
                distances = encoded_distances(n, edges)
                original_yes = any(
                    all(tuple(sorted((a, b))) in edges for a, b in zip(order, order[1:] + order[:1]))
                    for order in orders
                )
                transformed_yes = min(cycle_cost(order, distances) for order in orders) <= n
                assert original_yes == transformed_yes
                assert all(
                    distances[a][c] <= distances[a][b] + distances[b][c]
                    for a, b, c in itertools.product(range(n), repeat=3)
                )
                count += 1
        assert count == 1096

    def graph_vertices(points, edges):
        result = []
        for a, b in edges:
            x1, y1 = points[a]
            x2, y2 = points[b]
            result.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{BLUE}" stroke-width="3"/>')
        for i, (x, y) in enumerate(points):
            result += [
                f'<circle cx="{x}" cy="{y}" r="22" fill="#fff" stroke="{BLUE}" stroke-width="2"/>',
                text(x, y + 9, "ABCD"[i], 26, INK, "middle"),
            ]
        return result

    def hamilton_to_tsp():
        check_reduction()
        cases = [
            ({(0, 1), (1, 2), (2, 3), (0, 3)}, "① 原图有环 → 新问题也回答“是”",
             "A → B → C → D → A", "1 + 1 + 1 + 1 = 4，满足预算 4。", 4),
            ({(0, 1), (0, 2), (0, 3)}, "② 原图无环 → 新问题也回答“否”",
             "A → B → C → D → A", "1 + 2 + 2 + 1 = 6，最短也超预算 4。", 6),
        ]
        elements = [
            text(36, 48, "有边设为 1，无边设为 2，预算设为 n", 31),
            text(36, 88, "四点演示；新问题使用完整距离矩阵。", 24, MUTED),
        ]
        for index, (edges, heading, route, conclusion, expected) in enumerate(cases):
            top = 120 + index * 475
            distances = encoded_distances(4, edges)
            assert min(cycle_cost(tour, distances) for tour in tours(4)) == expected
            elements += [
                panel(top, 450),
                text(44, top + 42, heading, 28),
                text(185, top + 88, "原图", 25, MUTED, "middle"),
                text(510, top + 88, "新距离", 25, MUTED, "middle"),
            ]
            points = [(105, top + 143), (245, top + 143), (245, top + 283), (105, top + 283)]
            elements += graph_vertices(points, edges)
            for j, label in enumerate("ABCD"):
                elements += [
                    text(450 + 55 * j, top + 133, label, 24, MUTED, "middle"),
                    text(400, top + 179 + 43 * j, label, 24, MUTED, "middle"),
                ]
                for k, cost in enumerate(distances[j]):
                    elements.append(text(450 + 55 * k, top + 179 + 43 * j, str(cost), 25, INK, "middle"))
            elements += [
                text(44, top + 353, f"最短路线之一：{route}", 25),
                text(44, top + 405, conclusion, 26, BLUE if expected == 4 else ORANGE),
            ]
        elements += [
            text(36, 1112, "一般理由：n 段各至少为 1，预算 n 迫使每段都是 1。", 24),
            text(36, 1158, "图上位置不代表成本；矩阵的 1／2 才是构造的距离。", 24, MUTED),
        ]
        return document(
            1195, "哈密顿回路到旅行商预算的两向归约",
            "上图为四顶点环，有边成本一，无边成本二，预算四，最短路线四，回答是。"
            "下图为四顶点星形图，没有哈密顿回路，转换后最短路线六，回答否。"
            "位置只是示意，不以图上长度冒充构造距离；生成脚本枚举核对所有三至五顶点简单无向图。",
            elements,
        )

    def complexity_map():
        elements = [
            text(36, 48, "先读假设，再看 P、NP 与 NPC", 32),
            text(36, 88, "下面的分离图假设 P ≠ NP；这不是已证明结论。", 24, ORANGE),
            '<rect x="36" y="130" width="428" height="430" rx="18" fill="#e1f0f5" stroke="#176786" stroke-width="3"/>',
            '<rect x="304" y="180" width="380" height="430" rx="18" fill="#fff1df" fill-opacity="0.62" stroke="#ad4f16" stroke-width="3" stroke-dasharray="9 6"/>',
            text(74, 180, "NP", 33, BLUE),
            text(505, 225, "NP-Hard", 29, ORANGE),
            '<rect x="76" y="248" width="184" height="136" rx="16" fill="#fff" stroke="#176786" stroke-width="2"/>',
            text(168, 300, "P", 32, BLUE, "middle"),
            text(168, 348, "可快速判定", 24, BLUE, "middle"),
            text(384, 325, "NPC", 31, ORANGE, "middle"),
            text(384, 370, "交集", 26, ORANGE, "middle"),
            text(560, 455, "例如停机问题", 23, ORANGE, "middle"),
            text(560, 499, "不属于 NP", 25, ORANGE, "middle"),
            text(74, 442, "留白不全是 NPC", 23, MUTED),
            text(74, 486, "面积不表示数量", 23, MUTED),
            panel(652, 257),
            text(44, 697, "另一种尚未排除的可能：P = NP", 29),
            text(44, 750, "那时 NP 中的所有问题，都可快速判定。", 26, BLUE),
            text(44, 798, "非平凡的 NP 判定问题，也都会是 NPC。", 25),
            text(44, 845, "但 NP-Hard 仍可包含 NP 外的不可判定问题。", 25),
            text(44, 887, "“非平凡”：既有“是”实例，也有“否”实例。", 23, MUTED),
            text(36, 954, "始终成立：P ⊆ NP；NPC = NP ∩ NP-Hard。", 27),
            text(36, 999, "不是所有问题都属于这四类；图只画相关关系。", 24, MUTED),
        ]
        return document(
            1035, "P与NP关系的假设图及另一种可能",
            "上图明确假设P不等于NP：P严格包含于NP，NP完全问题是NP与NP难的交集，"
            "P与此交集分离，NP难还延伸到NP之外。下方说明若P等于NP，"
            "NP中所有问题可快速判定，非平凡问题也为NP完全，但不可判定问题不会因此变可判定。"
            "面积和距离不表达数量与难度。",
            elements,
        )

    def double_tree():
        points = ((0, 0), (3, 0), (3, 4), (0, 4))
        distances = [
            [math.dist(a, b) for b in points]
            for a in points
        ]
        tree = ((0, 1), (0, 3), (2, 3))
        assert sum(distances[a][b] for a, b in tree) == 10
        # Check every three-edge set that connects all four vertices.
        tree_costs = []
        for edges in itertools.combinations(itertools.combinations(range(4), 2), 3):
            reached = {0}
            for _ in range(3):
                reached |= {b for a, b in edges if a in reached} | {a for a, b in edges if b in reached}
            if len(reached) == 4:
                tree_costs.append(sum(distances[a][b] for a, b in edges))
        assert min(tree_costs) == 10
        walk = (0, 1, 0, 3, 2, 3, 0)
        assert sum(distances[a][b] for a, b in zip(walk, walk[1:])) == 20
        route = (0, 1, 3, 2)
        assert cycle_cost(route, distances) == 16
        optimum = min(cycle_cost(tour, distances) for tour in tours(4))
        assert optimum == 14
        assert cycle_cost((0, 1, 2, 3), distances) == optimum
        assert 16 <= 2 * 10 <= 2 * optimum
        elements = [
            text(36, 48, "近似，不是凭感觉说“差不多”", 32),
            text(36, 88, "四点为 3 × 4 矩形；成本取欧氏距离，无单位。", 24, MUTED),
        ]
        headings = [
            ("① 最小生成树：三条边，成本 10", "树边：AB = 3，AD = 4，DC = 3。"),
            ("② 沿树往返：每条边走两次，成本 20", "次序：A → B → A → D → C → D → A"),
            ("③ 跳过重复城市：得到成本 16 的路线", "次序：A → B → D → C → A"),
        ]
        for index, (heading, caption) in enumerate(headings):
            top = 120 + index * 375
            drawn_points = [(270 + x * 40, top + 114 + y * 40) for x, y in points]
            elements += [panel(top, 350), text(44, top + 42, heading, 27)]
            edges = tree if index < 2 else ((0, 1), (1, 3), (3, 2), (2, 0))
            elements += graph_vertices(drawn_points, edges)
            if index == 1:
                elements += [
                    text(490, top + 155, "每边 × 2", 27, ORANGE),
                    text(490, top + 202, "10 × 2 = 20", 24, ORANGE),
                ]
            else:
                elements += [
                    text(490, top + 155, "对角线：5", 26, MUTED),
                    text(490, top + 202, "外圈最优：14", 24, MUTED),
                ]
            elements.append(text(44, top + 324, caption, 25, BLUE))
        elements += [
            text(36, 1293, "一般保证：返回成本 ≤ 2 × 树成本 ≤ 2 × 最优成本。", 24),
            text(36, 1338, "关键前提：距离对称、非负，满足三角不等式。", 24, MUTED),
        ]
        return document(
            1375, "度量旅行商的最小生成树二近似示例",
            "三乘四矩形上四个点，欧氏距离。最小生成树成本十，沿树往返二十，"
            "跳过重复点后的路线A、B、D、C、A成本十六，矩形外圈最优十四。"
            "图形保持坐标比例，交叉点不是城市；脚本核对所有生成树与闭合路线。"
            "一般二近似保证依赖非负对称度量与三角不等式。",
            elements,
        )

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        for name, make in (
            ("certificate", certificate),
            ("enumeration", enumeration),
            ("reduction-flow", reduction_flow),
            ("hamilton-to-tsp", hamilton_to_tsp),
            ("complexity-map", complexity_map),
            ("double-tree", double_tree),
        ):
            content = make()
            ET.fromstring(content)
            (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
            print(f"Wrote {name}.svg")

    main()


@register("recent-topics", "尺度、无理数分界、圆锥丹德林球与高维注意力", "algebra_logic")
def build_recent_topics():
    ROOT = REPO_ROOT

    INK = "#20334d"

    COLORS = ("#1e6e9a", "#8750a7", "#197858")

    STYLE = """
    text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}
    .s1{animation:r1 4.5s steps(1,end) 1 both}
    .s2{animation:r2 4.5s steps(1,end) 1 both}
    .s3{animation:r3 4.5s steps(1,end) 1 both}
    @keyframes r1{0%,9%{opacity:0}10%,100%{opacity:1}}
    @keyframes r2{0%,34%{opacity:0}35%,100%{opacity:1}}
    @keyframes r3{0%,64%{opacity:0}65%,100%{opacity:1}}
    @media(prefers-reduced-motion:reduce){.s1,.s2,.s3,.spinner{animation:none}}
    """

    def label(x, y, value, size=22, anchor="middle", color=INK, bold=False):
        # On 1000px viewBox inside ~760px Chirpy column (0.76x), cap titles at 21.5 (-> 16.3px) and scale labels by 0.78 (-> ~13px)
        if size >= 27:
            ns = min(size * 0.76, 21.5)
            bold = True
        else:
            ns = max(15.0, size * 0.78)
        adj_y = y - 0.28 * (size - ns)
        weight = ' font-weight="700"' if bold else ""
        return f'<text x="{x}" y="{adj_y:.2f}" text-anchor="{anchor}" font-size="{ns:.1f}" fill="{color}"{weight}>{escape(str(value))}</text>'

    def line(x1, y1, x2, y2, color="#a6b1c2", width=2):
        return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"/>'

    def box(x, y, w, h, color="#eef2f8"):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{color}" stroke="#dde6ee" stroke-width="1"/>'

    def write(name, height, title, description, body, extra_style=""):
        content = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>\n'
            f'<style>{extra_style.strip()}{STYLE.strip()}</style>\n'
            f'<rect x="1" y="1" width="998" height="{height - 2}" rx="16" fill="#fbfcfd" stroke="#dde6ee" stroke-width="1.5"/>\n'
            f'{body}\n'
            '</svg>\n'
        )
        ET.fromstring(content)
        target = ROOT / "assets" / "images" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def dna():
        assert 2e-9 * 1e10 == 20
        assert abs(1e-10 * 1e10 - 1) < 1e-12
        assert abs(1e-15 * 1e10 - 1e-5) < 1e-18
        b = label(500, 48, "同一把放大尺：每个长度都乘 100 亿", 28, bold=True)
        b += label(500, 88, "不是物质真的变大，而是用同一比例重新理解尺度", 21)
        cards = [
            ("DNA 宽", "2 纳米", "20 米", "一座楼的宽度"),
            ("典型原子尺度", "0.1 纳米", "1 米", "日常家具尺度"),
            ("选取的核尺度", "1 飞米", "0.01 毫米", "仍是细小尘粒量级"),
        ]
        for i, (name, real, model, note) in enumerate(cards):
            x = 35 + i * 325
            b += f'<g class="s{i+1}">'
            b += box(x, 132, 285, 297, ["#e6eff9", "#f0e7f7", "#e4f2eb"][i])
            b += label(x+142, 175, f"{i+1}  {name}", 23, bold=True)
            b += label(x+142, 226, real, 25)
            b += label(x+142, 272, "× 100 亿 ↓", 22)
            b += label(x+142, 326, model, 32, color=COLORS[i], bold=True)
            b += label(x+142, 386, note, 18)
            b += "</g>"
        b += label(500, 480, "DNA 已像楼那么宽，原子核却依然很小", 26, bold=True)
        b += label(500, 526, "各卡片不是按面积或直径等比例画出的物体；精确的是上面的长度换算。", 19)
        b += label(500, 566, "原子没有硬球边界；核尺度随核种变化；这里没有给夸克指定实测直径。", 19)
        write("dna-scale/uniform-zoom.svg", 605, "DNA、原子与原子核的统一放大换算",
              "三步显示统一放大100亿倍的结果：2纳米变20米，0.1纳米变1米，选取的1飞米变0.01毫米。卡片大小不代表物体比例。", b)

    def irrational():
        assert 141421**2 < 2 * 100000**2
        assert 14142 * 10 < 141421
        b = label(500, 48, "用有理数提问：先分不出，再找到分界", 28, bold=True)
        b += label(500, 86, "x = 1.4142，y = √2；每一行只展示一次比较，不是无限检验", 20)
        rows = [
            ("① 问：比 1.4 大吗？", "x：大于", "y：大于", "这道问题分不出它们。"),
            ("② 问：比 1.415 小吗？", "x：小于", "y：小于", "第二次仍然分不出。"),
            ("③ 问：比 1.41421 小吗？", "x：小于", "y：大于", "终于找到一个区分它们的有理数。"),
        ]
        for i, (question, left, right, note) in enumerate(rows):
            y = 116 + 119*i
            b += f'<g class="s{i+1}">' + box(42, y, 916, 104)
            b += label(66, y+37, question, 23, anchor="start", bold=True)
            b += label(550, y+37, left, 22, color=COLORS[0])
            b += label(790, y+37, right, 22, color=COLORS[1])
            b += label(66, y+78, note, 20, anchor="start")
            b += "</g>"
        x0, x1 = 120, 880
        value = lambda q: x0 + (q-1.4142)/.00002*(x1-x0)
        b += label(500, 523, "放大窗口：[1.41420, 1.41422]，不是从 0 开始的数轴", 20)
        b += line(x0, 568, x1, 568, INK, 3)
        for q, name, y in [(1.4142, "x = 1.4142", 610), (1.41421, "r = 1.41421", 548), (2**.5, "y = √2", 610)]:
            x = value(q)
            b += line(x, 560, x, 577, INK)
            b += label(x, y, name, 21, bold=True)
        b += label(500, 659, "r² = 1.9999899241 ＜ 2，所以 x ＜ r ＜ √2", 24, bold=True)
        b += label(500, 700, "有限次回答相同不能证明相等；所有有理数的比较关系才是定义的关键。", 19)
        write("irrational-comparison/rational-questions.svg", 735, "三个有理数问题区分1.4142与根号二",
              "前两次比较一致，第三个有理数1.41421位于1.4142与根号二之间。底部是明确标出窗口范围的局部线性数轴。有限实验不是相等证明。", b)

    def ui_status():
        b = label(500, 48, "同一个等待界面，两种不同的信息", 28, bold=True)
        b += label(500, 88, "以下是概念示意，不是 Claude Code、Copilot 或 Cursor 的真实截图", 20)
        b += box(40, 120, 430, 350, "#eae8f7") + box(530, 120, 430, 350, "#e5f1ed")
        b += label(255, 164, "陪伴性文案", 25, bold=True)
        b += '<g class="spinner" style="transform-origin:255px 235px"><path d="M255 207 A28 28 0 1 1 227 235" fill="none" stroke="#8750a7" stroke-width="7" stroke-linecap="round"/></g>'
        b += label(255, 303, "Spelunking…", 29, bold=True)
        b += label(255, 355, "像在探险：传达气氛与个性", 21)
        b += label(255, 413, "不能据此推断读了哪些文件", 20)
        b += label(745, 164, "可核查的任务反馈", 25, bold=True)
        for i, value in enumerate(["① 读取：3 个相关文件", "② 修改：1 个目标文件", "③ 检查：结果另行展示"]):
            b += f'<g class="s{i+1}">' + label(565, 235+i*69, value, 23, anchor="start") + "</g>"
        b += label(745, 437, "示意次序不代表真实任务耗时", 18)
        b += label(500, 520, "会动 ≠ 有进展；完成操作 ≠ 已证明结果正确", 27, bold=True)
        b += label(500, 567, "动画只演示两层反馈的区别，不是模拟真实后台状态或百分比。", 20)
        write("ai-status/feedback-layers.svg", 605, "等待文案和操作反馈的差别",
              "左侧转圈配Spelunking文案，不提供可核查进度；右侧逐步列出示意操作，最后提醒仍需检查结果。不是任何产品的真实截图。",
              b, ".spinner{animation:spin 4s linear 1}@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(720deg)}}")

    def conics():
        source = ROOT / "assets/images/conic-sections/03-dandelin-ellipse.svg"
        r = ET.parse(source).getroot()
        ns = "{http://www.w3.org/2000/svg}"
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        r.find(ns+"title").text = "丹德林球：两次切线等长，再拼成定长"
        r.find(ns+"desc").text = "沿用原轴截面图；先显出蓝色同球切线，再显出红色同球切线，最后合并为PF1加PF2等于AB。不是球或截平面移动的动画。"
        r.find(ns+"style").text += STYLE
        for e in r:
            stroke = e.get("stroke")
            if stroke == "#2563eb":
                e.set("class", "s1")
            elif stroke == "#be185d":
                e.set("class", "s2")
            if e.tag == ns+"text":
                y = float(e.get("y"))
                if y == 177:
                    e.text = "① 蓝色同球切线：PF₁ = PA"
                    e.set("class", "small s1")
                elif y == 211:
                    e.text = "② 红色同球切线：PF₂ = PB"
                    e.set("class", "small s2")
                elif y == 410:
                    e.text = "③ 相加：PF₁ + PF₂ = AB"
                    e.set("class", "small s3")
        points = {"P": (394.27,379.87), "A": (327,496.38), "B": (415.72,342.71),
                  "F1": (273.93,440.04), "F2": (355.89,399.05)}
        distance = lambda a, b: hypot(points[a][0]-points[b][0], points[a][1]-points[b][1])
        assert abs(distance("P","F1")-distance("P","A")) < .03
        assert abs(distance("P","F2")-distance("P","B")) < .03
        assert abs(distance("P","A")+distance("P","B")-distance("A","B")) < .03
        target = ROOT / "assets/images/conic-sections/08-dandelin-steps.svg"
        ET.ElementTree(r).write(target, encoding="utf-8", xml_declaration=False)

    def shell():
        b = label(500, 48, "半径只取外面 1%，体积能占多少？", 28, bold=True)
        b += label(500, 88, "同样的壳厚 ε = 0.01；条长表示体积比例，不是球的形状", 20)
        b += label(120, 137, "维度 n", 20) + label(565, 137, "外壳占比：1 − 0.99ⁿ", 21)
        for i, n in enumerate([2, 3, 10, 100, 1000]):
            fraction = 1-.99**n
            assert 0 < fraction < 1
            y = 170+i*69
            b += label(120, y+25, n, 24, bold=True) + box(215, y, 610, 34, "#e7e8ef")
            b += f'<rect x="215" y="{y}" width="{610*fraction}" height="34" rx="4" fill="#277c67" data-n="{n}" data-fraction="{fraction}"/>'
            b += label(850, y+25, f"{fraction*100:.4f}%", 19, anchor="start")
        b += label(500, 563, "先固定壳厚，再提高维度：不是把二维圆环画得越来越厚", 23, bold=True)
        b += label(500, 607, "前提：在整个单位球体内均匀采样。中心仍在球内，球面本身的体积仍为 0。", 19)
        write("embedding-geometry/thin-shell.svg", 650, "固定1%半径厚度下的高维球壳体积比例",
              "2、3、10、100、1000维的外壳占比依次为1.99%、2.9701%、9.5618%、63.3968%、99.9957%。横条是数值图表，不是高维球的投影。", b)

    def attention():
        scores = [3., 0., 1.]
        weights = [exp(s)/sum(exp(v) for v in scores) for s in scores]
        assert abs(sum(weights)-1) < 1e-12
        values = [(1.,0.), (0.,1.), (.5,.5)]
        output = [sum(w*v[j] for w,v in zip(weights,values)) for j in range(2)]
        b = label(500, 48, "把注意力算一遍：分数 → 权重 → 加权取值", 27, bold=True)
        b += label(500, 87, "单头、单位置的玩具例子：三处可见信息；不是某个真实模型的测量", 19)
        headings = ["① 已缩放的匹配分数", "② softmax 后的权重", "③ 乘上对应的 V"]
        for i, heading in enumerate(headings):
            x = 30+i*328
            b += f'<g class="s{i+1}">' + box(x, 122, 303, 300, ["#e6eff9","#f0e7f7","#e4f2eb"][i])
            b += label(x+151, 165, heading, 21, bold=True)
            for j in range(3):
                name = "ABC"[j]
                value = [f"{name}：{scores[j]:g}", f"{name}：{weights[j]:.3f}", f"{weights[j]:.3f} × {values[j]}"][i]
                b += label(x+151, 232+j*70, value, 22)
            b += "</g>"
        b += label(500, 475, f"先用未四舍五入的权重计算：o ≈ ({output[0]:.4f}, {output[1]:.4f})", 25, bold=True)
        b += label(500, 524, "Q、K 参与算匹配分数；真正混合的内容来自 V，而不是把分数本身当内容。", 19)
        b += label(500, 565, "权重总和为 1，但不是“属于某个语义类别的概率”；输出还不是整个 Transformer 层。", 18)
        write("embedding-geometry/attention-steps.svg", 605, "单头注意力的具体数值分步图",
              "分数3、0、1经softmax后约0.844、0.042、0.114；值向量分别为(1,0)、(0,1)、(0.5,0.5)，加权输出约(0.9009,0.0991)。分三步出现，最终保留完整图。", b)

    for generate in [dna, irrational, ui_status, conics, shell, attention]:
        generate()
    print("Generated 6 SVGs; scale conversions, rational bounds, tangent lengths, shell fractions and attention weights verified.")
