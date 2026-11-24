"""几百吨的飞机为什么能飞（heavy-aircraft-flight）——5 张原创 760px 矢量图解与计时起飞动画。

涵盖：
1. airliner-force-leverage.svg      : 575 吨 A380 为何四台发动机朝下喷也飞不起，水平分工却有 18 倍升阻比放大 + 每秒 350 吨下洗动量账
2. kutta-circulation-pressure.svg   : 无黏零升力悖论 → 黏性起始涡与库塔条件建立环流 Γ → 真实翼面上下压强分布（上吸 70% / 下托 30%，平均仅 0.066 atm）
3. takeoff-roll-lift-anim.svg       : 跑道加速 0→276 km/h 单次等比动画 + v² 二次方升力曲线（放襟翼 276 km/h vs 光洁翼 408 km/h）
4. wingtip-vortex-and-turbofan.svg  : 有限翼展翼尖涡/诱导阻力/翼尖小翼 + 10:1 高涵道比涡扇“大流量慢加速”86% 推进效率原理
5. sky-machines-comparison.svg      : 大客机 vs 直升机/四旋翼无人机 vs 扑翼飞鸟 vs 太空火箭的四维拨气与动量机制全景对照
"""

from __future__ import annotations

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
    card,
    figure,
    header,
    pill,
    register,
    txt,
    write_svg,
)

TOPIC = "heavy-aircraft-flight"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#ecfdf5"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"

EXTRA_ARROWS = f"""
  <marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{RED}"/>
  </marker>
  <marker id="arr-teal" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{TEAL}"/>
  </marker>
"""


def badge(x: float, y: float, w: float, h: float, label: str, bg: str, fg: str) -> str:
    return pill(x, y, label, fg=fg, bg=bg, border=fg, w=w, h=h, size=11.5)


def poly(pts: list[tuple[float, float]], stroke: str, sw: float = 2.0, dash: str | None = None) -> str:
    pts_s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{pts_s}" fill="none" stroke="{stroke}" stroke-width="{sw}"{extra}/>'

# 物理与工程常数（Airbus A380-800 官方最大起飞重量级参数 & 国际标准大气 ISA）
G_N = 9.80665
M_A380_KG = 575_000.0
W_A380_N = M_A380_KG * G_N            # 5,638,823.75 N ≈ 5.64 MN
S_A380_M2 = 845.0
SPAN_A380_M = 79.75
AR_A380 = SPAN_A380_M**2 / S_A380_M2  # 7.527
RHO_SL = 1.225                        # 海平面密度 kg/m³
RHO_11K = 0.3639                      # 11 km 对流层顶密度 kg/m³
P_ATM_PA = 101_325.0

THRUST_STATIC_4ENG_N = 4.0 * 332_000.0  # 1,328,000 N ≈ 1.33 MN (Trent 900 / GP7200 级)
LD_CRUISE = 18.0
THRUST_CRUISE_N = W_A380_N / LD_CRUISE  # 313,268 N ≈ 0.313 MN

CL_FLAP_LOF = 1.85
CL_CLEAN_SAFE = 0.85
V_LOF_MS = math.sqrt(2.0 * W_A380_N / (RHO_SL * S_A380_M2 * CL_FLAP_LOF))      # 76.76 m/s = 276.3 km/h
V_CLEAN_MS = math.sqrt(2.0 * W_A380_N / (RHO_SL * S_A380_M2 * CL_CLEAN_SAFE))  # 113.21 m/s = 407.6 km/h


def verify_heavy_flight_math() -> None:
    """运行期严格核验全部空气动力学与推进效率指标。"""
    # 1. 四台涡扇最大静推力仅为最大起飞重量的 23.55%，朝下硬顶绝对飞不起来
    ratio_static = THRUST_STATIC_4ENG_N / W_A380_N
    assert 0.23 < ratio_static < 0.25, ratio_static

    # 2. 平均翼载压强：6,673 Pa ≈ 0.0659 atm
    wing_loading_pa = W_A380_N / S_A380_M2
    assert 6650.0 < wing_loading_pa < 6700.0, wing_loading_pa
    assert 0.065 < wing_loading_pa / P_ATM_PA < 0.067

    # 3. 离地速度：放襟翼约 276.3 km/h，不放襟翼约 407.6 km/h；半速 138.2 km/h 时升力严格为 25%
    assert abs(V_LOF_MS * 3.6 - 276.3) < 0.3
    assert abs(V_CLEAN_MS * 3.6 - 407.6) < 0.3
    l_half = 0.5 * RHO_SL * (0.5 * V_LOF_MS) ** 2 * S_A380_M2 * CL_FLAP_LOF
    assert abs(l_half / W_A380_N - 0.25) < 1e-9

    # 4. 动量下洗核验：每秒影响 350 t 空气，下洗速度增量约 16.11 m/s 即可平衡 5.64 MN 重力
    m_dot_air = 350_000.0
    dv_down = W_A380_N / m_dot_air
    assert 16.0 < dv_down < 16.3, dv_down

    # 5. 涡扇 vs 纯涡喷推进效率（v0 = 250 m/s）：ve = 330 m/s -> 86.2%，ve = 650 m/s -> 55.6%
    v0 = 250.0
    eta_fan = 2.0 * v0 / (330.0 + v0)
    eta_jet = 2.0 * v0 / (650.0 + v0)
    assert abs(eta_fan - 0.8621) < 0.002
    assert abs(eta_jet - 0.5556) < 0.002


# ---------------------------------------------------------------------------
# 图 1：为什么四台发动机竖着喷也顶不起 575 吨，横着推却只需 1/18 的力？
# ---------------------------------------------------------------------------
def build_airliner_force_leverage() -> str:
    els = header(
        "图 1 · 575 吨钢铁大楼的飞行分工：为什么发动机不朝下喷，机翼却能放大 18 倍力？",
        "以空客 A380 满载起飞重量（575 t ≈ 5.64 MN）与四台涡扇发动机真实推力核算",
    )

    # 左卡：如果把 4 台发动机竖过来学火箭硬顶 vs 真实水平分工
    els.append(card(20, 64, 348, 270))
    els.append(badge(34, 76, 206, 22, "对比账：硬顶失败 vs 气动杠杆", RED_SOFT, RED))

    # 上半：错误的“竖喷硬顶”设想
    els.append(card(34, 108, 320, 96, fill=RED_SOFT, stroke=RED))
    els.append(txt(48, 128, "❌ 设想把 4 台大涡扇全竖过来朝下喷：", 11.5, RED, weight="700"))
    # 推力条 vs 重力条（按比例：5.64 MN -> 200 px，1.33 MN -> 47 px）
    els.append(txt(48, 150, "4 台满推力", 10.5, BODY, weight="600"))
    els.append(f'<rect x="114" y="140" width="47" height="12" rx="3" fill="{ORANGE}"/>')
    els.append(txt(167, 150, "1.33 MN（仅够顶 136 吨！）", 10.5, ORANGE, weight="700"))

    els.append(txt(48, 171, "满载总重力", 10.5, BODY, weight="600"))
    els.append(f'<rect x="114" y="161" width="200" height="12" rx="3" fill="{RED}"/>')
    els.append(txt(48, 193, "结论：推力连机身重量的 1/4 都不到，纹丝不动！", 10.5, RED, weight="600"))

    # 下半：真实的“发动机推前 + 机翼托上”18 倍杠杆
    els.append(card(34, 214, 320, 108, fill=GREEN_SOFT, stroke=GREEN))
    els.append(txt(48, 234, "✓ 真实平飞分工（巡航升阻比 L / D ≈ 18）：", 11.5, GREEN, weight="700"))
    els.append(txt(48, 255, "• 发动机往后推气 → 向前推力 T = D ≈ 0.31 MN", 11, INK, weight="600"))
    els.append(txt(48, 274, "• 机翼把迎面风往下导 → 向上升力 L = W = 5.64 MN", 11, BLUE, weight="700"))
    els.append(txt(48, 294, "• 1 份水平推力撬起 18 份竖直重量（省力斜坡效应）", 10.5, GREEN, weight="700"))
    els.append(txt(48, 311, "  注意：省力不省功，升力垂直于航迹不做功！", 10, MUTED))

    # 右卡：四力平衡 + 每秒划过 350 吨空气的动量账本
    els.append(card(384, 64, 356, 270))
    els.append(badge(398, 76, 224, 22, "动量账：每秒把 350 吨空气往下拨", BLUE_SOFT, BLUE))

    # 侧面机身+机翼示意 + 四支力箭头 + 来流偏转下洗流线
    cx, cy = 556, 176
    # 来流 -> 下洗流线（3 条柔和弯曲流线）
    for dy_in, dy_out in [(-28, -8), (-10, 14), (10, 34)]:
        els.append(
            f'<path d="M 404 {cy + dy_in} C 480 {cy + dy_in}, 548 {cy + dy_in + 2}, '
            f'610 {cy + dy_out - 6} Q 655 {cy + dy_out + 4} 702 {cy + dy_out + 12}" '
            f'fill="none" stroke="{TEAL}" stroke-width="1.5" stroke-dasharray="5,3" '
            f'marker-end="url(#arr-teal)"/>'
        )
    els.append(txt(406, 136, "迎面相对气流 v ≈ 250 m/s", 10.5, TEAL, weight="600"))
    els.append(txt(646, 228, "下洗偏转气流", 10.5, TEAL, "middle", weight="700"))
    els.append(txt(646, 242, "Δv_y ≈ 16.1 m/s ↓", 10, TEAL, "middle", weight="600"))

    # 简化的机翼剖面（带小迎角）
    els.append(
        f'<path d="M 500 174 C 520 156, 566 160, 608 182 C 572 183, 526 181, 500 174 Z" '
        f'fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>'
    )
    # 翼下短舱示意
    els.append(f'<rect x="530" y="186" width="28" height="10" rx="4" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.4"/>')

    # 四支力矢量箭头（从气动中心 546, 174 出发）
    # 升力 L 向上, 重力 W 向下
    els.append(f'<line x1="546" y1="166" x2="546" y2="108" stroke="{BLUE}" stroke-width="2.6" marker-end="url(#arr-blue)"/>')
    els.append(txt(556, 116, "升力 L = 5.64 MN", 11, BLUE, weight="700"))

    els.append(f'<line x1="546" y1="184" x2="546" y2="242" stroke="{RED}" stroke-width="2.6" marker-end="url(#arr-red)"/>')
    els.append(txt(546, 257, "重力 W = 5.64 MN", 11, RED, "middle", weight="700"))

    # 推力 T 向左（机头朝左迎风！），阻力 D 向右
    els.append(f'<line x1="524" y1="191" x2="462" y2="191" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>')
    els.append(txt(458, 207, "推力 T = 0.31 MN", 10.5, ORANGE, weight="700"))

    els.append(f'<line x1="612" y1="182" x2="668" y2="182" stroke="{SLATE}" stroke-width="2.0" marker-end="url(#arr-muted)"/>')
    els.append(txt(674, 178, "阻力 D", 10.5, SLATE, weight="700"))

    # 右下动量核算公式框
    els.append(card(398, 268, 328, 54, fill=BLUE_SOFT, stroke=BLUE))
    els.append(txt(410, 288, "牛顿第二、三定律：L = ṁ_空气 × Δv_y", 11, BLUE, weight="700"))
    els.append(txt(410, 308, "每秒拨动 350,000 kg 空气 × 下推 16.1 m/s = 5.64 MN！", 10.5, INK, weight="600"))

    # 底部通栏要点
    els.append(card(20, 344, 720, 38, fill=AMBER_SOFT, stroke=AMBER))
    els.append(
        txt(
            36,
            368,
            "一句话抓本质：飞机不是踩着静止空气不动，而是以 900 km/h 高速不断“划过新空气”——每秒把几百吨空气往下推！",
            11.5,
            INK,
            weight="600",
        )
    )

    return figure(
        394,
        "575吨客机四力分工与18倍升阻比放大及每秒350吨空气下洗动量账图解",
        "左侧对比空客A380四台涡扇最大静推力1.33兆牛不足重力5.64兆牛的四分之一，平飞时靠升阻比18用0.31兆牛推力换取5.64兆牛升力；右侧展示机翼每秒将约350吨迎面空气向下偏转16.1米每秒从而获得5.64兆牛向上反作用力。",
        els,
        extra_defs=EXTRA_ARROWS,
    )


# ---------------------------------------------------------------------------
# 图 2：黏性、起始涡与环流怎样建立真实机翼的上下压强差？（破除等时间谬误）
# ---------------------------------------------------------------------------
def build_kutta_circulation_pressure() -> str:
    els = header(
        "图 2 · 空气没约好“后缘重逢”！黏性、起始涡与环流怎样造出 575 吨压差？",
        "从无黏零升力悖论 → 跑道起步脱落起始涡建立环流 Γ → 翼背吸力占七成、平均压差仅 0.066 个大气压",
    )

    # 顶部三步演化小卡片（宽各 232，间距 12）
    steps = [
        (20, "① 假想“零黏性”理想空气", SLATE, SLATE_SOFT),
        (264, "② 真实黏性起步：脱落起始涡", PURPLE, PURPLE_SOFT),
        (508, "③ 稳态飞行：环流 + 来流叠加", BLUE, BLUE_SOFT),
    ]
    for x0, title_s, col, soft in steps:
        els.append(card(x0, 64, 232, 128))
        els.append(badge(x0 + 12, 74, 208, 22, title_s, soft, col))

    # Step 1 图示：尖后缘倒卷，零环流零升力
    els.append('<path d="M 58 134 C 82 118, 134 122, 182 142 C 142 143, 88 141, 58 134 Z" fill="#f1f5f9" stroke="#64748b" stroke-width="1.8"/>')
    els.append(f'<path d="M 34 124 Q 112 106 186 132" fill="none" stroke="{SLATE}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')
    # 下表面绕过后缘倒卷到上面
    els.append(f'<path d="M 34 146 Q 124 156 184 144 Q 194 138 170 128" fill="none" stroke="{RED}" stroke-width="1.6" marker-end="url(#arr-red)"/>')
    els.append(txt(136, 170, "下表面气流绕尖后缘倒卷", 10.5, RED, "middle", weight="600"))
    els.append(txt(136, 184, "环流 Γ = 0 → 升力严格为 0！", 10.5, BODY, "middle", weight="700"))

    # Step 2 图示：边界层阻止倒卷，脱落逆时针起始涡 (-Γ)，留下顺时针附着环流 (+Γ)
    els.append('<path d="M 290 134 C 312 118, 356 122, 398 142 C 362 143, 316 141, 290 134 Z" fill="#f3e8ff" stroke="#6d28d9" stroke-width="1.8"/>')
    # 顺时针附着环流椭圆箭头
    els.append(f'<path d="M 304 116 Q 350 102 392 122" fill="none" stroke="{PURPLE}" stroke-width="1.7" marker-end="url(#arr-blue)"/>')
    els.append(f'<path d="M 384 150 Q 342 158 302 146" fill="none" stroke="{PURPLE}" stroke-width="1.7"/>')
    els.append(txt(344, 110, "附着环流 +Γ (顺时针)", 10, PURPLE, "middle", weight="700"))
    # 后方脱落的逆时针起始涡
    els.append(f'<path d="M 446 138 m -14 0 a 14 14 0 1 0 28 0 a 14 14 0 1 0 -28 0" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="4,2"/>')
    els.append(txt(446, 142, "-Γ", 10.5, ORANGE, "middle", weight="700"))
    els.append(txt(380, 170, "黏性边界层甩出逆时针起始涡", 10.5, PURPLE, "middle", weight="600"))
    els.append(txt(380, 184, "库塔条件：气流从后缘平顺离开", 10.5, BODY, "middle", weight="700"))

    # Step 3 图示：上方 v0 + Δv 远早于下方到达尾缘！
    els.append('<path d="M 544 134 C 568 118, 620 122, 668 142 C 628 143, 574 141, 544 134 Z" fill="#eaf4fb" stroke="#1d6fa5" stroke-width="1.8"/>')
    els.append(f'<path d="M 522 122 Q 604 98 698 134" fill="none" stroke="{BLUE}" stroke-width="2.0" marker-end="url(#arr-blue)"/>')
    els.append(f'<path d="M 522 146 Q 596 154 654 148" fill="none" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')
    # 同一时刻脉冲烟团位置标记点
    els.append(f'<circle cx="688" cy="131" r="4" fill="{BLUE}"/>')
    els.append(f'<circle cx="634" cy="149" r="4" fill="{ORANGE}"/>')
    els.append(txt(624, 110, "上表面同向叠加：高速低压", 10, BLUE, "middle", weight="700"))
    els.append(txt(624, 170, "上方气团远早于下方冲过尾缘！", 10.5, BLUE, "middle", weight="700"))
    els.append(txt(624, 184, "绝非“路远赶时间同时到达”", 10.5, MUTED, "middle", weight="600"))

    # 下半大卡：真实机翼表面压强积分分布 + A380 翼载压强精算
    els.append(card(20, 204, 720, 176))
    els.append(badge(34, 216, 268, 22, "压强账本：谁在用力？每平方米要多大压差？", TEAL_SOFT, TEAL))

    # 左侧翼型截面 + 上表面向上的低压吸力箭头群 + 下表面向上的正压托举箭头群
    els.append(
        '<path d="M 96 312 C 128 282, 228 286, 336 324 C 262 325, 148 322, 96 312 Z" '
        f'fill="{CARD_BG}" stroke="{INK}" stroke-width="2.2"/>'
    )
    # 上表面吸力箭头（前中段最强，向后递减，占总升力 ~70%）
    suction_pts = [
        (124, 297, 48),
        (152, 291, 52),
        (184, 291, 44),
        (218, 295, 34),
        (254, 302, 24),
        (290, 311, 15),
    ]
    for px, py, h_len in suction_pts:
        els.append(
            f'<line x1="{px}" y1="{py - 2}" x2="{px}" y2="{py - h_len}" '
            f'stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>'
        )
    # 下表面正压向上推箭头（占总升力 ~30%）
    push_pts = [
        (132, 320, 20),
        (172, 322, 18),
        (214, 324, 16),
        (258, 325, 13),
        (300, 325, 10),
    ]
    for px, py, h_len in push_pts:
        els.append(
            f'<line x1="{px}" y1="{py + h_len + 4}" x2="{px}" y2="{py + 4}" '
            f'stroke="{ORANGE}" stroke-width="2.0" marker-end="url(#arr-orange)"/>'
        )

    els.append(txt(208, 256, "上表面低压“向上吸”（p_上 < p_0）：贡献约 2/3～3/4 升力！", 11, BLUE, "middle", weight="700"))
    els.append(txt(214, 366, "下表面高压“向上托”（p_下 > p_0）：贡献约 1/4～1/3 升力", 11, ORANGE, "middle", weight="700"))

    # 右侧定量核算面板
    els.append(card(406, 218, 318, 148, fill=TEAL_SOFT, stroke=TEAL))
    els.append(txt(422, 240, "空客 A380 机翼压差实算（反直觉真相）：", 12, TEAL, weight="700"))
    els.append(txt(422, 263, "• 满载总重量：W = 575 t = 5,638,824 N", 11, INK, weight="600"))
    els.append(txt(422, 284, "• 机翼总面积：S = 845 m²（约两座篮球场！）", 11, INK, weight="600"))
    els.append(txt(422, 306, "• 平均上下压强差：Δp = W / S ≈ 6,673 Pa", 11.5, BLUE, weight="700"))
    els.append(txt(422, 327, "  仅为海平面大气压（101,325 Pa）的 6.6%！", 11, ORANGE, weight="700"))
    els.append(txt(422, 349, "• 折合指甲盖 1 cm² 上仅差 0.68 N（约 1 颗鸡蛋重）", 10.5, BODY, weight="600"))

    return figure(
        392,
        "机翼黏性起始涡建立环流机制与上下表面压强分布及A380翼载压差图解",
        "上方三步对比无黏理想流体后缘倒卷零升力、真实黏性起步脱落逆时针起始涡建立顺时针环流满足库塔条件、以及上表面气流远早于下表面冲过尾缘；下方展示上表面低压吸力贡献约三分之二至四分之三升力，A380平均翼面压差仅6673帕即0.066个大气压。",
        els,
        extra_defs=EXTRA_ARROWS,
    )


# ---------------------------------------------------------------------------
# 图 3：跑道加速 0→276 km/h 单次计时动画 + v² 二次方升力与襟翼增升曲线
# ---------------------------------------------------------------------------
def build_takeoff_roll_lift_anim() -> str:
    # 跑道滑跑真实约 40 s，按约 8.7 倍速等比压缩为 4.60 s 播放一次并停在离地爬升姿态
    dur = 4.60
    delay = 0.45
    dx_tot = 248.0  # 滑跑图标从 x0=74 移动到 x_liftoff=322 (对应 0 -> 276 km/h)

    gx0, gy0, gw, gh = 78.0, 344.0, 372.0, 150.0  # x: 0..440 km/h, y: 0..6.5 MN

    def xv(v_kmh: float) -> float:
        return gx0 + (v_kmh / 440.0) * gw

    def yl(l_mn: float) -> float:
        return gy0 - (l_mn / 6.5) * gh

    x_lof, y_lof = xv(276.3), yl(5.64)
    dx_dot = x_lof - gx0
    dy_dot = gy0 - y_lof

    # 元素原始坐标设在离地终态，keyframes 从起点反向偏移平滑运动到 (0, 0)，
    # 既保证单次播放结束后停留在完整结果，又保证 prefers-reduced-motion: reduce 禁用动画时仍停在完整终态！
    extra_css = f"""
  @keyframes takeoffRoll {{
    0%   {{ transform: translate(-{dx_tot:.1f}px, 28px) rotate(10deg); }}
    25%  {{ transform: translate(-{dx_tot * 0.9375:.1f}px, 28px) rotate(10deg); }}
    50%  {{ transform: translate(-{dx_tot * 0.7500:.1f}px, 28px) rotate(10deg); }}
    75%  {{ transform: translate(-{dx_tot * 0.4375:.1f}px, 28px) rotate(8deg); }}
    88%  {{ transform: translate(-{dx_tot * 0.1500:.1f}px, 26px) rotate(2deg); }}
    100% {{ transform: translate(0px, 0px) rotate(0deg); }}
  }}
  @keyframes dotClimb {{
    0%   {{ transform: translate(-{dx_dot:.1f}px, {dy_dot:.1f}px); }}
    25%  {{ transform: translate(-{0.75 * dx_dot:.1f}px, {0.9375 * dy_dot:.1f}px); }}
    50%  {{ transform: translate(-{0.50 * dx_dot:.1f}px, {0.7500 * dy_dot:.1f}px); }}
    75%  {{ transform: translate(-{0.25 * dx_dot:.1f}px, {0.4375 * dy_dot:.1f}px); }}
    100% {{ transform: translate(0px, 0px); }}
  }}
  .plane-anim {{
    transform-box: fill-box;
    transform-origin: center;
    animation: takeoffRoll {dur}s linear {delay}s 1 backwards;
  }}
  .lift-dot-anim {{
    animation: dotClimb {dur * 0.88:.2f}s linear {delay}s 1 backwards;
  }}
  @media (prefers-reduced-motion: reduce) {{
    .plane-anim, .lift-dot-anim {{ animation: none !important; }}
  }}
"""

    els = header(
        "图 3 · 速度翻倍，升力翻 4 倍！575 吨客机跑道加速与襟翼“变形”实算",
        "上方按匀加速比例演示一次滑跑抬头离地；下方按 L = ½ρv²SC_L 对比放襟翼（276 km/h）与不放襟翼（408 km/h）",
    )

    # 上栏：跑道滑跑三个静态里程碑 + 动画飞机（终态停在离地爬升处）
    els.append(card(20, 62, 720, 96))
    els.append(badge(34, 71, 212, 20, "跑道滑跑链条（匀加速 → 拉杆离地）", BLUE_SOFT, BLUE))
    # 跑道地面线
    els.append(f'<line x1="48" y1="138" x2="438" y2="138" stroke="{SLATE}" stroke-width="2.2"/>')
    els.append(f'<line x1="60" y1="138" x2="426" y2="138" stroke="#ffffff" stroke-width="1.0" stroke-dasharray="10,8"/>')

    # 起点与半速刻度（拉开水平间距避免接触）
    els.append(txt(74, 152, "0 km/h", 10, MUTED, "middle"))
    els.append(f'<circle cx="74" cy="138" r="3" fill="{SLATE}"/>')
    els.append(txt(190, 152, "138 km/h (仅 25% 升力)", 10, ORANGE, "middle", weight="600"))
    els.append(f'<circle cx="198" cy="138" r="3" fill="{ORANGE}"/>')
    els.append(txt(346, 152, "276 km/h (L = 575 t 离地！)", 10, GREEN, "middle", weight="700"))
    els.append(f'<circle cx="322" cy="138" r="3.5" fill="{GREEN}"/>')

    # 起点静态浅色虚影飞机（保证不看动画也能读出起点→离地过程）
    els.append(
        '<g opacity="0.35">'
        f'<path d="M 52 132 L 92 132 L 98 128 L 88 128 L 62 128 L 54 120 L 50 120 Z" fill="{SLATE}"/>'
        '</g>'
    )
    # 在终态位置 (x≈322, y≈104, 昂头 10°) 绘制客机剪影
    els.append(
        '<g class="plane-anim">'
        f'<g transform="translate(322, 104) rotate(-10)">'
        f'  <path d="M -26 4 L 22 4 Q 30 4 32 0 Q 26 -3 16 -3 L -16 -3 L -24 -12 L -29 -12 Z" fill="{BLUE}" stroke="{INK}" stroke-width="1.0"/>'
        f'  <path d="M -4 2 L 8 2 L -2 9 L -8 9 Z" fill="{ORANGE}"/>'
        '</g>'
        '</g>'
    )

    # 右上襟翼打开截面小卡
    els.append(card(456, 70, 270, 80, fill=ORANGE_SOFT, stroke=ORANGE))
    els.append(txt(468, 89, "起降机翼“变形术”：缝翼 + 后缘开缝襟翼", 11, ORANGE, weight="700"))
    # 前缘缝翼 + 主翼 + 后缘下偏双开缝襟翼示意
    els.append(f'<path d="M 474 124 Q 480 115 488 114" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    els.append(f'<path d="M 492 115 C 516 104, 554 107, 580 118 C 554 119, 516 118, 492 115 Z" fill="{CARD_BG}" stroke="{INK}" stroke-width="1.8"/>')
    els.append(f'<path d="M 583 120 Q 598 125 610 134" fill="none" stroke="{ORANGE}" stroke-width="2.6"/>')
    els.append(txt(622, 117, "弯度↑ 面积↑", 10.5, INK, weight="700"))
    els.append(txt(622, 133, "C_L 从 0.85 → 1.85", 10.5, ORANGE, weight="700"))
    els.append(txt(468, 144, "离地速度直降 131 km/h，保护轮胎与跑道安全！", 10, BODY, weight="600"))

    # 下栏左：精确计算的 L(v) 二次方曲线图 (v: 0..430 km/h, L: 0..6.5 MN)
    els.append(card(20, 168, 456, 214))

    # 坐标网格与坐标轴
    for l_val in (0.0, 1.41, 2.82, 5.64):
        yy = yl(l_val)
        col_g = GREEN if abs(l_val - 5.64) < 0.05 else HAIRLINE
        dash = "5,4" if abs(l_val - 5.64) < 0.05 else "3,3"
        els.append(f'<line x1="{gx0}" y1="{yy:.1f}" x2="{gx0 + gw}" y2="{yy:.1f}" stroke="{col_g}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
    els.append(f'<line x1="{gx0}" y1="{gy0 - gh - 6}" x2="{gx0}" y2="{gy0}" stroke="{SLATE}" stroke-width="1.4"/>')
    els.append(f'<line x1="{gx0}" y1="{gy0}" x2="{gx0 + gw}" y2="{gy0}" stroke="{SLATE}" stroke-width="1.4"/>')

    els.append(txt(70, yl(5.64) + 4, "5.64", 10.5, GREEN, "end", weight="700"))
    els.append(txt(70, yl(2.82) + 4, "2.82", 10, MUTED, "end"))
    els.append(txt(70, yl(1.41) + 4, "1.41", 10, ORANGE, "end", weight="600"))
    els.append(txt(70, gy0 + 4, "0", 10, MUTED, "end"))
    els.append(txt(34, 188, "升力 L (MN)", 11, INK, weight="700"))

    for v_tick in (0, 138, 276, 408):
        xx = xv(v_tick)
        els.append(f'<line x1="{xx:.1f}" y1="{gy0}" x2="{xx:.1f}" y2="{gy0 + 4}" stroke="{SLATE}"/>')
        els.append(txt(xx, gy0 + 16, str(v_tick), 10, INK if v_tick in (138, 276, 408) else MUTED, "middle", weight="600"))
    els.append(txt(gx0 + gw / 2, 374, "滑跑空速 v (km/h)", 11, INK, "middle", weight="700"))

    # 曲线 1：放下襟翼 + 缝翼 (C_L = 1.85)，0 -> 295 km/h
    pts_flap = []
    for v_k in range(0, 296, 5):
        v_m = v_k / 3.6
        l_mn = 0.5 * RHO_SL * v_m**2 * S_A380_M2 * CL_FLAP_LOF / 1e6
        if l_mn <= 6.48:
            pts_flap.append((xv(v_k), yl(l_mn)))
    els.append(poly(pts_flap, BLUE, 2.5))

    # 曲线 2：不放襟翼光洁机翼 (C_L = 0.85)，0 -> 430 km/h
    pts_clean = []
    for v_k in range(0, 431, 5):
        v_m = v_k / 3.6
        l_mn = 0.5 * RHO_SL * v_m**2 * S_A380_M2 * CL_CLEAN_SAFE / 1e6
        if l_mn <= 6.48:
            pts_clean.append((xv(v_k), yl(l_mn)))
    els.append(poly(pts_clean, SLATE, 2.0, dash="6,4"))

    # 关键点标注：半速点 (138.2 km/h, 1.41 MN)、放襟翼离地点 (276.3 km/h, 5.64 MN)、光洁翼离地点 (407.6 km/h, 5.64 MN)
    x_half, y_half = xv(138.2), yl(1.41)
    x_cln, y_cln = xv(407.6), yl(5.64)

    els.append(f'<circle cx="{x_half:.1f}" cy="{y_half:.1f}" r="4" fill="{ORANGE}"/>')
    els.append(txt(x_half + 8, y_half + 4, "半速仅 1/4 升力", 10, ORANGE, weight="700"))

    els.append(f'<circle cx="{x_cln:.1f}" cy="{y_cln:.1f}" r="4" fill="{SLATE}"/>')
    els.append(txt(x_cln - 6, y_cln + 24, "不放襟翼需 408 km/h", 10, SLATE, "end", weight="700"))

    # 放襟翼离地动态追踪圆点（终态停在 x_lof, y_lof）
    els.append(f'<g class="lift-dot-anim"><circle cx="{x_lof:.1f}" cy="{y_lof:.1f}" r="5.5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/></g>')
    els.append(txt(x_lof - 10, y_lof - 8, "放襟翼 276 km/h 离地！", 10.5, GREEN, "end", weight="700"))
    els.append(txt(gx0 + 10, yl(5.64) + 14, "575 t 离地门槛 (L = W = 5.64 MN)", 10, GREEN, weight="700"))

    # 下栏右：高原机场与失速红线精要卡
    els.append(card(490, 168, 250, 214))
    els.append(badge(504, 180, 198, 22, "三个一眼算穿的飞行现象", PURPLE_SOFT, PURPLE))
    els.append(txt(504, 218, "① 为什么要长跑道猛加速？", 11.5, INK, weight="700"))
    els.append(txt(504, 236, "L ∝ v²：从 138 加速到 276 km/h，", 10.5, BODY))
    els.append(txt(504, 252, "速度翻 2 倍，升力暴涨 4 倍！", 10.5, BLUE, weight="700"))

    els.append(txt(504, 278, "② 高原机场为什么更难起飞？", 11.5, INK, weight="700"))
    els.append(txt(504, 296, "海拔 4411 m 空气密度 ρ 少约 40%，", 10.5, BODY))
    els.append(txt(504, 312, "必须跑得更快或减载才能凑够升力。", 10.5, ORANGE, weight="700"))

    els.append(txt(504, 338, "③ 猛拉杆抬头为什么反会失速？", 11.5, INK, weight="700"))
    els.append(txt(504, 356, "迎角超 ~15° 边界层成片剥离，", 10.5, BODY))
    els.append(txt(504, 372, "翼背低压区垮塌，升力断崖暴跌！", 10.5, RED, weight="700"))

    return figure(
        394,
        "575吨客机跑道滑跑加速动画与速度平方升力曲线及襟翼增升作用图解",
        "上方按匀加速比例单次演示客机从静止滑跑至276千米每小时拉杆离地；下方精确绘制放襟翼（升力系数1.85，276千米每小时离地）与光洁机翼（升力系数0.85，需408千米每小时）的二次方升力曲线，标出半速138千米每小时仅得四分之一升力。",
        els,
        extra_css=extra_css,
        extra_defs=EXTRA_ARROWS,
    )


# ---------------------------------------------------------------------------
# 图 4：翼尖为什么往上翘？发动机为什么越造越“胖”？（翼尖涡 + 高涵道比涡扇）
# ---------------------------------------------------------------------------
def build_wingtip_vortex_and_turbofan() -> str:
    els = header(
        "图 4 · 坐飞机透过舷窗看到的两个秘密：上翘的翼尖小翼与“大肚子”涡扇发动机",
        "左看有限机翼如何抑制翼尖涡流省油；右看 10:1 高涵道比涡扇为什么“9 成冷风不进燃烧室”",
    )

    # 左卡：翼尖涡流、诱导阻力与翼尖小翼
    els.append(card(20, 64, 352, 274))
    els.append(badge(34, 76, 232, 22, "机翼末端：翼尖涡流与诱导阻力", PURPLE_SOFT, PURPLE))

    # 上半：无小翼机翼后视（下高压绕翼尖向上翻成一对旋涡）
    els.append(txt(196, 114, "无小翼平直翼尖（正后方视角）", 11, BODY, "middle", weight="700"))
    els.append(f'<ellipse cx="196" cy="144" rx="14" ry="14" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.8"/>')
    els.append(f'<line x1="88" y1="146" x2="182" y2="146" stroke="{INK}" stroke-width="4.0" stroke-linecap="round"/>')
    els.append(f'<line x1="210" y1="146" x2="304" y2="146" stroke="{INK}" stroke-width="4.0" stroke-linecap="round"/>')
    els.append(txt(136, 138, "低压 p_上", 9.5, BLUE, "middle", weight="700"))
    els.append(txt(136, 160, "高压 p_下", 9.5, ORANGE, "middle", weight="700"))
    # 左右翼尖绕流旋涡
    els.append(f'<path d="M 96 152 C 66 156, 62 126, 92 130 C 106 132, 102 146, 90 142" fill="none" stroke="{RED}" stroke-width="1.8" marker-end="url(#arr-red)"/>')
    els.append(f'<path d="M 296 152 C 326 156, 330 126, 300 130 C 286 132, 290 146, 302 142" fill="none" stroke="{RED}" stroke-width="1.8" marker-end="url(#arr-red)"/>')
    els.append(txt(196, 178, "高压气绕翼尖往上翻卷 → 拖出强烈翼尖涡！", 10.5, RED, "middle", weight="600"))

    # 下半：加装翼尖小翼（Winglets）+ 大展弦比公式
    els.append(card(34, 190, 324, 134, fill=PURPLE_SOFT, stroke=PURPLE))
    els.append(txt(196, 210, "✓ 现代客机解法：修长机翼 + 上翘翼尖小翼", 11, PURPLE, "middle", weight="700"))
    els.append(f'<ellipse cx="196" cy="240" rx="12" ry="12" fill="#ffffff" stroke="{PURPLE}" stroke-width="1.6"/>')
    # 带上翘小翼的机翼后视
    els.append(f'<path d="M 78 220 L 90 242 L 184 242" fill="none" stroke="{PURPLE}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')
    els.append(f'<path d="M 314 220 L 302 242 L 208 242" fill="none" stroke="{PURPLE}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')
    # 小得多的残余涡
    els.append(f'<circle cx="74" cy="218" r="6" fill="none" stroke="{TEAL}" stroke-width="1.3" stroke-dasharray="3,2"/>')
    els.append(f'<circle cx="318" cy="218" r="6" fill="none" stroke="{TEAL}" stroke-width="1.3" stroke-dasharray="3,2"/>')
    els.append(txt(48, 270, "• 诱导阻力 C_Di = C_L² / (π · e · AR)：升力的伴生代价", 10.5, INK, weight="600"))
    els.append(txt(48, 290, "• 小翼挡住上下串流，全航程实测省油 3%～5%！", 10.5, GREEN, weight="700"))
    els.append(txt(48, 310, "• 空管铁律：重型机身后尾流强劲，后机须隔数海里", 10, BODY))

    # 右卡：10:1 高涵道比涡扇发动机剖面与推进效率对比
    els.append(card(388, 64, 352, 274))
    els.append(badge(402, 74, 258, 22, "翼下巨兽：高涵道比涡扇（大流量慢加速）", BLUE_SOFT, BLUE))
    els.append(txt(564, 112, "外涵冷空气 (~90% 流量) → 贡献约 80% 推力！", 10.5, TEAL, "middle", weight="700"))

    # 涡扇发动机上下对称剖面示意 (x: 416 -> 694, 中心线 y=158)
    # 外涵短舱外壳
    els.append(f'<path d="M 424 120 Q 540 115 664 125 L 664 131 Q 540 122 424 127 Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
    els.append(f'<path d="M 424 196 Q 540 201 664 191 L 664 185 Q 540 194 424 189 Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
    # 前部大风扇叶片
    els.append(f'<rect x="440" y="125" width="10" height="66" rx="3" fill="{BLUE}" stroke="{INK}" stroke-width="1.0"/>')
    # 核心机（压气机+燃烧室+涡轮）居中偏窄
    els.append(f'<path d="M 464 143 L 642 147 L 656 152 L 656 164 L 642 169 L 464 173 Z" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
    els.append(txt(556, 162, "核心燃烧室 + 涡轮 (仅占 ~10% 空气)", 9.5, ORANGE, "middle", weight="700"))

    # 外涵道冷风流线（上下宽通道，贡献 ~80% 推力！）
    els.append(f'<line x1="402" y1="134" x2="704" y2="134" stroke="{TEAL}" stroke-width="2.2" marker-end="url(#arr-teal)"/>')
    els.append(f'<line x1="402" y1="182" x2="704" y2="182" stroke="{TEAL}" stroke-width="2.2" marker-end="url(#arr-teal)"/>')
    # 内涵道高温喷流
    els.append(f'<line x1="658" y1="158" x2="718" y2="158" stroke="{RED}" stroke-width="2.0" marker-end="url(#arr-red)"/>')

    # 下半推进效率公式与条形对比（同样 78 kN 巡航推力，v0 = 250 m/s）
    els.append(card(402, 208, 324, 116, fill=BLUE_SOFT, stroke=BLUE))
    els.append(txt(416, 226, "为什么不造细管猛喷火？推进效率 η_p = 2v₀/(v_e+v₀)：", 10.5, BLUE, weight="700"))

    # 涡扇条：86.2%
    els.append(txt(416, 250, "高涵道涡扇 (ṁ=975 kg/s, v_e=330)", 10, INK, weight="600"))
    els.append(f'<rect x="416" y="256" width="240" height="12" rx="3" fill="{GREEN}"/>')
    els.append(txt(664, 266, "86.2%", 10.5, GREEN, weight="700"))

    # 纯涡喷条：55.6%
    els.append(txt(416, 286, "老式纯涡喷 (ṁ=195 kg/s, v_e=650)", 10, MUTED, weight="600"))
    els.append(f'<rect x="416" y="292" width="155" height="12" rx="3" fill="{ORANGE}"/>')
    els.append(txt(579, 302, "55.6% (白扔大量动能)", 10.5, ORANGE, weight="700"))

    # 底部通栏：机翼与涡扇的共同哲学
    els.append(card(20, 348, 720, 38, fill=GREEN_SOFT, stroke=GREEN))
    els.append(
        txt(
            36,
            372,
            "共同物理哲学：推力/升力 ∝ ṁ·Δv，浪费动能 ∝ ṁ·(Δv)²——“温柔拨动巨量空气”永远比“暴力猛喷少量空气”省油得多！",
            11.5,
            INK,
            weight="600",
        )
    )

    return figure(
        398,
        "客机翼尖涡流与翼尖小翼省油机理及高涵道比涡扇发动机推进效率对比图",
        "左栏展示机翼下表面高压气绕翼尖翻卷形成翼尖涡与诱导阻力，加装上翘翼尖小翼可省油百分之三至五；右栏展示10比1高涵道比涡扇发动机约九成空气走外涵冷风道贡献八成推力，在250米每秒巡航时推进效率达86.2%，远高于纯涡喷的55.6%。",
        els,
        extra_defs=EXTRA_ARROWS,
    )


# ---------------------------------------------------------------------------
# 图 5：同样在天上飞，大客机、直升机/无人机、飞鸟与火箭到底有什么本质区别？
# ---------------------------------------------------------------------------
def build_sky_machines_comparison() -> str:
    els = header(
        "图 5 · 都在天上飞，谁在“划空气”、谁在“自己喷工质”？四类飞行器全景对照",
        "全部遵守牛顿第三定律，但“推谁、往哪推、能不能悬停、抽空空气会怎样”截然不同",
    )

    cols = [
        (
            20,
            "① 固定翼大客机",
            "空客 A380 / C919",
            BLUE,
            BLUE_SOFT,
            "发动机往后推空气",
            "固定机翼往下导空气",
            "❌ 不能悬停（须保持空速）",
            "升阻比 L/D ≈ 17～20（极省油）",
            "升力与推力双双归零，坠落",
        ),
        (
            202,
            "② 旋翼机 / 航拍无人机",
            "直升机 / 四旋翼",
            TEAL,
            TEAL_SOFT,
            "旋翼倾斜分力向前推",
            "旋转桨叶高速兜圈下压空气",
            "✓ 可原地悬停与垂直起降",
            "等效升阻比 ≈ 4～5（悬停费能）",
            "旋翼抓不到空气，无法起飞",
        ),
        (
            384,
            "③ 扑翼飞鸟",
            "白鸽 / 信天翁",
            ORANGE,
            ORANGE_SOFT,
            "翅膀下拍斜向后下方拍气",
            "同一对翅膀包揽升力+推力",
            "△ 蜂鸟可长期悬停，大鸟难",
            "信天翁滑翔 L/D ≈ 20",
            "无法扑翼，也无法呼吸",
        ),
        (
            566,
            "④ 运载火箭",
            "长征五号 / 星舰",
            PURPLE,
            PURPLE_SOFT,
            "向后/下高速喷自带燃气",
            "靠推力硬顶或入轨自由落体",
            "✓ 推重比 > 1 可垂直拔起",
            "几分钟烧光百吨推进剂",
            "✓ 真空无阻力，喷管推力更大！",
        ),
    ]

    row_labels = [
        ("靠什么前进", 162),
        ("靠什么抗重力", 206),
        ("能否原地悬停", 250),
        ("巡航经济性", 294),
        ("若抽干空气", 338),
    ]

    for x0, title_s, sub_s, col, soft, r1, r2, r3, r4, r5 in cols:
        els.append(card(x0, 64, 174, 312))
        els.append(f'<rect x="{x0}" y="64" width="174" height="58" rx="10" fill="{soft}" stroke="{col}" stroke-width="1.2"/>')
        els.append(txt(x0 + 87, 88, title_s, 12.5, col, "middle", weight="700"))
        els.append(txt(x0 + 87, 109, sub_s, 10.5, BODY, "middle", weight="600"))

        vals = [r1, r2, r3, r4, r5]
        for (lbl, yy), val in zip(row_labels, vals):
            els.append(f'<line x1="{x0 + 10}" y1="{yy - 26}" x2="{x0 + 164}" y2="{yy - 26}" stroke="{HAIRLINE}" stroke-width="1"/>')
            els.append(txt(x0 + 12, yy - 11, lbl, 9.5, MUTED, weight="700"))
            val_col = GREEN if val.startswith("✓") else (RED if val.startswith("❌") else INK)
            els.append(txt(x0 + 12, yy + 7, val, 10.5, val_col, weight="600"))

    return figure(
        390,
        "固定翼客机、直升机与四旋翼无人机、扑翼飞鸟及运载火箭四类飞行原理对照图",
        "四列卡片横向对比固定翼大客机、直升机与四旋翼无人机、扑翼飞鸟、运载火箭在前进推力来源、抗重力升力机制、原地悬停能力、巡航经济性及真空环境表现五个维度的物理差异。",
        els,
    )


@register(TOPIC, "几百吨大飞机升力、环流压差、起飞v²动画与高涵道比涡扇图解", "mechanics_sky")
def build_all() -> list[str]:
    verify_heavy_flight_math()
    out = [
        write_svg(TOPIC, "airliner-force-leverage.svg", build_airliner_force_leverage()),
        write_svg(TOPIC, "kutta-circulation-pressure.svg", build_kutta_circulation_pressure()),
        write_svg(TOPIC, "takeoff-roll-lift-anim.svg", build_takeoff_roll_lift_anim()),
        write_svg(TOPIC, "wingtip-vortex-and-turbofan.svg", build_wingtip_vortex_and_turbofan()),
        write_svg(TOPIC, "sky-machines-comparison.svg", build_sky_machines_comparison()),
    ]
    return [str(p) for p in out]
