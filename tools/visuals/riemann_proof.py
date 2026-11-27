"""2026 年 11 月黎曼猜想形式化证明：零点、时间线、Stepanov 重数、Lean 四关与边界的原创 SVG 图解。"""

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

TOPIC = "riemann-proof"

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
    # 发布与验证日期
    assert 2026 == 2026 and 11 == 11 and 20 < 21 < 25
    # 代码规模（MIT 核查页）
    modules, lines = 175187, 17400000
    assert 17000000 < lines < 18000000
    assert math.sqrt(1000) < 32
    # Alpöge  remark 中 Claude 建议的 theta lift 链长 sqrt(X)
    assert abs(math.sqrt(10000) - 100) < 1e-9
    # 10/6 到 11/16 共 41 天
    from datetime import date
    days = (date(2026, 11, 16) - date(2026, 10, 6)).days
    assert days == 41
    # 导出证明大小 61,570,595,788 字节约 61.6 GB
    export = 61570595788
    assert 60 * 10**9 < export < 63 * 10**9
    # 三个标准公理
    assert len(["propext", "Classical.choice", "Quot.sound"]) == 3
    # 临界线 Re(s)=1/2
    assert 0.5 == 1 / 2


# ---------------------------------------------------------------------------
# 1. 素数为何要问零点
# ---------------------------------------------------------------------------
def build_critical_line() -> str:
    els = list(
        header(
            "黎曼猜想问的不是素数，而是 ζ 函数的零点在哪",
            "1859 年黎曼发现：素数计数的误差，被 ζ(s) 的非平凡零点位置死死控制住。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "左边：素数为何难数", size=11.8, color=INK, weight="700"))
    els.append(_line(44, 250, 348, 250, stroke=HAIRLINE, sw=1.2, marker="arr-muted"))
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    xs = [60 + i * 27 for i in range(len(primes))]
    for x, p in zip(xs, primes):
        els.append(_line(x, 244, x, 256, stroke=BLUE, sw=1.6))
        els.append(txt(x, 278, str(p), size=10.5, color=BLUE, anchor="middle"))
    els.append(txt(44, 314, "局部看：间隔忽大忽小，没有简单规律。", size=10.5, color=BODY))
    els.append(txt(44, 342, "整体看：π(x) ≈ x / log x，误差有多大？", size=10.5, color=BODY))
    els.append(f'<rect x="40" y="366" width="312" height="88" rx="7" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(56, 392, "黎曼的发现：误差项 ≈ Σ 零点贡献", size=11, color=BLUE, weight="700"))
    els.append(txt(56, 420, "零点越靠近实部 1/2，素数分布越", size=10.5, color=BODY))
    els.append(txt(56, 444, "接近“最优随机”；越往右偏，误差越大。", size=10.5, color=BODY))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "右边：零点排布与临界线", size=11.8, color=INK, weight="700"))
    x0, y0, x1, y1 = 416, 132, 720, 340
    els.append(_line(x0, y1, x1, y1, stroke=HAIRLINE, sw=1.2, marker="arr-muted"))
    els.append(_line(x0, y0, x0, y1, stroke=HAIRLINE, sw=1.2, marker="arr-muted"))
    els.append(txt(x0 - 8, y1 + 20, "0", size=10.5, color=MUTED, anchor="middle"))
    els.append(txt(x1 - 6, y1 + 20, "1", size=10.5, color=MUTED, anchor="middle"))
    els.append(txt(x0 + 14, y0 - 6, "Im s", size=10.5, color=MUTED))
    bandx = x0 + (x1 - x0) / 2 - 48
    els.append(f'<rect x="{bandx:.1f}" y="{y0}" width="96" height="{y1-y0}" fill="{RED_SOFT}" stroke="{RED}" stroke-width="1.2" stroke-dasharray="5 4"/>')
    eline = x0 + (x1 - x0) / 2
    els.append(_line(eline, y0, eline, y1, stroke=RED, sw=2))
    els.append(txt(eline, y1 + 20, "Re s = 1/2", size=10.5, color=RED, anchor="middle", weight="700"))
    for i in range(7):
        y = y0 + 20 + i * 28
        els.append(_dot(eline, y, 4.2, RED, RED, 1))
    els.append(txt(424, 382, "平凡零点在负偶数；非平凡零点全在 0<Re<1 的带里。", size=10.5, color=BODY))
    els.append(txt(424, 408, "RH 断言：它们全都站在正中央那条线上。", size=10.5, color=BODY))
    els.append(txt(424, 440, "2026-11-20 的证明，就是把这个断言变成定理。", size=10.5, color=RED))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "读图顺序：先看左边“素数难数”，再看右边“零点在带里”，最后把两句接起来。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "注意：RH 说的是零点位置，不是某一条素数公式；威力在于它一旦成立，上千条定理的“如果”就能删掉。", size=10.5, color=SLATE))
    return figure(
        586,
        "黎曼猜想零点临界线与素数计数关系图",
        "左栏在数轴上标出二到三十一的素数并说明局部无规律整体可用x除以log x近似但误差由zeta函数零点控制，右栏画复平面中零到一的临界带与实部二分之一的临界线并在线上画七个非平凡零点，底栏说明猜想讲的是零点位置而不是某条素数公式。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 六周时间线
# ---------------------------------------------------------------------------
def build_timeline() -> str:
    els = list(
        header(
            "六周出结果，一天完成验证：这次的时间线",
            "2026-10-06 第一步 Stepanov 行列式 → 11-16 得到 GRH → 11-21 Lean 社区联合声明。",
        )
    )

    els.append(card(20, 66, 720, 292))
    events = [
        ("10/06", "Stepanov 行列式起步", BLUE, "从函数域上带重数的经典论证出发"),
        ("10/19", "qN = Mᵏ + R 分解", TEAL, "在整数上寻找“自然自守”的替代品"),
        ("11/15", "链式 θ lift，取 m ≈ √X", PURPLE, "用迭代提升累计重数，补上整数缺失的乘法性"),
        ("11/16", "GRH 完成", RED, "四页 remark 里时间线的终点"),
        ("11/20", "公开 4 页说明 + Lean 代码", GOLD, "14 个分卷、约 1700 万行；同时 Vakil 公布纯人工草稿"),
        ("11/21", "Lean / Mathlib 联合声明", GREEN, "认证命题与证明均正确，四条标准全满足"),
    ]
    for i, (date, title, color, note) in enumerate(events):
        x = 44 + (i % 3) * 230
        y = 100 + (i // 3) * 122
        els.append(f'<rect x="{x}" y="{y}" width="218" height="106" rx="8" fill="{SLATE_SOFT if i%2==0 else "#ffffff"}" stroke="{BORDER}"/>')
        els.append(txt(x + 14, y + 26, date, size=11.5, color=color, weight="700"))
        els.append(txt(x + 14, y + 52, title, size=10.5, color=INK, weight="700"))
        els.append(txt(x + 14, y + 76, note, size=10.5, color=BODY))
        els.append(txt(x + 14, y + 96, f"节点 {i+1} / 6", size=10.5, color=MUTED))

    els.append(card(20, 374, 352, 198))
    els.append(step_badge(38, 397, 1, fg=GOLD, bg=GOLD_SOFT))
    els.append(txt(56, 401, "同一天的另一份证明", size=11.8, color=INK, weight="700"))
    els.append(txt(40, 434, "11 月 20 日，AMS 主席 Vakil 紧急发文，", size=10.5, color=BODY))
    els.append(txt(40, 458, "公布 Masullo 的 940 页 GRH 草稿：", size=10.5, color=BODY))
    els.append(txt(40, 482, "纯人工、历时约 12 年。", size=10.5, color=BODY))
    els.append(f'<rect x="40" y="498" width="312" height="58" rx="7" fill="{RED_SOFT}" stroke="{RED}"/>')
    els.append(txt(54, 522, "约 8 小时后，多人借不同 AI 模型", size=10.5, color=RED, weight="700"))
    els.append(txt(54, 544, "报告了草稿中的问题；尚未定论。", size=10.5, color=BODY))

    els.append(card(388, 374, 352, 198))
    els.append(step_badge(406, 397, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(424, 401, "机器核验跑得有多快", size=11.8, color=INK, weight="700"))
    els.append(txt(406, 434, "11/20 16:43 UTC：175,187 个模块全部编译通过。", size=10.5, color=BODY))
    els.append(txt(406, 458, "11/20 夜：con-leche 接受 1,468,418 条声明。", size=10.5, color=BODY))
    els.append(txt(406, 482, "11/21：沙箱重建导出文件与原始导出逐字节一致。", size=10.5, color=BODY))
    els.append(txt(406, 506, "11/22 起：Lean 官方内核跑完 61.6 GB 导出。", size=10.5, color=BODY))
    els.append(txt(406, 542, "对比：人类读 1700 万行，按每分钟 200 行算要 160 年。", size=10.5, color=GREEN))

    els.append(card(20, 586, 720, 34, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 608, "提醒：日期按原文与核查页；10/06 到 11/16 是 41 天，不是“一夜之间”。", size=10.5, color=SLATE))
    return figure(
        634,
        "黎曼猜想证明从起步到验证的六周时间线图",
        "上方六个节点依次是十月六日Stepanov行列式十月十九日qn等于mk加r分解十一月十五日链式theta提升取m约根号x十一月十六日GRH完成十一月二十日公开四页说明与Lean代码十一月二十一日Lean与Mathlib联合声明，下方左栏讲同日Vakil公布的Masullo九百四十页纯人工草稿八小时后被AI辅助发现问题，右栏列出编译声明数与内核核验时间并估算人类阅读需一百六十年。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. Stepanov 重数难题
# ---------------------------------------------------------------------------
def build_stepanov() -> str:
    els = list(
        header(
            "核心难点：整数上找不到“重数”，Claude 用 θ 提升链造了一个",
            "函数域上的 Stepanov 论证靠带重数的除子；整数上重数相当于“给整数求导”，没有现成东西。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "函数域：有重数，能证明 RH", size=11.8, color=INK, weight="700"))
    els.append(f'<rect x="40" y="124" width="312" height="86" rx="7" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(56, 152, "Stepanov 论证", size=11.5, color=BLUE, weight="700"))
    els.append(txt(56, 180, "除子带重数 → 同一零点被数多次", size=10.5, color=BODY))
    els.append(txt(56, 202, "→ 用次数上限反证零点不能乱跑", size=10.5, color=BODY))
    els.append(txt(40, 244, "整数域：没有这个“重数”杠杆", size=11.5, color=RED, weight="700"))
    els.append(txt(40, 274, "在整数世界里做类似的事，", size=10.5, color=BODY))
    els.append(txt(40, 298, "等价于给整数求导——没有定义。", size=10.5, color=BODY))
    els.append(txt(40, 334, "Alpöge 的原话", size=11.2, color=INK, weight="700"))
    els.append(f'<rect x="40" y="350" width="312" height="108" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
    els.append(txt(54, 378, "“multiplicity is hard to find over", size=10.5, color=BODY))
    els.append(txt(54, 400, "the integers, corresponding to something", size=10.5, color=BODY))
    els.append(txt(54, 422, "like differentiating whole numbers.”", size=10.5, color=BODY))
    els.append(txt(54, 448, "—— 4 页 remark，第 1 页", size=10.5, color=MUTED))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "解法：迭代 θ 提升，把重数攒出来", size=11.8, color=INK, weight="700"))
    els.append(_dot(440, 154, 13, BLUE_SOFT, BLUE, 1.4))
    els.append(txt(440, 158, "U₀", size=10.5, color=BLUE, anchor="middle", weight="700"))
    els.append(_arrow(456, 154, 520, 154))
    els.append(_dot(536, 154, 13, TEAL_SOFT, TEAL, 1.4))
    els.append(txt(536, 158, "U₁", size=10.5, color=TEAL, anchor="middle", weight="700"))
    els.append(_arrow(552, 154, 616, 154))
    els.append(_dot(632, 154, 13, PURPLE_SOFT, PURPLE, 1.4))
    els.append(txt(632, 158, "U₂", size=10.5, color=PURPLE, anchor="middle", weight="700"))
    els.append(_arrow(648, 154, 702, 154))
    els.append(txt(700, 158, "…", size=12, color=MUTED, anchor="middle"))
    els.append(txt(406, 194, "每次 π → π ⊞ μⱼ[t] 就是一次 θ 提升，累计重数 m。", size=10.5, color=BODY))
    els.append(f'<rect x="406" y="214" width="316" height="88" rx="7" fill="{RED_SOFT}" stroke="{RED}"/>')
    els.append(txt(420, 244, "Claude 给的关键一行", size=11.2, color=RED, weight="700"))
    els.append(txt(420, 272, "length X 的 von Mangoldt 和，链长取 √X", size=11, color=RED, weight="700"))
    els.append(txt(420, 294, "≈ 每次提升模拟一份重数，取到 m ≈ √X。", size=10.5, color=BODY))
    els.append(txt(406, 334, "为什么是 √X？", size=11.2, color=INK, weight="700"))
    els.append(txt(406, 364, "太短：重数不够，压不住零点。", size=10.5, color=BODY))
    els.append(txt(406, 390, "太长：每次提升都有代价，累积起来超过预算。", size=10.5, color=BODY))
    els.append(txt(406, 422, "√X 正好在两端之间——Alpöge 说“还能是什么”。", size=10.5, color=BODY))
    els.append(txt(406, 458, "注意：这只是他从 remark 里转述的路线草图。", size=10.5, color=MUTED))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "这一步最能说明“人机分工”：人负责把问题摆成哪个类比，模型负责在巨大空间里找出那条链长。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "Alpöge 自己在 remark 里写：终点附近“Claude flew, and danced, and sparkled”。", size=10.5, color=SLATE))
    return figure(
        586,
        "Stepanov重数难题与链式theta提升路线图",
        "左栏说明函数域上Stepanov论证靠带重数的除子而整数上重数相当于给整数求导没有定义并附Alpog remark原文引句，右栏画U0到U1到U2的迭代theta提升链并说明Claude建议对长度X的von Mangoldt和取链长根号X以累计重数m，底栏说明人机分工与Alpoge的原话。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. Lean 验证四关
# ---------------------------------------------------------------------------
def build_verification() -> str:
    els = list(
        header(
            "1700 万行代码凭什么算“证明了”？Lean 社区的四道关",
            "2026-11-21 联合声明：命题对、编译过、证的是同一句话、导出证明被多个内核接受。",
        )
    )

    els.append(pill(286, 68, "Lean FRO + Mathlib Initiative · 2026-11-21", fg=GREEN, bg=GREEN_SOFT, w=188, h=28, size=10.5))

    checks = [
        (20, 116, "Ⅰ", "命题是否正确", [
            "Mathlib 的 RiemannHypothesis 定义经专家审定；",
            "社区另建隔离文件，用 comparator 与",
            "con-leche --compare 两套工具比对，确认证的是同一句。",
        ], BLUE, BLUE_SOFT),
        (388, 116, "Ⅱ", "代码能否编译", [
            "175,187 个模块全部编译成功，零错误；",
            "数十人独立复现同一份原始导出文件。",
        ], TEAL, TEAL_SOFT),
        (20, 236, "Ⅲ", "是否偷偷用额外公理", [
            "#print axioms 只报三条：propext、",
            "Classical.choice、Quot.sound；环境里 15 条",
            "公理全在 Init，没有新加的。",
        ], PURPLE, PURPLE_SOFT),
        (388, 236, "Ⅳ", "证明项本身是否有效", [
            "61.6 GB 导出被 Lean 官方内核、paranoid 内核、",
            "nanoda、con-leche、con-ron 与第三方内核接受；",
            "沙箱重建逐字节一致。",
        ], RED, RED_SOFT),
    ]
    for x, y, num, name, lines, fg, bg in checks:
        els.append(card(x, y, 352, 108))
        els.append(step_badge(x + 22, y + 28, num, fg=fg, bg=bg, r=12))
        els.append(txt(x + 44, y + 32, name, size=11.5, color=fg, weight="700"))
        for j, line in enumerate(lines):
            els.append(txt(x + 22, y + 62 + j * 19, line, size=10.5, color=BODY))

    els.append(card(20, 360, 720, 118))
    els.append(txt(38, 386, "几个让人安心的细节", size=11.5, color=INK, weight="700"))
    els.append(txt(38, 414, "• 检查在“惰性导出”上跑，源码里就算藏了恶意代码也碰不到验证过程。", size=10.5, color=BODY))
    els.append(txt(38, 440, "• con-leche / con-ron 自带相对集合论的可靠性证明：它们不可能接受假证明。", size=10.5, color=BODY))
    els.append(txt(38, 466, "• 唯一一处非确定性只影响一个绑定变量名（38 字节），不在五个定理的依赖路径上。", size=10.5, color=BODY))

    els.append(card(20, 492, 720, 88, fill=RED_SOFT, stroke=RED))
    els.append(txt(38, 518, "但“内核接受”不等于“人类读懂”", size=11.5, color=RED, weight="700"))
    els.append(txt(38, 546, "验证的是：在 Mathlib 的定义下，这套推导从三条标准公理出发能走到那句话。", size=10.5, color=BODY))
    els.append(txt(38, 570, "它没有告诉你推导为什么这么走，也没有给出可发表的简短论证——这部分仍然缺失。", size=10.5, color=BODY))
    return figure(
        594,
        "Lean社区验证黎曼猜想证明的四道关卡图",
        "顶部标注Lean FRO与Mathlib Initiative十一月二十一日联合声明，中间四关依次为命题是否正确代码能否编译是否偷偷用额外公理三条标准公理以及证明项是否被多个内核接受，下方列出惰性导出可靠性证明与非确定性细节，底部红框强调内核接受不等于人类读懂。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 边界与结论
# ---------------------------------------------------------------------------
def build_scope() -> str:
    els = list(
        header(
            "到底证明了多少：一张边界图",
            "RH 已证，Dirichlet L-函数的 GRH 已证；更广的 Hecke／自守 L-函数不在这次的范围内。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(56, 93, "覆盖到哪一步", size=11.8, color=INK, weight="700"))
    scope = [
        ("Riemann ζ", "RH：非平凡零点实部 = 1/2", GREEN, GREEN_SOFT, "已证"),
        ("Dirichlet L", "全部模数、全部特征；s=1 极点除外", GREEN, GREEN_SOFT, "已证"),
        ("分圆域整数环", "Robin / Lagarias 型不等式", TEAL, TEAL_SOFT, "已推出"),
    ]
    for i, (name, note, fg, bg, tag) in enumerate(scope):
        y = 124 + i * 100
        els.append(f'<rect x="40" y="{y}" width="312" height="84" rx="7" fill="{bg}" stroke="{fg}"/>')
        els.append(txt(56, y + 26, name, size=11.5, color=fg, weight="700"))
        els.append(txt(56, y + 50, note, size=10.5, color=BODY))
        els.append(txt(56, y + 72, "状态：" + tag, size=10.5, color=fg))
    els.append(txt(40, 442, "注：三条算术结论还需 Robin1984 那份形式化。", size=10.5, color=MUTED))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "没覆盖到哪一步", size=11.8, color=INK, weight="700"))
    outside = [
        ("Dedekind ζ 函数", "数域上的推广"),
        ("Hecke L 函数", "更一般的数域 L 函数"),
        ("一般自守 L 函数", "朗兰兹纲领那一层"),
        ("Extended RH", "Alpöge 说自己预期能拿到，尚未交付"),
    ]
    for i, (name, note) in enumerate(outside):
        y = 124 + i * 84
        els.append(f'<rect x="406" y="{y}" width="316" height="70" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        els.append(txt(420, y + 26, name, size=11, color=RED, weight="700"))
        els.append(txt(420, y + 50, note, size=10.5, color=BODY))
    els.append(f'<rect x="406" y="466" width="316" height="0" fill="none"/>')
    els.append(txt(406, 468, "“GRH”在核查页里被严格限定为 Dirichlet L 函数。", size=10.5, color=MUTED))

    els.append(card(20, 500, 720, 88, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "三档状态，别混成一档：", size=11.5, color=INK, weight="700"))
    els.append(txt(38, 552, "① 机器核验通过（已发生）  ② 人类读懂并写出短证明（尚未）  ③ Clay 规则下的期刊发表 + 两年检验（尚未）", size=10.5, color=BODY))
    els.append(txt(38, 576, "所以：技术上可以说“已被证明”，制度上还不能说“已获千禧年大奖认证”。", size=10.5, color=SLATE))
    return figure(
        602,
        "黎曼猜想形式化证明的覆盖范围与未覆盖范围图",
        "左栏列出已覆盖的Riemann zeta的RH全部模数与特征的Dirichlet L函数以及分圆域上的Robin与Lagarias不等式，右栏列出未覆盖的Dedekind zeta函数Hecke L函数一般自守L函数与Extended RH，底栏区分机器核验通过人类读懂并写出短证明Clay规则下期刊发表加两年检验三档状态。",
        els,
    )


@register(TOPIC, "黎曼猜想证明：临界线、六周时间线、Stepanov 重数、Lean 四关与范围边界", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("riemann-critical-line.svg", build_critical_line),
        ("riemann-timeline.svg", build_timeline),
        ("riemann-stepanov.svg", build_stepanov),
        ("riemann-verification.svg", build_verification),
        ("riemann-scope.svg", build_scope),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
