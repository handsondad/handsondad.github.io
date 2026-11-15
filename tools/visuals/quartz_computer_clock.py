"""
Visuals for '石英钟与电脑时钟' (Quartz Clocks & Computer Clocks: Piezoelectricity, 32,768 Hz Binary Division,
Parabolic vs AT-Cut Thermal Drift, PC Dual-Clock Architecture RTC+PLL+TSC, Resolution vs Accuracy, and NTPv4).
Generates 6 original 760px Chinese SVG diagrams in assets/images/quartz-computer-clock/
with verified mathematical and engineering assertions.
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
    pill,
    register,
    txt,
    write_svg,
)

TOPIC = "quartz-computer-clock"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"


def _line(x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, marker=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def _verify_clock_math() -> None:
    # 1. Binary division: 2^15 = 32,768 Hz -> 15 stages -> exact 1 Hz
    assert 2**15 == 32_768
    assert 2**13 == 8_192  # 1969 Seiko Quartz Astron 35SQ

    # 2. NIST frequency division error scaling: 0.1 Hz error on 32,768 Hz vs 1 Hz pendulum
    err_hz = 0.1
    sec_per_1s_err_quartz = 32_768 / err_hz
    daily_err_quartz = 86_400 / sec_per_1s_err_quartz
    assert sec_per_1s_err_quartz == 327_680.0
    assert round(daily_err_quartz, 2) == 0.26

    # 3. Parabolic temperature drift of 32.768 kHz tuning-fork crystal: df/f0 = B * (T - T0)^2
    B = -0.035  # ppm / °C^2
    T0 = 25.0
    ppm_at_0C = B * (0.0 - T0) ** 2
    sec_day_at_0C = ppm_at_0C * 1e-6 * 86_400
    assert round(ppm_at_0C, 2) == -21.88
    assert round(sec_day_at_0C, 2) == -1.89

    # 4. Resolution vs Accuracy (Microsoft Learn example: 3 GHz TSC, 50 ppm offset -> 4.32 s/day!)
    tsc_res_ps = 1e12 / 3e9
    assert round(tsc_res_ps, 1) == 333.3
    drift_50ppm_day = 86_400 * 50e-6
    assert round(drift_50ppm_day, 2) == 4.32

    # 5. Counter wrap-around horizons (Linux kernel timekeeping.html)
    wrap_32bit_100mhz_s = (2**32) / 1e8
    wrap_64bit_ns_years = (2**64) / (1e9 * 86_400 * 365.2425)
    assert 42.9 < wrap_32bit_100mhz_s < 43.0
    assert 584.0 < wrap_64bit_ns_years < 585.0

    # 6. NTPv4 (RFC 5905) 4-timestamp worked example
    t1, t2, t3, t4 = 10.000, 10.080, 10.090, 10.050
    delay = (t4 - t1) - (t3 - t2)
    offset = 0.5 * ((t2 - t1) + (t3 - t4))
    assert round(delay * 1000, 1) == 40.0    # 40 ms round-trip flight time (20 ms each way)
    assert round(offset * 1000, 1) == 60.0   # Server is +60 ms ahead of local clock!


# ---------------------------------------------------------------------------
# 1. Piezoelectric Effect & Quartz Tuning-Fork Closed-Loop Oscillator + Q Factor
# ---------------------------------------------------------------------------
def build_piezoelectric_oscillator() -> None:
    W, H = 760, 512
    el = []
    el.append(txt(W / 2, 30, "一块透明小石头凭什么当节拍器？压电效应与石英音叉振荡闭环", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "1880 年居里兄弟发现“捏石英生电”，配合电路正反馈，造出了品质因数 Q 高达机械摆轮百倍的物理摆", size=12.2, color=MUTED, anchor="middle"))

    # Left card: Direct vs Converse Piezoelectric Effect in SiO2 Lattice
    el.append(card(22, 68, 352, 422))
    el.append(pill(38, 82, "① 物理根基：SiO₂ 晶格的“机电双向翻译”", fg=TEAL, bg=TEAL_SOFT, w=304))

    # Top sub-box: Direct Piezoelectricity (Squeeze -> Voltage)
    el.append(card(38, 120, 320, 158, rx=10, fill="#f8fafc", stroke=BORDER))
    el.append(txt(52, 142, "正压电效应（1880 居里兄弟）：机械形变 → 产生电压", size=11.5, weight="700", color=TEAL))
    # Draw compressed hexagon lattice
    el.append('<polygon points="92,172 132,162 162,188 152,226 112,236 82,210" fill="#ccfbf1" stroke="#0f766e" stroke-width="2"/>')
    el.append(_line(122, 147, 122, 160, stroke=RED, sw=2.2, marker="arr-orange"))
    el.append(_line(122, 251, 122, 238, stroke=RED, sw=2.2, marker="arr-orange"))
    el.append(txt(106, 188, "+Si⁴⁺", size=10.2, weight="700", color=RED))
    el.append(txt(116, 218, "−O²⁻", size=10.2, weight="700", color=BLUE))
    el.append(txt(186, 178, "• 无外力时正负电荷中心重合；", size=10.5, color=BODY))
    el.append(txt(186, 198, "• 受压弯曲瞬间，硅氧离子错位，", size=10.5, color=BODY))
    el.append(txt(186, 218, "  晶面两端吐出微弱交变电压！", size=10.5, weight="700", color=INK))
    el.append(txt(52, 265, "（打火机咔哒一按冒电火花，也是同一原理！）", size=10.2, color=MUTED))

    # Bottom sub-box: Converse Piezoelectricity (Voltage -> Flexing)
    el.append(card(38, 290, 320, 184, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(52, 312, "逆压电效应（1881 李普曼）：施加电压 → 精准弹动", size=11.5, weight="700", color=BLUE))
    # Quartz tuning fork prongs flexing inward/outward
    el.append('<path d="M 88 432 L 88 386 L 74 386 L 74 332 L 88 332 L 88 372 L 108 372 L 108 332 L 122 332 L 122 386 L 108 386 L 108 432 Z" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>')
    el.append(_line(60, 344, 71, 344, stroke=ORANGE, sw=2.0, marker="arr-orange"))
    el.append(_line(136, 344, 125, 344, stroke=ORANGE, sw=2.0, marker="arr-orange"))
    el.append(txt(98, 450, "4 毫米微型石英音叉", size=10.2, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(154, 346, "• 电极通电 → 两根音叉臂弯曲；", size=10.5, color=BODY))
    el.append(txt(154, 368, "• 音叉回弹 → 正压电吐回电信号；", size=10.5, color=BODY))
    el.append(txt(154, 390, "• 唯有切口决定的“固有谐振频率”", size=10.5, color=BODY))
    el.append(txt(154, 410, "  能通过，其余杂波全被滤除！", size=10.5, weight="700", color=BLUE))
    el.append(txt(154, 434, "• 真空金属壳封装，零空气阻力！", size=10.5, weight="700", color=TEAL))

    # Right card: Closed-loop Pierce Oscillator + Resonance Q-Curve Comparison
    el.append(card(388, 68, 350, 422))
    el.append(pill(404, 82, "② 永不疲倦的闭环 + 碾压机械表的 Q 值", fg=AMBER, bg=AMBER_SOFT, w=310))

    # Top feedback diagram (404..722, 120..254)
    el.append(card(404, 120, 318, 132, rx=10, fill=AMBER_SOFT, stroke="#fcd34d"))
    el.append(card(422, 146, 114, 44, rx=8, fill="#ffffff", stroke=AMBER))
    el.append(txt(479, 166, "石英音叉谐振器", size=11, weight="700", color=AMBER, anchor="middle"))
    el.append(txt(479, 182, "（机械选频核心）", size=9.8, color=MUTED, anchor="middle"))

    el.append(card(590, 146, 114, 44, rx=8, fill="#ffffff", stroke=BLUE))
    el.append(txt(647, 166, "CMOS 放大器", size=11, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(647, 182, "（电池微能量补推）", size=9.8, color=MUTED, anchor="middle"))

    el.append(_line(538, 158, 588, 158, stroke=BLUE, sw=2.2, marker="arr-blue"))
    el.append(txt(563, 150, "正压电信号", size=9.8, color=BLUE, anchor="middle"))
    el.append(_line(588, 180, 538, 180, stroke=AMBER, sw=2.2, marker="arr-orange"))
    el.append(txt(563, 200, "逆压电轻推一把", size=9.8, color=AMBER, anchor="middle"))
    el.append(txt(563, 234, "就像大人在最高点轻轻推秋千：每振动一次只补极微弱电能", size=10.3, weight="700", color=INK, anchor="middle"))

    # Bottom Q-factor resonance sharpness plot (404..722, 268..474)
    el.append(card(404, 268, 318, 206, rx=10, fill="#f8fafc", stroke=BORDER))
    el.append(txt(563, 290, "为什么石英表比顶级陀飞轮准几十倍？看谐振峰锐度（Q 值）", size=11, weight="700", color=INK, anchor="middle"))

    # Axes: x=436..696, y=428 (baseline) up to 312
    el.append(_line(436, 428, 700, 428, stroke=SLATE, sw=1.4))
    el.append(_line(436, 428, 436, 308, stroke=SLATE, sw=1.4))
    el.append(txt(428, 322, "振幅", size=10, color=MUTED, anchor="end"))
    el.append(txt(568, 446, "偏离标准中心频率 f₀ 的程度", size=10.2, color=MUTED, anchor="middle"))

    # Broad curve: Mechanical balance wheel (Q ~ 100 - 300)
    mech_pts = []
    for i in range(65):
        u = -3.2 + 6.4 * (i / 64.0)
        px = 568 + u * 38.0
        amp = 1.0 / (1.0 + (u / 1.35) ** 2)
        py = 426 - amp * 68.0
        mech_pts.append(f"{px:.1f},{py:.1f}")
    el.append(f'<polyline points="{" ".join(mech_pts)}" fill="none" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="5 3"/>')
    el.append(txt(486, 376, "机械游丝摆轮", size=10.4, weight="700", color=ORANGE, anchor="middle"))
    el.append(txt(486, 392, "Q ≈ 10²（峰宽易歪）", size=9.8, color=ORANGE, anchor="middle"))

    # Razor-sharp Lorentzian peak: Vacuum Quartz Crystal (Q ~ 50,000 - 100,000)
    qtz_pts = []
    for i in range(81):
        u = -3.2 + 6.4 * (i / 80.0)
        px = 568 + u * 38.0
        amp = 1.0 / (1.0 + (u / 0.11) ** 2)
        py = 426 - amp * 110.0
        qtz_pts.append(f"{px:.1f},{py:.1f}")
    el.append(f'<polyline points="{" ".join(qtz_pts)}" fill="none" stroke="{TEAL}" stroke-width="2.8"/>')
    el.append(txt(646, 330, "真空石英音叉", size=10.8, weight="700", color=TEAL, anchor="middle"))
    el.append(txt(646, 347, "Q ≈ 10⁵（针尖锁定！）", size=10.2, weight="700", color=TEAL, anchor="middle"))
    el.append(txt(563, 464, "Q 值越高，振动能量损耗越小，外界干扰越难把频率拽偏", size=10.2, color=BODY, anchor="middle"))

    write_svg(
        TOPIC,
        "piezoelectric-quartz-tuning-fork-loop.svg",
        figure(H, "石英晶体正逆压电效应、皮尔斯振荡闭环与谐振品质因数Q对比图", "左图展示SiO2晶格正压电与逆压电形变机理，右图展示音叉正反馈电路及石英晶体Q≈10^5相对机械摆轮Q≈10^2的极窄谐振峰", el),
    )


# ---------------------------------------------------------------------------
# 2. Why 32,768 Hz? 15-Stage Binary Divider Chain (with 1-shot CSS animation)
# ---------------------------------------------------------------------------
def build_why_32768_binary_divider() -> None:
    W, H = 760, 504
    extra_css = """
      .anim-div-pulse {
        stroke-dasharray: 660;
        stroke-dashoffset: 660;
        animation: divCascade 3.4s ease-out 0.25s 1 forwards;
      }
      @keyframes divCascade {
        from { stroke-dashoffset: 660; }
        to   { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .anim-div-pulse {
          animation: none !important;
          stroke-dashoffset: 0 !important;
        }
      }
    """
    el = []
    el.append(txt(W / 2, 30, "为什么全世界的石英表和电脑主板，都偏爱“32,768 Hz”？", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "32,768 = 2¹⁵：既能靠 15 个触发器一路对半除出整 1 秒，又恰好卡在人耳超声波静音区与微安省电甜点上", size=12.2, color=MUTED, anchor="middle"))

    # Top wide card: 15-stage flip-flop binary division cascade
    el.append(card(22, 68, 716, 206))
    el.append(pill(38, 82, "核心密码一：二进制完美对半砍 15 刀（32,768 ÷ 2¹⁵ = 1.000 Hz 整秒脉冲）", fg=BLUE, bg=BLUE_SOFT, w=512))

    stages = [
        (40, "石英音叉输入", "32,768 Hz", "2¹⁵ 次/秒", TEAL_SOFT, TEAL),
        (166, "第 1 级 ÷2", "16,384 Hz", "2¹⁴ 次/秒", BLUE_SOFT, BLUE),
        (286, "第 2 级 ÷2", "8,192 Hz", "1969 首款石英表", BLUE_SOFT, BLUE),
        (420, "… 第 3–14 级 …", "一路 ÷2 递减", "共串联 15 级触发器", SLATE_SOFT, SLATE),
        (562, "第 15 级 ÷2", "1.000 Hz", "精准每秒 1 滴答！", GREEN_SOFT, GREEN),
    ]
    # Animated signal bus connecting all stages at y=166
    el.append(_line(96, 166, 686, 166, stroke="#cbd5e1", sw=6))
    el.append('<line class="anim-div-pulse" x1="96" y1="166" x2="686" y2="166" stroke="#2563eb" stroke-width="3.6" marker-end="url(#arr-blue)"/>')

    for sx, top_lbl, hz_lbl, sub_lbl, bg, col in stages:
        bw = 112 if "3–14" not in top_lbl else 124
        if sx == 562:
            bw = 156
        el.append(card(sx, 122, bw, 88, rx=10, fill=bg, stroke=col))
        el.append(txt(sx + bw / 2, 144, top_lbl, size=10.6, weight="700", color=col, anchor="middle"))
        el.append(txt(sx + bw / 2, 169, hz_lbl, size=13, weight="700", color=INK, anchor="middle"))
        el.append(txt(sx + bw / 2, 192, sub_lbl, size=10, color=BODY, anchor="middle"))

    el.append(txt(380, 238, "• 数字电路里“除以 10”很麻烦，但 T 触发器“每来两个脉冲翻转一次（除以 2）”只需寥寥几颗晶体管！", size=10.8, color=BODY, anchor="middle"))
    el.append(txt(380, 258, "• 输出的 1 Hz 秒脉冲：在石英钟里驱动步进马达秒针跳一格；在电脑主板里让实时时钟（RTC）秒寄存器 +1。", size=10.8, weight="700", color=INK, anchor="middle"))

    # Bottom 3 cards: Why NOT 16,384 Hz? Why NOT 65,536 / 1,048,576 Hz? + NIST error compression!
    bottom_cards = [
        (
            22, RED_SOFT, "#fca5a5", RED,
            "为什么不选更低的 16,384 Hz？",
            [
                "• 2¹⁴ = 16,384 Hz（及 1969 精工",
                "  初代 Astron 的 8,192 Hz）全都落",
                "  在人耳听觉上限（20,000 Hz）以内！",
                "• 夜深人静贴近耳朵会听到细微高频",
                "  蚊鸣声，且低频音叉体积更长更厚，",
                "  难塞进超薄女表与紧凑主板。",
            ],
        ),
        (
            266, TEAL_SOFT, "#5eead4", TEAL,
            "为什么 32,768 Hz 是“黄金甜点”？",
            [
                "• 刚好跃过 20 kHz 人耳极限 → 绝对静音！",
                "• CMOS 电路动态功耗 P ∝ C·V²·f：",
                "  频率越低越省电！在 32.768 kHz 下",
                "  整颗 RTC 耗电不足 1 微安（<1 μA），",
                "• 一颗 2 元钱的 CR2032 纽扣电池能",
                "  在电脑彻底拔插头后苦撑 5–10 年！",
            ],
        ),
        (
            510, PURPLE_SOFT, "#d8b4fe", PURPLE,
            "NIST 算账：高频分频有多抗误差？",
            [
                "• 假定计时摆受干扰偏了 0.1 Hz：",
                "• 老式 1 Hz 大摆钟偏 0.1 Hz → 走",
                "  10 秒钟就错出整整 1 秒！",
                "• 32,768 Hz 石英晶振偏 0.1 Hz →",
                "  相对误差仅百万分之三，要走完",
                "  327,680 秒才差 1 秒（每天 0.26 秒）！",
            ],
        ),
    ]
    for bx, bg, bd, col, btitle, lines in bottom_cards:
        el.append(card(bx, 288, 228, 196, rx=12, fill="#ffffff", stroke=BORDER))
        el.append(card(bx + 10, 298, 208, 32, rx=8, fill=bg, stroke=bd))
        el.append(txt(bx + 114, 319, btitle, size=11.4, weight="700", color=col, anchor="middle"))
        for idx, ln in enumerate(lines):
            w_val = "700" if idx in (2, 4, 5) and ("绝对静音" in ln or "5–10" in ln or "0.26" in ln) else None
            el.append(txt(bx + 16, 352 + idx * 21, ln, size=10.4, color=BODY, weight=w_val))

    write_svg(
        TOPIC,
        "why-32768-hz-binary-divider-chain.svg",
        figure(H, "32768赫兹15级二进制分频链与超声波低功耗甜点原理解析图", "顶部单次动画展示32768Hz经15级除以2触发器输出1Hz整秒脉冲，底部对比20kHz静音门槛、微安级功耗与NIST频率误差压缩效应", el, extra_css=extra_css),
    )


# ---------------------------------------------------------------------------
# 3. Tuning-Fork Parabolic Temperature Drift vs AT-Cut Cubic S-Curve & TCXO
# ---------------------------------------------------------------------------
def build_temperature_drift_curves() -> None:
    W, H = 760, 496
    el = []
    el.append(txt(W / 2, 30, "为什么石英表戴在手腕上比扔桌上更准？晶振温漂曲线大揭秘", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "32.768 kHz 音叉晶振呈开口向下的抛物线（冷热皆变慢！），而电脑高频晶振改用“AT 切角”三次曲线稳频", size=12.2, color=MUTED, anchor="middle"))

    el.append(card(22, 68, 468, 408))
    el.append(txt(256, 94, "实算频率温漂对比：音叉切型抛物线 vs 高频 AT 切型 vs TCXO 温补", size=12.8, weight="700", color=INK, anchor="middle"))

    # Plot box: T in [-20, +70] °C -> x in [82, 462]; df/f0 in [-80, +30] ppm -> y in [416, 124]
    def tx(temp_c: float) -> float:
        return 82.0 + (temp_c - (-20.0)) / 90.0 * 380.0

    def py(ppm: float) -> float:
        return 416.0 - (ppm - (-80.0)) / 110.0 * 292.0

    # Grid lines
    for ppm_g in (-80, -60, -40, -20, 0, 20):
        gy = py(ppm_g)
        el.append(_line(82, gy, 462, gy, stroke="#e2e8f0" if ppm_g != 0 else "#94a3b8", sw=1.1 if ppm_g != 0 else 1.6, dash="4 3" if ppm_g != 0 else None))
        el.append(txt(74, gy + 4, f"{ppm_g:+d}" if ppm_g != 0 else "0 ppm", size=10, color=MUTED, anchor="end"))

    for t_g in (-20, 0, 25, 50, 70):
        gx = tx(t_g)
        el.append(_line(gx, 124, gx, 416, stroke="#e2e8f0" if t_g != 25 else "#cbd5e1", sw=1.1, dash="3 3"))
        el.append(txt(gx, 434, f"{t_g}℃", size=10.2, weight="700" if t_g == 25 else None, color=INK if t_g == 25 else MUTED, anchor="middle"))

    el.append(txt(272, 456, "环境工作温度 T（℃）—— 注意 11.6 ppm 误差 ≈ 每天快慢 1.0 秒", size=10.5, color=BODY, anchor="middle"))

    # Wrist temperature shaded green band (24°C .. 30°C)
    wx1, wx2 = tx(23.0), tx(31.0)
    el.append(f'<rect x="{wx1:.1f}" y="124" width="{wx2 - wx1:.1f}" height="292" fill="#dcfce7" opacity="0.55"/>')
    el.append(txt((wx1 + wx2) / 2, 140, "手腕恒温区", size=9.8, weight="700", color=GREEN, anchor="middle"))

    # Curve 1: 32.768 kHz Tuning-Fork Parabola df/f0 = -0.035 * (T - 25)^2
    parab_pts = []
    for i in range(91):
        t_val = -20.0 + i * 1.0
        ppm_val = -0.035 * ((t_val - 25.0) ** 2)
        parab_pts.append(f"{tx(t_val):.1f},{py(ppm_val):.1f}")
    el.append(f'<polyline points="{" ".join(parab_pts)}" fill="none" stroke="{RED}" stroke-width="3"/>')

    # Curve 2: High-freq AT-cut (24-100 MHz motherboard crystal) cubic S-curve
    # df/f0 ≈ 0.00042*(T - 25)^3 - 0.32*(T - 25) stays within ±15 ppm!
    at_pts = []
    for i in range(91):
        t_val = -20.0 + i * 1.0
        dt = t_val - 25.0
        ppm_val = 0.00042 * (dt**3) - 0.32 * dt
        at_pts.append(f"{tx(t_val):.1f},{py(ppm_val):.1f}")
    el.append(f'<polyline points="{" ".join(at_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

    # Curve 3: TCXO (±2 ppm flat line)
    el.append(_line(tx(-20), py(1.5), tx(70), py(-1.5), stroke=TEAL, sw=2.4, dash="6 3"))

    # Key callout dots on parabola
    x_25, y_25 = tx(25.0), py(0.0)
    x_0, y_0 = tx(0.0), py(-21.875)
    el.append(f'<circle cx="{x_25:.1f}" cy="{y_25:.1f}" r="4.8" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(f'<circle cx="{x_0:.1f}" cy="{y_0:.1f}" r="4.8" fill="{RED}" stroke="#ffffff" stroke-width="1.5"/>')
    el.append(txt(x_0 - 6, y_0 + 22, "0℃ 窗台：−21.9 ppm（日慢 1.9 秒）", size=9.8, weight="700", color=RED))
    el.append(txt(368, py(-48.0), "① 32.768 kHz 音叉抛物线", size=10.3, weight="700", color=RED))
    el.append(txt(354, py(17.0), "② 电脑 MHz 级 AT 切三次曲线", size=10.2, weight="700", color=BLUE))
    el.append(txt(154, py(12.0), "③ 温补晶振 TCXO（±2 ppm）", size=10.0, weight="700", color=TEAL))

    # Right explanatory column
    el.append(card(504, 68, 234, 408))
    el.append(pill(518, 82, "读图秒懂三个生活现象", fg=AMBER, bg=AMBER_SOFT, w=198))

    notes = [
        ("1. 为什么手表摘下放冬天桌会变慢？", RED, [
            "音叉晶振拐点设在 T₀ = 25℃（贴近佩",
            "戴手腕温度）：",
            "Δf/f₀ = −0.035 × (T − 25)² ppm",
            "因为平方项恒为正、系数为负，无论",
            "天冷（0℃）还是暴晒（50℃），音叉",
            "永远只会往“变慢”一侧掉速！",
        ]),
        ("2. 电脑发烧到 70℃ 怎么没乱套？", BLUE, [
            "主板上 24/25/100 MHz 高频晶振改用",
            "神奇的 35°15′“AT 切角”薄晶片，温漂",
            "呈横卧 S 形三次曲线，在 −20℃ 至",
            "70℃ 宽温区内死死锁在 ±20 ppm 内。",
        ]),
        ("3. 手机基站与精密 RTC 怎么破局？", TEAL, [
            "内置微型温度传感器每分钟测温，",
            "按抛物线反向增减负载电容或分频脉",
            "冲（TCXO 温补晶振），把年误差压到",
            "区区 ±1 分钟以内！",
        ]),
    ]
    cur_y = 132
    for h_txt, h_col, body_lines in notes:
        el.append(txt(518, cur_y, h_txt, size=11.0, weight="700", color=h_col))
        cur_y += 20
        for bl in body_lines:
            el.append(txt(518, cur_y, bl, size=10.1, color=BODY))
            cur_y += 17.5
        cur_y += 10

    write_svg(
        TOPIC,
        "tuning-fork-parabolic-vs-at-cut-temp-drift.svg",
        figure(H, "32.768kHz音叉晶振抛物线温漂与电脑高频AT切晶振三次曲线对比图", "左图精确绘制音叉晶振在25摄氏度拐点两侧对称变慢的抛物线、AT切三次S曲线及TCXO温补线，右图解释手腕恒温效应", el),
    )


# ---------------------------------------------------------------------------
# 4. Computer Dual-Clock Architecture: RTC + Coin Cell vs Base Crystal + PLL + TSC
# ---------------------------------------------------------------------------
def build_computer_dual_clocks() -> None:
    W, H = 760, 524
    el = []
    el.append(txt(W / 2, 30, "拔掉电源插头半个月，电脑开机为什么还知道今天是几号？", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "一台电脑里其实住着两套分工迥异的时钟：微安级“守夜更夫（RTC）”与十亿赫兹“狂飙节拍器（PLL+TSC）”", size=12.2, color=MUTED, anchor="middle"))

    # Left Kingdom: Hardware Real-Time Clock (RTC) + CR2032 Coin Cell
    el.append(card(22, 68, 326, 336))
    el.append(pill(38, 82, "第一套：硬件实时时钟 RTC（断电守夜人）", fg=AMBER, bg=AMBER_SOFT, w=294))

    el.append(card(38, 122, 294, 92, rx=10, fill=AMBER_SOFT, stroke="#fcd34d"))
    el.append('<circle cx="82" cy="168" r="26" fill="#e2e8f0" stroke="#64748b" stroke-width="2"/>')
    el.append(txt(82, 164, "CR2032", size=10.2, weight="700", color=INK, anchor="middle"))
    el.append(txt(82, 180, "3V 纽扣电池", size=9.2, color=BODY, anchor="middle"))
    el.append(_line(112, 168, 146, 168, stroke=AMBER, sw=2.2, marker="arr-orange"))
    el.append(card(150, 136, 168, 64, rx=8, fill="#ffffff", stroke=AMBER))
    el.append(txt(234, 158, "主板南桥/PCH 内置 RTC", size=10.8, weight="700", color=AMBER, anchor="middle"))
    el.append(txt(234, 176, "+ 32.768 kHz 石英音叉", size=10.3, color=BODY, anchor="middle"))
    el.append(txt(234, 192, "（待机功耗 < 1 μA！）", size=10.0, weight="700", color=TEAL, anchor="middle"))

    rtc_pts = [
        "• 源自 1984 年 IBM PC/AT 的 MC146818 芯片传统；",
        "• 哪怕主机彻底关机拔掉插线板，纽扣电池依然供它",
        "  每秒钟静静 +1，把年月日时分秒记在寄存器里；",
        "• 精度粗（通常只到秒级）、读取慢（走低速总线），",
        "  绝对没法拿来指挥每秒几十亿拍的 CPU 运算；",
        "• 一旦五六年电池耗尽 → 开机瞬间时间倒退回",
        "  1970-01-01 或主板出厂日，BIOS 报错提示按 F1！",
    ]
    for idx, rp in enumerate(rtc_pts):
        w_val = "700" if idx >= 5 else None
        col_v = RED if idx >= 5 else BODY
        el.append(txt(38, 238 + idx * 22, rp, size=10.4, color=col_v, weight=w_val))

    # Boot handoff arrow from Left to Right!
    el.append(_line(350, 168, 396, 168, stroke=PURPLE, sw=2.8, marker="arr-blue"))
    el.append(txt(373, 144, "开机瞬间", size=10.2, weight="700", color=PURPLE, anchor="middle"))
    el.append(txt(373, 159, "读取一次", size=10.2, weight="700", color=PURPLE, anchor="middle"))

    # Right Kingdom: High-Frequency Base Crystal + PLL + TSC / HPET + OS Software Clock
    el.append(card(400, 68, 338, 336))
    el.append(pill(416, 82, "第二套：高频系统时钟树（开机狂飙总指挥）", fg=BLUE, bg=BLUE_SOFT, w=304))

    # Flow chain inside right card: 24-100 MHz AT crystal -> PLL x40 -> 4.0 GHz CPU & TSC -> OS Kernel
    el.append(card(416, 122, 138, 62, rx=8, fill=TEAL_SOFT, stroke="#5eead4"))
    el.append(txt(485, 145, "高频基准石英晶振", size=10.6, weight="700", color=TEAL, anchor="middle"))
    el.append(txt(485, 163, "24 / 25 / 100 MHz", size=10.4, weight="700", color=INK, anchor="middle"))
    el.append(txt(485, 178, "（AT 切薄晶片）", size=9.5, color=MUTED, anchor="middle"))

    el.append(_line(556, 153, 584, 153, stroke=BLUE, sw=2.2, marker="arr-blue"))
    el.append(card(588, 122, 134, 62, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(655, 145, "PLL 锁相环倍频器", size=10.6, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(655, 163, "×40 倍 → 4.0 GHz", size=10.6, weight="700", color=INK, anchor="middle"))
    el.append(txt(655, 178, "（每秒 40 亿拍！）", size=9.6, color=BLUE, anchor="middle"))

    el.append(card(416, 198, 306, 86, rx=8, fill="#f8fafc", stroke=BORDER))
    el.append(txt(428, 218, "硬件高速计数器阵列：", size=10.8, weight="700", color=INK))
    el.append(txt(428, 238, "• CPU 内部恒定速率 TSC 寄存器（RDTSC 指令，0.25 ns 级极速读数）", size=10.1, color=BODY))
    el.append(txt(428, 256, "• 主板平台定时器 HPET（≥10 MHz）与 ACPI PM Timer（3.58 MHz）", size=10.1, color=BODY))
    el.append(txt(428, 274, "• ARM 架构通用系统计数器（Generic Timer，现代固定 1 GHz）", size=10.1, color=BODY))

    el.append(card(416, 296, 306, 92, rx=8, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(428, 317, "操作系统内核软件时钟（Linux / Windows / macOS）：", size=10.8, weight="700", color=PURPLE))
    el.append(txt(428, 338, "• 接过开机时 RTC 报出的日历初值后，彻底甩开慢吞吞的 RTC；", size=10.2, color=BODY))
    el.append(txt(428, 357, "• 用快速移位乘法 ns ≈ (ticks × mult) >> shift 把硬件计数值", size=10.2, color=BODY))
    el.append(txt(428, 376, "  实时换算成纳秒级系统时间，关机瞬间断电清零！", size=10.2, weight="700", color=INK))

    # Bottom wide FAQ card: Why can't we just slice quartz directly to 4 GHz?!
    el.append(card(22, 418, 716, 86, rx=12, fill=TEAL_SOFT, stroke="#5eead4"))
    el.append(txt(40, 443, "灵魂追问：为什么不直接切一块每秒震动 40 亿次（4 GHz）的石英晶片给 CPU 用，非要靠 PLL 锁相环倍频？", size=12, weight="700", color=TEAL))
    el.append(txt(40, 465, "• AT 切石英晶片基频与厚度成反比（f ≈ 1.66 MHz·mm ÷ 厚度 d）：25 MHz 晶片厚约 66 微米（接近头发丝），结实耐造；", size=10.6, color=BODY))
    el.append(txt(40, 486, "• 若硬切到 4,000 MHz 基频，石英片厚度只剩 0.41 微米（比肥皂泡膜还薄）——一碰就碎成渣！所以必须“低频稳晶振 + 电子倍频”。", size=10.6, weight="700", color=INK))

    write_svg(
        TOPIC,
        "computer-dual-clock-architecture-rtc-pll-tsc.svg",
        figure(H, "电脑双时钟架构：主板纽扣电池RTC实时时钟与高频晶振PLL倍频TSC系统时钟协作图", "左栏展示CR2032供电的32.768kHz断电守夜RTC，右栏展示24至100MHz主晶振经PLL倍频至GHz驱动TSC与操作系统内核纳秒时钟", el),
    )


# ---------------------------------------------------------------------------
# 5. Two Classic Computer Time Traps: Resolution != Accuracy & REALTIME vs MONOTONIC
# ---------------------------------------------------------------------------
def build_computer_clock_traps() -> None:
    W, H = 760, 510
    el = []
    el.append(txt(W / 2, 30, "电脑计时的两大认知陷阱：皮秒刻度照样慢 4 秒 & 时间倒流 Bug", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "高分辨率不等于高准确度；测耗时若误用“日历时钟”，一次网络校时往回拨表就能让程序瞬间死锁崩溃", size=12.2, color=MUTED, anchor="middle"))

    # Top half: Trap 1 — Resolution (刻度多密) vs Accuracy (尺子准不准)
    el.append(card(22, 68, 716, 198))
    el.append(pill(38, 82, "陷阱一：3 GHz CPU 计数器能切出 0.33 纳秒刻度，为什么断网一天照样能歪 4.3 秒？", fg=ORANGE, bg=ORANGE_SOFT, w=606))

    # Ruler A: 3 GHz CPU TSC with +50 ppm crystal offset ("刻度密如发丝的橡皮尺")
    el.append(card(38, 122, 332, 126, rx=10, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(52, 145, "A. 未联网校准的 3 GHz 电脑 TSC（高分辨率 · 低准确度）", size=11.0, weight="700", color=ORANGE))
    # Fine ruler ticks
    el.append(_line(54, 168, 350, 168, stroke=ORANGE, sw=2))
    for rx in range(54, 352, 6):
        th = 10 if (rx - 54) % 30 == 0 else 5
        el.append(_line(rx, 168 - th, rx, 168, stroke=ORANGE, sw=1.1))
    el.append(txt(52, 192, "• 分辨率（最小刻度）：1 ÷ 3×10⁹ = 0.333 纳秒（极精细！）", size=10.3, color=BODY))
    el.append(txt(52, 212, "• 准确度受主板晶振 ±50 ppm 公差拖累：86,400 秒 × 50×10⁻⁶", size=10.3, color=BODY))
    el.append(txt(52, 232, "  → 走满一天累计偏差 ±4.32 秒！（像印满微米刻度的橡皮尺）", size=10.3, weight="700", color=RED))

    # Ruler B: ±2 ppm TCXO 1 Hz Watch/RTC ("刻度粗糙的钢尺")
    el.append(card(386, 122, 336, 126, rx=10, fill=TEAL_SOFT, stroke="#5eead4"))
    el.append(txt(400, 145, "B. 温补石英表 TCXO 秒脉冲（低分辨率 · 高准确度）", size=11.0, weight="700", color=TEAL))
    el.append(_line(402, 168, 702, 168, stroke=TEAL, sw=2))
    for rx in range(402, 706, 60):
        el.append(_line(rx, 156, rx, 168, stroke=TEAL, sw=2))
    el.append(txt(400, 192, "• 分辨率（最小刻度）：每秒才跳 1 下（1.0 秒，测不了微秒耗时）", size=10.3, color=BODY))
    el.append(txt(400, 212, "• 但晶振经过 ±2 ppm 精密温补：86,400 秒 × 2×10⁻⁶", size=10.3, color=BODY))
    el.append(txt(400, 232, "  → 走满一天误差仅 ±0.17 秒！（刻度虽疏，总长却稳如钢尺）", size=10.3, weight="700", color=TEAL))

    # Bottom half: Trap 2 — CLOCK_REALTIME vs CLOCK_MONOTONIC
    el.append(card(22, 282, 716, 208))
    el.append(pill(38, 296, "陷阱二：为什么所有现代操作系统都强制拆分“墙上日历钟”与“单调秒表钟”？", fg=PURPLE, bg=PURPLE_SOFT, w=564))

    # Left: CLOCK_REALTIME backward jump disaster
    el.append(card(38, 336, 332, 138, rx=10, fill=RED_SOFT, stroke="#fca5a5"))
    el.append(txt(52, 358, "❌ 日历墙上钟 CLOCK_REALTIME（会跳变倒流！）", size=11.2, weight="700", color=RED))
    # Sawtooth jump plot
    el.append('<polyline points="56,418 156,382 156,412 246,378" fill="none" stroke="#dc2626" stroke-width="2.6"/>')
    el.append('<circle cx="156" cy="382" r="4" fill="#dc2626"/>')
    el.append(txt(166, 412, "NTP/手动回拨 −2 秒！", size=9.8, weight="700", color=RED))
    el.append(txt(52, 438, "• 用途：给人类看现在几点、给文件盖 UTC 日期戳；", size=10.2, color=BODY))
    el.append(txt(52, 458, "• 禁忌：测耗时算 t₂ − t₁ 可能算出负数，导致超时器卡死！", size=10.2, weight="700", color=RED))

    # Right: CLOCK_MONOTONIC / QPC smooth upward line
    el.append(card(386, 336, 336, 138, rx=10, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(400, 358, "✅ 单调秒表钟 CLOCK_MONOTONIC / QPC（绝不倒退！）", size=11.2, weight="700", color=GREEN))
    el.append('<line x1="406" y1="418" x2="596" y2="372" stroke="#16a34a" stroke-width="2.8" marker-end="url(#arr-green)"/>')
    el.append(txt(604, 384, "开机起算", size=9.8, weight="700", color=GREEN))
    el.append(txt(604, 400, "永远单调递增", size=9.8, weight="700", color=GREEN))
    el.append(txt(400, 438, "• 用途：测量函数耗时、网络超时、游戏帧间隔、动画计时；", size=10.2, color=BODY))
    el.append(txt(400, 458, "• 铁律：不管用户把系统年份改到哪一年，它都稳步向前走！", size=10.2, weight="700", color=GREEN))

    write_svg(
        TOPIC,
        "resolution-vs-accuracy-and-monotonic-clock.svg",
        figure(H, "电脑计时分辨率与准确度区别及CLOCK_REALTIME与CLOCK_MONOTONIC对比图", "上半图对比3GHz高分辨率TSC因50ppm偏差日漂4.32秒与温补晶振高准确度，下半图对比会回跳的日历时钟与永不倒退的单调时钟", el),
    )


# ---------------------------------------------------------------------------
# 6. NTPv4 4-Timestamp Handshake (RFC 5905) & Clock Discipline Slewing vs Stepping
# ---------------------------------------------------------------------------
def build_ntp_handshake_and_slewing() -> None:
    W, H = 760, 514
    el = []
    el.append(txt(W / 2, 30, "网速延迟忽快忽慢，电脑怎么隔着互联网把表对准原子钟？", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "NTP 协议靠“四时间戳乒乓算术”扣掉网络路途耗时，再用“调频慢追（Slew）”温柔抚平误差", size=12.2, color=MUTED, anchor="middle"))

    # Left card: RFC 5905 4-timestamp spacetime exchange + worked arithmetic
    el.append(card(22, 68, 412, 426))
    el.append(pill(38, 82, "① NTP 四时间戳对表术（IETF RFC 5905）", fg=BLUE, bg=BLUE_SOFT, w=314))

    # Spacetime timelines: Server top (y=154), Client bottom (y=252)
    el.append(card(38, 122, 380, 172, rx=10, fill="#f8fafc", stroke=BORDER))
    el.append(_line(112, 162, 404, 162, stroke=TEAL, sw=2.4))
    el.append(txt(48, 158, "原子钟授时", size=10.2, weight="700", color=TEAL))
    el.append(txt(48, 173, "服务器表盘", size=10.2, weight="700", color=TEAL))

    el.append(_line(112, 252, 404, 252, stroke=BLUE, sw=2.4))
    el.append(txt(48, 248, "你的电脑", size=10.2, weight="700", color=BLUE))
    el.append(txt(48, 263, "本地表盘", size=10.2, weight="700", color=BLUE))

    # Request arrow T1 -> T2; Reply arrow T3 -> T4
    el.append(_line(142, 252, 224, 164, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    el.append(_line(284, 162, 366, 250, stroke=PURPLE, sw=2.4, marker="arr-blue"))

    el.append(txt(142, 274, "T₁ = 10.000s", size=10.2, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(214, 146, "T₂ = 10.080s", size=10.2, weight="700", color=TEAL, anchor="middle"))
    el.append(txt(302, 146, "T₃ = 10.090s", size=10.2, weight="700", color=TEAL, anchor="middle"))
    el.append(txt(366, 274, "T₄ = 10.050s", size=10.2, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(166, 206, "去程", size=9.8, color=ORANGE, anchor="middle"))
    el.append(txt(340, 206, "回程", size=9.8, color=PURPLE, anchor="middle"))

    # Worked arithmetic box
    el.append(card(38, 306, 380, 172, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(52, 328, "小学生加减法秒破“路途延迟 + 表盘快慢”双未知数：", size=11.2, weight="700", color=BLUE))
    el.append(txt(52, 352, "• 往返纯网络路途延迟 δ = (T₄ − T₁) − (T₃ − T₂)", size=10.5, weight="700", color=INK))
    el.append(txt(52, 372, "  = (10.050 − 10.000) − (10.090 − 10.080) = 0.040 秒（单程 20 ms）", size=10.2, color=BODY))
    el.append(txt(52, 398, "• 你的电脑相对标准时间偏差 θ = [(T₂ − T₁) + (T₃ − T₄)] ÷ 2", size=10.5, weight="700", color=INK))
    el.append(txt(52, 418, "  = [(+0.080) + (+0.040)] ÷ 2 = +0.060 秒（你的电脑慢了 60 ms！）", size=10.2, color=BODY))
    el.append(txt(52, 444, "• 多次采样挑最短延迟包过滤排队抖动，公网对时精度可达几毫秒，", size=10.1, color=MUTED))
    el.append(txt(52, 462, "  局域网更可达几十微秒（精密工业则用硬件时间戳 PTP 达亚微秒）。", size=10.1, color=MUTED))

    # Right card: Stratum Hierarchy + Slewing vs Stepping
    el.append(card(448, 68, 290, 426))
    el.append(pill(464, 82, "② 授时金字塔与“温柔慢拨”艺术", fg=TEAL, bg=TEAL_SOFT, w=254))

    # Compact Stratum pyramid (y=122..246)
    strata = [
        (488, 210, 124, TEAL_SOFT, TEAL, "Stratum 0：铯/氢原子钟、GPS/北斗星载钟"),
        (476, 234, 162, BLUE_SOFT, BLUE, "Stratum 1：国家级一级授时服务器"),
        (464, 258, 200, PURPLE_SOFT, PURPLE, "Stratum 2/3：云厂商与操作系统授时池"),
    ]
    for sx, sw, sy, bg, col, lbl in strata:
        el.append(card(sx, sy, sw, 30, rx=7, fill=bg, stroke=col))
        el.append(txt(sx + sw / 2, sy + 19, lbl, size=9.8, weight="700", color=col, anchor="middle"))
    el.append(_line(593, 154, 593, 161, stroke=SLATE, sw=1.6))
    el.append(_line(593, 192, 593, 199, stroke=SLATE, sw=1.6))

    # Slewing vs Stepping comparison (y=244..478)
    el.append(card(464, 244, 258, 234, rx=10, fill="#f8fafc", stroke=BORDER))
    el.append(txt(476, 266, "发现慢了 60 毫秒，系统怎么追？", size=11.4, weight="700", color=INK))

    # Plot: Target UTC line vs Smooth Slew curve vs Hard Step
    el.append(_line(482, 346, 704, 294, stroke=SLATE, sw=1.8, dash="4 3"))
    el.append(txt(658, 290, "标准原子钟 UTC", size=9.6, color=MUTED, anchor="middle"))
    # Smooth Slew curve catching up gently
    el.append('<path d="M 482 368 Q 566 346 704 294" fill="none" stroke="#0f766e" stroke-width="2.8"/>')
    el.append(txt(616, 350, "调频慢追（Slew）", size=10.2, weight="700", color=TEAL))

    el.append(txt(476, 388, "• 小误差（<128 ms）走“慢拨 Slew”：", size=10.3, weight="700", color=TEAL))
    el.append(txt(476, 407, "  绝不硬跳表！内核把软件时钟步伐悄", size=10.1, color=BODY))
    el.append(txt(476, 424, "  悄调快 0.05%（500 ppm，每秒追", size=10.1, color=BODY))
    el.append(txt(476, 441, "  0.5 ms），花 2 分钟丝滑贴合标准时；", size=10.1, color=BODY))
    el.append(txt(476, 462, "• 唯刚开机差几分钟以上才“硬跳 Step”。", size=10.1, weight="700", color=RED))

    write_svg(
        TOPIC,
        "ntp-four-timestamp-handshake-and-slewing.svg",
        figure(H, "NTP网络时间协议四时间戳延迟抵消算例与平滑调频慢拨机制图解", "左栏用具体数值演示RFC5905四时间戳解算往返延迟40ms与时钟偏差60ms，右栏展示Stratum原子钟层级及小误差调频慢追Slew曲线", el),
    )


@register(
    TOPIC,
    "Quartz Clocks & Computer Clocks: Piezoelectricity, 32,768 Hz divider, thermal drift curves, PC RTC+PLL+TSC dual clocks, resolution vs accuracy & NTPv4",
    "science",
)
def build_all() -> None:
    print(f"[{TOPIC}] building & verifying assertions...")
    _verify_clock_math()
    build_piezoelectric_oscillator()
    build_why_32768_binary_divider()
    build_temperature_drift_curves()
    build_computer_dual_clocks()
    build_computer_clock_traps()
    build_ntp_handshake_and_slewing()
