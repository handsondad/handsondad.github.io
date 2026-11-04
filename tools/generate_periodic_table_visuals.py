"""Original periodic-table teaching diagrams, not reproductions of source pages."""

from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "periodic-table"
INK, BLUE, GREEN, GOLD = "#18364b", "#21699a", "#176d5b", "#a45708"
PALE = {"s": "#e4f2e9", "d": "#e2edf9", "p": "#faeedb", "f": "#eee6f5"}
SYMBOLS = "K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr".split()
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


def text(x, y, value, size=25, color=INK, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}">{escape(str(value))}</text>')


def box(x, y, w, h, fill="#edf3f8", stroke="#adc2d1", radius=10):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')


def line(d, step=None):
    static = f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#arrow)"/>'
    if step is None:
        return static
    return static + (f'<path class="trace" d="{d}" pathLength="1" fill="none" '
                     f'stroke="#cf850e" stroke-width="5" style="animation-delay:{step}s"/>')


def save(name, title, description, body, height):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" viewBox="0 0 720 {height}" '
           'role="img" aria-labelledby="title desc" lang="zh-CN">'
           f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
           '<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" '
           'orient="auto" markerUnits="userSpaceOnUse">'
           f'<path d="M1 1L10 6L1 11" fill="none" stroke="{BLUE}" stroke-width="2"/>'
           '</marker></defs><style>'
           'text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}'
           '.trace{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1s linear 1 both}'
           '@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}'
           '@media(prefers-reduced-motion:reduce){.trace{animation:none}}'
           '</style>'
           f'<rect width="720" height="{height}" rx="16" fill="#fafcfe"/>'
           + text(28, 46, title, 30) + body + '</svg>\n')
    root = ET.fromstring(svg)
    assert root.get("width") == "720" and root.get("height") == str(height)
    assert root.find("{http://www.w3.org/2000/svg}title") is not None
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


def fold():
    b = text(28, 92, "只取第四周期：同样 18 个元素，换一种排法。", 24)
    b += text(28, 146, "① 长表：沿一行读 K → Kr", 27)
    for i, symbol in enumerate(SYMBOLS):
        x = 36 + i * 36
        block = "s" if i < 2 else "d" if i < 12 else "p"
        b += text(x + 17, 187, i + 1, 17, anchor="middle")
        b += box(x, 201, 34, 62, PALE[block], radius=3)
        b += text(x + 17, 240, symbol, 21, anchor="middle")
    b += text(28, 305, "上面的小数字是现代族号，不是原子序数。", 23)
    b += line("M360 325V371", 0)
    b += text(28, 414, "② 短表：一个长周期拆成上下两行", 27)
    slots = ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni"]
    lower = ["Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", None, None, "Kr"]
    for j, label in enumerate(ROMAN):
        x = 50 + j * 62
        width = 62 if j < 7 else 186
        b += box(x, 447, width, 43, "#edf3f8", radius=0)
        b += text(x + width / 2, 478, label, 23, anchor="middle")
    for row, symbols in enumerate([slots, lower]):
        for j, symbol in enumerate(symbols):
            x, y = 50 + j * 62, 492 + row * 77
            b += box(x, y, 62, 75, "#fff", radius=0)
            if symbol:
                z = SYMBOLS.index(symbol) + 19
                block = "s" if z <= 20 else "d" if z <= 30 else "p"
                b += box(x + 3, y + 3, 56, 69, PALE[block], radius=3)
                b += text(x + 31, y + 27, z, 17, anchor="middle")
                b += text(x + 31, y + 59, symbol, 27, anchor="middle")
    b += text(28, 700, "这里的小数字才是原子序数：19 → 36。", 24)
    b += text(28, 745, "VIII 大标题下，Fe、Co、Ni 已经占了三小列。", 24)
    b += text(28, 790, "采用俄方示例卷的分行位置；不是完整周期表。", 23)
    assert slots + [s for s in lower if s] == SYMBOLS
    assert len(set(slots + [s for s in lower if s])) == 18
    save("fold-period-four", "八个大标题，为什么装得下十八个元素？",
         "第四周期的18个元素。上方为现代1至18族长行，下方按俄罗斯2026化学示例卷的短表位置分成两行，铁钴镍置于第VIII大族下，氪在第二行最右。下表角标为原子序数，上方为族号。", b, 830)


def relatives():
    b = text(28, 92, "短表的 I 大族，包含两支不相同的家族。", 24)
    b += box(28, 125, 664, 130)
    b += text(48, 169, "同一旧标题：I", 28)
    b += text(48, 219, "K（钾）　　　　　　　　　Cu（铜）", 28)
    b += line("M210 265V312H165V340", 0)
    b += line("M510 265V312H555V340", 1)
    for x, label, members, configuration, oxide in [
        (28, "现代第 1 族", "Li　Na　K", "[Ar] 4s¹", "K₂O：钾为 +1"),
        (372, "现代第 11 族", "Cu　Ag　Au", "[Ar] 3d¹⁰ 4s¹", "Cu₂O：铜为 +1"),
    ]:
        b += box(x, 350, 320, 270, PALE["s"] if x == 28 else PALE["d"])
        b += text(x + 160, 398, label, 28, anchor="middle")
        b += text(x + 160, 451, members, 27, anchor="middle")
        b += text(x + 160, 502, configuration, 25, anchor="middle")
        b += text(x + 160, 566, oxide, 24, anchor="middle")
    b += text(28, 670, "同有“+1”这条线索，不等于化学性质全都相同。", 24)
    b += text(28, 717, "铜还能形成 CuO（+2）；不能照抄碱金属的性格。", 23)
    b += text(28, 764, "电子式分别取中性钾、铜基态；[Ar]表示氩核芯。", 23)
    b += text(28, 811, "A/B 旧标号有不同传统，本文优先写现代族号。", 23)
    save("one-heading-two-families", "钾和铜：旧表的“同楼”，不是同一家",
         "短表旧第I大族可以同时容纳碱金属和铜族，现代分别列为1族和11族。K2O和Cu2O都体现+1氧化态，但铜还有+2等化学状态。K与Cu中性原子的基态电子排布并不相同。", b, 855)


def oxides():
    examples = [
        ("I", "Na₂O", 2, 1, 1),
        ("II", "MgO", 1, 1, 2),
        ("III", "Al₂O₃", 2, 3, 3),
        ("IV", "SiO₂", 1, 2, 4),
        ("V", "P₂O₅*", 2, 5, 5),
        ("VI", "SO₃", 1, 3, 6),
        ("VII", "Cl₂O₇", 2, 7, 7),
    ]
    b = text(28, 92, "一条历史线索：一些氧化物，能排出化学计量阶梯。", 23)
    for i, (group, formula, metal, oxygen, state) in enumerate(examples):
        y = 127 + i * 77
        b += box(28, y, 664, 68, "#edf3f8")
        b += text(55, y + 44, group, 25)
        b += text(173, y + 44, formula, 28)
        b += text(455, y + 44, f"元素为 +{state}", 25)
        assert metal * state == oxygen * 2
    b += text(28, 720, "氧按 −2 记：2 × (+3) + 3 × (−2) = 0", 25, BLUE)
    b += text(28, 768, "例如 Al₂O₃：氧化数之和配平，不是原子排队图。", 23)
    b += text(28, 815, "* P₂O₅是常用经验式；常见分子形式写作 P₄O₁₀。", 22)
    b += text(28, 859, "只选示例：氧、氟等有例外，不能套成万能口诀。", 23)
    save("oxide-clues", "还看不见原子，也能找到元素的“亲戚”",
         "以钠镁铝硅磷硫氯的若干氧化物展示旧I至VII族所利用的化学计量联系。每行核对元素氧化数与氧的负二价总和为零，磷化合物标明经验式。不是每个族每个元素都适用的最高氧化态规则。", b, 900)


def orbitals():
    b = text(28, 92, "每个方框代表一个轨道，每个轨道至多容纳 2 电子。", 22)
    for i, (label, count) in enumerate([("s", 1), ("p", 3), ("d", 5), ("f", 7)]):
        y = 128 + i * 130
        b += box(28, y, 664, 112, PALE[label])
        b += text(50, y + 43, f"{label} 亚层", 27)
        b += text(660, y + 43, f"{count} × 2 = {count * 2}", 26, anchor="end")
        for j in range(count):
            x = 52 + j * 84
            b += box(x, y + 58, 65, 40, "#fff", radius=3)
            b += text(x + 32, y + 86, "↑↓", 24, anchor="middle")
    b += text(28, 702, "第四周期的区块宽度", 28)
    widths = [("4s", 2, "s"), ("3d", 10, "d"), ("4p", 6, "p")]
    x = 36
    for label, count, block in widths:
        w = count * 36
        b += box(x, 736, w, 75, PALE[block], radius=0)
        b += text(x + w / 2, 782, f"{label}：{count}", 24, anchor="middle")
        x += w
    b += text(28, 862, "2 + 10 + 6 = 18；更长周期还涉及 14 格的 f 区。", 24)
    b += text(28, 910, "框图不是电子轨道照片；填充次序有例外。", 24)
    b += text(28, 952, "氦排在第18族，却是 1s²；位置也要照顾化学性质。", 22)
    assert sum(count for _, count, _ in widths) == 18
    assert 2 + 14 + 10 + 6 == 32
    save("orbital-widths", "长表的宽度，不是排版师随便拉出来的",
         "s、p、d、f亚层分别有1、3、5、7个轨道，每轨道最多2电子，得到2、6、10、14的容量。第四周期4s、3d、4p的区块宽度为2加10加6等于18。框和箭头只是量子态记号，不是经典运动轨道。", b, 995)


def timeline():
    entries = [
        ("1869", "门捷列夫发表早期周期体系", "按原子量与化学性质组织，尚不知道现代原子结构。"),
        ("1871", "表格继续修订，并为未知元素留位", "不是一张排好后永不修改的八列表。"),
        ("1905", "维尔纳提出展开式排列", "已像现代长表，但包含后来被纠正的位置与数量。"),
        ("1913", "莫塞莱的工作推动原子序数认识", "元素排序的根本编号，不再只是平均原子量。"),
        ("1923", "德明《普通化学》采用长表", "教材、仪器供应商与挂图，帮助这种画法传播。"),
        ("1988", "IUPAC推荐族号 1—18", "统一编号，不等于宣布唯一合法的图形。"),
    ]
    b = text(28, 92, "读成多人的接力，不是两国各自发明一张表。", 24)
    for i, (year, title, detail) in enumerate(entries):
        y = 130 + i * 126
        b += box(28, y, 664, 107)
        b += text(48, y + 38, year, 29, BLUE)
        b += text(155, y + 38, title, 24)
        b += text(48, y + 82, detail, 22)
    b += text(28, 940, "这是关键节点选读，不是周期表发展的完整名单。", 23)
    save("history", "一张表，是怎样被许多人慢慢改出来的？",
         "1869门捷列夫早期周期体系，1871修订与预言，1905维尔纳展开式，1913莫塞莱原子序数工作，1923德明教材长表，1988IUPAC推荐1至18族编号。并非完整发明史，也不暗示所有版本单线继承。", b, 980)


if __name__ == "__main__":
    assert len(SYMBOLS) == len(set(SYMBOLS)) == 18
    assert len(list(range(19, 37))) == 18
    assert {s: i + 19 for i, s in enumerate(SYMBOLS)} == {
        "K": 19, "Ca": 20, "Sc": 21, "Ti": 22, "V": 23, "Cr": 24,
        "Mn": 25, "Fe": 26, "Co": 27, "Ni": 28, "Cu": 29, "Zn": 30,
        "Ga": 31, "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Kr": 36,
    }
    assert 18 + 1 == 19 and 18 + 10 + 1 == 29
    fold()
    relatives()
    oxides()
    orbitals()
    timeline()
    print("Generated 5 original periodic-table diagrams; element, charge and capacity assertions passed.")
