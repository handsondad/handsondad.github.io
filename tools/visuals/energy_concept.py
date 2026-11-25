"""能量的定义、形式、守恒、地球能量收支、光热转换与光合作用原创图解。"""

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
    card,
    figure,
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

TOPIC = "energy-concept"


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
    # 机械能守恒：1 kg 从 5 m 落下
    m, g, hgt = 1.0, 9.8, 5.0
    pe = m * g * hgt
    v = math.sqrt(2 * g * hgt)
    ke = 0.5 * m * v**2
    assert 48 < pe < 50 and 9.8 < v < 10.0
    assert abs(pe - ke) < 1e-9

    # 地球能量收支
    solar = 1361.0
    mean = solar / 4
    absorbed = mean * 0.7
    assert 338 < mean < 342
    assert 238 < absorbed < 242
    sigma = 5.670374419e-8
    t_eff = (absorbed / sigma) ** 0.25
    surface_emit = sigma * 288.0**4
    assert 254 < t_eff < 256
    assert 385 < surface_emit < 395

    # 维恩位移
    b = 2.8977729e-3
    for temp, lo, hi in [(5778, 490, 510), (3000, 950, 990), (310, 9300, 9400)]:
        peak_nm = b / temp * 1e9
        assert lo < peak_nm < hi

    # 680 nm 光子能量
    h_planck, c_light, e_charge = 6.62607015e-34, 2.99792458e8, 1.602176634e-19
    photon_j = h_planck * c_light / (680e-9)
    photon_ev = photon_j / e_charge
    assert 2.9e-19 < photon_j < 3.0e-19
    assert 1.80 < photon_ev < 1.85


# ---------------------------------------------------------------------------
# 1. 能量形式地图
# ---------------------------------------------------------------------------
def build_energy_forms() -> str:
    els = []
    els.extend(
        header(
            "能量不是一种东西，而是一本统一的账",
            "动能、势能、热能、电能、光能……名字不同，账本上的单位都是焦耳。",
        )
    )

    forms = [
        (20, 66, "动能", BLUE, BLUE_SOFT, "运动着的物体", "Eₖ = ½mv²", "风、流水、飞驰的车"),
        (388, 66, "势能", ORANGE, ORANGE_SOFT, "位置或状态储存", "Eₚ = mgh / ½kx²", "水库、拉开的弓、化学键"),
        (20, 268, "热能", GREEN, GREEN_SOFT, "微观粒子无规则运动", "与温度和物质量都有关", "热水、地热、人体"),
        (388, 268, "电能", PURPLE, PURPLE_SOFT, "电荷与电势差", "E = qV", "电池、电网、静电"),
        (20, 470, "光能（辐射能）", "#b45309", "#fef3c7", "电磁波的能量", "E = hν = hc/λ", "阳光、红外、微波"),
        (388, 470, "核能", "#be123c", "#ffe4e6", "原子核结合能", "ΔE = Δm·c²", "太阳、核电站、放射性"),
    ]
    for x, y, title, fg, soft, desc, formula, example in forms:
        els.append(card(x, y, 352, 180))
        els.append(f'<rect x="{x+18}" y="{y+18}" width="112" height="30" rx="8" fill="{soft}" stroke="{fg}"/>')
        els.append(txt(x + 74, y + 39, title, size=11.4, color=fg, anchor="middle", weight="700"))
        els.append(txt(x + 20, y + 76, desc, size=10.6, color=INK, weight="600"))
        els.append(txt(x + 20, y + 106, formula, size=11.6, color=fg, weight="700"))
        els.append(txt(x + 20, y + 140, "例：" + example, size=10.2, color=BODY))
        els.append(txt(x + 20, y + 166, "单位：焦耳（J）", size=9.8, color=MUTED))

    els.append(card(20, 662, 720, 40, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 688, "分类是方便记账，不是物理壁垒：电池里是化学势能，灯泡把它变成光与热。", size=10.8, color=SLATE))

    return figure(
        712,
        "能量六种常见形式与公式示例图",
        "六个卡片分别列出动能二分之一mv平方、势能mgh与二分之一kx平方、热能取决于温度和物质量、电能qV、光能hν以及核能质能方程，强调各类能量单位都是焦耳且可相互转化。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 能量守恒：势能换动能
# ---------------------------------------------------------------------------
def build_conservation() -> str:
    m, g, hgt = 1.0, 9.8, 5.0
    pe = m * g * hgt
    v = math.sqrt(2 * g * hgt)
    ke = 0.5 * m * v**2
    els = []
    els.extend(
        header(
            "能量守恒：账不会平白多出一分，也不会少一分",
            "只看机械能与内能的互换，就能看懂刹车、摆锤和过山车。",
        )
    )

    els.append(card(20, 66, 430, 400))
    els.append(step_badge(38, 88, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 92, "1 kg 小球从 5 m 高处由静止落下", size=11.8, color=INK, weight="700"))

    els.append(_line(80, 152, 400, 152, stroke=SLATE, sw=1.4))
    for x, label in [(80, "0 m"), (240, "2.5 m"), (400, "5 m")]:
        els.append(_line(x, 148, x, 158, stroke=SLATE, sw=1))
        els.append(txt(x, 176, label, size=9.8, color=MUTED, anchor="middle"))
    els.append('<circle cx="80" cy="140" r="12" fill="#dbeafe" stroke="#1d6fa5" stroke-width="1.6"/>')
    els.append('<circle cx="240" cy="140" r="12" fill="#fde4d0" stroke="#c25014" stroke-width="1.6"/>')
    els.append('<circle cx="400" cy="140" r="12" fill="#f9d7b5" stroke="#c25014" stroke-width="1.6"/>')
    els.append(txt(400, 122, "起点：全部是势能", size=10.2, color=ORANGE, anchor="end"))
    els.append(_line(390, 132, 330, 132, stroke=ORANGE, sw=1.5, marker="arr-orange"))

    els.append(txt(48, 216, "高度 5 m：", size=10.6, color=ORANGE, weight="700"))
    els.append(txt(48, 242, f"Eₚ = mgh = 1×9.8×5 = {pe:.0f} J；Eₖ = 0", size=11.4, color=INK, weight="700"))
    els.append(txt(48, 280, "落地前：", size=10.6, color=BLUE, weight="700"))
    els.append(txt(48, 306, f"v = √(2gh) ≈ {v:.1f} m/s；Eₖ = ½mv² ≈ {ke:.0f} J", size=11.4, color=INK, weight="700"))
    els.append(_line(44, 324, 428, 324, stroke=BORDER, sw=1))
    els.append(txt(48, 354, "总机械能一直是 49 J——势能少了多少，动能就多多少。", size=10.6, color=BODY))
    els.append(txt(48, 388, "撞地后动能耗散为热与声：能量没消失，只是变得“不好再用”。", size=10.6, color=PURPLE, weight="600"))
    els.append(txt(48, 430, "效率 η = 有用输出 / 总输入；守恒不等于全部可用。", size=10.4, color=SLATE))

    els.append(card(466, 66, 274, 400))
    els.append(step_badge(484, 88, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(502, 92, "势能与动能的柱状互换", size=11.8, color=INK, weight="700"))
    bars = [("起点", 49, 0), ("半程", 24.5, 24.5), ("落地前", 0, 49)]
    for i, (label, ep, ek) in enumerate(bars):
        y = 130 + i * 102
        els.append(txt(484, y, label, size=10.6, color=INK, weight="600"))
        max_w = 190
        els.append(f'<rect x="484" y="{y+12}" width="{max_w*ep/49:.1f}" height="18" rx="4" fill="#f2b880"/>')
        els.append(f'<rect x="{484+max_w*ep/49:.1f}" y="{y+12}" width="{max_w*ek/49:.1f}" height="18" rx="4" fill="#9fc7e8"/>')
        els.append(txt(484, y + 48, f"Eₚ {ep:.0f} J   Eₖ {ek:.0f} J   总 49 J", size=9.8, color=SLATE))
    els.append(txt(484, 440, "橙色＝势能，蓝色＝动能；总长度不变。", size=9.8, color=MUTED))

    els.append(card(20, 482, 720, 46, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 511, "能量守恒定律：能量只能转移或转化，总量不变；效率掌管“有多少还能拿来干活”。", size=10.8, color=SLATE))

    return figure(
        538,
        "势能转动能的机械能守恒与效率图",
        "一千克小球从五米高处落下，起点重力势能49焦、动能为零；落地前速度约9.9米每秒、动能49焦；柱状图显示三个位置势能与动能互换但总和49焦不变，撞地后能量转为热与声说明守恒不等于全部可用。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 地球能量收支
# ---------------------------------------------------------------------------
def build_earth_budget() -> str:
    solar, sigma = 1361.0, 5.670374419e-8
    mean = solar / 4
    reflected = mean * 0.29
    absorbed = mean * 0.71
    t_eff = (absorbed / sigma) ** 0.25
    surface_emit = sigma * 288.0**4
    els = []
    els.extend(
        header(
            "地球的能量账：来的太阳光，最后都以红外光走",
            "几何平均一除四，反照率再打七折——剩下的才真正进入气候系统。",
        )
    )

    els.append(card(20, 66, 352, 400))
    els.append(step_badge(38, 88, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 92, "为什么 1361 变成 340？", size=11.8, color=INK, weight="700"))
    els.append('<circle cx="196" cy="204" r="66" fill="#f4f8fc" stroke="#9fc7e8" stroke-width="1.6"/>')
    els.append(_line(196, 112, 196, 138, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    els.append(txt(196, 126, "阳光", size=9.8, color=ORANGE, anchor="middle"))
    els.append(_line(196, 270, 196, 296, stroke=BLUE, sw=2.4, marker="arr-blue"))
    els.append(txt(196, 290, "红外", size=9.8, color=BLUE, anchor="middle"))
    els.append(txt(38, 156, "太阳常数 ≈ 1361 W/m²", size=10.6, color=ORANGE, weight="600"))
    els.append(txt(38, 340, "截面积 πR² 接光，球面 4πR² 分摊 ⇒ ÷4", size=10.4, color=BODY))
    els.append(txt(38, 370, f"全球平均入射 ≈ {mean:.0f} W/m²", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 410, "这就是 NASA 常说的 “340 W/m²”。", size=10.2, color=SLATE))

    els.append(card(388, 66, 352, 400))
    els.append(step_badge(406, 88, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(424, 92, "340 的去向与温度", size=11.8, color=INK, weight="700"))
    flows = [
        ("入射太阳", 340, ORANGE),
        ("反射回太空（约 29%）", reflected, SLATE),
        ("地球系统吸收（约 71%）", absorbed, ORANGE),
        ("向外红外辐射", absorbed, BLUE),
    ]
    for i, (label, value, color) in enumerate(flows):
        y = 124 + i * 52
        els.append(txt(404, y, label, size=10.2, color=INK))
        els.append(f'<rect x="404" y="{y+8}" width="{value/340*272:.1f}" height="16" rx="4" fill="{color}"/>')
        els.append(txt(684, y + 20, f"{value:.0f} W/m²", size=9.8, color=color, anchor="start", weight="700"))
    els.append(_line(404, 340, 724, 340, stroke=BORDER, sw=1))
    els.append(txt(404, 370, f"有效辐射温度 ≈ {t_eff:.0f} K（−18°C）", size=10.8, color=BLUE, weight="600"))
    els.append(txt(404, 398, f"地表 288 K 向外辐射 ≈ {surface_emit:.0f} W/m²", size=10.8, color=ORANGE, weight="600"))
    els.append(txt(404, 430, "温室效应让地表比“从太空看”热约 33°C。", size=10.4, color=PURPLE, weight="600"))

    els.append(card(20, 482, 720, 48, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 511, "长期平均下吸收太阳能 ≈ 向外红外能；两边失衡，地球就会升温或降温。", size=10.8, color=SLATE))

    return figure(
        540,
        "地球能量收支几何平均反照率与红外辐射图",
        "太阳常数1361瓦每平方米按地球截面积与球面面积之比除以四得到全球平均340瓦每平方米，其中约100被反射、240被吸收并以红外形式向太空辐射；有效辐射温度约255开尔文，地表288开尔文向外辐射约390瓦每平方米，温室效应使地表高约33摄氏度。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 光与热的互转
# ---------------------------------------------------------------------------
def build_light_and_heat() -> str:
    b = 2.8977729e-3
    peaks = [("太阳光球", 5778, "#eab308"), ("白炽灯丝", 3000, "#f97316"), ("人体皮肤", 310, "#ef4444")]
    x0, x1 = 408, 700
    def logx(um):
        return x0 + (math.log10(um) + 1) / 3 * (x1 - x0)

    els = []
    els.extend(
        header(
            "光变热，热也会变光：两者是同一份能量的不同外衣",
            "吸收让分子动起来；足够热的物体自己就会发光。",
        )
    )

    els.append(card(20, 66, 352, 372))
    els.append(step_badge(38, 88, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 92, "光照到物体：三条去路", size=11.8, color=INK, weight="700"))
    els.append(_line(48, 158, 156, 158, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    els.append(txt(90, 146, "入射光", size=9.8, color=ORANGE, anchor="middle"))
    els.append('<rect x="160" y="126" width="86" height="64" rx="6" fill="#f4f8fc" stroke="#94a3b8" stroke-width="1.5"/>')
    els.append(txt(203, 164, "物体", size=10.4, color=INK, anchor="middle", weight="700"))
    els.append(_line(246, 142, 320, 114, stroke=BLUE, sw=2, marker="arr-blue"))
    els.append(txt(300, 108, "反射", size=9.8, color=BLUE, anchor="middle"))
    els.append(_line(246, 158, 320, 158, stroke=GREEN, sw=2, marker="arr-green"))
    els.append(txt(300, 152, "透射", size=9.8, color=GREEN, anchor="middle"))
    els.append(_line(246, 174, 320, 202, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    els.append(txt(300, 214, "吸收→热", size=9.8, color=ORANGE, anchor="middle"))
    els.append(_line(38, 226, 350, 226, stroke=BORDER, sw=1))
    els.append(txt(38, 256, "吸收的光子能量转成分子振动、转动，", size=10.4, color=BODY))
    els.append(txt(38, 282, "宏观表现就是温度升高。", size=10.4, color=BODY))
    els.append(txt(38, 320, "热辐射反过来发光：", size=11.0, color=PURPLE, weight="700"))
    els.append(txt(38, 350, "铁块加热先暗红、再橙黄、最后白炽。", size=10.4, color=BODY))
    els.append(txt(38, 390, "白天晒被子暖，夜里被子也向夜空发红外。", size=10.2, color=SLATE))

    els.append(card(388, 66, 352, 372))
    els.append(step_badge(406, 88, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(424, 92, "维恩位移：越热，光越偏蓝", size=11.8, color=INK, weight="700"))
    els.append(_line(x0, 300, x1, 300, stroke=SLATE, sw=1.5))
    for um in (0.1, 1, 10, 100):
        xx = logx(um)
        els.append(_line(xx, 296, xx, 306, stroke=SLATE, sw=1))
        els.append(txt(xx, 322, f"{um:g} µm", size=9.4, color=MUTED, anchor="middle"))
    els.append(txt(554, 348, "波长 λ（对数刻度）", size=10.0, color=SLATE, anchor="middle"))
    for idx, (name, temp, color) in enumerate(peaks):
        peak_um = b / temp * 1e6
        xx = logx(peak_um)
        label_y = 108 if idx == 1 else 132
        peak_y = 246 if idx == 1 else 270
        els.append(_line(xx, label_y + 12, xx, 300, stroke=color, sw=1.4, dash="4 4"))
        els.append('<circle cx="%.1f" cy="300" r="5" fill="%s"/>' % (xx, color))
        els.append(txt(xx, label_y, f"{name} {temp} K", size=9.8, color=color, anchor="middle", weight="700"))
        els.append(txt(xx, peak_y, f"峰值 {peak_um:.2f} µm", size=9.4, color=color, anchor="middle"))
    els.append(txt(404, 392, "λ峰值 = b / T，b ≈ 2.898×10⁻³ m·K", size=10.8, color=INK, weight="700"))
    els.append(txt(404, 418, "太阳峰值在可见光；人体峰值在红外。", size=10.2, color=SLATE))

    els.append(card(20, 454, 720, 44, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 482, "光与热不是“同一种东西”，而是能量在电磁辐射与微观运动之间来回换账。", size=10.8, color=SLATE))

    return figure(
        508,
        "光热转换与维恩位移黑体峰值波长图",
        "左栏展示光被反射透射或吸收，吸收后转为分子振动热，物体升温又会发出热辐射；右栏按维恩位移定律在对数波长轴上标出太阳5778开峰值约0.50微米、白炽灯3000开约0.97微米、人体310开约9.35微米。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 光合作用能量链
# ---------------------------------------------------------------------------
def build_photosynthesis_chain() -> str:
    h, c, e = 6.62607015e-34, 2.99792458e8, 1.602176634e-19
    photon_ev = h * c / (680e-9) / e
    els = []
    els.extend(
        header(
            "光合作用没有把光先“烧成热”：它抢的是光子的电子",
            "680 nm 的红光约 1.82 eV，刚好够把叶绿素电子顶到高能级。",
        )
    )

    els.append(card(20, 66, 720, 224))
    els.append(step_badge(38, 88, 1, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(56, 92, "从光子到糖：五站接力", size=11.8, color=INK, weight="700"))
    nodes = [
        (40, "① 捕光", "叶绿素吸光子", GREEN),
        (176, "② PSII", "水裂解放 O₂", ORANGE),
        (312, "③ 电子链", "泵 H⁺ 建梯度", BLUE),
        (448, "④ ATP/NADPH", "能量货币与还原力", PURPLE),
        (584, "⑤ Calvin 循环", "CO₂ 固定成糖", GREEN),
    ]
    for i, (x, title, note, color) in enumerate(nodes):
        els.append(f'<rect x="{x}" y="128" width="120" height="82" rx="8" fill="#f8fafc" stroke="{color}" stroke-width="1.4"/>')
        els.append(txt(x + 60, 154, title, size=10.8, color=color, anchor="middle", weight="700"))
        els.append(txt(x + 60, 180, note, size=9.6, color=BODY, anchor="middle"))
        els.append(txt(x + 60, 198, "能量 ↓", size=9.2, color=MUTED, anchor="middle"))
        if i < 4:
            els.append(_line(x + 122, 168, x + 172, 168, stroke=color, sw=2, marker="arr-orange"))
    els.append(txt(40, 250, "每放出 1 个 O₂ 至少需 8 个红光光子；合成 1 个葡萄糖约需 48 个。", size=10.6, color=INK, weight="600"))
    els.append(txt(40, 276, "短波光子多出的能量先在内转换中变成热，真正用于水裂解与固碳的只有“红光那份”。", size=10.2, color=SLATE))

    els.append(card(20, 306, 352, 182))
    els.append(step_badge(38, 328, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 332, "一个红光光子有多少钱？", size=11.6, color=INK, weight="700"))
    els.append(txt(38, 366, "E = hc / λ，λ = 680 nm", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 394, f"≈ {photon_ev:.2f} eV ≈ {photon_ev*1.602e-19:.2e} J", size=11.0, color=ORANGE, weight="700"))
    els.append(txt(38, 428, "不是“热”，而是精确的能量包：", size=10.4, color=BODY))
    els.append(txt(38, 456, "被色素吸收后把电子抬升到激发态。", size=10.4, color=BODY))

    els.append(card(388, 306, 352, 182))
    els.append(step_badge(406, 328, 3, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(424, 332, "效率为什么不高？", size=11.6, color=INK, weight="700"))
    els.append(txt(404, 366, "理论上限约 30%（按 48 个红光光子算）", size=10.4, color=BODY))
    els.append(txt(404, 394, "全光谱与实际生理成本折算后约 4.5%", size=10.4, color=BODY))
    els.append(txt(404, 422, "全球尺度常年低于 1%（常见估计 0.2% 左右）", size=10.4, color=BODY))
    els.append(txt(404, 456, "能量没丢：大多变成热散回环境。", size=10.6, color=BLUE, weight="700"))

    els.append(card(20, 504, 720, 44, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 532, "光合作用不是把光“加热”成化学能，而是用光子的能量重排电子，最终存进糖的化学键。", size=10.8, color=SLATE))

    return figure(
        558,
        "光合作用光能转化学能五站接力与效率图",
        "五站依次为叶绿素捕光、光系统II裂解放氧、电子传递链泵质子、生成ATP与NADPH、卡尔文循环固定二氧化碳；680纳米红光光子能量约1.82电子伏，每放出一个氧分子至少八个红光光子，合成一个葡萄糖约需48个，理论效率约30%而全球实际常低于1%。",
        els,
    )


@register(TOPIC, "能量概念：形式、守恒、地球收支、光热互转与光合作用能量链", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("energy-forms-map.svg", build_energy_forms),
        ("energy-conservation-erg.svg", build_conservation),
        ("earth-energy-budget.svg", build_earth_budget),
        ("light-heat-wien-shift.svg", build_light_and_heat),
        ("photosynthesis-energy-chain.svg", build_photosynthesis_chain),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
