"""Diagrams for growth rates, Knuth arrows, and the 2-state busy beaver."""

import math
from pathlib import Path
import xml.etree.ElementTree as ET

from generate_bernoulli_visuals import BLUE, INK, MUTED, ORANGE, document, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "busy-beaver"


def panel(x, y, width, height):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16" '
        'fill="#fff" stroke="#c9d6df" stroke-width="2"/>'
    )


WIN_FILL = "#d9eef5"


def ackermann(m, n, memo=None):
    if memo is None:
        memo = {}
    key = (m, n)
    if key in memo:
        return memo[key]
    if m == 0:
        value = n + 1
    elif n == 0:
        value = ackermann(m - 1, 1, memo)
    else:
        value = ackermann(m - 1, ackermann(m, n - 1, memo), memo)
    memo[key] = value
    return value


def up_arrow(a, arrows, b, memo=None):
    """Knuth up-arrow: one arrow is exponentiation; more arrows iterate it."""
    if memo is None:
        memo = {}
    key = (a, arrows, b)
    if key in memo:
        return memo[key]
    if arrows == 1:
        value = a ** b
    elif b == 1:
        value = a
    else:
        value = up_arrow(a, arrows - 1, up_arrow(a, arrows, b - 1, memo), memo)
    memo[key] = value
    return value


RULES = {
    ("A", 0): (1, 1, "B"),
    ("A", 1): (1, -1, "B"),
    ("B", 0): (1, -1, "A"),
    ("B", 1): (1, 1, "H"),
}


def run_beaver():
    tape = {}
    position = 0
    state = "A"
    frames = []
    for step in range(1, 8):
        symbol = tape.get(position, 0)
        write, move, nxt = RULES[(state, symbol)]
        tape[position] = write
        position += move
        state = nxt
        frames.append(
            {
                "step": step,
                "tape": dict(tape),
                "head": position,
                "state": state,
                "ones": sum(1 for value in tape.values() if value == 1),
            }
        )
        if state == "H":
            break
    return frames


def facts():
    assert (3 ** 3) ** 3 == 19683
    assert 3 ** (3 ** 3) == 3 ** 27 == 7625597484987
    assert up_arrow(3, 2, 2) == 27
    assert up_arrow(3, 2, 3) == 7625597484987
    assert up_arrow(2, 2, 3) == 16
    assert up_arrow(2, 2, 4) == 65536
    memo = {}
    table = {(m, n): ackermann(m, n, memo) for m in range(4) for n in range(4)}
    assert table[(1, 3)] == 5
    assert table[(2, 3)] == 9
    assert table[(3, 3)] == 61
    assert ackermann(3, 4, memo) == 125
    for n in range(5):
        assert ackermann(3, n, memo) == 2 ** (n + 3) - 3
    assert 2 ** (13 + 3) - 3 == 65533
    last_poly = max(n for n in range(1, 1200) if n ** 100 >= 2 ** n)
    assert last_poly == 996
    assert all(2 ** n > n ** 100 for n in range(997, 1100))
    frames = run_beaver()
    assert len(frames) == 6
    assert frames[-1]["state"] == "H"
    assert frames[-1]["ones"] == 4
    assert [frame["head"] for frame in frames] == [1, 0, -1, -2, -1, 0]
    assert 21 ** 10 == 16679880978201
    return {"crossover": last_poly + 1, "frames": frames, "ackermann": table}


def growth(crossover):
    rows = []
    for n in range(1, 9):
        rows.append((n, n * n, 2 ** n, math.factorial(n)))
        assert rows[-1][2] == 2 ** n and rows[-1][3] == math.factorial(n)
    elements = [
        text(36, 48, "先看三列算得完的数", 32),
        text(36, 88, "同一行的 n 相同。三列都是按定义算出的精确值。", 24, MUTED),
        panel(24, 112, 672, 520),
        text(70, 158, "n", 24, MUTED),
        text(180, 158, "n²", 24, MUTED),
        text(340, 158, "2^n", 24, MUTED),
        text(520, 158, "n!", 24, MUTED),
    ]
    for index, (n, square, power, factorial) in enumerate(rows):
        y = 206 + index * 48
        elements += [
            text(70, y, str(n), 24),
            text(180, y, f"{square:,}", 24),
            text(340, y, f"{power:,}", 24, BLUE if power > square else INK),
            text(520, y, f"{factorial:,}", 24, BLUE if factorial > power else INK),
        ]
    elements += [
        text(36, 676, "从 n＝4 起，阶乘超过 2^n；2^n 在 n＝5 超过平方。", 24),
        text(36, 716, f"n^100 最后一次不小于 2^n，是在 n＝{crossover - 1}。", 24),
        text(36, 750, f"从 n＝{crossover} 起，2^n 一直更大。", 24, BLUE),
    ]
    return document(
        790,
        "平方、指数与阶乘的精确值",
        "n 从 1 到 8。三列分别是 n 的平方、2 的 n 次方和 n 的阶乘，全部按定义算出。"
        f"n 的 100 次方最后一次不小于 2 的 n 次方是在 n 等于 {crossover - 1}；从 {crossover} 起指数一直更大。",
        elements,
    )


def arrows():
    height = 7625597484987
    assert height == 3 ** 27
    elements = [
        text(36, 46, "幂塔从顶上往下算", 32),
        text(36, 84, "同样三个 3，结合顺序会把结果差出很多个数量级。", 24, MUTED),
        panel(24, 108, 672, 150),
        text(44, 152, "① (3³)³ ＝ 27³ ＝ 19,683", 28),
        text(44, 198, "先算下面，再把结果拿去乘方。", 24, MUTED),
        panel(24, 274, 672, 168),
        text(44, 318, "② 3^(3³) ＝ 3²⁷ ＝ 7,625,597,484,987", 26, BLUE),
        text(44, 366, "高德纳箭头采用这一侧：从最上的指数算起。", 24, MUTED),
        text(44, 408, "3^^3 就是这座塔。^^ 表示两支上箭头。", 22),
        panel(24, 458, 672, 220),
        text(44, 502, "③ 3^^^3 ＝ 3^^(3^^3)", 28),
        text(44, 550, "它是 3 的幂塔，层数等于 7,625,597,484,987。", 24, ORANGE),
        text(44, 596, "大约 7.63 万亿层。图里画不出这些层，层数是算出来的。", 24),
        text(44, 642, "多一支箭头，是把前一种运算再迭代这么多次。", 24, MUTED),
    ]
    return document(
        720,
        "高德纳箭头与三层幂塔",
        "三个 3 从底部结合得到 19683；从顶部结合得到 3 的 27 次方，等于 7625597484987。"
        "3^^3 表示两支箭头，等于后者。3^^^3 表示三支箭头，是一座 3 的幂塔，层数恰为 7625597484987。",
        elements,
    )


def beaver(frames):
    cells = (-2, -1, 0, 1)
    elements = [
        text(36, 46, "两状态的海狸：六步后停下", 32),
        text(36, 84, "纸带开始全是 0。橙框只沿六行各停一次，最后留在停机行。", 22, MUTED),
        (
            "<style>.scan{animation:scan 6s linear 1 forwards}"
            "@keyframes scan{0%{transform:translateY(0)}"
            "16%{transform:translateY(0)}20%{transform:translateY(62px)}"
            "32%{transform:translateY(62px)}36%{transform:translateY(124px)}"
            "48%{transform:translateY(124px)}52%{transform:translateY(186px)}"
            "64%{transform:translateY(186px)}68%{transform:translateY(248px)}"
            "80%{transform:translateY(248px)}84%{transform:translateY(310px)}"
            "100%{transform:translateY(310px)}}"
            "@media(prefers-reduced-motion:reduce){.scan{animation:none;transform:translateY(310px)}}"
            "</style>"
        ),
        text(48, 128, "步", 20, MUTED),
        text(110, 128, "纸带", 20, MUTED),
        text(430, 128, "结束后", 20, MUTED),
    ]
    for index, frame in enumerate(frames):
        y = 146 + index * 62
        elements.append(panel(24, y, 672, 54))
        elements.append(text(48, y + 36, str(frame["step"]), 24, BLUE))
        for offset, cell in enumerate(cells):
            x = 110 + offset * 70
            symbol = frame["tape"].get(cell, 0)
            fill = "#fff7ea" if frame["head"] == cell else (WIN_FILL if symbol else "#fff")
            stroke = ORANGE if frame["head"] == cell else BLUE
            elements.append(
                f'<rect x="{x}" y="{y + 8}" width="58" height="38" rx="8" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            )
            elements.append(text(x + 29, y + 35, str(symbol), 22, INK, "middle"))
        label = "停机" if frame["state"] == "H" else frame["state"]
        elements.append(text(470, y + 36, label, 24, ORANGE if label == "停机" else INK))
    elements.append(
        '<rect class="scan" x="28" y="148" width="664" height="50" rx="12" '
        'fill="none" stroke="#ad4f16" stroke-width="4"/>'
    )
    elements += [
        text(36, 548, "橙格是这一步结束时读写头所在的格子。", 22),
        text(36, 582, "A 读 0：写 1，向右，到 B。A 读 1：写 1，向左，到 B。", 22),
        text(36, 616, "B 读 0：写 1，向左，到 A。B 读 1：写 1，向右，停机。", 22),
        text(36, 650, "停机时有 4 个 1，共六步。文献里的最大值也是这两项。", 22, BLUE),
    ]
    return document(
        700,
        "两状态忙碌海狸的六步",
        "一台两状态、符号为 0 和 1 的图灵机，从全 0 纸带出发。"
        "六步之后停机，纸带上留下四个 1。每行给出该步结束时的纸带和下一个状态。"
        "橙框依次移过六行并停在最后一行；减少动态效果时直接停在最后一行。"
        "这台机器的步数等于已知的两状态最大值，最大值本身的证明不在这张图里。",
        elements,
    )


def halt_argument():
    blocks = [
        ("① 假定有判定器 H", "输入任意机器，回答会停或永不停。"),
        ("② 用 H 做一个对角机器 D", "若 H 说“会停”，D 就死循环；若 H 说“永不停”，D 立刻停。"),
        ("③ 把 D 自己的说明书交给 D", "问的是：D 在读到自己的说明书时会不会停。"),
        ("④ 两种回答都矛盾", "若 D 停下，它本该死循环；若 D 不停，它本该停下。"),
    ]
    elements = [
        text(36, 48, "假定能预先判定停机，就会自相矛盾", 30),
        text(36, 88, "沿编号往下读。四格一直都在，没有需要追着看的动画。", 24, MUTED),
    ]
    for index, (title, body) in enumerate(blocks):
        y = 112 + index * 118
        elements += [
            panel(24, y, 672, 104),
            text(44, y + 42, title, 26, BLUE),
            text(44, y + 80, body, 22),
        ]
    return document(
        600,
        "停机问题的自指矛盾",
        "假定存在一台机器，能判定任何图灵机是否停机。"
        "用它构造对角机器：判定器说会停，它就循环；判定器说不停，它就停机。"
        "把这台对角机器用于它自己的描述，两种结果都与构造矛盾。",
        elements,
    )


def domination():
    blocks = [
        ("① 计算 f 的程序", "状态数是一个常数 c，不随输入的数值变大。"),
        ("② 先把 n 写上空白纸带", "用二进制写下 n，额外状态数只随位数增长，大约是 log₂n。"),
        ("③ 再空转，步数超过 f(n)", "这台合成机器会停。它的步数已经大于 f(n)。"),
    ]
    elements = [
        text(36, 48, "可计算的 f，会被稍多几个状态超过", 30),
        text(36, 88, "c 由 f 的程序决定。写 n 的开销不跟着 f(n) 的大小膨胀。", 22, MUTED),
    ]
    for index, (title, body) in enumerate(blocks):
        y = 120 + index * 130
        elements += [
            panel(24, y, 672, 114),
            text(44, y + 44, title, 26, BLUE),
            text(44, y + 86, body, 22),
        ]
    elements += [
        text(36, 530, "所以 S(k) ＞ F(n)。k 是 c 加上写下 n 的状态，F 取到 n 为止的最大。", 22, ORANGE),
        text(36, 572, "k 最终不超过 n。状态变多时，最长步数只增不减。", 22),
        text(36, 610, "因此对所有足够大的 n，S(n) 都大于 F(n)，也就大于 f(n)。", 22, MUTED),
    ]
    return document(
        660,
        "忙碌海狸为什么最终超过可计算函数",
        "设 f 可由一台 c 个状态的图灵机计算。再花大约 log n 个状态把 n 写到空白纸带上，"
        "然后空转超过 f(n) 步。合成机器会停，因此忙碌海狸在 c 加 O(log n) 个状态处已经大于 f(n)。"
        "把 f 换成不超过 n 的最大值之后，对所有足够大的状态数，忙碌海狸都更大。",
        elements,
    )


def main():
    data = facts()
    OUT.mkdir(parents=True, exist_ok=True)
    pictures = {
        "growth": growth(data["crossover"]),
        "arrows": arrows(),
        "beaver": beaver(data["frames"]),
        "halt": halt_argument(),
        "dominate": domination(),
    }
    for name, content in pictures.items():
        root = ET.fromstring(content)
        assert root.get("width") == "720"
        assert root.get("viewBox") == f'0 0 720 {root.get("height")}'
        (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
        print(name, root.get("height"))
    print("crossover", data["crossover"])
    print("ackermann", data["ackermann"])


if __name__ == "__main__":
    main()
