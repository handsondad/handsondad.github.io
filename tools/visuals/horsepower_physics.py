"""Visuals for '1马力真的等于一匹马的力气吗' (horsepower-physics).

Generates 5 original 760px Chinese SVG diagrams with mathematical assertions:
1. watt-mill-wheel-origin.svg        — Watt's 1782–1783 mill-wheel & pulley derivation (745.7 W)
2. horse-human-burst-vs-sustained.svg— Peak 5s burst (14.9 hp) vs 8h sustained output (Nature 1993)
3. power-lifting-race-anim.svg       — Time-accurate CSS hoist race (same 75 kg / 2942 J, 0.25 vs 1 vs 3 PS)
4. torque-power-ev-ice.svg           — Torque vs Power curves (200 kW EV vs 2.0T ICE, P = T*n/9549)
5. horsepower-family-and-drag-cube.svg— hp / PS / AC '1匹' conversions + aerodynamic P_drag ∝ v³ wall
"""

from __future__ import annotations

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
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "horsepower-physics"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#ecfdf5"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"

# Exact physical & metrological constants (NIST SP 811 / BIPM SI)
FT_M = 0.3048
LB_KG = 0.45359237
G_STD = 9.80665
HP_IMPERIAL_W = 550.0 * FT_M * LB_KG * G_STD  # 745.6998715822702 W
PS_METRIC_W = 75.0 * G_STD  # 735.49875 W
HP_ELECTRIC_W = 746.0


def verify_horsepower_math() -> None:
    """Assert exact metrological, historical, and mechanical calculations."""
    # 1. Watt's August 1782 Blotting & Calculation Book arithmetic
    d_ft = 24.0
    rpm_mill = 2.5
    pull_lbf = 180.0
    watt_pi3 = d_ft * 3.0 * rpm_mill * pull_lbf
    watt_exact_pi = d_ft * math.pi * rpm_mill * pull_lbf
    assert watt_pi3 == 32400.0
    assert abs(watt_exact_pi - 33929.20) < 0.05
    assert 33000.0 / 60.0 == 550.0

    # 2. Imperial hp & Metric PS exact SI conversions (NIST SP 811)
    assert abs(HP_IMPERIAL_W - 745.69987) < 1e-4
    assert abs(PS_METRIC_W - 735.49875) < 1e-5
    assert abs(HP_IMPERIAL_W / PS_METRIC_W - 1.0138697) < 1e-5

    # 3. Hoist race physics: m = 75 kg, Δh = 4.0 m -> F = 735.49875 N, W = 2941.995 J
    f_n = 75.0 * G_STD
    dh = 4.0
    work_j = f_n * dh
    assert abs(work_j - 2941.995) < 1e-2
    for ps_val, expected_t in [(0.25, 16.0), (1.0, 4.0), (3.0, 4.0 / 3.0)]:
        p_w = ps_val * PS_METRIC_W
        v_ms = p_w / f_n
        t_real = dh / v_ms
        assert abs(t_real - expected_t) < 1e-9

    # 4. Rotational power constant: P[kW] = T[N·m] * n[rpm] / 9549.2965855
    rot_k = 60.0 * 1000.0 / (2.0 * math.pi)
    assert abs(rot_k - 9549.2966) < 1e-3
    # EV base speed where 400 N·m reaches 200 kW:
    n_base = 200.0 * rot_k / 400.0
    assert abs(n_base - 4774.65) < 0.1

    # 5. Aerodynamic cubic scaling: doubling speed multiplies drag power by 8x
    def drag_kw(v_kmh: float) -> float:
        v = v_kmh / 3.6
        return 0.5 * 1.225 * 0.28 * 2.2 * (v ** 3) / 1000.0

    assert abs(drag_kw(200.0) / drag_kw(100.0) - 8.0) < 1e-9
    assert abs(drag_kw(400.0) / drag_kw(100.0) - 64.0) < 1e-9


# ---------------------------------------------------------------------------
# 图 1：瓦特 1782–1783 年怎么算出“1 马力”
# ---------------------------------------------------------------------------
def build_watt_mill_wheel() -> str:
    els = header(
        "图 1 · 瓦特怎么算出“1 马力”：从 24 英尺磨坊转轮到 550 英尺·磅力/秒",
        "1782–1783 年瓦特计算簿手稿：把客户熟悉的挽马绕圈换算成蒸汽机统一定价标尺",
    )

    # 左栏：1782 磨坊转轮俯视几何图
    els.append(card(20, 64, 352, 252, fill=CARD_BG, stroke=BORDER))
    els.append(pill(32, 76, "① 1782.8 造纸磨坊木匠 Wrigley 的实测账", fg=BLUE, bg=BLUE_SOFT, w=264))

    cx, cy, r_wheel = 100, 200, 52
    els.append(f'<circle cx="{cx}" cy="{cy}" r="{r_wheel}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="5,4"/>')
    els.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.4"/>')
    # 横向直径标注
    els.append(f'<line x1="{cx - r_wheel}" y1="{cy}" x2="{cx + r_wheel}" y2="{cy}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3,3"/>')
    els.append(txt(cx, cy + 16, "直径 D = 24 ft", 11, MUTED, "middle", halo=True))
    els.append(txt(cx, cy + 32, "每分钟走 2.5 圈", 11, BLUE, "middle", weight="600", halo=True))
    # 垂直连杆 + 顶部挽马节点 + 切向拉力箭头
    els.append(f'<line x1="{cx}" y1="{cy - 8}" x2="{cx}" y2="{cy - r_wheel}" stroke="{INK}" stroke-width="2"/>')
    els.append(f'<circle cx="{cx}" cy="{cy - r_wheel}" r="5.5" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')
    els.append(
        f'<line x1="{cx + 6}" y1="{cy - r_wheel}" x2="{cx + 66}" y2="{cy - r_wheel}" '
        f'stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>'
    )
    els.append(txt(cx + 12, cy - r_wheel - 12, "切向拉力 180 lbf", 11, ORANGE, "middle", weight="700"))

    # 右侧分步算式
    rx = 198
    els.append(txt(rx, 138, "瓦特手稿按 π ≈ 3 粗算：", 11.5, INK, weight="700"))
    els.append(txt(rx, 159, "路程 = 24 × 3 × 2.5", 11.5, BODY))
    els.append(txt(rx, 178, "     = 180 ft / min", 11.5, BLUE, weight="700"))
    els.append(txt(rx, 200, "做功 = 180 × 180 lbf", 11.5, BODY))
    els.append(txt(rx, 219, "     = 32,400 ft·lbf/min", 11.5, ORANGE, weight="700"))
    els.append(txt(rx, 241, "（若按真 π 算为 33,929）", 11, MUTED))

    els.append(card(32, 268, 328, 36, rx=7, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(196, 291, "1783.9 凑成 60 的整倍数：33,000 ft·lbf/min", 11.5, INK, "middle", weight="700"))

    # 右栏：等效滑轮吊重 + 现代国际单位制精确换算
    els.append(card(388, 64, 352, 252, fill=CARD_BG, stroke=BORDER))
    els.append(pill(400, 76, "② 等效滑轮吊重定义（1 英制马力 hp）", fg=GREEN, bg=GREEN_SOFT, w=258))

    # 简易定滑轮与重物
    px, py = 456, 130
    els.append(f'<line x1="422" y1="108" x2="490" y2="108" stroke="{SLATE}" stroke-width="3"/>')
    els.append(f'<line x1="{px}" y1="108" x2="{px}" y2="{py}" stroke="{SLATE}" stroke-width="2"/>')
    els.append(f'<circle cx="{px}" cy="{py}" r="14" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>')
    els.append(f'<circle cx="{px}" cy="{py}" r="3" fill="{GREEN}"/>')
    # 左侧牵引绳、右侧吊重绳
    els.append(f'<line x1="{px - 14}" y1="{py}" x2="412" y2="172" stroke="{INK}" stroke-width="1.6"/>')
    els.append(f'<path d="M422 162 L406 178" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
    els.append(f'<line x1="{px + 14}" y1="{py}" x2="{px + 14}" y2="196" stroke="{INK}" stroke-width="1.6"/>')
    els.append(card(px - 12, 196, 52, 40, rx=5, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.4))
    els.append(txt(px + 14, 214, "550 lbf", 11.5, ORANGE, "middle", weight="700"))
    els.append(txt(px + 14, 230, "≈249.5kg", 10.5, BODY, "middle"))
    # 上升 1 ft / 1 s 箭头
    els.append(f'<line x1="506" y1="234" x2="506" y2="196" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#arr-green)"/>')
    els.append(txt(460, 255, "1 秒匀速拎高 1 英尺 (0.3048 m)", 11, GREEN, "middle", weight="700"))

    # 右侧精确 SI 换算链
    sx = 538
    els.append(txt(sx, 128, "折合每秒：550 ft·lbf / s", 11.5, INK, weight="700"))
    els.append(txt(sx, 150, "• 1 ft = 0.3048 m", 11, BODY))
    els.append(txt(sx, 170, "• 1 lb = 0.45359237 kg", 11, BODY))
    els.append(txt(sx, 190, "• gₙ = 9.80665 m/s²", 11, BODY))
    els.append(card(sx - 4, 204, 192, 48, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.2))
    els.append(txt(sx + 92, 224, f"1 hp = {HP_IMPERIAL_W:.2f} W", 13, GREEN, "middle", weight="700"))
    els.append(txt(sx + 92, 243, "每秒输出约 745.7 焦耳机械功", 11, BODY, "middle"))

    els.append(card(400, 268, 328, 36, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
    els.append(txt(564, 291, "比普通马 8 小时均值高约 50%：宁可多给绝不虚标", 11.5, ORANGE, "middle", weight="700"))

    # 底部通栏：商业洞察
    els.append(card(20, 328, 720, 48, fill=BLUE_SOFT, stroke=BLUE))
    els.append(
        txt(
            36,
            357,
            "商业算盘：真马干 6–8 小时就得歇班，蒸汽机却 24 小时连轴转——三班倒矿井里 1 台 10 马力机器能顶 20–30 匹真马！",
            11.5,
            INK,
            weight="600",
        )
    )

    return figure(
        390,
        "瓦特定义1英制马力的历史推算与国际单位制745.7瓦换算图解",
        "左栏展示1782年木匠Wrigley提供的24英尺直径磨坊转轮参数，挽马以180磅力每分钟走2.5圈，瓦特取圆周率约为3算得32400并在1783年定为33000英尺磅每分钟；右栏展示等效每秒将550磅重物提升1英尺，精确折合745.70瓦特。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 2：一匹真马到底有几马力？（短时爆发 vs 全天持续功率谱）
# ---------------------------------------------------------------------------
def build_burst_vs_sustained() -> str:
    els = header(
        "图 2 · 一匹真马到底有几马力？5 秒极限爆发与 8 小时轮班差出十几倍",
        "数据核查：1925 爱荷华州博览会测功车实测（Nature, 1993）对比人类运动生理学输出",
    )

    els.append(card(20, 64, 720, 276, fill=CARD_BG, stroke=BORDER))

    x0 = 228.0
    max_hp = 16.0
    bar_span = 416.0  # 1 hp = 26.0 px
    scale = bar_span / max_hp

    # 1.0 hp 垂直基准虚线
    x_one = x0 + 1.0 * scale
    els.append(f'<line x1="{x_one:.1f}" y1="88" x2="{x_one:.1f}" y2="306" stroke="{PURPLE}" stroke-width="1.4" stroke-dasharray="4,3"/>')
    els.append(txt(x_one + 6, 86, "瓦特 1 hp 基准线 (745.7 W)", 11, PURPLE, weight="700"))

    rows = [
        ("挽马 · 5 秒极限爆发", 14.9, "14.9 hp (≈11.1 kW)", ORANGE, ORANGE_SOFT),
        ("奥运车手 · 5 秒冲刺", 2.7, "≈2.7 hp (≈2.0 kW)", AMBER, AMBER_SOFT),
        ("瓦特标准 · 1 英制马力", 1.0, "1.00 hp (745.7 W)", PURPLE, PURPLE_SOFT),
        ("普通挽马 · 8 小时轮班", 0.75, "0.67–1.0 hp (500–746 W)", BLUE, BLUE_SOFT),
        ("环法车手 · 1 小时骑行", 0.54, "≈0.54 hp (≈400 W)", GREEN, GREEN_SOFT),
        ("普通成人 · 日常持续劳作", 0.134, "≈0.13 hp (≈100 W)", SLATE, SLATE_SOFT),
    ]

    for idx, (label, hp_val, val_str, col, soft) in enumerate(rows):
        y = 100 + idx * 34
        els.append(txt(216, y + 15, label, 12, BODY, "end", weight="600"))
        els.append(f'<rect x="{x0:.1f}" y="{y}" width="{bar_span:.1f}" height="20" rx="5" fill="{BG}" stroke="{BORDER}" stroke-width="0.8"/>')
        w = max(4.0, hp_val * scale)
        if idx == 3:
            # 展示 0.67..1.0 hp 区间带
            w_min = 0.67 * scale
            w_max = 1.00 * scale
            els.append(f'<rect x="{x0:.1f}" y="{y}" width="{w_max:.1f}" height="20" rx="5" fill="{soft}" stroke="{col}" stroke-width="1.2"/>')
            els.append(f'<rect x="{x0:.1f}" y="{y}" width="{w_min:.1f}" height="20" rx="5" fill="{col}"/>')
            tx = x0 + w_max + 10
        else:
            els.append(f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="20" rx="5" fill="{col}"/>')
            tx = x0 + w + 10
        # 第一行条很长，把数值写在右侧空白内或条末
        if tx > 590:
            els.append(txt(x0 + w - 10, y + 15, val_str, 11.5, "#ffffff", "end", weight="700"))
        else:
            els.append(txt(tx, y + 15, val_str, 11.5, col, "start", weight="700"))

    # 横轴刻度 0..16 hp
    y_axis = 312
    els.append(f'<line x1="{x0:.1f}" y1="{y_axis}" x2="{x0 + bar_span:.1f}" y2="{y_axis}" stroke="{SLATE}" stroke-width="1"/>')
    for tick in range(0, 17, 2):
        xt = x0 + tick * scale
        els.append(f'<line x1="{xt:.1f}" y1="{y_axis}" x2="{xt:.1f}" y2="{y_axis + 5}" stroke="{SLATE}" stroke-width="1"/>')
        els.append(txt(xt, y_axis + 19, f"{tick} hp", 10.5, MUTED, "middle"))

    # 底部生理机制说明栏
    els.append(card(20, 348, 720, 40, fill=GREEN_SOFT, stroke=GREEN))
    els.append(
        txt(
            36,
            373,
            "生理分水岭：5 秒爆发烧肌肉现存磷酸肌酸与无氧糖酵解；8 小时轮班受心肺供氧限制，只能靠有氧呼吸稳态供能。",
            11.5,
            INK,
            weight="600",
        )
    )

    return figure(
        400,
        "真实马匹与人类的短时爆发功率和长时间持续功率对比图",
        "按0至16马力线性比例对比：挽马5秒极限爆发高达14.9马力（11.1千瓦），奥运车手5秒冲刺约2.7马力，瓦特1马力标准为1.00马力（745.7瓦），普通挽马8小时持续工作约0.67至1.0马力，环法车手1小时约0.54马力，普通成人日常持续约0.13马力。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 3：功、力与功率的时间竞速动画（同吊 75 kg 升 4 m，按距离÷速度真实比例计时）
# ---------------------------------------------------------------------------
def build_power_lifting_race_anim() -> str:
    # 物理模型：三台卷扬机匀速吊起完全相同的 m = 75 kg 重物（拉力 F = 735.5 N 完全相等！）
    # 升高 Δh = 4.0 m（总做功 W = 2,942 J 完全相等！）
    # 功率分别为 0.25 PS (v=0.25 m/s, 真实 16.0 s)、1.0 PS (v=1.0 m/s, 真实 4.0 s)、3.0 PS (v=3.0 m/s, 真实 1.33 s)
    # 动画时间严格按 4x 倍速缩放：4.00 s : 1.00 s : 0.333 s（保持 12 : 3 : 1 严格物理比例）
    dy_px = 124.0  # y_start = 258 (0 m) -> y_top = 134 (4.0 m)
    delay = 0.55

    extra_css = f"""
  @keyframes liftCrate {{
    from {{ transform: translateY({dy_px:.1f}px); }}
    to   {{ transform: translateY(0px); }}
  }}
  @keyframes badgePop {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
  }}
  .crate-a {{ animation: liftCrate 4.00s linear {delay}s 1 backwards; }}
  .crate-b {{ animation: liftCrate 1.00s linear {delay}s 1 backwards; }}
  .crate-c {{ animation: liftCrate 0.333s linear {delay}s 1 backwards; }}
  .done-a  {{ animation: badgePop 0.25s ease-out {delay + 4.00:.2f}s 1 backwards; }}
  .done-b  {{ animation: badgePop 0.25s ease-out {delay + 1.00:.2f}s 1 backwards; }}
  .done-c  {{ animation: badgePop 0.25s ease-out {delay + 0.333:.2f}s 1 backwards; }}
  @media (prefers-reduced-motion: reduce) {{
    .crate-a, .crate-b, .crate-c, .done-a, .done-b, .done-c {{ animation: none !important; }}
  }}
"""

    els = header(
        "图 3 · “力气一样大”为什么“马力差 12 倍”？同吊 75 kg 升 4 米的时间竞速",
        "三根绳子拉力同为 735.5 N、总做功同为 2,942 J；动画按 4 倍速真实比例播放一次并停在终点",
    )

    # 左侧吊装井道区（用 clipPath 让钢索在滑轮 y=122 处真实收卷，不向上穿出顶梁）
    els.append(
        '<defs><clipPath id="hoist-shaft-clip">'
        '<rect x="70" y="122" width="380" height="170"/>'
        '</clipPath></defs>'
    )
    els.append(card(20, 64, 444, 266, fill=CARD_BG, stroke=BORDER))
    y_top = 134
    y_bot = int(y_top + dy_px)  # 258

    # 高度标尺线 4.0 m 与 0 m
    els.append(f'<line x1="74" y1="{y_top}" x2="444" y2="{y_top}" stroke="{GREEN}" stroke-width="1.2" stroke-dasharray="5,4"/>')
    els.append(f'<line x1="74" y1="{y_bot + 30}" x2="444" y2="{y_bot + 30}" stroke="{SLATE}" stroke-width="1.4"/>')
    els.append(txt(68, y_top + 4, "4.0 m", 11, GREEN, "end", weight="700"))
    els.append(txt(68, y_bot + 28, "0.0 m", 11, MUTED, "end"))

    lanes = [
        (134, "A · 人力手摇", "0.25 PS", "v = 0.25 m/s", "16.0 s 到顶", SLATE, SLATE_SOFT, "crate-a", "done-a"),
        (256, "B · 1 匹电机", "1.0 PS", "v = 1.00 m/s", "4.0 s 到顶", BLUE, BLUE_SOFT, "crate-b", "done-b"),
        (378, "C · 3 匹卷扬", "3.0 PS", "v = 3.00 m/s", "1.33 s 到顶", ORANGE, ORANGE_SOFT, "crate-c", "done-c"),
    ]

    for cx, title_s, p_s, v_s, t_s, col, soft, c_cls, d_cls in lanes:
        els.append(txt(cx, 86, title_s, 12, INK, "middle", weight="700"))
        els.append(txt(cx, 103, f"{p_s} ({v_s})", 10.5, col, "middle", weight="600"))
        # 顶梁滑轮
        els.append(f'<circle cx="{cx}" cy="118" r="6" fill="{soft}" stroke="{col}" stroke-width="1.5"/>')
        # 静态起点虚线框（0 m 处）+ 上升轨迹虚线，保证不看动画也一目了然
        els.append(
            f'<rect x="{cx - 28}" y="{y_bot}" width="56" height="30" rx="5" '
            f'fill="none" stroke="{HAIRLINE}" stroke-width="1.2" stroke-dasharray="3,3"/>'
        )
        els.append(
            f'<line x1="{cx}" y1="{y_bot - 4}" x2="{cx}" y2="{y_top + 36}" '
            f'stroke="{col}" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.45"/>'
        )
        # 运动重物组（钢索 y1=-4 经 clipPath 在 y=122 滑轮下沿精确收卷，终态停在 y_top）
        els.append('<g clip-path="url(#hoist-shaft-clip)">')
        els.append(f'  <g class="{c_cls}">')
        els.append(f'    <line x1="{cx}" y1="-4" x2="{cx}" y2="{y_top}" stroke="{col}" stroke-width="1.6"/>')
        els.append(f'    <rect x="{cx - 28}" y="{y_top}" width="56" height="30" rx="5" fill="{soft}" stroke="{col}" stroke-width="1.6"/>')
        els.append(f'    {txt(cx, y_top + 14, "75 kg", 11, INK, "middle", weight="700")}')
        els.append(f'    {txt(cx, y_top + 26, "735.5 N", 9.5, col, "middle", weight="600")}')
        els.append("  </g>")
        els.append("</g>")
        # 到顶时间标签
        els.append(txt(cx, 312, t_s, 11.5, col, "middle", weight="700", cls=d_cls))

    # 右侧物理对照账本
    els.append(card(480, 64, 260, 266, fill=CARD_BG, stroke=BORDER))
    els.append(pill(494, 76, "核心辨析：力 ≠ 功 ≠ 功率", fg=PURPLE, bg=PURPLE_SOFT, w=206))

    els.append(txt(496, 118, "① 绳子拉力 F（力气大小）：", 11.5, INK, weight="700"))
    els.append(txt(496, 137, "匀速提升时 F = mg = 735.5 N", 11.5, BODY))
    els.append(txt(496, 155, "→ A、B、C 三者拉力完全相等！", 11.5, GREEN, weight="700"))

    els.append(txt(496, 184, "② 搬运总做功 W（干活总量）：", 11.5, INK, weight="700"))
    els.append(txt(496, 203, "W = F·Δh = 735.5 × 4 = 2,942 J", 11.5, BODY))
    els.append(txt(496, 221, "→ A、B、C 干的总活完全相等！", 11.5, GREEN, weight="700"))

    els.append(txt(496, 250, "③ 功率 P（干活快慢 = 马力）：", 11.5, INK, weight="700"))
    els.append(txt(496, 269, "P = W ÷ t = F × v", 12, ORANGE, weight="700"))
    els.append(txt(496, 289, "• 1 PS 恰好 1 秒拎高 1 米 (735.5 W)", 11, BODY))
    els.append(txt(496, 308, "• 3 PS 速度快 3 倍，耗时缩为 1/3", 11, BODY))

    # 底部提示栏
    els.append(card(20, 342, 720, 36, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(
        txt(
            36,
            365,
            "记住这句话：小马达配大减速齿轮也能拉动千斤重物（力气大），但只有大马力机器才能把重物“飞快”拎上去（功率大）。",
            11.5,
            INK,
            weight="600",
        )
    )

    return figure(
        390,
        "力、功与功率的区别动画：0.25马力、1马力与3马力匀速吊起75千克重物升高4米的速度对比",
        "三台装置匀速提升同为75千克（拉力同为735.5牛）的重物升高4米（总功同为2942焦耳）：0.25公制马力速度0.25米每秒耗时16秒，1公制马力速度1米每秒耗时4秒，3公制马力速度3米每秒耗时1.33秒，直观展示马力衡量做功快慢而非拉力大小。",
        els,
        extra_css=extra_css,
    )


# ---------------------------------------------------------------------------
# 图 4：汽车扭矩 vs 马力曲线（200 kW 永磁电机 vs 2.0T 涡轮燃油机）
# ---------------------------------------------------------------------------
def build_torque_power_curves() -> str:
    els = header(
        "图 4 · 扭矩 vs 马力：为什么电车起步“零延迟猛窜”，油车要拉高转速爆发？",
        "同为 200 kW（约 272 PS）峰值功率动力源：P [kW] = 扭矩 T [N·m] × 转速 n [rpm] ÷ 9549",
    )

    els.append(card(20, 64, 464, 264, fill=CARD_BG, stroke=BORDER))

    x0, x1 = 68.0, 424.0  # 0..7000 rpm -> 356 px
    y_bot, y_top = 286.0, 96.0  # 190 px height
    rpm_max = 7000.0
    p_max_ax = 250.0  # left axis: 0..250 kW
    t_max_ax = 500.0  # right axis: 0..500 N·m
    rot_k = 60.0 * 1000.0 / (2.0 * math.pi)  # 9549.2966

    def x_rpm(n: float) -> float:
        return x0 + (x1 - x0) * (n / rpm_max)

    def y_kw(p: float) -> float:
        return y_bot - (y_bot - y_top) * (p / p_max_ax)

    def y_nm(t: float) -> float:
        return y_bot - (y_bot - y_top) * (t / t_max_ax)

    # 网格线与双纵轴刻度
    for k in range(6):
        p_val = k * 50
        t_val = k * 100
        yy = y_kw(p_val)
        els.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.9"/>')
        els.append(txt(x0 - 6, yy + 4, f"{p_val}", 10.5, INK, "end"))
        els.append(txt(x1 + 6, yy + 4, f"{t_val}", 10.5, MUTED, "start"))

    els.append(txt(x0 - 8, 82, "功率 kW", 11, INK, "middle", weight="700"))
    els.append(txt(x1 + 18, 82, "扭矩 N·m", 11, MUTED, "middle", weight="700"))

    for r_tick in range(0, 7001, 1000):
        xx = x_rpm(r_tick)
        els.append(f'<line x1="{xx:.1f}" y1="{y_bot}" x2="{xx:.1f}" y2="{y_bot + 4}" stroke="{SLATE}" stroke-width="1"/>')
        els.append(txt(xx, y_bot + 17, f"{r_tick // 1000}k" if r_tick else "0", 10.5, MUTED, "middle"))
    els.append(txt((x0 + x1) / 2, y_bot + 33, "转速 n (rpm)", 11, BODY, "middle", weight="600"))

    # 电机基速分界线 n_base = 4775 rpm
    n_base = 200.0 * rot_k / 400.0
    xb = x_rpm(n_base)
    els.append(f'<line x1="{xb:.1f}" y1="{y_top}" x2="{xb:.1f}" y2="{y_bot}" stroke="{BLUE_LINE}" stroke-width="1.2" stroke-dasharray="4,3"/>')
    els.append(txt((x0 + xb) / 2, 110, "电机恒转矩区", 10.5, BLUE, "middle", halo=True))
    els.append(txt((xb + x1) / 2, 110, "恒功率区", 10.5, BLUE, "middle", halo=True))

    # 1) 永磁电机曲线：0..4775 rpm 扭矩 400 N·m，4775..7000 rpm 功率恒 200 kW
    ev_t_pts, ev_p_pts = [], []
    for step in range(141):
        n = step * 50.0
        t_ev = 400.0 if n <= n_base else 200.0 * rot_k / n
        p_ev = t_ev * n / rot_k
        ev_t_pts.append(f"{x_rpm(n):.2f},{y_nm(t_ev):.2f}")
        ev_p_pts.append(f"{x_rpm(n):.2f},{y_kw(p_ev):.2f}")

    # 2) 2.0T 燃油机曲线：800 rpm 怠速 -> 1500..4500 rpm 扭矩平台 380 N·m -> 5026..6000 rpm 维持 200 kW -> 6500 rpm 略降
    def ice_torque(n: float) -> float:
        if n < 800.0:
            return 160.0 * (n / 800.0)
        if n < 1500.0:
            return 160.0 + 220.0 * ((n - 800.0) / 700.0)
        if n <= 4500.0:
            return 380.0
        n_peak = 200.0 * rot_k / 380.0  # 5026 rpm
        if n <= n_peak:
            return 380.0
        if n <= 6000.0:
            return 200.0 * rot_k / n
        return (200.0 - 18.0 * ((n - 6000.0) / 1000.0)) * rot_k / n

    ice_t_pts, ice_p_pts = [], []
    for step in range(16, 136):  # 800..6750 rpm
        n = step * 50.0
        t_ic = ice_torque(n)
        p_ic = t_ic * n / rot_k
        ice_t_pts.append(f"{x_rpm(n):.2f},{y_nm(t_ic):.2f}")
        ice_p_pts.append(f"{x_rpm(n):.2f},{y_kw(p_ic):.2f}")

    els.append(f'<polyline points="{" ".join(ev_t_pts)}" fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="5,3"/>')
    els.append(f'<polyline points="{" ".join(ice_t_pts)}" fill="none" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="5,3"/>')
    els.append(f'<polyline points="{" ".join(ev_p_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
    els.append(f'<polyline points="{" ".join(ice_p_pts)}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')

    # 图内直接标注曲线身份（不光靠颜色）
    els.append(txt(x_rpm(2100), y_nm(400) - 8, "电机扭矩 400 N·m (虚线)", 10.5, BLUE, "middle", weight="700", halo=True))
    els.append(txt(x_rpm(2950), y_nm(380) + 15, "2.0T 扭矩 380 N·m (虚线)", 10.5, ORANGE, "middle", weight="700", halo=True))
    els.append(txt(x_rpm(5850), y_kw(200) - 9, "峰值 200 kW (实线)", 10.5, INK, "middle", weight="700", halo=True))

    # 右栏：读图三步法
    els.append(card(498, 64, 242, 264, fill=CARD_BG, stroke=BORDER))
    els.append(pill(512, 76, "读懂这张图，买车不再被忽悠", fg=INK, bg=SLATE_SOFT, w=214))

    els.append(step_badge(520, 118, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(536, 122, "起步看低转扭矩：", 12, BLUE, weight="700"))
    els.append(txt(514, 141, "电机 0 rpm 直接满扭 400 N·m；", 11, BODY))
    els.append(txt(514, 158, "油车怠速弱，需变速箱降挡放大。", 11, BODY))

    els.append(step_badge(520, 186, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(536, 190, "中段看功率爬坡：", 12, ORANGE, weight="700"))
    els.append(txt(514, 209, "油车 1500–4500 rpm 扭矩平直，", 11, BODY))
    els.append(txt(514, 226, "转速翻倍则输出马力同步翻倍。", 11, BODY))

    els.append(step_badge(520, 254, 3, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(536, 258, "高速超车看峰值马力：", 12, GREEN, weight="700"))
    els.append(txt(514, 277, "车速高时 F_轮 = η·P ÷ v，", 11, BODY))
    els.append(txt(514, 294, "峰值同为 272 PS，后段底气相当！", 11, BODY))

    # 底部通栏
    els.append(card(20, 338, 720, 38, fill=ORANGE_SOFT, stroke=ORANGE))
    els.append(
        txt(
            36,
            362,
            "骑车比喻秒懂：扭矩是“脚踩踏板那一下蹬多重”，转速是“每分钟踩几圈”，两者乘起来才是你往前冲的马力！",
            11.5,
            INK,
            weight="600",
        )
    )

    return figure(
        388,
        "200千瓦电动汽车电机与2.0T涡轮增压发动机的扭矩与功率特性曲线对比",
        "横轴为0至7000转每分：蓝色电机在0至4775转为400牛米恒转矩区、功率线性升至200千瓦，随后进入200千瓦恒功率区；橙色2.0T发动机在1500至4500转维持380牛米扭矩平台，5000转以上达200千瓦峰值功率。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 5：马力家族换算表（hp / PS / 空调 1 匹）与极速的“三次方风阻高墙”
# ---------------------------------------------------------------------------
def build_family_and_drag_wall() -> str:
    els = header(
        "图 5 · 马力家族换算账本与极速“三次方高墙”：马力翻倍为何极速远不能翻倍？",
        "左看英制 hp、公制 PS 与空调“1 匹”的差别；右看高速风阻功率 P_drag ∝ v³ 的陡峭代价",
    )

    # 左栏：四种“马力 / 匹”对照卡
    els.append(card(20, 64, 344, 272, fill=CARD_BG, stroke=BORDER))
    els.append(pill(32, 76, "① 日常最易混的 4 种“马力 / 匹”", fg=BLUE, bg=BLUE_SOFT, w=232))

    items = [
        ("英制马力 1 hp", "745.7 W", "英美传统机械定义 (550 ft·lbf/s)", BLUE, BLUE_SOFT),
        ("公制马力 1 PS", "735.5 W", "德/日/国内常说“多少匹” (75 kgf·m/s)", GREEN, GREEN_SOFT),
        ("电机马力 1 hp(E)", "746.0 W", "工业电动机铭牌采用的精确整瓦值", PURPLE, PURPLE_SOFT),
        ("家用空调“1 匹”", "制冷 ≈2500 W", "压缩机耗电 ≈735 W × 能效比 COP≈3.4", ORANGE, ORANGE_SOFT),
    ]
    for idx, (name, val, desc_s, col, soft) in enumerate(items):
        yy = 108 + idx * 55
        els.append(card(32, yy, 320, 46, rx=8, fill=soft, stroke=col, sw=1))
        els.append(txt(44, yy + 19, name, 12, INK, weight="700"))
        els.append(txt(340, yy + 19, val, 12, col, "end", weight="700"))
        els.append(txt(44, yy + 37, desc_s, 10.5, BODY))

    # 右栏：极速 vs 所需发动机马力曲线 (P_total = (0.5*ρ*Cd*A*v³ + Crr*m*g*v) / η)
    els.append(card(380, 64, 360, 272, fill=CARD_BG, stroke=BORDER))
    els.append(pill(392, 76, "② 冲击极速所需的马力陡坡 (P_drag ∝ v³)", fg=RED, bg=RED_SOFT, w=268))

    gx0, gx1 = 434.0, 716.0  # 0..400 km/h
    gy0, gy1 = 292.0, 118.0  # 0..900 PS
    v_max_ax = 400.0
    ps_max_ax = 900.0

    def req_ps(v_kmh: float) -> float:
        v = v_kmh / 3.6
        p_drag = 0.5 * 1.225 * 0.28 * 2.2 * (v ** 3)
        p_roll = 0.012 * 1600.0 * G_STD * v
        p_engine_w = (p_drag + p_roll) / 0.88
        return p_engine_w / PS_METRIC_W

    def px_v(v_kmh: float) -> float:
        return gx0 + (gx1 - gx0) * (v_kmh / v_max_ax)

    def py_ps(ps_v: float) -> float:
        return gy0 - (gy0 - gy1) * (ps_v / ps_max_ax)

    for ps_tick in (0, 300, 600, 900):
        yy = py_ps(ps_tick)
        els.append(f'<line x1="{gx0}" y1="{yy:.1f}" x2="{gx1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.9"/>')
        els.append(txt(gx0 - 6, yy + 4, f"{ps_tick}", 10.5, MUTED, "end"))
    els.append(txt(gx0 - 4, 108, "需马力 PS", 10.5, INK, "middle", weight="700"))

    for v_tick in (0, 100, 200, 300, 400):
        xx = px_v(v_tick)
        els.append(f'<line x1="{xx:.1f}" y1="{gy0}" x2="{xx:.1f}" y2="{gy0 + 4}" stroke="{SLATE}" stroke-width="1"/>')
        els.append(txt(xx, gy0 + 17, f"{v_tick}", 10.5, MUTED, "middle"))
    els.append(txt((gx0 + gx1) / 2, gy0 + 34, "巡航极速 v (km/h，轿车 Cd=0.28)", 10.5, BODY, "middle", weight="600"))

    curve_pts = [f"{px_v(k * 4.0):.2f},{py_ps(req_ps(k * 4.0)):.2f}" for k in range(101)]
    els.append(f'<polyline points="{" ".join(curve_pts)}" fill="none" stroke="{RED}" stroke-width="2.5"/>')

    milestones = [
        (100, "100 km/h: 约 19 PS", -6, -10, "start"),
        (200, "200 km/h: 约 116 PS", -8, -10, "end"),
        (300, "300 km/h: 约 365 PS", -10, -8, "end"),
        (400, "400 km/h: 约 842 PS!", -10, 4, "end"),
    ]
    for vk, label_m, dx, dy, anc in milestones:
        pv = req_ps(vk)
        cx_m, cy_m = px_v(vk), py_ps(pv)
        els.append(f'<circle cx="{cx_m:.1f}" cy="{cy_m:.1f}" r="4.2" fill="{RED}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(cx_m + dx, cy_m + dy, label_m, 10.5, RED, anc, weight="700", halo=True))

    # 底部总结栏
    els.append(card(20, 348, 720, 38, fill=RED_SOFT, stroke=RED))
    els.append(
        txt(
            36,
            372,
            "三次方高墙：风阻 F_D ∝ v²、功率 P_drag ∝ v³——车速从 100 翻到 400 km/h（×4），克服风阻功率要暴涨 64 倍！",
            11.5,
            INK,
            weight="600",
        )
    )

    return figure(
        398,
        "四种常见马力换算对照与汽车克服空气阻力功率随车速三次方暴涨曲线",
        "左栏对比英制1hp=745.7瓦、公制1PS=735.5瓦、电机马力746瓦及空调1匹（输入约735瓦、制冷量约2500瓦）；右栏展示轿车维持100、200、300、400千米每小时分别需约19、116、365、842公制马力。",
        els,
    )


@register("horsepower-physics", "1马力等于一匹马的力气吗：瓦特手稿、真马爆发与扭矩功率曲线", "science")
def build_all() -> list[str]:
    verify_horsepower_math()
    outputs = {
        "watt-mill-wheel-origin.svg": build_watt_mill_wheel(),
        "horse-human-burst-vs-sustained.svg": build_burst_vs_sustained(),
        "power-lifting-race-anim.svg": build_power_lifting_race_anim(),
        "torque-power-ev-ice.svg": build_torque_power_curves(),
        "horsepower-family-and-drag-cube.svg": build_family_and_drag_wall(),
    }
    for fname, svg in outputs.items():
        write_svg(SUBDIR, fname, svg)
    return [f"{SUBDIR}/{k}" for k in outputs]
