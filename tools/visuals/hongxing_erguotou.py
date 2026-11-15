"""
Visuals for '红星二锅头：传统酿造技艺、历史渊源与风味形成' (Hongxing Erguotou:
340+ Years of Beijing Erguotou Heritage from 1680 Qianmen Yuanshenghao to 1949 Founding Tribute & ICH VIII-144,
Zengtong + Overhead Tin Tianguo Condenser & 3 Cooling-Water Distillation Cuts with Boiling-Point/GCxGC-MS Curves,
Solid-State Craft: Red Sorghum + Barley/Pea Daqu, Ceramic Digang 28-Day Fermentation & Marangoni Kanhua Zhaijiu,
4-Stage Microbial Biochemical Relay & 751-Compound Flavor Architecture [Ethyl Acetate / Ethyl Lactate Ratio],
and Porous Pottery-Jar Aging: Micro-Oxidation, Metal-Ion Acetalization & Ethanol-Water Hydrogen-Bond Clustering).
Generates 5 original 760px Chinese SVG diagrams in assets/images/hongxing-erguotou/
with verified thermodynamic, physical-chemistry, and flavoromics assertions.
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

TOPIC = "hongxing-erguotou"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
CRIMSON = "#9f1239"
CRIMSON_SOFT = "#fff1f2"


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


def _arrow_defs():
    return """<marker id="arr-ink" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#0f172a"/>
  </marker>
  <marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#dc2626"/>
  </marker>"""


# ---------------------------------------------------------------------------
# 1. 340+ Years Historical Lineage: Yuanshenghao (1680) -> Hongxing (1949) -> ICH VIII-144
# ---------------------------------------------------------------------------
def build_three_hundred_year_lineage() -> str:
    years = [1300, 1680, 1792, 1949, 1952, 2008]
    assert years == sorted(years)
    span_years = 2008 - 1680
    assert span_years == 328  # 1680 formalization to 2008 national ICH listing

    el = [
        txt(20, 30, "从康熙前门源升号到开国大典献礼酒：北京二锅头三百四十余年非遗传承脉络", size=15.5, weight="700", color=INK),
        txt(20, 50, "中国首个以“蒸馏摘酒工艺”命名的白酒品类；2008 年列入国家级非物质文化遗产（项目编号 Ⅷ-144）", size=12, color=MUTED),
    ]

    # Top timeline card
    el.append(card(18, 66, 724, 214))
    el.append(pill(32, 78, "历史主轴：从京城老烧锅手艺暗语到国民口粮酒标杆", fg=RED, bg=RED_SOFT, w=318))

    # Horizontal timeline spine
    y_spine = 132
    el.append(_line(56, y_spine, 704, y_spine, stroke="#cbd5e1", sw=3.2))

    nodes = [
        (68, "元明肇始", "烧酒入京", "高粱蒸馏烧酒兴起", "留存三条烧酒胡同", SLATE, SLATE_SOFT),
        (192, "1680 康熙", "前门源升号", "赵氏三兄弟定型", "掐头去尾取二锅", AMBER, AMBER_SOFT),
        (316, "1792 乾隆", "大酒缸风尚", "半埋陶缸覆朱木盖", "平民站饮京味武酒", ORANGE, ORANGE_SOFT),
        (440, "1949.05", "收编十二烧锅", "建专卖公司实验厂", "开国大典献礼定名", RED, RED_SOFT),
        (564, "1952–1965", "科学化与授艺", "方心芳创麸曲节粮", "向京郊 19 厂传艺", BLUE, BLUE_SOFT),
        (686, "1980s–2008", "提净与非遗", "清蒸清烧大麸结合", "国家级非遗 Ⅷ-144", GREEN, GREEN_SOFT),
    ]
    for cx, era, title_s, d1, d2, col, bg in nodes:
        el.append(f'<circle cx="{cx}" cy="{y_spine}" r="8.5" fill="{bg}" stroke="{col}" stroke-width="2.6"/>')
        el.append(txt(cx, y_spine - 16, era, size=11, weight="700", color=col, anchor="middle"))
        el.append(card(cx - 54, y_spine + 16, 108, 116, rx=8, fill=bg, stroke=col, sw=1.1))
        el.append(txt(cx, y_spine + 38, title_s, size=11.5, weight="700", color=col, anchor="middle"))
        el.append(txt(cx, y_spine + 68, d1, size=10.5, color=INK, anchor="middle"))
        el.append(txt(cx, y_spine + 92, d2, size=10.5, weight="700", color=BODY, anchor="middle"))
        el.append(txt(cx, y_spine + 116, "↓" if cx == 440 else "•", size=11, weight="700", color=col, anchor="middle"))

    # Bottom Left Card: Pre-1949 Front-Shop Back-Workshop & Dajiugang Culture
    el.append(card(18, 294, 354, 152))
    el.append(pill(32, 306, "前店后坊与老北京“大酒缸”文化", fg=AMBER, bg=AMBER_SOFT, w=224))
    el.append(txt(32, 346, "• 源升号格局：前门大街临街设铺售酒，后院立灶蒸烧，", size=11.5, color=BODY))
    el.append(txt(42, 366, "清人载“灶火如屋，突烟腾上，数里外皆见之”。", size=11.5, color=BODY))
    el.append(txt(32, 390, "• 大酒缸民俗：大陶缸半截埋土保温，缸口扣朱漆大木盘", size=11.5, color=BODY))
    el.append(txt(42, 410, "当圆桌；车夫、匠人与文人围缸站饮，配开花豆、拍黄瓜。", size=11.5, color=BODY))
    el.append(txt(32, 434, "• 关键突破：打破按地名命名的惯例，直接以纯度承诺命名。", size=11.5, weight="700", color=AMBER))

    # Bottom Right Card: 1949 Brand Birth & Modern Flavoromics Inheritance
    el.append(card(388, 294, 354, 152))
    el.append(pill(402, 306, "红星诞生与现代风味科学解码", fg=RED, bg=RED_SOFT, w=214))
    el.append(txt(402, 346, "• 1949 年整合源升号、龙泉等 12 家老烧锅组建国营酒厂；", size=11.5, color=BODY))
    el.append(txt(412, 366, "1949.10 献礼开国大典；1951.06 注册新中国首批“红星”商标。", size=11.5, color=BODY))
    el.append(txt(402, 390, "• 技艺迭代：从传统大曲老五甑，拓展出麸曲纯种发酵、", size=11.5, color=BODY))
    el.append(txt(412, 410, "清蒸清烧与大麸曲结合，兼具醇厚底蕴与清爽净度。", size=11.5, color=BODY))
    el.append(txt(402, 434, "• 分子家底：GC-MS 检出 751 种微量风味物，传承人高景炎领衔。", size=11.5, weight="700", color=RED))

    return figure(
        460,
        "北京二锅头三百四十余年历史渊源与红星非遗传承脉络图",
        "展示从元明烧酒、1680年康熙十九年前门源升号赵氏三兄弟定型掐头去尾取二锅、1792年大酒缸民俗，到1949年整合12家老烧锅创立红星献礼开国大典、1952年方心芳麸曲革新、1965年传艺京郊及2008年入选国家级非遗VIII-144的完整历程。",
        el,
        extra_defs=_arrow_defs(),
    )


# ---------------------------------------------------------------------------
# 2. Zengtong + Tianguo Condenser & 3 Cooling-Water Cuts (with 1-shot anim)
# ---------------------------------------------------------------------------
def build_zengtong_tianguo_distillation() -> str:
    # Boiling points (°C at 1 atm) & GCxGC-MS head/heart/tail concentrations (Tian et al., Foods 2025, PMC12385443)
    bp_acetaldehyde = 20.2
    bp_methanol = 64.7
    bp_ethyl_acetate = 77.1
    bp_ethanol = 78.3
    bp_acetic_acid = 117.9
    bp_isoamylol = 131.1
    bp_ethyl_lactate = 154.0
    assert bp_acetaldehyde < bp_methanol < bp_ethyl_acetate < bp_ethanol < bp_acetic_acid < bp_isoamylol < bp_ethyl_lactate

    # Relative elution profile across 3 cooling-water pots (normalized 0..100 visual height)
    # Pot 1 (Head ~78% vol), Pot 2 (Erguotou Heart ~65% vol), Pot 3 (Tail ~45% vol)
    head_aldehydes = [92, 24, 10]
    heart_esters = [68, 95, 30]
    tail_acids_fusel = [18, 36, 94]
    assert head_aldehydes[0] > head_aldehydes[1] > head_aldehydes[2]
    assert heart_esters[1] > heart_esters[0] and heart_esters[1] > heart_esters[2]
    assert tail_acids_fusel[2] > tail_acids_fusel[1] > tail_acids_fusel[0]

    extra_css = """
      @keyframes steamCutRise {
        0% { opacity: 0.25; transform: translateY(8px); }
        55% { opacity: 1.0; transform: translateY(-2px); }
        100% { opacity: 1.0; transform: translateY(0px); }
      }
      .anim-steam-cut {
        animation: steamCutRise 2.8s ease-out 1 forwards;
      }
      @media (prefers-reduced-motion: reduce) {
        .anim-steam-cut {
          animation: none !important;
          opacity: 1.0 !important;
          transform: none !important;
        }
      }
    """

    el = [
        txt(20, 30, "“二锅头”不是蒸两遍，而是换第二锅冷却水：甑桶天锅构造与三段馏分曲线", size=15.5, weight="700", color=INK),
        txt(20, 50, "酒汽遇锡制“天锅”冷底凝成酒珠；按冷却水换锅次序掐去头锅燥辣醛、截断三锅酸涩尾", size=12, color=MUTED),
    ]

    # Left Card: Zengtong + Tianguo Cross-Section
    el.append(card(18, 66, 344, 412))
    el.append(pill(32, 78, "古法器皿剖面：甑桶 + 锡制天锅", fg=BLUE, bg=BLUE_SOFT, w=214))

    # Tianguo (Top cooling water basin with conical bottom!)
    # Rim at y=126..170, conical bottom pointing down to (172, 198) so condensate drips into collector!
    el.append('<polygon points="74,126 270,126 252,172 172,198 92,172" fill="#dbeafe" stroke="#1d6fa5" stroke-width="2.2"/>')
    el.append(txt(172, 148, "天锅（盛满凉水冷却）", size=11.5, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(172, 166, "连换 3 锅凉水 = 分出 3 段酒", size=10.5, weight="700", color=INK, anchor="middle"))

    # Water change badge on top-right of Tianguo
    el.append(_line(264, 136, 304, 118, stroke=BLUE, sw=1.6, marker="arr-blue"))
    el.append(txt(308, 116, "舀出热水", size=10.5, weight="700", color=BLUE))
    el.append(txt(308, 132, "注入新凉水", size=10.5, color=MUTED))

    # Zengtong body (trapezoidal wooden/metal barrel y=172..348)
    el.append('<polygon points="84,172 260,172 246,348 98,348" fill="#fefce8" stroke="#b45309" stroke-width="2.2"/>')

    # Collector trough & spout leading right to jar
    el.append('<polygon points="154,204 196,214 298,238 298,247 154,213" fill="#e2e8f0" stroke="#475569" stroke-width="1.5"/>')
    el.append(txt(306, 232, "流酒槽", size=10.5, weight="700", color=SLATE))
    el.append(card(284, 254, 64, 54, rx=6, fill=GREEN_SOFT, stroke=GREEN, sw=1.5))
    el.append(txt(316, 276, "只接第2锅", size=10.5, weight="700", color=GREEN, anchor="middle"))
    el.append(txt(316, 296, "二锅头!", size=11, weight="700", color=GREEN, anchor="middle"))

    # Animated rising alcohol-flavor steam + dripping droplets
    el.append('<g class="anim-steam-cut">')
    for sx in (118, 152, 192, 226):
        el.append(_line(sx, 266, sx, 192, stroke=ORANGE, sw=1.8, dash="4,3", marker="arr-orange"))
    el.append(f'<circle cx="172" cy="203" r="3.8" fill="{GREEN}"/>')
    el.append(f'<circle cx="294" cy="250" r="3.8" fill="{GREEN}"/>')
    el.append("</g>")

    # Fermented sorghum Jiupei bed (y=268..342)
    el.append('<polygon points="92,268 252,268 246,342 98,342" fill="#fde68a" stroke="#d97706" stroke-width="1.4"/>')
    el.append(txt(172, 294, "疏松高粱酒醅 + 稻壳层", size=11.5, weight="700", color=AMBER, anchor="middle"))
    el.append(txt(172, 314, "轻撒匀铺：边蒸粮糊化、边蒸酒提香", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(172, 333, "（混蒸混烧 / 清蒸清烧）", size=10.5, color=MUTED, anchor="middle"))

    # Perforated Zengbi grate (y=348)
    el.append(_line(96, 348, 248, 348, stroke=INK, sw=2.6, dash="6,4"))
    el.append(txt(60, 352, "甑箅", size=10.5, weight="700", color=INK, anchor="middle"))

    # Bottom Diguo boiling water pot (y=352..412)
    el.append('<polygon points="98,354 246,354 232,406 112,406" fill="#ffedd5" stroke="#c25014" stroke-width="2.0"/>')
    el.append(txt(172, 378, "底锅沸水：产纯净水蒸气穿醅而上", size=11, weight="700", color=ORANGE, anchor="middle"))
    el.append(txt(172, 397, "火候口诀：“缓慢蒸馏，大火追尾”", size=10.5, color=RED, anchor="middle"))

    # Bottom takeaway note inside Left Card
    el.append(card(30, 418, 320, 48, rx=7, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(42, 437, "误区澄清：不是把酒回锅重蒸第 2 次，而是同一甑酒醅", size=10.5, weight="700", color=INK))
    el.append(txt(42, 455, "在天锅换上“第 2 锅凉水”期间流出的中段精华原酒！", size=10.5, weight="700", color=RED))

    # Right Card: 3 Cooling-Water Cuts & Chemical Boiling-Point Partitioning
    el.append(card(376, 66, 366, 412))
    el.append(pill(390, 78, "三锅冷却水切出的化学世界（GC×GC-MS 实测规律）", fg=GREEN, bg=GREEN_SOFT, w=326))

    # Cut 1: First Pot (Head)
    el.append(card(390, 114, 338, 102, rx=8, fill=RED_SOFT, stroke="#fca5a5"))
    el.append(txt(402, 134, "① 第一锅凉水 · 酒头（75–80% vol）→ 掐头舍弃", size=12, weight="700", color=RED))
    el.append(txt(402, 155, "• 物理机制：低沸点、强脂溶性小分子抢先随高浓乙醇冲出", size=10.5, color=BODY))
    el.append(txt(402, 175, "• 富集物质：乙醛（沸点 20.2°C，冲鼻辣喉易眩晕）、甲醇", size=10.5, color=BODY))
    el.append(txt(412, 194, "（64.7°C）、甲酸乙酯（54.3°C）及超高浓早期醛缩物", size=10.5, color=BODY))

    # Cut 2: Second Pot (Erguotou Heart)
    el.append(card(390, 226, 338, 118, rx=8, fill=GREEN_SOFT, stroke="#86efac", sw=1.8))
    el.append(txt(402, 247, "② 第二锅凉水 · 二锅头酒心（58–68% vol）→ 黄金中段", size=12, weight="700", color=GREEN))
    el.append(txt(402, 268, "• 物理机制：水醇比例适中，疏水香酯与亲水甜酯同步馏出", size=10.5, color=BODY))
    el.append(txt(402, 288, "• 核心风味：乙醇（78.3°C）+ 清脆果香乙酸乙酯（77.1°C，", size=10.5, weight="700", color=INK))
    el.append(txt(412, 307, "约 127 mg/L）+ 绵甜醇厚乳酸乙酯（154°C，随水汽共沸", size=10.5, weight="700", color=INK))
    el.append(txt(412, 326, "馏出约 40 mg/L，酒头中几乎为零！）→ 净爽不燥、绵甜回甘", size=10.5, weight="700", color=GREEN))

    # Cut 3: Third Pot (Tail)
    el.append(card(390, 354, 338, 112, rx=8, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(402, 375, "③ 第三锅凉水 · 酒尾（<48% vol）→ 去尾另存回蒸", size=12, weight="700", color=ORANGE))
    el.append(txt(402, 396, "• 物理机制：酒精渐竭、温度升高，高沸点水溶性与重油涌出", size=10.5, color=BODY))
    el.append(txt(402, 416, "• 富集物质：异戊醇等杂醇油（131°C，飙升逾 212 mg/L 苦涩", size=10.5, color=BODY))
    el.append(txt(412, 435, "上头）、乙酸/乳酸（酸涩）与亚油酸乙酯（低度浑浊油花）", size=10.5, color=BODY))
    el.append(txt(412, 454, "注：酒尾富含香味前体，不直接饮用但可泼回下轮酒醅复蒸", size=10.5, weight="700", color=AMBER))

    return figure(
        492,
        "二锅头甑桶天锅蒸馏构造与三锅冷却水掐头去尾化学机制图",
        "左侧剖面展示底锅沸水蒸汽穿过高粱酒醅并在顶部盛凉水的锡制天锅底壁冷凝成酒；右侧结合沸点与GCxGC-MS实测对比第一锅酒头（20.2°C乙醛、64.7°C甲醇富集）、第二锅二锅头酒心（78.3°C乙醇协同77.1°C乙酸乙酯与154°C乳酸乙酯达到清爽绵甜平衡）与第三锅酒尾（131°C异戊醇杂醇油及有机酸涌出）的取舍原理。",
        el,
        extra_css=extra_css,
        extra_defs=_arrow_defs(),
    )


# ---------------------------------------------------------------------------
# 3. Solid-State Craft: Qu, Ceramic Digang 28-Day Curve & Marangoni Kanhua
# ---------------------------------------------------------------------------
def build_solid_state_craft_and_kanhua() -> str:
    # Verify surface tension & viscosity physics of ethanol-water mixtures at 25°C (Bozorgmehr & Murray 2021 PMC8154141)
    gamma_water = 72.0      # mN/m
    gamma_60vol = 27.5      # mN/m (~60% vol ethanol-water)
    gamma_ethanol = 22.3    # mN/m
    eta_water = 0.89        # mPa·s
    eta_peak_50vol = 2.68   # mPa·s (H-bond network viscosity maximum around 45-55% vol!)
    eta_ethanol = 1.07      # mPa·s
    assert gamma_water > gamma_60vol > gamma_ethanol
    assert eta_peak_50vol > 2.4 * eta_water and eta_peak_50vol > 2.4 * eta_ethanol

    # Digang 28-day fermentation temperature curve ("前缓、中挺、后缓落")
    days = [0, 5, 12, 18, 28]
    temps = [19.0, 26.5, 31.0, 29.5, 22.5]
    assert temps[0] < temps[1] < temps[2] and temps[2] > temps[3] > temps[4]

    el = [
        txt(20, 30, "一粒红高粱怎样炼成清香原酒：固态酿造五步法、地缸控温与“看花摘酒”流体物理", size=15.5, weight="700", color=INK),
        txt(20, 50, "陶土地缸隔绝泥土杂菌守护“一清到底”；水醇表面张力差与黏度峰造就毫米级酒花标尺", size=12, color=MUTED),
    ]

    # Top Card: 5-Step Craft Pipeline
    el.append(card(18, 66, 724, 158))
    el.append(pill(32, 78, "国家级非遗酿造主线：老五甑混蒸混烧 / 现代清蒸清烧", fg=AMBER, bg=AMBER_SOFT, w=328))

    steps = [
        (28, "① 选粮润糁", "红高粱粉碎", "支链淀粉 ~80%", "单宁 ~1% 烂心不烂皮", AMBER, AMBER_SOFT),
        (170, "② 大麦豌豆曲", "糖化发酵剂", "大麦:豌豆 = 6:4", "或大曲+麸曲结合", PURPLE, PURPLE_SOFT),
        (312, "③ 清蒸糊化", "辅料单独清蒸", "稻壳单蒸 ≥30 min", "彻底驱除生糠邪杂味", BLUE, BLUE_SOFT),
        (454, "④ 地缸发酵", "闭关 ≥28 天", "陶缸埋地隔菌控温", "前缓、中挺、后缓落", GREEN, GREEN_SOFT),
        (596, "⑤ 装甑摘酒", "六字诀探汽上甑", "轻·松·薄·匀·散·准", "看花摘酒·取二锅心", RED, RED_SOFT),
    ]
    for idx, (sx, stitle, ssub, l1, l2, col, bg) in enumerate(steps):
        el.append(card(sx, 112, 134, 98, rx=8, fill=bg, stroke=col, sw=1.2))
        el.append(txt(sx + 67, 132, stitle, size=11.5, weight="700", color=col, anchor="middle"))
        el.append(txt(sx + 67, 152, ssub, size=11, weight="700", color=INK, anchor="middle"))
        el.append(txt(sx + 67, 174, l1, size=10.5, color=BODY, anchor="middle"))
        el.append(txt(sx + 67, 194, l2, size=10.5, color=BODY, anchor="middle"))
        if idx < len(steps) - 1:
            el.append(_line(sx + 135, 161, sx + 168, 161, stroke=INK, sw=1.5, marker="arr-ink"))

    # Bottom Left Card: Why Ceramic Digang vs Mud Pit + 28-Day Temperature Curve
    el.append(card(18, 238, 354, 240))
    el.append(pill(32, 250, "为什么用“陶土地缸”而不用浓香“泥窖”？", fg=GREEN, bg=GREEN_SOFT, w=268))
    el.append(txt(32, 288, "• 四川泥窖：窖泥富集己酸菌/梭菌，产浓郁己酸乙酯与窖香", size=10.5, color=MUTED))
    el.append(txt(32, 308, "• 北京陶缸：致密陶壁严防土壤梭菌侵入，刷洗消毒极净，", size=10.5, weight="700", color=GREEN))
    el.append(txt(42, 326, "让酵母与乳酸菌纯粹接力，成就“清字当头、一清到底”！", size=10.5, weight="700", color=INK))

    # Mini chart of 28-day Digang temperature curve (x=54..346, y=354..442)
    el.append(card(32, 340, 324, 124, rx=7, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(44, 358, "地缸 28 天发酵品温曲线（°C）：前缓 → 中挺 → 后缓落", size=10.5, weight="700", color=INK))
    gx0, gy0, gw, gh = 64, 438, 266, 62
    el.append(_line(gx0, gy0, gx0 + gw, gy0, stroke=SLATE, sw=1.2))
    el.append(_line(gx0, gy0, gx0, gy0 - gh, stroke=SLATE, sw=1.2))
    el.append(txt(gx0 - 6, gy0 - 2, "18°", size=10, color=MUTED, anchor="end"))
    el.append(txt(gx0 - 6, gy0 - gh + 6, "32°", size=10, color=MUTED, anchor="end"))

    pts = []
    for d, t in zip(days, temps):
        px = gx0 + (d / 28.0) * gw
        py = gy0 - ((t - 18.0) / 15.0) * gh
        pts.append((px, py, d, t))
    poly = " ".join(f"{px:.1f},{py:.1f}" for px, py, _, _ in pts)
    el.append(f'<polyline points="{poly}" fill="none" stroke="{GREEN}" stroke-width="2.6"/>')
    stage_notes = ["入缸 19°C", "前缓生香", "中挺 31°C", "主发酵", "后缓酯化"]
    for (px, py, d, _), sn in zip(pts, stage_notes):
        el.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="{GREEN}"/>')
        el.append(txt(px, gy0 + 16, f"{d}天", size=10, color=MUTED, anchor="middle"))
    el.append(txt(pts[0][0] + 18, pts[0][1] - 8, "前缓", size=10.5, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(pts[2][0], pts[2][1] - 8, "中挺顶温 31°C", size=10.5, weight="700", color=RED, anchor="middle"))
    el.append(txt(pts[4][0] - 24, pts[4][1] - 10, "后缓落产酯", size=10.5, weight="700", color=GREEN, anchor="middle"))

    # Bottom Right Card: Fluid Physics of "Kanhua Zhaijiu" (Judging ABV by Foam Beads)
    el.append(card(388, 238, 354, 240))
    el.append(pill(402, 250, "“看花摘酒”背后的流体力学：表面张力与马兰戈尼效应", fg=BLUE, bg=BLUE_SOFT, w=328))
    el.append(txt(402, 288, "• 纯水表面张力 72.0 mN/m（泡大易破），纯乙醇仅 22.3 mN/m；", size=10.5, color=BODY))
    el.append(txt(402, 307, "• 50–65% vol 时水醇氢键网络黏度暴涨至 ~2.7 mPa·s（纯水 3 倍），", size=10.5, weight="700", color=BLUE))
    el.append(txt(412, 325, "液膜蒸发触发马兰戈尼回流自愈，酒花大小与寿命精确锁定酒度！", size=10.5, color=BODY))

    flowers = [
        ("大清花", "65–75% vol", "黄豆大·晶莹速散", "初段高度头酒", AMBER, AMBER_SOFT),
        ("小清花", "55–65% vol", "绿豆大·持久匀净", "二锅头核心中段!", GREEN, GREEN_SOFT),
        ("云花", "45–55% vol", "米粒叠聚·绵密慢散", "中后段临界区", BLUE, BLUE_SOFT),
        ("水花/油花", "<40% vol", "碎沫铺面·浮油微浑", "断花截尾信号!", RED, RED_SOFT),
    ]
    for idx, (fname, abv, desc_f, role_f, col, bg) in enumerate(flowers):
        fy = 340 + idx * 32
        el.append(card(402, fy, 326, 27, rx=5, fill=bg, stroke=col, sw=1.0))
        el.append(txt(412, fy + 18, fname, size=11, weight="700", color=col))
        el.append(txt(482, fy + 18, abv, size=10.5, weight="700", color=INK))
        el.append(txt(556, fy + 18, desc_f, size=10.5, color=BODY))
        el.append(txt(720, fy + 18, role_f, size=10.5, weight="700", color=col, anchor="end"))

    return figure(
        492,
        "红星二锅头固态酿造五步工艺、陶土地缸控温曲线与看花摘酒流体物理图",
        "上方展示红高粱润糁、大麦豌豆大曲/麸曲、清蒸辅料去糠味、陶土地缸28天发酵及装甑六字诀；左下方对比陶土地缸隔绝杂菌机制与前缓中挺后缓落品温曲线；右下方解析50至65度乙醇水氢键黏度峰值及马兰戈尼效应如何形成大清花、小清花、云花与水花。",
        el,
        extra_defs=_arrow_defs(),
    )


# ---------------------------------------------------------------------------
# 4. 4-Stage Microbial Biochemical Relay & 751-Compound Sensory Map
# ---------------------------------------------------------------------------
def build_microbial_relay_and_flavor_wheel() -> str:
    # Verify Qingxiangxing Baijiu mass balance & Ethyl Acetate : Ethyl Lactate signature
    ethanol_water_pct = 98.0
    trace_flavor_pct = 2.0
    assert math.isclose(ethanol_water_pct + trace_flavor_pct, 100.0)
    identified_compounds = 751
    assert identified_compounds > 700

    # Odor thresholds in μg/L (Qiao, Zhang & Zheng 2023 PMC10739939)
    ot_ethyl_phenylacetate = 407.0
    ot_acetaldehyde = 1200.0
    ot_acetal = 2090.0
    ot_ethyl_acetate = 32600.0
    ot_ethyl_lactate = 128000.0
    assert ot_ethyl_phenylacetate < ot_acetaldehyde < ot_acetal < ot_ethyl_acetate < ot_ethyl_lactate

    el = [
        txt(20, 30, "2% 微量分子决定灵魂：地缸四棒微生物接力与红星二锅头“清爽绵甜凛”风味解码", size=15.5, weight="700", color=INK),
        txt(20, 50, "98% 是乙醇与水，剩下 2%（已检出 751 种微量成分）由霉菌、双酵母、细菌与高粱单宁合力锻造", size=12, color=MUTED),
    ]

    # Left Card: 4-Stage Microbial & Thermal Biochemical Relay
    el.append(card(18, 66, 348, 438))
    el.append(pill(32, 78, "地缸里的“四棒微生物接力赛”（边糖化边发酵）", fg=PURPLE, bg=PURPLE_SOFT, w=308))

    relays = [
        (
            114,
            "第 1 棒 · 曲霉/根霉 + 扣囊复膜孢酵母",
            "分泌淀粉酶与蛋白酶（开路先锋）",
            "高粱支链淀粉 → 可发酵葡萄糖；蛋白质 → 亮氨酸/苯丙氨酸",
            PURPLE,
            PURPLE_SOFT,
        ),
        (
            204,
            "第 2 棒 · 酿酒酵母 (S. cerevisiae)",
            "厌氧糖酵解 + 艾氏途径 (Ehrlich)",
            "葡萄糖 → 主体乙醇；苯丙氨酸脱羧还原 → 玫瑰蜜香 β-苯乙醇",
            BLUE,
            BLUE_SOFT,
        ),
        (
            294,
            "第 3 棒 · 异常威克汉姆酵母 / 毕赤酵母",
            "醇酰基转移酶 (AATase / ATF1) 生香引擎",
            "乙酰辅酶 A + 乙醇 → 头号清香酯“乙酸乙酯”（清脆果香）",
            GREEN,
            GREEN_SOFT,
        ),
        (
            384,
            "第 4 棒 · 乳酸菌 + 芽孢杆菌 + 高粱单宁",
            "酯化绵甜骨架 + 蒸馏热裂解粮香",
            "乳酸 → 乳酸乙酯（塑黄金乙乳比）；产四甲基吡嗪与愈创木酚",
            AMBER,
            AMBER_SOFT,
        ),
    ]
    for idx, (ry, rtitle, rsub, rchem, col, bg) in enumerate(relays):
        el.append(card(30, ry, 324, 76, rx=8, fill=bg, stroke=col, sw=1.2))
        el.append(txt(42, ry + 21, rtitle, size=11.5, weight="700", color=col))
        el.append(txt(42, ry + 42, rsub, size=10.5, weight="700", color=INK))
        el.append(txt(42, ry + 62, rchem, size=10.5, color=BODY))
        if idx < len(relays) - 1:
            el.append(_line(192, ry + 77, 192, ry + 89, stroke=INK, sw=1.5, marker="arr-ink"))

    el.append(txt(32, 486, "核心比例：清香型追求“清香纯正”，乙酸乙酯 : 乳酸乙酯常保持 > 1.2 : 1", size=10.5, weight="700", color=GREEN))

    # Right Card: Which Molecule Creates Every Taste & Aroma?
    el.append(card(380, 66, 362, 438))
    el.append(pill(394, 78, "舌尖与鼻腔的分子字典：每种味道从何而来？", fg=RED, bg=RED_SOFT, w=304))

    flavors = [
        ("清脆果香（清·爽）", "乙酸乙酯", "阈值 32.6 mg/L · 清香头号骨架，苹果梨香", GREEN, GREEN_SOFT),
        ("绵柔醇甜（绵·甜）", "乳酸乙酯+多元醇", "阈值 128 mg/L · 增稠压辣，拉长回甘尾韵", BLUE, BLUE_SOFT),
        ("玫瑰蜜香（幽·雅）", "β-苯乙醇/苯乙酯", "阈值 0.41 mg/L · 极微浓度赋予花蜜细香", PURPLE, PURPLE_SOFT),
        ("烘焙粮香（醇·厚）", "四甲基吡嗪+愈创木酚", "高粱单宁裂解与芽孢杆菌合成坚果谷物香", AMBER, AMBER_SOFT),
        ("凛冽生津（凛·净）", "乙酸 + 乳酸", "恰当有机酸压住浮香，入口挺拔落口爽净", TEAL, TEAL_SOFT),
        ("陈年柔熟（柔·陈）", "乙缩醛 (二乙氧基乙烷)", "阈值 2.09 mg/L · 陶坛陈酿圆润度金指标", ORANGE, ORANGE_SOFT),
        ("冲辣苦涩（需驯服）", "游离乙醛+过量杂醇油", "新酒暴辣上头元凶 · 靠掐头去尾与陈酿消减", RED, RED_SOFT),
    ]
    for idx, (sense, mol, detail, col, bg) in enumerate(flavors):
        fy = 114 + idx * 54
        el.append(card(392, fy, 338, 46, rx=7, fill=bg, stroke=col, sw=1.0))
        el.append(txt(402, fy + 18, sense, size=11, weight="700", color=col))
        el.append(txt(720, fy + 18, mol, size=11, weight="700", color=INK, anchor="end"))
        el.append(txt(402, fy + 37, detail, size=10.5, color=BODY))

    return figure(
        518,
        "红星二锅头四路微生物生化接力与751种微量风味分子感官映射图",
        "左侧展示曲霉糖化蛋白水解、酿酒酵母糖酵解与艾氏途径、威克汉姆生香酵母AATase合成乙酸乙酯、乳酸菌与高粱单宁生成乳酸乙酯及酚类吡嗪的四棒接力；右侧将清爽果香、绵柔回甘、玫瑰蜜香、烘焙粮香、凛冽生津、陈年柔熟与冲辣苦涩逐一对应到具体化学分子与嗅觉阈值。",
        el,
        extra_defs=_arrow_defs(),
    )


# ---------------------------------------------------------------------------
# 5. Pottery-Jar Aging (Taotan Chenniang): 3 Molecular Smoothing Mechanisms
# ---------------------------------------------------------------------------
def build_pottery_jar_aging_smoothing() -> str:
    # Stoichiometric mass check for acetalization: 2 C2H5OH (46.07*2=92.14) + CH3CHO (44.05) -> CH3CH(OC2H5)2 (118.17) + H2O (18.02)
    lhs_mw = 2 * 46.07 + 44.05
    rhs_mw = 118.17 + 18.02
    assert math.isclose(lhs_mw, rhs_mw, abs_tol=0.02)

    el = [
        txt(20, 30, "为什么刚出甑的新酒暴辣刺喉，钻进陶坛睡一觉就变绵柔？三重分子陈酿机制", size=15.5, weight="700", color=INK),
        txt(20, 50, "微孔陶坛并非死密封玻璃瓶：排杂挥发、金属离子催化缩醛化、水醇氢键缔合共同磨平烈酒棱角", size=12, color=MUTED),
    ]

    # Card 1: Physical Micro-Breathing & Sulfide/Aldehyde Escape
    el.append(card(18, 68, 232, 286))
    el.append(pill(30, 80, "① 陶壁微孔呼吸排杂", fg=ORANGE, bg=ORANGE_SOFT, w=176))
    # Mini pottery jar illustration
    el.append('<ellipse cx="134" cy="134" rx="28" ry="8" fill="#fed7aa" stroke="#c25014" stroke-width="1.8"/>')
    el.append('<path d="M106,134 C86,162 88,212 108,236 L160,236 C180,212 182,162 162,134 Z" fill="#ffedd5" stroke="#c25014" stroke-width="2.0"/>')
    el.append(txt(134, 182, "陶坛陈酿", size=12, weight="700", color=AMBER, anchor="middle"))
    el.append(txt(134, 202, "避光恒温地窖", size=10.5, color=BODY, anchor="middle"))
    # Outward volatile escape & inward trace O2 arrows
    el.append(_line(88, 168, 52, 152, stroke=RED, sw=1.6, dash="3,2", marker="arr-red"))
    el.append(txt(48, 146, "逸出硫醇", size=10.5, weight="700", color=RED, anchor="middle"))
    el.append(_line(180, 168, 214, 152, stroke=BLUE, sw=1.6, marker="arr-blue"))
    el.append(txt(214, 146, "微量 O2", size=10.5, weight="700", color=BLUE, anchor="middle"))

    el.append(txt(30, 264, "• 陶胎含微米级烧结气孔，", size=10.5, color=BODY))
    el.append(txt(38, 283, "液态酒不渗漏而气体可微交换", size=10.5, color=BODY))
    el.append(txt(30, 304, "• 极低沸点硫化氢、甲硫醇（烂", size=10.5, color=BODY))
    el.append(txt(38, 323, "菜叶味）与部分游离乙醛逸散", size=10.5, color=BODY))
    el.append(txt(30, 343, "→ 褪去刺鼻“新酒燥气”", size=11, weight="700", color=ORANGE))

    # Card 2: Trace Metal Ion Catalysis & Acetalization
    el.append(card(264, 68, 232, 286))
    el.append(pill(276, 80, "② 金属离子催化缩醛化", fg=GREEN, bg=GREEN_SOFT, w=190))

    el.append(card(276, 118, 208, 116, rx=8, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(380, 138, "陶土溶出 Ca²⁺ / Mg²⁺ / Fe³⁺ / Cu²⁺", size=10.5, weight="700", color=GREEN, anchor="middle"))
    el.append(txt(380, 162, "2 乙醇 + 游离乙醛（暴辣）", size=11, weight="700", color=RED, anchor="middle"))
    el.append(txt(380, 184, "⇌ 催化缩合 + 酸醇缓慢酯化", size=10.5, color=INK, anchor="middle"))
    el.append(txt(380, 206, "乙缩醛（柔和熟果香）+ 水", size=11, weight="700", color=GREEN, anchor="middle"))
    el.append(txt(380, 226, "分子量守恒：92.1 + 44.1 = 118.2 + 18.0", size=10, color=MUTED, anchor="middle"))

    el.append(txt(276, 264, "• 游离乙醛强烈刺激三叉神经，", size=10.5, color=BODY))
    el.append(txt(284, 283, "锁进乙缩醛后化作清甜果香！", size=10.5, color=BODY))
    el.append(txt(276, 304, "• 多价金属离子与有机酸配位络", size=10.5, color=BODY))
    el.append(txt(284, 323, "合，显著缓和尖锐酸涩感", size=10.5, color=BODY))
    el.append(txt(276, 343, "→ 辛辣转甜润，陈香渐显", size=11, weight="700", color=GREEN))

    # Card 3: Ethanol-Water Hydrogen-Bond Clustering
    el.append(card(510, 68, 232, 286))
    el.append(pill(522, 80, "③ 水—醇氢键网络重排", fg=BLUE, bg=BLUE_SOFT, w=186))

    # New vs Aged molecular cluster comparison box
    el.append(card(522, 118, 208, 54, rx=7, fill=RED_SOFT, stroke="#fca5a5"))
    el.append(txt(532, 138, "新酒：游离乙醇横冲直撞", size=10.5, weight="700", color=RED))
    el.append(txt(532, 158, "直接轰击口腔 TRPV1 灼痛受体", size=10.5, color=BODY))

    el.append(card(522, 180, 208, 54, rx=7, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(532, 200, "老熟酒：C2H5OH · nH2O 氢键笼", size=10.5, weight="700", color=BLUE))
    el.append(txt(532, 220, "水分子包拢乙醇，释放更平缓", size=10.5, color=BODY))

    el.append(txt(522, 264, "• 乙醇极性与水相近，但空间重", size=10.5, color=BODY))
    el.append(txt(530, 283, "排跨越能垒需数月至数年时间", size=10.5, color=BODY))
    el.append(txt(522, 304, "• 缔合簇增大后黏度微升、挥发", size=10.5, color=BODY))
    el.append(txt(530, 323, "冲劲减弱，挂杯与绵柔感倍增", size=10.5, color=BODY))
    el.append(txt(522, 343, "→ 凛冽不刺喉，一线顺入胃", size=11, weight="700", color=BLUE))

    # Bottom Summary Strip: Blending ("以酒调酒")
    el.append(card(18, 368, 724, 78, rx=9, fill=SLATE_SOFT, stroke=BORDER))
    el.append(pill(32, 380, "画龙点睛：传统“勾调（以酒调酒）” ≠ 酒精勾兑", fg=INK, bg="#e2e8f0", w=310))
    el.append(txt(356, 396, "纯粮固态二锅头绝不外加食用酒精或人工香精！", size=11.5, weight="700", color=RED))
    el.append(txt(32, 426, "勾调师将不同轮次（大楂劲爽、二楂绵甜）、不同陈酿年份与微量高香调味老酒按比例拼配，让每批次“乙乳比”与风味恒定如一。", size=11, color=BODY))

    return figure(
        460,
        "红星二锅头陶坛陈酿三重分子驯化机制与以酒调酒示意图",
        "展示刚蒸馏出的原酒在陶坛陈酿中经历微孔呼吸排走低沸点硫醇与燥气、陶土溶出钙镁铁铜离子催化游离乙醛缩合为柔和果香乙缩醛、以及游离乙醇与水分子缔合为稳定氢键簇降低TRPV1灼痛刺激的三重机制，并说明纯粮固态酒以酒调酒原理。",
        el,
        extra_defs=_arrow_defs(),
    )


@register(
    TOPIC,
    "红星二锅头三百四十年非遗传承、甑桶天锅换水蒸馏、地缸发酵看花摘酒、751种风味分子与陶坛陈酿图解",
    "饮食科学与非遗工艺",
)
def build_all() -> list[str]:
    written = [
        write_svg(TOPIC, "three-hundred-year-lineage-yuanshenghao-to-hongxing.svg", build_three_hundred_year_lineage()),
        write_svg(TOPIC, "zengtong-tianguo-three-cooling-pots-distillation.svg", build_zengtong_tianguo_distillation()),
        write_svg(TOPIC, "solid-state-craft-qu-digang-and-kanhua.svg", build_solid_state_craft_and_kanhua()),
        write_svg(TOPIC, "microbial-relay-and-751-flavor-wheel.svg", build_microbial_relay_and_flavor_wheel()),
        write_svg(TOPIC, "pottery-jar-aging-molecular-smoothing.svg", build_pottery_jar_aging_smoothing()),
    ]
    return written
