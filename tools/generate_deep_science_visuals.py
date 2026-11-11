"""Original mechanism diagrams; all motion is a reading cue, not a physical rate."""

from html import escape
from math import cos, isclose, pi, sin
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "deep-science"
INK, BLUE, GREEN, GOLD = "#18364b", "#226ca2", "#187864", "#b56308"


def t(x, y, value, size=26, color=INK, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}">{escape(str(value))}</text>')


def rect(x, y, w, h, fill="#edf4f8", stroke="#adc4d2", radius=12):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')


def circle(x, y, r=12, fill=GREEN):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def route(d, color=BLUE, step=None, dashed=False):
    result = (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" '
              f'{"stroke-dasharray=\"7 6\"" if dashed else ""} marker-end="url(#arrow)"/>')
    if step is not None:
        result += (f'<path class="trace" data-step="{step}" style="animation-delay:{step}s" '
                   f'd="{d}" fill="none" stroke="#dc900c" stroke-width="5" '
                   'pathLength="1"/>')
    return result


def carbon(x, y, count, color=GREEN, gap=29):
    return "".join(circle(x + j * gap, y, 10, color) for j in range(count))


def save(name, title, description, body, height):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" viewBox="0 0 720 {height}" '
           'role="img" aria-labelledby="title desc" lang="zh-CN">'
           f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
           '<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" '
           'orient="auto" markerUnits="userSpaceOnUse">'
           '<path d="M1 1L10 6L1 11" fill="none" stroke="#18364b" stroke-width="2"/>'
           '</marker><radialGradient id="cloud"><stop stop-color="#6da4d4" stop-opacity=".85"/>'
           '<stop offset="1" stop-color="#6da4d4" stop-opacity=".05"/></radialGradient></defs>'
           '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}'
           '.trace{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1s linear 1 both}'
           '@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}'
           '@media(prefers-reduced-motion:reduce){.trace{animation:none}}'
           '</style>'
           f'<rect width="720" height="{height}" rx="18" fill="#fafcfe"/>'
           + t(28, 46, title, 30) + body + '</svg>\n')
    root = ET.fromstring(svg)
    assert root.get("viewBox") == f"0 0 720 {height}"
    assert root.get("width") == "720" and root.get("height") == str(height)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


def photosynthesis():
    b = t(28, 88, "先找地点，再看反应：不是叶片里的一锅绿水。", 24)
    b += '<path d="M65 225Q110 70 245 125Q295 235 140 270Z" fill="#b9ddba" stroke="#187864" stroke-width="3"/>'
    b += route("M95 245L235 139", GREEN)
    b += t(80, 310, "叶片：CO₂经气孔进入", 24)
    b += route("M270 190H370")
    b += rect(390, 125, 270, 160, "#e5f3e7", GREEN)
    b += t(415, 164, "一个叶肉细胞", 25)
    for x, y in [(430, 200), (515, 220), (605, 195)]:
        b += f'<ellipse cx="{x}" cy="{y}" rx="28" ry="15" fill="#73b881" stroke="{GREEN}"/>'
    b += t(395, 310, "绿色小体：叶绿体", 24)
    b += route("M525 325V375")
    b += '<ellipse cx="360" cy="555" rx="310" ry="155" fill="#edf8e8" stroke="#187864" stroke-width="4"/>'
    b += '<ellipse cx="360" cy="555" rx="300" ry="145" fill="none" stroke="#90b89b" stroke-width="2"/>'
    b += t(90, 456, "叶绿体剖面", 25)
    for y in [510, 530, 550, 570]:
        b += rect(135, y, 190, 16, "#87be8f", GREEN, 8)
    b += t(125, 625, "类囊体堆叠", 25)
    b += t(394, 518, "基质", 28)
    b += t(380, 560, "卡尔文循环", 25)
    b += t(380, 596, "在这里固定碳", 24)
    b += t(28, 755, "类囊体膜上：光反应；膜包围的内部叫“腔”。", 24)
    b += t(28, 796, "基质：类囊体外、叶绿体包膜内的空间。", 24)
    b += t(28, 840, "各层单独放大，形状、数量、大小均为结构示意。", 23)
    save("leaf-map", "从一片叶，走到两种反应的现场", "叶片、叶肉细胞与叶绿体逐层放大。光反应位于类囊体膜，卡尔文循环位于叶绿体基质；各层不是等比例。", b, 875)

    b = t(28, 92, "实线读电子路线；虚线读跨膜 H⁺方向。", 24)
    b += rect(28, 145, 664, 520, "#edf6ed", "#b4ceb6")
    b += t(46, 188, "叶绿体基质", 27)
    b += rect(28, 320, 664, 70, "#94c39c", GREEN, 0)
    b += t(46, 620, "类囊体腔：H⁺在这里积累", 27)
    b += route("M335 248V490", GREEN, dashed=True)
    for x, label in [(125, "光系统II"), (335, "传递链"), (550, "光系统I")]:
        b += rect(x - 64, 305, 128, 100, "#fff", GREEN)
        b += t(x, 351, label, 23, anchor="middle")
    b += t(125, 238, "光能 ↓", 27, GOLD, "middle")
    b += t(550, 238, "光能 ↓", 27, GOLD, "middle")
    b += route("M125 495V410", step=0)
    b += t(54, 530, "2 H₂O", 25)
    b += t(54, 568, "→ O₂ + 4 H⁺", 24)
    b += t(157, 451, "4 e⁻", 24, BLUE)
    b += route("M195 355H265", step=1)
    b += route("M405 355H480", step=2)
    b += route("M550 300V275H660V215", step=3)
    b += t(389, 139, "末端还原 NADP⁺ → NADPH", 23, BLUE)
    b += t(352, 468, "H⁺入腔", 24, GREEN)
    b += t(28, 711, "① 水补电子　② 接力建立梯度　③ 光再“抬升”", 24)
    b += t(28, 752, "④ 形成 NADPH；H⁺回流驱动 ATP，见正文。", 24)
    b += t(28, 797, "省略中间载体与 ATP 合酶；线长不是能量或速率。", 23)
    save("light-reactions", "水的电子，要经过两次光能帮助", "膜拓扑简图：水氧化在类囊体腔侧，电子经光系统II、传递链、光系统I，最终在基质侧用于生成NADPH。H离子梯度并非电子流本身，图省略ATP合酶。", b, 830)

    b = t(28, 92, "每个圆点代表 1 个碳；只数碳，不画完整分子。", 24)
    b += rect(28, 125, 664, 140)
    b += t(48, 166, "① 固定：3 CO₂ + 3 RuBP", 27)
    b += carbon(55, 215, 3, GOLD, 33)
    for i in range(3):
        b += carbon(240 + i * 145, 215, 5, gap=22)
    b += route("M360 275V313", step=0)
    b += rect(28, 325, 664, 160)
    b += t(48, 368, "② 还原：6 个三碳单位", 27)
    for i in range(6):
        b += carbon(65 + i * 105, 412, 3, gap=24)
    b += t(48, 458, "6 ATP + 6 NADPH：把 3-PGA 加工为 G3P", 23)
    b += route("M360 495V534", step=1)
    b += rect(28, 545, 664, 175)
    b += t(48, 584, "③ 分流：取出 1 份，留下 5 份", 27)
    b += carbon(65, 630, 3, GOLD, 25)
    b += t(48, 684, "净产 G3P", 24)
    for i in range(5):
        b += carbon(250 + i * 86, 630, 3, gap=21)
    b += t(235, 684, "15 个碳 + 3 ATP → 再生 3 RuBP", 23)
    b += route("M670 695H704V118H652", GREEN, step=2)
    b += t(28, 769, "投入 18 个碳 = 净取出 3 个 + 再生受体的 15 个", 24)
    b += t(28, 810, "净消耗 9 ATP、6 NADPH；不是 6 份产物都运走。", 24)
    save("calvin-carbon", "卡尔文循环：为什么造出六份，却只拿走一份？", "3个二氧化碳的3个碳与3个RuBP的15个碳共18个碳，形成6个三碳单位。净取出1个G3P，其余5个用于再生RuBP。圆点是收支，不是逐个标记原子的轨迹。", b, 845)


def respiration():
    b = t(28, 90, "圆点只记碳收支；不表示反应只发生这几步。", 24)
    rows = [(125, "① 葡萄糖：6 碳", [6], "糖酵解：投入 2 ATP，产生 4 ATP"),
            (305, "② 两个丙酮酸：2 × 3 碳", [3, 3], "净得 2 ATP、2 NADH；此时还没释放 CO₂"),
            (485, "③ 两个乙酰基：2 × 2 碳", [2, 2], "释放 2 CO₂，另得 2 NADH"),
            (665, "④ 两轮三羧酸循环：净释 4 CO₂", [1, 1, 1, 1], "再得 6 NADH、2 FADH₂、约 2 ATP 当量")]
    for i, (y, heading, groups, detail) in enumerate(rows):
        b += rect(28, y, 664, 145)
        b += t(48, y + 38, heading, 26)
        for j, count in enumerate(groups):
            b += carbon(65 + j * 128, y + 78, count)
        if i == 2:
            b += carbon(470, y + 78, 2, GOLD, 80)
            b += t(450, y + 112, "2 CO₂", 23, GOLD)
        b += t(48, y + 132, detail, 23)
        if i < 3:
            b += route(f"M360 {y+151}V{y+174}", step=i)
    b += t(28, 863, "总账：6 碳 → 6 CO₂；10 NADH、2 FADH₂待交电子。", 23)
    b += t(28, 904, "循环有受体再生；新进乙酰碳未必当轮离开。", 24)
    save("respiration-carbon", "一颗葡萄糖，六个碳怎样离开？", "按每分子葡萄糖的稳态净收支，糖酵解不释放CO2，丙酮酸氧化释放2个CO2，两个循环净释放4个CO2。循环不是逐个碳当轮离开的录像。", b, 940)

    b = t(28, 89, "局部展平的线粒体内膜；不是整个细胞器的形状。", 23)
    b += rect(28, 120, 664, 470, "#edf5fb")
    b += t(48, 163, "膜间隙：H⁺较多", 27)
    b += rect(28, 270, 664, 65, "#b2cfe0", BLUE, 0)
    b += t(48, 575, "线粒体基质", 27)
    for x, label in [(95, "I"), (245, "III"), (395, "IV")]:
        b += route(f"M{x} 410V190", GREEN, dashed=True)
        b += rect(x - 38, 250, 76, 110, "#fff", BLUE)
        b += t(x, 310, label, 27, anchor="middle")
        b += t(x + 12, 208, "H⁺", 23, GREEN)
    b += route("M135 302H200", step=0)
    b += route("M285 302H350", step=1)
    b += route("M395 365V425", step=2)
    b += t(35, 525, "NADH → I → Q → III → 细胞色素c → IV", 23, BLUE)
    b += t(305, 455, "O₂接电子", 24, BLUE)
    b += t(305, 490, "形成水", 24, BLUE)
    b += rect(548, 250, 76, 110, "#fff", GREEN)
    b += route("M586 190V410", GREEN, step=3)
    b += t(495, 453, "ATP 合酶", 25, GREEN)
    b += t(487, 493, "ADP + Pi → ATP", 22, GREEN)
    b += t(28, 635, "① 电子接力　② 泵 H⁺　③ 氧接电子　④ 回流合成 ATP", 22)
    b += t(28, 680, "复合体II不泵 H⁺；其电子从 Q 汇入，图中未画。", 24)
    b += t(28, 724, "箭头顺序仅供读图：真实过程耦联进行，不是排队开机。", 22)
    save("respiration-membrane", "电子向前走，H⁺绕一圈，ATP 才合成", "线粒体内膜拓扑示意，复合体I、III、IV将氢离子泵向膜间隙，电子最终给氧，氢离子经ATP合酶返回基质。省略复合体II及部分载体结构。", b, 760)


def earth():
    distances = [("金星", .723), ("地球", 1.0), ("火星", 1.524)]
    b = t(28, 91, "同一颗太阳，距离增大，单位面积收到的光变少。", 24)
    for i, (name, d) in enumerate(distances):
        flux = 1 / d**2
        y = 145 + i * 125
        b += t(28, y, f"{name}｜距离 {d:g} AU", 25)
        b += rect(28, y + 17, flux * 305, 42, [GOLD, GREEN, BLUE][i], "none", 4)
        b += t(55 + flux * 305, y + 49, f"{flux:.2f}", 25)
    b += t(28, 528, "柱长 ∝ 1 / 距离²；把地球收到的光定为 1。", 25)
    b += rect(28, 568, 664, 166, "#f7efdf", "#d9bd8f")
    b += t(48, 608, "但这不是温度计，更不是生命概率。", 27)
    b += t(48, 652, "大气、反射率、云与水循环都能改变结果。", 24)
    b += t(48, 695, "地表液态水还需要合适的压力条件。", 24)
    b += t(28, 779, "圆轨道近似：取平均轨道尺度；忽略轨道与太阳变化。", 22)
    save("earth-sunlight", "“离太阳刚好”只答对了第一小问", "以平均轨道尺度作近似，单位面积太阳辐射随距离平方反比变化。金星、地球、火星分别约为地球的1.91、1、0.43倍，不是地表温度或宜居概率。", b, 815)

    age = 4.54e9
    clock = lambda ago: (1 - ago / age) * 24
    def hhmm(h):
        minutes = round(h * 60)
        return f"{minutes//60:02d}:{minutes%60:02d}"
    events = [("地球形成", age), ("约35亿年前：已有生命证据", 3.5e9),
              ("约24亿年前：大氧化事件前后", 2.4e9),
              ("约5.39亿年前：寒武纪开始", .539e9)]
    b = t(28, 92, "模型：把 45.4 亿年等比例压成一天，现在是 24:00。", 23)
    b += route("M60 155H665")
    for hour in range(0, 25, 4):
        x = 60 + hour * 25
        b += f'<path d="M{x} 144V165" stroke="{INK}" stroke-width="2"/>'
        b += t(x, 197, f"{hour:02d}:00", 21, anchor="middle")
    for i, (label, ago) in enumerate(events):
        h = clock(ago)
        x = 60 + h * 25
        y = 250 + i * 83
        b += circle(x, 155, 6, GOLD if i else GREEN)
        b += f'<path d="M{x:.2f} 167V{y-24}H45" fill="none" stroke="#98b0c1" stroke-dasharray="4 5"/>'
        b += rect(28, y - 10, 664, 66, "#f0f5f9", "#c5d3dd", 8)
        b += t(45, y + 31, f"{hhmm(h)}　{label}", 24)
    b += rect(28, 620, 664, 175, "#f8efdf", "#d4b481")
    b += t(48, 660, "再放大午夜前的最后一小时", 27)
    b += t(48, 705, f"{hhmm(clock(66e6))}　约6600万年前：非鸟恐龙灭绝", 24)
    human_seconds = .3e6 / age * 86400
    b += t(48, 752, f"午夜前约 {human_seconds:.1f} 秒：约30万年前的智人", 24)
    b += t(28, 839, "时钟由所选近似年代换算；不是每件事的精确起点。", 23)
    b += t(28, 880, "早期生命证据的年代，不等于生命诞生的时刻。", 24)
    assert 5 < human_seconds < 6
    assert hhmm(clock(3.5e9)) == "05:30"
    assert hhmm(clock(2.4e9)) == "11:19"
    save("earth-day", "若地球历史只有一天，我们来得有多晚？", "地球45.4亿年压缩成24小时。约35亿年前生命证据约05点30分，约24亿年前大氧化事件约11点19分，寒武纪约21点09分。年代均为近似，后两项以数值生成时间。", b, 920)


def computer():
    b = t(28, 91, "只算两个二进制位；输出“本位”和“进位”。", 24)
    b += t(55, 175, "输入 a", 26) + t(55, 325, "输入 b", 26)
    b += rect(270, 130, 160, 90, "#e3eef8", BLUE)
    b += rect(270, 285, 160, 90, "#e3f2e9", GREEN)
    b += t(350, 184, "XOR 异或", 25, anchor="middle")
    b += t(350, 340, "AND 与", 25, anchor="middle")
    b += route("M145 165H250V175H265")
    b += route("M145 315H210V195H265")
    b += route("M170 165V330H265", GREEN)
    b += route("M145 315H240V350H265", GREEN)
    b += route("M440 175H545", BLUE)
    b += route("M440 330H545", GREEN)
    b += t(556, 184, "本位 s", 25, BLUE)
    b += t(556, 339, "进位 c", 25, GREEN)
    b += rect(28, 425, 664, 250)
    b += t(75, 468, "a　b", 26) + t(300, 468, "进位 c", 26) + t(510, 468, "本位 s", 26)
    for i, (a, v) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
        y = 515 + i * 42
        b += t(75, y, f"{a}　{v}", 26)
        b += t(340, y, a & v, 26)
        b += t(550, y, a ^ v, 26)
        assert 2 * (a & v) + (a ^ v) == a + v
    b += t(28, 725, "1 + 1 = 二进制 10：本位 0，把 1 交给左一位。", 24)
    b += t(28, 768, "这是半加器；连续加法还要接收前一位的进位。", 24)
    save("computer-adder", "电路不会背加法口诀，却能完成 1 + 1", "半加器逻辑：异或产生本位，与门产生进位，四种输入的真值表均由逻辑计算生成。线为逻辑连接示意，交叉不表示额外接点。", b, 805)

    program = [("LOAD", 20), ("ADD", 21), ("STORE", 22), ("HALT", None)]
    def execute(instructions, initial_memory):
        memory = initial_memory.copy()
        acc, rows = 0, []
        for pc, (op, address) in enumerate(instructions):
            if op == "LOAD":
                acc = memory[address]
            elif op == "ADD":
                acc += memory[address]
            elif op == "STORE":
                memory[address] = acc
            elif op != "HALT":
                raise ValueError(f"Unknown toy instruction: {op}")
            rows.append((pc, op + (f" [{address}]" if address is not None else ""), acc, memory[22]))
            if op == "HALT":
                break
        return rows, memory

    initial_memory = {20: 13, 21: 7, 22: 0}
    rows, memory = execute(program, initial_memory)
    assert [row[2:] for row in rows] == [(13, 0), (20, 0), (20, 20), (20, 20)]
    assert initial_memory[22] == 0 and memory[22] == 20
    _, changed_input = execute(program, {20: 13, 21: 9, 22: 0})
    assert changed_input[22] == 22
    stopped_rows, no_store = execute(program[:2] + [("HALT", None)], initial_memory)
    assert stopped_rows[-1][2:] == (20, 0) and no_store[22] == 0
    b = t(28, 90, "玩具 CPU：ACC 存当前值，PC 指向当前指令。", 24)
    b += rect(28, 120, 664, 150)
    b += t(48, 162, "内存初态", 28)
    b += t(48, 207, "[20] = 13　　[21] = 7　　[22] = 0", 26)
    b += t(48, 246, "方括号内是地址；等号右边才是数据。", 24)
    for i, (pc, op, a, stored) in enumerate(rows):
        y = 310 + i * 120
        b += rect(28, y, 664, 90, "#f0f5f9")
        b += t(48, y + 35, f"PC {pc}：{op}", 26)
        b += t(48, y + 73, f"执行后 ACC = {a}；[22] = {stored}", 24)
        if i < 3:
            b += route(f"M360 {y+94}V{y+114}", step=i)
    b += t(28, 837, "每步都经历：取指令 → 译码 → 执行 → 更新状态。", 23)
    b += t(28, 880, "自定义指令教学模型，不是 x86、ARM 或 Hack 指令集。", 22)
    save("computer-execution", "把 13 + 7 算完：谁记住下一步该做什么？", "四条自定义玩具CPU指令读取地址20的13，加上地址21的7，存到地址22，最后停止。所有执行状态由脚本模拟产生，未规定实际指令编码与时钟周期。", b, 915)

    glyph = ["01110", "10001", "10001", "11111", "10001", "10001", "10001"]
    b = t(28, 91, "同一个字符，可以有许多不同字形。", 26)
    b += rect(28, 130, 328, 365)
    b += t(48, 177, "字符身份：A", 29)
    b += t(48, 233, "Unicode：U+0041", 25)
    b += t(48, 283, "十进制码点：65", 25)
    b += t(48, 333, "UTF-8：41（十六进制）", 22)
    b += t(48, 383, "二进制：01000001", 24)
    b += t(48, 450, "编码不存“这个字的照片”", 23)
    for row, bits in enumerate(glyph):
        for col, bit in enumerate(bits):
            b += rect(425 + col * 40, 150 + row * 40, 36, 36,
                      BLUE if bit == "1" else "#e8eef3", "#a9bfd0", 2)
    b += t(525, 476, "原创 5 × 7 字形", 24, anchor="middle")
    b += t(28, 550, "数值 20：单字节无符号表示可为 14（十六进制）", 23)
    b += t(28, 593, "文本“20”：UTF-8 则是 32 30（十六进制）", 24)
    b += t(28, 638, "字符 → 字形 → 图形结果；真实排版还包含许多步骤。", 22)
    assert ord("A") == 65 and "A".encode() == bytes([0x41])
    assert (20).to_bytes(1) == bytes([0x14]) and "20".encode() == bytes([0x32, 0x30])
    assert len(glyph) == 7 and all(len(row) == 5 for row in glyph)
    save("computer-display", "内存里的一个数，不会自动变成屏幕上的字", "字符A的码点、UTF8编码与原创5乘7像素字形对照；数值20的一个字节表示和字符串20的两个UTF8字节不同。字形网格是教学示意。", b, 675)


def dna():
    b = t(28, 91, "借鉴读者截图的放大路线；以下各幅分别放大。", 24)
    for i in range(3):
        b += rect(28, 125 + 235 * i, 664, 215)
    for y in range(155, 305, 5):
        phase = (y - 155) / 150 * 2 * pi
        x1, x2 = 145 + 48 * sin(phase), 145 - 48 * sin(phase)
        b += circle(x1, y, 4, GREEN) + circle(x2, y, 4, GOLD)
        if (y - 155) % 25 == 0:
            b += f'<path d="M{x1:.2f} {y}H{x2:.2f}" stroke="{BLUE}" stroke-width="4"/>'
    b += t(265, 172, "① DNA 本身就是大分子", 26)
    b += t(265, 219, "B 型双螺旋：宽约 2 nm", 24)
    b += t(265, 266, "不是所有 DNA 都长 2 nm", 24)
    b += t(265, 309, "把镜头移到局部化学结构 ↓", 24)
    # A bent water molecule illustrates why the screenshot's generic size is not universal.
    b += f'<path d="M145 412L97 464M145 412L193 464" stroke="#90a5b4" stroke-width="12"/>'
    b += circle(145, 412, 28, "#bb5147")
    b += circle(97, 464, 19, BLUE) + circle(193, 464, 19, BLUE)
    b += t(145, 420, "O", 23, "#fff", "middle")
    b += t(97, 472, "H", 20, "#fff", "middle") + t(193, 472, "H", 20, "#fff", "middle")
    b += t(265, 409, "② 分子没有统一的尺寸", 26)
    b += t(265, 455, "水只是例子，不是 DNA 单元", 24)
    b += t(265, 501, "典型小分子可在亚纳米量级", 24)
    b += t(265, 544, "DNA 由碳、氢、氧、氮、磷等组成", 22)
    b += circle(145, 690, 73, "url(#cloud)") + circle(145, 690, 5, GOLD)
    b += t(265, 644, "③ 原子：约 10⁻¹⁰ m 量级", 26)
    b += t(265, 690, "电子云：概率分布示意", 24)
    b += t(265, 736, "没有画行星式电子轨道", 24)
    b += t(265, 779, "中央核点已夸大；真实比例见尺", 23)
    b += t(28, 865, "此图讲组成与层次；大小比较请用正文对数尺。", 24)
    save("dna-chemistry", "沿着截图放大：先从生命走进化学", "原创中文版分层示意：DNA就是大分子，水分子只是小分子例子，不是DNA的重复单元；原子用电子云而非行星轨道表示。各图独立放大，核点夸大。", b, 905)

    b = t(28, 91, "不是实心套娃：电子那条支路并不会通向夸克。", 24)
    for i in range(3):
        b += rect(28, 125 + 235 * i, 664, 215)
    for row in range(-2, 3):
        for col in range(-2, 3):
            if row**2 + col**2 <= 5:
                b += circle(145 + col * 25, 228 + row * 25, 13,
                            BLUE if (row + col) % 2 else GOLD)
    b += t(265, 172, "④ 原子核：约 10⁻¹⁵～10⁻¹⁴ m", 24)
    b += t(265, 218, "尺度随核种与定义改变", 24)
    b += t(265, 264, "通常含质子和中子", 24)
    b += t(265, 309, "普通氢核只有一个质子", 24)
    b += circle(145, 462, 76, "#e4ecf7")
    for angle, label in zip([0, 2 * pi / 3, 4 * pi / 3], ["u", "u", "d"]):
        x, y = 145 + 40 * cos(angle), 462 + 40 * sin(angle)
        b += circle(x, y, 17, BLUE) + t(x, y + 8, label, 23, "#fff", "middle")
    b += t(265, 409, "⑤ 质子：特征尺度在飞米量级", 24)
    b += t(265, 455, "均方根电荷半径约 0.84 fm", 24)
    b += t(265, 501, "u、u、d 只表示价夸克组成", 24)
    b += t(265, 544, "还涉及胶子与海夸克，不是三弹珠", 22)
    b += f'<path d="M110 695H180M145 660V730" stroke="{BLUE}" stroke-width="3"/>'
    b += t(145, 775, "符号，不是照片", 22, anchor="middle")
    b += t(265, 644, "⑥ 夸克：未测得有限大小", 26)
    b += t(265, 690, "标准模型中按点状粒子描述", 24)
    b += t(265, 736, "10⁻¹⁸ m 仅作参照长度", 24)
    b += t(265, 779, "不能把紫色圆球当作实测外形", 24)
    b += t(28, 865, "1 nm = 10⁻⁹ m；1 fm = 10⁻¹⁵ m；各幅不同比例。", 23)
    save("dna-particles", "继续放大：从原子核走到尚未分辨的边界", "原子核和质子各自放大。质子的三价夸克仅代表组成，非静态三球模型。夸克画为定位符号，不赋予有限半径。电子不是由夸克组成。", b, 905)


def main():
    assert 3 + 3 * 5 == 6 * 3 == 3 + 5 * 3
    assert 6 + 3 == 9
    assert 6 == 2 * 3 == 2 * 2 + 2 == 2 + 4
    assert (2 + 2 + 6) * 2 + 2 * 2 == 24  # Electron-pair carriers account for 24 electrons.
    assert 4 + 10 * 2.5 + 2 * 1.5 == 32
    assert 4 + 8 * 2.5 + 2 * 1.5 + 2 * 1.5 == 30
    assert isclose(1 / .723**2, 1.913, abs_tol=.001)
    assert int("01101", 2) + int("00111", 2) == int("10100", 2) == 20
    for a in range(2):
        for b in range(2):
            for carry in range(2):
                s = a ^ b ^ carry
                c = (a & b) | (carry & (a ^ b))
                assert 2 * c + s == a + b + carry
    photosynthesis()
    respiration()
    earth()
    computer()
    dna()
    print("Generated 12 original mechanism diagrams; numerical and logic assertions passed.")


if __name__ == "__main__":
    main()
