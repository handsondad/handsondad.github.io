"""Quantitative & step-by-step SVG visuals for Bacteria vs. Viruses blog post.

Generates 5 verified 760x520 figures under assets/images/bacteria-vs-virus/:
1. microbial-size-and-filter-scale.svg
2. anatomy-factory-vs-usb.svg
3. replication-fission-vs-hijack-anim.svg (1-shot CSS animation + reduced-motion fallback)
4. antibiotic-vs-antiviral-targets.svg
5. bacteria-vs-virus-master-card.svg
"""

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
    WIDTH,
    card,
    figure,
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "bacteria-vs-virus"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"


def _log_x(nm, x0=56.0, x1=704.0, lo_exp=1.0, hi_exp=5.0):
    """Map size in nm across 10^1 nm (10 nm) .. 10^5 nm (100 um) onto [x0, x1]."""
    val = math.log10(nm)
    assert lo_exp <= val <= hi_exp, f"{nm} nm outside log scale!"
    return x0 + (val - lo_exp) / (hi_exp - lo_exp) * (x1 - x0)


def build_size_and_filter_scale():
    """Fig 1: Logarithmic size scale (10 nm to 100 um) + 1892 Chamberland filter experiment."""
    # Quantitative sanity assertions
    x_10 = _log_x(10)
    x_30 = _log_x(30)        # Rhinovirus / Poliovirus ~30 nm
    x_100 = _log_x(100)      # Chamberland pore ~100 nm; Flu / Coronavirus ~100 nm
    x_200 = _log_x(200)      # Optical limit ~200 nm; T4 phage ~200 nm
    x_1000 = _log_x(1000)    # Pandoravirus ~1000 nm / Staph coccus ~1000 nm
    x_2000 = _log_x(2000)    # E. coli length ~2000 nm (2 um)
    x_8000 = _log_x(8000)    # Human RBC ~8000 nm (8 um)
    x_100k = _log_x(100000)  # Naked-eye threshold ~100 um (hair diameter)
    assert x_10 < x_30 < x_100 < x_200 < x_1000 < x_2000 < x_8000 < x_100k

    el = []
    el.extend(
        header(
            "差出十到一百倍的微观比例尺：从纳米病毒、微米细菌到瓷滤器百年悬案",
            "上方对数坐标轴（每格差 10 倍）对比真实尺寸与光学极限；下方还原 1892 年伊万诺夫斯基瓷滤器实验",
        )
    )

    # Top Panel: Log scale ruler (y=64..286)
    el.append(card(20, 64, 720, 222))
    el.append(pill(34, 74, "① 对数尺度全景（1 μm = 1,000 nm，注意横轴每跨一格放大 10 倍）", fg=BLUE, bg=BLUE_SOFT, w=456))

    # Shaded visibility zones
    el.append(
        f'<rect x="{x_10:.1f}" y="106" width="{x_200 - x_10:.1f}" height="106" rx="6" '
        f'fill="{PURPLE_SOFT}" opacity="0.55"/>'
    )
    el.append(
        f'<rect x="{x_200:.1f}" y="106" width="{x_100k - x_200:.1f}" height="106" rx="6" '
        f'fill="{GREEN_SOFT}" opacity="0.50"/>'
    )
    el.append(txt((x_10 + x_200) / 2, 122, "仅电子显微镜可见区（<200 nm）", size=11.5, color=PURPLE, anchor="middle", weight="600"))
    el.append(txt((x_200 + x_100k) / 2, 122, "普通光学显微镜可见区（≥200 nm，含绝大多数细菌与真核细胞）", size=11.5, color=GREEN, anchor="middle", weight="600"))

    # Axis line at y=212
    axis_y = 212
    el.append(f'<line x1="{x_10:.1f}" y1="{axis_y}" x2="{x_100k:.1f}" y2="{axis_y}" stroke="{INK}" stroke-width="2"/>')
    ticks = [
        (10, "10 nm"),
        (100, "100 nm"),
        (1000, "1 μm (1,000 nm)"),
        (10000, "10 μm"),
        (100000, "100 μm（肉眼极限）"),
    ]
    for nm, lab in ticks:
        tx = _log_x(nm)
        el.append(f'<line x1="{tx:.1f}" y1="{axis_y - 6}" x2="{tx:.1f}" y2="{axis_y + 6}" stroke="{INK}" stroke-width="1.8"/>')
        anc = "end" if nm == 100000 else ("start" if nm == 10 else "middle")
        dx = 6 if nm == 100000 else (-4 if nm == 10 else 0)
        el.append(txt(tx + dx, axis_y + 21, lab, size=11, color=SLATE, anchor=anc, weight="600"))

    # Cutoff dashed vertical lines
    el.append(f'<line x1="{x_100:.1f}" y1="106" x2="{x_100:.1f}" y2="{axis_y}" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    el.append(f'<line x1="{x_200:.1f}" y1="106" x2="{x_200:.1f}" y2="{axis_y}" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 3"/>')

    # Specimens plotted at exact log positions with staggered non-overlapping callouts
    # 1) Rhinovirus 30 nm
    el.append(f'<circle cx="{x_30:.1f}" cy="192" r="4.5" fill="{PURPLE}"/>')
    el.append(f'<line x1="{x_30:.1f}" y1="154" x2="{x_30:.1f}" y2="186" stroke="{PURPLE}" stroke-width="1.2"/>')
    el.append(txt(x_30, 148, "鼻病毒 30 nm", size=11.5, color=PURPLE, anchor="middle", weight="600", halo=True))

    # 2) Flu / Coronavirus 100 nm
    el.append(f'<circle cx="{x_100:.1f}" cy="190" r="6.5" fill="{PURPLE}" stroke="#fff" stroke-width="1.2"/>')
    el.append(f'<line x1="{x_100:.1f}" y1="172" x2="{x_100:.1f}" y2="183" stroke="{PURPLE}" stroke-width="1.2"/>')
    el.append(txt(x_100, 167, "流感/新冠 ~100 nm", size=11.5, color=PURPLE, anchor="middle", weight="600", halo=True))

    # 3) T4 Phage 200 nm (optical limit)
    el.append(f'<polygon points="{x_200:.1f},181 {x_200+6:.1f},189 {x_200:.1f},197 {x_200-6:.1f},189" fill="{BLUE}"/>')
    el.append(f'<line x1="{x_200:.1f}" y1="146" x2="{x_200:.1f}" y2="179" stroke="{BLUE}" stroke-width="1.2"/>')
    el.append(txt(x_200, 141, "T4噬菌体 200 nm（光学极限）", size=11.2, color=BLUE, anchor="middle", weight="600", halo=True))

    # 4) Overlap zone: Pandoravirus / Mycoplasma ~1000 nm
    el.append(f'<ellipse cx="{x_1000:.1f}" cy="190" rx="8" ry="5.5" fill="{ORANGE}" stroke="#fff" stroke-width="1"/>')
    el.append(f'<line x1="{x_1000:.1f}" y1="172" x2="{x_1000:.1f}" y2="183" stroke="{ORANGE}" stroke-width="1.2"/>')
    el.append(txt(x_1000 - 6, 167, "潘多拉巨型病毒 ~1 μm", size=11.5, color=ORANGE, anchor="middle", weight="600", halo=True))

    # 5) E. coli 2 um
    el.append(f'<rect x="{x_2000 - 11:.1f}" y="183" width="22" height="12" rx="6" fill="{GREEN}"/>')
    el.append(f'<line x1="{x_2000:.1f}" y1="146" x2="{x_2000:.1f}" y2="181" stroke="{GREEN}" stroke-width="1.2"/>')
    el.append(txt(x_2000 + 28, 141, "大肠杆菌 ~2 μm", size=11.5, color=GREEN, anchor="middle", weight="700", halo=True))

    # 6) Red blood cell 8 um
    el.append(f'<circle cx="{x_8000:.1f}" cy="187" r="11" fill="{RED_SOFT}" stroke="{RED}" stroke-width="2.2"/>')
    el.append(f'<circle cx="{x_8000:.1f}" cy="187" r="4" fill="none" stroke="{RED}" stroke-width="1" opacity="0.6"/>')
    el.append(f'<line x1="{x_8000:.1f}" y1="168" x2="{x_8000:.1f}" y2="175" stroke="{RED}" stroke-width="1.2"/>')
    el.append(txt(x_8000 + 16, 165, "红细胞 ~8 μm", size=11.5, color=RED, anchor="start", weight="700", halo=True))

    # Analogy + Outlier banner at bottom of Panel 1
    el.append(card(34, 242, 692, 34, rx=7, fill=SLATE_SOFT, stroke=HAIRLINE))
    el.append(
        txt(
            380,
            264,
            "直观比喻：红细胞若像篮球场，大肠杆菌就像场上的家用轿车，流感病毒像轮胎旁的足球！跨界异类：华丽硫珠菌长达 1 cm",
            size=11.5,
            color=BODY,
            anchor="middle",
            weight="600",
        )
    )

    # Bottom Panel: 1892 Chamberland Filter Detective Experiment + 1935 Crystallization (y=298..502)
    el.append(card(20, 298, 446, 204))
    el.append(pill(34, 308, "② 1892 瓷滤器破案：拦得住所有细菌，却拦不住“滤过性毒”", fg=ORANGE, bg=ORANGE_SOFT, w=380))

    # Funnel / Porcelain filter schematic
    el.append(card(42, 342, 126, 144, rx=8, fill="#fff7ed", stroke=ORANGE))
    el.append(txt(105, 360, "烟草病叶汁液", size=12, color=INK, anchor="middle", weight="700"))
    # Bacteria rods + Virus dots above filter
    el.append(f'<rect x="60" y="370" width="22" height="9" rx="4.5" fill="{GREEN}"/>')
    el.append(f'<rect x="116" y="372" width="22" height="9" rx="4.5" fill="{GREEN}"/>')
    for vx, vy in [(94, 374), (76, 386), (108, 385), (138, 386)]:
        el.append(f'<circle cx="{vx}" cy="{vy}" r="3.2" fill="{PURPLE}"/>')

    # Porcelain barrier (100 nm pores)
    el.append(f'<rect x="48" y="398" width="114" height="18" rx="3" fill="#fed7aa" stroke="{ORANGE}" stroke-width="1.4"/>')
    for px in [70, 94, 118, 142]:
        el.append(f'<line x1="{px}" y1="398" x2="{px}" y2="416" stroke="#ffffff" stroke-width="2.6"/>')
    el.append(txt(105, 411, "100 nm 素烧瓷板", size=10.8, color=INK, anchor="middle", weight="700"))

    # Filtrate below: only purple virus dots pass through!
    for vx, vy in [(72, 430), (96, 434), (120, 429), (140, 435), (86, 446), (114, 447)]:
        el.append(f'<circle cx="{vx}" cy="{vy}" r="3.2" fill="{PURPLE}"/>')
    el.append(txt(105, 468, "清澈滤液仍致病！", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(105, 482, "（仅纳米颗粒穿孔）", size=10.8, color=MUTED, anchor="middle"))

    # Two test outcomes on right side of left card
    el.append(card(184, 342, 268, 66, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(196, 362, "滤渣中的细菌（≥200 nm）：", size=12, color=GREEN, weight="700"))
    el.append(txt(196, 381, "• 被瓷孔死死卡住；涂在无细胞肉汤琼脂", size=11.2, color=BODY))
    el.append(txt(196, 398, "  平板上能自己吃糖长出肉眼可见菌落", size=11.2, color=BODY))

    el.append(card(184, 418, 268, 68, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(196, 438, "穿孔而过的烟草花叶病毒（TMV）：", size=12, color=PURPLE, weight="700"))
    el.append(txt(196, 457, "• 在肉汤琼脂上死寂一片（0 繁殖）！", size=11.2, color=BODY))
    el.append(txt(196, 474, "• 唯有擦回活烟草叶细胞内才疯狂扩增", size=11.2, color=BODY))

    # Bottom-Right Card: 1935 Stanley Crystallization & Core Criterion (y=298..502)
    el.append(card(480, 298, 260, 204))
    el.append(pill(494, 308, "③ 1935 结晶震撼与终极分界线", fg=PURPLE, bg=PURPLE_SOFT, w=224))
    # Crystal polygon illustration
    el.append(
        f'<polygon points="528,354 562,344 580,362 546,374" fill="#ede9fe" stroke="{PURPLE}" stroke-width="1.5"/>'
    )
    el.append(
        f'<polygon points="566,358 602,348 616,366 582,376" fill="#ddd6fe" stroke="{PURPLE}" stroke-width="1.5"/>'
    )
    el.append(txt(628, 358, "斯坦利提纯出", size=11.2, color=INK, weight="600"))
    el.append(txt(628, 374, "TMV 针状晶体", size=11.2, color=PURPLE, weight="700"))
    el.append(txt(494, 398, "像食盐一样装瓶结晶，兑水后仍能感染！", size=11.2, color=BODY))
    el.append(f'<line x1="494" y1="410" x2="726" y2="410" stroke="{BORDER}" stroke-width="1"/>')
    el.append(txt(494, 430, "无论个头多大，铁律只有一条：", size=11.8, color=INK, weight="700"))
    el.append(txt(494, 450, "• 细菌 = 活细胞（自带 70S 核糖体 + 产能）", size=11.2, color=GREEN, weight="600"))
    el.append(txt(494, 470, "• 病毒 = 非细胞（0 核糖体 + 0 独立代谢）", size=11.2, color=PURPLE, weight="600"))
    el.append(txt(494, 488, "  潘多拉病毒再大也是“巨型U盘”！", size=11, color=MUTED))

    svg = figure(
        520,
        "细菌与病毒的对数尺寸比例尺及1892年瓷滤器发现史图解",
        "对数坐标对比鼻病毒30纳米、流感新冠100纳米、T4噬菌体200纳米、潘多拉病毒1微米、大肠杆菌2微米与红细胞8微米，并展示1892年尚贝兰瓷滤器实验与1935年病毒结晶。",
        el,
    )
    write_svg(SUBDIR, "microbial-size-and-filter-scale.svg", svg)


def build_anatomy_factory_vs_usb():
    """Fig 2: Self-contained bacterial factory vs. viral capsid/envelope USB + alcohol/soap vulnerability."""
    el = []
    el.extend(
        header(
            "解剖台正面交锋：五脏俱全的“自给自足微缩工厂” vs 极简“劫持型代码胶囊”",
            "左侧细菌拥有双链DNA、70S核糖体与ATP发电膜；右侧病毒仅含核酸+蛋白壳（部分披脂质包膜），决定了消毒弱点",
        )
    )

    # Left Card: Bacterium Cutaway (x=20..374, y=64..358)
    el.append(card(20, 64, 354, 294))
    el.append(pill(34, 74, "细菌（原核活细胞）：全套生产线齐全", fg=GREEN, bg=GREEN_SOFT, w=274))

    # Capsule / Peptidoglycan Wall / Plasma Membrane nested rounded stadium
    el.append(f'<rect x="52" y="122" width="218" height="112" rx="56" fill="#dcfce7" stroke="{GREEN}" stroke-width="3"/>')
    el.append(f'<rect x="62" y="132" width="198" height="92" rx="46" fill="#fefce8" stroke="{AMBER}" stroke-width="2" stroke-dasharray="5 3"/>')
    el.append(f'<rect x="70" y="140" width="182" height="76" rx="38" fill="#ffffff" stroke="{TEAL}" stroke-width="1.5"/>')

    # Tangled circular dsDNA nucleoid in center
    el.append(
        f'<path d="M112,176 C122,154 152,156 160,176 C168,196 196,194 202,174 C206,158 176,152 154,170 C134,188 118,196 112,176 Z" '
        f'fill="none" stroke="{BLUE}" stroke-width="2.4"/>'
    )
    # Plasmid ring
    el.append(f'<circle cx="226" cy="178" r="11" fill="none" stroke="{ORANGE}" stroke-width="2.2"/>')
    # 70S Ribosome dots
    for rx, ry in [(92, 166), (98, 188), (138, 198), (182, 156), (206, 196), (168, 202)]:
        el.append(f'<circle cx="{rx}" cy="{ry}" r="3.3" fill="{PURPLE}"/>')

    # Flagellum tail on right of bacterium
    el.append(
        f'<path d="M270,178 Q292,158 310,178 T348,174" fill="none" stroke="{GREEN}" stroke-width="2.6" stroke-linecap="round"/>'
    )

    # Numbered callouts inside Left Card (clean non-overlapping rows below diagram)
    el.append(txt(92, 114, "肽聚糖细胞壁（抗渗透压盔甲）", size=11.2, color=GREEN, weight="600"))
    el.append(f'<line x1="146" y1="117" x2="146" y2="122" stroke="{GREEN}" stroke-width="1.2"/>')
    el.append(txt(314, 152, "旋转鞭毛马达", size=11.2, color=GREEN, anchor="middle", weight="600"))

    specs_b = [
        ("① 遗传主机：", "环状双链 DNA 拟核 + 可插拔质粒（常携耐药基因）", BLUE),
        ("② 蛋白打印：", "自带数万台 70S 核糖体（30S+50S），独立造酶", PURPLE),
        ("③ 能源电网：", "细胞膜质子泵自己合成 ATP，喝糖水就能活", AMBER),
        ("④ 生态真相：", "人体约 38 万亿细菌（≈1:1），99%以上无害或有益！", GREEN),
    ]
    for idx, (k, v, col) in enumerate(specs_b):
        yy = 256 + idx * 24
        el.append(txt(34, yy, k, size=11.5, color=col, weight="700"))
        el.append(txt(108, yy, v, size=11.2, color=BODY))

    # Right Card: Viruses Cutaway (x=386..740, y=64..358)
    el.append(card(386, 64, 354, 294))
    el.append(pill(400, 74, "病毒（非细胞寄生体）：核酸图纸 + 蛋白快递盒", fg=PURPLE, bg=PURPLE_SOFT, w=304))

    # Sub-diagram A: Enveloped Virus (cx=466, cy=168)
    cx1, cy1 = 466, 168
    el.append(f'<circle cx="{cx1}" cy="{cy1}" r="38" fill="#fff1f2" stroke="{ORANGE}" stroke-width="2.2" stroke-dasharray="5 3"/>')
    # Spikes around envelope
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        sx1, sy1 = cx1 + 38 * math.cos(rad), cy1 + 38 * math.sin(rad)
        sx2, sy2 = cx1 + 47 * math.cos(rad), cy1 + 47 * math.sin(rad)
        el.append(f'<line x1="{sx1:.1f}" y1="{sy1:.1f}" x2="{sx2:.1f}" y2="{sy2:.1f}" stroke="{ORANGE}" stroke-width="2.2"/>')
        el.append(f'<circle cx="{sx2:.1f}" cy="{sy2:.1f}" r="2.8" fill="{ORANGE}"/>')
    # Inner icosahedral hexagon + RNA wave
    pts1 = " ".join(
        f"{cx1 + 24 * math.cos(math.radians(a)):.1f},{cy1 + 24 * math.sin(math.radians(a)):.1f}"
        for a in range(30, 390, 60)
    )
    el.append(f'<polygon points="{pts1}" fill="#f3e8ff" stroke="{PURPLE}" stroke-width="2"/>')
    el.append(f'<path d="M{cx1-13},{cy1} Q{cx1-6},{cy1-9} {cx1},{cy1} T{cx1+13},{cy1}" fill="none" stroke="{RED}" stroke-width="2.2"/>')
    el.append(txt(cx1, 229, "有包膜病毒（流感/新冠）", size=11.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(cx1, 112, "脂质包膜+刺突", size=10.8, color=ORANGE, anchor="middle", weight="600"))

    # Sub-diagram B: Naked Virus (cx=592, cy=168)
    cx2, cy2 = 592, 168
    pts2 = " ".join(
        f"{cx2 + 30 * math.cos(math.radians(a)):.1f},{cy2 + 30 * math.sin(math.radians(a)):.1f}"
        for a in range(0, 360, 60)
    )
    el.append(f'<polygon points="{pts2}" fill="#e0f2fe" stroke="{BLUE}" stroke-width="2.4"/>')
    el.append(f'<path d="M{cx2-14},{cy2} Q{cx2-7},{cy2-10} {cx2},{cy2} T{cx2+14},{cy2}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
    el.append(txt(cx2, 229, "无包膜裸病毒（诺如）", size=11.2, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(cx2, 124, "纯蛋白二十面体壳", size=10.8, color=BLUE, anchor="middle", weight="600"))

    # Sub-diagram C: Phage silhouette (cx=692, cy=168)
    cx3 = 692
    el.append(f'<polygon points="{cx3},126 {cx3+16},136 {cx3+16},154 {cx3},164 {cx3-16},154 {cx3-16},136" fill="#ede9fe" stroke="{PURPLE}" stroke-width="2"/>')
    el.append(f'<rect x="{cx3-4}" y="164" width="8" height="26" fill="#ddd6fe" stroke="{PURPLE}" stroke-width="1.6"/>')
    for dx in (-18, -10, 10, 18):
        el.append(f'<path d="M{cx3},190 L{cx3 + dx//2},198 L{cx3 + dx},210" fill="none" stroke="{PURPLE}" stroke-width="1.5"/>')
    el.append(txt(cx3, 229, "噬菌体", size=11.2, color=PURPLE, anchor="middle", weight="700"))

    specs_v = [
        ("① 极简家当：", "DNA 或 RNA 二选一，仅数个至数百基因", PURPLE),
        ("② 三无人员：", "0 细胞壁、0 核糖体、0 产 ATP，离体如结晶", RED),
        ("③ 专一开锁：", "靠刺突/尾丝配对受体（连细菌也遭噬菌体感染）", BLUE),
    ]
    for idx, (k, v, col) in enumerate(specs_v):
        yy = 262 + idx * 28
        el.append(txt(398, yy, k, size=11.2, color=col, weight="700"))
        el.append(txt(468, yy, v, size=10.8, color=BODY))

    # Bottom Strip: Practical Disinfection Payoff (y=370..502)
    el.append(card(20, 370, 720, 132))
    el.append(pill(34, 380, "日常洗手实战推论：为什么 75% 酒精秒杀流感和新冠，遇到“诺如病毒”却失灵？", fg=INK, bg=SLATE_SOFT, w=516))

    el.append(card(34, 412, 336, 78, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(48, 434, "有包膜病毒（流感 / 新冠 / 疱疹）：怕酒精 & 肥皂", size=12, color=ORANGE, weight="700"))
    el.append(txt(48, 455, "外层是偷来的脆弱磷脂双分子油膜——75% 医用酒精或肥皂", size=11.2, color=BODY))
    el.append(txt(48, 474, "一碰就把脂质包膜溶解拆散，刺突钥匙脱落，瞬间丧失感染力！", size=11.2, color=BODY))

    el.append(card(386, 412, 340, 78, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(400, 434, "无包膜裸病毒（诺如 / 手足口 / 鼻病毒）：不怕酒精！", size=12, color=BLUE, weight="700"))
    el.append(txt(400, 455, "浑身没有半点油脂包膜，致密蛋白硬壳让免洗酒精凝露无从下嘴；", size=11.2, color=BODY))
    el.append(txt(400, 474, "CDC 指南：必须用肥皂+流动水搓洗 ≥20 秒冲走，物表用含氯消毒液！", size=11.2, color=BODY))

    svg = figure(
        520,
        "细菌细胞结构与病毒非细胞结构对比及酒精消毒差异图解",
        "左图拆解细菌的环状双链DNA、质粒、70S核糖体、细胞膜ATP合成与肽聚糖细胞壁；右图对比有包膜病毒、无包膜裸病毒与噬菌体，底部解释75%酒精为何对无包膜诺如病毒无效。",
        el,
    )
    write_svg(SUBDIR, "anatomy-factory-vs-usb.svg", svg)


def build_replication_anim():
    """Fig 3: Animated comparison of Bacterial Binary Fission vs. Viral Hijack & Lytic Burst (30 min @ 37C)."""
    # Quantitative assertions: E. coli g=20 min -> N(60)=8; Phage latent=25-30 min -> burst ~120
    assert 2 ** (60 // 20) == 8
    burst = 120
    assert math.log10(burst) > 2.0

    css = """
  @keyframes bvScan {
    0% { transform: translateX(0px); opacity: 0.95; }
    100% { transform: translateX(188px); opacity: 0.95; }
  }
  @keyframes bvPinch {
    0%, 35% { opacity: 0.35; }
    55%, 100% { opacity: 1; }
  }
  @keyframes bvBurst {
    0%, 72% { transform: scale(0.86); opacity: 0.35; }
    88%, 100% { transform: scale(1); opacity: 1; }
  }
  @keyframes bvDraw {
    0% { stroke-dashoffset: 280; }
    100% { stroke-dashoffset: 0; }
  }
  .bv-cursor {
    animation: bvScan 6.2s ease-in-out 1 forwards;
  }
  .bv-daughter {
    animation: bvPinch 6.2s ease-out 1 forwards;
  }
  .bv-burst-pack {
    transform-box: fill-box;
    transform-origin: center;
    animation: bvBurst 6.2s ease-out 1 forwards;
  }
  .bv-curve {
    stroke-dasharray: 280;
    stroke-dashoffset: 0;
    animation: bvDraw 6.2s ease-out 1 forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .bv-cursor, .bv-daughter, .bv-burst-pack, .bv-curve {
      animation: none !important;
      opacity: 1 !important;
      stroke-dashoffset: 0 !important;
      transform: none !important;
    }
  }
    """

    el = []
    el.extend(
        header(
            "繁殖方式天壤之别：稳扎稳打的“二分裂分家” vs 先隐身再百倍爆裂的“木马劫持”",
            "左侧对比两者 30 分钟内的命运操作；右侧半对数增长曲线展示细菌指数翻倍（2ⁿ）与病毒一步生长跃迁",
        )
    )

    # Left Top Card: Bacterial Binary Fission (x=20..456, y=64..266)
    el.append(card(20, 64, 436, 202))
    el.append(pill(34, 74, "细菌繁殖：二分裂（Binary Fission，给口肉汤就能自己生）", fg=GREEN, bg=GREEN_SOFT, w=388))

    # Step 1 -> Step 2 -> Step 3 inside card
    # Step 1 (x=42..154)
    el.append(card(36, 108, 122, 108, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    el.append(txt(97, 126, "① 复制环状 DNA", size=11.5, color=GREEN, anchor="middle", weight="700"))
    el.append(f'<rect x="58" y="146" width="78" height="34" rx="17" fill="#dcfce7" stroke="{GREEN}" stroke-width="2"/>')
    el.append(f'<circle cx="84" cy="163" r="9" fill="none" stroke="{BLUE}" stroke-width="1.8"/>')
    el.append(f'<circle cx="108" cy="163" r="9" fill="none" stroke="{BLUE}" stroke-width="1.8"/>')
    el.append(txt(97, 202, "0–10 min：体积长大", size=10.8, color=MUTED, anchor="middle"))

    el.append(f'<line x1="162" y1="162" x2="178" y2="162" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#arr-green)"/>')

    # Step 2 (x=182..302)
    el.append(card(182, 108, 122, 108, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    el.append(txt(243, 126, "② FtsZ 蛋白环收腰", size=11.5, color=GREEN, anchor="middle", weight="700"))
    el.append(
        f'<path d="M198,163 C198,145 234,145 243,156 C252,145 288,145 288,163 C288,181 252,181 243,170 C234,181 198,181 198,163 Z" '
        f'fill="#dcfce7" stroke="{GREEN}" stroke-width="2"/>'
    )
    el.append(f'<line x1="243" y1="146" x2="243" y2="180" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="3 2"/>')
    el.append(txt(243, 202, "15 min：砌新细胞壁隔膜", size=10.8, color=MUTED, anchor="middle"))

    el.append(f'<line x1="308" y1="162" x2="324" y2="162" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#arr-green)"/>')

    # Step 3 (x=328..444)
    el.append(card(328, 108, 114, 108, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(385, 126, "③ 一分为二（2¹）", size=11.5, color=GREEN, anchor="middle", weight="700"))
    el.append('<g class="bv-daughter">')
    el.append(f'<rect x="346" y="138" width="76" height="24" rx="12" fill="#ffffff" stroke="{GREEN}" stroke-width="2"/>')
    el.append(f'<circle cx="384" cy="150" r="6.5" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append(f'<rect x="346" y="168" width="76" height="24" rx="12" fill="#ffffff" stroke="{GREEN}" stroke-width="2"/>')
    el.append(f'<circle cx="384" cy="180" r="6.5" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
    el.append("</g>")
    el.append(txt(385, 206, "20 min：两颗对等子细胞", size=10.8, color=GREEN, anchor="middle", weight="600"))

    el.append(
        txt(
            238,
            236,
            "关键特征：全程细胞完整存在，不依赖任何活宿主细胞；",
            size=10.8,
            color=BODY,
            anchor="middle",
            weight="600",
        )
    )
    el.append(
        txt(
            238,
            254,
            "大肠杆菌最优每 20 分钟翻一倍（N = N₀·2ⁿ）",
            size=10.8,
            color=GREEN,
            anchor="middle",
            weight="600",
        )
    )

    # Left Bottom Card: Viral Hijack & Lytic Burst (x=20..456, y=278..502)
    el.append(card(20, 278, 436, 224))
    el.append(pill(34, 288, "病毒增殖：五步劫持裂解（纯肉汤里 100 年也是 0 增长！）", fg=PURPLE, bg=PURPLE_SOFT, w=388))

    # Step A: Attachment & Injection (x=36..162)
    el.append(card(36, 322, 124, 126, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    el.append(txt(98, 340, "① 吸附与注射图纸", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(f'<rect x="52" y="388" width="92" height="34" rx="14" fill="#ecfdf5" stroke="{GREEN}" stroke-width="1.8"/>')
    el.append(f'<polygon points="98,350 108,357 108,369 98,376 88,369 88,357" fill="#ede9fe" stroke="{PURPLE}" stroke-width="1.8"/>')
    el.append(f'<line x1="98" y1="376" x2="98" y2="402" stroke="{RED}" stroke-width="2.2"/>')
    el.append(txt(98, 438, "0 min：外壳留门外", size=10.8, color=MUTED, anchor="middle"))

    el.append(f'<line x1="164" y1="385" x2="178" y2="385" stroke="{PURPLE}" stroke-width="1.8" marker-end="url(#arr-muted)"/>')

    # Step B: Eclipse Phase Mass Printing (x=182..306)
    el.append(card(182, 322, 124, 126, rx=8, fill="#fffbeb", stroke=AMBER))
    el.append(txt(244, 340, "② 隐蔽期劫持打印", size=11.5, color=AMBER, anchor="middle", weight="700"))
    el.append(f'<rect x="196" y="356" width="96" height="58" rx="16" fill="#ffffff" stroke="{AMBER}" stroke-width="1.8" stroke-dasharray="4 2"/>')
    # Loose parts inside hijacked cell
    for lx, ly in [(214, 374), (236, 370), (262, 376), (222, 396), (250, 394), (272, 396)]:
        el.append(f'<circle cx="{lx}" cy="{ly}" r="4" fill="none" stroke="{PURPLE}" stroke-width="1.6"/>')
        el.append(f'<line x1="{lx-4}" y1="{ly+6}" x2="{lx+5}" y2="{ly+6}" stroke="{RED}" stroke-width="1.6"/>')
    el.append(txt(244, 428, "2–15 min：完整病毒=0！", size=10.8, color=AMBER, anchor="middle", weight="700"))
    el.append(txt(244, 442, "（拆散正借核糖体赶工）", size=10.5, color=MUTED, anchor="middle"))

    el.append(f'<line x1="310" y1="385" x2="324" y2="385" stroke="{PURPLE}" stroke-width="1.8" marker-end="url(#arr-muted)"/>')

    # Step C: Assembly & Lysis Burst (x=328..444)
    el.append(card(328, 322, 114, 126, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(385, 340, "③ 组装与破壁爆裂", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(
        f'<path d="M346,396 C342,374 360,362 374,366 M398,366 C416,368 424,386 416,404 C406,416 362,418 350,406" '
        f'fill="none" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="5 4"/>'
    )
    el.append('<g class="bv-burst-pack">')
    for bx, by in [(364, 374), (386, 366), (408, 374), (358, 394), (382, 388), (404, 394), (374, 406), (396, 408)]:
        el.append(f'<circle cx="{bx}" cy="{by}" r="5" fill="{PURPLE}" stroke="#fff" stroke-width="1"/>')
    el.append("</g>")
    el.append(txt(385, 430, "25–30 min：1 → 120+！", size=11, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(385, 443, "宿主炸裂同归于尽", size=10.5, color=RED, anchor="middle", weight="600"))

    el.append(
        txt(
            238,
            468,
            "注：温和噬菌体/疱疹/HIV 还能走“溶原潜伏”路线——",
            size=10.6,
            color=BODY,
            anchor="middle",
        )
    )
    el.append(
        txt(
            238,
            486,
            "把基因缝进宿主染色体装睡数年，等免疫力低时再引爆",
            size=10.6,
            color=MUTED,
            anchor="middle",
        )
    )

    # Right Card: Quantitative Semilog Growth Comparison (x=470..740, y=64..502)
    el.append(card(470, 64, 270, 438))
    el.append(pill(484, 74, "定量对决：一步生长曲线 vs 二分裂", fg=BLUE, bg=BLUE_SOFT, w=238))
    el.append(txt(605, 112, "37 °C 下单颗起点 0–60 min 粒子数（对数纵轴）", size=11, color=MUTED, anchor="middle"))

    # Plot box: x=518..706 (w=188), y=134..364 (h=230), log10(N) from -0.5 (eclipse=0 floor) to 4.2 (10^4)
    gx0, gx1 = 518.0, 706.0
    gy0, gy1 = 134.0, 354.0

    def px(t_min):
        return gx0 + (t_min / 60.0) * (gx1 - gx0)

    def py(log_n):
        # map log_n in [-0.6, 4.0] -> [gy1, gy0]
        return gy1 - ((log_n - (-0.6)) / 4.6) * (gy1 - gy0)

    # Grid lines
    for lg, lab in [(-0.6, "0(隐蔽)"), (0.0, "1 (10⁰)"), (1.0, "10¹"), (2.0, "10²"), (3.0, "10³"), (4.0, "10⁴")]:
        yy = py(lg)
        el.append(f'<line x1="{gx0}" y1="{yy:.1f}" x2="{gx1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="1"/>')
        el.append(txt(gx0 - 5, yy + 4, lab, size=10.5, color=SLATE, anchor="end"))

    for tm in [0, 20, 30, 40, 60]:
        xx = px(tm)
        el.append(f'<line x1="{xx:.1f}" y1="{gy0}" x2="{xx:.1f}" y2="{gy1}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="2 3"/>')
        el.append(txt(xx, gy1 + 16, f"{tm}", size=10.5, color=SLATE, anchor="middle"))
    el.append(txt((gx0 + gx1) / 2, gy1 + 32, "时间 t（分钟）", size=11, color=INK, anchor="middle", weight="600"))

    # Axes
    el.append(f'<line x1="{gx0}" y1="{gy0}" x2="{gx0}" y2="{gy1}" stroke="{INK}" stroke-width="1.6"/>')
    el.append(f'<line x1="{gx0}" y1="{gy1}" x2="{gx1}" y2="{gy1}" stroke="{INK}" stroke-width="1.6"/>')

    # Curve 1: Sterile broth virus = flat line at 1 (log=0)
    el.append(
        f'<line x1="{px(0):.1f}" y1="{py(0):.1f}" x2="{px(60):.1f}" y2="{py(0):.1f}" '
        f'stroke="{SLATE}" stroke-width="1.8" stroke-dasharray="4 3"/>'
    )
    el.append(txt(px(58), py(0) + 14, "无细胞肉汤中的病毒（永远=1）", size=10.2, color=SLATE, anchor="end", halo=True))

    # Curve 2: E. coli binary fission step/line (0->1, 20->2, 40->4, 60->8)
    b_pts = " ".join(f"{px(t):.1f},{py(math.log10(2**(t/20.0))):.1f}" for t in [0, 20, 40, 60])
    el.append(f'<polyline class="bv-curve" points="{b_pts}" fill="none" stroke="{GREEN}" stroke-width="2.8"/>')
    for t, n in [(0, 1), (20, 2), (40, 4), (60, 8)]:
        el.append(f'<circle cx="{px(t):.1f}" cy="{py(math.log10(n)):.1f}" r="3.6" fill="{GREEN}"/>')
    el.append(txt(px(58), py(math.log10(8)) - 9, "大肠杆菌（60min → 8颗）", size=10.8, color=GREEN, anchor="end", weight="700", halo=True))

    # Curve 3: T4 phage one-step + second wave (0..2min=1 -> 3..22min=-0.6 eclipse -> 28min=120 -> 32..50 eclipse2 -> 58min=14400)
    v_coords = [
        (0, 0.0),
        (2, 0.0),
        (4, -0.6),
        (20, -0.6),
        (27, 2.08),   # ~120 burst 1
        (36, 2.08),
        (58, 3.95),   # second burst wave ~9000+
        (60, 3.95),
    ]
    v_pts = " ".join(f"{px(t):.1f},{py(lg):.1f}" for t, lg in v_coords)
    el.append(f'<polyline class="bv-curve" points="{v_pts}" fill="none" stroke="{PURPLE}" stroke-width="2.8"/>')
    el.append(f'<circle cx="{px(27):.1f}" cy="{py(2.08):.1f}" r="4" fill="{PURPLE}"/>')
    el.append(txt(px(27) + 4, py(2.08) - 10, "首轮裂解 ~120颗", size=10.8, color=PURPLE, anchor="start", weight="700", halo=True))
    el.append(txt(px(56), py(3.95) - 7, "次轮波 ~10⁴颗！", size=10.8, color=PURPLE, anchor="end", weight="700", halo=True))

    # Animated vertical scan bar across plot
    el.append(
        f'<line class="bv-cursor" x1="{gx0:.1f}" y1="{gy0}" x2="{gx0:.1f}" y2="{gy1}" '
        f'stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="3 3"/>'
    )

    # Bottom takeaway box in right card
    el.append(card(484, 394, 242, 94, rx=8, fill=SLATE_SOFT, stroke=HAIRLINE))
    el.append(txt(496, 414, "看懂这张图的两个反直觉点：", size=11.5, color=INK, weight="700"))
    el.append(txt(496, 434, "1. 隐蔽期：第 4–20 min 敲碎宿主也找不", size=10.8, color=BODY))
    el.append(txt(496, 451, "   到整颗病毒，因为外壳已拆成流水线；", size=10.8, color=BODY))
    el.append(txt(496, 470, "2. 爆发量：细菌 1→2，噬菌体 1→120！", size=10.8, color=PURPLE, weight="700"))

    svg = figure(
        520,
        "细菌二分裂繁殖与病毒劫持宿主一步生长曲线动态对比图",
        "左侧对比大肠杆菌20分钟二分裂与T4噬菌体吸附注射、隐蔽期赶工、组装裂解三阶段；右侧对数坐标曲线展示细菌平稳2^n增长、无细胞肉汤中病毒零增长，以及活细胞内病毒隐蔽归零后百倍爆发。",
        el,
        extra_css=css,
    )
    write_svg(SUBDIR, "replication-fission-vs-hijack-anim.svg", svg)


def build_antibiotic_vs_antiviral():
    """Fig 4: Why antibiotics miss viruses 100% (4x 404 targets) vs. how antivirals & vaccines strike."""
    el = []
    el.extend(
        header(
            "药箱里的靶点真相：为什么头孢和阿莫西林对感冒病毒“四枪全脱靶”？",
            "左图：抗生素专打细菌独有零件，病毒压根没这些靶点；右图：疫苗与抗病毒药如何在宿主体内精准设卡",
        )
    )

    # Left Card: Antibiotic 4 Targets on Bacteria vs 4x 404 on Virus (x=20..382, y=64..502)
    el.append(card(20, 64, 362, 438))
    el.append(pill(34, 74, "抗生素（抗菌药）的四把狙击枪", fg=GREEN, bg=GREEN_SOFT, w=244))

    # Mini Bacterium on upper-left vs Mini Virus on upper-right inside Left Card
    el.append(card(34, 108, 160, 88, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(114, 128, "细菌（全套靶点齐全）", size=11.5, color=GREEN, anchor="middle", weight="700"))
    el.append(f'<rect x="64" y="138" width="100" height="42" rx="21" fill="#ffffff" stroke="{GREEN}" stroke-width="2.5"/>')
    el.append(f'<circle cx="96" cy="159" r="9" fill="none" stroke="{BLUE}" stroke-width="1.8"/>')
    el.append(f'<circle cx="122" cy="152" r="3.5" fill="{PURPLE}"/>')
    el.append(f'<circle cx="134" cy="166" r="3.5" fill="{PURPLE}"/>')
    el.append(txt(114, 190, "吃对症抗生素 → 精准瓦解", size=10.6, color=GREEN, anchor="middle", weight="600"))

    el.append(card(208, 108, 160, 88, rx=8, fill=RED_SOFT, stroke=RED))
    el.append(txt(288, 128, "感冒/流感病毒", size=11.5, color=RED, anchor="middle", weight="700"))
    pts_v = " ".join(
        f"{288 + 18 * math.cos(math.radians(a)):.1f},{158 + 18 * math.sin(math.radians(a)):.1f}"
        for a in range(0, 360, 60)
    )
    el.append(f'<polygon points="{pts_v}" fill="#ffffff" stroke="{RED}" stroke-width="2"/>')
    el.append(f'<path d="M279,158 Q288,149 297,158" fill="none" stroke="{RED}" stroke-width="1.8"/>')
    el.append(txt(288, 190, "吃头孢/青霉素 → 0 伤害！", size=10.6, color=RED, anchor="middle", weight="700"))

    # 4 Target Rows (y=208..418)
    targets = [
        ("靶点① 肽聚糖细胞壁", "青霉素 / 阿莫西林 / 头孢", "404 无细胞壁！（连支原体也无）"),
        ("靶点② 细菌 70S 核糖体", "阿奇霉素 / 红霉素 / 四环素", "404 无核糖体！（借人80S打印）"),
        ("靶点③ 细菌 DNA 旋转酶", "左氧氟沙星 / 莫西沙星", "404 无此酶！"),
        ("靶点④ 细菌叶酸合成酶", "复方磺胺甲噁唑", "404 不做代谢！"),
    ]
    for i, (tname, drugs, miss) in enumerate(targets):
        ry = 208 + i * 52
        el.append(card(34, ry, 334, 46, rx=7, fill="#f8fafc", stroke=HAIRLINE))
        el.append(txt(44, ry + 18, tname, size=11.4, color=INK, weight="700"))
        el.append(txt(358, ry + 18, miss, size=10.6, color=RED, anchor="end", weight="700"))
        el.append(txt(44, ry + 37, f"代表药：{drugs}", size=10.8, color=GREEN, weight="600"))

    # Bottom warning box inside Left Card
    el.append(card(34, 422, 334, 68, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(46, 441, "病毒性感冒乱吃抗生素的三大实锤代价：", size=11.5, color=ORANGE, weight="700"))
    el.append(txt(46, 460, "• 病程 1 秒不缩短，却把肠道有益菌无差别误伤致腹泻；", size=10.8, color=BODY))
    el.append(txt(46, 478, "• 替幸存耐药菌清场，亲手筛选出无药可医的“超级细菌”！", size=10.8, color=BODY))

    # Right Card: How Vaccines & Antivirals Stop Viruses (x=396..740, y=64..502)
    el.append(card(396, 64, 344, 438))
    el.append(pill(410, 74, "对付病毒的真正王牌：疫苗 + 精准抗病毒药", fg=BLUE, bg=BLUE_SOFT, w=298))

    # 4 Checkpoints down a clean vertical flow inside Right Card
    checkpoints = [
        (
            "防线 A｜门外拦截（疫苗预演免疫记忆）",
            "接种流感 / HPV / 乙肝 / 狂犬疫苗 → 提前训练 B/T 细胞，中和抗体在病毒进门前直接糊住刺突钥匙！",
            BLUE,
            BLUE_SOFT,
        ),
        (
            "防线 B｜伪装积木卡死复制酶（核苷类似物）",
            "阿昔洛韦（需疱疹病毒胸苷激酶激活才生效！）、索磷布韦等冒充核苷原料，一嵌进病毒链就当场停机",
            PURPLE,
            PURPLE_SOFT,
        ),
        (
            "防线 C｜没收蛋白裁剪刀（蛋白酶/内切酶抑制）",
            "玛巴洛沙韦（掐断流感抢帽内切酶）、奈玛特韦或 HIV 蛋白酶抑制剂，让病毒造出一长串废料切不开",
            TEAL,
            TEAL_SOFT,
        ),
        (
            "防线 D｜焊死出口大门（神经氨酸酶抑制剂）",
            "奥司他韦（达菲）专门锁死流感的 N 刺突小剪刀——新病毒出芽后剪不断绳子，成串粘死在旧细胞表面！",
            ORANGE,
            ORANGE_SOFT,
        ),
    ]
    for i, (title_s, desc_s, fg_c, bg_c) in enumerate(checkpoints):
        cy = 110 + i * 82
        el.append(card(410, cy, 316, 72, rx=8, fill=bg_c, stroke=fg_c))
        el.append(txt(422, cy + 21, title_s, size=11.6, color=fg_c, weight="700"))
        # split desc_s cleanly into 2 lines around ~22 chars
        mid = 23
        el.append(txt(422, cy + 42, desc_s[:mid], size=10.9, color=BODY))
        el.append(txt(422, cy + 60, desc_s[mid:], size=10.9, color=BODY))

    # Bottom bonus box: Phage therapy twist
    el.append(card(410, 440, 316, 50, rx=8, fill=SLATE_SOFT, stroke=HAIRLINE))
    el.append(txt(422, 460, "以毒攻毒彩蛋：噬菌体疗法（Phage Therapy）", size=11.4, color=INK, weight="700"))
    el.append(txt(422, 479, "派专吃细菌的病毒去猎杀超级耐药菌，连有益菌都不伤！", size=10.8, color=PURPLE, weight="600"))

    svg = figure(
        520,
        "抗生素四大细菌靶点脱靶原因与抗病毒药物四大拦截机制图解",
        "左侧展示青霉素头孢、阿奇霉素、左氧氟沙星和磺胺类分别攻击细菌细胞壁、70S核糖体、DNA旋转酶与叶酸合成，而病毒完全缺失这四大结构；右侧展示疫苗中和抗体、核苷类似物、蛋白酶抑制剂与奥司他韦阻断释放。",
        el,
    )
    write_svg(SUBDIR, "antibiotic-vs-antiviral-targets.svg", svg)


def build_master_card():
    """Fig 5: Clinical & everyday decision cheat-sheet + debunking '消炎药' & '黄鼻涕' myths."""
    el = []
    el.extend(
        header(
            "一张图收进收藏夹：细菌 vs 病毒六维终极对照与门诊避坑指南",
            "上方六维硬核速查表（附“裸奔细菌”支原体特例）；下方拆穿“消炎药=头孢”与“黄鼻涕=细菌”两大高频误区",
        )
    )

    # Table Card (x=20..740, y=64..358)
    el.append(card(20, 64, 720, 294))
    # Table header row
    el.append(f'<rect x="28" y="72" width="704" height="34" rx="7" fill="{INK}"/>')
    el.append(txt(98, 94, "对比维度", size=12, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(296, 94, "细菌（Bacteria · 原核活细胞）", size=12, color="#86efac", anchor="middle", weight="700"))
    el.append(txt(578, 94, "病毒（Viruses · 非细胞寄生颗粒）", size=12, color="#d8b4fe", anchor="middle", weight="700"))

    rows = [
        ("典型尺寸", "约 0.5–5 μm（普通光学显微镜可见）", "约 20–300 nm（小 10–100 倍，需电镜）"),
        ("核心装备", "双链DNA + 70S核糖体 + 产能膜 + 肽聚糖壁", "DNA 或 RNA 二选一 + 蛋白衣壳（±脂包膜）"),
        ("独立生存", "能！在营养琼脂/肉汤中每 20min–数小时二分裂", "不能！离体零代谢可结晶，必钻活细胞劫持爆裂"),
        ("人类关系", "99%以上无害或共生有益（合成维生素/发酵酸奶）", "已知大多引起宿主病变，但噬菌体可帮人杀耐药菌"),
        ("常见疾病", "链球菌咽炎、细菌性肺炎、尿路感染、破伤风、结核", "普通感冒、流感、新冠、诺如腹泻、水痘带状疱疹"),
        ("对症武器", "抗生素有效（头孢破壁；无壁支原体用阿奇）", "抗生素100%无效！靠疫苗预防 + 48h内靶向抗病毒药"),
    ]
    for i, (dim, b_txt, v_txt) in enumerate(rows):
        ry = 110 + i * 40
        bg_r = "#f8fafc" if i % 2 == 0 else "#ffffff"
        el.append(f'<rect x="28" y="{ry}" width="704" height="38" rx="5" fill="{bg_r}"/>')
        el.append(f'<line x1="168" y1="{ry+4}" x2="168" y2="{ry+34}" stroke="{BORDER}" stroke-width="1"/>')
        el.append(f'<line x1="432" y1="{ry+4}" x2="432" y2="{ry+34}" stroke="{BORDER}" stroke-width="1"/>')
        el.append(txt(98, ry + 24, dim, size=11.6, color=INK, anchor="middle", weight="700"))
        el.append(txt(178, ry + 24, b_txt, size=11.1, color=BODY))
        el.append(txt(442, ry + 24, v_txt, size=11.1, color=BODY))

    # Bottom 3 Practical Myth-Buster Cards (y=370..502)
    # Card 1: 消炎药 != 抗生素
    el.append(card(20, 370, 232, 132, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(34, 392, "误区①：“头孢是万能消炎药”？", size=11.8, color=ORANGE, weight="700"))
    el.append(txt(34, 414, "• 真正退烧止痛消肿的抗炎药是：", size=10.9, color=BODY))
    el.append(txt(34, 432, "  布洛芬 / 对乙酰氨基酚；", size=10.9, color=INK, weight="700"))
    el.append(txt(34, 452, "• 头孢/阿莫西林只杀细菌，不直接", size=10.9, color=BODY))
    el.append(txt(34, 470, "  退烧！叫它“消炎药”最易乱吃", size=10.9, color=BODY))

    # Card 2: 黄鼻涕 != 细菌感染
    el.append(card(264, 370, 232, 132, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(278, 392, "误区②：“流黄绿浓涕=细菌”？", size=11.8, color=BLUE, weight="700"))
    el.append(txt(278, 414, "• CDC 明确辟谣：病毒性感冒第", size=10.9, color=BODY))
    el.append(txt(278, 432, "  3–5 天中性粒细胞赶来打扫战场，", size=10.9, color=BODY))
    el.append(txt(278, 452, "  释放含铁髓过氧化物酶就会染成", size=10.9, color=BODY))
    el.append(txt(278, 470, "  黄绿色！单看鼻涕颜色抓不准凶手", size=10.9, color=INK, weight="700"))

    # Card 3: 医院怎么精准破案？
    el.append(card(508, 370, 232, 132, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(522, 392, "医院靠什么证据锁定真凶？", size=11.8, color=GREEN, weight="700"))
    el.append(txt(522, 414, "• 直接抓现行：咽拭子抗原 / PCR", size=10.9, color=INK, weight="600"))
    el.append(txt(522, 432, "  核酸快检、24–48h 细菌培养药敏", size=10.9, color=BODY))
    el.append(txt(522, 452, "• 血液旁证：血常规白细胞分类 +", size=10.9, color=BODY))
    el.append(txt(522, 470, "  CRP + 降钙素原（PCT）综合判断", size=10.9, color=BODY))

    svg = figure(
        520,
        "细菌与病毒六维全景对比表及日常就医三大误区指南",
        "汇总细菌与病毒在尺寸、结构、独立繁殖、生态角色、疾病谱与药物靶点上的六大核心差异，并澄清抗生素不等于退烧消炎药、黄鼻涕不等于细菌感染及门诊PCR培养与PCT检验逻辑。",
        el,
    )
    write_svg(SUBDIR, "bacteria-vs-virus-master-card.svg", svg)


@register("bacteria_vs_virus", "细菌与病毒的区别全景系列配图（5张）", "biology")
def build_all():
    build_size_and_filter_scale()
    build_anatomy_factory_vs_usb()
    build_replication_anim()
    build_antibiotic_vs_antiviral()
    build_master_card()
