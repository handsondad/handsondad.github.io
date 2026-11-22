"""
Visuals for '两小儿辩日的现代原理'
(The Modern Physics, Astronomy & Neuroscience of Two Children Debating the Sun:
1. Distance Verdict: Earth Rotation [-5,186 km at Qufu] vs Elliptical Orbit Radial Speed [±10,750 km in 6h] -> Spring vs Autumn Reversal! [1-shot CSS animation],
2. Optical Reality Check: Differential Atmospheric Refraction Lifts Sunrise Sun & Squashes Vertical Diameter by ~17% [32.0' -> 26.5'],
3. Why Sunrise Looks Huge ('大如车盖'): Flattened Sky Vault + Ponzo Depth Cues + V1 Primary Visual Cortex Expansion & 3 De-illusion Tests,
4. Why Noon Feels Like Boiling Soup ('如探汤', Part 1): Lambert's Cosine Projection [11.5 m² vs 1.23 m²] × Spherical Kasten-Young 38× Air Mass Extinction,
5. Why Sunrise Is Freezing & 14:30 Beats 12:00 Noon (Part 2): 24-Hour Surface Energy Budget [Q_in vs Q_out] & Thermal Inertia Bank Account).

Generates 5 original 760px Chinese SVG diagrams in assets/images/two-children-sun/
with verified orbital, atmospheric-optics, radiative, and visual-angle assertions.
"""
from __future__ import annotations

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
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

TOPIC = "two-children-sun"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#d97706"
AMBER_SOFT = "#fffbeb"
DARK_NAVY = "#0f172a"


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
    <marker id="arr-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{BLUE}"/>
    </marker>
    <marker id="arr-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{ORANGE}"/>
    </marker>
    <marker id="arr-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{GREEN}"/>
    </marker>
    <marker id="arr-slate" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{SLATE}"/>
    </marker>
    """


def kasten_young_am(elev_deg: float) -> float:
    """Kasten & Young (1989, Applied Optics 28:4735) relative optical air mass."""
    gamma = max(0.0, elev_deg)
    z = 90.0 - gamma
    return 1.0 / (math.sin(math.radians(gamma)) + 0.50572 * ((gamma + 6.07995) ** -1.6364))


# ---------------------------------------------------------------------------
# 1. Distance Verdict: Rotation vs Elliptical Orbit (with 1-shot CSS animation)
# ---------------------------------------------------------------------------
def build_distance_paradox_rotation_vs_orbit() -> str:
    # Exact astronomical assertions (IAU 2015 Resolution B3 + J2000 Earth orbit)
    au_km = 149_597_870.7
    r_earth_km = 6378.1
    e_orb = 0.0167086
    lat_qufu = 35.6  # Qufu, Shandong (Confucius's home region)
    # Equinox solar noon elevation at Qufu = 90 - 35.6 = 54.4 deg
    rot_gain_qufu = r_earth_km * math.cos(math.radians(lat_qufu))
    assert 5175.0 < rot_gain_qufu < 5195.0  # ~5,186 km closer due to rotation alone!

    v_orb_kms = 2 * math.pi * au_km / (365.25636 * 86400.0)
    assert 29.75 < v_orb_kms < 29.82
    vr_max_kms = e_orb * v_orb_kms / math.sqrt(1.0 - e_orb**2)  # radial speed at nu = +-90 deg
    assert 0.49 < vr_max_kms < 0.51  # ~0.498 km/s = ~1,791 km/h!
    orb_6h_km = vr_max_kms * 6.0 * 3600.0
    assert 10_700.0 < orb_6h_km < 10_800.0  # ~10,748 km in 6 hours — MORE than 2x Qufu rotation!

    net_spring_km = +orb_6h_km - rot_gain_qufu   # Noon is FARTHER by ~5,562 km in Spring!
    net_autumn_km = -orb_6h_km - rot_gain_qufu   # Noon is CLOSER by ~15,934 km in Autumn!
    assert net_spring_km > 5500.0 and net_autumn_km < -15800.0
    assert abs(net_autumn_km) / au_km < 1.1e-4   # < 0.011% of 1 AU!

    anim_defs = (
        _markers()
        + """
    <style>
      @keyframes rot6h {
        0%   { transform: rotate(-90deg); }
        100% { transform: rotate(0deg); }
      }
      .anim-obs {
        transform-origin: 146px 226px;
        animation: rot6h 3.2s cubic-bezier(0.22, 1, 0.36, 1) 1 forwards;
      }
      @media (prefers-reduced-motion: reduce) {
        .anim-obs {
          animation: none !important;
          transform: none !important;
        }
      }
    </style>
    """
    )

    els = []
    els.extend(
        header(
            "裁判第一锤：日出近还是正午近？连春天和秋天都会给出相反答案！",
            "单看地球自转正午拉近约 5186 km；但加上地球椭圆轨道 6 小时狂奔 ±10750 km，春秋季胜负直接反转",
        )
    )

    # Left Card: Earth 6-hour rotation geometry (schematic scale clearly noted)
    els.append(card(20, 62, 350, 340))
    els.append(step_badge(38, 84, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 88, "账本 A：地球自转 6 小时（正午拉近半个地球）", size=12.4, color=INK, weight="700"))

    # Schematic Earth seen from North Pole (exaggerated radius noted)
    ex, ey, er = 146, 226, 72
    # Night half (left) & Day half (right, facing Sun on the right)
    els.append(f'<circle cx="{ex}" cy="{ey}" r="{er}" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.8"/>')
    els.append(
        f'<path d="M {ex} {ey - er} A {er} {er} 0 0 0 {ex} {ey + er} Z" '
        f'fill="#1e293b" fill-opacity="0.78"/>'
    )
    els.append(_line(ex, ey - er - 10, ex, ey + er + 10, stroke=SLATE, sw=1.2, dash="4,3"))
    els.append(txt(ex - 36, ey + 5, "黑夜", size=10.5, color="#f8fafc", anchor="middle", weight="600"))
    els.append(txt(ex + 34, ey + 5, "白昼", size=10.5, color=BLUE, anchor="middle", weight="700"))

    # Sunlight parallel arrows from right
    for sy in [172, 226, 280]:
        els.append(_line(348, sy, 252, sy, stroke=AMBER, sw=1.8, marker="arr-orange"))
    els.append(txt(300, 154, "平行阳光（距日 1.5 亿 km）", size=10.0, color=AMBER, anchor="middle", weight="700"))

    # Static 6:00 sunrise dot at top (terminator) & static ghost target + animated dot rotating to 12:00 right
    els.append(f'<circle cx="{ex}" cy="{ey - er}" r="5" fill="#94a3b8" stroke="#fff" stroke-width="1.2"/>')
    els.append(txt(ex, 126, "① 清晨 06:00 日出（晨昏线）", size=10.2, color=INK, anchor="middle", weight="600"))

    # Dashed rotation arc from top (6:00) to right (12:00)
    ar = er + 14
    els.append(
        f'<path d="M {ex} {ey - ar} A {ar} {ar} 0 0 1 {ex + ar} {ey}" '
        f'fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#arr-red)"/>'
    )

    # Static dashed outline at 12:00 so initial frame still shows endpoint clearly
    els.append(f'<circle cx="{ex + er}" cy="{ey}" r="6.2" fill="none" stroke="{RED}" stroke-width="1.2" stroke-dasharray="2,2"/>')
    els.append(
        f'<g class="anim-obs">'
        f'<circle cx="{ex + er}" cy="{ey}" r="6.2" fill="{RED}" stroke="#fff" stroke-width="1.5"/>'
        f'</g>'
    )
    els.append(txt(ex + er + 10, ey + 18, "② 正午 12:00", size=10.5, color=RED, weight="700"))

    # Horizontal bracket showing R_lat ≈ 5186 km (at Qufu 35.6°N)
    by = 322
    els.append(_line(ex, ey, ex, by + 4, stroke=SLATE, sw=1.0, dash="3,3"))
    els.append(_line(ex + er, ey, ex + er, by + 4, stroke=RED, sw=1.0, dash="3,3"))
    els.append(_line(ex, by, ex + er, by, stroke=RED, sw=1.8, marker="arr-red"))
    els.append(txt(ex + er / 2, by + 16, "自转拉近 ≈ 5186 km", size=10.5, color=RED, anchor="middle", weight="700"))
    els.append(txt(36, 362, "• 以孔子故里曲阜（北纬 35.6°）春分为例：赤道半径 6378 km，", size=10.0, color=BODY))
    els.append(txt(36, 380, "  自转 6 小时把人朝太阳方向端近了 R·cos35.6° ≈ 5186 km。", size=10.0, color=BODY))
    els.append(txt(36, 395, "  （注：左图地球尺寸为看清几何刻意放大，非真实日地比例）", size=9.6, color=MUTED))

    # Right Card: Elliptical Orbit 6-Hour Radial Motion (The Big Seasonal Twist!)
    els.append(card(384, 62, 356, 340))
    els.append(step_badge(402, 84, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(420, 88, "账本 B：椭圆公转 6 小时（比地球半径大一倍！）", size=12.4, color=INK, weight="700"))

    els.append(card(400, 106, 324, 92, rx=8, fill=AMBER_SOFT, stroke="#fcd34d", sw=1.1))
    els.append(txt(412, 126, "1 月初近日点 1.471 亿 km（隆冬）↔ 7 月初远日点 1.521 亿 km", size=10.0, color=INK, weight="700"))
    els.append(txt(412, 145, "半年进出 500 万公里！春／秋分前后径向速度高达 ±1791 km/h：", size=10.0, color=BODY))
    els.append(txt(412, 164, "• 06:00 → 12:00 仅 6 小时，公转改变日地距离 ±10750 km！", size=10.2, color=ORANGE, weight="700"))
    els.append(txt(412, 183, "• 公转 6 小时位移竟是自转拉近量（5186 km）的 2.07 倍！", size=10.1, color=RED, weight="700"))

    # Case 1: Autumn morning (approaching Jan perihelion) — fully opaque in all frames
    els.append(card(400, 210, 324, 82, rx=8, fill=RED_SOFT, stroke="#fca5a5", sw=1.1))
    els.append(txt(412, 230, "秋季早晨（9 月底至 10 月初，加速扑向近日点）：", size=10.6, color=RED, weight="700"))
    els.append(txt(412, 249, "公转拉近 10750 km ＋ 自转拉近 5186 km", size=10.1, color=BODY))
    els.append(txt(412, 269, "⇒ 正午比日出【近约 15900 km】！（体感派小儿胜）", size=10.4, color=RED, weight="700"))

    # Case 2: Spring morning (receding toward Jul aphelion)
    els.append(card(400, 302, 324, 86, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE, sw=1.1))
    els.append(txt(412, 322, "春季早晨（3 月底至 4 月初，远离太阳奔向远日点）：", size=10.6, color=BLUE, weight="700"))
    els.append(txt(412, 341, "公转推远 10750 km － 自转拉近 5186 km", size=10.1, color=BODY))
    els.append(txt(412, 361, "⇒ 日出反而比正午【近约 5560 km】！（视觉派小儿翻盘）", size=10.4, color=BLUE, weight="700"))

    # Bottom Full-Width Verdict Banner
    els.append(card(20, 414, 720, 86, rx=10, fill=TEAL_SOFT, stroke="#5eead4", sw=1.2))
    els.append(pill(36, 424, "终极比例尺裁决：两小儿的推理前提双双落空！", fg=TEAL, bg="#ccfbf1", w=292, size=11.2))
    els.append(
        txt(
            36,
            466,
            "无论 5186 km 还是 15900 km，除以日地平均距离 1.496 亿 km，相对变化率都不到【万分之一（0.004%–0.011%）】！",
            size=10.6,
            color=INK,
            weight="700",
        )
    )
    els.append(
        txt(
            36,
            486,
            "这就好比你站在 10 米外烤篝火，身体只往前探了 0.4 毫米——既不可能让太阳看起来变大，也不可能把清凉变滚烫！",
            size=10.2,
            color=BODY,
        )
    )

    return figure(
        515,
        "两小儿辩日距离真相：地球自转与椭圆公转叠加下的春秋胜负反转图",
        "左卡演示地球6小时自转将北纬35.6度观测者向太阳拉近约5186公里；右卡揭示地球椭圆轨道在春秋两季6小时内产生正负10750公里的径向距离变化，使秋季正午更近而春季日出更近；底部指出两者均不足日地距离的万分之一。",
        els,
        extra_defs=anim_defs,
    )


# ---------------------------------------------------------------------------
# 1B. Full 365-Day Qufu Sunrise-vs-Noon Competition Curve & 500 BCE Precession
# ---------------------------------------------------------------------------
def build_annual_morning_vs_noon_crossover_curve() -> str:
    phi = math.radians(35.6)  # Qufu latitude
    r_qufu = 6370.93          # Geocentric radius at 35.6°N (WGS-84)
    au_km = 149_597_870.7
    e_orb = 0.0167086
    eps = math.radians(23.4393)
    p_sec = 365.25636 * 86400.0
    n_rad_s = 2.0 * math.pi / p_sec

    def calc_curve(varpi_deg: float):
        varpi = math.radians(varpi_deg)
        out = []
        for doy in range(1, 366):
            lam = 2.0 * math.pi * (doy - 79.5) / 365.2422
            delta = math.asin(math.sin(eps) * math.sin(lam))
            h0 = math.acos(-math.tan(phi) * math.tan(delta))
            dt_sec = (math.degrees(h0) / 15.0) * 3600.0
            rot_closer = r_qufu * math.cos(phi - delta)  # exact 3D sunrise(0) -> noon projection!
            nu = lam - varpi
            vr = (n_rad_s * au_km * e_orb * math.sin(nu)) / math.sqrt(1.0 - e_orb**2)
            orb_change = vr * dt_sec
            net_km = orb_change - rot_closer  # d(noon) - d(sunrise): >0 means sunrise is closer!
            out.append((doy, net_km))
        return out

    c_now = calc_curve(283.4)   # 2026 epoch (perihelion ~ Jan 3)
    c_500bc = calc_curve(240.0) # ~500 BCE Confucius era (perihelion ~ Nov 21, precessed ~43.4°)

    days_rise_now = sum(1 for _, v in c_now if v > 0.0)
    days_rise_bc = sum(1 for _, v in c_500bc if v > 0.0)
    assert 126 <= days_rise_now <= 132   # 129 days in 2026!
    assert 127 <= days_rise_bc <= 133    # 130 days in 500 BCE!

    doy_peak_rise, val_peak_rise = max(c_now, key=lambda x: x[1])
    doy_peak_noon, val_peak_noon = min(c_now, key=lambda x: x[1])
    assert 5500.0 < val_peak_rise < 5900.0     # +5,727 km around Apr 7 (DOY 97)
    assert -16000.0 < val_peak_noon < -15300.0 # -15,670 km around Sep 15 (DOY 258)

    # Zero crossings in 2026: DOY ~26.4 (Jan 26) and DOY ~155.0 (Jun 4)
    crossings = []
    for i in range(len(c_now) - 1):
        d1, v1 = c_now[i]
        d2, v2 = c_now[i + 1]
        if v1 * v2 <= 0.0:
            frac = d1 + (0.0 - v1) / (v2 - v1)
            crossings.append(frac)
    assert len(crossings) == 2 and 25.0 < crossings[0] < 28.0 and 153.5 < crossings[1] < 156.5

    els = []
    els.extend(
        header(
            "全年 365 天逐日精确裁决：一年有 129 天日出更近、两天绝对平局！",
            "耦合曲阜昼长伸缩、太阳赤纬与椭圆轨道速度，对比当代（实线）与公元前 500 年孔子时代（虚线）",
        )
    )

    # Left Card: 365-day plot
    els.append(card(20, 62, 466, 424))
    els.append(step_badge(38, 84, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 88, "曲阜（35.6°N）正午减日出日地距离差 Δd ＝ d(正午) － d(日出)", size=11.8, color=INK, weight="700"))

    gx0, gx1 = 78.0, 468.0
    gy_top, gy_bot = 118.0, 422.0
    v_min, v_max = -21000.0, 9200.0

    def dx(doy_f: float) -> float:
        return gx0 + ((doy_f - 1.0) / 364.0) * (gx1 - gx0)

    def dy(val_km: float) -> float:
        return gy_bot - ((val_km - v_min) / (v_max - v_min)) * (gy_bot - gy_top)

    y_zero = dy(0.0)

    # Background shaded bands above/below zero
    els.append(
        f'<rect x="{gx0:.1f}" y="{gy_top:.1f}" width="{gx1 - gx0:.1f}" height="{y_zero - gy_top:.1f}" '
        f'fill="#eff6ff" fill-opacity="0.7"/>'
    )
    els.append(
        f'<rect x="{gx0:.1f}" y="{y_zero:.1f}" width="{gx1 - gx0:.1f}" height="{gy_bot - y_zero:.1f}" '
        f'fill="#fff1f2" fill-opacity="0.55"/>'
    )

    for tick_km in [-15000, -10000, -5000, 0, 5000]:
        yy = dy(float(tick_km))
        st_col = INK if tick_km == 0 else "#e2e8f0"
        st_w = 1.5 if tick_km == 0 else 1.0
        els.append(_line(gx0, yy, gx1, yy, stroke=st_col, sw=st_w))
        lbl = "0" if tick_km == 0 else f"{tick_km // 1000:+d}k"
        els.append(txt(gx0 - 6, yy + 3.5, lbl, size=9.6, color=INK if tick_km == 0 else MUTED, anchor="end", cls="mono"))

    els.append(txt(gx0 + 6, gy_top + 13, "↑ Δd>0：日出更近（车盖派胜）", size=9.8, color=BLUE, weight="700"))
    els.append(txt(gx0 + 6, gy_bot - 8, "↓ Δd<0：正午更近（探汤派胜）", size=9.8, color=RED, weight="700"))

    # Fill positive lobe of 2026 curve (Jan 26 -> Jun 4)
    pos_pts = [f"{dx(crossings[0]):.1f},{y_zero:.1f}"]
    for d_i, v_i in c_now:
        if v_i > 0:
            pos_pts.append(f"{dx(float(d_i)):.1f},{dy(v_i):.1f}")
    pos_pts.append(f"{dx(crossings[1]):.1f},{y_zero:.1f}")
    els.append(f'<polygon points="{" ".join(pos_pts)}" fill="#93c5fd" fill-opacity="0.42"/>')

    # 500 BCE Confucius-era curve (purple dashed)
    poly_bc = " ".join(f"{dx(float(d_i)):.1f},{dy(v_i):.1f}" for d_i, v_i in c_500bc[::3])
    els.append(f'<polyline points="{poly_bc}" fill="none" stroke="{PURPLE}" stroke-width="1.8" stroke-dasharray="5,4"/>')

    # 2026 curve (two-tone or bold blue/red polyline)
    poly_now = " ".join(f"{dx(float(d_i)):.1f},{dy(v_i):.1f}" for d_i, v_i in c_now[::2])
    els.append(f'<polyline points="{poly_now}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')

    # Highlight key markers on 2026 curve: 2 zero crossings + spring peak + autumn trough
    for cx_doy in crossings:
        els.append(f'<circle cx="{dx(cx_doy):.1f}" cy="{y_zero:.1f}" r="5.0" fill="{GREEN}" stroke="#fff" stroke-width="1.4"/>')
    els.append(f'<circle cx="{dx(float(doy_peak_rise)):.1f}" cy="{dy(val_peak_rise):.1f}" r="5.0" fill="{BLUE}" stroke="#fff" stroke-width="1.4"/>')
    els.append(f'<circle cx="{dx(float(doy_peak_noon)):.1f}" cy="{dy(val_peak_noon):.1f}" r="5.0" fill="{RED}" stroke="#fff" stroke-width="1.4"/>')

    els.append(txt(dx(float(doy_peak_rise)) + 6, dy(val_peak_rise) - 7, f"4月7日峰值 +{val_peak_rise:.0f} km", size=9.6, color=BLUE, weight="700"))
    els.append(txt(dx(crossings[0]) + 5, y_zero + 15, "1月26日平局", size=9.4, color=GREEN, weight="700"))
    els.append(txt(dx(crossings[1]) + 6, y_zero - 7, "6月4日平局", size=9.4, color=GREEN, weight="700"))
    els.append(txt(dx(float(doy_peak_noon)) + 16, dy(val_peak_noon) + 17, f"9月15日谷底 {val_peak_noon:.0f} km", size=9.5, color=RED, anchor="middle", weight="700"))
    els.append(_line(304, gy_top + 15, 326, gy_top + 15, stroke=PURPLE, sw=2.0, dash="5,4"))
    els.append(txt(331, gy_top + 19, "前500年孔子时代", size=9.4, color=PURPLE, weight="700"))

    # Month ticks along x-axis
    month_doys = [(1, "1月"), (60, "3月"), (121, "5月"), (182, "7月"), (244, "9月"), (305, "11月"), (365, "12月底")]
    els.append(_line(gx0, gy_top, gx0, gy_bot, stroke=SLATE, sw=1.2))
    els.append(_line(gx0, gy_bot, gx1, gy_bot, stroke=SLATE, sw=1.2))
    for md, mlbl in month_doys:
        xx = dx(float(md))
        els.append(_line(xx, gy_bot, xx, gy_bot + 5, stroke=SLATE, sw=1.1))
        els.append(txt(xx, gy_bot + 17, mlbl, size=9.5, color=MUTED, anchor="middle"))
    els.append(txt((gx0 + gx1) / 2, gy_bot + 38, "公历日期（单位 km：正值代表日出更近，负值代表正午更近）", size=9.8, color=MUTED, anchor="middle"))

    # Right Card: 3 Key Insights
    els.append(card(498, 62, 242, 424))
    els.append(step_badge(516, 84, 2, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(534, 88, "看懂这条曲线的三把钥匙", size=11.8, color=INK, weight="700"))

    els.append(card(512, 106, 214, 118, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    els.append(txt(522, 125, f"① 当代每年 {days_rise_now} 天“早晨更近”", size=10.3, color=BLUE, weight="700"))
    els.append(txt(522, 144, "几何日出瞬间，观测者地心半径永远", size=9.8, color=BODY))
    els.append(txt(522, 161, "垂直于阳光（投影恒为 0）；正午拉", size=9.8, color=BODY))
    els.append(txt(522, 178, "近量随季节在冬至 3278 km 至夏至", size=9.8, color=BODY))
    els.append(txt(522, 195, "6228 km 间变化，1月底公转即反超！", size=9.8, color=INK, weight="600"))

    els.append(card(512, 234, 214, 110, rx=8, fill=GREEN_SOFT, stroke="#86efac"))
    els.append(txt(522, 253, "② 一年两次“绝对平局日”", size=10.3, color=GREEN, weight="700"))
    els.append(txt(522, 272, "每年 1 月 26 日与 6 月 4 日前后，", size=9.8, color=BODY))
    els.append(txt(522, 289, "半日椭圆轨道退行量恰好等于曲阜自", size=9.8, color=BODY))
    els.append(txt(522, 306, "转拉近量（Δd＝0），早晨和中午距", size=9.8, color=BODY))
    els.append(txt(522, 323, "太阳一公里不差——两小儿战成平手！", size=9.8, color=INK, weight="600"))

    els.append(card(512, 354, 214, 118, rx=8, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    els.append(txt(522, 373, "③ 回到 2500 年前孔子时代", size=10.3, color=PURPLE, weight="700"))
    els.append(txt(522, 392, "地球椭圆近日点约 2.1 万年进动一圈", size=9.8, color=BODY))
    els.append(txt(522, 409, "（每 58 年推迟 1 天）。前 500 年近", size=9.8, color=BODY))
    els.append(txt(522, 426, "日点在 11 月下旬，12月中旬至 4月20", size=9.8, color=BODY))
    els.append(txt(522, 443, f"日共 {days_rise_bc} 天日出更近，暮春照样翻盘！", size=9.8, color=INK, weight="600"))

    return figure(
        502,
        "曲阜全年365天日出与正午日地距离差逐日曲线及孔子时代岁差对比图",
        f"左卡精确计算北纬35.6度全年每日正午减日出距离差Δd：当代1月26日至6月4日共{days_rise_now}天日出更近（4月7日峰值+5727公里），其余236天正午更近（9月15日谷底-15670公里），两交点为平局日；紫色虚线展示公元前500年近日点进动后的{days_rise_bc}天反转窗口。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 2. Optical Reality Check: Differential Atmospheric Refraction Squashes Sun
# ---------------------------------------------------------------------------
def build_atmospheric_refraction_squashed_sun() -> str:
    # Astronomical refraction assertions (Bennett 1982 / Meeus standard refraction)
    d_true_arcmin = 32.0       # True solar angular diameter ~31'59"
    r_lower_arcmin = 34.5      # Refraction at apparent altitude 0'
    r_upper_arcmin = 29.0      # Refraction at apparent altitude +26.5'
    d_vert_apparent = d_true_arcmin - (r_lower_arcmin - r_upper_arcmin)
    squash_pct = (1.0 - d_vert_apparent / d_true_arcmin) * 100.0
    assert 26.0 <= d_vert_apparent <= 27.0
    assert 16.5 <= squash_pct <= 18.0  # Vertically squashed by ~17.2%!

    els = []
    els.extend(
        header(
            "拿同焦距相机给“车盖派”验伤：大气层不是放大镜，反而把朝阳拍扁了 17%！",
            "地平线大气折射把整轮太阳提前“拎”出地面，且下缘比上缘抬得更高，把正圆挤成扁鸭蛋",
        )
    )

    # Left Card: Curved Atmosphere Differential Refraction Ray Diagram
    els.append(card(20, 62, 400, 410))
    els.append(step_badge(38, 84, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 88, "大气差异折射：为什么下缘抬升 34.5′、上缘只抬 29.0′？", size=12.2, color=INK, weight="700"))

    # Concentric atmospheric shells + Earth horizon
    els.append('<path d="M 38 308 Q 210 278 398 326 L 398 354 L 38 354 Z" fill="#cbd5e1"/>')
    els.append('<path d="M 38 242 Q 210 212 398 260" fill="none" stroke="#93c5fd" stroke-width="1.2" stroke-dasharray="5,4"/>')
    els.append('<path d="M 38 182 Q 210 152 398 200" fill="none" stroke="#bfdbfe" stroke-width="1.2" stroke-dasharray="5,4"/>')
    els.append(txt(52, 162, "高层稀薄空气 n ≈ 1.00005", size=9.8, color=MUTED))
    els.append(txt(52, 220, "近地稠密空气 n ≈ 1.00029（光线向地面弯折）", size=9.8, color=BLUE, weight="600"))

    # Observer at left-center on ground
    ox, oy = 72, 294
    els.append(f'<circle cx="{ox}" cy="{oy}" r="5.5" fill="{INK}"/>')
    els.append(txt(ox, oy + 20, "观测者", size=10.2, color=INK, anchor="middle", weight="700"))

    # True Sun below geometric horizon line on the right!
    els.append(_line(ox, oy, 398, 294, stroke=SLATE, sw=1.3, dash="6,4"))
    els.append(txt(162, 315, "几何真地平线（天顶距 90°）", size=9.6, color=SLATE, anchor="middle"))

    # True Sun (dashed circle completely below horizon!)
    tsx, tsy, tsr = 370, 326, 18
    els.append(f'<circle cx="{tsx}" cy="{tsy}" r="{tsr}" fill="#fde68a" fill-opacity="0.48" stroke="{AMBER}" stroke-width="1.4" stroke-dasharray="4,3"/>')
    els.append(txt(244, 344, "真实太阳（整轮藏在地平线下！）", size=9.8, color=AMBER, anchor="middle", weight="700"))

    # Apparent Sun (lifted above horizon AND vertically flattened!)
    asx, asy = 370, 256
    els.append(f'<ellipse cx="{asx}" cy="{asy}" rx="18" ry="14.9" fill="#fb923c" fill-opacity="0.88" stroke="{RED}" stroke-width="1.6"/>')
    els.append(txt(342, 240, "视太阳虚像（被整轮拎出地面）", size=10.0, color=RED, anchor="end", weight="700"))

    # Curved real rays from true limbs to observer + straight apparent sightlines
    els.append(f'<path d="M {tsx} {tsy - tsr} Q 230 264 {ox} {oy}" fill="none" stroke="{ORANGE}" stroke-width="1.7"/>')
    els.append(f'<path d="M {tsx} {tsy + tsr} Q 230 284 {ox} {oy}" fill="none" stroke="{RED}" stroke-width="1.7"/>')
    els.append(_line(ox, oy, asx, asy - 14.9, stroke=ORANGE, sw=1.2, dash="3,3"))
    els.append(_line(ox, oy, asx, asy + 14.9, stroke=RED, sw=1.2, dash="3,3"))

    els.append(card(36, 364, 368, 96, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE, sw=1.0))
    els.append(txt(48, 383, "戳破伪科普：“清晨水汽像凸透镜放大了太阳”", size=10.5, color=INK, weight="700"))
    els.append(txt(48, 402, "• 大气下密上疏把阳光向下弯折，USNO 日出标准天顶距达 90°50′；", size=9.8, color=BODY))
    els.append(txt(48, 420, "• 下缘贴近稠密底层抬升 34.5′，上缘仅抬升 29.0′（差值 5.5′）；", size=9.8, color=BODY))
    els.append(txt(48, 438, "• 下巴往上挤了 5.5 角分，大气折射非但没放大，反而把太阳压扁了！", size=9.8, color=RED, weight="600"))

    # Right Card: Fixed-Focal-Length Solar-Filter Camera Pixel Comparison
    els.append(card(434, 62, 306, 410))
    els.append(step_badge(452, 84, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(470, 88, "铁证：同焦距减光相机实拍叠图", size=12.2, color=INK, weight="700"))

    # Camera viewfinder dark box
    els.append(card(452, 106, 270, 232, rx=10, fill=DARK_NAVY, stroke="#334155", sw=1.2))
    # Pixel measurement grid lines (same horizontal width x = 587 +- 54)
    cx = 587
    rx_px = 52.0
    ry_noon = 52.0
    ry_hor = ry_noon * (d_vert_apparent / d_true_arcmin)  # 43.1 px (exact 26.5/32 ratio!)

    els.append(_line(cx - rx_px, 134, cx - rx_px, 326, stroke="#475569", sw=1.1, dash="4,3"))
    els.append(_line(cx + rx_px, 134, cx + rx_px, 326, stroke="#475569", sw=1.1, dash="4,3"))
    els.append(txt(cx, 125, "← 水平宽度完全相等 (32.0′) →", size=9.6, color="#93c5fd", anchor="middle"))

    # Top disc: Noon Sun (32.0' x 32.0' exact circle)
    y_noon = 186
    els.append(f'<circle cx="{cx}" cy="{y_noon}" r="{rx_px:.1f}" fill="#fef08a" stroke="#facc15" stroke-width="1.8"/>')
    els.append(txt(cx, y_noon - 4, "正午日中", size=10.8, color=INK, anchor="middle", weight="700"))
    els.append(txt(cx, y_noon + 14, "32.0′ × 32.0′", size=9.8, color=BODY, anchor="middle", cls="mono"))

    # Bottom disc: Horizon Sunrise Sun (32.0' wide x 26.5' tall exact ellipse!)
    y_hor = 284
    els.append(f'<ellipse cx="{cx}" cy="{y_hor}" rx="{rx_px:.1f}" ry="{ry_hor:.1f}" fill="#f97316" stroke="#fb923c" stroke-width="1.8"/>')
    els.append(txt(cx, y_hor - 4, "清晨日出", size=10.8, color="#fff", anchor="middle", weight="700"))
    els.append(txt(cx, y_hor + 13, f"32.0′ × {d_vert_apparent:.1f}′", size=9.8, color="#ffedd5", anchor="middle", cls="mono"))
    els.append(txt(648, 287, f"压扁 {squash_pct:.0f}%", size=9.8, color="#fca5a5", weight="700"))

    els.append(card(452, 350, 270, 110, rx=8, fill=AMBER_SOFT, stroke="#fcd34d", sw=1.0))
    els.append(txt(464, 370, "像素尺量出来的真相：", size=10.6, color=INK, weight="700"))
    els.append(txt(464, 389, "1. 横向直径：早中晚恒为约 32 角分（0.53°），", size=9.8, color=BODY))
    els.append(txt(464, 407, "   连伸直手臂小拇指指甲盖的一半宽都不到；", size=9.8, color=BODY))
    els.append(txt(464, 425, "2. 纵向直径：日出时反而被压扁缩水约 1/6！", size=9.8, color=RED, weight="700"))
    els.append(txt(464, 443, "⇒ “大如车盖”100% 发生在眼球之后的大脑里！", size=9.8, color=INK, weight="700"))

    return figure(
        490,
        "地平线大气差异折射使日出太阳垂直压扁约17%的光路与相机实拍对比图",
        "左卡展示大气密度梯度导致太阳下缘抬升34.5角分、上缘抬升29.0角分；右卡按真实比例绘制同焦距减光相机下正午正圆（32.0×32.0角分）与日出扁椭圆（32.0×26.5角分）的像素宽度完全一致。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 3. Horizon Illusion: Flattened Sky Vault + Ponzo Cues + V1 Cortex Expansion
# ---------------------------------------------------------------------------
def build_horizon_illusion_ponzo_and_v1() -> str:
    # Retinal image size check: eye nodal distance f_eye ≈ 17 mm, theta = 0.533 deg
    f_eye_mm = 17.0
    theta_rad = math.radians(0.533)
    retinal_mm = f_eye_mm * theta_rad
    assert 0.15 < retinal_mm < 0.17  # ~0.158 mm tiny spot on retina both morning and noon!

    els = []
    els.extend(
        header(
            "第一个小孩为什么发誓“大如车盖”？扁平天穹错觉与大脑 V1 皮层的自动放大",
            "视网膜光斑永远只有 0.16 毫米；但地景深度线索骗过了大脑，让初级视觉皮层点亮了更大面积",
        )
    )

    # Left Card: Flattened Sky Vault + Emmert's Size-Distance Scaling
    els.append(card(20, 62, 392, 422))
    els.append(step_badge(38, 84, 1, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 88, "扁平天穹与埃默特定律：感知大小 ＝ 视角 θ × 感知距离", size=12.0, color=INK, weight="700"))

    # Ground line + Observer at (96, 302)
    ox, oy = 96, 302
    els.append(_line(36, oy, 394, oy, stroke="#64748b", sw=2.0))
    # Trees, houses, hills receding to right horizon (Ponzo terrestrial depth cues!)
    els.append('<polygon points="154,302 164,274 174,302" fill="#16a34a" opacity="0.75"/>')
    els.append('<rect x="206" y="282" width="18" height="20" fill="#94a3b8"/>')
    els.append('<polygon points="203,282 215,270 227,282" fill="#64748b"/>')
    els.append('<path d="M 252 302 L 278 276 L 304 302 L 328 284 L 352 302 Z" fill="#cbd5e1"/>')
    els.append(txt(248, 320, "树木 → 房屋 → 远山层云（丰富地面透视线索把地平线推得很远）", size=9.9, color=SLATE, anchor="middle"))

    # True equal-distance hemisphere arc (dashed slate) vs Perceived flattened dome (purple)
    # True hemisphere radius r = 136 around (96, 302): zenith at (96, 166), horizon at (232, 302)
    els.append(
        f'<path d="M {ox} {oy - 136} A 136 136 0 0 1 {ox + 136} {oy}" '
        f'fill="none" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4,4"/>'
    )
    els.append(txt(208, 206, "真实等距轨迹", size=9.6, color=SLATE))

    # Perceived flattened sky bowl: zenith low at (96, 204), horizon far at (368, 302)!
    els.append(
        f'<path d="M 52 208 Q 210 198 368 {oy}" '
        f'fill="none" stroke="{PURPLE}" stroke-width="2.4"/>'
    )
    els.append(txt(216, 122, "大脑感知的“扁平覆碗天穹”（四边远、头顶矮）", size=10.2, color=PURPLE, anchor="middle", weight="700"))

    # Observer eye
    els.append(f'<circle cx="{ox}" cy="{oy}" r="5.5" fill="{INK}"/>')

    # Zenith sightlines & small perceived "盘盂" disc at (96, 204)
    els.append(_line(ox, oy, ox - 8, 204, stroke=BLUE, sw=1.2, dash="3,3"))
    els.append(_line(ox, oy, ox + 8, 204, stroke=BLUE, sw=1.2, dash="3,3"))
    els.append(f'<circle cx="{ox}" cy="204" r="9" fill="#fef08a" stroke="{AMBER}" stroke-width="1.6"/>')
    els.append(txt(ox + 12, 146, "头顶无参照物 → 感知近", size=9.8, color=BLUE, weight="600"))
    els.append(txt(ox + 12, 163, "大脑判定：“小如盘盂”", size=9.9, color=INK, weight="700"))

    # Horizon sightlines (SAME cone angle!) & large perceived "车盖" disc at (368, 283)
    els.append(_line(ox, oy, 368, 266, stroke=ORANGE, sw=1.2, dash="3,3"))
    els.append(_line(ox, oy, 368, 300, stroke=ORANGE, sw=1.2, dash="3,3"))
    els.append('<circle cx="368" cy="283" r="20" fill="#fb923c" fill-opacity="0.88" stroke="#dc2626" stroke-width="1.8"/>')
    els.append(txt(394, 232, "感知远 2.5–3 倍 →“大如车盖”！", size=9.8, color=RED, anchor="end", weight="700"))

    els.append(card(36, 336, 360, 134, rx=8, fill=PURPLE_SOFT, stroke="#d8b4fe", sw=1.0))
    els.append(txt(48, 356, "为什么王充《论衡》猜反了亮度，考夫曼（1962）抓到了主因？", size=10.3, color=PURPLE, weight="700"))
    els.append(txt(48, 376, "• 东汉王充猜“暗处看火显得大”，但实测刺眼强光才会有辐照膨胀，", size=9.8, color=BODY))
    els.append(txt(48, 394, "  只是日出经 38 倍空气消光柔和可看清轮廓，正午眩光刺眼难直视；", size=9.8, color=BODY))
    els.append(txt(48, 412, "• Kaufman & Rock (1962, Science) 人工月亮证实：遮住地面远景后，", size=9.8, color=BODY))
    els.append(txt(48, 430, "  “车盖巨日／巨月”当场缩回原形！加上平视与仰头 90° 的辐辏差异，", size=9.8, color=BODY))
    els.append(txt(48, 448, "  大脑把完全相同的 0.16 mm 视网膜像强行放大成了两三倍巨轮。", size=9.8, color=INK, weight="600"))

    # Right Card: 2006 Nature Neuroscience V1 fMRI + 3 Instant De-illusion Experiments
    els.append(card(426, 62, 314, 422))
    els.append(step_badge(444, 84, 2, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(462, 88, "fMRI 脑扫描实锤 ＋ 三招一秒破除魔法", size=12.0, color=INK, weight="700"))

    # V1 cortex retinotopic activation comparison box
    els.append(card(442, 106, 282, 152, rx=8, fill="#f8fafc", stroke=BORDER, sw=1.1))
    els.append(txt(454, 126, "Murray 等 (2006, Nat. Neurosci.) fMRI 发现：", size=10.0, color=INK, weight="700"))
    els.append(txt(454, 144, "视网膜光斑完全相等（0.53°），但初级视觉皮层 V1 里：", size=9.8, color=BODY))

    # Two brain/V1 patch badges
    els.append(card(456, 158, 120, 86, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    els.append('<circle cx="516" cy="192" r="12" fill="#3b82f6" fill-opacity="0.8"/>')
    els.append(txt(516, 222, "头顶近处目标", size=10.0, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(516, 237, "V1 激活区较小", size=9.9, color=BODY, anchor="middle"))

    els.append(card(590, 158, 120, 86, rx=8, fill=ORANGE_SOFT, stroke="#fdba74"))
    els.append('<circle cx="650" cy="192" r="22" fill="#f97316" fill-opacity="0.82" stroke="#dc2626" stroke-width="1.3"/>')
    els.append(txt(650, 222, "地平线远处目标", size=10.0, color=RED, anchor="middle", weight="700"))
    els.append(txt(650, 237, "V1 激活区真的变大！", size=9.9, color=RED, anchor="middle", weight="700"))

    # Bottom right: 3 hands-on tests you can do tomorrow morning (with eye safety note!)
    els.append(card(442, 270, 282, 200, rx=8, fill=TEAL_SOFT, stroke="#5eead4", sw=1.1))
    els.append(txt(454, 291, "亲自验证！（仅限日出微光或满月，严禁直视烈日）", size=10.5, color=TEAL, weight="700"))
    els.append(txt(454, 314, "① 纸筒窥视法：把 A4 纸卷成细筒只看日轮，挡住", size=10.1, color=BODY))
    els.append(txt(454, 332, "   树梢与房屋，大车盖瞬间缩回小盘子！", size=10.1, color=INK, weight="600"))
    els.append(txt(454, 355, "② 弯腰胯下倒看法：背对日出弯腰从两腿间倒着看，", size=10.1, color=BODY))
    els.append(txt(454, 373, "   天地透视线索颠倒，巨日错觉当场消失大半！", size=10.1, color=INK, weight="600"))
    els.append(txt(454, 396, "③ 小拇指标尺法：伸直手臂竖起小拇指（宽约 1°），", size=10.1, color=BODY))
    els.append(txt(454, 414, "   无论早晚，太阳和月亮永远只占半个指甲盖宽！", size=10.1, color=INK, weight="600"))
    els.append(txt(454, 440, "⚠️ 安全红线：正午阳光聚焦视网膜 1 秒即可灼伤黄斑，", size=9.9, color=RED, weight="700"))
    els.append(txt(454, 457, "   测正午太阳大小请务必使用小孔成像投影或巴德膜！", size=9.9, color=RED))

    return figure(
        500,
        "日出大如车盖的视觉神经机制：扁平天穹庞佐错觉与初级视觉皮层V1激活扩张图",
        "左卡展示地面树木建筑远山构成的深度线索将地平线天穹推远2.5至3倍，按埃默特定律将同为0.53度的视角放大为车盖；右卡展示2006年Nature Neuroscience的V1皮层fMRI证据及纸筒窥视、弯腰倒看、小拇指测角三种破除错觉实验。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 4. Cosine Projection Spread × Spherical 38x Air Mass Extinction
# ---------------------------------------------------------------------------
def build_cosine_projection_and_air_mass() -> str:
    s0 = 1361.0  # W/m^2 (IAU 2015 Resolution B3)
    tau_zenith = 0.18  # clean-sky broadband optical depth

    am_0 = kasten_young_am(0.0)
    am_5 = kasten_young_am(5.0)
    am_noon = kasten_young_am(54.4)  # Qufu equinox noon
    am_90 = kasten_young_am(90.0)
    assert 37.5 < am_0 < 38.5       # ~37.9 AM at horizon!
    assert 10.2 < am_5 < 10.6       # ~10.4 AM at 5 deg elevation
    assert 1.22 < am_noon < 1.24    # ~1.23 AM at 54.4 deg
    assert abs(am_90 - 1.0) < 0.01

    area_5 = 1.0 / math.sin(math.radians(5.0))       # 11.47 m^2
    area_noon = 1.0 / math.sin(math.radians(54.4))   # 1.23 m^2
    assert 11.4 < area_5 < 11.6 and 1.22 < area_noon < 1.24

    # Direct horizontal irradiance I_horiz = S0 * exp(-tau * AM) * sin(alpha)  [Meinel / Beer-Lambert clean sky]
    # Using Meinel empirical clean-sky direct beam I_b = S0 * 0.7^(AM^0.678) for realistic broadband spectrum!
    def horiz_irrad(elev_deg: float) -> float:
        if elev_deg <= 0.0:
            return 0.0
        am = kasten_young_am(elev_deg)
        i_beam = s0 * (0.7 ** (am ** 0.678))
        return i_beam * math.sin(math.radians(elev_deg))

    eh_5 = horiz_irrad(5.0)
    eh_noon = horiz_irrad(54.4)
    eh_summer = horiz_irrad(77.8)  # Qufu summer solstice noon (90 - 35.6 + 23.4 = 77.8 deg)
    assert 20.0 < eh_5 < 30.0          # ~23 W/m^2 just after sunrise!
    assert 720.0 < eh_noon < 800.0     # ~757 W/m^2 at equinox noon!
    assert 910.0 < eh_summer < 970.0   # ~935 W/m^2 at summer solstice noon (~40x sunrise 5°!)

    els = []
    els.extend(
        header(
            "替“探汤派”破案（上）：为什么早晨沧沧凉凉、中午火辣烫手？",
            "不是太阳跑近了，而是“斜射余弦摊薄 10 倍”叠加上“球壳大气层 38 倍闯关削弱”！",
        )
    )

    # Left Card: Lambert's Cosine Projection Law
    els.append(card(20, 62, 360, 426))
    els.append(step_badge(38, 84, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 88, "第一刀：兰伯特余弦定律（1 m² 光束摊多宽？）", size=12.2, color=INK, weight="700"))

    # Top sub-diagram: Noon steep beam (54.4 deg -> 1.23 m^2)
    els.append(card(36, 106, 328, 126, rx=8, fill="#fffbeb", stroke="#fcd34d"))
    els.append(txt(48, 126, "☀️ 正午高悬（曲阜春分 α＝54.4°，夏至 α＝77.8°）", size=10.6, color=ORANGE, weight="700"))
    # Steep beam polygon hitting ground bar
    els.append('<polygon points="154,136 194,136 164,204 116,204" fill="#fde047" fill-opacity="0.65" stroke="#eab308" stroke-width="1.3"/>')
    els.append(_line(54, 204, 344, 204, stroke=INK, sw=2.2))
    els.append(_line(116, 212, 164, 212, stroke=RED, sw=2.4))
    els.append(txt(252, 164, "光束集中砸在 1.23 m²", size=10.5, color=RED, anchor="middle", weight="700"))
    els.append(txt(252, 183, "（夏至仅 1.02 m²，火力全开！）", size=10.0, color=BODY, anchor="middle"))
    els.append(txt(140, 225, "1.23 m²", size=10.0, color=RED, anchor="middle", weight="700", cls="mono"))

    # Bottom sub-diagram: Morning grazing beam (5 deg -> 11.5 m^2!) — non-crossing cyclic polygon!
    els.append(card(36, 242, 328, 130, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    els.append(txt(48, 262, "🌅 日出低斜（刚出山 α＝5°）", size=10.5, color=BLUE, weight="700"))
    els.append('<polygon points="348,274 348,292 268,342 64,342" fill="#93c5fd" fill-opacity="0.48" stroke="#3b82f6" stroke-width="1.2"/>')
    els.append(_line(48, 342, 352, 342, stroke=INK, sw=2.2))
    els.append(_line(64, 349, 268, 349, stroke=BLUE, sw=2.4))
    els.append(txt(200, 365, f"同一束光摊薄在 {area_5:.1f} m² 大地上（密度仅剩 8.7%）", size=9.7, color=BLUE, anchor="middle", weight="700"))

    els.append(card(36, 382, 328, 92, rx=8, fill="#f8fafc", stroke=BORDER))
    els.append(txt(48, 402, "手电筒直照 vs 斜擦桌面实验：", size=10.5, color=INK, weight="700"))
    els.append(txt(48, 421, "大气层顶太阳常数恒为 S₀＝1361 W/m²（IAU 2015 标准）。", size=9.8, color=BODY))
    els.append(txt(48, 439, "单靠几何投影 E ＝ I·sin α，5° 低阳比春分正午就已被摊薄了", size=9.8, color=BODY))
    els.append(txt(48, 457, f"sin 54.4° ÷ sin 5° ≈ {area_5 / area_noon:.1f} 倍！这还只是第一刀。", size=10.0, color=RED, weight="700"))

    # Right Card: Kasten-Young Air Mass & Ground Horizontal Irradiance Curve
    els.append(card(394, 62, 346, 426))
    els.append(step_badge(412, 84, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(430, 88, "第二刀：穿过 38 倍厚大气层（Kasten–Young 曲线）", size=12.0, color=INK, weight="700"))

    gx0, gx1 = 444.0, 718.0
    gy_top, gy_bot = 122.0, 312.0

    def px(elev: float) -> float:
        return gx0 + (elev / 80.0) * (gx1 - gx0)

    def py_irr(w_m2: float) -> float:
        return gy_bot - (w_m2 / 1000.0) * (gy_bot - gy_top)

    for w_tick in [0, 250, 500, 750, 1000]:
        yy = py_irr(float(w_tick))
        els.append(_line(gx0, yy, gx1, yy, stroke="#e2e8f0", sw=1.0))
        els.append(txt(gx0 - 6, yy + 4, f"{w_tick}", size=9.8, color=MUTED, anchor="end", cls="mono"))

    for el_tick in [0, 15, 30, 54.4, 77.8]:
        xx = px(el_tick)
        els.append(_line(xx, gy_bot, xx, gy_bot + 5, stroke=SLATE, sw=1.1))
        lbl = f"{el_tick:.0f}°" if el_tick in (0, 15, 30) else f"{el_tick:.1f}°"
        els.append(txt(xx, gy_bot + 18, lbl, size=9.8, color=MUTED, anchor="middle", cls="mono"))

    els.append(txt((gx0 + gx1) / 2, gy_bot + 36, "太阳高度角 α（0° 日出地平线 → 77.8° 曲阜夏至正午）", size=10.0, color=MUTED, anchor="middle"))
    els.append(_line(gx0, gy_top, gx0, gy_bot, stroke=SLATE, sw=1.3))
    els.append(_line(gx0, gy_bot, gx1, gy_bot, stroke=SLATE, sw=1.3))

    # Plot clean-sky horizontal direct irradiance curve (W/m^2)
    pts = [(el, horiz_irrad(float(el))) for el in range(0, 81, 2)]
    poly = " ".join(f"{px(el):.1f},{py_irr(v):.1f}" for el, v in pts)
    area_poly = f"{px(0):.1f},{gy_bot:.1f} " + poly + f" {px(80):.1f},{gy_bot:.1f}"
    els.append(f'<polygon points="{area_poly}" fill="#fed7aa" fill-opacity="0.48"/>')
    els.append(f'<polyline points="{poly}" fill="none" stroke="{RED}" stroke-width="2.6"/>')

    # Key annotated points: 5° (~23 W/m²), 54.4° (~757 W/m²), 77.8° (~935 W/m²)
    for el_p, v_p, col_p in [(5.0, eh_5, BLUE), (54.4, eh_noon, ORANGE), (77.8, eh_summer, RED)]:
        els.append(f'<circle cx="{px(el_p):.1f}" cy="{py_irr(v_p):.1f}" r="4.8" fill="{col_p}" stroke="#fff" stroke-width="1.3"/>')

    els.append(txt(px(14.0), py_irr(eh_5) - 4, f"α=5°: 仅 {eh_5:.0f} W/m² (10.4 AM)", size=9.6, color=BLUE, weight="700"))
    els.append(txt(px(54.4) - 8, py_irr(eh_noon) - 9, f"春分正午 {eh_noon:.0f} W/m² (1.23 AM)", size=9.6, color=ORANGE, anchor="end", weight="700"))
    els.append(txt(px(77.8) - 8, py_irr(eh_summer) - 7, f"夏至正午 {eh_summer:.0f} W/m²", size=9.6, color=RED, anchor="end", weight="700"))
    els.append(txt(gx0 + 6, gy_top + 14, "晴空地面直射火力 (W/m²)", size=10.0, color=RED, weight="700"))

    els.append(card(410, 360, 314, 114, rx=8, fill=RED_SOFT, stroke="#fca5a5", sw=1.0))
    els.append(txt(422, 380, f"日出切线光学质量高达 {am_0:.0f} 倍大气厚度（38 AM）！", size=10.7, color=RED, weight="700"))
    els.append(txt(422, 399, "• 蓝紫短波被空气分子瑞利散射一空，只剩红橙光染红朝阳；", size=10.0, color=BODY))
    els.append(txt(422, 417, "• 水汽与尘埃再截留大半红外热能，叠加余弦摊薄后，5° 低阳", size=10.0, color=BODY))
    els.append(txt(422, 435, f"  地面火力（{eh_5:.0f} W/m²）不到夏至正午（{eh_summer:.0f} W/m²）的 1/40！", size=10.1, color=INK, weight="700"))
    els.append(txt(422, 453, "  这就是早晨直视朝阳不刺眼、晒在身上也不烫的物理根源。", size=10.0, color=BODY))

    return figure(
        505,
        "兰伯特余弦投影摊薄与Kasten-Young球壳大气38倍光学质量消光对比图",
        "左卡对比正午54.4度（光束集中于1.23平方米）与日出5度（摊薄于11.5平方米）的余弦面积效应；右卡绘出地面水平直射辐照度随太阳高度角暴涨曲线，从日出5度的23瓦每平方米跃升至正午757至935瓦每平方米。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 5. Diurnal Heat Budget & Thermal Inertia Lag (Why Sunrise Is Coldest & 14:30 Hottest)
# ---------------------------------------------------------------------------
def build_diurnal_heat_budget_lag() -> str:
    # Simulate physically coupled 24h surface energy balance:
    # C * dT/dt = Q_in(t) - Q_out(T(t)), solved to periodic steady state!
    dt_h = 0.1
    n_steps = int(24.0 / dt_h)
    temps = [15.0] * (n_steps + 1)
    q_in_arr = [0.0] * (n_steps + 1)
    q_out_arr = [0.0] * (n_steps + 1)

    def solar_abs(hour: float) -> float:
        if hour <= 6.0 or hour >= 18.0:
            return 0.0
        # Peaks sharply at 12:00 solar noon (~680 W/m^2 absorbed shortwave)
        return 680.0 * (math.sin(math.pi * (hour - 6.0) / 12.0) ** 1.35)

    # Iterate 8 diurnal cycles so T(0) == T(24) periodic equilibrium!
    t_cur = 15.0
    c_eff = 76.0  # W*h / (m^2 * K) effective continental boundary-layer heat capacity
    for _ in range(8):
        for i in range(n_steps + 1):
            hr = i * dt_h
            qi = solar_abs(hr)
            qo = 160.0 + 22.0 * (t_cur - 11.0)  # linearized longwave + sensible/latent cooling
            q_in_arr[i] = qi
            q_out_arr[i] = qo
            if i < n_steps:
                t_cur += ((qi - qo) / c_eff) * dt_h
                temps[i + 1] = t_cur
        temps[0] = t_cur

    i_min = min(range(n_steps + 1), key=lambda i: temps[i])
    i_max = max(range(n_steps + 1), key=lambda i: temps[i])
    hr_min, t_min = round(i_min * dt_h, 2), temps[i_min]
    hr_max, t_max = round(i_max * dt_h, 2), temps[i_max]
    # Verify sunrise (~6.5–6.8h, ~30–48 min after 06:00 sunrise) is coldest AND afternoon (~14.3–14.6h) is hottest!
    assert 6.1 <= hr_min <= 6.9, f"Expected min shortly after sunrise, got {hr_min}"
    assert 14.0 <= hr_max <= 15.0, f"Expected max near 14:30, got {hr_max}"
    assert t_max - t_min > 10.0

    def fmt_hm(h_val: float) -> str:
        hh = int(h_val)
        mm = int(round((h_val - hh) * 60))
        if mm == 60:
            hh += 1
            mm = 0
        return f"{hh:02d}:{mm:02d}"

    hm_min_str = fmt_hm(hr_min)
    hm_max_str = fmt_hm(hr_max)

    els = []
    els.extend(
        header(
            "替“探汤派”破案（下）：为什么日出比半夜还冷，最热却不在 12 点而在下午两点半？",
            "大地像一只巨型储热银行账户：只要“阳光进账 ＞ 红外散热支出”，过了正午气温还会继续涨！",
        )
    )

    # Main 24-hour dual-panel or unified chart card (Left: 24h Curves, Right: Bank Account Logic)
    els.append(card(20, 62, 456, 412))
    els.append(step_badge(38, 84, 1, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(56, 88, "昼夜 24 小时地表能量收支与气温滞后曲线（物理耦合解）", size=12.0, color=INK, weight="700"))

    gx0, gx1 = 68.0, 452.0
    # Top sub-axis: Flux Q_in & Q_out (122..258), Bottom sub-axis: Air Temp T (292..418)
    fy_top, fy_bot = 122.0, 256.0
    ty_top, ty_bot = 294.0, 416.0

    def hx(hr: float) -> float:
        return gx0 + (hr / 24.0) * (gx1 - gx0)

    def fy(q: float) -> float:
        return fy_bot - (q / 720.0) * (fy_bot - fy_top)

    def ty(temp_c: float) -> float:
        return ty_bot - ((temp_c - (t_min - 5.2)) / ((t_max + 3.2) - (t_min - 5.2))) * (ty_bot - ty_top)

    # Vertical guide lines at 06:00, 12:00, hr_max (~14.4h), 18:00
    for h_guide, col_g in [(hr_min, BLUE), (12.0, AMBER), (hr_max, RED)]:
        els.append(_line(hx(h_guide), fy_top, hx(h_guide), ty_bot, stroke=col_g, sw=1.1, dash="4,3"))

    # Top Flux Panel
    els.append(_line(gx0, fy_top, gx0, fy_bot, stroke=SLATE, sw=1.2))
    els.append(_line(gx0, fy_bot, gx1, fy_bot, stroke=SLATE, sw=1.2))
    els.append(txt(gx0 - 6, fy_top + 6, "700", size=9.8, color=MUTED, anchor="end", cls="mono"))
    els.append(txt(gx0 - 6, fy_bot + 4, "0", size=9.8, color=MUTED, anchor="end", cls="mono"))
    els.append(txt(gx0 + 6, fy_top + 12, "辐射功率 (W/m²)", size=10.0, color=INK, weight="700"))

    # Shade Net Gain region (Q_in > Q_out between hr_min and hr_max)
    gain_pts = (
        [f"{hx(i * dt_h):.1f},{fy(q_in_arr[i]):.1f}" for i in range(i_min, i_max + 1, 2)]
        + [f"{hx(i * dt_h):.1f},{fy(q_out_arr[i]):.1f}" for i in range(i_max, i_min - 1, -2)]
    )
    els.append(f'<polygon points="{" ".join(gain_pts)}" fill="#bbf7d0" fill-opacity="0.58"/>')
    els.append(txt(hx(10.3), fy(430), "净储热区", size=10.0, color=GREEN, anchor="middle", weight="700"))

    qin_poly = " ".join(f"{hx(i * dt_h):.1f},{fy(q_in_arr[i]):.1f}" for i in range(0, n_steps + 1, 2))
    qout_poly = " ".join(f"{hx(i * dt_h):.1f},{fy(q_out_arr[i]):.1f}" for i in range(0, n_steps + 1, 2))
    els.append(f'<polyline points="{qin_poly}" fill="none" stroke="{GREEN}" stroke-width="2.3"/>')
    els.append(f'<polyline points="{qout_poly}" fill="none" stroke="{SLATE}" stroke-width="2.0" stroke-dasharray="5,3"/>')

    els.append(txt(hx(12.0), fy(680) - 7, "12:00 阳光进账峰值 Q_in", size=10.0, color=GREEN, anchor="middle", weight="700"))
    els.append(txt(hx(20.6), fy(q_out_arr[206]) - 9, "地表红外散热支出 Q_out", size=9.9, color=SLATE, anchor="middle", weight="600"))

    # Bottom Temperature Panel
    els.append(_line(gx0, ty_top, gx0, ty_bot, stroke=SLATE, sw=1.2))
    els.append(_line(gx0, ty_bot, gx1, ty_bot, stroke=SLATE, sw=1.2))
    els.append(txt(gx0 + 6, ty_top + 12, "近地面气温 T (°C)", size=10.0, color=ORANGE, weight="700"))

    t_poly = " ".join(f"{hx(i * dt_h):.1f},{ty(temps[i]):.1f}" for i in range(0, n_steps + 1, 2))
    els.append(f'<polyline points="{t_poly}" fill="none" stroke="{ORANGE}" stroke-width="2.8"/>')

    # Min & Max temperature dots + Noon dot
    els.append(f'<circle cx="{hx(hr_min):.1f}" cy="{ty(t_min):.1f}" r="5" fill="{BLUE}" stroke="#fff" stroke-width="1.3"/>')
    els.append(f'<circle cx="{hx(12.0):.1f}" cy="{ty(temps[120]):.1f}" r="4.5" fill="{AMBER}" stroke="#fff" stroke-width="1.2"/>')
    els.append(f'<circle cx="{hx(hr_max):.1f}" cy="{ty(t_max):.1f}" r="5.5" fill="{RED}" stroke="#fff" stroke-width="1.4"/>')

    els.append(txt(hx(hr_min) + 7, ty(t_min) + 12, f"{hm_min_str} 谷底“沧沧凉凉”({t_min:.0f}°C)", size=9.6, color=BLUE, weight="700"))
    els.append(txt(hx(hr_max) + 7, ty(t_max) - 7, f"{hm_max_str} 气温峰值 ({t_max:.0f}°C)", size=9.8, color=RED, weight="700"))
    els.append(txt(hx(12.0) - 6, ty(temps[120]) - 8, "12:00 直射体感烫", size=9.4, color=AMBER, anchor="end", weight="700"))

    for h_tick in [0, 6, 12, 15, 18, 24]:
        xx = hx(float(h_tick))
        els.append(_line(xx, ty_bot, xx, ty_bot + 5, stroke=SLATE, sw=1.1))
        els.append(txt(xx, ty_bot + 18, f"{h_tick:02d}:00", size=9.8, color=MUTED, anchor="middle", cls="mono"))
    els.append(txt((gx0 + gx1) / 2, ty_bot + 38, "地方太阳时（06:00 日出 · 12:00 日中 · 18:00 日落）", size=10.0, color=MUTED, anchor="middle"))

    # Right Card: Three Intuitive Takeaways ("Bank Account" + Seasonal Analogy)
    els.append(card(490, 62, 250, 412))
    els.append(step_badge(508, 84, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(526, 88, "秒懂“热惯性存款账本”", size=12.0, color=INK, weight="700"))

    els.append(card(504, 108, 222, 110, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    els.append(txt(516, 128, "① 为什么日出是一天最冷时刻？", size=10.5, color=BLUE, weight="700"))
    els.append(txt(516, 148, "整晚 12 小时太阳零进账，大地却一刻", size=10.0, color=BODY))
    els.append(txt(516, 166, "不停向太空发射红外线散热。日出刚", size=10.0, color=BODY))
    els.append(txt(516, 184, "露头时进账仍小于支出，昨晚热老本", size=10.0, color=BODY))
    els.append(txt(516, 202, "彻底赔光，跌入全天最冷谷底！", size=10.0, color=INK, weight="600"))

    els.append(card(504, 228, 222, 122, rx=8, fill=RED_SOFT, stroke="#fca5a5"))
    els.append(txt(516, 248, "② 正午晒皮烫 vs 午后空气热", size=10.3, color=RED, weight="700"))
    els.append(txt(516, 267, "12 点阳光直射皮肤火力最强（体感如", size=9.8, color=BODY))
    els.append(txt(516, 285, f"探汤）；而背阴气温因 12 点至 {hm_max_str}", size=9.8, color=BODY))
    els.append(txt(516, 303, "进账仍大于支出，继续涨到午后才见", size=9.8, color=BODY))
    els.append(txt(516, 321, "顶！两者叠加，早晨自然最凉。", size=9.8, color=INK, weight="600"))

    els.append(card(504, 360, 222, 100, rx=8, fill=AMBER_SOFT, stroke="#fcd34d"))
    els.append(txt(516, 380, "③ 年度放大版：“夏至不热三伏热”", size=10.4, color=AMBER, weight="700"))
    els.append(txt(516, 400, "北半球 6 月 21 日夏至阳光最强（且", size=10.0, color=BODY))
    els.append(txt(516, 418, "7 月初反而在远日点！），但土壤海", size=10.0, color=BODY))
    els.append(txt(516, 436, "洋持续净储热，最热推迟到 7 月底！", size=10.0, color=INK, weight="600"))

    return figure(
        490,
        "昼夜24小时地表辐射收支账本与日出最冷、午后两点半最热的热惯性滞后图",
        f"左卡用耦合热平衡方程绘出阳光吸收功率Q_in（12点达峰）、地表红外与对流散热Q_out及近地面气温曲线，标出{hm_min_str}日出后收支交点对应全天最低温、{hm_max_str}收支交点对应全天最高温；右卡用银行存取款类比解释热滞后与三伏天原理。",
        els,
        extra_defs=_markers(),
    )


@register(TOPIC, "两小儿辩日的现代原理（6张760px原创SVG图解）", "mechanics_sky")
def build_all() -> None:
    builders = [
        ("distance-paradox-rotation-vs-orbit.svg", build_distance_paradox_rotation_vs_orbit),
        ("annual-morning-vs-noon-crossover-curve.svg", build_annual_morning_vs_noon_crossover_curve),
        ("atmospheric-refraction-squashed-sun.svg", build_atmospheric_refraction_squashed_sun),
        ("horizon-illusion-ponzo-and-v1-cortex.svg", build_horizon_illusion_ponzo_and_v1),
        ("cosine-projection-and-38x-air-mass.svg", build_cosine_projection_and_air_mass),
        ("diurnal-heat-budget-thermal-lag.svg", build_diurnal_heat_budget_lag),
    ]
    for fname, fn in builders:
        svg = fn()
        write_svg(TOPIC, fname, svg)
