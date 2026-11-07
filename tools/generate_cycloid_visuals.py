"""Cycloid diagrams and once-only motion, calculated under ideal gravity."""

import bisect
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from generate_kepler_newton_visuals import (
    BLUE, GOLD, INK, RED, dot, line, panel, path, save, text,
)


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "cycloid"
R, G = 1.0, 9.81
PI = math.pi
DESCENT = PI * math.sqrt(R / G)
SLOWDOWN = 4.0
X, Y = PI * R, 2 * R
CIRCLE_R = (X * X + Y * Y) / (2 * X)
CIRCLE_END = math.acos(1 - X / CIRCLE_R)
STRAIGHT_TIME = math.sqrt(2 * (X * X + Y * Y) / (G * Y))


def cycloid(theta):
    return R * (theta - math.sin(theta)), R * (1 - math.cos(theta))


def evolute(theta):
    return R * (theta + math.sin(theta)), R * (math.cos(theta) - 1)


def integrate(f, a, b, count=4096):
    step = (b - a) / count
    return sum(step * (f(a + i * step) + 4 * f(a + (i + .5) * step)
                       + f(a + (i + 1) * step)) / 6 for i in range(count))


def circle_integrand(q):
    if q == 0:
        return math.sqrt(2 * CIRCLE_R * CIRCLE_END / G)
    angle = CIRCLE_END * q * q
    return 2 * CIRCLE_R * CIRCLE_END * q / math.sqrt(2 * G * CIRCLE_R * math.sin(angle))


def circle_table(count):
    result = [0.0]
    for i in range(count):
        result.append(result[-1] + integrate(circle_integrand, i / count, (i + 1) / count, 1))
    return result


CIRCLE_CLOCK = circle_table(4096)
CIRCLE_TIME = CIRCLE_CLOCK[-1]
RACE_END = max(DESCENT, CIRCLE_TIME, STRAIGHT_TIME)


def circle_at(t):
    if t >= CIRCLE_TIME:
        return X, Y
    index = max(0, min(len(CIRCLE_CLOCK) - 2, bisect.bisect_right(CIRCLE_CLOCK, t) - 1))
    weight = (t - CIRCLE_CLOCK[index]) / (CIRCLE_CLOCK[index + 1] - CIRCLE_CLOCK[index])
    q = (index + weight) / (len(CIRCLE_CLOCK) - 1)
    angle = CIRCLE_END * q * q
    return CIRCLE_R * (1 - math.cos(angle)), CIRCLE_R * math.sin(angle)


def race_at(kind, t):
    if kind == "cycloid":
        return cycloid(min(PI, t * math.sqrt(G / R)))
    if kind == "circle":
        return circle_at(t)
    if kind == "straight":
        u = min(1.0, (t / STRAIGHT_TIME) ** 2)
        return X * u, Y * u
    raise ValueError(kind)


def tautochrone_at(s0, t):
    s = s0 * math.cos(min(PI / 2, t * math.sqrt(G / (4 * R))))
    return cycloid(2 * math.acos(max(0, min(1, s / (4 * R)))))


def period_circle(s0, length=4 * R):
    k = math.sin(s0 / (2 * length))
    return 4 * math.sqrt(length / G) * integrate(
        lambda u: 1 / math.sqrt(1 - k * k * math.sin(u) ** 2), 0, PI / 2, 1024)


def curve_points(fn, a, b, x, y, scale, count=180):
    return [(x + scale * px, y + scale * py)
            for px, py in (fn(a + (b - a) * i / count) for i in range(count + 1))]


def title_write(name, height, title, desc, body, css=""):
    save(name, height, title, desc, text(36, 44, title, 28) + body,
         css, output_directory=OUT)


def marker_motion(name, fn, duration, scale, ox, oy, colour, events=()):
    # Each keyframe is evaluated at physical time, not at equal path lengths.
    count = 240
    times = sorted(set([duration * i / count for i in range(count + 1)] + list(events)))
    positions = []
    for t in times:
        x, y = fn(t)
        positions.append((ox + scale * x, oy + scale * y))
    frames = "".join(
        f"{100*t/duration:.9f}%{{transform:translate({x:.6f}px,{y:.6f}px)}}"
        for t, (x, y) in zip(times, positions)
    )
    endx, endy = positions[-1]
    body = (f'<circle class="{name}" data-motion="{name}" cx="0" cy="0" r="9" '
            f'fill="{colour}" stroke="white" stroke-width="3"/>')
    css = (f".{name}{{transform:translate({endx:.6f}px,{endy:.6f}px);"
           f"animation:{name}-move {duration*SLOWDOWN:.9f}s linear 1s 1 both}}"
           f"@keyframes {name}-move{{{frames}}}"
           f"@media(prefers-reduced-motion:reduce){{.{name}{{animation:none}}}}")
    # Bound the geometric error of CSS linear interpolation between frames.
    for i in range(len(times) - 1):
        exact = fn((times[i] + times[i + 1]) / 2)
        approx = ((positions[i][0] + positions[i + 1][0]) / 2,
                  (positions[i][1] + positions[i + 1][1]) / 2)
        assert math.hypot(ox + scale * exact[0] - approx[0],
                          oy + scale * exact[1] - approx[1]) < .08
    return body, css


def rolling():
    base, ox, radius = 370, 70, 85
    body = panel(70, 495)
    body += text(48, 112, "圆沿直线无滑动滚动；观察轮缘上的红点。", 24)
    pts = [(ox + radius * (a - math.sin(a)), base - radius * (1 - math.cos(a)))
           for a in (2 * PI * i / 240 for i in range(241))]
    body += path(pts, RED, 4) + line(48, base, 660, base, INK)
    for a, label in [(0, "起点"), (PI / 2, "¼ 圈"), (PI, "½ 圈"), (2 * PI, "1 圈")]:
        x = ox + radius * (a - math.sin(a))
        y = base - radius * (1 - math.cos(a))
        body += dot(x, y, 5, RED)
        body += text(x, y - 20 if a == PI else y + 32, label, 22, INK, "middle")
    body += f'<g transform="translate({ox},{base-radius})"><g class="wheel-travel">'
    body += f'<circle cx="0" cy="0" r="{radius}" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    body += '<g class="wheel-turn">' + line(0, 0, 0, radius, BLUE)
    body += (f'<circle data-motion="rolling-point" cx="0" cy="{radius}" r="9" fill="{RED}"/>'
             + '</g>' + dot(0, 0, 5, BLUE) + '</g></g>')
    body += text(48, 455, "圆心走过的距离＝半径 × 转过的弧度。", 24)
    body += text(48, 505, "完整曲线一直保留；下面的滑轨会把它翻转。", 23)
    body += text(36, 610, "这是造曲线的滚动圆，不是沿滑轨滚动的球。", 23)
    css = (
        f".wheel-travel{{transform:translate({2*PI*radius:.9f}px,0);animation:travel 6s linear 1s 1 both}}"
        ".wheel-turn{transform:rotate(360deg);animation:turn 6s linear 1s 1 both}"
        f"@keyframes travel{{from{{transform:translate(0,0)}}to{{transform:translate({2*PI*radius:.9f}px,0)}}}}"
        "@keyframes turn{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}"
        "@media(prefers-reduced-motion:reduce){.wheel-travel,.wheel-turn{animation:none}}"
    )
    title_write("rolling-cycloid.svg", 650, "图 1｜一只滚动的圆，画出一条摆线",
                "无滑动滚动圆的轮缘点画摆线，圆心平移距离与转角满足无滑动约束。一圈六秒仅为绘图速度。", body, css)


def racing():
    body, css = "", ""
    types = [("cycloid", "① 摆线", BLUE, DESCENT),
             ("circle", "② 圆弧", GOLD, CIRCLE_TIME),
             ("straight", "③ 直线", RED, STRAIGHT_TIME)]
    for i, (kind, label, colour, end) in enumerate(types):
        top, ox, scale = 70 + 380 * i, 100, 130
        oy = top + 50
        body += panel(top, 360)
        body += text(48, top + 32, f"{label}：{end:.3f} 秒", 25, colour)
        if kind == "cycloid":
            pts = curve_points(cycloid, 0, PI, ox, oy, scale)
        elif kind == "circle":
            fn = lambda a: (CIRCLE_R * (1 - math.cos(a)), CIRCLE_R * math.sin(a))
            pts = curve_points(fn, 0, CIRCLE_END, ox, oy, scale)
        else:
            pts = [(ox, oy), (ox + scale * X, oy + scale * Y)]
        assert all(24 < x < 696 and top + 40 <= y < top + 345 for x, y in pts)
        body += path(pts, colour, 4)
        body += dot(ox, oy, 5, colour) + text(70, oy + 22, "A", 23)
        body += dot(ox + scale * X, oy + scale * Y, 5, colour)
        body += text(ox + scale * X + 29, oy + scale * Y, "B", 23)
        for fraction in [.25, .5, .75]:
            x, y = race_at(kind, end * fraction)
            body += dot(ox + scale * x, oy + scale * y, 4, "#8295a5")
        marker, rule = marker_motion("race-" + kind, lambda t, k=kind: race_at(k, t),
                                     RACE_END, scale, ox, oy, colour, events=(end,))
        body += marker
        css += rule
    body += text(36, 1248, "每条轨道：水平 3.142 米，落差 2.000 米。", 24)
    body += text(36, 1290, "灰点为各自用时的 ¼、½、¾；显示统一放慢四倍。", 22)
    title_write("descent-race.svg", 1330, "图 2｜同一出发点，三条轨道竞速",
                "同起点终点的摆线、初始竖直切线圆弧和直线，在无摩擦质点模型下从静止释放。每条画面等比例，统一时间尺度，终点停留仅为结束演示。", body, css)


def speed_depth():
    body = panel(70, 480)
    body += text(48, 112, "同一起点静止释放：下降越多，速率越大。", 24)
    body += text(48, 151, "到达同一深度，速率相同；到达时间未必相同。", 23)
    for i, depth in enumerate([.125, .5, 1.125, 2]):
        y = 215 + i * 80
        v = math.sqrt(2 * G * depth)
        body += text(48, y + 8, f"下降 {depth:g} 米", 23)
        body += line(245, y, 245 + v * 40, y, BLUE, arrow=True)
        body += text(540, y + 8, f"{v:.3f} 米/秒", 22)
    body += panel(580, 205)
    body += text(48, 625, "省时间的诀窍：先获得速度，再走后面的路。", 24)
    body += text(48, 672, "但“越陡越好”不成立：横向绕路也会花时间。", 23)
    body += text(48, 725, "时间账：每一小段用时＝这段长度 ÷ 当时速率。", 23)
    title_write("speed-and-depth.svg", 825, "图 3｜最快，不等于路程最短",
                "均匀重力下从相同起点静止释放，速率为根号二倍重力加速度乘下降深度，箭头长度按速率比例。", body)


def refraction():
    ox, oy, scale = 95, 175, 150
    body = panel(70, 630)
    body += text(48, 112, "把空间想成水平薄层：深处运动更快。", 24)
    for depth in [.125, .5, 1, 1.5, 2]:
        y = oy + scale * depth
        body += line(65, y, 640, y, "#a8bac9", dash=True)
        body += text(525, y - 9, f"y＝{depth:g} 米", 21)
    body += path(curve_points(cycloid, 0, PI, ox, oy, scale), BLUE, 4)
    for theta in [.65, 1.6, 2.0, 2.65]:
        x, y = cycloid(theta)
        px, py = ox + scale * x, oy + scale * y
        body += line(px, py, px + 45 * math.sin(theta / 2),
                     py + 45 * math.cos(theta / 2), RED, arrow=True)
    theta = 1.6
    x, y = cycloid(theta)
    px, py = ox + scale * x, oy + scale * y
    body += line(px, py, px, py + 65, INK, dash=True)
    body += path([(px + 30 * math.sin(a), py + 30 * math.cos(a))
                  for a in (theta / 2 * i / 30 for i in range(31))], INK, 2)
    body += text(px + 23, py + 55, "α", 24)
    body += text(48, 565, "α 从竖直线量起；红箭头沿切线。", 24)
    body += text(48, 612, "低速层少绕路，高速层承担更多横向移动。", 23)
    body += text(48, 658, "薄层折射类比解释候选曲线，不代替完整最优证明。", 21)
    title_write("refraction-layers.svg", 740, "图 4｜伯努利把下滑问题，想成了折射",
                "摆线切线角随深度增大，满足正弦切线角除以速率恒定；角从竖直方向测量。水平层只是推导类比，不是真实分层介质。", body)


def tautochrone():
    body, css = "", ""
    starts = [(.45, "① 较高处", BLUE), (1.2, "② 中间处", GOLD), (2.2, "③ 较低处", RED)]
    for i, (theta0, label, colour) in enumerate(starts):
        top, scale, ox = 70 + i * 310, 90, 75
        oy = top + 70
        s0 = 4 * R * math.cos(theta0 / 2)
        h0 = R * (1 + math.cos(theta0))
        body += panel(top, 290)
        body += text(48, top + 36, f"{label}：距底部弧长 {s0:.3f} 米", 24, colour)
        body += path(curve_points(cycloid, 0, 2 * PI, ox, oy, scale), "#a8bac9", 3)
        body += path(curve_points(cycloid, theta0, PI, ox, oy, scale), colour, 4)
        x, y = cycloid(theta0)
        body += dot(ox + scale * x, oy + scale * y, 5, colour)
        body += text(48, top + 272, f"出发高度 {h0:.3f} 米；到达 {DESCENT:.3f} 秒", 23)
        marker, rule = marker_motion(f"tauto-{i}", lambda t, s=s0: tautochrone_at(s, t),
                                     DESCENT, scale, ox, oy, colour)
        body += marker
        css += rule
    body += text(36, 1050, "三幅是同尺寸轨道的副本，不是三条不同形状。", 23)
    body += text(36, 1094, "同时从静止释放；都用四倍慢放，到底部结束演示。", 22)
    title_write("tautochrone-race.svg", 1135, "图 5｜同一轨道，不同起点同时到达",
                "三枚互不作用的理想质点在相同半径摆线轨道的三个非底部位置同时从静止释放，用弧长简谐运动解析式计时，均在约1.003秒到达底部。", body, css)


def arc_length():
    body = panel(70, 430)
    body += text(48, 112, "s 是沿轨道量到最低点的距离，不是水平距离。", 23)
    ox, oy, scale = 95, 165, 145
    body += path(curve_points(cycloid, 0, PI, ox, oy, scale), "#8295a5", 4)
    theta0 = 2 * PI / 3
    body += path(curve_points(cycloid, theta0, PI, ox, oy, scale), RED, 6)
    x, y = cycloid(theta0)
    px, py = ox + scale * x, oy + scale * y
    body += dot(px, py, 8, RED)
    body += line(px, py, px, oy + 2 * scale, GOLD, dash=True)
    body += text(px - 15, py + 45, "h", 24, GOLD, "end")
    body += text(465, 415, "s", 26, RED)
    body += text(48, 486, "这个点：s＝2 米，h＝0.5 米（r＝1 米）。", 23)
    body += panel(510, 420)
    body += text(48, 552, "摆线的特殊关系：高度随弧长的平方增长", 24)
    # Heights h(s)=s²/(8r), for r=1 m, from 0 to the cusp.
    gx, gy, sx, sy = 100, 840, 125, 115
    body += line(gx, gy, 630, gy, INK, arrow=True)
    body += line(gx, gy, gx, 590, INK, arrow=True)
    body += path([(gx + sx * s, gy - sy * s * s / (8 * R))
                  for s in (4 * R * i / 120 for i in range(121))], BLUE, 4)
    for s in [1, 2, 3, 4]:
        h = s * s / (8 * R)
        body += dot(gx + sx * s, gy - sy * h, 6, BLUE)
        body += text(gx + sx * s, gy + 32, s, 22, INK, "middle")
    for h in [0, .5, 1, 1.5, 2]:
        body += text(gx - 15, gy - sy * h + 7, f"{h:g}", 20, INK, "end")
    body += text(124, 609, "h（米）", 22)
    body += text(600, 910, "s（米）", 22, INK, "middle")
    body += text(48, 990, "沿轨道的加速度＝−g s / (4r)。", 27, BLUE)
    body += text(48, 1038, "离底部越远，拉回去的加速度恰好同比例增大。", 22)
    title_write("arc-length-restoring.svg", 1080, "图 6｜等时的秘密，藏在弧长里",
                "摆线到最低点的弧长s与高度h满足h等于s平方除以8r。红色曲段为弧长，金虚线为高度。高度弧长图使用独立标度并有单位。", body)


def periods():
    body = panel(70, 520)
    body += text(48, 112, "共同参数：普通摆长 L＝4 米；摆线 r＝1 米。", 23)
    body += text(48, 157, "横轴：两者从底部沿各自轨道量出的初始弧长。", 22)
    ox, oy, sx, sy = 100, 465, 140, 720
    body += line(ox, oy, 640, oy, INK, arrow=True)
    body += line(ox, oy, ox, 200, INK, arrow=True)
    t0 = 4 * DESCENT
    pts = [(ox + sx * s, oy - sy * (period_circle(s) - t0))
           for s in (3.6 * i / 100 for i in range(101))]
    body += path(pts, GOLD, 4)
    body += line(ox, oy, ox + 3.6 * sx, oy, BLUE)
    body += text(115, 390, "摆线：周期不随振幅改变", 22, BLUE)
    body += text(330, 220, "普通圆弧摆：周期逐渐变长", 22, GOLD)
    for s in [0, 1, 2, 3]:
        body += text(ox + sx * s, oy + 34, s, 22, INK, "middle")
    for delta in [0, .1, .2, .3]:
        yy = oy - sy * delta
        body += text(85, yy + 7, f"{t0+delta:.2f}", 20, INK, "end")
    body += text(120, 200, "周期（秒）", 22)
    body += text(415, 553, "出发弧长 s₀（米）", 23)
    body += panel(620, 295)
    body += text(48, 665, "相同出发弧长      普通摆完整周期      摆线完整周期", 22)
    for i, s in enumerate([1, 2, 3]):
        y = 718 + i * 62
        body += text(100, y, f"{s:g} 米", 24)
        body += text(340, y, f"{period_circle(s):.3f} 秒", 24, GOLD, "middle")
        body += text(575, y, f"{t0:.3f} 秒", 24, BLUE, "middle")
    body += text(36, 966, "小振幅时非常接近；此图没有把“近似”等同于“精确”。", 22)
    title_write("pendulum-periods.svg", 1005, "图 7｜普通钟摆，为什么只是近似等时？",
                "普通单摆完整周期用椭圆积分数值计算，与相同初始弧长的理想摆线完整周期比较。L为4米，r为1米，共同小振幅周期约4.012秒。", body)


def cheeks():
    body = panel(70, 735)
    body += text(48, 112, "线缠上弯曲挡板，自由悬垂的部分就变短。", 24)
    ox, oy, scale = 360 - PI * 90, 385, 90
    pivot = (ox + PI * scale, oy - 2 * R * scale)
    theta = 1.3
    left = curve_points(evolute, 0, PI, ox, oy, scale)
    right = curve_points(evolute, PI, 2 * PI, ox, oy, scale)
    body += path(left, BLUE, 6) + path(right, BLUE, 6)
    body += path(curve_points(cycloid, .25, 2 * PI - .25, ox, oy, scale),
                 "#8295a5", 3, dash=True)
    body += path(curve_points(evolute, theta, PI, ox, oy, scale), RED, 5)
    ex, ey = evolute(theta)
    px, py = cycloid(theta)
    contact = (ox + scale * ex, oy + scale * ey)
    bob = (ox + scale * px, oy + scale * py)
    body += line(*contact, *bob, RED) + dot(*pivot, 7, INK) + dot(*contact, 6, RED)
    body += dot(*bob, 12, GOLD)
    body += line(*pivot, ox + PI * scale, oy + 2 * R * scale, INK, dash=True)
    body += text(360, 183, "固定悬点", 24, INK, "middle")
    body += text(470, 270, "摆线挡板", 24, BLUE)
    body += text(48, 355, "贴着挡板的绳", 22, RED)
    body += text(48, 495, "自由绳段", 23, RED)
    body += text(360, 602, "虚线：摆锤的摆线轨迹", 23, INK, "middle")
    wrapped = 4 * R * (1 - math.sin(theta / 2))
    free = 4 * R * math.sin(theta / 2)
    body += text(48, 674, f"图中：缠绕 {wrapped:.3f} 米＋自由 {free:.3f} 米", 24)
    body += text(48, 722, "总绳长仍为 4 米；绳在接触点沿挡板切线离开。", 23)
    body += text(48, 770, "两块挡板和下方轨迹都是同尺寸的摆线片段。", 23)
    body += panel(840, 165)
    body += text(48, 883, "理想条件：细绳无质量、不可伸长、无弯曲阻力。", 22)
    body += text(48, 930, "实际钟表还受摩擦、驱动、温度与制造误差影响。", 23)
    body += text(48, 977, "数学上精确，不代表工程上一定最实用。", 24)
    title_write("huygens-cheeks.svg", 1045, "图 8｜惠更斯：让绳子改变自己的有效长度",
                "摆线挡板是摆锤轨迹的渐屈线，红绳沿挡板缠绕后切向离开。按统一长度比例作图，绳总长4r，接触点与摆锤满足切向约束。", body)


def validate():
    assert math.isclose(CIRCLE_TIME, circle_table(8192)[-1], abs_tol=1e-11)
    assert DESCENT < CIRCLE_TIME < STRAIGHT_TIME
    for kind in ["cycloid", "circle", "straight"]:
        assert math.dist(race_at(kind, 0), (0, 0)) < 1e-12
        assert math.dist(race_at(kind, RACE_END), (X, Y)) < 1e-12
    # Arc, height, tangent force and total rope length at many locations.
    for i in range(1, 300):
        theta = PI * i / 300
        x, y = cycloid(theta)
        s = 4 * R * math.cos(theta / 2)
        h = 2 * R - y
        assert math.isclose(h, s * s / (8 * R), rel_tol=1e-10)
        assert math.isclose(G * math.cos(theta / 2), G * s / (4 * R), rel_tol=1e-12)
        ex, ey = evolute(theta)
        cord = (x - ex, y - ey)
        tangent = (R * (1 + math.cos(theta)), -R * math.sin(theta))
        track_tangent = (R * (1 - math.cos(theta)), R * math.sin(theta))
        assert abs(tangent[0] * cord[1] - tangent[1] * cord[0]) < 1e-11
        assert abs(track_tangent[0] * cord[0] + track_tangent[1] * cord[1]) < 1e-11
        wrapped = 4 * R * (1 - math.sin(theta / 2))
        assert math.isclose(wrapped + math.hypot(*cord), 4 * R, abs_tol=1e-11)
        assert math.isclose(math.sin(theta / 2) / math.sqrt(2 * G * y),
                            1 / (2 * math.sqrt(G * R)), rel_tol=1e-10)
    # Independent energy-integral check, regularized at the release point.
    for theta0 in [.45, 1.2, 2.2]:
        s0 = 4 * R * math.cos(theta0 / 2)
        def dt_du(u):
            s = s0 * math.cos(u)
            numerator = s0 * math.sin(u)
            if abs(numerator) < 1e-10:
                return 2 * math.sqrt(R / G)
            v = math.sqrt(G * (s0 * s0 - s * s) / (4 * R))
            return numerator / v
        assert math.isclose(integrate(dt_du, 0, PI / 2), DESCENT, abs_tol=1e-9)
        assert math.dist(tautochrone_at(s0, DESCENT), (X, Y)) < 1e-12
        for j in range(100):
            t = DESCENT * j / 100
            theta = 2 * math.acos(s0 * math.cos(t * math.sqrt(G / (4 * R))) / (4 * R))
            v = s0 * math.sqrt(G / (4 * R)) * math.sin(t * math.sqrt(G / (4 * R)))
            assert abs(.5 * v * v - G * (cycloid(theta)[1] - cycloid(theta0)[1])) < 1e-10
    # Arc and enclosed area of a full arch.
    assert math.isclose(integrate(lambda t: 2 * R * math.sin(t / 2), 0, 2 * PI),
                        8 * R, rel_tol=1e-12)
    assert math.isclose(integrate(lambda t: R * R * (1 - math.cos(t)) ** 2, 0, 2 * PI),
                        3 * PI * R * R, rel_tol=1e-12)
    ns = {"s": "http://www.w3.org/2000/svg"}
    files = sorted(OUT.glob("*.svg"))
    assert len(files) == 8
    for file in files:
        root = ET.parse(file).getroot()
        assert root.find("s:title", ns) is not None and root.find("s:desc", ns) is not None
        assert root.attrib["viewBox"] == f'0 0 {root.attrib["width"]} {root.attrib["height"]}'
    print(f"Race seconds: cycloid={DESCENT:.9f}, circle={CIRCLE_TIME:.9f}, straight={STRAIGHT_TIME:.9f}")
    print("Equal-time arrivals, energy, no-slip geometry, tangent rope and integration convergence passed.")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [rolling, racing, speed_depth, refraction, tautochrone,
                 arc_length, periods, cheeks]:
        draw()
    validate()
