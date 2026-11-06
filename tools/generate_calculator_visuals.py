"""Original calculator-history diagrams; arithmetic and scale checks use stdlib."""

import math
from decimal import Decimal
from pathlib import Path

from generate_kepler_newton_visuals import BLUE, GOLD, INK, RED, dot, line, panel, path, save, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "calculator-history"
GRAY = "#71869a"


def heading(title, subtitle):
    return text(36, 52, title, 29) + text(36, 91, subtitle, 22)


def write(name, height, title, description, body):
    save(name, height, title, description, body, output_directory=OUT)


def digits(value, y, active=None):
    body = ""
    for i, digit in enumerate(f"{value:04d}"):
        x = 136 + i * 112
        color = RED if i == active else BLUE
        body += (
            f'<rect x="{x}" y="{y}" width="88" height="76" rx="8" '
            f'fill="#f3f7fa" stroke="{color}" stroke-width="2"/>'
        )
        body += text(x + 44, y + 54, digit, 44, color, "middle")
    return body


def carry():
    title = "① 99 + 1：最难的是把那个 1 传过去"
    body = heading(title, "数位状态图；不是帕斯卡机内部零件的精确复刻")
    values = [99, 90, 0, 100]
    notes = [
        ("原来是 0099，准备在个位加 1。", "每个十进制数位只容纳 0—9。"),
        ("个位 9 → 0，向十位发出进位。", "这里的 0 不是结束，而是触发下一步。"),
        ("十位也从 9 → 0，再向百位进 1。", "连着几个 9，就需要连续几次进位。"),
        ("百位收到 1，结果成为 0100。", "完整结果：99 + 1 = 100。"),
    ]
    for step, value in enumerate(values):
        y = 120 + step * 240
        body += panel(y, 220)
        body += text(48, y + 37, f"{step + 1}  " + notes[step][0], 24)
        for i, name in enumerate(["千位", "百位", "十位", "个位"]):
            body += text(180 + 112 * i, y + 76, name, 20, GRAY, "middle")
        body += digits(value, y + 88, [3, 3, 2, 1][step])
        body += text(48, y + 199, notes[step][1], 22)
    body += text(36, 1114, "重点不是四个轮子一起转，而是数位之间可靠地传信。", 22)
    write("carry-chain.svg", 1150, title, "从0099加一，依次处理个位和十位进位，最后得到0100。", body)


def drum():
    title = "② 阶梯鼓：一圈，怎样恰好加 3？"
    body = heading(title, "把圆柱表面展开来看；横向是轴向，纵向是转动次序")
    body += panel(120, 650)
    body += text(48, 163, "九条齿棱长短不同，并非九层圆盘。", 24)
    origin, pitch = 110, 50
    probe = origin + 6.5 * pitch
    for i in range(1, 10):
        y = 195 + i * 46
        end = origin + i * pitch
        color = RED if end >= probe else BLUE
        body += text(76, y + 7, str(i), 22, GRAY, "middle")
        body += (
            f'<rect x="{origin}" y="{y - 11}" width="{i * pitch}" height="22" '
            f'rx="4" fill="{color}"/>'
        )
        if end >= probe:
            body += dot(probe, y, 7, GOLD)
    body += line(probe, 196, probe, 650, GOLD, True)
    body += text(probe, 691, "小齿轮的接触位置", 22, GOLD, "middle")
    body += text(48, 735, "这个位置只有三条齿棱经过 → 接收齿轮走三步。", 22)
    body += panel(795, 255)
    body += text(48, 837, "调节轴向位置，就改变一圈经过的齿数", 24)
    for index, n in enumerate([0, 3, 7]):
        x = 150 + index * 205
        body += text(x, 897, f"设为 {n}", 28, BLUE, "middle")
        body += text(x, 946, f"遇到 {n} 齿", 25, RED, "middle")
    body += text(48, 1019, "转完齿区后，还要处理进位；此处只拆解输入机制。", 21)
    body += text(36, 1095, "示意省略真实齿形、传动比、定位与无齿区的角度。", 22)
    write("stepped-drum.svg", 1130, title, "展开后的九根渐长齿棱中，一条接触线只与最长的三根相交，说明设为3时每圈输入3。", body)


def multiply():
    title = "③ 乘法：重复相加，加上十进位移"
    body = heading(title, "1709 × 365 = 1709 × (5 + 60 + 300)")
    total = 0
    for index, (place, turns) in enumerate([(0, 5), (1, 6), (2, 3)]):
        y = 120 + index * 275
        value = 1709 * 10**place
        part = value * turns
        total += part
        body += panel(y, 250)
        body += text(48, y + 39, f"{index + 1}  滑架位移 {place} 格；转 {turns} 圈", 25)
        body += text(60, y + 95, f"每圈加 {value:,}", 29, BLUE)
        body += text(60, y + 147, f"本步增加 {part:,}", 29, GOLD)
        body += text(60, y + 207, f"累计结果 {total:,}", 32, RED)
    body += text(36, 1004, "5 + 6 + 3 = 14 圈，而不是连续加 365 次。", 25)
    body += text(36, 1045, "滑架每左移一格，输入数对齐更高一位，贡献乘 10。", 22)
    write("carriage-multiplication.svg", 1090, title, "输入1709，分别转5圈、左移后转6圈、再左移转3圈，累计得到623785。", body)


def slide_rule():
    title = "④ 计算尺：把乘法，变成长度的相加"
    body = heading(title, "这是另一条技术路线：对数刻度，读出近似结果")
    body += panel(120, 540)
    start, scale = 90, 490
    offset = scale * math.log10(2)
    for y, base, label in [(265, start, "固定尺"), (425, start + offset, "滑动尺")]:
        body += text(48, y - 79, label, 24)
        body += line(base, y, base + scale * math.log10(5), y, BLUE)
        ticks = range(1, 11) if label == "固定尺" else range(1, 6)
        if label == "固定尺":
            body += line(base, y, base + scale, y, BLUE)
        for value in ticks:
            x = base + scale * math.log10(value)
            body += line(x, y - 12, x, y + 12, BLUE)
            body += text(x, y + 43, value, 23, INK, "middle")
    for n, label in [(2, "上尺 2 对齐下尺 1"), (6, "下尺 3 对应上尺 6")]:
        x = start + scale * math.log10(n)
        body += line(x, 252, x, 438, RED, True)
        body += text(48, 543 if n == 2 else 592, label, 24, RED)
    body += text(36, 711, "log₁₀2 + log₁₀3 = log₁₀6", 30, BLUE)
    body += text(36, 758, "刻度越往右越密；图中不是等距排了 1 到 10。", 23)
    body += text(36, 801, "计算尺主要给有效数字，数量级通常还要由人判断。", 22)
    write("logarithmic-slide-rule.svg", 845, title, "按十进对数位置绘制的双尺，滑动尺的1对准固定尺2后，滑动尺3对准固定尺6。", body)


def binary():
    title = "⑤ 换成电路，进位这件事还在"
    body = heading(title, "教学用二进制加法；不表示所有计算器都用同一编码")
    body += panel(120, 330)
    body += text(48, 166, "同一个十进制 3 + 1，换一种写法", 25)
    for y, value in [(235, "0011"), (299, "+ 0001"), (387, "= 0100")]:
        body += text(360, y, value, 42, RED if y == 387 else BLUE, "middle")
    body += text(48, 426, "右边两位连续进位，十进制结果仍然是 4。", 22)
    body += panel(475, 500)
    body += text(48, 520, "拆开一个“全加器”：处理当前这一位", 25)
    for x, label in [(143, "输入 A"), (360, "输入 B"), (577, "低位进位 C")]:
        body += text(x, 585, label, 24, BLUE, "middle")
        body += line(x, 605, x, 665, BLUE, arrow=True)
    body += '<rect x="85" y="672" width="550" height="104" rx="14" fill="#eaf2f7" stroke="#176786" stroke-width="2"/>'
    body += text(360, 735, "把三个 0 或 1 相加", 30, BLUE, "middle")
    body += text(360, 835, "A + B + C = S + 2 × C′", 29, RED, "middle")
    body += text(48, 894, "S：留在本位的和；C′：交给高位的进位。", 23)
    body += text(48, 940, "例：1 + 1 + 1 = 1 + 2 × 1。", 25)
    body += text(36, 1024, "电路用逻辑门实现规则；齿轮和脉冲不是同一种机构。", 22)
    write("binary-carry.svg", 1065, title, "二进制0011加0001得到0100；全加器把两个输入位和低位进位转换成本位和及高位进位。", body)


def graphing():
    title = "⑥ 从“一个答案”，到“一整条曲线”"
    body = heading(title, "教学示意：反复计算 y = x²，把数对放到屏幕位置")
    body += panel(120, 690)
    body += text(48, 165, "取九个示例输入，不只问一次“2 的平方是多少”", 23)
    for y in range(5):
        screen_y = 650 - 100 * y
        body += line(160, screen_y, 560, screen_y, "#dce5ec", True)
        if y:
            body += text(339, screen_y + 7, y, 20, GRAY, "end")
    body += line(130, 650, 605, 650, BLUE, arrow=True)
    body += line(360, 675, 360, 215, BLUE, arrow=True)
    for x in range(-2, 3):
        body += text(360 + 100 * x, 690, x, 22, INK, "middle")
    body += text(619, 657, "x", 24, BLUE)
    body += text(373, 220, "y", 24, BLUE)
    points = [(360 + 100 * x, 650 - 100 * x * x) for x in [i / 4 for i in range(-8, 9)]]
    body += path(points, BLUE, 3)
    for i in range(-4, 5):
        x = i / 2
        body += dot(360 + 100 * x, 650 - 100 * x * x, 7, RED)
    body += text(48, 751, "红点：九个精确数对；蓝线：更密采样后的折线。", 22)
    body += text(36, 861, "有限像素只能近似显示连续曲线；窗口选择也会影响观察。", 22)
    body += text(36, 902, "这是原理图，不是 fx-7000G 的屏幕复刻或算法测绘。", 22)
    write("graphing-points.svg", 945, title, "九个精确平方函数样本点与十七点采样折线，展示绘图计算器将数值变成图形的基本思路。", body)


def timeline():
    title = "⑦ 不是一位天才，按下了所有时代的等号"
    body = heading(title, "精选路标，纵向间距不代表真实时间间隔")
    rows = [
        ("1623", "席卡德的通信记录", "齿轮加减，配合纳皮尔算筹处理乘除。"),
        ("1640 年代", "帕斯卡计算器", "把加法与自动进位做成实际机器。"),
        ("1673 起", "莱布尼茨持续展示、改进计算机", "后来以阶梯鼓、滑架实现四则运算。"),
        ("1820 起", "托马斯算术计；随后改进、量产", "原理之外，可靠性、制造与市场同样重要。"),
        ("二战后", "Curta：口袋里的纯机械计算器", "阶梯鼓的后代，不用电池也能做四则运算。"),
        ("1961", "ANITA 电子桌面计算器发布", "电子管时代的计算器，不是单芯片小机器。"),
        ("1971", "Intel 4004 首次公开广告", "为计算器开发芯片，推动微处理器发展。"),
        ("1972", "HP-35 掌上科学计算器", "三角、对数等函数进入衣兜。"),
        ("1983", "SL-800：薄至 0.8 毫米", "电子计算器不只变小，还向卡片的厚度靠近。"),
        ("1985", "fx-7000G 绘图计算器", "答案不只是一串数，还能是一幅函数图。"),
        ("今天", "计算器也成为一种软件功能", "科学、绘图、编程与专用计算器仍然并存。"),
    ]
    for index, (date, label, detail) in enumerate(rows):
        y = 130 + index * 150
        body += panel(y, 132)
        body += text(48, y + 34, date, 24, RED)
        body += text(48, y + 75, label, 25, BLUE)
        body += text(48, y + 112, detail, 21)
    write("calculator-timeline.svg", 1800, title, "计算器发展精选时间线，区分通信记录、发明改进、量产、发布与软件时代。", body)


def precision():
    title = "⑧ 按下等号前，还要知道“数”怎样保存"
    body = heading(title, "这些是表示方式的例子，不是所有产品的统一实现")
    rows = [
        ("有限位十进制整数", "例如：四个数轮只能显示 0000—9999。", "9999 再加 1，需要额外一位或溢出处理。"),
        ("有限精度二进制浮点数", "0.1 的二进制小数无限循环，存储时需舍入。", "常见示例：0.1 + 0.2 → 0.30000000000000004"),
        ("十进制、整数或有理数算法", "0.1 可按十进小数处理，也可记成分数 1/10。", "能精确处理哪些运算，仍取决于算法和资源。"),
    ]
    for index, (label, detail, example) in enumerate(rows):
        y = 120 + index * 220
        body += panel(y, 200)
        body += text(48, y + 40, label, 25, BLUE)
        body += text(48, y + 95, detail, 22)
        body += text(48, y + 151, example, 21, RED)
    body += text(36, 832, "显示“0.3”，不一定能反推出内部恰好存了什么。", 23)
    body += text(36, 878, "无限循环小数、无理数与有限屏幕，是不同层面的限制。", 22)
    write("number-representation.svg", 920, title, "比较有限位机械整数、二进制浮点、十进制或有理数算法，说明显示结果与内部表示并非一回事。", body)


def validate():
    assert 99 + 1 == 100
    states, carry_in = [], 1
    for n in [9, 9, 0, 0]:
        carry_in, digit = divmod(n + carry_in, 10)
        states.append(digit)
    assert states == [0, 0, 1, 0]
    for digit in range(10):
        probe = 9.5 - digit
        assert sum(length >= probe for length in range(1, 10)) == digit
    partials = [1709 * turns * 10**place for place, turns in enumerate([5, 6, 3])]
    assert partials == [8545, 102540, 512700]
    assert sum(partials) == 1709 * 365 == 623785
    assert sum([5, 6, 3]) == 14
    assert math.isclose(math.log10(2) + math.log10(3), math.log10(6))
    for a in range(2):
        for b in range(2):
            for c in range(2):
                carry_out, result = divmod(a + b + c, 2)
                assert a + b + c == result + 2 * carry_out
    assert f"{3:04b}" == "0011" and f"{4:04b}" == "0100"
    assert repr(0.1 + 0.2) == "0.30000000000000004"
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
    samples = [(i / 2, (i / 2) ** 2) for i in range(-4, 5)]
    assert len(samples) == 9 and samples[0] == (-2, 4) and samples[-1] == (2, 4)
    assert samples[4] == (0, 0)
    assert len({x for x, _ in samples}) == 9


if __name__ == "__main__":
    validate()
    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [carry, drum, multiply, slide_rule, binary, graphing, timeline, precision]:
        draw()
    print("Generated eight SVGs; decimal/binary carries, tooth counts, products, log scales, graph samples and numeric representations verified.")
