"""Quantitative & step-by-step SVG visuals for Lotus Root Browning & Everyday Chemistry.

Generates 5 verified 760x520 figures under assets/images/lotus-browning/:
1. compartmentalization-and-ppo-anim.svg (1-shot CSS animation + reduced-motion fallback)
2. iron-wok-and-ancient-ink.svg
3. kitchen-anti-blackening-curves.svg
4. everyday-ppo-heroes-and-villains.svg
5. four-brownings-comparison-map.svg
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

SUBDIR = "lotus-browning"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
BROWN = "#6b4423"
BROWN_SOFT = "#f8f1ea"
INDIGO = "#312e81"
INDIGO_SOFT = "#eef2ff"


def _lotus_slice_svg(cx, cy, r, fill_body, stroke_col, hole_fill="#ffffff", cls=None):
    """Draw an iconic 7-hole lotus root cross-section."""
    cls_attr = f' class="{cls}"' if cls else ""
    parts = [
        f'<g{cls_attr}>',
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill_body}" stroke="{stroke_col}" stroke-width="2"/>',
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.16:.1f}" fill="{hole_fill}" stroke="{stroke_col}" stroke-width="1"/>',
    ]
    for k in range(7):
        ang = math.radians(k * (360.0 / 7.0) - 90.0)
        hx = cx + r * 0.56 * math.cos(ang)
        hy = cy + r * 0.56 * math.sin(ang)
        parts.append(
            f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{r * 0.17:.1f}" ry="{r * 0.12:.1f}" '
            f'transform="rotate({k * (360.0 / 7.0):.1f} {hx:.1f} {hy:.1f})" '
            f'fill="{hole_fill}" stroke="{stroke_col}" stroke-width="1"/>'
        )
    parts.append("</g>")
    return "\n".join(parts)


def _ppo_temp_activity(temp_c):
    """Normalized lotus root PPO relative activity (%) across 0..100 C.

    Anchored to verified experimental optimum T_opt = 35.0 C (Li et al., Food Chem. 2023)
    and irreversible thermal denaturation above 80-90 C.
    """
    if temp_c <= 35.0:
        # Q10-like rise from ~20% at 0 C to 100% at 35 C
        val = 100.0 * math.exp(-((temp_c - 35.0) / 27.5) ** 2)
    else:
        # Sharper thermal unfolding falloff above 35 C -> <2% by 85 C, 0% at >=92 C
        if temp_c >= 92.0:
            return 0.0
        val = 100.0 * math.exp(-((temp_c - 35.0) / 23.0) ** 2.25)
    return max(0.0, min(100.0, val))


def _ppo_ph_activity(ph):
    """Normalized lotus root PPO relative activity (%) across pH 2.0..9.5.

    Anchored to verified experimental optimum pH_opt = 6.5 (Li et al., Food Chem. 2023)
    and strong acid inhibition (<8% below pH 3.5).
    """
    if ph <= 6.5:
        val = 100.0 * math.exp(-(abs(ph - 6.5) / 1.95) ** 2.1)
    else:
        val = 100.0 * math.exp(-(abs(ph - 6.5) / 1.75) ** 2.0)
    return max(0.0, min(100.0, val))


def build_compartmentalization_and_ppo_anim():
    """SVG 1: Cell compartmentalization vs. knife rupture + PPO browning animation."""
    assert abs(_ppo_temp_activity(35.0) - 100.0) < 1e-6
    assert abs(_ppo_ph_activity(6.5) - 100.0) < 1e-6

    extra_css = """
  @keyframes bladeDrop {
    0% { transform: translateY(-6px); opacity: 0.35; }
    22% { transform: translateY(4px); opacity: 1; }
    100% { transform: translateY(4px); opacity: 1; }
  }
  @keyframes o2Enter {
    0%, 15% { transform: translate(-18px, -6px); opacity: 0; }
    42%, 100% { transform: translate(0px, 0px); opacity: 1; }
  }
  @keyframes sliceDarken {
    0%, 30% { opacity: 0; }
    65% { opacity: 0.55; }
    100% { opacity: 1; }
  }
  @keyframes stepGlow {
    0%, 45% { opacity: 0.35; }
    78%, 100% { opacity: 1; }
  }
  .anim-blade { animation: bladeDrop 6.2s ease-out 1 forwards; }
  .anim-o2 { animation: o2Enter 6.2s ease-out 1 forwards; }
  .anim-dark-slice { animation: sliceDarken 6.2s ease-in-out 1 forwards; }
  .anim-final { animation: stepGlow 6.2s ease-out 1 forwards; }
  @media (prefers-reduced-motion: reduce) {
    .anim-blade, .anim-o2, .anim-dark-slice, .anim-final {
      animation: none !important;
      opacity: 1 !important;
      transform: none !important;
    }
  }
    """

    el = []
    el.extend(
        header(
            "凶手一（酶促褐变）：完整莲藕雪白脆嫩，凭什么一刀切开就发黑？",
            "核心机制：细胞区室化隔离被刀刃打破，液泡多酚、质体双铜酶（PPO）与空气氧气三方会师",
        )
    )

    # Left panel: Intact cell
    el.append(card(24, 66, 338, 232, fill=CARD_BG, stroke=BORDER))
    el.append(pill(38, 78, "状态 A：淤泥里的完整细胞（分区上锁）", fg=GREEN, bg=GREEN_SOFT, w=254, h=22, size=11.5))

    # Plant cell wall + membrane
    el.append('<rect x="42" y="110" width="212" height="142" rx="18" fill="#f8fafc" stroke="#18794e" stroke-width="2"/>')
    el.append('<rect x="48" y="116" width="200" height="130" rx="14" fill="#ffffff" stroke="#86efac" stroke-width="1.2" stroke-dasharray="4 3"/>')
    el.append(txt(56, 132, "细胞壁 + 完整细胞膜（阻挡外界 O2）", size=10.5, color=GREEN, weight="600"))

    # Vacuole box
    el.append('<rect x="58" y="142" width="108" height="92" rx="12" fill="#eaf4fb" stroke="#1d6fa5" stroke-width="1.5"/>')
    el.append(txt(112, 160, "液泡保险箱", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(112, 177, "(+)-儿茶素", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(112, 193, "(-)-EGC / 绿原酸", size=10.5, color=BODY, anchor="middle"))
    el.append(txt(112, 211, "（无色邻二酚底物）", size=10, color=MUTED, anchor="middle"))
    el.append(txt(112, 227, "液泡膜完好上锁", size=10, color=BLUE, anchor="middle", weight="600"))

    # Plastid box
    el.append('<rect x="174" y="142" width="66" height="92" rx="12" fill="#fef1e8" stroke="#c25014" stroke-width="1.5"/>')
    el.append(txt(207, 160, "质体车间", size=11.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(207, 179, "PPO 酶", size=11, color=BODY, anchor="middle", weight="600"))
    el.append('<circle cx="197" cy="198" r="7" fill="#fed7aa" stroke="#c25014" stroke-width="1.2"/>')
    el.append('<circle cx="217" cy="198" r="7" fill="#fed7aa" stroke="#c25014" stroke-width="1.2"/>')
    el.append(txt(197, 201.5, "Cu", size=8.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(217, 201.5, "Cu", size=8.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(207, 224, "双铜中心", size=10, color=MUTED, anchor="middle"))

    # Snow-white lotus root icon on right side of left card
    el.append(_lotus_slice_svg(306, 176, 38, "#fdfcf7", "#cbd5e1"))
    el.append(txt(306, 232, "雪白脆嫩", size=11.5, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(306, 248, "0 褐变色素", size=10.5, color=MUTED, anchor="middle"))
    el.append(txt(42, 282, "结论：底物与酶隔膜相望 + 淤泥缺氧 = 几个月都不变黑", size=11, color=GREEN, weight="600"))

    # Right panel: Cut cell + 3-step chain
    el.append(card(378, 66, 358, 232, fill=CARD_BG, stroke=BORDER))
    el.append(pill(392, 78, "状态 B：菜刀切开瞬间（破壁 + 见氧）", fg=ORANGE, bg=ORANGE_SOFT, w=252, h=22, size=11.5))

    # Ruptured cell + blade + O2
    el.append('<rect x="394" y="114" width="218" height="136" rx="16" fill="#fffaf5" stroke="#c25014" stroke-width="1.6" stroke-dasharray="6 4"/>')
    # Knife wedge at top middle of cell + static clear label inside ruptured cell
    el.append(
        '<polygon class="anim-blade" points="488,103 510,103 502,136 496,136" fill="#64748b" stroke="#334155" stroke-width="1"/>'
        '<text x="518" y="139" font-size="10.5" fill="#b91c1c" font-weight="700">① 刀刃破膜</text>'
    )
    # O2 rushing in
    el.append(
        '<g class="anim-o2">'
        '<rect x="404" y="124" width="66" height="22" rx="11" fill="#eaf4fb" stroke="#1d6fa5" stroke-width="1"/>'
        '<text x="437" y="139" font-size="10.5" fill="#1d6fa5" text-anchor="middle" font-weight="700">空气 O2 涌入</text>'
        "</g>"
    )
    # Step 2 box inside ruptured zone
    el.append('<rect x="404" y="154" width="198" height="40" rx="8" fill="#fef1e8" stroke="#c25014" stroke-width="1.2"/>')
    el.append(txt(503, 171, "② 双铜 PPO 催化夺氢（酶促步）", size=11, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(503, 187, "无色邻二酚 + O2 → 淡黄邻苯醌 + H2O", size=10.5, color=BODY, anchor="middle"))

    # Step 3 box inside ruptured zone
    el.append('<g class="anim-final">')
    el.append('<rect x="404" y="202" width="198" height="40" rx="8" fill="#f8f1ea" stroke="#6b4423" stroke-width="1.3"/>')
    el.append(txt(503, 219, "③ 邻苯醌自发聚合（无需酶！）", size=11, color=BROWN, anchor="middle", weight="700"))
    el.append(txt(503, 235, "交联氨基酸 → 茶黄素类 + 类黑色素", size=10.5, color=BODY, anchor="middle"))
    el.append("</g>")

    # Lotus slice morphing from pale to brown-black
    el.append(_lotus_slice_svg(674, 176, 38, "#fdfcf7", "#cbd5e1"))
    el.append(_lotus_slice_svg(674, 176, 38, "#7c5841", "#4a3222", hole_fill="#f8fafc", cls="anim-dark-slice"))
    el.append(txt(674, 232, "灰褐—黑褐色", size=11.5, color=BROWN, anchor="middle", weight="700"))
    el.append(txt(674, 248, "伤口保护铠甲", size=10.5, color=MUTED, anchor="middle"))
    el.append(txt(394, 282, "植物本意：用不溶性醌聚合物封住伤口、抵御病菌入侵", size=11, color=BROWN, weight="600"))

    # Bottom quantitative & chemical card
    el.append(card(24, 312, 712, 192, fill=CARD_BG, stroke=BORDER))
    el.append(pill(38, 324, "分步化学拆解与实验实测参数（Nelumbo nucifera）", fg=BLUE, bg=BLUE_SOFT, w=326, h=22, size=11.5))

    # Left equation block
    el.append(card(38, 356, 412, 134, rx=8, fill=SLATE_SOFT, stroke=HAIRLINE))
    el.append(step_badge(58, 376, 1, fg=ORANGE, bg=ORANGE_SOFT))
    el.append(txt(76, 380, "酶促氧化步（必须有活性 PPO + Cu2+ + O2）：", size=11.5, color=INK, weight="700"))
    el.append(txt(56, 402, "2 邻二酚（如儿茶素） + O2  ──PPO──▶  2 邻苯醌（高活性亲电体） + 2 H2O", size=11, color=ORANGE, weight="600"))
    el.append('<line x1="52" y1="416" x2="436" y2="416" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4 3"/>')
    el.append(step_badge(58, 436, 2, fg=BROWN, bg=BROWN_SOFT))
    el.append(txt(76, 440, "非酶聚合步（一旦生成邻苯醌，关掉酶也会继续变黑）：", size=11.5, color=INK, weight="700"))
    el.append(txt(56, 462, "邻苯醌 + 多酚 / 蛋白质氨基  ──自发聚合──▶  茶黄素类 + 类黑色素（褐黑）", size=11, color=BROWN, weight="600"))
    el.append(txt(56, 481, "注：催化还原产物是水（H2O）而非双氧水；双铜间距在氧化/还原态间由 3.3 Å 呼吸至 4.4 Å。", size=10, color=MUTED))

    # Right quantitative data card
    el.append(card(464, 356, 258, 134, rx=8, fill="#fffbeb", stroke="#f59e0b"))
    el.append(txt(478, 377, "实验室实测莲藕褐变档案", size=12, color=AMBER, weight="700"))
    el.append(txt(478, 399, "• 最适巅峰：35 °C、pH 6.5", size=11, color=BODY, weight="600"))
    el.append(txt(478, 419, "• 速度冠军：(+)-儿茶素（Vmax 最高）", size=11, color=BODY))
    el.append(txt(478, 439, "• 亲和冠军：(-)-EGC（Km 最低）", size=11, color=BODY))
    el.append(txt(478, 459, "• 食用安全：褐变主产物为茶黄素类", size=11, color=GREEN, weight="700"))
    el.append(txt(488, 477, "（与红茶同源！不发黏发臭即可安心吃）", size=10.5, color=GREEN))

    svg = figure(
        520,
        "莲藕切开变黑的细胞区室化崩塌与多酚氧化酶催化动画",
        "对比完整莲藕细胞中液泡多酚与质体双铜多酚氧化酶的隔离状态，以及切开后氧气涌入触发邻苯醌生成与自发聚合成类黑色素的三步过程。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "compartmentalization-and-ppo-anim.svg", svg)


def build_iron_wok_and_ancient_ink():
    """SVG 2: Iron-polyphenol coordination complexation & 1,400-year Iron Gall Ink."""
    el = []
    el.extend(
        header(
            "凶手二（铁酚络合）：为什么铁锅炒藕会“秒变蓝紫乌黑”？",
            "就算沸水已经烫死所有酶，莲藕多酚抓到铁离子仍会瞬间配位——你其实在铁锅里熬出了中世纪墨水",
        )
    )

    # Left Card: Iron Wok Chelation Mechanism
    el.append(card(24, 66, 348, 286, fill=CARD_BG, stroke=BORDER))
    el.append(pill(38, 78, "铁锅现场：五元螯合环 + 电荷转移跃迁", fg=INDIGO, bg=INDIGO_SOFT, w=262, h=22, size=11.5))

    # Step 1: Iron wok leaching
    el.append('<rect x="38" y="110" width="320" height="58" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>')
    el.append(step_badge(56, 139, 1, fg=INDIGO, bg=INDIGO_SOFT))
    el.append(txt(74, 132, "铸铁锅 / 碳钢菜刀溶出微量铁离子", size=11.5, color=INK, weight="700"))
    el.append(txt(74, 152, "热油翻炒 + 食盐/微酸加速溶出 Fe2+，遇空气 O2 迅速氧化为 Fe3+", size=10.5, color=MUTED))

    # Step 2: Chelation claw diagram
    el.append('<rect x="38" y="176" width="320" height="96" rx="8" fill="#eef2ff" stroke="#818cf8" stroke-width="1.3"/>')
    el.append(step_badge(56, 198, 2, fg=INDIGO, bg=CARD_BG))
    el.append(txt(74, 201, "邻二酚“螃蟹钳”死死夹住 Fe3+（双齿螯合）", size=11.5, color=INDIGO, weight="700"))

    # Schematic aromatic ring + 2 O- -> Fe3+ five-membered chelate ring
    # Hexagon centered at (128, 240), r=18
    hx_pts = []
    for k in range(6):
        a = math.radians(k * 60)
        hx_pts.append(f"{118 + 17 * math.cos(a):.1f},{240 + 17 * math.sin(a):.1f}")
    el.append(f'<polygon points="{" ".join(hx_pts)}" fill="#ffffff" stroke="#312e81" stroke-width="1.6"/>')
    el.append('<circle cx="118" cy="240" r="9" fill="none" stroke="#6366f1" stroke-width="1.2" stroke-dasharray="3 2"/>')
    el.append(txt(82, 244, "酚环", size=10, color=INDIGO, anchor="end", weight="600"))
    # Two O atoms & coordinate bonds to Fe3+
    el.append('<line x1="127" y1="226" x2="158" y2="230" stroke="#312e81" stroke-width="1.8"/>')
    el.append('<line x1="127" y1="254" x2="158" y2="250" stroke="#312e81" stroke-width="1.8"/>')
    el.append('<circle cx="158" cy="230" r="7.5" fill="#ffffff" stroke="#b91c1c" stroke-width="1.3"/>')
    el.append('<circle cx="158" cy="250" r="7.5" fill="#ffffff" stroke="#b91c1c" stroke-width="1.3"/>')
    el.append(txt(158, 233.5, "O", size=9.5, color=RED, anchor="middle", weight="700"))
    el.append(txt(158, 253.5, "O", size=9.5, color=RED, anchor="middle", weight="700"))
    el.append('<line x1="166" y1="231" x2="194" y2="238" stroke="#4338ca" stroke-width="2" stroke-dasharray="3 2"/>')
    el.append('<line x1="166" y1="249" x2="194" y2="242" stroke="#4338ca" stroke-width="2" stroke-dasharray="3 2"/>')
    el.append('<circle cx="204" cy="240" r="13" fill="#312e81" stroke="#1e1b4b" stroke-width="1.5"/>')
    el.append(txt(204, 244, "Fe3+", size=10, color="#ffffff", anchor="middle", weight="700"))

    el.append(txt(226, 232, "五元螯合环极稳固", size=10.5, color=INDIGO, weight="700"))
    el.append(txt(226, 248, "无需任何酶参与！", size=10.5, color=RED, weight="700"))
    el.append(txt(226, 264, "100 °C 沸锅照样秒发", size=10, color=MUTED))

    # Step 3: LMCT absorption
    el.append('<rect x="38" y="280" width="320" height="58" rx="8" fill="#1e1b4b" stroke="#312e81"/>')
    el.append(txt(52, 302, "③ 配体→金属电荷转移跃迁（LMCT 强吸光）：", size=11, color="#e0e7ff", weight="700"))
    el.append(txt(52, 322, "强烈吞掉 550–600 nm 黄绿光 → 肉眼呈现深蓝紫至乌黑色！", size=10.5, color="#c7d2fe"))

    # Right Card: Cross-century siblings
    el.append(card(388, 66, 348, 286, fill=CARD_BG, stroke=BORDER))
    el.append(pill(402, 78, "同款化学四胞胎：从达·芬奇手稿到饭后浓茶", fg=PURPLE, bg=PURPLE_SOFT, w=282, h=22, size=11.5))

    siblings = [
        (
            "1. 欧洲千年“铁胆墨水”（Iron Gall Ink）",
            "橡树五倍子单宁/没食子酸 + 绿矾（FeSO4）→ 见氧变不溶紫黑墨迹；",
            "公元 5–19 世纪欧洲标准墨水，达·芬奇、巴赫、牛顿手稿皆用它写成。",
            PURPLE,
            PURPLE_SOFT,
        ),
        (
            "2. 中国非遗草木染“皂矾媒染乌黑布”",
            "莲蓬壳、五倍子、栗壳熬出多酚染液 + 皂矾（绿矾 FeSO4）固色，",
            "纤维内原位生成耐洗铁—单宁黑络合物（香云纱河泥铁染同源）。",
            BROWN,
            BROWN_SOFT,
        ),
        (
            "3. 碳钢刀切柿子留黑印 & 土豆熟后返青黑",
            "涩柿子单宁遇铁刀秒留蓝黑印；土豆富含绿原酸，煮熟时与薯内 Fe2+",
            "结合，出锅晾凉遇空气氧化成 Fe3+–绿原酸络合物，令熟土豆发灰发乌。",
            BLUE,
            BLUE_SOFT,
        ),
        (
            "4. 贫血人群“饭后忌立刻喝浓茶”",
            "浓茶单宁与儿茶素在胃肠道内用同款“螯合钳”锁死植物性非血红素铁，",
            "形成难溶沉淀随粪便排出，显著拉低铁剂与蔬菜铁的吸收率。",
            ORANGE,
            ORANGE_SOFT,
        ),
    ]
    sy = 110
    for title_s, line1, line2, col, bg_c in siblings:
        el.append(f'<rect x="402" y="{sy}" width="320" height="54" rx="7" fill="{bg_c}" stroke="{col}" stroke-opacity="0.35"/>')
        el.append(txt(412, sy + 17, title_s, size=11, color=col, weight="700"))
        el.append(txt(412, sy + 33, line1, size=10, color=BODY))
        el.append(txt(412, sy + 47, line2, size=10, color=MUTED))
        sy += 60

    # Bottom Card: pH-dependent Fe3+-catechol coordination & Vinegar rescue
    el.append(card(24, 366, 712, 138, fill=CARD_BG, stroke=BORDER))
    el.append(pill(38, 378, "Fe3+–邻二酚络合物的 pH 变色光谱 & 为什么淋一勺白醋能“一键褪黑”", fg=TEAL, bg=TEAL_SOFT, w=456, h=22, size=11.5))

    zones = [
        (38, 162, "#ecfdf5", "#10b981", "pH < 4.0（白醋/柠檬汁）", "H+ 夺回酚羟基 + 柠檬酸抢铁", "络合解体 → 恢复浅白！", GREEN),
        (210, 158, "#f0fdfa", "#14b8a6", "pH 5.0–6.0（弱酸单配位）", "1 个多酚夹 1 个铁 [FeL]+", "呈灰绿 — 暗蓝绿色", TEAL),
        (378, 174, "#eef2ff", "#4338ca", "pH 6.5–8.0（日常炒菜区）", "2 个多酚夹 1 个铁 [FeL2]-", "呈深紫蓝 — 乌黑色！", INDIGO),
        (562, 160, "#fef2f2", "#dc2626", "pH > 9.0（强碱三配位）", "3 个多酚夹 1 个铁 [FeL3]3-", "呈暗红褐色（加小苏打更糟）", RED),
    ]
    for zx, zw, zbg, zst, zt, zm, zb, zcol in zones:
        el.append(f'<rect x="{zx}" y="410" width="{zw}" height="80" rx="8" fill="{zbg}" stroke="{zst}" stroke-width="1.3"/>')
        el.append(txt(zx + zw / 2, 430, zt, size=11, color=zcol, anchor="middle", weight="700"))
        el.append(txt(zx + zw / 2, 451, zm, size=10, color=BODY, anchor="middle"))
        el.append(txt(zx + zw / 2, 472, zb, size=10.5, color=zcol, anchor="middle", weight="700"))

    svg = figure(
        520,
        "铁锅炒藕变紫黑的铁酚配位络合机制与铁胆墨水家族",
        "展示铁锅溶出的铁离子与莲藕邻二酚形成五元螯合环并通过电荷转移跃迁显紫黑色的机制，对比铁胆墨水、草木染、土豆返黑及白醋降pH解救原理。",
        el,
    )
    write_svg(SUBDIR, "iron-wok-and-ancient-ink.svg", svg)


def build_kitchen_anti_blackening_curves():
    """SVG 3: Quantitative PPO temperature & pH curves + 4 anti-blackening strikes."""
    el = []
    el.extend(
        header(
            "厨房防黑四板斧：每一招民间窍门，都精准卡死一个化学齿轮",
            "基于莲藕多酚氧化酶（PPO）温度—活性与 pH—活性实测规律（最适 35 °C、pH 6.5）的定量拆解",
        )
    )

    # Panel A: Temperature vs PPO Activity (0..100 C)
    el.append(card(24, 66, 344, 232, fill=CARD_BG, stroke=BORDER))
    el.append(txt(40, 88, "图 A：温度对莲藕 PPO 活性的影响", size=12.5, color=INK, weight="700"))
    gx0, gy0, gw, gh = 66.0, 256.0, 280.0, 146.0  # y from 110..256

    # Shaded danger warm-water zone (30..45 C) and blanch kill zone (85..100 C)
    x_30 = gx0 + (30.0 / 100.0) * gw
    x_45 = gx0 + (45.0 / 100.0) * gw
    x_85 = gx0 + (85.0 / 100.0) * gw
    el.append(f'<rect x="{x_30:.1f}" y="{gy0 - gh:.1f}" width="{x_45 - x_30:.1f}" height="{gh:.1f}" fill="#fef2f2"/>')
    el.append(f'<rect x="{x_85:.1f}" y="{gy0 - gh:.1f}" width="{gx0 + gw - x_85:.1f}" height="{gh:.1f}" fill="#e7f6ee"/>')

    # Grid & axes
    for pct in (0, 50, 100):
        yy = gy0 - (pct / 100.0) * gh
        el.append(f'<line x1="{gx0:.1f}" y1="{yy:.1f}" x2="{gx0 + gw:.1f}" y2="{yy:.1f}" stroke="{HAIRLINE}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        el.append(txt(gx0 - 6, yy + 4, f"{pct}%", size=10, color=MUTED, anchor="end"))
    for tc in (0, 20, 35, 60, 80, 100):
        xx = gx0 + (tc / 100.0) * gw
        el.append(f'<line x1="{xx:.1f}" y1="{gy0:.1f}" x2="{xx:.1f}" y2="{gy0 + 4:.1f}" stroke="{SLATE}" stroke-width="1"/>')
        el.append(txt(xx, gy0 + 16, f"{tc}°C", size=10, color=MUTED, anchor="middle"))

    el.append(f'<line x1="{gx0:.1f}" y1="{gy0 - gh:.1f}" x2="{gx0:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.2"/>')
    el.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0 + gw:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.2"/>')

    pts_t = []
    for tc in range(0, 101, 2):
        xx = gx0 + (tc / 100.0) * gw
        yy = gy0 - (_ppo_temp_activity(tc) / 100.0) * gh
        pts_t.append(f"{xx:.1f},{yy:.1f}")
    el.append(f'<polyline points="{" ".join(pts_t)}" fill="none" stroke="{ORANGE}" stroke-width="2.6"/>')

    # Key markers: 4 C fridge, 35 C peak, 95 C blanching
    x4, y4 = gx0 + 0.04 * gw, gy0 - (_ppo_temp_activity(4) / 100.0) * gh
    x35, y35 = gx0 + 0.35 * gw, gy0 - 1.0 * gh
    x95, y95 = gx0 + 0.95 * gw, gy0
    el.append(f'<circle cx="{x4:.1f}" cy="{y4:.1f}" r="4" fill="{BLUE}"/>')
    el.append(txt(x4 + 6, y4 - 6, "4°C 冷藏慢速", size=10, color=BLUE, weight="600", halo=True))
    el.append(f'<circle cx="{x35:.1f}" cy="{y35:.1f}" r="4.5" fill="{RED}"/>')
    el.append(txt(x35 + 8, y35 + 12, "35°C 巅峰！温水泡藕反而催黑", size=10, color=RED, weight="700", halo=True))
    el.append(f'<circle cx="{x95:.1f}" cy="{y95:.1f}" r="4.5" fill="{GREEN}"/>')
    el.append(txt(x_85 - 4, gy0 - 52, "沸水焯烫杀青", size=10.5, color=GREEN, anchor="end", weight="700", halo=True))
    el.append(txt(x_85 - 4, gy0 - 36, "蛋白变性归零", size=10, color=GREEN, anchor="end", halo=True))
    el.append(txt(196, 290, "温度 T（°C）", size=10.5, color=SLATE, anchor="middle", weight="600"))

    # Panel B: pH vs PPO Activity (pH 2.0..9.5)
    el.append(card(392, 66, 344, 232, fill=CARD_BG, stroke=BORDER))
    el.append(txt(408, 88, "图 B：酸碱度（pH）对莲藕 PPO 活性的影响", size=12.5, color=INK, weight="700"))
    px0, py0, pw, ph_h = 434.0, 256.0, 280.0, 146.0

    def _ph_x(p):
        return px0 + ((p - 2.0) / 7.5) * pw

    # Shaded acid safe zone (pH 2.5..4.0)
    el.append(f'<rect x="{_ph_x(2.0):.1f}" y="{py0 - ph_h:.1f}" width="{_ph_x(4.0) - _ph_x(2.0):.1f}" height="{ph_h:.1f}" fill="#e7f6ee"/>')

    for pct in (0, 50, 100):
        yy = py0 - (pct / 100.0) * ph_h
        el.append(f'<line x1="{px0:.1f}" y1="{yy:.1f}" x2="{px0 + pw:.1f}" y2="{yy:.1f}" stroke="{HAIRLINE}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        el.append(txt(px0 - 6, yy + 4, f"{pct}%", size=10, color=MUTED, anchor="end"))
    for pv in (2.0, 3.5, 5.0, 6.5, 8.0, 9.5):
        xx = _ph_x(pv)
        el.append(f'<line x1="{xx:.1f}" y1="{py0:.1f}" x2="{xx:.1f}" y2="{py0 + 4:.1f}" stroke="{SLATE}" stroke-width="1"/>')
        el.append(txt(xx, py0 + 16, f"{pv:.1f}", size=10, color=MUTED, anchor="middle"))

    el.append(f'<line x1="{px0:.1f}" y1="{py0 - ph_h:.1f}" x2="{px0:.1f}" y2="{py0:.1f}" stroke="{SLATE}" stroke-width="1.2"/>')
    el.append(f'<line x1="{px0:.1f}" y1="{py0:.1f}" x2="{px0 + pw:.1f}" y2="{py0:.1f}" stroke="{SLATE}" stroke-width="1.2"/>')

    pts_p = []
    for i in range(0, 76):
        pv = 2.0 + i * 0.1
        xx = _ph_x(pv)
        yy = py0 - (_ppo_ph_activity(pv) / 100.0) * ph_h
        pts_p.append(f"{xx:.1f},{yy:.1f}")
    el.append(f'<polyline points="{" ".join(pts_p)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

    xp35, yp35 = _ph_x(3.5), py0 - (_ppo_ph_activity(3.5) / 100.0) * ph_h
    xp65, yp65 = _ph_x(6.5), py0 - 1.0 * ph_h
    el.append(f'<circle cx="{xp35:.1f}" cy="{yp35:.1f}" r="4.5" fill="{GREEN}"/>')
    el.append(txt(xp35 + 4, yp35 - 18, "白醋/柠檬汁区", size=10.5, color=GREEN, weight="700", halo=True))
    el.append(txt(xp35 + 4, yp35 - 4, "pH≤3.5 活性<8%", size=10, color=GREEN, halo=True))
    el.append(f'<circle cx="{xp65:.1f}" cy="{yp65:.1f}" r="4.5" fill="{RED}"/>')
    el.append(txt(xp65, yp65 + 22, "鲜藕汁天然 pH≈6.5", size=10, color=RED, anchor="middle", weight="700", halo=True))
    el.append(txt(xp65, yp65 + 36, "正撞最适枪口！", size=10, color=RED, anchor="middle", halo=True))
    el.append(txt(564, 290, "溶液酸碱度 pH", size=10.5, color=SLATE, anchor="middle", weight="600"))

    # Bottom 4-card toolkit
    el.append(card(24, 312, 712, 192, fill=CARD_BG, stroke=BORDER))
    el.append(pill(38, 324, "厨房实战防黑四板斧（按菜式精准选招）", fg=GREEN, bg=GREEN_SOFT, w=282, h=22, size=11.5))

    tools = [
        (
            38,
            "① 切完立刻泡凉水",
            "卡死齿轮：隔绝氧气 O2",
            "常温水溶氧仅 ~8.3 mg/L，",
            "且 O2 在水中扩散速度比",
            "空气慢约 10,000 倍！",
            BLUE,
            BLUE_SOFT,
        ),
        (
            210,
            "② 沸水焯烫 1–2 分钟",
            "卡死齿轮：高温废掉 PPO",
            "95–100 °C 令双铜酶蛋白",
            "不可逆变性坍塌（与绿茶",
            "“杀青”保翠绿完全同源）。",
            ORANGE,
            ORANGE_SOFT,
        ),
        (
            382,
            "③ 白醋 / 柠檬汁一箭三雕",
            "降 pH + 螯合金属 + 还原醌",
            "酸度压低酶活；柠檬酸抢",
            "走 Cu2+/Fe3+；维 C 把邻",
            "苯醌重新还原回无色酚！",
            GREEN,
            GREEN_SOFT,
        ),
        (
            554,
            "④ 避开铁锅与碳钢刀",
            "卡死齿轮：断绝游离铁源",
            "改用不锈钢刀切片，搭配",
            "不锈钢锅、陶瓷锅或砂锅，",
            "彻底杜绝铁酚紫黑墨水。",
            PURPLE,
            PURPLE_SOFT,
        ),
    ]
    for tx, tt, sub_t, l1, l2, l3, tcol, tbg in tools:
        el.append(f'<rect x="{tx}" y="356" width="164" height="134" rx="8" fill="{tbg}" stroke="{tcol}" stroke-opacity="0.4"/>')
        el.append(txt(tx + 10, 376, tt, size=11.5, color=tcol, weight="700"))
        el.append(txt(tx + 10, 395, sub_t, size=10, color=INK, weight="700"))
        el.append(f'<line x1="{tx + 10}" y1="404" x2="{tx + 154}" y2="404" stroke="{tcol}" stroke-opacity="0.25"/>')
        el.append(txt(tx + 10, 424, l1, size=10, color=BODY))
        el.append(txt(tx + 10, 443, l2, size=10, color=BODY))
        el.append(txt(tx + 10, 462, l3, size=10, color=BODY))

    svg = figure(
        520,
        "莲藕多酚氧化酶温度与pH活性曲线及厨房防黑四板斧",
        "绘出莲藕PPO在35摄氏度与pH6.5处的活性峰值曲线，警示温水泡藕误区，并拆解凉水隔氧、沸水杀青、酸与维C三重阻断及换非铁锅四项防黑机制。",
        el,
    )
    write_svg(SUBDIR, "kitchen-anti-blackening-curves.svg", svg)


def build_everyday_ppo_heroes_and_villains():
    """SVG 4: Everyday life connections of copper PPO / tyrosinase across plants, tea, seafood & skin."""
    el = []
    el.extend(
        header(
            "一把“双铜氧化剪刀”走天下：生活里原来全是莲藕的化学亲戚",
            "从切苹果发锈、红茶“假发酵”、冰鲜大虾黑头到夏天晒黑长斑——底层竟是同一个含铜酶家族",
        )
    )

    # Central unifying spine banner
    el.append(card(24, 66, 712, 52, rx=10, fill="#fff7ed", stroke="#ea580c", sw=1.3))
    el.append(pill(38, 81, "共同底层引擎", fg=ORANGE, bg="#ffedd5", w=108, h=22, size=11.5))
    el.append(
        txt(
            158,
            90,
            "第 3 型双铜金属酶家族（植物多酚氧化酶 PPO / 动物与真菌酪氨酸酶 Tyrosinase）",
            size=12,
            color=INK,
            weight="700",
        )
    )
    el.append(
        txt(
            158,
            108,
            "统一套路：单酚 / 邻二酚底物  +  O2  ──双铜活性中心──▶  高活性邻苯醌  ──自发聚合──▶  棕红/褐黑色素",
            size=10.5,
            color=ORANGE,
            weight="600",
        )
    )

    quads = [
        (
            24,
            130,
            "① 餐桌上的“颜值刺客”：果蔬切面褐变",
            "讨厌它？得想方设法关掉酶",
            BLUE,
            BLUE_SOFT,
            [
                "• 代表成员：苹果、梨、土豆、茄子、牛油果、香蕉黑斑、白蘑菇",
                "• 各自底物：苹果/土豆富绿原酸，香蕉皮富多巴胺，蘑菇富酪氨酸",
                "• 碰撞与冷害：香蕉放冰箱冷藏（<12 °C）细胞膜冻伤渗漏，皮秒变黑",
                "• 现代生物黑科技：北美 Arctic 转基因苹果通过 RNA 干扰直接让",
                "  PPO 基因“静音”，切开摆几小时依然雪白不发锈！",
            ],
        ),
        (
            388,
            130,
            "② 化腐朽为神奇：红茶、乌龙茶与可可豆",
            "利用它！故意揉破细胞催生香气色泽",
            AMBER,
            AMBER_SOFT,
            [
                "• 百年误称：红茶所谓“全发酵茶”其实 0 微生物参与，纯属酶促褐变！",
                "• 一叶分天下（茶鲜叶儿茶素占干重 ~25%）：",
                "  - 绿茶：摘下立刻高温炒/蒸“杀青”，烫死 PPO → 保住翠绿清鲜",
                "  - 红茶：用力揉捻压破液泡，任 PPO 100% 氧化儿茶素 → 生成金红",
                "    透亮的茶黄素与醇厚茶红素！（可可豆、咖啡、葡萄干同理）",
            ],
        ),
        (
            24,
            322,
            "③ 海鲜市场大冤案：虾头、蟹脚为什么发黑？",
            "别慌！多半不是重金属超标或变质中毒",
            TEAL,
            TEAL_SOFT,
            [
                "• 现象（Melanosis 黑变病）：冰鲜大虾解冻后虾头、虾尾先泛黑",
                "• 真凶：虾头肝胰腺与外壳富集含铜“酪氨酸酶”，死后照样开工，",
                "  把虾体天然无色的酪氨酸氧化聚合成黑色素（跟藕变黑一模一样！）",
                "• 鉴别金标准：仅虾头黑但虾肉紧实弹牙、无氨臭酸味 = 安全可食；",
                "  若头肉脱节、发黏发臭，才是细菌分解蛋白质产生的真腐败。",
            ],
        ),
        (
            388,
            322,
            "④ 藏在你皮肤里的同款工厂：防晒黑与白化病",
            "人体黑色素细胞同样握着这把双铜剪刀",
            PURPLE,
            PURPLE_SOFT,
            [
                "• 人体 TYR 基因编码含铜酪氨酸酶（坐镇皮肤黑色素小体）：",
                "  紫外线照射 → 激活酶催化 L-酪氨酸 → L-多巴 → 多巴醌 → 黑色素",
                "• 生理使命：黑色素像小黑伞盖在细胞核上方，替 DNA 挡住紫外线伤害",
                "• 医学与护肤映射：TYR 基因失活突变会导致先天性白化病（OCA1）；",
                "  而美白精华里的维 C、熊果苷、曲酸，本质就是“皮肤版柠檬汁”！",
            ],
        ),
    ]

    for qx, qy, qt, qsub, qcol, qbg, qlines in quads:
        el.append(card(qx, qy, 348, 180, fill=CARD_BG, stroke=BORDER))
        el.append(f'<rect x="{qx}" y="{qy}" width="348" height="44" rx="10" fill="{qbg}"/>')
        el.append(f'<line x1="{qx}" y1="{qy + 44}" x2="{qx + 348}" y2="{qy + 44}" stroke="{qcol}" stroke-opacity="0.3"/>')
        el.append(txt(qx + 14, qy + 19, qt, size=11.5, color=qcol, weight="700"))
        el.append(txt(qx + 14, qy + 36, qsub, size=10, color=MUTED, weight="600"))
        ly = qy + 64
        for ln in qlines:
            el.append(txt(qx + 14, ly, ln, size=10.3, color=BODY))
            ly += 22

    svg = figure(
        520,
        "生活中多酚氧化酶与酪氨酸酶的四大家族现象图谱",
        "以第3型双铜氧化酶为核心，串联果蔬切面褐变、绿茶杀青与红茶酶促氧化、虾蟹死后酪氨酸黑变，以及人类皮肤紫外线黑色素合成与美白机制。",
        el,
    )
    write_svg(SUBDIR, "everyday-ppo-heroes-and-villains.svg", svg)


def build_four_brownings_comparison_map():
    """SVG 5: Master 4-way classifier of everyday chemical browning & darkening."""
    el = []
    el.extend(
        header(
            "厨房终极破案图谱：同样是“变棕变黑”，背后竟有四套完全不同的化学",
            "分清酶促褐变、金属配位、美拉德反应与焦糖化反应——从此切菜防黑、煎肉增香不再张冠李戴",
        )
    )

    # Master comparison table card
    el.append(card(24, 66, 712, 314, fill=CARD_BG, stroke=BORDER))

    # Table header
    el.append('<rect x="24" y="66" width="712" height="36" rx="10" fill="#0f172a"/>')
    cols = [
        (36, "反应类型"),
        (164, "核心反应物"),
        (332, "触发温度与条件"),
        (482, "标志产物与气味"),
        (618, "生活代表场景"),
    ]
    for cx, cname in cols:
        el.append(txt(cx, 89, cname, size=11.5, color="#ffffff", weight="700"))

    rows = [
        (
            102,
            "#fffaf5",
            ORANGE,
            "1. 酶促褐变",
            "（生物酶催化）",
            "多酚 / 酪氨酸 + O2",
            "需活性双铜酶（PPO）",
            "常温 20–45 °C 最快",
            "沸水 >90 °C 酶死即停",
            "茶黄素类 + 类黑色素",
            "无焦香（红茶花果香）",
            "切开的藕片、苹果、",
            "红茶发酵、虾头黑变",
        ),
        (
            170,
            "#eef2ff",
            INDIGO,
            "2. 铁—多酚络合",
            "（配位化学）",
            "邻二酚 / 单宁",
            "+ Fe2+ / Fe3+ 离子",
            "常温至 100 °C 皆秒发",
            "无需酶！pH 6–8 最黑",
            "多酚铁螯合物（LMCT）",
            "深蓝紫—乌黑，略涩",
            "铁锅炒藕/山药发黑、",
            "铁胆墨水、浓茶遇铁",
        ),
        (
            238,
            "#fef2f2",
            RED,
            "3. 美拉德反应",
            "（非酶褐变 A）",
            "还原糖（羰基 C=O）",
            "+ 氨基酸/蛋白（-NH2）",
            "140–165 °C 高速爆发",
            "无需酶、无需氧气！",
            "类黑精 + 吡嗪/呋喃等",
            "诱人烤肉香、麦香、咖香",
            "煎牛排焦壳、烤面包、",
            "红烧肉、烘焙咖啡豆",
        ),
        (
            306,
            "#fffbeb",
            AMBER,
            "4. 焦糖化反应",
            "（非酶褐变 B）",
            "纯糖类单枪匹马",
            "（无需蛋白质/氨基酸）",
            "果糖 105°C / 葡萄糖 150°C",
            "蔗糖 170°C 高温脱水热解",
            "焦糖素 + 双乙酰等",
            "奶油焦甜香（过火发苦）",
            "拔丝红薯、焦糖布丁、",
            "冰糖炒糖色、可乐色",
        ),
    ]

    for ry, rbg, rcol, c1a, c1b, c2a, c2b, c3a, c3b, c4a, c4b, c5a, c5b in rows:
        el.append(f'<rect x="25" y="{ry}" width="710" height="68" fill="{rbg}"/>')
        el.append(f'<line x1="25" y1="{ry}" x2="735" y2="{ry}" stroke="{BORDER}" stroke-width="1"/>')
        el.append(txt(36, ry + 27, c1a, size=11.5, color=rcol, weight="700"))
        el.append(txt(36, ry + 47, c1b, size=10, color=MUTED, weight="600"))

        el.append(txt(164, ry + 27, c2a, size=10.5, color=INK, weight="600"))
        el.append(txt(164, ry + 47, c2b, size=10, color=MUTED))

        el.append(txt(332, ry + 27, c3a, size=10.5, color=BODY, weight="600"))
        el.append(txt(332, ry + 47, c3b, size=10, color=rcol, weight="600"))

        el.append(txt(482, ry + 27, c4a, size=10.5, color=BODY, weight="600"))
        el.append(txt(482, ry + 47, c4b, size=10, color=MUTED))

        el.append(txt(618, ry + 27, c5a, size=10.5, color=BODY))
        el.append(txt(618, ry + 47, c5b, size=10.5, color=BODY))

    # Bottom 3-second diagnostic strip
    el.append(card(24, 394, 712, 110, fill=CARD_BG, stroke=BORDER))
    el.append(pill(38, 406, "三秒厨房破案口诀（看温度 + 看锅具 + 闻香味）", fg=BLUE, bg=BLUE_SOFT, w=304, h=22, size=11.5))

    clues = [
        (38, "常温切开慢慢暗", "→ 酶促褐变（泡水/焯水）", ORANGE),
        (212, "下铁锅秒变紫乌黑", "→ 铁酚络合（换锅/加醋）", INDIGO),
        (388, "猛火干煎出肉麦香", "→ 美拉德（擦干水分才香）", RED),
        (564, "白糖熬化冒琥珀泡", "→ 焦糖化（控温防碳化苦）", AMBER),
    ]
    for kx, kt, kb, kcol in clues:
        el.append(f'<rect x="{kx}" y="438" width="160" height="54" rx="8" fill="{SLATE_SOFT}" stroke="{kcol}" stroke-opacity="0.45"/>')
        el.append(txt(kx + 80, 459, kt, size=11, color=INK, anchor="middle", weight="700"))
        el.append(txt(kx + 80, 479, kb, size=10, color=kcol, anchor="middle", weight="700"))

    svg = figure(
        520,
        "生活中四大褐变与发黑化学反应的终极对比图谱",
        "从反应物、触发温度条件、标志产物气味与生活代表场景四个维度对比酶促褐变、铁酚配位络合、美拉德反应与焦糖化反应，附三秒厨房破案口诀。",
        el,
    )
    write_svg(SUBDIR, "four-brownings-comparison-map.svg", svg)


@register("lotus-browning", "莲藕变黑与生活中的褐变及配位化学图解", "chemistry")
def build_all():
    build_compartmentalization_and_ppo_anim()
    build_iron_wok_and_ancient_ink()
    build_kitchen_anti_blackening_curves()
    build_everyday_ppo_heroes_and_villains()
    build_four_brownings_comparison_map()
