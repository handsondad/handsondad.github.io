"""Generate original P/NP diagrams and verify their numerical constructions."""

import itertools
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from generate_bernoulli_visuals import BLUE, INK, MUTED, ORANGE, document, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "p-np"


def panel(y, height):
    return (
        f'<rect x="24" y="{y}" width="672" height="{height}" rx="16" '
        'fill="#fff" stroke="#c9d6df" stroke-width="2"/>'
    )


def certificate():
    coins = (3, 5, 6, 9, 12)
    target = 17
    valid, invalid = (1, 4), (0, 2, 3)
    assert sum(coins[i] for i in valid) == target
    assert sum(coins[i] for i in invalid) == 18
    subsets = [[i for i in range(len(coins)) if mask >> i & 1] for mask in range(2 ** len(coins))]
    solutions = [subset for subset in subsets if sum(coins[i] for i in subset) == target]
    assert solutions == [[0, 1, 3], [1, 4]]
    elements = [
        text(36, 48, "找到一个组合，与检查一份清单", 32),
        text(36, 88, "每枚最多用一次；目标：恰好凑出 17。", 25, MUTED),
        panel(120, 172),
    ]
    for i, value in enumerate(coins):
        x = 100 + i * 130
        elements += [
            f'<circle cx="{x}" cy="189" r="36" fill="#e1f0f5" stroke="{BLUE}" stroke-width="2"/>',
            text(x, 201, str(value), 32, BLUE, "middle"),
            text(x, 267, f"第 {i+1} 枚", 24, MUTED, "middle"),
        ]
    elements += [
        panel(320, 218),
        text(44, 364, "① 证书：选第 2、5 枚", 29),
        text(44, 413, "核对：编号合法，没有重复。", 26),
        text(44, 461, "求和：5 + 12 = 17。", 28, BLUE),
        text(44, 509, "结论：存在，回答“是”。", 27, BLUE),
        panel(565, 218),
        text(44, 609, "② 另一份证书：选第 1、3、4 枚", 28),
        text(44, 658, "求和：3 + 6 + 9 = 18，不是 17。", 27, ORANGE),
        text(44, 706, "只能排除这一份组合。", 27),
        text(44, 754, "不能由此推出：所有组合都不行。", 27),
        text(36, 832, "5 枚 → 2⁵ = 32 个候选；检查一份不必枚举全部。", 24, MUTED),
    ]
    return document(
        870, "子集和的证书与验证",
        "五枚硬币面值三、五、六、九、十二，每枚最多使用一次，目标十七。"
        "选择第二和第五枚得到十七，是有效证书；第一、三、四枚得到十八，"
        "只能排除该组合，不能据此认定无解。共三十二个候选子集。",
        elements,
    )


def enumeration():
    rate = 10**9
    seconds_per_year = 365.25 * 24 * 60 * 60
    entries = [
        (30, "约 10.7 亿个", "约 1.07 秒"),
        (60, "约 1.15 × 10¹⁸ 个", "约 36.5 年"),
        (100, "约 1.27 × 10³⁰ 个", "约 4.02 × 10¹³ 年"),
    ]
    assert math.isclose(2**30 / rate, 1.073741824)
    assert 36.5 < 2**60 / rate / seconds_per_year < 36.6
    assert 4.01e13 < 2**100 / rate / seconds_per_year < 4.03e13
    elements = [
        text(36, 48, "每多一个选／不选，候选数就翻倍", 32),
        text(36, 88, "乐观假设：每秒检查 10 亿个候选，忽略其他成本。", 24, MUTED),
    ]
    for index, (n, count, duration) in enumerate(entries):
        top = 120 + index * 205
        elements += [
            panel(top, 180),
            text(44, top + 42, f"{n} 个物品 → 2 的 {n} 次方个候选", 28),
            text(44, top + 91, count, 29, BLUE),
            text(44, top + 143, f"全部检查：{duration}", 29, ORANGE),
        ]
    elements += [
        text(36, 787, "这是完整穷举的算账，不是任意算法的时间下界。", 25),
        text(36, 831, "实际可能提前找到解；聪明算法也可能避开完整枚举。", 24, MUTED),
    ]
    return document(
        870, "子集候选数的指数增长",
        "三十、六十和一百个物品，分别有二的对应次方个候选子集。"
        "假设每秒检查十亿个，完整枚举约需一点零七秒、三十六点五年、"
        "四点零二乘十的十三次方年。这是枚举估算，不是复杂性下界。",
        elements,
    )


def reduction_flow():
    elements = [
        text(36, 48, "A ≤ₚ B：把 A 的输入交给 B", 32),
        text(36, 88, "输入沿箭头流动；描边提示次序，不表示耗时。", 24, MUTED),
        '<style>.stage{animation:focus 2s linear 1 forwards}.s2{animation-delay:2s}'
        '.s3{animation-delay:4s}@keyframes focus{0%,90%{stroke:#ad4f16;stroke-width:6}'
        '100%{stroke:#176786;stroke-width:2}}'
        '@media(prefers-reduced-motion:reduce){.stage{animation:none}}</style>',
    ]
    stages = [
        (120, "① A 的输入 x → 多项式时间翻译", "得到 B 的输入 f(x)，不能偷偷先解出 A。"),
        (355, "② 假设有一台 B 的快速判定器", "把 f(x) 交进去；此处是假设，不是已实现。"),
        (590, "③ 返回同一个“是／否”答案", "A 的原输入为“是” ⇔ B 的新输入为“是”。"),
    ]
    for i, (top, heading, detail) in enumerate(stages):
        elements += [
            f'<rect class="stage s{i+1}" x="24" y="{top}" width="672" height="160" '
            f'rx="16" fill="#fff" stroke="{BLUE}" stroke-width="2"/>',
            text(44, top + 51, heading, 28),
            text(44, top + 108, detail, 24, MUTED),
        ]
        if i < 2:
            elements += [
                f'<path d="M360 {top+174}V{top+218}" stroke="{BLUE}" stroke-width="4"/>',
                f'<path d="M360 {top+225}L349 {top+209}H371Z" fill="{BLUE}"/>',
            ]
    elements += [
        text(36, 807, "如果 B 能快速判定，A 就也能快速判定。", 27, BLUE),
        text(36, 854, "要证明 B 很难：从已知难的 A，归约到 B。", 27),
        text(36, 899, "一次转换、一个新实例：本文只用多对一归约。", 24, MUTED),
    ]
    return document(
        935, "多项式时间多对一归约的方向",
        "从问题A的输入出发，多项式时间转换成B的输入，交给假设存在的快速判定器，"
        "把其是或否答案作为A的答案。转换保留两个方向。三个步骤一直可读，"
        "描边依次提示流程，播放一次后保持完整静态信息；减少动态效果时不播放。",
        elements,
    )


def cycle_cost(order, weights):
    return sum(weights[a][b] for a, b in zip(order, order[1:] + order[:1]))


def tours(n):
    return [(0,) + rest for rest in itertools.permutations(range(1, n))]


def encoded_distances(n, edges):
    return [
        [0 if i == j else 1 if tuple(sorted((i, j))) in edges else 2 for j in range(n)]
        for i in range(n)
    ]


def check_reduction():
    count = 0
    for n in (3, 4, 5):
        pairs = list(itertools.combinations(range(n), 2))
        orders = tours(n)
        for mask in range(2 ** len(pairs)):
            edges = {edge for i, edge in enumerate(pairs) if mask >> i & 1}
            distances = encoded_distances(n, edges)
            original_yes = any(
                all(tuple(sorted((a, b))) in edges for a, b in zip(order, order[1:] + order[:1]))
                for order in orders
            )
            transformed_yes = min(cycle_cost(order, distances) for order in orders) <= n
            assert original_yes == transformed_yes
            assert all(
                distances[a][c] <= distances[a][b] + distances[b][c]
                for a, b, c in itertools.product(range(n), repeat=3)
            )
            count += 1
    assert count == 1096


def graph_vertices(points, edges):
    result = []
    for a, b in edges:
        x1, y1 = points[a]
        x2, y2 = points[b]
        result.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{BLUE}" stroke-width="3"/>')
    for i, (x, y) in enumerate(points):
        result += [
            f'<circle cx="{x}" cy="{y}" r="22" fill="#fff" stroke="{BLUE}" stroke-width="2"/>',
            text(x, y + 9, "ABCD"[i], 26, INK, "middle"),
        ]
    return result


def hamilton_to_tsp():
    check_reduction()
    cases = [
        ({(0, 1), (1, 2), (2, 3), (0, 3)}, "① 原图有环 → 新问题也回答“是”",
         "A → B → C → D → A", "1 + 1 + 1 + 1 = 4，满足预算 4。", 4),
        ({(0, 1), (0, 2), (0, 3)}, "② 原图无环 → 新问题也回答“否”",
         "A → B → C → D → A", "1 + 2 + 2 + 1 = 6，最短也超预算 4。", 6),
    ]
    elements = [
        text(36, 48, "有边设为 1，无边设为 2，预算设为 n", 31),
        text(36, 88, "四点演示；新问题使用完整距离矩阵。", 24, MUTED),
    ]
    for index, (edges, heading, route, conclusion, expected) in enumerate(cases):
        top = 120 + index * 475
        distances = encoded_distances(4, edges)
        assert min(cycle_cost(tour, distances) for tour in tours(4)) == expected
        elements += [
            panel(top, 450),
            text(44, top + 42, heading, 28),
            text(185, top + 88, "原图", 25, MUTED, "middle"),
            text(510, top + 88, "新距离", 25, MUTED, "middle"),
        ]
        points = [(105, top + 143), (245, top + 143), (245, top + 283), (105, top + 283)]
        elements += graph_vertices(points, edges)
        for j, label in enumerate("ABCD"):
            elements += [
                text(450 + 55 * j, top + 133, label, 24, MUTED, "middle"),
                text(400, top + 179 + 43 * j, label, 24, MUTED, "middle"),
            ]
            for k, cost in enumerate(distances[j]):
                elements.append(text(450 + 55 * k, top + 179 + 43 * j, str(cost), 25, INK, "middle"))
        elements += [
            text(44, top + 353, f"最短路线之一：{route}", 25),
            text(44, top + 405, conclusion, 26, BLUE if expected == 4 else ORANGE),
        ]
    elements += [
        text(36, 1112, "一般理由：n 段各至少为 1，预算 n 迫使每段都是 1。", 24),
        text(36, 1158, "图上位置不代表成本；矩阵的 1／2 才是构造的距离。", 24, MUTED),
    ]
    return document(
        1195, "哈密顿回路到旅行商预算的两向归约",
        "上图为四顶点环，有边成本一，无边成本二，预算四，最短路线四，回答是。"
        "下图为四顶点星形图，没有哈密顿回路，转换后最短路线六，回答否。"
        "位置只是示意，不以图上长度冒充构造距离；生成脚本枚举核对所有三至五顶点简单无向图。",
        elements,
    )


def complexity_map():
    elements = [
        text(36, 48, "先读假设，再看 P、NP 与 NPC", 32),
        text(36, 88, "下面的分离图假设 P ≠ NP；这不是已证明结论。", 24, ORANGE),
        '<rect x="36" y="130" width="428" height="430" rx="18" fill="#e1f0f5" stroke="#176786" stroke-width="3"/>',
        '<rect x="304" y="180" width="380" height="430" rx="18" fill="#fff1df" fill-opacity="0.62" stroke="#ad4f16" stroke-width="3" stroke-dasharray="9 6"/>',
        text(74, 180, "NP", 33, BLUE),
        text(505, 225, "NP-Hard", 29, ORANGE),
        '<rect x="76" y="248" width="184" height="136" rx="16" fill="#fff" stroke="#176786" stroke-width="2"/>',
        text(168, 300, "P", 32, BLUE, "middle"),
        text(168, 348, "可快速判定", 24, BLUE, "middle"),
        text(384, 325, "NPC", 31, ORANGE, "middle"),
        text(384, 370, "交集", 26, ORANGE, "middle"),
        text(560, 455, "例如停机问题", 23, ORANGE, "middle"),
        text(560, 499, "不属于 NP", 25, ORANGE, "middle"),
        text(74, 442, "留白不全是 NPC", 23, MUTED),
        text(74, 486, "面积不表示数量", 23, MUTED),
        panel(652, 257),
        text(44, 697, "另一种尚未排除的可能：P = NP", 29),
        text(44, 750, "那时 NP 中的所有问题，都可快速判定。", 26, BLUE),
        text(44, 798, "非平凡的 NP 判定问题，也都会是 NPC。", 25),
        text(44, 845, "但 NP-Hard 仍可包含 NP 外的不可判定问题。", 25),
        text(44, 887, "“非平凡”：既有“是”实例，也有“否”实例。", 23, MUTED),
        text(36, 954, "始终成立：P ⊆ NP；NPC = NP ∩ NP-Hard。", 27),
        text(36, 999, "不是所有问题都属于这四类；图只画相关关系。", 24, MUTED),
    ]
    return document(
        1035, "P与NP关系的假设图及另一种可能",
        "上图明确假设P不等于NP：P严格包含于NP，NP完全问题是NP与NP难的交集，"
        "P与此交集分离，NP难还延伸到NP之外。下方说明若P等于NP，"
        "NP中所有问题可快速判定，非平凡问题也为NP完全，但不可判定问题不会因此变可判定。"
        "面积和距离不表达数量与难度。",
        elements,
    )


def double_tree():
    points = ((0, 0), (3, 0), (3, 4), (0, 4))
    distances = [
        [math.dist(a, b) for b in points]
        for a in points
    ]
    tree = ((0, 1), (0, 3), (2, 3))
    assert sum(distances[a][b] for a, b in tree) == 10
    # Check every three-edge set that connects all four vertices.
    tree_costs = []
    for edges in itertools.combinations(itertools.combinations(range(4), 2), 3):
        reached = {0}
        for _ in range(3):
            reached |= {b for a, b in edges if a in reached} | {a for a, b in edges if b in reached}
        if len(reached) == 4:
            tree_costs.append(sum(distances[a][b] for a, b in edges))
    assert min(tree_costs) == 10
    walk = (0, 1, 0, 3, 2, 3, 0)
    assert sum(distances[a][b] for a, b in zip(walk, walk[1:])) == 20
    route = (0, 1, 3, 2)
    assert cycle_cost(route, distances) == 16
    optimum = min(cycle_cost(tour, distances) for tour in tours(4))
    assert optimum == 14
    assert cycle_cost((0, 1, 2, 3), distances) == optimum
    assert 16 <= 2 * 10 <= 2 * optimum
    elements = [
        text(36, 48, "近似，不是凭感觉说“差不多”", 32),
        text(36, 88, "四点为 3 × 4 矩形；成本取欧氏距离，无单位。", 24, MUTED),
    ]
    headings = [
        ("① 最小生成树：三条边，成本 10", "树边：AB = 3，AD = 4，DC = 3。"),
        ("② 沿树往返：每条边走两次，成本 20", "次序：A → B → A → D → C → D → A"),
        ("③ 跳过重复城市：得到成本 16 的路线", "次序：A → B → D → C → A"),
    ]
    for index, (heading, caption) in enumerate(headings):
        top = 120 + index * 375
        drawn_points = [(270 + x * 40, top + 114 + y * 40) for x, y in points]
        elements += [panel(top, 350), text(44, top + 42, heading, 27)]
        edges = tree if index < 2 else ((0, 1), (1, 3), (3, 2), (2, 0))
        elements += graph_vertices(drawn_points, edges)
        if index == 1:
            elements += [
                text(490, top + 155, "每边 × 2", 27, ORANGE),
                text(490, top + 202, "10 × 2 = 20", 24, ORANGE),
            ]
        else:
            elements += [
                text(490, top + 155, "对角线：5", 26, MUTED),
                text(490, top + 202, "外圈最优：14", 24, MUTED),
            ]
        elements.append(text(44, top + 324, caption, 25, BLUE))
    elements += [
        text(36, 1293, "一般保证：返回成本 ≤ 2 × 树成本 ≤ 2 × 最优成本。", 24),
        text(36, 1338, "关键前提：距离对称、非负，满足三角不等式。", 24, MUTED),
    ]
    return document(
        1375, "度量旅行商的最小生成树二近似示例",
        "三乘四矩形上四个点，欧氏距离。最小生成树成本十，沿树往返二十，"
        "跳过重复点后的路线A、B、D、C、A成本十六，矩形外圈最优十四。"
        "图形保持坐标比例，交叉点不是城市；脚本核对所有生成树与闭合路线。"
        "一般二近似保证依赖非负对称度量与三角不等式。",
        elements,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, make in (
        ("certificate", certificate),
        ("enumeration", enumeration),
        ("reduction-flow", reduction_flow),
        ("hamilton-to-tsp", hamilton_to_tsp),
        ("complexity-map", complexity_map),
        ("double-tree", double_tree),
    ):
        content = make()
        ET.fromstring(content)
        (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
        print(f"Wrote {name}.svg")


if __name__ == "__main__":
    main()
