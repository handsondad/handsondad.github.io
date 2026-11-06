"""Reproduce the article's original diagrams using only the standard library."""

import math
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "kepler-newton"
TAU = 2 * math.pi
E = 0.6
B = math.sqrt(1 - E * E)
INK, BLUE, RED, GOLD = "#172b45", "#176786", "#b34039", "#b77a09"


def text(x, y, value, size=24, color=INK, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}">{escape(str(value))}</text>'
    )


def line(x1, y1, x2, y2, color=INK, dash=False, arrow=False):
    return (
        f'<path d="M{x1:.3f},{y1:.3f} L{x2:.3f},{y2:.3f}" fill="none" '
        f'stroke="{color}" stroke-width="3"'
        + (' stroke-dasharray="7 6"' if dash else "")
        + (' marker-end="url(#arrow)"' if arrow else "")
        + "/>"
    )


def dot(x, y, r=6, color=BLUE):
    return f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{color}"/>'


def path(points, color=BLUE, width=3, dash=False):
    d = "M" + " L".join(f"{x:.3f},{y:.3f}" for x, y in points)
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"'
        + (' stroke-dasharray="8 6"' if dash else "")
        + "/>"
    )


def panel(y, height):
    return (
        f'<rect x="24" y="{y}" width="672" height="{height}" rx="16" '
        'fill="#fff" stroke="#ccd8e2" stroke-width="2"/>'
    )


def save(name, height, title, description, body, css="", output_directory=None):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{height}" '
        f'viewBox="0 0 720 {height}" role="img" aria-labelledby="title desc" lang="zh-CN">'
        f"<title id=\"title\">{escape(title)}</title>"
        f"<desc id=\"desc\">{escape(description)}</desc>"
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" '
        'refY="4" orient="auto-start-reverse"><path d="M0 0L8 4L0 8Z" '
        'fill="context-stroke"/></marker></defs>'
        '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}'
        + css
        + "</style>"
        f'<rect width="720" height="{height}" fill="#f3f7fa"/>'
        + body
        + "</svg>\n"
    )
    root = ET.fromstring(svg)
    assert root.attrib["viewBox"] == f'0 0 {root.attrib["width"]} {root.attrib["height"]}'
    directory = OUT if output_directory is None else output_directory
    (directory / name).write_text(svg, encoding="utf-8")


def eccentric_anomaly(mean):
    value = mean
    for _ in range(20):
        delta = (value - E * math.sin(value) - mean) / (1 - E * math.cos(value))
        value -= delta
        if abs(delta) < 1e-14:
            break
    assert abs(value - E * math.sin(value) - mean) < 1e-12
    return value


def position(mean):
    anomaly = eccentric_anomaly(mean)
    return math.cos(anomaly) - E, B * math.sin(anomaly)


def project(point, sx=480, sy=405, scale=260):
    x, y = point
    return sx + scale * x, sy - scale * y


def orbit():
    return [project(position(TAU * i / 960)) for i in range(961)]


def geometry():
    # Two distances to the foci sum to 2a for every point.
    point = (math.cos(math.pi / 3) - E, B * math.sin(math.pi / 3))
    d1 = math.hypot(*point)
    d2 = math.hypot(point[0] + 2 * E, point[1])
    assert math.isclose(d1 + d2, 2, abs_tol=1e-12)
    p = project(point)
    other = project((-2 * E, 0))
    body = text(36, 52, "① 太阳不在椭圆中心", 30)
    body += text(36, 91, "教学模型：半长轴 a = 1，偏心率 e = 0.6", 23)
    body += path(orbit())
    body += line(*other, *p, GOLD) + line(480, 405, *p, GOLD)
    body += line(64, 405, 584, 405, "#9aa9b6", True)
    body += dot(*other, color=GOLD) + dot(324, 405, color=INK)
    body += dot(480, 405, 13, GOLD) + dot(*p, 9)
    body += text(108, 446, "另一焦点", 22)
    body += text(295, 446, "中心", 22)
    body += text(457, 446, "太阳", 22)
    body += text(470, 195, "行星 P", 23)
    body += text(189, 264, f"距离 2 = {d2:.1f}", 22, GOLD)
    body += text(320, 360, f"距离 1 = {d1:.1f}", 22, GOLD)
    body += line(324, 660, 584, 660, BLUE)
    body += text(454, 701, "半长轴 a = 1", 23, BLUE, "middle")
    body += text(36, 755, "近日点：距太阳 0.4；远日点：距太阳 1.6", 24)
    body += text(36, 797, "不管 P 在哪里，两焦点距离之和始终为 2a。", 24)
    body += text(36, 841, "轨道刻意画扁，方便观察；不代表地球的形状。", 22)
    save("orbit-geometry.svg", 880, "椭圆的中心、焦点和半长轴",
         "偏心率0.6的计算椭圆，太阳在焦点，点P到两焦点距离为0.7和1.3，和为2。", body)


def equal_time():
    body = text(36, 52, "② 等时间，不是等路程", 30)
    body += text(36, 91, "一圈用 8 秒演示；每个阴影区对应 T / 8", 23)
    areas, polygon_areas = [], []
    for midpoint, color in [(0, RED), (math.pi, BLUE)]:
        m1, m2 = midpoint - math.pi / 8, midpoint + math.pi / 8
        e1, e2 = eccentric_anomaly(m1), eccentric_anomaly(m2)
        areas.append(B * ((e2 - E * math.sin(e2)) - (e1 - E * math.sin(e1))) / 2)
        arc = [project(position(m1 + (m2 - m1) * i / 120)) for i in range(121)]
        polygon = [(480, 405), *arc, (480, 405)]
        polygon_area = abs(sum(
            x1 * y2 - y1 * x2
            for (x1, y1), (x2, y2) in zip(polygon, polygon[1:])
        )) / (2 * 260 ** 2)
        polygon_areas.append(polygon_area)
        assert abs(polygon_area - areas[-1]) < 3e-5
        body += (
            '<path d="M480,405 L'
            + " L".join(f"{x:.3f},{y:.3f}" for x, y in arc)
            + f' Z" fill="{color}" fill-opacity=".18" stroke="{color}" stroke-width="2"/>'
        )
    assert math.isclose(areas[0], areas[1], abs_tol=1e-12)
    assert math.isclose(areas[0], math.pi * B / 8, abs_tol=1e-12)
    assert math.isclose(math.sqrt(2 / (1 - E) - 1) / math.sqrt(2 / (1 + E) - 1), 4)
    body += path(orbit()) + dot(480, 405, 13, GOLD)
    labels = [
        (0, 596, 447, "0 / T"),
        (math.pi / 2, 107, 182, "T / 4"),
        (math.pi, 40, 447, "T / 2"),
        (3 * math.pi / 2, 109, 635, "3T / 4"),
    ]
    for mean, x, y, label in labels:
        body += dot(*project(position(mean)), 7) + text(x, y, label, 23)
    body += text(400, 446, "太阳", 22)
    body += '<circle class="traveller" cx="0" cy="0" r="11" fill="#b34039" stroke="white" stroke-width="3"/>'
    body += panel(690, 147)
    body += text(46, 729, "红区：近处，弧长大；蓝区：远处，弧长小", 23)
    body += text(46, 773, "两块弯曲扇形面积相等，都是整个椭圆的 1/8。", 23)
    body += text(46, 814, "近日点速度 / 远日点速度 = 1.6 / 0.4 = 4", 23)
    body += text(36, 883, "圆点标出四个等时刻；没有动画也能循点阅读。", 22)
    body += text(36, 924, "播放一次停回近日点；减少动态效果时只显示静态。", 22)
    frames = []
    max_residual = 0
    for i in range(961):
        p = project(position(TAU * i / 960))
        frames.append(f"{100*i/960:.6f}%{{transform:translate({p[0]:.4f}px,{p[1]:.4f}px)}}")
        if i < 960:
            p1, p2 = position(TAU * i / 960), position(TAU * (i + 1) / 960)
            x, y = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            max_residual = max(max_residual, abs((x + E) ** 2 + (y / B) ** 2 - 1))
    assert max_residual < 7e-5
    css = (
        ".traveller{transform:translate(584px,405px);animation:orbit 8s linear 1s 1 both}"
        "@keyframes orbit{" + "".join(frames) + "}"
        "@media(prefers-reduced-motion:reduce){.traveller{animation:none}}"
    )
    save("equal-time.svg", 963, "按开普勒方程计时的等面积轨道动画",
         "同一椭圆上两个T/8时段扫掠等面积；等时间采样解开普勒方程，近日点速度为远日点四倍。", body, css)
    print(f"Equal areas: {areas}; rendered polygon areas: {polygon_areas}; animation midpoint ellipse residual: {max_residual:.3g}")


def period_scale():
    body = text(36, 52, "③ 轨道放大，周期不只同比放大", 29)
    body += text(36, 94, "同一中心天体；以第一条轨道的 a、T 为单位", 23)
    for i, a in enumerate([1, 2, 4]):
        y = 142 + i * 172
        period = a ** 1.5
        assert math.isclose(period ** 2 / a ** 3, 1)
        body += panel(y, 148)
        body += text(46, y + 38, f"半长轴 a = {a}", 26)
        body += line(48, y + 70, 48 + a * 72, y + 70, BLUE)
        body += text(387, y + 45, f"周期 T ≈ {period:.3f}", 25, BLUE)
        body += text(387, y + 91, f"T² = {a**3}；a³ = {a**3}", 23)
        body += text(46, y + 127, "线段长度代表半长轴，不是行星直径。", 22)
    body += text(36, 710, "距离放大 4 倍 → 引力加速度变为 1/16", 24)
    body += text(36, 756, "圆轨道速度变为 1/2 → 绕一圈需要 8 倍时间", 24)
    body += text(36, 803, "上面的一般周期规律适用椭圆；末两行用圆解释。", 22)
    save("period-scale.svg", 845, "半长轴与周期的平方立方关系",
         "半长轴1、2、4，对应周期1、约2.828、8；同一中心质量下T平方除a立方为常数。", body)


def newton_motion():
    body = text(36, 52, "牛顿：速度怎么变，先看合力", 30)
    body += panel(115, 417)
    body += text(46, 155, "① 没有合力：沿切线直走，不必持续推着走", 24)
    body += f'<circle cx="275" cy="328" r="140" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    body += dot(275, 328, 14, GOLD) + dot(415, 328, 12)
    body += line(415, 328, 415, 210, INK, arrow=True)
    body += line(415, 328, 305, 328, RED, arrow=True)
    body += line(415, 210, 415, 185, INK, dash=True)
    body += text(449, 235, "速度 v", 24)
    body += text(319, 365, "引力 F", 24, RED)
    body += text(232, 367, "太阳", 22)
    body += text(46, 501, "② 有合力：F合 = ma；改方向，也属于加速", 24)
    body += panel(558, 314)
    body += text(46, 599, "③ 作用与反作用：同样大，作用在不同物体", 24)
    body += dot(180, 699, 40, GOLD) + dot(540, 699, 18)
    body += line(180, 699, 285, 699, RED, arrow=True)
    body += line(540, 699, 435, 699, RED, arrow=True)
    barycenter = (10 * 180 + 540) / 11
    assert math.isclose(10 * (barycenter - 180), 540 - barycenter)
    body += line(barycenter, 747, barycenter, 771, INK)
    body += text(128, 646, "质量 10", 24)
    body += text(494, 646, "质量 1", 24)
    body += text(128, 808, "共同质心偏向重者", 23)
    body += text(393, 808, "轻者加速度是 10 倍", 23)
    body += text(46, 852, "双物体质量比为教学模型，不是太阳与地球的比例。", 22)
    body += text(36, 917, "万有引力另给规则：距离加倍，力变为 1/4。", 24)
    body += text(36, 961, "箭头只标方向；上图长度不用于比较速度和力。", 22)
    save("newton-motion.svg", 1005, "惯性、受力转弯与作用反作用",
         "圆轨道速度沿切线，引力朝圆心。质量比10比1的两体受力相等，加速度不同，质心靠近重者。", body)


def calculus():
    body = text(36, 52, "微分看瞬间，积分把变化加回来", 29)
    body += text(36, 94, "玩具运动：t 以秒计，位置 s 的米数 = t²", 23)
    body += panel(120, 539)
    body += text(46, 162, "① 看位置曲线：两点割线 → 一点切线", 24)
    px = lambda t: 90 + 150 * t
    py = lambda s: 480 - 29 * s
    body += line(90, 480, 585, 480, arrow=True)
    body += line(90, 480, 90, 190, arrow=True)
    body += path([(px(t / 100), py((t / 100) ** 2)) for t in range(301)])
    body += path([(px(t), py(4 + 4 * (t - 2))) for t in [1.1, 2.9]], RED)
    body += line(px(2), py(4), px(3), py(9), GOLD, True)
    body += dot(px(2), py(4), 8) + dot(px(3), py(9), 7, GOLD)
    body += text(110, 211, "位置 / 米", 22)
    body += text(597, 489, "t / 秒", 22)
    body += text(354, 406, "(2, 4)", 22)
    body += text(555, 228, "(3, 9)", 22)
    body += text(46, 539, "从第 2 秒看：平均速度随区间缩短而逼近", 23)
    body += text(46, 583, "1 秒：5 → 0.1 秒：4.1 → 0.01 秒：4.01", 23, GOLD)
    body += text(46, 629, "切线斜率 = 第 2 秒的瞬时速度 = 4 米/秒", 24, RED)
    body += panel(685, 455)
    body += text(46, 729, "② 看速度曲线：窄条面积 → 累积位移", 24)
    for count, x0 in [(4, 82), (8, 400)]:
        y0, w, h = 977, 224, 172
        dt = 2 / count
        left_sum = sum(2 * i * dt * dt for i in range(count))
        right_sum = sum(2 * (i + 1) * dt * dt for i in range(count))
        assert left_sum < 4 < right_sum
        for i in range(count):
            height = h * i / count
            body += (
                f'<rect x="{x0+w*i/count:.3f}" y="{y0-height:.3f}" '
                f'width="{w/count:.3f}" height="{height:.3f}" '
                'fill="#d0e7ef" stroke="#176786" stroke-width="1"/>'
            )
        body += line(x0, y0, x0 + w + 13, y0, arrow=True)
        body += line(x0, y0, x0, y0 - h - 15, arrow=True)
        body += line(x0, y0, x0 + w, y0 - h, RED)
        body += text(x0 + 13, 781, f"{count} 份；v / (米/秒)", 22)
        body += text(x0 - 23, y0 - h + 8, "4", 20)
        body += text(x0 - 20, 1008, "0", 22)
        body += text(x0 + w - 24, 1008, "2秒", 22)
        body += text(x0 + 8, 1047, f"左端矩形和 = {left_sum:g} 米", 22, BLUE)
    body += text(46, 1100, "速度—时间图下面积：½ × 2秒 × 4米/秒 = 4米", 23)
    body += text(36, 1189, "两张图用的是同一次运动，纵轴不同，不能混读。", 22)
    body += text(36, 1230, "此例始终向前；若倒退，积分算位移而非总路程。", 22)
    save("calculus-zoom.svg", 1273, "同一次运动中的导数和积分",
         "位置为t平方，2秒时速度为4米每秒。速度为2t，0到2秒的位移为4米；左端矩形和由3米到3.5米趋近4米。", body)


def verlet(count):
    step = TAU / count
    x, y, vx, vy = 1 - E, 0.0, 0.0, math.sqrt((1 + E) / (1 - E))
    points = [(x, y)]
    for _ in range(count):
        r = math.hypot(x, y)
        ax, ay = -x / r ** 3, -y / r ** 3
        nx, ny = x + vx * step + ax * step ** 2 / 2, y + vy * step + ay * step ** 2 / 2
        nr = math.hypot(nx, ny)
        nax, nay = -nx / nr ** 3, -ny / nr ** 3
        vx, vy = vx + step * (ax + nax) / 2, vy + step * (ay + nay) / 2
        x, y = nx, ny
        assert abs(x * vy - y * vx - B) < 1e-12
        points.append((x, y))
    error = math.hypot(x - (1 - E), y)
    return points, error


def numerical():
    body = text(36, 52, "电脑怎样从引力，一步步算出轨道？", 29)
    body += text(36, 94, "同一初值；只算一个真实周期 T = 2π", 23)
    errors = []
    for i, count in enumerate([100, 200, 400]):
        y = 124 + i * 249
        body += panel(y, 227)
        cy = y + 116
        exact = [(240 + 88 * p[0], cy - 88 * p[1]) for p in (position(TAU * k / 960) for k in range(961))]
        points, error = verlet(count)
        errors.append(error)
        body += path(exact, "#8795a4", 3, True)
        body += path([(240 + 88 * x, cy - 88 * z) for x, z in points], BLUE)
        body += dot(240, cy, 9, GOLD)
        body += dot(240 + 88 * points[-1][0], cy - 88 * points[-1][1], 6, RED)
        body += text(382, y + 50, f"分成 {count} 步", 27)
        body += text(382, y + 98, f"步长 Δt = T / {count}", 23)
        body += text(382, y + 145, f"终点误差 ≈ {error:.4f} a", 23, RED)
        body += text(46, y + 207, "虚线：解析椭圆；实线：数值路径；红点：计算终点", 21)
    assert 3.8 < errors[0] / errors[1] < 4.1
    assert 3.8 < errors[1] / errors[2] < 4.1
    body += text(36, 926, "步长减半，终点位置误差在此例约缩为 1/4。", 24)
    body += text(36, 971, "速度 Verlet 法；不是“画得像”就算计算准确。", 23)
    body += text(36, 1014, "无量纲单位：a = 1，GM = 1；初始偏心率 0.6。", 22)
    save("numerical-orbit.svg", 1056, "数值积分的步长收敛对比",
         "速度Verlet法把一个周期分为100、200、400步，终点位置误差约0.5270、0.1361、0.0338个半长轴。", body)
    print("Velocity Verlet return-position errors:", errors)


def transfer():
    radius = 1.52
    a = (1 + radius) / 2
    e = (radius - 1) / (radius + 1)
    b = a * math.sqrt(1 - e * e)
    time = a ** 1.5 / 2
    phase = math.pi - TAU * time / radius ** 1.5
    assert math.isclose(a * (1 - e), 1)
    assert math.isclose(a * (1 + e), radius)
    cx, cy, scale = 360, 419, 180
    body = text(36, 52, "应用：去火星，不是朝它现在的位置飞", 28)
    body += text(36, 93, "把两行星轨道近似成同平面圆：1 与 1.52 AU", 23)
    for r, color in [(1, BLUE), (radius, "#8795a4")]:
        body += f'<circle cx="{cx}" cy="{cy}" r="{r*scale}" fill="none" stroke="{color}" stroke-width="3"/>'
    transfer_points = [
        (cx + scale * (a * math.cos(math.pi * k / 300) - a * e),
         cy - scale * b * math.sin(math.pi * k / 300))
        for k in range(301)
    ]
    body += path(transfer_points, RED, 5)
    body += dot(cx, cy, 13, GOLD)
    body += dot(cx + scale, cy, 10)
    start = (cx + scale * radius * math.cos(phase), cy - scale * radius * math.sin(phase))
    end = (cx - scale * radius, cy)
    body += dot(*start, 10, GOLD) + dot(*end, 10, RED)
    body += text(443, 465, "出发点", 23, BLUE)
    body += text(531, 202, "火星起点", 22, GOLD)
    body += text(33, 465, "相遇点", 23, RED)
    body += text(332, 465, "太阳", 22)
    body += text(234, 320, "红色半椭圆：转移段", 23, RED)
    body += panel(735, 180)
    body += text(46, 776, f"半长轴 = (1 + 1.52) / 2 = {a:.2f} AU", 24)
    body += text(46, 823, f"半个周期 ≈ {time:.3f} 年 ≈ {time*365.25:.0f} 天", 25, RED)
    body += text(46, 871, f"此模型发射时，火星须在前方约 {math.degrees(phase):.1f}°。", 23)
    body += text(36, 960, "只算绕日转移段，不含离地、入轨和着陆。", 23)
    body += text(36, 1003, "真实轨道有偏心率、倾角与摄动，不是任务时刻表。", 22)
    save("mars-transfer.svg", 1046, "地球至火星的理想化霍曼转移",
         "1AU和1.52AU同平面圆轨道之间的半椭圆转移，半长轴1.26AU，约258天。火星初始领先约44.1度。", body)
    print(f"Ideal transfer: {time*365.25:.6f} days; launch phase {math.degrees(phase):.6f} degrees")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    geometry()
    equal_time()
    period_scale()
    newton_motion()
    calculus()
    numerical()
    transfer()
    print(f"Generated seven diagrams in {OUT}")


if __name__ == "__main__":
    main()
