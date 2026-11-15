"""Cosmic Nucleosynthesis & Chemical Evolution visual builders."""

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

CRIMSON = "#b91c1c"
CRIMSON_SOFT = "#fef2f2"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"


# AME2020 nuclear binding energy per nucleon B/A (MeV) for representative nuclides
BINDING_ENERGY_POINTS = [
    (1, "¹H", 0.000),
    (2, "²H", 1.112),
    (3, "³He", 2.573),
    (4, "⁴He", 7.074),
    (7, "⁷Li", 5.606),
    (9, "⁹Be", 6.463),
    (12, "¹²C", 7.680),
    (16, "¹⁶O", 7.976),
    (24, "²⁴Mg", 8.261),
    (28, "²⁸Si", 8.448),
    (40, "⁴⁰Ca", 8.551),
    (56, "⁵⁶Fe", 8.790),
    (62, "⁶²Ni", 8.795),
    (88, "⁸⁸Sr", 8.733),
    (120, "¹²⁰Sn", 8.505),
    (138, "¹³⁸Ba", 8.393),
    (197, "¹⁹⁷Au", 7.916),
    (208, "²⁰⁸Pb", 7.867),
    (238, "²³⁸U", 7.570),
]


def _verify_cosmic_nucleosynthesis_math():
    """Verify BBN mass fractions, Hoyle resonance energetics, AME2020 B/A peak, and 70 kg human body tally."""
    # 1. Big Bang Nucleosynthesis: n/p = 1/7 at t ~ 180s after deuterium bottleneck clears
    n_cnt, p_cnt = 2, 14
    assert n_cnt / p_cnt == 1 / 7
    total_nucleons = n_cnt + p_cnt  # 16
    he4_nucleons = 2 * n_cnt        # 4 nucleons locked into one He-4
    h1_nucleons = total_nucleons - he4_nucleons  # 12 lone protons
    y_p = he4_nucleons / total_nucleons          # 0.25 (25% He by mass)
    x_p = h1_nucleons / total_nucleons           # 0.75 (75% H by mass)
    assert abs(y_p - 0.25) < 1e-12 and abs(x_p - 0.75) < 1e-12
    # By number of nuclei: 12 H vs 1 He -> 12/13 = 92.31% H, 1/13 = 7.69% He
    assert abs(12 / 13 - 0.9230769) < 1e-5

    # 2. Hoyle state & Triple-Alpha energetics (MeV, CODATA / AME2020 nuclear masses)
    # 3 * m(He-4) - m(C-12) = 3 * (4.002603254 u - 2*me) - (12.0000000 u - 6*me) = 0.007809762 u
    u_to_mev = 931.49410242
    q_triple_alpha = (3 * 4.002603254 - 12.000000000) * u_to_mev  # +7.2747 MeV net energy release
    assert 7.274 <= q_triple_alpha <= 7.276
    # Be-8 is unbound by ~0.0918 MeV relative to 2 He-4; Be-8 + He-4 sits at +7.3666 MeV above C-12 ground
    e_threshold_be8_alpha = q_triple_alpha + 0.0918  # 7.3665 MeV
    e_hoyle = 7.6542                                  # Hoyle 0+ state in C-12
    delta_res = e_hoyle - e_threshold_be8_alpha       # +0.2877 MeV (matched by ~10^8 K Gamow peak!)
    assert 0.28 <= delta_res <= 0.30

    # 3. AME2020 Binding energy per nucleon peak check
    peak_a, peak_name, peak_ba = max(BINDING_ENERGY_POINTS, key=lambda item: item[2])
    assert peak_a == 62 and peak_name == "⁶²Ni"
    fe56_ba = dict((a, ba) for a, _, ba in BINDING_ENERGY_POINTS)[56]
    he4_ba = dict((a, ba) for a, _, ba in BINDING_ENERGY_POINTS)[4]
    u238_ba = dict((a, ba) for a, _, ba in BINDING_ENERGY_POINTS)[238]
    assert fe56_ba > 8.78 and fe56_ba > he4_ba > 7.0 and fe56_ba > u238_ba > 7.5

    # 4. Human 70 kg elemental mass budget check
    body_mass = 70.0
    m_o = 0.650 * body_mass      # 45.50 kg
    m_c = 0.185 * body_mass      # 12.95 kg
    m_h = 0.095 * body_mass      #  6.65 kg (Big Bang!)
    m_n = 0.032 * body_mass      #  2.24 kg
    m_ca = 0.015 * body_mass     #  1.05 kg
    m_p = 0.010 * body_mass      #  0.70 kg
    m_other = 0.013 * body_mass  #  0.91 kg (K, S, Na, Cl, Mg, Fe 4.2g, Zn, I 15-20mg, Au 0.2mg)
    assert abs((m_o + m_c + m_h + m_n + m_ca + m_p + m_other) - body_mass) < 1e-9
    stardust_frac = 1.0 - 0.095  # 90.5% of human body mass forged inside stars/explosions!
    assert abs(stardust_frac - 0.905) < 1e-9


def _purple_And_crimson_markers():
    return """<marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#6d28d9"/>
  </marker>
  <marker id="arr-crimson" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#b91c1c"/>
  </marker>"""


def _line(x1, y1, x2, y2, color=HAIRLINE, sw=1.5, dash=None, marker=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    mk = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{extra}{mk}/>'
    )


def _build_big_bang_3min():
    """SVG 1: First 20 minutes of the Big Bang — 1:7 n/p ratio -> 75% H / 25% He & A=5, A=8 mass-gap chasms."""
    h = 482
    el = []
    el.extend(
        header(
            "创世前 20 分钟的闪电炼金：为什么宇宙大爆炸只造出氢和氦就紧急熄火了？",
            "受困于“氘瓶颈”与质量数 A=5、A=8 两大无人断崖：中子质子比 1:7 直接算出了 75% 氢与 25% 氦",
        )
    )

    # Left Card: 2 neutrons + 14 protons = 25% He-4 + 75% H-1 by mass
    el.append(card(16, 68, 362, 398))
    el.append(pill(28, 80, "第 3 分钟账本：16 个核子的分配", fg=BLUE, bg=BLUE_SOFT, w=208, h=24))
    el.append(txt(244, 96, "n : p ≈ 1 : 7（即 2 : 14）", size=11.5, color=MUTED))

    el.append(txt(28, 124, "① 冷却至约 9 亿度（t ≈ 180 秒），氘核不再被光子打碎：", size=11.5, color=BODY))

    # Draw 2 neutrons + 14 protons in 2 rows of 8
    # Highlight first 2n + 2p inside a dashed box -> 1 He-4!
    el.append(
        f'<rect x="28" y="136" width="174" height="54" rx="8" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="4 3"/>'
    )
    el.append(txt(115, 151, "2中子 + 2质子 锁进 1 个氦-4", size=10.5, color=ORANGE, anchor="middle", weight="700"))
    for i in range(4):
        cx_p = 49 + i * 44
        is_n = i < 2
        fc = SLATE if is_n else BLUE
        lbl = "n" if is_n else "p"
        el.append(f'<circle cx="{cx_p}" cy="172" r="11" fill="{fc}"/>')
        el.append(txt(cx_p, 176, lbl, size=11, color="#ffffff", anchor="middle", weight="700"))

    # Next 4 protons on row 1
    for i in range(4):
        cx_p = 222 + i * 36
        el.append(f'<circle cx="{cx_p}" cy="172" r="11" fill="{BLUE}"/>')
        el.append(txt(cx_p, 176, "p", size=11, color="#ffffff", anchor="middle", weight="700"))

    # Remaining 8 protons on row 2
    for i in range(8):
        cx_p = 49 + i * 40
        el.append(f'<circle cx="{cx_p}" cy="212" r="11" fill="{BLUE}"/>')
        el.append(txt(cx_p, 216, "p", size=11, color="#ffffff", anchor="middle", weight="700"))

    el.append(_line(197, 232, 197, 258, color=BLUE, sw=2.0, marker="arr-blue"))
    el.append(txt(210, 249, "瞬间聚变清场", size=11, color=BLUE, weight="600"))

    # Result boxes: 25% He-4 vs 75% H-1
    el.append(
        f'<rect x="28" y="266" width="156" height="86" rx="8" fill="{ORANGE_SOFT}" stroke="#fdba74"/>'
    )
    el.append(txt(106, 288, "氦-4（⁴He）", size=12.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(106, 311, "占 4 / 16 核子质量", size=11.5, color=BODY, anchor="middle"))
    el.append(txt(106, 336, "质量占比 ≈ 25%", size=13, color=ORANGE, anchor="middle", weight="700"))

    el.append(
        f'<rect x="196" y="266" width="170" height="86" rx="8" fill="{BLUE_SOFT}" stroke="#93c5fd"/>'
    )
    el.append(txt(281, 288, "氢-1（¹H 单质子）", size=12.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(281, 311, "剩 12 / 16 核子质量", size=11.5, color=BODY, anchor="middle"))
    el.append(txt(281, 336, "质量占比 ≈ 75%", size=13, color=BLUE, anchor="middle", weight="700"))

    el.append(
        f'<rect x="28" y="366" width="338" height="86" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    el.append(txt(40, 387, "注意区分“按质量算”与“按原子个数算”：", size=11.5, color=INK, weight="700"))
    el.append(txt(40, 408, "• 按质量：75% 氢 + 25% 氦（外加约 10⁻⁹ 量级锂-7）", size=11, color=BODY))
    el.append(txt(40, 428, "• 按个数：12 颗氢对 1 颗氦 ⇒ 氢占 92.3%，氦占 7.7%！", size=11, color=BLUE, weight="600"))
    el.append(txt(40, 445, "  （宇宙微波背景与古老气体云实测完美吻合这一理论预言）", size=10.5, color=MUTED))

    # Right Card: Why BBN stopped — A=5 and A=8 Mass Gaps + Rapid Expansion Cooling
    el.append(card(390, 68, 354, 398))
    el.append(pill(402, 80, "第 20 分钟熄火：两道质量数断崖", fg=CRIMSON, bg=CRIMSON_SOFT, w=214, h=24))
    el.append(txt(624, 96, "A=5 与 A=8 无稳定核", size=11.5, color=MUTED))

    # Stepping stones diagram (y ~ 180..240)
    stones = [
        (422, "A=1", "¹H 稳", GREEN_SOFT, GREEN, True),
        (468, "A=2,3", "²H ³He", GREEN_SOFT, GREEN, True),
        (518, "A=4", "⁴He 极稳", ORANGE_SOFT, ORANGE, True),
        (572, "A=5", "断崖!", CRIMSON_SOFT, CRIMSON, False),
        (626, "A=8", "断崖!", CRIMSON_SOFT, CRIMSON, False),
        (694, "A=12", "¹²C 碳", SLATE_SOFT, MUTED, True),
    ]
    for sx, top_t, sub_t, bg_s, fg_s, solid in stones:
        if solid:
            el.append(
                f'<rect x="{sx - 22:.1f}" y="164" width="44" height="52" rx="7" fill="{bg_s}" stroke="{fg_s}" stroke-width="1.5"/>'
            )
            el.append(txt(sx, 184, top_t, size=11, color=fg_s, anchor="middle", weight="700"))
            el.append(txt(sx, 204, sub_t, size=10, color=BODY, anchor="middle"))
        else:
            el.append(
                f'<rect x="{sx - 22:.1f}" y="182" width="44" height="54" rx="7" fill="{bg_s}" stroke="{fg_s}" stroke-width="1.5" stroke-dasharray="3 3"/>'
            )
            el.append(txt(sx, 202, top_t, size=11, color=fg_s, anchor="middle", weight="700"))
            el.append(txt(sx, 222, sub_t, size=10.5, color=fg_s, anchor="middle", weight="700"))

    # Blocked jump arcs from A=4
    el.append(
        f'<path d="M 526 160 Q 548 128 568 176" fill="none" stroke="{CRIMSON}" stroke-width="1.7" marker-end="url(#arr-crimson)"/>'
    )
    el.append(txt(546, 134, "⁴He+p", size=10.5, color=CRIMSON, anchor="middle", weight="700"))

    el.append(
        f'<path d="M 532 160 Q 580 108 622 176" fill="none" stroke="{CRIMSON}" stroke-width="1.7" marker-end="url(#arr-crimson)"/>'
    )
    el.append(txt(588, 120, "⁴He+⁴He", size=10.5, color=CRIMSON, anchor="middle", weight="700"))

    # Detailed explanation cards below stones
    el.append(
        f'<rect x="402" y="252" width="330" height="96" rx="8" fill="{CRIMSON_SOFT}" stroke="#fca5a5"/>'
    )
    el.append(txt(414, 273, "为什么跨不过去？自然界缺失两块关键踏脚石：", size=11.5, color=CRIMSON, weight="700"))
    el.append(txt(414, 295, "• A = 5 全灭：⁵He 与 ⁵Li 在约 10⁻²² 秒内瞬间散架；", size=11, color=BODY))
    el.append(txt(414, 316, "• A = 8 全灭：两个氦拼成的 ⁸Be 在 8.2×10⁻¹⁷ 秒内裂回两半；", size=11, color=BODY))
    el.append(txt(414, 336, "• 等不及第 3 颗氦撞上来，宇宙已极速膨胀变冷！", size=11, color=INK, weight="600"))

    el.append(
        f'<rect x="402" y="362" width="330" height="90" rx="8" fill="{AMBER_SOFT}" stroke="#fcd34d"/>'
    )
    el.append(txt(414, 383, "宇宙前 1~2 亿年“黑暗时代”的化学真相：", size=11.5, color=AMBER, weight="700"))
    el.append(txt(414, 405, "• 第 20 分钟后核聚变彻底停火：0 颗碳、0 颗氧、0 颗铁！", size=11, color=BODY))
    el.append(txt(414, 426, "• 没有岩石行星，没有一滴水（H₂O 缺氧），只有漫天氢氦云，", size=11, color=BODY))
    el.append(txt(414, 444, "  静待引力把它们重新压进第一代恒星的高压炉。", size=11, color=INK, weight="600"))

    write_svg(
        "cosmic-elements",
        "big-bang-3min-bottleneck.svg",
        figure(
            h,
            "宇宙大爆炸前20分钟原初核合成75%氢与25%氦比例计算及A=5、A=8质量断崖图",
            "左面板展示中子质子比1:7（2中子配14质子）合成1个氦-4与12个氢-1，严格得出氦占质量25%、氢占75%；右面板展示因缺乏A=5（⁵He/⁵Li）和A=8（⁸Be寿命仅8.2×10⁻¹⁷秒）稳定核且宇宙急速膨胀降温，大爆炸无法合成碳及更重元素。",
            el,
            extra_defs=_purple_And_crimson_markers(),
        ),
    )


def _build_triple_alpha_and_spallation():
    """SVG 2: Hoyle's Triple-Alpha resonance (with 1-shot accessible CSS animation) & Cosmic-Ray Spallation for Li/Be/B."""
    h = 476
    anim_css = """
      @keyframes ta-a1 {
        0%        { transform: translate(-54px, -24px); }
        34%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes ta-a2 {
        0%        { transform: translate(-54px, 24px); }
        34%, 100% { transform: translate(0px, 0px); }
      }
      @keyframes ta-a3 {
        0%, 30%   { transform: translate(-112px, -48px); opacity: 0.45; }
        62%, 100% { transform: translate(0px, 0px); opacity: 1; }
      }
      @keyframes ta-c12 {
        0%, 58%   { opacity: 0.25; }
        82%, 100% { opacity: 1; }
      }
      .ta-1 { animation: ta-a1 7s ease-out 0.3s 1 forwards; }
      .ta-2 { animation: ta-a2 7s ease-out 0.3s 1 forwards; }
      .ta-3 { animation: ta-a3 7s ease-in-out 0.3s 1 forwards; }
      .ta-fin { animation: ta-c12 7s ease-out 0.3s 1 forwards; }
      @media (prefers-reduced-motion: reduce) {
        .ta-1, .ta-2, .ta-3, .ta-fin {
          animation: none !important;
          transform: none !important;
          opacity: 1 !important;
        }
      }
    """
    el = []
    el.extend(
        header(
            "跨越 A=8 断崖的奇迹：霍伊尔“3α 共振”造碳术与锂铍硼的宇宙射线身世",
            "左看红巨星亿度核心如何靠 7.654 MeV 共振态三氦成碳（含单次动画）；右看宇宙射线如何敲碎碳氧补齐锂铍硼",
        )
    )

    # Left Card: Hoyle's Triple-Alpha Process (x=16..404)
    el.append(card(16, 68, 388, 392))
    el.append(pill(28, 80, "红巨星核心（≥ 1 亿 K）：3α 过程", fg=ORANGE, bg=ORANGE_SOFT, w=214, h=24))
    el.append(txt(250, 96, "霍伊尔 1953 预言共振态", size=11.5, color=MUTED))

    # Step 1 -> Step 2 -> Step 3 visual chain inside Left Card (y=118..296)
    # Two initial He-4 labels on far left (static reference)
    el.append(
        f'<circle cx="56" cy="164" r="16" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="3 2"/>'
    )
    el.append(txt(56, 168, "⁴He", size=11, color=BLUE, anchor="middle", weight="700"))
    el.append(
        f'<circle cx="56" cy="224" r="16" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="3 2"/>'
    )
    el.append(txt(56, 228, "⁴He", size=11, color=BLUE, anchor="middle", weight="700"))
    el.append(_line(76, 172, 112, 188, color=BLUE, sw=1.6, marker="arr-blue"))
    el.append(_line(76, 216, 112, 200, color=BLUE, sw=1.6, marker="arr-blue"))
    el.append(txt(92, 152, "① 双氦先撞", size=10.5, color=BLUE, anchor="middle", weight="600"))

    # Fleeting Be-8 box at x=146, y=194
    el.append(
        f'<rect x="116" y="168" width="64" height="52" rx="8" fill="{CRIMSON_SOFT}" stroke="{CRIMSON}" stroke-width="1.4" stroke-dasharray="4 2"/>'
    )
    el.append(
        '<g class="ta-1"><circle cx="136" cy="186" r="7" fill="#1d6fa5"/></g>'
        '<g class="ta-2"><circle cx="158" cy="186" r="7" fill="#1d6fa5"/></g>'
    )
    el.append(txt(148, 211, "⁸Be 瞬态", size=11, color=CRIMSON, anchor="middle", weight="700"))
    el.append(txt(148, 236, "仅活 8.2×10⁻¹⁷s", size=10.5, color=CRIMSON, anchor="middle"))

    # Third He-4 swooping in from top
    el.append(
        f'<circle cx="148" cy="126" r="14" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="3 2"/>'
    )
    el.append(txt(148, 130, "第3颗⁴He", size=9.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(_line(164, 134, 212, 170, color=ORANGE, sw=1.7, marker="arr-orange"))
    el.append(_line(184, 194, 212, 194, color=ORANGE, sw=1.8, marker="arr-orange"))
    el.append(txt(206, 146, "② 趁未散架闪击!", size=10.5, color=ORANGE, anchor="middle", weight="700"))

    # Hoyle Resonance State C-12* at x=254, y=194
    el.append(
        f'<rect x="216" y="162" width="80" height="64" rx="9" fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="1.8"/>'
    )
    el.append('<g class="ta-3"><circle cx="256" cy="176" r="6.5" fill="#c25014"/></g>')
    el.append(txt(256, 198, "¹²C* 霍伊尔态", size=11, color=AMBER, anchor="middle", weight="700"))
    el.append(txt(256, 216, "7.654 MeV 共振", size=10, color=BODY, anchor="middle"))

    # Relaxation to stable C-12 at x=354, y=194
    el.append(_line(300, 194, 322, 194, color=GREEN, sw=1.8, marker="arr-green"))
    el.append(txt(311, 178, "③放γ", size=10, color=GREEN, anchor="middle", weight="700"))
    el.append(
        f'<g class="ta-fin"><rect x="326" y="164" width="66" height="60" rx="9" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.8"/>'
        + txt(359, 191, "稳定 ¹²C", size=12, color=GREEN, anchor="middle", weight="700")
        + txt(359, 212, "碳诞生!", size=11, color=INK, anchor="middle", weight="600")
        + "</g>"
    )

    # Energy resonance match box at bottom of Left Card
    el.append(
        f'<rect x="28" y="256" width="364" height="190" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    el.append(txt(40, 278, "为什么霍伊尔敢靠“人类存在”倒推核能级？", size=12, color=INK, weight="700"))
    el.append(txt(40, 301, "• ⁸Be + ⁴He 门槛能量恰比基态 ¹²C 高出 7.367 MeV；", size=11, color=BODY))
    el.append(txt(40, 323, "• 红巨星亿度热运动再添约 0.29 MeV，合计 ≈ 7.65 MeV；", size=11, color=BODY))
    el.append(txt(40, 345, "• 1953 年福勒实验室果真在 7.654 MeV 测出 ¹²C 激发态！", size=11, color=ORANGE, weight="700"))
    el.append(txt(40, 367, "  共振把反应率放大超 1000 万倍；若此能级偏移 4%，", size=11, color=BODY))
    el.append(txt(40, 387, "  宇宙几乎造不出碳和氧（¹²C + ⁴He → ¹⁶O），生命无从谈起。", size=11, color=BODY))
    el.append(txt(40, 412, "• 净释能：3 颗 ⁴He → ¹²C + 7.275 MeV（紧接着吃第 4 颗氦变 ¹⁶O）", size=11, color=GREEN, weight="700"))
    el.append(txt(40, 434, "  （注：开启“减少动态效果”时直接静态呈现完整三步链）", size=10.5, color=MUTED))

    # Right Card: Why Li(3), Be(4), B(5) were skipped & forged by Cosmic-Ray Spallation (x=416..744)
    el.append(card(416, 68, 328, 392))
    el.append(pill(428, 80, "星际冷空间：宇宙射线散裂补缺", fg=PURPLE, bg=PURPLE_SOFT, w=212, h=24))
    el.append(txt(648, 96, "3·4·5 号从哪来？", size=11.5, color=MUTED))

    el.append(txt(428, 125, "悬念：恒星从 2 号氦直接跳到 6 号碳，", size=11.5, color=INK, weight="700"))
    el.append(txt(428, 145, "那 3 号锂(Li)、4 号铍(Be)、5 号硼(B)谁造的？", size=11.5, color=BODY))

    # Spallation visual diagram (y=164..294)
    el.append(
        f'<rect x="428" y="160" width="304" height="136" rx="8" fill="{PURPLE_SOFT}" stroke="#d8b4fe"/>'
    )
    # Incoming cosmic ray proton
    el.append(pill(438, 214, "高能宇宙射线 p", fg=CRIMSON, bg="#ffffff", w=104, h=24, size=10.5))
    el.append(_line(546, 226, 582, 226, color=CRIMSON, sw=2.2, marker="arr-crimson"))

    # Target C / N / O nucleus
    el.append(
        f'<circle cx="610" cy="226" r="23" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>'
    )
    el.append(txt(610, 223, "¹²C / ¹⁶O", size=10.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(610, 238, "星际重核", size=9.5, color=BODY, anchor="middle"))

    # Shattered fragments -> Li, Be, B
    el.append(_line(634, 212, 668, 186, color=PURPLE, sw=1.7, marker="arr-purple"))
    el.append(_line(636, 226, 668, 226, color=PURPLE, sw=1.7, marker="arr-purple"))
    el.append(_line(634, 240, 668, 266, color=PURPLE, sw=1.7, marker="arr-purple"))

    el.append(pill(672, 172, "³Li 锂", fg=PURPLE, bg="#ffffff", w=52, h=22, size=10.5))
    el.append(pill(672, 215, "⁴Be 铍", fg=PURPLE, bg="#ffffff", w=52, h=22, size=10.5))
    el.append(pill(672, 256, "⁵B 硼", fg=PURPLE, bg="#ffffff", w=52, h=22, size=10.5))

    # Bottom explanation of abundance canyon
    el.append(
        f'<rect x="428" y="310" width="304" height="136" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    el.append(txt(440, 332, "为什么锂铍硼在宇宙里比碳氧稀少上百万倍？", size=11.5, color=PURPLE, weight="700"))
    el.append(txt(440, 355, "• 在恒星内部：锂铍硼非但造不出来，在几百万度", size=11, color=BODY))
    el.append(txt(440, 375, "  下反而会被质子迅速烧毁（恒星是它们的坟场）；", size=11, color=BODY))
    el.append(txt(440, 398, "• 在星际空间：只能靠超新星加速的高能质子反向", size=11, color=BODY))
    el.append(txt(440, 418, "  “敲碎”现成的碳氮氧核（散裂反应），产量极低！", size=11, color=INK, weight="600"))
    el.append(txt(440, 437, "  （你家耐热高硼硅玻璃里的硼，全是星际撞击碎片）", size=10.5, color=MUTED))

    write_svg(
        "cosmic-elements",
        "triple-alpha-and-spallation.svg",
        figure(
            h,
            "红巨星霍伊尔3α共振合成碳-12单次动画分步图与锂铍硼宇宙射线散裂起源图",
            "左面板展示两颗氦-4先碰撞为寿命8.2×10⁻¹⁷秒的铍-8，第3颗氦-4借7.654 MeV霍伊尔共振态合成稳定碳-12；右面板展示星际高能宇宙射线质子击碎碳氧核产生3号锂、4号铍、5号硼。",
            el,
            extra_css=anim_css,
            extra_defs=_purple_And_crimson_markers(),
        ),
    )


def _build_binding_energy_curve():
    """SVG 3: Exact AME2020 Nuclear Binding Energy per Nucleon B/A curve showing the Iron-56 Peak."""
    h = 482
    el = []
    el.extend(
        header(
            "核物理第一铁律：比结合能曲线（B/A）为什么把恒星聚变死死卡在“铁-56”？",
            "按 AME2020 实验核质量精确绘制：铁峰左侧“聚变放能”点亮恒星，铁峰右侧“聚变倒贴能量”立刻熄火",
        )
    )

    el.append(card(16, 68, 728, 400))

    # Plot box: x in [98, 720] for A in [0, 250]; y in [104, 362] for B/A in [0, 9.5] MeV
    px0, px1 = 98.0, 720.0
    py0, py1 = 362.0, 104.0  # py0 is B/A=0, py1 is B/A=9.5

    def x_a(a_val):
        return px0 + (a_val / 250.0) * (px1 - px0)

    def y_ba(ba_val):
        return py0 - (ba_val / 9.5) * (py0 - py1)

    x_fe = x_a(56)

    # Shaded regions: Fusion exothermic (left of A=56) vs Endothermic fusion / Fission exothermic (right of A=56)
    el.append(
        f'<rect x="{px0:.1f}" y="{py1:.1f}" width="{x_fe - px0:.1f}" height="{py0 - py1:.1f}" '
        f'fill="{ORANGE_SOFT}" opacity="0.55"/>'
    )
    el.append(
        f'<rect x="{x_fe:.1f}" y="{py1:.1f}" width="{px1 - x_fe:.1f}" height="{py0 - py1:.1f}" '
        f'fill="{BLUE_SOFT}" opacity="0.45"/>'
    )

    # Horizontal gridlines for B/A = 0, 2, 4, 6, 8, 9 MeV
    for ba_tick in (0, 2, 4, 6, 8, 9):
        gy = y_ba(ba_tick)
        el.append(_line(px0, gy, px1, gy, color="#e2e8f0" if ba_tick > 0 else SLATE, sw=1.1 if ba_tick > 0 else 1.5))
        el.append(txt(px0 - 8, gy + 4, f"{ba_tick}", size=11, color=MUTED, anchor="end"))

    # Vertical ticks for A = 0, 50, 100, 150, 200, 250
    for a_tick in (0, 50, 100, 150, 200, 250):
        gx = x_a(a_tick)
        el.append(_line(gx, py0, gx, py0 + 5, color=SLATE, sw=1.2))
        el.append(txt(gx, py0 + 19, str(a_tick), size=11, color=MUTED, anchor="middle"))

    el.append(_line(px0, py1, px0, py0, color=SLATE, sw=1.5))
    el.append(txt(48, 232, "比结合能", size=11, color=INK, anchor="middle", weight="700"))
    el.append(txt(48, 250, "B/A (MeV)", size=10.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt((px0 + px1) / 2, py0 + 36, "原子核质量数 A（质子数 Z + 中子数 N）", size=11.5, color=INK, anchor="middle", weight="600"))

    # Vertical dashed summit line at Fe-56 / Ni-62
    el.append(_line(x_fe, py1, x_fe, py0, color=CRIMSON, sw=1.6, dash="5 3"))
    el.append(pill(x_fe - 64, 82, "铁峰绝壁 A≈56–62", fg=CRIMSON, bg=CRIMSON_SOFT, w=128, h=22, size=11))

    # Polyline through exact AME2020 points
    poly_pts = " ".join(f"{x_a(a):.1f},{y_ba(ba):.1f}" for a, _, ba in BINDING_ENERGY_POINTS)
    el.append(
        f'<polyline points="{poly_pts}" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>'
    )

    # Plot dots & carefully placed non-overlapping labels
    label_offsets = {
        "¹H": (16, -4),
        "²H": (18, 4),
        "⁴He": (28, -10),
        "⁷Li": (20, 13),
        "¹²C": (-2, -13),
        "¹⁶O": (16, -8),
        "²⁸Si": (16, 13),
        "⁵⁶Fe": (-20, -12),
        "⁸⁸Sr": (16, -10),
        "¹²⁰Sn": (18, -8),
        "¹⁹⁷Au": (-14, 16),
        "²³⁸U": (-18, -12),
    }
    for a, name, ba in BINDING_ENERGY_POINTS:
        cx_p, cy_p = x_a(a), y_ba(ba)
        is_peak = a in (56, 62)
        dot_c = CRIMSON if is_peak else (ORANGE if a <= 40 else PURPLE)
        el.append(
            f'<circle cx="{cx_p:.1f}" cy="{cy_p:.1f}" r="{"4.4" if is_peak else "3.4"}" '
            f'fill="{dot_c}" stroke="#ffffff" stroke-width="1.2"/>'
        )
        if name in label_offsets:
            dx, dy = label_offsets[name]
            el.append(
                txt(
                    cx_p + dx,
                    cy_p + dy,
                    f"{name}({ba:.2f})" if name in ("⁴He", "⁵⁶Fe", "²³⁸U") else name,
                    size=10.5,
                    color=CRIMSON if name == "⁵⁶Fe" else INK,
                    anchor="middle",
                    weight="700" if name in ("⁴He", "⁵⁶Fe", "¹⁹⁷Au", "²³⁸U") else "600",
                    halo=True,
                )
            )

    # Explanatory callouts inside plot area (ample empty space at bottom-middle/right where B/A < 6!)
    el.append(
        f'<rect x="122" y="258" width="214" height="76" rx="8" fill="#ffffff" stroke="{ORANGE}" stroke-width="1.3"/>'
    )
    el.append(txt(134, 279, "↖ 聚变放能上坡区（A < 56）", size=11.5, color=ORANGE, weight="700"))
    el.append(txt(134, 299, "轻核拼成重核 ⇒ 结合得更紧，", size=10.8, color=BODY))
    el.append(txt(134, 318, "多余质量按 ΔE=Δmc² 化作星光！", size=10.8, color=INK, weight="600"))

    el.append(
        f'<rect x="374" y="246" width="332" height="96" rx="8" fill="#ffffff" stroke="{PURPLE}" stroke-width="1.3"/>'
    )
    el.append(txt(386, 267, "↘ 铁后下坡区（A > 56：金、铂、铅、铀）", size=11.5, color=PURPLE, weight="700"))
    el.append(txt(386, 288, "• 往右强行聚变 = 倒贴巨额能量，恒星核心当场熄火坍缩！", size=10.8, color=CRIMSON, weight="600"))
    el.append(txt(386, 308, "• 往左核裂变（如 ²³⁸U/²³⁵U 裂回中等核）= 重新爬坡放能；", size=10.8, color=BODY))
    el.append(txt(386, 328, "• 造金和铀必须靠灾变现场倒贴能量“硬塞中子”！", size=10.8, color=INK, weight="600"))

    # Rigor footer inside card (2 wrapped lines)
    el.append(
        txt(
            32,
            436,
            "严谨注：单核子结合能绝对冠军其实是镍-62（8.795 MeV），铁-56（8.790 MeV）紧随第三；",
            size=10.5,
            color=MUTED,
        )
    )
    el.append(
        txt(
            32,
            454,
            "因大质量恒星硅燃烧沿 α 链直产双幻核镍-56 并经 β⁺ 衰变为铁-56，故宇宙元素丰度呈显著“铁峰”。",
            size=10.5,
            color=MUTED,
        )
    )

    write_svg(
        "cosmic-elements",
        "binding-energy-iron-peak.svg",
        figure(
            h,
            "原子核比结合能曲线（AME2020实验值）与铁-56聚变终点绝壁图",
            "按实验核质量绘制质量数A从1到238的平均核子结合能B/A曲线：氢-1为0，氦-4跃升至7.07 MeV，至铁-56（8.79 MeV）与镍-62（8.795 MeV）达最高峰，此后向金-197（7.92 MeV）与铀-238（7.57 MeV）回落，解释为何恒星放能聚变止步于铁。",
            el,
            extra_defs=_purple_And_crimson_markers(),
        ),
    )


def _build_onion_shells_and_countdown():
    """SVG 4: Massive star (~20 M_sun) onion-shell structure + exponential death countdown + Type Ia comparison."""
    h = 492
    el = []
    el.extend(
        header(
            "大质量恒星（≈20 M☉）的“洋葱圈”炼金炉与疯狂加速的死亡倒计时",
            "左图分层为示意半径（真实硅铁核心仅地球大小）；右图展示中微子逃逸如何把最后硅聚变压缩到仅 1 天",
        )
    )

    # Left Card: Onion shells schematic (x=16..356)
    el.append(card(16, 68, 340, 408))
    el.append(pill(28, 80, "临终前的同心“元素洋葱”（示意比例）", fg=ORANGE, bg=ORANGE_SOFT, w=234, h=24))

    ocx, ocy = 186.0, 248.0
    shells = [
        (124, "#eff6ff", "#93c5fd", "最外层：H 氢包层（未燃尽）", -110),
        (104, "#fef9c3", "#fde047", "He 氦层（H → He）", -90),
        (85, "#ffedd5", "#fdba74", "C 碳层（3α → C, O）", -71),
        (67, "#fce7f3", "#f9a8d4", "Ne 氖层（C → Ne, Mg）", -53),
        (50, "#ede9fe", "#c4b5fd", "O 氧层（Ne/O → Si, S）", -36),
        (34, "#dcfce7", "#86efac", "Si 硅层（Si → ⁵⁶Ni）", -20),
        (18, CRIMSON_SOFT, CRIMSON, "Fe", 0),
    ]
    for rad, f_col, s_col, _, _ in shells:
        el.append(
            f'<circle cx="{ocx:.1f}" cy="{ocy:.1f}" r="{rad}" fill="{f_col}" stroke="{s_col}" stroke-width="1.4"/>'
        )
    el.append(txt(ocx, ocy + 4, "铁核", size=10.5, color=CRIMSON, anchor="middle", weight="700"))

    # Clean leader labels on staggered vertical positions? Wait: centered labels on top/bottom arcs!
    el.append(txt(ocx, ocy - 109, "H 氢包层", size=10.5, color=BLUE, anchor="middle", weight="700", halo=True))
    el.append(txt(ocx, ocy - 90, "He 氦壳层", size=10, color=AMBER, anchor="middle", weight="700", halo=True))
    el.append(txt(ocx, ocy - 71, "C 碳氧壳层", size=10, color=ORANGE, anchor="middle", weight="700", halo=True))
    el.append(txt(ocx, ocy - 53, "Ne 氖镁层", size=9.8, color=CRIMSON, anchor="middle", weight="700", halo=True))
    el.append(txt(ocx, ocy + 45, "O 氧硅层", size=9.8, color=PURPLE, anchor="middle", weight="700", halo=True))
    el.append(txt(ocx, ocy + 28, "Si 硅层", size=9.8, color=GREEN, anchor="middle", weight="700", halo=True))

    # Bottom dual-supernova Iron source note inside Left Card
    el.append(
        f'<rect x="28" y="384" width="316" height="78" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    el.append(txt(40, 404, "你血液里的铁，不全是大质量恒星造的！", size=11.5, color=INK, weight="700"))
    el.append(txt(40, 424, "• 大质量超新星：主要抛洒氧、镁、硅、钙 + 约 40% 铁；", size=10.8, color=BODY))
    el.append(txt(40, 444, "• 白矮星 Ia 型热核整星殉爆：贡献太阳系约 60% 的铁！", size=10.8, color=CRIMSON, weight="700"))

    # Right Card: Accelerating Fusion Countdown Table (x=368..744)
    el.append(card(368, 68, 376, 408))
    el.append(pill(380, 80, "20 倍太阳质量恒星：燃料倒计时", fg=CRIMSON, bg=CRIMSON_SOFT, w=222, h=24))
    el.append(txt(610, 96, "对数级死亡冲刺", size=11.5, color=MUTED))

    stages = [
        ("① 氢燃烧 → 氦", "≈ 0.4 亿 K", "≈ 1,000 万年", 210, BLUE, BLUE_SOFT),
        ("② 氦燃烧 → 碳、氧", "≈ 2 亿 K", "≈ 100 万年", 176, TEAL, TEAL_SOFT),
        ("③ 碳燃烧 → 氖、镁", "≈ 8 亿 K", "≈ 600–1,000 年", 128, GREEN, GREEN_SOFT),
        ("④ 氖燃烧 → 氧、镁", "≈ 15 亿 K", "≈ 1 年", 92, AMBER, AMBER_SOFT),
        ("⑤ 氧燃烧 → 硅、硫", "≈ 20 亿 K", "≈ 6 个月", 68, ORANGE, ORANGE_SOFT),
        ("⑥ 硅燃烧 → 镍/铁", "≈ 35 亿 K", "仅 ≈ 1 天（24h）!", 38, PURPLE, PURPLE_SOFT),
        ("⑦ 铁核超 1.4 M☉ 坍缩", "> 50 亿 K", "不到 1 秒 ⇒ 超新星!", 16, CRIMSON, CRIMSON_SOFT),
    ]

    for idx, (st_name, temp_s, dur_s, bar_w, fg_c, bg_c) in enumerate(stages):
        ry = 118 + idx * 41
        el.append(
            f'<rect x="380" y="{ry}" width="352" height="34" rx="6" fill="#ffffff" stroke="{BORDER}"/>'
        )
        el.append(
            f'<rect x="380" y="{ry}" width="{bar_w}" height="34" rx="6" fill="{bg_c}"/>'
        )
        el.append(txt(390, ry + 22, st_name, size=11.2, color=INK, weight="700"))
        el.append(txt(544, ry + 22, temp_s, size=10.8, color=MUTED))
        el.append(txt(722, ry + 22, dur_s, size=11.2, color=fg_c, anchor="end", weight="700"))

    el.append(
        f'<rect x="380" y="410" width="352" height="52" rx="8" fill="{AMBER_SOFT}" stroke="#fcd34d"/>'
    )
    el.append(txt(392, 430, "为什么越往后烧得越快？双重催命符：", size=11.2, color=AMBER, weight="700"))
    el.append(txt(392, 449, "重核每核子释能骤降 + 99% 热量被穿墙而过的“中微子”瞬间偷走！", size=10.8, color=BODY))

    write_svg(
        "cosmic-elements",
        "massive-star-onion-countdown.svg",
        figure(
            h,
            "20倍太阳质量大质量恒星晚年洋葱壳层结构示意与七阶段核聚变死亡倒计时图",
            "左面板展示大质量恒星由外向内的氢、氦、碳、氖、氧、硅壳层与中心铁核（标明非等比例示意），并对比Ia型白矮星超新星贡献约60%铁；右面板列出从氢燃烧1000万年、碳燃烧数百年直至硅燃烧仅1天、铁核坍缩不足1秒的加速过程。",
            el,
            extra_defs=_purple_And_crimson_markers(),
        ),
    )


def _build_s_vs_r_process():
    """SVG 5: Bypassing Iron via neutral neutrons — AGB s-process vs Neutron-Star Merger r-process (GW170817 & JWST)."""
    h = 486
    el = []
    el.extend(
        header(
            "铁之后的元素怎么造？零电荷中子“暗度陈仓”：慢俘获（s）vs 快俘获（r）",
            "中子不带电、无视几十个质子的电磁斥力钻进原子核，再靠 β⁻ 衰变（n → p + e⁻）把元素序号往上推",
        )
    )

    # Left Card: (N, Z) Nuclear Chart Staircase (s-process vs r-process)
    el.append(card(16, 68, 392, 402))
    el.append(pill(28, 80, "核素图攀登路线：慢走楼梯 vs 海啸冲锋", fg=GREEN, bg=GREEN_SOFT, w=242, h=24))

    gx0, gy0 = 66.0, 388.0  # Origin of (N, Z) schematic chart
    gw, gh = 320.0, 256.0
    el.append(_line(gx0, gy0 - gh, gx0, gy0, color=SLATE, sw=1.5))
    el.append(_line(gx0, gy0, gx0 + gw, gy0, color=SLATE, sw=1.5))
    el.append(txt(40, gy0 - gh / 2, "质子数 Z", size=11, color=INK, anchor="middle", weight="700"))
    el.append(txt(40, gy0 - gh / 2 + 16, "(元素种类)", size=10, color=MUTED, anchor="middle"))
    el.append(txt(gx0 + gw / 2, gy0 + 22, "中子数 N（向右 = 吞入不带电中子）", size=11, color=INK, anchor="middle", weight="600"))

    # Valley of beta-stability band
    el.append(
        f'<polygon points="{gx0 + 18},{gy0 - 24} {gx0 + 236},{gy0 - 236} {gx0 + 258},{gy0 - 224} {gx0 + 36},{gy0 - 14}" '
        f'fill="{SLATE_SOFT}" stroke="#cbd5e1" stroke-width="1"/>'
    )
    el.append(txt(gx0 + 112, gy0 - 150, "β 稳定核素谷", size=10.5, color=SLATE, weight="700", halo=True))

    # Fe-56 starting seed
    fx, fy = gx0 + 28, gy0 - 22
    el.append(f'<circle cx="{fx}" cy="{fy}" r="6" fill="{INK}"/>')
    el.append(txt(fx - 4, fy - 12, "⁵⁶Fe 种子", size=10.5, color=INK, weight="700", halo=True))

    # s-process staircase hugging the stability valley (Green)
    s_pts = [
        (fx, fy),
        (fx + 26, fy), (fx + 16, fy - 24),
        (fx + 44, fy - 24), (fx + 34, fy - 48),
        (fx + 64, fy - 48), (fx + 54, fy - 74),
        (fx + 86, fy - 74), (fx + 76, fy - 102),
        (fx + 112, fy - 102), (fx + 102, fy - 130),
        (fx + 142, fy - 130), (fx + 132, fy - 158),
        (fx + 172, fy - 158), (fx + 164, fy - 186),
    ]
    el.append(
        f'<polyline points="{" ".join(f"{x},{y}" for x, y in s_pts)}" fill="none" stroke="{GREEN}" stroke-width="2.2"/>'
    )
    el.append(f'<circle cx="{fx + 164}" cy="{fy - 186}" r="5.5" fill="{GREEN}"/>')
    el.append(pill(gx0 + 62, gy0 - 238, "s-过程终点：铅(82)/铋(83)", fg=GREEN, bg=GREEN_SOFT, w=166, h=22, size=10.5))
    el.append(txt(gx0 + 48, gy0 - 82, "s-慢俘获", size=11, color=GREEN, weight="700", halo=True))

    # r-process tsunami (Orange horizontal burst right, then diagonal beta-decay cascade up-left to Au/Pt & U/Th!)
    rx1, ry1 = fx + 216, fy - 22
    rx2, ry2 = fx + 278, fy - 138
    ux, uy = fx + 214, fy - 218
    el.append(_line(fx, fy, rx1, ry1, color=ORANGE, sw=2.4, marker="arr-orange"))
    el.append(_line(rx1, ry1, rx2, ry2, color=ORANGE, sw=2.2, dash="5 3"))
    el.append(_line(rx2, ry2, ux, uy, color=PURPLE, sw=2.4, marker="arr-purple"))
    el.append(_line(fx + 228, fy - 74, fx + 158, fy - 150, color=PURPLE, sw=2.0, marker="arr-purple"))

    el.append(txt(fx + 168, fy + 4, "r-快俘获（<1s 狂吞数十中子）", size=10.3, color=ORANGE, anchor="middle", weight="700", halo=True))
    el.append(txt(fx + 258, fy - 64, "极端丰中子区", size=10.5, color=ORANGE, anchor="middle", weight="600", halo=True))
    el.append(txt(fx + 252, fy - 178, "连环 β⁻ 衰变", size=10.5, color=PURPLE, anchor="middle", weight="700", halo=True))
    el.append(pill(fx + 174, fy - 242, "越过断层 → 金(79)·铂·铀(92)!", fg=PURPLE, bg=PURPLE_SOFT, w=178, h=22, size=10.5))

    el.append(
        txt(
            28,
            433,
            "• s-过程（衰老红巨星）：数十年吞 1 中子，遇不稳定核先衰变，造锶、钡、铅；",
            size=10.3,
            color=BODY,
        )
    )
    el.append(
        txt(
            28,
            453,
            "• r-过程（中子星并合）：中子密度 >10²²/cm³，秒级越过裂变断层造黄金与铀！",
            size=10.3,
            color=INK,
            weight="600",
        )
    )

    # Right Card: Multi-Messenger Observational Proof (GW170817 & JWST GRB 230307A)
    el.append(card(420, 68, 324, 402))
    el.append(pill(432, 80, "天文破案铁证：当场抓获宇宙炼金炉", fg=PURPLE, bg=PURPLE_SOFT, w=236, h=24))

    # Evidence Box 1: GW170817 (2017 / 2019 ESO Strontium)
    el.append(
        f'<rect x="432" y="116" width="300" height="146" rx="8" fill="{ORANGE_SOFT}" stroke="#fdba74"/>'
    )
    el.append(pill(444, 128, "证据 ①：2017 双中子星并合 GW170817", fg=ORANGE, bg="#ffffff", w=242, h=22, size=10.8))
    el.append(txt(444, 170, "• 距离 1.3 亿光年（NGC 4993 星系），LIGO 先听见", size=11, color=BODY))
    el.append(txt(444, 190, "  引力波，全球 70 多台望远镜紧接着拍到“千新星”！", size=11, color=BODY))
    el.append(txt(444, 212, "• 欧洲南方天文台 VLT 光谱当场检出新生的 38 号锶(Sr)，", size=11, color=ORANGE, weight="700"))
    el.append(txt(444, 232, "  单次碰撞抛出的黄金、铂金等重元素总量达数倍地球质量！", size=10.8, color=INK, weight="600"))

    # Evidence Box 2: JWST GRB 230307A (2023 Tellurium)
    el.append(
        f'<rect x="432" y="274" width="300" height="118" rx="8" fill="{PURPLE_SOFT}" stroke="#d8b4fe"/>'
    )
    el.append(pill(444, 286, "证据 ②：2023 韦布望远镜直测 52 号碲", fg=PURPLE, bg="#ffffff", w=242, h=22, size=10.8))
    el.append(txt(444, 326, "• 韦布（JWST）追踪亮伽马暴千新星 GRB 230307A，", size=11, color=BODY))
    el.append(txt(444, 347, "  在 2.1 微米中红外波段首次直接捕获重元素碲（Te）！", size=11, color=PURPLE, weight="700"))
    el.append(txt(444, 368, "• 周期表上紧挨着碲的邻居，正是人体必需的 53 号碘（I）！", size=10.8, color=INK, weight="600"))

    # Ongoing frontier note (per AGENTS.md: clearly state active scientific debate!)
    el.append(
        f'<rect x="432" y="402" width="300" height="56" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>'
    )
    el.append(txt(444, 422, "前沿边界说明：", size=11, color=INK, weight="700"))
    el.append(txt(444, 441, "除中子星并合外，强磁场极超新星（磁旋转超新星）对早期宇宙", size=10.3, color=MUTED))
    el.append(txt(444, 454, "r-过程元素的分担比例，仍是当今核天体物理活跃课题。", size=10.3, color=MUTED))

    write_svg(
        "cosmic-elements",
        "neutron-capture-s-vs-r-process.svg",
        figure(
            h,
            "慢中子俘获（s-过程）与快中子俘获（r-过程）核素攀登路径及GW170817、韦布望远镜实测证据图",
            "左面板在(N,Z)核素图上对比AGB恒星s-过程沿稳定谷拾级而上至铅铋，与双中子星并合r-过程瞬间冲入丰中子区再经β衰变合成金、铂、铀；右面板总结2017年GW170817检出锶及2023年JWST检出碲的观测证据。",
            el,
            extra_defs=_purple_And_crimson_markers(),
        ),
    )


def _build_cosmic_evolution_and_human_body():
    """SVG 6: 13.8 Gyr Stellar Generations (Pop III -> II -> I) & 70 kg Human Body Cosmic Origin Receipt."""
    h = 492
    el = []
    el.extend(
        header(
            "138 亿年宇宙化学接力与你的身体：三代恒星演化及“人体 70 kg 产地账单”",
            "宇宙重元素丰度（Z）从 0% 一代代攒到太阳系的 1.4%，才凝结出岩质地球与我们一身滚烫的星尘",
        )
    )

    # Top Card: 13.8 Billion Years Chemical Enrichment (Pop III -> Pop II -> Pop I)
    el.append(card(16, 68, 728, 186))
    el.append(pill(28, 80, "上半场：138 亿年三代恒星“重元素（金属丰度 Z）”接力赛", fg=BLUE, bg=BLUE_SOFT, w=342, h=24))
    el.append(txt(380, 96, "天文学把氢、氦以外的所有元素统称“金属”", size=11, color=MUTED))

    gen_boxes = [
        (
            28,
            "第三星族 Pop III（最早!）",
            "宇宙约 1–3 亿岁 · Z = 0%",
            PURPLE,
            PURPLE_SOFT,
            "纯大爆炸氢氦云凝结，缺碳氧冷却，长成数十至上百倍太阳质量巨兽；仅活几百万年便轰然爆炸，播撒宇宙第一批碳、氧、硅、铁！",
        ),
        (
            268,
            "第二星族 Pop II（贫金属）",
            "宇宙约 3–80 亿岁 · Z ≈ 0.01%",
            AMBER,
            AMBER_SOFT,
            "含微量重元素，寿命可达百亿年（至今仍存于银河系晕与球状星团）；但硅镁铁尘埃太稀薄，尚难大量孕育类地岩质行星。",
        ),
        (
            508,
            "第一星族 Pop I（太阳与地球）",
            "92 亿岁太阳诞生 · Z☉ ≈ 1.4%",
            GREEN,
            GREEN_SOFT,
            "浓缩前百代超新星、AGB 星风、白矮星与中子星遗产！就靠这 1.4% 的“重元素佐料”，凝聚出了地球铁核、硅酸盐地壳与生命海洋。",
        ),
    ]
    for bx, b_title, b_sub, b_fg, b_bg, b_desc in gen_boxes:
        el.append(
            f'<rect x="{bx}" y="114" width="224" height="126" rx="8" fill="{b_bg}" stroke="{b_fg}" stroke-width="1.2"/>'
        )
        el.append(txt(bx + 10, 134, b_title, size=11.5, color=b_fg, weight="700"))
        el.append(txt(bx + 10, 152, b_sub, size=10.5, color=INK, weight="600"))
        # Wrap b_desc cleanly into 3 lines (~19 chars per line)
        lines_3 = [b_desc[0:19], b_desc[19:38], b_desc[38:57], b_desc[57:]]
        for li, l_str in enumerate(lines_3):
            if l_str:
                el.append(txt(bx + 10, 173 + li * 16, l_str, size=10.2, color=BODY))

    el.append(_line(254, 176, 266, 176, color=SLATE, sw=1.8, marker="arr-muted"))
    el.append(_line(494, 176, 506, 176, color=SLATE, sw=1.8, marker="arr-muted"))

    # Bottom Card: 70 kg Human Body Cosmic Origin Receipt
    el.append(card(16, 266, 728, 210))
    el.append(pill(28, 278, "下半场：一个 70 kg 成年人体的“宇宙产地溯源账单”", fg=ORANGE, bg=ORANGE_SOFT, w=324, h=24))
    el.append(txt(362, 294, "你体重的 90.5% 诞生于恒星熔炉与星体爆炸！", size=11.5, color=ORANGE, weight="700"))

    # Proportional Horizontal Bar (x=28..732, total width=704)
    # 65% O (458px), 18.5% C (130px), 9.5% H (67px), 3.2% N (23px), 3.8% Ca+P+Fe+I (26px)
    bar_y, bar_h = 312, 30
    segs = [
        (28, 456, GREEN, "氧 O 65% (45.5kg)"),
        (484, 130, TEAL, "碳 C 18.5% (13kg)"),
        (614, 67, BLUE, "氢 9.5%"),
        (681, 51, PURPLE, "氮钙铁碘"),
    ]
    for sx, sw_b, sc, slbl in segs:
        el.append(f'<rect x="{sx}" y="{bar_y}" width="{sw_b}" height="{bar_h}" rx="4" fill="{sc}"/>')
        el.append(txt(sx + sw_b / 2, bar_y + 20, slbl, size=10.5, color="#ffffff", anchor="middle", weight="700"))

    # 4 Receipt Origin Mini-Boxes below bar (y=354..462)
    receipts = [
        (28, 174, "大质量恒星 & 红巨星", "≈ 63.3 kg（90.5%）", GREEN, GREEN_SOFT, "呼吸的水氧、DNA 碳氮骨架、骨骼钙磷全由恒星聚变锻造。"),
        (210, 168, "宇宙大爆炸前 3 分钟", "≈ 6.65 kg（9.5%）", BLUE, BLUE_SOFT, "体内所有水分子和有机物里的氢(H)，已满 138 亿岁高龄！"),
        (386, 172, "白矮星 Ia + 坍缩超新星", "≈ 4.2 g 铁 + 锌铜", CRIMSON, CRIMSON_SOFT, "红细胞血红蛋白里的铁（够打一枚铁钉），六成源自白矮星殉爆。"),
        (566, 166, "双中子星并合千新星", "≈ 20 mg 碘 + 微量金", PURPLE, PURPLE_SOFT, "调节代谢的甲状腺素碘原子，每一颗都经历过中子星相撞！"),
    ]
    for rx, rw, r_t, r_mass, r_fg, r_bg, r_note in receipts:
        el.append(
            f'<rect x="{rx}" y="354" width="{rw}" height="108" rx="8" fill="{r_bg}" stroke="{BORDER}"/>'
        )
        el.append(txt(rx + 10, 374, r_t, size=11, color=r_fg, weight="700"))
        el.append(txt(rx + 10, 393, r_mass, size=11, color=INK, weight="700"))
        n1, n2, n3 = r_note[0:14], r_note[14:28], r_note[28:]
        el.append(txt(rx + 10, 414, n1, size=10.2, color=BODY))
        el.append(txt(rx + 10, 431, n2, size=10.2, color=BODY))
        if n3:
            el.append(txt(rx + 10, 448, n3, size=10.2, color=BODY))

    write_svg(
        "cosmic-elements",
        "cosmic-chemical-evolution-and-you.svg",
        figure(
            h,
            "138亿年宇宙三代恒星（Pop III/II/I）重元素演化与70公斤成年人体元素宇宙产地账单图",
            "上半部分展示从零金属第三星族巨星、贫金属第二星族到富含1.4%重元素的第一星族太阳系演化；下半部分按70 kg人体质量拆解氧65%、碳18.5%、大爆炸氢9.5%、白矮星与超新星铁4.2g、中子星并合碘20mg的宇宙来源。",
            el,
            extra_defs=_purple_And_crimson_markers(),
        ),
    )


@register("cosmic-elements", "Big Bang 3-min bottleneck, 3-alpha & spallation, B/A iron peak, onion shells, s/r-process, and human stardust", "science")
def build_cosmic_elements():
    _verify_cosmic_nucleosynthesis_math()
    _build_big_bang_3min()
    _build_triple_alpha_and_spallation()
    _build_binding_energy_curve()
    _build_onion_shells_and_countdown()
    _build_s_vs_r_process()
    _build_cosmic_evolution_and_human_body()
