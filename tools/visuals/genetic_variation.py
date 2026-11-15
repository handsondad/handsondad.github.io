"""Original SVG visuals for genetic division/replication variation and evolution."""

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
    register,
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "genetic-variation"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"


def arrow_defs():
    return (
        f'<defs><marker id="arr-ink" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M0,1 L9,5 L0,9 Z" fill="{SLATE}"/></marker></defs>'
    )


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker_end=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    m_attr = f' marker-end="url(#{marker_end})"' if marker_end else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}"{d_attr}{m_attr}/>'
    )


def _polyline(pts, color=BLUE, sw=2.5, dash=None):
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    p_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (
        f'<polyline points="{p_str}" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{d_attr}/>'
    )


def _verify_genetics_and_evolution_math():
    """Verify quantitative replication fidelity, Kong 2012 trio rates, meiosis & Kimura clock."""
    # 1. Three-tier fidelity cascade (Schaaper 1993)
    e_base = 1e-5
    e_proof = e_base * 1e-2
    e_mmr = e_proof * 1e-3
    assert math.isclose(e_base, 1e-5)
    assert math.isclose(e_proof, 1e-7)
    assert math.isclose(e_mmr, 1e-10)

    # 2. Kong et al. (2012, Nature) human germline de novo mutations & paternal age model
    mu_gen = 1.2e-8
    diploid_callable_bp = 5.0e9  # ~2 x 2.5e9 callable euchromatic bp inKong et al.
    expected_snvs_age30 = mu_gen * diploid_callable_bp
    assert 55.0 <= expected_snvs_age30 <= 75.0  # ~60 de novo SNVs at father age ~30

    def total_dnm(father_age):
        mat = 15.0
        pat = 25.0 + 2.0 * (father_age - 20.0)
        return mat, pat, mat + pat

    _, pat20, tot20 = total_dnm(20)
    _, pat30, tot30 = total_dnm(30)
    _, pat40, tot40 = total_dnm(40)
    assert pat20 == 25.0 and tot20 == 40.0
    assert pat30 == 45.0 and tot30 == 60.0
    assert pat40 == 65.0 and tot40 == 80.0

    # 3. Meiosis independent assortment
    gamete_combos = 2 ** 23
    zygote_combos = 2 ** 46
    assert gamete_combos == 8_388_608
    assert zygote_combos == 70_368_744_177_664
    assert zygote_combos / 8.2e9 > 8_000  # >8,000x current world population!

    # 4. Luria-Delbruck fluctuation contrast (variance / mean)
    poisson_tubes = [4, 5, 3, 4, 6, 3, 5, 4]
    m_p = sum(poisson_tubes) / len(poisson_tubes)
    v_p = sum((x - m_p) ** 2 for x in poisson_tubes) / (len(poisson_tubes) - 1)
    jackpot_tubes = [0, 0, 1, 0, 64, 2, 0, 1]
    m_j = sum(jackpot_tubes) / len(jackpot_tubes)
    v_j = sum((x - m_j) ** 2 for x in jackpot_tubes) / (len(jackpot_tubes) - 1)
    assert 0.2 < v_p / m_p < 1.5
    assert v_j / m_j > 40.0  # Massive fluctuation signature of pre-existing random division mutation!

    # 5. Kimura (1968) neutral substitution rate k = (2*N*mu0) * (1/(2*N)) == mu0
    mu0 = 1.2e-8
    for pop_n in (100, 10_000, 10_000_000):
        k_sub = (2 * pop_n * mu0) * (1.0 / (2 * pop_n))
        assert math.isclose(k_sub, mu0, rel_tol=1e-12)

    # 6. Haigh (1978) Muller's ratchet least-loaded class n0 = N * exp(-U / s)
    # Small asexual population N=100, deleterious U=0.6, s=0.1 -> n0 = 100 * e^-6 = 0.248 < 1 -> ratchet clicks!
    n0_small = 100 * math.exp(-0.6 / 0.1)
    assert n0_small < 1.0


def build_fig1_replication_fidelity_and_paternal_age():
    """Fig 1: 3-gate DNA replication fidelity cascade + Kong 2012 paternal age mutation curve."""
    el = [arrow_defs()]
    el.extend(
        header(
            "第一幕：三道安检把错字率压到百亿分之一，为何每个新生儿仍自带 ~60 个新突变？",
            "DNA 聚合酶几何卡槽 × 外切酶“退格键” × 错配修复巡逻队，遇上 64 亿碱基与精原干细胞终身分裂！",
        )
    )

    # Left Card: 3-Gate Replication Fidelity Funnel
    el.append(card(22, 68, 356, 386, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 95, "细胞分裂 S 期：DNA 复制的“三重纠错安检门”", size=11.5, color=INK, weight="700"))

    gates = [
        (
            "第 1 关：聚合酶活性口袋“几何卡槽筛选”",
            "正确 A-T / G-C 碱基对几何宽度严丝合缝才给成键",
            "漏网错字率：~ 10⁻⁵（每抄 10 万字错 1 个）",
            BLUE,
            BLUE_SOFT,
        ),
        (
            "第 2 关：3'→5' 外切酶即时“退格键校对”",
            "刚装歪瞬间聚合酶卡壳倒车，一刀切掉错碱基重填",
            "再压低 100 倍 → 错字率降至 ~ 10⁻⁷（千万分之一）",
            PURPLE,
            PURPLE_SOFT,
        ),
        (
            "第 3 关：复制后错配修复巡逻队（MMR）",
            "MutS/MutL 沿新链扫描凸起鼓包，剪除错段补齐",
            "再压低 100～1000 倍 → 终极错字率 ~ 10⁻¹⁰！",
            GREEN,
            GREEN_SOFT,
        ),
    ]
    gy = 112
    for g_title, g_sub, g_rate, fg_c, bg_c in gates:
        el.append(card(36, gy, 328, 86, rx=8, fill=bg_c, stroke=fg_c))
        el.append(txt(48, gy + 22, g_title, size=10.6, color=fg_c, weight="700"))
        el.append(txt(48, gy + 44, g_sub, size=9.8, color=BODY))
        el.append(txt(48, gy + 67, g_rate, size=10.0, color=INK, weight="700"))
        if gy < 280:
            el.append(_line(200, gy + 88, 200, gy + 100, color=SLATE, sw=1.8, marker_end="arr-ink"))
        gy += 102

    el.append(card(36, 416, 328, 28, rx=6, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(200, 434, "比喻：相当于连抄 1000 部《红楼梦》只许打错 1 个标点！", size=9.8, color=ORANGE, anchor="middle", weight="700"))

    # Right Card: Why ~60 De Novo Mutations Still Arise + Kong 2012 Paternal Age Plot
    el.append(card(394, 68, 344, 386, fill=CARD_BG))
    el.append(step_badge(414, 90, 2, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(432, 95, "百亿分之一 × 几十轮分裂 = 新生儿 ~60 个突变", size=11.3, color=INK, weight="700"))

    # Plot box inside x=[446..716], y=[274..128]
    px0, px1 = 446.0, 714.0
    py0, py1 = 274.0, 128.0

    def map_age(age, muts):
        # age in [18, 46], muts in [0, 95]
        x = px0 + ((age - 18.0) / 28.0) * (px1 - px0)
        y = py0 - (muts / 95.0) * (py0 - py1)
        return (x, y)

    for m_tick in (0, 20, 40, 60, 80):
        _, ty = map_age(18, m_tick)
        el.append(_line(px0, ty, px1, ty, color="#e2e8f0" if m_tick else SLATE, sw=1.0 if m_tick else 1.4))
        el.append(txt(px0 - 6, ty + 4, str(m_tick), size=9.4, color=MUTED, anchor="end"))

    el.append(_line(px0, py1, px0, py0, color=SLATE, sw=1.4))
    for a_tick in (20, 25, 30, 35, 40, 45):
        tx, _ = map_age(a_tick, 0)
        el.append(_line(tx, py0, tx, py0 + 4, color=SLATE, sw=1.2))
        el.append(txt(tx, py0 + 16, f"{a_tick}岁", size=9.2, color=MUTED, anchor="middle"))

    el.append(txt(580, 120, "Kong 等 (2012 Nature) 父母年龄与子代新发突变实测线", size=9.6, color=INK, anchor="middle", weight="600"))

    # Maternal flat line ~15
    pts_mat = [map_age(a, 15.0) for a in (18, 45)]
    el.append(_polyline(pts_mat, color=PURPLE, sw=2.4, dash="4,3"))
    _, ym15 = map_age(36, 15.0)
    el.append(txt(708, ym15 - 6, "母源卵子恒定 ~15 个", size=9.4, color=PURPLE, anchor="end", weight="700", halo=True))

    # Paternal rising line: 25 + 2*(age-20)
    pts_pat = [map_age(a, 25.0 + 2.0 * (a - 20.0)) for a in (19, 45)]
    el.append(_polyline(pts_pat, color=BLUE, sw=2.6))

    # Total newborn mutations: 40 + 2*(age-20)
    pts_tot = [map_age(a, 40.0 + 2.0 * (a - 20.0)) for a in (19, 45)]
    el.append(_polyline(pts_tot, color=RED, sw=2.8))

    for a_pt in (20, 30, 40):
        tot_v = 40.0 + 2.0 * (a_pt - 20.0)
        cx, cy = map_age(a_pt, tot_v)
        el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.2" fill="{RED}" stroke="#ffffff" stroke-width="1.2"/>')

    x30, y30 = map_age(30, 60)
    el.append(txt(x30 - 8, y30 - 10, "30岁生娃：总计 ~60 个", size=9.5, color=RED, anchor="middle", weight="700", halo=True))
    x36_p, y36_p = map_age(37, 59)
    el.append(txt(x36_p + 4, y36_p + 18, "父源精子线 (+2个/年)", size=9.4, color=BLUE, anchor="middle", weight="700", halo=True))

    # Explanation box below plot
    el.append(card(408, 302, 316, 140, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(420, 323, "为什么子代新发突变 ~75% 来自爸爸？", size=10.5, color=INK, weight="700"))
    el.append(txt(420, 344, "• 妈妈卵子：女婴出生前卵原细胞就停止有丝分裂", size=9.7, color=BODY))
    el.append(txt(420, 362, "  （一生固定约 23 次分裂），年龄再大也不多抄书；", size=9.7, color=BODY))
    el.append(txt(420, 382, "• 爸爸精子：青春期后精原干细胞每 16 天分裂一轮", size=9.7, color=BODY))
    el.append(txt(420, 400, "  （每年多抄 23 遍）！20岁约分裂150次，40岁已达", size=9.7, color=BODY))
    el.append(txt(420, 418, "  610 次——多抄一次，就多攒一点微小复制笔误！", size=9.7, color=RED, weight="700"))

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            491,
            "记住第一条铁律：体细胞（皮肤/肌肉）分裂突变只影响自己，唯有生殖细胞（精卵）里的突变才能遗传并参与演化！",
            size=11.0,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "DNA复制三重纠错保真机制与人类父母年龄对新生儿新发突变数量影响实测图",
        "左图展示DNA聚合酶碱基几何筛选、外切酶校对与错配修复将错误率从十万分之一压低至百亿分之一；右图按Kong等2012年Nature冰岛家系全基因组测序结果绘制母源恒定约15个与父源随年龄每年增加约2个新发突变的线性规律。",
        el,
    )
    write_svg(SUBDIR, "replication-fidelity-three-gates.svg", svg)


def build_fig2_four_molecular_mutation_glitches():
    """Fig 2: 2x2 grid of the 4 core molecular replication & spontaneous lesion glitches."""
    el = [arrow_defs()]
    el.extend(
        header(
            "第二幕：哪怕躲在没紫外线的黑屋里，分裂时哪四种“分子手滑”会改写密码？",
            "不用核辐射也不用毒药——量子氢原子跳位、37℃ 水分子偷袭与重复序列打滑，天天都在制造自发变异！",
        )
    )

    boxes = [
        (
            22,
            68,
            1,
            "① 互变异构瞬态“假面舞会”（点突变）",
            BLUE,
            BLUE_SOFT,
            [
                ("案发机制：", "碱基上的氢原子偶尔瞬间跳到隔壁氮/氧原子上"),
                ("怎样骗过安检：", "稀有的胸腺嘧啶烯醇式 T* 几何长相酷似胞嘧啶 C，"),
                ("永久改写：", "复制叉经过那微秒瞬间，T* 硬拉来 G 配对 → 下一轮"),
                ("演化后果：", "分裂彻底变成 C-G 碱基对（产生同义/错义/无义点突变）！"),
            ],
        ),
        (
            388,
            68,
            2,
            "② 37℃ 体温水分子“拔氨基”（CpG 热点）",
            ORANGE,
            ORANGE_SOFT,
            [
                ("案发机制：", "细胞内的水分子每天自发撞掉数百个胞嘧啶 C 的氨基"),
                ("甲基化陷阱：", "普通 C 脱氨变成非法碱基 U，修复酶一眼认出秒切；"),
                ("真假美猴王：", "但基因调控常见的“甲基化 5-mC”脱氨后，直接变成"),
                ("演化后果：", "合法碱基 T！修复酶难辨真假，使 CpG 突变率飙高 10 倍！"),
            ],
        ),
        (
            22,
            266,
            3,
            "③ 聚合酶“复制打滑”（插入/缺失移码）",
            RED,
            RED_SOFT,
            [
                ("案发地形：", "遇到微卫星重复路段（如 CACACACACA... 连续重复）"),
                ("打滑瞬间：", "聚合酶喘口气短暂脱手，新链或模板链拱起一个小环，"),
                ("多抄或漏抄：", "重新抓紧时错位一格，白白多塞或漏掉 1～2 个字母！"),
                ("演化后果：", "若非 3 的倍数，后面所有三联体密码子全乱套（移码突变）！"),
            ],
        ),
        (
            388,
            266,
            4,
            "④ 错位不等交换与转座子跳跃（大段拷贝）",
            PURPLE,
            PURPLE_SOFT,
            [
                ("案发地形：", "基因组里遍布相似的重复序列或“跳跃基因”逆转录转座子"),
                ("错位对齐：", "分裂重组时两条同源染色体“看走眼”错开一格配对互换，"),
                ("一多一少：", "一条染色体白捡了双份完整基因（基因重复！），另一条缺失；"),
                ("演化后果：", "白捡的备份基因成了日后演化“发明全新器官功能”的金矿！"),
            ],
        ),
    ]

    for bx, by, num, b_title, fg_c, bg_c, rows in boxes:
        el.append(card(bx, by, 350, 184, fill=CARD_BG))
        el.append(card(bx + 12, by + 12, 326, 36, rx=7, fill=bg_c, stroke=fg_c))
        el.append(step_badge(bx + 28, by + 30, num, r=10, fg=fg_c, bg="#ffffff"))
        el.append(txt(bx + 45, by + 35, b_title, size=10.8, color=fg_c, weight="700"))

        ry = by + 68
        for k_idx, (r_head, r_txt) in enumerate(rows):
            is_last = k_idx == 3
            el.append(txt(bx + 20, ry, r_head + r_txt, size=9.8, color=INK if is_last else BODY, weight="700" if is_last else "400"))
            ry += 27

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(
        txt(
            380,
            491,
            "外因（紫外线胸腺嘧啶二聚体、电离辐射断链、烟草亚硝胺）只是踩下油门；内源热涨落与化学水解才是永不停歇的底噪！",
            size=10.8,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "细胞分裂期四大内源分子变异机制图解",
        "分四格展示碱基互变异构瞬态错配、37摄氏度水分子诱导甲基化胞嘧啶脱氨基形成CpG十倍突变热点、重复序列复制打滑导致移码突变，以及错位不等交换产生基因重复。",
        el,
    )
    write_svg(SUBDIR, "four-molecular-glitches.svg", svg)


def build_fig3_meiosis_recombination_anim():
    """Fig 3: 1-shot animated SVG contrasting Mitosis vs Meiosis 3-step variation engine."""
    extra_css = """
      @keyframes chiasma-glow {
        0%, 15% { opacity: 0.25; }
        35%, 100% { opacity: 1; }
      }
      @keyframes swap-seg {
        0%, 25% { opacity: 0; transform: translateY(-6px); }
        48%, 100% { opacity: 1; transform: translateY(0); }
      }
      @keyframes gamete-pop {
        0%, 55% { opacity: 0.2; }
        82%, 100% { opacity: 1; }
      }
      .anim-chiasma { animation: chiasma-glow 6.5s ease-out 1 forwards; }
      .anim-swap { animation: swap-seg 6.5s ease-out 1 forwards; }
      .anim-gametes { animation: gamete-pop 6.5s ease-out 1 forwards; }
      @media (prefers-reduced-motion: reduce) {
        .anim-chiasma, .anim-swap, .anim-gametes {
          animation: none !important; opacity: 1 !important; transform: none !important;
        }
      }
    """

    el = [arrow_defs()]
    el.extend(
        header(
            "第三幕：减数分裂不是“复印机”，而是演化最疯狂的“三层基因洗牌机”！",
            "为什么同一对父母生出的亲兄妹长相性格迥异？SPO11 主动断链互换 + 2²³ 独立分配把底牌洗出万亿花样",
        )
    )

    # Top Wide Card: 3-Stage Meiotic Shuffle Pipeline (Animated 1-shot)
    el.append(card(22, 68, 716, 224, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(60, 95, "减数分裂（一次复制、两次分裂）：把父母两套染色体剪接洗牌成独一无二的配子", size=11.4, color=INK, weight="700"))

    # Stage Box A: Prophase I SPO11 + Crossing Over
    el.append(card(36, 110, 214, 168, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(143, 130, "① 前期I：同源联会与交叉互换", size=10.5, color=BLUE, anchor="middle", weight="700"))
    # Draw paternal (blue) and maternal (orange) chromatid pair crossing at chiasma
    el.append(f'<rect x="92" y="144" width="12" height="68" rx="6" fill="{BLUE}"/>')
    el.append(f'<rect x="110" y="144" width="12" height="68" rx="6" fill="{BLUE}"/>')
    el.append(f'<rect x="164" y="144" width="12" height="68" rx="6" fill="{ORANGE}"/>')
    el.append(f'<rect x="182" y="144" width="12" height="68" rx="6" fill="{ORANGE}"/>')
    # Crossing X lines between x=116 and x=170
    el.append(
        f'<g class="anim-chiasma">'
        f'<line x1="116" y1="162" x2="170" y2="198" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/>'
        f'<line x1="170" y1="162" x2="116" y2="198" stroke="{ORANGE}" stroke-width="5" stroke-linecap="round"/>'
        f'<circle cx="143" cy="180" r="8" fill="#ffffff" stroke="{RED}" stroke-width="2"/>'
        f'{txt(143, 184, "✂", size=10, color=RED, anchor="middle", weight="700")}'
        f'</g>'
    )
    el.append(txt(143, 232, "SPO11 酶故意剪断约 250 处双链！", size=9.5, color=RED, anchor="middle", weight="700"))
    el.append(txt(143, 250, "爷爷与外婆的基因片段当场互换", size=9.5, color=BODY, anchor="middle"))
    el.append(txt(143, 267, "每条染色体平均交换 1～3 处", size=9.4, color=INK, anchor="middle", weight="600"))

    el.append(_line(254, 194, 272, 194, color=SLATE, sw=2.0, marker_end="arr-ink"))

    # Stage Box B: Metaphase I Independent Assortment (2^23)
    el.append(card(276, 110, 214, 168, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(383, 130, "② 中期I：23对染色体随机站队", size=10.5, color=PURPLE, anchor="middle", weight="700"))
    # Show chimeric chromatids after swap
    el.append(
        f'<g class="anim-swap">'
        f'<rect x="316" y="146" width="12" height="58" rx="5" fill="{BLUE}"/>'
        f'<rect x="334" y="146" width="12" height="38" rx="4" fill="{BLUE}"/>'
        f'<rect x="334" y="180" width="12" height="24" rx="4" fill="{ORANGE}"/>'
        f'<rect x="420" y="146" width="12" height="38" rx="4" fill="{ORANGE}"/>'
        f'<rect x="420" y="180" width="12" height="24" rx="4" fill="{BLUE}"/>'
        f'<rect x="438" y="146" width="12" height="58" rx="5" fill="{ORANGE}"/>'
        f'{_line(383, 142, 383, 210, color=PURPLE, sw=1.5, dash="3,2")}'
        f'{txt(383, 180, "左/右抛硬币", size=9.2, color=PURPLE, anchor="middle", weight="700", halo=True)}'
        f'</g>'
    )
    el.append(txt(383, 232, "单凭左右随机分配：2²³ = 838.8 万种", size=9.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(383, 250, "精卵结合底牌：2⁴⁶ ≈ 70.4 万亿种！", size=9.5, color=RED, anchor="middle", weight="700"))
    el.append(txt(383, 267, "相当于全球总人口的 8,500 倍以上", size=9.4, color=BODY, anchor="middle"))

    el.append(_line(494, 194, 512, 194, color=SLATE, sw=2.0, marker_end="arr-ink"))

    # Stage Box C: 4 Distinct Chimeric Gametes
    el.append(card(516, 110, 208, 168, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(txt(620, 130, "③ 终局：4 颗全异单倍体配子", size=10.5, color=GREEN, anchor="middle", weight="700"))
    # Draw 4 gamete circles with distinct chromatid color patterns
    g_centers = [(546, 178), (595, 178), (645, 178), (694, 178)]
    el.append('<g class="anim-gametes">')
    for idx_g, (gx, gy) in enumerate(g_centers):
        el.append(f'<circle cx="{gx}" cy="{gy}" r="20" fill="#ffffff" stroke="{GREEN}" stroke-width="1.8"/>')
        if idx_g == 0:
            el.append(f'<rect x="{gx-4}" y="{gy-13}" width="8" height="26" rx="4" fill="{BLUE}"/>')
        elif idx_g == 1:
            el.append(f'<rect x="{gx-4}" y="{gy-13}" width="8" height="15" rx="3" fill="{BLUE}"/>')
            el.append(f'<rect x="{gx-4}" y="{gy}" width="8" height="13" rx="3" fill="{ORANGE}"/>')
        elif idx_g == 2:
            el.append(f'<rect x="{gx-4}" y="{gy-13}" width="8" height="15" rx="3" fill="{ORANGE}"/>')
            el.append(f'<rect x="{gx-4}" y="{gy}" width="8" height="13" rx="3" fill="{BLUE}"/>')
        else:
            el.append(f'<rect x="{gx-4}" y="{gy-13}" width="8" height="26" rx="4" fill="{ORANGE}"/>')
    el.append("</g>")
    el.append(txt(620, 232, "1 颗全父本 + 2 颗新拼嵌合 + 1 颗全母本", size=9.3, color=INK, anchor="middle", weight="700"))
    el.append(txt(620, 250, "哪怕一个新点突变都没发生，", size=9.5, color=BODY, anchor="middle"))
    el.append(txt(620, 267, "每颗精卵也是从未存在过的新配方！", size=9.5, color=GREEN, anchor="middle", weight="700"))

    # Bottom Left Card: Mitosis vs Meiosis Functional Contrast
    el.append(card(22, 304, 350, 150, fill=CARD_BG))
    el.append(step_badge(42, 326, 2, fg=SLATE, bg=SLATE_SOFT))
    el.append(txt(60, 331, "有丝分裂 vs 减数分裂：保真与求变的双轨制", size=11.4, color=INK, weight="700"))
    el.append(txt(40, 356, "• 体细胞有丝分裂（2n → 2n）：目标是“零走样复印”，", size=9.9, color=BODY))
    el.append(txt(40, 375, "  同源染色体互不联会互换；一旦失控积累突变只会引发", size=9.9, color=BODY))
    el.append(txt(40, 394, "  个体衰老或肿瘤，随着个体去世归零，不传给下一代；", size=9.9, color=SLATE, weight="600"))
    el.append(txt(40, 416, "• 生殖系减数分裂（2n → n）：专为跨代演化而生！把点突变", size=9.9, color=BODY))
    el.append(txt(40, 435, "  创造的“新零件”与同源重组的“新组装”打包送进受精卵。", size=9.9, color=BLUE, weight="700"))

    # Bottom Right Card: Chromosomal Nondisjunction & Whole-Genome Duplication (Polyploidy)
    el.append(card(388, 304, 350, 150, fill=CARD_BG))
    el.append(step_badge(408, 326, 3, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(426, 331, "纺锤丝拉拽失手：非整倍体与全基因组加倍", size=11.4, color=INK, weight="700"))
    el.append(txt(406, 356, "• 单条染色体不分离（Nondisjunction）：两姐妹或同源体", size=9.9, color=BODY))
    el.append(txt(406, 375, "  挤进同一颗配子，造成剂量失衡（如人类 21 三体综合征）；", size=9.9, color=RED, weight="600"))
    el.append(txt(406, 397, "• 整套染色体翻倍（多倍化 Polyploidy）：在植物界直接催生", size=9.9, color=BODY))
    el.append(txt(406, 416, "  新物种（如六倍体普通小麦、无籽西瓜）；5亿年前寒武纪", size=9.9, color=BODY))
    el.append(txt(406, 435, "  脊椎动物祖先更是靠“两轮全基因组加倍 (2R)”跃升复杂生命！", size=9.9, color=GREEN, weight="700"))

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(
        txt(
            380,
            491,
            "一句话分清两大源泉：DNA 复制突变负责发明“新等位基因字母”，减数分裂重组负责把字母拼成“亿万种新句子”！",
            size=11.0,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "减数分裂同源重组交叉互换与独立分配单次动画及染色体分离变异图解",
        "上图通过单次动画依次展示减数分裂前期I由SPO11酶启动的同源非姐妹染色单体交叉互换、中期I二十三对染色体独立分配产生838.8万种配子，以及终局四颗各不相同的单倍体配子；下图对比有丝分裂保真与减数分裂染色体不分离及全基因组加倍。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "meiosis-recombination-shuffle-anim.svg", svg)


def build_fig4_luria_delbruck_and_kimura_clock():
    """Fig 4: Luria-Delbruck 1943 random mutation test + Kimura 1968 neutral clock k = mu."""
    el = [arrow_defs()]
    el.extend(
        header(
            "第四幕：变异是“被环境逼出来的”吗？波动实验铁证与中性分子钟",
            "破除“用进废退定向变异”迷思：分裂变异完全盲目超前，自然选择与随机漂变决定谁留下！",
        )
    )

    # Left Card: Luria-Delbruck 1943 Fluctuation Test (1969 Nobel Prize)
    el.append(card(22, 68, 352, 386, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(60, 95, "1943 波动实验：细菌不是见了毒药才学着抗药！", size=11.3, color=INK, weight="700"))

    # Hypothesis A vs Hypothesis B mini bar charts
    el.append(card(36, 112, 324, 134, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(48, 132, "假说 A（错）：见了噬菌体/抗生素才“被逼变异”", size=10.2, color=MUTED, weight="700"))
    el.append(txt(48, 150, "→ 每支平行培养管临阵抱佛脚概率一样（均匀泊松分布）：", size=9.5, color=BODY))
    # Draw 6 uniform small bars [4, 5, 3, 4, 5, 4]
    bars_a = [4, 5, 3, 4, 5, 4]
    for i_b, bv in enumerate(bars_a):
        bx = 58 + i_b * 46
        bh = bv * 6
        el.append(f'<rect x="{bx}" y="{218 - bh}" width="26" height="{bh}" rx="3" fill="{SLATE}"/>')
        el.append(txt(bx + 13, 214 - bh, str(bv), size=9.2, color=SLATE, anchor="middle", weight="700"))
        el.append(txt(bx + 13, 234, f"管{i_b + 1}", size=8.8, color=MUTED, anchor="middle"))

    el.append(card(36, 258, 324, 182, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(48, 278, "真实实验 B（1969诺奖）：分裂时早就随机盲目突变！", size=10.2, color=ORANGE, weight="700"))
    el.append(txt(48, 296, "→ 早几代偶然撞上突变的管子，翻倍繁衍出“头奖克隆团”：", size=9.5, color=BODY))
    # Draw 6 jackpot bars [0, 0, 1, 64, 0, 2]
    bars_b = [0, 0, 1, 64, 0, 2]
    heights_b = [2, 2, 6, 62, 2, 10]
    for i_b, (bv, bh) in enumerate(zip(bars_b, heights_b)):
        bx = 58 + i_b * 46
        col_b = RED if bv == 64 else BLUE
        el.append(f'<rect x="{bx}" y="{384 - bh}" width="26" height="{bh}" rx="3" fill="{col_b}"/>')
        el.append(txt(bx + 13, 379 - bh, f"{bv}!", size=9.5 if bv == 64 else 9.0, color=col_b, anchor="middle", weight="700"))
        el.append(txt(bx + 13, 400, f"管{i_b + 1}", size=8.8, color=INK if bv == 64 else MUTED, anchor="middle"))
    el.append(txt(198, 426, "铁证：变异是分裂前乱掷的骰子，抗生素只是事后筛子！", size=9.7, color=RED, anchor="middle", weight="700"))

    # Right Card: Mutation Fitness Spectrum + Kimura Neutral Clock Cancellation
    el.append(card(390, 68, 348, 386, fill=CARD_BG))
    el.append(step_badge(410, 90, 2, fg=BLUE, bg=BLUE_SOFT))
    el.append(txt(428, 95, "突变命运三岔口与木村资生“分子钟神仙约分”", size=11.3, color=INK, weight="700"))

    # Stacked horizontal spectrum bar
    el.append(txt(406, 120, "新发突变对生存繁衍（适应度）的三类真实比例：", size=9.8, color=INK, weight="600"))
    # Bar x=[406..722] width=316: Neutral/nearly-neutral 70% (221px), Deleterious 29% (92px, split visual 210 + 92 + 14)
    el.append(f'<rect x="406" y="130" width="200" height="24" rx="4" fill="{BLUE}"/>')
    el.append(txt(506, 146, "中性/近中性 (~70–85%)", size=9.4, color="#ffffff", anchor="middle", weight="700"))
    el.append(f'<rect x="608" y="130" width="94" height="24" rx="4" fill="{SLATE}"/>')
    el.append(txt(655, 146, "有害(被淘汰)", size=9.2, color="#ffffff", anchor="middle", weight="700"))
    el.append(f'<rect x="704" y="130" width="18" height="24" rx="3" fill="{GREEN}"/>')

    el.append(txt(406, 173, "• 有害突变：破坏关键酶结构，被“净化选择”迅速扫出种群；", size=9.6, color=BODY))
    el.append(txt(406, 192, "• 极少数有利突变（右端绿线 <1%）：如藏族高原低氧 EPAS1、", size=9.6, color=BODY))
    el.append(txt(406, 210, "  欧洲牧民成年乳糖酶持久、疟区镰刀红细胞杂合优势→正选择暴涨！", size=9.6, color=GREEN, weight="700"))
    el.append(txt(406, 229, "• 海量中性突变：非编码区或同义密码子替换，靠“随机漂变”浮沉。", size=9.6, color=BLUE, weight="600"))

    # Kimura Neutral Clock Box
    el.append(card(404, 246, 320, 194, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(564, 268, "木村资生（1968）中性演化分子钟的惊天约分：", size=10.4, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(416, 291, "设二倍体种群有 N 个个体（共 2N 份基因拷贝）：", size=9.6, color=BODY))
    el.append(txt(416, 311, "① 每代全族新诞生的中性突变总数 = 2N · μ₀", size=9.8, color=INK, weight="600"))
    el.append(txt(416, 331, "② 任一中性新突变纯凭运气最终占领全族概率 = 1 / (2N)", size=9.8, color=INK, weight="600"))

    el.append(card(420, 344, 288, 36, rx=6, fill="#ffffff", stroke=BLUE))
    el.append(txt(564, 367, "物种基因替换速率  k = (2N · μ₀) × [1 / (2N)] = μ₀ ！", size=10.6, color=RED, anchor="middle", weight="700"))

    el.append(txt(416, 400, "种群大小 2N 完美抵消！无论老鼠还是鲸鱼，中性位点固定", size=9.5, color=BODY))
    el.append(txt(416, 419, "突变的步调只等于突变率 μ₀ —— 分裂笔误直接化作“生命时钟”！", size=9.5, color=INK, weight="700"))

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        txt(
            380,
            491,
            "达尔文自然选择雕刻“适应环境的精巧表型”，木村资生中性漂变刻下“记录亿万年分家时间的分子钟”——二者完美互补！",
            size=10.8,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "卢瑞亚德尔布吕克波动实验与木村资生中性演化分子钟原理图",
        "左图对比环境诱导假说的均匀泊松分布与分裂随机预突变假说的头奖克隆爆发波动；右图展示新发突变的有害、中性与有利谱系，并推导木村资生分子演化速率k等于中性突变率μ0的种群规模约分公式。",
        el,
    )
    write_svg(SUBDIR, "luria-delbruck-and-kimura-clock.svg", svg)


def build_fig5_duplication_innovation_and_ratchet():
    """Fig 5: Ohno gene duplication (primate trichromacy) + Muller's ratchet & optimal fidelity."""
    el = [arrow_defs()]
    el.extend(
        header(
            "第五幕：演化怎样无中生有发明“新功能”？为什么不进化出 100% 零差错？",
            "靠“备份基因自由试错”让我们看清万紫千红；靠减数分裂重组打破穆勒棘轮，守住演化刀锋平衡！",
        )
    )

    # Left Card: Gene Duplication + Neofunctionalization (Primate Red/Green Vision)
    el.append(card(22, 68, 352, 386, fill=CARD_BG))
    el.append(step_badge(42, 90, 1, fg=PURPLE, bg=PURPLE_SOFT))
    el.append(txt(60, 95, "大野乾“备份试错法”：人类凭啥比猫狗多看懂红色？", size=11.1, color=INK, weight="700"))

    steps_dup = [
        (
            "① 独苗基因不敢乱改（猫狗祖先二色视觉）",
            "只剩蓝光 + 1 个中长波视蛋白基因：一旦突变改坏就变瞎，",
            "净化选择死死锁住它，几千万年寸步难行（红绿不分）！",
            SLATE,
            SLATE_SOFT,
        ),
        (
            "② 减数分裂“不等交换”：天降双份拷贝！",
            "约 3500 万年前旧大陆灵长类祖先 X 染色体错位重组，",
            "白捡了一份一模一样的“冗余备份视蛋白基因”！",
            PURPLE,
            PURPLE_SOFT,
        ),
        (
            "③ 正本保命、副本狂野试错（新功能化！）",
            "正本继续看绿光（530 nm），副本卸下保命包袱自由突变：",
            "仅改了 3 个关键氨基酸就把吸收峰推到 560 nm 红光——",
            GREEN,
            GREEN_SOFT,
        ),
    ]
    sy = 112
    for s_head, s_l1, s_l2, fg_c, bg_c in steps_dup:
        el.append(card(36, sy, 324, 90, rx=8, fill=bg_c, stroke=fg_c))
        el.append(txt(48, sy + 22, s_head, size=10.4, color=fg_c, weight="700"))
        el.append(txt(48, sy + 45, s_l1, size=9.7, color=BODY))
        el.append(txt(48, sy + 66, s_l2, size=9.7, color=INK, weight="600"))
        if sy < 290:
            el.append(_line(198, sy + 92, 198, sy + 102, color=SLATE, sw=1.8, marker_end="arr-ink"))
        sy += 104

    el.append(card(36, 422, 324, 24, rx=6, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(198, 438, "一眼在绿叶丛中认出熟透红果！血红蛋白家族同样靠这招诞生", size=9.5, color=ORANGE, anchor="middle", weight="700"))

    # Right Card: Muller's Ratchet & Why Mutation Rate != 0 (Goldilocks Zone)
    el.append(card(390, 68, 348, 386, fill=CARD_BG))
    el.append(step_badge(410, 90, 2, fg=RED, bg=RED_SOFT))
    el.append(txt(428, 95, "穆勒棘轮与终极追问：为何不进化到“零突变”？", size=11.2, color=INK, weight="700"))

    # Box 1: Muller's Ratchet
    el.append(card(404, 112, 320, 148, rx=8, fill=RED_SOFT, stroke=RED))
    el.append(txt(416, 133, "为什么高等生物宁付“两倍繁殖代价”也要搞有性减数分裂？", size=10.0, color=RED, weight="700"))
    el.append(txt(416, 155, "• 无性克隆死局（穆勒棘轮 Muller's Ratchet）：没有重组，子代", size=9.6, color=BODY))
    el.append(txt(416, 174, "  只能整包继承母亲的全部暗伤；一旦最健康个体也攒上 1 个", size=9.6, color=BODY))
    el.append(txt(416, 193, "  微害突变，全族就再也回不到 0 伤状态，咔哒咔哒滑向灭绝！", size=9.6, color=INK, weight="600"))
    el.append(txt(416, 215, "• 减数分裂解药：把爸爸的“A段好基因”与妈妈的“B段好基因”", size=9.6, color=BODY))
    el.append(txt(416, 234, "  交叉拼接，一举重塑零暗伤子代，还能把两项有利突变合体！", size=9.6, color=GREEN, weight="700"))

    # Box 2: The Goldilocks Mutation Rate Balance
    el.append(card(404, 272, 320, 170, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(416, 293, "突变率的“刀锋平衡”：太高会融化，等于零会团灭！", size=10.2, color=BLUE, weight="700"))
    el.append(txt(416, 315, "① 往左走到 0（绝对零差错）：先不说每再准 10 倍都要烧掉巨量", size=9.6, color=BODY))
    el.append(txt(416, 334, "   ATP 拖慢分裂；一旦冰期或新瘟疫降临，基因库一潭死水", size=9.6, color=BODY))
    el.append(txt(416, 353, "   拿不出一张新底牌，整个物种直接走入灭绝死胡同！", size=9.6, color=SLATE, weight="700"))
    el.append(txt(416, 375, "② 往右太高（越过艾根错误灾难阈值）：每代把祖传核心基因", size=9.6, color=BODY))
    el.append(txt(416, 394, "   全抄烂，遗传信息彻底崩溃（这也是抗病毒药诱变杀毒原理）！", size=9.6, color=RED, weight="600"))
    el.append(txt(416, 417, "→ 百亿分之一的微小笔误，正是生命跨越 38 亿年的火种！", size=9.8, color=BLUE, weight="700"))

    # Footer
    el.append(card(22, 466, 716, 40, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    el.append(
        txt(
            380,
            491,
            "结语：所谓“完美无瑕的复制”只会造出脆弱的化石；恰到好处的分裂小瑕疵，才让一团原始细胞写出了整部生命史诗。",
            size=10.9,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    svg = figure(
        520,
        "基因重复新功能化演化出灵长类三色视觉与穆勒棘轮及突变率刀锋平衡图",
        "左图以旧大陆灵长类X染色体视蛋白基因不等交换重复与3个氨基酸突变分化出530nm绿光和560nm红光视觉为例解析大野乾基因重复理论；右图解析有性减数分裂重组如何打破穆勒棘轮，以及突变率处于零差错僵死与错误灾难崩溃之间的刀锋平衡。",
        el,
    )
    write_svg(SUBDIR, "gene-duplication-and-mullers-ratchet.svg", svg)


@register("genetic-variation", "基因分裂变异机制与生物演化五幕曲", "科学")
def build_all():
    print("[genetic-variation] building & verifying assertions...")
    _verify_genetics_and_evolution_math()
    build_fig1_replication_fidelity_and_paternal_age()
    build_fig2_four_molecular_mutation_glitches()
    build_fig3_meiosis_recombination_anim()
    build_fig4_luria_delbruck_and_kimura_clock()
    build_fig5_duplication_innovation_and_ratchet()
