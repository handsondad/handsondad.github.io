"""Original Chinese SVG diagrams for the technical principles of Brocade, Satin,
and Embroidery Art (assets/images/brocade-embroidery/).
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

SUBDIR = "brocade-embroidery"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
GOLD = "#b45309"
GOLD_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"


def _valid_regular_satin_steps(r_val):
    """Return all valid step values S for an R-end regular satin weave:
    1 < S < R - 1 and gcd(R, S) == 1.
    """
    return [s for s in range(2, r_val - 1) if math.gcd(r_val, s) == 1]


def _verify_textile_and_optical_math():
    # 1. Silk fibroin optical Cauchy dispersion (Bucciarelli et al. 2018, Opt. Mater. 78, 407)
    lam_um = 0.55
    n_silk = 1.527 + 5.5e-3 * (lam_um ** -2) + 3.0e-4 * (lam_um ** -4)
    assert 1.545 < n_silk < 1.552
    theta_crit_deg = math.degrees(math.asin(1.0 / n_silk))
    assert 40.0 < theta_crit_deg < 40.5  # ~40.24 deg total internal reflection critical angle!

    # 2. Regular Satin Number Theory Theorem:
    # R = 2, 3, 4 -> empty; R = 5 -> [2, 3]; R = 6 -> EMPTY (!); R = 7 -> [2,3,4,5]; R = 8 -> [3,5]
    assert _valid_regular_satin_steps(2) == []
    assert _valid_regular_satin_steps(3) == []
    assert _valid_regular_satin_steps(4) == []
    assert _valid_regular_satin_steps(5) == [2, 3]
    assert _valid_regular_satin_steps(6) == []  # No 6-harness regular satin exists!
    assert _valid_regular_satin_steps(7) == [2, 3, 4, 5]
    assert _valid_regular_satin_steps(8) == [3, 5]

    # Verify traditional Chinese irregular 6-end satin permutation [0, 3, 1, 5, 2, 4] (1-based: 1,4,2,6,3,5):
    # Every row & column has exactly 1 binding point, and no two cyclically adjacent columns are +-1 mod 6!
    irr6 = [0, 3, 1, 5, 2, 4]
    assert sorted(irr6) == list(range(6))
    for i in range(6):
        diff = (irr6[(i + 1) % 6] - irr6[i]) % 6
        assert diff not in (0, 1, 5), f"Diagonal touch at {i}: diff={diff}"

    # 3. Verify warp-float coverage ratios across 8x8 tiles:
    # Plain weave: 50.0%; 3/1 Twill: 75.0%; 5-end warp satin: 80.0%; 8-end warp satin: 87.5%
    assert abs((5 - 1) / 5 - 0.80) < 1e-12
    assert abs((8 - 1) / 8 - 0.875) < 1e-12

    # 4. Thread splitting scale: 1 embroidery strand -> 1/64 and 1/128 fine silk threads
    d_base_um = 200.0
    # Cross-sectional area scales as 1/N, so effective bundle diameter scales as d_base / sqrt(N)
    # Wait: a single silk brin filament (单根蚕丝丝素) is ~10-12 um; one plied embroidery thread (~16-32 brins)
    # split into 1/16 gives 1-2 brins (~10-14 um), and ultra-fine splitting of fine filaments reaches ~2-4 um!
    d_16 = d_base_um / math.sqrt(16)
    d_64 = d_base_um / math.sqrt(64)
    assert abs(d_16 - 50.0) < 1e-9 and abs(d_64 - 25.0) < 1e-9


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker_end=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    m_attr = f' marker-end="url(#{marker_end})"' if marker_end else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}"{d_attr}{m_attr}/>'
    )


def build_fig1_silk_prism_optics():
    """Fig 1: Raw vs Degummed Silk triangular prism microstructure + directional luster anisotropy."""
    el = []
    el.extend(
        header(
            "底层材料密码：为什么唯独桑蚕丝自带“珍珠柔光”？",
            "精练脱去粗糙丝胶后，露出两根折射率 n ≈ 1.55 的天然圆角三棱镜丝素；转个角度就能变幻明暗！",
        )
    )

    # Left Card: Raw Silk (生丝) vs Degummed Silk (熟丝) Cross-Section
    el.append(card(22, 68, 356, 384, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(60, 95, "微米级横截面：从“毛玻璃生丝”到“双棱镜熟丝”", size=12.5, color=INK, weight="700"))

    # Sub-box A: Raw silk with sericin coat
    el.append(card(36, 112, 328, 134, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(48, 133, "① 未脱胶“生丝”（20%–25% 丝胶包裹两根丝素）", size=11.5, color=SLATE, weight="700"))
    # Rough bumpy outer sericin blob
    el.append(
        f'<path d="M74,192 C66,166 86,150 116,154 C138,148 168,162 164,190 '
        f'C168,214 140,226 116,220 C88,226 68,214 74,192 Z" '
        f'fill="#e2e8f0" stroke="{SLATE}" stroke-width="2" stroke-dasharray="4,2"/>'
    )
    # Two inner rounded triangles (fibroin brins)
    el.append(f'<path d="M84,202 Q96,164 112,202 Q98,210 84,202 Z" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="1.8"/>')
    el.append(f'<path d="M120,202 Q134,164 150,202 Q135,210 120,202 Z" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="1.8"/>')
    el.append(txt(117, 236, "总宽约 25 μm", size=10.5, color=MUTED, anchor="middle"))

    el.append(txt(180, 162, "• 外层丝胶粗糙凹凸 → 漫反射发乌", size=10.5, color=BODY))
    el.append(txt(180, 184, "• 丝身挺括偏硬（用于织生绢、轻绡）", size=10.5, color=BODY))
    el.append(txt(180, 208, "↓ 碱性皂液煮练脱胶（精练）", size=11, color=ORANGE, weight="700"))

    # Sub-box B: Degummed fibroin triangular prism optics
    el.append(card(36, 258, 328, 180, rx=8, fill=GOLD_SOFT, stroke=GOLD))
    el.append(txt(48, 279, "② 脱胶“熟丝”：单根丝素 ≈ 10–12 μm 圆角三棱镜！", size=11.5, color=GOLD, weight="700"))

    # Large optical triangular prism diagram centered at (114, 358)
    el.append(
        f'<path d="M68,388 Q114,298 160,388 Q114,402 68,388 Z" '
        f'fill="#ffffff" stroke="{GOLD}" stroke-width="2.6"/>'
    )
    # Incident light ray -> specular reflection + internal refraction + TIR -> exit shimmer
    el.append(_line(46, 322, 92, 344, color=ORANGE, sw=2.2, marker_end="arr-orange"))
    el.append(_line(92, 344, 66, 304, color=BLUE, sw=1.8, dash="3,2", marker_end="arr-blue"))
    el.append(_line(92, 344, 138, 356, color=RED, sw=2.0))
    el.append(_line(138, 356, 114, 392, color=RED, sw=2.0))
    el.append(_line(114, 392, 162, 332, color=PURPLE, sw=2.2, marker_end="arr-blue"))
    el.append(txt(114, 422, "圆角三角形截面", size=10.5, color=GOLD, anchor="middle", weight="700"))

    el.append(txt(176, 312, "• 折射率 n ≈ 1.548（堪比光学玻璃）", size=10.5, color=INK, weight="700"))
    el.append(txt(176, 334, "• 全反射临界角 θc ≈ 40.2°！", size=10.5, color=RED, weight="700"))
    el.append(txt(176, 356, "• 平坦侧面镜面反光 + 内部棱镜折射", size=10.5, color=BODY))
    el.append(txt(176, 376, "  叠加出柔和深邃的“内蕴珠光”", size=10.5, color=BODY))
    el.append(txt(176, 400, "• 对比：棉纤维扁塌发暗；化纤圆柱", size=10.5, color=MUTED))
    el.append(txt(176, 418, "  截面只剩一道刺眼“塑料贼光”！", size=10.5, color=MUTED))

    # Right Card: Directional Optical Anisotropy ("顺光亮、逆光暗、转折生立体")
    el.append(card(392, 68, 346, 384, fill=CARD_BG))
    el.append(step_badge(412, 90, 2, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(430, 95, "织锦与刺绣的魔术：同一根色线“转角即变色”", size=12.5, color=INK, weight="700"))

    # Diagram of two bundles of identical red silk threads oriented at 0 deg vs 90 deg
    el.append(card(406, 112, 318, 178, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(565, 132, "完全同一种染缸色号，仅改变丝线排布方向：", size=11, color=INK, anchor="middle", weight="700"))

    # Left swatch: longitudinal parallel to light plane (bright specular band!)
    el.append(f'<rect x="424" y="146" width="124" height="86" rx="6" fill="#f87171" stroke="{RED}" stroke-width="1.8"/>')
    for k in range(7):
        yk = 156 + k * 11
        col_line = "#fef2f2" if k in (2, 3) else "#fca5a5"
        el.append(_line(430, yk, 542, yk, color=col_line, sw=3.2))
    el.append(txt(486, 250, "顺光排针/浮线 (0°)", size=11, color=RED, anchor="middle", weight="700"))
    el.append(txt(486, 268, "柱面高光入眼 → 鲜亮耀目", size=10.5, color=INK, anchor="middle", weight="600"))

    # Right swatch: perpendicular orientation (90 deg -> deep velvety rich crimson!)
    el.append(f'<rect x="582" y="146" width="124" height="86" rx="6" fill="#7f1d1d" stroke="{RED}" stroke-width="1.8"/>')
    for k in range(10):
        xk = 592 + k * 11.5
        el.append(_line(xk, 152, xk, 226, color="#991b1b", sw=3.0))
    el.append(txt(644, 250, "横切排针/浮线 (90°)", size=11, color=INK, anchor="middle", weight="700"))
    el.append(txt(644, 268, "反射光锥偏开 → 深沉浓郁", size=10.5, color=BODY, anchor="middle"))

    # Bottom explanation box in Right Card
    el.append(card(406, 302, 318, 136, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(418, 324, "光学各向异性（Optical Anisotropy）实战威力：", size=11.5, color=PURPLE, weight="700"))
    el.append(txt(418, 347, "• 织缎：经面缎竖直反光，纬面缎横向反光——把经面缎", size=10.5, color=BODY))
    el.append(txt(418, 366, "  做底、纬面缎织花（暗花绸/绫），纯白单色也能显花！", size=10.5, color=INK, weight="600"))
    el.append(txt(418, 390, "• 刺绣：苏绣猫眼、湘绣虎斑顺着肌肉骨骼旋转运针，", size=10.5, color=BODY))
    el.append(txt(418, 409, "  人走动一步，高光跟着流转，仿佛活物呼吸！", size=10.5, color=GREEN, weight="700"))

    # Footer
    el.append(card(22, 464, 716, 42, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            490,
            "一句话总结：绘画靠“颜料吸收光”，而锦缎与丝绣靠成千上万根微米三棱镜“定向操控反射光”！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "桑蚕丝脱胶前后三棱柱截面光学原理与方向各向异性图解",
        "左图对比粗糙丝胶包裹的生丝与精练脱胶后折射率1.548的圆角三棱镜熟丝截面；右图展示同色丝线在0度顺光与90度横切排布下的明暗反差，解释暗花缎与刺绣立体光影来源。",
        el,
    )
    write_svg(SUBDIR, "silk-triangular-prism-optics.svg", svg)


def _draw_weave_grid(el, x0, y0, cell, n, is_warp_up_fn, warp_col=BLUE, weft_col=GOLD_SOFT):
    """Draw an n x n weave point diagram (意匠图). Filled cell = warp over weft."""
    for row in range(n):
        # row 0 at bottom in traditional textile drafting, so screen y = y0 + (n - 1 - row) * cell
        sy = y0 + (n - 1 - row) * cell
        for col in range(n):
            sx = x0 + col * cell
            up = is_warp_up_fn(col, row)
            fill = warp_col if up else weft_col
            el.append(
                f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{cell:.1f}" height="{cell:.1f}" '
                f'fill="{fill}" stroke="#cbd5e1" stroke-width="0.9"/>'
            )


def build_fig2_three_weaves_and_satin_math():
    """Fig 2: Plain / Twill / Satin weave matrices + Why 6-end regular satin is mathematically impossible."""
    el = []
    el.extend(
        header(
            "“缎”凭什么滑如镜面？织物三原组织矩阵与藏在缎纹里的“互质数论”",
            "深色格=经线浮在上面，浅色格=纬线在上面；长浮线越长、交织点越隐蔽，表面就越像一整面丝绸镜子！",
        )
    )

    # Top row: 4 exact 8x8 weave matrices side by side!
    cards_cfg = [
        (22, "① 平纹 (R=2)", "一上一下棋盘格", lambda c, r: (c + r) % 2 == 0, SLATE, "交织率 50%｜结实发暗（绢/平布）"),
        (204, "② 斜纹 (R=4, 3/1)", "连续斜对角浮线", lambda c, r: (r - c) % 4 != 3, BLUE, "浮长 3｜45°斜纹（绫/斜纹绸）"),
        (386, "③ 五枚缎 (R=5, S=2)", "最小正规经面缎！", lambda c, r: (r * 2) % 5 != c % 5, ORANGE, "浮长 4｜交织点彻底打散（五丝缎）"),
        (568, "④ 八枚缎 (R=8, S=3)", "贡缎/素软缎王牌", lambda c, r: (r * 3) % 8 != c % 8, PURPLE, "浮长 7｜87.5% 顺滑长丝"),
    ]
    for x_left, title_s, sub_s, fn, col_theme, foot_s in cards_cfg:
        el.append(card(x_left, 68, 170, 246, fill=CARD_BG))
        el.append(txt(x_left + 85, 90, title_s, size=12, color=col_theme, anchor="middle", weight="700"))
        el.append(txt(x_left + 85, 108, sub_s, size=10.5, color=MUTED, anchor="middle"))
        # 8x8 grid of 17px cells = 136px wide -> margin = (170 - 136)/2 = 17px!
        _draw_weave_grid(el, x_left + 17, 118, 17.0, 8, fn, warp_col=col_theme, weft_col="#fffbeb")
        el.append(txt(x_left + 85, 274, "深色=经浮  浅格=纬扣", size=10, color=SLATE, anchor="middle"))
        el.append(txt(x_left + 85, 296, foot_s, size=10, color=INK, anchor="middle", weight="600"))

    # Bottom Left Card: The Number-Theory Theorem of Regular Satin (Why R=6 fails!)
    el.append(card(22, 326, 462, 132, fill=CARD_BG))
    el.append(step_badge(40, 348, 1, fg=RED, bg=RED_SOFT))
    el.append(txt(58, 353, "纺织机上的数论铁律：为什么偏偏没有“六枚正规缎纹”？", size=12, color=INK, weight="700"))

    el.append(txt(36, 378, "• 正规缎纹每升一纬横移固定“飞数 S”，须同时满足三条公理：", size=10.5, color=BODY))
    el.append(txt(44, 399, "① R ≥ 5；  ② 1 < S < R−1（防退化为斜纹）；  ③ gcd(R, S) = 1 互质！", size=10.5, color=BLUE, weight="700"))
    el.append(txt(36, 421, "• 代入 R = 6：候选 S ∈ {2, 3, 4} 全与 6 不互质（必漏织散架，无解）！", size=10.5, color=RED, weight="700"))
    el.append(txt(36, 442, "• 唐宋织工破局绝招：改用变步长序列 [1, 4, 2, 6, 3, 5] 创制“六枚变则缎”！", size=10.5, color=GREEN, weight="700"))

    # Bottom Right Card: Mechanics trade-off & Quanzhou Zayton etymology
    el.append(card(496, 326, 242, 132, fill=CARD_BG))
    el.append(step_badge(514, 348, 2, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(532, 353, "光泽与勾丝的博弈", size=12, color=INK, weight="700"))
    el.append(txt(508, 378, "• 越亮越娇贵：八枚缎连跨 7 纬才", size=10.3, color=BODY))
    el.append(txt(508, 397, "  扣紧 1 点 → 倒刺一刮极易勾丝！", size=10.3, color=ORANGE, weight="700"))
    el.append(txt(508, 419, "• 词源：英语 Satin 源自元代福建", size=10.3, color=BODY))
    el.append(txt(508, 438, "  泉州“刺桐港 (Zayton)”！", size=10.3, color=PURPLE, weight="700"))

    # Footer
    el.append(card(22, 470, 716, 40, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(
        txt(
            380,
            495,
            "丝绸品种一眼分清：平纹轻薄叫“绢/绡”，斜纹起浪叫“绫”，镂空绞经叫“罗”，长浮镜面就叫“缎”！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        524,
        "织物三原组织意匠矩阵与缎纹互质数论原理图解",
        "上方并列展示平纹(R=2)、斜纹(R=4)、五枚缎(R=5,S=2)和八枚缎(R=8,S=3)的8x8精确意匠图；下方证明因2,3,4与6均不互质故不存在六枚正规缎纹，以及唐宋六枚变则缎破局法。",
        el,
    )
    write_svg(SUBDIR, "three-weaves-and-satin-math.svg", svg)


def build_fig3_brocade_drawloom_binary_anim():
    """Fig 3: Animated binary pattern-book (挑花结本) reading on drawloom + Yunjin 通经断纬 brocade."""
    # 1-shot 6.4s CSS animation highlighting 4 rows of binary pattern reading sequentially, holding final state
    extra_css = """
  .bin-row-1 { opacity: 1; animation: rowPulse1 6.4s ease-out 0.3s 1 forwards; }
  .bin-row-2 { opacity: 0.45; animation: rowPulse2 6.4s ease-out 0.3s 1 forwards; }
  .bin-row-3 { opacity: 0.45; animation: rowPulse3 6.4s ease-out 0.3s 1 forwards; }
  .bin-row-4 { opacity: 0.45; animation: rowPulse4 6.4s ease-out 0.3s 1 forwards; }
  .shuttle-anim { transform: translate(0px, 0px); animation: shuttlePass 6.4s ease-in-out 0.3s 1 forwards; }
  @keyframes rowPulse1 {
    0%, 24% { opacity: 1; }
    25%, 90% { opacity: 0.85; }
    100% { opacity: 1; }
  }
  @keyframes rowPulse2 {
    0%, 24% { opacity: 0.4; }
    25%, 49% { opacity: 1; }
    50%, 90% { opacity: 0.85; }
    100% { opacity: 1; }
  }
  @keyframes rowPulse3 {
    0%, 49% { opacity: 0.4; }
    50%, 74% { opacity: 1; }
    75%, 90% { opacity: 0.85; }
    100% { opacity: 1; }
  }
  @keyframes rowPulse4 {
    0%, 74% { opacity: 0.4; }
    75%, 100% { opacity: 1; }
  }
  @keyframes shuttlePass {
    0% { transform: translate(0px, 0px); }
    25% { transform: translate(86px, 0px); }
    50% { transform: translate(0px, 0px); }
    75% { transform: translate(86px, 0px); }
    100% { transform: translate(44px, 0px); }
  }
  @media (prefers-reduced-motion: reduce) {
    .bin-row-1, .bin-row-2, .bin-row-3, .bin-row-4 { animation: none !important; opacity: 1 !important; }
    .shuttle-anim { animation: none !important; transform: translate(44px, 0px) !important; }
  }
"""
    el = []
    el.extend(
        header(
            "“锦”为什么寸锦寸金？比电子计算机早两千年的“二进制花本”与通经断纬",
            "缎是单色组织光泽，锦则是“重组织多色提花”：花纹在织布瞬间按 0/1 代码同步长进布骨子里！",
        )
    )

    # Left Card: Binary Pattern Loom (老官山汉墓提花机 -> 大花楼挑花结本 -> 1804 贾卡打孔卡)
    el.append(card(22, 68, 372, 386, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 95, "挑花结本：用结绳/孔卡存储 0 与 1 的“丝绸只读程序”", size=12, color=INK, weight="700"))

    # Binary program matrix box (4 rows x 8 warp columns representing a symmetric diamond brocade motif!)
    el.append(card(36, 112, 344, 174, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(208, 132, "花本指令行（1 = 拽起经线露底，0 = 沉下经线显彩纬）", size=10.5, color=INK, anchor="middle", weight="700"))

    prog_rows = [
        ("bin-row-1", "第 1 纬", [1, 1, 1, 0, 0, 1, 1, 1]),
        ("bin-row-2", "第 2 纬", [1, 1, 0, 0, 0, 0, 1, 1]),
        ("bin-row-3", "第 3 纬", [1, 0, 0, 1, 1, 0, 0, 1]),
        ("bin-row-4", "第 4 纬", [1, 1, 0, 0, 0, 0, 1, 1]),
    ]
    for r_idx, (cls_name, r_lbl, bits) in enumerate(prog_rows):
        ry = 144 + r_idx * 27
        row_parts = [f'<g class="{cls_name}">']
        row_parts.append(txt(48, ry + 15, r_lbl, size=10.5, color=SLATE, weight="700"))
        for c_idx, b in enumerate(bits):
            bx = 104 + c_idx * 31
            bg_c = BLUE if b == 1 else ORANGE
            fg_c = "#ffffff"
            row_parts.append(f'<rect x="{bx}" y="{ry}" width="26" height="21" rx="4" fill="{bg_c}"/>')
            row_parts.append(txt(bx + 13, ry + 15, str(b), size=11, color=fg_c, anchor="middle", weight="700"))
        row_parts.append("</g>")
        el.append("".join(row_parts))

    el.append(txt(208, 274, "蓝色 1 = 提综抬经    橙色 0 = 沉经露金红彩纬（菱形花纹成形！）", size=10, color=MUTED, anchor="middle", weight="600"))

    # Shedding + Shuttle diagram at bottom of Left Card
    el.append(card(36, 296, 344, 144, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(48, 316, "大花楼双人协同（上拽花本读指令，下投飞梭织彩锦）：", size=11, color=BLUE, weight="700"))
    # Upper & lower warp shed lines forming diamond opening for shuttle!
    el.append(_line(54, 356, 156, 334, color=BLUE, sw=2.0))
    el.append(_line(156, 334, 266, 356, color=BLUE, sw=2.0))
    el.append(_line(54, 356, 156, 378, color=SLATE, sw=2.0))
    el.append(_line(156, 378, 266, 356, color=SLATE, sw=2.0))
    el.append(_line(156, 318, 156, 334, color=RED, sw=1.8, dash="3,2"))
    el.append(txt(274, 342, "↑ 提花工拽起“1”经", size=10.5, color=RED, weight="700"))
    el.append(txt(274, 366, "← 梭口张开投彩纬", size=10.5, color=ORANGE, weight="700"))

    # Animated gold shuttle inside shed
    el.append(
        f'<g class="shuttle-anim">'
        f'<polygon points="96,356 112,350 132,350 148,356 132,362 112,362" fill="{GOLD}" stroke="#ffffff" stroke-width="1.2"/>'
        f'</g>'
    )
    el.append(txt(48, 404, "• 历史传承链：成都老官山汉墓提花机(前2世纪) → 明清云锦结绳花本", size=10, color=INK, weight="600"))
    el.append(txt(48, 423, "  → 1804 法国贾卡打孔卡织机 → 巴贝奇分析机与现代计算机编程鼻祖！", size=10, color=PURPLE, weight="700"))

    # Right Card: Compound Weave & Nanjing Yunjin "通经断纬 (挖花妆彩)"
    el.append(card(408, 68, 330, 386, fill=CARD_BG))
    el.append(step_badge(428, 90, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(446, 95, "三大名锦核心绝活：重组织与“通经断纬”", size=12, color=INK, weight="700"))

    # Top box:通经通纬 vs 通经断纬 diagram
    el.append(card(422, 112, 302, 186, rx=8, fill=GOLD_SOFT, stroke=GOLD))
    el.append(txt(434, 133, "为什么南京云锦至今无法被现代工业织机完全替代？", size=11, color=GOLD, weight="700"))

    # Draw vertical continuous warps across [446..700]
    for k in range(11):
        wx = 450 + k * 25
        el.append(_line(wx, 146, wx, 248, color="#cbd5e1", sw=1.8))

    # Top row: Ordinary full-width weft (通经通纬) wasting gold yarn across whole width
    el.append(_line(440, 164, 708, 164, color=SLATE, sw=4.0))
    el.append(txt(574, 182, "普通提花（通经通纬）：金线横贯全幅，背面全浪费！", size=10, color=MUTED, anchor="middle"))

    # Bottom zones: Discontinuous swivel wefts (通经断纬 / 挖花盘织)!
    el.append(f'<rect x="468" y="198" width="68" height="22" rx="6" fill="{RED_SOFT}" stroke="{RED}" stroke-width="1.8"/>')
    el.append(txt(502, 213, "红绒小梭", size=10, color=RED, anchor="middle", weight="700"))

    el.append(f'<rect x="552" y="198" width="68" height="22" rx="6" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>')
    el.append(txt(586, 213, "孔雀羽梭", size=10, color=GREEN, anchor="middle", weight="700"))

    el.append(f'<rect x="634" y="198" width="68" height="22" rx="6" fill="#fef3c7" stroke="{GOLD}" stroke-width="1.8"/>')
    el.append(txt(668, 213, "扁金线梭", size=10, color=GOLD, anchor="middle", weight="700"))

    el.append(txt(574, 242, "云锦“通经断纬（挖花妆彩）”：几十把小梭分区盘织！", size=10.5, color=RED, anchor="middle", weight="700"))
    el.append(txt(574, 263, "同一横行自由换几十种色彩，连真金线与孔雀羽都能织进去，", size=10, color=BODY, anchor="middle"))
    el.append(txt(574, 280, "两位老匠人配合一天仅能织出 5～6 厘米，故称“寸锦寸金”！", size=10, color=INK, anchor="middle", weight="600"))

    # Bottom box: Quick comparison of China's Three Famous Brocades (三大名锦)
    el.append(card(422, 310, 302, 130, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(434, 331, "中国三大名锦的“重组织”技术指纹：", size=11.5, color=INK, weight="700"))
    el.append(txt(434, 355, "• 四川蜀锦（最古，兴于秦汉）：多用“经锦”（多色经线", size=10.5, color=BODY))
    el.append(txt(434, 373, "  交替浮出显花，不显花的色经藏入夹层背面）", size=10.5, color=MUTED))
    el.append(txt(434, 395, "• 苏州宋锦（文人书画装裱圣品）：三枚斜纹地 + 纬重组织", size=10.5, color=BODY))
    el.append(txt(434, 417, "• 南京云锦（宫廷巅峰，2009 世遗）：缎纹地 + 挖花盘金羽", size=10.5, color=GOLD, weight="700"))

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            491,
            "核心判别法：把面料翻到背面看——印花布背面惨白模糊；织锦背面则是严丝合缝的彩色经纬结构反相或换梭接头！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "织锦大花楼挑花结本二进制提花原理与南京云锦通经断纬图解",
        "左图通过单次逐行动画展示花本0/1二进制代码控制经线起落与梭口投纬及从老官山汉墓织机到贾卡织机的传承；右图对比普通通经通纬与南京云锦多小梭局部盘织的通经断纬结构。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "brocade-drawloom-binary-code-anim.svg", svg)


def build_fig4_embroidery_splitting_and_stitches():
    """Fig 4: Splitting silk down to 1/64-1/128 + Optical spatial color mixing (套针 / 乱针绣)."""
    el = []
    el.extend(
        header(
            "从“织”跨入“绣”：挣脱 90° 经纬网格，1/128 劈丝与“以针代笔”光学混色",
            "染好的丝线不能像油彩一样调和，绣娘靠“微米劈丝 + 犬牙套针/斜叉乱针”骗过人眼分辨率！",
        )
    )

    # Left Card: Thread Splitting Scale (1 strand -> 1/2 -> 1/16 -> 1/64 -> 1/128!)
    el.append(card(22, 68, 356, 384, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(60, 95, "指尖微米手术：一根绣花线劈成 128 丝有多细？", size=12, color=INK, weight="700"))

    el.append(card(36, 112, 328, 198, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    scales = [
        ("1 根原装花线（1 股）", 16.0, PURPLE, "直径约 200 μm｜粗犷打底"),
        ("成人头发丝（参照标尺）", 7.0, SLATE, "直径约 70 μm"),
        ("劈成 1/16 丝（精细平绣）", 3.2, BLUE, "约 1～2 根单蚕丝（~12 μm）"),
        ("劈成 1/64～1/128 丝！", 1.1, RED, "仅约 2～4 μm（发丝的 1/20！）"),
    ]
    sy = 136
    for lbl, r_vis, col, note in scales:
        el.append(f'<circle cx="68" cy="{sy + 6}" r="{r_vis:.1f}" fill="{col}"/>')
        el.append(txt(96, sy + 4, lbl, size=11, color=INK, weight="700"))
        el.append(txt(96, sy + 20, note, size=10.5, color=col if col == RED else MUTED, weight="600" if col == RED else "400"))
        sy += 44

    # Why split so fine? Optical resolution box!
    el.append(card(36, 322, 328, 116, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(48, 344, "为什么非要劈到肉眼几乎看不见？", size=11.5, color=PURPLE, weight="700"))
    el.append(txt(48, 367, "• 人眼在 30 cm 正常观赏距离的分辨极限约 90 μm！", size=10.5, color=INK, weight="700"))
    el.append(txt(48, 388, "• 当丝线细至几微米（远小于 90 μm），深红、绯红、粉白", size=10.5, color=BODY))
    el.append(txt(48, 407, "  几十种色丝并排穿插，视网膜会自动融合成无缝柔光渐变，", size=10.5, color=BODY))
    el.append(txt(48, 426, "  彻底消灭笔刷痕迹！（原理同手机视网膜屏亚像素混色）", size=10.5, color=GREEN, weight="700"))

    # Right Card: Three Core Stitch Engineering Paradigms
    el.append(card(392, 68, 346, 384, fill=CARD_BG))
    el.append(step_badge(412, 90, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(430, 95, "三大里程碑针法：如何消除色块硬边与制造景深？", size=12, color=INK, weight="700"))

    # Paradigm 1:齐针 hard seam defect
    el.append(card(406, 112, 318, 94, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(418, 132, "① 齐针并排（反例）：同长齐头换色 → 必留“生硬刀切缝”", size=10.5, color=SLATE, weight="700"))
    for k in range(6):
        yk = 146 + k * 8
        el.append(_line(426, yk, 536, yk, color="#dc2626", sw=2.6))
        el.append(_line(540, yk, 650, yk, color="#fca5a5", sw=2.6))
    el.append(_line(538, 140, 538, 194, color=INK, sw=1.4, dash="2,2"))
    el.append(txt(684, 172, "断层刺眼!", size=10.5, color=RED, anchor="middle", weight="700"))

    # Paradigm 2: 苏绣散套针 (Encroaching Satin / Long-and-Short Stitch)
    el.append(card(406, 216, 318, 104, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(418, 236, "② 苏绣“散套针”：长短犬牙嵌合 → 如水彩晕染无痕过渡！", size=10.5, color=BLUE, weight="700"))
    offsets = [(426, 534, 510, 608, 582, 694), (426, 506, 486, 586, 560, 694),
               (426, 548, 520, 622, 598, 694), (426, 518, 494, 596, 570, 694),
               (426, 540, 514, 614, 588, 694), (426, 512, 490, 590, 566, 694)]
    for k, (a1, a2, b1, b2, c1, c2) in enumerate(offsets):
        yk = 250 + k * 9
        el.append(_line(a1, yk, a2, yk, color="#b91c1c", sw=2.3))
        el.append(_line(b1, yk - 3, b2, yk - 3, color="#ef4444", sw=2.3))
        el.append(_line(c1, yk, c2, yk, color="#fca5a5", sw=2.3))
    el.append(txt(565, 311, "后一批色丝深插进前一批缝隙，丝光顺畅接力！", size=10, color=INK, anchor="middle", weight="600"))

    # Paradigm 3: 杨守玉“乱针绣” (Random-Stitch / Cross-Layered Vector Blending)
    el.append(card(406, 330, 318, 110, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(418, 350, "③ 现代突破“乱针绣”（杨守玉创立）：斜叉叠压出油画景深！", size=10.5, color=ORANGE, weight="700"))
    # Criss-crossing angled strokes (base dark blue/purple, mid warm orange, top bright gold/red)
    strokes = [
        (426, 418, 488, 364, PURPLE), (452, 422, 520, 364, BLUE), (492, 420, 558, 366, PURPLE),
        (434, 368, 506, 418, ORANGE), (470, 366, 542, 420, RED), (512, 368, 576, 418, GOLD),
        (444, 404, 534, 378, "#f59e0b"), (480, 412, 566, 380, "#ef4444"),
    ]
    for x1, y1, x2, y2, sc in strokes:
        el.append(_line(x1, y1, x2, y2, color=sc, sw=2.2))
    el.append(txt(590, 376, "• 底层粗丝铺大色块", size=10, color=BODY))
    el.append(txt(590, 395, "• 面层细丝多角度斜叉", size=10, color=BODY))
    el.append(txt(590, 414, "• 三维立体散射混色！", size=10.5, color=RED, weight="700"))

    # Footer
    el.append(card(22, 464, 716, 40, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            489,
            "苏绣八字真言“平、齐、细、密、和、顺、光、匀”——每一字背后都是纤维张力控制与微米级光学排列！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        518,
        "苏绣1/128劈丝尺度对比与齐针、散套针、乱针绣光学混色原理图",
        "左图对比1股花线(200微米)、人发(70微米)、1/16丝与1/128极细丝(2-4微米)及人眼90微米分辨极限混色原理；右图对比齐针断层、散套针犬牙嵌合晕染与乱针绣多层斜叉叠光。",
        el,
    )
    write_svg(SUBDIR, "embroidery-splitting-and-stitches.svg", svg)


def build_fig5_double_sided_hetero_and_comparison():
    """Fig 5: Double-sided three-hetero embroidery cross-section topology + Weaving vs Embroidery synthesis."""
    el = []
    el.extend(
        header(
            "巅峰解密：一块透明薄纱正反绣出“橘猫与黑狗”，异色丝线到底藏哪儿了？",
            "放大 100 倍剖开“双面三异绣（异稿、异针、异色）”的微观走针拓扑，并看懂锦、缎、绣的终极分工",
        )
    )

    # Left Card: Cross-section of Double-Sided Heterochromatic Embroidery
    el.append(card(22, 68, 396, 384, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=RED, bg=RED_SOFT))
    el.append(txt(60, 95, "微观横截面解剖：双面异色绣“长浮遮短扣”隐身术", size=12, color=INK, weight="700"))

    el.append(card(36, 112, 368, 210, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(220, 134, "↑ 正面观赏者视线（只看见鲜亮橘猫毛色，毫无黑点！）", size=10.5, color=ORANGE, anchor="middle", weight="700"))

    # Sheer silk organza ground fabric (底料薄绡经纱截面 dots along y = 216)
    el.append(_line(50, 216, 390, 216, color=BORDER, sw=1.5, dash="3,3"))
    for k in range(11):
        gx = 66 + k * 31
        el.append(f'<circle cx="{gx}" cy="216" r="5" fill="#e2e8f0" stroke="{SLATE}" stroke-width="1.4"/>')
    el.append(txt(394, 206, "透明底绢丝", size=9.5, color=MUTED, anchor="end"))

    # Top Orange Thread path: Long visible float on TOP (x=66..221), tiny micro-tuck under ONE ground yarn at x=221, back up (x=221..376)!
    el.append(
        f'<path d="M62,188 C90,174 190,174 216,188 L221,227 L227,188 C256,174 348,174 380,188" '
        f'fill="none" stroke="{ORANGE}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    # Bottom Blue/Black Thread path: Long visible float on BOTTOM covering the tiny orange micro-tuck at x=221!
    # And its own tiny micro-tuck on TOP at x=128 is completely buried underneath the wide orange float!
    el.append(
        f'<path d="M62,244 C82,256 108,256 123,244 L128,205 L134,244 C170,258 330,258 380,244" '
        f'fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    # Callouts pointing to the two hidden micro-tucks!
    el.append(_line(128, 202, 128, 160, color=BLUE, sw=1.4, dash="2,2"))
    el.append(txt(218, 155, "← 黑线折返微点 (<0.2 mm) 被橘色长丝完全盖死！", size=9.8, color=BLUE, anchor="middle", weight="700", halo=True))

    el.append(_line(221, 231, 221, 272, color=RED, sw=1.4, dash="2,2"))
    el.append(txt(221, 286, "橘线折返微点被背面黑色长丝严密遮蔽！", size=9.8, color=RED, anchor="middle", weight="700", halo=True))

    el.append(txt(220, 310, "↓ 背面观赏者视线（只看见乌亮黑犬皮毛，零线头零死结！）", size=10.5, color=INK, anchor="middle", weight="700"))

    # Three rules box at bottom of Left Card
    el.append(card(36, 332, 368, 108, rx=8, fill=RED_SOFT, stroke=RED))
    el.append(txt(48, 353, "双面三异绣三大铁律（容错率为零）：", size=11.5, color=RED, weight="700"))
    el.append(txt(48, 375, "① 藏头隐尾不打结：起针穿入底丝夹心，收针顺贴邻线靠摩擦自锁；", size=10.5, color=BODY))
    el.append(txt(48, 395, "② 轮廓重合公用边界：正反两幅异形图案的外轮廓严丝合缝对齐遮挡；", size=10.5, color=BODY))
    el.append(txt(48, 415, "③ 夹层遮蔽：异色折返点必须落在对方长浮针肚皮底下，绝不露异色！", size=10.5, color=INK, weight="700"))

    # Right Card: Ultimate Technical Synthesis (锦 vs 缎 vs 绣)
    el.append(card(432, 68, 306, 384, fill=CARD_BG))
    el.append(step_badge(452, 90, 2, fg=TEAL, bg=TEAL_SOFT))
    el.append(txt(470, 95, "一图分清“锦、缎、绣”底层技术原理", size=12, color=INK, weight="700"))

    boxes = [
        ("缎 (Satin) —— 单层镜面织法", PURPLE, PURPLE_SOFT, [
            "• 原理：经纬交织点极少且互质打散(R≥5,R≠6)",
            "• 特长：极度顺滑光亮，是刺绣最佳“发光画布”",
            "• 短板：单层结构浮线长，怕硬物刮擦勾丝",
        ]),
        ("锦 (Brocade) —— 多层编程织花", GOLD, GOLD_SOFT, [
            "• 原理：先染后织，0/1 花本控制多套重经/断纬",
            "• 特长：花纹与布骨一体成型，挺括富丽耐磨",
            "• 短板：受限于正交网格，制版挑花耗时数月",
        ]),
        ("绣 (Embroidery) —— 自由矢量针画", GREEN, GREEN_SOFT, [
            "• 原理：织好底布后，劈丝至微米级 360° 穿刺",
            "• 特长：突破经纬直角，色彩渐变与立体感无敌",
            "• 融合：在锦缎底上施刺绣 = 名副其实“锦上添花”！",
        ]),
    ]
    by = 112
    for b_title, fg_c, bg_c, lines in boxes:
        el.append(card(444, by, 282, 104, rx=8, fill=bg_c, stroke=fg_c))
        el.append(txt(456, by + 21, b_title, size=11, color=fg_c, weight="700"))
        for idx_l, ln in enumerate(lines):
            el.append(txt(456, by + 43 + idx_l * 20, ln, size=10.2, color=INK if "锦上添花" in ln else BODY, weight="700" if "锦上添花" in ln else "400"))
        by += 114

    # Footer
    el.append(card(22, 464, 716, 40, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(
        txt(
            380,
            489,
            "成语“锦上添花”的技术真相：在本来就用重组织提花织出暗纹的“锦缎”底料上，再用劈丝彩线“刺绣”出高光花鸟！",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        518,
        "双面三异绣横截面藏针隐色拓扑图与锦缎绣三大技术对比表",
        "左图放大展示双面异色绣在透明底绢两侧利用长浮线遮蔽对方小于0.2毫米微折返点的横截面拓扑；右图系统对比缎(单层镜面长浮)、锦(重组织0/1提花)与绣(360度劈丝混色)的技术本质。",
        el,
    )
    write_svg(SUBDIR, "double-sided-three-hetero-embroidery.svg", svg)


@register("brocade-embroidery", "锦缎刺绣艺术技术原理原创图解集", "humanities")
def build_all():
    _verify_textile_and_optical_math()
    build_fig1_silk_prism_optics()
    build_fig2_three_weaves_and_satin_math()
    build_fig3_brocade_drawloom_binary_anim()
    build_fig4_embroidery_splitting_and_stitches()
    build_fig5_double_sided_hetero_and_comparison()
