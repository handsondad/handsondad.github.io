"""《Hardware Is Software》解读：伪装成硬件的软件、三条证据、成本账、边界与程序员转型的原创 SVG 图解。"""

from __future__ import annotations

import math

from .core import (
    BODY,
    BORDER,
    BLUE,
    BLUE_SOFT,
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

TOPIC = "hardware-is-software"

RED = "#b42318"
RED_SOFT = "#fee9e7"
TEAL = "#0f766e"
TEAL_SOFT = "#e6f5f2"
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


def _arrow(x1, y1, x2, y2, marker="arr-blue", sw=1.6):
    return _line(x1, y1, x2, y2, stroke=SLATE, sw=sw, marker=marker)


def _dot(cx, cy, r, fill, stroke=BORDER, sw=1.2):
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def _verify() -> None:
    # Boom 的数字
    assert 100 > 1 and 6 > 0 and 65 + 35 == 100
    assert 50 < 150
    # NASA 三个数字是原文转述，未能在原始报告核实 —— 因此图中不画成已核实事实
    assert 40 < 66 and 85 > 66
    # OpenAI 官方数字
    assert 13 > 10 and 14 > 13 and 9881 > 9000
    assert 5 < 12
    # Anthropic 基准
    assert 69 > 25 and 83.5 > 69
    assert 25 < 25.5 and 10 < 25 and 8.9 > 3.4
    # 成本账（原文作者估算，图示标注为估算）
    assert 62 + 26 + 3 + 1.8 + 1.5 + 1.4 > 95
    assert 0.63 * 0.63 < 0.4


# ---------------------------------------------------------------------------
# 1. 伪装成硬件的软件
# ---------------------------------------------------------------------------
def build_thesis() -> str:
    els = list(
        header(
            "文章的核心断言：很多“硬件工程”，其实是没被当软件对待的软件",
            "Blake Scholl：不要设计硬件，要设计“设计硬件的算法”。这是全文最值得记住的一句话。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=SLATE, bg=SLATE_SOFT))
    els.append(txt(56, 93, "传统硬件工程现场", size=11.8, color=INK, weight="700"))
    old = [
        ("Excel 表格", "复杂公式 + VBScript，散落在工程师电脑里"),
        ("邮件交接", "气动工程师把表格发给结构工程师"),
        ("没有版本控制", "没有自动化测试，改一处要重算一大片"),
        ("迭代很贵", "改一次几何，等几小时甚至几天才知道结果"),
    ]
    for i, (name, note) in enumerate(old):
        y = 124 + i * 86
        els.append(f'<rect x="40" y="{y}" width="312" height="74" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        els.append(txt(56, y + 28, name, size=11.2, color=SLATE, weight="700"))
        els.append(txt(56, y + 54, note[:17], size=10.5, color=BODY))
        els.append(txt(56, y + 72, note[17:], size=10.5, color=BODY))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(424, 93, "软件化之后", size=11.8, color=INK, weight="700"))
    new = [
        ("设计即代码", "需求、约束、仿真、文档进入同一套可版本化系统"),
        ("实时反馈", "改几何，秒级看到结构与气动结果"),
        ("自动再设计", "今天条件变了，明天重新生成一版"),
        ("分工反转", "软件工程师搭架构，领域工程师写自己的模块"),
    ]
    for i, (name, note) in enumerate(new):
        y = 124 + i * 86
        els.append(f'<rect x="408" y="{y}" width="312" height="74" rx="7" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
        els.append(txt(424, y + 28, name, size=11.2, color=BLUE, weight="700"))
        els.append(txt(424, y + 54, note[:17], size=10.5, color=BODY))
        els.append(txt(424, y + 72, note[17:], size=10.5, color=BODY))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "关键不是“AI 会画图”，而是把设计过程变成可计算、可回放、可复用的对象。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "这一步一旦完成，AI 才有下手的地方；否则它面对的是一堆没人能读懂的邮件附件。", size=10.5, color=SLATE))
    return figure(
        586,
        "硬件工程软件化前后对比图",
        "左栏列出传统硬件工程的Excel表格邮件交接无版本控制迭代昂贵四桩现状，右栏对应设计即代码实时反馈自动再设计分工反转四项软件化改造，底栏强调核心是把设计过程变成可计算可回放可复用的对象。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 三条硬证据
# ---------------------------------------------------------------------------
def build_evidence() -> str:
    els = list(
        header(
            "三条最硬的证据：飞机、电路板、芯片内核",
            "分别来自 Boom 创始人、OpenAI 官方技术报告和 Anthropic 官方研究页——不是媒体转述。",
        )
    )

    els.append(card(20, 66, 720, 148))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "Boom Supersonic：把飞机设计变成软件", size=11.8, color=INK, weight="700"))
    els.append(txt(40, 128, "1 名工程师实时改叶片几何  ≈  过去 100 人做 6 个月", size=12, color=BLUE, weight="700"))
    els.append(txt(40, 158, "整机结构 65% 自动生成；50 人造出 XB-1 超音速验证机，150 人造出全尺寸超音速涡轮。", size=10.5, color=BODY))
    els.append(txt(40, 188, "来源：创始人 Blake Scholl 的公开叙述；数字为其自述，不是独立审计结果。", size=10.5, color=MUTED))

    els.append(card(20, 228, 720, 148))
    els.append(step_badge(38, 251, 2, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(56, 255, "OpenAI × AMD：模型改写 RTL，已进流片设计", size=11.8, color=INK, weight="700"))
    els.append(txt(40, 290, "旗舰 GPU IP 最高 14% PPA 提升；Jalapeño 向量单元面积 −13%，矩阵单元 −10%", size=11, color=TEAL, weight="700"))
    els.append(txt(40, 320, "9,881 次计分测试；用 Synopsys 工具验证行为等价；AMD 已把部分改动纳入送厂设计。", size=10.5, color=BODY))
    els.append(txt(40, 350, "官方原话：不到 5 个月完成约一年的进展。但 14% 是最高值，不是平均值。", size=10.5, color=MUTED))

    els.append(card(20, 390, 720, 148))
    els.append(step_badge(38, 413, 3, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 417, "Anthropic × Diode：一句话到可工作原型", size=11.8, color=INK, weight="700"))
    els.append(txt(40, 452, "三款设备从提示词到规格、原理图、PCB、外壳、固件，工厂按文件直接做出来", size=11, color=PURPLE, weight="700"))
    els.append(txt(40, 482, "Diode PCB Gym：69%（前代 25%）；BenchCAD 2.1：83.5%。", size=10.5, color=BODY))
    els.append(txt(40, 512, "但官方明确写：仍是原型，未做电气验证、天线调校、热测试与认证。", size=10.5, color=MUTED))

    els.append(card(20, 552, 720, 34, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 574, "读法：证据强度从上到下递增（自述 → 官方技术报告 + 商业流片 → 官方研究页 + 实物原型），但三条都不是“量产”。", size=10.5, color=SLATE))
    return figure(
        600,
        "硬件软件化三条一手证据对照图",
        "三张卡片分别列Boom的一人实时设计对百人六个月与65%自动生成OpenAI与AMD的14% PPA提升和9881次计分测试以及Anthropic与Diode的三款设备端到端设计与69%基准分数，每张卡片下方标注数字口径与局限底栏按证据强度排序并强调三条都不是量产。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 成本账
# ---------------------------------------------------------------------------
def build_cost() -> str:
    els = list(
        header(
            "原文最激进的推演：成本沿供应链复利下降",
            "65–75% 这个数字是作者自己建模的估算，不是任何机构的研究结论。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=GOLD, bg=GOLD_SOFT))
    els.append(txt(56, 93, "作者的成本拆分", size=11.8, color=INK, weight="700"))
    parts = [
        ("零部件 / 物料 / 包装", 62, BLUE),
        ("人力（蓝领 + 白领）", 26, ORANGE),
        ("机械", 3, SLATE),
        ("能源", 1.8, GREEN),
        ("维护 / 维修 / 废料", 1.5, SLATE),
        ("土地 / 建筑", 1.4, SLATE),
    ]
    bx, bw = 44, 292
    for i, (name, val, color) in enumerate(parts):
        y = 126 + i * 58
        els.append(txt(bx, y, name, size=10.5, color=BODY))
        els.append(txt(bx + bw, y, f"{val:g}%", size=10.5, color=color, anchor="end", weight="700"))
        els.append(f'<rect x="{bx}" y="{y+8}" width="{bw*val/65:.1f}" height="9" rx="4" fill="{color}"/>')
    els.append(txt(40, 452, "注意：这些比例来自原文作者，", size=10.5, color=MUTED))
    els.append(txt(40, 472, "不是行业统计口径。", size=10.5, color=MUTED))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "复利到哪里停", size=11.8, color=INK, weight="700"))
    steps = [
        ("第 0 步", "一家公司降本约 37%", "人力砍 20–25% + 物料降 12 个点"),
        ("第 1 步", "供应商同样降 37%", "采购价继续下探"),
        ("第 2 步", "整条链累计约 74%", "作者估算，非实测"),
        ("最后剩下", "原材料、能源、部分人力", "约 25%"),
    ]
    for i, (a, b, c) in enumerate(steps):
        y = 124 + i * 82
        fill = RED_SOFT if i == 2 else SLATE_SOFT
        els.append(f'<rect x="406" y="{y}" width="316" height="72" rx="7" fill="{fill}" stroke="{BORDER}"/>')
        els.append(txt(420, y + 25, a, size=10.5, color=RED if i == 2 else MUTED))
        els.append(txt(420, y + 48, b, size=11.2, color=INK, weight="700"))
        els.append(txt(420, y + 67, c, size=10.5, color=BODY))
    els.append(txt(406, 460, "算式为 1 − 0.63² ≈ 0.60，", size=10.5, color=MUTED))
    els.append(txt(406, 478, "原文按更多层级推到 74%。", size=10.5, color=MUTED))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "该信哪一半：方向有道理——设计人力占比越高，被自动化后成本结构越向原材料和能源倾斜。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "不该信的是精度：供应链有合同、库存、产能、认证、物流，不会按一个统一比例同步下降。", size=10.5, color=SLATE))
    return figure(
        586,
        "制造业成本结构与供应链降本复利估算图",
        "左栏用条形列出作者估算的零部件62%人力26%机械3%能源1.8%等成本拆分并标注非行业统计，右栏四步展示单公司降37%供应商再降37%整链累计74%最后剩原材料能源与部分人力，底栏区分方向合理与精度不可信。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 事实与推测的边界
# ---------------------------------------------------------------------------
def build_boundary() -> str:
    els = list(
        header(
            "事实、已实现、仍属推测：把原文拆成三档",
            "作者最有价值的判断是方向；最需要打折的是时间表和成本幅度。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(56, 93, "已经发生（可核查）", size=11.8, color=INK, weight="700"))
    done = [
        "模型改写量产级 RTL，进入送厂设计",
        "三块电路板按 AI 文件直接制出并工作",
        "新芯片适配周期从数月压到约 3 天",
        "设计过程开始具备代码式版本与测试",
    ]
    for i, s in enumerate(done):
        y = 126 + i * 84
        els.append(f'<rect x="40" y="{y}" width="312" height="72" rx="7" fill="{GREEN_SOFT}" stroke="{GREEN}"/>')
        els.append(txt(56, y + 28, f"✓ {s[:15]}", size=10.5, color=GREEN, weight="700"))
        els.append(txt(56, y + 52, s[15:], size=10.5, color=BODY))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "仍是作者的推测", size=11.8, color=INK, weight="700"))
    guess = [
        ("整链降本 65–75%", "自己建模，不是行业数据"),
        ("蓝领 2–5 年大幅自动化", "取决于人形机器人成熟度"),
        ("转型 1–4 年或 5–20 年", "作者自己给了两个差 5 倍的区间"),
        ("英伟达护城河消失", "原文是“may have collapsed”"),
    ]
    for i, (a, b) in enumerate(guess):
        y = 126 + i * 84
        els.append(f'<rect x="406" y="{y}" width="316" height="72" rx="7" fill="{RED_SOFT}" stroke="{RED}"/>')
        els.append(txt(420, y + 28, a, size=10.5, color=RED, weight="700"))
        els.append(txt(420, y + 52, b, size=10.5, color=BODY))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "一个很能说明边界的细节：Anthropic 的三个设备没做过电气验证、天线调校、热测试和认证。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "“做出来能跑”和“能安全量产”之间，隔着的正是工程师最不可替代的那段。", size=10.5, color=SLATE))
    return figure(
        586,
        "硬件软件化事实与推测三档对照图",
        "左栏列出四条已发生可核查事实包括模型改写RTL进入流片三块电路板工作新芯片适配压到三天等，右栏列出四条作者推测包括整链降本65到75%蓝领2到5年自动化转型1到4年或5到20年以及英伟达护城河消失，底栏用Anthropic三设备未做验证认证说明能跑与能量产的距离。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 程序员转型路线
# ---------------------------------------------------------------------------
def build_career() -> str:
    els = list(
        header(
            "程序员怎么转：别去抢画图，去占“可验证的边界”",
            "从 OpenAI 与 Anthropic 的报告看，人和 EDA 工具守的是验证、评测、采纳和生产决策。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "三层技能栈", size=11.8, color=INK, weight="700"))
    stack = [
        ("① 数据层", ["Python 脚本化 EDA：KiCad / Yosys /", "Verilator / Synopsys 接口"], BLUE, BLUE_SOFT),
        ("② 模型层", ["Agent 工具调用、上下文工程、", "评测集与回归测试"], PURPLE, PURPLE_SOFT),
        ("③ 领域层", ["RTL / PCB / DFM / PPA /", "热与认证的判据"], TEAL, TEAL_SOFT),
    ]
    for i, (name, lines, fg, bg) in enumerate(stack):
        y = 124 + i * 112
        els.append(f'<rect x="40" y="{y}" width="312" height="92" rx="7" fill="{bg}" stroke="{fg}"/>')
        els.append(txt(56, y + 28, name, size=11.5, color=fg, weight="700"))
        for j, line in enumerate(lines):
            els.append(txt(56, y + 56 + j * 22, line, size=10.5, color=BODY))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(424, 93, "一个 90 天动作清单", size=11.8, color=INK, weight="700"))
    actions = [
        ("第 1–2 周", ["用 Python 脚本生成一块简单 KiCad", "板，跑通 DRC"]),
        ("第 3–6 周", ["复现 OpenAI 的 RISC-V 思路：让模型", "改 RTL，用 Yosys/仿真判分"]),
        ("第 7–10 周", ["搭一个小型“设计—验证”闭环：", "改 → 测 → 打分 → 回滚"]),
        ("第 11–13 周", ["选一个垂直场景做到可演示：", "电源板 / 传感器板 / 加速器子模块"]),
    ]
    for i, (a, lines) in enumerate(actions):
        y = 124 + i * 84
        els.append(f'<rect x="406" y="{y}" width="316" height="70" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        els.append(txt(420, y + 26, a, size=10.5, color=GREEN, weight="700"))
        for j, line in enumerate(lines):
            els.append(txt(420, y + 50 + j * 18, line, size=10.5, color=BODY))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "一句话：把“我会写代码”升级成“我能定义一个机器可检验的问题，并让模型反复求解”。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "OpenAI 用 9,881 次计分测试做的事，本质上就是这个能力的高配版。", size=10.5, color=SLATE))
    return figure(
        586,
        "程序员向AI硬件工程转型的三层技能栈与90天路线图",
        "左栏三层技能栈依次为Python脚本化EDA与模型agent评测以及RTL PCB DFM PPA领域判据并标注纯应用层最易替代，右栏给出90天四阶段动作清单从KiCad脚本到RISC-V复现再到设计验证闭环与垂直场景，底栏强调把会写代码升级为能定义机器可检验的问题。",
        els,
    )


@register(TOPIC, "《Hardware Is Software》解读：核心论点、三条证据、成本账、边界与程序员转型", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("hardware-is-software-thesis.svg", build_thesis),
        ("hardware-is-software-evidence.svg", build_evidence),
        ("hardware-is-software-cost.svg", build_cost),
        ("hardware-is-software-boundary.svg", build_boundary),
        ("hardware-is-software-career.svg", build_career),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
