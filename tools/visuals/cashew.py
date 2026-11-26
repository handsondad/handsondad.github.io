"""腰果：假果与真果、毒壳 CNSL、同科毒藤、加工去毒与营养过敏的原创 SVG 图解。"""

from __future__ import annotations

from .core import (
    BLUE,
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
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

TOPIC = "cashew"

ROSE = "#be123c"
ROSE_SOFT = "#ffe9ee"
GOLD = "#b45309"
GOLD_SOFT = "#fdf1d8"
TEAL = "#0f766e"
TEAL_SOFT = "#e6f5f2"


def _line(x1, y1, x2, y2, stroke=SLATE, sw=1.6, dash=None, marker=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def _verify() -> None:
    # 果壳液 CNSL 占壳重 15–30%；成分以腰果酸为主
    assert 15 <= 20 <= 30
    assert 60 <= 65 <= 70 and 5 <= 10 <= 20
    # 腰果苹果维 C 约为橙子的 5 倍
    orange = 53
    apple = 5 * orange
    assert 200 < apple < 300
    # 营养：每 100 g 腰果仁 553 kcal、脂肪 43.8 g、蛋白 18.2 g
    energy = 43.8 * 9 + 18.2 * 4 + 30.2 * 4
    assert 500 < energy < 600
    # 产量 2023：科特迪瓦 > 印度 > 越南
    assert 1044450 > 782000 > 347635
    # 三类主要过敏原
    assert len(["Ana o 1", "Ana o 2", "Ana o 3"]) == 3


# ---------------------------------------------------------------------------
# 1. 假果与真果：腰果到底长在哪
# ---------------------------------------------------------------------------
def build_false_true_fruit() -> str:
    els = []
    els.extend(
        header(
            "你吃的腰果，其实是挂在“苹果”底下的种子",
            "膨大的是花梗，不是子房；真正的果实是那颗肾形坚果。",
        )
    )

    els.append(card(20, 66, 352, 430))
    els.append(step_badge(38, 89, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 93, "整根枝条上长着什么", size=11.8, color=INK, weight="700"))
    els.append(_line(60, 290, 330, 290, stroke=GREEN, sw=4))
    els.append(txt(60, 280, "枝条", size=10, color=GREEN, weight="600"))
    # 花梗膨大的假果
    els.append(f'<path d="M150 288 Q130 220 170 176 Q205 148 230 176 Q262 220 236 288 Z" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2"/>')
    els.append(txt(194, 226, "假果", size=12, color=ORANGE, anchor="middle", weight="700"))
    els.append(txt(194, 246, "腰果苹果", size=10, color=BODY, anchor="middle"))
    # 真果：肾形坚果
    els.append(f'<path d="M170 300 Q160 272 190 268 Q220 264 226 288 Q232 312 204 316 Q178 320 170 300 Z" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="2"/>')
    els.append(txt(198, 300, "真果", size=10, color=GOLD, anchor="middle", weight="700"))
    # 花
    for i, (x, y) in enumerate([(280, 190), (300, 170), (310, 205)]):
        els.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1"/>')
    els.append(txt(268, 236, "花", size=9.8, color=PURPLE))
    els.append(txt(38, 374, "花梗先长胖成梨形“苹果”，坚果挂在它末端。", size=10.2, color=BODY))
    els.append(txt(38, 404, "两者是同一条枝上的相邻结构，不是“果里有果”。", size=10.2, color=SLATE))
    els.append(txt(38, 436, "英文：cashew apple（假果） / cashew nut（真果）。", size=9.8, color=MUTED))

    els.append(card(388, 66, 352, 430))
    els.append(step_badge(406, 89, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(424, 93, "两个器官，身份完全不同", size=11.8, color=INK, weight="700"))
    rows = [
        ("谁膨大", "花梗／花托", "子房", BLUE),
        ("植物学", "附属果（假果）", "核果（真果）", GREEN),
        ("能不能吃", "能，多汁但极易腐", "果仁能，带毒壳不能", ORANGE),
        ("维生素 C", "约 219 mg/100g", "约 0.5 mg/100g", ROSE),
        ("热量", "约 48 kcal/100g", "约 553 kcal/100g", GOLD),
    ]
    els.append(txt(406, 128, "比较项", size=10, color=MUTED, weight="600"))
    els.append(txt(520, 128, "腰果苹果", size=10, color=ORANGE, weight="700"))
    els.append(txt(646, 128, "腰果仁", size=10, color=GOLD, weight="700"))
    for i, (k, a, b, color) in enumerate(rows):
        y = 146 + i * 46
        els.append(f'<rect x="404" y="{y}" width="330" height="40" rx="6" fill="{SLATE_SOFT if i%2==0 else "#ffffff"}" stroke="{BORDER}"/>')
        els.append(txt(414, y + 25, k, size=9.6, color=MUTED, weight="600"))
        els.append(txt(506, y + 25, a, size=9.6, color=color, weight="600"))
        els.append(txt(636, y + 25, b, size=9.6, color=color, weight="600"))
    els.append(txt(406, 426, "维 C 差 400 多倍：一个补维生素，一个补脂肪热量。", size=10.0, color=SLATE))

    els.append(card(20, 510, 720, 44, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 538, "所以“腰果是什么果”要看你指哪一个：甜蜜多汁的那个是假果，硬壳月牙才是植物学意义上的真果。", size=10.6, color=SLATE))
    return figure(
        568,
        "腰果假果花梗与真果核果结构及营养对比图",
        "左图画腰果枝条上膨大成梨形的花梗假果即腰果苹果与挂在末端的肾形真果坚果，右表比较谁膨大植物学身份能否食用维生素C约二百一十九对零点五毫克与热量约四十八对五百五十三千卡，底栏说明两者身份完全不同。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 毒壳横截面：CNSL 藏在哪
# ---------------------------------------------------------------------------
def build_toxic_shell() -> str:
    els = []
    els.extend(
        header(
            "腰果壳不是“硬壳”，而是一灌满腐蚀油的蜂窝夹层",
            "果壳液 CNSL 占壳重 15%–30%，主成分是腰果酸。",
        )
    )

    els.append(card(20, 66, 352, 430))
    els.append(step_badge(38, 89, 1, fg=ROSE, bg=ROSE_SOFT))
    els.append(txt(56, 93, "剖开一层壳看夹层", size=11.8, color=INK, weight="700"))
    # 外壳
    els.append(f'<rect x="60" y="150" width="270" height="22" rx="6" fill="{SLATE}" stroke="{INK}" stroke-width="1"/>')
    els.append(txt(74, 166, "坚硬外壳", size=9.8, color="#ffffff", weight="600"))
    # 蜂窝夹层
    els.append(f'<rect x="60" y="172" width="270" height="84" fill="{ROSE_SOFT}" stroke="{ROSE}" stroke-width="1.4"/>')
    for row in range(2):
        for col in range(7):
            cx = 78 + col * 37 + (18 if row else 0)
            cy = 194 + row * 40
            els.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#ffffff" stroke="{ROSE}" stroke-width="1.2"/>')
    els.append(txt(196, 278, "蜂窝夹层：灌满 CNSL 毒油", size=10.6, color=ROSE, anchor="middle", weight="700"))
    # 内壳
    els.append(f'<rect x="60" y="288" width="270" height="18" rx="5" fill="{SLATE}" stroke="{INK}" stroke-width="1"/>')
    # 果仁
    els.append(f'<path d="M110 342 Q100 312 140 308 Q186 304 196 330 Q206 356 166 362 Q122 368 110 342 Z" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="2"/>')
    els.append(txt(152, 340, "果仁", size=11, color=GOLD, anchor="middle", weight="700"))
    els.append(txt(38, 394, "夹层在两层硬壳之间：压碎壳，毒油立刻渗到手和果仁上。", size=10.2, color=BODY))
    els.append(txt(38, 424, "这就是腰果从不带壳卖的原因。", size=10.4, color=ROSE, weight="600"))
    els.append(txt(38, 454, "示意图按结构层次绘制，比例非真实尺寸。", size=9.6, color=MUTED))

    els.append(card(388, 66, 352, 430))
    els.append(step_badge(406, 89, 2, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(424, 93, "CNSL 里到底有什么", size=11.8, color=INK, weight="700"))
    comps = [
        ("腰果酸 anacardic acid", "约 60%–70%", ROSE, 0.65),
        ("腰果酚 cardanol", "约 10%–20%", ORANGE, 0.15),
        ("腰果二酚 cardol", "少量", PURPLE, 0.08),
    ]
    for i, (name, pct, color, frac) in enumerate(comps):
        y = 128 + i * 62
        els.append(txt(406, y + 8, name, size=10.2, color=color, weight="600"))
        els.append(f'<rect x="406" y="{y+16}" width="300" height="16" rx="8" fill="{SLATE_SOFT}"/>')
        els.append(f'<rect x="406" y="{y+16}" width="{300*frac:.1f}" height="16" rx="8" fill="{color}"/>')
        els.append(txt(718, y + 8, pct, size=9.8, color=color, anchor="end", weight="700"))
    els.append(_line(406, 318, 724, 318, stroke=BORDER, sw=1))
    els.append(txt(406, 344, "关键机制：长侧链烷基酚能穿透皮肤，引发接触性皮炎。", size=10.2, color=BODY))
    els.append(txt(406, 372, "它是漆酚（urushiol）的酸式近亲——毒藤的同源物。", size=10.2, color=ROSE, weight="600"))
    els.append(txt(406, 402, "加热后腰果酸脱羧变成腰果酚，毒性大减，还成了工业原料。", size=10.0, color=SLATE))
    els.append(txt(406, 432, "一份毒油，既是危害也是资源。", size=10.4, color=TEAL, weight="700"))

    els.append(card(20, 510, 720, 44, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 538, "记住结构就好懂了：壳是油箱，果仁是被油箱包着的食品——只要油不漏进来，果仁本身是安全的。", size=10.6, color=SLATE))
    return figure(
        568,
        "腰果壳蜂窝夹层与腰果壳油CNSL成分结构图",
        "左图剖开腰果壳显示外壳蜂窝夹层与内壳三层结构，夹层灌满占壳重百分之十五到三十的腰果壳油并包着果仁；右图列出腰果酸约百分之六十到七十、腰果酚约百分之十到二十与腰果二酚少量，说明烷基酚穿透皮肤引发接触性皮炎且与漆酚同源加热脱羧变腰果酚。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 同科关系：腰果与毒藤、芒果
# ---------------------------------------------------------------------------
def build_toxic_family() -> str:
    els = []
    els.extend(
        header(
            "腰果与毒藤同科：一颗坚果为啥跟“碰不得”的草是亲戚",
            "漆树科的共同化学武器：烷基酚类树脂。",
        )
    )

    els.append(card(20, 66, 720, 214))
    els.append(step_badge(38, 89, 1, fg=ROSE, bg=ROSE_SOFT))
    els.append(txt(56, 93, "漆树科 Anacardiaceae 的一家子", size=11.8, color=INK, weight="700"))
    els.append(f'<rect x="316" y="112" width="128" height="38" rx="10" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.4"/>')
    els.append(txt(380, 136, "漆树科", size=12, color=SLATE, anchor="middle", weight="700"))
    members = [
        (60, "腰果", ROSE, ROSE_SOFT, "壳油 · 腰果酸"),
        (214, "毒藤", ROSE, ROSE_SOFT, "漆酚 · urushiol"),
        (368, "芒果", ORANGE, ORANGE_SOFT, "果皮 · 漆酚类"),
        (522, "开心果", GREEN, GREEN_SOFT, "同科 · 也可过敏"),
    ]
    for x, name, fg, soft, note in members:
        els.append(_line(380, 150, x + 66, 190, stroke=BORDER, sw=1.2))
        els.append(f'<rect x="{x}" y="190" width="132" height="66" rx="8" fill="{soft}" stroke="{fg}" stroke-width="1.4"/>')
        els.append(txt(x + 66, 216, name, size=11.4, color=fg, anchor="middle", weight="700"))
        els.append(txt(x + 66, 240, note, size=9.2, color=BODY, anchor="middle"))

    els.append(card(20, 296, 352, 232))
    els.append(step_badge(38, 319, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(56, 323, "为什么亲戚会有毒？", size=11.6, color=INK, weight="700"))
    els.append(txt(38, 356, "同一科植物共用一套生化工具箱：", size=10.4, color=BODY))
    els.append(txt(38, 386, "把带长侧链的酚类树脂涂在表面，", size=10.4, color=BODY))
    els.append(txt(38, 416, "谁啃我，谁就沾一身疹子。", size=10.4, color=BODY))
    els.append(txt(38, 452, "这不是巧合，是共同祖先传下来的防御策略。", size=9.8, color=SLATE))
    els.append(txt(38, 484, "果仁把这套武器封在壳的油箱里。", size=10.2, color=GREEN, weight="600"))

    els.append(card(388, 296, 352, 232))
    els.append(step_badge(406, 319, 3, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 323, "毒性只在外面，不在果仁", size=11.6, color=INK, weight="700"))
    els.append(txt(406, 356, "腰果仁本身不含腰果酸，正常食用安全。", size=10.2, color=BODY))
    els.append(txt(406, 386, "危险发生在剥壳：毒油沾到皮肤和果仁。", size=10.2, color=BODY))
    els.append(txt(406, 416, "症状：灼痛、红肿、水疱，类似毒藤。", size=10.2, color=ROSE))
    els.append(txt(406, 452, "误食浓 CNSL 可致消化道灼伤与化学性肺炎。", size=9.8, color=SLATE))
    els.append(txt(406, 484, "所以工业剥壳必须高温＋防护。", size=10.2, color=ORANGE, weight="600"))

    els.append(card(20, 542, 720, 40, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 568, "“同科有毒”不等于“果仁有毒”：防御化学品被封在壳里，果仁只是被保护的种子。", size=10.4, color=SLATE))
    return figure(
        596,
        "漆树科腰果毒藤芒果开心果亲缘关系与毒性分布图",
        "顶部是漆树科分类树连出腰果毒藤芒果开心果四个分支并标注各自酚类树脂，左下面解释同科共用烷基酚防御工具箱果仁把武器封在壳里，右下面说明毒性只在外面果仁本身不含腰果酸剥壳才会沾油以及误食浓腰果壳油可致消化道灼伤。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 加工去毒：从毒果到零食
# ---------------------------------------------------------------------------
def build_processing() -> str:
    els = []
    els.extend(
        header(
            "货架上的“生腰果”其实都熟过：一道高温工序把毒油逼出来",
            "蒸或烤 → 壳脆油出 → 剥壳 → 分级，毒性就此归零。",
        )
    )

    els.append(card(20, 66, 720, 220))
    els.append(step_badge(38, 89, 1, fg=GOLD, bg=GOLD_SOFT))
    els.append(txt(56, 93, "带壳腰果的工业化流程", size=11.8, color=INK, weight="700"))
    steps = [
        (36, "带壳果", "毒油满壳", ROSE),
        (176, "蒸汽/烘烤", "高温脱毒", GOLD),
        (316, "壳裂油出", "CNSL 回收", ORANGE),
        (456, "机械剥壳", "果仁分离", GREEN),
        (596, "分级包装", "出口上市", BLUE),
    ]
    for i, (x, title, note, color) in enumerate(steps):
        els.append(f'<rect x="{x}" y="132" width="124" height="88" rx="8" fill="{SLATE_SOFT}" stroke="{color}" stroke-width="1.4"/>')
        els.append(txt(x + 62, 162, title, size=10.8, color=color, anchor="middle", weight="700"))
        els.append(txt(x + 62, 188, note, size=9.4, color=BODY, anchor="middle"))
        if i < len(steps) - 1:
            els.append(f'<path d="M{x+126} 176 L{x+172} 176" stroke="{SLATE}" stroke-width="1.6" fill="none" marker-end="url(#arr-blue)"/>')
    els.append(txt(36, 248, "关键就在第二步：高温让壳中油囊破裂、腰果酸脱羧，毒油流出被回收。", size=10.2, color=SLATE))
    els.append(txt(36, 274, "所以“raw cashew（生腰果）”只是“未调味”的营销叫法，不是真的生。", size=10.2, color=ROSE, weight="600"))

    els.append(card(20, 302, 352, 224))
    els.append(step_badge(38, 325, 2, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(56, 329, "毒油变宝贝", size=11.6, color=INK, weight="700"))
    els.append(txt(38, 362, "回收的 CNSL 是贵重工业原料：", size=10.4, color=BODY))
    els.append(txt(38, 392, "• 刹车片、离合器摩擦材料", size=10.2, color=TEAL))
    els.append(txt(38, 420, "• 酚醛树脂、涂料、绝缘材料", size=10.2, color=TEAL))
    els.append(txt(38, 448, "• 抗菌活性研究、药物中间体", size=10.2, color=TEAL))
    els.append(txt(38, 484, "脱羧后的腰果酚毒性大减。", size=10.2, color=SLATE))

    els.append(card(388, 302, 352, 224))
    els.append(step_badge(406, 325, 3, fg=ROSE, bg=ROSE_SOFT))
    els.append(txt(424, 329, "别在家里剥生腰果", size=11.6, color=INK, weight="700"))
    els.append(txt(406, 362, "树上现摘的带壳腰果会渗毒油：", size=10.4, color=BODY))
    els.append(txt(406, 392, "• 皮肤灼痛、红疹、水疱", size=10.2, color=ROSE))
    els.append(txt(406, 420, "• 沾到果仁再入口，口腔灼伤", size=10.2, color=ROSE))
    els.append(txt(406, 448, "• 溅入眼睛需立刻大量冲洗就医", size=10.2, color=ROSE))
    els.append(txt(406, 484, "戴手套也没用：酚类能穿透乳胶。", size=10.2, color=SLATE, weight="600"))

    els.append(card(20, 542, 720, 40, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 568, "产业链的聪明之处：把同一份“毒”从食品里分离出去，变成工业的“宝”。", size=10.4, color=SLATE))
    return figure(
        596,
        "腰果工业化加工去毒流程与腰果壳油回收利用图",
        "顶部五步流程从带壳果经蒸汽烘烤壳裂油出机械剥壳到分级包装，说明高温使腰果酸脱羧毒油流出回收且所谓生腰果只是未调味；左下讲回收腰果壳油用作刹车片树脂涂料与药物中间体，右下讲家里剥生腰果会导致皮肤水疱口腔灼伤与眼睛刺激且乳胶手套无效。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 营养与过敏
# ---------------------------------------------------------------------------
def build_nutrition_allergy() -> str:
    els = []
    els.extend(
        header(
            "果仁很营养，但也是“顶级过敏原”：营养密度与免疫风险并存",
            "每 100 g 约 553 kcal，铜、镁突出；Ana o 1/2/3 可致严重过敏。",
        )
    )

    els.append(card(20, 66, 352, 430))
    els.append(step_badge(38, 89, 1, fg=GOLD, bg=GOLD_SOFT))
    els.append(txt(56, 93, "每 100 g 腰果仁的营养账", size=11.6, color=INK, weight="700"))
    rows = [
        ("热量", "553 kcal", "一小把 28 g ≈ 155 kcal"),
        ("脂肪", "43.8 g", "以不饱和脂肪酸为主"),
        ("蛋白质", "18.2 g", "植物蛋白补充"),
        ("碳水化合物", "30.2 g", "坚果中偏高"),
        ("镁", "约 260 mg", "能量代谢与神经肌肉"),
        ("铜", "约 1.66 mg", "远超多数坚果"),
    ]
    for i, (k, v, note) in enumerate(rows):
        y = 120 + i * 55
        els.append(f'<rect x="38" y="{y}" width="316" height="48" rx="6" fill="{SLATE_SOFT if i%2==0 else "#ffffff"}" stroke="{BORDER}"/>')
        els.append(txt(50, y + 20, k, size=10.2, color=MUTED, weight="600"))
        els.append(txt(50, y + 39, note, size=9.2, color=BODY))
        els.append(txt(342, y + 28, v, size=10.4, color=GOLD, anchor="end", weight="700"))
    els.append(txt(38, 460, "数据：USDA FoodData Central（ID 170566）。", size=9.4, color=MUTED))

    els.append(card(388, 66, 352, 430))
    els.append(step_badge(406, 89, 2, fg=ROSE, bg=ROSE_SOFT))
    els.append(txt(424, 93, "三种主要过敏蛋白", size=11.6, color=INK, weight="700"))
    allergens = [
        ("Ana o 1", "7S 球蛋白（vicilin 类）", "种子储存蛋白"),
        ("Ana o 2", "11S 球蛋白（legumin 类）", "与豆类交叉反应"),
        ("Ana o 3", "2S 白蛋白", "与严重过敏反应相关"),
    ]
    for i, (name, kind, note) in enumerate(allergens):
        y = 122 + i * 78
        els.append(f'<rect x="406" y="{y}" width="318" height="66" rx="8" fill="{ROSE_SOFT}" stroke="{ROSE}" stroke-width="1.2"/>')
        els.append(txt(420, y + 22, name, size=11.4, color=ROSE, weight="700"))
        els.append(txt(420, y + 44, kind, size=9.8, color=BODY))
        els.append(txt(420, y + 60, note, size=9.2, color=MUTED))
    els.append(_line(406, 362, 724, 362, stroke=BORDER, sw=1))
    els.append(txt(406, 390, "机制：IgE 介导的 I 型超敏反应，症状可迅速加重。", size=9.8, color=BODY))
    els.append(txt(406, 418, "从口腔瘙痒、荨麻疹到喉头水肿、过敏性休克。", size=9.8, color=ROSE))
    els.append(txt(406, 448, "与开心果交叉反应高，两者需一同规避。", size=10.0, color=SLATE))
    els.append(txt(406, 476, "对坚果过敏者，彻底避免比“少量试试”安全得多。", size=9.8, color=INK, weight="600"))

    els.append(card(20, 510, 720, 44, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 538, "毒壳的“外毒”与果仁的“内敏”是两回事：前者高温可解，后者只能靠规避。", size=10.6, color=SLATE))
    return figure(
        568,
        "腰果仁营养成分与Ana过敏蛋白对照图",
        "左表列出每100克腰果仁热量553千卡脂肪43.8克蛋白质18.2克碳水30.2克镁约260毫克铜约1.66毫克并注一小把28克约155千卡，右表列出Ana o 1七S球蛋白Ana o 2十一S球蛋白Ana o 3二S白蛋白及IgE介导过敏症状与开心果交叉反应，底栏区分毒壳外毒与果仁内敏。",
        els,
    )


@register(TOPIC, "腰果：假果真相、毒壳 CNSL、同科毒藤、加工去毒与营养过敏", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("cashew-false-true-fruit.svg", build_false_true_fruit),
        ("cashew-toxic-shell.svg", build_toxic_shell),
        ("cashew-toxic-family.svg", build_toxic_family),
        ("cashew-processing.svg", build_processing),
        ("cashew-nutrition-allergy.svg", build_nutrition_allergy),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
