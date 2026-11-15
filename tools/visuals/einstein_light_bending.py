"""Original 760px Chinese SVG diagrams for the Einstein Light Deflection & Verification post."""

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

SUBDIR = "einstein-light-bending"

# IAU / CODATA physical constants
G_SI = 6.67430e-11          # m^3 kg^-1 s^-2
C_SI = 299_792_458.0        # m / s
GM_SUN = 1.3271244e20       # m^3 / s^2 (IAU nominal solar mass parameter)
R_SUN = 6.957e8             # m (IAU nominal solar radius)
AU_M = 1.495978707e11       # m
GM_JUP = 1.2668653e17       # m^3 / s^2
R_JUP = 6.9911e7            # m (mean volumetric / equatorial ~7.1492e7 m)
RAD_TO_ARCSEC = 180.0 * 3600.0 / math.pi


def _verify_light_bending_math():
    """Assert every physical formula, angle, linear plate shift, and chart coordinate."""
    # 1. Solar limb deflection: GR (4GM/c^2 R) vs Newtonian/1911 (2GM/c^2 R)
    alpha_gr_rad = 4.0 * GM_SUN / (C_SI ** 2 * R_SUN)
    alpha_gr_arcsec = alpha_gr_rad * RAD_TO_ARCSEC
    alpha_1911_arcsec = 0.5 * alpha_gr_arcsec
    assert 1.748 < alpha_gr_arcsec < 1.753, f"Unexpected GR limb deflection: {alpha_gr_arcsec}"
    assert 0.874 < alpha_1911_arcsec < 0.877
    assert abs(alpha_gr_arcsec / alpha_1911_arcsec - 2.0) < 1e-12

    # 2. Elevator drop across 3 m room in 1 g
    dt_room = 3.0 / C_SI
    dy_room = 0.5 * 9.8 * (dt_room ** 2)
    assert 4.8e-16 < dy_room < 5.0e-16  # ~4.9e-16 m (~half a femtometer)

    # 3. Visual scale of 1.75 arcsec: 25 mm coin (1 RMB coin) distance
    d_coin_m = 0.025 / alpha_gr_rad
    assert 2930 < d_coin_m < 2960  # ~2.95 km

    # 4. Linear shift on Sobral 4-inch / 19-foot (5.7912 m) photographic plate
    f_cortie_m = 19.0 * 0.3048  # 5.7912 m
    dx_limb_mm = f_cortie_m * alpha_gr_rad * 1000.0        # ~0.0491 mm at limb
    dx_2rsun_mm = 0.5 * dx_limb_mm                         # ~0.0246 mm at r = 2 R_sun
    assert 0.048 < dx_limb_mm < 0.051
    assert 0.024 < dx_2rsun_mm < 0.026

    # 5. All-sky solar deflection at 90 deg elongation (Gaia): 2 GM_sun / (c^2 * 1 AU)
    alpha_90_mas = (2.0 * GM_SUN / (C_SI ** 2 * AU_M)) * RAD_TO_ARCSEC * 1000.0
    assert 4.05 < alpha_90_mas < 4.10  # ~4.07 mas

    # 6. Jupiter limb monopole deflection (Gaia 2022 release: 16.2 mas at equatorial limb)
    r_jup_eq = 7.1492e7
    alpha_jup_mas = (4.0 * GM_JUP / (C_SI ** 2 * r_jup_eq)) * RAD_TO_ARCSEC * 1000.0
    assert 16.1 < alpha_jup_mas < 16.4


def _defs_arrows():
    return """
    <marker id="arr-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#1d6fa5"/>
    </marker>
    <marker id="arr-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#c25014"/>
    </marker>
    <marker id="arr-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#18794e"/>
    </marker>
    <marker id="arr-p" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#6d28d9"/>
    </marker>
    <marker id="arr-s" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#475569"/>
    </marker>
    """


def _box(x, y, w, h, fill=SLATE_SOFT, stroke=BORDER, rx=8):
    return card(x, y, w, h, rx=rx, fill=fill, stroke=stroke, sw=1)


def _build_elevator_equivalence():
    """Fig 1: Einstein's 1907/1911 accelerating-elevator thought experiment & Equivalence Principle."""
    H = 510
    el = [
        *header(
            "没有质量的光，凭什么会被引力掰弯？——爱因斯坦“加速电梯”思想实验",
            "先看左舱火箭向上加速 → 再用等效原理平移到右舱引力场：只要等效原理成立，光线在引力场中必然向下弯曲",
        )
    ]

    # Left card: Deep-space rocket elevator accelerating upward at a = g
    el.append(card(22, 68, 346, 358))
    el.append(step_badge(42, 92, 1, BLUE, BLUE_SOFT))
    el.append(txt(62, 97, "深空无引力场：火箭以加速度 a = g 向上猛推", size=12.8, color=INK, weight="700"))
    el.append(txt(42, 117, "舱外看光走水平直线；但光飞越舱宽 L 期间地板迎面往上追", size=10.8, color=MUTED))

    # Elevator cabin box
    cx, cy, cw, ch = 76, 152, 236, 174
    el.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="8" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>')
    # Rocket nozzle flames at bottom
    el.append(f'<polygon points="{cx+98},{cy+ch} {cx+138},{cy+ch} {cx+118},{cy+ch+26}" fill="#fb923c" opacity="0.85"/>')
    el.append(f'<polygon points="{cx+108},{cy+ch} {cx+128},{cy+ch} {cx+118},{cy+ch+16}" fill="#fde047"/>')
    # Upward acceleration arrow on left
    el.append(f'<line x1="48" y1="285" x2="48" y2="180" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#arr-b)"/>')
    el.append(txt(48, 168, "a = g", size=11.5, color=BLUE, anchor="middle", weight="700"))

    # Window on left wall at y=194
    wy = 194
    el.append(f'<rect x="{cx-4}" y="{wy-8}" width="8" height="16" fill="#ffffff" stroke="{BLUE}" stroke-width="1.5"/>')
    # External horizontal dashed straight line (inertial path)
    el.append(f'<line x1="{cx+4}" y1="{wy}" x2="{cx+cw-6}" y2="{wy}" stroke="{SLATE}" stroke-width="1.5" stroke-dasharray="5,4"/>')
    el.append(txt(cx + 118, wy - 10, "舱外惯性系看：光沿水平虚线直飞", size=10.5, color=SLATE, anchor="middle"))

    # Parabolic apparent path inside accelerating cabin (schematic exaggeration noted)
    end_y = wy + 68
    el.append(f'<path d="M {cx+4},{wy} Q {cx+130},{wy+4} {cx+cw-6},{end_y}" fill="none" stroke="{ORANGE}" stroke-width="3" marker-end="url(#arr-o)"/>')
    el.append(f'<circle cx="{cx+cw-4}" cy="{end_y}" r="5" fill="{ORANGE}"/>')
    el.append(txt(cx + 114, wy + 52, "舱内乘客看：光画出向下抛物线！", size=11.2, color=ORANGE, anchor="middle", weight="700", halo=True))

    # Delta y bracket on right wall
    el.append(f'<line x1="{cx+cw+12}" y1="{wy}" x2="{cx+cw+12}" y2="{end_y}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(f'<line x1="{cx+cw+7}" y1="{wy}" x2="{cx+cw+17}" y2="{wy}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(f'<line x1="{cx+cw+7}" y1="{end_y}" x2="{cx+cw+17}" y2="{end_y}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(txt(cx + cw + 20, (wy + end_y) / 2 + 4, "Δy", size=11.5, color=ORANGE, weight="700"))

    # Formula box inside left card bottom
    el.append(_box(40, 362, 310, 48, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(195, 382, "飞越舱宽耗时 Δt = L / c", size=11.2, color=INK, anchor="middle", weight="700"))
    el.append(txt(195, 401, "地板上追距离 Δy = ½ g (L / c)²（图中曲率已放大示意）", size=10.6, color=MUTED, anchor="middle"))

    # Center equivalence badge between cards
    el.append(_box(353, 224, 54, 42, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(380, 243, "等效", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(380, 259, "原理", size=11.5, color=PURPLE, anchor="middle", weight="700"))

    # Right card: Stationary cabin in gravitational field g (Sun / Earth)
    el.append(card(392, 68, 346, 358))
    el.append(step_badge(412, 92, 2, GREEN, GREEN_SOFT))
    el.append(txt(432, 97, "天体表面引力场 g：静置不动的封闭房间", size=12.8, color=INK, weight="700"))
    el.append(txt(412, 117, "局域内无法区分“向上加速”与“向下引力”→ 光必同样下弯", size=10.8, color=MUTED))

    rx = 446
    # Planet/Sun surface arc at bottom of cabin
    el.append(f'<path d="M {rx-24},{cy+ch+22} Q {rx+118},{cy+ch-10} {rx+cw+24},{cy+ch+22}" fill="#fde68a" stroke="#d97706" stroke-width="2"/>')
    el.append(txt(rx + 118, cy + ch + 20, "大质量天体表面（太阳 / 地球引力场 g）", size=10.6, color="#92400e", anchor="middle", weight="700"))

    el.append(f'<rect x="{rx}" y="{cy}" width="{cw}" height="{ch}" rx="8" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>')
    el.append(f'<rect x="{rx-4}" y="{wy-8}" width="8" height="16" fill="#ffffff" stroke="{GREEN}" stroke-width="1.5"/>')
    el.append(f'<line x1="{rx+4}" y1="{wy}" x2="{rx+cw-6}" y2="{wy}" stroke="{SLATE}" stroke-width="1.5" stroke-dasharray="5,4"/>')
    el.append(txt(rx + 118, wy - 10, "若引力不影响光：本该打在同高度靶心", size=10.5, color=SLATE, anchor="middle"))

    el.append(f'<path d="M {rx+4},{wy} Q {rx+130},{wy+4} {rx+cw-6},{end_y}" fill="none" stroke="{ORANGE}" stroke-width="3" marker-end="url(#arr-o)"/>')
    el.append(f'<circle cx="{rx+cw-4}" cy="{end_y}" r="5" fill="{ORANGE}"/>')
    el.append(txt(rx + 114, wy + 52, "真实结果：引力场把光线往下拽弯 Δy！", size=11.2, color=ORANGE, anchor="middle", weight="700", halo=True))

    # Gravity downward arrow
    el.append(f'<line x1="{rx+cw+22}" y1="180" x2="{rx+cw+22}" y2="285" stroke="{GREEN}" stroke-width="2.4" marker-end="url(#arr-g)"/>')
    el.append(txt(rx + cw + 22, 168, "引力 g", size=11.2, color=GREEN, anchor="middle", weight="700"))

    el.append(_box(410, 362, 310, 48, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(565, 382, "无需光子有静止质量 m₀！", size=11.2, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(565, 401, "光线走的是弯曲时空里的“最直短程线”（测地线）", size=10.6, color=MUTED, anchor="middle"))

    # Bottom reality-check strip: why don't we see laser beams droop in a room?
    el.append(card(22, 438, 716, 56, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(40, 461, "为什么平时拿激光笔照墙看不出下垂？算笔账：房间宽 L = 3 m 时，光飞过去仅需 10⁻⁸ 秒，下坠量 Δy ≈ 4.9 × 10⁻¹⁶ 米", size=11.2, color=INK, weight="700"))
    el.append(txt(40, 482, "——这还不到一颗质子直径的二分之一！想肉眼测出弯曲，必须请出太阳系最重的“引力怪兽”：太阳（M☉ ≈ 2×10³⁰ kg）！", size=10.8, color=ORANGE))

    write_svg(
        SUBDIR,
        "elevator-thought-experiment-equivalence.svg",
        figure(
            H,
            "爱因斯坦加速电梯思想实验与等效原理推导光线弯曲示意图",
            "对比无引力深空向上加速火箭与天体引力场静置房间内的激光轨迹，展示等效原理如何预言光线弯曲及日常尺度下垂量级。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_1911_vs_1915_factor_of_two():
    """Fig 2: Why 1915 full GR doubled 1911 Equivalence-Principle deflection (0.875'' -> 1.750'') + 1914 Crimea twist."""
    H = 536
    el = [
        *header(
            "从 0.875″ 到 1.75″：为什么爱因斯坦 1915 年把自己的预言翻了一倍？",
            "1911 年只算了“引力让时间变慢”；1915 年补齐“空间本身也在弯曲”，两项各贡献一半偏折角（γ = 1）",
        )
    ]

    # Left card: 1801 Soldner / 1911 Einstein (Time dilation ONLY -> 0.875")
    el.append(card(22, 68, 346, 336))
    el.append(_box(38, 82, 314, 28, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(195, 101, "1911 布拉格版（及 1801 牛顿微粒版）：只算一半", size=11.8, color=SLATE, anchor="middle", weight="700"))

    # Sun + flat Euclidean grid + tilting wavefronts
    sx, sy = 195, 238
    # Flat regular grid
    for gx in range(65, 330, 26):
        el.append(f'<line x1="{gx}" y1="126" x2="{gx}" y2="292" stroke="#e2e8f0" stroke-width="1"/>')
    for gy in range(130, 295, 26):
        el.append(f'<line x1="58" y1="{gy}" x2="332" y2="{gy}" stroke="#e2e8f0" stroke-width="1"/>')

    el.append(f'<circle cx="{sx}" cy="{sy}" r="34" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>')
    el.append(txt(sx, sy + 4, "太阳 M☉", size=11.2, color="#78350f", anchor="middle", weight="700"))

    # Grazing light ray on top of Sun (slight bend)
    el.append(f'<line x1="54" y1="176" x2="334" y2="176" stroke="{HAIRLINE}" stroke-width="1.3" stroke-dasharray="4,4"/>')
    el.append(f'<path d="M 54,176 Q 195,176 334,194" fill="none" stroke="{BLUE}" stroke-width="2.8" marker-end="url(#arr-b)"/>')
    # Huygens wavefront ticks showing inner edge slower due to time dilation
    for wx, tilt in [(115, 2), (165, 5), (225, 9), (275, 12)]:
        wy_top = 160 + (wx - 54) * 0.03
        wy_bot = 192 + (wx - 54) * 0.05
        el.append(f'<line x1="{wx}" y1="{wy_top:.1f}" x2="{wx-tilt}" y2="{wy_bot:.1f}" stroke="{BLUE}" stroke-width="1.6"/>')

    el.append(txt(195, 145, "平直空间网格 ＋ 靠近太阳钟表走得慢（g₀₀）", size=11.0, color=BLUE, anchor="middle", weight="700", halo=True))
    el.append(txt(285, 214, "α₁₉₁₁ = 0.875″", size=11.8, color=BLUE, anchor="middle", weight="700", halo=True))

    el.append(_box(38, 304, 314, 86, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(195, 325, "机制：惠更斯波前内慢外快（等效折射率 n ≈ 1 + GM/c²r）", size=10.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(195, 346, "公式：α₁₉₁₁ = 2GM☉ / (c²R☉) ≈ 0.875 角秒", size=11.4, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(195, 368, "注：与 1801 年索尔德纳把光当牛顿重粒子的结果完全重合", size=10.5, color=MUTED, anchor="middle"))

    # Right card: 1915 Full General Relativity (Time dilation + Spatial curvature -> 1.750")
    el.append(card(392, 68, 346, 336))
    el.append(_box(408, 82, 314, 28, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(565, 101, "1915.11 完整广义相对论：时间＋空间双双弯曲", size=11.8, color=ORANGE, anchor="middle", weight="700"))

    rx = 565
    # Curved spatial grid dipping toward the Sun!
    for gx in range(435, 700, 26):
        dx = gx - rx
        el.append(f'<path d="M {gx},126 Q {gx - (0.18*dx):.1f},{sy} {gx},292" fill="none" stroke="#fed7aa" stroke-width="1.2"/>')
    for gy in range(130, 295, 26):
        dy = gy - sy
        dip = 18.0 * math.exp(-(dy / 55.0) ** 2) * (1 if dy < 0 else -0.6)
        el.append(f'<path d="M 428,{gy} Q {rx},{gy + dip:.1f} 702,{gy}" fill="none" stroke="#fed7aa" stroke-width="1.2"/>')

    el.append(f'<circle cx="{rx}" cy="{sy}" r="34" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>')
    el.append(txt(rx, sy + 4, "太阳 M☉", size=11.2, color="#78350f", anchor="middle", weight="700"))

    el.append(f'<line x1="424" y1="176" x2="704" y2="176" stroke="{HAIRLINE}" stroke-width="1.3" stroke-dasharray="4,4"/>')
    # Doubly bent ray!
    el.append(f'<path d="M 424,176 Q 565,178 704,212" fill="none" stroke="{ORANGE}" stroke-width="3.2" marker-end="url(#arr-o)"/>')
    el.append(txt(565, 145, "时间变慢（g₀₀）＋ 空间尺子拉伸弯曲（gᵣᵣ，γ = 1）", size=11.0, color=ORANGE, anchor="middle", weight="700", halo=True))
    el.append(txt(664, 234, "α₁₉₁₅ = 1.75″（翻倍！）", size=11.4, color=ORANGE, anchor="middle", weight="700", halo=True))

    el.append(_box(408, 304, 314, 86, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(565, 325, "机制：光以近 c 高速穿行，空间曲率与时间变慢平分秋色", size=10.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(565, 346, "后牛顿通式：α = (1+γ)·2GM☉/(c²R☉) = 4GM☉/(c²R☉)", size=11.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(565, 368, "平直空间 γ = 0 得 0.875″；广义相对论 γ = 1 得 1.750″！", size=10.6, color=INK, anchor="middle"))

    # Bottom historical twist timeline: how 1914 WWI clouds/arrest saved Einstein!
    el.append(card(22, 418, 716, 102, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(42, 442, "科学史惊险一幕：1914 年的一场大雨和一战战俘营，意外“救”了爱因斯坦的声誉！", size=12.4, color=GREEN, weight="700"))
    steps = [
        (42, "1911 布拉格（0.83″ 半值）"),
        (238, "1914.08 克里米亚日食（扣押＋阴天未拍成）"),
        (508, "1915.11 柏林（补齐空间曲率 → 1.75″）"),
    ]
    for sx_i, t_head in steps:
        el.append(txt(sx_i, 468, f"● {t_head}", size=11.0, color=INK, weight="700"))
    el.append(txt(42, 492, "若 1914 年晴空万里测出 1.75″，当时拿着 0.87″ 错答案的爱因斯坦反而会被判“理论失败”；1915 年补上空间曲率才真正铸就绝杀。", size=10.8, color=BODY))

    write_svg(
        SUBDIR,
        "factor-of-two-1911-vs-1915-spacetime.svg",
        figure(
            H,
            "1911年等效原理半值0.875角秒与1915年广义相对论时空弯曲全值1.75角秒对比图",
            "左栏展示仅计引力时间膨胀得到0.875角秒，右栏展示加入空间曲率γ=1后翻倍至1.750角秒，底栏梳理1914克里米亚日食历史插曲。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_eclipse_geometry_and_plates():
    """Fig 3: Why inward light bending shifts star images OUTWARD + how eclipse vs night check plates work (with 1-shot animation)."""
    H = 532
    extra_css = """
    @keyframes rayTravel {
      0% { stroke-dashoffset: 620; }
      65% { stroke-dashoffset: 0; }
      100% { stroke-dashoffset: 0; }
    }
    @keyframes sightBack {
      0%, 58% { opacity: 0.15; }
      100% { opacity: 1; }
    }
    .anim-ray {
      stroke-dasharray: 620;
      stroke-dashoffset: 0;
      animation: rayTravel 2.8s ease-out 1 both;
    }
    .anim-sight {
      animation: sightBack 2.8s ease-out 1 both;
    }
    @media (prefers-reduced-motion: reduce) {
      .anim-ray, .anim-sight {
        animation: none !important;
        stroke-dashoffset: 0 !important;
        opacity: 1 !important;
      }
    }
    """

    el = [
        *header(
            "最易搞反的几何题：星光明明向太阳“内弯”，星像为什么反而向“外移”？",
            "先看上图光线拐弯与视线反向延长 → 再看下图两张玻璃底片叠合比对法（动画单次演示光路与视位置，角度已放大示意）",
        )
    ]

    # Top panel: Ray geometry (Star -> Grazing eclipsed Sun -> Earth observer -> Apparent position shifted outward!)
    el.append(card(22, 68, 716, 224))
    el.append(step_badge(42, 92, 1, BLUE, BLUE_SOFT))
    el.append(txt(62, 97, "侧视光路解剖：人眼和望远镜“不懂拐弯”，永远顺着光线进镜筒的最后切线往回找星星", size=12.4, color=INK, weight="700"))

    # Reference undisturbed line (Sun absent) from True Star (86, 206) to Earth (662, 206)
    el.append(f'<line x1="86" y1="206" x2="662" y2="206" stroke="{HAIRLINE}" stroke-width="1.5" stroke-dasharray="6,5"/>')
    el.append(txt(222, 224, "半年前夜空无太阳时：星光沿水平直线直达地球", size=10.6, color=MUTED, anchor="middle"))

    # Eclipsed Sun + Moon disk at (378, 244), radius 24
    sun_x, sun_y = 378, 244
    el.append(f'<circle cx="{sun_x}" cy="{sun_y}" r="32" fill="#fde68a" opacity="0.55"/>')
    el.append(f'<circle cx="{sun_x}" cy="{sun_y}" r="22" fill="#1e293b" stroke="#f59e0b" stroke-width="2.5"/>')
    el.append(txt(sun_x, sun_y + 4, "日全食", size=10.5, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(sun_x, sun_y + 40, "月亮挡住刺眼日面，露出日冕旁暗星", size=10.6, color=SLATE, anchor="middle"))

    # Impact parameter b arrow
    el.append(f'<line x1="{sun_x}" y1="{sun_y-22}" x2="{sun_x}" y2="184" stroke="{SLATE}" stroke-width="1.4"/>')
    el.append(txt(sun_x + 10, 202, "掠过距离 b", size=10.5, color=SLATE))

    # True star S1 at (86, 206)
    el.append(f'<circle cx="86" cy="206" r="6.5" fill="{BLUE}"/>')
    el.append(txt(86, 244, "恒星真位置 S", size=11.2, color=BLUE, anchor="middle", weight="700"))

    # Curved real light ray: (86,206) -> apex -> Earth (662,206)
    el.append(f'<path d="M 86,206 Q 378,154 662,206" fill="none" stroke="{ORANGE}" stroke-width="3" class="anim-ray" marker-end="url(#arr-o)"/>')
    el.append(txt(245, 166, "① 真实星光在太阳引力下向内弯折 α", size=11.0, color=ORANGE, anchor="middle", weight="700", halo=True))

    # Apparent straight-line back-projection from Earth (662,206) back to S' (86, 134)
    el.append(f'<line x1="662" y1="206" x2="94" y2="134" stroke="{PURPLE}" stroke-width="2.2" stroke-dasharray="6,4" class="anim-sight" marker-end="url(#arr-p)"/>')
    el.append(f'<circle cx="86" cy="134" r="6.5" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="2.2" class="anim-sight"/>')
    el.append(txt(150, 125, "日食拍到的视位置 S′（向外推开 α！）", size=11.5, color=PURPLE, weight="700", halo=True))
    el.append(txt(536, 174, "② 望远镜顺着入射光线反向直指", size=10.8, color=PURPLE, anchor="middle", weight="700", halo=True))

    # Shift bracket between S (86,206) and S' (86,134)
    el.append(f'<line x1="62" y1="202" x2="62" y2="138" stroke="{PURPLE}" stroke-width="1.8" marker-end="url(#arr-p)"/>')
    el.append(txt(44, 174, "外移", size=10.8, color=PURPLE, anchor="middle", weight="700"))

    # Earth + telescope at right (662, 206)
    el.append(f'<circle cx="684" cy="212" r="18" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    el.append(txt(684, 216, "地球", size=10.5, color=BLUE, anchor="middle", weight="700"))
    el.append(f'<rect x="648" y="198" width="18" height="8" rx="2" transform="rotate(8 657 202)" fill="{INK}"/>')

    # Bottom-left card: Sky plate overlay (May 29 Eclipse Plate + July Night Reference Plate)
    el.append(card(22, 306, 366, 210))
    el.append(step_badge(42, 330, 2, GREEN, GREEN_SOFT))
    el.append(txt(62, 335, "底片叠合法：日全食底片 vs 夜间基准底片", size=12.4, color=INK, weight="700"))
    el.append(txt(42, 355, "离日缘越近外推越大（α ∝ 1/b），越远几乎不动", size=10.8, color=MUTED))

    # Dark circular sky field centered at (122, 436)
    px, py = 122, 436
    el.append(f'<circle cx="{px}" cy="{py}" r="64" fill="#0f172a" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<circle cx="{px}" cy="{py}" r="18" fill="#020617" stroke="#fbbf24" stroke-width="2"/>')
    el.append(txt(px, py + 4, "日冕", size=10.5, color="#fde68a", anchor="middle"))

    stars = [
        (24, -10, 14),
        (-18, -22, 12),
        (16, 26, 11),
        (-36, 18, 7),
        (44, -26, 5.5),
        (-46, -32, 5.0),
    ]
    for dx, dy, shift in stars:
        r_len = math.hypot(dx, dy)
        ux, uy = dx / r_len, dy / r_len
        x0, y0 = px + dx, py + dy
        x1, y1 = x0 + ux * shift, y0 + uy * shift
        el.append(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="2.6" fill="#93c5fd"/>')
        el.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#fb923c" stroke-width="1.8"/>')
        el.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="3.0" fill="#fb923c"/>')

    # Legend on right half of bottom-left card (well separated from px+64=186)
    el.append(f'<circle cx="206" cy="390" r="3.5" fill="#93c5fd"/>')
    el.append(txt(216, 394, "夜间基准星位（无太阳）", size=10.8, color=BODY))
    el.append(f'<circle cx="206" cy="416" r="3.5" fill="#fb923c"/>')
    el.append(txt(216, 420, "日全食星位（辐射外扩）", size=10.8, color=ORANGE, weight="700"))
    el.append(txt(202, 448, "实操：两张玻璃底片药膜贴", size=10.6, color=MUTED))
    el.append(txt(202, 468, "药膜，测微显微镜逐颗比对，", size=10.6, color=MUTED))
    el.append(txt(202, 488, "扣除大气折射与热胀缩放。", size=10.6, color=MUTED))

    # Bottom-right card: How tiny is 1.75 arcseconds?
    el.append(card(402, 306, 336, 210))
    el.append(step_badge(422, 330, 3, ORANGE, ORANGE_SOFT))
    el.append(txt(442, 335, "1.75 角秒到底有多小？苛刻到极致的精度", size=12.4, color=INK, weight="700"))
    el.append(txt(422, 355, "1 度 = 60 角分 = 3,600 角秒 → 1.75″ ≈ 0.000486°", size=10.8, color=MUTED))

    el.append(_box(420, 372, 300, 60, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(570, 395, "一枚直径 25 mm 的 1 元硬币", size=12.0, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(570, 417, "放到 2.95 公里（近 6 里地）外张开的视角！", size=11.2, color=INK, anchor="middle", weight="700"))

    el.append(_box(420, 444, 300, 58, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(570, 466, "在索布拉尔 5.8 米长焦望远镜底片上：", size=11.0, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(570, 487, "2 倍太阳半径处星点仅挪动 0.025 mm（1/3 根头发丝）", size=10.6, color=INK, anchor="middle"))

    write_svg(
        SUBDIR,
        "eclipse-measurement-geometry-outward-shift.svg",
        figure(
            H,
            "日全食星光向内弯曲导致星像向外偏移的几何原理与底片叠合测量图",
            "上图演示星光向太阳内折而视线反向延长使星像外移，左下展示日全食底片与夜间基准底片叠合呈1/b辐射外扩，右下换算1.75角秒相当于2.95公里外一元硬币宽度。",
            el,
            extra_css=extra_css,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_1919_data_and_controversy():
    """Fig 4: Real 1919 Sobral & Principe data curves + error bars + 1979 RGO machine reanalysis."""
    H = 556
    el = [
        *header(
            "1919 年一锤定音的真实数据，以及“爱丁顿有没有偏心删数据”历史悬案",
            "左看索布拉尔 4 英寸镜 7 颗毕星团恒星实测曲线 → 右看三套原始数据与 1979 年现代测片仪重测铁证",
        )
    ]

    # Left panel: Deflection vs distance r / R_sun plot (reconstructed mathematically from Dyson et al. 1920 Diagram 2)
    el.append(card(22, 68, 366, 470))
    el.append(txt(42, 95, "星像外移量 α 随离日心距离 r / R☉ 衰减曲线", size=12.6, color=INK, weight="700"))
    el.append(txt(42, 115, "实线：广义相对论 1.75″/(r/R☉) ｜ 虚线：牛顿半值 0.875″/(r/R☉)", size=10.5, color=MUTED))

    # Plot axes: x in [1.0, 6.2] -> px [78, 362]; y in [0.0, 2.0] arcsec -> py [436, 150]
    px0, px1 = 78.0, 362.0
    py0, py1 = 436.0, 150.0

    def map_x(r_ratio):
        return px0 + (r_ratio - 1.0) / 5.2 * (px1 - px0)

    def map_y(arcsec):
        return py0 - (arcsec / 2.0) * (py0 - py1)

    # Horizontal grid & y-axis labels
    for y_val in [0.0, 0.5, 1.0, 1.5, 2.0]:
        yy = map_y(y_val)
        el.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="#e2e8f0" stroke-width="1"/>')
        el.append(txt(px0 - 8, yy + 4, f'{y_val:.1f}″', size=10.5, color=MUTED, anchor="end"))

    # Vertical grid & x-axis labels
    for r_val in [1, 2, 3, 4, 5, 6]:
        xx = map_x(r_val)
        el.append(f'<line x1="{xx:.1f}" y1="{py1}" x2="{xx:.1f}" y2="{py0}" stroke="#f1f5f9" stroke-width="1"/>')
        el.append(txt(xx, py0 + 18, f"{r_val}R☉", size=10.5, color=MUTED, anchor="middle"))

    el.append(f'<line x1="{px0}" y1="{py1}" x2="{px0}" y2="{py0}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{px0}" y1="{py0}" x2="{px1}" y2="{py0}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(txt((px0 + px1) / 2, py0 + 40, "恒星视线距太阳中心距离 r（太阳半径 R☉ 倍数）", size=10.8, color=INK, anchor="middle"))

    # Solar limb vertical marker at r = 1 R_sun
    el.append(f'<rect x="{px0}" y="{py1}" width="10" height="{py0-py1}" fill="#fef3c7" opacity="0.7"/>')
    el.append(txt(px0 + 12, py1 + 14, "日缘 r = 1R☉", size=10.5, color="#b45309"))

    # GR curve: alpha = 1.750 / r
    pts_gr = " ".join(f"{map_x(1.0 + 0.1*k):.1f},{map_y(1.750 / (1.0 + 0.1*k)):.1f}" for k in range(53))
    el.append(f'<polyline points="{pts_gr}" fill="none" stroke="{ORANGE}" stroke-width="2.8"/>')

    # Newtonian / 1911 curve: alpha = 0.875 / r
    pts_nw = " ".join(f"{map_x(1.0 + 0.1*k):.1f},{map_y(0.875 / (1.0 + 0.1*k)):.1f}" for k in range(53))
    el.append(f'<polyline points="{pts_nw}" fill="none" stroke="{BLUE}" stroke-width="2.2" stroke-dasharray="6,4"/>')

    # 7 Hyades stars from Sobral 4-inch lens (Dyson, Eddington & Davidson 1920 radial displacements)
    sobral_stars = [
        (1.99, 1.00),
        (2.12, 0.92),
        (3.13, 0.56),
        (3.28, 0.58),
        (4.09, 0.44),
        (5.12, 0.36),
        (5.39, 0.33),
    ]
    for rr, aa in sobral_stars:
        sx_p, sy_p = map_x(rr), map_y(aa)
        el.append(f'<circle cx="{sx_p:.1f}" cy="{sy_p:.1f}" r="4.5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.4"/>')

    el.append(txt(map_x(2.7), map_y(1.22), "广义相对论 1.75″/r", size=11.0, color=ORANGE, weight="700", halo=True))
    el.append(txt(map_x(3.3), map_y(0.14), "牛顿/1911 半值 0.875″/r", size=10.8, color=BLUE, weight="700", halo=True))
    el.append(f'<circle cx="46" cy="512" r="4.5" fill="{GREEN}"/>')
    el.append(txt(58, 516, "绿点：索布拉尔 4 英寸镜实测 7 颗恒星（外推日缘 1.98″）", size=10.5, color=INK, weight="700"))

    # Right panel: Error-bar comparison of all 1919 instruments + 1979 RGO machine reanalysis
    el.append(card(402, 68, 336, 470))
    el.append(txt(420, 95, "三台望远镜实测值与 1979 现代重测平反", size=12.6, color=INK, weight="700"))
    el.append(txt(420, 115, "换算至日缘（r = R☉）偏折角及误差棒对比", size=10.5, color=MUTED))

    # Horizontal scale for right chart: [0.4", 2.4"] -> [434, 714]
    bx0, bx1 = 434.0, 714.0

    def map_bx(val):
        return bx0 + (val - 0.4) / 2.0 * (bx1 - bx0)

    # Vertical reference lines at 0.875" (Newton) and 1.750" (Einstein)
    xn = map_bx(0.875)
    xe = map_bx(1.750)
    el.append(f'<line x1="{xn:.1f}" y1="146" x2="{xn:.1f}" y2="412" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5,4"/>')
    el.append(f'<line x1="{xe:.1f}" y1="146" x2="{xe:.1f}" y2="412" stroke="{ORANGE}" stroke-width="2.0"/>')
    el.append(txt(xn - 4, 140, "牛顿 0.88″", size=10.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(xe + 6, 140, "爱因斯坦 1.75″", size=10.5, color=ORANGE, anchor="middle", weight="700"))

    rows = [
        ("① 索布拉尔 4 英寸镜（7 星清晰）：1.98″ ± 0.18″", 1.98, 0.18, GREEN, 180),
        ("② 普林西比 13 英寸镜（云缝 2 片）：1.61″ ± 0.45″", 1.61, 0.45, PURPLE, 236),
        ("③ 索布拉尔 13 英寸镜（晒弯失焦）：0.93″ / 固焦 1.52″", 0.93, 0.30, SLATE, 292),
        ("④ 1979 现代测片仪重测 4 英寸原片：1.90″ ± 0.11″", 1.90, 0.11, GREEN, 348),
        ("⑤ 1979 重测失焦 13 英寸原片：1.55″ ± 0.34″", 1.55, 0.34, ORANGE, 404),
    ]
    for label_top, mean_v, err_v, col, yy in rows:
        el.append(txt(420, yy - 14, label_top, size=10.6, color=INK, weight="700", halo=True))
        xc = map_bx(mean_v)
        xl = max(bx0, map_bx(mean_v - err_v))
        xr = min(bx1, map_bx(mean_v + err_v))
        el.append(f'<line x1="{xl:.1f}" y1="{yy}" x2="{xr:.1f}" y2="{yy}" stroke="{col}" stroke-width="3"/>')
        el.append(f'<line x1="{xl:.1f}" y1="{yy-5}" x2="{xl:.1f}" y2="{yy+5}" stroke="{col}" stroke-width="2"/>')
        el.append(f'<line x1="{xr:.1f}" y1="{yy-5}" x2="{xr:.1f}" y2="{yy+5}" stroke="{col}" stroke-width="2"/>')
        el.append(f'<circle cx="{xc:.1f}" cy="{yy}" r="5" fill="{col}" stroke="#ffffff" stroke-width="1.4"/>')

    # Verdict box at bottom-right
    el.append(_box(416, 430, 308, 92, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(570, 452, "真相核查（Kennefick 档案考证）：", size=11.0, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(570, 472, "索布拉尔数据由皇家天文学家戴森团队独立处理；", size=10.5, color=INK, anchor="middle"))
    el.append(txt(570, 491, "13 英寸镜因烈日晒弯定天镜失焦，次日即记录在案；", size=10.5, color=INK, anchor="middle"))
    el.append(txt(570, 510, "1979 年自动测片仪重测两套原片双双支持广义相对论！", size=10.5, color=GREEN, anchor="middle", weight="700"))

    write_svg(
        SUBDIR,
        "sobral-principe-1919-data-and-controversy.svg",
        figure(
            H,
            "1919年索布拉尔与普林西比日全食实测数据曲线及1979年重测核查图",
            "左栏绘制索布拉尔4英寸望远镜7颗恒星偏折角随距离衰减点位与广义相对论及牛顿理论曲线对比，右栏对比三组1919原始误差棒与1979年格林尼治天文台自动测片仪重测结果。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_modern_precision_tests():
    """Fig 5: Ditching solar eclipses — VLBI quasars (0.02%), Cassini Shapiro delay (0.002%), and ESA Gaia Jupiter (10 mas)."""
    H = 524
    el = [
        *header(
            "不用再苦等日全食！现代物理学怎样把验证精度狂飙一万倍？",
            "从光学底片的 10% 误差，到洲际射电干涉（VLBI）、卡西尼号穿日无线电与盖亚卫星全天微角秒测绘",
        )
    ]

    cards_spec = [
        (
            22,
            BLUE,
            BLUE_SOFT,
            "1. 洲际射电干涉（VLBI）",
            "大白天透视日冕盯紧类星体",
            "射电波不怕蓝天散射！全球 87 台",
            "射电望远镜联网成“地球口径大眼”，",
            "20 年追踪 541 颗类星体 170 万次。",
            "Shapiro 等 (2004)：",
            "γ = 0.99983 ± 0.00045",
            "相对误差 0.02%（2018 再提 4.5 倍）",
        ),
        (
            268,
            ORANGE,
            ORANGE_SOFT,
            "2. 卡西尼号土星飞船（2003）",
            "引力掰弯光路＋拉长飞行时间",
            "飞船绕到太阳正背面（上合），双频",
            "无线电擦过日缘往返，消去日冕等离",
            "子体干扰，直测夏皮罗引力延迟。",
            "Bertotti 等 (2003, Nature)：",
            "γ − 1 = (2.1 ± 2.3) × 10⁻⁵",
            "精度高达十万分之二（0.002%）！",
        ),
        (
            514,
            GREEN,
            GREEN_SOFT,
            "3. 欧空局盖亚卫星（Gaia）",
            "连木星掰弯星光都能直接拍到！",
            "太空无大气抖动，测角达微角秒级：",
            "不仅全天修正太阳弯曲（离太阳 90°",
            "处星光仍偏折 4.07 毫角秒！），",
            "2022 公布木星掠射实测：",
            "距木星边缘 7″ 偏折 10 毫角秒",
            "连巨行星扁率四极矩都能分辨！",
        ),
    ]

    for cx, col, soft, t1, t2, l1, l2, l3, res_k, res_v, res_foot in cards_spec:
        el.append(card(cx, 68, 224, 326))
        el.append(_box(cx + 14, 82, 196, 26, fill=soft, stroke=col))
        el.append(txt(cx + 112, 100, t1, size=11.6, color=col, anchor="middle", weight="700"))
        el.append(txt(cx + 112, 124, t2, size=11.0, color=INK, anchor="middle", weight="700"))

        # Mini schematic box inside each card [y=136..226]
        el.append(f'<rect x="{cx+16}" y="136" width="192" height="86" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')

        el.append(txt(cx + 16, 244, l1, size=10.6, color=BODY))
        el.append(txt(cx + 16, 263, l2, size=10.6, color=BODY))
        el.append(txt(cx + 16, 282, l3, size=10.6, color=BODY))

        el.append(_box(cx + 14, 298, 196, 82, fill=soft, stroke=BORDER))
        el.append(txt(cx + 112, 318, res_k, size=10.5, color=MUTED, anchor="middle"))
        el.append(txt(cx + 112, 341, res_v, size=11.4, color=col, anchor="middle", weight="700"))
        el.append(txt(cx + 112, 364, res_foot, size=10.5, color=INK, anchor="middle", weight="700"))

    # Card 1 mini-diagram: Quasar waves -> Sun -> Earth 2 VLBI dishes
    c1 = 22
    el.append(f'<circle cx="{c1+42}" cy="175" r="5" fill="{PURPLE}"/>')
    el.append(txt(c1 + 42, 204, "类星体", size=10.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(f'<circle cx="{c1+108}" cy="190" r="14" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>')
    el.append(f'<path d="M {c1+48},175 Q {c1+108},154 {c1+174},164" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    el.append(f'<path d="M {c1+48},175 Q {c1+108},164 {c1+174},194" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="4,3"/>')
    el.append(f'<circle cx="{c1+182}" cy="179" r="16" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.5"/>')
    el.append(f'<circle cx="{c1+174}" cy="164" r="3" fill="{INK}"/>')
    el.append(f'<circle cx="{c1+174}" cy="194" r="3" fill="{INK}"/>')

    # Card 2 mini-diagram: Earth <-> Sun <-> Cassini at Saturn
    c2 = 268
    el.append(f'<circle cx="{c2+44}" cy="178" r="11" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.5"/>')
    el.append(txt(c2 + 50, 212, "深空网", size=10.5, color=BLUE, anchor="middle"))
    el.append(f'<circle cx="{c2+112}" cy="190" r="15" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>')
    el.append(f'<path d="M {c2+56},175 Q {c2+112},148 {c2+174},175" fill="none" stroke="{ORANGE}" stroke-width="2.4" marker-end="url(#arr-o)"/>')
    el.append(f'<rect x="{c2+174}" y="169" width="14" height="12" rx="2" fill="{SLATE}"/>')
    el.append(txt(c2 + 178, 212, "卡西尼", size=10.5, color=SLATE, anchor="middle"))

    # Card 3 mini-diagram: Star grazing Jupiter limb (7") -> Gaia L2 spacecraft
    c3 = 514
    el.append(f'<circle cx="{c3+86}" cy="178" r="18" fill="#fed7aa" stroke="#c2410c" stroke-width="1.5"/>')
    el.append(f'<line x1="{c3+69}" y1="173" x2="{c3+103}" y2="173" stroke="#ea580c" stroke-width="2"/>')
    el.append(f'<line x1="{c3+69}" y1="183" x2="{c3+103}" y2="183" stroke="#ea580c" stroke-width="1.5"/>')
    el.append(txt(c3 + 86, 213, "木星", size=10.5, color="#9a3412", anchor="middle", weight="700"))
    el.append(f'<circle cx="{c3+34}" cy="160" r="4" fill="{GREEN}"/>')
    el.append(f'<path d="M {c3+38},160 Q {c3+88},148 {c3+174},174" fill="none" stroke="{GREEN}" stroke-width="2.2" marker-end="url(#arr-g)"/>')
    el.append(f'<polygon points="{c3+178},164 {c3+194},174 {c3+178},184" fill="{GREEN}"/>')
    el.append(txt(c3 + 180, 212, "Gaia", size=10.5, color=GREEN, anchor="middle", weight="700"))

    # Bottom log-precision progression bar
    el.append(card(22, 408, 716, 100))
    el.append(txt(42, 432, "百年空间曲率参数 γ 检验精度跃迁（广义相对论预言 γ ≡ 1，不确定度越小越苛刻）：", size=11.8, color=INK, weight="700"))

    lx0, lx1, ly = 66.0, 694.0, 468.0
    el.append(f'<line x1="{lx0}" y1="{ly}" x2="{lx1}" y2="{ly}" stroke="{HAIRLINE}" stroke-width="4" stroke-linecap="round"/>')
    milestones = [
        (0.00, "1919 光学日食", "误差 ~10%–20%", SLATE),
        (0.33, "1970s 早期射电", "误差 ~1%", BLUE),
        (0.66, "2004 全球 VLBI", "误差 0.045%", PURPLE),
        (1.00, "2003 卡西尼号穿日", "误差 0.0023%（提升近万倍！）", ORANGE),
    ]
    for frac, m_top, m_bot, col in milestones:
        mx = lx0 + frac * (lx1 - lx0)
        el.append(f'<circle cx="{mx:.1f}" cy="{ly}" r="6.5" fill="{col}" stroke="#ffffff" stroke-width="1.8"/>')
        anc = "start" if frac == 0 else ("end" if frac == 1 else "middle")
        el.append(txt(mx, ly - 13, m_top, size=10.8, color=col, anchor=anc, weight="700"))
        el.append(txt(mx, ly + 23, m_bot, size=10.5, color=BODY, anchor=anc))

    write_svg(
        SUBDIR,
        "modern-precision-vlbi-cassini-gaia.svg",
        figure(
            H,
            "现代检验光线弯曲三大精密手段：VLBI射电干涉、卡西尼号夏皮罗延迟与盖亚卫星木星实测图",
            "对比全球VLBI类星体干涉测量、卡西尼号太阳上合双频射电延迟及欧空局Gaia空间望远镜木星掠射偏折，展示后牛顿参数γ检验精度从百分之十跃升至十万分之二。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_gravitational_lensing_tool():
    """Fig 6: From verifying Einstein to using gravitational lensing as a cosmic telescope & dark-matter/white-dwarf scale."""
    H = 518
    el = [
        *header(
            "终极反转：从“费尽心机验证爱因斯坦”，变成称量暗物质与恒星的宇宙放大镜",
            "左看星系团强引力透镜（爱因斯坦环与四重像）→ 右看哈勃推翻爱因斯坦 1936 悲观预言、直接给孤立白矮星称重",
        )
    ]

    # Left panel: Galaxy-cluster strong gravitational lensing (Einstein ring & Einstein Cross)
    el.append(card(22, 68, 366, 434))
    el.append(step_badge(42, 92, 1, PURPLE, PURPLE_SOFT))
    el.append(txt(62, 97, "星系级强引力透镜：给看不见的暗物质“过秤”", size=12.4, color=INK, weight="700"))
    el.append(txt(42, 117, "前景星系团时空凹陷把背景星系星光从上下左右同时掰弯汇聚", size=10.6, color=MUTED))

    # Side-on 3D schematic of lensing
    el.append(f'<rect x="38" y="132" width="334" height="176" rx="8" fill="#0f172a"/>')
    el.append(f'<circle cx="72" cy="214" r="8" fill="#38bdf8"/>')
    el.append(txt(72, 242, "百亿光年外", size=10.5, color="#bae6fd", anchor="middle"))
    el.append(txt(72, 260, "背景星系", size=10.5, color="#bae6fd", anchor="middle"))

    el.append(f'<circle cx="198" cy="214" r="34" fill="#a855f7" opacity="0.24"/>')
    el.append(f'<circle cx="198" cy="214" r="13" fill="#fbbf24"/>')
    el.append(txt(198, 294, "前景星系团＋暗物质晕", size=10.5, color="#e9d5ff", anchor="middle", weight="700"))

    el.append(f'<path d="M 80,212 Q 198,148 320,212" fill="none" stroke="#38bdf8" stroke-width="2.3"/>')
    el.append(f'<path d="M 80,216 Q 198,280 320,216" fill="none" stroke="#38bdf8" stroke-width="2.3"/>')
    el.append(f'<line x1="320" y1="212" x2="220" y2="160" stroke="#7dd3fc" stroke-width="1.3" stroke-dasharray="4,3"/>')
    el.append(f'<line x1="320" y1="216" x2="220" y2="268" stroke="#7dd3fc" stroke-width="1.3" stroke-dasharray="4,3"/>')
    el.append(f'<circle cx="330" cy="214" r="9" fill="#e2e8f0" stroke="#38bdf8" stroke-width="2"/>')
    el.append(txt(330, 244, "太空望远镜", size=10.5, color="#e2e8f0", anchor="middle"))

    # Two visual badges below dark box: Einstein Ring & Supernova Refsdal Einstein Cross
    el.append(_box(38, 322, 160, 82, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(f'<circle cx="72" cy="363" r="18" fill="none" stroke="{PURPLE}" stroke-width="3.2" stroke-dasharray="22,6"/>')
    el.append(f'<circle cx="72" cy="363" r="5" fill="#d97706"/>')
    el.append(txt(144, 354, "正对共线：", size=10.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(144, 374, "爱因斯坦环", size=11.2, color=PURPLE, anchor="middle", weight="700"))

    el.append(_box(212, 322, 160, 82, fill=BLUE_SOFT, stroke=BLUE_LINE))
    cx_cross, cy_cross = 246, 363
    el.append(f'<circle cx="{cx_cross}" cy="{cy_cross}" r="5" fill="#d97706"/>')
    for dx_c, dy_c in [(0, -14), (14, 0), (0, 14), (-14, 0)]:
        el.append(f'<circle cx="{cx_cross+dx_c}" cy="{cy_cross+dy_c}" r="3.5" fill="{BLUE}"/>')
    el.append(txt(318, 354, "椭球偏心：", size=10.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(318, 374, "爱因斯坦十字", size=11.2, color=BLUE, anchor="middle", weight="700"))

    el.append(_box(38, 416, 334, 72, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(205, 438, "爱因斯坦环角半径：θ_E = √[(4GM/c²) · D_LS / (D_L D_S)]", size=10.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(205, 459, "发光恒星远远不够掰出这么大的环 → 直接称出星系团里", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(205, 477, "约 85% 的引力质量是不发光的“暗物质”！", size=10.8, color=PURPLE, anchor="middle", weight="700"))

    # Right panel: 1936 Einstein Science paper vs 2017/2023 Hubble weighing lone white dwarfs!
    el.append(card(402, 68, 336, 434))
    el.append(step_badge(422, 92, 2, ORANGE, ORANGE_SOFT))
    el.append(txt(442, 97, "天体测量微透镜：给孤立死亡恒星“单颗称重”", size=12.4, color=INK, weight="700"))
    el.append(txt(422, 117, "相隔百年的跨时空对话：哈勃望远镜圆了爱因斯坦不敢想的梦", size=10.6, color=MUTED))

    el.append(_box(418, 134, 304, 74, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(570, 156, "1936 年爱因斯坦在《Science》撰文感叹：", size=11.0, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(570, 177, "单颗恒星引力透镜角太小，“我们毫无希望直接观测到”", size=10.6, color=INK, anchor="middle"))
    el.append(txt(570, 196, "（当年地面望远镜根本分不开几毫角秒的星点偏移）", size=10.5, color=MUTED, anchor="middle"))

    el.append(f'<line x1="570" y1="214" x2="570" y2="242" stroke="{GREEN}" stroke-width="2.4" marker-end="url(#arr-g)"/>')
    el.append(txt(644, 232, "百年太空光学突破", size=10.6, color=GREEN, anchor="middle", weight="700"))

    el.append(f'<rect x="418" y="248" width="304" height="148" rx="8" fill="{GREEN_SOFT}" stroke="#86efac"/>')
    el.append(txt(570, 270, "2017 & 2023 哈勃望远镜（Gaia 提前预报交会）：", size=11.0, color=GREEN, anchor="middle", weight="700"))

    el.append(f'<line x1="444" y1="326" x2="696" y2="308" stroke="{SLATE}" stroke-width="1.6" stroke-dasharray="5,4" marker-end="url(#arr-s)"/>')
    el.append(f'<circle cx="534" cy="319" r="9" fill="#ffffff" stroke="{BLUE}" stroke-width="2.5"/>')
    el.append(txt(502, 344, "前景白矮星", size=10.5, color=BLUE, anchor="middle", weight="700"))

    el.append(f'<circle cx="556" cy="298" r="3.5" fill="{MUTED}"/>')
    el.append(f'<circle cx="566" cy="285" r="4.5" fill="{ORANGE}"/>')
    el.append(f'<line x1="556" y1="298" x2="566" y2="285" stroke="{ORANGE}" stroke-width="2"/>')
    el.append(txt(640, 290, "背景星偏移 ~2 毫角秒！", size=10.6, color=ORANGE, anchor="middle", weight="700"))

    el.append(txt(570, 368, "● 2017 Stein 2051 B：测出 0.675 M☉，验证简并态理论", size=10.5, color=INK, anchor="middle"))
    el.append(txt(570, 388, "● 2023 孤立白矮星 LAWD 37：首测单星 0.56 M☉！", size=10.5, color=INK, anchor="middle", weight="700"))

    el.append(_box(418, 410, 304, 78, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(570, 434, "精度对比：比 1919 日全食偏折角还要小 625 倍！", size=11.2, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(570, 455, "相当于从地球看清月球表面停着的一辆小汽车长度——", size=10.5, color=INK, anchor="middle"))
    el.append(txt(570, 474, "广义相对论早已从“被考证的猜想”变成天文学日常标尺", size=10.5, color=MUTED, anchor="middle"))

    write_svg(
        SUBDIR,
        "gravitational-lensing-cosmic-scale.svg",
        figure(
            H,
            "引力透镜现代应用：星系团暗物质称重与哈勃望远镜孤立白矮星微透镜测质量图",
            "左栏展示前景星系团弯曲背景星光形成爱因斯坦环与四重像并称量暗物质，右栏展示哈勃望远镜通过2毫角秒天体测量微透镜直接测出白矮星Stein 2051 B与孤立白矮星LAWD 37质量。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


@register(
    "einstein-light-bending",
    "Einstein gravitational light deflection: equivalence principle, 1911 vs 1915 factor of 2, 1919 eclipse & modern VLBI/Gaia/Hubble tests",
    "physics",
)
def build_einstein_light_bending():
    _verify_light_bending_math()
    _build_elevator_equivalence()
    _build_1911_vs_1915_factor_of_two()
    _build_eclipse_geometry_and_plates()
    _build_1919_data_and_controversy()
    _build_modern_precision_tests()
    _build_gravitational_lensing_tool()
