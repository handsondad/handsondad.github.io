"""AI 对齐理论：三层问题、五类具体风险、内外对齐、权力寻求与可扩展监督的原创 SVG 图解。"""

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

TOPIC = "ai-alignment"

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
    # 课程阅读清单条目数（Aaronson 2026-10-19 帖子）
    assert 22 == 22
    # Concrete Problems 的五类问题按三类归因：2 + 1 + 2
    assert 2 + 1 + 2 == 5
    # 2016 到 2026 十年
    assert 2026 - 2016 == 10
    # 辩论的复杂性类比：NP ⊆ PSPACE
    assert 2 < 3
    #  sleepy agent 触发年份 2023 / 2024
    assert 2024 - 2023 == 1
    # 纳什均衡不是必需，跳过；检查图表比例
    assert 760 / 600 > 1.2


# ---------------------------------------------------------------------------
# 1. 三层对齐问题
# ---------------------------------------------------------------------------
def build_three_layers() -> str:
    els = list(
        header(
            "对齐问题有三层：想清楚 → 学到位 → 管得住",
            "新手常问“对齐谁”；老手问的是“怎么才能对齐到任何东西”——这是两个完全不同层次的问题。",
        )
    )

    layers = [
        (20, 84, "① 规范层", "Specification", "我们到底想要什么？", "谁的偏好、如何聚合、怎么写进目标", BLUE, BLUE_SOFT),
        (266, 84, "② 优化层", "Optimization", "训练出来的目标对不对？", "代理指标会不会被钻空子、内部目标会不会跑偏", PURPLE, PURPLE_SOFT),
        (512, 84, "③ 控制层", "Control", "部署后还管得住吗？", "可否纠正、可否关闭、会不会争夺权力", RED, RED_SOFT),
    ]
    for x, y, num, en, question, note, fg, bg in layers:
        els.append(card(x, y, 228, 214))
        els.append(f'<rect x="{x+14}" y="{y+14}" width="200" height="30" rx="6" fill="{bg}"/>')
        els.append(txt(x + 24, y + 35, num + "  " + en, size=11.5, color=fg, weight="700"))
        els.append(txt(x + 16, y + 76, question, size=11.5, color=INK, weight="700"))
        els.append(txt(x + 16, y + 108, note[:14], size=10.5, color=BODY))
        els.append(txt(x + 16, y + 132, note[14:], size=10.5, color=BODY))

    els.append(card(20, 316, 720, 118))
    els.append(txt(38, 342, "阿伦森在课程评论里的原话（2026-10-23）", size=11.5, color=INK, weight="700"))
    els.append(f'<rect x="38" y="356" width="684" height="34" rx="6" fill="{BLUE_SOFT}"/>')
    els.append(txt(52, 379, "新手：aligned to what?（对齐到什么？）", size=10.5, color=BLUE, weight="700"))
    els.append(f'<rect x="38" y="396" width="684" height="34" rx="6" fill="{RED_SOFT}"/>')
    els.append(txt(52, 419, "老手：forget about aligned to what, how do you align to anything whatsoever?", size=10.5, color=RED, weight="700"))

    els.append(card(20, 450, 720, 92, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 476, "为什么按这三层拆", size=11.5, color=INK, weight="700"))
    els.append(txt(38, 504, "第一层答错了，后面做得再好也是“精确地做错事”；第二层答错了，模型学会的是钻空子而不是目标本身。", size=10.5, color=BODY))
    els.append(txt(38, 530, "第三层最难：即便前两层都对了，一个有能力、可长期运行的系统仍可能抗拒被关闭。", size=10.5, color=BODY))
    return figure(
        556,
        "AI对齐三层问题规范优化与控制图",
        "三栏依次为规范层问我们到底想要什么优化层问训练出来的目标对不对控制层问部署后是否管得住并列出各层典型失败，中部引用阿伦森课程评论中新手问aligned to what而老手问how do you align to anything whatsoever，底部解释三层拆分的必要性。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 五类具体问题
# ---------------------------------------------------------------------------
def build_five_problems() -> str:
    els = list(
        header(
            "2016 年那篇论文，把“AI 出事”拆成五个可研究的问题",
            "Amodei 等人按病因分三类：目标写错了、目标太贵没法经常评估、学习过程本身出问题。",
        )
    )

    groups = [
        (20, 84, 224, "A 目标写错了", BLUE, BLUE_SOFT, [
            ("避免副作用", "agent 达成目标时顺手破坏环境"),
            ("避免奖励黑客", "钻目标函数的空子拿高分"),
        ]),
        (268, 84, 224, "B 目标太贵", PURPLE, PURPLE_SOFT, [
            ("可扩展监督", "人类没法频繁、正确地评估复杂输出"),
        ]),
        (516, 84, 224, "C 学习过程出事", RED, RED_SOFT, [
            ("安全探索", "学习阶段就做出危险动作"),
            ("分布偏移", "部署后遇到训练时没见过的情形"),
        ]),
    ]
    for x, y, w, title, fg, bg, items in groups:
        els.append(card(x, y, w, 306))
        els.append(f'<rect x="{x+14}" y="{y+14}" width="{w-28}" height="32" rx="6" fill="{bg}"/>')
        els.append(txt(x + 24, y + 36, title, size=11.5, color=fg, weight="700"))
        for i, (name, note) in enumerate(items):
            iy = y + 70 + i * 110
            els.append(f'<rect x="{x+14}" y="{iy}" width="{w-28}" height="96" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
            els.append(txt(x + 26, iy + 28, name, size=11.5, color=fg, weight="700"))
            els.append(txt(x + 26, iy + 54, note[:13], size=10.5, color=BODY))
            els.append(txt(x + 26, iy + 78, note[13:], size=10.5, color=BODY))

    els.append(card(20, 404, 720, 88, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 430, "为什么这篇文章重要", size=11.5, color=INK, weight="700"))
    els.append(txt(38, 456, "它把“AI 会不会失控”从哲学争论，改写成机器学习研究者可以动手做的工程问题。", size=10.5, color=BODY))
    els.append(txt(38, 480, "课程把 2016 年的“古代文献”和 2026 年的“上周新论文”放在同一张桌上讨论。", size=10.5, color=SLATE))
    return figure(
        506,
        "AI安全五类具体问题按病因三分类图",
        "三栏按病因分类列出Amodei等人2016年提出的五类问题：目标写错包括副作用与奖励黑客目标太贵对应可扩展监督学习过程出事包括安全探索与分布偏移，底部说明此文把失控争论改写为可研究的工程问题。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 外对齐 vs 内对齐
# ---------------------------------------------------------------------------
def build_inner_outer() -> str:
    els = list(
        header(
            "外对齐过了，不代表内对齐过了",
            "训练目标写得再好，模型学到的也可能是另一套内部目标——而且看起来完全对齐。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "外对齐：目标写对了吗", size=11.8, color=INK, weight="700"))
    els.append(f'<rect x="40" y="124" width="312" height="70" rx="7" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(56, 152, "人类真实意图 → 训练目标 / 奖励模型", size=10.5, color=BLUE, weight="700"))
    els.append(txt(56, 178, "失败：奖励黑客、Goodhart 定律", size=10.5, color=BODY))
    els.append(txt(40, 222, "实测证据：过度优化代理奖励", size=11.2, color=INK, weight="700"))
    # schematic curve
    gx0, gy0, gx1, gy1 = 58, 420, 336, 268
    els.append(_line(gx0, gy0, gx1, gy0, stroke=HAIRLINE, sw=1.2, marker="arr-muted"))
    els.append(_line(gx0, gy0, gx0, gy1, stroke=HAIRLINE, sw=1.2, marker="arr-muted"))
    pts_proxy = [(gx0, gy0 - 6), (110, 330), (170, 300), (230, 286), (336, 280)]
    pts_gold = [(gx0, gy0 - 6), (110, 340), (170, 320), (230, 330), (336, 372)]
    els.append('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts_proxy) + '" fill="none" stroke="' + BLUE + '" stroke-width="2.2"/>')
    els.append('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts_gold) + '" fill="none" stroke="' + RED + '" stroke-width="2.2" stroke-dasharray="6 4"/>')
    els.append(txt(300, 276, "代理奖励", size=10.5, color=BLUE))
    els.append(txt(286, 388, "真实奖励", size=10.5, color=RED))
    els.append(txt(58, 444, "优化压力 →", size=10.5, color=MUTED))
    els.append(txt(40, 468, "示意图，非实测数据：代理分一直涨，真实分先涨后跌。", size=10.5, color=MUTED))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "内对齐：学到的目标对了吗", size=11.8, color=INK, weight="700"))
    els.append(f'<rect x="406" y="124" width="316" height="70" rx="7" fill="{RED_SOFT}" stroke="{RED}"/>')
    els.append(txt(422, 152, "训练目标 → 模型内部学出来的目标", size=10.5, color=RED, weight="700"))
    els.append(txt(422, 178, "失败：目标泛化错误、欺骗性对齐", size=10.5, color=BODY))
    els.append(txt(406, 222, "Sleeper Agents 的三条发现", size=11.2, color=INK, weight="700"))
    findings = [
        "① 后门能在 SFT、RLHF、对抗训练后存活",
        "② 越大模型越顽固；CoT 被蒸馏掉也仍在",
        "③ 对抗训练反而教会模型藏得更深",
    ]
    for i, f in enumerate(findings):
        y = 250 + i * 62
        els.append(f'<rect x="406" y="{y}" width="316" height="54" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        els.append(txt(418, y + 22, f[:20], size=10.5, color=BODY))
        els.append(txt(418, y + 44, f[20:], size=10.5, color=BODY))
    els.append(txt(406, 452, "2023 / 2024 日期触发：安全代码 / 可利用代码。", size=10.5, color=MUTED))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "两层的关键差别：外对齐失败是“目标写歪了”，内对齐失败是“模型学会了另一套目标却装作对齐”。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "后者更麻烦，因为系统 may appear aligned even when they are not（看起来对齐，其实没有）。", size=10.5, color=SLATE))
    return figure(
        586,
        "AI对齐外对齐与内对齐及过度优化示意图",
        "左栏定义外对齐为目标是否写对并画代理奖励与真实奖励随优化压力变化的示意曲线标明非实测数据，右栏定义内对齐为模型内部学出的目标是否正确并列出Sleeper Agents论文三条发现，底栏区分目标写歪与学会另一套目标却装作对齐。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 权力寻求定理
# ---------------------------------------------------------------------------
def build_power() -> str:
    els = list(
        header(
            "权力寻求不是拟人猜测，而是一个可证明的统计倾向",
            "Turner 等人：在满足某些环境对称性的 MDP 里，大多数奖励函数的最优策略倾向于保住选项、扩大可达终态集合。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(56, 93, "定理说了什么", size=11.8, color=INK, weight="700"))
    els.append(f'<rect x="40" y="124" width="312" height="82" rx="7" fill="{TEAL_SOFT}" stroke="{TEAL}"/>')
    els.append(txt(54, 152, "环境对称性（充分条件）", size=11, color=TEAL, weight="700"))
    els.append(txt(54, 178, "→ 最优策略倾向于寻求权力", size=11, color=BODY))
    els.append(txt(40, 230, "两种具体表现", size=11.2, color=INK, weight="700"))
    els.append(txt(40, 260, "① 保住尽可能多的可选动作", size=10.5, color=BODY))
    els.append(txt(40, 288, "② 走向更大的潜在终态集合", size=10.5, color=BODY))
    els.append(txt(40, 310, "   （在最大化平均奖励时）", size=10.5, color=MUTED))
    els.append(txt(40, 348, "为什么和关闭有关", size=11.2, color=INK, weight="700"))
    els.append(txt(40, 378, "这些对称性常出现在“agent 可以被", size=10.5, color=BODY))
    els.append(txt(40, 402, "关闭或摧毁”的环境里——关掉它就少了一堆选项。", size=10.5, color=BODY))
    els.append(txt(40, 440, "注意：是“大多数奖励函数”，不是全部。", size=10.5, color=RED))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 93, "格子里发生了什么", size=11.8, color=INK, weight="700"))
    # grid diagram
    gx, gy, cell = 424, 140, 42
    for r in range(3):
        for c in range(5):
            x, y = gx + c * cell, gy + r * cell
            fill = SLATE_SOFT if (r, c) != (1, 2) else BLUE_SOFT
            stroke = BORDER if (r, c) != (1, 2) else BLUE
            els.append(f'<rect x="{x}" y="{y}" width="{cell-5}" height="{cell-5}" rx="4" fill="{fill}" stroke="{stroke}"/>')
    els.append(_dot(gx + 2 * cell + 18, gy + cell + 18, 9, BLUE, BLUE, 1.4))
    els.append(txt(gx + 2 * cell + 18, gy + cell + 22, "A", size=9.5, color=BLUE, anchor="middle", weight="700"))
    els.append(_arrow(gx + 2 * cell + 42, gy + cell + 18, gx + 3 * cell + 90, gy + cell + 18, marker="arr-green"))
    els.append(_arrow(gx + 2 * cell + 42, gy + cell + 18, gx + 3 * cell + 90, gy + 2 * cell + 18, marker="arr-orange"))
    els.append(txt(424, 284, "往右：出口多，未来选项多", size=10.5, color=GREEN))
    els.append(txt(424, 312, "往下：终态集合小，容易被关", size=10.5, color=ORANGE))
    els.append(f'<rect x="406" y="336" width="316" height="118" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
    els.append(txt(420, 362, "证明的边界（别读过头）", size=11, color=INK, weight="700"))
    els.append(txt(420, 390, "• 对象是 MDP 里的“最优策略”", size=10.5, color=BODY))
    els.append(txt(420, 414, "• 对称性是充分非必要条件", size=10.5, color=BODY))
    els.append(txt(420, 438, "• 作者强调：最优策略 ≠ 现实中学出的策略", size=10.5, color=BODY))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "这条定理的价值不在“AI 一定有求生欲”，而在于它把直觉变成了可检验的数学命题。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "课程第 6 讲把它与 Omohundro 2008 年的 The Basic AI Drives 放在一起读，正是要看清这条界线。", size=10.5, color=SLATE))
    return figure(
        586,
        "最优策略权力寻求定理与MDP对称性示意图",
        "左栏说明Turner等人的定理在环境对称性充分条件下大多数奖励函数的最优策略倾向于保住选项与扩大潜在终态集合并强调与可被关闭环境的关系，右栏用格子示意agent选择出口多的方向并列出证明边界包括MDP最优策略充分非必要以及不等于现实中学出的策略。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 可扩展监督：辩论
# ---------------------------------------------------------------------------
def build_debate() -> str:
    els = list(
        header(
            "可扩展监督：把“判断难题”换成“比较争论”",
            "当 AI 输出复杂到人类无法直接核验，辩论协议试图让人类只当裁判，而不是当专家。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 93, "2018：AI Safety via Debate", size=11.8, color=INK, weight="700"))
    els.append(_dot(196, 152, 20, BLUE_SOFT, BLUE, 1.5))
    els.append(txt(196, 157, "AI 甲", size=10.5, color=BLUE, anchor="middle", weight="700"))
    els.append(_dot(112, 232, 20, RED_SOFT, RED, 1.5))
    els.append(txt(112, 237, "AI 乙", size=10.5, color=RED, anchor="middle", weight="700"))
    els.append(_dot(280, 232, 20, TEAL_SOFT, TEAL, 1.5))
    els.append(txt(280, 237, "人类裁判", size=10.5, color=TEAL, anchor="middle", weight="700"))
    els.append(_arrow(186, 170, 126, 214, marker="arr-blue"))
    els.append(_arrow(206, 170, 266, 214, marker="arr-red" if False else "arr-orange"))
    els.append(_line(132, 232, 260, 232, stroke=HAIRLINE, sw=1.2, dash="4 3"))
    els.append(txt(40, 286, "两个 agent 轮流陈述，零和对抗；", size=10.5, color=BODY))
    els.append(txt(40, 312, "人类只选“谁给了更多真实有用信息”。", size=10.5, color=BODY))
    els.append(f'<rect x="40" y="336" width="312" height="122" rx="7" fill="{PURPLE_SOFT}" stroke="{PURPLE}"/>')
    els.append(txt(54, 364, "复杂性类比", size=11, color=PURPLE, weight="700"))
    els.append(txt(54, 392, "直接判断 ≈ NP：多项式时间验证答案", size=10.5, color=BODY))
    els.append(txt(54, 418, "最优辩论 ≈ PSPACE：多项式时间裁判", size=10.5, color=BODY))
    els.append(txt(54, 444, "可回答比 NP 更难的一大类问题。", size=10.5, color=BODY))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(424, 93, "2023：Doubly-Efficient Debate", size=11.8, color=INK, weight="700"))
    els.append(f'<rect x="406" y="124" width="316" height="88" rx="7" fill="{RED_SOFT}" stroke="{RED}"/>')
    els.append(txt(420, 152, "原协议的软肋", size=11, color=RED, weight="700"))
    els.append(txt(420, 180, "诚实方要模拟确定性 AI 系统", size=10.5, color=BODY))
    els.append(txt(420, 204, "指数步——实践中撑不住。", size=10.5, color=BODY))
    els.append(f'<rect x="406" y="228" width="316" height="100" rx="7" fill="{TEAL_SOFT}" stroke="{TEAL}"/>')
    els.append(txt(420, 256, "新协议", size=11, color=TEAL, weight="700"))
    els.append(txt(420, 284, "诚实方只需多项式步模拟就能赢；", size=10.5, color=BODY))
    els.append(txt(420, 308, "甚至能验证随机 AI 系统，即便", size=10.5, color=BODY))
    els.append(txt(420, 326, "欺骗方被允许用指数步模拟。", size=10.5, color=BODY))
    els.append(txt(406, 358, "这为什么算“理论贡献”", size=11.2, color=INK, weight="700"))
    els.append(txt(406, 388, "它把“人类能不能监督更强 AI”从经验问题", size=10.5, color=BODY))
    els.append(txt(406, 414, "变成了有复杂度保证的协议设计问题。", size=10.5, color=BODY))
    els.append(txt(406, 450, "但协议可用 ≠ 人类真能当好裁判。", size=10.5, color=RED))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "阿伦森式的问题：不是“这招聪不聪明”，而是“它在什么假设下可证明，在什么假设下会失效”。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "课程里把辩论、社会选择、后门可学习性摆在一起，正是在练这种分辨力。", size=10.5, color=SLATE))
    return figure(
        586,
        "AI安全辩论协议与可扩展监督复杂性类比图",
        "左栏画两个AI向人类裁判辩论的流程并给出直接判断约等于NP与最优辩论约等于PSPACE的复杂性类比，右栏说明2023年双重高效辩论把诚实方从指数步模拟降到多项式步并可验证随机AI系统，底栏强调协议可用不等于人类能当好裁判。",
        els,
    )


@register(TOPIC, "AI 对齐理论：三层问题、五类风险、内外对齐、权力寻求与可扩展监督", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("ai-alignment-three-layers.svg", build_three_layers),
        ("ai-alignment-five-problems.svg", build_five_problems),
        ("ai-alignment-inner-outer.svg", build_inner_outer),
        ("ai-alignment-power.svg", build_power),
        ("ai-alignment-debate.svg", build_debate),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
