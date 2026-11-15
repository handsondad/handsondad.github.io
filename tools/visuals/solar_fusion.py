"""Original SVG diagrams for the solar nuclear fusion process (quantum tunneling, pp-chain, CNO cycle, mass defect, and photon/neutrino escape)."""

import math
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

SUBDIR = "solar-fusion"

RED = "#dc2626"
RED_SOFT = "#fef2f2"
RED_BORDER = "#fca5a5"
AMBER = "#b45309"
AMBER_SOFT = "#fef3c7"
TEAL = "#0f766e"
TEAL_SOFT = "#ccfbf1"


def _verify_solar_metrics():
    """Verify nuclear mass defect, Q-values, E=mc^2 mass conversion, and Gamow/power metrics."""
    # Atomic masses in u (CODATA / AME): 1H = 1.007825032 u, 4He = 4.002603254 u, 1 u = 931.4941 MeV/c^2
    m_4h = 4 * 1.007825032
    m_he4 = 4.002603254
    dm_u = m_4h - m_he4
    frac_loss = dm_u / m_4h
    q_mev = dm_u * 931.4941
    assert abs(dm_u - 0.028697) < 1e-4
    assert abs(frac_loss - 0.007119) < 1e-4
    assert abs(q_mev - 26.731) < 0.01

    # pp-I energy budget: 2*(1.442) + 2*(5.493) + 12.859 = 26.729 MeV
    pp1_sum = 2 * 1.442 + 2 * 5.493 + 12.859
    assert abs(pp1_sum - 26.729) < 0.01

    # Solar luminosity L_sun = 3.828e26 W -> dm/dt = L / c^2
    l_sun = 3.828e26
    c = 299_792_458.0
    dm_kg_s = l_sun / (c * c)
    dm_million_tonnes = dm_kg_s / 1e9  # 10^6 metric tonnes/s (万吨/s = dm_kg_s / 1e7)
    assert abs(dm_million_tonnes - 4.259) < 0.01
    h_fused_100m_tonnes = (dm_kg_s / frac_loss) / 1e11  # 亿吨/s
    assert 5.95 < h_fused_100m_tonnes < 6.05

    # Core thermal energy k_B * T at 1.571e7 K
    kb_ev = 8.617333e-5
    kt_kev = kb_ev * 1.571e7 / 1000.0
    assert abs(kt_kev - 1.354) < 0.01


def build_coulomb_tunneling_weak_lock() -> str:
    """Diagram 1: Quantum tunneling across the Coulomb barrier & the 9-billion-year weak-force bottleneck."""
    _verify_solar_metrics()
    el = []
    el.extend(
        header(
            "1570 万度根本不够点火？“量子穿墙术”与“90 亿年弱力慢门”双密码",
            "左栏看质子怎样钻过百倍高的静电排斥山峰 → 右栏看为什么太阳不像氢弹一秒炸完、功率密度还不如人体",
        )
    )

    # Left panel: Coulomb Barrier & Gamow Peak Quantum Tunneling (x=24..382, y=68..508)
    el.append(card(24, 68, 358, 440, rx=10))
    el.append(step_badge(42, 88, "1", fg=BLUE, bg=BLUE_SOFT, r=10))
    el.append(txt(58, 92, "第一关：翻不过库仑高山，全靠伽莫夫“量子隧穿”", size=12.0, color=INK, weight="700"))

    # Potential energy plot box (x=40..366, y=108..322)
    el.append(card(40, 108, 326, 214, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    # Axes: x from 76 to 348, baseline y=272, nuclear well x=76..114 (y=306), peak at x=114, y=132 (~550 keV)
    el.append(f'<line x1="68" y1="272" x2="352" y2="272" stroke="{SLATE}" stroke-width="1.4"/>')
    el.append(f'<line x1="76" y1="120" x2="76" y2="310" stroke="{SLATE}" stroke-width="1.4"/>')
    # Shaded nuclear strong-force well
    el.append(f'<rect x="76" y="272" width="38" height="32" fill="{GREEN_SOFT}"/>')
    # Coulomb 1/r curve from x=114..346
    coul_pts = []
    for i in range(40):
        rx = 114 + i * 6.0
        # 1/r decay from y=134 down toward y=266
        ry = 272 - 138.0 * (38.0 / (38.0 + (rx - 114)))
        coul_pts.append(f"{rx:.1f},{ry:.1f}")
    poly_coul = f"76,304 114,304 114,134 " + " ".join(coul_pts)
    el.append(f'<polyline points="{poly_coul}" fill="none" stroke="{RED}" stroke-width="2.6"/>')

    # Tunneling wave band around Gamow Peak (~6 keV, y=238)
    el.append(f'<rect x="114" y="230" width="166" height="16" fill="{BLUE_SOFT}" opacity="0.85"/>')
    wave_pts = []
    for i in range(34):
        wx = 280 - i * 5.0
        amp = 5.5 if wx > 215 else (2.5 * max(0.25, (wx - 114) / 101.0))
        wy = 238 + amp * math.sin(i * 1.15)
        wave_pts.append(f"{wx:.1f},{wy:.1f}")
    el.append(f'<polyline points="{" ".join(wave_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
    el.append(f'<line x1="126" y1="238" x2="98" y2="238" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>')

    # Thermal average line (1.35 keV, y=262)
    el.append(f'<line x1="76" y1="262" x2="346" y2="262" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="4 3"/>')

    el.append(txt(122, 130, "同性电荷库仑势垒峰 ≈ 550 keV（需几十亿度！）", size=10.0, color=RED, weight="700"))
    el.append(txt(95, 293, "强核力深井", size=9.6, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(244, 224, "伽莫夫隧穿窗口 ≈ 6 keV（概率波穿墙！）", size=10.0, color=BLUE, anchor="middle", weight="700", halo=True))
    el.append(txt(258, 258, "核心平均热动能 kT ≈ 1.35 keV", size=9.8, color=ORANGE, anchor="middle", weight="600"))
    el.append(txt(214, 312, "两颗质子间距 r（强力吸引区 < 2 飞米） →", size=10.0, color=MUTED, anchor="middle"))

    el.append(txt(40, 346, "• 经典死局：太阳核心 1571 万 K 的质子平均动能仅 1.35 keV，", size=10.6, color=BODY))
    el.append(txt(50, 366, "离翻越 550 keV 静电排斥墙差了 400 倍，按经典物理绝无可能点火！", size=10.6, color=BODY))
    el.append(txt(40, 390, "• 量子破局（1928 伽莫夫）：微观质子不是硬钢珠，而是弥散的概率波；", size=10.6, color=BLUE, weight="600"))
    el.append(txt(50, 410, "高能尾端约 6 keV 的快质子，靠“量子隧穿”直接钻进山体另一侧。", size=10.6, color=BLUE, weight="600"))
    el.append(txt(40, 434, "• 即使靠穿墙术撞进核力范围，两颗裸质子拼成的“双质子 ²He”极不稳，", size=10.6, color=BODY))
    el.append(txt(50, 454, "超 99.999999% 会在 10⁻²¹ 秒内原路弹开——还得等右边第二道慢门！", size=10.6, color=INK, weight="600"))
    el.append(txt(40, 488, "（注：纵轴能量刻度做示意拉伸，突出 1.35 / 6 / 550 keV 三级反差）", size=9.8, color=MUTED))

    # Right panel: Weak-force bottleneck vs H-Bomb + Compost heap power density (x=398..736, y=68..508)
    el.append(card(398, 68, 338, 440, rx=10))
    el.append(step_badge(416, 88, "2", fg=PURPLE, bg=PURPLE_SOFT, r=10))
    el.append(txt(432, 92, "第二关：为什么太阳没像氢弹一样一秒炸光？", size=12.0, color=INK, weight="700"))

    # H-bomb vs Sun box (y=108..288)
    el.append(card(414, 108, 306, 82, rx=8, fill=RED_SOFT, stroke=RED_BORDER))
    el.append(pill(424, 116, "人造氢弹（氘 D + 氚 T）：自带中子，强核力秒炸", fg=RED, bg="#fee2e2", w=282, h=20, size=10.4))
    el.append(txt(424, 154, "• 反应：²D + ³T → ⁴He + n，无需质子临时变中子", size=10.5, color=BODY))
    el.append(txt(424, 174, "• 纯走强核力高速路，百万分之一秒内倾泻全部能量！", size=10.5, color=RED, weight="700"))

    el.append(card(414, 200, 306, 98, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(pill(424, 208, "太阳核心（质子 p + 质子 p）：弱核力卡住咽喉！", fg=PURPLE, bg="#ede9fe", w=282, h=20, size=10.4))
    el.append(txt(424, 245, "• 没有现成中子！必须在撞击那 10⁻²¹ 秒瞬间触发弱核力", size=10.4, color=BODY))
    el.append(txt(424, 265, "  β⁺ 衰变（p → n + e⁺ + νₑ），才能锁死成稳定的氘核 ²D。", size=10.4, color=PURPLE, weight="700"))
    el.append(txt(424, 285, "• 平均每颗质子每秒撞上亿次，却要排队苦等约 90 亿年！", size=10.4, color=INK, weight="700"))

    # Volumetric Power Density Shock Comparison (y=310..492)
    el.append(card(414, 310, 306, 182, rx=8, fill=AMBER_SOFT, stroke=ORANGE))
    el.append(txt(426, 332, "颠覆直觉：太阳最中心每立方米发热还不如你的身体！", size=11.1, color=AMBER, weight="700"))

    # Horizontal bars comparing volumetric power density (W/m^3)
    # Sun core center: 276.5 W/m^3; Compost pile: ~250-300 W/m^3; Resting adult human: ~1200 W/m^3
    el.append(txt(426, 358, "太阳核心峰值", size=10.4, color=INK, weight="700"))
    el.append(f'<rect x="506" y="346" width="46" height="16" rx="4" fill="{ORANGE}"/>')
    el.append(txt(558, 358, "276.5 W/m³（≈ 农家发酵堆肥堆）", size=10.2, color=INK, weight="600"))

    el.append(txt(426, 386, "静卧成年人体", size=10.4, color=RED, weight="700"))
    el.append(f'<rect x="506" y="374" width="194" height="16" rx="4" fill="{RED}"/>')
    el.append(txt(514, 386, "≈ 1200 W/m³（太阳中心的 4.3 倍！）", size=10.0, color="#ffffff", weight="700"))

    el.append(txt(426, 416, "• 70 kg 人体体积约 0.07 m³，静息功率 85 W → 1214 W/m³！", size=10.3, color=BODY))
    el.append(txt(426, 437, "• 为什么太阳还能飙到 1571 万度？因为核心体积高达地球", size=10.3, color=BODY))
    el.append(txt(434, 457, "的 3 万多倍，外裹 70 万公里厚隔热层，热量攒了十万年", size=10.3, color=INK, weight="600"))
    el.append(txt(434, 477, "排不出去！慢门锁死了功率，才赐予地球百亿年温柔阳光。", size=10.3, color=AMBER, weight="700"))

    return figure(
        522,
        "太阳核聚变伽莫夫量子隧穿与弱核力90亿年慢门机理图",
        "左栏展示1.35 keV核心质子如何借约6 keV伽莫夫窗口量子隧穿翻越约550 keV库仑势垒，右栏对比氢弹强核力瞬爆与太阳弱核力90亿年等待时间，并定量对比太阳核心276.5 W/m³与人体1200 W/m³的单位体积发热功率。",
        el,
    )


def build_pp_chain_anim() -> str:
    """1-shot CSS animation of the 3-step proton-proton chain (pp-I + pp-II/III overview)."""
    _verify_solar_metrics()
    extra_css = """
  @keyframes sfStep {
    0% { opacity: 0.15; transform: translateY(4px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  .sf-1 { opacity: 0.15; animation: sfStep 0.85s ease-out 0.15s forwards; }
  .sf-2 { opacity: 0.15; animation: sfStep 0.85s ease-out 1.75s forwards; }
  .sf-3 { opacity: 0.15; animation: sfStep 0.90s ease-out 3.35s forwards; }
  @media (prefers-reduced-motion: reduce) {
    .sf-1, .sf-2, .sf-3 {
      animation: none !important;
      opacity: 1 !important;
      transform: none !important;
    }
  }"""

    el = []
    el.extend(
        header(
            "四颗质子怎样拼成一颗氦核？分步跟读占太阳 99% 能量的“质子—质子链”",
            "按上→中→下三步跟读 pp-I 主干道（领 6 颗质子入场、退还 2 颗媒人质子）→ 底栏速查 pp-II / pp-III 支线",
        )
    )

    # Step 1: p + p -> 2D + e+ + nu_e (happens x2) (y=66..196, h=130)
    el.append(
        f"""<g class="sf-1">
  {card(24, 66, 712, 130, rx=10, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.2)}
  {step_badge(42, 86, "1", fg=PURPLE, bg=CARD_BG, r=10)}
  {txt(58, 90, "第一步（弱核力破冰 · 需平行发生 ×2 次）：两颗质子隧穿相撞，一颗变身中子锁成“氘核 ²D”", size=12.0, color=INK, weight="700")}

  {card(40, 104, 152, 58, rx=8, fill=CARD_BG, stroke=RED)}
  <circle cx="72" cy="133" r="11" fill="{RED}"/>{txt(72, 137, "p⁺", size=10.2, color="#fff", anchor="middle", weight="700")}
  {txt(96, 137, "+", size=13, color=INK, anchor="middle", weight="700")}
  <circle cx="120" cy="133" r="11" fill="{RED}"/>{txt(120, 137, "p⁺", size=10.2, color="#fff", anchor="middle", weight="700")}
  {txt(162, 137, "×2组", size=10.6, color=PURPLE, anchor="middle", weight="700")}

  <line x1="196" y1="133" x2="252" y2="133" stroke="{PURPLE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>
  {txt(224, 122, "等90亿年", size=9.8, color=PURPLE, anchor="middle", weight="700")}

  {card(256, 104, 198, 58, rx=8, fill=CARD_BG, stroke=PURPLE)}
  <circle cx="284" cy="133" r="11" fill="{RED}"/>{txt(284, 137, "p⁺", size=9.8, color="#fff", anchor="middle", weight="700")}
  <circle cx="305" cy="133" r="11" fill="{SLATE}"/>{txt(305, 137, "n⁰", size=9.8, color="#fff", anchor="middle", weight="700")}
  {txt(384, 127, "重氢：氘核 ²₁D（×2）", size=11.0, color=INK, anchor="middle", weight="700")}
  {txt(384, 147, "1质子 + 1中子紧紧吸住", size=10.0, color=MUTED, anchor="middle")}

  <line x1="458" y1="133" x2="496" y2="133" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>

  {card(500, 104, 220, 58, rx=8, fill=CARD_BG, stroke=ORANGE)}
  {txt(610, 126, "抛出 e⁺ 正电子 + νₑ 电子中微子", size=10.8, color=ORANGE, anchor="middle", weight="700")}
  {txt(610, 147, "e⁺遇电子湮灭成2γ · 每组放能 1.442 MeV", size=10.0, color=BODY, anchor="middle")}

  {txt(40, 182, "• 方程：¹H + ¹H → ²D + e⁺ + νₑ（连同 e⁺+e⁻→2γ 湮灭，两组共释放 2 × 1.442 = 2.884 MeV；中微子 2.3 秒直飞出太阳）", size=10.5, color=BODY)}
</g>"""
    )

    # Step 2: 2D + 1H -> 3He + gamma (happens x2) (y=208..336, h=128)
    el.append(
        f"""<g class="sf-2">
  {card(24, 208, 712, 128, rx=10, fill=BLUE_SOFT, stroke=BLUE, sw=1.2)}
  {step_badge(42, 228, "2", fg=BLUE, bg=CARD_BG, r=10)}
  {txt(58, 232, "第二步（强核力秒杀 · 同样发生 ×2 次）：刚出生的氘核只活约 1 秒，立刻吞下第 3 颗质子变“氦-3”", size=12.0, color=INK, weight="700")}

  {card(40, 246, 186, 56, rx=8, fill=CARD_BG, stroke=BLUE)}
  {txt(133, 270, "氘核 ²₁D + 第3颗质子 ¹₁H", size=11.0, color=BLUE, anchor="middle", weight="700")}
  {txt(133, 290, "（上下两路同步进行 ×2 组）", size=10.0, color=MUTED, anchor="middle")}

  <line x1="230" y1="274" x2="290" y2="274" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#arr-blue)"/>
  {txt(260, 264, "仅需 ~1 秒!", size=10.0, color=BLUE, anchor="middle", weight="700")}

  {card(294, 246, 206, 56, rx=8, fill=CARD_BG, stroke=TEAL)}
  <circle cx="322" cy="274" r="10" fill="{RED}"/>
  <circle cx="340" cy="268" r="10" fill="{RED}"/>
  <circle cx="332" cy="284" r="10" fill="{SLATE}"/>
  {txt(424, 270, "轻氦同位素：氦-3 ³₂He（×2）", size=10.8, color=TEAL, anchor="middle", weight="700")}
  {txt(424, 290, "2 质子 + 1 中子稳定核", size=10.0, color=MUTED, anchor="middle")}

  <line x1="504" y1="274" x2="540" y2="274" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>

  {card(544, 246, 176, 56, rx=8, fill=CARD_BG, stroke=ORANGE)}
  {txt(632, 270, "射出高能伽马光子 γ", size=11.0, color=ORANGE, anchor="middle", weight="700")}
  {txt(632, 290, "每组释放 5.493 MeV", size=10.4, color=INK, anchor="middle", weight="600")}

  {txt(40, 322, "• 方程：²D + ¹H → ³He + γ（无需弱力变身，强核力瞬间拉拢，两组共释放 2 × 5.493 = 10.986 MeV 辐射热能）", size=10.5, color=BODY)}
</g>"""
    )

    # Step 3: 3He + 3He -> 4He + 2 1H (pp-I 83.3%) + pp-II / pp-III branches (y=348..524, h=176)
    el.append(
        f"""<g class="sf-3">
  {card(24, 348, 712, 176, rx=10, fill=GREEN_SOFT, stroke=GREEN, sw=1.3)}
  {step_badge(42, 368, "3", fg=GREEN, bg=CARD_BG, r=10)}
  {txt(58, 372, "第三步（终极合体 · 氦-3 平均巡游约 400 年）：两颗氦-3 迎头拼出氦-4，原封不动退还 2 颗媒人质子！", size=11.8, color=INK, weight="700")}

  {card(40, 386, 184, 58, rx=8, fill=CARD_BG, stroke=TEAL)}
  {txt(132, 410, "³₂He  +  ³₂He", size=12.0, color=TEAL, anchor="middle", weight="700")}
  {txt(132, 431, "pp-I 主干道（占 pp 链 83.3%）", size=10.0, color=BODY, anchor="middle")}

  <line x1="228" y1="415" x2="282" y2="415" stroke="{GREEN}" stroke-width="2.4" marker-end="url(#arr-green)"/>
  {txt(255, 405, "~400年", size=9.8, color=GREEN, anchor="middle", weight="700")}

  {card(286, 386, 224, 58, rx=8, fill=CARD_BG, stroke=GREEN)}
  {txt(398, 409, "氦-4 ⁴₂He（α粒子）+ 退回 2 颗 ¹₁H", size=11.0, color=GREEN, anchor="middle", weight="700")}
  {txt(398, 430, "领 6 颗氢进场，退 2 颗，净耗 4 颗！", size=10.2, color=INK, anchor="middle", weight="600")}

  <line x1="514" y1="415" x2="546" y2="415" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>

  {card(550, 386, 170, 58, rx=8, fill=CARD_BG, stroke=RED)}
  {txt(635, 409, "单步猛放 12.859 MeV", size=11.0, color=RED, anchor="middle", weight="700")}
  {txt(635, 430, "全链总计 26.731 MeV!", size=10.4, color=INK, anchor="middle", weight="700")}

  {card(40, 454, 680, 58, rx=8, fill=CARD_BG, stroke=BORDER)}
  {txt(52, 475, "• 旁路支线：pp-II（约 16.68%）：³He 先抱住现成的 ⁴He 变铍-7（⁷Be），俘获电子变锂-7（⁷Li），再吃 1 颗质子裂成两颗 ⁴He；", size=10.3, color=BODY)}
  {txt(52, 497, "• 探针支线：pp-III（仅 0.02%）：⁷Be 再吃 1 颗质子变硼-8（⁸B）衰变出高达 14.06 MeV 超高能中微子，帮人类解开中微子失踪案！", size=10.3, color=PURPLE, weight="600")}
</g>"""
    )

    return figure(
        538,
        "太阳质子—质子链（pp链）三步核聚变分步动画图",
        "分三步展示占太阳99%能量的质子—质子链：第一步两对质子经弱力β+衰变生成两颗氘核，第二步氘核在1秒内捕获质子生成两颗氦-3，第三步两颗氦-3合成为氦-4并退还两颗质子，总释放26.731 MeV能量，并附pp-II与pp-III分支。",
        el,
        extra_css=extra_css,
    )


def build_cno_wheel_vs_pp() -> str:
    """Diagram 3: CNO-I catalytic cycle wheel & PP vs CNO temperature sensitivity curve."""
    el = []
    el.extend(
        header(
            "太阳核心 1% 的隐藏副业：碳氮氧（CNO）催化转盘与恒星温度分水岭",
            "左栏顺时针看碳-12 怎样当“不消耗媒人”吞四颗氢吐一颗氦 → 右栏看为什么超 1.3 倍太阳质量恒星全靠它当家",
        )
    )

    # Left panel: CNO-I 6-step catalytic wheel (x=24..382, y=68..508)
    el.append(card(24, 68, 358, 440, rx=10))
    el.append(step_badge(42, 88, "1", fg=TEAL, bg=TEAL_SOFT, r=10))
    el.append(txt(58, 92, "CNO-I 催化转盘：碳-12 借壳生蛋，循环不息", size=12.0, color=INK, weight="700"))

    # Wheel center (cx=203, cy=254, R=106)
    cx, cy, R = 203, 254, 106
    el.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{TEAL}" stroke-width="2.2" stroke-dasharray="6 4"/>')
    el.append(f'<circle cx="{cx}" cy="{cy}" r="54" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="1.2"/>')
    el.append(txt(cx, cy - 12, "催化净反应", size=10.6, color=TEAL, anchor="middle", weight="700"))
    el.append(txt(cx, cy + 7, "4 ¹H → ⁴He", size=11.4, color=INK, anchor="middle", weight="700"))
    el.append(txt(cx, cy + 25, "26.73 MeV", size=10.2, color=BODY, anchor="middle", weight="600"))

    nodes = [
        (-90, "¹²C", "碳-12 起点", "+p → γ", BLUE, BLUE_SOFT),
        (-30, "¹³N", "9.97分 β⁺", "e⁺+νₑ", ORANGE, ORANGE_SOFT),
        (30, "¹³C", "碳-13", "+p → γ", BLUE, BLUE_SOFT),
        (90, "¹⁴N", "最慢瓶颈!", "+p 极慢", RED, RED_SOFT),
        (150, "¹⁵O", "122秒 β⁺", "e⁺+νₑ", ORANGE, ORANGE_SOFT),
        (210, "¹⁵N", "氮-15 收官", "+p→⁴He!", GREEN, GREEN_SOFT),
    ]
    for deg, sym, sub1, sub2, fg_c, bg_c in nodes:
        rad = math.radians(deg)
        nx = cx + R * math.cos(rad)
        ny = cy + R * math.sin(rad)
        el.append(card(nx - 42, ny - 24, 84, 48, rx=8, fill=bg_c, stroke=fg_c, sw=1.4))
        el.append(txt(nx, ny - 5, f"{sym} ({sub2})", size=9.9, color=fg_c, anchor="middle", weight="700"))
        el.append(txt(nx, ny + 13, sub1, size=9.4, color=INK, anchor="middle", weight="600"))

    el.append(txt(40, 404, "• 催化剂奥秘：太阳诞生时继承自前代超新星的少量 ¹²C，顺时针", size=10.5, color=BODY))
    el.append(txt(50, 424, "连吞 4 颗质子 + 2 次 β⁺ 衰变，最后在 ¹⁵N+¹H→¹²C+⁴He 吐出氦核", size=10.5, color=BODY))
    el.append(txt(50, 444, "并满血变回 ¹²C！最慢一步卡在 ¹⁴N 吃质子（决定球状星团年龄）。", size=10.5, color=INK, weight="600"))
    el.append(txt(40, 468, "• 2020 里程碑：意大利地下 Borexino 实验首次直接抓到太阳 CNO", size=10.5, color=TEAL, weight="700"))
    el.append(txt(50, 488, "中微子（《Nature》），实锤证实它贡献了太阳约 0.8%~1% 能量！", size=10.5, color=TEAL, weight="700"))

    # Right panel: Temperature dependence PP (~T^4) vs CNO (~T^16-17) (x=398..736, y=68..508)
    el.append(card(398, 68, 338, 440, rx=10))
    el.append(step_badge(416, 88, "2", fg=PURPLE, bg=PURPLE_SOFT, r=10))
    el.append(txt(432, 92, "温度分水岭：为什么太阳由 pp 当家、巨星靠 CNO？", size=11.8, color=INK, weight="700"))

    # Chart area (x=414..720, y=108..336)
    el.append(card(414, 108, 306, 228, rx=8, fill=SLATE_SOFT, stroke=BORDER))
    gx0, gx1, gy0, gy1 = 462, 704, 300, 128  # T from 8 MK to 28 MK
    el.append(f'<line x1="{gx0}" y1="{gy0}" x2="{gx1}" y2="{gy0}" stroke="{SLATE}" stroke-width="1.4"/>')
    el.append(f'<line x1="{gx0}" y1="{gy1}" x2="{gx0}" y2="{gy0}" stroke="{SLATE}" stroke-width="1.4"/>')

    # Map T in [8, 28] MK; crossover at T_cross = 18.0 MK where log10(eps/eps_cross) = 0 -> y_cross = 204
    def tx(t_mk):
        return gx0 + (t_mk - 8.0) / 20.0 * (gx1 - gx0)

    def ty(log_rel):
        # log_rel in [-3.2, +2.8] mapped to [gy0, gy1]
        clamped = max(-3.2, min(2.8, log_rel))
        return gy0 - (clamped + 3.2) / 6.0 * (gy0 - gy1)

    pp_pts, cno_pts = [], []
    for i in range(41):
        t = 8.0 + i * 0.5
        log_pp = 4.0 * math.log10(t / 18.0)
        log_cno = 16.5 * math.log10(t / 18.0)
        pp_pts.append(f"{tx(t):.1f},{ty(log_pp):.1f}")
        if -3.2 <= log_cno <= 2.8:
            cno_pts.append(f"{tx(t):.1f},{ty(log_cno):.1f}")

    el.append(f'<polyline points="{" ".join(pp_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.8"/>')
    el.append(f'<polyline points="{" ".join(cno_pts)}" fill="none" stroke="{RED}" stroke-width="2.8" stroke-dasharray="6 3"/>')

    # Sun vertical marker at T = 15.7 MK
    sx = tx(15.7)
    sy_pp = ty(4.0 * math.log10(15.7 / 18.0))
    sy_cno = ty(16.5 * math.log10(15.7 / 18.0))
    el.append(f'<line x1="{sx:.1f}" y1="{gy1}" x2="{sx:.1f}" y2="{gy0}" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    el.append(f'<circle cx="{sx:.1f}" cy="{sy_pp:.1f}" r="5" fill="{ORANGE}"/>')
    el.append(f'<circle cx="{sx:.1f}" cy="{sy_cno:.1f}" r="4.5" fill="{RED}"/>')
    el.append(txt(sx - 6, 144, "太阳 15.7 MK", size=9.8, color=ORANGE, anchor="end", weight="700"))

    # Crossover marker at T = 18 MK
    cx_cross = tx(18.0)
    cy_cross = ty(0.0)
    el.append(f'<circle cx="{cx_cross:.1f}" cy="{cy_cross:.1f}" r="5" fill="{PURPLE}"/>')
    el.append(txt(cx_cross + 8, cy_cross + 14, "反超点 ≈ 18 MK", size=9.8, color=PURPLE, weight="700"))

    el.append(txt(648, 190, "pp 链 (∝ T⁴)", size=10.2, color=BLUE, weight="700"))
    el.append(txt(612, 144, "CNO (∝ T¹⁶~¹⁷)", size=10.2, color=RED, weight="700"))

    for t_tick in (10, 15, 20, 25):
        el.append(txt(tx(t_tick), 315, f"{t_tick}", size=9.6, color=MUTED, anchor="middle"))
    el.append(txt((gx0 + gx1) / 2, 330, "恒星核心温度 T（百万开尔文 MK）", size=9.8, color=BODY, anchor="middle", weight="600"))
    el.append(txt(438, 218, "对数产率", size=9.6, color=MUTED, anchor="middle"))

    el.append(txt(414, 360, "• 电荷门槛更高：碳氮原子核带 +6/+7 正电荷，库仑排斥墙比单质子", size=10.4, color=BODY))
    el.append(txt(424, 380, "高 6~7 倍！在太阳 1571 万 K 下，质子极难钻进碳氮核，仅占 ~1%。", size=10.4, color=BODY))
    el.append(txt(414, 404, "• 指数级狂飙：pp 产率平缓（∝ T⁴），CNO 对温度极敏感", size=10.3, color=PURPLE, weight="600"))
    el.append(txt(424, 424, "（∝ T¹⁶~¹⁷）！一旦超 ~1800 万 K（>1.3 M☉，如天狼星 A），", size=10.3, color=PURPLE, weight="600"))
    el.append(txt(424, 444, "CNO 立刻接管全星，猛烧燃料把恒星寿命缩短至几亿年！", size=10.3, color=INK, weight="600"))
    el.append(txt(414, 482, "（注：曲线按核天体物理对数相对产率关系 log₁₀ ε 绘制）", size=9.6, color=MUTED))

    return figure(
        522,
        "太阳碳氮氧（CNO）催化循环转盘与pp/CNO温度敏感度对比图",
        "左栏展示碳-12作为催化剂吞下4颗质子生成1颗氦-4并复原的六步CNO-I循环及2020年Borexino实验证实，右栏对数曲线对比pp链（正比于T的4次方）与CNO循环（正比于T的16至17次方）在约1800万K的产能反超分水岭。",
        el,
    )


def build_mass_defect_thermostat() -> str:
    """Diagram 4: Exact E=mc^2 mass defect ledger (4.26M tonnes/s) & hydrostatic negative-feedback thermostat."""
    _verify_solar_metrics()
    el = []
    el.extend(
        header(
            "每秒“凭空消失”426 万吨质量去哪了？爱因斯坦天平与太阳自动恒温器",
            "左栏给 4 颗氢核和 1 颗氦核精确过秤算清 0.71% 亏损 → 右栏看太阳稳烧 46 亿年不炸不灭的负反馈温控阀",
        )
    )

    # Left panel: E = mc^2 Precision Mass Ledger (x=24..380, y=68..504)
    el.append(card(24, 68, 356, 436, rx=10))
    el.append(step_badge(42, 88, "1", fg=ORANGE, bg=ORANGE_SOFT, r=10))
    el.append(txt(58, 92, "核聚变过秤单：4 颗氢比 1 颗氦重了 0.71%！", size=12.0, color=INK, weight="700"))

    # Balance scale visual (y=108..262)
    el.append(card(40, 108, 324, 152, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    # Tilted beam showing 4 x 1H heavier than 4He
    el.append(f'<polygon points="196,244 208,244 202,212" fill="{SLATE}"/>')
    el.append(f'<line x1="88" y1="222" x2="316" y2="198" stroke="{INK}" stroke-width="3"/>')
    # Left pan (lower = heavier)
    el.append(card(52, 154, 128, 62, rx=7, fill=CARD_BG, stroke=RED, sw=1.3))
    el.append(txt(116, 176, "聚变前：4 × ¹H 原子", size=10.6, color=RED, anchor="middle", weight="700"))
    el.append(txt(116, 198, "4.031300 u（更重！）", size=10.8, color=INK, anchor="middle", weight="700"))
    # Right pan (higher = lighter + E=mc^2 burst)
    el.append(card(224, 130, 128, 62, rx=7, fill=CARD_BG, stroke=GREEN, sw=1.3))
    el.append(txt(288, 152, "聚变后：1 × ⁴He 原子", size=10.6, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(288, 174, "4.002603 u（变轻！）", size=10.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(202, 253, "亏损质量 Δm = 0.028697 u（占 0.712%）→ 26.731 MeV!", size=10.3, color=AMBER, anchor="middle", weight="700"))

    # Macroscopic per-second ledger box (y=272..490)
    el.append(card(40, 272, 324, 216, rx=8, fill=CARD_BG, stroke=BORDER))
    el.append(pill(52, 282, "太阳每秒钟的宏观物质—能量总账单（NASA 实测）", fg=BLUE, bg=BLUE_SOFT, w=300, h=20, size=10.5))
    el.append(txt(52, 322, "• 每秒吞下氢燃料：≈ 6.00 亿吨（约 3.7 × 10³⁸ 颗质子）", size=10.6, color=BODY))
    el.append(txt(52, 345, "• 每秒炼出氦灰烬：≈ 5.9574 亿吨", size=10.6, color=BODY))
    el.append(txt(52, 369, "• 每秒彻底化作纯能量消失的质量 Δm = L☉ / c²：", size=10.6, color=INK, weight="600"))
    el.append(txt(64, 393, "426 万吨 / 秒！（≈ 每秒凭空蒸发 85 万头成年大象）", size=11.0, color=RED, weight="700"))
    el.append(txt(52, 418, "• 总辐射光度 L☉ = 3.828 × 10²⁶ W（相当于每秒同时引爆", size=10.5, color=BODY))
    el.append(txt(64, 438, "约 915 亿颗百万吨级氢弹！地球仅接住其中 22 亿分之一）", size=10.5, color=BODY))
    el.append(txt(52, 466, "• 别怕烧光：46 亿年加起来才瘦身 0.03% 太阳总质量！", size=10.5, color=GREEN, weight="700"))

    # Right panel: Gravitational Hydrostatic Thermostat (x=396..736, y=68..504)
    el.append(card(396, 68, 340, 436, rx=10))
    el.append(step_badge(414, 88, "2", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(430, 92, "天然防爆温控器：引力与热压的“负热容”太极", size=12.0, color=INK, weight="700"))

    el.append(txt(412, 118, "没有控制棒也没有安全壳，2500 亿大气压的太阳核心凭啥稳如钟表？", size=10.4, color=MUTED))

    # Branch A: Overheating self-brake (y=130..248)
    el.append(card(412, 130, 308, 116, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(pill(422, 138, "假如核聚变突然“烧猛了一点点”（自动踩刹车）", fg=BLUE, bg="#dbeafe", w=288, h=20, size=10.5))
    el.append(txt(422, 176, "产热 ↑ → 核心等离子体热压大于外层万有引力", size=10.5, color=BODY))
    el.append(txt(422, 198, "→ 核心向外轻微膨胀做功 → 密度 ρ ↓ 且温度 T ↓", size=10.5, color=BLUE, weight="700"))
    el.append(txt(422, 220, "→ 聚变速率对温度密度极敏感，立刻自动降回原位！", size=10.5, color=INK, weight="600"))

    # Branch B: Undercooling self-throttle (y=258..376)
    el.append(card(412, 258, 308, 116, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(pill(422, 266, "假如核聚变突然“偷懒弱了一点点”（自动补油门）", fg=GREEN, bg="#dcfce7", w=288, h=20, size=10.5))
    el.append(txt(422, 304, "产热 ↓ → 热压顶不住 33 万个地球质量的万有引力", size=10.5, color=BODY))
    el.append(txt(422, 326, "→ 核心向内轻微收缩挤压 → 密度 ρ ↑ 且温度 T ↑", size=10.5, color=GREEN, weight="700"))
    el.append(txt(422, 348, "→ 碰撞与隧穿频率回升，立刻把火力重新旺起来！", size=10.5, color=INK, weight="600"))

    # Long-term secular brightening note (y=388..490)
    el.append(card(412, 388, 308, 100, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(424, 410, "百亿年慢镜头：为什么太阳每隔 1 亿年变亮约 1%？", size=11.0, color=PURPLE, weight="700"))
    el.append(txt(424, 432, "• 4 颗氢核合 1 颗氦核，核心粒子总数减少 → 为顶住同等", size=10.3, color=BODY))
    el.append(txt(432, 452, "外层引力，核心必须缓慢收缩升温，倒逼聚变加快：如今", size=10.3, color=BODY))
    el.append(txt(432, 472, "太阳已比 46 亿年前刚诞生时亮了约 30%！", size=10.3, color=INK, weight="700"))

    return figure(
        518,
        "太阳核聚变质能亏损账单与引力静力平衡自动恒温器图解",
        "左栏精确对比4颗氢原子（4.031300 u）与1颗氦-4原子（4.002603 u）的0.712%质量亏损及太阳每秒消耗6亿吨氢、湮灭426万吨质量释放3.828×10²⁶ W功率的宏观账单，右栏图解引力与热压负反馈稳住核聚变及太阳每亿年增亮1%的演化机制。",
        el,
    )


def build_neutrino_vs_photon_escape() -> str:
    """Diagram 5: 2.3-second straight-line neutrino escape (and oscillation) vs 170,000-year photon random walk."""
    el = []
    el.extend(
        header(
            "同在太阳中心诞生：为什么中微子 8 分钟到地球，光子却要迷路十万年？",
            "上路看视十倍铅密度如空气的“幽灵中微子”穿墙直飞 → 下路看伽马光子在辐射区碰撞百亿亿次的“醉汉漫步”",
        )
    )

    # Main cross-section canvas (x=24..736, y=68..362)
    el.append(card(24, 68, 712, 294, rx=10, fill="#0f172a", stroke=SLATE, sw=1.4))

    # Concentric solar zones centered at (cx=128, cy=215)
    # Core r=68, Radiative r=182, Convective r=246; Photosphere arc around x=374
    el.append('<clipPath id="sun-clip"><rect x="26" y="70" width="708" height="290" rx="9"/></clipPath>')
    el.append(
        f"""<g clip-path="url(#sun-clip)">
  <circle cx="128" cy="215" r="248" fill="#ea580c" opacity="0.92"/>
  <circle cx="128" cy="215" r="184" fill="#f59e0b" opacity="0.95"/>
  <circle cx="128" cy="215" r="72" fill="#fef08a"/>
</g>"""
    )

    # Zone labels inside solar slice
    el.append(txt(128, 208, "核聚变核心", size=11.0, color=INK, anchor="middle", weight="700"))
    el.append(txt(128, 226, "0~0.24 R☉", size=9.8, color=AMBER, anchor="middle", weight="700"))
    el.append(txt(128, 243, "162 g/cm³", size=9.6, color=INK, anchor="middle", weight="600"))

    el.append(txt(250, 298, "辐射区（0.24~0.71 R☉）", size=10.4, color="#fffbeb", anchor="middle", weight="700"))
    el.append(txt(250, 315, "自由电子密布如铜墙铁壁", size=9.6, color="#fef3c7", anchor="middle"))

    el.append(txt(342, 336, "对流区 → 光球层 5772 K", size=10.0, color="#ffedd5", anchor="middle", weight="700"))

    # Earth on right (cx=674, cy=215)
    el.append(f'<circle cx="674" cy="215" r="24" fill="#2563eb" stroke="#93c5fd" stroke-width="2"/>')
    el.append(txt(674, 219, "地球", size=10.8, color="#ffffff", anchor="middle", weight="700"))
    el.append(txt(674, 256, "1.5 亿公里", size=9.8, color="#cbd5e1", anchor="middle"))

    # Upper track: Neutrino straight-line escape (y=138)
    el.append(f'<line x1="154" y1="138" x2="644" y2="138" stroke="#38bdf8" stroke-width="2.8" stroke-dasharray="8 4" marker-end="url(#arr-blue)"/>')
    el.append(card(392, 84, 326, 44, rx=7, fill="#1e293b", stroke="#38bdf8", sw=1.1))
    el.append(txt(555, 103, "① 电子中微子 νₑ：只受弱力，2.3 秒直穿太阳，8分20秒抵地球！", size=10.2, color="#7dd3fc", anchor="middle", weight="700"))
    el.append(txt(555, 121, "每秒约 650 亿颗穿过你指甲盖 · 途中三味振荡变脸（νₑ↔ν_μ↔ν_τ）", size=9.6, color="#e2e8f0", anchor="middle"))

    # Lower track: Photon jagged 3D random walk inside radiative zone, then straight visible light to Earth
    jag_pts = [
        (164, 224), (178, 198), (170, 236), (194, 206), (188, 248),
        (212, 212), (206, 254), (232, 202), (228, 246), (254, 196),
        (248, 242), (276, 206), (272, 248), (298, 214), (318, 232),
        (344, 208), (376, 224),
    ]
    poly_jag = " ".join(f"{px},{py}" for px, py in jag_pts)
    el.append(f'<polyline points="{poly_jag}" fill="none" stroke="#ffffff" stroke-width="2.2"/>')
    el.append(f'<line x1="376" y1="224" x2="644" y2="224" stroke="#fde047" stroke-width="2.8" marker-end="url(#arr-orange)"/>')

    el.append(card(392, 272, 326, 74, rx=7, fill="#1e293b", stroke="#fde047", sw=1.1))
    el.append(txt(555, 292, "② 伽马光子 γ：每飞 < 1 厘米就撞电子转向，迷路 1 万~17 万年！", size=10.2, color="#fde047", anchor="middle", weight="700"))
    el.append(txt(555, 311, "经历 ~10²¹ 次散射层层降级：1 颗致命 MeV 伽马光子裂变成几百万颗", size=9.6, color="#e2e8f0", anchor="middle"))
    el.append(txt(555, 330, "5772 K 温柔可见光，出太阳表面后再用 8 分 20 秒洒在你肩头！", size=9.6, color="#fef08a", anchor="middle", weight="600"))

    # Bottom two insight cards: Random-walk math & Solar Neutrino Problem Nobel story (y=374..512)
    el.append(card(24, 374, 348, 138, rx=10))
    el.append(step_badge(42, 394, "1", fg=ORANGE, bg=ORANGE_SOFT, r=10))
    el.append(txt(58, 398, "为什么光走 70 万公里要花十几万年？（醉汉漫步）", size=11.6, color=INK, weight="700"))
    el.append(txt(40, 424, "• 若直线飞出半径 R☉ ≈ 70 万公里，光速只需 R☉/c ≈ 2.3 秒；", size=10.5, color=BODY))
    el.append(txt(40, 445, "• 但在辐射区每步自由程 ℓ 仅毫米级，随机散射走远距离按", size=10.5, color=BODY))
    el.append(txt(48, 466, "步数平方根推进：总步数 N ≈ (R/ℓ)² ≈ 10²¹ 步！", size=10.6, color=ORANGE, weight="700"))
    el.append(txt(40, 489, "• 今天晒暖你的阳光，其实在冰河期旧石器时代就已在核心点燃！", size=10.4, color=INK, weight="600"))

    el.append(card(388, 374, 348, 138, rx=10))
    el.append(step_badge(406, 394, "2", fg=BLUE, bg=BLUE_SOFT, r=10))
    el.append(txt(422, 398, "两夺诺奖悬案：如果太阳今晚熄火，谁先报信？", size=11.6, color=INK, weight="700"))
    el.append(txt(404, 424, "• 光照会靠十万年存货继续亮很久，但中微子 8 分钟就会断流！", size=10.5, color=BLUE, weight="600"))
    el.append(txt(404, 445, "• 1968 年戴维斯用 600 吨干洗剂只抓到理论 1/3 的太阳中微子，", size=10.5, color=BODY))
    el.append(txt(412, 466, "一度让人怀疑太阳停火了！直到 SNO 与超级神冈证实 2/3 在", size=10.5, color=BODY))
    el.append(txt(412, 489, "半路变身成了 μ/τ 中微子，完美印证标准太阳核聚变模型！", size=10.4, color=INK, weight="600"))

    return figure(
        524,
        "太阳核心中微子8分钟直飞逃逸与伽马光子十万年随机漫步对比图",
        "剖面展示太阳核心、辐射区、对流区至地球的两条信使路径：电子中微子2.3秒穿出太阳、8分20秒抵地球并发生三味振荡；伽马光子在辐射区经历约10的21次方次散射随机漫步耗时1万至17万年降级为5772K可见光。",
        el,
    )


@register("solar-fusion", "太阳核聚变全过程科学图解", "physics")
def build_all() -> list[str]:
    _verify_solar_metrics()
    specs = [
        ("coulomb-tunneling-and-weak-lock.svg", build_coulomb_tunneling_weak_lock()),
        ("pp-chain-three-steps-anim.svg", build_pp_chain_anim()),
        ("cno-catalytic-wheel-vs-pp.svg", build_cno_wheel_vs_pp()),
        ("mass-defect-and-thermostat.svg", build_mass_defect_thermostat()),
        ("neutrino-8min-vs-photon-170kyr.svg", build_neutrino_vs_photon_escape()),
    ]
    written = []
    for fname, svg_text in specs:
        write_svg(SUBDIR, fname, svg_text)
        written.append(f"assets/images/{SUBDIR}/{fname}")
    return written
