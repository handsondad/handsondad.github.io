"""Original SVG diagrams for automotive fuel tank negative pressure (EVAP) and gasoline octane grades."""

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

SUBDIR = "fuel-tank-gasoline"

RED = "#dc2626"
RED_SOFT = "#fef2f2"
RED_BORDER = "#fca5a5"
AMBER = "#b45309"
AMBER_SOFT = "#fef3c7"
TEAL = "#0f766e"
TEAL_SOFT = "#ccfbf1"


def _verify_fuel_metrics():
    """Verify pressure unit conversions, crushing forces, and RON/MON/AKI formulas."""
    # 1 in.-H2O = 0.249089 kPa; 1 psi = 6.89476 kPa; 1 in.-Hg = 3.38639 kPa
    kpa_per_inh2o = 0.249089
    purge_vac_min = -2.0 * kpa_per_inh2o  # ~ -0.50 kPa
    purge_vac_max = -4.0 * kpa_per_inh2o  # ~ -1.00 kPa
    leak_test_vac = -8.0 * kpa_per_inh2o  # ~ -1.99 kPa
    cap_pos_kpa = 1.5 * 6.89476           # ~ +10.34 kPa
    cap_neg_kpa = -1.5 * 3.38639          # ~ -5.08 kPa
    assert -0.55 < purge_vac_min < -0.45
    assert -1.05 < purge_vac_max < -0.95
    assert -2.05 < leak_test_vac < -1.90
    assert 10.2 < cap_pos_kpa < 10.5
    assert -5.2 < cap_neg_kpa < -5.0

    # Crushing force on 0.6 m^2 tank area at -50 kPa manifold vacuum
    force_n = 50_000 * 0.6
    force_tons = force_n / 9806.65
    assert force_n == 30_000
    assert abs(force_tons - 3.059) < 0.02

    # AKI = (RON + MON) / 2
    assert (92 + 82) / 2 == 87.0
    assert (95 + 85) / 2 == 90.0
    assert (98 + 88) / 2 == 93.0


def build_evap_loop_anim() -> str:
    """1-shot CSS animation of EVAP vapor capture, intake purge slight vacuum, and OBD leak test."""
    _verify_fuel_metrics()
    extra_css = """
  @keyframes evFade {
    0% { opacity: 0.16; transform: translateY(4px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  @keyframes flowDash {
    from { stroke-dashoffset: 36; }
    to { stroke-dashoffset: 0; }
  }
  .ev-1 { opacity: 0.16; animation: evFade 0.85s ease-out 0.15s forwards; }
  .ev-2 { opacity: 0.16; animation: evFade 0.85s ease-out 1.75s forwards; }
  .ev-3 { opacity: 0.16; animation: evFade 0.90s ease-out 3.45s forwards; }
  .purge-line { stroke-dasharray: 7 5; animation: flowDash 1.6s linear 1.8s 2 forwards; }
  @media (prefers-reduced-motion: reduce) {
    .ev-1, .ev-2, .ev-3 {
      animation: none !important;
      opacity: 1 !important;
      transform: none !important;
    }
    .purge-line {
      animation: none !important;
    }
  }"""

    el = []
    el.extend(
        header(
            "汽车油箱为什么会“自己吸气”？读懂 EVAP 活性炭罐回路与健康微负压",
            "先看熄火/加油怎样锁住汽油蒸气 → 再看开车时进气歧管怎样抽洗碳罐形成微负压 → 下排看双向安全阀兜底",
        )
    )

    # Lane 1: Refueling / Hot Parking Vapor Capture (y=66..196, h=130)
    el.append(
        f"""<g class="ev-1">
  {card(24, 66, 712, 130, rx=10, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.2)}
  {step_badge(42, 86, "1", fg=ORANGE, bg=CARD_BG, r=10)}
  {txt(58, 90, "工况 ① 熄火暴晒与加油瞬间（ORVR）：密闭油箱不准直接排空，全靠活性炭罐“吃掉”油气", size=12.2, color=INK, weight="700")}

  {card(40, 104, 186, 60, rx=8, fill=CARD_BG, stroke=ORANGE)}
  {txt(133, 127, "密闭燃油箱（汽油易挥发）", size=11.4, color=ORANGE, anchor="middle", weight="700")}
  {txt(133, 148, "RVP 蒸气压 45~88 kPa", size=10.6, color=MUTED, anchor="middle")}

  <line x1="230" y1="134" x2="282" y2="134" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>
  {txt(256, 124, "油气上浮", size=10.2, color=ORANGE, anchor="middle", weight="700")}

  {card(286, 104, 206, 60, rx=8, fill=CARD_BG, stroke=TEAL)}
  {txt(389, 127, "活性炭罐（多孔炭床吸附）", size=11.4, color=TEAL, anchor="middle", weight="700")}
  {txt(389, 148, "扣留 HC 油气 · 电磁阀 CPS 关闭", size=10.6, color=BODY, anchor="middle")}

  <line x1="496" y1="134" x2="544" y2="134" stroke="{GREEN}" stroke-width="2" marker-end="url(#arr-green)"/>
  {txt(520, 124, "CVS常开", size=10.2, color=GREEN, anchor="middle", weight="700")}

  {card(548, 104, 172, 60, rx=8, fill=CARD_BG, stroke=GREEN)}
  {txt(634, 127, "脱油干净空气排入大气", size=11.2, color=GREEN, anchor="middle", weight="700")}
  {txt(634, 148, "拦截 98% 以上加油挥发烃", size=10.4, color=MUTED, anchor="middle")}

  {txt(40, 182, "• 为什么现代油箱必须全密封？早期敞口油箱挥发的碳氢化合物占整车污染约 20%，还会引发臭氧光化学烟雾。", size=10.8, color=BODY)}
</g>"""
    )

    # Lane 2: Engine Running Purge & Normal Slight Negative Pressure (y=208..354, h=146)
    el.append(
        f"""<g class="ev-2">
  {card(24, 208, 712, 146, rx=10, fill=BLUE_SOFT, stroke=BLUE, sw=1.3)}
  {step_badge(42, 228, "2", fg=BLUE, bg=CARD_BG, r=10)}
  {txt(58, 232, "工况 ② 热车巡航“脱附抽吸”：油泵抽油 + 进气歧管真空洗炭床 = 健康微负压（-0.5 ~ -1.0 kPa）", size=12.1, color=INK, weight="700")}

  {card(40, 248, 168, 62, rx=8, fill=CARD_BG, stroke=GREEN)}
  {txt(124, 271, "大气新鲜空气吸入", size=11.4, color=GREEN, anchor="middle", weight="700")}
  {txt(124, 292, "经 CVS 通风阀滤网补气", size=10.5, color=MUTED, anchor="middle")}

  <line x1="212" y1="279" x2="254" y2="279" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>

  {card(258, 248, 214, 62, rx=8, fill=CARD_BG, stroke=BLUE)}
  {txt(365, 271, "反吹洗脱炭罐 + 平衡油箱体积", size=11.3, color=BLUE, anchor="middle", weight="700")}
  {txt(365, 292, "油箱保持 -2~-4 in.-H₂O 微负压", size=10.6, color=INK, anchor="middle", weight="600")}

  <line class="purge-line" x1="476" y1="279" x2="532" y2="279" stroke="{BLUE}" stroke-width="2.6" marker-end="url(#arr-blue)"/>
  {txt(504, 268, "CPS打开", size=10.2, color=BLUE, anchor="middle", weight="700")}

  {card(536, 248, 184, 62, rx=8, fill=CARD_BG, stroke=PURPLE)}
  {txt(628, 271, "发动机进气歧管强真空", size=11.3, color=PURPLE, anchor="middle", weight="700")}
  {txt(628, 292, "负压高达 -40~-70 kPa 抽吸烧掉", size=10.4, color=BODY, anchor="middle")}

  {txt(40, 326, "• 两大微负压来源：① 油泵不断抽走液态汽油腾出空间；② 新鲜空气穿过碳罐滤网与炭粒存在轻微流阻。", size=10.8, color=BODY)}
  {txt(40, 344, "• 好处：只要油箱维持一丁点微负压，哪怕管路有微米级缝隙也是空气往里吸，绝不会让易燃汽油蒸气往外漏！", size=10.8, color=BLUE, weight="600")}
</g>"""
    )

    # Lane 3: OBD-II Leak Self-Check & Gas Cap Two-Way Valve (y=366..516, h=150)
    el.append(
        f"""<g class="ev-3">
  {card(24, 366, 712, 150, rx=10, fill=SLATE_SOFT, stroke=BORDER, sw=1.2)}
  {step_badge(42, 386, "3", fg=PURPLE, bg=PURPLE_SOFT, r=10)}
  {txt(58, 390, "工况 ③ 电脑主动抽真空检漏与油箱盖“双向保命弹簧阀”：三重防线护住油箱", size=12.2, color=INK, weight="700")}

  {card(40, 404, 218, 98, rx=8, fill=CARD_BG, stroke=PURPLE)}
  {pill(52, 412, "OBD-II 主动真空检漏", fg=PURPLE, bg=PURPLE_SOFT, w=194, h=20, size=10.8)}
  {txt(52, 450, "• 电脑短暂关死 CVS + 打开 CPS", size=10.8, color=BODY)}
  {txt(52, 470, "• 抽至约 -1.7~-2.0 kPa 保压30秒", size=10.8, color=PURPLE, weight="600")}
  {txt(52, 490, "• 连 0.5 mm 针孔没拧紧盖都能报警", size=10.5, color=MUTED)}

  {card(271, 404, 218, 98, rx=8, fill=CARD_BG, stroke=TEAL)}
  {pill(283, 412, "熄火降温自然微负压 NVLD", fg=TEAL, bg=TEAL_SOFT, w=194, h=20, size=10.8)}
  {txt(283, 450, "• 热车停放过夜，油气冷却收缩", size=10.8, color=BODY)}
  {txt(283, 470, "• 按理想气体 P∝T 自然生出微真空", size=10.8, color=TEAL, weight="600")}
  {txt(283, 490, "• 清晨拧盖听到轻响 1 秒属完全正常", size=10.5, color=MUTED)}

  {card(502, 404, 218, 98, rx=8, fill=CARD_BG, stroke=RED)}
  {pill(514, 412, "油箱盖机械双向限压阀", fg=RED, bg=RED_SOFT, w=194, h=20, size=10.8)}
  {txt(514, 450, "• 超正压 > +10.3 kPa：向外泄压防鼓", size=10.8, color=BODY)}
  {txt(514, 470, "• 超负压 < -5.1 kPa：向内吸气防瘪", size=10.8, color=RED, weight="700")}
  {txt(514, 490, "• 万一碳罐堵死时的最后一道救命门", size=10.5, color=MUTED)}
</g>"""
    )

    return figure(
        530,
        "汽车油箱EVAP活性炭罐呼吸回路与负压形成原理动画",
        "分步展示汽车熄火与加油时活性炭罐吸附汽油蒸气、行驶时进气歧管抽洗碳罐形成健康微负压，以及OBD-II闭环真空检漏和油箱盖双向安全限压阀的工作原理。",
        el,
        extra_css=extra_css,
    )


def build_healthy_vs_crushed_tank() -> str:
    """Contrast normal slight hiss vs pathological strong negative pressure crushing a fuel tank."""
    _verify_fuel_metrics()
    el = []
    el.extend(
        header(
            "拧油箱盖一声“嗤”到底用不用修？分清健康呼吸与“三吨大气铁掌”吸瘪油箱",
            "左栏看无需担心的两种一秒轻响 → 右栏看加油跳枪强行凑整怎样淹死碳罐、把油箱生生吸扁",
        )
    )

    # Left card: Healthy slight pressure/vacuum (x=24..368, y=68..356)
    el.append(card(24, 68, 344, 288, rx=10, stroke=GREEN, sw=1.3))
    el.append(step_badge(42, 88, "1", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(58, 92, "完全正常：拧盖轻响 1 秒即停（±5 kPa 内）", size=12.4, color=INK, weight="700"))

    el.append(card(40, 108, 312, 104, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1))
    el.append(txt(52, 129, "场景 A：夏天暴晒或跑完长途 → 轻微向外“噗”一声", size=11.3, color=GREEN, weight="700"))
    el.append(txt(52, 151, "• 原因：路面烘烤 + 回油升温令汽油挥发膨胀（微正压）", size=10.8, color=BODY))
    el.append(txt(52, 171, "• 说明：正好证明你的油箱密封圈与 EVAP 管路严丝合缝！", size=10.8, color=INK, weight="600"))
    el.append(txt(52, 191, "  （若一点气都不存、还飘汽油味，反而可能是胶圈老化漏气）", size=10.3, color=MUTED))

    el.append(card(40, 224, 312, 116, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1))
    el.append(txt(52, 245, "场景 B：清晨冷车或刚熄火加油 → 轻微向内吸气声", size=11.3, color=BLUE, weight="700"))
    el.append(txt(52, 267, "• 原因：夜间油气冷却收缩（NVLD）或刚完成碳罐负压脱附", size=10.8, color=BODY))
    el.append(txt(52, 287, "• 判据：油箱盖轻松拧动、吸气声短促柔和、动力怠速平稳、", size=10.8, color=BODY))
    el.append(txt(52, 307, "  油表准确无故障灯——属于健康工作态，完全不用修！", size=10.8, color=BLUE, weight="700"))

    # Right card: Pathological excessive vacuum (x=384..736, y=68..356)
    el.append(card(384, 68, 352, 288, rx=10, stroke=RED, sw=1.4))
    el.append(step_badge(402, 88, "2", fg=RED, bg=RED_SOFT, r=10))
    el.append(txt(418, 92, "故障警报：异常强负压（P1450）四大症状与真凶", size=12.4, color=RED, weight="700"))

    el.append(card(400, 108, 320, 104, rx=8, fill=RED_SOFT, stroke=RED_BORDER, sw=1))
    el.append(txt(412, 129, "危险信号（中一条以上立即排查碳罐与电磁阀！）：", size=11.3, color=RED, weight="700"))
    el.append(txt(412, 151, "① 油箱盖被死死吸住极难拧动，拧开持续数秒尖锐倒吸风声", size=10.7, color=BODY))
    el.append(txt(412, 171, "② 热车跑高速突然加速无力、耸车甚至熄火（油泵抢不过真空）", size=10.7, color=BODY))
    el.append(txt(412, 191, "③ 油箱底部肉眼可见内凹变形，油浮子被顶歪导致油表乱跳", size=10.7, color=INK, weight="600"))

    el.append(card(400, 224, 320, 116, rx=8, fill=AMBER_SOFT, stroke=ORANGE, sw=1))
    el.append(txt(412, 245, "两大罪魁祸首（“只抽不补”死局）：", size=11.3, color=AMBER, weight="700"))
    el.append(txt(412, 267, "• 元凶① 碳罐呼吸口堵死：加油“跳枪后硬凑整”让液态汽油", size=10.7, color=BODY))
    el.append(txt(422, 286, "顺通风管灌进碳罐，活性炭泡油结块 + 泥沙糊死大气滤网！", size=10.7, color=RED, weight="600"))
    el.append(txt(412, 306, "• 元凶② 碳罐电磁阀（CPS）卡滞常开：发动机进气歧管", size=10.7, color=BODY))
    el.append(txt(422, 325, "-50 kPa 强真空直接连通密闭油箱，不停顿死命狂抽！", size=10.7, color=INK, weight="600"))

    # Bottom quantitative physics strip: Atmospheric crushing calculation (x=24..736, y=370..506)
    el.append(card(24, 370, 712, 136, rx=10, fill=CARD_BG, stroke=PURPLE, sw=1.2))
    el.append(txt(40, 393, "物理算账：为什么区区半个大气压的负压，能把坚固的钢制或工程塑料（HDPE）油箱压扁？", size=12.3, color=INK, weight="700"))

    # Crushed tank visual on left (x=42..292, y=404..492)
    el.append(card(42, 404, 250, 88, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    # Deformed inward tank silhouette + external atmospheric arrows
    el.append(
        f"""<path d="M 88,426 Q 167,444 246,426 L 252,472 Q 167,454 82,472 Z" fill="#fee2e2" stroke="{RED}" stroke-width="2.4"/>
{txt(167, 453, "油箱内被抽至 51.3 kPa", size=10.4, color=RED, anchor="middle", weight="700")}
<line x1="126" y1="410" x2="126" y2="429" stroke="{PURPLE}" stroke-width="2" marker-end="url(#arr-blue)"/>
<line x1="208" y1="410" x2="208" y2="429" stroke="{PURPLE}" stroke-width="2" marker-end="url(#arr-blue)"/>
<line x1="126" y1="488" x2="126" y2="469" stroke="{PURPLE}" stroke-width="2" marker-end="url(#arr-blue)"/>
<line x1="208" y1="488" x2="208" y2="469" stroke="{PURPLE}" stroke-width="2" marker-end="url(#arr-blue)"/>
{txt(167, 486, "外部大气压 101.3 kPa 四面猛压", size=10.2, color=PURPLE, anchor="middle", weight="700")}"""
    )

    el.append(txt(310, 424, "• 压差计算：外部标准大气压 101.3 kPa，若歧管抽成 -50 kPa 负压，", size=11.2, color=BODY))
    el.append(txt(320, 446, "油箱壁内外压差 ΔP = 50,000 Pa（每平方米承受 5 吨压力！）。", size=11.2, color=INK, weight="700"))
    el.append(txt(310, 469, "• 以典型 60 L 扁平油箱单侧受压面积 A ≈ 0.6 m² 计算：", size=11.2, color=BODY))
    el.append(txt(320, 491, "总挤压力 F = ΔP × A = 30,000 N ≈ 3.06 吨 —— 等于两辆轿车直接踩在油箱上！", size=11.2, color=RED, weight="700"))

    return figure(
        520,
        "汽车油箱正常微压与异常强负压吸瘪油箱机理对比图",
        "对比正常微正压/微负压与碳罐堵塞及电磁阀常开引发的强负压故障症状，并定量计算-50 kPa负压在0.6平方米油箱表面产生的约3.06吨大气压差挤压力。",
        el,
    )


def build_octane_ruler_diagram() -> str:
    """Molecular basis of octane number (isooctane=100 vs n-heptane=0) & China RON vs US AKI conversion."""
    _verify_fuel_metrics()
    el = []
    el.extend(
        header(
            "92、95、98 号到底在给什么打分？一把“异辛烷 vs 正庚烷”的抗爆震标尺",
            "先看左栏 0 分直链正庚烷与 100 分支链异辛烷的分子骨架 → 再看右栏中外加油站标号为什么差 5 分",
        )
    )

    # Left panel: 0 vs 100 Reference Hydrocarbons (x=24..376, y=66..358)
    el.append(card(24, 66, 352, 292, rx=10))
    el.append(step_badge(42, 86, "1", fg=BLUE, bg=BLUE_SOFT, r=10))
    el.append(txt(58, 90, "辛烷值标尺：不是“纯度”，而是“抗自燃定力”！", size=12.4, color=INK, weight="700"))

    # n-Heptane = 0 box (y=104..194)
    el.append(card(38, 104, 324, 90, rx=8, fill=RED_SOFT, stroke=RED_BORDER, sw=1))
    el.append(pill(48, 112, "0 分学渣基准：正庚烷 n-C₇H₁₆（RON = 0）", fg=RED, bg="#fee2e2", w=264, h=20, size=10.8))
    # Zigzag 7-carbon chain
    pts_c7 = [(56 + i * 22, 156 if i % 2 == 0 else 144) for i in range(7)]
    poly_c7 = " ".join(f"{px},{py}" for px, py in pts_c7)
    dots_c7 = "".join(f'<circle cx="{px}" cy="{py}" r="4.5" fill="{RED}"/>' for px, py in pts_c7)
    el.append(f'<polyline points="{poly_c7}" fill="none" stroke="{RED}" stroke-width="2.8"/>{dots_c7}')
    el.append(txt(206, 152, "细长无支链 → 高温高压下极易", size=10.8, color=BODY))
    el.append(txt(206, 171, "断裂生过氧化物，一挤就暴躁自燃！", size=10.8, color=RED, weight="700"))
    el.append(txt(48, 187, "（正辛烷更惨：RON = -20！碳链越直越长，汽油机越容易敲缸）", size=10.1, color=MUTED))

    # Iso-octane = 100 box (y=204..304)
    el.append(card(38, 204, 324, 100, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.1))
    el.append(pill(48, 212, "100 分学霸基准：异辛烷 2,2,4-三甲基戊烷（RON = 100）", fg=GREEN, bg="#dcfce7", w=304, h=20, size=10.6))
    # Branched 5-carbon backbone + 3 methyl branches
    pts_c5 = [(60 + i * 24, 262 if i % 2 == 0 else 252) for i in range(5)]
    poly_c5 = " ".join(f"{px},{py}" for px, py in pts_c5)
    c2x, c2y = pts_c5[1]
    c4x, c4y = pts_c5[3]
    el.append(
        f"""<polyline points="{poly_c5}" fill="none" stroke="{GREEN}" stroke-width="2.8"/>
<line x1="{c2x}" y1="{c2y}" x2="{c2x - 8}" y2="{c2y - 16}" stroke="{GREEN}" stroke-width="2.5"/>
<line x1="{c2x}" y1="{c2y}" x2="{c2x + 8}" y2="{c2y + 18}" stroke="{GREEN}" stroke-width="2.5"/>
<line x1="{c4x}" y1="{c4y}" x2="{c4x}" y2="{c4y - 17}" stroke="{GREEN}" stroke-width="2.5"/>
{"".join(f'<circle cx="{px}" cy="{py}" r="4.5" fill="{GREEN}"/>' for px, py in pts_c5)}
<circle cx="{c2x - 8}" cy="{c2y - 16}" r="4.2" fill="{BLUE}"/>
<circle cx="{c2x + 8}" cy="{c2y + 18}" r="4.2" fill="{BLUE}"/>
<circle cx="{c4x}" cy="{c4y - 17}" r="4.2" fill="{BLUE}"/>"""
    )
    el.append(txt(182, 255, "紧凑多支链抱团 → 自由基极难链式", size=10.8, color=BODY))
    el.append(txt(182, 274, "蔓延，高压下稳如泰山，乖乖等火花！", size=10.8, color=GREEN, weight="700"))
    el.append(txt(48, 296, "定义：92 号汽油 = 抗爆定力等同于“92% 异辛烷 + 8% 正庚烷”标准液", size=10.3, color=INK, weight="600"))

    el.append(txt(38, 326, "• 真相：现代商品汽油并非真拿异辛烷兑正庚烷，而是由上百种 C₄~C₁₂", size=10.6, color=BODY))
    el.append(txt(38, 345, "  异构烷烃、环烷烃、芳烃及含氧抗爆剂（如乙醇 RON≈108.6）调合而成。", size=10.6, color=BODY))

    # Right panel: RON vs MON vs AKI Global Pump Translation (x=392..736, y=66..358)
    el.append(card(392, 66, 344, 292, rx=10))
    el.append(step_badge(410, 86, "2", fg=PURPLE, bg=PURPLE_SOFT, r=10))
    el.append(txt(426, 90, "出国自驾别加错：为什么美国最高才标 93 号？", size=12.2, color=INK, weight="700"))

    el.append(txt(406, 115, "• 研究法 RON（中/欧标准）：600 rpm 温和进气，模拟市区加速", size=10.7, color=BLUE, weight="600"))
    el.append(txt(406, 135, "• 马达法 MON（严苛测试）：900 rpm 预热进气，同款油低 8~12 分", size=10.7, color=ORANGE, weight="600"))
    el.append(txt(406, 155, "• 美加抗爆指数 AKI = (RON + MON) ÷ 2 → 数字天生低 4~5 分！", size=10.7, color=PURPLE, weight="700"))

    # Equivalence table cards (y=170..312)
    eq_rows = [
        ("中国 89#", "RON ≥ 89", "老款低压缩比机 / 农机", SLATE, SLATE_SOFT),
        ("中国 92#", "RON 92 / MON≈82", "≈ 美国 Regular 87", BLUE, BLUE_SOFT),
        ("中国 95#", "RON 95 / MON≈85", "≈ 美国 Mid 89~90 / 欧 95", GREEN, GREEN_SOFT),
        ("中国 98#", "RON 98 / MON≈88", "≈ 美国 Premium 93 / 欧 98", PURPLE, PURPLE_SOFT),
    ]
    for idx, (cn_g, rm_s, intl_s, fg_c, bg_c) in enumerate(eq_rows):
        ry = 170 + idx * 36
        el.append(card(406, ry, 316, 30, rx=6, fill=bg_c, stroke=fg_c, sw=1))
        el.append(txt(416, ry + 19, cn_g, size=11.2, color=fg_c, weight="700"))
        el.append(txt(486, ry + 19, rm_s, size=10.4, color=BODY, weight="600"))
        el.append(txt(606, ry + 19, intl_s, size=10.4, color=INK, weight="700"))

    el.append(txt(406, 332, "• 超过 100 分存在吗？完全存在！德国 Aral 102、赛车汽油、", size=10.5, color=BODY))
    el.append(txt(406, 349, "  航空活塞油及纯乙醇（RON 108.6）抗爆性都比纯异辛烷更强。", size=10.5, color=MUTED))

    # Bottom contrast strip: Gasoline Octane vs Diesel Cetane (x=24..736, y=372..502)
    el.append(card(24, 372, 712, 130, rx=10, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(40, 395, "顺手打通任督二脉：为什么汽油怕“提前自燃”，柴油（0# / -10# / -35#）标号却完全是另一套逻辑？", size=12.1, color=INK, weight="700"))

    el.append(card(40, 408, 332, 82, rx=8, fill=CARD_BG, stroke=BLUE))
    el.append(txt(52, 429, "汽油机（火花塞点燃）：追求“沉得住气”的高辛烷值", size=11.2, color=BLUE, weight="700"))
    el.append(txt(52, 450, "• 先把油气混合好再一起压缩，绝不许在火花塞点火前自燃", size=10.7, color=BODY))
    el.append(txt(52, 470, "• 92 / 95 / 98 全代表抗爆震辛烷值（RON），跟结冰温度无关！", size=10.7, color=INK, weight="600"))

    el.append(card(388, 408, 332, 82, rx=8, fill=CARD_BG, stroke=ORANGE))
    el.append(txt(400, 429, "柴油机（压燃无火花塞）：标号代表“凝点温度”！", size=11.2, color=ORANGE, weight="700"))
    el.append(txt(400, 450, "• 先把纯空气压到滚烫再喷柴油，越容易自燃越好（高十六烷值）", size=10.7, color=BODY))
    el.append(txt(400, 470, "• 0#、-10#、-35# 柴油代表抗结蜡凝点（℃），冬天选错真会冻住！", size=10.7, color=RED, weight="600"))

    return figure(
        516,
        "汽油辛烷值分子标尺与中外标号换算及汽柴油逻辑对比图",
        "展示0分正庚烷直链与100分异辛烷多支链分子结构差异、中国RON研究法标号（89/92/95/98）与北美AKI标号（87/89/93）的换算关系，以及汽油抗爆标号与柴油凝点标号的本质区别。",
        el,
    )


def build_normal_vs_knock_combustion() -> str:
    """Compare smooth 20-40 m/s deflagration flame front vs >1000 m/s end-gas detonation knock."""
    el = []
    el.extend(
        header(
            "气缸里的 3 毫秒生死战：柔顺推活塞 vs 超音速“爆震敲缸”怎样砸穿发动机？",
            "先对比左缸正常火焰推进与右缸末端混合气自燃对撞 → 下排看现代 ECU 推迟点火救命的油耗代价",
        )
    )

    # Left panel: Normal Combustion (x=24..372, y=68..372)
    el.append(card(24, 68, 348, 304, rx=10, stroke=GREEN, sw=1.3))
    el.append(step_badge(42, 88, "1", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(58, 92, "正常受控燃烧（标号匹配）：单核火焰柔顺推进", size=12.3, color=INK, weight="700"))

    # Cylinder schematic (x=42..354, y=108..264)
    el.append(card(42, 108, 312, 156, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    el.append(
        f"""<rect x="118" y="122" width="160" height="128" rx="6" fill="#ffffff" stroke="{SLATE}" stroke-width="2.5"/>
<rect x="193" y="110" width="10" height="16" rx="2" fill="{INK}"/>
<polygon points="198,126 193,136 200,136 196,145" fill="{ORANGE}"/>
<path d="M 156,126 Q 198,168 240,126" fill="none" stroke="{BLUE}" stroke-width="2.2" stroke-dasharray="5 3"/>
<path d="M 132,140 Q 198,200 264,140" fill="none" stroke="{GREEN}" stroke-width="2.8"/>
<rect x="122" y="206" width="152" height="34" rx="4" fill="#cbd5e1" stroke="{SLATE}" stroke-width="2"/>
<line x1="198" y1="214" x2="198" y2="236" stroke="{GREEN}" stroke-width="3" marker-end="url(#arr-green)"/>
{txt(198, 172, "火焰锋面 20~40 m/s 平顺扩散", size=10.6, color=GREEN, anchor="middle", weight="700", halo=True)}
{txt(198, 257, "上止点后 10°~15° 达峰值压力，稳推活塞下行", size=10.3, color=INK, anchor="middle", weight="600")}"""
    )

    el.append(txt(42, 286, "• 火花塞在上止点前 10°~35° 点火，单一火焰波像海浪一样推进", size=10.8, color=BODY))
    el.append(txt(42, 307, "• 角落里的未燃混合气“定力够高”，耐心等火焰扫过才燃烧", size=10.8, color=BODY))
    el.append(txt(42, 328, "• 缸压曲线圆润平滑，正好在曲柄力臂黄金角度发力做功", size=10.8, color=GREEN, weight="700"))
    el.append(txt(42, 349, "• 气缸壁附着一层低温气体边界层，保护铝活塞不被烧熔", size=10.5, color=MUTED))

    # Right panel: Engine Knock / Detonation (x=388..736, y=68..372)
    el.append(card(388, 68, 348, 304, rx=10, stroke=RED, sw=1.4))
    el.append(step_badge(406, 88, "2", fg=RED, bg=RED_SOFT, r=10))
    el.append(txt(422, 92, "爆震敲缸（辛烷值不足）：末端自燃激波对撞！", size=12.3, color=RED, weight="700"))

    el.append(card(406, 108, 312, 156, rx=8, fill=RED_SOFT, stroke=RED))
    el.append(
        f"""<rect x="482" y="122" width="160" height="128" rx="6" fill="#fff1f2" stroke="{RED}" stroke-width="2.5"/>
<rect x="557" y="110" width="10" height="16" rx="2" fill="{INK}"/>
<path d="M 510,132 Q 562,176 614,132" fill="none" stroke="{ORANGE}" stroke-width="2.4"/>
<circle cx="506" cy="186" r="16" fill="#fecaca" stroke="{RED}" stroke-width="2.2" stroke-dasharray="3 2"/>
<circle cx="618" cy="186" r="16" fill="#fecaca" stroke="{RED}" stroke-width="2.2" stroke-dasharray="3 2"/>
{txt(506, 190, "自燃!", size=9.8, color=RED, anchor="middle", weight="700")}
{txt(618, 190, "自燃!", size=9.8, color=RED, anchor="middle", weight="700")}
<rect x="486" y="206" width="152" height="34" rx="4" fill="#cbd5e1" stroke="{RED}" stroke-width="2"/>
{txt(562, 162, "主火焰未到，角落混合气先炸了！", size=10.4, color=INK, anchor="middle", weight="700", halo=True)}
{txt(562, 227, "活塞正往上顶 ← 激波 >1000 m/s 迎头猛砸", size=10.1, color=RED, anchor="middle", weight="700")}
{txt(562, 257, "发出清脆铁锤敲击般“咔啦咔啦”金属敲缸声", size=10.3, color=RED, anchor="middle", weight="700")}"""
    )

    el.append(txt(406, 286, "• 主火焰膨胀把角落未燃油气挤得又热又密，低标号油撑不住自燃", size=10.8, color=BODY))
    el.append(txt(406, 307, "• 速度从几十米/秒突变为超音速激波（>1000 m/s），峰值缸压翻倍", size=10.8, color=RED, weight="700"))
    el.append(txt(406, 328, "• 激波刮掉缸壁隔热边界层 → 铝活塞顶像被喷砂一样蚀坑甚至烧穿！", size=10.8, color=BODY))
    el.append(txt(406, 349, "• 涡轮直喷机更需警惕机油液滴诱发的破坏性“低速早燃/超级爆震”", size=10.5, color=MUTED))

    # Bottom strip: Knock sensor & ECU ignition retard rescue (x=24..736, y=386..504)
    el.append(card(24, 386, 712, 118, rx=10, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.2))
    el.append(txt(40, 410, "实战问答：规定加 95 号的涡轮车，偏远地区被迫加了一箱 92 号油，为什么没听到敲缸却觉得肉、还更费油？", size=11.8, color=INK, weight="700"))
    el.append(txt(40, 436, "1. 爆震传感器立功：缸体上的压电陶瓷“听诊器”刚捕捉到微弱爆震高频振动，立刻向行车电脑 ECU 拉响警报；", size=11, color=BODY))
    el.append(txt(40, 459, "2. 推迟点火提前角（丢卒保车）：ECU 被迫等活塞越过上止点开始往下走了才点火、并泄掉部分涡轮增压值来降温防炸；", size=11, color=PURPLE, weight="700"))
    el.append(txt(40, 482, "3. 隐藏代价：燃烧追着下行的活塞跑，热效率大跌 → 动力变肉、排气滚烫、百公里油耗反升（应急时务必轻踩油门）！", size=11, color=BODY))

    return figure(
        518,
        "汽油机正常火焰推进与爆震敲缸机理及ECU推迟点火对比图",
        "对比正常火花塞点火20-40m/s平顺燃烧与低辛烷值末端混合气自燃产生超1000m/s激波敲缸的物理过程，并解释现代爆震传感器推迟点火提前角保命却降低热效率的机制。",
        el,
    )


def build_grades_guide_and_myths() -> str:
    """Complete guide to 89/92/95/98/E10 gasoline grades and debunking the 4 classic refueling myths."""
    el = []
    el.extend(
        header(
            "各标号汽油全景指南与四大谣言终结：92 的车加 95 真能省油、清积碳吗？",
            "上排速查 89 / 92 / 95 / 98 / E10 适用机型 → 下排拆穿压缩比教条、高标号崇拜与冬夏配方秘密",
        )
    )

    # Top row: 5 grade pills/cards (x=24..736, y=66..182)
    grades = [
        ("89 号汽油", "RON ≥ 89", "低压缩比老引擎", "小型农机/割草机", SLATE, SLATE_SOFT),
        ("92 号汽油", "RON ≥ 92", "家用自然吸气主力", "混动阿特金森循环", BLUE, BLUE_SOFT),
        ("95 号汽油", "RON ≥ 95", "主流涡轮增压直喷", "欧系/国产高功率机", GREEN, GREEN_SOFT),
        ("98 / 102 号", "RON ≥ 98", "高增压性能车/超跑", "极限点火提前压榨马力", PURPLE, PURPLE_SOFT),
        ("E10 乙醇汽油", "90%油+10%醇", "与同标号抗爆相同", "亲水保质期约1个月", ORANGE, ORANGE_SOFT),
    ]
    for idx, (g_name, g_ron, g_l1, g_l2, fg_c, bg_c) in enumerate(grades):
        gx = 24 + idx * 144
        el.append(card(gx, 66, 136, 114, rx=8, fill=CARD_BG, stroke=fg_c, sw=1.2))
        el.append(pill(gx + 8, 74, g_name, fg=fg_c, bg=bg_c, w=120, h=20, size=10.8))
        el.append(txt(gx + 68, 113, g_ron, size=10.8, color=fg_c, anchor="middle", weight="700"))
        el.append(txt(gx + 68, 136, g_l1, size=10.3, color=INK, anchor="middle", weight="600"))
        el.append(txt(gx + 68, 156, g_l2, size=10.0, color=MUTED, anchor="middle"))

    # Bottom 2x2 Myth-Buster Grid: Row 1 y=194..346 (h=152), Row 2 y=358..510 (h=152)
    # Myth 1
    el.append(card(24, 194, 348, 152, rx=10))
    el.append(step_badge(42, 214, "1", fg=BLUE, bg=BLUE_SOFT, r=10))
    el.append(txt(58, 218, "迷思 ① “压缩比超 10 就必须加 95？” → 早就过时了！", size=12, color=INK, weight="700"))
    el.append(txt(40, 244, "• 反例 A：丰田/马自达等 13:1~14:1 高压缩比阿特金森/米勒循环", size=10.7, color=BODY))
    el.append(txt(50, 264, "机，靠“进气门晚关”吐回部分气体，实际压缩终温低，照喝 92#！", size=10.7, color=BLUE, weight="600"))
    el.append(txt(40, 287, "• 反例 B：涡轮机几何压缩比虽仅 9.8:1，但增压器硬塞进两倍密", size=10.7, color=BODY))
    el.append(txt(50, 307, "度滚烫空气，实际缸压极高，反而必须喝 95# 或 98#！", size=10.7, color=ORANGE, weight="600"))
    el.append(txt(40, 331, "• 唯一金标准：直接看油箱盖背面出厂贴纸，工程师已标定好！", size=10.8, color=GREEN, weight="700"))

    # Myth 2
    el.append(card(388, 194, 348, 152, rx=10))
    el.append(step_badge(406, 214, "2", fg=RED, bg=RED_SOFT, r=10))
    el.append(txt(422, 218, "迷思 ② “92 车加 95 更纯更省油？” → 纯智商税！", size=11.8, color=INK, weight="700"))
    el.append(txt(404, 244, "• 清洁度完全相同：国六下 92/95/98 硫含量统统严控在", size=10.6, color=BODY))
    el.append(txt(414, 264, "≤ 10 ppm，杂质与胶质限值一视同仁，高标号并不更纯！", size=10.6, color=RED, weight="600"))
    el.append(txt(404, 287, "• 热值几乎重叠：各标号低位热值均约 43~44 MJ/kg（体积", size=10.6, color=BODY))
    el.append(txt(414, 307, "差 < 1.8%），填不平 6%+ 差价；高芳烃反易生积碳。", size=10.6, color=BODY))
    el.append(txt(404, 331, "• 92 车 ECU 不会凭空涨压缩比，多花的钱纯打水漂。", size=10.6, color=MUTED))

    # Myth 3
    el.append(card(24, 358, 348, 152, rx=10))
    el.append(step_badge(42, 378, "3", fg=PURPLE, bg=PURPLE_SOFT, r=10))
    el.append(txt(58, 382, "冷知识 ③ 当年 90/93/97 为什么集体降 1 分变 89/92/95？", size=12, color=INK, weight="700"))
    el.append(txt(40, 408, "• 炼油化学真相：国四升国五时，环保要求把汽油硫含量从 50 ppm", size=10.7, color=BODY))
    el.append(txt(50, 428, "猛砍五分之四降到 10 ppm，必须对催化裂化汽油深度“加氢脱硫”。", size=10.7, color=BODY))
    el.append(txt(40, 451, "• 加氢拔硫时，高辛烷值的“烯烃双键”也会顺手被氢饱和成低辛烷", size=10.7, color=PURPLE, weight="600"))
    el.append(txt(50, 471, "值烷烃，导致辛烷值天然掉约 1 分！顺势定为 89/92/95 + 新增 98，", size=10.7, color=PURPLE, weight="600"))
    el.append(txt(50, 491, "既保护三元催化器减少雾霾，又省下强行补辛烷值的炼厂巨额能耗。", size=10.5, color=MUTED))

    # Myth 4
    el.append(card(388, 358, 348, 152, rx=10))
    el.append(step_badge(406, 378, "4", fg=TEAL, bg=TEAL_SOFT, r=10))
    el.append(txt(422, 382, "闭环彩蛋 ④ 冬夏汽油暗换配方，恰与油箱负压首尾相连！", size=12, color=INK, weight="700"))
    el.append(txt(404, 408, "• 冬季配方（高蒸气压 RVP）：炼厂多调入易挥发丁烷组分，确保天", size=10.7, color=BODY))
    el.append(txt(414, 428, "寒地冻时冷启动也能迅速雾化点着火；", size=10.7, color=BODY))
    el.append(txt(404, 451, "• 夏季配方（低蒸气压 RVP）：严控挥发度，一来防油管沸腾“气阻”，", size=10.7, color=TEAL, weight="600"))
    el.append(txt(414, 471, "二来防止暴晒生出海量油气冲垮活性炭罐！加上“跳枪即停不凑整”，", size=10.7, color=TEAL, weight="600"))
    el.append(txt(414, 491, "就能让你的油箱碳罐呼吸顺畅十年不坏。", size=10.7, color=INK, weight="700"))

    return figure(
        524,
        "各标号汽油选油指南与四大常见加油误区拆解图",
        "汇总89/92/95/98及E10乙醇汽油的适用机型，并从工程与炼油化学角度拆解阿特金森循环与涡轮压缩比反差、高标号不等于高清洁度或高热值、国五降标号脱硫机理及冬夏蒸气压与碳罐保护的关联。",
        el,
    )


@register("fuel-tank-gasoline", "汽车油箱负压原理（EVAP）与各标号汽油科学图解", "engineering")
def build_all() -> list[str]:
    _verify_fuel_metrics()
    specs = [
        ("evap-loop-and-negative-pressure-anim.svg", build_evap_loop_anim()),
        ("healthy-breath-vs-crushed-tank.svg", build_healthy_vs_crushed_tank()),
        ("octane-ruler-isooctane-vs-heptane.svg", build_octane_ruler_diagram()),
        ("normal-flame-vs-engine-knock.svg", build_normal_vs_knock_combustion()),
        ("gasoline-grades-guide-and-myths.svg", build_grades_guide_and_myths()),
    ]
    written = []
    for fname, svg_text in specs:
        write_svg(SUBDIR, fname, svg_text)
        written.append(f"assets/images/{SUBDIR}/{fname}")
    return written
