"""Original SVG diagrams for the chemical properties and uses of methanol and ethanol."""

from . import core
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
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "methanol-ethanol"

RED = "#dc2626"
RED_SOFT = "#fef2f2"
RED_BORDER = "#fca5a5"
AMBER = "#b45309"
AMBER_SOFT = "#fef3c7"
TEAL = "#0f766e"
TEAL_SOFT = "#ccfbf1"


def _verify_chemical_metrics():
    """Verify exact stoichiometric, boiling-point, and thermochemical invariants."""
    m_meoh = 12.011 + 4 * 1.008 + 15.999
    m_etoh = 2 * 12.011 + 6 * 1.008 + 15.999
    assert abs(m_meoh - 32.042) < 0.01
    assert abs(m_etoh - 46.069) < 0.01

    # Oxygen mass fractions
    o_frac_meoh = 15.999 / m_meoh
    o_frac_etoh = 15.999 / m_etoh
    assert abs(o_frac_meoh - 0.4993) < 0.002
    assert abs(o_frac_etoh - 0.3473) < 0.002

    # Boiling point jumps upon replacing -H with -OH
    jump_c1 = 64.7 - (-161.5)
    jump_c2 = 78.2 - (-88.6)
    isomer_gap = 78.2 - (-24.8)  # ethanol vs dimethyl ether (C2H6O)
    assert abs(jump_c1 - 226.2) < 0.05
    assert abs(jump_c2 - 166.8) < 0.05
    assert abs(isomer_gap - 103.0) < 0.05


def build_molecule_hbond_boiling() -> str:
    """Compare CH3OH vs CH3CH2OH amphiphilic structure, H-bonding, and boiling-point jumps."""
    _verify_chemical_metrics()
    el = []
    el.extend(
        header(
            "只差一个 -CH₂- 的亲兄弟：双亲分子结构、氢键拉手网与沸点暴涨 200℃ 之谜",
            "先看左栏“憎水碳尾 + 亲水羟基头”的双亲构造 → 再看右栏装上羟基后沸点怎样从极寒气体一步跨进常温液体",
        )
    )

    # Left panel: Molecular comparison & hydrogen bond network (x=24..376, y=66..348)
    el.append(card(24, 66, 352, 282, rx=10))
    el.append(step_badge(42, 86, "1", fg=BLUE, bg=BLUE_SOFT, r=10))
    el.append(txt(58, 90, "结构对照：同样顶着极性 -OH，碳尾巴长短差一截", size=12.6, color=INK, weight="700"))

    # Methanol sub-box (x=38..362, y=102..182)
    el.append(card(38, 102, 324, 80, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1))
    # Ball-and-stick CH3-O-H
    el.append(
        f"""<line x1="78" y1="142" x2="122" y2="142" stroke="{SLATE}" stroke-width="3.2"/>
<line x1="122" y1="142" x2="152" y2="124" stroke="{BLUE}" stroke-width="3.2"/>
<line x1="78" y1="142" x2="56" y2="122" stroke="{SLATE}" stroke-width="2.2"/>
<line x1="78" y1="142" x2="56" y2="162" stroke="{SLATE}" stroke-width="2.2"/>
<line x1="78" y1="142" x2="82" y2="114" stroke="{SLATE}" stroke-width="2.2"/>
<circle cx="78" cy="142" r="13" fill="{AMBER}" stroke="#ffffff" stroke-width="1.5"/>
{txt(78, 146, "C", size=11, color="#ffffff", anchor="middle", weight="700")}
<circle cx="54" cy="120" r="6.5" fill="#94a3b8"/><circle cx="54" cy="164" r="6.5" fill="#94a3b8"/><circle cx="83" cy="112" r="6.5" fill="#94a3b8"/>
<circle cx="122" cy="142" r="12" fill="{RED}" stroke="#ffffff" stroke-width="1.5"/>
{txt(122, 146, "O", size=11, color="#ffffff", anchor="middle", weight="700")}
<circle cx="154" cy="123" r="7.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.2"/>
{txt(154, 127, "H", size=9.5, color="#ffffff", anchor="middle", weight="700")}"""
    )
    el.append(txt(168, 124, "甲醇 CH₃OH（M = 32.04）", size=11.8, color=INK, weight="700"))
    el.append(txt(168, 145, "• 仅 1 个碳（无 C–C 键），含氧 50%", size=10.8, color=BODY))
    el.append(txt(168, 166, "• 沸点 64.7℃，20℃ 蒸气压 13.0 kPa", size=10.8, color=ORANGE, weight="600"))

    # Ethanol sub-box (x=38..362, y=192..274)
    el.append(card(38, 192, 324, 82, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1))
    # Ball-and-stick CH3-CH2-O-H
    el.append(
        f"""<line x1="62" y1="238" x2="98" y2="226" stroke="{SLATE}" stroke-width="3.2"/>
<line x1="98" y1="226" x2="132" y2="238" stroke="{SLATE}" stroke-width="3.2"/>
<line x1="132" y1="238" x2="156" y2="220" stroke="{BLUE}" stroke-width="3.2"/>
<circle cx="62" cy="238" r="12" fill="{AMBER}" stroke="#ffffff" stroke-width="1.5"/>
{txt(62, 242, "Cβ", size=9.8, color="#ffffff", anchor="middle", weight="700")}
<circle cx="98" cy="226" r="12" fill="{AMBER}" stroke="#ffffff" stroke-width="1.5"/>
{txt(98, 230, "Cα", size=9.8, color="#ffffff", anchor="middle", weight="700")}
<circle cx="132" cy="238" r="11.5" fill="{RED}" stroke="#ffffff" stroke-width="1.5"/>
{txt(132, 242, "O", size=10.5, color="#ffffff", anchor="middle", weight="700")}
<circle cx="157" cy="219" r="7.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.2"/>
{txt(157, 223, "H", size=9.5, color="#ffffff", anchor="middle", weight="700")}"""
    )
    el.append(txt(168, 214, "乙醇 CH₃CH₂OH（M = 46.07）", size=11.8, color=INK, weight="700"))
    el.append(txt(168, 235, "• 多 1 个 -CH₂-（有 β-碳），含氧 34.7%", size=10.8, color=BODY))
    el.append(txt(168, 256, "• 沸点 78.2℃，20℃ 蒸气压 5.95 kPa", size=10.8, color=BLUE, weight="600"))

    # Amphiphilic + H-bond note inside left panel bottom (y=284..338)
    el.append(txt(38, 296, "双亲绝活：碳氢尾亲油脂，极性羟基（1.69 D）与水结氢键网——", size=10.8, color=BODY))
    el.append(txt(38, 316, "50 mL 乙醇 + 50 mL 水混合体积缩至约 96.3 mL！", size=11, color=TEAL, weight="700"))
    el.append(txt(38, 336, "（水分子钻进醇氢键空隙，既能与水混溶，又能溶解油污）", size=10.5, color=MUTED))

    # Right panel: Quantitative Boiling-Point Chart (x=392..736, y=66..348)
    # Temperature scale: T in [-180, +100] -> x_bar from 502 to 680
    el.append(card(392, 66, 344, 282, rx=10))
    el.append(step_badge(410, 86, "2", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(426, 90, "氢键威力实测：装上 -OH 沸点飙升 167~226℃", size=12.4, color=INK, weight="700"))

    x_min, x_max = 502.0, 680.0
    t_min, t_max = -180.0, 100.0

    def tx(temp_c):
        return x_min + (temp_c - t_min) / (t_max - t_min) * (x_max - x_min)

    x_zero = tx(0.0)
    x_room = tx(25.0)
    el.append(f'<line x1="{x_zero:.1f}" y1="120" x2="{x_zero:.1f}" y2="288" stroke="{HAIRLINE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    el.append(txt(x_zero - 4, 115, "0℃", size=10.2, color=MUTED, anchor="end"))
    el.append(f'<line x1="{x_room:.1f}" y1="120" x2="{x_room:.1f}" y2="288" stroke="{GREEN}" stroke-width="1.1" stroke-dasharray="3 3"/>')
    el.append(txt(x_room + 4, 115, "25℃室温", size=10.2, color=GREEN, anchor="start"))

    bars = [
        ("甲烷 CH₄", -161.5, SLATE, 130),
        ("甲醇 CH₃OH", 64.7, ORANGE, 162),
        ("乙烷 C₂H₆", -88.6, SLATE, 194),
        ("二甲醚 C₂H₆O", -24.8, PURPLE, 226),
        ("乙醇 C₂H₅OH", 78.2, BLUE, 258),
    ]
    for label_s, bp_val, col, y_row in bars:
        xb = tx(bp_val)
        el.append(txt(406, y_row + 11.5, label_s, size=10.8, color=BODY, anchor="start", weight="600"))
        left_x = min(x_zero, xb)
        bar_w = max(2.0, abs(xb - x_zero))
        el.append(f'<rect x="{left_x:.1f}" y="{y_row}" width="{bar_w:.1f}" height="15" rx="3" fill="{col}" opacity="0.85"/>')
        val_s = f"{bp_val:+.1f}℃" if bp_val > 0 else f"{bp_val:.1f}℃"
        label_x = (x_zero + 6) if bp_val < 0 else (left_x + bar_w + 5)
        el.append(txt(label_x, y_row + 11.5, val_s, size=10.5, color=col, anchor="start", weight="700", halo=True))

    el.append(txt(406, 312, "铁证：二甲醚与乙醇分子式同为 C₂H₆O，", size=10.8, color=PURPLE, weight="600"))
    el.append(txt(406, 332, "只因二甲醚无 O–H 氢键，沸点比乙醇低整整 103℃！", size=10.8, color=PURPLE, weight="600"))

    # Bottom parameter comparison strip (x=24..736, y=362..502)
    el.append(card(24, 362, 712, 140, rx=10, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(40, 386, "为什么挂着 -OH 却不是碱，也不是酸？——三个最容易踩坑的基础物化性质：", size=12.4, color=INK, weight="700"))

    cards_bot = [
        (
            40,
            "① 水溶液中呈电中性",
            "甲醇 pKa = 15.5，乙醇 pKa = 15.9",
            "与水相当，共价 C–O 键绝不电离 OH⁻！",
            BLUE,
            BLUE_SOFT,
        ),
        (
            274,
            "② 沸点差与 95.6% 共沸墙",
            "甲醇沸点低 13.5℃，酿酒“掐头”可减除",
            "乙醇与水在 78.15℃ 结成 95.6% 共沸物",
            ORANGE,
            ORANGE_SOFT,
        ),
        (
            508,
            "③ 外观气味难凭感官分辨",
            "密度几乎重叠（0.792 vs 0.789 g/cm³）",
            "皆为无色微香挥发液，严禁靠闻尝鉴酒！",
            RED,
            RED_SOFT,
        ),
    ]
    for cx_b, h_s, l1_s, l2_s, fg_c, bg_c in cards_bot:
        el.append(card(cx_b, 398, 216, 90, rx=8, fill=CARD_BG, stroke=fg_c, sw=1))
        el.append(pill(cx_b + 10, 406, h_s, fg=fg_c, bg=bg_c, w=196, h=20, size=11))
        el.append(txt(cx_b + 12, 446, l1_s, size=11, color=BODY, weight="600"))
        el.append(txt(cx_b + 12, 468, l2_s, size=10.8, color=MUTED))

    return figure(
        518,
        "甲醇与乙醇分子结构、氢键效应与沸点对比图",
        "对比甲醇与乙醇的双亲分子结构、分子间氢键网络导致的体积收缩与沸点暴涨数据，以及与同分异构体二甲醚的沸点差异和中性电离常数。",
        el,
    )


def build_four_bond_cleavage_map() -> str:
    """Four bond-cleavage switches of methanol and ethanol."""
    el = []
    el.extend(
        header(
            "醇分子的四个“拆键开关”：断哪根化学键，决定它产氢、造香精、变乙烯还是发光",
            "把乙醇 R–CH₂–O–H 当作拆解模板，对比甲醇“缺少 β-碳、没有 C–C 键”带来的两处关键分岔",
        )
    )

    # Central bond-cleavage banner (x=24..736, y=64..122)
    el.append(card(24, 64, 712, 58, rx=10, fill=CARD_BG, stroke=BLUE, sw=1.2))
    el.append(
        txt(
            380,
            87,
            "拆键地图：  [ R / H ] — CβH₂ — CαH₂ — O — H    （甲醇仅含 H—CαH₂—O—H，天生没有 Cβ 碳！）",
            size=12.2,
            color=INK,
            anchor="middle",
            weight="700",
        )
    )
    el.append(
        txt(
            380,
            109,
            "开关① 断 O–H 键（置换/酯化）  |  开关② 断 C–O 键（脱水/成烯）  |  开关③ 断 O–H + Cα–H（氧化）  |  开关④ 全分子燃烧/羰基化",
            size=11,
            color=BLUE,
            anchor="middle",
            weight="600",
        )
    )

    # 2x2 Quadrant Grid: Row 1 y=134..314 (h=180), Row 2 y=328..508 (h=180)
    # Q1: Cleave O-H bond (x=24..372, y=134..314)
    el.append(card(24, 134, 348, 180, rx=10))
    el.append(step_badge(42, 154, "1", fg=BLUE, bg=BLUE_SOFT, r=10))
    el.append(txt(58, 158, "开关 ① 只断 O–H 键：遇钠吐氢 · 遇酸造酯", size=12.6, color=INK, weight="700"))
    el.append(txt(40, 184, "• 与活泼金属置换（比水与钠反应温和可控）：", size=11.4, color=BODY, weight="600"))
    el.append(txt(50, 205, "2 R–OH + 2 Na → 2 R–ONa（醇钠强碱）+ H₂↑", size=11.2, color=BLUE, weight="600"))
    el.append(txt(40, 231, "• 与羧酸酯化（浓硫酸加热，可逆反应）：", size=11.4, color=BODY, weight="600"))
    el.append(txt(50, 252, "CH₃COOH + C₂H₅¹⁸OH ⇌ CH₃CO¹⁸OC₂H₅ + H₂O", size=11.2, color=TEAL, weight="700"))
    el.append(txt(40, 276, "• 同位素 ¹⁸O 铁律：“酸脱羟基（-OH），醇脱氢（-H）”", size=11.2, color=INK, weight="600"))
    el.append(txt(40, 298, "• 陈年老酒越放越香，正是乙醇与有机酸慢速生成果香酯！", size=10.8, color=MUTED))

    # Q2: Cleave C-O bond (x=388..736, y=134..314)
    el.append(card(388, 134, 348, 180, rx=10))
    el.append(step_badge(406, 154, "2", fg=ORANGE, bg=ORANGE_SOFT, r=10))
    el.append(txt(422, 158, "开关 ② 断 C–O 键：有无 β-碳让两兄弟分道扬镳！", size=12.6, color=INK, weight="700"))
    el.append(txt(404, 184, "• 乙醇（有 β-H，温控切换两条路）：", size=11.4, color=BODY, weight="600"))
    el.append(txt(414, 205, "170℃ 分子内消去 → CH₂=CH₂↑（乙烯）；140℃ → 乙醚", size=11.2, color=ORANGE, weight="600"))
    el.append(txt(404, 231, "• 甲醇（无 β-碳，常规酸催化绝不能单分子消去成烯）：", size=11.4, color=BODY, weight="600"))
    el.append(txt(414, 252, "中温脱水 → CH₃OCH₃（二甲醚清洁燃料/气雾推进剂）", size=11.2, color=BODY))
    el.append(txt(404, 276, "• 工业神反转（MTO 甲醇制烯烃）：400℃ SAPO-34 分子筛", size=11.2, color=PURPLE, weight="700"))
    el.append(txt(414, 298, "纳米笼内“碳池拼接”，把甲醇变成乙烯/丙烯造塑料！", size=10.8, color=MUTED))

    # Q3: Cleave O-H + alpha C-H (x=24..372, y=328..508)
    el.append(card(24, 328, 348, 180, rx=10))
    el.append(step_badge(42, 348, "3", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(58, 352, "开关 ③ 同断 O–H 与 α-C–H：伯醇两步阶梯氧化", size=12.6, color=INK, weight="700"))
    el.append(txt(40, 378, "• 催化脱氢（红热铜丝黑变红：2ROH + O₂ → 2RCHO + 2H₂O）", size=11.2, color=BODY, weight="600"))
    el.append(txt(40, 401, "• 强氧化剂变色（橙红重铬酸钾 → 灰绿 Cr³⁺，测酒驾经典反应）", size=11.2, color=GREEN, weight="600"))
    el.append(txt(40, 427, "• 乙醇阶梯：乙醇 → 乙醛（CH₃CHO）→ 乙酸（CH₃COOH）", size=11.2, color=BLUE, weight="700"))
    el.append(txt(40, 450, "• 甲醇阶梯：甲醇 → 甲醛（HCHO）→ 甲酸（HCOOH）→ CO₂", size=11.2, color=RED, weight="700"))
    el.append(txt(40, 475, "• 注：甲醛与甲酸仍带醛基氢，可被继续氧化直至二氧化碳！", size=10.8, color=MUTED))
    el.append(txt(40, 495, "  这条氧化阶梯搬进人体肝脏，就是真假酒的生死分界线。", size=10.8, color=MUTED))

    # Q4: Total combustion & Carbonylation (x=388..736, y=328..508)
    el.append(card(388, 328, 348, 180, rx=10))
    el.append(step_badge(406, 348, "4", fg=PURPLE, bg=PURPLE_SOFT, r=10))
    el.append(txt(422, 352, "开关 ④ 清洁燃烧、“幽灵蓝火”与羰基化重整", size=12.6, color=INK, weight="700"))
    el.append(txt(404, 378, "• 燃烧热（HHV）：甲醇 725.7 kJ/mol，乙醇 1367 kJ/mol", size=11.2, color=BODY, weight="600"))
    el.append(txt(404, 401, "• 自带氧原子助燃，几乎不生黑烟碳粒——尤其甲醇无 C–C 键，", size=11.2, color=BODY))
    el.append(txt(414, 422, "白天燃烧呈近乎全透明的“看不见的幽灵火焰”（极易误踩）！", size=11.2, color=RED, weight="700"))
    el.append(txt(404, 448, "• 铱催化 Cativa 羰基化（原子经济性 100% 造醋酸）：", size=11.2, color=PURPLE, weight="700"))
    el.append(txt(414, 470, "CH₃OH + CO → CH₃COOH（现代工业冰醋酸头号主力工艺）", size=11.2, color=INK, weight="600"))
    el.append(txt(404, 494, "• 水蒸气重整：CH₃OH + H₂O → CO₂ + 3H₂（车载移动制氢）", size=10.8, color=MUTED))

    return figure(
        522,
        "甲醇与乙醇四大化学反应拆键地图",
        "以醇分子的O-H键、C-O键、α-C-H键和全分子氧化重整为主线，系统对比甲醇与乙醇在钠置换、酯化、脱水消去、阶梯氧化及清洁燃烧中的异同。",
        el,
    )


def build_liver_oxidation_antidote_anim() -> str:
    """1-shot CSS animation of hepatic ADH/ALDH divergence + competitive inhibition rescue."""
    extra_css = """
  @keyframes laneFade {
    0% { opacity: 0.16; transform: translateX(-4px); }
    100% { opacity: 1; transform: translateX(0); }
  }
  @keyframes shieldPulse {
    0%, 45% { stroke-opacity: 0; }
    70% { stroke-opacity: 0.95; }
    100% { stroke-opacity: 0.85; }
  }
  .lv-1 { opacity: 0.16; animation: laneFade 0.85s ease-out 0.15s forwards; }
  .lv-2 { opacity: 0.16; animation: laneFade 0.85s ease-out 1.75s forwards; }
  .lv-3 { opacity: 0.16; animation: laneFade 0.95s ease-out 3.55s forwards; }
  .adh-lock { stroke-opacity: 0; animation: shieldPulse 5.2s ease-out 0s forwards; }
  @media (prefers-reduced-motion: reduce) {
    .lv-1, .lv-2, .lv-3 {
      animation: none !important;
      opacity: 1 !important;
      transform: none !important;
    }
    .adh-lock {
      animation: none !important;
      stroke-opacity: 0.85 !important;
    }
  }"""

    el = []
    el.extend(
        header(
            "肝脏里的生死分岔口：同样走过两道脱氢酶，为什么乙醇变食醋，甲醇却致盲夺命？",
            "先看上排乙醇安全代谢链 → 再看中排甲酸根锁死视神经线粒体 → 下排揭秘急诊“真酒救假酒”抢座原理",
        )
    )

    # Lane 1: Ethanol metabolism (y=66..196, h=130)
    el.append(
        f"""<g class="lv-1">
  {card(24, 66, 712, 130, rx=10, fill=GREEN_SOFT, stroke=GREEN, sw=1.2)}
  {step_badge(42, 86, "1", fg=GREEN, bg=CARD_BG, r=10)}
  {txt(58, 90, "乙醇正常代谢通道：两步脱氢变成“食醋成分”，最终化作二氧化碳和水", size=12.6, color=INK, weight="700")}

  {card(40, 104, 136, 56, rx=8, fill=CARD_BG, stroke=BLUE)}
  {txt(108, 127, "乙醇 C₂H₅OH", size=11.8, color=BLUE, anchor="middle", weight="700")}
  {txt(108, 147, "微醺镇静", size=10.8, color=MUTED, anchor="middle")}

  <line x1="180" y1="132" x2="226" y2="132" stroke="{GREEN}" stroke-width="2" marker-end="url(#arr-green)"/>
  {txt(203, 123, "ADH酶", size=10.5, color=GREEN, anchor="middle", weight="700")}

  {card(230, 104, 146, 56, rx=8, fill=CARD_BG, stroke=ORANGE)}
  {txt(303, 127, "乙醛 CH₃CHO", size=11.8, color=ORANGE, anchor="middle", weight="700")}
  {txt(303, 147, "脸红心跳·宿醉伤肝", size=10.8, color=MUTED, anchor="middle")}

  <line x1="380" y1="132" x2="428" y2="132" stroke="{GREEN}" stroke-width="2" marker-end="url(#arr-green)"/>
  {txt(404, 123, "ALDH2", size=10.5, color=GREEN, anchor="middle", weight="700")}

  {card(432, 104, 142, 56, rx=8, fill=CARD_BG, stroke=GREEN)}
  {txt(503, 127, "乙酸根 CH₃COO⁻", size=11.8, color=GREEN, anchor="middle", weight="700")}
  {txt(503, 147, "普通食醋温和代谢物", size=10.8, color=MUTED, anchor="middle")}

  <line x1="578" y1="132" x2="614" y2="132" stroke="{GREEN}" stroke-width="2" marker-end="url(#arr-green)"/>
  {card(618, 104, 104, 56, rx=8, fill=CARD_BG, stroke=GREEN)}
  {txt(670, 127, "CO₂ + H₂O", size=11.8, color=GREEN, anchor="middle", weight="700")}
  {txt(670, 147, "三羧酸循环排出", size=10.5, color=MUTED, anchor="middle")}

  {txt(40, 181, "注：约半数东亚人群携带 ALDH2 慢速突变，导致中间产物“乙醛”堆积上脸，所以喝酒脸红其实是酶警报！", size=11, color=BODY)}
</g>"""
    )

    # Lane 2: Methanol lethal bioactivation (y=208..354, h=146)
    el.append(
        f"""<g class="lv-2">
  {card(24, 208, 712, 146, rx=10, fill=RED_SOFT, stroke=RED, sw=1.2)}
  {step_badge(42, 228, "2", fg=RED, bg=CARD_BG, r=10)}
  {txt(58, 232, "甲醇致命“代谢增毒”陷阱：潜伏 10–30 小时后，甲酸根掐断视神经线粒体呼吸链！", size=12.6, color=INK, weight="700")}

  {card(40, 246, 136, 58, rx=8, fill=CARD_BG, stroke=ORANGE)}
  {txt(108, 269, "甲醇 CH₃OH", size=11.8, color=ORANGE, anchor="middle", weight="700")}
  {txt(108, 289, "初喝仅似轻度醉酒", size=10.8, color=MUTED, anchor="middle")}

  <line x1="180" y1="275" x2="226" y2="275" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>
  {txt(203, 266, "同一ADH", size=10.2, color=RED, anchor="middle", weight="700")}

  {card(230, 246, 146, 58, rx=8, fill=CARD_BG, stroke=RED_BORDER)}
  {txt(303, 269, "甲醛 HCHO", size=11.8, color=RED, anchor="middle", weight="700")}
  {txt(303, 289, "约1–2分钟即转走", size=10.8, color=MUTED, anchor="middle")}

  <line x1="380" y1="275" x2="428" y2="275" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>
  {txt(404, 266, "FDH/ALDH", size=10.0, color=RED, anchor="middle", weight="700")}

  {card(432, 246, 152, 58, rx=8, fill="#fee2e2", stroke=RED, sw=1.5)}
  {txt(508, 269, "甲酸根 HCOO⁻", size=12, color=RED, anchor="middle", weight="700")}
  {txt(508, 289, "终极真凶·极难排出！", size=10.8, color=RED, anchor="middle", weight="600")}

  <line x1="588" y1="275" x2="614" y2="275" stroke="{RED}" stroke-width="2" marker-end="url(#arr-orange)"/>
  {card(618, 246, 104, 58, rx=8, fill=CARD_BG, stroke=RED)}
  {txt(670, 268, "锁死细胞色素", size=10.8, color=RED, anchor="middle", weight="700")}
  {txt(670, 287, "c 氧化酶 → 失明", size=10.6, color=RED, anchor="middle", weight="700")}

  {txt(40, 324, "• 关键辟谣：甲醛在血中半衰期仅约 1 分钟，来不及积聚；真正致盲夺命的是排不出去的“甲酸/甲酸根”！", size=11, color=INK, weight="600")}
  {txt(40, 343, "• 剂量红线：视网膜耗氧极高，误饮纯甲醇仅 4–15 mL 即可致暴风雪样永久失明，约 30–70 mL 可致死。", size=11, color=RED, weight="600")}
</g>"""
    )

    # Lane 3: Competitive inhibition rescue in ER (y=366..514, h=148)
    el.append(
        f"""<g class="lv-3">
  {card(24, 366, 712, 148, rx=10, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.2)}
  {step_badge(42, 386, "3", fg=PURPLE, bg=CARD_BG, r=10)}
  {txt(58, 390, "急诊室“抢座位”解毒法：为什么甲吡唑或医用真乙醇能救回假酒中毒患者？", size=12.6, color=INK, weight="700")}

  {card(40, 404, 244, 94, rx=8, fill=CARD_BG, stroke=PURPLE, sw=1.3)}
  <rect class="adh-lock" x="37" y="401" width="250" height="100" rx="10" fill="none" stroke="{PURPLE}" stroke-width="2.2" stroke-dasharray="5 3"/>
  {pill(52, 412, "抢先霸占 ADH 酶活性口袋", fg=PURPLE, bg=PURPLE_SOFT, w=218, h=20, size=11)}
  {txt(52, 450, "• 首选甲吡唑（亲和力高数千倍）", size=11.2, color=PURPLE, weight="700")}
  {txt(52, 471, "• 应急输注医用乙醇（高 10–20 倍）", size=11.2, color=BLUE, weight="700")}
  {txt(52, 490, "→ 把甲醇死死堵在第一道酶门外！", size=10.8, color=BODY)}

  <line x1="288" y1="451" x2="322" y2="451" stroke="{BLUE}" stroke-width="2" marker-end="url(#arr-blue)"/>

  {card(326, 404, 190, 94, rx=8, fill=CARD_BG, stroke=BLUE)}
  {pill(338, 412, "未氧化甲醇原样排出", fg=BLUE, bg=BLUE_SOFT, w=166, h=20, size=11)}
  {txt(338, 450, "• 不再变成甲醛与甲酸根", size=11.2, color=BODY, weight="600")}
  {txt(338, 471, "• 经肾脏尿液与肺部呼吸排走", size=11.2, color=BLUE, weight="600")}
  {txt(338, 490, "• 重症同步上血液透析快速滤除", size=10.8, color=MUTED)}

  <line x1="520" y1="451" x2="548" y2="451" stroke="{GREEN}" stroke-width="2" marker-end="url(#arr-green)"/>

  {card(552, 404, 170, 94, rx=8, fill=CARD_BG, stroke=GREEN)}
  {pill(562, 412, "清除残余甲酸根组合拳", fg=GREEN, bg=GREEN_SOFT, w=150, h=20, size=10.8)}
  {txt(562, 450, "• 碳酸氢钠：纠正酸中毒", size=11, color=BODY, weight="600")}
  {txt(562, 471, "• 亚叶酸/叶酸：激活一碳", size=11, color=GREEN, weight="600")}
  {txt(572, 490, "通道把甲酸拆成 CO₂！", size=10.8, color=GREEN, weight="600")}
</g>"""
    )

    return figure(
        528,
        "乙醇与甲醇肝脏代谢分岔及急诊竞争性解毒动画",
        "分步展示乙醇经ADH与ALDH2安全转化为乙酸根、甲醇经同一酶系转化为甲酸根抑制线粒体细胞色素c氧化酶致盲的机理，以及甲吡唑和乙醇竞争性抑制ADH的急救方案。",
        el,
        extra_css=extra_css,
    )


def build_disinfection_75_vs_95() -> str:
    """Explain why 70%-75% ethanol beats 95% ethanol and where alcohol disinfectants fail."""
    el = []
    el.extend(
        header(
            "消毒反直觉真相：为什么 70%–75% 酒精杀菌稳准狠，95% 纯酒精反而失手？",
            "先对比左栏“瞬间脱水结硬壳”与中栏“水分子开路穿透全菌” → 右栏牢记酒精杀不死的三类对手",
        )
    )

    # Column 1: 95%-99% ethanol (x=24..248, y=68..496)
    el.append(card(24, 68, 224, 428, rx=10))
    el.append(step_badge(42, 88, "1", fg=ORANGE, bg=ORANGE_SOFT, r=10))
    el.append(txt(58, 92, "95%–99% 高浓乙醇", size=13, color=INK, weight="700"))
    el.append(txt(42, 112, "过猛脱水 → 表面结出“保护硬壳”", size=11.2, color=ORANGE, weight="600"))

    # Diagram of bacterium with coagulated outer crust blocking arrows
    el.append(card(40, 124, 192, 146, rx=8, fill=ORANGE_SOFT, stroke=BORDER))
    el.append(
        f"""<ellipse cx="136" cy="197" rx="58" ry="38" fill="#fef9c3" stroke="{RED}" stroke-width="6"/>
<ellipse cx="136" cy="197" rx="44" ry="25" fill="#ffffff" stroke="{HAIRLINE}" stroke-width="1.2" stroke-dasharray="3 3"/>
{txt(136, 194, "内部酶蛋白", size=10.8, color=INK, anchor="middle", weight="600")}
{txt(136, 210, "完好幸存！", size=10.8, color=RED, anchor="middle", weight="700")}
<path d="M 52,158 L 76,174 M 76,174 L 66,177 M 76,174 L 74,164" fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-linecap="round"/>
<path d="M 220,158 L 196,174 M 196,174 L 206,177 M 196,174 L 198,164" fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-linecap="round"/>
{txt(136, 145, "外膜蛋白瞬间凝固成致密硬壳", size=10.5, color=RED, anchor="middle", weight="700")}
{txt(136, 256, "后续酒精分子被自己造的壳挡在门外", size=10.2, color=BODY, anchor="middle")}"""
    )

    el.append(txt(40, 294, "• 机理：纯乙醇是强脱水剂，一碰", size=11.3, color=BODY, weight="600"))
    el.append(txt(50, 315, "细菌外壳就令表层蛋白瞬间凝结", size=11.3, color=BODY))
    el.append(txt(40, 341, "• 后果：硬壳阻断酒精继续向细胞", size=11.3, color=BODY))
    el.append(txt(50, 362, "内部渗透，且挥发极快停留太短", size=11.3, color=BODY))
    el.append(txt(40, 388, "• 部分微生物仅暂时休眠，等酒精", size=11.3, color=ORANGE, weight="600"))
    el.append(txt(50, 409, "挥发干后仍可能“死灰复燃”！", size=11.3, color=ORANGE, weight="600"))
    el.append(txt(40, 442, "• 95% 酒精真正用途：紫外灯擦拭、", size=11, color=MUTED))
    el.append(txt(50, 462, "酒精灯燃料、病理组织脱水固定", size=11, color=MUTED))

    # Column 2: 70%-75% ethanol (x=268..492, y=68..496)
    el.append(card(268, 68, 224, 428, rx=10, stroke=GREEN, sw=1.4))
    el.append(step_badge(286, 88, "2", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(302, 92, "70%–75% 医用乙醇", size=13, color=INK, weight="700"))
    el.append(txt(286, 112, "水分子开路 → 溶膜 + 全员蛋白变性", size=11.2, color=GREEN, weight="700"))

    # Diagram of hydrated permeable membrane + internal denaturation
    el.append(card(284, 124, 192, 146, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        f"""<ellipse cx="380" cy="197" rx="58" ry="38" fill="#ffffff" stroke="{GREEN}" stroke-width="2.6" stroke-dasharray="7 5"/>
<path d="M 300,174 L 342,188" fill="none" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>
<path d="M 460,174 L 418,188" fill="none" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>
<path d="M 352,196 Q 364,182 376,198 Q 388,214 404,192" fill="none" stroke="{GREEN}" stroke-width="2.6" stroke-linecap="round"/>
{txt(380, 145, "水分子延缓挥发并保持膜孔张开", size=10.5, color=BLUE, anchor="middle", weight="700")}
{txt(380, 222, "胞内酶解链失活·彻底死亡", size=10.6, color=GREEN, anchor="middle", weight="700")}
{txt(380, 256, "CDC 黄金窗口：60%–80%（v/v）", size=10.5, color=INK, anchor="middle", weight="700")}"""
    )

    el.append(txt(284, 294, "• 第一步（破墙）：碳氢尾巴插入并", size=11.3, color=BODY, weight="600"))
    el.append(txt(294, 315, "溶解细菌细胞膜与病毒脂质包膜", size=11.3, color=BODY))
    el.append(txt(284, 341, "• 第二步（攻心）：25%–30% 的水", size=11.3, color=BODY, weight="600"))
    el.append(txt(294, 362, "防止表皮过早结壳，协助乙醇深", size=11.3, color=BODY))
    el.append(txt(294, 383, "入内部拆散蛋白质氢键与疏水核", size=11.3, color=BODY))
    el.append(txt(284, 411, "• 实测速度：10 秒内灭活金葡菌、", size=11.3, color=GREEN, weight="700"))
    el.append(txt(294, 432, "大肠杆菌、流感病毒与冠状病毒", size=11.3, color=GREEN, weight="700"))
    el.append(txt(284, 462, "• 低于 50% 时杀菌力断崖式下跌", size=11, color=MUTED))

    # Column 3: Three blind spots & methanol warning (x=512..736, y=68..496)
    el.append(card(512, 68, 224, 428, rx=10))
    el.append(step_badge(530, 88, "3", fg=RED, bg=RED_SOFT, r=10))
    el.append(txt(546, 92, "酒精消毒三大禁区", size=13, color=INK, weight="700"))
    el.append(txt(530, 112, "这些场景喷再多酒精也不管用！", size=11.2, color=RED, weight="600"))

    blind_boxes = [
        (
            126,
            "禁区① 细菌芽孢纹丝不动",
            "破伤风梭菌、炭疽芽孢有厚壁盔甲，",
            "手术刀绝不能只泡酒精（需高温高压）",
            PURPLE,
            PURPLE_SOFT,
        ),
        (
            242,
            "禁区② 部分无包膜肠道病毒",
            "诺如病毒、甲肝病毒、脊灰病毒没有",
            "脂质包膜，需肥皂流水洗手或含氯消毒",
            BLUE,
            BLUE_SOFT,
        ),
        (
            358,
            "禁区③ 严禁拿甲醇冒充消毒水",
            "CDC 明文指出：甲醇杀菌力在醇类中",
            "最垫底，且经皮肤吸收与吸入可中毒！",
            RED,
            RED_SOFT,
        ),
    ]
    for by, b_head, b_l1, b_l2, fg_c, bg_c in blind_boxes:
        el.append(card(526, by, 196, 104, rx=8, fill=CARD_BG, stroke=fg_c, sw=1.1))
        el.append(pill(536, by + 8, b_head, fg=fg_c, bg=bg_c, w=176, h=20, size=10.6))
        el.append(txt(536, by + 50, b_l1, size=10.8, color=BODY))
        el.append(txt(536, by + 72, b_l2, size=10.8, color=INK, weight="600"))

    el.append(txt(528, 482, "安全提示：远离明火，切勿大面积喷洒空气", size=10.6, color=RED, weight="600"))

    return figure(
        512,
        "70%-75%医用乙醇与95%乙醇杀菌机理对比及消毒盲区图解",
        "对比95%乙醇使细菌表面蛋白瞬间凝固结壳阻挡渗透与70%-75%乙醇借助水分子穿透细胞膜彻底变性蛋白质的机理，并列出细菌芽孢、无包膜病毒及禁用甲醇三大注意事项。",
        el,
    )


def build_industrial_and_green_future() -> str:
    """Dual industrial & clean-energy panorama of methanol and ethanol."""
    el = []
    el.extend(
        header(
            "双醇工业帝国与零碳未来：一个撑起 C1 化工与远洋巨轮，一个横跨药房、实验室与油箱",
            "左栏看甲醇如何从煤/绿氢变成塑料与船用清洁燃料 → 右栏看乙醇如何凭双亲结构与高辛烷值通吃四大领域",
        )
    )

    # Left half: Methanol C1 Empire & Liquid Sunshine (x=24..372, y=68..498)
    el.append(card(24, 68, 348, 430, rx=10, fill=CARD_BG, stroke=TEAL, sw=1.3))
    el.append(pill(38, 80, "甲醇 CH₃OH：全球年产超亿吨的“C1 化工之母”", fg=TEAL, bg=TEAL_SOFT, w=320, h=24, size=11.6))

    # Feedstock box
    el.append(card(38, 114, 320, 68, rx=8, fill=TEAL_SOFT, stroke=TEAL, sw=1))
    el.append(txt(50, 135, "经典低压合成（ICI 铜锌铝催化）：CO + 2H₂ → CH₃OH", size=11, color=INK, weight="700"))
    el.append(txt(50, 156, "零碳“液态阳光”路线：绿电制 H₂ + 捕集 CO₂ → 绿色甲醇", size=11, color=TEAL, weight="700"))
    el.append(txt(50, 174, "（把难存难运的氢气与二氧化碳，锁进常温常压液体里！）", size=10.5, color=MUTED))

    meoh_uses = [
        ("① 聚合物基石（甲醛·约占3成）", "氧化制甲醛 → 脲醛/酚醛树脂、聚甲醛工程塑料（POM）", ORANGE),
        ("② MTO 煤/气制烯烃（中国王牌）", "绕开石油！分子筛催化甲醇直产乙烯、丙烯造日用塑料", PURPLE),
        ("③ 冰醋酸与燃油添加剂", "Cativa 法与 CO 合成乙酸；合成 MTBE、生物柴油酯交换", BLUE),
        ("④ 防冻玻璃水与深海油气防堵", "低冰点（-97.6℃）防结冰；注入海底管道防天然气水合物冰堵", SLATE),
        ("⑤ 远洋双燃料巨轮与燃料电池", "体积能量密度 15.6 MJ/L，几乎零硫氧化物，航运脱碳主力", GREEN),
    ]
    for idx, (u_title, u_desc, col) in enumerate(meoh_uses):
        uy = 194 + idx * 58
        el.append(card(38, uy, 320, 50, rx=7, fill=BG, stroke=BORDER))
        el.append(f'<rect x="38" y="{uy}" width="5" height="50" rx="2.5" fill="{col}"/>')
        el.append(txt(52, uy + 20, u_title, size=11.4, color=col, weight="700"))
        el.append(txt(52, uy + 39, u_desc, size=10.6, color=BODY))

    # Right half: Ethanol Versatile Champion (x=388..736, y=68..498)
    el.append(card(388, 68, 348, 430, rx=10, fill=CARD_BG, stroke=BLUE, sw=1.3))
    el.append(pill(402, 80, "乙醇 C₂H₅OH：横跨能源、医药与科研的“万能桥梁”", fg=BLUE, bg=BLUE_SOFT, w=320, h=24, size=11.6))

    # Feedstock box
    el.append(card(402, 114, 320, 68, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1))
    el.append(txt(414, 135, "生物发酵法（占全球逾9成）：C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂↑", size=11, color=INK, weight="700"))
    el.append(txt(414, 156, "石化水合法（高纯工业醇）：CH₂=CH₂ + H₂O → C₂H₅OH", size=11, color=BLUE, weight="700"))
    el.append(txt(414, 174, "（无水乙醇需分子筛吸附打破 95.6% 共沸极限）", size=10.5, color=MUTED))

    etoh_uses = [
        ("① 高辛烷值车用燃料（头号消耗）", "E10/E85 汽油（RON 辛烷值≈108.6 抗爆震，能量密度 21–24 MJ/L）", ORANGE),
        ("② 药房与日化“万能双亲溶剂”", "碘酊、止咳糖浆等逾 700 种液态药物辅料；香水定香快干", BLUE),
        ("③ 医疗感控与甲醇中毒急救", "70%–75% 表面及手部消毒；无甲吡唑时静脉/口服竞争解毒", GREEN),
        ("④ 实验室超低温浴与 DNA 提纯", "配干冰制 -78℃ 冷浴（凝固点 -114℃）；破坏水合层析出 DNA", PURPLE),
        ("⑤ 千年酿造饮品与风味酯合成", "白酒/葡萄酒/啤酒灵魂成分；合成乙酸乙酯等食品果香香精", AMBER),
    ]
    for idx, (u_title, u_desc, col) in enumerate(etoh_uses):
        uy = 194 + idx * 58
        el.append(card(402, uy, 320, 50, rx=7, fill=BG, stroke=BORDER))
        el.append(f'<rect x="402" y="{uy}" width="5" height="50" rx="2.5" fill="{col}"/>')
        el.append(txt(416, uy + 20, u_title, size=11.4, color=col, weight="700"))
        el.append(txt(416, uy + 39, u_desc, size=10.6, color=BODY))

    return figure(
        514,
        "甲醇与乙醇工业生产路线及五大核心用途全景图",
        "对比甲醇（合成气与绿色甲醇路线、甲醛树脂、MTO制烯烃、醋酸、防冻防堵及远洋船用燃料）与乙醇（发酵与乙烯水合、E10/E85高辛烷值燃料、医药香水双亲溶剂、医疗消毒解毒、低温冷浴与DNA沉淀、食品酿造）的全景用途。",
        el,
    )


@register("methanol-ethanol", "甲醇与乙醇的化学性质、毒理分岔与工业用途图解", "chemistry")
def build_all() -> list[str]:
    _verify_chemical_metrics()
    specs = [
        ("molecule-hbond-boiling-jump.svg", build_molecule_hbond_boiling()),
        ("four-bond-cleavage-map.svg", build_four_bond_cleavage_map()),
        ("liver-oxidation-and-antidote-anim.svg", build_liver_oxidation_antidote_anim()),
        ("disinfection-75-vs-95-ethanol.svg", build_disinfection_75_vs_95()),
        ("industrial-tree-and-green-methanol.svg", build_industrial_and_green_future()),
    ]
    written = []
    for fname, svg_text in specs:
        write_svg(SUBDIR, fname, svg_text)
        written.append(f"assets/images/{SUBDIR}/{fname}")
    return written
