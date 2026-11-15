"""Original Chinese SVG diagrams for Multi-Stage Satellite Launch Rocket
Propulsion Principles (assets/images/multistage-rocket/).
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

SUBDIR = "multistage-rocket"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
GOLD = "#b45309"
GOLD_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"


def _area_mach_ratio(mach, gamma=1.22):
    """Isentropic 1D compressible nozzle area ratio A / A* as a function of Mach M."""
    term = (2.0 / (gamma + 1.0)) * (1.0 + 0.5 * (gamma - 1.0) * mach * mach)
    exp = (gamma + 1.0) / (2.0 * (gamma - 1.0))
    return (1.0 / mach) * (term ** exp)


def _solve_supersonic_mach(eps, gamma=1.22):
    """Solve A / A* = eps for supersonic Mach M > 1 via bisection."""
    lo, hi = 1.0001, 12.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if _area_mach_ratio(mid, gamma) < eps:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _max_payload_n_stages(m0_tons, dv_req, ve, eps_struct, n_stages):
    """Exact optimal equal-mass-ratio N-stage payload mass (in tons) for identical
    exhaust velocity ve and stage structural fraction eps_struct = m_s / (m_p + m_s).
    For each stage i, stage step factor lambda_stage = m_{0,i+1} / m_{0,i}.
    Stage mass ratio R = 1 / (eps_struct + (1 - eps_struct) * lam).
    Equal R across N stages requires R = exp(dv_req / (N * ve)).
    """
    r_stage = math.exp(dv_req / (n_stages * ve))
    # From 1 / R = eps_struct + (1 - eps_struct) * lam -> lam = (1/R - eps_struct) / (1 - eps_struct)
    lam = (1.0 / r_stage - eps_struct) / (1.0 - eps_struct)
    if lam <= 0:
        return 0.0
    return m0_tons * (lam ** n_stages)


def _verify_propulsion_and_staging_physics():
    # 1. Verify 1D isentropic de Laval nozzle math (gamma = 1.22 hot rocket gas):
    assert abs(_area_mach_ratio(1.0, 1.22) - 1.0) < 1e-12
    m_sl = _solve_supersonic_mach(16.0, 1.22)     # Sea-level Merlin-class nozzle (eps ~ 16)
    m_vac = _solve_supersonic_mach(165.0, 1.22)   # Vacuum MVac nozzle (eps ~ 165)
    assert 3.4 < m_sl < 3.8
    assert 5.0 < m_vac < 5.7
    # Static pressure ratio p_e / p_c = (1 + (gamma-1)/2 * M^2)^(-gamma/(gamma-1))
    g = 1.22
    p_ratio_sl = (1.0 + 0.5 * (g - 1.0) * m_sl ** 2) ** (-g / (g - 1.0))
    p_ratio_vac = (1.0 + 0.5 * (g - 1.0) * m_vac ** 2) ** (-g / (g - 1.0))
    assert p_ratio_vac < p_ratio_sl * 0.06  # Vacuum bell expands gas >16x lower exit pressure!

    # 2. Verify Tsiolkovsky SSTO impossibility vs 2-stage & 3-stage triumph!
    # Parameters: m0 = 300 t, dv_req = 9300 m/s, kerolox avg ve = 3100 m/s, structural fraction eps = 0.07
    m0 = 300.0
    dv_leo = 9300.0
    ve_kero = 3100.0
    eps = 0.07
    dv_ssto_zero_payload = ve_kero * math.log(1.0 / eps)
    assert 8240.0 < dv_ssto_zero_payload < 8250.0  # ~8,244 m/s < 9,300 m/s -> SSTO CANNOT REACH ORBIT!
    assert _max_payload_n_stages(m0, dv_leo, ve_kero, eps, 1) == 0.0

    pay_2 = _max_payload_n_stages(m0, dv_leo, ve_kero, eps, 2)
    pay_3 = _max_payload_n_stages(m0, dv_leo, ve_kero, eps, 3)
    assert 8.0 < pay_2 < 8.3      # 8.13 tons to LEO with 2 stages!
    assert 9.7 < pay_3 < 10.0     # 9.86 tons to LEO with 3 stages!
    assert pay_3 > pay_2 > 0.0

    # 3. Verify Exhaust Velocity molecular-mass scaling: ve ~ sqrt(T_c / M_mol)
    # Hydrolox (M ~ 11 g/mol) vs Kerolox (M ~ 22.5 g/mol) at similar chamber temperatures:
    ratio_ve = math.sqrt(22.5 / 11.0)
    assert 1.40 < ratio_ve < 1.45  # Explains ~440 s vs ~310 s Isp (~1.42x)!


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker_end=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    m_attr = f' marker-end="url(#{marker_end})"' if marker_end else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}"{d_attr}{m_attr}/>'
    )


def polyline(pts, color=BLUE, sw=2.5, dash=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    p_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{p_str}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{d_attr}/>'


def build_fig1_thrust_and_delaval_nozzle():
    """Fig 1: Reaction thrust in vacuum + de Laval nozzle subsonic-to-supersonic inversion + expansion regimes."""
    el = []
    el.extend(
        header(
            "第一关：太空没空气可“蹬”，火箭推谁？拉瓦尔喷管的超音速反转密码",
            "火箭不推空气而是“反推自己扔出的燃气”；先捏细卡住 1 倍音速，再敞开喇叭反而飙到 10 倍音速！",
        )
    )

    # Left Card: De Laval Convergent-Divergent Nozzle Profile & Mach/Pressure Curves
    el.append(card(22, 68, 412, 386, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(60, 95, "拉瓦尔喷管（收缩—扩张喷管）：为什么“越敞开飞得越快”？", size=12, color=INK, weight="700"))

    # Draw cutaway nozzle silhouette inside x=[44..414], center y=190
    el.append(card(36, 112, 384, 170, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    # Upper wall and lower wall paths:
    # Chamber x=54..140 (half-height 38), converging x=140..205 to throat (half-height 14), bell diverging x=205..365 (half-height 48)
    upper_w = "M54,152 L136,152 C164,152 184,176 205,176 C236,176 296,144 366,140"
    lower_w = "M54,228 L136,228 C164,228 184,204 205,204 C236,204 296,236 366,240"
    # Hot gas gradient fill polygon
    el.append(
        f'<defs><linearGradient id="noz-grad" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="#dc2626" stop-opacity="0.85"/>'
        f'<stop offset="48%" stop-color="#f97316" stop-opacity="0.85"/>'
        f'<stop offset="100%" stop-color="#3b82f6" stop-opacity="0.75"/>'
        f'</linearGradient></defs>'
    )
    el.append(
        f'<path d="{upper_w} L366,240 C296,236 236,204 205,204 C184,204 164,228 136,228 L54,228 Z" fill="url(#noz-grad)"/>'
    )
    el.append(f'<path d="{upper_w}" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>')
    el.append(f'<path d="{lower_w}" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>')
    el.append(_line(54, 152, 54, 228, color=INK, sw=3.2))

    # Throat vertical dashed line at x=205
    el.append(_line(205, 130, 205, 250, color=INK, sw=1.5, dash="3,2"))
    el.append(txt(100, 194, "燃烧室 M<1", size=10.5, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(205, 126, "喉部 M = 1.0（音速咽喉）", size=10, color=RED, anchor="middle", weight="700"))
    el.append(txt(306, 194, "扩张段 M>3!", size=11, color="#ffffff", anchor="middle", weight="700"))
    # Exhaust velocity arrow
    el.append(_line(368, 190, 410, 190, color=BLUE, sw=2.6, marker_end="arr-blue"))
    # Forward reaction thrust arrow on chamber head
    el.append(_line(92, 134, 50, 134, color=GREEN, sw=2.8))
    el.append(txt(126, 268, "红区：高温高压乱撞热能 (3500 K)", size=9.6, color=RED, anchor="middle", weight="600"))
    el.append(txt(322, 268, "蓝区：降温减压→定向超音速动能!", size=9.6, color=BLUE, anchor="middle", weight="700"))

    # Formula & physical insight box at bottom of Left Card
    el.append(card(36, 294, 384, 146, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(48, 315, "可压缩流体面积—速度反转定律：", size=11.5, color=ORANGE, weight="700"))
    el.append(txt(228, 338, "(1 − M²) · (dv / v) = − (dA / A)", size=12, color=INK, anchor="middle", weight="700"))
    el.append(txt(48, 362, "• 前半截亚音速 (M < 1)：1−M² > 0，像捏扁浇花水管，管子越细流得越快；", size=10.2, color=BODY))
    el.append(txt(48, 383, "• 喉部卡死 M = 1 后进入超音速 (M > 1)：1−M² 变成负数！气体剧烈膨胀", size=10.2, color=BODY))
    el.append(txt(48, 402, "  密度暴跌，喇叭口越敞开 (dA > 0)，喷气速度 v 反而一路狂飙破 3–4.5 km/s！", size=10.2, color=RED, weight="700"))
    el.append(txt(48, 424, "• 广义推力公式：F = ṁ·ve + (pe − p0)·Ae（动量推力 + 喷口压差推力）", size=10.2, color=BLUE, weight="700"))

    # Right Card: Sea-Level Short Nozzle vs Vacuum Giant Bell Nozzle
    el.append(card(448, 68, 290, 386, fill=CARD_BG))
    el.append(step_badge(468, 90, 2, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(486, 95, "为什么一级短喷管、二级大裙摆？", size=12, color=INK, weight="700"))

    regimes = [
        ("① 海平面一级发动机（短小喷口 ε≈16）", BLUE, BLUE_SOFT, [
            "地面大气压 p0 = 1 atm 顶着喷口：",
            "必须收短喇叭让出口压 pe ≈ 1 atm，",
            "羽流笔直紧束，推力扎实不抖动！",
        ]),
        ("② 太空二级发动机（巨型钟罩 ε≈165）", PURPLE, PURPLE_SOFT, [
            "高空真空 p0 ≈ 0，毫无空气背压：",
            "接上巨大铌合金裙摆把燃气榨干到极致，",
            "猎鹰9同款核心机比冲从 282s 飙到 348s！",
        ]),
        ("③ 禁忌反例：把真空大喷管放地面点火！", RED, RED_SOFT, [
            "口太大导致 pe 远低于外界 1 atm →",
            "大气强行倒灌进喷管壁引发“过膨胀分离”，",
            "剧烈侧向狂抖，几秒钟撕碎整台发动机！",
        ]),
    ]
    ry = 112
    for r_title, fg_c, bg_c, r_lines in regimes:
        el.append(card(460, ry, 266, 102, rx=8, fill=bg_c, stroke=fg_c))
        el.append(txt(472, ry + 21, r_title, size=10.8, color=fg_c, weight="700"))
        for i_l, ln in enumerate(r_lines):
            el.append(txt(472, ry + 43 + i_l * 19, ln, size=10.1, color=INK if i_l == 2 else BODY, weight="600" if i_l == 2 else "400"))
        ry += 112

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            491,
            "多级火箭的第一个隐形红利：不仅扔掉死重，还能在地面和太空分别换上“专属尺寸”的最佳膨胀比喷管！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "火箭真空反推原理、拉瓦尔喷管超音速反转与海平面及真空喷管对比图",
        "左图展示拉瓦尔收缩扩张喷管在喉部达到M=1音速后利用(1-M^2)符号反转将3500K热能转化为超音速射流；右图对比一级短喷管(膨胀比16)、二级真空大喷管(膨胀比165)及地面过膨胀流分离破坏。",
        el,
    )
    write_svg(SUBDIR, "thrust-and-delaval-nozzle.svg", svg)


def build_fig2_turbopump_and_propellants():
    """Fig 2: Turbopump + Regenerative cooling anatomy & Propellant Isp vs Density trade-off."""
    el = []
    el.extend(
        header(
            "第二关：每秒狂吞两吨半油的“涡轮泵心脏”，以及一级煤油、二级液氢的绝配",
            "3500 K 烈火比钢熔点高近两千度怎么不烧穿？靠零下两百度的燃料先给铜壁“洗冷水澡”！",
        )
    )

    # Left Card: Liquid Rocket Engine Plumbing (Turbopump + Regenerative Cooling + Open vs Staged Cycle)
    el.append(card(22, 68, 370, 386, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=RED, bg=RED_SOFT))
    el.append(txt(60, 95, "液体发动机解剖：涡轮泵增压与“再生冷却”", size=12, color=INK, weight="700"))

    # Schematic diagram box
    el.append(card(36, 112, 342, 188, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    # Two tanks top left: LOX (blue) & Fuel (orange)
    el.append(f'<rect x="50" y="124" width="66" height="36" rx="6" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
    el.append(txt(83, 146, "液氧箱 LOX", size=10, color=BLUE, anchor="middle", weight="700"))

    el.append(f'<rect x="130" y="124" width="66" height="36" rx="6" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.8"/>')
    el.append(txt(163, 146, "低温燃料箱", size=10, color=ORANGE, anchor="middle", weight="700"))

    # Central Turbopump assembly
    el.append(f'<rect x="64" y="182" width="120" height="34" rx="14" fill="#ffffff" stroke="{PURPLE}" stroke-width="2.2"/>')
    el.append(txt(124, 203, "高速涡轮泵 (3万转/分)", size=10, color=PURPLE, anchor="middle", weight="700"))
    el.append(_line(83, 160, 88, 182, color=BLUE, sw=2.0, marker_end="arr-blue"))
    el.append(_line(163, 160, 158, 182, color=ORANGE, sw=2.0, marker_end="arr-orange"))

    # Right side inside schematic: Combustion chamber + Cooling jacket loop!
    el.append(f'<path d="M242,154 L294,154 L294,188 L278,208 L308,266 L228,266 L258,208 L242,188 Z" fill="#fee2e2" stroke="{RED}" stroke-width="2.2"/>')
    el.append(txt(268, 178, "3500 K", size=10, color=RED, anchor="middle", weight="700"))
    el.append(txt(268, 250, "主燃烧室", size=10, color=RED, anchor="middle", weight="700"))

    # Regenerative cooling loop arrow from pump -> nozzle wall -> injector head!
    el.append(
        f'<path d="M184,202 L222,258 L248,208 L234,142 L268,142 L268,154" '
        f'fill="none" stroke="{TEAL}" stroke-width="2.2" stroke-dasharray="4,2"/>'
    )
    el.append(txt(136, 246, "再生冷却回路：", size=10.2, color=TEAL, anchor="middle", weight="700"))
    el.append(txt(136, 264, "冰冷燃料先流经喷管夹层", size=9.8, color=BODY, anchor="middle"))
    el.append(txt(136, 281, "吸热降温后再喷入炉膛！", size=9.8, color=INK, anchor="middle", weight="600"))

    # Bottom comparison: Open Gas-Generator vs Closed Staged Combustion
    el.append(card(36, 312, 342, 128, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(48, 333, "涡轮泵动力哪儿来？（决定发动机代差的分水岭）", size=11, color=PURPLE, weight="700"))
    el.append(txt(48, 355, "• 土星五号单台 F-1 涡轮泵高达 5.5 万马力，每秒吞油 2.58 吨！", size=10, color=INK, weight="700"))
    el.append(txt(48, 376, "• 燃气发生器开式循环（F-1/梅林）：抽 ~2% 燃料吹完涡轮直接排掉，", size=10, color=BODY))
    el.append(txt(48, 394, "  结构轻巧耐造，但损失少许比冲（喷管旁常冒一缕黑烟）；", size=10, color=MUTED))
    el.append(txt(48, 415, "• 高压补燃闭式循环（长五 YF-100/星舰猛禽）：吹完涡轮的尾气", size=10, color=BODY))
    el.append(txt(48, 432, "  100% 压回主燃烧室烧尽，零浪费，压榨出极限比冲！", size=10, color=GREEN, weight="700"))

    # Right Card: Four Propellant Families ("大力士" vs "长跑冠军")
    el.append(card(406, 68, 332, 386, fill=CARD_BG))
    el.append(step_badge(426, 90, 2, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(444, 95, "推进剂分工：为什么一级烧煤油、上面级烧液氢？", size=11.8, color=INK, weight="700"))

    el.append(card(418, 112, 308, 66, rx=8, fill=GOLD_SOFT, stroke=GOLD))
    el.append(txt(572, 133, "热力学铁律：排气速度 ve ∝ √(燃烧温度 Tc / 燃气分子量 M)", size=10.2, color=GOLD, anchor="middle", weight="700"))
    el.append(txt(572, 153, "分子量 M 越轻 → 喷气越快（比冲 Isp 越高，越省油）！", size=10.2, color=INK, anchor="middle", weight="600"))
    el.append(txt(572, 170, "燃料密度 ρ 越高 → 油箱越小巧（起飞迎风阻力与结构死重越小）！", size=9.8, color=BODY, anchor="middle"))

    # 4 horizontal comparison bars for Vacuum Isp & Bulk Density
    fuels = [
        ("① 固体推进剂（助推器大力士）", "真空比冲 ~265 s｜密度 1800 kg/m³（推力猛、难关机）", 150, SLATE),
        ("② 液氧 + 煤油（一级起飞王牌）", "真空比冲 ~335 s｜密度 1030 kg/m³（长五助推/猎鹰9）", 192, ORANGE),
        ("③ 液氧 + 甲烷（复用火箭新星）", "真空比冲 ~370 s｜密度 820 kg/m³（不积碳易洗刷）", 214, BLUE),
        ("④ 液氧 + 液氢（高空长跑霸主）", "真空比冲 ~445 s!｜液氢仅 71 kg/m³（极轻但占大肚子）", 262, PURPLE),
    ]
    fy = 190
    for f_name, f_sub, bar_w, f_col in fuels:
        el.append(txt(424, fy + 14, f_name, size=10.6, color=f_col, weight="700"))
        el.append(f'<rect x="424" y="{fy + 20}" width="{bar_w}" height="12" rx="6" fill="{f_col}" opacity="0.85"/>')
        el.append(txt(424, fy + 47, f_sub, size=9.8, color=BODY))
        fy += 64

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(
        txt(
            380,
            491,
            "多级火箭的第二个黄金分工：底层用高密度煤油/固推“猛力拔地抗重力”，高层用轻分子液氢“超高比冲冲刺入轨”！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "液体火箭发动机涡轮泵再生冷却结构与四大推进剂比冲密度对比图",
        "左图剖析高速涡轮泵增压、低温燃料流经喷管夹层吸热的再生冷却及开式与高压补燃闭式循环；右图基于排气速度反比于分子量平方根解释固体、液氧煤油、液氧甲烷与液氧液氢在多级火箭中的分工。",
        el,
    )
    write_svg(SUBDIR, "turbopump-and-propellant-chemistry.svg", svg)


def build_fig3_tsiolkovsky_staging_math():
    """Fig 3: Exact computed Tsiolkovsky staging comparison: 300t rocket SSTO (0t!) vs 2-stage (8.7t) vs 3-stage (11.8t)."""
    el = []
    el.extend(
        header(
            "第三关：火箭方程的“指数暴政”——为什么不造一枚单级火箭直飞太空？",
            "算一笔硬核死账：同样 300 吨起飞、7% 结构死重，单级火箭连空铁皮都飞不上去，切两级立送 8.1 吨卫星！",
        )
    )

    # Left Card: Computed Delta-v vs Payload Curves for 1-Stage, 2-Stage, 3-Stage (m0=300t, ve=3100m/s, eps=0.07)
    el.append(card(22, 68, 434, 386, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 95, "300 吨液氧煤油火箭实算对比（ve = 3100 m/s，结构比 ε = 7%）", size=11.8, color=INK, weight="700"))

    # Plot axes: x = Payload mass m_pay from 0 to 20 tons -> [84 .. 424] (width 340)
    # y = Achievable Delta-v from 5,000 to 12,000 m/s -> [386 .. 126] (height 260)
    px0, px1 = 84.0, 424.0
    py0, py1 = 386.0, 126.0

    def map_pt(mpay, dv):
        x = px0 + (mpay / 20.0) * (px1 - px0)
        y = py0 - ((dv - 5000.0) / 7000.0) * (py0 - py1)
        return (x, y)

    # Gridlines & axes
    for dv_tick in (6000, 8000, 9300, 11000):
        _, gy = map_pt(0, dv_tick)
        is_leo = dv_tick == 9300
        el.append(_line(px0, gy, px1, gy, color=RED if is_leo else "#e2e8f0", sw=1.8 if is_leo else 1.0, dash="5,3" if is_leo else None))
        el.append(txt(px0 - 6, gy + 4, f"{dv_tick/1000:.1f}", size=9.8, color=RED if is_leo else MUTED, anchor="end", weight="700" if is_leo else "400"))

    for m_tick in (0, 5, 10, 15, 20):
        gx, _ = map_pt(m_tick, 5000)
        el.append(_line(gx, py0, gx, py0 + 4, color=SLATE, sw=1.2))
        el.append(txt(gx, py0 + 17, f"{m_tick}t", size=9.8, color=MUTED, anchor="middle"))

    el.append(_line(px0, py1, px0, py0, color=SLATE, sw=1.5))
    el.append(_line(px0, py0, px1, py0, color=SLATE, sw=1.5))
    el.append(txt(42, 256, "总 Δv", size=10, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(42, 272, "(km/s)", size=9.5, color=MUTED, anchor="middle"))
    el.append(txt(254, 422, "送入近地轨道的卫星有效载荷质量 m_pay（吨）", size=10.5, color=INK, anchor="middle", weight="600"))

    # Highlight LEO threshold line at 9.3 km/s
    _, y_leo = map_pt(0, 9300)
    el.append(txt(436, y_leo - 7, "入轨生死线 Δv = 9.3 km/s", size=9.8, color=RED, anchor="end", weight="700", halo=True))

    # Compute exact curves for N = 1, 2, 3 stages:
    # Given m_pay, lambda_stage = (m_pay / m0) ** (1/N), R_stage = 1 / (eps + (1 - eps) * lambda_stage), dv = N * ve * ln(R_stage)
    m0, ve, eps = 300.0, 3100.0, 0.07
    curves_spec = [
        (1, SLATE, "2,2", "单级火箭 (SSTO)"),
        (2, BLUE, None, "两级串联接力"),
        (3, GREEN, None, "三级串联接力"),
    ]
    for n_st, col_c, dsh, _ in curves_spec:
        pts = []
        for i in range(101):
            mp = 0.05 + i * (19.95 / 100.0)
            lam = (mp / m0) ** (1.0 / n_st)
            r_st = 1.0 / (eps + (1.0 - eps) * lam)
            dv_val = n_st * ve * math.log(r_st)
            if 5000.0 <= dv_val <= 12000.0:
                pts.append(map_pt(mp, dv_val))
        # Also add m_pay -> 0 point for N=1 (dv = 8244 m/s!)
        if n_st == 1:
            pts.insert(0, map_pt(0.0, ve * math.log(1.0 / eps)))
        el.append(polyline(pts, color=col_c, sw=2.6, dash=dsh))

    # Mark exact critical intersections!
    # 1) N=1 at m_pay = 0 -> 8,244 m/s (FAILS to reach 9,300 m/s!)
    x_ssto, y_ssto = map_pt(0.0, ve * math.log(1.0 / eps))
    el.append(f'<circle cx="{x_ssto:.1f}" cy="{y_ssto:.1f}" r="5" fill="{RED}"/>')
    el.append(txt(x_ssto + 10, y_ssto + 14, "单级极限仅 8.24 km/s（0吨卫星也坠毁！）", size=9.8, color=SLATE, weight="700", halo=True))

    # 2) N=2 at dv = 9300 -> pay_2 = 8.66 t
    pay2 = _max_payload_n_stages(m0, 9300.0, ve, eps, 2)
    x2, y2 = map_pt(pay2, 9300.0)
    el.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="5.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(x2 - 6, y2 + 20, f"两级入轨：{pay2:.1f} 吨！", size=10, color=BLUE, anchor="end", weight="700", halo=True))

    # 3) N=3 at dv = 9300 -> pay_3 = 9.86 t
    pay3 = _max_payload_n_stages(m0, 9300.0, ve, eps, 3)
    x3, y3 = map_pt(pay3, 9300.0)
    el.append(f'<circle cx="{x3:.1f}" cy="{y3:.1f}" r="5.5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(x3, y3 - 11, f"三级：{pay3:.1f} 吨", size=9.8, color=GREEN, anchor="middle", weight="700", halo=True))

    # Right Card: Why "Fuel Carrying Fuel" Ruins Single-Stage & Why Not 10 Stages?
    el.append(card(470, 68, 268, 386, fill=CARD_BG))
    el.append(step_badge(490, 90, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(508, 95, "“燃料背燃料”恶性循环与分级甜点", size=11.8, color=INK, weight="700"))

    el.append(card(482, 112, 244, 158, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(494, 133, "单级火箭死在哪儿？", size=11, color=ORANGE, weight="700"))
    el.append(txt(494, 155, "• 要装 279 吨燃料，必须造一个承重近", size=10, color=BODY))
    el.append(txt(494, 174, "  300 吨的巨型金属桶（干重 ~20 吨）；", size=10, color=BODY))
    el.append(txt(494, 194, "• 到了最后 10 秒，桶早空了，发动机却还", size=10, color=BODY))
    el.append(txt(494, 213, "  在拼命给这 20 吨废铁皮加速到 8 km/s！", size=10, color=RED, weight="700"))
    el.append(txt(494, 235, "• 多级精髓：油烧光瞬间把十几吨空铁桶", size=10, color=BODY))
    el.append(txt(494, 254, "  一脚踹掉，总速度变成各级 Δv 直接相加！", size=10, color=GREEN, weight="700"))

    el.append(card(482, 282, 244, 158, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(494, 303, "那切成 10 级岂不是更省油？", size=11, color=PURPLE, weight="700"))
    el.append(txt(494, 325, "• 边际收益骤降：从 1 级变 2 级是从 0 到", size=10, color=BODY))
    el.append(txt(494, 344, "  8.1 吨的质变；3 级变 4 级仅多几百公斤；", size=10, color=BODY))
    el.append(txt(494, 365, "• 级间代价反噬：每多一级就多一套独立", size=10, color=BODY))
    el.append(txt(494, 384, "  发动机、涡轮泵、级间环和爆炸螺栓死重，", size=10, color=BODY))
    el.append(txt(494, 403, "  高空点火与分离故障率还会成倍叠加！", size=10, color=RED, weight="600"))
    el.append(txt(494, 424, "→ 全球运载火箭黄金甜点：2 级 ～ 3.5 级！", size=10.2, color=BLUE, weight="700"))

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            491,
            "齐奥尔科夫斯基名言：“地球是人类的摇篮，但没有一枚单级化学火箭能带人类离开摇篮——唯有靠多级火箭列车！”",
            size=11.3,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "齐奥尔科夫斯基火箭方程单级死锁与二三级接力运力实算对比图",
        "左图按300吨总重、排气速度3100m/s与7%结构系数精确绘制单级(最高8.24km/s无法入轨)、两级(入轨载荷8.1吨)与三级(9.9吨)的速度载荷曲线；右图解释空贮箱死重拖累与2至3.5级工程最优区间。",
        el,
    )
    write_svg(SUBDIR, "tsiolkovsky-tyranny-and-staging-curve.svg", svg)


def build_fig4_staging_relay_and_hot_cold_anim():
    """Fig 4: Animated 1-shot multi-stage ascent sawtooth g-load curve + Cold vs Hot Staging mechanics."""
    extra_css = """
  .st-p1 { opacity: 1; animation: stFade1 7.0s ease-out 0.2s 1 forwards; }
  .st-p2 { opacity: 0.35; animation: stFade2 7.0s ease-out 0.2s 1 forwards; }
  .st-p3 { opacity: 0.35; animation: stFade3 7.0s ease-out 0.2s 1 forwards; }
  .g-dot { opacity: 0; animation: dotShow 7.0s ease-out 0.2s 1 forwards; }
  @keyframes stFade1 {
    0%, 33% { opacity: 1; }
    34%, 92% { opacity: 0.85; }
    100% { opacity: 1; }
  }
  @keyframes stFade2 {
    0%, 32% { opacity: 0.3; }
    33%, 66% { opacity: 1; }
    67%, 92% { opacity: 0.85; }
    100% { opacity: 1; }
  }
  @keyframes stFade3 {
    0%, 65% { opacity: 0.3; }
    66%, 100% { opacity: 1; }
  }
  @keyframes dotShow {
    0%, 70% { opacity: 0; }
    85%, 100% { opacity: 1; }
  }
  @media (prefers-reduced-motion: reduce) {
    .st-p1, .st-p2, .st-p3, .g-dot { animation: none !important; opacity: 1 !important; }
  }
"""
    el = []
    el.extend(
        header(
            "第四关：10 分钟高空换挡实录——“锯齿形过载曲线”与失重状态怎么点火？",
            "为什么宇航员感觉推背感一浪高过一浪又突然归零？一级刚关机燃料全飘起来，二级怎么防吸空爆炸？",
        )
    )

    # Top Wide Card: Sawtooth Acceleration (g-load) & Velocity Relay Timeline across 0..600s
    el.append(card(22, 68, 716, 212, fill=CARD_BG))
    el.append(step_badge(42, 88, 1, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 93, "多级火箭标志性指纹：过载加速度“锯齿波”（推力恒定，越烧越轻→过载猛涨，换级瞬间跌零！）", size=11.5, color=INK, weight="700"))

    # Plot area x=[74..710], y=[242..126] (g from 0g to 4.5g)
    ax0, ax1 = 74.0, 710.0
    ay0, ay1 = 242.0, 126.0

    def map_g(t_sec, g_val):
        x = ax0 + (t_sec / 600.0) * (ax1 - ax0)
        y = ay0 - (g_val / 4.5) * (ay0 - ay1)
        return (x, y)

    for g_tick in (0, 1, 2, 3, 4):
        _, gy = map_g(0, g_tick)
        el.append(_line(ax0, gy, ax1, gy, color="#e2e8f0" if g_tick else SLATE, sw=1.0 if g_tick else 1.4))
        el.append(txt(ax0 - 8, gy + 4, f"{g_tick}g", size=9.8, color=MUTED, anchor="end"))

    el.append(_line(ax0, ay1, ax0, ay0, color=SLATE, sw=1.4))
    for t_tick, t_lbl in [(0, "0s 点火"), (156, "156s 换级"), (220, "220s 抛罩"), (420, "420s 二级关机"), (580, "580s 三级入轨!")]:
        tx, _ = map_g(t_tick, 0)
        el.append(_line(tx, ay0, tx, ay0 + 4, color=SLATE, sw=1.2))
        el.append(txt(tx, ay0 + 18, t_lbl, size=9.6, color=INK if t_tick in (156, 580) else MUTED, anchor="middle", weight="600" if t_tick in (156, 580) else "400"))

    # Stage 1 sawtooth: t=0 (1.35g) -> t=70 Max-Q throttle dip -> t=156 (3.95g) -> drop to 0g at t=160!
    pts_s1 = [map_g(t, g) for t, g in [(0, 1.35), (55, 1.85), (75, 1.65), (120, 2.65), (156, 3.95), (160, 0.05)]]
    # Stage 2 sawtooth: t=166 (0.95g) -> t=220 fairing drop jump -> t=416 (3.4g) -> drop to 0g at t=422!
    pts_s2 = [map_g(t, g) for t, g in [(160, 0.05), (168, 0.95), (220, 1.25), (224, 1.38), (330, 2.2), (416, 3.4), (422, 0.05)]]
    # Stage 3 sawtooth: t=428 (0.85g) -> t=580 (2.9g SECO orbital insertion v = 7.8 km/s!)
    pts_s3 = [map_g(t, g) for t, g in [(422, 0.05), (428, 0.85), (510, 1.65), (580, 2.95)]]

    el.append(f'<g class="st-p1">{polyline(pts_s1, color=ORANGE, sw=3.0)}'
              f'{txt(154, 118, "① 一级/助推猛推 (v→2.4 km/s)", size=9.8, color=ORANGE, anchor="middle", weight="700")}</g>')
    el.append(f'<g class="st-p2">{polyline(pts_s2, color=BLUE, sw=3.0)}'
              f'{txt(340, 118, "② 二级接力 + 抛罩 (v→5.6 km/s)", size=9.8, color=BLUE, anchor="middle", weight="700")}</g>')
    el.append(f'<g class="st-p3">{polyline(pts_s3, color=GREEN, sw=3.0)}'
              f'{txt(548, 118, "③ 末级冲刺入轨 (v = 7.8 km/s!)", size=9.8, color=GREEN, anchor="middle", weight="700")}</g>')

    gx_end, gy_end = map_g(580, 2.95)
    el.append(f'<circle class="g-dot" cx="{gx_end:.1f}" cy="{gy_end:.1f}" r="5.5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/>')

    # Bottom Left Card: Cold Staging + Ullage Settling Thrusters (冷分离 + 正推沉底火箭)
    el.append(card(22, 292, 350, 162, fill=CARD_BG))
    el.append(step_badge(42, 314, 2, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 319, "高空换挡方案 A：冷分离 + 正推沉底", size=12, color=INK, weight="700"))

    el.append(txt(40, 344, "• 生死隐患：一级刚熄火瞬间进入失重，二级油箱里", size=10.2, color=BODY))
    el.append(txt(40, 363, "  几十吨液氧煤油全飘成悬浮气泡！涡轮泵一旦吸入气体", size=10.2, color=BODY))
    el.append(txt(40, 382, "  会瞬间超速飞车甚至炸毁发动机！", size=10.2, color=RED, weight="700"))
    el.append(txt(40, 404, "• 冷分离三步曲（土星五号 / 猎鹰 9 号）：", size=10.2, color=BLUE, weight="700"))
    el.append(txt(40, 423, "  ① 一级关机解锁推开 → ② 点燃小型“正推火箭/冷气”", size=10, color=BODY))
    el.append(txt(40, 441, "  制造微重力把液体压回箱底吸口 → ③ 二级主引擎点火！", size=10, color=INK, weight="600"))

    # Bottom Right Card: Hot Staging ("热分离 / 笼式级间环直喷点火")
    el.append(card(388, 292, 350, 162, fill=CARD_BG))
    el.append(step_badge(408, 314, 3, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(426, 319, "高空换挡方案 B：惊心动魄的“热分离”", size=12, color=INK, weight="700"))

    el.append(txt(406, 344, "• 暴力美学（联盟号 / 长征二号F / SpaceX 星舰）：", size=10.2, color=ORANGE, weight="700"))
    el.append(txt(406, 363, "  根本不等一级脱开！在一级推力即将结束前最后 1～2 秒，", size=10.2, color=BODY))
    el.append(txt(406, 382, "  二级主发动机直接对着镂空网格级间环喷火点燃！", size=10.2, color=INK, weight="700"))
    el.append(txt(406, 404, "• 两大奇效：① 借一级残余推力天然压实液面，省掉沉底", size=10.2, color=BODY))
    el.append(txt(406, 423, "  小火箭；② 彻底消灭几秒钟无动力掉速（重力损耗），", size=10.2, color=BODY))
    el.append(txt(406, 441, "  星舰改用热分离后近地轨道运力直接暴涨约 10%！", size=10.2, color=GREEN, weight="700"))

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(
        txt(
            380,
            491,
            "并联捆绑 vs 串联叠罗汉：四周助推器与芯一级地面同时点火叫“并联半级”，头顶一级接一级点叫“串联分级”！",
            size=11.3,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "多级火箭升空锯齿形过载时间曲线动画与冷分离及热分离原理对比",
        "上图通过单次分段动画展示三级接力升空过程中因推进剂消耗质量减轻导致的锯齿状过载上升与换级归零曲线；下图对比防失重吸空的冷分离正推沉底法与镂空级间环热分离直喷点火法。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "multistage-ascent-relay-anim.svg", svg)


def build_fig5_three_iconic_rockets():
    """Fig 5: Architectural comparison of Saturn V, Long March 5, and Reusable Falcon 9 Block 5."""
    el = []
    el.extend(
        header(
            "第五关：三代经典运载火箭动力架构同台拆解——从一次性登月巨兽到垂直回收",
            "把前面四关物理拼在一起，看懂人类三条标志性技术路线怎样各自驯服火箭方程！",
        )
    )

    cols = [
        (
            22,
            "① 土星五号 (Saturn V)",
            "三级纯串联登月巨兽｜起飞 2,965 吨",
            ORANGE,
            ORANGE_SOFT,
            [
                ("一级 S-IC（大力拔地）", "5 台 F-1 液氧煤油机｜推力 3400 吨，150秒烧掉 2214 吨油"),
                ("二级 S-II（高空接力）", "5 台 J-2 液氧液氢机｜真空比冲 424 s，轻分子高比冲横扫中段"),
                ("三级 S-IVB（入轨+奔月）", "1 台 J-2 液氧液氢机｜二次点火把阿波罗飞船推上奔月轨道"),
                ("LEO 运力与历史定位", "近地轨道 140 吨（约占起飞重 4.7%）｜人类载人深空串联教科书"),
            ],
        ),
        (
            266,
            "② 长征五号（中国“胖五”）",
            "并联助推 + 氢氧芯级｜起飞 852 吨",
            RED,
            RED_SOFT,
            [
                ("4 枚助推器（零级重拳）", "8 台 YF-100 高压补燃液氧煤油机｜贡献起飞 90% 推力（960 吨）！"),
                ("5 米芯一级（氢氧长跑）", "2 台 YF-77 液氧液氢机｜地面与助推同点，真空比冲高达 428 s"),
                ("芯二级（真空精推）", "2 台 YF-75D 膨胀循环氢氧机｜比冲 ~442 s，送天和核心舱与嫦娥"),
                ("LEO 运力与技术亮点", "近地轨道 25 吨｜煤油高推重比与液氢超高比冲混搭的典范！"),
            ],
        ),
        (
            510,
            "③ 猎鹰 9 号 (Falcon 9 B5)",
            "两级液氧煤油 + 一级回收｜起飞 549 吨",
            BLUE,
            BLUE_SOFT,
            [
                ("一级（9 机并联+复用）", "9 台梅林 1D 液氧煤油机（ε≈16）｜刻意提早分离留 ~10% 返航油"),
                ("二级（单机大裙摆冲刺）", "1 台真空梅林 MVac（ε=165!）｜比冲跃升至 348 s 独自完成入轨"),
                ("一级三脚刹车回收术", "高空掉头→再入减速点火→单机悬停“自杀式着陆点火 (TWR>1)”"),
                ("运力代价换成本革命", "不回收运力 22.8 吨 → 海上回收 17.5 吨｜牺牲 23% 运力省下整级箭！"),
            ],
        ),
    ]

    for x0, c_title, c_sub, fg_c, bg_c, items in cols:
        el.append(card(x0, 68, 228, 386, fill=CARD_BG))
        el.append(card(x0 + 10, 78, 208, 52, rx=8, fill=bg_c, stroke=fg_c))
        el.append(txt(x0 + 114, 98, c_title, size=11.5, color=fg_c, anchor="middle", weight="700"))
        el.append(txt(x0 + 114, 118, c_sub, size=9.6, color=INK, anchor="middle", weight="600"))

        iy = 140
        for it_head, it_body in items:
            el.append(f'<rect x="{x0 + 10}" y="{iy}" width="208" height="72" rx="6" fill="{SLATE_SOFT}" stroke="{BORDER}" stroke-width="1"/>')
            el.append(txt(x0 + 18, iy + 18, it_head, size=10.3, color=fg_c, weight="700"))
            # Split it_body into 2 clean lines around 15-17 chars
            mid = len(it_body) // 2
            # Find nearest punctuation or split cleanly
            split_pos = it_body.find("｜")
            if split_pos != -1:
                l1 = it_body[:split_pos]
                l2 = it_body[split_pos + 1:]
            else:
                l1 = it_body[:16]
                l2 = it_body[16:]
            el.append(txt(x0 + 18, iy + 39, l1, size=9.6, color=BODY))
            el.append(txt(x0 + 18, iy + 57, l2, size=9.6, color=INK, weight="600"))
            iy += 78

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            491,
            "殊途同归的动力哲学：无论构型如何演变，“拉瓦尔超音速喷管 + 高比冲推进剂 + 分级甩死重”永远是入轨三大支柱！",
            size=11.3,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "土星五号、长征五号与猎鹰9号三大经典多级运载火箭动力架构对比图",
        "三栏并列拆解土星五号三级纯串联(F-1煤油+J-2氢氧)、长征五号并联煤油助推加氢氧芯级、以及猎鹰9号两级同源煤油机配合预留余油垂直反推回收的动力系统参数与工程取舍。",
        el,
    )
    write_svg(SUBDIR, "three-famous-rockets-architecture.svg", svg)


@register("multistage-rocket", "发射卫星多级火箭动力原理原创图解集", "science_tech")
def build_all():
    _verify_propulsion_and_staging_physics()
    build_fig1_thrust_and_delaval_nozzle()
    build_fig2_turbopump_and_propellants()
    build_fig3_tsiolkovsky_staging_math()
    build_fig4_staging_relay_and_hot_cold_anim()
    build_fig5_three_iconic_rockets()
