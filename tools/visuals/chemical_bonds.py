"""Original SVG visuals for chemical bonds: Morse curve, bond triangle, VSEPR/carbon, MO O2, and IMFs."""

import math

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
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "chemical-bonds"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"


EXTRA_DEFS = (
    f'<marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">'
    f'<path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{RED}"/></marker>'
)


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker_end=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    m_attr = f' marker-end="url(#{marker_end})"' if marker_end else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}"{d_attr}{m_attr}/>'
    )


def _polyline(pts, color=BLUE, sw=2.5, dash=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    p_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (
        f'<polyline points="{p_str}" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{d_attr}/>'
    )


def _morse_h2(r_pm: float) -> float:
    """Shifted Morse potential V(r) in kJ/mol for H2 with r0 = 74 pm, well -436 kJ/mol, a = 0.0194 pm^-1."""
    r0 = 74.0
    d_well = 436.0
    a = 0.0194  # physical H2 Morse width (~1.94 Å^-1); V(r)=0 inner crossing at r = 74 - ln(2)/a ≈ 38.3 pm
    term = 1.0 - math.exp(-a * (r_pm - r0))
    return d_well * (term * term - 1.0)


def _verify_chemical_bond_math():
    """Assert quantitative thermochemistry, Morse minimum, Born-Haber, MO bond order, and IMF data."""
    # 1. H2 Morse curve minimum at r0 = 74 pm, V(74) = -436 kJ/mol, inner V=0 crossing ~38.3 pm, steep wall <35 pm
    assert abs(_morse_h2(74.0) - (-436.0)) < 1e-9
    r_inner_zero = 74.0 - math.log(2.0) / 0.0194
    assert 38.0 < r_inner_zero < 38.6 and abs(_morse_h2(r_inner_zero)) < 1e-6
    assert _morse_h2(31.0) > 250.0
    assert abs(_morse_h2(300.0)) < 12.0

    # 2. H2 + Cl2 -> 2 HCl reaction enthalpy from OpenStax Table 7.2 bond energies
    d_hh, d_clcl, d_hcl = 436, 243, 432
    delta_h_rxn = (d_hh + d_clcl) - 2 * d_hcl
    assert delta_h_rxn == -185

    # 3. Gas-phase electron transfer Na(g) + Cl(g) -> Na+(g) + Cl-(g) vs NaCl lattice energy
    ie_na = 496   # kJ/mol endothermic ionization energy of Na(g)
    ea_cl = -349  # kJ/mol exothermic electron affinity of Cl(g)
    gas_ion_pair_cost = ie_na + ea_cl
    assert gas_ion_pair_cost == 147  # unfavorable in isolated gas pair!
    lattice_nacl = -769  # OpenStax Chemistry 2e 7.1 & 7.5
    assert gas_ion_pair_cost + lattice_nacl == -622  # strongly exothermic thanks to 3D lattice!

    # 4. Carbon single / double / triple bond length & bond energy monotonicity (OpenStax Table 7.3)
    cc_lengths = [154, 134, 120]  # pm
    cc_energies = [345, 611, 837]  # kJ/mol
    assert cc_lengths[0] > cc_lengths[1] > cc_lengths[2]
    assert cc_energies[0] < cc_energies[1] < cc_energies[2]

    # 5. VSEPR sp3 lone-pair compression angles (CH4 -> NH3 -> H2O)
    angles = [109.5, 107.0, 104.5]
    assert angles[0] > angles[1] > angles[2]

    # 6. Molecular orbital bond orders (OpenStax 8.4)
    bo_he2 = (2 - 2) // 2
    bo_n2 = (8 - 2) // 2  # valence electrons: 8 bonding, 2 antibonding (sigma2s*)
    bo_o2 = (8 - 4) // 2  # valence electrons: 8 bonding, 4 antibonding (sigma2s*2, pi2p*2)
    assert (bo_he2, bo_n2, bo_o2) == (0, 3, 2)

    # 7. Group 16 hydride boiling points (°C) and water vaporization vs O-H bond energy
    bp_h2te, bp_h2se, bp_h2s, bp_h2o = -2, -41, -60, 100
    assert bp_h2te > bp_h2se > bp_h2s and bp_h2o - (-80) == 180
    assert round(464 / 40.7, 1) == 11.4  # breaking O-H bond takes >11x boiling water


def build_h2_morse_potential_anim():
    """Figure 1: Animated H2 Morse potential energy curve + bond formation/breaking energy ledger."""
    w, h = 760, 520
    body = []
    anim_css = """
  @keyframes approachAtom {
    0%, 10% { transform: translateX(182px); }
    68%, 100% { transform: translateX(0px); }
  }
  @keyframes cloudGlow {
    0%, 28% { opacity: 0.08; }
    68%, 100% { opacity: 0.92; }
  }
  @keyframes wellPulse {
    0%, 62% { opacity: 0.25; }
    78%, 100% { opacity: 1; }
  }
  .h-approach { animation: approachAtom 6.2s cubic-bezier(0.25, 0.8, 0.25, 1) 1 forwards; }
  .bond-cloud { animation: cloudGlow 6.2s ease-out 1 forwards; }
  .well-badge { animation: wellPulse 6.2s ease-out 1 forwards; }
  @media (prefers-reduced-motion: reduce) {
    .h-approach, .bond-cloud, .well-badge { animation: none !important; transform: none !important; opacity: 1 !important; }
  }
"""

    body.extend(
        header(
            "为什么两个原子既不擦肩而过，也不撞成一团？——氢分子势能阱",
            "核间距离 r 决定吸引与排斥的平衡点（r₀ = 74 pm，成键放热 −436 kJ/mol；支持减少动态效果）",
        )
    )

    # Left card: Morse curve + approaching H atoms
    body.append(card(20, 74, 456, 412))
    body.append(step_badge(40, 96, 1, fg=BLUE, bg=BLUE_SOFT))
    body.append(txt(62, 101, "H₂ 莫尔斯势能曲线 V(r) 与电子云相长干涉", size=14, weight="700", color=INK))

    # Top mini visual strip inside left card: fixed H_A + approaching H_B
    body.append(f'<rect x="38" y="114" width="420" height="68" rx="10" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
    # Shared bonding orbital cloud at equilibrium (cx between x=116 and x=166 -> center 141)
    body.append(
        f'<ellipse class="bond-cloud" cx="141" cy="148" rx="46" ry="22" '
        f'fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="4 3"/>'
    )
    # Fixed H_A nucleus at r=0 -> x=116
    body.append(f'<circle cx="116" cy="148" r="15" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>')
    body.append(txt(116, 153, "Hₐ⁺", size=12, weight="700", color=BLUE, anchor="middle"))

    # Equilibrium H_B target ghost at x=166 (74 pm) and animated H_B starting +182px right (x=348, ~240 pm)
    body.append(f'<circle cx="166" cy="148" r="15" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    body.append(
        f'<g class="h-approach">'
        f'<circle cx="166" cy="148" r="15" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>'
        f'{txt(166, 153, "Hᵦ⁺", size=12, weight="700", color=GREEN, anchor="middle")}'
        f'</g>'
    )
    body.append(_line(332, 148, 200, 148, color=GREEN, sw=1.5, dash="4 3", marker_end="arr-muted"))
    body.append(txt(272, 136, "从远距靠近 → 停在 74 pm", size=11, weight="600", color=SLATE, anchor="middle"))
    body.append(txt(394, 169, "单次动画定格成键态", size=10.5, color=MUTED, anchor="middle"))

    # Plot coordinate system:
    # r_pm in [26, 280] -> x in [82, 448]
    # V in [-500, +350] kJ/mol -> y in [424, 198]
    x0, x1 = 82.0, 448.0
    y_top, y_bot = 198.0, 424.0
    r_min, r_max = 26.0, 280.0
    v_min, v_max = -500.0, 350.0

    def map_x(r_val):
        return x0 + (r_val - r_min) / (r_max - r_min) * (x1 - x0)

    def map_y(v_val):
        return y_bot - (v_val - v_min) / (v_max - v_min) * (y_bot - y_top)

    y_zero = map_y(0.0)
    # Axes and reference gridlines
    body.append(_line(x0, y_top, x0, y_bot, color=SLATE, sw=1.5))
    body.append(_line(x0, y_bot, x1, y_bot, color=SLATE, sw=1.5))
    body.append(_line(x0, y_zero, x1, y_zero, color=MUTED, sw=1.3, dash="5 4"))
    body.append(txt(75, y_zero + 4, "0", size=11, weight="600", color=SLATE, anchor="end"))
    body.append(txt(75, map_y(300) + 4, "+300", size=10.5, color=RED, anchor="end"))
    body.append(txt(75, map_y(-200) + 4, "−200", size=10.5, color=MUTED, anchor="end"))
    body.append(txt(75, map_y(-436) + 4, "−436", size=11, weight="700", color=BLUE, anchor="end"))
    body.append(txt(34, 250, "势能", size=11, weight="700", color=SLATE))
    body.append(txt(32, 266, "kJ/mol", size=10, color=MUTED))

    for r_tick in (38, 74, 150, 250):
        xt = map_x(r_tick)
        body.append(_line(xt, y_bot, xt, y_bot + 5, color=SLATE, sw=1.3))
        lbl_col = BLUE if r_tick == 74 else MUTED
        lbl_w = "700" if r_tick == 74 else "400"
        body.append(txt(xt, y_bot + 19, f"{r_tick}", size=10.5, weight=lbl_w, color=lbl_col, anchor="middle"))
    body.append(txt(266, 464, "两原子核间距离 r (pm，1 pm = 10⁻¹² m)", size=11.5, weight="600", color=BODY, anchor="middle"))

    # Split curve into repulsive (<=39 pm where V>=0, red) and attractive/well (>=38 pm, blue)
    rep_pts = []
    att_pts = []
    for i in range(251):
        r_v = 30.0 + i * 1.0
        v_v = _morse_h2(r_v)
        if v_v <= 340.0:
            pt = (map_x(r_v), map_y(v_v))
            if r_v <= 39.0:
                rep_pts.append(pt)
            if r_v >= 38.0:
                att_pts.append(pt)
    body.append(_polyline(rep_pts, color=RED, sw=2.8))
    body.append(_polyline(att_pts, color=BLUE, sw=2.8))

    # Minimum drop-lines & callouts
    x_min = map_x(74.0)
    y_min = map_y(-436.0)
    body.append(_line(x_min, y_zero, x_min, y_min, color=GREEN, sw=1.6, dash="4 3"))
    body.append(f'<circle class="well-badge" cx="{x_min:.1f}" cy="{y_min:.1f}" r="6" fill="{BLUE}" stroke="#ffffff" stroke-width="2"/>')

    # Three step callout labels on the plot (carefully non-overlapping)
    body.append(txt(106, 218, "④ r < 38 pm 强排斥陡墙", size=11, weight="700", color=RED))
    body.append(txt(106, 234, "核间正电斥力+泡利排斥", size=10.5, color=BODY))

    body.append(txt(332, 274, "① 远距孤立双原子 (V = 0)", size=11, weight="700", color=SLATE, anchor="middle"))
    body.append(txt(336, 338, "② 共享电子云吸引 → 放热下滑", size=11, weight="600", color=BLUE, anchor="middle"))

    body.append(f'<rect x="164" y="380" width="236" height="36" rx="8" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    body.append(txt(282, 396, "③ 谷底平衡键长 r₀ = 74 pm", size=11.5, weight="700", color=BLUE, anchor="middle"))
    body.append(txt(282, 411, "成键释放 436 kJ/mol（最稳态）", size=10.5, color=BODY, anchor="middle"))

    # Right card: Energy ledger & misconception busting
    body.append(card(492, 74, 248, 412))
    body.append(step_badge(512, 96, 2, fg=ORANGE, bg=ORANGE_SOFT))
    body.append(txt(534, 101, "头号误区：断键其实要吸热！", size=14, weight="700", color=INK))

    # Box A: Exothermic bond making vs Endothermic bond breaking
    body.append(f'<rect x="508" y="116" width="216" height="122" rx="10" fill="{ORANGE_SOFT}" stroke="{ORANGE}"/>')
    body.append(txt(520, 137, "成键 = 掉进势能坑（放热）", size=12, weight="700", color=ORANGE))
    body.append(txt(520, 155, "2 H(g) → H₂(g)   ΔH = −436 kJ", size=11, weight="600", color=INK))
    body.append(_line(520, 168, 712, 168, color=BORDER, sw=1.0))
    body.append(txt(520, 188, "断键 = 从坑底往上拔（吸热）", size=12, weight="700", color=RED))
    body.append(txt(520, 206, "H₂(g) → 2 H(g)   ΔH = +436 kJ", size=11, weight="600", color=INK))
    body.append(txt(520, 227, "燃料放热靠生成更稳的新强键！", size=10.5, weight="600", color=BODY))

    # Box B: Real H2 + Cl2 -> 2 HCl ledger (OpenStax 7.5)
    body.append(f'<rect x="508" y="252" width="216" height="218" rx="10" fill="{GREEN_SOFT}" stroke="{GREEN}"/>')
    body.append(txt(520, 274, "算一笔真实反应账：H₂ + Cl₂ → 2HCl", size=11.5, weight="700", color=GREEN))
    body.append(txt(520, 297, "① 先投入能量拆旧键（吸热）：", size=11, weight="600", color=RED))
    body.append(txt(528, 315, "• 拆 1 mol H–H：+436 kJ", size=10.5, color=BODY))
    body.append(txt(528, 332, "• 拆 1 mol Cl–Cl：+243 kJ", size=10.5, color=BODY))
    body.append(txt(528, 349, "合计投入：+679 kJ", size=10.5, weight="700", color=RED))

    body.append(txt(520, 373, "② 再组装新键回血（放热）：", size=11, weight="600", color=BLUE))
    body.append(txt(528, 391, "• 成 2 mol H–Cl：−2 × 432", size=10.5, color=BODY))
    body.append(txt(528, 408, "合计释放：−864 kJ", size=10.5, weight="700", color=BLUE))

    body.append(_line(520, 421, 712, 421, color=GREEN, sw=1.2))
    body.append(txt(520, 441, "净焓变 ΔH = 679 − 864", size=11, weight="700", color=INK))
    body.append(txt(520, 459, "= −185 kJ/mol（净放热！）", size=11.5, weight="700", color=GREEN))

    body.append(txt(380, 505, "数据来源：OpenStax Chemistry 2e 7.2 & 7.5 节；1927 年海特勒-伦敦量子计算首次算出 H₂ 势能阱", size=11, color=MUTED, anchor="middle"))
    write_svg(
        SUBDIR,
        "h2-morse-potential-anim.svg",
        figure(
            h,
            "氢分子莫尔斯势能曲线与化学键成键放热断键吸热能量账本",
            "左侧展示两个氢原子靠近时势能随核间距变化的莫尔斯势能曲线，在74皮米处达到负436千焦每摩尔最低点，小于50皮米急剧排斥；右侧用氢气与氯气生成氯化氢展示拆旧键吸热679千焦、成新键放热864千焦、净放热185千焦。",
            body,
            extra_css=anim_css,
            extra_defs=EXTRA_DEFS,
        ),
    )


def build_electronegativity_and_bond_triangle():
    """Figure 2: Electronegativity tug-of-war, Van Arkel-Ketelaar triangle, and NaCl vs Cu crystal behavior."""
    w, h = 760, 520
    body = []
    body.extend(
        header(
            "化学键不是孤立抽屉：电负性拔河与三大主价键连续谱",
            "平均电负性 χ̄ 与电负性差 Δχ 决定电子归属；三维晶格能与电子海塑造截然不同的宏观物性",
        )
    )

    # Left card: Tug-of-war + Van Arkel-Ketelaar bonding triangle
    body.append(card(20, 74, 368, 412))
    body.append(step_badge(40, 96, 1, fg=BLUE, bg=BLUE_SOFT))
    body.append(txt(62, 101, "鲍林电负性差 Δχ 与键型三角连续谱", size=14, weight="700", color=INK))

    # Three mini pills showing electron cloud distortion
    rows = [
        (114, "非极性共价 H–H", "Δχ = 0.0", "电子云完全对称均分", BLUE_SOFT, BLUE, 0),
        (158, "极性共价 Hδ⁺–Clδ⁻", "Δχ = 0.9", "电子云偏向高电负性氯", PURPLE_SOFT, PURPLE, 1),
        (202, "离子键 Na⁺ Cl⁻", "Δχ = 2.1", "价电子近似转移成阴阳离子", ORANGE_SOFT, ORANGE, 2),
    ]
    for ry, name, dchi, desc, bgc, fg, mode in rows:
        body.append(f'<rect x="36" y="{ry}" width="336" height="38" rx="8" fill="{bgc}" stroke="{fg}"/>')
        body.append(txt(48, ry + 16, name, size=11.5, weight="700", color=fg))
        body.append(txt(48, ry + 31, f"{dchi}｜{desc}", size=10.5, color=BODY))
        # Mini cloud graphic on right of pill (x=280..360)
        cy = ry + 19
        if mode == 0:
            body.append(f'<ellipse cx="322" cy="{cy}" rx="28" ry="11" fill="#ffffff" stroke="{fg}" stroke-width="1.6"/>')
            body.append(f'<circle cx="308" cy="{cy}" r="3.5" fill="{fg}"/><circle cx="336" cy="{cy}" r="3.5" fill="{fg}"/>')
        elif mode == 1:
            body.append(f'<path d="M294,{cy} C294,{cy-8} 322,{cy-14} 344,{cy-12} C356,{cy-10} 356,{cy+10} 344,{cy+12} C322,{cy+14} 294,{cy+8} 294,{cy} Z" fill="#ffffff" stroke="{fg}" stroke-width="1.6"/>')
            body.append(f'<circle cx="304" cy="{cy}" r="3" fill="{fg}"/><circle cx="340" cy="{cy}" r="4.5" fill="{fg}"/>')
        else:
            body.append(f'<circle cx="304" cy="{cy}" r="8" fill="#ffffff" stroke="{fg}" stroke-width="1.5"/>')
            body.append(f'<circle cx="338" cy="{cy}" r="13" fill="#ffffff" stroke="{fg}" stroke-width="1.8"/>')
            body.append(txt(304, cy + 3.5, "+", size=10, weight="700", color=fg, anchor="middle"))
            body.append(txt(338, cy + 3.5, "−", size=11, weight="700", color=fg, anchor="middle"))

    # Van Arkel-Ketelaar Triangle in lower half of left card (y=252..472)
    body.append(txt(204, 266, "范阿克尔-凯特拉尔键型三角（无绝对分界线）", size=12, weight="700", color=SLATE, anchor="middle"))
    # Triangle vertices: Top = Ionic (204, 294), Bottom-Left = Metallic (84, 434), Bottom-Right = Covalent (324, 434)
    body.append(
        f'<polygon points="204,294 84,434 324,434" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="2"/>'
    )
    # Vertex badges
    body.append(f'<circle cx="204" cy="294" r="7" fill="{ORANGE}"/>')
    body.append(txt(204, 283, "离子键 (CsF / NaCl)", size=11, weight="700", color=ORANGE, anchor="middle"))

    body.append(f'<circle cx="84" cy="434" r="7" fill="{GREEN}"/>')
    body.append(txt(92, 454, "金属键 (Na / Cu)", size=11, weight="700", color=GREEN, anchor="middle"))
    body.append(txt(92, 469, "低 χ̄：大家都松手 → 电子海", size=10, color=MUTED, anchor="middle"))

    body.append(f'<circle cx="324" cy="434" r="7" fill="{BLUE}"/>')
    body.append(txt(304, 454, "共价键 (F₂ / 金刚石)", size=11, weight="700", color=BLUE, anchor="middle"))
    body.append(txt(304, 469, "高 χ̄：大家都抓紧 → 共享对", size=10, color=MUTED, anchor="middle"))

    # Intermediate points inside/along edges
    body.append(f'<circle cx="264" cy="364" r="4.5" fill="{PURPLE}"/>')
    body.append(txt(308, 362, "极性共价", size=10.5, weight="700", color=PURPLE, anchor="middle"))
    body.append(txt(308, 376, "(HCl / H₂O)", size=10, color=BODY, anchor="middle"))

    body.append(f'<circle cx="204" cy="422" r="4.5" fill="{TEAL}"/>')
    body.append(txt(204, 412, "半导体 Si（共价↔金属过渡）", size=10, weight="600", color=TEAL, anchor="middle"))

    # Vertical Δχ indicator inside triangle
    body.append(_line(204, 392, 204, 318, color=MUTED, sw=1.3, dash="3 3", marker_end="arr-muted"))
    body.append(txt(204, 356, "Δχ 增大", size=10.5, weight="600", color=SLATE, anchor="middle"))

    # Right card: Born-Haber NaCl surprise + Ionic brittle cleavage vs Metallic malleability
    body.append(card(404, 74, 336, 412))
    body.append(step_badge(424, 96, 2, fg=ORANGE, bg=ORANGE_SOFT))
    body.append(txt(446, 101, "食盐晶格反转与“脆盐 vs 韧铜”之谜", size=14, weight="700", color=INK))

    # Top box: Born-Haber surprise
    body.append(f'<rect x="420" y="114" width="304" height="122" rx="10" fill="{ORANGE_SOFT}" stroke="{ORANGE}"/>')
    body.append(txt(432, 134, "反转真相：孤立一对钠氯抢电子其实亏本！", size=11.5, weight="700", color=ORANGE))
    body.append(txt(432, 154, "• 从 Na(g) 拔走电子（电离能）：+496 kJ/mol", size=10.5, color=BODY))
    body.append(txt(432, 172, "• Cl(g) 接住电子（电子亲和能）：−349 kJ/mol", size=10.5, color=BODY))
    body.append(txt(432, 190, "→ 气态单对移交净亏 +147 kJ/mol（吸热不划算）", size=10.5, weight="700", color=RED))
    body.append(_line(432, 200, 712, 200, color=BORDER, sw=1.0))
    body.append(txt(432, 219, "★ 全靠三维晶格能 −769 kJ/mol 一举扭亏成盐！", size=10.5, weight="700", color=GREEN))

    # Middle box: Ionic crystal hammer -> like-charge repulsion -> brittle cleavage
    body.append(f'<rect x="420" y="248" width="304" height="106" rx="10" fill="{RED_SOFT}" stroke="{RED}"/>')
    body.append(txt(432, 268, "① 离子晶体（食盐 NaCl）：一敲就沿平面崩裂", size=11.5, weight="700", color=RED))
    # Draw shifted 2-row ion grid on left (x=438..536), explanation on right
    ions_row1 = [(456, 294, "+"), (484, 294, "−"), (512, 294, "+")]  # shifted right by half cell!
    ions_row2 = [(456, 326, "+"), (484, 326, "−"), (512, 326, "+")]
    body.append(_line(430, 294, 444, 294, color=RED, sw=1.8, marker_end="arr-red"))
    for ix, iy, sgn in ions_row1 + ions_row2:
        col = ORANGE if sgn == "+" else BLUE
        body.append(f'<circle cx="{ix}" cy="{iy}" r="10" fill="#ffffff" stroke="{col}" stroke-width="1.8"/>')
        body.append(txt(ix, iy + 4, sgn, size=11, weight="700", color=col, anchor="middle"))
    body.append(txt(540, 296, "外力推错半格 →", size=10.5, weight="600", color=BODY))
    body.append(txt(540, 315, "+对+、−对− 同号相斥", size=10.5, weight="700", color=RED))
    body.append(txt(540, 334, "瞬间产生解理脆断！", size=10.5, color=BODY))

    # Bottom box: Metallic crystal hammer -> electron sea cushions shift -> malleable
    body.append(f'<rect x="420" y="366" width="304" height="106" rx="10" fill="{GREEN_SOFT}" stroke="{GREEN}"/>')
    body.append(txt(432, 386, "② 金属晶体（铜/金）：自由电子海柔性润滑", size=11.5, weight="700", color=GREEN))
    body.append(f'<rect x="442" y="398" width="84" height="60" rx="10" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-dasharray="3 2"/>')
    for ix, iy in [(460, 414), (488, 414), (514, 414), (452, 442), (480, 442), (508, 442)]:
        body.append(f'<circle cx="{ix}" cy="{iy}" r="9" fill="#ffffff" stroke="{GREEN}" stroke-width="1.8"/>')
        body.append(txt(ix, iy + 3.5, "+", size=10, weight="700", color=GREEN, anchor="middle"))
    body.append(txt(540, 414, "无方向性离域电子海", size=10.5, weight="600", color=BODY))
    body.append(txt(540, 433, "随阳离子滑移即时填补", size=10.5, weight="700", color=GREEN))
    body.append(txt(540, 452, "捶成金箔不断、导电反光", size=10.5, color=BODY))

    body.append(txt(380, 505, "数据来源：OpenStax Chemistry 2e 7.1、7.2、7.5 与 10.5 节；鲍林电负性标度（F = 4.0）", size=11, color=MUTED, anchor="middle"))
    write_svg(
        SUBDIR,
        "electronegativity-and-bond-triangle.svg",
        figure(
            h,
            "鲍林电负性拔河、键型连续谱三角与离子金属晶体力学对比",
            "左侧展示非极性共价、极性共价与离子键的电子云偏移，以及连接离子键、金属键、共价键的范阿克尔-凯特拉尔键型三角；右侧解析氯化钠晶格能负769千焦每摩尔如何扭转气态抢电子亏本，以及食盐错位脆断与金属电子海延展性的微观机制。",
            body,
            extra_defs=EXTRA_DEFS,
        ),
    )


def build_vsepr_hybridization_and_carbon():
    """Figure 3: VSEPR lone-pair angle compression, sigma/pi multiple bonds, and diamond vs graphite."""
    w, h = 760, 520
    body = []
    body.extend(
        header(
            "三维分子建筑学：孤对电子挤压、π 键旋转锁与碳的“双面人生”",
            "杂化轨道与价层电子对互斥（VSEPR）塑造分子几何；成键方式一变，金刚石与铅笔芯天壤之别",
        )
    )

    # Top full-width card: VSEPR sp3 lone-pair compression + CO2 contrast
    body.append(card(20, 74, 720, 196))
    body.append(step_badge(40, 96, 1, fg=BLUE, bg=BLUE_SOFT))
    body.append(txt(62, 101, "同是四组电子云（sp³ 骨架），为什么甲烷、氨气、水的键角步步缩水？", size=14, weight="700", color=INK))

    vsepr_cols = [
        (36, "甲烷 CH₄", "0 对孤对电子", "109.5°", "正四面体｜非极性", BLUE_SOFT, BLUE, 0),
        (212, "氨气 NH₃", "1 对孤对电子挤压", "107.0°", "三角锥形｜极性", PURPLE_SOFT, PURPLE, 1),
        (388, "水分子 H₂O", "2 对孤对电子强挤", "104.5°", "V 形折线｜强极性！", ORANGE_SOFT, ORANGE, 2),
        (564, "对照：CO₂", "sp 杂化双键直线", "180.0°", "偶极对消｜非极性", SLATE_SOFT, SLATE, 3),
    ]
    for bx, title, lp_txt, ang, shape_txt, bgc, fg, mode in vsepr_cols:
        body.append(f'<rect x="{bx}" y="114" width="162" height="142" rx="10" fill="{bgc}" stroke="{fg}"/>')
        body.append(txt(bx + 81, 133, title, size=12, weight="700", color=fg, anchor="middle"))
        cx, cy = bx + 81, 178
        if mode == 0:
            # CH4 tetrahedron schematic
            for hx, hy in [(cx, cy - 26), (cx - 28, cy + 16), (cx + 28, cy + 16), (cx + 8, cy + 24)]:
                body.append(_line(cx, cy, hx, hy, color=fg, sw=2.0))
                body.append(f'<circle cx="{hx}" cy="{hy}" r="6" fill="#ffffff" stroke="{fg}" stroke-width="1.5"/>')
            body.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{fg}"/>')
            body.append(txt(cx, cy + 4, "C", size=10.5, weight="700", color="#ffffff", anchor="middle"))
        elif mode == 1:
            # NH3: 1 lone pair lobe on top + 3 H legs
            body.append(f'<ellipse cx="{cx}" cy="{cy - 22}" rx="11" ry="15" fill="#ffffff" stroke="{fg}" stroke-width="1.5" stroke-dasharray="3 2"/>')
            body.append(txt(cx, cy - 20, "··", size=13, weight="700", color=fg, anchor="middle"))
            for hx, hy in [(cx - 26, cy + 18), (cx, cy + 23), (cx + 26, cy + 18)]:
                body.append(_line(cx, cy, hx, hy, color=fg, sw=2.0))
                body.append(f'<circle cx="{hx}" cy="{hy}" r="6" fill="#ffffff" stroke="{fg}" stroke-width="1.5"/>')
            body.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{fg}"/>')
            body.append(txt(cx, cy + 4, "N", size=10.5, weight="700", color="#ffffff", anchor="middle"))
        elif mode == 2:
            # H2O: 2 lone pair lobes on top + 2 H legs at 104.5°
            body.append(f'<ellipse cx="{cx - 14}" cy="{cy - 20}" rx="9" ry="14" fill="#ffffff" stroke="{fg}" stroke-width="1.5" stroke-dasharray="3 2"/>')
            body.append(f'<ellipse cx="{cx + 14}" cy="{cy - 20}" rx="9" ry="14" fill="#ffffff" stroke="{fg}" stroke-width="1.5" stroke-dasharray="3 2"/>')
            body.append(txt(cx - 14, cy - 18, "··", size=12, weight="700", color=fg, anchor="middle"))
            body.append(txt(cx + 14, cy - 18, "··", size=12, weight="700", color=fg, anchor="middle"))
            for hx, hy in [(cx - 27, cy + 18), (cx + 27, cy + 18)]:
                body.append(_line(cx, cy, hx, hy, color=fg, sw=2.2))
                body.append(f'<circle cx="{hx}" cy="{hy}" r="6.5" fill="#ffffff" stroke="{fg}" stroke-width="1.6"/>')
            body.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{fg}"/>')
            body.append(txt(cx, cy + 4, "O", size=10.5, weight="700", color="#ffffff", anchor="middle"))
        else:
            # CO2 linear O=C=O
            body.append(_line(cx - 38, cy - 3, cx + 38, cy - 3, color=fg, sw=2.0))
            body.append(_line(cx - 38, cy + 3, cx + 38, cy + 3, color=fg, sw=2.0))
            body.append(f'<circle cx="{cx - 40}" cy="{cy}" r="8.5" fill="#ffffff" stroke="{RED}" stroke-width="1.6"/>')
            body.append(f'<circle cx="{cx + 40}" cy="{cy}" r="8.5" fill="#ffffff" stroke="{RED}" stroke-width="1.6"/>')
            body.append(f'<circle cx="{cx}" cy="{cy}" r="9.5" fill="{fg}"/>')
            body.append(txt(cx, cy + 4, "C", size=10, weight="700", color="#ffffff", anchor="middle"))
            body.append(txt(cx - 40, cy + 3.5, "O", size=9.5, weight="700", color=RED, anchor="middle"))
            body.append(txt(cx + 40, cy + 3.5, "O", size=9.5, weight="700", color=RED, anchor="middle"))

        body.append(txt(bx + 81, 221, f"键角 {ang}（{lp_txt}）", size=10.5, weight="700", color=INK, anchor="middle"))
        body.append(txt(bx + 81, 241, shape_txt, size=10.5, color=BODY, anchor="middle"))

    # Bottom-left card: Single / Double / Triple C-C bonds (sigma vs pi)
    body.append(card(20, 284, 348, 202))
    body.append(step_badge(40, 306, 2, fg=GREEN, bg=GREEN_SOFT))
    body.append(txt(62, 311, "单双三键对比：σ 自由转轴 vs π 旋转锁", size=13.5, weight="700", color=INK))

    bond_rows = [
        (326, "C–C 单键", "1σ", "154 pm", "345 kJ/mol", "头碰头自由旋转", BLUE),
        (376, "C=C 双键", "1σ + 1π", "134 pm", "611 kJ/mol", "肩并肩锁死平面", PURPLE),
        (426, "C≡C 三键", "1σ + 2π", "120 pm", "837 kJ/mol", "短而刚硬高键能", ORANGE),
    ]
    for ry, bname, comp, blen, beng, note, col in bond_rows:
        body.append(f'<rect x="36" y="{ry}" width="316" height="42" rx="8" fill="{CARD_BG}" stroke="{BORDER}"/>')
        body.append(txt(46, ry + 18, f"{bname} ({comp})", size=11.5, weight="700", color=col))
        body.append(txt(46, ry + 34, f"键长 {blen} ｜ 键能 {beng}", size=10.5, color=BODY))
        # Scaled energy bar on right (x=214..340)
        bar_w = round(float(beng.split()[0]) / 837.0 * 116)
        body.append(f'<rect x="224" y="{ry + 9}" width="{bar_w}" height="10" rx="4" fill="{col}"/>')
        body.append(txt(224, ry + 34, note, size=10, weight="600", color=SLATE))

    # Bottom-right card: Diamond (sp3) vs Graphite (sp2 + delocalized pi)
    body.append(card(384, 284, 356, 202))
    body.append(step_badge(404, 306, 3, fg=PURPLE, bg=PURPLE_SOFT))
    body.append(txt(426, 311, "同是 100% 纯碳：金刚石 vs 石墨", size=13.5, weight="700", color=INK))

    # Left sub-panel: Diamond
    body.append(f'<rect x="400" y="326" width="156" height="144" rx="10" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    body.append(txt(478, 345, "金刚石（sp³ 三维网）", size=11.5, weight="700", color=BLUE, anchor="middle"))
    # Tetrahedral node network
    d_nodes = [(478, 384), (478, 360), (452, 400), (504, 400), (470, 412)]
    for nx, ny in d_nodes[1:]:
        body.append(_line(478, 384, nx, ny, color=BLUE, sw=2.2))
    for nx, ny in d_nodes:
        body.append(f'<circle cx="{nx}" cy="{ny}" r="5.5" fill="#ffffff" stroke="{BLUE}" stroke-width="1.8"/>')
    body.append(txt(478, 434, "全为 154 pm 强 σ 键", size=10.5, weight="600", color=INK, anchor="middle"))
    body.append(txt(478, 451, "无自由电子 → 绝缘", size=10, color=BODY, anchor="middle"))
    body.append(txt(478, 465, "天然界硬度之王", size=10, weight="700", color=BLUE, anchor="middle"))

    # Right sub-panel: Graphite
    body.append(f'<rect x="568" y="326" width="156" height="144" rx="10" fill="{PURPLE_SOFT}" stroke="{PURPLE}"/>')
    body.append(txt(646, 345, "石墨（sp² 层状蜂窝）", size=11.5, weight="700", color=PURPLE, anchor="middle"))
    # Two layered flat hexagon sheets + weak dashed interlayer lines
    for sy in (368, 402):
        pts_hex = [(606, sy + 6), (626, sy), (654, sy), (674, sy + 6), (654, sy + 12), (626, sy + 12), (606, sy + 6)]
        body.append(_polyline(pts_hex, color=PURPLE, sw=2.0))
    for lx in (626, 654):
        body.append(_line(lx, 380, lx, 402, color=MUTED, sw=1.3, dash="3 3"))
    body.append(txt(695, 395, "335pm", size=9.5, color=MUTED, anchor="middle"))
    body.append(txt(646, 434, "层内 142 pm + 大 π 电子海", size=10.5, weight="600", color=INK, anchor="middle"))
    body.append(txt(646, 451, "层间仅范德华力 → 一划就掉", size=10, color=BODY, anchor="middle"))
    body.append(txt(646, 465, "既软滑又能良导电！", size=10, weight="700", color=PURPLE, anchor="middle"))

    body.append(txt(380, 505, "数据来源：OpenStax Chemistry 2e 7.5、7.6、8.2、8.3 与 10.5 节", size=11, color=MUTED, anchor="middle"))
    write_svg(
        SUBDIR,
        "vsepr-hybridization-and-carbon.svg",
        figure(
            h,
            "VSEPR孤对电子挤压键角变化、单双三键对比与金刚石石墨成键差异",
            "上方展示甲烷109.5度、氨气107.0度、水104.5度随孤对电子增加键角缩水及二氧化碳180度非极性对照；左下方对比碳碳单双三键键长缩短键能激增；右下方对比金刚石sp3三维共价网与石墨sp2层状大π键结构。",
            body,
            extra_defs=EXTRA_DEFS,
        ),
    )


def build_molecular_orbital_liquid_oxygen():
    """Figure 4: Lewis failure on liquid O2 paramagnetism & Molecular Orbital (MO) diagram."""
    w, h = 760, 520
    body = []
    body.extend(
        header(
            "为什么淡蓝色液氧会被磁铁吸住悬空？——分子轨道（MO）破案",
            "路易斯点式把电子全配成双而失算；量子力学反键轨道 π* 揭开两颗单身电子与键级公式",
        )
    )

    # Left card: Lewis prediction vs Liquid O2 magnet experiment + sigma/sigma* wave interference
    body.append(card(20, 74, 336, 412))
    body.append(step_badge(40, 96, 1, fg=ORANGE, bg=ORANGE_SOFT))
    body.append(txt(62, 101, "路易斯结构的盲区：液氧顺磁性实验", size=13.5, weight="700", color=INK))

    # Box 1: Lewis prediction
    body.append(f'<rect x="36" y="114" width="304" height="72" rx="10" fill="{RED_SOFT}" stroke="{RED}"/>')
    body.append(txt(48, 134, "路易斯点式写法：  :Ö = Ö:", size=12, weight="700", color=RED))
    body.append(txt(48, 154, "表面看 12 颗价电子全部两两成对 →", size=10.5, color=BODY))
    body.append(txt(48, 173, "错误预言：氧气应当抗磁（不被磁铁吸引）", size=10.5, weight="700", color=RED))

    # Box 2: Liquid O2 suspended between N and S poles
    body.append(f'<rect x="36" y="198" width="304" height="122" rx="10" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    body.append(txt(188, 218, "真实物理实验：−183°C 液氧悬停在磁极间！", size=11.5, weight="700", color=BLUE, anchor="middle"))
    # N pole left, S pole right, trapped blue liquid O2 bridge in center
    body.append(f'<rect x="54" y="238" width="76" height="44" rx="6" fill="{RED}" />')
    body.append(txt(92, 265, "N 极", size=13, weight="700", color="#ffffff", anchor="middle"))
    body.append(f'<rect x="246" y="238" width="76" height="44" rx="6" fill="{SLATE}" />')
    body.append(txt(284, 265, "S 极", size=13, weight="700", color="#ffffff", anchor="middle"))
    body.append(f'<ellipse cx="188" cy="260" rx="54" ry="18" fill="#38bdf8" stroke="{BLUE}" stroke-width="2"/>')
    body.append(txt(188, 264, "淡蓝液氧 O₂ ↑↓?", size=10.5, weight="700", color="#ffffff", anchor="middle"))
    body.append(txt(188, 305, "古伊磁天平实测：每个 O₂ 必含 2 颗未成对电子！", size=10.5, weight="700", color=INK, anchor="middle"))

    # Box 3: Constructive (bonding) vs Destructive (antibonding) wave combination
    body.append(f'<rect x="36" y="332" width="304" height="140" rx="10" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
    body.append(txt(48, 352, "原子轨道线性组合（LCAO）两条铁律：", size=11.5, weight="700", color=SLATE))
    body.append(txt(48, 375, "• 同相叠加（ψₐ + ψᵦ）→ 成键轨道 (σ / π)", size=10.5, weight="700", color=GREEN))
    body.append(txt(56, 393, "核间电子密度暴增，能量降低，把两核拉紧", size=10.5, color=BODY))
    body.append(txt(48, 417, "• 反相相减（ψₐ − ψᵦ）→ 反键轨道 (σ* / π*)", size=10.5, weight="700", color=RED))
    body.append(txt(56, 435, "核间出现电子为零的“节面”，能量升高拆台", size=10.5, color=BODY))
    body.append(txt(48, 458, "★ 键级 BO = (成键电子数 − 反键电子数) ÷ 2", size=10.5, weight="700", color=BLUE))

    # Right card: Full O2 2p MO energy-level diagram + Bond order comparisons
    body.append(card(372, 74, 368, 412))
    body.append(step_badge(392, 96, 2, fg=BLUE, bg=BLUE_SOFT))
    body.append(txt(414, 101, "O₂ 的 2p 分子轨道能级图（洪特规则破案）", size=13.5, weight="700", color=INK))

    # Energy vertical axis on left of MO diagram
    body.append(_line(394, 368, 394, 128, color=SLATE, sw=1.5, marker_end="arr-muted"))
    body.append(txt(394, 122, "能量", size=10.5, weight="700", color=SLATE, anchor="middle"))

    # Helper to draw orbital bar + electron arrows
    def orb(x_l, x_r, y_lvl, col, up=False, down=False):
        out = [_line(x_l, y_lvl, x_r, y_lvl, color=col, sw=2.6)]
        xm = (x_l + x_r) / 2.0
        if up and down:
            out.append(txt(xm - 5, y_lvl - 4, "↑", size=13, weight="700", color=col, anchor="middle"))
            out.append(txt(xm + 5, y_lvl - 4, "↓", size=13, weight="700", color=col, anchor="middle"))
        elif up:
            out.append(txt(xm, y_lvl - 4, "↑", size=14, weight="700", color=col, anchor="middle"))
        return "".join(out)

    # Left O atom 2p4 (y=248): 3 bars at x=[412..430], [435..453], [458..476]
    y_ao = 248
    body.append(orb(412, 430, y_ao, SLATE, up=True, down=True))
    body.append(orb(435, 453, y_ao, SLATE, up=True))
    body.append(orb(458, 476, y_ao, SLATE, up=True))
    body.append(txt(444, y_ao + 18, "左 O (2p⁴)", size=10.5, weight="600", color=SLATE, anchor="middle"))

    # Right O atom 2p4 (y=248): 3 bars at x=[640..658], [663..681], [686..704]
    body.append(orb(640, 658, y_ao, SLATE, up=True, down=True))
    body.append(orb(663, 681, y_ao, SLATE, up=True))
    body.append(orb(686, 704, y_ao, SLATE, up=True))
    body.append(txt(672, y_ao + 18, "右 O (2p⁴)", size=10.5, weight="600", color=SLATE, anchor="middle"))

    # Central MOs (center around x=558):
    # sigma* 2p (empty): y=148
    body.append(orb(542, 574, 148, MUTED))
    body.append(txt(558, 164, "σ*₂ₚ（反键空）", size=10, color=MUTED, anchor="middle"))

    # pi* 2p (2 degenerate singly-occupied!): y=204 -> HIGHLIGHT BOX!
    body.append(f'<rect x="506" y="176" width="104" height="44" rx="8" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
    body.append(orb(518, 550, 204, ORANGE, up=True))
    body.append(orb(566, 598, 204, ORANGE, up=True))
    body.append(txt(558, 233, "π*₂ₚ（2 颗单身同自旋！）", size=10.5, weight="700", color=ORANGE, anchor="middle"))

    # pi 2p (2 degenerate full): y=292
    body.append(orb(518, 550, 292, BLUE, up=True, down=True))
    body.append(orb(566, 598, 292, BLUE, up=True, down=True))
    body.append(txt(558, 309, "π₂ₚ（成键 4e⁻）", size=10, weight="600", color=BLUE, anchor="middle"))

    # sigma 2p (1 full): y=344
    body.append(orb(542, 574, 344, GREEN, up=True, down=True))
    body.append(txt(558, 361, "σ₂ₚ（成键 2e⁻）", size=10, weight="600", color=GREEN, anchor="middle"))

    # Dashed correlation lines
    for y_m in (148, 204, 292, 344):
        body.append(_line(478, y_ao, 514 if y_m in (204, 292) else 540, y_m, color=HAIRLINE, sw=1.1, dash="3 3"))
        body.append(_line(638, y_ao, 602 if y_m in (204, 292) else 576, y_m, color=HAIRLINE, sw=1.1, dash="3 3"))

    # Bottom summary table of bond orders inside right card
    body.append(f'<rect x="388" y="376" width="336" height="96" rx="10" fill="{GREEN_SOFT}" stroke="{GREEN}"/>')
    body.append(txt(400, 396, "键级公式一算即准（含 2s 成/反键抵消后）：", size=11, weight="700", color=GREEN))
    body.append(txt(400, 417, "• 氧气 O₂：(8 成键 − 4 反键)÷2 = 键级 2（顺磁双键）", size=10.5, weight="700", color=INK))
    body.append(txt(400, 437, "• 氮气 N₂：(8 成键 − 2 反键)÷2 = 键级 3（946 kJ 极稳）", size=10.5, color=BODY))
    body.append(txt(400, 457, "• 双氦 He₂：(2 成键 − 2 反键)÷2 = 键级 0（根本不成键）", size=10.5, color=BODY))

    body.append(txt(380, 505, "数据来源：OpenStax Chemistry 2e 8.4 节（分子轨道理论、二周期双原子分子排布与键级）", size=11, color=MUTED, anchor="middle"))
    write_svg(
        SUBDIR,
        "molecular-orbital-liquid-oxygen.svg",
        figure(
            h,
            "液氧顺磁性实验与氧气分子轨道能级排布图",
            "左侧对比路易斯结构预言抗磁性与真实负183摄氏度淡蓝色液氧悬停在磁铁两极间的顺磁现象，总结成键与反键轨道叠加规则；右侧绘出氧气2p分子轨道能级图，显示两颗电子按洪特规则分占两个简并反键π星轨道，键级为2。",
            body,
            extra_defs=EXTRA_DEFS,
        ),
    )


def build_chemical_bonds_vs_imf_scale():
    """Figure 5: 3-order-of-magnitude strength scale (Chemical Bonds vs IMFs) + Hydride boiling anomaly."""
    w, h = 760, 520
    body = []
    body.extend(
        header(
            "100°C 烧开水并没有断掉化学键！——主价键与分子间作用力标尺",
            "分子内化学键掌管化学身份（数百至数千 kJ/mol），分子间弱作用力掌管物态相变与生命拉链",
        )
    )

    # Left card: Logarithmic bar chart of strengths (1 to 4000 kJ/mol)
    body.append(card(20, 74, 368, 412))
    body.append(step_badge(40, 96, 1, fg=BLUE, bg=BLUE_SOFT))
    body.append(txt(62, 101, "能量跨度三数量级：化学键 vs 分子间力", size=13.5, weight="700", color=INK))

    # Log10 horizontal bar mapping: E in [1, 5000] kJ/mol -> log10(E) in [0, 3.7] -> width in [8, 178]
    def log_w(e_val):
        return max(10, round(math.log10(max(1.2, e_val)) / 3.65 * 172))

    bars = [
        ("MgO 离子晶格能", 3900, "3900", ORANGE, "主价键"),
        ("N≡N 共价三键", 946, "946", BLUE, "主价键"),
        ("NaCl 离子晶格能", 769, "769", ORANGE, "主价键"),
        ("水分子内 O–H 键", 464, "464", BLUE, "主价键"),
        ("碳骨架 C–C 单键", 345, "345", BLUE, "主价键"),
        ("水分子间氢键", 20, "~20 (汽化 40.7)", GREEN, "分子间"),
        ("HCl 偶极吸引力", 17, "~17", PURPLE, "分子间"),
        ("伦敦色散力(单接触)", 3, "1 ~ 5", SLATE, "分子间"),
    ]
    y_start = 122
    for idx, (lbl, ev, val_str, col, cat) in enumerate(bars):
        ry = y_start + idx * 34
        if idx == 5:
            # Divider between primary chemical bonds and secondary IMFs!
            body.append(_line(36, ry - 5, 372, ry - 5, color=RED, sw=1.4, dash="5 3"))
        ry_adj = ry + (6 if idx >= 5 else 0)
        body.append(txt(38, ry_adj + 14, lbl, size=10.5, weight="700" if idx in (3, 5) else "600", color=INK))
        bw = log_w(ev)
        body.append(f'<rect x="156" y="{ry_adj + 3}" width="{bw}" height="15" rx="4" fill="{col}"/>')
        body.append(txt(162 + bw, ry_adj + 15, f"{val_str}", size=10, weight="700", color=col))

    # Highlight takeaway box at bottom of left card
    body.append(f'<rect x="36" y="408" width="336" height="64" rx="10" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    body.append(txt(48, 428, "关键分水岭（对数横条，单位 kJ/mol）：", size=11, weight="700", color=BLUE))
    body.append(txt(48, 447, "• 100°C 沸腾只克服 40.7 kJ/mol 分子间氢键（水→水蒸气）", size=10.2, color=BODY))
    body.append(txt(48, 464, "• 扯断分子内 O–H 共价键需 464 kJ/mol（超 2000°C 才热解）", size=10.2, weight="700", color=RED))

    # Right card: Group 16 hydride boiling point anomaly plot + DNA zipper & Gecko
    body.append(card(404, 74, 336, 412))
    body.append(step_badge(424, 96, 2, fg=GREEN, bg=GREEN_SOFT))
    body.append(txt(446, 101, "氢键救地球：水沸点暴涨 180°C 与生命拉链", size=13.5, weight="700", color=INK))

    # Plot box inside right card: x in [458, 712], y in [124, 304], T in [-100, +120] °C
    px0, px1 = 458.0, 712.0
    py_top, py_bot = 128.0, 298.0
    t_min, t_max = -100.0, 120.0

    def map_ty(t_c):
        return py_bot - (t_c - t_min) / (t_max - t_min) * (py_bot - py_top)

    body.append(_line(px0, py_top, px0, py_bot, color=SLATE, sw=1.4))
    body.append(_line(px0, py_bot, px1, py_bot, color=SLATE, sw=1.4))
    y0c = map_ty(0.0)
    body.append(_line(px0, y0c, px1, y0c, color=MUTED, sw=1.1, dash="4 3"))
    body.append(txt(452, map_ty(100) + 4, "+100°C", size=10, weight="700", color=BLUE, anchor="end"))
    body.append(txt(452, y0c + 4, "0°C", size=10, color=SLATE, anchor="end"))
    body.append(txt(452, map_ty(-80) + 4, "−80°C", size=10, color=RED, anchor="end"))

    # X positions: Period 2 (H2O), Period 3 (H2S), Period 4 (H2Se), Period 5 (H2Te)
    xs = [492.0, 560.0, 628.0, 696.0]
    real_pts = [(xs[0], map_ty(100)), (xs[1], map_ty(-60)), (xs[2], map_ty(-41)), (xs[3], map_ty(-2))]
    # Extrapolated no-H-bond line from H2S (-60) to hypothetical H2O (-80)
    body.append(_polyline([(xs[0], map_ty(-80)), (xs[1], map_ty(-60)), (xs[2], map_ty(-41)), (xs[3], map_ty(-2))], color=MUTED, sw=2.0, dash="5 4"))
    body.append(_polyline(real_pts, color=BLUE, sw=2.6))

    # Vertical jump arrow at H2O (-80 -> +100)
    body.append(_line(xs[0], map_ty(-76), xs[0], map_ty(92), color=GREEN, sw=2.0, dash="4 3", marker_end="arr-blue"))
    body.append(txt(xs[0] + 58, map_ty(15), "氢键拉高", size=10.5, weight="700", color=GREEN, anchor="middle"))
    body.append(txt(xs[0] + 58, map_ty(-4), "+180°C！", size=11, weight="700", color=GREEN, anchor="middle"))

    labels_pt = [
        (xs[0], 100, "H₂O (+100°)", BLUE, -10),
        (xs[1], -60, "H₂S (−60°)", SLATE, 16),
        (xs[2], -41, "H₂Se (−41°)", SLATE, 16),
        (xs[3], -2, "H₂Te (−2°)", SLATE, -10),
    ]
    for x_p, tv, ltxt, col, dy in labels_pt:
        yp = map_ty(tv)
        body.append(f'<circle cx="{x_p:.1f}" cy="{yp:.1f}" r="4.5" fill="{col}"/>')
        anch = "start" if x_p == xs[0] else ("end" if x_p == xs[3] else "middle")
        dx = -8 if x_p == xs[0] else (8 if x_p == xs[3] else 0)
        body.append(txt(x_p + dx, yp + dy, ltxt, size=10, weight="700" if x_p == xs[0] else "600", color=col, anchor=anch))

    body.append(f'<circle cx="{xs[0]:.1f}" cy="{map_ty(-80):.1f}" r="4" fill="#ffffff" stroke="{RED}" stroke-width="1.6"/>')
    body.append(txt(xs[0] + 8, map_ty(-80) + 14, "无氢键外推 −80°C（海洋全气化）", size=9.8, weight="600", color=RED))
    body.append(txt(585, 318, "第 16 族氢化物常压沸点随周期变化", size=10.5, weight="600", color=MUTED, anchor="middle"))

    # Bottom two biological/materials cards inside right card
    body.append(f'<rect x="420" y="330" width="304" height="68" rx="9" fill="{GREEN_SOFT}" stroke="{GREEN}"/>')
    body.append(txt(432, 349, "① DNA 双螺旋：刚柔并济的“氢键拉链”", size=11, weight="700", color=GREEN))
    body.append(txt(432, 367, "单链骨架靠 ~350 kJ 共价磷酸二酯键锁死防断；", size=10.2, color=BODY))
    body.append(txt(432, 384, "双链碱基靠 ~20 kJ 氢键（A=T 二重、G≡C 三重）可逆开合！", size=10.2, weight="600", color=INK))

    body.append(f'<rect x="420" y="408" width="304" height="64" rx="9" fill="{PURPLE_SOFT}" stroke="{PURPLE}"/>')
    body.append(txt(432, 427, "② 壁虎飞檐走壁：百万根纳米刚毛色散力叠加", size=11, weight="700", color=PURPLE))
    body.append(txt(432, 445, "无需胶水吸盘，脚趾数百万三角形匙突紧贴玻璃，", size=10.2, color=BODY))
    body.append(txt(432, 461, "微弱瞬时偶极色散力积少成多，轻松托起数倍体重！", size=10.2, weight="600", color=INK))

    body.append(txt(380, 505, "数据来源：OpenStax Chemistry 2e 7.5 与 10.1 节（氢键沸点反常、Autumn 2000 壁虎范德华力实验）", size=11, color=MUTED, anchor="middle"))
    write_svg(
        SUBDIR,
        "chemical-bonds-vs-imf-scale.svg",
        figure(
            h,
            "化学键与分子间作用力能量标尺及氢键沸点反常图解",
            "左侧以对数横条对比氧化镁晶格能3900、氮三键946、水分子内氧氢共价键464与水分子间氢键20、色散力1至5千焦每摩尔；右侧绘出第16族氢化物沸点曲线，展示氢键将水沸点从外推负80摄氏度拉升至正100摄氏度，以及DNA氢键拉链与壁虎纳米刚毛色散力。",
            body,
            extra_defs=EXTRA_DEFS,
        ),
    )


@register("chemical-bonds", "化学键势能阱、键型连续谱、杂化几何、氧气分子轨道与分子间作用力", "physics")
def build_all():
    _verify_chemical_bond_math()
    build_h2_morse_potential_anim()
    build_electronegativity_and_bond_triangle()
    build_vsepr_hybridization_and_carbon()
    build_molecular_orbital_liquid_oxygen()
    build_chemical_bonds_vs_imf_scale()
