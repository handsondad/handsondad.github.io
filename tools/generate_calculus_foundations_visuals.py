"""Draw and check eight original diagrams for the calculus introduction."""

import math
from fractions import Fraction
from pathlib import Path

from generate_kepler_newton_visuals import (
    BLUE, GOLD, INK, RED, dot, line, panel, path, save, text,
)


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "calculus-foundations"
G = 9.8
R = 8.314


def write(name, height, title, description, body, css=""):
    save(name, height, title, description, body, css, output_directory=OUT)


def polygon(points, color, opacity=.16):
    coordinates = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
    return f'<polygon points="{coordinates}" fill="{color}" fill-opacity="{opacity}"/>'


def axes(px, py, xs, ys, xlabel, ylabel):
    body = line(px(xs[0]), py(0), px(xs[1]), py(0), arrow=True)
    body += line(px(0), py(ys[0]), px(0), py(ys[1]), arrow=True)
    body += text(px(xs[1]) - 15, py(0) + 40, xlabel, 22, anchor="end")
    body += text(px(0) + 14, py(ys[1]) + 5, ylabel, 22)
    return body


def secant_limit():
    px = lambda x: 100 + 245 * x
    py = lambda y: 560 - 90 * y
    body = text(36, 52, "一段的平均变化，怎样变成一点的变化？", 28)
    body += text(36, 94, "固定 P = (1, 1)；另一个点 Q 沿 y = x² 接近 P", 23)
    body += '<defs><clipPath id="plot"><rect x="100" y="145" width="520" height="415"/></clipPath></defs>'
    body += axes(px, py, (0, 2.28), (0, 4.6), "x", "y")
    body += text(px(1), 600, "1", 22, anchor="middle")
    body += text(px(2), 600, "2", 22, anchor="middle")
    body += text(71, py(1) + 8, "1", 22)
    body += text(71, py(4) + 8, "4", 22)
    body += path([(px(2.05 * i / 300), py((2.05 * i / 300) ** 2))
                  for i in range(301)], BLUE, 4)
    body += text(407, 169, "蓝色曲线：y = x²", 23, BLUE)
    states = [(1., "h = 1；割线斜率 3"),
              (.5, "h = 0.5；割线斜率 2.5"),
              (.1, "h = 0.1；割线斜率 2.1"),
              (0., "极限切线：斜率 2")]
    for i, (h, label) in enumerate(states):
        body += f'<g class="step step-{i}" data-step="{i}" data-h="{h:g}">'
        slope = 2 + h
        body += '<g clip-path="url(#plot)">'
        body += path([(px(x), py(1 + slope * (x - 1))) for x in [0, 2.1]], GOLD, 3)
        body += '</g>'
        if h:
            q = (1 + h, (1 + h) ** 2)
            assert math.isclose((q[1] - 1) / h, slope, abs_tol=1e-12)
            body += line(px(1), py(1), px(q[0]), py(1), INK, True)
            body += line(px(q[0]), py(1), px(q[0]), py(q[1]), INK, True)
            body += f'<circle data-role="q" cx="{px(q[0]):.3f}" cy="{py(q[1]):.3f}" r="8" fill="{RED}"/>'
        body += text(36, 660, label, 27, GOLD)
        body += '</g>'
    body += dot(px(1), py(1), 8, BLUE)
    body += text(px(1) - 39, py(1) - 15, "P", 24, BLUE)
    body += panel(697, 179)
    body += text(46, 740, "静态路线：h 越小，割线斜率 2 + h 越接近 2", 24)
    body += text(46, 788, "h = 1 → 0.5 → 0.1：斜率 3 → 2.5 → 2.1", 23)
    body += text(46, 835, "过程只用非零 h；切线是极限，不是把 0 除以 0。", 22)
    body += text(36, 923, "8 秒分步演示，播放一次；减少动态效果时直接显示切线。", 22)
    css = ".step{opacity:0}.step-3{opacity:1}"
    css += (
        "@keyframes show0{0%,24.999%{opacity:1}25%,100%{opacity:0}}"
        "@keyframes show1{0%,24.999%{opacity:0}25%,49.999%{opacity:1}50%,100%{opacity:0}}"
        "@keyframes show2{0%,49.999%{opacity:0}50%,74.999%{opacity:1}75%,100%{opacity:0}}"
        "@keyframes show3{0%,74.999%{opacity:0}75%,100%{opacity:1}}"
    )
    css += "@media(prefers-reduced-motion:no-preference){"
    for i in range(4):
        css += f".step-{i}{{animation:show{i} 8s steps(1,end) 1s 1 both}}"
    css += "}"
    css += "@media(prefers-reduced-motion:reduce){.step{animation:none;opacity:0}.step-3{opacity:1}}"
    write("secant-limit.svg", 968, "割线斜率的极限给出切线斜率",
          "平方函数在1处的差商为2加h。分步显示h为1、0.5、0.1的精确割线，最后停在斜率2的切线；静态保留全部数值。", body, css)


def corner_counterexample():
    body = text(36, 52, "连续，只是没有断开；不保证能求导", 29)
    body += text(36, 94, "反例 y = |x|：在 x = 0 接得上，却有一个尖角", 23)
    px = lambda x: 360 + 150 * x
    py = lambda y: 445 - 140 * y
    body += axes(px, py, (-1.65, 1.65), (0, 2), "x", "y")
    body += path([(px(-1.6), py(1.6)), (px(0), py(0)), (px(1.6), py(1.6))], BLUE, 4)
    body += dot(px(0), py(0), 7, RED)
    body += text(112, 398, "左边斜率 -1", 24)
    body += text(445, 398, "右边斜率 +1", 24)
    body += panel(521, 186)
    body += text(46, 563, "h < 0：|h| / h = -1", 25)
    body += text(46, 610, "h > 0：|h| / h = +1", 25)
    body += text(46, 661, "两边不趋向同一个数，所以 0 处的导数不存在。", 23, RED)
    body += text(36, 759, "另一个提醒：y = x² 在 0 处的导数存在，且等于 0。", 22)
    body += text(36, 805, "“导数必须非零”与“连续就可导”，都不是规则。", 23)
    for h in [-1, -.1, -.001, .001, .1, 1]:
        assert abs(h) / h == (1 if h > 0 else -1)
    write("corner-counterexample.svg", 850, "绝对值函数的尖角与不可导",
          "绝对值函数在0连续，但左侧差商恒为负1、右侧恒为正1，导数不存在。平方函数在0的导数则存在且等于0。", body)


def motion_graphs():
    body = text(36, 52, "同一场下落，三张图回答三个问题", 29)
    body += text(36, 94, "向下为正；从静止开始；g = 9.8 米/秒²；忽略阻力", 22)
    cases = [
        ("① 位置 s", lambda t: .5 * G * t * t, "s = 4.9 t²", "第 2 秒：19.6 米"),
        ("② 速度 v", lambda t: G * t, "v = 9.8 t", "第 2 秒：19.6 米/秒"),
        ("③ 加速度 a", lambda t: G, "a = 9.8", "每秒改变 9.8 米/秒"),
    ]
    for i, (title, f, formula, value) in enumerate(cases):
        y = 132 + 308 * i
        body += panel(y, 282)
        body += text(46, y + 39, title, 26)
        px = lambda t: 79 + 157 * t
        py = lambda v: y + 232 - 8 * v
        body += line(px(0), py(0), px(2.15), py(0), arrow=True)
        body += line(px(0), py(0), px(0), py(22), arrow=True)
        body += path([(px(2 * j / 200), py(f(2 * j / 200))) for j in range(201)], BLUE, 4)
        body += text(px(0), y + 265, "0", 21, anchor="middle")
        body += text(px(1), y + 265, "1", 21, anchor="middle")
        body += text(px(2), y + 265, "2 秒", 21, anchor="middle")
        body += dot(px(2), py(f(2)), 6, GOLD)
        body += text(453, y + 107, formula, 27, BLUE)
        body += text(453, y + 158, value, 21)
        if i < 2:
            body += text(453, y + 210, "对时间求导 ↓", 23, GOLD)
    body += text(36, 1113, "纵轴依次为米、米/秒、米/秒²，不能当成同一种量。", 22)
    body += text(36, 1158, "s 是向下位移，不是离地高度；如果高度为 H，剩下 H-s。", 22)
    assert math.isclose(.5 * G * 2 ** 2, 19.6)
    for t in [.1, .5, 1, 2]:
        h = 1e-4
        derivative = (.5 * G * (t + h) ** 2 - .5 * G * (t - h) ** 2) / (2 * h)
        assert math.isclose(derivative, G * t, rel_tol=1e-10)
    write("motion-three-graphs.svg", 1201, "自由落体的位置、速度和加速度图",
          "取向下为正，重力加速度9.8米每二次方秒，从静止下落。位置4.9t平方、速度9.8t、加速度9.8，横轴均为0到2秒。", body)


def rectangle_sums():
    body = text(36, 52, "曲线下的面积：用两本账夹住答案", 28)
    body += text(36, 94, "y = x²，区间 0 到 1；同宽矩形，左端低估、右端高估", 22)
    for row, n in enumerate([4, 8, 16]):
        y = 132 + 265 * row
        body += panel(y, 238)
        body += text(46, y + 35, f"①②③"[row] + f" N = {n}", 25)
        sums = []
        for side, color in [("left", BLUE), ("right", GOLD)]:
            x0 = 62 if side == "left" else 397
            px = lambda x: x0 + 235 * x
            py = lambda v: y + 165 - 101 * v
            total = Fraction(0)
            for i in range(n):
                x = Fraction(i if side == "left" else i + 1, n)
                height = x * x
                total += height / n
                body += (
                    f'<rect x="{px(i/n):.3f}" y="{py(float(height)):.3f}" '
                    f'width="{235/n:.6f}" height="{101*float(height):.6f}" '
                    f'fill="{color}" fill-opacity=".18" stroke="{color}" stroke-width="1"/>'
                )
            body += line(px(0), py(0), px(1.08), py(0))
            body += line(px(0), py(0), px(0), py(1.05))
            body += path([(px(j / 200), py((j / 200) ** 2)) for j in range(201)], INK)
            body += text(x0, y + 211, f"{'左端' if side == 'left' else '右端'}和 {float(total):.6f}", 23, color)
            sums.append(total)
        low, high = sums
        assert low < Fraction(1, 3) < high
        assert high - low == Fraction(1, n)
        assert low == Fraction(1, 3) - Fraction(1, 2*n) + Fraction(1, 6*n*n)
        assert high == Fraction(1, 3) + Fraction(1, 2*n) + Fraction(1, 6*n*n)
    body += text(36, 985, "两本账之差 = 1 / N；N 增大时，夹缝可以任意小。", 23)
    body += text(36, 1032, "共同极限是 1/3；不是把矩形顶端的空隙直接当作 0。", 22)
    body += text(36, 1077, "每幅小图都用同一坐标尺度；蓝、金同时配“左、右”标记。", 21)
    write("rectangle-sums.svg", 1120, "平方曲线面积的左右端点黎曼和",
          "0到1的平方函数，使用4、8、16个等宽矩形。左右端点和分别低估和高估面积，差为1除N，极限同为三分之一。", body)


def fundamental_bridge():
    body = text(36, 52, "为什么“累积”的导数，正好是原来的高度？", 28)
    body += text(36, 94, "A(x) = 从 0 累积到 x 的曲线下方面积；这里 f(u) = u²", 22)
    px = lambda u: 104 + 470 * u
    py = lambda f: 489 - 275 * f
    x, h = .6, .2
    for lo, hi, color in [(0, x, BLUE), (x, x+h, GOLD)]:
        points = [(px(lo), py(0))]
        points += [(px(lo + (hi-lo) * i/150), py((lo + (hi-lo) * i/150) ** 2))
                   for i in range(151)]
        points += [(px(hi), py(0))]
        body += polygon(points, color)
    body += axes(px, py, (0, 1.1), (0, 1.15), "u", "f(u)")
    body += path([(px(i/200), py((i/200) ** 2)) for i in range(201)], INK, 4)
    body += line(px(x), py(0), px(x), py(x*x), BLUE, True)
    body += line(px(x+h), py(0), px(x+h), py((x+h)**2), GOLD, True)
    body += text(px(x), 534, "x", 24, BLUE, "middle")
    body += text(px(x+h), 534, "x+h", 24, GOLD, "middle")
    body += text(137, 388, "原有面积", 24, BLUE)
    body += text(409, 187, "新添的窄条", 24, GOLD)
    body += line(480, 208, 437, 447, GOLD, True, True)
    body += panel(577, 231)
    body += text(46, 620, "① 只多走 h，面积只多出这条窄条 ΔA", 25)
    body += text(46, 670, "② ΔA / h 是窄条的平均高度，不是总面积", 23)
    body += text(46, 719, "③ h → 0 且 f 连续：平均高度 → f(x)", 24)
    body += text(46, 769, "所以 A′(x) = f(x)：这是连接微分与积分的桥。", 23, BLUE)
    body += text(36, 862, "图中 x = 0.6；h = 0.2，故窄条还明显有弯曲。", 23)
    values = []
    for increment in [.2, .05, .01]:
        quotient = ((x+increment)**3-x**3)/(3*increment)
        assert math.isclose(quotient, x*x+x*increment+increment**2/3, rel_tol=1e-12)
        values.append(quotient)
    body += text(36, 909, "平均高度：0.49333 → 0.39083 → 0.36603 → 0.36", 22)
    body += text(36, 957, "前三项对应 h = 0.2、0.05、0.01；0.36 是极限。", 22)
    assert all(values[i] > values[i+1] > x*x for i in range(2))
    write("fundamental-bridge.svg", 1000, "微积分基本定理的窄条解释",
          "累积面积A增加一条宽h的窄条。面积增量除以h是平均高度，连续性使其趋于曲线在x的高度。平方函数在x为0.6时极限高度为0.36。", body)


def binomial_coefficient(exponent, k):
    value = Fraction(1)
    for i in range(k):
        value *= (exponent-i)/(i+1)
    return value


def binomial_series():
    body = text(36, 52, "二项式：从有限多项式，走到无穷级数", 29)
    body += text(36, 94, "同一串系数规则，不同的指数，却有不同的使用范围", 23)
    body += panel(133, 222)
    body += text(46, 176, "① 指数 3：会结束", 27)
    body += text(46, 230, "(1+u)³ = 1 + 3u + 3u² + u³", 27, BLUE)
    body += text(46, 281, "再下一项含有 3-3 = 0，后面的系数都变成 0。", 23)
    body += text(46, 325, "这是有限展开，对任意实数 u 都成立。", 23)
    body += panel(390, 250)
    body += text(46, 433, "② 指数 1/2：不会这样结束", 26)
    body += text(46, 486, "√(1+u) = 1 + u/2 - u²/8 + u³/16", 25, GOLD)
    body += text(219, 529, "- 5u⁴/128 + …", 25, GOLD)
    body += text(46, 575, "这里采用 |u| < 1；不能把无穷多项当成有限公式。", 22)
    body += text(46, 617, "写出一串项，还要证明收敛，并且和等于原函数。", 22)
    body += panel(678, 271)
    u = Fraction(1, 5)
    target = math.sqrt(1+float(u))
    for i, degree in enumerate([1, 2, 4]):
        estimate = sum((binomial_coefficient(Fraction(1, 2), k)*u**k
                        for k in range(degree+1)), Fraction(0))
        body += text(46, 721+57*i, f"保留到 u{'¹²⁴'[i]}：{float(estimate):.7f}", 25)
        assert abs(float(estimate)-target) < [.005, .00045, .000008][i]
    body += text(46, 904, f"本例 u = 0.2；√1.2 ≈ {target:.7f}", 24, BLUE)
    body += text(36, 1005, "这些是计算出的近似，不是把省略号当作“随便省略”。", 22)
    assert binomial_coefficient(Fraction(3), 4) == 0
    assert [binomial_coefficient(Fraction(1, 2), k) for k in range(5)] == [
        Fraction(1), Fraction(1, 2), Fraction(-1, 8), Fraction(1, 16), Fraction(-5, 128)
    ]
    write("binomial-series.svg", 1050, "有限二项式展开与平方根的二项式级数",
          "指数3的展开在u三次项结束。指数二分之一的展开不会结束，在绝对值u小于1时可用，取u为0.2比较一次、二次、四次近似与平方根1.2。", body)


def gas_partials():
    body = text(36, 52, "偏导数：只动一个旋钮，锁住另一个", 29)
    body += text(36, 94, "1 摩尔理想气体；V = nRT/P；T 用开尔文，P 用绝对压强", 22)
    cases = [
        (200, 400, lambda t: R*t/100, "① 固定 P = 100 千帕", "温度 T / K", [200, 300, 400]),
        (50, 150, lambda p: R*300/p, "② 固定 T = 300 K", "压强 P / 千帕", [50, 100, 150]),
    ]
    for row, (lo, hi, f, label, xlabel, ticks) in enumerate(cases):
        y = 133 + row * 362
        body += panel(y, 333)
        body += text(46, y+40, label, 26)
        px = lambda x: 111+(x-lo)*2.4 if row == 0 else 111+(x-lo)*4.8
        py = lambda v: y+257-3.6*v
        body += line(px(lo), py(0), px(hi)+25, py(0), arrow=True)
        body += line(px(lo), py(0), px(lo), py(52), arrow=True)
        body += text(124, py(52)+4, "体积 V / 升", 22)
        body += path([(px(lo+(hi-lo)*i/250), py(f(lo+(hi-lo)*i/250))) for i in range(251)], BLUE, 4)
        for x in ticks:
            body += dot(px(x), py(f(x)), 6, GOLD)
            body += text(px(x), y+288, str(x), 22, anchor="middle")
        body += text(620, y+322, xlabel, 22, anchor="end")
    volume = R*300/100
    d_temperature = R/100
    d_pressure = -R*300/100**2
    body += panel(891, 190)
    body += text(46, 932, f"共同状态：300 K、100 千帕 → 约 {volume:.2f} 升", 24)
    body += text(46, 982, f"只升温：局部每增 1 K，体积约增 {d_temperature:.5f} 升", 23)
    body += text(46, 1033, f"只增压：局部每增 1 千帕，体积约减 {-d_pressure:.5f} 升", 23)
    body += text(36, 1131, "“局部每增”是导数的线性近似；不是任意大变化的精确账。", 22)
    for h in [.1, .01]:
        finite = (R*300/(100+h)-R*300/(100-h))/(2*h)
        assert math.isclose(finite, d_pressure, rel_tol=2e-6)
    assert math.isclose(volume, 24.942)
    write("partial-gas.svg", 1176, "理想气体的两个偏导数切片",
          "固定1摩尔气体，分别锁定100千帕压强改变温度，以及锁定300开尔文温度改变压强。共同状态体积24.942升，两种局部变化率不同。", body)


def heat_temperature(x, tau):
    return 20+60*x+20*math.exp(-math.pi**2*tau)*math.sin(math.pi*x)


def heat_boundaries():
    body = text(36, 52, "方程管怎么变，条件管“具体是哪一次”", 29)
    body += text(36, 94, "均匀细杆，侧面绝热，无内部热源；左端 20°C，右端 80°C", 22)
    body += panel(130, 162)
    body += text(46, 173, "边界条件：两端的温度一直保持不变", 25)
    body += '<rect x="100" y="204" width="500" height="28" rx="8" fill="#d1e2e9"/>'
    body += dot(100, 218, 12, BLUE)
    body += dot(600, 218, 12, RED)
    body += text(100, 271, "20°C", 23, BLUE, "middle")
    body += text(600, 271, "80°C", 23, RED, "middle")
    px = lambda x: 109+494*x
    py = lambda temperature: 732-4.05*temperature
    body += line(px(0), py(0), px(1.09), py(0), arrow=True)
    body += line(px(0), py(0), px(0), py(91), arrow=True)
    body += text(124, py(91)+5, "温度 / °C", 23)
    body += text(px(0), 773, "0", 22, anchor="middle")
    body += text(px(.5), 773, "L/2", 22, anchor="middle")
    body += text(px(1), 773, "L", 22, anchor="middle")
    body += text(690, 773, "位置", 22, anchor="end")
    for temperature in [20, 50, 80]:
        body += text(87, py(temperature)+7, str(temperature), 21, anchor="end")
    for tau, color, dash, label, baseline in [
        (0, RED, False, "初始：中间比稳态多一个鼓包", 826),
        (.05, GOLD, True, "稍后：τ = 0.05", 870),
        (.2, BLUE, False, "更后：τ = 0.2", 914),
        (math.inf, INK, True, "最终稳态：20 + 60x/L", 958),
    ]:
        points = [(px(i/300), py(heat_temperature(i/300, tau))) for i in range(301)]
        body += path(points, color, 3, dash)
        body += line(46, baseline-8, 84, baseline-8, color, dash)
        body += text(105, baseline, label, 23, color)
        assert math.isclose(heat_temperature(0, tau), 20, abs_tol=1e-12)
        assert math.isclose(heat_temperature(1, tau), 80, abs_tol=1e-12)
    body += panel(997, 177)
    body += text(46, 1038, "τ = αt/L²：时间已缩放，不是直接标成秒的实测录像", 22)
    body += text(46, 1086, "初始条件：整根杆在 t = 0 的温度分布", 24)
    body += text(46, 1135, "稳态不再随时间变，但仍有热量从右端流向左端。", 23)
    for x in [.1, .3, .5, .8]:
        for tau in [0, .05, .2]:
            common = -20*math.pi**2*math.exp(-math.pi**2*tau)*math.sin(math.pi*x)
            step = 1e-4
            u_tau = (heat_temperature(x, tau+step)-heat_temperature(x, tau-step))/(2*step)
            u_xx = (heat_temperature(x+step, tau)-2*heat_temperature(x, tau)+
                    heat_temperature(x-step, tau))/step**2
            assert math.isclose(u_tau, common, rel_tol=2e-7)
            assert math.isclose(u_xx, common, rel_tol=2e-7)
    assert math.isclose(heat_temperature(.5, 0), 70)
    assert math.isclose(heat_temperature(.5, math.inf), 50)
    write("heat-boundaries.svg", 1220, "热传导的初始条件、边界条件与稳态",
          "侧面绝热的均匀杆两端固定20与80摄氏度，初态在线性稳态上增加20摄氏度正弦鼓包。按热方程解析解画缩放时间0、0.05、0.2及最终稳态，并核对方程与端点。", body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    secant_limit()
    corner_counterexample()
    motion_graphs()
    rectangle_sums()
    fundamental_bridge()
    binomial_series()
    gas_partials()
    heat_boundaries()
    print("Generated eight checked calculus diagrams.")


if __name__ == "__main__":
    main()
