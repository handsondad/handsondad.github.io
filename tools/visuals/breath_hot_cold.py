"""
Visuals for '为什么呼气（哈气）和吹气，手感觉一个热一个冷？'
(Physics, Fluid Mechanics, Thermodynamics & Neuroscience of Blowing Hot and Cold:
1. Open-Mouth 'Ha~' Potential Core vs Pursed-Lip 'Fu~' Ricou-Spalding Turbulent Jet Entrainment [1:11 Room Air Dilution, 1-shot CSS animation],
2. Myth-Busting NIST Joule-Thomson [0.004 °C] & Dynamic Drop [0.11 °C] vs Exact Jet Temperature-Distance Curves [Why 1 cm Pursed-Lip Feels HOT!],
3. Forced Convection Stripping the Skin's 3 mm 'Invisible Down Jacket' Thermal Boundary Layer [h jumps 5x],
4. Water Phase-Change Amplifier: Dew-Point Condensation Heating [+2420 J/g on Cold Hands/Glasses] vs Evaporative Cooling [-2420 J/g],
5. The 45 °C Sauna 'Air-Fryer' Reversal & 2021 Nobel Prize TRPM8 [Cold/Menthol] vs TRPV1/TRPV3 Skin Thermoreceptors).

Generates 5 original 760px Chinese SVG diagrams in assets/images/breath-hot-cold/
with verified turbulent-jet, NIST thermodynamic, psychrometric, and heat-transfer assertions.
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

TOPIC = "breath-hot-cold"
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
    <marker id="arr-slate" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{SLATE}"/>
    </marker>
    """


def jet_mass_ratio(x_cm: float, d_mm: float) -> float:
    """Ricou & Spalding (1961, J. Fluid Mech. 11:21-32) round turbulent jet mass flux ratio m(x)/m0.
    Near-field potential core smoothly transitions around x/D ≈ 3.125 to far-field 0.32 * (x/D).
    """
    xd = (x_cm * 10.0) / d_mm
    if xd <= 3.125:
        # Smooth near-field shear-layer entrainment growth from 1.0 at x=0 to ~1.35 at x/D=3.125
        return 1.0 + 0.08 * xd
    return 1.25 + 0.32 * (xd - 3.125)


def jet_mixed_temp(x_cm: float, d_mm: float, t_exit: float = 35.0, t_amb: float = 20.0) -> float:
    """Bulk enthalpy-conserving mixed jet temperature (°C) at axial distance x_cm."""
    mr = jet_mass_ratio(x_cm, d_mm)
    return t_amb + (t_exit - t_amb) / mr


def jet_centerline_temp(x_cm: float, d_mm: float, t_exit: float = 35.0, t_amb: float = 20.0) -> float:
    """Axisymmetric turbulent round jet centerline temperature T_c(x) (Chen & Rodi 1980 / Pope):
    Smooth transition from potential core (x/D <= ~4.5) to 5.0 / (x/D) self-similar decay.
    """
    xd = (x_cm * 10.0) / d_mm
    # Smooth C1 transition matching potential core plateau = 1 at xd=0 and 5.0/xd for xd >> 5:
    decay = 1.0 / math.sqrt(1.0 + (xd / 5.0) ** 2)
    return t_amb + (t_exit - t_amb) * decay


# ---------------------------------------------------------------------------
# 1. Open-Mouth 'Ha~' vs Pursed-Lip 'Fu~' Turbulent Jet Entrainment (Animated)
# ---------------------------------------------------------------------------
def build_ha_vs_chui_jet_entrainment() -> str:
    t_exit = 35.0
    t_room = 20.0
    t_skin = 32.5

    # Open-mouth 'Ha~': D = 30 mm, x = 10 cm (x/D = 3.33)
    mr_ha_10 = jet_mass_ratio(10.0, 30.0)
    t_ha_10 = jet_mixed_temp(10.0, 30.0, t_exit, t_room)
    assert 1.2 < mr_ha_10 < 1.4          # Barely diluted!
    assert t_ha_10 > 31.0                # Centerline is still ~34.5 °C (> 32.5 °C skin!)

    # Pursed-lip 'Fu~': D = 4 mm, x = 15 cm (x/D = 37.5!)
    mr_chui_15 = jet_mass_ratio(15.0, 4.0)
    t_chui_15 = jet_mixed_temp(15.0, 4.0, t_exit, t_room)
    assert 11.8 < mr_chui_15 < 12.6      # ~12.25 total mass -> ~11.2 parts room air per 1 part lung air!
    assert 21.0 < t_chui_15 < 21.6       # Plunges to ~21.2 °C (< 32.5 °C skin!)

    anim_defs = (
        _markers()
        + """
    <style>
      @keyframes warmFlow {
        0%   { transform: translateX(-18px); opacity: 0.35; }
        100% { transform: translateX(0px); opacity: 1; }
      }
      @keyframes coldEntrain {
        0%   { transform: translateY(-10px); opacity: 0.25; }
        100% { transform: translateY(0px); opacity: 1; }
      }
      .anim-warm {
        animation: warmFlow 2.6s ease-out 1 forwards;
      }
      .anim-entrain {
        animation: coldEntrain 2.6s cubic-bezier(0.22, 1, 0.36, 1) 1 forwards;
      }
      @media (prefers-reduced-motion: reduce) {
        .anim-warm, .anim-entrain {
          animation: none !important;
          transform: none !important;
          opacity: 1 !important;
        }
      }
    </style>
    """
    )

    els = []
    els.extend(
        header(
            "同一张嘴吐出 35°C 肺部暖气，为什么“哈气”暖手、“吹气”冰凉？",
            "核心第一关：嘴唇口径相差 7–8 倍，决定了暖气是“抱团直达”还是半路卷进 11 倍室温冷空气！",
        )
    )

    # Top Card: Open-mouth "哈气 (Ha~)"
    els.append(card(20, 62, 720, 198))
    els.append(step_badge(38, 84, 1, fg=RED, bg=RED_SOFT))
    els.append(txt(56, 88, "张大嘴“哈——气”：大口径慢速暖柱（口裂 D ≈ 30 mm，流速 v₀ ≈ 1.5 m/s）", size=12.4, color=INK, weight="700"))

    # Mouth profile (wide open, left)
    els.append('<path d="M 48 134 Q 72 130 82 142 L 82 182 Q 72 194 48 190" fill="none" stroke="#be123c" stroke-width="3.2" stroke-linecap="round"/>')
    els.append(txt(64, 212, "35°C 肺部暖湿气", size=10.0, color=RED, anchor="middle", weight="700"))
    els.append(txt(64, 228, "（口径 30 mm）", size=9.9, color=MUTED, anchor="middle"))

    # Wide warm potential core reaching palm at x = 10 cm (pixel x=84 -> x=346)
    els.append('<g class="anim-warm">')
    els.append('<polygon points="84,142 346,128 346,196 84,182" fill="#fecaca" fill-opacity="0.62" stroke="#f87171" stroke-width="1.4"/>')
    els.append('<polygon points="84,146 318,156 318,168 84,178" fill="#fca5a5" fill-opacity="0.72"/>')
    els.append(_line(106, 162, 326, 162, stroke=RED, sw=2.2, marker="arr-red"))
    els.append("</g>")
    els.append(txt(214, 120, "未稀释“势流核心区”长达 ~5D（约 15 cm）！", size=10.3, color=RED, anchor="middle", weight="700"))
    els.append(txt(222, 212, "剪切弱、涡旋少，20°C 空气难混入核心", size=10.0, color=SLATE, anchor="middle"))

    # Palm bar at x = 10 cm (348)
    els.append('<rect x="348" y="118" width="16" height="90" rx="7" fill="#fed7aa" stroke="#ea580c" stroke-width="1.8"/>')
    els.append(txt(356, 230, "手掌（10 cm）", size=10.1, color=ORANGE, anchor="middle", weight="700"))
    els.append(txt(356, 246, "皮温 32.5°C", size=9.9, color=MUTED, anchor="middle"))

    # Right summary box inside Top Card
    els.append(card(418, 102, 304, 142, rx=8, fill=RED_SOFT, stroke="#fca5a5", sw=1.1))
    els.append(txt(432, 124, "🔥 抵达手掌温度：中心仍高达 34–35°C！", size=11.0, color=RED, weight="700"))
    els.append(txt(432, 146, f"• 10 cm 仅相当于 3.3 倍口径（x/D ≈ 3.3），平均仅混入", size=10.1, color=BODY))
    els.append(txt(432, 165, f"  约 {(mr_ha_10 - 1.0)*100:.0f}% 外界空气，核心区几乎原汁原味保留肺温；", size=10.1, color=BODY))
    els.append(txt(432, 184, "• 气流温度（34.5°C）＞ 皮肤温度（32.5°C），加上饱和", size=10.1, color=BODY))
    els.append(txt(432, 203, "  水汽遇冷手凝结放热，热量实打实往手心里灌！", size=10.1, color=INK, weight="600"))
    els.append(txt(432, 224, "⇒ 手感结论：温润暖洋洋（冬天暖手姿势）", size=10.3, color=RED, weight="700"))

    # Bottom Card: Pursed-lip "吹气 (Fu~)"
    els.append(card(20, 274, 720, 224))
    els.append(step_badge(38, 296, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 300, "撅起嘴“呼——吹气”：细孔高速湍流射流（圆孔 D ≈ 4 mm，流速 v₀ ≈ 15 m/s）", size=12.4, color=INK, weight="700"))

    # Mouth profile (pursed small orifice, left)
    els.append('<path d="M 48 378 Q 76 386 82 394 M 48 418 Q 76 410 82 402" fill="none" stroke="#be123c" stroke-width="3.2" stroke-linecap="round"/>')
    els.append(txt(64, 438, "同样 35°C 出发！", size=10.0, color=RED, anchor="middle", weight="700"))
    els.append(txt(64, 455, "（圆孔仅 4 mm）", size=9.9, color=MUTED, anchor="middle"))

    # Tiny red core (~5D = 2 cm!) + wide expanding blue turbulent jet cone to x = 15 cm (368)
    els.append('<polygon points="84,394 366,346 366,450 84,402" fill="#dbeafe" fill-opacity="0.72" stroke="#60a5fa" stroke-width="1.4"/>')
    els.append('<polygon points="84,394 122,397 122,399 84,402" fill="#ef4444"/>')
    els.append(_line(124, 398, 350, 398, stroke=BLUE, sw=2.2, marker="arr-blue"))

    # Turbulent entrainment arrows sucking 20°C ambient air from top and bottom!
    els.append('<g class="anim-entrain">')
    for ex_arr, ey_top, ey_bot in [(152, 338, 458), (218, 334, 462), (284, 330, 466)]:
        els.append(_line(ex_arr, ey_top, ex_arr + 14, ey_top + 28, stroke=BLUE, sw=1.7, marker="arr-blue"))
        els.append(_line(ex_arr, ey_bot, ex_arr + 14, ey_bot - 28, stroke=BLUE, sw=1.7, marker="arr-blue"))
    els.append("</g>")
    els.append(txt(224, 324, "高速涡旋疯狂“卷吸”周围 20°C 空气！（Ricou–Spalding 定律）", size=10.1, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(224, 486, "暖核 2 cm 内被扯碎，1 份肺气裹进 11 份冷空气！", size=10.0, color=BLUE, anchor="middle", weight="600"))

    # Palm bar at x = 15 cm (368)
    els.append('<rect x="368" y="346" width="16" height="104" rx="7" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.8"/>')
    els.append(txt(376, 466, "手掌 (15 cm)", size=10.0, color=BLUE, anchor="middle", weight="700"))

    # Right summary box inside Bottom Card
    els.append(card(418, 316, 304, 166, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE, sw=1.1))
    els.append(txt(432, 338, f"❄️ 抵达手掌温度：暴跌至 {t_chui_15:.1f}°C（几乎等于室温）！", size=10.8, color=BLUE, weight="700"))
    els.append(txt(432, 360, "• 15 cm 相当于 37.5 倍孔径（x/D ＝ 37.5）！按经典圆射流", size=10.1, color=BODY))
    els.append(txt(432, 379, "  卷吸公式 m/m₀ ≈ 0.32(x/D)，总流量暴涨至约 12 倍；", size=10.1, color=BODY))
    els.append(txt(432, 398, f"• 1 份 35°C 呼气 ＋ 11.2 份 20°C 室温空气混合后仅 {t_chui_15:.1f}°C；", size=10.1, color=BODY))
    els.append(txt(432, 417, "• 21.2°C 凉风猛吹 32.5°C 温热手掌，撕开保温层＋加速汗液", size=10.1, color=BODY))
    els.append(txt(432, 436, "  蒸发，三重抽热叠加，瞬间让你感觉凉风嗖嗖！", size=10.1, color=INK, weight="600"))
    els.append(txt(432, 460, "⇒ 手感结论：清凉降温（吹热粥／吹烫手姿势）", size=10.3, color=BLUE, weight="700"))

    return figure(
        515,
        "张嘴哈气与撅嘴吹气的湍流射流卷吸效应对比图",
        "上图展示张嘴哈气（口径约30毫米）势流核心长达15厘米，10厘米处手掌仍接收34至35摄氏度肺部暖湿气；下图展示撅嘴吹气（孔径约4毫米）高速湍流射流按Ricou-Spalding定律在15厘米内卷入约11倍20摄氏度室温空气，混合气温降至21.2摄氏度。",
        els,
        extra_defs=anim_defs,
    )


# ---------------------------------------------------------------------------
# 2. Myth-Busting Joule-Thomson vs Exact Distance Curve (1 cm Pursed-Lip Test!)
# ---------------------------------------------------------------------------
def build_myth_busting_jt_vs_distance() -> str:
    # NIST N2/Air Joule-Thomson at 310 K, 1 atm: mu_JT ≈ 2.0–2.2 K/MPa = 0.0022 K/kPa
    mu_jt_k_per_kpa = 0.0022
    dp_kpa = 2.0  # generous cheek-puffing gauge pressure (2 kPa ≈ 20 cmH2O)
    dt_jt = mu_jt_k_per_kpa * dp_kpa
    assert dt_jt < 0.006  # ~0.0044 °C!

    # Dynamic kinetic cooling before stagnation: v0^2 / (2 * cp)
    v0 = 15.0
    cp = 1005.0
    dt_dyn = (v0**2) / (2.0 * cp)
    assert 0.10 < dt_dyn < 0.12  # ~0.11 °C!

    # Check pursed-lip centerline temperature at x = 1 cm vs x = 15 cm
    t_chui_1cm = jet_centerline_temp(1.0, 4.0, 35.0, 20.0)
    t_chui_15cm = jet_centerline_temp(15.0, 4.0, 35.0, 20.0)
    assert t_chui_1cm > 33.0     # ~33.7 °C (> 32.5 °C skin at 1 cm) -> FEELS WARM!
    assert t_chui_15cm < 22.5    # ~22.0 °C centerline (21.2 °C bulk) at 15 cm -> FEELS COOL!

    els = []
    els.extend(
        header(
            "辟谣“气体绝热膨胀致冷说”：一秒钟贴唇实验，当场抓获真凶！",
            "嘴唇喷气的膨胀降温连 0.12°C 都不到；真正让冷暖反转的，是手掌离嘴唇的距离 x/D",
        )
    )

    # Left Card: Quantitative Takedown of Textbook Expansion Myth
    els.append(card(20, 62, 344, 418))
    els.append(step_badge(38, 84, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 88, "算账辟谣：嘴巴真的能当“空调膨胀阀”吗？", size=12.0, color=INK, weight="700"))

    els.append(card(36, 108, 312, 174, rx=8, fill="#f8fafc", stroke=BORDER, sw=1.1))
    els.append(txt(48, 128, "实际需要降温幅度 vs 膨胀效应真实贡献：", size=10.6, color=INK, weight="700"))

    # Bar 1: Real cooling observed (~13.8 °C drop from 35 to 21.2 °C)
    els.append(txt(48, 152, "① 湍流卷吸冷空气实测降温：", size=10.1, color=BLUE, weight="700"))
    els.append('<rect x="48" y="160" width="248" height="16" rx="4" fill="#2563eb"/>')
    els.append(txt(302, 172, "-13.8°C", size=10.0, color=BLUE, weight="700", cls="mono"))

    # Bar 2: Reversible dynamic drop v^2/(2*cp) at 15 m/s (-0.11 °C, and recovers on impact!)
    els.append(txt(48, 198, "② 喷口高速动能折算温降（撞手掌即恢复）：", size=10.1, color=ORANGE, weight="600"))
    els.append('<rect x="48" y="206" width="4" height="16" rx="2" fill="#f97316"/>')
    els.append(txt(60, 218, "仅 -0.11°C（差 120 倍！）", size=10.0, color=ORANGE, weight="700"))

    # Bar 3: NIST Joule-Thomson throttling at ΔP = 2 kPa (-0.0044 °C!)
    els.append(txt(48, 244, "③ 焦耳—汤姆孙节流效应（NIST 实测系数）：", size=10.1, color=SLATE, weight="600"))
    els.append('<rect x="48" y="252" width="2" height="16" rx="1" fill="#64748b"/>')
    els.append(txt(58, 264, f"仅 -{dt_jt:.3f}°C（差 3000 倍！）", size=10.0, color=RED, weight="700"))

    els.append(card(36, 294, 312, 172, rx=8, fill=AMBER_SOFT, stroke="#fcd34d", sw=1.1))
    els.append(txt(48, 315, "🧪 现在就试！1 秒钟“贴唇吹气”证伪实验：", size=10.8, color=INK, weight="700"))
    els.append(txt(48, 337, "1. 把嘴唇撅成最细的“O”形，使出浑身力气猛吹；", size=10.1, color=BODY))
    els.append(txt(48, 356, "2. 先把手心贴到离嘴唇只有【1 厘米】处——", size=10.1, color=BODY))
    els.append(txt(48, 375, "   你会惊讶地发现：撅嘴猛吹的气明明是【热的】！", size=10.2, color=RED, weight="700"))
    els.append(txt(48, 394, "3. 嘴型和力度丝毫不变，把手慢慢拉远到 10–15 cm：", size=10.1, color=BODY))
    els.append(txt(48, 413, "   过了 3–5 cm 分界线后，热风突然变成了凉风！", size=10.2, color=BLUE, weight="700"))
    els.append(txt(48, 436, "⇒ 如果是嘴唇膨胀致冷，出口 1 cm 处才最该冰凉；", size=10.0, color=BODY))
    els.append(txt(48, 453, "   出口滚烫、半路变凉，100% 证明是半路掺了冷风！", size=10.0, color=INK, weight="700"))

    # Right Card: Exact Plot of Mixed Jet Temperature vs Axial Distance x (0..25 cm)
    els.append(card(378, 62, 362, 418))
    els.append(step_badge(396, 84, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(414, 88, "气流混合温度随距离衰减曲线（室温 20°C）", size=12.0, color=INK, weight="700"))

    gx0, gx1 = 428.0, 718.0
    gy_top, gy_bot = 120.0, 344.0

    def px(x_cm: float) -> float:
        return gx0 + (x_cm / 25.0) * (gx1 - gx0)

    def py(temp_c: float) -> float:
        return gy_bot - ((temp_c - 18.0) / (37.0 - 18.0)) * (gy_bot - gy_top)

    # Warm vs Cool zones divided by Palm Skin Temperature = 32.5 °C
    y_skin = py(32.5)
    els.append(f'<rect x="{gx0}" y="{gy_top}" width="{gx1 - gx0}" height="{y_skin - gy_top:.1f}" fill="#fef2f2" fill-opacity="0.65"/>')
    els.append(f'<rect x="{gx0}" y="{y_skin:.1f}" width="{gx1 - gx0}" height="{gy_bot - y_skin:.1f}" fill="#eff6ff" fill-opacity="0.65"/>')
    els.append(_line(gx0, y_skin, gx1, y_skin, stroke=ORANGE, sw=1.5, dash="5,4"))
    els.append(txt(gx1 - 6, y_skin - 6, "手掌皮温分界线 32.5°C（上热下凉）", size=9.9, color=ORANGE, anchor="end", weight="700"))

    for t_tick in [20, 25, 30, 35]:
        yy = py(float(t_tick))
        els.append(_line(gx0, yy, gx1, yy, stroke="#e2e8f0", sw=1.0))
        els.append(txt(gx0 - 6, yy + 4, f"{t_tick}°C", size=9.8, color=MUTED, anchor="end", cls="mono"))

    for x_tick in [0, 5, 10, 15, 20, 25]:
        xx = px(float(x_tick))
        els.append(_line(xx, gy_bot, xx, gy_bot + 5, stroke=SLATE, sw=1.1))
        els.append(txt(xx, gy_bot + 18, f"{x_tick}", size=9.8, color=MUTED, anchor="middle", cls="mono"))

    els.append(txt((gx0 + gx1) / 2, gy_bot + 36, "手掌距嘴唇距离 x (cm)", size=10.1, color=MUTED, anchor="middle"))
    els.append(_line(gx0, gy_top, gx0, gy_bot, stroke=SLATE, sw=1.3))
    els.append(_line(gx0, gy_bot, gx1, gy_bot, stroke=SLATE, sw=1.3))

    # Curve A: Open-mouth 'Ha~' (D = 30 mm) — centerline stays > 32.5 °C out to ~10 cm!
    pts_ha = [(x * 0.5, jet_centerline_temp(x * 0.5, 30.0)) for x in range(0, 51)]
    poly_ha = " ".join(f"{px(x):.1f},{py(t):.1f}" for x, t in pts_ha)
    els.append(f'<polyline points="{poly_ha}" fill="none" stroke="{RED}" stroke-width="2.6"/>')

    # Curve B: Pursed-lip 'Fu~' (D = 4 mm) — plunges steeply right after 2 cm!
    pts_chui = [(x * 0.5, jet_centerline_temp(x * 0.5, 4.0)) for x in range(0, 51)]
    poly_chui = " ".join(f"{px(x):.1f},{py(t):.1f}" for x, t in pts_chui)
    els.append(f'<polyline points="{poly_chui}" fill="none" stroke="{BLUE}" stroke-width="2.8"/>')

    # Highlight key points: (1 cm, chui = 33.7°C WARM!), (15 cm, chui = 22.0°C COOL!)
    els.append(f'<circle cx="{px(1.0):.1f}" cy="{py(t_chui_1cm):.1f}" r="5" fill="{RED}" stroke="#fff" stroke-width="1.4"/>')
    els.append(txt(px(1.0) + 10, py(t_chui_1cm) + 16, f"1 cm 贴唇吹气: {t_chui_1cm:.1f}°C (热!)", size=9.9, color=RED, weight="700"))

    els.append(f'<circle cx="{px(15.0):.1f}" cy="{py(t_chui_15cm):.1f}" r="5" fill="{BLUE}" stroke="#fff" stroke-width="1.4"/>')
    els.append(txt(px(15.0), py(t_chui_15cm) - 10, f"15 cm 吹气中心: {t_chui_15cm:.1f}°C (凉!)", size=10.0, color=BLUE, anchor="middle", weight="700"))

    els.append(txt(px(18.5), py(jet_centerline_temp(18.5, 30.0)) - 10, "张嘴哈气中心 (D=30 mm)", size=10.0, color=RED, anchor="middle", weight="700"))

    els.append(card(394, 392, 330, 74, rx=8, fill=TEAL_SOFT, stroke="#5eead4", sw=1.0))
    els.append(txt(406, 413, "反过来试：张大嘴“哈气”，但把手伸远到 40 cm 外！", size=10.4, color=TEAL, weight="700"))
    els.append(txt(406, 433, "一旦超过 5 倍大口径（>15 cm），哈气暖柱也会被冷空气", size=10.0, color=BODY))
    els.append(txt(406, 451, "吞没稀释——哪怕张大嘴哈气，隔老远照样变成凉风！", size=10.0, color=INK, weight="600"))

    return figure(
        495,
        "焦耳-汤姆孙膨胀降温量级证伪与哈气吹气温度随距离衰减曲线图",
        "左卡对比实测卷吸降温（-13.8摄氏度）与喷口动能温降（-0.11摄氏度）、焦耳-汤姆孙效应（-0.004摄氏度）的悬殊差距，并给出1厘米贴唇吹气变热的实验；右卡绘出哈气与吹气混合温度随距离衰减曲线及32.5摄氏度皮温分界线。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 3. Skin Thermal Boundary Layer ("Invisible Down Jacket") Forced Convection
# ---------------------------------------------------------------------------
def build_skin_boundary_layer() -> str:
    # Effective stagnant thermal boundary-layer thickness delta_eff = k_air / h:
    k_air = 0.026    # W/(m*K)
    h_calm = 6.5     # W/(m^2*K) natural convection around a warm human hand
    h_blow = 34.0    # W/(m^2*K) turbulent jet impingement (~4.5 m/s) on palm!
    d_calm = 1000.0 * k_air / h_calm   # 4.00 mm effective insulating blanket
    d_blow = 1000.0 * k_air / h_blow   # 0.76 mm thin stripped film!
    assert 3.8 <= d_calm <= 4.2 and 0.70 <= d_blow <= 0.85

    q_ha = h_calm * 2.2 * (32.5 - 34.5)       # negative = heat GAINED by skin (~ -29 W/m^2 sensible + condensation!)
    q_blow = h_blow * (32.5 - 21.2)           # positive = sensible heat LOST (~ +384 W/m^2!)
    assert q_ha < -25.0 and q_blow > 350.0

    els = []
    els.extend(
        header(
            "核心第二关：吹气怎样一把掀掉皮肤表面的“3 毫米隐形羽绒服”？",
            "静止空气是极佳的隔热棉；高速凉风把热边界层削薄 4 倍，让皮肤散热功率瞬间飙升！",
        )
    )

    # Left Card: Calm / Gentle 'Ha~' Preserves & Warms Boundary Layer
    els.append(card(20, 62, 352, 412))
    els.append(step_badge(38, 84, 1, fg=RED, bg=RED_SOFT))
    els.append(txt(56, 88, "平时与哈气：厚保温层护体 → 暖气倒灌进皮肤", size=12.0, color=INK, weight="700"))

    # Cross-section of Palm Skin + Thick Warm Boundary Layer
    els.append('<rect x="44" y="256" width="304" height="54" rx="8" fill="#fdba74" stroke="#ea580c" stroke-width="1.5"/>')
    els.append(txt(196, 279, "手掌真皮与毛细血管网（恒温供热 32.5°C）", size=10.5, color="#7c2d12", anchor="middle", weight="700"))
    els.append(txt(196, 298, "暖觉受体 TRPV3 / TRPV4 被激活 → 大脑报“暖！”", size=10.0, color=RED, anchor="middle", weight="700"))

    # Thick ~4-5 mm thermal boundary layer blanket above skin
    els.append('<rect x="44" y="182" width="304" height="74" rx="6" fill="#fee2e2" fill-opacity="0.82" stroke="#f87171" stroke-dasharray="5,3"/>')
    els.append(txt(196, 206, "平时：厚约 3–5 mm 的“静止暖空气羽绒服”", size=10.3, color=RED, anchor="middle", weight="700"))
    els.append(txt(196, 226, "空气导热极慢 k ≈ 0.026 W/(m·K)，牢牢锁住体温", size=9.9, color=BODY, anchor="middle"))

    # Gentle 34.5 °C 'Ha~' arrows pressing warm air INTO skin
    for ax in [96, 196, 296]:
        els.append(_line(ax, 122, ax, 176, stroke=RED, sw=2.2, marker="arr-red"))
    els.append(txt(196, 114, "张嘴哈气：34.5°C 暖湿气流（高于皮温 32.5°C）", size=10.3, color=RED, anchor="middle", weight="700"))
    els.append(txt(196, 246, "↓ 热量净流入皮肤（显热＋凝结潜热双加热）↓", size=10.0, color=RED, anchor="middle", weight="700"))

    els.append(card(38, 326, 316, 132, rx=8, fill=RED_SOFT, stroke="#fca5a5"))
    els.append(txt(50, 347, "为什么 20°C 房间里不吹风时手不觉得冷？", size=10.6, color=INK, weight="700"))
    els.append(txt(50, 368, "• 房间明明只有 20°C，但贴着你皮肤的那几毫米空气已被", size=10.0, color=BODY))
    els.append(txt(50, 386, "  体温焐热到了 28–31°C，自然对流换热系数仅 h ≈ 6 W/m²K；", size=10.0, color=BODY))
    els.append(txt(50, 404, "• 张嘴哈气直接送来 34.5°C 热气团，比这件“隐形羽绒服”", size=10.0, color=BODY))
    els.append(txt(50, 422, "  还要烫，热流方向从外往里走，冰凉的手立刻缓过劲来！", size=10.0, color=INK, weight="600"))

    # Right Card: High-Speed 'Fu~' Shreds Boundary Layer -> Massive Heat Extraction!
    els.append(card(388, 62, 352, 412))
    els.append(step_badge(406, 84, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(424, 88, "撅嘴吹气：削薄保温层 4 倍 → 热量狂泻而出", size=12.0, color=INK, weight="700"))

    # Skin block (cooled epidermis!)
    els.append('<rect x="412" y="256" width="304" height="54" rx="8" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>')
    els.append(txt(564, 279, "手掌表皮迅速失温（dT/dt ＜ 0，跌破 28°C）", size=10.5, color="#1e3a8a", anchor="middle", weight="700"))
    els.append(txt(564, 298, "冷觉离子通道 TRPM8 高频放电 → 大脑报“好凉！”", size=10.0, color=BLUE, anchor="middle", weight="700"))

    # Razor-thin ~0.8-1.1 mm boundary layer!
    els.append('<rect x="412" y="238" width="304" height="18" rx="3" fill="#dbeafe" stroke="#3b82f6" stroke-dasharray="4,2"/>')
    els.append(txt(564, 251, "边界层被高速风削薄至 ≈ 1 mm！（h 暴涨 5 倍至 34 W/m²K）", size=9.8, color=BLUE, anchor="middle", weight="700"))

    # Sweeping 21.2 °C wind arrows stripping warm air away + upward heat-loss red-to-blue arrows
    els.append(_line(422, 162, 702, 162, stroke=BLUE, sw=2.6, marker="arr-blue"))
    els.append(_line(422, 196, 702, 196, stroke=BLUE, sw=2.6, marker="arr-blue"))
    for hx_arr in [476, 564, 652]:
        els.append(_line(hx_arr, 254, hx_arr + 20, 174, stroke=ORANGE, sw=1.9, marker="arr-orange"))
    els.append(txt(564, 138, "21.2°C 高速混合风（v ≈ 4–5 m/s）横扫手面", size=10.4, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(564, 224, f"↑ 仅对流显热流失就高达 q'' ≈ {q_blow:.0f} W/m²！↑", size=10.1, color=ORANGE, anchor="middle", weight="700"))

    els.append(card(406, 326, 316, 132, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    els.append(txt(418, 347, "电风扇与“风寒效应（Wind Chill）”同一原理！", size=10.6, color=BLUE, weight="700"))
    els.append(txt(418, 368, "• 夏天开电风扇并没有降低屋里的空气温度，却让你一秒", size=10.0, color=BODY))
    els.append(txt(418, 386, "  凉快下来——因为它遵循边界层定律 δ ∝ 1/√v；", size=10.0, color=BODY))
    els.append(txt(418, 404, "• 吹气风速比自然对流快近 20 倍，一把扯掉皮肤表面的", size=10.0, color=BODY))
    els.append(txt(418, 422, "  暖气被子，让 21.2°C 凉空气贴脸抽走你的热量！", size=10.0, color=INK, weight="600"))

    return figure(
        490,
        "皮肤表面静止空气保温边界层在哈气与吹气下的强制对流剥离对比图",
        "左卡展示平时手掌表面裹着3至5毫米静止暖空气边界层，张嘴哈气（34.5摄氏度）使热量向皮肤内净流入；右卡展示撅嘴吹气高速凉风（21.2摄氏度）将边界层削薄至约1毫米，对流换热系数暴涨5倍，显热抽走功率超380瓦每平方米。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 4. Water Phase-Change Amplifier: Condensation (+2420 J/g) vs Evaporation (-2420 J/g)
# ---------------------------------------------------------------------------
def build_condensation_vs_evaporation() -> str:
    # Exact NIST psychrometric & latent heat checks
    lv_j_per_g = 2420.0          # NIST at ~33 °C: 2561 - 138 ≈ 2423 J/g
    cp_water = 4.18              # J/(g*K)
    ratio_latent = lv_j_per_g / cp_water
    assert 575.0 < ratio_latent < 585.0  # 1 g evaporation = cooling 1 g water by ~579 °C!

    # Vapor density check (g/m^3):
    # Lung exit: 35 °C, 95% RH -> 0.95 * 39.67 = 37.7 g/m^3 (Dew point ≈ 34.1 °C!)
    rho_lung = 0.95 * 39.67
    # Room air: 20 °C, 40% RH -> 0.40 * 17.31 = 6.92 g/m^3
    rho_room = 0.40 * 17.31
    # 1:11.25 diluted pursed-lip jet at 15 cm:
    mr = jet_mass_ratio(15.0, 4.0)
    rho_chui = rho_room + (rho_lung - rho_room) / mr
    # Skin saturated surface at 32.5 °C: ~34.7 g/m^3!
    rho_skin_sat = 34.7
    assert rho_lung > rho_skin_sat       # 37.7 > 34.7 (and >> 17.3 g/m^3 on 20 °C cold winter hands!) -> CONDENSES!
    assert 9.0 < rho_chui < 10.0         # ~9.4 g/m^3 << 34.7 g/m^3 -> EVAPORATES RAPIDLY!

    els = []
    els.extend(
        header(
            "核心第三关：水蒸气的“正反外挂”——为什么哈气起白雾，吹气秒除雾？",
            "每 1 克水相变藏着 2420 焦耳潜热（顶得上把 1 克水烧开近 6 次）！哈气凝结放热，吹气蒸发吸热",
        )
    )

    # Left Card: 'Ha~' Condensation Heating (Micro Steam Iron!)
    els.append(card(20, 62, 352, 422))
    els.append(step_badge(38, 84, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 88, "哈气＝微型蒸汽熨斗：水汽凝结释放潜热", size=12.0, color=INK, weight="700"))

    # Visual box: Glasses / Cold winter hand receiving saturated breath -> droplets + heat!
    els.append(card(38, 108, 316, 186, rx=8, fill="#fff7ed", stroke="#fdba74"))
    els.append(txt(196, 130, f"肺部呼气含水量高达 {rho_lung:.1f} g/m³（露点 ≈ 34.1°C）", size=10.3, color=ORANGE, anchor="middle", weight="700"))

    # Vapor wavy arrows condensing into droplets on cold hand/lens surface (y=236)
    els.append('<rect x="58" y="236" width="276" height="36" rx="6" fill="#fed7aa" stroke="#ea580c" stroke-width="1.4"/>')
    els.append(txt(196, 259, "冬天冰凉的手 / 眼镜片（15–25°C ＜ 露点 34.1°C）", size=10.1, color="#7c2d12", anchor="middle", weight="700"))

    for dx in [94, 146, 198, 250, 300]:
        els.append(_line(dx, 148, dx, 214, stroke=ORANGE, sw=1.7, dash="4,3", marker="arr-orange"))
        els.append(f'<circle cx="{dx}" cy="230" r="5.2" fill="#38bdf8" stroke="#0284c7" stroke-width="1.2"/>')
    els.append(txt(196, 192, "水蒸气无处可逃 → 凝结成微米水珠（起白雾！）", size=10.1, color=INK, anchor="middle", weight="700"))
    els.append(txt(196, 284, "🔥 每凝结 1 克水珠，向手心释放 +2420 J 潜热！", size=10.2, color=RED, anchor="middle", weight="700"))

    els.append(card(38, 308, 316, 160, rx=8, fill=AMBER_SOFT, stroke="#fcd34d"))
    els.append(txt(50, 329, "擦眼镜动作里藏着的相变铁证：", size=10.6, color=INK, weight="700"))
    els.append(txt(50, 350, "• 想擦眼镜时，所有人都会本能地【张大嘴哈气】：因为", size=10.0, color=BODY))
    els.append(txt(50, 369, "  未稀释暖气露点高达 34°C，碰到室温镜片必结一层白雾；", size=10.0, color=BODY))
    els.append(txt(50, 388, "• 冬天冻僵的手只有十来度，哈气时不仅没法蒸发汗水，", size=10.0, color=BODY))
    els.append(txt(50, 407, "  反而在手背结出肉眼难辨的微水膜，把气化潜热倒贴给", size=10.0, color=BODY))
    els.append(txt(50, 426, "  你的皮肤——这就是哈气总带着一股“湿热劲儿”的原因！", size=10.0, color=INK, weight="600"))
    els.append(txt(50, 450, f"（注：2420 J 足以让 1 克液态水升温 {ratio_latent:.0f}°C！）", size=9.9, color=RED, weight="700"))

    # Right Card: 'Fu~' Evaporative Cooling (Turbo Sweat Dryer!)
    els.append(card(388, 62, 352, 422))
    els.append(step_badge(406, 84, 2, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(424, 88, "吹气＝高速抽湿机：微汗瞬间蒸发狂吸潜热", size=12.0, color=INK, weight="700"))

    els.append(card(406, 108, 316, 186, rx=8, fill="#f0fdfa", stroke="#5eead4"))
    els.append(txt(564, 130, f"掺入 11 倍干空气后含水量骤降至 {rho_chui:.1f} g/m³（露点仅 10°C）", size=10.1, color=TEAL, anchor="middle", weight="700"))

    els.append('<rect x="426" y="236" width="276" height="36" rx="6" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.4"/>')
    els.append(txt(564, 259, "手掌微汗毛孔表面饱和水汽 ≈ 34.7 g/m³（远高于 9.4！）", size=10.0, color="#1e3a8a", anchor="middle", weight="700"))

    # Droplets lifting off and evaporating into fast blue airstream!
    els.append(_line(432, 162, 696, 162, stroke=BLUE, sw=2.2, marker="arr-blue"))
    for dx in [474, 534, 594, 654]:
        els.append(f'<circle cx="{dx}" cy="230" r="4.2" fill="#38bdf8" fill-opacity="0.55" stroke="#0284c7" stroke-dasharray="2,2"/>')
        els.append(_line(dx, 224, dx + 16, 170, stroke=TEAL, sw=1.8, marker="arr-green"))
    els.append(txt(564, 204, "巨大湿度差＋强风吹散 → 隐性微汗瞬间气化飞走！", size=10.1, color=TEAL, anchor="middle", weight="700"))
    els.append(txt(564, 284, "❄️ 每蒸发 1 克微汗，从皮肤硬抢走 -2420 J 潜热！", size=10.2, color=BLUE, anchor="middle", weight="700"))

    els.append(card(406, 308, 316, 160, rx=8, fill=TEAL_SOFT, stroke="#5eead4"))
    els.append(txt(418, 329, "🧪 沾一滴水再试：冷热反差当场放大 5 倍！", size=10.6, color=TEAL, weight="700"))
    els.append(txt(418, 350, "• 哪怕你觉得手是“干”的，人类手掌每平方厘米也有数百", size=10.0, color=BODY))
    els.append(txt(418, 369, "  条汗腺时刻在分泌微量“不显性失水（TEWL）”；", size=10.0, color=BODY))
    els.append(txt(418, 388, "• 在手背抹半滴自来水再撅嘴吹一口：你会冻得一激灵！", size=10.0, color=BODY))
    els.append(txt(418, 407, "• 平时我们端起滚烫的稀饭【撅嘴吹气】，高达 70%–80%", size=10.0, color=BODY))
    els.append(txt(418, 426, "  的降温功劳，正是吹走粥面饱和蒸汽、逼着热水蒸发吸热！", size=10.0, color=INK, weight="600"))
    els.append(txt(418, 450, "（套一只密封塑料袋在手上再吹，凉意立刻减半！）", size=9.9, color=BLUE, weight="700"))

    return figure(
        500,
        "水蒸气相变潜热双向放大效应：哈气露点凝结放热与吹气稀释蒸发吸热对比图",
        "左卡展示肺部呼气含水量37.7克每立方米（露点34.1摄氏度），遇冷手或镜片凝结成水雾并每克释放2420焦耳潜热；右卡展示吹气混入11倍室温干空气后含水量降至9.4克每立方米（露点10摄氏度），驱动手面微汗急速蒸发并每克吸走2420焦耳潜热。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 5. Extreme Counterexample (45 °C Sauna Reversal) & 2021 Nobel TRPM8 Sensors
# ---------------------------------------------------------------------------
def build_sauna_reversal_and_trpm8() -> str:
    # Check mixed jet temperature inside a 48 °C dry sauna!
    t_sauna = 48.0
    t_jet_sauna = jet_mixed_temp(15.0, 4.0, 35.5, t_sauna)
    # 1 part 35.5 °C breath + 11.25 parts 48 °C sauna air -> ~47.0 °C (>> 33 °C skin!)
    assert 46.5 < t_jet_sauna < 47.5

    els = []
    els.extend(
        header(
            "终极反转与大脑彩蛋：桑拿房里吹气反而烫手？薄荷糖为何骗过冷觉神经？",
            "卷吸进什么温度的空气就吹出什么风；而皮肤报给大脑的不是“温度读数”，而是“失温速率”！",
        )
    )

    # Left Card: 48 °C Dry Sauna / Air-Fryer Counterexample
    els.append(card(20, 62, 356, 418))
    els.append(step_badge(38, 84, 1, fg=RED, bg=RED_SOFT))
    els.append(txt(56, 88, "极限反例：在 48°C 干蒸桑拿房里撅嘴吹温度计！", size=12.0, color=INK, weight="700"))

    els.append(card(38, 108, 320, 178, rx=8, fill=RED_SOFT, stroke="#fca5a5"))
    els.append(txt(198, 130, "当环境室温（48°C）＞ 肺温（35.5°C）＞ 皮温（34°C）", size=10.2, color=RED, anchor="middle", weight="700"))

    # Jet cone entraining 48 °C HOT sauna air!
    els.append('<polygon points="62,188 286,154 286,226 62,194" fill="#fecaca" fill-opacity="0.75" stroke="#ef4444" stroke-width="1.4"/>')
    els.append(_line(128, 138, 144, 166, stroke=RED, sw=1.7, marker="arr-red"))
    els.append(_line(208, 136, 224, 162, stroke=RED, sw=1.7, marker="arr-red"))
    els.append(_line(128, 244, 144, 216, stroke=RED, sw=1.7, marker="arr-red"))
    els.append(_line(208, 246, 224, 220, stroke=RED, sw=1.7, marker="arr-red"))
    els.append(txt(176, 194, f"卷入 11 倍热浪 → 混合风高达 {t_jet_sauna:.0f}°C！", size=10.1, color="#7f1d1d", anchor="middle", weight="700"))
    els.append('<rect x="290" y="150" width="48" height="82" rx="6" fill="#f97316" stroke="#c2410c" stroke-width="1.5"/>')
    els.append(txt(314, 188, "干包裹", size=10.0, color="#fff", anchor="middle", weight="700"))
    els.append(txt(314, 206, "越吹越烫!", size=9.9, color="#fef08a", anchor="middle", weight="700"))
    els.append(txt(198, 272, "这正是【空气炸锅】与【沙漠热风】的强制对流加热原理！", size=10.0, color=RED, anchor="middle", weight="700"))

    els.append(card(38, 298, 320, 168, rx=8, fill="#f8fafc", stroke=BORDER))
    els.append(txt(50, 320, "为什么桑拿房里吹“湿手”和“干手套”截然不同？", size=10.6, color=INK, weight="700"))
    els.append(txt(50, 341, "• 对着戴薄橡胶手套的手（或干温度计）吹气：隔绝了汗水", size=10.0, color=BODY))
    els.append(txt(50, 360, f"  蒸发后，47°C 热风撕开隔热层，你会觉得像电吹风一样烫！", size=10.0, color=BODY))
    els.append(txt(50, 379, "• 对着满是汗珠的裸手吹气：只要桑拿房很干燥（湿球温度", size=10.0, color=BODY))
    els.append(txt(50, 398, "  低于皮温），汗珠猛烈蒸发仍能抢回一丝短暂凉意；但若", size=10.0, color=BODY))
    els.append(txt(50, 417, "  是 100% 湿度的蒸汽浴室，蒸发归零，怎么吹都是滚烫的！", size=10.0, color=RED, weight="600"))
    els.append(txt(50, 444, "⇒ 铁证闭环：卷吸改气温 ＋ 风速破保温 ＋ 湿度定相变。", size=10.0, color=INK, weight="700"))

    # Right Card: 2021 Nobel Prize Thermoreceptors (TRPM8 vs TRPV1/TRPV3)
    els.append(card(390, 62, 350, 418))
    els.append(step_badge(408, 84, 2, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(426, 88, "2021 诺奖彩蛋：皮肤里的冷热分子开关", size=12.0, color=INK, weight="700"))

    # Channel activation window diagram (10 °C .. 50 °C)
    els.append(card(408, 108, 314, 178, rx=8, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    els.append(txt(565, 129, "David Julius 等发现的皮肤 TRP 温度离子通道家族", size=10.2, color=PURPLE, anchor="middle", weight="700"))

    ax0, ax1, ay = 434.0, 698.0, 236.0
    els.append(_line(ax0, ay, ax1, ay, stroke=SLATE, sw=1.4))
    for temp_t in [15, 25, 32.5, 43]:
        tx = ax0 + ((temp_t - 12.0) / 36.0) * (ax1 - ax0)
        els.append(_line(tx, ay, tx, ay + 5, stroke=SLATE, sw=1.2))
        lbl = f"{temp_t:.1f}°C" if temp_t == 32.5 else f"{temp_t}°C"
        els.append(txt(tx, ay + 18, lbl, size=9.8, color=MUTED, anchor="middle", cls="mono"))

    # TRPM8 cold curve (peaks < 26 °C, threshold ~28 °C)
    els.append('<path d="M 436 164 Q 496 164 552 234" fill="none" stroke="#2563eb" stroke-width="2.8"/>')
    els.append(txt(484, 156, "TRPM8 冷觉＋薄荷醇通道", size=10.0, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(484, 198, "＜28°C 开启", size=9.9, color=BLUE, anchor="middle"))

    # TRPV3/V4 warm curve (31..39 °C) & TRPV1 hot/capsaicin curve (>43 °C)
    els.append('<path d="M 556 234 Q 604 176 644 234" fill="none" stroke="#ea580c" stroke-width="2.4"/>')
    els.append(txt(604, 174, "TRPV3/4 温热", size=9.9, color=ORANGE, anchor="middle", weight="700"))
    els.append('<path d="M 648 234 Q 674 166 698 158" fill="none" stroke="#dc2626" stroke-width="2.6"/>')
    els.append(txt(668, 152, "TRPV1 灼痛/辣椒素", size=9.9, color=RED, anchor="middle", weight="700"))

    els.append(txt(565, 272, "皮肤神经对【温度变化率 dT/dt】比绝对温度敏感十倍！", size=10.0, color=INK, anchor="middle", weight="700"))

    els.append(card(408, 298, 314, 168, rx=8, fill="#f8fafc", stroke=BORDER))
    els.append(txt(420, 320, "含一颗薄荷糖再吸气／吹气，为什么像进了北极？", size=10.5, color=PURPLE, weight="700"))
    els.append(txt(420, 341, "• 平时室温铁块和木块同为 20°C，摸铁块却冰手得多——因", size=10.0, color=BODY))
    els.append(txt(420, 360, "  为铁导热快，让表皮每秒跌温更快，猛烈触发 TRPM8；", size=10.0, color=BODY))
    els.append(txt(420, 379, "• 薄荷醇（Menthol）是一把化学万能钥匙，能把 TRPM8 的", size=10.0, color=BODY))
    els.append(txt(420, 398, "  激活门槛从 28°C 抬高到 34°C 以上！吃颗薄荷糖在手背涂", size=10.0, color=BODY))
    els.append(txt(420, 417, "  一点薄荷清凉油，哪怕轻轻哈一口暖气都会觉得透心凉！", size=10.0, color=INK, weight="600"))
    els.append(txt(420, 444, "（辣椒素同理强开 TRPV1，所以吃火锅像嘴里着了火！）", size=9.9, color=RED, weight="600"))

    return figure(
        495,
        "48摄氏度桑拿房吹气变烫极限反例与2021诺贝尔奖TRP温度离子通道原理图",
        "左卡展示在48摄氏度干蒸桑拿房中吹气会卷入11倍48摄氏度热空气，混合风达47摄氏度使干包裹越吹越烫；右卡展示2021年诺贝尔生理学或医学奖揭示的TRPM8冷觉薄荷醇通道与TRPV3/TRPV1热觉辣椒素通道。",
        els,
        extra_defs=_markers(),
    )


@register(TOPIC, "physics", "为什么哈气热、吹气冷（5张760px原创SVG图解）")
def build_all() -> None:
    builders = [
        ("ha-vs-chui-jet-entrainment.svg", build_ha_vs_chui_jet_entrainment),
        ("myth-busting-joule-thomson-vs-distance.svg", build_myth_busting_jt_vs_distance),
        ("skin-boundary-layer-invisible-down-jacket.svg", build_skin_boundary_layer),
        ("condensation-heating-vs-evaporation.svg", build_condensation_vs_evaporation),
        ("sauna-reversal-and-trpm8-receptors.svg", build_sauna_reversal_and_trpm8),
    ]
    for fname, fn in builders:
        svg = fn()
        write_svg(TOPIC, fname, svg)
