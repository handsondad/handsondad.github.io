"""Atomic & Nuclear Physics visual builders (Isotopes & Carbon-14 Radiocarbon Dating)."""

from html import escape
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
    LABEL_SIZE,
    MUTED,
    NOTE_SIZE,
    ORANGE,
    ORANGE_SOFT,
    PANEL_TITLE,
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

RED = "#b91c1c"
RED_SOFT = "#fef2f2"
WARM_RED = "#dc2626"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"


def _arrow(x1, y1, x2, y2, color=BLUE, sw=2.0, marker="arr-blue", dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{extra}{mk}/>'
    )


def _curve(d, color=BLUE, sw=2.0, marker=None, dash=None, fill="none", opacity=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#{marker})"' if marker else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round"{extra}{mk}{op}/>'
    )


def _verify_isotope_and_c14_math():
    """Verify IUPAC atomic mass of carbon, C-14 decay math, and 1 mg AMS vs Geiger statistics."""
    # 1. Standard atomic weight of carbon from C-12 (12.000000 u, ~98.93%) & C-13 (13.003355 u, ~1.07%)
    m_c12 = 12.000000
    m_c13 = 13.003354835
    abund_c12 = 0.9893
    abund_c13 = 0.0107
    avg_mass = m_c12 * abund_c12 + m_c13 * abund_c13
    assert abs(avg_mass - 12.0107) < 0.0005

    # 2. C-14 Cambridge physical half-life vs Libby conventional half-life
    t_half_phys = 5730.0
    t_half_libby = 5568.0
    tau_phys = t_half_phys / math.log(2.0)   # ~8266.6 years
    tau_libby = t_half_libby / math.log(2.0) # ~8033.0 years (ORAU exact constant!)
    assert abs(round(tau_libby) - 8033) == 0
    assert 8266.0 <= tau_phys <= 8268.0

    # 3. Remaining fraction checks at key historical dates
    frac_sanxingdui = 0.5 ** (3100.0 / t_half_phys)  # ~68.7%
    frac_otzi = 0.5 ** (5300.0 / t_half_phys)        # ~52.7%
    frac_10_hl = 0.5 ** 10                           # 1/1024 ~ 0.0977%
    assert 0.67 <= frac_sanxingdui <= 0.70
    assert 0.51 <= frac_otzi <= 0.54
    assert abs(frac_10_hl - 1.0 / 1024.0) < 1e-12

    # 4. Atoms vs decays in 1 mg of 5730-year-old carbon:
    # 1 mg C = 1e-3 / 12 mol * 6.022e23 = 5.018e19 C-12 atoms.
    # Modern 14C/12C ~ 1.2e-12 -> at 1 half-life (5730 yr) = 0.6e-12 -> ~3.01e7 C-14 atoms!
    n_c12_1mg = (1e-3 / 12.0) * 6.02214076e23
    n_c14_1hl = n_c12_1mg * 0.6e-12
    assert 2.8e7 <= n_c14_1hl <= 3.2e7
    # Decay rate = N / tau_phys:
    decays_per_hour = n_c14_1hl / (tau_phys * 365.2425 * 24.0)
    hours_per_decay = 1.0 / decays_per_hour
    assert 2.2 <= hours_per_decay <= 2.6  # ~1 decay every 2.4 hours in 1 mg!
    return avg_mass, tau_phys, tau_libby, n_c14_1hl, hours_per_decay


def _nucleus_cluster(cx, cy, n_protons, n_neutrons, p_col=WARM_RED, n_col=BLUE):
    """Draw a deterministic compact nucleon cluster + two electron shells (2 + 4 for carbon)."""
    out = []
    # Electron shells (inner K=2, outer L=4 for Z=6)
    out.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="4 3"/>')
    for ang_deg in (35, 215):
        ex = cx + 34 * math.cos(math.radians(ang_deg))
        ey = cy + 34 * math.sin(math.radians(ang_deg))
        out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.1" fill="{TEAL}"/>')
    for ang_deg in (0, 90, 180, 270):
        ex = cx + 50 * math.cos(math.radians(ang_deg))
        ey = cy + 50 * math.sin(math.radians(ang_deg))
        out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.1" fill="{TEAL}"/>')

    # Deterministic spiral nucleon placement around (cx, cy)
    total = n_protons + n_neutrons
    kinds = []
    p_left, n_left = n_protons, n_neutrons
    while p_left > 0 or n_left > 0:
        if p_left > 0:
            kinds.append("p")
            p_left -= 1
        if n_left > 0:
            kinds.append("n")
            n_left -= 1
    golden = 2.39996323
    for i, k in enumerate(kinds):
        rr = 0.0 if i == 0 else 4.7 * math.sqrt(i)
        ang = i * golden
        nx = cx + rr * math.cos(ang)
        ny = cy + rr * math.sin(ang)
        col = p_col if k == "p" else n_col
        out.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="4.5" fill="{col}" stroke="#ffffff" stroke-width="0.9"/>')
    return "\n".join(out)


def _build_carbon_triplet_isotopes():
    """Fig 1: Periodic table seat #6 + Carbon-12, Carbon-13, Carbon-14 structure & abundance."""
    avg_mass, _, _, _, _ = _verify_isotope_and_c14_math()
    h = 504
    el = []
    el.extend(
        header(
            "什么是“同位素”？挤在元素周期表第 6 号座位上的碳家三兄弟",
            "质子数 Z=6 决定它们都叫“碳”、化学脾气相同；中子数 N=6, 7, 8 不同，让体重与原子核寿命大相径庭",
        )
    )

    # Left card: Periodic Table Seat #6 ("同位" = same place!)
    el.append(card(24, 68, 174, 412, fill="#ffffff"))
    el.append(pill(38, 82, "为什么叫“同位”素？", fg=PURPLE, bg=PURPLE_SOFT, w=146, size=11.5))

    # Big periodic table tile
    el.append(card(46, 120, 130, 136, rx=10, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.8))
    el.append(txt(58, 144, "6", size=15, color=PURPLE, weight="700", cls="mono"))
    el.append(txt(164, 142, "第6号座位", size=10.5, color=PURPLE, anchor="end", weight="600"))
    el.append(txt(111, 186, "C", size=22, color=INK, anchor="middle", weight="700"))
    el.append(txt(111, 218, "碳 Carbon", size=12.5, color=BODY, anchor="middle", weight="600"))
    el.append(txt(111, 242, f"{avg_mass:.3f}", size=13, color=WARM_RED, anchor="middle", weight="700", cls="mono"))

    el.append(txt(38, 280, "索迪（1913）造词：", size=11.5, color=INK, weight="700"))
    el.append(txt(38, 299, "希腊语 isos(相同) +", size=11, color=BODY))
    el.append(txt(38, 317, "topos(位置) = 同占一格", size=11, color=BODY))

    el.append(card(36, 334, 150, 132, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(46, 354, "为什么原子量带小数？", size=11.5, color=WARM_RED, weight="700"))
    el.append(txt(46, 374, "12 × 98.93%", size=11, color=BODY, cls="mono"))
    el.append(txt(46, 392, "+ 13.003 × 1.07%", size=11, color=BODY, cls="mono"))
    el.append(txt(46, 410, f"≈ {avg_mass:.3f}！", size=11.5, color=WARM_RED, weight="700", cls="mono"))
    el.append(txt(46, 431, "小数尾数正是天然重稳定", size=10.5, color=MUTED))
    el.append(txt(46, 448, "同位素 ¹³C 留下的证据", size=10.5, color=MUTED))

    # Legend strip above the 3 sibling cards
    el.append(f'<circle cx="226" cy="84" r="5" fill="{WARM_RED}"/>')
    el.append(txt(236, 88, "质子 (+e，固定 6 个)", size=11.5, color=BODY, weight="600"))
    el.append(f'<circle cx="384" cy="84" r="5" fill="{BLUE}"/>')
    el.append(txt(394, 88, "中子 (不带电，6 / 7 / 8 个)", size=11.5, color=BODY, weight="600"))
    el.append(f'<circle cx="566" cy="84" r="4" fill="{TEAL}"/>')
    el.append(txt(576, 88, "核外电子 (6 个，决定化学键)", size=11.5, color=BODY, weight="600"))

    # Three sibling cards across x=212..736 (each w=166, gap=13)
    siblings = [
        (
            "碳-12 (¹²C)",
            "老大哥 · 绝对主力",
            6,
            6,
            BLUE,
            BLUE_SOFT,
            "98.93%",
            "稳定（永不衰变）",
            "6 质子 + 6 中子 = 12",
            "身手最轻快，植物光合",
            "作用吸收 CO₂ 时最偏爱它",
        ),
        (
            "碳-13 (¹³C)",
            "二哥 · 产地指纹官",
            6,
            7,
            GREEN,
            GREEN_SOFT,
            "1.07%",
            "稳定（永不衰变）",
            "6 质子 + 7 中子 = 13",
            "重约 8%，专门用来鉴别",
            "古人食谱、真假蜂蜜与碳源",
        ),
        (
            "碳-14 (¹⁴C)",
            "三弟 · 考古时间秒表",
            6,
            8,
            ORANGE,
            ORANGE_SOFT,
            "≈ 1 / 10¹²",
            "放射性（半衰期 5730 年）",
            "6 质子 + 8 中子 = 14",
            "一万亿个碳里仅 1 个！中子",
            "过多不稳定，死后定时衰变",
        ),
    ]

    for idx, (name, role, np_, nn_, fg, bg, abund, stab, formula, line1, line2) in enumerate(siblings):
        cx0 = 212 + idx * 179
        el.append(card(cx0, 102, 166, 378, fill="#ffffff", stroke=fg if idx == 2 else BORDER, sw=1.5 if idx == 2 else 1.0))
        el.append(pill(cx0 + 14, 114, name, fg=fg, bg=bg, w=138, size=12))
        el.append(txt(cx0 + 83, 153, role, size=11.5, color=MUTED, anchor="middle", weight="600"))

        # Atom diagram centered at (cx0 + 83, 222)
        el.append(_nucleus_cluster(cx0 + 83, 222, np_, nn_))
        if idx == 2:
            # Tiny radiation wave badge on C-14
            el.append(pill(cx0 + 106, 166, "β⁻衰变", fg=WARM_RED, bg=RED_SOFT, w=50, h=18, size=10))

        el.append(card(cx0 + 12, 288, 142, 86, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        el.append(txt(cx0 + 83, 308, formula, size=11, color=INK, anchor="middle", weight="700"))
        el.append(txt(cx0 + 83, 330, f"自然丰度：{abund}", size=11.5, color=fg, anchor="middle", weight="700"))
        el.append(txt(cx0 + 83, 352, stab, size=10.5, color=WARM_RED if idx == 2 else GREEN, anchor="middle", weight="600"))

        el.append(txt(cx0 + 14, 398, "• 核外都有 6 个电子，都", size=10.5, color=BODY))
        el.append(txt(cx0 + 14, 415, "  能生成 CO₂ 进入生命体", size=10.5, color=BODY))
        el.append(txt(cx0 + 14, 436, f"• {line1}", size=10.5, color=INK, weight="600"))
        el.append(txt(cx0 + 22, 453, line2, size=10.5, color=INK, weight="600"))

    svg = figure(
        h,
        "碳元素三种同位素（碳-12、碳-13、碳-14）原子核结构与丰度对比图",
        "左侧展示元素周期表第6号碳格（原子量12.011源于稳定同位素加权平均）及1913年索迪提出同位素（同占一格）的词源；右侧并列对比碳-12（6质子6中子，丰度98.93%，稳定）、碳-13（6质子7中子，丰度1.07%，稳定）与碳-14（6质子8中子，丰度约一万亿分之一，半衰期5730年β衰变）。",
        el,
    )
    write_svg("isotopes-c14", "carbon-triplet-isotopes.svg", svg)


def _build_stable_vs_radio_detectives():
    """Fig 2: Overview of Stable Isotopes (fingerprints/thermometers) vs Radioactive Isotopes (clocks)."""
    h = 482
    el = []
    el.extend(
        header(
            "不止碳十四！同位素神探家族的“两大破案流派”",
            "稳定同位素靠“轻重分馏差”查身世与古温度；放射性同位素靠“固定半衰期”给地球、古人类与文物算年龄",
        )
    )

    # Left Column: Stable Isotopes (x=24, w=346)
    el.append(card(24, 68, 346, 392, fill="#ffffff"))
    el.append(pill(40, 82, "流派一：稳定同位素（永不衰变的“指纹仪”）", fg=TEAL, bg=TEAL_SOFT, w=312, size=11.5))
    el.append(txt(40, 121, "核心原理：化学反应一样，但“胖原子”蒸发慢、反应慢！", size=11.5, color=INK, weight="700"))

    stable_cases = [
        (
            "氧-18 / 氧-16 (¹⁸O / ¹⁶O) · 冰芯古温度计",
            BLUE,
            BLUE_SOFT,
            "含 ¹⁶O 的轻水分子更易蒸发，含 ¹⁸O 的重水更易凝结降落。",
            "钻取南极冰芯与深海有孔虫测 ¹⁸O 比例，就能重建过去",
            "80 万年冰期—间冰期的地球古温度曲线！",
        ),
        (
            "碳-13 / 碳-12 (δ¹³C) · 古人食谱与打假神探",
            GREEN,
            GREEN_SOFT,
            "水稻/小麦(C3植物，δ¹³C≈-27‰)与小米/玉米/甘蔗(C4植物，",
            "≈-13‰)挑食程度不同。测一段古人骨胶原可知吃粟还是吃稻；",
            "测一勺蜂蜜立刻抓出掺入廉价玉米/甘蔗糖浆的假蜂蜜！",
        ),
        (
            "氢同位素：氕(¹H) · 氘(²H 重氢) + 氮-15(¹⁵N)",
            PURPLE,
            PURPLE_SOFT,
            "重水(D₂O)可用作核反应堆慢化剂；骨骼 ¹⁵N 越富集代表食物链",
            "营养级越高——一眼分辨古人类究竟吃素还是吃肉为主！",
            "",
        ),
    ]
    cy = 136
    for title_s, fg_s, bg_s, l1, l2, l3 in stable_cases:
        bh = 100 if l3 else 84
        el.append(card(40, cy, 314, bh, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        el.append(pill(50, cy + 8, title_s, fg=fg_s, bg=bg_s, w=294, h=20, size=11))
        el.append(txt(52, cy + 45, l1, size=10.5, color=BODY))
        el.append(txt(52, cy + 63, l2, size=10.5, color=BODY))
        if l3:
            el.append(txt(52, cy + 81, l3, size=10.5, color=INK, weight="600"))
        cy += bh + 12

    # Right Column: Radioactive Isotopes Ruler (x=386, w=350)
    el.append(card(386, 68, 350, 392, fill="#ffffff"))
    el.append(pill(402, 82, "流派二：放射性同位素（自带节拍的“原子钟”）", fg=ORANGE, bg=ORANGE_SOFT, w=318, size=11.5))
    el.append(txt(402, 121, "核心原理：半衰期不受高温高压化学反应影响，各管一段历史！", size=11.5, color=INK, weight="700"))

    clocks = [
        ("铀-238 → 铅-206", "半衰期 44.7 亿年", "测地球年龄(45.4亿年)、月岩与陨石", SLATE, 304),
        ("钾-40 → 氩-40", "半衰期 12.5 亿年", "测百万年火山灰夹层（如东非古人类化石）", PURPLE, 248),
        ("碳-14 → 氮-14", "半衰期 5,730 年", "黄金标尺：几百年 ～ 5 万年内人类文明遗存！", WARM_RED, 186),
        ("医疗短寿核素 ¹⁸F / ¹³¹I", "110 分钟 / 8 天", "医院 PET-CT 肿瘤显像、甲亢靶向治疗", BLUE, 108),
    ]
    ry = 138
    for c_name, c_hl, c_use, c_col, bar_len in clocks:
        is_c14 = "碳-14" in c_name
        el.append(
            card(
                402,
                ry,
                318,
                68,
                rx=8,
                fill=RED_SOFT if is_c14 else SLATE_SOFT,
                stroke=WARM_RED if is_c14 else BORDER,
                sw=1.5 if is_c14 else 1.0,
            )
        )
        el.append(txt(414, ry + 20, c_name, size=12, color=c_col, weight="700"))
        el.append(txt(708, ry + 20, c_hl, size=11, color=c_col, anchor="end", weight="700"))
        el.append(f'<rect x="414" y="{ry + 28}" width="{bar_len}" height="8" rx="4" fill="{c_col}" opacity="0.82"/>')
        el.append(txt(414, ry + 54, c_use, size=10.5, color=INK if is_c14 else BODY, weight="600" if is_c14 else None))
        ry += 78

    el.append(txt(402, 452, "注：恐龙化石(≥6600万年前)远超碳十四5万年量程，须测夹层铀铅/钾氩！", size=10, color=WARM_RED, weight="600"))

    svg = figure(
        h,
        "稳定同位素示踪与放射性同位素测年家族分工对比图",
        "左栏展示稳定同位素（氧-18冰芯古温度计、碳-13食谱与蜂蜜鉴伪、重氢与氮-15营养级追踪）；右栏按半衰期跨度对比铀-238（44.7亿年，测地球年龄）、钾-40（12.5亿年，测古人类火山灰）、碳-14（5730年，测5万年以内有机文物）及医学短寿命核素氟-18（110分钟）。",
        el,
    )
    write_svg("isotopes-c14", "stable-vs-radio-isotope-detectives.svg", svg)


def _build_c14_cosmic_cycle():
    """Fig 3: Cosmic ray creation + living recharge + post-mortem beta decay (1-shot accessible animation)."""
    h = 528
    extra_defs = f"""
    <marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{WARM_RED}"/>
    </marker>
    """
    extra_css = """
    @keyframes c14-flow {
      0%   { stroke-dashoffset: 360; opacity: 0.35; }
      100% { stroke-dashoffset: 0;   opacity: 1; }
    }
    @keyframes meter-drop {
      0%, 40% { transform: scaleX(1); }
      100%    { transform: scaleX(0.5); }
    }
    .flow-anim {
      stroke-dasharray: 360;
      animation: c14-flow 6.5s ease-out 1 forwards;
    }
    .decay-bar-anim {
      transform-box: fill-box;
      transform-origin: left center;
      animation: meter-drop 7.5s ease-in-out 1 forwards;
    }
    @media (prefers-reduced-motion: reduce) {
      .flow-anim, .decay-bar-anim {
        animation: none !important;
      }
    }
    """
    el = []
    el.extend(
        header(
            "地球 45 亿岁了，半衰期才 5730 年的碳十四为什么没死光？",
            "高空宇宙射线每时每刻都在“新造”碳十四：活着不断充值同步，死亡瞬间拔掉电源启动倒计时",
        )
    )

    # Top Stage 1 Card: Upper Atmosphere Factory (y=68..208)
    el.append(card(24, 68, 712, 138, fill="#eff6ff", stroke=BLUE_LINE, sw=1.2))
    el.append(step_badge(44, 90, 1, fg=BLUE, bg="#ffffff"))
    el.append(txt(62, 94, "高空造碳工厂（距地 12–15 km 平流层低层）：宇宙射线把氮变成碳十四", size=13, color=INK, weight="700"))

    # Reaction flow boxes horizontally: Cosmic Ray -> Slow Neutron + 14N -> 14C + Proton -> 14CO2
    el.append(card(42, 114, 142, 74, rx=8, fill="#ffffff", stroke=BORDER))
    el.append(txt(113, 138, "外太空宇宙射线", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(113, 158, "轰击大气碎裂出", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(113, 175, "慢速热中子 (n)", size=11, color=BLUE, anchor="middle", weight="700"))

    el.append(_arrow(188, 151, 218, 151, color=BLUE, sw=2.2))

    el.append(card(224, 114, 290, 74, rx=8, fill="#ffffff", stroke=ORANGE, sw=1.4))
    el.append(txt(369, 137, "核反应：n + ¹⁴₇N  →  ¹⁴₆C + ¹₁p（踢走 1 个质子！）", size=12, color=WARM_RED, anchor="middle", weight="700"))
    el.append(txt(369, 158, "大气 78% 是氮-14(7质子7中子)；吞下 1 个中子、踢出 1 个质子", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(369, 176, "刚好变成 6 质子 8 中子的碳-14！（全球每年新产约 7.5 kg）", size=10.5, color=MUTED, anchor="middle"))

    el.append(_arrow(518, 151, 548, 151, color=ORANGE, sw=2.2, marker="arr-orange"))

    el.append(card(554, 114, 164, 74, rx=8, fill="#ffffff", stroke=GREEN, sw=1.3))
    el.append(txt(636, 138, "迅速氧化为 ¹⁴CO₂", size=12, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(636, 158, "混入普通 ¹²CO₂ 大气池", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(636, 175, "平衡比 ≈ 1 : 10¹²", size=11, color=GREEN, anchor="middle", weight="700", cls="mono"))

    # Downward animated assimilation path into Stage 2
    el.append(
        f'<path d="M636,190 L636,222 L200,222 L200,242" fill="none" stroke="{GREEN}" '
        f'stroke-width="2.4" class="flow-anim" marker-end="url(#arr-green)"/>'
    )
    el.append(txt(425, 217, "光合作用与食物链传递（全球生物共享同一浓度）", size=11, color=GREEN, anchor="middle", weight="600", halo=True))

    # Bottom Left Stage 2 Card: Living Organism ("Online Recharge", x=24, y=244, w=344, h=262)
    el.append(card(24, 244, 344, 262, fill="#ffffff", stroke=GREEN, sw=1.4))
    el.append(step_badge(44, 268, 2, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(62, 272, "活着的时候：边衰变边“实时充值”", size=13, color=GREEN, weight="700"))

    el.append(card(42, 290, 308, 108, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.0))
    el.append(txt(56, 314, "• 树木光合作用吸碳 → 食草动物吃植物 → 人类吃饭", size=11, color=BODY))
    el.append(txt(56, 336, "• 体内虽不断有 ¹⁴C 衰变，但每天呼吸进食持续补新货", size=11, color=BODY))
    el.append(txt(56, 358, "• 活体组织（新长树轮、竹子、骨骼）里的比值恒定：", size=11, color=INK, weight="600"))
    el.append(txt(196, 383, "¹⁴C / ¹²C  =  100% 现代大气标准（约每克碳每分钟衰变 13.6 次）", size=10.5, color=GREEN, anchor="middle", weight="700"))

    # Meter bar at 100%
    el.append(txt(42, 422, "活体 ¹²C 存量（稳定不变）", size=11, color=SLATE))
    el.append(f'<rect x="206" y="411" width="140" height="13" rx="4" fill="{BLUE}"/>')
    el.append(txt(42, 448, "活体 ¹⁴C 比例（满格 100%）", size=11, color=GREEN, weight="700"))
    el.append(f'<rect x="206" y="437" width="140" height="13" rx="4" fill="{GREEN}"/>')
    el.append(txt(42, 484, "关键提醒：树木只有最外圈当年新树轮在“充值”，树心老木早已停表！", size=10.5, color=MUTED))

    # Arrow from Living to Dead/Buried
    el.append(_arrow(370, 372, 394, 372, color=WARM_RED, sw=2.4, marker="arr-red"))

    # Bottom Right Stage 3 Card: Death & Burial ("Unplugged Stopwatch", x=396, y=244, w=340, h=262)
    el.append(card(396, 244, 340, 262, fill="#ffffff", stroke=WARM_RED, sw=1.4))
    el.append(step_badge(416, 268, 3, fg=WARM_RED, bg=RED_SOFT))
    el.append(txt(434, 272, "死亡那一刻：拔掉充电线，秒表启动！", size=13, color=WARM_RED, weight="700"))

    el.append(card(414, 290, 304, 108, rx=8, fill=RED_SOFT, stroke=WARM_RED, sw=1.0))
    el.append(txt(426, 314, "• 砍伐或死亡后，停止呼吸与进食，不再补充新 ¹⁴C", size=11, color=BODY))
    el.append(txt(426, 336, "• 遗骸里的 ¹²C 纹丝不动，而 ¹⁴C 发生 β⁻ 衰变变回氮：", size=11, color=BODY))
    el.append(txt(566, 360, "¹⁴₆C  →  ¹⁴₇N + e⁻ + ν̄ₑ", size=12, color=WARM_RED, anchor="middle", weight="700"))
    el.append(txt(566, 383, "每过 5,730 年，剩下的 ¹⁴C/¹²C 比例就精确折半！", size=10.5, color=INK, anchor="middle", weight="700"))

    # Meter bar after 1 half-life (50%)
    el.append(txt(414, 422, "遗骸 ¹²C 存量（依然 100%）", size=11, color=SLATE))
    el.append(f'<rect x="580" y="411" width="136" height="13" rx="4" fill="{BLUE}"/>')
    el.append(txt(414, 448, "5730年后 ¹⁴C（剩 50%！）", size=11, color=WARM_RED, weight="700"))
    el.append('<rect x="580" y="437" width="136" height="13" rx="4" fill="#fee2e2" stroke="#fca5a5"/>')
    el.append(f'<rect x="580" y="437" width="68" height="13" rx="4" fill="{WARM_RED}"/>')
    el.append(txt(414, 484, "测出样品里“还剩百分之几的 ¹⁴C/¹²C”，就能反推出死亡距今年代！", size=10.5, color=WARM_RED, weight="600"))

    svg = figure(
        h,
        "碳十四高空生成、活体循环充值与死后衰变计时闭环图",
        "分三步展示碳十四循环：①高空12至15公里宇宙射线慢中子轰击氮-14踢出1个质子生成碳-14并氧化为二氧化碳；②活体植物与动物通过光合作用和食物链维持与大气相同的10⁻¹²平衡丰度；③生物死亡后停止补碳，碳-12保持不变而碳-14以5730年半衰期发生β衰变变回氮-14。",
        el,
        extra_css=extra_css,
        extra_defs=extra_defs,
    )
    write_svg("isotopes-c14", "c14-cosmic-birth-life-death-cycle.svg", svg)


def _build_c14_decay_curve():
    """Fig 4: Exact exponential decay curve N(t)/N0 = 2^(-t/5730) with Sanxingdui, Shroud, Otzi & 50kyr limit."""
    _, tau_phys, tau_libby, _, _ = _verify_isotope_and_c14_math()
    h = 498
    el = []
    el.extend(
        header(
            "碳十四指数衰变曲线：从都灵裹尸布、三星堆祭祀坑到 5 万年量程极限",
            "按真实物理半衰期 T₁/₂ = 5,730 年精确计算：每多走一个半衰期减半一次，10 个半衰期后不足千分之一",
        )
    )

    # Main plot card
    el.append(card(24, 68, 712, 336, fill="#ffffff"))

    gx0, gx1 = 76.0, 708.0
    gy0, gy1 = 98.0, 354.0  # gy0 = 100%, gy1 = 0%
    t_max = 57300.0  # 10 half-lives

    def x_t(t_yr):
        return gx0 + (t_yr / t_max) * (gx1 - gx0)

    def y_f(frac):
        return gy1 - frac * (gy1 - gy0)

    # Horizontal grid lines (100%, 75%, 50%, 25%, 12.5%, 0%)
    for pct in (100, 75, 50, 25, 0):
        yy = y_f(pct / 100.0)
        el.append(_curve(f"M{gx0:.1f},{yy:.1f} L{gx1:.1f},{yy:.1f}", color=HAIRLINE if pct else SLATE, sw=1.0, dash="4 4" if pct else None))
        el.append(txt(gx0 - 8, yy + 4, f"{pct}%", size=11, color=SLATE, anchor="end", cls="mono"))

    # Vertical half-life grid lines (0, 1, 2, 3, 5, 8, 10 half-lives)
    for k in (0, 1, 2, 3, 5, 8, 10):
        tt = k * 5730.0
        xx = x_t(tt)
        el.append(_curve(f"M{xx:.1f},{gy0:.1f} L{xx:.1f},{gy1:.1f}", color=HAIRLINE, sw=0.9, dash="3 4"))
        lbl_yr = "0(现代)" if k == 0 else f"{int(tt):,}"
        el.append(txt(xx, gy1 + 17, lbl_yr, size=10.5, color=SLATE, anchor="middle", cls="mono"))
        if k in (1, 2, 3, 5, 10):
            el.append(txt(xx, gy1 + 32, f"{k}T₁/₂", size=10, color=MUTED, anchor="middle", cls="mono"))

    el.append(txt(548, gy1 + 33, "死亡距今年数 t（年）", size=11, color=INK, anchor="middle", weight="600"))

    # Shaded area under exponential curve + exact polyline (120 steps)
    pts = []
    for i in range(121):
        tt = t_max * i / 120.0
        ff = 0.5 ** (tt / 5730.0)
        pts.append((x_t(tt), y_f(ff)))
    poly_d = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    area_d = poly_d + f" L{gx1:.2f},{gy1:.2f} L{gx0:.2f},{gy1:.2f} Z"
    el.append(f'<path d="{area_d}" fill="{ORANGE_SOFT}" opacity="0.55"/>')
    el.append(_curve(poly_d, color=WARM_RED, sw=2.8))

    # Landmark pins (carefully staggered so zero text overlap!)
    # 1. Turin Shroud (~670 yr old -> ~92.2%)
    t1, f1 = 670.0, 0.5 ** (670.0 / 5730.0)
    el.append(f'<circle cx="{x_t(t1):.1f}" cy="{y_f(f1):.1f}" r="4" fill="{PURPLE}" stroke="#fff" stroke-width="1.2"/>')
    el.append(_curve(f"M{x_t(t1) + 4:.1f},{y_f(f1) - 2:.1f} L{x_t(t1) + 46:.1f},{y_f(f1) - 12:.1f}", color=PURPLE, sw=1.2))
    el.append(txt(x_t(t1) + 50, y_f(f1) - 10, "都灵裹尸布 (~670年, 剩92.2% → 中世纪亚麻)", size=10.5, color=PURPLE, weight="700", halo=True))

    # 2. Sanxingdui Sacrificial Pits (~3,100 yr old -> ~68.7%)
    t2, f2 = 3100.0, 0.5 ** (3100.0 / 5730.0)
    el.append(f'<circle cx="{x_t(t2):.1f}" cy="{y_f(f2):.1f}" r="4.5" fill="{WARM_RED}" stroke="#fff" stroke-width="1.3"/>')
    el.append(_curve(f"M{x_t(t2) + 5:.1f},{y_f(f2) - 2:.1f} L{x_t(t2) + 54:.1f},{y_f(f2) - 14:.1f}", color=WARM_RED, sw=1.4))
    el.append(txt(x_t(t2) + 58, y_f(f2) - 11, "三星堆祭祀坑炭屑 (~3100年, 剩68.7% → 商代晚期)", size=11, color=WARM_RED, weight="700", halo=True))

    # 3. 1st Half-life (5,730 yr -> 50.0%, near Otzi 5300 yr)
    t3, f3 = 5730.0, 0.5
    el.append(f'<circle cx="{x_t(t3):.1f}" cy="{y_f(f3):.1f}" r="4.5" fill="{BLUE}" stroke="#fff" stroke-width="1.3"/>')
    el.append(_curve(f"M{x_t(t3) + 5:.1f},{y_f(f3):.1f} L{x_t(t3) + 46:.1f},{y_f(f3) - 6:.1f}", color=BLUE, sw=1.3))
    el.append(txt(x_t(t3) + 50, y_f(f3) - 3, "1个半衰期 5,730年：剩 50.0%（冰人奥兹 ~5300年近此）", size=10.5, color=BLUE, weight="700", halo=True))

    # 4. 2nd Half-life (11,460 yr -> 25.0%)
    t4, f4 = 11460.0, 0.25
    el.append(f'<circle cx="{x_t(t4):.1f}" cy="{y_f(f4):.1f}" r="4" fill="{BLUE}" stroke="#fff" stroke-width="1.2"/>')
    el.append(txt(x_t(t4) + 12, y_f(f4) - 6, "2个半衰期 (11,460年)：剩 25.0%（万年新石器之交）", size=10.5, color=BLUE, weight="600", halo=True))

    # 5. 3rd Half-life (17,190 yr -> 12.5%)
    t5, f5 = 17190.0, 0.125
    el.append(f'<circle cx="{x_t(t5):.1f}" cy="{y_f(f5):.1f}" r="4" fill="{TEAL}" stroke="#fff" stroke-width="1.2"/>')
    el.append(txt(x_t(t5) + 12, y_f(f5) - 10, "3个半衰期 (17,190年)：剩 12.5%（拉斯科洞穴壁画期）", size=10.5, color=TEAL, weight="600", halo=True))

    # 6. 50,000 - 57,300 yr limit (<0.1%)
    t6, f6 = 51570.0, 0.5 ** 9
    el.append(f'<circle cx="{x_t(t6):.1f}" cy="{y_f(f6):.1f}" r="4" fill="{SLATE}" stroke="#fff" stroke-width="1.2"/>')
    el.append(txt(702, y_f(0.055), "≈5万年测年上限：剩 <0.2%（10T₁/₂ 仅剩 1/1024）", size=10, color=SLATE, anchor="end", weight="700", halo=True))

    # Bottom dual-half-life convention explanation card
    el.append(card(24, 414, 712, 68, fill="#ffffff"))
    el.append(pill(38, 426, "为什么报告有两个半衰期(5568 vs 5730)？", fg=ORANGE, bg=ORANGE_SOFT, w=258, h=20, size=10.5))
    el.append(
        txt(
            306,
            440,
            f"利比初测 5568 年(均寿 {tau_libby:.0f} 年)，精确物理值 5730±40 年(均寿 {tau_phys:.0f} 年)。",
            size=10,
            color=BODY,
        )
    )
    el.append(
        txt(
            38,
            466,
            "国际约定原始“惯用年龄 BP(距1950年)”仍按 5568 年报数，再用 IntCal20 树轮曲线统一校正为日历年(cal BC/AD)！",
            size=10,
            color=MUTED,
        )
    )

    svg = figure(
        h,
        "碳十四5730年半衰期指数衰变曲线与典型文物年代标定图",
        "精确绘制N(t)/N0=2^(-t/5730)指数衰变曲线，标出都灵裹尸布（约670年，剩92.2%）、三星堆祭祀坑炭屑（约3100年，剩68.7%）、1个半衰期5730年（剩50%）、2个半衰期11460年（剩25%）、3个半衰期17190年（剩12.5%）及约5万年测年上限（不足0.2%），底部说明5568年惯用半衰期与5730年物理半衰期的国际换算约定。",
        el,
    )
    write_svg("isotopes-c14", "c14-exponential-decay-curve.svg", svg)


def _build_geiger_vs_ams_revolution():
    """Fig 5: Why waiting for beta decay needed grams of sample, while AMS counts C-14 atoms directly from 1 mg."""
    _, _, _, n_c14_1hl, hours_per_decay = _verify_isotope_and_c14_math()
    h = 468
    el = []
    el.extend(
        header(
            "从“烧掉几克木炭苦等爆炸”到“几毫克直接点名”：加速器质谱（AMS）革命",
            f"算一笔惊人账：1 毫克 5730 岁的古碳里藏着约 {n_c14_1hl / 1e7:.0f}000 万个 ¹⁴C 原子，但每 {hours_per_decay:.1f} 小时才衰变 1 个！",
        )
    )

    # Top Comparison Strip: 1949 Decay Counting vs 1977+ AMS Atom Counting
    el.append(card(24, 68, 344, 152, fill="#ffffff"))
    el.append(pill(40, 82, "初代方法：β 衰变计数法（利比 1949）", fg=SLATE, bg=SLATE_SOFT, w=254, size=11.5))
    el.append(txt(40, 120, "• 做法：守株待兔，用盖革/液闪计数器等 ¹⁴C 自己衰变", size=11, color=BODY))
    el.append(txt(40, 142, f"• 痛点：1 mg 古碳每 {hours_per_decay:.1f} 小时才蹦出 1 个电子！效率极低", size=11, color=WARM_RED, weight="600"))
    el.append(txt(40, 164, "• 代价：必须烧毁 1～10 克木炭/骨骼，屏蔽宇宙射线测数天", size=11, color=BODY))
    el.append(txt(40, 186, "  （珍贵丝绸、字画、单粒种子根本舍不得烧！）", size=10.5, color=MUTED))

    el.append(card(384, 68, 352, 152, fill="#ffffff", stroke=BLUE, sw=1.4))
    el.append(pill(400, 82, "现代王牌：加速器质谱法 AMS（灵敏度升百万倍）", fg=BLUE, bg=BLUE_SOFT, w=318, size=11.5))
    el.append(txt(400, 120, "• 思路逆转：不等它衰变，把样品电离加速，直接数 ¹⁴C 原子！", size=11, color=INK, weight="700"))
    el.append(txt(400, 142, "• 用量骤降：仅需 0.5～1 毫克碳（几粒炭屑、一根毛发、一粒稻谷）", size=11, color=GREEN, weight="700"))
    el.append(txt(400, 164, "• 速度飞跃：几十分钟即可数出上万颗 ¹⁴C 离子，精度达 ±20–30 年", size=11, color=BODY))
    el.append(txt(400, 186, "• 但它必须连闯“三大冒牌货关卡”（空气里全是同体重的 ¹⁴N！）", size=10.5, color=ORANGE, weight="600"))

    # Bottom Pipeline Card: How AMS eliminates 14N and 13CH in 3 physical stages
    el.append(card(24, 234, 712, 214, fill="#ffffff"))
    el.append(txt(42, 258, "AMS 三关筛出“一万亿分之一”真身：怎样剔除体重几乎一模一样的氮-14 (¹⁴N) 与氢化物分子 (¹³CH)？", size=12, color=INK, weight="700"))

    # Stage 1 Box
    el.append(card(40, 274, 206, 154, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.3))
    el.append(step_badge(58, 294, 1, fg=ORANGE, bg="#ffffff"))
    el.append(txt(76, 298, "铯束轰击制负离子 C⁻", size=12, color=ORANGE, weight="700"))
    el.append(txt(52, 322, "样品还原成约 0.5 mg 石墨靶，", size=10.5, color=BODY))
    el.append(txt(52, 340, "用铯离子轰出带负电的碳离子 C⁻。", size=10.5, color=BODY))
    el.append(card(52, 354, 182, 60, rx=6, fill="#ffffff", stroke=ORANGE))
    el.append(txt(143, 375, "第一关秒杀：淘汰氮-14！", size=11, color=WARM_RED, anchor="middle", weight="700"))
    el.append(txt(143, 395, "¹⁴N 虽占空气78%，但无法形成", size=10, color=BODY, anchor="middle"))
    el.append(txt(143, 408, "稳定负离子 N⁻，当场出局！", size=10, color=BODY, anchor="middle"))

    el.append(_arrow(250, 351, 272, 351, color=ORANGE, sw=2.2, marker="arr-orange"))

    # Stage 2 Box
    el.append(card(276, 274, 210, 154, rx=8, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.3))
    el.append(step_badge(294, 294, 2, fg=PURPLE, bg="#ffffff"))
    el.append(txt(312, 298, "百万伏加速 + 剥离碎分子", size=12, color=PURPLE, weight="700"))
    el.append(txt(288, 322, "高压电场把 C⁻ 加速到约数千 km/s", size=10.5, color=BODY))
    el.append(txt(288, 340, "穿过气体/薄膜剥离器扯掉外层电子。", size=10.5, color=BODY))
    el.append(card(288, 354, 186, 60, rx=6, fill="#ffffff", stroke=PURPLE))
    el.append(txt(381, 375, "第二关秒杀：炸碎 ¹³CH / ¹²CH₂！", size=11, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(381, 395, "凑够质量14的冒牌分子失去成键", size=10, color=BODY, anchor="middle"))
    el.append(txt(381, 408, "电子后瞬间解体，仅剩纯 C³⁺！", size=10, color=BODY, anchor="middle"))

    el.append(_arrow(490, 351, 512, 351, color=BLUE, sw=2.2, marker="arr-blue"))

    # Stage 3 Box
    el.append(card(516, 274, 204, 154, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.3))
    el.append(step_badge(534, 294, 3, fg=BLUE, bg="#ffffff"))
    el.append(txt(552, 298, "强磁场偏转 · 逐颗点名", size=12, color=BLUE, weight="700"))
    el.append(txt(528, 322, "磁场按质量把三种碳弯成三条轨道：", size=10.5, color=BODY))
    # Mini 3-track deflection illustration
    el.append(_curve("M532,352 Q582,350 618,336", color=SLATE, sw=1.6))
    el.append(txt(624, 339, "¹²C (最轻弯最急)", size=10, color=SLATE))
    el.append(_curve("M532,358 Q585,358 622,356", color=GREEN, sw=1.6))
    el.append(txt(628, 360, "¹³C (法拉第杯测)", size=10, color=GREEN))
    el.append(_curve("M532,364 Q588,368 622,380", color=WARM_RED, sw=2.2))
    el.append(txt(628, 384, "¹⁴C (探测器逐颗数!)", size=10, color=WARM_RED, weight="700"))
    el.append(txt(528, 412, "直接算出 ¹⁴C / ¹²C 精确原子个数比！", size=10.5, color=INK, weight="700"))

    svg = figure(
        h,
        "传统β衰变计数法与现代加速器质谱仪AMS原理对比图",
        "上方对比1949年利比衰变计数法（需数克样品苦等每2.4小时一次的衰变）与现代AMS（仅需0.5至1毫克样品直接数出数千万个碳十四原子）；下方拆解AMS三道关卡：①铯离子源制取负离子C⁻直接淘汰无法形成稳定负离子的氮-14；②高压加速穿剥离膜炸碎¹³CH与¹²CH₂干扰分子；③强磁场按质量分道逐颗计数¹⁴C。",
        el,
    )
    write_svg("isotopes-c14", "geiger-vs-ams-revolution.svg", svg)


def _build_calibration_suess_bomb_pulse():
    """Fig 6: Why atmospheric C-14 wasn't constant: Tree-ring IntCal20, Suess fossil-fuel dilution, & 1963 Bomb Pulse."""
    h = 504
    el = []
    el.extend(
        header(
            "碳十四时钟的“三大剧情反转”：树轮校准、化石燃料铁证与 1963 核爆脉冲",
            "大气 ¹⁴C 并非一成不变——修正误差后，它不仅测得更准，还跨界成了气候取证与法医鉴伪神器！",
        )
    )

    # Left Column: Two stacked cards (Tree-ring IntCal20 + Suess Fossil Fuel Effect)
    # Card A: Tree-ring calibration IntCal20 (x=24, y=68, w=336, h=198)
    el.append(card(24, 68, 336, 198, fill="#ffffff"))
    el.append(step_badge(44, 90, 1, fg=GREEN, bg=GREEN_SOFT))
    el.append(txt(62, 94, "反转一：太阳与地磁场波动 → 树轮标尺校准", size=12.5, color=INK, weight="700"))
    el.append(txt(42, 120, "• 宇宙射线强弱随地磁场与太阳活动波动几个百分点", size=11, color=BODY))
    el.append(txt(42, 141, "• 科学家用长寿刺果松、古橡木一圈一圈重叠拼接，建起", size=11, color=BODY))
    el.append(txt(42, 160, "  连续 14,000 年树轮账本（结合石笋珊瑚达 5.5 万年：IntCal20）", size=10.5, color=GREEN, weight="700"))
    el.append(card(42, 174, 300, 76, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(54, 195, "考古采样铁律（以三星堆为例）：", size=11, color=WARM_RED, weight="700"))
    el.append(txt(54, 214, "青铜器不含碳不能直接测！北大团队专挑坑内“短寿命碳化", size=10.5, color=BODY))
    el.append(txt(54, 233, "竹屑/种子”测 200+ 份，避开百年老树心“老木头偏老误差”。", size=10.5, color=BODY))

    # Card B: Suess Effect - Fossil Fuels dilute 14C (x=24, y=280, w=336, h=202)
    el.append(card(24, 280, 336, 202, fill="#ffffff"))
    el.append(step_badge(44, 302, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(62, 306, "反转二：苏斯效应 → 锁定人类烧煤排碳的铁证", size=12.5, color=INK, weight="700"))
    el.append(txt(42, 332, "• 煤炭、石油埋藏上亿年，里面的 ¹⁴C 早已 100% 死光！", size=11, color=BODY))
    el.append(txt(42, 353, "• 19 世纪末工业革命以来，大量“零 ¹⁴C 化石碳”排入天空，", size=11, color=BODY))
    el.append(txt(42, 372, "  把大气 ¹⁴C 浓度冲淡了（1900 年的木头测出来反而显老！）", size=10.5, color=ORANGE, weight="600"))
    el.append(card(42, 388, 300, 78, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.1))
    el.append(txt(54, 410, "意外立大功（NOAA 温室气体溯源核心证据）：", size=11, color=ORANGE, weight="700"))
    el.append(txt(54, 430, "正是大气 CO₂ 暴涨同时 Δ¹⁴C 与 δ¹³C 双双下降，铁证如山", size=10.5, color=BODY))
    el.append(txt(54, 449, "地证明新增 CO₂ 来自人类燃烧化石燃料，而非海洋释放！", size=10.5, color=INK, weight="600"))

    # Right Column: The 1955-1963 Nuclear Bomb Pulse Chart & Forensics (x=376, y=68, w=360, h=414)
    el.append(card(376, 68, 360, 414, fill="#ffffff"))
    el.append(step_badge(396, 90, 3, fg=WARM_RED, bg=RED_SOFT))
    el.append(txt(414, 94, "反转三：1963“核爆脉冲”变身现代鉴伪神尺", size=12.5, color=INK, weight="700"))
    el.append(txt(394, 118, "大气核试验瞬间让北半球 ¹⁴C 暴涨近一倍（Δ¹⁴C ‰，据 NOAA）：", size=10.5, color=MUTED))

    # Bomb pulse mini-plot (1950 -> 2025, y from -50‰ to +1000‰)
    px0, px1 = 426.0, 716.0
    py_top, py_bot = 136.0, 312.0

    def bx(yr):
        return px0 + (yr - 1950.0) / (2025.0 - 1950.0) * (px1 - px0)

    def by(permil):
        return py_bot - (permil - (-60.0)) / (1040.0 - (-60.0)) * (py_bot - py_top)

    # Grid & axes
    for pm in (0, 250, 500, 750, 1000):
        yy = by(pm)
        el.append(_curve(f"M{px0:.1f},{yy:.1f} L{px1:.1f},{yy:.1f}", color=HAIRLINE if pm else SLATE, sw=0.9, dash="3 3" if pm else None))
        el.append(txt(px0 - 6, yy + 4, f"+{pm}‰" if pm > 0 else "0‰", size=10, color=SLATE, anchor="end", cls="mono"))

    for yr in (1950, 1963, 1980, 2000, 2020):
        xx = bx(yr)
        el.append(f'<line x1="{xx:.1f}" y1="{py_bot:.1f}" x2="{xx:.1f}" y2="{py_bot + 4:.1f}" stroke="{SLATE}"/>')
        el.append(txt(xx, py_bot + 16, str(yr), size=10, color=WARM_RED if yr == 1963 else SLATE, anchor="middle", weight="700" if yr == 1963 else None, cls="mono"))

    # Northern Hemisphere Bomb Spike curve (representative NOAA GML trajectory)
    nh_data = [
        (1950, -20), (1954, -22), (1956, 45), (1958, 160), (1959, 290),
        (1961, 240), (1962, 430), (1963.6, 940), (1965, 760), (1968, 560),
        (1972, 430), (1976, 330), (1980, 260), (1985, 195), (1990, 145),
        (1995, 108), (2000, 82), (2005, 58), (2010, 38), (2015, 18),
        (2020, 0), (2024, -14),
    ]
    sh_data = [
        (1950, -20), (1955, -18), (1959, 140), (1962, 230), (1965.0, 650),
        (1968, 540), (1972, 420), (1980, 255), (1990, 142), (2000, 80),
        (2010, 38), (2020, 2), (2024, -12),
    ]
    nh_d = "M" + " L".join(f"{bx(y):.1f},{by(v):.1f}" for y, v in nh_data)
    sh_d = "M" + " L".join(f"{bx(y):.1f},{by(v):.1f}" for y, v in sh_data)
    el.append(_curve(sh_d, color=BLUE, sw=1.9, dash="5 3"))
    el.append(_curve(nh_d, color=WARM_RED, sw=2.6))

    # Peak annotation at 1963.6
    pk_x, pk_y = bx(1963.6), by(940)
    el.append(f'<circle cx="{pk_x:.1f}" cy="{pk_y:.1f}" r="3.8" fill="{WARM_RED}" stroke="#fff" stroke-width="1"/>')
    el.append(txt(pk_x + 8, pk_y + 4, "1963 禁试条约生效（北半球峰值近翻倍！）", size=10, color=WARM_RED, weight="700", halo=True))
    el.append(txt(bx(1981), by(560), "海洋与森林快速吸走核爆 ¹⁴C", size=10, color=SLATE, halo=True))
    el.append(txt(bx(1966), by(350), "南半球（滞后约1年）", size=9.8, color=BLUE, weight="600", halo=True))

    # Three modern forensic superpowers box
    el.append(card(392, 338, 328, 128, rx=8, fill=RED_SOFT, stroke=WARM_RED, sw=1.1))
    el.append(txt(404, 359, "1955 年后每一年浓度都不同 → 精确到“哪一年生”：", size=11, color=WARM_RED, weight="700"))
    el.append(txt(404, 380, "① 抓假陈年名酒/假字画：标称 1945 年红酒若含核爆 ¹⁴C 必假！", size=10.5, color=BODY))
    el.append(txt(404, 400, "② 抓盗猎象牙：一测象牙尖端 ¹⁴C，立判大象死于禁贸令前或后", size=10.5, color=BODY))
    el.append(txt(404, 420, "③ 测人体细胞生日：牙釉质与大脑皮层神经元 DNA 保留你出生", size=10.5, color=BODY))
    el.append(txt(404, 439, "   那年的核爆 ¹⁴C（终身几乎不换），肠道上皮细胞仅几岁年轻！", size=10.5, color=INK, weight="600"))

    svg = figure(
        h,
        "碳十四树轮校准IntCal20、化石燃料苏斯效应与1963核爆脉冲应用图",
        "左栏上方说明宇宙射线波动与14000年树轮校准曲线IntCal20及三星堆短寿命竹屑取样原则；左栏下方说明化石燃料不含碳十四稀释大气（苏斯效应），成为人类排放二氧化碳的铁证；右栏绘出1950至2024年大气核试验引发的1963核爆碳十四尖峰及其在名酒字画鉴伪、盗猎象牙取证与人体细胞年龄测定中的跨界应用。",
        el,
    )
    write_svg("isotopes-c14", "calibration-suess-bomb-pulse.svg", svg)


@register(
    "isotopes-c14",
    "Isotopes physics, stable vs radioactive tracers & Carbon-14 AMS dating",
    "Atomic & Nuclear Science",
)
def build_isotopes_c14():
    _build_carbon_triplet_isotopes()
    _build_stable_vs_radio_detectives()
    _build_c14_cosmic_cycle()
    _build_c14_decay_curve()
    _build_geiger_vs_ams_revolution()
    _build_calibration_suess_bomb_pulse()
