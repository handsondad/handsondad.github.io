"""Original catenary diagrams: equilibrium, load distribution and thermal sag."""

import math
from pathlib import Path
import xml.etree.ElementTree as ET

from generate_kepler_newton_visuals import BLUE, GOLD, INK, RED, dot, line, panel, path, save, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "catenary"
SPAN, W, A0, ALPHA = 200.0, 10.0, 500.0, 2e-5
L0 = 2 * A0 * math.sinh(SPAN / (2 * A0))


def ordinate(x, a):
    return 2 * a * math.sinh(x / (2 * a)) ** 2


def sag(a, span=SPAN):
    return ordinate(span / 2, a)


def length(a, span=SPAN):
    return 2 * a * math.sinh(span / (2 * a))


def parameter_for_length(target, span=SPAN):
    if target <= span:
        raise ValueError("A finite-tension hanging cable must be longer than its span")
    low, high = span / 100, span
    while length(high, span) > target:
        high *= 2
    for _ in range(100):
        mid = (low + high) / 2
        if length(mid, span) > target:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def parameter_for_sag(depth, span):
    if depth <= 0:
        raise ValueError("Sag must be positive")
    low, high = span / 100, span
    while sag(high, span) > depth:
        high *= 2
    for _ in range(100):
        mid = (low + high) / 2
        if sag(mid, span) > depth:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def thermal(delta):
    total = L0 * (1 + ALPHA * delta)
    a = parameter_for_length(total)
    w = W * L0 / total
    return a, total, w, w * a


def write(name, height, title, desc, body, css=""):
    save(name, height, title, desc, text(36, 44, title, 27) + body,
         css, output_directory=OUT)


def points(fn, lo, hi, ox, oy, sx, sy, count=160):
    return [(ox + sx * x, oy - sy * fn(x))
            for x in (lo + (hi - lo) * i / count for i in range(count + 1))]


def comparison():
    body = ""
    for i, a in enumerate([10.0, 1.0]):
        top, bottom, scale = 70 + 370 * i, 325 + 370 * i, 100
        depth = sag(a, 4)
        body += panel(top, 345)
        body += text(48, top + 38, "① 浅垂：几乎重合" if i == 0 else "② 深垂：差别显现", 24)
        sy = 125 if i == 0 else 65
        cat = lambda x: ordinate(x, a)
        parabola = lambda x: depth * (x / 2) ** 2
        body += path(points(parabola, -2, 2, 360, bottom, scale, sy), GOLD, 4, dash=True)
        body += path(points(cat, -2, 2, 360, bottom, scale, sy), BLUE, 4)
        for x in [-2, 2]:
            body += dot(360 + scale * x, bottom - sy * depth, 7, INK)
        body += dot(360, bottom, 5, INK)
        body += text(360, bottom + 28, "同一最低点", 21, INK, "middle")
        gap = parabola(1) - cat(1)
        body += text(48, top + 318, f"跨度 4 米；弧垂 {depth:.3f} 米；x＝1 处差 {gap:.4f} 米", 20)
        if i == 1:
            body += line(460, bottom - sy * parabola(1), 460, bottom - sy * cat(1), RED)
    body += text(48, 860, "蓝实线：悬链线；金虚线：同端点、同底部的抛物线。", 22)
    body += text(48, 907, "横纵标度独立；上图纵向放大，下图纵向压缩。", 22)
    write("chain-or-parabola.svg", 950, "图 1｜都像一个 U，却不是同一种曲线",
          "两组悬链线与抛物线各有相同跨度、最低点和弧垂。浅垂时近似重合，深垂时区别可见；坐标标度不等。", body)


def distribution():
    body = ""
    for i in range(2):
        top, bottom = 70 + i * 385, 315 + i * 385
        body += panel(top, 365)
        body += text(48, top + 36, "① 同样长的链段 → 同样重" if i == 0 else "② 同样宽的桥面段 → 同样重", 24)
        if i == 0:
            body += path(points(lambda x: ordinate(x, 1), -2, 2, 360, bottom, 100, 55), BLUE, 4)
            arc = math.sinh(2)
            xs = [math.asinh(-arc + 2 * arc * k / 8) for k in range(9)]
            for k, x in enumerate(xs):
                px, py = 360 + 100 * x, bottom - 55 * ordinate(x, 1)
                body += dot(px, py, 5, RED)
                if k < 8:
                    xm = math.asinh(-arc + 2 * arc * (k + .5) / 8)
                    body += line(360 + 100 * xm, bottom - 55 * ordinate(xm, 1) + 8,
                                 360 + 100 * xm, bottom - 55 * ordinate(xm, 1) + 37, RED, arrow=True)
            body += text(48, top + 319, "红点之间的弧长相等，水平间距却不相等。", 22)
        else:
            cable = lambda x: .45 * x * x + .4
            body += path(points(cable, -2, 2, 360, bottom, 100, 60), GOLD, 4)
            body += line(160, bottom + 15, 560, bottom + 15, INK)
            for k in range(9):
                x = -2 + k * .5
                px = 360 + 100 * x
                body += line(px, bottom - 60 * cable(x), px, bottom + 15, "#8295a5")
                if k < 8:
                    body += line(px + 25, bottom + 24, px + 25, bottom + 53, RED, arrow=True)
            body += text(48, top + 340, "细线为吊杆；相同桥面段传给主缆相同的载荷。", 21)
    body += text(48, 890, "一个按 ds 数重量，一个按 dx 数重量。", 27, BLUE)
    body += text(48, 938, "等长链段是积分单元示意，不是对真实链环逐个建模。", 21)
    write("where-weight-lives.svg", 980, "图 5｜重量是沿链条，还是沿桥面分布？",
          "上图按弧长等分均匀链条，等长段等重；下图按水平距离等分均匀桥面，等宽段等重。箭头长短仅表等重，不比较上下两种模型的数值。", body)


def forces():
    a, x, w, scale = 1.0, 1.2, 10.0, 145
    s = a * math.sinh(x / a)
    horizontal, vertical = w * a, w * s
    px, py = 130 + scale * x, 385 - scale * ordinate(x, a)
    body = panel(70, 490)
    body += text(48, 112, "只取最低点 O 到右侧 P 的这一段链条。", 24)
    body += path(points(lambda u: ordinate(u, a), 0, x, 130, 385, scale, scale), BLUE, 5)
    body += dot(130, 385, 6, INK) + text(130, 421, "O", 22, INK, "middle")
    body += dot(px, py, 6, INK) + text(px - 16, py - 10, "P", 22, INK, "end")
    # Weight acts at the segment's center of mass, not at the arc midpoint.
    center_x = (x * math.sinh(x) - math.cosh(x) + 1) / math.sinh(x)
    center_y = ((x / 2 + math.sinh(2 * x) / 4) - math.sinh(x)) / math.sinh(x)
    arrows = [
        line(130, 385, 55, 385, GOLD, arrow=True),
        line(px, py, px + 75, py - 7.5 * vertical, RED, arrow=True),
        line(130 + scale * center_x, 385 - scale * center_y,
             130 + scale * center_x, 385 - scale * center_y + 7.5 * vertical, BLUE, arrow=True),
    ]
    css = ""
    for i, arrow in enumerate(arrows):
        body += f'<g class="force-{i}" data-reveal="force-{i}">{arrow}</g>'
        css += (f".force-{i}{{opacity:1;animation:show-force .4s linear {1+i}s 1 both}}")
    css += "@keyframes show-force{from{opacity:0}to{opacity:1}}"
    css += "@media(prefers-reduced-motion:reduce){[data-reveal]{animation:none;opacity:1}}"
    body += text(48, 477, "O：左拉 H；P：斜向右上拉；重力：向下。", 23)
    body += text(48, 526, "箭头依同一力尺度绘制；动画仅逐步显示受力。", 21)
    body += panel(585, 370)
    body += text(48, 627, "把 P 点的斜拉力拆成两个分量", 24)
    fx, fy, factor = 220, 850, 10
    body += line(fx, fy, fx + factor * horizontal, fy, GOLD, arrow=True)
    body += line(fx + factor * horizontal, fy, fx + factor * horizontal, fy - factor * vertical, BLUE, arrow=True)
    body += line(fx, fy, fx + factor * horizontal, fy - factor * vertical, RED, arrow=True)
    body += text(360, 720, f"竖直 V＝{vertical:.3f} 牛", 23, BLUE)
    body += text(360, 766, f"斜拉 T＝{math.hypot(horizontal, vertical):.3f} 牛", 23, RED)
    body += text(360, 850, "水平 H＝10 牛", 23, GOLD)
    body += text(48, 915, f"链长 s＝{s:.3f} 米；每米重 w＝10 牛；V＝ws。", 22)
    body += text(48, 1005, "斜率 y′＝V / H：越往外，需要托住的链越多。", 23)
    write("cut-and-balance.svg", 1050, "图 2｜剪出一段链，算清三股力",
          "从最低点到x为1.2米处的一段理想均匀链，悬链参数a为1米。水平张力10牛，竖直分量等于链段总重15.095牛。重量箭头置于链段重心；下方静态分力图始终保留。", body, css)


def accumulating():
    body, css = "", ""
    for i, s in enumerate([.5, 1.0, 1.5]):
        top, ox, oy = 70 + 280 * i, 105, 280 + 280 * i
        x = math.asinh(s)
        body += panel(top, 265)
        body += text(48, top + 36, f"步骤 {i+1}：从最低点数到链长 {s:.1f} 米", 24)
        body += path(points(lambda u: ordinate(u, 1), 0, math.asinh(1.5),
                            ox, oy, 125, 125), "#ccd8e2", 4)
        selected = points(lambda u: ordinate(u, 1), 0, x, ox, oy, 125, 125)
        body += (f'<path class="segment-{i}" data-segment="{i}" '
                 f'd="{path_data(selected)}" pathLength="1" fill="none" '
                 f'stroke="{BLUE}" stroke-width="6"/>')
        css += (f".segment-{i}{{stroke-dasharray:1;stroke-dashoffset:0;"
                f"animation:trace-segment 1.2s linear {1+1.5*i}s 1 both}}")
        for k in range(i + 2):
            ss = .5 * k
            xx = math.asinh(ss)
            body += dot(ox + 125 * xx, oy - 125 * ordinate(xx, 1), 5, INK)
        px, py = ox + 125 * x, oy - 125 * ordinate(x, 1)
        body += line(px, py, px + 30, py - 30 * s, RED, arrow=True)
        fx, fy = 435, top + 170
        body += line(fx, fy, fx + 70, fy, GOLD, arrow=True)
        body += line(fx + 70, fy, fx + 70, fy - 70 * s, BLUE, arrow=True)
        body += line(fx, fy, fx + 70, fy - 70 * s, RED, arrow=True)
        body += text(540, top + 125, f"V＝{10*s:.0f} 牛", 22, BLUE)
        body += text(435, top + 209, "H＝10 牛不变", 22, GOLD)
        body += text(48, top + 239, f"x＝{x:.3f} 米；切线斜率＝V/H＝{s:.1f}", 22)
    css += "@keyframes trace-segment{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}"
    css += "@media(prefers-reduced-motion:reduce){[data-segment]{animation:none;stroke-dashoffset:0}}"
    body += text(48, 958, "黑点每隔 0.5 米链长；不是每隔 0.5 米水平距离。", 22)
    body += text(48, 1003, "动画只依次选取静止链段，不表示链条在伸长或下落。", 21)
    write("length-builds-slope.svg", 1045, "图 3｜多托住一段链，拉力就更陡",
          "同一条静止均匀悬链线上，从最低点取链长0.5、1和1.5米的三个截段。每米重10牛，水平张力10牛，竖直张力分别为5、10和15牛；切线斜率为0.5、1和1.5。链图横纵等比例，分力三角形用相同的独立力尺度。", body, css)


def calculus():
    body = panel(70, 455)
    body += text(48, 110, "双曲余弦 cosh u，是两条指数曲线的平均。", 23)
    ox, oy, sx, sy = 360, 450, 185, 75
    body += line(110, oy, 625, oy, INK, arrow=True)
    body += line(ox, oy, ox, 160, INK, arrow=True)
    for fn, color, dash in [(math.exp, RED, False), (lambda u: math.exp(-u), GOLD, True), (math.cosh, BLUE, False)]:
        body += path(points(fn, -1.2, 1.2, ox, oy, sx, sy), color, 3, dash=dash)
    for u in [-1, 0, 1]:
        body += text(ox + sx * u, oy + 30, u, 21, INK, "middle")
    for v in [1, 2, 3]:
        body += text(340, oy - sy * v + 7, v, 20, INK, "end")
    at = 1
    body += line(ox + sx * at, oy - sy * math.exp(at), ox + sx * at, oy - sy * math.exp(-at), "#8295a5", dash=True)
    body += dot(ox + sx * at, oy - sy * math.cosh(at), 6, BLUE)
    body += text(70, 158, "红实线 eᵘ", 21, RED)
    body += text(70, 195, "金虚线 e⁻ᵘ", 21, GOLD)
    body += text(70, 232, "蓝线 cosh u", 21, BLUE)
    body += text(600, 495, "u＝x/a", 22, INK, "middle")
    body += panel(550, 295)
    for i, value in enumerate([
        "① 受力：H 不变，V＝ws，y′＝ws/H。",
        "② 弧长：ds/dx＝√(1＋y′²)。",
        "③ 积分：y＝a[cosh(x/a)－1]，a＝H/w。",
    ]):
        body += text(48, 600 + i * 78, value, 24)
    body += text(48, 805, "减去 1：把链的最低点移到 y＝0。", 23, BLUE)
    body += text(48, 900, "这里使用现代函数与符号，不冒充 1691 年原稿。", 22)
    write("calculus-finds-chain.svg", 945, "图 4｜从受力条件，到一条函数",
          "指数函数exp(u)和exp(-u)的平均为cosh(u)，灰竖线及蓝点给出u为1处的平均值。下方列出受力、弧长与积分三步，采用现代写法。", body)


def bridge():
    span, depth = 200.0, 20.0
    a = parameter_for_sag(depth, span)
    body = ""
    for i in range(2):
        top, base = 70 + i * 380, 190 + i * 380
        body += panel(top, 355)
        body += text(48, top + 38, "① 主缆只承受自身重量" if i == 0 else "② 主缆承受均匀水平桥面载荷", 24)
        cable = (lambda x: ordinate(x, a)) if i == 0 else (lambda x: depth * (2 * x / span) ** 2)
        pts = [(360 + 2.5 * x, base + 5 * (depth - cable(x)))
               for x in (-100 + 200 * k / 160 for k in range(161))]
        body += path(pts, BLUE if i == 0 else GOLD, 5)
        for px in [110, 610]:
            body += line(px, base - 22, px, base + 155, INK)
            body += dot(px, base, 6, INK)
        if i == 1:
            body += line(110, base + 138, 610, base + 138, BLUE)
            for x in range(-80, 81, 20):
                px, py = 360 + 2.5 * x, base + 5 * (depth - cable(x))
                body += line(px, py, px, base + 138, "#8295a5")
                body += line(px, base + 145, px, base + 173, RED, arrow=True)
        body += text(48, top + 335, "悬链线：每米链长等重。" if i == 0 else "抛物线：每米水平桥面等重，暂忽略主缆自重。", 21)
    body += text(48, 882, "桥面 → 吊杆 → 主缆 → 塔与锚固体系", 25, BLUE)
    body += text(48, 928, "只画主跨，省略边跨和锚碇；竖向比例放大两倍。", 21)
    body += text(48, 974, "真实桥梁还须考虑缆重、非均匀活载与结构变形。", 21)
    write("bridge-loads.svg", 1020, "图 6｜桥面一挂上，数学模型就变了",
          "上下各为跨度200米弧垂20米的主跨。自由均匀缆为悬链线，忽略缆重而均匀水平加载的主缆为抛物线。两图不是同一根定长缆的施工前后模拟。", body)


def tension():
    body = panel(70, 375)
    body += text(48, 111, "跨度 200 米；每米缆重 10 牛；支点同高。", 23)
    for h, color, dash in [(2500, RED, False), (5000, BLUE, True), (10000, GOLD, False)]:
        a = h / W
        pts = [(360 + 2.5 * x, 185 + 5 * (sag(a) - ordinate(x, a)))
               for x in (-100 + 200 * k / 160 for k in range(161))]
        body += path(pts, color, 4, dash=dash)
    for x in [110, 610]:
        body += dot(x, 185, 7, INK)
    body += text(48, 380, "金：拉得更紧；蓝虚线：中间；红：垂得更深。", 22)
    body += text(48, 422, "支点固定；竖向比例放大两倍。", 21)
    body += panel(470, 335)
    body += text(48, 515, "水平张力 H        弧垂 f          支点总张力 T", 23)
    for i, h in enumerate([2500, 5000, 10000]):
        a, yy = h / W, 579 + i * 70
        body += text(65, yy, f"{h/1000:.1f} 千牛", 23)
        body += text(345, yy, f"{sag(a):.3f} 米", 23, BLUE, "middle")
        body += text(585, yy, f"{h*math.cosh(100/a)/1000:.3f} 千牛", 23, RED, "middle")
    body += text(48, 775, "这些是不同缆长的平衡状态，不是定长绳随意调力。", 21)
    body += text(48, 858, "f ≈ wD²/(8H)：跨度加倍，弧垂约变成四倍。", 24)
    body += text(48, 910, "要几乎笔直，需要极大的张力；不是越紧越好。", 23)
    write("sag-and-tension.svg", 950, "图 7｜为什么不能把电线拉成直线？",
          "三条自重均匀缆分别具有水平张力2.5、5、10千牛，跨度相同而长度不同。弧垂与支点总张力由悬链线精确公式计算，竖直方向放大两倍。", body)


def thermal_points(delta):
    a, _, _, _ = thermal(delta)
    return [(360 + 2.5 * x, 175 + 10 * (sag(a) - ordinate(x, a)))
            for x in (-100 + 200 * i / 120 for i in range(121))]


def path_data(pts):
    return "M" + " L".join(f"{x:.6f},{y:.6f}" for x, y in pts)


def thermal_zoom_points(delta):
    a, _, _, _ = thermal(delta)
    return [(360 + 8 * x, 630 + 110 * (sag(a) - 10 - ordinate(x, a)))
            for x in (-15 + 30 * i / 120 for i in range(121))]


def heating():
    body = panel(70, 470)
    body += text(48, 112, "同一段教学导线：升温伸长，重新找到平衡。", 23)
    for delta, color, dash in [(0, BLUE, True), (30, GOLD, True), (60, RED, False)]:
        body += path(thermal_points(delta), color, 3, dash=dash)
    final = path_data(thermal_points(60))
    body += f'<path class="heat-cable" data-heat="cable" d="{final}" fill="none" stroke="{RED}" stroke-width="5"/>'
    vertical_scale = 10
    ground = 175 + 24 * vertical_scale
    for px in [110, 610]:
        body += dot(px, 175, 7, INK) + line(px, 175, px, ground, INK)
    body += line(70, ground, 650, ground, INK)
    body += text(650, ground - 8, "地面", 21, INK, "end")
    body += text(48, 445, "蓝虚：初态；金虚：升温 30℃；红：升温 60℃。", 22)
    body += text(48, 480, "支点高 24 米；横纵不等比例，竖向放大 4 倍。", 21)
    body += text(48, 515, "动画 6 秒扫过平衡状态，不是实际升温或振动计时。", 20)
    body += panel(560, 325)
    body += text(48, 599, "最低点局部放大：不是第二段导线", 24)
    for delta, color, dash in [(0, BLUE, True), (30, GOLD, True), (60, RED, False)]:
        body += path(thermal_zoom_points(delta), color, 3, dash=dash)
    zoom_final = path_data(thermal_zoom_points(60))
    body += (f'<path class="heat-zoom" data-heat="zoom" d="{zoom_final}" '
             f'fill="none" stroke="{RED}" stroke-width="5"/>')
    initial_y = thermal_zoom_points(0)[60][1]
    final_y = thermal_zoom_points(60)[60][1]
    body += line(490, initial_y, 490, final_y, INK, arrow=True)
    body += text(525, 675, "下降", 21)
    body += text(525, 712, f"{sag(thermal(60)[0])-sag(A0):.3f} 米", 21)
    body += text(48, 788, "蓝虚：10.033 米弧垂；红实：10.908 米弧垂。", 22)
    body += text(48, 828, "只取中间 30 米；横纵独立缩放，竖向放大 13.75 倍。", 20)
    body += text(48, 866, "长度只增加 0.242 米；完整数值表见正文。", 21, BLUE)
    css = ""
    for name, geometry in [("cable", thermal_points), ("zoom", thermal_zoom_points)]:
        shape = path_data(geometry(60))
        css += f'.heat-{name}{{d:path("{shape}");animation:heat-{name} 6s linear 1s 1 both}}'
        frames = []
        for i in range(121):
            delta = i / 2
            frames.append(f'{100*i/120:.9f}%{{d:path("{path_data(geometry(delta))}")}}')
            if i < 120:
                exact, start, end = geometry(delta + .25), geometry(delta), geometry(delta + .5)
                assert max(math.hypot(p[0] - (s[0] + n[0]) / 2, p[1] - (s[1] + n[1]) / 2)
                           for p, s, n in zip(exact, start, end)) < .01
        css += f"@keyframes heat-{name}" + "{" + "".join(frames) + "}"
    css += "@media(prefers-reduced-motion:reduce){[data-heat]{animation:none}}"
    body += text(48, 923, "α＝0.000020/℃；忽略弹性、蠕变、风和覆冰。", 21)
    body += text(48, 965, "净空只是本图数值，不是任何电压的安全距离标准。", 22, RED)
    write("temperature-and-clearance.svg", 995, "图 8｜多出 24 厘米，最低点降了约 87 厘米",
          "200米跨度、初始a为500米的教学导线，按有效热膨胀系数每摄氏度0.000020增加长度。保持总重量不变并数值求解平衡状态。固定支点高24米，全图竖向放大4倍；局部图只取中间30米，竖向放大13.75倍。两图同步显示同一模型，不模拟弹性或真实升温时间。", body, css)


def inverted():
    body = ""
    for i in range(2):
        top, center = 70 + 355 * i, 285 if i == 0 else 530
        body += panel(top, 330)
        body += text(48, top + 36, "① 柔软链：靠拉力维持形状" if i == 0 else "② 翻转的理想拱：靠压力传递载荷", 24)
        fn = (lambda x: ordinate(x, 1)) if i == 0 else (lambda x: -ordinate(x, 1))
        pts = points(fn, -1.5, 1.5, 360, center, 130, 55)
        body += path(pts, BLUE if i == 0 else GOLD, 8)
        for x in [-1.5, 1.5]:
            px, py = 360 + 130 * x, center - 55 * fn(x)
            body += dot(px, py, 7, INK)
        for x in [-1, 0, 1]:
            px, py = 360 + 130 * x, center - 55 * fn(x)
            body += line(px, py + 6, px, py + 44, RED, arrow=True)
        body += text(48, top + 302, "红箭头仅提示向下重量；不是完整受力图。", 21)
    body += text(48, 830, "倒过来的不只是外形，还把内力从拉变成了压。", 24)
    body += text(48, 880, "拱厚、载荷、侧推力与地基都要另算，不能照图盖桥。", 21)
    body += text(48, 930, "并非所有弧形建筑都是同一个 a cosh(x/a)。", 23, BLUE)
    write("chain-to-arch.svg", 975, "图 9｜链条翻过来，为何让人想到拱？",
          "均匀线重柔链的悬链形状与其竖向镜像，分别提示受拉的索与理想受压拱的对应。线条只是力路示意，不给出有限厚度砖拱尺寸或工程安全性。", body)


def validate():
    for a in [1.0, 10.0, 250.0, 500.0, 1000.0]:
        span = 4.0 if a <= 10 else SPAN
        for k in range(101):
            x = span * (k / 100 - .5)
            slope = math.sinh(x / a)
            second = math.cosh(x / a) / a
            assert abs(second - math.sqrt(1 + slope * slope) / a) < 1e-12
            h, v = W * a, W * a * slope
            assert abs(math.hypot(h, v) - W * a * math.cosh(x / a)) < 1e-9
        n = 2048
        step = span / n
        numerical = sum(step / 6 * (math.cosh((-span / 2 + i * step) / a)
                        + 4 * math.cosh((-span / 2 + (i + .5) * step) / a)
                        + math.cosh((-span / 2 + (i + 1) * step) / a)) for i in range(n))
        assert abs(numerical - length(a, span)) < 1e-10
        found = parameter_for_length(length(a, span), span)
        assert abs(found / a - 1) < 1e-11
    for delta in range(61):
        a, total, w, h = thermal(delta)
        assert abs(length(a) - total) < 1e-10
        assert abs(w * total - W * L0) < 1e-9
        assert abs(h / w - a) < 1e-10
        assert all(abs(pts[1] - 175) < 1e-8 for pts in [thermal_points(delta)[0], thermal_points(delta)[-1]])
    assert sag(thermal(60)[0]) > sag(thermal(30)[0]) > sag(A0)
    assert thermal(60)[3] < thermal(30)[3] < W * A0
    assert sag(500) > SPAN ** 2 / (8 * 500)
    assert abs(sag(1000) / (SPAN ** 2 / (8 * 1000)) - 1) < .001
    assert abs((length(1000) - SPAN) / (8 * sag(1000)**2 / (3 * SPAN)) - 1) < .002
    assert abs(math.hypot(10, 10 * math.sinh(1.2)) - 18.107) < .0005
    assert abs((sag(1, 4) / 4 - ordinate(1, 1)) - .1475) < .00005
    for s in [.5, 1, 1.5]:
        x = math.asinh(s)
        assert abs(math.sinh(x) - s) < 1e-12
        assert abs(math.sqrt(1+s*s) - math.cosh(x)) < 1e-12
    assert abs((thermal_zoom_points(60)[60][1] - thermal_zoom_points(0)[60][1]) / 110
               - (sag(thermal(60)[0])-sag(A0))) < 1e-12
    print("Sag/tension:", [(h, round(sag(h/W), 6)) for h in [2500, 5000, 10000]])
    print("Thermal states:", [(d, tuple(round(v, 6) for v in thermal(d)), round(sag(thermal(d)[0]), 6)) for d in [0, 30, 60]])


if __name__ == "__main__":
    validate()
    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [comparison, distribution, forces, accumulating, calculus, bridge, tension, heating, inverted]:
        draw()
    for filename in OUT.glob("*.svg"):
        root = ET.parse(filename).getroot()
        assert root.find("{http://www.w3.org/2000/svg}title") is not None
        assert root.find("{http://www.w3.org/2000/svg}desc") is not None
        assert root.attrib["viewBox"] == f'0 0 {root.attrib["width"]} {root.attrib["height"]}'
    print("Nine SVGs: equilibrium, equal arc segments, force scaling, thermal zoom and conserved mass passed.")
