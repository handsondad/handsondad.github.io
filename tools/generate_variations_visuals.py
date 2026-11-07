"""Original variational-calculus diagrams, with a one-shot curve-family illustration."""

import math
from pathlib import Path

from generate_kepler_newton_visuals import BLUE, GOLD, INK, RED, dot, line, panel, path, save, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "variations"
C = 299792458.0


def write(name, height, title, description, body, css=""):
    save(name, height, title, description, body, css, output_directory=OUT)


def heading(number, value):
    return text(36, 48, f"{number} {value}", 29)


def rows(x, y, values, size=23, step=43, color=INK):
    return "".join(text(x, y+i*step, value, size, color) for i, value in enumerate(values))


def integrate(f, a=0.0, b=1.0, count=8192):
    assert count % 2 == 0
    h = (b-a)/count
    return h/3 * (f(a)+f(b)+4*sum(f(a+i*h) for i in range(1, count, 2)) +
                  2*sum(f(a+i*h) for i in range(2, count, 2)))


def slope_score(amplitude):
    return 1+math.pi**2*amplitude**2/2


def curve_length(amplitude):
    return integrate(lambda x: math.sqrt(1+(1+amplitude*math.pi*math.cos(math.pi*x))**2))


def route(amplitude, ox=160, oy=855, scale=300):
    return [(ox+scale*x, oy-scale*(x+amplitude*math.sin(math.pi*x)))
            for x in [i/160 for i in range(161)]]


def functions():
    body = heading("①", "函数看一个值，泛函评整条曲线")
    body += panel(76, 365) + text(48, 116, "函数：给 x = 0.5，算 f(x) = x² = 0.25", 24)
    body += line(100, 345, 650, 345, INK, arrow=True)
    body += line(100, 345, 100, 145, INK, arrow=True)
    body += text(651, 379, "x", 23) + text(73, 154, "y", 23)
    body += path([(100+520*x, 345-200*x*x) for x in [i/160 for i in range(161)]])
    body += line(360, 345, 360, 295, GOLD, True)
    body += line(100, 295, 360, 295, GOLD, True) + dot(360, 295, 8, BLUE)
    body += text(360, 378, "0.5", 22, INK, "middle") + text(48, 301, "0.25", 21)
    body += text(48, 416, "你得到的是曲线上的一个数值，不是整条线的评分。", 22)
    body += panel(461, 482) + text(48, 503, "泛函：给整条 y(x)，算全程长度 ℓ[y]", 24)
    for amplitude, color, dashed in [(0.2, GOLD, True), (-0.2, RED, True), (0, BLUE, False)]:
        body += path(route(amplitude), color, 3, dashed)
    body += dot(160, 855, 8, INK) + dot(460, 555, 8, INK)
    body += text(124, 885, "A", 24) + text(471, 555, "B", 24)
    body += rows(478, 613, ["直线", "ℓ ≈ 1.414"], 22, 34, BLUE)
    body += rows(478, 720, ["弯曲候选", "ℓ ≈ 1.451"], 22, 34, GOLD)
    body += text(48, 921, "两条弯曲候选等长；此处横纵等比例，数值无量纲。", 22)
    write("function-and-functional.svg", 975, "函数的单点值与泛函的整条曲线评分",
          "上图函数x平方在x零点五的值为零点二五。下图固定端点的直线与正负正弦扰动，弧长分别为根号二和约一点四五一；曲线等比例绘制。", body)


def perturbation_coordinates(amplitude):
    return route(amplitude, oy=745)


def perturbation_d(amplitude):
    return "M"+" L".join(f"{x:.6f},{y:.6f}" for x, y in perturbation_coordinates(amplitude))


def perturbation_amplitude(time_ms):
    if time_ms <= 1500:
        return 0.2*time_ms/1500
    if time_ms <= 3500:
        return 0.2-0.4*(time_ms-1500)/2000
    return -0.2+0.2*(time_ms-3500)/1500


def perturbation():
    body = heading("②", "ε 控制幅度，η 决定改动的形状")
    body += panel(76, 280) + rows(48, 115, ["先选 η(x) = sin(πx)：中间鼓起、两端为零。", "再用一个小数 ε，把这份改动加到整条基线上。"], 23, 38)
    body += line(100, 275, 650, 275, INK, arrow=True)
    body += path([(100+520*x, 275-100*math.sin(math.pi*x))
                  for x in [i/160 for i in range(161)]], GOLD)
    body += dot(100, 275, 6, INK) + dot(620, 275, 6, INK)
    body += text(100, 306, "0", 21, INK, "middle") + text(620, 306, "1", 21, INK, "middle")
    body += text(48, 343, "η(0) = η(1) = 0 → 无论怎样改变 ε，端点都不动。", 22)
    body += panel(376, 470) + text(48, 415, "基线 y(x) = x；候选 yε(x) = x + ε sin(πx)", 23)
    for a, color in [(0.2, GOLD), (-0.2, RED), (0, "#a2b4c2")]:
        body += path(perturbation_coordinates(a), color, 2, True)
    body += f'<path class="perturb-curve" d="{perturbation_d(0)}" stroke="{BLUE}" stroke-width="4" fill="none"/>'
    body += f'<circle class="perturb-point" data-perturb-point="midpoint" cx="310" cy="595" r="8" fill="{BLUE}"/>'
    body += dot(160, 745, 8, INK) + dot(460, 445, 8, INK)
    body += text(130, 782, "A", 24) + text(481, 452, "B", 24)
    body += text(492, 532, "ε = +0.2", 23, GOLD)
    body += text(492, 589, "Δy = εη", 23)
    body += text(492, 644, "ε = 0", 23, BLUE)
    body += text(492, 710, "ε = −0.2", 23, RED)
    body += text(48, 819, "只在演示函数家族的变化，不是物体沿线运动。", 23)
    keyframes = [(0, 0), (30, 0.2), (70, -0.2), (100, 0)]
    css = '.perturb-curve{d:path("'+perturbation_d(0)+'");animation:curve-family 5s linear 1 both}'
    css += "@keyframes curve-family{"+''.join(
        f'{p}%{{d:path("{perturbation_d(a)}")}}' for p, a in keyframes)+"}"
    css += ".perturb-point{transform:translateY(0px);animation:curve-point 5s linear 1 both}"
    css += "@keyframes curve-point{"+''.join(f"{p}%{{transform:translateY({-300*a:.6f}px)}}" for p, a in keyframes)+"}"
    css += "@media(prefers-reduced-motion:reduce){.perturb-curve,.perturb-point{animation:none}}"
    for a in [0, 0.2, -0.2]:
        points = perturbation_coordinates(a)
        assert math.dist(points[0], (160, 745)) < 1e-12
        assert math.dist(points[-1], (460, 445)) < 1e-12
    write("perturb-a-curve.svg", 877, "固定端点的正弦小扰动家族",
          "先展示扰动形状sinπx，再将幅度从零变为正零点二、负零点二、最后回零，按统一线性参数改变整条曲线。两端始终固定，静态候选始终完整，减少动态效果保留最终基线和比较曲线。", body, css)


def score():
    body = heading("③", "把整条线的评分，暂时变成 ε 的函数")
    body += panel(76, 359) + rows(48, 115, ["基线 y = x，评分 J[y] = ∫₀¹(y′)² dx", "φ(ε) = 1 + π²ε²/2；φ′(0) = 0"], 23, 38)
    body += line(120, 355, 635, 355, INK, arrow=True) + line(120, 355, 120, 195, INK, arrow=True)
    body += text(48, 214, "J − 1", 22) + text(643, 363, "ε", 24)
    body += path([(360+700*e, 355-200*(slope_score(e)-1))
                  for e in [-0.3+0.6*i/200 for i in range(201)]], BLUE)
    body += dot(360, 355, 8, BLUE) + text(360, 389, "0", 22, INK, "middle")
    body += text(402, 235, "这里斜率为 0", 23, BLUE)
    body += text(48, 425, "一阶变化为零；J 本身却等于 1，不是 0。", 22)
    body += panel(455, 386) + rows(48, 494, ["换成弯曲基线：y = x + 0.2 sin(πx)", "φ(ε) = 1 + π²(0.2 + ε)²/2"], 23, 38)
    body += line(140, 720, 641, 720, INK, arrow=True) + line(140, 720, 140, 568, INK, arrow=True)
    body += text(48, 593, "J − 1", 22) + text(649, 728, "ε", 24)
    body += path([(495+1100*e, 720-200*(slope_score(0.2+e)-1))
                  for e in [-0.3+0.4*i/200 for i in range(201)]], RED)
    body += dot(495, 720-200*(slope_score(0.2)-1), 8, RED)
    body += dot(275, 720, 7, GOLD)
    body += text(495, 753, "0", 22, INK, "middle") + text(275, 753, "−0.2", 22, INK, "middle")
    body += text(386, 597, "φ′(0) ≈ 1.974 > 0", 23, RED)
    body += text(48, 809, "稍取 ε < 0 就能降分：弯曲基线还没有驻定。", 22)
    write("score-and-first-variation.svg", 872, "直线与弯曲基线的第一变分比较",
          "无量纲坡度平方积分评分。直线沿正弦方向的评分为1加π平方ε平方除2，导数在零处为零；弯曲基线的导数为约一点九七四。两个图各标J减1，横轴为扰动幅度。", body)


def local_bump(x):
    z = (x-0.5)/0.2
    return 0.1*(1-z*z)**3 if abs(z) < 1 else 0.0


def residual(x):
    return 0.4*math.pi**2*math.sin(math.pi*x)


LOCAL_VARIATION = integrate(lambda x: residual(x)*local_bump(x))


def local():
    body = heading("④", "为什么“所有扰动”会逼出局部方程？")
    charts = [
        (76, "① 弯曲基线的残差 R(x) = −2y″(x)", residual, residual(0.5), RED),
        (366, "② 挑一个只在中间起作用的扰动 η(x)", local_bump, 0.1, BLUE),
        (656, "③ 相乘后积分：正面积，不可能等于零", lambda x: residual(x)*local_bump(x), residual(0.5)*0.1, GOLD),
    ]
    for y, title, f, peak, color in charts:
        body += panel(y, 270) + text(48, y+40, title, 23)
        baseline = y+224
        points = [(100+520*x, baseline-110*f(x)/peak)
                  for x in [i/400 for i in range(401)]]
        if y == 656:
            body += '<path d="M100,'+str(baseline)+" L"+" L".join(f"{x:.6f},{v:.6f}" for x, v in points)+f' L620,{baseline} Z" fill="{GOLD}" fill-opacity=".18"/>'
        body += line(100, baseline, 650, baseline, INK, arrow=True) + path(points, color)
        body += text(100, baseline+27, "0", 21, INK, "middle")
        body += text(620, baseline+27, "1", 21, INK, "middle")
        body += text(486, y+102, f"最大 {peak:.3f}", 22, color)
    body += rows(36, 972, [f"本例 δJ = ∫Rη dx ≈ {LOCAL_VARIATION:.6f} > 0。", "三幅纵轴分别缩放；面积数值按实际公式积分。"], 22, 37)
    assert abs(LOCAL_VARIATION-integrate(lambda x: residual(x)*local_bump(x), count=16384)) < 1e-12
    assert LOCAL_VARIATION > 0
    write("local-bump.svg", 1033, "局部扰动与变分基本引理的直观解释",
          "残差对应y为x加零点二sinπx。选择支撑在零点三到零点七间、峰值零点一的二次连续可导紧支撑扰动，相乘积分约零点零七零六二。三图纵轴独立归一到同样高度，只比较符号，实际积分由原值计算。", body)


def boundaries():
    body = heading("⑤", "同一个内部方程，边界可以改掉答案")
    body += panel(76, 375) + rows(48, 115, ["最短曲线问题：A = (0,0)，B = (1,1) 都固定。", "允许改中间，不允许把 B 挪走。"], 23, 39)
    body += line(220, 380, 420, 180, BLUE) + dot(220, 380, 8, INK) + dot(420, 180, 8, INK)
    body += text(182, 410, "A", 25) + text(447, 183, "B", 25)
    body += text(468, 290, "最佳：y = x", 23, BLUE)
    body += panel(471, 390) + rows(48, 510, ["现在只固定终点横坐标 x = 1，纵坐标可以滑动。", "A 仍固定；同样是在找最短曲线。"], 23, 39)
    body += line(220, 755, 420, 555, "#aab9c6", True)
    body += line(220, 755, 420, 655, "#aab9c6", True)
    body += line(420, 555, 420, 755, "#aab9c6", True)
    body += line(220, 755, 420, 755, BLUE)
    body += dot(220, 755, 8, INK) + dot(420, 755, 8, BLUE)
    body += line(450, 622, 450, 709, RED, arrow=True)
    body += text(478, 650, "末端可以滑", 23, RED)
    body += text(186, 795, "A", 25) + text(428, 795, "C", 25)
    body += text(48, 838, "最佳到 C：y = 0，末端与竖直边界垂直。", 23, BLUE)
    body += panel(881, 155)
    body += rows(48, 925, ["欧拉—拉格朗日方程管内部。", "边界项与端点条件，决定你到底在解哪道题。"], 23, 50)
    assert math.dist((0, 0), (1, 1)) == math.sqrt(2)
    assert math.dist((0, 0), (1, 0)) == 1
    write("fixed-and-free-endpoints.svg", 1067, "固定终点与竖直边界上自由终点的最短路径",
          "上图固定两点最短线为斜率一的直线，下图末端只固定横坐标一，纵坐标可变，最短线为水平线并垂直于竖直边界。两图均等比例。", body)


def optical_time(u):
    return (math.sqrt(1+u*u)+1.5*math.sqrt(1+(1-u)**2))/C


def refraction_crossing():
    lo, hi = 0, 1
    for _ in range(80):
        u = (lo+hi)/2
        derivative = u/math.sqrt(1+u*u)-1.5*(1-u)/math.sqrt(1+(1-u)**2)
        if derivative > 0:
            hi = u
        else:
            lo = u
    return (lo+hi)/2


def optics():
    u = refraction_crossing()
    t1, t2 = math.atan(u), math.atan(1-u)
    assert abs(math.sin(t1)-1.5*math.sin(t2)) < 1e-14
    assert optical_time(u) < min(optical_time(0), optical_time(0.5), optical_time(1))
    assert math.sqrt(1+u*u)+math.sqrt(1+(1-u)**2) > math.sqrt(5)
    body = heading("⑥", "光为什么在界面处拐弯？")
    body += panel(76, 760) + text(48, 116, "A = (0,1) 米，B = (1,−1) 米；界面在 y = 0", 23)
    body += text(48, 155, "理想均匀、无色散介质；图中横纵等比例。", 23)
    body += '<rect x="26" y="175" width="668" height="295" fill="#edf5f9"/>'
    body += '<rect x="26" y="470" width="668" height="290" fill="#fff6e6"/>'
    a, b, p = (180, 230), (420, 710), (180+240*u, 470)
    body += path([a, (180, 470), b], "#a4b5c3", 2, True)
    body += path([a, b], GOLD, 2, True)
    body += line(48, 470, 672, 470, INK)
    body += line(p[0], 262, p[0], 690, "#869aaa", True)
    body += path([a, p, b], BLUE, 4)
    for point in [a, b, p]:
        body += dot(*point, 8, BLUE)
    body += text(142, 225, "A", 25) + text(445, 719, "B", 25)
    body += text(478, 334, "介质 1：n₁ = 1", 23)
    body += text(478, 592, "介质 2：n₂ = 1.5", 23)
    body += text(48, 393, "几何直线", 23, GOLD)
    body += text(381, 445, f"交点 u = {u:.3f}", 22)
    body += path([(p[0]-60*math.sin(t1*i/60), p[1]-60*math.cos(t1*i/60)) for i in range(61)], GOLD)
    body += path([(p[0]+60*math.sin(t2*i/60), p[1]+60*math.cos(t2*i/60)) for i in range(61)], RED)
    body += text(289, 377, "θ₁", 25, GOLD) + text(370, 552, "θ₂", 25, RED)
    body += text(48, 805, f"入射 {math.degrees(t1):.3f}°，折射 {math.degrees(t2):.3f}°；都对法线量。", 23)
    body += panel(856, 240) + text(48, 897, "各候选的两段时间相加：距离 ÷ 各段速度", 23)
    body += text(48, 941, f"交点 u = 0：{optical_time(0)*1e9:.3f} 纳秒", 23)
    body += text(48, 982, f"几何直线 u = 0.5：{optical_time(0.5)*1e9:.3f} 纳秒", 23, GOLD)
    body += text(48, 1023, f"交点 u = {u:.3f}：{optical_time(u)*1e9:.3f} 纳秒", 23, BLUE)
    body += text(48, 1066, "本例时间函数严格凸，驻定点确实是唯一最小。", 22)
    write("refraction-time.svg", 1127, "变动折射交点得到斯涅尔定律",
          "均匀非色散介质折射率一和一点五，固定两端距界面一米。最短时间交点约零点六二三二；金虚线为交点零点五的几何最短直线，用时却更多。蓝线角度验证斯涅尔定律，灰线为零交点候选；三线不是同时存在的折射光线。", body)


def chain():
    height = math.cosh(1)-1
    length = 2*math.sinh(1)
    deeper_length = math.sqrt(5)+math.asinh(2)/2
    body = heading("⑦", "链子不能一边比较，一边偷偷变长")
    body += panel(76, 530) + rows(48, 116, ["固定两端 x = ±1 米，支点等高；均匀柔链。", f"固定总长 {length:.6f} 米，只受自身重力。"], 23, 38)
    for f, color, dashed in [
        (lambda x: height, "#92a7b7", True),
        (lambda x: math.cosh(x)-1, BLUE, False),
        (lambda x: height-(1-x*x), RED, True),
    ]:
        points = [(360+260*x, 365-250*f(x)) for x in [-1+2*i/240 for i in range(241)]]
        body += path(points, color, 3, dashed)
        assert abs(f(-1)-height) < 1e-14 and abs(f(1)-height) < 1e-14
    for x in [100, 620]:
        body += dot(x, 365-250*height, 8, INK)
    body += text(240, 209, "支点高度固定", 23)
    body += dot(360, 365, 7, BLUE) + text(280, 410, "悬链线最低点", 22, BLUE)
    body += text(449, 509, "更深的候选", 22, RED)
    body += text(48, 575, "图为受力形状比较，不是链条下落动画；纵向略缩放。", 22)
    body += panel(626, 245)
    body += rows(48, 667, ["直线：长 2.000 米，不满足给定链长。"], 23, color=INK)
    body += text(48, 716, "悬链线：长 2.350 米，满足约束。", 23, BLUE)
    body += text(48, 765, f"更深抛物线：长 {deeper_length:.3f} 米，链不够长。", 23, RED)
    body += text(48, 835, "要找的是：在同样链长的允许形状中，势能最低。", 22)
    assert abs(integrate(lambda x: math.cosh(x), -1, 1)-length) < 1e-12
    assert abs(integrate(lambda x: math.sqrt(1+4*x*x), -1, 1)-deeper_length) < 1e-12
    write("chain-length-constraint.svg", 903, "悬链线势能比较必须保持链长不变",
          "支点横距两米、总长二点三五零四零二米。直线长两米，构造的更深抛物线长二点九五七八八六米，都不满足固定链长。蓝线为a等于一米的悬链线；纵横缩放比为250比260。", body)


def motion():
    g, m, epsilon = 9.81, 1, 0.4
    def lagrangian(t, amplitude):
        q = g*t*t/2+amplitude*math.sin(math.pi*t)
        v = g*t+amplitude*math.pi*math.cos(math.pi*t)
        return m*v*v/2+m*g*q

    for e in [-epsilon, epsilon]:
        assert abs(integrate(lambda t: lagrangian(t, e)-lagrangian(t, 0))-m*e*e*math.pi**2/4) < 1e-11
    body = heading("⑧", "同一套变分运算，换成时间就管运动")
    body += panel(76, 245) + rows(48, 117, [
        "形状问题：输入 y(x)，比较 J[y] = ∫F dx。",
        "动力学：输入 q(t)，比较 S[q] = ∫L dt。",
        "变的是整段函数；换的是变量和实际的评分规则。",
        "L = K − U，不是只比较势能 U。"], 23, 47)
    body += panel(341, 415) + rows(48, 380, ["例：向下为正的自由落体，从静止释放。", "一秒后到 q = 4.905 米；比较固定两端的候选。"], 23, 38)
    body += line(100, 670, 638, 670, INK, arrow=True) + line(100, 670, 100, 437, INK, arrow=True)
    body += text(648, 678, "t", 24) + text(65, 459, "q", 24)
    for e, color, dashed in [(epsilon, GOLD, True), (0, BLUE, False)]:
        points = [(100+520*t, 670-45*(g*t*t/2+e*math.sin(math.pi*t))) for t in [i/240 for i in range(241)]]
        body += path(points, color, 3, dashed)
    body += dot(100, 670, 7, INK) + dot(620, 670-45*g/2, 7, INK)
    body += text(100, 702, "0", 21, INK, "middle") + text(620, 702, "1 秒", 21, INK, "middle")
    body += text(48, 737, "这是时间—位移图，不是球在空间里向上爬的路线。", 22)
    body += panel(776, 244)
    body += rows(48, 816, [
        "真实曲线：q(t) = gt²/2；金虚线只是候选。",
        "候选不必满足牛顿定律，否则根本无从比较。",
        "运算得到 d(∂L/∂q̇)/dt − ∂L/∂q = 0。",
        "重力模型给出 q̈ = g，正是同一条运动规律。"], 23, 49)
    write("variation-to-mechanics.svg", 1051, "空间函数变分与时间运动函数变分的同一结构",
          "区分形状的空间积分与动力学作用量时间积分。自由落体以向下位移为正，g九点八一，固定零与一秒端点；真实曲线为二分之一gt平方，候选加零点四sinπt。图是位移时间坐标，不是空间轨迹。", body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for amplitude in [-0.2, 0, 0.2]:
        numerical = integrate(lambda x: (1+amplitude*math.pi*math.cos(math.pi*x))**2)
        assert abs(numerical-slope_score(amplitude)) < 1e-12
    assert abs(curve_length(0)-math.sqrt(2)) < 1e-12
    assert abs(curve_length(0.2)-curve_length(-0.2)) < 1e-12
    assert abs(math.pi**2*0.2-1.973920880217872) < 1e-14
    for generate in [functions, perturbation, score, local, boundaries, optics, chain, motion]:
        generate()
    print("Generated 8 original diagrams and one one-shot illustration; variational assertions passed.")


if __name__ == "__main__":
    main()
