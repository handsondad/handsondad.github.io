"""
Visuals for '电压、电流和电阻：电是如何跨越千里传进家门，又在电子元器件里精准干活的'
(Voltage, Current, Resistance, UHV Power Transmission, R/C/L Passive Components,
Diode/MOSFET Active Components, and 220V AC -> 5V DC Charger Full Pipeline).

Generates 6 original 760px Chinese SVG diagrams in assets/images/voltage-current-resistance/
with verified mathematical and circuit physics assertions.
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
    step_badge,
    txt,
    write_svg,
)

TOPIC = "voltage-current-resistance"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"

# Exact & verified constants
E_CHARGE = 1.602176634e-19  # C (2019 SI exact definition)
ELECTRONS_PER_AMP_SEC = 1.0 / E_CHARGE  # 6.241509074e18


def verify_circuit_math() -> None:
    # 1. SI Ampere exact count
    assert abs(ELECTRONS_PER_AMP_SEC - 6.241509074460763e18) < 1e6

    # 2. LED ballast resistor example: Vs = 5.0 V, Vf = 2.0 V, I = 20 mA = 0.02 A -> R = 150 Ohm
    vs, vf, i_target = 5.0, 2.0, 0.020
    r_led = (vs - vf) / i_target
    p_res = (i_target**2) * r_led
    p_led = vf * i_target
    p_src = vs * i_target
    assert abs(r_led - 150.0) < 1e-12
    assert abs(p_res - 0.060) < 1e-12  # 60 mW
    assert abs(p_led - 0.040) < 1e-12  # 40 mW
    assert abs(p_res + p_led - p_src) < 1e-12  # KVL / energy conservation: 60 + 40 = 100 mW

    # 3. High-voltage transmission comparison: P = 10 MW = 1e7 W, R_line = 10 Ohm
    p_tx, r_line = 10.0e6, 10.0
    v_low, v_high = 10.0e3, 500.0e3
    i_low = p_tx / v_low  # 1000 A
    i_high = p_tx / v_high  # 20 A
    loss_low = (i_low**2) * r_line  # 10 MW (100% lost in toy V=P/I limit!)
    loss_high = (i_high**2) * r_line  # 4000 W = 4 kW (0.04%!)
    assert abs(i_low - 1000.0) < 1e-9
    assert abs(i_high - 20.0) < 1e-9
    assert abs(loss_high - 4000.0) < 1e-9
    assert abs((loss_low / loss_high) - (50.0**2)) < 1e-6  # 2500x reduction!

    # 4. RC charging curve: Vs = 5.0 V, R = 1000 Ohm, C = 1000 uF = 1e-3 F -> tau = 1.0 s
    tau = 1000.0 * 1.0e-3
    assert abs(tau - 1.0) < 1e-12
    v_1tau = 5.0 * (1.0 - math.exp(-1.0))
    v_3tau = 5.0 * (1.0 - math.exp(-3.0))
    v_5tau = 5.0 * (1.0 - math.exp(-5.0))
    assert abs(v_1tau / 5.0 - 0.6321205588) < 1e-8
    assert abs(v_3tau / 5.0 - 0.9502129316) < 1e-8
    assert abs(v_5tau / 5.0 - 0.9932620530) < 1e-8

    # 5. AC peak & rectifier ripple: 220 Vrms -> 311.13 Vpk; 12 Vrms -> 16.97 Vpk -> ~15.6 V after 2 Si diodes
    v_ac_pk = 220.0 * math.sqrt(2.0)
    assert abs(v_ac_pk - 311.1269837) < 1e-6
    v_sec_pk = 12.0 * math.sqrt(2.0)
    assert abs(v_sec_pk - 16.9705627) < 1e-6


def _zigzag_h(x0: float, x1: float, y: float, peaks: int = 5, amp: float = 6.5) -> str:
    pts = [(x0, y), (x0 + 8, y)]
    span = (x1 - 8) - (x0 + 8)
    n = peaks * 2
    for k in range(1, n):
        xk = x0 + 8 + span * k / n
        yk = y - amp if k % 2 == 1 else y + amp
        pts.append((xk, yk))
    pts.extend([(x1 - 8, y), (x1, y)])
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)


# ---------------------------------------------------------------------------
# 图 1：电压 V、电流 I、电阻 R 的物理定义与 LED 限流电阻算例
# ---------------------------------------------------------------------------
def build_vir_triad() -> str:
    els = header(
        "图 1 · 电世界的三位主角：电压推、电流跑、电阻拦",
        "先看三张角色卡抓准单位与物理意义，再看下方 5 V 点亮红光 LED 的完整分压算账",
    )

    cards = [
        (
            20,
            "电压 V（伏特 Volt）",
            "1 V = 1 J / C",
            "每 1 库仑电荷获得的能量落差",
            "像水箱的高度差：没落差就不流动",
            "例：干电池 1.5 V ｜ USB 5 V ｜ 插座 220 V",
            BLUE,
            BLUE_SOFT,
        ),
        (
            266,
            "电流 I（安培 Ampere）",
            "1 A = 1 C / s",
            "每秒流过截面的电荷总量",
            "1 A ≈ 每秒 6.24×10¹⁸ 颗电子过关",
            "例：LED 0.02 A ｜ 手机快充 5 A ｜ 烧水壶 8 A",
            GREEN,
            GREEN_SOFT,
        ),
        (
            512,
            "电阻 R（欧姆 Ohm）",
            "R = ρ · L / A",
            "材料晶格对电荷定向移动的阻碍",
            "越细越长越难走，撞击晶格变成热",
            "例：1 m 铜线约 0.011 Ω ｜ 干燥皮肤数千 Ω",
            ORANGE,
            ORANGE_SOFT,
        ),
    ]
    for x0, title, unit, mean, meta, ex, col, soft in cards:
        els.append(card(x0, 62, 228, 150, fill=CARD_BG, stroke=col, sw=1.3))
        els.append(f'<rect x="{x0}" y="{x0 * 0 + 62}" width="228" height="30" rx="10" fill="{soft}"/>')
        els.append(f'<rect x="{x0}" y="82" width="228" height="10" fill="{soft}"/>')
        els.append(txt(x0 + 114, 82, title, 12.5, col, "middle", weight="700"))
        els.append(txt(x0 + 114, 112, unit, 13, INK, "middle", weight="700", cls="mono"))
        els.append(txt(x0 + 114, 136, mean, 11.5, BODY, "middle"))
        els.append(txt(x0 + 114, 158, meta, 11.5, MUTED, "middle"))
        els.append(txt(x0 + 114, 194, ex, 11, col, "middle", weight="600"))

    # 下方实战回路：5V USB -> 150 Ω 电阻 -> 2.0V 红光 LED (20 mA)
    els.append(card(20, 226, 720, 148, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(36, 250, "实战算账：为什么 5 V 电源绝不能直接捅进 2 V 的红光 LED？", 13, INK, weight="700"))

    # 绘制串联回路简图 (左侧 x=44..416, y=268..354)
    els.append(card(36, 262, 396, 98, fill=CARD_BG, stroke=BORDER))
    # 导线框
    els.append(f'<path d="M78 338 L78 292 L146 292" fill="none" stroke="{SLATE}" stroke-width="1.8"/>')
    els.append(f'<polyline points="{_zigzag_h(146, 232, 292)}" fill="none" stroke="{ORANGE}" stroke-width="2"/>')
    els.append(f'<path d="M232 292 L292 292" fill="none" stroke="{SLATE}" stroke-width="1.8"/>')
    # LED 符号 (三角形 + 竖线)
    els.append(f'<polygon points="292,281 292,303 314,292" fill="{RED_SOFT}" stroke="{RED}" stroke-width="1.8"/>')
    els.append(f'<line x1="315" y1="280" x2="315" y2="304" stroke="{RED}" stroke-width="2"/>')
    # 光线小箭头
    els.append(f'<path d="M312 276 L322 267 M320 280 L330 271" stroke="{RED}" stroke-width="1.3"/>')
    els.append(f'<path d="M315 292 L386 292 L386 338 L78 338" fill="none" stroke="{SLATE}" stroke-width="1.8"/>')
    # 电源符号（在左竖线上覆盖白色背景）
    els.append(f'<rect x="64" y="305" width="28" height="18" fill="{CARD_BG}"/>')
    els.append(f'<line x1="66" y1="310" x2="90" y2="310" stroke="{BLUE}" stroke-width="2.4"/>')
    els.append(f'<line x1="71" y1="319" x2="85" y2="319" stroke="{BLUE}" stroke-width="1.8"/>')
    els.append(txt(60, 318, "5 V", 11.5, BLUE, "end", weight="700"))

    # 元件标注
    els.append(txt(189, 278, "R = 150 Ω（替身挡压 3 V）", 11.5, ORANGE, "middle", weight="700"))
    els.append(txt(308, 320, "LED 压降 2.0 V", 11.5, RED, "middle", weight="600"))
    els.append(f'<path d="M200 338 L248 338" stroke="{GREEN}" stroke-width="2" marker-end="url(#arr-green)"/>')
    els.append(txt(224, 353, "回路电流 I = 20 mA (0.02 A)", 11.5, GREEN, "middle", weight="700"))

    # 右侧分步公式核对
    els.append(txt(448, 282, "① 扣掉灯珠压降：ΔV = 5.0 − 2.0 = 3.0 V", 12, BODY))
    els.append(txt(448, 305, "② 欧姆定律配阻：R = 3.0 V ÷ 0.02 A = 150 Ω", 12, ORANGE, weight="700"))
    els.append(txt(448, 328, "③ 能量守恒去向：总输入 5 V × 20 mA = 100 mW", 12, BODY))
    els.append(txt(448, 350, "   电阻发热 60 mW + 灯珠耗电 40 mW = 100 mW ✓", 11.5, GREEN, weight="700"))

    return figure(
        388,
        "电压、电流与电阻的三元关系及LED串联限流算例",
        "上方三卡定义电压（每库仑焦耳数）、电流（每秒库仑数，1安约6.24乘10的18次方个电子每秒）与电阻（材料几何阻碍）；下方用5伏电源串联150欧限流电阻驱动2伏红光LED的回路演示欧姆定律与功率守恒。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 2：为什么远距离输电必须升到几十万伏？P = V·I 与 ΔP = I²R 算账对比
# ---------------------------------------------------------------------------
def build_high_voltage_tx() -> str:
    els = header(
        "图 2 · 为什么高压线非要升到 500 kV 甚至 1100 kV？",
        "输送同样 10 MW 功率、走同样 R = 10 Ω 的长导线：电压抬高 50 倍，发热损耗骤降 2500 倍",
    )

    # 上栏：低压直供反例 (10 kV)
    els.append(card(20, 62, 720, 108, fill=RED_SOFT, stroke=RED, sw=1.2))
    els.append(pill(34, 74, "反例：只用 10 kV 低压硬送 10 MW", fg=RED, bg="#ffffff", w=244))
    els.append(txt(292, 90, "所需电流 I = P ÷ V = 10,000,000 W ÷ 10,000 V = 1000 A", 12, INK, weight="700"))
    # 能量条：100% 烧在路上
    els.append(txt(36, 120, "导线发热 I²R：", 11.5, BODY, weight="600"))
    els.append(f'<rect x="132" y="106" width="420" height="20" rx="6" fill="{RED}"/>')
    els.append(txt(342, 121, "1000² × 10 Ω = 10 MW（100% 功率全把铁塔电线烧成电炉！）", 11.5, "#ffffff", "middle", weight="700"))
    els.append(txt(564, 121, "到站可用：0 MW", 12, RED, weight="700"))
    els.append(txt(36, 152, "误区拆解：不能直接套 V²/R 算线损！长导线两端的“压降 ΔV = I·R”远小于电网对地电压 V。", 11.5, MUTED))

    # 下栏：特高压输电正例 (500 kV)
    els.append(card(20, 184, 720, 112, fill=GREEN_SOFT, stroke=GREEN, sw=1.2))
    els.append(pill(34, 196, "正解：升压 50 倍到 500 kV 再送 10 MW", fg=GREEN, bg="#ffffff", w=264))
    els.append(txt(312, 212, "所需电流 I = 10,000,000 W ÷ 500,000 V = 20 A（缩小到 1/50）", 12, INK, weight="700"))
    els.append(txt(36, 244, "功率去向对比：", 11.5, BODY, weight="600"))
    els.append(f'<rect x="132" y="230" width="420" height="20" rx="6" fill="{GREEN}"/>')
    # 极细损耗条示意
    els.append(f'<rect x="132" y="230" width="4" height="20" fill="{ORANGE}"/>')
    els.append(txt(342, 245, "99.96% 功率（9.996 MW）稳稳送到远方城市", 11.5, "#ffffff", "middle", weight="700"))
    els.append(txt(564, 245, "线损仅 4 kW (0.04%)", 12, GREEN, weight="700"))
    els.append(
        txt(
            36,
            278,
            "核对：I²R = 20² × 10 Ω = 4,000 W = 4 kW；电压升 k 倍 → 电流降为 1/k → 导线损耗降为 1/k²（50² = 2500 倍）。",
            11.5,
            BODY,
        )
    )

    # 底部：发电厂到插座的五级阶梯
    els.append(card(20, 310, 720, 74, fill=CARD_BG, stroke=BORDER))
    stages = [
        (32, 122, "发电机出口", "10–20 kV", BLUE, BLUE_SOFT),
        (174, 134, "升压变电站", "220–1100 kV", PURPLE, PURPLE_SOFT),
        (328, 126, "城市降压站", "110 / 10 kV", TEAL, TEAL_SOFT),
        (474, 122, "小区配电箱", "380 / 220 V", GREEN, GREEN_SOFT),
        (616, 112, "手机充电头", "5–20 V DC", ORANGE, ORANGE_SOFT),
    ]
    for x0, w, name, val, col, soft in stages:
        els.append(card(x0, 322, w, 50, rx=8, fill=soft, stroke=col))
        els.append(txt(x0 + w / 2, 342, name, 11.5, col, "middle", weight="700"))
        els.append(txt(x0 + w / 2, 361, val, 11.5, INK, "middle", weight="600"))
    for ax in (156, 310, 456, 598):
        els.append(f'<path d="M{ax} 347 L{ax + 15} 347" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')

    return figure(
        398,
        "高压输电减损原理：10千伏与500千伏输送10兆瓦功率的线损对比及电网五级变压阶梯",
        "对比输送10兆瓦功率经过10欧导线：10千伏需1000安电流，线损高达10兆瓦；升压50倍至500千伏仅需20安电流，线损降至4千瓦（0.04%，缩小2500倍）。底部列出从发电机10至20千伏、特高压220至1100千伏、城市10千伏、入户220伏到充电头5至20伏的五级阶梯。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 3：无源三兄弟（电阻 R、电容 C、电感 L）——耗能 vs 电场储能 vs 磁场储能
# ---------------------------------------------------------------------------
def build_passive_rcl() -> str:
    els = header(
        "图 3 · 电路板上的“无源三兄弟”：一个耗能分压，两个一快一慢吞吐能量",
        "它们不需要额外供电就能工作，靠完全不同的脾气把粗糙电流驯服成干净信号",
    )

    cols = [
        (
            20,
            "电阻 R · 节流阀与分压尺",
            "V = I · R",
            BLUE,
            BLUE_SOFT,
            "能量脾气：只耗能、不储能（变焦耳热）",
            "对频率态度：直流交流一视同仁",
            "拿手活：限流护灯、串联分压、采样电流",
        ),
        (
            266,
            "电容 C · 极板蓄水池",
            "I = C · dV/dt",
            GREEN,
            GREEN_SOFT,
            "能量脾气：电场储能 E = ½ C V²",
            "核心铁律：两端电压 V 不能瞬间突变",
            "拿手活：隔直通交、滤除电源电压纹波",
        ),
        (
            512,
            "电感 L · 电流大飞轮",
            "V = L · dI/dt",
            PURPLE,
            PURPLE_SOFT,
            "能量脾气：磁场储能 E = ½ L I²",
            "核心铁律：流过电流 I 不能瞬间突变",
            "拿手活：通直阻交、开关电源升降压储能",
        ),
    ]

    for idx, (x0, title, eq, col, soft, line1, line2, line3) in enumerate(cols):
        els.append(card(x0, 62, 228, 252, fill=CARD_BG, stroke=col, sw=1.3))
        els.append(f'<rect x="{x0}" y="62" width="228" height="30" rx="10" fill="{soft}"/>')
        els.append(f'<rect x="{x0}" y="82" width="228" height="10" fill="{soft}"/>')
        els.append(txt(x0 + 114, 82, title, 12.5, col, "middle", weight="700"))

        # 中部画标准符号框
        els.append(card(x0 + 16, 102, 196, 66, rx=8, fill=SLATE_SOFT, stroke=HAIRLINE))
        cy = 135.0
        if idx == 0:
            els.append(f'<line x1="{x0 + 34}" y1="{cy}" x2="{x0 + 70}" y2="{cy}" stroke="{SLATE}" stroke-width="1.8"/>')
            els.append(f'<polyline points="{_zigzag_h(x0 + 70, x0 + 158, cy, peaks=5, amp=9)}" fill="none" stroke="{col}" stroke-width="2.2"/>')
            els.append(f'<line x1="{x0 + 158}" y1="{cy}" x2="{x0 + 194}" y2="{cy}" stroke="{SLATE}" stroke-width="1.8"/>')
        elif idx == 1:
            els.append(f'<line x1="{x0 + 34}" y1="{cy}" x2="{x0 + 106}" y2="{cy}" stroke="{SLATE}" stroke-width="1.8"/>')
            els.append(f'<line x1="{x0 + 106}" y1="{cy - 18}" x2="{x0 + 106}" y2="{cy + 18}" stroke="{col}" stroke-width="3"/>')
            els.append(f'<line x1="{x0 + 122}" y1="{cy - 18}" x2="{x0 + 122}" y2="{cy + 18}" stroke="{col}" stroke-width="3"/>')
            els.append(f'<line x1="{x0 + 122}" y1="{cy}" x2="{x0 + 194}" y2="{cy}" stroke="{SLATE}" stroke-width="1.8"/>')
            els.append(txt(x0 + 96, cy - 10, "+", 12, col, "end", weight="700"))
            els.append(txt(x0 + 132, cy - 10, "−", 12, col, "start", weight="700"))
        else:
            els.append(f'<line x1="{x0 + 34}" y1="{cy + 6}" x2="{x0 + 66}" y2="{cy + 6}" stroke="{SLATE}" stroke-width="1.8"/>')
            coils = (
                f"M{x0 + 66},{cy + 6} "
                f"A12,14 0 0,1 {x0 + 90},{cy + 6} "
                f"A12,14 0 0,1 {x0 + 114},{cy + 6} "
                f"A12,14 0 0,1 {x0 + 138},{cy + 6} "
                f"A12,14 0 0,1 {x0 + 162},{cy + 6}"
            )
            els.append(f'<path d="{coils}" fill="none" stroke="{col}" stroke-width="2.2"/>')
            els.append(f'<line x1="{x0 + 162}" y1="{cy + 6}" x2="{x0 + 194}" y2="{cy + 6}" stroke="{SLATE}" stroke-width="1.8"/>')

        els.append(txt(x0 + 114, 190, eq, 13.5, INK, "middle", weight="700", cls="mono"))
        els.append(txt(x0 + 16, 218, line1, 11.5, BODY))
        els.append(txt(x0 + 16, 242, line2, 11.5, col, weight="700"))
        els.append(txt(x0 + 16, 266, line3, 11.5, BODY))
        els.append(
            txt(
                x0 + 16,
                294,
                ["阻抗 Z_R = R（与频率无关）", "容抗 X_C = 1/(2πfC)（高频易过）", "感抗 X_L = 2πfL（高频难过）"][idx],
                11,
                MUTED,
            )
        )

    els.append(card(20, 328, 720, 44, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(
        txt(
            36,
            355,
            "一句话记牢：电阻把多余能量变热散掉；电容像水库“削峰填谷”稳住电压；电感像重飞轮“拒快迎慢”稳住电流。",
            12,
            INK,
            weight="600",
        )
    )

    return figure(
        386,
        "无源电子元器件三兄弟对比：电阻耗能分压、电容电场储能稳压、电感磁场储能稳流",
        "三栏并列展示电阻R（V=IR，焦耳热耗能，阻抗与频率无关）、电容C（I=C dV/dt，极板电场储能，电压不能突变，容抗随频率升高而减小）与电感L（V=L dI/dt，线圈磁场储能，电流不能突变，感抗随频率升高而增大）。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 4：RC 充电过程动画（单次播放停在终态，展示电压渐升、电流渐衰）
# ---------------------------------------------------------------------------
def build_rc_charging_anim() -> str:
    # 模型参数：Vs = 5 V, R = 1 kΩ, C = 1000 μF -> τ = R·C = 1.0 s
    # 真实时间 0..5.0 s (5τ)；动画按 1:0.7 压缩为 3.5 s 线性扫描，单次停在完整曲线
    x0, x1 = 96.0, 436.0  # 340 px 对应 0..5τ
    y_bot, y_top = 276.0, 116.0  # 160 px 对应 0..5.0 V (或 0..5.0 mA)
    t_max = 5.0

    v_pts = []
    i_pts = []
    for k in range(101):
        t = t_max * k / 100.0
        px = x0 + (x1 - x0) * (t / t_max)
        vc_ratio = 1.0 - math.exp(-t)
        ic_ratio = math.exp(-t)
        v_pts.append(f"{px:.2f},{y_bot - (y_bot - y_top) * vc_ratio:.2f}")
        i_pts.append(f"{px:.2f},{y_bot - (y_bot - y_top) * ic_ratio:.2f}")

    dur = 3.2
    delay = 0.6
    extra_css = f"""
  @keyframes rcSweep {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  @keyframes rcFade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  .rc-mask-rect {{
    transform-box: view-box;
    transform-origin: {x0:.1f}px 0px;
    animation: rcSweep {dur}s linear {delay}s 1 backwards;
  }}
  .rc-done {{ animation: rcFade 0.45s ease-out {delay + dur:.2f}s 1 backwards; }}
  @media (prefers-reduced-motion: reduce) {{
    .rc-mask-rect, .rc-done {{ animation: none !important; }}
  }}
"""
    extra_defs = f"""
  <clipPath id="rc-reveal">
    <rect class="rc-mask-rect" x="{x0:.1f}" y="86" width="{x1 - x0 + 8:.1f}" height="215"/>
  </clipPath>"""

    els = header(
        "图 4 · 电容充电慢动作：为什么刚合闸时电流最大、充满后电流归零？",
        "算例：5 V 电源经 R = 1 kΩ 给 C = 1000 μF 充电（时间常数 τ = R·C = 1.0 s）；动画约 3.8 秒单次停在终态",
    )

    # 左：曲线坐标系
    els.append(card(20, 64, 452, 266))
    els.append(txt(38, 88, "电容电压 V_C(t) 与充电电流 I(t) 实算曲线", 12.5, INK, weight="700"))

    # 水平参考网格 (0%, 63.2%, 100%)
    y_63 = y_bot - (y_bot - y_top) * (1.0 - math.exp(-1.0))
    els.append(f'<line x1="{x0}" y1="{y_top}" x2="{x1}" y2="{y_top}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="4 3"/>')
    els.append(f'<line x1="{x0}" y1="{y_63:.2f}" x2="{x1}" y2="{y_63:.2f}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    els.append(f'<line x1="{x0}" y1="{y_bot}" x2="{x1 + 8}" y2="{y_bot}" stroke="{SLATE}" stroke-width="1.5"/>')
    els.append(f'<line x1="{x0}" y1="{y_top - 8}" x2="{x0}" y2="{y_bot}" stroke="{SLATE}" stroke-width="1.5"/>')

    # Y 轴刻度
    els.append(txt(x0 - 8, y_top + 4, "5.0 V / 5 mA", 11, MUTED, "end"))
    els.append(txt(x0 - 8, y_63 + 4, "3.16 V (63%)", 11, GREEN, "end", weight="600"))
    els.append(txt(x0 - 8, y_bot + 4, "0", 11, MUTED, "end"))

    # X 轴刻度 0, 1τ, 2τ, 3τ, 4τ, 5τ
    for k in range(6):
        tx = x0 + (x1 - x0) * (k / 5.0)
        els.append(f'<line x1="{tx:.1f}" y1="{y_bot}" x2="{tx:.1f}" y2="{y_bot + 5}" stroke="{SLATE}" stroke-width="1.3"/>')
        lab = "0" if k == 0 else f"{k}τ ({k}s)"
        els.append(txt(tx, y_bot + 19, lab, 11, MUTED, "middle"))

    # 静态浅色底线（保证初态或不支持动画时也完整可读）
    els.append(f'<polyline points="{" ".join(v_pts)}" fill="none" stroke="{GREEN}" stroke-opacity="0.22" stroke-width="2" stroke-dasharray="4 3"/>')
    els.append(f'<polyline points="{" ".join(i_pts)}" fill="none" stroke="{ORANGE}" stroke-opacity="0.22" stroke-width="2" stroke-dasharray="4 3"/>')

    # 动态揭示实线
    els.append('<g clip-path="url(#rc-reveal)">')
    els.append(f'<polyline points="{" ".join(v_pts)}" fill="none" stroke="{GREEN}" stroke-width="2.6"/>')
    els.append(f'<polyline points="{" ".join(i_pts)}" fill="none" stroke="{ORANGE}" stroke-width="2.4" stroke-dasharray="6 3"/>')
    els.append("</g>")

    # 关键点标注 (1τ, 3τ, 5τ)
    x_1t = x0 + (x1 - x0) * (1.0 / 5.0)
    x_3t = x0 + (x1 - x0) * (3.0 / 5.0)
    y_3t = y_bot - (y_bot - y_top) * (1.0 - math.exp(-3.0))
    els.append(f'<circle cx="{x_1t:.1f}" cy="{y_63:.2f}" r="3.8" fill="{GREEN}"/>')
    els.append(f'<line x1="{x_1t:.1f}" y1="{y_63:.2f}" x2="{x_1t:.1f}" y2="{y_bot}" stroke="{GREEN}" stroke-width="1.1" stroke-dasharray="3 2"/>')
    els.append(f'<circle cx="{x_3t:.1f}" cy="{y_3t:.2f}" r="3.5" fill="{GREEN}"/>')

    # 图例与终态读数
    els.append('<g class="rc-done">')
    els.append(txt(x_3t - 8, y_3t + 26, "3τ 充到 95.0%", 11.5, GREEN, "middle", weight="700", halo=True))
    els.append(txt(x1 - 4, y_top - 4, "绿实线 V_C：5τ 达 99.3% (4.97 V)", 11.5, GREEN, "end", weight="700", halo=True))
    els.append(txt(x1 - 4, y_bot - 14, "橙虚线 I(t)：从 5 mA 衰减至 ≈0", 11.5, ORANGE, "end", weight="700", halo=True))
    els.append("</g>")
    els.append(txt(246, 318, "时间 t（τ = R·C = 1.0 s）", 11.5, INK, "middle", weight="600"))

    # 右：三步物理拆解卡片
    els.append(card(488, 64, 252, 266))
    els.append(txt(504, 88, "三个时刻发生了什么？", 12.5, INK, weight="700"))
    steps = [
        (
            104,
            "① t = 0⁺ 刚合闸瞬间",
            "极板还是空的（V_C = 0 V），",
            "5 V 落差全压在电阻上：",
            "I(0) = 5 V ÷ 1 kΩ = 5 mA 最大",
            ORANGE,
            ORANGE_SOFT,
        ),
        (
            178,
            "② t = 1τ（1.0 秒）",
            "极板攒起电荷，反向顶住电源；",
            "V_C 升到 63.2%（3.16 V），",
            "电流降到 36.8%（1.84 mA）",
            BLUE,
            BLUE_SOFT,
        ),
        (
            252,
            "③ t ≥ 5τ（5.0 秒后）",
            "极板电压几乎追平 5.0 V，",
            "电阻两端没了落差（ΔV ≈ 0），",
            "直流电流停步 →“隔直”生效",
            GREEN,
            GREEN_SOFT,
        ),
    ]
    for sy, st, l1, l2, l3, col, soft in steps:
        els.append(card(502, sy, 224, 66, rx=8, fill=soft, stroke=col))
        els.append(txt(512, sy + 18, st, 11.5, col, weight="700"))
        els.append(txt(512, sy + 36, l1, 11, BODY))
        els.append(txt(512, sy + 52, l3, 11, INK, weight="600"))

    return figure(
        344,
        "RC电容充电动态过程：电容电压指数上升与充电电流指数衰减",
        "左侧按V_C(t)=5(1-e^(-t/tau))和I(t)=5e^(-t/tau)精确绘制5伏经1千欧给1000微法电容充电曲线（tau=1秒）：1tau充至63.2%，3tau达95.0%，5tau达99.3%；右侧分三步解释刚合闸最大电流、半程反顶与充满隔直。",
        els,
        extra_css=extra_css,
        extra_defs=extra_defs,
    )


# ---------------------------------------------------------------------------
# 图 5：半导体两件套——二极管（单向止回阀）与 MOSFET 晶体管（电控水龙头）
# ---------------------------------------------------------------------------
def build_semiconductor_duo() -> str:
    els = header(
        "图 5 · 半导体登场：从“只许单向走”的二极管，到“小电压控大电流”的晶体管",
        "打破线性欧姆定律！正是这两件有源器件，把死板的电路变成了会整流、会计算的数字芯片",
    )

    # 左卡：PN 结二极管
    els.append(card(20, 64, 350, 266))
    els.append(txt(36, 88, "① 二极管（PN 结）：电流的单向旋转门", 13, BLUE, weight="700"))

    # 正向导通小框
    els.append(card(36, 102, 318, 82, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    els.append(txt(48, 122, "正向偏置（P 接正、N 接负，跨过约 0.7 V 门槛）", 11.5, GREEN, weight="700"))
    els.append(f'<rect x="52" y="134" width="64" height="34" rx="5" fill="#dbeafe" stroke="{BLUE}"/>')
    els.append(txt(84, 155, "P 区", 12, BLUE, "middle", weight="700"))
    els.append(f'<rect x="116" y="134" width="12" height="34" fill="#e2e8f0"/>')
    els.append(f'<rect x="128" y="134" width="64" height="34" rx="5" fill="#fef3c7" stroke="{ORANGE}"/>')
    els.append(txt(160, 155, "N 区", 12, ORANGE, "middle", weight="700"))
    els.append(f'<path d="M40 151 L208 151" stroke="{GREEN}" stroke-width="2.2" marker-end="url(#arr-green)"/>')
    els.append(txt(220, 147, "耗尽层被压窄", 11.5, INK, weight="700"))
    els.append(txt(220, 165, "闸门大开，顺畅导通", 11.5, GREEN, weight="600"))

    # 反向截止小框
    els.append(card(36, 194, 318, 82, rx=8, fill=RED_SOFT, stroke=RED))
    els.append(txt(48, 214, "反向偏置（P 接负、N 接正，未达击穿电压）", 11.5, RED, weight="700"))
    els.append(f'<rect x="52" y="226" width="48" height="34" rx="5" fill="#dbeafe" stroke="{BLUE}"/>')
    els.append(txt(76, 247, "P 区", 12, BLUE, "middle", weight="700"))
    els.append(f'<rect x="100" y="226" width="44" height="34" fill="#cbd5e1" stroke="{SLATE}" stroke-dasharray="3 2"/>')
    els.append(txt(122, 247, "宽墙", 11, SLATE, "middle", weight="700"))
    els.append(f'<rect x="144" y="226" width="48" height="34" rx="5" fill="#fef3c7" stroke="{ORANGE}"/>')
    els.append(txt(168, 247, "N 区", 12, ORANGE, "middle", weight="700"))
    els.append(txt(214, 239, "耗尽层被拉宽成绝缘墙", 11.5, INK, weight="700"))
    els.append(txt(214, 257, "电流几乎为 0，倒流堵死", 11.5, RED, weight="600"))

    els.append(txt(36, 300, "代表分工：整流桥把交流掰成单向直流；", 11.5, BODY))
    els.append(txt(36, 318, "发光二极管（LED）让复合能量直接变成光子。", 11.5, BODY))

    # 右卡：MOSFET 场效应晶体管
    els.append(card(390, 64, 350, 266))
    els.append(txt(406, 88, "② MOSFET 晶体管：不费力气的“电控水龙头”", 13, PURPLE, weight="700"))

    # 截止态 V_GS = 0
    els.append(card(406, 102, 318, 82, rx=8, fill=SLATE_SOFT, stroke=SLATE))
    els.append(txt(418, 122, "关断态（栅极电压 V_GS < 阈值 V_th → 逻辑 0）", 11.5, SLATE, weight="700"))
    # 简化截面：源 S、漏 D、栅 G + 氧化层
    els.append(f'<rect x="430" y="146" width="144" height="28" rx="4" fill="#f8fafc" stroke="{SLATE}"/>')
    els.append(f'<rect x="436" y="146" width="34" height="16" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(453, 158, "源 S", 10.5, BLUE, "middle", weight="700"))
    els.append(f'<rect x="534" y="146" width="34" height="16" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(551, 158, "漏 D", 10.5, BLUE, "middle", weight="700"))
    els.append(f'<rect x="476" y="139" width="52" height="6" fill="#fde68a" stroke="{ORANGE}"/>')
    els.append(f'<line x1="476" y1="134" x2="528" y2="134" stroke="{PURPLE}" stroke-width="3"/>')
    els.append(txt(590, 146, "栅极没加正电压", 11.5, INK, weight="700"))
    els.append(txt(590, 164, "S 与 D 之间断路不通", 11.5, SLATE, weight="600"))

    # 导通态 V_GS > V_th
    els.append(card(406, 194, 318, 82, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    els.append(txt(418, 214, "导通态（栅极电压 V_GS > 阈值 V_th → 逻辑 1）", 11.5, PURPLE, weight="700"))
    els.append(f'<rect x="430" y="238" width="144" height="28" rx="4" fill="#f8fafc" stroke="{SLATE}"/>')
    els.append(f'<rect x="470" y="246" width="64" height="8" fill="{GREEN}"/>')
    els.append(f'<rect x="436" y="238" width="34" height="16" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(453, 250, "源 S", 10.5, BLUE, "middle", weight="700"))
    els.append(f'<rect x="534" y="238" width="34" height="16" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(551, 250, "漏 D", 10.5, BLUE, "middle", weight="700"))
    els.append(f'<rect x="476" y="231" width="52" height="6" fill="#fde68a" stroke="{ORANGE}"/>')
    els.append(f'<line x1="476" y1="226" x2="528" y2="226" stroke="{PURPLE}" stroke-width="3"/>')
    els.append(txt(588, 239, "氧化层下吸出导电沟道", 11.5, INK, weight="700"))
    els.append(txt(588, 257, "毫微功耗即可开关大电流", 11.5, GREEN, weight="700"))

    els.append(txt(406, 300, "代表分工：快充头里每秒斩波几十万次的功率开关；", 11.5, BODY))
    els.append(txt(406, 318, "手机 CPU 里上百亿颗每秒翻转几十亿次的 0/1 逻辑门。", 11.5, BODY))

    return figure(
        344,
        "半导体核心器件原理对比：PN结二极管单向导通与MOSFET场效应晶体管电压控制沟道",
        "左栏对比PN结二极管正向偏置压窄耗尽层导通与反向偏置拉宽耗尽层截止；右栏对比MOSFET在栅极电压低于阈值时源漏断开、高于阈值时在二氧化硅绝缘层下感应出导电沟道，实现小电压控制大电流和数字逻辑开关。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 6：大合奏——拆开一颗手机充电器，看五大元器件怎样把 220V 交流变成纯净 5V 直流
# ---------------------------------------------------------------------------
def build_charger_symphony() -> str:
    els = header(
        "图 6 · 终极合奏：拆开手机充电器，看五大元器件怎样接力驯服 220 V 交流电",
        "跟着底部的电压波形一路向右看：正弦波 → 馒头脉动波 → 高频方波 → 低压小纹波 → 5.00 V 直线",
    )

    stages = [
        (16, 136, "① 整流桥", "4 颗二极管", "把正负交替的\n220 V 掰成单向", BLUE, BLUE_SOFT, "sine_to_rect"),
        (164, 136, "② 高压滤波 + 斩波", "大电容 + MOSFET", "先滤成约 311 V DC\n再高频切碎成方波", PURPLE, PURPLE_SOFT, "chop"),
        (312, 136, "③ 高频变压器", "磁芯耦合电感", "高频磁通隔空传能\n安全隔离并降压", ORANGE, ORANGE_SOFT, "stepdown"),
        (460, 136, "④ 次级整流滤波", "肖特基管 + 电容", "再次单向整流\n电容填平电压坑洼", GREEN, GREEN_SOFT, "smooth"),
        (608, 136, "⑤ 反馈稳压保护", "采样电阻 + 光耦", "实时盯死输出电压\n锁定纯净 5.0 V DC", TEAL, TEAL_SOFT, "flat"),
    ]

    for x0, w, name, comp, desc, col, soft, wave in stages:
        els.append(card(x0, 62, w, 212, fill=CARD_BG, stroke=col, sw=1.3))
        els.append(f'<rect x="{x0}" y="62" width="{w}" height="28" rx="10" fill="{soft}"/>')
        els.append(f'<rect x="{x0}" y="80" width="{w}" height="10" fill="{soft}"/>')
        els.append(txt(x0 + w / 2, 81, name, 12, col, "middle", weight="700"))
        els.append(txt(x0 + w / 2, 108, comp, 11.5, INK, "middle", weight="700"))
        for i, line in enumerate(desc.split("\n")):
            els.append(txt(x0 + w / 2, 130 + i * 18, line, 11, BODY, "middle"))

        # 底部迷你波形窗 (y=172..258)
        wx, wy, ww, wh = x0 + 12, 174, w - 24, 68
        els.append(card(wx, wy, ww, wh, rx=6, fill=SLATE_SOFT, stroke=HAIRLINE))
        mid_y = wy + wh * 0.58
        els.append(f'<line x1="{wx + 6}" y1="{mid_y:.1f}" x2="{wx + ww - 6}" y2="{mid_y:.1f}" stroke="{HAIRLINE}" stroke-width="1"/>')

        if wave == "sine_to_rect":
            # 3 个半波翻正（馒头波）
            pts = []
            for k in range(49):
                ang = 3.0 * math.pi * k / 48.0
                px = wx + 8 + (ww - 16) * (k / 48.0)
                py = (wy + wh - 12) - 36.0 * abs(math.sin(ang))
                pts.append(f"{px:.1f},{py:.1f}")
            els.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2"/>')
            els.append(txt(x0 + w / 2, 260, "100 Hz 单向馒头波", 10.5, col, "middle", weight="600"))
        elif wave == "chop":
            # 高频方波脉冲
            path = []
            x_cur = wx + 10
            step = (ww - 20) / 5.0
            for _ in range(5):
                x_hi = x_cur + step * 0.52
                x_nx = x_cur + step
                path.append(f"M{x_cur:.1f},{wy + wh - 12} L{x_cur:.1f},{wy + 14} L{x_hi:.1f},{wy + 14} L{x_hi:.1f},{wy + wh - 12} L{x_nx:.1f},{wy + wh - 12}")
                x_cur = x_nx
            els.append(f'<path d="{" ".join(path)}" fill="none" stroke="{col}" stroke-width="1.7"/>')
            els.append(txt(x0 + w / 2, 260, "百 kHz 级高频脉冲", 10.5, col, "middle", weight="600"))
        elif wave == "stepdown":
            # 幅度压低的次级高频脉冲
            path = []
            x_cur = wx + 10
            step = (ww - 20) / 5.0
            for _ in range(5):
                x_hi = x_cur + step * 0.52
                x_nx = x_cur + step
                path.append(f"M{x_cur:.1f},{wy + wh - 12} L{x_cur:.1f},{wy + 34} L{x_hi:.1f},{wy + 34} L{x_hi:.1f},{wy + wh - 12} L{x_nx:.1f},{wy + wh - 12}")
                x_cur = x_nx
            els.append(f'<path d="{" ".join(path)}" fill="none" stroke="{col}" stroke-width="1.8"/>')
            els.append(txt(x0 + w / 2, 260, "低压隔离脉冲", 10.5, col, "middle", weight="600"))
        elif wave == "smooth":
            # 微小锯齿纹波
            pts = []
            for k in range(41):
                px = wx + 8 + (ww - 16) * (k / 40.0)
                ripple = 4.0 * ((k % 8) / 8.0)
                py = wy + 24 + ripple
                pts.append(f"{px:.1f},{py:.1f}")
            els.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.1"/>')
            els.append(txt(x0 + w / 2, 260, "纹波被电容抹平", 10.5, col, "middle", weight="600"))
        else:
            els.append(f'<line x1="{wx + 8}" y1="{wy + 25}" x2="{wx + ww - 8}" y2="{wy + 25}" stroke="{col}" stroke-width="2.8"/>')
            els.append(txt(x0 + w / 2, 260, "稳定 5.0 V 直流", 10.5, col, "middle", weight="700"))

    for ax in (153, 301, 449, 597):
        els.append(f'<path d="M{ax} 168 L{ax + 9} 168" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')

    # 反馈回路箭头（从 ⑤ 回到 ② 的 MOSFET 占空比控制）
    extra_defs = f"""
  <marker id="arr-teal" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{TEAL}"/>
  </marker>"""
    els.append(
        f'<path d="M676 276 L676 306 Q676 316 664 316 L244 316 Q232 316 232 306 L232 278" '
        f'fill="none" stroke="{TEAL}" stroke-width="1.7" stroke-dasharray="5 3" marker-end="url(#arr-teal)"/>'
    )
    els.append(f'<rect x="330" y="303" width="256" height="24" rx="12" fill="{BG}"/>')
    els.append(txt(458, 319, "← 光耦隔离反馈：动态调节 MOSFET 开关占空比", 11.5, TEAL, "middle", weight="700"))

    els.append(
        txt(
            20,
            350,
            "为什么氮化镓（GaN）充电头能缩成饼干大小？因为它把 ② 里的开关频率推高到数百 kHz 至 MHz，③ 里的变压器磁芯就能大幅缩小。",
            11.5,
            MUTED,
        )
    )

    return figure(
        368,
        "手机开关电源充电器五级电路合奏：从220伏交流电到稳定5伏直流电的波形演变与元器件分工",
        "五张卡片依次展示：①二极管整流桥将220V正弦交流变为100Hz单向脉动波；②高压电容与MOSFET滤波并高频斩波成百千赫兹脉冲；③高频变压器磁耦合隔离降压；④次级肖特基管与电容整流抹平纹波；⑤采样电阻与光耦把输出误差反馈给MOSFET调节占空比，输出纯净5.0V直流。",
        els,
        extra_defs=extra_defs,
    )


@register(TOPIC, "电压、电流与电阻：远距输电与电子元器件协同原理图解（6图）", "science_tech")
def build_all() -> None:
    verify_circuit_math()
    write_svg(TOPIC, "vir-triad-led-loop.svg", build_vir_triad())
    write_svg(TOPIC, "high-voltage-transmission.svg", build_high_voltage_tx())
    write_svg(TOPIC, "passive-rcl-trio.svg", build_passive_rcl())
    write_svg(TOPIC, "rc-charging-anim.svg", build_rc_charging_anim())
    write_svg(TOPIC, "semiconductor-diode-mosfet.svg", build_semiconductor_duo())
    write_svg(TOPIC, "charger-five-stage-symphony.svg", build_charger_symphony())
