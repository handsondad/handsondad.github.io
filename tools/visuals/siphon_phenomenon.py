"""
Visuals for '虹吸现象：流体力学原理、百年物理学大论战、气蚀高度极限与古今工程巧思'
(Siphon Phenomenon: Bernoulli & Darcy-Weisbach Pressure Profile + Hero's Counterexample,
100-Year OED Debate & 4 Extreme Lab Experiments [Vacuum / Gas / Hypobaric Waterfall / 15.4m Negative Pressure],
Antoine Cavitation Height Limit vs Water Temperature & Altitude + Young-Laplace Microbubble Nucleation,
Automatic Triggered Siphons: Pythagoras / Palace Museum Gongdaobei Cup & S-Trap Flush Toilet,
and True Siphon [Kewu Over-Hill] vs Inverted Siphon [Pressurized U-Conduit] & Siphonic Roof Drainage).

Generates 5 original 760px Chinese SVG diagrams in assets/images/siphon-phenomenon/
with verified fluid-dynamic, thermodynamic, and hydrostatic numerical assertions.
"""
from __future__ import annotations

import math

from .core import (
    BLUE,
    BLUE_LINE,
    BLUE_SOFT,
    BODY,
    BORDER,
    GREEN,
    GREEN_SOFT,
    header,
    INK,
    MUTED,
    ORANGE,
    ORANGE_SOFT,
    pill,
    PURPLE,
    PURPLE_SOFT,
    register,
    SLATE,
    SLATE_SOFT,
    step_badge,
    txt,
    card,
    figure,
    write_svg,
)

TOPIC = "siphon-phenomenon"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"


def _line(x1, y1, x2, y2, stroke=INK, sw=1.6, dash=None, marker=None, cls=None):
    extra = ""
    if cls:
        extra += f' class="{cls}"'
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def _extra_markers() -> str:
    return f"""<marker id="arr-ink" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{INK}"/>
  </marker>
  <marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{RED}"/>
  </marker>
  <marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{PURPLE}"/>
  </marker>
  <marker id="arr-teal" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{TEAL}"/>
  </marker>"""


# ---------------------------------------------------------------------------
# 1. Siphon Anatomy, Pressure Profile & Hero's Counterexample (with 1-shot CSS animation)
# ---------------------------------------------------------------------------
def build_siphon_anatomy_and_pressure() -> str:
    g = 9.80665
    rho = 998.2  # kg/m^3 at 20 C
    p_atm = 101.325  # kPa
    h1 = 0.60  # crest height above upper surface (m)
    H = 0.80   # net drop from upper surface to outlet (m)

    # Ideal inviscid Bernoulli velocity & pressures (in kPa)
    v_ideal = math.sqrt(2 * g * H)
    assert 3.95 < v_ideal < 3.97
    dyn_ideal = 0.5 * rho * v_ideal**2 / 1000.0  # kPa
    p_b_ideal = p_atm - dyn_ideal
    p_c_ideal = p_atm - (rho * g * h1) / 1000.0 - dyn_ideal
    p_d = p_atm
    assert p_c_ideal < p_b_ideal < p_atm

    # Realistic viscous flow (L=3.0 m, d=12 mm, f=0.028, sum_K=1.5 -> total K = 1 + 1.5 + f*L/d = 9.5)
    L_pipe, d_pipe, f_dw, k_minor = 3.0, 0.012, 0.028, 1.5
    loss_factor = 1.0 + k_minor + f_dw * (L_pipe / d_pipe)
    v_real = math.sqrt(2 * g * H / loss_factor)
    assert 1.25 < v_real < 1.30  # ~1.285 m/s realistic aquarium hose velocity!
    dyn_real = 0.5 * rho * v_real**2 / 1000.0

    # Along tube s in [0, 3.0 m]: intake at z=-0.25 (s=0), B at z=0 (s=0.25), C at z=+0.60 (s=1.05), D at z=-0.80 (s=3.0)
    # Exact extended Bernoulli energy equation from free surface A (z=0, v=0, P=P_atm) to tube station s:
    # P(s) = P_atm - rho*g*z(s) - 0.5*rho*v_real^2 * (1 + k_loc + f*(s/d))
    def p_visc(s: float, z: float, k_loc: float) -> float:
        head_drop_pa = (1.0 + k_loc + f_dw * (s / d_pipe)) * (0.5 * rho * v_real**2)
        return p_atm - (rho * g * z + head_drop_pa) / 1000.0

    p_in_real = p_visc(0.0, -0.25, 0.5)   # submerged 0.25 m, entrance loss K=0.5
    p_b_real = p_visc(0.25, 0.0, 0.5)
    p_c_real = p_visc(1.05, h1, 0.9)      # entrance + first bend loss up to crest
    p_d_real = p_visc(3.0, -H, k_minor)   # exit jet closes identically to P_atm!
    assert abs(p_d_real - p_atm) < 1e-6
    assert 91.5 < p_c_real < 92.5
    assert p_c_ideal < p_c_real < p_atm

    css = """
  @keyframes siphonParcel {
    0%   { stroke-dashoffset: 380; opacity: 0.25; }
    15%  { opacity: 0.95; }
    100% { stroke-dashoffset: 0; opacity: 0.95; }
  }
  .anim-flow {
    stroke-dasharray: 10 14;
    stroke-dashoffset: 380;
    animation: siphonParcel 3.2s cubic-bezier(0.22, 0.61, 0.36, 1) 1 forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .anim-flow {
      animation: none !important;
      stroke-dashoffset: 0 !important;
      opacity: 0.95 !important;
    }
  }"""

    els = []
    els.extend(
        header(
            "虹吸管剖面、沿管压强曲线与希罗反例：水为什么愿意先爬坡再下坠？",
            f"模型参数：P₀ = {p_atm:.1f} kPa，爬升高度 h₁ = {h1:.2f} m，液面总落差 H = {H:.2f} m（20 °C 清水）",
        )
    )

    # Left Card: Physical Siphon Diagram + Hero's Counterexample
    els.append(card(20, 62, 366, 412))
    els.append(step_badge(40, 84, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(58, 88, "物理空间：四处关键截面（A → B → C → D）", size=13, color=INK, weight="700"))

    # Coordinate setup inside left card:
    # z = +0.60 m (Crest C) -> y = 132
    # z =  0.00 m (Upper surface A & B) -> y = 204  (scale: 120 px per meter!)
    # z = -0.25 m (Tube intake) -> y = 234
    # z = -0.80 m (Outlet D) -> y = 300
    y_crest = 132.0
    y_surf = 204.0
    y_in = 234.0
    y_out = 300.0

    # Upper reservoir tank
    els.append('<rect x="42" y="186" width="112" height="72" rx="4" fill="#f8fafc" stroke="#64748b" stroke-width="1.6"/>')
    els.append('<rect x="44" y="204" width="108" height="52" rx="2" fill="#dbeafe"/>')
    els.append(_line(44, y_surf, 152, y_surf, stroke=BLUE, sw=2.0))
    # Open top of tank
    els.append(_line(42, 186, 154, 186, stroke="#f8fafc", sw=2.6))

    # Lower catch basin below D
    els.append('<rect x="234" y="316" width="96" height="44" rx="4" fill="#f8fafc" stroke="#64748b" stroke-width="1.6"/>')
    els.append('<rect x="236" y="334" width="92" height="24" rx="2" fill="#dbeafe"/>')
    els.append(_line(234, 316, 330, 316, stroke="#f8fafc", sw=2.6))

    # Reference elevation dashed lines
    els.append(_line(152, y_surf, 368, y_surf, stroke=BLUE, sw=1.1, dash="4 3"))
    els.append(_line(188, y_crest, 368, y_crest, stroke=RED, sw=1.1, dash="4 3"))
    els.append(_line(266, y_out, 368, y_out, stroke=GREEN, sw=1.1, dash="4 3"))

    # Height dimension arrows on right of siphon
    # h1: y_surf (204) to y_crest (132) at x=336
    els.append(_line(334, y_surf - 2, 334, y_crest + 3, stroke=RED, sw=1.4, marker="arr-red"))
    els.append(txt(342, 171, "h₁=0.6m", size=11, color=RED, weight="600"))
    # H: y_surf (204) to y_out (300) at x=334
    els.append(_line(334, y_surf + 2, 334, y_out - 3, stroke=GREEN, sw=1.4, marker="arr-green"))
    els.append(txt(342, 256, "H=0.8m", size=11, color=GREEN, weight="700"))

    # Siphon Tube (inverted U path from (116, 238) up to (116, 154) arc to (262, 154) down to (262, 300))
    # Centerline path: M 116,238 L 116,162 C 116,120 262,120 262,162 L 262,300
    # Note: Bezier apex of C (116,120) (262,120) from y=162 has y_min = 0.25*162 + 0.75*120 = 40.5 + 90 = 130.5 (~132)!
    tube_d = "M 116,238 L 116,162 C 116,122 262,122 262,162 L 262,300"
    els.append(f'<path d="{tube_d}" fill="none" stroke="#334155" stroke-width="15" stroke-linecap="butt"/>')
    els.append(f'<path d="{tube_d}" fill="none" stroke="#93c5fd" stroke-width="11" stroke-linecap="butt"/>')
    # Animated parcels inside tube
    els.append(f'<path d="{tube_d}" fill="none" stroke="#1d4ed8" stroke-width="4.5" stroke-linecap="round" class="anim-flow"/>')
    # Falling jet into lower basin
    els.append(_line(262, 301, 262, 332, stroke="#60a5fa", sw=6.5))
    els.append(_line(262, 304, 262, 326, stroke=BLUE, sw=1.6, marker="arr-blue"))

    # Atmospheric push arrow on A
    els.append(_line(74, 166, 74, 199, stroke=ORANGE, sw=1.8, marker="arr-orange"))
    els.append(txt(74, 160, "大气压 P₀", size=11, color=ORANGE, anchor="middle", weight="600"))

    # Labels A, B, C, D with clear callout circles
    pts = [
        (74, y_surf, "A", ORANGE, "A 自由液面"),
        (116, y_surf, "B", BLUE, "B 管内等高面"),
        (189, 132, "C", RED, "C 管顶低压极值"),
        (262, y_out, "D", GREEN, "D 出口射流面"),
    ]
    for px, py, code, col, _ in pts:
        els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8.5" fill="#ffffff" stroke="{col}" stroke-width="2"/>')
        els.append(txt(px, py + 4, code, size=11, color=col, anchor="middle", weight="700"))

    els.append(txt(46, 274, "A: z=0, v≈0, P=P₀", size=11, color=BODY))
    els.append(txt(46, 291, "B: z=0, P_B < P₀ (流速降压)", size=11, color=BLUE))
    els.append(txt(189, 115, "C 管顶最低压区 (易析出气泡)", size=11.5, color=RED, anchor="middle", weight="600"))
    els.append(txt(144, 348, f"D 实测流速 ≈ {v_real:.2f} m/s", size=11, color=GREEN, weight="600"))

    # Hero of Alexandria Counterexample Box at bottom of Left Card
    els.append(card(34, 372, 338, 90, rx=8, fill=AMBER_SOFT, stroke=AMBER, sw=1.1))
    els.append(txt(46, 391, "古希腊希罗反例（《气动力学》命题 1，约公元 1 世纪）：", size=11.5, color=AMBER, weight="700"))
    els.append(txt(46, 410, "• 误区：“外侧管更粗、装水总重量更大，就能把水拽出来”", size=11, color=BODY))
    els.append(txt(46, 428, "• 希罗实验：内侧细长、外侧粗短（出口高于上液面 H < 0），", size=11, color=BODY))
    els.append(txt(46, 446, "  哪怕外管水重十倍，水仍倒流回桶！决定流向的唯独是高差 H。", size=11, color=INK, weight="600"))

    # Right Card: Computed Pressure Profile Chart P(s)
    els.append(card(398, 62, 342, 412))
    els.append(step_badge(418, 84, 2, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(436, 88, "沿管绝对压强分布 P(s)：理想 vs 真实黏性流", size=13, color=INK, weight="700"))

    # Plot box: x in [446, 718] (width=272), s in [0, 3.0 m]
    # y in [126, 326] (height=200), P in [86, 106] kPa -> 10 px per kPa!
    x0, x1 = 448.0, 718.0
    y_top, y_bot = 126.0, 326.0
    p_min, p_max = 86.0, 106.0

    def sx(s_val: float) -> float:
        return x0 + (s_val / 3.0) * (x1 - x0)

    def sy(p_val: float) -> float:
        return y_bot - ((p_val - p_min) / (p_max - p_min)) * (y_bot - y_top)

    # Grid lines
    for pv in [88, 92, 96, 100, 104]:
        gy = sy(pv)
        els.append(_line(x0, gy, x1, gy, stroke="#e2e8f0", sw=1.0))
        els.append(txt(x0 - 6, gy + 4, f"{pv}", size=10.5, color=MUTED, anchor="end", cls="mono"))
    els.append(txt(442, 114, "绝对压强 P (kPa)", size=11, color=MUTED))

    # P_atm reference line (101.325 kPa)
    y_patm = sy(p_atm)
    els.append(_line(x0, y_patm, x1, y_patm, stroke=ORANGE, sw=1.3, dash="5 3"))
    els.append(txt(x1 - 2, y_patm - 5, "大气压 101.3 kPa", size=10.5, color=ORANGE, anchor="end", weight="600"))

    # Axes
    els.append(_line(x0, y_top, x0, y_bot, stroke=SLATE, sw=1.4))
    els.append(_line(x0, y_bot, x1, y_bot, stroke=SLATE, sw=1.4))

    # Ideal Bernoulli polyline: s=0 (z=-0.25, P=101.3+2.45-7.83=95.94), s=0.25 (B, 93.49), s=1.05 (C, 87.62), s=3.0 (D, 101.33)
    p_in_id = p_atm + (rho * g * 0.25) / 1000.0 - dyn_ideal
    ideal_pts = [
        (0.0, p_in_id),
        (0.25, p_b_ideal),
        (1.05, p_c_ideal),
        (3.0, p_d),
    ]
    id_poly = " ".join(f"{sx(s):.1f},{sy(p):.1f}" for s, p in ideal_pts)
    els.append(f'<polyline points="{id_poly}" fill="none" stroke="{PURPLE}" stroke-width="2.0" stroke-dasharray="5 4"/>')

    # Real viscous Darcy-Weisbach polyline:
    real_pts = [
        (0.0, p_in_real),
        (0.25, p_b_real),
        (1.05, p_c_real),
        (3.0, p_d_real),
    ]
    re_poly = " ".join(f"{sx(s):.1f},{sy(p):.1f}" for s, p in real_pts)
    els.append(f'<polyline points="{re_poly}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

    # Dots and station ticks on x-axis
    stations = [
        (0.0, "管口", p_in_real),
        (0.25, "B", p_b_real),
        (1.05, "C(管顶)", p_c_real),
        (3.0, "D(出口)", p_d_real),
    ]
    for s_val, lbl, pv in stations:
        px = sx(s_val)
        py = sy(pv)
        els.append(_line(px, y_bot, px, y_bot + 4, stroke=SLATE, sw=1.2))
        anch = "start" if s_val == 0 else ("end" if s_val == 3.0 else "middle")
        dx = -2 if s_val == 0 else (4 if s_val == 0.25 else 0)
        els.append(txt(px + dx, y_bot + 17, lbl, size=10.5, color=INK, anchor=anch, weight="600"))
        els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.2" fill="{BLUE}" stroke="#ffffff" stroke-width="1.4"/>')

    # Highlight minimum at C
    cx_id, cy_id = sx(1.05), sy(p_c_ideal)
    cx_re, cy_re = sx(1.05), sy(p_c_real)
    els.append(f'<circle cx="{cx_id:.1f}" cy="{cy_id:.1f}" r="4.0" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.4"/>')
    els.append(txt(cx_re + 8, cy_re - 6, f"真实管顶 {p_c_real:.1f} kPa", size=11, color=BLUE, weight="700"))
    els.append(txt(cx_id + 8, cy_id + 13, f"无摩擦理想 {p_c_ideal:.1f} kPa", size=10.5, color=PURPLE, weight="600"))

    # Legend & takeaway box inside Right Card
    els.append(_line(416, 362, 444, 362, stroke=BLUE, sw=2.6))
    els.append(txt(450, 366, f"真实软管（内径 12 mm，长 3 m）：v ≈ {v_real:.2f} m/s", size=11, color=BODY))
    els.append(_line(416, 382, 444, 382, stroke=PURPLE, sw=2.0, dash="5 4"))
    els.append(txt(450, 386, f"理想无黏性流（托里拆利极限）：v = √(2gH) = {v_ideal:.2f} m/s", size=11, color=BODY))

    els.append(card(412, 398, 314, 64, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE, sw=1.0))
    els.append(txt(424, 418, "读图关键：从 A 到 C 压强一路跌破大气压（负表压抽吸），", size=11, color=INK, weight="600"))
    els.append(txt(424, 436, "过了管顶 C 后重力加速大于沿程摩擦，压强回升至出口 D", size=11, color=BODY))
    els.append(txt(424, 453, "的 P₀；管越细长，摩擦耗散越大，管顶低压反而更温和。", size=11, color=BODY))

    return figure(
        490,
        "虹吸管物理剖面、沿管绝对压强分布与古希腊希罗反例",
        "左图展示虹吸管A自由液面、B等高面、C管顶最高点与D出口射流面及希罗反例；右图对比理想伯努利流与真实黏性管流的沿管绝对压强曲线。",
        els,
        extra_css=css,
        extra_defs=_extra_markers(),
    )


# ---------------------------------------------------------------------------
# 2. 100-Year OED Siphon Debate & Four Extreme Laboratory Experiments
# ---------------------------------------------------------------------------
def build_pump_vs_chain_experiments() -> str:
    # Numerical verification of Vera et al. (2016) 15.4 m siphon & Boatwright et al. (2015) 15.04 m siphon:
    g = 9.80665
    rho = 998.2
    p_atm_sea = 101.325  # kPa
    h_vera = 15.4  # m
    p_crest_vera = p_atm_sea - (rho * g * h_vera) / 1000.0
    assert -50.0 < p_crest_vera < -49.0  # ~ -49.4 kPa absolute negative pressure!

    h_boatwright = 15.04  # m at P_atm = 99.8 kPa
    p_crest_boat = 99.8 - (rho * g * h_boatwright) / 1000.0
    assert -48.0 < p_crest_boat < -47.0  # ~ -47.4 kPa absolute negative pressure!

    # Hughes & Gurung (2014) hypobaric chamber at 40,000 ft: P0 = 18.75 kPa, T=25C (Pv=3.15 kPa), v=0.59 m/s
    p_40k = 18.75
    pv_25 = 3.15
    v_40k = 0.59
    h_max_40k = (p_40k - pv_25 - 0.5 * rho * v_40k**2 / 1000.0) * 1000.0 / (rho * g)
    assert 1.55 < h_max_40k < 1.60  # matches Hughes & Gurung's reported 1.57 m!

    els = []
    els.extend(
        header(
            "大气压“推泵”还是分子“链条”？终结百年词典之争的四组极限实验",
            "2010 年《牛津英语词典》释义争议引爆物理学界实测潮：单一假说均被证伪，重力与双传力机制缺一不可",
        )
    )

    # 2x2 Matrix of Extreme Experiments
    cards_spec = [
        (
            20, 64, 352, 168,
            1, PURPLE, PURPLE_SOFT,
            "高真空离子液体虹吸（2011）",
            "环境气压 P₀ ≈ 0 Pa · 极低蒸气压液体",
            [
                "• 诺丁汉大学团队（Boatwright 等）在超高真空腔内实验",
                "• 完全没有大气压“推”液面，不可挥发的离子液体照样翻越",
                "  弯管流向下游容器！",
                "• 结论：证伪“虹吸必须有大气压”，分子内聚拉力可独立传力。",
            ],
            "支持：重力 + 分子内聚力链条",
        ),
        (
            388, 64, 352, 168,
            2, ORANGE, ORANGE_SOFT,
            "CO₂ 重气体虹吸与气泡断链虹吸（2011）",
            "分子内聚拉力 = 0 · 环境气压 P₀ = 1 atm",
            [
                "• Ramette 等用密度大于空气的二氧化碳气体完成“无液虹吸”；",
                "• Richert 与 Binder 在水虹吸管顶部注入大气泡截断水柱",
                "• 气体无内聚拉力、水分子链彻底断开，虹吸依然稳定运行！",
                "• 结论：证伪“虹吸必须靠分子手拉手”，正气压差可独立传力。",
            ],
            "支持：重力 + 大气压差推动",
        ),
        (
            20, 244, 352, 168,
            3, BLUE, BLUE_SOFT,
            "低压舱 1.2 万米高空“管内瀑布”（2014）",
            f"P₀ = 18.75 kPa（0.185 atm）· 理论限高 {h_max_40k:.2f} m",
            [
                "• Hughes 与 Gurung 将 1.52 m 虹吸管升至等效 4 万英尺高空",
                "• 管顶水室温沸腾，下游出现高约 41 cm 的自由落体“管内瀑布”",
                "• 水柱虽在下游断开，仍维持 4.1 L/min 流量；再降至 17.9 kPa",
                "  彻底分裂成两支背靠背气压计，升压后水柱自动重连恢复！",
            ],
            "揭示：虹吸与气压计的连续相变边界",
        ),
        (
            388, 244, 352, 168,
            4, GREEN, GREEN_SOFT,
            "突破 10.33 米铁律：15.4 米负压水虹吸（2015–2016）",
            f"管顶绝对压强 ≈ {p_crest_vera:.1f} kPa（绝对负压拉伸态）",
            [
                "• Boatwright 等（15.04 m 深度脱气水）与 Vera 等（15.4 m",
                "  脱气+洗洁精表面活性剂除核）先后打破托里拆利极限！",
                "• 管顶水处于约 -0.5 atm 亚稳态张力下持续双向换向流动 224 s",
                "• 结论：10.3 米不是绝对上限，而是普通含气水的“气蚀红线”。",
            ],
            "打通：工程虹吸与百米巨杉木质部输水",
        ),
    ]

    for x, y, w, h, num, col, bg, title, sub, bullets, tag in cards_spec:
        els.append(card(x, y, w, h, rx=10, fill="#ffffff", stroke=BORDER))
        els.append(f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="3" fill="{col}"/>')
        els.append(step_badge(x + 20, y + 24, num, fg=col, bg=bg))
        els.append(txt(x + 38, y + 28, title, size=12.8, color=INK, weight="700"))
        els.append(txt(x + 16, y + 48, sub, size=11, color=col, weight="600"))
        by = y + 69
        for b in bullets:
            els.append(txt(x + 16, by, b, size=11, color=BODY))
            by += 18
        els.append(pill(x + 16, y + h - 28, tag, fg=col, bg=bg, w=236, h=20, size=11))

    # Bottom Unified Verdict Banner
    els.append(card(20, 424, 720, 72, rx=10, fill=SLATE_SOFT, stroke=INK, sw=1.3))
    els.append(txt(36, 444, "现代流体力学终极定论（动力源 vs 传力桥梁）：", size=12.2, color=INK, weight="700"))
    els.append(
        txt(
            36,
            464,
            "① 唯一能量引擎永远是【重力】（进出口液面落差 H > 0 释放引力势能，无论真空还是高压均不可违背）；",
            size=11,
            color=BODY,
        )
    )
    els.append(
        txt(
            36,
            483,
            "② 跨过管顶传递动量的桥梁有两条：含气液体与气体虹吸靠【环境正气压防断流】，真空与超 10 米靠【脱气液体内聚抗拉强度】。",
            size=11,
            color=BODY,
        )
    )

    return figure(
        510,
        "终结虹吸百年争论的四组极限实验对比图",
        "四宫格展示2011年高真空离子液体虹吸、2011年二氧化碳气体与气泡断链虹吸、2014年低压舱管内瀑布实验与2015至2016年15.4米绝对负压水虹吸实验，底部总结重力引擎与双传力桥梁统一定论。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. Cavitation Height Limit vs Water Temperature, Altitude & Bubble Nucleation
# ---------------------------------------------------------------------------
def build_cavitation_height_limit() -> str:
    g = 9.80665
    p0 = 101325.0  # Pa

    # Antoine equation for water (1 to 100 C): log10(Pv_mmHg) = 8.07131 - 1730.63 / (233.426 + T)
    def pv_pa(temp_c: float) -> float:
        mmhg = 10.0 ** (8.07131 - 1730.63 / (233.426 + temp_c))
        return mmhg * 133.322368

    # Approximate water density kg/m^3 from 0 to 100 C
    def rho_w(temp_c: float) -> float:
        return 999.84 + 0.068 * temp_c - 0.0085 * temp_c**2 + 0.000042 * temp_c**3

    def h_max_temp(temp_c: float) -> float:
        return max(0.0, (p0 - pv_pa(temp_c)) / (rho_w(temp_c) * g))

    h_0 = h_max_temp(0.0)
    h_20 = h_max_temp(20.0)
    h_60 = h_max_temp(60.0)
    h_85 = h_max_temp(85.0)
    h_100 = h_max_temp(100.0)
    assert 10.25 < h_0 < 10.30
    assert 10.08 < h_20 < 10.14   # ~10.11 m at 20 C!
    assert 8.40 < h_60 < 8.55     # ~8.47 m at 60 C!
    assert 4.45 < h_85 < 4.65     # ~4.55 m at 85 C!
    assert h_100 < 0.02           # ~0.00 m at 100 C!

    # Standard atmosphere pressure vs altitude (troposphere barometric formula)
    def p_alt_pa(alt_m: float) -> float:
        return 101325.0 * (1.0 - 2.25577e-5 * alt_m) ** 5.25588

    def h_max_alt(alt_m: float, temp_c: float = 20.0) -> float:
        return max(0.0, (p_alt_pa(alt_m) - pv_pa(temp_c)) / (rho_w(temp_c) * g))

    alt_cases = [
        ("海平面 (0 m)", 0, BLUE),
        ("昆明 (1890 m)", 1890, TEAL),
        ("拉萨 (3650 m)", 3650, GREEN),
        ("珠峰大本营 (5200 m)", 5200, ORANGE),
        ("客机巡航高度 (12000 m)", 12000, RED),
    ]
    alt_vals = [(lbl, alt, h_max_alt(alt), col) for lbl, alt, col in alt_cases]
    assert 10.0 < alt_vals[0][2] < 10.2
    assert 6.3 < alt_vals[2][2] < 6.6
    assert 1.65 < alt_vals[4][2] < 1.85

    # Young-Laplace microbubble critical diameter for 1 atm tension: d = 4 * gamma / P0
    gamma = 0.072  # N/m
    d_crit_um = (4.0 * gamma / p0) * 1e6
    assert 2.80 < d_crit_um < 2.88  # ~2.84 um!

    els = []
    els.extend(
        header(
            "普通水虹吸的“生死红线”：水温、海拔与微米气核如何锁死爬升高度？",
            "一旦管顶压强跌至饱和蒸气压 Pᵥ，水在室温下剧烈沸腾（气蚀断流）；开水根本无法向上虹吸",
        )
    )

    # Left Card: h_max(T) Curve from 0 C to 100 C
    els.append(card(20, 62, 362, 404))
    els.append(step_badge(40, 84, 1, fg=RED, bg=RED_SOFT))
    els.append(txt(58, 88, "海平面极限高度 h_max 随水温骤降曲线", size=13, color=INK, weight="700"))

    lx0, lx1 = 64.0, 358.0
    ly_top, ly_bot = 122.0, 322.0

    def tx_map(tc: float) -> float:
        return lx0 + (tc / 100.0) * (lx1 - lx0)

    def hy_map(hm: float) -> float:
        return ly_bot - (hm / 11.0) * (ly_bot - ly_top)

    for hm in [0, 2, 4, 6, 8, 10]:
        gy = hy_map(hm)
        els.append(_line(lx0, gy, lx1, gy, stroke="#e2e8f0", sw=1.0))
        els.append(txt(lx0 - 6, gy + 4, f"{hm}m", size=10.5, color=MUTED, anchor="end", cls="mono"))

    # Classical 10.33 m dry-vacuum myth line
    y_1033 = hy_map(10.33)
    els.append(_line(lx0, y_1033, lx1, y_1033, stroke=SLATE, sw=1.1, dash="4 3"))
    els.append(txt(lx1 - 2, y_1033 - 4, "忽略蒸气压理论值 10.33 m", size=10.5, color=SLATE, anchor="end"))

    els.append(_line(lx0, ly_top, lx0, ly_bot, stroke=SLATE, sw=1.4))
    els.append(_line(lx0, ly_bot, lx1, ly_bot, stroke=SLATE, sw=1.4))

    for tc in [0, 20, 40, 60, 80, 100]:
        gx = tx_map(tc)
        els.append(_line(gx, ly_bot, gx, ly_bot + 4, stroke=SLATE, sw=1.2))
        els.append(txt(gx, ly_bot + 17, f"{tc}°C", size=10.5, color=MUTED, anchor="middle", cls="mono"))

    # Fill under curve + curve polyline
    pts_curve = [(tc, h_max_temp(float(tc))) for tc in range(0, 101, 2)]
    poly_str = " ".join(f"{tx_map(t):.1f},{hy_map(h):.1f}" for t, h in pts_curve)
    area_str = f"{tx_map(0):.1f},{ly_bot:.1f} " + poly_str + f" {tx_map(100):.1f},{ly_bot:.1f}"
    els.append(f'<polygon points="{area_str}" fill="#fee2e2" fill-opacity="0.45"/>')
    els.append(f'<polyline points="{poly_str}" fill="none" stroke="{RED}" stroke-width="2.6"/>')

    # Key annotated points
    key_t = [
        (20, h_20, f"20°C: {h_20:.1f} m", -10, 19, BLUE, "start"),
        (60, h_60, f"60°C: {h_60:.1f} m", 8, -7, ORANGE, "start"),
        (85, h_85, f"85°C: {h_85:.1f} m", -10, -8, RED, "end"),
        (100, h_100, "100°C: 0 m (沸水断流)", -6, -10, INK, "end"),
    ]
    for tc, hv, lbl, dx, dy, col, anch in key_t:
        px, py = tx_map(tc), hy_map(hv)
        els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.2" fill="{col}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(px + dx, py + dy, lbl, size=10.8, color=col, anchor=anch, weight="700"))

    els.append(card(34, 354, 334, 98, rx=8, fill=RED_SOFT, stroke="#fecaca", sw=1.0))
    els.append(txt(46, 374, "生活反直觉实验：为什么刚烧开的热水很难用软管虹吸？", size=11.5, color=RED, weight="700"))
    els.append(txt(46, 393, "• 20 °C 冷水饱和蒸气压仅 2.33 kPa，大气压还能撑起 10.1 m；", size=11, color=BODY))
    els.append(txt(46, 411, "• 85 °C 热水蒸气压暴涨至 57.8 kPa，极限高度腰斩至 4.6 m；", size=11, color=BODY))
    els.append(txt(46, 429, "• 100 °C 沸水 Pᵥ = P₀，只要软管略高于液面立刻沸腾断流！", size=11, color=INK, weight="600"))

    # Right Card: Altitude Bars + Young-Laplace Microbubble Physics
    els.append(card(396, 62, 344, 404))
    els.append(step_badge(416, 84, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(434, 88, "海拔气压衰减（20 °C 水）与微米气核准则", size=13, color=INK, weight="700"))

    bx0 = 548.0
    bw_max = 152.0  # for 11 m
    by = 114.0
    for lbl, alt, hv, col in alt_vals:
        els.append(txt(540, by + 13, lbl, size=11, color=BODY, anchor="end"))
        bw = (hv / 11.0) * bw_max
        els.append(f'<rect x="{bx0:.1f}" y="{by:.1f}" width="{bw_max:.1f}" height="18" rx="4" fill="#f1f5f9"/>')
        els.append(f'<rect x="{bx0:.1f}" y="{by:.1f}" width="{bw:.1f}" height="18" rx="4" fill="{col}"/>')
        els.append(txt(bx0 + bw + 6, by + 13, f"{hv:.1f} m", size=11, color=col, weight="700", cls="mono"))
        by += 32

    # Young-Laplace Microbubble Nucleation Box
    els.append(card(410, 282, 316, 170, rx=8, fill=TEAL_SOFT, stroke="#99f6e4", sw=1.1))
    els.append(txt(422, 303, "杨-拉普拉斯气核定律：ΔP = 2γ / r（γ = 0.072 N/m）", size=11.5, color=TEAL, weight="700"))
    els.append(txt(422, 323, f"• 管壁缝隙藏着直径 ≥ {d_crit_um:.1f} μm 微气泡：负压刚过 1 atm", size=11, color=BODY))
    els.append(txt(422, 341, "  （爬升 > 10.1 m）气核瞬间失稳膨胀，扯断水柱；", size=11, color=BODY))
    els.append(txt(422, 361, "• 真空脱气 + 表面活性剂润湿除核：消除微米气核后，", size=11, color=BODY))
    els.append(txt(422, 379, "  实验室虹吸一举爬上 15.4 m（负压 -49 kPa）；", size=11, color=BODY))
    els.append(txt(422, 399, "• 北美巨杉木质部纹孔膜（纳米孔径 ~2.8 nm）：可抗", size=11, color=BODY))
    els.append(txt(422, 417, "  100 MPa 级张力，靠叶片蒸腾把水拉上 110 米树冠！", size=11, color=INK, weight="600"))
    els.append(pill(422, 426, "气泡越小 → 表面张力锁死越紧 → 抗负压越强", fg=TEAL, bg="#ffffff", w=288, h=20, size=10.8))

    return figure(
        480,
        "水虹吸极限爬升高度与水温、海拔及微米气核关系图",
        "左图基于安托万方程绘制0至100摄氏度海平面水虹吸极限高度曲线；右图展示不同海拔极限高度条形对比及杨-拉普拉斯微米气核失稳与巨杉纳米抗负压机理。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. Automatic Intermittent Siphon: Fairness Cup (Gongdaobei) & S-Trap Flush Toilet
# ---------------------------------------------------------------------------
def build_intermittent_siphon_devices() -> str:
    # Geometric level assertions for the 3-state Fairness Cup
    crest_level = 0.72      # normalized cup height where inner bend crest sits
    state1_level = 0.55     # < crest -> holds wine safely
    state2_level = 0.80     # > crest -> self-primes siphon!
    state3_level = 0.22     # < crest yet still draining until intake at 0.08!
    intake_level = 0.08
    assert intake_level < state3_level < state1_level < crest_level < state2_level

    els = []
    els.extend(
        header(
            "不靠嘴吸、自动触发的间歇虹吸：从“知足常乐”公道杯到抽水马桶",
            "把弯管藏进容器内部：液面越过弯顶的瞬间自动排空管内空气，完成“无人工引水”自启动",
        )
    )

    # Left Card: 3-stage Fairness Cup / Pythagoras Cup / Palace Museum Gongdaobei
    els.append(card(20, 62, 444, 408))
    els.append(step_badge(40, 84, 1, fg=AMBER, bg=AMBER_SOFT))
    els.append(txt(58, 88, "公道杯 / 毕达哥拉斯贪心杯：跨过红线就“倾家荡产”", size=13, color=INK, weight="700"))
    els.append(txt(40, 108, "古希腊希罗《气动力学》命题 12 同心套管 · 故宫藏清光绪宜兴窑绿地粉彩公道杯", size=11, color=MUTED))

    stages = [
        (38, "① 知足态（安全）", "酒面低于暗管弯顶", state1_level, False, False, GREEN),
        (182, "② 越界触发（自充管）", "贪倒一口淹没弯顶", state2_level, True, False, ORANGE),
        (326, "③ 贪心排空（停不住）", "液面跌破弯顶仍抽干", state3_level, True, True, RED),
    ]

    for sx0, st_title, st_sub, lvl, flowing, low_drain, col in stages:
        # Cup box geometry: x in [sx0, sx0+118], cup bowl y in [164, 272], stem y in [272, 314]
        cx = sx0 + 59.0
        y_rim = 164.0
        y_bowl_bot = 272.0
        y_crest = y_bowl_bot - crest_level * (y_bowl_bot - y_rim)  # ~194.2
        y_liq = y_bowl_bot - lvl * (y_bowl_bot - y_rim)

        els.append(txt(cx, 134, st_title, size=11.8, color=col, anchor="middle", weight="700"))
        els.append(txt(cx, 150, st_sub, size=10.5, color=MUTED, anchor="middle"))

        # Liquid inside bowl
        els.append(
            f'<rect x="{sx0 + 16:.1f}" y="{y_liq:.1f}" width="86" height="{y_bowl_bot - y_liq:.1f}" '
            f'rx="4" fill="#fde68a" fill-opacity="0.85"/>'
        )
        els.append(_line(sx0 + 16, y_liq, sx0 + 102, y_liq, stroke=AMBER, sw=1.8))

        # Crest threshold red dashed line
        els.append(_line(sx0 + 10, y_crest, sx0 + 108, y_crest, stroke=RED, sw=1.1, dash="3 3"))

        # Cup walls & stem with bottom drain hole
        els.append(
            f'<path d="M {sx0 + 14},{y_rim} L {sx0 + 14},{y_bowl_bot} L {cx - 9},{y_bowl_bot} '
            f'L {cx - 9},310 M {sx0 + 104},{y_rim} L {sx0 + 104},{y_bowl_bot} L {cx + 9},{y_bowl_bot} L {cx + 9},310" '
            f'fill="none" stroke="#334155" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        # Central concealed siphon column: intake at bottom left of column, up over y_crest, down center bore to y=312
        siph_d = f"M {cx - 14},265 L {cx - 14},{y_crest + 6:.1f} C {cx - 14},{y_crest - 8:.1f} {cx},{y_crest - 8:.1f} {cx},{y_crest + 6:.1f} L {cx},312"
        els.append(f'<path d="{siph_d}" fill="none" stroke="#475569" stroke-width="8.5" stroke-linecap="butt"/>')

        if not flowing:
            # Only ascending leg filled up to y_liq!
            up_d = f"M {cx - 14},265 L {cx - 14},{y_liq:.1f}"
            els.append(f'<path d="{up_d}" fill="none" stroke="#f59e0b" stroke-width="4.8"/>')
            els.append(f'<path d="M {cx - 14},{y_liq:.1f} L {cx - 14},{y_crest + 6:.1f} C {cx - 14},{y_crest - 8:.1f} {cx},{y_crest - 8:.1f} {cx},{y_crest + 6:.1f} L {cx},312" fill="none" stroke="#f8fafc" stroke-width="4.5"/>')
            els.append(txt(cx, 330, "管顶存气·滴酒不漏", size=10.5, color=GREEN, anchor="middle", weight="600"))
        else:
            # Full continuous wine siphon + bottom jet!
            els.append(f'<path d="{siph_d}" fill="none" stroke="#f59e0b" stroke-width="5.0"/>')
            els.append(_line(cx, 312, cx, 338, stroke="#d97706", sw=4.2))
            els.append(_line(cx + 8, 314, cx + 8, 334, stroke=col, sw=1.4, marker="arr-red" if low_drain else "arr-orange"))
            note_b = "满管负压·整杯漏光" if low_drain else "漫顶排气·瞬间启动"
            els.append(txt(cx, 352, note_b, size=10.5, color=col, anchor="middle", weight="700"))

    els.append(txt(42, 190, "平心刻度线", size=10.5, color=RED, weight="600", halo=True))

    # Explanation box at bottom of Left Card
    els.append(card(34, 368, 416, 88, rx=8, fill=AMBER_SOFT, stroke="#fde68a", sw=1.1))
    els.append(txt(46, 388, "为什么液面降回红线以下（状态 ③），酒还是停不下来？", size=11.5, color=AMBER, weight="700"))
    els.append(txt(46, 408, "• 启动条件 ≠ 维持条件！弯顶红线只是“排尽空气、接通水柱”的触发门槛；", size=11, color=BODY))
    els.append(txt(46, 426, "• 一旦连通，维持流动只看【杯内液面高于杯底漏孔（H > 0）】，直到酒面跌至", size=11, color=BODY))
    els.append(txt(46, 444, "  杯底进水口吸入空气，水柱断裂才会停止——正合“满招损，谦受益”。", size=11, color=INK, weight="600"))

    # Right Card: S-Trap Flush Toilet Engineering
    els.append(card(478, 62, 262, 408))
    els.append(step_badge(498, 84, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(516, 88, "虹吸式马桶 S 型存水弯", size=13, color=INK, weight="700"))
    els.append(txt(494, 108, "日常水封防臭 + 冲水满管抽吸双模态", size=11, color=MUTED))

    # Schematic S-trap inside Right Card (x in [504, 714], y in [128, 294])
    els.append(card(494, 124, 230, 178, rx=8, fill="#f8fafc", stroke=BORDER))
    # Bowl + S-bend path
    strap_d = "M 526,158 L 526,228 C 526,258 574,258 574,220 C 574,174 636,174 636,222 L 636,284"
    els.append(f'<path d="{strap_d}" fill="none" stroke="#334155" stroke-width="24" stroke-linecap="round"/>')
    els.append(f'<path d="{strap_d}" fill="none" stroke="#dbeafe" stroke-width="18" stroke-linecap="round"/>')
    # Full-bore flush streamline arrow
    els.append(f'<path d="M 526,166 L 526,228 C 526,252 574,252 574,220 C 574,180 636,180 636,222 L 636,278" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-dasharray="5 3" marker-end="url(#arr-blue)"/>')

    # Water seal height annotation (~50 mm)
    els.append(_line(506, 192, 658, 192, stroke=TEAL, sw=1.2, dash="4 3"))
    els.append(txt(508, 146, "水箱急冲注水", size=10.8, color=BLUE, weight="600"))
    els.append(txt(606, 166, "S 弯波峰堰顶", size=10.8, color=RED, anchor="middle", weight="700"))
    els.append(txt(550, 276, "5 cm 静态水封防臭", size=10.8, color=TEAL, anchor="middle", weight="600"))
    els.append(txt(680, 256, "直通排污立管", size=10.5, color=SLATE, anchor="middle"))

    # 3 bullet mechanics of S-trap
    els.append(txt(494, 324, "三步读懂每次冲水的声音密码：", size=11.8, color=INK, weight="700"))
    els.append(txt(494, 346, "① 待机防臭：水位停在 S 弯堰顶", size=11, color=BODY))
    els.append(txt(494, 364, "   边缘，5 cm 水封隔绝沼气与臭味；", size=11, color=BODY))
    els.append(txt(494, 386, "② 满管触发：水箱大流量瞬间灌满", size=11, color=BODY))
    els.append(txt(494, 404, "   越过堰顶排空空气，产生强负压抽吸；", size=11, color=BODY))
    els.append(txt(494, 426, "③ 咕噜断流：池底抽空吸进空气，", size=11, color=BODY))
    els.append(txt(494, 444, "   发出“咕噜”声破除虹吸，补水封口。", size=11, color=INK, weight="600"))

    return figure(
        485,
        "自动间歇虹吸装置：公道杯三态演变与虹吸式马桶S型存水弯剖面",
        "左图分知足态、越界触发态、贪心排空态展示公道杯与希罗同心套管自动虹吸原理；右图展示现代虹吸式坐便器S型存水弯水封防臭与满管负压排污过程。",
        els,
        extra_defs=_extra_markers(),
    )


# ---------------------------------------------------------------------------
# 5. True Siphon (Kewu) vs "Inverted Siphon" (Pressurized U-Tube) & Siphonic Roof Drainage
# ---------------------------------------------------------------------------
def build_true_vs_inverted_and_engineering() -> str:
    g = 9.80665
    rho = 998.2
    p_atm = 101.325  # kPa

    # True siphon crest +6 m -> P_top ~ 42.6 kPa (< P_atm, sub-atmospheric!)
    p_true_top = p_atm - (rho * g * 6.0) / 1000.0
    assert 42.0 < p_true_top < 43.0

    # Inverted siphon valley depth -40 m (e.g. Yellow River crossing) -> P_bot ~ 492.9 kPa (~4.9 atm!)
    # Roman Gier aqueduct Yzeron valley depth -120 m -> P_bot ~ 1276 kPa (~12.6 atm!)
    p_inv_40 = p_atm + (rho * g * 40.0) / 1000.0
    p_inv_120 = p_atm + (rho * g * 120.0) / 1000.0
    assert 490.0 < p_inv_40 < 495.0
    assert 1270.0 < p_inv_120 < 1280.0

    els = []
    els.extend(
        header(
            "名字最骗人的水利工程：“正虹吸”翻山越岭 vs “倒虹吸”穿河过谷",
            "“倒虹吸”本质是有压连通器而非真虹吸！右附现代大型场馆“屋面满管虹吸排水”提速奥秘",
        )
    )

    # Top-Left Card: True Siphon (Over-hill n-shape, Tang Tongdian Kewu)
    els.append(card(20, 62, 352, 196))
    els.append(step_badge(40, 84, 1, fg=RED, bg=RED_SOFT))
    els.append(txt(58, 88, "正虹吸（∩ 型翻山）：唐《通典》“渴乌隔山取水”", size=12.5, color=INK, weight="700"))

    # Hill & over-hill pipe
    els.append('<path d="M 42,206 Q 186,100 344,206 Z" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>')
    els.append('<rect x="36" y="176" width="54" height="30" rx="3" fill="#bfdbfe" stroke="#1d6fa5" stroke-width="1.2"/>')
    els.append('<rect x="298" y="192" width="54" height="24" rx="3" fill="#bfdbfe" stroke="#1d6fa5" stroke-width="1.2"/>')
    over_d = "M 64,192 L 64,154 Q 186,88 320,164 L 320,204"
    els.append(f'<path d="{over_d}" fill="none" stroke="#334155" stroke-width="9" stroke-linecap="round"/>')
    els.append(f'<path d="{over_d}" fill="none" stroke="#60a5fa" stroke-width="5" stroke-linecap="round"/>')
    els.append(f'<circle cx="186" cy="126" r="5" fill="{RED}" stroke="#ffffff" stroke-width="1.5"/>')
    els.append(txt(186, 113, f"管顶负表压（+6m 处 ≈ {p_true_top:.0f} kPa）", size=10.8, color=RED, anchor="middle", weight="700", halo=True))
    els.append(txt(36, 226, "• 必须人工引水（唐代竹筒麻漆封裹、筒尾燃松桦干草排气）", size=10.8, color=BODY))
    els.append(txt(36, 244, "• 受 ~10.1 m 气蚀红线限制；管顶一旦漏气立刻断流停摆", size=10.8, color=RED, weight="600"))

    # Bottom-Left Card: Inverted Siphon (Under-valley U-shape, Roman Gier & South-to-North Water Diversion)
    els.append(card(20, 270, 352, 198))
    els.append(step_badge(40, 292, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(58, 296, "倒虹吸（∪ 型穿河）：古罗马引水渠 & 南水北调穿黄", size=12.5, color=INK, weight="700"))

    # Valley & under-river U-conduit
    els.append('<path d="M 38,324 L 112,324 Q 186,412 260,334 L 348,334 L 348,414 L 38,414 Z" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.2"/>')
    # River in middle of valley
    els.append('<path d="M 148,354 Q 186,374 224,354 Z" fill="#bae6fd" stroke="#0284c7" stroke-width="1.2"/>')
    els.append(txt(186, 350, "地上河流/深谷", size=10.5, color=BLUE, anchor="middle", weight="600"))
    under_d = "M 64,324 L 122,386 Q 186,408 250,386 L 318,334"
    els.append(f'<path d="{under_d}" fill="none" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>')
    els.append(f'<path d="{under_d}" fill="none" stroke="#38bdf8" stroke-width="5.5" stroke-linecap="round"/>')
    els.append(f'<circle cx="186" cy="396" r="5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.5"/>')
    els.append(txt(186, 384, f"谷底超高压（深40m ≈ {p_inv_40:.0f} kPa）", size=10.8, color=INK, anchor="middle", weight="700", halo=True))
    els.append(txt(36, 434, "• 实为【有压连通器】：无需抽真空，灌水即靠进出水位差自流", size=10.8, color=BODY))
    els.append(txt(36, 452, f"• 无 10 米限制！里昂古渠深 120 m 谷底承压 {p_inv_120/100:.1f} bar 考验防爆管", size=10.8, color=BLUE, weight="600"))

    # Right Card: Siphonic Roof Drainage vs Conventional Gravity Drainage
    els.append(card(388, 62, 352, 406))
    els.append(step_badge(408, 84, 3, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(426, 88, "现代建筑黑科技：屋面满管虹吸雨水系统", size=13, color=INK, weight="700"))
    els.append(txt(404, 108, "机场航站楼与奥运场馆如何在暴雨中秒排万吨积水？", size=11, color=MUTED))

    # Sub-box A: Traditional Gravity Roof Drainage
    els.append(card(404, 124, 320, 134, rx=8, fill="#f8fafc", stroke=BORDER))
    els.append(txt(418, 145, "传统重力式雨水排水（气水混流·效率低）", size=11.8, color=SLATE, weight="700"))
    # Funnel with vortex air core + sloped wide pipe
    els.append(_line(432, 162, 468, 162, stroke="#64748b", sw=2.0))
    els.append(_line(450, 162, 450, 192, stroke="#64748b", sw=12))
    els.append(_line(450, 192, 690, 214, stroke="#64748b", sw=14))
    els.append(_line(450, 192, 690, 214, stroke="#ffffff", sw=8))  # 2/3 air core!
    els.append(_line(450, 195, 690, 217, stroke="#60a5fa", sw=4))  # 1/3 water at bottom
    els.append(txt(575, 186, "漩涡卷入约 2/3 空气，横管必须留坡度", size=10.8, color=SLATE, anchor="middle"))
    els.append(txt(418, 240, "• 管内常压附壁流，流速慢（~1 m/s），需大量粗立管", size=10.8, color=MUTED))

    # Sub-box B: Siphonic Full-Bore Roof Drainage
    els.append(card(404, 270, 320, 182, rx=8, fill=TEAL_SOFT, stroke="#99f6e4", sw=1.2))
    els.append(txt(418, 291, "虹吸式屋面雨水排水（防漩涡斗·100% 满管负压）", size=11.8, color=TEAL, weight="700"))
    # Anti-vortex baffle cap + horizontal zero-slope pipe + tall vertical drop H!
    els.append('<rect x="432" y="304" width="38" height="7" rx="3" fill="#0f766e"/>')
    els.append(txt(480, 312, "防漩涡挡板隔绝空气", size=10.5, color=TEAL, weight="600"))
    siph_roof_d = "M 451,312 L 451,334 L 682,334 L 682,404"
    els.append(f'<path d="{siph_roof_d}" fill="none" stroke="#1e293b" stroke-width="9" stroke-linejoin="round"/>')
    els.append(f'<path d="{siph_roof_d}" fill="none" stroke="#0d9488" stroke-width="5.2" stroke-linejoin="round"/>')
    els.append(_line(510, 334, 620, 334, stroke="#ffffff", sw=1.6, dash="4 4", marker="arr-teal"))
    els.append(txt(566, 352, "水平悬吊管【零坡度】满流狂飙", size=10.8, color=TEAL, anchor="middle", weight="700"))
    els.append(txt(640, 382, "整栋楼落差 H", size=10.5, color=INK, anchor="end", weight="600"))
    els.append(txt(418, 408, "• 借十几米立管坠落形成强负压抽吸，流速飙至 3–8 m/s", size=10.8, color=BODY))
    els.append(txt(418, 426, "• 管径缩减约 1/3～1/2，悬吊横管零坡度节省顶棚净空，", size=10.8, color=BODY))
    els.append(txt(418, 443, "  但必须精确核算最低负压区，严防管材吸瘪与气蚀震颤。", size=10.8, color=INK, weight="600"))

    return figure(
        485,
        "正虹吸、倒虹吸与现代屋面满管虹吸排水工程对比图",
        "左上展示唐代通典渴乌隔山取水的正虹吸负压结构；左下展示古罗马引水渠与南水北调穿黄倒虹吸的高正压连通器本质；右侧对比传统气水混流重力排水与防漩涡满管负压虹吸屋面排水系统。",
        els,
        extra_defs=_extra_markers(),
    )


@register(TOPIC, "虹吸现象：压强曲线、百年实验论战、气蚀红线与古今工程巧思（5图）", "physics")
def build_all() -> list[str]:
    specs = [
        ("siphon-anatomy-pressure-and-bernoulli", build_siphon_anatomy_and_pressure),
        ("pump-vs-chain-four-extreme-experiments", build_pump_vs_chain_experiments),
        ("cavitation-height-limit-altitude-temperature", build_cavitation_height_limit),
        ("intermittent-siphon-fairness-cup-and-toilet", build_intermittent_siphon_devices),
        ("true-siphon-vs-inverted-siphon-and-roof-drainage", build_true_vs_inverted_and_engineering),
    ]
    built = []
    for name, fn in specs:
        svg = fn()
        write_svg(TOPIC, name, svg)
        built.append(f"assets/images/{TOPIC}/{name}.svg")
    return built
