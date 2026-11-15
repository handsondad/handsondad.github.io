"""Celestial Body Rotation & Spin Dynamics visual builders."""

import math

from .core import (
    BG,
    BLUE,
    BLUE_SOFT,
    BODY,
    BORDER,
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
    txt,
    write_svg,
)

CRIMSON = "#b91c1c"
CRIMSON_SOFT = "#fef2f2"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"


# Official NASA NSSDCA Planetary Fact Sheet parameters:
# (name_zh, obliquity_deg, sidereal_hours, solar_day_hours, r_eq_km, r_pol_km, color)
PLANETS_SPIN = [
    ("水星", 0.034, 1407.6, 4222.6, 2439.7, 2439.7, SLATE),
    ("金星", 177.4, -5832.5, 2802.0, 6051.8, 6051.8, ORANGE),
    ("地球", 23.44, 23.9345, 24.000, 6378.1, 6356.8, BLUE),
    ("火星", 25.19, 24.6229, 24.6597, 3396.2, 3376.2, CRIMSON),
    ("木星", 3.13, 9.9250, 9.9259, 71492.0, 66854.0, AMBER),
    ("土星", 26.73, 10.656, 10.656, 60268.0, 54364.0, TEAL),
    ("天王星", 97.77, -17.24, 17.24, 25559.0, 24973.0, PURPLE),
    ("海王星", 28.32, 16.11, 16.11, 24764.0, 24341.0, BLUE),
]


def _verify_celestial_spin_math():
    """Verify sidereal/solar day relation, equatorial speeds, oblateness, Sun differential law, and breakup limits."""
    c_light = 299792.458  # km/s

    # 1. Exact Sidereal vs Solar Day formula: 1/T_solar = 1/T_sid - 1/T_orb (signed T_sid)
    # Earth: T_sid = 23.9344696 h = 0.99726957 d, T_orb = 365.25636 d
    t_sol_earth = 1.0 / (1.0 / (86164.0905 / 86400.0) - 1.0 / 365.25636)
    assert abs(t_sol_earth - 1.000000) < 1e-4

    # Venus: retrograde T_sid = -5832.5 h = -243.0208 d, T_orb = 224.701 d
    t_sid_venus_d = -5832.5 / 24.0
    t_sol_venus_d = abs(1.0 / (1.0 / t_sid_venus_d - 1.0 / 224.701))
    assert 116.7 <= t_sol_venus_d <= 116.8  # 116.75 Earth days (~2802 hours)

    # Mercury: 3:2 spin-orbit resonance -> T_sid = 58.646 d, T_orb = 87.969 d => T_solar = 175.94 d = 2 * T_orb
    t_sol_merc_d = abs(1.0 / (1.0 / (1407.5 / 24.0) - 1.0 / 87.969))
    assert 175.8 <= t_sol_merc_d <= 176.1

    # 2. Equatorial linear velocities v = 2*pi*R_eq / |T_sid|
    v_venus_ms = 2 * math.pi * 6051800.0 / (5832.5 * 3600.0)     # 1.811 m/s (6.52 km/h)
    v_earth_ms = 2 * math.pi * 6378137.0 / 86164.0905             # 465.10 m/s (1674.4 km/h)
    v_jup_kms = 2 * math.pi * 71492.0 / (9.9250 * 3600.0)         # 12.571 km/s
    assert 1.80 <= v_venus_ms <= 1.82
    assert 465.0 <= v_earth_ms <= 465.2
    assert 12.55 <= v_jup_kms <= 12.59

    # 3. Earth centrifugal breakup period T_min = 2*pi*sqrt(R_eq^3 / GM_earth)
    mu_earth = 3.986004418e14  # m^3/s^2
    t_break_min = (2 * math.pi * math.sqrt((6378137.0 ** 3) / mu_earth)) / 60.0
    assert 84.4 <= t_break_min <= 84.6  # 84.49 minutes!

    # 4. Oblateness f = (R_eq - R_pol) / R_eq
    f_earth = (6378.1 - 6356.8) / 6378.1
    f_jup = (71492.0 - 66854.0) / 71492.0
    f_sat = (60268.0 - 54364.0) / 60268.0
    assert 0.0033 <= f_earth <= 0.0034
    assert 0.0648 <= f_jup <= 0.0650
    assert 0.0979 <= f_sat <= 0.0981

    # 5. Sun differential rotation law (NASA Sun Fact Sheet): Omega(L) = 14.37 - 2.33 sin^2 L - 1.56 sin^4 L deg/day
    def sun_period_days(lat_deg):
        s2 = math.sin(math.radians(lat_deg)) ** 2
        omega = 14.37 - 2.33 * s2 - 1.56 * (s2 ** 2)
        return 360.0 / omega

    assert 25.0 <= sun_period_days(0) <= 25.1
    assert abs(sun_period_days(16) - 609.12 / 24.0) < 0.02  # 25.380 Earth days (609.12 hours)
    assert 34.3 <= sun_period_days(90) <= 34.5

    # 6. Fastest pulsar PSR J1748-2446ad: f = 716.36 Hz, R <= 16 km => v_eq ~ 0.24 c
    v_psr_kms = 2 * math.pi * 16.0 * 716.36
    assert 0.238 <= (v_psr_kms / c_light) <= 0.242


def _extra_markers():
    return """<marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#6d28d9"/>
  </marker>
  <marker id="arr-crimson" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#b91c1c"/>
  </marker>"""


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{extra}{mk}/>'
    )


def _build_angular_momentum_origin():
    """SVG 1: Why almost everything in the universe spins — collapse amplifies tiny initial angular momentum."""
    h = 478
    el = []
    el.extend(
        header(
            "天体自转的第一推动力：太空里没人推一把，星球凭什么自己转起来？",
            "角动量守恒（L = Iω ∝ M·R²·ω）：只要初始气体云净涡旋不为绝对零，引力坍缩就会把微动放大百万倍",
        )
    )

    # Left Card: Nebula -> Flattened Disk -> Spinning Star & Planets (x=16..396)
    el.append(card(16, 68, 380, 394))
    el.append(pill(28, 80, "花样滑冰收臂效应：星云坍缩三部曲", fg=BLUE, bg=BLUE_SOFT, w=236, h=24))

    # Stage 1: Diffuse molecular cloud
    el.append(
        f'<ellipse cx="96" cy="176" rx="58" ry="44" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    )
    el.append(txt(96, 171, "① 原始星云", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(96, 190, "R ≈ 1 光年", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(96, 236, "湍流无法 100% 抵消", size=10.3, color=MUTED, anchor="middle"))
    el.append(txt(96, 252, "残余微弱净旋转", size=10.3, color=INK, anchor="middle", weight="600"))

    el.append(_line(160, 176, 188, 176, color=BLUE, sw=1.8, marker="arr-blue"))

    # Stage 2: Flattened protoplanetary disk
    el.append(
        f'<ellipse cx="242" cy="176" rx="46" ry="15" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>'
    )
    el.append(f'<circle cx="242" cy="176" r="10" fill="{ORANGE}"/>')
    el.append(txt(242, 145, "② 坍缩摊成圆盘", size=11, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(242, 236, "垂直方向掉向赤道面", size=10.3, color=MUTED, anchor="middle"))
    el.append(txt(242, 252, "水平角动量拉住物质", size=10.3, color=INK, anchor="middle", weight="600"))

    el.append(_line(294, 176, 318, 176, color=ORANGE, sw=1.8, marker="arr-orange"))

    # Stage 3: Spinning star & planets
    el.append(f'<circle cx="352" cy="176" r="24" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>')
    el.append(_line(352, 142, 352, 210, color=GREEN, sw=1.5, dash="3 2"))
    el.append(txt(352, 180, "ω 暴增!", size=10.5, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(352, 236, "③ 恒星与行星", size=11, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(352, 252, "继承同一转向", size=10.3, color=INK, anchor="middle", weight="600"))

    # Key physical intuition box at bottom of Left Card
    el.append(
        f'<rect x="28" y="274" width="356" height="174" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    el.append(txt(40, 296, "为什么牛顿当年感叹“第一推动”，而现代天体物理不慌？", size=11.3, color=INK, weight="700"))
    el.append(txt(40, 319, "• 真实宇宙气体云受邻近超新星冲击与星系差异旋转扰动，", size=10.8, color=BODY))
    el.append(txt(40, 339, "  往左与往右的动量矩刚好抵消到小数点后无穷位的概率为 0；", size=10.8, color=BODY))
    el.append(txt(40, 361, "• 当半径 R 缩小 1,000 万倍凝成恒星时，哪怕最初边缘只有", size=10.8, color=BODY))
    el.append(txt(40, 381, "  每秒几厘米的微风偏转，按 v_⊥ ∝ 1/R 也会飙升到千米/秒！", size=10.8, color=BLUE, weight="700"))
    el.append(txt(40, 405, "• 这同时解释了为什么太阳自转、八大行星公转与大多数行星", size=10.8, color=BODY))
    el.append(txt(40, 425, "  自转，从北极俯视全都是整齐划一的“逆时针（自西向东）”！", size=10.8, color=INK, weight="600"))

    # Right Card: Quantitative R^2 Scaling Ladder (x=408..744)
    el.append(card(408, 68, 336, 394))
    el.append(pill(420, 80, "坍缩放大账本：ω₂ / ω₁ ≈ (R₁ / R₂)²", fg=PURPLE, bg=PURPLE_SOFT, w=244, h=24))

    rungs = [
        ("① 星际分子云核", "R ≈ 10¹² km", "几百万年才微转一圈", BLUE, BLUE_SOFT),
        ("② 坍缩成年轻恒星", "R ≈ 7×10⁵ km", "几天至几十天一圈（如太阳 25天）", GREEN, GREEN_SOFT),
        ("③ 晚年压成白矮星", "R ≈ 6,000 km", "几分钟至几小时一圈", ORANGE, ORANGE_SOFT),
        ("④ 铁核坍成中子星!", "R ≈ 12–16 km", "每秒几十圈至 716 圈!", PURPLE, PURPLE_SOFT),
    ]
    for idx, (r_title, r_rad, r_spin, fg_c, bg_c) in enumerate(rungs):
        ry = 118 + idx * 66
        el.append(
            f'<rect x="420" y="{ry}" width="312" height="54" rx="8" fill="{bg_c}" stroke="{fg_c}" stroke-width="1.2"/>'
        )
        el.append(txt(432, ry + 22, r_title, size=11.5, color=fg_c, weight="700"))
        el.append(txt(720, ry + 22, r_rad, size=11, color=INK, anchor="end", weight="700"))
        el.append(txt(432, ry + 42, f"自转速率：{r_spin}", size=10.8, color=BODY))

    el.append(
        f'<rect x="420" y="386" width="312" height="62" rx="8" fill="{AMBER_SOFT}" stroke="#fcd34d"/>'
    )
    el.append(txt(432, 407, "心算验证（③→④ 恒星铁核坍缩为中子星）：", size=11, color=AMBER, weight="700"))
    el.append(txt(432, 427, "半径从 1.2万km 缩至 12km（缩 1,000倍）⇒ 转动惯量 I∝R²", size=10.4, color=BODY))
    el.append(txt(432, 442, "骤降 100 万倍 ⇒ 原本 10天/圈 直接飙到 每秒超 1 圈！", size=10.4, color=INK, weight="600"))

    write_svg(
        "celestial-spin",
        "ice-skater-angular-momentum.svg",
        figure(
            h,
            "角动量守恒驱动星云坍缩起旋与恒星至中子星四级自转加速账本图",
            "左面板展示原始星云因湍流净角动量不为零，在引力坍缩中摊平为原行星盘并令恒星与行星同向自转；右面板列出从分子云、恒星、白矮星到中子星按I∝R²缩小的转速跃升。",
            el,
            extra_defs=_extra_markers(),
        ),
    )


def _build_solar_system_spin_zoo():
    """SVG 2: All 8 Solar System planets drawn at their exact NASA axial obliquities."""
    h = 486
    el = []
    el.extend(
        header(
            "太阳系八大行星“自转怪咖图鉴”：正转、倒转与横躺着滚的星球",
            "按 NASA 实测自转轴倾角（Obliquity）精确绘制：6 颗逆时针正转，唯独金星倒立逆转、天王星横躺打滚",
        )
    )

    el.append(card(16, 68, 728, 402))
    el.append(txt(32, 92, "灰色水平虚线 = 绕太阳公转轨道面；带箭头斜轴 = 北自转轴指向（右手法则拇指朝向）：", size=11.2, color=MUTED))

    # 2 rows x 4 columns of planet cells
    for idx, (p_name, obliq, sid_h, _, _, _, col) in enumerate(PLANETS_SPIN):
        row = idx // 4
        col_i = idx % 4
        bx = 28 + col_i * 178
        by = 106 + row * 136
        is_weird = p_name in ("金星", "天王星")
        box_bg = ORANGE_SOFT if p_name == "金星" else (PURPLE_SOFT if p_name == "天王星" else "#f8fafc")
        box_bd = ORANGE if p_name == "金星" else (PURPLE if p_name == "天王星" else BORDER)

        el.append(
            f'<rect x="{bx}" y="{by}" width="168" height="124" rx="8" fill="{box_bg}" stroke="{box_bd}" stroke-width="{"1.6" if is_weird else "1.1"}"/>'
        )

        cx_p, cy_p = bx + 84, by + 56
        # Orbit plane reference line
        el.append(_line(bx + 18, cy_p, bx + 150, cy_p, color="#cbd5e1", sw=1.2, dash="3 3"))

        # Planet circle
        el.append(f'<circle cx="{cx_p}" cy="{cy_p}" r="20" fill="#ffffff" stroke="{col}" stroke-width="2.0"/>')

        # Spin axis tilted by `obliq` degrees clockwise from straight up (0 deg = straight up, 98 deg = just below horizontal right, 177.4 deg = nearly straight down!)
        rad = math.radians(obliq)
        ax_len = 31.0
        dx = ax_len * math.sin(rad)
        dy = -ax_len * math.cos(rad)
        el.append(_line(cx_p - dx * 0.85, cy_p - dy * 0.85, cx_p + dx, cy_p + dy, color=col, sw=2.0, marker="arr-blue" if col == BLUE else ("arr-orange" if col in (ORANGE, AMBER) else ("arr-purple" if col == PURPLE else "arr-muted"))))

        # Equator line perpendicular to spin axis
        eq_dx = 19.0 * math.cos(rad)
        eq_dy = 19.0 * math.sin(rad)
        el.append(_line(cx_p - eq_dx, cy_p - eq_dy, cx_p + eq_dx, cy_p + eq_dy, color=col, sw=1.3, dash="2 2"))

        # Planet title + exact NASA tilt & period
        tag_t = f"{p_name} · 倾角 {obliq:.1f}°" if obliq >= 0.5 else f"{p_name} · 倾角 0.03°"
        el.append(txt(bx + 10, by + 19, tag_t, size=11.2, color=col if is_weird else INK, weight="700"))

        if abs(sid_h) >= 48:
            per_str = f"自转 {abs(sid_h)/24.0:.1f} 地球日" + ("（逆!）" if sid_h < 0 else "")
        else:
            hh = int(abs(sid_h))
            mm = int(round((abs(sid_h) - hh) * 60))
            per_str = f"自转 {hh}h {mm:02d}m" + ("（横躺!）" if sid_h < 0 else "")
        el.append(txt(cx_p, by + 113, per_str, size=10.6, color=CRIMSON if sid_h < 0 else BODY, anchor="middle", weight="700" if is_weird else "600"))

    # Bottom explanation strip for the two famous rebels (Venus & Uranus)
    el.append(
        f'<rect x="28" y="380" width="346" height="78" rx="8" fill="{ORANGE_SOFT}" stroke="#fdba74"/>'
    )
    el.append(txt(40, 401, "怪咖 ① 金星（倾角 177.4°）：太阳打西边出来！", size=11.3, color=ORANGE, weight="700"))
    el.append(txt(40, 421, "早期巨型撞击 + 92 倍地球气压浓厚大气的“太阳热潮汐力矩”，", size=10.5, color=BODY))
    el.append(txt(40, 440, "把金星搓成了极其缓慢的倒转，赤道自转线速度仅 6.5 km/h（慢跑速）！", size=10.5, color=INK, weight="600"))

    el.append(
        f'<rect x="386" y="380" width="346" height="78" rx="8" fill="{PURPLE_SOFT}" stroke="#d8b4fe"/>'
    )
    el.append(txt(398, 401, "怪咖 ② 天王星（倾角 97.8°）：躺着滚完 84 年！", size=11.3, color=PURPLE, weight="700"))
    el.append(txt(398, 421, "疑被地球级原行星斜撞放倒。虽然每 17.2 小时自转一圈，但南北极", size=10.5, color=BODY))
    el.append(txt(398, 440, "轮流直对太阳：一侧连晒 42 年极昼，另一侧连熬 42 年极夜！", size=10.5, color=INK, weight="600"))

    write_svg(
        "celestial-spin",
        "solar-system-spin-zoo.svg",
        figure(
            h,
            "太阳系八大行星NASA实测自转轴倾角与自转周期全览对比图",
            "按真实倾角绘制水星0.03°、金星177.4°（逆向自转243天）、地球23.4°、火星25.2°、木星3.1°（9小时56分最快）、土星26.7°、天王星97.8°（横躺自转致42年极昼极夜）及海王星28.3°。",
            el,
            extra_defs=_extra_markers(),
        ),
    )


def _build_venus_solar_day_paradox():
    """SVG 3: Why Venus spins once in 243 days (> 224.7d year) yet its sunrise-to-sunrise day is 116.75 days!"""
    h = 474
    el = []
    el.extend(
        header(
            "金星“度日如年”的算术反转：自转一圈 243 天，为什么白天黑夜一轮只要 116.8 天？",
            "恒星日（对遥远恒星转 360°）≠ 太阳日（太阳重回正午）：顺转要多追太阳，逆转反而迎面撞向太阳！",
        )
    )

    # Left Card: Prograde Earth (1/T_sol = 1/T_sid - 1/T_orb)
    el.append(card(16, 68, 350, 390))
    el.append(pill(28, 80, "顺向自转（地球）：公转与自转同为逆时针", fg=BLUE, bg=BLUE_SOFT, w=264, h=24))

    # Sun at left, Earth at two orbital spots
    el.append(f'<circle cx="92" cy="196" r="24" fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="1.8"/>')
    el.append(txt(92, 200, "太阳", size=11.5, color=AMBER, anchor="middle", weight="700"))

    # Orbit arc on right
    el.append(
        f'<path d="M 246 256 A 164 164 0 0 0 246 136" fill="none" stroke="{SLATE}" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#arr-muted)"/>'
    )
    # Bottom Earth (Day 0 noon facing left toward Sun)
    el.append(f'<circle cx="252" cy="240" r="18" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(_line(252, 240, 228, 240, color=CRIMSON, sw=2.0, marker="arr-crimson"))
    el.append(txt(296, 244, "第0天正午", size=10.5, color=BODY))

    # Top Earth after 360 deg sidereal spin (still pointing purely left -> hasn't pointed down-left at Sun yet!)
    el.append(f'<circle cx="252" cy="152" r="18" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(_line(252, 152, 228, 152, color=SLATE, sw=1.5, dash="2 2"))
    el.append(_line(252, 152, 230, 162, color=CRIMSON, sw=2.0, marker="arr-crimson"))
    el.append(txt(302, 148, "转满360°后", size=10.5, color=BLUE, weight="700"))
    el.append(txt(302, 164, "还差约 1°(4分钟)", size=10.2, color=CRIMSON, weight="600"))

    el.append(
        f'<rect x="28" y="284" width="326" height="160" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    el.append(txt(40, 306, "顺转追赶账（公转抵消了一小截自转）：", size=11.3, color=BLUE, weight="700"))
    el.append(txt(40, 329, "• 地球恒星日 T_sid = 23 小时 56 分 04 秒；", size=10.8, color=BODY))
    el.append(txt(40, 350, "• 因一边自转一边逆时针公转，每天要多转约 0.986°", size=10.8, color=BODY))
    el.append(txt(40, 370, "  （多花 3 分 56 秒）才能让太阳重回头顶正午 = 24 小时！", size=10.8, color=INK, weight="600"))
    el.append(txt(40, 395, "• 水星更极端：58.6 天自转配 88 天公转（3:2 共振），", size=10.6, color=MUTED))
    el.append(txt(40, 415, "  在水星上熬过一个昼夜（太阳日），竟要整整 176 地球日", size=10.6, color=MUTED))
    el.append(txt(40, 433, "  ——相当于在水星上“过一天等于过两年”！", size=10.6, color=INK, weight="700"))

    # Right Card: Retrograde Venus (1/T_sol = 1/|T_sid| + 1/T_orb -> 116.75 days!)
    el.append(card(378, 68, 366, 390))
    el.append(pill(390, 80, "逆向自转（金星）：公转逆时针 + 自转顺时针!", fg=ORANGE, bg=ORANGE_SOFT, w=282, h=24))

    vcx, vcy = 561.0, 184.0
    orb_r = 62.0
    el.append(f'<circle cx="{vcx}" cy="{vcy}" r="{orb_r}" fill="none" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
    el.append(f'<circle cx="{vcx}" cy="{vcy}" r="18" fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="1.8"/>')
    el.append(txt(vcx, vcy + 4, "太阳", size=11, color=AMBER, anchor="middle", weight="700"))

    # Position 1: Right (t = 0, red arrow faces left toward Sun = Noon!)
    p1x, p1y = vcx + orb_r, vcy
    el.append(f'<circle cx="{p1x}" cy="{p1y}" r="12" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(_line(p1x, p1y, p1x - 18, p1y, color=CRIMSON, sw=2.0, marker="arr-crimson"))
    el.append(txt(p1x + 18, p1y - 4, "① t = 0 天", size=10.5, color=INK, weight="700"))
    el.append(txt(p1x + 18, p1y + 12, "金星正午", size=10.2, color=ORANGE, weight="600"))

    # Position 2: Top-Left at angle ~ 187 deg CCW! Wait: in 116.75 days, Venus orbits 116.75 / 224.70 * 360 = 187.05 deg CCW!
    # Meanwhile, its red flag rotates CLOCKWISE by 116.75 / 243.02 * 360 = 172.95 deg!
    # Starting from pointing 180 deg (West/Left), rotating 172.95 deg CW makes it point at +7.05 deg (right-upward, straight back at the Sun at center!!)!
    ang_orb = math.radians(187.05)
    p2x = vcx + orb_r * math.cos(ang_orb)
    p2y = vcy - orb_r * math.sin(ang_orb)
    el.append(f'<circle cx="{p2x:.1f}" cy="{p2y:.1f}" r="12" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
    # Vector from p2 back toward Sun (vcx, vcy)
    ux = (vcx - p2x) / orb_r
    uy = (vcy - p2y) / orb_r
    el.append(_line(p2x, p2y, p2x + ux * 18, p2y + uy * 18, color=CRIMSON, sw=2.0, marker="arr-crimson"))
    el.append(txt(p2x - 16, p2y - 6, "② t = 116.8 天", size=10.5, color=INK, anchor="end", weight="700"))
    el.append(txt(p2x - 16, p2y + 10, "重回正午!", size=10.2, color=CRIMSON, anchor="end", weight="700"))

    # Midpoint note at top of orbit (t = 58.4 days = Midnight)
    el.append(txt(vcx, vcy - orb_r - 10, "公转逆时针跑半圈 + 自转顺时针倒半圈 = 半途提前撞见正午!", size=10.2, color=PURPLE, anchor="middle", weight="600"))

    el.append(
        f'<rect x="390" y="284" width="342" height="160" rx="8" fill="{ORANGE_SOFT}" stroke="#fdba74"/>'
    )
    el.append(txt(402, 306, "一行公式统一所有顺转与逆转星球：", size=11.3, color=ORANGE, weight="700"))
    el.append(txt(402, 330, "1 / T_太阳日 = | 1 / T_自转 − 1 / T_公转 |（逆转取负号变相加!）", size=10.8, color=INK, weight="700"))
    el.append(txt(402, 354, "• 代入金星：1 / (-243.0天) − 1 / 224.7天 ⇒ 相加！", size=10.8, color=BODY))
    el.append(txt(402, 376, "• 算出金星太阳日 T_太阳日 = 116.75 地球日（约 58.4 天白昼 +", size=10.8, color=CRIMSON, weight="700"))
    el.append(txt(402, 396, "  58.4 天黑夜）！所以在金星过 1 年（224.7天），能看近两次", size=10.8, color=BODY))
    el.append(txt(402, 416, "  “太阳从西边升起、东边落下”，绝不是网传的“一天比一年长”！", size=10.8, color=INK, weight="600"))

    write_svg(
        "celestial-spin",
        "venus-solar-day-paradox.svg",
        figure(
            h,
            "恒星日与太阳日几何关系及金星243天逆向自转对应116.75天太阳日计算图",
            "左面板展示顺向自转的地球因公转需每天多转约4分钟追赶太阳，以及水星3:2共振导致1太阳日等于176天（2水星年）；右面板按真实角度187.05°公转与172.95°顺时针逆转，严格演示金星每116.75天重回正午。",
            el,
            extra_defs=_extra_markers(),
        ),
    )


def _build_bulge_and_differential_spin():
    """SVG 4: Centrifugal equatorial bulge (Saturn 9.8% oblateness & Chimborazo) + Sun differential rotation."""
    h = 482
    el = []
    el.extend(
        header(
            "自转怎样重塑星球身材？把土星甩扁近 10%，把太阳磁场拧成“麻花”",
            "左看离心力如何把旋转星球甩成赤道鼓起的扁球；右看流体太阳“赤道快、两极慢”的较差自转",
        )
    )

    # Left Card: Oblateness comparison (Earth vs Jupiter vs Saturn at exact 1 : 0.902 ratio!)
    el.append(card(16, 68, 362, 398))
    el.append(pill(28, 80, "离心扁率 f = (赤道半径 − 极半径) / 赤道半径", fg=TEAL, bg=TEAL_SOFT, w=292, h=24))

    # Draw Saturn's exact 1 : 0.902 oblate silhouette vs dashed perfect circle!
    scx, scy = 197.0, 194.0
    rx_sat = 63.0
    ry_sat = rx_sat * (54364.0 / 60268.0)  # 56.83 px (exact NASA 0.90204 ratio!)
    el.append(f'<circle cx="{scx}" cy="{scy}" r="{rx_sat}" fill="none" stroke="{CRIMSON}" stroke-width="1.3" stroke-dasharray="4 3"/>')
    el.append(
        f'<ellipse cx="{scx}" cy="{scy}" rx="{rx_sat:.1f}" ry="{ry_sat:.2f}" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="2.2"/>'
    )
    # Subtle ring line
    el.append(_line(scx - 116, scy, scx + 116, scy, color=AMBER, sw=2.2))
    el.append(txt(scx, scy - 8, "土星真实扁率轮廓", size=11, color=TEAL, anchor="middle", weight="700", halo=True))
    el.append(txt(scx, scy + 16, "10.7 小时转一圈 · 扁率 9.8%!", size=10.5, color=INK, anchor="middle", weight="600", halo=True))
    el.append(txt(scx, scy - rx_sat - 8, "红色虚线 = 假想正球体（两极被压矮整整 5,904 km!）", size=10.2, color=CRIMSON, anchor="middle", weight="600"))

    # Three-planet quantitative comparison cards
    rows_ob = [
        ("地球（岩石刚度高，24h/圈）", "赤道比极半径鼓出 21.3 km（扁率 0.335%）", BLUE),
        ("木星（气态狂转，9.9h/圈）", "赤道比极半径鼓出 4,638 km（扁率 6.49%）", AMBER),
        ("土星（密度低于水，10.7h/圈）", "赤道比极半径鼓出 5,904 km（扁率 9.80% 冠军!）", TEAL),
    ]
    for idx, (r_head, r_val, r_col) in enumerate(rows_ob):
        ry = 272 + idx * 44
        el.append(f'<rect x="28" y="{ry}" width="338" height="38" rx="6" fill="#f8fafc" stroke="{BORDER}"/>')
        el.append(txt(38, ry + 16, r_head, size=10.6, color=r_col, weight="700"))
        el.append(txt(38, ry + 32, r_val, size=10.3, color=BODY))

    el.append(
        txt(
            28,
            424,
            "趣味彩蛋：正因地球赤道鼓起 21.3 km，南美赤道附近的钦博拉索山",
            size=10.4,
            color=INK,
            weight="600",
        )
    )
    el.append(
        txt(
            28,
            443,
            "（海拔 6,263 m）离地心的真实距离，反倒比珠穆朗玛峰还要远约 2.1 km！",
            size=10.4,
            color=BLUE,
            weight="700",
        )
    )

    # Right Card: Sun Differential Rotation & Magnetic Winding (x=390..744)
    el.append(card(390, 68, 354, 398))
    el.append(pill(402, 80, "较差自转：气体与等离子体星球不按整块转！", fg=ORANGE, bg=ORANGE_SOFT, w=288, h=24))

    # Draw Sun disk with NASA latitude periods & stretched magnetic meridian!
    sun_cx, sun_cy, sun_r = 524.0, 214.0, 78.0
    el.append(f'<circle cx="{sun_cx}" cy="{sun_cy}" r="{sun_r}" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2.0"/>')
    el.append(_line(sun_cx, sun_cy - sun_r - 12, sun_cx, sun_cy + sun_r + 12, color=SLATE, sw=1.3, dash="3 2"))

    # Initial straight meridian (dashed grey) vs wound magnetic field line (crimson curve bowing far right at equator!)
    el.append(
        f'<path d="M {sun_cx:.1f} {sun_cy - sun_r:.1f} Q {sun_cx - 26:.1f} {sun_cy:.1f} {sun_cx:.1f} {sun_cy + sun_r:.1f}" '
        f'fill="none" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="3 3"/>'
    )
    el.append(
        f'<path d="M {sun_cx:.1f} {sun_cy - sun_r:.1f} C {sun_cx + 8:.1f} {sun_cy - 48:.1f}, {sun_cx + 68:.1f} {sun_cy - 18:.1f}, {sun_cx + 68:.1f} {sun_cy:.1f} '
        f'C {sun_cx + 68:.1f} {sun_cy + 18:.1f}, {sun_cx + 8:.1f} {sun_cy + 48:.1f}, {sun_cx:.1f} {sun_cy + sun_r:.1f}" '
        f'fill="none" stroke="{CRIMSON}" stroke-width="2.3"/>'
    )

    # Latitude speed arrows & exact NASA period labels on the right
    lats = [
        (-66, "极区 (≈80°–90°)", "≈ 34.4 天/圈（慢）", SLATE, 18),
        (-36, "中纬 (45°)", "≈ 27.9 天/圈", AMBER, 34),
        (0, "赤道 (0°)", "25.05 天/圈（最快!）", CRIMSON, 56),
        (36, "南纬 45°", "≈ 27.9 天/圈", AMBER, 34),
    ]
    for dy_l, l_name, l_per, l_col, arr_w in lats:
        ly = sun_cy + dy_l
        el.append(_line(sun_cx - 24, ly, sun_cx - 24 + arr_w, ly, color=l_col, sw=1.8, marker="arr-crimson" if l_col == CRIMSON else "arr-orange"))
        el.append(txt(sun_cx + sun_r + 12, ly - 2, l_name, size=10.3, color=INK, weight="700"))
        el.append(txt(sun_cx + sun_r + 12, ly + 13, l_per, size=10.0, color=l_col, weight="600"))

    el.append(
        f'<rect x="402" y="316" width="330" height="134" rx="8" fill="{AMBER_SOFT}" stroke="#fcd34d"/>'
    )
    el.append(txt(414, 338, "较差自转的蝴蝶效应：11 年太阳黑子与耀斑周期", size=11.3, color=AMBER, weight="700"))
    el.append(txt(414, 360, "• 地球是坚硬岩石，北京与赤道角速度严格相等（同为 24h）；", size=10.6, color=BODY))
    el.append(txt(414, 380, "• 太阳是沸腾等离子体球，赤道每转 3.5 圈就比两极多套 1 圈！", size=10.6, color=INK, weight="600"))
    el.append(txt(414, 401, "• 冻结在等离子体里的南北向磁力线（红线）被赤道越拽越长，", size=10.6, color=BODY))
    el.append(txt(414, 421, "  像缠毛线一样绕着赤道拧成强磁绳，浮出表面便炸开太阳黑子", size=10.6, color=BODY))
    el.append(txt(414, 439, "  与日冕物质抛射（木星大红斑与彩带云系同理受快自转塑造）。", size=10.4, color=MUTED))

    write_svg(
        "celestial-spin",
        "centrifugal-bulge-and-differential-spin.svg",
        figure(
            h,
            "自转离心扁率（地球、木星与土星9.8%扁率真实比例）及太阳纬度较差自转扭曲磁力线图",
            "左面板按真实比例绘制土星9.8%扁率椭圆与正圆对比，列出地球（21.3 km，钦博拉索山离地心最远）、木星（4,638 km）、土星（5,904 km）赤道隆起；右面板按NASA公式展示太阳赤道25.05天与极区34.4天较差自转缠绕磁力线机制。",
            el,
            extra_defs=_extra_markers(),
        ),
    )


def _build_tidal_locking_and_brake():
    """SVG 5: Moon 1:1 tidal locking (with 1-shot accessible CSS comparison animation) & Earth's slowing day."""
    h = 486
    anim_css = """
      @keyframes tl-orbit {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(-360deg); }
      }
      @keyframes tl-counter {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      .tl-locked-arm {
        transform-origin: 112px 218px;
        animation: tl-orbit 8s ease-in-out 0.3s 1 forwards;
      }
      .tl-nospin-arm {
        transform-origin: 294px 218px;
        animation: tl-orbit 8s ease-in-out 0.3s 1 forwards;
      }
      .tl-keep-upright {
        transform-origin: 294px 158px;
        animation: tl-counter 8s ease-in-out 0.3s 1 forwards;
      }
      @media (prefers-reduced-motion: reduce) {
        .tl-locked-arm, .tl-nospin-arm, .tl-keep-upright {
          animation: none !important;
          transform: none !important;
        }
      }
    """
    el = []
    el.extend(
        header(
            "月球永远拿“正脸”看地球，是因为它不自转吗？潮汐锁定与地球刹车",
            "左看单次对照动画：不自转反而会露出后脑勺；右看海洋潮汐摩擦如何把地球每天拖慢、把月球推远",
        )
    )

    # Left Card: True 1:1 Spin-Orbit Lock vs Hypothetical Zero-Spin (x=16..392)
    el.append(card(16, 68, 376, 402))
    el.append(pill(28, 80, "破解直觉误区：为什么“永远露正脸”恰恰证明月球在自转？", fg=BLUE, bg=BLUE_SOFT, w=348, h=24))

    # Sub-panel A: Real Moon (1:1 Locked, center 112, 218, r=60)
    cx1, cy1, r_m = 112.0, 218.0, 60.0
    el.append(txt(cx1, 130, "✅ 真实月球：公转1圈 = 自转1圈", size=11, color=GREEN, anchor="middle", weight="700"))
    el.append(f'<circle cx="{cx1}" cy="{cy1}" r="{r_m}" fill="none" stroke="{GREEN}" stroke-width="1.3" stroke-dasharray="4 3"/>')
    el.append(f'<circle cx="{cx1}" cy="{cy1}" r="14" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
    el.append(txt(cx1, cy1 + 4, "地球", size=10, color=BLUE, anchor="middle", weight="700"))

    # Ghost static quarter-orbit moons showing red dot ALWAYS inward toward Earth!
    for ang_d, op_g in [(90, "0.35"), (180, "0.35"), (270, "0.35")]:
        ar = math.radians(ang_d)
        mx = cx1 + r_m * math.sin(ar)
        my = cy1 - r_m * math.cos(ar)
        dx_in = -9.0 * math.sin(ar)
        dy_in = 9.0 * math.cos(ar)
        el.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="10" fill="{GREEN_SOFT}" stroke="{GREEN}" opacity="{op_g}"/>')
        el.append(f'<circle cx="{mx + dx_in:.1f}" cy="{my + dy_in:.1f}" r="3.2" fill="{CRIMSON}" opacity="0.65"/>')

    # Animated locked arm (starts at top: 112, 158; red dot at bottom of moon 112, 167 facing Earth!)
    el.append(
        f'<g class="tl-locked-arm">'
        f'<circle cx="{cx1}" cy="{cy1 - r_m}" r="11" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>'
        f'<circle cx="{cx1}" cy="{cy1 - r_m + 8.5}" r="3.6" fill="{CRIMSON}"/>'
        f'</g>'
    )
    el.append(txt(cx1, 302, "红点（正面）每走 1/4 圈", size=10.3, color=BODY, anchor="middle"))
    el.append(txt(cx1, 318, "自身也同步转过 90° ⇒ 永远朝地!", size=10.3, color=GREEN, anchor="middle", weight="700"))

    # Sub-panel B: Hypothetical Non-Rotating Moon (center 294, 218, r=60)
    cx2, cy2 = 294.0, 218.0
    el.append(txt(cx2, 130, "❌ 假如不自转：半个月就露背面!", size=11, color=CRIMSON, anchor="middle", weight="700"))
    el.append(f'<circle cx="{cx2}" cy="{cy2}" r="{r_m}" fill="none" stroke="{CRIMSON}" stroke-width="1.3" stroke-dasharray="4 3"/>')
    el.append(f'<circle cx="{cx2}" cy="{cy2}" r="14" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
    el.append(txt(cx2, cy2 + 4, "地球", size=10, color=BLUE, anchor="middle", weight="700"))

    # Ghost static quarter-orbit moons with red dot ALWAYS pointing straight DOWN (fixed in space)!
    for ang_d in (90, 180, 270):
        ar = math.radians(ang_d)
        mx = cx2 + r_m * math.sin(ar)
        my = cy2 - r_m * math.cos(ar)
        el.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="10" fill="{CRIMSON_SOFT}" stroke="{CRIMSON}" opacity="0.35"/>')
        el.append(f'<circle cx="{mx:.1f}" cy="{my + 8.5:.1f}" r="3.2" fill="{CRIMSON}" opacity="0.65"/>')

    # Animated non-rotating moon (arm rotates -360, inner moon counter-rotates +360 so red dot stays pointing south!)
    el.append(
        f'<g class="tl-nospin-arm"><g class="tl-keep-upright">'
        f'<circle cx="{cx2}" cy="{cy2 - r_m}" r="11" fill="{CRIMSON_SOFT}" stroke="{CRIMSON}" stroke-width="1.8"/>'
        f'<circle cx="{cx2}" cy="{cy2 - r_m + 8.5}" r="3.6" fill="{CRIMSON}"/>'
        f'</g></g>'
    )
    el.append(txt(cx2, 302, "红点死指宇宙同一方向：", size=10.3, color=BODY, anchor="middle"))
    el.append(txt(cx2, 318, "走到下方时地球直接看见月背!", size=10.3, color=CRIMSON, anchor="middle", weight="700"))

    el.append(
        f'<rect x="28" y="336" width="352" height="120" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    el.append(txt(40, 358, "潮汐锁定的本质（宇宙大卫星的共同宿命）：", size=11.2, color=INK, weight="700"))
    el.append(txt(40, 379, "• 早期月球自转飞快，地球引力把月球拉成微凸的“橄榄球”；", size=10.5, color=BODY))
    el.append(txt(40, 398, "• 岩石反复揉搓发热耗散动能，直到隆起端死死对准地球（27.32天", size=10.5, color=BODY))
    el.append(txt(40, 417, "  转一圈 = 公转一圈）才停止摩擦；木星、土星的大卫星也全被锁定！", size=10.5, color=INK, weight="600"))
    el.append(txt(40, 439, "  （注：天平动让我们累计能偷瞄到约 59% 的月面；支持减少动态效果）", size=10.0, color=MUTED))

    # Right Card: Earth's Tidal Brake & Receding Moon (x=404..744)
    el.append(card(404, 68, 340, 402))
    el.append(pill(416, 80, "地球也在被月球刹车：恐龙时代一年有 370 多天！", fg=ORANGE, bg=ORANGE_SOFT, w=314, h=24))

    # Diagram of Earth's forward-dragged ocean tidal bulge pulling Moon ahead!
    ecx, ecy = 516.0, 198.0
    mcx, mcy = 684.0, 198.0
    # Earth-Moon center line
    el.append(_line(ecx, ecy, mcx, mcy, color=SLATE, sw=1.2, dash="3 3"))
    # Tilted ocean tidal ellipse (+18 deg ahead CCW because Earth spins in 24h << 27.3d!)
    el.append(
        f'<g transform="rotate(-20 {ecx} {ecy})">'
        f'<ellipse cx="{ecx}" cy="{ecy}" rx="54" ry="34" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>'
        f'</g>'
    )
    el.append(f'<circle cx="{ecx}" cy="{ecy}" r="28" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
    el.append(txt(ecx, ecy - 2, "地球快转", size=10.2, color=INK, anchor="middle", weight="700"))
    el.append(txt(ecx, ecy + 13, "24h 逆时针", size=9.8, color=BLUE, anchor="middle", weight="600"))
    el.append(txt(ecx + 38, ecy - 34, "海水涨潮隆起被", size=10, color=BLUE, weight="700"))
    el.append(txt(ecx + 38, ecy - 20, "海床摩擦往前带偏!", size=10, color=BLUE, weight="700"))

    # Moon on right + forward orbital boost arrow
    el.append(f'<circle cx="{mcx}" cy="{mcy}" r="14" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.8"/>')
    el.append(txt(mcx, mcy + 4, "月", size=10.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(_line(mcx, mcy - 18, mcx, mcy - 54, color=GREEN, sw=2.0, marker="arr-green"))
    el.append(txt(mcx - 6, mcy - 60, "被斜前隆起往前拽", size=10, color=GREEN, anchor="end", weight="700"))
    el.append(txt(mcx + 16, mcy + 28, "每年远离 ≈3.8cm", size=10, color=ORANGE, anchor="end", weight="700"))

    # Fossil coral & NIST leap-second timeline box
    el.append(
        f'<rect x="416" y="276" width="316" height="180" rx="8" fill="{AMBER_SOFT}" stroke="#fcd34d"/>'
    )
    el.append(txt(428, 298, "铁证如山的地球“慢动作回放”（总角动量守恒）：", size=11.2, color=AMBER, weight="700"))
    el.append(txt(428, 320, "• 海底摩擦拖慢地球自转，损失的自转角动量传给月球公转，", size=10.5, color=BODY))
    el.append(txt(428, 339, "  阿波罗激光角反射器实测月球正以每年约 3.8 cm 螺旋远离；", size=10.5, color=BODY))
    el.append(txt(428, 361, "• 4 亿年前泥盆纪珊瑚化石日生长纹显示：当时一年约 400 天，", size=10.5, color=INK, weight="700"))
    el.append(txt(428, 380, "  地球转一圈只要 21.9 小时！近几百年平均每世纪变长约 1.4–", size=10.5, color=BODY))
    el.append(txt(428, 399, "  1.8 毫秒（1972 年以来原子钟已累计插入 27 次“闰秒”）；", size=10.5, color=BODY))
    el.append(txt(428, 421, "• 严谨补记：地核—地幔耦合与冰川融化偶尔会带来毫秒级短期", size=10.2, color=MUTED))
    el.append(txt(428, 439, "  波动（如 2022 年 6 月 29 日曾比 24h 短了 1.59 毫秒，NIST）。", size=10.2, color=MUTED))

    write_svg(
        "celestial-spin",
        "tidal-locking-and-moon-brake.svg",
        figure(
            h,
            "月球1:1同步自转潮汐锁定对照动画及地月潮汐摩擦导致地球变慢月球远离机制图",
            "左面板对比真实月球（公转一圈自转一圈，红点始终朝向地球）与假想不自转月球（红点朝向固定星空，半月后露出背面）；右面板展示地球快自转将海水潮汐隆起带偏超前，反向刹慢地球（泥盆纪一天21.9小时）并以每年约3.8厘米推远月球。",
            el,
            extra_css=anim_css,
            extra_defs=_extra_markers(),
        ),
    )


def _build_cosmic_spin_limits():
    """SVG 6: Cosmic spin speed benchmark & centrifugal breakup limit up to 716 Hz pulsar PSR J1748-2446ad."""
    h = 482
    el = []
    el.extend(
        header(
            "宇宙自转的终极狂飙：星球转太快会散架吗？从慢跑金星到每秒 716 圈脉冲星",
            "向心引力 GM/R² 必须拽住离心加速度 ω²R：一旦越过解体红线星球当场崩飞，中子星赤道飙至 24% 光速",
        )
    )

    el.append(card(16, 68, 728, 398))
    el.append(pill(28, 80, "天体赤道自转线速度跨度榜（横跨 7 个数量级的对数标尺！）", fg=PURPLE, bg=PURPLE_SOFT, w=366, h=24))
    el.append(txt(406, 96, "解体极限周期 T_min = 2π√(R³ / GM)", size=11.2, color=CRIMSON, weight="700"))

    # 6 horizontal log-scaled benchmark bars
    benchmarks = [
        (
            "金星赤道",
            "1.81 m/s（6.5 km/h）",
            "比普通人慢跑还慢！在金星赤道迎着西边散步就能让日落永远停在半空",
            48,
            SLATE,
            SLATE_SOFT,
        ),
        (
            "地球赤道",
            "465.1 m/s（1,674 km/h）",
            "超音速 1.36 倍（文昌发射火箭白捡这笔顺风速度；若缩至 84.5 分钟/圈地球将解体!）",
            174,
            BLUE,
            BLUE_SOFT,
        ),
        (
            "木星赤道",
            "12.57 km/s（4.53 万 km/h）",
            "太阳系行星自转冠军（9小时56分转完 45 万公里腰围，比地球第一宇宙速度还快）",
            306,
            TEAL,
            TEAL_SOFT,
        ),
        (
            "大质量狂转星 VFTS 102",
            "≈ 500–600 km/s",
            "大麦哲伦云恒星测速纪录保持者，已被离心力甩成扁橄榄球，赤道物质正往外甩盘",
            458,
            ORANGE,
            ORANGE_SOFT,
        ),
        (
            "脉冲星 PSR J1748-2446ad",
            "≈ 72,000 km/s（0.24 c!）",
            "直径不足 32 km 的中子星每秒狂转 716 圈（快过料理机刀片），赤道逼近四分之一光速！",
            644,
            PURPLE,
            PURPLE_SOFT,
        ),
    ]

    for idx, (b_name, b_spd, b_desc, bar_w, fg_c, bg_c) in enumerate(benchmarks):
        ry = 118 + idx * 54
        el.append(f'<rect x="28" y="{ry}" width="704" height="44" rx="7" fill="#f8fafc" stroke="{BORDER}"/>')
        el.append(f'<rect x="28" y="{ry}" width="{bar_w}" height="44" rx="7" fill="{bg_c}" stroke="{fg_c}" stroke-width="1.2"/>')
        el.append(txt(40, ry + 18, b_name, size=11.3, color=fg_c, weight="700", halo=True))
        el.append(txt(720, ry + 18, b_spd, size=11.3, color=INK, anchor="end", weight="700", halo=True))
        el.append(txt(40, ry + 36, b_desc, size=10.3, color=BODY, halo=True))

    # Bottom synthesis box: Why doesn't PSR J1748-2446ad fly apart, and what happens for Kerr Black Holes?
    el.append(
        f'<rect x="28" y="394" width="704" height="58" rx="8" fill="{CRIMSON_SOFT}" stroke="#fca5a5"/>'
    )
    el.append(
        txt(
            40,
            415,
            "为什么中子星每秒转 716 圈都不散架？因为它的密度超原子核（每立方厘米上亿吨），表面引力是地球的千亿倍！",
            size=10.8,
            color=CRIMSON,
            weight="700",
        )
    )
    el.append(
        txt(
            40,
            436,
            "而若再坍缩成“克尔旋转黑洞（Kerr Black Hole）”，连实体表面都消失了——高速自转甚至会把周围的时空本身一起拽着旋转（参考系拖拽）！",
            size=10.5,
            color=INK,
            weight="600",
        )
    )

    write_svg(
        "celestial-spin",
        "cosmic-spin-limits.svg",
        figure(
            h,
            "宇宙天体赤道自转线速度对数跨度榜与离心解体极限（金星至每秒716圈脉冲星）图",
            "对数尺度对比金星（1.81 m/s）、地球（465.1 m/s，解体极限周期84.5分钟）、木星（12.57 km/s）、高速恒星VFTS 102（约500-600 km/s）与最快毫秒脉冲星PSR J1748-2446ad（每秒716圈，赤道约0.24倍光速）及旋转黑洞参考系拖拽。",
            el,
            extra_defs=_extra_markers(),
        ),
    )


@register("celestial-spin", "Angular momentum origin, 8-planet spin zoo, Venus solar day, oblateness & Sun differential spin, tidal locking, and 716 Hz pulsar", "science")
def build_celestial_spin():
    _verify_celestial_spin_math()
    _build_angular_momentum_origin()
    _build_solar_system_spin_zoo()
    _build_venus_solar_day_paradox()
    _build_bulge_and_differential_spin()
    _build_tidal_locking_and_brake()
    _build_cosmic_spin_limits()
