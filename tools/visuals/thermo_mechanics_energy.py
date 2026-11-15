"""Original Chinese SVG diagrams for Mechanics vs. Thermodynamics:
Energy Conservation & State Variables (assets/images/thermo-mechanics/).
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
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "thermo-mechanics"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#ecfdf5"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"


def _verify_physics():
    # 1. Exact SI / CODATA 2022 constants & Joule mechanical equivalent
    k_b = 1.380649e-23
    n_a = 6.02214076e23
    r_gas = k_b * n_a
    assert abs(r_gas - 8.314462618) < 1e-6

    cal_th = 4.184  # J per thermochemical calorie
    g_std = 9.80665
    # Height to drop 1 kg to warm 1 kg of water (4184 J/K) by 1 K:
    h_1k = 4184.0 / (1.0 * g_std)
    assert 426.0 < h_1k < 427.5  # ~426.65 m

    # 2. Exact P-V path comparison for n = 1 mol monatomic ideal gas
    # State A: P_A = 2.0 bar (2.0e5 Pa), V_A = 10.0 L (0.010 m^3) -> P_A*V_A = 2000 J = 2.00 kJ
    # State B: P_B = 1.0 bar (1.0e5 Pa), V_B = 30.0 L (0.030 m^3) -> P_B*V_B = 3000 J = 3.00 kJ
    p_a, v_a = 2.0e5, 0.010
    p_b, v_b = 1.0e5, 0.030
    u_a = 1.5 * p_a * v_a  # 3000 J
    u_b = 1.5 * p_b * v_b  # 4500 J
    du = u_b - u_a         # +1500 J = +1.50 kJ
    assert abs(du - 1500.0) < 1e-9

    # Path 1: Isobaric expansion at P_A to V_B, then isochoric cooling at V_B to P_B
    w_1 = p_a * (v_b - v_a)            # 4000 J = +4.00 kJ
    q_1 = du + w_1                     # 5500 J = +5.50 kJ
    # Path 2: Straight line from (V_A, P_A) to (V_B, P_B)
    w_2 = 0.5 * (p_a + p_b) * (v_b - v_a)  # 3000 J = +3.00 kJ
    q_2 = du + w_2                         # 4500 J = +4.50 kJ
    # Path 3: Isochoric cooling at V_A to P_B, then isobaric expansion at P_B to V_B
    w_3 = p_b * (v_b - v_a)            # 2000 J = +2.00 kJ
    q_3 = du + w_3                     # 3500 J = +3.50 kJ

    assert abs((q_1 - w_1) - du) < 1e-9
    assert abs((q_2 - w_2) - du) < 1e-9
    assert abs((q_3 - w_3) - du) < 1e-9
    assert abs(w_1 - 4000.0) < 1e-9 and abs(w_2 - 3000.0) < 1e-9 and abs(w_3 - 2000.0) < 1e-9
    assert abs(q_1 - 5500.0) < 1e-9 and abs(q_2 - 4500.0) < 1e-9 and abs(q_3 - 3500.0) < 1e-9

    # 3. Microstate dimensionality for 1 mol of point particles: 6 * N_A
    dim_1mol = 6.0 * n_a
    assert 3.61e24 < dim_1mol < 3.62e24

    # 4. 1 kWh electricity dissipated into 25 C (298.15 K) room air
    e_kwh = 3.6e6
    ds_room = e_kwh / 298.15
    assert 12070.0 < ds_room < 12080.0  # ~12,074.5 J/K


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker_end=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    m_attr = f' marker-end="url(#{marker_end})"' if marker_end else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}"{d_attr}{m_attr}/>'
    )


def build_fig1_mechanical_to_joule():
    """Fig 1: Apparent loss of mechanical energy vs Joule's bridge to internal energy U."""
    el = []
    el.extend(
        header(
            "刹车停下后机械能去哪了？从“热质假说”崩塌到热力学第一定律大一统",
            "纯力学只盯住宏观动能与势能；一旦算上 10²⁴ 个分子的微观热运动内能 U，宇宙总账一焦耳都没丢",
        )
    )

    # Panel 1: Pure mechanics (Left)
    el.append(card(22, 68, 224, 368, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 95, "纯力学账本：遇摩擦就“破产”", size=13, color=INK, weight="700"))

    # Ideal保守力 vs 真实刹车 subcards
    el.append(card(34, 110, 200, 132, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(46, 130, "理想无摩擦（仅保守力做功）", size=12, color=BLUE, weight="700"))
    # Mini U-track with ball
    el.append('<path d="M52,152 Q134,226 216,152" fill="none" stroke="#1d6fa5" stroke-width="2.2"/>')
    el.append(f'<circle cx="66" cy="163" r="7" fill="{BLUE}"/>')
    el.append(f'<circle cx="134" cy="189" r="7" fill="{GREEN}"/>')
    el.append(_line(75, 166, 118, 184, color=BLUE, sw=1.5, marker_end="arr-blue"))
    el.append(txt(134, 212, "势能 Ep ⇄ 动能 Ek 互换", size=11.5, color=BODY, anchor="middle", weight="600"))
    el.append(txt(134, 231, "E机 = Ek + Ep = 常数（守恒）", size=11.5, color=BLUE, anchor="middle", weight="700"))

    el.append(card(34, 254, 200, 168, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(46, 274, "真实世界（踩刹车 / 橡皮泥落地）", size=12, color=ORANGE, weight="700"))
    # Sliding block stopping on rough floor
    el.append(_line(46, 326, 220, 326, color=SLATE, sw=2))
    el.append(f'<rect x="52" y="302" width="38" height="24" rx="4" fill="{BLUE}" opacity="0.85"/>')
    el.append(txt(71, 318, "v₀", size=11.5, color="#ffffff", anchor="middle", weight="700"))
    el.append(_line(96, 314, 144, 314, color=ORANGE, sw=1.8, dash="4,3", marker_end="arr-orange"))
    el.append(f'<rect x="154" y="302" width="38" height="24" rx="4" fill="{SLATE}"/>')
    el.append(txt(173, 318, "v=0", size=11.5, color="#ffffff", anchor="middle", weight="700"))
    # Friction sparks/heat waves
    el.append('<path d="M112,300 Q116,291 112,283 M126,300 Q130,291 126,283 M140,300 Q144,291 140,283" fill="none" stroke="#c25014" stroke-width="1.6"/>')
    el.append(txt(134, 350, "末态宏观 Ek = 0，Ep = 0", size=11.5, color=INK, anchor="middle", weight="600"))
    el.append(txt(134, 370, "ΔE机 = W非保守 < 0", size=12, color=RED, anchor="middle", weight="700"))
    el.append(txt(134, 391, "表面悬案：宏观机械能“蒸发”了！", size=11.5, color=ORANGE, anchor="middle"))
    el.append(txt(134, 410, "旧物理曾误以为热是守恒流体“热质”", size=11, color=MUTED, anchor="middle"))

    # Arrow Panel 1 -> Panel 2
    el.append(_line(248, 250, 266, 250, color=ORANGE, sw=2, marker_end="arr-orange"))

    # Panel 2: Historical Bridge & Exact Exchange Rate (Middle)
    el.append(card(270, 68, 224, 368, fill=CARD_BG))
    el.append(step_badge(290, 90, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(308, 95, "三步破案：锁定“功—热汇率”", size=13, color=INK, weight="700"))

    # Sub-step A: Rumford 1798
    el.append(card(282, 110, 200, 74, rx=7, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(292, 129, "① 1798 伦福德钝钻头钻炮筒", size=12, color=INK, weight="700"))
    el.append(txt(292, 148, "无碎屑仍 2.5 小时烧开整箱冰水：", size=11.5, color=BODY))
    el.append(txt(292, 167, "热不是挤出的“热质”，而是运动！", size=11.5, color=ORANGE, weight="600"))

    # Sub-step B: Mayer 1840-1842
    el.append(card(282, 194, 200, 78, rx=7, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(292, 213, "② 1840–1842 迈尔热带放血顿悟", size=12, color=INK, weight="700"))
    el.append(txt(292, 232, "爪哇水手静脉血鲜红→少耗氧产热；", size=11.5, color=BODY))
    el.append(txt(292, 251, "由气体 Cp − Cv = R 首算热功当量", size=11.5, color=BLUE, weight="600"))

    # Sub-step C: Joule 1845-1850 Paddle Wheel
    el.append(card(282, 282, 200, 140, rx=7, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(292, 302, "③ 1850 焦耳重锤叶轮精确测汇率", size=12, color=GREEN, weight="700"))
    # Mini schematic of paddle-wheel & falling weight
    el.append(f'<rect x="296" y="318" width="56" height="46" rx="4" fill="#ffffff" stroke="{BLUE}" stroke-width="1.4"/>')
    el.append(_line(324, 312, 324, 358, color=SLATE, sw=1.8))
    el.append(_line(310, 334, 338, 334, color=ORANGE, sw=2.2))
    el.append(_line(310, 348, 338, 348, color=ORANGE, sw=2.2))
    el.append(_line(324, 312, 368, 312, color=SLATE, sw=1.3))
    el.append(_line(368, 312, 368, 344, color=SLATE, sw=1.3))
    el.append(f'<rect x="360" y="344" width="16" height="18" rx="2" fill="{ORANGE}"/>')
    el.append(txt(380, 332, "1 cal = 4.184 J", size=12, color=GREEN, weight="700"))
    el.append(txt(380, 352, "1 kg 下落 427 m", size=11, color=BODY))
    el.append(txt(380, 370, "升温 1 kg 水 1 K", size=11, color=ORANGE, weight="700"))
    el.append(txt(382, 405, "机械功与热只是同一种货币！", size=11.5, color=GREEN, anchor="middle", weight="700"))

    # Arrow Panel 2 -> Panel 3
    el.append(_line(496, 250, 514, 250, color=GREEN, sw=2, marker_end="arr-green"))

    # Panel 3: Unified First Law (Right)
    el.append(card(518, 68, 220, 368, fill=CARD_BG))
    el.append(step_badge(538, 90, 3, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(556, 95, "热力学第一定律：宇宙总账", size=13, color=INK, weight="700"))

    # Particle box showing microscopic random kinetic + intermolecular potential energy
    el.append(card(530, 110, 196, 128, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(628, 130, "新状态参量：内能 U（微观总账）", size=12, color=PURPLE, anchor="middle", weight="700"))
    pts = [(554, 158, 12, -8), (592, 174, -13, -9), (632, 154, 11, 10), (674, 170, -12, 8), (700, 152, -10, -10), (572, 192, 14, 5), (652, 192, -11, -7)]
    for px, py, dx, dy in pts:
        el.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="{PURPLE}"/>')
        el.append(_line(px, py, px + dx, py + dy, color=PURPLE, sw=1.4))
    el.append(txt(628, 216, "U = Σ(分子平动/转动/振动动能", size=11.5, color=BODY, anchor="middle"))
    el.append(txt(628, 232, "    + 分子间相互作用势能)", size=11.5, color=BODY, anchor="middle"))

    # Unified Ledger Box
    el.append(card(530, 250, 196, 172, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(628, 272, "静止闭系第一定律：", size=12, color=INK, anchor="middle", weight="700"))
    el.append(txt(628, 296, "ΔU = Q − W对外", size=15, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(540, 320, "• 吸热 Q > 0：热传递存入能量", size=11.5, color=BODY))
    el.append(txt(540, 340, "• 对外做功 W对外 > 0：对外支取", size=11.5, color=BODY))
    el.append(txt(540, 360, "• 总账：Δ(Ek+Ep+U) = Q − W", size=11.5, color=INK, weight="600"))
    el.append(_line(542, 374, 714, 374, color=BLUE_LINE, sw=1))
    el.append(txt(628, 393, "深层根源：1918 诺特定理", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(628, 411, "物理定律的时间平移对称性 ⇒ 能量守恒", size=11, color=MUTED, anchor="middle"))

    # Bottom summary banner
    el.append(card(22, 448, 716, 46, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(
        txt(
            380,
            476,
            "一句话贯通：力学守恒只看“整块物体齐步走”（1 个宏观自由度），热力学把“分子乱撞的热运动”并表入账，能量分毫未损！",
            size=12,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        508,
        "力学机械能损耗与热力学第一定律能量守恒统一图解",
        "展示无摩擦单摆中机械能守恒、摩擦刹车中宏观机械能看似消失，经伦福德钻炮、迈尔放血观察与焦耳叶轮实验（1 cal = 4.184 J）统一为热力学第一定律 ΔU = Q - W对外。",
        el,
    )
    write_svg(SUBDIR, "mechanical-loss-to-joule-bridge.svg", svg)


def build_fig2_pv_paths_anim():
    """Fig 2: Animated P-V diagram showing 3 paths between A and B (1 mol monatomic ideal gas)."""
    # Exact coordinate mapping for P-V plot:
    # V axis: 5 L to 35 L -> x from 84 to 424 (10 L = 140.7, 30 L = 367.3; let's make exact integer grid!)
    # Let V in [5, 35] map linearly with 11 px per L: V=5 -> x=85, V=10 -> x=140, V=20 -> x=250, V=30 -> x=360, V=35 -> x=415!
    # Let P in [0, 2.5] bar map linearly with 110 px per bar: P=0 -> y=395, P=1.0 -> y=285, P=2.0 -> y=175, P=2.5 -> y=120!
    x_a, y_a = 140.0, 175.0   # V_A = 10 L, P_A = 2.0 bar
    x_b, y_b = 360.0, 285.0   # V_B = 30 L, P_B = 1.0 bar
    x_c1, y_c1 = 360.0, 175.0  # Upper corner (30 L, 2.0 bar) -> length = 220 + 110 = 330
    x_c3, y_c3 = 140.0, 285.0  # Lower corner (10 L, 1.0 bar) -> length = 110 + 220 = 330
    len_diag = math.hypot(x_b - x_a, y_b - y_a)  # sqrt(220^2 + 110^2) = 245.97

    extra_css = f"""
  .pv-p1 {{
    stroke-dasharray: 340;
    stroke-dashoffset: 340;
    animation: drawP1 1.7s ease-out 0.2s forwards;
  }}
  .pv-p2 {{
    stroke-dasharray: 260;
    stroke-dashoffset: 260;
    animation: drawP2 1.5s ease-out 1.4s forwards;
  }}
  .pv-p3 {{
    stroke-dasharray: 340;
    stroke-dashoffset: 340;
    animation: drawP3 1.7s ease-out 2.5s forwards;
  }}
  .pv-loop {{
    opacity: 0;
    animation: showLoop 0.9s ease-out 3.8s forwards;
  }}
  @keyframes drawP1 {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes drawP2 {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes drawP3 {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes showLoop {{ to {{ opacity: 1; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .pv-p1, .pv-p2, .pv-p3 {{
      animation: none !important;
      stroke-dashoffset: 0 !important;
    }}
    .pv-loop {{
      animation: none !important;
      opacity: 1 !important;
    }}
  }}
"""

    el = []
    el.extend(
        header(
            "状态参量 vs 过程量：终点海拔（ΔU）一模一样，三条路做功与吸热全不同！",
            "以 1 mol 单原子理想气体从初态 A(2.0 bar, 10 L) 到末态 B(1.0 bar, 30 L) 为精确算例（面积 ∫P dV 即对外做功）",
        )
    )

    # Left Card: P-V coordinate plot
    el.append(card(22, 68, 426, 392, fill=CARD_BG))
    el.append(txt(40, 94, "P–V 状态图：点代表“平衡态”，线代表“准静态过程”", size=13, color=INK, weight="700"))

    # Shaded under-path-3 base area + loop rectangle area
    el.append(f'<rect x="{x_a:.1f}" y="{y_b:.1f}" width="{x_b - x_a:.1f}" height="{395 - y_b:.1f}" fill="{GREEN_SOFT}" opacity="0.75"/>')
    el.append(
        f'<rect class="pv-loop" x="{x_a:.1f}" y="{y_a:.1f}" width="{x_b - x_a:.1f}" height="{y_b - y_a:.1f}" '
        f'fill="{ORANGE_SOFT}" opacity="0.85"/>'
    )

    # Grid lines
    for v_val, gx in [(10, 140), (20, 250), (30, 360)]:
        el.append(_line(gx, 120, gx, 395, color=BORDER, sw=1, dash="3,3"))
        el.append(txt(gx, 414, f"{v_val} L", size=11.5, color=SLATE, anchor="middle"))
    for p_val, gy in [(1.0, 285), (2.0, 175)]:
        el.append(_line(85, gy, 418, gy, color=BORDER, sw=1, dash="3,3"))
        el.append(txt(77, gy + 4, f"{p_val:.1f}", size=11.5, color=SLATE, anchor="end"))

    # Axes
    el.append(_line(85, 395, 426, 395, color=INK, sw=1.8, marker_end="arr-muted"))
    el.append(_line(85, 395, 85, 114, color=INK, sw=1.8, marker_end="arr-muted"))
    el.append(txt(85, 107, "压强 P (bar)", size=11.5, color=INK, anchor="middle", weight="600"))
    el.append(txt(394, 434, "体积 V (L)", size=11.5, color=INK, anchor="middle", weight="600"))
    el.append(txt(77, 399, "0", size=11.5, color=SLATE, anchor="end"))

    # Static faint guide tracks so static / pre-animation state is 100% readable
    el.append(f'<polyline points="{x_a},{y_a} {x_c1},{y_c1} {x_b},{y_b}" fill="none" stroke="{ORANGE}" stroke-width="1.2" stroke-opacity="0.28"/>')
    el.append(_line(x_a, y_a, x_b, y_b, color=BLUE, sw=1.2, dash="5,4"))
    el.append(f'<polyline points="{x_a},{y_a} {x_c3},{y_c3} {x_b},{y_b}" fill="none" stroke="{GREEN}" stroke-width="1.2" stroke-opacity="0.28"/>')

    # Animated paths with distinct line patterns + labels
    # Path 1: solid thick orange
    el.append(
        f'<polyline class="pv-p1" points="{x_a},{y_a} {x_c1},{y_c1} {x_b},{y_b}" '
        f'fill="none" stroke="{ORANGE}" stroke-width="3.2" stroke-linejoin="round"/>'
    )
    # Path 2: dashed blue
    el.append(
        f'<line class="pv-p2" x1="{x_a}" y1="{y_a}" x2="{x_b}" y2="{y_b}" '
        f'stroke="{BLUE}" stroke-width="2.8"/>'
    )
    # Path 3: green polyline
    el.append(
        f'<polyline class="pv-p3" points="{x_a},{y_a} {x_c3},{y_c3} {x_b},{y_b}" '
        f'fill="none" stroke="{GREEN}" stroke-width="3.0" stroke-linejoin="round"/>'
    )

    # Direction arrows on paths
    el.append(_line(235, y_a, 265, y_a, color=ORANGE, sw=2.2, marker_end="arr-orange"))
    el.append(_line(235, 222.5, 265, 237.5, color=BLUE, sw=2.2, marker_end="arr-blue"))
    el.append(_line(235, y_b, 265, y_b, color=GREEN, sw=2.2, marker_end="arr-green"))

    # Path callout labels with white halo (carefully non-overlapping!)
    el.append(txt(285, 162, "路线 ① 先等压膨胀再等容", size=11.5, color=ORANGE, anchor="middle", weight="700", halo=True))
    el.append(txt(234, 214, "路线 ② 直线降压膨胀", size=11.5, color=BLUE, anchor="start", weight="700", halo=True))
    el.append(txt(232, 306, "路线 ③ 先等容再等压膨胀", size=11.5, color=GREEN, anchor="middle", weight="700", halo=True))
    el.append(txt(250, 354, "路线 ③ 下方面积 W₃ = 2.00 kJ", size=11.5, color=GREEN, anchor="middle", weight="600", halo=True))

    # Endpoints A and B
    el.append(f'<circle cx="{x_a}" cy="{y_a}" r="6.5" fill="{INK}" stroke="#ffffff" stroke-width="2"/>')
    el.append(f'<circle cx="{x_b}" cy="{y_b}" r="6.5" fill="{INK}" stroke="#ffffff" stroke-width="2"/>')
    el.append(txt(94, 145, "初态 A (Uₐ=3.00 kJ)", size=12, color=INK, anchor="start", weight="700", halo=True))
    el.append(txt(420, 272, "末态 B (Uᵦ=4.50 kJ)", size=12, color=INK, anchor="end", weight="700", halo=True))

    # Bottom note inside left card
    el.append(txt(235, 451, "注：若沿 ① 去、沿 ③ 回构成闭合循环，∮dU = 0，橙框净功 = 2.00 kJ！", size=11, color=ORANGE, anchor="middle", weight="600"))

    # Right Card: Exact Ledger Comparison Table + Core Math Rule
    el.append(card(462, 68, 276, 392, fill=CARD_BG))
    el.append(txt(478, 94, "三本对账单：谁看路径？谁只看终点？", size=13, color=INK, weight="700"))

    # Route 1 box
    el.append(card(474, 108, 252, 64, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(486, 127, "路线 ①（上折线）", size=12, color=ORANGE, weight="700"))
    el.append(txt(486, 146, "对外功 W₁ = +4.00 kJ  |  吸热 Q₁ = +5.50 kJ", size=11.5, color=BODY))
    el.append(txt(486, 164, "内能差 ΔU = Q₁ − W₁ = +1.50 kJ", size=11.5, color=INK, weight="700"))

    # Route 2 box
    el.append(card(474, 180, 252, 64, rx=7, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(486, 199, "路线 ②（中斜线）", size=12, color=BLUE, weight="700"))
    el.append(txt(486, 218, "对外功 W₂ = +3.00 kJ  |  吸热 Q₂ = +4.50 kJ", size=11.5, color=BODY))
    el.append(txt(486, 236, "内能差 ΔU = Q₂ − W₂ = +1.50 kJ", size=11.5, color=INK, weight="700"))

    # Route 3 box
    el.append(card(474, 252, 252, 64, rx=7, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(486, 271, "路线 ③（下折线）", size=12, color=GREEN, weight="700"))
    el.append(txt(486, 290, "对外功 W₃ = +2.00 kJ  |  吸热 Q₃ = +3.50 kJ", size=11.5, color=BODY))
    el.append(txt(486, 308, "内能差 ΔU = Q₃ − W₃ = +1.50 kJ", size=11.5, color=INK, weight="700"))

    # Mathematical distinction box: dU vs delta Q, delta W
    el.append(card(474, 326, 252, 122, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(600, 347, "微积分符号里的“防坑警报”", size=12.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(486, 369, "• 态函数用 dU：全微分，∮dU = 0", size=11.5, color=INK, weight="600"))
    el.append(txt(496, 387, "如同银行余额，只取决于当前状态", size=11, color=MUTED))
    el.append(txt(486, 408, "• 过程量用 δQ、δW：不完全微分", size=11.5, color=RED, weight="600"))
    el.append(txt(496, 426, "如同刷卡流水，严禁写“含有多少热量”！", size=11, color=BODY))

    # Footer
    el.append(card(22, 472, 716, 46, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(
        txt(
            380,
            500,
            "核心铁律：W₁ ≠ W₂ ≠ W₃，Q₁ ≠ Q₂ ≠ Q₃（过程量记住历史）；但 Q − W 永远等于 Uᵦ − Uₐ = +1.50 kJ（状态量毫无历史记忆）！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        532,
        "P-V 图上三条路径的做功、吸热与内能变化对比动画",
        "精确计算 1 mol 单原子理想气体从 A(2.0 bar, 10 L) 到 B(1.0 bar, 30 L) 沿三条不同路径的功 W(4.00/3.00/2.00 kJ) 与热 Q(5.50/4.50/3.50 kJ)，展示内能增量恒为 +1.50 kJ。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "pv-paths-state-vs-process-anim.svg", svg)


def build_fig3_micro_to_macro_funnel():
    """Fig 3: Dimensionality reduction from 6N_A mechanical coordinates to 2 thermodynamic state variables."""
    el = []
    el.extend(
        header(
            "从 3.6×10²⁴ 个力学坐标到 2 个热力学表盘：物理学最震撼的“史诗级降维”",
            "为什么力学里描述 1 mol 气体会让超级计算机崩溃，而平衡态热力学只看两块仪表就能锁死全局？",
        )
    )

    # Left Card: Classical Mechanics Phase Space
    el.append(card(22, 68, 232, 358, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(60, 95, "力学微观态：拉普拉斯妖的噩梦", size=12.5, color=INK, weight="700"))

    el.append(card(34, 112, 208, 134, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(138, 132, "1 mol 气体 = 6.022×10²³ 个分子", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    # Draw several particles with (r_i, p_i) vectors
    m_pts = [(64, 166, 18, -10, "r₁,p₁"), (136, 162, -16, 12, "r₂,p₂"), (194, 174, -14, -12, "rᵢ,pᵢ"), (96, 204, 16, 8, "…"), (168, 208, -15, 6, "rₙ,pₙ")]
    for px, py, vx, vy, lb in m_pts:
        el.append(f'<circle cx="{px}" cy="{py}" r="5" fill="{ORANGE}"/>')
        el.append(_line(px, py, px + vx, py + vy, color=INK, sw=1.5))
        el.append(txt(px, py + 18, lb, size=11, color=BODY, anchor="middle"))

    el.append(card(34, 258, 208, 154, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(46, 280, "每个质点需 6 个力学状态量：", size=11.5, color=INK, weight="600"))
    el.append(txt(46, 300, "位置 (xᵢ, yᵢ, zᵢ) + 动量 (pₓᵢ, pᵧᵢ, p₂ᵢ)", size=11.5, color=BODY))
    el.append(txt(138, 328, "总维数 = 6 Nₐ ≈ 3.61×10²⁴", size=13, color=RED, anchor="middle", weight="700"))
    el.append(txt(46, 352, "• 哪怕每秒抄写 1 万亿个数字，", size=11, color=MUTED))
    el.append(txt(46, 370, "  写完一瞬间的状态也要 11.4 万年！", size=11, color=MUTED))
    el.append(txt(46, 392, "• 微观可逆，且受初值混沌高度敏感", size=11, color=BODY))

    # Middle Card: Statistical Bridge / Funnel
    el.append(card(272, 68, 216, 358, fill=CARD_BG))
    el.append(step_badge(292, 90, 2, fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(310, 95, "统计物理漏斗：碰撞抹平细节", size=12.5, color=INK, weight="700"))

    # Funnel trapezoid polygon
    el.append(
        f'<polygon points="288,118 472,118 434,242 326,242" '
        f'fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.5"/>'
    )
    el.append(txt(380, 144, "每秒 ~10⁹ 次/分子激烈碰撞", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(380, 166, "进入“热动平衡态”后：", size=11.5, color=INK, anchor="middle", weight="600"))
    el.append(txt(380, 190, "① 平动动能均值 → 温度 T", size=11.5, color=BODY, anchor="middle"))
    el.append(txt(380, 208, "   ⟨ε平⟩ = (3/2) kB T", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(380, 230, "② 器壁冲量密度 → 压强 P", size=11.5, color=BODY, anchor="middle"))

    el.append(_line(380, 244, 380, 266, color=PURPLE, sw=2, marker_end="arr-muted"))

    el.append(card(284, 272, 192, 140, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(380, 294, "状态方程再砍掉 1 个自由度！", size=12, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(380, 320, "P V = n R T", size=15, color=INK, anchor="middle", weight="700"))
    el.append(txt(380, 344, "吉布斯相律：F = C − Φ + 2", size=11.5, color=BODY, anchor="middle", weight="600"))
    el.append(txt(380, 366, "纯单相闭系（C=1, Φ=1）：", size=11, color=MUTED, anchor="middle"))
    el.append(txt(380, 388, "独立强度参量仅 F = 2 个！", size=12, color=GREEN, anchor="middle", weight="700"))

    # Right Card: Equilibrium Macrostate Dials
    el.append(card(506, 68, 232, 358, fill=CARD_BG))
    el.append(step_badge(526, 90, 3, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(544, 95, "热力学宏观态：2 个表盘定乾坤", size=12.5, color=INK, weight="700"))

    # Two dials (T and P)
    el.append(card(518, 112, 208, 120, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    # Dial 1: T
    el.append(f'<circle cx="572" cy="164" r="30" fill="#ffffff" stroke="{ORANGE}" stroke-width="2"/>')
    el.append(_line(572, 164, 590, 146, color=ORANGE, sw=2.4))
    el.append(txt(572, 184, "T", size=13, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(572, 214, "温度计", size=11.5, color=INK, anchor="middle", weight="600"))
    # Dial 2: P
    el.append(f'<circle cx="672" cy="164" r="30" fill="#ffffff" stroke="{BLUE}" stroke-width="2"/>')
    el.append(_line(672, 164, 692, 152, color=BLUE, sw=2.4))
    el.append(txt(672, 184, "P", size=13, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(672, 214, "压力表", size=11.5, color=INK, anchor="middle", weight="600"))

    el.append(_line(622, 234, 622, 254, color=GREEN, sw=2, marker_end="arr-green"))

    el.append(card(518, 258, 208, 154, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(622, 280, "一旦固定 n 并读出 (T, P)：", size=12, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(530, 304, "• 体积 V = V(T, P) 自动锁死", size=11.5, color=BODY))
    el.append(txt(530, 325, "• 内能 U = U(T, P) 自动锁死", size=11.5, color=BODY))
    el.append(txt(530, 346, "• 熵 S、焓 H、自由能 G 全锁死", size=11.5, color=BODY))
    el.append(_line(530, 362, 714, 362, color=HAIRLINE, sw=1))
    el.append(txt(622, 382, "适用边界：必须处于热平衡态！", size=11.5, color=RED, anchor="middle", weight="700"))
    el.append(txt(622, 400, "爆炸湍流瞬间不能用单个 P、T 概括", size=11, color=MUTED, anchor="middle"))

    # Bottom banner
    el.append(card(22, 438, 716, 46, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(
        txt(
            380,
            466,
            "对比精髓：力学追踪“每一棵树的枝叶摇晃”（6N 维相空间）；热力学测量“整片森林的海拔与气温”（2～3 维平衡态流形）。",
            size=12,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        498,
        "力学微观相空间与平衡态热力学状态参量的降维对比图",
        "展示 1 mol 气体的 3.61×10²⁴ 个经典力学位置动量坐标如何经统计平均与理想气体状态方程 PV=nRT 降维为仅需 2 个独立热力学状态参量。",
        el,
    )
    write_svg(SUBDIR, "microstate-6n-to-macrostate-funnel.svg", svg)


def build_fig4_extensive_intensive_potentials():
    """Fig 4: Cut-in-half tea test (Intensive vs Extensive) + 4 Thermodynamic Potentials."""
    el = []
    el.extend(
        header(
            "把一杯 80℃ 热茶一刀切两半：秒懂“强度量 vs 广延量”与四大能量家族",
            "强度量管“往哪流”（推动力），广延量管“装多少”（容量）；两者成对相乘恰好就是功与热！",
        )
    )

    # Top Section: The Partition Test
    el.append(card(22, 68, 716, 198, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 95, "思想实验：在热平衡的 400 mL 热茶正中央，轻轻插进一块薄隔板", size=13, color=INK, weight="700"))

    # Visual cup split in half on left of top card
    el.append(card(36, 110, 212, 142, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(142, 130, "原系统：400 mL，80℃，1 atm", size=11.5, color=INK, anchor="middle", weight="700"))
    # Two half-cups separated by dashed red partition
    el.append(f'<rect x="58" y="144" width="76" height="72" rx="6" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(f'<rect x="150" y="144" width="76" height="72" rx="6" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(_line(142, 138, 142, 224, color=RED, sw=2, dash="5,3"))
    el.append(txt(96, 174, "左半杯", size=12, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(96, 194, "200 mL", size=11.5, color=BODY, anchor="middle"))
    el.append(txt(96, 210, "80℃!", size=11.5, color=RED, anchor="middle", weight="700"))
    el.append(txt(188, 174, "右半杯", size=12, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(188, 194, "200 mL", size=11.5, color=BODY, anchor="middle"))
    el.append(txt(188, 210, "80℃!", size=11.5, color=RED, anchor="middle", weight="700"))
    el.append(txt(142, 242, "切半后温度绝不会变成 40℃！", size=11, color=RED, anchor="middle", weight="600"))

    # Intensive box (Middle)
    el.append(card(262, 110, 224, 142, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(374, 131, "强度量（Intensive：不随大小变）", size=12, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(274, 154, "• 温度 T（80℃ 不变 → 管热量流向）", size=11.5, color=BODY))
    el.append(txt(274, 175, "• 压强 P（1 atm 不变 → 管边界膨胀）", size=11.5, color=BODY))
    el.append(txt(274, 196, "• 化学势 μ、密度 ρ、比热容 c", size=11.5, color=BODY))
    el.append(txt(374, 222, "本质：决定平衡与否的“水位高度”", size=11.5, color=ORANGE, anchor="middle", weight="600"))
    el.append(txt(374, 241, "不可直接相加（80℃+80℃ ≠ 160℃）", size=11, color=MUTED, anchor="middle"))

    # Extensive box (Right)
    el.append(card(500, 110, 224, 142, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(612, 131, "广延量（Extensive：随份额减半）", size=12, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(512, 154, "• 体积 V、质量 m、摩尔数 n（全减半）", size=11.5, color=BODY))
    el.append(txt(512, 175, "• 内能 U、焓 H、自由能 F、G（减半）", size=11.5, color=BODY))
    el.append(txt(512, 196, "• 熵 S（无序度规模也严格减半）", size=11.5, color=BODY))
    el.append(txt(612, 222, "本质：具有严格可加性的“蓄水容量”", size=11.5, color=BLUE, anchor="middle", weight="600"))
    el.append(txt(612, 241, "广延量 ÷ 广延量 = 强度量（如 ρ=m/V）", size=11, color=MUTED, anchor="middle"))

    # Bottom Section: Conjugate Pairs & Four Thermodynamic Potentials
    el.append(card(22, 278, 716, 232, fill=CARD_BG))
    el.append(step_badge(42, 300, 2, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(60, 305, "共轭配对铁律 dU = T dS − P dV + μ dN，以及为什么要造出“四大能量态函数”？", size=13, color=INK, weight="700"))

    # 4 cards for U, H, F, G across bottom
    potentials = [
        (
            36,
            "内能 U(S, V)",
            "系统微粒真身总家底",
            "dU = T dS − P dV",
            "主场：密封刚性钢罐（恒容 V）",
            "等容吸热 Qv = ΔU",
            BLUE,
            BLUE_SOFT,
        ),
        (
            208,
            "焓 H = U + PV",
            "自带“挤开大气过路费”",
            "dH = T dS + V dP",
            "主场：敞口烧杯/锅炉（恒压 P）",
            "等压反应热 Qp = ΔH",
            ORANGE,
            ORANGE_SOFT,
        ),
        (
            380,
            "亥姆霍兹 F = U − TS",
            "扣掉恒温必交的“热税 TS”",
            "dF = −S dT − P dV",
            "主场：恒温恒容容器（恒 T, V）",
            "最大总功 Wmax = −ΔF",
            PURPLE,
            PURPLE_SOFT,
        ),
        (
            552,
            "吉布斯 G = H − TS",
            "化工与生命细胞的终极裁判",
            "dG = −S dT + V dP",
            "主场：室温常压（恒 T, P）",
            "ΔG<0 自发；电功≤−ΔG",
            GREEN,
            GREEN_SOFT,
        ),
    ]
    for px, name, tag, diff_eq, scene, punch, fg, bg in potentials:
        el.append(card(px, 320, 162, 176, rx=8, fill=bg, stroke=fg))
        el.append(txt(px + 81, 342, name, size=12.5, color=fg, anchor="middle", weight="700"))
        el.append(txt(px + 81, 362, tag, size=11, color=INK, anchor="middle", weight="600"))
        el.append(_line(px + 12, 372, px + 150, 372, color=fg, sw=0.9))
        el.append(txt(px + 81, 394, diff_eq, size=11.5, color=INK, anchor="middle", weight="700"))
        el.append(txt(px + 81, 422, scene, size=11, color=BODY, anchor="middle"))
        el.append(card(px + 10, 440, 142, 44, rx=6, fill="#ffffff", stroke=fg))
        el.append(txt(px + 81, 467, punch, size=11, color=fg, anchor="middle", weight="700"))

    svg = figure(
        524,
        "热力学强度量与广延量切半测试及四大热力学势对比图",
        "上半图用 400 mL 80℃ 热茶一分为二说明强度量(T,P,μ)不变而广延量(V,m,U,S)减半；下半图展示通过勒让德变换构造的内能 U、焓 H、亥姆霍兹自由能 F 与吉布斯自由能 G 的各自适用场景。",
        el,
    )
    write_svg(SUBDIR, "extensive-intensive-and-potentials.svg", svg)


def build_fig5_entropy_and_energy_quality():
    """Fig 5: Clausius integrating factor 1/T -> dS, and why conserved energy still degrades!"""
    el = []
    el.extend(
        header(
            "克劳修斯的神来之笔（dS = δQrev/T）与终极反问：能量守恒，为啥还要省电？",
            "第一定律管“总金额一分不少”，第二定律与状态参量“熵 S”管“整钞一旦花成散碎硬币就捡不回来了”",
        )
    )

    # Left Card: Integrating factor 1/T turns path quantity delta Q into state function S!
    el.append(card(22, 68, 350, 374, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(60, 95, "1865 克劳修斯：除以 T，过程量变态函数！", size=12.5, color=INK, weight="700"))

    el.append(card(34, 112, 326, 132, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(197, 133, "同样输入 δQ = +1,000 J 热量，冲击力一样吗？", size=11.5, color=PURPLE, anchor="middle", weight="700"))

    # Hot furnace vs Cold ice room
    el.append(card(46, 146, 144, 86, rx=6, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(118, 166, "1,000 K 炼钢炉", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(118, 187, "像在嘈杂菜市场喊一声", size=11, color=BODY, anchor="middle"))
    el.append(txt(118, 212, "ΔS = 1000/1000 = +1 J/K", size=11, color=ORANGE, anchor="middle", weight="700"))

    el.append(card(204, 146, 144, 86, rx=6, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(276, 166, "250 K 寂静冰窖", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(276, 187, "像在安静图书馆喊一声", size=11, color=BODY, anchor="middle"))
    el.append(txt(276, 212, "ΔS = 1000/250 = +4 J/K", size=11, color=BLUE, anchor="middle", weight="700"))

    el.append(card(34, 256, 326, 174, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(197, 280, "数学奇迹：积分因子 1/T 消除路径依赖", size=12, color=INK, anchor="middle", weight="700"))
    el.append(txt(197, 308, "∮ δQrev ≠ 0   ──除以 T──▶   ∮ (δQrev / T) = 0", size=12, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(48, 336, "• 定义新状态参量“熵”：dS = δQrev / T", size=11.5, color=INK, weight="600"))
    el.append(txt(48, 358, "• 微观真身（玻尔兹曼墓碑公式）：S = kB ln Ω", size=11.5, color=BLUE, weight="700"))
    el.append(txt(48, 380, "  Ω 是同一宏观态对应的微观排列方式总数", size=11, color=BODY))
    el.append(txt(48, 404, "• 不可逆自发过程铁律：ΔS总 = ΔS系统 + ΔS环境 > 0", size=11.5, color=RED, weight="700"))

    # Right Card: 1 kWh Electricity -> Room Heat (Quantity conserved, Quality destroyed!)
    el.append(card(388, 68, 350, 374, fill=CARD_BG))
    el.append(step_badge(408, 90, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(426, 95, "1 度电开风扇吹一晚：数量 100% 在，品质归零", size=12.5, color=INK, weight="700"))

    # High-grade input box
    el.append(card(400, 112, 326, 86, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(414, 134, "输入：1 kWh 电能 = 3,600,000 J（高品位自由能）", size=11.5, color=GREEN, weight="700"))
    el.append(txt(414, 156, "• 电子定向驱动电机做功，携带的熵增 ΔS电 = 0 J/K", size=11.5, color=BODY))
    el.append(txt(414, 178, "• 可用能（Exergy）占比 = 100%，可提重物 367 吨升 1 米！", size=11, color=GREEN, weight="600"))

    el.append(_line(563, 200, 563, 224, color=ORANGE, sw=2.2, marker_end="arr-orange"))
    el.append(txt(575, 216, "叶片搅动空气粘滞摩擦生热", size=11, color=ORANGE, weight="600"))

    # Low-grade output box
    el.append(card(400, 224, 326, 98, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(412, 245, "输出：25℃(298.15 K) 空气升温 → ΔU = +3.60 MJ", size=11.5, color=ORANGE, weight="700"))
    el.append(txt(412, 266, "• 第一定律：总能量 3.60 MJ（一焦耳都没丢！）", size=11.5, color=INK, weight="600"))
    el.append(txt(412, 287, "• 第二定律：ΔS = 3.6×10⁶/298.15 = +12,074 J/K", size=11.5, color=RED, weight="700"))
    el.append(txt(412, 308, "• 无温差(TH=TC) ⇒ 卡诺效率 η=0，可用功 = 0 J", size=11, color=BODY))

    # Counterexample box: why warm water never splits into ice + boiling
    el.append(card(400, 330, 326, 102, rx=8, fill=RED_SOFT, stroke=RED))
    el.append(txt(563, 350, "反例：为何温水不会自发半边结冰、半边沸腾？", size=11.5, color=RED, anchor="middle", weight="700"))
    el.append(txt(412, 371, "• 左半降温放热给右半升温：ΔU=0 不违背第一定律", size=11, color=BODY))
    el.append(txt(412, 392, "• 但高温吸热 ΔS正 < 低温放热 |ΔS负|，导致", size=11, color=INK, weight="600"))
    el.append(txt(412, 412, "  总熵变 ΔS总 < 0，被第二定律一票否决！", size=11, color=RED, weight="700"))

    # Bottom banner
    el.append(card(22, 454, 716, 44, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(
        txt(
            380,
            481,
            "克劳修斯 1865 名言：“宇宙的能量是恒定的（第一定律）；宇宙的熵趋于极大值（第二定律）。”省电省的是低熵可用能！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        512,
        "克劳修斯熵状态参量诞生与能量守恒下的品质贬值图解",
        "左图对比 1,000 J 热量注入 1,000 K 高温炉(+1 J/K)与 250 K 冰窖(+4 J/K)说明 dS=δQrev/T 如何成为状态参量；右图用 1 kWh 电能耗散为 25℃ 室温内能(+12,074 J/K)解释为何能量守恒仍需节约能源。",
        el,
    )
    write_svg(SUBDIR, "clausius-entropy-and-energy-quality.svg", svg)


@register("thermo-mechanics", "力学与热力学的能量守恒与状态参量原创图解", "physics")
def build_all():
    _verify_physics()
    build_fig1_mechanical_to_joule()
    build_fig2_pv_paths_anim()
    build_fig3_micro_to_macro_funnel()
    build_fig4_extensive_intensive_potentials()
    build_fig5_entropy_and_energy_quality()
