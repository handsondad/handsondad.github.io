"""Visuals for '家里养的花为什么插土、泡水、播种、嫁接各显神通' (home-plant-propagation).

Generates 5 original 760px Chinese SVG diagrams with biological & quantitative assertions:
1. propagation-panorama-switch.svg — 4 home propagation modes + totipotency + Skoog-Miller (1957) hormone seesaw
2. stem-leaf-water-anatomy.svg     — Polar auxin node rooting, chimera leaf-cutting trap & water-root aerenchyma (10,000x O2 gap)
3. seed-lottery-vs-clone.svg       — Heterozygous apple seed reshuffling ((1/2)^n lottery) vs vegetative cloning
4. graft-cambium-healing-anim.svg  — Cambium alignment rule + Melnyk (2015) 7-day phloem-then-xylem healing animation
5. home-plant-cheatsheet.svg       — 4-column practical guide for 16 common household flowers & balcony fruit trees
"""

from __future__ import annotations

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
    txt,
    write_svg,
)

TOPIC = "home-plant-propagation"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#ecfdf5"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"

EXTRA_ARROWS = f"""
  <marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{RED}"/>
  </marker>
  <marker id="arr-teal" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{TEAL}"/>
  </marker>
  <marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{PURPLE}"/>
  </marker>
"""

# ---------------------------------------------------------------------------
# Quantitative & physiological model constants
# ---------------------------------------------------------------------------
D_O2_AIR_M2_S = 2.0e-5       # O2 molecular diffusivity in air (~20 °C), m²/s
D_O2_WATER_M2_S = 2.0e-9     # O2 molecular diffusivity in water (~20 °C), m²/s
O2_DIFFUSION_RATIO = D_O2_AIR_M2_S / D_O2_WATER_M2_S  # 10,000x

# Mendelian heterozygous genotype retention probability for n independent Aa loci
PROB_HET_5 = 0.5**5          # 3.125% for just 5 loci
PROB_HET_20 = 0.5**20        # < 1 in a million for 20 loci

# Melnyk et al. (2015, Current Biology) measured graft healing timeline (DAG = days after grafting)
DAG_TOTAL = 7.0
DAG_ADHESION = 2.0           # Tissue attachment within 1–2 DAG
DAG_PHLOEM = 3.5             # Phloem reconnection at 3–4 DAG
DAG_ROOT_RESUME = 5.0        # Root growth resumes ~5 DAG
DAG_XYLEM = 6.5              # Xylem reconnection at 6–7 DAG


def verify_plant_propagation_math() -> None:
    assert abs(O2_DIFFUSION_RATIO - 10000.0) < 1.0
    assert abs(PROB_HET_5 - 0.03125) < 1e-9
    assert PROB_HET_20 < 1e-6
    assert 0.0 < DAG_ADHESION < DAG_PHLOEM < DAG_ROOT_RESUME < DAG_XYLEM <= DAG_TOTAL


def badge(x: float, y: float, w: float, h: float, label: str, bg: str, fg: str) -> str:
    return pill(x, y, label, fg=fg, bg=bg, border=fg, w=w, h=h, size=11.5)


# ---------------------------------------------------------------------------
# 图 1：壁虎断尾只长尾巴，花草剪一截凭什么长成一整棵？（四大绝活 + 激素天平）
# ---------------------------------------------------------------------------
def build_propagation_panorama_switch() -> str:
    els = header(
        "图 1 · 阳台花草的“分身术”总账：为什么切一截枝叶就能重造整株植物？",
        "左看家庭养花四大繁殖路线；右看斯库格—米勒（1957）揭开的“生根 vs 长芽”定量激素天平",
    )

    # 左大卡：四大路线 2x2 网格
    els.append(card(20, 64, 368, 272))
    els.append(badge(34, 75, 224, 22, "阳台四大繁殖奇观（两条底层大路）", GREEN_SOFT, GREEN))

    modes = [
        (34, 108, "① 插土成活（扦插）", "月季插枝、多肉掰叶", "带茎节/叶基分生细胞 → 诱发不定根", GREEN_SOFT, GREEN),
        (208, 108, "② 丢水生根（水插）", "绿萝、富贵竹、龟背竹", "低氧刺激长出带通气孔道的白水根", BLUE_SOFT, BLUE),
        (34, 200, "③ 埋籽发芽（有性）", "向日葵、矮牵牛、香草", "花粉受精基因重洗，抗寒休眠越冬", ORANGE_SOFT, ORANGE),
        (208, 200, "④ 换头合体（嫁接）", "蟹爪兰接仙人掌、果树", "好果接穗 + 强根砧木，形成层焊通", PURPLE_SOFT, PURPLE),
    ]
    for mx, my, mtitle, mex, mdesc, mbg, mfg in modes:
        els.append(card(mx, my, 164, 80, rx=8, fill=mbg, stroke=mfg))
        els.append(txt(mx + 10, my + 22, mtitle, 11.5, mfg, weight="700"))
        els.append(txt(mx + 10, my + 43, mex, 10.5, INK, weight="600"))
        els.append(txt(mx + 10, my + 63, mdesc, 9.5, BODY))

    els.append(txt(34, 304, "• 无性克隆阵营（①②④）：有丝分裂原样复制，100% 锁死母株花色与甜度", 10, INK, weight="600"))
    els.append(txt(34, 323, "• 有性洗牌阵营（③）：减数分裂 + 授粉重组，适合一年生草花与选育新品种", 10, BODY))

    # 右大卡：细胞全能性 + 斯库格-米勒 1957 激素比值天平
    els.append(card(404, 64, 336, 272))
    els.append(badge(418, 75, 272, 22, "底层总开关：细胞全能性 + 激素配比天平", BLUE_SOFT, BLUE))

    els.append(txt(418, 114, "植物活细胞保留全套基因组（全能性 Totipotency）：", 10.5, INK, weight="700"))
    els.append(txt(418, 132, "受伤后可“脱分化”退回愈伤组织，再按激素比值重造器官！", 10, BODY))

    # 三档定量激素结果条（Skoog & Miller, 1957）
    rows = [
        (150, "生长素 IAA 高  >  细胞分裂素 低", "→ 专心往下【生根】", TEAL_SOFT, TEAL, "扦插蘸生根粉原理"),
        (206, "生长素 IAA  ≈  细胞分裂素 均衡", "→ 增殖【愈伤组织】", AMBER_SOFT, AMBER, "嫁接切口填缝架桥"),
        (262, "生长素 IAA 低  <  细胞分裂素 高", "→ 唤醒往上【长芽】", PURPLE_SOFT, PURPLE, "叶插冒芽/分枝促芽"),
    ]
    for ry, rcond, rout, rbg, rfg, rnote in rows:
        els.append(card(418, ry, 308, 46, rx=7, fill=rbg, stroke=rfg))
        els.append(txt(428, ry + 19, rcond, 10.5, INK, weight="700"))
        els.append(txt(428, ry + 37, f"{rout}（{rnote}）", 10, rfg, weight="700"))

    els.append(txt(418, 325, "出处：Skoog & Miller (1957) 经典烟草茎段再生定量实验", 9.5, MUTED))

    # 底部通栏：为什么壁虎断尾长不出第二只壁虎，绿萝剪十段能变十盆？
    els.append(card(20, 348, 720, 38, fill=GREEN_SOFT, stroke=GREEN))
    els.append(
        txt(
            36,
            372,
            "动物细胞分化后大多锁死命运；植物不能跑路躲天敌，演化出了遍布茎节的分生组织与“切碎也能重开一局”的再生超能力！",
            11,
            INK,
            weight="600",
        )
    )

    return figure(
        398,
        "家庭养花四大繁殖方式与植物细胞全能性及激素比值调控开关图解",
        "左栏归纳扦插、水插、播种与嫁接四条繁殖路线及其无性克隆与有性重组归属；右栏展示1957年斯库格与米勒发现的生长素与细胞分裂素比值决定生根、愈伤组织或长芽的定量机制。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 2：土插为什么要留“节”且不能倒插？水插大白根下土为什么容易死？
# ---------------------------------------------------------------------------
def build_stem_leaf_water_anatomy() -> str:
    els = header(
        "图 2 · 插土与泡水的微观真相：茎节“激素单行道”、虎皮兰丢金边与水根“潜水管”",
        "左看为什么枝条插反必死、金边虎皮兰叶插变纯绿；右看水中缺氧 10,000 倍造出的两套根系",
    )

    # 左卡：茎插极性 + 叶插嵌合体彩蛋
    els.append(card(20, 64, 356, 314))
    els.append(badge(34, 75, 246, 22, "土插密码：生长素单行道与“茎节”生死线", GREEN_SOFT, GREEN))

    # 正插成活示意 (x=96)
    els.append(card(34, 106, 158, 152, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    els.append(txt(113, 124, "✓ 顺向正插（带茎节）", 10.5, GREEN, "middle", weight="700"))
    # 土壤面
    els.append(f'<line x1="44" y1="196" x2="182" y2="196" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="4,3"/>')
    els.append(txt(58, 191, "土面", 9.5, AMBER, weight="600"))
    # 茎秆 + 上下两节
    els.append(f'<rect x="108" y="136" width="10" height="96" rx="3" fill="{GREEN}"/>')
    els.append(f'<line x1="104" y1="162" x2="122" y2="162" stroke="{INK}" stroke-width="2"/>')
    els.append(f'<line x1="104" y1="214" x2="122" y2="214" stroke="{INK}" stroke-width="2"/>')
    # 上节腋芽抽新叶
    els.append(f'<path d="M 118 160 Q 140 144 150 154 Q 136 168 118 162 Z" fill="{GREEN}" stroke="{INK}" stroke-width="0.9"/>')
    els.append(txt(144, 150, "腋芽抽叶", 9.2, GREEN, weight="700"))
    # 极性运输向下箭头
    els.append(f'<line x1="96" y1="146" x2="96" y2="210" stroke="{ORANGE}" stroke-width="2.0" marker-end="url(#arr-orange)"/>')
    els.append(txt(68, 176, "IAA↓", 9.5, ORANGE, "middle", weight="700"))
    # 下节长出不定根
    els.append(f'<path d="M 108 216 Q 86 226 78 242 M 118 216 Q 140 226 148 242 M 113 228 L 113 246" fill="none" stroke="{TEAL}" stroke-width="1.8"/>')
    els.append(txt(113, 253, "节部冒出不定根", 9.5, TEAL, "middle", weight="700"))

    # 倒插失败示意 (x=276)
    els.append(card(204, 106, 158, 152, rx=8, fill=RED_SOFT, stroke=RED))
    els.append(txt(283, 124, "✗ 上下倒插（必枯死）", 10.5, RED, "middle", weight="700"))
    els.append(f'<line x1="214" y1="196" x2="352" y2="196" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="4,3"/>')
    els.append(f'<rect x="278" y="136" width="10" height="96" rx="3" fill="{SLATE}"/>')
    # 即使倒放，IAA 仍往原本的形态学下端（此时朝天！）运送
    els.append(f'<line x1="266" y1="212" x2="266" y2="148" stroke="{RED}" stroke-width="2.0" marker-end="url(#arr-red)"/>')
    els.append(txt(238, 180, "IAA仍往", 9.5, RED, "middle", weight="700"))
    els.append(txt(238, 192, "原根端运", 9.5, RED, "middle", weight="700"))
    els.append(txt(283, 232, "土下无激素难生根", 9.5, RED, "middle", weight="600"))
    els.append(txt(283, 248, "切口腐烂黑杆！", 9.5, BODY, "middle"))

    # 左下：叶插限制与金边虎皮兰嵌合体冷知识
    els.append(card(34, 268, 328, 98, rx=8, fill=AMBER_SOFT, stroke=AMBER))
    els.append(txt(46, 288, "叶插两大奇观（多肉/海棠能活，月季单叶变“僵尸叶”）：", 10.5, AMBER, weight="700"))
    els.append(txt(46, 308, "• 月季/绿萝单叶无腋芽，偶能生根却抽不出茎芽，成不了新株；", 10, INK))
    els.append(txt(46, 327, "• 金边虎皮兰是“周缘嵌合体”：叶插新芽只从内部纯绿细胞层", 10, INK))
    els.append(txt(46, 345, "  冒出，金边100%消失！想保住金边必须连地下根状茎【分株】。", 10, RED, weight="700"))

    # 右卡：水插 vs 土插根系横切面与 10,000 倍氧气差
    els.append(card(392, 64, 348, 314))
    els.append(badge(406, 75, 274, 22, "水插玄机：水中氧气慢 1 万倍，逼出“潜水根”", BLUE_SOFT, BLUE))

    els.append(txt(406, 113, "水中 O₂ 扩散比空气慢约 10,000 倍，25°C 静水溶氧仅 ~8 mg/L：", 10, INK, weight="700"))

    # 水生根横切面 (左圆 cx=482, cy=182)
    els.append(card(406, 124, 154, 146, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    els.append(txt(483, 142, "水生根（白、粗、脆）", 10.5, BLUE, "middle", weight="700"))
    els.append(f'<circle cx="483" cy="188" r="32" fill="#ffffff" stroke="{BLUE}" stroke-width="2.0"/>')
    # 一圈莲藕式通气孔道 (Aerenchyma)
    for ang_deg in range(0, 360, 60):
        import math
        rad = math.radians(ang_deg)
        ax = 483 + 19 * math.cos(rad)
        ay = 188 + 19 * math.sin(rad)
        els.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="6.2" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.2"/>')
    els.append(f'<circle cx="483" cy="188" r="7" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="1.4"/>')
    els.append(txt(483, 236, "• 皮层充满通气孔道输氧", 9.5, BLUE, "middle", weight="700"))
    els.append(txt(483, 252, "• 几乎无根毛，木质化极弱", 9.5, BODY, "middle"))

    # 土生根横切面 (右圆 cx=649, cy=188)
    els.append(card(572, 124, 154, 146, rx=8, fill=TEAL_SOFT, stroke=TEAL))
    els.append(txt(649, 142, "土生根（黄褐、韧、密毛）", 10.5, TEAL, "middle", weight="700"))
    # 外圈密集根毛
    for ang_deg in range(0, 360, 20):
        import math
        rad = math.radians(ang_deg)
        x1 = 649 + 30 * math.cos(rad)
        y1 = 188 + 30 * math.sin(rad)
        x2 = 649 + 41 * math.cos(rad)
        y2 = 188 + 41 * math.sin(rad)
        els.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{TEAL}" stroke-width="1.3"/>')
    els.append(f'<circle cx="649" cy="188" r="30" fill="#fef3c7" stroke="{AMBER}" stroke-width="2.4"/>')
    els.append(f'<circle cx="649" cy="188" r="9" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="1.6"/>')
    els.append(txt(649, 236, "• 外表木质化耐摩擦抗旱", 9.5, TEAL, "middle", weight="700"))
    els.append(txt(649, 252, "• 亿万根毛把吸水面扩百倍", 9.5, BODY, "middle"))

    # 右下：水培转土培保命指南
    els.append(card(406, 280, 320, 86, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    els.append(txt(418, 300, "水培苗移栽进土“不死口诀”：", 10.5, GREEN, weight="700"))
    els.append(txt(418, 320, "① 黄金窗口：水根刚长到 2～5 cm 时就下土（别等长满一瓶！）", 10, INK, weight="600"))
    els.append(txt(418, 339, "② 泥浆过渡：头 10 天保持盆土微湿偏润，诱发带根毛的新土根", 10, INK))
    els.append(txt(418, 357, "③ 纯水培秘诀：水位只淹没 1/3～1/2 根系，留上半截在空气呼吸", 10, BLUE, weight="600"))

    return figure(
        392,
        "茎插生长素极性运输、金边虎皮兰嵌合体叶插退化与水生根通气组织解剖对比图",
        "左栏对比顺向正插在茎节处汇集生长素生根发芽、倒插因极性运输反向而枯死，并解释金边虎皮兰叶插丢失金边的周缘嵌合体机制；右栏展示水中氧气扩散慢一万倍诱导水生根形成莲藕状通气孔道且无根毛，给出2至5厘米水转土黄金窗口。",
        els,
        extra_defs=EXTRA_ARROWS,
    )


# ---------------------------------------------------------------------------
# 图 3：为什么吃完的苹果、车厘子吐籽种不出原味甜果？（基因洗牌盲盒 vs 克隆）
# ---------------------------------------------------------------------------
def build_seed_lottery_vs_clone() -> str:
    els = header(
        "图 3 · 吃完红富士吐籽种下去，为什么结不出红富士？（有性基因洗牌 vs 无性克隆）",
        "果树与名贵花卉高度“杂合”，减数分裂会把好基因拆散重洗；想原样复刻必须靠扦插或嫁接克隆",
    )

    # 左卡：有性播种——基因重洗大盲盒
    els.append(card(20, 64, 360, 272))
    els.append(badge(34, 75, 258, 22, "有性繁殖（播种）：基因洗牌开盲盒", ORANGE_SOFT, ORANGE))

    els.append(card(34, 108, 332, 62, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    els.append(txt(46, 128, "母本：红富士苹果树（基因高度杂合 AaBbCcDdEe…）", 10.5, ORANGE, weight="700"))
    els.append(txt(46, 147, "+ 苹果具 S 位点“自交不亲和”，必须借另一品种花粉异花授粉！", 10, INK, weight="600"))
    els.append(txt(46, 163, "↓ 减数分裂配子重组：甜度、脆度、果个、抗病等位基因彻底打乱", 9.5, BODY))

    # 概率定量核算框
    els.append(card(34, 180, 332, 86, rx=8, fill=CARD_BG, stroke=BORDER))
    els.append(txt(46, 200, "就算只盯 5 对独立杂合优良基因（AaBbCcDdEe）：", 10.5, INK, weight="700"))
    # 画 5 个基因位点小方块 + 概率条
    loci = ["甜 Aa", "脆 Bb", "大 Cc", "红 Dd", "香 Ee"]
    for idx, loc in enumerate(loci):
        lx = 46 + idx * 62
        els.append(card(lx, 209, 56, 22, rx=5, fill=AMBER_SOFT, stroke=AMBER))
        els.append(txt(lx + 28, 224, loc, 9.5, AMBER, "middle", weight="700"))
    els.append(txt(46, 252, f"• 5 对全保住原杂合组合概率：(1/2)⁵ = {PROB_HET_5 * 100:.2f}%（32 棵里才 1 棵）", 10, RED, weight="700"))

    els.append(txt(34, 286, "• 真实苹果有数万基因位点：实生苗结同款好果概率几乎为 0（八成酸涩小果）", 9.8, INK, weight="600"))
    els.append(txt(34, 305, "• 还要苦熬 6～10 年“童期”才开花；F₁ 杂交草花自留种 F₂ 也会花色退化", 9.8, BODY))
    els.append(txt(34, 324, "★ 种子真正强项：选育全新超级品种 + 挡住多数母本病毒 + 干籽抗寒越冬！", 9.8, GREEN, weight="700"))

    # 右卡：无性克隆——Ctrl+C 原样复刻 + 跨过童期
    els.append(card(396, 64, 344, 272))
    els.append(badge(410, 75, 258, 22, "无性繁殖（扦插/分株/嫁接）：100% 基因锁死", BLUE_SOFT, BLUE))

    els.append(card(410, 108, 316, 62, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    els.append(txt(422, 128, "全世界所有“红富士”苹果、所有“阳光玫瑰”葡萄：", 10.5, BLUE, weight="700"))
    els.append(txt(422, 147, "本质上都是最初那 1 棵传奇母树剪枝嫁接出来的“克隆分身”！", 10, INK, weight="600"))
    els.append(txt(422, 163, "只走有丝分裂（不经减数分裂洗牌），DNA 与果味 100% 原样复刻", 9.5, BODY))

    # 挂果年限硬核对比条（实生苗 8 年 vs 嫁接成年枝 2.5 年）
    els.append(card(410, 180, 316, 86, rx=8, fill=CARD_BG, stroke=BORDER))
    els.append(txt(422, 200, "挂果等待时间对比（为什么果农绝不拿种子种果园）：", 10.5, INK, weight="700"))

    els.append(txt(422, 222, "苹果籽实生苗", 9.5, ORANGE, weight="700"))
    els.append(f'<rect x="502" y="212" width="176" height="12" rx="3" fill="{ORANGE}"/>')
    els.append(txt(684, 222, "6～10 年", 9.5, ORANGE, weight="700"))

    els.append(txt(422, 246, "成年枝条嫁接", 9.5, GREEN, weight="700"))
    els.append(f'<rect x="502" y="236" width="55" height="12" rx="3" fill="{GREEN}"/>')
    els.append(txt(564, 246, "2～3 年挂果（跳过童期！）", 9.5, GREEN, weight="700"))

    els.append(txt(410, 286, "• 成熟枝条早已度过“生理童期”，接活后直接延续成年开花记忆", 9.8, INK, weight="600"))
    els.append(txt(410, 305, "• 三倍体无籽西瓜、华盛顿脐橙、香蕉连饱满种子都没有，全靠克隆传代", 9.8, BODY))
    els.append(txt(410, 324, "⚠ 软肋：基因完全一致，遇新型病害易同批中招（如香蕉枯萎病）", 9.5, RED, weight="600"))

    # 底部通栏
    els.append(card(20, 348, 720, 38, fill=TEAL_SOFT, stroke=TEAL))
    els.append(
        txt(
            36,
            372,
            "一句话总结：想“开盲盒创奇迹、一年一播省心越冬”播种子；想“原封不动留住神仙颜值与甜脆口感”必须走扦插或嫁接！",
            11,
            INK,
            weight="600",
        )
    )

    return figure(
        398,
        "有性繁殖种子基因杂合重组盲盒与无性克隆100%复刻性状及童期对比图",
        "左栏定量展示高度杂合的苹果经异花授粉与减数分裂重组后，仅5对杂合位点保住原组合概率就低至3.12%，实生苗需熬6至10年童期且果味退化；右栏展示扦插与嫁接通过有丝分裂100%锁死优良风味并跳过童期在2至3年挂果。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 4：嫁接“一线生死”形成层对齐 + 7 天血管重连实测时序单次动画
# ---------------------------------------------------------------------------
def build_graft_cambium_healing_anim() -> str:
    # 严格按 Melnyk et al. (2015, Current Biology) 拟南芥实测 0→7 DAG 时间比例：
    # 1 DAG = 0.75 s，总时长 5.25 s，播放 1 次并停在完整接通终态；支持 prefers-reduced-motion: reduce
    dur = 5.25
    delay = 0.40

    # 关键生理节点占 7 天总时长的精确百分比：
    # Day 0..1.5 (0%..21%): 黏附开始；Day 2..3 (29%..43%): 愈伤组织团扩张填缝；
    # Day 3..4 (43%..57%): 韧皮部率先接通（橙色脉冲桥长通）；
    # Day 6..7 (86%..100%): 木质部导管最后接通（蓝色水流桥长通）！
    extra_css = f"""
  @keyframes callusGrow {{
    0%   {{ transform: scale(0.08); opacity: 0.15; }}
    20%  {{ transform: scale(0.35); opacity: 0.55; }}
    43%  {{ transform: scale(1.00); opacity: 1.00; }}
    100% {{ transform: scale(1.00); opacity: 1.00; }}
  }}
  @keyframes phloemBridge {{
    0%, 38%  {{ stroke-dashoffset: 68; opacity: 0.15; }}
    57%      {{ stroke-dashoffset: 0;  opacity: 1.00; }}
    100%     {{ stroke-dashoffset: 0;  opacity: 1.00; }}
  }}
  @keyframes xylemBridge {{
    0%, 78%  {{ stroke-dashoffset: 68; opacity: 0.15; }}
    100%     {{ stroke-dashoffset: 0;  opacity: 1.00; }}
  }}
  @keyframes progressCursor {{
    0%   {{ transform: translateX(-276px); }}
    100% {{ transform: translateX(0px); }}
  }}
  .callus-anim {{
    transform-box: fill-box;
    transform-origin: center;
    animation: callusGrow {dur}s linear {delay}s 1 backwards;
  }}
  .phloem-anim {{
    stroke-dasharray: 68;
    stroke-dashoffset: 0;
    animation: phloemBridge {dur}s linear {delay}s 1 backwards;
  }}
  .xylem-anim {{
    stroke-dasharray: 68;
    stroke-dashoffset: 0;
    animation: xylemBridge {dur}s linear {delay}s 1 backwards;
  }}
  .cursor-anim {{
    animation: progressCursor {dur}s linear {delay}s 1 backwards;
  }}
  @media (prefers-reduced-motion: reduce) {{
    .callus-anim, .phloem-anim, .xylem-anim, .cursor-anim {{ animation: none !important; }}
  }}
"""

    els = header(
        "图 4 · 果树嫁接的“一线生死”与血管重连动画：为什么先通韧皮部、后通木质部？",
        "左看横切面“维管形成层对齐”铁律与单子叶死穴；右按 Melnyk (2015) 实测 7 天时序单次演示愈合",
    )

    # 左卡：砧粗穗细的横切面对齐法则 + 单子叶散生维管束反例
    els.append(card(20, 64, 344, 316))
    els.append(badge(34, 75, 256, 22, "刀口成败只在 0.1 毫米：维管形成层对齐", PURPLE_SOFT, PURPLE))

    # 错误：居中插（两边形成层全错开）
    els.append(card(34, 108, 152, 138, rx=8, fill=RED_SOFT, stroke=RED))
    els.append(txt(110, 126, "✗ 贪图居中（形成层错位）", 10, RED, "middle", weight="700"))
    # 粗砧木横切圆 (cx=110, cy=176, r=36)
    els.append(f'<circle cx="110" cy="176" r="36" fill="#fde68a" stroke="#92400e" stroke-width="3.0"/>')
    els.append(f'<circle cx="110" cy="176" r="29" fill="#fef9c3" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="4,2"/>')
    # 细接穗居中 (cx=110, cy=176, r=15) -> 绿色形成层圈完全悬空在木质部里！
    els.append(f'<circle cx="110" cy="176" r="16" fill="#ffffff" stroke="#92400e" stroke-width="2.0"/>')
    els.append(f'<circle cx="110" cy="176" r="12" fill="#eff6ff" stroke="{GREEN}" stroke-width="2.0"/>')
    els.append(txt(110, 226, "细穗插在死木芯里", 9.5, RED, "middle", weight="700"))
    els.append(txt(110, 240, "绿圈互不接触 → 必死！", 9.5, BODY, "middle"))

    # 正确：偏靠一侧（右侧形成层严丝合缝贴合！）
    els.append(card(198, 108, 152, 138, rx=8, fill=GREEN_SOFT, stroke=GREEN))
    els.append(txt(274, 126, "✓ 偏靠一侧（形成层吻合）", 10, GREEN, "middle", weight="700"))
    els.append(f'<circle cx="274" cy="176" r="36" fill="#fde68a" stroke="#92400e" stroke-width="3.0"/>')
    els.append(f'<circle cx="274" cy="176" r="29" fill="#fef9c3" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="4,2"/>')
    # 细接穗偏右，使其 r=12 绿圈与砧木 r=29 绿圈在 x=303 处精准内切吻合！(cx = 274 + 17 = 291)
    els.append(f'<circle cx="291" cy="176" r="16" fill="#ffffff" stroke="#92400e" stroke-width="2.0"/>')
    els.append(f'<circle cx="291" cy="176" r="12" fill="#eff6ff" stroke="{GREEN}" stroke-width="2.2"/>')
    els.append(f'<circle cx="303" cy="176" r="4.5" fill="{GREEN}"/>')
    els.append(txt(274, 226, "至少一侧绿圈贴紧", 9.5, GREEN, "middle", weight="700"))
    els.append(txt(274, 240, "分裂愈伤 → 100% 能活！", 9.5, BODY, "middle"))

    # 左下：为什么竹子、玉米成年茎不能常规劈接？
    els.append(card(34, 256, 316, 112, rx=8, fill=SLATE_SOFT, stroke=SLATE))
    els.append(txt(46, 276, "为什么竹子、玉米、百合不能拿刀随便劈接？", 10.5, INK, weight="700"))
    # 小圆示意满天星散生维管束
    els.append(f'<circle cx="72" cy="316" r="24" fill="#ffffff" stroke="{SLATE}" stroke-width="1.8"/>')
    for bx, by in [(64, 306), (78, 304), (60, 318), (73, 316), (84, 319), (66, 329), (79, 328)]:
        els.append(f'<circle cx="{bx}" cy="{by}" r="2.6" fill="{ORANGE}"/>')
    els.append(txt(106, 302, "• 双子叶（果树/月季/番茄）：形成层连成整圈环", 9.8, GREEN, weight="700"))
    els.append(txt(106, 321, "• 单子叶（竹/玉米/棕榈）：维管束满天星散生，", 9.8, INK))
    els.append(txt(106, 338, "  成年茎干无形成层环，常规枝接无法愈合！", 9.8, RED, weight="700"))
    els.append(txt(106, 356, "  （仅种子萌发胚胎期可显微嫁接，Nature 2021）", 9.2, MUTED))

    # 右卡：纵切面血管重连单次动画 + 7 天里程碑进度轴
    els.append(card(380, 64, 360, 316))
    els.append(badge(394, 75, 294, 22, "接口愈合 4 步曲（先通运糖管，再通抽水管！）", BLUE_SOFT, BLUE))

    # 纵切面示意框 (x=394..554, y=108..288)
    els.append(card(394, 108, 162, 180, rx=8, fill="#f8fafc", stroke=BORDER))
    # 上半段：接穗 Scion
    els.append(f'<rect x="440" y="118" width="70" height="68" rx="4" fill="#dcfce7" stroke="{GREEN}" stroke-width="1.6"/>')
    els.append(txt(475, 134, "接穗 (好果枝)", 9.5, GREEN, "middle", weight="700"))
    # 下半段：砧木 Rootstock
    els.append(f'<rect x="440" y="208" width="70" height="68" rx="4" fill="#fef3c7" stroke="{AMBER}" stroke-width="1.6"/>')
    els.append(txt(475, 266, "砧木 (强根系)", 9.5, AMBER, "middle", weight="700"))

    # 上下原有维管管道（两侧橙色韧皮部，中间蓝色木质部）
    for px in (452, 498):
        els.append(f'<line x1="{px}" y1="142" x2="{px}" y2="184" stroke="{ORANGE}" stroke-width="3.0"/>')
        els.append(f'<line x1="{px}" y1="210" x2="{px}" y2="250" stroke="{ORANGE}" stroke-width="3.0"/>')
    for xx in (469, 481):
        els.append(f'<line x1="{xx}" y1="142" x2="{xx}" y2="184" stroke="{BLUE}" stroke-width="3.2"/>')
        els.append(f'<line x1="{xx}" y1="210" x2="{xx}" y2="250" stroke="{BLUE}" stroke-width="3.2"/>')

    # 接口中央：愈伤组织团（动画扩张填满 y=184..210 缝隙）
    els.append(
        f'<ellipse class="callus-anim" cx="475" cy="197" rx="40" ry="15" '
        f'fill="#fbcfe8" stroke="#db2777" stroke-width="1.4"/>'
    )
    # 动画搭桥 1：韧皮部桥（两侧橙色曲线，Day 3-4 率先连通，向下运糖/IAA）
    els.append(
        f'<path class="phloem-anim" d="M 452 182 C 446 192, 446 202, 452 212" '
        f'fill="none" stroke="{ORANGE}" stroke-width="3.2"/>'
    )
    els.append(
        f'<path class="phloem-anim" d="M 498 182 C 504 192, 504 202, 498 212" '
        f'fill="none" stroke="{ORANGE}" stroke-width="3.2"/>'
    )
    # 动画搭桥 2：木质部导管桥（中间蓝色桥，Day 6-7 最后连通，向上供水）
    els.append(
        f'<path class="xylem-anim" d="M 469 182 C 467 194, 467 200, 469 212" '
        f'fill="none" stroke="{BLUE}" stroke-width="3.4"/>'
    )
    els.append(
        f'<path class="xylem-anim" d="M 481 182 C 483 194, 483 200, 481 212" '
        f'fill="none" stroke="{BLUE}" stroke-width="3.4"/>'
    )
    els.append(txt(475, 201, "愈伤桥", 9.0, "#9d174d", "middle", weight="700"))

    # 右侧四步文字时间卡 (x=566..728)
    steps = [
        (112, "① 第1–2天：果胶黏附", "切口细胞膨胀粘连固定", SLATE),
        (156, "② 第2–3天：愈伤架桥", "形成层分裂填满接口缝隙", "#be185d"),
        (200, "③ 第3–4天：韧皮部先通", "接穗往下运糖与生长素！", ORANGE),
        (244, "④ 第6–7天：木质部焊通", "根系往上抽水，恢复抗旱！", BLUE),
    ]
    for sy, st, sd, sc in steps:
        els.append(txt(566, sy + 13, st, 10, sc, weight="700"))
        els.append(txt(566, sy + 29, sd, 9.5, BODY))

    # 底部 0→7 天等比进度尺（木本果树对应约 2～4 周，次序完全一致）
    els.append(card(394, 298, 332, 70, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    els.append(txt(408, 316, "实测生理进度轴（拟南芥天 / 木本果树同序放大为 2～4 周）：", 9.5, INK, weight="700"))
    # 轴线 x: 422 -> 698 (长 276 px)
    els.append(f'<line x1="422" y1="336" x2="698" y2="336" stroke="{SLATE}" stroke-width="2.2"/>')
    for d_val, d_lbl, d_col in [
        (0.0, "0d 切接", MUTED),
        (2.0, "2d 愈伤", "#be185d"),
        (3.5, "3.5d 韧皮通", ORANGE),
        (6.5, "6.5d 木质通", BLUE),
    ]:
        dx = 422 + (d_val / 7.0) * 276.0
        els.append(f'<circle cx="{dx:.1f}" cy="336" r="3.5" fill="{d_col}"/>')
        els.append(txt(dx, 355, d_lbl, 9.2, d_col, "middle", weight="700"))
    # 终态位于 x=698 的游标圆点
    els.append(f'<g class="cursor-anim"><circle cx="698" cy="336" r="5.5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/></g>')

    return figure(
        394,
        "果树嫁接维管形成层对齐铁律与韧皮部木质部7天分步重连动画图解",
        "左栏对比砧粗穗细时居中错位必死与偏靠一侧形成层贴合成活，并指出单子叶植物维管束散生缺乏形成层环；右栏依据Melnyk等2015年实测时序单次动画演示第1至2天黏附、第2至3天愈伤架桥、第3至4天韧皮部率先接通运糖、第6至7天木质部导管贯通供水。",
        els,
        extra_css=extra_css,
    )


# ---------------------------------------------------------------------------
# 图 5：家里常见的 16 种花果到底该怎么繁？四大家族一图对号入座
# ---------------------------------------------------------------------------
def build_home_plant_cheatsheet() -> str:
    els = header(
        "图 5 · 阳台实战速查卡：家里养的 16 种花草果木，选哪招繁殖成功率最高？",
        "按植物器官构造对号入座，避开“月季插单叶、水根太长下土、金边虎皮兰叶插”三大新手坑",
    )

    cols = [
        (
            "剪段枝条·水插/土插",
            "自带茎节与潜伏根原基",
            GREEN,
            GREEN_SOFT,
            [
                ("绿萝 / 龟背竹", "带气生根茎节剪下，泡水或插蛭石 7 天冒白根"),
                ("吊兰 / 草莓", "直接剪走茎“小吊兰”（自带气根），沾土即活"),
                ("月季 / 绣球", "选半木质化枝留 2 节+2 半叶，蛭石保湿生根"),
                ("茉莉 / 栀子", "梅雨季剪当年壮枝，水插露半根或沙插最稳"),
            ],
            "避坑：必须留“节”且顺向正插！",
        ),
        (
            "掰片叶子·叶插/分株",
            "叶基/叶脉具双器官再生力",
            TEAL,
            TEAL_SOFT,
            [
                ("景天多肉(玉露/桃蛋)", "左右轻晃掰下完整叶片（保住生长点），晾干平放"),
                ("落地生根(不死鸟)", "叶缘锯齿直接长满带根小苗，落地就成一片"),
                ("非洲堇 / 大岩桐", "带叶柄插进珍珠岩或浅水，叶基同时冒根冒芽"),
                ("虎皮兰 / 秋海棠", "纯绿虎皮兰可切叶插；金边虎皮兰必须【分株】！"),
            ],
            "避坑：多肉叶插未出根前别浇水！",
        ),
        (
            "春播秋播·种子育苗",
            "一年生草花与快手阳台菜",
            ORANGE,
            ORANGE_SOFT,
            [
                ("向日葵 / 百日草", "大粒种子温水浸种点播，向阳猛晒 60 天开花"),
                ("矮牵牛 / 三色堇", "细小好光种子撒土表别埋深！喷雾保湿发芽"),
                ("罗勒 / 薄荷 / 香菜", "香草播种无病毒活力旺（薄荷长大后可无限水插）"),
                ("樱桃萝卜 / 小白菜", "十字花科 3 天破土，最适合带娃观察子叶真叶"),
            ],
            "避坑：F₁杂交名花别自留二代籽！",
        ),
        (
            "强强联手·换头嫁接",
            "同科近亲形成层贴合锁紧",
            PURPLE,
            PURPLE_SOFT,
            [
                ("蟹爪兰 → 仙人掌", "同属仙人掌科！削去表皮插进仙人掌肉质茎防烂根"),
                ("苹果 → 矮化海棠", "海棠抗寒矮化控树高，接富士枝 2～3 年阳台挂果"),
                ("名品月季 → 野蔷薇", "野蔷薇根系狂野，高位芽接养成“棒棒糖树状月季”"),
                ("西瓜 → 南瓜砧木", "葫芦科换根绝招：彻底防住重茬枯萎病且耐寒高产"),
            ],
            "避坑：包严保湿度 + 抹掉砧木野芽！",
        ),
    ]

    w_col = 172
    gap = 10
    x_start = 20

    for idx, (ctitle, csub, cfg, cbg, items, cpit) in enumerate(cols):
        cx = x_start + idx * (w_col + gap)
        els.append(card(cx, 64, w_col, 314, rx=10, fill=CARD_BG, stroke=cfg, sw=1.3))
        els.append(card(cx + 6, 70, w_col - 12, 42, rx=7, fill=cbg, stroke=cfg))
        els.append(txt(cx + w_col / 2, 88, ctitle, 11, cfg, "middle", weight="700"))
        els.append(txt(cx + w_col / 2, 104, csub, 9.2, BODY, "middle"))

        for j, (pname, ptip) in enumerate(items):
            iy = 120 + j * 54
            els.append(f'<line x1="{cx + 10}" y1="{iy}" x2="{cx + w_col - 10}" y2="{iy}" stroke="{HAIRLINE}" stroke-width="1"/>')
            els.append(txt(cx + 10, iy + 17, f"• {pname}", 10, INK, weight="700"))
            # 自动拆分为两行每行约 15 字，确保绝不触碰卡片右壁
            line1 = ptip[:14]
            line2 = ptip[14:]
            els.append(txt(cx + 14, iy + 33, line1, 9.2, BODY))
            if line2:
                els.append(txt(cx + 14, iy + 46, line2, 9.2, BODY))

        els.append(card(cx + 6, 342, w_col - 12, 28, rx=6, fill=cbg, stroke=cfg))
        els.append(txt(cx + w_col / 2, 360, cpit, 9.2, cfg, "middle", weight="700"))

    return figure(
        390,
        "阳台16种常见花卉蔬果四大繁殖方式对号入座与新手避坑速查图",
        "四列卡片分别列出适合剪枝水插或土插、掰叶叶插或分株、春播秋播育苗、以及同科换头嫁接的16种家庭常见花果代表、操作要点与头号避坑口诀。",
        els,
    )


@register(TOPIC, "家庭养花四大繁殖方式、激素天平与果树嫁接形成层重连（5图）", "植物生理·园艺")
def build() -> list[str]:
    verify_plant_propagation_math()
    return [
        write_svg(TOPIC, "propagation-panorama-switch.svg", build_propagation_panorama_switch()),
        write_svg(TOPIC, "stem-leaf-water-anatomy.svg", build_stem_leaf_water_anatomy()),
        write_svg(TOPIC, "seed-lottery-vs-clone.svg", build_seed_lottery_vs_clone()),
        write_svg(TOPIC, "graft-cambium-healing-anim.svg", build_graft_cambium_healing_anim()),
        write_svg(TOPIC, "home-plant-cheatsheet.svg", build_home_plant_cheatsheet()),
    ]
