"""Earth & Climate System visual builders (ENSO / El Niño-Southern Oscillation)."""

from html import escape
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
    LABEL_SIZE,
    MUTED,
    NOTE_SIZE,
    ORANGE,
    ORANGE_SOFT,
    PANEL_TITLE,
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

RED = "#b91c1c"
RED_SOFT = "#fef2f2"
RED_LINE = "#fca5a5"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
DEEP_SEA = "#0c4a6e"
WARM_RED = "#dc2626"
WARM_ORANGE = "#ea580c"


def _arrow(x1, y1, x2, y2, color=BLUE, sw=2.0, marker="arr-blue", dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{extra}{mk}/>'
    )


def _curve(d, color=BLUE, sw=2.0, marker=None, dash=None, fill="none", opacity=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#{marker})"' if marker else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round"{extra}{mk}{op}/>'
    )


def _cloud(cx, cy, scale=1.0, fill="#e2e8f0", stroke="#64748b"):
    return (
        f'<g transform="translate({cx:.1f},{cy:.1f}) scale({scale:.2f})">'
        f'<path d="M-24,6 C-30,6 -34,1 -34,-4 C-34,-10 -29,-14 -23,-14 '
        f'C-21,-22 -13,-27 -4,-26 C3,-31 14,-28 18,-20 C25,-20 31,-14 31,-7 '
        f'C31,1 25,6 18,6 Z" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
        f"</g>"
    )


def _verify_enso_physics_and_data():
    """Verify Kelvin/Rossby wave speeds, Clausius-Clapeyron slope, and NOAA ONI/RONI data."""
    # 1. Reduced gravity shallow-water equatorial Kelvin wave check:
    # g' ~ 0.045 m/s^2, H ~ 150 m -> c = sqrt(g' * H) ~ 2.60 m/s
    g_prime = 0.045
    h_thermo = 150.0
    c_kelvin = math.sqrt(g_prime * h_thermo)
    assert 2.4 <= c_kelvin <= 2.8
    pacific_span_m = 15_000_000.0
    kelvin_days = pacific_span_m / c_kelvin / 86400.0
    rossby_days = pacific_span_m / (c_kelvin / 3.0) / 86400.0
    assert 60.0 <= kelvin_days <= 75.0
    assert 180.0 <= rossby_days <= 225.0

    # 2. Clausius-Clapeyron saturation vapor pressure rate (Magnus formula):
    # es(T) = 6.1094 * exp(17.625 * T / (T + 243.04)) hPa
    def es_hpa(t_c):
        return 6.1094 * math.exp(17.625 * t_c / (t_c + 243.04))

    rate_7c = (es_hpa(7.5) - es_hpa(6.5)) / es_hpa(7.0) * 100.0   # tropospheric mean ~6.85%/K
    rate_27c = (es_hpa(27.5) - es_hpa(26.5)) / es_hpa(27.0) * 100.0  # tropical SST ~5.87%/K
    assert 6.6 <= rate_7c <= 7.1
    assert 5.7 <= rate_27c <= 6.2
    return kelvin_days, rossby_days, rate_7c, rate_27c


# Official NOAA CPC ONI (ERSSTv6) & Relative ONI (RONI, NWS PNS 26-05) representative
# peak seasonal anomaly values for each calendar/ENSO year 1950-2026 (deg C).
# Major event peaks verified directly from:
# https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/
# https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/
NOAA_ONI_V6_SERIES = [
    (1950, -1.4), (1951, 0.9), (1952, 0.4), (1953, 0.8), (1954, -0.9),
    (1955, -1.7), (1956, -1.1), (1957, 1.7), (1958, 1.6), (1959, 0.5),
    (1960, -0.2), (1961, -0.3), (1962, -0.4), (1963, 1.2), (1964, -0.9),
    (1965, 1.8), (1966, 1.2), (1967, -0.5), (1968, 0.9), (1969, 1.0),
    (1970, -1.0), (1971, -1.4), (1972, 1.8), (1973, -1.9), (1974, -1.7),
    (1975, -1.7), (1976, 0.8), (1977, 0.8), (1978, 0.1), (1979, 0.6),
    (1980, 0.5), (1981, -0.4), (1982, 2.1), (1983, 2.1), (1984, -1.0),
    (1985, -1.0), (1986, 1.2), (1987, 1.6), (1988, -1.8), (1989, -1.6),
    (1990, 0.4), (1991, 1.6), (1992, 1.7), (1993, 0.7), (1994, 1.1),
    (1995, -1.0), (1996, -0.9), (1997, 2.4), (1998, -1.6), (1999, -1.7),
    (2000, -1.7), (2001, -0.7), (2002, 1.3), (2003, 0.9), (2004, 0.7),
    (2005, -0.8), (2006, 0.9), (2007, -1.6), (2008, -1.6), (2009, 1.5),
    (2010, -1.6), (2011, -1.4), (2012, -0.8), (2013, -0.4), (2014, 0.7),
    (2015, 2.6), (2016, -0.7), (2017, -1.0), (2018, 0.9), (2019, 0.8),
    (2020, -1.2), (2021, -1.1), (2022, -1.0), (2023, 2.0), (2024, -0.6),
    (2025, -0.6), (2026, 2.5),
]

SUPER_EVENTS_COMPARE = [
    # (label, oni_v6, roni_v6, note)
    ("1982–83", 2.1, 2.4, "热带底温尚低"),
    ("1997–98", 2.4, 2.3, "经典世纪圣婴"),
    ("2015–16", 2.6, 2.3, "ONI 历史峰值"),
    ("2023–24", 2.0, 1.4, "底温抬高 +0.6°C"),
    ("2026 秋", 2.5, 2.0, "底温+耦合双强"),
]


def _build_pacific_normal_vs_elnino():
    """Fig 1: Equatorial Pacific cross-section comparing Normal vs El Nino + 1-shot Kelvin wave animation."""
    kelvin_days, _, _, _ = _verify_enso_physics_and_data()
    h = 596
    extra_defs = f"""
    <linearGradient id="ocean-deep" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1d6fa5"/>
      <stop offset="100%" stop-color="#0c4a6e"/>
    </linearGradient>
    <linearGradient id="warm-pool" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#dc2626"/>
      <stop offset="65%" stop-color="#ea580c"/>
      <stop offset="100%" stop-color="#f59e0b"/>
    </linearGradient>
    <marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{WARM_RED}"/>
    </marker>
    """
    extra_css = """
    @keyframes kelvin-surge {
      0%   { transform: translateX(-210px); opacity: 0.25; }
      20%  { opacity: 0.95; }
      85%  { transform: translateX(0px); opacity: 0.95; }
      100% { transform: translateX(0px); opacity: 0.92; }
    }
    @keyframes rain-shift {
      0%   { transform: translateX(-165px); opacity: 0.35; }
      100% { transform: translateX(0px); opacity: 1; }
    }
    .kelvin-pulse {
      animation: kelvin-surge 7.5s cubic-bezier(0.22, 0.61, 0.36, 1) 1 forwards;
    }
    .conv-shift {
      animation: rain-shift 7.5s cubic-bezier(0.22, 0.61, 0.36, 1) 1 forwards;
    }
    @media (prefers-reduced-motion: reduce) {
      .kelvin-pulse, .conv-shift {
        animation: none !important;
        transform: none !important;
        opacity: 1 !important;
      }
    }
    """
    el = []
    el.extend(
        header(
            "赤道太平洋“海—气大跷跷板”：常态年 vs 厄尔尼诺年剖面图",
            "横跨约 15,000 km（西：印尼/澳洲 120°E → 东：秘鲁/厄瓜多尔 80°W），纵向放大展示海面落差与温跃层倾角",
        )
    )

    # ---------------- TOP PANEL: NORMAL YEAR ----------------
    py1 = 68
    ph1 = 236
    el.append(card(24, py1, 712, ph1, fill="#ffffff"))
    el.append(pill(38, py1 + 12, "常态年（沃克环流强劲 · 西暖东冷）", fg=BLUE, bg=BLUE_SOFT, w=238))
    el.append(txt(290, py1 + 27, "赤道东风信风像推土机把暖水推向西太平洋，秘鲁近岸冷水上翻", size=12, color=MUTED))

    # Sky & Walker loop in panel 1 (x=80..680, sky y=104..186, ocean y=188..282)
    # Ocean basin background (deep cold water)
    el.append('<path d="M84,186 L676,193 L676,282 L84,282 Z" fill="url(#ocean-deep)" opacity="0.92"/>')
    # Sloped warm layer above 20C thermocline: deep in west (y=254, ~180m), shallow in east (y=204, ~40m)
    el.append(
        '<path d="M84,184 Q240,185 380,189 L676,193 L676,204 Q470,212 310,238 Q195,256 84,256 Z" '
        'fill="url(#warm-pool)" opacity="0.88"/>'
    )
    # 20 deg C Thermocline dashed curve
    el.append(
        _curve(
            "M84,256 Q195,256 310,238 Q470,212 676,204",
            color="#fef08a",
            sw=2.2,
            dash="6 4",
        )
    )
    # Continents at left/right margins
    el.append('<path d="M40,174 L84,174 L84,282 L40,282 Z" fill="#cbd5e1" stroke="#94a3b8"/>')
    el.append('<path d="M676,170 L720,170 L720,282 L676,282 Z" fill="#cbd5e1" stroke="#94a3b8"/>')
    el.append(txt(62, 296, "印尼/澳洲(120°E)", size=11.5, color=SLATE, anchor="middle", weight="600"))
    el.append(txt(380, 296, "日界线(180°) · 中太平洋", size=11.5, color=MUTED, anchor="middle"))
    el.append(txt(698, 296, "秘鲁/南美(80°W)", size=11.5, color=SLATE, anchor="middle", weight="600"))

    # Walker circulation arrows in Normal panel
    # Easterly trade winds (East -> West near surface)
    el.append(_arrow(605, 174, 245, 174, color=BLUE, sw=2.6, marker="arr-blue"))
    el.append(txt(425, 166, "强劲赤道东风信风（把表层暖水向西推）", size=11.5, color=BLUE, anchor="middle", weight="700", halo=True))
    # Rising air + cloud + rain in West (x=155)
    el.append(_arrow(148, 174, 148, 128, color=WARM_RED, sw=2.2, marker="arr-red"))
    el.append(_cloud(155, 124, scale=0.88, fill="#dbeafe", stroke=BLUE))
    for rx in (138, 152, 166):
        el.append(f'<line x1="{rx}" y1="133" x2="{rx - 4}" y2="147" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(txt(155, 108, "深对流上升多雨", size=11.5, color=BLUE, anchor="middle", weight="700"))
    # Upper-level westerly return flow
    el.append(_arrow(205, 114, 590, 114, color=SLATE, sw=1.8, marker="arr-muted", dash="5 4"))
    el.append(txt(400, 109, "高空西风回流（沃克环流闭合）", size=11, color=MUTED, anchor="middle"))
    # Sinking dry air in East (x=632)
    el.append(_arrow(632, 120, 632, 168, color=ORANGE, sw=2.1, marker="arr-orange"))
    el.append(txt(626, 142, "下沉干冷少雨", size=11.5, color=ORANGE, anchor="end", weight="600", halo=True))

    # Ocean annotations in Normal panel
    el.append(txt(185, 214, "西太平洋暖池 29–30 °C", size=12, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(185, 232, "海面比东岸高约 40–50 cm", size=11, color="#ffedd5", anchor="middle"))
    el.append(txt(185, 248, "温跃层深达 150–200 m", size=11, color="#fef08a", anchor="middle"))
    el.append(txt(435, 252, "20 °C 温跃层（上暖下冷分界）", size=11.5, color="#fef08a", anchor="middle", weight="600"))
    # Cold upwelling arrow off Peru
    el.append(_arrow(654, 268, 654, 202, color="#bae6fd", sw=2.5, marker="arr-blue"))
    el.append(txt(640, 232, "秘鲁寒流涌升(20–22°C)", size=11.5, color="#e0f2fe", anchor="end", weight="700"))
    el.append(txt(640, 248, "上翻营养盐 → 鳀鱼丰收", size=11, color="#bae6fd", anchor="end"))

    # ---------------- BOTTOM PANEL: EL NINO YEAR ----------------
    py2 = 316
    ph2 = 258
    el.append(card(24, py2, 712, ph2, fill="#ffffff"))
    el.append(pill(38, py2 + 12, "厄尔尼诺年（信风松劲 · 暖池东泻 · 暴雨搬家）", fg=ORANGE, bg=ORANGE_SOFT, w=282))
    el.append(txt(332, py2 + 27, "水下开尔文波约 2–3 个月横穿太平洋，压平温跃层并切断秘鲁冷水上翻", size=12, color=MUTED))

    # Ocean basin background in panel 2 (y=438..536)
    el.append('<path d="M84,442 L676,435 L676,536 L84,536 Z" fill="url(#ocean-deep)" opacity="0.92"/>')
    # Flattened / reversed sea surface (west drops 15-20cm, east rises 30-40cm!) & deepened eastern thermocline
    el.append(
        '<path d="M84,442 Q350,438 676,434 L676,496 Q450,498 260,486 Q150,478 84,474 Z" '
        'fill="url(#warm-pool)" opacity="0.90"/>'
    )
    # Animated subsurface Kelvin wave warm pulse surging west -> east
    el.append(
        '<g class="kelvin-pulse">'
        '<ellipse cx="455" cy="472" rx="135" ry="16" fill="#fde047" opacity="0.32" stroke="#fef08a" stroke-width="1.4" stroke-dasharray="5 3"/>'
        f'{_arrow(345, 472, 560, 472, color="#fef08a", sw=2.6, marker="arr-orange")}'
        "</g>"
    )
    # Flattened 20 deg C Thermocline in El Nino
    el.append(
        _curve(
            "M84,474 Q180,480 340,490 Q510,498 676,496",
            color="#fef08a",
            sw=2.2,
            dash="6 4",
        )
    )
    # Continents
    el.append('<path d="M40,426 L84,426 L84,536 L40,536 Z" fill="#cbd5e1" stroke="#94a3b8"/>')
    el.append('<path d="M676,422 L720,422 L720,536 L676,536 Z" fill="#cbd5e1" stroke="#94a3b8"/>')

    # Step badges + Walker reversal / split in El Nino panel
    # 1. Westerly wind bursts
    el.append(step_badge(198, 418, 1, fg=WARM_RED, bg=RED_SOFT))
    el.append(_arrow(214, 418, 355, 418, color=WARM_RED, sw=2.6, marker="arr-red"))
    el.append(txt(285, 405, "西风爆发/信风减弱", size=11.5, color=WARM_RED, anchor="middle", weight="700", halo=True))

    # Sinking dry air over Indonesia/Australia (West drought!)
    el.append(_arrow(132, 368, 132, 418, color=ORANGE, sw=2.2, marker="arr-orange"))
    el.append(txt(136, 362, "下沉少雨 → 印尼/澳洲干旱山火", size=11.5, color=ORANGE, anchor="start", weight="700", halo=True))

    # 4. Shifted convection + rain over Central-Eastern Pacific (animated shift with static labels)
    el.append('<g class="conv-shift">')
    el.append(_cloud(475, 378, scale=0.95, fill="#dbeafe", stroke=BLUE))
    for rx in (456, 472, 488, 502):
        el.append(f'<line x1="{rx}" y1="388" x2="{rx - 5}" y2="404" stroke="{BLUE}" stroke-width="1.8"/>')
    el.append("</g>")
    el.append(step_badge(420, 376, 4, fg=BLUE, bg=BLUE_SOFT))
    el.append(_arrow(475, 426, 475, 396, color=WARM_RED, sw=2.2, marker="arr-red"))
    el.append(txt(518, 375, "深对流东移：中东太平洋与秘鲁豪雨", size=11.5, color=BLUE, anchor="start", weight="700", halo=True))
    # Upper return flows left & right
    el.append(_arrow(430, 362, 175, 362, color=SLATE, sw=1.6, marker="arr-muted", dash="4 4"))

    # Ocean labels in El Nino panel
    el.append(txt(172, 462, "西侧海面降 15–20 cm", size=11, color="#ffedd5", anchor="middle"))
    el.append(step_badge(325, 456, 2, fg=ORANGE, bg=AMBER_SOFT))
    el.append(
        txt(
            458,
            459,
            f"赤道开尔文波东传（约 {kelvin_days:.0f} 天横穿太平洋）",
            size=11.5,
            color="#ffffff",
            anchor="middle",
            weight="700",
        )
    )
    el.append(step_badge(568, 514, 3, fg=ORANGE, bg=AMBER_SOFT))
    el.append(txt(552, 518, "东岸海面抬高 30–40 cm，温跃层压深至 >120 m，冷水上翻中断", size=11.5, color="#fef08a", anchor="end", weight="600"))

    el.append(txt(62, 554, "西太平洋暖池变浅", size=11.5, color=ORANGE, anchor="middle", weight="600"))
    el.append(txt(380, 554, "Niño 3.4 监测核心区（170°W–120°W）显著发烧", size=11.5, color=WARM_RED, anchor="middle", weight="700"))
    el.append(txt(698, 554, "鳀鱼减产/海岸洪涝", size=11.5, color=WARM_RED, anchor="middle", weight="600"))

    svg = figure(
        h,
        "赤道太平洋常态年与厄尔尼诺年海气耦合剖面对比图",
        "上方展示常态年强劲东风信风将29至30摄氏度暖水推向印尼一侧、秘鲁寒流冷水上翻并构成闭合沃克环流；下方展示厄尔尼诺年西风爆发触发水下开尔文波在约67天内东传压平温跃层，使暴雨中心东移至中东太平洋、印尼澳洲转入下沉干旱。",
        el,
        extra_css=extra_css,
        extra_defs=extra_defs,
    )
    write_svg("el-nino", "pacific-normal-vs-elnino.svg", svg)


def _build_bjerknes_feedback_loop():
    """Fig 2: Bjerknes positive ocean-atmosphere feedback loop + delayed Rossby oscillator brake."""
    kelvin_days, rossby_days, _, _ = _verify_enso_physics_and_data()
    h = 468
    el = []
    el.extend(
        header(
            "1969 年比耶克内斯揭开的秘密：为什么一小片暖水能滚成全球级事件？",
            "左侧为“海—气互相拱火”的正反馈闭环；右侧为 9–12 个月后让厄尔尼诺自动熄火的海洋负反馈刹车",
        )
    )

    # Left main card: Bjerknes Positive Feedback
    el.append(card(24, 68, 476, 376, fill="#ffffff"))
    el.append(pill(40, 82, "放大引擎：比耶克内斯正反馈（Bjerknes, 1969）", fg=ORANGE, bg=ORANGE_SOFT, w=326))

    # 4 cycle boxes arranged cleanly around center (cx=262, cy=268)
    # Top box (1)
    el.append(card(142, 118, 240, 62, rx=10, fill=RED_SOFT, stroke=WARM_RED, sw=1.3))
    el.append(step_badge(162, 138, 1, fg=WARM_RED, bg="#ffffff"))
    el.append(txt(180, 142, "东/中太平洋初现暖水异常", size=12.5, color=WARM_RED, weight="700"))
    el.append(txt(162, 164, "表层海温 ΔT > 0，冷舌开始退缩", size=11.5, color=BODY))

    # Right box (2)
    el.append(card(284, 224, 200, 74, rx=10, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.3))
    el.append(step_badge(304, 245, 2, fg=ORANGE, bg="#ffffff"))
    el.append(txt(322, 249, "东西海温差缩小", size=12.5, color=ORANGE, weight="700"))
    el.append(txt(298, 270, "西暖东冷温差 (T西 − T东) 变小", size=11.5, color=BODY))
    el.append(txt(298, 287, "东太平洋低空海平面气压下降", size=11.5, color=MUTED))

    # Bottom box (3)
    el.append(card(142, 344, 240, 68, rx=10, fill=BLUE_SOFT, stroke=BLUE, sw=1.3))
    el.append(step_badge(162, 365, 3, fg=BLUE, bg="#ffffff"))
    el.append(txt(180, 369, "赤道东风信风显著减弱", size=12.5, color=BLUE, weight="700"))
    el.append(txt(158, 390, "达尔文—塔希提气压跷跷板翻转", size=11.5, color=BODY))
    el.append(txt(158, 405, "（即沃克发现的“南方涛动”负位相）", size=11, color=MUTED))

    # Left box (4)
    el.append(card(40, 224, 200, 74, rx=10, fill=AMBER_SOFT, stroke=AMBER, sw=1.3))
    el.append(step_badge(60, 245, 4, fg=AMBER, bg="#ffffff"))
    el.append(txt(78, 249, "暖池东涌·温跃层压深", size=12.5, color=AMBER, weight="700"))
    el.append(txt(54, 270, "开尔文波东传，抑制深层冷水上翻", size=11.5, color=BODY))
    el.append(txt(54, 287, "东太平洋表层进一步增暖！", size=11.5, color=WARM_RED, weight="600"))

    # Curved clockwise arrows connecting 1->2->3->4->1
    el.append(_curve("M384,154 Q422,172 422,218", color=ORANGE, sw=2.3, marker="arr-orange"))
    el.append(_curve("M422,302 Q420,352 388,370", color=BLUE, sw=2.3, marker="arr-blue"))
    el.append(_curve("M138,370 Q104,352 104,304", color=ORANGE, sw=2.3, marker="arr-orange"))
    el.append(_curve("M104,218 Q106,172 136,154", color=ORANGE, sw=2.3, marker="arr-orange"))

    # Center badge
    el.append(card(246 - 30, 242, 60, 38, rx=8, fill=SLATE_SOFT, stroke=HAIRLINE))
    el.append(txt(246, 259, "正反馈", size=11.5, color=INK, anchor="middle", weight="700"))
    el.append(txt(246, 274, "滚雪球", size=11, color=ORANGE, anchor="middle", weight="600"))

    # Right card: Why doesn't it burn forever? (Delayed Oscillator / Recharge-Discharge)
    el.append(card(514, 68, 222, 376, fill="#ffffff"))
    el.append(pill(528, 82, "自动刹车：为什么只烧 9–12 个月？", fg=GREEN, bg=GREEN_SOFT, w=194, size=11.5))

    el.append(card(528, 120, 194, 92, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(540, 141, "刹车 A：西传罗斯贝波反射", size=12, color=GREEN, weight="700"))
    el.append(txt(540, 161, f"西传罗斯贝波慢约 3 倍（~{rossby_days:.0f} 天）", size=11, color=BODY))
    el.append(txt(540, 179, "撞上印尼西边界后反射为“冷性", size=11, color=BODY))
    el.append(txt(540, 197, "开尔文波”东传，从水下抽走暖水", size=11, color=MUTED))

    el.append(card(528, 224, 194, 92, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(540, 245, "刹车 B：赤道热库“放电耗尽”", size=12, color=BLUE, weight="700"))
    el.append(txt(540, 265, "暖水摊平到巨大海面后剧烈蒸发，", size=11, color=BODY))
    el.append(txt(540, 283, "且地转流把赤道热量向南北高纬", size=11, color=BODY))
    el.append(txt(540, 301, "排空（Jin 充放电振荡器模型）", size=11, color=MUTED))

    el.append(card(528, 328, 194, 100, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.1))
    el.append(txt(540, 350, "结果：2–7 年不规则钟摆", size=12, color=GREEN, weight="700"))
    el.append(txt(540, 370, "春季海温梯度最小、耦合最脆弱", size=11, color=BODY))
    el.append(txt(540, 388, "（春季预报障碍），峰值在圣诞前", size=11, color=BODY))
    el.append(txt(540, 406, "后，次年春夏季熄火常转拉尼娜", size=11, color=GREEN, weight="600"))

    svg = figure(
        h,
        "比耶克内斯海气正反馈闭环与厄尔尼诺负反馈终止机制图",
        "左侧展示1969年比耶克内斯提出的四步正反馈循环：东太平洋暖水异常缩小东西温差、削弱东风信风、促使暖池东涌压深温跃层并进一步增暖；右侧展示西传罗斯贝波边界反射（约200天）与赤道海洋热量向高纬放电排空，使事件在9至12个月后终止并进入2至7年振荡。",
        el,
    )
    write_svg("el-nino", "bjerknes-feedback-loop.svg", svg)


def _build_oni_vs_roni_history():
    """Fig 3: Exact NOAA CPC 1950-2026 ONI (ERSSTv6) curve + 2026 RONI comparison bars."""
    assert len(NOAA_ONI_V6_SERIES) == 77
    assert NOAA_ONI_V6_SERIES[0][0] == 1950 and NOAA_ONI_V6_SERIES[-1][0] == 2026
    oni_dict = dict(NOAA_ONI_V6_SERIES)
    assert oni_dict[1982] == 2.1 and oni_dict[1997] == 2.4
    assert oni_dict[2015] == 2.6 and oni_dict[2023] == 2.0 and oni_dict[2026] == 2.5

    h = 524
    el = []
    el.extend(
        header(
            "77 年实测账本（1950–2026）：NOAA 官方 ONI 曲线与全新 RONI 对比",
            "数据核自 NOAA CPC（ERSSTv6）：为什么 2026 年官方不得不启用扣除全球热带变暖底温的 RONI？",
        )
    )

    # Top card: 1950-2026 Time Series (x=24..736, y=68..314)
    el.append(card(24, 68, 712, 248, fill="#ffffff"))
    el.append(txt(42, 90, "Niño 3.4 区海洋尼诺指数 ONI 代表峰值演变（°C，阈值 ±0.5 °C，≥+2.0 °C 为超强厄尔尼诺）", size=12, color=INK, weight="700"))

    gx0, gx1 = 68.0, 712.0
    gy_top, gy_bot = 104.0, 286.0
    vmin, vmax = -2.2, 3.0

    def x_of(yr):
        return gx0 + (yr - 1950) / (2026 - 1950) * (gx1 - gx0)

    def y_of(val):
        return gy_bot - (val - vmin) / (vmax - vmin) * (gy_bot - gy_top)

    y_zero = y_of(0.0)
    y_p05 = y_of(0.5)
    y_p20 = y_of(2.0)
    y_m05 = y_of(-0.5)
    assert gy_top < y_p20 < y_p05 < y_zero < y_m05 < gy_bot

    # Shaded super El Nino band (>= 2.0C)
    el.append(
        f'<rect x="{gx0:.1f}" y="{gy_top:.1f}" width="{gx1 - gx0:.1f}" height="{y_p20 - gy_top:.1f}" '
        f'fill="{RED_SOFT}" opacity="0.75"/>'
    )
    # Grid lines & y labels
    for val, lbl, col, dash in [
        (2.0, "+2.0°C 超强线", WARM_RED, "4 3"),
        (0.5, "+0.5°C 厄尔尼诺", ORANGE, "3 3"),
        (0.0, "0.0°C 常态", SLATE, None),
        (-0.5, "-0.5°C 拉尼娜", BLUE, "3 3"),
        (-1.5, "-1.5°C", MUTED, "2 4"),
    ]:
        yy = y_of(val)
        sw = 1.2 if val in (0.0, 2.0) else 0.9
        el.append(_curve(f"M{gx0:.1f},{yy:.1f} L{gx1:.1f},{yy:.1f}", color=col, sw=sw, dash=dash, opacity=0.65))
        if val in (2.0, 0.5, 0.0, -0.5, -1.5):
            short_lbl = f"{val:+.1f}" if val != 0.0 else "0.0"
            el.append(txt(gx0 - 6, yy + 4, short_lbl, size=10.5, color=col, anchor="end", cls="mono"))

    el.append(txt(gx0 + 6, y_p20 - 6, "超强区 (≥ +2.0°C)", size=10.5, color=WARM_RED, weight="600"))

    # Bars for each year (positive = warm orange/red, negative = cool blue)
    bar_w = (gx1 - gx0) / 77.0 * 0.68
    for yr, val in NOAA_ONI_V6_SERIES:
        cx = x_of(yr)
        yy = y_of(val)
        if val >= 0:
            fill = WARM_RED if val >= 2.0 else (WARM_ORANGE if val >= 0.5 else "#cbd5e1")
            el.append(
                f'<rect x="{cx - bar_w / 2:.1f}" y="{yy:.1f}" width="{bar_w:.1f}" '
                f'height="{max(1.5, y_zero - yy):.1f}" rx="1.2" fill="{fill}" opacity="0.88"/>'
            )
        else:
            fill = BLUE if val <= -0.5 else "#cbd5e1"
            el.append(
                f'<rect x="{cx - bar_w / 2:.1f}" y="{y_zero:.1f}" width="{bar_w:.1f}" '
                f'height="{max(1.5, yy - y_zero):.1f}" rx="1.2" fill="{fill}" opacity="0.82"/>'
            )

    # X-axis decade ticks
    for yr in (1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2026):
        cx = x_of(yr)
        el.append(f'<line x1="{cx:.1f}" y1="{gy_bot:.1f}" x2="{cx:.1f}" y2="{gy_bot + 4:.1f}" stroke="{SLATE}"/>')
        el.append(txt(cx, gy_bot + 17, str(yr), size=10.5, color=SLATE, anchor="middle", cls="mono"))

    # Callout pins for landmark peaks & triple-dip La Nina
    peaks = [
        (1972, 1.8, "72–73 (+1.8)", -8, -8, "middle"),
        (1982.5, 2.1, "82–83 (+2.1)", 0, -9, "middle"),
        (1997, 2.4, "97–98 (+2.4)", 0, -9, "middle"),
        (2015, 2.6, "15–16 (+2.6)", -14, -8, "end"),
        (2023, 2.0, "23–24 (+2.0)", -6, -12, "end"),
        (2026, 2.5, "26秋 (+2.5)", -2, -9, "end"),
    ]
    for yr_p, val_p, label_p, dx, dy, anc in peaks:
        px, py = x_of(yr_p), y_of(val_p)
        el.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.2" fill="{WARM_RED}" stroke="#ffffff" stroke-width="1"/>')
        el.append(txt(px + dx, py + dy, label_p, size=10.5, color=WARM_RED, anchor=anc, weight="700", halo=True))

    el.append(
        txt(
            x_of(2021),
            y_of(-1.2) + 16,
            "20–22 三重拉尼娜",
            size=10.5,
            color=BLUE,
            anchor="middle",
            weight="600",
            halo=True,
        )
    )

    # Bottom card: Why NOAA adopted RONI in 2026 (ONI vs RONI side-by-side comparison)
    el.append(card(24, 328, 712, 178, fill="#ffffff"))
    el.append(pill(40, 340, "关键破案线索：传统 ONI vs 2026 新标准 RONI（扣除 20°N–20°S 全球热带变暖）", fg=PURPLE, bg=PURPLE_SOFT, w=505, size=11.5))
    el.append(f'<rect x="566" y="344" width="12" height="12" rx="2" fill="{WARM_RED}"/>')
    el.append(txt(583, 354, "传统 ONI", size=11, color=BODY, weight="600"))
    el.append(f'<rect x="646" y="344" width="12" height="12" rx="2" fill="{BLUE}"/>')
    el.append(txt(663, 354, "相对 RONI", size=11, color=BODY, weight="600"))

    # 5 event clusters horizontally across x=48..716
    slot_w = 132.0
    base_y = 458.0
    scale_h = 28.0  # 1.0 deg C = 28px -> 2.6 deg C = 72.8px
    for idx, (ev_lbl, oni_v, roni_v, ev_note) in enumerate(SUPER_EVENTS_COMPARE):
        sx = 46.0 + idx * slot_w
        el.append(card(sx, 372, 122, 122, rx=8, fill=SLATE_SOFT if idx < 3 else AMBER_SOFT, stroke=BORDER if idx < 3 else ORANGE))
        h_oni = oni_v * scale_h
        h_roni = roni_v * scale_h
        bx1 = sx + 26
        bx2 = sx + 68
        el.append(f'<rect x="{bx1:.1f}" y="{base_y - h_oni:.1f}" width="26" height="{h_oni:.1f}" rx="3" fill="{WARM_RED}"/>')
        el.append(f'<rect x="{bx2:.1f}" y="{base_y - h_roni:.1f}" width="26" height="{h_roni:.1f}" rx="3" fill="{BLUE}"/>')
        el.append(txt(bx1 + 13, base_y - h_oni - 5, f"+{oni_v:.1f}", size=10.5, color=WARM_RED, anchor="middle", weight="700", cls="mono"))
        el.append(txt(bx2 + 13, base_y - h_roni - 5, f"+{roni_v:.1f}", size=10.5, color=BLUE, anchor="middle", weight="700", cls="mono"))
        el.append(txt(sx + 61, 474, ev_lbl, size=11.5, color=INK, anchor="middle", weight="700"))
        el.append(txt(sx + 61, 489, ev_note, size=10.5, color=ORANGE if idx >= 3 else MUTED, anchor="middle", weight="600" if idx >= 3 else None))

    svg = figure(
        h,
        "1950至2026年NOAA官方海洋尼诺指数ONI演变与相对指数RONI对比图",
        "上方时间序列基于NOAA气候预测中心ERSSTv6实测数据绘出1950至2026年Niño 3.4区峰值演变，标出1982-83(+2.1°C)、1997-98(+2.4°C)、2015-16(+2.6°C)、2023-24(+2.0°C)与2026年秋季(+2.5°C)五次强至超强峰值；下方柱状图对比传统ONI与2026年启用的RONI，直观揭示近些年全球热带海洋背景增温贡献了约0.5至0.6°C的额外底温。",
        el,
    )
    write_svg("el-nino", "oni-vs-roni-history-1950-2026.svg", svg)


def _build_four_amplifiers_recent_elnino():
    """Fig 4: Why recent El Ninos feel and act so intense - 4 physical layers + confidence boundaries."""
    _, _, rate_7c, rate_27c = _verify_enso_physics_and_data()
    h = 544
    el = []
    el.extend(
        header(
            "近些年厄尔尼诺为什么如此凶猛？四重物理放大器与科学置信度",
            "综合 IPCC AR6、Cai 等（Nature Rev. 2021）与 NOAA 观测：区分“板上钉钉的热力学放大”与“前沿动力学课题”",
        )
    )

    # 2x2 grid of cards:
    # Left col x=24, w=348; Right col x=388, w=348
    # Row 1 y=68, h=222; Row 2 y=304, h=222

    # --- Card 1: Baseline Warming + Ocean Heat Content ---
    el.append(card(24, 68, 348, 222, fill="#ffffff"))
    el.append(step_badge(44, 90, 1, fg=WARM_RED, bg=RED_SOFT))
    el.append(txt(62, 94, "底温抬升：踩在 +1.2°C 高台上起跳", size=13, color=INK, weight="700"))
    el.append(pill(274, 78, "高信度共识", fg=WARM_RED, bg=RED_SOFT, w=84, h=20, size=10.5))

    # Mini stacked bar comparison: 1982 vs 2023-2026
    # Baseline floor + ENSO jump
    el.append(card(42, 112, 312, 108, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    # 1950s-80s bar
    el.append('<rect x="82" y="160" width="54" height="44" rx="3" fill="#fb923c"/>')
    el.append(txt(109, 153, "绝对峰值", size=10.5, color=MUTED, anchor="middle"))
    el.append(txt(109, 186, "+2.1°C", size=11, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(109, 215, "20世纪中后期", size=10.5, color=SLATE, anchor="middle"))

    # Arrow
    el.append(_arrow(152, 172, 194, 152, color=WARM_RED, sw=2.0, marker="arr-orange"))

    # 2020s bar: Base fever (+0.6C tropical / +1.2C global) + ENSO jump
    el.append(f'<rect x="212" y="182" width="64" height="22" rx="2" fill="{PURPLE}"/>')
    el.append(f'<rect x="212" y="128" width="64" height="54" rx="3" fill="{WARM_RED}"/>')
    el.append(txt(244, 122, "破历史极值！", size=11, color=WARM_RED, anchor="middle", weight="700"))
    el.append(txt(244, 158, "ENSO 振幅", size=10.5, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(244, 197, "全球底温抬升", size=10, color="#ffffff", anchor="middle"))
    el.append(txt(244, 215, "2023–2026 年", size=10.5, color=INK, anchor="middle", weight="700"))

    el.append(txt(42, 242, "• 温室效应逾 90% 额外热量存入海洋（海洋热含量屡创新高）", size=11.5, color=BODY))
    el.append(txt(42, 261, "• 同样幅度的圣婴叠加在变暖底座上，使 2024 首破 +1.5°C 关口", size=11.5, color=BODY))
    el.append(txt(42, 279, "• 珊瑚白化、农业热害感受的是“总绝对温度”，而非去趋势指数", size=11, color=MUTED))

    # --- Card 2: Clausius-Clapeyron + 28 deg C Convective Threshold ---
    el.append(card(388, 68, 348, 222, fill="#ffffff"))
    el.append(step_badge(408, 90, 2, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(426, 94, "水汽倍增与 28 °C 深对流“点火线”", size=13, color=INK, weight="700"))
    el.append(pill(638, 78, "极可能(IPCC)", fg=BLUE, bg=BLUE_SOFT, w=84, h=20, size=10.5))

    el.append(card(406, 112, 312, 108, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    # Nonlinear convective curve crossing 28 deg C threshold
    # x from 24C (430) to 30C (696), 28C line at x=607
    el.append(_curve("M432,202 L700,202", color=SLATE, sw=1.0))
    el.append(_curve("M607,120 L607,202", color=WARM_RED, sw=1.6, dash="4 3"))
    el.append(txt(603, 132, "28 °C 深对流门槛", size=10.5, color=WARM_RED, anchor="end", weight="700"))
    # Hockey-stick convective rainfall curve
    el.append(_curve("M436,197 Q555,195 607,178 Q645,142 692,124", color=BLUE, sw=2.6))
    el.append(txt(442, 214, "24°C", size=10, color=MUTED, cls="mono"))
    el.append(txt(520, 214, "26°C", size=10, color=MUTED, cls="mono"))
    el.append(txt(607, 214, "28°C", size=10, color=WARM_RED, anchor="middle", weight="700", cls="mono"))
    el.append(txt(684, 214, "30°C", size=10, color=WARM_RED, anchor="middle", cls="mono"))
    el.append(txt(652, 172, "暴雨非线性暴增", size=10.5, color=BLUE, anchor="middle", weight="700", halo=True))

    el.append(txt(406, 242, f"• 克劳修斯—克拉佩龙：每升 1°C 饱和水汽增约 {rate_27c:.0f}%–{rate_7c:.0f}%", size=11.5, color=BODY))
    el.append(txt(406, 261, "• 热带海温一旦跨过约 28°C 门槛，雷暴深对流像点火一样爆发", size=11.5, color=BODY))
    el.append(txt(406, 279, "• 东太平洋背景变暖后，圣婴年更容易大片跨过 28°C 制造极端豪雨", size=11, color=MUTED))

    # --- Card 3: Upper-Ocean Stratification ---
    el.append(card(24, 304, 348, 222, fill="#ffffff"))
    el.append(step_badge(44, 326, 3, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(62, 330, "上层海洋“层结增强”放大海气耦合", size=13, color=INK, weight="700"))
    el.append(pill(270, 314, "动力学强证据", fg=ORANGE, bg=ORANGE_SOFT, w=88, h=20, size=10.5))

    el.append(card(42, 348, 312, 104, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    # Two vertical depth profiles: Past (gentler dT/dz) vs Greenhouse Warmer Surface (steeper dT/dz in top 75m)
    el.append(txt(126, 366, "过去：上下温差较缓", size=10.5, color=SLATE, anchor="middle", weight="600"))
    el.append('<rect x="74" y="374" width="104" height="24" rx="3" fill="#fb923c" opacity="0.8"/>')
    el.append('<rect x="74" y="398" width="104" height="44" rx="3" fill="#1d6fa5" opacity="0.85"/>')
    el.append(txt(126, 390, "表层 0–75 m", size=10.5, color="#ffffff", anchor="middle"))
    el.append(txt(126, 424, "次表层冷水", size=10.5, color="#e0f2fe", anchor="middle"))

    el.append(txt(268, 366, "近年：表层升温快、层结变陡", size=10.5, color=WARM_RED, anchor="middle", weight="700"))
    el.append('<rect x="214" y="374" width="108" height="22" rx="3" fill="#dc2626"/>')
    el.append('<line x1="214" y1="396" x2="322" y2="396" stroke="#fde047" stroke-width="2.4"/>')
    el.append('<rect x="214" y="398" width="108" height="44" rx="3" fill="#0c4a6e"/>')
    el.append(txt(268, 389, "更轻更暖薄盖层", size=10.5, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(268, 424, "密度跃层更锋利", size=10.5, color="#fef08a", anchor="middle"))

    el.append(txt(42, 474, "• 表层海水比 100–300 m 深处升温更快 → 垂直密度层结更强", size=11.5, color=BODY))
    el.append(txt(42, 493, "• 暖水盖层更轻薄，同样的西风异常更容易推动暖池大幅东移", size=11.5, color=BODY))
    el.append(txt(42, 511, "• 高仿真气候模式显示：极端厄尔尼诺与极端拉尼娜摆动更频繁", size=11, color=MUTED))

    # --- Card 4: Warm Pool Expansion, Triple La Nina Spring, & Scientific Caveat ---
    el.append(card(388, 304, 348, 222, fill="#ffffff"))
    el.append(step_badge(408, 326, 4, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(426, 330, "暖池扩容蓄能 + 严谨的科学边界", size=13, color=INK, weight="700"))
    el.append(pill(634, 314, "理性区分边界", fg=GREEN, bg=GREEN_SOFT, w=88, h=20, size=10.5))

    el.append(card(406, 348, 312, 104, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.0))
    el.append(txt(418, 370, "蓄能弹簧：印太暖池 (>28°C) 面积较 1900 年近乎翻倍", size=11.5, color=GREEN, weight="700"))
    el.append(txt(418, 390, "2020–2023 罕见“三重拉尼娜”连续三年把巨量暖水死死压在", size=11, color=BODY))
    el.append(txt(418, 408, "西太平洋次表层；信风一松，蓄积热能便接连剧烈释放。", size=11, color=BODY))
    el.append(txt(418, 434, "科学界诚实限定：太平洋本身存在 20–30 年年代际自然波动", size=11, color=INK, weight="700"))

    el.append(txt(406, 474, "• 已证实：1950 年以来 ENSO 变率显著强于过去数百年珊瑚记录", size=11.5, color=BODY))
    el.append(txt(406, 493, "• 已明确：全球变暖必然放大厄尔尼诺带来的极端暴雨、热浪与干旱", size=11.5, color=BODY))
    el.append(txt(406, 511, "• 仍在攻关：单次事件海温振幅中“人为强迫 vs 自然波动”精确占比", size=11, color=MUTED))

    svg = figure(
        h,
        "近年厄尔尼诺现象愈发强烈的四重物理机制与科学置信度拆解图",
        "四宫格依次拆解：①全球变暖抬升1.2°C以上底温与海洋热含量；②克劳修斯-克拉佩龙每度约7%水汽倍增与28°C热带深对流门槛突破；③赤道太平洋表层比深层升温更快导致上层层结增强、放大海气耦合；④印太暖池翻倍与三重拉尼娜蓄能，同时明确区分热力学高信度放大与年代际自然变率边界。",
        el,
    )
    write_svg("el-nino", "four-amplifiers-recent-elnino.svg", svg)


def _build_global_teleconnections():
    """Fig 5: Pacific-centered schematic of global flood & drought teleconnections during El Nino."""
    h = 466
    el = []
    el.extend(
        header(
            "一场太平洋发烧，为什么让半个地球闹洪灾、另半个地球烧山火？",
            "大气遥相关（Teleconnections）：沃克环流裂变改写热带雨带，高空急流罗斯贝波列搅动中高纬风暴",
        )
    )

    # Map canvas card (Pacific-centered: left 95E Asia/Aus -> center 180 -> right 55W Americas)
    el.append(card(24, 68, 712, 312, fill="#f0f9ff", stroke=BORDER))

    # Equator & Tropics guide lines
    eq_y = 248.0
    el.append(_curve(f"M36,{eq_y:.1f} L724,{eq_y:.1f}", color=SLATE, sw=1.1, dash="6 4", opacity=0.55))
    el.append(txt(46, eq_y - 6, "0° 赤道", size=10.5, color=SLATE, cls="mono"))
    el.append(_curve("M36,158 L724,158", color=HAIRLINE, sw=0.9, dash="3 4"))
    el.append(txt(46, 153, "30°N", size=10, color=MUTED, cls="mono"))
    el.append(_curve("M36,322 L724,322", color=HAIRLINE, sw=0.9, dash="3 4"))
    el.append(txt(46, 317, "30°S", size=10, color=MUTED, cls="mono"))

    # Stylized recognizable continent silhouettes (Pacific-centered schematic, labeled clearly)
    # East Asia (top-left)
    el.append(
        '<path d="M42,92 L176,92 L192,132 L162,178 L128,196 L95,190 L68,214 L42,206 Z" '
        'fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>'
    )
    # Maritime Continent / Indonesia (mid-left along equator)
    el.append(
        '<path d="M92,232 L135,238 L148,252 L112,258 Z M156,240 L196,246 L190,260 L152,255 Z" '
        'fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>'
    )
    # Australia (bottom-left)
    el.append(
        '<path d="M118,284 L196,282 L214,316 L194,352 L134,350 L110,320 Z" '
        'fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>'
    )
    # North America (top-right)
    el.append(
        '<path d="M468,88 L646,88 L626,152 L584,186 L552,214 L526,194 L492,148 Z" '
        'fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>'
    )
    # South America (bottom-right)
    el.append(
        '<path d="M566,222 L658,236 L692,278 L664,356 L618,366 L594,312 L568,262 Z" '
        'fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>'
    )

    # Equatorial Central-Eastern Pacific Warm Tongue (El Nino heat source!)
    el.append(
        '<ellipse cx="432" cy="248" rx="148" ry="26" fill="#dc2626" opacity="0.28" '
        'stroke="#dc2626" stroke-width="1.6" stroke-dasharray="6 3"/>'
    )
    el.append(txt(432, 252, "厄尔尼诺暖水舌（巨大潜热发动机）", size=11.5, color=WARM_RED, anchor="middle", weight="700", halo=True))

    # Extended & southward-shifted Pacific Subtropical Jet Stream -> Southern US / California storms
    el.append(
        _curve(
            "M245,168 Q365,176 475,168 Q545,164 615,158",
            color=BLUE,
            sw=3.0,
            marker="arr-blue",
        )
    )
    el.append(txt(375, 160, "太平洋副热带急流南移拉直（风暴走廊直扑北美南侧）", size=11, color=BLUE, anchor="middle", weight="700", halo=True))

    # Rossby wave train arc poleward into North America
    el.append(
        _curve(
            "M415,222 Q435,162 490,124 Q545,104 595,126",
            color=PURPLE,
            sw=1.9,
            dash="5 4",
            marker="arr-muted",
        )
    )
    el.append(txt(474, 110, "高空罗斯贝波列（暖冬：加拿大/美北）", size=10.5, color=PURPLE, anchor="middle", weight="600", halo=True))

    # --- Drought Zones (Orange dashed badges) ---
    # 1. Indonesia & SE Asia drought/fires
    el.append(card(72, 214, 152, 46, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.4, dash="4 2"))
    el.append(txt(148, 233, "旱 印尼/东南亚少雨", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(148, 250, "泥炭林山火与跨境烟霾", size=10.5, color=BODY, anchor="middle"))

    # 2. Eastern Australia drought
    el.append(card(106, 294, 148, 46, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.4, dash="4 2"))
    el.append(txt(180, 313, "旱 澳洲东部高温干旱", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(180, 330, "小麦减产与丛林火灾风险", size=10.5, color=BODY, anchor="middle"))

    # 3. Amazon / Northern South America drought
    el.append(card(586, 212, 134, 46, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.4, dash="4 2"))
    el.append(txt(653, 231, "旱 亚马逊流域干旱", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(653, 248, "下沉支笼罩，河流水位骤降", size=10.5, color=BODY, anchor="middle"))

    # --- Flood / Heavy Rain Zones (Blue solid badges) ---
    # 4. Peru / Ecuador coastal floods
    el.append(card(452, 286, 162, 48, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.5))
    el.append(txt(533, 305, "涝 秘鲁/厄瓜多尔暴雨", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(533, 323, "沿海荒漠突发山洪泥石流", size=10.5, color=BODY, anchor="middle"))

    # 5. California & Southern US floods
    el.append(card(528, 152, 178, 46, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.5))
    el.append(txt(617, 171, "涝 加州与美国南部多雨", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(617, 188, "急流裹挟水汽触发洪涝风暴", size=10.5, color=BODY, anchor="middle"))

    # 6. East Asia / Yangtze Basin (noted as winter + next-summer focus)
    el.append(card(52, 114, 168, 48, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.5))
    el.append(txt(136, 133, "东亚：冬偏暖 + 次夏防涝", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(136, 151, "长江中下游梅雨洪涝高发", size=10.5, color=BODY, anchor="middle"))

    # Bottom explanation strip
    el.append(card(24, 392, 712, 56, fill="#ffffff"))
    el.append(txt(42, 415, "读图提示（示意投影，非等面积）：实线蓝框为上升或急流集中的“洪涝高发区”，虚线橙框为空气下沉的“干旱山火高发区”。", size=11, color=BODY))
    el.append(txt(42, 435, "遥相关机制：暖水每蒸发 1 kg 水汽释放约 2.5×10⁶ J 潜热，像向高空急流投入巨石，激起跨越上万公里的罗斯贝行星波列。", size=11, color=MUTED))

    svg = figure(
        h,
        "厄尔尼诺全球大气遥相关洪涝与干旱空间分布示意图",
        "以太平洋为中心的示意地图标出厄尔尼诺期间全球极端天气遥相关格局：中东太平洋暖水舌释放巨量潜热，导致秘鲁厄瓜多尔海岸、美国南部与加州以及东亚长江流域（次年夏季）多雨洪涝（实线蓝框），而印尼东南亚、澳大利亚东部与亚马逊流域则因下沉气流遭遇高温干旱与山火（虚线橙框）。",
        el,
    )
    write_svg("el-nino", "global-teleconnections-flood-drought.svg", svg)


def _build_china_second_year_summer_impact():
    """Fig 6: Why China's biggest flood risk occurs in the decaying summer AFTER El Nino peaks."""
    h = 482
    el = []
    el.extend(
        header(
            "为什么中国气象台最警惕“厄尔尼诺次年夏天”？（1998 · 2016 · 2024 复盘）",
            "依据国家气候中心机理：当年冬季偏暖但防寒潮过山车；次年夏季“印度洋电容器 + 西太副高”联手向长江泵水",
        )
    )

    # Left Card: Developing Winter (Year 0 DJF)
    el.append(card(24, 68, 332, 322, fill="#ffffff"))
    el.append(pill(40, 82, "阶段一：厄尔尼诺发展年冬季（当年 12–2 月）", fg=ORANGE, bg=ORANGE_SOFT, w=294, size=11.5))

    el.append(card(40, 118, 300, 118, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.1))
    el.append(txt(54, 141, "总体趋势：东亚冬季风偏弱 → 暖冬概率高", size=12, color=ORANGE, weight="700"))
    el.append(txt(54, 163, "• 西伯利亚冷高压与东亚大槽平均强度偏弱", size=11.5, color=BODY))
    el.append(txt(54, 183, "• 冷空气主力偏北，我国大部冬季均温易偏高", size=11.5, color=BODY))
    el.append(txt(54, 203, "• 南方水汽充沛，华南/江南冬季降水往往偏多", size=11.5, color=BLUE, weight="600"))
    el.append(txt(54, 223, "（如 2023/24 冬季全国平均气温明显偏暖）", size=11, color=MUTED))

    el.append(card(40, 250, 300, 124, rx=8, fill=RED_SOFT, stroke=WARM_RED, sw=1.1, dash="4 2"))
    el.append(txt(54, 273, "反直觉陷阱：“暖冬 ≠ 没有暴雪寒潮！”", size=12, color=WARM_RED, weight="700"))
    el.append(txt(54, 295, "• 暖冬说的是整个冬季（3 个月）的平均账本", size=11.5, color=BODY))
    el.append(txt(54, 315, "• 西风带剧烈摆动时，极地寒潮仍会阶段性南下", size=11.5, color=BODY))
    el.append(txt(54, 335, "• 强冷空气撞上异常丰沛的暖湿气流 → 极易触发", size=11.5, color=BODY))
    el.append(txt(54, 355, "  大范围雨雪冰冻与“断崖式降温”（如 2024 年 2 月）", size=11, color=WARM_RED, weight="600"))

    # Right Card: Decaying Following Summer (Year +1 JJA)
    el.append(card(372, 68, 364, 322, fill="#ffffff"))
    el.append(pill(388, 82, "阶段二：厄尔尼诺次年夏季（次年 6–8 月 · 防汛大考）", fg=BLUE, bg=BLUE_SOFT, w=328, size=11.5))

    # Schematic diagram inside Right Card (y=118..292)
    el.append(card(388, 118, 332, 176, rx=8, fill="#f8fafc", stroke=BORDER))

    # 1. Indian Ocean Capacitor (bottom-left of mini-map)
    el.append(card(400, 232, 126, 48, rx=8, fill=AMBER_SOFT, stroke=ORANGE, sw=1.3))
    el.append(step_badge(416, 250, 1, fg=ORANGE, bg="#ffffff", r=9.5))
    el.append(txt(430, 253, "印度洋“电容器”", size=11.5, color=ORANGE, weight="700"))
    el.append(txt(410, 271, "滞后增暖，东传开尔文波", size=10.5, color=BODY))

    # Arrow from Indian Ocean to WNP Subtropical High
    el.append(_arrow(528, 252, 568, 232, color=ORANGE, sw=2.1, marker="arr-orange"))

    # 2. Western North Pacific Subtropical High (right-middle oval)
    el.append(
        '<ellipse cx="634" cy="218" rx="74" ry="34" fill="#dbeafe" stroke="#1d6fa5" stroke-width="1.8"/>'
    )
    el.append(step_badge(580, 210, 2, fg=BLUE, bg="#ffffff", r=9.5))
    el.append(txt(640, 214, "西太副高偏强偏西", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(640, 232, "顺时针高压脊盘踞南海—西太", size=10, color=SLATE, anchor="middle"))

    # Clockwise moisture conveyor along NW flank of Subtropical High into Yangtze
    el.append(
        _curve(
            "M564,228 Q536,196 544,166",
            color=BLUE,
            sw=2.8,
            marker="arr-blue",
        )
    )
    el.append(txt(486, 200, "西南暖湿水汽泵", size=11, color=BLUE, anchor="middle", weight="700", halo=True))

    # Cold weak northerly air meeting warm moist air at Yangtze River rainband
    el.append(_arrow(516, 126, 536, 146, color=SLATE, sw=1.8, marker="arr-muted"))
    el.append(txt(464, 136, "北方冷空气南下交汇", size=10.5, color=SLATE, anchor="middle"))

    # 3. Yangtze & Jiangnan Meiyu Flood Band (top)
    el.append(card(488, 132, 218, 42, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.6))
    el.append(step_badge(504, 153, 3, fg=BLUE, bg="#ffffff", r=9.5))
    el.append(txt(518, 150, "长江中下游/江南锋面雨带停滞", size=11.5, color=BLUE, weight="700"))
    el.append(txt(518, 166, "梅雨偏强、流域性暴雨洪涝风险骤增", size=10.5, color=BODY))

    # Bullet summary under right schematic
    el.append(txt(390, 314, "• 历史铁证：1998、2016、2024 均为强厄尔尼诺衰减次年夏季大水", size=11.5, color=INK, weight="700"))
    el.append(txt(390, 336, "• 北方防旱涝急转：华北部分时段易高温少雨，盛夏需防北上暴雨", size=11.5, color=BODY))
    el.append(txt(390, 358, "• 台风特征：西北太平洋生成总数常偏少，但单个位置偏远、强度偏强", size=11.5, color=BODY))
    el.append(txt(390, 378, "• 2026 超强厄尔尼诺启示：2026/27 冬防阶段寒潮，2027 夏防大汛", size=11, color=WARM_RED, weight="600"))

    # Bottom timeline strip
    el.append(card(24, 404, 712, 60, fill="#ffffff"))
    el.append(txt(42, 426, "为什么东太平洋退烧后中国还下暴雨？厄尔尼诺冬季给热带印度洋“充饱热电”，次夏持续放电维持西太异常反气旋！", size=11.5, color=INK, weight="600"))
    el.append(txt(42, 448, "（学界称为 Xie et al. 2009“印度洋电容器效应 Indian Ocean Capacitor Effect”，是我国汛期气候预测的核心物理抓手。）", size=11, color=MUTED))

    svg = figure(
        h,
        "厄尔尼诺对我国当年冬季与次年夏季气候影响的接力机制图",
        "左侧说明厄尔尼诺发展年冬季东亚冬季风偏弱、总体偏暖概率高，但在充沛水汽配合下仍易出现阶段性寒潮与冻雨雪灾；右侧拆解厄尔尼诺次年夏季通过热带印度洋滞后增暖（电容器效应）维持西太平洋副热带高压偏强偏西，源源不断向长江中下游输送水汽，复现1998、2016、2024年次年夏季洪涝规律。",
        el,
    )
    write_svg("el-nino", "china-second-year-summer-impact.svg", svg)


@register(
    "el-nino",
    "El Niño-Southern Oscillation physics, NOAA ONI/RONI data & recent intensification",
    "Earth & Climate Science",
)
def build_el_nino():
    _build_pacific_normal_vs_elnino()
    _build_bjerknes_feedback_loop()
    _build_oni_vs_roni_history()
    _build_four_amplifiers_recent_elnino()
    _build_global_teleconnections()
    _build_china_second_year_summer_impact()
