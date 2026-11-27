"""姆潘巴效应：反直觉的交叉、四个嫌疑人、1 厘米误差、新战场与家庭实验的原创 SVG 图解。"""

from __future__ import annotations

import math

from .core import (
    BODY,
    BORDER,
    BLUE,
    BLUE_SOFT,
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

TOPIC = "mpemba"

RED = "#b42318"
RED_SOFT = "#fee9e7"


def _line(x1, y1, x2, y2, stroke=SLATE, sw=1.5, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def _path(points, stroke=BLUE, sw=2.2, dash=None):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


def _dot(cx, cy, r=3.5, fill=BLUE):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="#ffffff" stroke-width="1"/>'


def _axes(x0, y0, w, h, label_x="时间", label_y="温度"):
    """返回坐标轴元素；绘图区映射 T:100→y0, -20→y0+h；t:0→x0, 20→x0+w。"""
    els = [
        f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="6" fill="#ffffff" stroke="{BORDER}"/>',
        _line(x0, y0 + h, x0 + w, y0 + h, stroke=HAIRLINE, sw=1.2),
        _line(x0, y0, x0, y0 + h, stroke=HAIRLINE, sw=1.2),
        txt(x0 + w, y0 + h + 16, label_x, size=10.5, color=MUTED, anchor="end"),
        txt(x0 - 4, y0 - 6, label_y, size=10.5, color=MUTED, anchor="end"),
    ]
    return els


def _txy(t, T, x0, y0, w, h):
    return x0 + t / 20.0 * w, y0 + (100.0 - T) / 120.0 * h


def _curve(T0, tau, x0, y0, w, h, stroke, t_end=20):
    pts = []
    t = 0.0
    while t <= t_end + 1e-9:
        T = -18.0 + (T0 + 18.0) * math.exp(-t / tau)
        pts.append(_txy(t, T, x0, y0, w, h))
        t += 0.25
    return _path(pts, stroke=stroke, sw=2.3)


def _verify() -> None:
    # 同一指数冷却模型：热水到 0°C 的时间必然更长
    ratio = math.log((90.0 + 18) / 18.0) / math.log((20.0 + 18) / 18.0)
    assert 2.3 < ratio < 2.5
    # 若要出现交叉，热水等效冷却时间常数必须显著变小
    cross = math.log(108.0 / 38.0) / (1.0 / 3.6 - 1.0 / 10.0)
    assert 5.0 < cross < 7.0
    assert 90.0 > 20.0 and cross < math.log(38.0 / 18.0) * 10.0
    # Burridge & Linden 2016 原文实验数据
    t_c, t_h = 6397.0, 10812.0
    q_ratio = (84.7 / t_h) / (21.8 / t_c)
    d_ratio = 84.7 / 21.8
    assert q_ratio < d_ratio
    assert 2.2 < q_ratio < 2.4 and 3.8 < d_ratio < 4.0
    assert t_h > t_c
    # 0°C 水结冰的潜热约等于从 80°C 冷到 0°C
    assert 80 > 0 and 10812 / 60 > 6397 / 60


# ---------------------------------------------------------------------------
# 1. 交叉为什么需要解释
# ---------------------------------------------------------------------------
def build_paradox() -> str:
    els = list(
        header(
            "问题的核心：热水必须“追上并超过”冷水，才可能先结冰",
            "下面两条曲线是同一冷却模型的示意，不是实验数据；先看哪里需要额外机制。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=SLATE, bg=SLATE_SOFT))
    els.append(txt(56, 93, "常识模型：同一条降温规律", size=11.8, color=INK, weight="700"))
    x0, y0, w, h = 44, 118, 300, 226
    els += _axes(x0, y0, w, h)
    y_zero = _txy(0, 0, x0, y0, w, h)[1]
    els.append(_line(x0, y_zero, x0 + w, y_zero, stroke=ORANGE, sw=1.2, dash="5 4"))
    els.append(txt(x0 + w - 2, y_zero - 5, "0°C", size=10.5, color=ORANGE, anchor="end"))
    els.append(_curve(90, 10, x0, y0, w, h, ORANGE))
    els.append(_curve(20, 10, x0, y0, w, h, BLUE))
    t_cold = math.log(38.0 / 18.0) * 10
    t_hot = math.log(108.0 / 18.0) * 10
    xc, yc = _txy(t_cold, 0, x0, y0, w, h)
    xh, yh = _txy(t_hot, 0, x0, y0, w, h)
    els.append(_dot(xc, yc, fill=BLUE))
    els.append(_dot(xh, yh, fill=ORANGE))
    els.append(txt(xc - 4, yc + 18, f"冷 {t_cold:.1f} 分", size=10.5, color=BLUE, anchor="end"))
    els.append(txt(xh + 4, yh - 6, f"热 {t_hot:.1f} 分", size=10.5, color=ORANGE))
    els.append(txt(40, 366, "同一条曲线 → 热水永远落在冷水后面", size=10.5, color=SLATE))
    els.append(txt(40, 388, "这不是热力学第一定律被推翻，而是提示缺少机制。", size=10.5, color=MUTED))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 93, "姆潘巴说法：曲线必须交叉", size=11.8, color=INK, weight="700"))
    x1 = 412
    els += _axes(x1, y0, w, h)
    els.append(_line(x1, y_zero, x1 + w, y_zero, stroke=ORANGE, sw=1.2, dash="5 4"))
    els.append(_curve(90, 3.6, x1, y0, w, h, ORANGE))
    els.append(_curve(20, 10, x1, y0, w, h, BLUE))
    cross = math.log(108.0 / 38.0) / (1.0 / 3.6 - 1.0 / 10.0)
    t_cross = 20.0 + 18.0 * math.exp(-cross / 3.6)
    xcr, ycr = _txy(cross, t_cross, x1, y0, w, h)
    els.append(_dot(xcr, ycr, r=4.5, fill=RED))
    els.append(txt(xcr + 6, ycr - 8, "交叉点", size=10.5, color=RED, weight="700"))
    els.append(txt(408, 366, "要交叉，热水必须多一条散热通道：", size=10.5, color=SLATE))
    els.append(pill(408, 380, "蒸发带走质量与热量", fg=ORANGE, bg=ORANGE_SOFT, w=150, h=22, size=10.5))
    els.append(pill(408, 408, "对流改变传热路径", fg=BLUE, bg=BLUE_SOFT, w=132, h=22, size=10.5))
    els.append(pill(408, 436, "成核时间被改写", fg=PURPLE, bg=PURPLE_SOFT, w=132, h=22, size=10.5))

    els.append(card(20, 500, 720, 78, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "先定义再争论：是“先降到 0°C”，还是“先出现第一粒冰”，还是“完全冻成冰块”？", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "2016 年的综述指出，文献里这三件事经常混用——相当一部分争吵其实不在同一个赛道上。", size=10.5, color=SLATE))
    return figure(
        590,
        "姆潘巴效应为什么需要额外机制的解释图",
        "左栏用同一指数冷却模型示意90度热水与20度冷水降到0度的时间分别约17.9分与7.5分热水不可能反超右栏画出曲线交叉并要求蒸发对流或成核时间等额外机制底栏强调必须先定义降到0度出现第一粒冰还是完全冻结。两栏曲线均为示意非实验数据。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 四个嫌疑人
# ---------------------------------------------------------------------------
def build_suspects() -> str:
    els = list(
        header(
            "四个最常被点名的“嫌疑人”，以及各自的边界",
            "它们确实都会改变冷却或结冰；难点在于，单独拿出哪一个都难以稳定解释全部实验。",
        )
    )

    blocks = [
        (
            20, 66, ORANGE, ORANGE_SOFT, "① 蒸发",
            ["热水蒸发更快：水量变少，", "汽化潜热也直接带走能量。"],
            ["但密闭容器会堵住这条通道；", "失水量通常不足以解释大幅反超。"],
        ),
        (
            388, 66, BLUE, BLUE_SOFT, "② 自然对流",
            ["温差越大，浮力驱动越强，", "杯内翻滚把热量送到杯壁。"],
            ["但对流标度分析显示：在同一", "标度下，热水到 0°C 仍更慢。"],
        ),
        (
            20, 286, PURPLE, PURPLE_SOFT, "③ 溶解气体",
            ["加热赶走溶解空气，改变", "成核条件与局部导热。"],
            ["主要影响“什么时候开始结冰”，", "不等于“谁先降到 0°C”。"],
        ),
        (
            388, 286, GREEN, GREEN_SOFT, "④ 过冷",
            ["水可低于 0°C 仍不结冰；", "谁先成核高度依赖杂质。"],
            ["2025 年受控实验里，热水反而", "更晚开始结晶，却冻得更深。"],
        ),
    ]
    for x, y, fg, bg, title, upper, lower in blocks:
        els.append(card(x, y, 352, 200))
        els.append(f'<rect x="{x+16}" y="{y+16}" width="316" height="30" rx="7" fill="{bg}"/>')
        els.append(txt(x + 30, y + 37, title, size=11.8, color=fg, weight="700"))
        for i, line in enumerate(upper):
            els.append(txt(x + 30, y + 76 + i * 22, line, size=10.5, color=BODY))
        els.append(_line(x + 30, y + 126, x + 322, y + 126, stroke=BORDER, sw=1))
        for i, line in enumerate(lower):
            els.append(txt(x + 30, y + 150 + i * 22, line, size=10.5, color=MUTED))

    els.append(card(20, 500, 720, 78, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "别忘了第五类变量：杯底霜层、容器材质、探头高度、开关门次数。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "2016 年的实验证明：温度探头位置哪怕差 1 cm，就足以把“没效应”读成“有效应”。", size=10.5, color=SLATE))
    return figure(
        590,
        "姆潘巴效应四种经典解释及其边界图",
        "四张卡片分别列出蒸发自然对流溶解气体与过冷的作用机制和各自边界其中过冷卡片指出2025年受控实验中热水更晚开始结晶却冻得更深底栏强调杯底霜容器探头高度等实验变量并指出探头差1厘米足以造成假阳性。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 一厘米如何翻转结论
# ---------------------------------------------------------------------------
def build_measurement() -> str:
    els = list(
        header(
            "2016 年那盆水：把“热水更快”变成了一个测量问题",
            "下面三组数字来自 Burridge & Linden 的原文实验；判据也是他们给出的。",
        )
    )

    els.append(card(20, 66, 720, 168))
    els.append(txt(38, 92, "同一冰柜、同样 400 g 水、煮沸后放置到三个初温；降到 0°C 的时间：", size=11.2, color=INK, weight="700"))
    data = [(21.8, 6397, BLUE), (57.3, 9504, PURPLE), (84.7, 10812, ORANGE)]
    for i, (temp, secs, color) in enumerate(data):
        x = 66 + i * 226
        els.append(f'<rect x="{x}" y="110" width="180" height="104" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        els.append(f'<rect x="{x+58}" y="126" width="64" height="52" rx="4" fill="{color}" fill-opacity="0.22" stroke="{color}"/>')
        els.append(txt(x + 90, 158, f"{temp:g}°C", size=11.5, color=color, anchor="middle", weight="700"))
        els.append(txt(x + 90, 196, f"t₀ = {secs/60:.1f} 分钟", size=10.5, color=BODY, anchor="middle"))
        els.append(txt(x + 90, 212, f"（{secs} 秒）", size=10.5, color=MUTED, anchor="middle"))

    els.append(card(20, 248, 720, 208))
    els.append(txt(38, 274, "判据：热水平均散热率之比 > 需要移走的热量之比，才算看到效应", size=11.2, color=INK, weight="700"))
    q_ratio = (84.7 / 10812.0) / (21.8 / 6397.0)
    d_ratio = 84.7 / 21.8
    bx, bw, scale = 250, 380, 4.2
    els.append(txt(38, 312, "实际散热率比 Q热/Q冷", size=10.5, color=BLUE))
    els.append(f'<rect x="{bx}" y="300" width="{bw*q_ratio/scale:.1f}" height="18" rx="5" fill="{BLUE}"/>')
    els.append(txt(bx + bw * q_ratio / scale + 8, 313, f"{q_ratio:.2f}", size=10.5, color=BLUE, weight="700"))
    els.append(txt(38, 350, "需要移走的热量比 ΔT热/ΔT冷", size=10.5, color=ORANGE))
    els.append(f'<rect x="{bx}" y="338" width="{bw*d_ratio/scale:.1f}" height="18" rx="5" fill="{ORANGE}"/>')
    els.append(txt(bx + bw * d_ratio / scale + 8, 351, f"{d_ratio:.2f}", size=10.5, color=ORANGE, weight="700"))
    els.append(_line(bx, 372, bx + bw, 372, stroke=HAIRLINE, sw=1))
    els.append(txt(38, 404, "2.30 < 3.89：热水没有反超；热水初温越高，到 0°C 的时间反而越长。", size=10.5, color=SLATE))
    els.append(txt(38, 432, "这正是论文标题的意思：“热水并不比冷水冷却得更快”。", size=10.5, color=MUTED))

    els.append(card(20, 470, 720, 108, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 496, "最容易被忽略的一行：探头位置差 1 cm，数据点就会落到“姆潘巴线”上方。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 524, "把结冰过程也算进去也不救命：0°C 的水结成冰，潜热约等于把同样多的水从 80°C 冷到 0°C。", size=10.5, color=BODY))
    els.append(txt(38, 552, "成核又极度依赖微小杂质与容器缺陷，重复出的差异常与测量波动同量级。", size=10.5, color=MUTED))
    return figure(
        592,
        "2016年姆潘巴效应对照实验与一厘米测量误差图",
        "顶部给出三组原文实验数据初温21.8度57.3度84.7度对应降到0度时间6397秒9504秒10812秒中部用条形比较84.7度与21.8度的平均散热率比2.30和需要移走热量比3.89说明未反超底部指出探头位置差1厘米即可造成假阳性并说明结冰潜热约等于从80度冷到0度。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 2025—2026 的新战场
# ---------------------------------------------------------------------------
def build_frontier() -> str:
    els = list(
        header(
            "2025—2026：争论没有结束，但战场已经换了",
            "水杯、热力学判据、量子系统、玻璃材料——四条线各自回答不同的问题。",
        )
    )

    cards = [
        (
            20, ORANGE, ORANGE_SOFT, "① 受控冻结实验（2025）",
            [
                "冰核剂饱和冰柜，",
                "消除随机过冷；",
                "热水冻得更快更深，",
                "但开始结晶更晚。",
                "解释回到牛顿传热：",
                "温差大 → 热流大。",
            ],
        ),
        (
            256, BLUE, BLUE_SOFT, "② 严格判据（2025）",
            [
                "热主序 thermomajorization，",
                "不再挑一个距离度量；",
                "统一所有单调度量；",
                "在马尔可夫动力学中，",
                "任意温度区间都可能",
                "出现该效应。",
            ],
        ),
        (
            492, PURPLE, PURPLE_SOFT, "③ 量子与材料（2025—26）",
            [
                "离子阱 qutrit 观测",
                "量子强姆潘巴效应；",
                "单量子比特用消相干",
                "切断最慢衰减模；",
                "玻璃中经 β 弛豫",
                "发现类姆潘巴老化。",
            ],
        ),
    ]
    for x, fg, bg, title, lines in cards:
        els.append(card(x, 66, 226, 412))
        els.append(f'<rect x="{x+14}" y="82" width="198" height="34" rx="7" fill="{bg}"/>')
        els.append(txt(x + 23, 105, title, size=10.5, color=fg, weight="700"))
        for i, line in enumerate(lines):
            y = 140 + i * 48
            els.append(f'<circle cx="{x+22}" cy="{y-4}" r="2.5" fill="{fg}"/>')
            els.append(txt(x + 34, y, line, size=10.5, color=BODY))

    els.append(card(20, 492, 720, 86, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 518, "不能画等号：热水先结冰 ≠ 离平衡更远却更快弛豫 ≠ 强姆潘巴效应。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 546, "“强”有严格含义：让初态与最慢衰减模的重叠为零，之后的指数衰减率由次慢模决定。", size=10.5, color=SLATE))
    els.append(txt(38, 570, "前面三张图讲的是一杯水；这一张讲的是同一个名字下的推广与重新定义。", size=10.5, color=MUTED))
    return figure(
        590,
        "2025至2026年姆潘巴效应研究三条新战线图",
        "三栏分别总结2025年冰核剂受控冻结实验发现热水冻得更深但结晶更晚2025年热主序理论给出不依赖距离度量的严格判据以及2025到2026年离子阱单量子比特与玻璃材料中的量子和类姆潘巴效应底栏强调热水先结冰不等于离平衡更远更快弛豫也不等于强姆潘巴效应。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 自己动手怎么不骗自己
# ---------------------------------------------------------------------------
def build_protocol() -> str:
    els = list(
        header(
            "想在家验证？先把实验写成一份“可复现协议”",
            "如果只是随手把两杯水丢进冰箱，你看到的更可能是杯子位置和霜层，而不是效应。",
        )
    )

    els.append(card(20, 66, 352, 420))
    steps = [
        ("① 先定义终点", ["出现第一粒冰 / 降到 0°C /", "完全冻结：三选一写下来。"]),
        ("② 控制变量", ["同水量、同容器、同探头高度；", "同时放入、全程不挪动。"]),
        ("③ 连续记录", ["多个探头秒级记录，记下", "冷冻室温度与开关门时间。"]),
        ("④ 看波动", ["重复十几轮，比较平均值", "与离散度；差值小于波动", "就只能写“没看到”。"]),
    ]
    for i, (name, lines) in enumerate(steps):
        y = 94 + i * 98
        els.append(f'<rect x="38" y="{y}" width="316" height="86" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        els.append(txt(54, y + 25, name, size=11.2, color=BLUE, weight="700"))
        for j, line in enumerate(lines):
            els.append(txt(54, y + 48 + j * 18, line, size=10.5, color=BODY))

    els.append(card(388, 66, 352, 420))
    els.append(txt(406, 93, "三种“结冰”，别混着说", size=11.8, color=INK, weight="700"))
    ends = [
        ("开始成核", "受杂质与微小缺陷支配", PURPLE, PURPLE_SOFT),
        ("降到 0°C", "2016 年判据针对的阶段", BLUE, BLUE_SOFT),
        ("完全冻结", "还要移走凝固潜热，量级很大", ORANGE, ORANGE_SOFT),
    ]
    for i, (a, b, fg, bg) in enumerate(ends):
        y = 118 + i * 74
        els.append(f'<rect x="406" y="{y}" width="316" height="62" rx="7" fill="{bg}" stroke="{fg}"/>')
        els.append(txt(420, y + 25, a, size=11.2, color=fg, weight="700"))
        els.append(txt(420, y + 48, b, size=10.5, color=BODY))
    els.append(_line(406, 356, 722, 356, stroke=BORDER, sw=1))
    els.append(txt(406, 382, "实用建议：想快点得到冰，用浅金属盘、小水量、贴紧冷板。", size=10.5, color=BODY))
    els.append(txt(406, 408, "“先烧热再冻”既不稳定，也更费电，别当成节能捷径。", size=10.5, color=MUTED))
    els.append(pill(406, 430, "效应是科学问题，制冰是工程问题", fg=GREEN, bg=GREEN_SOFT, w=250, h=24, size=10.5))

    els.append(card(20, 500, 720, 78, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "判断是否复现的最低标准：同样条件下，差异要稳定、显著、并且能被别人重复。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "一条也没有满足时，最老实的写法是：这次没有观察到姆潘巴效应。", size=10.5, color=SLATE))
    return figure(
        590,
        "家庭验证姆潘巴效应的可复现实验协议图",
        "左栏四步协议先定义终点再控制变量再连续记录最后看波动右栏区分开始成核降到0度完全冻结三种结冰终点并给出浅金属盘小水量贴紧冷板的实用建议底栏强调稳定显著可重复才算复现否则应如实写没观察到。",
        els,
    )


@register(TOPIC, "姆潘巴效应：反直觉交叉、四个机制、1厘米误差、2025—2026新进展与实验协议", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("mpemba-paradox.svg", build_paradox),
        ("mpemba-suspects.svg", build_suspects),
        ("mpemba-measurement.svg", build_measurement),
        ("mpemba-frontier.svg", build_frontier),
        ("mpemba-protocol.svg", build_protocol),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
