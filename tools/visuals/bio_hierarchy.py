"""生物层级结构：系统到器官、组织、细胞、蛋白质、氨基酸与 DNA 的原创图解。"""

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

TOPIC = "bio-hierarchy"

TEAL = "#0f766e"
TEAL_SOFT = "#e6f5f2"
ROSE = "#be123c"
ROSE_SOFT = "#ffe9ee"
GOLD = "#b45309"
GOLD_SOFT = "#fdf1d8"


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
    levels = ["系统", "器官", "组织", "细胞", "蛋白质", "氨基酸", "DNA"]
    tissues = ["上皮", "结缔", "肌肉", "神经"]
    systems = ["循环", "消化", "内分泌", "免疫", "皮肤", "肌肉", "神经", "生殖", "呼吸", "骨骼", "泌尿"]
    assert len(levels) == 7
    assert len(tissues) == 4
    assert len(systems) == 11
    assert len(set(tissues)) == 4 and len(set(systems)) == 11

    # 密码子：4 种碱基、三联体，64 个密码子中 61 个有义、3 个终止
    assert 4**3 == 64 and 64 == 61 + 3
    assert 4**2 == 16 < 20 <= 4**3 == 64

    # 20 种标准氨基酸，9 种必需；硒半胱氨酸为人体第 21 种
    assert 20 + 1 == 21 and 9 < 20

    # 肽键数 = 氨基酸数 - 1（成熟胰岛素 A21 + B30 = 51）
    insulin = 21 + 30
    assert insulin == 51 and insulin - 1 == 50

    # B-DNA 每碱基对上升 0.34 nm；体细胞两套基因组拉直接近 2 m
    bp_per_genome = 3.0e9
    rise = 0.34e-9
    length_one = bp_per_genome * rise
    length_two = 2 * length_one
    assert 1.0 < length_one < 1.1
    assert 1.9 < length_two < 2.2

    # 核糖体速度：细菌约 20 个/秒，真核约 5~6 个/秒
    chain = 200
    assert chain / 20 == 10
    assert 30 < chain / 5.5 < 40


# ---------------------------------------------------------------------------
# 1. 七级阶梯总览
# ---------------------------------------------------------------------------
def build_ladder() -> str:
    rows = [
        ("系统", "循环系统＝心脏＋血管＋血液", "≈ 1 m", "把氧和养分送到全身", BLUE, BLUE_SOFT),
        ("器官", "心脏：由至少两类组织搭成", "≈ 12 cm", "有外形，能独立泵血", ORANGE, ORANGE_SOFT),
        ("组织", "心肌组织：许多心肌细胞协同", "mm～cm", "同步收缩形成合力", GREEN, GREEN_SOFT),
        ("细胞", "一个心肌细胞", "10～20 µm", "自己代谢、自己兴奋", PURPLE, PURPLE_SOFT),
        ("蛋白质", "肌球蛋白：把 ATP 变成推力", "≈ 5 nm", "分子机器输出机械功", GOLD, GOLD_SOFT),
        ("氨基酸", "亮氨酸、谷氨酸等 20 种", "≈ 0.8 nm", "排列顺序决定折叠", ROSE, ROSE_SOFT),
        ("DNA", "肌球蛋白基因写在基因组里", "双螺旋 2 nm", "可复制，能传给后代", TEAL, TEAL_SOFT),
    ]
    els = []
    els.extend(
        header(
            "从系统到 DNA：七层台阶，每下一层都更小、更多、更基础",
            "以“心脏—肌球蛋白”为一条线走到底；右边一列是该层才冒出来的新性质。",
        )
    )
    els.append(txt(36, 64, "层级", size=10.2, color=MUTED, weight="600"))
    els.append(txt(152, 64, "顺着心脏往下看", size=10.2, color=MUTED, weight="600"))
    els.append(txt(438, 64, "典型尺度", size=10.2, color=MUTED, weight="600"))
    els.append(txt(548, 64, "这一层才有的能力", size=10.2, color=MUTED, weight="600"))

    for i, (name, example, scale, emergent, fg, soft) in enumerate(rows):
        y = 72 + i * 72
        els.append(card(20, y, 720, 66))
        els.append(f'<rect x="20" y="{y}" width="6" height="66" rx="3" fill="{fg}"/>')
        els.append(pill(36, y + 18, name, fg=fg, bg=soft, w=92, h=26, size=11.4))
        els.append(txt(152, y + 36, example, size=10.9, color=INK, weight="600"))
        els.append(txt(438, y + 36, scale, size=10.2, color=fg, weight="700"))
        els.append(txt(548, y + 36, emergent, size=10.4, color=BODY))
        if i < len(rows) - 1:
            els.append(_line(82, y + 66, 82, y + 72, stroke=fg, sw=1.4, marker="arr-muted"))

    els.append(card(20, 584, 720, 44, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 612, "“涌现”：下层零件本身没有泵血功能，按层级组织起来才出现；往上走看功能，往下走看机制。", size=10.6, color=SLATE))
    return figure(
        642,
        "系统器官组织细胞蛋白质氨基酸DNA七级生物层级总览图",
        "七行阶梯以心脏为例逐层下钻：系统循环系统约一米、器官心脏约十二厘米、组织心肌组织毫米至厘米、细胞心肌细胞十到二十微米、蛋白质肌球蛋白约五纳米、氨基酸约零点八纳米、DNA双螺旋直径两纳米；右列逐层列出新出现的能力，底栏解释涌现。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 组织四型与十一系统
# ---------------------------------------------------------------------------
def build_tissues_systems() -> str:
    els = []
    els.extend(
        header(
            "器官不是“一块肉”：四类组织搭台，十一个系统唱戏",
            "同一种细胞按不同排列方式，就能形成完全不同的组织。",
        )
    )

    els.append(card(20, 66, 352, 446))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "四类基本组织（人体）", size=11.8, color=INK, weight="700"))

    # 上皮：紧密排列的片状细胞
    y = 116
    els.append(txt(38, y + 10, "上皮组织", size=10.7, color=BLUE, weight="700"))
    for k in range(7):
        els.append(f'<rect x="{40 + k*44}" y="{y+22}" width="40" height="34" rx="4" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1"/>')
    els.append(txt(38, y + 72, "细胞紧密成片，覆盖表面、构成腺体", size=9.9, color=BODY))

    # 结缔：细胞散在基质中
    y = 202
    els.append(txt(38, y + 10, "结缔组织", size=10.7, color=ORANGE, weight="700"))
    els.append(f'<rect x="38" y="{y+20}" width="310" height="44" rx="6" fill="{ORANGE_SOFT}" stroke="{BORDER}"/>')
    for k, cx in enumerate([70, 148, 228, 310]):
        els.append(f'<circle cx="{cx}" cy="{y+42}" r="8" fill="#ffffff" stroke="{ORANGE}" stroke-width="1.3"/>')
        els.append(_line(cx + 8, y + 42, cx + 34, y + 30, stroke=ORANGE, sw=0.9))
    els.append(txt(38, y + 82, "细胞散在大量细胞外基质中：骨、软骨、血液", size=9.5, color=BODY))

    # 肌肉：长梭形，有横纹
    y = 300
    els.append(txt(38, y + 10, "肌肉组织", size=10.7, color=GREEN, weight="700"))
    for k in range(3):
        yy = y + 22 + k * 16
        els.append(f'<rect x="40" y="{yy}" width="300" height="13" rx="6" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.2"/>')
        for s in range(9):
            els.append(_line(58 + s * 32, yy + 1, 58 + s * 32, yy + 12, stroke=GREEN, sw=0.8))
    els.append(txt(38, y + 82, "细胞细长、能收缩：骨骼肌、心肌、平滑肌", size=9.5, color=BODY))

    # 神经：带长突起
    y = 398
    els.append(txt(38, y + 10, "神经组织", size=10.7, color=PURPLE, weight="700"))
    els.append(f'<circle cx="96" cy="{y+38}" r="16" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.3"/>')
    for sx, sy, dx, dy in [(84, y + 30, 56, y + 16), (84, y + 46, 56, y + 60),
                           (110, y + 30, 150, y + 18), (110, y + 46, 158, y + 54)]:
        els.append(_line(sx, sy, dx, dy, stroke=PURPLE, sw=1.3))
    els.append(txt(180, y + 34, "细胞带长突起，用电信号传递信息", size=9.6, color=BODY))
    els.append(txt(180, y + 55, "脑、脊髓、外周神经", size=9.6, color=MUTED))

    els.append(card(388, 66, 352, 446))
    els.append(step_badge(406, 89, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 93, "十一大器官系统", size=11.8, color=INK, weight="700"))
    systems = [
        ("循环", BLUE), ("消化", ORANGE), ("内分泌", PURPLE), ("免疫", TEAL),
        ("皮肤", GOLD), ("肌肉", GREEN), ("神经", PURPLE), ("生殖", ROSE),
        ("呼吸", BLUE), ("骨骼", SLATE), ("泌尿", TEAL),
    ]
    for i, (name, color) in enumerate(systems):
        col, row = i % 2, i // 2
        x = 406 + col * 168
        y = 118 + row * 42
        els.append(pill(x, y, name, fg=color, bg=SLATE_SOFT, w=152, h=30, size=11.2))

    els.append(_line(406, 356, 724, 356, stroke=BORDER, sw=1))
    els.append(txt(406, 380, "器官＝至少两种组织搭起来", size=11.0, color=INK, weight="700"))
    layers = [("心肌", GREEN, GREEN_SOFT), ("结缔（瓣膜、支架）", ORANGE, ORANGE_SOFT),
              ("上皮（内皮）", BLUE, BLUE_SOFT), ("神经（传导）", PURPLE, PURPLE_SOFT)]
    for i, (label, fg, soft) in enumerate(layers):
        y = 394 + i * 27
        els.append(f'<rect x="406" y="{y}" width="120" height="22" rx="5" fill="{soft}" stroke="{fg}" stroke-width="1"/>')
        els.append(txt(470, y + 16, label, size=9.6, color=fg, anchor="middle", weight="600"))
        els.append(txt(538, y + 16, "心脏里都有", size=9.6, color=MUTED))
    els.append(txt(406, 506, "系统由多个器官组成，例：心脏＋血管＋血液＝循环系统。", size=9.8, color=SLATE))

    els.append(card(20, 526, 720, 44, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 554, "分类是人为的方便：血液算结缔组织，心肌是组织也是器官的一部分，层级之间并非刀切。", size=10.6, color=SLATE))
    return figure(
        584,
        "四类基本组织与人体十一大器官系统关系图",
        "左栏画出上皮紧密成片、结缔细胞散在基质、肌肉长梭形带横纹、神经细胞带长突起四种基本组织；右栏列出循环消化内分泌免疫皮肤肌肉神经生殖呼吸骨骼泌尿共十一个器官系统，并用心脏示意器官由心肌结缔上皮与神经四类组织构成。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 细胞到蛋白质
# ---------------------------------------------------------------------------
def build_cell_to_protein() -> str:
    els = []
    els.extend(
        header(
            "细胞不是“一袋蛋白质”：它有边界、有分工、有能量供应",
            "一个心肌细胞直径约 10～20 µm，里面同时运转着上万种蛋白质。",
        )
    )

    els.append(card(20, 66, 352, 428))
    els.append(step_badge(38, 89, 1, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 93, "细胞：生命最小的独立单位", size=11.8, color=INK, weight="700"))
    els.append(f'<ellipse cx="196" cy="252" rx="150" ry="118" fill="#fbfdff" stroke="{PURPLE}" stroke-width="2"/>')
    els.append(f'<ellipse cx="196" cy="252" rx="141" ry="109" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="0.8" stroke-opacity="0.35"/>')
    els.append(f'<ellipse cx="182" cy="242" rx="56" ry="44" fill="#ffffff" stroke="{BLUE}" stroke-width="1.6"/>')
    els.append(txt(182, 246, "细胞核", size=10.6, color=BLUE, anchor="middle", weight="700"))
    for cx, cy, lab in [(262, 202, "线粒体"), (258, 292, "核糖体"), (112, 316, "细胞骨架")]:
        els.append(f'<circle cx="{cx}" cy="{cy}" r="15" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="1.2"/>')
        els.append(txt(cx + 20, cy + 4, lab, size=9.6, color=GOLD))
    els.append(txt(38, 128, "膜把内外分开；细胞器分工；ATP 供能。", size=10.2, color=BODY))
    els.append(txt(38, 396, "全成人约 30 万亿个细胞、约 200 种类型。", size=10.2, color=SLATE))
    els.append(txt(38, 424, "红细胞是特例：成熟后没有细胞核。", size=10.0, color=MUTED))

    els.append(card(388, 66, 352, 428))
    els.append(step_badge(406, 89, 2, fg=GOLD, bg=GOLD_SOFT))
    els.append(txt(424, 93, "蛋白质：细胞里的分子机器", size=11.8, color=INK, weight="700"))

    # 一条肽链折叠成球蛋白的示意
    chain = [(424, 156), (452, 140), (482, 152), (506, 134), (534, 152),
             (560, 138), (588, 156), (600, 186), (578, 206), (548, 194),
             (520, 214), (490, 196), (462, 220), (436, 200)]
    els.append('<path d="M' + " L".join(f"{x},{y}" for x, y in chain) + '" fill="none" stroke="' + ROSE + '" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    for x, y in chain:
        els.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#ffffff" stroke="{ROSE}" stroke-width="1.3"/>')
    els.append(txt(512, 244, "一条氨基酸链折叠成有形状的蛋白", size=9.8, color=BODY, anchor="middle"))
    els.append(_line(388, 264, 740, 264, stroke=BORDER, sw=1))
    facts = [
        ("运输", "血红蛋白运氧"),
        ("催化", "酶降低反应门槛"),
        ("运动", "肌球蛋白把 ATP 变推力"),
        ("防御", "抗体识别外来物"),
    ]
    for i, (role, desc) in enumerate(facts):
        y = 280 + i * 31
        els.append(pill(406, y, role, fg=GOLD, bg=GOLD_SOFT, w=56, h=22, size=10.4))
        els.append(txt(474, y + 16, desc, size=10.2, color=BODY))
    els.append(txt(406, 414, "人体蛋白中位长度约 415 个氨基酸。", size=10.0, color=SLATE))
    els.append(txt(406, 442, "直径量级：细胞 10 µm → 蛋白 5 nm。", size=10.0, color=MUTED))

    els.append(card(20, 508, 720, 44, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 536, "看细胞要显微镜，看蛋白质要靠 X 射线晶体学、冷冻电镜或结构预测；尺度差约一千倍。", size=10.6, color=SLATE))
    return figure(
        566,
        "细胞结构到蛋白质分子机器的尺度放大图",
        "左图画一个约十到二十微米的心肌细胞，含细胞核线粒体核糖体与细胞骨架，并标注成人约三十万亿个细胞约两百种类型；右图画一条氨基酸链折叠成球蛋白，列举运输催化运动防御四类功能，标注人体蛋白中位长度约四百一十五个氨基酸，强调细胞与蛋白尺度相差约一千倍。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 氨基酸到蛋白质
# ---------------------------------------------------------------------------
def build_amino_acids() -> str:
    els = []
    els.extend(
        header(
            "氨基酸只有 20 种，为什么能拼出十万种蛋白？",
            "关键在于侧链 R 的化学性格，以及排列顺序带来的折叠方式。",
        )
    )

    els.append(card(20, 66, 352, 438))
    els.append(step_badge(38, 89, 1, fg=ROSE, bg=ROSE_SOFT))
    els.append(txt(56, 93, "一个氨基酸的通用骨架", size=11.8, color=INK, weight="700"))
    cx, cy = 196, 202
    els.append(_line(cx, cy - 24, cx, cy - 58, stroke=SLATE, sw=1.4))
    els.append(_line(cx, cy + 24, cx, cy + 58, stroke=SLATE, sw=1.4))
    els.append(_line(cx - 24, cy, cx - 72, cy, stroke=SLATE, sw=1.4))
    els.append(_line(cx + 24, cy, cx + 72, cy, stroke=SLATE, sw=1.4))
    els.append(f'<circle cx="{cx}" cy="{cy}" r="24" fill="#ffffff" stroke="{ROSE}" stroke-width="1.6"/>')
    els.append(txt(cx, cy + 5, "Cα", size=11.4, color=ROSE, anchor="middle", weight="700"))
    els.append(txt(cx, cy - 66, "氨基 —NH₂", size=10.2, color=BLUE, anchor="middle", weight="600"))
    els.append(txt(cx, cy + 76, "羧基 —COOH", size=10.2, color=ORANGE, anchor="middle", weight="600"))
    els.append(txt(cx - 82, cy + 4, "H", size=10.2, color=MUTED, anchor="middle"))
    els.append(txt(cx + 84, cy + 4, "R 侧链", size=10.2, color=ROSE, anchor="middle", weight="700"))
    els.append(_line(38, 306, 352, 306, stroke=BORDER, sw=1))
    els.append(txt(38, 332, "20 种标准氨基酸：共同骨架相同，只有 R 不同。", size=10.3, color=INK, weight="600"))
    els.append(txt(38, 360, "人体还会用第 21 种：硒半胱氨酸。", size=10.2, color=BODY))
    els.append(txt(38, 388, "其中 9 种人体不能自己合成，必须从食物来。", size=10.2, color=BODY))
    els.append(txt(38, 420, "R 有带电极性、疏水、含硫等性格，决定折叠。", size=10.2, color=SLATE))
    els.append(txt(38, 452, "单个氨基酸直径量级：约 0.8 nm。", size=10.0, color=MUTED))

    els.append(card(388, 66, 352, 438))
    els.append(step_badge(406, 89, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(424, 93, "肽键：一颗一颗焊成链，再折成形状", size=11.6, color=INK, weight="700"))
    els.append(txt(406, 128, "羧基 + 氨基 → 肽键 + 一分子水", size=10.4, color=GREEN, weight="600"))
    beads = [(414, 164), (454, 164), (494, 164), (534, 164), (574, 164), (614, 164), (654, 164)]
    for i, (bx, by) in enumerate(beads):
        els.append(f'<circle cx="{bx}" cy="{by}" r="13" fill="{["#fde68a", "#bfdbfe", "#fecaca", "#bbf7d0", "#ddd6fe"][i%5]}" stroke="{SLATE}" stroke-width="1"/>')
        els.append(txt(bx, by + 4, "R", size=9.2, color=SLATE, anchor="middle"))
        if i < len(beads) - 1:
            els.append(_line(bx + 14, by, bx + 26, by, stroke=ROSE, sw=1.8))
    els.append(txt(534, 194, "n 个氨基酸 → n−1 个肽键", size=10.4, color=INK, anchor="middle", weight="700"))
    els.append(_line(406, 216, 724, 216, stroke=BORDER, sw=1))

    els.append(f'<circle cx="556" cy="298" r="56" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
    els.append(f'<circle cx="556" cy="298" r="40" fill="#ffffff" stroke="{GREEN}" stroke-width="0.9" stroke-dasharray="4 3"/>')
    els.append(txt(556, 302, "折叠后的\n蛋白质", size=10.6, color=GREEN, anchor="middle", weight="700"))
    els.append(_line(470, 240, 516, 266, stroke=GREEN, sw=1.4, marker="arr-green"))
    els.append(txt(406, 384, "成熟胰岛素＝51 个氨基酸，50 个肽键。", size=10.4, color=BODY))
    els.append(txt(406, 412, "细菌核糖体约 20 个/秒；人体细胞约 5～6 个/秒。", size=10.0, color=BODY))
    els.append(txt(406, 440, "一条 200 氨基酸的链：细菌约 10 秒，人体约 36 秒。", size=10.0, color=SLATE))
    els.append(txt(406, 470, "顺序 → 折叠 → 形状 → 功能，一步错可能全盘错。", size=10.0, color=MUTED))

    els.append(card(20, 518, 720, 44, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 546, "20 种字母不是 20 种蛋白：组合数是天文数字，细胞再用折叠、剪接与修饰把可能性收束到可用的少数。", size=10.6, color=SLATE))
    return figure(
        576,
        "氨基酸通用骨架肽键连接与蛋白质折叠示意图",
        "左图画氨基酸的α碳连接氨基羧基氢原子与侧链R，说明二十种标准氨基酸人体额外使用硒半胱氨酸九种必需且侧链性格决定折叠；右图画七个氨基酸经肽键连成链并折叠成球蛋白，标注n个氨基酸形成n减一个肽键、成熟胰岛素五十一个氨基酸五十个肽键，以及细菌每秒约二十个而人体每秒约五到六个氨基酸的翻译速度。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. DNA 到蛋白质
# ---------------------------------------------------------------------------
def build_dna_to_protein() -> str:
    els = []
    els.extend(
        header(
            "DNA 写的是字母，细胞读的是三字母一个词",
            "30 亿对碱基里挑出约 2 万个基因，先抄成 mRNA，再翻译成氨基酸链。",
        )
    )

    els.append(card(20, 66, 720, 196))
    els.append(step_badge(38, 89, 1, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(56, 93, "DNA：双螺旋直径约 2 nm，一个细胞里拉直约 2 m", size=11.6, color=INK, weight="700"))
    # 双螺旋示意
    import math
    left, right = [], []
    for k in range(19):
        x = 42 + k * 16
        phase = k * 0.8
        left.append((x, 196 + 26 * math.sin(phase)))
        right.append((x, 196 - 26 * math.sin(phase)))
    for pts, color in [(left, TEAL), (right, BLUE)]:
        els.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '" fill="none" stroke="' + color + '" stroke-width="2"/>')
    for k in range(0, 19, 2):
        els.append(_line(left[k][0], left[k][1], right[k][0], right[k][1], stroke=SLATE, sw=1.1))
    els.append(txt(196, 250, "A—T 两个氢键，G—C 三个氢键", size=9.6, color=SLATE, anchor="middle"))
    els.append(_line(390, 124, 390, 244, stroke=BORDER, sw=1))
    dna_facts = [
        ("全人类基因组", "约 30 亿对碱基"),
        ("蛋白编码基因", "约 2 万～2.5 万个"),
        ("编码序列占比", "约 1.5%"),
        ("每个基因平均", "约 3 种蛋白"),
    ]
    for i, (k, v) in enumerate(dna_facts):
        y = 140 + i * 28
        els.append(txt(408, y, k, size=10.2, color=MUTED))
        els.append(txt(556, y, v, size=10.4, color=INK, weight="700"))
    els.append(txt(408, 252, "同一套 DNA，不同细胞只读其中一小部分。", size=9.8, color=TEAL))

    els.append(card(20, 278, 720, 148))
    els.append(step_badge(38, 301, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 305, "信息流：DNA → RNA → 蛋白质", size=11.6, color=INK, weight="700"))
    nodes = [
        (40, "DNA", "基因片段", TEAL),
        (176, "转录", "RNA 聚合酶抄写", BLUE),
        (312, "mRNA", "剪掉内含子", PURPLE),
        (448, "翻译", "核糖体读密码子", ORANGE),
        (584, "蛋白质", "折叠后上岗", GREEN),
    ]
    for i, (x, title, note, color) in enumerate(nodes):
        els.append(f'<rect x="{x}" y="326" width="120" height="72" rx="8" fill="#f8fafc" stroke="{color}" stroke-width="1.4"/>')
        els.append(txt(x + 60, 352, title, size=11.0, color=color, anchor="middle", weight="700"))
        els.append(txt(x + 60, 376, note, size=9.6, color=BODY, anchor="middle"))
        if i < 4:
            els.append(_line(x + 122, 362, x + 172, 362, stroke=color, sw=1.8, marker="arr-blue"))
    els.append(txt(40, 416, "4 种碱基 × 3 个字母 = 64 个密码子：61 个指定氨基酸，3 个是“停”。", size=10.4, color=INK, weight="600"))

    els.append(card(20, 442, 720, 92))
    els.append(step_badge(38, 464, 3, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(56, 468, "这不是单向命令，而是一场循环", size=11.6, color=INK, weight="700"))
    els.append(txt(40, 496, "DNA 决定氨基酸顺序；读 DNA、复制 DNA、剪接 mRNA 的酶本身也是蛋白质。", size=10.4, color=BODY))
    els.append(txt(40, 522, "环境、饮食、信号与表观修饰都会改变哪些基因被读、读多少——基因给的是剧本，不是定稿。", size=10.2, color=SLATE))

    els.append(card(20, 550, 720, 44, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 578, "层级不是一条单行道：往上追功能，往下追机制，再往回看 DNA 与蛋白质的互相成就。", size=10.6, color=SLATE))
    return figure(
        608,
        "DNA双螺旋到蛋白质翻译的信息流与反馈循环图",
        "顶部画出DNA双螺旋直径约两纳米、单个细胞DNA拉直约两米，列出人类基因组约三十亿对碱基、两万到两万五千个蛋白编码基因、编码序列约百分之一点五、每个基因平均约三种蛋白；中部展示DNA转录成mRNA剪接后由核糖体翻译成蛋白质的五站流程与六十四密码子六十一有义三个终止；底部强调DNA与蛋白质互为因果并受环境影响。",
        els,
    )


@register(TOPIC, "生物层级：系统、器官、组织、细胞、蛋白质、氨基酸与 DNA 的七级结构", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("bio-hierarchy-ladder.svg", build_ladder),
        ("tissues-and-organ-systems.svg", build_tissues_systems),
        ("cell-to-protein-zoom.svg", build_cell_to_protein),
        ("amino-acid-to-protein.svg", build_amino_acids),
        ("dna-to-protein-flow.svg", build_dna_to_protein),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
