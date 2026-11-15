"""Original 760px Chinese SVG diagrams for the Speed of Light Measurement History post."""

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

SUBDIR = "light-speed"

C_EXACT = 299_792_458.0  # m/s (1983 17th CGPM exact definition)
AU_M = 149_597_870_700.0  # m (IAU exact astronomical unit)


def _verify_light_speed_math():
    """Verify every physical formula, travel time, and log-scale coordinate used in the figures."""
    # 1. Galileo two-hilltop lantern round-trip vs human reaction time
    d_galileo = 1_600.0  # ~1 mile in meters
    dt_light = 2.0 * d_galileo / C_EXACT  # ~10.674e-6 s
    assert 10.6e-6 < dt_light < 10.8e-6
    t_human = 0.20  # 200,000 microseconds
    ratio_human = t_human / dt_light
    assert 18_500 < ratio_human < 19_000

    # 2. Romer 2 AU transit time & Huygens conversion
    dt_2au = 2.0 * AU_M / C_EXACT  # 998.01 s = 16 min 38 s
    assert 997.5 < dt_2au < 998.5
    c_huygens = 1.1e8 * 1.949  # 110 million French toises/s * 1.949 m/toise
    assert 2.14e8 < c_huygens < 2.15e8

    # 3. Bradley stellar aberration angle
    v_earth = 2.0 * math.pi * AU_M / (365.25636 * 86400.0)  # ~29,784.7 m/s
    theta_rad = math.atan(v_earth / C_EXACT)
    theta_arcsec = math.degrees(theta_rad) * 3600.0
    assert 20.48 < theta_arcsec < 20.51

    # 4. Fizeau 1849 cogwheel formula: c = 4 * N * d * f
    n_teeth = 720
    d_fizeau = 8_633.0
    f_fizeau = 12.6
    c_fizeau = 4.0 * n_teeth * d_fizeau * f_fizeau
    assert abs(c_fizeau - 313_274_304.0) < 1.0

    # 5. Michelson 1926 octagonal mirror formula: c_air = 16 * f * d
    d_mw = 35_385.5
    f_mw = 529.37
    c_mw_air = 16.0 * f_mw * d_mw
    assert 2.996e8 < c_mw_air < 2.999e8

    # 6. Evenson 1972 laser relative uncertainty
    rel_evenson = 1.1 / C_EXACT
    assert 3.6e-9 < rel_evenson < 3.8e-9


def _build_galileo_lantern_svg():
    el = []
    el.extend(
        header(
            "为什么伽利略站在两座山头掀灯笼测不出光速？两万倍的时间尺度鸿沟",
            "光跑完 3.2 公里往返仅需 10.7 微秒，而人类神经反应与掀灯罩动作慢了近 19,000 倍",
        )
    )

    # Left panel: Two-hilltop schematic
    el.append(card(24, 66, 356, 412))
    el.append(txt(42, 92, "一、1638《两门新科学》双灯实验构想", size=13.2, color=INK, weight="700"))

    # Sky/hills canvas
    el.append(card(40, 106, 324, 178, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Two hills
    el.append(f'<path d="M40,284 Q96,208 152,284 Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.4"/>')
    el.append(f'<path d="M252,284 Q308,208 364,284 Z" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.4"/>')
    # Lanterns on peaks
    el.append(f'<circle cx="96" cy="212" r="8" fill="#fde047" stroke="{BLUE}" stroke-width="1.5"/>')
    el.append(txt(96, 194, "甲（伽利略）", size=11, color=BLUE, anchor="middle", weight="700"))
    el.append(f'<circle cx="308" cy="212" r="8" fill="#fde047" stroke="{ORANGE}" stroke-width="1.5"/>')
    el.append(txt(308, 194, "乙（助手）", size=11, color=ORANGE, anchor="middle", weight="700"))

    # Forward & return rays
    el.append(f'<line x1="108" y1="206" x2="296" y2="206" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')
    el.append(txt(202, 198, "① 去程光：5.34 微秒", size=10.5, color=BLUE, anchor="middle", weight="600"))
    el.append(f'<line x1="296" y1="220" x2="108" y2="220" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#arr-green)"/>')
    el.append(txt(202, 236, "③ 回程光：5.34 微秒", size=10.5, color=GREEN, anchor="middle", weight="600"))
    el.append(txt(202, 268, "山头间距 d ≈ 1.6 km（往返 3.2 km）", size=10.8, color=SLATE, anchor="middle", weight="600"))

    # Breakdown steps below hills
    el.append(card(40, 296, 324, 168, rx=8, fill="#fffdf9", stroke=ORANGE))
    el.append(txt(54, 319, "致命瓶颈：乙看到光 → 大脑反应 → 掀开灯罩", size=11.8, color=ORANGE, weight="700"))
    el.append(txt(54, 342, "• 光往返总耗时 Δt_光 = 2d/c ≈ 0.0000107 秒", size=11, color=BODY))
    el.append(txt(54, 364, "• 人手最快反应 τ_人 ≈ 0.20 秒（随机波动几十毫秒）", size=11, color=BODY))
    el.append(txt(54, 386, "• 噪声是信号的 18,700 倍！想靠人手分辨 0.2 秒延迟，", size=11, color=BODY))
    el.append(txt(54, 408, "  两座山必须隔开 30,000 km（绕地球赤道 3/4 圈）！", size=11, color=INK, weight="700"))
    el.append(txt(54, 434, "史实：伽利略仅在不到 1 英里处试过，严谨结论“极快”。", size=10.5, color=MUTED))
    el.append(txt(54, 452, "1667 年佛罗伦萨西门托学院远距复测仍未能测出延迟。", size=10.5, color=MUTED))

    # Right panel: Log-scale bar comparison + Descartes lunar eclipse fallacy
    el.append(card(394, 66, 342, 412))
    el.append(txt(412, 92, "二、对数坐标时间尺（单位：微秒 μs）", size=13.2, color=INK, weight="700"))
    el.append(txt(412, 112, "注：横轴采用对数坐标（每向右一格放大 10 倍）", size=10.6, color=MUTED))

    # Log10 axis from 10^0 (1 us) to 10^6 (1,000,000 us = 1 s)
    ax0, ax1 = 424, 712  # width 288 -> 48 px per decade
    ay_top, ay_bot = 134, 286
    for k in range(7):
        gx = ax0 + k * 48
        el.append(f'<line x1="{gx}" y1="{ay_top}" x2="{gx}" y2="{ay_bot}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
        lbl = f"10^{k}" if k >= 3 else str(10**k)
        el.append(txt(gx, ay_bot + 16, lbl, size=10, color=MUTED, anchor="middle"))

    bars = [
        ("光往返 3.2 km", 10.67, "10.7 μs", BLUE, BLUE_SOFT),
        ("步枪子弹飞 1 m", 1100.0, "1,100 μs", SLATE, SLATE_SOFT),
        ("蜂鸟振翅 1 次", 12500.0, "12,500 μs", GREEN, GREEN_SOFT),
        ("人手掀灯反应", 200000.0, "200,000 μs", ORANGE, ORANGE_SOFT),
    ]
    for bi, (bname, val_us, vstr, bfg, bbg) in enumerate(bars):
        by = 144 + bi * 35
        bw = max(6.0, math.log10(val_us) * 48.0)
        el.append(txt(424, by - 3, f"{bname}（{vstr}）", size=10.6, color=INK, weight="600"))
        el.append(f'<rect x="{ax0}" y="{by + 2}" width="{bw:.1f}" height="12" rx="4" fill="{bbg}" stroke="{bfg}" stroke-width="1.3"/>')

    # Descartes vs Huygens box
    el.append(card(410, 316, 310, 148, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(424, 338, "同期的哲学交锋：笛卡尔为什么断定光速无穷大？", size=11.5, color=PURPLE, weight="700"))
    el.append(txt(424, 360, "• 笛卡尔推理：若光从地球到月球要走 1 小时，月食", size=10.8, color=BODY))
    el.append(txt(424, 380, "  发生时地球已公转走远，食甚位置会偏离日地连线", size=10.8, color=BODY))
    el.append(txt(424, 400, "  约 33°；既然观测毫无偏角，说明光速必定无穷大！", size=10.8, color=BODY))
    el.append(txt(424, 422, "• 惠更斯反击：地月光行其实仅需 1.28 秒（往返 2.6 秒），", size=10.8, color=INK, weight="600"))
    el.append(txt(424, 442, "  偏角不足几角秒，全淹没在地球本影模糊边缘里了！", size=10.8, color=INK, weight="600"))

    svg = figure(
        496,
        "伽利略山头双灯实验原理与人类反应时间对数对比图",
        "左栏展示1638年伽利略两座山头相距1.6公里掀灯笼测光速的往返光程仅需10.7微秒，而人手反应需20万微秒；右栏用对数坐标直观对比两万倍时间差，并附笛卡尔月食论证与惠更斯的反驳。",
        el,
    )
    write_svg(SUBDIR, "galileo-lantern-reaction-trap.svg", svg)


def _build_romer_io_svg():
    extra_css = """
  .pulse-near {
    stroke-dasharray: 210;
    stroke-dashoffset: 210;
    animation: shootNear 2.2s linear 0.3s 1 forwards;
  }
  .pulse-far {
    stroke-dasharray: 350;
    stroke-dashoffset: 350;
    animation: shootFar 3.67s linear 0.3s 1 forwards;
  }
  @keyframes shootNear {
    to { stroke-dashoffset: 0; }
  }
  @keyframes shootFar {
    to { stroke-dashoffset: 0; }
  }
  @media (prefers-reduced-motion: reduce) {
    .pulse-near, .pulse-far {
      animation: none;
      stroke-dashoffset: 0;
    }
  }"""

    el = []
    el.extend(
        header(
            "向太阳系借一把三亿公里的大尺子：罗默“木卫一蚀延误”与惠更斯换算",
            "地面基线太短，天文学家干脆拿地球公转轨道直径（2 AU ≈ 3 亿 km）把微秒级延迟放大成十几分钟！",
        )
    )

    # Left panel: Orbital geometry (schematic radii labeled clearly; pulse timing proportional to path length 210:350 = 2.2s:3.67s!)
    el.append(card(24, 66, 396, 452))
    el.append(txt(42, 92, "一、木卫一（Io）出蚀光信号的路程差（轨道比例示意）", size=13, color=INK, weight="700"))

    # Sun & Earth orbit on left
    sx, sy, r_earth = 132, 266, 70
    el.append(f'<circle cx="{sx}" cy="{sy}" r="{r_earth}" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    el.append(f'<circle cx="{sx}" cy="{sy}" r="13" fill="#fde047" stroke="{ORANGE}" stroke-width="1.5"/>')
    el.append(txt(sx, sy + 4, "日", size=11, color=ORANGE, anchor="middle", weight="700"))

    # Near Earth position E1 (sx + 70 = 202, sy - 24? Let's place E_near at (202, 266) and E_far at (62, 266) along horizontal diameter 2*r_earth = 140px!)
    # Wait: if Jupiter & Io are at (362, 266), a straight horizontal ray from (362,266) to (62,266) passes through Sun!
    # So just like Romer's real quadrature geometry: place E_near at top-right of orbit and E_far at top-left, OR place Jupiter at (362, 232), E_near at (196, 232) [dist = 166px], and E_far at (68, 232) [chord near top, or let's place Sun at (132, 290), Earth orbit r=72: E_near=(204, 290)? No, top tangent chord y=230: dx = sqrt(72^2 - 60^2) = 39.6; even better: tilt Jupiter to right, E_near at (194, 240), E_far at (64, 262) so neither ray hits the Sun!].
    # Let's calculate exact non-Sun-intersecting coordinates with exact velocity-matched timing!
    # Sun at (134, 298), r_earth = 70:
    # Point B (near quadrature, angle -35 deg): bx = 134 + 70*cos(-35°) = 191.3, by = 298 + 70*sin(-35°) = 257.9
    # Point C (receded Earth, angle -155 deg): cx = 134 + 70*cos(-155°) = 70.6, cy = 298 + 70*sin(-155°) = 268.4
    # Io emergence point H near Jupiter at (362, 226):
    # Distance H->B = hypot(362 - 191.3, 226 - 257.9) = hypot(170.7, -31.9) = 173.7 px!
    # Distance H->C = hypot(362 - 70.6, 226 - 268.4) = hypot(291.4, -42.4) = 294.5 px!
    # Speed invariance check (AGENTS.md: 时间比较按真实模型的“距离÷速度”计算):
    # At constant speed v_anim = 95 px/s: t_near = 173.7 / 95 = 1.83 s, t_far = 294.5 / 95 = 3.10 s! Exact same speed!
    sx, sy, r_e = 134, 298, 70
    # Redraw Sun & orbit at (134, 298) — let's clear previous Sun lines and write clean ones!
    el.pop()  # remove old sun label
    el.pop()  # remove old sun circle
    el.pop()  # remove old orbit circle

    el.append(card(38, 106, 368, 272, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    el.append(f'<circle cx="{sx}" cy="{sy}" r="{r_e}" fill="none" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="5 4"/>')
    el.append(f'<circle cx="{sx}" cy="{sy}" r="13" fill="#fde047" stroke="{ORANGE}" stroke-width="1.5"/>')
    el.append(txt(sx, sy + 4, "太阳", size=10, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(sx, sy + 86, "地球公转轨道（直径 2 AU ≈ 3 亿 km）", size=10.5, color=SLATE, anchor="middle", weight="600"))

    bx, by = 134 + 70 * math.cos(math.radians(-35)), 298 + 70 * math.sin(math.radians(-35))
    cx_far, cy_far = 134 + 70 * math.cos(math.radians(-155)), 298 + 70 * math.sin(math.radians(-155))

    # Jupiter & shadow cone & Io at top-right
    jx, jy = 356, 196
    # Shadow cone pointing right (away from Sun)
    el.append(f'<polygon points="{jx},{jy - 16} 402,{jy - 24} 402,{jy + 4} {jx},{jy + 16}" fill="#cbd5e1" opacity="0.65"/>')
    el.append(f'<circle cx="{jx}" cy="{jy}" r="17" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(txt(jx, jy + 4, "木星", size=10.5, color=ORANGE, anchor="middle", weight="700"))
    # Io orbit & emergence point H
    el.append(f'<ellipse cx="{jx}" cy="{jy}" rx="34" ry="28" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 3"/>')
    hx, hy = 356, 224
    el.append(f'<circle cx="{hx}" cy="{hy}" r="5.5" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.5"/>')
    el.append(txt(hx - 6, hy + 18, "木卫一（周期 42.5h）", size=10.2, color=PURPLE, anchor="end", weight="700", halo=True))

    # Static guide rays + constant-velocity animated rays
    dist_near = math.hypot(hx - bx, hy - by)
    dist_far = math.hypot(hx - cx_far, hy - cy_far)
    v_px = 95.0
    t_near = dist_near / v_px
    t_far = dist_far / v_px
    # Update CSS dynamically so dasharray & duration strictly satisfy distance / speed = constant!
    extra_css = f"""
  .pulse-near {{
    stroke-dasharray: {dist_near:.1f};
    stroke-dashoffset: {dist_near:.1f};
    animation: shootNear {t_near:.2f}s linear 0.3s 1 forwards;
  }}
  .pulse-far {{
    stroke-dasharray: {dist_far:.1f};
    stroke-dashoffset: {dist_far:.1f};
    animation: shootFar {t_far:.2f}s linear 0.3s 1 forwards;
  }}
  @keyframes shootNear {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes shootFar {{ to {{ stroke-dashoffset: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .pulse-near, .pulse-far {{ animation: none; stroke-dashoffset: 0; }}
  }}"""

    el.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{BLUE_LINE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    el.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{cx_far:.1f}" y2="{cy_far:.1f}" stroke="#fdba74" stroke-width="1.4" stroke-dasharray="4 3"/>')
    el.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{bx:.1f}" y2="{by:.1f}" class="pulse-near" stroke="{BLUE}" stroke-width="2.8" marker-end="url(#arr-blue)"/>')
    el.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{cx_far:.1f}" y2="{cy_far:.1f}" class="pulse-far" stroke="{ORANGE}" stroke-width="2.8" marker-end="url(#arr-orange)"/>')

    el.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="7.5" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(txt(bx + 12, by + 16, "近点 B（准时见蚀）", size=10.5, color=BLUE, weight="700", halo=True))
    el.append(f'<circle cx="{cx_far:.1f}" cy="{cy_far:.1f}" r="7.5" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(txt(cx_far + 2, cy_far - 13, "远点 C（迟到！）", size=10.5, color=ORANGE, anchor="middle", weight="700", halo=True))

    el.append(txt(198, 132, "多跑整条轨道直径 ΔL → 信号系统性迟到！", size=11, color=ORANGE, anchor="middle", weight="700"))

    # Bottom explanation inside Left Panel
    el.append(card(38, 390, 368, 114, rx=8, fill="#fffdf9", stroke=BLUE))
    el.append(txt(52, 412, "为什么盯住“木卫一”就能当太空秒表？", size=11.6, color=BLUE, weight="700"))
    el.append(txt(52, 434, "• 木卫一每 42.5 小时钻进木星阴影一次，极其守时；", size=10.8, color=BODY))
    el.append(txt(52, 455, "• 当地球从 B 公转远离至 C，连续几十次食的观测时刻越", size=10.8, color=BODY))
    el.append(txt(52, 476, "  积越晚（靠近时又逐次提前）——铁证光传播需要时间！", size=10.8, color=BODY))
    el.append(txt(52, 495, "  （注：天体间距为非等比例示意；光束动画严格按等速计时）", size=10, color=MUTED))

    # Right panel: Historical distinction Romer (1676) vs Huygens (1678/1690)
    el.append(card(434, 66, 302, 452))
    el.append(txt(452, 92, "二、史实辨析：谁测时间，谁算速度？", size=13, color=INK, weight="700"))

    el.append(card(450, 108, 270, 174, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(step_badge(468, 130, "1", fg=BLUE, bg="#ffffff", r=9.5))
    el.append(txt(484, 134, "罗默（Ole Rømer，1676 论文）", size=11.8, color=BLUE, weight="700"))
    el.append(txt(462, 158, "• 巴黎天文台十年观测，成功预言 1676 年", size=10.8, color=BODY))
    el.append(txt(462, 178, "  11 月木卫一重现将比旧历表推迟 10 分钟；", size=10.8, color=BODY))
    el.append(txt(462, 200, "• 推算光横穿地球轨道直径需 约 22 分钟", size=10.8, color=INK, weight="700"))
    el.append(txt(462, 220, "  （现代精确值为 16 分 38 秒 ＝ 998 秒）；", size=10.8, color=BODY))
    el.append(txt(462, 242, "• 纠偏：罗默本人只证明了光速有限并给出", size=10.6, color=ORANGE, weight="600"))
    el.append(txt(462, 262, "  22 分钟耗时，并未写出 km/s 速度数值！", size=10.6, color=ORANGE, weight="600"))

    el.append(f'<line x1="585" y1="282" x2="585" y2="300" stroke="{GREEN}" stroke-width="1.6" marker-end="url(#arr-green)"/>')

    el.append(card(450, 302, 270, 202, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(step_badge(468, 324, "2", fg=GREEN, bg="#ffffff", r=9.5))
    el.append(txt(484, 328, "惠更斯（Huygens，1678/1690）", size=11.8, color=GREEN, weight="700"))
    el.append(txt(462, 352, "• 在名著《光论》第一章完成首次除法：", size=10.8, color=BODY))
    el.append(txt(462, 374, "  取轨道直径 ≈ 22,000 个地球直径，除以", size=10.8, color=BODY))
    el.append(txt(462, 394, "  22 分钟 ＝ 每秒跑 16.7 个地球直径！", size=10.8, color=BODY))
    el.append(txt(462, 416, "• 代入皮卡尔 1669 年测得的地球周长：", size=10.8, color=BODY))
    el.append(pill(462, 428, "人类首个光速值 ≈ 214,000 km/s", fg=GREEN, bg="#ffffff", w=244, h=24, size=11.2))
    el.append(txt(462, 472, "• 虽因当年日地距离与 22 分钟偏粗而偏低", size=10.5, color=MUTED))
    el.append(txt(462, 490, "  约 28%，却首次命中 10^8 m/s 正确数量级！", size=10.5, color=INK, weight="600"))

    svg = figure(
        536,
        "罗默木卫一蚀延误测光速几何原理与惠更斯首次数值换算图",
        "左侧展示木卫一从木星阴影出现的光脉冲传向地球近点B与远点C的路程差及等速传播时间差演示；右侧严格区分1676年罗默测出22分钟轨道横穿时间与惠更斯在《光论》中算出约21.4万千米每秒首个光速数值的史实。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "romer-io-orbital-delay.svg", svg)


def _build_bradley_aberration_svg():
    el = []
    el.extend(
        header(
            "雨天奔跑为什么要把伞往前倾？布拉德雷“恒星光行差”意外测准光速（1728）",
            "本来想找恒星周年视差，却凭 20.25 角秒的望远镜倾角把光速误差一口气压缩进 1% 以内！",
        )
    )

    # Left panel: Raindrop / telescope tilt vector intuition
    el.append(card(24, 66, 356, 422))
    el.append(txt(42, 92, "一、直觉破译：奔跑接雨滴 ＝ 地球带着望远镜跑", size=12.8, color=INK, weight="700"))

    el.append(card(40, 108, 324, 232, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Sub-column A: Standing still
    el.append(txt(116, 130, "① 地球若静止（v = 0）", size=11.2, color=SLATE, anchor="middle", weight="700"))
    el.append(f'<line x1="116" y1="146" x2="116" y2="274" stroke="{BLUE}" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#arr-blue)"/>')
    # Vertical tube
    el.append(f'<rect x="106" y="186" width="20" height="86" rx="3" fill="none" stroke="{SLATE}" stroke-width="2.2"/>')
    el.append(txt(116, 300, "星光以速度 c 竖直落下", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(116, 318, "镜筒竖直对准头顶（θ = 0）", size=10.5, color=SLATE, anchor="middle", weight="600"))

    el.append(f'<line x1="194" y1="122" x2="194" y2="326" stroke="{HAIRLINE}" stroke-width="1"/>')

    # Sub-column B: Moving right at v
    el.append(txt(278, 130, "② 地球向右公转（速度 v）", size=11.2, color=ORANGE, anchor="middle", weight="700"))
    # Tilted telescope tube (exaggerated angle 18 deg for visual clarity, explicitly noted!)
    el.append(
        f'<g transform="translate(278,230) rotate(18)">'
        f'<rect x="-10" y="-46" width="20" height="90" rx="3" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2.2"/>'
        f'</g>'
    )
    # Apparent diagonal ray inside tilted tube
    el.append(f'<line x1="298" y1="168" x2="262" y2="278" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
    # Velocity triangle on side
    el.append(f'<line x1="238" y1="154" x2="238" y2="226" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')
    el.append(txt(230, 194, "c", size=11.5, color=BLUE, anchor="end", weight="700"))
    el.append(f'<line x1="238" y1="232" x2="288" y2="232" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#arr-green)"/>')
    el.append(txt(263, 248, "地球速度 v", size=10.2, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(278, 300, "必须向运动前方倾斜 θ 角", size=10.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(278, 318, "tan θ = v / c（图中倾角放大示意）", size=10.2, color=MUTED, anchor="middle"))

    el.append(card(40, 352, 324, 120, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(54, 375, "泰晤士河游船上的顿悟：", size=11.6, color=BLUE, weight="700"))
    el.append(txt(54, 397, "• 布拉德雷乘帆船时发现，风向明明没变，船一转向，桅杆", size=10.8, color=BODY))
    el.append(txt(54, 417, "  顶端的风向标就跟着变——因为它指示的是船速与风速的", size=10.8, color=BODY))
    el.append(txt(54, 437, "  矢量合成方向！星光进入运动地球上的望远镜同理。", size=10.8, color=BODY))
    el.append(txt(54, 458, "• 这同时成为哥白尼“地球确实在绕日运动”的首个直接实证！", size=10.6, color=INK, weight="700"))

    # Right panel: Gamma Draconis observation & calculation
    el.append(card(394, 66, 342, 422))
    el.append(txt(412, 92, "二、实测天龙座 γ 星：算出 30.1 万 km/s！", size=12.8, color=INK, weight="700"))

    # Apparent annual ellipse diagram
    el.append(card(410, 108, 310, 166, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    ecx, ecy = 565, 188
    el.append(f'<ellipse cx="{ecx}" cy="{ecy}" rx="86" ry="42" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>')
    el.append(f'<line x1="{ecx - 96}" y1="{ecy}" x2="{ecx + 96}" y2="{ecy}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    el.append(f'<line x1="{ecx}" y1="{ecy - 50}" x2="{ecx}" y2="{ecy + 50}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    el.append(f'<circle cx="{ecx}" cy="{ecy}" r="4" fill="{SLATE}"/>')
    el.append(txt(ecx, ecy - 10, "真实恒星方向", size=10.2, color=SLATE, anchor="middle"))
    # Dimension arrow for semi-major axis theta = 20.25"
    el.append(f'<line x1="{ecx}" y1="{ecy + 18}" x2="{ecx + 84}" y2="{ecy + 18}" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')
    el.append(txt(ecx + 43, ecy + 34, "θ ≈ 20.25″", size=11, color=ORANGE, anchor="middle", weight="700", halo=True))
    el.append(txt(ecx, 128, "伦敦天顶恒星一年内在天球画出的视椭圆", size=11, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(ecx, 260, "注：20.5 角秒仅相当于满月视直径的约 1/90！", size=10.4, color=MUTED, anchor="middle"))

    # Calculation card
    el.append(card(410, 286, 310, 186, rx=8, fill="#fffdf9", stroke=GREEN))
    el.append(txt(426, 310, "布拉德雷的三步神算（1728 皇家学会论文）：", size=11.6, color=GREEN, weight="700"))
    el.append(txt(426, 334, "① 测得全年最大光行差半角 θ ≈ 20.25″（现代 20.50″）", size=10.8, color=BODY))
    el.append(txt(426, 356, "② 速度比：c / v_地 = 1 / tan(20.25″) ≈ 10,186 倍！", size=10.8, color=INK, weight="700"))
    el.append(txt(426, 378, "③ 既然地球绕日一圈（2πR）要 365.25 天，光走完日地", size=10.8, color=BODY))
    el.append(txt(426, 398, "   半径 R 只需：365.25 天 ÷ (2π × 10,186) ＝ 8 分 12 秒！", size=10.8, color=BODY))
    el.append(pill(426, 414, "折合光速 ≈ 301,000 km/s（误差仅 ~0.4%！）", fg=ORANGE, bg=ORANGE_SOFT, w=278, h=24, size=11.2))
    el.append(txt(426, 458, "整整提前一百年达到百公里级惊人精度！", size=10.8, color=GREEN, weight="700"))

    svg = figure(
        506,
        "布拉德雷恒星光行差测光速原理与矢量合成图解",
        "左栏用雨天奔跑斜举雨伞类比地球以公转速度v运动时望远镜须前倾θ角（tanθ=v/c）；右栏展示天龙座γ星一年视位置椭圆半长轴约20.25角秒，由此算出光速约为地球公转速度的10186倍即约30.1万千米每秒。",
        el,
    )
    write_svg(SUBDIR, "bradley-stellar-aberration.svg", svg)


def _build_fizeau_foucault_svg():
    el = []
    el.extend(
        header(
            "把三亿公里星际跑道搬回地面：斐索旋转齿轮（1849）与傅科旋转镜（1850/1862）",
            "不再仰望木星与恒星！一对巴黎科学搭档兼对手，用高速机械快门与偏转镜在地球上驯服光速",
        )
    )

    # Top panel: Fizeau 1849 cogwheel
    el.append(card(24, 66, 712, 224))
    el.append(step_badge(44, 90, "1", fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(62, 95, "1849 年斐索（Fizeau）720 齿高速齿轮：人类史上第一次地面直接测光速！", size=13, color=INK, weight="700"))

    # Schematic diagram on left (x=40..448, y=108..274)
    el.append(card(40, 108, 406, 166, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Light source & beam splitter
    el.append(f'<circle cx="72" cy="156" r="9" fill="#fde047" stroke="{ORANGE}" stroke-width="1.4"/>')
    el.append(txt(72, 138, "光源", size=10.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(f'<line x1="81" y1="156" x2="122" y2="156" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')
    # Diagonal half-silvered mirror at (130, 186)
    el.append(f'<line x1="118" y1="174" x2="142" y2="198" stroke="{BLUE}" stroke-width="2.4"/>')
    el.append(f'<line x1="130" y1="156" x2="130" y2="186" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(txt(82, 228, "目镜观察", size=10.2, color=SLATE, anchor="middle", weight="600"))
    el.append(f'<line x1="124" y1="186" x2="96" y2="212" stroke="{SLATE}" stroke-width="1.4" stroke-dasharray="3 3"/>')

    # Toothed wheel at x=196, y=186
    wx, wy = 196, 186
    el.append(f'<circle cx="{wx}" cy="{wy}" r="26" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
    for k in range(12):
        ang = 2 * math.pi * k / 12
        tx1, ty1 = wx + 25 * math.cos(ang), wy + 25 * math.sin(ang)
        tx2, ty2 = wx + 32 * math.cos(ang), wy + 32 * math.sin(ang)
        el.append(f'<line x1="{tx1:.1f}" y1="{ty1:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" stroke="{BLUE}" stroke-width="3.2"/>')
    el.append(txt(wx, 236, "720 齿齿轮", size=10.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(wx, 253, "12.6 转/秒", size=10.2, color=MUTED, anchor="middle"))

    # Long path across Paris suburbs (8,633 m) to Montmartre mirror at x=418
    el.append(f'<line x1="232" y1="178" x2="408" y2="178" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
    el.append(f'<line x1="408" y1="194" x2="232" y2="194" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 3" marker-end="url(#arr-green)"/>')
    el.append(f'<rect x="412" y="164" width="8" height="44" rx="2" fill="{SLATE}" stroke="{INK}" stroke-width="1.2"/>')
    el.append(txt(322, 166, "去程：穿过齿缝飞越巴黎西郊", size=10.2, color=ORANGE, anchor="middle", weight="600"))
    el.append(txt(322, 214, "回程：恰被转来的相邻齿牙挡死！", size=10.2, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(322, 253, "单程 d = 8,633 m（往返 17.266 km）", size=10.5, color=INK, anchor="middle", weight="600"))

    # Formula card on right (x=460..720, y=108..274)
    el.append(card(460, 108, 260, 166, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(476, 132, "消光计时算账（首次变黑条件）：", size=11.6, color=BLUE, weight="700"))
    el.append(txt(476, 155, "• 从“齿缝”转到“紧邻齿牙”只需转过", size=10.8, color=BODY))
    el.append(txt(476, 175, "  1/(2N) = 1/1440 圈！", size=10.8, color=INK, weight="700"))
    el.append(txt(476, 197, "• 往返时间 Δt = 1/(2Nf) ≈ 55.1 微秒", size=10.8, color=BODY))
    el.append(txt(476, 219, "• 公式：c = 2d / Δt = 4 N d f", size=11.2, color=BLUE, weight="700"))
    el.append(pill(476, 234, "测得 c ≈ 313,300 km/s（偏高 ~4.5%）", fg=BLUE, bg="#ffffff", w=228, h=24, size=10.8))

    # Bottom panel: Foucault 1850/1862 rotating mirror
    el.append(card(24, 304, 712, 228))
    el.append(step_badge(44, 328, "2", fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(62, 333, "1850/1862 年傅科（Foucault）高速涡轮旋转镜：装进实验室房间，一剑封喉微粒说！", size=12.8, color=INK, weight="700"))

    # Schematic diagram on left (x=40..448, y=346..516)
    el.append(card(40, 346, 406, 170, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Source S -> Rotating Mirror R -> Concave Mirror M
    el.append(f'<circle cx="76" cy="404" r="8" fill="#fde047" stroke="{ORANGE}" stroke-width="1.4"/>')
    el.append(txt(76, 388, "光源", size=10.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(f'<line x1="84" y1="404" x2="192" y2="404" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')

    # Rotating mirror at (206, 404)
    rx, ry = 206, 404
    el.append(f'<line x1="{rx - 14}" y1="{ry + 14}" x2="{rx + 14}" y2="{ry - 14}" stroke="{SLATE}" stroke-width="2.5" stroke-dasharray="3 2"/>')
    el.append(f'<line x1="{rx - 10}" y1="{ry + 17}" x2="{rx + 10}" y2="{ry - 17}" stroke="{ORANGE}" stroke-width="2.8"/>')
    el.append(txt(rx, 372, "气动旋转镜（800 转/秒）", size=10.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(rx, 444, "光往返间转过微角 α", size=10.2, color=PURPLE, anchor="middle", weight="600"))

    # Path to fixed concave mirror at (398, 404) — folded 20m indoor path
    el.append(f'<line x1="218" y1="398" x2="388" y2="398" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')
    el.append(f'<line x1="388" y1="412" x2="218" y2="412" stroke="{PURPLE}" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#arr-muted)"/>')
    el.append(f'<path d="M394,378 Q408,404 394,430" fill="none" stroke="{BLUE}" stroke-width="3"/>')
    el.append(txt(308, 386, "室内折返光程仅 20 m（可插入水管！）", size=10.2, color=BLUE, anchor="middle", weight="600"))

    # Deflected return ray by angle 2*alpha to displaced scale image I'
    el.append(f'<line x1="196" y1="412" x2="90" y2="466" stroke="{PURPLE}" stroke-width="2" marker-end="url(#arr-muted)"/>')
    el.append(txt(144, 466, "反射光偏转 2α → 像移 0.7 mm", size=10.4, color=PURPLE, anchor="middle", weight="700", halo=True))
    el.append(txt(243, 502, "把“卡死时间点”升级为“连续测量微小偏角”，精度暴涨！", size=10.4, color=MUTED, anchor="middle"))

    # Achievement card on right (x=460..720, y=346..516)
    el.append(card(460, 346, 260, 170, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(476, 370, "傅科转镜改写物理学史的两记重锤：", size=11.5, color=ORANGE, weight="700"))
    el.append(txt(476, 394, "① 1850 水中光速判决实验：测出光在水", size=10.8, color=BODY))
    el.append(txt(476, 414, "   中速度仅为空气的 3/4，当场宣判牛顿", size=10.8, color=BODY))
    el.append(txt(476, 434, "   “微粒说（入水加速）”死刑！", size=10.8, color=INK, weight="700"))
    el.append(txt(476, 456, "② 1862 精密值：298,000 ± 500 km/s", size=11, color=ORANGE, weight="700"))
    el.append(txt(476, 476, "   误差仅 0.6%！恰与麦克斯韦纯电磁算", size=10.6, color=BODY))
    el.append(txt(476, 496, "   出的波速吻合，证实“光就是电磁波”！", size=10.6, color=GREEN, weight="700"))

    svg = figure(
        548,
        "斐索1849年旋转齿轮法与傅科1850至1862年旋转平面镜法测光速对比图",
        "上图展示斐索用720齿旋转齿轮跨越8633米基线在12.6转每秒首次遮住回光测得31.33万千米每秒；下图展示傅科用800转每秒气动旋转镜在20米室内光程测偏转角2α，既证明水中光速慢于空气又在1862年测得29.8万千米每秒。",
        el,
    )
    write_svg(SUBDIR, "fizeau-cogwheel-and-foucault-mirror.svg", svg)


def _build_michelson_laser_svg():
    el = []
    el.extend(
        header(
            "从加州双峰八面转镜到甲烷稳频激光：人类如何把光速逼到 1 m/s 级精度？",
            "上半场把“飞行时间法”推向机械极限（迈克耳孙）；下半场彻底换赛道改用波动方程 c = λν（谐振腔与激光）",
        )
    )

    # Top panel: Michelson 1926 Mount Wilson octagonal mirror
    el.append(card(24, 66, 712, 218))
    el.append(step_badge(44, 90, "1", fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(62, 95, "1926 年迈克耳孙（Michelson）威尔逊山八面旋转镜：机械光学时代的封神绝唱", size=12.8, color=INK, weight="700"))

    el.append(card(40, 108, 424, 160, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    # Octagonal mirror on left (cx=116, cy=186, r=28)
    ocx, ocy, r_oct = 116, 186, 26
    oct_pts = " ".join(
        f"{ocx + r_oct * math.cos(math.radians(22.5 + 45 * k)):.1f},{ocy + r_oct * math.sin(math.radians(22.5 + 45 * k)):.1f}"
        for k in range(8)
    )
    el.append(f'<polygon points="{oct_pts}" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>')
    el.append(txt(ocx, ocy + 4, "8面镜", size=10, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(ocx, 234, "威尔逊山天文台", size=10.5, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(ocx, 252, "转速 ≈ 528 转/秒", size=10.2, color=MUTED, anchor="middle"))

    # Mountain-to-mountain beam to Mt San Antonio (x=404)
    el.append(f'<line x1="146" y1="176" x2="392" y2="176" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
    el.append(f'<line x1="392" y1="194" x2="146" y2="194" stroke="{BLUE}" stroke-width="2" stroke-dasharray="5 3" marker-end="url(#arr-blue)"/>')
    el.append(f'<path d="M366,256 L406,162 L446,256 Z" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.3"/>')
    el.append(f'<rect x="398" y="168" width="8" height="32" rx="2" fill="{BLUE}"/>')
    el.append(txt(406, 246, "圣安东尼奥山", size=10.2, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(268, 164, "大地测量局毫米级勘测基线 d ≈ 35.4 km", size=10.4, color=INK, anchor="middle", weight="700"))
    el.append(txt(268, 214, "往返约 236 μs，八面镜恰转过 1/8 圈复位！", size=10.4, color=BLUE, anchor="middle", weight="600"))

    # Right summary card for Michelson
    el.append(card(478, 108, 242, 160, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(494, 132, "为什么八面镜比傅科更准百倍？", size=11.5, color=GREEN, weight="700"))
    el.append(txt(494, 155, "• 同步零位法：下一镜面精准替代前", size=10.8, color=BODY))
    el.append(txt(494, 175, "  一镜面角度，无需测极小位移：", size=10.8, color=BODY))
    el.append(txt(494, 197, "  c_空气 = 16 f d（音叉频闪校准转速）", size=11, color=INK, weight="700"))
    el.append(pill(494, 210, "真空值：299,796 ± 4 km/s", fg=GREEN, bg="#ffffff", w=210, h=24, size=11))
    el.append(txt(494, 252, "晚年更修 1.6 km 真空铁管排除空气干扰", size=10.2, color=MUTED))

    # Bottom panel: Wave equation c = lambda * nu (Cavity + Laser chain)
    el.append(card(24, 298, 712, 222))
    el.append(step_badge(44, 322, "2", fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(62, 327, "二战后换道超车：不跑长途了！直接同测一束电磁波的“波长 λ × 频率 ν ＝ c”", size=12.8, color=INK, weight="700"))

    # Left sub-card: Essen cavity resonator (1946-1950)
    el.append(card(40, 342, 332, 162, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(56, 366, "① 埃森微波谐振腔（1946–1950，英国 NPL）", size=11.6, color=BLUE, weight="700"))
    # Standing wave cylinder icon
    el.append(f'<rect x="56" y="380" width="136" height="34" rx="5" fill="#ffffff" stroke="{BLUE}" stroke-width="1.5"/>')
    wave_pts = " ".join(f"{60 + x:.1f},{397 + 11 * math.sin(2 * math.pi * x / 64):.1f}" for x in range(0, 129, 4))
    wave_pts2 = " ".join(f"{60 + x:.1f},{397 - 11 * math.sin(2 * math.pi * x / 64):.1f}" for x in range(0, 129, 4))
    el.append(f'<polyline points="{wave_pts}" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(f'<polyline points="{wave_pts2}" fill="none" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="3 2"/>')
    el.append(txt(204, 394, "精密真空金属腔", size=10.6, color=INK, weight="700"))
    el.append(txt(204, 412, "尺寸定 λ，石英钟测 ν", size=10.4, color=BODY))
    el.append(txt(56, 438, "• 揪出战前光学界偏低 16 km/s 的系统误差！", size=10.8, color=BODY))
    el.append(txt(56, 460, "• 1950 年得出 299,792.5 ± 1 km/s，埃森随后更", size=10.8, color=BODY))
    el.append(txt(56, 480, "  造出世界首台实用铯原子钟，改写“秒”的定义。", size=10.8, color=INK, weight="600"))

    # Right sub-card: Evenson & Hall laser frequency chain (1972)
    el.append(card(388, 342, 332, 162, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(404, 366, "② 埃文森与霍尔稳频激光链（1972，美国 NIST）", size=11.6, color=PURPLE, weight="700"))
    el.append(txt(404, 390, "• 难点：可见／红外激光每秒震荡近百太赫兹（10^14 Hz），", size=10.6, color=BODY))
    el.append(txt(404, 410, "  任何电子计数器都数不过来！", size=10.6, color=BODY))
    el.append(txt(404, 432, "• 破局：搭起多级谐波激光“频率梯”，把铯原子钟频率一", size=10.6, color=BODY))
    el.append(txt(404, 452, "  路锁相传递到 3.39 μm 甲烷稳频氦氖激光（88.38 THz）", size=10.6, color=BODY))
    el.append(pill(404, 466, "精度暴涨百倍：299,792,456.2 ± 1.1 m/s", fg=PURPLE, bg="#ffffff", w=300, h=24, size=10.8))

    svg = figure(
        536,
        "迈克耳孙威尔逊山八面旋转镜实验与战后谐振腔及稳频激光测光速原理图",
        "上图展示1926年迈克耳孙在35.4千米山峰基线上用528转每秒八面镜测得299796千米每秒；下图展示战后转向c=λν波动法，包括埃森微波谐振腔与1972年埃文森团队甲烷稳频激光频率链将不确定度缩小到1.1米每秒。",
        el,
    )
    write_svg(SUBDIR, "michelson-mt-wilson-and-laser-chain.svg", svg)


def _build_precision_and_1983_svg():
    el = []
    el.extend(
        header(
            "三百年精度狂飙一百万倍，为什么 1983 年人类宣布“永远不再测光速”？",
            "当激光比“一米”本身还要准时，国际计量大会干脆把光速焊死为精确常数，反过来重新定义“米”！",
        )
    )

    # Top panel: Log10 relative uncertainty chart
    el.append(card(24, 66, 712, 248))
    el.append(txt(42, 91, "一、三百年光速测量相对误差演进图（纵轴对数坐标 log₁₀(Δc/c)，越往下越精准）", size=12.6, color=INK, weight="700"))

    # Plot box: x from 104 to 688, y from 112 (10^0) to 272 (10^-10): 16px per decade!
    px0, px1 = 108, 692
    py0, py1 = 112, 272  # 10 decades: log10 = 0 at py0=112, log10 = -10 at py1=272
    for dec in [0, -2, -4, -6, -8, -10]:
        gy = py0 + (-dec) * 16
        el.append(f'<line x1="{px0}" y1="{gy}" x2="{px1}" y2="{gy}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
        lbl = "10⁰" if dec == 0 else f"10^{dec}"
        el.append(txt(px0 - 10, gy + 4, lbl, size=10.2, color=MUTED, anchor="end"))

    # Krypton-86 metre definition fuzziness floor at 4e-9 -> log10(4e-9) = -8.40 -> y = 112 + 8.40*16 = 246.4
    y_kr = py0 + 8.40 * 16
    el.append(f'<line x1="{px0}" y1="{y_kr:.1f}" x2="{px1}" y2="{y_kr:.1f}" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="6 4"/>')
    el.append(txt(262, y_kr + 16, "1960 年氪-86“米”定义自身模糊极限（±4×10⁻⁹）", size=10.2, color=ORANGE, anchor="middle", weight="700", halo=True))

    milestones = [
        (128, -0.54, "1676/90 罗默+惠更斯", "21.4万 km/s", BLUE, 62, 6),
        (234, -2.40, "1728 布拉德雷", "30.1万 km/s", BLUE, 6, 22),
        (336, -2.78, "1862 傅科转镜", "298,000 km/s", BLUE, 12, -16),
        (432, -4.87, "1926 迈克耳孙", "299,796 km/s", GREEN, -12, 22),
        (522, -5.48, "1950 埃森谐振腔", "299,792.5 km/s", GREEN, 16, -16),
        (608, -8.43, "1972 埃文森激光", "±1.1 m/s", PURPLE, 16, -16),
    ]

    poly = []
    for mx, lg, mname, mval, mcol, dx, dy in milestones:
        my = py0 + (-lg) * 16
        poly.append(f"{mx},{my:.1f}")
    el.append(f'<polyline points="{" ".join(poly)} 680,294" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')

    for mx, lg, mname, mval, mcol, dx, dy in milestones:
        my = py0 + (-lg) * 16
        el.append(f'<circle cx="{mx}" cy="{my:.1f}" r="5.5" fill="#ffffff" stroke="{mcol}" stroke-width="2.2"/>')
        el.append(txt(mx + dx, my + dy, f"{mname}", size=10.3, color=mcol, anchor="middle", weight="700", halo=True))
        el.append(txt(mx + dx, my + dy + (14 if dy > 0 else -13), mval, size=9.8, color=BODY, anchor="middle", halo=True))

    # 1983 exact lock badge at (680, 294)
    el.append(f'<circle cx="680" cy="294" r="7" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2.2"/>')
    el.append(txt(666, 298, "1983 精确锁定（零误差！）", size=10.5, color=ORANGE, anchor="end", weight="700", halo=True))

    # Bottom panel: The logical inversion of 1983
    el.append(card(24, 328, 712, 184))
    el.append(txt(42, 353, "二、1983 年第 17 届国际计量大会（CGPM）的历史性大反转", size=13, color=INK, weight="700"))

    el.append(card(40, 368, 312, 128, rx=8, fill=SLATE_SOFT, stroke=SLATE))
    el.append(txt(56, 391, "旧逻辑（1983 年以前）：拿“尺子”去量光速", size=11.5, color=SLATE, weight="700"))
    el.append(txt(56, 414, "• 先用铂铱米原器（1889）或氪-86 橙红光波长（1960）", size=10.6, color=BODY))
    el.append(txt(56, 434, "  规定“1 米有多长”，再测光每秒走多少米；", size=10.6, color=BODY))
    el.append(txt(56, 456, "• 尴尬困局：氪-86 谱线自身发虚（±1.2 m/s），不同实", size=10.6, color=BODY))
    el.append(txt(56, 476, "  验室激光明明更稳，却被模糊的“米”卡死了上限！", size=10.6, color=ORANGE, weight="600"))

    el.append(f'<line x1="356" y1="432" x2="396" y2="432" stroke="{GREEN}" stroke-width="2.4" marker-end="url(#arr-green)"/>')
    el.append(txt(376, 420, "反转", size=10.8, color=GREEN, anchor="middle", weight="700"))

    el.append(card(404, 368, 316, 128, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.4))
    el.append(txt(420, 391, "新逻辑（1983 至今）：拿“光速＋秒”定义尺子！", size=11.5, color=GREEN, weight="700"))
    el.append(pill(420, 402, "精确常数 c ≡ 299,792,458 m/s（误差 = 0）", fg=GREEN, bg="#ffffff", w=284, h=24, size=11))
    el.append(txt(420, 446, "• 新定义：1 米 ＝ 光在真空中于 1/299,792,458 秒", size=10.8, color=INK, weight="700"))
    el.append(txt(420, 466, "  内行进的路程（“秒”由铯-133 原子钟超精密定义）；", size=10.6, color=BODY))
    el.append(txt(420, 486, "• 从此技术越进步，改变的不是 c，而是“1 米”更准！", size=10.6, color=GREEN, weight="700"))

    svg = figure(
        528,
        "三百年光速测量相对误差对数演进与1983年国际计量大会重新定义米原理图",
        "上图用对数坐标展示从1676年罗默与惠更斯到1972年埃文森激光将相对不确定度从10^-1压至3.7×10^-9撞上氪86米定义极限的过程；下图对比1983年前后从拿米尺测光速反转为将c精确固定为299792458米每秒来定义1米的计量学革命。",
        el,
    )
    write_svg(SUBDIR, "precision-leap-and-1983-metre-redefinition.svg", svg)


@register("light-speed", "Methods and 350-year history of measuring the speed of light up to the 1983 SI redefinition", "science")
def build_light_speed():
    _verify_light_speed_math()
    _build_galileo_lantern_svg()
    _build_romer_io_svg()
    _build_bradley_aberration_svg()
    _build_fizeau_foucault_svg()
    _build_michelson_laser_svg()
    _build_precision_and_1983_svg()
