"""6 original 760px Chinese SVGs for the Satellite Flight Principles & Full Lifecycle post."""

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
    pill,
    register,
    txt,
    write_svg,
)

RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"


def _line(x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, marker=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'

TOPIC = "satellite-flight"
MU_EARTH = 398600.4418  # km^3 / s^2
R_EARTH = 6378.137      # km


def _solve_kepler(M: float, e: float) -> float:
    """Solve M = E - e*sin(E) by Newton-Raphson."""
    E = M
    for _ in range(25):
        E -= (E - e * math.sin(E) - M) / (1.0 - e * math.cos(E))
    return E


def _verify_satellite_flight_math() -> None:
    # 1. Molniya orbit: T = 43082 s (half sidereal day), h_p = 500 km, e = 0.722 -> check v_p, v_a & critical i
    T_mol = 86164.09 / 2.0
    a_mol = (MU_EARTH * (T_mol / (2.0 * math.pi)) ** 2) ** (1.0 / 3.0)
    assert 26550 < a_mol < 26565
    r_p_mol = R_EARTH + 500.0
    r_a_mol = 2.0 * a_mol - r_p_mol
    h_a_mol = r_a_mol - R_EARTH
    assert 39800 < h_a_mol < 39950
    v_p_mol = math.sqrt(MU_EARTH * (2.0 / r_p_mol - 1.0 / a_mol))
    v_a_mol = math.sqrt(MU_EARTH * (2.0 / r_a_mol - 1.0 / a_mol))
    assert 9.95 < v_p_mol < 10.10
    assert 1.45 < v_a_mol < 1.55
    i_crit = math.degrees(math.acos(1.0 / math.sqrt(5.0)))
    assert abs(i_crit - 63.435) < 0.01

    # 2. Hohmann transfer from 200 km circular LEO to 35,786 km circular GEO
    r1 = R_EARTH + 200.0
    r2 = 42164.17
    v1 = math.sqrt(MU_EARTH / r1)
    v2 = math.sqrt(MU_EARTH / r2)
    a_t = 0.5 * (r1 + r2)
    vp_t = math.sqrt(MU_EARTH * (2.0 / r1 - 1.0 / a_t))
    va_t = math.sqrt(MU_EARTH * (2.0 / r2 - 1.0 / a_t))
    dv1 = vp_t - v1
    dv2 = v2 - va_t
    t_coast_hr = math.pi * math.sqrt(a_t ** 3 / MU_EARTH) / 3600.0
    assert 2.45 < dv1 < 2.47
    assert 1.47 < dv2 < 1.49
    assert 5.24 < t_coast_hr < 5.27  # ~5 hr 15 min

    # 3. Graveyard +300 km above GEO vs direct deorbit from GEO
    r_grave = r2 + 300.0
    a_g = 0.5 * (r2 + r_grave)
    dv_grave = (math.sqrt(MU_EARTH * (2.0 / r2 - 1.0 / a_g)) - v2) + (
        math.sqrt(MU_EARTH / r_grave) - math.sqrt(MU_EARTH * (2.0 / r_grave - 1.0 / a_g))
    )
    assert 0.0108 < dv_grave < 0.0110  # ~10.9 m/s


# ---------------------------------------------------------------------------
# 1. Ascent Staging, Fairing Jettison & LEOP First-Hour Timeline
# ---------------------------------------------------------------------------
def build_ascent_leop() -> None:
    W, H = 760, 536
    el = []
    el.append(txt(W / 2, 30, "从地面铁塔到太空独立生活：10 分钟多级接力与黄金 60 分钟唤醒", size=19, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "一边像竹笋剥壳甩掉 96% 死重冲出大气层，一边赶在蓄电池耗尽前展开太阳翼“晒太阳续命”", size=12.5, color=MUTED, anchor="middle"))

    # Left panel: Ascent staging & fairing jettison (T+0 to T+10 min)
    el.append(card(22, 68, 366, 444))
    el.append(txt(40, 95, "第一阶段：动力入轨段（约 8–10 分钟）", size=15, weight="700", color=BLUE))

    # Atmosphere background bands inside sub-plot
    px, py, pw, ph = 42, 112, 326, 250
    el.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="#0f172a"/>')
    el.append(f'<rect x="{px}" y="{py+148}" width="{pw}" height="52" fill="#1e3a8a" opacity="0.55"/>')
    el.append(f'<rect x="{px}" y="{py+200}" width="{pw}" height="50" rx="4" fill="#0284c7" opacity="0.45"/>')
    # Karman line 100 km dashed
    ky = py + 148
    el.append(_line(px + 8, ky, px + pw - 8, ky, stroke="#38bdf8", sw=1.3, dash="5 4"))
    el.append(txt(px + pw - 10, ky - 6, "100 km 卡门线（太空边界）", size=10.5, color="#7dd3fc", anchor="end"))
    el.append(txt(px + pw - 10, py + 242, "稠密对流层 / 平流层", size=10.5, color="#bae6fd", anchor="end"))

    # Ascent curve from (64, 348) to (342, 144)
    el.append(
        '<path d="M 64 348 C 78 292, 118 228, 184 184 C 236 152, 290 144, 342 144" '
        'fill="none" stroke="#f97316" stroke-width="3.2" marker-end="url(#arr-orange)"/>'
    )
    pts = [
        (64, 348, "① 点火", "T+0 s", 76, 340),
        (114, 274, "② 助推/一级分离", "T+135 s · ~65 km", 126, 278),
        (188, 182, "③ 抛整流罩", "T+195 s · ~110 km", 196, 194),
        (320, 144, "④ 星箭分离", "T+540 s · 7.7 km/s", 232, 128),
    ]
    for cx, cy, lbl1, lbl2, lx, ly in pts:
        el.append(f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="#fb923c" stroke="#ffffff" stroke-width="1.8"/>')
        el.append(txt(lx, ly, lbl1, size=11, weight="700", color="#ffffff"))
        el.append(txt(lx, ly + 14, lbl2, size=10.5, color="#cbd5e1"))

    # Clamshell fairing icon near ③
    el.append('<path d="M 176 164 C 170 154, 174 146, 182 144" fill="none" stroke="#fde047" stroke-width="2"/>')
    el.append('<path d="M 196 172 C 204 166, 206 156, 202 148" fill="none" stroke="#fde047" stroke-width="2"/>')

    # Explanation box under ascent plot
    el.append(card(40, 374, 330, 124, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(54, 396, "为什么要早早“剥蚌壳”（抛整流罩）？", size=12.5, weight="700", color=BLUE))
    el.append(txt(54, 417, "• 低空罩住卫星：防超音速气动暴压与摩擦高温；", size=11.2, color=BODY))
    el.append(txt(54, 437, "• 冲过 110 km 后空气近真空，热流跌破 1,135 W/m²", size=11.2, color=BODY))
    el.append(txt(54, 456, "  （约等于阳光强度），立刻解锁甩掉几吨重壳！", size=11.2, color=BODY))
    el.append(txt(54, 478, "• 星箭分离靠精密弹簧轻推（Δv ≈ 0.5–1.5 m/s）。", size=11.2, weight="700", color=INK))

    # Right panel: LEOP ("Launch and Early Orbit Phase") 4 steps
    el.append(card(402, 68, 336, 444))
    el.append(txt(420, 95, "第二阶段：生死早期轨道段（LEOP）", size=15, weight="700", color=GREEN))
    el.append(txt(420, 115, "星箭分离后蓄电池仅够撑 45–90 分钟，四步自主求生：", size=11.2, color=MUTED))

    steps = [
        (
            128, 84, ORANGE_SOFT, "#fdba74", ORANGE,
            "⑤ 微动开关唤醒 & 阻尼消旋（1–5 分钟）",
            "分离弹射常带微弱翻滚；星载电脑自动苏醒，",
            "靠陀螺仪测转速并点动微推力器把翻滚刹停。",
        ),
        (
            222, 92, GREEN_SOFT, "#86efac", GREEN,
            "⑥ 解锁展开太阳翼 & 寻日充电（生死红线！）",
            "切割器剪断压紧绳，折叠太阳翼如手风琴展开；",
            "太阳敏感器寻日对准阳光——充电电流涌入母线",
            "那一刻，测控大厅才会爆发出真正的欢呼！",
        ),
        (
            324, 82, PURPLE_SOFT, "#d8b4fe", PURPLE,
            "⑦ 展开通信天线 & 锁定测控网（TT&C）",
            "建立双向遥测遥控链路，下传全星几千个温度",
            "电压体检数据，星敏感器拍星空锁死三轴姿态。",
        ),
        (
            416, 82, TEAL_SOFT, "#99f6e4", TEAL,
            "⑧ 在轨测试与变轨就位（数天至数月）",
            "依次开机相机与转发器，执行霍曼变轨或电推",
            "爬升，抵达预定“空中车位”后交付业务运行。",
        ),
    ]
    for sy, sh, bg, bd, col, h1, b1, *rest in steps:
        el.append(card(418, sy, 304, sh, rx=10, fill=bg, stroke=bd))
        el.append(txt(430, sy + 22, h1, size=12, weight="700", color=col))
        el.append(txt(430, sy + 42, b1, size=11, color=BODY))
        for idx, rline in enumerate(rest):
            el.append(txt(430, sy + 60 + idx * 17, rline, size=11, color=BODY))

    write_svg(
        TOPIC,
        "ascent-staging-fairing-leop-timeline.svg",
        figure(H, "卫星发射多级接力、抛整流罩与早期轨道段唤醒时间轴", "展示动力入轨段四次关键分离与星箭分离后黄金60分钟自主展开太阳翼寻日求生流程", el),
    )


# ---------------------------------------------------------------------------
# 2. Vis-Viva Equation & Molniya Equal-Time Orbital Loitering
# ---------------------------------------------------------------------------
def build_vis_viva_molniya() -> None:
    W, H = 760, 524
    el = []
    el.append(txt(W / 2, 30, "不踩油门凭什么飞十几年？活力公式与“近快远慢”悬停魔术", size=19, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "引力与惯性永恒拔河：每 1 小时打一个点，高偏心“闪电轨道”自动在北极头顶慢放 8 小时", size=12.5, color=MUTED, anchor="middle"))

    el.append(card(22, 68, 392, 434))
    el.append(txt(40, 95, "12 小时“闪电轨道”等时间间隔（每 1 小时 1 点）", size=14.2, weight="700", color=INK))

    e = 0.722
    a_px = 142.0
    b_px = a_px * math.sqrt(1.0 - e * e)
    tilt = math.radians(-55.0)
    fx, fy = 132.0, 366.0
    ux, uy = math.cos(tilt), math.sin(tilt)
    vx, vy = -math.sin(tilt), math.cos(tilt)

    def orb_pt(E_val: float) -> tuple[float, float]:
        along = a_px * (e - math.cos(E_val))
        perp = b_px * math.sin(E_val)
        return (fx + along * ux + perp * vx, fy + along * uy + perp * vy)

    Ep1, Ep2 = _solve_kepler(-math.pi / 12, e), _solve_kepler(math.pi / 12, e)
    p_wedge = [(fx, fy)] + [orb_pt(Ep1 + (Ep2 - Ep1) * k / 16) for k in range(17)]
    el.append(
        '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in p_wedge) + '" '
        'fill="#fed7aa" stroke="#f97316" stroke-width="1.2" opacity="0.78"/>'
    )
    Ea1, Ea2 = _solve_kepler(math.pi - math.pi / 12, e), _solve_kepler(math.pi + math.pi / 12, e)
    a_wedge = [(fx, fy)] + [orb_pt(Ea1 + (Ea2 - Ea1) * k / 16) for k in range(17)]
    el.append(
        '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in a_wedge) + '" '
        'fill="#bbf7d0" stroke="#16a34a" stroke-width="1.2" opacity="0.78"/>'
    )

    path_pts = [orb_pt(2.0 * math.pi * k / 120) for k in range(121)]
    el.append(
        '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in path_pts) + '" '
        'fill="none" stroke="#2563eb" stroke-width="2.4"/>'
    )

    r_earth_px = 25
    el.append(f'<circle cx="{fx}" cy="{fy}" r="{r_earth_px}" fill="#dbeafe" stroke="{BLUE}" stroke-width="2.2"/>')
    el.append(_line(fx - 33, fy, fx + 33, fy, stroke=MUTED, sw=1.1, dash="3 3"))
    el.append(txt(fx, fy + 4, "地球", size=11.5, weight="700", color=BLUE, anchor="middle"))

    for hr in range(12):
        M_val = 2.0 * math.pi * hr / 12.0
        E_val = _solve_kepler(M_val, e)
        px_i, py_i = orb_pt(E_val)
        col = ORANGE if hr in (0, 1, 11) else GREEN
        el.append(f'<circle cx="{px_i:.1f}" cy="{py_i:.1f}" r="5.0" fill="{col}" stroke="#ffffff" stroke-width="1.5"/>')
        if hr in (0, 2, 4, 6, 8, 10):
            dx = -16 if hr in (0, 10) else (11 if hr in (2, 4) else 10)
            dy = 15 if hr == 0 else (-10 if hr == 6 else 4)
            el.append(txt(px_i + dx, py_i + dy, f"{hr}h", size=10.5, weight="700", color=col, halo=True))

    el.append(txt(40, 434, "近地点 h = 500 km", size=11.5, weight="700", color=ORANGE))
    el.append(txt(40, 452, "狂飙 vp = 10.0 km/s（嗖地掠过南半球）", size=11, color=BODY))
    el.append(txt(40, 124, "远地点 ha = 39,870 km", size=11.5, weight="700", color=GREEN))
    el.append(txt(40, 142, "慢走 va = 1.5 km/s（连盯北极 8 小时！）", size=11, color=BODY))
    el.append(txt(40, 484, "两块彩色扇形耗时同为 1 小时，扫过面积严格相等（开普勒第二定律）", size=10.6, weight="600", color=PURPLE))

    el.append(card(428, 68, 310, 434))
    el.append(txt(446, 95, "天体力学总开关：活力公式", size=15, weight="700", color=PURPLE))

    el.append(card(444, 110, 278, 86, rx=10, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(583, 138, "v² = μ ( 2 / r − 1 / a )", size=16.5, weight="700", color=PURPLE, anchor="middle"))
    el.append(txt(583, 161, "r：当前到地心距离 · a：椭圆半长轴", size=11, color=BODY, anchor="middle"))
    el.append(txt(583, 180, "总机械能 E = −μm / (2a) 全程守恒！", size=11, weight="700", color=INK, anchor="middle"))

    notes = [
        (
            210, 88, BLUE_SOFT, BLUE_LINE, BLUE,
            "① 正圆轨道特例（r = a）",
            "代入得 v = √(μ/r)：高度越高，引力越弱，",
            "巡航反而越慢（400 km 跑 7.67 km/s，静止轨",
            "3.07 km/s），完全不需要发动机持续推着走！",
        ),
        (
            310, 86, GREEN_SOFT, "#86efac", GREEN,
            "② 椭圆轨道自动“能量换挡”",
            "爬向远地点：引力拉后腿，动能自动存成势能；",
            "跌回近地点：势能兑现回动能，一滴油不烧",
            "就能让卫星在目标上空“定点慢放”！",
        ),
        (
            408, 80, ORANGE_SOFT, "#fdba74", ORANGE,
            "③ 63.4° 临界倾角锁死远地点",
            "赤道鼓包会使普通椭圆拱线漂移；唯独令",
            "5cos²i − 1 = 0（i = 63.43°），远地点永远",
            "钉在北半球不南漂——3 颗星全天覆盖北极！",
        ),
    ]
    for ny, nh, bg, bd, col, h1, *lines_txt in notes:
        el.append(card(444, ny, 278, nh, rx=10, fill=bg, stroke=bd))
        el.append(txt(456, ny + 21, h1, size=12, weight="700", color=col))
        for k, lt in enumerate(lines_txt):
            el.append(txt(456, ny + 40 + k * 16, lt, size=10.8, color=BODY))

    write_svg(
        TOPIC,
        "vis-viva-elliptical-orbit-molniya.svg",
        figure(H, "卫星活力公式与闪电高椭圆轨道等时间间隔悬停原理图", "精确求解开普勒方程绘制12小时闪电轨道每1小时点位，展示近快远慢与开普勒第二定律等面积扇形", el),
    )


# ---------------------------------------------------------------------------
# 3. Hohmann Two-Burn Fast Transfer (Animated) vs Electric Spiral Slow Climb
# ---------------------------------------------------------------------------
def build_hohmann_vs_electric() -> None:
    W, H = 760, 532
    extra_css = """
      .anim-hohmann {
        stroke-dasharray: 520;
        stroke-dashoffset: 520;
        animation: hohmannTransfer 3.6s cubic-bezier(0.32, 0.08, 0.24, 1) 0.3s 1 forwards;
      }
      @keyframes hohmannTransfer {
        from { stroke-dashoffset: 520; }
        to   { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .anim-hohmann {
          animation: none !important;
          stroke-dashoffset: 0 !important;
        }
      }
    """
    el = []
    el.append(txt(W / 2, 30, "太空变道怎么换高轨？霍曼两脚油门快车 vs 离子电推螺旋慢车", size=19, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "一边是化学火箭 5 小时 15 分滑行到位，一边是“一张纸推力”连推几个月省下一半燃料重", size=12.5, color=MUTED, anchor="middle"))

    el.append(card(22, 68, 356, 442))
    el.append(pill(38, 82, "方案 A：化学推进 · 霍曼转移（1925）", fg=ORANGE, bg=ORANGE_SOFT, w=262))

    cx, cy = 200, 266
    r_leo = 34
    r_geo = 122
    el.append(f'<circle cx="{cx}" cy="{cy}" r="{r_geo}" fill="none" stroke="{GREEN}" stroke-width="2.2" stroke-dasharray="6 4"/>')
    el.append(f'<circle cx="{cx}" cy="{cy}" r="{r_leo}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
    el.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    el.append(txt(cx, cy + 4, "地球", size=11, weight="700", color=BLUE, anchor="middle"))

    a_t, b_t = 78.0, math.sqrt(78.0 ** 2 - 44.0 ** 2)
    arc_d = f"M {cx} {cy + r_leo} A {b_t:.1f} {a_t:.1f} 0 0 0 {cx} {cy - r_geo}"
    el.append(f'<path d="{arc_d}" fill="none" stroke="#fed7aa" stroke-width="4"/>')
    el.append(f'<path class="anim-hohmann" d="{arc_d}" fill="none" stroke="{ORANGE}" stroke-width="3.6" marker-end="url(#arr-orange)"/>')

    el.append(f'<circle cx="{cx}" cy="{cy + r_leo}" r="6" fill="{RED}" stroke="#ffffff" stroke-width="1.8"/>')
    el.append(_line(cx, cy + r_leo, cx + 48, cy + r_leo, stroke=RED, sw=2.6, marker="arr-orange"))
    el.append(txt(cx, cy + r_leo + 20, "① 近地点点火 Δv₁ = +2.46 km/s", size=11.2, weight="700", color=RED, anchor="middle"))
    el.append(txt(cx, cy + r_leo + 36, "（借奥伯特效应在高速井底猛踹一脚）", size=10.5, color=MUTED, anchor="middle"))

    el.append(f'<circle cx="{cx}" cy="{cy - r_geo}" r="6" fill="{GREEN}" stroke="#ffffff" stroke-width="1.8"/>')
    el.append(_line(cx, cy - r_geo, cx - 50, cy - r_geo, stroke=GREEN, sw=2.6, marker="arr-green"))
    el.append(txt(cx, cy - r_geo - 12, "② 远地点圆化点火 Δv₂ = +1.48 km/s", size=11.2, weight="700", color=GREEN, anchor="middle"))

    el.append(txt(cx + 76, cy - 22, "熄火滑行", size=11.2, weight="700", color=ORANGE))
    el.append(txt(cx + 76, cy - 5, "5 小时 15 分", size=11.2, weight="700", color=ORANGE))

    el.append(card(38, 404, 324, 92, rx=10, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(50, 426, "快车特点：两脚切向点火、当天到站", size=12, weight="700", color=ORANGE))
    el.append(txt(50, 446, "• 近地点拉高对岸远地点；远地点抬平近地点（圆化）。", size=10.8, color=BODY))
    el.append(txt(50, 464, "• 推力几百牛，但化学排气慢（ve ≈ 3.1 km/s），", size=10.8, color=BODY))
    el.append(txt(50, 482, "  整颗星将近一半起飞重量都得拿来装变轨燃料！", size=10.8, weight="700", color=INK))

    el.append(card(392, 68, 346, 442))
    el.append(pill(408, 82, "方案 B：全电推卫星 · 氙离子螺旋慢爬", fg=BLUE, bg=BLUE_SOFT, w=268))

    cx2, cy2 = 565, 258
    el.append(f'<circle cx="{cx2}" cy="{cy2}" r="{r_geo}" fill="none" stroke="{GREEN}" stroke-width="2.2" stroke-dasharray="6 4"/>')
    el.append(f'<circle cx="{cx2}" cy="{cy2}" r="22" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    el.append(txt(cx2, cy2 + 4, "地球", size=11, weight="700", color=BLUE, anchor="middle"))

    turns = 5.5
    sp_pts = []
    steps_sp = 260
    for k in range(steps_sp + 1):
        frac = k / steps_sp
        ang = -2.0 * math.pi * turns * frac + math.pi / 2
        rr = 32.0 + (r_geo - 32.0) * frac
        sp_pts.append((cx2 + rr * math.cos(ang), cy2 + rr * math.sin(ang)))
    el.append(
        '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in sp_pts) + '" '
        f'fill="none" stroke="{BLUE}" stroke-width="2.0" marker-end="url(#arr-blue)"/>'
    )
    el.append(txt(cx2, cy2 - r_geo - 10, "目标静止轨道 GEO（35,786 km）", size=11.2, weight="700", color=GREEN, anchor="middle"))
    el.append(txt(cx2, cy2 + 134, "绕地数千圈持续微推爬升", size=11, weight="700", color=BLUE, anchor="middle"))

    el.append(card(408, 404, 314, 92, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(420, 426, "慢车特点：硬币级微推力，比冲翻 5–10 倍！", size=12, weight="700", color=BLUE))
    el.append(txt(420, 446, "• 电场把氙离子加速到 15–30 km/s 喷出（蓝紫羽流）；", size=10.8, color=BODY))
    el.append(txt(420, 464, "• 推力仅 0.1–0.5 N（托一枚硬币），爬升需 3–6 个月，", size=10.8, color=BODY))
    el.append(txt(420, 482, "  但省下 1–2 吨燃料死重，直接让运载火箭小一号！", size=10.8, weight="700", color=INK))

    write_svg(
        TOPIC,
        "hohmann-vs-electric-spiral-transfer.svg",
        figure(H, "化学霍曼双脉冲转移与全电推进离子螺旋升轨对比图", "左侧单次动画演示霍曼转移两次切向点火与5小时15分滑行，右侧展示氙离子电推进数月螺旋爬升", el, extra_css=extra_css),
    )


# ---------------------------------------------------------------------------
# 4. Orbital Rendezvous Paradox ("Brake to Speed Up" & Gemini IV Lesson)
# ---------------------------------------------------------------------------
def build_rendezvous_paradox() -> None:
    W, H = 760, 524
    el = []
    el.append(txt(W / 2, 30, "太空超车大反直觉：为什么猛踩油门反而追丢，踩刹车才能追上前车？", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "1965 年“双子星 4 号”烧掉 42% 燃料买来的教训：加速 = 升上慢车道，减速 = 切入内圈超车道", size=12.5, color=MUTED, anchor="middle"))

    el.append(card(22, 68, 356, 336))
    el.append(pill(38, 82, "错觉翻车：1965 双子星 4 号直踩油门", fg=RED, bg=RED_SOFT, w=266))

    cx, cy = 200, 430
    el.append(f'<path d="M 48 314 A 240 240 0 0 1 352 314" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 4"/>')
    el.append(txt(205, 256, "目标空间站圆轨（v₀，周期 T₀）", size=10.8, color=MUTED, anchor="middle"))

    ang_tgt = math.radians(-68)
    tx, ty = cx + 240 * math.cos(ang_tgt), cy + 240 * math.sin(ang_tgt)
    el.append(f'<rect x="{tx-9:.1f}" y="{ty-6:.1f}" width="18" height="12" rx="3" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(tx + 14, ty + 4, "前车（目标）", size=11.2, weight="700", color=GREEN))

    ang_ch = math.radians(-110)
    sx, sy = cx + 240 * math.cos(ang_ch), cy + 240 * math.sin(ang_ch)
    el.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="6.5" fill="{RED}" stroke="#ffffff" stroke-width="1.6"/>')
    el.append(txt(116, 228, "后车猛踩油门 Δv > 0", size=11, weight="700", color=RED, anchor="middle"))

    el.append(
        f'<path d="M {sx:.1f} {sy:.1f} Q 186 144 238 152" fill="none" stroke="{RED}" stroke-width="3" marker-end="url(#arr-orange)"/>'
    )
    el.append(txt(200, 128, "被甩进更高外圈：周期变长、越追越远！", size=11.2, weight="700", color=RED, anchor="middle"))

    el.append(card(38, 322, 324, 68, rx=9, fill=RED_SOFT, stroke="#fca5a5"))
    el.append(txt(50, 344, "铁律：向前加速 → 半长轴 a 变大 → T ∝ a^(3/2) 变长", size=11, weight="700", color=RED))
    el.append(txt(50, 363, "麦克迪维特对着泰坦二级直喷追赶，结果飞到头顶越落", size=10.6, color=BODY))
    el.append(txt(50, 379, "越远，白烧 42% 燃料被迫放弃——太空不是地面高速路！", size=10.6, color=BODY))

    el.append(card(392, 68, 346, 336))
    el.append(pill(408, 82, "正确超车：先踩刹车切入低轨“超车道”", fg=GREEN, bg=GREEN_SOFT, w=272))

    cx2, cy2 = 565, 430
    el.append(f'<path d="M 416 314 A 240 240 0 0 1 714 314" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 4"/>')
    el.append(f'<path d="M 438 338 A 198 198 0 0 1 692 338" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')

    sx2, sy2 = cx2 + 240 * math.cos(math.radians(-112)), cy2 + 240 * math.sin(math.radians(-112))
    mx2, my2 = cx2 + 198 * math.cos(math.radians(-90)), cy2 + 198 * math.sin(math.radians(-90))
    ex2, ey2 = cx2 + 240 * math.cos(math.radians(-68)), cy2 + 240 * math.sin(math.radians(-68))

    el.append(f'<path d="M {sx2:.1f} {sy2:.1f} Q 518 228 {mx2:.1f} {my2:.1f} Q 608 228 {ex2:.1f} {ey2:.1f}" fill="none" stroke="{GREEN}" stroke-width="3" marker-end="url(#arr-green)"/>')
    el.append(f'<circle cx="{sx2:.1f}" cy="{sy2:.1f}" r="6" fill="{BLUE}" stroke="#ffffff" stroke-width="1.6"/>')
    el.append(f'<rect x="{ex2-9:.1f}" y="{ey2-6:.1f}" width="18" height="12" rx="3" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/>')

    el.append(txt(422, 186, "① 向后刹车 Δv < 0", size=11, weight="700", color=BLUE))
    el.append(txt(mx2, my2 + 22, "② 内圈周长短 + 线速度更快，下方超车！", size=10.8, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(714, 186, "③ 追平再加速升轨", size=11, weight="700", color=GREEN, anchor="end"))

    el.append(card(408, 322, 314, 68, rx=9, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(420, 344, "神舟 / 天舟飞船追“天宫”空间站同款秘籍：", size=11, weight="700", color=GREEN))
    el.append(txt(420, 363, "先在比空间站低几十公里的调相轨道快速追赶缩小相位差，", size=10.6, color=BODY))
    el.append(txt(420, 379, "追到前下方后再分级点火抬轨，最快 2 小时精准对接！", size=10.6, color=BODY))

    el.append(card(22, 418, 716, 86, rx=12, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(40, 443, "同源奇观——“大气阻力悖论”：为什么低轨卫星被稀薄空气摩擦，速度反而越掉越快？", size=12.8, weight="700", color=PURPLE))
    el.append(txt(40, 465, "圆轨道总机械能 E = −μm/(2r)，而动能 Ek = +μm/(2r) = −E！空气阻力每摩掉 1 焦耳总能量（ΔE = −1 J），轨道降低，", size=11, color=BODY))
    el.append(txt(40, 485, "地球引力立刻把 2 焦耳势能兑换成动能（ΔEk = +1 J）——卫星一边螺旋下坠，一边越飞越快，直至冲入稠密大气烧毁！", size=11, weight="700", color=INK))

    write_svg(
        TOPIC,
        "orbital-rendezvous-brake-to-catch-paradox.svg",
        figure(H, "太空交会对接踩刹车超车悖论与大气阻力加速悖论图解", "对比1965年双子星4号直踩油门升入高慢轨追丢目标与正确向后减速切入内圈超车道流程", el),
    )


# ---------------------------------------------------------------------------
# 5. Attitude Control (Star Tracker + Reaction Wheels) & Orbit Station-Keeping
# ---------------------------------------------------------------------------
def build_attitude_station_keeping() -> None:
    W, H = 760, 528
    el = []
    el.append(txt(W / 2, 30, "在天上怎么稳住镜头与车位？无燃料飞轮调姿与终身轨道维持", size=19, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "姿态控制负责“眼睛朝哪看”（角秒级稳像），轨道维持负责对抗大气阻力与日月拉扯“不跑偏”", size=12.5, color=MUTED, anchor="middle"))

    el.append(card(22, 68, 362, 438))
    el.append(txt(40, 95, "姿态控制（AACS）：不喷气怎么转身？", size=15, weight="700", color=BLUE))

    bx, by, bw, bh = 135, 156, 136, 118
    el.append(f'<rect x="52" y="194" width="76" height="38" rx="4" fill="#1d4ed8" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(f'<rect x="278" y="194" width="76" height="38" rx="4" fill="#1d4ed8" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(_line(90, 194, 90, 232, stroke="#93c5fd", sw=1))
    el.append(_line(316, 194, 316, 232, stroke="#93c5fd", sw=1))
    el.append(_line(128, 213, 135, 213, stroke=INK, sw=2.5))
    el.append(_line(271, 213, 278, 213, stroke=INK, sw=2.5))

    el.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="2.2"/>')
    el.append('<polygon points="188,156 178,128 208,128 198,156" fill="#e2e8f0" stroke="#334155" stroke-width="1.6"/>')
    el.append(txt(203, 120, "星敏感器（拍星空认星座定姿）", size=10.8, weight="700", color=INK, anchor="middle"))

    el.append(f'<ellipse cx="182" cy="202" rx="22" ry="8" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    el.append(f'<ellipse cx="226" cy="214" rx="8" ry="22" fill="#dcfce7" stroke="{GREEN}" stroke-width="2"/>')
    el.append(f'<circle cx="186" cy="240" r="15" fill="#f3e8ff" stroke="{PURPLE}" stroke-width="2"/>')
    el.append(txt(203, 294, "三轴正交反作用飞轮：飞轮顺转 → 卫星逆转", size=11, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(203, 312, "（内部角动量守恒 Is·ωs = −Iw·ωw，用电不用油！）", size=10.5, color=MUTED, anchor="middle"))

    el.append(card(38, 330, 330, 160, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(52, 353, "飞轮越转越快“转爆表”了怎么办？（动量卸载）", size=12, weight="700", color=BLUE))
    el.append(txt(52, 374, "• 太阳光压等微弱外力矩会让飞轮朝单向越攒越快；", size=10.8, color=BODY))
    el.append(txt(52, 393, "• 近地轨道绝活：给“磁力矩器”线圈通电，借地磁场", size=10.8, color=BODY))
    el.append(txt(52, 411, "  产生力矩 τ = m × B⊕ 悄悄给飞轮减速（哈勃望远镜", size=10.8, color=BODY))
    el.append(txt(52, 429, "  全靠这招，绝不喷一滴尾气污染光学镜面！）；", size=10.8, color=BODY))
    el.append(txt(52, 449, "• 高轨或深空磁场太弱时，才点动 1 N 小推力器卸载；", size=10.8, color=BODY))
    el.append(txt(52, 469, "• 金色外衣（MLI 多层隔热膜）：防暴晒与深空严寒。", size=10.8, weight="700", color=INK))

    el.append(card(398, 68, 340, 438))
    el.append(txt(416, 95, "轨道维持：对抗三大“太空偷车贼”", size=15, weight="700", color=ORANGE))

    thieves = [
        (
            114, 118, ORANGE_SOFT, "#fdba74", ORANGE,
            "① 低轨头号小偷：高层大气阻力与太阳峰年",
            "400 km 仍有稀薄气体；每 11 年太阳活动高年，",
            "紫外暴晒使热层大气膨胀上涌！平时一年只需抬轨",
            "约 4 次，太阳峰年每 2–3 周就得点火抬升一次。",
        ),
        (
            246, 118, PURPLE_SOFT, "#d8b4fe", PURPLE,
            "② 高轨头号小偷：日月拉扯 + 赤道微椭圆重力谷",
            "日月引力每年把静止轨道掰歪约 0.85°（南北保持",
            "年耗 Δv ≈ 45–50 m/s）；赤道半径差约 70 m 的重力谷",
            "还会拽着卫星东西漂移，须死守 ±0.05° 窄小车位！",
        ),
        (
            378, 112, RED_SOFT, "#fca5a5", RED,
            "③ 致命暗器：太空碎片预警与紧急变轨闪避",
            "监控网追踪约 4.7 万个 >10 cm 目标；相对碰撞速度",
            "达 10–14 km/s（1 克铝球堪比手榴弹）！碰撞概率",
            "一旦越过警戒线，卫星提前半圈微推几厘米/秒闪避。",
        ),
    ]
    for ty, th, bg, bd, col, h1, *tlines in thieves:
        el.append(card(414, ty, 308, th, rx=10, fill=bg, stroke=bd))
        el.append(txt(426, ty + 22, h1, size=11.8, weight="700", color=col))
        for k, tl in enumerate(tlines):
            el.append(txt(426, ty + 43 + k * 19, tl, size=10.8, color=BODY))

    write_svg(
        TOPIC,
        "attitude-reaction-wheels-and-station-keeping.svg",
        figure(H, "卫星三轴反作用飞轮姿态控制与终身轨道维持机制图解", "左图展示星敏感器与三轴反作用飞轮及磁力矩器动量卸载，右图拆解低轨大气阻力、高轨日月摄动与碎片规避", el),
    )


# ---------------------------------------------------------------------------
# 6. End-of-Life Disposal: LEO 5-Year Re-entry / Point Nemo vs GEO +300km Graveyard
# ---------------------------------------------------------------------------
def build_eol_disposal() -> None:
    W, H = 760, 520
    el = []
    el.append(txt(W / 2, 30, "卫星老了怎么体面谢幕？低轨“五年火化”与高轨“三百公里养老院”", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "留最后一口救命燃料清场 + 排空电池余气“钝化”，绝不给人类留下一片凯斯勒碎片雷区", size=12.5, color=MUTED, anchor="middle"))

    el.append(card(22, 68, 356, 430))
    el.append(pill(38, 82, "低轨卫星（LEO < 2,000 km）：落叶归根火化", fg=ORANGE, bg=ORANGE_SOFT, w=286))

    cx, cy = 186, 234
    el.append(f'<circle cx="{cx}" cy="{cy}" r="76" fill="#e0f2fe" opacity="0.7"/>')
    el.append(f'<circle cx="{cx}" cy="{cy}" r="56" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    el.append(txt(cx, cy - 5, "南太平洋无人区", size=10.8, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(cx, cy + 12, "“尼莫点”公墓", size=10.8, weight="700", color=BLUE, anchor="middle"))

    el.append(f'<circle cx="{cx}" cy="{cy}" r="102" fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    el.append(f'<circle cx="{cx}" cy="{cy - 102}" r="5.5" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(cx, cy - 112, "末次反向点火降低近地点", size=10.8, weight="700", color=ORANGE, anchor="middle"))
    el.append(
        f'<path d="M {cx} {cy - 102} C {cx + 86} {cy - 100}, {cx + 92} {cy - 22}, {cx + 40} {cy + 26}" '
        f'fill="none" stroke="{RED}" stroke-width="3.2" marker-end="url(#arr-orange)"/>'
    )
    el.append(txt(cx + 86, cy - 42, "80–110 km", size=10.5, weight="700", color=RED))
    el.append(txt(cx + 86, cy - 27, "气动烧蚀解体", size=10.5, color=RED))

    el.append(card(38, 350, 324, 132, rx=10, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(50, 372, "国际离轨新规：从“25 年”大幅收紧至“5 年”！", size=11.8, weight="700", color=ORANGE))
    el.append(txt(50, 393, "• 欧空局（2023 零碎片政策）等要求新发低轨卫星退役后", size=10.6, color=BODY))
    el.append(txt(50, 411, "  5 年内受控或借稀薄大气阻力再入烧毁；", size=10.6, color=BODY))
    el.append(txt(50, 429, "• 烧不尽的巨型航天器（空间站、货运飞船）精准制导坠入", size=10.6, color=BODY))
    el.append(txt(50, 447, "  距最近陆地 2,688 km 的南太平洋“尼莫点”", size=10.6, color=BODY))
    el.append(txt(50, 465, "  （48°52.6′S, 123°23.6′W）深海安葬！", size=10.6, weight="700", color=INK))

    el.append(card(392, 68, 346, 430))
    el.append(pill(408, 82, "高轨卫星（GEO 35,786 km）：搬上 +300 km 坟墓轨", fg=PURPLE, bg=PURPLE_SOFT, w=314))

    cx2, cy2 = 556, 236
    el.append(f'<circle cx="{cx2}" cy="{cy2}" r="22" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    el.append(txt(cx2, cy2 + 4, "地球", size=10.5, weight="700", color=BLUE, anchor="middle"))
    el.append(f'<circle cx="{cx2}" cy="{cy2}" r="74" fill="none" stroke="{GREEN}" stroke-width="2.4"/>')
    el.append(f'<circle cx="{cx2}" cy="{cy2}" r="102" fill="none" stroke="{PURPLE}" stroke-width="2.6" stroke-dasharray="6 4"/>')
    el.append(_line(cx2 + 74, cy2, cx2 + 99, cy2, stroke=PURPLE, sw=2.6, marker="arr-blue"))
    el.append(txt(cx2, cy2 - 80, "现役黄金静止环（35,786 km）", size=10.6, weight="700", color=GREEN, anchor="middle"))
    el.append(txt(cx2, cy2 - 110, "外圈“坟墓轨道”（≥ 36,086 km，抬高 +300 km）", size=10.8, weight="700", color=PURPLE, anchor="middle"))
    el.append(txt(cx2 + 78, cy2 + 22, "Δv ≈ 11 m/s", size=10.8, weight="700", color=PURPLE))

    el.append(card(408, 350, 314, 132, rx=10, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(420, 372, "为什么高轨不往下烧，反而往上搬？", size=11.8, weight="700", color=PURPLE))
    el.append(txt(420, 393, "• 往下回地球需 Δv ≈ 1,480 m/s（够在轨用 30 年！），", size=10.6, color=BODY))
    el.append(txt(420, 411, "  而往上抬高 300 km 仅需 Δv ≈ 10.9 m/s（3 个月余油）；", size=10.6, color=BODY))
    el.append(txt(420, 429, "• 最后一步“钝化（Passivation）”：排空残余推进剂与", size=10.6, color=BODY))
    el.append(txt(420, 447, "  高压气瓶、断开蓄电池充电，防止多年后短路自爆", size=10.6, color=BODY))
    el.append(txt(420, 465, "  （史上超 560 起在轨解体多源于残余能源自爆！）。", size=10.6, weight="700", color=INK))

    write_svg(
        TOPIC,
        "satellite-end-of-life-reentry-vs-graveyard.svg",
        figure(H, "卫星退役离轨处置：低轨五年大气层再入火化与高轨300公里坟墓轨道", "对比低轨卫星受控再入尼莫点烧毁与高轨静止卫星消耗11 m/s抬升至36,086 km坟墓轨道并钝化", el),
    )


@register(
    TOPIC,
    "Satellite flight principles & full mission lifecycle: ascent/LEOP, Vis-Viva & Molniya, Hohmann vs electric spiral, rendezvous paradox, ADCS/station-keeping, EOL disposal",
    "physics",
)
def build_all() -> None:
    print(f"[{TOPIC}] building & verifying assertions...")
    _verify_satellite_flight_math()
    build_ascent_leop()
    build_vis_viva_molniya()
    build_hohmann_vs_electric()
    build_rendezvous_paradox()
    build_attitude_station_keeping()
    build_eol_disposal()
