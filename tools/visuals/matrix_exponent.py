"""矩阵乘法指数 ω=9/4：57 年长跑、Strassen、张量三角形、几何尺子与反证法的原创 SVG 图解。"""

from __future__ import annotations

import math

from .core import (
    BODY,
    BORDER,
    BLUE,
    BLUE_SOFT,
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

TOPIC = "matrix-exponent"

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
    # 论文日期与定理数字（OpenAI preprint, 2026-11-24, Theorem 1.1）
    assert 9 / 4 == 2.25 and 2 < 2.25 < 3
    # Strassen 递归指数
    assert abs(math.log2(7) - 2.807354922) < 1e-8
    # 论文给出的两个有限规模数字：n=1000 与 n=10^6
    r1 = 1000**3 / 1000**2.25
    r2 = (10**6) ** 3 / (10**6) ** 2.25
    assert 177 < r1 < 179 and 31600 < r2 < 31700
    # 三脚架：单位臂、尖端距离 2、周长 6，标签率 8/3
    assert abs(6 / (8 / 3) - 9 / 4) < 1e-9
    # 欧氏平面里三条单位臂的尖端距离
    assert abs(math.sqrt(3) - 1.7320508) < 1e-6
    # 历史指数顺序严格递减
    seq = [3.0, math.log2(7), 2.376, 2.371055, 2.25, 2.0]
    assert all(a > b for a, b in zip(seq, seq[1:]))
    # 每侧 2w 个词、每个词 2w 位：指数 w*2^(2w)
    assert 8 * 32 == 256  # w=4 时的输入位数


# ---------------------------------------------------------------------------
# 1. 指数长跑：从 n³ 到 n^2.25
# ---------------------------------------------------------------------------
def build_timeline() -> str:
    els = list(
        header(
            "矩阵乘法指数 ω：57 年，把 3 挪到了 2.25",
            "ω = inf{s : 两个 n×n 矩阵可在 O(n^s) 次标量运算内相乘}；输出本身有 n² 项，ω ≥ 2 曾被视为铁律。",
        )
    )

    els.append(card(20, 66, 292, 486))
    els.append(step_badge(38, 89, 1, fg=RED, bg=RED_SOFT))
    els.append(txt(56, 93, "结论先放这里", size=11.8, color=INK, weight="700"))
    els.append(txt(166, 164, "ω = 9/4", size=21, color=RED, anchor="middle", weight="700"))
    els.append(txt(166, 196, "= 2.25，恰好卡在 2 和 3 之间", size=10.5, color=BODY, anchor="middle"))
    els.append(_line(40, 216, 292, 216, stroke=BORDER, sw=1))
    els.append(txt(40, 244, "它度量什么", size=11.2, color=RED, weight="700"))
    els.append(txt(40, 270, "n×n 矩阵相乘所需运算", size=10.5, color=BODY))
    els.append(txt(40, 292, "随 n 增长的幂次。", size=10.5, color=BODY))
    els.append(txt(40, 320, "它不是某台机器跑多久，", size=10.5, color=BODY))
    els.append(txt(40, 342, "而是 n → ∞ 时的指数。", size=10.5, color=BODY))
    els.append(txt(40, 374, "定理覆盖任意域 F，", size=10.5, color=BODY))
    els.append(txt(40, 396, "包括有限域。", size=10.5, color=BODY))
    els.append(_line(40, 414, 292, 414, stroke=BORDER, sw=1))
    els.append(txt(40, 440, "规模账（仅算运算次数）", size=11.2, color=RED, weight="700"))
    els.append(txt(40, 466, "n = 1000：10⁹ → 约 5.6×10⁶", size=10.5, color=BODY))
    els.append(txt(40, 488, "省约 178 倍。", size=10.5, color=MUTED))
    els.append(txt(40, 516, "n = 10⁶：10¹⁸ → 约 3.2×10¹³", size=10.5, color=BODY))
    els.append(txt(40, 538, "这是渐近量，不是实测加速。", size=10.5, color=MUTED))

    els.append(card(328, 66, 412, 486))
    els.append(step_badge(346, 89, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(364, 93, " milestones：指数是怎么一步步掉下来的", size=11.8, color=INK, weight="700"))
    rows = [
        ("1969", "3 → 2.8074", "Strassen 七乘积恒等式", BLUE),
        ("1990", "2.376", "Coppersmith–Winograd", GREEN),
        ("2026.09", "< 2.371055", "交错抽取，任意域", ORANGE),
        ("2026.10", "≤ 2.25", "OpenAI 多项式乘法上界", PURPLE),
        ("2026.11", "= 2.25", "匹配下界，指数被钉死", RED),
        ("旧猜想", "2", "ω = 2 的猜想被否定", MUTED),
    ]
    for i, (year, value, note, color) in enumerate(rows):
        y = 126 + i * 68
        fill = RED_SOFT if i == 4 else (SLATE_SOFT if i % 2 == 0 else "#ffffff")
        els.append(f'<rect x="344" y="{y}" width="380" height="60" rx="7" fill="{fill}" stroke="{BORDER}"/>')
        els.append(txt(358, y + 25, year, size=10.5, color=color, weight="700"))
        els.append(txt(358, y + 47, "时间 / 来源", size=10.5, color=MUTED))
        els.append(txt(436, y + 25, value, size=12, color=color, weight="700"))
        els.append(txt(436, y + 47, "可达指数", size=10.5, color=MUTED))
        els.append(txt(526, y + 25, note, size=10.5, color=BODY))
        els.append(txt(526, y + 47, "论文原文与附录引用", size=10.5, color=MUTED))

    els.append(card(20, 566, 720, 34, fill=SLATE_SOFT, stroke=BORDER))
    els.append(
        txt(
            36,
            588,
            "读法：上界说“存在这么快的算法”，下界说“不可能更快”；只有两头合拢，才算真正确定一个指数。",
            size=10.5,
            color=SLATE,
        )
    )
    return figure(
        610,
        "矩阵乘法指数七十五年演进与九四分之一定理图",
        "左栏定义矩阵乘法指数omega为可在O括号n的s次方内相乘的s的下确界并给出n等于一千与一百万时三次方与二点二五次方运算量对比，右栏按年份列出1969年Strassen二点八零七四、1990年CoppersmithWinograd二点三七六、2026年九月交错抽取二点三七一零五五、十月上界二点二五、十一月匹配下界二点二五以及被否定的omega等于二猜想，底栏说明上下界合拢才叫确定。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. Strassen：8 次乘法变 7 次
# ---------------------------------------------------------------------------
def build_strassen() -> str:
    els = list(
        header(
            "Strassen 1969：2×2 分块，8 次乘法 → 7 次",
            "省下的那一次乘法递归下去，就省掉一个 n 的幂：T(n)=7T(n/2) ⇒ n^(log₂7) ≈ n^2.8074。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "朴素分块：8 次块乘法", size=11.8, color=INK, weight="700"))
    boxes = [
        (40, 122, "A₁₁", BLUE_SOFT, BLUE),
        (106, 122, "A₁₂", BLUE_SOFT, BLUE),
        (40, 166, "A₂₁", BLUE_SOFT, BLUE),
        (106, 166, "A₂₂", BLUE_SOFT, BLUE),
        (224, 122, "B₁₁", GREEN_SOFT, GREEN),
        (290, 122, "B₁₂", GREEN_SOFT, GREEN),
        (224, 166, "B₂₁", GREEN_SOFT, GREEN),
        (290, 166, "B₂₂", GREEN_SOFT, GREEN),
    ]
    for x, y, label, bg, fg in boxes:
        els.append(f'<rect x="{x}" y="{y}" width="60" height="36" rx="6" fill="{bg}" stroke="{fg}"/>')
        els.append(txt(x + 30, y + 24, label, size=10.5, color=fg, anchor="middle", weight="700"))
    els.append(txt(192, 158, "×", size=15, color=MUTED, anchor="middle"))
    els.append(txt(40, 246, "C₁₁ = A₁₁B₁₁ + A₁₂B₂₁", size=10.5, color=BODY))
    els.append(txt(40, 272, "C₁₂ = A₁₁B₁₂ + A₁₂B₂₂", size=10.5, color=BODY))
    els.append(txt(40, 298, "C₂₁ = A₂₁B₁₁ + A₂₂B₂₁", size=10.5, color=BODY))
    els.append(txt(40, 324, "C₂₂ = A₂₁B₁₂ + A₂₂B₂₂", size=10.5, color=BODY))
    els.append(_line(40, 344, 352, 344, stroke=BORDER, sw=1))
    els.append(txt(40, 372, "8 次块乘法 + 4 次块加法", size=11.2, color=BLUE, weight="700"))
    els.append(txt(40, 402, "T(n) = 8T(n/2) + O(n²)", size=10.5, color=BODY))
    els.append(txt(40, 432, "⇒ T(n) = O(n³)", size=12, color=BLUE, weight="700"))
    els.append(txt(40, 462, "指数 3，和逐个点积一样。", size=10.5, color=MUTED))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "Strassen：7 次块乘法", size=11.8, color=INK, weight="700"))
    products = ["M₁  (A₁₁+A₂₂)(B₁₁+B₂₂)", "M₂  (A₂₁+A₂₂)B₁₁", "M₃  A₁₁(B₁₂−B₂₂)", "M₄  A₂₂(B₂₁−B₁₁)",
                "M₅  (A₁₁+A₁₂)B₂₂", "M₆  (A₂₁−A₁₁)(B₁₁+B₁₂)", "M₇  (A₁₂−A₂₂)(B₂₁+B₂₂)"]
    for i, p in enumerate(products):
        col, row = i % 2, i // 2
        x = 406 + col * 166
        y = 124 + row * 52
        els.append(f'<rect x="{x}" y="{y}" width="158" height="44" rx="6" fill="{RED_SOFT if i == 6 else SLATE_SOFT}" stroke="{BORDER}"/>')
        els.append(txt(x + 10, y + 27, p, size=10.5, color=RED if i == 6 else BODY))
    els.append(_line(406, 342, 724, 342, stroke=BORDER, sw=1))
    els.append(txt(406, 370, "18 次块加减换 1 次块乘法", size=10.5, color=BODY))
    els.append(txt(406, 398, "T(n) = 7T(n/2) + O(n²)", size=10.5, color=BODY))
    els.append(txt(406, 430, "⇒ T(n) = O(n^2.8074)", size=12, color=RED, weight="700"))
    els.append(txt(406, 460, "57 年的“挤牙膏”，从这里起步。", size=10.5, color=MUTED))

    els.append(card(20, 500, 720, 92, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "递归树：为什么只少一次乘法，指数就变了", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "第 0 层：1 个 n 阶问题   →   第 1 层：7 个 n/2   →   第 2 层：49 个 n/4   →   …   →   第 k 层：7ᵏ 个 n/2ᵏ", size=10.5, color=BODY))
    els.append(txt(38, 580, "k = log₂n 时叶子数 = 7^(log₂n) = n^(log₂7) ≈ n^2.8074；朴素算法同样位置是 8^k = n³。", size=10.5, color=SLATE))
    return figure(
        606,
        "Strassen七乘积恒等式与递归指数计算图",
        "左栏展示二乘二分块矩阵的朴素算法四个输出块共八次块乘法并得到Tn等于八T括号n除以二括号即n三次方，右栏列出Strassen的七个乘积式说明用十八次块加减换一次块乘法得到指数log二下七约二点八零七四，底栏用递归树说明第七层叶子数等于n的log二七次方。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 张量三角形：三条线与一个共享标签
# ---------------------------------------------------------------------------
def build_tensor_triangle() -> str:
    els = list(
        header(
            "张量图里的三角形：三个下标，三条边",
            "T_n = Σ e_ij ⊗ e_jk ⊗ e_ki；i、j、k 各出现两次，于是 A、B、C 三点被三条线连成三角形。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "三条线：每个下标共享一次", size=11.8, color=INK, weight="700"))
    ax, ay, bx, by, cx, cy = 196, 154, 72, 322, 320, 322
    els.append(_line(ax, ay, bx, by, stroke=BLUE, sw=2.2))
    els.append(_line(bx, by, cx, cy, stroke=GREEN, sw=2.2))
    els.append(_line(cx, cy, ax, ay, stroke=PURPLE, sw=2.2))
    els.append(_dot(ax, ay, 22, BLUE_SOFT, BLUE, 1.6))
    els.append(_dot(bx, by, 22, GREEN_SOFT, GREEN, 1.6))
    els.append(_dot(cx, cy, 22, PURPLE_SOFT, PURPLE, 1.6))
    els.append(txt(ax, ay + 5, "A", size=11.5, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(bx, by + 5, "B", size=11.5, color=GREEN, anchor="middle", weight="700"))
    els.append(txt(cx, cy + 5, "C", size=11.5, color=PURPLE, anchor="middle", weight="700"))
    els.append(txt(128, 220, "j", size=12.5, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(196, 344, "k", size=12.5, color=GREEN, anchor="middle", weight="700"))
    els.append(txt(264, 220, "i", size=12.5, color=PURPLE, anchor="middle", weight="700"))
    els.append(txt(40, 378, "A 看 (i,j)，B 看 (j,k)，C 看 (k,i)。", size=10.5, color=BODY))
    els.append(txt(40, 404, "下标 j 在 A、B 之间共享，k 在 B、C 之间，i 在 C、A 之间。", size=10.5, color=BODY))
    els.append(txt(40, 432, "三条线长度之和 × log₂n = 这个张量的价格。", size=10.5, color=SLATE))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "一个标签：r 种取值同时喂给三点", size=11.8, color=INK, weight="700"))
    lx, ly = 564, 160
    targets = [(452, 300, "A", BLUE, BLUE_SOFT), (564, 320, "B", GREEN, GREEN_SOFT), (676, 300, "C", PURPLE, PURPLE_SOFT)]
    for tx, ty, label, color, bg in targets:
        els.append(_arrow(lx, ly + 24, tx, ty - 24, marker="arr-muted", sw=1.5))
        els.append(_dot(tx, ty, 21, bg, color, 1.6))
        els.append(txt(tx, ty + 5, label, size=11.5, color=color, anchor="middle", weight="700"))
    els.append(_dot(lx, ly, 26, RED_SOFT, RED, 1.8))
    els.append(txt(lx, ly + 5, "ℓ", size=13, color=RED, anchor="middle", weight="700"))
    els.append(txt(406, 356, "秩 r 分解：三点各自做线性映射，", size=10.5, color=BODY))
    els.append(txt(406, 380, "只看同一个标签 ℓ ∈ [r]。", size=10.5, color=BODY))
    els.append(f'<rect x="406" y="398" width="316" height="62" rx="7" fill="{RED_SOFT}" stroke="{RED}"/>')
    els.append(txt(418, 423, "周长 × log₂n  ≤  D × log₂r", size=11.5, color=RED, anchor="middle", weight="700"))
    els.append(txt(418, 448, "⇒ 指数 ≥ 三角形周长 ÷ 标签率 D", size=10.5, color=BODY, anchor="middle"))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "这就是“尺子”：把张量下标摆进一个有距离概念的空间，指数就变成几何比值。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "欧几里得平面给出的比值只有 2 —— 正好是老下界；要得到 9/4，必须换一套几何。", size=10.5, color=SLATE))
    return figure(
        586,
        "矩阵乘法张量三角形与共享标签价格不等式图",
        "左栏画三个站点A B C组成三角形三条边分别标下标j k i说明A看ijB看jkC看ki每条线代表一次共享，右栏画中心标签ell同时连到三点说明秩r分解的共享标签率D并给出周长乘log二n小于等于D乘log二r的不等式，底栏说明欧氏几何只能给比值二要得到九四分之四必须换几何。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 几何尺子：三脚架的比值恰好 9/4
# ---------------------------------------------------------------------------
def build_geometry() -> str:
    els = list(
        header(
            "9/4 的几何来源：三脚架的两倍距离与 8/3 的标签率",
            "伴随论文：两点共享一个比特，价格是欧氏距离；三点共享，价格是凸包平均宽度——三角形就是半周长。",
        )
    )

    els.append(card(20, 66, 352, 420))
    els.append(step_badge(38, 89, 1, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(56, 93, "关键形状：三条单位臂的三脚架", size=11.8, color=INK, weight="700"))
    ox, oy = 196, 226
    tips = [(196, 126, "P₁"), (104, 292, "P₂"), (288, 292, "P₃")]
    for tx, ty, _ in tips:
        els.append(_line(ox, oy, tx, ty, stroke=TEAL, sw=2.4))
    els.append(_dot(ox, oy, 17, TEAL_SOFT, TEAL, 1.6))
    els.append(txt(ox, oy + 5, "O", size=11.5, color=TEAL, anchor="middle", weight="700"))
    for tx, ty, label in tips:
        els.append(_dot(tx, ty, 19, GOLD_SOFT, GOLD, 1.6))
        els.append(txt(tx, ty + 5, label, size=10.5, color=GOLD, anchor="middle", weight="700"))
    els.append(txt(228, 178, "1", size=11.5, color=TEAL, weight="700"))
    els.append(txt(134, 268, "1", size=11.5, color=TEAL, weight="700"))
    els.append(txt(258, 268, "1", size=11.5, color=TEAL, weight="700"))
    for tx, ty, _ in tips:
        els.append(_line(ox, oy, tx, ty, stroke=GOLD, sw=1.2, dash="5 4"))
    els.append(txt(40, 342, "树状度量：两尖之间必须走", size=10.5, color=BODY))
    els.append(txt(40, 366, "1 + 1 = 2，不是欧氏直线距离。", size=10.5, color=BODY))
    els.append(f'<rect x="40" y="386" width="312" height="70" rx="7" fill="{TEAL_SOFT}" stroke="{TEAL}"/>')
    els.append(txt(56, 412, "三条尖端距离：2 + 2 + 2 = 6", size=11.5, color=TEAL, weight="700"))
    els.append(txt(56, 440, "周长 6 就是三点共享比特的价格。", size=10.5, color=BODY))

    els.append(card(388, 66, 352, 420))
    els.append(step_badge(406, 89, 2, fg=RED, bg=RED_SOFT))
    els.append(txt(424, 93, "比值算出来：6 ÷ (8/3) = 9/4", size=11.8, color=INK, weight="700"))
    els.append(f'<rect x="406" y="124" width="316" height="52" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
    els.append(txt(418, 157, "分子：三角形半周长 = 6", size=10.5, color=BODY))
    els.append(f'<rect x="406" y="188" width="316" height="52" rx="7" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
    els.append(txt(418, 221, "分母：共享标签率 = 8/3", size=10.5, color=BODY))
    els.append(txt(564, 310, "6 ÷ 8/3 = 9/4", size=21, color=RED, anchor="middle", weight="700"))
    els.append(txt(406, 348, "若 ω < 9/4，这种三脚架在价格空间", size=10.5, color=BODY))
    els.append(txt(406, 372, "里不能出现；排除它，就能给一整族", size=10.5, color=BODY))
    els.append(txt(406, 396, "张量统一定价，进而压缩网络。", size=10.5, color=BODY))
    els.append(txt(406, 434, "这是全文最反直觉的一步：几何上", size=10.5, color=MUTED))
    els.append(txt(406, 458, "的“不可能”变成了算法上的“不可能”。", size=10.5, color=MUTED))

    els.append(card(20, 500, 720, 72, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(38, 526, "别把它画成欧氏三角形：三条单位臂在平面里的尖端距离只有 √3 ≈ 1.732，比值只到 2。", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 554, "9/4 来自树状／非正曲率的度量；这正是论文必须引入新几何的原因。", size=10.5, color=SLATE))
    return figure(
        586,
        "三脚架几何与九四分之四比值推导图",
        "左栏画中心O到三个尖端P1P2P3的三条单位臂并说明这是树状度量两尖距离为1加1等于2周长为6，右栏用分子分母两条说明三角形半周长6除以共享标签率三分之八等于四分之九并说明若指数小于九四分之四这种三脚架不能出现，底栏提醒欧氏平面里单位臂尖端距离只有根号三比值只到二。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 反证法四步：压缩撞上去重下界
# ---------------------------------------------------------------------------
def build_contradiction() -> str:
    els = list(
        header(
            "反证法四步：假设 ω < 9/4，去重网络会被压得太便宜",
            "同一批张量网络，一边被压到 O(w^η)，另一边必须有 Ω(w^σ)；取 η < σ 即矛盾。",
        )
    )

    els.append(pill(300, 68, "假设：存在有限域 k 使 ω_k < 9/4", fg=RED, bg=RED_SOFT, w=160, h=28, size=11.5))

    parts = [
        (20, 116, "Ⅰ", "稳定排序 + 批量查表", "把 2w 个词排好，相邻比较判断是否全不同。", BLUE, BLUE_SOFT),
        (388, 116, "Ⅱ", "关联位集中", "球面张量的关联不等式，让记录沿网点集中。", GREEN, GREEN_SOFT),
        (20, 222, "Ⅲ", "张量幂压缩", "把一次网络复制 d 次，每份分摊更少的顶点。", PURPLE, PURPLE_SOFT),
        (388, 222, "Ⅳ", "与独立列表下界相撞", "网络同时测 t 张独立列表，体积却有硬下界。", ORANGE, ORANGE_SOFT),
    ]
    for x, y, num, name, note, fg, bg in parts:
        els.append(card(x, y, 352, 90))
        els.append(step_badge(x + 22, y + 28, num, fg=fg, bg=bg, r=12))
        els.append(txt(x + 44, y + 32, name, size=11.5, color=fg, weight="700"))
        els.append(txt(x + 22, y + 64, note, size=10.5, color=BODY))

    els.append(card(20, 332, 352, 158))
    els.append(txt(38, 358, "定理 2.1：压缩上界", size=11.5, color=BLUE, weight="700"))
    els.append(txt(38, 388, "xⱼ₊₁ ≤ h⁻ᵞ xⱼ + h^η", size=12, color=BODY))
    els.append(txt(38, 420, "h = ⌈log₂n⌉；每轮顶点数按 h⁻ᵞ 缩小，", size=10.5, color=BODY))
    els.append(txt(38, 444, "每个外部位只收 h^η 的小税。", size=10.5, color=BODY))
    els.append(f'<rect x="38" y="456" width="316" height="26" rx="5" fill="{BLUE_SOFT}"/>')
    els.append(txt(48, 474, "重复固定 J 轮后：x_J = O(w^η)", size=10.5, color=BLUE, weight="700"))

    els.append(card(388, 332, 352, 158))
    els.append(txt(406, 358, "定理 2.2：去重下界", size=11.5, color=RED, weight="700"))
    els.append(txt(406, 388, "vol_k(D_w^⊗t) > t · n_w · w^σ", size=11.5, color=BODY))
    els.append(txt(406, 420, "D_w 判定 2w 个词是否两两不同；", size=10.5, color=BODY))
    els.append(txt(406, 444, "即使 t 张列表可跨网连线，每位仍要 w^σ。", size=10.5, color=BODY))
    els.append(f'<rect x="406" y="456" width="316" height="26" rx="5" fill="{RED_SOFT}"/>')
    els.append(txt(416, 474, "对所有 1 ≤ t ≤ 2w 一致成立", size=10.5, color=RED, weight="700"))

    els.append(card(20, 504, 720, 48, fill=RED_SOFT, stroke=RED))
    els.append(txt(36, 534, "η < σ ⇒ O(w^η) < Ω(w^σ)：同一个网络的体积被同时压低和托高，矛盾。故有限域上 ω_k ≥ 9/4。", size=10.5, color=RED, weight="700"))

    els.append(card(20, 566, 720, 48, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 596, "再由双线性化与有限化推广到任意域 F。边界：Lean 只形式化了无除法电路版本，预印本尚未同行评议。", size=10.5, color=SLATE))
    return figure(
        628,
        "矩阵乘法指数下界反证法四步与矛盾链条图",
        "顶部假设某有限域上指数小于四分之九，中间四步依次为稳定排序批量查表关联位集中张量幂压缩与独立列表下界相撞，下方左卡定理2点1给出每轮按h的负伽马缩小得到xJ等于O括号w的eta次方，右卡定理2点2给出去重网络体积大于t乘nw乘w的sigma次方，底部说明eta小于sigma导致矛盾并由双线性化推广到任意域同时注明Lean只形式化无除法电路且未同行评议。",
        els,
    )


@register(TOPIC, "矩阵乘法指数 ω=9/4：57 年长跑、张量三角形、几何尺子与反证链条", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("matrix-exponent-timeline.svg", build_timeline),
        ("matrix-exponent-strassen.svg", build_strassen),
        ("matrix-exponent-tensor-triangle.svg", build_tensor_triangle),
        ("matrix-exponent-geometry.svg", build_geometry),
        ("matrix-exponent-contradiction.svg", build_contradiction),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
