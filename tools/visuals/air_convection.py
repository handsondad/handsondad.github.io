"""空气对流原理：浮力、边界层、瑞利数与大气环流的原创 SVG 图解。"""

from __future__ import annotations

import math

from .core import (
    BLUE,
    BLUE_LINE,
    BLUE_SOFT,
    BODY,
    BORDER,
    CARD_BG,
    GREEN,
    GREEN_SOFT,
    INK,
    MUTED,
    ORANGE,
    ORANGE_SOFT,
    PURPLE,
    PURPLE_SOFT,
    SLATE,
    card,
    figure,
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

TOPIC = "air-convection"


def _line(x1, y1, x2, y2, stroke=SLATE, sw=1.6, dash=None, marker=None, opacity=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    if opacity is not None:
        extra += f' stroke-opacity="{opacity}"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def _anim_defs(names, keyframes):
    css = ["<style>"]
    for name, body in keyframes:
        css.append(f"  @keyframes {name} {{{body}}}")
    css.append(f"  .{names[0]} {{ animation: {names[0]} 2.8s ease-out 1 forwards; }}")
    for name in names[1:]:
        css.append(f"  .{name} {{ animation: {name} 2.8s cubic-bezier(0.22, 0.61, 0.36, 1) 1 forwards; }}")
    css.append("  @media (prefers-reduced-motion: reduce) {")
    css.append("    ." + ", .".join(names) + " {")
    css.append("      animation: none !important; transform: none !important;")
    css.append("      stroke-dashoffset: 0 !important; opacity: 1 !important;")
    css.append("    }")
    css.append("  }")
    css.append("</style>")
    return "\n".join(css)


# ---------------------------------------------------------------------------
# 1. 浮力从哪里来：重力 + 密度差，而不是“热自己想往上走”
# ---------------------------------------------------------------------------
def build_buoyancy_origin() -> str:
    rho_20 = 1.205
    t_cold_k, t_hot_k = 293.15, 303.15
    rho_30 = rho_20 * t_cold_k / t_hot_k
    d_rho = rho_20 - rho_30
    net_force_per_m3 = d_rho * 9.81
    accel = net_force_per_m3 / rho_30
    assert 0.038 < d_rho < 0.042
    assert 0.37 < net_force_per_m3 < 0.41
    assert 0.32 < accel < 0.35

    css = _anim_defs(
        ["anim-rise", "anim-inflow"],
        [
            ("riseAir", "0% { transform: translateY(12px); opacity: 0.3; } 100% { transform: translateY(0px); opacity: 1; }"),
            ("inflowAir", "0% { transform: translateX(-8px); opacity: 0.35; } 100% { transform: translateX(0px); opacity: 1; }"),
        ],
    )

    els = []
    els.extend(
        header(
            "热空气为什么会上升？真正的发动机是重力，不是“热”本身",
            "温差先造出密度差，重力再把它变成净浮力；抽掉重力，自然对流就熄火。",
        )
    )

    els.append(card(20, 66, 352, 390))
    els.append(step_badge(38, 88, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 92, "浮力账本：1 m³ 的 30°C 热团泡在 20°C 空气里", size=12.2, color=INK, weight="700"))

    els.append('<rect x="36" y="106" width="320" height="150" rx="8" fill="#f3f8fc" stroke="#d7e6f2"/>')
    els.append(txt(48, 126, "环境空气 20°C", size=10.6, color=BLUE, weight="600"))
    els.append(txt(48, 144, "ρ冷 = 1.205 kg/m³", size=10.2, color=SLATE))
    els.append(_line(56, 170, 56, 230, stroke=BLUE, sw=1.5, marker="arr-blue"))
    els.append(_line(56, 170, 56, 122, stroke=BLUE, sw=1.5, marker="arr-blue"))
    els.append(txt(38, 268, "蓝色箭头：冷空气在重力下建立“下高上低”的气压梯度", size=10.0, color=BLUE))

    els.append('<g class="anim-rise">')
    els.append('<ellipse cx="228" cy="172" rx="72" ry="38" fill="#fde4d0" stroke="#e59a6a" stroke-width="1.5"/>')
    els.append(txt(228, 166, "热团 30°C", size=11.6, color=ORANGE, anchor="middle", weight="700"))
    els.append(txt(228, 184, f"ρ热 ≈ {rho_30:.3f} kg/m³", size=10.2, color=ORANGE, anchor="middle"))
    els.append(_line(228, 130, 228, 112, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    els.append("</g>")
    els.append(txt(228, 242, "F浮 = (ρ冷−ρ热)gV", size=10.4, color=ORANGE, anchor="middle", weight="600"))

    els.append(txt(38, 298, f"• 理想气体 ρ ∝ 1/T：密度只差 {d_rho / rho_20 * 100:.1f}%（约 3.3%）", size=10.5, color=BODY))
    els.append(txt(38, 321, f"• 每 1 m³ 净浮力 = {d_rho:.3f} × 9.81 ≈ {net_force_per_m3:.2f} N", size=10.5, color=BODY))
    els.append(txt(38, 344, f"• 加速度 a = F/m ≈ {accel:.2f} m/s² ≈ {accel / 9.81 * 100:.1f}% g", size=10.5, color=BODY))
    els.append(txt(38, 372, "别把“热”当成推力：真正推它上升的，是周围", size=10.4, color=INK, weight="600"))
    els.append(txt(38, 391, "更重的冷空气通过压力场挤上来的那一下。", size=10.4, color=INK, weight="600"))
    els.append(txt(38, 428, "没有温差 ⇒ 没有密度差 ⇒ 没有浮力 ⇒ 空气静止", size=10.4, color=MUTED))

    els.append(card(388, 66, 352, 390))
    els.append(step_badge(406, 88, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(424, 92, "反证实验：把重力拿走会怎样？", size=12.2, color=INK, weight="700"))

    els.append(txt(420, 108, "地球：重力场里的烛焰", size=10.8, color=ORANGE, anchor="middle", weight="700"))
    els.append('<path d="M 420 210 Q 404 180 420 142 Q 436 180 420 210 Z" fill="#fca5a5" stroke="#c25014" stroke-width="1.4"/>')
    els.append('<path d="M 420 200 Q 413 183 420 160 Q 427 183 420 200 Z" fill="#fde68a"/>')
    els.append('<g class="anim-rise">')
    els.append(_line(420, 138, 420, 120, stroke=ORANGE, sw=2, marker="arr-orange"))
    els.append("</g>")
    els.append('<g class="anim-inflow">')
    els.append(_line(388, 222, 408, 210, stroke=BLUE, sw=1.7, marker="arr-blue"))
    els.append(_line(452, 222, 432, 210, stroke=BLUE, sw=1.7, marker="arr-blue"))
    els.append("</g>")
    els.append(txt(420, 240, "热气上升，冷空气从下方补位", size=9.8, color=SLATE, anchor="middle"))

    els.append(_line(570, 112, 570, 240, stroke=BORDER, sw=1, dash="4 4"))
    els.append(txt(670, 126, "国际空间站：微重力", size=10.8, color=BLUE, anchor="middle", weight="700"))
    els.append('<circle cx="670" cy="180" r="30" fill="#fde4d0" stroke="#c25014" stroke-width="1.6"/>')
    els.append('<circle cx="670" cy="180" r="15" fill="#fde68a" fill-opacity="0.85"/>')
    els.append(txt(670, 240, "浮力环流消失 → 球形火焰", size=9.8, color=SLATE, anchor="middle"))

    els.append(txt(404, 278, "NASA 的原话很直白：地球上的烛焰之所以尖，是因为", size=10.4, color=BODY))
    els.append(txt(404, 299, "较轻的热气上升、较重的环境空气从下方补位；", size=10.4, color=BODY))
    els.append(txt(404, 320, "在微重力里“that circulation effect does not happen”。", size=10.4, color=BODY))
    els.append(txt(404, 352, "热传导、热辐射不靠重力；风扇驱动的强迫对流也不靠。", size=10.4, color=INK, weight="600"))
    els.append(txt(404, 381, "靠浮力吃饭的“自然对流”，才是重力的孩子。", size=10.6, color=BLUE, weight="700"))
    els.append(txt(404, 420, "一句话：自然对流 = 温差 × 重力 × 可流动的流体", size=10.8, color=INK, weight="700"))

    els.append(card(20, 468, 720, 38, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 493, "图解只标出力的来源与数量级；真实热团上升时会被周围空气卷吸、拉伸，速度远小于理想加速度。", size=10.6, color=SLATE))

    return figure(
        516,
        "空气对流的浮力起源与微重力反证图",
        "20摄氏度环境密度1.205千克每立方米，30摄氏度热团密度约1.165，密度差3.3%，每立方米净浮力约0.39牛，加速度约0.33米每二次方秒。图示地球烛焰因热气上升冷空气补位而呈尖形，国际空间站微重力下浮力环流消失呈球形。",
        els,
        extra_css=css,
    )


# ---------------------------------------------------------------------------
# 2. 边界层：热量先烤热贴着壁面的一层空气
# ---------------------------------------------------------------------------
def build_boundary_layer() -> str:
    g, beta, dt = 9.81, 1.0 / 303.15, 20.0
    nu, alpha, k_air, length = 1.57e-5, 2.2e-5, 0.026, 0.5
    ra = g * beta * dt * length**3 / (nu * alpha)
    nu_avg = 0.59 * ra**0.25
    h = nu_avg * k_air / length
    q_conv = h * dt
    q_still = k_air / length * dt
    delta_eff = k_air / h
    assert 2.2e8 < ra < 2.5e8
    assert 70 < nu_avg < 75
    assert 3.6 < h < 4.0
    assert 74 < q_conv < 78
    assert abs(q_conv / q_still - nu_avg) < 1e-9
    assert 0.006 < delta_eff < 0.008

    els = []
    els.extend(
        header(
            "热量不是直接“跳”进空气：先烤热贴壁的那层薄气膜",
            "竖直 40°C 热板放进 20°C 静止空气，温度与速度边界层从下往上越长越厚。",
        )
    )

    els.append(card(20, 66, 392, 398))
    els.append(step_badge(38, 88, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 92, "边界层剖面：越往上，被烤热的空气层越厚", size=12.0, color=INK, weight="700"))

    els.append('<rect x="72" y="112" width="18" height="298" rx="3" fill="#f9d7b5" stroke="#c25014" stroke-width="1.6"/>')
    els.append(txt(81, 104, "40°C 竖板", size=10.4, color=ORANGE, anchor="middle", weight="700"))
    els.append('<rect x="90" y="112" width="286" height="298" rx="4" fill="#f4f9fd" stroke="#dbe8f2"/>')
    els.append(txt(360, 130, "环境 20°C", size=10.4, color=BLUE, anchor="end", weight="600"))

    for yy, reach in [(170, 60), (260, 94), (350, 132)]:
        els.append(_line(90, yy, 376, yy, stroke=BORDER, sw=1, dash="3 4"))
        els.append(
            f'<path d="M 91 {yy} C {105 + reach * 0.3:.0f} {yy - 2}, '
            f'{105 + reach * 0.7:.0f} {yy - 13}, {92 + reach} {yy - 13}" '
            'fill="none" stroke="#e08a4c" stroke-width="2.2"/>'
        )
        els.append(_line(92, yy - 4, 92 + reach, yy - 4, stroke=GREEN, sw=1, dash="2 3"))
        els.append(txt(92 + reach + 4, yy - 6, "δT", size=10.0, color=GREEN, weight="700"))

    els.append(_line(112, 300, 112, 244, stroke=ORANGE, sw=2.1, marker="arr-orange"))
    els.append(_line(142, 250, 142, 190, stroke=ORANGE, sw=2.1, marker="arr-orange"))
    els.append(_line(182, 200, 182, 140, stroke=ORANGE, sw=2.1, marker="arr-orange"))
    els.append(txt(220, 222, "贴壁空气受热变轻 → 沿板上升", size=10.2, color=ORANGE, weight="600"))
    els.append(txt(206, 244, "黏性让壁面速度为 0，只能靠传导穿过气膜", size=10.0, color=SLATE))
    els.append(pill(244, 396, "层流 → 湍流（Ra 更高时）", fg=PURPLE, bg=PURPLE_SOFT, border=PURPLE, w=142, h=22, size=10.2))
    els.append(txt(38, 432, "温度从壁面 40°C 衰减到远处 20°C 的距离，就是热边界层厚度 δT。", size=10.4, color=BODY))
    els.append(txt(38, 452, "气膜越厚 = 热阻越大；流动把它削薄，换热系数 h 就上去。", size=10.4, color=INK, weight="600"))

    els.append(card(426, 66, 314, 398))
    els.append(step_badge(444, 88, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(462, 92, "把这张图换算成硬数字", size=12.0, color=INK, weight="700"))

    els.append(txt(444, 124, "① 浮力有多强：瑞利数", size=11.4, color=BLUE, weight="700"))
    els.append(txt(444, 148, "Ra = gβΔT·L³ / (ν·α)", size=11.8, color=INK, weight="700"))
    els.append(txt(444, 168, "β≈1/303 K⁻¹，ν≈1.57×10⁻⁵ m²/s", size=10.0, color=SLATE))
    els.append(txt(444, 187, "α≈2.2×10⁻⁵ m²/s，L=0.5 m", size=10.0, color=SLATE))
    els.append(txt(444, 211, f" Ra ≈ {ra:.2e}（层流，落在 10⁴–10⁹ 区间）", size=10.6, color=BLUE, weight="600"))

    els.append(_line(444, 226, 722, 226, stroke=BORDER, sw=1))
    els.append(txt(444, 250, "② 换热增强多少：努塞尔数", size=11.4, color=BLUE, weight="700"))
    els.append(txt(444, 274, "Nu = hL/k ≈ 0.59 Ra¹⁄⁴", size=11.8, color=INK, weight="700"))
    els.append(txt(444, 298, f"Nu ≈ {nu_avg:.0f} ⇒ h = Nu·k/L ≈ {h:.1f} W/(m²·K)", size=10.6, color=BODY))
    els.append(txt(444, 317, "这里 k 是空气导热系数 ≈ 0.026 W/(m·K)", size=10.0, color=SLATE))

    els.append(_line(444, 332, 722, 332, stroke=BORDER, sw=1))
    els.append(txt(444, 356, "③ 每平方米每秒搬走多少热", size=11.4, color=ORANGE, weight="700"))
    els.append(txt(444, 380, f"q″ = hΔT ≈ {q_conv:.0f} W/m²", size=11.8, color=INK, weight="700"))
    els.append(txt(444, 402, f"若 0.5 m 空气完全静止：kΔT/L ≈ {q_still:.0f} W/m²", size=10.2, color=SLATE))
    els.append(txt(444, 424, f"⇒ 对流把散热放大约 {nu_avg:.0f} 倍！", size=11.2, color=ORANGE, weight="700"))
    els.append(txt(444, 450, "等效气膜厚度 δ = k/h ≈ 6.9 mm", size=10.4, color=GREEN, weight="600"))

    els.append(card(20, 476, 720, 36, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 500, "注意：h 不是空气的“固定常数”。几何、流速、温差、特征长度一变，h 就会跟着变。", size=10.6, color=SLATE))

    return figure(
        520,
        "竖直热板自然对流的温度边界层与换热计算图",
        "40摄氏度竖直热板置于20摄氏度静止空气中，热边界层沿板向上增厚；按空气物性取贝塔约1/303每开、运动黏度1.57e-5、热扩散率2.2e-5平方米每秒，板高0.5米温差20开时瑞利数约2.3e8，努塞尔数约73，换热系数约3.8瓦每平方米每开，热流密度约76瓦每平方米，是整层静止空气导热的约73倍。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 瑞利–贝纳德：为什么不是“一加热就对流”
# ---------------------------------------------------------------------------
def build_rayleigh_onset() -> str:
    ra_free = 27 * math.pi**4 / 4
    assert 657 < ra_free < 658

    def layer_ra(d_mm, dt, t_mean_k, nu, alpha):
        return 9.81 * (1.0 / t_mean_k) * dt * (d_mm / 1000.0) ** 3 / (nu * alpha)

    ra_8 = layer_ra(8, 10, 283.15, 1.43e-5, 2.0e-5)
    ra_12 = layer_ra(12, 10, 283.15, 1.43e-5, 2.0e-5)
    ra_20 = layer_ra(20, 10, 283.15, 1.43e-5, 2.0e-5)
    assert 500 < ra_8 < 750
    assert 1708 < ra_12 < 2500
    assert 9000 < ra_20 < 10500

    css = _anim_defs(
        ["anim-roll"],
        [("rollUp", "0% { stroke-dashoffset: 140; opacity: 0.25; } 100% { stroke-dashoffset: 0; opacity: 1; }")],
    )

    els = []
    els.extend(
        header(
            "为什么一加热不一定马上对流？浮力要赢过黏性和热扩散",
            "1900 年贝纳德看见六角形对流胞，1916 年瑞利算出那道看不见的门槛：Ra ≈ 1708。",
        )
    )

    els.append(card(20, 66, 352, 396))
    els.append(step_badge(38, 88, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 92, "同一层空气，两种截然不同的传热状态", size=12.0, color=INK, weight="700"))

    els.append('<rect x="38" y="108" width="316" height="120" rx="7" fill="#f5f9fc" stroke="#d7e6f2"/>')
    els.append('<rect x="44" y="112" width="304" height="10" rx="3" fill="#f2b880"/>')
    els.append('<rect x="44" y="214" width="304" height="10" rx="3" fill="#9fc7e8"/>')
    for yy in (138, 158, 178, 198):
        els.append(_line(46, yy, 346, yy, stroke=BLUE_LINE, sw=1.1))
    els.append(txt(52, 236, "下热上冷，但 Ra < 1708：空气静止，热量只靠传导穿过", size=9.9, color=BLUE, weight="600"))

    els.append('<rect x="38" y="242" width="316" height="130" rx="7" fill="#fff8f2" stroke="#f0d5bc"/>')
    els.append('<rect x="44" y="246" width="304" height="10" rx="3" fill="#f2b880"/>')
    els.append('<rect x="44" y="360" width="304" height="10" rx="3" fill="#9fc7e8"/>')
    els.append('<g class="anim-roll">')
    for cx in (110, 200, 290):
        els.append(
            f'<path d="M {cx-34} 336 C {cx-46} 286, {cx+46} 286, {cx+34} 336" '
            'fill="none" stroke="#c25014" stroke-width="2.2" stroke-dasharray="8 6" marker-end="url(#arr-orange)"/>'
        )
        els.append(
            f'<path d="M {cx+34} 270 C {cx+46} 316, {cx-46} 316, {cx-34} 270" '
            'fill="none" stroke="#1d6fa5" stroke-width="2.2" stroke-dasharray="8 6" marker-end="url(#arr-blue)"/>'
        )
    els.append("</g>")
    els.append(txt(52, 378, "Ra > 1708：浮力压过阻尼，自发卷成规则对流胞（六角／条带）", size=9.9, color=ORANGE, weight="600"))
    els.append(txt(38, 406, "控制变量只有三个：温差 ΔT、层厚 d、流体物性（ν、α、β）。", size=10.4, color=BODY))
    els.append(txt(38, 428, "加大温差或层厚 ⇒ Ra 暴涨；黏性、热扩散是稳定器。", size=10.4, color=INK, weight="600"))

    els.append(card(388, 66, 352, 396))
    els.append(step_badge(406, 88, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 92, "瑞利数：浮力与阻尼的“拔河比分”", size=12.0, color=INK, weight="700"))

    els.append(txt(404, 124, "Ra = gβ·ΔT·d³ / (ν·α)", size=12.4, color=INK, weight="700"))
    els.append(txt(404, 146, "分子＝浮力驱动力；分母＝黏性阻尼 × 热抹平速度", size=10.2, color=SLATE))
    els.append(txt(404, 170, "注意 d³：层厚翻倍，浮力效应涨 8 倍！", size=10.6, color=ORANGE, weight="600"))
    els.append(_line(404, 184, 724, 184, stroke=BORDER, sw=1))

    els.append(txt(404, 208, "临界值（上下恒温平板，下热上冷）", size=11.0, color=BLUE, weight="700"))
    els.append(txt(404, 232, "上下刚壁、无滑移：Ra_c ≈ 1708", size=10.8, color=INK))
    els.append(txt(404, 253, f"上下自由滑移：Ra_c = 27π⁴/4 ≈ {ra_free:.1f}", size=10.8, color=INK))
    els.append(txt(404, 276, "刚壁摩擦更强，门槛更高；上下都加热反而更稳。", size=10.0, color=SLATE))
    els.append(_line(404, 290, 724, 290, stroke=BORDER, sw=1))

    els.append(txt(404, 314, "实战：中空玻璃的空气层能有多厚？", size=11.0, color=PURPLE, weight="700"))
    els.append(txt(404, 335, "取 ΔT=10 K、平均 10°C；", size=10.0, color=SLATE))
    els.append(txt(404, 352, "ν≈1.43×10⁻⁵，α≈2.0×10⁻⁵ m²/s", size=10.0, color=SLATE))
    els.append(txt(404, 374, f"间隙 8 mm ⇒ Ra ≈ {ra_8:.0f} < 1708：近似纯传导", size=10.6, color=GREEN, weight="600"))
    els.append(txt(404, 395, f"间隙 12 mm ⇒ Ra ≈ {ra_12:.0f} ＞ 1708：对流启动", size=10.6, color=ORANGE, weight="600"))
    els.append(txt(404, 416, f"间隙 20 mm ⇒ Ra ≈ {ra_20:.0f}：对流更强，隔热反变差", size=10.6, color=ORANGE, weight="600"))
    els.append(txt(404, 444, "所以空气层不是越厚越保温：越过临界值就“漏热”。", size=10.6, color=PURPLE, weight="700"))

    els.append(card(20, 474, 720, 40, fill="#f1f5f9", stroke=BORDER))
    ticks = [(100, "10²"), (250, "10³"), (400, "10⁴"), (550, "10⁵"), (700, "10⁶")]
    for xpos, label in ticks:
        els.append(_line(xpos, 492, xpos, 500, stroke=SLATE, sw=1))
        els.append(txt(xpos, 512, label, size=9.6, color=MUTED, anchor="middle"))
    els.append(_line(100, 496, 700, 496, stroke=SLATE, sw=1.6))
    x_crit = 100 + (math.log10(1708) - 2) / 4 * 600
    els.append(_line(x_crit, 486, x_crit, 506, stroke=ORANGE, sw=2))
    els.append(txt(x_crit + 6, 488, "Ra_c≈1708：传导 → 对流", size=10.0, color=ORANGE, weight="700"))
    els.append(txt(108, 486, "稳定传导区", size=10.0, color=BLUE, weight="600"))
    els.append(txt(520, 486, "对流／湍流区", size=10.0, color=ORANGE, weight="600"))

    return figure(
        524,
        "瑞利–贝纳德对流的临界瑞利数与中空玻璃算例图",
        "下热上冷的空气层在瑞利数小于约1708时保持静止传导，超过1708后浮力克服黏性和热扩散形成对流胞；自由边界临界值27π的四次方除以4约657.5；中空玻璃间隙8毫米时瑞利数约620近似纯传导，12毫米约2092开始对流，20毫米约9700对流更强反而更漏热。",
        els,
        extra_css=css,
    )


# ---------------------------------------------------------------------------
# 4. 房间循环与烟囱效应
# ---------------------------------------------------------------------------
def build_room_and_stack() -> str:
    p_atm, g_earth, r_air = 101325.0, 9.81, 287.0
    t_in, t_out, height = 293.15, 278.15, 30.0
    dp = p_atm * g_earth * height / r_air * (1.0 / t_out - 1.0 / t_in)
    assert 18.0 < dp < 20.5

    els = []
    els.extend(
        header(
            "同一条浮力链：在房间里转成圈，在烟囱里变成抽力",
            "热空气上升不是终点；它必须找地方冷却、下沉，循环才闭合。",
        )
    )

    els.append(card(20, 66, 424, 392))
    els.append(step_badge(38, 88, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 92, "房间里的闭合环流：暖气为什么装低处", size=12.0, color=INK, weight="700"))

    els.append('<rect x="44" y="112" width="376" height="286" rx="6" fill="#f8fbfe" stroke="#b9cfe0" stroke-width="1.5"/>')
    els.append('<rect x="58" y="140" width="28" height="84" rx="3" fill="#dbeafe" stroke="#60a5fa" stroke-width="1.3"/>')
    els.append(txt(72, 240, "冷窗", size=9.8, color=BLUE, anchor="middle", weight="600"))
    els.append(_line(66, 160, 66, 206, stroke=BLUE, sw=1.6, marker="arr-blue"))
    els.append(txt(72, 262, "玻璃降温", size=9.6, color=BLUE, anchor="middle"))
    els.append(txt(72, 278, "冷气下沉", size=9.6, color=BLUE, anchor="middle"))

    els.append('<rect x="100" y="344" width="72" height="28" rx="4" fill="#f9d7b5" stroke="#c25014" stroke-width="1.5"/>')
    for xx in (110, 124, 138, 152):
        els.append(_line(xx, 350, xx, 366, stroke=ORANGE, sw=1.2))
    els.append(txt(136, 388, "暖气片", size=9.8, color=ORANGE, anchor="middle", weight="600"))

    els.append('<path d="M 138 336 C 140 290, 156 230, 190 196" fill="none" stroke="#c25014" stroke-width="2.4" marker-end="url(#arr-orange)"/>')
    els.append('<path d="M 196 186 C 268 154, 344 168, 388 204" fill="none" stroke="#c25014" stroke-width="2.4" marker-end="url(#arr-orange)"/>')
    els.append('<path d="M 396 216 C 412 252, 404 308, 372 338" fill="none" stroke="#1d6fa5" stroke-width="2.4" marker-end="url(#arr-blue)"/>')
    els.append('<path d="M 362 350 C 300 374, 220 374, 180 368" fill="none" stroke="#1d6fa5" stroke-width="2.4" marker-end="url(#arr-blue)"/>')
    els.append(txt(228, 162, "顶部最热", size=10.2, color=ORANGE, anchor="middle", weight="600"))
    els.append(txt(320, 300, "贴墙冷却后下沉", size=10.0, color=BLUE, anchor="middle"))
    els.append(txt(248, 326, "地板附近回流", size=10.0, color=BLUE, anchor="middle"))

    els.append(txt(40, 424, "• 暖气片放窗下：刚下沉的冷气立刻被加热，循环带动整屋", size=10.2, color=BODY))
    els.append(txt(40, 445, "• 夏季风扇只是搅动空气；它不制冷，靠加速蒸发与撕薄气膜", size=10.2, color=BODY))

    els.append(card(460, 66, 280, 392))
    els.append(step_badge(478, 88, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(496, 92, "烟囱效应：高度就是抽力", size=12.0, color=INK, weight="700"))

    els.append('<rect x="636" y="128" width="46" height="242" rx="3" fill="#f5f8fb" stroke="#94a3b8" stroke-width="1.6"/>')
    els.append(_line(659, 352, 659, 152, stroke=ORANGE, sw=2.6, marker="arr-orange"))
    els.append(_line(608, 364, 632, 352, stroke=BLUE, sw=2, marker="arr-blue"))
    els.append(_line(710, 364, 686, 352, stroke=BLUE, sw=2, marker="arr-blue"))
    els.append(txt(659, 120, "热烟气上升", size=10.2, color=ORANGE, anchor="middle", weight="600"))
    els.append(txt(659, 392, "底部补入冷空气", size=9.8, color=BLUE, anchor="middle"))
    els.append(_line(616, 254, 634, 254, stroke=MUTED, sw=1, dash="4 4"))
    els.append(txt(608, 250, "中性面", size=9.4, color=MUTED, anchor="end"))

    els.append(txt(476, 208, "Δp = (ρ外−ρ内)·g·h", size=11.4, color=INK, weight="700"))
    els.append(txt(476, 230, "≈ (p·g·h/R)·(1/T外−1/T内)", size=10.6, color=BLUE))
    els.append(txt(476, 254, "取 h=30 m、ΔT=15 K：", size=10.0, color=SLATE))
    els.append(txt(476, 278, f"Δp ≈ {dp:.0f} Pa（NIST 公式）", size=11.6, color=ORANGE, weight="700"))
    els.append(txt(476, 304, "越高、内外温差越大，抽力越强。", size=10.2, color=BODY))
    els.append(txt(476, 329, "中性面以上室内向外漏风，", size=10.2, color=BODY))
    els.append(txt(476, 349, "以下则室外空气从缝隙灌入。", size=10.2, color=BODY))
    els.append(txt(476, 382, "火场烟气、老式烟囱、高层建筑", size=9.8, color=MUTED))
    els.append(txt(476, 401, "的“拔风”，全是这一条公式。", size=9.8, color=MUTED))

    els.append(card(20, 470, 720, 36, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 494, "房间示意只画出一个主环流；真实房间会被门窗、家具、热源位置撕成多个涡。", size=10.6, color=SLATE))

    return figure(
        516,
        "室内自然对流环流与烟囱效应压差图",
        "暖气片装在冷窗下加热下沉气流形成房间闭合环流，顶部热空气向冷墙流动后下沉；烟囱效应压差约为室外密度减室内密度乘重力加速度乘高度，取高30米室内20摄氏度室外5摄氏度算得约19帕，中性面之上室内向外漏风、之下室外向内补风。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 从海陆风到三圈环流
# ---------------------------------------------------------------------------
def build_earth_circulation() -> str:
    lats = [-90, -60, -30, 0, 30, 60, 90]
    assert lats[0] < lats[1] < lats[2] < lats[3] < lats[4] < lats[5] < lats[6]

    els = []
    els.extend(
        header(
            "从海边到整个地球：同一个浮力引擎，被自转掰成三圈",
            "海陆风是“小尺度热机”，哈德利环流是“行星尺度热机”；引擎相同，边界条件不同。",
        )
    )

    def sea_cell(x0, daytime):
        land_x, sea_x = x0 + 95, x0 + 245
        warm_x = land_x if daytime else sea_x
        cool_x = sea_x if daytime else land_x
        els.append(card(x0, 66, 352, 190))
        els.append(step_badge(x0 + 18, 88, 1 if daytime else 2, fg=ORANGE if daytime else BLUE, bg=ORANGE_SOFT if daytime else BLUE_SOFT))
        els.append(txt(x0 + 36, 92, "白天：海风（海洋 → 陆地）" if daytime else "夜晚：陆风（陆地 → 海洋）", size=11.8, color=INK, weight="700"))
        els.append(f'<rect x="{x0+40}" y="124" width="110" height="26" rx="3" fill="#f3d5ae" stroke="#d3a267"/>')
        els.append(f'<rect x="{x0+190}" y="124" width="110" height="26" rx="3" fill="#cfe4f5" stroke="#78a9d2"/>')
        els.append(txt(land_x, 142, "陆地", size=10.2, color=ORANGE, anchor="middle", weight="700"))
        els.append(txt(sea_x, 142, "海洋", size=10.2, color=BLUE, anchor="middle", weight="700"))

        els.append(_line(warm_x, 120, warm_x, 96, stroke=ORANGE, sw=2.2, marker="arr-orange"))
        upper_from = warm_x + (12 if warm_x < cool_x else -12)
        upper_to = cool_x + (-12 if warm_x < cool_x else 12)
        els.append(_line(upper_from, 98, upper_to, 98, stroke=ORANGE, sw=2.0, marker="arr-orange"))
        els.append(_line(cool_x, 116, cool_x, 152, stroke=BLUE, sw=2.0, marker="arr-blue"))
        surface_from = cool_x + (-18 if warm_x > cool_x else 18)
        surface_to = warm_x + (18 if warm_x > cool_x else -18)
        els.append(_line(surface_from, 164, surface_to, 164, stroke=BLUE, sw=2.2, marker="arr-blue"))
        if daytime:
            els.append(txt(x0 + 176, 188, "陆地升温快 → 空气上升 → 海面冷湿空气登陆", size=10.0, color=SLATE, anchor="middle"))
            els.append(txt(x0 + 176, 222, "近地面风来自：海洋（海风）", size=10.4, color=INK, anchor="middle", weight="700"))
        else:
            els.append(txt(x0 + 176, 188, "陆地降温快 → 海洋相对暖 → 空气从陆地吹向海面", size=10.0, color=SLATE, anchor="middle"))
            els.append(txt(x0 + 176, 222, "近地面风来自：陆地（陆风）", size=10.4, color=INK, anchor="middle", weight="700"))

    sea_cell(20, True)
    sea_cell(388, False)

    els.append(card(20, 272, 720, 216))
    els.append(step_badge(38, 294, 3, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 298, "行星尺度：无自转时每半球一个环流圈；真实地球被科里奥利效应拆成三圈", size=11.8, color=INK, weight="700"))

    x0, span = 70, 620
    def lat_x(lat):
        return x0 + (lat + 90) / 180 * span

    els.append(_line(x0, 346, x0 + span, 346, stroke=SLATE, sw=1.6))
    for lat in lats:
        xx = lat_x(lat)
        els.append(_line(xx, 342, xx, 352, stroke=SLATE, sw=1))
        els.append(txt(xx, 366, f"{lat}°", size=9.8, color=MUTED, anchor="middle"))
    els.append(txt(x0 + span / 2, 386, "赤道：受热最强，空气上升 → 低压多雨", size=10.4, color=ORANGE, anchor="middle", weight="600"))

    for left, right, color, marker in [
        (-30, 0, ORANGE, "arr-orange"),
        (0, 30, ORANGE, "arr-orange"),
        (30, 60, BLUE, "arr-blue"),
        (60, 90, BLUE, "arr-blue"),
        (-60, -30, BLUE, "arr-blue"),
        (-90, -60, BLUE, "arr-blue"),
    ]:
        els.append(_line(lat_x(left), 334, lat_x(right), 334, stroke=color, sw=2.0, marker=marker))

    els.append(_line(lat_x(0), 346, lat_x(0), 326, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    els.append(txt(lat_x(0), 320, "赤道上升", size=10.0, color=ORANGE, anchor="middle", weight="700"))
    els.append(_line(lat_x(30), 324, lat_x(30), 346, stroke=BLUE, sw=2.4, marker="arr-blue"))
    els.append(txt(lat_x(30), 320, "30° 下沉 → 干燥带", size=9.8, color=BLUE, anchor="middle", weight="600"))
    els.append(_line(lat_x(60), 346, lat_x(60), 326, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    els.append(txt(lat_x(60), 320, "60° 上升", size=9.8, color=ORANGE, anchor="middle", weight="600"))

    els.append(txt(40, 410, "哈德利圈（低纬）", size=10.4, color=ORANGE, weight="700"))
    els.append(txt(214, 410, "费雷尔圈（中纬）", size=10.4, color=BLUE, weight="700"))
    els.append(txt(392, 410, "极地圈（高纬）", size=10.4, color=PURPLE, weight="700"))
    els.append(txt(560, 410, "示意图：垂直尺度夸大，不代表真实比例", size=9.8, color=MUTED))
    els.append(txt(40, 470, "NOAA：若无地球自转与海陆差异，每半球只需一个简单环流圈就能把热量从赤道搬到极地。", size=10.4, color=BODY))

    return figure(
        500,
        "海陆风昼夜反转与地球三圈环流示意图",
        "白天陆地升温快空气上升，海面冷空气登陆形成海风；夜晚陆地降温快，空气从陆地吹向海洋形成陆风；全球尺度上赤道上升、30度附近下沉、60度附近上升、极地下沉，受地球自转影响每半球形成哈德利圈、费雷尔圈和极地圈三个环流。",
        els,
    )


@register(TOPIC, "空气对流的浮力、边界层、瑞利数与大气环流原理原创图解", "physics")
def build_all() -> None:
    builders = [
        ("buoyancy-origin-and-microgravity.svg", build_buoyancy_origin),
        ("boundary-layer-warm-plate.svg", build_boundary_layer),
        ("rayleigh-benard-onset.svg", build_rayleigh_onset),
        ("room-circulation-and-stack-effect.svg", build_room_and_stack),
        ("sea-breeze-and-global-cells.svg", build_earth_circulation),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
