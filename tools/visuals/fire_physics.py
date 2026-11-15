"""
Visuals for '火为什么向上燃烧，并且火到底是什么？'
(Fire Physics & Chemistry:
1. Faraday Candle Flame 4-Zone Anatomy + Material Nature & Chemi-ionization vs Plasma Scale,
2. Earth 1g Buoyancy Thermal Plume vs Space 0g Spherical Blue Diffusion Flame [1-shot CSS animation],
3. Blue Radical Chemiluminescence [CH*/C2*] vs Yellow Soot Blackbody Radiation & Bunsen Air-Port Control,
4. Buoyant Toroidal Vortex Puffing Frequency Law f ≈ 1.5/√D & Upward vs Downward Match Flame Spread,
5. Einstein Equivalence Forward-Tilting Flame in an Accelerating Jar & Kitchen Stove Flame-Rectification Sensor).

Generates 5 original 760px Chinese SVG diagrams in assets/images/fire-physics/
with verified thermodynamic, plasma-physics, radiation, and fluid-mechanics numerical assertions.
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

TOPIC = "fire-physics"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#d97706"
AMBER_SOFT = "#fffbeb"
DARK_NAVY = "#0f172a"


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


def _markers() -> str:
    return f"""<marker id="arr-ink" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{INK}"/>
  </marker>
  <marker id="arr-blue" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{BLUE}"/>
  </marker>
  <marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{RED}"/>
  </marker>
  <marker id="arr-orange" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{ORANGE}"/>
  </marker>
  <marker id="arr-green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{GREEN}"/>
  </marker>
  <marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{PURPLE}"/>
  </marker>"""


# ---------------------------------------------------------------------------
# 1. Candle Flame 4-Zone Anatomy & Is Fire a Plasma? Quantitative Verdict
# ---------------------------------------------------------------------------
def build_candle_anatomy_and_plasma_scale() -> str:
    p_atm = 101325.0
    kb = 1.380649e-23
    h_planck = 6.62607015e-34
    m_e = 9.1093837e-31
    e_charge = 1.602176634e-19
    eps0 = 8.8541878128e-12

    t_flame = 1673.15  # 1400 C outer reaction sheet
    n0_m3 = p_atm / (kb * t_flame)
    n0_cm3 = n0_m3 * 1e-6
    assert 4.3e18 < n0_cm3 < 4.5e18

    # Saha thermal ionization fraction of O2 (ionization energy 12.07 eV) at 1673 K:
    chi_j = 12.07 * e_charge
    lam_th = h_planck / math.sqrt(2.0 * math.pi * m_e * kb * t_flame)
    saha_rhs = (2.0 / lam_th**3) * math.exp(-chi_j / (kb * t_flame))
    alpha_saha = math.sqrt(saha_rhs / n0_m3)
    assert alpha_saha < 1e-15  # ~1.2e-17 -> thermal ionization is virtually ZERO!

    # Chemi-ionization CH + O -> HCO+ + e- gives n_e ~ 1e10 cm^-3:
    ne_cm3 = 1.0e10
    alpha_chem = ne_cm3 / n0_cm3
    assert 1e-9 < alpha_chem < 5e-9  # ~2.3e-9 (2 parts per billion!)
    debye_um = math.sqrt(eps0 * kb * t_flame / ((ne_cm3 * 1e6) * e_charge**2)) * 1e6
    assert 25.0 < debye_um < 32.0

    defs = (
        _markers()
        + """
  <radialGradient id="grad-luminous" cx="50%" cy="58%" r="52%">
    <stop offset="0%" stop-color="#fffbeb"/>
    <stop offset="55%" stop-color="#fde047"/>
    <stop offset="100%" stop-color="#f97316"/>
  </radialGradient>
  <linearGradient id="grad-outer" x1="0%" y1="100%" x2="0%" y2="0%">
    <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.55"/>
    <stop offset="38%" stop-color="#fb923c" stop-opacity="0.28"/>
    <stop offset="100%" stop-color="#ef4444" stop-opacity="0.18"/>
  </linearGradient>"""
    )

    els = []
    els.extend(
        header(
            "火到底是什么？蜡烛火焰四层解剖与“火是不是等离子体”定量判决",
            "火不是单一物质形态，而是流动的高温气相化学反应区（热气体 + 白炽纳米碳烟 + 十亿分之二化学电离离子）",
        )
    )

    # Left Card: Faraday Candle Anatomy
    els.append(card(20, 62, 364, 424))
    els.append(step_badge(38, 84, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 88, "法拉第蜡烛解剖：固态蜡怎样一步步变成火？", size=12.8, color=INK, weight="700"))

    cx = 122.0
    # Outer veil (Zone 4: ~1400 C)
    els.append(
        f'<path d="M {cx:.1f} 116 C {cx - 56:.1f} 196, {cx - 54:.1f} 286, {cx:.1f} 314 '
        f'C {cx + 54:.1f} 286, {cx + 56:.1f} 196, {cx:.1f} 116 Z" '
        f'fill="url(#grad-outer)" stroke="#f97316" stroke-width="1.3" stroke-dasharray="4 3"/>'
    )
    # Blue radical base (Zone 2: 1200-1400 C)
    els.append(
        f'<path d="M {cx - 34:.1f} 276 C {cx - 38:.1f} 298, {cx - 18:.1f} 315, {cx:.1f} 316 '
        f'C {cx + 18:.1f} 315, {cx + 38:.1f} 298, {cx + 34:.1f} 276 '
        f'C {cx + 22:.1f} 294, {cx - 22:.1f} 294, {cx - 34:.1f} 276 Z" '
        f'fill="#2563eb" fill-opacity="0.72"/>'
    )
    # Luminous soot zone (Zone 3: 1000-1250 C)
    els.append(
        f'<path d="M {cx:.1f} 138 C {cx - 38:.1f} 204, {cx - 36:.1f} 274, {cx:.1f} 302 '
        f'C {cx + 36:.1f} 274, {cx + 38:.1f} 204, {cx:.1f} 138 Z" '
        f'fill="url(#grad-luminous)" stroke="#ea580c" stroke-width="1.2"/>'
    )
    # Dark inner vapor core (Zone 1: 300-600 C)
    els.append(
        f'<path d="M {cx:.1f} 234 C {cx - 17:.1f} 264, {cx - 16:.1f} 294, {cx:.1f} 306 '
        f'C {cx + 16:.1f} 294, {cx + 17:.1f} 264, {cx:.1f} 234 Z" '
        f'fill="#1e293b" fill-opacity="0.82"/>'
    )

    # Candle body + concave melted wax cup + capillary wick
    els.append(f'<rect x="{cx - 34:.1f}" y="330" width="68" height="92" rx="5" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.6"/>')
    els.append(
        f'<path d="M {cx - 34:.1f} 330 Q {cx:.1f} 342 {cx + 34:.1f} 330 L {cx + 30:.1f} 340 Q {cx:.1f} 348 {cx - 30:.1f} 340 Z" '
        f'fill="#fde68a" stroke="#d97706" stroke-width="1.1"/>'
    )
    els.append(f'<path d="M {cx:.1f} 338 L {cx:.1f} 286 Q {cx + 3:.1f} 276 {cx + 7:.1f} 272" fill="none" stroke="#334155" stroke-width="3.2" stroke-linecap="round"/>')
    els.append(_line(cx, 326, cx, 294, stroke=AMBER, sw=1.4, dash="2 2", marker="arr-orange"))
    els.append(txt(cx, 366, "固态石蜡", size=11, color=SLATE, anchor="middle", weight="600"))
    els.append(txt(cx, 384, "（本身不直接烧）", size=10, color=MUTED, anchor="middle"))

    # Callout lines to right side of Left Card (x=192..372)
    callouts = [
        (cx + 26, 152, 190, 124, RED, "④ 外焰薄壳（~1400°C 最烫）", "氧气充足，完全生成 CO₂ + H₂O"),
        (cx + 22, 208, 190, 178, ORANGE, "③ 亮黄内焰（1000–1250°C）", "纳米碳烟白炽热辐射（含瞬生金刚石）"),
        (cx + 8, 266, 190, 232, INK, "① 暗区焰心（300–600°C）", "刚汽化的石蜡烷烃蒸气，缺氧未燃"),
        (cx + 26, 298, 190, 286, BLUE, "② 蓝光底座（1200–1400°C）", "CH* / C₂* 自由基跃迁发出化学蓝光"),
        (cx + 28, 336, 190, 340, AMBER, "液态蜡碗 + 烛芯毛细抽吸", "上升冷气流冷却外沿，毛细力往上送油"),
    ]
    for x0, y0, x1, y1, col, t1, t2 in callouts:
        els.append(_line(x0, y0, x1 - 4, y1 - 3, stroke=col, sw=1.2))
        els.append(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="2.8" fill="{col}"/>')
        els.append(txt(x1, y1, t1, size=10.8, color=col, weight="700"))
        els.append(txt(x1, y1 + 15, t2, size=10.0, color=BODY))

    els.append(card(34, 404, 336, 68, rx=8, fill=ORANGE_SOFT, stroke="#fdba74", sw=1.0))
    els.append(txt(46, 423, "圣安德鲁斯大学实测彩蛋（Su & Zhou, 2011）：", size=11, color=ORANGE, weight="700"))
    els.append(txt(46, 441, "亮黄内焰每秒诞生约 150 万颗纳米金刚石微粒（连同石墨、富勒", size=10.3, color=BODY))
    els.append(txt(46, 458, "烯与无定形碳），但不到一眨眼就在外焰被烧成二氧化碳！", size=10.3, color=BODY))

    # Right Card: Is Fire a Plasma? Log10 Ionization Fraction Scale
    els.append(card(396, 62, 344, 424))
    els.append(step_badge(414, 84, 2, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(432, 88, "辟谣与深究：日常火焰算“等离子体”吗？", size=12.8, color=INK, weight="700"))

    els.append(txt(412, 114, "电离度 α = 自由电子数 nₑ ÷ 中性气体分子总数 n₀（对数标尺）", size=10.5, color=MUTED))

    # Horizontal log10 scale from 10^-18 to 10^0
    sx0, sx1 = 420.0, 718.0
    sy_bar = 158.0

    def lx(log_a: float) -> float:
        return sx0 + ((log_a + 18.0) / 18.0) * (sx1 - sx0)

    # Background zones on bar
    x_weak = lx(-6.0)
    els.append(f'<rect x="{sx0:.1f}" y="{sy_bar - 10:.1f}" width="{x_weak - sx0:.1f}" height="20" rx="4" fill="{BLUE_SOFT}" stroke="{BLUE_LINE}"/>')
    els.append(f'<rect x="{x_weak:.1f}" y="{sy_bar - 10:.1f}" width="{sx1 - x_weak:.1f}" height="20" rx="4" fill="{PURPLE_SOFT}" stroke="#d8b4fe"/>')
    els.append(txt((sx0 + x_weak) / 2, sy_bar - 16, "中性／极弱电离气体区", size=10.2, color=BLUE, anchor="middle", weight="600"))
    els.append(txt((x_weak + sx1) / 2, sy_bar - 16, "典型等离子体区", size=10.2, color=PURPLE, anchor="middle", weight="700"))

    for exp_v in [-18, -14, -10, -6, -2, 0]:
        px = lx(float(exp_v))
        els.append(_line(px, sy_bar + 10, px, sy_bar + 15, stroke=SLATE, sw=1.2))
        lbl = "1" if exp_v == 0 else f"10^{exp_v}"
        els.append(txt(px, sy_bar + 28, lbl, size=9.8, color=MUTED, anchor="middle", cls="mono"))

    # Markers on scale
    pts_ion = [
        (-16.9, "1400°C 纯热电离理论值", "萨哈方程 α ≈ 10⁻¹⁷（热碰撞根本撞不出电子！）", SLATE, 212),
        (-8.64, "蜡烛／木柴／燃气灶真实火焰", "化学电离 CH + O → HCO⁺ + e⁻，α ≈ 2×10⁻⁹", ORANGE, 260),
        (-4.8, "氧-乙炔焊枪超高温焰（~3100°C）", "热电离开始显著介入，步入弱电离等离子体门槛", RED, 308),
        (-0.5, "闪电通道／电弧焊／太阳日冕", "α ≈ 0.1–1.0，集体电磁屏蔽主导的标准等离子体", PURPLE, 356),
    ]
    for log_v, title_p, desc_p, col, card_y in pts_ion:
        px = lx(log_v)
        els.append(f'<circle cx="{px:.1f}" cy="{sy_bar:.1f}" r="4.8" fill="{col}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(card(412, card_y - 16, 312, 40, rx=6, fill="#ffffff", stroke=BORDER, sw=1.0))
        els.append(f'<rect x="{412}" y="{card_y - 16}" width="5" height="40" rx="2" fill="{col}"/>')
        els.append(txt(424, card_y - 1, title_p, size=10.8, color=col, weight="700"))
        els.append(txt(424, card_y + 15, desc_p, size=10.0, color=BODY))

    els.append(card(412, 392, 312, 80, rx=8, fill=PURPLE_SOFT, stroke="#d8b4fe", sw=1.0))
    els.append(txt(424, 411, "一句话定性日常火焰：", size=11.2, color=PURPLE, weight="700"))
    els.append(txt(424, 429, "普通火不是第四态热等离子体，而是十亿分子里混着约 2 个化学", size=10.3, color=BODY))
    els.append(txt(424, 446, "离子的【发光高温反应气流】——虽算不上标准等离子体，却已比空", size=10.3, color=BODY))
    els.append(txt(424, 463, "气导电百万倍，足够被高压电场掰弯，也能触发燃气灶离子保护针！", size=10.3, color=BODY))

    return figure(
        505,
        "蜡烛火焰四层结构解剖与火焰电离度定量对比图",
        "左图展示固态石蜡熔化、烛芯毛细上升与暗区、蓝光底座、亮黄碳烟层、高温外焰四层结构；右图通过萨哈方程与化学电离实测标尺说明日常火焰电离度仅约十亿分之二，属于弱电离反应气流而非典型热等离子体。",
        els,
        extra_defs=defs,
    )


# ---------------------------------------------------------------------------
# 2. Earth 1g Buoyancy Plume vs Space 0g Spherical Blue Flame (with 1-shot CSS animation)
# ---------------------------------------------------------------------------
def build_earth_vs_space_flame() -> str:
    g = 9.80665
    t_amb = 293.15   # 20 C
    t_hot = 1500.0   # ~1227 C mean buoyant plume zone
    rho_amb = 1.204  # kg/m^3
    rho_hot = rho_amb * (t_amb / t_hot)
    ratio_rho = rho_amb / rho_hot
    assert 5.0 < ratio_rho < 5.2

    a_buoy_g = ratio_rho - 1.0
    assert 4.0 < a_buoy_g < 4.2  # ~4.12 g upward acceleration!

    z_flame = 0.04  # 4 cm candle flame height
    u_ideal = math.sqrt(2.0 * g * (1.0 - rho_hot / rho_amb) * z_flame)
    assert 0.75 < u_ideal < 0.85  # ~0.80 m/s upward plume speed!

    css = """
  @keyframes risePlume {
    0%   { stroke-dashoffset: 220; opacity: 0.25; }
    20%  { opacity: 0.95; }
    100% { stroke-dashoffset: 0; opacity: 0.95; }
  }
  @keyframes diffuseSphere {
    0%   { stroke-dashoffset: 90; opacity: 0.25; }
    25%  { opacity: 0.95; }
    100% { stroke-dashoffset: 0; opacity: 0.95; }
  }
  .anim-plume {
    stroke-dasharray: 8 10;
    stroke-dashoffset: 220;
    animation: risePlume 2.8s cubic-bezier(0.22, 0.61, 0.36, 1) 1 forwards;
  }
  .anim-diff {
    stroke-dasharray: 6 8;
    stroke-dashoffset: 90;
    animation: diffuseSphere 2.8s ease-out 1 forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .anim-plume, .anim-diff {
      animation: none !important;
      stroke-dashoffset: 0 !important;
      opacity: 0.95 !important;
    }
  }"""

    defs = (
        _markers()
        + """
  <radialGradient id="grad-space-blue" cx="50%" cy="55%" r="50%">
    <stop offset="0%" stop-color="#e0f2fe" stop-opacity="0.95"/>
    <stop offset="55%" stop-color="#38bdf8" stop-opacity="0.78"/>
    <stop offset="88%" stop-color="#2563eb" stop-opacity="0.65"/>
    <stop offset="100%" stop-color="#1d4ed8" stop-opacity="0.0"/>
  </radialGradient>
  <linearGradient id="grad-earth-tear" x1="0%" y1="100%" x2="0%" y2="0%">
    <stop offset="0%" stop-color="#2563eb"/>
    <stop offset="22%" stop-color="#f97316"/>
    <stop offset="68%" stop-color="#fde047"/>
    <stop offset="100%" stop-color="#fef9c3"/>
  </linearGradient>"""
    )

    els = []
    els.extend(
        header(
            "火为什么偏偏向上烧？地球 1g“浮力烟囱” vs 太空 0g“蓝色圆球”",
            "火本身没有方向！是重力让沉重冷空气下沉挤压、把轻了 5 倍的热燃气向上拔成了尖尖的泪滴",
        )
    )

    # Left Card: Earth 1g Buoyant Convection
    els.append(card(20, 62, 352, 424))
    els.append(step_badge(38, 84, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 88, "地球表面（1g 重力场）：自然对流拔尖拉长", size=12.8, color=INK, weight="700"))

    ex = 186.0
    # Rising invisible hot plume envelope
    els.append(
        f'<path d="M {ex - 54:.1f} 310 Q {ex - 30:.1f} 240 {ex - 26:.1f} 118 L {ex + 26:.1f} 118 Q {ex + 30:.1f} 240 {ex + 54:.1f} 310 Z" '
        f'fill="#fff7ed" stroke="#fed7aa" stroke-width="1.2" stroke-dasharray="4 3"/>'
    )
    # Animated rising thermal plume streamlines
    els.append(
        f'<path d="M {ex - 64:.1f} 312 Q {ex - 30:.1f} 296 {ex - 20:.1f} 224 L {ex - 16:.1f} 112" '
        f'fill="none" stroke="{ORANGE}" stroke-width="2.2" class="anim-plume" marker-end="url(#arr-orange)"/>'
    )
    els.append(
        f'<path d="M {ex + 64:.1f} 312 Q {ex + 30:.1f} 296 {ex + 20:.1f} 224 L {ex + 16:.1f} 112" '
        f'fill="none" stroke="{ORANGE}" stroke-width="2.2" class="anim-plume" marker-end="url(#arr-orange)"/>'
    )
    els.append(_line(ex, 160, ex, 108, stroke=RED, sw=2.2, marker="arr-red"))

    # Teardrop flame + candle
    els.append(
        f'<path d="M {ex:.1f} 168 C {ex - 32:.1f} 222, {ex - 30:.1f} 280, {ex:.1f} 304 '
        f'C {ex + 30:.1f} 280, {ex + 32:.1f} 222, {ex:.1f} 168 Z" '
        f'fill="url(#grad-earth-tear)" stroke="#ea580c" stroke-width="1.2"/>'
    )
    els.append(f'<rect x="{ex - 24:.1f}" y="316" width="48" height="46" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>')
    els.append(_line(ex, 316, ex, 294, stroke="#334155", sw=3.0))

    # Cold heavy air lateral entrainment arrows
    els.append(_line(54, 292, 128, 292, stroke=BLUE, sw=2.0, marker="arr-blue"))
    els.append(_line(318, 292, 244, 292, stroke=BLUE, sw=2.0, marker="arr-blue"))
    els.append(txt(42, 278, "重冷空气下沉补氧", size=10.5, color=BLUE, weight="700"))
    els.append(txt(42, 310, f"ρ₀ ≈ {rho_amb:.2f} kg/m³", size=10.2, color=MUTED, cls="mono"))
    els.append(txt(244, 278, "横向夹带收拢底座", size=10.5, color=BLUE, weight="700"))

    els.append(txt(ex + 30, 134, "热羽流飙至 ~0.8 m/s", size=10.8, color=RED, weight="700"))
    els.append(txt(ex + 30, 151, f"高温燃气 ρ_f ≈ {rho_hot:.2f} kg/m³", size=10.0, color=BODY, cls="mono"))
    els.append(txt(ex - 34, 198, "碳烟被热流", size=10.3, color=ORANGE, anchor="end", weight="600"))
    els.append(txt(ex - 34, 213, "裹挟向上烧亮", size=10.3, color=ORANGE, anchor="end", weight="600"))

    # Physics summary box on Earth side
    els.append(card(34, 372, 324, 100, rx=8, fill=ORANGE_SOFT, stroke="#fdba74", sw=1.0))
    els.append(txt(46, 392, f"阿基米德浮力账本（温度暴涨 5 倍 → 密度剩 1/5）：", size=11, color=INK, weight="700"))
    els.append(txt(46, 411, f"• 向上净浮力加速度 a = g(T_f/T₀ − 1) ≈ {a_buoy_g:.1f}g（约 40 m/s²）", size=10.4, color=BODY))
    els.append(txt(46, 429, "• 底部源源不断卷入氧气，燃烧猛烈、碳烟多、火焰呈亮黄色；", size=10.4, color=BODY))
    els.append(txt(46, 447, "• 上升气流收束火苗腰身，在顶端交汇削出尖锐“泪滴锥形”。", size=10.4, color=BODY))
    els.append(txt(46, 464, "• 地面同款蜡烛寿命：约 10 分钟迅速烧完。", size=10.4, color=ORANGE, weight="700"))

    # Right Card: Microgravity 0g Spherical Diffusion Flame (NASA Mir & ISS)
    els.append(card(388, 62, 352, 424, fill="#0f172a", stroke="#334155"))
    els.append(step_badge(406, 84, 2, fg="#38bdf8", bg="#1e293b"))
    els.append(txt(424, 88, "太空微重力（0g 空间站）：静谧的淡蓝圆球", size=12.8, color="#f8fafc", weight="700"))

    sx_c, sy_c = 564.0, 238.0
    # Spherical blue glow
    els.append(f'<circle cx="{sx_c:.1f}" cy="{sy_c:.1f}" r="54" fill="url(#grad-space-blue)"/>')
    els.append(f'<circle cx="{sx_c:.1f}" cy="{sy_c:.1f}" r="42" fill="none" stroke="#7dd3fc" stroke-width="1.8" stroke-dasharray="4 3"/>')
    els.append(f'<circle cx="{sx_c:.1f}" cy="{sy_c:.1f}" r="16" fill="#0f172a" fill-opacity="0.72"/>')

    # Candle in space
    els.append(f'<rect x="{sx_c - 22:.1f}" y="286" width="44" height="68" rx="4" fill="#cbd5e1" stroke="#64748b" stroke-width="1.4"/>')
    els.append(_line(sx_c, 286, sx_c, 244, stroke="#475569", sw=3.2))

    # Isotropic 360-degree radial diffusion arrows (inward O2, outward CO2/H2O)
    for deg in [35, 90, 145, 205, 335]:
        rad = math.radians(deg)
        r_out, r_in = 88.0, 50.0
        x_start = sx_c + r_out * math.cos(rad)
        y_start = sy_c - r_out * math.sin(rad)
        x_end = sx_c + r_in * math.cos(rad)
        y_end = sy_c - r_in * math.sin(rad)
        els.append(_line(x_start, y_start, x_end, y_end, stroke="#38bdf8", sw=1.8, cls="anim-diff", marker="arr-blue"))

    els.append(txt(sx_c, 132, "360° 各向同性分子慢扩散供氧（O₂）", size=10.8, color="#7dd3fc", anchor="middle", weight="700"))
    els.append(txt(sx_c + 56, 236, "直径 ≈ 1.5 cm", size=10.8, color="#bae6fd", weight="700"))
    els.append(txt(sx_c + 56, 253, "无碳烟 · 纯蓝色", size=10.3, color="#94a3b8"))

    # Space findings summary box
    els.append(card(402, 372, 324, 100, rx=8, fill="#1e293b", stroke="#334155", sw=1.0))
    els.append(txt(414, 392, "NASA 和平号与国际空间站实测（Dietrich 等，2001/2012）：", size=10.8, color="#38bdf8", weight="700"))
    els.append(txt(414, 411, "• g = 0 时热空气不再上升！冷热气体不分轻重，浮力对流彻底归零；", size=10.3, color="#e2e8f0"))
    els.append(txt(414, 429, "• 氧气仅靠菲克分子扩散均匀渗入，火焰完美呈球冠／球形且不闪烁；", size=10.3, color="#e2e8f0"))
    els.append(txt(414, 447, "• 慢速充分氧化不生碳烟，黄光消失只剩自由基蓝光，最长慢烧 45 分钟；", size=10.3, color="#e2e8f0"))
    els.append(txt(414, 464, "• 液滴熄灭后甚至能转为 600–800 K 肉眼看不见的“隐形冷焰”！", size=10.3, color="#fde047", weight="600"))

    return figure(
        505,
        "地球重力对流泪滴火焰与太空微重力球形蓝色火焰对比图",
        "左图展示地球1g重力下密度降低5倍的高温燃气产生约4.1g浮力加速度，拉出向上泪滴形黄火；右图展示太空微重力下浮力消失，仅靠360度各向同性分子扩散形成1.5厘米无碳烟淡蓝色球形火焰。",
        els,
        extra_css=css,
        extra_defs=defs,
    )


# ---------------------------------------------------------------------------
# 3. Blue Radical Chemiluminescence vs Yellow Soot Blackbody & Bunsen Air Control
# ---------------------------------------------------------------------------
def build_blue_vs_yellow_spectra() -> str:
    # Planck spectral radiance B_lambda(lam, T) relative curve & Wien peak check
    b_wien = 2897.77  # um * K
    t_soot = 1450.0   # K (~1177 C luminous soot)
    lam_peak_um = b_wien / t_soot
    assert 1.95 < lam_peak_um < 2.05  # peaks at 2.00 um in the Near-Infrared!

    def planck_rel(lam_nm: float, temp_k: float) -> float:
        lam_m = lam_nm * 1e-9
        c2 = 1.438776877e-2  # hc / k_B (m*K)
        val = 1.0 / ((lam_m**5) * (math.exp(c2 / (lam_m * temp_k)) - 1.0))
        return val

    # Normalize soot blackbody across 380..760 nm to [0, 1] at 760 nm
    p_max = planck_rel(760.0, t_soot)
    assert planck_rel(450.0, t_soot) / p_max < 0.05  # negligible blue, steep rise to yellow/orange/red!

    els = []
    els.extend(
        header(
            "为什么燃气灶是蓝火、蜡烛篝火是黄火？两种截然不同的发光物理",
            "黄光是纳米固体碳粒的“连续黑体热辐射”，蓝光是 CH* 与 C₂* 自由基的“量子跃迁化学发光”",
        )
    )

    # Left Card: Spectral comparison 380 - 760 nm
    els.append(card(20, 62, 364, 404))
    els.append(step_badge(38, 84, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 88, "可见光谱对决：离散分子谱线 vs 连续黑体尾翼", size=12.6, color=INK, weight="700"))

    gx0, gx1 = 62.0, 362.0
    gy_top, gy_bot = 124.0, 310.0

    def wx(nm: float) -> float:
        return gx0 + ((nm - 380.0) / (760.0 - 380.0)) * (gx1 - gx0)

    def wy(norm_y: float) -> float:
        return gy_bot - norm_y * (gy_bot - gy_top)

    # Visible color strip along x-axis
    bands = [
        (380, 440, "#8b5cf6"),
        (440, 490, "#2563eb"),
        (490, 560, "#10b981"),
        (560, 595, "#eab308"),
        (595, 635, "#f97316"),
        (635, 760, "#ef4444"),
    ]
    for b0, b1, bcol in bands:
        els.append(
            f'<rect x="{wx(b0):.1f}" y="{gy_bot:.1f}" width="{wx(b1) - wx(b0):.1f}" height="6" fill="{bcol}" opacity="0.8"/>'
        )

    for yv in [0.0, 0.5, 1.0]:
        py = wy(yv)
        els.append(_line(gx0, py, gx1, py, stroke="#e2e8f0", sw=1.0))
    els.append(txt(gx0 - 6, wy(1.0) + 4, "强", size=10, color=MUTED, anchor="end"))
    els.append(txt(gx0 - 6, wy(0.0) + 4, "0", size=10, color=MUTED, anchor="end", cls="mono"))

    for nm_tick in [400, 470, 550, 630, 700, 760]:
        px = wx(float(nm_tick))
        els.append(_line(px, gy_bot + 6, px, gy_bot + 10, stroke=SLATE, sw=1.1))
        els.append(txt(px, gy_bot + 22, f"{nm_tick}", size=9.8, color=MUTED, anchor="middle", cls="mono"))
    els.append(txt((gx0 + gx1) / 2, gy_bot + 38, "波长 λ (nm) — 右侧 >780 nm 进入红外热辐射主峰区", size=10.2, color=MUTED, anchor="middle"))

    els.append(_line(gx0, gy_top, gx0, gy_bot, stroke=SLATE, sw=1.3))
    els.append(_line(gx0, gy_bot, gx1, gy_bot, stroke=SLATE, sw=1.3))

    # Soot Planck blackbody curve (1450 K)
    soot_pts = [(nm, planck_rel(float(nm), t_soot) / p_max) for nm in range(380, 764, 6)]
    soot_poly = " ".join(f"{wx(nm):.1f},{wy(v):.1f}" for nm, v in soot_pts)
    soot_area = f"{wx(380):.1f},{gy_bot:.1f} " + soot_poly + f" {wx(760):.1f},{gy_bot:.1f}"
    els.append(f'<polygon points="{soot_area}" fill="#fed7aa" fill-opacity="0.45"/>')
    els.append(f'<polyline points="{soot_poly}" fill="none" stroke="{ORANGE}" stroke-width="2.6"/>')

    # Radical chemiluminescence spectrum: CH* (431.5 nm), C2* Swan bands (473.7, 516.5, 563.5 nm)
    def radical_spec(nm: float) -> float:
        peaks = [
            (431.5, 0.92, 5.5),   # CH* violet-blue
            (473.7, 0.62, 5.0),   # C2* blue-cyan
            (516.5, 0.85, 5.5),   # C2* Swan main cyan-green band
            (563.5, 0.24, 6.0),   # C2* weak yellow-green band
        ]
        return min(1.0, sum(amp * math.exp(-0.5 * ((nm - mu) / sig) ** 2) for mu, amp, sig in peaks) + 0.02)

    rad_pts = [(nm, radical_spec(float(nm))) for nm in range(380, 762, 2)]
    rad_poly = " ".join(f"{wx(nm):.1f},{wy(v):.1f}" for nm, v in rad_pts)
    els.append(f'<polyline points="{rad_poly}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')

    # Peak labels with zero overlap
    els.append(txt(wx(431.5), wy(0.92) - 8, "CH* (431 nm)", size=10.2, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(wx(516.5) + 4, wy(0.85) - 8, "C₂* 斯旺带 (516 nm)", size=10.2, color=TEAL, anchor="start", weight="700"))
    els.append(txt(wx(712), wy(0.58), "1450 K 碳烟黑体辐射", size=10.5, color=ORANGE, anchor="end", weight="700"))
    els.append(txt(wx(712), wy(0.49), "（98% 能量在红外区！）", size=9.8, color=RED, anchor="end"))

    els.append(card(34, 360, 336, 92, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE, sw=1.0))
    els.append(txt(46, 380, "为什么隔着一米烤篝火，脸还没碰到火就觉得烫？", size=11, color=INK, weight="700"))
    els.append(txt(46, 398, f"按维恩位移定律，1450 K 碳烟辐射峰值在近红外 {lam_peak_um:.2f} μm！", size=10.3, color=BODY))
    els.append(txt(46, 415, "热空气虽全部向上飞走，但纳米碳烟像无数微型红外浴霸灯，以", size=10.3, color=BODY))
    els.append(txt(46, 432, "光速向四面八方直线发射红外线；纯氢／甲醇无碳烟火反而辐射弱。", size=10.3, color=BODY))

    # Right Card: Diffusion vs Premixed (Kitchen Stove / Bunsen Burner) + Temperature Myth
    els.append(card(396, 62, 344, 404))
    els.append(step_badge(414, 84, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(432, 88, "灶台风门一调，黄火秒变蓝火的秘密", size=12.6, color=INK, weight="700"))

    # Sub-box A: Closed air port -> Diffusion yellow smoky flame
    els.append(card(412, 108, 150, 214, rx=8, fill="#fffbeb", stroke="#fcd34d"))
    els.append(txt(487, 128, "① 扩散火焰（风门堵死）", size=10.8, color=ORANGE, anchor="middle", weight="700"))
    els.append(
        '<path d="M 487 142 C 463 176, 465 212, 487 228 C 509 212, 511 176, 487 142 Z" '
        'fill="#facc15" stroke="#ea580c" stroke-width="1.3"/>'
    )
    els.append('<rect x="475" y="228" width="24" height="34" rx="2" fill="#64748b"/>')
    els.append(txt(487, 278, "先出气、再找氧", size=10.5, color=INK, anchor="middle", weight="600"))
    els.append(txt(487, 295, "缺氧裂解出碳烟 · 熏黑锅底", size=9.8, color=BODY, anchor="middle"))
    els.append(txt(487, 311, "生成一氧化碳 · 约 1200°C", size=9.8, color=RED, anchor="middle", weight="600"))

    # Sub-box B: Open air port -> Premixed blue clean flame
    els.append(card(574, 108, 150, 214, rx=8, fill="#eff6ff", stroke="#93c5fd"))
    els.append(txt(649, 128, "② 预混火焰（风门打开）", size=10.8, color=BLUE, anchor="middle", weight="700"))
    els.append(
        '<path d="M 649 156 C 631 186, 633 214, 649 228 C 665 214, 667 186, 649 156 Z" '
        'fill="#60a5fa" fill-opacity="0.55" stroke="#2563eb" stroke-width="1.3"/>'
    )
    els.append(
        '<path d="M 649 184 L 638 228 L 660 228 Z" fill="#38bdf8" stroke="#0284c7" stroke-width="1.2"/>'
    )
    els.append('<rect x="637" y="228" width="24" height="34" rx="2" fill="#64748b"/>')
    els.append('<circle cx="649" cy="248" r="4.2" fill="#eff6ff" stroke="#1d4ed8" stroke-width="1.2"/>')
    els.append(txt(649, 278, "管内先混足氧气再烧", size=10.5, color=INK, anchor="middle", weight="600"))
    els.append(txt(649, 295, "碳烟零生成 · 只剩自由基光", size=9.8, color=BODY, anchor="middle"))
    els.append(txt(649, 311, "双锥烈焰 · 1750–1950°C", size=9.8, color=BLUE, anchor="middle", weight="700"))

    # Warning box on "Blue is always hotter" myth
    els.append(card(412, 334, 312, 118, rx=8, fill=RED_SOFT, stroke="#fecaca", sw=1.0))
    els.append(txt(424, 354, "破除误区：“蓝火一定比黄火白火温度高”？不一定！", size=11, color=RED, weight="700"))
    els.append(txt(424, 373, "• 只有同属【黑体热辐射】（如铁水、恒星）时，颜色越偏蓝白才越热；", size=10.2, color=BODY))
    els.append(txt(424, 391, "• 燃气灶蓝火比蜡烛黄火热，是因为【预混供氧充分、无散热碳烟】；", size=10.2, color=BODY))
    els.append(txt(424, 409, "• 反例：空间站微重力“冷焰”也泛微弱蓝光，温度却仅 300–500°C，", size=10.2, color=BODY))
    els.append(txt(424, 427, "  而氧-乙炔焰掺碳白炽区（>2500°C）比普通酒精灯蓝焰烫得多！", size=10.2, color=BODY))

    return figure(
        485,
        "火焰蓝光与黄光光谱机制及扩散预混火焰对比图",
        "左图对比1450K纳米碳烟连续普朗克黑体辐射曲线与CH*、C2*自由基离散化学发光谱峰；右图展示灶台风门开闭对应的扩散黄火与预混蓝火，并澄清火焰颜色与温度的对应条件。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. Puffing Vortex Frequency Law f ≈ 1.5/√D & Upward vs Downward Match Spread
# ---------------------------------------------------------------------------
def build_puffing_and_match_spread() -> str:
    g = 9.80665

    # Cetegen & Ahmed (1993) / Xia & Zhang (2018 JFM): f = 0.48 * sqrt(g / D) ≈ 1.503 / sqrt(D)
    def f_puff(d_m: float) -> float:
        return 0.48 * math.sqrt(g / d_m)

    f_candle = f_puff(0.02)
    f_camp = f_puff(0.25)
    f_bonfire = f_puff(1.00)
    f_pool = f_puff(9.00)
    assert 10.4 < f_candle < 10.8
    assert 2.95 < f_camp < 3.06
    assert 1.48 < f_bonfire < 1.53
    assert 0.49 < f_pool < 0.52

    els = []
    els.extend(
        header(
            "浮力制造的两大奇观：篝火“呼呼”跳动定律与火柴倒拿狂烧之谜",
            "小火苗安静稳定，大火堆却按 f ≈ 1.5/√D 周期脱落环形涡流；顺着浮力方向更会让火势暴涨数倍",
        )
    )

    # Left Card: Puffing Frequency Law f ≈ 1.5 / sqrt(D)
    els.append(card(20, 62, 368, 412))
    els.append(step_badge(38, 84, 1, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 88, "为什么篝火总是一跳一跳？浮力涡环脱落定律", size=12.6, color=INK, weight="700"))

    px0, px1 = 68.0, 362.0
    py_top, py_bot = 124.0, 306.0

    # Log10(D) from -2 (0.01 m) to +1 (10 m); y from 0 to 12 Hz
    def dx_map(d_m: float) -> float:
        return px0 + ((math.log10(d_m) + 2.0) / 3.0) * (px1 - px0)

    def fy_map(f_hz: float) -> float:
        return py_bot - (f_hz / 12.5) * (py_bot - py_top)

    for fv in [0, 3, 6, 9, 12]:
        gy = fy_map(float(fv))
        els.append(_line(px0, gy, px1, gy, stroke="#e2e8f0", sw=1.0))
        els.append(txt(px0 - 6, gy + 4, f"{fv}Hz", size=9.8, color=MUTED, anchor="end", cls="mono"))

    for dm, dlbl in [(0.01, "1cm"), (0.1, "10cm"), (1.0, "1m"), (10.0, "10m")]:
        gx = dx_map(dm)
        els.append(_line(gx, py_bot, gx, py_bot + 4, stroke=SLATE, sw=1.1))
        els.append(txt(gx, py_bot + 17, dlbl, size=9.8, color=MUTED, anchor="middle", cls="mono"))
    els.append(txt((px0 + px1) / 2, py_bot + 34, "火源底部直径 D（对数坐标）", size=10.2, color=MUTED, anchor="middle"))

    els.append(_line(px0, py_top, px0, py_bot, stroke=SLATE, sw=1.3))
    els.append(_line(px0, py_bot, px1, py_bot, stroke=SLATE, sw=1.3))

    pts = []
    for i in range(61):
        d_val = 10.0 ** (-1.85 + (2.85 * i / 60.0))
        pts.append((d_val, f_puff(d_val)))
    poly = " ".join(f"{dx_map(d):.1f},{fy_map(f):.1f}" for d, f in pts)
    els.append(f'<polyline points="{poly}" fill="none" stroke="{PURPLE}" stroke-width="2.6"/>')

    marks = [
        (0.02, f_candle, f"并排蜡烛 (2cm): {f_candle:.1f} Hz", 8, 4, "start", ORANGE),
        (0.25, f_camp, f"露营篝火 (25cm): {f_camp:.1f} Hz", 8, -7, "start", RED),
        (1.00, f_bonfire, f"大型篝火 (1m): {f_bonfire:.1f} Hz", -6, -9, "end", PURPLE),
        (9.00, f_pool, f"油池大火 (9m): {f_pool:.1f} Hz", -4, -10, "end", INK),
    ]
    for dm, fv, lbl, ox, oy, anch, col in marks:
        mx, my = dx_map(dm), fy_map(fv)
        els.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="4.2" fill="{col}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(mx + ox, my + oy, lbl, size=10.0, color=col, anchor=anch, weight="700"))

    els.append(card(34, 354, 340, 106, rx=8, fill=PURPLE_SOFT, stroke="#d8b4fe", sw=1.0))
    els.append(txt(46, 374, "Cetegen & Ahmed 定律：f ≈ 0.48√(g/D) ≈ 1.5/√D", size=11, color=PURPLE, weight="700"))
    els.append(txt(46, 393, "• 热羽流加速上升剪切外围冷空气，卷出一圈圈“甜甜圈”环形涡流；", size=10.2, color=BODY))
    els.append(txt(46, 411, "• 涡环每爬升约 1 个火源直径就饱和脱落，把火舌掐脖子向上抛断；", size=10.2, color=BODY))
    els.append(txt(46, 429, "• 单支蜡烛极稳，但三支蜡烛紧挨凑成 2 cm 火源就会每秒同步狂闪", size=10.2, color=BODY))
    els.append(txt(46, 446, "  约 10 次！直径越大的巨型火场，火球吞吐反而越慢越深沉。", size=10.2, color=BODY))

    # Right Card: Upward vs Downward Match & Mountain/Stairwell Chimney Effect
    els.append(card(402, 62, 338, 412))
    els.append(step_badge(420, 84, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(438, 88, "顺浮力 vs 逆浮力：一根火柴看懂火场生死法则", size=12.4, color=INK, weight="700"))

    # Sub-panel 1: Match head UP (slow downward spread)
    els.append(card(418, 108, 146, 224, rx=8, fill="#f8fafc", stroke=BORDER))
    els.append(txt(491, 128, "A. 火柴头朝上（逆流慢烧）", size=10.6, color=TEAL, anchor="middle", weight="700"))
    els.append(_line(491, 158, 491, 136, stroke=ORANGE, sw=1.8, marker="arr-orange"))
    els.append(
        '<path d="M 491 164 C 478 184, 480 206, 491 214 C 502 206, 504 184, 491 164 Z" '
        'fill="#fde047" stroke="#ea580c" stroke-width="1.2"/>'
    )
    els.append('<rect x="487" y="212" width="8" height="72" rx="2" fill="#fde68a" stroke="#b45309" stroke-width="1.2"/>')
    els.append('<ellipse cx="491" cy="212" rx="5.5" ry="7" fill="#334155"/>')
    els.append(txt(491, 300, "热羽流飞向空中", size=10.2, color=TEAL, anchor="middle", weight="600"))
    els.append(txt(491, 317, "下方木杆冷，常半途自熄", size=9.8, color=MUTED, anchor="middle"))

    # Sub-panel 2: Match head DOWN (rapid upward engulfing spread!)
    els.append(card(578, 108, 146, 224, rx=8, fill=RED_SOFT, stroke="#fca5a5"))
    els.append(txt(651, 128, "B. 火柴头朝下（顺流猛蹿）", size=10.6, color=RED, anchor="middle", weight="700"))
    els.append(
        '<path d="M 651 150 C 626 196, 628 250, 651 272 C 674 250, 676 196, 651 150 Z" '
        'fill="#fb923c" fill-opacity="0.45" stroke="#dc2626" stroke-width="1.3" stroke-dasharray="3 2"/>'
    )
    els.append(
        '<path d="M 651 174 C 635 210, 636 252, 651 268 C 666 252, 667 210, 651 174 Z" '
        'fill="#fde047" stroke="#ea580c" stroke-width="1.2"/>'
    )
    els.append('<rect x="647" y="184" width="8" height="76" rx="2" fill="#fde68a" stroke="#b45309" stroke-width="1.2"/>')
    els.append('<ellipse cx="651" cy="260" rx="5.5" ry="7" fill="#334155"/>')
    els.append(_line(626, 256, 626, 176, stroke=RED, sw=1.8, marker="arr-red"))
    els.append(txt(651, 300, "高温羽流包裹整根木杆", size=10.2, color=RED, anchor="middle", weight="700"))
    els.append(txt(651, 317, "提前热解出可燃气，秒烧到手！", size=9.8, color=BODY, anchor="middle"))

    # Safety insight box
    els.append(card(418, 344, 306, 116, rx=8, fill="#fff7ed", stroke="#fdba74", sw=1.0))
    els.append(txt(430, 364, "从火柴放大到森林山火与高层逃生铁律：", size=11, color=RED, weight="700"))
    els.append(txt(430, 383, "1. 严禁往山上跑：陡坡与峡谷把向上热羽流压向坡面树冠（贴壁", size=10.2, color=BODY))
    els.append(txt(430, 400, "   柯恩达效应 + 辐射预热），山火上坡蔓延速度可达平地的 4–10 倍！", size=10.2, color=BODY))
    els.append(txt(430, 418, "2. 火场弯腰低姿：楼梯间与电梯井是天然大烟囱，剧毒高温烟气", size=10.2, color=BODY))
    els.append(txt(430, 435, "   以 3–5 m/s 直冲顶层，贴近地面 30 cm 才有残存低温空气层。", size=10.2, color=BODY))

    return figure(
        490,
        "火焰浮力涡环闪烁频率定律与火柴顺逆流燃烧蔓延对比图",
        "左图绘制火焰闪烁频率随火源直径平方根成反比的实验曲线（从2厘米蜡烛10.6赫兹到9米油池火0.5赫兹）；右图对比火柴头朝上逆流慢烧与朝下顺流预热猛烧，延伸至山火上坡加速与火场低姿逃生原理。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 5. Accelerating Jar Equivalence Tilt & Kitchen Gas Stove Ionization Sensor
# ---------------------------------------------------------------------------
def build_accelerating_jar_and_stove_sensor() -> str:
    g = 9.80665
    a_car = 3.5  # m/s^2 forward acceleration (~0 to 100 km/h in 7.9 s)
    theta_deg = math.degrees(math.atan2(a_car, g))
    assert 19.0 < theta_deg < 20.2  # ~19.6 degrees FORWARD!

    els = []
    els.extend(
        header(
            "两个颠覆直觉的现实应用：加速车里的火往哪偏？燃气灶靠什么防漏气？",
            "一个验证爱因斯坦等效原理与浮力本质，一个把火焰十亿分之二的化学电离变成千家万户的救命开关",
        )
    )

    # Left Card: Candle inside a sealed jar accelerating right
    els.append(card(20, 62, 360, 404))
    els.append(step_badge(38, 84, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 88, "密闭玻璃瓶向右加速：火苗竟然“迎着前方”偏！", size=12.4, color=INK, weight="700"))

    # Glass jar on a cart accelerating right
    els.append(card(56, 126, 288, 178, rx=12, fill="#f8fafc", stroke="#64748b", sw=2.0))
    els.append(txt(72, 148, "密闭玻璃罩（隔绝车外迎面风）", size=10.3, color=SLATE, weight="600"))

    # Acceleration arrow to the RIGHT
    els.append(_line(140, 112, 264, 112, stroke=RED, sw=2.6, marker="arr-red"))
    els.append(txt(202, 104, f"整体向右加速 a = {a_car:.1f} m/s²", size=10.8, color=RED, anchor="middle", weight="700"))

    # Heavy cold air pushed to the LEFT rear inside jar
    els.append(' <rect x="60" y="158" width="96" height="142" rx="8" fill="#dbeafe" fill-opacity="0.65"/>')
    els.append(_line(166, 236, 92, 236, stroke=BLUE, sw=2.0, marker="arr-blue"))
    els.append(txt(112, 218, "重冷空气惯性", size=10.2, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(112, 256, "拥向后壁增压", size=10.2, color=BLUE, anchor="middle", weight="700"))

    # Candle at x=204, y=262..302 with flame tilted FORWARD (to the RIGHT by +19.6 deg!)
    cx_j, cy_wick = 204.0, 250.0
    els.append(f'<rect x="{cx_j - 14:.1f}" y="260" width="28" height="42" rx="3" fill="#e2e8f0" stroke="#64748b" stroke-width="1.3"/>')
    els.append(_line(cx_j, 260, cx_j, cy_wick, stroke="#334155", sw=2.8))
    # Vertical dashed reference
    els.append(_line(cx_j, cy_wick, cx_j, 162, stroke=SLATE, sw=1.2, dash="4 3"))
    # Tilted flame group rotated +theta_deg around (cx_j, cy_wick) -> leans RIGHT (forward!)
    els.append(
        f'<g transform="translate({cx_j:.1f},{cy_wick:.1f}) rotate({theta_deg:.1f})">'
        f'<path d="M 0 -78 C -18 -46, -17 -14, 0 0 C 17 -14, 18 -46, 0 -78 Z" '
        f'fill="#fde047" stroke="#ea580c" stroke-width="1.3"/>'
        f'<path d="M 0 -28 C -7 -16, -7 -5, 0 0 C 7 -5, 7 -16, 0 -28 Z" fill="#2563eb" fill-opacity="0.7"/>'
        f"</g>"
    )
    els.append(txt(cx_j + 34, 178, f"向前倾 θ ≈ {theta_deg:.1f}°！", size=11, color=ORANGE, weight="700"))
    els.append(txt(cx_j + 34, 195, "θ = arctan(a / g)", size=10.2, color=MUTED, cls="mono"))

    # Wheels under jar
    els.append('<circle cx="110" cy="314" r="9" fill="#475569"/>')
    els.append('<circle cx="290" cy="314" r="9" fill="#475569"/>')

    els.append(card(34, 336, 332, 118, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE, sw=1.0))
    els.append(txt(46, 356, "为什么没往后倒，反而和氦气球一样“往前冲”？", size=11, color=INK, weight="700"))
    els.append(txt(46, 375, "• 车厢向右加速等价于叠加向左的惯性力场 −a，合成“等效重力”", size=10.2, color=BODY))
    els.append(txt(46, 393, "  g_eff 指向【左下方】；", size=10.2, color=BODY))
    els.append(txt(46, 411, "• 密度大 5 倍的冷空气被甩向车尾（左），产生指向【右上方】的", size=10.2, color=BODY))
    els.append(txt(46, 429, "  阿基米德浮力，把轻盈火苗推向前方！旋转圆盘上火苗则指向圆心。", size=10.2, color=BODY))

    # Right Card: Kitchen Gas Stove Flame Ionization / Rectification Safety Sensor
    els.append(card(396, 62, 344, 404))
    els.append(step_badge(414, 84, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(432, 88, "厨房灶台救命机关：火焰离子整流熄火保护", size=12.4, color=INK, weight="700"))

    # Burner schematic
    els.append(card(412, 114, 312, 196, rx=10, fill="#0f172a", stroke="#334155"))
    # Metal burner cap (large area cathode/ground)
    els.append('<rect x="454" y="256" width="160" height="22" rx="4" fill="#64748b" stroke="#94a3b8" stroke-width="1.3"/>')
    els.append(txt(534, 271, "金属火盖（大面积接地电极）", size=10.0, color="#f8fafc", anchor="middle", weight="600"))

    # Blue premixed flames + ions
    for fx in [478, 514, 550, 586]:
        els.append(
            f'<path d="M {fx} 188 C {fx - 13} 218, {fx - 12} 244, {fx} 256 C {fx + 12} 244, {fx + 13} 218, {fx} 188 Z" '
            f'fill="#38bdf8" fill-opacity="0.65" stroke="#7dd3fc" stroke-width="1.1"/>'
        )
    els.append(txt(518, 174, "火焰区含 HCO⁺ / H₃O⁺ 正离子与高速自由电子 e⁻", size=10.0, color="#7dd3fc", anchor="middle", weight="600"))

    # Thin flame-sensing electrode pin entering right flame
    els.append('<path d="M 656 266 L 656 218 L 588 218" fill="none" stroke="#fbbf24" stroke-width="3.2" stroke-linecap="round"/>')
    els.append('<rect x="648" y="256" width="16" height="32" rx="2" fill="#f8fafc" stroke="#94a3b8"/>')
    els.append(txt(668, 214, "离子感应针", size=10.5, color="#fbbf24", weight="700"))
    els.append(txt(668, 230, "（细金属探针）", size=9.6, color="#cbd5e1"))

    # Microampere DC rectified current loop indicator
    els.append(card(426, 126, 196, 32, rx=6, fill="#1e293b", stroke="#22c55e", sw=1.2))
    els.append(txt(524, 146, "整流直流电 I ≈ 2–10 μA → 吸合电磁阀", size=10.0, color="#4ade80", anchor="middle", weight="700"))
    els.append(txt(534, 296, "汤水扑灭火焰 → 离子 0.1 秒消失 → 电流归零瞬间断气！", size=10.0, color="#fde047", anchor="middle", weight="600"))

    els.append(card(412, 324, 312, 130, rx=8, fill=GREEN_SOFT, stroke="#86efac", sw=1.0))
    els.append(txt(424, 344, "为什么“烧红的铁丝”骗不过离子感应针？（对比热电偶）", size=11, color=GREEN, weight="700"))
    els.append(txt(424, 363, "• 老式热电偶靠温度发电，溢锅灭了火但余温尚烫，需等几秒才断气；", size=10.2, color=BODY))
    els.append(txt(424, 381, "• 离子针施加交流电：电子 e⁻ 比正离子轻数万倍、跑得飞快，加上", size=10.2, color=BODY))
    els.append(txt(424, 399, "  火盖面积远大于细针，把火焰变成天然【单向二极管】（火焰整流）！", size=10.2, color=BODY))
    els.append(txt(424, 417, "• 哪怕灶头烫得通红或被油污短路，只要没有真实燃烧产生的化学", size=10.2, color=BODY))
    els.append(txt(424, 435, "  电离单向直流脉冲，控制器 0.1 秒内果断关阀，杜绝燃气泄漏爆炸。", size=10.2, color=BODY))

    return figure(
        480,
        "加速密闭容器火焰前倾效应与家用燃气灶火焰离子整流保护原理图",
        "左图展示向右加速的密闭玻璃罩内冷空气后涌使火焰反直觉向前倾斜约19.6度；右图展示燃气灶利用火焰化学电离产生的电子与正离子迁移率差异及电极面积不对称实现单向整流检测，0.1秒熄火断气。",
        els,
        extra_defs=_markers(),
    )


@register(TOPIC, "physics", "火为什么向上燃烧与火的本质（5张760px原创SVG图解）")
def build_all() -> None:
    builders = [
        ("candle-flame-anatomy-and-material-nature.svg", build_candle_anatomy_and_plasma_scale),
        ("earth-buoyancy-plume-vs-space-spherical-flame.svg", build_earth_vs_space_flame),
        ("blue-radical-spectra-vs-yellow-soot-blackbody.svg", build_blue_vs_yellow_spectra),
        ("puffing-frequency-and-upward-flame-spread.svg", build_puffing_and_match_spread),
        ("accelerating-jar-tilt-and-flame-ion-sensor.svg", build_accelerating_jar_and_stove_sensor),
    ]
    for fname, fn in builders:
        svg = fn()
        write_svg(TOPIC, fname, svg)
