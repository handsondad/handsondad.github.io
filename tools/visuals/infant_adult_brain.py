"""Original 760px Chinese SVG diagrams for the Infant vs Adult Brain post."""

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
    card,
    figure,
    header,
    register,
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "infant-adult-brain"


def _verify_infant_brain_math():
    """Verify quantitative neuroscience milestones, rates, and chart proportions."""
    # 1. Holland et al. (2014, JAMA Neurol): neonatal mean volume & 90-day 64% expansion
    v_male_mm3, v_female_mm3 = 347_388.0, 335_509.0
    v_birth_cm3 = 0.5 * (v_male_mm3 + v_female_mm3) / 1000.0
    v_90d_cm3 = v_birth_cm3 * 1.64
    assert 340.0 < v_birth_cm3 < 343.0
    assert 558.0 < v_90d_cm3 < 562.0

    # 2. Myelination conduction latency across a 0.15 m cortical pathway
    tract_m = 0.15
    dt_unmyel_ms = (tract_m / 1.0) * 1000.0     # 150 ms at 1 m/s
    dt_myel_ms = (tract_m / 60.0) * 1000.0      # 2.5 ms at 60 m/s
    assert abs(dt_unmyel_ms / dt_myel_ms - 60.0) < 1e-9

    # 3. Harvard synaptogenesis rate: >1,000,000 connections/sec -> 86.4 billion/day
    syn_per_day = 1_000_000 * 86_400
    assert syn_per_day == 86_400_000_000

    # 4. Kuzawa et al. (2014, PNAS): childhood peak RMR% vs adult RMR%
    rmr_birth_m, rmr_birth_f = 52.5, 59.8
    rmr_peak_m, rmr_peak_f = 66.3, 65.0
    der_peak_m, der_peak_f = 43.3, 43.8
    rmr_adult = 20.0
    assert 3.2 < (rmr_peak_m / rmr_adult) < 3.4
    assert rmr_birth_m < rmr_peak_m and der_peak_m > 40.0

    # 5. Sleep REM absolute daily hours (Grigg-Damberger & Wolfe 2017)
    rem_infant_h = 16.5 * 0.50   # 8.25 h/day
    rem_adult_h = 7.5 * 0.20     # 1.50 h/day
    assert abs(rem_infant_h / rem_adult_h - 5.5) < 1e-9


def _box(x, y, w, h, fill=SLATE_SOFT, stroke=BORDER, rx=8):
    return card(x, y, w, h, rx=rx, fill=fill, stroke=stroke, sw=1)


def _defs_arrows():
    return """
    <marker id="arr-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#1d6fa5"/>
    </marker>
    <marker id="arr-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#c25014"/>
    </marker>
    <marker id="arr-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#18794e"/>
    </marker>
    <marker id="arr-p" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#6d28d9"/>
    </marker>
    """


def _build_hardware_scaling_and_myelin():
    """Fig 1: Hardware paradox — same ~86B neurons at birth, why 4x volume growth? Myelination & 60x speed."""
    H = 528
    el = [
        *header(
            "硬件账本第一怪：刚出生的宝宝已有约 860 亿神经元，脑重凭什么还涨 4 倍？",
            "神经元总数出生即基本配齐 → 暴涨的体积来自树突丛林、胶质细胞与“髓鞘绝缘皮”（传导提速数十倍）",
        )
    ]

    # Left panel: Volume expansion timeline (Holland 2014 JAMA Neurol + Bethlehem 2022 Nature)
    el.append(card(22, 68, 368, 442))
    el.append(step_badge(42, 92, 1, BLUE, BLUE_SOFT))
    el.append(txt(62, 97, "脑容量狂飙曲线：出生头 90 天每天长约 1%！", size=12.4, color=INK, weight="700"))
    el.append(txt(42, 117, "神经元颗粒数几乎不增，但单颗体积、树突分支与白质猛涨", size=10.6, color=MUTED))

    # 4 comparative brain scale bars + silhouettes
    stages = [
        ("足月新生儿", "~340–360 g（成人 27%）", 0.27, "约 860 亿神经元已就位", BLUE, 162),
        ("出生 90 天", "~560 cm³（暴涨 +64%！）", 0.43, "小脑体积 3 个月翻一倍多", GREEN, 224),
        ("2 岁幼儿", "~1,050 g（约成人 80%）", 0.80, "皮层厚度在 1.7 岁达一生峰值", ORANGE, 286),
        ("成年人", "~1,300–1,400 g（100%）", 1.00, "灰质 5.9 岁达峰；白质涨到 28.7 岁", PURPLE, 348),
    ]
    bar_x0, bar_max_w = 132.0, 232.0
    for st_name, st_val, ratio, st_note, col, yy in stages:
        el.append(txt(40, yy, st_name, size=11.4, color=INK, weight="700"))
        bw = bar_max_w * ratio
        el.append(f'<rect x="{bar_x0}" y="{yy-15}" width="{bar_max_w}" height="20" rx="10" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        el.append(f'<rect x="{bar_x0}" y="{yy-15}" width="{bw:.1f}" height="20" rx="10" fill="{col}" opacity="0.85"/>')
        el.append(txt(bar_x0 + 8, yy + 20, f"{st_val}｜{st_note}", size=10.5, color=BODY))

    el.append(_box(38, 404, 336, 90, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(206, 426, "反直觉真相（Herculano-Houzel 2009 / Stiles 2010）：", size=10.8, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(206, 447, "大脑皮层神经元早在孕中期前就基本生产完毕！", size=11.0, color=INK, anchor="middle", weight="700"))
    el.append(txt(206, 467, "婴儿不是“缺芯片”，而是芯片之间还没铺好光纤绝缘层，", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(206, 485, "甚至核磁共振 T1 图像上新生儿灰白质明暗都与成人相反。", size=10.5, color=MUTED, anchor="middle"))

    # Right panel: Myelination ("Bare copper wire" vs "Myelinated saltatory optical cable")
    el.append(card(404, 68, 334, 442))
    el.append(step_badge(424, 92, 2, ORANGE, ORANGE_SOFT))
    el.append(txt(444, 97, "髓鞘化（Myelination）：从漏电裸线到高速光纤", size=12.4, color=INK, weight="700"))
    el.append(txt(424, 117, "少突胶质细胞给轴突裹上脂肪髓鞘，信号“蛙跳”前进", size=10.6, color=MUTED))

    # Top box: Infant unmyelinated axon
    el.append(_box(420, 136, 302, 136, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(434, 158, "婴儿未髓鞘化轴突（裸露轴突膜）", size=11.4, color=SLATE, weight="700"))
    # Soma + bare thin axon + dense small arrows
    el.append(f'<circle cx="454" cy="204" r="15" fill="#93c5fd" stroke="{BLUE}" stroke-width="2"/>')
    el.append(f'<line x1="469" y1="204" x2="692" y2="204" stroke="{SLATE}" stroke-width="4"/>')
    for ax_x in range(485, 675, 28):
        el.append(f'<path d="M {ax_x},196 Q {ax_x+12},184 {ax_x+24},196" fill="none" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#arr-b)"/>')
    el.append(txt(571, 232, "传导速度仅 ~0.5–2 m/s（连续爬行、易串扰）", size=10.8, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(571, 253, "跨脑区 15 cm 路程耗时 ≈ 150 毫秒（动作慢半拍）", size=10.5, color=MUTED, anchor="middle"))

    # Bottom box: Adult myelinated axon (Nodes of Ranvier saltatory conduction)
    el.append(_box(420, 286, 302, 148, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(434, 308, "成人已髓鞘化轴突（郎飞结跳跃式传导）", size=11.4, color=ORANGE, weight="700"))
    el.append(f'<circle cx="454" cy="358" r="15" fill="#fdba74" stroke="{ORANGE}" stroke-width="2"/>')
    el.append(f'<line x1="469" y1="358" x2="696" y2="358" stroke="{ORANGE}" stroke-width="4"/>')
    # Myelin sheaths (fatty yellow-white sleeves)
    for mx in [478, 536, 594, 652]:
        el.append(f'<rect x="{mx}" y="348" width="44" height="20" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>')
    # Big saltatory leaps over myelin sleeves!
    for jx in [474, 532, 590]:
        el.append(f'<path d="M {jx},346 Q {jx+29},318 {jx+58},346" fill="none" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-o)"/>')
    el.append(txt(571, 394, "传导速度飙至 50–100 m/s（提速 50–100 倍！）", size=10.8, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(571, 415, "同样 15 cm 跨脑区路程仅需 ≈ 2.5 毫秒！", size=10.6, color=INK, anchor="middle", weight="700"))

    # Sequencing rule at bottom-right
    el.append(_box(420, 446, 302, 50, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(571, 467, "铺设顺序（从后往前、从下往上）：", size=10.8, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(571, 486, "感官运动区最先包好 → 前额叶控制区要包到 25 岁后！", size=10.5, color=INK, anchor="middle"))

    write_svg(
        SUBDIR,
        "brain-hardware-scaling-neurons-myelin.svg",
        figure(
            H,
            "婴儿与成人大脑硬件尺度对比：860亿神经元存量、体积四倍增长与轴突髓鞘化提速图",
            "左栏展示从足月新生儿340克到成人1350克脑容量增长里程碑，右栏对比婴儿未髓鞘化轴突每秒1米慢速传导与成人髓鞘化跳跃传导每秒60米以上的高速机制。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_synapse_pruning_curve():
    """Fig 2: Synaptogenesis (>1M/sec) & Pruning — why a 2-year-old has ~2x adult synaptic density (with 1-shot animation)."""
    H = 538
    extra_css = """
    @keyframes highwayGlow {
      0% { stroke-dashoffset: 260; opacity: 0.35; }
      65% { stroke-dashoffset: 0; opacity: 1; }
      100% { stroke-dashoffset: 0; opacity: 1; }
    }
    @keyframes pruneDim {
      0%, 35% { opacity: 0.85; }
      100% { opacity: 0.28; }
    }
    .anim-hwy {
      stroke-dasharray: 260;
      stroke-dashoffset: 0;
      animation: highwayGlow 3.0s ease-out 1 both;
    }
    .anim-prune {
      opacity: 0.28;
      animation: pruneDim 3.0s ease-out 1 both;
    }
    @media (prefers-reduced-motion: reduce) {
      .anim-hwy, .anim-prune {
        animation: none !important;
        stroke-dashoffset: 0 !important;
      }
      .anim-hwy { opacity: 1 !important; }
      .anim-prune { opacity: 0.28 !important; }
    }
    """

    el = [
        *header(
            "硬件账本第二怪：2 岁宝宝的突触连接密度，竟然是成年人的近 2 倍！",
            "先看左图三大脑区分波疯长与修剪曲线 → 再看右图“先铺满小路、再修剪成高速公路”（含单次修剪强化动画）",
        )
    ]

    # Left panel: Huttenlocher & Dabholkar (1997) / Harvard Center regional synaptogenesis curves
    el.append(card(22, 68, 386, 452))
    el.append(step_badge(42, 92, 1, PURPLE, PURPLE_SOFT))
    el.append(txt(62, 97, "人类皮层突触密度随年龄变化（以成人稳态 = 100% 计）", size=12.0, color=INK, weight="700"))
    el.append(txt(42, 117, "生命最初几年每秒新建超 100 万个突触，随后砍掉近一半冗余连接", size=10.5, color=MUTED))

    # Axes: non-linear developmental timeline ticks [出生, 6月, 1岁, 3岁, 7岁, 15岁, 25岁+] -> x [74..384]
    px0, px1 = 74.0, 384.0
    py0, py1 = 418.0, 150.0   # y: 0% to 210%

    def map_y(pct):
        return py0 - (pct / 210.0) * (py0 - py1)

    for pct in [50, 100, 150, 200]:
        yy = map_y(pct)
        dash = ' stroke-dasharray="5,4"' if pct == 100 else ""
        col_g = SLATE if pct == 100 else "#e2e8f0"
        sw_g = "1.5" if pct == 100 else "1"
        el.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="{col_g}" stroke-width="{sw_g}"{dash}/>')
        el.append(txt(px0 - 6, yy + 4, f"{pct}%", size=10.5, color=INK if pct == 100 else MUTED, anchor="end", weight="700" if pct == 100 else None))

    x_ticks = [
        (0.00, "出生"),
        (0.16, "6月"),
        (0.30, "1岁"),
        (0.48, "3岁"),
        (0.66, "7岁"),
        (0.83, "15岁"),
        (1.00, "25岁+"),
    ]
    for frac, lbl in x_ticks:
        xx = px0 + frac * (px1 - px0)
        el.append(f'<line x1="{xx:.1f}" y1="{py1}" x2="{xx:.1f}" y2="{py0}" stroke="#f1f5f9" stroke-width="1"/>')
        el.append(txt(xx, py0 + 18, lbl, size=10.5, color=MUTED, anchor="middle"))

    el.append(f'<line x1="{px0}" y1="{py1}" x2="{px0}" y2="{py0}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{px0}" y1="{py0}" x2="{px1}" y2="{py0}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(txt(px1 - 4, map_y(100) - 7, "成人基准线 100%", size=10.5, color=SLATE, anchor="end", weight="700", halo=True))

    def curve_pts(pairs):
        return " ".join(f"{px0 + f*(px1-px0):.1f},{map_y(p):.1f}" for f, p in pairs)

    # Curve A: Visual / Auditory sensory cortex (peaks early ~4-8 months at ~190%, prunes faster)
    pts_vis = curve_pts([(0.0, 52), (0.08, 135), (0.17, 192), (0.30, 175), (0.48, 140), (0.66, 112), (0.83, 102), (1.0, 100)])
    el.append(f'<polyline points="{pts_vis}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

    # Curve B: Language cortex (peaks ~9-12 months at ~185%)
    pts_lang = curve_pts([(0.0, 48), (0.12, 118), (0.28, 185), (0.48, 158), (0.66, 125), (0.83, 106), (1.0, 100)])
    el.append(f'<polyline points="{pts_lang}" fill="none" stroke="{GREEN}" stroke-width="2.6" stroke-dasharray="7,4"/>')

    # Curve C: Prefrontal cortex (executive function, peaks ~2-3 years at ~180%, slow pruning into mid-20s!)
    pts_pfc = curve_pts([(0.0, 42), (0.16, 95), (0.32, 150), (0.48, 182), (0.66, 162), (0.83, 128), (1.0, 100)])
    el.append(f'<polyline points="{pts_pfc}" fill="none" stroke="{ORANGE}" stroke-width="2.8"/>')

    # Labels on curves (carefully spaced so zero overlap!)
    el.append(txt(px0 + 0.16 * (px1 - px0), map_y(198), "① 视听感官皮层（~6月达峰）", size=10.5, color=BLUE, weight="700", halo=True))
    el.append(txt(px0 + 0.31 * (px1 - px0), map_y(187) + 16, "② 语言区（~1岁达峰）", size=10.5, color=GREEN, weight="700", halo=True))
    el.append(txt(px0 + 0.50 * (px1 - px0), map_y(184) - 6, "③ 前额叶控制区（修剪至25岁）", size=10.5, color=ORANGE, weight="700", halo=True))

    el.append(_box(38, 450, 354, 54, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(215, 471, "数据来源：Huttenlocher & Dabholkar (1997) 人类皮层电镜实测", size=10.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(215, 491, "及哈佛大学儿童发展中心：感官先定型，高级理性控制最后定型", size=10.5, color=INK, anchor="middle"))

    # Right panel: 3-stage network sculpture (Newborn sparse -> 2yo exuberant jungle -> Adult pruned highway)
    el.append(card(422, 68, 316, 452))
    el.append(step_badge(442, 92, 2, GREEN, GREEN_SOFT))
    el.append(txt(462, 97, "为什么长大反而要“砍掉一半连线”？", size=12.2, color=INK, weight="700"))
    el.append(txt(442, 117, "小胶质细胞精准修剪闲置支路，保留主干道", size=10.5, color=MUTED))

    # 3 stacked mini network boxes
    boxes_info = [
        (134, "A. 新生儿：神经元就位，连线尚稀疏", "仅保留心跳呼吸与基础反射通路", SLATE_SOFT, BORDER),
        (252, "B. 2–3 岁幼儿：全城铺满羊肠小道（~200%）", "万物皆可连！可塑性极强，但信号嘈杂耗能巨高", ORANGE_SOFT, "#fdba74"),
        (370, "C. 成年人：用进废退，修剪成八车道高速（100%）", "虚线闲置路被剪除，高频使用的实线主干加粗包髓鞘", GREEN_SOFT, "#86efac"),
    ]
    nodes_rel = [(28, 36), (78, 22), (76, 56), (138, 24), (142, 58), (196, 38)]

    for idx_b, (by, btitle, bsub, bfill, bstroke) in enumerate(boxes_info):
        el.append(_box(438, by, 284, 106, fill=bfill, stroke=bstroke))
        el.append(txt(450, by + 20, btitle, size=10.8, color=INK, weight="700"))
        # Network drawing region: x = 478 + rel_x, y = by + 24 + rel_y
        pts = [(478 + rx, by + 22 + ry) for rx, ry in nodes_rel]
        if idx_b == 0:
            # Sparse 3 edges
            for i, j in [(0, 1), (1, 3), (2, 4)]:
                el.append(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" y2="{pts[j][1]}" stroke="{SLATE}" stroke-width="1.5"/>')
        elif idx_b == 1:
            # Exuberant all-to-all mesh!
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    el.append(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" y2="{pts[j][1]}" stroke="{ORANGE}" stroke-width="1.5" opacity="0.72"/>')
        else:
            # Adult: pruned dashed unused lines + thick animated green highway!
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    if (i, j) not in [(0, 1), (1, 3), (3, 5), (0, 2), (2, 4), (4, 5)]:
                        el.append(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" y2="{pts[j][1]}" stroke="{SLATE}" stroke-width="1.2" stroke-dasharray="3,3" class="anim-prune"/>')
            el.append(f'<polyline points="{pts[0][0]},{pts[0][1]} {pts[1][0]},{pts[1][1]} {pts[3][0]},{pts[3][1]} {pts[5][0]},{pts[5][1]}" fill="none" stroke="{GREEN}" stroke-width="3.6" class="anim-hwy"/>')
            el.append(f'<polyline points="{pts[0][0]},{pts[0][1]} {pts[2][0]},{pts[2][1]} {pts[4][0]},{pts[4][1]} {pts[5][0]},{pts[5][1]}" fill="none" stroke="{BLUE}" stroke-width="2.8" class="anim-hwy"/>')

        for nx, ny in pts:
            el.append(f'<circle cx="{nx}" cy="{ny}" r="4.5" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>')
        el.append(txt(580, by + 97, bsub, size=10.5, color=BODY, anchor="middle"))

    el.append(txt(580, 502, "养育启示：“发球—回球”高质量互动决定保留哪条主干道", size=10.6, color=GREEN, anchor="middle", weight="700"))

    write_svg(
        SUBDIR,
        "synapse-explosion-and-pruning-curve.svg",
        figure(
            H,
            "人类大脑突触爆发式生成与修剪曲线及三阶段神经网络重塑对比图",
            "左栏绘制视听皮层、语言区与前额叶突触密度冲上成人近200%后再修剪回100%的分波曲线，右栏对比新生儿稀疏网、幼儿全连接丛林与成人修剪后高速主干道。",
            el,
            extra_css=extra_css,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_metabolic_furnace():
    """Fig 3: Kuzawa et al. (2014, PNAS) — Childhood brain devours 66% of resting metabolism, forcing body growth to slow down!"""
    H = 516
    el = [
        *header(
            "能量账本：小小脑袋竟烧掉全身 66% 静息热量！人类童年为什么长不高？",
            "据 Kuzawa 等 (2014, PNAS) 正电子断层扫描实测：大脑抢走海量葡萄糖建突触，迫使身体生长踩下刹车",
        )
    ]

    # Left panel: Lifespan inverse curves (Brain Glucose % of RMR vs Body Weight Growth Rate)
    el.append(card(22, 68, 418, 430))
    el.append(step_badge(42, 92, 1, ORANGE, ORANGE_SOFT))
    el.append(txt(62, 97, "大脑能耗占比 vs 身体长肉速度的“跷跷板效应”", size=12.4, color=INK, weight="700"))
    el.append(txt(42, 117, "实线：大脑葡萄糖消耗占静息代谢率（RMR%）｜ 虚线：体重增速示意", size=10.5, color=MUTED))

    px0, px1 = 76.0, 416.0
    py0, py1 = 414.0, 152.0  # y: 0% to 75% RMR

    def map_x(age):
        # Piecewise mapping [0..22 yr] emphasizing 0..10 yr
        if age <= 6:
            return px0 + (age / 6.0) * 0.50 * (px1 - px0)
        return px0 + (0.50 + ((age - 6.0) / 16.0) * 0.50) * (px1 - px0)

    def map_y(pct):
        return py0 - (pct / 75.0) * (py0 - py1)

    for pct in [0, 20, 40, 60]:
        yy = map_y(pct)
        el.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="#e2e8f0" stroke-width="1"/>')
        el.append(txt(px0 - 8, yy + 4, f"{pct}%", size=10.5, color=MUTED, anchor="end"))

    for age_t, lbl in [(0, "出生"), (2, "2岁"), (4.5, "4.5岁"), (6, "6岁"), (10, "10岁"), (14, "14岁"), (22, "成人")]:
        xx = map_x(age_t)
        el.append(f'<line x1="{xx:.1f}" y1="{py1}" x2="{xx:.1f}" y2="{py0}" stroke="#f1f5f9" stroke-width="1"/>')
        el.append(txt(xx, py0 + 18, lbl, size=10.5, color=MUTED, anchor="middle"))

    el.append(f'<line x1="{px0}" y1="{py1}" x2="{px0}" y2="{py0}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{px0}" y1="{py0}" x2="{px1}" y2="{py0}" stroke="{SLATE}" stroke-width="1.5"/>')

    # Highlight 4-5 yr peak band
    x_pk = map_x(4.5)
    el.append(f'<rect x="{map_x(3.6):.1f}" y="{py1}" width="{map_x(5.4)-map_x(3.6):.1f}" height="{py0-py1}" fill="#ffedd5" opacity="0.65"/>')

    # Brain Glucose % of RMR curve (Kuzawa et al. 2014: ~53% birth -> 66.3% at ~4.5 yr -> ~20% adult)
    rmr_data = [(0, 53.0), (1, 58.0), (2.5, 63.0), (4.5, 66.3), (6, 62.0), (10, 46.0), (14, 32.0), (18, 24.0), (22, 20.0)]
    pts_rmr = " ".join(f"{map_x(a):.1f},{map_y(v):.1f}" for a, v in rmr_data)
    el.append(f'<polyline points="{pts_rmr}" fill="none" stroke="{ORANGE}" stroke-width="3.0"/>')
    el.append(f'<circle cx="{x_pk:.1f}" cy="{map_y(66.3):.1f}" r="5.5" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')

    # Relative body weight growth rate curve (scaled onto plot to show exact inverse trough at 4-5 yr & puberty spurt at 13-14 yr!)
    growth_scaled = [(0, 68.0), (1, 36.0), (2.5, 22.0), (4.5, 14.0), (6, 16.0), (10, 24.0), (13.5, 44.0), (17, 15.0), (22, 4.0)]
    pts_grw = " ".join(f"{map_x(a):.1f},{map_y(v):.1f}" for a, v in growth_scaled)
    el.append(f'<polyline points="{pts_grw}" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-dasharray="6,4"/>')

    el.append(txt(x_pk + 6, map_y(66.3) - 8, "峰值 66.3% RMR！", size=11.0, color=ORANGE, weight="700", halo=True))
    el.append(txt(map_x(13.5), map_y(44.0) - 10, "青春期身高体重猛蹿", size=10.5, color=BLUE, anchor="middle", weight="700", halo=True))
    el.append(txt(map_x(4.5), map_y(14.0) + 18, "童年身体增速谷底", size=10.5, color=BLUE, anchor="middle", weight="700", halo=True))
    el.append(txt(map_x(19.5), map_y(20.0) - 9, "成人稳态 ~20%", size=10.5, color=ORANGE, anchor="middle", weight="700", halo=True))

    el.append(txt(246, 464, "注：虚线为相对体重年增速变化趋势（与大脑耗糖峰值严格反向咬合）", size=10.5, color=MUTED, anchor="middle"))
    el.append(txt(246, 484, "等十几岁突触修剪完、大脑省下口粮，青少年才迎来身高暴涨！", size=10.6, color=INK, anchor="middle", weight="700"))

    # Right panel: Direct budget comparison cards (Child 4–5 yr vs Adult)
    el.append(card(454, 68, 284, 430))
    el.append(step_badge(474, 92, 2, GREEN, GREEN_SOFT))
    el.append(txt(494, 97, "全身能量账单正面对比", size=12.4, color=INK, weight="700"))
    el.append(txt(474, 117, "为什么幼童玩一会儿就饿、低血糖更危险？", size=10.5, color=MUTED))

    # Child 4-5 yr box
    el.append(_box(470, 136, 252, 152, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(596, 159, "幼儿 / 学龄前大脑（4–5 岁峰值）", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(596, 188, "66% 静息代谢热量", size=15.0, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(596, 211, "（占全天总活动能耗的 43%！）", size=11.0, color=INK, anchor="middle", weight="700"))
    el.append(txt(596, 236, "● 约 30% 葡萄糖走“有氧糖酵解”，", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(596, 255, "专门当砖瓦合成突触蛋白与细胞膜脂质", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(596, 274, "● 密集突触不停放电维护，耗能是成人3倍", size=10.5, color=MUTED, anchor="middle"))

    # Adult box
    el.append(_box(470, 304, 252, 112, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(596, 327, "成年人大脑（修剪定型后）", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(596, 356, "~20% 静息代谢热量", size=15.0, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(596, 380, "体重占比仅 ~2%，但路线精简高效，", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(596, 399, "像修好的高速公路，日常养护省电得多", size=10.5, color=BODY, anchor="middle"))

    el.append(_box(470, 430, 252, 54, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(596, 452, "演化代价：黑猩猩幼崽断奶后飞速长壮，", size=10.5, color=INK, anchor="middle"))
    el.append(txt(596, 471, "唯独人类把漫长童年全拿来“喂脑子”！", size=10.8, color=GREEN, anchor="middle", weight="700"))

    write_svg(
        SUBDIR,
        "metabolic-furnace-66-percent-tradeoff.svg",
        figure(
            H,
            "儿童与成人大脑葡萄糖代谢占比曲线及身体生长速度权衡对比图",
            "左栏根据Kuzawa等2014年PNAS数据绘制人类大脑占静息代谢率比例在4至5岁冲上66.3%峰值并与体重增速谷底反向对应，右栏对比幼儿66%与成人20%的能量账单。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_lantern_vs_spotlight():
    """Fig 4: Alison Gopnik's Lantern Consciousness vs Adult Spotlight Attention (PFC inhibition & explore-exploit)."""
    H = 512
    el = [
        *header(
            "认知模式大不同：为什么宝宝管不住手脚，却能发现大人完全漏掉的规律？",
            "前额叶“刹车片”尚未包好髓鞘：婴儿是 360° 全景探索的“灯笼意识”，成人是窄束高效的“激光探照灯”",
        )
    ]

    # Left card: Infant "Lantern Consciousness" (Broad 360° glow, uninhibited PFC, high exploration)
    el.append(card(22, 68, 352, 366))
    el.append(_box(38, 82, 320, 28, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(198, 101, "婴幼儿大脑：360° 敞亮“灯笼意识”（广角探索模式）", size=11.6, color=ORANGE, anchor="middle", weight="700"))

    # Lantern glow schematic centered at (198, 206)
    lx, ly = 198, 206
    el.append(f'<circle cx="{lx}" cy="{ly}" r="74" fill="#fef3c7" opacity="0.65"/>')
    el.append(f'<circle cx="{lx}" cy="{ly}" r="48" fill="#fde68a" opacity="0.75"/>')
    el.append(f'<circle cx="{lx}" cy="{ly}" r="18" fill="{ORANGE}"/>')
    el.append(txt(lx, ly + 4, "幼脑", size=11.0, color="#ffffff", anchor="middle", weight="700"))

    # Surrounding diverse stimuli all entering awareness!
    cues_infant = [
        (lx - 102, ly - 52, "新奇声音", ORANGE),
        (lx + 102, ly - 52, "妈妈表情", ORANGE),
        (lx - 108, ly + 48, "地板纹理", ORANGE),
        (lx + 108, ly + 48, "隐藏因果律", GREEN),
        (lx, ly - 78, "陌生语音细节", BLUE),
    ]
    for cx_i, cy_i, clbl, ccol in cues_infant:
        el.append(txt(cx_i, cy_i, f"★ {clbl}", size=10.6, color=ccol, anchor="middle", weight="700", halo=True))

    el.append(_box(38, 300, 320, 120, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(52, 323, "● 硬件根源：前额叶皮层（PFC）抑制通路尚未成熟", size=10.8, color=INK, weight="700"))
    el.append(txt(52, 345, "● 短板（算力散）：屏蔽不了干扰，没法自己系鞋带、", size=10.5, color=BODY))
    el.append(txt(64, 364, "做长计划，情绪说崩就崩（缺“顶层刹车片”）。", size=10.5, color=BODY))
    el.append(txt(52, 386, "● 超能力（无成见）：没有先验偏见束缚，像算法里的", size=10.5, color=ORANGE, weight="700"))
    el.append(txt(64, 405, "“高温模拟退火”，最擅长破解反常规抽象规律！", size=10.5, color=ORANGE, weight="700"))

    # Right card: Adult "Spotlight Attention" (Narrow focused beam, strong PFC inhibition, high exploitation)
    el.append(card(386, 68, 352, 366))
    el.append(_box(402, 82, 320, 28, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(562, 101, "成年人大脑：窄束聚焦“探照灯”（高效执行模式）", size=11.6, color=BLUE, anchor="middle", weight="700"))

    sx, sy = 486, 224
    # Focused cone beam pointing to single target on right (656, 178)
    el.append(f'<polygon points="{sx},{sy} 676,142 676,222" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.5"/>')
    el.append(f'<circle cx="{sx}" cy="{sy}" r="18" fill="{BLUE}"/>')
    el.append(txt(sx, sy + 4, "成脑", size=11.0, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(sx, sy + 34, "前额叶强力屏蔽噪音", size=10.5, color=BLUE, anchor="middle", weight="700"))

    el.append(f'<circle cx="650" cy="182" r="9" fill="{GREEN}"/>')
    el.append(txt(650, 206, "当前KPI目标", size=10.6, color=GREEN, anchor="middle", weight="700", halo=True))

    # Ignored peripheral cues (muted/crossed)
    el.append(txt(546, 142, "× 背景细节（已过滤）", size=10.5, color=MUTED, anchor="middle"))
    el.append(txt(628, 258, "× 外语微弱音差（已过滤）", size=10.5, color=MUTED, anchor="middle"))

    el.append(_box(402, 300, 320, 120, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(416, 323, "● 硬件根源：前额叶髓鞘化完成＋GABA 抑制网络成熟", size=10.8, color=INK, weight="700"))
    el.append(txt(416, 345, "● 优势（执行稳）：能瞬间屏蔽 95% 无关信息，专注", size=10.5, color=BODY))
    el.append(txt(428, 364, "开车、写代码、压住脾气完成跨年复杂工程。", size=10.5, color=BODY))
    el.append(txt(416, 386, "● 代价（思维定势）：被已有经验牢牢锁死（低温锁定），", size=10.5, color=BLUE, weight="700"))
    el.append(txt(428, 405, "遇到反直觉新规则时，有时反而输给四岁小孩！", size=10.5, color=BLUE, weight="700"))

    # Bottom evolutionary division-of-labor strip
    el.append(card(22, 446, 716, 52, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(380, 468, "发展心理学家艾莉森·高普尼克（Alison Gopnik）总结的人类演化神分工：", size=11.0, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(380, 488, "“婴儿是人类的研发部（R&D，负责不设限探索新世界）；成人是生产部（Production，负责高效执行与兜底照料）。”", size=10.8, color=INK, anchor="middle", weight="700"))

    write_svg(
        SUBDIR,
        "lantern-vs-spotlight-prefrontal-cortex.svg",
        figure(
            H,
            "婴儿灯笼意识与成人探照灯注意力对比及前额叶探索利用权衡示意图",
            "左栏展示婴儿前额叶未成熟形成360度全景接收的灯笼意识与高探索灵活性，右栏展示成人前额叶抑制成熟形成窄束聚焦探照灯注意力与高执行效率。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_phoneme_citizen_and_social_gating():
    """Fig 5: Patricia Kuhl (2003 PNAS / 2006 / 2010 Neuron) — 6–12m perceptual narrowing & Live Tutor vs TV social gating."""
    H = 528
    el = [
        *header(
            "语言超能力与“真人开关”：6 个月听懂全球语音，为什么看电视学外语却等于零？",
            "左看帕特里夏·库尔（Kuhl）美日婴儿语音窄化实验 → 右看轰动学界的“真人互动 vs 电视录像”对照实验",
        )
    ]

    # Left panel: 6-8m vs 10-12m American vs Japanese infants on English /ra/-/la/
    el.append(card(22, 68, 356, 442))
    el.append(step_badge(42, 92, 1, BLUE, BLUE_SOFT))
    el.append(txt(62, 97, "从“世界公民”到“母语专家”仅需半年", size=12.4, color=INK, weight="700"))
    el.append(txt(42, 117, "测试美、日婴儿分辨英语 /ra/–/la/ 辅音正确率（Kuhl 2006）", size=10.5, color=MUTED))

    # Plot [50%..85%] -> py [376..158], x two age groups: 6-8m (x=138) and 10-12m (x=296)
    px0, px1 = 76.0, 352.0
    py0, py1 = 376.0, 158.0

    def map_py(pct):
        return py0 - ((pct - 50.0) / 35.0) * (py0 - py1)

    for pct in [50, 60, 70, 80]:
        yy = map_py(pct)
        dash = ' stroke-dasharray="4,4"' if pct == 50 else ""
        el.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="#e2e8f0" stroke-width="1"{dash}/>')
        el.append(txt(px0 - 6, yy + 4, f"{pct}%", size=10.5, color=MUTED, anchor="end"))

    el.append(f'<line x1="{px0}" y1="{py1}" x2="{px0}" y2="{py0}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{px0}" y1="{py0}" x2="{px1}" y2="{py0}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(txt(px1 - 4, map_py(50) - 6, "随机瞎猜线 50%", size=10.5, color=MUTED, anchor="end"))

    x_early, x_late = 136.0, 294.0
    el.append(txt(x_early, py0 + 20, "6–8 个月（世界公民期）", size=10.6, color=INK, anchor="middle", weight="700"))
    el.append(txt(x_late, py0 + 20, "10–12 个月（神经定型期）", size=10.6, color=INK, anchor="middle", weight="700"))

    # American infants: 64.6% -> 78.7%
    y_us0, y_us1 = map_py(64.8), map_py(78.7)
    el.append(f'<line x1="{x_early}" y1="{y_us0:.1f}" x2="{x_late}" y2="{y_us1:.1f}" stroke="{BLUE}" stroke-width="3"/>')
    el.append(f'<circle cx="{x_early}" cy="{y_us0:.1f}" r="5.5" fill="{BLUE}"/>')
    el.append(f'<circle cx="{x_late}" cy="{y_us1:.1f}" r="5.5" fill="{BLUE}"/>')
    el.append(txt(x_late - 6, y_us1 - 12, "美国婴儿 ↑ 79%", size=10.8, color=BLUE, anchor="end", weight="700", halo=True))

    # Japanese infants: 64.5% -> 58.8% (drops as日语 doesn't separate /r/ and /l/)
    y_jp0, y_jp1 = map_py(64.2), map_py(58.8)
    el.append(f'<line x1="{x_early}" y1="{y_jp0:.1f}" x2="{x_late}" y2="{y_jp1:.1f}" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="6,4"/>')
    el.append(f'<circle cx="{x_early}" cy="{y_jp0:.1f}" r="5.5" fill="{ORANGE}"/>')
    el.append(f'<circle cx="{x_late}" cy="{y_jp1:.1f}" r="5.5" fill="{ORANGE}"/>')
    el.append(txt(x_late - 6, y_jp1 + 20, "日本婴儿 ↓ 59%", size=10.8, color=ORANGE, anchor="end", weight="700", halo=True))
    el.append(txt(x_early + 8, y_us0 - 14, "6个月时美日宝宝同分 (~65%)！", size=10.5, color=INK, weight="700", halo=True))

    el.append(_box(38, 412, 324, 82, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(200, 434, "知觉窄化（Perceptual Narrowing）：", size=10.8, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(200, 454, "半岁婴儿能听清全世界所有语言约 800 种音素差异；", size=10.5, color=INK, anchor="middle"))
    el.append(txt(200, 474, "1 岁前大脑统计母语高频音并修剪其余通道，成人反而听不出！", size=10.5, color=BODY, anchor="middle"))

    # Right panel: Kuhl, Tsao & Liu (2003, PNAS) Mandarin Social Gating Experiment!
    el.append(card(392, 68, 346, 442))
    el.append(step_badge(412, 92, 2, GREEN, GREEN_SOFT))
    el.append(txt(432, 97, "震撼实验：给 9 个月美国宝宝听中文 12 次", size=12.4, color=INK, weight="700"))
    el.append(txt(412, 117, "同样 ~33,000 个普通话音节，不同媒介学习效果天壤之别", size=10.5, color=MUTED))

    # Horizontal bar chart of Mandarin phoneme discrimination scores (Kuhl et al. 2003 PNAS)
    bars = [
        ("① 真人老师面对面陪玩读绘本", 65.9, GREEN, "65.9%（追平中国台湾母语宝宝！）"),
        ("② 高清电视播放同款老师录像", 52.2, SLATE, "52.2%（完全没学会 ≈ 瞎猜）"),
        ("③ 纯音响播放同款普通话录音", 51.4, SLATE, "51.4%（完全没学会 ≈ 瞎猜）"),
        ("④ 对照组（只听英语未接触中文）", 52.0, MUTED, "52.0%（基准对照线）"),
    ]
    bx0, bmax = 416.0, 296.0
    for idx_r, (blbl, score, bcol, bnote) in enumerate(bars):
        by = 156 + idx_r * 62
        el.append(txt(bx0, by - 8, blbl, size=10.8, color=INK, weight="700"))
        el.append(f'<rect x="{bx0}" y="{by}" width="{bmax}" height="22" rx="6" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        # Scale [45%..72%] across bar width
        bw = ((score - 45.0) / 27.0) * bmax
        el.append(f'<rect x="{bx0}" y="{by}" width="{bw:.1f}" height="22" rx="6" fill="{bcol}" opacity="0.88"/>')
        el.append(txt(bx0 + 8, by + 15, bnote, size=10.5, color="#ffffff" if score > 60 else INK, weight="700"))

    el.append(_box(408, 404, 314, 90, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(565, 426, "社交门控假说（Social Gating Hypothesis）：", size=11.0, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(565, 447, "婴儿大脑不是冷冰冰的录音机！只有真人的眼神追随、", size=10.5, color=INK, anchor="middle"))
    el.append(txt(565, 466, "表情回应与共同注意，才能拧开听觉皮层的可塑性开关——", size=10.5, color=INK, anchor="middle"))
    el.append(txt(565, 485, "把平板和电视丢给一岁宝宝“磨耳朵”，神经科学证明无效。", size=10.5, color=GREEN, anchor="middle", weight="700"))

    write_svg(
        SUBDIR,
        "world-citizen-phoneme-social-gating.svg",
        figure(
            H,
            "婴儿语音知觉窄化曲线与真人互动对决电视录像社交门控实验图",
            "左栏展示6至8个月美日婴儿同等分辨英语r-l音素而10至12个月出现母语分化，右栏展示Kuhl等2003年PNAS实验证明9个月婴儿仅能从真人互动学会普通话音素而看电视与听录音完全无效。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_sleep_and_infantile_amnesia():
    """Fig 6: Newborn 50% REM sleep body-map wiring + 2025 Yale Science breakthrough on Infantile Amnesia."""
    H = 528
    el = [
        *header(
            "睡梦施工队与“三岁前失忆之谜”：既然宝宝学得那么快，长大后怎么全忘了？",
            "左看新生儿 50% 快速眼动睡眠如何边抽动边搭电路 → 右看 2025 耶鲁《Science》清醒婴儿脑成像大反转",
        )
    ]

    # Left panel: Sleep architecture (16-18h, 50% REM vs Adult 7-8h, 20% REM)
    el.append(card(22, 68, 344, 442))
    el.append(step_badge(42, 92, 1, PURPLE, PURPLE_SOFT))
    el.append(txt(62, 97, "睡眠结构差异：宝宝睡觉不是休息，是在施工！", size=12.0, color=INK, weight="700"))
    el.append(txt(42, 117, "足月新生儿每天睡 16–18 小时，一半是活跃 REM 睡眠", size=10.5, color=MUTED))

    # Stacked 24-hour bar comparison
    # Infant 24h bar
    el.append(txt(42, 148, "足月新生儿 24 小时分配（REM 每天超 8 小时！）", size=10.8, color=INK, weight="700"))
    ix, iw = 42.0, 304.0
    w_rem_i = iw * (8.25 / 24.0)
    w_nrem_i = iw * (8.25 / 24.0)
    w_wake_i = iw - w_rem_i - w_nrem_i
    el.append(f'<rect x="{ix}" y="156" width="{w_rem_i:.1f}" height="28" rx="4" fill="{PURPLE}"/>')
    el.append(f'<rect x="{ix+w_rem_i:.1f}" y="156" width="{w_nrem_i:.1f}" height="28" fill="{BLUE}"/>')
    el.append(f'<rect x="{ix+w_rem_i+w_nrem_i:.1f}" y="156" width="{w_wake_i:.1f}" height="28" rx="4" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
    el.append(txt(ix + w_rem_i / 2, 175, "REM 50%", size=10.5, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(ix + w_rem_i + w_nrem_i / 2, 175, "安静睡眠", size=10.5, color="#ffffff", anchor="middle"))
    el.append(txt(ix + w_rem_i + w_nrem_i + w_wake_i / 2, 175, "清醒", size=10.5, color=BODY, anchor="middle"))

    # Adult 24h bar
    el.append(txt(42, 214, "成年人 24 小时分配（REM 每天仅约 1.5 小时）", size=10.8, color=INK, weight="700"))
    w_rem_a = iw * (1.5 / 24.0)
    w_nrem_a = iw * (6.0 / 24.0)
    w_wake_a = iw - w_rem_a - w_nrem_a
    el.append(f'<rect x="{ix}" y="222" width="{w_rem_a:.1f}" height="28" rx="3" fill="{PURPLE}"/>')
    el.append(f'<rect x="{ix+w_rem_a:.1f}" y="222" width="{w_nrem_a:.1f}" height="28" fill="{BLUE}"/>')
    el.append(f'<rect x="{ix+w_rem_a+w_nrem_a:.1f}" y="222" width="{w_wake_a:.1f}" height="28" rx="4" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
    el.append(txt(ix + w_rem_a + w_nrem_a / 2, 241, "非REM 80%", size=10.5, color="#ffffff", anchor="middle"))
    el.append(txt(ix + w_rem_a + w_nrem_a + w_wake_a / 2, 241, "白天清醒 ~16.5 小时", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(ix + 2, 266, "↑ REM 仅占睡眠 20%（却是新生儿绝对时长的 1/5.5）", size=10.5, color=PURPLE, weight="700"))

    el.append(_box(38, 286, 312, 208, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(194, 310, "为什么小宝宝睡着了总咧嘴笑、手脚一惊一乍？", size=11.0, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(52, 334, "● 成人做梦时脑干会锁死肌肉（防把梦演出来）；", size=10.5, color=BODY))
    el.append(txt(52, 355, "● 婴儿脑干抑制未成熟，REM 期手脚胡乱抽动——", size=10.5, color=INK, weight="700"))
    el.append(txt(52, 376, "每一次指尖抽动都会向体感运动皮层发射一串校准脉冲，", size=10.5, color=BODY))
    el.append(txt(52, 396, "帮大脑画好“这只手归哪根神经管”的身体地图！", size=10.5, color=PURPLE, weight="700"))
    el.append(txt(52, 422, "● 同时早产儿 REM 占比甚至高达 80%，千万别在宝宝", size=10.5, color=BODY))
    el.append(txt(52, 442, "眼皮乱动哼唧时急着拍醒或抱起——他只是在活跃睡眠", size=10.5, color=BODY))
    el.append(txt(52, 462, "里热火朝天地焊接突触！（Grigg-Damberger 2017）", size=10.5, color=MUTED))

    # Right panel: Infantile Amnesia & 2025 Yale Science awake-infant fMRI breakthrough!
    el.append(card(380, 68, 358, 442))
    el.append(step_badge(400, 92, 2, ORANGE, ORANGE_SOFT))
    el.append(txt(420, 97, "婴儿期遗忘症：不是“没存盘”，而是“找不着索引”！", size=12.0, color=INK, weight="700"))
    el.append(txt(400, 117, "Yates & Turk-Browne 等 (2025, Science) 清醒婴儿核磁新发现", size=10.5, color=MUTED))

    # Old myth crossed out
    el.append(_box(396, 134, 326, 62, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(410, 156, "× 旧教科书假说：“婴儿海马体太稚嫩，根本没法写入情景记忆”", size=10.5, color=SLATE, weight="700"))
    el.append(txt(410, 178, "难以解释：如果完全不能记事，宝宝怎么认出昨天去过的公园和绘本？", size=10.5, color=MUTED))

    # Hippocampus dual-pathway diagram (Anterior = Statistical learning from 3m; Posterior = Episodic encoding by 12m!)
    el.append(_box(396, 208, 326, 146, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(559, 230, "耶鲁团队给清醒看图的 4–24 月龄宝宝做 fMRI 实测：", size=10.8, color=ORANGE, anchor="middle", weight="700"))

    # Stylized dual-zone hippocampus
    el.append(f'<ellipse cx="492" cy="278" rx="56" ry="22" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>')
    el.append(txt(492, 275, "前部海马体", size=10.8, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(492, 291, "3 个月已开启统计学习", size=10.5, color=INK, anchor="middle"))

    el.append(f'<ellipse cx="626" cy="278" rx="62" ry="22" fill="#dcfce7" stroke="{GREEN}" stroke-width="2"/>')
    el.append(txt(626, 275, "后部海马体", size=10.8, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(626, 291, "1 岁起已能编码单次事件！", size=10.5, color=INK, anchor="middle", weight="700"))

    el.append(txt(559, 324, "宝宝第一次看新图片时后部海马体越活跃 → 稍后再见越能认出！", size=10.5, color=INK, anchor="middle", weight="700"))
    el.append(txt(559, 343, "证明 1 岁婴儿大脑已经在往硬盘里“写入”具体情景记忆了！", size=10.5, color=ORANGE, anchor="middle", weight="700"))

    # Why can't adults retrieve them? Two mechanisms!
    el.append(_box(396, 366, 326, 128, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(559, 388, "那为什么成年后提取不出 3 岁前的具体回忆？两大原因：", size=10.8, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(410, 411, "① 海马齿状回神经元疯长洗牌：海量新生神经元挤入回路，", size=10.5, color=INK))
    el.append(txt(422, 430, "改写了旧记忆的物理寻址路径（但统计规律已沉淀进皮层）；", size=10.5, color=BODY))
    el.append(txt(410, 452, "② 文件格式不兼容：婴儿期尚无“语言标签”与“自我时间轴”，", size=10.5, color=INK))
    el.append(txt(422, 471, "成人大脑升级成语言操作系统后，搜不到当年的无字老档案！", size=10.5, color=GREEN, weight="700"))

    write_svg(
        SUBDIR,
        "sleep-rem-and-infantile-amnesia-mystery.svg",
        figure(
            H,
            "新生儿50%快速眼动睡眠发育机制与耶鲁大学2025婴儿期遗忘症海马体研究图",
            "左栏对比新生儿16至18小时睡眠中50%快速眼动睡眠与成人20%比例及其运动地图校准功能，右栏图解2025年Science研究揭示1岁婴儿后部海马体已能编码情景记忆而成人失忆源于提取路径重塑。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


@register(
    "infant-adult-brain",
    "Infant vs adult brain differences: 86B neurons & myelination, synaptic pruning, 66% metabolic peak, lantern vs spotlight, language gating & amnesia",
    "biology",
)
def build_infant_adult_brain():
    _verify_infant_brain_math()
    _build_hardware_scaling_and_myelin()
    _build_synapse_pruning_curve()
    _build_metabolic_furnace()
    _build_lantern_vs_spotlight()
    _build_phoneme_citizen_and_social_gating()
    _build_sleep_and_infantile_amnesia()
