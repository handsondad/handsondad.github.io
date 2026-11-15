"""Quantitative & step-by-step SVG visuals for Why Substances Are Acidic or Basic.

Generates 5 verified 760x520 figures under assets/images/acid-base-causes/:
1. grotthuss-proton-relay-anim.svg (1-shot CSS animation + reduced-motion fallback)
2. three-generations-acid-base-map.svg (Arrhenius -> Bronsted-Lowry -> Lewis nested unification)
3. four-atomic-switches-of-acidity.svg (R-O-H cleavage, period/group HF vs HI paradox, resonance)
4. titration-and-blood-buffer-curves.svg (exact HCl vs AcOH titration & pH 7.40 buffer shield)
5. everyday-ph-and-magic-acid-scale.svg (purple cabbage anthocyanin indicator + Olah's magic acid)
"""

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
    WIDTH,
    card,
    figure as _core_figure,
    header as _core_header,
    pill as _core_pill,
    register,
    step_badge,
    txt as _core_txt,
    write_svg,
)

SUBDIR = "acid-base-causes"
RED = "#b91c1c"
RED_BRIGHT = "#dc2626"
RED_SOFT = "#fef2f2"
BLUE_DARK = "#1e3a8a"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
VIOLET = "#7c3aed"
VIOLET_SOFT = "#f5f3ff"


def header(title: str, subtitle: str) -> str:
    return "\n".join(_core_header(title, subtitle))


def txt(x, y, value, size=12, weight=None, fill=BODY, anchor="start") -> str:
    return _core_txt(x, y, value, size=size, color=fill, anchor=anchor, weight=weight)


def pill(x, y, w, h, label, fill=BLUE_SOFT, stroke=BLUE, text_fill=BLUE, size=11) -> str:
    return _core_pill(x, y, label, fg=text_fill, bg=fill, border=stroke, w=w, h=h, size=size)


def figure(width, height, title, description, elements, extra_css="") -> str:
    return _core_figure(height, title, description, elements, extra_css=extra_css, width=width)


def build_grotthuss_proton_relay_anim() -> str:
    """1. 1-shot animated proton transfer + Grotthuss hydrogen-bond relay & taste/skin mechanism."""
    # Ionic mobility check in water at 25 C (10^-8 m^2 s^-1 V^-1):
    # H+ (~36.2) vs Na+ (~5.2) -> ~7.0x faster due to Grotthuss hopping!
    mobility_ratio = 36.2 / 5.2
    assert 6.8 <= mobility_ratio <= 7.2
    # Pure water at 25 C: [H2O] = 55.5 M, [H3O+] = 1.0e-7 M -> 1 in 555 million ionized
    unionized_per_ion = 55.5 / 1.0e-7
    assert 5.5e8 <= unionized_per_ion <= 5.6e8

    extra_css = """
      @keyframes hop1 {
        0%, 15%  { transform: translate(152px, 198px); opacity: 1; }
        38%, 100%{ transform: translate(236px, 198px); opacity: 1; }
      }
      @keyframes hop2 {
        0%, 36%  { transform: translate(294px, 198px); opacity: 1; }
        62%, 100%{ transform: translate(382px, 198px); opacity: 1; }
      }
      @keyframes hop3 {
        0%, 60%  { transform: translate(440px, 198px); opacity: 1; }
        86%, 100%{ transform: translate(528px, 198px); opacity: 1; }
      }
      @keyframes glowTarget {
        0%, 78%  { stroke-width: 1.8px; fill: #ffffff; }
        90%, 100%{ stroke-width: 3.2px; fill: #fef2f2; }
      }
      .p-hop1 { animation: hop1 5.4s ease-in-out 1 forwards; }
      .p-hop2 { animation: hop2 5.4s ease-in-out 1 forwards; }
      .p-hop3 { animation: hop3 5.4s ease-in-out 1 forwards; }
      .o-end  { animation: glowTarget 5.4s ease-in-out 1 forwards; }
      @media (prefers-reduced-motion: reduce) {
        .p-hop1 { animation: none !important; transform: translate(236px, 198px); }
        .p-hop2 { animation: none !important; transform: translate(382px, 198px); }
        .p-hop3 { animation: none !important; transform: translate(528px, 198px); }
        .o-end  { animation: none !important; stroke-width: 3.2px; fill: #fef2f2; }
      }
    """

    body = [
        header(
            "酸和碱在水里到底干了什么？“裸质子”抱水成团与格罗特斯接力跳",
            "先看上栏 H⁺ 在水分子链上的“击鼓传花”超高速跳跃 → 再看下栏为什么舌头觉得酸、手指觉得滑",
        ),
        # Top Card: Grotthuss Relay Chain (x=24..736, y=84..286)
        card(24, 84, 712, 202, fill="#ffffff", stroke=BORDER),
        step_badge(42, 106, 1, RED),
        txt(62, 111, "水中的真相：裸露质子 H⁺ 绝不单飞，靠氢键网格“换棒接力”狂飙（格罗特斯机制，1806）", size=12.3, weight="700", fill=INK),
        txt(42, 134, "H 丢掉唯一电子后半径缩至 ~10⁻¹⁵ m（比原子小十万倍！），强电场瞬间吸住水分子变成水合氢离子 H₃O⁺", size=11, fill=MUTED),
        # Hydrogen-bond track line
        f'<line x1="114" y1="198" x2="646" y2="198" stroke="#fca5a5" stroke-width="3" stroke-dasharray="6 5"/>',
        # Donor Cl- at x=112, Water1 O at x=265, Water2 O at x=411, Water3 O at x=557, OTOP1 gate at x=668
        f'<circle cx="112" cy="198" r="24" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2"/>',
        txt(112, 195, "HCl", size=11.5, weight="700", fill=GREEN, anchor="middle"),
        txt(112, 211, "→Cl⁻", size=10, fill=GREEN, anchor="middle"),
        f'<circle cx="265" cy="198" r="24" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
        txt(265, 195, "H₂O", size=11.5, weight="700", fill=BLUE_DARK, anchor="middle"),
        txt(265, 211, "水分子①", size=9.8, fill=BODY, anchor="middle"),
        f'<circle cx="411" cy="198" r="24" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>',
        txt(411, 195, "H₂O", size=11.5, weight="700", fill=BLUE_DARK, anchor="middle"),
        txt(411, 211, "水分子②", size=9.8, fill=BODY, anchor="middle"),
        f'<circle class="o-end" cx="557" cy="198" r="25" fill="#ffffff" stroke="{RED_BRIGHT}" stroke-width="2"/>',
        txt(557, 195, "H₃O⁺", size=11.5, weight="700", fill=RED, anchor="middle"),
        txt(557, 211, "新水合氢!", size=9.8, fill=RED, anchor="middle"),
        card(612, 166, 108, 64, rx=10, fill=RED_SOFT, stroke="#fca5a5"),
        txt(666, 189, "接棒终点", size=10.8, weight="700", fill=RED, anchor="middle"),
        txt(666, 207, "比 Na⁺ 挤地铁", size=10.2, fill=BODY, anchor="middle"),
        txt(666, 222, "快 ~7 倍！", size=10.8, weight="700", fill=RED, anchor="middle"),
        # Animated hopping protons (r=9 circles free of surrounding text!)
        f'<g class="p-hop1"><circle cx="0" cy="0" r="9.5" fill="{RED_BRIGHT}" stroke="#ffffff" stroke-width="1.6"/><text x="0" y="3.5" font-size="9.5" font-weight="700" fill="#ffffff" text-anchor="middle">H⁺</text></g>',
        f'<g class="p-hop2"><circle cx="0" cy="0" r="9.5" fill="{RED_BRIGHT}" stroke="#ffffff" stroke-width="1.6"/><text x="0" y="3.5" font-size="9.5" font-weight="700" fill="#ffffff" text-anchor="middle">H⁺</text></g>',
        f'<g class="p-hop3"><circle cx="0" cy="0" r="9.5" fill="{RED_BRIGHT}" stroke="#ffffff" stroke-width="1.6"/><text x="0" y="3.5" font-size="9.5" font-weight="700" fill="#ffffff" text-anchor="middle">H⁺</text></g>',
        txt(340, 248, "共价键与氢键交替翻转（O–H⋯O → O⋯H–O）：不必同一颗质子跑完全程，信号瞬间闪现对岸！", size=11, weight="600", fill=RED, anchor="middle"),
        pill(168, 256, 344, 22, "纯水自身也在拔河：每 5.55 亿个水分子仅有 1 对变成 H₃O⁺ + OH⁻", fill=SLATE_SOFT, stroke=SLATE, text_fill=INK, size=10.3),
        # Bottom Left Card: Why Sour? (OTOP1 Proton Channel)
        card(24, 300, 348, 148, fill=RED_SOFT, stroke="#fca5a5"),
        step_badge(42, 322, 2, RED),
        txt(62, 327, "为什么醋和柠檬“酸掉牙”？（OTOP1 质子门）", size=12.5, weight="700", fill=RED),
        txt(40, 352, "• 2018–2019 揭晓谜底：舌头酸味细胞膜上装有专属", size=11, fill=INK),
        txt(40, 372, "  质子离子通道 OTOP1（Otopetrin-1）；", size=11, weight="600", fill=INK),
        txt(40, 394, "• 食物里的 H₃O⁺ 顺通道直接涌入味蕾细胞内；", size=11, fill=BODY),
        txt(40, 414, "• 细胞膜电位反转触发神经放电 → 大脑亮起“酸味警报”", size=11, fill=BODY),
        txt(40, 434, "  （演化本意：提醒未熟野果或腐败变质食物！）", size=10.5, fill=MUTED),
        # Bottom Right Card: Why Slippery? (Skin Saponification)
        card(388, 300, 348, 148, fill=BLUE_SOFT, stroke="#93c5fd"),
        step_badge(406, 322, 3, BLUE),
        txt(426, 327, "为什么小苏打和碱水“滑溜溜”？（现场造肥皂！）", size=12.5, weight="700", fill=BLUE_DARK),
        txt(404, 352, "• 碱水本身并不比清水滑！滑的是你自己的皮肤油脂：", size=11, fill=INK),
        txt(404, 372, "  指尖皮脂 + OH⁻ ──▶ 脂肪酸盐（微米级肥皂膜）+ 甘油", size=11, weight="700", fill=BLUE_DARK),
        txt(404, 394, "• 这叫皂化反应（Saponification）：古人用草木灰水", size=11, fill=BODY),
        txt(404, 414, "  （含 K₂CO₃ 碱）洗头去油，正是把油污现场变成肥皂；", size=11, fill=BODY),
        txt(404, 434, "  ⚠️ 若摸到强碱觉得极滑，说明角质与皮脂正被溶解，速冲水！", size=10.5, weight="600", fill=RED),
        # Footer
        card(24, 460, 712, 42, rx=10, fill=AMBER_SOFT, stroke="#fcd34d"),
        txt(
            380,
            486,
            "1909 年嘉士伯啤酒厂实验室：丹麦化学家索伦森为精准控制酿酒酶酸度，发明 pH = −lg[H⁺]，把 0.0000001 M 化作简洁的 pH 7！",
            size=11.0,
            weight="600",
            fill=AMBER,
            anchor="middle",
        ),
    ]
    return figure(
        760,
        520,
        "水中质子格罗特斯接力跳跃机制与酸味味蕾、碱水皂化滑腻感原理图",
        "展示氯化氢在水中给出质子后通过水分子氢键网络发生格罗特斯跳跃接力，以及OTOP1质子通道产生酸味和氢氧根皂化皮脂产生滑腻感的机理。",
        body,
        extra_css=extra_css,
    )


def build_three_generations_acid_base_map() -> str:
    """2. Nested 3-tier theoretical upgrade: Arrhenius (1884) -> Bronsted-Lowry (1923) -> Lewis (1923)."""
    body = [
        header(
            "没有 OH⁻ 的氨水凭什么是碱？没有 H 的 CO₂ 凭什么变酸？三代酸碱大统一",
            "不是推翻前人而是层层扩容：阿伦尼乌斯水电离(1884) ⊂ 布朗斯特-劳里质子战(1923) ⊂ 路易斯电子对(1923)",
        ),
        # Outer Ring Card: Tier 3 Lewis (x=24..736, y=84..446)
        card(24, 84, 712, 362, rx=16, fill=PURPLE_SOFT, stroke="#c4b5fd", sw=2),
        step_badge(44, 108, 3, PURPLE),
        txt(66, 113, "第三代终极底层：路易斯电子理论（G. N. Lewis，1923）——连氢原子都不必有！", size=13, weight="700", fill=PURPLE),
        txt(44, 136, "判据：路易斯酸 = 缺电子“空房间”（接纳电子对）  ‖  路易斯碱 = 富电子“金主”（捐出孤对电子 :B）", size=11.5, weight="600", fill=INK),
        # Lewis examples on right column (x=504..722, y=152..432)
        card(502, 152, 218, 278, rx=12, fill="#ffffff", stroke="#c4b5fd"),
        txt(611, 176, "路易斯视野才懂的奇案", size=12, weight="700", fill=PURPLE, anchor="middle"),
        txt(516, 202, "① 汽水与酸雨为什么酸？", size=11, weight="700", fill=INK),
        txt(516, 220, "CO₂ 无 H，但碳带正电缺电子，", size=10.6, fill=BODY),
        txt(516, 238, "一口咬住 H₂O 孤对电子 → H₂CO₃！", size=10.6, fill=BODY),
        txt(516, 266, "② 明矾/三氯化铝为何显酸性？", size=11, weight="700", fill=INK),
        txt(516, 284, "Al³⁺ 空轨道猛拽周围水分子电子，", size=10.6, fill=BODY),
        txt(516, 302, "逼得水分子当场甩出 H⁺！", size=10.6, fill=BODY),
        txt(516, 330, "③ 经典无氢配位成键：", size=11, weight="700", fill=INK),
        pill(516, 342, 190, 24, "BF₃(空轨道) + :NH₃ → F₃B←NH₃", fill=PURPLE_SOFT, stroke=PURPLE, text_fill=PURPLE, size=10.2),
        txt(516, 388, "④ 血红素 Fe²⁺ 抓 O₂、叶绿素 Mg²⁺", size=10.5, fill=MUTED),
        txt(516, 406, "本质全都是路易斯酸碱配位！", size=10.5, weight="600", fill=PURPLE),
        # Middle Nested Card: Tier 2 Bronsted-Lowry (x=42..486, y=152..432)
        card(42, 152, 446, 278, rx=14, fill=BLUE_SOFT, stroke="#93c5fd", sw=1.8),
        step_badge(62, 176, 2, BLUE),
        txt(84, 181, "第二代：质子转移理论（Brønsted & Lowry，1923）", size=12.5, weight="700", fill=BLUE_DARK),
        txt(60, 202, "判据：酸 = 扔出 H⁺ 的射手 ‖ 碱 = 接住 H⁺ 的捕手（突破水限制！）", size=11, weight="600", fill=INK),
        txt(60, 224, "• 破解小苏打/氨水无 OH⁻ 之谜：它们不自带 OH⁻，而是抢走水的 H⁺！", size=10.8, fill=BODY),
        pill(60, 236, 408, 22, "NH₃(碱) + H₂O(酸) ⇌ NH₄⁺(共轭酸) + OH⁻(共轭碱)  |  隔空冒白烟也成立", fill="#ffffff", stroke=BLUE, text_fill=BLUE_DARK, size=10.2),
        # Inner Core Card: Tier 1 Arrhenius (x=60..468, y=272..416)
        card(60, 272, 410, 144, rx=12, fill="#ffffff", stroke=GREEN, sw=1.8),
        step_badge(80, 294, 1, GREEN),
        txt(102, 299, "第一代核心：水电离理论（Arrhenius，1884，诺奖）", size=12, weight="700", fill=GREEN),
        txt(78, 322, "• 酸：在水中解离出 H⁺(H₃O⁺)，如 HCl、H₂SO₄、HNO₃", size=10.8, fill=INK),
        txt(78, 344, "• 碱：在水中解离出 OH⁻，如 NaOH、KOH、Ca(OH)₂", size=10.8, fill=INK),
        txt(78, 366, "• 中和反应本质：H₃O⁺ + OH⁻ → 2 H₂O（放热 57.3 kJ/mol）", size=10.8, weight="600", fill=GREEN),
        txt(78, 392, "局限：出了水溶液（如气态氨遇氯化氢、熔融盐、有机溶剂）就失灵", size=10.3, fill=MUTED),
        # Footer historical twist
        card(24, 460, 712, 42, rx=10, fill=ORANGE_SOFT, stroke="#fdba74"),
        txt(
            380,
            486,
            "科学史彩蛋：拉瓦锡 1776 年误以为所有酸都含氧，才把 Oxygen 命名为“酸素”；直到 1810 年戴维证明盐酸不含氧才翻案！",
            size=11.0,
            weight="600",
            fill=ORANGE,
            anchor="middle",
        ),
    ]
    return figure(
        760,
        520,
        "阿伦尼乌斯、布朗斯特-劳里与路易斯三代酸碱理论包含关系图解",
        "用三层嵌套结构展示从水溶液电离H+和OH-、到质子给予体与接受体、再到电子对接受体与给予体的酸碱本质统一过程。",
        body,
    )


def build_four_atomic_switches_of_acidity() -> str:
    """3. The 4 atomic/structural switches causing acidity & basicity (including HF vs HI paradox!)."""
    # Quantitative check: delta pKa between HI (-10.4) and HF (+3.1) is 13.5 log units -> 10^13.5x stronger!
    delta_pka_hx = 3.1 - (-10.4)
    assert abs(delta_pka_hx - 13.5) < 1e-6
    # Acetic acid (pKa 4.76) vs Ethanol (pKa 15.9) -> >10^11x stronger due to carboxylate resonance!
    assert (15.9 - 4.76) > 11.0

    body = [
        header(
            "同挂着 -OH 为什么烧碱是强碱、酒精中性、醋酸是酸？四大原子级开关",
            "酸碱不是死记化学式，全看：① 拔河断哪根键 ② 同周期电负性 ③ 同族键能反杀 ④ 负离子稳不稳",
        ),
        # Quadrant 1 (Top-Left): R-O-H Bond Cleavage Tug-of-War
        card(24, 84, 348, 176, fill="#ffffff", stroke=BORDER),
        step_badge(42, 106, 1, BLUE),
        txt(62, 111, "开关①：X—O—H 三人拔河，到底断哪边？", size=12.3, weight="700", fill=INK),
        txt(40, 134, "氧电负性极高(3.44)，氢居中(2.20)，胜负全看左边 X 是谁：", size=10.8, fill=MUTED),
        pill(40, 146, 316, 24, "Na⁺ ⋯ ⁻O—H（X=0.93 慷慨金属）：断左键 → 放 OH⁻ 强碱！", fill=BLUE_SOFT, stroke=BLUE, text_fill=BLUE_DARK, size=10.3),
        pill(40, 178, 316, 24, "C₂H₅—O—H（X=2.55 势均力敌）：两边不断 → 酒精中性！", fill=SLATE_SOFT, stroke=SLATE, text_fill=INK, size=10.3),
        pill(40, 210, 316, 24, "O₃Cl—O⋯H⁺（高价吸电子团猛抽氧）：断右键 → 放 H⁺ 强酸！", fill=RED_SOFT, stroke=RED, text_fill=RED, size=10.3),
        txt(40, 250, "氯含氧酸铁证：HClO(7.5) → HClO₂(2.0) → HClO₃(-1) → HClO₄(-8)", size=10.2, weight="600", fill=RED),
        # Quadrant 2 (Top-Right): Period 2 Electronegativity Sweep
        card(388, 84, 348, 176, fill="#ffffff", stroke=BORDER),
        step_badge(406, 106, 2, TEAL),
        txt(426, 111, "开关②：同周期从左到右 → 电负性说了算", size=12.3, weight="700", fill=INK),
        txt(404, 134, "第二周期原子半径相近，核电荷越强，把 H 的电子抢得越狠：", size=10.8, fill=MUTED),
        # 4 mini boxes for CH4, NH3, H2O, HF
        card(404, 148, 72, 74, rx=8, fill=SLATE_SOFT, stroke=BORDER),
        txt(440, 168, "CH₄", size=12, weight="700", fill=INK, anchor="middle"),
        txt(440, 186, "pKa ~50", size=10, fill=MUTED, anchor="middle"),
        txt(440, 206, "死不放氢", size=10, weight="600", fill=SLATE, anchor="middle"),
        card(485, 148, 72, 74, rx=8, fill=BLUE_SOFT, stroke="#93c5fd"),
        txt(521, 168, "NH₃", size=12, weight="700", fill=BLUE_DARK, anchor="middle"),
        txt(521, 186, "孤对抢H⁺", size=10, fill=BLUE_DARK, anchor="middle"),
        txt(521, 206, "反而是碱!", size=10, weight="700", fill=BLUE_DARK, anchor="middle"),
        card(566, 148, 72, 74, rx=8, fill=TEAL_SOFT, stroke="#5eead4"),
        txt(602, 168, "H₂O", size=12, weight="700", fill=TEAL, anchor="middle"),
        txt(602, 186, "pKa 14", size=10, fill=TEAL, anchor="middle"),
        txt(602, 206, "两性基准", size=10, weight="600", fill=TEAL, anchor="middle"),
        card(647, 148, 73, 74, rx=8, fill=RED_SOFT, stroke="#fca5a5"),
        txt(683, 168, "HF", size=12, weight="700", fill=RED, anchor="middle"),
        txt(683, 186, "pKa 3.1", size=10, fill=RED, anchor="middle"),
        txt(683, 206, "明显显酸", size=10, weight="700", fill=RED, anchor="middle"),
        txt(562, 246, "从 CH₄ 到 HF：抢电子能力升级，酸性暴涨 10⁴⁶ 倍以上！", size=10.5, weight="600", fill=TEAL, anchor="middle"),
        # Quadrant 3 (Bottom-Left): Group 17 HF vs HI Bond-Energy Reversal
        card(24, 272, 348, 176, fill="#ffffff", stroke=BORDER),
        step_badge(42, 294, 3, ORANGE),
        txt(62, 299, "开关③：同主族往下 → 键能反杀电负性（HF冤案）", size=12.1, weight="700", fill=INK),
        txt(40, 322, "氟抢电子最强，为何氢氟酸在水里只是弱酸，氢碘酸却是超猛强酸？", size=10.5, fill=MUTED),
        txt(40, 344, "• HF（键能 567 kJ/mol）：F 太小，把 H⁺ 死死抱在怀里不撒手", size=10.6, weight="600", fill=ORANGE),
        txt(40, 364, "  → 水中 pKa = +3.1（弱酸！靠强结 Si–F 键才腐蚀玻璃）", size=10.5, fill=BODY),
        txt(40, 388, "• HCl(431) → HBr(366) → HI(298 kJ/mol)：碘像大皮球，", size=10.6, fill=INK),
        txt(40, 408, "  5p 与 1s 轨道够不着，一碰水就断 → HI pKa = −10.4！", size=10.6, weight="700", fill=RED),
        pill(40, 418, 316, 22, "结论：HI 比 HF 酸性强出 ~30 万亿倍（10¹³·⁵）！键弱更好断", fill=ORANGE_SOFT, stroke=ORANGE, text_fill=ORANGE, size=10.2),
        # Quadrant 4 (Bottom-Right): Conjugate Base Resonance & Inductive Effect
        card(388, 272, 348, 176, fill="#ffffff", stroke=BORDER),
        step_badge(406, 294, 4, PURPLE),
        txt(426, 299, "开关④：“离婚后”负离子稳不稳？（共振与诱导）", size=12.1, weight="700", fill=INK),
        txt(404, 322, "吐出 H⁺ 后留下的 A⁻ 负电荷越分散、越体面，酸就越肯放手：", size=10.5, fill=MUTED),
        txt(404, 346, "• 乙醇 C₂H₅O⁻：−1 电荷全压在 1 颗氧上 → 极想抢回 H⁺(pKa 16)", size=10.6, fill=BODY),
        txt(404, 370, "• 醋酸 CH₃COO⁻：双氧共振平摊各 −0.5 电荷 → 稳如泰山！", size=10.6, weight="700", fill=PURPLE),
        txt(404, 390, "  酸性瞬间比酒精暴涨 1,000 亿倍（pKa = 4.76）！", size=10.5, fill=PURPLE),
        pill(404, 414, 316, 24, "再挂三颗吸电子氟：三氟乙酸 CF₃COOH pKa 飙至 0.23 准强酸！", fill=PURPLE_SOFT, stroke=PURPLE, text_fill=PURPLE, size=10.2),
        # Footer unified rule
        card(24, 460, 712, 42, rx=10, fill=SLATE_SOFT, stroke=BORDER),
        txt(
            380,
            486,
            "一句话总口诀：H–A 键越极化、键长越长越易断、丢氢后的 A⁻ 电荷越分散稳定 —— 物质就越酸；反之有孤对电子爱抢 H⁺ 就越碱！",
            size=10.9,
            weight="600",
            fill=INK,
            anchor="middle",
        ),
    ]
    return figure(
        760,
        520,
        "决定物质酸碱强弱的四大分子与原子结构机制图解",
        "对比X-O-H成键电负性差异、第二周期氢化物酸性递增、卤化氢HF到HI键能主导的酸性反转以及羧酸根共振与诱导稳定效应。",
        body,
    )


def _titration_ph_strong(vol_naoh_ml: float, v0_ml: float = 25.0, c: float = 0.1) -> float:
    """Exact pH for titrating 25 mL of 0.1 M HCl with 0.1 M NaOH at 25 C."""
    n_acid = v0_ml * c
    n_base = vol_naoh_ml * c
    v_tot = v0_ml + vol_naoh_ml
    kw = 1.0e-14
    if abs(n_acid - n_base) < 1e-9:
        return 7.0
    elif n_acid > n_base:
        h = (n_acid - n_base) / v_tot
        return -math.log10(0.5 * (h + math.sqrt(h * h + 4.0 * kw)))
    else:
        oh = (n_base - n_acid) / v_tot
        h = kw / (0.5 * (oh + math.sqrt(oh * oh + 4.0 * kw)))
        return -math.log10(h)


def _titration_ph_weak(vol_naoh_ml: float, v0_ml: float = 25.0, c: float = 0.1, ka: float = 1.75e-5) -> float:
    """Accurate pH for titrating 25 mL of 0.1 M Acetic Acid (pKa 4.76) with 0.1 M NaOH."""
    v_tot = v0_ml + vol_naoh_ml
    ca = (v0_ml * c) / v_tot
    cb = (vol_naoh_ml * c) / v_tot
    kw = 1.0e-14
    # Solve charge balance [H+] + cb = kw/[H+] + ca * ka / ([H+] + ka) via bisection on pH in [0, 14]
    lo, hi = 0.5, 13.5
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        h = 10.0 ** (-mid)
        lhs = h + cb
        rhs = (kw / h) + (ca * ka) / (h + ka)
        if lhs > rhs:
            lo = mid  # too much H+, pH must be higher
        else:
            hi = mid
    return 0.5 * (lo + hi)


def build_titration_and_blood_buffer_curves() -> str:
    """4. Computed titration & buffer curves (HCl vs Acetic Acid + Human pH 7.40 Blood Buffer)."""
    ph_ac_start = _titration_ph_weak(0.0)
    ph_ac_half = _titration_ph_weak(12.5)
    ph_ac_eq = _titration_ph_weak(25.0)
    assert 2.85 <= ph_ac_start <= 2.90
    assert 4.73 <= ph_ac_half <= 4.78  # pH == pKa at half-equivalence!
    assert 8.70 <= ph_ac_eq <= 8.75    # Alkaline equivalence point due to acetate hydrolysis!

    # Plot box: x in [72..452] maps vol in [0..40 mL]; y in [104..424] maps pH in [14..0]
    x0, x1 = 72.0, 452.0
    y_top, y_bot = 104.0, 424.0

    def vx(v: float) -> float:
        return x0 + (v / 40.0) * (x1 - x0)

    def phy(ph: float) -> float:
        return y_bot - (ph / 14.0) * (y_bot - y_top)

    vols = [i * 0.5 for i in range(81)]
    pts_hcl = " ".join(f"{vx(v):.1f},{phy(_titration_ph_strong(v)):.1f}" for v in vols)
    pts_ac = " ".join(f"{vx(v):.1f},{phy(_titration_ph_weak(v)):.1f}" for v in vols)

    body = [
        header(
            "强酸与弱酸差在哪？为什么弱酸配盐能炼成“稳压防弹衣”（缓冲溶液）？",
            "左看精确计算的滴定曲线（醋酸半中和稳压平台与 pH 8.72 碱性终点）→ 右看人体血液 pH 7.40 生死护盾",
        ),
        # Left Card: Quantitative Titration Plot (x=24..474, y=84..448)
        card(24, 84, 450, 364, fill="#ffffff", stroke=BORDER),
        txt(38, 102, "0.1 M NaOH 滴定 25 mL 盐酸(红) vs 醋酸(蓝)", size=12, weight="700", fill=INK),
        # Horizontal gridlines for pH 0, 4.76, 7, 10, 13
        *[
            f'<line x1="{x0:.1f}" y1="{phy(p):.1f}" x2="{x1:.1f}" y2="{phy(p):.1f}" stroke="{HAIRLINE}" stroke-dasharray="3 3"/>'
            + txt(x0 - 6, phy(p) + 4, f"{p}", size=10, fill=MUTED, anchor="end")
            for p in (1, 5, 7, 9, 13)
        ],
        f'<line x1="{x0:.1f}" y1="{y_bot:.1f}" x2="{x1:.1f}" y2="{y_bot:.1f}" stroke="{BORDER}"/>',
        txt(x0 - 6, y_bot + 4, "0", size=10, fill=MUTED, anchor="end"),
        txt(38, 266, "pH", size=11, weight="700", fill=INK),
        # Shaded buffer zone around V=5..20 mL, pH=3.76..5.76
        f'<rect x="{vx(5):.1f}" y="{phy(5.76):.1f}" width="{vx(20) - vx(5):.1f}" height="{phy(3.76) - phy(5.76):.1f}" rx="6" fill="{BLUE_SOFT}" fill-opacity="0.7" stroke="#93c5fd" stroke-dasharray="4 2"/>',
        txt(vx(12.5), phy(5.76) - 6, "缓冲平台区（pH ≈ pKa ± 1）", size=10.3, weight="700", fill=BLUE_DARK, anchor="middle"),
        # Equivalence vertical line at V=25 mL
        f'<line x1="{vx(25):.1f}" y1="112" x2="{vx(25):.1f}" y2="{y_bot:.1f}" stroke="{AMBER}" stroke-width="1.3" stroke-dasharray="4 3"/>',
        # Curves
        f'<polyline points="{pts_hcl}" fill="none" stroke="{RED_BRIGHT}" stroke-width="2.6"/>',
        f'<polyline points="{pts_ac}" fill="none" stroke="{BLUE}" stroke-width="2.8"/>',
        # Key points
        f'<circle cx="{vx(12.5):.1f}" cy="{phy(ph_ac_half):.1f}" r="4.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.4"/>',
        f'<circle cx="{vx(25.0):.1f}" cy="{phy(ph_ac_eq):.1f}" r="4.5" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.4"/>',
        f'<circle cx="{vx(25.0):.1f}" cy="{phy(7.0):.1f}" r="4.5" fill="{RED_BRIGHT}" stroke="#ffffff" stroke-width="1.4"/>',
        # Annotations inside plot
        txt(vx(31), phy(8.72) + 4, "← 醋酸终点 pH 8.72(偏碱!)", size=10.2, weight="700", fill=PURPLE),
        txt(vx(31), phy(7.0) + 14, "← 盐酸终点 pH 7.00", size=10.2, weight="600", fill=RED),
        txt(vx(12.5), phy(4.76) + 16, "半中和 pH=4.76", size=10, weight="600", fill=BLUE_DARK, anchor="middle"),
        # X-axis ticks
        *[
            txt(vx(v), 440, f"{v}mL", size=9.8, fill=MUTED, anchor="middle")
            for v in (0, 12.5, 25, 40)
        ],
        # Right Card: How Buffer Shields Human Blood at pH 7.35-7.45 (x=490..736, y=84..448)
        card(490, 84, 246, 364, fill=TEAL_SOFT, stroke="#5eead4"),
        step_badge(508, 108, 1, TEAL),
        txt(528, 113, "生命的酸碱防弹衣", size=13, weight="700", fill=TEAL),
        txt(504, 136, "人体动脉血必须死守：", size=11, fill=INK),
        pill(504, 146, 218, 26, "pH 7.35 – 7.45（偏离 0.4 即危及生命）", fill="#ffffff", stroke=TEAL, text_fill=TEAL, size=10.4),
        txt(504, 194, "为什么喝柠檬水或狂跑产乳酸，", size=10.8, weight="700", fill=INK),
        txt(504, 212, "血液不会变酸？靠双向弹簧库：", size=10.8, weight="700", fill=INK),
        card(504, 224, 218, 66, rx=8, fill="#ffffff", stroke="#99f6e4"),
        txt(613, 246, "CO₂ + H₂O ⇌ H₂CO₃", size=11.2, weight="700", fill=TEAL, anchor="middle"),
        txt(613, 268, "⇌ H⁺ + HCO₃⁻（碳酸氢根）", size=11.2, weight="700", fill=BLUE_DARK, anchor="middle"),
        txt(504, 312, "• 酸冲进来（+H⁺）：", size=10.8, weight="700", fill=RED),
        txt(504, 330, "  海量 HCO₃⁻ 捕手瞬间吞掉 H⁺", size=10.5, fill=BODY),
        txt(504, 348, "  化成 CO₂，肺大口喘气呼出体外！", size=10.5, fill=BODY),
        txt(504, 372, "• 碱冲进来（+OH⁻）：", size=10.8, weight="700", fill=BLUE_DARK),
        txt(504, 390, "  H₂CO₃ 立刻补吐 H⁺ 把它中和成水！", size=10.5, fill=BODY),
        pill(504, 410, 218, 24, "粉碎谣言：“酸碱体质食疗”纯属伪科学！", fill=RED_SOFT, stroke=RED, text_fill=RED, size=10.1),
        # Footer
        card(24, 460, 712, 42, rx=10, fill=SLATE_SOFT, stroke=BORDER),
        txt(
            380,
            486,
            "强弱不等于浓稀：醋酸虽只电离 ~1%（弱酸），但 1 升 0.1 M 醋酸最终能中和的烧碱总量与 0.1 M 盐酸分毫不差（仓库照样吐光）！",
            size=10.9,
            weight="600",
            fill=INK,
            anchor="middle",
        ),
    ]
    return figure(
        760,
        520,
        "强酸与弱酸滴定曲线对比及人体血液碳酸氢盐缓冲体系机制图",
        "左侧绘制0.1M氢氧化钠滴定盐酸与醋酸的精确pH曲线及缓冲平台，右侧详解人体血液依靠CO2与碳酸氢根死守pH 7.35至7.45的原理。",
        body,
    )


def build_everyday_ph_and_magic_acid_scale() -> str:
    """5. Full acid-base spectrum: Olah's candle-eating Magic Acid + Everyday items + Purple Cabbage Indicator."""
    stops = [
        ("pH<0", "超强酸·魔酸", "H₀ ≈ −23", "#7f1d1d", "#fef2f2"),
        ("1.5", "人体胃酸", "杀菌助消化", "#dc2626", "#fee2e2"),
        ("2.4", "柠檬/可乐", "酸味浓郁", "#ea580c", "#ffedd5"),
        ("5.6", "正常雨水", "溶空气 CO₂", "#ca8a04", "#fef9c3"),
        ("7.0", "25°C纯水", "中性分水岭", "#16a34a", "#dcfce7"),
        ("7.4", "人体动脉血", "微弱偏碱", "#0d9488", "#ccfbf1"),
        ("8.3", "小苏打水", "馒头蓬松", "#0284c7", "#e0f2fe"),
        ("10.2", "肥皂/皮蛋", "皂化微滑", "#2563eb", "#dbeafe"),
        ("13.5", "管道通/烧碱", "强腐蚀溶发!", "#6d28d9", "#ede9fe"),
    ]

    body = [
        header(
            "从厨房紫甘蓝“变色龙”到一口吞掉蜡烛的“魔酸”：全景酸碱标尺",
            "每差 1 个 pH 单位代表 [H⁺] 相差 10 倍！上排看日常全景标尺 → 下排看花青素天然试纸与诺奖超强酸",
        ),
        # Top Card: 9-stop Spectrum (x=24..736, y=84..242)
        card(24, 84, 712, 158, fill="#ffffff", stroke=BORDER),
        txt(40, 106, "酸碱度全景阶梯（pH 每降 1 格，氢离子浓度翻 10 倍；可乐 pH 2.4 比纯水酸约 40,000 倍！）", size=11.8, weight="700", fill=INK),
    ]

    for idx, (ph_lbl, name, desc, fg, bg) in enumerate(stops):
        sx = 34 + idx * 77
        body.extend(
            [
                card(sx, 120, 71, 108, rx=8, fill=bg, stroke=fg, sw=1.4),
                txt(sx + 35.5, 142, ph_lbl, size=11.5, weight="700", fill=fg, anchor="middle"),
                txt(sx + 35.5, 168, name, size=10.2, weight="700", fill=INK, anchor="middle"),
                txt(sx + 35.5, 192, desc, size=9.6, fill=BODY, anchor="middle"),
            ]
        )

    body.extend(
        [
            # Bottom Left Card: Purple Cabbage Anthocyanin DIY Indicator
            card(24, 256, 348, 192, fill="#ffffff", stroke=BORDER),
            step_badge(42, 278, 1, PURPLE),
            txt(62, 283, "厨房里的天然试纸：紫甘蓝汤为什么变五彩？", size=12.2, weight="700", fill=PURPLE),
            txt(40, 306, "紫甘蓝、黑枸杞、蓝莓富含花青素（Anthocyanin），", size=10.8, fill=BODY),
            txt(40, 324, "得失 H⁺ 会直接改写分子共轭双键长度，切换吸收光色：", size=10.8, fill=BODY),
            # 4 color swatches
            pill(40, 338, 74, 24, "滴白醋:亮红", fill="#fee2e2", stroke="#dc2626", text_fill="#b91c1c", size=9.8),
            pill(120, 338, 74, 24, "自来水:紫蓝", fill="#ede9fe", stroke="#7c3aed", text_fill="#6d28d9", size=9.8),
            pill(200, 338, 74, 24, "小苏打:翠绿", fill="#dcfce7", stroke="#16a34a", text_fill="#15803d", size=9.8),
            pill(280, 338, 76, 24, "强碱水:亮黄", fill="#fef9c3", stroke="#ca8a04", text_fill="#a16207", size=9.8),
            txt(40, 386, "• 炒紫甘蓝滴醋红艳诱人；拿碱性井水焯烫秒变蓝绿“黑暗料理”！", size=10.4, fill=INK),
            txt(40, 408, "• 温度彩蛋：100°C 沸水中性点其实是 pH 6.14（自偶电离吸热），", size=10.4, fill=MUTED),
            txt(40, 426, "  此时 [H⁺] = [OH⁻]，它依然是百分之百的中性水！", size=10.4, weight="600", fill=TEAL),
            # Bottom Right Card: Olah's Candle-Dissolving Magic Acid
            card(388, 256, 348, 192, fill=RED_SOFT, stroke="#fca5a5"),
            step_badge(406, 278, 2, RED),
            txt(426, 283, "酸性的天花板：把圣诞蜡烛溶化的诺奖“魔酸”", size=12.2, weight="700", fill=RED),
            txt(404, 306, "在水里比不出高下的强酸（水的拉平效应），换上路易斯酸", size=10.8, fill=INK),
            txt(404, 324, "助阵就能突破天际！1966 圣诞派对后，奥拉实验室把石蜡蜡烛", size=10.8, fill=INK),
            txt(404, 342, "丢进 FSO₃H·SbF₅ 混合液，蜡烛竟像冰块一样溶化了：", size=10.8, weight="600", fill=INK),
            pill(404, 356, 316, 26, "CH₄(极稳烷烃) + H⁺ ──魔酸──▶ CH₅⁺(五配位碳正离子!)", fill="#ffffff", stroke=RED, text_fill=RED, size=10.3),
            txt(404, 404, "• 氟锑酸 (HF·SbF₅) 酸性高达纯硫酸的 10¹⁶–10¹⁹ 倍，必须装在", size=10.4, fill=BODY),
            txt(404, 424, "  聚四氟乙烯(特氟龙)瓶里——乔治·奥拉凭此独揽 1994 化学诺奖！", size=10.4, weight="600", fill=RED),
            # Footer
            card(24, 460, 712, 42, rx=10, fill=SLATE_SOFT, stroke=BORDER),
            txt(
                380,
                486,
                "跳出“0 到 14”刻板印象：10 mol/L 浓盐酸 pH 约为 −1，10 mol/L 浓烧碱 pH 约为 15；pH < 0 时改用哈米特酸度函数 H₀ 丈量",
                size=10.9,
                weight="600",
                fill=INK,
                anchor="middle",
            ),
        ]
    )
    return figure(
        760,
        520,
        "日常物质酸碱度pH全景标尺、紫甘蓝花青素变色与奥拉超强酸魔酸原理图",
        "展示从负值超强酸到pH 14强碱的对数标尺，解释紫甘蓝花青素随质子得失变色的共轭原理及乔治·奥拉魔酸质子化烷烃溶解蜡烛的诺奖发现。",
        body,
    )


@register("acid-base-causes", "酸碱性质的底层原因：质子接力、三代统一与分子结构开关", "化学与物质")
def build_all() -> list[str]:
    return [
        write_svg(SUBDIR, "grotthuss-proton-relay-anim.svg", build_grotthuss_proton_relay_anim()),
        write_svg(SUBDIR, "three-generations-acid-base-map.svg", build_three_generations_acid_base_map()),
        write_svg(SUBDIR, "four-atomic-switches-of-acidity.svg", build_four_atomic_switches_of_acidity()),
        write_svg(SUBDIR, "titration-and-blood-buffer-curves.svg", build_titration_and_blood_buffer_curves()),
        write_svg(SUBDIR, "everyday-ph-and-magic-acid-scale.svg", build_everyday_ph_and_magic_acid_scale()),
    ]
