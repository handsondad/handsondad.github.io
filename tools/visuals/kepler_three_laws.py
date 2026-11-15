"""Original Chinese SVG diagrams for Kepler's Three Laws of Planetary Motion
(assets/images/kepler-three-laws/).
"""

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
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "kepler-three-laws"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
GOLD = "#b45309"
GOLD_SOFT = "#fffbeb"


def _solve_kepler(mean_anom, ecc):
    """Solve M = E - e*sin(E) for eccentric anomaly E via Newton-Raphson."""
    e_val = mean_anom
    for _ in range(30):
        diff = (e_val - ecc * math.sin(e_val) - mean_anom) / (1.0 - ecc * math.cos(e_val))
        e_val -= diff
        if abs(diff) < 1e-13:
            break
    assert abs(e_val - ecc * math.sin(e_val) - mean_anom) < 1e-11
    return e_val


def _sector_area_from_E(e1, e2, a, ecc):
    """Exact focal sector area swept between eccentric anomalies E1 and E2.
    Cross-checked against independent polar Simpson integration of 0.5 * r(theta)^2 dtheta!
    """
    b = a * math.sqrt(1.0 - ecc * ecc)
    analytic = 0.5 * a * b * ((e2 - ecc * math.sin(e2)) - (e1 - ecc * math.sin(e1)))

    def e_to_theta(ev):
        return 2.0 * math.atan2(math.sqrt(1.0 + ecc) * math.sin(ev / 2.0), math.sqrt(1.0 - ecc) * math.cos(ev / 2.0))

    th1 = e_to_theta(e1)
    th2 = e_to_theta(e2)
    if th2 < th1:
        th2 += 2.0 * math.pi
    p = a * (1.0 - ecc * ecc)
    n = 1000  # even number for Simpson's rule
    h = (th2 - th1) / n

    def integrand(th):
        r = p / (1.0 + ecc * math.cos(th))
        return 0.5 * r * r

    simpson = integrand(th1) + integrand(th2)
    for i in range(1, n):
        w = 4.0 if i % 2 == 1 else 2.0
        simpson += w * integrand(th1 + i * h)
    simpson *= h / 3.0
    assert abs(analytic - simpson) < 1e-11, f"analytic={analytic}, simpson={simpson}"
    return analytic


def _verify_physics():
    # 1. Mars ellipse flattenings vs focus offset (e = 0.0934)
    e_mars = 0.0934
    b_over_a = math.sqrt(1.0 - e_mars * e_mars)
    flattening = 1.0 - b_over_a
    assert 0.0043 < flattening < 0.0045  # 0.437% width shrinkage vs 9.34% focus shift!

    # 2. Equal-area verification on e = 0.55 teaching orbit (a = 1.0)
    ecc = 0.55
    a = 1.0
    b = math.sqrt(1.0 - ecc * ecc)
    total_area = math.pi * a * b
    # Sector 1 around perihelion: M in [-pi/6, +pi/6] (duration = T/6)
    e_p1 = _solve_kepler(-math.pi / 6.0, ecc)
    e_p2 = _solve_kepler(+math.pi / 6.0, ecc)
    area_peri = _sector_area_from_E(e_p1, e_p2, a, ecc)
    # Sector 2 around aphelion: M in [5*pi/6, 7*pi/6] (duration = T/6)
    e_a1 = _solve_kepler(5.0 * math.pi / 6.0, ecc)
    e_a2 = _solve_kepler(7.0 * math.pi / 6.0, ecc)
    area_aph = _sector_area_from_E(e_a1, e_a2, a, ecc)
    assert abs(area_peri - total_area / 6.0) < 1e-9
    assert abs(area_aph - total_area / 6.0) < 1e-9
    assert abs(area_peri - area_aph) < 1e-10

    # 3. Earth Northern Summer vs Winter asymmetry (e = 0.01671, perihelion near winter solstice)
    # Exact Kepler equation difference between two halves split by perpendicular chord through focus (theta = +-pi/2, +-3pi/2):
    # At theta = pi/2: cos(theta) = 0 -> cos(E) = e -> sin(E) = sqrt(1 - e^2)
    # Time from -pi/2 to +pi/2 (perihelion half, autumn+winter):
    # Delta_M_winter = 2 * (arccos(e) - e*sqrt(1-e^2))
    e_earth = 0.01671
    e_anom_eq = math.acos(e_earth)
    frac_winter = (2.0 * (e_anom_eq - e_earth * math.sqrt(1.0 - e_earth ** 2))) / (2.0 * math.pi)
    days_winter = 365.2422 * frac_winter
    days_summer = 365.2422 * (1.0 - frac_winter)
    diff_days = days_summer - days_winter
    assert 7.5 < diff_days < 8.0  # ~7.76 days! (actual ~7.6 days because perihelion is Jan 3, ~13 deg from solstice)

    # 4. Third Law across Solar System bodies (a in AU, T in Julian years)
    bodies = [
        ("Mercury", 0.38710, 0.24085),
        ("Venus", 0.72333, 0.61520),
        ("Earth", 1.00000, 1.00000),
        ("Mars", 1.52368, 1.88085),
        ("Ceres", 2.7675, 4.604),
        ("Jupiter", 5.20260, 11.8620),
        ("Saturn", 9.53707, 29.4475),
        ("Halley", 17.834, 75.32),
        ("Uranus", 19.1913, 84.0168),
        ("Neptune", 30.0690, 164.791),
    ]
    for name, a_au, t_yr in bodies:
        ratio = (t_yr ** 2) / (a_au ** 3)
        assert 0.997 < ratio < 1.003, f"{name} ratio={ratio}"

    # 5. Star S2 around Sgr A*: a ~ 1020 AU (at d=8.18 kpc, 0.1254" * 8180 = 1025.8 AU), T = 16.0518 yr
    a_s2 = 0.1254 * 8178.0  # GRAVITY 2019 distance ~8178 pc -> a = 1025.5 AU
    t_s2 = 16.0518
    m_bh_solar = (a_s2 ** 3) / (t_s2 ** 2)
    assert 4.10e6 < m_bh_solar < 4.30e6  # ~4.19e6 M_sun!


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker_end=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    m_attr = f' marker-end="url(#{marker_end})"' if marker_end else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}"{d_attr}{m_attr}/>'
    )


def build_fig1_tycho_mars_triangulation():
    """Fig 1: Tycho's 8-arcminute crisis + Kepler's 687-day Mars cosmic triangulation."""
    el = []
    el.extend(
        header(
            "既没望远镜更没飞出地球，开普勒怎么量出火星的三维轨道？",
            "靠第谷精确到 1～2 角分的肉眼星表“死磕 8 角分误差”，再用 687 天重合法在太空中解三角形！",
        )
    )

    # Left Card: The 8-arcminute crisis
    el.append(card(22, 68, 342, 378, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(60, 95, "导火索：逼疯开普勒的“8 角分裂缝”", size=13, color=INK, weight="700"))

    # Visual comparison of Full Moon (30') vs 8' error vs Tycho's 2' precision
    el.append(card(36, 112, 314, 152, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(193, 132, "夜空视角尺度直观对比（1° = 60 角分 = 60′）", size=11.5, color=INK, anchor="middle", weight="700"))

    # Moon circle r=42 px -> diameter = 84 px represents 30' (2.8 px per arcmin!)
    el.append(f'<circle cx="104" cy="196" r="42" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="1.8"/>')
    el.append(_line(62, 196, 146, 196, color=GOLD, sw=1.4, dash="3,3"))
    el.append(txt(104, 191, "满月视直径", size=11, color=GOLD, anchor="middle", weight="700"))
    el.append(txt(104, 210, "≈ 30′ (0.5°)", size=11, color=BODY, anchor="middle"))

    # 8' gap bar (8 * 2.8 = 22.4 px) and 2' Tycho error bar (5.6 px)
    el.append(txt(162, 166, "• 开普勒“代用偏心圆”最大偏差：", size=11, color=BODY))
    el.append(f'<rect x="174" y="175" width="45" height="12" rx="3" fill="{RED}"/>')
    el.append(txt(226, 185, "8′（约满月 1/4 宽）", size=11, color=RED, weight="700"))

    el.append(txt(162, 210, "• 第谷墙象限仪肉眼极限误差：", size=11, color=BODY))
    el.append(f'<rect x="174" y="219" width="11" height="12" rx="2" fill="{GREEN}"/>')
    el.append(txt(193, 229, "仅 1′～2′（一缕发丝宽）", size=11, color=GREEN, weight="700"))
    el.append(txt(193, 255, "8′ 远超第谷误差上限 ⇒ 两千年正圆假说必错！", size=11, color=RED, anchor="middle", weight="700"))

    # Three-stage battle with Mars
    el.append(card(36, 276, 314, 156, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(48, 298, "开普勒“向战神马尔斯宣战”的三轮试错：", size=12, color=ORANGE, weight="700"))
    el.append(txt(48, 322, "① 偏心正圆（Ch.39–44）：两侧轨道偏胖，超调 +8′", size=11, color=BODY))
    el.append(txt(48, 344, "② 鸡蛋形卵线（Ch.45–50）：两侧收得太窄，反偏 −8′", size=11, color=BODY))
    el.append(txt(48, 366, "③ 1605 复活节顿悟（Ch.58）：正圆与卵线正中间——", size=11, color=INK, weight="600"))
    el.append(txt(62, 388, "椭圆 r = a(1 − e cos E) 完美命中全部观测！", size=11.5, color=GREEN, weight="700"))
    el.append(txt(48, 414, "注：开普勒顺手发明了“轨道(orbit)”与“焦点(focus)”两词", size=10.5, color=MUTED))

    # Right Card: 687-day Cosmic Triangulation
    el.append(card(378, 68, 360, 378, fill=CARD_BG))
    el.append(step_badge(398, 90, 2, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(416, 95, "破局神技：每隔 687 天给火星“太空三角定位”", size=13, color=INK, weight="700"))

    # Geometric diagram inside right card
    el.append(card(392, 112, 332, 220, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    sx, sy = 532.0, 226.0  # Sun S
    r_earth_px = 64.0
    # Earth orbit circle
    el.append(f'<circle cx="{sx}" cy="{sy}" r="{r_earth_px}" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="4,3"/>')
    # Mars partial elliptical path
    el.append(f'<ellipse cx="{sx - 12}" cy="{sy}" rx="116" ry="112" fill="none" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="6,4"/>')

    # Fixed Mars spatial point M (revisited every 687.0 days!)
    mx, my = sx + 92.0, sy - 58.0  # (624, 168)
    # Two Earth positions separated by 687 days (= 2*365.25 - 43.5 days -> ~42.9 deg apart!)
    ang1 = math.radians(-12.0)
    ang2 = math.radians(-68.0)
    e1x, e1y = sx + r_earth_px * math.cos(ang1), sy + r_earth_px * math.sin(ang1)
    e2x, e2y = sx + r_earth_px * math.cos(ang2), sy + r_earth_px * math.sin(ang2)

    # Triangle edges: S-M, S-E1, S-E2, E1-M, E2-M
    el.append(_line(sx, sy, mx, my, color=RED, sw=2.2))
    el.append(_line(sx, sy, e1x, e1y, color=BLUE, sw=1.8))
    el.append(_line(sx, sy, e2x, e2y, color=BLUE, sw=1.8))
    el.append(_line(e1x, e1y, mx, my, color=GREEN, sw=1.8, dash="4,2"))
    el.append(_line(e2x, e2y, mx, my, color=GREEN, sw=1.8, dash="4,2"))

    # Sun, E1, E2, M dots
    el.append(f'<circle cx="{sx}" cy="{sy}" r="8" fill="{GOLD}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(sx - 14, sy + 5, "太阳 S", size=11.5, color=GOLD, anchor="end", weight="700", halo=True))

    el.append(f'<circle cx="{e1x:.1f}" cy="{e1y:.1f}" r="5.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(e1x + 8, e1y + 14, "地球 E₁ (第 0 天)", size=11, color=BLUE, weight="700", halo=True))

    el.append(f'<circle cx="{e2x:.1f}" cy="{e2y:.1f}" r="5.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(e2x - 6, e2y - 8, "地球 E₂ (第 687 天)", size=11, color=BLUE, anchor="end", weight="700", halo=True))

    el.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="6.5" fill="{RED}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(mx + 8, my - 6, "火星同一点 M", size=11.5, color=RED, weight="700", halo=True))
    el.append(txt(580, 206, "rM = ?", size=11.5, color=RED, weight="700", halo=True))
    el.append(txt(458, 318, "地球轨道半径 ≈ 1 AU（已知基线尺）", size=11, color=BLUE, weight="600"))

    # Step-by-step explanation box under diagram
    el.append(card(392, 342, 332, 90, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(404, 363, "• 关键妙招：火星恒星周期 T火 = 687.0 天早已测准！", size=11, color=INK, weight="700"))
    el.append(txt(404, 384, "• 挑相隔 687 天的两夜：火星必回到宇宙同一点 M，而地球", size=11, color=BODY))
    el.append(txt(404, 403, "  换到了 E₁、E₂ 两处，实测视线角即可解出日火距离 rM！", size=11, color=BODY))
    el.append(txt(404, 422, "• 攒够几十个点 M₁, M₂… 真相浮现：不是正圆，是椭圆！", size=11, color=GREEN, weight="700"))

    # Footer
    el.append(card(22, 458, 716, 42, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            484,
            "为什么偏偏是火星立功？金星(e=0.007)和地球(e=0.017)太接近正圆，肉眼绝难分辨；火星(e=0.093)是肉眼可见最偏的外行星！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        514,
        "第谷8角分观测危机与开普勒687天火星三角测量法图解",
        "左图对比满月视直径(30角分)、开普勒偏心圆误差(8角分)与第谷肉眼观测精度(1-2角分)；右图展示利用火星687天周期回到空间同一点M，从地球轨道两处E1、E2解三角形测定日火距离。",
        el,
    )
    write_svg(SUBDIR, "tycho-mars-687d-triangulation.svg", svg)


def build_fig2_first_law_ellipse_and_conics():
    """Fig 2: Law I exact geometry, the visual flattening illusion (0.44% vs 9.34%), and conic energy family."""
    el = []
    el.extend(
        header(
            "第一定律（椭圆定律）全拆解：别被夸张示意图骗了，“偏心”比“压扁”显著得多！",
            "行星沿椭圆运行，太阳独占其中一个焦点（另一焦点空无一物）；总机械能 E 决定四类圆锥曲线命运",
        )
    )

    # Left Card: Full Ellipse Anatomy (e = 0.60 pedagogical model)
    el.append(card(22, 68, 392, 384, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 95, "椭圆几何解剖图（以 e = 0.60 放大示意几何关系）", size=12.5, color=INK, weight="700"))

    cx, cy = 218.0, 232.0
    a_px = 145.0
    ecc = 0.60
    b_px = a_px * math.sqrt(1.0 - ecc * ecc)  # 145 * 0.8 = 116 px
    c_px = a_px * ecc                         # 145 * 0.6 = 87 px
    f1x, f1y = cx + c_px, cy                  # Sun at right focus (305, 232)
    f2x, f2y = cx - c_px, cy                  # Empty focus at left (131, 232)

    # Major and minor axes
    el.append(_line(cx - a_px, cy, cx + a_px, cy, color=BORDER, sw=1.3, dash="4,3"))
    el.append(_line(cx, cy - b_px, cx, cy + b_px, color=BORDER, sw=1.3, dash="4,3"))

    # Ellipse curve
    el.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{a_px}" ry="{b_px:.1f}" fill="{BLUE_SOFT}" fill-opacity="0.42" stroke="{BLUE}" stroke-width="2.6"/>')

    # Planet P at E = 65 deg
    e_ang = math.radians(65.0)
    px = cx + a_px * math.cos(e_ang)
    py = cy - b_px * math.sin(e_ang)

    # Two string segments r1 + r2 = 2a
    el.append(_line(f1x, f1y, px, py, color=ORANGE, sw=2.2))
    el.append(_line(f2x, f2y, px, py, color=PURPLE, sw=1.8, dash="5,3"))

    # Semi-latus rectum p = a(1-e^2) vertical chord at F1
    p_px = a_px * (1.0 - ecc * ecc)  # 145 * 0.64 = 92.8 px
    el.append(_line(f1x, f1y, f1x, f1y - p_px, color=GREEN, sw=1.8, dash="3,2"))
    el.append(txt(f1x + 6, f1y - 48, "半通径 p", size=10.5, color=GREEN, weight="700", halo=True))

    # Center O, Empty Focus F2, Sun Focus F1, Perihelion, Aphelion, Planet P
    el.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{SLATE}"/>')
    el.append(txt(cx, cy + 17, "中心 O", size=11, color=SLATE, anchor="middle", halo=True))

    el.append(f'<circle cx="{f2x}" cy="{f2y}" r="5" fill="#ffffff" stroke="{PURPLE}" stroke-width="2" stroke-dasharray="2,2"/>')
    el.append(txt(f2x, f2y + 20, "空焦点 F₂", size=11, color=PURPLE, anchor="middle", weight="600", halo=True))
    el.append(txt(f2x, f2y + 34, "(空无一物!)", size=10.5, color=MUTED, anchor="middle", halo=True))

    el.append(f'<circle cx="{f1x}" cy="{f1y}" r="9" fill="{GOLD}" stroke="#ffffff" stroke-width="2"/>')
    el.append(txt(f1x - 4, f1y + 23, "太阳 F₁", size=11.5, color=GOLD, anchor="middle", weight="700", halo=True))

    # Perihelion & Aphelion dots
    el.append(f'<circle cx="{cx + a_px}" cy="{cy}" r="4.5" fill="{RED}"/>')
    el.append(txt(cx + a_px + 4, cy - 10, "近日点", size=11, color=RED, anchor="end", weight="700", halo=True))
    el.append(f'<circle cx="{cx - a_px}" cy="{cy}" r="4.5" fill="{BLUE}"/>')
    el.append(txt(cx - a_px + 4, cy - 10, "远日点", size=11, color=BLUE, anchor="start", weight="700", halo=True))

    # Planet dot
    el.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6.5" fill="{BLUE}" stroke="#ffffff" stroke-width="2"/>')
    el.append(txt(px + 8, py - 8, "行星 P", size=11.5, color=BLUE, weight="700", halo=True))
    el.append(txt((f1x + px) / 2 + 8, (f1y + py) / 2 - 4, "r₁", size=11.5, color=ORANGE, weight="700", halo=True))
    el.append(txt((f2x + px) / 2 - 8, (f2y + py) / 2 - 6, "r₂", size=11.5, color=PURPLE, weight="700", halo=True))

    # Dimension annotations at bottom of Left Card
    el.append(card(36, 362, 364, 78, rx=7, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(48, 382, "• 绳长铁律：r₁ + r₂ = 2a（半长轴 a）；半焦距 c = a·e", size=11, color=INK, weight="600"))
    el.append(txt(48, 402, "• 近日距 r近 = a(1−e)，远日距 r远 = a(1+e)，短半轴 b = a√(1−e²)", size=11, color=BODY))
    el.append(txt(48, 422, "• 极坐标方程（以太阳为原点）：r(θ) = a(1−e²) / (1 + e cos θ)", size=11, color=BLUE, weight="700"))

    # Right Card: Top = Real Mars Scale Surprise; Bottom = Conic Section Family
    el.append(card(428, 68, 310, 192, fill=CARD_BG))
    el.append(step_badge(448, 90, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(466, 95, "视觉反常识：真实火星轨道有多“圆”？", size=12.5, color=INK, weight="700"))

    # Real Mars orbit circle vs ellipse (r = 46 px)
    mcx, mcy, mr = 492.0, 170.0, 46.0
    el.append(f'<circle cx="{mcx}" cy="{mcy}" r="{mr}" fill="none" stroke="{SLATE}" stroke-width="1.5" stroke-dasharray="3,3"/>')
    # True Mars ry = 46 * 0.9956 = 45.8 px! Sun offset = 46 * 0.0934 = 4.3 px!
    el.append(f'<ellipse cx="{mcx}" cy="{mcy}" rx="{mr}" ry="45.8" fill="none" stroke="{ORANGE}" stroke-width="2.2"/>')
    el.append(f'<circle cx="{mcx}" cy="{mcy}" r="2.5" fill="{SLATE}"/>')
    el.append(f'<circle cx="{mcx + 4.3:.1f}" cy="{mcy}" r="5.2" fill="{GOLD}"/>')
    el.append(txt(492, 238, "真实火星轨道 (e=0.093)", size=10.5, color=ORANGE, anchor="middle", weight="600"))

    el.append(txt(556, 130, "对火星 e = 0.0934：", size=11.5, color=INK, weight="700"))
    el.append(txt(556, 152, "• 焦点偏移 c/a = 9.34%", size=11, color=RED, weight="700"))
    el.append(txt(556, 170, "  （一阶效应 ∝ e，很明显）", size=10.5, color=MUTED))
    el.append(txt(556, 194, "• 短轴缩扁 1−b/a = 0.44%!", size=11, color=BLUE, weight="700"))
    el.append(txt(556, 212, "  （二阶效应 ≈ e²/2，肉眼", size=10.5, color=MUTED))
    el.append(txt(556, 228, "   几乎看不出比正圆扁！）", size=10.5, color=MUTED))

    # Bottom Right Card: 4 Conic Sections by Energy E
    el.append(card(428, 272, 310, 180, fill=CARD_BG))
    el.append(step_badge(448, 294, 3, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(466, 299, "牛顿推广：总机械能 E 决定四类轨道", size=12.5, color=INK, weight="700"))

    rows = [
        ("正圆 e = 0", "E = −GMm/(2r) 极小值", GREEN),
        ("椭圆 0 < e < 1", "E = −GMm/(2a) < 0（行星/彗星）", BLUE),
        ("抛物线 e = 1", "E = 0（第二宇宙速度逃逸临界）", ORANGE),
        ("双曲线 e > 1", "E > 0（星际访客，如奥陌陌）", RED),
    ]
    ry = 328
    for tag, desc, col in rows:
        el.append(txt(440, ry, tag, size=11, color=col, weight="700"))
        el.append(txt(524, ry, desc, size=10.5, color=BODY))
        ry += 30

    # Footer
    el.append(card(22, 464, 716, 42, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(
        txt(
            380,
            490,
            "记忆口诀：地球轨道短轴仅比长轴短 0.014%（画在 A4 纸上差不到半根头发丝），但日地距离冬夏却实打实差了 500 万公里！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "开普勒第一定律椭圆几何解剖与真实偏心率对比图",
        "左图展示椭圆两焦点(太阳在F1、F2为空)、半长轴a、短半轴b、半通径p与r1+r2=2a；右上对比真实火星轨道焦点偏移9.34%而短轴仅缩扁0.44%；右下列出按总能量E划分的四类圆锥曲线轨道。",
        el,
    )
    write_svg(SUBDIR, "first-law-ellipse-trap-and-conics.svg", svg)


def build_fig3_second_law_anim():
    """Fig 3: Animated Second Law using exact Kepler equation steps + Northern Summer vs Winter asymmetry."""
    ecc = 0.55
    cx, cy = 216.0, 246.0
    a_px = 148.0
    b_px = a_px * math.sqrt(1.0 - ecc * ecc)  # 123.6 px
    c_px = a_px * ecc                         # 81.4 px
    sx, sy = cx + c_px, cy                    # Sun at right focus (297.4, 246)

    def pt_from_M(m_rad):
        e_val = _solve_kepler(m_rad, ecc)
        return cx + a_px * math.cos(e_val), cy - b_px * math.sin(e_val)

    # Build exact polygon path for Perihelion sector M in [-pi/6, +pi/6] (duration = T/6)
    peri_pts = [(sx, sy)] + [pt_from_M(-math.pi / 6.0 + (math.pi / 3.0) * i / 32.0) for i in range(33)]
    peri_poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in peri_pts)

    # Build exact polygon path for Aphelion sector M in [5*pi/6, 7*pi/6] (duration = T/6)
    aph_pts = [(sx, sy)] + [pt_from_M(5.0 * math.pi / 6.0 + (math.pi / 3.0) * i / 32.0) for i in range(33)]
    aph_poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in aph_pts)

    # Build 25 CSS keyframe samples (0%, 4%, 8%, ..., 100%) strictly uniform in TIME (Mean Anomaly M)!
    kf_lines = []
    for k in range(25):
        pct = k * 4
        m_val = 2.0 * math.pi * (k / 24.0)
        px, py = pt_from_M(m_val)
        kf_lines.append(f"    {pct}% {{ transform: translate({px:.1f}px, {py:.1f}px); }}")
    kf_block = "\n".join(kf_lines)
    p0x, p0y = pt_from_M(0.0)

    extra_css = f"""
  .kp-planet {{
    transform: translate({p0x:.1f}px, {p0y:.1f}px);
    animation: keplerTrueOrbit 7s linear 0.4s 1 forwards;
  }}
  @keyframes keplerTrueOrbit {{
{kf_block}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .kp-planet {{
      animation: none !important;
      transform: translate({p0x:.1f}px, {p0y:.1f}px) !important;
    }}
  }}
"""

    el = []
    el.extend(
        header(
            "第二定律（等面积定律）真实计时动画：为什么北半球夏天比冬天多出近 8 天？",
            "太阳与行星连线在相等时间内扫过相等面积；近处柄短必狂奔，远处柄长慢散步（按开普勒方程精确计时）",
        )
    )

    # Left Card: True-time orbital sweep
    el.append(card(22, 68, 396, 386, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(60, 95, "每隔 T/12 等时间闪光拍照（e = 0.55 模型）", size=12.5, color=INK, weight="700"))

    # Equal-area shaded sectors (each = T/6 = 1/6 of total ellipse area!)
    el.append(f'<polygon points="{peri_poly}" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(f'<polygon points="{aph_poly}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')

    # Full ellipse orbit
    el.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{a_px}" ry="{b_px:.1f}" fill="none" stroke="{INK}" stroke-width="2"/>')

    # 12 equal-time strobe dots around the orbit
    for j in range(12):
        mx, my = pt_from_M(2.0 * math.pi * j / 12.0)
        col = ORANGE if j in (0, 1, 11) else (BLUE if j in (5, 6, 7) else SLATE)
        el.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="4.2" fill="{col}" stroke="#ffffff" stroke-width="1.2"/>')

    # Sun at focus
    el.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="9.5" fill="{GOLD}" stroke="#ffffff" stroke-width="2"/>')
    el.append(txt(sx - 14, sy + 5, "太阳", size=11.5, color=GOLD, anchor="end", weight="700", halo=True))

    # Animated planet marker (starts & ends cleanly at perihelion M=0)
    el.append(
        f'<g class="kp-planet"><circle cx="0" cy="0" r="7.5" fill="{RED}" stroke="#ffffff" stroke-width="2.2"/></g>'
    )

    # Sector labels (carefully placed with zero overlap!)
    el.append(txt(332, 250, "扇形 A₁", size=11.5, color=ORANGE, anchor="middle", weight="700", halo=True))
    el.append(txt(332, 267, "(耗时 T/6)", size=10.5, color=ORANGE, anchor="middle", weight="600", halo=True))

    el.append(txt(148, 246, "扇形 A₂ (耗时 T/6)", size=11.5, color=BLUE, anchor="middle", weight="700", halo=True))
    el.append(txt(148, 264, "面积 A₂ = A₁ 严格相等！", size=10.5, color=BLUE, anchor="middle", weight="600", halo=True))

    el.append(txt(338, 128, "近日点狂奔", size=11.5, color=RED, anchor="middle", weight="700", halo=True))
    el.append(txt(338, 145, "v近/v远 = 3.44 倍!", size=10.5, color=RED, anchor="middle", weight="600", halo=True))
    el.append(txt(104, 134, "远日点慢走", size=11.5, color=BLUE, anchor="middle", weight="700", halo=True))
    el.append(txt(104, 151, "点位密集成串", size=10.5, color=MUTED, anchor="middle", halo=True))

    # Bottom caption inside left card
    el.append(card(36, 386, 368, 54, rx=7, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(220, 407, "注：红球按开普勒方程 M = E − e sin E 真实非匀速运动 1 圈；", size=11, color=INK, anchor="middle", weight="600"))
    el.append(txt(220, 426, "即使未播放动画，12 个等时闪光点疏密也直观呈现快慢反差。", size=10.5, color=MUTED, anchor="middle"))

    # Right Card: Top = Angular Momentum Essence; Bottom = Earth Season Length Mystery!
    el.append(card(432, 68, 306, 182, fill=CARD_BG))
    el.append(step_badge(452, 90, 2, fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(470, 95, "物理本质：中心力场角动量守恒！", size=12.5, color=INK, weight="700"))

    el.append(card(444, 112, 282, 124, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(456, 134, "• 引力沿连线指向太阳 ⇒ 力矩 τ = r × F = 0", size=11, color=INK, weight="600"))
    el.append(txt(456, 156, "• 角动量 L = m r v⊥ 全程守恒不变！", size=11, color=PURPLE, weight="700"))
    el.append(txt(456, 178, "• 掠面速率 dA/dt = L / (2m) = 常数", size=11.5, color=BLUE, weight="700"))
    el.append(txt(456, 200, "• 近日/远日点切线垂直连线：v近 / v远 = (1+e)/(1−e)", size=10.5, color=BODY))
    el.append(txt(456, 220, "• 适用边界：只要是中心力（哪怕平方不反比）皆成立！", size=10.5, color=GREEN, weight="700"))

    # Bottom Right Card: Why Northern Summer is 7.6 days longer than Winter
    el.append(card(432, 262, 306, 192, fill=CARD_BG))
    el.append(step_badge(452, 284, 3, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(470, 289, "身边的彩蛋：北半球夏天多赚 7.6 天！", size=12.5, color=INK, weight="700"))

    el.append(card(444, 306, 282, 134, rx=7, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(456, 327, "• 1 月初地球过近日点（北半球隆冬！）：", size=11, color=INK, weight="600"))
    el.append(txt(456, 346, "  公转极速 30.29 km/s → 秋冬半圈嗖一下跑完！", size=11, color=ORANGE, weight="700"))
    el.append(txt(456, 369, "• 7 月初地球过远日点（北半球盛夏！）：", size=11, color=INK, weight="600"))
    el.append(txt(456, 388, "  公转慢速 29.29 km/s → 春夏半圈慢悠悠散步！", size=11, color=BLUE, weight="700"))
    el.append(_line(456, 400, 714, 400, color=GREEN, sw=1))
    el.append(txt(585, 422, "春分→秋分 186.4 天 vs 秋分→春分 178.8 天", size=11, color=INK, anchor="middle", weight="700"))

    # Footer
    el.append(card(22, 466, 716, 42, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(
        txt(
            380,
            492,
            "历史冷知识：开普勒在 1602 年先发现了“第二定律（面积律）”，靠它做时间标尺，才在 3 年后算出了“第一定律（椭圆律）”！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        522,
        "开普勒第二定律等面积真实计时动画与地球四季时长差异图",
        "左图按开普勒方程精确计算12个等时间间隔位置及近远日点等面积扇形(各占T/6)，附7秒单次真实运动动画；右图说明角动量守恒本质及地球1月过近日点导致北半球春夏比秋冬长7.6天。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "second-law-equal-area-and-seasons-anim.svg", svg)


def build_fig4_third_law_loglog_and_scale():
    """Fig 4: Real computed log10(T) vs log10(a) plot for Solar System + Newton's cosmic weighing scale."""
    el = []
    el.extend(
        header(
            "第三定律（调和定律 T² ∝ a³）：跨越百倍距离，十颗天体严丝合缝钉在斜率 1.5 直线上！",
            "1618 年 5 月 15 日开普勒在战火与审巫案奔波中算出的宇宙节律；牛顿进一步把它升级成“天体电子秤”",
        )
    )

    # Left Card: Exact log10(T [yr]) vs log10(a [AU]) plot
    el.append(card(22, 68, 424, 386, fill=CARD_BG))
    el.append(txt(40, 93, "太阳系实测对数图：log₁₀(T/年) = 1.5 · log₁₀(a/AU)", size=12.5, color=INK, weight="700"))

    # Plot box mapping:
    # log10(a) in [-0.5, 1.6] -> x from 86 to 416 (width = 330 px -> 157.14 px per unit)
    # log10(T) in [-0.75, 2.40] -> y from 396 to 118 (height = 278 px -> 88.25 px per unit)
    def map_pt(log_a, log_t):
        x = 86.0 + (log_a - (-0.5)) / 2.1 * 330.0
        y = 396.0 - (log_t - (-0.75)) / 3.15 * 278.0
        return x, y

    # Grid lines for log10(a) = 0, 0.5, 1.0, 1.5
    for la, lbl in [(0.0, "1 AU"), (0.5, "3.16"), (1.0, "10 AU"), (1.5, "31.6 AU")]:
        gx, _ = map_pt(la, 0.0)
        el.append(_line(gx, 116, gx, 396, color=BORDER, sw=1, dash="3,3"))
        el.append(txt(gx, 414, lbl, size=10.5, color=SLATE, anchor="middle"))

    for lt, lbl in [(0.0, "1 年"), (1.0, "10 年"), (2.0, "100 年")]:
        _, gy = map_pt(0.0, lt)
        el.append(_line(86, gy, 420, gy, color=BORDER, sw=1, dash="3,3"))
        el.append(txt(78, gy + 4, lbl, size=10.5, color=SLATE, anchor="end"))

    # Axes
    el.append(_line(86, 396, 428, 396, color=INK, sw=1.8, marker_end="arr-muted"))
    el.append(_line(86, 396, 86, 118, color=INK, sw=1.8, marker_end="arr-muted"))
    el.append(txt(256, 436, "轨道半长轴 a（对数刻度，AU）", size=11, color=INK, anchor="middle", weight="600"))
    el.append(txt(76, 124, "周期 T", size=11, color=INK, anchor="end", weight="600"))

    # Exact theoretical line T = a^(1.5) from log_a = -0.48 to +1.55
    lx1, ly1 = map_pt(-0.48, -0.72)
    lx2, ly2 = map_pt(1.55, 2.325)
    el.append(_line(lx1, ly1, lx2, ly2, color=BLUE, sw=2.4))

    # Plot real Solar System points with non-overlapping label offsets!
    pts = [
        ("水星", 0.38710, 0.24085, 8, 12, "start", INK),
        ("金星", 0.72333, 0.61520, -8, -8, "end", INK),
        ("地球", 1.00000, 1.00000, 9, 11, "start", BLUE),
        ("火星", 1.52368, 1.88085, 9, 10, "start", ORANGE),
        ("谷神星", 2.7675, 4.604, -8, -8, "end", SLATE),
        ("木星", 5.20260, 11.8620, 9, 10, "start", INK),
        ("土星", 9.53707, 29.4475, -9, -7, "end", INK),
        ("哈雷彗星(e=0.967!)", 17.834, 75.32, -10, -8, "end", RED),
        ("天王星", 19.1913, 84.0168, 9, 12, "start", INK),
        ("海王星", 30.0690, 164.791, -10, -8, "end", BLUE),
    ]
    for name, a_au, t_yr, dx, dy, anc, col in pts:
        px, py = map_pt(math.log10(a_au), math.log10(t_yr))
        r_dot = 5.5 if "哈雷" in name or name in ("地球", "火星") else 4.5
        fill_c = RED if "哈雷" in name else (ORANGE if name == "火星" else BLUE)
        el.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_dot}" fill="{fill_c}" stroke="#ffffff" stroke-width="1.4"/>')
        el.append(txt(px + dx, py + dy, name, size=10.5, color=col, anchor=anc, weight="700" if "哈雷" in name else "600", halo=True))

    el.append(txt(264, 356, "斜率严格 = 3/2 = 1.500", size=12, color=BLUE, weight="700", halo=True))
    el.append(txt(264, 374, "哈雷彗星极扁却仍在同一直线上！", size=10.5, color=RED, weight="600", halo=True))

    # Right Card: Newton's Exact Formula & Why T only depends on a (not e!)
    el.append(card(460, 68, 278, 386, fill=CARD_BG))
    el.append(step_badge(480, 90, 2, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(498, 95, "牛顿揭秘：这其实是一台宇宙秤！", size=12.5, color=INK, weight="700"))

    el.append(card(472, 112, 254, 126, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(599, 134, "牛顿双体精确版第三定律：", size=11.5, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(599, 162, "T² = [ 4π² / G(M + m) ] · a³", size=13.5, color=INK, anchor="middle", weight="700"))
    el.append(txt(484, 188, "• 比例常数 K = 4π²/[G(M+m)] 由中心", size=11, color=BODY))
    el.append(txt(484, 206, "  总质量决定（不同主星绝不能混用！）", size=11, color=RED, weight="600"))
    el.append(txt(484, 226, "• 木星重约太阳 1/1047 ⇒ T²/a³ 偏小 0.1%", size=10.5, color=MUTED))

    el.append(card(472, 250, 254, 92, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(599, 272, "奇迹追问：为什么周期 T 跟偏心率 e 无关？", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(484, 294, "• 椭圆面积 A = πab = πa²√(1−e²)", size=11, color=BODY))
    el.append(txt(484, 314, "• 角动量 L = m√[GMa(1−e²)]", size=11, color=BODY))
    el.append(txt(484, 333, "• 相除 T = A/(L/2m) 时 √(1−e²) 完美约掉！", size=11, color=INK, weight="700"))

    el.append(card(472, 354, 254, 86, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(599, 375, "隔空称天体秘诀：只要它有卫星！", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(484, 396, "• 看木卫绕木星 (a, T) ⇒ 直接算出木星质量", size=10.5, color=BODY))
    el.append(txt(484, 415, "• 金星无天然卫星 ⇒ 直到飞船掠过才称准！", size=10.5, color=INK, weight="600"))

    # Footer
    el.append(card(22, 466, 716, 42, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(
        txt(
            380,
            492,
            "核心洞见：同半长轴 a 的正圆行星与细长彗星，总机械能 E = −GMm/(2a) 一模一样，跑完一圈的周期 T 也一秒不差！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        522,
        "太阳系十天体开普勒第三定律对数实测图与牛顿天体称重原理",
        "左图按真实天文数据绘制水星至海王星、谷神星及高偏心率哈雷彗星的 log(T)-log(a) 图，全部落在斜率1.5直线上；右图解释牛顿双体质量修正及偏心率因子在周期推导中精确相消。",
        el,
    )
    write_svg(SUBDIR, "third-law-loglog-solar-system.svg", svg)


def build_fig5_modern_blackhole_and_darkmatter():
    """Fig 5: Modern triumphs & productive breakdowns — Sgr A* star S2 + Dark Matter & GR precession."""
    el = []
    el.extend(
        header(
            "四百年后的硬核战场：用开普勒定律称出银心黑洞，再用它的“失效”揪出暗物质！",
            "当观测完美符合它，人类找到了 415 万倍太阳质量黑洞；当观测违背它，人类发现了广义相对论与暗物质晕",
        )
    )

    # Left Card: Star S2 orbiting Sgr A* (2020 Nobel Prize)
    el.append(card(22, 68, 356, 382, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(60, 95, "巅峰应用：恒星 S2 称出银河系中心黑洞", size=12.5, color=INK, weight="700"))

    # True aspect ellipse for S2 (e = 0.8847 -> b/a = sqrt(1 - 0.8847^2) = 0.4662!)
    el.append(card(36, 112, 328, 198, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    scx, scy = 196.0, 206.0
    sa = 112.0
    se = 0.8847
    sb = sa * math.sqrt(1.0 - se * se)  # 52.2 px
    sc = sa * se                         # 99.1 px
    bhx, bhy = scx + sc, scy             # Sgr A* at (295.1, 206)

    # Rotate ellipse slightly (-22 deg) for authentic visual clarity while keeping labels crystal clear
    el.append(
        f'<g transform="rotate(-18 {scx} {scy})">'
        f'<ellipse cx="{scx}" cy="{scy}" rx="{sa}" ry="{sb:.1f}" fill="{PURPLE_SOFT}" fill-opacity="0.55" stroke="{PURPLE}" stroke-width="2.4"/>'
        f'</g>'
    )
    # Compute rotated black hole focus & pericenter & apocenter coordinates
    rot = math.radians(-18.0)
    bh_rx = scx + sc * math.cos(rot)
    bh_ry = scy + sc * math.sin(rot)
    peri_rx = scx + sa * math.cos(rot)
    peri_ry = scy + sa * math.sin(rot)
    apo_rx = scx - sa * math.cos(rot)
    apo_ry = scy - sa * math.sin(rot)

    el.append(f'<circle cx="{bh_rx:.1f}" cy="{bh_ry:.1f}" r="7.5" fill="#111827" stroke="{GOLD}" stroke-width="2.2"/>')
    el.append(txt(bh_rx - 12, bh_ry - 12, "银心黑洞 Sgr A*", size=11, color=INK, anchor="end", weight="700", halo=True))

    el.append(f'<circle cx="{peri_rx:.1f}" cy="{peri_ry:.1f}" r="5" fill="{RED}"/>')
    el.append(txt(peri_rx + 2, peri_ry + 18, "2018 近心点: 7,650 km/s!", size=10.5, color=RED, anchor="end", weight="700", halo=True))

    el.append(f'<circle cx="{apo_rx:.1f}" cy="{apo_ry:.1f}" r="5" fill="{BLUE}"/>')
    el.append(txt(apo_rx + 6, apo_ry + 22, "恒星 S2 (e=0.885)", size=11, color=PURPLE, anchor="start", weight="700", halo=True))
    el.append(txt(200, 296, "周期 T = 16.05 年，半长轴 a ≈ 1,020 AU", size=11, color=INK, anchor="middle", weight="600"))

    # Calculation summary box
    el.append(card(36, 320, 328, 118, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(48, 342, "• 直接代入第三定律 M = a³ / T²（太阳单位）：", size=11, color=INK, weight="600"))
    el.append(txt(200, 368, "M ≈ 1020³ / 16.05² ≈ 415 万倍太阳质量！", size=12, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(48, 392, "• 400 多万颗太阳塞进比海王星轨道大不了多少的空间", size=10.5, color=BODY))
    el.append(txt(48, 412, "• 根泽尔与盖兹凭此斩获 2020 年诺贝尔物理学奖！", size=11, color=GREEN, weight="700"))

    # Right Card: Two Historic Breakdowns -> Dark Matter & General Relativity
    el.append(card(392, 68, 346, 382, fill=CARD_BG))
    el.append(step_badge(412, 90, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(430, 95, "当开普勒定律“算不准”：两大新物理诞生！", size=12.5, color=INK, weight="700"))

    # Sub-plot: Galaxy Rotation Curve (Flat vs Keplerian r^-1/2)
    el.append(card(406, 112, 318, 188, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(418, 133, "反常 ①：星系外围恒星拒绝按 v ∝ 1/√r 减速！", size=11.5, color=BLUE, weight="700"))

    # Axes inside sub-card: x in [442, 704], y in [150, 258]
    el.append(_line(442, 258, 706, 258, color=INK, sw=1.5, marker_end="arr-muted"))
    el.append(_line(442, 258, 442, 148, color=INK, sw=1.5, marker_end="arr-muted"))
    el.append(txt(436, 158, "v", size=11, color=INK, anchor="end", weight="700"))
    el.append(txt(698, 274, "距星系中心距离 r", size=10.5, color=SLATE, anchor="end"))

    # Observed flat curve (solid red) vs Expected Keplerian decline (dashed blue)
    el.append('<path d="M442,258 Q466,182 496,178 L694,175" fill="none" stroke="#b91c1c" stroke-width="2.6"/>')
    el.append('<path d="M496,178 Q554,218 694,238" fill="none" stroke="#1d6fa5" stroke-width="2.2" stroke-dasharray="5,4"/>')

    el.append(txt(596, 166, "实测星系旋转曲线：v ≈ 常数（平坦！）", size=10.5, color=RED, anchor="middle", weight="700", halo=True))
    el.append(txt(612, 248, "开普勒预期：v ∝ r⁻¹/²", size=10.5, color=BLUE, anchor="middle", weight="600", halo=True))
    el.append(txt(565, 290, "推论：外围包着巨量看不见的“暗物质晕” M(r) ∝ r！", size=10.5, color=INK, anchor="middle", weight="700"))

    # Sub-box 2: General Relativity Precession
    el.append(card(406, 310, 318, 128, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(418, 332, "反常 ②：强引力场下椭圆不再严格闭合（进动）", size=11.5, color=ORANGE, weight="700"))
    el.append(txt(418, 355, "• 纯 1/r² 引力特有的拉普拉斯—龙格—楞次矢量守恒，", size=10.5, color=BODY))
    el.append(txt(418, 374, "  才保证理想二体椭圆万年不转圈；", size=10.5, color=BODY))
    el.append(txt(418, 396, "• 水星每世纪多转 43 角秒、恒星 S2 每圈进动 12 角分，", size=10.5, color=INK, weight="600"))
    el.append(txt(418, 416, "  精准验证爱因斯坦广义相对论的时空弯曲修正！", size=10.5, color=RED, weight="700"))

    # Footer
    el.append(card(22, 462, 716, 42, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            488,
            "科学史最美闭环：1609 年开普勒因“8 角分偏差”掀翻正圆；300 年后爱因斯坦因水星“43 角秒偏差”掀翻牛顿绝对时空！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        518,
        "开普勒定律现代前沿应用：银心黑洞S2轨道测重与星系暗物质旋转曲线",
        "左图展示恒星S2沿偏心率0.885椭圆每16.05年绕Sgr A*一周，由第三定律测出415万倍太阳质量黑洞；右图展示星系平坦旋转曲线揭示暗物质晕及近日点进动验证广义相对论。",
        el,
    )
    write_svg(SUBDIR, "modern-frontiers-blackhole-and-darkmatter.svg", svg)


@register("kepler-three-laws", "开普勒三大定律深度拆解原创图解集", "physics")
def build_all():
    _verify_physics()
    build_fig1_tycho_mars_triangulation()
    build_fig2_first_law_ellipse_and_conics()
    build_fig3_second_law_anim()
    build_fig4_third_law_loglog_and_scale()
    build_fig5_modern_blackhole_and_darkmatter()
