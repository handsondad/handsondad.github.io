"""Generate the Bernoulli family map and reproducible teaching diagrams."""

import math
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "bernoulli"
INK = "#172b45"
MUTED = "#41576a"
BLUE = "#176786"
ORANGE = "#ad4f16"


def text(x, y, value, size=24, color=INK, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}">{escape(value)}</text>'
    )


def document(height, title, description, elements):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" '
        f'viewBox="0 0 720 {height}" role="img" aria-labelledby="title desc" lang="zh-CN">\n'
        f'<title id="title">{escape(title)}</title>\n'
        f'<desc id="desc">{escape(description)}</desc>\n'
        '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}</style>\n'
        f'<rect width="720" height="{height}" fill="#f3f7fa"/>\n'
        + "\n".join(elements)
        + "\n</svg>\n"
    )


def node(x, y, name, dates, number=None):
    width = 684 - x
    color = BLUE if number else "#8798a6"
    heading = f"{number} {name}" if number else name
    return [
        f'<rect x="{x}" y="{y}" width="{width}" height="82" rx="14" '
        f'fill="{"#fff" if number else "#e8eef2"}" stroke="{color}" stroke-width="2"/>',
        text(x + 18, y + 31, heading, 28, BLUE if number else MUTED),
        text(x + 18, y + 68, dates, 23, MUTED),
    ]


def connector(path):
    return f'<path d="{path}" fill="none" stroke="#738a9c" stroke-width="3"/>'


def family_tree():
    elements = [
        text(36, 48, "八位数学家，三代亲缘", 32),
        text(36, 84, "沿线往下读；向右缩进一级，是下一代。", 24, MUTED),
        connector("M54 202V691M54 311H88M54 421H88M54 691H88"),
        connector("M122 462V531H156"),
        connector("M122 732V1021M122 801H156M122 911H156M122 1021H156"),
        connector("M190 1062V1241M190 1131H224M190 1241H224"),
    ]
    elements += node(36, 120, "尼古拉斯：经营香料生意的父亲", "1623—1708；灰框不计入八位数学家")
    people = [
        (88, 270, "雅各布一世", "1655—1705；约翰的哥哥", "①"),
        (88, 380, "尼古拉斯：两位数学家之间的兄弟", "1662—1716；尼古拉斯一世之父", None),
        (156, 490, "尼古拉斯一世", "1687—1759；丹尼尔的堂兄", "③"),
        (88, 650, "约翰一世", "1667—1748；以下三人为他的儿子", "②"),
        (156, 760, "尼古拉斯二世", "1695—1726；丹尼尔的哥哥", "④"),
        (156, 870, "丹尼尔", "1700—1782；研究流体与风险", "⑤"),
        (156, 980, "约翰二世", "1710—1790；以下两人为他的儿子", "⑥"),
        (224, 1090, "约翰三世", "1744—1807；丹尼尔的侄子", "⑦"),
        (224, 1200, "雅各布二世", "1759—1789；约翰三世的弟弟", "⑧"),
    ]
    assert {p[4] for p in people if p[4]} == set("①②③④⑤⑥⑦⑧")
    for person in people:
        elements += node(*person)
    elements += [
        text(36, 1330, "只列连接这八位所需的关系，并非全部子女名单。", 24, MUTED),
        text(36, 1365, "同名人物用“一世、二世、三世”区分。", 24, MUTED),
    ]
    return document(
        1400,
        "伯努利家族八位数学家的亲缘图",
        "灰框父亲有雅各布、尼古拉斯、约翰三个儿子。中间一支有尼古拉斯一世；"
        "约翰一世的三个数学家儿子是尼古拉斯二世、丹尼尔、约翰二世。"
        "约翰二世的两个儿子是约翰三世与雅各布二世。",
        elements,
    )


def spiral_path(radius, scale, cy):
    points = []
    for i in range(1001):
        theta = 4 * math.pi * i / 1000
        r = scale * radius(theta)
        x, y = 310 + r * math.cos(theta), cy - r * math.sin(theta)
        points.append(f"{'M' if i == 0 else 'L'}{x:.3f},{y:.3f}")
    return " ".join(points)


def spiral_comparison():
    arch = lambda theta: 1 + 2 * theta / math.pi
    logarithmic = lambda theta: 2 ** (theta / (2 * math.pi))
    for turn, expected in enumerate((1, 5, 9)):
        assert math.isclose(arch(turn * 2 * math.pi), expected)
    for turn, expected in enumerate((1, 2, 4)):
        assert math.isclose(logarithmic(turn * 2 * math.pi), expected)
    for theta in (0, 0.3, 1, 4):
        assert math.isclose(logarithmic(theta + 2 * math.pi), 2 * logarithmic(theta))
    elements = [
        text(36, 48, "墓碑上，差的是哪一条螺线？", 32),
        text(36, 86, "沿同一条向右的射线，比较每绕一圈的半径。", 24, MUTED),
    ]
    panels = [
        (125, 365, "① 阿基米德螺线：每圈加相同长度", arch, 20, (1, 5, 9),
         "半径 1 → 5 → 9：每圈都加 4。", "构造：r = 1 + 2θ/π"),
        (635, 875, "② 对数螺线：每圈乘相同倍数", logarithmic, 45, (1, 2, 4),
         "半径 1 → 2 → 4：每圈都乘 2。", "构造：r = 2 的 θ/(2π) 次方"),
    ]
    for top, cy, title, radius, scale, values, conclusion, formula in panels:
        elements += [
            f'<rect x="24" y="{top}" width="672" height="480" rx="18" '
            'fill="#fff" stroke="#c9d6df" stroke-width="2"/>',
            text(44, top + 39, title, 26),
            text(44, top + 72, formula, 22, MUTED),
            f'<path d="{spiral_path(radius, scale, cy)}" fill="none" '
            f'stroke="{BLUE}" stroke-width="3.5"/>',
            f'<path d="M310 {cy}H520" fill="none" stroke="#687f90" '
            'stroke-width="2" stroke-dasharray="6 5"/>',
            f'<circle cx="310" cy="{cy}" r="4" fill="{INK}"/>',
            text(280, cy + 33, "中心", 20, MUTED, "middle"),
        ]
        for value in values:
            x = 310 + value * scale
            elements += [
                f'<circle cx="{x}" cy="{cy}" r="5.5" fill="#ad4f16" '
                'stroke="#fff" stroke-width="2"/>',
                text(x, cy + 33, str(value), 24, "#ad4f16", "middle"),
            ]
        elements += [text(44, top + 443, conclusion, 26)]
    elements += [
        text(36, 1152, "两图分别缩放；半径无单位，只画有限两圈。", 24, MUTED),
        text(36, 1186, "原创数学示意，不是墓碑曲线的描摹。", 24, MUTED),
    ]
    return document(
        1220,
        "阿基米德螺线与对数螺线的两圈比较",
        "上图半径每圈加四，沿向右射线三次交点半径为一、五、九；"
        "下图半径每圈乘二，对应一、二、四。曲线按方程计算，两图分别缩放。",
        elements,
    )


def large_numbers():
    elements = [
        text(36, 48, "次数增多，比例怎样变得可靠？", 32),
        text(36, 86, "独立、公平硬币：统计所有可能结果，不抽样模拟。", 24, MUTED),
    ]
    expected = (0.75390625, 0.05688793364098079, 2.7284641560660184e-10)
    labels = ("75.390625%", "约 5.689%", "约 2.73 × 10⁻¹⁰（概率值）")
    for index, n in enumerate((10, 100, 1000)):
        top = 120 + 300 * index
        probabilities = [math.comb(n, k) / 2**n for k in range(n + 1)]
        tail = [k for k in range(n + 1) if abs(10 * k - 5 * n) >= n]
        probability = sum(math.comb(n, k) for k in tail) / 2**n
        assert math.isclose(sum(probabilities), 1, abs_tol=1e-14)
        assert math.isclose(probability, expected[index], rel_tol=1e-13)
        elements += [
            f'<rect x="24" y="{top}" width="672" height="282" rx="16" '
            'fill="#fff" stroke="#c9d6df"/>',
            text(44, top + 36, f"抛 {n} 次", 28),
            text(44, top + 76, f"至少偏离 10 个百分点：{labels[index]}", 24, ORANGE),
            text(150, top + 121, "计入左端", 21, MUTED, "middle"),
            text(570, top + 121, "计入右端", 21, MUTED, "middle"),
        ]
        peak = max(probabilities)
        for k, p in enumerate(probabilities):
            x = 90 + 540 * k / n
            height = 100 * p / peak
            width = min(26, 540 / n * 0.85)
            elements.append(
                f'<rect x="{x-width/2:.4f}" y="{top+230-height:.4f}" '
                f'width="{width:.4f}" height="{height:.6g}" '
                f'fill="{ORANGE if k in tail else BLUE}"/>'
            )
        for fraction in (0, 0.4, 0.5, 0.6, 1):
            x = 90 + 540 * fraction
            elements.append(text(x, top + 264, f"{fraction:.0%}", 22, MUTED, "middle"))
        for fraction in (0.4, 0.6):
            x = 90 + 540 * fraction
            elements.append(
                f'<path d="M{x} {top+130}V{top+235}" stroke="{ORANGE}" '
                'stroke-width="1.5" stroke-dasharray="4 4"/>'
            )
        elements.append(f'<path d="M75 {top+230}H645" stroke="{MUTED}"/>')
    elements += [
        text(36, 1054, "横轴：正面比例；每根柱：该比例的概率。", 24, MUTED),
        text(36, 1092, "三图纵轴分别缩放；虚线边界及外侧均计入。", 24, MUTED),
    ]
    return document(
        1120, "公平硬币正面比例的精确二项分布",
        "分别计算十、一百、一千次独立公平抛掷的全部二项概率。"
        "正面比例不高于百分之四十或不低于百分之六十的合计概率随次数增加大幅下降。"
        "三图横轴同尺度，柱高分别归一化到各自峰值，不能跨图比较高度。",
        elements,
    )


def orthogonal_trajectories():
    px, py = 1, 1
    tangent = (1, -1)
    assert px * tangent[0] + py * tangent[1] == 0
    assert math.isclose(px**2 + py**2, 2)
    elements = [
        text(36, 48, "正交轨线：每次相交，都成直角", 32),
        text(36, 86, "教学例子：同心圆，与过圆心的直线。", 24, MUTED),
        '<rect x="24" y="115" width="672" height="520" rx="18" fill="#fff" stroke="#c9d6df"/>',
        f'<path d="M120 405H550M330 600V195" stroke="#c5d0d9" stroke-width="2"/>',
        text(564, 413, "x", 24, MUTED),
        text(330, 177, "y", 24, MUTED, "middle"),
        text(310, 438, "O", 23, MUTED, "middle"),
    ]
    for angle in (0, math.pi / 4, math.pi / 2, 3 * math.pi / 4):
        dx, dy = 190 * math.cos(angle), 190 * math.sin(angle)
        elements.append(
            f'<path d="M{330-dx:.4f} {405+dy:.4f}L{330+dx:.4f} {405-dy:.4f}" '
            f'stroke="{ORANGE}" stroke-width="2" stroke-dasharray="7 6"/>'
        )
    for radius in (60, 100, 100 * math.sqrt(2), 180):
        elements.append(
            f'<circle cx="330" cy="405" r="{radius:.4f}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>'
        )
    elements += [
        f'<path d="M390 265L470 345" stroke="{INK}" stroke-width="3"/>',
        f'<path d="M418 317L430 329L442 317" fill="none" stroke="{INK}" stroke-width="2.5"/>',
        f'<circle cx="430" cy="305" r="6" fill="{INK}"/>',
        text(500, 298, "P(1,1)", 25),
        text(500, 336, "切线 ⟂ 半径", 23),
        text(44, 680, "① 先选一条圆：x² + y² = C。", 26),
        text(44, 724, "② 再选过圆心的直线；在交点看切线方向。", 26),
        text(44, 768, "③ P 点：圆的斜率 −1，直线斜率 +1。", 26),
        text(36, 830, "横纵轴同尺度、坐标无量纲；不是历史论文复刻。", 24, MUTED),
    ]
    return document(
        865, "同心圆与过圆心直线的正交轨线示例",
        "蓝色实线为同心圆，棕色虚线为过圆心直线。"
        "点一逗号一处的半径方向与圆切线方向点积为零；直角用折线标记。"
        "此图解释轨线问题，不复刻尼古拉斯二世的双曲线论文。",
        elements,
    )


def fluid_energy():
    density, area1, area2, speed1 = 1000, 2e-4, 1e-4, 1
    flow = area1 * speed1
    speed2 = flow / area2
    pressure1 = 100000
    kinetic1 = density * speed1**2 / 2
    kinetic2 = density * speed2**2 / 2
    pressure2 = pressure1 + kinetic1 - kinetic2
    assert math.isclose(flow * 1000, 0.2)
    assert speed2 == 2 and pressure1 - pressure2 == 1500
    assert pressure1 + kinetic1 == pressure2 + kinetic2 == 100500
    elements = [
        text(36, 48, "水变快了，能量从哪里来？", 32),
        text(36, 86, "水密度 1000 kg/m³；以下数值为教学构造。", 24, MUTED),
        '<rect x="24" y="115" width="672" height="162" rx="16" fill="#fff" stroke="#c9d6df"/>',
        text(44, 156, "① 先核对：每秒进出的水一样多", 28),
        text(44, 201, "2 cm² × 1 m/s = 1 cm² × 2 m/s", 26),
        text(44, 244, "两边流量都是 0.2 L/s。", 26, BLUE),
        text(36, 318, "② 截面变小，水流加快（管形示意）", 28),
        f'<path d="M70 355H290L460 380H650V480H460L290 505H70" '
        f'fill="#e1f0f5" stroke="{BLUE}" stroke-width="4"/>',
        f'<path d="M110 430H260M495 430H615" stroke="{ORANGE}" stroke-width="5"/>',
        f'<path d="M260 430L244 421V439ZM615 430L599 421V439Z" fill="{ORANGE}"/>',
        text(200, 547, "截面①：2 cm²", 26, INK, "middle"),
        text(525, 547, "截面②：1 cm²", 26, INK, "middle"),
        text(200, 589, "速度：1 m/s", 26, BLUE, "middle"),
        text(525, 589, "速度：2 m/s", 26, BLUE, "middle"),
        text(200, 631, "压力：100 kPa", 26, ORANGE, "middle"),
        text(525, 631, "压力：98.5 kPa", 26, ORANGE, "middle"),
        '<rect x="24" y="662" width="672" height="206" rx="16" fill="#fff" stroke="#c9d6df"/>',
        text(44, 704, "③ 核对：压力 + 动能密度", 28),
        text(44, 748, "①侧：100000 + 500 = 100500 Pa", 26),
        text(44, 792, "②侧：98500 + 2000 = 100500 Pa", 26),
        text(44, 836, "动能项多 1500 Pa，压力项少 1500 Pa。", 26, BLUE),
        text(36, 910, "水平、稳态、不可压缩、无损耗；同一流线、无外加功。", 23, MUTED),
    ]
    return document(
        945, "水平水管的流量守恒与伯努利能量核对",
        "截面积二平方厘米、速度每秒一米，与截面积一平方厘米、速度每秒二米的流量相同。"
        "在图注所述理想条件下，压力从一百千帕降到九十八点五千帕，"
        "两侧压力加动能密度均为十万零五百帕。管形不按实际截面比例绘制。",
        elements,
    )


def string_modes():
    length, wave_speed = 1, 100
    frequency1 = wave_speed / (2 * length)
    frequency3 = 3 * frequency1
    assert frequency1 == 50 and frequency3 == 150

    def first(x):
        return math.sin(math.pi * x)

    def third(x):
        return 0.35 * math.sin(3 * math.pi * x)

    for x in (0, 1):
        assert abs(first(x)) < 1e-14 and abs(third(x)) < 1e-14
    for x in (1 / 3, 2 / 3):
        assert abs(third(x)) < 1e-14
    assert math.isclose(third(0.5), -0.35)
    elements = [
        text(36, 48, "一根琴弦，叠加几种简单运动", 32),
        text(36, 86, "同一时刻、同一位置相加；三图采用相同位移比例。", 24, MUTED),
    ]
    panels = [
        (f"① 第一振型：f₁ = {frequency1:g} Hz", "振幅 1 mm；两端不动，中间一个波腹。", first),
        (f"② 第三振型：f₃ = {frequency3:g} Hz", "振幅 0.35 mm；还有两个内部节点。", third),
        ("③ 两者叠加：不是单一的正弦形状", "逐点相加，而不是把两根弦接起来。", lambda x: first(x) + third(x)),
    ]
    for index, (heading, caption, shape) in enumerate(panels):
        top = 120 + 290 * index
        baseline = top + 174
        elements += [
            f'<rect x="24" y="{top}" width="672" height="268" rx="16" fill="#fff" stroke="#c9d6df"/>',
            text(44, top + 38, heading, 27),
            text(44, top + 78, caption, 24, MUTED),
            f'<path d="M90 {baseline}H630" stroke="#8798a6" stroke-dasharray="6 5"/>',
        ]
        points = [
            (90 + 540 * i / 600, baseline - 55 * shape(i / 600))
            for i in range(601)
        ]
        path = " ".join(
            f"{'M' if i == 0 else 'L'}{x:.4f},{y:.4f}"
            for i, (x, y) in enumerate(points)
        )
        elements.append(f'<path d="{path}" fill="none" stroke="{BLUE}" stroke-width="3.5"/>')
        for x in (90, 630):
            elements.append(f'<circle cx="{x}" cy="{baseline}" r="5" fill="{INK}"/>')
        for x, label in ((90, "0 m"), (360, "沿弦位置"), (630, "1 m")):
            elements.append(text(x, baseline + 55, label, 22, MUTED, "middle"))
        if index == 1:
            for x in (270, 450):
                elements += [
                    f'<circle cx="{x}" cy="{baseline}" r="5" fill="{ORANGE}"/>',
                    text(x, baseline + 55, "节点", 22, ORANGE, "middle"),
                ]
    elements += [
        text(36, 1037, "理想均匀张紧弦、两端固定、小振幅；f₃ = 3f₁。", 24, MUTED),
        text(36, 1076, "位移单位为 mm；横纵单位不同，外形非实物比例。", 24, MUTED),
    ]
    return document(
        1110, "第一与第三弦振型在同一时刻的叠加",
        "一米长的理想弦，第一振型振幅一毫米、频率五十赫兹；"
        "第三振型振幅零点三五毫米、频率一百五十赫兹，有两个内部节点。"
        "下图逐点相加，展示复杂形状如何由简单振型组成；不表现时间演变。",
        elements,
    )


def recurring_decimal():
    remainder = 1
    steps = []
    for index in range(6):
        digit, new_remainder = divmod(remainder * 10, 7)
        steps.append((index + 1, remainder, digit, new_remainder))
        remainder = new_remainder
    assert remainder == 1
    assert "".join(str(step[2]) for step in steps) == "142857"
    assert all(1 <= step[3] <= 6 for step in steps)
    assert 142857 * 7 == 999999
    elements = [
        text(36, 48, "循环小数：为什么会回到起点？", 32),
        text(36, 86, "每一步：原余数乘 10，再除以 7。", 24, MUTED),
        text(36, 130, "从 1 ÷ 7 的余数 1 开始往下读。", 26),
        '<rect x="24" y="155" width="672" height="520" rx="16" fill="#fff" stroke="#c9d6df"/>',
    ]
    for x, heading in ((80, "步骤"), (235, "原余数 × 10"), (435, "商的这一位"), (605, "新余数")):
        elements.append(text(x, 191, heading, 23, MUTED, "middle"))
    for index, old, digit, new in steps:
        y = 240 + 78 * (index - 1)
        if index == 6:
            elements.append(f'<rect x="38" y="{y-36}" width="644" height="60" rx="10" fill="#e1f0f5"/>')
        for x, label in ((80, str(index)), (235, f"{old} × 10"), (435, str(digit)), (605, str(new))):
            elements.append(text(x, y, label, 28, BLUE if x == 435 else INK, "middle"))
    elements += [
        text(36, 719, "余数回到 1 → 后面的步骤与数字原样重复。", 26),
        text(36, 765, "得到：0.142857142857…，周期为 6。", 28, BLUE),
        text(36, 816, "教学例子，不声称该小数由约翰三世发现。", 24, MUTED),
    ]
    return document(
        850, "一除以七的六步余数循环",
        "每步从旧余数乘十后除以七，依次得到数字一四二八五七；"
        "新余数依次为三、二、六、四、五、一，回到起点，所以循环重现。",
        elements,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, content in (
        ("bernoulli-family-tree.svg", family_tree()),
        ("spiral-comparison.svg", spiral_comparison()),
        ("large-numbers.svg", large_numbers()),
        ("orthogonal-trajectories.svg", orthogonal_trajectories()),
        ("fluid-energy.svg", fluid_energy()),
        ("string-modes.svg", string_modes()),
        ("recurring-decimal.svg", recurring_decimal()),
    ):
        ET.fromstring(content)
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"Wrote {name}")


if __name__ == "__main__":
    main()
