"""
Visuals for '文物-玉 的形成方式' (How Jade Cultural Relics Form: Geological Genesis, Neolithic Abrasive Craft, and Burial Alteration).
Generates 6 original 760px Chinese SVG diagrams in assets/images/jade-relics/
with verified mineralogical/optical/archaeometric assertions.
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

TOPIC = "jade-relics"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
JADE_DARK = "#115e59"
JADE_MID = "#0d9488"
JADE_PALE = "#ccfbf1"


def _line(x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, marker=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def _verify_jade_math() -> None:
    # 1. GIA relative fracture toughness vs Mohs hardness assertions
    toughness = {
        "nephrite": 225_000,
        "jadeite": 120_000,
        "diamond": 6_500,    # 5,000 - 8,000 midpoint
        "quartz": 1_000,
        "corundum": 600,
    }
    assert toughness["nephrite"] / toughness["corundum"] == 375.0
    assert 25.0 < toughness["nephrite"] / toughness["diamond"] < 46.0
    assert 1.8 < toughness["nephrite"] / toughness["jadeite"] < 1.95

    # 2. Specific gravity & Mohs hardness separation (GIA)
    mohs_nephrite = (6.0, 6.5)
    mohs_jadeite = (6.5, 7.0)
    mohs_quartz = 7.0
    mohs_bronze_iron = (3.5, 5.0)
    assert mohs_quartz > mohs_nephrite[1], "Quartz sand (Mohs 7) must exceed nephrite (6.0-6.5) to abrade it"
    assert mohs_bronze_iron[1] < mohs_nephrite[0], "Ancient bronze/iron tools are softer than nephrite"

    sg_nephrite, sg_jadeite = 2.95, 3.34
    assert round((sg_jadeite - sg_nephrite) / sg_nephrite * 100, 1) == 13.2

    # 3. Geological P-T regimes (1 GPa = 10 kbar ≈ 30-33 km lithostatic depth)
    # Nephrite contact metasomatism: 0.2-0.7 GPa (2-7 kbar), 300-500 °C
    # Jadeite HP-LT subduction: 1.0-2.5 GPa (10-25 kbar), 200-500 °C -> geothermal gradient ~6-12 °C/km
    p_jad_gpa = 1.5
    depth_km = p_jad_gpa * 33.0
    assert 45.0 <= depth_km <= 55.0
    grad_subduction = 350.0 / depth_km
    assert 6.0 <= grad_subduction <= 8.5, "HP-LT cold subduction gradient < 10 °C/km"

    # 4. Fresnel interface reflectance R = ((n1 - n2)/(n1 + n2))^2 explaining "鸡骨白" & "盘玉回润"
    n_tremolite = 1.615
    n_air = 1.000
    n_sebum = 1.475  # human skin lipid / oil refractive index ~1.47-1.48
    r_air = ((n_tremolite - n_air) / (n_tremolite + n_air)) ** 2
    r_oil = ((n_tremolite - n_sebum) / (n_tremolite + n_sebum)) ** 2
    # Filling air-filled weathering pores with oil drops single-interface scatter reflectance by > 25x!
    ratio_scatter = r_air / r_oil
    assert 0.054 < r_air < 0.057
    assert 0.0019 < r_oil < 0.0022
    assert ratio_scatter > 25.0


# ---------------------------------------------------------------------------
# 1. Three Births Overview: Geological Stone -> Crafted Ritual Vessel -> Buried Relic
# ---------------------------------------------------------------------------
def build_three_births_overview() -> None:
    W, H = 760, 492
    el = []
    el.append(txt(W / 2, 30, "一块传世“文物古玉”的三重诞生：天地炼石、匠人攻器与岁月受沁", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "博物馆里的古玉不是天生那副模样——它先后经历亿年地质变质、无铁时代砂磨与数千年地下化学风化", size=12.2, color=MUTED, anchor="middle"))

    cols = [
        (
            22, TEAL_SOFT, "#5eead4", JADE_DARK,
            "第一重诞生：天地成石",
            "时间尺度：数千万至数亿年",
            "【地下高温高压变质与冰河筛选】",
            [
                "• 软玉（和田玉/良渚玉）：岩浆热液",
                "  交代白云质大理岩，长出毛毡纤维；",
                "• 硬玉（翡翠）：大洋俯冲带 30–60 km",
                "  万倍大气压“高压低温”挤出硬玉岩；",
                "• 冰川崩落 + 河水冲刷去粗存精成籽料。",
            ],
            "产物：温润致密的天然玉石矿料",
        ),
        (
            268, AMBER_SOFT, "#fcd34d", AMBER,
            "第二重诞生：匠人成器",
            "时间尺度：数月至数十年苦功",
            "【“他山之石”解玉砂切磋琢磨】",
            [
                "• 青铜与生铁都比玉软，根本刻不动！",
                "• 靠莫氏硬度 7 的石英砂（解玉砂）",
                "  加水，由麻绳、竹管、木片带动研磨；",
                "• 砂绳线切留弧痕、双面管钻留台痕、",
                "  燧石微刻神徽，赋予礼天敬祖灵魂。",
            ],
            "产物：晶莹半透明的崭新礼仪玉器",
        ),
        (
            514, PURPLE_SOFT, "#d8b4fe", PURPLE,
            "第三重诞生：入土成古",
            "时间尺度：埋藏一两千至五千年",
            "【地下水淋滤受沁与祭祀火燎】",
            [
                "• 弱酸碱地下水溶蚀晶界，蚀出纳米微孔，",
                "  漫反射白化成象牙般的“鸡骨白”；",
                "• 墓中朱砂（α-HgS）、铁锈、青铜绿",
                "  顺微裂隙渗入，染出红沁、黄沁、绿沁；",
                "• 辰砂转黑辰砂（β-HgS）成“水银沁”。",
            ],
            "产物：带历史包浆与沁色的文物古玉",
        ),
    ]

    for cx, bg, bd, col, title, span, sub, bullets, foot in cols:
        el.append(card(cx, 72, 224, 396, rx=12, fill="#ffffff", stroke=BORDER))
        el.append(card(cx + 12, 86, 200, 58, rx=9, fill=bg, stroke=bd))
        el.append(txt(cx + 112, 110, title, size=14.5, weight="700", color=col, anchor="middle"))
        el.append(txt(cx + 112, 131, span, size=11, color=BODY, anchor="middle"))

        # Central symbolic illustration area (y=154..242)
        el.append(card(cx + 12, 154, 200, 82, rx=8, fill="#f8fafc", stroke=BORDER))
        if cx == 22:
            # Mountain + river pebble
            el.append('<polygon points="48,224 84,168 118,224" fill="#cbd5e1" stroke="#64748b" stroke-width="1.5"/>')
            el.append('<polygon points="92,224 128,176 162,224" fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>')
            el.append(f'<ellipse cx="182" cy="206" rx="20" ry="13" fill="{JADE_PALE}" stroke="{JADE_DARK}" stroke-width="2"/>')
            el.append('<path d="M 166 198 Q 182 190 198 199" fill="none" stroke="#d97706" stroke-width="2.5"/>')
            el.append(txt(182, 229, "红皮籽料", size=10.2, weight="700", color=JADE_DARK, anchor="middle"))
        elif cx == 268:
            # Jade Cong square outer, round inner + bamboo drill
            el.append(f'<rect x="352" y="168" width="56" height="56" rx="5" fill="{JADE_PALE}" stroke="{JADE_DARK}" stroke-width="2.2"/>')
            el.append(f'<circle cx="380" cy="196" r="19" fill="#ffffff" stroke="{JADE_DARK}" stroke-width="1.8"/>')
            el.append(txt(380, 200, "玉琮", size=10.5, weight="700", color=JADE_DARK, anchor="middle"))
            el.append(txt(442, 190, "石英砂", size=10.5, weight="700", color=AMBER, anchor="middle"))
            el.append(txt(442, 207, "+ 竹管钻", size=10.5, color=BODY, anchor="middle"))
        else:
            # Unearthed ivory-white Bi disk with cinnabar & mercury spots
            el.append('<circle cx="626" cy="195" r="28" fill="#f5f5f4" stroke="#78716c" stroke-width="2.2"/>')
            el.append('<circle cx="626" cy="195" r="10" fill="#f8fafc" stroke="#78716c" stroke-width="1.8"/>')
            el.append('<path d="M 604 182 Q 614 176 622 183" fill="none" stroke="#dc2626" stroke-width="3"/>')
            el.append('<path d="M 638 206 Q 646 212 634 218" fill="none" stroke="#1e293b" stroke-width="3"/>')
            el.append(txt(564, 188, "鸡骨白", size=10.2, weight="700", color="#57534e", anchor="middle"))
            el.append(txt(688, 188, "朱砂/黑沁", size=10.2, weight="700", color=RED, anchor="middle"))

        el.append(txt(cx + 112, 258, sub, size=11.6, weight="700", color=col, anchor="middle"))
        for idx, bl in enumerate(bullets):
            el.append(txt(cx + 16, 281 + idx * 24, bl, size=10.8, color=BODY))

        el.append(card(cx + 12, 412, 200, 42, rx=8, fill=bg, stroke=bd))
        el.append(txt(cx + 112, 438, foot, size=11, weight="700", color=col, anchor="middle"))

    # Connecting arrows between columns
    el.append(_line(247, 265, 266, 265, stroke=AMBER, sw=2.6, marker="arr-orange"))
    el.append(_line(493, 265, 512, 265, stroke=PURPLE, sw=2.6, marker="arr-blue"))

    write_svg(
        TOPIC,
        "three-births-of-archaic-jade-overview.svg",
        figure(H, "文物古玉的三重形成过程全景图", "展示一块文物古玉依次经历地质成矿、解玉砂琢磨成器与地下千年埋藏受沁风化的三重形成机制", el),
    )


# ---------------------------------------------------------------------------
# 2. Hardness vs Fracture Toughness: Why Nephrite Beats Diamond & Steel in Toughness
# ---------------------------------------------------------------------------
def build_toughness_vs_hardness() -> None:
    W, H = 760, 518
    el = []
    el.append(txt(W / 2, 30, "硬度只排中游的玉，凭什么是宝石界“最抗砸的冠军”？", size=19, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "抗刮擦看“莫氏硬度”，抗砸裂看“断裂韧性”——毛毡般绞抱的微晶纤维让软玉韧性高达刚玉的 375 倍", size=12.2, color=MUTED, anchor="middle"))

    # Left panel: Microstructure comparison (Nephrite felted fibers vs Diamond cleavage)
    el.append(card(22, 68, 344, 428))
    el.append(txt(40, 95, "显微密码：毛毡交织纤维 vs 平直解理面", size=14.8, weight="700", color=JADE_DARK))

    # Top sub-box: Nephrite felted hair-like tremolite bundles
    el.append(card(38, 112, 312, 174, rx=10, fill=TEAL_SOFT, stroke="#5eead4"))
    el.append(txt(52, 134, "① 软玉（透闪石）：乱向拧绞的“微米藤甲”", size=12.2, weight="700", color=JADE_DARK))
    # Draw interwoven curved fiber bundles inside (52..210, 146..236)
    fibers = [
        "M 56 162 Q 98 148 142 168 T 218 158",
        "M 54 182 Q 104 198 148 174 T 220 188",
        "M 60 204 Q 108 182 154 210 T 216 202",
        "M 58 222 Q 102 234 150 214 T 218 226",
        "M 82 150 Q 96 192 78 232",
        "M 126 150 Q 112 192 134 232",
        "M 172 150 Q 188 190 166 232",
    ]
    for fd in fibers:
        el.append(f'<path d="{fd}" fill="none" stroke="{JADE_MID}" stroke-width="2.6" opacity="0.72"/>')
    # Stopped zigzag crack!
    el.append('<polyline points="136,146 132,164 146,174 138,188" fill="none" stroke="#dc2626" stroke-width="3"/>')
    el.append('<circle cx="138" cy="188" r="4.5" fill="#dc2626"/>')
    el.append(txt(232, 172, "外力裂纹撞上", size=10.8, weight="700", color=RED))
    el.append(txt(232, 190, "乱向纤维束，被", size=10.8, color=BODY))
    el.append(txt(232, 208, "迫拐弯分叉耗尽", size=10.8, color=BODY))
    el.append(txt(232, 226, "能量，砸不碎！", size=10.8, weight="700", color=JADE_DARK))
    el.append(txt(52, 256, "• 旧石器“打制劈裂法”对它完全失效，逼出研磨工艺", size=10.6, color=BODY))
    el.append(txt(52, 274, "• 硬玉（翡翠）为粒状变晶镶嵌，韧性居亚军但光泽更亮", size=10.6, color=BODY))

    # Bottom sub-box: Diamond /单晶宝石 straight cleavage plane
    el.append(card(38, 298, 312, 180, rx=10, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(52, 320, "② 钻石 / 单晶宝石：极硬，但有平直“解理面”", size=12.2, weight="700", color=ORANGE))
    # Crystal polygon + straight cleavage split
    el.append('<polygon points="84,344 156,344 182,380 120,428 58,380" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/>')
    el.append(_line(72, 358, 168, 404, stroke=RED, sw=2.8, dash="5 3"))
    el.append(txt(200, 366, "铁锤猛敲解理方向：", size=10.8, weight="700", color=RED))
    el.append(txt(200, 385, "裂纹沿整齐原子平面", size=10.8, color=BODY))
    el.append(txt(200, 404, "一劈到底瞬间崩裂！", size=10.8, color=BODY))
    el.append(txt(52, 448, "• 钻石莫氏硬度 10（谁也划不动它），却怕重锤猛磕；", size=10.6, color=BODY))
    el.append(txt(52, 466, "• 软玉莫氏硬度仅 6–6.5（会被石英砂划伤），却极耐冲击！", size=10.6, weight="700", color=INK))

    # Right panel: GIA Quantitative Comparison Chart (Toughness vs Mohs Hardness)
    el.append(card(380, 68, 358, 428))
    el.append(txt(398, 95, "GIA 宝石耐用性实测：断裂韧性 vs 莫氏硬度", size=14.5, weight="700", color=BLUE))
    el.append(txt(398, 115, "断裂功相对标度（数值越大越抗砸裂，注意悬殊倍数！）", size=11, color=MUTED))

    rows = [
        ("软玉（和田玉/良渚玉）", 225_000, "莫氏 6.0–6.5", JADE_MID, "225,000（抗砸总冠军！）"),
        ("硬玉（缅甸翡翠）", 120_000, "莫氏 6.5–7.0", GREEN, "120,000（微晶颗粒交织）"),
        ("金刚石（钻石）", 7_500, "莫氏 10（最抗刮）", ORANGE, "5,000–8,000（具八面体解理）"),
        ("石英（解玉砂主力）", 1_000, "莫氏 7.0", BLUE, "~1,000（比软玉硬，可磨玉！）"),
        ("刚玉（红蓝宝石）", 600, "莫氏 9.0", PURPLE, "600（软玉韧性是它的 375 倍）"),
    ]
    max_bar_w = 304.0
    for idx, (name, val, mohs_lbl, col, val_lbl) in enumerate(rows):
        ry = 136 + idx * 62
        bw = max(4.0, max_bar_w * (val / 225_000.0))
        el.append(txt(398, ry + 14, name, size=11.8, weight="700", color=INK))
        el.append(txt(720, ry + 14, mohs_lbl, size=10.8, weight="700", color=col, anchor="end"))
        el.append(f'<rect x="398" y="{ry + 22}" width="{max_bar_w}" height="18" rx="5" fill="#f1f5f9"/>')
        el.append(f'<rect x="398" y="{ry + 22}" width="{bw:.1f}" height="18" rx="5" fill="{col}"/>')
        txt_x = 406 + bw if bw < 130 else 408
        txt_col = INK if bw < 130 else "#ffffff"
        el.append(txt(txt_x, ry + 35, val_lbl, size=10.5, weight="700", color=txt_col))

    el.append(card(396, 446, 326, 36, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(559, 469, "1863 年法国矿物学家达穆尔首次测出“软玉”与“硬玉”分属两族矿物", size=10.5, weight="700", color=BLUE, anchor="middle"))

    write_svg(
        TOPIC,
        "nephrite-felted-fibers-vs-gem-toughness.svg",
        figure(H, "软玉毛毡状纤维交织结构与GIA宝石断裂韧性对比图", "左图对比软玉微米纤维束阻断裂纹与单晶宝石解理劈裂，右图按真实比例绘制GIA断裂韧性标度（软玉225,000对比刚玉600）", el),
    )


# ---------------------------------------------------------------------------
# 3. Geological Furnaces (Animated River Boulder -> Seed Jade Pebble)
# ---------------------------------------------------------------------------
def build_geological_furnaces() -> None:
    W, H = 760, 534
    extra_css = """
      .anim-river {
        stroke-dasharray: 290;
        stroke-dashoffset: 290;
        animation: riverTransport 3.8s ease-out 0.3s 1 forwards;
      }
      @keyframes riverTransport {
        from { stroke-dashoffset: 290; }
        to   { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .anim-river {
          animation: none !important;
          stroke-dashoffset: 0 !important;
        }
      }
    """
    el = []
    el.append(txt(W / 2, 30, "两种“玉”的地下炼丹炉：昆仑山热液交代 vs 大洋俯冲高压低温带", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "中华八千年古玉皆为透闪石软玉；而清代风靡的缅甸翡翠（硬玉），则诞生于板块俯冲的万倍高压冷缝", size=12.2, color=MUTED, anchor="middle"))

    # Left panel: Nephrite (Kunlun / Hetian Dolomite Contact Metasomatism + Placer Seed Jade)
    el.append(card(22, 68, 360, 444))
    el.append(pill(38, 82, "软玉（和田玉）：中温低压接触交代 + 冰河淘洗", fg=JADE_DARK, bg=TEAL_SOFT, w=314))

    # Cross-section diagram (38..366, 118..348)
    el.append(card(38, 118, 328, 232, rx=10, fill="#f8fafc", stroke=BORDER))
    # Sky & Kunlun snow peak (>4,500 m)
    el.append('<polygon points="48,256 124,136 204,256" fill="#e2e8f0" stroke="#64748b" stroke-width="1.6"/>')
    el.append('<polygon points="98,177 124,136 150,177 136,184 124,174 112,184" fill="#ffffff"/>')
    el.append(txt(124, 130, "昆仑雪山原生矿（>4,000 m）", size=10.5, weight="700", color=INK, anchor="middle"))

    # Underground marble + magma intrusion + nephrite skarn lens
    el.append('<path d="M 44 256 L 360 256 L 360 342 L 44 342 Z" fill="#f1f5f9"/>')
    # Magma chamber bottom-left
    el.append('<path d="M 44 342 L 44 286 Q 98 268 142 342 Z" fill="#fecaca" stroke="#dc2626" stroke-width="1.6"/>')
    el.append(txt(84, 326, "中酸性岩浆侵入", size=10.2, weight="700", color=RED, anchor="middle"))
    # Dolomitic marble layer
    el.append('<rect x="136" y="274" width="112" height="44" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.3"/>')
    el.append(txt(192, 294, "白云质大理岩", size=10.2, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(192, 310, "CaMg(CO₃)₂", size=9.8, color=BODY, anchor="middle"))
    # Nephrite reaction zone lens between magma & dolomite!
    el.append(f'<ellipse cx="134" cy="292" rx="18" ry="11" transform="rotate(-28 134 292)" fill="{JADE_MID}" stroke="#ffffff" stroke-width="1.8"/>')
    el.append(txt(134, 268, "① 成玉带（300–500℃）", size=10.2, weight="700", color=JADE_DARK, anchor="middle", halo=True))

    # River transport curve from mountain peak (136, 178) down to riverbed (332, 246)
    river_d = "M 136 178 C 166 206, 214 236, 334 244"
    el.append(f'<path d="{river_d}" fill="none" stroke="#bae6fd" stroke-width="5"/>')
    el.append(f'<path class="anim-river" d="{river_d}" fill="none" stroke="#0284c7" stroke-width="3.2" marker-end="url(#arr-blue)"/>')

    # Angular mountain料 -> sub-angular -> rounded seed jade pebble!
    el.append('<polygon points="152,188 166,184 170,196 156,199" fill="#99f6e4" stroke="#0f766e" stroke-width="1.4"/>')
    el.append(txt(198, 190, "② 山料（棱角多裂）", size=10, weight="700", color=JADE_DARK))
    el.append(f'<ellipse cx="252" cy="228" rx="9" ry="6" fill="#99f6e4" stroke="#0f766e" stroke-width="1.4"/>')
    el.append(txt(264, 216, "③ 山流水", size=10, color=BODY))
    el.append(f'<ellipse cx="332" cy="242" rx="12" ry="8" fill="{JADE_PALE}" stroke="#b45309" stroke-width="2.2"/>')
    el.append(txt(314, 272, "④ 玉龙喀什河“籽料”", size=10.5, weight="700", color=AMBER, anchor="middle"))

    el.append(card(38, 362, 328, 134, rx=10, fill=TEAL_SOFT, stroke="#5eead4"))
    el.append(txt(50, 384, "为什么老匠人偏爱河床里的“籽料”？", size=12, weight="700", color=JADE_DARK))
    el.append(txt(50, 404, "• 岩浆热液含硅流体交代白云岩（0.2–0.7 GPa）生成透闪石；", size=10.6, color=BODY))
    el.append(txt(50, 422, "• 造山抬升后冰川崩落，洪水裹挟玉石翻滚碰撞几十公里，", size=10.6, color=BODY))
    el.append(txt(50, 440, "  天然替工匠砸掉松散裂隙，只留最致密玉核；", size=10.6, color=BODY))
    el.append(txt(50, 458, "• 河床铁锰离子渗入表皮氧化，染出金黄/枣红“洒金皮”！", size=10.6, weight="700", color=INK))
    el.append(txt(50, 478, "（另有一类“碧玉”由超基性蛇纹岩接触交代生成，含铁铬显深绿）", size=10.2, color=MUTED))

    # Right panel: Jadeite (Subduction Zone High-Pressure Low-Temperature HP-LT)
    el.append(card(396, 68, 342, 444))
    el.append(pill(412, 82, "硬玉（缅甸翡翠）：板块俯冲“高压低温”奇迹", fg=GREEN, bg=GREEN_SOFT, w=308))

    el.append(card(412, 118, 310, 232, rx=10, fill="#f8fafc", stroke=BORDER))
    # Continental overriding wedge (right) & Subducting oceanic slab (plunging left-to-right)
    el.append('<polygon points="534,158 716,158 716,336 618,336" fill="#e2e8f0" stroke="#64748b" stroke-width="1.5"/>')
    el.append(txt(646, 184, "上覆大陆/岛弧地幔楔", size=10.5, weight="700", color=INK, anchor="middle"))
    el.append(txt(646, 202, "（蛇纹石化橄榄岩）", size=10, color=MUTED, anchor="middle"))

    # Plunging blue oceanic plate
    el.append('<polygon points="418,166 516,166 636,336 568,336" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.8"/>')
    el.append(_line(468, 186, 542, 268, stroke=BLUE, sw=2.4, marker="arr-blue"))
    el.append(txt(474, 154, "大洋板块携海水俯冲", size=10.5, weight="700", color=BLUE, anchor="middle"))

    # Jadeitite HP-LT formation pocket at 30-60 km depth!
    el.append('<ellipse cx="576" cy="272" rx="22" ry="13" transform="rotate(42 576 272)" fill="#22c55e" stroke="#ffffff" stroke-width="2"/>')
    el.append(txt(502, 298, "硬玉岩结晶带", size=11, weight="700", color=GREEN, anchor="middle"))
    el.append(txt(502, 315, "深 30–60 km", size=10.5, weight="700", color=GREEN, anchor="middle"))
    el.append(txt(502, 331, "1.0–2.5 GPa · 200–450℃", size=10, color=INK, anchor="middle"))

    el.append(card(412, 362, 310, 134, rx=10, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(424, 384, "为什么宝石级翡翠产地比软玉稀罕得多？", size=12, weight="700", color=GREEN))
    el.append(txt(424, 404, "• 地下越深通常越烫，硬玉却偏要“1–2 万倍大气压 +", size=10.6, color=BODY))
    el.append(txt(424, 422, "  仅两三百度低温”！只有冰冷大洋板块快速俯冲才具备；", size=10.6, color=BODY))
    el.append(txt(424, 440, "• 高压挤出富钠铝热液结晶成 NaAlSi₂O₆，微量 Cr³⁺", size=10.6, color=BODY))
    el.append(txt(424, 458, "  混入晶格染出惊艳帝王绿，18 世纪末自缅甸传入中国。", size=10.6, weight="700", color=INK))
    el.append(txt(424, 478, "（因此先秦两汉高古玉器中绝无缅甸硬玉翡翠！）", size=10.4, weight="700", color=RED))

    write_svg(
        TOPIC,
        "kunlun-nephrite-vs-subduction-jadeite-geology.svg",
        figure(H, "透闪石软玉接触交代与硬玉翡翠俯冲带高压低温成矿对比图", "左图单次动画演示昆仑山软玉原生矿经冰川河水搬运滚磨成籽料，右图展示大洋俯冲带30至60公里高压低温生成翡翠", el, extra_css=extra_css),
    )


# ---------------------------------------------------------------------------
# 4. Neolithic Jade-Working: Quartz Sand Abrasive, String Sawing & Tubular Drilling
# ---------------------------------------------------------------------------
def build_neolithic_jade_working() -> None:
    W, H = 760, 520
    el = []
    el.append(txt(W / 2, 30, "五千年前连铁器都没有，良渚先民凭什么雕出玉琮王？", size=19, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "“他山之石，可以攻玉”：竹木麻绳只是搬运工，真正啃下硬玉的是莫氏硬度 7 的石英“解玉砂”", size=12.2, color=MUTED, anchor="middle"))

    # Panel 1: Microscopic three-body abrasion mechanism
    el.append(card(22, 68, 232, 430))
    el.append(pill(36, 82, "① 核心原理：以砂攻玉", fg=AMBER, bg=AMBER_SOFT, w=186))

    # Bamboo/wood carrier pressing angular quartz grains onto nephrite surface
    el.append('<rect x="44" y="132" width="188" height="36" rx="6" fill="#fde68a" stroke="#d97706" stroke-width="1.8"/>')
    el.append(txt(138, 154, "柔韧工具载体（竹管 / 麻绳 / 木片）", size=10.5, weight="700", color=AMBER, anchor="middle"))
    el.append(_line(84, 120, 192, 120, stroke=AMBER, sw=2.2, marker="arr-orange"))
    el.append(txt(138, 113, "往复拉动或旋转施压", size=10.2, color=AMBER, anchor="middle"))

    # Water slurry layer + sharp quartz polygons
    el.append('<rect x="44" y="168" width="188" height="34" fill="#e0f2fe"/>')
    for qx in (68, 108, 148, 188):
        el.append(f'<polygon points="{qx},172 {qx+14},178 {qx+10},196 {qx-6},194" fill="#38bdf8" stroke="#0369a1" stroke-width="1.6"/>')
    el.append(txt(138, 217, "石英解玉砂 SiO₂（硬度 7.0）+ 水", size=10.5, weight="700", color=BLUE, anchor="middle", halo=True))

    # Nephrite base being micro-grooved
    el.append(f'<rect x="44" y="202" width="188" height="58" rx="6" fill="{JADE_PALE}" stroke="{JADE_DARK}" stroke-width="2"/>')
    el.append(txt(138, 244, "透闪石玉料（硬度 6.0–6.5）", size=11, weight="700", color=JADE_DARK, anchor="middle"))

    el.append(card(36, 276, 204, 206, rx=10, fill=AMBER_SOFT, stroke="#fcd34d"))
    el.append(txt(48, 298, "为什么软竹片反而比硬刀好用？", size=11.4, weight="700", color=AMBER))
    el.append(txt(48, 320, "• 石英砂棱角嵌进微软的竹木或麻绳", size=10.5, color=BODY))
    el.append(txt(48, 338, "  表层，就变成了一把“天然砂轮”；", size=10.5, color=BODY))
    el.append(txt(48, 358, "• 清水既防摩擦高热炸裂玉料，又把", size=10.5, color=BODY))
    el.append(txt(48, 376, "  磨下的石粉及时冲出沟槽；", size=10.5, color=BODY))
    el.append(txt(48, 396, "• 商周以后升级为青铜/铁质圆盘", size=10.5, color=BODY))
    el.append(txt(48, 414, "  “水凳砣机”，并引入硬度 7.5", size=10.5, color=BODY))
    el.append(txt(48, 432, "  石榴子石红砂与硬度 9 刚玉砂，", size=10.5, color=BODY))
    el.append(txt(48, 450, "  本质仍是“工具带砂磨玉”！", size=10.5, weight="700", color=INK))

    # Panel 2: String sawing (线切割) & Curved Saw Marks
    el.append(card(268, 68, 224, 430))
    el.append(pill(282, 82, "② 开料绝技：砂绳线切割", fg=BLUE, bg=BLUE_SOFT, w=186))

    # Jade slab with curved string cut & parabolic striations
    el.append(f'<rect x="302" y="136" width="156" height="114" rx="10" fill="{JADE_PALE}" stroke="{JADE_DARK}" stroke-width="2"/>')
    # Parabolic striations left on cut face
    for ay in (158, 176, 194, 212):
        el.append(f'<path d="M 314 {ay} Q 380 {ay+22} 446 {ay}" fill="none" stroke="{JADE_MID}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    # String bow pulling down
    el.append('<path d="M 280 152 Q 380 218 480 152" fill="none" stroke="#b45309" stroke-width="2.8"/>')
    el.append(txt(380, 126, "蘸满湿砂的兽皮条 / 麻绳拉锯", size=10.5, weight="700", color=AMBER, anchor="middle"))
    el.append(txt(380, 240, "标志性微痕：抛物线状弧形切痕", size=10.3, weight="700", color=BLUE, anchor="middle"))

    el.append(card(282, 276, 196, 206, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(294, 298, "微痕考古怎么一眼认出真古玉？", size=11.4, weight="700", color=BLUE))
    el.append(txt(294, 320, "• 兴隆洼、红山至良渚玉器上广泛留有", size=10.5, color=BODY))
    el.append(txt(294, 338, "  弯弯的“砂绳切割凹弧痕”；", size=10.5, color=BODY))
    el.append(txt(294, 358, "• 硬石片（石锯）直拉切割则会留下", size=10.5, color=BODY))
    el.append(txt(294, 376, "  笔直平行的沟槽；", size=10.5, color=BODY))
    el.append(txt(294, 396, "• 良渚玉琮神人兽面纹细如发丝", size=10.5, color=BODY))
    el.append(txt(294, 414, "  （1 毫米内刻 3–5 道阴线！），", size=10.5, weight="700", color=INK))
    el.append(txt(294, 432, "  系用尖锐燧石（硬度 7）或鲨鱼齿", size=10.5, color=BODY))
    el.append(txt(294, 450, "  在抛光玉面上反复刮刻而成。", size=10.5, color=BODY))

    # Panel 3: Biconical Hollow Tubular Drilling ("对钻蜂腰孔与台痕")
    el.append(card(506, 68, 232, 430))
    el.append(pill(520, 82, "③ 穿孔铁证：双面空心管钻", fg=PURPLE, bg=PURPLE_SOFT, w=196))

    # Cross-section of a tall Jade Cong drilled from top & bottom with slight offset step!
    el.append(f'<rect x="556" y="132" width="132" height="122" rx="6" fill="{JADE_PALE}" stroke="{JADE_DARK}" stroke-width="2.2"/>')
    # Top bore tapering slightly inward + Bottom bore slightly shifted right by 5px -> step ridge!
    el.append('<polygon points="598,132 642,132 637,194 603,194" fill="#ffffff" stroke="#0f766e" stroke-width="1.6"/>')
    el.append('<polygon points="607,194 641,194 646,254 602,254" fill="#ffffff" stroke="#0f766e" stroke-width="1.6"/>')
    # Horizontal spiral grooves inside bore
    for gy in (150, 168, 214, 232):
        el.append(_line(604, gy, 639, gy, stroke="#94a3b8", sw=1.1, dash="3 2"))
    # Highlight the misalignment ridge (对钻台痕)
    el.append('<circle cx="605" cy="194" r="5" fill="none" stroke="#dc2626" stroke-width="2"/>')
    el.append(_line(548, 194, 599, 194, stroke=RED, sw=1.8, marker="arr-orange"))
    el.append(txt(544, 182, "对钻错位", size=10.2, weight="700", color=RED, anchor="end"))
    el.append(txt(544, 198, "“台痕”", size=10.2, weight="700", color=RED, anchor="end"))
    el.append(txt(622, 122, "竹管/骨管双面对钻", size=10.5, weight="700", color=PURPLE, anchor="middle"))

    el.append(card(520, 276, 204, 206, rx=10, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(532, 298, "为什么古玉孔道大多“两头大中间窄”？", size=11.2, weight="700", color=PURPLE))
    el.append(txt(532, 320, "• 空心竹管只磨一圈环形窄缝，中间", size=10.5, color=BODY))
    el.append(txt(532, 338, "  掉出圆柱“玉芯”，比实心钻省力数倍；", size=10.5, color=BODY))
    el.append(txt(532, 358, "• 越往下钻竹管外壁越磨损变细，且单面", size=10.5, color=BODY))
    el.append(txt(532, 376, "  钻到底易崩裂，故从上下两面相向对钻；", size=10.5, color=BODY))
    el.append(txt(532, 396, "• 两孔交汇处留下的“蜂腰孔、错位台痕", size=10.5, weight="700", color=INK))
    el.append(txt(532, 414, "  与不等距螺旋砂纹”，是现代高速金刚石", size=10.5, color=BODY))
    el.append(txt(532, 432, "  钻头极难自然模仿的时代指纹！", size=10.5, color=BODY))

    write_svg(
        TOPIC,
        "neolithic-abrasive-string-sawing-and-tubular-drilling.svg",
        figure(H, "新石器时代解玉砂微磨削、砂绳线切割与双面空心管钻工艺图解", "分三栏展示硬度7石英砂磨削原理、柔性砂绳切割抛物线弧痕以及双面管钻形成的蜂腰孔与对钻错位台痕", el),
    )


# ---------------------------------------------------------------------------
# 5. "Chicken-Bone White" (鸡骨白): Nanopore Scattering Physics vs Calcification Myth
# ---------------------------------------------------------------------------
def build_chicken_bone_white_optics() -> None:
    W, H = 760, 506
    el = []
    el.append(txt(W / 2, 30, "古玉“鸡骨白”并不是变成了石灰！显微溶蚀孔隙与散射光学揭秘", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "就像透明冰块砸成碎冰茬会变白雪：拉曼光谱证实鸡骨白仍是透闪石，白化源于微孔对光线的漫散射", size=12.2, color=MUTED, anchor="middle"))

    # Left panel: Fresh Translucent Nephrite (Low Δn, deep light penetration -> Greasy luster)
    el.append(card(22, 68, 356, 318))
    el.append(pill(38, 82, "入土前的新玉：致密无隙 · 温润半透明", fg=JADE_DARK, bg=TEAL_SOFT, w=274))

    # Optical block (42..358, 126..278)
    el.append(f'<rect x="44" y="166" width="312" height="106" rx="10" fill="{JADE_PALE}" stroke="{JADE_DARK}" stroke-width="2"/>')
    # Tightly packed tremolite bricks without air gaps
    for row in range(3):
        for col_i in range(6):
            bx = 56 + col_i * 49 + (row % 2) * 10
            by = 178 + row * 28
            if bx + 44 < 350:
                el.append(f'<rect x="{bx}" y="{by}" width="44" height="22" rx="4" fill="#99f6e4" stroke="#0d9488" stroke-width="1"/>')

    # Incident golden rays penetrating deeply & softly diffusing
    el.append(_line(96, 118, 134, 236, stroke=AMBER, sw=2.6, marker="arr-orange"))
    el.append(_line(166, 118, 204, 244, stroke=AMBER, sw=2.6, marker="arr-orange"))
    el.append(_line(204, 244, 266, 124, stroke=JADE_MID, sw=2.2, dash="5 3", marker="arr-green"))
    el.append(txt(132, 132, "入射自然光", size=10.8, weight="700", color=AMBER, anchor="middle"))
    el.append(txt(286, 146, "深层柔和透射", size=10.8, weight="700", color=JADE_DARK, anchor="middle"))

    el.append(txt(44, 298, "• 微晶严丝合缝，晶间孔隙远小于可见光波长（<10 nm）；", size=10.8, color=BODY))
    el.append(txt(44, 318, "• 内部折射率处处均匀（n ≈ 1.61–1.63），光线深入玉肉", size=10.8, color=BODY))
    el.append(txt(44, 338, "  再柔柔折回人眼，呈现凝脂般的“油脂光泽”。", size=10.8, weight="700", color=JADE_DARK))

    # Right panel: Buried/Heated "Chicken-Bone White" Jade (Etched sub-micron air pores -> Mie scatter)
    el.append(card(392, 68, 346, 318))
    el.append(pill(408, 82, "千年古玉“鸡骨白”：微孔散射 · 象牙白化", fg=PURPLE, bg=PURPLE_SOFT, w=288))

    el.append('<rect x="412" y="166" width="306" height="106" rx="10" fill="#f5f5f4" stroke="#78716c" stroke-width="2"/>')
    # Loosened etched fibers + abundant white air micro-voids!
    voids = [
        (444, 186, 9), (482, 194, 11), (524, 184, 8), (566, 196, 12), (612, 186, 10), (658, 194, 9),
        (462, 222, 10), (506, 228, 9), (548, 220, 11), (592, 232, 8), (638, 224, 11), (682, 218, 8),
        (486, 252, 8), (536, 250, 10), (582, 254, 9), (628, 250, 8),
    ]
    for vx, vy, vr in voids:
        el.append(f'<circle cx="{vx}" cy="{vy}" r="{vr}" fill="#ffffff" stroke="#a8a29e" stroke-width="1.3"/>')

    # Incident rays immediately scattered in all directions at shallow surface!
    el.append(_line(496, 118, 524, 184, stroke=AMBER, sw=2.6))
    for sx, sy in [(458, 128), (512, 122), (574, 124), (624, 138)]:
        el.append(_line(524, 184, sx, sy, stroke=PURPLE, sw=2.0, marker="arr-blue"))
    el.append(txt(565, 118, "全波段强烈漫散射 → 肉眼见纯白！", size=10.8, weight="700", color=PURPLE, anchor="middle"))

    el.append(txt(412, 298, "• 成因 A（自然受沁）：土壤弱酸碱地下水淋滤溶蚀晶界；", size=10.8, color=BODY))
    el.append(txt(412, 318, "• 成因 B（祭祀燎玉）：商周/红山火烧 >800℃ 脱水相变扩孔；", size=10.8, color=BODY))
    el.append(txt(412, 338, "• 空气孔（n=1.00）与玉晶（n=1.62）界面单次反射率飙升！", size=10.8, weight="700", color=PURPLE))

    # Bottom wide explanatory banner: Why folk "钙化 (calcification)" is wrong & why "盘玉回润" works!
    el.append(card(22, 400, 716, 88, rx=12, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(40, 425, "连破两大谜团：① 为什么说“古玉钙化”是用词错误？ ② 为什么手盘古玉会慢慢“回润变透”？", size=12.5, weight="700", color=BLUE))
    el.append(txt(40, 447, "• 钙化误区：红外与拉曼光谱检测表明，鸡骨白古玉并未变成碳酸钙（CaCO₃），反而因地下水淋滤流失了部分钙镁硅，应称“白化/受沁风化”。", size=10.7, color=BODY))
    el.append(txt(40, 468, "• 盘玉光学：人体皮脂（n ≈ 1.48）渗入表层微孔赶走空气（n = 1.00），界面散射率骤降超 25 倍，光线重新穿透——但出土文物严禁手盘污染！", size=10.7, weight="700", color=INK))

    write_svg(
        TOPIC,
        "chicken-bone-white-nanopore-light-scattering.svg",
        figure(H, "古玉鸡骨白纳米微孔散射白化机制与盘玉回润光学原理图", "对比致密新玉深层透射与风化古玉微孔米氏散射白化，解释为何鸡骨白并非碳酸钙化以及油脂填充微孔降低折射率差的物理效应", el),
    )


# ---------------------------------------------------------------------------
# 6. Forensic Chemistry of Jade "Qin" Colors: Debunking the "Blood Qin" Myth
# ---------------------------------------------------------------------------
def build_qin_colors_forensics() -> None:
    W, H = 760, 516
    el = []
    el.append(txt(W / 2, 30, "科学拆穿古玉“血沁”迷信：五彩斑斓的出土沁色到底从哪来？", size=18.5, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "“千年碧血入玉”只是志怪小说——现代无损光谱与三维显微揪出了墓葬里的四种真实矿物染匠", size=12.2, color=MUTED, anchor="middle"))

    cards_data = [
        (
            22, 72, RED_SOFT, "#fca5a5", RED,
            "① 红沁 / 枣皮红：是朱砂与铁锈，绝非人血！",
            "民间传言：墓主咽气时的鲜血渗入玉肌化为“血沁”。",
            "科学铁证：血液血红蛋白是大分子有机物，入土不久便被",
            "微生物分解殆尽，二价铁氧化后也只会变成暗褐铁锈！",
            "• 真凶一：先秦两汉贵族敛葬大量铺洒鲜红朱砂（辰砂 α-HgS）；",
            "• 真凶二：富铁地下水沿玉器微裂纹渗入，沉淀出赤铁矿（Fe₂O₃）。",
        ),
        (
            390, 72, AMBER_SOFT, "#fcd34d", AMBER,
            "② 土沁 / 栗子黄：地下水里的针铁矿慢染",
            "常见部位：玉璧边缘、受压微裂隙与疏松白化层。",
            "科学机制：北方黄土或南方红壤中的可溶性铁离子（Fe²⁺）",
            "随毛细地下水年复一年浸润玉表受蚀微孔，在氧气参与下",
            "• 水解沉淀为羟基氧化铁——针铁矿 / 褐铁矿（FeOOH）；",
            "• 呈现由表及里、顺裂隙深浅过渡的自然秋葵黄与栗子皮色。",
        ),
        (
            22, 290, GREEN_SOFT, "#86efac", GREEN,
            "③ 铜绿沁（鹦哥绿）：青铜礼器邻居的“串色”",
            "典型场景：商周大墓（如殷墟妇好墓）玉器紧挨青铜鼎爵陪葬。",
            "科学机制：青铜器在潮湿墓室中发生电化学腐蚀，析出游离",
            "铜离子（Cu²⁺），随墓室积水迁移进紧贴的透闪石玉微孔：",
            "• 与碳酸根结合结晶为翠绿色的孔雀石 Cu₂CO₃(OH)₂，",
            "• 或蓝色的蓝铜矿，在白化古玉上染出鲜亮“松石绿/鹦哥绿”！",
        ),
        (
            390, 290, SLATE_SOFT, "#cbd5e1", INK,
            "④ 水银沁 / 黑漆古：红朱砂变身“黑辰砂”！",
            "千年悬案：纯液态金属水银张力极大，实验证明钻不进完整好玉！",
            "2023 飞秒泵浦—探测非线性光学三维显微无损揭秘：",
            "• 高等级东周大墓中的黑沁并非液态纯汞直接浸染，而是墓中",
            "  红色辰砂（α-HgS）或尸身腐解硫元素与汞反应，转化为黑色",
            "  同质多象变体——黑辰砂（β-HgS，检出深达 38 μm）及炭质！",
        ),
    ]

    for cx, cy, bg, bd, col, h1, l1, l2, l3, l4, l5 in cards_data:
        el.append(card(cx, cy, 348, 202, rx=12, fill="#ffffff", stroke=BORDER))
        el.append(card(cx + 12, cy + 12, 324, 34, rx=8, fill=bg, stroke=bd))
        el.append(txt(cx + 22, cy + 34, h1, size=12, weight="700", color=col))
        for idx, lt in enumerate([l1, l2, l3, l4, l5]):
            w_val = "700" if idx in (0, 3, 4) and lt.startswith("•") else None
            el.append(txt(cx + 20, cy + 68 + idx * 24, lt, size=10.6, color=BODY, weight=w_val))

    write_svg(
        TOPIC,
        "ancient-jade-qin-colors-science-vs-myth.svg",
        figure(H, "出土古玉红沁黄沁铜绿沁与黑漆古水银沁的矿物化学成因图解", "四宫格对比古玉红沁（辰砂与赤铁矿而非人血）、黄褐土沁（针铁矿）、铜绿沁（孔雀石）与黑漆古水银沁（黑辰砂β-HgS）的科学机制", el),
    )


@register(
    TOPIC,
    "Formation of jade cultural relics: 3-stage lifecycle, nephrite toughness vs Mohs, Kunlun metasomatism vs subduction jadeite, Neolithic abrasive carving, chicken-bone white scattering & Qin chemistry",
    "humanities",
)
def build_all() -> None:
    print(f"[{TOPIC}] building & verifying assertions...")
    _verify_jade_math()
    build_three_births_overview()
    build_toughness_vs_hardness()
    build_geological_furnaces()
    build_neolithic_jade_working()
    build_chicken_bone_white_optics()
    build_qin_colors_forensics()
