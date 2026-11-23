"""CAD / CAE / CAM & digital-twin visual builders (三维物理建模 article).

Figures:
1. modeling-pipeline.svg        点→线框→曲面→实体 + CSG/B-rep 对照
2. mesh-vs-nurbs-circle.svg     正 n 边形逼近圆的误差账（边中点偏差 1-cos(pi/n)）
3. fem-spring-example.svg       两段弹簧串联有限元手算（静态完整结果）
4. fem-spring-loading-anim.svg  同一算例的加载过程短动画（播放一次停在终态）
5. virtual-real-loop.svg        造型→仿真→制造→实测→数字孪生闭环

All numbers are computed or exactly constructed; assertions run at build time.
"""

import math
from fractions import Fraction

from .core import (
    BG,
    BLUE,
    BLUE_SOFT,
    BODY,
    BORDER,
    CARD_BG,
    GREEN,
    GREEN_SOFT,
    HAIRLINE,
    INK,
    MUTED,
    ORANGE,
    ORANGE_SOFT,
    PURPLE,
    PURPLE_SOFT,
    SLATE,
    SLATE_SOFT,
    card,
    figure,
    header,
    register,
    txt,
    write_svg,
)

SUBDIR = "cad-physics-modeling"

# ---------------------------------------------------------------------------
# Shared exact numerics (asserted once, reused by every figure)
# ---------------------------------------------------------------------------
K1, K2, FORCE = 100.0, 200.0, 1000.0  # N/mm, N/mm, N


def spring_solution():
    """Solve the reduced 2x2 stiffness system exactly with fractions."""
    # [ k1+k2  -k2 ] [u2]   [0]
    # [ -k2    k2  ] [u3] = [F]
    a, b, c, d = Fraction(300), Fraction(-200), Fraction(-200), Fraction(200)
    det = a * d - b * c
    u2 = (Fraction(0) * d - b * Fraction(1000)) / det
    u3 = (a * Fraction(1000) - Fraction(0) * c) / det
    assert u2 == 10 and u3 == 15
    assert K1 * float(u2) == FORCE  # 第一段内力
    assert K2 * float(u3 - u2) == FORCE  # 第二段内力
    k_eq = K1 * K2 / (K1 + K2)  # 串联等效刚度 200/3 N/mm
    assert abs(FORCE / k_eq - float(u3)) < 1e-9
    return float(u2), float(u3)


def polygon_deviation(n):
    """Relative sagitta of a regular n-gon inscribed in the unit circle."""
    return 1.0 - math.cos(math.pi / n)


def verify_numbers():
    u2, u3 = spring_solution()
    assert abs(u2 - 10.0) < 1e-12 and abs(u3 - 15.0) < 1e-12
    # 文中表格的舍入必须与三角函数直接计算一致
    assert f"{polygon_deviation(8) * 100:.1f}" == "7.6"
    assert f"{polygon_deviation(32) * 100:.2f}" == "0.48"
    assert f"{polygon_deviation(1024) * 100:.4f}" == "0.0005"
    # 砖形零件质量：1×2×3 cm³ 钢，密度 7.85 g/cm³
    assert abs(1 * 2 * 3 * 7.85 - 47.1) < 1e-9
    # 偏差随边数单调下降
    assert polygon_deviation(8) > polygon_deviation(32) > polygon_deviation(1024) > 0


def spring_path(x0, x1, y, amp=12.0, coils=5, lead=12.0):
    """Zigzag spring polyline from x0 to x1 at height y."""
    pts = [(x0, y), (x0 + lead, y)]
    span = (x1 - lead) - (x0 + lead)
    steps = coils * 2
    for i in range(1, steps):
        x = x0 + lead + span * i / steps
        pts.append((x, y - amp if i % 2 == 1 else y + amp))
    pts.append((x1 - lead, y))
    pts.append((x1, y))
    return " ".join(f"{x:.2f},{yy:.2f}" for x, yy in pts)


def wall(x, y_top, y_bot):
    els = [f'<line x1="{x}" y1="{y_top}" x2="{x}" y2="{y_bot}" stroke="{SLATE}" stroke-width="3"/>']
    y = y_top + 8
    while y <= y_bot:
        els.append(f'<line x1="{x - 10}" y1="{y}" x2="{x}" y2="{y - 8}" stroke="{HAIRLINE}" stroke-width="1.2"/>')
        y += 16
    return els


# ---------------------------------------------------------------------------
# Figure 1: point -> wireframe -> surface -> solid, CSG vs B-rep
# ---------------------------------------------------------------------------
def build_modeling_pipeline():
    els = header("图 1 · 形状怎样进入电脑：从坐标点到可计算的实体")

    cards = [
        (16, "① 点：三个数定位", BLUE),
        (206, "② 线框：连成骨架", ORANGE),
        (396, "③ 曲面：蒙上一层皮", GREEN),
        (586, "④ 实体：填满内部", PURPLE),
    ]
    for x0, title, col in cards:
        els.append(card(x0, 44, 158, 176))
        els.append(txt(x0 + 79, 68, title, 13.5, col, "middle", weight="700"))

    # ① points
    for cy, lab in ((110, "(0, 0, 0)"), (135, "(1, 0, 0)"), (160, "(1, 1, 0)")):
        els.append(f'<circle cx="62" cy="{cy}" r="3.5" fill="{BLUE}"/>')
        els.append(txt(72, cy + 4, lab, 11.5, BODY))
    els.append(txt(95, 196, "一堆带坐标的点", 11.5, MUTED, "middle"))

    # ② wireframe cube (front square + offset back square)
    els.append(
        f'<g stroke="{ORANGE}" stroke-width="1.6" fill="none">'
        '<path d="M261 104 L301 104 L301 144 L261 144 Z"/>'
        '<path d="M275 90 L315 90 L315 130 L275 130 Z"/>'
        '<path d="M261 104 L275 90 M301 104 L315 90 M301 144 L315 130 M261 144 L275 130"/>'
        "</g>"
    )
    els.append(txt(285, 196, "只有线，不知里外", 11.5, MUTED, "middle"))

    # ③ surface cube (faces filled, still hollow)
    els.append(
        f'<g stroke="{GREEN}" stroke-width="1.4" stroke-linejoin="round">'
        '<path d="M451 104 L491 104 L491 144 L451 144 Z" fill="#e7f6ee"/>'
        '<path d="M465 90 L505 90 L505 130 L465 130 Z" fill="#eaf4fb"/>'
        '<path d="M451 104 L465 90 M491 104 L505 90 M491 144 L505 130 M451 144 L465 130" fill="none"/>'
        '<path d="M491 104 L505 90 L505 130 L491 144 Z" fill="#fef1e8"/>'
        "</g>"
    )
    els.append(txt(475, 196, "看着光滑，仍然空心", 11.5, MUTED, "middle"))

    # ④ solid cube + mass example
    els.append(
        f'<path d="M641 104 L681 104 L681 144 L641 144 Z" fill="{PURPLE}" fill-opacity="0.55" stroke="{PURPLE}" stroke-width="1.4"/>'
        f'<path d="M655 90 L695 90 L695 130 L655 130 Z" fill="{PURPLE}" fill-opacity="0.18" stroke="{PURPLE}" stroke-width="1.4"/>'
        f'<path d="M641 104 L655 90 M681 104 L695 90 M681 144 L695 130 M641 144 L655 130" stroke="{PURPLE}" stroke-width="1.4" fill="none"/>'
    )
    els.append(txt(665, 176, "V = a × b × h", 11.5, PURPLE, "middle", weight="600"))
    els.append(txt(665, 192, "例：6 cm³ 钢块 ≈ 47.1 g", 11.5, PURPLE, "middle"))
    els.append(txt(665, 208, "有体积，能算重量", 11.5, MUTED, "middle"))

    # arrows between cards
    for x0 in (178, 368, 558):
        els.append(
            f'<path d="M{x0} 132 L{x0 + 22} 132" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr-muted)"/>'
        )

    # CSG vs B-rep band
    els.append(card(16, 238, 354, 84, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(30, 259, "CSG｜像玩橡皮泥：拼上去、挖掉", 13.5, INK, weight="700"))
    els.append(f'<rect x="32" y="270" width="30" height="30" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.3"/>')
    els.append(
        f'<circle cx="47" cy="285" r="9" fill="{BG}" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="3 2"/>'
    )
    els.append(txt(72, 282, "长方体 − 圆柱", 12, BODY))
    els.append(txt(72, 299, "= 带孔实体（布尔差集）", 12, BODY))

    els.append(card(390, 238, 354, 84, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(404, 259, "B-rep｜像包礼物：精确记录每张面", 13.5, INK, weight="700"))
    els.append(txt(404, 280, "面 6 张 ｜ 边 12 条 ｜ 顶点 8 个", 12, BODY))
    els.append(txt(404, 299, "还要记清它们怎样拼接成封闭边界", 12, BODY))

    return figure(
        336,
        "从坐标点到可计算实体：CAD 几何建模四步与两种实体表示",
        "四张卡片依次展示点、线框、曲面、实体：只有填满内部的实体才能算出体积与质量（例：6立方厘米钢块约47.1克）；"
        "底部对比CSG布尔运算与B-rep边界表示两种实体构造方法。立方体为教学示意，比例不代表真实工程尺度。",
        els,
    )


# ---------------------------------------------------------------------------
# Figure 2: inscribed polygon vs circle, deviation table
# ---------------------------------------------------------------------------
def build_mesh_vs_nurbs_circle():
    els = header(
        "图 2 · 网格逼近圆的误差账：边中点处差 1 − cos(π/n)",
        "顶点落在圆上，边中点陷进圆内；边数越多偏差越小，但永远不为零",
    )

    # Left: circle + inscribed octagon, highlighted bottom-edge gap
    els.append(card(20, 64, 368, 256))
    cx, cy, R = 204.0, 190.0, 94.0
    els.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{BLUE}" stroke-width="1.8"/>')
    verts = []
    for k in range(8):
        ang = math.radians(22.5 + 45.0 * k)
        verts.append((cx + R * math.cos(ang), cy - R * math.sin(ang)))
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in verts)
    els.append(f'<polygon points="{pts}" fill="{ORANGE_SOFT}" fill-opacity="0.55" stroke="{ORANGE}" stroke-width="1.8"/>')
    for x, y in verts:
        els.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.6" fill="{ORANGE}"/>')

    # bottom edge midpoint (angle 270°) and the arc point below it
    mid_r = R * math.cos(math.pi / 8)
    mx, my = cx, cy + mid_r
    ax, ay = cx, cy + R
    gap = R - mid_r
    assert abs(gap / R - polygon_deviation(8)) < 1e-12
    els.append(f'<line x1="{cx}" y1="{cy}" x2="{ax}" y2="{ay}" stroke="{HAIRLINE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    els.append(f'<line x1="{mx:.2f}" y1="{my:.2f}" x2="{ax}" y2="{ay}" stroke="#b34039" stroke-width="3"/>')
    els.append(f'<circle cx="{mx:.2f}" cy="{my:.2f}" r="3" fill="#b34039"/>')
    mid_gap_y = 0.5 * (my + ay)
    els.append(
        f'<polyline points="{mx + 4:.1f},{mid_gap_y:.1f} {mx + 18:.1f},{my - 24:.1f} {mx + 26:.1f},{my - 24:.1f}" '
        f'fill="none" stroke="#b34039" stroke-width="1.2"/>'
    )
    els.append(txt(mx + 30, my - 20, f"差 {polygon_deviation(8) * 100:.1f}% R", 12, "#b34039", weight="700", halo=True))
    els.append(txt(cx, cy - R - 10, "蓝 = 真圆（NURBS 可精确表示）", 11.5, BLUE, "middle"))
    els.append(txt(cx, cy + R + 22, "橙 = 正八边形网格（顶点在圆上）", 11.5, ORANGE, "middle"))

    # Right: deviation table with computed mini polygons
    els.append(card(404, 64, 336, 256))
    els.append(txt(420, 90, "相对偏差 = 1 − cos(π/n)", 13.5, INK, weight="700"))
    rows = [(8, "7.6%", "一眼就是八边形"), (32, "0.48%", "远看像圆"), (1024, "0.0005%", "几乎与真圆重合")]
    for i, (n, pct, feel) in enumerate(rows):
        ry = 128 + i * 56
        # mini circle + polygon, geometry computed from n
        mcx, mcy, mr = 438.0, ry - 4.0, 16.0
        els.append(f'<circle cx="{mcx}" cy="{mcy}" r="{mr}" fill="none" stroke="{BLUE}" stroke-width="1.2"/>')
        mpts = []
        for k in range(n):
            ang = math.pi / n + 2 * math.pi * k / n
            mpts.append(f"{mcx + mr * math.cos(ang):.2f},{mcy - mr * math.sin(ang):.2f}")
        els.append(f'<polygon points="{" ".join(mpts)}" fill="none" stroke="{ORANGE}" stroke-width="1.2"/>')
        els.append(txt(466, ry, f"n = {n}", 12.5, INK, weight="700"))
        els.append(txt(548, ry, pct, 12.5, "#b34039", weight="700"))
        els.append(txt(622, ry, feel, 11.5, MUTED))
    els.append(txt(420, 288, "NURBS 是有理 B 样条：圆与圆锥曲线", 11.5, BODY))
    els.append(txt(420, 306, "可精确表示，误差为 0（《The NURBS Book》第 7 章）", 11.5, BODY))

    # Bottom note band
    els.append(card(20, 334, 720, 46, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(34, 353, "偏差在顶点处为 0、边中点处最大；小角度下 1 − cos θ ≈ θ²/2，", 12, BODY))
    els.append(txt(34, 371, "所以边数翻倍，偏差约缩小到原来的 1/4。表中数字由三角函数直接算出，不靠肉眼判断。", 12, BODY))

    return figure(
        394,
        "网格逼近圆的误差账：正n边形边中点偏差与NURBS精确表示对比",
        "左侧真圆内接正八边形，底边中点陷进圆内，偏差为半径的7.6%（1-cos(pi/8)精确计算）；"
        "右侧表格给出n=8、32、1024的相对偏差7.6%、0.48%、0.0005%，并说明NURBS作为有理B样条可精确表示圆。",
        els,
    )


# ---------------------------------------------------------------------------
# Figure 3: static two-spring FEM worked example
# ---------------------------------------------------------------------------
def build_fem_spring_example():
    u2, u3 = spring_solution()
    els = header("图 3 · 化整为零：把一根杆切成两段，方程立刻能手算")

    els.extend(wall(92, 86, 138))
    els.append(txt(92, 176, "固定端", 11.5, MUTED, "middle"))

    els.append(
        f'<polyline points="{spring_path(92, 226, 120)}" fill="none" stroke="{BLUE}" stroke-width="2"/>'
    )
    els.append(f'<circle cx="92" cy="120" r="4" fill="{BLUE}"/>')
    els.append(f'<circle cx="226" cy="120" r="4" fill="{BLUE}"/>')
    els.append(txt(163, 94, "k₁ = 100 N/mm", 12, BLUE, "middle", weight="600"))

    els.append(
        f'<polyline points="{spring_path(226, 356, 120)}" fill="none" stroke="{ORANGE}" stroke-width="2"/>'
    )
    els.append(f'<circle cx="356" cy="120" r="4" fill="{ORANGE}"/>')
    els.append(txt(295, 94, "k₂ = 200 N/mm", 12, ORANGE, "middle", weight="600"))

    els.append(f'<path d="M364 120 L444 120" stroke="{GREEN}" stroke-width="2.5" marker-end="url(#arr-green)"/>')
    els.append(txt(404, 108, "F = 1000 N", 12, GREEN, "middle", weight="600"))

    els.append(txt(92, 156, "u₁ = 0", 12, INK, "middle"))
    els.append(txt(226, 156, f"u₂ = {u2:.0f} mm", 12, INK, "middle"))
    els.append(txt(356, 156, f"u₃ = {u3:.0f} mm", 12, INK, "middle"))

    els.append(card(472, 62, 272, 130))
    els.append(txt(486, 84, "怎么算出来的？", 13.5, INK, weight="700"))
    els.append(txt(486, 106, "① 每段弹簧：k = EA / L，先算刚度", 11.5, BODY))
    els.append(txt(486, 126, "② 在节点写平衡式，拼成整体矩阵", 11.5, BODY))
    els.append(txt(486, 146, "③ 解线性方程，得到所有节点位移", 11.5, BODY))
    els.append(txt(486, 170, "位移 × 刚度 = 内力，再校核平衡", 11.5, MUTED))

    els.append(card(16, 204, 728, 130, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(30, 226, "整体方程（固定端 u₁ = 0，只剩两个未知数）：", 13.5, INK, weight="700"))
    els.append(txt(30, 250, "[ 300   −200 ] · [ u₂ ]    [    0 ]", 12.5, BODY, cls="mono"))
    els.append(txt(30, 270, "[ −200   200 ]   [ u₃ ]  = [ 1000 ]", 12.5, BODY, cls="mono"))
    els.append(txt(30, 296, f"解得：u₂ = {u2:.0f} mm，u₃ = {u3:.0f} mm", 12.5, GREEN, weight="700"))
    els.append(
        txt(
            30,
            318,
            f"校核：100×10 = 1000 N；200×(15−10) = 1000 N，两段内力都与外力相等 ✓",
            11.5,
            MUTED,
        )
    )

    return figure(
        350,
        "两段弹簧串联的有限元算例：位移、内力与平衡校核",
        "左端固定，两段刚度分别为100与200牛每毫米的弹簧串联，右端受1000牛拉力；"
        "由整体刚度方程解出中间节点位移10毫米、右端位移15毫米，两段内力都等于1000牛。教学玩具模型，非真实结构测量。",
        els,
    )


# ---------------------------------------------------------------------------
# Figure 4: loading-process animation (plays once, rests at final state)
# ---------------------------------------------------------------------------
PX_PER_MM = 6.0
REST_X1, REST_X2, REST_X3 = 80.0, 260.0, 440.0
SPRING_REST_LEN = 180.0


def build_fem_spring_loading_anim():
    u2, u3 = spring_solution()
    fin_x2 = REST_X2 + PX_PER_MM * u2  # 320
    fin_x3 = REST_X3 + PX_PER_MM * u3  # 530
    fin_len1 = fin_x2 - REST_X1  # 240
    fin_len2 = fin_x3 - fin_x2  # 210
    elong1 = u2  # 10 mm
    elong2 = u3 - u2  # 5 mm
    # 几何与物理一致性断言
    assert abs(fin_x2 - 320.0) < 1e-9 and abs(fin_x3 - 530.0) < 1e-9
    assert abs(fin_len1 - (SPRING_REST_LEN + PX_PER_MM * elong1)) < 1e-9
    assert abs(fin_len2 - (SPRING_REST_LEN + PX_PER_MM * elong2)) < 1e-9
    s1_from = SPRING_REST_LEN / fin_len1  # 0.75
    s2_from = SPRING_REST_LEN / fin_len2  # 6/7
    delay, dur, read_delay, read_dur = 0.8, 2.2, 3.2, 0.5
    assert delay + dur <= read_delay  # 读数在运动结束后出现
    total_time = read_delay + read_dur
    assert abs(total_time - 3.7) < 1e-9

    extra_css = f"""
  @keyframes femS1 {{ from {{ transform: scaleX({s1_from:.10f}); }} to {{ transform: scaleX(1); }} }}
  @keyframes femS2 {{ from {{ transform: scaleX({s2_from:.10f}); }} to {{ transform: scaleX(1); }} }}
  @keyframes femN2 {{ from {{ transform: translateX(-{PX_PER_MM * u2:.1f}px); }} to {{ transform: translateX(0); }} }}
  @keyframes femN3 {{ from {{ transform: translateX(-{PX_PER_MM * (u3 - u2):.1f}px); }} to {{ transform: translateX(0); }} }}
  @keyframes femFade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  .a-s1 {{ transform-box: fill-box; transform-origin: left center;
           animation: femS1 {dur}s cubic-bezier(0.4,0,0.2,1) {delay}s 1 backwards; }}
  .a-s2 {{ transform-box: fill-box; transform-origin: left center;
           animation: femS2 {dur}s cubic-bezier(0.4,0,0.2,1) {delay}s 1 backwards; }}
  .a-n2 {{ animation: femN2 {dur}s cubic-bezier(0.4,0,0.2,1) {delay}s 1 backwards; }}
  .a-n3 {{ animation: femN3 {dur}s cubic-bezier(0.4,0,0.2,1) {delay}s 1 backwards; }}
  .a-force {{ animation: femFade 0.6s ease-out 0.2s 1 backwards; }}
  .a-read {{ animation: femFade {read_dur}s ease-out {read_delay}s 1 backwards; }}
  @media (prefers-reduced-motion: reduce) {{
    .a-s1, .a-s2, .a-n2, .a-n3, .a-force, .a-read {{ animation: none !important; }}
  }}
"""

    els = header(
        "图 4 · 加载全过程：串联两段传同一个力，软的伸得多、硬的伸得少",
        f"动画约 {total_time:.1f} 秒，播放一次即停在终态；虚线为加载前位置。位移按 1 mm = {PX_PER_MM:.0f} px 教学放大绘制",
    )

    y = 130.0
    els.extend(wall(int(REST_X1), 96, 148))
    els.append(f'<circle cx="{REST_X1:.0f}" cy="{y}" r="4.5" fill="{SLATE}"/>')
    els.append(txt(REST_X1, 166, "u₁ = 0", 12, INK, "middle"))

    # ghost rest configuration (always visible, static)
    els.append(
        f'<g fill="none" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="4 3" opacity="0.75">'
        f'<polyline points="{spring_path(REST_X1, REST_X2, y)}"/>'
        f'<polyline points="{spring_path(REST_X2, REST_X3, y)}"/>'
        "</g>"
    )
    for gx in (REST_X2, REST_X3):
        els.append(f'<circle cx="{gx:.0f}" cy="{y}" r="4" fill="{BG}" stroke="{MUTED}" stroke-width="1.4"/>')
    els.append(txt(REST_X3 + 8, y + 26, "虚线 = 加载前", 11.5, MUTED))

    # final configuration in markup; keyframes start from the rest state
    els.append(
        f'<g class="a-s1"><polyline points="{spring_path(REST_X1, fin_x2, y)}" fill="none" '
        f'stroke="{BLUE}" stroke-width="2" vector-effect="non-scaling-stroke"/></g>'
    )
    els.append(f'<g class="a-n2">')
    els.append(f'<circle cx="{fin_x2:.0f}" cy="{y}" r="4.5" fill="{BLUE}"/>')
    els.append(
        f'<g class="a-s2"><polyline points="{spring_path(fin_x2, fin_x3, y)}" fill="none" '
        f'stroke="{ORANGE}" stroke-width="2" vector-effect="non-scaling-stroke"/></g>'
    )
    els.append(f'<g class="a-n3">')
    els.append(f'<circle cx="{fin_x3:.0f}" cy="{y}" r="4.5" fill="{ORANGE}"/>')
    els.append(
        f'<g class="a-force"><path d="M{fin_x3 + 8:.0f} {y} L{fin_x3 + 88:.0f} {y}" stroke="{GREEN}" '
        f'stroke-width="2.5" marker-end="url(#arr-green)"/>'
        + txt(fin_x3 + 48, y - 12, "F = 1000 N", 12, GREEN, "middle", weight="600")
        + "</g>"
    )
    els.append("</g>")  # a-n3
    els.append("</g>")  # a-n2

    # displacement brackets (appear with the readout)
    els.append('<g class="a-read">')
    for xa, xb, lab, col in (
        (REST_X2, fin_x2, f"u₂ = {u2:.0f} mm", BLUE),
        (REST_X3, fin_x3, f"u₃ = {u3:.0f} mm", ORANGE),
    ):
        els.append(
            f'<path d="M{xa:.0f} 190 L{xa:.0f} 198 L{xb:.0f} 198 L{xb:.0f} 190" fill="none" stroke="{col}" stroke-width="1.4"/>'
        )
        els.append(txt((xa + xb) / 2, 214, lab, 12, col, "middle", weight="700"))
    els.append("</g>")

    # readout band
    els.append('<g class="a-read">')
    els.append(card(16, 232, 728, 96, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(
        txt(30, 254, f"第一段（软 k₁ = 100 N/mm）：伸长 {elong1:.0f} mm → 内力 100×10 = 1000 N", 12, BLUE, weight="600")
    )
    els.append(
        txt(30, 276, f"第二段（硬 k₂ = 200 N/mm）：伸长 {elong2:.0f} mm → 内力 200×5 = 1000 N", 12, ORANGE, weight="600")
    )
    els.append(
        txt(30, 298, "串联传力处处相等；谁软谁伸得多。节点位移与图 3 的手算结果完全一致 ✓", 12, GREEN, weight="700")
    )
    els.append("</g>")

    return figure(
        342,
        "两段弹簧有限元加载过程动画：位移增长与内力校核",
        "左端固定的两段串联弹簧在1000牛拉力下从虚线所示的加载前位置伸长：软段（100牛每毫米）伸长10毫米，"
        "硬段（200牛每毫米）伸长5毫米，节点2位移10毫米、节点3位移15毫米；两段内力都等于1000牛。"
        "动画播放一次停在终态；开启减少动态效果时直接呈现完整终态。位移按1毫米=6像素教学放大。",
        els,
        extra_css=extra_css,
    )


# ---------------------------------------------------------------------------
# Figure 5: virtual -> real -> virtual engineering loop
# ---------------------------------------------------------------------------
def build_virtual_real_loop():
    els = header("图 5 · 从屏幕到现实，再回到屏幕：一个不断被修正的闭环")

    stages = [
        (16, 132, "① CAD 造型", "点线面 → 实体", "回答「长什么样」", BLUE, BLUE_SOFT),
        (164, 132, "② CAE 仿真", "受力·流动·传热", "回答「会怎样」", ORANGE, ORANGE_SOFT),
        (312, 132, "③ 制造 / 施工", "CNC·3D打印·BIM", "把数字变成实物", GREEN, GREEN_SOFT),
        (460, 132, "④ 真实物体", "桥·机器·零件", "接受现实检验", PURPLE, PURPLE_SOFT),
        (608, 136, "⑤ 数字孪生", "传感器实时回流", "回答「此刻如何」", SLATE, SLATE_SOFT),
    ]
    for x0, w, title, sub, note, col, bg in stages:
        els.append(card(x0, 52, w, 92, fill=bg, stroke=col))
        els.append(txt(x0 + w / 2, 76, title, 12.5, col, "middle", weight="700"))
        els.append(txt(x0 + w / 2, 98, sub, 11.5, BODY, "middle"))
        els.append(txt(x0 + w / 2, 118, note, 11.5, MUTED, "middle"))

    for x0 in (150, 298, 446, 594):
        els.append(f'<path d="M{x0} 98 L{x0 + 12} 98" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')

    extra_defs = f"""
  <marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{PURPLE}"/>
  </marker>"""
    els.append(
        f'<path d="M676 146 L676 190 Q676 202 664 202 L244 202 Q230 202 230 188 L230 148" fill="none" '
        f'stroke="{PURPLE}" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#arr-purple)"/>'
    )
    els.append(f'<rect x="348" y="188" width="208" height="28" rx="14" fill="{BG}"/>')
    els.append(txt(452, 207, "← 实测数据回流修正模型", 11.5, PURPLE, "middle", weight="700"))

    els.append(txt(16, 246, "静态 3D 模型只描述外观；仿真预测「如果这样会怎样」；数字孪生再接上实时数据，", 11.5, BODY))
    els.append(txt(16, 266, "让虚拟副本跟着真实物体一起呼吸——三者不是一回事（定义依据见文末 IBM 资料）。", 11.5, BODY))
    els.append(txt(16, 288, "注：图中为教学示意，流程顺序在真实工程中常反复迭代，并非严格一次走完。", 11.5, MUTED))

    return figure(
        300,
        "从虚拟到现实再回到虚拟：三维物理建模的工程闭环",
        "五个步骤依次是CAD造型、CAE仿真、制造或施工、真实物体、数字孪生；最后一步通过传感器实时数据把真实状态送回模型，形成闭环。"
        "静态3D模型、仿真与数字孪生三者定义不同；流程为教学示意，真实工程常反复迭代。",
        els,
        extra_defs=extra_defs,
    )


@register(
    "cad-physics-modeling",
    "三维物理建模：点线面体与CSG/B-rep、网格逼近圆误差账、两段弹簧有限元手算与加载动画、数字孪生工程闭环",
    "science_tech",
)
def build_cad_physics_modeling():
    verify_numbers()
    write_svg(SUBDIR, "modeling-pipeline", build_modeling_pipeline())
    write_svg(SUBDIR, "mesh-vs-nurbs-circle", build_mesh_vs_nurbs_circle())
    write_svg(SUBDIR, "fem-spring-example", build_fem_spring_example())
    write_svg(SUBDIR, "fem-spring-loading-anim", build_fem_spring_loading_anim())
    write_svg(SUBDIR, "virtual-real-loop", build_virtual_real_loop())
