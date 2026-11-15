"""Original 760px Chinese SVG diagrams for the Angular Momentum & Applications post."""

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

SUBDIR = "angular-momentum"


def _verify_angular_momentum_math():
    """Verify every rotational equation, inertia ratio, precession rate, and cat-twist angle."""
    # 1. Straight-line particle angular momentum invariance: L = r * p * sin(theta) = r_perp * p
    r_perp = 3.0
    p_mag = 12.0
    for x in [-5.0, 0.0, 4.0, 11.0]:
        r = math.hypot(x, r_perp)
        sin_theta = r_perp / r
        assert abs(r * p_mag * sin_theta - r_perp * p_mag) < 1e-12

    # 2. Skater inertia 4x reduction -> 4x angular speed AND 4x rotational kinetic energy
    i0, w0 = 4.0, 1.5 * 2.0 * math.pi
    l0 = i0 * w0
    i1 = 0.25 * i0
    w1 = l0 / i1
    assert abs(w1 / w0 - 4.0) < 1e-12
    k0 = 0.5 * i0 * w0**2
    k1 = 0.5 * i1 * w1**2
    assert abs(k1 / k0 - 4.0) < 1e-12

    # 3. Gyroscope precession rate (OpenStax University Physics Vol 1 Example 11.10)
    m_top, r_disk, r_cm, f_spin, g = 0.30, 0.05, 0.05, 20.0, 9.8
    i_top = 0.5 * m_top * r_disk**2
    w_spin = 2.0 * math.pi * f_spin
    w_prec = (r_cm * m_top * g) / (i_top * w_spin)
    t_prec = 2.0 * math.pi / w_prec
    assert 3.11 < w_prec < 3.13 and 2.00 < t_prec < 2.03

    # 4. Falling cat two-phase tuck-and-twist zero-angular-momentum arithmetic
    # Phase 1: I_front = 1, I_rear = 3, relative twist +160 deg -> d_front = +120, d_rear = -40
    df1, dr1 = 120.0, -40.0
    assert abs(1.0 * df1 + 3.0 * dr1) < 1e-12
    # Phase 2: I_front = 3, I_rear = 1, untwist -160 deg -> d_front = -40, d_rear = +120
    df2, dr2 = -40.0, 120.0
    assert abs(3.0 * df2 + 1.0 * dr2) < 1e-12
    assert abs((df1 + df2) - 80.0) < 1e-12 and abs((dr1 + dr2) - 80.0) < 1e-12

    # 5. Hubble Space Telescope reaction wheel ratio check
    # 45 kg wheel r~0.3m (I_w ~ 2 kg*m^2) vs 11,000 kg bus (I_h ~ 30,000-80,000 kg*m^2)
    i_wheel = 0.5 * 45.0 * 0.30**2
    assert 1.8 < i_wheel < 2.2


def _build_vector_and_inertia_svg():
    el = []
    el.extend(
        header(
            "什么是角动量？连走直线的飞球都有角动量，而且方向居然“竖着指天”！",
            "角动量衡量“转动有多难刹住”：单质点看垂直力臂 L = r⊥mv，刚体看转动惯量 L = Iω",
        )
    )

    # Left panel: Straight-line particle has conserved L!
    el.append(card(24, 66, 356, 408))
    el.append(txt(42, 92, "一、反直觉真相：走直线照样有角动量！", size=13, color=INK, weight="700"))

    el.append(card(40, 108, 324, 198, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Trajectory line at y=148
    el.append(f'<line x1="56" y1="148" x2="348" y2="148" stroke="{BLUE_LINE}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    # Pivot O at (112, 258)
    ox, oy = 112, 258
    el.append(f'<circle cx="{ox}" cy="{oy}" r="5.5" fill="{INK}"/>')
    el.append(txt(ox, oy + 20, "参考支点 O", size=10.8, color=INK, anchor="middle", weight="700"))

    # Perpendicular lever arm r_perp from (112,258) to (112,148)
    el.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="148" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="4 3"/>')
    el.append(f'<rect x="{ox}" y="148" width="9" height="9" fill="none" stroke="{GREEN}" stroke-width="1.2"/>')
    el.append(txt(ox - 10, 206, "垂直力臂 r⊥", size=10.6, color=GREEN, anchor="end", weight="700"))

    # Ball at Position 1 (x=166, y=148) and Position 2 (x=276, y=148)
    for px, lbl in [(168, "时刻 t₁"), (274, "时刻 t₂")]:
        el.append(f'<line x1="{ox}" y1="{oy}" x2="{px}" y2="148" stroke="{SLATE}" stroke-width="1.3"/>')
        el.append(f'<circle cx="{px}" cy="148" r="7" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.8"/>')
        el.append(f'<line x1="{px + 8}" y1="148" x2="{px + 48}" y2="148" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
        el.append(txt(px, 132, lbl, size=10.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(322, 134, "动量 p=mv", size=10.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(228, 224, "矢径 r 变长，但夹角 θ 变小", size=10.4, color=SLATE, anchor="middle", halo=True))
    el.append(txt(228, 242, "乘积 r·sinθ ≡ r⊥ 纹丝不变！", size=10.6, color=GREEN, anchor="middle", weight="700", halo=True))

    # Text summary box
    el.append(card(40, 318, 324, 142, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(54, 341, "公式拆解：L = r × p ，大小 L = r⊥ · m · v", size=11.4, color=BLUE, weight="700"))
    el.append(txt(54, 364, "• 只要直线轨迹不穿过支点 O（r⊥ > 0），飞球相对", size=10.8, color=BODY))
    el.append(txt(54, 384, "  于 O 就拥有恒定角动量！", size=10.8, color=BODY))
    el.append(txt(54, 406, "• 比如滑冰场上你伸手接住迎面偏侧飞来的冰球，", size=10.8, color=BODY))
    el.append(txt(54, 426, "  原本走直线的冰球会立刻把你撞得原地转起圈来", size=10.8, color=INK, weight="700"))
    el.append(txt(54, 446, "  ——那就是它自带的角动量交到了你身上！", size=10.8, color=INK, weight="700"))

    # Right panel: Right-hand rule + Moment of inertia I = sum m r^2
    el.append(card(394, 66, 342, 408))
    el.append(txt(412, 92, "二、右手定则与“质量离轴越远越难停”", size=13, color=INK, weight="700"))

    el.append(card(410, 108, 310, 174, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Spinning horizontal disk centered at (516, 212)
    dx, dy = 512, 214
    el.append(f'<ellipse cx="{dx}" cy="{dy}" rx="74" ry="26" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="2"/>')
    # Upward L vector along axis!
    el.append(f'<line x1="{dx}" y1="{dy + 34}" x2="{dx}" y2="126" stroke="{PURPLE}" stroke-width="3" marker-end="url(#arr-muted)"/>')
    el.append(txt(dx, 120, "角动量矢量 L（竖直向上！）", size=10.8, color=PURPLE, anchor="middle", weight="700"))
    # Rotation direction curved arrow on disk front
    el.append(f'<path d="M462,222 Q512,244 560,220" fill="none" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
    el.append(txt(dx, 256, "逆时针旋转角速度 ω", size=10.4, color=ORANGE, anchor="middle", weight="700"))

    # Right-hand rule note on right side of box
    el.append(txt(650, 166, "右手螺旋定则：", size=10.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(650, 188, "四指顺着旋转方向", size=10.4, color=BODY, anchor="middle"))
    el.append(txt(650, 206, "弯曲，大拇指所指", size=10.4, color=BODY, anchor="middle"))
    el.append(txt(650, 224, "的转轴方向就是 L！", size=10.4, color=PURPLE, anchor="middle", weight="700"))

    # Moment of inertia comparison (same M, same R, same omega!)
    el.append(card(410, 294, 310, 166, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(426, 317, "刚体公式 L = Iω（转动惯量 I = Σ mᵢ rᵢ²）：", size=11.4, color=ORANGE, weight="700"))
    el.append(txt(426, 340, "同样质量 M、同样外半径 R、同样转速 ω 下：", size=10.6, color=BODY))

    shapes = [
        ("薄圆环（车轮外圈）", "I = M R²", 1.00, BLUE),
        ("均匀实心圆盘", "I = 0.5 M R²", 0.50, GREEN),
        ("均匀实心圆球", "I = 0.4 M R²", 0.40, SLATE),
    ]
    for si, (sname, sform, frac, scol) in enumerate(shapes):
        sy = 362 + si * 28
        el.append(txt(426, sy, f"{sname}", size=10.4, color=INK, weight="600"))
        bw = 96 * frac
        el.append(f'<rect x="556" y="{sy - 10}" width="{bw:.1f}" height="12" rx="3" fill="#ffffff" stroke="{scol}" stroke-width="1.5"/>')
        el.append(txt(562 + bw, sy, sform, size=10, color=scol, weight="700"))
    el.append(txt(426, 446, "结论：质量越往外圈甩（r² 放大），角动量越强劲！", size=10.6, color=INK, weight="700"))

    svg = figure(
        492,
        "质点与刚体角动量定义、右手螺旋定则与转动惯量分布对比图",
        "左栏展示沿直线运动的物体只要垂直力臂r⊥不为零就具有恒定角动量L=r⊥mv；右栏展示刚体旋转L=Iω的右手螺旋定则方向，并对比同质量同半径下薄圆环、实心盘与实心球的转动惯量差异。",
        el,
    )
    write_svg(SUBDIR, "vector-definition-and-lever-arm.svg", svg)


def _build_skater_spin_svg():
    # Exact 1:4 rotation angle ratio in identical 2.8s duration: wide spins 180 deg, tucked spins 720 deg!
    extra_css = """
  .spin-wide {
    transform-box: view-box;
    transform-origin: 120px 236px;
    animation: turnWide 2.8s ease-out 0.25s 1 forwards;
  }
  .spin-tuck {
    transform-box: view-box;
    transform-origin: 298px 236px;
    animation: turnTuck 2.8s ease-out 0.25s 1 forwards;
  }
  @keyframes turnWide {
    from { transform: rotate(0deg); }
    to   { transform: rotate(-180deg); }
  }
  @keyframes turnTuck {
    from { transform: rotate(0deg); }
    to   { transform: rotate(-720deg); }
  }
  @media (prefers-reduced-motion: reduce) {
    .spin-wide, .spin-tuck { animation: none; }
  }"""

    el = []
    el.extend(
        header(
            "花样滑冰选手一抱臂转速暴涨 4 倍，可“翻了 4 倍的动能”是谁给的？",
            "冰刀摩擦力矩近乎为零，角动量 L = Iω 严格守恒；但转动动能并不守恒——全靠手臂肌肉向内硬拽做功！",
        )
    )

    # Left panel: Top-down 1:4 angular speed comparison
    el.append(card(24, 66, 376, 434))
    el.append(txt(42, 92, "一、俯视对比：等效半径缩半 → 惯量降为 1/4 → 转速 ×4", size=12.4, color=INK, weight="700"))

    el.append(card(38, 108, 348, 254, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Sub-view 1: Extended arms (cx=120, cy=236, arm r=64)
    el.append(txt(120, 132, "① 双臂平展（初态）", size=11.4, color=BLUE, anchor="middle", weight="700"))
    el.append(f'<circle cx="120" cy="236" r="64" fill="none" stroke="{BLUE_LINE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    el.append(
        f'<g class="spin-wide">'
        f'<line x1="56" y1="236" x2="184" y2="236" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>'
        f'<circle cx="56" cy="236" r="6.5" fill="{BLUE}"/>'
        f'<circle cx="184" cy="236" r="6.5" fill="{BLUE}"/>'
        f'<circle cx="120" cy="236" r="16" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>'
        f'</g>'
    )
    el.append(txt(120, 240, "躯干", size=9.8, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(120, 322, "转动惯量 = I₀", size=10.8, color=INK, anchor="middle", weight="600"))
    el.append(pill(62, 330, "转速 ω₀ = 1.5 转/秒", fg=BLUE, bg=BLUE_SOFT, w=116, h=22, size=10.4))

    # Arrow between states
    el.append(f'<line x1="196" y1="236" x2="228" y2="236" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>')
    el.append(txt(212, 222, "收臂", size=10.2, color=ORANGE, anchor="middle", weight="700"))

    # Sub-view 2: Tucked arms (cx=298, cy=236, arm r=32 -> half radius!)
    el.append(txt(298, 132, "② 双臂抱胸（终态）", size=11.4, color=ORANGE, anchor="middle", weight="700"))
    el.append(f'<circle cx="298" cy="236" r="32" fill="none" stroke="#fdba74" stroke-width="1.4" stroke-dasharray="4 3"/>')
    el.append(
        f'<g class="spin-tuck">'
        f'<line x1="266" y1="236" x2="330" y2="236" stroke="{ORANGE}" stroke-width="4.5" stroke-linecap="round"/>'
        f'<circle cx="266" cy="236" r="6.5" fill="{ORANGE}"/>'
        f'<circle cx="330" cy="236" r="6.5" fill="{ORANGE}"/>'
        f'<circle cx="298" cy="236" r="16" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2"/>'
        f'</g>'
    )
    el.append(txt(298, 240, "躯干", size=9.8, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(298, 322, "转动惯量 I₁ = I₀ / 4", size=10.8, color=INK, anchor="middle", weight="600"))
    el.append(pill(238, 330, "转速 4ω₀ = 6.0 转/秒！", fg=ORANGE, bg=ORANGE_SOFT, w=120, h=22, size=10.4))

    # Bottom conservation summary inside Left Panel
    el.append(card(38, 374, 348, 112, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(52, 397, "为什么体操空翻、跳水十米台全都拼命“抱膝团身”？", size=11.4, color=GREEN, weight="700"))
    el.append(txt(52, 419, "• 腾空后重力精准穿过人体质心，外力矩 τ ≡ 0；", size=10.8, color=BODY))
    el.append(txt(52, 439, "• 把长条形身体（L_长）团成球（L_长/2），转动惯量立减", size=10.8, color=BODY))
    el.append(txt(52, 459, "  为 1/4，0.5 秒下落就能在空中干净利落翻完两整周！", size=10.8, color=INK, weight="700"))
    el.append(txt(52, 478, "  （注：上方俯视动画严格按 1:4 真实角速度比播放一次）", size=9.8, color=MUTED))

    # Right panel: The Kinetic Energy Quadrupling Paradox!
    el.append(card(414, 66, 322, 434))
    el.append(txt(432, 92, "二、烧脑盲区：暴涨 3 倍的动能从哪来？", size=12.8, color=INK, weight="700"))

    el.append(card(430, 108, 290, 166, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(446, 132, "算一笔让你吃惊的能量账：", size=11.5, color=PURPLE, weight="700"))
    el.append(txt(446, 156, "• 角动量：L₁ = (I₀/4)·(4ω₀) = I₀ω₀ （没变！）", size=10.8, color=BODY))
    el.append(txt(446, 178, "• 初态动能：Ek₀ = ½ I₀ ω₀²", size=10.8, color=BODY))
    el.append(txt(446, 200, "• 终态动能：Ek₁ = ½ (I₀/4) (4ω₀)² = 4 Ek₀ ！", size=11, color=PURPLE, weight="700"))
    el.append(pill(446, 214, "凭空多出了 300% 的旋转动能！", fg=PURPLE, bg="#ffffff", w=256, h=24, size=11))
    el.append(txt(446, 260, "既然冰面没推她，这笔巨款是谁买的单？", size=10.6, color=INK, weight="600"))

    el.append(card(430, 288, 290, 198, rx=8, fill="#fffdf9", stroke=ORANGE))
    el.append(txt(446, 312, "破案真相：径向肌肉拉力“零力矩、做正功”！", size=11.4, color=ORANGE, weight="700"))
    el.append(txt(446, 336, "① 为什么不改角动量？", size=10.8, color=INK, weight="700"))
    el.append(txt(446, 356, "   手臂往胸口拉的力 F 直指转轴（力臂=0），", size=10.6, color=BODY))
    el.append(txt(446, 375, "   力矩 τ = r × F = 0，因此 L 纹丝不动。", size=10.6, color=BODY))
    el.append(txt(446, 399, "② 为什么猛增动能？", size=10.8, color=INK, weight="700"))
    el.append(txt(446, 419, "   高速旋转中双臂拼命想往外甩，选手必须消耗", size=10.6, color=BODY))
    el.append(txt(446, 438, "   体内化学能，沿向内螺旋线硬拽双臂移动距离", size=10.6, color=BODY))
    el.append(txt(446, 457, "   Δr——肌肉做的功 100% 变成了新增转动动能！", size=10.6, color=ORANGE, weight="700"))

    svg = figure(
        518,
        "花样滑冰收臂加速4倍的角动量守恒与肌肉做功增能原理解析图",
        "左栏俯视对比花滑选手双臂平展与抱胸时转动惯量减为1/4、角速度严格增至4倍的过程；右栏解释为何角动量不变但转动动能增至4倍：向内拉手臂的径向力穿过转轴力矩为零，却克服离心趋势沿径向做正功。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "skater-spin-and-energy-paradox.svg", svg)


def _build_gyroscope_bicycle_svg():
    el = []
    el.extend(
        header(
            "歪斜的陀螺为什么“宁可横着兜圈也绝不倒地”？兼破自行车百年迷思",
            "核心密码只有一句话：角动量的改变量 ΔL 永远顺着力矩 τ 的方向走，而不是顺着力 F 的方向倒！",
        )
    )

    # Top panel: Gyroscope Precession 3D Vector Geometry
    el.append(card(24, 66, 712, 232))
    el.append(step_badge(44, 90, "1", fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(62, 95, "陀螺进动（Precession）：重力明明往下拽，为什么转轴反而往侧面水平画圈？", size=12.8, color=INK, weight="700"))

    # Left sub-diagram: Tilted spinning top & horizontal precession cone
    el.append(card(40, 108, 404, 174, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    px, py = 186, 256  # pivot tip on floor
    # Vertical Z axis
    el.append(f'<line x1="{px}" y1="{py}" x2="{px}" y2="122" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
    # Precession horizontal ellipse at top (cx=186, cy=146, rx=74, ry=20)
    el.append(f'<ellipse cx="{px}" cy="146" rx="74" ry="18" fill="none" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="5 3"/>')
    # Top axle tilted right to (246, 152)
    tx, ty = 246, 152
    el.append(f'<line x1="{px}" y1="{py}" x2="{tx + 12}" y2="{ty - 18}" stroke="{BLUE}" stroke-width="2.8" marker-end="url(#arr-blue)"/>')
    # Spinning flywheel disk perpendicular to tilted axle around midpoint (216, 204)
    el.append(
        f'<g transform="translate(216,204) rotate(30)">'
        f'<ellipse cx="0" cy="0" rx="34" ry="11" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>'
        f'</g>'
    )
    # Gravity Mg arrow straight down from (216, 204)
    el.append(f'<line x1="216" y1="204" x2="216" y2="254" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
    el.append(txt(224, 248, "重力 Mg", size=10.2, color=ORANGE, weight="700"))
    # Torque / dL sideways tangent arrow at tip of L!
    el.append(f'<line x1="{tx + 8}" y1="{ty - 12}" x2="{tx - 32}" y2="{ty - 24}" stroke="{GREEN}" stroke-width="2.4" marker-end="url(#arr-green)"/>')
    el.append(txt(tx + 22, ty + 8, "自转角动量 L", size=10.6, color=BLUE, weight="700"))
    el.append(txt(196, 124, "ΔL = τΔt 垂直于 L → 推着轴尖水平绕圈！", size=10.5, color=GREEN, anchor="middle", weight="700", halo=True))
    el.append(txt(102, 182, "若不转(L=0)", size=10.2, color=MUTED, anchor="middle"))
    el.append(txt(102, 198, "直接砸倒！", size=10.2, color=ORANGE, anchor="middle", weight="700"))

    # Right sub-card: Precession rate formula
    el.append(card(458, 108, 262, 174, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(474, 132, "进动快慢公式：Ω_P = r M g / (I ω)", size=11.5, color=BLUE, weight="700"))
    el.append(txt(474, 156, "• 重力力矩 τ = r × Mg 始终处于水平面，", size=10.6, color=BODY))
    el.append(txt(474, 176, "  与倾斜的 L 永远成 90° 正交；", size=10.6, color=BODY))
    el.append(txt(474, 198, "• 反直觉推论：陀螺自转 ω 越快，分母越", size=10.6, color=INK, weight="700"))
    el.append(txt(474, 218, "  大，水平兜圈进动 Ω_P 反而越慢越稳！", size=10.6, color=INK, weight="700"))
    el.append(txt(474, 242, "• 地球本身也是大陀螺：太阳与月球拉扯赤", size=10.4, color=MUTED))
    el.append(txt(474, 260, "  道隆起，使地轴每 2.58 万年进动一圈！", size=10.4, color=MUTED))

    # Bottom panel: Busting the 100-year Bicycle Stability Myth (Science 2011)
    el.append(card(24, 312, 712, 204))
    el.append(step_badge(44, 336, "2", fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(62, 341, "科学辟谣：自行车骑起来不倒，真的“全靠车轮角动量”吗？（2011《Science》实测）", size=12.6, color=INK, weight="700"))

    el.append(card(40, 356, 332, 144, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(56, 380, "普通自行车上：陀螺进动确实在“帮忙打把”", size=11.4, color=GREEN, weight="700"))
    el.append(txt(56, 404, "• 当车身不慎向左倾斜时，重力对前轮施加力矩；", size=10.6, color=BODY))
    el.append(txt(56, 424, "• 前轮向前的自转角动量发生进动，恰好自动把车", size=10.6, color=BODY))
    el.append(txt(56, 444, "  把向左拧（“往要倒的一侧转向”）！", size=10.6, color=INK, weight="700"))
    el.append(txt(56, 466, "• 车轮随之滚回人体重心正下方，帮你化险为夷。", size=10.6, color=BODY))

    el.append(card(388, 356, 332, 144, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(404, 380, "2011 康奈尔/代尔夫特反例车：L = 0 照样不倒！", size=11.4, color=ORANGE, weight="700"))
    el.append(txt(404, 404, "• 鲁伊纳团队给前后轮各配一个反向对转副轮，把", size=10.6, color=BODY))
    el.append(txt(404, 424, "  车轮净角动量 100% 归零（且取消脚轮正拖距）！", size=10.6, color=INK, weight="700"))
    el.append(txt(404, 446, "• 无人小车推出去后依然能自动扶正稳行！证明：", size=10.6, color=BODY))
    el.append(txt(404, 466, "  前叉重心分布引起的“向倾倒侧自动转向”同样关键，", size=10.6, color=BODY))
    el.append(txt(404, 485, "  角动量是得力助手，但绝非唯一救命恩人！", size=10.6, color=ORANGE, weight="700"))

    svg = figure(
        534,
        "陀螺进动三维矢量正交原理与2011年Science无陀螺自稳定自行车实验解析图",
        "上图展示高速旋转陀螺受水平重力力矩τ作用时ΔL垂直于L从而绕竖直轴水平进动（Ω_P=rMg/Iω）；下图区分普通自行车前轮进动辅助向倾倒侧转向的机制与2011年康奈尔团队对转轮零角动量自行车仍能自稳定的反例。",
        el,
    )
    write_svg(SUBDIR, "gyroscope-precession-and-bicycle-truth.svg", svg)


def _build_helicopter_antitorque_svg():
    el = []
    el.extend(
        header(
            "断了尾桨的直升机为什么秒变“空中旋转木马”？三种角动量清零工程方案",
            "悬空机身没有地面撑脚：发动机让头顶旋翼逆时针转（+L），机身就必定顺时针反着转（-L）！",
        )
    )

    configs = [
        (
            24,
            "1",
            "单旋翼 ＋ 抗扭尾桨",
            "经典构型（阿帕奇 / 直-20）",
            BLUE,
            BLUE_SOFT,
            "• 头顶主旋翼逆时针狂转（+L_主），对机",
            "  身施加顺时针反扭矩；",
            "• 机尾长梁末端竖装高速小尾桨，向侧方",
            "  推气产生反向力矩死死顶住机身！",
            "代价：尾桨要白白吃掉约 8%–10% 动力，",
            "一旦尾桨受损机身立刻失控原地打转。",
        ),
        (
            266,
            "2",
            "纵列双旋翼反向对转",
            "重载运输机（CH-47 支奴干）",
            GREEN,
            GREEN_SOFT,
            "• 机头机尾各装一副等大主旋翼，通过同",
            "  步传动轴严格一正一反等速旋转；",
            "• 角动量天生互相抵消：(+L) + (-L) = 0，",
            "  机身净反扭矩直接归零！",
            "优势：省掉尾桨功率损耗，100% 发动机",
            "马力全用来吊运几十吨重装备！",
        ),
        (
            508,
            "3",
            "共轴上下双旋翼对转",
            "NASA“机智号”火星直升机",
            ORANGE,
            ORANGE_SOFT,
            "• 上下两副 1.2 米碳纤维旋翼套在同一根",
            "  立轴上，以约 2,400 RPM 正反对转；",
            "• 无需长尾梁和尾桨，结构极致紧凑且",
            "  上下角动量当场清零！",
            "战绩：在仅地球 1% 大气密度的火星荒原",
            "稳稳完成 72 次飞行，开创人类历史！",
        ),
    ]

    for cx0, badge_n, title_s, sub_s, col, bg_col, b1, b2, b3, b4, f1, f2 in configs:
        el.append(card(cx0, 66, 228, 422))
        el.append(step_badge(cx0 + 22, 92, badge_n, fg=col, bg=bg_col))
        el.append(txt(cx0 + 40, 97, title_s, size=12.4, color=INK, weight="700"))
        el.append(txt(cx0 + 22, 118, sub_s, size=10.4, color=col, weight="600"))

        # Top-down / schematic rotor diagram box
        el.append(card(cx0 + 16, 132, 196, 138, rx=8, fill="#f8fafc", stroke=HAIRLINE))
        midx = cx0 + 114
        if badge_n == "1":
            # Fuselage + tail boom + main rotor + tail rotor thrust
            el.append(f'<rect x="{midx - 28}" y="176" width="44" height="22" rx="10" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
            el.append(f'<line x1="{midx + 16}" y1="187" x2="{midx + 68}" y2="187" stroke="{BLUE}" stroke-width="3"/>')
            el.append(f'<circle cx="{midx - 6}" cy="187" r="42" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 3"/>')
            el.append(txt(midx - 6, 145, "主旋翼 +L（逆时针）", size=9.8, color=BLUE, anchor="middle", weight="700"))
            # Tail rotor pushing up on diagram to create CCW counter-torque!
            el.append(f'<line x1="{midx + 68}" y1="175" x2="{midx + 68}" y2="199" stroke="{ORANGE}" stroke-width="3"/>')
            el.append(f'<line x1="{midx + 68}" y1="224" x2="{midx + 68}" y2="202" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
            el.append(txt(midx + 42, 248, "尾桨侧推力矩抵消反转", size=9.8, color=ORANGE, anchor="middle", weight="700"))
        elif badge_n == "2":
            # Tandem fuselage + two overlapping opposite-spin rotor circles
            el.append(f'<rect x="{midx - 54}" y="184" width="108" height="24" rx="10" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
            el.append(f'<circle cx="{midx - 36}" cy="196" r="36" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 3"/>')
            el.append(f'<circle cx="{midx + 36}" cy="196" r="36" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="5 3"/>')
            el.append(txt(midx - 42, 152, "前桨 +L", size=10, color=BLUE, anchor="middle", weight="700"))
            el.append(txt(midx + 42, 152, "后桨 -L", size=10, color=ORANGE, anchor="middle", weight="700"))
            el.append(txt(midx, 252, "L_总 = (+L) + (-L) = 0", size=10.2, color=GREEN, anchor="middle", weight="700"))
        else:
            # Side-view coaxial Mars Ingenuity: cube body + four legs + upper/lower counter-spinning blades
            el.append(f'<rect x="{midx - 18}" y="204" width="36" height="28" rx="4" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
            el.append(f'<line x1="{midx}" y1="154" x2="{midx}" y2="204" stroke="{SLATE}" stroke-width="2.4"/>')
            # Solar panel on top
            el.append(f'<rect x="{midx - 24}" y="148" width="48" height="6" rx="2" fill="{SLATE}"/>')
            # Upper rotor (+L) & Lower rotor (-L)
            el.append(f'<ellipse cx="{midx}" cy="168" rx="68" ry="8" fill="none" stroke="{BLUE}" stroke-width="1.8"/>')
            el.append(f'<ellipse cx="{midx}" cy="186" rx="68" ry="8" fill="none" stroke="{ORANGE}" stroke-width="1.8"/>')
            # Landing legs
            el.append(f'<line x1="{midx - 16}" y1="232" x2="{midx - 42}" y2="256" stroke="{SLATE}" stroke-width="1.6"/>')
            el.append(f'<line x1="{midx + 16}" y1="232" x2="{midx + 42}" y2="256" stroke="{SLATE}" stroke-width="1.6"/>')
            el.append(txt(midx, 254, "上桨 +L / 下桨 -L 对消", size=10, color=ORANGE, anchor="middle", weight="700", halo=True))

        el.append(txt(cx0 + 18, 294, b1, size=10.5, color=BODY))
        el.append(txt(cx0 + 18, 314, b2, size=10.5, color=BODY))
        el.append(txt(cx0 + 18, 338, b3, size=10.5, color=BODY))
        el.append(txt(cx0 + 18, 358, b4, size=10.5, color=INK, weight="700"))

        el.append(card(cx0 + 16, 378, 196, 94, rx=7, fill=bg_col, stroke=col))
        el.append(txt(cx0 + 26, 404, f1, size=10.2, color=BODY))
        el.append(txt(cx0 + 26, 424, f2, size=10.2, color=col, weight="700"))
        el.append(txt(cx0 + 26, 452, "本质：向外部借力矩 vs 内部抵消", size=9.8, color=MUTED))

    svg = figure(
        506,
        "直升机反扭矩现象与尾桨、纵列双桨及机智号共轴反转双桨三种角动量平衡方案图",
        "三栏并列对比单旋翼配侧推尾桨施加外力矩、支奴干纵列双旋翼正反转抵消角动量、以及NASA机智号火星直升机共轴双旋翼2400转每分对转实现零净角动量的工程设计。",
        el,
    )
    write_svg(SUBDIR, "helicopter-antitorque-and-mars-ingenuity.svg", svg)


def _build_falling_cat_hubble_svg():
    el = []
    el.extend(
        header(
            "悬空零借力怎么翻身？从“落猫四步扭腰术”到哈勃望远镜的无燃料调头",
            "总角动量 L ≡ 0 并不禁止转身！只要不是死板的刚体，靠内部“变惯量／转飞轮”就能凭空换朝向",
        )
    )

    # Top panel: Falling Cat 4-step tuck-and-twist (Marey 1894 & NASA/Kane 1969)
    el.append(card(24, 66, 712, 238))
    el.append(step_badge(44, 90, "1", fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(62, 95, "“落猫问题”（NASA 曾专门立项研究教宇航员太空转身）：全程 L = 0 怎样翻过 180°？", size=12.6, color=INK, weight="700"))

    cat_steps = [
        (40, "① 四脚朝天松手", "初态 L_总 = 0", "前后半身均未转", "脊柱柔韧弯曲预备", SLATE, SLATE_SOFT),
        (212, "② 前爪抱胸+后腿伸直", "I_前 小，I_后 = 3I_前", "前半身顺转 +120°！", "后半身仅逆退 -40°", BLUE, BLUE_SOFT),
        (384, "③ 前爪张开+后腿蜷缩", "互换：I_前 = 3I_后", "后半身顺追 +120°！", "前半身仅微退 -40°", ORANGE, ORANGE_SOFT),
        (556, "④ 重复配合稳稳落地", "每瞬时 L_前+L_后 ≡ 0", "一轮净赚 +80° 姿态", "约 0.3 秒四脚着地！", GREEN, GREEN_SOFT),
    ]
    for sx, stitle, s1, s2, s3, scol, sbg in cat_steps:
        el.append(card(sx, 110, 164, 178, rx=8, fill=sbg, stroke=scol))
        el.append(txt(sx + 82, 132, stitle, size=10.8, color=scol, anchor="middle", weight="700"))
        # Two-cylinder cat icon in middle (y=144..202)
        cxm = sx + 82
        if sx == 40:
            el.append(f'<rect x="{cxm - 44}" y="160" width="38" height="22" rx="6" fill="#ffffff" stroke="{scol}" stroke-width="1.6"/>')
            el.append(f'<rect x="{cxm + 6}" y="160" width="38" height="22" rx="6" fill="#ffffff" stroke="{scol}" stroke-width="1.6"/>')
            el.append(txt(cxm, 198, "背朝下 / 爪朝天", size=9.8, color=MUTED, anchor="middle"))
        elif sx == 212:
            # Front small radius (tucked), Rear tall radius (extended legs)
            el.append(f'<rect x="{cxm - 44}" y="164" width="38" height="16" rx="5" fill="#ffffff" stroke="{BLUE}" stroke-width="2"/>')
            el.append(f'<rect x="{cxm + 6}" y="148" width="38" height="44" rx="6" fill="#ffffff" stroke="{SLATE}" stroke-width="1.6"/>')
            el.append(txt(cxm - 25, 198, "小I快转", size=9.6, color=BLUE, anchor="middle", weight="700"))
            el.append(txt(cxm + 25, 204, "大I慢退", size=9.6, color=SLATE, anchor="middle"))
        elif sx == 384:
            # Front tall radius (extended), Rear small radius (tucked)
            el.append(f'<rect x="{cxm - 44}" y="148" width="38" height="44" rx="6" fill="#ffffff" stroke="{SLATE}" stroke-width="1.6"/>')
            el.append(f'<rect x="{cxm + 6}" y="164" width="38" height="16" rx="5" fill="#ffffff" stroke="{ORANGE}" stroke-width="2"/>')
            el.append(txt(cxm - 25, 204, "大I稳住", size=9.6, color=SLATE, anchor="middle"))
            el.append(txt(cxm + 25, 198, "小I补齐", size=9.6, color=ORANGE, anchor="middle", weight="700"))
        else:
            el.append(f'<rect x="{cxm - 44}" y="156" width="38" height="22" rx="6" fill="#ffffff" stroke="{GREEN}" stroke-width="2"/>')
            el.append(f'<rect x="{cxm + 6}" y="156" width="38" height="22" rx="6" fill="#ffffff" stroke="{GREEN}" stroke-width="2"/>')
            el.append(txt(cxm, 198, "四脚稳稳朝下！", size=9.8, color=GREEN, anchor="middle", weight="700"))

        el.append(txt(sx + 82, 226, s1, size=10.2, color=INK, anchor="middle", weight="600"))
        el.append(txt(sx + 82, 246, s2, size=10.2, color=scol, anchor="middle", weight="700"))
        el.append(txt(sx + 82, 266, s3, size=10, color=BODY, anchor="middle"))

    # Bottom panel: Hubble Space Telescope Reaction Wheels
    el.append(card(24, 318, 712, 202))
    el.append(step_badge(44, 342, "2", fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(62, 347, "哈勃与韦伯太空望远镜：不烧一滴火箭燃料，靠肚子里的小飞轮在太空精准调头！", size=12.6, color=INK, weight="700"))

    # Left cutaway schematic of Hubble + internal reaction wheel
    el.append(card(40, 362, 376, 142, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Solar panels
    el.append(f'<rect x="132" y="374" width="12" height="118" rx="2" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.4"/>')
    el.append(f'<rect x="276" y="374" width="12" height="118" rx="2" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.4"/>')
    # Hubble main tube
    el.append(f'<rect x="108" y="406" width="204" height="54" rx="8" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>')
    # Internal reaction wheel spinning clockwise
    el.append(f'<circle cx="210" cy="433" r="19" fill="#ffffff" stroke="{PURPLE}" stroke-width="2.2"/>')
    el.append(txt(210, 437, "飞轮", size=10, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(210, 396, "内部 45kg 飞轮顺时针转（+I_轮 ω_轮）", size=10.2, color=PURPLE, anchor="middle", weight="700", halo=True))
    el.append(txt(210, 482, "11 吨镜筒必逆时针缓转（-I_镜 ω_镜），总 L ≡ 0！", size=10.4, color=BLUE, anchor="middle", weight="700", halo=True))

    # Right engineering facts card (NASA verified specs!)
    el.append(card(430, 362, 290, 142, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(446, 385, "NASA 哈勃指向控制系统硬核参数：", size=11.4, color=BLUE, weight="700"))
    el.append(txt(446, 408, "• 禁用喷气推力器：防止尾气污染光学镜面！", size=10.5, color=BODY))
    el.append(txt(446, 428, "• 4 台直径约 0.6m 飞轮，全靠太阳能供电调速；", size=10.5, color=BODY))
    el.append(txt(446, 448, "• 锁定精度 0.007 角秒（相当于从北京拿激光稳", size=10.5, color=INK, weight="700"))
    el.append(txt(446, 468, "  稳照住 320 km 外一枚硬币上的人像 24 小时）！", size=10.5, color=INK, weight="700"))
    el.append(txt(446, 488, "• 另配 2.4m 磁力矩棒借地磁场给飞轮“卸转速”。", size=10.2, color=MUTED))

    svg = figure(
        538,
        "落猫问题四步变惯量零角动量翻身原理与哈勃太空望远镜反作用飞轮调头示意图",
        "上图分四步展示猫咪下落时先缩前爪伸后腿扭腰、再伸前爪缩后腿回扭，在总角动量恒为零的前提下净翻转身体；下图展示11吨哈勃望远镜利用内部45千克反作用飞轮反向旋转实现无推进剂0.007角秒级高精度调头。",
        el,
    )
    write_svg(SUBDIR, "falling-cat-and-hubble-reaction-wheel.svg", svg)


def _build_cosmic_quantum_svg():
    el = []
    el.extend(
        header(
            "横跨 60 个数量级的宇宙铁律：从月球每年逃离 3.8 厘米，到最小量子硬币 ℏ",
            "埃米·诺特证明：只要宇宙空间“转个方向物理规律不变”，角动量就注定从星系到夸克永恒守恒！",
        )
    )

    # Left panel: Earth-Moon angular momentum transfer
    el.append(card(24, 66, 356, 428))
    el.append(txt(42, 92, "一、地月大账本：地球刹车，月球为什么往外跑？", size=12.6, color=INK, weight="700"))

    el.append(card(40, 108, 324, 178, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Earth with tidal bulge on left (cx=110, cy=198, r=28)
    el.append(f'<ellipse cx="110" cy="198" rx="34" ry="26" transform="rotate(-18 110 198)" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(f'<circle cx="110" cy="198" r="22" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.8"/>')
    el.append(txt(110, 202, "地球", size=10.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(110, 246, "潮汐摩擦给自转刹车", size=10.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(110, 264, "每百年一天变长 ~1.7 ms", size=10, color=MUTED, anchor="middle"))

    # Transfer arrow to Moon on right (cx=288, cy=178)
    el.append(f'<path d="M150,184 Q216,148 266,172" fill="none" stroke="{GREEN}" stroke-width="2.2" marker-end="url(#arr-green)"/>')
    el.append(txt(212, 148, "角动量转移 ΔL", size=10.5, color=GREEN, anchor="middle", weight="700"))

    el.append(f'<circle cx="288" cy="182" r="13" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.8"/>')
    el.append(txt(288, 186, "月", size=10, color=SLATE, anchor="middle", weight="700"))
    el.append(f'<line x1="304" y1="182" x2="346" y2="182" stroke="{GREEN}" stroke-width="2" marker-end="url(#arr-green)"/>')
    el.append(txt(292, 220, "外推 +3.8 cm/年！", size=10.8, color=GREEN, anchor="middle", weight="700"))

    el.append(card(40, 298, 324, 180, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(54, 322, "为什么月球拿到角动量反而“越飞越远”？", size=11.4, color=GREEN, weight="700"))
    el.append(txt(54, 346, "• 地月系统总和守恒：L_地球自转 + L_月球公转 = 常数；", size=10.6, color=BODY))
    el.append(txt(54, 368, "• 由万有引力提供向心力（v = √(GM/r)），月球轨道", size=10.6, color=BODY))
    el.append(txt(54, 388, "  角动量为：L_月 = m_月 r v = m_月 √(G M_地 r) ∝ √r ！", size=10.8, color=INK, weight="700"))
    el.append(txt(54, 412, "• 轨道半径 r 越大，公转角动量反而越大！因此地球丢", size=10.6, color=BODY))
    el.append(txt(54, 432, "  掉的自转角动量，全变成了把月球往高轨道推的动力", size=10.6, color=BODY))
    el.append(txt(54, 452, "  （已被阿波罗登月激光测距毫米级实测证实）！", size=10.6, color=GREEN, weight="700"))

    # Right panel: Noether's theorem & Quantum Planck constant hbar
    el.append(card(394, 66, 342, 428))
    el.append(txt(412, 92, "二、终极揭秘：诺特定理与普朗克常数 ℏ", size=12.6, color=INK, weight="700"))

    el.append(card(410, 108, 310, 144, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(426, 132, "① 为什么角动量绝对守恒？（诺特定理，1918）", size=11.3, color=BLUE, weight="700"))
    el.append(txt(426, 156, "• 数学家埃米·诺特证明：每一条物理守恒律背后，", size=10.6, color=BODY))
    el.append(txt(426, 176, "  都对应着宇宙的一种对称性：", size=10.6, color=BODY))
    el.append(txt(426, 198, "  时间平移不变 → 能量守恒；空间平移 → 动量守恒；", size=10.4, color=SLATE, weight="600"))
    el.append(txt(426, 220, "  空间各向同性（旋转对称） → 角动量守恒！", size=10.8, color=BLUE, weight="700"))
    el.append(txt(426, 240, "  因为宇宙空间没有“偏心的方向”，L 才永不凭空生灭。", size=10.2, color=MUTED))

    el.append(card(410, 266, 310, 212, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(426, 290, "② 微观彩蛋：普朗克常数 ℏ 就是“角动量最小硬币”！", size=11.1, color=PURPLE, weight="700"))
    el.append(txt(426, 314, "• 拆开约化普朗克常数 ℏ = h/(2π) 的国际单位看看：", size=10.6, color=BODY))
    el.append(pill(426, 326, "1 J·s = 1 (N·m)·s = 1 kg·m²/s ≡ 角动量单位！", fg=PURPLE, bg="#ffffff", w=278, h=24, size=10.4))
    el.append(txt(426, 370, "• 在原子尺度，角动量不能连续变化，只能按", size=10.6, color=BODY))
    el.append(txt(426, 390, "  ℏ ≈ 1.055 × 10⁻³⁴ J·s 一份份整数／半整数跳变！", size=10.6, color=INK, weight="700"))
    el.append(txt(426, 414, "• 医院核磁共振（MRI）怎么拍清大脑与内脏？", size=10.6, color=PURPLE, weight="700"))
    el.append(txt(426, 434, "  正是用强磁场让体内水分子氢原子核的自旋角动量", size=10.5, color=BODY))
    el.append(txt(426, 454, "  （½ℏ）像小陀螺一样发生“拉莫尔进动”来成像的！", size=10.5, color=INK, weight="600"))

    svg = figure(
        512,
        "地月潮汐角动量转移推远月球、诺特空间旋转对称性与量子普朗克常数角动量本质图",
        "左栏展示地球潮汐减速将自转角动量转移给月球公转（L∝√r）使月球每年远离地球3.8厘米；右栏阐述1918年诺特定理揭示空间旋转对称性决定角动量守恒，并指出约化普朗克常数ℏ本身就是微观角动量的最小量子单位及MRI进动成像基础。",
        el,
    )
    write_svg(SUBDIR, "earth-moon-recession-and-quantum-hbar.svg", svg)


@register("angular-momentum", "Angular momentum principles, paradoxes, engineering applications, and quantum hbar", "science")
def build_angular_momentum():
    _verify_angular_momentum_math()
    _build_vector_and_inertia_svg()
    _build_skater_spin_svg()
    _build_gyroscope_bicycle_svg()
    _build_helicopter_antitorque_svg()
    _build_falling_cat_hubble_svg()
    _build_cosmic_quantum_svg()
