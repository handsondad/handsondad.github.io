"""氧化还原反应：电子账本、氧化数、丹尼尔电池、能斯特方程与生命工业场景。"""

from __future__ import annotations

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
    card,
    figure,
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

TOPIC = "redox-reactions"


def _line(x1, y1, x2, y2, stroke=SLATE, sw=1.6, dash=None, marker=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def _verify() -> None:
    # 氧化数校验
    assert (+4) + 2 * (-2) == 0
    assert 2 * (+1) + (-2) == 0
    # 丹尼尔电池
    e_cu, e_zn, n, faraday = 0.34, -0.7618, 2, 96485.0
    e_cell = e_cu - e_zn
    dg = -n * faraday * e_cell / 1000
    assert 1.10 < e_cell < 1.11
    assert -215 < dg < -210
    # 能斯特方程：[Zn2+]=1 M, [Cu2+]=0.01 M ⇒ Q=100, n=2
    e_nernst = e_cell - (0.0592 / n) * 2
    assert 1.03 < e_nernst < 1.05
    # 标准电极电势阶梯单调
    ladder = [-3.04, -0.76, -0.44, 0.34, 0.80, 1.23, 2.87]
    assert all(a < b for a, b in zip(ladder, ladder[1:]))


# ---------------------------------------------------------------------------
# 1. 电子账本：氧化与还原的正确对应
# ---------------------------------------------------------------------------
def build_electron_bookkeeping() -> str:
    els = []
    els.extend(
        header(
            "氧化还原的第一张图：电子从谁手里，交到谁手里",
            "氧化剂被还原、还原剂被氧化——这两个“被”字最容易写反。",
        )
    )

    els.append(card(20, 66, 352, 330))
    els.append(step_badge(38, 88, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 92, "氧化：失电子（还原剂做的事）", size=12.0, color=INK, weight="700"))
    els.append('<rect x="40" y="116" width="312" height="84" rx="8" fill="#fff8f2" stroke="#f0d5bc"/>')
    els.append(txt(60, 146, "还原剂", size=12.0, color=ORANGE, weight="700"))
    els.append(txt(60, 176, "Zn → Zn²⁺ + 2e⁻", size=13.0, color=INK, weight="700"))
    els.append(_line(196, 142, 294, 142, stroke=ORANGE, sw=2.2, marker="arr-orange"))
    els.append(txt(246, 132, "交出电子", size=9.8, color=ORANGE, anchor="middle"))
    els.append(txt(196, 230, "氧化数：0 → +2（升高）", size=10.6, color=ORANGE, weight="600"))
    els.append(txt(40, 262, "失去电子 = 被氧化 = 充当还原剂", size=10.6, color=BODY))
    els.append(txt(40, 292, "还原剂把自己氧化，好把电子送出去。", size=10.4, color=SLATE))
    els.append(txt(40, 340, "口诀：OIL — Oxidation Is Loss（氧化即失）", size=10.4, color=ORANGE, weight="700"))

    els.append(card(388, 66, 352, 330))
    els.append(step_badge(406, 88, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(424, 92, "还原：得电子（氧化剂做的事）", size=12.0, color=INK, weight="700"))
    els.append('<rect x="408" y="116" width="312" height="84" rx="8" fill="#f4f8fc" stroke="#cfe0ed"/>')
    els.append(txt(428, 146, "氧化剂", size=12.0, color=BLUE, weight="700"))
    els.append(txt(428, 176, "Cu²⁺ + 2e⁻ → Cu", size=13.0, color=INK, weight="700"))
    els.append(_line(564, 142, 662, 142, stroke=BLUE, sw=2.2, marker="arr-blue"))
    els.append(txt(614, 132, "收下电子", size=9.8, color=BLUE, anchor="middle"))
    els.append(txt(564, 230, "氧化数：+2 → 0（降低）", size=10.6, color=BLUE, weight="600"))
    els.append(txt(408, 262, "得到电子 = 被还原 = 充当氧化剂", size=10.6, color=BODY))
    els.append(txt(408, 292, "氧化剂把自己还原，换来对方的电子。", size=10.4, color=SLATE))
    els.append(txt(408, 340, "口诀：RIG — Reduction Is Gain（还原即得）", size=10.4, color=BLUE, weight="700"))

    els.append(_line(372, 180, 388, 180, stroke=PURPLE, sw=2.4, marker="arr-orange"))
    els.append(txt(380, 168, "e⁻", size=10.0, color=PURPLE, anchor="middle", weight="700"))

    els.append(card(20, 412, 720, 88))
    els.append(txt(40, 442, "你给的两行示例里，电子箭头方向是对的，但括号标签刚好写反了：", size=11.2, color=INK, weight="700"))
    els.append(txt(40, 468, "氧化剂 + e⁻ → 还原产物（这是“还原”，不是氧化）；还原剂 → 氧化产物 + e⁻（这是“氧化”，不是还原）。", size=10.8, color=BODY))
    els.append(txt(40, 492, "记法：谁“被”氧化/还原，看它自己发生了什么；它扮演的角色，正好是相反的那一面。", size=10.2, color=MUTED))

    return figure(
        510,
        "氧化还原电子账本：氧化剂被还原、还原剂被氧化图解",
        "左侧显示还原剂锌失电子生成锌离子，氧化数0升到+2，角色是还原剂；右侧显示氧化剂铜离子得电子生成铜，氧化数+2降到0，角色是氧化剂；底部纠正氧化剂加电子应标注还原、还原剂失电子应标注氧化。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 氧化数与半反应配平
# ---------------------------------------------------------------------------
def build_oxidation_numbers() -> str:
    els = []
    els.extend(
        header(
            "氧化数：给每个原子记一笔“电子账”",
            "不一定真有电子完全转移；氧化数是一种形式记账规则。",
        )
    )

    els.append(card(20, 66, 352, 372))
    els.append(step_badge(38, 88, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 92, "五条常用规则", size=12.0, color=INK, weight="700"))
    rules = [
        ("单质", "氧化数为 0", "O₂、Zn、C：都是 0"),
        ("单原子离子", "等于离子电荷", "Na⁺ 为 +1，Cl⁻ 为 −1"),
        ("氢", "通常为 +1", "金属氢化物中为 −1"),
        ("氧", "通常为 −2", "过氧化物中为 −1"),
        ("总和", "分子为 0；离子为净电荷", "H₂O：2×(+1)+(−2)=0"),
    ]
    for i, (name, rule, example) in enumerate(rules):
        y = 124 + i * 56
        els.append(f'<rect x="38" y="{y}" width="316" height="46" rx="6" fill="#f7fafc" stroke="#dbe6ee"/>')
        els.append(txt(50, y + 19, name, size=10.6, color=BLUE, weight="700"))
        els.append(txt(50, y + 37, rule, size=9.8, color=INK))
        els.append(txt(212, y + 28, example, size=9.6, color=SLATE))
    els.append(txt(38, 418, "IUPAC：异核键电子形式上判给电负性更大的一方。", size=10.2, color=MUTED))

    els.append(card(388, 66, 352, 372))
    els.append(step_badge(406, 88, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 92, "用氧化数追踪两个反应", size=12.0, color=INK, weight="700"))

    els.append(txt(404, 128, "① 置换反应", size=11.0, color=ORANGE, weight="700"))
    els.append(txt(404, 156, "Zn + Cu²⁺ → Zn²⁺ + Cu", size=12.4, color=INK, weight="700"))
    for x, label, color in [(418, "0", SLATE), (488, "+2", BLUE), (566, "+2", ORANGE), (650, "0", SLATE)]:
        els.append(txt(x, 180, label, size=10.4, color=color, anchor="middle", weight="700"))
    els.append(txt(404, 208, "Zn：0 → +2 升高，被氧化；", size=10.4, color=ORANGE))
    els.append(txt(404, 230, "Cu²⁺：+2 → 0 降低，被还原。", size=10.4, color=BLUE))
    els.append(_line(404, 244, 724, 244, stroke=BORDER, sw=1))

    els.append(txt(404, 274, "② 燃烧反应", size=11.0, color=ORANGE, weight="700"))
    els.append(txt(404, 302, "C + O₂ → CO₂", size=12.4, color=INK, weight="700"))
    els.append(txt(404, 330, "C：0 → +4（氧化）", size=10.6, color=ORANGE, weight="600"))
    els.append(txt(404, 354, "O：0 → −2（还原）", size=10.6, color=BLUE, weight="600"))
    els.append(txt(404, 384, "“氧化”不一定是和氧反应：", size=10.4, color=BODY))
    els.append(txt(404, 408, "本质是氧化数升高、失去电子。", size=10.6, color=INK, weight="700"))

    els.append(card(20, 452, 720, 44, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 480, "半反应法配平：先分开写氧化与还原，再让两边电子数相等，最后相加消去 e⁻。", size=10.8, color=SLATE))

    return figure(
        506,
        "氧化数规则与置换燃烧反应记账图",
        "左侧列出氧化数五条常用规则：单质为零、单原子离子等于电荷、氢通常正一、氧通常负二、分子总和为零；右侧用锌置换铜离子和碳燃烧两个反应示范氧化数升高即氧化、降低即还原，并强调氧化不等于必须与氧反应。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 丹尼尔电池
# ---------------------------------------------------------------------------
def build_daniell_cell() -> str:
    e_cell = 0.34 - (-0.7618)
    dg = -2 * 96485.0 * e_cell / 1000
    els = []
    els.extend(
        header(
            "把氧化还原拆成两半：电子被迫绕外电路走一趟",
            "丹尼尔电池里，锌被氧化、铜离子被还原，钱变成了电。",
        )
    )

    els.append(card(20, 66, 720, 372))
    # 左烧杯
    els.append('<rect x="60" y="152" width="200" height="180" rx="8" fill="#f4f8fc" stroke="#9fc7e8" stroke-width="1.6"/>')
    els.append('<rect x="62" y="194" width="196" height="136" rx="4" fill="#dbeafe" fill-opacity="0.8"/>')
    els.append('<rect x="132" y="106" width="22" height="150" rx="3" fill="#b8c0c9" stroke="#64748b" stroke-width="1.4"/>')
    els.append(txt(160, 200, "Zn 电极（−）", size=11.2, color=ORANGE, weight="700"))
    els.append(txt(160, 226, "阳极：Zn → Zn²⁺ + 2e⁻", size=10.6, color=BODY))
    els.append(txt(160, 252, "E°(Zn²⁺/Zn) = −0.76 V", size=10.4, color=SLATE))

    # 右烧杯
    els.append('<rect x="460" y="152" width="200" height="180" rx="8" fill="#f6f3fc" stroke="#c4b5fd" stroke-width="1.6"/>')
    els.append('<rect x="462" y="194" width="196" height="136" rx="4" fill="#e8e0ff" fill-opacity="0.8"/>')
    els.append('<rect x="538" y="106" width="22" height="150" rx="3" fill="#c9895a" stroke="#9a5b2e" stroke-width="1.4"/>')
    els.append(txt(568, 200, "Cu 电极（+）", size=11.2, color=BLUE, weight="700"))
    els.append(txt(568, 226, "阴极：Cu²⁺ + 2e⁻ → Cu", size=10.6, color=BODY))
    els.append(txt(568, 252, "E°(Cu²⁺/Cu) = +0.34 V", size=10.4, color=SLATE))

    # 外电路
    els.append(_line(143, 106, 143, 78, stroke=SLATE, sw=2))
    els.append(_line(143, 78, 549, 78, stroke=SLATE, sw=2))
    els.append(_line(549, 78, 549, 106, stroke=SLATE, sw=2))
    els.append(_line(210, 78, 470, 78, stroke=ORANGE, sw=2.6, marker="arr-orange"))
    els.append(txt(340, 66, "电子 e⁻ 从锌流向铜", size=10.6, color=ORANGE, anchor="middle", weight="700"))
    els.append(pill(274, 88, "电流计 / 负载", fg=PURPLE, bg=PURPLE_SOFT, w=112, h=22, size=10.2))

    # 盐桥
    els.append('<path d="M 260 210 C 320 176, 400 176, 460 210" fill="none" stroke="#94a3b8" stroke-width="14" stroke-linecap="round"/>')
    els.append('<path d="M 260 210 C 320 176, 400 176, 460 210" fill="none" stroke="#e2e8f0" stroke-width="9" stroke-linecap="round"/>')
    els.append(_line(300, 190, 342, 184, stroke=BLUE, sw=1.8, marker="arr-blue"))
    els.append(_line(420, 184, 378, 190, stroke=ORANGE, sw=1.8, marker="arr-orange"))
    els.append(txt(360, 154, "盐桥：离子迁移维持电中性", size=10.2, color=SLATE, anchor="middle"))

    els.append(txt(50, 360, "总反应：Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)", size=12.0, color=INK, weight="700"))
    els.append(txt(50, 396, f"E°cell = E°阴极 − E°阳极 = 0.34 − (−0.7618) = +{e_cell:.4f} V ≈ +1.10 V", size=11.0, color=ORANGE, weight="700"))
    els.append(txt(50, 422, f"n = 2，ΔG° = −nFE° ≈ {dg:.0f} kJ/mol（F = 96 485 C/mol）", size=10.6, color=BLUE))

    els.append(card(20, 452, 720, 48, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 480, "电池不创造新反应，只是把自发的氧化还原拆开，让电子经过外部电路去做功。", size=10.8, color=SLATE))

    return figure(
        510,
        "丹尼尔电池锌铜半电池电子流与电动势计算图",
        "左槽锌阳极发生氧化反应Zn生成锌离子加两电子，右槽铜离子阴极发生还原反应生成铜；电子经外电路从锌流向铜，盐桥离子迁移维持电中性；标准电动势等于阴极电势加0.34伏减去阳极电势负0.7618伏约1.10伏，对应自由能变化约负213千焦每摩尔。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 电势阶梯与能斯特方程
# ---------------------------------------------------------------------------
def build_nernst_ladder() -> str:
    e_cell = 0.34 - (-0.7618)
    e_nernst = e_cell - (0.0592 / 2) * 2
    els = []
    els.extend(
        header(
            "E° 是电子的“势能地图”，浓度会改写实际电压",
            "上方氧化性强，下方还原性强；差值就是电池电压。",
        )
    )

    els.append(card(20, 66, 352, 400))
    els.append(step_badge(38, 88, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 92, "标准还原电势阶梯（25 °C）", size=11.8, color=INK, weight="700"))
    ladder = [
        ("F₂ + 2e⁻ → 2F⁻", 2.87, ORANGE),
        ("O₂ + 4H⁺ + 4e⁻ → 2H₂O", 1.23, ORANGE),
        ("Ag⁺ + e⁻ → Ag", 0.80, ORANGE),
        ("Cu²⁺ + 2e⁻ → Cu", 0.34, ORANGE),
        ("Fe²⁺ + 2e⁻ → Fe", -0.44, BLUE),
        ("Zn²⁺ + 2e⁻ → Zn", -0.76, BLUE),
        ("Li⁺ + e⁻ → Li", -3.04, BLUE),
    ]
    for i, (label, value, color) in enumerate(ladder):
        y = 126 + i * 43
        els.append(txt(40, y, label, size=10.0, color=INK))
        els.append(f'<rect x="236" y="{y-12}" width="76" height="17" rx="4" fill="{BLUE_SOFT if value < 0 else ORANGE_SOFT}"/>')
        els.append(txt(274, y + 1, f"{value:+.2f} V", size=10.0, color=color, anchor="middle", weight="700"))
    els.append(txt(40, 444, "越靠上越容易得电子（强氧化剂）；越靠下越容易失电子（强还原剂）。", size=10.2, color=SLATE))

    els.append(card(388, 66, 352, 400))
    els.append(step_badge(406, 88, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 92, "能斯特方程：把浓度算进来", size=11.8, color=INK, weight="700"))
    els.append(txt(404, 130, "E = E° − (RT / nF)·ln Q", size=12.0, color=INK, weight="700"))
    els.append(txt(404, 158, "25 °C：E = E° − (0.0592 / n)·log Q", size=11.4, color=BLUE, weight="700"))
    els.append(txt(404, 186, "n = 转移电子数；Q = 反应商；F = 96 485 C/mol", size=10.0, color=SLATE))
    els.append(_line(404, 204, 724, 204, stroke=BORDER, sw=1))
    els.append(txt(404, 234, "算一算：锌铜电池，铜离子稀释 100 倍", size=11.0, color=ORANGE, weight="700"))
    els.append(txt(404, 264, "[Zn²⁺] = 1 M，[Cu²⁺] = 0.01 M", size=10.6, color=BODY))
    els.append(txt(404, 292, "Q = [Zn²⁺] / [Cu²⁺] = 100", size=10.6, color=BODY))
    els.append(txt(404, 320, "log Q = 2，n = 2", size=10.6, color=BODY))
    els.append(txt(404, 356, f"E = 1.10 − (0.0592/2)×2", size=11.2, color=INK, weight="700"))
    els.append(txt(404, 388, f"≈ {e_nernst:.2f} V（比标准状态低）", size=12.0, color=ORANGE, weight="700"))
    els.append(txt(404, 430, "浓度改变 → Q 改变 → 电压改变。", size=10.4, color=SLATE))

    els.append(card(20, 482, 720, 42, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 510, "E° > 0 表示标准状态下自发；但“自发”说的是热力学，不代表反应一定快。", size=10.8, color=SLATE))

    return figure(
        534,
        "标准还原电势阶梯与能斯特方程浓度修正图",
        "左侧按从高到低列出氟气2.87伏、氧气1.23伏、银离子0.80伏、铜离子0.34伏、亚铁负0.44伏、锌离子负0.76伏和锂离子负3.04伏的标准还原电势；右侧用能斯特方程计算锌铜电池在铜离子浓度0.01摩尔时电压由1.10伏降到约1.04伏。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 生命与工业中的氧化还原
# ---------------------------------------------------------------------------
def build_redox_applications() -> str:
    els = []
    els.extend(
        header(
            "同一套电子账本：燃烧、腐蚀、电池与代谢",
            "场景不同，主角不同；追踪的永远是电子往哪儿走。",
        )
    )

    panels = [
        (20, 66, "① 燃烧", ORANGE, ORANGE_SOFT,
         "CH₄ + 2O₂ → CO₂ + 2H₂O",
         "C：−4 → +4，被氧化；",
         "O：0 → −2，被还原。",
         "燃料是还原剂，氧气是氧化剂。"),
        (388, 66, "② 腐蚀", BLUE, BLUE_SOFT,
         "Fe → Fe²⁺ + 2e⁻",
         "O₂ + 2H₂O + 4e⁻ → 4OH⁻",
         "铁被氧化，氧气被还原；",
         "铁锈疏松，腐蚀会继续向内吃。"),
        (20, 286, "③ 电池", PURPLE, PURPLE_SOFT,
         "Zn → Zn²⁺ + 2e⁻",
         "Cu²⁺ + 2e⁻ → Cu",
         "把两半反应分开，",
         "逼电子经过外电路做功。"),
        (388, 286, "④ 代谢", GREEN, GREEN_SOFT,
         "NAD⁺ + 2e⁻ + H⁺ ⇌ NADH",
         "NAD⁺ 接电子变 NADH；",
         "NADH 再把电子交给电子传递链，",
         "释放的能量用于合成 ATP。"),
    ]
    for x, y, title, fg, soft, line1, line2, line3, line4 in panels:
        els.append(card(x, y, 352, 196))
        els.append(step_badge(x + 18, y + 22, 1 if y == 66 else 2, fg=fg, bg=soft))
        els.append(txt(x + 36, y + 26, title, size=11.8, color=INK, weight="700"))
        els.append(f'<rect x="{x+20}" y="{y+48}" width="312" height="38" rx="6" fill="{soft}" stroke="{fg}"/>')
        els.append(txt(x + 176, y + 73, line1, size=11.0, color=INK, anchor="middle", weight="700"))
        els.append(txt(x + 20, y + 112, line2, size=10.4, color=BODY))
        els.append(txt(x + 20, y + 140, line3, size=10.4, color=BODY))
        els.append(txt(x + 20, y + 170, line4, size=10.2, color=fg, weight="600"))

    els.append(card(20, 498, 720, 42, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 526, "共同规律：还原剂失去的电子数 = 氧化剂得到的电子数；配平方程式就是在守这条账。", size=10.8, color=SLATE))

    return figure(
        550,
        "燃烧腐蚀电池与代谢中的氧化还原统一图解",
        "四个场景并列：甲烷燃烧中碳从负四升到正四被氧化、氧从零降到负二被还原；铁腐蚀中铁失电子、氧气在水存在下得电子生成氢氧根；锌铜电池把两半反应分开迫使电子走外电路；代谢中NAD正离子接受电子变成NADH再把电子送入呼吸链合成ATP。",
        els,
    )


@register(TOPIC, "氧化还原反应：电子账本、氧化数、丹尼尔电池、能斯特方程与生命工业场景", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("redox-electron-bookkeeping.svg", build_electron_bookkeeping),
        ("oxidation-number-rules.svg", build_oxidation_numbers),
        ("daniell-cell-electron-flow.svg", build_daniell_cell),
        ("nernst-potential-ladder.svg", build_nernst_ladder),
        ("redox-in-life-and-industry.svg", build_redox_applications),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
