"""Generate original analytical-mechanics diagrams and model-timed animations."""

import math
from pathlib import Path

from generate_kepler_newton_visuals import BLUE, GOLD, INK, RED, dot, line, panel, path, save, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "analytical-mechanics"
G, LENGTH, MASS = 9.81, 1.0, 1.0
AMPLITUDE = math.pi / 6
FRAMES = 240


def write(name, height, title, description, body, css=""):
    save(name, height, title, description, body, css, output_directory=OUT)


def heading(number, title):
    return text(36, 48, f"{number} {title}", 29)


def rows(x, y, values, size=23, step=38, color=INK):
    return "".join(text(x, y + i * step, value, size, color) for i, value in enumerate(values))


def animation(name, values, duration, prop="transform"):
    frames = "".join(f"{100*i/(len(values)-1):.6f}%{{{prop}:{v}}}" for i, v in enumerate(values))
    return (
        f".{name}{{{prop}:{values[-1]};transform-origin:0 0;"
        f"animation:{name} {duration:.9f}s linear 1 both}}"
        f"@keyframes {name}{{{frames}}}"
        f"@media(prefers-reduced-motion:reduce){{.{name}{{animation:none}}}}"
    )


def pendulum_period():
    k2 = math.sin(AMPLITUDE / 2) ** 2
    n = 2048
    step = math.pi / (2 * n)
    values = [1 / math.sqrt(1 - k2 * math.sin(i * step) ** 2) for i in range(n + 1)]
    integral = step * (values[0] + values[-1] + 4 * sum(values[1:-1:2]) + 2 * sum(values[2:-1:2])) / 3
    return 4 * math.sqrt(LENGTH / G) * integral


PERIOD = pendulum_period()
ENERGY = MASS * G * LENGTH * (1 - math.cos(AMPLITUDE))


def pendulum_samples(count):
    theta, omega = AMPLITUDE, 0.0
    samples = [(theta, omega)]
    for i in range(1, count + 1):
        interval = PERIOD / count
        steps = math.ceil(interval / 0.0002)
        h = interval / steps
        for _ in range(steps):
            def acc(angle):
                return -G / LENGTH * math.sin(angle)

            k1 = omega, acc(theta)
            k2 = omega + h * k1[1] / 2, acc(theta + h * k1[0] / 2)
            k3 = omega + h * k2[1] / 2, acc(theta + h * k2[0] / 2)
            k4 = omega + h * k3[1], acc(theta + h * k3[0])
            theta += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
            omega += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        samples.append((theta, omega))
    for theta, omega in samples:
        energy = MASS * LENGTH ** 2 * omega ** 2 / 2 + MASS * G * LENGTH * (1 - math.cos(theta))
        assert abs(energy - ENERGY) < 1e-10
    assert abs(samples[-1][0] - AMPLITUDE) < 1e-10
    assert abs(samples[-1][1]) < 1e-9
    return samples


def history():
    entries = [
        ("1687", "牛顿", "《原理》：运动定律与万有引力", "给出物理规律；书中主要用几何论证"),
        ("1736", "欧拉", "《力学》：系统使用分析方法", "把质点动力学翻译成微分方程"),
        ("1743", "达朗贝尔", "《动力学论》：达朗贝尔原理", "在理想约束下，借虚功组织运动方程"),
        ("1788", "拉格朗日", "《分析力学》：统一的坐标方法", "用广义坐标和统一运算处理复杂系统"),
        ("1834—1835", "哈密顿", "两篇动力学论文", "从光学走向动力学，发展新的状态描述"),
        ("1918", "诺特", "连续对称性与守恒定理", "解释为什么某些量会在运动中不变"),
    ]
    body = heading("①", "不是推翻牛顿，而是重组问题")
    for i, (year, person, book, task) in enumerate(entries):
        y = 76 + 160 * i
        body += panel(y, 144) + text(48, y + 36, year, 25, BLUE)
        body += text(300, y + 36, person, 25)
        body += rows(48, y + 77, [book, task], 23, 36)
    body += rows(36, 1080, ["这里只选六个路标，不是完整的发明人名单。", "伯努利家族、莫佩尔蒂等人也参与了这段历史。"], 22)
    write("history.svg", 1140, "分析力学发展的六个历史路标",
          "列出六个有史料依据的出版或论文年份，区分各人的贡献，不表示一人独自发明整套理论。", body)


def constraints():
    theta = math.pi / 6
    pivot, length = (300, 172), 220
    p = (pivot[0] + length * math.sin(theta), pivot[1] + length * math.cos(theta))
    radial = (math.sin(theta), math.cos(theta))
    tangent = (math.cos(theta), -math.sin(theta))
    assert abs(sum(a * b for a, b in zip(radial, tangent))) < 1e-14
    assert abs(math.dist(pivot, p) - length) < 1e-12
    body = heading("②", "两个位置坐标，只有一个自由度")
    body += panel(76, 442) + text(48, 113, "固定支点、定长轻杆、平面运动；图取 θ = 30°", 23)
    body += line(82, pivot[1], 560, pivot[1], "#a3afb9", arrow=True)
    body += line(pivot[0], pivot[1], pivot[0], 134, "#a3afb9", arrow=True)
    body += text(570, 181, "x", 24) + text(271, 155, "y", 24)
    body += path([(pivot[0] + length * math.sin(t), pivot[1] + length * math.cos(t))
                  for t in [(-0.8 + 1.6 * i / 180) for i in range(181)]], "#bac8d3", 2, True)
    body += line(*pivot, *p, BLUE) + dot(*pivot, 8, INK) + dot(*p, 12, BLUE)
    body += path([(pivot[0] + 55 * math.sin(t), pivot[1] + 55 * math.cos(t))
                  for t in [theta * i / 40 for i in range(41)]], GOLD)
    body += text(307, 251, "θ", 26, GOLD) + text(384, 270, "长度 l", 22, BLUE)
    body += line(*p, p[0] - 72 * radial[0], p[1] - 72 * radial[1], GOLD, arrow=True)
    body += text(447, 315, "杆的约束力", 23, GOLD)
    body += line(*p, p[0] + 100 * tangent[0], p[1] + 100 * tangent[1], RED, arrow=True)
    body += text(480, 391, "虚位移 δr", 23, RED)
    body += line(*p, p[0], p[1] + 74, INK, arrow=True) + text(431, 464, "重力 mg", 23)
    body += panel(538, 234)
    body += rows(48, 579, ["① 只在同一时刻，想象一个满足杆长的微小位移。", "② 它沿圆弧切线，不是任意指向。", "③ 杆力沿半径，与这个虚位移垂直。", "因此杆力的虚功为零，但杆力并没有消失。"], 23, 47)
    body += panel(792, 168)
    body += rows(48, 834, ["位置：x = l sin θ，y = −l cos θ", "支点为原点；x 向右、y 向上为正。", "约束：x² + y² = l² → 只需 θ 来描述位置。"], 23, 45)
    write("constraints.svg", 990, "单摆广义坐标与理想约束力的零虚功",
          "单摆位置由一个角度决定，虚位移与杆方向正交。支点为原点，横坐标向右、纵坐标向上，位置公式与坐标图一致。", body)


def energy_motion():
    states = pendulum_samples(FRAMES)
    fine = pendulum_samples(2 * FRAMES)
    for i in range(FRAMES):
        assert abs((states[i][0] + states[i + 1][0]) / 2 - fine[2 * i + 1][0]) * 230 < 0.02
    duration = 3 * PERIOD
    rotations = [f"rotate({-math.degrees(theta):.8f}deg)" for theta, _ in states]
    kinetic = [MASS * LENGTH ** 2 * omega ** 2 / (2 * ENERGY) for _, omega in states]
    potential = [MASS * G * LENGTH * (1 - math.cos(theta)) / ENERGY for theta, _ in states]
    assert all(abs(k + u - 1) < 1e-10 for k, u in zip(kinetic, potential))
    css = animation("pendulum-rod", rotations, duration)
    css += animation("bar-kinetic", [f"scaleX({max(0, k):.9f})" for k in kinetic], duration)
    css += animation("bar-potential", [f"scaleX({u:.9f})" for u in potential], duration)
    body = heading("③", "球摆过去，能量怎样换班？")
    body += panel(76, 418) + text(48, 116, "1 千克、1 米、从 30° 静止释放，无摩擦", 23)
    body += text(48, 154, f"非线性单摆周期 {PERIOD:.3f} 秒；动画放慢 3 倍", 23)
    pivot = (360, 198)
    arc = [(pivot[0] + 230 * math.sin(-AMPLITUDE + 2 * AMPLITUDE * i / 120),
            pivot[1] + 230 * math.cos(-AMPLITUDE + 2 * AMPLITUDE * i / 120)) for i in range(121)]
    body += path(arc, "#a6b7c6", 3, True)
    for angle in [-AMPLITUDE, 0, AMPLITUDE]:
        body += dot(pivot[0] + 230 * math.sin(angle), pivot[1] + 230 * math.cos(angle), 7, GOLD)
    body += line(360, 198, 360, 428, "#c4cfd8", True)
    body += '<g transform="translate(360 198)"><g class="pendulum-rod" data-motion="rod">'
    body += line(0, 0, 0, 230, BLUE) + '<circle data-motion="bob" cx="0" cy="230" r="14" fill="' + BLUE + '"/></g></g>'
    body += dot(*pivot, 8, INK) + text(245, 473, "左端", 22, INK, "middle")
    body += text(360, 473, "最低点", 22, INK, "middle") + text(475, 473, "右端", 22, INK, "middle")
    body += panel(514, 242) + text(48, 553, "两根条使用相同尺度；零势能取最低点", 23)
    for y, label, name, color in [(580, "动能 K", "bar-kinetic", BLUE), (648, "势能 U", "bar-potential", GOLD)]:
        body += text(48, y + 25, label, 24, color)
        body += f'<g transform="translate(185 {y})"><rect width="430" height="30" rx="3" fill="#e4ebf0"/>'
        body += f'<rect class="{name}" data-energy="{name}" width="430" height="30" fill="{color}"/></g>'
    body += text(48, 729, f"K + U 恒为 {ENERGY:.3f} 焦耳；条长相加恒为 430。", 23)
    body += panel(776, 224)
    body += rows(48, 816, ["端点：速度 0，动能 0，势能最大。", f"最低点：速度 {math.sqrt(2*ENERGY/MASS):.3f} 米/秒，势能 0。", "一圈后回到释放点：位置和能量条都回到初态。", "虚线、三个静态位置与这张账表无需动画也能读。"], 23, 46)
    write("pendulum-energy.svg", 1030, "非线性单摆运动与动势能交换的一次动画",
          "用完整正弦单摆方程数值积分，按同一物理时间同步杆角和两种能量。三倍慢放一周期，最后回到释放点，减少动态效果保留完整轨迹和能量账。", body, css)


def degrees():
    body = heading("④", "把一个角度，升级成一组角度")
    body += panel(76, 342) + text(48, 116, "单摆：一个独立角度 θ", 25, BLUE)
    body += line(250, 162, 342, 335, BLUE) + dot(250, 162, 8, INK) + dot(342, 335, 14)
    body += line(250, 162, 250, 350, "#a8b7c4", True) + text(290, 219, "θ", 26, GOLD)
    body += text(425, 223, "自由度：1", 25)
    body += text(425, 264, "写 1 条二阶方程", 22)
    body += text(48, 388, "杆长固定，所以 x、y 不能独立选择。", 23)
    body += panel(438, 388) + text(48, 478, "双摆：两个独立角度 θ₁、θ₂", 25, BLUE)
    p0 = (265, 516)
    p1 = (p0[0] + 150 * math.sin(0.6), p0[1] + 150 * math.cos(0.6))
    p2 = (p1[0] + 120 * math.sin(-0.8), p1[1] + 120 * math.cos(-0.8))
    assert abs(math.dist(p0, p1) - 150) < 1e-12
    assert abs(math.dist(p1, p2) - 120) < 1e-12
    body += line(*p0, *p1, BLUE) + line(*p1, *p2, RED)
    body += dot(*p0, 8, INK) + dot(*p1, 13, BLUE) + dot(*p2, 13, RED)
    body += line(*p0, p0[0], p0[1] + 155, "#a8b7c4", True)
    body += line(*p1, p1[0], p1[1] + 145, "#a8b7c4", True)
    body += text(270, 611, "θ₁", 26, BLUE) + text(311, 714, "θ₂", 26, RED)
    body += text(450, 580, "自由度：2", 25)
    body += rows(450, 626, ["写 2 条耦合", "二阶方程"], 22)
    body += text(48, 794, "第二个球的速度，还包含第一个关节带来的运动。", 22)
    body += panel(846, 186)
    body += rows(48, 886, ["空间中无约束的刚体：3 个位置 + 3 个姿态参数。", "局部共 6 个自由度，不等于有 6 个互不影响的运动。", "机器人、刚体、振动系统：换坐标，统一列方程。"], 22, 48)
    write("degrees-of-freedom.svg", 1060, "单摆双摆与自由刚体的自由度",
          "按独立坐标计数：平面单摆一自由度、平面双摆二自由度、空间自由刚体局部六自由度。双摆角度均相对竖直，图为固定构型不是运动模拟。", body)


def action_difference(n, epsilon=0.2):
    time = 2 * math.pi
    return epsilon ** 2 / 4 * ((n * math.pi) ** 2 / time - time)


def action():
    assert math.isclose(action_difference(1), -0.0471238898038469, abs_tol=1e-14)
    assert math.isclose(action_difference(3), 0.0785398163397448, abs_tol=1e-14)
    for n in [1, 3]:
        count, time = 4096, 2 * math.pi
        f = lambda t: (0.2 * n / 2 * math.cos(n * t / 2)) ** 2 / 2 - (0.2 * math.sin(n * t / 2)) ** 2 / 2
        h = time / count
        integral = h * (f(0) + f(time) + 4 * sum(f(i*h) for i in range(1, count, 2)) +
                        2 * sum(f(i*h) for i in range(2, count, 2))) / 3
        assert abs(integral - action_difference(n)) < 1e-12
    body = heading("⑤", "驻定，不保证是最小")
    body += panel(76, 454)
    body += rows(48, 115, ["无摩擦弹簧：m = 1 千克，k = 1 牛顿/米", "固定 t = 0 与 t = 2π 秒的两端位置 x = 0"], 23)
    body += line(100, 473, 641, 473, INK, arrow=True) + text(624, 510, "t", 24)
    body += line(100, 420, 100, 194, INK, arrow=True) + text(69, 215, "x", 24)
    body += text(64, 326, "0", 22) + text(100, 510, "0", 22) + text(615, 445, "2π", 22)
    body += line(100, 320, 620, 320, BLUE)
    body += text(327, 449, "真实运动：x(t) ≡ 0", 23, BLUE)
    css = ""
    for n, name, color, start in [(1, "candidate-one", GOLD, 20), (3, "candidate-three", RED, 60)]:
        points = [(100 + 520*i/320, 320 - 300*0.2*math.sin(n*math.pi*i/320)) for i in range(321)]
        body += path(points, color, 2, True)
        body += path(points, color, 4).replace('<path ', f'<path class="{name}" data-candidate="{n}" ')
        css += (f".{name}{{opacity:1;animation:{name} 5s linear 1 both}}"
                f"@keyframes {name}{{0%,{start}%{{opacity:0}}{start+20}%,100%{{opacity:1}}}}"
                f"@media(prefers-reduced-motion:reduce){{.{name}{{animation:none}}}}")
    body += text(267, 235, "① 一次鼓起：ε sin(t/2)", 22, GOLD)
    body += text(171, 412, "② 三段波动：ε sin(3t/2)", 22, RED)
    body += panel(550, 220) + text(48, 590, "取 ε = 0.2 米，直接积分得到作用量差：", 23)
    body += text(48, 639, "① ΔS = −0.047124 焦耳·秒", 24, GOLD)
    body += text(48, 685, "真实运动 S = 0", 24, BLUE)
    body += text(48, 731, "② ΔS = +0.078540 焦耳·秒", 24, RED)
    body += panel(790, 188)
    body += rows(48, 830, ["两个候选的作用量分别更小、更大：真实解不是极小。", "但任意微小扰动的一阶变化为零，这才叫驻定。", "动画只依次强调候选线，不模拟球沿候选线运动。"], 22, 48)
    write("stationary-action.svg", 1008, "固定端点谐振子作用量的非极小反例",
          "时间二倍圆周率秒，真实轨道为平衡点静止。两类正弦候选固定端点，作用量差一负一正，真实轨道为驻定但非极小。教学动画依次强调候选，全部信息静态保留。", body, css)


def oscillator_state(fraction):
    t = math.pi * fraction
    return 0.5 * math.cos(2*t), -math.sin(2*t)


def spring_shape(x):
    start, end, y = 140, 400 + 180*x - 22, 225
    points = [(start, y), (start+12, y)]
    points += [(start+12+(end-start-24)*i/20, y+(12 if i % 2 else -12)) for i in range(1, 20)]
    points += [(end-12, y), (end, y)]
    return "M" + " L".join(f"{px:.6f},{py:.6f}" for px, py in points)


def phase():
    states = [oscillator_state(i / FRAMES) for i in range(FRAMES + 1)]
    for x, p in states:
        assert abs(p*p/2 + 4*x*x/2 - 0.5) < 1e-14
    assert math.dist(states[0], states[-1]) < 1e-14
    for i in range(FRAMES):
        mid = oscillator_state((i + 0.5) / FRAMES)
        linear = tuple((a+b)/2 for a, b in zip(states[i], states[i+1]))
        assert math.hypot(420*(mid[0]-linear[0]), 110*(mid[1]-linear[1])) < 0.02
    duration = 2 * math.pi
    css = animation("spring-mass", [f"translate({400+180*x:.7f}px,225px)" for x, _ in states], duration)
    css += animation("phase-dot", [f"translate({360+420*x:.7f}px,{650-110*p:.7f}px)" for x, p in states], duration)
    css += animation("moving-spring", [f'path("{spring_shape(x)}")' for x, _ in states], duration, "d")
    body = heading("⑥", "现实中的直线，相空间中的椭圆")
    body += panel(76, 282) + rows(48, 116, ["m = 1 千克，k = 4 牛顿/米，振幅 A = 0.5 米", "周期 π 秒；上下两图同步，动画放慢 2 倍。"], 23)
    body += line(125, 184, 125, 261, INK) + line(126, 252, 600, 252, "#aab9c6")
    body += line(400, 185, 400, 258, "#aab9c6", True)
    body += f'<path class="moving-spring" d="{spring_shape(0.5)}" stroke="{GOLD}" stroke-width="3" fill="none"/>'
    body += f'<g class="spring-mass"><rect x="-22" y="-19" width="44" height="38" rx="4" fill="{BLUE}"/></g>'
    body += line(310, 286, 490, 286, INK, arrow=True)
    body += text(400, 321, "x = 0", 22, INK, "middle") + text(512, 292, "x", 24)
    body += panel(378, 452) + text(48, 419, "相图的一点 = 此刻的位置 x 与动量 p", 24)
    body += line(90, 650, 636, 650, INK, arrow=True) + line(360, 785, 360, 488, INK, arrow=True)
    body += text(641, 659, "x", 24) + text(371, 495, "p", 24)
    body += path([(360+420*x, 650-110*p) for x, p in states], BLUE)
    body += '<g class="phase-dot"><circle cx="0" cy="0" r="10" fill="' + RED + '" stroke="white" stroke-width="2"/></g>'
    for x, p in [(-0.5, 0), (0, 1), (0.5, 0), (0, -1)]:
        body += dot(360+420*x, 650-110*p, 5, GOLD)
    body += text(110, 686, "−0.5", 21, INK, "middle") + text(612, 686, "0.5", 21, INK, "middle")
    body += text(385, 520, "1", 21) + text(385, 790, "−1", 21)
    body += line(573, 617, 573, 643, RED, arrow=True)
    body += text(48, 817, "横轴单位：米；纵轴单位：千克·米/秒", 22)
    body += panel(850, 230)
    body += rows(48, 890, ["右端：x = 0.5，p = 0 → 向左加速。", "经过原点向左：x = 0，p = −1。", "左端：x = −0.5，p = 0 → 向右加速。", "椭圆不是球的空间轨道；它是一圈状态变化。"], 23, 47)
    write("phase-space.svg", 1110, "同步的弹簧振子位置与动量相图",
          "解析解x为二分之一cos2t，p为负sin2t，能量恒为二分之一焦耳。空间运动为直线，相图为椭圆，同步两倍慢放一个周期，静态椭圆和状态表保留。", body, css)


def symmetry():
    body = heading("⑦", "不变的规律，留下守恒的量")
    entries = [
        ("时间平移", "能量", "今天与明天，用同一套运动规律。", "例：固定支点、无摩擦单摆。"),
        ("空间平移", "总动量", "整体搬到另一处，规律仍相同。", "例：无外力、相互作用只依赖相对位置的系统。"),
        ("空间旋转", "角动量", "整体转一个角度，规律仍相同。", "例：固定中心的球对称引力场。"),
    ]
    for i, (left, right, explanation, example) in enumerate(entries):
        y = 76 + 244 * i
        body += panel(y, 222) + text(48, y+43, left, 27, BLUE)
        body += line(230, y+34, 420, y+34, GOLD, arrow=True) + text(457, y+43, right, 27, RED)
        body += rows(48, y+103, [explanation, example], 22, 48)
        body += text(48, y+196, "要求作用量的相应连续对称性，不是外观相似。", 22)
    body += panel(828, 196)
    body += rows(48, 870, ["单摆支点选定了一个位置：空间平移对称性被打破。", "所以摆球自身动量不守恒，不能套用第二条。", "若支点主动移动或有摩擦，原来的能量账也要重写。"], 22, 49)
    write("symmetry-conservation.svg", 1054, "诺特定理的三个常见守恒对应",
          "时间、空间平移与旋转连续对称性分别关联能量、总动量、角动量，需针对系统作用量判断。固定单摆只有这里所述时间对称性而不具空间平移对称性。", body)


def effective_potential(r):
    return 0.8**2 / (2*r*r) - 1/r


def orbit():
    angular_momentum, energy = 0.8, -0.6
    a = -1 / (2*energy)
    e = math.sqrt(1+2*energy*angular_momentum**2)
    b, c = a*math.sqrt(1-e*e), a*e
    r1, r2 = a-c, a+c
    assert abs(effective_potential(r1)-energy) < 1e-12
    assert abs(effective_potential(r2)-energy) < 1e-12
    rmin = angular_momentum**2
    assert abs(effective_potential(rmin) + 0.78125) < 1e-12
    body = heading("⑧", "把二维轨道，变成径向能量账")
    body += panel(76, 424) + rows(48, 116, ["理想固定中心引力；归一化单位 GM = m = 1", "取角动量 J = 0.8、总能量 E = −0.6"], 23)
    points = [(420+170*(a*math.cos(2*math.pi*i/360)-c),
               294-170*b*math.sin(2*math.pi*i/360)) for i in range(361)]
    body += path(points, BLUE) + dot(420, 294, 12, GOLD)
    body += text(430, 333, "引力中心", 22, GOLD)
    body += dot(420+170*r1, 294, 9, RED) + dot(420-170*r2, 294, 9, BLUE)
    body += text(526, 264, "近日点", 22, RED) + text(145, 264, "远日点", 22, BLUE)
    body += text(48, 468, f"r 从 {r1:.3f} 到 {r2:.3f}；这张轨道图等比例绘制。", 22)
    body += panel(520, 480) + text(48, 562, "有效势能：转动项 + 引力势能", 24)
    body += text(48, 603, "不是多出一种力，而是把角运动的能量计入。", 22)
    points = [(120+240*r, 770-105*effective_potential(r))
              for r in [0.25+1.75*i/500 for i in range(501)]]
    body += path(points, BLUE)
    body += line(140, 900, 640, 900, INK, arrow=True) + text(650, 909, "r", 24)
    body += line(140, 900, 140, 632, INK, arrow=True) + text(48, 662, "有效势能", 20)
    body += line(140, 770, 620, 770, "#a6b5c0", True) + text(111, 777, "0", 21)
    ey = 770-105*energy
    body += line(174, ey, 620, ey, RED, True)
    body += text(460, 743, "能量 E = −0.6", 22, RED)
    for r in [r1, r2]:
        body += dot(120+240*r, ey, 7, RED)
        body += line(120+240*r, ey, 120+240*r, 900, "#aab9c6", True)
    body += dot(120+240*rmin, 770-105*effective_potential(rmin), 7, GOLD)
    for r in [0.5, 1, 1.5, 2]:
        x = 120+240*r
        body += line(x, 900, x, 906) + text(x, 934, str(r), 21, INK, "middle")
    body += text(48, 974, "两交点是径向转折点；谷底 r = 0.640 对应圆轨道。", 22)
    write("orbital-energy.svg", 1030, "中心引力轨道与有效势能的同一组计算",
          "归一化固定中心模型，角动量零点八、能量负零点六。椭圆近日远日距离与有效势能水平线两交点一致。谷底对应同一角动量下的圆轨道，势能图两轴为不同物理量。", body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert 2.040 < PERIOD < 2.041
    for generate in [history, constraints, energy_motion, degrees, action, phase, symmetry, orbit]:
        generate()
    print("Generated 8 diagrams, including 3 one-shot animations; mechanics assertions passed.")


if __name__ == "__main__":
    main()
