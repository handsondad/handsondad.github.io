"""Celestial Mechanics, Physical Curves & Analytical Mechanics visual builders."""

import math
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET
import bisect

from .core import (
    BG,
    BLUE,
    BLUE_LINE,
    BLUE_SOFT,
    BODY,
    BORDER,
    CARD_BG,
    DISP_SCALE,
    GREEN,
    GREEN_SOFT,
    HAIRLINE,
    IMAGES_ROOT,
    INK,
    K_BLUE,
    K_GOLD,
    K_INK,
    K_MUTED,
    K_ORANGE,
    K_RED,
    LABEL_SIZE,
    MUTED,
    NOTE_SIZE,
    ORANGE,
    ORANGE_SOFT,
    PANEL_TITLE,
    PURPLE,
    PURPLE_SOFT,
    REPO_ROOT,
    SLATE,
    SLATE_SOFT,
    SUB_SIZE,
    TITLE_SIZE,
    WIDTH,
    b_document,
    card,
    figure,
    header,
    k_dot,
    k_line,
    k_panel,
    k_path,
    k_save,
    k_text,
    pill,
    register,
    step_badge,
    txt,
)


@register("kepler-newton", "开普勒与牛顿：椭圆面积律、周期律、Verlet 积分与霍曼转移", "mechanics_sky")
def build_kepler_newton():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = lambda name, height, title, description, body, css="", output_directory=None: k_save(name, height, title, description, body, css, OUT if output_directory is None else output_directory)

    OUT = REPO_ROOT / "assets" / "images" / "kepler-newton"

    TAU = 2 * math.pi

    E = 0.6

    B = math.sqrt(1 - E * E)

    INK, BLUE, RED, GOLD = "#172b45", "#176786", "#b34039", "#b77a09"

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

    main()


@register("calculus-gravity", "微积分与万有引力：月地检验、微重力、逃逸功与轨道命运", "mechanics_sky")
def build_calculus_gravity():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "calculus-gravity"

    MU = 398600.435507  # JPL DE440 Earth GM, km^3/s^2.

    EARTH_RADIUS = 6370.0

    MOON_DISTANCE = 384400.0

    MOON_PERIOD = 27.3 * 86400

    TAU = 2 * math.pi

    def write(name, height, title, description, body, css=""):
        save(name, height, title, description, body, css, output_directory=OUT)

    def moon_fall():
        surface_g = 1000 * MU / EARTH_RADIUS ** 2
        moon_g = 1000 * MU / MOON_DISTANCE ** 2
        observed = 1000 * TAU ** 2 * MOON_DISTANCE / MOON_PERIOD ** 2
        ratio = MOON_DISTANCE / EARTH_RADIUS
        assert math.isclose(surface_g / moon_g, ratio ** 2, rel_tol=1e-12)
        assert abs(observed / moon_g - 1) < .012
        body = text(36, 52, "苹果与月亮：同一个引力，不同的尺度", 29)
        body += text(36, 94, "下面的地月距离与天体直径，使用同一长度比例", 23)
        scale = 550 / MOON_DISTANCE
        body += line(90, 210, 640, 210, "#8295a5", True)
        body += dot(90, 210, EARTH_RADIUS * scale)
        body += dot(640, 210, 1740 * scale, GOLD)
        body += text(65, 169, "地球", 24)
        body += text(602, 169, "月亮", 24)
        body += text(330, 255, "约 384,400 千米", 24, INK, "middle")
        body += text(36, 304, "月亮很小并非漏画；距离约为 60.3 个地球半径。", 23)
        body += panel(338, 179)
        body += text(46, 378, f"① 地表附近：每秒的速度变化约 {surface_g:.2f} 米/秒", 24)
        body += text(46, 427, f"从静止自由落下 1 秒，约下降 {surface_g / 2:.2f} 米。", 26, BLUE)
        body += text(46, 479, "忽略空气阻力；只看靠近地表的短时间。", 23)
        body += panel(544, 194)
        body += text(46, 585, "② 月球距离处：地球的引力加速度", 25)
        body += text(46, 634, f"约 {moon_g:.5f} 米/秒²；1 秒约偏离切线 {500 * moon_g:.2f} 毫米", 23, GOLD)
        body += text(46, 684, f"从月球轨道反算：约 {observed:.5f} 米/秒²", 24)
        body += text(46, 718, "两个估计接近，但不是高精度月球模型。", 22)
        body += text(36, 791, "注意：这里不是月亮表面约 1.6 米/秒²的自身重力。", 22, RED)
        body += text(36, 836, "“下落”是相对惯性切线弯曲，不是轨道半径持续缩小。", 22)
        write("moon-and-apple.svg", 879, "苹果和月球运动的引力数量级比较",
              "地月图按统一比例，地球半径6370千米，地月平均距离384400千米。地球在月球距离处的引力加速度约0.00270米每二次方秒。", body)
        print(f"Moon: gravity={moon_g:.10f}, circular estimate={observed:.10f} m/s^2")

    def microgravity():
        radius = EARTH_RADIUS + 400
        ratio = (EARTH_RADIUS / radius) ** 2
        g = 1000 * MU / radius ** 2
        speed = math.sqrt(MU / radius)
        period = TAU * math.sqrt(radius ** 3 / MU) / 60
        escape_speed = math.sqrt(2 * MU / radius)
        assert .885 < ratio < .886
        assert math.isclose(speed ** 2 / radius * 1000, g, rel_tol=1e-12)
        assert math.isclose(escape_speed / speed, math.sqrt(2), rel_tol=1e-12)
        assert 10.85 < escape_speed < 10.86
        body = text(36, 52, "漂浮，不等于引力消失", 30)
        body += text(36, 95, "取高度 400 千米；地球近似为不自转的球体", 23)
        body += panel(126, 214)
        body += text(46, 168, "地表引力：100%", 25)
        body += '<rect x="48" y="190" width="580" height="24" rx="5" fill="#d9e3ea"/>'
        body += '<rect x="48" y="190" width="580" height="24" rx="5" fill="#176786"/>'
        body += text(46, 252, f"400 千米处：{ratio * 100:.1f}%（约 {g:.2f} 米/秒²）", 25)
        body += f'<rect x="48" y="274" width="{580*ratio:.3f}" height="24" rx="5" fill="#b77a09"/>'
        for x, label in [(42, "① 有支撑"), (378, "② 一起自由落体")]:
            body += text(x + 16, 391, label, 26)
            body += f'<rect x="{x}" y="415" width="295" height="275" rx="14" fill="white" stroke="#8295a5" stroke-width="2"/>'
            body += dot(x + 145, 490, 17)
            body += line(x + 145, 508, x + 145, 574, BLUE)
            body += line(x + 145, 535, x + 111, 551, BLUE)
            body += line(x + 145, 535, x + 179, 551, BLUE)
            body += line(x + 145, 574, x + 116, 620, BLUE)
            body += line(x + 145, 574, x + 174, 620, BLUE)
            body += line(x + 77, 622, x + 209, 622, INK)
            body += line(x + 195, 520, x + 195, 586, RED, arrow=True)
            body += text(x + 211, 572, "引力", 22, RED)
            if x == 42:
                body += line(x + 91, 606, x + 91, 539, GOLD, arrow=True)
                body += text(x + 9, 500, "支撑", 22, GOLD)
                body += text(x + 42, 665, "秤有读数", 24)
            else:
                body += line(x + 312, 485, x + 312, 560, RED, arrow=True)
                body += text(x + 42, 665, "秤的支撑读数≈0", 23)
        body += text(46, 757, "右图的人、物体与舱体共同自由落体；房间不按比例。", 22)
        body += panel(787, 165)
        body += text(46, 829, f"同高度的理想圆轨道：速度约 {speed:.2f} 千米/秒", 24)
        body += text(46, 875, f"绕地球一圈约 {period:.1f} 分钟；不需要引力被抵消。", 23)
        body += text(46, 922, "真实空间站有阻力、振动与潮汐差，并非完美失重。", 22)
        write("microgravity.svg", 989, "轨道上的强引力与微重力",
              "400千米高度的地球引力约为地表88.5%。比较受支撑的人和共同自由落体的人，秤的读数是支撑力而非引力是否存在。", body)
        print(f"400 km: gravity ratio={ratio:.10f}, speed={speed:.10f} km/s, period={period:.10f} min")

    def vector_motion():
        cx, cy, radius = 330, 396, 165
        body = text(36, 52, "距离不变，为什么仍然有速度和加速度？", 28)
        body += text(36, 94, "黑箭头：切向速度 v；红箭头：向心加速度 a", 23)
        body += f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#8295a5" stroke-width="3"/>'
        body += dot(cx, cy, 18, GOLD)
        body += text(294, 445, "地心", 24)
        for angle, x, y, label in [
            (math.pi / 2, 289, 211, "T / 4"),
            (math.pi, 77, 406, "T / 2"),
            (3 * math.pi / 2, 290, 602, "3T / 4"),
        ]:
            body += dot(cx + radius * math.cos(angle), cy - radius * math.sin(angle), 5)
            body += text(x, y, label, 23)
        body += text(531, 411, "0 / T", 23)
        body += '<g class="orbit-marker">'
        body += line(cx + radius, cy, cx + radius, cy - 100, INK, arrow=True)
        body += line(cx + radius, cy, cx + radius - 90, cy, RED, arrow=True)
        body += f'<circle data-role="moving-body" cx="{cx+radius}" cy="{cy}" r="11" fill="#176786" stroke="white" stroke-width="3"/>'
        body += '</g>'
        body += panel(643, 179)
        body += text(46, 684, "① 微分位置向量 → 速度：沿轨道切线", 25)
        body += text(46, 733, "② 再微分速度向量 → 加速度：指向地心", 25)
        body += text(46, 780, "只把“距地心的距离”求导，会丢掉转向的信息。", 23)
        body += text(36, 869, "教学圆轨道：8 秒映射一圈，箭头始终保持几何约束。", 22)
        body += text(36, 914, "只播放一次停回初态；减少动态效果时保留静态箭头。", 22)
        css = (
            f".orbit-marker{{transform-origin:{cx}px {cy}px;animation:turn 8s linear 1s 1 both}}"
            "@keyframes turn{from{transform:rotate(0deg)}to{transform:rotate(-360deg)}}"
            "@media(prefers-reduced-motion:reduce){.orbit-marker{animation:none}}"
        )
        for i in range(65):
            t = TAU * i / 64
            r = (math.cos(t), math.sin(t))
            v = (-math.sin(t), math.cos(t))
            a = (-math.cos(t), -math.sin(t))
            assert abs(sum(x * y for x, y in zip(r, v))) < 1e-12
            assert math.isclose(math.hypot(*v), 1)
            assert math.isclose(sum(x * y for x, y in zip(r, a)), -1)
        write("differentiate-motion.svg", 958, "圆周运动中的位置、速度和加速度向量",
              "圆轨道半径不变，速度向量沿切线，加速度向量指向地心。动画旋转整个向量组，几何方向约束始终成立。", body, css)

    def verlet_step(position, velocity, step):
        r = math.hypot(*position)
        acceleration = tuple(-x / r ** 3 for x in position)
        new_position = tuple(x + v * step + .5 * a * step ** 2
                             for x, v, a in zip(position, velocity, acceleration))
        nr = math.hypot(*new_position)
        new_acceleration = tuple(-x / nr ** 3 for x in new_position)
        new_velocity = tuple(v + .5 * (a + na) * step
                             for v, a, na in zip(velocity, acceleration, new_acceleration))
        return new_position, new_velocity

    def check_integration():
        results = []
        for count in [200, 400, 800]:
            r, v = (1., 0.), (0., 1.)
            max_energy_error = 0.
            for _ in range(count):
                r, v = verlet_step(r, v, TAU / count)
                assert abs(r[0] * v[1] - r[1] * v[0] - 1) < 1e-12
                energy = sum(x * x for x in v) / 2 - 1 / math.hypot(*r)
                max_energy_error = max(max_energy_error, abs(energy + .5))
            assert max_energy_error < 1e-6
            results.append(math.hypot(r[0] - 1, r[1]))
        assert 3.9 < results[0] / results[1] < 4.1
        assert 3.9 < results[1] / results[2] < 4.1
        print("Circle integration return errors:", results)

    def calculate_next():
        dt = .2
        r, v = verlet_step((1., 0.), (0., 1.), dt)
        assert r == (.98, .2)
        error = math.hypot(r[0] - math.cos(dt), r[1] - math.sin(dt))
        assert error < .00134
        body = text(36, 52, "把“这一刻的引力”接到“下一刻的位置”", 28)
        body += text(36, 94, "归一化教学算例：GM = 1；一步时间 Δt = 0.2", 23)
        rows = [
            ("① 读入初始条件", "位置 (1, 0)；速度 (0, 1)", "知道在哪，还必须知道朝哪里、以多快在动。"),
            ("② 按距离与方向计算引力", "此刻加速度 a₀ = (-1, 0)", "箭头朝地心；不是只记一个“引力大小”。"),
            ("③ 用短时间近似推进位置", "新位置≈(0.98000, 0.20000)", "位置增量：v₀ Δt + ½ a₀ Δt²"),
            ("④ 新位置重算引力，再更新速度",
             f"新速度≈({v[0]:.5f}, {v[1]:.5f})", "使用步首与步尾加速度的平均值更新。"),
        ]
        for i, (title, value, note) in enumerate(rows):
            y = 131 + i * 199
            body += panel(y, 170)
            body += text(46, y + 39, title, 25)
            body += text(46, y + 87, value, 25, BLUE)
            body += text(46, y + 132, note, 22)
            if i < 3:
                body += line(360, y + 174, 360, y + 190, GOLD, arrow=True)
        body += text(36, 981, "解析圆轨道同一时刻：(0.98007, 0.19867)", 24)
        body += text(36, 1027, "并不完全相同！有限步长算法是近似，不是微积分本身。", 22, RED)
        body += text(36, 1072, "采用速度 Verlet 法；单位经过缩放，不是秒与千米。", 22)
        write("calculate-next.svg", 1114, "速度Verlet法推进一个短时间步的示例",
              "初始位置1和0、速度0和1，引力参数为1，时间步0.2。先估计新位置0.98和0.20，再重算引力更新速度，并与解析圆轨道比较。", body)
        check_integration()

    def escape_work():
        body = text(36, 52, "走到无限远，为什么只需有限的能量？", 29)
        body += text(36, 94, "横轴 u = r / r₀；纵轴 f = F / F₀ = 1 / u²", 23)
        px = lambda u: 102 + (u - 1) * 72
        py = lambda f: 491 - 290 * f
        colors = [BLUE, GOLD, RED]
        intervals = [(1, 2), (2, 4), (4, 8)]
        for (lo, hi), color in zip(intervals, colors):
            pts = [(px(lo), py(0))]
            pts += [(px(lo + (hi - lo) * i / 120), py(1 / (lo + (hi - lo) * i / 120) ** 2))
                    for i in range(121)]
            pts += [(px(hi), py(0))]
            rendered_points = [(round(x, 3), round(y, 3)) for x, y in pts]
            twice_area = sum(x * ny - nx * y
                             for (x, y), (nx, ny) in
                             zip(rendered_points, rendered_points[1:] + rendered_points[:1]))
            rendered_integral = abs(twice_area) / (2 * 72 * 290)
            assert math.isclose(rendered_integral, 1 / lo - 1 / hi, rel_tol=5e-5)
            d = "M" + " L".join(f"{x:.3f},{y:.3f}" for x, y in pts) + " Z"
            body += f'<path d="{d}" fill="{color}" fill-opacity=".19"/>'
        body += line(102, 491, 643, 491, arrow=True)
        body += line(102, 491, 102, 160, arrow=True)
        body += path([(px(1 + 7 * i / 500), py(1 / (1 + 7 * i / 500) ** 2))
                      for i in range(501)], INK)
        for u in [1, 2, 4, 8]:
            body += text(px(u), 531, str(u), 23, anchor="middle")
        body += text(40, 205, "1", 22)
        body += text(41, 425, "1/4", 22)
        body += text(123, 171, "f", 24)
        body += text(646, 531, "u", 24)
        body += text(315, 288, "曲线下面积 = 力 × 位移的累积", 22)
        body += text(315, 334, "8 以后的尾巴没有画完，不能当成 0。", 22, RED)
        body += panel(570, 296)
        fractions = [1 / lo - 1 / hi for lo, hi in intervals] + [1 / 8]
        assert math.isclose(sum(fractions), 1)
        for i, (label, fraction) in enumerate(zip(["r₀ → 2r₀", "2r₀ → 4r₀", "4r₀ → 8r₀", "8r₀ → 无限远"], fractions)):
            body += text(46, 610 + 63 * i, label, 24)
            body += text(350, 610 + 63 * i, f"全部能量的 {fraction * 100:g}%", 24,
                         [BLUE, GOLD, RED, INK][i])
        body += text(36, 919, "合计：50% + 25% + 12.5% + 12.5% = 100%", 24)
        body += text(36, 965, "越远引力越弱；无穷多个贡献的和，可能仍然有限。", 22)
        write("escape-work.svg", 1008, "反平方引力的积分与有限逃逸能量",
              "归一化引力曲线1除u平方，距离从1到2、2到4、4到8和8到无穷远的功，分别占总逃逸能量50%、25%、12.5%、12.5%。", body)

    def conic_points(speed, end_angle, count=600):
        signed_e = speed ** 2 - 1
        angular_momentum = speed
        energy = speed ** 2 / 2 - 1
        points = []
        for i in range(count + 1):
            angle = end_angle * i / count
            radius = speed ** 2 / (1 + signed_e * math.cos(angle))
            position = (radius * math.cos(angle), radius * math.sin(angle))
            radial_speed = signed_e * math.sin(angle) / angular_momentum
            transverse_speed = angular_momentum / radius
            vx = radial_speed * math.cos(angle) - transverse_speed * math.sin(angle)
            vy = radial_speed * math.sin(angle) + transverse_speed * math.cos(angle)
            assert abs((vx * vx + vy * vy) / 2 - 1 / radius - energy) < 1e-12
            assert abs(position[0] * vy - position[1] * vx - angular_momentum) < 1e-12
            points.append(position)
        assert math.isclose(points[0][0], 1)
        return points

    def different_fates():
        body = text(36, 52, "同一个引力，换个初速度就换一种命运", 28)
        body += text(36, 94, "同位置，全部沿切线出发；k = 初速度 / 当地圆轨道速度", 22)
        planet_radius = .75
        cases = [
            (.65, "① 撞向天体", "速度偏小，路径与地表相交"),
            (1., "② 圆轨道", "每一处都保持相同的地心距离"),
            (1.2, "③ 椭圆轨道", "升到更远处，再绕回来"),
            (1.6, "④ 双曲线逃逸", "仍被引力拉弯，但不再返回"),
        ]
        for i, (speed, label, note) in enumerate(cases):
            y = 127 + i * 245
            cx, cy, scale = 227, y + 124, 40
            if speed < 1:
                end = math.acos((speed ** 2 / planet_radius - 1) / (speed ** 2 - 1))
            elif speed <= math.sqrt(2):
                end = TAU
            else:
                end = math.acos((speed ** 2 / 2.5 - 1) / (speed ** 2 - 1))
            points = conic_points(speed, end)
            assert all(20 < cy - scale * z - y < 201 for _, z in points)
            if speed < 1:
                assert math.isclose(math.hypot(*points[-1]), planet_radius)
            if 1 <= speed < math.sqrt(2):
                assert math.hypot(points[-1][0] - 1, points[-1][1]) < 1e-12
            body += panel(y, 221)
            body += dot(cx, cy, planet_radius * scale, "#d1e2e9")
            body += dot(cx, cy, 5, GOLD)
            body += path([(cx + scale * x, cy - scale * z) for x, z in points], BLUE, 4)
            body += dot(cx + scale, cy, 6, RED)
            body += line(cx + scale, cy, cx + scale, cy - 30, INK, arrow=True)
            body += text(378, y + 45, label, 27)
            body += text(378, y + 94, f"k = {speed:g}", 23)
            body += text(378, y + 136, note, 21)
            if speed > math.sqrt(2):
                p1, p2 = points[-4], points[-1]
                body += line(cx + scale * p1[0], cy - scale * p1[1],
                             cx + scale * p2[0], cy - scale * p2[1], BLUE, arrow=True)
        body += text(36, 1118, "淡色圆：天体地表；红点：共同出发位置；箭头：初速度", 21)
        body += text(36, 1154, "图按同一长度尺度构造，天体半径为出发半径的 0.75。", 22)
        body += text(36, 1197, "开放轨道仅画可见的一段；不是“离开图框就没有引力”。", 22)
        body += text(36, 1241, "图是归一化两体模型，不对应真实空间站高度或任务。", 22)
        write("orbit-fates.svg", 1285, "改变切向初速度产生碰撞、圆轨道、椭圆与双曲线",
              "出发位置相同，初速度为当地圆轨道速度的0.65、1、1.2、1.6倍。四条路径由反平方引力圆锥曲线方程构造，并核对能量和角动量。", body)

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        moon_fall()
        microgravity()
        vector_motion()
        calculate_next()
        escape_work()
        different_fates()
        print(f"Generated six diagrams in {OUT}")

    main()


@register("laplace", "拉普拉斯天体力学：摄动残差、近共振、引力势与可预测边界", "mechanics_sky")
def build_laplace():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "laplace"

    GM = 1.32712440041279419e20 * (365.25 * 86400) ** 2 / 149597870700 ** 3

    MASS = (1, 126712764.1 / 1.32712440041279419e11, 37940584.8418 / 1.32712440041279419e11)

    RADII = (5.202887, 9.53667594)

    NJ = 3034.90371757 / 36000

    NS = 1222.11494724 / 36000

    BEAT = 1 / abs(2 * NJ - 5 * NS)

    def write(name, height, title, description, body, css=""):
        save(name, height, title, description, body, css, output_directory=OUT)

    def heading(number, title):
        return text(36, 49, f"{number} {title}", 29)

    def rows(x, y, values, size=23, step=36, color=INK):
        return "".join(text(x, y + i * step, value, size, color) for i, value in enumerate(values))

    def initial(factor):
        masses = [MASS[0], MASS[1] * factor, MASS[2] * factor]
        state = [[0., 0., 0., 0.]]
        for radius, angle, mass in zip(RADII, (0, math.pi / 3), masses[1:]):
            speed = math.sqrt(GM * (1 + mass) / radius)
            state.append([radius * math.cos(angle), radius * math.sin(angle),
                          -speed * math.sin(angle), speed * math.cos(angle)])
        for k in range(4):
            mean = sum(m * p[k] for m, p in zip(masses, state)) / sum(masses)
            for p in state:
                p[k] -= mean
        return masses, state

    def accelerations(state, masses):
        a = [[0., 0.] for _ in state]
        for i in range(3):
            for j in range(i + 1, 3):
                dx, dy = state[j][0] - state[i][0], state[j][1] - state[i][1]
                r = math.hypot(dx, dy)
                assert r > .1, "Teaching model encountered a close approach"
                for k, delta in enumerate((dx, dy)):
                    a[i][k] += GM * masses[j] * delta / r ** 3
                    a[j][k] -= GM * masses[i] * delta / r ** 3
        return a

    def energy(state, masses):
        value = sum(m * (p[2] ** 2 + p[3] ** 2) / 2 for m, p in zip(masses, state))
        for i in range(3):
            for j in range(i + 1, 3):
                value -= GM * masses[i] * masses[j] / math.dist(state[i][:2], state[j][:2])
        return value

    def simulate(factor=1, dt=.0025):
        masses, state = initial(factor)
        e0 = energy(state, masses)
        a = accelerations(state, masses)
        frames, max_error = [], 0
        count = round(120 / dt)
        stride = round(.5 / dt)
        for step in range(count + 1):
            if step % stride == 0:
                t = step * dt
                dx, dy = state[1][0] - state[0][0], state[1][1] - state[0][1]
                phase = math.atan2(dy, dx) - math.sqrt(GM * (1 + masses[1]) / RADII[0] ** 3) * t
                residual = math.atan2(math.sin(phase), math.cos(phase)) * 180 / math.pi
                frames.append((t, dx, dy, residual))
                max_error = max(max_error, abs((energy(state, masses) - e0) / e0))
            if step == count:
                break
            for p, force in zip(state, a):
                for k in range(2):
                    p[k] += p[k + 2] * dt + force[k] * dt ** 2 / 2
                    p[k + 2] += force[k] * dt / 2
            a = accelerations(state, masses)
            for p, force in zip(state, a):
                for k in range(2):
                    p[k + 2] += force[k] * dt / 2
        assert max_error < 2e-6
        for k in range(4):
            assert abs(sum(m * p[k] for m, p in zip(masses, state))) < 1e-10
        return frames, max_error

    def history():
        body = heading("①", "一条引力定律，为什么需要几代人？")
        entries = [
            ("1687", "牛顿", "给出运动定律与万有引力。"),
            ("18 世纪", "欧拉、拉格朗日等", "发展分析方法与摄动计算。"),
            ("1780 年代", "拉普拉斯", "解释木星、土星的长周期偏差。"),
            ("1799 起", "《天体力学》", "前两卷出版，全书共五卷。"),
            ("19 世纪末", "庞加莱", "揭示三体问题远比想象复杂。"),
            ("今天", "观测与数值积分", "精密星历与长期统计研究并行。"),
        ]
        for i, (year, name, detail) in enumerate(entries):
            y = 85 + i * 120
            body += panel(y, 103)
            body += text(48, y + 34, year, 24, BLUE)
            body += text(242, y + 34, name, 25)
            body += text(48, y + 77, detail, 23)
        body += text(36, 842, "年份是研究与出版路标，不是一人接替一人的完整名单。", 22)
        write("history.svg", 880, "从牛顿到现代星历的天体力学路标",
              "六个历史路标说明拉普拉斯连接牛顿引力、分析计算与可检验的天文预报；并未证明永远稳定。", body)

    def differential():
        body = heading("②", "土星拉木星，也拉着太阳")
        body += rows(36, 91, ["只看日心位置时，要扣除太阳本身的加速度。", "下面采用同一直线上的构型，距离按比例画。"], 23)
        scale, ox, y = 53, 90, 300
        jx, sx = ox + scale * RADII[0], ox + scale * RADII[1]
        body += line(ox, y, sx, y, "#a2b4c2", True)
        body += dot(ox, y, 15, GOLD) + dot(jx, y, 11, BLUE) + dot(sx, y, 12, RED)
        body += text(ox, 348, "太阳", 24, INK, "middle")
        body += text(jx, 348, "木星 J", 24, INK, "middle")
        body += text(sx, 348, "土星 S", 24, INK, "middle")
        a_sun = GM * MASS[2] / RADII[1] ** 2
        a_jup = GM * MASS[2] / (RADII[1] - RADII[0]) ** 2
        ratio = a_jup / a_sun
        body += line(ox, 238, ox + 32, 238, RED, arrow=True)
        body += line(jx, 238, jx + 32 * ratio, 238, RED, arrow=True)
        body += text(36, 197, "土星引起的加速度：1 份", 22)
        body += text(345, 197, f"加速度：{ratio:.2f} 份", 22)
        body += panel(400, 257)
        body += rows(48, 443, ["① 木星确实被土星向右拉。", "② 太阳也被土星向右拉，但加速度较小。", "③ 木星相对太阳的额外加速度＝两者之差。"], 24, 48)
        body += text(48, 624, "图中红箭头表示加速度，长度按同一倍率绘制。", 22)
        body += text(36, 706, "不是所有“行星受到的力”，都能直接当日心方程的项。", 22)
        assert 4.8 < ratio < 4.9
        write("relative-pull.svg", 750, "日心摄动需要直接项和间接项",
              f"共线教学构型中，土星对木星的加速度约为对太阳的{ratio:.2f}倍；两者都向土星，日心额外加速度为差。", body)

    def residuals(data):
        body = heading("③", "椭圆是起点，偏差才是线索")
        body += rows(36, 91, ["同一组人工初始位置与速度，积分 120 年。", "比较：三体木星方向 − 独立二体基线方向。"], 23)
        ox, oy, sx, sy = 100, 230, 4.5, 32
        body += line(ox, 565, 655, 565, INK, arrow=True)
        body += line(ox, 565, ox, 190, INK, arrow=True)
        for val in (-10, -8, -6, -4, -2, 0):
            yy = oy - val * sy
            body += line(ox, yy, 640, yy, "#d5dfe6", True)
            body += text(83, yy + 7, val, 21, INK, "end")
        for t in (0, 40, 80, 120):
            body += text(ox + t * sx, 605, t, 21, INK, "middle")
        body += text(116, 199, "方向偏差 / 度", 22)
        body += text(574, 636, "时间 / 年", 22)
        for factor, color in [(10, GOLD), (1, BLUE)]:
            body += path([(ox + t * sx, oy - v * sy) for t, _, _, v in data[factor]], color, 3, factor == 10)
        body += panel(662, 159)
        body += rows(48, 702, ["蓝实线：采用真实数量级的行星质量。", "金虚线：两颗行星质量都乘 10，方便比较。", "相同坐标轴；不是实测误差，也不是当前星历。"], 23, 43)
        write("perturbation-residual.svg", 855, "三体积分相对独立二体基线的方向偏差",
              "采用人工共面近圆初值；太阳也参与运动。横轴0至120年，纵轴木星方向偏差，真实质量与十倍行星质量用同一尺度比较。", body)

    def resonance():
        tj, ts = 1 / NJ, 1 / NS
        body = heading("④", "快钟差一点，慢拍慢很多")
        body += rows(36, 91, ["冻结频率的教学模型，不是逐年精密星历。", f"木星 5 圈：{5*tj:.2f} 年；土星 2 圈：{2*ts:.2f} 年。"], 23)
        for y, count, duration, color, label in [(210, 5, tj, BLUE, "木星"), (310, 2, ts, RED, "土星")]:
            body += text(36, y + 7, label, 23)
            for i in range(count):
                xx = 118 + i * duration * 8
                body += f'<rect x="{xx:.3f}" y="{y-20}" width="{duration*8:.3f}" height="40" fill="{color}" opacity=".13" stroke="{color}" stroke-width="2"/>'
                body += text(xx + duration * 4, y + 8, i + 1, 21, color, "middle")
        body += text(36, 389, "少量的节拍差，累积成约 883 年的慢相位一圈。", 23)
        ox, oy, width, amp = 90, 585, 550, 108
        body += line(ox, oy, 655, oy, INK, arrow=True)
        body += line(ox, oy + 130, ox, oy - 145, INK, arrow=True)
        body += path([(ox + width * i / 320, oy - amp * math.cos(4 * math.pi * i / 320)) for i in range(321)])
        for i in range(3):
            body += text(ox + width * i / 2, 757, f"{i*BEAT:.0f}", 22, INK, "middle")
        body += text(36, 438, "只画 cos(2λJ − 5λS)，振幅人为定为 1。", 23)
        body += text(37, oy - amp + 8, "+1", 22)
        body += text(37, oy + amp + 8, "−1", 22)
        body += text(529, 797, "时间 / 年", 22)
        keyframes = []
        for i in range(161):
            f = i / 160
            keyframes.append(f"{f*100:.5f}%{{transform:translate({width*f:.4f}px,{-amp*math.cos(4*math.pi*f):.4f}px)}}")
        body += f'<g transform="translate({ox},{oy})"><circle class="beat-dot" r="8" fill="{RED}"/></g>'
        body += rows(36, 850, ["红点用 8 秒走完两次慢拍，结束后保留完整曲线。", "这不是木星位置曲线，也没有算出真实摄动振幅。"], 22)
        css = f".beat-dot{{transform:translate({width}px,{-amp}px);animation:slow-beat 8s linear 1}}"
        css += "@keyframes slow-beat{" + "".join(keyframes) + "}"
        css += "@media(prefers-reduced-motion:reduce){.beat-dot{animation:none}}"
        assert 880 < BEAT < 890
        write("near-resonance.svg", 943, "木星土星近五比二关系与慢相位",
              "两种公转频率接近整数比，二倍木星平均角与五倍土星平均角之差变化缓慢。蓝线是单位振幅余弦示意，不是历史大不等式的完整解。", body, css)

    def potential():
        body = heading("⑤", "引力势不为零，拉普拉斯和却可以为零")
        body += rows(36, 91, ["球对称天体外部：把距离和势都无量纲化。", "本图令 GM = 1，横轴 r 从 1 到 4，不画内部。"], 23)
        ox, oy = 90, 245
        body += line(ox, oy, 650, oy, INK, arrow=True)
        body += line(ox, 513, ox, 190, INK, arrow=True)
        body += path([(ox + (r - 1) * 170, oy + 230 / r) for r in [1 + i * 3 / 240 for i in range(241)]], BLUE)
        for r in (1, 2, 3, 4):
            body += text(ox + (r - 1) * 170, 224, r, 22, INK, "middle")
        body += text(632, 224, "r", 22)
        body += text(124, 524, "Φ = −1/r；引力指向势下降的方向。", 24, BLUE)
        body += text(46, 482, "−1", 22) + text(35, 310, "−0.25", 19)
        body += panel(568, 260)
        body += rows(48, 611, ["看 P = (1, 0, 0)，不在中心质量上：", "三个方向的势曲率分别是 −2、+1、+1。", "加起来为 0；但势 Φ = −1，引力大小为 1。", "“没有当地质量”不等于“没有远方的引力”。"], 24, 53)
        body += text(36, 874, "完整三维函数：Φ(x,y,z) = −1 / √(x²+y²+z²)。", 23)
        def phi(x, y, z):
            return -1 / math.sqrt(x*x+y*y+z*z)
        h = .0001
        second = [(phi(1+h, 0, 0)-2*phi(1, 0, 0)+phi(1-h, 0, 0))/h**2,
                  (phi(1, h, 0)-2*phi(1, 0, 0)+phi(1, -h, 0))/h**2]
        assert abs(second[0] + 2) < 1e-6 and abs(second[1] - 1) < 1e-6
        write("potential.svg", 920, "引力势和真空中的拉普拉斯方程",
              "曲线为天体外部负一除以r的势。无量纲点P处三个坐标二阶偏导为负二、正一、正一，和为零但势与引力均不为零。", body)

    def predictions():
        body = heading("⑥", "预报不是只把方程往后算")
        for i, (title, detail) in enumerate([
            ("① 观测", "测角、测距、航天器无线电数据。"),
            ("② 建模", "质量、引力、相对论修正等。"),
            ("③ 积分与拟合", "调整初值和参数，让模型贴近观测。"),
            ("④ 检查残差", "区分测量噪声、数值误差、遗漏的物理。"),
            ("⑤ 预报并再检验", "给出适用时段，继续接受新观测挑战。"),
        ]):
            y = 85 + i * 114
            body += panel(y, 99) + text(48, y + 35, title, 26, BLUE)
            body += text(48, y + 77, detail, 23)
        body += rows(36, 704, ["能预报一段时间 ≠ 证明永远稳定。", "存在长期混沌 ≠ 明天就会发生行星碰撞。", "规律确定 ≠ 有限精度的初值能预知无限未来。"], 24, 51)
        write("prediction-and-limits.svg", 885, "从观测到预报的天体力学工作链",
              "五步连接观测、物理模型、积分拟合、残差和新预报，并区别短期精度、长期稳定性与混沌。", body)

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        data = {}
        for factor in (1, 10):
            frames, error = simulate(factor)
            finer, _ = simulate(factor, .00125)
            finer2, _ = simulate(factor, .000625)
            coarse_error = math.dist(frames[-1][1:3], finer[-1][1:3])
            fine_error = math.dist(finer[-1][1:3], finer2[-1][1:3])
            assert 3.8 < coarse_error / fine_error < 4.2
            assert coarse_error < .0002
            data[factor] = frames
            print(f"mass x{factor}: final residual {frames[-1][3]:.9f} deg; energy error {error:.3g}; convergence {coarse_error/fine_error:.3f}")
        history()
        differential()
        residuals(data)
        resonance()
        potential()
        predictions()
        print(f"Slow-phase period: {BEAT:.9f} years; six SVGs generated.")

    main()


@register("catenary", "悬链线：受力平衡、荷载对比、热胀弧垂与倒置拱", "mechanics_sky")
def build_catenary():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "catenary"

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


@register("cycloid", "摆线：最速降线竞赛、折射类比、等时摆与惠更斯护颊", "mechanics_sky")
def build_cycloid():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "cycloid"

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

    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [rolling, racing, speed_depth, refraction, tautochrone,
                 arc_length, periods, cheeks]:
        draw()
    validate()


@register("analytical-mechanics", "分析力学：约束广义坐标、相空间、最小作用量与诺特对称", "mechanics_sky")
def build_analytical_mechanics():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "analytical-mechanics"

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

    main()
