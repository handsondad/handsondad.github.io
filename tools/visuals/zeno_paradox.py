"""Zeno's Paradoxes: motion, continuum measure, supertasks, and quantum Zeno visual builders."""

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
    step_badge,
    txt,
    write_svg,
)

CRIMSON = "#b91c1c"
CRIMSON_SOFT = "#fef2f2"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"


def _verify_zeno_math():
    """Assert exact series limits, catch-up coordinates, relative velocities, and quantum Zeno survival probabilities."""
    # 1. Achilles (10 m/s) vs Tortoise (1 m/s, 90 m head start)
    va, vt, d0 = 10.0, 1.0, 90.0
    t_catch = d0 / (va - vt)
    x_catch = va * t_catch
    assert abs(t_catch - 10.0) < 1e-12
    assert abs(x_catch - 100.0) < 1e-12

    # Partial sums of Zeno catch-up intervals: 9 + 0.9 + 0.09 + ...
    t_steps = [9.0 * (0.1 ** k) for k in range(8)]
    assert abs(sum(t_steps) - 10.0 * (1.0 - 0.1 ** 8)) < 1e-12

    # 2. Dichotomy geometric series vs Harmonic series
    geom_10 = sum(0.5 ** k for k in range(1, 11))
    assert abs(geom_10 - (1.0 - 2.0 ** -10)) < 1e-12
    harm_10 = sum(1.0 / k for k in range(1, 11))
    assert harm_10 > 2.928  # Diverges!

    # 3. Stadium relative velocity: v_B = +v, v_C = -v => v_BC = 2v
    v = 1.0
    v_rel = v - (-v)
    assert abs(v_rel - 2.0 * v) < 1e-12

    # 4. Thomson's lamp switching instants: t_n = 2 * (1 - 2^-n) minutes
    t_switch = [2.0 * (1.0 - 0.5 ** n) for n in range(7)]
    assert abs(t_switch[0] - 0.0) < 1e-12
    assert abs(t_switch[1] - 1.0) < 1e-12
    assert abs(t_switch[2] - 1.5) < 1e-12
    assert t_switch[-1] < 2.0

    # 5. Quantum Zeno survival probability after N projective measurements during pi-pulse (Omega * T = pi):
    # P_surv(N) = [cos^2(pi / (2*N))]^N
    p1 = (math.cos(math.pi / 2.0) ** 2) ** 1
    p4 = (math.cos(math.pi / 8.0) ** 2) ** 4
    p16 = (math.cos(math.pi / 32.0) ** 2) ** 16
    p64 = (math.cos(math.pi / 128.0) ** 2) ** 64
    assert abs(p1 - 0.0) < 1e-12
    assert 0.530 <= p4 <= 0.532
    assert 0.856 <= p16 <= 0.858
    assert 0.961 <= p64 <= 0.963


def _build_achilles_tortoise_svg():
    """SVG 1: Achilles & the Tortoise — real-time linear race animation vs Zeno's camera snapshots & spacetime intersection."""
    # Model: v_A = 10 m/s, v_T = 1 m/s, Tortoise starts at x0 = 90 m.
    # Exact catch-up at t = 10 s, x = 100 m; race shown to t = 12 s (x_A = 120 m, x_T = 102 m).
    # Track x-mapping: 0 m -> x=64, 120 m -> x=700 (5.30 px per meter).
    x0_px = 64.0
    scale_x = 5.30  # 120 m * 5.30 = 636 px -> x_end = 700.0
    xa_start = x0_px + 0.0 * scale_x       # 64.0
    xa_end = x0_px + 120.0 * scale_x       # 700.0 (dx = +636.0 px over 12 model s)
    xt_start = x0_px + 90.0 * scale_x      # 541.0
    xt_end = x0_px + 102.0 * scale_x       # 604.6 (dx = +63.6 px over 12 model s — exact 1:10 speed ratio!)
    x_meet = x0_px + 100.0 * scale_x       # 594.0

    extra_css = f"""
      @keyframes zeno-achilles-run {{
        from {{ transform: translateX(0px); }}
        to   {{ transform: translateX({xa_end - xa_start:.1f}px); }}
      }}
      @keyframes zeno-tortoise-crawl {{
        from {{ transform: translateX(0px); }}
        to   {{ transform: translateX({xt_end - xt_start:.1f}px); }}
      }}
      .za-runner {{
        animation: zeno-achilles-run 6s linear 0.3s 1 forwards;
      }}
      .zt-crawler {{
        animation: zeno-tortoise-crawl 6s linear 0.3s 1 forwards;
      }}
      @media (prefers-reduced-motion: reduce) {{
        .za-runner, .zt-crawler {{
          animation: none !important;
        }}
      }}
    """

    el = []
    el += header(
        "阿喀琉斯追乌龟：真实匀速超越 vs 芝诺把时钟卡在 10 秒前的“慢放陷阱”",
        "设阿喀琉斯 10 m/s（起点 0 m）、乌龟 1 m/s（让先 90 m）：真实世界精确在 t = 10 s、x = 100 m 并肩反超",
    )

    # Top card: 120m race track (y=66..244)
    el.append(card(20, 66, 720, 178))
    el.append(pill(34, 78, "上栏：真实时间匀速赛跑（0 → 12 秒，速度严格按 10 : 1 等比运动）", fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(724, 93, "注：动画播放一次停在 12 s 反超终态", size=11, color=MUTED, anchor="end"))

    # Track baseline
    ty = 166.0
    el.append(f'<line x1="{x0_px:.1f}" y1="{ty:.1f}" x2="{xa_end:.1f}" y2="{ty:.1f}" stroke="{SLATE}" stroke-width="2.5"/>')

    # Distance ticks: 0m, 50m, 90m, 99m, 100m (catch!), 120m
    ticks = [
        (0.0, "0 m", "起点 t=0", SLATE, 0),
        (50.0, "50 m", "t=5 s", MUTED, 0),
        (90.0, "90 m", "t₁=9 s", ORANGE, -16),
        (100.0, "100 m", "追上! t=10 s", CRIMSON, 18),
        (120.0, "120 m", "t=12 s 终态", BLUE, 0),
    ]
    for m_val, lbl_top, lbl_bot, col, x_off in ticks:
        tx = x0_px + m_val * scale_x
        sw = 2.2 if m_val in (90.0, 100.0) else 1.3
        el.append(f'<line x1="{tx:.1f}" y1="{ty - 10:.1f}" x2="{tx:.1f}" y2="{ty + 10:.1f}" stroke="{col}" stroke-width="{sw}"/>')
        el.append(txt(tx + x_off, ty + 26, lbl_top, size=11.5, color=col, anchor="middle", weight="700" if m_val == 100.0 else None))
        el.append(txt(tx + x_off, ty + 42, lbl_bot, size=10.8, color=col if m_val == 100.0 else MUTED, anchor="middle"))

    # Highlight catch-up vertical dashed line at x = 100 m
    el.append(f'<line x1="{x_meet:.1f}" y1="108" x2="{x_meet:.1f}" y2="{ty - 10:.1f}" stroke="{CRIMSON}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    el.append(txt(x_meet - 8, 118, "芝诺无限拍照全部挤在这条红线左侧 (90, 99, 99.9… m)", size=11, color=CRIMSON, anchor="end", weight="600"))

    # Static ghost markers at t=12s so static / reduced-motion viewers ALSO see both start and final overtake positions!
    el.append(f'<circle cx="{xa_end:.1f}" cy="{ty - 24:.1f}" r="8" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="3 2"/>')
    el.append(txt(xa_end, ty - 38, "12s 阿喀琉斯 (120m)", size=10.8, color=BLUE, anchor="end", weight="600"))
    el.append(f'<circle cx="{xt_end:.1f}" cy="{ty - 8:.1f}" r="6.5" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="3 2"/>')

    # Animated Achilles marker (starts at x=0m, y=ty-24)
    el.append(
        f'<g class="za-runner">'
        f'<circle cx="{xa_start:.1f}" cy="{ty - 24:.1f}" r="8.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.8"/>'
        f'{txt(xa_start, ty - 38, "阿喀琉斯 10 m/s", size=11.2, color=BLUE, anchor="start", weight="700", halo=True)}'
        f'</g>'
    )
    # Animated Tortoise marker (starts at x=90m, y=ty-8)
    el.append(
        f'<g class="zt-crawler">'
        f'<rect x="{xt_start - 7:.1f}" y="{ty - 15:.1f}" width="14" height="10" rx="5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/>'
        f'{txt(xt_start - 10, ty - 20, "乌龟 1 m/s", size=10.8, color=GREEN, anchor="end", weight="700", halo=True)}'
        f'</g>'
    )

    # Bottom split: Left = Spacetime (t, x) graph (y=256..478, w=416); Right = Zeno's arithmetic vs reality table (w=292)
    el.append(card(20, 256, 416, 222))
    el.append(pill(34, 268, "下左：时空图 (t, x) 一眼看穿——两条直线必相交", fg=PURPLE, bg=PURPLE_SOFT))

    # Plot axes inside left bottom card: t in [0, 12] -> x in [74, 410] (28 px/s); pos in [0, 120] -> y in [442, 310] (1.1 px/m)
    gx0, gy0 = 74.0, 442.0
    st, sx = 27.0, 1.05  # 12s * 27 = 324 -> gx1 = 398; 120m * 1.05 = 126 -> gy1 = 316
    el.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0 + 12.4 * st:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')
    el.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0:.1f}" y2="{gy0 - 126 * sx:.1f}" stroke="{SLATE}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')
    el.append(txt(gx0 - 8, gy0 - 118 * sx, "位置 x(m)", size=10.8, color=MUTED, anchor="end"))
    el.append(txt(gx0 + 6.0 * st, gy0 + 30, "时间 t (秒)", size=10.8, color=MUTED, anchor="middle"))

    for t_tick in (0, 5, 9, 10, 12):
        px = gx0 + t_tick * st
        col = CRIMSON if t_tick == 10 else MUTED
        el.append(f'<line x1="{px:.1f}" y1="{gy0:.1f}" x2="{px:.1f}" y2="{gy0 + 4:.1f}" stroke="{col}" stroke-width="1.3"/>')
        el.append(txt(px, gy0 + 16, f"{t_tick}", size=10.8, color=col, anchor="middle", weight="700" if t_tick == 10 else None))

    for x_tick, y_lbl_off in ((0, 4), (90, 9), (100, -3)):
        py = gy0 - x_tick * sx
        el.append(f'<line x1="{gx0 - 4:.1f}" y1="{py:.1f}" x2="{gx0:.1f}" y2="{py:.1f}" stroke="{MUTED}" stroke-width="1.2"/>')
        el.append(txt(gx0 - 8, py + y_lbl_off, f"{x_tick}", size=10.8, color=CRIMSON if x_tick == 100 else MUTED, anchor="end"))

    # Zeno shaded region t < 10 s
    px_10 = gx0 + 10.0 * st
    py_100 = gy0 - 100.0 * sx
    el.append(f'<rect x="{gx0:.1f}" y="{py_100:.1f}" width="{10.0 * st:.1f}" height="{100.0 * sx:.1f}" fill="{ORANGE_SOFT}" opacity="0.45"/>')
    el.append(f'<line x1="{px_10:.1f}" y1="{gy0:.1f}" x2="{px_10:.1f}" y2="{py_100 - 14:.1f}" stroke="{CRIMSON}" stroke-width="1.4" stroke-dasharray="4 3"/>')

    # Worldline of Tortoise: (0, 90) -> (12, 102)
    el.append(f'<line x1="{gx0:.1f}" y1="{gy0 - 90 * sx:.1f}" x2="{gx0 + 12 * st:.1f}" y2="{gy0 - 102 * sx:.1f}" stroke="{GREEN}" stroke-width="2.4"/>')
    el.append(txt(gx0 + 2.2 * st, gy0 - 96 * sx, "乌龟 x_T = 90 + t", size=11, color=GREEN, weight="600"))

    # Worldline of Achilles: (0, 0) -> (12, 120)
    el.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0 + 12 * st:.1f}" y2="{gy0 - 120 * sx:.1f}" stroke="{BLUE}" stroke-width="2.6"/>')
    el.append(txt(gx0 + 4.3 * st, gy0 - 34 * sx, "阿喀琉斯 x_A = 10t", size=11, color=BLUE, weight="700"))

    # Zeno staircase: (0,0)->(9,90)->(9,99) wait: staircase between the two lines!
    # At t=0, T is at 90; A reaches 90 at t=9; at t=9, T is at 99; A reaches 99 at t=9.9
    p_t9_x90 = (gx0 + 9.0 * st, gy0 - 90.0 * sx)
    p_t9_x99 = (gx0 + 9.0 * st, gy0 - 99.0 * sx)
    p_t99_x99 = (gx0 + 9.9 * st, gy0 - 99.0 * sx)
    el.append(
        f'<polyline points="{gx0:.1f},{gy0 - 90 * sx:.1f} {p_t9_x90[0]:.1f},{p_t9_x90[1]:.1f} '
        f'{p_t9_x99[0]:.1f},{p_t9_x99[1]:.1f} {p_t99_x99[0]:.1f},{p_t99_x99[1]:.1f}" '
        f'fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="3 2"/>'
    )
    el.append(f'<circle cx="{px_10:.1f}" cy="{py_100:.1f}" r="5" fill="{CRIMSON}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(px_10 - 8, py_100 - 10, "交点 (10 s, 100 m)", size=11.2, color=CRIMSON, anchor="end", weight="700"))

    # Right bottom card: Step ledger (x=448, y=256, w=292, h=222)
    el.append(card(448, 256, 292, 222))
    el.append(pill(462, 268, "下右：芝诺账本漏掉了什么？", fg=ORANGE, bg=ORANGE_SOFT))

    rows = [
        ("第 1 段", "Δt = 9 s", "A 到 90 m"),
        ("第 2 段", "Δt = 0.9 s", "A 到 99 m"),
        ("第 3 段", "Δt = 0.09 s", "A 到 99.9 m"),
        ("第 k 段", "Δt = 9×10¹⁻ᵏ s", "无限逼近 100 m"),
    ]
    ry = 314
    for col1, col2, col3 in rows:
        el.append(txt(462, ry, col1, size=11.5, color=INK, weight="600"))
        el.append(txt(536, ry, col2, size=11.5, color=ORANGE, cls="mono"))
        el.append(txt(644, ry, col3, size=11.3, color=BODY))
        ry += 24

    el.append(f'<line x1="462" y1="406" x2="726" y2="406" stroke="{HAIRLINE}" stroke-width="1"/>')
    el.append(txt(462, 426, "无穷段总耗时 = 9 + 0.9 + 0.09 + … = 10.0 秒！", size=11.8, color=CRIMSON, weight="700"))
    el.append(txt(462, 446, "• 芝诺把 0 到 10 秒切成了无穷多帧慢镜头，", size=11.2, color=BODY))
    el.append(txt(462, 464, "  却误把“无穷多步”当成“无穷长时间”！", size=11.2, color=BODY, weight="600"))

    svg = figure(
        492,
        "阿喀琉斯追乌龟悖论的真实匀速运动对比与时空图解",
        "上栏按 10:1 真实速度比展示阿喀琉斯在 10 秒、100 米处追上并反超乌龟；下栏时空图与账本揭示芝诺的无穷追赶段总耗时精确收敛于 10 秒。",
        el,
        extra_css=extra_css,
    )
    write_svg("zeno-paradox", "achilles-tortoise-race.svg", svg)


def _build_dichotomy_square_svg():
    """SVG 2: Progressive & Regressive Dichotomy + Geometric Unit Square + Convergent vs Divergent Infinite Sums."""
    el = []
    el += header(
        "二分法悖论：连第一步都迈不出去？单位正方形与柯西部分和的正面破局",
        "区分“递进二分”与更刁钻的“倒退二分”，并用柯西收敛判别回答“为什么无穷个正数相加未必等于无穷大”",
    )

    # Left card: Regressive dichotomy + Unit square geometric proof (x=20, y=66, w=352, h=404)
    el.append(card(20, 66, 352, 404))
    el.append(pill(34, 78, "左栏：倒退二分陷阱 & 1×1 正方形无缝拼图", fg=BLUE, bg=BLUE_SOFT))

    # Regressive line bar (y=114..166)
    lx0, lx1, ly = 44.0, 348.0, 134.0
    lw = lx1 - lx0  # 304 px
    el.append(txt(44, 118, "倒退二分：到 1 前先到 1/2，到 1/2 前先到 1/4…哪来第一步？", size=11.2, color=CRIMSON, weight="600"))
    el.append(f'<line x1="{lx0:.1f}" y1="{ly:.1f}" x2="{lx1:.1f}" y2="{ly:.1f}" stroke="{BLUE}" stroke-width="3"/>')
    for frac, label in [(0.0, "0"), (0.125, "1/8"), (0.25, "1/4"), (0.5, "1/2"), (1.0, "1")]:
        px = lx0 + frac * lw
        el.append(f'<line x1="{px:.1f}" y1="{ly - 6:.1f}" x2="{px:.1f}" y2="{ly + 6:.1f}" stroke="{INK}" stroke-width="1.5"/>')
        el.append(txt(px, ly + 20, label, size=11, color=INK if frac in (0.0, 0.5, 1.0) else MUTED, anchor="middle"))

    # Unit square geometric dissection: 208 x 208 square at (92, 178)
    sx, sy, sw = 92.0, 178.0, 208.0
    el.append(f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{sw:.1f}" height="{sw:.1f}" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>')
    # 1/2: left half (w=104, h=208)
    el.append(f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{sw / 2:.1f}" height="{sw:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.3"/>')
    el.append(txt(sx + sw / 4, sy + sw / 2, "1/2", size=15, color=BLUE, anchor="middle", weight="700"))
    # 1/4: top-right half (x=sx+104, y=sy, w=104, h=104)
    el.append(f'<rect x="{sx + sw / 2:.1f}" y="{sy:.1f}" width="{sw / 2:.1f}" height="{sw / 2:.1f}" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.3"/>')
    el.append(txt(sx + 0.75 * sw, sy + 0.25 * sw + 4, "1/4", size=14, color=GREEN, anchor="middle", weight="700"))
    # 1/8: bottom-right left half (x=sx+104, y=sy+104, w=52, h=104)
    el.append(f'<rect x="{sx + sw / 2:.1f}" y="{sy + sw / 2:.1f}" width="{sw / 4:.1f}" height="{sw / 2:.1f}" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.3"/>')
    el.append(txt(sx + 0.625 * sw, sy + 0.75 * sw + 4, "1/8", size=13, color=ORANGE, anchor="middle", weight="700"))
    # 1/16: (x=sx+156, y=sy+104, w=52, h=52)
    el.append(f'<rect x="{sx + 0.75 * sw:.1f}" y="{sy + 0.5 * sw:.1f}" width="{sw / 4:.1f}" height="{sw / 4:.1f}" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.2"/>')
    el.append(txt(sx + 0.875 * sw, sy + 0.625 * sw + 4, "1/16", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    # 1/32: (x=sx+156, y=sy+156, w=26, h=52)
    el.append(f'<rect x="{sx + 0.75 * sw:.1f}" y="{sy + 0.75 * sw:.1f}" width="{sw / 8:.1f}" height="{sw / 4:.1f}" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="1.1"/>')
    el.append(txt(sx + 0.8125 * sw, sy + 0.875 * sw + 4, "1/32", size=9.8, color=TEAL, anchor="middle", weight="600"))
    # 1/64 + remainder corner
    el.append(f'<rect x="{sx + 0.875 * sw:.1f}" y="{sy + 0.75 * sw:.1f}" width="{sw / 8:.1f}" height="{sw / 8:.1f}" fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="1.0"/>')
    el.append(f'<rect x="{sx + 0.875 * sw:.1f}" y="{sy + 0.875 * sw:.1f}" width="{sw / 8:.1f}" height="{sw / 8:.1f}" fill="{CRIMSON_SOFT}" stroke="{CRIMSON}" stroke-width="1.0" stroke-dasharray="2 2"/>')

    el.append(txt(196, 408, "前 N 块面积和 S_N = 1 − (1/2)ᴺ，永远装在面积 1 的方框内！", size=11.4, color=INK, anchor="middle", weight="600"))
    el.append(txt(196, 428, "右下角剩余缺口 (1/2)ᴺ → 0：极限面积精确等于 1，既不溢出也不少。", size=11.2, color=MUTED, anchor="middle"))
    el.append(txt(196, 450, "• 倒退二分没有“第 1 步”，但起点 x=0 仍在闭区间 [0,1] 里！", size=11.2, color=BLUE, anchor="middle", weight="600"))

    # Right card: Cauchy partial sums — Geometric (converges to 1) vs Harmonic (diverges!) (x=388, y=66, w=352, h=404)
    el.append(card(388, 66, 352, 404))
    el.append(pill(402, 78, "右栏：无穷多项正数相加，到底有限还是无限？", fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(402, 118, "关键不在“项数是不是无穷”，而在部分和 S_N 有没有天花板：", size=11.3, color=BODY))

    # Plot N = 1..10 on x in [438, 712] (30.4 px per step), y_val in [0, 3.2] -> y in [336, 152] (57.5 px per unit)
    px0, py0 = 438.0, 336.0
    dx_n = 29.5
    dy_u = 55.0

    # Axes
    el.append(f'<line x1="{px0:.1f}" y1="{py0:.1f}" x2="{px0 + 9.6 * dx_n:.1f}" y2="{py0:.1f}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{px0:.1f}" y1="{py0:.1f}" x2="{px0:.1f}" y2="{py0 - 3.25 * dy_u:.1f}" stroke="{SLATE}" stroke-width="1.5"/>')

    for yv in (0, 1, 2, 3):
        yy = py0 - yv * dy_u
        dash = ' stroke-dasharray="5 3"' if yv == 1 else ""
        scol = BLUE if yv == 1 else HAIRLINE
        el.append(f'<line x1="{px0:.1f}" y1="{yy:.1f}" x2="{px0 + 9.2 * dx_n:.1f}" y2="{yy:.1f}" stroke="{scol}" stroke-width="{1.5 if yv == 1 else 1.0}"{dash}/>')
        el.append(txt(px0 - 8, yy + 4, f"{yv}", size=11, color=BLUE if yv == 1 else MUTED, anchor="end", weight="700" if yv == 1 else None))

    for n_val in (1, 2, 4, 6, 8, 10):
        xx = px0 + (n_val - 1) * dx_n
        el.append(f'<line x1="{xx:.1f}" y1="{py0:.1f}" x2="{xx:.1f}" y2="{py0 + 4:.1f}" stroke="{MUTED}" stroke-width="1.2"/>')
        el.append(txt(xx, py0 + 17, f"N={n_val}" if n_val == 1 else f"{n_val}", size=10.8, color=MUTED, anchor="middle"))

    # Curve 1: Harmonic partial sums H_N = sum_{k=1}^N (1/k) -> diverges!
    harm_pts = []
    h_acc = 0.0
    for n_val in range(1, 11):
        h_acc += 1.0 / n_val
        xx = px0 + (n_val - 1) * dx_n
        yy = py0 - h_acc * dy_u
        harm_pts.append((xx, yy))
    el.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in harm_pts)}" fill="none" stroke="{CRIMSON}" stroke-width="2.3"/>')
    for x, y in harm_pts:
        el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.3" fill="{CRIMSON}"/>')
    el.append(txt(724, py0 - 3.04 * dy_u, "调和级数 1+1/2+1/3+… → ∞（耗时无穷！）", size=10.8, color=CRIMSON, anchor="end", weight="700"))

    # Curve 2: Zeno geometric partial sums S_N = sum_{k=1}^N (1/2)^k = 1 - 2^-N -> converges to 1!
    geom_pts = []
    g_acc = 0.0
    for n_val in range(1, 11):
        g_acc += 0.5 ** n_val
        xx = px0 + (n_val - 1) * dx_n
        yy = py0 - g_acc * dy_u
        geom_pts.append((xx, yy))
    el.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in geom_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
    for x, y in geom_pts:
        el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{BLUE}"/>')
    el.append(txt(724, py0 - 1.18 * dy_u, "芝诺级数 1/2+1/4+1/8+… → 1（严格收敛！）", size=10.8, color=BLUE, anchor="end", weight="700"))

    # Explanation box at bottom of right card
    el.append(card(402, 368, 324, 88, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(414, 390, "柯西极限定义（1821）：无穷级数之和定义为部分和的极限", size=11.3, color=INK, weight="700"))
    el.append(txt(414, 412, "• 匀速跑步把 1 秒切成 1/2 + 1/4 + 1/8… 秒，极限 = 1 秒；", size=11.1, color=BODY))
    el.append(txt(414, 432, "• 若每段故意减速成耗时 1/k 秒，总时间才会真的发散到 ∞；", size=11.1, color=BODY))
    el.append(txt(414, 450, "• 1−1+1−1… 则因部分和在 1 与 0 间震荡而“无定义”。", size=11.1, color=MUTED))

    svg = figure(
        484,
        "芝诺二分法悖论、单位正方形几何证明与柯西收敛级数对比图解",
        "左栏展示倒退二分悖论与 1/2+1/4+1/8+... 填满单位正方形的几何证明；右栏对比收敛于 1 的芝诺等比级数与发散到无穷的调和级数。",
        el,
    )
    write_svg("zeno-paradox", "dichotomy-unit-square-sum.svg", svg)


def _build_arrow_and_stadium_svg():
    """SVG 3: The Flying Arrow (at-at motion & derivative slope) + The Moving Rows / Stadium (relative velocity & discrete grid)."""
    el = []
    el += header(
        "飞矢不动与游行队伍：另外两大运动悖论到底卡在了哪里？",
        "亚里士多德《物理学》卷六第九章记载的后两个悖论：一个拷问“瞬间速度是什么”，一个拷问“相对运动与最小微元”",
    )

    # Left card: The Flying Arrow (x=20, y=66, w=352, h=406)
    el.append(card(20, 66, 352, 406))
    el.append(pill(34, 78, "左栏：飞矢不动（The Arrow）——瞬间照片能分清动静吗？", fg=BLUE, bg=BLUE_SOFT))

    # Two snapshot boxes at t = t0 (Δt = 0)
    el.append(card(36, 112, 152, 68, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(112, 131, "时刻 t₀ 快门（Δt = 0）", size=10.8, color=BLUE, anchor="middle", weight="600"))
    el.append(f'<line x1="56" y1="152" x2="156" y2="152" stroke="{BLUE}" stroke-width="3.2" marker-end="url(#arr-blue)"/>')
    el.append(txt(112, 171, "飞行的箭：占据自身长", size=10.8, color=INK, anchor="middle"))

    el.append(card(204, 112, 152, 68, fill=SLATE_SOFT, stroke=SLATE))
    el.append(txt(280, 131, "时刻 t₀ 快门（Δt = 0）", size=10.8, color=SLATE, anchor="middle", weight="600"))
    el.append(f'<line x1="224" y1="152" x2="324" y2="152" stroke="{SLATE}" stroke-width="3.2" marker-end="url(#arr-muted)"/>')
    el.append(txt(280, 171, "桌上的箭：占据自身长", size=10.8, color=INK, anchor="middle"))

    el.append(txt(196, 202, "芝诺推理：每瞬间 Δx=0、Δt=0（0/0 无意义）⇒ 全程静止？", size=11.1, color=CRIMSON, anchor="middle", weight="600"))

    # Spacetime tangent comparison (y=218..380)
    gx, gy = 74.0, 368.0
    el.append(f'<line x1="{gx:.1f}" y1="{gy:.1f}" x2="342" y2="{gy:.1f}" stroke="{SLATE}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')
    el.append(f'<line x1="{gx:.1f}" y1="{gy:.1f}" x2="{gx:.1f}" y2="222" stroke="{SLATE}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')
    el.append(txt(gx - 8, 232, "位置 x", size=10.8, color=MUTED, anchor="end"))
    el.append(txt(340, gy + 18, "时间 t", size=10.8, color=MUTED, anchor="end"))

    # Resting arrow horizontal line: y = 326
    el.append(f'<line x1="88" y1="326" x2="326" y2="326" stroke="{SLATE}" stroke-width="2.2" stroke-dasharray="5 3"/>')
    el.append(txt(282, 344, "静止的箭：dx/dt = 0", size=10.8, color=SLATE, anchor="middle"))

    # Flying arrow curve: x(t) rising through (t0=196, y=300) with tangent slope
    el.append(f'<path d="M 88,352 Q 186,314 322,232" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')
    # Tangent line at t0 = 196 (point on quad bezier at u=0.5: x=0.25*88+0.5*186+0.25*322=195.5, y=0.25*352+0.5*314+0.25*232=303)
    el.append(f'<line x1="135.5" y1="333.0" x2="255.5" y2="273.0" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="4 2"/>')
    el.append(f'<circle cx="195.5" cy="303.0" r="4.8" fill="{CRIMSON}" stroke="#ffffff" stroke-width="1.4"/>')
    el.append(f'<line x1="195.5" y1="{gy:.1f}" x2="195.5" y2="303.0" stroke="{CRIMSON}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    el.append(txt(195.5, gy + 16, "t₀", size=11, color=CRIMSON, anchor="middle", weight="700"))
    el.append(txt(222, 256, "飞行的箭：切线斜率 v(t₀) > 0", size=11, color=BLUE, weight="700"))

    el.append(card(36, 394, 320, 64, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(48, 415, "罗素“在—在”理论 + 微积分导数：", size=11.3, color=GREEN, weight="700"))
    el.append(txt(48, 435, "运动不是在 Δt=0 内部挤出位移，而是不同时刻处在", size=11, color=BODY))
    el.append(txt(48, 451, "不同位置的函数映射 x(t)，瞬时速度是邻域差商的极限。", size=11, color=BODY))

    # Right card: The Moving Rows / Stadium (x=388, y=66, w=352, h=406)
    el.append(card(388, 66, 352, 406))
    el.append(pill(402, 78, "右栏：游行队伍（The Stadium）——一半时间等于一倍时间？", fg=ORANGE, bg=ORANGE_SOFT))

    def draw_blocks(cx_start, y_top, labels, fill_c, stroke_c, arrow_dir=0):
        bw, bh = 38.0, 22.0
        for idx, lb in enumerate(labels):
            bx = cx_start + idx * (bw + 3.0)
            el.append(f'<rect x="{bx:.1f}" y="{y_top:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="4" fill="{fill_c}" stroke="{stroke_c}" stroke-width="1.4"/>')
            el.append(txt(bx + bw / 2, y_top + 15.2, lb, size=11, color=stroke_c, anchor="middle", weight="700"))
        if arrow_dir == 1:
            rx = cx_start + len(labels) * (bw + 3.0) + 4
            el.append(f'<line x1="{rx:.1f}" y1="{y_top + 11:.1f}" x2="{rx + 26:.1f}" y2="{y_top + 11:.1f}" stroke="{stroke_c}" stroke-width="2" marker-end="url(#arr-blue)"/>')
            el.append(txt(rx + 32, y_top + 15, "+v", size=11, color=stroke_c, weight="700"))
        elif arrow_dir == -1:
            lx = cx_start - 8
            el.append(f'<line x1="{lx:.1f}" y1="{y_top + 11:.1f}" x2="{lx - 26:.1f}" y2="{y_top + 11:.1f}" stroke="{stroke_c}" stroke-width="2" marker-end="url(#arr-orange)"/>')
            el.append(txt(lx - 32, y_top + 15, "−v", size=11, color=stroke_c, anchor="end", weight="700"))

    # Stage 1: Before step (t = 0)
    el.append(txt(404, 122, "① 初态 t = 0（领头 B₃ 与领头 C₁ 同对准看台中央 A₂）：", size=11.1, color=INK, weight="600"))
    # Center A1 A2 A3 at x = 510, 551, 592
    draw_blocks(510.0, 132.0, ["A₁", "A₂", "A₃"], SLATE_SOFT, SLATE, 0)
    # B1 B2 B3 shifted 1 block left so B3 aligns with A2: x = 469, 510, 551
    draw_blocks(469.0, 160.0, ["B₁", "B₂", "B₃"], BLUE_SOFT, BLUE, 1)
    # C1 C2 C3 shifted 1 block right so C1 aligns with A2: x = 551, 592, 633
    draw_blocks(551.0, 188.0, ["C₁", "C₂", "C₃"], ORANGE_SOFT, ORANGE, -1)

    # Stage 2: After 1 unit step Δt = L/v (B moves +1 right, C moves -1 left -> all aligned!)
    el.append(txt(404, 234, "② 经 Δt = L/v 后（B 右移 1 格、C 左移 1 格，三排对齐）：", size=11.1, color=INK, weight="600"))
    draw_blocks(510.0, 244.0, ["A₁", "A₂", "A₃"], SLATE_SOFT, SLATE, 0)
    draw_blocks(510.0, 272.0, ["B₁", "B₂", "B₃"], BLUE_SOFT, BLUE, 1)
    draw_blocks(510.0, 300.0, ["C₁", "C₂", "C₃"], ORANGE_SOFT, ORANGE, -1)

    # Explanation of both the trivial relative-speed level AND the deep discrete-spacetime trap!
    el.append(card(402, 334, 324, 124, fill=AMBER_SOFT, stroke=AMBER))
    el.append(txt(414, 354, "两层拆解（别只把芝诺当成不会算相对速度！）：", size=11.3, color=AMBER, weight="700"))
    el.append(txt(414, 375, "1. 连续时空层：B₃ 掠过 1 个静止 A，却掠过 2 个反向 C，", size=10.9, color=BODY))
    el.append(txt(414, 393, "   只因相对速度 v_BC = v − (−v) = 2v，耗时都是 Δt，无矛盾。", size=10.9, color=BODY))
    el.append(txt(414, 414, "2. 离散时空暴击：若一格是“不可再分的最小空间原子”，", size=10.9, color=CRIMSON, weight="600"))
    el.append(txt(414, 432, "   Δt 是“最小时间原子”，那 B₃ 和 C₂ 何时迎面擦肩对齐？", size=10.9, color=BODY))
    el.append(txt(414, 449, "   它们竟在没有中间时刻的情况下“瞬移穿模”越过了彼此！", size=10.9, color=BODY))

    svg = figure(
        486,
        "芝诺飞矢不动与游行队伍（运动场）悖论的双栏机制拆解图",
        "左栏对比时刻快照与时空曲线切线斜率，解释罗素在-在运动观与导数；右栏展示游行队伍三排方块的相对运动及对离散原子时空观的反证。",
        el,
    )
    write_svg("zeno-paradox", "flying-arrow-and-stadium.svg", svg)


def _build_plurality_measure_svg():
    """SVG 4: Paradoxes of Plurality & Complete Divisibility — Cantor uncountable continuum & Lebesgue measure."""
    el = []
    el += header(
        "芝诺更狠的底牌“多之悖论”：无数个长度为 0 的点，凭什么拼出 1 米长的线段？",
        "微积分级数只能算“可数无穷项”，真正破解“零长点拼线段”靠的是康托尔不可数集与勒贝格测度论",
    )

    # Left card: Zeno's Two-Horned Dilemma of Complete Divisibility (x=20, y=66, w=346, h=404)
    el.append(card(20, 66, 346, 404))
    el.append(pill(34, 78, "左栏：芝诺“彻底分割”两难推理（进退皆荒谬）", fg=CRIMSON, bg=CRIMSON_SOFT, w=314))

    # Top root box
    el.append(card(56, 114, 274, 44, fill=SLATE_SOFT, stroke=SLATE))
    el.append(txt(193, 133, "把一根 1 米木棍“彻头彻尾”无限分割到底", size=11.5, color=INK, anchor="middle", weight="700"))
    el.append(txt(193, 150, "最终剩下的终极组元，尺寸 ε 是多少？", size=11, color=MUTED, anchor="middle"))

    # Branch arrows
    el.append(f'<line x1="135" y1="158" x2="104" y2="192" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')
    el.append(f'<line x1="251" y1="158" x2="282" y2="192" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')

    # Horn A (left): epsilon > 0
    el.append(card(34, 198, 148, 132, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(108, 219, "分支 A：终极微元 ε > 0", size=11.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(108, 241, "哪怕 ε 小到 10⁻¹⁰⁰ 米，", size=10.8, color=BODY, anchor="middle"))
    el.append(txt(108, 259, "无穷多个相等正数相加：", size=10.8, color=BODY, anchor="middle"))
    el.append(txt(108, 281, "ε + ε + ε + … = ∞", size=11.5, color=CRIMSON, anchor="middle", weight="700", cls="mono"))
    el.append(txt(108, 304, "结论：木棍变成无穷长！", size=10.8, color=CRIMSON, anchor="middle", weight="600"))
    el.append(txt(108, 321, "（且 ε>0 意味着还能再切）", size=10.3, color=MUTED, anchor="middle"))

    # Horn B (right): epsilon = 0
    el.append(card(204, 198, 148, 132, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(278, 219, "分支 B：终极几何点 ε = 0", size=11.2, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(278, 241, "加一个 0 不会变大，", size=10.8, color=BODY, anchor="middle"))
    el.append(txt(278, 259, "无数个 0 加起来呢？", size=10.8, color=BODY, anchor="middle"))
    el.append(txt(278, 281, "0 + 0 + 0 + … = 0 ?", size=11.5, color=CRIMSON, anchor="middle", weight="700", cls="mono"))
    el.append(txt(278, 304, "结论：木棍缩成长度 0！", size=10.8, color=CRIMSON, anchor="middle", weight="600"))
    el.append(txt(278, 321, "（整个物质世界沦为幻觉）", size=10.3, color=MUTED, anchor="middle"))

    # Bottom punchline on left card
    el.append(card(34, 346, 318, 108, fill="#ffffff", stroke=CRIMSON, dash="4 3"))
    el.append(txt(46, 368, "为什么柯西级数救不了分支 B？", size=11.4, color=CRIMSON, weight="700"))
    el.append(txt(46, 389, "• 在柯西无穷级数里，0 + 0 + 0 + … 确实严格等于 0！", size=10.9, color=BODY))
    el.append(txt(46, 409, "• 但级数求和每次只能排第 1、第 2、第 3…个点（可数无穷），", size=10.9, color=BODY))
    el.append(txt(46, 429, "  而 1 米线段上的实数点根本排不成队——它是“不可数无穷”！", size=10.9, color=INK, weight="600"))

    # Right card: Cantor Bijection + Lebesgue Measure (x=382, y=66, w=358, h=404)
    el.append(card(382, 66, 358, 404))
    el.append(pill(396, 78, "右栏：康托尔一一对应 & 测度论的终极解答", fg=GREEN, bg=GREEN_SOFT))

    # Diagram 1: Radial projection proving 1 cm and 1 m have the EXACT SAME number of points!
    apex_x, apex_y = 536.0, 120.0
    el.append(f'<circle cx="{apex_x:.1f}" cy="{apex_y:.1f}" r="3.8" fill="{PURPLE}"/>')
    el.append(txt(apex_x + 8, apex_y + 4, "投影中心 O", size=10.8, color=PURPLE, weight="600"))

    # Short segment AB (length 84 px, y=166): x in [494, 578]
    # Long segment CD (y=226): exact collinear rays from O(536, 120)
    ax1, ax2, ay = 494.0, 578.0, 166.0
    cx1, cx2, cy = 536.0 - 42.0 * (106.0 / 46.0), 536.0 + 42.0 * (106.0 / 46.0), 226.0

    # Rays from O through endpoints and 3 interior sample points
    for frac in (0.0, 0.28, 0.62, 1.0):
        px_short = ax1 + frac * (ax2 - ax1)
        px_long = cx1 + frac * (cx2 - cx1)
        col = PURPLE if frac in (0.28, 0.62) else MUTED
        sw = 1.4 if frac in (0.28, 0.62) else 1.1
        el.append(f'<line x1="{apex_x:.1f}" y1="{apex_y:.1f}" x2="{px_long:.1f}" y2="{cy:.1f}" stroke="{col}" stroke-width="{sw}" stroke-dasharray="3 2"/>')
        if frac in (0.28, 0.62):
            el.append(f'<circle cx="{px_short:.1f}" cy="{ay:.1f}" r="3.4" fill="{BLUE}"/>')
            el.append(f'<circle cx="{px_long:.1f}" cy="{cy:.1f}" r="3.4" fill="{GREEN}"/>')

    el.append(f'<line x1="{ax1:.1f}" y1="{ay:.1f}" x2="{ax2:.1f}" y2="{ay:.1f}" stroke="{BLUE}" stroke-width="3.2"/>')
    el.append(txt(ax2 + 8, ay + 4, "1 cm 线段（基数 = c）", size=10.8, color=BLUE, weight="700"))

    el.append(f'<line x1="{cx1:.1f}" y1="{cy:.1f}" x2="{cx2:.1f}" y2="{cy:.1f}" stroke="{GREEN}" stroke-width="3.6"/>')
    el.append(txt(561, cy + 20, "1 m 线段（点集基数同样 = c，点的个数一模一样！）", size=10.9, color=GREEN, anchor="middle", weight="700"))

    # Two comparison rows at bottom of right card (y=264..454)
    el.append(card(396, 262, 330, 86, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(408, 283, "① 可数稠密点集（如 [0,1] 内全部有理数 Q，基数 ℵ₀）：", size=11, color=BLUE, weight="700"))
    el.append(txt(408, 303, "虽密密麻麻，但能编号 q₁, q₂, q₃… 用长 ε/2ⁿ 的小盖子全盖住，", size=10.8, color=BODY))
    el.append(txt(408, 321, "总盖长 ≤ ε → 0，勒贝格测度 μ(Q) = 0（像筛子一样全是洞）！", size=10.8, color=BODY))
    el.append(txt(408, 339, "这正是“可数个零加起来仍是零”的精确数学体现。", size=10.6, color=MUTED))

    el.append(card(396, 358, 330, 98, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(408, 379, "② 连续实数区间 [a, b]（含无理数，不可数基数 c = 2^ℵ₀）：", size=11, color=GREEN, weight="700"))
    el.append(txt(408, 399, "1 cm 与 1 m 点的个数相同 ⇒ 单靠“数点再相加”算不出长度！", size=10.8, color=INK, weight="600"))
    el.append(txt(408, 419, "现代数学中，长度不是点尺寸的算术和，而是定义在区间集合", size=10.8, color=BODY))
    el.append(txt(408, 438, "上的测度函数 μ([a, b]) = b − a（满足可数可加性，彻底自洽）。", size=10.8, color=BODY))

    svg = figure(
        484,
        "芝诺多之悖论（彻底分割两难）与康托尔连续统及勒贝格测度解答图解",
        "左栏展示把木棍无限分割陷入微元大于零则无穷长、等于零则长度为零的两难；右栏用中心投影证明不同长度线段点集等势，并对比有理数零测度与实数区间测度。",
        el,
    )
    write_svg("zeno-paradox", "plurality-and-measure-paradox.svg", svg)


def _build_thomson_lamp_svg():
    """SVG 5: 20th-Century Supertasks & Thomson's Lamp (1954) — missing limit vs convergent trajectory."""
    el = []
    el += header(
        "汤姆逊台灯超任务（1954）：2 分钟内按无穷次开关，最后灯是亮还是灭？",
        "微积分解决了连续位移收敛，却被 20 世纪哲学家追问出一个新陷阱：如果状态序列没有极限怎么办？",
    )

    # Left card: Thomson's Lamp step waveform vs Achilles smooth limit (x=20, y=66, w=404, h=404)
    el.append(card(20, 66, 404, 404))
    el.append(pill(34, 78, "左栏：开关状态 S(t) 在 t → 2 分钟时的极限震荡", fg=ORANGE, bg=ORANGE_SOFT))

    # Plot t in [0, 2.0] min -> x in [72, 372] (150 px per min; t=2.0 at x=372)
    gx0, gx_lim = 72.0, 372.0
    scale_t = 150.0
    y_on, y_off = 154.0, 244.0

    # Axes & ON/OFF labels
    el.append(f'<line x1="{gx0:.1f}" y1="{y_off:.1f}" x2="404" y2="{y_off:.1f}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{gx0:.1f}" y1="{y_off + 8:.1f}" x2="{gx0:.1f}" y2="128" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{gx0:.1f}" y1="{y_on:.1f}" x2="{gx_lim:.1f}" y2="{y_on:.1f}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    el.append(txt(gx0 - 8, y_on + 4, "亮 (1)", size=11.2, color=ORANGE, anchor="end", weight="700"))
    el.append(txt(gx0 - 8, y_off + 4, "灭 (0)", size=11.2, color=SLATE, anchor="end", weight="700"))

    # Build exact square-wave path up to n=8: ON on [0,1), OFF on [1, 1.5), ON on [1.5, 1.75)...
    pts = []
    state = 1
    t_curr = 0.0
    dt = 1.0
    for step in range(8):
        t_next = t_curr + dt
        x1 = gx0 + t_curr * scale_t
        x2 = gx0 + t_next * scale_t
        yy = y_on if state == 1 else y_off
        pts.append((x1, yy))
        pts.append((x2, yy))
        # Shade ON intervals softly
        if state == 1:
            el.append(f'<rect x="{x1:.1f}" y="{y_on:.1f}" width="{x2 - x1:.1f}" height="{y_off - y_on:.1f}" fill="{AMBER_SOFT}" opacity="0.65"/>')
        t_curr = t_next
        dt *= 0.5
        state = 1 - state

    el.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{ORANGE}" stroke-width="2.2"/>')
    # Dense oscillation zone near t=2
    el.append(f'<rect x="{gx_lim - 5.0:.1f}" y="{y_on:.1f}" width="5.0" height="{y_off - y_on:.1f}" fill="{ORANGE}" opacity="0.45"/>')

    # Deadline vertical line at t = 2.0 min
    el.append(f'<line x1="{gx_lim:.1f}" y1="126" x2="{gx_lim:.1f}" y2="262" stroke="{CRIMSON}" stroke-width="2" stroke-dasharray="5 3"/>')
    el.append(f'<circle cx="{gx_lim:.1f}" cy="{(y_on + y_off) / 2:.1f}" r="13" fill="{CRIMSON_SOFT}" stroke="{CRIMSON}" stroke-width="1.8"/>')
    el.append(txt(gx_lim, (y_on + y_off) / 2 + 5, "?", size=15, color=CRIMSON, anchor="middle", weight="700"))
    el.append(txt(gx_lim + 8, 140, "t = 2 分钟", size=11.2, color=CRIMSON, weight="700"))

    # Time ticks
    for tv, t_lbl in [(0.0, "0"), (1.0, "1"), (1.5, "1.5"), (1.75, "1.75"), (2.0, "2.0 min")]:
        xx = gx0 + tv * scale_t
        el.append(f'<line x1="{xx:.1f}" y1="{y_off:.1f}" x2="{xx:.1f}" y2="{y_off + 5:.1f}" stroke="{INK}" stroke-width="1.3"/>')
        el.append(txt(xx, y_off + 19, t_lbl, size=10.5, color=CRIMSON if tv == 2.0 else MUTED, anchor="middle", weight="700" if tv == 2.0 else None))

    # Contrast mini-panel inside left card (y=286..454): Why Achilles converges while Lamp doesn't
    el.append(card(36, 286, 372, 168, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(50, 308, "核心差异：连续收敛 vs 离散震荡发散", size=11.5, color=INK, weight="700"))
    el.append(txt(50, 331, "• 阿喀琉斯位置序列：90, 99, 99.9… → 极限唯一存在 (= 100 m)，", size=11, color=BLUE, weight="600"))
    el.append(txt(50, 349, "  加上运动连续性，t = 10 s 时的位置被唯一锁定为 100 m。", size=10.8, color=BODY))
    el.append(txt(50, 373, "• 汤姆逊台灯状态序列：1, 0, 1, 0, 1, 0… → 极限根本不存在！", size=11, color=CRIMSON, weight="600"))
    el.append(txt(50, 391, "  每次开灯后都有更晚一次关灯，每次关灯后也都有更晚一次开灯；", size=10.8, color=BODY))
    el.append(txt(50, 409, "  不能把平均值 1/2 当答案——开关只有 0 和 1 两个离散态，", size=10.8, color=BODY))
    el.append(txt(50, 427, "  没有“半亮半灭”的中间位置！", size=10.8, color=BODY, weight="600"))

    # Right card: Benacerraf's logical resolution + Relativistic physical barrier (x=440, y=66, w=300, h=404)
    el.append(card(440, 66, 300, 404))
    el.append(pill(454, 78, "右栏：逻辑拆解与物理极限两道关", fg=PURPLE, bg=PURPLE_SOFT))

    el.append(step_badge(466, 124, 1, fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(484, 128, "贝纳塞拉夫（1962）的逻辑破案", size=11.8, color=PURPLE, weight="700"))
    el.append(txt(454, 150, "题目只规定了 t < 2 每一刻的开关规则，", size=10.9, color=BODY))
    el.append(txt(454, 168, "压根没有规定 t = 2 那一刻的状态！", size=10.9, color=INK, weight="600"))
    el.append(txt(454, 188, "• 无穷动作序列 1, 2, 3…（序数 ω）", size=10.8, color=BODY))
    el.append(txt(454, 206, "  满足“每一步都被执行完”，但不存在", size=10.8, color=BODY))
    el.append(txt(454, 224, "  所谓的“最后第 ∞ 次按键”！", size=10.8, color=CRIMSON, weight="600"))
    el.append(txt(454, 242, "• 因此 t = 2 时灯亮或灭在纯逻辑上都不", size=10.8, color=BODY))
    el.append(txt(454, 260, "  矛盾——只是题目条件欠定（不连续）。", size=10.8, color=BODY))

    el.append(f'<line x1="454" y1="278" x2="726" y2="278" stroke="{HAIRLINE}" stroke-width="1"/>')

    el.append(step_badge(466, 302, 2, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(484, 306, "真实物理宇宙为什么造不出这盏灯？", size=11.8, color=GREEN, weight="700"))
    el.append(txt(454, 328, "设按钮行程仅 δ = 1 mm，第 n 次按键", size=10.9, color=BODY))
    el.append(txt(454, 346, "必须在 Δt_n = 60 × 2⁻ⁿ 秒内完成：", size=10.9, color=BODY))
    el.append(card(454, 358, 272, 54, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(590, 378, "第 n = 35 次按键（距 2 分钟差 1.7 ns）", size=10.8, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(590, 398, "按钮速度 v₃₅ > 5.7×10⁵ m/s → 第 45 次超光速 c！", size=10.6, color=INK, anchor="middle", weight="600"))
    el.append(txt(454, 432, "结论：连续运动无需离散机械往返，而离散", size=10.8, color=BODY))
    el.append(txt(454, 450, "无限按键会被狭义相对论光速上限直接熔断。", size=10.8, color=BODY, weight="600"))

    svg = figure(
        484,
        "汤姆逊台灯超任务悖论（1954）、贝纳塞拉夫逻辑拆解与相对论光速极限图解",
        "左栏绘制汤姆逊台灯在 2 分钟内无限次按指数减半间隔开关的方波震荡及与阿喀琉斯连续极限的对比；右栏给出贝纳塞拉夫逻辑欠定分析与按钮超光速物理限制。",
        el,
    )
    write_svg("zeno-paradox", "thomson-lamp-supertask.svg", svg)


def _build_quantum_zeno_svg():
    """SVG 6: Quantum Zeno Effect — quadratic short-time survival cos^2(Omega t / 2) & NIST 1990 Be+ ion experiment."""
    el = []
    el += header(
        "量子芝诺效应：为什么在微观世界里，“一直盯着看”真能把演化冻住？",
        "Misra & Sudarshan (1977) 命名、1990 年 NIST 温兰德团队用铍离子实验证实：密集测量坍缩把跃迁硬生生按回起点",
    )

    # Left card: Exact quantum survival curves for N = 1 (unobserved), N = 4, N = 16, N = 64 measurements (x=20, y=66, w=412, h=406)
    el.append(card(20, 66, 412, 406))
    el.append(pill(34, 78, "左栏：留在初态概率 P(t) —— 二次方平顶 vs 频繁测量重置", fg=BLUE, bg=BLUE_SOFT))

    # Plot u = t / T in [0, 1] -> x in [74, 404] (330 px); P in [0, 1] -> y in [346, 136] (210 px)
    gx0, gy0 = 74.0, 346.0
    gw, gh = 330.0, 210.0

    # Grid & axes
    for pv in (0.0, 0.5, 1.0):
        yy = gy0 - pv * gh
        el.append(f'<line x1="{gx0:.1f}" y1="{yy:.1f}" x2="{gx0 + gw:.1f}" y2="{yy:.1f}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
        el.append(txt(gx0 - 8, yy + 4, f"{int(pv * 100)}%", size=10.8, color=MUTED, anchor="end"))

    el.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0 + gw + 8:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0:.1f}" y2="{gy0 - gh - 12:.1f}" stroke="{SLATE}" stroke-width="1.5"/>')

    for uv, ulbl in [(0.0, "0"), (0.25, "T/4"), (0.5, "T/2"), (0.75, "3T/4"), (1.0, "T = π/Ω")]:
        xx = gx0 + uv * gw
        el.append(f'<line x1="{xx:.1f}" y1="{gy0:.1f}" x2="{xx:.1f}" y2="{gy0 + 4:.1f}" stroke="{MUTED}" stroke-width="1.2"/>')
        el.append(txt(xx, gy0 + 18, ulbl, size=10.6, color=MUTED, anchor="middle"))

    # Helper to compute exact piecewise-reset survival curve for N projective measurements over [0, T]
    def zeno_curve_pts(n_meas, samples_per_seg=16):
        pts = []
        p_base = 1.0
        for k in range(n_meas):
            u_start = k / n_meas
            for s in range(samples_per_seg + 1):
                du = (s / samples_per_seg) / n_meas
                u = u_start + du
                p_val = p_base * (math.cos(0.5 * math.pi * du) ** 2)
                pts.append((gx0 + u * gw, gy0 - p_val * gh))
            p_base *= math.cos(0.5 * math.pi / n_meas) ** 2
        return pts, p_base

    # 1. Unobserved coherent Rabi flip (N = 1): P(u) = cos^2(pi*u/2) -> drops from 100% to 0%
    pts_1, _ = zeno_curve_pts(1, 48)
    el.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts_1)}" fill="none" stroke="{SLATE}" stroke-width="2.2" stroke-dasharray="6 3"/>')
    el.append(txt(gx0 + 0.56 * gw, gy0 - 0.22 * gh, "不观测 (N=1)：100% 跃迁走 → 剩 0%", size=10.8, color=SLATE, weight="600"))

    # 2. N = 4 measurements -> ends at 53.1%
    pts_4, p4_end = zeno_curve_pts(4, 14)
    el.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts_4)}" fill="none" stroke="{ORANGE}" stroke-width="2.1"/>')
    el.append(txt(gx0 + 0.62 * gw, gy0 - 0.57 * gh, f"测 N=4 次 → 剩 {p4_end * 100:.1f}%", size=10.8, color=ORANGE, weight="700"))

    # 3. N = 16 measurements -> ends at 85.7%
    pts_16, p16_end = zeno_curve_pts(16, 6)
    el.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts_16)}" fill="none" stroke="{BLUE}" stroke-width="2.1"/>')
    el.append(txt(gx0 + 0.58 * gw, gy0 - 0.80 * gh, f"测 N=16 次 → 剩 {p16_end * 100:.1f}%", size=10.8, color=BLUE, weight="700"))

    # 4. N = 64 measurements -> ends at 96.2%!
    pts_64, p64_end = zeno_curve_pts(64, 2)
    el.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts_64)}" fill="none" stroke="{GREEN}" stroke-width="2.6"/>')
    el.append(txt(gx0 + 0.44 * gw, gy0 - 1.03 * gh, f"密集测 N=64 次 → 剩 {p64_end * 100:.1f}%（近乎冻结！）", size=11, color=GREEN, weight="700"))

    # Highlight quadratic flat top at u -> 0
    el.append(f'<circle cx="{gx0:.1f}" cy="{gy0 - gh:.1f}" r="4.5" fill="{CRIMSON}"/>')
    el.append(txt(gx0 + 10, gy0 - gh + 18, "极短时间平顶：P(δt) ≈ 1 − c·δt²", size=10.6, color=CRIMSON, weight="700"))

    # Bottom formula box in left card
    el.append(card(34, 376, 384, 82, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(46, 397, "为什么能冻住？因为量子初态演化起步是“二次方慢热”！", size=11.2, color=BLUE, weight="700"))
    el.append(txt(46, 417, "每次隔 δt = T/N 测一下，溜走概率只有 O(1/N²)；连测 N 次累计", size=10.8, color=BODY))
    el.append(txt(46, 435, "溜走概率 N × O(1/N²) = O(1/N) → 0！当 N → ∞ 时系统永远停在初态。", size=10.8, color=INK, weight="600"))

    # Right card: 1990 NIST Beryllium-9+ experiment + Classical boundary warning (x=448, y=66, w=292, h=406)
    el.append(card(448, 66, 292, 406))
    el.append(pill(462, 78, "右栏：1990 NIST 铍离子实验 & 适用边界", fg=GREEN, bg=GREEN_SOFT))

    el.append(txt(462, 118, "Itano & Wineland 等（Phys. Rev. A, 1990）：", size=11.3, color=INK, weight="700"))
    el.append(txt(462, 137, "彭宁离子阱中约 5000 个激光冷却 ⁹Be⁺ 离子", size=10.8, color=MUTED))

    # Energy level diagram inside right card (y=148..290)
    el.append(card(462, 148, 264, 146, fill="#ffffff", stroke=BORDER))
    # Level |2> (upper, non-fluorescing)
    el.append(f'<line x1="482" y1="176" x2="588" y2="176" stroke="{PURPLE}" stroke-width="2.6"/>')
    el.append(txt(482, 168, "激发超精细态 |2⟩（暗态）", size=10.8, color=PURPLE, weight="700"))
    # Level |1> (ground, strongly scattering UV probe)
    el.append(f'<line x1="482" y1="244" x2="588" y2="244" stroke="{BLUE}" stroke-width="2.6"/>')
    el.append(txt(482, 262, "基态 |1⟩（初态）", size=10.8, color=BLUE, weight="700"))
    # Auxiliary fast-decay level |3> for UV probe measurement
    el.append(f'<line x1="616" y1="168" x2="712" y2="168" stroke="{GREEN}" stroke-width="2.4"/>')
    el.append(txt(664, 160, "探测态 |3⟩", size=10.6, color=GREEN, anchor="middle", weight="700"))

    # RF continuous drive arrow between |1> and |2>
    el.append(f'<line x1="534" y1="238" x2="534" y2="184" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
    el.append(txt(542, 214, "射频场慢推", size=10.5, color=ORANGE, weight="600"))
    el.append(txt(542, 228, "(T=256 ms)", size=10, color=MUTED))

    # Short UV laser measurement pulses |1> <-> |3>
    el.append(f'<line x1="588" y1="240" x2="646" y2="174" stroke="{GREEN}" stroke-width="2" stroke-dasharray="4 2" marker-end="url(#arr-green)"/>')
    el.append(txt(658, 216, "N 次紫外脉冲", size=10.5, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(658, 232, "散射光子=点名!", size=10.3, color=GREEN, anchor="middle"))
    el.append(txt(594, 282, "实测 N 从 1 增至 64：跃迁率从近 100% 跌至 ~1%！", size=10.6, color=INK, anchor="middle", weight="600"))

    # Boundary warning card (y=306..458)
    el.append(card(462, 306, 264, 152, fill=CRIMSON_SOFT, stroke=CRIMSON))
    el.append(txt(474, 327, "重要科学边界：别误当成宏观定身术！", size=11.2, color=CRIMSON, weight="700"))
    el.append(txt(474, 348, "1. 盯着飞矢看，箭绝不会停在半空：", size=10.8, color=INK, weight="600"))
    el.append(txt(474, 366, "   宏观箭由 ~10²⁴ 个原子组成且早已环境退相干，", size=10.6, color=BODY))
    el.append(txt(474, 383, "   人眼看反光不会把整支箭投影回单一量子初态。", size=10.6, color=BODY))
    el.append(txt(474, 404, "2. 甚至还有“反芝诺效应”（Kofman & Kurizki）：", size=10.8, color=INK, weight="600"))
    el.append(txt(474, 422, "   在某些连续谱衰变体系中，特定频率的观测反而", size=10.6, color=BODY))
    el.append(txt(474, 439, "   会加速衰变——关键取决于短时能谱结构！", size=10.6, color=BODY))

    svg = figure(
        486,
        "量子芝诺效应短时二次方存活率曲线与 1990 年 NIST 铍离子实验原理图解",
        "左栏精确计算 N=1,4,16,64 次投影测量下的存活概率曲线，展示 96.2% 冻结效果；右栏展示 NIST 铍离子三能级探测机制并阐明不能外推到宏观飞矢的科学边界。",
        el,
    )
    write_svg("zeno-paradox", "quantum-zeno-effect.svg", svg)


@register("zeno-paradox", "Zeno's paradoxes of motion, plurality, supertasks & quantum Zeno", "mathematics")
def build_zeno_paradox():
    print("[zeno-paradox] building & verifying assertions...")
    _verify_zeno_math()
    _build_achilles_tortoise_svg()
    _build_dichotomy_square_svg()
    _build_arrow_and_stadium_svg()
    _build_plurality_measure_svg()
    _build_thomson_lamp_svg()
    _build_quantum_zeno_svg()
