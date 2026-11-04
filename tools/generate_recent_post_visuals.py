"""Rebuild the original educational SVGs added to the October/November 2026 posts."""

from html import escape
from math import exp, hypot
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
INK = "#20334d"
COLORS = ("#1e6e9a", "#8750a7", "#197858")
STYLE = """
text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}
.s1{animation:r1 4.5s steps(1,end) 1 both}
.s2{animation:r2 4.5s steps(1,end) 1 both}
.s3{animation:r3 4.5s steps(1,end) 1 both}
@keyframes r1{0%,9%{opacity:0}10%,100%{opacity:1}}
@keyframes r2{0%,34%{opacity:0}35%,100%{opacity:1}}
@keyframes r3{0%,64%{opacity:0}65%,100%{opacity:1}}
@media(prefers-reduced-motion:reduce){.s1,.s2,.s3,.spinner{animation:none}}
"""


def label(x, y, value, size=22, anchor="middle", color=INK, bold=False):
    weight = ' font-weight="700"' if bold else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}"{weight}>{escape(str(value))}</text>'


def line(x1, y1, x2, y2, color="#a6b1c2", width=2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def box(x, y, w, h, color="#eef2f8"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{color}"/>'


def write(name, height, title, description, body, extra_style=""):
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<style>{extra_style}{STYLE}</style>
<rect width="1000" height="{height}" rx="20" fill="#faf8f3"/>
{body}
</svg>
'''
    ET.fromstring(content)
    target = ROOT / "assets" / "images" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def dna():
    assert 2e-9 * 1e10 == 20
    assert abs(1e-10 * 1e10 - 1) < 1e-12
    assert abs(1e-15 * 1e10 - 1e-5) < 1e-18
    b = label(500, 48, "同一把放大尺：每个长度都乘 100 亿", 28, bold=True)
    b += label(500, 88, "不是物质真的变大，而是用同一比例重新理解尺度", 21)
    cards = [
        ("DNA 宽", "2 纳米", "20 米", "一座楼的宽度"),
        ("典型原子尺度", "0.1 纳米", "1 米", "日常家具尺度"),
        ("选取的核尺度", "1 飞米", "0.01 毫米", "仍是细小尘粒量级"),
    ]
    for i, (name, real, model, note) in enumerate(cards):
        x = 35 + i * 325
        b += f'<g class="s{i+1}">'
        b += box(x, 132, 285, 297, ["#e6eff9", "#f0e7f7", "#e4f2eb"][i])
        b += label(x+142, 175, f"{i+1}  {name}", 23, bold=True)
        b += label(x+142, 226, real, 25)
        b += label(x+142, 272, "× 100 亿 ↓", 22)
        b += label(x+142, 326, model, 32, color=COLORS[i], bold=True)
        b += label(x+142, 386, note, 18)
        b += "</g>"
    b += label(500, 480, "DNA 已像楼那么宽，原子核却依然很小", 26, bold=True)
    b += label(500, 526, "各卡片不是按面积或直径等比例画出的物体；精确的是上面的长度换算。", 19)
    b += label(500, 566, "原子没有硬球边界；核尺度随核种变化；这里没有给夸克指定实测直径。", 19)
    write("dna-scale/uniform-zoom.svg", 605, "DNA、原子与原子核的统一放大换算",
          "三步显示统一放大100亿倍的结果：2纳米变20米，0.1纳米变1米，选取的1飞米变0.01毫米。卡片大小不代表物体比例。", b)


def irrational():
    assert 141421**2 < 2 * 100000**2
    assert 14142 * 10 < 141421
    b = label(500, 48, "用有理数提问：先分不出，再找到分界", 28, bold=True)
    b += label(500, 86, "x = 1.4142，y = √2；每一行只展示一次比较，不是无限检验", 20)
    rows = [
        ("① 问：比 1.4 大吗？", "x：大于", "y：大于", "这道问题分不出它们。"),
        ("② 问：比 1.415 小吗？", "x：小于", "y：小于", "第二次仍然分不出。"),
        ("③ 问：比 1.41421 小吗？", "x：小于", "y：大于", "终于找到一个区分它们的有理数。"),
    ]
    for i, (question, left, right, note) in enumerate(rows):
        y = 116 + 119*i
        b += f'<g class="s{i+1}">' + box(42, y, 916, 104)
        b += label(66, y+37, question, 23, anchor="start", bold=True)
        b += label(550, y+37, left, 22, color=COLORS[0])
        b += label(790, y+37, right, 22, color=COLORS[1])
        b += label(66, y+78, note, 20, anchor="start")
        b += "</g>"
    x0, x1 = 120, 880
    value = lambda q: x0 + (q-1.4142)/.00002*(x1-x0)
    b += label(500, 523, "放大窗口：[1.41420, 1.41422]，不是从 0 开始的数轴", 20)
    b += line(x0, 568, x1, 568, INK, 3)
    for q, name, y in [(1.4142, "x = 1.4142", 610), (1.41421, "r = 1.41421", 548), (2**.5, "y = √2", 610)]:
        x = value(q)
        b += line(x, 560, x, 577, INK)
        b += label(x, y, name, 21, bold=True)
    b += label(500, 659, "r² = 1.9999899241 ＜ 2，所以 x ＜ r ＜ √2", 24, bold=True)
    b += label(500, 700, "有限次回答相同不能证明相等；所有有理数的比较关系才是定义的关键。", 19)
    write("irrational-comparison/rational-questions.svg", 735, "三个有理数问题区分1.4142与根号二",
          "前两次比较一致，第三个有理数1.41421位于1.4142与根号二之间。底部是明确标出窗口范围的局部线性数轴。有限实验不是相等证明。", b)


def ui_status():
    b = label(500, 48, "同一个等待界面，两种不同的信息", 28, bold=True)
    b += label(500, 88, "以下是概念示意，不是 Claude Code、Copilot 或 Cursor 的真实截图", 20)
    b += box(40, 120, 430, 350, "#eae8f7") + box(530, 120, 430, 350, "#e5f1ed")
    b += label(255, 164, "陪伴性文案", 25, bold=True)
    b += '<g class="spinner" style="transform-origin:255px 235px"><path d="M255 207 A28 28 0 1 1 227 235" fill="none" stroke="#8750a7" stroke-width="7" stroke-linecap="round"/></g>'
    b += label(255, 303, "Spelunking…", 29, bold=True)
    b += label(255, 355, "像在探险：传达气氛与个性", 21)
    b += label(255, 413, "不能据此推断读了哪些文件", 20)
    b += label(745, 164, "可核查的任务反馈", 25, bold=True)
    for i, value in enumerate(["① 读取：3 个相关文件", "② 修改：1 个目标文件", "③ 检查：结果另行展示"]):
        b += f'<g class="s{i+1}">' + label(565, 235+i*69, value, 23, anchor="start") + "</g>"
    b += label(745, 437, "示意次序不代表真实任务耗时", 18)
    b += label(500, 520, "会动 ≠ 有进展；完成操作 ≠ 已证明结果正确", 27, bold=True)
    b += label(500, 567, "动画只演示两层反馈的区别，不是模拟真实后台状态或百分比。", 20)
    write("ai-status/feedback-layers.svg", 605, "等待文案和操作反馈的差别",
          "左侧转圈配Spelunking文案，不提供可核查进度；右侧逐步列出示意操作，最后提醒仍需检查结果。不是任何产品的真实截图。",
          b, ".spinner{animation:spin 4s linear 1}@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(720deg)}}")


def conics():
    source = ROOT / "assets/images/conic-sections/03-dandelin-ellipse.svg"
    r = ET.parse(source).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    r.find(ns+"title").text = "丹德林球：两次切线等长，再拼成定长"
    r.find(ns+"desc").text = "沿用原轴截面图；先显出蓝色同球切线，再显出红色同球切线，最后合并为PF1加PF2等于AB。不是球或截平面移动的动画。"
    r.find(ns+"style").text += STYLE
    for e in r:
        stroke = e.get("stroke")
        if stroke == "#2563eb":
            e.set("class", "s1")
        elif stroke == "#be185d":
            e.set("class", "s2")
        if e.tag == ns+"text":
            y = float(e.get("y"))
            if y == 177:
                e.text = "① 蓝色同球切线：PF₁ = PA"
                e.set("class", "small s1")
            elif y == 211:
                e.text = "② 红色同球切线：PF₂ = PB"
                e.set("class", "small s2")
            elif y == 410:
                e.text = "③ 相加：PF₁ + PF₂ = AB"
                e.set("class", "small s3")
    points = {"P": (394.27,379.87), "A": (327,496.38), "B": (415.72,342.71),
              "F1": (273.93,440.04), "F2": (355.89,399.05)}
    distance = lambda a, b: hypot(points[a][0]-points[b][0], points[a][1]-points[b][1])
    assert abs(distance("P","F1")-distance("P","A")) < .03
    assert abs(distance("P","F2")-distance("P","B")) < .03
    assert abs(distance("P","A")+distance("P","B")-distance("A","B")) < .03
    target = ROOT / "assets/images/conic-sections/08-dandelin-steps.svg"
    ET.ElementTree(r).write(target, encoding="utf-8", xml_declaration=False)


def shell():
    b = label(500, 48, "半径只取外面 1%，体积能占多少？", 28, bold=True)
    b += label(500, 88, "同样的壳厚 ε = 0.01；条长表示体积比例，不是球的形状", 20)
    b += label(120, 137, "维度 n", 20) + label(565, 137, "外壳占比：1 − 0.99ⁿ", 21)
    for i, n in enumerate([2, 3, 10, 100, 1000]):
        fraction = 1-.99**n
        assert 0 < fraction < 1
        y = 170+i*69
        b += label(120, y+25, n, 24, bold=True) + box(215, y, 610, 34, "#e7e8ef")
        b += f'<rect x="215" y="{y}" width="{610*fraction}" height="34" rx="4" fill="#277c67" data-n="{n}" data-fraction="{fraction}"/>'
        b += label(850, y+25, f"{fraction*100:.4f}%", 19, anchor="start")
    b += label(500, 563, "先固定壳厚，再提高维度：不是把二维圆环画得越来越厚", 23, bold=True)
    b += label(500, 607, "前提：在整个单位球体内均匀采样。中心仍在球内，球面本身的体积仍为 0。", 19)
    write("embedding-geometry/thin-shell.svg", 650, "固定1%半径厚度下的高维球壳体积比例",
          "2、3、10、100、1000维的外壳占比依次为1.99%、2.9701%、9.5618%、63.3968%、99.9957%。横条是数值图表，不是高维球的投影。", b)


def attention():
    scores = [3., 0., 1.]
    weights = [exp(s)/sum(exp(v) for v in scores) for s in scores]
    assert abs(sum(weights)-1) < 1e-12
    values = [(1.,0.), (0.,1.), (.5,.5)]
    output = [sum(w*v[j] for w,v in zip(weights,values)) for j in range(2)]
    b = label(500, 48, "把注意力算一遍：分数 → 权重 → 加权取值", 27, bold=True)
    b += label(500, 87, "单头、单位置的玩具例子：三处可见信息；不是某个真实模型的测量", 19)
    headings = ["① 已缩放的匹配分数", "② softmax 后的权重", "③ 乘上对应的 V"]
    for i, heading in enumerate(headings):
        x = 30+i*328
        b += f'<g class="s{i+1}">' + box(x, 122, 303, 300, ["#e6eff9","#f0e7f7","#e4f2eb"][i])
        b += label(x+151, 165, heading, 21, bold=True)
        for j in range(3):
            name = "ABC"[j]
            value = [f"{name}：{scores[j]:g}", f"{name}：{weights[j]:.3f}", f"{weights[j]:.3f} × {values[j]}"][i]
            b += label(x+151, 232+j*70, value, 22)
        b += "</g>"
    b += label(500, 475, f"先用未四舍五入的权重计算：o ≈ ({output[0]:.4f}, {output[1]:.4f})", 25, bold=True)
    b += label(500, 524, "Q、K 参与算匹配分数；真正混合的内容来自 V，而不是把分数本身当内容。", 19)
    b += label(500, 565, "权重总和为 1，但不是“属于某个语义类别的概率”；输出还不是整个 Transformer 层。", 18)
    write("embedding-geometry/attention-steps.svg", 605, "单头注意力的具体数值分步图",
          "分数3、0、1经softmax后约0.844、0.042、0.114；值向量分别为(1,0)、(0,1)、(0.5,0.5)，加权输出约(0.9009,0.0991)。分三步出现，最终保留完整图。", b)


if __name__ == "__main__":
    for generate in [dna, irrational, ui_status, conics, shell, attention]:
        generate()
    print("Generated 6 SVGs; scale conversions, rational bounds, tangent lengths, shell fractions and attention weights verified.")
