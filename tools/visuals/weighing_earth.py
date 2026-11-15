"""
Visuals for '新文章：详细介绍下 地球的重量可以通过引力测试，另外有哪些有趣的地球重量测试方法'
(Comprehensive Visual Guide to Weighing the Earth:
1. The GM Product Lock & Precision Gap [Why Apple/Moon only give GM, CODATA 2022 10,000x gap],
2. Schiehallion Mountain Plumb-Line [Maskelyne 1774 11.6'' & Hutton 1778 Contours] vs Harton Coal Mine Pendulum [Airy 1854 -383 m Faster Clock],
3. Cavendish's 1798 Sealed-Shed Torsion Balance & Optical Amplification [1-shot CSS animation + prefers-reduced-motion],
4. Four Ingenious Gravitational Setups [Jolly 1881 25 m Tower Balance, LAGEOS + GRACE-FO Satellites, Rosi 2014 Cold-Atom Fountain, HUST 2018 Dual Torsion Cave],
5. Weighing Earth WITHOUT Gravity via South Pole IceCube Neutrinos [Donini et al. 2018 Nature Physics] & Earth's Annual Cosmic Weight-Loss Ledger [Rojas et al. 2021]).

Generates 5 original 760px Chinese SVG diagrams in assets/images/weighing-earth/
with verified physical, astronomical, and particle-physics assertions.
"""
from __future__ import annotations

import math

from .core import (
    BLUE,
    BLUE_LINE,
    BLUE_SOFT,
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

TOPIC = "weighing-earth"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#d97706"
AMBER_SOFT = "#fffbeb"


def _txt(x, y, value, size=12, fill=INK, anchor="start", weight=None, halo=False, cls=None):
    return txt(x, y, value, size=size, color=fill, anchor=anchor, weight=weight, halo=halo, cls=cls)


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
    return f"""
    <marker id="arr-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{RED}"/>
    </marker>
    <marker id="arr-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{PURPLE}"/>
    </marker>
    <marker id="arr-teal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{TEAL}"/>
    </marker>
    """


# ---------------------------------------------------------------------------
# 1. The GM Product Lock & Precision Gap (760 x 505)
# ---------------------------------------------------------------------------
def build_gm_lock_and_precision() -> str:
    W, H = 760, 505
    # Physics verification (CODATA 2022 & IAU/IERS geocentric gravitational constant)
    mu_earth = 3.986004418e14  # m^3 / s^2
    G_codata = 6.67430e-11     # m^3 kg^-1 s^-2
    R_earth = 6.3710e6         # m
    M_earth = mu_earth / G_codata
    V_earth = (4.0 / 3.0) * math.pi * (R_earth ** 3)
    rho_earth = M_earth / V_earth
    assert 5.971e24 < M_earth < 5.973e24, f"Unexpected M_earth: {M_earth}"
    assert 5510 < rho_earth < 5518, f"Unexpected rho_earth: {rho_earth}"

    u_mu = 2.0e-9
    u_G = 2.2e-5
    ratio_gap = u_G / u_mu
    assert 9000 < ratio_gap < 12000

    parts = [
        *header(
            "为什么苹果落地和月亮绕地测不出地球质量？牛顿遭遇的 GM“乘积死锁”",
            "自由落体与卫星轨道只能测准乘积 G·M⊕；想拆开这把锁，必须搬来一块“已知质量的地面砝码”单测 G",
        ),
        # Step 1 top card: Apple + Satellite = GM lock
        card(22, 76, 716, 134),
        step_badge(42, 96, 1, BLUE, BLUE_SOFT),
        _txt(64, 101, "看落体与轨道：无论掉苹果还是发卫星，G 与地球质量 M⊕ 永远黏在一起", size=13.5, weight="700", fill=BLUE),
        # Left sub-box: Apple
        card(40, 114, 214, 82, fill=BLUE_SOFT, stroke="#93c5fd"),
        _txt(147, 136, "地面掉苹果：g = G·M⊕ / R⊕²", size=12, weight="700", fill=BLUE, anchor="middle"),
        _txt(147, 158, "已知 g ≈ 9.81 m/s²，R⊕ ≈ 6371 km", size=11, fill=INK, anchor="middle"),
        _txt(147, 178, "只能算出 G·M⊕，拆不出 M⊕！", size=11, weight="700", fill=RED, anchor="middle"),
        # Middle lock badge
        card(272, 114, 216, 82, fill=AMBER_SOFT, stroke="#fcd34d"),
        _txt(380, 136, "地心引力常数（乘积死锁）", size=12, weight="700", fill=AMBER, anchor="middle"),
        _txt(380, 158, "μ⊕ = G·M⊕ = 3.986004418×10¹⁴", size=11.5, weight="700", fill=INK, anchor="middle"),
        _txt(380, 178, "单位 m³/s²（有效数字高达 10 位！）", size=10.8, fill=MUTED, anchor="middle"),
        # Right sub-box: Moon / Satellite
        card(506, 114, 214, 82, fill=BLUE_SOFT, stroke="#93c5fd"),
        _txt(613, 136, "月球与卫星：4π²a³ / T² = G·M⊕", size=12, weight="700", fill=BLUE, anchor="middle"),
        _txt(613, 158, "被吸引物质量 m 在等式两边约掉了", size=11, fill=INK, anchor="middle"),
        _txt(613, 178, "同样只能锁死乘积 G·M⊕！", size=11, weight="700", fill=RED, anchor="middle"),

        # Step 2 middle card: Two fake Earths yielding identical g = 9.81 m/s^2
        card(22, 222, 716, 136),
        step_badge(42, 242, 2, ORANGE, ORANGE_SOFT),
        _txt(64, 247, "思想实验：如果不测 G，下面两颗假地球在地面产生的重力 g = 9.81 m/s² 一模一样！", size=13.2, weight="700", fill=ORANGE),
        # Fake Earth A
        card(40, 260, 216, 84, fill="#fff7ed", stroke="#fdba74"),
        '<circle cx="76" cy="302" r="24" fill="#fef3c7" stroke="#d97706" stroke-width="2" stroke-dasharray="4 3"/>',
        _txt(76, 306, "空心轻球", size=9.5, weight="700", fill=AMBER, anchor="middle"),
        _txt(180, 283, "假想 A：棉花糖轻地球", size=11.8, weight="700", fill=ORANGE, anchor="middle"),
        _txt(180, 304, "M⊕ 极小 × 引力常数 G 极大", size=11, fill=INK, anchor="middle"),
        _txt(180, 324, "乘积不变 ⇒ 苹果照样 9.81 落地", size=10.5, fill=MUTED, anchor="middle"),
        # Fake Earth B
        card(272, 260, 216, 84, fill=SLATE_SOFT, stroke="#94a3b8"),
        '<circle cx="308" cy="302" r="24" fill="#334155" stroke="#0f172a" stroke-width="2"/>',
        _txt(308, 306, "超重铅球", size=9.5, weight="700", fill="#ffffff", anchor="middle"),
        _txt(412, 283, "假想 B：纯锇重金属地球", size=11.8, weight="700", fill=INK, anchor="middle"),
        _txt(412, 304, "M⊕ 极大 × 引力常数 G 极小", size=11, fill=INK, anchor="middle"),
        _txt(412, 324, "乘积不变 ⇒ 月亮轨道分毫不差", size=10.5, fill=MUTED, anchor="middle"),
        # Unlock key box
        card(504, 260, 216, 84, fill=GREEN_SOFT, stroke="#86efac"),
        _txt(612, 282, "破局唯一钥匙：地面已知质量 m₀", size=11.8, weight="700", fill=GREEN, anchor="middle"),
        _txt(612, 303, "拿一座山或两颗铅球测出微弱引力", size=10.8, fill=INK, anchor="middle"),
        _txt(612, 323, "先定 G ⇒ M⊕ = (G·M⊕) / G 解锁！", size=11, weight="700", fill=GREEN, anchor="middle"),

        # Step 3 bottom card: Modern precision bottleneck bar chart (log scale)
        card(22, 370, 716, 118),
        step_badge(42, 390, 3, PURPLE, PURPLE_SOFT),
        _txt(64, 395, "直到今天：G 仍是物理学最难测准的基本常数，拖累地球质量止步于 5 位有效数字", size=13, weight="700", fill=PURPLE),
    ]

    # Plot effective precision digits (-log10 relative uncertainty) from 0 (x=232) to 10 (x=512)
    x_min, x_max = 232.0, 512.0
    def _ux(u_val: float) -> float:
        digits = -math.log10(u_val)
        return x_min + (digits / 10.0) * (x_max - x_min)

    x_mu = _ux(u_mu)  # ~8.70 digits
    x_g = _ux(u_G)    # ~4.66 digits

    parts.extend([
        _txt(42, 427, "乘积 μ⊕ = G·M⊕（激光卫星）", size=11.5, weight="700", fill=TEAL),
        f'<rect x="{x_min:.1f}" y="414" width="{x_mu - x_min:.1f}" height="18" rx="5" fill="{TEAL}"/>',
        _txt(x_mu + 8, 428, "相对误差 2×10⁻⁹（准到近 9 位数字！）", size=11, weight="700", fill=TEAL),

        _txt(42, 456, "引力常数 G（CODATA 2022）", size=11.5, weight="700", fill=RED),
        f'<rect x="{x_min:.1f}" y="443" width="{x_g - x_min:.1f}" height="18" rx="5" fill="{RED}"/>',
        _txt(x_g + 8, 457, "相对误差 2.2×10⁻⁵（差 1 万倍 ⇒ M⊕ ≈ 5.9722×10²⁴ kg）", size=11, weight="700", fill=RED),

        _txt(380, 479, "注：牛顿 1687 年在《原理》中盲猜地球平均密度是水的 5～6 倍，现代实测为 5.514 g/cm³，神级直觉！", size=10.8, fill=MUTED, anchor="middle"),
    ])

    return figure(
        H,
        "牛顿遭遇的 GM 乘积死锁与引力常数 G 精度瓶颈图",
        "展示自由落体与天体轨道只能测准地心引力常数 G·M⊕，假想轻球与重球可产生相同地面重力 g，以及 CODATA 2022 中 G·M⊕ 与 G 相差一万倍的不确定度鸿沟。",
        parts,
        extra_defs=_markers(),
        width=W,
    )


# ---------------------------------------------------------------------------
# 2. Schiehallion Mountain (1774) vs Airy Coal Mine (1854) (760 x 520)
# ---------------------------------------------------------------------------
def build_mountain_and_mine() -> str:
    W, H = 760, 520
    # Verify Maskelyne 1775 exact numbers (Phil. Trans. R. Soc.: 54".6 - 42".94 = 11".66, reported as 11".6)
    lat_astro = 54.6    # arcsec
    lat_trig = 42.94    # arcsec
    two_theta = lat_astro - lat_trig
    assert math.isclose(two_theta, 11.6, abs_tol=0.08)

    # Verify Airy 1854 Harton Colliery (-383 m) gravity increase sign
    d_mine = 383.0
    R_e = 6.371e6
    rho_shell = 2.50
    rho_mean = 5.514
    frac_dg = (d_mine / R_e) * (2.0 - 3.0 * rho_shell / rho_mean)
    assert frac_dg > 0, "Gravity at 383 m depth MUST increase because rho_shell < 2/3 rho_mean!"

    parts = [
        *header(
            "走出书房去称地球：1774 年借一座苏格兰孤峰，1854 年钻进 383 米深煤矿",
            "上山看铅垂线被山体拽歪 11.6 角秒（顺带发明等高线）；下井看摆钟因逼近铁核每天快走 2.24 秒",
        ),
        # Left Panel: Schiehallion 1774
        card(20, 76, 352, 424),
        step_badge(38, 96, 1, TEAL, TEAL_SOFT),
        _txt(60, 101, "1774 谢哈利恩山实验（马斯基林 & 赫顿）", size=13, weight="700", fill=TEAL),
        pill(40, 114, "天顶恒星测角 − 三角测量 = 11.6″ 偏角", TEAL, TEAL_SOFT, w=254),

        # Mountain illustration inside (36..356, y=150..320)
        _line(40, 292, 352, 292, stroke=SLATE, sw=1.8),
        # Symmetrical mountain peak at x=196, y=184
        '<path d="M 68,292 Q 132,286 164,218 Q 196,162 228,218 Q 260,286 324,292 Z" fill="#d1fae5" stroke="#0f766e" stroke-width="2"/>',
        # Contour rings hint on mountain
        '<path d="M 142,258 Q 196,244 250,258" fill="none" stroke="#0f766e" stroke-width="1.1" stroke-dasharray="4 3"/>',
        '<path d="M 164,224 Q 196,212 228,224" fill="none" stroke="#0f766e" stroke-width="1.1" stroke-dasharray="4 3"/>',
        _txt(196, 278, "孤峰岩石 ρ山 ≈ 2.5 g/cm³", size=10.5, weight="700", fill=TEAL, anchor="middle"),

        # South station (left x=88) and North station (right x=304)
        '<rect x="78" y="278" width="20" height="14" rx="2" fill="#0284c7"/>',
        _txt(88, 309, "南观测站", size=10.5, weight="700", fill=BLUE, anchor="middle"),
        # True vertical dashed vs deflected plumb line inward (exaggerated angle clearly labeled)
        _line(88, 162, 88, 278, stroke=SLATE, sw=1.3, dash="4 3"),
        _line(88, 224, 104, 276, stroke=RED, sw=2.0),
        '<circle cx="104" cy="276" r="3.5" fill="#dc2626"/>',
        _line(104, 266, 132, 266, stroke=RED, sw=1.6, marker="arr-red"),

        '<rect x="294" y="278" width="20" height="14" rx="2" fill="#0284c7"/>',
        _txt(304, 309, "北观测站", size=10.5, weight="700", fill=BLUE, anchor="middle"),
        _line(304, 162, 304, 278, stroke=SLATE, sw=1.3, dash="4 3"),
        _line(304, 224, 288, 276, stroke=RED, sw=2.0),
        '<circle cx="288" cy="276" r="3.5" fill="#dc2626"/>',
        _line(288, 266, 260, 266, stroke=RED, sw=1.6, marker="arr-red"),

        _txt(196, 166, "★ 天顶恒星视差 54.60″（角度为示意放大）", size=10.5, weight="700", fill=INK, anchor="middle"),

        # Calculation summary box left
        card(36, 322, 320, 164, fill=TEAL_SOFT, stroke="#99f6e4"),
        _txt(50, 344, "• 地面三角测量真纬度差：42.94″", size=11.2, fill=INK),
        _txt(50, 365, "• 铅垂线被山拽向内侧总偏角：54.60″ − 42.94″ = 11.6″", size=11.2, weight="700", fill=RED),
        _txt(50, 386, "• 地球引力 / 山体引力 ≈ 9933 : 1", size=11.2, fill=INK),
        _txt(50, 409, "• 意外副产品：数学家赫顿（1778）为切分山体体积，", size=10.8, fill=MUTED),
        _txt(50, 427, "  把相同海拔点连成细线——人类陆地“等高线”诞生！", size=10.8, weight="700", fill=TEAL),
        _txt(50, 451, "⇒ 测得地球平均密度 ρ⊕ ≈ 4.5 g/cm³（约现代值 82%）", size=11.3, weight="700", fill=TEAL),
        _txt(50, 471, "  一举击碎“地球空心说”，预言地心藏着重金属核！", size=10.8, fill=INK),

        # Right Panel: Airy 1854 Harton Colliery
        card(388, 76, 352, 424),
        step_badge(406, 96, 2, PURPLE, PURPLE_SOFT),
        _txt(428, 101, "1854 哈顿煤矿深井摆钟（艾里 Airy）", size=13, weight="700", fill=PURPLE),
        pill(408, 114, "下井 383 米：电报同步顶底双摆钟", PURPLE, PURPLE_SOFT, w=244),

        # Mine shaft + Earth shell schematic (404..724, y=150..320)
        # Outer crust band
        '<rect x="408" y="168" width="312" height="132" rx="10" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>',
        _txt(422, 188, "头顶 383 m 表层岩壳（ρ壳 ≈ 2.5 g/cm³）", size=10.5, weight="700", fill=SLATE),
        _txt(422, 205, "球壳定理：壳内各向引力相消 → 不再向下拉你", size=10.2, fill=MUTED),
        # Vertical shaft at x=596..636
        '<rect x="592" y="168" width="44" height="132" fill="#ffffff" stroke="#475569" stroke-width="1.8"/>',
        # Surface clock above shaft
        '<rect x="646" y="152" width="68" height="28" rx="5" fill="#eff6ff" stroke="#0284c7" stroke-width="1.5"/>',
        _txt(680, 170, "井口摆钟 g₀", size=10.2, weight="700", fill=BLUE, anchor="middle"),
        # Telegraph dashed line down shaft
        _line(614, 168, 614, 286, stroke=ORANGE, sw=1.8, dash="4 3"),
        _txt(584, 238, "电报线同步", size=10, weight="700", fill=ORANGE, anchor="end"),
        # Mine bottom clock
        '<rect x="646" y="268" width="68" height="28" rx="5" fill="#faf5ff" stroke="#7c3aed" stroke-width="1.5"/>',
        _txt(680, 286, "井底摆钟 g井", size=10.2, weight="700", fill=PURPLE, anchor="middle"),
        # Dense core glow below y=300
        '<path d="M 418,300 Q 564,274 710,300" fill="none" stroke="#dc2626" stroke-width="2.5"/>',
        _txt(515, 314, "脚下更靠近高密度铁镍地核（ρ⊕ > 1.5 ρ壳）！", size=10.5, weight="700", fill=RED, anchor="middle"),

        # Calculation summary box right
        card(404, 322, 320, 164, fill=PURPLE_SOFT, stroke="#d8b4fe"),
        _txt(418, 344, "• 直觉陷阱：下井后头顶少了一层石头，重力会变小吗？", size=11, weight="700", fill=INK),
        _txt(418, 365, "• 真相反转：离高密度地心近了 383 米，距离平方反比", size=11, fill=INK),
        _txt(418, 384, "  带来的引力增益，压倒了头顶轻岩壳归零的损失！", size=11, fill=INK),
        _txt(418, 407, "• 实测结果：井底重力比地面大 1 / 19286，", size=11.2, weight="700", fill=PURPLE),
        _txt(418, 426, "  井底摆钟每天比地面快走 2.24 秒！", size=11.2, weight="700", fill=RED),
        _txt(418, 451, "⇒ 推算地球平均密度 ρ⊕ ≈ 6.566 g/cm³", size=11.3, weight="700", fill=PURPLE),
        _txt(418, 471, "  （受矿区局部高密度岩层干扰略偏高，但方法极妙）", size=10.5, fill=MUTED),
    ]

    return figure(
        H,
        "1774 谢哈利恩山铅垂线实验与 1854 哈顿煤矿深井摆钟实验对比图",
        "左图展示马斯基林测得山体两侧铅垂线 11.6 角秒内偏角及赫顿等高线切分法；右图展示艾里在 383 米深煤矿井底测得摆钟每日快走 2.24 秒的壳层与地核竞争机制。偏角与井深比例为示意放大。",
        parts,
        extra_defs=_markers(),
        width=W,
    )


# ---------------------------------------------------------------------------
# 3. Cavendish 1798 Torsion Balance & Optical Amplification (760 x 535, 1-shot CSS anim)
# ---------------------------------------------------------------------------
def build_cavendish_torsion_balance() -> str:
    W, H = 760, 535
    # Exact Cavendish 1798 physics verification
    G = 6.67430e-11
    M_big = 158.0     # kg (348 lb)
    m_small = 0.73    # kg (1.61 lb)
    r_sep = 0.225     # m (8.85 in)
    F_grav = G * M_big * m_small / (r_sep ** 2)
    assert 1.4e-7 < F_grav < 1.9e-7, f"Unexpected F_grav: {F_grav}"
    sand_equiv_mg = (F_grav / 9.80665) * 1e6  # in mg * 1000 -> ug; wait: kg * 1e6 = mg!
    assert 0.014 < sand_equiv_mg < 0.020  # ~0.0155-0.0177 mg (~17 ug, one fine sand grain!)

    anim_css = """
  @keyframes cavTwist {
    0%, 14% { transform: rotate(-7deg); }
    72%, 100% { transform: rotate(0deg); }
  }
  @keyframes beamSweep {
    0%, 14% { opacity: 0.22; stroke-dashoffset: 210; }
    72%, 100% { opacity: 1; stroke-dashoffset: 0; }
  }
  .cav-arm-anim {
    transform-origin: 248px 258px;
    animation: cavTwist 4.2s cubic-bezier(0.22, 0.8, 0.25, 1) 1 forwards;
  }
  .cav-ray-anim {
    stroke-dasharray: 210;
    stroke-dashoffset: 0;
    animation: beamSweep 4.2s cubic-bezier(0.22, 0.8, 0.25, 1) 1 forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .cav-arm-anim, .cav-ray-anim {
      animation: none !important;
      transform: none !important;
      opacity: 1 !important;
      stroke-dashoffset: 0 !important;
    }
  }
    """

    cx, cy = 248.0, 258.0  # center of torsion wire (top-down view)
    arm_r = 108.0
    # Final equilibrium angle: +11 deg clockwise from horizontal (exaggerated for visual clarity; real 0.16° / 0.03°)
    ang_eq = math.radians(11.0)
    x1_eq = cx - arm_r * math.cos(ang_eq)
    y1_eq = cy - arm_r * math.sin(ang_eq)
    x2_eq = cx + arm_r * math.cos(ang_eq)
    y2_eq = cy + arm_r * math.sin(ang_eq)

    # Initial neutral reference angle (-7 deg relative -> 4 deg)
    ang_0 = math.radians(2.0)
    x1_0 = cx - arm_r * math.cos(ang_0)
    y1_0 = cy - arm_r * math.sin(ang_0)
    x2_0 = cx + arm_r * math.cos(ang_0)
    y2_0 = cy + arm_r * math.sin(ang_0)

    # Big lead spheres W1 (upper-left of right end? Wait: clockwise twist means left end goes UP-right, right end goes DOWN-left!
    # Wait: in SVG y grows DOWNWARD! Rotating by +11 deg clockwise moves right end (cx+R, cy) to (cx+R cos11, cy+R sin11) [DOWN],
    # and left end (cx-R, cy) to (cx-R cos11, cy-R sin11) [UP]!
    # So to attract small balls clockwise, Big Ball W_left sits ABOVE left small ball, and Big Ball W_right sits BELOW right small ball!
    w1_x, w1_y = x1_eq + 6, y1_eq - 36
    w2_x, w2_y = x2_eq - 6, y2_eq + 36

    parts = [
        *header(
            "把地球搬进花园木屋：1798 年卡文迪许扭秤如何捕捉“一粒细沙”的引力？",
            "0.0177 毫克重（1.74×10⁻⁷ N）的引力连呼吸气流都扛不住——唯有双层密封 + 扭丝悬臂 + 墙外望远镜／光杠杆放大",
        ),
        # Outer Sealed Shed Card (left 22..474)
        card(22, 76, 452, 344, fill="#f8fafc", stroke="#64748b"),
        _txt(40, 98, "双层密封花园木屋（隔绝人体体温对流与微风）", size=12, weight="700", fill=SLATE),
        # Inner Mahogany Box
        card(48, 110, 368, 292, fill="#fffbeb", stroke="#d97706"),
        _txt(64, 130, "桃花心木防风内箱（俯视示意，偏转角已放大）", size=11, weight="700", fill=AMBER),

        # Pulley dashed circle for big balls
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="118" fill="none" stroke="#cbd5e1" stroke-width="1.3" stroke-dasharray="5 4"/>',

        # Initial reference rod (dashed static guide so static readers see start -> end!)
        _line(x1_0, y1_0, x2_0, y2_0, stroke="#94a3b8", sw=1.8, dash="5 4"),
        f'<circle cx="{x1_0:.1f}" cy="{y1_0:.1f}" r="8" fill="none" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="3 2"/>',
        f'<circle cx="{x2_0:.1f}" cy="{y2_0:.1f}" r="8" fill="none" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="3 2"/>',
        _txt(x1_0 - 8, y1_0 + 22, "初态平衡位", size=9.8, fill=SLATE, anchor="middle"),

        # Two massive 158 kg lead spheres W1, W2
        f'<circle cx="{w1_x:.1f}" cy="{w1_y:.1f}" r="24" fill="#334155" stroke="#0f172a" stroke-width="2"/>',
        _txt(w1_x, w1_y + 4, "158 kg", size=10, weight="700", fill="#ffffff", anchor="middle"),
        _txt(w1_x - 30, w1_y - 16, "大铅球 W₁", size=10.5, weight="700", fill=INK, anchor="end"),

        f'<circle cx="{w2_x:.1f}" cy="{w2_y:.1f}" r="24" fill="#334155" stroke="#0f172a" stroke-width="2"/>',
        _txt(w2_x, w2_y + 4, "158 kg", size=10, weight="700", fill="#ffffff", anchor="middle"),
        _txt(w2_x - 32, w2_y + 22, "大铅球 W₂", size=10.5, weight="700", fill=INK, anchor="end"),

        # Animated torsion arm group settling at equilibrium
        '<g class="cav-arm-anim">',
        _line(x1_eq, y1_eq, x2_eq, y2_eq, stroke=BLUE, sw=4.0),
        f'<circle cx="{x1_eq:.1f}" cy="{y1_eq:.1f}" r="9.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.5"/>',
        f'<circle cx="{x2_eq:.1f}" cy="{y2_eq:.1f}" r="9.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.5"/>',
        # Tiny mirror at center torsion wire
        f'<rect x="{cx - 4:.1f}" y="{cy - 11:.1f}" width="8" height="22" rx="2" fill="#38bdf8" stroke="#0369a1" stroke-width="1.5"/>',
        '</g>',

        # Force arrows between small balls and big balls (at equilibrium)
        _line(x1_eq + 2, y1_eq - 9, w1_x - 2, w1_y + 23, stroke=RED, sw=1.8, marker="arr-red"),
        _line(x2_eq - 2, y2_eq + 9, w2_x + 2, w2_y - 23, stroke=RED, sw=1.8, marker="arr-red"),
        _txt(x1_eq - 36, y1_eq - 12, "小铅球 0.73 kg", size=10.2, weight="700", fill=BLUE, anchor="end"),
        _txt(cx, cy + 28, "镀银铜扭丝 + 中心反射镜", size=10.2, weight="700", fill=BLUE, anchor="middle"),
        _txt(cx, cy + 44, "真实偏角仅 0.03°～0.16°", size=10, fill=RED, weight="700", anchor="middle"),

        # Optical / Telescope readout crossing right shed wall (x=474) to scale at x=496
        '<rect x="468" y="218" width="12" height="80" rx="3" fill="#e2e8f0" stroke="#475569" stroke-width="1.5"/>',
        _txt(458, 212, "木屋观测窗", size=9.8, fill=SLATE, anchor="end"),
        # Incident + reflected optical lever beam / telescope sightline
        _line(492, 232, cx + 4, cy - 2, stroke=ORANGE, sw=1.5, dash="4 3"),
        _line(cx + 4, cy + 2, 492, 286, stroke=RED, sw=2.2, marker="arr-red", cls="cav-ray-anim"),

        # Right side 3-step explanation cards (x=492..738)
        card(492, 76, 246, 106, fill=BLUE_SOFT, stroke="#93c5fd"),
        step_badge(510, 96, 1, BLUE, BLUE_SOFT),
        _txt(530, 101, "门外拉滑轮防气流", size=12.2, weight="700", fill=BLUE),
        _txt(508, 124, "引力仅 1.74×10⁻⁷ N（相当于", size=10.6, fill=INK),
        _txt(508, 143, "0.0177 毫克细沙重，小球自重", size=10.6, weight="700", fill=RED),
        _txt(508, 162, "的五千万分之一），人绝不进屋！", size=10.6, fill=INK),

        card(492, 194, 246, 108, fill=ORANGE_SOFT, stroke="#fdba74"),
        step_badge(510, 214, 2, ORANGE, ORANGE_SOFT),
        _txt(530, 219, "墙外望远镜／光杠杆放大", size=12.2, weight="700", fill=ORANGE),
        _txt(508, 242, "原版用墙孔望远镜读游标尺（准", size=10.6, fill=INK),
        _txt(508, 261, "至 0.25 mm）；现代改进加中心", size=10.6, fill=INK),
        _txt(508, 280, "小镜反射光束，转 θ 光斑偏 2θ！", size=10.6, weight="700", fill=ORANGE),

        card(492, 314, 246, 106, fill=GREEN_SOFT, stroke="#86efac"),
        step_badge(510, 334, 3, GREEN, GREEN_SOFT),
        _txt(530, 339, "测扭摆周期消去悬丝刚度", size=12.2, weight="700", fill=GREEN),
        _txt(508, 362, "扭丝多硬怎么测？直接秒表测横", size=10.6, fill=INK),
        _txt(508, 381, "杆自由扭摆周期 T（约 7～15 分", size=10.6, fill=INK),
        _txt(508, 400, "钟），一举算出 ρ⊕ = 5.448 g/cm³！", size=10.6, weight="700", fill=GREEN),

        # Bottom summary formula strip
        card(22, 432, 716, 86, fill=SLATE_SOFT, stroke="#cbd5e1"),
        _txt(380, 456, "卡文迪许核心联立：力矩平衡 κ·θ = 2·F·(L/2)   且   自由扭摆周期 T = 2π√(I / κ)", size=12, weight="700", fill=INK, anchor="middle"),
        _txt(380, 480, "消去未知刚度 κ ⇒ G = 2π²·L·r²·θ / (M·T²)  ⇒  与现代真值 5.514 g/cm³ 仅差 1.2%，尘封百年无人超越！", size=11.3, weight="700", fill=TEAL, anchor="middle"),
        _txt(380, 502, "（动画单次播放扭杆趋向引力平衡与光束偏转；开启系统“减少动态效果”或静态查看时保留完整初末态对照）", size=10.2, fill=MUTED, anchor="middle"),
    ]

    return figure(
        H,
        "1798 卡文迪许密封木屋扭秤实验与光杠杆放大动画图",
        "俯视展示双层密封花园木屋内 158 kg 大铅球吸引 0.73 kg 小铅球产生微牛级引力扭矩、墙外望远镜与光杠杆放大读数，以及通过扭摆周期消去悬丝刚度的完整原理。偏转角为示意放大。",
        parts,
        extra_css=anim_css,
        extra_defs=_markers(),
        width=W,
    )


# ---------------------------------------------------------------------------
# 4. Four Ingenious Modern & Classical Gravitational Setups (760 x 520)
# ---------------------------------------------------------------------------
def build_four_clever_methods() -> str:
    W, H = 760, 520
    # Verify Philipp von Jolly 1881 5,775 kg lead sphere pull on 5 kg mass at ~0.568 m center distance
    G = 6.67430e-11
    M_lead = 5775.0
    m_flask = 5.0
    r_jolly = 0.568  # radius of 5775 kg lead sphere (~0.495 m) + gap (~0.073 m)
    dm_mg = (G * M_lead * m_flask / (r_jolly ** 2)) / 9.80665 * 1e6
    assert 0.50 < dm_mg < 0.68, f"Unexpected Jolly extra weight: {dm_mg} mg"

    parts = [
        *header(
            "脑洞大开的四种引力称地术：高塔天平、激光迪斯科球、冷原子与山洞双扭秤",
            "从硬刚毫克增重的 25 米楼梯井，到十亿分之二精度的太空反射球，再到没有一根悬丝的量子物质波",
        ),
        # Card 1 (Top-Left): Jolly 1881 25m Tower Balance
        card(22, 78, 352, 202),
        step_badge(40, 98, 1, AMBER, AMBER_SOFT),
        _txt(62, 103, "1881 慕尼黑 25 米高塔双盘天平（冯·约利）", size=12.6, weight="700", fill=AMBER),
        # Mini illustration of tower balance (x=38..148, y=118..264)
        '<rect x="44" y="118" width="94" height="146" rx="8" fill="#fffbeb" stroke="#fcd34d"/>',
        _line(64, 132, 118, 132, stroke=INK, sw=2.2),
        '<polygon points="91,124 86,132 96,132" fill="#d97706"/>',
        # Upper pans
        _line(66, 132, 66, 152, stroke=SLATE, sw=1.3),
        _line(116, 132, 116, 152, stroke=SLATE, sw=1.3),
        '<rect x="56" y="152" width="20" height="5" fill="#d97706"/>',
        '<rect x="106" y="152" width="20" height="5" fill="#d97706"/>',
        # 21m wire down to lower pans
        _line(66, 157, 66, 214, stroke=SLATE, sw=1.2, dash="3 2"),
        _line(116, 157, 116, 214, stroke=SLATE, sw=1.2, dash="3 2"),
        '<rect x="56" y="214" width="20" height="5" fill="#0284c7"/>',
        '<circle cx="66" cy="208" r="6" fill="#0284c7"/>',
        # 5775 kg lead sphere underneath left lower pan
        '<circle cx="66" cy="242" r="18" fill="#334155" stroke="#0f172a" stroke-width="1.5"/>',
        _txt(66, 246, "5.8吨", size=9.2, weight="700", fill="#ffffff", anchor="middle"),
        _txt(152, 134, "• 21 米长悬丝上下挂两副秤盘：", size=10.8, fill=INK),
        _txt(152, 154, "  5 kg 球移到下盘先增重 ~31 mg", size=10.8, fill=INK),
        _txt(152, 176, "• 再往底盘正下方推入一颗重达", size=10.8, fill=INK),
        _txt(152, 195, "  5775 kg 的一米大铅球！", size=10.8, weight="700", fill=INK),
        _txt(152, 217, "• 天平直接“称”出大铅球额外", size=10.8, fill=INK),
        _txt(152, 236, "  往下拽了 0.589 毫克！", size=11, weight="700", fill=RED),
        _txt(152, 259, "⇒ 算出 ρ⊕ ≈ 5.69 g/cm³", size=11, weight="700", fill=AMBER),

        # Card 2 (Top-Right): LAGEOS + GRACE-FO Satellites
        card(386, 78, 352, 202),
        step_badge(404, 98, 2, BLUE, BLUE_SOFT),
        _txt(426, 103, "太空“激光迪斯科球”与双星追逐（LAGEOS & GRACE）", size=12.3, weight="700", fill=BLUE),
        '<rect x="402" y="118" width="96" height="146" rx="8" fill="#eff6ff" stroke="#93c5fd"/>',
        # LAGEOS sphere with grid of reflectors
        '<circle cx="450" cy="162" r="24" fill="#cbd5e1" stroke="#0284c7" stroke-width="2"/>',
        '<circle cx="442" cy="154" r="3" fill="#ffffff"/><circle cx="452" cy="152" r="3" fill="#ffffff"/><circle cx="460" cy="158" r="3" fill="#ffffff"/>',
        '<circle cx="440" cy="166" r="3" fill="#ffffff"/><circle cx="450" cy="164" r="3" fill="#ffffff"/><circle cx="458" cy="170" r="3" fill="#ffffff"/>',
        _line(416, 246, 444, 184, stroke=RED, sw=1.8, marker="arr-red"),
        _txt(450, 204, "426 块角反射器", size=9.6, weight="700", fill=BLUE, anchor="middle"),
        # Twin GRACE satellites at bottom of mini box
        '<rect x="414" y="224" width="18" height="10" rx="2" fill="#0f766e"/>',
        '<rect x="468" y="224" width="18" height="10" rx="2" fill="#0f766e"/>',
        _line(434, 229, 466, 229, stroke=TEAL, sw=1.6, dash="3 2"),
        _txt(450, 254, "双星距 220 km", size=9.6, fill=TEAL, anchor="middle"),
        _txt(510, 134, "• LAGEOS（60 cm 实心黄铜球，", size=10.8, fill=INK),
        _txt(510, 154, "  重 407 kg）：地面毫米级激光", size=10.8, fill=INK),
        _txt(510, 174, "  测距把 G·M⊕ 锁准到 2×10⁻⁹！", size=10.8, weight="700", fill=BLUE),
        _txt(510, 198, "• GRACE-FO 双子星：飞过冰川", size=10.8, fill=INK),
        _txt(510, 217, "  或地下水富集区时前星先加速，", size=10.8, fill=INK),
        _txt(510, 236, "  微米级测距按月给冰盖和含水", size=10.8, fill=INK),
        _txt(510, 256, "  层“称体重”！", size=11, weight="700", fill=TEAL),

        # Card 3 (Bottom-Left): Cold-Atom Quantum Interferometer (Rosi 2014)
        card(22, 294, 352, 202),
        step_badge(40, 314, 3, PURPLE, PURPLE_SOFT),
        _txt(62, 319, "2014 超冷铷原子量子喷泉（Rosi 等 Nature）", size=12.5, weight="700", fill=PURPLE),
        '<rect x="44" y="334" width="94" height="146" rx="8" fill="#faf5ff" stroke="#d8b4fe"/>',
        # Tungsten cylinders flanking atom wave packet
        '<rect x="52" y="366" width="18" height="68" rx="3" fill="#475569"/>',
        '<rect x="112" y="366" width="18" height="68" rx="3" fill="#475569"/>',
        _txt(91, 352, "516 kg 钨柱阵", size=9.5, weight="700", fill=SLATE, anchor="middle"),
        # Matter wave interference loops in center x=91
        '<path d="M 91,446 Q 76,406 91,368 Q 106,406 91,446" fill="none" stroke="#7c3aed" stroke-width="2"/>',
        '<circle cx="91" cy="406" r="5" fill="#7c3aed"/>',
        _txt(91, 466, "⁸⁷Rb 物质波", size=9.5, weight="700", fill=PURPLE, anchor="middle"),
        _txt(152, 350, "• 彻底抛弃宏观悬丝（零机械老化", size=10.8, weight="700", fill=PURPLE),
        _txt(152, 369, "  与金属滞弹性误差）！", size=10.8, fill=INK),
        _txt(152, 391, "• 激光冷却铷-87 原子团至接近", size=10.8, fill=INK),
        _txt(152, 410, "  绝对零度，向上喷射自由下落；", size=10.8, fill=INK),
        _txt(152, 432, "• 两侧 516 kg 高密度钨柱改写", size=10.8, fill=INK),
        _txt(152, 451, "  原子德布罗意波干涉相位，直", size=10.8, fill=INK),
        _txt(152, 471, "  接读出 G（精度 150 ppm）！", size=11, weight="700", fill=PURPLE),

        # Card 4 (Bottom-Right): HUST 2018 Cave Dual Torsion Pendulum (Luo Jun team)
        card(386, 294, 352, 202),
        step_badge(404, 314, 4, GREEN, GREEN_SOFT),
        _txt(426, 319, "2018 武汉山洞双法扭秤破纪录（罗俊团队 Nature）", size=12.2, weight="700", fill=GREEN),
        '<rect x="402" y="334" width="96" height="146" rx="8" fill="#f0fdf4" stroke="#86efac"/>',
        # Mountain cave arch + quartz plate torsion pendulum
        '<path d="M 410,466 L 410,374 Q 450,342 490,374 L 490,466" fill="#dcfce7" stroke="#15803d" stroke-width="1.8"/>',
        _line(450, 360, 450, 412, stroke=INK, sw=1.5),
        '<rect x="432" y="412" width="36" height="10" rx="2" fill="#15803d"/>',
        '<circle cx="422" cy="417" r="8" fill="#334155"/>',
        '<circle cx="478" cy="417" r="8" fill="#334155"/>',
        _txt(450, 450, "恒温山洞实验室", size=9.5, weight="700", fill=GREEN, anchor="middle"),
        _txt(510, 350, "• 躲进武汉喻家山防震恒温山洞，", size=10.8, fill=INK),
        _txt(510, 369, "  镀膜石英块镀金悬丝抑制静电力；", size=10.8, fill=INK),
        _txt(510, 391, "• 同时采用两套独立物理原理：", size=10.8, weight="700", fill=INK),
        _txt(510, 411, "  ① 扭摆周期法：11.64 ppm", size=10.8, weight="700", fill=GREEN),
        _txt(510, 430, "  ② 角加速度反馈法：11.61 ppm", size=10.8, weight="700", fill=GREEN),
        _txt(510, 453, "⇒ 创下迄今人类测 G 最高精度", size=11, weight="700", fill=RED),
        _txt(510, 472, "  世界纪录，把地球称得最准！", size=10.8, fill=INK),
    ]

    return figure(
        H,
        "四种经典与现代引力称地巧思对比图",
        "对比 1881 慕尼黑 25 米高塔双盘天平与 5.8 吨大铅球、LAGEOS 激光测距卫星与 GRACE-FO 双星重力追逐、2014 超冷铷原子物质波干涉仪，以及 2018 武汉山洞双法扭秤破纪录实验。",
        parts,
        extra_defs=_markers(),
        width=W,
    )


# ---------------------------------------------------------------------------
# 5. Neutrino CT Scan (Without Gravity!) & Cosmic Mass-Loss Ledger (760 x 515)
# ---------------------------------------------------------------------------
def build_neutrino_and_mass_ledger() -> str:
    W, H = 760, 515
    # Verify Donini, Palomares-Ruiz, & Salvado (Nature Physics 2018 / arXiv:1803.05901) & Rojas 2021
    M_nu = 6.0e24
    M_grav = 5.9722e24
    assert abs(M_nu - M_grav) / M_grav < 0.01  # central value within 0.5% (68% CI +1.6/-1.3)
    in_dust_tons = 5200
    out_h_tons = 95000
    out_he_tons = 1600
    net_loss_tons = out_h_tons + out_he_tons - in_dust_tons
    assert 85000 < net_loss_tons < 95000

    ecx, ecy = 200.0, 258.0
    r_outer = 96.0
    r_core = 96.0 * (3485.0 / 6371.0)  # true scale core radius = 52.5 px!

    parts = [
        *header(
            "彻底不用引力的终极脑洞：南极幽灵粒子“弱力 CT”称地球，外加地球年度减肥账单",
            "数一数穿透地心的 TeV 级中微子被拦下几成就能算出地球质量；而地球每年正悄悄向太空净瘦身约 9 万吨",
        ),
        # Left Panel: IceCube Neutrino Tomography (2018 Nature Physics)
        card(20, 76, 408, 420),
        step_badge(38, 96, 1, TEAL, TEAL_SOFT),
        _txt(60, 101, "2018 零引力称重：南极 IceCube 中微子透视地球", size=12.8, weight="700", fill=TEAL),
        pill(38, 114, "靠弱相互作用吸收率反推核幔密度（Donini 等 2018）", TEAL, TEAL_SOFT, w=324),

        # True-proportion Earth cross section (crust/mantle + core r_core = 52.5 px)
        f'<circle cx="{ecx:.1f}" cy="{ecy:.1f}" r="{r_outer:.1f}" fill="#dbeafe" stroke="#0284c7" stroke-width="2"/>',
        f'<circle cx="{ecx:.1f}" cy="{ecy:.1f}" r="{r_core:.1f}" fill="#fde68a" stroke="#d97706" stroke-width="2"/>',
        f'<circle cx="{ecx:.1f}" cy="{ecy:.1f}" r="18.4" fill="#fca5a5" stroke="#dc2626" stroke-width="1.5"/>',
        _txt(ecx, ecy + 4, "致密铁核", size=10, weight="700", fill=RED, anchor="middle"),
        _txt(ecx, ecy - 68, "硅酸盐地幔", size=10, weight="700", fill=BLUE, anchor="middle"),

        # North atmosphere cosmic-ray shower at top, IceCube at South Pole bottom (ecx, ecy + r_outer)
        _txt(116, 148, "北半球大气层宇宙线簇射 (>5 TeV 中微子)", size=10.2, weight="700", fill=PURPLE),
        # Ray A: Straight through dense core -> ~50% absorbed!
        _line(192, 154, 192, ecy + r_outer - 4, stroke=RED, sw=2.3, dash="6 3", marker="arr-red"),
        # Ray B: Grazing chord through mantle only -> ~90%+ survive!
        _line(118, 186, ecx - 4, ecy + r_outer - 4, stroke=TEAL, sw=2.2, marker="arr-teal"),
        # Ray C: Outer chord on right
        _line(282, 186, ecx + 4, ecy + r_outer - 4, stroke=TEAL, sw=2.2, marker="arr-teal"),

        # IceCube 1 km^3 detector block at South Pole
        f'<rect x="{ecx - 26:.1f}" y="{ecy + r_outer - 2:.1f}" width="52" height="22" rx="4" fill="#0f172a"/>',
        _txt(ecx, ecy + r_outer + 13, "IceCube", size=9.5, weight="700", fill="#38bdf8", anchor="middle"),
        _txt(ecx + 34, ecy + r_outer + 13, "南极冰下 1 km³ 探测器", size=10.2, weight="700", fill=INK),

        # Callouts on rays
        _txt(312, 232, "擦边穿地幔：", size=10.5, weight="700", fill=TEAL),
        _txt(312, 249, "密度低，近九成穿过", size=10.2, fill=INK),
        _txt(302, 286, "直穿高密地核：", size=10.5, weight="700", fill=RED),
        _txt(302, 303, ">5 TeV 约一半被吸收！", size=10.2, weight="700", fill=RED),

        # Bottom result card inside left panel
        card(36, 386, 376, 96, fill=TEAL_SOFT, stroke="#99f6e4"),
        _txt(50, 408, "• 原理：高能中微子撞击质子／中子的弱力截面已知", size=10.8, fill=INK),
        _txt(50, 429, "• 纯弱力测得地球质量：M⊕(ν) = (6.0 +1.6 / −1.3) × 10²⁴ kg", size=11, weight="700", fill=TEAL),
        _txt(50, 450, "• 引力测得标准质量：  M⊕(引力) = 5.9722 × 10²⁴ kg", size=11, weight="700", fill=BLUE),
        _txt(50, 471, "⇒ 人类首次完全不靠万有引力，独立验证地球体重与重核！", size=10.6, weight="700", fill=INK),

        # Right Panel: Earth's Annual Cosmic Weight-Loss Ledger
        card(444, 76, 296, 420),
        step_badge(462, 96, 2, ORANGE, ORANGE_SOFT),
        _txt(484, 101, "彩蛋：地球每年变胖还是变瘦？", size=12.8, weight="700", fill=ORANGE),
        pill(462, 114, "太空尘埃进账 vs 大气逃逸出账", ORANGE, ORANGE_SOFT, w=236),

        # Income box
        card(460, 148, 264, 96, fill=GREEN_SOFT, stroke="#86efac"),
        _txt(476, 170, "【年度增重】彗星与小行星微陨石", size=11.5, weight="700", fill=GREEN),
        _txt(476, 192, "• 南极 Concordia 站 20 年雪样实测", size=10.5, fill=INK),
        _txt(476, 211, "  （Rojas 等 2021）：落达地表约", size=10.5, fill=INK),
        _txt(476, 231, "  +5,200 吨 / 年（大气顶层约 1.5～4 万吨）", size=10.8, weight="700", fill=GREEN),

        # Outflow box
        card(460, 256, 264, 108, fill=RED_SOFT, stroke="#fca5a5"),
        _txt(476, 278, "【年度减重】高层大气轻气体逃逸", size=11.5, weight="700", fill=RED),
        _txt(476, 300, "• 太阳极紫外加热顶层大气：", size=10.5, fill=INK),
        _txt(476, 320, "  氢气逃逸：约 −95,000 吨 / 年（每秒 3 kg）", size=10.6, weight="700", fill=RED),
        _txt(476, 340, "  氦气逃逸：约 −1,600 吨 / 年", size=10.6, fill=INK),
        _txt(476, 356, "  （核裂变／辐射质能亏损微乎其微）", size=9.8, fill=MUTED),

        # Net verdict box
        card(460, 376, 264, 106, fill=AMBER_SOFT, stroke="#fcd34d"),
        _txt(592, 400, "年度净账单：每年净“瘦身”约 5～9 万吨！", size=11.3, weight="700", fill=RED, anchor="middle"),
        _txt(476, 424, "• 听起来很多？除以 5.9722×10²⁴ kg：", size=10.5, fill=INK),
        _txt(476, 444, "  每年仅流失约 1.5 × 10⁻¹⁷（千万亿分", size=10.5, fill=INK),
        _txt(476, 464, "  之一点五），一亿年也瘦不到十亿分之一！", size=10.5, weight="700", fill=AMBER),
    ]

    return figure(
        H,
        "南极 IceCube 中微子零引力透视称重与地球年度质量收支账本图",
        "左图按真实核幔半径比例（3485 km / 6371 km）展示高能大气中微子穿过地幔与地核的弱力吸收差异；右图对比每年约 5200 吨微陨石落地增重与约 9.66 万吨氢氦逃逸减重。",
        parts,
        extra_defs=_markers(),
        width=W,
    )


@register(
    TOPIC,
    "地球重量引力测试与花式称地方法（GM锁、孤峰深井、卡文迪许扭秤动画、冷原子、南极中微子）",
    "physics",
)
def build_all() -> list[str]:
    write_svg(TOPIC, "gm-lock-and-precision-gap.svg", build_gm_lock_and_precision())
    write_svg(TOPIC, "schiehallion-mountain-and-airy-mine.svg", build_mountain_and_mine())
    write_svg(TOPIC, "cavendish-torsion-balance-shed.svg", build_cavendish_torsion_balance())
    write_svg(TOPIC, "four-clever-ways-tower-laser-atom.svg", build_four_clever_methods())
    write_svg(TOPIC, "neutrino-ct-scan-and-mass-diet.svg", build_neutrino_and_mass_ledger())
    return [
        "gm-lock-and-precision-gap.svg",
        "schiehallion-mountain-and-airy-mine.svg",
        "cavendish-torsion-balance-shed.svg",
        "four-clever-ways-tower-laser-atom.svg",
        "neutrino-ct-scan-and-mass-diet.svg",
    ]
