"""Quantitative & step-by-step SVG visuals for Circulatory Systems (Human & Comparative Zoology).

Generates 5 verified 760x520 figures under assets/images/circulatory-systems/:
1. human-double-circulation-anim.svg (1-shot CSS animation + reduced-motion fallback)
2. hemodynamics-pressure-velocity-cascade.svg (quantitative pressure, area & velocity curves)
3. open-vs-closed-and-insect-hack.svg (Fick barrier, insect tracheal bypass & octopus 3-heart loop)
4. vertebrate-heart-evolution-and-extremes.svg (1->3->4 chambers, crocodile Panizza shunt & giraffe)
5. rainbow-blood-chemistry-spectrum.svg (Fe/Cu/biliverdin/clear 5-color blood chemistry gallery)
"""

import math
from .core import (
    BG,
    BLUE,
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
    figure as _core_figure,
    header as _core_header,
    pill as _core_pill,
    register,
    step_badge,
    txt as _core_txt,
    write_svg,
)


def header(title: str, subtitle: str) -> str:
    return "\n".join(_core_header(title, subtitle))


def txt(x, y, value, size=12, weight=None, fill=BODY, anchor="start") -> str:
    return _core_txt(x, y, value, size=size, color=fill, anchor=anchor, weight=weight)


def pill(x, y, w, h, label, fill=BLUE_SOFT, stroke=BLUE, text_fill=BLUE, size=11) -> str:
    return _core_pill(x, y, label, fg=text_fill, bg=fill, border=stroke, w=w, h=h, size=size)


def figure(width, height, title, description, elements, extra_css="") -> str:
    return _core_figure(height, title, description, elements, extra_css=extra_css, width=width)

SUBDIR = "circulatory-systems"
RED = "#b91c1c"
RED_BRIGHT = "#dc2626"
RED_SOFT = "#fef2f2"
VENOUS = "#1d4ed8"
VENOUS_DARK = "#1e3a8a"
VENOUS_SOFT = "#eff6ff"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
VIOLET = "#9333ea"
VIOLET_SOFT = "#faf5ff"
ICE_DARK = "#0369a1"
ICE_SOFT = "#f0f9ff"


def _fick_diffusion_seconds(distance_m: float, diff_m2_s: float = 2.0e-9) -> float:
    """Characteristic 1D diffusion time t = L^2 / (2D) for O2 in water/tissue."""
    return (distance_m ** 2) / (2.0 * diff_m2_s)


def build_human_double_circulation_anim() -> str:
    """1. 1-shot animated figure-8 diagram of human 4-chambered double circulation."""
    # Quantitative physiological assertions:
    # Stroke volume ~70 mL * 72 bpm = 5,040 mL/min (~7,258 L/day)
    co_l_min = 0.070 * 72.0
    co_l_day = co_l_min * 60.0 * 24.0
    assert 4.8 <= co_l_min <= 5.5
    assert 7000.0 <= co_l_day <= 7600.0
    # Harvey 1628 conservative bound: 4.7 mL * 2000 beats/hr * 24 hr = 225.6 L/day
    harvey_l_day = 0.0047 * 2000.0 * 24.0
    assert 220.0 <= harvey_l_day <= 230.0

    extra_css = """
      @keyframes rbcPulmOut {
        0%   { transform: translate(334px, 240px); opacity: 0; }
        12%  { transform: translate(334px, 240px); opacity: 1; }
        46%  { transform: translate(316px, 146px); opacity: 1; }
        82%  { transform: translate(366px, 118px); opacity: 1; }
        100% { transform: translate(366px, 118px); opacity: 1; }
      }
      @keyframes rbcPulmIn {
        0%   { transform: translate(394px, 118px); opacity: 0.25; }
        35%  { transform: translate(444px, 146px); opacity: 1; }
        78%  { transform: translate(426px, 206px); opacity: 1; }
        100% { transform: translate(426px, 186px); opacity: 1; }
      }
      @keyframes rbcSysOut {
        0%   { transform: translate(426px, 286px); opacity: 0.25; }
        35%  { transform: translate(466px, 344px); opacity: 1; }
        78%  { transform: translate(414px, 398px); opacity: 1; }
        100% { transform: translate(398px, 398px); opacity: 1; }
      }
      @keyframes rbcSysIn {
        0%   { transform: translate(356px, 398px); opacity: 0.25; }
        42%  { transform: translate(294px, 344px); opacity: 1; }
        84%  { transform: translate(334px, 206px); opacity: 1; }
        100% { transform: translate(334px, 186px); opacity: 1; }
      }
      @keyframes heartPulse {
        0%, 100% { stroke-width: 2.2px; }
        35%      { stroke-width: 3.6px; }
        70%      { stroke-width: 2.2px; }
      }
      .rbc-p-out { animation: rbcPulmOut 5.8s ease-in-out 1 forwards; }
      .rbc-p-in  { animation: rbcPulmIn  5.8s ease-in-out 1 forwards; }
      .rbc-s-out { animation: rbcSysOut  5.8s ease-in-out 1 forwards; }
      .rbc-s-in  { animation: rbcSysIn   5.8s ease-in-out 1 forwards; }
      .lv-wall   { animation: heartPulse 2.9s ease-in-out 2 forwards; }
      @media (prefers-reduced-motion: reduce) {
        .rbc-p-out { animation: none !important; transform: translate(366px, 118px); opacity: 1 !important; }
        .rbc-p-in  { animation: none !important; transform: translate(426px, 186px); opacity: 1 !important; }
        .rbc-s-out { animation: none !important; transform: translate(398px, 398px); opacity: 1 !important; }
        .rbc-s-in  { animation: none !important; transform: translate(334px, 186px); opacity: 1 !important; }
        .lv-wall   { animation: none !important; }
      }
    """

    body = [
        header(
            "人体四腔双泵串联回路：为什么一颗心要拆成“低压右泵”与“高压左泵”？",
            "先看中央四腔心与四道单向瓣膜 → 再顺箭头跟读 8 字双循环 → 对比右心 25/10 与左心 120/80 mmHg 压差",
        ),
        # Left card: Right Heart Low-Pressure Pulmonary Pump
        card(24, 152, 182, 224, fill=VENOUS_SOFT, stroke="#93c5fd"),
        step_badge(42, 174, 1, VENOUS),
        txt(62, 179, "右心：低压护肺泵", size=13, weight="700", fill=VENOUS_DARK),
        txt(36, 204, "• 路径：右心房 → 三尖瓣", size=11.5, fill=INK),
        txt(36, 224, "  → 右心室 → 肺动脉瓣", size=11.5, fill=INK),
        txt(36, 248, "• 肺动脉压：25 / 10 mmHg", size=11.5, weight="700", fill=VENOUS_DARK),
        txt(36, 268, "• 右室肌壁：薄（3–4 mm）", size=11.5, fill=BODY),
        txt(36, 292, "• 原因：肺泡膜仅 0.3 μm，", size=11, fill=BODY),
        txt(36, 310, "  高压会把液体压进肺泡！", size=11, fill=BODY),
        pill(36, 326, 158, 22, "陷阱：肺动脉流暗红缺氧血", fill="#dbeafe", stroke=VENOUS, text_fill=VENOUS_DARK, size=10.5),
        # Right card: Left Heart High-Pressure Systemic Pump
        card(554, 152, 182, 224, fill=RED_SOFT, stroke="#fca5a5"),
        step_badge(572, 174, 2, RED),
        txt(592, 179, "左心：高压全身泵", size=13, weight="700", fill=RED),
        txt(566, 204, "• 路径：左心房 → 二尖瓣", size=11.5, fill=INK),
        txt(566, 224, "  → 左心室 → 主动脉瓣", size=11.5, fill=INK),
        txt(566, 248, "• 主动脉压：120 / 80 mmHg", size=11.5, weight="700", fill=RED),
        txt(566, 268, "• 左室肌壁：厚 3 倍(8–12mm)", size=11.5, fill=BODY),
        txt(566, 292, "• 自带电网：窦房结起搏 →", size=11, fill=BODY),
        txt(566, 310, "  房室结延 0.1s → 心尖上挤", size=11, fill=BODY),
        pill(566, 326, 158, 22, "冠脉特例：主要在舒张期供血", fill="#fee2e2", stroke=RED, text_fill=RED, size=10.5),
        # Top Pulmonary Capillary Zone
        card(224, 82, 312, 56, fill="#f8fafc", stroke=BORDER),
        txt(380, 102, "肺泡毛细血管网（吸 O₂ · 排 CO₂ · 气血屏障 ~0.3 μm）", size=12, weight="700", fill=INK, anchor="middle"),
        txt(294, 125, "肺动脉（蓝·缺氧）↗", size=11, weight="600", fill=VENOUS, anchor="middle"),
        txt(466, 125, "↘ 肺静脉（红·富氧）", size=11, weight="600", fill=RED, anchor="middle"),
        # Bottom Systemic Capillary Zone
        card(224, 386, 312, 62, fill="#f8fafc", stroke=BORDER),
        txt(380, 406, "全身毛细血管网 + 肝门静脉双毛细血管海关", size=12, weight="700", fill=INK, anchor="middle"),
        txt(380, 426, "左右心流量严格相等：70 mL × 72 次/分 ≈ 5 L/min（7,200 L/天）", size=11, fill=BODY, anchor="middle"),
        # Figure-8 Vascular Arcs connecting Heart <-> Lungs & Body
        # Pulmonary artery: RV (338, 252) -> up-left -> Lung left (348, 138)
        f'<path d="M 344 252 C 296 226, 296 156, 344 138" fill="none" stroke="{VENOUS}" stroke-width="4" stroke-dasharray="6 3"/>',
        # Pulmonary vein: Lung right (416, 138) -> down-right -> LA (426, 198)
        f'<path d="M 416 138 C 464 156, 464 182, 434 198" fill="none" stroke="{RED_BRIGHT}" stroke-width="4"/>',
        # Systemic aorta: LV (422, 266) -> arch -> down-right -> Body right (424, 386)
        f'<path d="M 416 268 C 488 292, 488 362, 424 386" fill="none" stroke="{RED_BRIGHT}" stroke-width="5"/>',
        # Systemic venae cavae: Body left (336, 386) -> up-left -> RA (326, 198)
        f'<path d="M 336 386 C 272 362, 272 224, 326 198" fill="none" stroke="{VENOUS}" stroke-width="5" stroke-dasharray="7 3"/>',
        # Central 4-chamber Heart Box (x=318..442, y=174..336)
        card(318, 170, 124, 166, rx=18, fill="#ffffff", stroke=SLATE, sw=2.0),
        # Interatrial & interventricular septum
        f'<line x1="380" y1="172" x2="380" y2="334" stroke="{SLATE}" stroke-width="4"/>',
        f'<line x1="320" y1="242" x2="440" y2="242" stroke="{SLATE}" stroke-width="2" stroke-dasharray="4 2"/>',
        # Four chambers fills & labels (patient's right = viewer's left!)
        f'<rect x="323" y="175" width="53" height="63" rx="10" fill="{VENOUS_SOFT}" stroke="{VENOUS}" stroke-width="1.4"/>',
        txt(349, 202, "右心房", size=11.5, weight="700", fill=VENOUS_DARK, anchor="middle"),
        txt(349, 220, "三尖瓣↓", size=10, fill=VENOUS_DARK, anchor="middle"),
        f'<rect x="384" y="175" width="53" height="63" rx="10" fill="{RED_SOFT}" stroke="{RED_BRIGHT}" stroke-width="1.4"/>',
        txt(410, 202, "左心房", size=11.5, weight="700", fill=RED, anchor="middle"),
        txt(410, 220, "↓二尖瓣", size=10, fill=RED, anchor="middle"),
        f'<rect x="323" y="246" width="53" height="84" rx="12" fill="{VENOUS_SOFT}" stroke="{VENOUS}" stroke-width="1.8"/>',
        txt(349, 282, "右心室", size=11.5, weight="700", fill=VENOUS_DARK, anchor="middle"),
        txt(349, 300, "25/10", size=10.5, weight="700", fill=VENOUS_DARK, anchor="middle"),
        txt(349, 316, "薄壁泵", size=10, fill=BODY, anchor="middle"),
        f'<rect class="lv-wall" x="384" y="246" width="53" height="84" rx="12" fill="{RED_SOFT}" stroke="{RED_BRIGHT}" stroke-width="3.2"/>',
        txt(410, 282, "左心室", size=11.5, weight="700", fill=RED, anchor="middle"),
        txt(410, 300, "120/80", size=10.5, weight="700", fill=RED, anchor="middle"),
        txt(410, 316, "厚壁泵", size=10, fill=BODY, anchor="middle"),
        # Heart sound note below heart
        txt(380, 356, "心音“咚-哒”= 房室瓣关 → 动脉瓣关", size=10.5, weight="600", fill=SLATE, anchor="middle"),
        # 1-shot animated RBC tokens placed on clear vessel coordinates
        f'<g class="rbc-p-out"><circle cx="0" cy="0" r="5.5" fill="{VENOUS}" stroke="#ffffff" stroke-width="1.5"/></g>',
        f'<g class="rbc-p-in"><circle cx="0" cy="0" r="5.5" fill="{RED_BRIGHT}" stroke="#ffffff" stroke-width="1.5"/></g>',
        f'<g class="rbc-s-out"><circle cx="0" cy="0" r="5.5" fill="{RED_BRIGHT}" stroke="#ffffff" stroke-width="1.5"/></g>',
        f'<g class="rbc-s-in"><circle cx="0" cy="0" r="5.5" fill="{VENOUS}" stroke="#ffffff" stroke-width="1.5"/></g>',
        # Bottom historical note
        card(24, 460, 712, 42, rx=10, fill=AMBER_SOFT, stroke="#fcd34d"),
        txt(
            380,
            486,
            "哈维 1628 算术破案：哪怕按极保守每搏 4.7 mL 算，一天也泵血 ~226 kg，肝脏绝不可能凭空造出——血液必然闭环循环！",
            size=11.2,
            weight="600",
            fill=AMBER,
            anchor="middle",
        ),
    ]
    return figure(
        760,
        520,
        "人体四腔双泵串联血液循环分步与短动画示意图",
        "展示右心低压肺循环（25/10 mmHg）与左心高压体循环（120/80 mmHg）组成的8字闭环、四道单向瓣膜及哈维定量推算。",
        body,
        extra_css=extra_css,
    )


def build_hemodynamics_pressure_velocity_cascade() -> str:
    """2. Quantitative dual-panel curves of Pressure, Total Area, and Velocity across vascular tiers."""
    # Seven canonical segments:
    # (label, x_pos, sys_mmhg, dia_mmhg, mean_mmhg, area_cm2, vel_cm_s)
    segments = [
        ("主动脉", 98, 120.0, 80.0, 95.0, 4.0, 35.0),
        ("大中动脉", 192, 122.0, 76.0, 91.0, 20.0, 18.0),
        ("微动脉", 296, 85.0, 55.0, 60.0, 120.0, 3.5),
        ("毛细血管", 412, 30.0, 20.0, 24.0, 2800.0, 0.05),
        ("微静脉", 522, 15.0, 12.0, 13.0, 800.0, 0.4),
        ("静脉", 614, 9.0, 7.0, 8.0, 80.0, 4.5),
        ("腔静脉", 698, 4.0, 2.0, 3.0, 18.0, 14.0),
    ]
    # Poiseuille law assertion: halving radius increases resistance 16x
    poiseuille_factor = (1.0 / 0.5) ** 4
    assert abs(poiseuille_factor - 16.0) < 1e-9
    # Continuity ratio: capillary area / aorta area = 700x -> velocity drops 700x (35 / 0.05 = 700)
    assert abs((segments[3][5] / segments[0][5]) - (segments[0][6] / segments[3][6])) < 1e-6

    # Top panel geometry: y in [94..242] corresponds to pressure [135..0] mmHg
    p_top, p_bot = 94.0, 242.0

    def py(mmhg: float) -> float:
        return p_bot - (mmhg / 135.0) * (p_bot - p_top)

    # Smooth pressure polygon (systolic upper -> diastolic lower reversed)
    sys_pts = [(x, py(s)) for _, x, s, _, _, _, _ in segments]
    dia_pts = [(x, py(d)) for _, x, _, d, _, _, _ in reversed(segments)]
    poly_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in (sys_pts + dia_pts))
    mean_str = " ".join(f"{x:.1f},{py(m):.1f}" for _, x, _, _, m, _, _ in segments)

    # Bottom panel geometry: y in [286..426]
    b_top, b_bot = 286.0, 426.0

    def vy(vel: float) -> float:
        # Linear scale 0..38 cm/s
        return b_bot - (vel / 38.0) * (b_bot - b_top)

    def ay(area: float) -> float:
        # Log10 scale from 1 cm^2 to 4000 cm^2 so shape is faithful and readable
        lv = math.log10(max(area, 1.0)) / math.log10(4000.0)
        return b_bot - lv * (b_bot - b_top)

    vel_str = " ".join(f"{x:.1f},{vy(v):.1f}" for _, x, _, _, _, _, v in segments)
    area_str = " ".join(f"{x:.1f},{ay(a):.1f}" for _, x, _, _, _, a, _ in segments)

    body = [
        header(
            "血管树的流体力学奇迹：微动脉怎样管血压，毛细血管怎样刹慢 700 倍？",
            "上栏看血压瀑布（泊肃叶定律 R ∝ 1/r⁴ 水龙头）→ 下栏看总截面积暴涨与流速急刹（A₁v₁ = A₂v₂）",
        ),
        # Top chart card
        card(24, 82, 712, 174, fill="#ffffff", stroke=BORDER),
        txt(36, 102, "① 血压级联瀑布 (mmHg)", size=12, weight="700", fill=RED),
        # Y gridlines for top chart
        f'<line x1="74" y1="{py(120):.1f}" x2="718" y2="{py(120):.1f}" stroke="{HAIRLINE}" stroke-dasharray="3 3"/>',
        txt(68, py(120) + 4, "120", size=10.5, fill=MUTED, anchor="end"),
        f'<line x1="74" y1="{py(80):.1f}" x2="718" y2="{py(80):.1f}" stroke="{HAIRLINE}" stroke-dasharray="3 3"/>',
        txt(68, py(80) + 4, "80", size=10.5, fill=MUTED, anchor="end"),
        f'<line x1="74" y1="{py(40):.1f}" x2="718" y2="{py(40):.1f}" stroke="{HAIRLINE}" stroke-dasharray="3 3"/>',
        txt(68, py(40) + 4, "40", size=10.5, fill=MUTED, anchor="end"),
        f'<line x1="74" y1="{py(0):.1f}" x2="718" y2="{py(0):.1f}" stroke="{BORDER}"/>',
        txt(68, py(0) + 4, "0", size=10.5, fill=MUTED, anchor="end"),
        # Vertical zone guides
        *[
            f'<line x1="{x}" y1="94" x2="{x}" y2="242" stroke="#f1f5f9" stroke-width="1"/>'
            for _, x, *_ in segments
        ],
        # Pulsatile envelope + mean pressure curve
        f'<polygon points="{poly_str}" fill="#fecaca" fill-opacity="0.65"/>',
        f'<polyline points="{mean_str}" fill="none" stroke="{RED}" stroke-width="2.8"/>',
        *[
            f'<circle cx="{x}" cy="{py(m):.1f}" r="4" fill="{RED}" stroke="#ffffff" stroke-width="1.2"/>'
            for _, x, _, _, m, _, _ in segments
        ],
        # Key top annotations in clean whitespace
        pill(108, 188, 154, 22, "弹性贮器稳压 120/80", fill=RED_SOFT, stroke="#fca5a5", text_fill=RED, size=10.5),
        pill(296, 110, 214, 22, "微动脉陡降：r 缩半 → 阻力涨 16 倍！", fill=ORANGE_SOFT, stroke="#fdba74", text_fill=ORANGE, size=10.5),
        pill(504, 156, 206, 22, "静脉低压贮血 ~64%（靠瓣膜+肌肉泵）", fill=VENOUS_SOFT, stroke="#93c5fd", text_fill=VENOUS_DARK, size=10.5),
        # Bottom chart card
        card(24, 268, 712, 184, fill="#ffffff", stroke=BORDER),
        txt(36, 288, "② 流速 v (cm/s，蓝实线) vs 总横截面积 A (cm² 对数尺，绿虚线)", size=12, weight="700", fill=INK),
        f'<line x1="74" y1="{vy(35):.1f}" x2="718" y2="{vy(35):.1f}" stroke="{HAIRLINE}" stroke-dasharray="3 3"/>',
        txt(68, vy(35) + 4, "35 cm/s", size=10, fill=VENOUS_DARK, anchor="end"),
        f'<line x1="74" y1="{vy(15):.1f}" x2="718" y2="{vy(15):.1f}" stroke="{HAIRLINE}" stroke-dasharray="3 3"/>',
        txt(68, vy(15) + 4, "15 cm/s", size=10, fill=VENOUS_DARK, anchor="end"),
        f'<line x1="74" y1="{b_bot:.1f}" x2="718" y2="{b_bot:.1f}" stroke="{BORDER}"/>',
        txt(68, b_bot + 4, "0", size=10, fill=VENOUS_DARK, anchor="end"),
        # Curves
        f'<polyline points="{area_str}" fill="none" stroke="{GREEN}" stroke-width="2.6" stroke-dasharray="6 4"/>',
        f'<polyline points="{vel_str}" fill="none" stroke="{VENOUS}" stroke-width="2.8"/>',
        *[
            f'<circle cx="{x}" cy="{vy(v):.1f}" r="3.8" fill="{VENOUS}" stroke="#ffffff" stroke-width="1.2"/>'
            for _, x, _, _, _, _, v in segments
        ],
        *[
            f'<rect x="{x - 3.5:.1f}" y="{ay(a) - 3.5:.1f}" width="7" height="7" fill="{GREEN}" stroke="#ffffff" stroke-width="1"/>'
            for _, x, _, _, _, a, _ in segments
        ],
        # Clean labels for extrema
        pill(326, 304, 198, 22, "总截面积暴涨 700 倍 (~2,800 cm²)", fill=GREEN_SOFT, stroke="#86efac", text_fill=GREEN, size=10.5),
        pill(310, 392, 212, 22, "流速急刹至 0.5 mm/s：从容换气 1–2s", fill=VENOUS_SOFT, stroke="#93c5fd", text_fill=VENOUS_DARK, size=10.5),
        txt(690, 362, "汇流提速 ~14 cm/s", size=10.5, weight="600", fill=VENOUS_DARK, anchor="end"),
        # X-axis segment labels along bottom of second card
        *[
            txt(x, 444, name, size=11, weight="700" if name in ("微动脉", "毛细血管") else "600", fill=INK, anchor="middle")
            for name, x, *_ in segments
        ],
        # Bottom myth-busting banner
        card(24, 460, 712, 42, rx=10, fill=TEAL_SOFT, stroke="#5eead4"),
        txt(
            380,
            486,
            "百年教材勘误（Poole 等 2021）：70 kg 成人毛细血管总长实为 9,000–19,000 km；“10 万公里”系 1922 年按 50 kg 纯肌肉外推误传",
            size=11.0,
            weight="600",
            fill=TEAL,
            anchor="middle",
        ),
    ]
    return figure(
        760,
        520,
        "人体血管树血压瀑布、总横截面积与血流速度定量关系图",
        "展示从主动脉、微动脉、毛细血管到腔静脉的血压级联下降（泊肃叶阻力定律）以及截面积扩大700倍使毛细血管流速降至0.5毫米每秒的连续性原理。",
        body,
    )


def build_open_vs_closed_and_insect_hack() -> str:
    """3. Three architectures solving Fick's diffusion barrier: Flatworm, Insect Open+Tracheae, Octopus 3-Heart Closed."""
    t_10um = _fick_diffusion_seconds(10e-6)
    t_1mm = _fick_diffusion_seconds(1e-3)
    t_1cm = _fick_diffusion_seconds(1e-2)
    assert 0.02 <= t_10um <= 0.03
    assert 240.0 <= t_1mm <= 260.0
    assert 24000.0 <= t_1cm <= 26000.0  # ~6.94 hours!

    body = [
        header(
            "无血管、开放洗浴与闭管三心：动物界破解“菲克扩散死锁”的三套方案",
            "按菲克定律 t ≈ L²/(2D) 距离翻 10 倍耗时翻 100 倍 → 对比涡虫压扁、昆虫气管外挂与章鱼闭管三心",
        ),
        # Column 1: Zero vessels (Jellyfish / Flatworm)
        card(24, 86, 224, 362, fill="#ffffff", stroke=BORDER),
        step_badge(42, 108, 1, TEAL),
        txt(62, 113, "无循环系统：压扁身体", size=13, weight="700", fill=TEAL),
        txt(36, 134, "代表：水母、海葵、涡虫", size=11, fill=MUTED),
        # Diagram of thin flatworm cross-section (<1 mm)
        card(40, 148, 192, 92, rx=10, fill=TEAL_SOFT, stroke="#99f6e4"),
        f'<ellipse cx="136" cy="194" rx="76" ry="16" fill="#ccfbf1" stroke="{TEAL}" stroke-width="2"/>',
        txt(136, 198, "扁平身体 + 分支消化腔", size=10.5, weight="700", fill=TEAL, anchor="middle"),
        txt(136, 168, "↓ 水中 O₂ 直接扩散 (<0.5 mm) ↓", size=10, fill=TEAL, anchor="middle"),
        txt(136, 228, "厚度 < 1 mm：细胞贴水自取", size=10, fill=BODY, anchor="middle"),
        # Quantitative Fick table
        txt(36, 264, "为什么变厚就必死？(t ≈ L²/2D)", size=11.5, weight="700", fill=INK),
        txt(36, 286, "• 10 μm 单细胞：~0.025 秒", size=11, fill=GREEN),
        txt(36, 308, "• 1 mm 扁虫极限：~4.2 分钟", size=11, fill=AMBER),
        txt(36, 330, "• 1 cm 厚肉块：~6.9 小时(窒息!)", size=11, weight="700", fill=RED),
        card(36, 350, 200, 82, rx=8, fill="#f8fafc", stroke=BORDER),
        txt(46, 372, "工程省钱法：", size=11, weight="700", fill=INK),
        txt(46, 392, "不造心脏与血管，代价是", size=10.8, fill=BODY),
        txt(46, 412, "永远长不大、没法变厚实。", size=10.8, fill=BODY),
        # Column 2: Open Circulatory + Insect Tracheal Bypass
        card(268, 86, 224, 362, fill="#ffffff", stroke=BORDER),
        step_badge(286, 108, 2, ORANGE),
        txt(306, 113, "开放式 + 昆虫气管外挂", size=13, weight="700", fill=ORANGE),
        txt(280, 134, "代表：蝗虫、蜜蜂、虾蟹、鲎", size=11, fill=MUTED),
        # Diagram of Dorsal ostia heart + hemocoel + silver air tubes
        card(284, 148, 192, 112, rx=10, fill=ORANGE_SOFT, stroke="#fed7aa"),
        f'<rect x="304" y="160" width="152" height="18" rx="8" fill="#fdba74" stroke="{ORANGE}" stroke-width="1.6"/>',
        txt(380, 173, "背血管管状心（带单向心门）", size=10, weight="700", fill="#7c2d12", anchor="middle"),
        txt(380, 198, "↙ 血腔低压漫灌（无色血淋巴）↘", size=10, fill=ORANGE, anchor="middle"),
        f'<rect x="300" y="212" width="160" height="36" rx="6" fill="#eff6ff" stroke="{VENOUS}" stroke-width="1.5" stroke-dasharray="4 2"/>',
        txt(380, 228, "独立外挂：气门 → 微气管网", size=10.5, weight="700", fill=VENOUS_DARK, anchor="middle"),
        txt(380, 243, "气态 O₂ 直插飞行肌线粒体！", size=10, fill=VENOUS_DARK, anchor="middle"),
        txt(280, 282, "为什么低压漫灌还能振翅 200Hz？", size=11.2, weight="700", fill=INK),
        txt(280, 304, "• 血液只送营养/激素，不送氧！", size=11, fill=BODY),
        txt(280, 326, "• 空气中 O₂ 扩散比水快 10⁴ 倍", size=11, weight="700", fill=VENOUS_DARK),
        card(280, 350, 200, 82, rx=8, fill="#f8fafc", stroke=BORDER),
        txt(290, 372, "体型枷锁：", size=11, weight="700", fill=INK),
        txt(290, 392, "气管扩散距离有限，现代氧气", size=10.8, fill=BODY),
        txt(290, 412, "21% 下造不出汽车大的甲虫。", size=10.8, fill=BODY),
        # Column 3: Closed Circulatory + Octopus 3 Hearts
        card(512, 86, 224, 362, fill="#ffffff", stroke=BORDER),
        step_badge(530, 108, 3, PURPLE),
        txt(550, 113, "闭管式：章鱼三心高压", size=13, weight="700", fill=PURPLE),
        txt(524, 134, "代表：蚯蚓、章鱼/乌贼、脊椎动物", size=11, fill=MUTED),
        # Diagram of Octopus 2 branchial hearts + 1 systemic heart
        card(528, 148, 192, 112, rx=10, fill=PURPLE_SOFT, stroke="#d8b4fe"),
        f'<circle cx="564" cy="182" r="18" fill="#dbeafe" stroke="{VENOUS}" stroke-width="1.8"/>',
        txt(564, 186, "左鳃心", size=9.8, weight="700", fill=VENOUS_DARK, anchor="middle"),
        f'<circle cx="684" cy="182" r="18" fill="#dbeafe" stroke="{VENOUS}" stroke-width="1.8"/>',
        txt(684, 186, "右鳃心", size=9.8, weight="700", fill=VENOUS_DARK, anchor="middle"),
        f'<rect x="594" y="166" width="60" height="34" rx="10" fill="#ede9fe" stroke="{PURPLE}" stroke-width="2.2"/>',
        txt(624, 187, "系统主心", size=10.5, weight="700", fill=PURPLE, anchor="middle"),
        txt(624, 218, "鳃心专克鳃部压降 → 主心 >75 mmHg", size=10, weight="600", fill=PURPLE, anchor="middle"),
        txt(624, 238, "全程密封管道 + 铜基蓝色血蓝蛋白", size=10, fill=BODY, anchor="middle"),
        txt(524, 282, "软体动物里的“高智商异类”：", size=11.2, weight="700", fill=INK),
        txt(524, 304, "• 双鳃心先给静脉血增压过鳃", size=11, fill=BODY),
        txt(524, 326, "• 主心高压精准喂饱巨型神经系统", size=11, fill=BODY),
        card(524, 350, 200, 82, rx=8, fill=RED_SOFT, stroke="#fca5a5"),
        txt(534, 372, "章鱼的软肋：", size=11, weight="700", fill=RED),
        txt(534, 392, "喷水疾游时外周阻力暴增，主心", size=10.8, fill=BODY),
        txt(534, 412, "会短暂罢工，所以平时爱爬行！", size=10.8, fill=BODY),
        # Footer comparison
        card(24, 460, 712, 42, rx=10, fill=SLATE_SOFT, stroke=BORDER),
        txt(
            380,
            486,
            "血量账本：开放式循环须灌满血腔，血淋巴占体重 20%–40%；闭管式循环密封高压快流，人血仅占体重 ~7%–8%（约 5 升）",
            size=11.1,
            weight="600",
            fill=INK,
            anchor="middle",
        ),
    ]
    return figure(
        760,
        520,
        "无血管扩散、昆虫开放式循环加气管系统与章鱼三心闭管式循环对比图",
        "对比扁形动物压扁身体突破菲克扩散限制、昆虫用气管网直供氧气配合低压血腔、以及章鱼演化出两颗鳃心加一颗主心的闭管式高压循环。",
        body,
    )


def build_vertebrate_heart_evolution_and_extremes() -> str:
    """4. Four-stage vertebrate heart evolution + Crocodilian Panizza shunt & Giraffe 250 mmHg anti-G suit."""
    # Hydrostatic head check for giraffe: delta_P = rho * g * h
    # rho = 1055 kg/m^3, g = 9.81 m/s^2, h = 2.0 m -> ~20,700 Pa = ~155 mmHg JUST to climb 2m!
    giraffe_head_mmhg = (1055.0 * 9.81 * 2.0) / 133.322
    assert 150.0 <= giraffe_head_mmhg <= 160.0

    body = [
        header(
            "脊椎动物心脏演化四部曲与极端改装：从鱼类单循环、鳄鱼潘氏孔到长颈鹿",
            "上排看心腔分隔演化（1房1室 → 2房1室 → 鳄鱼可切换4腔 → 恒温完全4腔）→ 下排看两大极端生存黑科技",
        ),
        # Top Row: 4 cards (width=166, gap=16 -> x=24, 206, 388, 570)
        # Stage 1: Fish
        card(24, 86, 166, 188, fill="#ffffff", stroke=BORDER),
        step_badge(40, 106, 1, VENOUS),
        txt(58, 111, "鱼类：1房1室", size=12.5, weight="700", fill=VENOUS_DARK),
        card(36, 124, 142, 62, rx=8, fill=VENOUS_SOFT, stroke="#93c5fd"),
        txt(107, 146, "心房 → 心室 → 鳃丝", size=10.8, weight="700", fill=VENOUS_DARK, anchor="middle"),
        txt(107, 168, "→ 全身毛细血管(串联)", size=10.5, fill=BODY, anchor="middle"),
        txt(36, 206, "• 单循环瓶颈：血液过鳃", size=10.6, fill=BODY),
        txt(36, 224, "  后血压掉大半，全身慢流", size=10.6, fill=BODY),
        txt(36, 244, "• 水浮力托身，耗氧较低", size=10.6, fill=MUTED),
        # Stage 2: Amphibian
        card(206, 86, 166, 188, fill="#ffffff", stroke=BORDER),
        step_badge(222, 106, 2, TEAL),
        txt(240, 111, "两栖类：2房1室", size=12.5, weight="700", fill=TEAL),
        card(218, 124, 142, 62, rx=8, fill=TEAL_SOFT, stroke="#5eead4"),
        txt(289, 146, "左房(肺) + 右房(体)", size=10.8, weight="700", fill=TEAL, anchor="middle"),
        txt(289, 168, "共入单心室（螺旋瓣导流）", size=10.5, fill=BODY, anchor="middle"),
        txt(218, 206, "• 肺皮双循环：湿润皮肤", size=10.6, fill=BODY),
        txt(218, 224, "  全天候补氧，水下可关肺", size=10.6, fill=BODY),
        txt(218, 244, "• 心室肌小梁减少清浊混血", size=10.6, fill=MUTED),
        # Stage 3: Crocodilian
        card(388, 86, 166, 188, fill="#ffffff", stroke=BORDER),
        step_badge(404, 106, 3, ORANGE),
        txt(422, 111, "鳄目：双模4腔", size=12.5, weight="700", fill=ORANGE),
        card(400, 124, 142, 62, rx=8, fill=ORANGE_SOFT, stroke="#fdba74"),
        txt(471, 146, "完全四腔 + 潘氏孔", size=10.8, weight="700", fill=ORANGE, anchor="middle"),
        txt(471, 168, "+ 肺动脉主动“齿轮瓣”", size=10.5, fill=BODY, anchor="middle"),
        txt(400, 206, "• 陆上呼吸 = 纯四腔不混血", size=10.6, fill=BODY),
        txt(400, 224, "• 潜水屏息 = 主动关肺分流", size=10.6, fill=BODY),
        txt(400, 244, "• 爬行类最精密流体阀门！", size=10.6, weight="600", fill=ORANGE),
        # Stage 4: Bird & Mammal
        card(570, 86, 166, 188, fill="#ffffff", stroke=BORDER),
        step_badge(586, 106, 4, RED),
        txt(604, 111, "鸟与哺乳：全隔4腔", size=12.5, weight="700", fill=RED),
        card(582, 124, 142, 62, rx=8, fill=RED_SOFT, stroke="#fca5a5"),
        txt(653, 146, "室间隔 100% 彻底焊死", size=10.8, weight="700", fill=RED, anchor="middle"),
        txt(653, 168, "低压护肺 ‖ 高压灌全身", size=10.5, fill=BODY, anchor="middle"),
        txt(582, 206, "• 零混血高纯氧供应全身", size=10.6, fill=BODY),
        txt(582, 224, "• 支撑恒温 37–41°C 与飞翔", size=10.6, fill=BODY),
        txt(582, 244, "• 鸟类与哺乳类独立趋同演化", size=10.6, fill=MUTED),
        # Bottom Left Card: Crocodile Panizza Shunt
        card(24, 288, 348, 160, fill=ORANGE_SOFT, stroke="#fdba74"),
        txt(40, 312, "深潜黑科技 ①：鳄鱼“潘氏孔 + 齿轮瓣”双模切换", size=12.5, weight="700", fill="#9a3412"),
        txt(40, 336, "• 潜伏水底屏息 1 小时，肺里氧气耗尽，继续泵肺纯属空转；", size=11, fill=INK),
        txt(40, 358, "• 肺动脉口特化的结缔组织“齿轮瓣”受迷走神经控制主动咬合；", size=11, fill=INK),
        txt(40, 380, "• 右心室压力升高，缺氧血经左右主动脉根部的【潘氏孔】改道", size=11, fill=INK),
        txt(40, 400, "  注入体循环（右向左分流），优先保住大脑与心脏供血；", size=11, fill=INK),
        pill(40, 414, 314, 22, "副产物：高 CO₂ 血液直送胃部，造出溶化兽骨的超强胃酸！", fill="#ffedd5", stroke=ORANGE, text_fill="#9a3412", size=10.3),
        # Bottom Right Card: Giraffe 2m Hydrostatic Tower
        card(388, 288, 348, 160, fill=RED_SOFT, stroke="#fca5a5"),
        txt(404, 312, "高空黑科技 ②：长颈鹿把血顶上 2 米高空的四重防护", size=12.5, weight="700", fill=RED),
        txt(404, 336, "• 光克服 2 m 血柱静水压 (ρgh) 就得先损耗 ~155 mmHg！", size=11, weight="600", fill=INK),
        txt(404, 358, "• ① 11 kg 超级心脏：左室壁厚达 7.5 cm，动脉压 ~250 mmHg；", size=11, fill=INK),
        txt(404, 380, "• ② 低头喝水防脑溢血：颈静脉 ~7 道单向瓣 + 颅底奇网缓冲；", size=11, fill=INK),
        txt(404, 400, "• ③ 猛抬头防晕厥：奇网血管收缩补血，不患体位性低血压；", size=11, fill=INK),
        pill(404, 414, 314, 22, "④ 小腿紧绷厚皮筋膜 = 战斗机飞行员“天然抗荷服”防腿肿！", fill="#fee2e2", stroke=RED, text_fill=RED, size=10.3),
        # Footer
        card(24, 460, 712, 42, rx=10, fill=SLATE_SOFT, stroke=BORDER),
        txt(
            380,
            486,
            "演化视角：没有“绝对完美”的心脏——两栖与鳄鱼的受控分流是外温动物省能杰作，恒温四腔则是高能耗发动机",
            size=11.1,
            weight="600",
            fill=INK,
            anchor="middle",
        ),
    ]
    return figure(
        760,
        520,
        "脊椎动物心脏演化四阶段与鳄鱼潘氏孔分流、长颈鹿高压抗荷机制对比图",
        "展示鱼类1房1室、两栖类2房1室、鳄目双模4腔与恒温动物全隔4腔的演化逻辑，详解鳄鱼水下潘氏孔右向左分流和长颈鹿250毫米汞柱血压适应。",
        body,
    )


def build_rainbow_blood_chemistry_spectrum() -> str:
    """5. Five-color spectrum of animal blood chemistry: Red, Blue, Green, Violet-Pink, Crystal Clear."""
    # Physical O2 solubility in plasma at 37 C (~3 mL/L) vs human whole blood (~200 mL/L) -> ~67x boost!
    o2_boost = 200.0 / 3.0
    assert 65.0 <= o2_boost <= 70.0

    cols = [
        {
            "x": 24,
            "title": "鲜红 · 铁血",
            "pigment": "血红蛋白",
            "eng": "Hemoglobin",
            "bg": RED_SOFT,
            "stroke": "#fca5a5",
            "liquid": RED_BRIGHT,
            "accent": RED,
            "metal": "血红素卟啉 Fe²⁺",
            "state": "氧合鲜红 / 脱氧暗红",
            "pack": "红细胞封装(浓67倍)",
            "who1": "人类与几乎所有",
            "who2": "脊椎动物、蚯蚓",
            "note": "温血高代谢首选",
        },
        {
            "x": 169,
            "title": "皇家蓝 · 铜血",
            "pigment": "血蓝蛋白",
            "eng": "Hemocyanin",
            "bg": VENOUS_SOFT,
            "stroke": "#93c5fd",
            "liquid": "#2563eb",
            "accent": VENOUS_DARK,
            "metal": "双铜中心 Cu⁺→Cu²⁺",
            "state": "氧合天蓝 / 脱氧无色",
            "pack": "巨型蛋白溶在血浆",
            "who1": "章鱼、乌贼、龙虾",
            "who2": "蜘蛛、中华鲎(LAL)",
            "note": "深海冰冷低氧更强",
        },
        {
            "x": 314,
            "title": "翡翠绿 · 绿血",
            "pigment": "血绿蛋白/胆绿素",
            "eng": "Chlorocruorin",
            "bg": GREEN_SOFT,
            "stroke": "#86efac",
            "liquid": "#16a34a",
            "accent": GREEN,
            "metal": "改构铁卟啉 / 胆绿素",
            "state": "稀绿浓红 / 翠绿血浆",
            "pack": "海虫血浆 / 蜥蜴血浆",
            "who1": "海洋羽鳃蠕虫 +",
            "who2": "新几内亚绿血石龙子",
            "note": "黄疸毒素超标40倍!",
        },
        {
            "x": 459,
            "title": "紫粉 · 双铁血",
            "pigment": "血紫蛋白",
            "eng": "Hemerythrin",
            "bg": VIOLET_SOFT,
            "stroke": "#d8b4fe",
            "liquid": VIOLET,
            "accent": "#6b21a8",
            "metal": "非血红素双铁中心",
            "state": "氧合紫粉 / 脱氧无色",
            "pack": "血细胞内(效率~1/4)",
            "who1": "星虫、鳃曳动物",
            "who2": "海豆芽(腕足动物)",
            "note": "虽叫heme却无血红素",
        },
        {
            "x": 604,
            "title": "冰晶透明 · 白血",
            "pigment": "零血红蛋白",
            "eng": "Pigment-Free",
            "bg": ICE_SOFT,
            "stroke": "#7dd3fc",
            "liquid": "#e0f2fe",
            "accent": ICE_DARK,
            "metal": "无金属载氧蛋白！",
            "state": "全程晶莹透明无色",
            "pack": "纯靠冰水血浆物理溶氧",
            "who1": "南极鳄冰鱼（唯一",
            "who2": "成年白血脊椎动物）",
            "note": "4倍血量+5倍心输出",
        },
    ]

    body = [
        header(
            "血液为什么不全是红色？地球生命“五彩血液”的元素周期表密码",
            "从铁红、铜蓝、海洋蠕虫与绿血蜥蜴、双铁紫罗兰到南极冰鱼的“零红细胞透明血”",
        ),
    ]

    for c in cols:
        x = c["x"]
        cx = x + 66
        body.extend(
            [
                card(x, 86, 132, 362, fill=c["bg"], stroke=c["stroke"]),
                txt(cx, 110, c["title"], size=12.5, weight="700", fill=c["accent"], anchor="middle"),
                txt(cx, 129, c["pigment"], size=11.5, weight="700", fill=INK, anchor="middle"),
                txt(cx, 145, c["eng"], size=9.8, fill=MUTED, anchor="middle"),
                # Test vial illustration (x+44..x+88, y=156..234)
                f'<rect x="{cx - 20}" y="156" width="40" height="76" rx="18" fill="#ffffff" stroke="{c["accent"]}" stroke-width="1.8"/>',
                f'<rect x="{cx - 16}" y="182" width="32" height="46" rx="14" fill="{c["liquid"]}" stroke="{c["stroke"]}" stroke-width="1"/>',
                f'<line x1="{cx - 24}" y1="156" x2="{cx + 24}" y2="156" stroke="{c["accent"]}" stroke-width="2.4"/>',
                # Specs below vial
                txt(cx, 256, c["metal"], size=10.4, weight="700", fill=c["accent"], anchor="middle"),
                txt(cx, 278, c["state"], size=10.2, fill=INK, anchor="middle"),
                txt(cx, 300, c["pack"], size=10.0, fill=BODY, anchor="middle"),
                f'<line x1="{x + 12}" y1="316" x2="{x + 120}" y2="316" stroke="{c["stroke"]}" stroke-width="1"/>',
                txt(cx, 338, "代表生物", size=10.2, weight="700", fill=MUTED, anchor="middle"),
                txt(cx, 358, c["who1"], size=10.4, weight="600", fill=INK, anchor="middle"),
                txt(cx, 376, c["who2"], size=10.4, weight="600", fill=INK, anchor="middle"),
                pill(x + 8, 402, 116, 24, c["note"], fill="#ffffff", stroke=c["stroke"], text_fill=c["accent"], size=9.8),
            ]
        )

    body.extend(
        [
            card(24, 460, 712, 42, rx=10, fill="#ffffff", stroke=BORDER),
            txt(
                380,
                486,
                "化学底层原因：37°C 纯血浆每升仅溶氧 ~3 mL；过渡金属 (Fe/Cu) 利用可变 d 轨道可逆抓放 O₂，把人类全血携氧拉高到 ~200 mL/L！",
                size=10.9,
                weight="600",
                fill=INK,
                anchor="middle",
            ),
        ]
    )
    return figure(
        760,
        520,
        "地球动物五种血液颜色与呼吸色素金属配位化学图谱",
        "对比血红蛋白（铁红）、血蓝蛋白（铜蓝）、血绿蛋白与绿血石龙子胆绿素（绿）、血紫蛋白（双铁紫粉）以及南极冰鱼无血红蛋白透明血。",
        body,
    )


@register("circulatory-systems", "血液循环系统：人体双循环流体力学与动物界多样循环工程", "生理与动物学")
def build_all() -> list[str]:
    return [
        write_svg(SUBDIR, "human-double-circulation-anim.svg", build_human_double_circulation_anim()),
        write_svg(SUBDIR, "hemodynamics-pressure-velocity-cascade.svg", build_hemodynamics_pressure_velocity_cascade()),
        write_svg(SUBDIR, "open-vs-closed-and-insect-hack.svg", build_open_vs_closed_and_insect_hack()),
        write_svg(SUBDIR, "vertebrate-heart-evolution-and-extremes.svg", build_vertebrate_heart_evolution_and_extremes()),
        write_svg(SUBDIR, "rainbow-blood-chemistry-spectrum.svg", build_rainbow_blood_chemistry_spectrum()),
    ]
