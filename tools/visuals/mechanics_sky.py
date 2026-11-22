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
    write_svg,
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

@register("space-weightless", "空间站失重与微重力：400公里引力比例、电梯视重、曲率追平下落、火焰对流与弹簧测质量", "mechanics_sky")
def build_space_weightless():
    SUBDIR = "space-weightless"

    def _poly(pts, stroke, sw=2.0, fill="none", dash=None, marker_end=None, opacity=None, cls=None):
        d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        extra = []
        if dash:
            extra.append(f'stroke-dasharray="{dash}"')
        if marker_end:
            extra.append(f'marker-end="url(#{marker_end})"')
        if opacity is not None:
            extra.append(f'opacity="{opacity}"')
        if cls:
            extra.append(f'class="{cls}"')
        ext = (" " + " ".join(extra)) if extra else ""
        return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{ext}/>'

    def _line(x1, y1, x2, y2, stroke=HAIRLINE, sw=1.2, dash=None, marker_end=None):
        extra = []
        if dash:
            extra.append(f'stroke-dasharray="{dash}"')
        if marker_end:
            extra.append(f'marker-end="url(#{marker_end})"')
        ext = (" " + " ".join(extra)) if extra else ""
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{ext}/>'

    def _verify_physics():
        """Assert all physical constants and derived orbital / mechanical quantities."""
        gm_earth = 3.986004355e14  # m^3 / s^2 (JPL DE440)
        r_earth = 6.371e6          # m (NASA Earth Fact Sheet volumetric mean radius)
        g0_std = 9.80665           # m / s^2 (CODATA standard gravity)
        h_iss = 4.00e5             # m (400 km typical China Space Station / ISS altitude)
        r_orb = r_earth + h_iss    # 6.771e6 m

        # 1. Gravity at 400 km (~88.5% - 88.6% of surface gravity, ~8.69 m/s^2)
        g_surf_sph = gm_earth / (r_earth ** 2)
        g_400 = gm_earth / (r_orb ** 2)
        ratio_inv_sq = (r_earth / r_orb) ** 2
        ratio_vs_g0 = g_400 / g0_std
        assert 9.81 < g_surf_sph < 9.83
        assert 8.68 < g_400 < 8.70
        assert 0.885 < ratio_inv_sq < 0.886
        assert 0.886 < ratio_vs_g0 < 0.887

        # Basketball scale shock: 24 cm diameter (120 mm radius) -> 7.53 mm above surface
        h_basketball_mm = 120.0 * (h_iss / r_earth)
        moon_basketball_m = 0.120 * (3.844e8 / r_earth)
        assert 7.50 < h_basketball_mm < 7.56
        assert 7.20 < moon_basketball_m < 7.28

        # 2. Circular orbital speed, period, and 1-second drop == Earth curvature sagitta
        v_orb = math.sqrt(gm_earth / r_orb)
        t_orb_min = (2.0 * math.pi * r_orb / v_orb) / 60.0
        drop_1s = 0.5 * g_400 * (1.0 ** 2)
        curv_quad_1s = (v_orb ** 2) / (2.0 * r_orb)
        curv_exact_1s = math.hypot(r_orb, v_orb * 1.0) - r_orb
        assert 7.66e3 < v_orb < 7.68e3
        assert 92.3 < t_orb_min < 92.6
        assert math.isclose(drop_1s, curv_quad_1s, rel_tol=1e-14)
        assert abs(curv_exact_1s - drop_1s) < 5e-6
        assert 4.34 < drop_1s < 4.35

        # Standard-g textbook convention g(400) = g0 * (R_E / r)^2 gives 4.341 m
        drop_1s_std = 0.5 * (g0_std * ratio_inv_sq)
        assert 4.340 < drop_1s_std < 4.343

        # 3. Elevator apparent weight N = m(g - a)
        m_person = 60.0
        g_elev = 9.8
        assert math.isclose(m_person * (g_elev - 0.0), 588.0)
        assert math.isclose(m_person * (g_elev - 0.5 * g_elev), 294.0)
        assert math.isclose(m_person * (g_elev - g_elev), 0.0)

        # 4. Tidal gravity-gradient acceleration 2 * GM * d / r^3
        tidal_per_m = 2.0 * gm_earth / (r_orb ** 3)
        tidal_10m_ug = (tidal_per_m * 10.0) / g0_std * 1e6
        assert 2.55e-6 < tidal_per_m < 2.59e-6
        assert 2.60 < tidal_10m_ug < 2.65

        # 5. Spring-mass chair T = 2 * pi * sqrt(m / k)
        k_spring = 800.0
        t_50 = 2.0 * math.pi * math.sqrt(50.0 / k_spring)
        t_80 = 2.0 * math.pi * math.sqrt(80.0 / k_spring)
        assert math.isclose(t_50, math.pi / 2.0, rel_tol=1e-12)
        assert 1.570 < t_50 < 1.572
        assert 1.986 < t_80 < 1.988
        assert math.isclose(k_spring * (t_50 ** 2) / (4.0 * math.pi ** 2), 50.0, rel_tol=1e-12)
        assert math.isclose(k_spring * (t_80 ** 2) / (4.0 * math.pi ** 2), 80.0, rel_tol=1e-12)

        return {
            "gm": gm_earth,
            "r_e_km": 6371.0,
            "r_orb_km": 6771.0,
            "g_400": g_400,
            "ratio_pct": ratio_inv_sq * 100.0,
            "ratio_g0_pct": ratio_vs_g0 * 100.0,
            "v_orb_kms": v_orb / 1e3,
            "t_orb_min": t_orb_min,
            "drop_1s": drop_1s,
            "h_ball_mm": h_basketball_mm,
            "tidal_10m_ug": tidal_10m_ug,
            "k_spring": k_spring,
            "t_50": t_50,
            "t_80": t_80,
        }

    def _svg_gravity_still_89pct(p):
        els = header(
            "离地面 400 公里有多近？空间站处的地球引力还剩将近九成！",
            "左图按严格几何比例画出地球弧面与 400 km 轨道；右图按牛顿平方反比律计算引力随高度的真实衰减。",
        )

        # Left panel: True-to-scale Earth limb vs 400 km orbit
        els.append(card(20, 64, 352, 300))
        els.append(step_badge(38, 84, 1, BLUE, BLUE_SOFT))
        els.append(txt(56, 88, "真实比例：400 km 只是贴着球皮飞", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 108, "同一把尺：1 像素 = 16.8 km（绝无视觉放大）", 11.2, MUTED))

        extra_defs = (
            '<clipPath id="earth-limb-clip">'
            '<rect x="34" y="118" width="324" height="156" rx="8"/>'
            "</clipPath>"
        )

        # Viewport frame
        els.append('<rect x="34" y="118" width="324" height="156" rx="8" fill="#0f172a"/>')
        # Subtle stars in space background
        for sx, sy, sr in [(54, 134, 1.1), (92, 148, 0.9), (138, 129, 1.2), (288, 132, 1.0), (334, 146, 1.2), (312, 168, 0.9), (66, 174, 1.0)]:
            els.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#e2e8f0" opacity="0.65"/>')

        # True scale geometry: R_E = 6371 km -> 380 px, h = 400 km -> 23.86 px
        cx, cy = 196.0, 562.0
        r_e_px = 380.0
        h_100_px = r_e_px * (100.0 / 6371.0)
        h_400_px = r_e_px * (400.0 / 6371.0)
        r_orb_px = r_e_px + h_400_px
        y_surf_top = cy - r_e_px      # 182.0
        y_orb_top = cy - r_orb_px     # 158.14

        els.append('<g clip-path="url(#earth-limb-clip)">')
        # Atmosphere 100 km Karman glow
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_e_px + h_100_px:.2f}" fill="#38bdf8" fill-opacity="0.22" stroke="#7dd3fc" stroke-width="0.9" stroke-dasharray="3 3"/>')
        # 400 km orbit arc
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_orb_px:.2f}" fill="none" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="5 4"/>')
        # Earth body
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_e_px:.2f}" fill="#1d6fa5" stroke="#93c5fd" stroke-width="1.5"/>')
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_e_px - 10:.2f}" fill="#165a8a" opacity="0.45"/>')
        els.append("</g>")

        # Space station icon at (cx, y_orb_top)
        els.append(_line(cx - 13, y_orb_top, cx + 13, y_orb_top, "#fbbf24", 2.6))
        els.append(f'<rect x="{cx - 4.5:.1f}" y="{y_orb_top - 3.2:.1f}" width="9" height="6.4" rx="1.5" fill="#ffffff" stroke="{ORANGE}" stroke-width="1.2"/>')

        # Dimension tick between orbit and surface at x = cx
        els.append(_line(cx, y_orb_top + 4, cx, y_surf_top, "#fbbf24", 1.4))
        els.append(txt(cx - 18, 143, "中国空间站 / ISS", 11.2, "#fde68a", "end", weight="600"))
        els.append(_line(cx + 16, (y_orb_top + y_surf_top) / 2, 232, 142, "#fbbf24", 1.1))
        els.append(txt(236, 145, "h = 400 km", 11.5, "#fbbf24", weight="700"))
        els.append(txt(236, 161, "仅地球半径的 6.3%", 10.6, "#cbd5e1"))

        # Labels inside Earth arc
        els.append(txt(196, 224, "地球平均半径 R_E = 6371 km", 12.0, "#ffffff", "middle", weight="700"))
        els.append(txt(196, 245, "轨道距地心 r = 6371 + 400 = 6771 km", 11.2, "#e0f2fe", "middle"))
        els.append(txt(196, 264, "（浅蓝虚线：100 km 卡门线大气层顶）", 10.5, "#bae6fd", "middle"))

        # Bottom basketball scale callout
        els.append(card(34, 284, 324, 66, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(46, 304, "把地球缩成直径 24 cm 的标准篮球：", 11.8, INK, weight="700"))
        els.append(txt(46, 324, f"空间站只贴在球皮外 {p['h_ball_mm']:.1f} 毫米处飞驰！", 11.8, BLUE, weight="700"))
        els.append(txt(46, 342, "（对比：月球在 7.24 米外，远出将近 1000 倍）", 10.8, MUTED))

        # Right panel: Computed inverse-square gravity curve g(h)/g(0)
        els.append(card(388, 64, 352, 300))
        els.append(step_badge(406, 84, 2, ORANGE, ORANGE_SOFT))
        els.append(txt(424, 88, "平方反比律：400 km 处仍有 88.5% 引力", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 108, "g(h) / g(0) = [R_E / (R_E + h)]²，按地心距离 r 计算", 11.2, MUTED))

        px0, px1 = 438.0, 718.0
        py0, py1 = 126.0, 262.0
        pw, ph = px1 - px0, py1 - py0
        h_max = 12000.0

        def map_pt(h_km):
            frac = (6371.0 / (6371.0 + h_km)) ** 2
            return px0 + pw * (h_km / h_max), py1 - ph * frac

        # Grid lines
        for pct in (0.25, 0.50, 0.75, 1.00):
            gy = py1 - ph * pct
            els.append(_line(px0, gy, px1, gy, "#e2e8f0", 1.0, dash="3 3" if pct < 1.0 else None))
            els.append(txt(px0 - 6, gy + 4, f"{int(pct * 100)}%", 10.5, MUTED, "end", cls="mono"))
        els.append(txt(px0 - 6, py1 + 4, "0%", 10.5, MUTED, "end", cls="mono"))

        for h_tick, lbl in [(0, "0"), (3000, "3000"), (6371, "6371"), (12000, "12000")]:
            gx = px0 + pw * (h_tick / h_max)
            els.append(_line(gx, py0, gx, py1, "#e2e8f0", 1.0, dash="3 3" if h_tick else None))
            els.append(txt(gx, py1 + 15, lbl, 10.5, MUTED, "middle", cls="mono"))
        els.append(txt((px0 + px1) / 2, py1 + 30, "离地高度 h（km）", 10.8, MUTED, "middle"))

        # Axes
        els.append(_line(px0, py0 - 4, px0, py1, SLATE, 1.3))
        els.append(_line(px0, py1, px1 + 4, py1, SLATE, 1.3))

        # Shaded area + curve
        curve_pts = [map_pt(h_max * i / 120.0) for i in range(121)]
        area_d = (
            f"M{px0:.2f},{py1:.2f} L"
            + " L".join(f"{x:.2f},{y:.2f}" for x, y in curve_pts)
            + f" L{px1:.2f},{py1:.2f} Z"
        )
        els.append(f'<path d="{area_d}" fill="{BLUE}" fill-opacity="0.09"/>')
        els.append(_poly(curve_pts, BLUE, sw=2.4))

        # Key points: h=0, h=400 km, h=6371 km
        x0, y0 = map_pt(0.0)
        x400, y400 = map_pt(400.0)
        x_re, y_re = map_pt(6371.0)

        els.append(_line(x400, y400, x400, py1, ORANGE, 1.3, dash="3 2"))
        els.append(_line(x_re, y_re, x_re, py1, PURPLE, 1.2, dash="3 2"))

        els.append(f'<circle cx="{x0:.2f}" cy="{y0:.2f}" r="4" fill="{BLUE}"/>')
        els.append(f'<circle cx="{x400:.2f}" cy="{y400:.2f}" r="5" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(f'<circle cx="{x_re:.2f}" cy="{y_re:.2f}" r="4.2" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.2"/>')

        # Callout for 400 km
        els.append(_line(x400 + 5, y400, 488, 145, ORANGE, 1.3))
        els.append(card(490, 128, 224, 38, rx=6, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(500, 144, f"空间站 h=400 km：{p['ratio_pct']:.1f}%", 11.4, ORANGE, weight="700"))
        els.append(txt(500, 160, f"g ≈ {p['g_400']:.2f} m/s²（约地表九成）", 10.8, BODY))

        # Callout for h = R_E (6371 km -> 25%)
        els.append(txt(646, y_re - 12, "h = R_E：距地心翻倍 → 25%", 10.6, PURPLE, "middle", weight="600", halo=True))

        # Bottom takeaway inside right card
        els.append(card(404, 298, 320, 52, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(416, 318, "若搭一座 400 km 高梯子站上去称重：", 11.6, INK, weight="700"))
        els.append(txt(416, 338, "60 kg 的人仍重约 53.1 kg——失重绝非因为没引力！", 11.3, ORANGE, weight="700"))

        svg = figure(
            380,
            "400公里空间站真实高度比例与地球引力平方反比衰减曲线",
            "左图按统一比例绘制6371千米地球弧面与400千米空间站轨道，对应24厘米篮球外仅7.5毫米；右图绘制引力随高度衰减曲线，标出400千米处仍保留地表引力的88.5%，约8.69米每二次方秒。",
            els,
            extra_defs=extra_defs,
        )
        write_svg(SUBDIR, "gravity-still-89pct.svg", svg)

    def _svg_elevator_apparent_weight():
        els = header(
            "“引力”不等于“体重秤读数”：为什么一松手就瞬间失重？",
            "你感受到的“沉重”，其实是地板向上托你的支持力 N = m(g − a)。当舱体和你一起自由下落，支持力归零。",
        )

        panels = [
            (
                20,
                1,
                "静止或匀速 (a = 0)",
                BLUE,
                BLUE_SOFT,
                0.0,
                588,
                "60.0 kg（正常）",
                "N = mg = 588 N",
                "地板稳稳托住脚底",
            ),
            (
                264,
                2,
                "向下加速 (a = 0.5g)",
                GREEN,
                GREEN_SOFT,
                0.5,
                294,
                "30.0 kg（半失重）",
                "N = m(g−0.5g) = 294 N",
                "地板一边退让一边轻托",
            ),
            (
                508,
                3,
                "自由下落 (a = g)",
                ORANGE,
                ORANGE_SOFT,
                1.0,
                0,
                "0.0 kg（完全失重！）",
                "N = m(g − g) = 0 N",
                "人与地板同速下落，零挤压",
            ),
        ]

        for px, num, title_s, col, soft_col, a_ratio, n_val, scale_txt, eq_txt, sub_txt in panels:
            els.append(card(px, 64, 232, 226))
            els.append(step_badge(px + 18, 84, num, col, soft_col))
            els.append(txt(px + 35, 88, title_s, 12.8, INK, weight="700"))

            # Elevator cabin
            cab_x, cab_y, cab_w, cab_h = px + 44, 102, 132, 114
            els.append(card(cab_x, cab_y, cab_w, cab_h, rx=8, fill="#f8fafc", stroke=col, sw=1.5, dash="5 3" if num == 3 else None))
            # Cable at top
            mid_x = cab_x + cab_w / 2
            if num < 3:
                els.append(_line(mid_x, 94, mid_x, cab_y, SLATE, 2.0))
            else:
                els.append(_line(mid_x - 6, 95, mid_x - 1, cab_y - 2, ORANGE, 1.8))
                els.append(_line(mid_x + 6, 95, mid_x + 1, cab_y - 2, ORANGE, 1.8))

            # Scale at floor
            scale_y = cab_y + cab_h - 12
            els.append(f'<rect x="{mid_x - 32:.1f}" y="{scale_y:.1f}" width="64" height="9" rx="3" fill="{soft_col}" stroke="{col}" stroke-width="1.2"/>')

            # Stick person (m = 60 kg); floats slightly in panel 3
            lift = 8 if num == 3 else 0
            foot_y = scale_y - lift
            cm_y = foot_y - 30
            head_y = foot_y - 54
            els.append(f'<circle cx="{mid_x:.1f}" cy="{head_y:.1f}" r="8" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
            els.append(_line(mid_x, head_y + 8, mid_x, foot_y - 16, INK, 1.8))
            els.append(_line(mid_x - 13, head_y + 18, mid_x + 13, head_y + 18, INK, 1.6))
            els.append(_line(mid_x, foot_y - 16, mid_x - 9, foot_y, INK, 1.7))
            els.append(_line(mid_x, foot_y - 16, mid_x + 9, foot_y, INK, 1.7))

            # Center-of-mass dot
            els.append(f'<circle cx="{mid_x:.1f}" cy="{cm_y:.1f}" r="3.2" fill="{INK}"/>')

            # Gravity vector mg = 588 N (ALWAYS 34 px downward!)
            els.append(_line(mid_x - 20, cm_y - 10, mid_x - 20, cm_y + 24, ORANGE, 2.2, marker_end="arr-orange"))
            els.append(txt(mid_x - 25, cm_y + 6, "mg", 11.0, ORANGE, "end", weight="700"))
            els.append(txt(mid_x - 25, cm_y + 19, "588N", 10.0, ORANGE, "end", cls="mono"))

            # Normal force vector N
            if n_val == 588:
                els.append(_line(mid_x + 20, cm_y + 10, mid_x + 20, cm_y - 24, BLUE, 2.2, marker_end="arr-blue"))
                els.append(txt(mid_x + 25, cm_y - 10, "N", 11.0, BLUE, weight="700"))
                els.append(txt(mid_x + 25, cm_y + 3, "588N", 10.0, BLUE, cls="mono"))
            elif n_val == 294:
                els.append(_line(mid_x + 20, cm_y + 10, mid_x + 20, cm_y - 7, GREEN, 2.2, marker_end="arr-green"))
                els.append(txt(mid_x + 25, cm_y - 4, "N", 11.0, GREEN, weight="700"))
                els.append(txt(mid_x + 25, cm_y + 9, "294N", 10.0, GREEN, cls="mono"))
            else:
                els.append(txt(mid_x + 19, cm_y + 2, "N = 0", 11.0, ORANGE, weight="700"))
                # Floating apple next to person
                els.append(f'<circle cx="{mid_x + 34:.1f}" cy="{head_y + 4:.1f}" r="5" fill="#ef4444"/>')

            # Downward acceleration arrow outside right cabin wall for panels 2 & 3
            if a_ratio > 0:
                arr_len = 22 if a_ratio == 0.5 else 38
                m_id = "arr-green" if a_ratio == 0.5 else "arr-orange"
                els.append(_line(cab_x + cab_w + 14, 134, cab_x + cab_w + 14, 134 + arr_len, col, 1.8, marker_end=m_id))
                els.append(txt(cab_x + cab_w + 14, 127, "a↓", 10.8, col, "middle", weight="700"))

            # Scale readout pill & formula
            els.append(card(px + 14, 224, 204, 24, rx=6, fill=soft_col, stroke=col))
            els.append(txt(px + 116, 240, f"秤读数：{scale_txt}", 11.3, col, "middle", weight="700"))
            els.append(txt(px + 116, 263, eq_txt, 11.2, INK, "middle", weight="600", cls="mono"))
            els.append(txt(px + 116, 280, sub_txt, 10.8, MUTED, "middle"))

        # Bottom wide card: Leaky cup home experiment
        els.append(card(20, 302, 720, 98))
        els.append(pill(34, 314, "动手实验", fg=BLUE, bg=BLUE_SOFT, w=74, h=22, size=11.5))
        els.append(txt(118, 329, "侧壁扎孔的纸杯：为什么一松手，漏水立刻停住？", 12.8, INK, weight="700"))

        # Cup A: Held still (leaking parabolic jet)
        els.append(f'<path d="M46,344 L52,388 L86,388 L92,344" fill="none" stroke="{SLATE}" stroke-width="1.8"/>')
        els.append(f'<path d="M48,354 L52,387 L86,387 L90,354 Z" fill="#93c5fd" fill-opacity="0.65"/>')
        els.append(f'<circle cx="87" cy="380" r="2.2" fill="{BG}"/>')
        jet_pts = [(88 + 34 * (i / 20.0), 380 + 13 * ((i / 20.0) ** 2)) for i in range(21)]
        els.append(_poly(jet_pts, BLUE, sw=2.4))
        els.append(txt(134, 360, "① 手捏住不动 (a = 0)：", 11.5, INK, weight="700"))
        els.append(txt(134, 380, "杯底托水产生水压 ρgh > 0，水柱喷出", 11.0, BODY))

        els.append(_line(376, 342, 376, 390, HAIRLINE, 1.0, dash="3 3"))

        # Cup B: Free-falling (zero leak!)
        els.append(f'<path d="M416,346 L422,390 L456,390 L462,346" fill="none" stroke="{ORANGE}" stroke-width="1.8"/>')
        els.append(f'<path d="M418,356 L422,389 L456,389 L460,356 Z" fill="#93c5fd" fill-opacity="0.65"/>')
        els.append(f'<circle cx="457" cy="382" r="2.2" fill="#3b82f6"/>')
        els.append(_line(400, 350, 400, 384, ORANGE, 1.8, marker_end="arr-orange"))
        els.append(txt(476, 360, "② 松手自由下落 (a = g)：", 11.5, ORANGE, weight="700"))
        els.append(txt(476, 380, "杯与水同速下落，水压差归零、滴水不漏！", 11.0, BODY))

        svg = figure(
            412,
            "电梯三态视重对比与自由下落扎孔水杯实验",
            "上方三栏对比60千克乘客在静止、以0.5g向下加速、以1g自由下落时重力mg始终为588牛而支持力N从588牛减至294牛再到0牛；下方展示侧壁扎孔水杯松手自由下落时水压差归零停止漏水。",
            els,
        )
        write_svg(SUBDIR, "elevator-apparent-weight.svg", svg)

    def _kepler_path(cx, cy, r_launch, v_ratio, r_stop, n_steps=160):
        """Exact polar conic r(theta) = p / (1 + e*cos(theta - theta0)) from top mountain launch."""
        # At launch (top, theta_screen = 0 -> up): r = r_launch, vr = 0.
        # Let mu_norm = 1, r_launch = 1 -> v_circ = 1. Angular momentum h = v_ratio.
        # p = h^2 = v_ratio^2. Since r(0) = 1 = p / (1 + e*cos(phi)),
        # if v_ratio < 1: launch is apogee -> e = 1 - v_ratio^2, r(th) = p / (1 - e*cos(th))
        # if v_ratio >= 1: launch is perigee -> e = v_ratio^2 - 1, r(th) = p / (1 + e*cos(th))
        p_orb = v_ratio ** 2
        pts = []
        for i in range(n_steps + 1):
            th = (2.0 * math.pi) * i / n_steps
            denom = 1.0 + (v_ratio ** 2 - 1.0) * math.cos(th)
            r = r_launch * (p_orb / denom)
            x = cx + r * math.sin(th)
            y = cy - r * math.cos(th)
            pts.append((x, y))
            if i > 0 and r <= r_stop:
                break
        return pts

    def _svg_falling_around_earth(p):
        # Play-once CSS rotation of the orbiting station dot around (188, 240), resting at 360 deg
        anim_css = """
      .orb-runner {
        transform-origin: 188px 240px;
        animation: orbitOnce 6.5s cubic-bezier(0.25, 0.1, 0.25, 1) 1 forwards;
      }
      @keyframes orbitOnce {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      @media (prefers-reduced-motion: reduce) {
        .orb-runner { animation: none; }
      }"""

        els = header(
            "每秒都在往下掉 4.35 米，为什么空间站永远砸不到地面？",
            "左图：牛顿高山大炮的精确圆锥曲线轨迹；右图：把 1 秒钟放大看——横飞 7.67 km 时，弯曲的地表刚好也退让了 4.35 m！",
        )

        # Left card: Newton's cannonball & circular orbit
        els.append(card(20, 64, 336, 344))
        els.append(step_badge(38, 84, 1, BLUE, BLUE_SOFT))
        els.append(txt(56, 88, "牛顿高山思想实验：绕地 = 追平曲率的下落", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 107, "高度与炮弹轨迹按开普勒方程绘制（高度示意放大）", 10.9, MUTED))

        cx, cy = 188.0, 240.0
        r_earth_d = 76.0
        r_launch_d = 100.0

        # Sub-orbital & elliptical trajectories
        pts_slow = _kepler_path(cx, cy, r_launch_d, 0.72, r_earth_d)
        pts_mid = _kepler_path(cx, cy, r_launch_d, 0.89, r_earth_d)
        pts_ell = _kepler_path(cx, cy, r_launch_d, 1.10, r_earth_d)

        els.append(_poly(pts_ell, PURPLE, sw=1.5, dash="4 3"))
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_launch_d:.1f}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')

        # Earth disk + mountain peak
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_earth_d:.1f}" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.6"/>')
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.0" fill="{INK}"/>')
        els.append(txt(cx, cy + 16, "地心", 10.8, INK, "middle", weight="600"))
        els.append(f'<polygon points="{cx - 10:.1f},{cy - r_earth_d + 2:.1f} {cx:.1f},{cy - r_launch_d:.1f} {cx + 10:.1f},{cy - r_earth_d + 2:.1f}" fill="{SLATE}"/>')

        els.append(_poly(pts_slow, SLATE, sw=1.7, dash="3 3"))
        els.append(_poly(pts_mid, GREEN, sw=1.8, dash="5 3"))

        # Static launch marker + animated orbiting station group
        els.append(f'<circle cx="{cx:.1f}" cy="{cy - r_launch_d:.1f}" r="3.6" fill="#ffffff" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append('<g class="orb-runner">')
        els.append(f'<circle cx="{cx:.1f}" cy="{cy - r_launch_d:.1f}" r="5.4" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append("</g>")
        els.append(_line(cx + 6, cy - r_launch_d, cx + 46, cy - r_launch_d, ORANGE, 2.0, marker_end="arr-orange"))

        # Trajectory labels
        els.append(txt(cx + 50, cy - r_launch_d + 4, "v = 7.67 km/s", 11.2, ORANGE, weight="700", halo=True))
        els.append(txt(264, 212, "慢 → 落回地面", 10.6, SLATE, halo=True))
        els.append(txt(248, 314, "更快 → 椭圆轨道", 10.6, PURPLE, halo=True))
        els.append(txt(64, 166, "圆轨道", 11.2, BLUE, weight="700", halo=True))

        # Bottom summary box in left card
        els.append(card(34, 344, 308, 52, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(46, 364, f"第一宇宙速度（400 km）：v ≈ {p['v_orb_kms']:.2f} km/s", 11.5, BLUE, weight="700"))
        els.append(txt(46, 383, f"约 2.76 万 km/h，每 {p['t_orb_min']:.1f} 分钟绕地球一圈！", 11.0, BODY))

        # Right card: 1-second geometric zoom
        els.append(card(372, 64, 368, 344))
        els.append(step_badge(390, 84, 2, ORANGE, ORANGE_SOFT))
        els.append(txt(408, 88, "放大看 1 秒钟：掉下去的，刚好被地球弯走！", PANEL_TITLE, INK, weight="700"))
        els.append(txt(388, 107, "横向 7.67 km 与竖直 4.35 m 相差 1760 倍（竖直示意放大）", 10.8, MUTED))

        # Geometric construction inside right card:
        # Start column x0 = 414, end column x1 = 664 (dx = 250 px -> 7.67 km)
        # Orbit tangent y_orb0 = 142; after 1 s falls dy_vis = 48 px -> y_orb1 = 190
        # Earth surface tangent y_surf0 = 228; after 7.67 km curves down SAME dy_vis = 48 px -> y_surf1 = 276
        x0, x1 = 414.0, 664.0
        y_orb0, y_orb1 = 142.0, 190.0
        y_surf0, y_surf1 = 228.0, 276.0
        dy_vis = y_orb1 - y_orb0

        # Parabolic / circular arcs matching dy_vis = 48 px
        orb_arc = [(x0 + (x1 - x0) * t, y_orb0 + dy_vis * (t ** 2)) for t in [i / 40.0 for i in range(41)]]
        surf_arc = [(x0 + (x1 - x0) * t, y_surf0 + dy_vis * (t ** 2)) for t in [i / 40.0 for i in range(41)]]

        # Shaded Earth crust under surf_arc
        earth_poly = (
            f"M{x0:.1f},302 L{x0:.1f},{y_surf0:.1f} L"
            + " L".join(f"{x:.1f},{y:.1f}" for x, y in surf_arc)
            + f" L{x1:.1f},302 Z"
        )
        els.append(f'<path d="{earth_poly}" fill="#dbeafe" opacity="0.75"/>')

        # Inertial straight tangent (top) & horizontal ground tangent (bottom)
        els.append(_line(x0, y_orb0, x1, y_orb0, SLATE, 1.4, dash="5 4", marker_end="arr-muted"))
        els.append(_line(x0, y_surf0, x1, y_surf0, SLATE, 1.2, dash="4 4"))

        # Actual orbit curve & Earth surface curve
        els.append(_poly(orb_arc, BLUE, sw=2.5))
        els.append(_poly(surf_arc, GREEN, sw=2.4))

        # Altitude bars at t = 0 and t = 1 s (both exact same 86 px = 400 km!)
        els.append(_line(x0, y_orb0 + 5, x0, y_surf0 - 3, BLUE, 1.3, dash="3 2"))
        els.append(txt(x0 + 6, (y_orb0 + y_surf0) / 2 + 4, "离地 400 km", 10.8, BLUE, weight="600", halo=True))

        els.append(_line(x1 - 54, orb_arc[31][1] + 2, x1 - 54, surf_arc[31][1] - 2, BLUE, 1.3, dash="3 2"))
        els.append(txt(x1 - 60, (orb_arc[31][1] + surf_arc[31][1]) / 2 + 4, "仍离地 400 km！", 10.8, BLUE, "end", weight="700", halo=True))

        # Drop arrows at x1 = 664 (4.35 m == 4.35 m)
        els.append(_line(x1, y_orb0 + 2, x1, y_orb1 - 3, ORANGE, 2.2, marker_end="arr-orange"))
        els.append(_line(x1, y_surf0 + 2, x1, y_surf1 - 3, GREEN, 2.2, marker_end="arr-green"))

        els.append(f'<circle cx="{x0:.1f}" cy="{y_orb0:.1f}" r="4.5" fill="{ORANGE}"/>')
        els.append(f'<circle cx="{x1:.1f}" cy="{y_orb1:.1f}" r="4.8" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.3"/>')

        # Labels on right zoom
        els.append(txt((x0 + x1) / 2, y_orb0 - 8, "若无引力惯性直飞：1 秒前进 7.67 km", 11.0, SLATE, "middle", weight="600"))
        els.append(txt(x1 + 7, (y_orb0 + y_orb1) / 2 - 2, "自由下落", 10.6, ORANGE, weight="700"))
        els.append(txt(x1 + 7, (y_orb0 + y_orb1) / 2 + 12, f"{p['drop_1s']:.2f} m", 11.0, ORANGE, weight="700", cls="mono"))
        els.append(txt(x1 + 7, (y_surf0 + y_surf1) / 2 - 2, "地表下弯", 10.6, GREEN, weight="700"))
        els.append(txt(x1 + 7, (y_surf0 + y_surf1) / 2 + 12, f"{p['drop_1s']:.2f} m", 11.0, GREEN, weight="700", cls="mono"))
        els.append(txt(424, 294, "弯曲的地球表面", 10.8, GREEN, weight="600"))

        # Algebraic identity box at bottom of right card
        els.append(card(388, 312, 336, 84, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(400, 332, "为什么两个 4.35 m 严丝合缝？因为 v = √(GM/r)：", 11.4, INK, weight="700"))
        els.append(txt(400, 353, "地表弯曲量 x²/(2r) = v²t²/(2r) = ½(GM/r²)t² = ½gt²", 11.1, ORANGE, weight="700"))
        els.append(txt(400, 374, "空间站、航天员、水珠沿同一条圆弧下落 → 相对漂浮！", 11.0, BODY))

        svg = figure(
            424,
            "牛顿高山大炮轨道速度分岔与空间站1秒下落追平地球曲率图解",
            "左图展示不同水平初速度对应的落回地面、圆轨道（7.67千米每秒，周期92.4分钟）与椭圆轨道，含播放一次的绕地动画；右图放大1秒内的运动，水平前进7.67千米的同时自由下落4.35米，恰好等于地球曲率下降的4.35米。",
            els,
            extra_css=anim_css,
        )
        write_svg(SUBDIR, "falling-around-earth.svg", svg)

    def _svg_microgravity_residuals(p):
        els = header(
            "为什么严谨的说法叫“微重力（10⁻⁶ g）”，而不是绝对零重力？",
            "左图：潮汐引力梯度与稀薄大气留下百万分之一 g 残余加速度；右图：失去浮力对流后，火焰与沸水大变样。",
        )

        # Left card: Three sources of ~10^-6 g residual acceleration
        els.append(card(20, 64, 352, 332))
        els.append(step_badge(38, 84, 1, PURPLE, PURPLE_SOFT))
        els.append(txt(56, 88, "百万分之一 g 从哪来？三大微弱扰动", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 107, "只有质心 1 个点完全抵消，舱体其余位置仍有微小差值", 10.8, MUTED))

        # Vertical 20 m module diagram (x = 96..156, y = 126..290)
        mod_x, mod_y, mod_w, mod_h = 90, 130, 66, 160
        cm_y = mod_y + mod_h / 2  # 210
        els.append(card(mod_x, mod_y, mod_w, mod_h, rx=14, fill="#f8fafc", stroke=SLATE, sw=1.6))
        # Solar wings
        els.append(_line(mod_x - 36, cm_y, mod_x, cm_y, BLUE, 3.0))
        els.append(_line(mod_x + mod_w, cm_y, mod_x + mod_w + 26, cm_y, BLUE, 3.0))

        # Top point (+10 m, farther from Earth -> drifts up/away)
        els.append(f'<circle cx="{mod_x + 33}" cy="{mod_y + 24}" r="4" fill="{PURPLE}"/>')
        els.append(_line(mod_x + 33, mod_y + 20, mod_x + 33, mod_y + 4, PURPLE, 2.0, marker_end="arr-muted"))
        # CM point (0 m -> exact balance)
        els.append(_line(mod_x + 8, cm_y, mod_x + mod_w - 8, cm_y, HAIRLINE, 1.1, dash="3 2"))
        els.append(f'<circle cx="{mod_x + 33}" cy="{cm_y}" r="4.2" fill="{GREEN}"/>')
        # Bottom point (-10 m, closer to Earth -> drifts down/toward Earth)
        els.append(f'<circle cx="{mod_x + 33}" cy="{mod_y + mod_h - 24}" r="4" fill="{ORANGE}"/>')
        els.append(_line(mod_x + 33, mod_y + mod_h - 20, mod_x + 33, mod_y + mod_h - 4, ORANGE, 2.0, marker_end="arr-orange"))

        # Rarefied air molecules hitting from left
        for ay in (156, 184, 236, 264):
            els.append(f'<circle cx="42" cy="{ay}" r="2.2" fill="{BLUE}"/>')
            els.append(_line(47, ay, 82, ay, BLUE, 1.3, dash="2 2", marker_end="arr-blue"))
        els.append(txt(40, 142, "稀薄分子", 10.2, BLUE, weight="600"))

        # Earth direction indicator at bottom
        els.append(txt(mod_x + 33, 308, "↓ 指向地心（r₀ = 6771 km）", 10.5, MUTED, "middle"))

        # Explanatory callouts on right side of Left Card (x = 188..358)
        els.append(card(190, 126, 168, 56, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(200, 144, "① 潮汐引力梯度", 11.4, PURPLE, weight="700"))
        els.append(txt(200, 160, "顶舱离地心远、引力略弱", 10.6, BODY))
        els.append(txt(200, 174, f"±10 m 处约 {p['tidal_10m_ug']:.1f}×10⁻⁶ g", 10.6, PURPLE, weight="600"))

        els.append(card(190, 190, 168, 48, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(200, 208, "② 400 km 稀薄大气阻力", 11.4, BLUE, weight="700"))
        els.append(txt(200, 226, "微弱迎风减速 ~0.1–1 μg", 10.6, BODY))

        els.append(card(190, 246, 168, 52, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(200, 264, "③ 推力器与人员活动", 11.4, ORANGE, weight="700"))
        els.append(txt(200, 281, "轨控点火、蹬壁、风扇振动", 10.6, BODY))
        els.append(txt(200, 294, "（跑步机须配专门隔振台）", 10.2, MUTED))

        els.append(card(34, 322, 324, 60, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(46, 342, "潮汐加速度公式：Δa ≈ (2GM / r³) · Δr", 11.4, INK, weight="700"))
        els.append(txt(46, 362, "偏离质心仅约 4 米，就有 1×10⁻⁶ g（百万分之一 g）！", 11.0, BODY))

        # Right card: Buoyancy disappears -> Spherical blue flame & giant boiling bubble
        els.append(card(388, 64, 352, 332))
        els.append(step_badge(406, 84, 2, ORANGE, ORANGE_SOFT))
        els.append(txt(424, 88, "没有“热空气上浮”：火焰与沸水大变样", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 107, "浮力来自重力造成的上下压强差；微重力下自然对流消失", 10.8, MUTED))

        # Flame comparison sub-cards
        # Sub-card A: Earth 1 g teardrop flame
        els.append(card(404, 122, 154, 152, rx=8, fill="#fffbeb", stroke=ORANGE))
        els.append(txt(481, 141, "地面蜡烛（1 g）", 11.8, ORANGE, "middle", weight="700"))
        # Candle stick + wick
        els.append(f'<rect x="473" y="218" width="16" height="28" rx="2" fill="#e2e8f0" stroke="{SLATE}" stroke-width="1.2"/>')
        els.append(_line(481, 210, 481, 218, INK, 1.8))
        # Teardrop yellow/orange flame
        els.append('<path d="M481,154 C495,176 496,202 481,210 C466,202 467,176 481,154 Z" fill="#f97316" fill-opacity="0.85"/>')
        els.append('<path d="M481,168 C489,182 489,200 481,208 C473,200 473,182 481,168 Z" fill="#fde047"/>')
        # Upward buoyancy convection arrows
        els.append(_line(452, 214, 452, 166, BLUE, 1.5, marker_end="arr-blue"))
        els.append(_line(510, 214, 510, 166, BLUE, 1.5, marker_end="arr-blue"))
        els.append(txt(481, 261, "热气上浮拉成瘦长黄火苗", 10.6, BODY, "middle", weight="600"))

        # Sub-card B: Space microgravity spherical blue flame
        els.append(card(570, 122, 154, 152, rx=8, fill="#eff6ff", stroke=BLUE))
        els.append(txt(647, 141, "空间站火焰（~10⁻⁶ g）", 11.8, BLUE, "middle", weight="700"))
        els.append(f'<rect x="639" y="218" width="16" height="28" rx="2" fill="#e2e8f0" stroke="{SLATE}" stroke-width="1.2"/>')
        els.append(_line(647, 198, 647, 218, INK, 1.8))
        # Calm blue spherical diffusion flame centered at (647, 194)
        els.append('<circle cx="647" cy="194" r="24" fill="#3b82f6" fill-opacity="0.28" stroke="#2563eb" stroke-width="1.8"/>')
        els.append('<circle cx="647" cy="194" r="14" fill="#60a5fa" fill-opacity="0.45"/>')
        # Symmetric radial diffusion arrows (8 directions -> 4 diagonals)
        for dx, dy in [(-28, -22), (28, -22), (-28, 16), (28, 16)]:
            els.append(_line(647 + dx, 194 + dy, 647 + dx * 0.62, 194 + dy * 0.62, BLUE, 1.2, dash="2 2"))
        els.append(txt(647, 261, "全向分子扩散成安静蓝球", 10.6, BLUE, "middle", weight="700"))

        # Boiling water comparison card at bottom of right panel
        els.append(card(404, 286, 320, 96, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(416, 306, "烧开水也一样（NASA 池沸腾实验）：", 11.6, GREEN, weight="700"))
        # Mini visual on right side of green card
        els.append(f'<rect x="634" y="296" width="80" height="62" rx="6" fill="#ffffff" stroke="{GREEN}" stroke-width="1.2"/>')
        els.append(_line(643, 350, 705, 350, ORANGE, 2.6))
        els.append(f'<circle cx="674" cy="329" r="17" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.5"/>')
        els.append(txt(674, 333, "大汽泡", 9.8, BLUE, "middle", weight="700"))
        els.append(txt(416, 326, "• 地面：蒸汽泡受浮力迅速上浮破裂；", 10.9, BODY))
        els.append(txt(416, 346, "• 太空：气泡不往上跑，聚成一颗大汽泡", 10.9, BODY))
        els.append(txt(416, 365, "  包住加热面（飞船须靠泵强制散热）", 10.7, MUTED))

        svg = figure(
            412,
            "空间站百万分之一g微重力来源与球形蓝色火焰及池沸腾对比",
            "左图展示空间站20米舱段内的潮汐引力梯度（偏离质心10米约2.6微g）、400千米稀薄大气阻力与推力器振动；右图对比地面受浮力对流拉长的黄色蜡烛火焰与微重力下靠分子扩散形成的球形蓝色火焰，以及微重力沸水聚合成单颗大汽泡的现象。",
            els,
        )
        write_svg(SUBDIR, "microgravity-residuals.svg", svg)

    def _svg_space_mass_spring(p):
        els = header(
            "体重秤读数永远是 0，空间站里怎样给航天员“称体重”？",
            "失重没有夺走“惯性质量”！坐上校准弹簧椅（k = 800 N/m），测一次往返周期 T = 2π√(m/k) 就能算出质量。",
        )

        # Left card: Spring-mass chair schematic
        els.append(card(20, 64, 292, 310))
        els.append(step_badge(38, 84, 1, GREEN, GREEN_SOFT))
        els.append(txt(56, 88, "太空质量测量仪（BMMD）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 107, "不用重力 mg，改用牛顿第二定律 F = ma", 10.8, MUTED))

        # Bulkhead + spring + sled schematic (y = 122..224)
        els.append(card(34, 120, 264, 106, rx=8, fill="#f8fafc", stroke=BORDER))
        # Left wall hatch
        els.append(_line(48, 130, 48, 214, SLATE, 2.4))
        for wy in range(134, 214, 12):
            els.append(_line(40, wy + 6, 48, wy, SLATE, 1.1))

        # Spring zigzag from x=48 to x=142 at y=174
        spring_pts = [(48, 174), (60, 174)]
        for i in range(7):
            sx = 64 + i * 10
            sy = 164 if i % 2 == 0 else 184
            spring_pts.append((sx, sy))
        spring_pts += [(134, 174), (146, 174)]
        els.append(_poly(spring_pts, GREEN, sw=2.0))
        els.append(txt(96, 155, "k = 800 N/m", 10.5, GREEN, "middle", weight="700", cls="mono"))

        # Sled + strapped astronaut
        els.append(card(146, 146, 68, 52, rx=7, fill=BLUE_SOFT, stroke=BLUE, sw=1.5))
        els.append(f'<circle cx="180" cy="161" r="7.5" fill="#ffffff" stroke="{INK}" stroke-width="1.5"/>')
        els.append(_line(180, 169, 180, 188, INK, 1.8))
        els.append(_line(166, 177, 194, 177, ORANGE, 2.0))  # rigid strap
        els.append(txt(180, 212, "绑紧身体 + 屏息", 10.4, BLUE, "middle", weight="600"))

        # Oscillation double arrow & optical sensor
        els.append(_line(224, 172, 278, 172, ORANGE, 1.6, marker_end="arr-orange"))
        els.append(_line(278, 172, 224, 172, ORANGE, 1.6))
        els.append(txt(252, 162, "往返 ±A", 10.5, ORANGE, "middle", weight="700"))
        els.append(txt(252, 190, "光电测 T", 10.4, MUTED, "middle"))

        # Formula & comparison box
        els.append(card(34, 238, 264, 122, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(46, 258, "• 地面体重秤：测支持力 N = mg（太空归零）", 10.9, BODY))
        els.append(txt(46, 279, "• 太空弹簧椅：测惯性回复 ma = −kx", 10.9, BODY))
        els.append(txt(46, 303, "周期 T = 2π√(m / k)  （式里根本没有 g！）", 11.2, GREEN, weight="700"))
        els.append(txt(46, 326, "反推质量：m = k · T² / (4π²)", 11.4, INK, weight="700"))
        els.append(txt(46, 346, "质量越大惯性越大 → 来回弹一次越慢", 10.7, MUTED))

        # Right card: Exact computed x(t) = A cos(2*pi*t / T) curves for 50 kg vs 80 kg
        els.append(card(328, 64, 412, 310))
        els.append(step_badge(346, 84, 2, BLUE, BLUE_SOFT))
        els.append(txt(364, 88, "精确位移曲线：50 kg vs 80 kg（k = 800 N/m）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(344, 107, "振幅 A = 10 cm  ｜  蓝实线：50 kg  ｜  橙虚线：80 kg", 10.8, MUTED))

        gx0, gx1 = 382.0, 718.0
        gy_top, gy_mid, gy_bot = 138.0, 198.0, 258.0
        gw = gx1 - gx0
        amp_px = gy_mid - gy_top  # 60 px -> 10 cm
        t_max = 4.0

        # Grid
        for gy, glbl in [(gy_top, "+10 cm"), (gy_mid, "0"), (gy_bot, "−10 cm")]:
            els.append(_line(gx0, gy, gx1, gy, "#e2e8f0" if gy != gy_mid else SLATE, 1.0 if gy != gy_mid else 1.2, dash="3 3" if gy != gy_mid else None))
            els.append(txt(gx0 - 6, gy + 4, glbl, 10.3, MUTED, "end", cls="mono"))

        for t_sec in (0.0, 1.0, 2.0, 3.0, 4.0):
            tx = gx0 + gw * (t_sec / t_max)
            els.append(_line(tx, gy_top - 6, tx, gy_bot + 6, "#e2e8f0", 1.0, dash="3 3" if t_sec > 0 else None))
            els.append(txt(tx, gy_bot + 20, f"{t_sec:.0f} s", 10.5, MUTED, "middle", cls="mono"))
        els.append(_line(gx0, gy_top - 8, gx0, gy_bot + 6, SLATE, 1.3))
        els.append(txt((gx0 + gx1) / 2, gy_bot + 35, "时间 t（秒）", 10.8, MUTED, "middle"))

        t_50, t_80 = p["t_50"], p["t_80"]
        pts_50 = [
            (gx0 + gw * (t_max * i / 200.0) / t_max, gy_mid - amp_px * math.cos(2.0 * math.pi * (t_max * i / 200.0) / t_50))
            for i in range(201)
        ]
        pts_80 = [
            (gx0 + gw * (t_max * i / 200.0) / t_max, gy_mid - amp_px * math.cos(2.0 * math.pi * (t_max * i / 200.0) / t_80))
            for i in range(201)
        ]

        els.append(_poly(pts_50, BLUE, sw=2.3))
        els.append(_poly(pts_80, ORANGE, sw=2.2, dash="6 4"))

        # Period bracket for T1 = 1.57 s (50 kg, peak at t=0 to peak at t=1.571 s)
        x_t50 = gx0 + gw * (t_50 / t_max)
        els.append(_line(gx0, 125, x_t50, 125, BLUE, 1.5))
        els.append(_line(gx0, 121, gx0, 134, BLUE, 1.3))
        els.append(_line(x_t50, 121, x_t50, 138, BLUE, 1.3, dash="2 2"))
        els.append(f'<circle cx="{x_t50:.1f}" cy="{gy_top:.1f}" r="4" fill="{BLUE}"/>')
        els.append(txt((gx0 + x_t50) / 2, 119, f"T₁ = {t_50:.2f} s → 50 kg", 10.8, BLUE, "middle", weight="700"))

        # Period marker for T2 = 1.99 s (80 kg, peak at t=1.987 s)
        x_t80 = gx0 + gw * (t_80 / t_max)
        els.append(f'<circle cx="{x_t80:.1f}" cy="{gy_top:.1f}" r="4.2" fill="{ORANGE}"/>')
        els.append(_line(x_t80 + 4, gy_top - 2, x_t80 + 26, 123, ORANGE, 1.3))
        els.append(txt(x_t80 + 30, 126, f"T₂ = {t_80:.2f} s → 80 kg", 10.8, ORANGE, weight="700"))

        # Bottom clinical & exercise note
        els.append(card(344, 302, 380, 58, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(356, 322, "NASA“天空实验室”实测精度达 0.1%（误差仅几十克）：", 11.3, INK, weight="700"))
        els.append(txt(356, 343, "配合每天约 2 小时抗阻/跑步机训练，实时监测骨密度与肌肉流失。", 10.9, BODY))

        svg = figure(
            388,
            "太空弹簧质量测量仪原理与50千克对80千克简谐振动周期对比",
            "左图展示校准劲度系数k=800牛每米的太空弹簧椅测质量原理T=2π√(m/k)；右图精确绘制50千克（实线蓝，周期1.57秒）与80千克（虚线橙，周期1.99秒）的余弦位移曲线，说明无需重力即可由振动快慢反推质量。",
            els,
        )
        write_svg(SUBDIR, "space-mass-spring.svg", svg)
    params = _verify_physics()
    _svg_gravity_still_89pct(params)
    _svg_elevator_apparent_weight()
    _svg_falling_around_earth(params)
    _svg_microgravity_residuals(params)
    _svg_space_mass_spring(params)


@register("cosmic-velocities", "卫星发射与三大宇宙速度：轨道族、高低轨速度能量悖论、霍曼变轨、第三宇宙速度合成与多级火箭", "mechanics_sky")
def build_cosmic_velocities():
    SUBDIR = "cosmic-velocities"

    GM_E = 398600.435507          # km^3 / s^2

    R_EQ = 6378.137               # km

    GM_SUN = 132712440041.27942   # km^3 / s^2

    AU_KM = 149597870.700         # km

    T_SID = 86164.09054           # s (mean sidereal day: 23h 56m 04.09s)

    R_MOON = 384400.0             # km (mean Earth-Moon distance)

    def _integrate_ballistic(r0, v0_km_s, dt=2.0, max_steps=6000):
        """RK4 integration of two-body trajectory in km & s from (0, r0) moving +x."""
        def accel(px, py):
            r2 = px * px + py * py
            r3 = r2 * math.sqrt(r2)
            return (-GM_E * px / r3, -GM_E * py / r3)

        x, y = 0.0, r0
        vx, vy = v0_km_s, 0.0
        pts = [(x, y)]
        for _ in range(max_steps):
            ax1, ay1 = accel(x, y)
            x2, y2 = x + 0.5 * dt * vx, y + 0.5 * dt * vy
            vx2, vy2 = vx + 0.5 * dt * ax1, vy + 0.5 * dt * ay1
            ax2, ay2 = accel(x2, y2)

            x3, y3 = x + 0.5 * dt * vx2, y + 0.5 * dt * vy2
            vx3, vy3 = vx + 0.5 * dt * ax2, vy + 0.5 * dt * ay2
            ax3, ay3 = accel(x3, y3)

            x4, y4 = x + dt * vx3, y + dt * vy3
            vx4, vy4 = vx + dt * ax3, vy + dt * ay3
            ax4, ay4 = accel(x4, y4)

            x += (dt / 6.0) * (vx + 2 * vx2 + 2 * vx3 + vx4)
            y += (dt / 6.0) * (vy + 2 * vy2 + 2 * vy3 + vy4)
            vx += (dt / 6.0) * (ax1 + 2 * ax2 + 2 * ax3 + ax4)
            vy += (dt / 6.0) * (ay1 + 2 * ay2 + 2 * ay3 + ay4)
            pts.append((x, y))
            r_now = math.hypot(x, y)
            if r_now <= R_EQ:
                break
        return pts
    v1 = math.sqrt(GM_E / R_EQ)
    v2 = math.sqrt(2.0 * GM_E / R_EQ)
    v_earth = math.sqrt(GM_SUN / AU_KM)
    v_sun_esc = math.sqrt(2.0 * GM_SUN / AU_KM)
    v_inf = v_sun_esc - v_earth
    v3 = math.sqrt(v2 * v2 + v_inf * v_inf)

    assert abs(v1 - 7.905) < 0.001, f"Unexpected v1={v1}"
    assert abs(v2 - 11.180) < 0.001, f"Unexpected v2={v2}"
    assert abs(v2 / v1 - math.sqrt(2.0)) < 1e-12
    assert abs(v_earth - 29.785) < 0.001, f"Unexpected v_earth={v_earth}"
    assert abs(v_sun_esc - 42.122) < 0.001, f"Unexpected v_sun_esc={v_sun_esc}"
    assert abs(v3 - 16.65) < 0.01, f"Unexpected v3={v3}"

    # Curvature drop in t = 1 s at v1 matches 1/2 g t^2
    g_eq = GM_E / (R_EQ * R_EQ) * 1000.0  # m/s^2
    drop_curv_m = (math.hypot(R_EQ, v1 * 1.0) - R_EQ) * 1000.0
    drop_fall_m = 0.5 * g_eq * (1.0 ** 2)
    assert abs(drop_curv_m - drop_fall_m) < 0.002 and abs(drop_fall_m - 4.90) < 0.02

    # Geostationary & Hohmann transfer from 200 km LEO to GEO
    r_geo = (GM_E * (T_SID / (2.0 * math.pi)) ** 2) ** (1.0 / 3.0)
    h_geo = r_geo - R_EQ
    v_geo = math.sqrt(GM_E / r_geo)
    assert abs(h_geo - 35786.0) < 1.0
    assert abs(v_geo - 3.075) < 0.002

    r_leo200 = R_EQ + 200.0
    v_leo200 = math.sqrt(GM_E / r_leo200)
    a_tr = 0.5 * (r_leo200 + r_geo)
    vp_tr = math.sqrt(GM_E * (2.0 / r_leo200 - 1.0 / a_tr))
    va_tr = math.sqrt(GM_E * (2.0 / r_geo - 1.0 / a_tr))
    dv1 = vp_tr - v_leo200
    dv2 = v_geo - va_tr
    t_tr_hr = math.pi * math.sqrt(a_tr ** 3 / GM_E) / 3600.0
    assert abs(dv1 - 2.46) < 0.01, f"Unexpected dv1={dv1}"
    assert abs(dv2 - 1.48) < 0.01, f"Unexpected dv2={dv2}"
    assert abs(t_tr_hr - 5.26) < 0.02

    # Tsiolkovsky staging assertions (100 t launch mass, 2 t payload, ve = 3.1 km/s, eps = 0.10)
    ve_kero = 3.1
    ve_hydro = 4.4
    dv_1stage = ve_kero * math.log(100.0 / (2.0 + 0.10 * 98.0))
    dv_2stage = (
        ve_kero * math.log(100.0 / (18.0 + 0.10 * 82.0))
        + ve_kero * math.log(18.0 / (2.0 + 0.10 * 16.0))
    )
    dv_3stage = (
        ve_kero * math.log(100.0 / (25.0 + 0.10 * 75.0))
        + ve_kero * math.log(25.0 / (7.0 + 0.10 * 18.0))
        + ve_kero * math.log(7.0 / (2.0 + 0.10 * 5.0))
    )
    assert 6.60 < dv_1stage < 6.65
    assert 9.13 < dv_2stage < 9.16
    assert 9.89 < dv_3stage < 9.93

    # ==================================================================
    # SVG 1: Newton's Mountain Cannonball & 4.90m Curvature Proof
    # ==================================================================
    def build_newton_cannon():
        els = header(
            "牛顿高山大炮实验：入轨不是“失重悬浮”，而是下落弧度刚好追上地球弯曲",
            "忽略空气阻力从山顶水平开炮：慢了砸回地面；达到第一宇宙速度时，地面每秒同步往下让开 4.90 米",
        )

        # Left Panel: RK4 two-body trajectories around Earth
        els.append(card(20, 62, 352, 294))
        els.append(txt(36, 84, "① 四种初速度的真实二体引力轨迹", 12.8, INK, weight="600"))

        cx, cy = 186.0, 194.0
        r_px = 56.0
        r_mtn = R_EQ * 1.10  # Schematic mountain top at 1.10 R_E for visual separation
        scale = r_px / R_EQ

        # Earth shaded disk + grid
        els.append(f'<circle cx="{cx}" cy="{cy}" r="{r_px}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
        els.append(f'<line x1="{cx - r_px}" y1="{cy}" x2="{cx + r_px}" y2="{cy}" stroke="{BLUE_LINE}" stroke-width="1" stroke-dasharray="3 3"/>')
        els.append(f'<line x1="{cx}" y1="{cy - r_px}" x2="{cx}" y2="{cy + r_px}" stroke="{BLUE_LINE}" stroke-width="1" stroke-dasharray="3 3"/>')
        els.append(txt(cx, cy + 4, "地球", 11.2, BLUE, "middle", weight="700"))

        # Mountain triangle at top
        peak_y = cy - r_mtn * scale
        els.append(f'<polygon points="{cx - 8},{cy - r_px + 1:.1f} {cx + 8},{cy - r_px + 1:.1f} {cx},{peak_y:.1f}" fill="{SLATE}" opacity="0.85"/>')

        # Sub-orbital A & B via RK4
        for v_sub, col, lbl, lx, ly in (
            (5.2, SLATE, "5.2 km/s 落回近处", cx + 68, cy - 42),
            (6.8, ORANGE, "6.8 km/s 绕半圈落地", cx + 76, cy + 36),
        ):
            pts = _integrate_ballistic(r_mtn, v_sub, dt=4.0, max_steps=2500)
            assert math.hypot(*pts[-1]) <= R_EQ + 1.0
            poly = " ".join(f"{cx + px * scale:.1f},{cy - py * scale:.1f}" for px, py in pts[::6] + [pts[-1]])
            els.append(f'<polyline points="{poly}" fill="none" stroke="{col}" stroke-width="1.8" stroke-dasharray="4 3"/>')
            hx, hy = cx + pts[-1][0] * scale, cy - pts[-1][1] * scale
            els.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="3.3" fill="{col}"/>')
            els.append(txt(lx, ly, lbl, 10.6, col, weight="600", halo=True))

        # Circular orbit at v_circ
        r_c_px = r_mtn * scale
        els.append(f'<circle cx="{cx}" cy="{cy}" r="{r_c_px:.1f}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
        els.append(txt(cx - 76, cy - 58, "v₁ ≈ 7.91 km/s", 11.0, BLUE, "middle", weight="700", halo=True))
        els.append(txt(cx - 76, cy - 43, "贴地闭合圆轨", 10.6, BLUE, "middle", halo=True))

        # Elliptical orbit (e = 0.21 -> r_a = r_p*(1+e)/(1-e))
        e_el = 0.21
        ra_px = r_c_px * (1.0 + e_el) / (1.0 - e_el)
        a_el = 0.5 * (r_c_px + ra_px)
        b_el = math.sqrt(a_el * a_el - (a_el - r_c_px) ** 2)
        cy_el = cy + (a_el - r_c_px)
        els.append(
            f'<ellipse cx="{cx:.1f}" cy="{cy_el:.1f}" rx="{b_el:.1f}" ry="{a_el:.1f}" '
            f'fill="none" stroke="{GREEN}" stroke-width="1.9" stroke-dasharray="6 3"/>'
        )
        els.append(txt(cx, cy_el + a_el + 16, "8.8 km/s → 椭圆轨道（远地点在下方）", 10.8, GREEN, "middle", weight="600", halo=True))
        els.append(txt(36, 344, "注：山高为示意放大；真实近地圆轨须在百公里以上避开大气。", 10.5, MUTED))

        # Right Panel: 1-second Earth curvature triangle proof
        els.append(card(388, 62, 352, 294))
        els.append(txt(404, 84, "② 1 秒钟几何账：平飞 7.91 km ↔ 地表弯落 4.90 m", 12.6, INK, weight="600"))

        # Schematic zoomed Earth arc
        ox, oy, r_arc = 452.0, 352.0, 214.0
        th_end = 0.86
        arc_pts = " ".join(
            f"{ox + r_arc * math.sin(th_end * i / 40):.1f},{oy - r_arc * math.cos(th_end * i / 40):.1f}"
            for i in range(41)
        )
        els.append(f'<path d="M {ox},{oy} L {arc_pts.split()[0]} {' '.join('L ' + p for p in arc_pts.split()[1:])} Z" fill="{BLUE_SOFT}" opacity="0.65"/>')
        els.append(f'<polyline points="{arc_pts}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')

        ax, ay = ox, oy - r_arc  # Top point A (452, 138)
        bx, by = ox + 172.0, ay  # Horizontal tangent point B (624, 138)
        ang_b = math.atan2(bx - ox, oy - by)
        cx_arc = ox + r_arc * math.sin(ang_b)
        cy_arc = oy - r_arc * math.cos(ang_b)

        # Radii OA and OB
        els.append(f'<line x1="{ox}" y1="{oy - 58}" x2="{ax}" y2="{ay}" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="{ox + 34:.1f}" y1="{oy - 58 * math.cos(ang_b):.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4 3"/>')

        # Horizontal inertial flight line A -> B
        els.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{INK}" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#arr-muted)"/>')
        # Gravity fall B -> C_arc along radial line
        els.append(f'<line x1="{bx:.1f}" y1="{by + 2:.1f}" x2="{cx_arc + 2:.1f}" y2="{cy_arc - 3:.1f}" stroke="{ORANGE}" stroke-width="2.3" marker-end="url(#arr-orange)"/>')
        # Actual circular orbit arc A -> C_arc
        sub_arc = " ".join(
            f"{ox + r_arc * math.sin(ang_b * i / 24):.1f},{oy - r_arc * math.cos(ang_b * i / 24):.1f}"
            for i in range(25)
        )
        els.append(f'<polyline points="{sub_arc}" fill="none" stroke="{GREEN}" stroke-width="2.6"/>')

        els.append(f'<circle cx="{ax}" cy="{ay}" r="4" fill="{BLUE}"/>')
        els.append(f'<circle cx="{cx_arc:.1f}" cy="{cy_arc:.1f}" r="4" fill="{GREEN}"/>')

        els.append(txt(538, 127, "若无引力：1 秒平飞 7.91 km", 11.2, INK, "middle", weight="600", halo=True))
        els.append(txt(630, 165, "引力拉拽下落", 11.0, ORANGE, weight="700", halo=True))
        els.append(txt(630, 181, "½gt² ≈ 4.90 m", 11.0, ORANGE, weight="700", halo=True))
        els.append(txt(462, 206, "地球半径 R_E", 10.8, SLATE, halo=True))
        els.append(txt(596, 228, "地表同步弯落 Δh ≈ v₁²/(2R_E) = 4.90 m", 10.6, BLUE, "middle", weight="600", halo=True))

        # Formula summary box
        els.append(card(404, 254, 320, 56, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(564, 274, "勾股展开：(R_E + Δh)² = R_E² + (v₁t)²", 11.3, INK, "middle", weight="600"))
        els.append(txt(564, 295, "⇒ Δh ≈ v₁²t²/(2R_E) = ½gt² ⇒ v₁ = √(gR_E) ≈ 7.91 km/s", 11.0, GREEN, "middle", weight="700"))
        els.append(txt(404, 344, "注：为看清 4.90 m 落差，右图竖直弯曲比例已放大示意。", 10.5, MUTED))

        svg = figure(
            372,
            "牛顿高山大炮思想实验与第一宇宙速度地球曲率推导",
            "左图用二体引力积分对比5.2、6.8、7.91与8.8 km/s四种水平初速度轨迹；右图用直角三角形证明平飞7.91 km时地表曲率弯落4.90 m恰等于1秒自由落体距离。",
            els,
        )
        write_svg(SUBDIR, "newton-cannon-freefall.svg", svg)

    # ==================================================================
    # SVG 2: Conic Velocity Ladder & Gravity Well Energy Ledger
    # ==================================================================
    def build_conic_ladder():
        els = header(
            "第一与第二宇宙速度：圆锥曲线轨道族与“√2 倍逃逸门槛”",
            "近地点同在地球附近时，速度每添一截，远地点就被甩得更远；动能翻倍（速度 ×√2）恰好爬平引力井",
        )

        clip_def = '<clipPath id="conic-box"><rect x="28" y="94" width="348" height="252" rx="6"/></clipPath>'

        # Left Panel: Exact two-body conic family r(theta) = rp*(1+e)/(1 + e*cos(theta))
        els.append(card(20, 62, 364, 322))
        els.append(txt(36, 84, "① 近地点点火速度决定轨道形状（焦点在球心）", 12.6, INK, weight="600"))
        els.append(card(28, 94, 348, 252, rx=6, fill="#f8fafc", stroke=BORDER))

        fx, fy = 110.0, 220.0
        rp_px = 25.0  # Perigee at (85, 220), apogees stretch right (+x)

        conic_group = ['<g clip-path="url(#conic-box)">']
        # Subtle axis line
        conic_group.append(f'<line x1="34" y1="{fy}" x2="370" y2="{fy}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')

        # 1) Circle e = 0 (v1 = 7.91 km/s)
        conic_group.append(f'<circle cx="{fx}" cy="{fy}" r="{rp_px}" fill="none" stroke="{BLUE}" stroke-width="2.1"/>')
        # Earth inside focus
        conic_group.append(f'<circle cx="{fx}" cy="{fy}" r="18" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.4"/>')
        conic_group.append(txt(fx, fy + 4, "地", 10.8, BLUE, "middle", weight="700"))

        # Helper to sample polar conic around focus (fx, fy) with perigee at (-rp_px, 0), so angle 0 points left (-x)
        def conic_poly(ecc, th_max, n=140):
            pts = []
            for i in range(-n, n + 1):
                th = th_max * i / n
                denom = 1.0 + ecc * math.cos(th)
                if denom <= 0.06:
                    continue
                r = rp_px * (1.0 + ecc) / denom
                # Perigee at (-rp_px, 0) => x = fx - r*cos(th), y = fy - r*sin(th)
                pts.append(f"{fx - r * math.cos(th):.1f},{fy - r * math.sin(th):.1f}")
            return " ".join(pts)

        # 2) Ellipse v = 9.50 km/s -> e = (9.50/v1)^2 - 1 = 0.444
        e_mid = (9.50 / v1) ** 2 - 1.0
        assert 0.44 < e_mid < 0.45
        conic_group.append(f'<polyline points="{conic_poly(e_mid, math.pi)}" fill="none" stroke="{GREEN}" stroke-width="1.9"/>')

        # 3) Stretched lunar transfer ellipse (schematic e = 0.815 so apogee lands inside box at x ≈ 355)
        e_lunar_vis = 0.815
        conic_group.append(
            f'<polyline points="{conic_poly(e_lunar_vis, math.pi)}" fill="none" stroke="{PURPLE}" stroke-width="2.0" stroke-dasharray="6 3"/>'
        )
        ap_lunar_x = fx + rp_px * (1.0 + e_lunar_vis) / (1.0 - e_lunar_vis)
        conic_group.append(f'<circle cx="{ap_lunar_x:.1f}" cy="{fy}" r="5.5" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.4"/>')
        conic_group.append(txt(ap_lunar_x - 2, fy - 10, "月", 10.5, PURPLE, "middle", weight="700", halo=True))

        # 4) Parabola e = 1.0 (v2 = 11.18 km/s)
        conic_group.append(f'<polyline points="{conic_poly(1.0, 2.38)}" fill="none" stroke="{ORANGE}" stroke-width="2.4"/>')

        # 5) Hyperbola e = (12.50/v1)^2 - 1 ≈ 1.50
        e_hyp = (12.50 / v1) ** 2 - 1.0
        max_th_hyp = math.acos(-1.0 / e_hyp) - 0.16
        conic_group.append(
            f'<polyline points="{conic_poly(e_hyp, max_th_hyp)}" fill="none" stroke="{SLATE}" stroke-width="1.9" stroke-dasharray="4 3"/>'
        )

        # Perigee burn marker
        conic_group.append(f'<circle cx="{fx - rp_px:.1f}" cy="{fy}" r="3.8" fill="{ORANGE}"/>')
        conic_group.append("</g>")
        els.extend(conic_group)

        # Crisp non-overlapping trajectory labels inside left box
        els.append(txt(54, 192, "近地点", 10.5, ORANGE, "middle", weight="700", halo=True))
        els.append(txt(92, 266, "7.91 圆轨(e=0)", 10.6, BLUE, "middle", weight="600", halo=True))
        els.append(txt(166, 178, "9.50 椭圆", 10.8, GREEN, "start", weight="600", halo=True))
        els.append(txt(222, 206, "≈10.9 奔月大椭圆(e<1)", 10.8, PURPLE, "start", weight="600", halo=True))
        els.append(txt(214, 136, "11.18 抛物线逃逸(e=1)", 10.8, ORANGE, "start", weight="700", halo=True))
        els.append(txt(168, 111, "12.50 双曲线逃逸(e>1)", 10.8, SLATE, "start", weight="600", halo=True))
        els.append(txt(32, 366, "注：真实月地距约 60 R_E，紫色奔月椭圆横向已压缩示意闭合端。", 10.5, MUTED))

        # Right Panel: Gravitational Potential Well U(r)/m = -GM_E / r & Energy Ladder
        els.append(card(396, 62, 344, 322))
        els.append(txt(412, 84, "② 引力势能井与比机械能分水岭（MJ/kg）", 12.6, INK, weight="600"))

        # Axes mapping: r/R_E in [1.0, 9.0] -> x in [456, 718]; E in [-66, +20] -> y in [326, 106]
        x0, x1 = 456.0, 718.0
        y_bot, y_top = 326.0, 106.0
        e_min, e_max = -66.0, 20.0

        def map_r(r_ratio):
            return x0 + (r_ratio - 1.0) / 8.0 * (x1 - x0)

        def map_e(e_val):
            return y_bot - (e_val - e_min) / (e_max - e_min) * (y_bot - y_top)

        y_zero = map_e(0.0)
        # Shaded bound well region below E = 0
        well_pts = []
        for i in range(81):
            rr = 1.0 + 8.0 * i / 80.0
            u_mj = -GM_E / (R_EQ * rr)  # km^2/s^2 == MJ/kg
            well_pts.append((map_r(rr), map_e(u_mj)))
        fill_d = (
            f"M {x0:.1f},{y_zero:.1f} "
            + " ".join(f"L {px:.1f},{py:.1f}" for px, py in well_pts)
            + f" L {x1:.1f},{y_zero:.1f} Z"
        )
        els.append(f'<path d="{fill_d}" fill="{BLUE_SOFT}" opacity="0.55"/>')
        els.append(
            f'<polyline points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in well_pts)}" '
            f'fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
        )

        # Left vertical wall r = 1 R_E & ticks
        els.append(f'<line x1="{x0}" y1="{y_top}" x2="{x0}" y2="{y_bot}" stroke="#94a3b8" stroke-width="1.3"/>')
        for ev, lbl in ((15.6, "+16"), (0.0, "0"), (-31.25, "-31.2"), (-62.49, "-62.5")):
            yy = map_e(ev)
            els.append(f'<line x1="{x0 - 4}" y1="{yy:.1f}" x2="{x0}" y2="{yy:.1f}" stroke="#94a3b8" stroke-width="1.2"/>')
            els.append(txt(x0 - 7, yy + 3.5, lbl, 10.5, MUTED, "end"))

        # Energy rungs
        rungs = [
            (+15.6, x1, SLATE, "4 3", "12.5 km/s：E > 0（双曲逃逸）", -5, x0 + 8),
            (0.0, x1, ORANGE, None, "v₂ = 11.18：E = 0（抛物线逃逸门槛）", -5, x0 + 8),
            (-2.1, x1 - 14, PURPLE, "5 3", "≈10.9 奔月：E ≈ −1 MJ/kg（仍束缚！）", 12, x0 + 8),
            (-17.4, map_r(62.49 / 17.4), GREEN, None, "9.50 椭圆：E = −17.4", -4, x0 + 8),
            (-31.25, map_r(2.0), BLUE, None, "v₁ = 7.91 圆轨：E = −31.2（半井深）", 4, map_r(2.0) + 6),
        ]
        for ev, x_end, col, dash, lbl, dy_txt, tx in rungs:
            yy = map_e(ev)
            d_attr = f' stroke-dasharray="{dash}"' if dash else ""
            els.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x_end:.1f}" y2="{yy:.1f}" stroke="{col}" stroke-width="1.7"{d_attr}/>')
            els.append(txt(tx, yy + dy_txt, lbl, 10.5, col, weight="600", halo=True))

        els.append(txt(536, 314, "地表井底 U(R_E) = −62.5 MJ/kg", 10.6, BLUE, weight="600", halo=True))
        els.append(card(412, 336, 312, 36, rx=6, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(568, 358, "圆轨动能 31.2 抵消半口井；逃逸需 62.5 ⇒ v₂ = √2 v₁", 11.0, ORANGE, "middle", weight="700"))

        svg = figure(
            404,
            "第一与第二宇宙速度的圆锥曲线轨道族及引力势能井",
            "左图精确绘制7.91圆轨、9.50椭圆、10.9奔月椭圆、11.18抛物线与12.50双曲线；右图在U(r)=-GM/r引力井中标出对应比机械能台阶，展示动能翻倍对应速度乘根号2。",
            els,
            extra_defs=clip_def,
        )
        write_svg(SUBDIR, "conic-velocity-ladder.svg", svg)

    # ==================================================================
    # SVG 3: High vs Low Orbit Speed-Energy Paradox
    # ==================================================================
    def build_speed_energy_paradox():
        els = header(
            "高低轨悖论：为什么飞得越高的卫星走得越慢，发上去却反而越费燃料？",
            "关键是拆开两本账：① 在轨巡航速度 v_orb = √(GM/r) 随高度下降；② 入轨总能量增量 ΔE 随高度飙升",
        )

        u_surf = -GM_E / R_EQ  # -62.495 MJ/kg
        cases = [
            ("近地空间站 LEO", "400 km", 400.0, BLUE, BLUE_SOFT),
            ("北斗中圆轨 MEO", "21,528 km", 21528.0, GREEN, GREEN_SOFT),
            ("静止卫星 GEO", "35,786 km", h_geo, ORANGE, ORANGE_SOFT),
        ]

        # Left Panel: v_orb(h) curve + 3 orbit callouts
        els.append(card(20, 62, 352, 314))
        els.append(txt(36, 84, "① 在轨运行速度 v_orb（越高引力越弱，越慢）", 12.6, INK, weight="600"))

        ox, oy, pw, ph = 66.0, 294.0, 282.0, 178.0
        h_max = 40000.0
        v_max = 8.5

        for yv in (2, 4, 6, 8):
            py = oy - (yv / v_max) * ph
            els.append(f'<line x1="{ox}" y1="{py:.1f}" x2="{ox + pw}" y2="{py:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(ox - 6, py + 3.5, f"{yv}", 10.5, MUTED, "end"))
        els.append(f'<path d="M{ox},{oy - ph} V{oy} H{ox + pw}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')
        els.append(txt(ox - 8, oy - ph - 6, "km/s", 10.5, MUTED, "end"))

        for hv, hlbl in ((0, "0"), (10000, "1万"), (20000, "2万"), (30000, "3万"), (40000, "4万 km")):
            px = ox + (hv / h_max) * pw
            els.append(txt(px, oy + 15, hlbl, 10.5, MUTED, "middle"))

        # Exact curve v_orb(h)
        curve_pts = []
        for i in range(101):
            hh = h_max * i / 100.0
            vv = math.sqrt(GM_E / (R_EQ + hh))
            curve_pts.append(f"{ox + (hh / h_max) * pw:.1f},{oy - (vv / v_max) * ph:.1f}")
        els.append(f'<polyline points="{" ".join(curve_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.3"/>')

        # Mark the 3 orbits (+ GPS note) with clean separation
        label_specs = [
            (10, -4, "start", "空间站"),
            (-4, -13, "end", "北斗"),
            (22, -11, "end", "静止轨"),
        ]
        for (name, h_str, hh, col, _), (dx, dy, anc, short_n) in zip(cases, label_specs):
            vv = math.sqrt(GM_E / (R_EQ + hh))
            px = ox + (hh / h_max) * pw
            py = oy - (vv / v_max) * ph
            els.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{oy}" stroke="{col}" stroke-width="1.2" stroke-dasharray="3 3"/>')
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{col}"/>')
            els.append(txt(px + dx, py + dy, f"{short_n} {vv:.2f} km/s", 10.8, col, anc, weight="700", halo=True))

        # Also subtle dot for GPS 20,200 km (3.87 km/s)
        v_gps = math.sqrt(GM_E / (R_EQ + 20200.0))
        gx = ox + (20200.0 / h_max) * pw
        gy = oy - (v_gps / v_max) * ph
        els.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="3.2" fill="{PURPLE}"/>')
        els.append(txt(gx - 8, gy + 19, f"GPS(20,200km): {v_gps:.2f}", 10.5, PURPLE, "end", halo=True))

        els.append(pill(36, 322, "GMm/r² = mv²/r ⇒ v_orb = √(GM/r)：轨道越高走得越慢", fg=BLUE, bg=BLUE_SOFT, w=320, h=22, size=10.8))
        els.append(txt(36, 362, "周期对比：空间站 1.54h · 北斗 12.9h · 静止轨 23h56m04s", 10.5, MUTED))

        # Right Panel: Stacked Energy Ledger (Potential climb dU + Orbital Kinetic K)
        els.append(card(388, 62, 352, 314))
        els.append(txt(404, 84, "② 地面送每千克卫星入轨的能量账（MJ/kg）", 12.6, INK, weight="600"))

        # Legend
        els.append(f'<rect x="404" y="96" width="11" height="11" rx="2" fill="{ORANGE}"/>')
        els.append(txt(420, 106, "爬高势能增量 ΔU", 10.8, BODY))
        els.append(f'<rect x="536" y="96" width="11" height="11" rx="2" fill="{BLUE}"/>')
        els.append(txt(552, 106, "在轨动能 K = ½v²", 10.8, BODY))

        bar_x = 404.0
        bar_max_w = 312.0
        e_scale_max = 64.0  # MJ/kg

        for idx, (name, h_str, hh, col, bg_s) in enumerate(cases):
            rr = R_EQ + hh
            u_orb = -GM_E / rr
            du = u_orb - u_surf            # Potential energy gained lifting from R_EQ to r
            k_orb = 0.5 * GM_E / rr        # Kinetic energy in circular orbit
            de_tot = du + k_orb            # Total energy added from rest on non-rotating Earth
            assert abs((u_orb + k_orb) - (-GM_E / (2.0 * rr))) < 1e-9

            ry = 122 + idx * 66
            els.append(txt(bar_x, ry + 12, f"{name}（{h_str}）", 11.4, INK, weight="600"))
            els.append(txt(bar_x + bar_max_w + 4, ry + 12, f"总计 +{de_tot:.1f} MJ/kg", 11.2, col, "end", weight="700"))

            w_du = (du / e_scale_max) * bar_max_w
            w_k = (k_orb / e_scale_max) * bar_max_w
            # Background track
            els.append(f'<rect x="{bar_x}" y="{ry + 19}" width="{bar_max_w}" height="22" rx="5" fill="{SLATE_SOFT}"/>')
            # Potential ΔU bar (left)
            els.append(f'<rect x="{bar_x}" y="{ry + 19}" width="{w_du:.1f}" height="22" rx="4" fill="{ORANGE}" opacity="0.88"/>')
            # Kinetic K bar (right)
            els.append(f'<rect x="{bar_x + w_du:.1f}" y="{ry + 19}" width="{w_k:.1f}" height="22" rx="4" fill="{BLUE}" opacity="0.88"/>')

            pct_u = round(100.0 * du / de_tot)
            pct_k = 100 - pct_u
            els.append(
                txt(
                    bar_x,
                    ry + 55,
                    f"爬高 {du:.1f} ({pct_u}%) + 动能 {k_orb:.1f} ({pct_k}%) → 在轨机械能 {u_orb + k_orb:.1f}",
                    10.5,
                    MUTED,
                )
            )

        els.append(pill(404, 322, "总机械能 E = −GMm/(2r)：越高动能越少，但爬井总账越贵！", fg=ORANGE, bg=ORANGE_SOFT, w=320, h=22, size=10.6))
        els.append(txt(404, 362, "注：以无自转地表静止（−62.5 MJ/kg）为基准，未计大气与重力损耗。", 10.5, MUTED))

        svg = figure(
            396,
            "卫星高低轨巡航速度与发射总能量悖论对比图",
            "左图展示400km空间站(7.67 km/s)、21528km北斗(3.78 km/s)与35786km静止卫星(3.07 km/s)随高度变慢；右图分解爬高势能与在轨动能，展示总注入能量从33.1升至57.8 MJ/kg。",
            els,
        )
        write_svg(SUBDIR, "speed-energy-paradox.svg", svg)

    # ==================================================================
    # SVG 4: Gravity Turn + 2-Burn Hohmann GEO Transfer (with CSS trace)
    # ==================================================================
    def build_hohmann_transfer():
        anim_css = """
      .trace-hohmann {
        stroke-dasharray: 290;
        stroke-dashoffset: 290;
        animation: hohmannDraw 2.4s ease-out 0.15s 1 forwards;
      }
      @keyframes hohmannDraw {
        to { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .trace-hohmann { animation: none; stroke-dashoffset: 0; }
      }"""

        els = header(
            "火箭怎么把卫星送上 35,786 km 静止轨道？程序转弯借自转 + 霍曼两次变轨",
            "先垂直穿大气再向东拐入 200 km 停泊圆轨，随后在近地点、远地点各点一把火完成“搭桥圆化”",
        )

        # Left Panel: 2-burn Hohmann Transfer Ellipse
        els.append(card(20, 62, 384, 330))
        els.append(txt(36, 84, "① 霍曼转移椭圆：两次点火接力（200 km → GEO）", 12.6, INK, weight="600"))

        fx, fy = 204.0, 224.0
        r_geo_px = 88.0
        r_leo_px = 24.0  # Inner ring enlarged slightly so 200 km parking orbit is distinct from Earth

        # Outer GEO circle
        els.append(
            f'<circle cx="{fx}" cy="{fy}" r="{r_geo_px}" fill="none" stroke="{GREEN}" '
            f'stroke-width="1.8" stroke-dasharray="5 3"/>'
        )
        # Inner LEO parking circle + Earth
        els.append(f'<circle cx="{fx}" cy="{fy}" r="{r_leo_px}" fill="none" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(f'<circle cx="{fx}" cy="{fy}" r="16" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.4"/>')
        els.append(txt(fx, fy + 4, "地球", 10.5, BLUE, "middle", weight="700"))

        # Transfer ellipse: perigee at (fx - r_leo_px, fy), apogee at (fx + r_geo_px, fy)
        a_px = 0.5 * (r_leo_px + r_geo_px)
        c_px = a_px - r_leo_px
        b_px = math.sqrt(a_px * a_px - c_px * c_px)
        ecx = fx + c_px

        # Lower return half (if 2nd burn fails -> falls back to LEO!)
        lower_pts = " ".join(
            f"{ecx + a_px * math.cos(math.pi * i / 60):.1f},{fy + b_px * math.sin(math.pi * i / 60):.1f}"
            for i in range(61)
        )
        els.append(f'<polyline points="{lower_pts}" fill="none" stroke="{HAIRLINE}" stroke-width="1.5" stroke-dasharray="4 4"/>')

        # Upper active transfer half (perigee pi -> apogee 0)
        upper_pts = " ".join(
            f"{ecx + a_px * math.cos(math.pi * (1.0 - i / 70.0)):.1f},{fy - b_px * math.sin(math.pi * (1.0 - i / 70.0)):.1f}"
            for i in range(71)
        )
        els.append(f'<polyline points="{upper_pts}" fill="none" stroke="{ORANGE}" stroke-opacity="0.45" stroke-width="2.0"/>')
        els.append(
            f'<polyline class="trace-hohmann" points="{upper_pts}" fill="none" stroke="{ORANGE}" '
            f'stroke-width="2.6" marker-end="url(#arr-orange)"/>'
        )

        # Burn 1 (Perigee) & Burn 2 (Apogee) markers + tangent velocity vectors
        px1, py1 = fx - r_leo_px, fy
        px2, py2 = fx + r_geo_px, fy
        els.append(f'<line x1="{px1}" y1="{py1}" x2="{px1}" y2="{py1 - 28}" stroke="{ORANGE}" stroke-width="2.1" marker-end="url(#arr-orange)"/>')
        els.append(f'<line x1="{px2}" y1="{py2}" x2="{px2}" y2="{py2 + 28}" stroke="{GREEN}" stroke-width="2.1" marker-end="url(#arr-green)"/>')
        els.append(step_badge(px1 - 13, py1 + 2, 1, fg=ORANGE, bg=ORANGE_SOFT, r=8.8))
        els.append(step_badge(px2 + 13, py2 - 2, 2, fg=GREEN, bg=GREEN_SOFT, r=8.8))

        # Labels cleanly outside the 88px GEO circle (x=116..292)
        els.append(txt(30, 198, "近地点点火①", 10.8, ORANGE, weight="700", halo=True))
        els.append(txt(30, 214, "Δv₁ = +2.46", 10.8, ORANGE, weight="700", halo=True))
        els.append(txt(30, 230, "7.78→10.24", 10.5, BODY, halo=True))

        els.append(txt(236, 166, "爬升 5小时16分", 10.6, ORANGE, "middle", weight="600", halo=True))
        els.append(txt(204, 122, "GEO 静止圆轨：35,786 km（v = 3.07 km/s）", 10.8, GREEN, "middle", weight="600", halo=True))

        els.append(txt(396, 190, "到顶剩 1.60", 10.5, BODY, "end", halo=True))
        els.append(txt(396, 206, "远地点点火②", 10.8, GREEN, "end", weight="700", halo=True))
        els.append(txt(396, 222, "Δv₂ = +1.48", 10.8, GREEN, "end", weight="700", halo=True))
        els.append(txt(396, 238, "圆化至 3.07", 10.5, GREEN, "end", halo=True))

        els.append(txt(204, 329, "若不点第②把火：卫星会沿灰虚线掉回 200 km 近地点", 10.5, MUTED, "middle", halo=True))
        els.append(pill(34, 354, "共面变轨总增量：Δv₁ + Δv₂ = 2.46 + 1.48 = 3.93 km/s", fg=BLUE, bg=BLUE_SOFT, w=356, h=22, size=10.8))

        # Right Panel: Gravity Turn + Eastward Rotation Boost by Latitude
        els.append(card(416, 62, 324, 330))
        els.append(txt(432, 84, "② 升空姿态与向东借自转“顺风车”", 12.6, INK, weight="600"))

        # Mini Gravity Turn box
        els.append(card(432, 96, 292, 108, rx=7, fill="#f8fafc", stroke=BORDER))
        els.append(f'<rect x="433" y="168" width="290" height="24" fill="{BLUE_SOFT}" opacity="0.6"/>')
        els.append(f'<line x1="433" y1="192" x2="723" y2="192" stroke="{SLATE}" stroke-width="1.4"/>')
        els.append(txt(714, 184, "底部稠密大气层", 10.5, BLUE, "end"))
        # Gravity turn curve
        els.append(
            f'<path d="M 462,192 C 462,154 482,126 688,122" fill="none" stroke="{ORANGE}" '
            f'stroke-width="2.4" marker-end="url(#arr-orange)"/>'
        )
        els.append(f'<circle cx="462" cy="192" r="3.5" fill="{ORANGE}"/>')
        els.append(f'<circle cx="490" cy="146" r="3.5" fill="{ORANGE}"/>')
        els.append(txt(478, 160, "① 先竖飞快穿大气", 10.6, INK, weight="600", halo=True))
        els.append(txt(552, 114, "② 向东程序转弯水平入轨", 10.6, ORANGE, weight="700", halo=True))
        els.append(txt(552, 140, "把推力全攒成水平环绕速度", 10.5, MUTED))

        # Latitude rotation speed bars: v_rot = 465.1 * cos(lat) m/s
        els.append(txt(432, 224, "地球自转线速度 v = 465 cos φ（越近赤道越快）", 11.2, INK, weight="600"))
        v_eq_ms = 2.0 * math.pi * R_EQ / T_SID * 1000.0
        sites = [
            ("赤道理想点 (0°)", 0.0, BLUE),
            ("海南文昌 (19.6°N)", 19.614, ORANGE),
            ("四川西昌 (28.2°N)", 28.246, GREEN),
            ("甘肃酒泉 (41.0°N)", 40.960, SLATE),
        ]
        for idx, (sname, lat_deg, col) in enumerate(sites):
            v_ms = v_eq_ms * math.cos(math.radians(lat_deg))
            ry = 236 + idx * 30
            bw = (v_ms / 500.0) * 112.0
            els.append(txt(432, ry + 14, sname, 10.7, BODY, weight="600" if idx == 1 else None))
            els.append(f'<rect x="550" y="{ry + 3}" width="114" height="14" rx="4" fill="{SLATE_SOFT}"/>')
            els.append(f'<rect x="550" y="{ry + 3}" width="{bw:.1f}" height="14" rx="4" fill="{col}" opacity="0.88"/>')
            els.append(txt(722, ry + 14, f"{v_ms:.0f} m/s", 10.6, col, "end", weight="700"))

        els.append(txt(432, 372, "文昌不仅多借自转，且离赤道面近、去静止轨省倾角燃料！", 10.5, ORANGE, weight="600"))

        svg = figure(
            412,
            "火箭程序转弯借地球自转与霍曼转移两次变轨飞向地球静止轨道",
            "左图按精确二体速度绘出200km停泊轨经Δv1=2.46 km/s进入转移椭圆、5小时16分后在35786km远地点经Δv2=1.48 km/s圆化；右图展示程序转弯与文昌等发射场纬度自转助推。",
            els,
            extra_css=anim_css,
        )
        write_svg(SUBDIR, "hohmann-geo-transfer.svg", svg)

    # ==================================================================
    # SVG 5: Third Cosmic Velocity (Heliocentric Tailwind + Pythagorean Energy)
    # ==================================================================
    def build_third_cosmic():
        els = header(
            "第三宇宙速度为什么只要 16.7 km/s，而不是逃离太阳所需的 42.1 km/s？",
            "先借地球公转 29.78 km/s 的顺风车，再用机械能守恒把“出井门槛 11.18”和“出井余速 12.34”勾股合成",
        )

        # Left Panel: Sun escape 42.12 vs Earth orbital tailwind 29.78
        els.append(card(20, 62, 352, 308))
        els.append(txt(36, 84, "① 太阳系账本：地球自带 29.78 km/s 顺风车", 12.6, INK, weight="600"))

        # Schematic Sun & 1 AU Earth orbit arc
        els.append(f'<circle cx="62" cy="186" r="19" fill="#fef3c7" stroke="#d97706" stroke-width="1.6"/>')
        els.append(txt(62, 190, "太阳", 10.8, "#b45309", "middle", weight="700"))
        els.append(f'<line x1="81" y1="186" x2="146" y2="186" stroke="{HAIRLINE}" stroke-width="1.2" stroke-dasharray="3 3"/>')
        els.append(txt(113, 179, "1 AU", 10.5, MUTED, "middle"))

        # Earth orbit arc passing through (156, 186) + velocity arrows
        els.append(f'<path d="M 136,220 A 118,118 0 0 0 136,104" fill="none" stroke="{BLUE_LINE}" stroke-width="1.5" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="156" y1="177" x2="156" y2="128" stroke="{BLUE}" stroke-width="2.3" marker-end="url(#arr-blue)"/>')
        els.append(f'<line x1="156" y1="126" x2="156" y2="102" stroke="{GREEN}" stroke-width="2.3" marker-end="url(#arr-green)"/>')
        els.append(f'<circle cx="156" cy="186" r="9" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
        els.append(txt(156, 210, "地球", 10.8, BLUE, "middle", weight="600"))
        els.append(txt(170, 156, "公转 29.78 km/s", 10.6, BLUE, weight="600"))
        els.append(txt(170, 118, "只需补 v_∞ = 12.34 km/s", 10.6, GREEN, weight="700"))
        els.append(txt(170, 134, "合速度即达 42.12 逃离太阳！", 10.5, BODY))

        # Horizontal velocity comparison bars to scale (max 42.12 km/s -> 296 px)
        bx0 = 40.0
        sc_v = 296.0 / v_sun_esc
        w_sun = v_sun_esc * sc_v
        w_e = v_earth * sc_v
        w_inf = v_inf * sc_v

        # Bar 1: Target 42.12 km/s
        els.append(txt(bx0, 240, "1 AU 处挣脱太阳引力门槛：√2 v_地 = 42.12 km/s", 10.8, INK, weight="600"))
        els.append(f'<rect x="{bx0}" y="246" width="{w_sun:.1f}" height="16" rx="4" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.2"/>')
        els.append(txt(bx0 + w_sun * 0.5, 258, "42.12 km/s（从静止硬逃太阳所需）", 10.5, ORANGE, "middle", weight="600"))

        # Bar 2: Earth's 29.78 + needed excess 12.34
        els.append(txt(bx0, 280, "顺着地球公转方向发射：白借 29.78 + 自备余速 12.34", 10.8, INK, weight="600"))
        els.append(f'<rect x="{bx0}" y="286" width="{w_e:.1f}" height="16" rx="4" fill="{BLUE}"/>')
        els.append(f'<rect x="{bx0 + w_e:.1f}" y="286" width="{w_inf:.1f}" height="16" rx="4" fill="{GREEN}"/>')
        els.append(txt(bx0 + w_e * 0.5, 298, "地球公转 29.78", 10.5, "#ffffff", "middle", weight="600"))
        els.append(txt(bx0 + w_e + w_inf * 0.5, 298, "+12.34", 10.5, "#ffffff", "middle", weight="700"))

        # Slingshot note card
        els.append(card(36, 314, 320, 42, rx=6, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(196, 331, "旅行者 1/2 号省油秘籍：借木星“引力弹弓”再蹭公转速度，", 10.5, PURPLE, "middle", weight="600"))
        els.append(txt(196, 347, "无需地面硬烧满 16.65 km/s 就踏上了飞出太阳系的单程票！", 10.5, PURPLE, "middle"))

        # Right Panel: Exact Energy Pythagorean Triangle v3 = sqrt(v2^2 + v_inf^2)
        els.append(card(388, 62, 352, 308))
        els.append(txt(404, 84, "② 出地心引力井：动能相加 ⇒ 速度走“勾股斜边”！", 12.6, INK, weight="600"))

        # Right triangle with legs proportional to v2 = 11.18 and v_inf = 12.34
        # Scale: 12.5 px per km/s -> leg_x = 139.8 px, leg_y = 154.2 px
        tx0, ty0 = 446.0, 268.0
        lx = v2 * 12.2       # ~136.4 px
        ly = v_inf * 11.2    # ~138.2 px
        tx1, ty1 = tx0 + lx, ty0
        tx2, ty2 = tx1, ty0 - ly

        # Shaded triangle + right-angle square
        els.append(f'<polygon points="{tx0:.1f},{ty0:.1f} {tx1:.1f},{ty1:.1f} {tx2:.1f},{ty2:.1f}" fill="{BLUE_SOFT}" opacity="0.55"/>')
        els.append(f'<polyline points="{tx1 - 11:.1f},{ty1:.1f} {tx1 - 11:.1f},{ty1 - 11:.1f} {tx1:.1f},{ty1 - 11:.1f}" fill="none" stroke="{SLATE}" stroke-width="1.2"/>')

        # Leg 1 (bottom): v2 = 11.18
        els.append(f'<line x1="{tx0:.1f}" y1="{ty0:.1f}" x2="{tx1:.1f}" y2="{ty1:.1f}" stroke="{ORANGE}" stroke-width="2.4"/>')
        # Leg 2 (right vertical): v_inf = 12.34
        els.append(f'<line x1="{tx1:.1f}" y1="{ty1:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" stroke="{GREEN}" stroke-width="2.4"/>')
        # Hypotenuse: v3 = 16.65
        els.append(f'<line x1="{tx0:.1f}" y1="{ty0:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" stroke="{BLUE}" stroke-width="3.0"/>')

        els.append(txt((tx0 + tx1) / 2, ty0 + 18, "v₂ = 11.18 km/s（填平地球井）", 10.8, ORANGE, "middle", weight="700"))
        els.append(txt(tx1 + 8, (ty1 + ty2) / 2 - 4, "出井对地余速", 10.8, GREEN, weight="600"))
        els.append(txt(tx1 + 8, (ty1 + ty2) / 2 + 13, "v_∞ = 12.34 km/s", 10.8, GREEN, weight="700"))

        els.append(txt(tx0 + 34, ty0 - 92, "v₃ = 16.65 km/s", 11.8, BLUE, "middle", weight="700", halo=True))
        els.append(txt(tx0 + 34, ty0 - 76, "(教科书约 16.7)", 10.5, BLUE, "middle", halo=True))

        # Equation & misconception comparison box
        els.append(card(404, 296, 320, 60, rx=6, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(564, 315, "守恒律：½v₃² − ½v₂² = ½v_∞² ⇒ v₃ = √(v₂² + v_∞²)", 10.6, INK, "middle", weight="600"))
        els.append(txt(564, 334, "误区对比：不是 11.18 + 12.34 = 23.52！井底省下近 7 km/s", 10.5, GREEN, "middle", weight="700"))
        els.append(txt(564, 350, "（高速井底点火动能收益倍增——即“奥伯特效应”）", 10.5, MUTED, "middle"))

        svg = figure(
            388,
            "第三宇宙速度的公转顺风车与能量勾股合成原理",
            "左图对比1AU太阳逃逸速度42.12 km/s与地球公转29.78 km/s，得出对地双曲余速v_inf=12.34 km/s；右图用直角三角形展示v3=sqrt(11.18^2+12.34^2)=16.65 km/s。",
            els,
        )
        write_svg(SUBDIR, "third-cosmic-vector.svg", svg)

    # ==================================================================
    # SVG 6: Tsiolkovsky Rocket Equation & Multi-Stage Comparison
    # ==================================================================
    def build_rocket_staging():
        els = header(
            "齐奥尔科夫斯基公式与多级火箭：为什么火箭 90% 是燃料，还非得边飞边扔壳？",
            "Δv = v_e ln(m₀/m_f) 意味着质量比随目标速度呈指数爆炸；半途扔掉空油箱，才能打破单级死胡同",
        )

        # Left Panel: Exponential Mass Ratio Wall
        els.append(card(20, 62, 360, 314))
        els.append(txt(36, 84, "① 理想火箭方程曲线：Δv = v_e ln(m₀ / m_f)", 12.6, INK, weight="600"))

        ox, oy, pw, ph = 66.0, 294.0, 290.0, 178.0
        mr_max = 22.0
        dv_max = 13.0

        for yv in (3, 6, 9, 12):
            py = oy - (yv / dv_max) * ph
            els.append(f'<line x1="{ox}" y1="{py:.1f}" x2="{ox + pw}" y2="{py:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(ox - 6, py + 3.5, f"{yv}", 10.5, MUTED, "end"))
        els.append(f'<path d="M{ox},{oy - ph} V{oy} H{ox + pw}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')
        els.append(txt(ox - 6, oy - ph - 6, "Δv(km/s)", 10.5, MUTED, "end"))

        for xv, xlbl in ((1, "1"), (5, "5(80%)"), (10, "10(90%)"), (15, "15"), (20, "20(95%燃料)")):
            px = ox + ((xv - 1.0) / (mr_max - 1.0)) * pw
            els.append(txt(px, oy + 15, xlbl, 10.5, MUTED, "middle"))

        # LEO practical budget line (~9.3 km/s including ~1.5 km/s gravity & drag loss)
        y_leo_budget = oy - (9.3 / dv_max) * ph
        els.append(
            f'<line x1="{ox}" y1="{y_leo_budget:.1f}" x2="{ox + pw}" y2="{y_leo_budget:.1f}" '
            f'stroke="{GREEN}" stroke-width="1.5" stroke-dasharray="5 3"/>'
        )
        els.append(txt(ox + pw - 4, y_leo_budget - 5, "近地入轨实战预算 ≈ 9.3 km/s", 10.5, GREEN, "end", weight="700", halo=True))

        # Plot hydrolox (ve=4.4) and kerolox (ve=3.1)
        for ve_val, col, lbl, lx, ly in (
            (ve_hydro, BLUE, "液氧液氢 (v_e≈4.4)", ox + 62, 128),
            (ve_kero, ORANGE, "液氧煤油 (v_e≈3.1)", ox + 150, 226),
        ):
            pts = []
            for i in range(101):
                mr = 1.0 + (mr_max - 1.0) * i / 100.0
                dv = ve_val * math.log(mr)
                if dv <= dv_max:
                    pts.append(f"{ox + ((mr - 1.0) / (mr_max - 1.0)) * pw:.1f},{oy - (dv / dv_max) * ph:.1f}")
            els.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.2"/>')
            els.append(txt(lx, ly, lbl, 10.8, col, weight="700", halo=True))

        # Highlight kerolox crossing 9.3 km/s at MR = e^(9.3/3.1) = e^3 = 20.09!
        mr_cross = math.exp(9.3 / ve_kero)
        cx_cross = ox + ((mr_cross - 1.0) / (mr_max - 1.0)) * pw
        els.append(f'<circle cx="{cx_cross:.1f}" cy="{y_leo_budget:.1f}" r="4.2" fill="{ORANGE}"/>')
        els.append(txt(cx_cross - 6, y_leo_budget + 16, "m₀/m_f ≈ 20.1", 10.6, ORANGE, "end", weight="700", halo=True))

        els.append(pill(36, 322, "横轴 m₀/m_f = 起飞总重÷燃尽干重：对数增长慢 ⇔ 燃料指数暴涨", fg=ORANGE, bg=ORANGE_SOFT, w=328, h=22, size=10.5))
        els.append(txt(36, 362, "实战 Δv ≈ 7.8 轨道速度 + 1.5 重力与空气阻力损耗 ≈ 9.3 km/s", 10.5, MUTED))

        # Right Panel: Same 100t rocket, 2t satellite, ve=3.1, 10% tank structure -> 1 vs 2 vs 3 stages
        els.append(card(392, 62, 348, 314))
        els.append(txt(408, 84, "② 同样 100 吨起飞送 2 吨卫星：为什么要分级？", 12.6, INK, weight="600"))
        els.append(txt(408, 101, "统一条件：v_e = 3.1 km/s，壳重占各子级 10%", 10.5, MUTED))

        stage_cases = [
            ("单级硬飞（不扔空壳）", dv_1stage, "末段死背 9.8t 大空箱 → 差一大截坠海", SLATE, SLATE_SOFT),
            ("两级接力（扔 8.2t 一级壳）", dv_2stage, "4.15 + 4.99 km/s → 轻装二级跨过入轨线", BLUE, BLUE_SOFT),
            ("三级接力（连扔两级空壳）", dv_3stage, "3.48 + 3.24 + 3.19 km/s → 轻松入轨有富余", GREEN, GREEN_SOFT),
        ]

        bx = 408.0
        bmax = 314.0
        dv_bar_max = 11.0
        x_thresh = bx + (9.1 / dv_bar_max) * bmax
        els.append(txt(x_thresh, 116, "入轨线 ~9.1", 10.5, ORANGE, "middle", weight="700", halo=True))

        for idx, (st_name, dv_val, note_s, col, bg_c) in enumerate(stage_cases):
            ry = 126 + idx * 64
            els.append(txt(bx, ry + 12, st_name, 11.3, INK, weight="600"))
            els.append(txt(bx + bmax, ry + 12, f"Δv = {dv_val:.2f} km/s", 11.3, col, "end", weight="700"))
            els.append(f'<rect x="{bx}" y="{ry + 18}" width="{bmax}" height="19" rx="5" fill="{SLATE_SOFT}"/>')
            bw = (dv_val / dv_bar_max) * bmax
            els.append(f'<rect x="{bx}" y="{ry + 18}" width="{bw:.1f}" height="19" rx="5" fill="{col}" opacity="0.88"/>')
            els.append(txt(bx, ry + 51, note_s, 10.5, MUTED))

        # Threshold dashed vertical line across bars
        els.append(f'<line x1="{x_thresh:.1f}" y1="121" x2="{x_thresh:.1f}" y2="296" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="4 3"/>')

        els.append(pill(408, 322, "分级本质：烧完一段油就扔一段空罐，不再花燃料加速废铁！", fg=GREEN, bg=GREEN_SOFT, w=316, h=22, size=10.6))
        els.append(txt(408, 362, "齐奥尔科夫斯基 1903 推导方程，1929 提出“多级火箭列车”构想。", 10.5, MUTED))

        svg = figure(
            396,
            "齐奥尔科夫斯基理想火箭方程指数曲线与单级两级三级火箭速度增量对比",
            "左图绘制液氧煤油(ve=3.1)与液氧液氢(ve=4.4)的Δv对质量比曲线；右图对比同为100吨起飞、2吨载荷、10%结构系数下单级(6.62 km/s)、两级(9.10 km/s)与三级(9.91 km/s)的表现。",
            els,
        )
        write_svg(SUBDIR, "rocket-staging-curve.svg", svg)

    build_newton_cannon()
    build_conic_ladder()
    build_speed_energy_paradox()
    build_hohmann_transfer()
    build_third_cosmic()
    build_rocket_staging()

def _register_calendar_astronomy():
    import datetime

    import math

    from .core import (
        BLUE,
        BLUE_LINE,
        BLUE_SOFT,
        BODY,
        BORDER,
        GREEN,
        GREEN_SOFT,
        HAIRLINE,
        INK,
        MUTED,
        ORANGE,
        ORANGE_SOFT,
        PANEL_TITLE,
        PURPLE,
        PURPLE_SOFT,
        SLATE,
        SLATE_SOFT,
        WIDTH,
        audit_all_svgs,
        card,
        figure,
        header,
        pill,
        register,
        step_badge,
        txt,
        write_svg,
    )

    SUBDIR = "calendar-astronomy"

    def _meeus_new_moon_utc8(k):
        """Compute true New Moon instant (JD UTC and UTC+8 datetime) via Meeus Ch. 49."""
        T = k / 1236.85
        jde = (
            2451550.09766
            + 29.530588861 * k
            + 0.00015437 * T**2
            - 0.000000150 * T**3
            + 0.00000000073 * T**4
        )
        e_fac = 1.0 - 0.002516 * T - 0.0000074 * T**2
        m_sun = math.radians((2.5534 + 29.10535670 * k - 0.0000014 * T**2 - 0.00000011 * T**3) % 360.0)
        m_moon = math.radians(
            (201.5643 + 385.81693528 * k + 0.0107582 * T**2 + 0.00001238 * T**3 - 0.000000058 * T**4) % 360.0
        )
        f_arg = math.radians(
            (160.7108 + 390.67050284 * k - 0.0016118 * T**2 - 0.00000227 * T**3 + 0.000000011 * T**4) % 360.0
        )
        omega = math.radians((124.7746 - 1.56375588 * k + 0.0020672 * T**2 + 0.00000215 * T**3) % 360.0)
        corr = (
            -0.40720 * math.sin(m_moon)
            + 0.17241 * e_fac * math.sin(m_sun)
            + 0.01608 * math.sin(2 * m_moon)
            + 0.01039 * math.sin(2 * f_arg)
            + 0.00739 * e_fac * math.sin(m_moon - m_sun)
            - 0.00514 * e_fac * math.sin(m_moon + m_sun)
            + 0.00208 * e_fac * e_fac * math.sin(2 * m_sun)
            - 0.00111 * math.sin(m_moon - 2 * f_arg)
            - 0.00057 * math.sin(m_moon + 2 * f_arg)
            + 0.00056 * math.sin(2 * m_moon + m_sun)
            - 0.00042 * math.sin(3 * m_moon)
            + 0.00042 * math.sin(m_sun + 2 * f_arg)
            + 0.00038 * math.sin(m_sun - 2 * f_arg)
            - 0.00024 * math.sin(2 * m_moon - m_sun)
            - 0.00017 * math.sin(omega)
        )
        jd_utc = jde + corr - 69.5 / 86400.0
        dt_utc8 = datetime.datetime(2000, 1, 1, 12, 0, 0) + datetime.timedelta(
            days=jd_utc - 2451545.0, hours=8
        )
        return jd_utc, dt_utc8

    def _sun_apparent_lon_deg(jd):
        """Apparent geocentric solar ecliptic longitude (degrees) via Meeus Ch. 25."""
        T = (jd - 2451545.0) / 36525.0
        l0 = (280.46646 + 36000.76983 * T + 0.0003032 * T * T) % 360.0
        m = math.radians((357.52911 + 35999.05029 * T - 0.0001537 * T * T) % 360.0)
        c = (
            (1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(m)
            + (0.019993 - 0.000101 * T) * math.sin(2 * m)
            + 0.000289 * math.sin(3 * m)
        )
        omega = math.radians(125.04 - 1934.136 * T)
        return (l0 + c - 0.00569 - 0.00478 * math.sin(omega)) % 360.0

    def _find_solar_term_jd(target_deg, jd_guess):
        jd = jd_guess
        for _ in range(18):
            diff = (_sun_apparent_lon_deg(jd) - target_deg + 180.0) % 360.0 - 180.0
            jd -= diff / 0.9856
        assert abs((_sun_apparent_lon_deg(jd) - target_deg + 180.0) % 360.0 - 180.0) < 1e-6
        return jd

    def _build_gregorian_leap_sieve():
        """SVG 1: Julian +0.00781 d/yr drift (1582 jump) vs Gregorian 97/400 sieve."""
        t_trop = 365.24219
        t_jul = 365.25
        t_greg = 365.0 + 97.0 / 400.0

        jul_err_d = t_jul - t_trop
        jul_err_s = jul_err_d * 86400.0
        greg_err_d = t_greg - t_trop
        greg_err_s = greg_err_d * 86400.0

        assert math.isclose(jul_err_d, 0.00781, abs_tol=1e-5)
        assert 674.0 < jul_err_s < 676.0  # 11 min 14.8 s
        assert math.isclose(t_greg, 365.2425, abs_tol=1e-9)
        assert 26.5 < greg_err_s < 27.1
        drift_1582 = (1582 - 325) * jul_err_d
        assert 9.80 < drift_1582 < 9.85

        els = header(
            "格里高利历的“三道筛子”：把每年 11 分 15 秒的滑移压到 27 秒",
            "儒略历每 128 年多攒 1 天，至 1582 年被迫连删 10 天；公历靠“四闰、百不闰、四百再闰”锁定春分",
        )

        # Left panel: Julian drift + 1582 calendar strip
        els.append(card(20, 62, 356, 326))
        els.append(txt(36, 85, "① 儒略历滑移与 1582 年“消失的十天”", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 104, "平均 365.25 天比回归年多 11 分 15 秒，约 128 年偏后 1 天", 11.0, MUTED))

        ox, oy, cw, ch = 68.0, 246.0, 282.0, 114.0
        # Gridlines for 0, 5, 10 days
        for yd in (0, 5, 10):
            py = oy - (yd / 10.5) * ch
            els.append(f'<line x1="{ox}" y1="{py:.1f}" x2="{ox + cw}" y2="{py:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(ox - 7, py + 4, f"{yd}天", 10.6, MUTED, "end"))
        els.append(f'<path d="M{ox},{oy - ch:.1f} V{oy} H{ox + cw:.1f}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')

        # X ticks: 325, 950, 1582
        for yr, lbl, anc in ((325, "325年(尼西亚)", "start"), (950, "950年", "middle"), (1582, "1582年", "end")):
            px = ox + ((yr - 325.0) / (1582.0 - 325.0)) * cw
            els.append(f'<line x1="{px:.1f}" y1="{oy}" x2="{px:.1f}" y2="{oy + 4}" stroke="#94a3b8" stroke-width="1.2"/>')
            els.append(txt(px, oy + 17, lbl, 10.5, MUTED, anc))

        # Shaded Julian error triangle & line
        y_end = oy - (drift_1582 / 10.5) * ch
        els.append(
            f'<polygon points="{ox},{oy} {ox + cw},{y_end:.1f} {ox + cw},{oy}" fill="{ORANGE_SOFT}" opacity="0.85"/>'
        )
        els.append(
            f'<line x1="{ox}" y1="{oy}" x2="{ox + cw}" y2="{y_end:.1f}" stroke="{ORANGE}" stroke-width="2.5"/>'
        )
        els.append(f'<circle cx="{ox}" cy="{oy}" r="4" fill="{BLUE}"/>')
        els.append(f'<circle cx="{ox + cw}" cy="{y_end:.1f}" r="4.5" fill="{ORANGE}"/>')
        els.append(
            txt(
                ox + cw - 8,
                y_end - 8,
                f"1257 年累计 +{drift_1582:.1f} 天 → 删 10 天校准",
                10.8,
                ORANGE,
                "end",
                weight="700",
                halo=True,
            )
        )
        # Gregorian near-flat reference slope over same span (1257 * 0.00031 = 0.39 d)
        y_greg = oy - ((1257 * greg_err_d) / 10.5) * ch
        els.append(
            f'<line x1="{ox}" y1="{oy}" x2="{ox + cw}" y2="{y_greg:.1f}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 3"/>'
        )
        els.append(txt(ox + 10, oy - 10, "虚线：若用公历同期仅漂移 0.39 天", 10.5, GREEN, weight="600", halo=True))

        # 1582 October strip
        els.append(card(34, 274, 328, 100, rx=8, fill="#f8fafc", stroke=HAIRLINE))
        els.append(txt(46, 293, "1582 年 10 月改历手术：日期跳十格，星期不断裂！", 11.2, INK, weight="700"))

        # Day tiles: 10/3 Wed, 10/4 Thu, [Skipped 10d], 10/15 Fri
        els.append(card(44, 304, 62, 46, rx=6, fill="#ffffff", stroke=BORDER))
        els.append(txt(75, 323, "10月3日", 10.8, BODY, "middle", weight="600"))
        els.append(txt(75, 341, "星期三", 10.5, MUTED, "middle"))

        els.append(card(112, 304, 66, 46, rx=6, fill=BLUE_SOFT, stroke=BLUE, sw=1.3))
        els.append(txt(145, 323, "10月4日", 10.8, BLUE, "middle", weight="700"))
        els.append(txt(145, 341, "星期四", 10.6, BLUE, "middle", weight="600"))

        els.append(card(184, 304, 92, 46, rx=6, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.2, dash="4 3"))
        els.append(txt(230, 323, "删 10/5–10/14", 10.6, ORANGE, "middle", weight="700"))
        els.append(txt(230, 341, "10 天不存在", 10.5, ORANGE, "middle"))

        els.append(card(282, 304, 70, 46, rx=6, fill=GREEN_SOFT, stroke=GREEN, sw=1.3))
        els.append(txt(317, 323, "10月15日", 10.8, GREEN, "middle", weight="700"))
        els.append(txt(317, 341, "星期五", 10.6, GREEN, "middle", weight="600"))

        els.append(txt(198, 366, "注：周四睡一觉醒来仍是周五，七日星期循环从未中断", 10.5, MUTED, "middle"))

        # Right panel: 400-year 97-leap sieve
        els.append(card(388, 62, 352, 326))
        els.append(txt(404, 85, "② 400 年 97 闰的“三道筛子”", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 104, "拿任意连续 400 年（如 1601—2000 年）过筛计闰：", 11.0, MUTED))

        steps = [
            (
                "第一筛：4 年一闰（能被 4 整除）",
                "400 ÷ 4 = 初选 100 个闰年 → 均长 365.2500 天",
                BLUE,
                BLUE_SOFT,
            ),
            (
                "第二筛：百年不闰（剔除整百年）",
                "筛掉 1700、1800、1900 共 3 年（全剔4年反慢3分09秒）",
                ORANGE,
                ORANGE_SOFT,
            ),
            (
                "第三筛：400 年再闰（保送 2000 年）",
                "100 − 3 = 97 闰！均长 365.2425 天（仅快 26.8 秒）",
                GREEN,
                GREEN_SOFT,
            ),
        ]
        for idx, (st_head, st_sub, fg, bg) in enumerate(steps):
            ry = 116 + idx * 60
            els.append(card(404, ry, 320, 50, rx=8, fill=bg, stroke=fg, sw=1.2))
            els.append(step_badge(423, ry + 25, idx + 1, fg=fg, bg="#ffffff", r=10))
            els.append(txt(441, ry + 20, st_head, 11.6, INK, weight="700"))
            els.append(txt(441, ry + 39, st_sub, 10.8, BODY))

        # Residual bar comparison box
        els.append(card(404, 298, 320, 76, rx=8, fill="#f8fafc", stroke=HAIRLINE))
        els.append(txt(416, 317, "每年相对真回归年（365.24219 天）误差压缩 25 倍：", 11.0, INK, weight="700"))

        bar_x = 496.0
        max_bar_w = 138.0
        w_jul = max_bar_w
        w_greg = max_bar_w * (greg_err_s / jul_err_s)
        els.append(txt(416, 339, "儒略历", 10.8, BODY, weight="600"))
        els.append(f'<rect x="{bar_x}" y="328" width="{w_jul:.1f}" height="13" rx="3" fill="{ORANGE}"/>')
        els.append(txt(bar_x + w_jul + 6, 339, "+675 秒/年", 10.6, ORANGE, weight="700"))

        els.append(txt(416, 361, "现行公历", 10.8, BODY, weight="600"))
        els.append(f'<rect x="{bar_x}" y="350" width="{w_greg:.1f}" height="13" rx="3" fill="{GREEN}"/>')
        els.append(txt(bar_x + w_greg + 6, 361, "+26.8 秒/年（约 3226 年才差 1 天）", 10.6, GREEN, weight="700"))

        return figure(
            402,
            "格里高利历三层闰年筛法与1582年十天校准图",
            "左图展示儒略历每年多算11分15秒导致1582年累计约9.8天滑移并跳过10月5日至14日共10天而星期不断裂；右图展示公历400年97闰三道筛子将年误差压缩至26.8秒。",
            els,
        )

    def _build_continuous_no_30_chuxi():
        """SVG 2: Why 2025-2029 have 5 consecutive years without 大年三十, and 2030 brings it back."""
        # k indices for 腊月初一 before 2025, 2026, 2027, 2028, 2029, 2030 Spring Festivals
        cases = [
            (309, "2025 乙巳蛇年春节前"),
            (322, "2026 丙午马年春节前"),
            (334, "2027 丁未羊年春节前"),
            (346, "2028 戊申猴年春节前"),
            (359, "2029 己酉鸡年春节前"),
            (371, "2030 庚戌狗年春节前"),
        ]

        computed = []
        for k, label in cases:
            jd1, dt1 = _meeus_new_moon_utc8(k)
            jd2, dt2 = _meeus_new_moon_utc8(k + 1)
            cal_days = (dt2.date() - dt1.date()).days
            t0_h = dt1.hour + dt1.minute / 60.0 + dt1.second / 3600.0
            dur_d = jd2 - jd1
            delta_h = (dur_d - 29.0) * 24.0
            total_h = t0_h + delta_h
            computed.append((label, dt1, dt2, cal_days, t0_h, delta_h, total_h))

        # Critical astronomical assertions
        assert [c[3] for c in computed] == [29, 29, 29, 29, 29, 30]
        # 2027 misses midnight by ~4 minutes; 2030 crosses midnight by ~8 minutes even though t0 < 11.26h!
        assert 23.90 < computed[2][6] < 23.98
        assert computed[5][4] < 11.0 and 24.08 < computed[5][6] < 24.20

        els = header(
            "定朔与午夜红线：为什么 2025—2029 连续五年没有“大年三十”？",
            "按国家标准 GB/T 33661-2017，合朔落入哪天哪天就是初一；腊月能否保住第 30 天，全看下一次合朔跨不跨午夜",
        )

        # Top panel: Visual explanation of t0 + Δh vs 24:00 midnight boundary
        els.append(card(20, 62, 720, 118))
        els.append(txt(36, 84, "① 判定公式：从腊月初一 00:00 起算，下一次合朔能否撑过第 30 天末的午夜 24:00？", PANEL_TITLE, INK, weight="700"))

        # Schematic timeline bar
        els.append(card(36, 96, 134, 28, rx=5, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(103, 114, "t₀：初一合朔时刻", 11.0, BLUE, "middle", weight="700"))
        els.append(txt(180, 115, "+", 14, INK, "middle", weight="700"))
        els.append(card(192, 96, 248, 28, rx=5, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(316, 114, "真实朔望月 = 29 整天 + Δh 小时 (6.4–20.2h)", 10.9, ORANGE, "middle", weight="700"))
        els.append(txt(454, 115, "vs", 12, MUTED, "middle", weight="700"))
        els.append(card(470, 96, 254, 28, rx=5, fill="#fef2f2", stroke="#dc2626", sw=1.3))
        els.append(txt(597, 114, "第 30 天午夜红线：t₀ + Δh = 24.0 小时", 11.0, "#b91c1c", "middle", weight="700"))

        els.append(
            txt(
                36,
                146,
                "• 若 t₀ + Δh < 24h：新月落回第 30 天内 → 第 30 天直接变成“正月初一”，腊月只剩 29 天（除夕为腊月廿九）！",
                11.0,
                BODY,
            )
        )
        els.append(
            txt(
                36,
                166,
                "• 若 t₀ + Δh ≥ 24h：新月跨过午夜进入第 31 天 → 第 30 天顺利留给腊月，迎来“大年三十”（如 2030 年）！",
                11.0,
                GREEN,
                weight="600",
            )
        )

        # Bottom panel: 6-year exact stacked bars
        els.append(card(20, 192, 720, 248))
        els.append(
            txt(
                36,
                215,
                "② 2025—2030 连续六年腊月实算对表（东八区北京时间，注意 2027 差 4 分钟与 2030 跨 8 分钟！）",
                PANEL_TITLE,
                INK,
                weight="700",
            )
        )

        ox = 182.0
        scale = 12.2  # px per hour (24h -> 292.8px, x_mid = 474.8)
        x_mid = ox + 24.0 * scale

        # Hour axis gridlines (0, 6, 12, 18, 24h)
        for hr in (0, 6, 12, 18):
            hx = ox + hr * scale
            els.append(f'<line x1="{hx:.1f}" y1="230" x2="{hx:.1f}" y2="394" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(hx, 409, f"{hr}h", 10.5, MUTED, "middle"))

        for idx, (label, dt1, dt2, cal_days, t0_h, delta_h, total_h) in enumerate(computed):
            ry = 236 + idx * 26
            is_30 = cal_days == 30
            els.append(txt(34, ry + 15, label, 10.8, INK if not is_30 else GREEN, weight="700" if is_30 else "600"))

            w1 = t0_h * scale
            w2 = delta_h * scale
            els.append(f'<rect x="{ox:.1f}" y="{ry + 3}" width="{w1:.1f}" height="16" rx="2" fill="{BLUE}"/>')
            els.append(
                f'<rect x="{ox + w1:.1f}" y="{ry + 3}" width="{w2:.1f}" height="16" rx="2" '
                f'fill="{GREEN if is_30 else ORANGE}" opacity="0.88"/>'
            )
            if w1 > 42:
                els.append(txt(ox + w1 / 2, ry + 15, f"{t0_h:.1f}h", 10.2, "#ffffff", "middle", weight="700"))
            els.append(txt(ox + w1 + w2 / 2, ry + 15, f"+{delta_h:.1f}h", 10.2, "#ffffff", "middle", weight="700"))

            # Verdict text on right (safely inside x <= 732)
            if idx == 2:
                verdict = f"初一 {dt2:%m/%d %H:%M}（差4分·廿九除夕）"
                vcol = "#b91c1c"
            elif is_30:
                verdict = f"初一 {dt2:%m/%d %H:%M}（跨8分·有年三十）"
                vcol = GREEN
            else:
                verdict = f"初一 {dt2:%m/%d %H:%M}（腊月29天·无三十）"
                vcol = BODY
            els.append(txt(500, ry + 15, verdict, 10.6, vcol, weight="700" if idx in (2, 5) else "600"))

        # Red midnight threshold line drawn on top of bars
        els.append(
            f'<line x1="{x_mid:.1f}" y1="226" x2="{x_mid:.1f}" y2="395" stroke="#dc2626" stroke-width="2" stroke-dasharray="5 3"/>'
        )
        els.append(txt(x_mid, 409, "24h 午夜线", 10.6, "#dc2626", "middle", weight="700"))

        # Legend on dedicated bottom row (zero collision with 0h..24h axis labels)
        els.append(f'<rect x="34" y="420" width="10" height="10" rx="2" fill="{BLUE}"/>')
        els.append(txt(48, 429, "t₀：腊月初一合朔时刻", 10.5, MUTED))
        els.append(f'<rect x="184" y="420" width="10" height="10" rx="2" fill="{ORANGE}"/>')
        els.append(txt(198, 429, "Δh：当月真实朔望月超出 29 天的小时数", 10.5, MUTED))
        els.append(f'<rect x="430" y="420" width="10" height="10" rx="2" fill="{GREEN}"/>')
        els.append(txt(444, 429, "绿色：t₀ + Δh ≥ 24h（保住大年三十）", 10.5, MUTED))

        return figure(
            452,
            "2025至2029连续五年无大年三十与2030年回归的定朔时刻计算图",
            "上图展示腊月初一合朔时刻t0加当月真实朔望月余时Δh与24小时午夜分界线的关系；下图实算2025至2029年总和均小于24小时（2027年23:56仅差4分钟），故连续五年除夕为腊月廿九，直至2030年00:08跨过午夜迎来大年三十。",
            els,
        )

    def _build_ecliptic_24_solarterms():
        """SVG 3: Computed 24 solar terms along elliptical orbit + step-duration wave."""
        terms_meta = [
            (0, "春分", True),
            (15, "清明", False),
            (30, "谷雨", True),
            (45, "立夏", False),
            (60, "小满", True),
            (75, "芒种", False),
            (90, "夏至", True),
            (105, "小暑", False),
            (120, "大暑", True),
            (135, "立秋", False),
            (150, "处暑", True),
            (165, "白露", False),
            (180, "秋分", True),
            (195, "寒露", False),
            (210, "霜降", True),
            (225, "立冬", False),
            (240, "小雪", True),
            (255, "大雪", False),
            (270, "冬至", True),
            (285, "小寒", False),
            (300, "大寒", True),
            (315, "立春", False),
            (330, "雨水", True),
            (345, "惊蛰", False),
        ]

        jd_base = 2460755.0  # 2025 Vernal Equinox
        jds = [_find_solar_term_jd(deg, jd_base + idx * 15.22) for idx, (deg, _, _) in enumerate(terms_meta)]
        jds.append(_find_solar_term_jd(0, jd_base + 365.2422))
        durations = [jds[i + 1] - jds[i] for i in range(24)]

        assert 14.70 < min(durations) < 14.75  # near perihelion (冬至-小寒-大寒)
        assert 15.70 < max(durations) < 15.76  # near aphelion (夏至-小暑-大暑)
        assert math.isclose(sum(durations), 365.242, abs_tol=0.02)

        els = header(
            "黄道二十四节气：藏在农历里的“纯太阳角度坐标”",
            "现代“定气法”按太阳视黄经每 15° 切一格；地球过近日点快、远日点慢，使相邻节气在 14.72–15.73 天间伸缩",
        )

        # Left panel: Elliptical ecliptic wheel with all 24 terms
        els.append(card(20, 62, 430, 368))
        els.append(txt(36, 85, "① 地球公转黄道圈：12 中气（●）与 12 节气（○）交错", PANEL_TITLE, INK, weight="700"))

        cx, cy = 235.0, 244.0
        rx, ry = 128.0, 118.0
        # Exaggerated visual focus shift toward perihelion (~283 deg, between 冬至 270° and 大寒 300°)
        peri_rad = math.radians(283.0)
        sun_x = cx + 26.0 * math.cos(peri_rad)
        sun_y = cy - 26.0 * math.sin(peri_rad)

        # Major/minor axes & apsides line
        ap_x1, ap_y1 = cx + rx * math.cos(peri_rad), cy - ry * math.sin(peri_rad)
        ap_x2, ap_y2 = cx - rx * math.cos(peri_rad), cy + ry * math.sin(peri_rad)
        els.append(
            f'<line x1="{ap_x2:.1f}" y1="{ap_y2:.1f}" x2="{ap_x1:.1f}" y2="{ap_y1:.1f}" '
            f'stroke="{ORANGE}" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.65"/>'
        )
        els.append(f'<line x1="{cx - rx}" y1="{cy}" x2="{cx + rx}" y2="{cy}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
        els.append(f'<line x1="{cx}" y1="{cy - ry}" x2="{cx}" y2="{cy + ry}" stroke="{SLATE_SOFT}" stroke-width="1"/>')

        # Orbit ellipse
        els.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{BLUE_LINE}" stroke-width="2"/>'
        )

        # Off-center Sun
        els.append(f'<circle cx="{sun_x:.1f}" cy="{sun_y:.1f}" r="14" fill="#fde047" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(txt(sun_x, sun_y + 4, "太阳", 10.5, INK, "middle", weight="700"))

        # Perihelion & Aphelion callouts inside orbit
        els.append(txt(cx - 24, cy - 68, "7月初远日点(最慢)", 10.5, GREEN, "middle", weight="700", halo=True))
        els.append(txt(cx - 24, cy - 53, "每15°需 15.73 天", 10.4, GREEN, "middle", halo=True))
        els.append(txt(cx + 12, cy + 78, "1月初近日点(最快)", 10.5, ORANGE, "middle", weight="700", halo=True))
        els.append(txt(cx + 12, cy + 93, "每15°仅 14.72 天", 10.4, ORANGE, "middle", halo=True))

        # 24 solar term points and labels
        for deg, name, is_zhongqi in terms_meta:
            rad = math.radians(deg)
            px = cx + rx * math.cos(rad)
            py = cy - ry * math.sin(rad)
            # Subtle ray from orbit inward
            ix = cx + (rx - 9) * math.cos(rad)
            iy = cy - (ry - 9) * math.sin(rad)
            els.append(f'<line x1="{ix:.1f}" y1="{iy:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="#94a3b8" stroke-width="1"/>')

            is_cardinal = deg in (0, 90, 180, 270)
            if is_zhongqi:
                dot_col = ORANGE if is_cardinal else BLUE
                r_dot = 5.0 if is_cardinal else 4.0
                els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_dot}" fill="{dot_col}"/>')
            else:
                els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="#ffffff" stroke="{SLATE}" stroke-width="1.4"/>')

            # Place label cleanly outside ellipse
            lx = cx + (rx + 26) * math.cos(rad)
            ly = cy - (ry + 22) * math.sin(rad) + 4.0
            lbl = f"{name}({deg}°)" if is_cardinal else name
            col = ORANGE if is_cardinal else (BLUE if is_zhongqi else BODY)
            wt = "700" if is_zhongqi else None
            els.append(txt(lx, ly, lbl, 10.6, col, "middle", weight=wt, halo=True))

        els.append(
            txt(
                235,
                416,
                "注：轨道扁率与太阳偏心放大示意（真实 e = 0.0167）；● 12 中气，○ 12 节气",
                10.5,
                MUTED,
                "middle",
            )
        )

        # Right panel: Computed interval curve + Pingqi vs Dingqi explanation
        els.append(card(462, 62, 278, 368))
        els.append(txt(478, 85, "② 相邻节气真实天数（2025 实算）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(478, 104, "平气均分 15.22 天 vs 定气按黄经 15° 实测：", 10.8, MUTED))

        gx, gy, gw, gh = 512.0, 234.0, 210.0, 104.0
        y_min, y_max = 14.5, 15.9
        for yv in (14.7, 15.2, 15.7):
            py = gy - ((yv - y_min) / (y_max - y_min)) * gh
            dash = ' stroke-dasharray="4 3"' if abs(yv - 15.2) < 0.05 else ""
            scol = ORANGE if abs(yv - 15.2) < 0.05 else SLATE_SOFT
            els.append(f'<line x1="{gx}" y1="{py:.1f}" x2="{gx + gw}" y2="{py:.1f}" stroke="{scol}" stroke-width="1.1"{dash}/>')
            els.append(txt(gx - 6, py + 4, f"{yv:.1f}d", 10.4, ORANGE if dash else MUTED, "end"))

        els.append(f'<path d="M{gx},{gy - gh:.1f} V{gy} H{gx + gw}" fill="none" stroke="#94a3b8" stroke-width="1.2"/>')
        for idx_t, t_lbl, anc in ((0, "春分", "start"), (6, "夏至", "middle"), (12, "秋分", "middle"), (18, "冬至", "middle"), (23, "惊蛰", "end")):
            tx = gx + (idx_t / 23.0) * gw
            els.append(txt(tx, gy + 16, t_lbl, 10.4, MUTED, anc))

        pts = []
        for i, d_val in enumerate(durations):
            px = gx + (i / 23.0) * gw
            py = gy - ((d_val - y_min) / (y_max - y_min)) * gh
            pts.append((px, py))
        d_str = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        els.append(f'<path d="{d_str}" fill="none" stroke="{BLUE}" stroke-width="2.3"/>')
        # Highlight peak (idx 6: 夏至->小暑) and trough (idx 18: 冬至->小寒)
        els.append(f'<circle cx="{pts[6][0]:.1f}" cy="{pts[6][1]:.1f}" r="4.2" fill="{GREEN}"/>')
        els.append(txt(pts[6][0] + 6, pts[6][1] - 5, "最长 15.73 天", 10.5, GREEN, "start", weight="700", halo=True))
        els.append(f'<circle cx="{pts[18][0]:.1f}" cy="{pts[18][1]:.1f}" r="4.2" fill="{ORANGE}"/>')
        els.append(txt(pts[18][0] - 6, pts[18][1] + 15, "最短 14.72 天", 10.5, ORANGE, "end", weight="700", halo=True))

        # Two concise insight cards below graph
        els.append(card(476, 264, 250, 72, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(488, 283, "为什么清明总在公历 4 月 4–5 日？", 11.2, BLUE, weight="700"))
        els.append(txt(488, 302, "节气本质是纯阳历角度（清明 = 15°），跟", 10.6, BODY))
        els.append(txt(488, 320, "公历回归年锁死；在农历里却会乱跳廿多天。", 10.6, BODY))

        els.append(card(476, 346, 250, 72, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(488, 365, "1645《时宪历》：平气法 → 定气法", 11.2, ORANGE, weight="700"))
        els.append(txt(488, 384, "古用平气（等时间 15.22 天）；改定气（等黄经", 10.6, BODY))
        els.append(txt(488, 402, "15°）后，直接造就了夏多闰月、冬罕闰月。", 10.6, BODY))

        return figure(
            444,
            "黄道二十四节气定气法15度划分与近日点远日点时间间隔实算图",
            "左图展示地球绕太阳椭圆轨道上每隔黄经15度划分二十四节气（12中气与12节气交错）；右图实算2025年各节气间隔从近日点14.72天到远日点15.73天的变化曲线及平气改定气的历法影响。",
            els,
        )

    def _build_eclipse_5deg_nodes():
        """SVG 4: 5.145° orbital tilt + eclipse nodes + total/annular + red lunar eclipse."""
        inc_deg = 5.145
        r_moon_mean_km = 384400.0
        max_z_km = r_moon_mean_km * math.sin(math.radians(inc_deg))
        earth_diam_km = 12742.0
        assert 34000.0 < max_z_km < 35000.0 and max_z_km > 2.5 * earth_diam_km

        # Apparent angular diameters (arcminutes): d_arcmin = 2 * asin(R / dist) * 60 * 180/pi
        r_moon_km = 1737.4
        ang_perigee = math.degrees(2 * math.asin(r_moon_km / 356400.0)) * 60.0
        ang_apogee = math.degrees(2 * math.asin(r_moon_km / 406700.0)) * 60.0
        assert 33.4 < ang_perigee < 33.6 and 29.3 < ang_apogee < 29.5

        els = header(
            "日月食的几何关卡：5.14° 黄白交角、伪本影金环与红月亮",
            "白道与黄道斜交使多数朔望错开影锥；月球椭圆距离变化决定日全食与日环食（尺度与倾角为教学示意）",
        )

        # Top panel: 5.14° inclination & 2 eclipse seasons
        els.append(card(20, 62, 720, 178))
        els.append(txt(36, 85, "① 为什么不是每月初一日食、每月十五月食？—— 5.14° 黄白交角与“食季”", PANEL_TITLE, INK, weight="700"))

        scx, scy = 380.0, 158.0
        erx, ery = 148.0, 42.0
        # Ecliptic orbit ellipse
        els.append(
            f'<ellipse cx="{scx}" cy="{scy}" rx="{erx}" ry="{ery}" fill="#f8fafc" stroke="{BLUE_LINE}" stroke-width="1.6"/>'
        )
        # Line of nodes across left-right stations (through Sun)
        els.append(
            f'<line x1="{scx - 190}" y1="{scy}" x2="{scx + 190}" y2="{scy}" stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="6 4"/>'
        )
        els.append(f'<circle cx="{scx}" cy="{scy}" r="15" fill="#fde047" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(txt(scx, scy + 4, "太阳", 10.5, INK, "middle", weight="700"))
        els.append(txt(scx, scy + 29, "黄道面（地球公转平面）", 10.3, BLUE, "middle", weight="600", halo=True))

        # Helper to draw tilted lunar orbit with constant orientation in space!
        def _lunar_ring(ex, ey, hit_node=False):
            col = GREEN if hit_node else ORANGE
            els.append(
                f'<g transform="translate({ex:.1f},{ey:.1f}) rotate(-18)">'
                f'<ellipse cx="0" cy="0" rx="30" ry="10" fill="none" stroke="{col}" stroke-width="1.6"/>'
                f"</g>"
            )
            els.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="6" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')

        # Left & Right stations: Eclipse seasons (Sun aligned with node line!)
        _lunar_ring(scx - erx, scy, hit_node=True)
        els.append(f'<circle cx="{scx - erx + 28.5:.1f}" cy="{scy:.1f}" r="3.6" fill="{GREEN}"/>')
        els.append(f'<circle cx="{scx - erx - 28.5:.1f}" cy="{scy:.1f}" r="3.6" fill="{GREEN}"/>')
        els.append(txt(36, 132, "食季①（过交点）", 11.0, GREEN, "start", weight="700"))
        els.append(txt(36, 150, "朔望恰落黄白交点", 10.5, BODY, "start"))
        els.append(txt(36, 168, "→ 初一日食 / 十五月食", 10.5, GREEN, "start", weight="700"))

        _lunar_ring(scx + erx, scy, hit_node=True)
        els.append(f'<circle cx="{scx + erx - 28.5:.1f}" cy="{scy:.1f}" r="3.6" fill="{GREEN}"/>')
        els.append(f'<circle cx="{scx + erx + 28.5:.1f}" cy="{scy:.1f}" r="3.6" fill="{GREEN}"/>')
        els.append(txt(724, 132, "食季②（约半年后）", 11.0, GREEN, "end", weight="700"))
        els.append(txt(724, 150, "交点线再次对准太阳", 10.5, BODY, "end"))
        els.append(txt(724, 168, "→ 每年约 2 个食季", 10.5, GREEN, "end", weight="700"))

        # Top & Bottom stations: Non-eclipse months (Moon passes ~34,500 km above/below shadow)
        _lunar_ring(scx, scy - ery, hit_node=False)
        els.append(f'<circle cx="{scx:.1f}" cy="{scy - ery + 9.5:.1f}" r="3.5" fill="{ORANGE}"/>')
        els.append(txt(scx + 38, scy - ery - 3, "非食季：偏离黄道 ±5.14°（约3.4万km），影锥擦过", 10.5, ORANGE, "start", weight="600", halo=True))

        _lunar_ring(scx, scy + ery, hit_node=False)
        els.append(f'<circle cx="{scx:.1f}" cy="{scy + ery - 9.5:.1f}" r="3.5" fill="{ORANGE}"/>')
        els.append(txt(36, 226, "注：交点线受太阳摄动每年西退约 19.3°，故两食季间隔约 173.3 天（比半年略短）", 10.5, MUTED))

        # Bottom-Left panel: Total vs Annular Solar Eclipse
        els.append(card(20, 252, 354, 192))
        els.append(txt(36, 275, "② 日全食 vs 日环食：月球远近改写影锥", PANEL_TITLE, INK, weight="700"))

        # Subcase A: Perigee Total Eclipse (y=318)
        y_tot = 318.0
        els.append(f'<circle cx="52" cy="{y_tot}" r="14" fill="#fde047" stroke="{ORANGE}" stroke-width="1.3"/>')
        # Penumbra & Umbra reaching Earth (x=206)
        els.append(f'<polygon points="132,{y_tot - 7} 206,{y_tot - 17} 206,{y_tot + 17} 132,{y_tot + 7}" fill="#e2e8f0" opacity="0.7"/>')
        els.append(f'<polygon points="132,{y_tot - 6} 206,{y_tot - 1.5} 206,{y_tot + 1.5} 132,{y_tot + 6}" fill="#1e293b"/>')
        els.append(f'<circle cx="132" cy="{y_tot}" r="6.2" fill="#475569"/>')
        els.append(f'<circle cx="212" cy="{y_tot}" r="11" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
        els.append(txt(234, y_tot - 6, "近地点（≈35.6万km，33.5′）", 10.6, BLUE, weight="700"))
        els.append(txt(234, y_tot + 11, "本影锥触地 → 日全食(见日冕)", 10.5, BODY))

        # Subcase B: Apogee Annular Eclipse (y=386)
        y_ann = 386.0
        els.append(f'<circle cx="52" cy="{y_ann}" r="14" fill="#fde047" stroke="{ORANGE}" stroke-width="1.3"/>')
        # Umbra ends early at x=178; Antumbra expands to Earth at x=212
        els.append(f'<polygon points="118,{y_ann - 6} 212,{y_ann - 18} 212,{y_ann + 18} 118,{y_ann + 6}" fill="#e2e8f0" opacity="0.7"/>')
        els.append(f'<polygon points="118,{y_ann - 5.5} 178,{y_ann} 118,{y_ann + 5.5}" fill="#1e293b"/>')
        els.append(f'<polygon points="178,{y_ann} 212,{y_ann - 4.5} 212,{y_ann + 4.5}" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="0.9"/>')
        els.append(f'<circle cx="118" cy="{y_ann}" r="5.6" fill="#475569"/>')
        els.append(f'<circle cx="218" cy="{y_ann}" r="11" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
        els.append(txt(234, y_ann - 6, "远地点（≈40.7万km，29.4′）", 10.6, ORANGE, weight="700"))
        els.append(txt(234, y_ann + 11, "伪本影触地 → 日环食(金环)", 10.5, BODY))
        els.append(txt(36, 430, "太阳视直径约 31.6′–32.7′，恰卡在月球最大与最小视直径之间！", 10.4, MUTED))

        # Bottom-Right panel: Total Lunar Eclipse & Red Moon refraction
        els.append(card(386, 252, 354, 192))
        els.append(txt(402, 275, "③ 月全食“红月亮”：地球大气层的散射折射", PANEL_TITLE, INK, weight="700"))

        ly = 348.0
        # Sun on left
        els.append(f'<circle cx="420" cy="{ly}" r="16" fill="#fde047" stroke="{ORANGE}" stroke-width="1.4"/>')
        els.append(txt(420, ly + 4, "太阳", 10.4, INK, "middle", weight="700"))

        # Earth's penumbra & umbra cones
        els.append(f'<polygon points="520,{ly - 17} 716,{ly - 34} 716,{ly + 34} 520,{ly + 17}" fill="#f1f5f9"/>')
        els.append(f'<polygon points="520,{ly - 16} 716,{ly - 9} 716,{ly + 9} 520,{ly + 16}" fill="#fce7e2" opacity="0.85"/>')

        # Refracted red rays bending through Earth's atmosphere to the Moon at x=668
        els.append(
            f'<path d="M436,{ly - 12} L520,{ly - 19} L668,{ly - 3}" fill="none" stroke="#dc2626" stroke-width="1.6"/>'
        )
        els.append(
            f'<path d="M436,{ly + 12} L520,{ly + 19} L668,{ly + 3}" fill="none" stroke="#dc2626" stroke-width="1.6"/>'
        )
        # Scattered short blue rays at Earth's limb
        els.append(
            f'<path d="M520,{ly - 19} L542,{ly - 36}" fill="none" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="3 2"/>'
        )
        els.append(
            f'<path d="M520,{ly + 19} L542,{ly + 36}" fill="none" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="3 2"/>'
        )

        # Earth + atmosphere ring
        els.append(f'<circle cx="520" cy="{ly}" r="20" fill="none" stroke="#93c5fd" stroke-width="3.5"/>')
        els.append(f'<circle cx="520" cy="{ly}" r="16" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
        els.append(txt(520, ly + 4, "地球", 10.4, BLUE, "middle", weight="700"))

        # Copper-red Moon inside Earth's umbra
        els.append(f'<circle cx="668" cy="{ly}" r="9.5" fill="#b93829" stroke="#7f1d1d" stroke-width="1.4"/>')
        els.append(txt(668, ly - 15, "本影内红月亮", 10.6, "#991b1b", "middle", weight="700", halo=True))

        els.append(txt(552, ly - 32, "蓝紫短波被大气散射滤除", 10.4, BLUE, "start", weight="600", halo=True))
        els.append(txt(402, 408, "• 地球本影比月球宽得多，背日夜半球整片可见月食（持续数小时）", 10.4, BODY))
        els.append(txt(402, 428, "• 红橙长波经地球大气折射入本影，故全食月亮呈暗铜红色而非全黑", 10.4, "#991b1b", weight="600"))

        return figure(
            458,
            "黄白交角5.14度食季原理与日全食日环食及月全食红月亮几何成因图",
            "上图展示白道面相对黄道面倾斜5.14度，仅在半年一次的黄白交点食季才发生交食；左下对比月球近地点日全食与远地点伪本影日环食；右下展示地球大气散射蓝光并折射红光形成暗红月全食。",
            els,
        )

    def _build_saros_resonance_lock():
        """SVG 5: Saros 223 synodic ≈ 242 draconic ≈ 239 anomalistic + 120° shift."""
        t_syn = 29.530589
        t_dra = 27.212221
        t_ano = 27.554550

        d_syn = 223 * t_syn
        d_dra = 242 * t_dra
        d_ano = 239 * t_ano

        diff_dra_min = (d_dra - d_syn) * 1440.0
        diff_ano_hr = (d_ano - d_syn) * 24.0
        west_shift_deg = (d_syn - int(d_syn)) * 360.0

        assert math.isclose(d_syn, 6585.3213, abs_tol=0.002)
        assert 50.0 < diff_dra_min < 54.0
        assert 5.1 < diff_ano_hr < 5.3
        assert 115.0 < west_shift_deg < 117.0  # ~116° (~120° westward shift)

        els = header(
            "沙罗周期（Saros）：三种“月”在 6585.32 天上的三重共振奇迹",
            "223 朔望月 ≈ 242 交点月 ≈ 239 近点月 ≈ 18 年 11 天 8 小时；多出的约 8 小时使日食带每次西移约 120°",
        )

        # Top panel: Three rulers locking onto 6585.32 days
        els.append(card(20, 62, 720, 178))
        els.append(txt(36, 85, "① 决定交食的三把天文周期尺，在 18 年 11 天 8 小时处几乎严丝合缝！", PANEL_TITLE, INK, weight="700"))

        tracks = [
            (
                "223 个朔望月",
                "29.53059d × 223",
                f"{d_syn:.3f} 天",
                "基准 0 分（锁死朔/望）",
                0.0,
                BLUE,
                BLUE_SOFT,
                22,
            ),
            (
                "242 个交点月",
                "27.21222d × 242",
                f"{d_dra:.3f} 天",
                f"+{diff_dra_min:.0f} 分钟（锁死食季交点）",
                d_dra - d_syn,
                GREEN,
                GREEN_SOFT,
                24,
            ),
            (
                "239 个近点月",
                "27.55455d × 239",
                f"{d_ano:.3f} 天",
                f"+{diff_ano_hr:.1f} 小时（锁死地月远近）",
                d_ano - d_syn,
                ORANGE,
                ORANGE_SOFT,
                24,
            ),
        ]

        rx0 = 246.0
        lock_x = 446.0
        for idx, (t_name, t_mul, t_tot, t_note, rem_d, fg, bg, n_ticks) in enumerate(tracks):
            ry = 100 + idx * 44
            els.append(pill(36, ry + 4, t_name, fg=fg, bg=bg, w=102, h=22, size=10.8))
            els.append(txt(144, ry + 19, t_mul, 10.4, MUTED))

            # Ruler bar from rx0 to lock_x + magnified residual (1 day = 65px for residual zoom)
            end_x = lock_x + rem_d * 65.0
            els.append(
                f'<rect x="{rx0}" y="{ry + 7}" width="{end_x - rx0:.1f}" height="16" rx="3" fill="{bg}" stroke="{fg}" stroke-width="1.3"/>'
            )
            for ti in range(1, n_ticks):
                tx = rx0 + (ti / n_ticks) * (lock_x - rx0)
                els.append(f'<line x1="{tx:.1f}" y1="{ry + 7}" x2="{tx:.1f}" y2="{ry + 14}" stroke="{fg}" stroke-width="0.9" opacity="0.55"/>')

            els.append(txt(end_x + 8, ry + 19, f"= {t_tot}｜{t_note}", 10.6, fg if idx > 0 else INK, weight="700"))

        # Vertical resonance lock line
        els.append(
            f'<line x1="{lock_x}" y1="94" x2="{lock_x}" y2="222" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5 3"/>'
        )
        els.append(txt(lock_x, 234, f"共振锁死线 {d_syn:.3f} 天（右侧残差放大显示）", 10.4, "#dc2626", "middle", weight="700"))

        # Bottom-Left panel: +0.322 day (~8h) -> 120° westward shift & 3-Saros Exeligmos
        els.append(card(20, 252, 368, 174))
        els.append(txt(36, 275, "② 尾数 0.322 天（≈8 小时）：日食带西移 120°", PANEL_TITLE, INK, weight="700"))

        ecx, ecy, er = 96.0, 354.0, 42.0
        els.append(f'<circle cx="{ecx}" cy="{ecy}" r="{er}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
        els.append(f'<circle cx="{ecx}" cy="{ecy}" r="3" fill="{INK}"/>')
        els.append(txt(ecx, ecy + 15, "北极俯视", 10.2, MUTED, "middle"))

        pts_3 = [
            (90, "第0轮", BLUE),
            (210, "第1轮(-120°)", ORANGE),
            (330, "第2轮(-240°)", PURPLE),
        ]
        for ang, lbl, col in pts_3:
            rad = math.radians(ang)
            px = ecx + er * math.cos(rad)
            py = ecy - er * math.sin(rad)
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{col}"/>')

        els.append(txt(ecx, ecy - er - 9, "第0轮 / 第3轮回归", 10.3, BLUE, "middle", weight="700"))
        els.append(txt(ecx - 38, ecy + er + 14, "+1沙罗", 10.3, ORANGE, "middle", weight="700"))
        els.append(txt(ecx + 38, ecy + er + 14, "+2沙罗", 10.3, PURPLE, "middle", weight="700"))

        els.append(txt(168, 306, "• 地球多自转约 7 小时 43 分（≈116°–120°）", 10.6, BODY))
        els.append(txt(168, 327, "• 下一次同族日食落向西边约 1/3 个地球", 10.6, BODY))
        els.append(txt(168, 348, "• 满 3 轮沙罗（54 年 33–34 天，“转轮周期”）", 10.6, GREEN, weight="700"))
        els.append(txt(168, 368, "  累计多转满一整圈，日食才回到同一经度区！", 10.6, GREEN, weight="600"))
        els.append(txt(168, 394, "• 月食因夜半球皆可见，单轮沙罗更易异地同观", 10.4, MUTED))

        # Bottom-Right panel: Finite Saros lifetime & Chinese Santong Calendar 135-month cycle
        els.append(card(400, 252, 340, 174))
        els.append(txt(416, 275, "③ 沙罗家族的寿命与中西古历“食周”", PANEL_TITLE, INK, weight="700"))

        els.append(card(414, 292, 312, 56, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(426, 311, "为什么一族沙罗不会永远循环下去？", 11.0, PURPLE, weight="700"))
        els.append(txt(426, 330, "52 分钟残差使交点每次微移约 0.5°（影轴南北移 ~300km），", 10.4, BODY))
        els.append(txt(426, 344, "每族历经 1226–1550 年（约 70–85 次食）后从两极谢幕。", 10.4, BODY))

        els.append(card(414, 358, 312, 56, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(426, 377, "中国古历独立推算的共振：135 月“食周”与交点月", 11.0, GREEN, weight="700"))
        els.append(txt(426, 396, "西汉《三统历》定 135 朔望月 = 23 食季（146.5 交点月）；", 10.4, BODY))
        els.append(txt(426, 410, "462 年祖冲之《大明历》测交点月 27.21223 天，仅差 0.9 秒！", 10.4, BODY))

        return figure(
            440,
            "沙罗周期223朔望月242交点月239近点月三重共振与120度西移机制图",
            "上图对比223个朔望月6585.322天、242个交点月6585.357天与239个近点月6585.538天的精密咬合；左下解释0.322天尾数导致日食带每次西移约120度、3轮54年回归原地；右下说明沙罗序列有限寿命与中国古历食周及大明历交点月精度。",
            els,
        )

    @register("calendar-astronomy", "农历公历置闰筛法、连续无大年三十、黄道二十四节气、黄白交角交食与沙罗共振", "mechanics_sky")
    def build_calendar_astronomy():
        write_svg(SUBDIR, "gregorian-leap-sieve.svg", _build_gregorian_leap_sieve())
        write_svg(SUBDIR, "continuous-no-30-chuxi.svg", _build_continuous_no_30_chuxi())
        write_svg(SUBDIR, "ecliptic-24-solarterms.svg", _build_ecliptic_24_solarterms())
        write_svg(SUBDIR, "eclipse-5deg-nodes.svg", _build_eclipse_5deg_nodes())
        write_svg(SUBDIR, "saros-resonance-lock.svg", _build_saros_resonance_lock())


_register_calendar_astronomy()


# ---------------------------------------------------------------------------
# Geosynchronous & Geostationary Satellites (geosync-orbit)
# ---------------------------------------------------------------------------
def _register_geosync_orbit():
    SUBDIR = "geosync-orbit"

    # WGS84 / IERS exact constants
    MU_E = 398600.4418  # km^3 / s^2
    R_E = 6378.137  # km (equatorial radius)
    T_SID = 86164.0905  # s (23h 56m 4.09s)
    T_SOL = 86400.0  # s (24h 00m 00s)
    OMEGA_E = 2.0 * math.pi / T_SID  # rad / s

    R_GEO = (MU_E * (T_SID ** 2) / (4.0 * math.pi ** 2)) ** (1.0 / 3.0)
    H_GEO = R_GEO - R_E
    V_GEO = OMEGA_E * R_GEO
    G_GEO = (MU_E * 1e9) / ((R_GEO * 1e3) ** 2)

    # Assertions verifying textbook & agency numbers
    assert abs(R_GEO - 42164.17) < 0.05, f"Unexpected R_GEO={R_GEO}"
    assert abs(H_GEO - 35786.03) < 0.05, f"Unexpected H_GEO={H_GEO}"
    assert abs(V_GEO - 3.07466) < 0.001, f"Unexpected V_GEO={V_GEO}"
    assert abs(G_GEO - 0.2242) < 0.002, f"Unexpected G_GEO={G_GEO}"

    # 1. Angular Chase & Kepler Third-Law Sweet Spot (Animated + Static)
    def _build_angular_chase_sweetspot():
        # 6 sidereal hours slice: Earth & GEO sweep exact 90 deg CCW
        r_leo = R_E + 400.0
        r_meo = R_E + 21528.0
        dtheta_geo = 90.0
        dtheta_meo = dtheta_geo * ((R_GEO / r_meo) ** 1.5)  # 167.26 deg
        dtheta_leo = dtheta_geo * ((R_GEO / r_leo) ** 1.5)  # 1395.97 deg
        assert abs(dtheta_meo - 167.26) < 0.2
        assert abs(dtheta_leo - 1395.97) < 1.0

        cx, cy = 192.0, 248.0
        scale = 104.0 / R_GEO  # 104 px = 42,164 km (exact true scale!)
        px_re = R_E * scale  # 15.73 px
        px_leo = r_leo * scale
        px_meo = r_meo * scale  # 68.83 px
        px_geo = R_GEO * scale  # 104.00 px

        anim_css = f"""
      .rot-earth {{
        transform-origin: {cx:.1f}px {cy:.1f}px;
        animation: spinEarth 6.4s linear 0.35s 1 forwards;
      }}
      .rot-geo {{
        transform-origin: {cx:.1f}px {cy:.1f}px;
        animation: spinGeo 6.4s linear 0.35s 1 forwards;
      }}
      .rot-meo {{
        transform-origin: {cx:.1f}px {cy:.1f}px;
        animation: spinMeo 6.4s linear 0.35s 1 forwards;
      }}
      .rot-leo {{
        transform-origin: {cx:.1f}px {cy:.1f}px;
        animation: spinLeo 6.4s linear 0.35s 1 forwards;
      }}
      @keyframes spinEarth {{
        from {{ transform: rotate({dtheta_geo:.2f}deg); }}
        to   {{ transform: rotate(0deg); }}
      }}
      @keyframes spinGeo {{
        from {{ transform: rotate({dtheta_geo:.2f}deg); }}
        to   {{ transform: rotate(0deg); }}
      }}
      @keyframes spinMeo {{
        from {{ transform: rotate({dtheta_meo:.2f}deg); }}
        to   {{ transform: rotate(0deg); }}
      }}
      @keyframes spinLeo {{
        from {{ transform: rotate({dtheta_leo:.2f}deg); }}
        to   {{ transform: rotate(0deg); }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .rot-earth, .rot-geo, .rot-meo, .rot-leo {{
          animation: none;
          transform: rotate(0deg);
        }}
      }}"""

        els = header(
            "角速度追逐战：为什么只有 35,786 km 能跟地球“同频锁死”？",
            "左：北极俯视 6 恒星时真实角速度比（ω ∝ r⁻³ᐟ²）；右：开普勒第三定律唯一交点",
        )

        # Left Card
        els.append(card(20, 62, 352, 360))
        els.append(txt(36, 84, "① 北极俯视真比例：6 恒星时追逐", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "t=0 从正右方出发 → t=6h 地球与 GEO 同转 90°", 11.0, MUTED))

        # Orbit circles
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{px_geo:.1f}" fill="none" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="6 4"/>')
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{px_meo:.1f}" fill="none" stroke="{PURPLE}" stroke-width="1.4" stroke-dasharray="4 4"/>')
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="24.0" fill="none" stroke="{ORANGE}" stroke-width="1.2" stroke-dasharray="2.5 2.5"/>')

        # Static t=0 start reference line (East, +x)
        els.append(
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + px_geo + 10:.1f}" y2="{cy:.1f}" '
            f'stroke="{HAIRLINE}" stroke-width="1.3" stroke-dasharray="3 3"/>'
        )
        els.append(f'<circle cx="{cx + px_geo:.1f}" cy="{cy:.1f}" r="4.5" fill="#ffffff" stroke="{GREEN}" stroke-width="1.5" stroke-dasharray="2 2"/>')
        els.append(txt(cx + px_geo - 4, cy + 16, "t=0 起点", 10.5, MUTED, "end"))

        # Swept 90 deg sector highlight for GEO = Earth lock (from East 0 deg CCW to North 90 deg)
        els.append(
            f'<path d="M {cx:.1f},{cy:.1f} L {cx + px_geo:.1f},{cy:.1f} '
            f'A {px_geo:.1f},{px_geo:.1f} 0 0 0 {cx:.1f},{cy - px_geo:.1f} Z" '
            f'fill="{GREEN}" fill-opacity="0.06"/>'
        )

        # Earth disk
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{px_re:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="{INK}"/>')

        # Animated radial sightline + GEO satellite (final at North: cx, cy - px_geo)
        els.append('<g class="rot-geo">')
        els.append(
            f'<line x1="{cx:.1f}" y1="{cy - px_re:.1f}" x2="{cx:.1f}" y2="{cy - px_geo + 6:.1f}" '
            f'stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="4 3"/>'
        )
        els.append(f'<circle cx="{cx:.1f}" cy="{cy - px_geo:.1f}" r="6.2" fill="{GREEN}" stroke="#ffffff" stroke-width="1.6"/>')
        els.append('</g>')

        # Animated rooftop dish on Earth equator (final at North: cx, cy - px_re)
        els.append('<g class="rot-earth">')
        els.append(f'<circle cx="{cx:.1f}" cy="{cy - px_re:.1f}" r="3.6" fill="{INK}"/>')
        els.append('</g>')

        # Animated MEO satellite (final at dtheta_meo = 167.26 deg CCW from East)
        ang_meo = math.radians(dtheta_meo)
        mx = cx + px_meo * math.cos(ang_meo)
        my = cy - px_meo * math.sin(ang_meo)
        els.append('<g class="rot-meo">')
        els.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="5.0" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append('</g>')

        # Animated LEO satellite (final at dtheta_leo = 1395.97 deg -> 315.97 deg CCW from East)
        ang_leo = math.radians(dtheta_leo)
        lx = cx + 24.0 * math.cos(ang_leo)
        ly = cy - 24.0 * math.sin(ang_leo)
        els.append('<g class="rot-leo">')
        els.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4.2" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append('</g>')

        # Clean static callouts for final t=6h positions
        els.append(pill(cx - 94, cy - px_geo - 26, "GEO 35,786 km（同转 90° 锁死！）", fg=GREEN, bg=GREEN_SOFT, w=198, h=20, size=10.6))
        els.append(txt(cx - px_meo - 2, cy - 26, "北斗 MEO", 10.5, PURPLE, "end", weight="700"))
        els.append(txt(cx - px_meo - 2, cy - 12, "已超前 167°", 10.1, PURPLE, "end"))
        els.append(txt(cx + 28, cy + 28, "空间站 LEO（400 km）", 10.4, ORANGE, weight="700"))
        els.append(txt(cx + 28, cy + 42, "6h 狂飙 3.88 圈！", 10.1, ORANGE))

        # Moon off-scale arrow note at bottom of Left Card
        els.append(card(34, 364, 324, 46, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(46, 382, "再往外？月球 r ≈ 384,400 km（GEO 的 9.1 倍）：", 10.6, INK, weight="600"))
        els.append(txt(46, 399, "6 小时仅慢吞吞挪动 3.3°，反过来被地球自转远远甩在身后。", 10.4, MUTED))

        # Right Card: Exact Kepler Third Law Curve T(h) vs Altitude h
        els.append(card(388, 62, 352, 360))
        els.append(txt(404, 84, "② 周期随高度抬升：唯一的同步交点", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "T = 2π √[(R_E + h)³ / GM_⊕] ，高度决定唯一周期", 11.0, MUTED))

        gx0, gy0 = 438.0, 326.0  # plot origin (h=0, T=0)
        gw, gh = 278.0, 196.0  # h_max = 45,000 km, T_max = 32 h
        h_max, t_max = 45000.0, 32.0

        def map_ht(h_km, t_hr):
            return gx0 + (h_km / h_max) * gw, gy0 - (t_hr / t_max) * gh

        # Gridlines
        for t_tick in (0, 8, 16, 24, 32):
            _, py = map_ht(0, t_tick)
            els.append(f'<line x1="{gx0:.1f}" y1="{py:.1f}" x2="{gx0 + gw:.1f}" y2="{py:.1f}" stroke="{BORDER}" stroke-width="1"/>')
            els.append(txt(gx0 - 7, py + 4, f"{t_tick}h", 10.2, MUTED, "end"))

        for h_tick, lbl in ((0, "0"), (15000, "1.5万"), (30000, "3万"), (45000, "4.5万km")):
            px, _ = map_ht(h_tick, 0)
            els.append(f'<line x1="{px:.1f}" y1="{gy0 - gh:.1f}" x2="{px:.1f}" y2="{gy0:.1f}" stroke="{BORDER}" stroke-width="1"/>')
            els.append(txt(px, gy0 + 16, lbl, 10.2, MUTED, "middle"))

        # Axes
        els.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0 + gw:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.4"/>')
        els.append(f'<line x1="{gx0:.1f}" y1="{gy0 - gh:.1f}" x2="{gx0:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.4"/>')

        # Horizontal Sidereal Day target line
        t_sid_hr = T_SID / 3600.0
        px_geo_plot, py_geo_plot = map_ht(H_GEO, t_sid_hr)
        els.append(
            f'<line x1="{gx0:.1f}" y1="{py_geo_plot:.1f}" x2="{gx0 + gw:.1f}" y2="{py_geo_plot:.1f}" '
            f'stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="5 3"/>'
        )
        els.append(
            f'<line x1="{px_geo_plot:.1f}" y1="{py_geo_plot:.1f}" x2="{px_geo_plot:.1f}" y2="{gy0:.1f}" '
            f'stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="4 3"/>'
        )
        els.append(txt(gx0 + 6, py_geo_plot - 6, "地球恒星日 23h 56m 04s", 10.4, GREEN, weight="700"))

        # Exact Kepler curve points
        pts = []
        for i in range(91):
            hk = (h_max * i) / 90.0
            rk = R_E + hk
            tk = (2.0 * math.pi * math.sqrt((rk ** 3) / MU_E)) / 3600.0
            pts.append(map_ht(hk, tk))
        path_d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        els.append(f'<path d="{path_d}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')

        # 3 Landmark dots: ISS, MEO, GEO
        t_leo_hr = (2.0 * math.pi * math.sqrt((r_leo ** 3) / MU_E)) / 3600.0
        t_meo_hr = (2.0 * math.pi * math.sqrt((r_meo ** 3) / MU_E)) / 3600.0
        px_l, py_l = map_ht(400.0, t_leo_hr)
        px_m, py_m = map_ht(21528.0, t_meo_hr)

        els.append(f'<circle cx="{px_l:.1f}" cy="{py_l:.1f}" r="4.8" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.3"/>')
        els.append(txt(px_l + 8, py_l - 3, "空间站 400km (1.54h, 7.67km/s)", 10.2, ORANGE, weight="600"))

        els.append(f'<circle cx="{px_m:.1f}" cy="{py_m:.1f}" r="5.0" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.3"/>')
        els.append(txt(px_m - 6, py_m - 10, "北斗 MEO (12.9h, 3.78km/s)", 10.2, PURPLE, "middle", weight="600"))

        els.append(f'<circle cx="{px_geo_plot:.1f}" cy="{py_geo_plot:.1f}" r="6.2" fill="{GREEN}" stroke="#ffffff" stroke-width="1.6"/>')
        els.append(txt(px_geo_plot - 8, py_geo_plot + 18, "35,786 km", 10.8, GREEN, "end", weight="700"))
        els.append(txt(px_geo_plot - 8, py_geo_plot + 32, "v = 3.075 km/s", 10.2, GREEN, "end"))

        # Bottom summary box on Right Card
        els.append(card(402, 354, 324, 56, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(414, 373, "黄金等式：GM_⊕ / r² = ω_⊕² r  ⇒  r = 42,164.17 km", 10.8, GREEN, weight="700"))
        els.append(txt(414, 391, "低一分则超前向东跑，高一分则落后向西漂，", 10.3, BODY))
        els.append(txt(414, 404, "与卫星质量无关——39 kg 轻星与 8 吨重星同轨同速！", 10.3, BODY))

        return figure(
            436,
            "地球同步轨道角速度追逐与开普勒第三定律唯一甜蜜点图解",
            "左图按真实比例展示地球、400公里空间站、21528公里北斗中圆轨道与35786公里地球静止轨道在6恒星时内的角速度追逐动画与终态；右图绘制轨道周期随高度变化曲线，标出23小时56分04秒对应的唯一同步高度35786公里。",
            els,
            extra_css=anim_css,
        )

    # 2. Sidereal Day vs Solar Day & The 77 km Error
    def _build_sidereal_vs_solar_day():
        r_wrong = (MU_E * (T_SOL ** 2) / (4.0 * math.pi ** 2)) ** (1.0 / 3.0)
        dh_wrong = r_wrong - R_GEO  # +76.93 km
        drift_deg_day = 360.0 * (T_SOL - T_SID) / T_SOL  # ~0.983 deg/day
        assert abs(dh_wrong - 76.93) < 0.15

        els = header(
            "为什么同步周期是 23 小时 56 分 04 秒，而不是整整 24 小时？",
            "地球一边自转一边绕太阳公转：对齐遥远恒星（惯性空间）比重新正对太阳每天少 3 分 56 秒",
        )

        # Left Panel: Sun + Orbiting Earth (exaggerated orbital step clearly noted)
        els.append(card(20, 62, 366, 344))
        els.append(txt(36, 84, "① 恒星日 vs 太阳日（公转角放大示意）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "真实地球每天公转 Δφ = 360° ÷ 365.256 ≈ 0.986°", 10.8, MUTED))

        # Sun on left
        sx, sy = 76.0, 236.0
        els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="26" fill="#fef3c7" stroke="{ORANGE}" stroke-width="2"/>')
        els.append(txt(sx, sy + 4, "太阳", 12.0, ORANGE, "middle", weight="700"))

        # Distant star reference rays (horizontal to the left: pointing to -x)
        els.append(txt(206, 126, "← 遥远恒星方向（惯性空间平行基准线）", 10.4, BLUE, "middle", weight="600"))

        # Orbit arc of Earth around Sun
        els.append(f'<path d="M 278,284 A 212,212 0 0 0 264,162" fill="none" stroke="{HAIRLINE}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#arr-muted)"/>')
        els.append(txt(314, 232, "地球公转", 10.5, MUTED))
        els.append(txt(314, 246, "+0.986°/天", 10.5, MUTED, weight="600"))

        # Day 0 Earth (bottom right: 278, 276)
        e1x, e1y = 266.0, 278.0
        els.append(f'<line x1="{sx + 26:.1f}" y1="{sy + 6:.1f}" x2="{e1x:.1f}" y2="{e1y:.1f}" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(f'<circle cx="{e1x:.1f}" cy="{e1y:.1f}" r="20" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.7"/>')
        # Arrow on Day 0 pointing toward Sun (left-up slightly; simplify Day 0 at y=278, put Sun at y=278? Even cleaner!)
        # Wait: let's check geometry! If Day 0 is at (266, 278) and Sun is at (76, 278), then at Day 0 BOTH Sun and distant star in -x direction align!
        # Let's refine coordinates right here before appending:
        els.clear()
        els.extend(
            header(
                "为什么同步周期是 23 小时 56 分 04 秒，而不是整整 24 小时？",
                "地球一边自转一边绕太阳公转：对齐遥远恒星（惯性空间）比重新正对太阳每天少 3 分 56 秒",
            )
        )
        els.append(card(20, 62, 366, 344))
        els.append(txt(36, 84, "① 恒星日 vs 太阳日（公转角放大示意）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "真实地球每天公转 0.986°，图中放大为 24° 以便看清夹角", 10.6, MUTED))

        sx, sy = 76.0, 286.0
        e0x, e0y = 268.0, 286.0
        orb_r = e0x - sx  # 192 px
        ang_exag = math.radians(26.0)
        e1x = sx + orb_r * math.cos(ang_exag)  # 248.6
        e1y = sy - orb_r * math.sin(ang_exag)  # 201.8

        # Orbit arc from Day 0 to Day 1
        els.append(
            f'<path d="M {e0x:.1f},{e0y:.1f} A {orb_r:.1f},{orb_r:.1f} 0 0 0 {e1x:.1f},{e1y:.1f}" '
            f'fill="none" stroke="{SLATE}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#arr-muted)"/>'
        )
        els.append(txt(296, 246, "公转 1 天", 10.4, SLATE, weight="600"))
        els.append(txt(296, 260, "(+0.986°)", 10.1, MUTED))

        # Sun at (sx, sy)
        els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="24" fill="#fef3c7" stroke="{ORANGE}" stroke-width="2"/>')
        els.append(txt(sx, sy + 4, "太阳", 12.0, ORANGE, "middle", weight="700"))

        # Day 0: horizontal line pointing straight left to BOTH Sun & distant star
        els.append(f'<line x1="{sx + 25:.1f}" y1="{e0y:.1f}" x2="{e0x - 22:.1f}" y2="{e0y:.1f}" stroke="{ORANGE}" stroke-width="1.5" marker-start="url(#arr-orange)"/>')
        els.append(f'<circle cx="{e0x:.1f}" cy="{e0y:.1f}" r="20" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.7"/>')
        els.append(f'<circle cx="{e0x - 20:.1f}" cy="{e0y:.1f}" r="3.5" fill="{INK}"/>')
        els.append(txt(e0x, e0y + 34, "第 0 天正午：同时正对太阳与遥远恒星", 10.5, BODY, "middle"))

        # Day 1: Horizontal parallel ray to distant star (360 deg sidereal turn!)
        els.append(f'<line x1="{sx + 10:.1f}" y1="{e1y:.1f}" x2="{e1x - 22:.1f}" y2="{e1y:.1f}" stroke="{GREEN}" stroke-width="1.8" marker-start="url(#arr-green)"/>')
        els.append(txt(144, e1y - 8, "① 转满 360°（恒星日 23h56m04s）", 10.4, GREEN, "middle", weight="700"))

        # Day 1: Slanted ray down-left to Sun (360.986 deg solar day!)
        ux = (sx - e1x) / orb_r
        uy = (sy - e1y) / orb_r
        els.append(
            f'<line x1="{e1x + ux * 20:.1f}" y1="{e1y + uy * 20:.1f}" '
            f'x2="{sx - ux * 26:.1f}" y2="{sy - uy * 26:.1f}" '
            f'stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#arr-orange)"/>'
        )
        els.append(f'<circle cx="{e1x:.1f}" cy="{e1y:.1f}" r="20" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.7"/>')
        els.append(f'<circle cx="{e1x - 20:.1f}" cy="{e1y:.1f}" r="3.6" fill="{GREEN}"/>')
        els.append(f'<circle cx="{e1x + ux * 20:.1f}" cy="{e1y + uy * 20:.1f}" r="3.6" fill="{ORANGE}"/>')

        # Extra 0.986 deg wedge highlight on Day 1 Earth
        els.append(txt(154, 232, "② 再多转 0.986°", 10.2, ORANGE, weight="700"))
        els.append(txt(154, 246, "(+3分56秒=24h正午)", 9.9, ORANGE))

        els.append(card(34, 344, 338, 48, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(46, 363, "关键结论：卫星轨道平面锚定在惯性空间（恒星背景）！", 10.6, GREEN, weight="700"))
        els.append(txt(46, 381, "所以卫星只需对齐地球转满 360° 的恒星日，绝不能对齐太阳。", 10.3, BODY))

        # Right Panel: Consequences of using 24h00m00s (+77 km error)
        els.append(card(402, 62, 338, 344))
        els.append(txt(418, 84, "② 假如错按 24 小时入轨会发生什么？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(418, 102, "差之四分钟，谬以七十七公里：屋顶锅盖两天失锁", 10.8, MUTED))

        # Comparison cards
        els.append(card(418, 118, 306, 86, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(430, 138, "✅ 正确周期：恒星日 T = 86,164.09 s", 11.2, GREEN, weight="700"))
        els.append(txt(430, 158, f"• 地心半径 r = {R_GEO:,.2f} km（高 {H_GEO:,.2f} km）", 10.6, BODY))
        els.append(txt(430, 176, "• 地面经度漂移：0.000° / 天（稳稳钉在同一经度）", 10.6, BODY))
        els.append(txt(430, 194, "• 家用 Ku 波段锅盖（波束宽 ~1.8°）：一次拧紧常年免调", 10.4, GREEN, weight="600"))

        els.append(card(418, 214, 306, 96, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(430, 234, "❌ 错误周期：太阳日 T = 86,400.00 s", 11.2, ORANGE, weight="700"))
        els.append(txt(430, 254, f"• 地心半径 r = {r_wrong:,.2f} km（偏高 +{dh_wrong:.1f} km！）", 10.6, BODY))
        els.append(txt(430, 272, f"• 地面经度西漂：−{drift_deg_day:.3f}° / 天（轨道弧长 ~725 km/天）", 10.6, BODY))
        els.append(txt(430, 290, "• 后果：仅 2 天就漂出锅盖波束，365 天倒退绕地球一圈！", 10.5, ORANGE, weight="700"))

        # Mini longitude drift timeline bar at bottom right
        els.append(txt(418, 330, "错误 24h 轨道的星下点西漂时间轴（相对东经 105° 起点）：", 10.5, INK, weight="600"))
        bx0, by0, bw = 424.0, 356.0, 292.0
        els.append(f'<line x1="{bx0:.1f}" y1="{by0:.1f}" x2="{bx0 + bw:.1f}" y2="{by0:.1f}" stroke="{SLATE}" stroke-width="1.6"/>')
        stops = [
            (0.0, "第0天", "105°E", GREEN),
            (0.25, "第2天", "出波束(-2°)", ORANGE),
            (0.60, "第91天", "15°E", PURPLE),
            (1.0, "第365天", "倒退一整圈", ORANGE),
        ]
        for frac, t_lbl, sub_lbl, col in stops:
            px = bx0 + frac * bw
            els.append(f'<circle cx="{px:.1f}" cy="{by0:.1f}" r="4.5" fill="{col}"/>')
            anch = "start" if frac == 0 else ("end" if frac == 1.0 else "middle")
            els.append(txt(px, by0 - 9, t_lbl, 10.0, col, anch, weight="700"))
            els.append(txt(px, by0 + 17, sub_lbl, 9.8, BODY, anch))

        return figure(
            420,
            "恒星日23小时56分04秒与太阳日24小时几何成因及77公里轨道误差对比图",
            "左图展示地球在绕太阳公转同时自转满360度对齐遥远恒星只需23小时56分04秒，而重新正对太阳需多转0.986度即3分56秒；右图计算若误用24小时周期将使轨道偏高76.9公里、每天向西漂移约0.98度。",
            els,
        )

    # 3. Why Not Hover Over Beijing + Exact GSO / GEO / IGSO Figure-8 Ground Tracks
    def _build_gso_geo_figure8_tracks():
        els = header(
            "地球同步（GSO）≠ 地球静止（GEO）：为什么头顶 8 字舞与赤道单点并存？",
            "左：地心引力锁定轨道面必过地心 O；右：真实球面几何精算的 4 类同步卫星星下点轨迹",
        )

        # Left Card: Force geometry at 40 deg N
        els.append(card(20, 62, 336, 368))
        els.append(txt(36, 84, "① 为什么不能悬停在北京（40°N）正上方？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "万有引力永远指向地心 O，不指向自转轴！", 10.8, MUTED))

        ecx, ecy, er = 156.0, 226.0, 66.0
        # Spin axis Oz
        els.append(f'<line x1="{ecx:.1f}" y1="126" x2="{ecx:.1f}" y2="322" stroke="{SLATE}" stroke-width="1.5" stroke-dasharray="5 3"/>')
        els.append(txt(ecx, 120, "北极自转轴 Oz", 10.4, SLATE, "middle", weight="600"))

        # Earth sphere + Equator
        els.append(f'<circle cx="{ecx:.1f}" cy="{ecy:.1f}" r="{er:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(f'<ellipse cx="{ecx:.1f}" cy="{ecy:.1f}" rx="{er:.1f}" ry="14" fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append(f'<circle cx="{ecx:.1f}" cy="{ecy:.1f}" r="3.2" fill="{INK}"/>')
        els.append(txt(ecx - 10, ecy + 15, "地心 O", 10.4, INK, "end", weight="700"))

        # Hypothetical 40 deg N hovering satellite S
        lat_rad = math.radians(40.0)
        sat_r = 128.0
        sx = ecx + sat_r * math.cos(lat_rad)  # 254.1
        sy = ecy - sat_r * math.sin(lat_rad)  # 143.7
        bx = ecx + er * math.cos(lat_rad)
        by = ecy - er * math.sin(lat_rad)

        # 40N parallel circle axis point A = (ecx, sy)
        els.append(f'<line x1="{ecx:.1f}" y1="{sy:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="{PURPLE}" stroke-width="1.6" stroke-dasharray="4 3" marker-start="url(#arr-muted)"/>')
        els.append(txt((ecx + sx) / 2, sy - 7, "悬停所需向心力（指向轴）", 10.0, PURPLE, "middle", weight="600"))

        # True Gravity vector S -> O
        gx_end = sx + 0.52 * (ecx - sx)
        gy_end = sy + 0.52 * (ecy - sy)
        els.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{gx_end:.1f}" y2="{gy_end:.1f}" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>')
        els.append(txt(sx + 6, sy + 32, "真实引力 F_g", 10.6, ORANGE, weight="700"))
        els.append(txt(sx + 6, sy + 46, "（直指地心 O！）", 10.2, ORANGE))

        # Inclined plane slicing O from 40N to 40S
        s_south_x = ecx - sat_r * math.cos(lat_rad)
        s_south_y = ecy + sat_r * math.sin(lat_rad)
        els.append(f'<line x1="{s_south_x + 28:.1f}" y1="{s_south_y - 23:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="3 3"/>')

        els.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3.6" fill="{INK}"/>')
        els.append(txt(bx - 6, by - 6, "40°N", 10.2, INK, "end", weight="700"))
        els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="5.8" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')

        # Explanation card at bottom left
        els.append(card(34, 334, 308, 82, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(46, 353, "力学铁律：无外力推力时，轨道平面必过地心 O！", 10.6, ORANGE, weight="700"))
        els.append(txt(46, 371, "• 只要在北纬 40° 出现，半圈后必穿过赤道去南纬 40°；", 10.3, BODY))
        els.append(txt(46, 389, "• 唯一能让“向轴”与“向地心”重合的平面——只有赤道面！", 10.3, BODY))
        els.append(txt(46, 407, "  （倾角 i = 0°、偏心率 e = 0 ⇒ 地球静止轨道 GEO）", 10.2, GREEN, weight="700"))

        # Right Card: Exact Computed Sub-satellite Ground Tracks
        els.append(card(372, 62, 368, 368))
        els.append(txt(388, 84, "② 同步卫星星下点轨迹（以 118°E 为中心经度）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(388, 102, "同样 23h56m04s 转一圈，倾角 i 与偏心率 e 决定地面舞步", 10.8, MUTED))

        mx0, my0, mw, mh = 424.0, 122.0, 292.0, 214.0  # lon [-30, +30], lat [-65, +65]
        lon_span, lat_span = 30.0, 65.0

        def map_ll(dlon_deg, lat_deg):
            x = mx0 + ((dlon_deg + lon_span) / (2.0 * lon_span)) * mw
            y = my0 + ((lat_span - lat_deg) / (2.0 * lat_span)) * mh
            return x, y

        # Map box + grid
        els.append(f'<rect x="{mx0:.1f}" y="{my0:.1f}" width="{mw:.1f}" height="{mh:.1f}" fill="#f8fafc" stroke="{BORDER}" stroke-width="1.2"/>')
        for lat_g in (-55, -33, 0, 33, 55):
            _, py = map_ll(0, lat_g)
            sw = "1.5" if lat_g == 0 else "1"
            col = SLATE if lat_g == 0 else BORDER
            els.append(f'<line x1="{mx0:.1f}" y1="{py:.1f}" x2="{mx0 + mw:.1f}" y2="{py:.1f}" stroke="{col}" stroke-width="{sw}"/>')
            lbl = "0° 赤道" if lat_g == 0 else (f"{lat_g}°N" if lat_g > 0 else f"{abs(lat_g)}°S")
            els.append(txt(mx0 - 5, py + 3.5, lbl, 9.8, MUTED, "end"))

        for dlon_g in (-20, -10, 0, 10, 20):
            px, _ = map_ll(dlon_g, 0)
            sw = "1.3" if dlon_g == 0 else "1"
            els.append(f'<line x1="{px:.1f}" y1="{my0:.1f}" x2="{px:.1f}" y2="{my0 + mh:.1f}" stroke="{BORDER}" stroke-width="{sw}"/>')
            lbl = "118°E" if dlon_g == 0 else (f"+{dlon_g}°" if dlon_g > 0 else f"{dlon_g}°")
            els.append(txt(px, my0 + mh + 14, lbl, 9.8, MUTED, "middle"))

        # Helper to compute exact ground track for (i_deg, e, omega_deg)
        def ground_track(i_deg, ecc=0.0, omega_deg=270.0, steps=240):
            inc = math.radians(i_deg)
            om = math.radians(omega_deg)
            # Align central crossing so mean longitude at ascending/reference matches 0
            pts_ll = []
            for k in range(steps + 1):
                M = 2.0 * math.pi * k / steps
                # Solve Kepler's equation E - e sin E = M
                E = M
                for _ in range(8):
                    E = E - (E - ecc * math.sin(E) - M) / (1.0 - ecc * math.cos(E))
                nu = 2.0 * math.atan2(
                    math.sqrt(1.0 + ecc) * math.sin(E / 2.0),
                    math.sqrt(1.0 - ecc) * math.cos(E / 2.0),
                )
                u = om + nu
                lat = math.degrees(math.asin(math.sin(inc) * math.sin(u)))
                ra = math.atan2(math.cos(inc) * math.sin(u), math.cos(u))
                # Subtract Earth uniform rotation M + om_ra0
                ra0 = math.atan2(math.cos(inc) * math.sin(om), math.cos(om))
                dlon = math.degrees(math.atan2(math.sin(ra - (M + ra0)), math.cos(ra - (M + ra0))))
                pts_ll.append((dlon, lat))
            return pts_ll

        # Track A: BeiDou-3 IGSO (i = 55 deg, e = 0)
        igso_pts = ground_track(55.0, 0.0)
        max_igso_lon = max(abs(p[0]) for p in igso_pts)
        assert abs(max_igso_lon - 15.72) < 0.15, f"Unexpected IGSO lon width {max_igso_lon}"
        d_igso = "M " + " L ".join(f"{map_ll(lo, la)[0]:.2f},{map_ll(lo, la)[1]:.2f}" for lo, la in igso_pts)
        els.append(f'<path d="{d_igso}" fill="none" stroke="{BLUE}" stroke-width="2.3"/>')

        # Track B: Syncom 2 (i = 33 deg, e = 0)
        syn2_pts = ground_track(33.0, 0.0)
        d_syn2 = "M " + " L ".join(f"{map_ll(lo, la)[0]:.2f},{map_ll(lo, la)[1]:.2f}" for lo, la in syn2_pts)
        els.append(f'<path d="{d_syn2}" fill="none" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="5 3"/>')

        # Track C: Eccentric Tundra/QZSS-style (i = 43 deg, e = 0.075, omega = 270 deg -> apogee at +43N!)
        # Note: at nu=180 (apogee), u = 270+180 = 90 deg (+43N)! Slow apogee -> tighter northern loop, wider southern loop!
        qzs_pts = ground_track(43.0, 0.075, omega_deg=270.0)
        d_qzs = "M " + " L ".join(f"{map_ll(lo, la)[0]:.2f},{map_ll(lo, la)[1]:.2f}" for lo, la in qzs_pts)
        els.append(f'<path d="{d_qzs}" fill="none" stroke="{PURPLE}" stroke-width="1.7" stroke-dasharray="2.5 2.5"/>')

        # Track D: True GEO (i = 0, e = 0) stationary dot!
        gx_dot, gy_dot = map_ll(0.0, 0.0)
        els.append(f'<circle cx="{gx_dot:.1f}" cy="{gy_dot:.1f}" r="6.5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.8"/>')

        # Clear legend below map
        els.append(f'<circle cx="396" cy="366" r="5" fill="{GREEN}"/>')
        els.append(txt(406, 370, "GEO（i=0°, e=0）：赤道不动点（风云四号 / 北斗 GEO）", 10.4, INK, weight="600"))

        els.append(f'<line x1="390" y1="386" x2="402" y2="386" stroke="{BLUE}" stroke-width="2.4"/>')
        els.append(txt(406, 390, "北斗 IGSO（i=55°, e=0）：±55° 对称 8 字（经度宽 ±15.7°）", 10.0, BLUE, weight="600"))

        els.append(f'<line x1="390" y1="405" x2="402" y2="405" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="4 2"/>')
        els.append(txt(406, 409, "1963 Syncom 2（i=33°）窄 8 字", 10.2, ORANGE))

        els.append(f'<line x1="564" y1="405" x2="576" y2="405" stroke="{PURPLE}" stroke-width="1.8" stroke-dasharray="2.5 2.5"/>')
        els.append(txt(580, 409, "偏心轨道（e=0.075）北窄南宽泪滴", 10.2, PURPLE))

        return figure(
            446,
            "非赤道悬停力学禁令与地球同步轨道星下点8字形轨迹精算图",
            "左图证明万有引力直指地心O而非自转轴，因此任何试图在北纬40度悬停的无动力卫星都会穿过赤道摆向南纬40度；右图精确计算i=0度静止单点、Syncom 2的33度窄8字、北斗IGSO的55度对称8字与偏心轨道不对称泪滴轨迹。",
            els,
        )

    # 4. Clarke's Three-Satellite Coverage, Polar 81.3 deg Blind Spot & Molniya Orbit
    def _build_clarke_and_molniya():
        phi_max = math.degrees(math.acos(R_E / R_GEO))  # 81.30 deg
        phi_5deg = math.degrees(math.acos((R_E / R_GEO) * math.cos(math.radians(5.0)))) - 5.0  # 76.31 deg
        assert abs(phi_max - 81.30) < 0.05
        assert abs(phi_5deg - 76.31) < 0.08

        els = header(
            "克拉克三颗星覆盖全球的几何学：为什么 ±81.3° 极区永远看不见它？",
            "左：真比例球面切线决定极区盲区与 120° 三星接力；右：高纬“闪电轨道”远地点慢速悬停破局",
        )

        # Left Panel: True scale Earth (R_E) vs GEO ring (6.61 R_E)
        els.append(card(20, 62, 356, 360))
        els.append(txt(36, 84, "① 1 : 6.61 真比例切线与三颗星全球网", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "cos φ_max = R_E / r_GEO = 6,378 / 42,164 ⇒ φ_max = 81.3°", 10.6, MUTED))

        cx, cy = 198.0, 232.0
        r_geo_px = 104.0
        r_e_px = r_geo_px * (R_E / R_GEO)  # 15.73 px (exact 1 : 6.61!)

        # GEO ring
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_geo_px:.1f}" fill="none" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="5 3"/>')

        # 3 Clarke satellites 120 deg apart: Top-Right (0 deg -> put primary at East 0 deg so meridional cross-section N/S poles are Up/Down!)
        # Wait: let's show Meridional View for primary satellite S1 on the RIGHT (cx + r_geo_px, cy), with N pole UP, S pole DOWN!
        # Wait: can S2 and S3 be in the equatorial plane while N/S is meridional? Better: clearly label the outer 120° triangle as equatorial Clarke layout OR draw primary S1 tangent cone on meridional Earth + inset / clean dual cue! Let's make Left Panel pure Meridional Cross-Section (showing exact 81.3° N/S tangent cone!) on top/center, and a crisp Equatorial 3-Satellite 120° mini-diagram right beside it—or better yet:
        # Let's check space in Left Panel (356 x 360):
        # Center of Meridional Cross-section at (136, 224) with r_geo_px = 96 px (Earth r = 14.5 px, OR zoomed Earth callout? Wait: if Earth is 14.5 px, 81.3 deg is small!).
        # Let's calculate: if we draw S1 at (332, 212) and Earth centered at (114, 212) with r_e_px = 54 px, how far is S1 at true scale? 54 * 6.61 = 357 px -> (471, 212) — across panel! Or if r_e_px = 34 px: 34 * 6.61 = 224.7 px! Check that:
        # Earth at (104, 216) with r_e_px = 33.0 px, S1 at (104 + 218.1 = 322.1, 216)!
        # Let's check! 104 - 33 = 71 (well inside left border 20!), and 322.1 + 14 = 336 (well inside right card border 376 = 20+356!).
        # AND r_e_px = 33.0 px is LARGE enough to clearly draw the North Pole, South Pole, ±81.3° tangent points, right-angle symbols, AND polar blind caps, at 100% TRUE 1 : 6.61 SCALE! Plus a neat 3-satellite 120° badge in the bottom strip! That is way clearer!

        ex, ey = 96.0, 206.0
        re_p = 34.0
        sx = ex + re_p * (R_GEO / R_E)  # 96 + 224.76 = 320.76 px!
        sy = ey

        # Exact tangent points on Earth at +-81.30 deg latitude
        phi_rad = math.acos(R_E / R_GEO)  # 81.30 deg
        tx = ex + re_p * math.cos(phi_rad)  # 96 + 5.14 = 101.14
        ty_n = ey - re_p * math.sin(phi_rad)  # 206 - 33.61 = 172.39
        ty_s = ey + re_p * math.sin(phi_rad)  # 206 + 33.61 = 239.61

        # Illuminated coverage cone fill
        els.append(
            f'<path d="M {sx:.1f},{sy:.1f} L {tx:.1f},{ty_n:.1f} '
            f'A {re_p:.1f},{re_p:.1f} 0 0 1 {tx:.1f},{ty_s:.1f} Z" '
            f'fill="{GREEN}" fill-opacity="0.11"/>'
        )
        # Tangent rays S -> T_N and S -> T_S
        els.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{tx:.1f}" y2="{ty_n:.1f}" stroke="{GREEN}" stroke-width="1.8"/>')
        els.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{tx:.1f}" y2="{ty_s:.1f}" stroke="{GREEN}" stroke-width="1.8"/>')
        els.append(f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="{SLATE}" stroke-width="1.2" stroke-dasharray="4 3"/>')

        # Earth sphere + polar blind caps (>81.3 deg N/S highlighted in orange!)
        els.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{re_p:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
        # North polar blind cap arc from (ex - re_p*cos(phi), ty_n) over North Pole to (tx, ty_n)
        tx_left = ex - re_p * math.cos(phi_rad)
        els.append(
            f'<path d="M {tx_left:.1f},{ty_n:.1f} A {re_p:.1f},{re_p:.1f} 0 0 1 {tx:.1f},{ty_n:.1f}" '
            f'fill="none" stroke="{ORANGE}" stroke-width="3.4"/>'
        )
        els.append(
            f'<path d="M {tx_left:.1f},{ty_s:.1f} A {re_p:.1f},{re_p:.1f} 0 0 0 {tx:.1f},{ty_s:.1f}" '
            f'fill="none" stroke="{ORANGE}" stroke-width="3.4"/>'
        )
        # Radius to tangent point T_N
        els.append(f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{tx:.1f}" y2="{ty_n:.1f}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<circle cx="{tx:.1f}" cy="{ty_n:.1f}" r="3.2" fill="{ORANGE}"/>')
        els.append(f'<circle cx="{tx:.1f}" cy="{ty_s:.1f}" r="3.2" fill="{ORANGE}"/>')
        els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="6.2" fill="{GREEN}" stroke="#ffffff" stroke-width="1.6"/>')

        els.append(txt(ex, ey - re_p - 10, "北极盲区 (>81.3°N)", 10.3, ORANGE, "middle", weight="700"))
        els.append(txt(ex, ey + re_p + 18, "南极盲区 (>81.3°S)", 10.3, ORANGE, "middle", weight="700"))
        els.append(txt((ex + sx) / 2 + 12, ey - 8, "r_GEO = 6.61 R_E（严格 1:1 真实比例）", 10.2, SLATE, "middle"))
        els.append(txt(sx - 6, sy + 22, "GEO 卫星", 10.6, GREEN, "end", weight="700"))
        els.append(txt(sx - 6, sy + 36, "单星可视 42.4% 地球面积", 10.0, MUTED, "end"))

        # Bottom mini-panel inside Left Card: Clarke 1945 3-satellite 120 deg equatorial relay
        els.append(card(34, 286, 328, 122, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        mcx, mcy, mr_g, mr_e = 92.0, 347.0, 42.0, 7.0
        els.append(f'<circle cx="{mcx:.1f}" cy="{mcy:.1f}" r="{mr_g:.1f}" fill="none" stroke="{GREEN}" stroke-width="1.3" stroke-dasharray="3 3"/>')
        els.append(f'<circle cx="{mcx:.1f}" cy="{mcy:.1f}" r="{mr_e:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.4"/>')
        tri_pts = []
        for ang_d in (90, 210, 330):
            ar = math.radians(ang_d)
            px = mcx + mr_g * math.cos(ar)
            py = mcy - mr_g * math.sin(ar)
            tri_pts.append((px, py))
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.2" fill="{GREEN}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(
            f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in tri_pts)}" '
            f'fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="3 2"/>'
        )
        els.append(txt(150, 311, "克拉克 1945 构想：赤道俯视 120° 三星组网", 10.8, INK, weight="700"))
        els.append(txt(150, 331, "• 3 颗星相隔 120° 即可无缝覆盖全球经度", 10.3, BODY))
        els.append(txt(150, 350, "• 实际工程要求仰角 ≥ 5°（防楼宇/大气折射）", 10.3, BODY))
        els.append(txt(150, 369, f"  有效南北界约为 ±{phi_5deg:.1f}°，北冰洋仍失联！", 10.3, ORANGE, weight="700"))
        els.append(txt(150, 389, "• 极地科考与高纬通信必须另请“奇兵” →", 10.2, MUTED))

        # Right Panel: Molniya High-Eccentricity Orbit (Kepler 2nd Law Equal-Time Dots!)
        els.append(card(392, 62, 348, 360))
        els.append(txt(408, 84, "② 极区救星：“闪电轨道”（Molniya）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(408, 102, "倾角 63.4°、周期 11h58m：用开普勒第二定律在北极“慢放”", 10.6, MUTED))

        # Exact Molniya parameters: rp = 6378+600 = 6978 km, ra = 6378+39750 = 46128 km
        rp_m, ra_m = R_E + 600.0, R_E + 39750.0
        a_m = 0.5 * (rp_m + ra_m)  # 26553 km
        e_m = (ra_m - rp_m) / (ra_m + rp_m)  # 0.7372
        inc_m = math.radians(63.4)

        # Project orbit in meridional plane: focus (Earth center) at (516, 286), apogee up-right at +63.4 deg!
        fcx, fcy = 500.0, 292.0
        sc_m = 178.0 / ra_m  # 178 px for ra_m = 46,128 km!
        re_mp = R_E * sc_m  # 24.6 px

        # Unit vector toward apogee (up-right at +63.4 deg from equatorial horizontal)
        ux_a, uy_a = math.cos(inc_m), -math.sin(inc_m)
        # Perpendicular in-plane unit vector for minor axis visual perspective (slight 3D tilt 0.55)
        ux_b, uy_b = -math.sin(inc_m), -math.cos(inc_m)

        mol_pts = []
        for k in range(181):
            nu = 2.0 * math.pi * k / 180.0
            r_cur = (a_m * (1.0 - e_m ** 2)) / (1.0 + e_m * math.cos(nu))
            # nu=0 is perigee (-ux_a), nu=pi is apogee (+ux_a)
            x_orb = -r_cur * math.cos(nu)  # +ra at nu=pi, -rp at nu=0
            y_orb = r_cur * math.sin(nu) * 0.62
            px = fcx + (x_orb * ux_a + y_orb * ux_b) * sc_m
            py = fcy + (x_orb * uy_a + y_orb * uy_b) * sc_m
            mol_pts.append((px, py))

        els.append(f'<path d="M {" L ".join(f"{x:.2f},{y:.2f}" for x, y in mol_pts)} Z" fill="{PURPLE_SOFT}" fill-opacity="0.35" stroke="{PURPLE}" stroke-width="2.0"/>')

        # Spin axis + Earth at focus (fcx, fcy)
        els.append(f'<line x1="{fcx:.1f}" y1="126" x2="{fcx:.1f}" y2="334" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="422" y1="{fcy:.1f}" x2="640" y2="{fcy:.1f}" stroke="{BORDER}" stroke-width="1.2"/>')
        els.append(f'<circle cx="{fcx:.1f}" cy="{fcy:.1f}" r="{re_mp:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(txt(fcx, fcy + 4, "地球", 10.2, BLUE, "middle", weight="700"))

        # Plot 12 EQUAL-TIME dots (every 1 hour of the 12-hour period!)
        for hr in range(12):
            M = 2.0 * math.pi * (hr / 12.0)  # hr=0 at perigee, hr=6 at apogee!
            E = M
            for _ in range(10):
                E = E - (E - e_m * math.sin(E) - M) / (1.0 - e_m * math.cos(E))
            nu = 2.0 * math.atan2(
                math.sqrt(1.0 + e_m) * math.sin(E / 2.0),
                math.sqrt(1.0 - e_m) * math.cos(E / 2.0),
            )
            r_cur = (a_m * (1.0 - e_m ** 2)) / (1.0 + e_m * math.cos(nu))
            x_orb = -r_cur * math.cos(nu)
            y_orb = r_cur * math.sin(nu) * 0.62
            px = fcx + (x_orb * ux_a + y_orb * ux_b) * sc_m
            py = fcy + (x_orb * uy_a + y_orb * uy_b) * sc_m
            is_high = 2 <= hr <= 10
            col = PURPLE if is_high else ORANGE
            rad_d = 4.6 if hr == 6 else 3.6
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rad_d}" fill="{col}" stroke="#ffffff" stroke-width="1.1"/>')

        # Apogee & Perigee annotations
        ap_x = fcx + ra_m * ux_a * sc_m
        ap_y = fcy + ra_m * uy_a * sc_m
        els.append(txt(ap_x + 12, ap_y + 4, "远地点 39,750 km", 10.8, PURPLE, weight="700"))
        els.append(txt(ap_x + 12, ap_y + 20, "v ≈ 1.5 km/s（极慢！）", 10.3, PURPLE))
        els.append(txt(606, 206, "每点间隔 = 1 小时：", 10.4, INK, weight="700"))
        els.append(txt(606, 222, "12 小时里有 8 小时以上", 10.3, PURPLE, weight="600"))
        els.append(txt(606, 238, "高悬北半球高纬头顶！", 10.3, PURPLE, weight="600"))
        els.append(txt(424, 326, "近地点 600 km", 10.2, ORANGE, weight="700"))
        els.append(txt(424, 340, "v ≈ 10.0 km/s 掠过南半球", 10.0, ORANGE))

        els.append(card(406, 354, 320, 54, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(418, 373, "为什么选 63.4°“临界倾角”？因为地球扁率摄动在此归零，", 10.3, PURPLE, weight="700"))
        els.append(txt(418, 391, "远地点永远锁在北半球不漂移，3 颗星接力即可全天照亮北极！", 10.2, BODY))

        return figure(
            436,
            "克拉克三颗静止卫星全球覆盖几何切线81.3度盲区与闪电轨道高纬接力对比图",
            "左图按1比6.61真实比例画出地球静止轨道切线，证明南北纬81.3度以上存在极区盲区，并展示克拉克120度三星覆盖；右图按开普勒方程标出闪电轨道12个等时间间隔（每1小时）点位，展示远地点慢速高纬悬停原理。",
            els,
        )

    # 5. GTO Apogee Plane-Change & Why Hainan Wenchang Saves Fuel
    def _build_gto_plane_change_wenchang():
        rp_gto = R_E + 200.0
        ra_gto = R_GEO
        a_gto = 0.5 * (rp_gto + ra_gto)
        vp = math.sqrt(MU_E * (2.0 / rp_gto - 1.0 / a_gto))  # 10.239 km/s
        va = math.sqrt(MU_E * (2.0 / ra_gto - 1.0 / a_gto))  # 1.597 km/s
        t_coast_hr = (math.pi * math.sqrt((a_gto ** 3) / MU_E)) / 3600.0  # 5.255 h

        def akm_dv(lat_deg):
            di = math.radians(lat_deg)
            return math.sqrt(va ** 2 + V_GEO ** 2 - 2.0 * va * V_GEO * math.cos(di)) * 1000.0  # m/s

        dv_kourou = akm_dv(5.2)
        dv_wenchang = akm_dv(19.6)
        dv_xichang = akm_dv(28.2)
        dv_jiuquan = akm_dv(41.0)
        dv_baikonur = akm_dv(45.9)
        assert abs(dv_wenchang - 1656.0) < 5.0
        assert abs(dv_xichang - 1831.0) < 8.0

        els = header(
            "怎么把卫星“掰”上赤道？GTO 远地点变轨与海南文昌的省油账本",
            f"近地点 {vp:.2f} km/s 太快掰不动，必须滑行 {t_coast_hr:.2f} 小时到远地点（{va:.2f} km/s）把圆化与消倾角合二为一",
        )

        # Left Panel: GTO Transfer + Apogee Velocity Vector Triangle
        els.append(card(20, 62, 352, 360))
        els.append(txt(36, 84, "① 地球同步转移轨道（GTO）与余弦定理点火", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "Δv_AKM = √(v_a² + v_GEO² − 2 v_a v_GEO cos Δi)", 10.8, MUTED))

        # Top sub-diagram: Inclined GTO ellipse meeting Equatorial GEO ring at Apogee node
        ocx, ocy = 128.0, 198.0
        els.append(f'<ellipse cx="{ocx + 42:.1f}" cy="{ocy:.1f}" rx="112" ry="36" fill="none" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="5 3"/>')
        els.append(txt(ocx + 116, ocy - 36, "赤道 GEO 圆轨 (i=0°)", 10.2, GREEN, "middle", weight="600"))

        # Tilted GTO ellipse
        els.append(
            f'<g transform="rotate(-17 {ocx + 84:.1f} {ocy:.1f})">'
            f'<ellipse cx="{ocx + 42:.1f}" cy="{ocy:.1f}" rx="70" ry="22" fill="{ORANGE_SOFT}" fill-opacity="0.35" stroke="{ORANGE}" stroke-width="2.0"/>'
            f'</g>'
        )
        els.append(f'<circle cx="{ocx - 16:.1f}" cy="{ocy + 18:.1f}" r="14" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
        els.append(txt(ocx - 16, ocy + 44, "近地点 200 km", 10.0, BLUE, "middle", weight="600"))
        els.append(txt(ocx - 16, ocy + 56, f"v_p = {vp:.2f} km/s", 9.8, MUTED, "middle"))

        # Apogee node at right (ocx + 154, ocy) -> adjust exact intersection at (282, 198)
        ax_n, ay_n = 240.0, 198.0
        els.append(f'<circle cx="{ax_n:.1f}" cy="{ay_n:.1f}" r="6.0" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(txt(ax_n + 10, ay_n - 8, "远地点交点", 10.5, ORANGE, weight="700"))
        els.append(txt(ax_n + 10, ay_n + 6, "35,786 km 点火！", 10.2, ORANGE, weight="600"))

        # Bottom sub-diagram in Left Card: Exact Velocity Vector Triangle (for Δi = 28.2 deg)
        els.append(card(34, 268, 324, 140, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(46, 288, "远地点速度矢量三角形（以 Δi = 28.2° 为例）：", 10.6, INK, weight="700"))

        vx0, vy0 = 64.0, 378.0
        v_scale = 76.0  # px per km/s -> v_GEO (3.075) = 233.7 px!
        # v_GEO horizontal to the right
        vg_x, vg_y = vx0 + V_GEO * v_scale, vy0
        # v_a tilted up by 28.2 deg
        ang_v = math.radians(28.2)
        va_x = vx0 + va * v_scale * math.cos(ang_v)
        va_y = vy0 - va * v_scale * math.sin(ang_v)

        els.append(f'<line x1="{vx0:.1f}" y1="{vy0:.1f}" x2="{vg_x:.1f}" y2="{vg_y:.1f}" stroke="{GREEN}" stroke-width="2.4" marker-end="url(#arr-green)"/>')
        els.append(f'<line x1="{vx0:.1f}" y1="{vy0:.1f}" x2="{va_x:.1f}" y2="{va_y:.1f}" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>')
        els.append(f'<line x1="{va_x:.1f}" y1="{va_y:.1f}" x2="{vg_x:.1f}" y2="{vg_y:.1f}" stroke="{ORANGE}" stroke-width="2.4" stroke-dasharray="5 3" marker-end="url(#arr-orange)"/>')

        els.append(txt((vx0 + vg_x) / 2, vy0 + 18, f"目标速度 v_GEO = {V_GEO:.2f} km/s（赤道面 0°）", 10.2, GREEN, "middle", weight="700"))
        els.append(txt(va_x - 8, va_y - 8, f"到站速度 v_a = {va:.2f} km/s", 10.2, BLUE, weight="700"))
        els.append(txt((va_x + vg_x) / 2 + 18, (va_y + vg_y) / 2 - 6, f"合成点火 Δv = {dv_xichang/1000:.2f} km/s", 10.3, ORANGE, "middle", weight="700"))
        els.append(txt(vx0 + 36, vy0 - 8, "Δi", 10.4, INK, weight="700"))

        # Right Panel: Spaceport Latitude vs Apogee Kick Delta-V Bar Comparison
        els.append(card(388, 62, 352, 360))
        els.append(txt(404, 84, "② 全球发射场纬度大比拼：文昌省下多少燃料？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "直接向东入轨最小倾角 i_min ≈ 发射场纬度 |φ|", 10.8, MUTED))

        sites = [
            ("赤道理想基准 (0°)", 0.0, akm_dv(0.0), SLATE),
            ("法属库鲁 (5.2°N)", 5.2, dv_kourou, BLUE),
            ("中国海南文昌 (19.6°N)", 19.6, dv_wenchang, GREEN),
            ("西昌 / 卡角 (~28.3°N)", 28.2, dv_xichang, ORANGE),
            ("中国酒泉 (41.0°N)", 41.0, dv_jiuquan, PURPLE),
            ("拜科努尔 (45.9°N)", 45.9, dv_baikonur, SLATE),
        ]

        bx_start = 548.0
        max_bar_w = 162.0
        dv_cap = 2450.0
        y_row0 = 132.0
        row_step = 36.0

        for idx, (name, lat_d, dv_val, col) in enumerate(sites):
            ry = y_row0 + idx * row_step
            bw = (dv_val / dv_cap) * max_bar_w
            is_wc = "文昌" in name
            fill_op = "0.24" if is_wc else "0.14"
            sw = "1.8" if is_wc else "1.1"
            els.append(txt(540, ry + 13, name, 10.5, GREEN if is_wc else BODY, "end", weight="700" if is_wc else "400"))
            els.append(
                f'<rect x="{bx_start:.1f}" y="{ry:.1f}" width="{bw:.1f}" height="18" rx="4" '
                f'fill="{col}" fill-opacity="{fill_op}" stroke="{col}" stroke-width="{sw}"/>'
            )
            els.append(txt(bx_start + bw + 6, ry + 13, f"{dv_val:.0f} m/s", 10.3, col, weight="700"))

        # Summary callout box at bottom of Right Card
        save_vs_xc = dv_xichang - dv_wenchang
        save_vs_jq = dv_jiuquan - dv_wenchang
        els.append(card(402, 348, 324, 62, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(414, 367, f"文昌红利：远地点变轨比西昌省 ~{save_vs_xc:.0f} m/s，比酒泉省 ~{save_vs_jq:.0f} m/s！", 10.5, GREEN, weight="700"))
        els.append(txt(414, 385, "• 按每年 ~50 m/s 轨位保持燃料算，省出 3.5～10 年在轨寿命；", 10.2, BODY))
        els.append(txt(414, 402, "• 且海运直达无铁路隧道限宽，长征五号等 5 米大火箭得以登场。", 10.2, BODY))

        return figure(
            436,
            "地球同步转移轨道GTO远地点合成变轨矢量三角形与文昌发射场纬度省油对比图",
            "左图展示200公里停泊轨道经GTO滑行5.26小时至35786公里远地点，利用余弦定理一次完成提速圆化与消除轨道倾角；右图对比库鲁、海南文昌、西昌/卡纳维拉尔角、酒泉与拜科努尔的远地点所需Δv。",
            els,
        )

    # 6. Station-Keeping Perturbations, 240 ms Light Latency & +300 km Graveyard Orbit
    def _build_station_keeping_and_graveyard():
        # Exact light-speed propagation latency: ground -> GEO -> ground
        # Sub-satellite vertical: 2 * 35786 / 299792.458 = 0.2387 s; mid-latitude slant (~38,500 km): 2 * 38500 / 299792.458 = 0.2568 s
        hop_min_ms = (2.0 * H_GEO / 299792.458) * 1000.0  # 238.7 ms
        hop_typ_ms = (2.0 * 38500.0 / 299792.458) * 1000.0  # 256.8 ms
        assert 238.0 < hop_min_ms < 240.0

        # Graveyard orbit Hohmann boost for +300 km above GEO
        r_grave = R_GEO + 300.0
        a_gr = 0.5 * (R_GEO + r_grave)
        dv_grave = (
            (math.sqrt(MU_E * (2.0 / R_GEO - 1.0 / a_gr)) - V_GEO)
            + (math.sqrt(MU_E / r_grave) - math.sqrt(MU_E * (2.0 / r_grave - 1.0 / a_gr)))
        ) * 1000.0  # ~10.87 m/s!
        assert 10.5 < dv_grave < 11.3

        els = header(
            "“静止”背后的终身拔河：轨位保持、240 毫秒延迟与 +300 km 坟墓轨道",
            "卫星并非放上去就一劳永逸——既要对抗地球扁率与日月拉扯，退役前还要留最后一口燃料让位",
        )

        # Left Panel: Station-Keeping (Equatorial Triaxiality + Lunar-Solar NSSK + ITU 0.1 deg box)
        els.append(card(20, 62, 356, 366))
        els.append(txt(36, 84, "① 轨位保持：严守 ±0.05°（约 74 km）“空中车位”", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "赤道微椭圆东西拉拽 + 日月引力每年把轨道面掰歪 ~0.85°", 10.6, MUTED))

        # Equatorial triaxial cross-section (exaggerated ellipse for visibility, clearly labeled)
        ecx, ecy = 198.0, 206.0
        els.append(f'<circle cx="{ecx:.1f}" cy="{ecy:.1f}" r="74" fill="none" stroke="{BORDER}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(
            f'<g transform="rotate(-15 {ecx:.1f} {ecy:.1f})">'
            f'<ellipse cx="{ecx:.1f}" cy="{ecy:.1f}" rx="42" ry="30" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.7"/>'
            f'</g>'
        )
        els.append(txt(ecx, ecy - 2, "赤道微椭圆", 10.2, BLUE, "middle", weight="700"))
        els.append(txt(ecx, ecy + 12, "(扁率夸张示意)", 9.6, MUTED, "middle"))

        # Two stable gravity wells: 75.3E (bottom-right) and 108W (top-left)
        els.append(f'<circle cx="{ecx + 64:.1f}" cy="{ecy + 37:.1f}" r="5.2" fill="{ORANGE}"/>')
        els.append(txt(ecx + 72, ecy + 42, "75.3°E 重力谷", 10.2, ORANGE, weight="700"))
        els.append(f'<circle cx="{ecx - 64:.1f}" cy="{ecy - 37:.1f}" r="5.2" fill="{ORANGE}"/>')
        els.append(txt(ecx - 72, ecy - 34, "108°W 重力谷", 10.2, ORANGE, "end", weight="700"))

        # ITU Slot box at top of ring
        els.append(f'<rect x="{ecx - 11:.1f}" y="{ecy - 85:.1f}" width="22" height="22" rx="3" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
        els.append(f'<circle cx="{ecx:.1f}" cy="{ecy - 74:.1f}" r="4.2" fill="{GREEN}"/>')
        els.append(txt(ecx + 16, ecy - 76, "ITU 轨位盒 (±0.05° ≈ 74 km)", 10.2, GREEN, weight="700"))

        # Fuel budget breakdown cards
        els.append(card(34, 298, 328, 116, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(46, 318, "每年轨位保持（Station-Keeping）燃料账单：", 10.7, INK, weight="700"))
        els.append(txt(46, 338, "• 南北保持（对抗日月引力掰歪轨道面）：~45–50 m/s / 年（大头！）", 10.2, PURPLE, weight="600"))
        els.append(txt(46, 357, "• 东西保持（对抗赤道重力谷滑落 + 光压）：≤ 2 m/s / 年", 10.2, BODY))
        els.append(txt(46, 376, "• 15 年设计寿命共需 ~750 m/s；新一代霍尔电推进比冲高 5–10 倍，", 10.2, BODY))
        els.append(txt(46, 394, "  大幅减轻燃料死重，让卫星带更多转发器上天！", 10.2, GREEN, weight="600"))

        # Right Panel: Light-Speed Latency + Graveyard Orbit (+300 km)
        els.append(card(392, 62, 348, 366))
        els.append(txt(408, 84, "② 物理代价与体面谢幕：延迟与坟墓轨道", PANEL_TITLE, INK, weight="700"))
        els.append(txt(408, 102, "3.6 万公里连光也要跑四分之一秒；寿终前必须爬高让位", 10.6, MUTED))

        # Sub-card A: Latency comparison (GEO vs LEO)
        els.append(card(406, 118, 320, 128, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(418, 138, "光速硬约束（c = 299,792 km/s）：为什么打游戏怕 GEO？", 10.7, BLUE, weight="700"))
        els.append(txt(418, 159, f"• GEO 单跳（地面 → 星 → 地面，约 7.2–7.7 万 km）：", 10.3, BODY))
        els.append(txt(428, 177, f"单程 {hop_min_ms:.0f}–{hop_typ_ms:.0f} ms，双向往返（RTT）高达 ~480–520 ms！", 10.3, ORANGE, weight="700"))
        els.append(txt(418, 197, "• 低轨星座 LEO（550 km）：单跳空口仅 ~4 ms（往返 ~25 ms）", 10.3, GREEN, weight="600"))
        els.append(txt(418, 217, "• 分工明确：电视广播/气象云图/导航增强选 GEO；", 10.2, BODY))
        els.append(txt(428, 233, "实时语音/高频交易/低时延互联选地面光纤或 LEO。", 10.2, MUTED))

        # Sub-card B: IADC Graveyard Orbit (+300 km)
        els.append(card(406, 258, 320, 156, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(418, 278, "退役规矩：IADC“坟墓轨道”（Graveyard Orbit）", 10.8, ORANGE, weight="700"))
        els.append(txt(418, 297, "ΔH_min = 235 + 1000·C_R·(A/m) km（常抬高 ≥300 km）", 10.0, INK, weight="600"))

        # Visual concentric arc comparison: GEO belt -> +200 km protected zone -> +300 km Graveyard
        els.append(f'<path d="M 424,352 Q 566,326 708,352" fill="none" stroke="{GREEN}" stroke-width="2.2"/>')
        els.append(txt(566, 360, "现役 GEO 黄金环（35,786 km）", 10.0, GREEN, "middle", weight="700"))

        els.append(f'<path d="M 424,324 Q 566,298 708,324" fill="none" stroke="{ORANGE}" stroke-width="2.0" stroke-dasharray="5 3"/>')
        els.append(txt(566, 313, "退役坟墓轨道（+300 km ≈ 36,086 km）", 10.0, ORANGE, "middle", weight="700"))

        els.append(f'<line x1="678" y1="348" x2="678" y2="324" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')
        els.append(txt(418, 382, f"• 仅需最后 Δv ≈ {dv_grave:.1f} m/s（约 3 个月保位燃料）即可永久让位；", 10.2, BODY))
        els.append(txt(418, 400, "• 随后排空余气、断开电池（钝化），守护全人类唯一的静止环。", 10.2, BODY))

        return figure(
            442,
            "地球静止卫星轨位保持摄动账单、240毫秒光速延迟与300公里坟墓轨道图解",
            "左图展示赤道微椭圆75.3E与108W重力谷及日月引力导致的每年约50米每秒轨位保持燃料消耗；右图对比GEO双向约480至520毫秒光速延迟与LEO低延迟分工，并图解退役前消耗约11米每秒爬升300公里进入坟墓轨道的国际规则。",
            els,
        )

    @register("geosync-orbit", "地球同步与静止轨道甜蜜点、恒星日误差、8字星下点、克拉克覆盖与闪电轨道、文昌GTO变轨及坟墓轨道", "mechanics_sky")
    def build_geosync_orbit():
        write_svg(SUBDIR, "angular-chase-sweetspot.svg", _build_angular_chase_sweetspot())
        write_svg(SUBDIR, "sidereal-vs-solar-day.svg", _build_sidereal_vs_solar_day())
        write_svg(SUBDIR, "gso-geo-figure8-tracks.svg", _build_gso_geo_figure8_tracks())
        write_svg(SUBDIR, "clarke-three-satellites-polar-blindspot.svg", _build_clarke_and_molniya())
        write_svg(SUBDIR, "gto-plane-change-wenchang.svg", _build_gto_plane_change_wenchang())
        write_svg(SUBDIR, "station-keeping-graveyard-belt.svg", _build_station_keeping_and_graveyard())


_register_geosync_orbit()


def _register_sky_blue():
    SUBDIR = "sky-blue"
    RED = "#b91c1c"
    RED_SOFT = "#fef2f2"
    TEAL = "#0f766e"
    TEAL_SOFT = "#f0fdfa"
    AMBER = "#b45309"
    AMBER_SOFT = "#fffbeb"
    VIOLET = "#6d28d9"
    VIOLET_SOFT = "#f5f3ff"

    # Exact physical helpers
    # 1. Rayleigh cross-section ratio relative to 700 nm deep red: (700 / lambda_nm)^4
    def rayleigh_rel(lam_nm: float) -> float:
        return (700.0 / lam_nm) ** 4

    assert abs(rayleigh_rel(400.0) / rayleigh_rel(470.0) - (470.0 / 400.0) ** 4) < 1e-12
    assert 1.90 < (470.0 / 400.0) ** 4 < 1.91
    assert 4.91 < rayleigh_rel(470.0) < 4.93

    # 2. Planck spectral irradiance B_lambda(T = 5772 K) normalized to peak = 1.0
    def planck_solar(lam_nm: float, temp_k: float = 5772.0) -> float:
        # h*c / k_B = 1.438776877e7 nm*K
        hc_over_k = 1.438776877e7
        lam5 = (lam_nm / 500.0) ** 5
        ex = math.exp(hc_over_k / (lam_nm * temp_k)) - 1.0
        ex_ref = math.exp(hc_over_k / (502.0 * temp_k)) - 1.0
        val = 1.0 / (lam5 * ex)
        val_ref = 1.0 / (((502.0 / 500.0) ** 5) * ex_ref)
        return val / val_ref

    # 3. Rayleigh optical depth of 1 standard atmosphere (Bucholtz 1995 / Hansen & Travis 1974):
    # tau_R(lambda) = 0.008569 * lam_um^(-4) * (1 + 0.0113 * lam_um^(-2) + 0.00013 * lam_um^(-4))
    def tau_rayleigh_1atm(lam_nm: float) -> float:
        lu = lam_nm / 1000.0
        return 0.008569 * (lu**-4) * (1.0 + 0.0113 * (lu**-2) + 0.00013 * (lu**-4))

    assert 0.18 < tau_rayleigh_1atm(470.0) < 0.20
    assert 0.045 < tau_rayleigh_1atm(650.0) < 0.055

    def _build_rayleigh_fourth_power():
        extra_css = """
  @keyframes sky-wave-ring {
    0% { r: 10px; stroke-opacity: 0.9; }
    100% { r: 62px; stroke-opacity: 0.0; }
  }
  .sky-ring-1 { animation: sky-wave-ring 2.4s ease-out 2 forwards; }
  @media (prefers-reduced-motion: reduce) {
    .sky-ring-1 { animation: none !important; opacity: 0 !important; }
  }"""

        els = header(
            "一、瑞利散射的四次方铁律：为什么波长短一截，散射本领暴涨好几倍？",
            "0.3 nm 氮氧分子电子云被阳光电场摇晃成偶极天线：加速度平方 × 功率平方 = 1/λ⁴",
        )

        # Panel A: Molecular Dipole Antenna, 1 + cos^2(theta) Lobe & 90-deg Polarization
        els.append(card(20, 64, 368, 442))
        els.append(pill(34, 76, "A · 分子偶极子天线 × 90° 线偏振几何", fg=BLUE, bg=BLUE_SOFT, w=340))

        els.append(card(34, 110, 340, 82, rx=8, fill="#f8fafc", stroke=BLUE_LINE, sw=1.1))
        els.append(txt(46, 131, "为什么偏偏反比于波长四次方（I ∝ 1/λ⁴）？", 11.5, INK, weight="700"))
        els.append(txt(46, 152, "① 弹簧电子受迫加速度 a = −ω²x ∝ 1/λ²（快2倍→a大4倍）", 11.5, BLUE, weight="600"))
        els.append(txt(46, 173, "② 偶极辐射光强 I ∝ |E|² ∝ a² ∝ (1/λ²)² = 1/λ⁴！", 11.5, ORANGE, weight="700"))

        # Dipole scattering diagram in center of Panel A
        cx_m, cy_m = 216.0, 286.0
        # Incident unpolarized sunlight beam from left
        els.append(f'<line x1="44" y1="{cy_m}" x2="{cx_m - 18}" y2="{cy_m}" stroke="{AMBER}" stroke-width="3.0"/>')
        # Transverse vibration arrows (vertical + slanted representing unpolarized 2D transverse E-field)
        for bx in (78, 122):
            els.append(f'<line x1="{bx}" y1="{cy_m - 18}" x2="{bx}" y2="{cy_m + 18}" stroke="{AMBER}" stroke-width="1.8"/>')
            els.append(f'<line x1="{bx - 11}" y1="{cy_m + 11}" x2="{bx + 11}" y2="{cy_m - 11}" stroke="{ORANGE}" stroke-width="1.8"/>')
        els.append(txt(44, cy_m - 28, "入射太阳白光", 11.5, AMBER, weight="700"))
        els.append(txt(44, cy_m - 12, "(非偏振横波)", 11.5, MUTED))

        # Exact Rayleigh dipole intensity lobe: r(theta) = R0 * (1 + cos^2 theta) / 2
        lobe_pts = []
        for deg in range(0, 361, 4):
            th = math.radians(deg)
            rad = 32.0 * (1.0 + math.cos(th) ** 2)
            lobe_pts.append(f"{cx_m + rad * math.cos(th):.1f},{cy_m - rad * math.sin(th):.1f}")
        els.append(
            f'<polygon points="{" ".join(lobe_pts)}" fill="{BLUE_SOFT}" fill-opacity="0.65" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="4 3"/>'
        )
        els.append(f'<circle class="sky-ring-1" cx="{cx_m}" cy="{cy_m}" r="28" fill="none" stroke="{BLUE}" stroke-width="2"/>')

        # N2 / O2 molecule at center
        els.append(f'<circle cx="{cx_m - 5}" cy="{cy_m}" r="7.5" fill="{BLUE}"/>')
        els.append(f'<circle cx="{cx_m + 5}" cy="{cy_m}" r="7.5" fill="{TEAL}"/>')
        els.append(txt(cx_m + 18, cy_m - 36, "N₂ / O₂ 分子 (~0.3 nm)", 11.5, INK, weight="700", halo=True))
        els.append(txt(cx_m + 72, cy_m + 4, "相函数 1+cos²θ", 11.5, BLUE, weight="600", halo=True))

        # 90-degree downward scattered ray to observer on ground (strongly linearly polarized!)
        els.append(f'<line x1="{cx_m}" y1="{cy_m + 14}" x2="{cx_m}" y2="386" stroke="{BLUE}" stroke-width="2.6"/>')
        # Pure out-of-plane / horizontal-only single polarization ticks
        for py_t in (326, 352):
            els.append(f'<circle cx="{cx_m}" cy="{py_t}" r="3.6" fill="#ffffff" stroke="{PURPLE}" stroke-width="2"/>')
        els.append(txt(cx_m + 12, 344, "90° 散射光：强线偏振！", 11.5, PURPLE, weight="700"))
        els.append(txt(cx_m + 12, 363, "转偏振墨镜明暗剧变", 11.5, BODY))
        els.append(txt(cx_m - 12, 384, "地面人眼", 11.5, INK, anchor="end", weight="700"))

        # Einstein-Smoluchowski box
        els.append(card(34, 398, 340, 94, rx=8, fill=TEAL_SOFT, stroke=TEAL, sw=1.1))
        els.append(txt(46, 419, "爱因斯坦 (1910) 关键补丁：为什么均匀空气不漆黑？", 11.5, TEAL, weight="700"))
        els.append(txt(46, 440, "• 若气体分子像完美晶格静止排列，侧向散射波两两反相", 11.5, BODY))
        els.append(txt(46, 459, "  完全抵消为零！正是分子热运动制造微米级“密度涨落”，", 11.5, BODY))
        els.append(txt(46, 478, "  才漏出瑞利散射（甚至能靠蓝天亮度算出阿伏伽德罗常数）！", 11.5, INK, weight="700"))

        # Panel B: Exact (700/lambda)^4 Curve from 380 nm to 700 nm
        els.append(card(402, 64, 338, 442))
        els.append(pill(416, 76, "B · 相对散射本领实算 (以 700 nm 深红 = 1×)", fg=VIOLET, bg=VIOLET_SOFT, w=310))

        gx0, gx1 = 456, 720
        gy_top, gy_bot = 122, 364

        def px_l(lam):
            return gx0 + (lam - 380.0) / 320.0 * (gx1 - gx0)

        def py_s(val):
            return gy_bot - (val / 12.0) * (gy_bot - gy_top)

        for y_t in (0, 3, 6, 9, 12):
            yy = py_s(y_t)
            els.append(f'<line x1="{gx0}" y1="{yy:.1f}" x2="{gx1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.9"/>')
            els.append(txt(gx0 - 7, yy + 4, f"{y_t}×", 11.5, MUTED, anchor="end", cls="mono"))

        for x_t in (400, 470, 550, 650, 700):
            xx = px_l(x_t)
            els.append(f'<line x1="{xx:.1f}" y1="{gy_top}" x2="{xx:.1f}" y2="{gy_bot}" stroke="{BORDER}" stroke-width="0.8"/>')
            els.append(txt(xx, gy_bot + 16, str(x_t), 11.5, MUTED, anchor="middle", cls="mono"))

        els.append(f'<line x1="{gx0}" y1="{gy_top}" x2="{gx0}" y2="{gy_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{gx0}" y1="{gy_bot}" x2="{gx1}" y2="{gy_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(txt((gx0 + gx1) / 2, gy_bot + 34, "可见光波长 λ (nm)：紫 → 蓝 → 绿 → 红", 11.5, INK, anchor="middle", weight="700"))

        c_pts = []
        for lam_i in range(380, 702, 4):
            c_pts.append(f"{px_l(lam_i):.1f},{py_s(rayleigh_rel(lam_i)):.1f}")
        els.append(f'<polyline points="{" ".join(c_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

        benchmarks = [
            (400.0, VIOLET, f"400nm 紫 {rayleigh_rel(400):.2f}×", 10, 4, "start"),
            (470.0, BLUE, f"470nm 蓝 {rayleigh_rel(470):.2f}×", 10, -4, "start"),
            (550.0, GREEN, f"550nm 绿 {rayleigh_rel(550):.2f}×", 8, -8, "start"),
            (650.0, RED, f"650nm 红 {rayleigh_rel(650):.2f}×", 0, -12, "middle"),
        ]
        for lam_b, col_b, lbl_b, dx_b, dy_b, anc_b in benchmarks:
            bx_p, by_p = px_l(lam_b), py_s(rayleigh_rel(lam_b))
            els.append(f'<circle cx="{bx_p:.1f}" cy="{by_p:.1f}" r="4.8" fill="{col_b}" stroke="#ffffff" stroke-width="1.4"/>')
            els.append(txt(bx_p + dx_b, by_p + dy_b, lbl_b, 11.5, col_b, anchor=anc_b, weight="700", halo=True))

        els.append(card(416, 408, 310, 84, rx=8, fill=VIOLET_SOFT, stroke=VIOLET, sw=1.2))
        els.append(txt(428, 429, "头号灵魂拷问（紫天悖论）：", 11.5, VIOLET, weight="700"))
        els.append(txt(428, 450, "400 nm 紫光散射高达 9.38×，比 470 nm 蓝光", 11.5, BODY))
        els.append(txt(428, 469, "还猛 1.90 倍！为什么天空不是紫罗兰色的？", 11.5, INK, weight="700"))

        return figure(
            520,
            "瑞利散射分子偶极子1+cos²θ方向图、90度线偏振与波长四次方反比曲线图解",
            "左图展示直径约0.3纳米的氮氧分子在阳光横波电场驱动下按1+cos²θ相函数散射并在90度方向产生强线偏振光，以及爱因斯坦1910年微观密度涨落机制；右图精确绘出(700/λ)⁴散射曲线，显示470纳米蓝光散射为700纳米深红光的4.92倍，而400纳米紫光高达9.38倍。",
            els,
            extra_css=extra_css,
        )

    def _build_violet_paradox_cones():
        els = header(
            "二、破解“紫天悖论”：紫光散射猛近两倍，为什么天空却不是紫色的？",
            "太阳光谱先砍第一刀，人眼视锥细胞再投决定票——宽谱天空光等价于“475 nm 纯蓝 + 白光”",
        )

        # Panel A: Solar Spectrum x Rayleigh Scattering -> Broad Skylight Spectrum
        els.append(card(20, 64, 362, 452))
        els.append(pill(34, 76, "A · 第一刀：太阳辐射短波骤降 + 宽谱散射", fg=AMBER, bg=AMBER_SOFT, w=334))

        sx0, sx1 = 62, 364
        sy_top, sy_bot = 122, 360

        def px_w(lam):
            return sx0 + (lam - 380.0) / 320.0 * (sx1 - sx0)

        def py_n(val):
            return sy_bot - val * (sy_bot - sy_top)

        for y_t in (0.0, 0.5, 1.0):
            yy = py_n(y_t)
            els.append(f'<line x1="{sx0}" y1="{yy:.1f}" x2="{sx1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.9"/>')
            els.append(txt(sx0 - 6, yy + 4, f"{y_t:.1f}", 11.5, MUTED, anchor="end", cls="mono"))

        for x_t in (400, 475, 550, 650):
            xx = px_w(x_t)
            els.append(f'<line x1="{xx:.1f}" y1="{sy_top}" x2="{xx:.1f}" y2="{sy_bot}" stroke="{BORDER}" stroke-width="0.8"/>')
            els.append(txt(xx, sy_bot + 16, str(x_t), 11.5, MUTED, anchor="middle", cls="mono"))

        els.append(f'<line x1="{sx0}" y1="{sy_top}" x2="{sx0}" y2="{sy_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{sx0}" y1="{sy_bot}" x2="{sx1}" y2="{sy_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(txt((sx0 + sx1) / 2, sy_bot + 34, "波长 λ (nm)", 11.5, INK, anchor="middle", weight="700"))

        # Realistic ground-level solar spectrum (5772 K blackbody * Fraunhofer/UV-violet atmospheric roll-off below 440 nm)
        def solar_ground(lam):
            bb = planck_solar(lam, 5772.0)
            uv_drop = 1.0 / (1.0 + math.exp(-(lam - 408.0) / 16.0)) * 0.62 + 0.38
            return bb * uv_drop * math.exp(-1.2 * tau_rayleigh_1atm(lam))

        lams = list(range(380, 702, 4))
        sol_raw = [solar_ground(l) for l in lams]
        sol_max = max(sol_raw)
        sol_norm = [v / sol_max for v in sol_raw]

        sky_raw = [solar_ground(l) * ((500.0 / l) ** 4) for l in lams]
        sky_max = max(sky_raw)
        sky_norm = [v / sky_max for v in sky_raw]

        # Shade broad green/yellow/red tail under sky_norm to show why it's NOT monochromatic!
        poly_sky = [f"{px_w(380):.1f},{sy_bot:.1f}"] + [f"{px_w(l):.1f},{py_n(v):.1f}" for l, v in zip(lams, sky_norm)] + [f"{px_w(700):.1f},{sy_bot:.1f}"]
        els.append(f'<polygon points="{" ".join(poly_sky)}" fill="{BLUE_SOFT}" fill-opacity="0.65"/>')

        pts_sol = [f"{px_w(l):.1f},{py_n(v):.1f}" for l, v in zip(lams, sol_norm)]
        pts_sky = [f"{px_w(l):.1f},{py_n(v):.1f}" for l, v in zip(lams, sky_norm)]
        els.append(f'<polyline points="{" ".join(pts_sol)}" fill="none" stroke="{AMBER}" stroke-width="2.3" stroke-dasharray="5 3"/>')
        els.append(f'<polyline points="{" ".join(pts_sky)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

        els.append(txt(px_w(608), py_n(0.83), "太阳光谱 (~5772 K)", 11.5, AMBER, anchor="middle", weight="700", halo=True))
        els.append(txt(px_w(525), py_n(0.50), "真实天空散射光谱", 11.5, BLUE, weight="700", halo=True))
        els.append(txt(px_w(525), py_n(0.38), "(含可观青绿黄长波尾巴!)", 11.5, INK, halo=True))

        els.append(card(34, 404, 334, 98, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 425, "• 太阳光峰值在 ~500 nm 蓝绿区，一进 400 nm 紫光区", 11.5, BODY))
        els.append(txt(46, 444, "  光子产率与高层透射率双双跳水，砍掉紫光先发优势；", 11.5, BODY))
        els.append(txt(46, 464, "• 更关键：天空光并非单色紫光，而是拖着厚厚一条", 11.5, INK, weight="700"))
        els.append(txt(46, 483, "  青、绿、黄红连续宽谱尾巴（阴影区）冲进人眼！", 11.5, BLUE, weight="700"))

        # Panel B: Human S, M, L Cone Sensitivities & Smith (2005) Metameric Match
        els.append(card(396, 64, 344, 452))
        els.append(pill(410, 76, "B · 第二刀：S/M/L 三色视锥如何否决“紫色”", fg=BLUE, bg=BLUE_SOFT, w=316))

        cx0, cx1 = 438, 724
        cy_top, cy_bot = 122, 294

        def px_c(lam):
            return cx0 + (lam - 380.0) / 320.0 * (cx1 - cx0)

        def py_c(val):
            return cy_bot - val * (cy_bot - cy_top)

        for x_t in (400, 475, 550, 650):
            xx = px_c(x_t)
            els.append(f'<line x1="{xx:.1f}" y1="{cy_top}" x2="{xx:.1f}" y2="{cy_bot}" stroke="{BORDER}" stroke-width="0.8"/>')
            els.append(txt(xx, cy_bot + 15, str(x_t), 11.5, MUTED, anchor="middle", cls="mono"))

        els.append(f'<line x1="{cx0}" y1="{cy_top}" x2="{cx0}" y2="{cy_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{cx0}" y1="{cy_bot}" x2="{cx1}" y2="{cy_bot}" stroke="{INK}" stroke-width="1.3"/>')

        # Smooth physiological S, M, L cone curves (including L-cone beta band near 415 nm!)
        def s_cone(lam):
            return math.exp(-0.5 * ((lam - 442.0) / 24.0) ** 2)

        def m_cone(lam):
            return math.exp(-0.5 * ((lam - 534.0) / 38.0) ** 2)

        def l_cone(lam):
            main = math.exp(-0.5 * ((lam - 564.0) / 44.0) ** 2)
            beta = 0.14 * math.exp(-0.5 * ((lam - 412.0) / 18.0) ** 2)
            return min(1.0, main + beta)

        pts_sc = [f"{px_c(l):.1f},{py_c(s_cone(l)):.1f}" for l in lams]
        pts_mc = [f"{px_c(l):.1f},{py_c(m_cone(l)):.1f}" for l in lams]
        pts_lc = [f"{px_c(l):.1f},{py_c(l_cone(l)):.1f}" for l in lams]
        els.append(f'<polyline points="{" ".join(pts_sc)}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
        els.append(f'<polyline points="{" ".join(pts_mc)}" fill="none" stroke="{GREEN}" stroke-width="2.4"/>')
        els.append(f'<polyline points="{" ".join(pts_lc)}" fill="none" stroke="{RED}" stroke-width="2.4"/>')

        # Mark 475 nm equivalent monochromatic sky hue
        x475 = px_c(475.0)
        els.append(f'<line x1="{x475:.1f}" y1="{cy_top}" x2="{x475:.1f}" y2="{cy_bot}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="4 3"/>')
        els.append(txt(px_c(442), py_c(1.03), "S 蓝", 11.5, BLUE, anchor="middle", weight="700"))
        els.append(txt(px_c(530), py_c(1.03), "M 绿", 11.5, GREEN, anchor="middle", weight="700"))
        els.append(txt(px_c(582), py_c(1.03), "L 红", 11.5, RED, anchor="middle", weight="700"))
        els.append(txt(px_c(410), py_c(0.26), "L紫端小峰", 11.5, RED, anchor="start", weight="600", halo=True))

        els.append(card(410, 320, 316, 182, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.1))
        els.append(txt(422, 341, "Smith (2005, AJP) 严格色度匹配结论：", 11.5, BLUE, weight="700"))
        els.append(txt(422, 362, "• 怎样才显紫色？单色 400 nm 光触发 S 蓝 + L 小峰，", 11.5, BODY))
        els.append(txt(422, 381, "  且几乎不碰 M 绿（大脑把“蓝+微红、缺绿”译成紫）；", 11.5, BODY))
        els.append(txt(422, 401, "• 天空宽谱尾巴同时等比垫高 M 绿和 L 红视锥！", 11.5, INK, weight="700"))
        els.append(txt(422, 421, "• 在人类视网膜里，整片天空光精确同色异谱等价于：", 11.5, BODY))
        els.append(card(422, 430, 292, 30, rx=6, fill="#ffffff", stroke=BLUE))
        els.append(txt(568, 450, "474–476 nm 纯正蓝光 ＋ 大量白光", 11.5, BLUE, anchor="middle", weight="700"))
        els.append(txt(422, 483, "→ 所以是柔和清透的“非饱和天蓝”，而非深紫！", 11.5, INK, weight="700"))

        return figure(
            530,
            "太阳光谱与人眼SML三色视锥细胞破解天空为什么是天蓝色而非紫色的定量图解",
            "左图计算5772K太阳地面光谱乘以λ⁻⁴后的真实天空散射光谱，显示400纳米紫端受太阳光谱跌落压制且保留宽广的青绿黄长波尾巴；右图绘出人眼S蓝、M绿、L红视锥灵敏度曲线，阐明宽谱尾巴等比激励M与L视锥，使晴空同色异谱等价于474至476纳米单色蓝光加白光。",
            els,
        )

    def _build_rayleigh_vs_mie_clouds():
        els = header(
            "三、粒子大小决定颜色命运：为什么天空湛蓝，朵云雪白，乌云却发黑？",
            "同样一束阳光：0.3 nm 分子挑着散射蓝光，10 μm 云滴全波段平权散射白光，厚云靠多次折返遮黑云底",
        )

        # Panel A: Scattering Wavelength Dependence Exponent alpha vs Particle Radius r
        els.append(card(20, 64, 362, 442))
        els.append(pill(34, 76, "A · 粒径跨越 5 个数量级：从挑色散射到全白散射", fg=TEAL, bg=TEAL_SOFT, w=334))

        regimes = [
            (
                "① 空气分子 N₂ / O₂（直径 ~0.3 nm ≪ λ）",
                "尺度参数 x = 2πr/λ ≈ 0.002 → 瑞利散射区",
                "散射 ∝ λ⁻⁴：蓝光散射是红光近 5 倍 → 蔚蓝晴空",
                BLUE,
                BLUE_SOFT,
            ),
            (
                "② 细霾与气溶胶微粒（粒径 0.1–0.5 μm ≈ λ）",
                "尺度参数 x ≈ 1–4 → 瑞利向米氏过渡区",
                "散射 ∝ λ⁻¹·³：波长偏好大减 → 天空变灰白乳浊",
                AMBER,
                AMBER_SOFT,
            ),
            (
                "③ 云滴与雾滴小水珠（半径 5–20 μm ≫ λ）",
                "尺度参数 x ≈ 60–250 → 米氏几何散射平台 (Q≈2)",
                "散射 ∝ λ⁰：红橙黄绿蓝紫平权散射 → 洁白朵云！",
                TEAL,
                TEAL_SOFT,
            ),
        ]
        for idx, (rt, r_sub, r_res, fg_c, bg_c) in enumerate(regimes):
            ry = 112 + idx * 124
            els.append(card(34, ry, 334, 110, rx=8, fill=bg_c, stroke=fg_c, sw=1.2))
            els.append(txt(46, ry + 23, rt, 11.5, fg_c, weight="700"))
            els.append(txt(46, ry + 45, r_sub, 11.5, BODY))
            els.append(card(46, ry + 58, 310, 38, rx=6, fill="#ffffff", stroke=fg_c, sw=0.9))
            els.append(txt(201, ry + 82, r_res, 11.5, INK, anchor="middle", weight="700"))

        # Panel B: Thin Cumulus vs Deep Storm Cumulonimbus + Horizon Whitening
        els.append(card(396, 64, 344, 442))
        els.append(pill(410, 76, "B · 薄云雪白 vs 乌云黑底 & 地平线泛白", fg=SLATE, bg=SLATE_SOFT, w=316))

        # Left sub-diagram: Thin fair-weather cloud (~300 m)
        els.append(card(410, 112, 150, 224, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(485, 132, "晴天薄积云 (~300m)", 11.5, BLUE, anchor="middle", weight="700"))
        els.append(txt(485, 150, "光学厚度 τ ≈ 10–20", 11.5, MUTED, anchor="middle"))
        # Sunlight arrows entering top
        els.append(f'<line x1="485" y1="160" x2="485" y2="184" stroke="{AMBER}" stroke-width="2.4"/>')
        els.append(card(426, 188, 118, 72, rx=22, fill="#ffffff", stroke=BLUE_LINE, sw=1.8))
        els.append(txt(485, 220, "10 μm 纯净水滴", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(485, 239, "全波段散射充足", 11.5, TEAL, anchor="middle", weight="600"))
        # Bright white rays exiting bottom
        for dx_r in (-24, 0, 24):
            els.append(f'<line x1="{485 + dx_r*0.5:.1f}" y1="262" x2="{485 + dx_r:.1f}" y2="296" stroke="{AMBER}" stroke-width="2.0"/>')
        els.append(txt(485, 318, "云底明亮洁白！", 11.5, GREEN, anchor="middle", weight="700"))

        # Right sub-diagram: Thick thundercloud (~6,000 m)
        els.append(card(574, 112, 152, 224, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(650, 132, "雷雨厚积雨云 (>5km)", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(650, 150, "光学厚度 τ > 200", 11.5, MUTED, anchor="middle"))
        # Sunlight entering & >90% reflected upward at cloud top!
        els.append(f'<line x1="636" y1="160" x2="644" y2="182" stroke="{AMBER}" stroke-width="2.4"/>')
        els.append(f'<line x1="656" y1="182" x2="672" y2="160" stroke="{AMBER}" stroke-width="2.2"/>')
        # Bright top + dark bottom gradient cloud
        els.append(card(590, 184, 120, 38, rx=14, fill="#ffffff", stroke=SLATE, sw=1.3))
        els.append(txt(650, 207, "云顶依然雪白刺眼", 11.5, INK, anchor="middle", weight="700"))
        els.append(card(590, 218, 120, 56, rx=12, fill="#334155", stroke="#1e293b", sw=1.3))
        els.append(txt(650, 243, "光线经上百次折返", 11.5, "#f8fafc", anchor="middle"))
        els.append(txt(650, 262, "穿透到底不足 2%！", 11.5, "#fde68a", anchor="middle", weight="700"))
        els.append(f'<line x1="650" y1="276" x2="650" y2="296" stroke="{SLATE}" stroke-width="1.4" stroke-dasharray="3 3"/>')
        els.append(txt(650, 318, "并非脏，是没光透下！", 11.5, RED, anchor="middle", weight="700"))

        # Horizon whitening explanation card
        els.append(card(410, 350, 316, 142, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.1))
        els.append(txt(422, 372, "顺手解开：为什么万里无云时，天边却泛白？", 11.5, BLUE, weight="700"))
        els.append(txt(422, 394, "• 抬头看天顶：只穿 1 倍大气，单次散射蓝光最纯；", 11.5, BODY))
        els.append(txt(422, 415, "• 平视看地平线：斜穿几十倍底层浓密空气与水汽，", 11.5, BODY))
        els.append(txt(422, 436, "  蓝光在半路遭遇“多次散射”损耗，而红绿长波散射", 11.5, BODY))
        els.append(txt(422, 457, "  一路累加追平，各色光重新混成乳白浅蓝色！", 11.5, INK, weight="700"))

        return figure(
            520,
            "瑞利散射与米氏散射三类粒径颜色规律、乌云黑底光学厚度及地平线泛白原理图解",
            "左图对比0.3纳米氮氧分子(λ⁻⁴蓝天)、亚微米霾粒(灰白)与10微米云滴(λ⁰米氏散射白云)的尺度效应；右图解释雷雨乌云并非含脏污而是光学厚度超200导致阳光在云顶折返耗尽，以及平视地平线因多次散射重新混白的原因。",
            els,
        )

    def _build_sunset_and_ozone_zenith():
        els = header(
            "四、日落的双重魔法：38 倍大气筛出火烧云，臭氧层悄悄救回头顶“暮光蓝”",
            "地平线晚霞靠长路径散尽蓝光；但黄昏头顶的深邃宝蓝，竟有三分之二归功于平流层臭氧！",
        )

        # Panel A: Air Mass 1 vs Air Mass 38 Direct Transmittance Spectrum
        els.append(card(20, 64, 370, 452))
        els.append(pill(34, 76, "A · 球壳几何 38 倍闯关：蓝光散尽只剩红霞", fg=ORANGE, bg=ORANGE_SOFT, w=342))

        # Top spherical shell geometry mini-diagram
        els.append(card(34, 110, 342, 134, rx=8, fill="#0f172a", stroke=SLATE))
        # Earth curve + atmosphere shell arc
        els.append('<path d="M 52,232 Q 190,186 356,232" fill="#1e3a8a" stroke="#60a5fa" stroke-width="1.8"/>')
        els.append('<path d="M 44,202 Q 190,148 364,202" fill="none" stroke="#93c5fd" stroke-width="1.3" stroke-dasharray="4 3"/>')
        obs_x, obs_y = 228.0, 207.0
        els.append(f'<circle cx="{obs_x}" cy="{obs_y}" r="4.5" fill="#ffffff"/>')
        # Noon vertical ray (AM = 1)
        els.append(f'<line x1="{obs_x}" y1="122" x2="{obs_x}" y2="{obs_y - 5}" stroke="#fde047" stroke-width="2.6"/>')
        els.append(txt(obs_x + 8, 138, "正午垂直 AM = 1×", 11.5, "#fde047", weight="700"))
        els.append(txt(obs_x + 8, 155, "(蓝光透83%, 红光透95%)", 11.5, "#e2e8f0"))
        # Sunset horizontal grazing ray from left (AM ~ 38)
        els.append(f'<line x1="48" y1="{obs_y - 2}" x2="{obs_x - 6}" y2="{obs_y - 2}" stroke="#f97316" stroke-width="2.8"/>')
        els.append(txt(48, 144, "日落擦地斜穿 AM ≈ 38×！", 11.5, "#fb923c", weight="700"))
        els.append(txt(48, 162, "蓝光剩<0.1%，红橙成霞", 11.5, "#fed7aa"))

        # Bottom exact Rayleigh direct transmittance plot T(lam) = exp(-AM * tau_R(lam))
        tx0, tx1 = 70, 360
        ty_top, ty_bot = 272, 460

        def px_lt(lam):
            return tx0 + (lam - 400.0) / 300.0 * (tx1 - tx0)

        def py_tr(tr_pct):
            return ty_bot - (tr_pct / 105.0) * (ty_bot - ty_top)

        for y_p in (0, 50, 100):
            yy = py_tr(y_p)
            els.append(f'<line x1="{tx0}" y1="{yy:.1f}" x2="{tx1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.9"/>')
            els.append(txt(tx0 - 6, yy + 4, f"{y_p}%", 11.5, MUTED, anchor="end", cls="mono"))

        for x_l in (400, 500, 600, 700):
            xx = px_lt(x_l)
            els.append(f'<line x1="{xx:.1f}" y1="{ty_top}" x2="{xx:.1f}" y2="{ty_bot}" stroke="{BORDER}" stroke-width="0.8"/>')
            els.append(txt(xx, ty_bot + 16, str(x_l), 11.5, MUTED, anchor="middle", cls="mono"))

        els.append(f'<line x1="{tx0}" y1="{ty_top}" x2="{tx0}" y2="{ty_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{tx0}" y1="{ty_bot}" x2="{tx1}" y2="{ty_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(txt((tx0 + tx1) / 2, ty_bot + 36, "阳光直射透射率 vs 波长 λ (nm)", 11.5, INK, anchor="middle", weight="700"))

        lams_t = list(range(400, 702, 5))
        for am_v, col_t, lbl_t, lx_t, ly_off in [
            (1.0, BLUE, "正午 AM=1", 495, -8),
            (6.0, AMBER, "低空10° AM=6", 540, -8),
            (38.0, RED, "地平线日落 AM=38", 605, -18),
        ]:
            pts_tr = [f"{px_lt(l):.1f},{py_tr(100.0 * math.exp(-am_v * tau_rayleigh_1atm(l))):.1f}" for l in lams_t]
            els.append(f'<polyline points="{" ".join(pts_tr)}" fill="none" stroke="{col_t}" stroke-width="2.4"/>')
            y_at = py_tr(100.0 * math.exp(-am_v * tau_rayleigh_1atm(lx_t)))
            els.append(txt(px_lt(lx_t), y_at + ly_off, lbl_t, 11.5, col_t, anchor="middle", weight="700", halo=True))

        # Panel B: Hulburt (1953) Ozone Chappuis Absorption Band Saving Twilight Zenith Blue
        els.append(card(404, 64, 336, 452))
        els.append(pill(418, 76, "B · 胡尔伯特 (1953)：臭氧查普伊带守护暮光蓝", fg=PURPLE, bg=PURPLE_SOFT, w=308))

        els.append(card(418, 110, 308, 66, rx=8, fill=RED_SOFT, stroke=RED, sw=1.1))
        els.append(txt(430, 131, "鲜为人知的反常：如果大气里只有氮气和氧气，", 11.5, RED, weight="700"))
        els.append(txt(430, 151, "日落时正头顶本来会变成灰黄绿色，绝不会是深蓝！", 11.5, INK, weight="700"))
        els.append(txt(430, 168, "是谁吃掉了头顶的橙黄红光？答案：平流层臭氧 O₃！", 11.5, BODY))

        # Exact Hulburt (1953, JOSA 43, p. 114) Ozone Chappuis absorption coefficients k(lambda) (cm^-1 STP)
        # (400, 0.000), (450, 0.0034), (500, 0.053), (550, 0.120), (600, 0.175), (650, 0.084), (700, 0.030), (750, 0.000)
        oz_data = [
            (400, 0.000),
            (430, 0.001),
            (450, 0.0034),
            (480, 0.022),
            (500, 0.053),
            (530, 0.095),
            (550, 0.120),
            (575, 0.155),
            (600, 0.175),
            (625, 0.132),
            (650, 0.084),
            (680, 0.046),
            (700, 0.030),
        ]
        ox0, ox1 = 458, 714
        oy_top, oy_bot = 204, 362

        def px_oz(lam):
            return ox0 + (lam - 400.0) / 300.0 * (ox1 - ox0)

        def py_oz(kv):
            return oy_bot - (kv / 0.20) * (oy_bot - oy_top)

        for kv_t in (0.0, 0.1, 0.2):
            yy = py_oz(kv_t)
            els.append(f'<line x1="{ox0}" y1="{yy:.1f}" x2="{ox1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.9"/>')
            els.append(txt(ox0 - 6, yy + 4, f"{kv_t:.1f}", 11.5, MUTED, anchor="end", cls="mono"))

        for x_l in (400, 500, 600, 700):
            xx = px_oz(x_l)
            els.append(f'<line x1="{xx:.1f}" y1="{oy_top}" x2="{xx:.1f}" y2="{oy_bot}" stroke="{BORDER}" stroke-width="0.8"/>')
            els.append(txt(xx, oy_bot + 16, str(x_l), 11.5, MUTED, anchor="middle", cls="mono"))

        els.append(f'<line x1="{ox0}" y1="{oy_top}" x2="{ox0}" y2="{oy_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{ox0}" y1="{oy_bot}" x2="{ox1}" y2="{oy_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(txt((ox0 + ox1) / 2, oy_bot + 34, "臭氧查普伊带可见光吸收系数 (cm⁻¹)", 11.5, INK, anchor="middle", weight="700"))

        poly_oz = [f"{px_oz(400):.1f},{oy_bot:.1f}"] + [f"{px_oz(l):.1f},{py_oz(k):.1f}" for l, k in oz_data] + [f"{px_oz(700):.1f},{oy_bot:.1f}"]
        els.append(f'<polygon points="{" ".join(poly_oz)}" fill="{PURPLE_SOFT}" fill-opacity="0.8"/>')
        pts_oz = [f"{px_oz(l):.1f},{py_oz(k):.1f}" for l, k in oz_data]
        els.append(f'<polyline points="{" ".join(pts_oz)}" fill="none" stroke="{PURPLE}" stroke-width="2.6"/>')
        els.append(f'<circle cx="{px_oz(600):.1f}" cy="{py_oz(0.175):.1f}" r="4.8" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(px_oz(585), py_oz(0.186), "600 nm 橙黄光吸收洪峰！", 11.5, PURPLE, anchor="middle", weight="700", halo=True))

        els.append(card(418, 408, 308, 94, rx=8, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.1))
        els.append(txt(430, 429, "• 正午竖穿臭氧层 (~3 mm STP)：仅吸 ~4%，无感；", 11.5, BODY))
        els.append(txt(430, 449, "• 日落阳光擦过 25 km 平流层切线，路径暴增数十倍，", 11.5, BODY))
        els.append(txt(430, 469, "  臭氧精准吞光 550–650 nm 橙黄光 → 日落天顶蓝", 11.5, INK, weight="700"))
        els.append(txt(430, 488, "  有 2/3 靠臭氧，日落后“蓝调时刻”几乎全靠臭氧！", 11.5, PURPLE, weight="700"))

        return figure(
            530,
            "日落38倍球壳大气质量透射光谱与胡尔伯特1953年臭氧查普伊吸收带守护黄昏天顶蓝图解",
            "左图精确计算AM=1、6、38时瑞利直射透射率，展示日落擦地斜穿38倍大气滤尽蓝光留下红霞；右图据Hulburt(1953)绘出臭氧500至700纳米查普伊吸收峰(600纳米处极值)，阐明日落与暮光时正头顶深蓝色有三分之二乃至全部归功于平流层臭氧吸收橙黄光。",
            els,
        )

    def _build_planetary_skies():
        els = header(
            "五、放眼太阳系三颗星球：为什么月球正午漆黑，火星却是“黄天配蓝日落”？",
            "同一轮太阳照耀下：大气有无与微粒尺寸彻底改写散射相函数，让地球与火星上演完美反转",
        )

        planets = [
            (
                20,
                "月球 · 超高真空 (~10⁻¹⁵ bar)",
                SLATE,
                SLATE_SOFT,
                "#090d16",
                "#1e293b",
                "#ffffff",
                "正午黑空 + 刺眼白日",
                [
                    "• 散射介质：零大气分子、零悬浮尘",
                    "• 白昼天空：毫无侧向散射 → 漆黑",
                    "  （遮住强光眩光即可在白天看星星）",
                    "• 日落景观：无晨昏蒙影，明暗立切",
                ],
            ),
            (
                266,
                "地球 · 1 bar 氮氧大气",
                BLUE,
                BLUE_SOFT,
                "#2563eb",
                "#ea580c",
                "#fed7aa",
                "白天蔚蓝 → 日落火红",
                [
                    "• 散射主力：0.3 nm N₂ / O₂ 分子",
                    "• 白昼天空：瑞利向四方散蓝 → 蔚蓝",
                    "• 日落景观：蓝光沿途向两侧散尽，",
                    "  穿透长路径直达人眼的只剩红橙光",
                ],
            ),
            (
                512,
                "火星 · 0.006 bar CO₂ + 铁锈尘",
                ORANGE,
                ORANGE_SOFT,
                "#c2854c",
                "#3b82f6",
                "#dbeafe",
                "白天焦糖黄 → 日落泛冷蓝！",
                [
                    "• 散射主力：r ≈ 1–1.5 μm 氧化铁尘",
                    "• 白昼天空：尘埃吸蓝散红 → 奶油黄",
                    "• 日落反转（好奇号 2015 实拍）：",
                    "  微尘把蓝光聚在太阳旁窄前向锥内！",
                ],
            ),
        ]

        for px_card, p_title, fg_c, bg_c, top_sky, bot_sky, sun_c, swatch_lbl, bullets in planets:
            els.append(card(px_card, 64, 228, 268))
            els.append(pill(px_card + 12, 76, p_title, fg=fg_c, bg=bg_c, w=204, size=11.5))
            # Two-tone sky swatch (upper = daytime/zenith, lower = sunset horizon + sun disk)
            els.append(f'<rect x="{px_card + 14}" y="108" width="200" height="44" rx="6" fill="{top_sky}"/>')
            els.append(f'<rect x="{px_card + 14}" y="144" width="200" height="40" rx="6" fill="{bot_sky}"/>')
            els.append(f'<circle cx="{px_card + 114}" cy="164" r="11" fill="{sun_c}"/>')
            els.append(txt(px_card + 114, 128, swatch_lbl, 11.5, "#ffffff", anchor="middle", weight="700"))
            for b_i, b_txt in enumerate(bullets):
                els.append(txt(px_card + 14, 206 + b_i * 22, b_txt, 11.5, INK if "反转" in b_txt or "实拍" in b_txt else BODY, weight="700" if ("反转" in b_txt or "前向锥" in b_txt) else "400"))

        # Bottom Wide Panel: Computed Forward Diffraction Cone of r = 1.2 um Martian Dust (Blue 450 nm vs Red 670 nm)
        els.append(card(20, 344, 720, 172))
        els.append(pill(34, 356, "C · 火星蓝色日落物理揭秘：1.2 μm 尘埃的米氏近前向散射峰 (θ ∈ [−20°, +20°])", fg=BLUE, bg=BLUE_SOFT, w=476))

        # Exact Airy/Fraunhofer near-forward diffraction intensity pattern (2*J1(x sin theta)/(x sin theta))^2
        # scaled by relative forward amplitude x^2 where x = 2*pi*r/lambda for r = 1.2 um:
        def j1_approx(z):
            if abs(z) < 1e-8:
                return 0.5 * z
            # Exact power series for Bessel J_1(z) (converges to 1e-15 in 14 terms for |z| <= 10)
            term = 0.5 * z
            tot = term
            for m_k in range(1, 16):
                term *= -0.25 * z * z / (m_k * (m_k + 1))
                tot += term
            return tot

        def dust_forward_norm(deg_v, lam_nm):
            r_nm = 1200.0  # 1.2 um dust radius
            x_p = 2.0 * math.pi * r_nm / lam_nm
            u_z = x_p * math.sin(math.radians(abs(deg_v)))
            airy = 1.0 if u_z < 1e-7 else (2.0 * j1_approx(u_z) / u_z) ** 2
            # Relative forward peak intensity scales as (x_p / x_ref)^2, normalized to blue peak = 1.0
            peak_scale = (450.0 / lam_nm) ** 2
            return peak_scale * airy

        dx0, dx1 = 56, 386
        dy_top, dy_bot = 398, 484

        def px_ang(deg_a):
            return dx0 + (deg_a + 20.0) / 40.0 * (dx1 - dx0)

        def py_int(iv):
            return dy_bot - iv * (dy_bot - dy_top)

        els.append(f'<line x1="{dx0}" y1="{dy_bot}" x2="{dx1}" y2="{dy_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{px_ang(0):.1f}" y1="{dy_top}" x2="{px_ang(0):.1f}" y2="{dy_bot}" stroke="{BORDER}" stroke-width="1.0" stroke-dasharray="3 3"/>')
        for a_t in (-20, -10, 0, 10, 20):
            els.append(txt(px_ang(a_t), dy_bot + 15, f"{a_t}°", 11.5, MUTED, anchor="middle", cls="mono"))
        els.append(txt(px_ang(0), dy_bot + 30, "偏离落日圆盘视角 θ", 11.5, INK, anchor="middle", weight="700"))

        angs = [a_i * 0.5 for a_i in range(-40, 41)]
        pts_b = [f"{px_ang(a):.1f},{py_int(dust_forward_norm(a, 450.0)):.1f}" for a in angs]
        pts_r = [f"{px_ang(a):.1f},{py_int(dust_forward_norm(a, 670.0)):.1f}" for a in angs]
        els.append(f'<polyline points="{" ".join(pts_r)}" fill="none" stroke="{ORANGE}" stroke-width="2.3" stroke-dasharray="5 3"/>')
        els.append(f'<polyline points="{" ".join(pts_b)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

        els.append(txt(px_ang(2.8), py_int(0.92), "450nm 蓝：窄锥聚日盘", 11.5, BLUE, weight="700", halo=True))
        els.append(txt(px_ang(5.5), py_int(0.36), "670nm 红：宽角散全天", 11.5, ORANGE, weight="700", halo=True))

        els.append(card(420, 390, 306, 112, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(432, 411, "Lemmon (2015) & Ehlers 等 (2014) 定量解释：", 11.5, INK, weight="700"))
        els.append(txt(432, 432, "• 火星微尘半径 (~1.2 μm) 恰与可见光波长相当；", 11.5, BODY))
        els.append(txt(432, 452, "• 蓝光波长短，前向衍射锥更窄、峰值高逾 2 倍，", 11.5, BLUE, weight="700"))
        els.append(txt(432, 472, "  紧贴落日聚成冷蓝光晕；红黄散向大角度染黄全天！", 11.5, BODY))

        return figure(
            530,
            "月球地球火星三颗星球白昼与日落天空色彩对比及火星微尘米氏前向散射蓝日落原理图解",
            "上图对比月球真空黑空、地球氮氧瑞利散射蓝天红日落与火星1至1.5微米氧化铁微尘焦糖黄天蓝日落；下图精确计算贝塞尔J₁前向散射峰，显示450纳米蓝光在落日视角±5度内前向散射峰比670纳米红光高且窄逾两倍。",
            els,
        )

    @register("sky-blue", "天空为什么是蓝色的五步图解：瑞利四次方偶极散射、紫天悖论与视锥色觉、白云乌云米氏散射、日落与臭氧暮光蓝及火星蓝日落", "mechanics_sky")
    def build_sky_blue():
        write_svg(SUBDIR, "rayleigh-dipole-fourth-power.svg", _build_rayleigh_fourth_power())
        write_svg(SUBDIR, "violet-paradox-cone-vision.svg", _build_violet_paradox_cones())
        write_svg(SUBDIR, "rayleigh-vs-mie-clouds-haze.svg", _build_rayleigh_vs_mie_clouds())
        write_svg(SUBDIR, "sunset-airmass-and-ozone-zenith.svg", _build_sunset_and_ozone_zenith())
        write_svg(SUBDIR, "earth-moon-mars-sky-comparison.svg", _build_planetary_skies())


_register_sky_blue()



# ---------------------------------------------------------------------------
# William Rowan Hamilton: Optics, Dynamics, Quantum Bridge & Quaternions
# ---------------------------------------------------------------------------
def _register_hamilton_optics_physics():
    SUBDIR = "hamilton-optics-physics"

    EXTRA_ARR = (
        f'<marker id="hm-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{BLUE}"/></marker>'
        f'<marker id="hm-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{ORANGE}"/></marker>'
        f'<marker id="hm-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{GREEN}"/></marker>'
        f'<marker id="hm-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{PURPLE}"/></marker>'
        f'<marker id="hm-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{INK}"/></marker>'
    )

    # 1. Conical Refraction & Fresnel Biaxial Wave-Vector Surface (1832)
    def _build_conical_refraction():
        # Real aragonite refractive indices (yellow D-line) for numerical assertion
        nx_ar, ny_ar, nz_ar = 1.5301, 1.6816, 1.6859
        a_ar = nx_ar ** -2 - ny_ar ** -2
        b_ar = ny_ar ** -2 - nz_ar ** -2
        cone_deg = math.degrees(math.atan(ny_ar * ny_ar * math.sqrt(a_ar * b_ar)))
        optic_half_deg = math.degrees(math.atan(math.sqrt(b_ar / a_ar)))
        assert 1.80 < cone_deg < 1.95, f"Unexpected aragonite cone angle {cone_deg}"
        assert 8.5 < optic_half_deg < 9.5, f"Unexpected optic axis half-angle {optic_half_deg}"

        els = header(
            "1832 年纸笔预言“锥形折射”：一束细光射进双轴晶体，为什么炸成空心光环？",
            "左：菲涅耳四次波矢曲面截面与四个圆锥漏斗奇点（非真实比例放大示意）｜右：劳埃德霰石实验与半角偏振旋转",
        )

        # Left Card: Exact kx-kz cross-section of Fresnel wavevector surface
        els.append(card(20, 62, 352, 386))
        els.append(txt(36, 84, "① 双轴晶体波矢曲面 kx–kz 截面（各向异性放大示意）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "圆截叶 r = ny 与椭圆截叶 (nx, nz) 横截相交出 4 个圆锥奇点", 10.6, MUTED))

        cx, cy = 196.0, 212.0
        sc = 50.0
        nx_d, ny_d, nz_d = 1.16, 1.52, 1.86
        sin2_th = (1.0 / ny_d ** 2 - 1.0 / nz_d ** 2) / (1.0 / nx_d ** 2 - 1.0 / nz_d ** 2)
        th_c = math.asin(math.sqrt(sin2_th))

        # Axes
        els.append(f'<line x1="{cx - 118:.1f}" y1="{cy:.1f}" x2="{cx + 118:.1f}" y2="{cy:.1f}" stroke="{HAIRLINE}" stroke-width="1.2"/>')
        els.append(f'<line x1="{cx:.1f}" y1="{cy - 84:.1f}" x2="{cx:.1f}" y2="{cy + 84:.1f}" stroke="{HAIRLINE}" stroke-width="1.2"/>')
        els.append(txt(cx + 116, cy + 14, "kx", 10.5, MUTED, "end"))
        els.append(txt(cx + 8, cy - 74, "kz", 10.5, MUTED))

        # Sheet A: circle radius ny_d * sc
        r_ny = ny_d * sc
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_ny:.1f}" fill="{BLUE}" fill-opacity="0.05" stroke="{BLUE}" stroke-width="2.1"/>')

        # Sheet B: ellipse rx = nz_d * sc, ry = nx_d * sc
        rx_nz = nz_d * sc
        ry_nx = nx_d * sc
        els.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx_nz:.1f}" ry="{ry_nx:.1f}" fill="{ORANGE}" fill-opacity="0.05" stroke="{ORANGE}" stroke-width="2.1"/>')

        # Two optic axes lines + 4 exact conoidal singular points
        for sx in (-1.0, 1.0):
            for sz in (-1.0, 1.0):
                px = cx + sx * r_ny * math.cos(th_c)
                py = cy - sz * r_ny * math.sin(th_c)
                err_el = ((sx * ny_d * math.cos(th_c)) / nz_d) ** 2 + ((sz * ny_d * math.sin(th_c)) / nx_d) ** 2 - 1.0
                assert abs(err_el) < 1e-12
                if sx > 0 and sz > 0:
                    els.append(
                        f'<line x1="{cx - 1.18 * r_ny * math.cos(th_c):.1f}" y1="{cy + 1.18 * r_ny * math.sin(th_c):.1f}" '
                        f'x2="{cx + 1.18 * r_ny * math.cos(th_c):.1f}" y2="{cy - 1.18 * r_ny * math.sin(th_c):.1f}" '
                        f'stroke="{PURPLE}" stroke-width="1.3" stroke-dasharray="4 3"/>'
                    )
                    els.append(
                        f'<line x1="{cx - 1.18 * r_ny * math.cos(th_c):.1f}" y1="{cy - 1.18 * r_ny * math.sin(th_c):.1f}" '
                        f'x2="{cx + 1.18 * r_ny * math.cos(th_c):.1f}" y2="{cy + 1.18 * r_ny * math.sin(th_c):.1f}" '
                        f'stroke="{PURPLE}" stroke-width="1.3" stroke-dasharray="4 3"/>'
                    )
                els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.2" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.5"/>')

        # Tangent plane line across top-right conoidal dimple
        c_x = math.sqrt(ny_d ** 2 - nx_d ** 2)
        c_z = math.sqrt(nz_d ** 2 - ny_d ** 2)
        rhs = ny_d * math.sqrt(nz_d ** 2 - nx_d ** 2)
        kx0 = ny_d * math.cos(th_c)
        t_pts = []
        for dk in (-0.34, 0.34):
            kxv = kx0 + dk
            kzv = (rhs - c_x * kxv) / c_z
            t_pts.append((cx + kxv * sc, cy - kzv * sc))
        els.append(
            f'<line x1="{t_pts[0][0]:.1f}" y1="{t_pts[0][1]:.1f}" x2="{t_pts[1][0]:.1f}" y2="{t_pts[1][1]:.1f}" '
            f'stroke="{GREEN}" stroke-width="2.2"/>'
        )
        els.append(txt(cx + 68, cy - 68, "切平面盖住圆环", 10.4, GREEN, weight="700", halo=True))
        els.append(txt(cx - 88, cy - 58, "光轴 I", 10.3, PURPLE, weight="700", halo=True))
        els.append(txt(cx - 94, cy + 68, "圆叶 r=ny", 10.3, BLUE, weight="600", halo=True))
        els.append(txt(cx + 58, cy + 68, "椭圆叶", 10.3, ORANGE, weight="600", halo=True))

        # Bottom comparison sub-cards inside Left Card: Fresnel's mistake vs Hamilton's funnel
        els.append(card(34, 304, 154, 128, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(111, 322, "菲涅耳误判：平滑相切", 10.6, SLATE, "middle", weight="700"))
        els.append(f'<path d="M 52,374 Q 111,344 170,374" fill="none" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(f'<path d="M 52,344 Q 111,374 170,344" fill="none" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="3 2"/>')
        els.append(f'<line x1="62" y1="359" x2="160" y2="359" stroke="{SLATE}" stroke-width="1.4"/>')
        els.append(txt(111, 398, "若仅1条法线 → 只出1束光", 10.0, MUTED, "middle"))
        els.append(txt(111, 415, "（漏掉了三维方向 ky！）", 10.0, MUTED, "middle"))

        els.append(card(198, 304, 160, 128, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(278, 322, "哈密顿严算：圆锥漏斗坑", 10.6, PURPLE, "middle", weight="700"))
        els.append(f'<ellipse cx="278" cy="350" rx="34" ry="8" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
        els.append(f'<path d="M 244,350 L 278,378 L 312,350" fill="none" stroke="{PURPLE}" stroke-width="2.0"/>')
        els.append(f'<circle cx="278" cy="378" r="3.8" fill="{PURPLE}"/>')
        for dx_n in (-20, -8, 8, 20):
            els.append(f'<line x1="278" y1="378" x2="{278 + dx_n}" y2="334" stroke="{ORANGE}" stroke-width="1.3" marker-end="url(#hm-orange)"/>')
        els.append(txt(278, 398, "尖点拥有一整圈无穷多法线", 10.1, INK, "middle", weight="600"))
        els.append(txt(278, 415, "⇒ 单束光炸成一圈空心光锥！", 10.1, PURPLE, "middle", weight="700"))

        # Right Card: Lloyd's Aragonite Experiment (Dec 14, 1832) + Half-Angle Polarization Ring
        els.append(card(388, 62, 352, 386))
        els.append(txt(404, 84, "② 劳埃德霰石实验（1832.12）与偏振半角旋转", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, f"霰石 n=(1.530, 1.682, 1.686) ⇒ 内锥顶角 {cone_deg:.2f}°（1°52′）", 10.4, MUTED))

        els.append(card(402, 116, 324, 174, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(f'<line x1="414" y1="196" x2="466" y2="196" stroke="{ORANGE}" stroke-width="2.6" marker-end="url(#hm-orange)"/>')
        els.append(txt(440, 182, "单束入射光", 10.2, ORANGE, "middle", weight="700"))
        els.append(f'<line x1="468" y1="150" x2="468" y2="191" stroke="{INK}" stroke-width="3.2"/>')
        els.append(f'<line x1="468" y1="201" x2="468" y2="242" stroke="{INK}" stroke-width="3.2"/>')
        els.append(txt(468, 256, "针孔光阑", 10.0, MUTED, "middle"))

        els.append(f'<rect x="472" y="142" width="96" height="108" rx="4" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.7"/>')
        els.append(txt(520, 159, "霰石晶体 CaCO₃", 10.4, BLUE, "middle", weight="700"))
        els.append(f'<polygon points="472,196 568,172 568,220" fill="{ORANGE}" fill-opacity="0.14"/>')
        els.append(f'<line x1="472" y1="196" x2="568" y2="172" stroke="{ORANGE}" stroke-width="2.1"/>')
        els.append(f'<line x1="472" y1="196" x2="568" y2="220" stroke="{ORANGE}" stroke-width="2.1"/>')
        els.append(f'<ellipse cx="568" cy="196" rx="6" ry="24" fill="none" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="3 2"/>')
        els.append(txt(522, 238, "空心光锥 ~1°52′", 10.2, ORANGE, "middle", weight="700"))

        els.append(f'<rect x="568" y="172" width="88" height="48" fill="{ORANGE}" fill-opacity="0.10"/>')
        els.append(f'<line x1="568" y1="172" x2="656" y2="172" stroke="{ORANGE}" stroke-width="2.1" marker-end="url(#hm-orange)"/>')
        els.append(f'<line x1="568" y1="220" x2="656" y2="220" stroke="{ORANGE}" stroke-width="2.1" marker-end="url(#hm-orange)"/>')
        els.append(txt(612, 162, "平行空心光柱", 10.2, GREEN, "middle", weight="700"))
        els.append(txt(612, 238, "移远屏幕环径不变！", 10.0, GREEN, "middle", weight="600"))

        els.append(f'<polygon points="660,136 714,126 714,256 660,266" fill="#ffffff" stroke="{SLATE}" stroke-width="1.4"/>')
        els.append(f'<ellipse cx="687" cy="196" rx="13" ry="24" fill="none" stroke="{ORANGE}" stroke-width="3.2"/>')
        els.append(f'<circle cx="687" cy="196" r="2.2" fill="{SLATE_SOFT}"/>')
        els.append(txt(687, 279, "银纸亮环", 10.3, INK, "middle", weight="700"))

        els.append(card(402, 302, 324, 130, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(414, 322, "意外彩蛋：绕亮环走 360°，偏振片只转 180°！", 10.7, GREEN, weight="700"))

        rcx, rcy, rr = 452.0, 378.0, 31.0
        els.append(f'<circle cx="{rcx:.1f}" cy="{rcy:.1f}" r="{rr:.1f}" fill="#ffffff" stroke="{ORANGE}" stroke-width="2.6"/>')
        for k in range(8):
            phi = math.radians(90.0 - k * 45.0)
            px = rcx + rr * math.cos(phi)
            py = rcy - rr * math.sin(phi)
            pol_ang = math.radians(90.0 - k * 22.5)
            dx = 7.5 * math.cos(pol_ang)
            dy = -7.5 * math.sin(pol_ang)
            els.append(f'<line x1="{px - dx:.1f}" y1="{py - dy:.1f}" x2="{px + dx:.1f}" y2="{py + dy:.1f}" stroke="{INK}" stroke-width="2.0"/>')
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.2" fill="{ORANGE}"/>')

        els.append(txt(500, 348, "• 环顶（φ=0°）：偏振竖直 ↕", 10.3, BODY))
        els.append(txt(500, 368, "• 环底（φ=180°）：偏振水平 ↔（转 90°）", 10.3, BODY))
        els.append(txt(500, 388, "• 绕环一周 360° ⇒ 偏振仅转 φ/2 = 180°", 10.3, INK, weight="700"))
        els.append(txt(500, 408, "• 现代物理：拓扑“贝里几何相位 π”先声", 10.2, PURPLE, weight="600"))

        return figure(
            464,
            "哈密顿1832年预言双轴晶体锥形折射：菲涅耳波矢曲面圆锥奇点与劳埃德霰石亮环实验",
            "左图展示双轴晶体四次波矢曲面截面在四个光轴方向横截形成的圆锥漏斗奇点，对比菲涅耳误以为的平滑相切与哈密顿发现的无穷多法线圆锥；右图还原1832年12月劳埃德用霰石薄片测得顶角约1度52分的空心光锥与平行空心光柱亮环，并标出沿环旋转360度偏振仅转180度的半角规律。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 2. Characteristic Function V(rA, rB): Wavefronts Orthogonal to Rays + Snell's Law
    def _build_characteristic_function_optics():
        els = header(
            "哈密顿光学特征函数 V(A, B)：只记一笔“光程总账”，自动吐出所有光线与波前",
            "左：渐变折射率介质中实算等光程波前 V = const 与正交弯曲光线｜右：切向梯度连续一步推出斯涅耳折射定律",
        )

        els.append(card(20, 62, 372, 378))
        els.append(txt(36, 84, "① 渐变折射率透镜：光线 p = ∇V 处处垂直于等光程波前", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "中心折射率高 n(y) = 1.60·sech(0.014y)，光程微分 dV = n·ds", 10.5, MUTED))

        ox, oy = 54.0, 224.0
        n0, alpha = 1.60, 0.0135

        def n_val(yv):
            return n0 / math.cosh(alpha * yv)

        def dn_dy(yv):
            sh = math.sinh(alpha * yv)
            ch = math.cosh(alpha * yv)
            return -n0 * alpha * sh / (ch * ch)

        def trace_ray(th0_deg, v_max=430.0, steps=900):
            dv = v_max / steps
            x, y = 0.0, 0.0
            px = n0 * math.cos(math.radians(th0_deg))
            py = n0 * math.sin(math.radians(th0_deg))
            pts = [(0.0, x, y, px, py)]
            for i in range(1, steps + 1):
                def deriv(xv, yv, pxv, pyv):
                    nv = n_val(yv)
                    inv_n2 = 1.0 / (nv * nv)
                    return pxv * inv_n2, pyv * inv_n2, 0.0, dn_dy(yv) / nv

                dx1, dy1, _, dpy1 = deriv(x, y, px, py)
                dx2, dy2, _, dpy2 = deriv(x + 0.5 * dv * dx1, y + 0.5 * dv * dy1, px, py + 0.5 * dv * dpy1)
                dx3, dy3, _, dpy3 = deriv(x + 0.5 * dv * dx2, y + 0.5 * dv * dy2, px, py + 0.5 * dv * dpy2)
                dx4, dy4, _, dpy4 = deriv(x + dv * dx3, y + dv * dy3, px, py + dv * dpy3)
                x += (dv / 6.0) * (dx1 + 2 * dx2 + 2 * dx3 + dx4)
                y += (dv / 6.0) * (dy1 + 2 * dy2 + 2 * dy3 + dy4)
                py += (dv / 6.0) * (dpy1 + 2 * dpy2 + 2 * dpy3 + dpy4)
                pts.append((i * dv, x, y, px, py))
            return pts

        els.append(card(36, 118, 340, 212, rx=8, fill="#f8fafc", stroke=BORDER))
        for band_h, op in ((84, 0.05), (56, 0.07), (28, 0.10)):
            els.append(f'<rect x="38" y="{oy - band_h:.1f}" width="336" height="{2 * band_h:.1f}" fill="{BLUE}" fill-opacity="{op}"/>')
        els.append(f'<line x1="42" y1="{oy:.1f}" x2="370" y2="{oy:.1f}" stroke="{HAIRLINE}" stroke-width="1.1" stroke-dasharray="4 3"/>')

        v_levels = [95.0, 185.0, 275.0, 365.0]
        dense_angles = [-36.0 + 1.5 * k for k in range(49)]
        dense_rays = [trace_ray(a, v_max=415.0, steps=830) for a in dense_angles]
        for idx_v, v_target in enumerate(v_levels):
            step_i = int(round(v_target / (415.0 / 830)))
            wf_pts = []
            for r_pts in dense_rays:
                _, xv, yv, pxv, pyv = r_pts[step_i]
                if ox + xv <= 368.0 and abs(yv) <= 95.0:
                    wf_pts.append((ox + xv, oy - yv, pxv, pyv))
            if len(wf_pts) >= 5:
                mid = len(wf_pts) // 4
                tx_w = wf_pts[mid + 1][0] - wf_pts[mid - 1][0]
                ty_w = -(wf_pts[mid + 1][1] - wf_pts[mid - 1][1])
                px_m, py_m = wf_pts[mid][2], wf_pts[mid][3]
                cos_err = abs(tx_w * px_m + ty_w * py_m) / (math.hypot(tx_w, ty_w) * math.hypot(px_m, py_m))
                assert cos_err < 0.015, f"Wavefront not orthogonal to ray: cos={cos_err}"
            d_wf = "M " + " L ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in wf_pts)
            els.append(f'<path d="{d_wf}" fill="none" stroke="{GREEN}" stroke-width="1.9" stroke-dasharray="5 3"/>')
            top_p = min(wf_pts, key=lambda p: p[1])
            els.append(txt(top_p[0], top_p[1] - 6, f"V{idx_v + 1}", 10.0, GREEN, "middle", weight="700", halo=True))

        for ang in (-33, -22, -11, 0, 11, 22, 33):
            r_pts = trace_ray(ang, v_max=425.0, steps=850)
            clipped = [(ox + p[1], oy - p[2]) for p in r_pts if ox + p[1] <= 366.0]
            d_ray = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in clipped[::6] + [clipped[-1]])
            els.append(f'<path d="{d_ray}" fill="none" stroke="{ORANGE}" stroke-width="1.85"/>')

        r_dn = trace_ray(-22.0, v_max=425.0, steps=850)
        _, x_h, y_h, px_h, py_h = r_dn[int(round(185.0 / 0.5))]
        sx_h, sy_h = ox + x_h, oy - y_h
        un_x, un_y = px_h / math.hypot(px_h, py_h), -py_h / math.hypot(px_h, py_h)
        els.append(f'<circle cx="{sx_h:.1f}" cy="{sy_h:.1f}" r="4.0" fill="{INK}"/>')
        els.append(
            f'<line x1="{sx_h:.1f}" y1="{sy_h:.1f}" x2="{sx_h + 26 * un_x:.1f}" y2="{sy_h + 26 * un_y:.1f}" '
            f'stroke="{INK}" stroke-width="2.1" marker-end="url(#hm-ink)"/>'
        )
        els.append(txt(sx_h + 12, sy_h + 26, "p = ∇V ⊥ 波前", 10.3, INK, weight="700", halo=True))

        els.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="4.8" fill="{BLUE}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(txt(ox + 2, oy + 18, "光源 A", 10.4, BLUE, weight="700", halo=True))
        focus_x = ox + math.pi / alpha
        els.append(f'<circle cx="{focus_x:.1f}" cy="{oy:.1f}" r="4.8" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(txt(focus_x, oy + 20, "自聚焦点 B", 10.4, PURPLE, "middle", weight="700", halo=True))

        els.append(card(36, 340, 340, 86, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(48, 360, "哈密顿核心总账：V(r_A, r_B) = ∫ n(r) ds（真实光程）", 10.8, BLUE, weight="700"))
        els.append(txt(48, 380, "• 终点求梯度得光学动量：p_B = ∇_B V = n(r_B)·u_B", 10.4, BODY))
        els.append(txt(48, 399, "• 两边取模平方得程函方程：|∇V|² = n²(r)（费马=惠更斯！）", 10.4, INK, weight="600"))
        els.append(txt(48, 417, "• 实线橙：光线轨迹；虚线绿：等光程波前，两者处处 90° 正交", 10.1, MUTED))

        # Right Card: Snell's Law from Tangential Continuity of Optical Momentum p = grad V
        els.append(card(408, 62, 332, 378))
        els.append(txt(424, 84, "② 一步秒推折射定律：切向动量 px 守恒", PANEL_TITLE, INK, weight="700"))
        els.append(txt(424, 102, "界面 y=0 两侧波前连续 ⇒ ∂V/∂x 相等 ⇒ n₁sinθ₁ = n₂sinθ₂", 10.5, MUTED))

        n1, n2 = 1.00, 1.50
        th1 = math.radians(45.0)
        th2 = math.asin((n1 / n2) * math.sin(th1))
        assert abs(math.degrees(th2) - 28.1255) < 0.01

        icx, icy = 574.0, 224.0
        sc_p = 66.0

        els.append(card(422, 118, 304, 212, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(f'<rect x="424" y="120" width="300" height="104" fill="#ffffff"/>')
        els.append(f'<rect x="424" y="224" width="300" height="104" fill="{BLUE_SOFT}" fill-opacity="0.65"/>')
        els.append(f'<line x1="428" y1="{icy:.1f}" x2="720" y2="{icy:.1f}" stroke="{INK}" stroke-width="1.8"/>')
        els.append(f'<line x1="{icx:.1f}" y1="126" x2="{icx:.1f}" y2="322" stroke="{SLATE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append(txt(436, 140, "空气 n₁ = 1.00", 10.5, SLATE, weight="700"))
        els.append(txt(436, 316, "玻璃 n₂ = 1.50", 10.5, BLUE, weight="700"))

        r1_px, r2_px = n1 * sc_p, n2 * sc_p
        els.append(f'<circle cx="{icx:.1f}" cy="{icy:.1f}" r="{r1_px:.1f}" fill="none" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="3 3"/>')
        els.append(f'<circle cx="{icx:.1f}" cy="{icy:.1f}" r="{r2_px:.1f}" fill="none" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="4 3"/>')

        in_x, in_y = icx - 74 * math.sin(th1), icy - 74 * math.cos(th1)
        els.append(f'<line x1="{in_x:.1f}" y1="{in_y:.1f}" x2="{icx:.1f}" y2="{icy:.1f}" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#hm-orange)"/>')
        els.append(txt(in_x - 4, in_y + 14, "θ₁ = 45°", 10.3, ORANGE, weight="700", halo=True))

        px_shared = n1 * math.sin(th1) * sc_p
        p1_end = (icx + px_shared, icy + n1 * math.cos(th1) * sc_p)
        p2_end = (icx + px_shared, icy + n2 * math.cos(th2) * sc_p)
        els.append(f'<line x1="{icx:.1f}" y1="{icy:.1f}" x2="{p1_end[0]:.1f}" y2="{p1_end[1]:.1f}" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="3 2" marker-end="url(#hm-orange)"/>')
        els.append(f'<line x1="{icx:.1f}" y1="{icy:.1f}" x2="{p2_end[0]:.1f}" y2="{p2_end[1]:.1f}" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#hm-blue)"/>')

        els.append(f'<line x1="{icx + px_shared:.1f}" y1="{icy:.1f}" x2="{p2_end[0]:.1f}" y2="{p2_end[1]:.1f}" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="3 2"/>')
        els.append(f'<line x1="{icx:.1f}" y1="{icy:.1f}" x2="{icx + px_shared:.1f}" y2="{icy:.1f}" stroke="{GREEN}" stroke-width="2.6"/>')
        els.append(txt(icx + px_shared / 2, icy - 7, "px 相等!", 10.2, GREEN, "middle", weight="700", halo=True))
        els.append(txt(p2_end[0] + 6, p2_end[1] - 14, "|p₂| = n₂ = 1.50", 10.1, BLUE, weight="700", halo=True))
        els.append(txt(p2_end[0] + 6, p2_end[1] + 1, "θ₂ = 28.13°", 10.1, BLUE, weight="600", halo=True))

        els.append(card(422, 340, 304, 86, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(434, 360, "光学哈密顿视角（把 z 当作“演化时间”）：", 10.8, GREEN, weight="700"))
        els.append(txt(434, 380, "• 折射率只随纵深 y 变、不随横向 x 变 ⇒ ∂H/∂x = 0", 10.3, BODY))
        els.append(txt(434, 399, "• 正则方程 dp_x/dy = −∂H/∂x = 0 ⇒ 横向动量 px 守恒！", 10.3, INK, weight="700"))
        els.append(txt(434, 417, "• 即 n₁sinθ₁ = n₂sinθ₂ = 0.7071（对称性直接给出守恒律）", 10.2, MUTED))

        return figure(
            456,
            "哈密顿光学特征函数：渐变折射率等光程波前正交光线与切向光学动量守恒推导斯涅耳定律",
            "左图通过四阶龙格库塔法精确积分双曲正割渐变折射率介质中的光线与等光程波前V=常数，验证光学动量p=∇V处处垂直于波前并实现自聚焦；右图展示界面横向平移不变导致光学动量横分量px守恒，一步推出n1 sinθ1 = n2 sinθ2。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 3. Canonical Phase Space & Liouville's Theorem (Animated + Static)
    def _build_phase_space_liouville():
        def rk4_pend(q0, p0, t_end, gamma=0.0, steps=240):
            dt = t_end / steps
            q, p = q0, p0
            for _ in range(steps):
                dq1, dp1 = p, -math.sin(q) - gamma * p
                dq2, dp2 = p + 0.5 * dt * dp1, -math.sin(q + 0.5 * dt * dq1) - gamma * (p + 0.5 * dt * dp1)
                dq3, dp3 = p + 0.5 * dt * dp2, -math.sin(q + 0.5 * dt * dq2) - gamma * (p + 0.5 * dt * dp2)
                dq4, dp4 = p + dt * dp3, -math.sin(q + dt * dq3) - gamma * (p + dt * dp3)
                q += (dt / 6.0) * (dq1 + 2 * dq2 + 2 * dq3 + dq4)
                p += (dt / 6.0) * (dp1 + 2 * dp2 + 2 * dp3 + dp4)
            return q, p

        def poly_area(pts):
            s = 0.0
            n = len(pts)
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                s += x1 * y2 - x2 * y1
            return 0.5 * abs(s)

        qc0, pc0, rad0 = -1.48, 0.92, 0.34
        n_b = 240
        blob_t0 = [(qc0 + rad0 * math.cos(2 * math.pi * k / n_b), pc0 + rad0 * math.sin(2 * math.pi * k / n_b)) for k in range(n_b)]
        blob_t1 = [rk4_pend(q, p, 1.35, gamma=0.0) for q, p in blob_t0]
        blob_t2 = [rk4_pend(q, p, 2.70, gamma=0.0) for q, p in blob_t0]

        area0 = poly_area(blob_t0)
        area1 = poly_area(blob_t1)
        area2 = poly_area(blob_t2)
        assert abs(area1 - area0) / area0 < 5e-4, f"Liouville area drift t1: {area0} -> {area1}"
        assert abs(area2 - area0) / area0 < 5e-4, f"Liouville area drift t2: {area0} -> {area2}"

        gamma_d = 0.45
        damped_t1 = [rk4_pend(q, p, 1.50, gamma=gamma_d) for q, p in blob_t0]
        damped_t2 = [rk4_pend(q, p, 3.20, gamma=gamma_d) for q, p in blob_t0]
        ratio_d2 = poly_area(damped_t2) / area0
        assert abs(ratio_d2 - math.exp(-gamma_d * 3.20)) < 0.005

        anim_css = """
      .lv-flow {
        stroke-dasharray: 260;
        stroke-dashoffset: 260;
        animation: lvDraw 3.2s ease-in-out 0.3s 1 forwards;
      }
      .lv-mid {
        opacity: 0.25;
        animation: lvShowMid 3.2s ease-out 0.3s 1 forwards;
      }
      .lv-end {
        opacity: 0.25;
        animation: lvShowEnd 3.2s ease-out 0.3s 1 forwards;
      }
      @keyframes lvDraw {
        0% { stroke-dashoffset: 260; }
        100% { stroke-dashoffset: 0; }
      }
      @keyframes lvShowMid {
        0%, 35% { opacity: 0.25; }
        55%, 100% { opacity: 1; }
      }
      @keyframes lvShowEnd {
        0%, 72% { opacity: 0.25; }
        95%, 100% { opacity: 1; }
      }
      @media (prefers-reduced-motion: reduce) {
        .lv-flow { animation: none; stroke-dashoffset: 0; }
        .lv-mid, .lv-end { animation: none; opacity: 1; }
      }"""

        els = header(
            "哈密顿相空间 (q, p) 与刘维尔定理：状态云被拉成弯月，面积却一分不少！",
            "左：无耗散非线性单摆 H = p²/2 + (1−cos q) 的保面积辛流｜右：有阻尼耗散收缩对比与正则方程反对称奥秘",
        )

        els.append(card(20, 62, 412, 396))
        els.append(txt(36, 84, "① 保守哈密顿流（∇·v = 0）：形状剧烈扭曲，面积严格守恒", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, f"实算 240 边形相体积：A(0) = {area0:.4f}，A(1.35) = {area1:.4f}，A(2.70) = {area2:.4f}", 10.4, MUTED))

        gx0, gy0, gw, gh = 52.0, 120.0, 362.0, 232.0
        q_min, q_max = -math.pi, math.pi
        p_min, p_max = -2.35, 2.35

        def mp(qv, pv):
            return gx0 + ((qv - q_min) / (q_max - q_min)) * gw, gy0 + ((p_max - pv) / (p_max - p_min)) * gh

        els.append(f'<rect x="{gx0:.1f}" y="{gy0:.1f}" width="{gw:.1f}" height="{gh:.1f}" rx="6" fill="#f8fafc" stroke="{BORDER}"/>')
        zx, zy = mp(0.0, 0.0)
        els.append(f'<line x1="{gx0:.1f}" y1="{zy:.1f}" x2="{gx0 + gw:.1f}" y2="{zy:.1f}" stroke="{HAIRLINE}" stroke-width="1.2"/>')
        els.append(f'<line x1="{zx:.1f}" y1="{gy0:.1f}" x2="{zx:.1f}" y2="{gy0 + gh:.1f}" stroke="{HAIRLINE}" stroke-width="1.2"/>')
        els.append(txt(gx0 + gw - 6, zy - 7, "位置 q (rad)", 10.0, MUTED, "end", halo=True))
        els.append(txt(zx - 6, gy0 + 14, "动量 p", 10.0, MUTED, "end", halo=True))

        for e_lvl in (0.35, 0.90, 1.50):
            q_max_e = math.acos(1.0 - e_lvl)
            pts_up = []
            pts_dn = []
            for k in range(61):
                qv = -q_max_e + (2 * q_max_e * k) / 60.0
                pv = math.sqrt(max(0.0, 2.0 * (e_lvl - (1.0 - math.cos(qv)))))
                pts_up.append(mp(qv, pv))
                pts_dn.append(mp(qv, -pv))
            loop = pts_up + list(reversed(pts_dn))
            d_loop = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in loop) + " Z"
            els.append(f'<path d="{d_loop}" fill="none" stroke="#cbd5e1" stroke-width="1.1"/>')

        for sgn in (1.0, -1.0):
            sep_pts = [mp(-math.pi + (2 * math.pi * k) / 80.0, sgn * 2.0 * math.cos((-math.pi + (2 * math.pi * k) / 80.0) / 2.0)) for k in range(81)]
            d_sep = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in sep_pts)
            els.append(f'<path d="{d_sep}" fill="none" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(txt(gx0 + 10, gy0 + 22, "分界线 E=2", 9.9, SLATE))

        for sample_idx in (0, 60, 120, 180):
            q_s, p_s = blob_t0[sample_idx]
            tr = [mp(q_s, p_s)]
            for st in range(1, 55):
                qt, pt = rk4_pend(q_s, p_s, 2.70 * st / 54.0, gamma=0.0, steps=40)
                tr.append(mp(qt, pt))
            d_tr = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in tr)
            els.append(f'<path class="lv-flow" d="{d_tr}" fill="none" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="3 2" opacity="0.75"/>')

        def blob_svg(b_pts, stroke_c, fill_c, cls_name=""):
            scr = [mp(q, p) for q, p in b_pts[::3]]
            d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in scr) + " Z"
            c_attr = f' class="{cls_name}"' if cls_name else ""
            return f'<path{c_attr} d="{d}" fill="{fill_c}" fill-opacity="0.32" stroke="{stroke_c}" stroke-width="2.1"/>'

        els.append(blob_svg(blob_t0, BLUE, BLUE))
        els.append(blob_svg(blob_t1, ORANGE, ORANGE, "lv-mid"))
        els.append(blob_svg(blob_t2, GREEN, GREEN, "lv-end"))

        x0_l, y0_l = mp(qc0 - 0.15, pc0 + 0.50)
        els.append(txt(x0_l, y0_l, "t = 0 初态圆团", 10.3, BLUE, "middle", weight="700", halo=True))
        x1_l, y1_l = mp(0.88, 1.88)
        els.append(txt(x1_l, y1_l, "t = 1.35 剪切椭圆", 10.3, ORANGE, "middle", weight="700", halo=True))
        x2_l, y2_l = mp(1.38, -0.78)
        els.append(txt(x2_l, y2_l, "t = 2.70 细弯月（面积不变）", 10.3, GREEN, "middle", weight="700", halo=True))

        els.append(card(36, 362, 380, 82, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(46, 382, "为什么面积分毫不差？看正则方程一正一负的偏导抵消：", 10.5, GREEN, weight="700"))
        els.append(txt(46, 402, "q̇=+∂H/∂p, ṗ=−∂H/∂q  ⇒  ∂q̇/∂q + ∂ṗ/∂p = ∂²H/∂q∂p − ∂²H/∂p∂q = 0", 9.8, INK, weight="700"))
        els.append(txt(46, 422, "相空间流体像“不可压缩理想流体”——统计力学系综与保辛算法的根基！", 10.0, BODY))

        # Right Card: Damped Contraction Contrast + Legendre Transform Comparison
        els.append(card(448, 62, 292, 396))
        els.append(txt(464, 84, "② 反例：一旦加入摩擦耗散", PANEL_TITLE, INK, weight="700"))
        els.append(txt(464, 102, f"阻尼 γ=0.45 ⇒ 散度 = −γ < 0，面积收缩至 {ratio_d2 * 100:.0f}%", 10.4, MUTED))

        dx0, dy0, dw, dh = 464.0, 118.0, 260.0, 152.0
        els.append(f'<rect x="{dx0:.1f}" y="{dy0:.1f}" width="{dw:.1f}" height="{dh:.1f}" rx="6" fill="#f8fafc" stroke="{BORDER}"/>')

        def mpd(qv, pv):
            return dx0 + ((qv + 2.4) / 4.8) * dw, dy0 + ((1.8 - pv) / 3.6) * dh

        dzx, dzy = mpd(0.0, 0.0)
        els.append(f'<line x1="{dx0:.1f}" y1="{dzy:.1f}" x2="{dx0 + dw:.1f}" y2="{dzy:.1f}" stroke="{HAIRLINE}" stroke-width="1.1"/>')
        els.append(f'<line x1="{dzx:.1f}" y1="{dy0:.1f}" x2="{dzx:.1f}" y2="{dy0 + dh:.1f}" stroke="{HAIRLINE}" stroke-width="1.1"/>')

        sp = [mpd(qc0, pc0)]
        for st in range(1, 90):
            qt, pt = rk4_pend(qc0, pc0, 5.5 * st / 89.0, gamma=gamma_d, steps=45)
            sp.append(mpd(qt, pt))
        els.append(f'<path d="{"M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in sp)}" fill="none" stroke="{PURPLE}" stroke-width="1.5" stroke-dasharray="3 2"/>')

        for b_pts, col in ((blob_t0, BLUE), (damped_t1, ORANGE), (damped_t2, PURPLE)):
            scr = [mpd(q, p) for q, p in b_pts[::3]]
            els.append(f'<path d="{"M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in scr) + " Z"}" fill="{col}" fill-opacity="0.30" stroke="{col}" stroke-width="1.8"/>')

        els.append(txt(dx0 + 10, dy0 + 18, "A₀ (100%)", 10.0, BLUE, weight="700"))
        els.append(txt(dx0 + dw - 10, dy0 + 22, "t=1.5 (51%)", 10.0, ORANGE, "end", weight="700"))
        els.append(txt(dx0 + dw - 14, dy0 + dh - 14, f"t=3.2 ({ratio_d2 * 100:.0f}%) 缩向吸引子", 10.0, PURPLE, "end", weight="700"))

        els.append(card(464, 282, 260, 162, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(476, 302, "勒让德变换：从拉格朗日升维到哈密顿", 10.7, BLUE, weight="700"))
        els.append(txt(476, 323, "• 拉格朗日 L(q, q̇) = T − U", 10.3, BODY))
        els.append(txt(486, 340, "n 个二阶方程，速度 q̇ 只是位置附庸", 10.0, MUTED))
        els.append(txt(476, 362, "• 定义正则动量：p = ∂L/∂q̇", 10.3, INK, weight="600"))
        els.append(txt(476, 382, "• 哈密顿量：H(q, p) = p·q̇ − L (= T + U)", 10.3, BLUE, weight="700"))
        els.append(txt(486, 400, "2n 个一阶对称方程，q 与 p 平起平坐", 10.1, BODY))
        els.append(txt(486, 418, "坐标变换升级为自由度翻倍的“正则变换”！", 10.1, GREEN, weight="600"))

        return figure(
            474,
            "哈密顿相空间刘维尔定理单次动画与耗散系统面积收缩对比",
            "左图通过精确数值积分展示无耗散非线性单摆相空间中一团圆形初态在t=0、1.35、2.70时刻被剪切拉长成弯月但面积严格保持0.3626不变（刘维尔定理）；右图对比阻尼单摆相面积按指数收缩至24%，并总结勒让德变换H=pq̇-L的结构升级。",
            els,
            extra_css=anim_css,
        )

    # 4. Optico-Mechanical Analogy -> 1926 Schrödinger Wave Mechanics Bridge
    def _build_optico_mechanical_quantum():
        els = header(
            "跨越 95 年的神级伏笔：哈密顿“光学—力学类比”怎样直接引出薛定谔方程？",
            "1831 年哈密顿把质点运动写成等作用量波前；1926 年薛定谔只需补上普朗克常数 ℏ，波动力学应运而生！",
        )

        cols = [
            (
                20,
                "① 几何光学（短波极限 λ→0）",
                BLUE,
                BLUE_SOFT,
                [
                    ("变分原理", "费马原理 δ∫ n ds = 0"),
                    ("主函数", "光程函数 V(r)"),
                    ("波前方程", "程函方程 |∇V|² = n²(r)"),
                    ("几何图景", "光线 p=∇V ⊥ 等相波前"),
                ],
            ),
            (
                268,
                "② 哈密顿—雅可比经典力学",
                ORANGE,
                ORANGE_SOFT,
                [
                    ("变分原理", "驻定作用量 δ∫ L dt = 0"),
                    ("主函数", "作用量主函数 S(q, t)"),
                    ("波前方程", "−∂S/∂t = |∇S|²/(2m) + U"),
                    ("几何图景", "轨迹 p=∇S ⊥ 等作用量面"),
                ],
            ),
            (
                516,
                "③ 薛定谔波动力学（1926）",
                PURPLE,
                PURPLE_SOFT,
                [
                    ("相位钥匙", "ψ = A · exp(i S / ℏ)"),
                    ("核心算符", "Ĥ = −(ℏ²/2m)∇² + U(q)"),
                    ("波动方程", "iℏ ∂ψ/∂t = Ĥ ψ（线性）"),
                    ("经典极限", "ℏ→0 退回 ② H–J 方程"),
                ],
            ),
        ]
        for x0, title_s, fg, bg, rows in cols:
            els.append(card(x0, 62, 224, 174, rx=10, fill=CARD_BG, stroke=fg, sw=1.5))
            els.append(f'<rect x="{x0 + 1}" y="63" width="222" height="28" rx="9" fill="{bg}"/>')
            els.append(txt(x0 + 112, 82, title_s, 11.4, fg, "middle", weight="700"))
            for r_i, (k_lbl, v_lbl) in enumerate(rows):
                ry = 110 + r_i * 31
                els.append(pill(x0 + 8, ry - 12, k_lbl, fg=fg, bg=bg, w=58, h=19, size=9.6))
                els.append(txt(x0 + 72, ry + 2, v_lbl, 10.0, INK, weight="600" if r_i == 2 else "400"))

        els.append(f'<line x1="246" y1="149" x2="266" y2="149" stroke="{ORANGE}" stroke-width="2.0" marker-end="url(#hm-orange)"/>')
        els.append(f'<line x1="494" y1="149" x2="514" y2="149" stroke="{PURPLE}" stroke-width="2.0" marker-end="url(#hm-purple)"/>')

        els.append(card(20, 250, 352, 202))
        els.append(txt(36, 272, "④ 经典极限（ℏ → 0）：势垒前硬折返，禁区绝对为零", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 290, "能量 E < U₀ 时 p = √[2m(E−U)] 变虚数，经典粒子撞上转折点 x_t", 10.4, MUTED))

        bx0, by0, bw, bh = 38.0, 304.0, 316.0, 132.0
        els.append(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="6" fill="#f8fafc" stroke="{BORDER}"/>')

        def map_bx(xv, yv):
            return bx0 + (xv / 10.0) * bw, by0 + bh - (yv / 1.35) * (bh - 14.0) - 6.0

        u_pts = [map_bx(10.0 * k / 100.0, 1.0 / (1.0 + math.exp(-(10.0 * k / 100.0 - 6.2) / 0.45))) for k in range(101)]
        poly_u = [map_bx(0.0, 0.0)] + u_pts + [map_bx(10.0, 0.0)]
        els.append(f'<path d="{"M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in poly_u) + " Z"}" fill="{SLATE_SOFT}" stroke="none"/>')
        els.append(f'<path d="{"M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in u_pts)}" fill="none" stroke="{SLATE}" stroke-width="2.0"/>')

        e_val = 0.72
        xt = 6.2 + 0.45 * math.log(e_val / (1.0 - e_val))
        ex0, ey = map_bx(0.2, e_val)
        ext, _ = map_bx(xt, e_val)
        els.append(f'<line x1="{ex0:.1f}" y1="{ey:.1f}" x2="{ext:.1f}" y2="{ey:.1f}" stroke="{ORANGE}" stroke-width="2.4" marker-end="url(#hm-orange)"/>')
        els.append(f'<circle cx="{ext:.1f}" cy="{ey:.1f}" r="4.6" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.4"/>')
        s_acc = 0.0
        next_s = 0.35
        for k in range(1, 200):
            xk = xt * k / 200.0
            uk = 1.0 / (1.0 + math.exp(-(xk - 6.2) / 0.45))
            if e_val > uk:
                s_acc += math.sqrt(e_val - uk) * (xt / 200.0)
                if s_acc >= next_s:
                    wx, _ = map_bx(xk, e_val)
                    els.append(f'<line x1="{wx:.1f}" y1="{ey - 20:.1f}" x2="{wx:.1f}" y2="{ey + 20:.1f}" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="3 2"/>')
                    next_s += 0.58
        els.append(txt(bx0 + 12, ey - 26, "等作用量波前 S = const", 10.1, BLUE, weight="700"))
        els.append(txt(ext - 6, ey + 24, "经典转折点 x_t", 10.1, ORANGE, "end", weight="700"))
        els.append(txt(bx0 + bw - 12, ey - 6, "经典禁区", 10.3, SLATE, "end", weight="700"))
        els.append(txt(bx0 + bw - 12, ey + 12, "(概率 = 0)", 10.0, MUTED, "end"))

        els.append(card(388, 250, 352, 202))
        els.append(txt(404, 272, "⑤ 波动真身（有限 ℏ）：驻波干涉 + 指数隧穿尾巴！", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 290, "实算薛定谔本征波函数 ψ(x)：正如光的全反射倏逝波渗入禁区", 10.4, MUTED))

        qx0, qy0, qw, qh = 406.0, 304.0, 316.0, 132.0
        els.append(f'<rect x="{qx0:.1f}" y="{qy0:.1f}" width="{qw:.1f}" height="{qh:.1f}" rx="6" fill="#f8fafc" stroke="{BORDER}"/>')

        def map_qx(xv, yv):
            return qx0 + (xv / 10.0) * qw, qy0 + qh - (yv / 1.35) * (qh - 14.0) - 6.0

        qu_pts = [map_qx(10.0 * k / 100.0, 1.0 / (1.0 + math.exp(-(10.0 * k / 100.0 - 6.2) / 0.45))) for k in range(101)]
        qpoly_u = [map_qx(0.0, 0.0)] + qu_pts + [map_qx(10.0, 0.0)]
        els.append(f'<path d="{"M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in qpoly_u) + " Z"}" fill="{PURPLE_SOFT}" fill-opacity="0.55" stroke="none"/>')
        els.append(f'<path d="{"M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in qu_pts)}" fill="none" stroke="{SLATE}" stroke-width="1.8"/>')

        c_qm = 15.0
        n_q = 500
        dx_q = 10.0 / n_q
        kap_r = math.sqrt(c_qm * (1.0 - e_val))
        psi_arr = [0.0] * (n_q + 1)
        psi_arr[n_q] = 1e-4
        psi_arr[n_q - 1] = 1e-4 * math.exp(kap_r * dx_q)
        for i in range(n_q - 1, 0, -1):
            xi = i * dx_q
            ui = 1.0 / (1.0 + math.exp(-(xi - 6.2) / 0.45))
            fi = c_qm * (ui - e_val)
            psi_arr[i - 1] = (2.0 + fi * dx_q * dx_q) * psi_arr[i] - psi_arr[i + 1]
        max_psi = max(abs(v) for v in psi_arr)
        psi_pts = [map_qx(i * dx_q, e_val + 0.34 * (psi_arr[i] / max_psi)) for i in range(0, n_q + 1, 2)]
        q_ext, q_ey = map_qx(xt, e_val)
        els.append(f'<line x1="{qx0 + 4:.1f}" y1="{q_ey:.1f}" x2="{qx0 + qw - 4:.1f}" y2="{q_ey:.1f}" stroke="{HAIRLINE}" stroke-width="1.1" stroke-dasharray="3 3"/>')
        els.append(f'<line x1="{q_ext:.1f}" y1="{qy0 + 8:.1f}" x2="{q_ext:.1f}" y2="{qy0 + qh - 8:.1f}" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(f'<path d="{"M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in psi_pts)}" fill="none" stroke="{PURPLE}" stroke-width="2.2"/>')
        els.append(txt(qx0 + 12, qy0 + 20, "振荡物质波 ψ(x)", 10.2, PURPLE, weight="700", halo=True))
        els.append(txt(q_ext + 8, q_ey - 22, "量子隧穿指数尾", 10.2, GREEN, weight="700", halo=True))
        els.append(txt(q_ext + 8, q_ey - 7, "exp(−|p|x / ℏ)", 10.0, GREEN, halo=True))

        return figure(
            466,
            "哈密顿光学—力学类比通往1926年薛定谔波动力学：三层对偶与量子势垒隧穿实算对比",
            "上半部分三栏对照几何光学程函方程、哈密顿—雅可比经典力学方程与1926年薛定谔波动力学方程的精确同构；下半部分对比光滑势垒前经典转折点硬反射与实算一维薛定谔波函数的驻波振荡及禁区指数隧穿尾。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 5. Broom Bridge Quaternions (1843) -> Vector Calculus (nabla) & Gimbal-Lock-Free 3D Rotation
    def _build_quaternions_and_vectors():
        def q_mul(a, b):
            w1, x1, y1, z1 = a
            w2, x2, y2, z2 = b
            return (
                w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
            )

        s3 = 1.0 / math.sqrt(3.0)
        ang_test = math.radians(120.0)
        q_rot = (math.cos(ang_test / 2), s3 * math.sin(ang_test / 2), s3 * math.sin(ang_test / 2), s3 * math.sin(ang_test / 2))
        q_conj = (q_rot[0], -q_rot[1], -q_rot[2], -q_rot[3])
        v_rot = q_mul(q_mul(q_rot, (0.0, 1.0, 0.0, 0.0)), q_conj)
        assert abs(v_rot[0]) < 1e-12 and abs(v_rot[1]) < 1e-12 and abs(v_rot[2] - 1.0) < 1e-12 and abs(v_rot[3]) < 1e-12

        els = header(
            "1843 布鲁姆桥头那一刀：砍掉交换律生出四元数，无心插柳孕育向量分析与三维旋转引擎",
            "上：i² = j² = k² = ijk = −1 非交换循环与 ∇ 向量算子｜下：欧拉角 90° 万向节死锁 vs 单位四元数无奇点旋转",
        )

        els.append(card(20, 62, 352, 186))
        els.append(txt(36, 84, "① 1843.10.16 布鲁姆桥石刻：放弃 ab = ba！", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "实数可除代数仅存 1、2、4 维（无 3 维！）⇒ 升入四维 ℍ", 10.4, MUTED))

        els.append(card(34, 116, 166, 116, rx=8, fill="#f1f5f9", stroke=SLATE, sw=1.5))
        els.append(txt(117, 136, "都柏林·皇家运河桥头", 10.2, MUTED, "middle", weight="600"))
        els.append(txt(117, 160, "i² = j² = k²", 13.0, INK, "middle", weight="700", cls="mono"))
        els.append(txt(117, 180, "= i j k = −1", 13.0, PURPLE, "middle", weight="700", cls="mono"))
        els.append(txt(117, 203, "顺乘为正：ij = +k", 10.2, GREEN, "middle", weight="700"))
        els.append(txt(117, 219, "逆乘反号：ji = −k", 10.2, ORANGE, "middle", weight="700"))

        wcx, wcy, wr = 286.0, 174.0, 44.0
        els.append(f'<circle cx="{wcx:.1f}" cy="{wcy:.1f}" r="{wr:.1f}" fill="none" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="5 3"/>')
        nodes = [(90, "i", BLUE, BLUE_SOFT), (-30, "j", ORANGE, ORANGE_SOFT), (210, "k", PURPLE, PURPLE_SOFT)]
        for ang_deg, sym, fg, bg in nodes:
            ar = math.radians(ang_deg)
            nx_p = wcx + wr * math.cos(ar)
            ny_p = wcy - wr * math.sin(ar)
            els.append(f'<circle cx="{nx_p:.1f}" cy="{ny_p:.1f}" r="14" fill="{bg}" stroke="{fg}" stroke-width="1.8"/>')
            els.append(txt(nx_p, ny_p + 4, sym, 12.6, fg, "middle", weight="700", cls="mono"))
        els.append(txt(wcx + 42, wcy - 28, "顺 +", 10.2, GREEN, weight="700"))
        els.append(txt(wcx - 64, wcy - 28, "逆 −", 10.2, ORANGE, weight="700"))
        els.append(txt(wcx, wcy + 5, "非交换环", 9.8, MUTED, "middle"))

        els.append(card(388, 62, 352, 186))
        els.append(txt(404, 84, "② 拆开四元数乘法：现代向量分析与 ∇ 算子诞生", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "哈密顿亲手造词：标量 Scalar、向量 Vector、张量 Tensor", 10.4, MUTED))

        els.append(card(402, 116, 324, 56, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(414, 136, "纯虚四元数相乘： u · v  =  −(u · v)  +  (u × v)", 11.2, INK, weight="700"))
        els.append(txt(414, 157, "标量部 = 负点积（功/通量） ｜ 向量部 = 叉积（力矩/洛伦兹力）", 10.2, BLUE, weight="600"))

        els.append(card(402, 180, 324, 54, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(414, 199, "哈密顿算子 ∇ = i ∂/∂x + j ∂/∂y + k ∂/∂z（形似腓尼基竖琴）", 10.6, GREEN, weight="700"))
        els.append(txt(414, 220, "梯度 ∇f  ｜  散度 ∇·E = ρ/ε₀  ｜  旋度 ∇×B （麦克斯韦方程组灵魂）", 10.1, BODY))

        els.append(card(20, 260, 352, 202))
        els.append(txt(36, 282, "③ 欧拉角死穴：俯仰 90° 触发“万向节死锁”", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 300, "外环（偏航 Yaw）与内环（滚转 Roll）共面重合，痛失 1 个自由度！", 10.3, MUTED))

        gcx, gcy = 114.0, 376.0
        els.append(f'<ellipse cx="{gcx:.1f}" cy="{gcy:.1f}" rx="64" ry="26" fill="none" stroke="{ORANGE}" stroke-width="3.0"/>')
        els.append(f'<ellipse cx="{gcx:.1f}" cy="{gcy:.1f}" rx="42" ry="17" fill="none" stroke="{ORANGE}" stroke-width="2.4" stroke-dasharray="5 3"/>')
        els.append(f'<ellipse cx="{gcx:.1f}" cy="{gcy:.1f}" rx="18" ry="52" fill="none" stroke="{SLATE}" stroke-width="1.8"/>')
        els.append(f'<line x1="{gcx:.1f}" y1="{gcy + 58:.1f}" x2="{gcx:.1f}" y2="{gcy - 60:.1f}" stroke="#dc2626" stroke-width="2.2" marker-end="url(#hm-orange)"/>')
        els.append(txt(gcx, gcy + 70, "两轴共线锁死！", 10.2, "#dc2626", "middle", weight="700"))

        els.append(txt(196, 334, "• 正常态：三枚环轴两两正交", 10.3, BODY))
        els.append(txt(196, 355, "• 死锁态（Pitch = ±90°）：", 10.3, ORANGE, weight="700"))
        els.append(txt(204, 373, "转外环与转内环产生完全相同旋转，", 10.1, BODY))
        els.append(txt(204, 390, "横向抬头自由度瞬间清零！", 10.1, BODY))
        els.append(txt(196, 414, "• 阿波罗 11 号与早期动画相机", 10.1, MUTED))
        els.append(txt(204, 430, "都曾专门防范万向节死锁报警。", 10.1, MUTED))

        els.append(card(388, 260, 352, 202))
        els.append(txt(404, 282, "④ 王者归来：四元数三明治旋转 v′ = q v q⁻¹", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 300, "q = cos(α/2) + u·sin(α/2)：零死锁、4 数紧凑、球面匀速插值 SLERP", 10.2, MUTED))

        scx, scy, sr = 462.0, 376.0, 50.0
        els.append(f'<circle cx="{scx:.1f}" cy="{scy:.1f}" r="{sr:.1f}" fill="{BLUE_SOFT}" fill-opacity="0.55" stroke="{BLUE}" stroke-width="1.6"/>')
        els.append(f'<ellipse cx="{scx:.1f}" cy="{scy:.1f}" rx="{sr:.1f}" ry="16" fill="none" stroke="{BLUE_LINE}" stroke-width="1.1" stroke-dasharray="3 3"/>')

        els.append(f'<line x1="{scx - 22:.1f}" y1="{scy + 34:.1f}" x2="{scx + 24:.1f}" y2="{scy - 44:.1f}" stroke="{GREEN}" stroke-width="2.1" marker-end="url(#hm-green)"/>')
        els.append(txt(scx + 18, scy - 52, "转轴 u", 10.0, GREEN, "middle", weight="700", halo=True))
        vx1, vy1 = scx - 40, scy - 8
        vx2, vy2 = scx + 34, scy + 18
        els.append(f'<line x1="{scx:.1f}" y1="{scy:.1f}" x2="{vx1:.1f}" y2="{vy1:.1f}" stroke="{SLATE}" stroke-width="1.8" stroke-dasharray="3 2"/>')
        els.append(f'<line x1="{scx:.1f}" y1="{scy:.1f}" x2="{vx2:.1f}" y2="{vy2:.1f}" stroke="{PURPLE}" stroke-width="2.3" marker-end="url(#hm-purple)"/>')
        els.append(f'<path d="M {vx1:.1f},{vy1:.1f} Q {scx + 4:.1f},{scy - 34:.1f} {vx2:.1f},{vy2:.1f}" fill="none" stroke="{PURPLE}" stroke-width="2.0" marker-end="url(#hm-purple)"/>')
        els.append(f'<circle cx="{vx1:.1f}" cy="{vy1:.1f}" r="3.6" fill="{SLATE}"/>')
        els.append(f'<circle cx="{vx2:.1f}" cy="{vy2:.1f}" r="4.0" fill="{PURPLE}"/>')
        els.append(txt(vx1 - 4, vy1 - 8, "v", 10.4, SLATE, "end", weight="700"))
        els.append(txt(vx2 + 6, vy2 + 4, "v′", 10.4, PURPLE, weight="700"))
        els.append(txt(scx, scy + 68, "SLERP 大圆平滑插值", 10.1, BLUE, "middle", weight="700"))

        els.append(txt(546, 330, "• 为什么乘半角 α/2？", 10.3, INK, weight="700"))
        els.append(txt(554, 348, "左乘 q、右乘 q⁻¹ 各转 α/2，", 10.0, BODY))
        els.append(txt(554, 364, "抵消四维分量、净转恰好 α！", 10.0, BODY))
        els.append(txt(546, 386, "• 飞船姿态、机械臂、Unity/UE", 10.1, GREEN, weight="700"))
        els.append(txt(554, 402, "三维引擎底层旋转标配。", 10.0, BODY))
        els.append(card(546, 412, 180, 38, rx=6, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(554, 428, "图论彩蛋：1856 二十面体棋", 10.0, PURPLE, weight="700"))
        els.append(txt(554, 443, "开创“哈密顿回路”遍历难题！", 9.8, BODY))

        return figure(
            476,
            "1843年哈密顿布鲁姆桥发明四元数：非交换乘法环、向量分析∇算子与免万向节死锁三维旋转",
            "左上展示1843年10月16日布鲁姆桥石刻公式与i、j、k顺正逆负的非交换循环；右上说明四元数乘法如何拆出标量点积、向量叉积及哈密顿算子∇；左下与右下对比欧拉角在俯仰90度时的万向节死锁与单位四元数v'=qvq^-1在三维空间无奇点SLERP球面插值旋转及1856年哈密顿回路。",
            els,
            extra_defs=EXTRA_ARR,
        )

    @register("hamilton-optics-physics", "哈密顿光学与数学物理：双轴晶体锥形折射、光程特征函数、相空间刘维尔定理、薛定谔量子桥与四元数旋转", "mechanics_sky")
    def build_hamilton_optics_physics():
        write_svg(SUBDIR, "conical-refraction-wave-surface.svg", _build_conical_refraction())
        write_svg(SUBDIR, "characteristic-function-wavefront-rays.svg", _build_characteristic_function_optics())
        write_svg(SUBDIR, "phase-space-liouville-flow-anim.svg", _build_phase_space_liouville())
        write_svg(SUBDIR, "optico-mechanical-schrodinger-bridge.svg", _build_optico_mechanical_quantum())
        write_svg(SUBDIR, "broom-bridge-quaternions-to-vectors.svg", _build_quaternions_and_vectors())


_register_hamilton_optics_physics()


# ---------------------------------------------------------------------------
# Voyager 1 Interstellar Journey: Gravity Slingshot, Grand Tour, RTG, DSN & Oort Scale
# ---------------------------------------------------------------------------
def _register_voyager_1_interstellar():
    SUBDIR = "voyager-1-interstellar"

    EXTRA_ARR = (
        f'<marker id="vg-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{BLUE}"/></marker>'
        f'<marker id="vg-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{ORANGE}"/></marker>'
        f'<marker id="vg-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{GREEN}"/></marker>'
        f'<marker id="vg-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{PURPLE}"/></marker>'
        f'<marker id="vg-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 1.5 L 8.5 5 L 0 8.5 z" fill="{INK}"/></marker>'
    )

    # Exact physical & NASA NSSDCA (1977-084A) orbital constants
    C_KMS = 299792.458
    AU_KM = 149597870.7
    LIGHT_DAY_KM = C_KMS * 86400.0
    LIGHT_DAY_AU = LIGHT_DAY_KM / AU_KM
    assert 25.90e9 < LIGHT_DAY_KM < 25.91e9
    assert 173.1 < LIGHT_DAY_AU < 173.2

    V_EARTH = 29.7847  # km/s circular heliocentric speed at 1 AU
    V_ESC_1AU = V_EARTH * math.sqrt(2.0)  # 42.122 km/s

    # Epoch 1 (Earth -> Jupiter, NSSDCA: rp=1.00 AU, ra=8.96 AU, e=0.79778)
    A1_AU = 0.5 * (1.00 + 8.96)  # 4.98 AU
    R_JUP = 5.20
    R_SAT = 9.54
    V_DEP_1AU = V_EARTH * math.sqrt(2.0 / 1.00 - 1.0 / A1_AU)  # 39.95 km/s < 42.12 km/s!
    V_IN_JUP = V_EARTH * math.sqrt(2.0 / R_JUP - 1.0 / A1_AU)  # 12.77 km/s
    V_ESC_JUP = V_ESC_1AU / math.sqrt(R_JUP)                  # 18.47 km/s

    # Epoch 2 (Post-Jupiter hyperbola, NSSDCA: q=5.20 AU, e=2.30274)
    A2_ABS = R_JUP / (2.30274 - 1.0)  # 3.9916 AU
    V_OUT_JUP = V_EARTH * math.sqrt(2.0 / R_JUP + 1.0 / A2_ABS)  # 23.74 km/s
    V_IN_SAT = V_EARTH * math.sqrt(2.0 / R_SAT + 1.0 / A2_ABS)   # 19.38 km/s
    assert V_DEP_1AU < V_ESC_1AU and V_IN_JUP < V_ESC_JUP < V_OUT_JUP

    # Jupiter flyby hyperbolic eccentricity e_J = 1.31898 -> turning angle delta = 2*asin(1/e_J)
    E_J_FLYBY = 1.31898
    TURN_DEG_J = math.degrees(2.0 * math.asin(1.0 / E_J_FLYBY))  # 98.54 deg
    assert 98.0 < TURN_DEG_J < 99.0

    # 1. Gravity Assist Vector Mechanics & Heliocentric Velocity Jump
    def _build_gravity_slingshot_mechanics():
        els = header(
            "引力弹弓怎么“白嫖”速度？木星系里等速拐弯，太阳系里暴涨 10.9 km/s",
            "左：行星参考系能量守恒与太阳参考系矢量叠加｜右：NASA 实测对日速度曲线跨越太阳逃逸门槛",
        )

        # Left Card: Jupiter Frame vs Sun Frame Vector Addition
        els.append(card(20, 62, 352, 404))
        els.append(txt(36, 84, "① 为什么“下坡加速、上坡减速”还能净赚速度？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, f"关键：木星不是静止靶，它正以 V_J ≈ 13.1 km/s 绕太阳狂奔！", 10.5, MUTED))

        # Top sub-box: Jupiter rest frame exact hyperbola (e = 1.31898, turn = 98.5 deg)
        els.append(card(34, 114, 324, 146, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 132, f"A. 木星静止参考系：进出速率相等，方向偏转 {TURN_DEG_J:.1f}°", 10.5, BLUE, weight="700"))

        jcx, jcy = 186.0, 198.0
        # Plot hyperbola r(theta) = p / (1 + e cos theta) rotated so periapsis is at bottom-right behind Jupiter
        p_px = 30.0
        rot_ang = math.radians(-42.0)  # periapsis direction
        hyp_pts = []
        for k in range(-52, 53):
            th = math.radians(k * 1.95)
            r_h = p_px / (1.0 + E_J_FLYBY * math.cos(th))
            if r_h < 108.0:
                ang = th + rot_ang
                hyp_pts.append((jcx + r_h * math.cos(ang), jcy - r_h * math.sin(ang)))
        d_hyp = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in hyp_pts)
        els.append(f'<path d="{d_hyp}" fill="none" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#vg-blue)"/>')

        # Jupiter globe
        els.append(f'<circle cx="{jcx:.1f}" cy="{jcy:.1f}" r="16" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2.0"/>')
        els.append(f'<line x1="{jcx - 14:.1f}" y1="{jcy - 5:.1f}" x2="{jcx + 14:.1f}" y2="{jcy - 5:.1f}" stroke="{ORANGE}" stroke-width="1.4"/>')
        els.append(f'<line x1="{jcx - 15:.1f}" y1="{jcy + 3:.1f}" x2="{jcx + 15:.1f}" y2="{jcy + 3:.1f}" stroke="{ORANGE}" stroke-width="1.8"/>')
        els.append(txt(jcx - 22, jcy + 4, "木星", 10.4, ORANGE, "end", weight="700"))

        # Labels on incoming & outgoing branches
        p_in = hyp_pts[4]
        p_out = hyp_pts[-4]
        els.append(txt(p_in[0] - 8, p_in[1] + 13, "驶入 |v_∞| = 10.7", 10.0, BODY, "middle", weight="600", halo=True))
        els.append(txt(p_out[0] + 10, p_out[1] - 6, "驶出 |v_∞| = 10.7 km/s", 10.0, BLUE, "middle", weight="700", halo=True))
        els.append(txt(244, 224, "从木星后方绕过", 9.9, PURPLE, weight="700", halo=True))
        els.append(txt(244, 240, "引力把速度矢量向前掰弯！", 9.8, MUTED, halo=True))

        # Bottom sub-box: Sun frame vector addition + tennis ball train analogy
        els.append(card(34, 270, 324, 182, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(46, 289, "B. 太阳参考系矢量合成：v_日 = V_木星 + v_相对", 10.5, GREEN, weight="700"))

        # Vector diagram Before vs After
        # Before: V_J pointing up-left/right? Let's draw V_J horizontal right (96 px = 13.06 km/s, scale = 7.2 px per km/s)
        sc_vec = 5.4
        # Left mini-diagram: BEFORE flyby (v_in,sun = 12.8 km/s)
        vx0, vy0 = 54.0, 372.0
        vj_px = 13.06 * sc_vec  # 70.5 px right
        v_inf_mag = 10.70
        cos_in = (V_IN_JUP ** 2 - 13.06 ** 2 - v_inf_mag ** 2) / (2.0 * 13.06 * v_inf_mag)
        ang_in = math.acos(cos_in)  # ~115.9 deg from +x
        in_x = vx0 + vj_px + v_inf_mag * sc_vec * math.cos(ang_in)
        in_y = vy0 - v_inf_mag * sc_vec * math.sin(ang_in)
        els.append(txt(104, 307, "掠过前：合速度仅 12.8", 10.0, SLATE, "middle", weight="700"))
        els.append(f'<line x1="{vx0:.1f}" y1="{vy0:.1f}" x2="{vx0 + vj_px:.1f}" y2="{vy0:.1f}" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#vg-orange)"/>')
        els.append(f'<line x1="{vx0 + vj_px:.1f}" y1="{vy0:.1f}" x2="{in_x:.1f}" y2="{in_y:.1f}" stroke="{SLATE}" stroke-width="1.9" stroke-dasharray="3 2" marker-end="url(#vg-ink)"/>')
        els.append(f'<line x1="{vx0:.1f}" y1="{vy0:.1f}" x2="{in_x:.1f}" y2="{in_y:.1f}" stroke="{INK}" stroke-width="2.4" marker-end="url(#vg-ink)"/>')
        els.append(txt(vx0 + 36, vy0 + 13, "V_木 13.1", 9.6, ORANGE, "middle", weight="700"))
        els.append(txt(vx0 + 12, vy0 - 28, "12.8", 10.0, INK, "middle", weight="700", halo=True))

        # Right mini-diagram: AFTER flyby (v_out,sun = 23.74 km/s)
        ox2, oy2 = 188.0, 372.0
        ang_out = math.radians(17.0)
        out_x = ox2 + vj_px + v_inf_mag * sc_vec * math.cos(ang_out)
        out_y = oy2 - v_inf_mag * sc_vec * math.sin(ang_out)
        els.append(txt(264, 307, "掠过后：转成顺向叠加 23.7！", 10.0, GREEN, "middle", weight="700"))
        els.append(f'<line x1="{ox2:.1f}" y1="{oy2:.1f}" x2="{ox2 + vj_px:.1f}" y2="{oy2:.1f}" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#vg-orange)"/>')
        els.append(f'<line x1="{ox2 + vj_px:.1f}" y1="{oy2:.1f}" x2="{out_x:.1f}" y2="{out_y:.1f}" stroke="{BLUE}" stroke-width="2.0" stroke-dasharray="3 2" marker-end="url(#vg-blue)"/>')
        els.append(f'<line x1="{ox2:.1f}" y1="{oy2:.1f}" x2="{out_x:.1f}" y2="{out_y:.1f}" stroke="{GREEN}" stroke-width="2.8" marker-end="url(#vg-green)"/>')
        els.append(txt(ox2 + 36, oy2 + 13, "V_木 13.1", 9.6, ORANGE, "middle", weight="700"))
        els.append(txt(ox2 + 102, oy2 - 2, "+v_∞ 10.7", 9.6, BLUE, "middle", weight="700"))
        els.append(txt(ox2 + 64, oy2 - 21, "v_出 ≈ 23.7 km/s", 10.2, GREEN, "middle", weight="700", halo=True))

        # Train tennis analogy note
        els.append(card(42, 392, 308, 50, rx=6, fill="#ffffff", stroke=HAIRLINE))
        els.append(txt(196, 410, "网球比喻：30 km/h 网球迎撞 50 km/h 火车，相对车头以 80", 9.5, BODY, "middle"))
        els.append(txt(196, 427, "弹回，叠加上火车 50 车速 ⇒ 对地飙到 130 km/h（木星慢 10⁻²⁴）", 9.5, GREEN, "middle", weight="700"))

        # Right Card: Exact Heliocentric Speed vs Distance (1 to 32 AU)
        els.append(card(388, 62, 352, 404))
        els.append(txt(404, 84, "② 旅行者 1 号对日速度全账本（1 ～ 32 AU 实算曲线）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "火箭离地时还差 2.2 km/s 才够逃离太阳，全靠木星一脚踹出重围", 10.4, MUTED))

        px0, py0, pw, ph = 436.0, 356.0, 284.0, 224.0
        r_min, r_max = 1.0, 32.0
        v_max = 45.0

        def rx_map(rv):
            return px0 + ((rv - r_min) / (r_max - r_min)) * pw

        def vy_map(vv):
            return py0 - (vv / v_max) * ph

        # Gridlines
        for vv in (10, 20, 30, 40):
            gy = vy_map(vv)
            els.append(f'<line x1="{px0:.1f}" y1="{gy:.1f}" x2="{px0 + pw:.1f}" y2="{gy:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(px0 - 6, gy + 3.5, f"{vv}", 10.0, MUTED, "end"))
        for rv, rlbl in ((1, "1(地球)"), (5.2, "5.2(木)"), (9.5, "9.5(土)"), (20, "20"), (30, "30 AU")):
            gx = rx_map(rv)
            els.append(f'<line x1="{gx:.1f}" y1="{py0:.1f}" x2="{gx:.1f}" y2="{py0 + 4:.1f}" stroke="#94a3b8" stroke-width="1.2"/>')
            els.append(txt(gx, py0 + 16, rlbl, 9.8, MUTED, "middle"))
        els.append(f'<path d="M{px0:.1f},{py0 - ph:.1f} V{py0:.1f} H{px0 + pw:.1f}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')
        els.append(txt(px0 - 6, py0 - ph - 6, "km/s", 10.0, MUTED, "end"))

        # Solar escape curve v_esc(r) = 42.122 / sqrt(r)
        esc_pts = []
        for i in range(125):
            rv = r_min + (r_max - r_min) * i / 124.0
            esc_pts.append((rx_map(rv), vy_map(V_ESC_1AU / math.sqrt(rv))))
        # Light orange fill below escape curve
        poly_trap = [(px0, py0)] + esc_pts + [(px0 + pw, py0)]
        els.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in poly_trap)}" fill="{ORANGE}" fill-opacity="0.07"/>')
        els.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in esc_pts)}" fill="none" stroke="{ORANGE}" stroke-width="2.0" stroke-dasharray="5 3"/>')
        els.append(txt(rx_map(18.5), vy_map(V_ESC_1AU / math.sqrt(18.5)) + 14, "太阳逃逸速度线 √(2GM☉/r)", 9.9, ORANGE, "middle", weight="700", halo=True))

        # Epoch 1: 1.00 -> 5.20 AU (and dashed no-Jupiter stall out to 8.96 AU!)
        ep1_pts = []
        for i in range(61):
            rv = 1.00 + (R_JUP - 1.00) * i / 60.0
            vv = V_EARTH * math.sqrt(2.0 / rv - 1.0 / A1_AU)
            ep1_pts.append((rx_map(rv), vy_map(vv)))
        els.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ep1_pts)}" fill="none" stroke="{SLATE}" stroke-width="2.3"/>')

        stall_pts = []
        for i in range(41):
            rv = R_JUP + (8.94 - R_JUP) * i / 40.0
            vv = V_EARTH * math.sqrt(max(0.0, 2.0 / rv - 1.0 / A1_AU))
            stall_pts.append((rx_map(rv), vy_map(vv)))
        els.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in stall_pts)}" fill="none" stroke="{SLATE}" stroke-width="1.4" stroke-dasharray="3 3"/>')
        els.append(txt(rx_map(8.9), vy_map(2.2) - 4, "无木星：8.96 AU 掉头", 9.5, SLATE, "start", halo=True))

        # Jupiter vertical jump: 12.77 -> 23.74 km/s at 5.20 AU
        jx = rx_map(R_JUP)
        els.append(f'<line x1="{jx:.1f}" y1="{vy_map(V_IN_JUP):.1f}" x2="{jx:.1f}" y2="{vy_map(V_OUT_JUP):.1f}" stroke="{BLUE}" stroke-width="2.8" marker-end="url(#vg-blue)"/>')
        els.append(f'<circle cx="{jx:.1f}" cy="{vy_map(V_IN_JUP):.1f}" r="3.6" fill="{SLATE}"/>')
        els.append(f'<circle cx="{jx:.1f}" cy="{vy_map(V_OUT_JUP):.1f}" r="4.0" fill="{BLUE}"/>')
        els.append(txt(jx + 6, vy_map(28.2), "木星弹弓 +10.9 km/s！", 10.0, BLUE, weight="700", halo=True))

        # Epoch 2: 5.20 -> 9.54 AU
        ep2_pts = []
        for i in range(41):
            rv = R_JUP + (R_SAT - R_JUP) * i / 40.0
            vv = V_EARTH * math.sqrt(2.0 / rv + 1.0 / A2_ABS)
            ep2_pts.append((rx_map(rv), vy_map(vv)))
        els.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ep2_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')

        # Saturn kick (9.54 AU -> post-Saturn barycentric escape ~21.8 km/s tapering to ~17.0 km/s at infinity; a_esc_bary = V_EARTH^2 / 16.6^2 = 3.22 AU -> at 9.54 AU v=21.5, at 32 AU v=18.2, at 173 AU v=16.9!)
        A3_BARY = (V_EARTH / 16.60) ** 2  # ~3.219 AU so v(173 AU) = 16.91 km/s (~3.57 AU/yr)!
        v_post_sat = V_EARTH * math.sqrt(2.0 / R_SAT + 1.0 / A3_BARY)
        sx = rx_map(R_SAT)
        els.append(f'<line x1="{sx:.1f}" y1="{vy_map(V_IN_SAT):.1f}" x2="{sx:.1f}" y2="{vy_map(v_post_sat):.1f}" stroke="{GREEN}" stroke-width="2.5"/>')
        els.append(f'<circle cx="{sx:.1f}" cy="{vy_map(v_post_sat):.1f}" r="4.0" fill="{GREEN}"/>')

        ep3_pts = []
        for i in range(81):
            rv = R_SAT + (r_max - R_SAT) * i / 80.0
            vv = V_EARTH * math.sqrt(2.0 / rv + 1.0 / A3_BARY)
            ep3_pts.append((rx_map(rv), vy_map(vv)))
        els.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ep3_pts)}" fill="none" stroke="{GREEN}" stroke-width="2.6"/>')
        els.append(txt(rx_map(24.0), vy_map(22.5), "土星再推一把 → 永超逃逸线", 9.8, GREEN, "middle", weight="700", halo=True))

        # Summary takeaway card at bottom of Right Card
        els.append(card(402, 384, 324, 68, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(412, 403, "• 1977 离地对日 39.95 km/s < 太阳逃逸 42.12 km/s（封闭椭圆）", 9.5, BODY))
        els.append(txt(412, 421, "• 1979 木星弹弓跃升至 23.7 km/s > 当地逃逸门槛 18.5 km/s", 9.5, BLUE, weight="700"))
        els.append(txt(412, 439, "• 此后纯靠真空惯性滑行，2026 年仍保持 ≈17.0 km/s（3.57 AU/年）", 9.5, GREEN, weight="700"))

        return figure(
            482,
            "旅行者1号木星与土星引力弹弓加速原理及对日速度跨越太阳逃逸速度实算图",
            "左图对比木星参考系中等速偏转98.5度与太阳参考系叠加木星公转13.1 km/s后合速度从12.8跃升至23.7 km/s的矢量机制；右图根据NASA NSSDCA轨道根数绘制1至32 AU对日速度曲线，展示无木星时将在8.96 AU掉头，借木星与土星两次引力弹弓后永久高于太阳逃逸速度。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 2. 175-Year Grand Tour Planetary Alignment & Twin Trajectory Split (Animated)
    def _build_grand_tour_alignment_anim():
        # Verify Uranus-Neptune synodic period ~171.4 yr and 4-giant-planet alignment ~175-176 yr
        t_j, t_s, t_u, t_n = 11.862, 29.457, 84.017, 164.79
        t_syn_un = 1.0 / (1.0 / t_u - 1.0 / t_n)
        assert 171.0 < t_syn_un < 172.0  # 9 J orbits = 171.4 / 19.86 -> ~175.6 yr full 4-planet repeat

        anim_css = """
  .vg-t1 { stroke-dasharray: 460; stroke-dashoffset: 460; animation: vgDraw1 5.6s cubic-bezier(.25,.6,.3,1) 0.3s forwards; }
  .vg-t2 { stroke-dasharray: 560; stroke-dashoffset: 560; animation: vgDraw2 6.8s cubic-bezier(.25,.6,.3,1) 0.5s forwards; }
  .vg-tag { opacity: 0.25; animation: vgShow 0.6s ease 4.8s forwards; }
  @keyframes vgDraw1 { to { stroke-dashoffset: 0; } }
  @keyframes vgDraw2 { to { stroke-dashoffset: 0; } }
  @keyframes vgShow { to { opacity: 1; } }
  @media (prefers-reduced-motion: reduce) {
    .vg-t1, .vg-t2 { animation: none !important; stroke-dashoffset: 0 !important; }
    .vg-tag { animation: none !important; opacity: 1 !important; }
  }"""

        els = header(
            "175 年一遇的“四巨星连珠”：为什么 1 号晚发 16 天，却偏偏不去天王星？",
            "左：1977–1989 外太阳系同侧走廊与双子分道航迹（径向压缩示意）｜右：土卫六大气侦察与 35.8° 北折抉择",
        )

        # Left Card: Top-down Ecliptic Geometric Tour (radially compressed r^0.52 so 1..30 AU are clear)
        els.append(card(20, 62, 396, 404))
        els.append(txt(36, 84, "① 175 年同侧几何窗口与双子航迹（径向压缩示意）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "上次同侧排列还是 1802 年杰斐逊总统任内；错过就要等到 2152 年前后", 10.3, MUTED))

        scx, scy = 148.0, 326.0

        def orb_r(au_val):
            return 28.0 * (au_val ** 0.56)  # 1->28, 5.2->70.4, 9.54->99.1, 19.2->146.5, 30.1->188.6

        # Semi-circular orbit arcs in upper-right quadrant
        for au_v, lbl_p, col_p in (
            (1.0, "地球 1 AU", SLATE),
            (5.2, "木星 5.2", ORANGE),
            (9.54, "土星 9.5", BLUE),
            (19.2, "天王星 19.2", PURPLE),
            (30.1, "海王星 30.1 AU", GREEN),
        ):
            rr = orb_r(au_v)
            a1, a2 = math.radians(-22.0), math.radians(102.0)
            x1, y1 = scx + rr * math.cos(a1), scy - rr * math.sin(a1)
            x2, y2 = scx + rr * math.cos(a2), scy - rr * math.sin(a2)
            els.append(f'<path d="M {x1:.1f},{y1:.1f} A {rr:.1f},{rr:.1f} 0 0 0 {x2:.1f},{y2:.1f}" fill="none" stroke="{HAIRLINE}" stroke-width="1.15" stroke-dasharray="3 3"/>')
            lx, ly = scx + rr * math.cos(math.radians(98.0)), scy - rr * math.sin(math.radians(98.0))
            if au_v >= 5.0:
                els.append(txt(lx - 4, ly + 4, lbl_p, 9.6, col_p, "end", weight="600", halo=True))

        # Sun
        els.append(f'<circle cx="{scx:.1f}" cy="{scy:.1f}" r="8.5" fill="#f59e0b" stroke="#b45309" stroke-width="1.4"/>')
        els.append(txt(scx - 12, scy + 18, "太阳", 10.0, "#b45309", "middle", weight="700"))

        # Planet encounter positions (angular progression matching real counter-clockwise Grand Tour)
        def pos(au_v, deg_v):
            rr = orb_r(au_v)
            rad = math.radians(deg_v)
            return scx + rr * math.cos(rad), scy - rr * math.sin(rad)

        p_earth = pos(1.0, -8.0)
        p_jup = pos(5.2, 18.0)
        p_sat1 = pos(9.54, 41.0)
        p_sat2 = pos(9.54, 34.0)
        p_ura = pos(19.2, 54.0)
        p_nep = pos(30.1, 66.0)
        p_v1_out = (368.0, 150.0)   # steep northward escape (+35.8 deg out of ecliptic)
        p_v2_out = (388.0, 128.0)   # post-Neptune escape

        # Faint static guide tracks (always visible per AGENTS.md)
        d_v1 = (
            f"M {p_earth[0]:.1f},{p_earth[1]:.1f} "
            f"Q {scx + 56:.1f},{scy - 2:.1f} {p_jup[0]:.1f},{p_jup[1]:.1f} "
            f"Q {p_jup[0] + 18:.1f},{p_jup[1] - 28:.1f} {p_sat1[0]:.1f},{p_sat1[1]:.1f} "
            f"L {p_v1_out[0]:.1f},{p_v1_out[1]:.1f}"
        )
        d_v2 = (
            f"M {p_earth[0]:.1f},{p_earth[1]:.1f} "
            f"Q {scx + 62:.1f},{scy + 8:.1f} {p_jup[0] + 3:.1f},{p_jup[1] + 5:.1f} "
            f"Q {p_jup[0] + 28:.1f},{p_jup[1] - 14:.1f} {p_sat2[0]:.1f},{p_sat2[1]:.1f} "
            f"Q {p_sat2[0] + 34:.1f},{p_sat2[1] - 42:.1f} {p_ura[0]:.1f},{p_ura[1]:.1f} "
            f"Q {p_ura[0] + 24:.1f},{p_ura[1] - 34:.1f} {p_nep[0]:.1f},{p_nep[1]:.1f} "
            f"L {p_v2_out[0]:.1f},{p_v2_out[1]:.1f}"
        )

        els.append(f'<path d="{d_v2}" fill="none" stroke="{PURPLE}" stroke-width="1.4" stroke-opacity="0.26"/>')
        els.append(f'<path d="{d_v1}" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-opacity="0.26"/>')
        els.append(f'<path class="vg-t2" d="{d_v2}" fill="none" stroke="{PURPLE}" stroke-width="2.3" stroke-dasharray="6 3" marker-end="url(#vg-purple)"/>')
        els.append(f'<path class="vg-t1" d="{d_v1}" fill="none" stroke="{BLUE}" stroke-width="2.7" marker-end="url(#vg-blue)"/>')

        # Planet dots & encounter dates
        for pt, r_dot, col_d, lbl_d, dx, dy, anc in (
            (p_earth, 4.2, SLATE, "1977.08/09 发射", 12, 14, "start"),
            (p_jup, 6.5, ORANGE, "木星 1979", 10, 8, "start"),
            (p_sat1, 5.8, BLUE, "土星 1980/81", 12, 6, "start"),
            (p_ura, 5.2, PURPLE, "天王星 1986", 10, 6, "start"),
            (p_nep, 5.2, GREEN, "海王星 1989", -10, -8, "end"),
        ):
            els.append(f'<circle cx="{pt[0]:.1f}" cy="{pt[1]:.1f}" r="{r_dot}" fill="#ffffff" stroke="{col_d}" stroke-width="2.2"/>')
            els.append(txt(pt[0] + dx, pt[1] + dy, lbl_d, 9.8, col_d, anc, weight="700", halo=True))

        # Trajectory end tags
        els.append(f'<g class="vg-tag">')
        els.append(txt(p_v1_out[0] - 4, p_v1_out[1] + 20, "旅行者 1 号（实线）", 10.2, BLUE, "end", weight="700", halo=True))
        els.append(txt(p_v1_out[0] - 4, p_v1_out[1] + 35, "北折 35.8° 直奔星际（3.57 AU/年）", 9.7, BLUE, "end", halo=True))
        els.append(txt(p_v2_out[0] - 8, p_v2_out[1] - 6, "旅行者 2 号（虚线）：连访四巨星", 9.9, PURPLE, "end", weight="700", halo=True))
        els.append(f'</g>')

        # Bottom legend inside Left Card
        els.append(card(34, 404, 368, 48, rx=6, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 422, "• 省时奇迹：直飞海王星需 ~30 年，旅行者 2 号借三连弹弓仅用 12 年！", 9.9, INK, weight="600"))
        els.append(txt(46, 439, "• 构想起源：1965 年 JPL 实习生弗兰德罗算出 175 年窗口，促成“壮游计划”", 9.8, MUTED))

        # Right Card: Why Voyager 1 Launched Later Yet Overtook V2, and Sacrificed Uranus for Titan
        els.append(card(432, 62, 308, 404))
        els.append(txt(448, 84, "② 三个最容易搞反的任务真相", PANEL_TITLE, INK, weight="700"))

        cards_r = [
            (
                "1",
                BLUE,
                BLUE_SOFT,
                "晚发 16 天，凭什么反而叫“1 号”？",
                "• 2 号先走（1977.08.20），走曲率更缓的慢线；",
                "• 1 号后发（1977.09.05），走更陡的快线；",
                "• 1977.12.15 在小行星带超车，提前 4 个月抵木星！",
            ),
            (
                "2",
                ORANGE,
                ORANGE_SOFT,
                "为什么 1 号拍完土星就“脱离主路”？",
                "• 头号目标：近距穿透土卫六（Titan）氮甲烷浓雾；",
                "• 必须从土星南极下方斜掠，引力将其向北猛折 35.8°；",
                "• 翘出黄道面无法再去天王星，却换来最快出逃速度！",
            ),
            (
                "3",
                GREEN,
                GREEN_SOFT,
                "为什么它们都没顺路去拍冥王星？",
                "• 1 号若改飞冥王星就得放弃土卫六近距飞掠；",
                "• 2 号若在海王星拐向冥王星，瞄准点要穿进海王星肚子；",
                "• 冥王星直到 2015 年才由“新视野号”专程造访。",
            ),
        ]

        for idx, (num_s, col_c, bg_c, title_c, l1, l2, l3) in enumerate(cards_r):
            cy_card = 104 + idx * 116
            els.append(card(446, cy_card, 280, 104, rx=8, fill=bg_c, stroke=col_c))
            els.append(step_badge(462, cy_card + 20, num_s, fg=col_c, bg="#ffffff", r=10))
            els.append(txt(478, cy_card + 24, title_c, 10.6, INK, weight="700"))
            els.append(txt(456, cy_card + 47, l1, 9.9, BODY))
            els.append(txt(456, cy_card + 66, l2, 9.9, BODY))
            els.append(txt(456, cy_card + 85, l3, 9.9, col_c, weight="700"))

        return figure(
            482,
            "175年一遇外太阳系四巨星连珠窗口与旅行者1号2号分道航迹动画图解",
            "左图展示1977至1989年木星、土星、天王星、海王星同侧几何走廊（径向压缩示意），动画演示旅行者1号在土星因贴掠土卫六向北偏折35.8度高速奔向星际空间，而旅行者2号连访四颗巨行星；右图解释1号晚发超车、土卫六轨道取舍与未访冥王星的原因。",
            els,
            extra_css=anim_css,
            extra_defs=EXTRA_ARR,
        )

    # 3. Plutonium-238 MHW-RTG Nuclear Battery & 50-Year Power Triage Curve
    def _build_rtg_power_survival():
        # Verify solar inverse-square at 1 light-day (173.15 AU) & Pu-238 decay
        inv_sq_1ld = LIGHT_DAY_AU ** 2  # ~29,980
        assert 29900 < inv_sq_1ld < 30100
        t_half = 87.7
        pu_rem_2026 = 0.5 ** ((2026.88 - 1977.68) / t_half)  # ~0.678 (67.8% isotope left!)
        assert 0.67 < pu_rem_2026 < 0.69

        els = header(
            "阳光只剩三万分之一，靠什么撑满半世纪？钚-238 温差核电池与“断臂求生”账本",
            "左：3 台串联 MHW-RTG 塞贝克温差发电结构｜右：470 W 跌至 ~213 W 衰减曲线与 +2°C 联氨防冻红线",
        )

        # Left Card: MHW-RTG Schematic & Inverse-Square Sunlight Collapse
        els.append(card(20, 62, 352, 412))
        els.append(txt(36, 84, "① 不是核反应堆！无运动部件的“温差发电保温杯”", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "173 AU 处阳光仅地球 1/30,000（0.045 W/m²），光伏帆板彻底失效", 10.3, MUTED))

        # Cutaway cylinder of an MHW-RTG
        els.append(card(34, 116, 324, 210, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(196, 135, "单台 MHW-RTG 剖面（全船吊杆串联 3 台，总初功率 ~470 W）", 10.2, INK, "middle", weight="700"))

        # Radiator fins top & bottom
        rcx, rcy = 122.0, 218.0
        for fy in (152, 272):
            els.append(f'<polygon points="{rcx - 62},{fy} {rcx + 62},{fy} {rcx + 50},{fy + (12 if fy < 200 else -12)} {rcx - 50},{fy + (12 if fy < 200 else -12)}" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.3"/>')
        # Outer beryllium case
        els.append(f'<rect x="{rcx - 72:.1f}" y="164" width="144" height="108" rx="10" fill="#e2e8f0" stroke="{SLATE}" stroke-width="1.8"/>')
        # SiGe thermocouple ring
        els.append(f'<rect x="{rcx - 58:.1f}" y="178" width="116" height="80" rx="8" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="4 2"/>')
        # Glowing PuO2 ceramic core
        els.append(f'<rect x="{rcx - 44:.1f}" y="194" width="88" height="48" rx="6" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2.2"/>')
        els.append(txt(rcx, 214, "²³⁸PuO₂ 陶瓷丸", 9.4, ORANGE, "middle", weight="700"))
        els.append(txt(rcx, 231, "α 衰变 ~1000°C", 9.2, ORANGE, "middle", weight="600"))

        # Callout arrows to right side of cylinder
        els.append(f'<line x1="{rcx + 44:.1f}" y1="206" x2="206" y2="176" stroke="{ORANGE}" stroke-width="1.4"/>')
        els.append(txt(210, 173, "热端：半衰期 87.7 年", 9.6, ORANGE, weight="700"))
        els.append(txt(210, 188, "α 粒子一张纸即可挡住", 9.4, BODY))

        els.append(f'<line x1="{rcx + 58:.1f}" y1="218" x2="206" y2="218" stroke="{BLUE}" stroke-width="1.4"/>')
        els.append(txt(210, 215, "312 对硅锗热电偶", 9.6, BLUE, weight="700"))
        els.append(txt(210, 230, "塞贝克温差直变直流电", 9.4, BODY))

        els.append(f'<line x1="{rcx + 64:.1f}" y1="254" x2="206" y2="258" stroke="{SLATE}" stroke-width="1.4"/>')
        els.append(txt(210, 255, "冷端：铍壳散热翅片", 9.6, SLATE, weight="700"))
        els.append(txt(210, 270, "向深空辐射排热造温差", 9.4, BODY))

        els.append(txt(196, 313, "零旋转齿轮、零磨损阀门 ⇒ 连续发电 49 年从不卡壳！", 9.8, GREEN, "middle", weight="700"))

        # Bottom box inside Left Card: Why +2°C Hydrazine Freezing Is the Real Killer
        els.append(card(34, 338, 324, 122, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(44, 358, "极寒生死线：为什么还剩 210 多瓦电，却连关科学仪器？", 9.9, ORANGE, weight="700"))
        els.append(txt(44, 378, "• 姿态推进剂“联氨（N₂H₄）”冰点高达 +2°C（比水还娇气！）", 9.5, INK, weight="600"))
        els.append(txt(44, 397, "• 一旦管路冻住，推进器失灵 → 天线偏离地球 0.5° 即失联", 9.5, BODY))
        els.append(txt(44, 416, "• 如今大半电力全在给油路和电脑“贴暖宝宝”保命；", 9.5, BODY))
        els.append(txt(44, 435, "• 2026.09 刚完成“Big Bang”三组加热器同步切换降耗！", 9.5, PURPLE, weight="700"))

        # Right Card: Exact Power Decay Curve (1977 - 2036) & Instrument Triage Milestones
        els.append(card(388, 62, 352, 412))
        els.append(txt(404, 84, "② 电功率衰减曲线（每年掉 ~4 W）与仪器关机时间表", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "双杀叠加：²³⁸Pu 放射性热源自然衰变 + 硅锗热电偶半世纪老化", 10.3, MUTED))

        gx0, gy0, gw, gh = 438.0, 342.0, 282.0, 206.0
        y_min_yr, y_max_yr = 1977.0, 2037.0
        w_max = 500.0

        def tx_map(yr):
            return gx0 + ((yr - y_min_yr) / (y_max_yr - y_min_yr)) * gw

        def wy_map(wv):
            return gy0 - (wv / w_max) * gh

        for wv in (100, 200, 300, 400, 500):
            yy = wy_map(wv)
            els.append(f'<line x1="{gx0:.1f}" y1="{yy:.1f}" x2="{gx0 + gw:.1f}" y2="{yy:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(gx0 - 6, yy + 3.5, f"{wv}W", 9.8, MUTED, "end"))
        for yr in (1977, 1990, 2005, 2020, 2026, 2035):
            xx = tx_map(yr)
            els.append(f'<line x1="{xx:.1f}" y1="{gy0:.1f}" x2="{xx:.1f}" y2="{gy0 + 4:.1f}" stroke="#94a3b8" stroke-width="1.2"/>')
            els.append(txt(xx, gy0 + 16, f"{yr}", 9.8, MUTED, "middle"))
        els.append(f'<path d="M{gx0:.1f},{gy0 - gh:.1f} V{gy0:.1f} H{gx0 + gw:.1f}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')

        # Curve 1 (dashed): Pure Pu-238 isotope decay without thermocouple aging: 470 * 0.5^((yr-1977.68)/87.7)
        iso_pts = []
        # Curve 2 (solid): Actual electrical power matching NASA points:
        # P(t) = 470 * 0.5^(dt/87.7) * exp(-0.00495 * dt) -> check dt=19.3 (1997): 470*0.859*0.909 = 367/335;
        # More exact NASA fit: thermocouple degradation fastest in first 15 yrs then ~4.1 W/yr linear-exponential:
        def p_elec(yr):
            dt = max(0.0, yr - 1977.68)
            p_iso = 470.0 * (0.5 ** (dt / 87.7))
            eta_rel = 0.895 + 0.105 * math.exp(-dt / 8.0) - 0.00425 * dt
            return p_iso * eta_rel

        assert 468.0 < p_elec(1977.68) < 471.0
        assert 330.0 < p_elec(1997.0) < 342.0
        assert 220.0 < p_elec(2023.5) < 232.0
        assert 210.0 < p_elec(2026.88) < 220.0

        act_pts = []
        for i in range(121):
            yr = y_min_yr + (y_max_yr - y_min_yr) * i / 120.0
            dt = max(0.0, yr - 1977.68)
            iso_pts.append((tx_map(yr), wy_map(470.0 * (0.5 ** (dt / 87.7)))))
            act_pts.append((tx_map(yr), wy_map(p_elec(yr))))

        els.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in iso_pts)}" fill="none" stroke="{SLATE}" stroke-width="1.7" stroke-dasharray="4 3"/>')
        els.append(txt(tx_map(2016), wy_map(362), "仅算同位素衰变（理论上限）", 9.6, SLATE, "middle", halo=True))

        # Threshold band around ~180-195 W (~2030-2035 telecom + heater floor)
        y_floor = wy_map(185.0)
        els.append(f'<rect x="{gx0:.1f}" y="{y_floor:.1f}" width="{gw:.1f}" height="{gy0 - y_floor:.1f}" fill="{ORANGE}" fill-opacity="0.08"/>')
        els.append(f'<line x1="{gx0:.1f}" y1="{y_floor:.1f}" x2="{gx0 + gw:.1f}" y2="{y_floor:.1f}" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(txt(gx0 + 8, y_floor + 14, "防冻加热 + 无线电最低维持线（约 2030 年代失联）", 9.5, ORANGE, weight="700", halo=True))

        els.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in act_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.7"/>')

        # Key milestone dots on actual curve
        for yr_m, lbl_m, col_m, dx_m, dy_m, anc_m in (
            (1977.7, "1977 发射 470 W", BLUE, 4, -8, "start"),
            (1990.1, "1990 拍完暗淡蓝点关相机", PURPLE, 6, -10, "start"),
            (2012.6, "2012 闯入星际", GREEN, -4, -12, "end"),
            (2026.9, "2026 ~218 W（仅剩 2 台）", ORANGE, 8, -10, "end"),
        ):
            mx, my = tx_map(yr_m), wy_map(p_elec(yr_m))
            els.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="4.0" fill="#ffffff" stroke="{col_m}" stroke-width="2.2"/>')
            els.append(txt(mx + dx_m, my + dy_m, lbl_m, 9.5, col_m, anc_m, weight="700", halo=True))

        # Bottom summary list of active vs shutoff instruments in Nov 2026
        els.append(card(402, 372, 324, 88, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(412, 391, "截至 2026 年 11 月仪器生死簿（10 台科学仪器关剩 2 台）：", 9.9, INK, weight="700"))
        els.append(txt(412, 410, "• 仍在坚守（2 台）：磁强计 MAG + 等离子体波子系统 PWS", 9.6, GREEN, weight="700"))
        els.append(txt(412, 428, "• 近年关停：宇宙射线 CRS（2025.02）｜低能粒子 LECP（2026.04）", 9.4, BODY))
        els.append(txt(412, 446, "• 早年关停：双相机 ISS（1990）｜红外 IRIS（1998）｜紫外 UVS", 9.4, MUTED))

        return figure(
            490,
            "旅行者1号钚238放射性同位素温差核电池原理与1977至2036年电功率衰减关机时间表",
            "左图展示MHW-RTG利用二氧化钚238自然α衰变热与312对硅锗热电偶塞贝克效应无磨损发电的结构，并解释联氨推进剂+2摄氏度结冰红线；右图绘制总电功率从1977年470瓦以每年约4瓦降至2026年约213瓦的实测曲线及10台科学仪器关停至仅剩MAG和PWS的过程。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 4. 23-Watt Transmitter Across 1 Light-Day (25.9 Billion km) & 69.63 KB Brain Surgery
    def _build_dsn_link_and_computer():
        # Verify X-band 8.4 GHz wavelength, 3.66m HGA beamwidth & received power order of magnitude
        freq_hz = 8.4e9
        lam_m = (C_KMS * 1000.0) / freq_hz  # 0.03569 m (~3.57 cm)
        d_hga = 3.66
        beam_deg = math.degrees(1.22 * lam_m / d_hga)  # ~0.68 deg!
        assert 0.60 < beam_deg < 0.75
        # Friis link budget check at R = 2.59e13 m: Pt = 23 W, Gt ~ eta*(pi*D/lam)^2 (~48 dBi = 6.3e4), Ar_70m ~ 0.65*pi*35^2 = 2500 m^2
        # Pr = Pt * Gt * Ar / (4 * pi * R^2) = 23 * 6.3e4 * 2500 / (12.566 * (2.59e13)^2) ~ 4.3e-19 to 1e-20 W (including losses)!
        pr_watts = 23.0 * (0.55 * (math.pi * d_hga / lam_m) ** 2) * (0.62 * math.pi * 35.0 ** 2) / (4.0 * math.pi * (LIGHT_DAY_KM * 1000.0) ** 2)
        assert 1e-20 < pr_watts < 1e-18

        els = header(
            "23 瓦“冰箱灯泡”怎样喊穿 259 亿公里？深空网 70 米巨耳与 69 KB 内存奇迹",
            "上：1 光日（单程 24 小时）X 波段极窄波束链路｜下：69.63 KB 古董电脑远程拆代码与光速延迟尺",
        )

        # Top Full-Width Card: End-to-End 1-Light-Day Link
        els.append(card(20, 62, 720, 206))
        els.append(txt(36, 84, "① 跨越 1 光日（259.02 亿 km）的极限通信账：功率稀释 10²¹ 倍还能听见！", PANEL_TITLE, INK, weight="700"))

        # Left: Voyager 1 HGA + 23 W X-band
        els.append(card(36, 98, 196, 154, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(134, 117, "飞船端：旅行者 1 号", 10.6, BLUE, "middle", weight="700"))
        # Dish icon facing right
        els.append(f'<rect x="54" y="148" width="22" height="32" rx="3" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.5"/>')
        els.append(f'<path d="M 86,132 Q 68,164 86,196" fill="none" stroke="{BLUE}" stroke-width="3.0"/>')
        els.append(f'<line x1="82" y1="164" x2="100" y2="164" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(f'<circle cx="102" cy="164" r="3.2" fill="{ORANGE}"/>')
        els.append(txt(114, 146, "• 3.7 米抛物面天线", 9.9, INK, weight="700"))
        els.append(txt(114, 164, "• 发射功率仅 23 W", 9.9, ORANGE, weight="700"))
        els.append(txt(114, 181, f"• 8.4 GHz 波束宽 {beam_deg:.2f}°", 9.8, BODY))
        els.append(txt(134, 214, "主动降速至 160 bps 攒信噪比", 9.8, BLUE, "middle", weight="600"))
        els.append(txt(134, 232, "（歪 0.5° 地球就彻底收不到！）", 9.6, MUTED, "middle"))

        # Middle: Narrow radio beam crossing 25.9 billion km (24h one-way)
        els.append(f'<polygon points="234,158 518,128 518,200 234,170" fill="{ORANGE}" fill-opacity="0.11"/>')
        els.append(f'<line x1="234" y1="160" x2="514" y2="132" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#vg-orange)"/>')
        els.append(f'<line x1="234" y1="168" x2="514" y2="196" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#vg-orange)"/>')
        els.append(txt(376, 120, "2026.11.18 突破 1 光日 = 259.02 亿 km（173.1 AU）", 10.3, ORANGE, "middle", weight="700", halo=True))
        els.append(txt(376, 162, "光速飞行单程 24 小时整｜一问一答往返 48 小时！", 10.2, INK, "middle", weight="700", halo=True))
        els.append(txt(376, 182, "平方反比稀释 1/(4πR²) ⇒ 落地功率仅剩 ~10⁻¹⁹～10⁻²⁰ W", 9.8, PURPLE, "middle", weight="700", halo=True))
        els.append(txt(376, 224, "（不到电子表电池功率的百亿亿分之一！）", 9.7, MUTED, "middle"))

        # Right: NASA Deep Space Network (3 x 120 deg global 70m dishes)
        els.append(card(522, 98, 202, 154, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(623, 117, "地球端：NASA 深空网 DSN", 10.6, GREEN, "middle", weight="700"))
        # 70m dish icon + 3 stations around Earth
        els.append(f'<circle cx="562" cy="166" r="21" fill="#ffffff" stroke="{GREEN}" stroke-width="1.6"/>')
        for ang_s, st_lbl in ((90, "加州"), (210, "马德里"), (330, "堪培拉")):
            rx_s = 562 + 21 * math.cos(math.radians(ang_s))
            ry_s = 166 - 21 * math.sin(math.radians(ang_s))
            els.append(f'<circle cx="{rx_s:.1f}" cy="{ry_s:.1f}" r="3.8" fill="{GREEN}"/>')
        els.append(txt(562, 170, "120°", 9.5, GREEN, "middle", weight="700"))
        els.append(txt(594, 146, "• 70 米巨型抛物面天线", 9.9, INK, weight="700"))
        els.append(txt(594, 164, "• 液氦超低温放大器", 9.9, GREEN, weight="700"))
        els.append(txt(594, 181, "• 全球经度隔 120° 三站", 9.8, BODY))
        els.append(txt(623, 214, "戈德斯通 · 马德里 · 堪培拉", 9.8, GREEN, "middle", weight="600"))
        els.append(txt(623, 232, "地球自转 24 小时无缝接力盯防", 9.6, MUTED, "middle"))

        # Bottom Left Card: 69.63 KB Computer & 2024 Remote Code Surgery
        els.append(card(20, 284, 352, 192))
        els.append(txt(36, 306, "② 69.63 KB 内存上的“星际脑外科手术”", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 324, "全船三台电脑每秒仅算 8,000 次（不及手机百万分之一！）", 9.8, MUTED))

        # Memory block diagram showing broken chip -> code sliced into 3 spare corners
        els.append(card(36, 338, 320, 74, rx=6, fill="#f8fafc", stroke=BORDER))
        els.append(card(48, 350, 92, 50, rx=5, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(94, 371, "FDS 损坏芯片", 9.9, ORANGE, "middle", weight="700"))
        els.append(txt(94, 388, "2023.11 传回乱码", 9.4, BODY, "middle"))

        els.append(f'<line x1="144" y1="375" x2="184" y2="375" stroke="{PURPLE}" stroke-width="2.0" marker-end="url(#vg-purple)"/>')
        els.append(txt(164, 366, "拆段搬家", 9.3, PURPLE, "middle", weight="700"))

        for k_slot, (sy_slot, sl_lbl) in enumerate(((346, "空闲角 A：工程打包代码"), (368, "空闲角 B：科学打包段 1"), (390, "空闲角 C：科学打包段 2"))):
            els.append(f'<rect x="190" y="{sy_slot}" width="154" height="17" rx="3" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.1"/>')
            els.append(txt(267, sy_slot + 12, sl_lbl, 9.2, PURPLE, "middle", weight="600"))

        els.append(txt(36, 433, "• 无整块空余内存 → 手拆代码塞进多处边角并重写跳转；", 9.5, BODY))
        els.append(txt(36, 452, "• 2024.04 奇迹复活！2026.11 冲一光日前夕再度远程排障。", 9.5, PURPLE, weight="700"))

        # Bottom Right Card: Cosmic Light-Time Ladder
        els.append(card(388, 284, 352, 192))
        els.append(txt(404, 306, "③ 光速延迟阶梯：为什么“1 光日”是史诗级路标？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 324, "真空光速 c ≈ 30 万 km/s，连光都要跑整整一昼夜", 10.1, MUTED))

        rungs = [
            ("地球 → 月球（38.4 万 km）", "1.28 光秒", 24, SLATE),
            ("太阳 → 地球（1 AU = 1.5 亿 km）", "8 分 20 秒", 68, BLUE),
            ("地球 → 海王星（约 45 亿 km）", "4 小时 10 分", 136, PURPLE),
            ("地球 → 旅行者 1 号（259 亿 km）", "24 小时（1 光日！）", 216, ORANGE),
            ("太阳 → 最近恒星比邻星", "4.24 光年（1549 光日）", 316, GREEN),
        ]
        for idx_r, (r_name, r_time, bar_w, r_col) in enumerate(rungs):
            ry = 342 + idx_r * 25
            els.append(f'<rect x="404" y="{ry}" width="{bar_w}" height="17" rx="4" fill="{r_col}" fill-opacity="0.16" stroke="{r_col}" stroke-width="1.2"/>')
            els.append(txt(410, ry + 12.5, r_name, 9.5, INK, weight="600"))
            els.append(txt(726, ry + 12.5, r_time, 9.6, r_col, "end", weight="700", halo=True))

        return figure(
            492,
            "旅行者1号23瓦X波段跨越1光日深空网通信链路与69KB计算机远程代码修复图解",
            "上图展示旅行者1号用3.7米高增益天线和23瓦X波段发射机跨越259.02亿公里（1光日，单程24小时），由全球间隔120度的三座NASA深空网70米天线接收约10^-20瓦微弱信号；左下图图解69.63 KB内存中拆分搬迁FDS损坏芯片代码的过程；右下图对比从地月1.28光秒到1光日与比邻星4.24光年的光行时间阶梯。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 5. Logarithmic Cosmic Ruler: Heliopause (122 AU) vs 1 Light-Day (173 AU) vs Oort Cloud (50,000 AU)
    def _build_heliopause_vs_oort_scale():
        # 10-meter dining table scale check: radius 50,000 AU = 5.0 m (500 cm = 5000 mm)
        # -> 1 AU = 0.1 mm! Neptune 30 AU = 3.0 mm! Voyager 1 at 173.1 AU = 17.3 mm = 1.73 cm!
        r_oort_au = 50000.0
        table_r_cm = 500.0  # 10 m diameter -> 500 cm radius
        neptune_mm = (30.1 / r_oort_au) * (table_r_cm * 10.0)
        voyager_cm = (LIGHT_DAY_AU / r_oort_au) * table_r_cm
        assert 2.9 < neptune_mm < 3.1
        assert 1.70 < voyager_cm < 1.76

        els = header(
            "冲进星际空间 ≠ 飞出太阳系！一张对数标尺分清“日球层磁泡”与“奥尔特云”",
            "上：10⁰ ～ 3×10⁵ AU 对数全景尺｜下：2012 日球层顶粒子反转铁证与 10 米圆桌真实比例尺",
        )

        # Top Full-Width Logarithmic Scale Card
        els.append(card(20, 62, 720, 212))
        els.append(txt(36, 84, "① 太阳系对数坐标全景尺（每向右一格距离放大 10 倍！）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "按等离子体算，2012 年已进星际空间；按太阳引力疆界算，还要再飞约 3 万年才出奥尔特云", 10.2, MUTED))

        lx0, lx1, ly = 54.0, 706.0, 184.0
        log_min, log_max = 0.0, 5.50  # 1 AU to ~316,000 AU (Proxima = 268,142 AU)

        def log_x(au_v):
            return lx0 + ((math.log10(au_v) - log_min) / (log_max - log_min)) * (lx1 - lx0)

        # Colored domain bands along axis
        x_helio = log_x(122.0)
        x_oort_in = log_x(1500.0)
        x_oort_out = log_x(60000.0)
        els.append(f'<rect x="{lx0:.1f}" y="{ly - 20:.1f}" width="{x_helio - lx0:.1f}" height="40" rx="4" fill="{ORANGE}" fill-opacity="0.12"/>')
        els.append(f'<rect x="{x_helio:.1f}" y="{ly - 20:.1f}" width="{x_oort_out - x_helio:.1f}" height="40" fill="{BLUE}" fill-opacity="0.10"/>')
        els.append(f'<rect x="{x_oort_in:.1f}" y="{ly - 12:.1f}" width="{x_oort_out - x_oort_in:.1f}" height="24" rx="4" fill="{PURPLE}" fill-opacity="0.14" stroke="{PURPLE}" stroke-width="1.1" stroke-dasharray="3 2"/>')
        els.append(f'<rect x="{x_oort_out:.1f}" y="{ly - 20:.1f}" width="{lx1 - x_oort_out:.1f}" height="40" rx="4" fill="{GREEN}" fill-opacity="0.11"/>')

        els.append(txt((lx0 + x_helio) / 2, ly + 40, "太阳风磁泡：日球层内", 9.8, ORANGE, "middle", weight="700"))
        els.append(txt((x_oort_in + x_oort_out) / 2, ly + 40, "奥尔特彗星云（仍受太阳引力束缚）", 9.8, PURPLE, "middle", weight="700"))
        els.append(txt((x_oort_out + lx1) / 2, ly + 40, "恒星际自由区", 9.6, GREEN, "middle", weight="700"))

        # Main axis + decade ticks 10^0 .. 10^5
        els.append(f'<line x1="{lx0:.1f}" y1="{ly:.1f}" x2="{lx1:.1f}" y2="{ly:.1f}" stroke="{INK}" stroke-width="2.0"/>')
        for p_dec in range(6):
            tx = log_x(10.0 ** p_dec)
            els.append(f'<line x1="{tx:.1f}" y1="{ly - 6:.1f}" x2="{tx:.1f}" y2="{ly + 6:.1f}" stroke="{INK}" stroke-width="1.5"/>')
            els.append(txt(tx, ly + 23, f"10^{p_dec} AU", 9.4, MUTED, "middle", halo=True))

        # Landmark pins alternating above / staggered above so zero overlap!
        pins = [
            (1.0, "地球 1", SLATE, -32, "start"),
            (5.2, "木 5.2", SLATE, -52, "middle"),
            (30.1, "海王星 30", SLATE, -32, "middle"),
            (122.0, "日球层顶 122 AU (2012)", BLUE, -62, "middle"),
            (LIGHT_DAY_AU, "1 光日 173 AU (2026.11) ★", ORANGE, -34, "start"),
            (1500.0, "奥尔特内缘 (~300年后)", PURPLE, -58, "middle"),
            (60000.0, "引力边界 (~3万年后)", PURPLE, -34, "middle"),
            (268142.0, "比邻星 4.24光年", GREEN, -58, "end"),
        ]
        for au_p, lbl_p, col_p, dy_p, anc_p in pins:
            px = log_x(au_p)
            els.append(f'<line x1="{px:.1f}" y1="{ly:.1f}" x2="{px:.1f}" y2="{ly + dy_p + 6:.1f}" stroke="{col_p}" stroke-width="1.3"/>')
            els.append(f'<circle cx="{px:.1f}" cy="{ly:.1f}" r="3.8" fill="#ffffff" stroke="{col_p}" stroke-width="2.2"/>')
            els.append(txt(px, ly + dy_p, lbl_p, 9.6, col_p, anc_p, weight="700", halo=True))

        els.append(txt(36, 256, "注：1 AU（天文单位）≈ 1.496 亿 km；1 光日 ≈ 173.1 AU；1 光年 ≈ 63,241 AU。", 9.7, MUTED))

        # Bottom Left Card: Aug 25, 2012 Heliopause Crossing Evidence
        els.append(card(20, 290, 352, 196))
        els.append(txt(36, 312, "② 2012.08.25 闯出日球层顶的“三大实测铁证”", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 330, "没有路牌的漆黑太空，科学家凭什么确认它跨过了 122 AU 边界？", 9.9, MUTED))

        # Mini step-change plot across 2012.65 (121.6 AU)
        cx0, cy0, cw, ch = 56.0, 430.0, 290.0, 74.0
        els.append(f'<rect x="{cx0}" y="{cy0 - ch}" width="{cw}" height="{ch}" rx="4" fill="#f8fafc" stroke="{BORDER}"/>')
        x_hp = cx0 + cw * 0.52
        els.append(f'<line x1="{x_hp:.1f}" y1="{cy0 - ch}" x2="{x_hp:.1f}" y2="{cy0}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 2"/>')
        els.append(txt(x_hp, cy0 - ch - 5, "2012.08.25 日球层顶", 9.5, INK, "middle", weight="700"))

        # Solar wind particles plummet (orange)
        els.append(f'<path d="M {cx0 + 6},{cy0 - 58} L {x_hp - 12},{cy0 - 55} L {x_hp + 8},{cy0 - 8} L {cx0 + cw - 6},{cy0 - 7}" fill="none" stroke="{ORANGE}" stroke-width="2.3"/>')
        els.append(txt(cx0 + 12, cy0 - 61, "太阳风低能粒子 → 骤降至零", 9.4, ORANGE, weight="700", halo=True))

        # Galactic cosmic rays & plasma density jump (blue)
        els.append(f'<path d="M {cx0 + 6},{cy0 - 16} L {x_hp - 12},{cy0 - 18} L {x_hp + 8},{cy0 - 58} L {cx0 + cw - 6},{cy0 - 60}" fill="none" stroke="{BLUE}" stroke-width="2.3"/>')
        els.append(txt(x_hp + 12, cy0 - 44, "银河宇宙射线暴涨", 9.4, BLUE, weight="700", halo=True))
        els.append(txt(x_hp + 12, cy0 - 28, "等离子体密度跃升 ~40 倍！", 9.4, GREEN, weight="700", halo=True))

        els.append(txt(36, 454, "• 等离子体仪早年停机，幸亏 2013 太阳风暴激起电子振荡，", 9.5, BODY))
        els.append(txt(36, 471, "  PWS 听出“星际琴弦音高”实测密度暴涨 40 倍，一锤定音！", 9.5, BLUE, weight="700"))

        # Bottom Right Card: 10m Dining Table Metaphor & 4.5-Billion-Year Golden Record
        els.append(card(388, 290, 352, 196))
        els.append(txt(404, 312, "③ 10 米大圆桌比例尺与“45 亿年镀金漂流瓶”", PANEL_TITLE, INK, weight="700"))

        # Sub-box 1: 10m table
        els.append(card(402, 326, 324, 68, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(414, 345, f"若把奥尔特云（半径 5 万 AU）缩成直径 10 米的大圆桌：", 9.8, PURPLE, weight="700"))
        els.append(txt(414, 364, f"• 八大行星全挤在圆心 {neptune_mm:.1f} 毫米的针尖里；", 9.6, BODY))
        els.append(txt(414, 382, f"• 狂奔 49 年的旅行者 1 号，才刚爬出圆心 {voyager_cm:.2f} 厘米！", 9.6, INK, weight="700"))

        # Sub-box 2: Golden Record (30 cm gold-plated copper disc + U-238 clock)
        els.append(card(402, 402, 324, 72, rx=8, fill="#fffbeb", stroke="#d97706"))
        els.append(f'<circle cx="434" cy="438" r="21" fill="#fde68a" stroke="#b45309" stroke-width="1.8"/>')
        els.append(f'<circle cx="434" cy="438" r="5" fill="#ffffff" stroke="#b45309" stroke-width="1.3"/>')
        els.append(txt(464, 421, "关机后永不停航：30 cm 镀金铜唱片", 9.9, "#b45309", weight="700"))
        els.append(txt(464, 439, "• 护盖镀超纯 ²³⁸U（45.1 亿年核时钟）+ 14 颗脉冲星定位", 9.3, BODY))
        els.append(txt(464, 457, "• 录 55 种语言问候与古琴《流水》，4 万年后掠过红矮星", 9.3, BODY))

        return figure(
            502,
            "太阳系对数坐标全景尺：对比旅行者1号日球层顶122AU、1光日173AU与奥尔特云50000AU引力边界",
            "上图以对数坐标展示从地球1 AU、海王星30 AU、日球层顶122 AU（2012年进入星际空间）、1光日173.1 AU（2026年11月18日）到奥尔特云外缘约5万至10万AU及比邻星4.24光年的真实尺度；左下图展示2012年8月25日太阳风粒子归零、银河宇宙射线暴涨与等离子体密度跃升40倍的实测证据；右下图给出10米圆桌缩尺比喻与旅行者金唱片45.1亿年铀238时钟。",
            els,
            extra_defs=EXTRA_ARR,
        )

    @register("voyager-1-interstellar", "旅行者1号星际旅行全解密：木星引力弹弓、175年四巨星连珠、钚238核电池、23瓦深空通信与奥尔特云尺度", "mechanics_sky")
    def build_voyager_1_interstellar():
        write_svg(SUBDIR, "gravity-slingshot-vector-mechanics.svg", _build_gravity_slingshot_mechanics())
        write_svg(SUBDIR, "grand-tour-175yr-slingshot-anim.svg", _build_grand_tour_alignment_anim())
        write_svg(SUBDIR, "rtg-plutonium-power-survival.svg", _build_rtg_power_survival())
        write_svg(SUBDIR, "dsn-23watt-1lightday-link.svg", _build_dsn_link_and_computer())
        write_svg(SUBDIR, "heliopause-vs-oort-log-scale.svg", _build_heliopause_vs_oort_scale())


_register_voyager_1_interstellar()


def _register_mars_sample_return():
    SUBDIR = "mars-sample-return-challenges"

    # Verified planetary & propulsion constants (SI / km-s units)
    G0 = 9.80665e-3  # km/s^2
    MU_MARS = 42828.37  # km^3/s^2
    R_MARS = 3389.5  # km
    V_ESC_MARS = math.sqrt(2.0 * MU_MARS / R_MARS)  # 5.027 km/s
    H_LMO = 350.0  # km typical rendezvous orbit
    V_LMO = math.sqrt(MU_MARS / (R_MARS + H_LMO))  # 3.384 km/s
    assert 5.02 < V_ESC_MARS < 5.04
    assert 3.37 < V_LMO < 3.40

    MU_MOON = 4902.80  # km^3/s^2
    R_MOON = 1737.4  # km
    V_ESC_MOON = math.sqrt(2.0 * MU_MOON / R_MOON)  # 2.376 km/s
    assert 2.37 < V_ESC_MOON < 2.39

    # Heliocentric Earth-Mars Hohmann transfer constants
    R_E_AU = 1.0000
    R_M_AU = 1.5237
    T_E_DAYS = 365.256
    T_M_DAYS = T_E_DAYS * (R_M_AU ** 1.5)  # 686.98 days
    T_SYN_DAYS = 1.0 / (1.0 / T_E_DAYS - 1.0 / T_M_DAYS)  # 779.9 days (~25.6 months)
    A_TRANS_AU = 0.5 * (R_E_AU + R_M_AU)  # 1.26185 AU
    T_TRANS_DAYS = 0.5 * T_E_DAYS * (A_TRANS_AU ** 1.5)  # 258.9 days (~8.5 months)

    # Phase angles for round-trip Hohmann transfer
    # Outbound: Mars travels omega_M * T_trans = 135.7 deg -> Mars leads Earth by 44.3 deg at departure
    MARS_SWEEP_DEG = 360.0 * (T_TRANS_DAYS / T_M_DAYS)  # 135.67 deg
    PHI_DEP_DEG = 180.0 - MARS_SWEEP_DEG  # 44.33 deg
    EARTH_SWEEP_DEG = 360.0 * (T_TRANS_DAYS / T_E_DAYS)  # 255.16 deg
    # At Mars arrival, Earth is ahead of Mars by (EARTH_SWEEP - 180) = +75.16 deg!
    # Return Hohmann requires Earth to be behind Mars by -75.16 deg (i.e. +284.84 deg ahead)
    WAIT_LAP_DEG = 360.0 - 2.0 * (EARTH_SWEEP_DEG - 180.0)  # 209.68 deg
    OMEGA_REL_DEG_DAY = 360.0 / T_E_DAYS - 360.0 / T_M_DAYS  # 0.4616 deg/day
    T_WAIT_DAYS = WAIT_LAP_DEG / OMEGA_REL_DEG_DAY  # 454.3 days (~15 months)
    assert 778.0 < T_SYN_DAYS < 782.0
    assert 258.0 < T_TRANS_DAYS < 260.0
    assert 452.0 < T_WAIT_DAYS < 457.0

    EXTRA_ARR = f"""
    <marker id="msr-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="{BLUE}"/>
    </marker>
    <marker id="msr-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="{ORANGE}"/>
    </marker>
    <marker id="msr-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="{GREEN}"/>
    </marker>
    <marker id="msr-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="{PURPLE}"/>
    </marker>
    """

    # 1. Escape Velocity & Tsiolkovsky Exponential Mass Pyramid (Asteroid / Phobos / Moon vs Mars)
    def _build_delta_v_and_mass_pyramid():
        # Verify Tsiolkovsky propellant ratios for Isp = 285 s (ve = 2.795 km/s)
        ve_solid = 285.0 * G0  # 2.795 km/s
        mr_moon_asc = math.exp(1.85 / 3.05)  # NTO/MMH ve~3.05 km/s -> 1.83
        mr_mars_asc = math.exp(4.10 / ve_solid)  # 4.34 (ideal) -> ~40.9 with 2-stage inert structure (450 kg / 11 kg)!
        mr_mars_direct = math.exp(6.30 / ve_solid)  # 9.53 (ideal)
        assert 1.80 < mr_moon_asc < 1.90
        assert 4.30 < mr_mars_asc < 4.40
        assert 9.45 < mr_mars_direct < 9.60

        els = header(
            "为什么月球和小行星都能采样回家，火星返程却像隔着一道指数高墙？",
            "左：四类天体逃逸速度与返程 Δv 硬账本｜右：齐奥尔科夫斯基公式下的“百万倍齿轮放大金字塔”",
        )

        # Left Panel: 4-Body Escape & Return Delta-v Comparison
        els.append(card(20, 62, 354, 412))
        els.append(txt(36, 84, "① 逃逸速度差一倍多，返程总 Δv 翻至 6.3 km/s", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "井深正比于 v_esc²：火星引力井深度是月球的 4.5 倍！", 10.2, MUTED))

        bodies = [
            ("小行星龙宫/贝努", "已返回", "v_esc ≈ 0.0002 km/s", 0.02, 0.0, "触碰喷气即走 (Δv < 1 m/s)", GREEN),
            ("火卫一 Phobos", "2026已发", "v_esc ≈ 0.011 km/s", 0.05, 0.95, "百米冲刺即逃，仅需母船返地", PURPLE),
            ("月球（嫦娥五/六）", "已返回", f"v_esc = {V_ESC_MOON:.2f} km/s", 1.85, 0.85, "升空 1.85 + 环月返地 0.85", BLUE),
            ("火星表面（难关！）", "至今 0 克", f"v_esc = {V_ESC_MARS:.2f} km/s", 4.10, 2.20, "升空 4.10 + 火轨返地 2.20", ORANGE),
        ]

        bx0 = 40.0
        max_w = 196.0
        dv_scale_max = 6.50  # km/s
        for idx, (b_name, status_tag, vesc_str, dv_asc, dv_tei, sub_note, col) in enumerate(bodies):
            ry = 122.0 + idx * 78.0
            els.append(card(34, ry, 326, 68, rx=7, fill="#f8fafc" if idx < 3 else ORANGE_SOFT, stroke=BORDER if idx < 3 else ORANGE))
            els.append(txt(46, ry + 18, b_name, 10.4, INK if idx < 3 else ORANGE, weight="700"))
            els.append(txt(186, ry + 18, vesc_str, 9.6, col, weight="700"))
            els.append(pill(284, ry + 5, status_tag, fg=col, bg="#ffffff", w=66, h=18, size=9.1))

            w_asc = max(3.0, (dv_asc / dv_scale_max) * max_w)
            w_tei = (dv_tei / dv_scale_max) * max_w
            els.append(f'<rect x="{bx0:.1f}" y="{ry + 27:.1f}" width="{w_asc:.1f}" height="14" rx="3" fill="{col}"/>')
            if w_tei > 1.0:
                els.append(f'<rect x="{bx0 + w_asc + 2:.1f}" y="{ry + 27:.1f}" width="{w_tei:.1f}" height="14" rx="3" fill="{col}" fill-opacity="0.45" stroke="{col}" stroke-width="1.0"/>')
            tot_dv = dv_asc + dv_tei
            lbl_tot = "< 0.01 km/s" if idx == 0 else f"总 Δv ≈ {tot_dv:.2f} km/s"
            els.append(txt(bx0 + w_asc + w_tei + 8.0, ry + 38, lbl_tot, 9.5, col, weight="700"))
            els.append(txt(46, ry + 57, sub_note, 9.3, BODY if idx == 3 else MUTED))

        els.append(txt(36, 444, "• 实心段 = 表面起飞入轨 Δv；浅色段 = 环绕轨道加速返地 Δv", 9.5, MUTED))
        els.append(txt(36, 461, "• 火面还多一层稀薄大气阻力 + 重力损耗（比理论圆轨速度多烧 ~0.7 km/s）", 9.4, ORANGE, weight="600"))

        # Right Panel: Why Direct Return Blows Up vs MOR Mass Pyramid
        els.append(card(388, 62, 352, 412))
        els.append(txt(404, 84, "② 指数级质量齿轮：0.5 kg 火星土背后的百万倍托举", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "m₀/m_f = e^(Δv/v_e)：每一级都在给上一级的燃料买单！", 10.2, MUTED))

        # Top sub-box: Why NOT direct Mars-surface-to-Earth?
        els.append(card(402, 114, 324, 78, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(414, 132, "为什么不敢像早期苏联月球探测器那样“火面直飞地球”？", 9.8, PURPLE, weight="700"))
        els.append(txt(414, 150, "• 直飞需火面火箭独自扛满 ~6.3 km/s，还要顶 90 kg 防热舱起飞；", 9.2, BODY))
        els.append(txt(414, 167, "• 光火面上升火箭就暴涨至 ~3 吨，连带着陆系统突破 10 吨级——", 9.2, BODY))
        els.append(txt(414, 184, "  彻底超出人类现有火星着陆能力！唯有用“火星轨道交会”拆单。", 9.3, PURPLE, weight="700"))

        # Mass Pyramid (5 stepped tiers wide enough to enclose every label cleanly!)
        tiers = [
            ("⑤ 最终到手的火星岩芯样品", "~0.5 kg", "约 30 管（一瓶矿泉水重）", 204, GREEN, GREEN_SOFT),
            ("④ 环火轨道样品球 (OS)", "11 kg", "钛管 + 密封球壳（排球大小）", 232, BLUE, BLUE_SOFT),
            ("③ 火星上升火箭 (MAV)", "450 kg", "两级固体火箭（放大 41 倍）", 262, ORANGE, ORANGE_SOFT),
            ("② 火星样品回收着陆器 (SRL)", "3,375 kg", "含保温舱+弹射架+机械臂", 292, PURPLE, PURPLE_SOFT),
            ("① 地球起飞两发重型运载火箭", "~800–1,600 吨", "如两发长征五号 / 重型火箭接力", 322, SLATE, SLATE_SOFT),
        ]

        cx_pyr = 564.0
        for t_idx, (t_title, t_mass, t_sub, w_box, stroke_c, fill_c) in enumerate(tiers):
            ty = 204.0 + t_idx * 47.0
            rx_left = cx_pyr - w_box / 2.0
            els.append(f'<rect x="{rx_left:.1f}" y="{ty:.1f}" width="{w_box:.1f}" height="40" rx="6" fill="{fill_c}" stroke="{stroke_c}" stroke-width="1.5"/>')
            els.append(txt(cx_pyr, ty + 16, f"{t_title}：{t_mass}", 9.3, stroke_c if stroke_c != SLATE else INK, "middle", weight="700"))
            els.append(txt(cx_pyr, ty + 32, t_sub, 8.9, BODY, "middle"))

        els.append(txt(564, 456, "总杠杆比：地球点火超百万公斤燃料，只为换回火星半公斤石头！", 9.7, ORANGE, "middle", weight="700"))

        return figure(
            490,
            "月球小行星与火星采样返回速度增量对比及齐奥尔科夫斯基火箭质量放大金字塔图",
            "左图对比小行星贝努/龙宫、火卫一Phobos、月球（嫦娥五号/六号）与火星表面的逃逸速度和返程总Δv（火星高达约6.3 km/s）；右图解释为何火面直飞地球质量失控，并按NASA/ESA与天问三号量级绘出从0.5公斤样品到11公斤样品球、450公斤火星上升火箭、3375公斤着陆器及地球千吨级重型火箭的五级质量金字塔。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 2. Mars's "1% Atmosphere Curse" & 3.38-Ton Heavy Rocket-Lander EDL
    def _build_mars_edl_curse():
        # Verify atmospheric pressure & density ratios
        p_earth_pa = 101325.0
        p_mars_pa = 610.0
        p_ratio_pct = (p_mars_pa / p_earth_pa) * 100.0  # 0.602%
        assert 0.55 < p_ratio_pct < 0.65

        els = header(
            "火星“1% 大气魔咒”：为什么把一枚满油火箭完好放上火星就快把工程师逼疯？",
            "左：610 帕稀薄大气“烧得着却刹不住”的双重惩罚｜右：着陆质量从毅力号 1.03 吨暴涨到 3.38 吨",
        )

        # Left Panel: The 1% Atmosphere EDL Descent Profile
        els.append(card(20, 62, 360, 404))
        els.append(txt(36, 84, "① 地球 0.6% 气压：最坏的两头凑齐了", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "月球真空只需反推；地球稠密可靠大伞；唯有火星两样全得背！", 9.9, MUTED))

        # Vertical altitude profile box (125 km -> 0 km)
        els.append(card(36, 114, 328, 276, rx=8, fill="#f8fafc", stroke=BORDER))

        stages_edl = [
            (126, "125 km 大气层顶：v ≈ 5.5–7.3 km/s 冲入", "激波压缩 CO₂ 产生 ~1,500 °C 等离子火球 → 必背沉重防热大底！", ORANGE, ORANGE_SOFT),
            (194, "11 km 超音速开伞：21.5 米巨伞也刹不住", "空气密度仅地球 ~1/80，开伞后仍以 >300 km/h 狂砸 → 单靠伞必碎！", PURPLE, PURPLE_SOFT),
            (262, "2 km 抛伞点反推：全靠火箭硬刹 + 雷达避障", "点燃多台反推发动机悬停找平地，还要扛住 ~15g 过载不震裂固体药柱", BLUE, BLUE_SOFT),
            (330, "全程“恐怖 7 分钟”：单程光行延迟 3–22 分钟", "地球收到“进入大气”信号时，着陆器其实早在十几分钟前就已成败落定", GREEN, GREEN_SOFT),
        ]
        for idx_s, (sy, s_head, s_desc, s_col, s_bg) in enumerate(stages_edl):
            els.append(f'<rect x="44" y="{sy}" width="312" height="56" rx="6" fill="{s_bg}" stroke="{s_col}" stroke-width="1.3"/>')
            els.append(txt(54, sy + 20, f"阶段 {idx_s + 1}｜{s_head}", 9.6, s_col, weight="700"))
            els.append(txt(54, sy + 40, s_desc, 8.9, BODY))
            if idx_s < 3:
                els.append(f'<line x1="200" y1="{sy + 56}" x2="200" y2="{sy + 68}" stroke="{SLATE}" stroke-width="1.6" marker-end="url(#msr-blue)"/>')

        els.append(txt(36, 414, "• 阻力公式 F_D = ½ ρ v² C_D A：火星地表 ρ ≈ 0.02 kg/m³（地球 1.225）", 9.5, INK, weight="600"))
        els.append(txt(36, 434, "• 同样面积的降落伞，要在火星攒够升力，下落速度必须比地球快 ~8 倍！", 9.5, ORANGE, weight="700"))
        els.append(txt(36, 452, "• 着陆器越重（质量 ∝ L³），伞面积（∝ L²）越不够用，超音速减速呈非线性恶化。", 9.3, MUTED))

        # Right Panel: Historical Mars Landed Mass Bar Chart vs SRL 3,375 kg
        els.append(card(394, 62, 346, 404))
        els.append(txt(410, 84, "② 历史火星着陆器体重榜：一步跨上 3 倍台阶", PANEL_TITLE, INK, weight="700"))
        els.append(txt(410, 102, "过去送的是“相机化验车”，这次送的是“满油火箭发射场”", 9.9, MUTED))

        landers = [
            ("旅居者号 (1997)", 11.5, "微型巡视器", SLATE),
            ("机遇/勇气号 (2004)", 185.0, "气囊弹跳着陆", SLATE),
            ("好奇号 (2012)", 899.0, "首创天空起重机", BLUE),
            ("毅力号 (2021 纪录)", 1025.0, "现役最重火星车", BLUE),
            ("祝融号+着陆平台 (2021)", 1285.0, "防热伞降+反推悬停", GREEN),
            ("MSR 样品回收着陆器", 3375.0, "宽 7.7 m！背 450 kg 火箭", ORANGE),
        ]

        bar_x0 = 544.0
        max_lw = 176.0
        m_cap = 3600.0
        for l_idx, (l_name, l_mass, l_note, l_col) in enumerate(landers):
            ly = 126.0 + l_idx * 44.0
            bw = max(3.0, (l_mass / m_cap) * max_lw)
            is_srl = l_mass > 3000.0
            els.append(txt(536, ly + 13, l_name, 9.7, ORANGE if is_srl else BODY, "end", weight="700" if is_srl else "400"))
            els.append(
                f'<rect x="{bar_x0:.1f}" y="{ly:.1f}" width="{bw:.1f}" height="19" rx="4" '
                f'fill="{l_col}" fill-opacity="{"0.28" if is_srl else "0.16"}" stroke="{l_col}" stroke-width="{"1.8" if is_srl else "1.2"}"/>'
            )
            lbl_x = bar_x0 + bw + 6.0 if bw < 115.0 else bar_x0 + bw - 6.0
            lbl_anc = "start" if bw < 115.0 else "end"
            els.append(txt(lbl_x, ly + 13.5, f"{l_mass:,.0f} kg", 9.5, l_col if bw < 115.0 else INK, lbl_anc, weight="700"))
            els.append(txt(544, ly + 32, l_note, 8.9, MUTED))

        # Breakdown box at bottom of Right Card
        els.append(card(408, 392, 318, 60, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(420, 411, "为什么样品着陆器高达 3,375 kg（毅力号的 3.3 倍）？", 9.7, ORANGE, weight="700"))
        els.append(txt(420, 429, "450 kg 上升火箭 + 恒温防冻圆顶舱 + VECTOR 抛射架 +", 9.3, BODY))
        els.append(txt(420, 445, "2 米装管机械臂 + 大推力着陆反推燃料与吸能缓冲腿！", 9.3, BODY))

        return figure(
            482,
            "火星百分之一稀薄大气着陆双重困境与3375公斤样品回收着陆器质量对比图",
            "左图按高度拆解火星大气进入、下降与着陆（EDL）四阶段：610帕大气既产生约1500摄氏度高超声速气动加热，又令21.5米巨伞终端速度仍超300 km/h而必须叠加反推火箭；右图对比1997旅居者号至2021毅力号（1025 kg）、祝融号组合体与MSR样品回收着陆器（3375 kg）的质量跨越。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 3. Alien Launchpad at -80 °C & VECTOR Mid-Air Mortar Toss Ignition
    def _build_mav_vector_launch():
        els = header(
            "没有发射塔、零下 80°C 极寒荒原：人类第一枚异星火箭怎样“半空抛射点火”？",
            "按 ① 机械臂装管 → ② 保温舱熬过极夜 → ③ VECTOR 弹簧抛高 → ④ 凌空点火两级入轨 四步拆解",
        )

        # Top Wide Trajectory & Step Arena (taller so graphics sit cleanly below step captions)
        els.append(card(20, 62, 720, 314))
        els.append(txt(36, 84, "火星上升器（MAV：长 3.0 m × 直径 0.5 m，地球重 450 kg / 火星重约 170 kgf）无塔台发射全流程", PANEL_TITLE, INK, weight="700"))

        # Martian ground slope curve along bottom of arena
        els.append(f'<path d="M 32,338 Q 220,324 430,336 T 728,332 L 728,364 L 32,364 Z" fill="#fed7aa" fill-opacity="0.45" stroke="{ORANGE}" stroke-width="1.4"/>')
        els.append(txt(626, 353, "杰泽罗陨石坑地表（允许着陆器倾斜达 ~15°）", 9.3, ORANGE, "middle", weight="600"))

        # Step 1 & 2 (Left x=44..245): Lander Deck + Thermal Igloo + Robotic Arm Loading Tubes
        els.append(f'<line x1="92" y1="312" x2="74" y2="334" stroke="{SLATE}" stroke-width="3.0"/>')
        els.append(f'<line x1="208" y1="312" x2="226" y2="332" stroke="{SLATE}" stroke-width="3.0"/>')
        els.append(f'<rect x="78" y="296" width="144" height="16" rx="4" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.8"/>')
        els.append(
            f'<g transform="translate(152,294) rotate(-55)">'
            f'<rect x="0" y="-12" width="90" height="24" rx="6" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="4 2"/>'
            f'<rect x="6" y="-7" width="76" height="14" rx="3" fill="#ffffff" stroke="{INK}" stroke-width="1.5"/>'
            f'<circle cx="78" cy="0" r="5.5" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.5"/>'
            f'</g>'
        )
        els.append(f'<polyline points="96,296 92,246 168,220" fill="none" stroke="{PURPLE}" stroke-width="2.5"/>')
        els.append(f'<circle cx="92" cy="246" r="3.6" fill="{PURPLE}"/>')

        els.append(step_badge(52, 114, 1, PURPLE))
        els.append(txt(70, 118, "2 米机械臂盲装 30 根钛管", 9.9, PURPLE, weight="700"))
        els.append(txt(70, 134, "塞入火箭鼻锥 11 kg 样品球", 9.2, BODY))

        els.append(step_badge(52, 158, 2, BLUE))
        els.append(txt(70, 162, "恒温防护圆筒熬过 −80 °C", 9.9, BLUE, weight="700"))
        els.append(txt(70, 178, "防固体药柱低于 −40 °C 冻裂", 9.2, BODY))

        # Step 3 (Middle x=275..465): VECTOR Toss into Mid-Air BEFORE Ignition!
        els.append(f'<line x1="306" y1="314" x2="292" y2="332" stroke="{SLATE}" stroke-width="2.6"/>')
        els.append(f'<line x1="394" y1="314" x2="408" y2="334" stroke="{SLATE}" stroke-width="2.6"/>')
        els.append(f'<rect x="298" y="300" width="104" height="14" rx="3" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.5"/>')
        els.append(f'<line x1="340" y1="298" x2="354" y2="254" stroke="{GREEN}" stroke-width="2.0" stroke-dasharray="4 2" marker-end="url(#msr-green)"/>')
        els.append(f'<line x1="358" y1="298" x2="372" y2="258" stroke="{GREEN}" stroke-width="2.0" stroke-dasharray="4 2" marker-end="url(#msr-green)"/>')

        els.append(
            f'<g transform="translate(382,222) rotate(-50)">'
            f'<rect x="-34" y="-7.5" width="72" height="15" rx="3" fill="#ffffff" stroke="{ORANGE}" stroke-width="1.8"/>'
            f'<polygon points="38,-7.5 51,0 38,7.5" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>'
            f'<polygon points="-34,-5 -58,-11 -45,0 -58,11 -34,5" fill="#fb923c" fill-opacity="0.85"/>'
            f'</g>'
        )
        els.append(step_badge(282, 114, 3, GREEN))
        els.append(txt(300, 118, "VECTOR 弹射：先当炮弹抛上天！", 9.9, GREEN, weight="700"))
        els.append(txt(300, 134, "弹簧作动器将整枚火箭抛离甲板数米", 9.2, BODY))
        els.append(txt(300, 150, "赋予精确初始抬头角，避开斜坡与尾焰", 9.2, BODY))

        # Step 4 (Right x=485..715): Mid-Air Ignition -> Stage 1/2 Separation -> 350 km LMO at ~4.0 km/s
        els.append(f'<path d="M 418,192 Q 528,118 664,120" fill="none" stroke="{ORANGE}" stroke-width="2.6" marker-end="url(#msr-orange)"/>')
        els.append(f'<circle cx="536" cy="136" r="4.5" fill="#ffffff" stroke="{ORANGE}" stroke-width="2.2"/>')
        els.append(txt(536, 118, "一二级分离 + 摆动喷管稳姿", 9.3, ORANGE, "middle", weight="700"))

        els.append(f'<circle cx="684" cy="120" r="11" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2.0"/>')
        els.append(txt(684, 124, "OS", 9.2, GREEN, "middle", weight="700"))
        els.append(txt(664, 150, "~10 分钟加速至 4.0 km/s", 9.5, GREEN, "middle", weight="700"))
        els.append(txt(664, 166, "送入 ~350 km 环火轨道", 9.3, BODY, "middle"))

        els.append(step_badge(494, 202, 4, ORANGE))
        els.append(txt(512, 206, "悬空点火 + 100% 全自主入轨", 9.9, ORANGE, weight="700"))
        els.append(txt(512, 224, "• 无尾翼细长弹体气动不稳定，靠喷管摆动硬控", 9.2, BODY))
        els.append(txt(512, 241, "• 无线电单程慢达 22 分钟，点火分秒全靠自算！", 9.2, BODY))
        els.append(txt(512, 258, "• 无水泥导流槽，若甲板直接点火尾焰必掀翻自身", 9.2, ORANGE, weight="600"))

        # Bottom Comparison Strip: Earth Launch Complex vs Mars Bare-Bones Launch
        els.append(card(20, 390, 352, 92, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(36, 411, "对比地球发射场（几千人团队伺候一枚火箭）：", 10.0, BLUE, weight="700"))
        els.append(txt(36, 431, "• 百米脐带塔持续补液氧、调温、供电，导流槽喷百吨水降温；", 9.3, BODY))
        els.append(txt(36, 450, "• 气象雷达盯高空切变风，稍有异常随时叫停倒计时；", 9.3, BODY))
        els.append(txt(36, 468, "• 地面控制室毫秒级遥测闭环监控。", 9.3, BODY))

        els.append(card(388, 390, 352, 92, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(404, 411, "对比火星荒原发射（零塔架、零地勤、零实时遥控）：", 10.0, ORANGE, weight="700"))
        els.append(txt(404, 431, "• 燃料在地球灌满后封死飞 8 个月，再挨过火星极寒与沙尘暴；", 9.3, BODY))
        els.append(txt(404, 450, "• 斜坡甲板弹簧抛射半空点火，全程只有一次开火机会；", 9.3, BODY))
        els.append(txt(404, 468, "• 这是人类航天史上从未在任何行星表面实战过的动作！", 9.3, ORANGE, weight="700"))

        return figure(
            498,
            "火星上升器MAV零下80摄氏度恒温防护与VECTOR半空抛射凌空点火四步图解",
            "上图按①2米机械臂装填30根钛合金样品管、②恒温圆筒抵御零下80摄氏度火星寒夜防止固体推进剂开裂、③VECTOR弹射系统将450公斤火箭抛至半空避免尾焰毁坏斜坡着陆器、④半空点火经10分钟加速至4 km/s送入350公里环火轨道四步拆解；下图对比地球发射场与火星荒原零保障起飞条件。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 4. 26-Month Synodic Window, 454-Day Forced Wait (Animated) & Autonomous Orbital Capture
    def _build_synodic_window_and_rendezvous():
        els = header(
            "错过一班再等 26 个月，到了还得苦等 15 个月！地火往返天体时刻表与盲抓样品球",
            f"左：霍曼去程 {T_TRANS_DAYS:.0f} 天 + 被迫等位 {T_WAIT_DAYS:.0f} 天 + 返程 {T_TRANS_DAYS:.0f} 天动画｜右：上亿公里外自主抓 23 cm 小球",
        )

        els.append(card(20, 62, 366, 426))
        els.append(txt(36, 84, f"① 为什么到了火星不能马上回？（会合周期 {T_SYN_DAYS:.0f} 天）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "内圈地球跑得快：等你飞到火星，地球早已甩到前方 +75.2°！", 9.7, MUTED))

        scx, scy = 208.0, 252.0
        px_per_au = 72.0
        r_e_px = R_E_AU * px_per_au  # 72.0 px
        r_m_px = R_M_AU * px_per_au  # 109.7 px

        els.append(f'<circle cx="{scx:.1f}" cy="{scy:.1f}" r="{r_m_px:.1f}" fill="none" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(f'<circle cx="{scx:.1f}" cy="{scy:.1f}" r="{r_e_px:.1f}" fill="none" stroke="{BLUE_LINE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(f'<circle cx="{scx:.1f}" cy="{scy:.1f}" r="11" fill="#fef08a" stroke="#ca8a04" stroke-width="1.6"/>')
        els.append(txt(scx, scy + 3.5, "太阳", 8.8, "#a16207", "middle", weight="700"))

        a_px = 0.5 * (r_e_px + r_m_px)
        c_px = a_px - r_e_px
        b_px = math.sqrt(a_px ** 2 - c_px ** 2)

        out_pts = []
        for k in range(61):
            u = math.pi * k / 60.0
            px = scx + b_px * math.sin(u)
            py = (scy - c_px) + a_px * math.cos(u)
            out_pts.append((px, py))
        out_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in out_pts)
        els.append(f'<path d="{out_d}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')

        wait_pts = []
        th_arr = 90.0
        dth_wait = 360.0 * (T_WAIT_DAYS / T_M_DAYS)
        for k in range(49):
            ang = math.radians(th_arr + dth_wait * k / 48.0)
            wait_pts.append((scx + r_m_px * math.cos(ang), scy - r_m_px * math.sin(ang)))
        wait_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in wait_pts)
        els.append(f'<path d="{wait_d}" fill="none" stroke="{PURPLE}" stroke-width="2.4" stroke-dasharray="5 3"/>')

        th_dep2 = math.radians(th_arr + dth_wait)
        ux_p = -math.cos(th_dep2)
        uy_p = math.sin(th_dep2)
        tx_ccw = -math.sin(th_dep2)
        ty_ccw = -math.cos(th_dep2)
        in_pts = []
        for k in range(61):
            u = math.pi - math.pi * k / 60.0
            cx_in = scx - c_px * ux_p
            cy_in = scy - c_px * uy_p
            px = cx_in + a_px * math.cos(u) * ux_p + b_px * math.sin(u) * tx_ccw
            py = cy_in + a_px * math.cos(u) * uy_p + b_px * math.sin(u) * ty_ccw
            in_pts.append((px, py))
        in_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in in_pts)
        els.append(f'<path d="{in_d}" fill="none" stroke="{GREEN}" stroke-width="2.3"/>')

        e0_x, e0_y = out_pts[0]
        els.append(f'<circle cx="{e0_x:.1f}" cy="{e0_y:.1f}" r="5.0" fill="{BLUE}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(e0_x, e0_y + 20, "① 地球出发 (t=0)", 9.2, BLUE, "middle", weight="700", halo=True))

        m1_x, m1_y = out_pts[-1]
        els.append(f'<circle cx="{m1_x:.1f}" cy="{m1_y:.1f}" r="5.2" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(m1_x + 8, m1_y - 10, f"② 抵火 ({T_TRANS_DAYS:.0f}天)", 9.2, ORANGE, "start", weight="700", halo=True))

        th_e1 = math.radians(-90.0 + EARTH_SWEEP_DEG)
        e1_x = scx + r_e_px * math.cos(th_e1)
        e1_y = scy - r_e_px * math.sin(th_e1)
        els.append(f'<circle cx="{e1_x:.1f}" cy="{e1_y:.1f}" r="4.0" fill="#ffffff" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(f'<line x1="{e1_x - 3:.1f}" y1="{e1_y + 3:.1f}" x2="{e1_x - 16:.1f}" y2="{e1_y + 24:.1f}" stroke="{BLUE}" stroke-width="1.1"/>')
        els.append(txt(34, e1_y + 36, "抵火时地球已超前+75°", 8.9, BLUE, "start", weight="600", halo=True))

        m2_x, m2_y = wait_pts[-1]
        els.append(f'<circle cx="{m2_x:.1f}" cy="{m2_y:.1f}" r="5.0" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(m2_x - 4, m2_y + 20, f"③ 等满{T_WAIT_DAYS:.0f}天返航", 9.1, PURPLE, "middle", weight="700", halo=True))

        e2_x, e2_y = in_pts[-1]
        els.append(f'<circle cx="{e2_x:.1f}" cy="{e2_y:.1f}" r="5.0" fill="{GREEN}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(f'<line x1="{e2_x - 3:.1f}" y1="{e2_y - 3:.1f}" x2="{e2_x - 16:.1f}" y2="{e2_y - 24:.1f}" stroke="{GREEN}" stroke-width="1.1"/>')
        els.append(txt(34, e2_y - 28, "④ 返抵地球 (~972天)", 9.1, GREEN, "start", weight="700", halo=True))

        seg_out = out_pts[::3]
        seg_wait = wait_pts[1::2]
        seg_in = in_pts[1::3]
        full_pts = seg_out + seg_wait + seg_in

        def _arc_len(pts):
            return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))

        len_out = _arc_len(seg_out)
        len_wait = _arc_len([seg_out[-1]] + seg_wait)
        len_in = _arc_len([seg_wait[-1]] + seg_in)
        len_tot = len_out + len_wait + len_in
        d1_pct = 100.0 * len_out / len_tot
        d2_pct = 100.0 * (len_out + len_wait) / len_tot
        t_tot_days = 2.0 * T_TRANS_DAYS + T_WAIT_DAYS
        k1_pct = 100.0 * T_TRANS_DAYS / t_tot_days
        k2_pct = 100.0 * (T_TRANS_DAYS + T_WAIT_DAYS) / t_tot_days

        full_motion_path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in full_pts)
        anim_css = f"""
        .msr-ship {{
          offset-path: path('{full_motion_path}');
          offset-distance: 100%;
          animation: msr-roundtrip 9.0s linear 1 forwards;
        }}
        @keyframes msr-roundtrip {{
          0%            {{ offset-distance: 0%; }}
          {k1_pct:.2f}% {{ offset-distance: {d1_pct:.2f}%; }}
          {k2_pct:.2f}% {{ offset-distance: {d2_pct:.2f}%; }}
          100%          {{ offset-distance: 100%; }}
        }}
        @media (prefers-reduced-motion: reduce) {{
          .msr-ship {{ animation: none; offset-distance: 100%; }}
        }}
        """
        els.append(f'<circle class="msr-ship" cx="0" cy="0" r="6.0" fill="{ORANGE}" stroke="#ffffff" stroke-width="2.0"/>')

        els.append(card(34, 396, 338, 78, rx=7, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 415, f"往返总耗时账单：{T_TRANS_DAYS:.0f}d 去（蓝）+ {T_WAIT_DAYS:.0f}d 等（紫虚）+ {T_TRANS_DAYS:.0f}d 回（绿）≈ 2.7 年", 9.2, INK, weight="700"))
        els.append(txt(46, 434, f"• 会合周期 T_syn = 1/(1/365.26 − 1/686.98) = {T_SYN_DAYS:.0f} 天（约 26 个月才开一扇窗）", 9.0, BODY))
        els.append(txt(46, 452, "• 任何环节晚半个月赶不上窗口，整套系统就得在太空或地面硬扛两年多！", 9.0, ORANGE, weight="600"))

        els.append(card(398, 62, 342, 426))
        els.append(txt(414, 84, "② 环火轨道“大海捞针”：盲抓一只 23 cm 排球", PANEL_TITLE, INK, weight="700"))
        els.append(txt(414, 102, "样品球没发动机也没信标天线，全靠母船光学与激光自寻的！", 9.7, MUTED))

        els.append(card(412, 116, 314, 200, rx=8, fill="#0f172a", stroke=SLATE))
        els.append(f'<path d="M 412,294 Q 569,254 726,294 L 726,316 L 412,316 Z" fill="#9a3412" fill-opacity="0.75" stroke="#fb923c" stroke-width="1.3"/>')
        els.append(txt(569, 307, "火星 350 km 低轨道（轨速 ~3.4 km/s，每 ~115 分钟绕一圈）", 8.9, "#fed7aa", "middle", weight="600"))

        els.append(f'<line x1="444" y1="158" x2="444" y2="236" stroke="#60a5fa" stroke-width="5.0"/>')
        els.append(f'<rect x="434" y="186" width="24" height="22" rx="3" fill="#e2e8f0" stroke="#93c5fd" stroke-width="1.5"/>')
        els.append(txt(424, 136, "返地轨道器 (7 吨 / 翼展 38 m)", 9.1, "#93c5fd", "start", weight="700"))

        els.append(f'<polygon points="458,197 678,170 678,224" fill="#38bdf8" fill-opacity="0.16" stroke="#38bdf8" stroke-width="1.1" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="458" y1="197" x2="672" y2="197" stroke="#4ade80" stroke-width="1.8" stroke-dasharray="3 2"/>')
        els.append(f'<circle cx="682" cy="197" r="7.0" fill="#fde047" stroke="#ffffff" stroke-width="1.6"/>')
        els.append(txt(682, 160, "样品球 OS", 9.2, "#fde047", "middle", weight="700"))
        els.append(txt(682, 240, "Ø 23 cm / 11 kg", 8.9, "#f8fafc", "middle"))

        els.append(txt(556, 156, "① >1,000 km 相机搜反光星点", 9.0, "#bae6fd", "middle", weight="600"))
        els.append(txt(552, 240, "② 近距 LiDAR 锁死相对位姿", 9.0, "#86efac", "middle", weight="600"))

        els.append(card(412, 330, 314, 144, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(424, 350, "为什么环火交会比嫦娥五号/六号环月交会还要凶险？", 9.8, BLUE, weight="700"))
        els.append(txt(424, 370, "• 距离远百倍以上：地月仅 38 万 km（延迟 1.3 秒，地面可兜底）；", 9.1, BODY))
        els.append(txt(424, 388, "  地火隔 5,500 万～4 亿 km，单程延迟达 22 分钟，零人工介入！", 9.1, ORANGE, weight="700"))
        els.append(txt(424, 407, "• 被动非合作目标：样品球为省重不带推进器与主动雷达应答机，", 9.1, BODY))
        els.append(txt(424, 425, "  万一上升器入轨偏差稍大，7 吨母船必须在茫茫火轨自己找回它；", 9.1, BODY))
        els.append(txt(424, 443, "• 天问三号则兼顾主动微波/激光导引交会，力求压缩捕获风险。", 9.1, GREEN, weight="700"))

        return figure(
            504,
            "地火霍曼往返26个月会合窗口与454天被迫等待轨道动画及环火轨道自主捕获23厘米样品球图解",
            "左图按精确开普勒轨道计算地火去程259天、火星表面或轨道等待454天（因抵达火星时地球已超前75.2度）、返程259天的完整972天往返轨迹并配单次播放动画；右图展示返地轨道器在单程最长达22分钟通信延迟下，用超过1000公里光学相机和激光雷达自主搜寻捕获直径23厘米无动力样品球的过程。",
            els,
            extra_css=anim_css,
            extra_defs=EXTRA_ARR,
        )

    # 5. COSPAR Category V "Break the Chain", Parachute-Free 12 km/s Earth Entry & Global Status
    def _build_break_chain_and_roadmap():
        els = header(
            "第五道鬼门关：“断链防疫”锁死百万分之一泄漏率、无伞硬砸地球与全球路线大比拼",
            "上：COSPAR 第 V 类受限返回“切断接触链”与无伞再入｜下：为什么美欧暂缓，中国天问三号 2028 出征？",
        )

        els.append(card(20, 62, 720, 198))
        els.append(txt(36, 84, "① 阿波罗 14 号以来最严生物检疫（COSPAR 第 V 类受限返回）：未受控颗粒泄漏率 < 10⁻⁶！", PANEL_TITLE, INK, weight="700"))

        steps_bio = [
            (
                36,
                "① 危险源：外壁沾有火尘",
                [
                    "样品球在火面装管时，外壁不可",
                    "避免沾染火星尘埃；若直接塞进",
                    "返地舱，火尘可能污染返地舱外",
                    "表面，带回地球大气层。",
                ],
                ORANGE,
                ORANGE_SOFT,
            ),
            (
                214,
                "② 太空“套娃断链”钎焊密封",
                [
                    "在环火轨道用双层隔离舱吞入样",
                    "品球，全自动高温钎焊封死洁净",
                    "内罐并对焊缝灭菌，彻底切断内",
                    "外接触链（Break the Chain）！",
                ],
                PURPLE,
                PURPLE_SOFT,
            ),
            (
                392,
                "③ 距地 3 天放舱·母船永不返",
                [
                    "确认密封完好后，在距地 3 天处",
                    "释放 90 kg 再入舱；轨道母船随",
                    "即点火变轨绕太阳永久飞行，绝",
                    "不把半粒火尘带进地球圈。",
                ],
                BLUE,
                BLUE_SOFT,
            ),
            (
                570,
                "④ ~12 km/s 故意不装降落伞",
                [
                    "吸取“起源号”不开伞摔裂教训，",
                    "直接砍掉降落伞故障点！靠碳酚",
                    "醛防热盾 + 蜂窝吸能材料硬抗着",
                    "陆冲击，直进 BSL-4 超净室。",
                ],
                GREEN,
                GREEN_SOFT,
            ),
        ]

        for s_idx, (sx, s_title, lines, s_col, s_bg) in enumerate(steps_bio):
            w_card = 158 if s_idx < 3 else 154
            els.append(card(sx, 98, w_card, 146, rx=7, fill=s_bg, stroke=s_col))
            els.append(txt(sx + 10, 118, s_title, 9.4, s_col, weight="700"))
            for l_i, line_str in enumerate(lines):
                els.append(txt(sx + 10, 142 + l_i * 20, line_str, 9.0, BODY))
            if s_idx < 3:
                els.append(f'<line x1="{sx + w_card + 2}" y1="170" x2="{sx + w_card + 16}" y2="170" stroke="{s_col}" stroke-width="1.8" marker-end="url(#msr-blue)"/>')

        # Bottom Full-Width Card: 3 Global Approaches Comparison (as of late 2026)
        els.append(card(20, 274, 720, 214))
        els.append(txt(36, 296, "② 现实大结局（截至 2026 年底）：为什么地球有 300 多块火星陨石，人类却还要拼命去挖这半公斤？", PANEL_TITLE, INK, weight="700"))

        cols = [
            (
                36,
                "自然火星陨石（>300 块已捡到）",
                "免费馈赠 · 但丢了关键证据",
                SLATE,
                "#f8fafc",
                [
                    "• 小行星猛烈撞击火星溅射来地",
                    "• 坚硬火成岩幸存，脆弱含水沉积",
                    "  泥岩（最可能藏古生命）全碎毁",
                    "• 不知采自火星哪个坑、哪一层",
                    "• 落地后遭地球微生物与雨水污染",
                ],
            ),
            (
                272,
                "美欧 MSR（2026.01 国会停拨）",
                "科学最精 · 被超长链条拖垮预算",
                ORANGE,
                ORANGE_SOFT,
                [
                    "• 毅力号已钻存 30 管（含豹纹岩）",
                    "• “车+3.4吨着陆器+火箭+7吨母船”",
                    "  多国多中心串联，复杂度失控",
                    "• 预算飙至 80–110 亿美元、2040 归",
                    "• 30 根钛管暂留杰泽罗坑等待新方案",
                ],
            ),
            (
                508,
                "中国天问三号 & 日本 MMX",
                "精简闭环冲刺首返（2028 → 2031）",
                GREEN,
                GREEN_SOFT,
                [
                    "• 日本 MMX（2026.10 升空）：绕开",
                    "  火星深井，只采微重力火卫一",
                    "• 中国天问三号：两发长征五号直奔",
                    "  主题（着上组合体 + 轨返组合体）",
                    "• 钻取+表取+无人机，2031 带回≥500g",
                ],
            ),
        ]

        for cx_c, c_head, c_tag, c_col, c_bg, bullets in cols:
            els.append(card(cx_c, 312, 216, 162, rx=8, fill=c_bg, stroke=c_col))
            els.append(txt(cx_c + 10, 332, c_head, 9.7, c_col if c_col != SLATE else INK, weight="700"))
            els.append(txt(cx_c + 10, 349, c_tag, 9.0, c_col, weight="600"))
            els.append(f'<line x1="{cx_c + 10}" y1="357" x2="{cx_c + 206}" y2="357" stroke="{BORDER}" stroke-width="1.0"/>')
            for b_i, b_line in enumerate(bullets):
                els.append(txt(cx_c + 10, 375 + b_i * 18, b_line, 9.0, BODY))

        return figure(
            504,
            "火星采样返回COSPAR第五类断链生物隔离、无降落伞再入与中美欧日方案进展对比图",
            "上图按四步展示COSPAR第V类受限地球返回的轨道套娃钎焊断链密封（泄漏概率小于百万分之一）、母船绕日隔离与90公斤再入舱约12 km/s无降落伞抗冲击着陆进入BSL-4超净实验室；下图对比地球现有300余块火星陨石的局限、2026年1月因80至110亿美元预算被美国国会停拨的美欧MSR计划，以及2026年10月采样火卫一的日本MMX和计划2028发射2031带回不少于500克火星样品的中国天问三号。",
            els,
            extra_defs=EXTRA_ARR,
        )

    @register("mars-sample-return-challenges", "火星采样返回与行星际往返五大工程物理难关：逃逸速度金字塔、1%大气着陆、VECTOR半空点火、26个月窗口与断链防疫", "mechanics_sky")
    def build_mars_sample_return():
        write_svg(SUBDIR, "moon-asteroid-vs-mars-delta-v-pyramid.svg", _build_delta_v_and_mass_pyramid())
        write_svg(SUBDIR, "mars-one-percent-atmosphere-heavy-edl.svg", _build_mars_edl_curse())
        write_svg(SUBDIR, "mav-cold-storage-and-vector-midair-launch.svg", _build_mav_vector_launch())
        write_svg(SUBDIR, "synodic-window-and-basketball-rendezvous.svg", _build_synodic_window_and_rendezvous())
        write_svg(SUBDIR, "break-the-chain-cat5-and-global-roadmap.svg", _build_break_chain_and_roadmap())


_register_mars_sample_return()


# ---------------------------------------------------------------------------
# SpaceX Starship & Super Heavy Recovery Architecture (starship-recovery)
# ---------------------------------------------------------------------------
def _register_starship_recovery():
    SUBDIR = "starship-recovery"

    G0 = 9.80665
    V_BOOSTER_SEP = 1480.0      # m/s (~5,328 km/h typical RTLS staging speed)
    V_SHIP_ORBIT = 7800.0       # m/s (~28,080 km/h LEO reentry speed)
    V_SHIP_TERM = 80.0          # m/s subsonic horizontal belly-flop terminal speed
    ISP_RVAC = 380.0            # s vacuum Raptor specific impulse
    VE_RVAC = ISP_RVAC * G0     # 3726.53 m/s

    E_BOOSTER_MJ = 0.5 * (V_BOOSTER_SEP ** 2) / 1e6   # 1.0952 MJ/kg
    E_SHIP_MJ = 0.5 * (V_SHIP_ORBIT ** 2) / 1e6       # 30.420 MJ/kg
    ENERGY_RATIO = E_SHIP_MJ / E_BOOSTER_MJ           # 27.776x
    PROP_BRAKE_MR = math.exp(V_SHIP_ORBIT / VE_RVAC)  # 8.109x mass ratio if braking purely by thrust
    AERO_DISSIP_FRAC = 1.0 - (V_SHIP_TERM / V_SHIP_ORBIT) ** 2  # 0.999895 (99.99%)

    # Terminal speed sanity check for horizontal 52.1 m x 9 m cylinder at ~1 km altitude
    m_ship_land = 115000.0  # kg (dry + residual header propellant)
    rho_1km = 1.11          # kg/m^3
    cd_cyl = 1.05
    area_belly = 52.1 * 9.0 * 0.86  # ~403 m^2 effective planform + flaps
    v_term_calc = math.sqrt((2.0 * m_ship_land * G0) / (rho_1km * cd_cyl * area_belly))

    assert 1.05 < E_BOOSTER_MJ < 1.15
    assert 30.3 < E_SHIP_MJ < 30.5
    assert 27.5 < ENERGY_RATIO < 28.1
    assert 8.05 < PROP_BRAKE_MR < 8.20
    assert AERO_DISSIP_FRAC > 0.9998
    assert 65.0 < v_term_calc < 85.0

    EXTRA_ARR = f"""
  <marker id="ss-blue" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{BLUE}"/>
  </marker>
  <marker id="ss-orange" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{ORANGE}"/>
  </marker>
  <marker id="ss-green" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{GREEN}"/>
  </marker>
  <marker id="ss-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{PURPLE}"/>
  </marker>
  <marker id="ss-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#dc2626"/>
  </marker>
  <marker id="ss-slate" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{SLATE}"/>
  </marker>"""

    # 1. 28x Specific Kinetic Energy Gap & Why Chop Off Landing Legs
    def _build_energy_gap_and_no_legs():
        els = header(
            "为什么要砍掉着陆腿？一级与二级差出 28 倍的“刹车账单”",
            "左：比动能 e = ½v² 决定一二级截然不同的减速路线｜右：把缓冲腿搬回地面发射塔的重量账",
        )

        # Left Card: 28x Specific Kinetic Energy Gap
        els.append(card(20, 62, 352, 430))
        els.append(txt(36, 84, "① 速度差 5.3 倍，单位质量动能差 27.8 倍！", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "一级刚出稠密大气便折返；二级必须从第一宇宙速度全身刹停", 10.3, MUTED))

        # Quantitative horizontal bar comparison (0 .. 32 MJ/kg -> 212 px)
        bx0, bw_max = 128.0, 214.0
        e_max = 32.0
        w_b1 = bw_max * (E_BOOSTER_MJ / e_max)   # 7.3 px
        w_s2 = bw_max * (E_SHIP_MJ / e_max)      # 203.4 px

        # Scale ticks
        els.append(f'<line x1="{bx0:.1f}" y1="122" x2="{bx0 + bw_max:.1f}" y2="122" stroke="{HAIRLINE}" stroke-width="1"/>')
        for ev in (0, 10, 20, 30):
            tx = bx0 + bw_max * (ev / e_max)
            els.append(f'<line x1="{tx:.1f}" y1="118" x2="{tx:.1f}" y2="125" stroke="{HAIRLINE}" stroke-width="1"/>')
            els.append(txt(tx, 115, f"{ev}" if ev < 30 else "30 MJ/kg", 9.4, MUTED, "middle"))

        # Row 1: Super Heavy Booster
        els.append(txt(36, 145, "一级超重助推", 10.6, INK, weight="700"))
        els.append(txt(36, 160, "v ≈ 1.48 km/s", 9.6, MUTED))
        els.append(f'<rect x="{bx0:.1f}" y="133" width="{w_b1:.1f}" height="24" rx="4" fill="{BLUE}"/>')
        els.append(txt(bx0 + w_b1 + 8, 149, f"{E_BOOSTER_MJ:.2f} MJ/kg（1× 基准）", 10.4, BLUE, weight="700"))

        # Row 2: Starship Upper Stage
        els.append(txt(36, 196, "二级星舰飞船", 10.6, INK, weight="700"))
        els.append(txt(36, 211, "v ≈ 7.80 km/s", 9.6, MUTED))
        els.append(f'<rect x="{bx0:.1f}" y="182" width="{w_s2:.1f}" height="28" rx="4" fill="{ORANGE}"/>')
        # Tiny green sliver at right tip representing the final 0.01% + flip burn
        els.append(f'<rect x="{bx0 + w_s2 - 4.0:.1f}" y="182" width="4.0" height="28" rx="1.5" fill="{GREEN}"/>')
        els.append(txt(bx0 + 8, 200, f"{E_SHIP_MJ:.2f} MJ/kg（一级 27.8 倍！）", 10.3, "#ffffff", weight="700"))
        els.append(txt(36, 228, "↑ 大气弓形激波与拍肚皮吃掉 99.99% 动能（刹至 ~80 m/s）", 9.6, ORANGE, weight="600"))

        # Why pure rocket braking fails for Stage 2
        els.append(card(34, 242, 324, 118, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(46, 262, "为什么二级不能像一级那样靠发动机硬刹？", 10.8, ORANGE, weight="700"))
        els.append(txt(46, 282, "• 真空猛禽 Isp = 380 s（排气速度 ve = 3,727 m/s）", 9.9, BODY))
        els.append(txt(46, 300, f"• 若纯靠反推刹停 7.8 km/s：m0/mf = exp(7800/3727) = {PROP_BRAKE_MR:.2f}", 9.9, BODY))
        els.append(txt(46, 318, "• 意味着 120 吨空船要背 >850 吨“刹车油”上太空，", 9.9, BODY))
        els.append(txt(46, 336, "  有效载荷直接归零倒贴！必须向大气“借阻力”免费刹车。", 9.9, ORANGE, weight="700"))

        # Stage 1 vs Stage 2 recovery recipe summary
        els.append(card(34, 370, 324, 108, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(46, 390, "两级分道扬镳的回收物理配方：", 10.8, BLUE, weight="700"))
        els.append(txt(46, 410, "• 一级（亚轨道 ~68 km）：反推调头 + 栅格翼减速 + 304L 裸钢", 9.8, BODY))
        els.append(txt(46, 428, "  硬抗短暂气动热 + 13→3 台猛禽精准悬停入筷（无隔热瓦）", 9.8, BODY))
        els.append(txt(46, 448, "• 二级（入轨再入）：1.8 万片陶瓷瓦扛 >1,400°C 等离子火海 +", 9.8, BODY))
        els.append(txt(46, 466, "  横躺拍肚皮跳伞 + 最后 550 米三机点火“神龙摆尾”挂入塔臂！", 9.8, GREEN, weight="700"))

        # Right Card: Why Chop Off Landing Legs ("The Best Part Is No Part")
        els.append(card(388, 62, 352, 430))
        els.append(txt(404, 84, "② “最好的零件就是没有零件”：砍掉着陆腿", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "把几十吨起落架与缓冲器剥离箭体，交给地面 146 米集成塔", 10.3, MUTED))

        # Left sub-card: Falcon 9 with 4 legs
        els.append(card(402, 116, 156, 168, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(480, 134, "猎鹰 9 号：自带 4 条腿", 10.4, SLATE, "middle", weight="700"))
        # Draw Falcon 9 lower stage + 4 deployed legs on droneship deck
        els.append(f'<line x1="418" y1="226" x2="542" y2="226" stroke="{SLATE}" stroke-width="2.2"/>')
        els.append(f'<rect x="469" y="148" width="22" height="62" rx="3" fill="#ffffff" stroke="{SLATE}" stroke-width="1.6"/>')
        els.append(f'<path d="M469,196 L442,225 M469,206 L448,225 M491,196 L518,225 M491,206 L512,225" stroke="{SLATE}" stroke-width="2.0"/>')
        els.append(f'<polygon points="476,210 484,210 487,223 473,223" fill="{ORANGE}" fill-opacity="0.7"/>')
        els.append(txt(480, 244, "碳纤维腿+一次性压溃铝芯", 9.5, BODY, "middle"))
        els.append(txt(480, 260, "驳船拖回港口需数天吊装", 9.5, MUTED, "middle"))
        els.append(txt(480, 276, "二级仍作一次性抛弃", 9.5, ORANGE, "middle", weight="600"))

        # Right sub-card: Starship + Mechazilla Chopsticks (Zero legs)
        els.append(card(570, 116, 156, 168, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(648, 134, "星舰一二级：零着陆腿！", 10.4, GREEN, "middle", weight="700"))
        # Draw tower + two chopstick rails + suspended cylinder with 2 short pins
        els.append(f'<rect x="586" y="144" width="12" height="86" rx="2" fill="#cbd5e1" stroke="{SLATE}" stroke-width="1.3"/>')
        els.append(f'<line x1="598" y1="168" x2="692" y2="168" stroke="{GREEN}" stroke-width="3.2"/>')
        els.append(f'<rect x="636" y="152" width="28" height="72" rx="4" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
        # Two tiny catch pins resting on rail
        els.append(f'<line x1="630" y1="165" x2="636" y2="165" stroke="{ORANGE}" stroke-width="3.0"/>')
        els.append(f'<line x1="664" y1="165" x2="670" y2="165" stroke="{ORANGE}" stroke-width="3.0"/>')
        els.append(txt(648, 244, "箭体仅留 2 根 ~30cm 承力销", 9.5, BODY, "middle"))
        els.append(txt(648, 260, "液压吸能缓冲全留在地面塔臂", 9.5, GREEN, "middle", weight="700"))
        els.append(txt(648, 276, "接住即可移回发射台复飞", 9.5, GREEN, "middle", weight="600"))

        # 3 Critical Reasons Box
        els.append(card(402, 294, 324, 184, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(414, 314, "若硬给星舰装上重型着陆腿，要吃哪三重苦头？", 10.6, INK, weight="700"))

        reasons = [
            ("1", ORANGE, "二级 1:1 吞噬运力：", "二级每多背 1 吨腿入轨，有效载荷就直降 1 吨；省下 ~10 吨起落架等于白赚 10 吨卫星运力！"),
            ("2", "#dc2626", "隔热罩严禁乱开缝：", "起落架舱门若切开迎风面隔热瓦，>1,400°C 等离子流极易顺缝钻入（哥伦比亚号惨痛教训）。"),
            ("3", GREEN, "避开地面激波与吊装：", "200–275 吨空箭悬在半空挂上筷子，既免遭尾焰砸地反弹，又能原地叠回发射台快周转。"),
        ]
        for idx, (num_s, col_r, head_r, body_r) in enumerate(reasons):
            ry = 336 + idx * 48
            els.append(step_badge(418, ry + 4, num_s, fg=col_r, bg="#ffffff", r=9.5))
            els.append(txt(434, ry + 2, head_r + body_r[:15], 9.8, INK, weight="700"))
            els.append(txt(434, ry + 18, body_r[15:], 9.6, BODY))

        return figure(
            506,
            "星舰一二级28倍比动能差距与砍掉着陆腿改用发射塔捕获的物理账单图",
            "左图按比动能公式e=1/2v^2计算超重助推器1.48 km/s（1.10 MJ/kg）与星舰二级7.80 km/s（30.42 MJ/kg，相差27.8倍）的减速账单，证明二级若纯靠真空猛禽反推需8.11倍质量比，必须靠大气耗散99.99%动能；右图对比猎鹰9号四条折叠腿与星舰无腿承力销方案，说明二级1:1运力惩罚、隔热瓦不开舱门与地面塔臂快周转三大原因。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 2. Super Heavy 7-Minute Recovery Loop: Hot-Staging, Grid Fins, 33-Engine Rings & Chopsticks (Animated)
    def _build_super_heavy_catch_anim():
        assert 20 + 10 + 3 == 33

        anim_css = """
  .sh-path {
    stroke-dasharray: 760;
    stroke-dashoffset: 760;
    animation: shTrace 6.6s cubic-bezier(.25,.6,.25,1) 0.35s 1 forwards;
  }
  .sh-lock {
    opacity: 0.25;
    animation: shLock 0.6s ease 6.4s 1 forwards;
  }
  @keyframes shTrace { to { stroke-dashoffset: 0; } }
  @keyframes shLock  { to { opacity: 1; } }
  @media (prefers-reduced-motion: reduce) {
    .sh-path { animation: none !important; stroke-dashoffset: 0 !important; }
    .sh-lock { animation: none !important; opacity: 1 !important; }
  }"""

        els = header(
            "超重助推器 7 分钟闭环：热分离、栅格翼滑翔与“机械哥斯拉”半空夹筷子",
            "左：升空至返航捕获全航迹与外海自动弃捕安全门（单次动画）｜右：33 机三环分工与挂销缓冲结构",
        )

        # Left Card: Trajectory Loop (x=20..472, y=62..508)
        els.append(card(20, 62, 452, 446))
        els.append(txt(36, 84, "① 升空 → 热分离 → 返航 → 13 变 3 平移入筷（T+00:00 ～ 06:56）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "惯性弹道默认指向外海；千项塔箭自检全绿灯才在最后数秒横移进塔臂", 10.1, MUTED))

        # Coordinate mapping inside plot (Downrange x_km: -2 .. 36 km -> px 56 .. 452; Alt h_km: 0 .. 76 km -> py 412 .. 126)
        px0, py0, pw, ph = 56.0, 412.0, 396.0, 286.0

        def map_xh(x_km, h_km):
            return px0 + ((x_km + 2.0) / 38.0) * pw, py0 - (h_km / 76.0) * ph

        # Altitude gridlines
        for hk in (0, 20, 40, 60):
            _, gy = map_xh(0, hk)
            els.append(f'<line x1="{px0:.1f}" y1="{gy:.1f}" x2="{px0 + pw:.1f}" y2="{gy:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(px0 - 5, gy + 3.5, f"{hk}km" if hk == 60 else f"{hk}", 9.4, MUTED, "end"))

        # Land (Starbase Texas x=-2..7 km) vs Gulf of Mexico (x=7..36 km)
        x_coast, _ = map_xh(7.0, 0)
        els.append(f'<rect x="{px0:.1f}" y="{py0:.1f}" width="{x_coast - px0:.1f}" height="10" rx="2" fill="#dcfce7"/>')
        els.append(f'<rect x="{x_coast:.1f}" y="{py0:.1f}" width="{px0 + pw - x_coast:.1f}" height="10" rx="2" fill="#dbeafe"/>')
        els.append(txt((px0 + x_coast) / 2, py0 + 23, "星港陆地", 9.6, GREEN, "middle", weight="700"))
        els.append(txt((x_coast + px0 + pw) / 2, py0 + 23, "墨西哥湾外海（安全缓冲海面）", 9.6, BLUE, "middle", weight="600"))

        # Starbase Mechazilla Tower at x=1.2 km
        tx_pad, ty_pad = map_xh(1.2, 0)
        els.append(f'<rect x="{tx_pad - 5:.1f}" y="{ty_pad - 36:.1f}" width="6" height="36" fill="{SLATE}"/>')
        els.append(f'<line x1="{tx_pad + 1:.1f}" y1="{ty_pad - 26:.1f}" x2="{tx_pad + 15:.1f}" y2="{ty_pad - 26:.1f}" stroke="{GREEN}" stroke-width="2.8"/>')

        # Key trajectory points
        p_lift = (tx_pad + 8, ty_pad - 2)
        p_sep = map_xh(23.0, 59.5)
        p_ship = map_xh(34.2, 74.0)
        p_ap = map_xh(28.0, 69.5)
        p_glide = map_xh(14.5, 36.0)
        p_burn = map_xh(7.6, 13.0)
        p_abort = map_xh(13.2, 0.4)
        p_catch = (tx_pad + 10, ty_pad - 26)

        # Starship Stage 2 orbital continuation arrow
        els.append(
            f'<path d="M {p_sep[0]:.1f},{p_sep[1]:.1f} Q {p_sep[0] + 42:.1f},{p_sep[1] - 32:.1f} {p_ship[0]:.1f},{p_ship[1]:.1f}" '
            f'fill="none" stroke="{PURPLE}" stroke-width="2.2" stroke-dasharray="5 3" marker-end="url(#ss-purple)"/>'
        )
        els.append(txt(p_ship[0] - 4, p_ship[1] - 6, "二级 6 机点火入轨 →", 9.5, PURPLE, "end", weight="700", halo=True))

        # Offshore Auto-Abort safety branch (dashed orange)
        els.append(
            f'<path d="M {p_glide[0]:.1f},{p_glide[1]:.1f} Q {p_burn[0] + 32:.1f},{p_burn[1] + 8:.1f} {p_abort[0]:.1f},{p_abort[1]:.1f}" '
            f'fill="none" stroke="{ORANGE}" stroke-width="1.9" stroke-dasharray="4 3" marker-end="url(#ss-orange)"/>'
        )
        els.append(txt(p_abort[0] + 8, p_abort[1] - 11, "未过检自动弃捕落海", 9.4, ORANGE, weight="700", halo=True))
        els.append(txt(p_abort[0] + 8, p_abort[1] + 3, "(如 F6 塔损 / F15 B22)", 9.1, MUTED, halo=True))

        # Full nominal booster path (faint static base + one-shot animated highlight)
        d_booster = (
            f"M {p_lift[0]:.1f},{p_lift[1]:.1f} "
            f"C {p_lift[0] + 30:.1f},{p_lift[1] - 125:.1f} {p_sep[0] - 78:.1f},{p_sep[1] + 36:.1f} {p_sep[0]:.1f},{p_sep[1]:.1f} "
            f"C {p_sep[0] + 24:.1f},{p_sep[1] - 20:.1f} {p_ap[0] + 8:.1f},{p_ap[1] - 6:.1f} {p_ap[0] - 12:.1f},{p_ap[1]:.1f} "
            f"C {p_ap[0] - 58:.1f},{p_ap[1] + 18:.1f} {p_glide[0] + 22:.1f},{p_glide[1] - 36:.1f} {p_glide[0]:.1f},{p_glide[1]:.1f} "
            f"C {p_glide[0] - 24:.1f},{p_glide[1] + 38:.1f} {p_burn[0] + 16:.1f},{p_burn[1] - 26:.1f} {p_burn[0]:.1f},{p_burn[1]:.1f} "
            f"Q {p_burn[0] - 24:.1f},{p_burn[1] + 24:.1f} {p_catch[0]:.1f},{p_catch[1]:.1f}"
        )
        els.append(f'<path d="{d_booster}" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-opacity="0.24"/>')
        els.append(f'<path class="sh-path" d="{d_booster}" fill="none" stroke="{BLUE}" stroke-width="2.7" marker-end="url(#ss-green)"/>')

        # Step badges & clean callouts along loop
        p_asc_mid = map_xh(7.0, 29.0)
        pts_steps = [
            (p_asc_mid[0], p_asc_mid[1], "1", BLUE, "① 33 机齐射升空", "推力 75–82 MN", "end", -13, -4),
            (p_sep[0], p_sep[1], "2", PURPLE, "② T+2:41 热分离", "留 3 机顶住液面", "end", -13, -4),
            (p_ap[0] - 12, p_ap[1], "3", ORANGE, "③ 13 机返航点火", "最高 ~70 km 调头", "start", 13, 2),
            (p_glide[0], p_glide[1], "4", SLATE, "④ 栅格翼超音速滑翔", "气动吃掉 ~80% 残速", "start", 14, -2),
            (p_burn[0], p_burn[1], "5", GREEN, "⑤ ~1 km 着陆点火", "13 机急刹 → 3 机横移", "start", 14, -4),
        ]
        for bx, by, ns, col_s, l1, l2, anc, dx, dy in pts_steps:
            els.append(step_badge(bx, by, ns, fg=col_s, bg="#ffffff", r=9.5))
            els.append(txt(bx + dx, by + dy, l1, 9.6, col_s, anc, weight="700", halo=True))
            els.append(txt(bx + dx, by + dy + 13, l2, 9.2, BODY, anc, halo=True))

        # Final lock pill cleanly positioned above tower without touching badge 5
        els.append('<g class="sh-lock">')
        els.append(f'<line x1="{tx_pad + 8:.1f}" y1="{ty_pad - 52:.1f}" x2="{tx_pad + 8:.1f}" y2="{ty_pad - 30:.1f}" stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="2 2"/>')
        els.append(pill(38, ty_pad - 72, "⑥ T+6:56 挂销落轨！", fg=GREEN, bg=GREEN_SOFT, w=116, h=20, size=9.4))
        els.append("</g>")

        # Bottom Hot-Staging note inside Left Card
        els.append(card(34, 442, 424, 54, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(46, 461, "为什么要“热分离”？传统冷分离一旦全关机失重，几百吨液氧甲烷会飘离箱底；", 9.6, BODY))
        els.append(txt(46, 480, "超重助推器保留中心 3 台猛禽节流推顶，二级贴脸点火直接让入轨运力暴涨约 10%！", 9.6, BLUE, weight="700"))

        # Right Card: 33-Engine Concentric Layout + Chopstick Pin Mechanics (x=486..740, y=62..508)
        els.append(card(486, 62, 254, 446))
        els.append(txt(500, 84, "② 底部仰视：33 台猛禽三环分工", 12.6, INK, weight="700"))

        cx, cy = 613.0, 168.0
        els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="60" fill="{SLATE_SOFT}" stroke="{BORDER}" stroke-width="1.4"/>')
        # Outer 20 fixed Raptors
        for i in range(20):
            ang = 2.0 * math.pi * i / 20.0
            ex = cx + 50.0 * math.cos(ang)
            ey = cy + 50.0 * math.sin(ang)
            els.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.8" fill="{SLATE}"/>')
        # Middle 10 gimbaled Raptors
        for i in range(10):
            ang = 2.0 * math.pi * i / 10.0 + 0.15
            ex = cx + 30.0 * math.cos(ang)
            ey = cy + 30.0 * math.sin(ang)
            els.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{ORANGE}" stroke="#ffffff" stroke-width="0.9"/>')
        # Center 3 gimbaled Raptors
        for i in range(3):
            ang = 2.0 * math.pi * i / 3.0 - math.pi / 2.0
            ex = cx + 11.5 * math.cos(ang)
            ey = cy + 11.5 * math.sin(ang)
            els.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5.2" fill="{GREEN}" stroke="#ffffff" stroke-width="1.1"/>')

        els.append(txt(500, 244, "• 外环 20 台（灰）：固定喷管，仅起飞出死力", 9.5, SLATE, weight="600"))
        els.append(txt(500, 261, "• 中环 10 台（橙）：可摆动重燃，返航+初段急刹", 9.5, ORANGE, weight="600"))
        els.append(txt(500, 278, "• 中心 3 台（绿）：±15° 电驱摆动，悬停入筷", 9.5, GREEN, weight="700"))

        els.append(f'<line x1="500" y1="291" x2="726" y2="291" stroke="{BORDER}" stroke-width="1"/>')
        els.append(txt(500, 312, "③ 筷子到底怎样“夹”住 9 米薄壳？", 12.6, INK, weight="700"))

        # Front elevation of Chopstick Arms + Catch Pins + Shock Rails
        bx_c = 613.0
        # Left & Right Chopstick Steel Truss Arms (viewed head-on)
        els.append(f'<rect x="{bx_c - 82:.1f}" y="356" width="42" height="14" rx="3" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.5"/>')
        els.append(f'<rect x="{bx_c + 40:.1f}" y="356" width="42" height="14" rx="3" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.5"/>')
        # Shock-absorbing bumper rails on top of arms
        els.append(f'<rect x="{bx_c - 64:.1f}" y="347" width="24" height="9" rx="2" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.4"/>')
        els.append(f'<rect x="{bx_c + 40:.1f}" y="347" width="24" height="9" rx="2" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.4"/>')
        # Closing arrows
        els.append(f'<line x1="{bx_c - 100:.1f}" y1="363" x2="{bx_c - 85:.1f}" y2="363" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#ss-blue)"/>')
        els.append(f'<line x1="{bx_c + 100:.1f}" y1="363" x2="{bx_c + 85:.1f}" y2="363" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#ss-blue)"/>')
        # 9m Booster Cylinder suspended between arms
        els.append(f'<rect x="{bx_c - 36:.1f}" y="324" width="72" height="92" rx="5" fill="#ffffff" stroke="{INK}" stroke-width="1.7"/>')
        els.append(txt(bx_c, 374, "9 m 箭体", 10.0, INK, "middle", weight="700"))
        els.append(txt(bx_c, 390, "3.97mm 钢壳", 8.8, MUTED, "middle"))
        # Two Forged Catch Pins resting on top of shock rails!
        els.append(f'<rect x="{bx_c - 52:.1f}" y="341" width="16" height="6" rx="2" fill="{ORANGE}"/>')
        els.append(f'<rect x="{bx_c + 36:.1f}" y="341" width="16" height="6" rx="2" fill="{ORANGE}"/>')
        els.append(txt(bx_c - 56, 335, "承力挂销", 9.4, ORANGE, "end", weight="700"))
        els.append(txt(bx_c + 56, 335, "液压缓冲轨", 9.4, GREEN, "start", weight="700"))

        els.append(txt(500, 436, "• 绝非拿铁臂硬挤薄壁！双臂合拢至窄缝后，", 9.5, BODY))
        els.append(txt(500, 453, "  箭体两侧锻造承力销稳稳坐上顶部液压吸能轨", 9.5, GREEN, weight="700"))
        els.append(txt(500, 471, "• Block 3 改为 3 片电驱栅格翼（90°/90°/180°）", 9.5, BODY))
        els.append(txt(500, 488, "  直接把承力挂点融进左右对称的两片翼根！", 9.5, BLUE, weight="600"))

        return figure(
            522,
            "超重助推器7分钟发射热分离返航与机械哥斯拉筷子捕获全流程动画图解",
            "左图按时间顺序演示超重助推器33机升空、T+2分41秒保留中心3机的级间热分离、13机返航点火、栅格翼超音速滑翔、外海自动弃捕安全分支以及1公里高度13变3机平移挂入146米发射塔筷子的单次动画；右图展示底部33台猛禽外20中10内3三环布局及双承力销坐落液压缓冲轨的机械细节。",
            els,
            extra_css=anim_css,
            extra_defs=EXTRA_ARR,
        )

    # 3. Raptor Full-Flow Staged Combustion (FFSC) & Nosecone Header Tank Slosh Shield
    def _build_raptor_and_header_tanks():
        els = header(
            "半空急刹全靠哪颗“心脏”？全流量分级燃烧猛禽与鼻锥“防晃小油箱”",
            "左：全球首款实用化全流量分级燃烧甲烷机（Raptor）｜右：为什么横躺坠落绝不能直接抽主贮箱？",
        )

        # Left Card: Raptor FFSC Cycle
        els.append(card(20, 62, 352, 432))
        els.append(txt(36, 84, "① 猛禽发动机：纯气态对撞燃烧，零结焦秒重燃", 13.0, INK, weight="700"))
        els.append(txt(36, 102, "过冷液态甲烷/液氧（~93–95 K，氧燃比 ~3.6:1）天生适合高频免检复用", 10.0, MUTED))

        # Dual propellant inlets
        els.append(card(36, 118, 150, 46, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(111, 137, "100% 过冷液氧 LOX", 10.2, BLUE, "middle", weight="700"))
        els.append(txt(111, 153, "SX500 耐富氧超合金泵增压", 9.3, BODY, "middle"))

        els.append(card(206, 118, 150, 46, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(281, 137, "100% 过冷甲烷 LCH₄", 10.2, ORANGE, "middle", weight="700"))
        els.append(txt(281, 153, "先流经喷管室壁再生冷却", 9.3, BODY, "middle"))

        # Arrows down to twin preburners
        els.append(f'<line x1="111" y1="164" x2="111" y2="184" stroke="{BLUE}" stroke-width="2.0" marker-end="url(#ss-blue)"/>')
        els.append(f'<line x1="281" y1="164" x2="281" y2="184" stroke="{ORANGE}" stroke-width="2.0" marker-end="url(#ss-orange)"/>')
        # Small cross-feed dashed lines (tiny CH4 to OX preburner, tiny LOX to Fuel preburner)
        els.append(f'<line x1="216" y1="172" x2="146" y2="184" stroke="{ORANGE}" stroke-width="1.2" stroke-dasharray="3 2" marker-end="url(#ss-orange)"/>')
        els.append(f'<line x1="176" y1="172" x2="246" y2="184" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="3 2" marker-end="url(#ss-blue)"/>')

        # Twin Preburners
        els.append(card(36, 188, 150, 52, rx=7, fill="#ffffff", stroke=BLUE, sw=1.4))
        els.append(txt(111, 208, "富氧预燃室 + 氧涡轮", 10.2, BLUE, "middle", weight="700"))
        els.append(txt(111, 226, "化作中温高压富氧燃气", 9.4, BODY, "middle"))

        els.append(card(206, 188, 150, 52, rx=7, fill="#ffffff", stroke=ORANGE, sw=1.4))
        els.append(txt(281, 208, "富燃预燃室 + 燃涡轮", 10.2, ORANGE, "middle", weight="700"))
        els.append(txt(281, 226, "化作中温高压富甲烷燃气", 9.4, BODY, "middle"))

        # Converging gas-gas injection into Main Chamber
        els.append(f'<path d="M111,240 L156,264" fill="none" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#ss-blue)"/>')
        els.append(f'<path d="M281,240 L236,264" fill="none" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#ss-orange)"/>')

        els.append(card(68, 266, 256, 62, rx=9, fill=GREEN_SOFT, stroke=GREEN, sw=1.6))
        els.append(txt(196, 287, "300–350 bar 主燃烧室：纯气-气对撞自燃！", 10.6, GREEN, "middle", weight="700"))
        els.append(txt(196, 305, "无液滴雾化延迟 · 高温高压接触即燃", 9.6, BODY, "middle"))
        els.append(txt(196, 320, "预燃室配电火花点火器 ⇒ 飞行中可多次重燃", 9.5, GREEN, "middle", weight="600"))

        # Gimbaled bell nozzle
        els.append(f'<polygon points="168,328 224,328 242,366 150,366" fill="{SLATE_SOFT}" stroke="{INK}" stroke-width="1.6"/>')
        els.append(txt(196, 352, "±15° 电驱摆动", 9.5, INK, "middle", weight="700"))

        # Bottom summary card
        els.append(card(34, 378, 324, 104, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 398, "• 零积碳结焦：甲烷无长碳链，彻底告别煤油机涡轮积碳翻修", 9.6, BODY))
        els.append(txt(46, 418, "• 全工质做功：无燃气发生器废气白抛，海平面 Isp 327–350 s", 9.6, BODY))
        els.append(txt(46, 438, "• Raptor 3 进化：次级流道 3D 打印进内壁，砍掉 >1 吨外防热罩，", 9.6, BODY))
        els.append(txt(46, 456, "  单机海平面推力跃升至 ~280 吨力，裸机可耐受高温返航尾流！", 9.6, BLUE, weight="700"))

        # Right Card: Slosh Trap vs Nosecone Header Tanks
        els.append(card(388, 62, 352, 432))
        els.append(txt(404, 84, "② 晃动生死劫：为什么要把着陆油箱藏进鼻锥尖？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "横躺坠落时着陆余油仅占主箱容积 ~2%，直接抽取必吸气泡爆炸", 10.0, MUTED))

        # Top counterfactual: Sucking from 52m main tank during horizontal belly-flop
        els.append(card(402, 118, 324, 144, rx=8, fill="#fef2f2", stroke="#dc2626"))
        els.append(txt(414, 138, "✕ 反例：横躺 90° 若从 1,200–1,600 吨巨型主箱抽油", 10.4, "#dc2626", weight="700"))

        # Horizontal Starship hull showing 98% gas + shallow sloshing puddle away from aft pump port
        els.append(f'<path d="M430,178 Q458,158 504,158 L678,158 L678,198 L504,198 Q458,198 430,178 Z" fill="#ffffff" stroke="#dc2626" stroke-width="1.5"/>')
        els.append(f'<line x1="566" y1="158" x2="566" y2="198" stroke="#dc2626" stroke-width="1.2"/>')
        # Sloshing shallow liquid puddle along bottom belly, exposing mid-height aft outlet to gas!
        els.append(f'<path d="M506,192 Q532,184 564,193 L564,197 L506,197 Z" fill="{ORANGE}" fill-opacity="0.45"/>')
        els.append(f'<path d="M568,191 Q615,182 676,193 L676,197 L568,197 Z" fill="{BLUE}" fill-opacity="0.45"/>')
        els.append(txt(622, 176, "98% 是增压气体！", 9.5, "#dc2626", "middle", weight="700"))
        # Aft engines sucking gas bubbles
        els.append(f'<polygon points="678,171 694,165 694,191 678,185" fill="#fecaca" stroke="#dc2626" stroke-width="1.2"/>')
        els.append(txt(414, 220, "• 涡轮泵转速超 3 万转/分，一旦吸入半口气泡瞬间空化飞车、", 9.6, BODY))
        els.append(txt(414, 238, "  富氧烧穿发动机！（早期 SN8/SN9 曾因头部箱增压不足坠毁）", 9.6, "#dc2626", weight="600"))

        # Bottom real solution: Nosecone Header Tanks + Insulated Downcomers
        els.append(card(402, 274, 324, 208, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(414, 294, "✓ 星舰正解：鼻锥尖端独立“头部小贮箱”（Header Tanks）", 10.4, GREEN, weight="700"))

        # Horizontal Starship hull with 100%-full nosecone LOX + LCH4 header tanks + pipes to 3 center Raptors
        els.append(f'<path d="M424,338 Q454,314 504,314 L678,314 L678,362 L504,362 Q454,362 424,338 Z" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
        # Tip LOX header tank (filled blue)
        els.append(f'<path d="M425,338 Q442,323 462,320 L462,356 Q442,353 425,338 Z" fill="{BLUE}" fill-opacity="0.85"/>')
        # Adjacent LCH4 header tank (filled orange)
        els.append(f'<path d="M464,320 L494,316 L494,360 L464,356 Z" fill="{ORANGE}" fill-opacity="0.85"/>')
        # Insulated downcomer pipes running straight to 3 SL Raptors
        els.append(f'<line x1="462" y1="334" x2="678" y2="334" stroke="{BLUE}" stroke-width="2.2"/>')
        els.append(f'<line x1="494" y1="343" x2="678" y2="343" stroke="{ORANGE}" stroke-width="2.2"/>')
        els.append(f'<polygon points="678,329 696,323 696,353 678,347" fill="{GREEN}" fill-opacity="0.85"/>')

        els.append(txt(414, 310, "↓ 鼻锥尖 100% 满液 LOX + LCH₄ 头箱", 9.3, INK, "start", weight="700"))
        els.append(txt(590, 329, "独立保温下输管直供 3 台海平面猛禽", 9.2, GREEN, "middle", weight="700"))

        els.append(txt(414, 386, "• 满灌锁死液面：容积恰好装 ~25–35 吨着陆推进剂，单向阀隔离", 9.6, BODY))
        els.append(txt(414, 406, "• 无惧 90° 狂甩：COPV 高压气瓶顶住锥形集液槽，全程零气泡吸入", 9.6, BODY))
        els.append(txt(414, 426, "• 一石二鸟调配重：把几十吨燃料压在鼻锥最前端，大幅前移质心", 9.6, BODY))
        els.append(txt(414, 446, "  （CM），抵消尾部 6 台发动机重锤，稳住高超音速再入俯仰平衡！", 9.6, GREEN, weight="700"))

        return figure(
            508,
            "猛禽全流量分级燃烧甲烷发动机循环与星舰鼻锥头部小贮箱防晃动供油原理图",
            "左图展示猛禽发动机（Raptor）100%过冷液氧与100%过冷液态甲烷分别驱动富氧与富燃预燃室涡轮泵、在300至350 bar主燃烧室纯气态混合自燃并支持电火花多次重燃的全流量分级燃烧架构；右图对比横躺90度从巨型主贮箱抽油导致吸入增压气体空化爆炸的反例，与鼻锥尖端100%满液LOX/LCH4头部小贮箱经独立下输管稳定供油并前移质心的设计。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 4. 304L Steel + 18,000 Pinned Hexagonal Ceramic Tiles + Skydiver Belly-Flop Flaps
    def _build_tps_and_belly_flop():
        els = header(
            "硬扛 1,400°C 等离子火海还当“跳伞员”：1.8 万片挂钩瓦与拍肚皮控姿术",
            "左：304L 不锈钢 + Pyron 烧蚀垫 + 六角石英瓦多层护盾｜右：四片襟翼怎样学跳伞员收放四肢？",
        )

        # Left Card: 304L Steel + Multi-Layer Windward TPS
        els.append(card(20, 62, 352, 442))
        els.append(txt(36, 84, "① 为什么弃铝合金，改用不锈钢 + 卡扣六角瓦？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "航天飞机 2.4 万块异形瓦靠胶粘；星舰 ~1.8 万块标准六角瓦靠钢钉挂扣", 10.0, MUTED))

        # Material temperature bar comparison (0 .. 1600 °C)
        els.append(card(34, 116, 324, 78, rx=7, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 134, "箭体金属耐温天花板对比（决定“万一掉一块瓦会不会死”）：", 9.8, INK, weight="700"))
        # Al-Li bar (softens ~160 C, melts ~600 C)
        els.append(txt(46, 155, "传统铝合金", 9.5, SLATE, weight="600"))
        els.append(f'<rect x="106" y="145" width="26" height="12" rx="3" fill="{SLATE}"/>')
        els.append(txt(138, 155, "~160°C 软化（~600°C 熔，掉瓦易烧穿）", 9.1, "#dc2626", weight="600"))
        # 304L Stainless Steel bar (~800 C working limit, ~1420 C melting)
        els.append(txt(46, 177, "304L 不锈钢", 9.5, BLUE, weight="700"))
        els.append(f'<rect x="106" y="167" width="96" height="12" rx="3" fill="{BLUE}"/>')
        els.append(txt(208, 177, "~800°C 仍保强度（~1420°C 熔）", 9.1, BLUE, weight="700"))

        # 5-Layer Windward TPS Cross-Section (x=34..358, y=206..390)
        els.append(txt(36, 218, "迎风面热防护（TPS）五层纵深剖面（左热右冷）：", 10.4, INK, weight="700"))

        # Layer 1: Bow shock & plasma (>1,400 C)
        els.append(card(34, 230, 56, 154, rx=6, fill="#ffedd5", stroke=ORANGE))
        els.append(txt(62, 266, "钝头弓形", 9.6, ORANGE, "middle", weight="700"))
        els.append(txt(62, 282, "脱体激波", 9.6, ORANGE, "middle", weight="700"))
        els.append(txt(62, 306, ">1,400°C", 9.6, "#dc2626", "middle", weight="700"))
        els.append(txt(62, 324, "9m 大曲率", 9.1, BODY, "middle"))
        els.append(txt(62, 339, "推开主热流", 9.1, BODY, "middle"))

        # Layer 2: Hexagonal Silica Ceramic Fiber Tile (~90% air, black borosilicate glaze)
        els.append(card(96, 230, 82, 154, rx=6, fill="#1e293b", stroke=INK))
        els.append(txt(137, 258, "六角石英瓦", 9.8, "#ffffff", "middle", weight="700"))
        els.append(txt(137, 276, "ρ≈0.34 g/cm³", 9.2, "#93c5fd", "middle", weight="600"))
        els.append(txt(137, 294, "~90% 是空气", 9.2, "#e2e8f0", "middle"))
        els.append(txt(137, 314, "黑硼硅玻璃釉", 9.1, "#fde68a", "middle"))
        els.append(txt(137, 330, "二次辐射散走", 9.1, "#fde68a", "middle"))
        els.append(txt(137, 346, ">90% 表面热！", 9.2, "#fde68a", "middle", weight="700"))

        # Layer 3: Ceramic Felt ("Crunch Wrap") + Pyron Secondary Ablative Layer
        els.append(card(184, 230, 68, 154, rx=6, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(218, 260, "缝隙陶瓷毡", 9.5, ORANGE, "middle", weight="700"))
        els.append(txt(218, 276, "+ Pyron", 9.5, ORANGE, "middle", weight="700"))
        els.append(txt(218, 292, "二次烧蚀层", 9.5, ORANGE, "middle", weight="700"))
        els.append(txt(218, 318, "防等离子钻缝", 9.0, BODY, "middle"))
        els.append(txt(218, 334, "掉瓦时替身保命", 9.0, BODY, "middle"))

        # Layer 4: 3.97 mm 304L Stainless Steel Hull + Welded Stud Pins (placed clear of Layer 3 text!)
        els.append(card(258, 230, 50, 154, rx=6, fill=SLATE_SOFT, stroke=SLATE, sw=1.5))
        els.append(f'<rect x="170" y="238" width="88" height="5" rx="1.5" fill="{SLATE}"/>')
        els.append(f'<rect x="170" y="366" width="88" height="5" rx="1.5" fill="{SLATE}"/>')
        els.append(txt(283, 292, "304L", 9.8, INK, "middle", weight="700"))
        els.append(txt(283, 308, "不锈钢壁", 9.4, INK, "middle", weight="700"))
        els.append(txt(283, 325, "3.97 mm", 9.1, MUTED, "middle"))
        els.append(txt(283, 342, "焊钉卡扣", 9.1, BLUE, "middle", weight="600"))

        # Layer 5: Cryogenic / Interior Safe Zone
        els.append(card(314, 230, 44, 154, rx=6, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(336, 294, "深冷箱", 9.4, BLUE, "middle", weight="700"))
        els.append(txt(336, 312, "<100°C", 9.3, GREEN, "middle", weight="700"))
        els.append(txt(336, 329, "安全区", 9.1, BODY, "middle"))

        # Bottom summary inside Left Card
        els.append(card(34, 396, 324, 96, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(46, 416, "• 六角阵列无十字长直通缝，钢钉机械卡扣允许瓦片自由热胀冷缩", 9.6, BODY))
        els.append(txt(46, 436, "• Block 2/3 将前襟翼后掠并向背风面折起 140°，彻底根治铰链烧蚀", 9.6, BODY))
        els.append(txt(46, 456, "• Flight 15 实战检验：Ship 42 扛过 7.8 km/s 再入，完好挂上筷子！", 9.6, GREEN, weight="700"))

        # Right Card: Skydiver Belly-Flop Aerodynamics
        els.append(card(388, 62, 352, 442))
        els.append(txt(404, 84, "② “拍肚皮”跳伞术：四片襟翼怎样不动尾翼控三轴？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "迎角 65°～90° 横躺迎风，亚音速终端下坠速度压至仅 ~75–85 m/s", 10.0, MUTED))

        # Aerodynamic Pitch Trim Diagram (x=402..594, y=118..316) & Cross-Section Flap Hinge Inset (x=600..726)
        els.append(card(402, 118, 190, 196, rx=8, fill="#ffffff", stroke=BORDER))
        els.append(txt(497, 136, "侧视：前后襟翼差动调压心", 10.0, INK, "middle", weight="700"))

        # Relative upward airflow arrows
        for ax in (428, 474, 520, 566):
            els.append(f'<line x1="{ax}" y1="296" x2="{ax}" y2="262" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#ss-blue)"/>')
        els.append(txt(497, 308, "迎面气流 v_∞（终端速度 ~80 m/s）", 9.2, BLUE, "middle", weight="600"))

        # Horizontal Starship body (tilted slightly nose-up by 6 deg)
        els.append('<g transform="translate(496,214) rotate(-6)">')
        els.append(f'<path d="M-76,0 Q-54,-14 -24,-14 L68,-14 L68,14 L-24,14 Q-54,14 -76,0 Z" fill="#f8fafc" stroke="{INK}" stroke-width="1.6"/>')
        # Black heat-shield belly strip
        els.append('<path d="M-72,3 Q-50,14 -24,14 L68,14 L68,9 L-24,9 Q-50,9 -70,0 Z" fill="#1e293b"/>')
        # Forward flap spread flat (big drag vector!)
        els.append(f'<rect x="-56" y="-8" width="24" height="7" rx="2" fill="{GREEN}" fill-opacity="0.85"/>')
        # Aft flap folded leeward (smaller drag vector!)
        els.append(f'<polygon points="44,-12 66,-12 62,-28 48,-24" fill="{ORANGE}" fill-opacity="0.85"/>')
        # CM and CP markers
        els.append(f'<circle cx="-10" cy="0" r="4.2" fill="{INK}"/>')
        els.append(f'<circle cx="-26" cy="0" r="4.2" fill="{GREEN}"/>')
        els.append("</g>")

        # Force arrows F_fwd (large) vs F_aft (small)
        els.append(f'<line x1="448" y1="206" x2="448" y2="154" stroke="{GREEN}" stroke-width="2.6" marker-end="url(#ss-green)"/>')
        els.append(txt(448, 149, "前翼平展(大阻)", 9.2, GREEN, "middle", weight="700"))
        els.append(f'<line x1="552" y1="214" x2="552" y2="184" stroke="{ORANGE}" stroke-width="2.0" marker-end="url(#ss-orange)"/>')
        els.append(txt(552, 178, "后翼上折(小阻)", 9.2, ORANGE, "middle", weight="700"))
        els.append(txt(496, 246, "压心 CP 前移 ⇒ 产生抬头力矩！", 9.3, GREEN, "middle", weight="700"))

        # Right Inset: Head-on cross-section showing leeward folding (0° flat <-> 80° folded, 140° mount)
        els.append(card(598, 118, 128, 196, rx=8, fill="#ffffff", stroke=BORDER))
        els.append(txt(662, 136, "迎头截面：背风收放", 10.0, INK, "middle", weight="700"))
        # Hull circle at (662, 218, r=24)
        els.append(f'<circle cx="662" cy="218" r="24" fill="#f8fafc" stroke="{INK}" stroke-width="1.6"/>')
        # Windward black bottom arc
        els.append('<path d="M638,218 A24,24 0 0 0 686,218" fill="none" stroke="#0f172a" stroke-width="4.2"/>')
        # Left flap spread flat (0 deg)
        els.append(f'<line x1="638" y1="214" x2="608" y2="214" stroke="{GREEN}" stroke-width="4.0" stroke-linecap="round"/>')
        # Right flap folded leeward (75 deg up into wake!)
        els.append(f'<line x1="684" y1="210" x2="696" y2="178" stroke="{ORANGE}" stroke-width="4.0" stroke-linecap="round"/>')
        els.append(f'<path d="M712,208 A34,34 0 0 0 700,180" fill="none" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="3 2" marker-end="url(#ss-orange)"/>')
        els.append(txt(623, 232, "0°平展", 9.1, GREEN, "middle", weight="700"))
        els.append(txt(702, 172, "80°收拢", 9.1, ORANGE, "middle", weight="700"))
        els.append(txt(662, 266, "不往下翻（避火流）", 9.2, BODY, "middle"))
        els.append(txt(662, 283, "只往背风侧收拢减阻", 9.2, BLUE, "middle", weight="600"))
        els.append(txt(662, 300, "左右不对称 ⇒ 滚转！", 9.2, PURPLE, "middle", weight="700"))

        # 3-Axis Skydiver Control Matrix
        els.append(card(402, 326, 324, 166, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(414, 346, "四片襟翼协同口诀（活脱脱一位钢铁高空跳伞员）：", 10.3, INK, weight="700"))

        rows_ctrl = [
            ("俯仰 Pitch", GREEN, "前翼平展 0° + 后翼收拢 80° ⇒ 抬头（神龙摆尾起手式！）"),
            ("横滚 Roll", PURPLE, "左收右展 ⇒ 机身侧倾偏转升力，高超音速横向滑翔数百公里"),
            ("偏航 Yaw", BLUE, "左前+右后对角差动 ⇒ 扭转船头，绕过外海安全门精准对塔"),
        ]
        for idx, (tag_c, col_c, desc_c) in enumerate(rows_ctrl):
            ry = 364 + idx * 40
            els.append(pill(414, ry, tag_c, fg=col_c, bg="#ffffff", w=76, h=22, size=9.6))
            els.append(txt(498, ry + 15, desc_c[:18], 9.5, INK, weight="600"))
            els.append(txt(498, ry + 30, desc_c[18:], 9.3, BODY))

        return figure(
            518,
            "星舰304L不锈钢与1.8万片六角石英隔热瓦多层防护及拍肚皮襟翼气动控制原理图",
            "左图对比铝合金约160°C软化与304L不锈钢约800°C保强度的耐温差距，剖解钝头脱体激波、密度0.34 g/cm^3六角多孔石英瓦、陶瓷毡与Pyron二次烧蚀层、焊钉机械卡扣不锈钢壁五层防热体系；右图展示星舰65至90度大迎角横躺拍肚皮（终端速度约80 m/s）时四片襟翼向背风侧0至80度收放控制俯仰、横滚与偏航的跳伞力学。",
            els,
            extra_defs=EXTRA_ARR,
        )

    # 5. Lossless Convexification (SOCP) + 18-Second Flip-and-Catch + Flight 1-15 Scoreboard
    def _build_convex_guidance_and_flip():
        # Mathematical verification of non-convex thrust ring vs convex SOCP cone
        t_min, t_max = 1.0, 2.2
        ang_rad = math.radians(22.0)
        ta = (-t_min * math.sin(ang_rad), t_min * math.cos(ang_rad))
        tb = (+t_min * math.sin(ang_rad), t_min * math.cos(ang_rad))
        t_mid_norm = math.hypot(0.5 * (ta[0] + tb[0]), 0.5 * (ta[1] + tb[1]))
        assert t_mid_norm < t_min  # Midpoint strictly violates non-convex lower bound!
        sigma_mid = 0.5 * (t_min + t_min)
        assert t_mid_norm <= sigma_mid and t_min <= sigma_mid <= t_max  # Valid inside lifted SOCP!

        els = header(
            "毫秒级“算命大脑”与最后 18 秒神龙摆尾：怎样把百吨飞船塞进两根铁臂？",
            "左上：无损凸优化把“带洞禁区”变成凸锥｜右上：Ship 42 翻身入筷轨迹｜下：15 次试飞通关表",
        )

        # Top-Left Card: Lossless Convexification (LCvx / SOCP)
        els.append(card(20, 62, 352, 308))
        els.append(txt(36, 84, "① 飞控算法核心：无损凸化（LCvx → 二阶锥规划）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(36, 102, "发动机无法节流至零（0 < T_min ≤ ‖T‖ ≤ T_max），可行域带空洞", 9.6, MUTED))

        # Mini-plot A: Non-Convex Thrust Ring Sector (cx=108, cy=218)
        cx1, cy1 = 108.0, 224.0
        r1, r2 = 30.0, 62.0
        th = math.radians(38.0)
        # Outer arc from -38 to +38 deg around +up, inner arc back
        x_o1, y_o1 = cx1 - r2 * math.sin(th), cy1 - r2 * math.cos(th)
        x_o2, y_o2 = cx1 + r2 * math.sin(th), cy1 - r2 * math.cos(th)
        x_i2, y_i2 = cx1 + r1 * math.sin(th), cy1 - r1 * math.cos(th)
        x_i1, y_i1 = cx1 - r1 * math.sin(th), cy1 - r1 * math.cos(th)
        els.append(
            f'<path d="M {x_o1:.1f},{y_o1:.1f} A {r2:.1f},{r2:.1f} 0 0 1 {x_o2:.1f},{y_o2:.1f} '
            f'L {x_i2:.1f},{y_i2:.1f} A {r1:.1f},{r1:.1f} 0 0 0 {x_i1:.1f},{y_i1:.1f} Z" '
            f'fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>'
        )
        # Forbidden inner hole < T_min
        els.append(
            f'<path d="M {cx1:.1f},{cy1:.1f} L {x_i1:.1f},{y_i1:.1f} A {r1:.1f},{r1:.1f} 0 0 1 {x_i2:.1f},{y_i2:.1f} Z" '
            f'fill="#fee2e2" stroke="#dc2626" stroke-width="1.2" stroke-dasharray="3 2"/>'
        )
        # Segment AB cutting across forbidden hole!
        pa_x, pa_y = cx1 - 24.0, cy1 - 22.0
        pb_x, pb_y = cx1 + 24.0, cy1 - 22.0
        els.append(f'<line x1="{pa_x:.1f}" y1="{pa_y:.1f}" x2="{pb_x:.1f}" y2="{pb_y:.1f}" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="3 2"/>')
        els.append(f'<circle cx="{pa_x:.1f}" cy="{pa_y:.1f}" r="3.4" fill="{ORANGE}"/>')
        els.append(f'<circle cx="{pb_x:.1f}" cy="{pb_y:.1f}" r="3.4" fill="{ORANGE}"/>')
        els.append(f'<circle cx="{cx1:.1f}" cy="{pa_y:.1f}" r="3.4" fill="#dc2626"/>')

        els.append(txt(cx1, 144, "原始推力域（非凸！）", 10.0, "#dc2626", "middle", weight="700"))
        els.append(txt(cx1, 240, "熄火禁区 ‖T‖<T_min", 9.1, "#dc2626", "middle", weight="600"))
        els.append(txt(cx1, 255, "两点连线掉进死洞", 9.1, MUTED, "middle"))

        # Arrow between plots
        els.append(f'<line x1="176" y1="196" x2="206" y2="196" stroke="{GREEN}" stroke-width="2.2" marker-end="url(#ss-green)"/>')
        els.append(txt(191, 186, "升维松弛", 9.2, GREEN, "middle", weight="700"))
        els.append(txt(191, 212, "σ ≥ ‖T‖", 9.2, GREEN, "middle", weight="700"))

        # Mini-plot B: Lifted Convex Second-Order Cone slice (cx=282, cy=224)
        cx2, cy2 = 282.0, 224.0
        # Trapezoid slice of cone ||T|| <= sigma, T_min <= sigma <= T_max
        s1, s2 = 28.0, 62.0
        w1, w2 = 22.0, 48.0
        els.append(
            f'<polygon points="{cx2 - w2:.1f},{cy2 - s2:.1f} {cx2 + w2:.1f},{cy2 - s2:.1f} '
            f'{cx2 + w1:.1f},{cy2 - s1:.1f} {cx2 - w1:.1f},{cy2 - s1:.1f}" '
            f'fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.7"/>'
        )
        els.append(f'<line x1="{cx2 - 54:.1f}" y1="{cy2:.1f}" x2="{cx2 + 54:.1f}" y2="{cy2:.1f}" stroke="{HAIRLINE}" stroke-width="1.1"/>')
        els.append(f'<line x1="{cx2:.1f}" y1="{cy2 + 6:.1f}" x2="{cx2:.1f}" y2="{cy2 - 70:.1f}" stroke="{HAIRLINE}" stroke-width="1.1"/>')
        # Valid convex chord inside filled trapezoid
        els.append(f'<line x1="{cx2 - 22:.1f}" y1="{cy2 - 36:.1f}" x2="{cx2 + 26:.1f}" y2="{cy2 - 48:.1f}" stroke="{GREEN}" stroke-width="2.0"/>')
        els.append(f'<circle cx="{cx2 - 22:.1f}" cy="{cy2 - 36:.1f}" r="3.4" fill="{GREEN}"/>')
        els.append(f'<circle cx="{cx2 + 26:.1f}" cy="{cy2 - 48:.1f}" r="3.4" fill="{GREEN}"/>')

        els.append(txt(cx2, 144, "二阶锥 SOCP（实心凸集！）", 10.0, GREEN, "middle", weight="700"))
        els.append(txt(cx2, 240, "全局唯一最优·毫秒级收敛", 9.1, GREEN, "middle", weight="700"))
        els.append(txt(cx2, 255, "最优解自动贴回边界 ‖T*‖=σ*", 9.1, BODY, "middle"))

        # Bottom explanation inside Top-Left Card
        els.append(card(34, 272, 324, 84, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(46, 291, "• 为什么叫“无损”？庞特里亚金极大值原理严格证明：省油目标会", 9.5, BODY))
        els.append(txt(46, 309, "  自动把松弛解推回锥面 ‖T*(t)‖ = σ*(t)，没有半点物理失真！", 9.5, BLUE, weight="700"))
        els.append(txt(46, 329, "• 顶着 >45 m/s 高空妖风，机载定制求解器每秒重算轨迹，把", 9.5, BODY))
        els.append(txt(46, 346, "  公里级散布硬生生收束到亚米级筷子夹缝（Blackmore, NAE 2017）。", 9.5, INK, weight="600"))

        # Top-Right Card: Final 18-Second Flip-and-Catch Strobe Kinematics
        els.append(card(388, 62, 352, 308))
        els.append(txt(404, 84, "② 最后 18 秒“神龙摆尾”（Ship 42 捕获轨迹实算）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(404, 102, "T+22:32:16 三台海平面猛禽点火 → T+22:32:34 双销稳落 Pad 2 塔臂", 9.9, MUTED))

        # Plot box inside Top-Right Card: Pad 2 Tower on right (x_tower = 678)
        els.append(f'<line x1="406" y1="348" x2="726" y2="348" stroke="{SLATE}" stroke-width="1.5"/>')
        # Pad 2 Mechazilla Tower (146 m scaled cleanly: ground y=348, top y=236, catch rail y=288)
        els.append(f'<rect x="688" y="232" width="12" height="116" rx="2" fill="#cbd5e1" stroke="{SLATE}" stroke-width="1.3"/>')
        els.append(f'<line x1="654" y1="288" x2="688" y2="288" stroke="{GREEN}" stroke-width="3.4"/>')
        els.append(txt(700, 224, "Pad 2 捕获塔", 9.3, SLATE, "middle", weight="700"))

        # 4 Strobe poses kept strictly inside Top-Right Card [388 .. 740]
        poses = [
            (448, 136, -86, 18, "1", ORANGE, "t=0s (540m, 80m/s)：横躺点火，猛摆 15°", 474, 134, "start"),
            (504, 186, -42, 16, "2", ORANGE, "t=4s (310m)：前展后收，甩尾抬头", 526, 184, "start"),
            (586, 234, +9, -12, "3", PURPLE, "t=9s (175m)：反向微摆刹住横移", 566, 238, "end"),
            (662, 294, 0, 0, "4", GREEN, "t=18s (95m, 0m/s)：零速双销落轨关机！", 642, 316, "end"),
        ]
        # Dashed trajectory curve through poses
        els.append(
            '<path d="M 448,136 Q 474,166 504,186 Q 542,212 586,234 Q 626,262 662,294" '
            f'fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="4 3"/>'
        )
        for px, py, rdeg, pdeg, bn, bcol, blbl, lx, ly, lanc in poses:
            els.append(f'<g transform="translate({px},{py}) rotate({rdeg})">')
            els.append(f'<path d="M0,-20 Q5,-12 5,-4 L5,16 L-5,16 L-5,-4 Q-5,-12 0,-20 Z" fill="#ffffff" stroke="{INK}" stroke-width="1.5"/>')
            if bn != "4":
                els.append(f'<g transform="translate(0,16) rotate({pdeg})"><polygon points="-3.5,0 3.5,0 0,15" fill="{ORANGE}" fill-opacity="0.85"/></g>')
            else:
                els.append(f'<rect x="-9" y="-8" width="4" height="3" fill="{ORANGE}"/>')
                els.append(f'<rect x="5" y="-8" width="4" height="3" fill="{ORANGE}"/>')
            els.append("</g>")
            els.append(txt(lx, ly, blbl, 9.2, bcol if bn == "4" else BODY, lanc, weight="700" if bn == "4" else "600", halo=True))

        # Bottom Full-Width Card: Flight 1 to Flight 15 Verified Evolution Scoreboard
        els.append(card(20, 382, 720, 136))
        els.append(txt(36, 404, "③ 从炸毁水泥台到天地双级塔捕：星舰 15 次综合试飞（2023.04 ～ 2026.11）通关时间线", PANEL_TITLE, INK, weight="700"))

        milestones = [
            ("2023.04–11", "F1–F2", SLATE, SLATE_SOFT, ["• F1 后加装水冷钢板", "• F2 首验级间热分离", "• 33 台猛禽全推升空"]),
            ("2024.06.06", "Flight 4", BLUE, BLUE_SOFT, ["• 一级海面软溅落成功", "• 二级襟翼烧穿仍控姿", "• 双级首次完整走完全程"]),
            ("2024.10.13", "Flight 5", ORANGE, ORANGE_SOFT, ["• 人类首次塔臂半空夹住", "  超重助推器 B12！", "• 随后 F7/F8 再连捕两次"]),
            ("2025–26.09", "F9–F14", PURPLE, PURPLE_SOFT, ["• F9 首飞复用助推器 B14", "• F12 首飞 V3 与猛禽 3", "• F14 首入正轨放 26 星"]),
            ("2026.11.14", "Flight 15", GREEN, GREEN_SOFT, ["• Ship 42 放 26 颗星链后", "  绕地 14 圈（22.5 小时）", "• 人类首次塔捕入轨二级！"]),
        ]
        for idx, (dt_s, fl_s, col_m, bg_m, lines_m) in enumerate(milestones):
            mx = 34 + idx * 140
            els.append(card(mx, 416, 132, 90, rx=8, fill=bg_m, stroke=col_m))
            els.append(txt(mx + 66, 433, f"{dt_s} · {fl_s}", 9.5, col_m, "middle", weight="700"))
            els.append(f'<line x1="{mx + 8}" y1="440" x2="{mx + 124}" y2="440" stroke="{BORDER}" stroke-width="1"/>')
            for li, ltxt in enumerate(lines_m):
                els.append(txt(mx + 8, 456 + li * 17, ltxt, 9.0, BODY, weight="700" if (idx in (2, 4) and li >= 1) else None))
            if idx < 4:
                els.append(f'<line x1="{mx + 132}" y1="461" x2="{mx + 140}" y2="461" stroke="{col_m}" stroke-width="1.6"/>')

        return figure(
            532,
            "星舰无损凸优化二阶锥制导原理、最后18秒神龙摆尾翻身捕获轨迹与15次试飞演进图",
            "左上图对比带熄火禁区的非凸推力圆环扇区与引入松弛变量后升维而成的实心二阶锥规划（SOCP）凸集，解释机载计算机毫秒级实时重算亚米级轨迹的数学原理；右上图绘制Flight 15任务中Ship 42在540米高度横躺点火、甩尾竖直、微反向消速至95米零速落入Pad 2筷子的18秒动力学过程；下图汇总2023年4月Flight 1至2026年11月14日Flight 15首次捕获入轨二级的五阶段里程碑。",
            els,
            extra_defs=EXTRA_ARR,
        )

    @register("starship-recovery", "SpaceX星舰双级回收原理：28倍比动能账单、热分离与筷子捕助推器、全流量猛禽与鼻锥小贮箱、六角隔热瓦拍肚皮与无损凸优化翻身捕获", "mechanics_sky")
    def build_starship_recovery():
        write_svg(SUBDIR, "mass-penalty-and-two-stage-energy-gap.svg", _build_energy_gap_and_no_legs())
        write_svg(SUBDIR, "super-heavy-hot-staging-and-chopstick-catch.svg", _build_super_heavy_catch_anim())
        write_svg(SUBDIR, "raptor-ffsc-and-header-tank-slosh-shield.svg", _build_raptor_and_header_tanks())
        write_svg(SUBDIR, "starship-tps-tiles-and-belly-flop-aerodynamics.svg", _build_tps_and_belly_flop())
        write_svg(SUBDIR, "lossless-convex-guidance-and-flip-burn-timeline.svg", _build_convex_guidance_and_flip())


_register_starship_recovery()


# ---------------------------------------------------------------------------
# Clouds, Rain, Lightning & Thunder: Microphysics, Charging, Discharge & Sound
# ---------------------------------------------------------------------------
def _register_weather_thunderstorm():
    SUBDIR = "weather-thunderstorm"
    RED = "#b91c1c"
    RED_SOFT = "#fef2f2"
    TEAL = "#0f766e"
    TEAL_SOFT = "#f0fdfa"
    AMBER = "#b45309"
    AMBER_SOFT = "#fffbeb"

    # 1. Exact Stokes fall speed for r = 10 um droplet in 20 C air
    RHO_W = 1000.0
    G_ACC = 9.81
    ETA_AIR = 1.81e-5
    VT_10UM = 2.0 * RHO_W * G_ACC * (10e-6) ** 2 / (9.0 * ETA_AIR)
    assert 0.0115 < VT_10UM < 0.0126  # ~1.20 cm/s

    # 2. Kohler curve parameters at T = 283 K for r_dry = 0.04 um NaCl sea-salt CCN
    A_KELVIN = 1.15e-3  # um
    B_RAOULT = 1.334 * (0.04 ** 3)  # um^3
    R_CRIT = math.sqrt(3.0 * B_RAOULT / A_KELVIN)
    S_CRIT_PCT = 100.0 * (math.exp(A_KELVIN / R_CRIT - B_RAOULT / (R_CRIT ** 3)) - 1.0)
    assert 0.44 < R_CRIT < 0.50 and 0.15 < S_CRIT_PCT < 0.19

    # 3. Buck (1981) saturation vapor pressure over supercooled liquid water vs hexagonal ice (Pa)
    def es_liquid_pa(tc: float) -> float:
        return 611.21 * math.exp((18.678 - tc / 234.5) * tc / (257.14 + tc))

    def es_ice_pa(tc: float) -> float:
        return 611.15 * math.exp((23.036 - tc / 333.7) * tc / (279.82 + tc))

    gaps = [(tc_i * 0.5, es_liquid_pa(tc_i * 0.5) - es_ice_pa(tc_i * 0.5)) for tc_i in range(-80, 1)]
    peak_tc, peak_de = max(gaps, key=lambda kv: kv[1])
    assert -13.0 < peak_tc < -11.5 and 26.0 < peak_de < 27.5

    def _build_cloud_buoyancy_and_kohler():
        els = header(
            "一、500 吨重的大白云为什么不掉下来？——绝热抬升、凝结核与科勒曲线",
            "1 km³ 晴天积云重达 500 吨：靠 10 微米水滴每秒仅落 1.2 厘米悬空，靠吸湿盐核跨过曲率势垒",
        )

        # Panel A: Adiabatic Lifting LCL + 500-tonne Cumulus Floating Mechanics
        els.append(card(20, 64, 362, 452))
        els.append(pill(34, 76, "A · 绝热抬升成云 + 500 吨白云悬空账", fg=BLUE, bg=BLUE_SOFT, w=334))

        # Schematic of rising thermal parcel & flat LCL cloud base
        els.append(card(34, 110, 334, 212, rx=8, fill="#f8fafc", stroke=BORDER))
        # Ground strip
        els.append('<rect x="44" y="294" width="314" height="16" rx="3" fill="#dcfce7" stroke="#16a34a" stroke-width="1"/>')
        els.append(txt(201, 306, "太阳晒热地面：暖湿气团 T=28°C, 露点 18°C", 11.5, GREEN, anchor="middle", weight="700"))

        # Updraft arrows
        for ux in (135, 201, 267):
            els.append(f'<line x1="{ux}" y1="290" x2="{ux}" y2="232" stroke="{ORANGE}" stroke-width="2.0" stroke-dasharray="4 3"/>')
        els.append(txt(201, 262, "上升膨胀绝热冷却 (−9.8°C/km)", 11.5, ORANGE, anchor="middle", weight="700", halo=True))
        els.append(txt(201, 281, "上升气流 w ≈ 100–200 cm/s", 11.5, BODY, anchor="middle", halo=True))

        # Cloud body above LCL
        els.append(card(66, 118, 270, 80, rx=22, fill="#ffffff", stroke=BLUE_LINE, sw=2.0))
        els.append(txt(201, 141, "1 km³ 晴天积云（含水 0.5 g/m³）", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(201, 161, "总水重 = 500 吨（≈ 100 头成年大象！）", 11.5, BLUE, anchor="middle", weight="700"))
        els.append(txt(201, 181, f"拆成 10¹⁴ 颗 10μm 微滴：沉降仅 {VT_10UM*100:.1f} cm/s！", 11.5, TEAL, anchor="middle", weight="700"))

        # LCL dashed line (flat cloud base!) cleanly below cloud card
        els.append(f'<line x1="46" y1="206" x2="356" y2="206" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="5 3"/>')
        els.append(txt(201, 223, "↑ 抬升凝结高度 LCL (~1.25km 达100%饱和→平云底)", 11.5, BLUE, anchor="middle", weight="700", halo=True))

        # Bottom fall speed comparison card
        els.append(card(34, 334, 334, 168, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.1))
        els.append(txt(46, 355, "为什么云掉不下来，变大成雨滴却能砸下来？", 11.5, BLUE, weight="700"))
        bars_v = [
            ("10 μm 云滴", "0.012 m/s (被微弱上升气流稳稳托住)", 16, TEAL),
            ("100 μm 毛毛雨", "0.70 m/s  (开始缓慢飘落出云底)", 84, AMBER),
            ("1 mm 标准雨滴", "6.50 m/s  (冲破上升气流倾盆而下!)", 218, BLUE),
        ]
        for idx, (b_lbl, b_val, b_w, b_col) in enumerate(bars_v):
            by = 374 + idx * 40
            els.append(txt(46, by + 12, b_lbl, 11.5, INK, weight="700"))
            els.append(f'<rect x="138" y="{by}" width="{b_w}" height="15" rx="3" fill="{b_col}" fill-opacity="0.22" stroke="{b_col}" stroke-width="1.2"/>')
            els.append(txt(46, by + 29, b_val, 11.5, BODY))

        # Panel B: Exact Kohler Curve (Kelvin Curvature Barrier vs Raoult Hygroscopic Salt CCN)
        els.append(card(396, 64, 344, 452))
        els.append(pill(410, 76, "B · 科勒曲线 (1936)：无凝结核湿透也难结云", fg=TEAL, bg=TEAL_SOFT, w=316))

        kx0, kx1 = 456, 722
        ky_top, ky_bot = 122, 342

        def px_r(r_um):
            # Log10 scale from 0.06 um to 3.0 um
            lo, hi = math.log10(0.06), math.log10(3.0)
            return kx0 + (math.log10(r_um) - lo) / (hi - lo) * (kx1 - kx0)

        def py_rh(rh_pct):
            # RH from 99.4% to 101.0%
            return ky_bot - ((rh_pct - 99.4) / 1.6) * (ky_bot - ky_top)

        for rh_t in (99.5, 100.0, 100.5, 101.0):
            yy = py_rh(rh_t)
            st_w = "1.4" if abs(rh_t - 100.0) < 1e-6 else "0.9"
            st_c = INK if abs(rh_t - 100.0) < 1e-6 else BORDER
            els.append(f'<line x1="{kx0}" y1="{yy:.1f}" x2="{kx1}" y2="{yy:.1f}" stroke="{st_c}" stroke-width="{st_w}"/>')
            els.append(txt(kx0 - 6, yy + 4, f"{rh_t:.1f}%", 11.5, MUTED, anchor="end", cls="mono"))

        for r_t, r_lbl in ((0.1, "0.1"), (0.3, "0.3"), (1.0, "1.0"), (3.0, "3.0")):
            xx = px_r(r_t)
            els.append(f'<line x1="{xx:.1f}" y1="{ky_top}" x2="{xx:.1f}" y2="{ky_bot}" stroke="{BORDER}" stroke-width="0.8"/>')
            els.append(txt(xx, ky_bot + 16, r_lbl, 11.5, MUTED, anchor="middle", cls="mono"))

        els.append(f'<line x1="{kx0}" y1="{ky_top}" x2="{kx0}" y2="{ky_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{kx0}" y1="{ky_bot}" x2="{kx1}" y2="{ky_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(txt((kx0 + kx1) / 2, ky_bot + 35, "液滴半径 r (μm，对数坐标)", 11.5, INK, anchor="middle", weight="700"))

        # Pure Kelvin curve 100 * exp(A/r) (clamped inside plot)
        pts_kelv = []
        for i in range(80):
            rv = 0.12 * ((3.0 / 0.12) ** (i / 79.0))
            rh_k = 100.0 * math.exp(A_KELVIN / rv)
            if rh_k <= 101.02:
                pts_kelv.append(f"{px_r(rv):.1f},{py_rh(rh_k):.1f}")
        els.append(f'<polyline points="{" ".join(pts_kelv)}" fill="none" stroke="{RED}" stroke-width="2.2" stroke-dasharray="5 3"/>')

        # Kohler curve 100 * exp(A/r - B/r^3)
        pts_koh = []
        for i in range(100):
            rv = 0.082 * ((3.0 / 0.082) ** (i / 99.0))
            rh_c = 100.0 * math.exp(A_KELVIN / rv - B_RAOULT / (rv ** 3))
            if 99.42 <= rh_c <= 101.0:
                pts_koh.append(f"{px_r(rv):.1f},{py_rh(rh_c):.1f}")
        els.append(f'<polyline points="{" ".join(pts_koh)}" fill="none" stroke="{TEAL}" stroke-width="2.6"/>')

        cx_p, cy_p = px_r(R_CRIT), py_rh(100.0 + S_CRIT_PCT)
        els.append(f'<circle cx="{cx_p:.1f}" cy="{cy_p:.1f}" r="4.8" fill="{TEAL}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(px_r(0.22), py_rh(100.82), "纯水曲率势垒 (无核需>300%!)", 11.5, RED, weight="700", halo=True))
        els.append(txt(cx_p + 8, cy_p - 8, f"盐核激活峰 {100+S_CRIT_PCT:.2f}%", 11.5, TEAL, weight="700", halo=True))

        els.append(card(410, 392, 316, 110, rx=8, fill=TEAL_SOFT, stroke=TEAL, sw=1.1))
        els.append(txt(422, 413, "• 纯净无尘空气：1 nm 胚胎表面弯曲极陡，水分子", 11.5, BODY))
        els.append(txt(422, 433, "  极易挣脱蒸发，相对湿度飙到 300%–400% 才凝结；", 11.5, RED, weight="700"))
        els.append(txt(422, 454, "• 真实大气靠海盐、硫酸盐等“云凝结核 CCN”：", 11.5, BODY))
        els.append(txt(422, 474, "  溶质锁水拉平势垒，湿度刚过 100.2% 即刻成云！", 11.5, INK, weight="700"))

        return figure(
            530,
            "晴天积云500吨悬空力学与科勒曲线云凝结核激活原理图解",
            "左图展示暖湿气团按每公里9.8摄氏度绝热冷却在抬升凝结高度形成平云底，以及1立方公里积云含500吨水却因10微米水滴沉降仅每秒1.2厘米而悬空；右图精确计算科勒曲线，对比纯水开尔文曲率势垒与海盐凝结核在100.18%湿度激活成云。",
            els,
        )

    def _build_bergeron_and_raindrop_shape():
        els = header(
            "二、体积暴涨一百万倍才能下雨：冷云“冰晶夺水”与雨滴真实的汉堡包形状",
            "单靠水汽扩散长成雨滴要熬十几个小时；大自然靠 −12 °C 冰晶抢水汽与暖云碰并走高速捷径",
        )

        # Panel A: Exact Bergeron-Findeisen Vapor Pressure Gap Curve (-40 C to 0 C)
        els.append(card(20, 64, 370, 452))
        els.append(pill(34, 76, "A · 贝吉龙机制：−12 °C 冰晶怎样吸干过冷水滴", fg=BLUE, bg=BLUE_SOFT, w=342))

        bx0, bx1 = 68, 368
        by_top, by_bot = 122, 306

        def px_t(tc):
            return bx0 + (tc + 40.0) / 40.0 * (bx1 - bx0)

        def py_de(de_pa):
            return by_bot - (de_pa / 32.0) * (by_bot - by_top)

        for y_v in (0, 10, 20, 30):
            yy = py_de(y_v)
            els.append(f'<line x1="{bx0}" y1="{yy:.1f}" x2="{bx1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.9"/>')
            els.append(txt(bx0 - 6, yy + 4, f"{y_v}", 11.5, MUTED, anchor="end", cls="mono"))

        for t_v in (-40, -30, -20, -12, 0):
            xx = px_t(t_v)
            els.append(f'<line x1="{xx:.1f}" y1="{by_top}" x2="{xx:.1f}" y2="{by_bot}" stroke="{BORDER}" stroke-width="0.8"/>')
            els.append(txt(xx, by_bot + 16, f"{t_v}°C", 11.5, MUTED, anchor="middle", cls="mono"))

        els.append(f'<line x1="{bx0}" y1="{by_top}" x2="{bx0}" y2="{by_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{bx0}" y1="{by_bot}" x2="{bx1}" y2="{by_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(txt((bx0 + bx1) / 2, by_bot + 35, "水面对冰面饱和蒸汽压差 Δe_s (Pa)", 11.5, INK, anchor="middle", weight="700"))

        t_vals = [i * 0.5 for i in range(-80, 1)]
        poly_g = [f"{px_t(-40):.1f},{by_bot:.1f}"] + [f"{px_t(t):.1f},{py_de(es_liquid_pa(t) - es_ice_pa(t)):.1f}" for t in t_vals] + [f"{px_t(0):.1f},{by_bot:.1f}"]
        els.append(f'<polygon points="{" ".join(poly_g)}" fill="{BLUE_SOFT}" fill-opacity="0.75"/>')
        pts_g = [f"{px_t(t):.1f},{py_de(es_liquid_pa(t) - es_ice_pa(t)):.1f}" for t in t_vals]
        els.append(f'<polyline points="{" ".join(pts_g)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

        px_pk, py_pk = px_t(peak_tc), py_de(peak_de)
        els.append(f'<circle cx="{px_pk:.1f}" cy="{py_pk:.1f}" r="4.8" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(txt(px_pk - 18, py_pk - 10, f"黄金造雨温区 {peak_tc:.1f}°C ({peak_de:.1f} Pa)", 11.5, ORANGE, anchor="middle", weight="700", halo=True))

        # Cold-cloud WBF 3-step chain card
        els.append(card(34, 356, 342, 146, rx=8, fill="#f8fafc", stroke=BLUE, sw=1.1))
        els.append(txt(46, 377, "中纬度大部分降雨，半空出生时其实是雪花！", 11.5, BLUE, weight="700"))
        els.append(txt(46, 398, "① 0 至 −38°C 云层里，大量过冷水滴与少量冰晶共存；", 11.5, BODY))
        els.append(txt(46, 419, "② 冰面锁水更紧（蒸汽压低 13%），空气对水滴刚饱和，", 11.5, BODY))
        els.append(txt(46, 440, "   对冰晶却严重过饱和 → 水汽从水滴蒸发直奔冰晶疯长；", 11.5, INK, weight="700"))
        els.append(txt(46, 461, "③ 冰晶粘连成雪片坠落，穿过 0°C 融化层化作大雨滴！", 11.5, TEAL, weight="700"))
        els.append(txt(46, 482, "   （碘化银人工增雨正是撒入仿冰晶格的“催化火种”）", 11.5, MUTED))

        # Panel B: Warm-Cloud Collision-Coalescence + NASA GPM Real Raindrop Shape
        els.append(card(404, 64, 336, 452))
        els.append(pill(418, 76, "B · 百万合一暖云碰并 & 雨滴真实形状", fg=ORANGE, bg=ORANGE_SOFT, w=308))

        els.append(card(418, 110, 308, 132, rx=8, fill=AMBER_SOFT, stroke=AMBER, sw=1.1))
        els.append(txt(430, 131, "热带暖云（全在 0°C 以上）靠什么 20 分钟下雨？", 11.5, AMBER, weight="700"))
        els.append(txt(430, 152, "• 体积鸿沟：(1 mm / 10 μm)³ = 1,000,000 颗云滴！", 11.5, INK, weight="700"))
        els.append(txt(430, 173, "• 大海盐核先造出少量 >25 μm“领跑大水滴”，", 11.5, BODY))
        els.append(txt(430, 194, "  下落更快 → 像滚雪球一路追尾吞并下方小云滴，", 11.5, BODY))
        els.append(txt(430, 215, "  越撞越大、越重越快，指数级加速冲破上升气流！", 11.5, TEAL, weight="700"))

        # NASA GPM Real Raindrop Shapes (4 stages)
        els.append(card(418, 254, 308, 248, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(430, 275, "NASA GPM 实测：雨滴绝不是绘本里的“泪滴形”！", 11.5, RED, weight="700"))

        # 4 shape mini-boxes (2x2 grid inside 418..726)
        # Box 1: <1 mm sphere
        els.append(card(428, 290, 138, 94, rx=6, fill="#ffffff", stroke=BORDER))
        els.append(f'<circle cx="497" cy="324" r="13" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>')
        els.append(txt(497, 356, "① < 1 mm 小雨滴", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(497, 374, "表面张力主导：正圆球", 11.5, BLUE, anchor="middle"))

        # Box 2: 2-3 mm hamburger bun!
        els.append(card(578, 290, 138, 94, rx=6, fill="#ffffff", stroke=BORDER))
        els.append(f'<path d="M 625,332 C 625,308 669,308 669,332 Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>')
        els.append(txt(647, 356, "② 2–3 mm 中大雨滴", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(647, 374, "底面风压顶平：汉堡包", 11.5, TEAL, anchor="middle", weight="700"))

        # Box 3: 4.5 mm kidney bean / parachute
        els.append(card(428, 394, 138, 96, rx=6, fill="#ffffff", stroke=BORDER))
        els.append(f'<path d="M 471,438 C 471,408 523,408 523,438 Q 497,426 471,438 Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2"/>')
        els.append(txt(497, 460, "③ ~4.5 mm 巨型雨滴", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(497, 478, "底面凹陷成蚕豆伞状", 11.5, AMBER, anchor="middle"))

        # Box 4: >5 mm breakup
        els.append(card(578, 394, 138, 96, rx=6, fill="#ffffff", stroke=BORDER))
        for cx_d, cy_d, rr_d in ((630, 424, 6), (650, 418, 5), (664, 428, 7), (642, 434, 5)):
            els.append(f'<circle cx="{cx_d}" cy="{cy_d}" r="{rr_d}" fill="{BLUE_SOFT}" stroke="{RED}" stroke-width="1.7"/>')
        els.append(txt(647, 460, "④ > 5 mm 气动极限", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(647, 478, "张力兜不住：空中解体!", 11.5, RED, anchor="middle", weight="700"))

        return figure(
            530,
            "冷云贝吉龙冰晶夺水蒸汽压差实算曲线、暖云碰并增长与NASA雨滴真实汉堡包形状演化图解",
            "左图按Buck饱和蒸汽压方程绘出0至-40°C水面与冰面蒸汽压差曲线，在-12.3°C达峰值26.9帕，解释冰晶吸干过冷水滴化雪成雨的机制；右图展示百万云滴暖云碰并，并给出小于1毫米圆球、2至3毫米汉堡包形、4.5毫米凹陷伞形及超5毫米空中解体的真实雨滴形态。",
            els,
        )

    def _build_thundercloud_charging_engine():
        els = header(
            "三、云里既没铜线也没磁铁，凭什么攒出十亿伏高压？——霰冰碰撞起电引擎",
            "上升气流托着微冰晶往上跑，重霰粒往下砸：−15 °C 之上每次碰撞搬运约 33 飞库仑电荷",
        )

        # Panel A: 12 km Cumulonimbus Tripolar Charge Structure & Lightning Types
        els.append(card(20, 64, 372, 452))
        els.append(pill(34, 76, "A · 积雨云 12 公里垂直“起电传送带”与三类闪电", fg=PURPLE, bg=PURPLE_SOFT, w=344))

        # Altitude & Temp axis on left of Panel A
        ax_x = 68.0
        y_0km, y_12km = 468.0, 128.0

        def py_km(z_km):
            return y_0km - (z_km / 12.0) * (y_0km - y_12km)

        els.append(f'<line x1="{ax_x}" y1="{y_12km}" x2="{ax_x}" y2="{y_0km}" stroke="{SLATE}" stroke-width="1.3"/>')
        for zk, t_lbl in ((0, "0km"), (4, "4km (0°C)"), (6.5, "6.5km (−15°C)"), (11, "11km (−50°C)")):
            yy = py_km(zk)
            els.append(f'<line x1="{ax_x - 4}" y1="{yy:.1f}" x2="366" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.9" stroke-dasharray="3 3"/>')
            els.append(txt(ax_x - 6, yy + 4, f"{zk:.0f}" if zk in (0, 11) else f"{zk:g}", 11.5, MUTED, anchor="end", cls="mono"))

        # Ground strip with induced positive charges
        els.append('<rect x="74" y="468" width="298" height="22" rx="3" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>')
        els.append(txt(223, 483, "地面感应正电荷影区 ＋ ＋ ＋ ＋ ＋", 11.5, RED, anchor="middle", weight="700"))

        # Cumulonimbus anvil cloud silhouette
        els.append(
            f'<path d="M 118,408 Q 98,340 118,260 Q 112,188 86,154 Q 82,126 150,124 L 336,124 Q 372,128 352,162 Q 312,182 304,254 Q 322,340 296,408 Z" '
            f'fill="#f1f5f9" stroke="{SLATE}" stroke-width="1.8"/>'
        )

        # Upper positive region (+40 C at 8.5-11.5 km)
        els.append(card(126, 136, 184, 52, rx=14, fill=RED_SOFT, stroke=RED, sw=1.3))
        els.append(txt(218, 157, "云砧顶部主正电荷区 (+40 C)", 11.5, RED, anchor="middle", weight="700"))
        els.append(txt(218, 176, "轻盈冰晶被上升气流吹上云顶", 11.5, BODY, anchor="middle"))

        # Middle main negative region (-40 C at 5-7.5 km)
        els.append(card(122, 246, 180, 56, rx=14, fill=BLUE_SOFT, stroke=BLUE, sw=1.4))
        els.append(txt(212, 268, "中部主负电荷饼 (−40 C)", 11.5, BLUE, anchor="middle", weight="700"))
        els.append(txt(212, 288, "−10~−25°C 重霰粒悬停富集", 11.5, BODY, anchor="middle"))

        # Small lower positive pocket (+5 C near 3.5 km)
        els.append(card(146, 354, 132, 34, rx=10, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.1))
        els.append(txt(212, 376, "云底小正电袋 (+5 C)", 11.5, ORANGE, anchor="middle", weight="700"))

        # 3 Lightning Discharge Paths:
        # 1) IC lightning (75-80% inside cloud!)
        els.append(f'<polyline points="172,188 186,214 168,226 184,246" fill="none" stroke="{PURPLE}" stroke-width="2.4"/>')
        els.append(txt(192, 222, "云内闪 IC (占75%–80%)", 11.5, PURPLE, weight="700", halo=True))

        # 2) Normal negative CG (-CG)
        els.append(f'<polyline points="146,302 132,356 144,398 126,436 136,468" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')
        els.append(txt(82, 434, "常规负地闪", 11.5, BLUE, weight="700", halo=True))

        # 3) Positive "Bolt from the Blue" (+CG from anvil top绕过云体劈向远处!)
        els.append(f'<polyline points="310,162 346,238 334,316 354,394 340,468" fill="none" stroke="{RED}" stroke-width="2.6"/>')
        els.append(txt(348, 344, "正地闪!", 11.5, RED, anchor="end", weight="700", halo=True))
        els.append(txt(348, 362, "(晴天霹雳)", 11.5, RED, anchor="end", halo=True))

        # Panel B: Takahashi (1978) Non-Inductive Graupel-Ice Riming Collision + GRAPES-3 1.3 GV
        els.append(card(406, 64, 334, 452))
        els.append(pill(420, 76, "B · 高桥 (1978) 霰冰碰撞起电 & 13 亿伏实测", fg=BLUE, bg=BLUE_SOFT, w=306))

        els.append(card(420, 110, 306, 224, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(432, 131, "绝不是“两朵云摩擦起电”！真实微观三主角：", 11.5, INK, weight="700"))

        # Graupel falling down + Ice crystal rising up collision diagram
        gx_c, gy_c = 548.0, 208.0
        # Falling graupel (rimed soft hail ~2 mm)
        els.append(f'<circle cx="{gx_c}" cy="{gy_c}" r="38" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>')
        els.append(txt(gx_c, gy_c - 4, "重霰粒", 11.5, BLUE, anchor="middle", weight="700"))
        els.append(txt(gx_c, gy_c + 14, "(~2mm, −)", 11.5, BLUE, anchor="middle", weight="700"))
        els.append(f'<line x1="494" y1="168" x2="494" y2="246" stroke="{BLUE}" stroke-width="2.2"/>')
        els.append(f'<polygon points="489,242 499,242 494,251" fill="{BLUE}"/>')
        els.append(txt(486, 212, "重力下坠", 11.5, BLUE, anchor="end", weight="700"))

        # Rising hexagonal ice crystal (~50 um) bouncing off right
        ix_c, iy_c = 622.0, 184.0
        els.append(f'<polygon points="{ix_c},{iy_c-16} {ix_c+14},{iy_c-8} {ix_c+14},{iy_c+8} {ix_c},{iy_c+16} {ix_c-14},{iy_c+8} {ix_c-14},{iy_c-8}" fill="{RED_SOFT}" stroke="{RED}" stroke-width="2.0"/>')
        els.append(txt(ix_c, iy_c + 4, "＋", 12.5, RED, anchor="middle", weight="700"))
        els.append(f'<line x1="648" y1="234" x2="648" y2="156" stroke="{RED}" stroke-width="2.2"/>')
        els.append(f'<polygon points="643,160 653,160 648,151" fill="{RED}"/>')
        els.append(txt(656, 194, "气流托升", 11.5, RED, weight="700"))
        els.append(txt(656, 212, "冰晶 (+)", 11.5, RED, weight="700"))

        els.append(txt(432, 280, "• T < −15°C 时：霰粒冻结过冷水放热表面略暖，", 11.5, BODY))
        els.append(txt(432, 300, "  擦撞冷冰晶瞬间转移质子/电荷（每次约 33 fC）；", 11.5, BODY))
        els.append(txt(432, 320, "• 重力与上升气流分道扬镳，拉开数公里巨型电容！", 11.5, INK, weight="700"))

        # GRAPES-3 1.3 GV + RREA cosmic-ray trigger card
        els.append(card(420, 346, 306, 156, rx=8, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.1))
        els.append(txt(432, 368, "GRAPES-3 宇宙线缪子透视 (PRL, 2019)：", 11.5, PURPLE, weight="700"))
        els.append(txt(432, 389, "• 实测雷暴云总电势高达 1.3 GV（13 亿伏特）！", 11.5, INK, weight="700"))
        els.append(txt(432, 409, "• 充电功率 ≥ 2 GW（堪比两台核电机组满发）！", 11.5, RED, weight="700"))
        els.append(txt(432, 431, "• 击穿之谜：云内宏观电场 (~200 kV/m) 远低于干", 11.5, BODY))
        els.append(txt(432, 451, "  空气击穿阈值 (3,000 kV/m)，全靠冰晶尖端增场", 11.5, BODY))
        els.append(txt(432, 471, "  ＋ 宇宙线相对论逃逸电子雪崩（RREA）点火！", 11.5, PURPLE, weight="700"))

        return figure(
            530,
            "积雨云12公里三极电荷分布、三类闪电路径与高桥1978霰冰非感应碰撞起电机制图解",
            "左图展示积雨云顶部8至12公里主正电荷区、中部4至7公里主负电荷饼、云底小正电袋以及云内闪、常规负地闪和云砧正地闪路径；右图图解霰粒下坠与冰晶上升碰撞分离电荷的微观机制及GRAPES-3实测13亿伏特电势与宇宙线雪崩击穿。",
            els,
        )

    def _build_stepped_leader_return_stroke():
        extra_css = """
  @keyframes return-flash {
    0% { stroke-dashoffset: 260; opacity: 0.35; }
    35% { stroke-dashoffset: 0; opacity: 1.0; }
    100% { stroke-dashoffset: 0; opacity: 1.0; }
  }
  .rs-bolt {
    stroke-dasharray: 260;
    stroke-dashoffset: 0;
    animation: return-flash 2.6s ease-out 1 forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .rs-bolt { animation: none !important; stroke-dashoffset: 0 !important; opacity: 1 !important; }
  }"""

        els = header(
            "四、慢放一万倍看闪电：肉眼以为从天往下劈，最亮那一下其实从地面往上蹿！",
            "20 毫秒暗弱梯级先导下探 → 地面尖端迎面先导升空 → 100 微秒 1/3 光速回击引爆 30,000 K 闪光",
        )

        stages = [
            (
                20,
                "① 0–19 ms · 梯级先导",
                BLUE,
                BLUE_SOFT,
                [
                    "每步 ~50 m 停顿 30 μs",
                    "折线分叉往下试探低阻路",
                    "均速 ~2×10⁵ m/s 极暗弱",
                ],
            ),
            (
                203,
                "② 19.9 ms · 迎面先导",
                ORANGE,
                ORANGE_SOFT,
                [
                    "先导逼近地面 30–100 m",
                    "树尖/避雷针电场急剧畸变",
                    "向上射出正电迎面火花！",
                ],
            ),
            (
                386,
                "③ 20.0 ms · 耀眼回击!",
                RED,
                RED_SOFT,
                [
                    "天地接通瞬间短路导通！",
                    "强光以 1/3 光速自下而上",
                    "狂飙回云端（肉眼所见）!",
                ],
            ),
            (
                569,
                "④ 60–200 ms · 直窜闪烁",
                PURPLE,
                PURPLE_SOFT,
                [
                    "每隔 ~40 ms 残余热通道",
                    "滑下直窜先导再触发回击",
                    "连闪 3–5 次造就肉眼闪烁",
                ],
            ),
        ]

        for idx, (sx, st_title, fg_c, bg_c, lines_s) in enumerate(stages):
            els.append(card(sx, 64, 171, 304))
            els.append(pill(sx + 10, 76, st_title, fg=fg_c, bg=bg_c, w=151, size=11.5))

            # Mini sky-to-ground box inside each stage card (y=108..276)
            els.append(f'<rect x="{sx + 12}" y="108" width="147" height="168" rx="6" fill="#0f172a"/>')
            # Cloud base bar
            els.append(f'<rect x="{sx + 20}" y="114" width="131" height="18" rx="6" fill="#334155"/>')
            els.append(txt(sx + 85.5, 127, "− − − 云底 − − −", 11.5, "#93c5fd", anchor="middle", weight="700"))
            # Ground bar + small lightning rod / tree on right-center
            els.append(f'<rect x="{sx + 12}" y="260" width="147" height="16" rx="2" fill="#14532d"/>')
            rx_rod = sx + 98
            els.append(f'<line x1="{rx_rod}" y1="260" x2="{rx_rod}" y2="238" stroke="#cbd5e1" stroke-width="2.2"/>')

            if idx == 0:
                # Faint branched stepped leader descending halfway
                els.append(f'<polyline points="{sx+80},132 {sx+68},158 {sx+86},182 {sx+74},208" fill="none" stroke="#60a5fa" stroke-width="2.0" stroke-dasharray="5 3"/>')
                els.append(f'<polyline points="{sx+86},182 {sx+108},204" fill="none" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="4 3"/>')
                els.append(txt(sx + 85.5, 232, "↓ 分叉暗弱下探", 11.5, "#93c5fd", anchor="middle"))
            elif idx == 1:
                # Leader near rod + upward red-orange streamer rising from rod!
                els.append(f'<polyline points="{sx+80},132 {sx+68},158 {sx+86},182 {sx+78},206 {sx+92},218" fill="none" stroke="#60a5fa" stroke-width="2.1"/>')
                els.append(f'<polyline points="{sx+68},158 {sx+46},194" fill="none" stroke="#60a5fa" stroke-width="1.4" opacity="0.6"/>')
                els.append(f'<line x1="{rx_rod}" y1="238" x2="{sx+94}" y2="221" stroke="#fb923c" stroke-width="2.8"/>')
                els.append(txt(sx + 54, 248, "↑ 迎面先导!", 11.5, "#fdba74", anchor="middle", weight="700"))
            elif idx == 2:
                # Dazzling return stroke shooting UPWARD from rod to cloud!
                pts_main = f"{rx_rod},238 {sx+92},218 {sx+78},206 {sx+86},182 {sx+68},158 {sx+80},132"
                els.append(f'<polyline points="{pts_main}" fill="none" stroke="#fde047" stroke-width="8.0" stroke-opacity="0.45"/>')
                els.append(f'<polyline points="{pts_main}" fill="none" stroke="#fef9c3" stroke-width="3.6" stroke-opacity="0.85"/>')
                els.append(f'<polyline class="rs-bolt" points="{pts_main}" fill="none" stroke="#ffffff" stroke-width="3.2"/>')
                els.append(txt(sx + 48, 198, "↑ 1/3光速", 11.5, "#fde047", anchor="middle", weight="700"))
                els.append(txt(sx + 48, 215, "自下往上!", 11.5, "#ffffff", anchor="middle", weight="700"))
            else:
                # Multiple parallel-shifted strokes representing 3-5 flicker strokes
                for dx_f, op_f in ((-10, "0.45"), (0, "0.75"), (10, "1.0")):
                    pts_f = f"{sx+76+dx_f},132 {sx+66+dx_f},174 {sx+82+dx_f},212 {sx+88+dx_f},246"
                    els.append(f'<polyline points="{pts_f}" fill="none" stroke="#e9d5ff" stroke-width="2.2" stroke-opacity="{op_f}"/>')
                els.append(txt(sx + 85.5, 254, "×3–5 次连击闪烁", 11.5, "#f3e8ff", anchor="middle", weight="700"))

            for li, l_str in enumerate(lines_s):
                els.append(txt(sx + 85.5, 298 + li * 21, l_str, 11.5, INK if li == 2 else BODY, anchor="middle", weight="700" if li == 2 else "400"))

        # Bottom Wide Physical Benchmarks Card
        els.append(card(20, 380, 720, 146))
        els.append(pill(34, 392, "C · 一道典型云地闪电的三大反直觉物理账单", fg=INK, bg=SLATE_SOFT, w=330))

        bench_cards = [
            (
                34,
                "真实直径：仅 2–3 厘米！",
                [
                    "核心等离子体仅大拇指粗；",
                    "照片里几米宽的光柱全是镜",
                    "头强光过曝晕轮。",
                ],
                BLUE,
                BLUE_SOFT,
            ),
            (
                272,
                "峰值温度：~30,000 K（太阳 5 倍）",
                [
                    "30 kA 巨流微秒灌入指粗通",
                    "道，瞬间烧至约 3 万开尔文，",
                    "达太阳表面 5772 K 的 5.2 倍！",
                ],
                RED,
                RED_SOFT,
            ),
            (
                510,
                "为什么不能靠抓闪电开电厂？",
                [
                    "瞬时功率虽达万亿瓦，却仅",
                    "亮百微秒！单次可捕电能仅",
                    "几百千瓦时，电费约几百元。",
                ],
                TEAL,
                TEAL_SOFT,
            ),
        ]
        for bx_b, bt_b, b_lines, fg_b, bg_b in bench_cards:
            els.append(card(bx_b, 424, 216, 90, rx=8, fill=bg_b, stroke=fg_b, sw=1.1))
            els.append(txt(bx_b + 10, 444, bt_b, 11.5, fg_b, weight="700"))
            for li_b, ln_b in enumerate(b_lines):
                els.append(txt(bx_b + 10, 464 + li_b * 19, ln_b, 11.5, INK if li_b == 2 else BODY, weight="700" if li_b == 2 else "400"))

        return figure(
            540,
            "云地闪电四阶段毫秒级过程（梯级先导、迎面先导、自下而上三分之一光速回击与直窜闪烁）图解",
            "上图按0至200毫秒顺序拆解梯级先导50米步长下探、30至100米击距触发地面上行迎面先导、回击以三分之一光速自地面冲向云底（含无障碍单次闪光动画）及3至5次直窜先导闪烁；下图对比2至3厘米通道直径、30000K高温与总电能账单。",
            els,
            extra_css=extra_css,
        )

    def _build_thunder_shockwave_and_refraction():
        els = header(
            "五、闪电只亮一瞬间，雷声凭什么轰隆十几秒？——超音速激波、声程差与消音盲区",
            "微秒等容暴热炸出几十大气压柱状激波；蜿蜒通道拉出十几秒声程差，高空冷层把雷声往上掰弯",
        )

        # Panel A: Isochoric Shockwave + Crooked Channel Rumble Geometry
        els.append(card(20, 64, 366, 452))
        els.append(pill(34, 76, "A · 柱状激波化声 & 为什么雷声“轰隆隆”拖十几秒", fg=ORANGE, bg=ORANGE_SOFT, w=338))

        els.append(card(34, 110, 338, 86, rx=8, fill=RED_SOFT, stroke=RED, sw=1.1))
        els.append(txt(46, 131, "打雷绝不是“两朵云撞响”，而是空气热爆炸：", 11.5, RED, weight="700"))
        els.append(txt(46, 152, "• 2 cm 空气在几微秒烧至 30,000 K，来不及膨胀，", 11.5, BODY))
        els.append(txt(46, 172, "  压强飙至 10–100 atm → 超音速激波在数米外化为巨响！", 11.5, INK, weight="700"))

        # Arrival-time geometry diagram (y=208..500)
        els.append(card(34, 208, 338, 294, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 229, "同一瞬间的闪电，不同高度雷声排队进耳朵：", 11.5, INK, weight="700"))

        # Ground line: Strike at x=92, Listener at x=318
        gy_g = 434.0
        els.append(f'<line x1="50" y1="{gy_g}" x2="356" y2="{gy_g}" stroke="#16a34a" stroke-width="2.0"/>')
        # Crooked lightning bolt from (82, 250) down to (96, 434)
        els.append(f'<polyline points="82,252 108,296 78,338 106,382 94,434" fill="none" stroke="{ORANGE}" stroke-width="3.0"/>')
        # Listener icon at (306, 434)
        els.append(f'<circle cx="306" cy="414" r="6" fill="{BLUE}"/>')
        els.append(f'<line x1="306" y1="420" x2="306" y2="434" stroke="{BLUE}" stroke-width="2.4"/>')
        els.append(txt(358, 452, "观测者 (距雷 1.5km)", 11.5, BLUE, anchor="end", weight="700"))

        # Three acoustic rays from P1 (bottom 1.5km), P2 (mid kink 3.5km), P3 (cloud top 6.2km)
        rays_th = [
            (94, 424, RED),
            (84, 338, ORANGE),
            (82, 256, PURPLE),
        ]
        for rx_s, ry_s, r_col in rays_th:
            els.append(f'<line x1="{rx_s}" y1="{ry_s}" x2="300" y2="416" stroke="{r_col}" stroke-width="1.5" stroke-dasharray="4 3"/>')
            els.append(f'<circle cx="{rx_s}" cy="{ry_s}" r="4.2" fill="{r_col}"/>')

        els.append(txt(120, 268, "③ 6.2km → 18.1s 低沉隆隆", 11.5, PURPLE, weight="700", halo=True))
        els.append(txt(122, 344, "② 3.5km → 10.2s 轰——!", 11.5, ORANGE, weight="700", halo=True))
        els.append(txt(116, 412, "① 1.5km → 4.4s 炸裂咔嚓!", 11.5, RED, weight="700", halo=True))
        els.append(txt(203, 484, "→ 0.1 秒的闪电，拉出 18.1−4.4 = 13.7 秒滚雷！", 11.5, INK, anchor="middle", weight="700"))

        # Panel B: 3-Second Distance Rule + Upward Acoustic Refraction Shadow Zone (>20 km)
        els.append(card(400, 64, 340, 452))
        els.append(pill(414, 76, "B · 读秒测距公式 & 20 公里外“有闪无雷”盲区", fg=TEAL, bg=TEAL_SOFT, w=312))

        els.append(card(414, 110, 312, 92, rx=8, fill=TEAL_SOFT, stroke=TEAL, sw=1.1))
        els.append(txt(426, 131, "实用救命口诀：看见闪电默数秒数 ÷ 3 ≈ 公里数", 11.5, TEAL, weight="700"))
        els.append(txt(426, 152, "• 光速瞬间到眼；声速 343m/s 约 3 秒跑 1 公里；", 11.5, BODY))
        els.append(txt(426, 173, "• 30 秒法则：闪雷间隔 < 30 秒（距你 < 10 km），", 11.5, RED, weight="700"))
        els.append(txt(426, 191, "  正地闪随时可能劈到头顶，立刻进屋或躲进汽车！", 11.5, INK, weight="700"))

        # Exact Upward Acoustic Refraction Ray Plot (x = 0..26 km, z = 0..5 km)
        rx0, rx1 = 446, 718
        ry_top, ry_bot = 236, 418

        def px_km(x_km):
            return rx0 + (x_km / 26.0) * (rx1 - rx0)

        def pz_km(z_km):
            return ry_bot - (z_km / 5.2) * (ry_bot - ry_top)

        # Shade Acoustic Shadow Zone beyond x = 18.5 km near ground!
        els.append(f'<polygon points="{px_km(17.5):.1f},{ry_bot:.1f} {px_km(26):.1f},{ry_bot:.1f} {px_km(26):.1f},{pz_km(1.7):.1f}" fill="{SLATE_SOFT}"/>')

        for z_t in (0, 2, 4):
            yy = pz_km(z_t)
            els.append(f'<line x1="{rx0}" y1="{yy:.1f}" x2="{rx1}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="0.8"/>')
            els.append(txt(rx0 - 6, yy + 4, f"{z_t}km", 11.5, MUTED, anchor="end", cls="mono"))

        for x_t in (0, 10, 20, 26):
            xx = px_km(x_t)
            els.append(txt(xx, ry_bot + 16, f"{x_t}km" if x_t == 26 else str(x_t), 11.5, MUTED, anchor="middle", cls="mono"))

        els.append(f'<line x1="{rx0}" y1="{ry_top}" x2="{rx0}" y2="{ry_bot}" stroke="{INK}" stroke-width="1.3"/>')
        els.append(f'<line x1="{rx0}" y1="{ry_bot}" x2="{rx1}" y2="{ry_bot}" stroke="#16a34a" stroke-width="2.0"/>')

        # Snell acoustic ray integration in linear sound-speed gradient dc/dz = -3.9 m/s per km
        # z(x) = z0 - tan(alpha0)*x + curvature * x^2 (upward bending!)
        z_src = 2.0
        els.append(f'<circle cx="{px_km(0.5):.1f}" cy="{pz_km(z_src):.1f}" r="5.0" fill="{ORANGE}"/>')
        els.append(txt(px_km(1.2), pz_km(4.55), "高空冷(声速慢) ← 地面暖(声速快)", 11.5, BLUE, weight="700", halo=True))

        for slope0, curv, col_r in [
            (0.32, 0.0065, TEAL),
            (0.226, 0.0065, BLUE),  # grazes z=0 right around x=17.4 km and bends UP!
            (0.14, 0.0065, PURPLE),
        ]:
            r_pts = []
            for xi in range(0, 53):
                xk = 0.5 + xi * 0.49
                zk = z_src - slope0 * (xk - 0.5) + curv * ((xk - 0.5) ** 2)
                if 0.0 <= zk <= 4.9:
                    r_pts.append(f"{px_km(xk):.1f},{pz_km(zk):.1f}")
                elif zk < 0.0:
                    break
            els.append(f'<polyline points="{" ".join(r_pts)}" fill="none" stroke="{col_r}" stroke-width="2.1"/>')

        els.append(txt(px_km(21.8), pz_km(0.45), "声影盲区!", 11.5, RED, anchor="middle", weight="700", halo=True))

        els.append(card(414, 444, 312, 60, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(426, 465, "• 对流层越往高处越冷，声速 c ∝ √T 上慢下快；", 11.5, BODY))
        els.append(txt(426, 486, "• 声波向高空弯折翘起 → 20 km 外“只见闪电不闻雷”", 11.5, INK, weight="700"))

        return figure(
            530,
            "闪电30000K超音速柱状激波生雷、蜿蜒通道声程差滚雷与大气声速梯度向上折射声影盲区图解",
            "左图解释微秒级等容暴热产生10至100大气压激波化为雷声，并按343米每秒声速计算1.5至6.2公里通道各段制造13.7秒滚雷；右图给出读秒除以3测距口诀及对流层上冷下暖导致声线向上折射、在约20公里外形成有闪无雷声影区的实算轨迹。",
            els,
        )

    @register("weather-thunderstorm", "云雨雷电全链条五步物理图解：积云悬空与科勒曲线、贝吉龙冰晶夺水与汉堡包雨滴、霰冰碰撞起电、梯级先导与回击及雷声激波声影区", "mechanics_sky")
    def build_weather_thunderstorm():
        write_svg(SUBDIR, "cloud-buoyancy-and-kohler-curve.svg", _build_cloud_buoyancy_and_kohler())
        write_svg(SUBDIR, "bergeron-ice-robbery-and-raindrop-shape.svg", _build_bergeron_and_raindrop_shape())
        write_svg(SUBDIR, "thundercloud-graupel-charging-engine.svg", _build_thundercloud_charging_engine())
        write_svg(SUBDIR, "stepped-leader-and-return-stroke.svg", _build_stepped_leader_return_stroke())
        write_svg(SUBDIR, "thunder-shockwave-rumble-and-refraction.svg", _build_thunder_shockwave_and_refraction())


_register_weather_thunderstorm()


# ---------------------------------------------------------------------------
# Why the Sun and Moon Appear to Follow a Moving Car:
# Motion Parallax, Window Reference Frame, Induced Motion & Cosmic Parallax
# ---------------------------------------------------------------------------
def _register_moon_following_car():
    SUBDIR = "moon-following-car"
    RED = "#b91c1c"
    RED_SOFT = "#fef2f2"
    TEAL = "#0f766e"
    TEAL_SOFT = "#f0fdfa"
    AMBER = "#b45309"
    AMBER_SOFT = "#fffbeb"
    GOLD = "#eab308"

    # 1. Exact transverse baseline and astronomical distances (NASA Fact Sheets & IAU 2015 B3)
    L_CAR_M = 100.0          # 100 km/h (27.778 m/s) * 3.6 s = 100 m
    L_HWY_M = 10_000.0       # 10 km straight highway run (6 min at 100 km/h)
    D_MOON_M = 3.844e8       # 384,400 km mean Earth-Moon distance
    D_SUN_M = 1.495978707e11 # 1 AU exact (IAU 2015 Resolution B2/B3)
    EYE_MAR_ARCSEC = 60.0    # 1 arcminute = 60" (20/20 = 6/6 = 5.0 visual acuity MAR)
    R_EQ_KM = 6378.137       # WGS-84 equatorial radius
    V_SOLAR_EQ = 2.0 * math.pi * R_EQ_KM / 24.0  # 1669.79 km/h solar-day equatorial speed

    def parallax_rad(baseline_m: float, dist_m: float) -> float:
        return 2.0 * math.atan(baseline_m / (2.0 * dist_m))

    def parallax_deg(baseline_m: float, dist_m: float) -> float:
        return math.degrees(parallax_rad(baseline_m, dist_m))

    def parallax_arcsec(baseline_m: float, dist_m: float) -> float:
        return parallax_deg(baseline_m, dist_m) * 3600.0

    # Verify exact physical benchmarks
    DEG_RAIL = parallax_deg(L_CAR_M, 2.5)
    DEG_TREE = parallax_deg(L_CAR_M, 20.0)
    DEG_BLDG = parallax_deg(L_CAR_M, 200.0)
    DEG_MTN = parallax_deg(L_CAR_M, 5_000.0)
    DEG_CLD = parallax_deg(L_CAR_M, 10_000.0)
    SEC_MOON_100M = parallax_arcsec(L_CAR_M, D_MOON_M)
    SEC_MOON_10KM = parallax_arcsec(L_HWY_M, D_MOON_M)
    SEC_SUN_100M = parallax_arcsec(L_CAR_M, D_SUN_M)

    assert 174.2 < DEG_RAIL < 174.4
    assert 136.3 < DEG_TREE < 136.5
    assert 28.0 < DEG_BLDG < 28.2
    assert 1.14 < DEG_MTN < 1.16
    assert 0.57 < DEG_CLD < 0.58
    assert 0.053 < SEC_MOON_100M < 0.055
    assert 5.35 < SEC_MOON_10KM < 5.39
    assert 1.35e-4 < SEC_SUN_100M < 1.40e-4
    assert 1669.5 < V_SOLAR_EQ < 1670.1

    # -----------------------------------------------------------------------
    # Figure 1: One-Shot Animated Top-Down Geometry + Car Window Speed Hierarchy
    # -----------------------------------------------------------------------
    def _build_window_parallax_hierarchy():
        els = header(
            "一、车窗外的速度阶梯：近树狂退、远山慢移、月亮“钉”在原处",
            "汽车 100 km/h 直行 3.6 秒前进 100 米（单次动画按真实时间放慢 2 倍为 7.2 秒，停在终态）",
        )

        # Panel A: Top-Down Optical Ray Geometry (Compressed Depth Schematic)
        els.append(card(20, 64, 720, 228))
        els.append(pill(34, 74, "A · 俯视几何光路（纵深压缩示意）：近处视线大角度偏转 vs 38.4 万公里平行月光", fg=BLUE, bg=BLUE_SOFT, w=548))
        els.append(txt(726, 90, "注：纵深非等比", 11.5, MUTED, anchor="end"))

        # Road & Car A -> Car B along y = 258
        ax_car, bx_car, ry_car = 246.0, 506.0, 258.0
        els.append('<rect x="196" y="244" width="360" height="28" rx="5" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>')
        els.append('<line x1="204" y1="258" x2="548" y2="258" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="8 6"/>')

        # Parallel golden moonbeams straight down from top celestial strip to A and B
        els.append('<rect x="206" y="106" width="340" height="24" rx="12" fill="#fefce8" stroke="#fde047" stroke-width="1"/>')
        els.append(f'<circle cx="376" cy="118" r="8.5" fill="{GOLD}" stroke="{AMBER}" stroke-width="1"/>')
        els.append(txt(392, 122, "月球 (38.4万km)", 11.5, AMBER, weight="700"))
        for cx_ray in (ax_car, bx_car):
            els.append(f'<line x1="{cx_ray:.1f}" y1="130" x2="{cx_ray:.1f}" y2="242" stroke="{AMBER}" stroke-width="1.8" stroke-dasharray="5 3"/>')

        # Distant mountain at (376, 158)
        els.append('<polygon points="358,170 376,148 394,170" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>')
        els.append(f'<line x1="{ax_car:.1f}" y1="246" x2="376" y2="166" stroke="{TEAL}" stroke-width="1.3" stroke-dasharray="3 3"/>')
        els.append(f'<line x1="{bx_car:.1f}" y1="246" x2="376" y2="166" stroke="{TEAL}" stroke-width="1.3" stroke-dasharray="3 3"/>')

        # Roadside tree at (376, 206)
        els.append(f'<line x1="{ax_car:.1f}" y1="246" x2="376" y2="208" stroke="{GREEN}" stroke-width="2.0"/>')
        els.append(f'<line x1="{bx_car:.1f}" y1="246" x2="376" y2="208" stroke="{GREEN}" stroke-width="2.0"/>')
        els.append('<circle cx="376" cy="204" r="9" fill="#dcfce7" stroke="#15803d" stroke-width="1.5"/>')
        els.append(txt(376, 208, "树", 11, GREEN, anchor="middle", weight="700"))

        # Ghost initial car A (t = 0 s)
        els.append(f'<rect x="{ax_car - 18:.1f}" y="{ry_car - 9:.1f}" width="36" height="18" rx="5" fill="#ffffff" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="3 2"/>')
        els.append(txt(ax_car, ry_car + 4, "A(0s)", 10.5, BLUE, anchor="middle", weight="700"))

        # Animated car moving A -> B, ending cleanly at B (t = 3.6 s)
        els.append(
            f'<g class="mfc-car-top">'
            f'<rect x="{bx_car - 20:.1f}" y="{ry_car - 9.5:.1f}" width="40" height="19" rx="5" fill="{BLUE}" stroke="#0f172a" stroke-width="1.2"/>'
            f'<text x="{bx_car:.1f}" y="{ry_car + 4:.1f}" font-size="10.5" fill="#ffffff" text-anchor="middle" font-weight="700">B(3.6s)</text>'
            f'</g>'
        )
        els.append(f'<line x1="{ax_car:.1f}" y1="281" x2="314" y2="281" stroke="{BLUE}" stroke-width="1.5"/>')
        els.append(f'<line x1="438" y1="281" x2="{bx_car:.1f}" y2="281" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#arr-blue)"/>')
        els.append(txt(376, 285, "直行基线 L = 100 m", 11.5, INK, anchor="middle", weight="700"))

        # Clean left & right callout cards completely outside sightline fan
        els.append(card(34, 114, 152, 156, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1))
        els.append(txt(44, 136, "近树 (D = 20 m)", 12, GREEN, weight="700"))
        els.append(txt(44, 157, "A 处：右前方 +68.2°", 11.5, BODY))
        els.append(txt(44, 177, "B 处：右后方 −68.2°", 11.5, BODY))
        els.append(txt(44, 199, f"总转角 Δθ = {DEG_TREE:.1f}°", 12, GREEN, weight="700"))
        els.append(txt(44, 221, "视线猛烈向后甩，", 11.5, BODY))
        els.append(txt(44, 240, "树影瞬间飞掠车窗！", 11.5, INK, weight="700"))

        els.append(card(564, 114, 162, 156, rx=8, fill=AMBER_SOFT, stroke=AMBER, sw=1))
        els.append(txt(574, 136, "月球 (38.4万km)", 12, AMBER, weight="700"))
        els.append(txt(574, 157, "两条月光夹角仅：", 11.5, BODY))
        els.append(txt(574, 178, f"Δθ = {SEC_MOON_100M:.3f}″ (角秒)", 12, RED, weight="700"))
        els.append(txt(574, 200, "≈ 0.000015° ≈ 平行光", 11.5, BODY))
        els.append(txt(574, 222, "远山 (5km)：偏 1.15°", 11.5, TEAL, weight="700"))
        els.append(txt(574, 242, "月亮方向几乎零变化！", 11.5, INK, weight="700"))

        # Panel B: Passenger Right Side Window (110 deg horizontal FOV) + Quantitative Table
        els.append(card(20, 304, 720, 236))
        els.append(pill(34, 314, "B · 乘客右侧车窗视野（横向约 110°）：按真实角位移比例映射 3.6 秒横移", fg=ORANGE, bg=ORANGE_SOFT, w=516))

        win_x, win_y, win_w, win_h = 34.0, 346.0, 444.0, 178.0
        px_per_deg = win_w / 110.0  # 4.036 px per degree
        dx_mtn = DEG_MTN * px_per_deg   # 4.6 px
        dx_bldg = DEG_BLDG * px_per_deg # 113.3 px

        # Dusk sky frame
        els.append(f'<rect x="{win_x:.1f}" y="{win_y:.1f}" width="{win_w:.1f}" height="{win_h:.1f}" rx="10" fill="#1e293b" stroke="#334155" stroke-width="3"/>')
        els.append(f'<g clip-path="url(#mfc-win-clip)">')
        # Horizon strip inside window
        els.append(f'<rect x="{win_x:.1f}" y="{win_y + 138:.1f}" width="{win_w:.1f}" height="40" fill="#0f172a"/>')

        # 1. Moon pinned rock-solid at (390, 384) (0.054" -> 0.00006 px!)
        els.append('<circle cx="390" cy="384" r="19" fill="#fef08a" fill-opacity="0.18"/>')
        els.append(f'<circle cx="390" cy="384" r="12.5" fill="#fde047" stroke="#facc15" stroke-width="1.2"/>')
        els.append('<text x="366" y="380" font-size="11.5" fill="#fef08a" text-anchor="end" font-weight="700">月亮：位移 0.054″</text>')
        els.append('<text x="366" y="397" font-size="11.5" fill="#fde68a" text-anchor="end">(钉在窗上不动！)</text>')

        # 2. Distant mountain ridge (shifts only -4.6 px)
        els.append('<polygon points="74,484 128,448 184,484" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="3 2"/>')
        els.append(
            f'<g class="mfc-mtn">'
            f'<polygon points="{74 - dx_mtn:.1f},484 {128 - dx_mtn:.1f},448 {184 - dx_mtn:.1f},484" fill="#475569" stroke="#94a3b8" stroke-width="1.2"/>'
            f'</g>'
        )
        els.append('<text x="126" y="440" font-size="11.5" fill="#cbd5e1" text-anchor="middle">远山：仅退 1.15°</text>')

        # 3. Building at D = 200 m (shifts -113.3 px from x=344 to x=230.7)
        bx0 = 344.0
        bx1 = bx0 - dx_bldg
        els.append(f'<rect x="{bx0:.1f}" y="432" width="32" height="52" rx="2" fill="none" stroke="#93c5fd" stroke-width="1.2" stroke-dasharray="3 2"/>')
        els.append(f'<text x="{bx0 + 16:.1f}" y="425" font-size="10.5" fill="#93c5fd" text-anchor="middle">0s</text>')
        els.append(
            f'<g class="mfc-bldg">'
            f'<rect x="{bx1:.1f}" y="432" width="32" height="52" rx="2" fill="#3b82f6" stroke="#bfdbfe" stroke-width="1.2"/>'
            f'</g>'
        )
        els.append(f'<line x1="{bx0 - 3:.1f}" y1="458" x2="{bx1 + 36:.1f}" y2="458" stroke="#93c5fd" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arr-blue)"/>')
        els.append(f'<text x="{0.5 * (bx0 + bx1) + 16:.1f}" y="451" font-size="11.5" fill="#bae6fd" text-anchor="middle" font-weight="700">楼房退 28.1°</text>')

        # 4. Roadside tree (D = 20 m, sweeps 136.4 deg across entire window!)
        els.append('<circle cx="446" cy="466" r="13" fill="none" stroke="#86efac" stroke-width="1.2" stroke-dasharray="3 2"/>')
        els.append(
            '<g class="mfc-tree">'
            '<rect x="64" y="474" width="6" height="16" fill="#92400e"/>'
            '<circle cx="67" cy="464" r="14" fill="#16a34a" stroke="#bbf7d0" stroke-width="1.2"/>'
            '</g>'
        )
        els.append('<line x1="428" y1="504" x2="90" y2="504" stroke="#86efac" stroke-width="1.6" stroke-dasharray="5 3"/>')
        els.append('<polygon points="84,504 93,499.5 93,508.5" fill="#86efac"/>')
        els.append('<text x="258" y="518" font-size="11.5" fill="#bbf7d0" text-anchor="middle" font-weight="700">近树 (20m) 飞掠 136.4° · 护栏 (2.5m) 闪掠 174.3°</text>')
        els.append('</g>')

        # Right side summary table card
        els.append(card(490, 346, 236, 178, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(502, 367, "目标 (距离 D)", 11.5, MUTED, weight="700"))
        els.append(txt(714, 367, "100m 视角差", 11.5, MUTED, anchor="end", weight="700"))
        els.append(f'<line x1="500" y1="375" x2="716" y2="375" stroke="{HAIRLINE}" stroke-width="1"/>')

        rows = [
            ("护栏 (2.5 m)", f"{DEG_RAIL:.1f}° 闪掠", SLATE),
            ("近树 (20 m)", f"{DEG_TREE:.1f}° 飞退", GREEN),
            ("高楼 (200 m)", f"{DEG_BLDG:.1f}° 后移", BLUE),
            ("远山 (5 km)", f"{DEG_MTN:.2f}° 慢滑", TEAL),
            ("月球 (38.4万km)", f"{SEC_MOON_100M:.3f}″ 钉住!", RED),
        ]
        for idx, (lbl, val, col) in enumerate(rows):
            ry = 396 + idx * 25
            els.append(txt(502, ry, lbl, 11.5, BODY, weight="600" if idx == 4 else None))
            els.append(txt(714, ry, val, 11.5, col, anchor="end", weight="700"))

        extra_defs = (
            f'<clipPath id="mfc-win-clip">'
            f'<rect x="{win_x + 2:.1f}" y="{win_y + 2:.1f}" width="{win_w - 4:.1f}" height="{win_h - 4:.1f}" rx="8"/>'
            f'</clipPath>'
        )
        extra_css = f"""
  @keyframes mfcCarTop {{
    0% {{ transform: translateX(-260px); }}
    100% {{ transform: translateX(0px); }}
  }}
  @keyframes mfcMtnSlide {{
    0% {{ transform: translateX({dx_mtn:.1f}px); }}
    100% {{ transform: translateX(0px); }}
  }}
  @keyframes mfcBldgSlide {{
    0% {{ transform: translateX({dx_bldg:.1f}px); }}
    100% {{ transform: translateX(0px); }}
  }}
  @keyframes mfcTreeSweep {{
    0% {{ transform: translateX(380px); }}
    100% {{ transform: translateX(0px); }}
  }}
  .mfc-car-top {{ animation: mfcCarTop 7.2s linear 1 forwards; }}
  .mfc-mtn {{ animation: mfcMtnSlide 7.2s linear 1 forwards; }}
  .mfc-bldg {{ animation: mfcBldgSlide 7.2s linear 1 forwards; }}
  .mfc-tree {{ animation: mfcTreeSweep 7.2s cubic-bezier(0.22, 0.68, 0.35, 0.96) 1 forwards; }}
  @media (prefers-reduced-motion: reduce) {{
    .mfc-car-top, .mfc-mtn, .mfc-bldg, .mfc-tree {{
      animation: none !important;
      transform: none !important;
    }}
  }}"""

        return figure(
            554,
            "汽车直行100米时的俯视几何视差光路与右侧车窗五层景物角位移阶梯单次动画图解",
            "上图对比20米近树视线偏转136.4度与38.4万公里月球视线仅偏0.054角秒的平行光几何；下图按真实角位移比例展示车窗视野内护栏、近树、高楼、远山与月亮的后退幅度，支持减少动态效果。",
            els,
            extra_css=extra_css,
            extra_defs=extra_defs,
        )

    # -----------------------------------------------------------------------
    # Figure 2: Log-Log Angular Shift vs 60" Eye Resolution + Straight vs Turn
    # -----------------------------------------------------------------------
    def _build_log_scale_and_turn():
        els = header(
            "二、差了 1100 倍的视觉门槛：双对数视差曲线与“直行 vs 转弯”判决",
            "左图实算 8 类距离目标的 Δθ 并对照人眼 60″ 分辨极限；右图解释为什么一拐弯月亮就换车窗",
        )

        # Panel A: Log-Log Chart of Angular Shift vs Distance D
        els.append(card(20, 64, 442, 452))
        els.append(pill(34, 74, "A · 双对数实算：开 100 m 与开 10 km 的视角变化 Δθ", fg=BLUE, bg=BLUE_SOFT, w=388))

        gx0, gx1 = 84.0, 442.0
        gy0, gy1 = 426.0, 118.0  # y from 10^-5" (426) to 10^6.5" (118)

        def px_logd(logd: float) -> float:
            return gx0 + (logd / 12.0) * (gx1 - gx0)

        def py_logsec(logsec: float) -> float:
            return gy0 - ((logsec + 5.0) / 11.5) * (gy0 - gy1)

        y_eye = py_logsec(math.log10(EYE_MAR_ARCSEC))  # 60" -> log10 = 1.7782

        # Shaded visible vs blind regions
        els.append(f'<rect x="{gx0:.1f}" y="{gy1:.1f}" width="{gx1 - gx0:.1f}" height="{y_eye - gy1:.1f}" fill="#ecfdf5"/>')
        els.append(f'<rect x="{gx0:.1f}" y="{y_eye:.1f}" width="{gx1 - gx0:.1f}" height="{gy0 - y_eye:.1f}" fill="#fff1f2"/>')
        els.append(f'<rect x="{gx0:.1f}" y="{gy1:.1f}" width="{gx1 - gx0:.1f}" height="{gy0 - gy1:.1f}" fill="none" stroke="{BORDER}" stroke-width="1"/>')

        # Gridlines and ticks
        for exp_d, lbl_d in [(0, "1m"), (3, "1km"), (6, "10³km"), (9, "10⁶km"), (12, "10⁹km")]:
            xx = px_logd(exp_d)
            els.append(f'<line x1="{xx:.1f}" y1="{gy1:.1f}" x2="{xx:.1f}" y2="{gy0:.1f}" stroke="{HAIRLINE}" stroke-width="0.8" stroke-dasharray="2 3"/>')
            els.append(txt(xx, gy0 + 16, lbl_d, 10.5, MUTED, anchor="middle"))
        els.append(txt(0.5 * (gx0 + gx1), gy0 + 34, "物体垂直距离 D（对数坐标）", 11.5, INK, anchor="middle", weight="600"))

        for exp_s, lbl_s in [(-4, "10⁻⁴″"), (-2, "0.01″"), (0, "1″"), (2, "100″"), (4, "2.8°"), (6, "278°")]:
            yy = py_logsec(exp_s)
            els.append(f'<line x1="{gx0:.1f}" y1="{yy:.1f}" x2="{gx1:.1f}" y2="{yy:.1f}" stroke="{HAIRLINE}" stroke-width="0.8" stroke-dasharray="2 3"/>')
            els.append(txt(gx0 - 6, yy + 4, lbl_s, 10.5, MUTED, anchor="end"))

        # Human eye 1 arcmin = 60" threshold line
        els.append(f'<line x1="{gx0:.1f}" y1="{y_eye:.1f}" x2="{gx1:.1f}" y2="{y_eye:.1f}" stroke="{RED}" stroke-width="1.8" stroke-dasharray="6 3"/>')
        els.append(txt(gx1 - 6, y_eye - 7, "人眼分辨极限 1′ = 60″ (视力 1.0)", 11, RED, anchor="end", weight="700", halo=True))
        els.append(txt(gx0 + 8, gy0 - 10, "↓ 视网膜盲区：移动不足 1 像素，肉眼看作静止", 11, RED, weight="600", halo=True))

        # Exact curves: L = 10 km (dashed teal) and L = 100 m (solid blue)
        pts_100m, pts_10km = [], []
        for i in range(121):
            ld = i * 0.1
            dm = 10.0 ** ld
            s100 = parallax_arcsec(L_CAR_M, dm)
            s10k = parallax_arcsec(L_HWY_M, dm)
            pts_100m.append(f"{px_logd(ld):.1f},{py_logsec(math.log10(s100)):.1f}")
            pts_10km.append(f"{px_logd(ld):.1f},{py_logsec(math.log10(s10k)):.1f}")
        els.append(f'<polyline points="{" ".join(pts_10km)}" fill="none" stroke="{TEAL}" stroke-width="1.8" stroke-dasharray="5 3"/>')
        els.append(f'<polyline points="{" ".join(pts_100m)}" fill="none" stroke="{BLUE}" stroke-width="2.3"/>')
        els.append(txt(342, 142, "虚线: 狂开10km", 11, TEAL, weight="700", halo=True))
        els.append(txt(342, 160, "实线: 直行100m", 11, BLUE, weight="700", halo=True))

        # Staggered non-overlapping benchmark markers
        pts_meta = [
            (2.5, "护栏 174°", BLUE, -6, 30, "start"),
            (20.0, "近树 136°", GREEN, 8, -5, "start"),
            (200.0, "高楼 28.1°", BLUE, 9, 4, "start"),
            (5_000.0, "远山 1.15°", TEAL, 8, -2, "start"),
            (10_000.0, "高云 0.57°", SLATE, -8, 13, "end"),
            (D_MOON_M, "月球(100m) 0.054″", RED, -9, 14, "end"),
            (D_SUN_M, "太阳 0.00014″", ORANGE, -8, -8, "end"),
        ]
        x_rail = px_logd(math.log10(2.5))
        y_rail = py_logsec(math.log10(parallax_arcsec(L_CAR_M, 2.5)))
        els.append(f'<line x1="{x_rail:.1f}" y1="{y_rail + 5:.1f}" x2="{x_rail:.1f}" y2="{y_rail + 18:.1f}" stroke="{BLUE}" stroke-width="1.1"/>')
        for dm, lbl, col, dx_t, dy_t, anc in pts_meta:
            ld = math.log10(dm)
            ls = math.log10(parallax_arcsec(L_CAR_M, dm))
            cx, cy = px_logd(ld), py_logsec(ls)
            els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.0" fill="{col}" stroke="#ffffff" stroke-width="1"/>')
            els.append(txt(cx + dx_t, cy + dy_t, lbl, 11, col, anchor=anc, weight="700", halo=True))

        # Moon 10 km point + 1118x gap callout
        xm = px_logd(math.log10(D_MOON_M))
        ym_10k = py_logsec(math.log10(SEC_MOON_10KM))
        ym_100 = py_logsec(math.log10(SEC_MOON_100M))
        els.append(f'<circle cx="{xm:.1f}" cy="{ym_10k:.1f}" r="4.0" fill="{TEAL}" stroke="#ffffff" stroke-width="1"/>')
        els.append(txt(xm - 9, ym_10k + 4, "月球(10km) 5.37″", 11, TEAL, anchor="end", weight="700", halo=True))
        els.append(f'<line x1="{xm + 8:.1f}" y1="{y_eye + 2:.1f}" x2="{xm + 8:.1f}" y2="{ym_100 - 2:.1f}" stroke="{RED}" stroke-width="1.5"/>')
        els.append(txt(xm + 14, 0.5 * (y_eye + ym_100) + 4, "差1118倍!", 11, RED, weight="700", halo=True))

        els.append(txt(34, 486, "• 哪怕在笔直高速连开 10 km，月球视差 5.37″ 仍不足人眼极限的 1/11；", 11.5, BODY))
        els.append(txt(34, 505, "• 想靠纯平移让月亮退后 1°（两个满月宽），需一口气直开 6,709 km！", 11.5, INK, weight="700"))

        # Panel B: Straight Translation vs 90-deg Intersection Turn
        els.append(card(474, 64, 266, 452))
        els.append(pill(488, 74, "B · 直行平移 vs 路口 90° 转弯", fg=PURPLE, bg=PURPLE_SOFT, w=238))

        # Subcard 1: Straight translation
        els.append(card(488, 108, 238, 186, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(500, 129, "① 直行平移：车头朝向角 ψ 不变", 12, BLUE, weight="700"))
        els.append('<line x1="510" y1="202" x2="704" y2="202" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>')
        els.append(f'<rect x="528" y="193" width="34" height="18" rx="4" fill="#ffffff" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="3 2"/>')
        els.append(f'<rect x="642" y="193" width="34" height="18" rx="4" fill="{BLUE}"/>')
        els.append(f'<circle cx="607" cy="148" r="8" fill="{GOLD}" stroke="{AMBER}" stroke-width="1"/>')
        els.append(f'<line x1="545" y1="193" x2="545" y2="152" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="659" y1="193" x2="659" y2="152" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="4 3"/>')
        els.append(txt(607, 234, "窗内方位 φ_窗 = θ_月 − ψ", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(607, 255, "ψ = 0° 不变，θ_月 仅变 0.054″", 11.5, BODY, anchor="middle"))
        els.append(txt(607, 276, "→ 月亮死死钉在同一扇侧窗！", 11.5, GREEN, anchor="middle", weight="700"))

        # Subcard 2: 90-degree intersection turn
        els.append(card(488, 308, 238, 194, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.1))
        els.append(txt(500, 329, "② 路口右转：车窗整体转 Δψ = 90°", 12, ORANGE, weight="700"))
        # L-shaped road corner
        els.append('<path d="M542,418 L542,374 Q542,360 556,360 L632,360" fill="none" stroke="#94a3b8" stroke-width="10" stroke-linecap="round"/>')
        els.append(f'<rect x="533" y="394" width="18" height="30" rx="4" fill="#ffffff" stroke="{BLUE}" stroke-width="1.4"/>')
        els.append(f'<rect x="594" y="351" width="30" height="18" rx="4" fill="{ORANGE}"/>')
        els.append(f'<circle cx="542" cy="342" r="7.5" fill="{GOLD}" stroke="{AMBER}" stroke-width="1"/>')
        els.append(txt(644, 365, "北↑月亮", 11.5, AMBER, weight="700"))
        els.append(txt(644, 386, "转弯前: 前挡风", 11, BODY))
        els.append(txt(644, 405, "右转后: 左车窗!", 11, RED, weight="700"))
        els.append(txt(607, 444, "转动效应 Δφ_窗 = −Δψ 与距离无关！", 11.5, INK, anchor="middle", weight="700"))
        els.append(txt(607, 465, "不管天体在 38 万公里还是无穷远，", 11.5, BODY, anchor="middle"))
        els.append(txt(607, 486, "车头转 90°，月亮立刻横扫 90° 换窗！", 11.5, RED, anchor="middle", weight="700"))

        return figure(
            532,
            "双对数坐标下8类物体运动视差角与人眼60角秒分辨极限对比及直行与90度转弯差异图解",
            "左图按精确三角公式绘制行驶100米与10公里的视差角双对数曲线，标出月球0.054角秒比人眼60角秒极限小1118倍；右图对比直行平移与路口90度转弯时车窗方位角的变化。",
            els,
        )

    # -----------------------------------------------------------------------
    # Figure 3: Window Frame Anchoring + Duncker Induced Motion + Flow Parsing
    # -----------------------------------------------------------------------
    def _build_induced_motion_and_frame():
        els = header(
            "三、“不往后退”为什么变成“追着车跑”？——参考系锚定与诱导运动错觉",
            "几何学只让月亮停在原角度；真正给月亮加上“+100 km/h 同行感”的，是大脑的三重视觉加工",
        )

        # Panel A: Galilean Reference Frame Switch (Ground vs Car Window)
        els.append(card(20, 64, 354, 294))
        els.append(pill(34, 74, "A · 第一重：车窗画框锚定（伴行车效应）", fg=BLUE, bg=BLUE_SOFT, w=326))

        # Ground frame box
        els.append(card(34, 108, 326, 98, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 128, "① 地面参考系（站在路边看真相）", 12, SLATE, weight="700"))
        els.append(txt(46, 151, "• 汽车与你：", 11.5, BODY))
        els.append(f'<line x1="132" y1="147" x2="232" y2="147" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>')
        els.append(txt(240, 151, "+100 km/h", 11.5, BLUE, weight="700"))
        els.append(txt(46, 173, "• 行道树：v = 0（扎根路边不动）", 11.5, BODY))
        els.append(txt(46, 194, "• 月　亮：视线方向近似恒定不变", 11.5, BODY))

        # Car-cabin frame box
        els.append(card(34, 218, 326, 126, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.1))
        els.append(txt(46, 239, "② 车厢参考系（大脑默认座椅与窗框静止！）", 12, BLUE, weight="700"))
        els.append(txt(46, 263, "• 窗框准星：v′ = 0（你和玻璃相对静止）", 11.5, BODY))
        els.append(txt(46, 285, "• 行道树：", 11.5, BODY))
        els.append(f'<line x1="212" y1="281" x2="122" y2="281" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>')
        els.append(txt(220, 285, "−100 km/h 狂退", 11.5, ORANGE, weight="700"))
        els.append(txt(46, 308, "• 月亮一直贴在窗框同一点 ＝ 隔壁车道", 11.5, BODY))
        els.append(txt(46, 329, "  同速飙车的伴行车 → 大脑判为 +100 km/h 同行！", 11.5, INK, weight="700"))

        # Panel B: Duncker (1929) Induced Motion + Cortical MT/MST Flow Parsing (2009)
        els.append(card(386, 64, 354, 294))
        els.append(pill(400, 74, "B · 第二、三重：诱导运动与光流拆解错配", fg=ORANGE, bg=ORANGE_SOFT, w=326))

        # Visual scene: moon behind backward-rushing tree branches
        els.append('<rect x="400" y="108" width="326" height="106" rx="8" fill="#1e293b"/>')
        els.append(f'<circle cx="576" cy="148" r="15" fill="#fde047"/>')
        # Foreground tree silhouettes sweeping left across moon
        for tx_c in (454, 536, 636):
            els.append(f'<polygon points="{tx_c - 22},214 {tx_c},152 {tx_c + 22},214" fill="#0f172a" stroke="#475569" stroke-width="1"/>')
        els.append('<line x1="696" y1="196" x2="432" y2="196" stroke="#93c5fd" stroke-width="1.8" stroke-dasharray="5 3"/>')
        els.append('<polygon points="424,196 434,191.5 434,200.5" fill="#93c5fd"/>')
        els.append('<text x="563" y="209" font-size="11" fill="#bae6fd" text-anchor="middle">前景树梢/电线杆向后形成强烈光流 (−ω)</text>')
        els.append('<line x1="596" y1="142" x2="664" y2="142" stroke="#fde047" stroke-width="2.2"/>')
        els.append('<polygon points="672,142 662,137.5 662,146.5" fill="#fde047"/>')
        els.append('<text x="634" y="131" font-size="11" fill="#fef08a" text-anchor="middle" font-weight="700">诱导出前冲感 (+ω)!</text>')

        # Explanation card below dark scene
        els.append(card(400, 224, 326, 120, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1))
        els.append(txt(412, 244, "• 邓克尔诱导运动 (1929)：大面积树影后掠，", 11.5, BODY))
        els.append(txt(412, 263, "  反向诱导出静止月亮“穿林前冲”（同月穿浮云）；", 11.5, BODY))
        els.append(txt(412, 285, "• 遮挡 + 光流拆解 (Warren & Rushton 2009)：", 11.5, INK, weight="700"))
        els.append(txt(412, 305, "  树挡住月亮→大脑低估距离，预期它也该后退；", 11.5, BODY))
        els.append(txt(412, 325, "  实测后退为 0 − 预期后退 (−ω) ＝ 主动前冲 (+ω)！", 11.5, RED, weight="700"))

        # Panel C: 3 Hands-on Kid/Passenger Experiments
        els.append(card(20, 370, 720, 156))
        els.append(pill(34, 380, "C · 坐车时 30 秒就能亲手验证的 3 个“破除错觉”小实验（乘客专享，司机专心看路！）", fg=GREEN, bg=GREEN_SOFT, w=586))

        exps = [
            (
                34,
                "① 玻璃便签准星实验",
                "头靠稳头枕，在侧窗边缘贴小纸角",
                "对准月亮。直行 1 km 月亮始终钉",
                "在纸尖——根本没有“忽快忽慢”！",
                BLUE,
                BLUE_SOFT,
            ),
            (
                268,
                "② 手掌遮挡前景实验",
                "用手掌挡住窗外下半截飞退的树梢",
                "和房屋，只留上方干净夜空：月亮",
                "“往前猛跑”的冲刺感立刻消失大半！",
                ORANGE,
                ORANGE_SOFT,
            ),
            (
                502,
                "③ 左右眼交替眨眼 (6.5cm)",
                "伸直手臂竖起大拇指遮住月亮，左",
                "右眼轮流睁闭：拇指跳开约 6°（12",
                "个满月宽），月亮在背景里纹丝不动！",
                GREEN,
                GREEN_SOFT,
            ),
        ]
        for ex_x, t_head, l1, l2, l3, fg_c, bg_c in exps:
            els.append(card(ex_x, 412, 224, 102, rx=8, fill=bg_c, stroke=fg_c, sw=1))
            els.append(txt(ex_x + 12, 433, t_head, 12, fg_c, weight="700"))
            els.append(txt(ex_x + 12, 455, l1, 11.5, BODY))
            els.append(txt(ex_x + 12, 475, l2, 11.5, BODY))
            els.append(txt(ex_x + 12, 495, l3, 11.5, INK, weight="600"))

        return figure(
            542,
            "车窗画框参考系速度变换、邓克尔诱导运动与大脑光流拆解错觉及3个乘车验证实验图解",
            "左图对比地面参考系与车厢参考系的速度变换；右图解释1929年邓克尔诱导运动与2009年大脑光流拆解机制如何把零角速度感知为主动前冲；底部给出玻璃准星、遮挡前景与双眼视差三个乘客小实验。",
            els,
        )

    # -----------------------------------------------------------------------
    # Figure 4: Earth Rotation Speed vs Latitude & 1973 Concorde 74-Min Eclipse
    # -----------------------------------------------------------------------
    def _build_curvature_and_concorde():
        els = header(
            "四、什么时候不再“死跟着走”？——地球自转、大地曲率与超音速追日",
            "把时间拉长到几小时、里程拉长到几百公里，或坐上 2 马赫协和号向西狂追，日月就会明显移位",
        )

        # Panel A: Westbound Speed Required to Beat Earth's Solar-Day Rotation
        els.append(card(20, 64, 374, 454))
        els.append(pill(34, 74, "A · 向西飞多快能追回落日？(v = 1670·cos φ)", fg=BLUE, bg=BLUE_SOFT, w=346))

        px0, px1 = 76.0, 376.0   # 0 .. 2300 km/h
        py0, py1 = 420.0, 122.0  # 0 .. 90 deg N

        def x_spd(v_kmh: float) -> float:
            return px0 + (v_kmh / 2300.0) * (px1 - px0)

        def y_lat(deg_lat: float) -> float:
            return py0 - (deg_lat / 90.0) * (py0 - py1)

        # Polygon fill to right of curve (sun rises in the west!)
        rot_pts = [f"{x_spd(V_SOLAR_EQ * math.cos(math.radians(lat))):.1f},{y_lat(lat):.1f}" for lat in range(0, 91, 2)]
        poly_right = " ".join(rot_pts + [f"{px1:.1f},{py1:.1f}", f"{px1:.1f},{py0:.1f}"])
        els.append(f'<rect x="{px0:.1f}" y="{py1:.1f}" width="{px1 - px0:.1f}" height="{py0 - py1:.1f}" fill="#f8fafc" stroke="{BORDER}" stroke-width="1"/>')
        els.append(f'<polygon points="{poly_right}" fill="#fef9c3" fill-opacity="0.65"/>')

        # Gridlines
        for lat_tick in (0, 30, 50, 60, 90):
            yy = y_lat(lat_tick)
            els.append(f'<line x1="{px0:.1f}" y1="{yy:.1f}" x2="{px1:.1f}" y2="{yy:.1f}" stroke="{HAIRLINE}" stroke-width="0.8" stroke-dasharray="2 3"/>')
            els.append(txt(px0 - 6, yy + 4, f"{lat_tick}°N", 10.5, MUTED, anchor="end"))
        for v_tick in (0, 500, 1000, 1500, 2000):
            xx = x_spd(v_tick)
            els.append(f'<line x1="{xx:.1f}" y1="{py1:.1f}" x2="{xx:.1f}" y2="{py0:.1f}" stroke="{HAIRLINE}" stroke-width="0.8" stroke-dasharray="2 3"/>')
            els.append(txt(xx, py0 + 16, str(v_tick), 10.5, MUTED, anchor="middle"))
        els.append(txt(0.5 * (px0 + px1), py0 + 34, "向西地面航速 v（km/h）", 11.5, INK, anchor="middle", weight="600"))

        # Earth rotation threshold curve
        els.append(f'<polyline points="{" ".join(rot_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')

        # Vehicle vertical lines
        for v_veh, lbl_v, col_v, ly_v in [
            (100, "汽车 100", SLATE, 396),
            (350, "高铁 350", GREEN, 366),
            (900, "民航 900", TEAL, 292),
            (2150, "协和 2150", RED, 206),
        ]:
            xv = x_spd(v_veh)
            els.append(f'<line x1="{xv:.1f}" y1="{py1:.1f}" x2="{xv:.1f}" y2="{py0:.1f}" stroke="{col_v}" stroke-width="1.5" stroke-dasharray="4 3"/>')
            anc_v = "end" if v_veh > 1800 else "start"
            dx_lbl = -4 if v_veh > 1800 else 4
            els.append(txt(xv + dx_lbl, ly_v, lbl_v, 10.5, col_v, anchor=anc_v, weight="700", halo=True))

        # Key latitude markers on rotation curve
        v_50n = V_SOLAR_EQ * math.cos(math.radians(50.0))  # 1073 km/h (London/Paris)
        els.append(f'<circle cx="{x_spd(v_50n):.1f}" cy="{y_lat(50):.1f}" r="4" fill="{BLUE}"/>')
        els.append(txt(x_spd(v_50n) + 7, y_lat(50) - 5, f"50°N: {v_50n:.0f} km/h", 10.5, BLUE, weight="700", halo=True))
        els.append(f'<circle cx="{x_spd(V_SOLAR_EQ):.1f}" cy="{y_lat(0):.1f}" r="4" fill="{BLUE}"/>')
        els.append(txt(x_spd(V_SOLAR_EQ) - 6, y_lat(0) - 8, f"赤道 {V_SOLAR_EQ:.0f}", 10.5, BLUE, anchor="end", weight="700", halo=True))
        els.append(txt(368, 152, "反超自转区：", 11, AMBER, anchor="end", weight="700", halo=True))
        els.append(txt(368, 169, "太阳从西边升起！", 11, RED, anchor="end", weight="700", halo=True))

        els.append(txt(34, 478, "• 即使原地停车，地球自转也令太阳 15°/h 西移；", 11.5, BODY))
        els.append(txt(34, 498, "• 60°N 航线民航向西飞 (900>835) 即可定格落日！", 11.5, INK, weight="700"))

        # Panel B: 1973 Concorde 001 Eclipse Chase + North-South Curvature
        els.append(card(406, 64, 334, 454))
        els.append(pill(420, 74, "B · 两个让日月“移位”的硬核现场", fg=ORANGE, bg=ORANGE_SOFT, w=306))

        # Subcard 1: Concorde 001 (June 30, 1973, Nature 246: 72-74)
        els.append(card(420, 108, 306, 202, rx=8, fill="#0f172a", stroke="#334155", sw=1.2))
        els.append('<text x="432" y="130" font-size="12" fill="#fde047" font-weight="700">① 1973.06.30 协和 001 号“夸父追日”</text>')
        # Sun-Moon eclipse icon + shadow cone to Sahara
        els.append('<circle cx="668" cy="154" r="13" fill="#020617" stroke="#fde047" stroke-width="2.2"/>')
        els.append('<polygon points="656,164 680,164 622,232 578,232" fill="#fde047" fill-opacity="0.14"/>')
        # Ground Sahara bar
        els.append('<rect x="432" y="232" width="282" height="12" rx="3" fill="#b45309"/>')
        els.append('<ellipse cx="600" cy="238" rx="24" ry="5" fill="#020617" stroke="#facc15" stroke-width="1"/>')
        # Supersonic Concorde silhouette at altitude 17 km
        els.append('<polygon points="566,196 618,196 602,190 578,190" fill="#f8fafc"/>')
        els.append('<line x1="530" y1="194" x2="562" y2="194" stroke="#38bdf8" stroke-width="1.8"/>')
        els.append('<text x="434" y="156" font-size="11" fill="#e2e8f0">月球本影扫过撒哈拉：</text>')
        els.append('<text x="434" y="175" font-size="11.5" fill="#38bdf8" font-weight="700">影速 ≈ 1,958 km/h (Mach 2.05)</text>')
        els.append('<text x="434" y="218" font-size="11" fill="#cbd5e1">地面站：最多黑 ~7 分钟</text>')
        els.append('<text x="434" y="266" font-size="11.5" fill="#f8fafc">协和 001 号在 17 km 高空同速狂追，</text>')
        els.append('<text x="434" y="287" font-size="11.5" fill="#fde047" font-weight="700">把日全食定在头顶整整 74 分钟！(Nature 1973)</text>')

        # Subcard 2: Earth Curvature (111.2 km per degree of latitude)
        els.append(card(420, 322, 306, 182, rx=8, fill=TEAL_SOFT, stroke=TEAL, sw=1))
        els.append(txt(432, 343, "② 南北长途自驾：大地曲率每 111 km 转 1°", 12, TEAL, weight="700"))
        # Earth arc schematic
        els.append(f'<path d="M446,432 Q536,374 626,432" fill="none" stroke="{TEAL}" stroke-width="2.2"/>')
        # Normal vectors at 40N (left) and 23N (right)
        els.append(f'<line x1="484" y1="412" x2="466" y2="366" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')
        els.append(f'<line x1="588" y1="412" x2="606" y2="366" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')
        els.append(txt(462, 361, "北京天顶", 10.5, BLUE, anchor="middle", weight="700"))
        els.append(txt(612, 361, "广州天顶", 10.5, ORANGE, anchor="middle", weight="700"))
        els.append(txt(676, 392, "转 17°!", 11.5, RED, anchor="middle", weight="700"))
        els.append(txt(432, 456, "• 地球是球体（R ≈ 6,371 km），南北每开 111.2 km，", 11.5, BODY))
        els.append(txt(432, 475, "  脚下地平线就倾转 1°；从北京开到广州 (Δφ=17°)，", 11.5, BODY))
        els.append(txt(432, 494, "  北极星压低 17°，正午太阳在车窗里抬高 17°！", 11.5, INK, weight="700"))

        return figure(
            534,
            "地球不同纬度自转线速度曲线、1973年协和001号74分钟超音速追日全食与南北大地曲率图解",
            "左图按v=1670cosφ计算不同纬度追平太阳周日西移所需向西航速；右上还原1973年6月30日协和001号以2.05马赫追赶月球本影创造74分钟日全食纪录；右下说明南北每开111.2公里地平线倾转1度。",
            els,
        )

    # -----------------------------------------------------------------------
    # Figure 5: Cosmic Baseline — From 6.5 cm Eyes & 100 m Car to 2 AU & Gaia
    # -----------------------------------------------------------------------
    def _build_cosmic_stellar_parallax():
        els = header(
            "五、把“汽车基线”放大 300 万倍：天文学家怎样用视差量穿银河系？",
            "你在车窗里纳闷的运动视差，恰恰是人类测量宇宙恒星真实距离最硬核的几何第一性标尺",
        )

        # Panel A: Earth's 2 AU (300 Million km) Orbital Baseline & Bessel / Gaia
        els.append(card(20, 64, 452, 458))
        els.append(pill(34, 74, "A · 地球这辆“宇宙敞篷车”：半年横跨 3 亿公里拍恒星晃动", fg=BLUE, bg=BLUE_SOFT, w=424))

        # Orbital parallax geometry schematic (y = 108..326)
        els.append(card(34, 108, 424, 214, rx=8, fill="#0f172a", stroke="#334155", sw=1))
        sx, sy, r_orb = 114.0, 215.0, 62.0
        # Orbit circle
        els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r_orb:.1f}" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="11" fill="#fde047" stroke="#f59e0b" stroke-width="1.2"/>')
        els.append(f'<text x="{sx:.1f}" y="{sy + 26:.1f}" font-size="10.5" fill="#fde68a" text-anchor="middle">太阳</text>')

        # Earth in Jan (top) and July (bottom)
        e1y, e2y = sy - r_orb, sy + r_orb
        els.append(f'<circle cx="{sx:.1f}" cy="{e1y:.1f}" r="6.5" fill="#38bdf8" stroke="#ffffff" stroke-width="1"/>')
        els.append(f'<circle cx="{sx:.1f}" cy="{e2y:.1f}" r="6.5" fill="#38bdf8" stroke="#ffffff" stroke-width="1"/>')
        els.append(f'<text x="{sx - 12:.1f}" y="{e1y + 4:.1f}" font-size="10.5" fill="#bae6fd" text-anchor="end" font-weight="700">1月地球</text>')
        els.append(f'<text x="{sx - 12:.1f}" y="{e2y + 4:.1f}" font-size="10.5" fill="#bae6fd" text-anchor="end" font-weight="700">7月地球</text>')

        # 2 AU baseline double line
        els.append(f'<line x1="{sx + 16:.1f}" y1="{e1y + 4:.1f}" x2="{sx + 16:.1f}" y2="{e2y - 4:.1f}" stroke="#38bdf8" stroke-width="1.6"/>')
        els.append(f'<text x="{sx + 22:.1f}" y="{sy - 4:.1f}" font-size="10.5" fill="#38bdf8" font-weight="700">基线 2 AU</text>')
        els.append(f'<text x="{sx + 22:.1f}" y="{sy + 11:.1f}" font-size="10.5" fill="#bae6fd">≈ 3 亿 km</text>')

        # Target nearby star (61 Cygni) at (288, 215) & background star screen at x = 432
        tx_s, ty_s, bx_scr = 288.0, 215.0, 432.0
        y_proj1 = ty_s + (ty_s - e1y) * ((bx_scr - tx_s) / (tx_s - sx))
        y_proj2 = ty_s - (e2y - ty_s) * ((bx_scr - tx_s) / (tx_s - sx))
        els.append(f'<line x1="{sx:.1f}" y1="{e1y:.1f}" x2="{bx_scr:.1f}" y2="{y_proj1:.1f}" stroke="#facc15" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="{sx:.1f}" y1="{e2y:.1f}" x2="{bx_scr:.1f}" y2="{y_proj2:.1f}" stroke="#fb923c" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{tx_s:.1f}" y2="{ty_s:.1f}" stroke="#64748b" stroke-width="1" stroke-dasharray="2 3"/>')

        els.append(f'<circle cx="{tx_s:.1f}" cy="{ty_s:.1f}" r="6.5" fill="#fde047" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(f'<text x="{tx_s:.1f}" y="{ty_s - 14:.1f}" font-size="11" fill="#fef08a" text-anchor="middle" font-weight="700">近距恒星</text>')
        els.append(f'<text x="{tx_s - 36:.1f}" y="{ty_s - 2:.1f}" font-size="10.5" fill="#cbd5e1" text-anchor="end">半张角 ϖ</text>')

        # Distant background stars strip
        els.append(f'<line x1="{bx_scr:.1f}" y1="126" x2="{bx_scr:.1f}" y2="304" stroke="#64748b" stroke-width="1.5"/>')
        els.append(f'<circle cx="{bx_scr:.1f}" cy="{y_proj1:.1f}" r="4" fill="#facc15"/>')
        els.append(f'<circle cx="{bx_scr:.1f}" cy="{y_proj2:.1f}" r="4" fill="#fb923c"/>')
        els.append(f'<text x="{bx_scr - 8:.1f}" y="138" font-size="10.5" fill="#e2e8f0" text-anchor="end">遥远背景星幕</text>')
        els.append(f'<text x="{bx_scr - 8:.1f}" y="{ty_s + 4:.1f}" font-size="11" fill="#fde047" text-anchor="end" font-weight="700">半年摆幅 2ϖ</text>')
        els.append('<text x="44" y="313" font-size="10.5" fill="#94a3b8">注：纵深压缩示意；定义 ϖ = 1″ 时的距离为 1 秒差距 (1 pc ≈ 3.2616 光年)</text>')

        # 3 Historical Milestones card below
        els.append(card(34, 334, 424, 174, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 356, "① 第谷的盲区 (16世纪)：肉眼极限 60″ 找不到恒星晃动，据此怀疑地动说", 11.5, BODY))
        els.append(txt(46, 376, "   ——实因最近恒星比邻星 (4.24 光年) 视差也仅 0.768″，比肉眼细 78 倍！", 11.5, MUTED))
        els.append(txt(46, 404, "② 贝塞尔首破纪录 (1838)：用劈裂物镜量日仪测出天鹅座 61 视差 0.314″", 11.5, BLUE, weight="700"))
        els.append(txt(46, 424, "   (现代盖亚值 0.286″，距地球 11.4 光年)，人类首次量出太阳系外恒星距离！", 11.5, BODY))
        els.append(txt(46, 452, "③ 欧空局盖亚卫星 Gaia (DR3, 2022)：精测 14.68 亿颗恒星视差与自行，", 11.5, GREEN, weight="700"))
        els.append(txt(46, 472, "   亮星精度达 10–20 微角秒 (μas) ≈ 在地球看清月球上一根头发丝！", 11.5, INK, weight="700"))
        els.append(txt(46, 495, "   核心公式一脉相承：距离 D = 基线半长 (1 AU) / tan ϖ ≈ 1 AU / ϖ", 11.5, PURPLE, weight="700"))

        # Panel B: Four-Tier Baseline Ladder
        els.append(card(484, 64, 256, 458))
        els.append(pill(498, 74, "B · 四级“视差标尺”大跳级", fg=TEAL, bg=TEAL_SOFT, w=228))

        tiers = [
            (
                "第 1 级 · 双眼瞳距",
                "基线 B ≈ 6.5 cm",
                "看 40 cm 拇指跳 ~9.3°；",
                "超过百米双眼立体感渐失。",
                SLATE,
                SLATE_SOFT,
            ),
            (
                "第 2 级 · 高速行车",
                "基线 B = 100 m (3.6s)",
                "看 20 m 树狂扫 136.4°；",
                "看月球仅 0.054″→跟着车走！",
                ORANGE,
                ORANGE_SOFT,
            ),
            (
                "第 3 级 · 洲际南北联测",
                "基线 B ≈ 8,720 km",
                "1751 拉卡伊(好望角)与拉朗德",
                "(柏林)同测月球错开 ~1.3°！",
                BLUE,
                BLUE_SOFT,
            ),
            (
                "第 4 级 · 地球公转轨道",
                "基线 B = 2 AU ≈ 3 亿 km",
                "比汽车基线放大 300 万倍，",
                "直接量出百亿亿公里恒星海！",
                GREEN,
                GREEN_SOFT,
            ),
        ]
        for idx, (t_title, t_base, t_l1, t_l2, fg_t, bg_t) in enumerate(tiers):
            cy_card = 106 + idx * 102
            els.append(card(498, cy_card, 228, 94, rx=8, fill=bg_t, stroke=fg_t, sw=1))
            els.append(txt(510, cy_card + 20, t_title, 12, fg_t, weight="700"))
            els.append(txt(510, cy_card + 40, t_base, 11, INK, weight="700"))
            els.append(txt(510, cy_card + 61, t_l1, 11.5, BODY))
            els.append(txt(510, cy_card + 81, t_l2, 11.5, INK, weight="600"))

        return figure(
            538,
            "地球公转2AU三亿公里基线恒星周年视差原理、贝塞尔与盖亚卫星里程碑及四级视差标尺对比图解",
            "左图展示1月与7月地球横跨3亿公里基线观测近距恒星在遥远背景星幕上的周年视差摆动，梳理第谷、1838年贝塞尔首测天鹅座61与2022年盖亚卫星14.68亿星微角秒测距；右图对比双眼6.5厘米、行车100米、洲际8720公里与地球轨道3亿公里四级视差标尺。",
            els,
        )

    @register("moon-following-car", "太阳和月亮为什么跟着汽车走五步图解：车窗视差速度阶梯动画、双对数60角秒门槛与转弯、参考系与诱导运动错觉、自转线速度与协和号追日及宇宙恒星视差尺", "mechanics_sky")
    def build_moon_following_car():
        write_svg(SUBDIR, "car-window-motion-parallax-hierarchy.svg", _build_window_parallax_hierarchy())
        write_svg(SUBDIR, "angular-shift-log-scale-vs-eye-limit.svg", _build_log_scale_and_turn())
        write_svg(SUBDIR, "induced-motion-and-window-reference-frame.svg", _build_induced_motion_and_frame())
        write_svg(SUBDIR, "earth-curvature-and-supersonic-sun-chase.svg", _build_curvature_and_concorde())
        write_svg(SUBDIR, "cosmic-baseline-stellar-parallax-ruler.svg", _build_cosmic_stellar_parallax())


_register_moon_following_car()


def _register_spacetime_cosmos():
    SUBDIR = "spacetime-cosmos"
    RED = "#b91c1c"
    RED_SOFT = "#fef2f2"
    AMBER = "#b45309"
    AMBER_SOFT = "#fffbeb"
    TEAL = "#0f766e"
    TEAL_SOFT = "#f0fdfa"

    def _build_cosmic_lookback_ladder():
        els = []
        els += header(
            "一、抬头没有“现在”：从月球 1.28 秒前到韦布 135 亿年前的回望阶梯",
            "光速被精确定义为 c = 299,792,458 m/s——在宇宙里望向远处，本质上就是用望远镜翻阅不同年代的历史底片",
        )

        # Panel A: Logarithmic lookback time ladder
        els.append(card(20, 64, 456, 452))
        els.append(pill(34, 74, "A · 六级宇宙“时间延迟尺”（按 log₁₀ 秒精确换算）", fg=BLUE, bg=BLUE_SOFT, w=346))

        # Axis ticks from 10^0 s to 10^18 s
        x0, x1 = 152.0, 452.0
        els.append(f'<line x1="{x0:.1f}" y1="118" x2="{x1:.1f}" y2="118" stroke="{HAIRLINE}" stroke-width="1"/>')
        for exp_s, lbl_s in [(0, "1 秒"), (4, "3 小时"), (8, "3.2 年"), (12, "3.2 万年"), (16, "3.2 亿年"), (18, "317 亿年")]:
            xt = x0 + (exp_s / 18.0) * (x1 - x0)
            els.append(f'<line x1="{xt:.1f}" y1="113" x2="{xt:.1f}" y2="452" stroke="#f1f5f9" stroke-width="1"/>')
            els.append(txt(xt, 110, lbl_s, 10, MUTED, anchor="middle"))

        rungs = [
            ("① 月球", 1.282, "1.28 秒前", "距离 38.44 万 km · 阿波罗通话延迟", SLATE, SLATE_SOFT),
            ("② 太阳", 499.0, "8 分 19 秒前", "1 AU ≈ 1.50 亿 km · 此刻阳光发自 8 分钟前", AMBER, AMBER_SOFT),
            ("③ 比邻星", 4.25 * 365.25 * 86400, "约 4.25 年前", "最近恒星邻居 · 4.25 光年外", GREEN, GREEN_SOFT),
            ("④ 仙女座 M31", 2.5e6 * 365.25 * 86400, "约 250 万年前", "肉眼最远大星系 · 地球早期人类刚打制石器", BLUE, BLUE_SOFT),
            ("⑤ JADES-GS-z14-0", 1.35e10 * 365.25 * 86400, "约 135 亿年前", "z = 14.32 (韦布 2024) · 大爆炸后仅 2.9 亿年", PURPLE, PURPLE_SOFT),
            ("⑥ 微波背景 CMB", 1.38e10 * 365.25 * 86400, "约 138 亿年前", "z ≈ 1090 (2.7255 K) · 大爆炸后 38 万年首缕光", RED, RED_SOFT),
        ]
        for idx, (r_name, t_sec, r_time, r_note, fg_r, bg_r) in enumerate(rungs):
            ry = 132 + idx * 54
            bar_end = x0 + (math.log10(t_sec) / 18.0) * (x1 - x0)
            bar_w = max(8.0, bar_end - x0)
            els.append(txt(34, ry + 16, r_name, 11.5, INK, weight="700"))
            els.append(f'<rect x="{x0:.1f}" y="{ry + 2:.1f}" width="{bar_w:.1f}" height="18" rx="5" fill="{bg_r}" stroke="{fg_r}" stroke-width="1.3"/>')
            els.append(f'<circle cx="{x0 + bar_w:.1f}" cy="{ry + 11:.1f}" r="4" fill="{fg_r}"/>')
            lbl_x = min(378.0, x0 + bar_w + 8.0)
            if x0 + bar_w > 365.0:
                els.append(txt(x0 + bar_w - 8.0, ry + 15, r_time, 10.5, fg_r, anchor="end", weight="700", halo=True))
            else:
                els.append(txt(lbl_x, ry + 15, r_time, 11, fg_r, weight="700"))
            els.append(txt(x0, ry + 36, r_note, 10.5, BODY))

        els.append(card(34, 462, 428, 42, rx=7, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 480, "关键结论：“光年”是长度单位（光走 1 年 ≈ 9.46 万亿 km），但宇宙深空", 10.8, INK, weight="700"))
        els.append(txt(46, 497, "没有“实时直播”——空间距离越远，你看到的必然是越遥远的过去。", 10.8, MUTED))

        # Panel B: Collapse of "Universal Now" (Andromeda Paradox)
        els.append(card(490, 64, 250, 452))
        els.append(pill(504, 74, "B · “全宇宙同一个现在”破产", fg=ORANGE, bg=ORANGE_SOFT, w=222))

        # Spacetime loaf slice diagram
        els.append(card(504, 108, 222, 182, rx=8, fill="#0f172a", stroke="#334155"))
        # Earth worldline & M31 worldline
        ex, mx = 542, 688
        els.append(f'<line x1="{ex}" y1="126" x2="{ex}" y2="274" stroke="#38bdf8" stroke-width="2"/>')
        els.append(f'<line x1="{mx}" y1="126" x2="{mx}" y2="274" stroke="#c084fc" stroke-width="2"/>')
        els.append('<text x="542" y="122" font-size="10.5" fill="#bae6fd" text-anchor="middle" font-weight="700">地球</text>')
        els.append('<text x="688" y="122" font-size="10.5" fill="#e9d5ff" text-anchor="middle" font-weight="700">仙女座 M31</text>')

        # Rest observer horizontal slice vs walking observer tilted slice
        els.append(f'<line x1="522" y1="214" x2="708" y2="214" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5 3"/>')
        els.append(f'<line x1="522" y1="220" x2="708" y2="162" stroke="#fb923c" stroke-width="2"/>')
        els.append(f'<circle cx="{ex}" cy="214" r="4.5" fill="#facc15"/>')
        els.append(f'<circle cx="{mx}" cy="214" r="4" fill="#94a3b8"/>')
        els.append(f'<circle cx="{mx}" cy="168" r="4.5" fill="#fb923c"/>')
        els.append('<text x="614" y="232" font-size="10" fill="#cbd5e1" text-anchor="middle">静坐者的“此刻”切片</text>')
        els.append('<text x="608" y="176" font-size="10" fill="#fed7aa" text-anchor="middle" font-weight="700">朝 M31 步行者的“此刻”</text>')
        els.append('<text x="682" y="195" font-size="10.5" fill="#fde047" text-anchor="end" font-weight="700">差约 3 天!</text>')
        els.append('<text x="615" y="282" font-size="10" fill="#94a3b8" text-anchor="middle">相距 L ≈ 250 万光年</text>')

        els.append(txt(504, 314, "彭罗斯“仙女座悖论”：", 11.5, ORANGE, weight="700"))
        els.append(txt(504, 335, "在地球街头擦肩而过的两个人：", 11, BODY))
        els.append(txt(504, 355, "• 甲原地静坐；乙以 v = 1 m/s", 11, BODY))
        els.append(txt(504, 374, "  朝仙女座方向散步。", 11, BODY))
        els.append(txt(504, 396, "• 按洛伦兹变换 Δt = v·L / c²，", 11, INK, weight="700"))
        els.append(txt(504, 416, "  两人在 250 万光年外定义的", 11, BODY))
        els.append(txt(504, 435, "  “现在”，足足错开约 3.0 天！", 11, RED, weight="700"))
        els.append(txt(504, 460, "• 宇宙不是一秒一帧同步翻页的", 11, SLATE))
        els.append(txt(504, 479, "  连环画，而是一整块四维时空", 11, SLATE))
        els.append(txt(504, 498, "  面包，不同速度切出不同斜面。", 11, INK, weight="600"))

        return figure(
            532,
            "宇宙六级光速回望时间阶梯与仙女座悖论同时性相对性切片图解",
            "左图按对数秒展示从月球1.28秒、太阳8分19秒、比邻星4.25年、仙女座250万年到韦布JADES-GS-z14-0约135亿年前与CMB约138亿年前的回望阶梯；右图展示相距250万光年时步行1米每秒即可使同时面偏转约3天。",
            els,
        )

    def _build_minkowski_light_cone():
        extra_css = """
  @keyframes wlDraw {
    0% { stroke-dashoffset: 240; opacity: 0.25; }
    100% { stroke-dashoffset: 0; opacity: 1; }
  }
  @keyframes badgeFade {
    0%, 45% { opacity: 0.15; }
    100% { opacity: 1; }
  }
  .wl-rest { stroke-dasharray: 240; animation: wlDraw 1.5s ease-out 0.15s 1 both; }
  .wl-fast { stroke-dasharray: 240; animation: wlDraw 1.5s ease-out 0.45s 1 both; }
  .wl-phot { stroke-dasharray: 240; animation: wlDraw 1.5s ease-out 0.75s 1 both; }
  .wl-tag { animation: badgeFade 1.8s ease-out 0.2s 1 both; }
  @media (prefers-reduced-motion: reduce) {
    .wl-rest, .wl-fast, .wl-phot, .wl-tag {
      animation: none !important;
      stroke-dashoffset: 0 !important;
      opacity: 1 !important;
    }
  }
"""
        els = []
        els += header(
            "二、闵可夫斯基四维光锥与“总速度预算”：跑得快为什么时间变慢？",
            "单次动画演示三条世界线（支持减少动态效果）：空间与时间单独看只是影子，唯有 ds² = c²dt² − dx² 人人相等",
        )

        # Panel A: Minkowski Light Cone
        els.append(card(20, 64, 388, 456))
        els.append(pill(34, 74, "A · 四维时空光锥与因果边界（1908 闵可夫斯基）", fg=BLUE, bg=BLUE_SOFT, w=346))

        ox, oy = 214.0, 294.0
        dh_up, dh_dn = 152.0, 122.0
        # Shaded future & past light cones (exact 45 deg: dx = dy)
        els.append(f'<polygon points="{ox:.1f},{oy:.1f} {ox - dh_up:.1f},{oy - dh_up:.1f} {ox + dh_up:.1f},{oy - dh_up:.1f}" fill="{BLUE_SOFT}" stroke="none"/>')
        els.append(f'<polygon points="{ox:.1f},{oy:.1f} {ox - dh_dn:.1f},{oy + dh_dn:.1f} {ox + dh_dn:.1f},{oy + dh_dn:.1f}" fill="{SLATE_SOFT}" stroke="none"/>')
        # Elliptical 3D cone caps for visual clarity
        els.append(f'<ellipse cx="{ox:.1f}" cy="{oy - dh_up:.1f}" rx="{dh_up:.1f}" ry="16" fill="#dbeafe" fill-opacity="0.55" stroke="{BLUE}" stroke-width="1" stroke-dasharray="4 3"/>')
        els.append(f'<ellipse cx="{ox:.1f}" cy="{oy + dh_dn:.1f}" rx="{dh_dn:.1f}" ry="13" fill="#e2e8f0" fill-opacity="0.55" stroke="{SLATE}" stroke-width="1" stroke-dasharray="4 3"/>')

        # Axes: horizontal x, vertical ct
        els.append(f'<line x1="42" y1="{oy:.1f}" x2="386" y2="{oy:.1f}" stroke="{SLATE}" stroke-width="1.3" marker-end="url(#arr-muted)"/>')
        els.append(f'<line x1="{ox:.1f}" y1="432" x2="{ox:.1f}" y2="114" stroke="{SLATE}" stroke-width="1.3" marker-end="url(#arr-muted)"/>')
        els.append(txt(384, oy + 16, "空间 x", 11, SLATE, anchor="end", weight="700"))
        els.append(txt(ox + 8, 122, "时间 ct", 11, SLATE, weight="700"))

        # 45-deg light cone walls
        els.append(f'<line x1="{ox - dh_dn:.1f}" y1="{oy + dh_dn:.1f}" x2="{ox + dh_up:.1f}" y2="{oy - dh_up:.1f}" stroke="{AMBER}" stroke-width="2" class="wl-phot"/>')
        els.append(f'<line x1="{ox + dh_dn:.1f}" y1="{oy + dh_dn:.1f}" x2="{ox - dh_up:.1f}" y2="{oy - dh_up:.1f}" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="5 3"/>')

        # Worldline A: stationary (dx=0, dy=-142) & Worldline B: fast v=0.6c (dx=+85, dy=-142)
        els.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ox:.1f}" y2="{oy - 140:.1f}" stroke="{GREEN}" stroke-width="2.8" marker-end="url(#arr-green)" class="wl-rest"/>')
        els.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ox + 84:.1f}" y2="{oy - 140:.1f}" stroke="{ORANGE}" stroke-width="2.8" marker-end="url(#arr-orange)" class="wl-fast"/>')
        els.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="5" fill="{INK}"/>')

        # Labels on cone
        els.append(txt(ox - 6, oy - 86, "① 静止者 A (v=0)", 11, GREEN, anchor="end", weight="700", halo=True, cls="wl-tag"))
        els.append(txt(ox - 6, oy - 70, "时间全速流逝", 10.5, GREEN, anchor="end", halo=True, cls="wl-tag"))
        els.append(txt(ox + 58, oy - 102, "② 飞船 B (0.6c)", 11, ORANGE, weight="700", halo=True, cls="wl-tag"))
        els.append(txt(ox + 58, oy - 86, "dτ = 0.8 dt", 10.5, ORANGE, weight="600", halo=True, cls="wl-tag"))
        els.append(txt(ox + 108, oy - 56, "③ 光线 (v=c)", 11, AMBER, weight="700", halo=True, cls="wl-tag"))
        els.append(txt(ox + 108, oy - 40, "ds² = 0, dτ = 0", 10.5, AMBER, halo=True, cls="wl-tag"))

        els.append(txt(ox, oy - 134, "绝对未来 (ds² > 0 · 因果可达)", 10.5, BLUE, anchor="middle", weight="700", halo=True))
        els.append(txt(ox, oy + 96, "绝对过去 (曾发信号影响此刻 O)", 10.5, SLATE, anchor="middle", weight="700", halo=True))
        els.append(txt(88, oy - 18, "类空区", 11, RED, anchor="middle", weight="700"))
        els.append(txt(88, oy - 3, "ds² < 0", 10.5, RED, anchor="middle"))
        els.append(txt(88, oy + 13, "因果绝缘", 10.5, MUTED, anchor="middle"))
        els.append(txt(214, oy + 16, "事件 O（此时此地）", 10.5, INK, anchor="middle", weight="700", halo=True))

        els.append(card(34, 444, 360, 62, rx=7, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 464, "光锥铁律：任何有质量物体只能走光锥内部 (v < c)；", 10.8, INK, weight="700"))
        els.append(txt(46, 482, "光锥外的“类空事件”连光都来不及赶到，绝不可能互为因果！", 10.5, BODY))

        # Panel B: Quarter-circle time-budget curve + Cosmic-ray muon proof
        els.append(card(422, 64, 318, 456))
        els.append(pill(436, 74, "B · 时间膨胀圆弧与大气 μ 子铁证", fg=PURPLE, bg=PURPLE_SOFT, w=274))

        # Quarter circle plot: x = v/c in [0,1], y = d_tau/dt = sqrt(1 - (v/c)^2) in [0,1]
        gx0, gy0, gw = 472.0, 266.0, 146.0
        els.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0 + gw + 18:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.2" marker-end="url(#arr-muted)"/>')
        els.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0:.1f}" y2="{gy0 - gw - 16:.1f}" stroke="{SLATE}" stroke-width="1.2" marker-end="url(#arr-muted)"/>')
        els.append(txt(gx0 - 6, gy0 - gw + 4, "1.0", 10, MUTED, anchor="end"))
        els.append(txt(gx0 - 6, gy0 + 4, "0", 10, MUTED, anchor="end"))
        els.append(txt(gx0 + gw, gy0 + 14, "1.0 c", 10, MUTED, anchor="middle"))
        els.append(txt(gx0 + gw * 0.5, gy0 + 15, "空间速度 v / c →", 10.5, SLATE, anchor="middle", weight="600"))
        els.append(txt(gx0 + 8, gy0 - gw - 14, "自身时间流速 dτ/dt", 10.5, PURPLE, weight="700"))

        arc_pts = []
        for i in range(61):
            vc = i / 60.0
            rt = math.sqrt(max(0.0, 1.0 - vc * vc))
            arc_pts.append(f"{gx0 + vc * gw:.2f},{gy0 - rt * gw:.2f}")
        els.append(f'<polyline points="{" ".join(arc_pts)}" fill="none" stroke="{PURPLE}" stroke-width="2.5"/>')

        # Key points on quarter-circle
        for vc_m, lbl_m, col_m, dx_l, dy_l in [
            (0.0, "静止 (100%)", GREEN, 8, 13),
            (0.6, "0.6c → 80%", ORANGE, 8, -4),
            (0.866, "0.87c → 50%", BLUE, 8, -2),
            (0.9957, "μ子 0.9957c → 11%", RED, 8, -6),
        ]:
            rt_m = math.sqrt(1.0 - vc_m * vc_m)
            px_m, py_m = gx0 + vc_m * gw, gy0 - rt_m * gw
            els.append(f'<circle cx="{px_m:.1f}" cy="{py_m:.1f}" r="4" fill="{col_m}"/>')
            els.append(txt(px_m + dx_l, py_m + dy_l, lbl_m, 10, col_m, weight="700"))

        # Muon box
        els.append(card(436, 296, 290, 210, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1))
        els.append(txt(448, 318, "大自然每天上演的铁证：高空宇宙线 μ 子", 11.5, ORANGE, weight="700"))
        els.append(txt(448, 340, "• 静止固有寿命 τ₀ = 2.197 微秒 (MuLan)", 11, INK, weight="600"))
        els.append(txt(448, 360, "  若无相对论：哪怕以光速飞，一辈子也只", 11, BODY))
        els.append(txt(448, 379, "  能走 c·τ₀ ≈ 659 米，绝难从高山落到海面！", 11, BODY))
        els.append(txt(448, 403, "• 1963 华盛顿山实测 (Frisch & Smith)：", 11, BLUE, weight="700"))
        els.append(txt(448, 423, "  速度 0.9954c–0.9960c 的 μ 子，地面测得", 11, BODY))
        els.append(txt(448, 442, "  寿命拉长 8.8 ± 0.8 倍，大批活到海平面！", 11, INK, weight="700"))
        els.append(txt(448, 466, "• 换到 μ 子视角：自己只活 2.2 微秒，但整座", 10.8, GREEN, weight="700"))
        els.append(txt(448, 485, "  1,907 米高山被“尺缩效应”压扁成 ~217 米！", 10.8, GREEN, weight="600"))

        return figure(
            536,
            "闵可夫斯基四维光锥世界线动画与时间膨胀圆弧及大气μ子寿命实测图解",
            "左图以单次动画展示静止观测者、0.6c飞船与光子在四维光锥中的世界线及类空因果绝缘区；右图精确绘制dτ/dt四分之一圆弧并给出1963年宇宙线μ子钟慢8.8倍穿透大气层的判决实验。",
            els,
            extra_css=extra_css,
        )

    def _build_curved_spacetime_gps():
        els = []
        els += header(
            "三、引力把时间拽慢：从手机 GPS 每天快 38 微秒到 1 毫米原子钟",
            "广义相对论揭示：越靠近大质量天体（引力势越深）时间走得越慢；轨道卫星同时受“引力快钟”与“高速慢钟”拉锯",
        )

        # Panel A: Exact calculated satellite clock offset vs orbital altitude h
        els.append(card(20, 64, 440, 452))
        els.append(pill(34, 74, "A · 地球圆轨道时钟日频移曲线（精确代入 GM_E 与 c² 计算）", fg=BLUE, bg=BLUE_SOFT, w=392))

        px0, px1 = 76.0, 434.0
        py_top, py_bot = 122.0, 368.0
        # y maps [-30, +60] us/day
        def map_x(h_km):
            return px0 + (h_km / 24000.0) * (px1 - px0)

        def map_y(us_day):
            return py_bot - ((us_day - (-30.0)) / 90.0) * (py_bot - py_top)

        y_zero = map_y(0.0)
        els.append(f'<rect x="{px0:.1f}" y="{py_top:.1f}" width="{px1 - px0:.1f}" height="{py_bot - py_top:.1f}" fill="#f8fafc" stroke="{BORDER}"/>')
        for y_val in [-20, 0, 20, 40, 60]:
            yv = map_y(y_val)
            sw_g = "1.4" if y_val == 0 else "1"
            col_g = SLATE if y_val == 0 else "#e2e8f0"
            els.append(f'<line x1="{px0:.1f}" y1="{yv:.1f}" x2="{px1:.1f}" y2="{yv:.1f}" stroke="{col_g}" stroke-width="{sw_g}"/>')
            els.append(txt(px0 - 6, yv + 4, f"{y_val:+d}" if y_val != 0 else "0", 10, MUTED, anchor="end"))

        for h_tick in [0, 5000, 10000, 15000, 20000]:
            xt = map_x(h_tick)
            els.append(f'<line x1="{xt:.1f}" y1="{py_top:.1f}" x2="{xt:.1f}" y2="{py_bot:.1f}" stroke="#eef2f7" stroke-width="1"/>')
            els.append(txt(xt, py_bot + 15, f"{h_tick // 1000}万km" if h_tick >= 10000 else f"{h_tick}km", 10, MUTED, anchor="middle"))

        els.append(txt((px0 + px1) / 2, py_bot + 32, "卫星离地轨道高度 h →", 11, SLATE, anchor="middle", weight="600"))
        els.append(txt(px0 + 6, py_top + 14, "相对地面时钟：微秒/天 (μs/d)", 10.5, SLATE, weight="600"))

        # Compute exact curves: R_E = 6378.137 km, GM = 398600.4418 km^3/s^2, c = 299792.458 km/s
        re_km = 6378.137
        gm_c2 = 398600.4418 / (299792.458 ** 2)
        sec_us = 86400.0 * 1e6
        pts_gr, pts_sr, pts_net = [], [], []
        for i in range(1, 97):
            h_k = 250.0 * i
            r_k = re_km + h_k
            d_gr = gm_c2 * (1.0 / re_km - 1.0 / r_k) * sec_us
            d_sr = -0.5 * gm_c2 * (1.0 / r_k) * sec_us
            d_net = d_gr + d_sr
            pts_gr.append(f"{map_x(h_k):.2f},{map_y(d_gr):.2f}")
            pts_sr.append(f"{map_x(h_k):.2f},{map_y(d_sr):.2f}")
            pts_net.append(f"{map_x(h_k):.2f},{map_y(d_net):.2f}")

        els.append(f'<polyline points="{" ".join(pts_gr)}" fill="none" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 3"/>')
        els.append(f'<polyline points="{" ".join(pts_sr)}" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="4 3"/>')
        els.append(f'<polyline points="{" ".join(pts_net)}" fill="none" stroke="{BLUE}" stroke-width="2.8"/>')

        # Mark crossover altitude h ≈ 3,189 km (a ≈ 9,545 km) & GPS h ≈ 20,200 km
        x_zero_h = map_x(3189.0)
        els.append(f'<circle cx="{x_zero_h:.1f}" cy="{y_zero:.1f}" r="4.5" fill="{PURPLE}"/>')
        els.append(txt(x_zero_h + 6, y_zero + 15, "抵消高度 h ≈ 3,170 km (净差=0)", 10, PURPLE, weight="700", halo=True))

        x_gps = map_x(20200.0)
        els.append(f'<line x1="{x_gps:.1f}" y1="{py_top:.1f}" x2="{x_gps:.1f}" y2="{py_bot:.1f}" stroke="{ORANGE}" stroke-width="1.2" stroke-dasharray="3 3"/>')
        els.append(f'<circle cx="{x_gps:.1f}" cy="{map_y(45.6):.1f}" r="4" fill="{GREEN}"/>')
        els.append(f'<circle cx="{x_gps:.1f}" cy="{map_y(-7.2):.1f}" r="4" fill="{RED}"/>')
        els.append(f'<circle cx="{x_gps:.1f}" cy="{map_y(38.4):.1f}" r="5" fill="{BLUE}"/>')

        els.append(txt(245, map_y(43.0) - 8, "广义相对论（高处引力弱）：约 +45 μs/天", 10.5, GREEN, weight="700", halo=True))
        els.append(txt(250, map_y(-10.0) + 14, "狭义相对论（3.9 km/s 高速）：约 −7 μs/天", 10.5, RED, weight="700", halo=True))
        els.append(txt(x_gps - 8, map_y(38.4) + 15, "GPS 净快 ≈ +38 μs/天", 11, BLUE, anchor="end", weight="700", halo=True))

        els.append(card(34, 412, 412, 90, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1))
        els.append(txt(46, 433, "为什么手机地图没导航进河里？（NASA / Ashby 2003）", 11.5, BLUE, weight="700"))
        els.append(txt(46, 454, "• 每天快 38 微秒 × 光速 c ≈ 每天累积约 11.4 公里的测距狂漂！", 11, INK, weight="700"))
        els.append(txt(46, 474, "• 工程师在卫星发射前，故意把星载 10.23 MHz 原子钟基准调慢", 10.8, BODY))
        els.append(txt(46, 492, "  至 10.22999999543 MHz，上天入轨后刚好与地面分毫不差！", 10.8, BODY))

        # Panel B: 3-tier experimental staircase down to 1 millimeter
        els.append(card(474, 64, 266, 452))
        els.append(pill(488, 74, "B · 从太空到 1 毫米：实测三级跳", fg=TEAL, bg=TEAL_SOFT, w=238))

        stairs = [
            (
                "第 1 级 · 太空导航星座",
                "高度差 Δh ≈ 20,200 km",
                "国际空间站 (h≈400 km) 因飞得",
                "太快，宇航员反而比地面略年轻；",
                "GPS 高轨引力更弱，净快 38 μs/天。",
                BLUE,
                BLUE_SOFT,
            ),
            (
                "第 2 级 · 桌面抬高一级台阶",
                "高度差 Δh = 33 厘米 (NIST 2010)",
                "Chou 等用两台单铝离子 (Al⁺) 光钟",
                "实测：把上面那台仅垫高 33 cm，",
                "走时立刻变快（79年快约 90 纳秒）！",
                ORANGE,
                ORANGE_SOFT,
            ),
            (
                "第 3 级 · 一团原子云的上下两端",
                "高度差 Δh = 1 毫米 (JILA 2022)",
                "叶军团队在 Nature 发表：在 1 mm",
                "超冷锶原子晶格内部，直接测出顶部",
                "比底部走得快的引力红移 (10⁻²¹)！",
                GREEN,
                GREEN_SOFT,
            ),
        ]
        for idx, (s_title, s_sub, l1, l2, l3, fg_s, bg_s) in enumerate(stairs):
            sy = 108 + idx * 132
            els.append(card(488, sy, 238, 120, rx=8, fill=bg_s, stroke=fg_s, sw=1))
            els.append(txt(500, sy + 21, s_title, 11.8, fg_s, weight="700"))
            els.append(txt(500, sy + 40, s_sub, 10.5, INK, weight="700"))
            els.append(txt(500, sy + 62, l1, 10.8, BODY))
            els.append(txt(500, sy + 81, l2, 10.8, BODY))
            els.append(txt(500, sy + 100, l3, 10.8, INK, weight="600"))

        return figure(
            532,
            "广义与狭义相对论地球轨道时钟频移曲线、GPS每天38微秒修正及33厘米与1毫米光钟实测图解",
            "左图精确绘制圆轨道卫星广义相对论快钟、狭义相对论慢钟与净频移曲线，标出3170公里抵消高度与20200公里GPS轨道净快38微秒每天；右图汇总太空星座、2010年33厘米铝离子钟与2022年1毫米锶光晶格钟三级实测。",
            els,
        )

    def _build_black_hole_light_cone_tipping():
        els = []
        els += header(
            "四、黑洞视界内外的终极反转：为什么掉进视界后“奇点”变成了你的未来？",
            "越逼近史瓦西半径 r_s = 2GM/c²，未来光锥越向内倾倒；一旦跨过 r < r_s，空间径向 r 与时间 t 彻底互换角色",
        )

        # Top main panel: Light cone tipping across event horizon
        els.append(card(20, 64, 720, 272, rx=10, fill="#0f172a", stroke="#334155"))
        els.append('<text x="36" y="88" font-size="12" fill="#f8fafc" font-weight="700">径向时空剖面（爱丁顿—芬克尔斯坦无奇异视角：观察未来光锥如何一步步向内倾倒）</text>')

        # Singularity wavy line at x = 88, Event Horizon at x = 338, Radial axis to x = 716
        sx_bh, hx_bh = 92.0, 342.0
        els.append(f'<rect x="36" y="102" width="{hx_bh - 36:.1f}" height="218" rx="6" fill="#1e1b4b" fill-opacity="0.55"/>')
        wavy_d = "M 92,106 " + " ".join(
            f"L {92 + (5 if k % 2 == 0 else -5)},{114 + k * 10}" for k in range(21)
        )
        els.append(f'<path d="{wavy_d}" fill="none" stroke="#f87171" stroke-width="2.6"/>')
        els.append('<text x="80" y="122" font-size="11" fill="#fca5a5" text-anchor="end" font-weight="700">中心奇点</text>')
        els.append('<text x="80" y="138" font-size="10.5" fill="#fca5a5" text-anchor="end">r = 0</text>')

        # Event horizon line r = r_s
        els.append(f'<line x1="{hx_bh:.1f}" y1="102" x2="{hx_bh:.1f}" y2="320" stroke="#facc15" stroke-width="2.2" stroke-dasharray="6 4"/>')
        els.append(f'<text x="{hx_bh:.1f}" y="118" font-size="11" fill="#fde047" text-anchor="middle" font-weight="700">事件视界 r = r_s = 2GM/c²</text>')

        # Radial axis at bottom
        els.append('<line x1="92" y1="304" x2="716" y2="304" stroke="#64748b" stroke-width="1.3" marker-end="url(#arr-muted)"/>')
        els.append('<text x="712" y="320" font-size="10.5" fill="#cbd5e1" text-anchor="end">远离黑洞径向距离 r →</text>')

        # 4 Light cones at: r=0.5 r_s (x=216), r=1.0 r_s (x=342), r=1.6 r_s (x=492), r=3.0 r_s (x=646)
        cones = [
            # (cx, cy, left_dx, left_dy, right_dx, right_dy, label_top, label_bot, fill_c, stroke_c)
            (646, 238, -42, -58, 42, -58, "① 远处平直时空", "光锥竖直 · 来去自由", "#38bdf8", "#bae6fd"),
            (496, 238, -54, -56, 22, -58, "② 强引力区 (1.6 r_s)", "光锥内倾 · 逃逸变难", "#60a5fa", "#bfdbfe"),
            (342, 238, -62, -54, 0, -64, "③ 事件视界 (r = r_s)", "外射光原地冻结！", "#facc15", "#fef08a"),
            (216, 238, -68, -44, -20, -62, "④ 视界内部 (r < r_s)", "整个未来全指向 r=0！", "#f87171", "#fecaca"),
        ]
        for cx_c, cy_c, ldx, ldy, rdx, rdy, l_top, l_bot, sc_c, tx_c in cones:
            els.append(
                f'<polygon points="{cx_c},{cy_c} {cx_c + ldx},{cy_c + ldy} {cx_c + rdx},{cy_c + rdy}" '
                f'fill="{sc_c}" fill-opacity="0.28" stroke="{sc_c}" stroke-width="1.8"/>'
            )
            mx_top = cx_c + (ldx + rdx) * 0.5
            my_top = cy_c + (ldy + rdy) * 0.5
            rx_e = max(8.0, abs(rdx - ldx) * 0.5)
            els.append(f'<ellipse cx="{mx_top:.1f}" cy="{my_top:.1f}" rx="{rx_e:.1f}" ry="6" fill="{sc_c}" fill-opacity="0.35" stroke="{sc_c}" stroke-width="1.2"/>')
            els.append(f'<circle cx="{cx_c}" cy="{cy_c}" r="4" fill="#ffffff"/>')
            els.append(f'<text x="{cx_c}" y="264" font-size="10.8" fill="{tx_c}" text-anchor="middle" font-weight="700">{escape(l_top)}</text>')
            els.append(f'<text x="{cx_c}" y="281" font-size="10" fill="#cbd5e1" text-anchor="middle">{escape(l_bot)}</text>')

        # Bottom cards: Role reversal vs EHT real black hole benchmarks
        els.append(card(20, 350, 362, 164, rx=10, fill=RED_SOFT, stroke=RED, sw=1))
        els.append(pill(34, 360, "为什么跨过视界就绝无可能回头？（Carroll 广义相对论）", fg=RED, bg="#ffffff", w=334))
        els.append(txt(34, 400, "• 史瓦西度规中 (1 − r_s/r) 在 r < r_s 时正负号翻转：", 11, INK, weight="700"))
        els.append(txt(34, 421, "  原本是空间的径向 r 变成了“类时方向”！", 11, RED, weight="700"))
        els.append(txt(34, 443, "• 这意味着：视界内的中心奇点 r = 0 根本不是“前方", 11, BODY))
        els.append(txt(34, 462, "  房间里的一堵墙”，而是你时间轴上的“下周一”！", 11, INK, weight="600"))
        els.append(txt(34, 484, "• 就像没人能阻止自己变老，视界内开火箭乱挣扎，", 10.8, BODY))
        els.append(txt(34, 502, "  反而会因时间膨胀缩短你抵达奇点的剩余固有寿命。", 10.8, SLATE, weight="600"))

        els.append(card(398, 350, 342, 164, rx=10, fill=PURPLE_SOFT, stroke=PURPLE, sw=1))
        els.append(pill(412, 360, "人类亲眼拍到的两座真实视界（EHT 合作组）", fg=PURPLE, bg="#ffffff", w=308))
        els.append(txt(412, 400, "① 银河系中心人马座 A* (Sgr A*, 2022 公布)：", 11, PURPLE, weight="700"))
        els.append(txt(412, 420, "   质量 ≈ 400 万倍太阳，r_s ≈ 1,180 万 km，", 10.8, BODY))
        els.append(txt(412, 439, "   光环角直径 51.8 ± 2.3 微角秒。", 10.8, INK, weight="600"))
        els.append(txt(412, 463, "② 室女座巨星系 M87* (2019 首张黑洞照片)：", 11, PURPLE, weight="700"))
        els.append(txt(412, 483, "   质量 (65 ± 7) 亿倍太阳，r_s ≈ 192 亿 km", 10.8, BODY))
        els.append(txt(412, 502, "   (≈ 128 AU，足可吞下整个太阳系冥王星轨道！)", 10.8, INK, weight="700"))

        return figure(
            528,
            "黑洞史瓦西视界内外未来光锥倾倒、时间与空间角色互换及EHT双黑洞实测参数图解",
            "上图展示从远处平直时空、强引力区、事件视界r=r_s到视界内部r<r_s未来光锥逐步向内倾倒直至完全指向奇点r=0；下图解释度规符号翻转导致r变为时间方向，并列出Sgr A*与M87*实测质量与史瓦西半径。",
            els,
        )

    def _build_expanding_universe_horizon():
        els = []
        els += header(
            "五、138 亿岁的宇宙凭什么宽达 920 多亿光年？膨胀空间与水滴光锥",
            "远方星系退行速度 v = H₀D 超过光速并不违背相对论——不是飞船跑赢当地光速，而是星系间的空间尺度本身在膨胀",
        )

        # Panel A: Concentric Observable Universe vs Hubble Sphere
        els.append(card(20, 64, 356, 458))
        els.append(pill(34, 74, "A · 可观测宇宙视界 vs 哈勃球（共动今天切片）", fg=BLUE, bg=BLUE_SOFT, w=324))

        cx_u, cy_u = 198.0, 232.0
        r_obs = 124.0
        r_hub = r_obs * (14.5 / 46.2)  # exact proportion ~ 38.9 px
        r_z14 = r_obs * (33.8 / 46.2)  # JADES-GS-z14-0 today ~ 90.7 px

        els.append(f'<circle cx="{cx_u:.1f}" cy="{cy_u:.1f}" r="{r_obs:.1f}" fill="#0f172a" stroke="{BLUE}" stroke-width="2.2"/>')
        els.append(f'<circle cx="{cx_u:.1f}" cy="{cy_u:.1f}" r="{r_z14:.1f}" fill="none" stroke="#a855f7" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append(f'<circle cx="{cx_u:.1f}" cy="{cy_u:.1f}" r="{r_hub:.1f}" fill="#1e3a8a" fill-opacity="0.55" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="5 3"/>')
        els.append(f'<circle cx="{cx_u:.1f}" cy="{cy_u:.1f}" r="4.5" fill="#facc15"/>')

        # Dimension radius arrow
        els.append(f'<line x1="{cx_u:.1f}" y1="{cy_u:.1f}" x2="{cx_u + r_obs:.1f}" y2="{cy_u:.1f}" stroke="#fbbf24" stroke-width="1.5" marker-end="url(#arr-orange)"/>')
        els.append(f'<circle cx="{cx_u - r_z14 * 0.72:.1f}" cy="{cy_u - r_z14 * 0.69:.1f}" r="4.5" fill="#e879f9"/>')

        els.append(f'<text x="{cx_u:.1f}" y="{cy_u + 16:.1f}" font-size="10" fill="#fef08a" text-anchor="middle" font-weight="700">地球</text>')
        els.append(f'<text x="{cx_u:.1f}" y="{cy_u - r_hub - 6:.1f}" font-size="10" fill="#7dd3fc" text-anchor="middle" font-weight="700">哈勃球 ≈ 145 亿光年</text>')
        els.append(f'<text x="{cx_u + 62:.1f}" y="{cy_u - 6:.1f}" font-size="10.5" fill="#fde047" text-anchor="middle" font-weight="700">半径 ≈ 462 亿光年</text>')
        els.append(f'<text x="{cx_u:.1f}" y="{cy_u - r_obs + 18:.1f}" font-size="10" fill="#cbd5e1" text-anchor="middle">粒子视界边界（全宽 ≈ 924–932 亿光年）</text>')
        els.append(f'<text x="{cx_u - 22:.1f}" y="{cy_u - 72:.1f}" font-size="10" fill="#f5d0fe">z=14.32 星系今天距我们 ≈ 338 亿光年</text>')

        els.append(card(34, 372, 328, 136, rx=8, fill="#f8fafc", stroke=BORDER))
        els.append(txt(46, 393, "为什么 138 亿年能跑出 460 多亿光年？（Gott 2005）", 11, INK, weight="700"))
        els.append(txt(46, 413, "• 就像蚂蚁在不断拉长的橡皮筋上爬：光子向我们跑来", 10.8, BODY))
        els.append(txt(46, 432, "  的同时，它身后的空间已被宇宙膨胀拉长了数倍！", 10.8, BODY))
        els.append(txt(46, 454, "• 哈勃常数悬案：普朗克早期宇宙测得 H₀ = 67.4，而", 10.8, PURPLE, weight="700"))
        els.append(txt(46, 473, "  SH0ES 造父变星测得 73.04 km/s/Mpc（5σ 哈勃张力", 10.8, BODY))
        els.append(txt(46, 492, "  至今是现代宇宙学头号未解之谜！）。", 10.8, INK, weight="600"))

        # Panel B: Numerically integrated LCDM Teardrop Past Light Cone
        els.append(card(392, 64, 348, 458))
        els.append(pill(406, 74, "B · 真实 ΛCDM“水滴形”过去光锥（Davis & Lineweaver）", fg=ORANGE, bg=ORANGE_SOFT, w=320))

        # Numerical integration of flat LCDM (Omega_m=0.315, Omega_L=0.685, H0=67.4 => 1/H0 = 14.51 Gly)
        om, ol, c_h0 = 0.315, 0.685, 14.51
        n_steps = 240
        a_vals = [0.002 + (0.998 * i) / n_steps for i in range(n_steps + 1)]
        t_gyr = [0.0] * (n_steps + 1)
        chi_gly = [0.0] * (n_steps + 1)  # comoving distance from today (a=1)

        def e_func(a_v):
            return math.sqrt(om / (a_v ** 3) + ol)

        for i in range(1, n_steps + 1):
            a0, a1 = a_vals[i - 1], a_vals[i]
            am = 0.5 * (a0 + a1)
            da = a1 - a0
            t_gyr[i] = t_gyr[i - 1] + c_h0 * da / (am * e_func(am))

        for i in range(n_steps - 1, -1, -1):
            a0, a1 = a_vals[i], a_vals[i + 1]
            am = 0.5 * (a0 + a1)
            da = a1 - a0
            chi_gly[i] = chi_gly[i + 1] + c_h0 * da / (am * am * e_func(am))

        t_now = t_gyr[-1]  # ~13.8 Gyr
        xc = 566.0
        yt_top, yt_bot = 124.0, 392.0
        scale_d = 12.2  # px per Gly (max D_proper ~ 5.8 Gly -> ~71 px half-width)

        def map_ty(t_v):
            return yt_bot - (t_v / t_now) * (yt_bot - yt_top)

        # Plot frame
        els.append(f'<rect x="424" y="{yt_top:.1f}" width="284" height="{yt_bot - yt_top:.1f}" fill="#f8fafc" stroke="{BORDER}"/>')
        els.append(f'<line x1="{xc:.1f}" y1="{yt_top:.1f}" x2="{xc:.1f}" y2="{yt_bot:.1f}" stroke="{SLATE}" stroke-width="1.2" stroke-dasharray="3 3"/>')
        for t_lbl in [0, 4, 8, 13.8]:
            yl = map_ty(min(t_lbl, t_now))
            els.append(f'<line x1="424" y1="{yl:.1f}" x2="708" y2="{yl:.1f}" stroke="#eef2f7" stroke-width="1"/>')
            els.append(txt(418, yl + 4, f"{int(round(t_lbl * 10))}亿年" if t_lbl > 0 else "0", 9.8, MUTED, anchor="end"))

        # Hubble sphere proper radius D_HS(a) = c / H(a) = c_h0 / e_func(a)
        hs_r, hs_l, lc_r, lc_l = [], [], [], []
        max_dp, max_idx = 0.0, 0
        for i in range(n_steps + 1):
            a_v = a_vals[i]
            dp = a_v * chi_gly[i]
            if dp > max_dp:
                max_dp, max_idx = dp, i
            d_hs = min(11.0, c_h0 / e_func(a_v))
            yy = map_ty(t_gyr[i])
            lc_r.append(f"{xc + dp * scale_d:.2f},{yy:.2f}")
            lc_l.append(f"{xc - dp * scale_d:.2f},{yy:.2f}")
            hs_r.append(f"{xc + d_hs * scale_d:.2f},{yy:.2f}")
            hs_l.append(f"{xc - d_hs * scale_d:.2f},{yy:.2f}")

        poly_lc = lc_r + list(reversed(lc_l))
        els.append(f'<polygon points="{" ".join(poly_lc)}" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="2.2"/>')
        els.append(f'<polyline points="{" ".join(hs_r)}" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="5 3"/>')
        els.append(f'<polyline points="{" ".join(hs_l)}" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="5 3"/>')

        # Mark Earth Today & Turnaround maximum (~58 亿光年 near t ~ 40 亿年)
        els.append(f'<circle cx="{xc:.1f}" cy="{yt_top:.1f}" r="4.5" fill="{INK}"/>')
        els.append(txt(xc + 8, yt_top + 12, "今天地球 (138亿年)", 10, INK, weight="700"))

        y_turn = map_ty(t_gyr[max_idx])
        x_turn = xc + max_dp * scale_d
        els.append(f'<circle cx="{x_turn:.1f}" cy="{y_turn:.1f}" r="4.5" fill="{RED}"/>')
        els.append(txt(x_turn + 6, y_turn + 4, "折返点 ≈ 58亿光年", 10, RED, weight="700", halo=True))
        els.append(txt(xc + 62, yt_top + 48, "蓝色虚线：哈勃球", 10, BLUE, weight="700", halo=True))
        els.append(txt(xc, yt_bot + 16, "← 发光时与地球的真实固有距离 D_proper →", 10.2, SLATE, anchor="middle", weight="600"))

        els.append(txt(406, 428, "• 为什么过去光锥长成“水滴形”而非三角形？", 11, ORANGE, weight="700"))
        els.append(txt(406, 448, "  大爆炸早期发出的光子（如 z=14.32），最初身处哈勃球外，", 10.6, BODY))
        els.append(txt(406, 466, "  空间膨胀太快，光子起初竟在被冲离地球（水滴向外鼓）！", 10.6, BODY))
        els.append(txt(406, 485, "  直到约 40 亿岁穿过哈勃球（折返点），才一路顺流跑进望远镜！", 10.6, INK, weight="700"))

        return figure(
            538,
            "可观测宇宙462亿光年粒子视界与哈勃球对比及ΛCDM水滴形过去光锥数值积分图解",
            "左图按比例对比145亿光年哈勃球、JADES-GS-z14-0今日约338亿光年共动距离与462亿光年可观测宇宙半径；右图由ΛCDM数值积分绘制水滴形过去光锥，展示早期光子先被超光速膨胀冲远至58亿光年折返点再抵达地球。",
            els,
        )

    @register(
        "spacetime-cosmos",
        "宇宙视角下的时间与空间五步图解：六级光速回望与同时性破产、闵可夫斯基光锥动画与μ子实测、引力慢钟与GPS毫米光钟、黑洞视界时空互换及膨胀宇宙水滴光锥",
        "mechanics_sky",
    )
    def build_spacetime_cosmos():
        write_svg(SUBDIR, "cosmic-lookback-time-ladder.svg", _build_cosmic_lookback_ladder())
        write_svg(SUBDIR, "minkowski-light-cone-and-time-budget.svg", _build_minkowski_light_cone())
        write_svg(SUBDIR, "curved-spacetime-gps-and-mm-clock.svg", _build_curved_spacetime_gps())
        write_svg(SUBDIR, "black-hole-light-cone-tipping.svg", _build_black_hole_light_cone_tipping())
        write_svg(SUBDIR, "expanding-universe-horizon-paradox.svg", _build_expanding_universe_horizon())


_register_spacetime_cosmos()


def _register_permanent_magnet_energy():
    SUBDIR = "permanent-magnet-energy"
    RED = "#dc2626"
    RED_SOFT = "#fef2f2"
    AMBER = "#d97706"
    AMBER_SOFT = "#fffbeb"
    TEAL = "#0d9488"
    TEAL_SOFT = "#f0fdfa"

    def _line(x1, y1, x2, y2, stroke=HAIRLINE, sw=1.4, dash=None, marker=None):
        attrs = [
            f'x1="{x1:.1f}"',
            f'y1="{y1:.1f}"',
            f'x2="{x2:.1f}"',
            f'y2="{y2:.1f}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw}"',
        ]
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        return f'<line {" ".join(attrs)}/>'

    def _build_static_force_vs_muscle():
        """SVG 1: Force != Work (W = F·ds = 0) vs why human skeletal muscle burns ATP statically."""
        els = []
        els.extend(
            header(
                "手臂举哑铃累得冒汗，为什么冰箱贴吸在铁门十年却“零耗能”？",
                "物理学第一铁律：有“力”不等于“做功”（W = F · Δs）！真正骗了你直觉的，是人类骨骼肌的特殊设计。",
            )
        )

        # Left Card: Static Forces = Zero Mechanical Work
        els.append(card(20, 68, 360, 408))
        els.append(pill(36, 82, "物理真相：位移 Δs = 0 → 做功 W = 0 焦耳！", fg=GREEN, bg=GREEN_SOFT, w=302, h=22, size=10.8))

        examples = [
            ("① 木桌托住 5 kg 大词典", "桌面弹性形变产生向上支持力 F = 49 N", "词典高度不变 (Δs = 0)，木桌一百年耗能 = 0 J！", BLUE, BLUE_SOFT),
            ("② 钢螺栓夹紧两块钢板", "螺杆预紧拉力高达数吨，死死咬合不松口", "无相对滑动 (Δs = 0)，钢螺栓无需装电池供电！", TEAL, TEAL_SOFT),
            ("③ 地球引力拉住整片海洋", "万有引力时刻把海水拽向地心", "海面不继续下落 (Δs = 0)，地球引力场不掉质量！", PURPLE, PURPLE_SOFT),
            ("④ 永磁冰箱贴吸住铁门", "水平磁吸力 F_mag 引发最大静摩擦力 ≥ mg", "静止悬停 (Δs = 0)，磁场势能一分钱都不用掏！", GREEN, GREEN_SOFT),
        ]
        for idx, (etitle, l1, l2, col, bgc) in enumerate(examples):
            ey = 118 + idx * 72
            els.append(card(36, ey, 328, 62, rx=7, fill=bgc, stroke=col))
            els.append(txt(48, ey + 19, etitle, 10.4, col, weight="700"))
            els.append(txt(48, ey + 37, l1, 9.8, BODY))
            els.append(txt(48, ey + 53, l2, 9.8, INK, weight="700"))

        els.append(txt(36, 424, "💡 费曼一语点醒：把“维持静态力”误当成“消耗能量”，", 10.1, INK, weight="700"))
        els.append(txt(36, 442, "   是人类拿自己的胳膊去揣测无生命世界闹出的最大误会！", 10.0, BODY))
        els.append(txt(36, 460, "   （见《费曼物理学讲义》第 1 卷第 14 章 §14-1）", 9.6, MUTED))

        # Right Card: Why Human Muscle Burns ATP While Holding Still
        els.append(card(396, 68, 344, 408))
        els.append(pill(412, 82, "生理破案：为什么你的胳膊平举重物会酸痛发烫？", fg=RED, bg=RED_SOFT, w=312, h=22, size=10.6))

        # Sarcomere cross-bridge illustration
        sx, sy = 568, 174
        els.append(f'<rect x="416" y="120" width="304" height="108" rx="8" fill="{RED_SOFT}" stroke="{RED}" stroke-width="1.3"/>')
        # Actin thin filaments
        els.append(f'<line x1="432" y1="146" x2="704" y2="146" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>')
        els.append(f'<line x1="432" y1="204" x2="704" y2="204" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>')
        # Myosin thick filament in center with cycling heads
        els.append(f'<rect x="466" y="169" width="204" height="12" rx="5" fill="{RED}"/>')
        for hx in (488, 528, 568, 608, 648):
            els.append(f'<path d="M {hx},169 Q {hx+8},154 {hx+14},148" fill="none" stroke="{RED}" stroke-width="2.6"/>')
            els.append(f'<circle cx="{hx+14}" cy="148" r="3.5" fill="{AMBER}"/>')
            els.append(f'<path d="M {hx},181 Q {hx+8},196 {hx+14},202" fill="none" stroke="{RED}" stroke-width="2.6"/>')
            els.append(f'<circle cx="{hx+14}" cy="202" r="3.5" fill="{AMBER}"/>')
        els.append(txt(568, 137, "肌动蛋白细丝 (Actin) —— 无机械卡扣棘轮！", 9.6, BLUE, weight="700", anchor="middle"))
        els.append(txt(568, 163, "肌球蛋白横桥每秒几十次：抓紧→烧ATP松开→再抓紧→全变废热 Q！", 9.4, RED, weight="700", anchor="middle"))

        els.append(txt(414, 250, "• 人类骨骼肌为了换取“毫秒级收放自如”的敏捷身手，", 10.1, BODY))
        els.append(txt(414, 269, "  演化时放弃了机械锁死卡扣！", 10.1, RED, weight="700"))
        els.append(txt(414, 289, "• 当你平举哑铃纹丝不动时，成百上千亿个肌球蛋白小爪子", 10.0, BODY))
        els.append(txt(414, 307, "  像拔河队员在冰面上小碎步倒手一样，每秒反复【结合—", 10.0, BODY))
        els.append(txt(414, 325, "  水解 ATP—脱开—再结合】数十次！", 10.0, INK, weight="700"))
        els.append(txt(414, 344, "• 注意能量账本：哑铃高度没变，你对哑铃做的机械功依然", 10.0, BODY))
        els.append(txt(414, 362, "  严格等于 0 J；你烧掉的 ATP 100% 变成了肌肉内热 Q！", 10.0, GREEN, weight="700"))

        els.append(card(412, 378, 312, 84, rx=7, fill=AMBER_SOFT, stroke=AMBER))
        els.append(txt(424, 398, "🦪 大自然反例：蛤蜊与扇贝的“闭壳平滑肌 (Catch Muscle)”！", 10.0, AMBER, weight="700"))
        els.append(txt(424, 416, "• 你拿刀撬生蚝或蛤蜊为什么那么费劲？因为贝类演化出了", 9.8, BODY))
        els.append(txt(424, 433, "  twitchin 蛋白分子插销——合拢后直接把横桥“机械上锁”，", 9.8, INK, weight="600"))
        els.append(txt(424, 450, "  几乎不烧 ATP 就能死死夹紧好几天，跟磁铁和螺栓一模一样！", 9.8, BODY))

        return figure(
            494,
            "静态力零做功物理定律与人类骨骼肌横桥耗能假象对比图解",
            "左栏展示木桌托书、螺栓夹紧、地球引力与永磁冰箱贴在位移为零时做功严格为零；右栏剖析人类骨骼肌因缺乏机械锁扣，需每秒数十次循环水解ATP维持张力并全部转化为内热，辅以贝类闭壳锁扣肌反例。",
            els,
        )

    def _build_field_energy_cycle():
        """SVG 2: Animated nail snap powered by external magnetic field energy u_B = B^2/(2 mu_0) + closed loop."""
        # Verify magnetic field energy density at B = 1.2 T: u_B = B^2 / (2 * 4pi * 1e-7) ≈ 572,958 J/m^3
        mu0 = 4.0 * math.pi * 1e-7
        u_b_kjm3 = (1.2 ** 2) / (2.0 * mu0) / 1000.0
        assert 572.0 < u_b_kjm3 < 574.0

        els = []
        els.extend(
            header(
                "磁铁隔空“啪”地把铁钉吸飞过来，这股动能又是从哪儿掏出来的？",
                "答案藏在磁铁周围看不见的空间里：外部磁场本身就是一座高压储能水库（u_B = B² / 2μ₀）！",
            )
        )

        extra_css = """
        @keyframes nailSnap {
          0%, 15% { transform: translateX(0px); }
          55%, 100% { transform: translateX(-118px); }
        }
        @keyframes tankDrop {
          0%, 15% { transform: scaleY(1); }
          55%, 100% { transform: scaleY(0.56); }
        }
        .nail-mover { animation: nailSnap 3.6s cubic-bezier(0.32, 0, 0.15, 1) 1 forwards; }
        .ub-bar { transform-box: fill-box; transform-origin: bottom; animation: tankDrop 3.6s cubic-bezier(0.32, 0, 0.15, 1) 1 forwards; }
        @media (prefers-reduced-motion: reduce) {
          .nail-mover { animation: none !important; transform: translateX(-118px) !important; }
          .ub-bar { animation: none !important; transform: scaleY(0.56) !important; }
        }
        """

        # Top Card: Animated Nail Attraction & Field Energy Drop
        els.append(card(20, 68, 720, 224))
        els.append(step_badge(40, 90, "1", fg=BLUE, bg=BLUE_SOFT, r=10))
        els.append(txt(58, 95, "第一幕（放手吸合动画）：高磁导率铁钉吸拢磁感线，空间总磁场能 U_B 下降买单！", 12.0, INK, weight="700"))

        # Magnet N-S block on left
        mx, my = 62, 148
        els.append(f'<rect x="{mx}" y="{my}" width="84" height="54" rx="5" fill="#2563eb"/>')
        els.append(f'<rect x="{mx+84}" y="{my}" width="84" height="54" rx="5" fill="{RED}"/>')
        els.append(txt(mx + 42, my + 33, "S", 15, "#ffffff", weight="700", anchor="middle"))
        els.append(txt(mx + 126, my + 33, "N", 15, "#ffffff", weight="700", anchor="middle"))

        # Stray flux loops around N pole
        els.append(f'<path d="M 230,158 C 296,112 110,104 72,154" fill="none" stroke="{BLUE_LINE}" stroke-width="1.6" stroke-dasharray="5 3"/>')
        els.append(f'<path d="M 230,192 C 296,238 110,246 72,196" fill="none" stroke="{BLUE_LINE}" stroke-width="1.6" stroke-dasharray="5 3"/>')

        # Ghost initial nail at x = 356 + animated moving nail snapping to x = 238
        els.append(f'<rect x="356" y="168" width="66" height="14" rx="3" fill="none" stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(txt(389, 161, "铁钉初位置", 9.5, MUTED, anchor="middle"))
        els.append(_line(348, 175, 252, 175, stroke=ORANGE, sw=2.0, dash="4 3", marker="arr-orange"))
        els.append(txt(304, 206, "磁吸力做正功 W > 0", 9.8, ORANGE, weight="700", anchor="middle"))

        els.append('<g class="nail-mover">')
        els.append(f'<rect x="356" y="167" width="62" height="16" rx="3" fill="{SLATE}" stroke="{INK}" stroke-width="1.5"/>')
        els.append(f'<polygon points="356,163 356,187 348,175" fill="{INK}"/>')
        els.append(txt(387, 179, "Fe 铁钉", 9.2, "#ffffff", weight="700", anchor="middle"))
        els.append('</g>')

        # Energy Ledger Gauge on Right of Top Card
        gx = 444
        els.append(card(gx, 114, 280, 162, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(gx + 14, 134, f"空间磁场能水库（1.2 T 处高达 {u_b_kjm3:.0f} kJ/m³）", 9.8, BLUE, weight="700"))
        # Initial outline + shrinking bar
        els.append(f'<rect x="{gx+20}" y="150" width="42" height="92" rx="4" fill="#ffffff" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="3 2"/>')
        els.append(f'<rect class="ub-bar" x="{gx+20}" y="150" width="42" height="92" rx="4" fill="{BLUE}"/>')
        els.append(txt(gx + 41, 258, "磁场能 U_B", 9.4, BLUE, weight="700", anchor="middle"))

        # Kinetic -> Heat/Sound bar
        els.append(f'<rect x="{gx+84}" y="190" width="42" height="52" rx="4" fill="{ORANGE}"/>')
        els.append(txt(gx + 105, 258, "动能→声+热", 9.4, ORANGE, weight="700", anchor="middle"))
        els.append(txt(gx + 138, 174, "• 铁磁导率 μ_r 高达上千倍，", 9.4, BODY))
        els.append(txt(gx + 138, 191, "  吸近后收拢外部散乱磁感线，", 9.4, BODY))
        els.append(txt(gx + 138, 208, "  空间总磁场能立降 -ΔU_B，", 9.4, BODY))
        els.append(txt(gx + 138, 225, "  精准转化为铁钉加速动能！", 9.4, INK, weight="700"))

        # Bottom Card: Why Magnet Perpetual Motion Always Fails!
        els.append(card(20, 308, 720, 186))
        els.append(step_badge(40, 330, "2", fg=RED, bg=RED_SOFT, r=10))
        els.append(txt(58, 335, "第二幕（永动机死刑判决）：吸住一次就躺进势能谷底！想再来一次，你的手必须替磁场“充值”", 11.8, INK, weight="700"))

        # Potential well U(x) curve on bottom-left
        px0, px1 = 68.0, 336.0
        py0, py1 = 462.0, 362.0
        els.append(_line(px0, py0, px1, py0, stroke=INK, sw=1.4))
        els.append(_line(px0, py0, px0, py1, stroke=INK, sw=1.4))
        well_pts = []
        for i in range(41):
            t = i / 40.0
            xx = px0 + 18 + t * (px1 - px0 - 26)
            # U(x) rises smoothly from deep well at magnet pole (t=0) toward asymptote (t=1)
            u_norm = 1.0 - 1.0 / (1.0 + 6.5 * t * t)
            yy = py0 - 14 - u_norm * 78.0
            well_pts.append(f"{xx:.1f},{yy:.1f}")
        els.append(f'<polyline points="{" ".join(well_pts)}" fill="none" stroke="{PURPLE}" stroke-width="2.6"/>')
        els.append(f'<circle cx="{px0+18:.1f}" cy="{py0-14:.1f}" r="5.5" fill="{RED}"/>')
        els.append(txt(px0 + 28, py0 - 6, "贴死在 N 极谷底（U_min，再也动不了！）", 9.6, RED, weight="700"))
        els.append(txt(px1 - 6, py1 + 16, "远处高势能 U_0", 9.6, PURPLE, weight="700", anchor="end"))
        els.append(txt(px0 + 150, py0 + 18, "铁钉距磁极距离 x →", 9.5, MUTED, anchor="middle"))

        els.append(card(356, 354, 368, 124, rx=7, fill=AMBER_SOFT, stroke=AMBER))
        els.append(txt(370, 375, "🔄 保守场铁律（∮ F_mag · ds = 0，跟弹簧和石头落地一模一样）：", 10.0, AMBER, weight="700"))
        els.append(txt(370, 395, "• 石头落地砸出响声是引力势能变热能；掉到底还能自己再砸吗？不能！", 9.6, BODY))
        els.append(txt(370, 414, "• 磁铁吸铁钉是一锤子买卖：贴上磁极后，系统跌入最低势能谷底；", 9.6, BODY))
        els.append(txt(370, 433, "• 想吸第二次，必须你出力气硬把铁钉掰开——你手做的机械功", 9.6, INK, weight="700"))
        els.append(txt(370, 452, "  W_手 ≥ +ΔU_B 重新充回空间磁场！网上“磁铁永动机”全藏了电池！", 9.6, RED, weight="700"))

        return figure(
            512,
            "空间磁场能驱动铁钉加速单次动画与保守势能谷底粉碎永动机图解",
            "上栏单次动画展示高磁导率铁钉被磁铁吸近时收拢外部发散磁感线，空间总磁场能U_B下降转化为铁钉动能与撞击声热；下栏绘制磁势能曲线U(x)，说明吸合后系统落入势能谷底，掰开铁钉需人手做功把能量充回磁场。",
            els,
            extra_css=extra_css,
        )

    def _build_quantum_spin_domains():
        """SVG 3: Bohr-van Leeuwen theorem + Quantum spin / Heisenberg exchange + Magnetic domains."""
        els = []
        els.extend(
            header(
                "电磁铁断电就失磁，为什么永磁铁体内没有电池，磁性却永不摩擦停转？",
                "1911 玻尔—范吕文定理惊天判决：经典物理世界里根本不可能存在永磁体！每一块吸铁石都是纯正量子奇迹。",
            )
        )

        # Left Card: Quantum Spin & Heisenberg Exchange (Zero Joule Heat!)
        els.append(card(20, 68, 368, 424))
        els.append(pill(36, 82, "微观真相：电子内禀自旋 + 海森堡交换作用", fg=PURPLE, bg=PURPLE_SOFT, w=302, h=22, size=10.8))

        els.append(card(36, 116, 336, 92, rx=7, fill=RED_SOFT, stroke=RED))
        els.append(txt(48, 136, "❌ 玻尔—范吕文定理（Bohr–van Leeuwen, 1911/1921）：", 10.2, RED, weight="700"))
        els.append(txt(48, 155, "• 如果电子只是绕原子核转圈的经典带电小球，严格统计力学证明：", 9.8, BODY))
        els.append(txt(48, 173, "  任何热平衡固体的宏观磁化强度恒等于 0！而且经典电流只要在", 9.8, BODY))
        els.append(txt(48, 191, "  常温金属晶格里跑，不到一纳秒就会被电阻发热耗光停转！", 9.8, INK, weight="700"))

        els.append(card(36, 218, 336, 146, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(48, 238, "✅ 量子力学亮出两张王牌，实现“零电阻永恒磁矩”：", 10.2, PURPLE, weight="700"))
        els.append(txt(48, 258, "① 电子内禀自旋 (Spin s = 1/2，1 玻尔磁子 μ_B = 9.27×10⁻²⁴ J/T)：", 9.8, INK, weight="700"))
        els.append(txt(48, 276, "   自旋不是小球真在机械自转，而是电子生来就焊死在身上的基态", 9.8, BODY))
        els.append(txt(48, 293, "   量子属性！没有宏观电荷穿过晶格，因此电阻发热 I²R 严格为 0！", 9.8, GREEN, weight="700"))
        els.append(txt(48, 313, "② 海森堡交换相互作用 (Heisenberg 1928)：", 9.8, INK, weight="700"))
        els.append(txt(48, 330, "   泡利不相容原理规定：相邻铁原子 3d 未成对电子若【自旋平行】，", 9.8, BODY))
        els.append(txt(48, 347, "   空间波函数反对称→电子自动离得更远→静电排斥能大幅降低！", 9.8, BODY))

        # Bound surface current equivalent illustration
        els.append(card(36, 374, 336, 102, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(48, 394, "🌀 安培分子环流几何戏法（内部抵消，只剩表面束缚电流 K_m）：", 10.0, BLUE, weight="700"))
        for col_i in range(4):
            cx0 = 76 + col_i * 42
            els.append(f'<circle cx="{cx0}" cy="436" r="15" fill="#ffffff" stroke="{BLUE}" stroke-width="1.6"/>')
            els.append(txt(cx0, 440, "↺", 13, BLUE, weight="700", anchor="middle"))
        els.append(txt(236, 424, "相邻晶格内部一上一下刚好抵消；", 9.6, BODY))
        els.append(txt(236, 442, "外表面等效于一圈永不耗能的", 9.6, BODY))
        els.append(txt(236, 460, "量子束缚面电流 K_m = M × n̂！", 9.6, INK, weight="700"))

        # Right Card: Why Plain Iron Nail Isn't a Magnet -> Magnetic Domains!
        els.append(card(404, 68, 336, 424))
        els.append(pill(420, 82, "中观破案：普通铁钉也有铁原子，为何平时不吸铁？", fg=TEAL, bg=TEAL_SOFT, w=304, h=22, size=10.6))

        # Top domain box: Unmagnetized multi-domain iron
        els.append(txt(420, 122, "状态 A：普通退火铁钉 —— 分裂成上百万个小【磁畴】互抵消", 10.1, INK, weight="700"))
        els.append(f'<rect x="420" y="132" width="304" height="96" rx="6" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.6"/>')
        # Polygonal domain walls
        els.append(_line(510, 132, 492, 228, stroke=INK, sw=1.6))
        els.append(_line(616, 132, 634, 228, stroke=INK, sw=1.6))
        els.append(_line(420, 180, 724, 180, stroke=INK, sw=1.6))
        dom_arrows = [
            (462, 160, "→", BLUE), (562, 160, "↑", ORANGE), (672, 160, "←", RED),
            (458, 208, "↓", GREEN), (566, 208, "←", PURPLE), (676, 208, "↗", TEAL),
        ]
        for dx, dy, sym, col in dom_arrows:
            els.append(txt(dx, dy, sym, 16, col, weight="700", anchor="middle"))
        els.append(txt(572, 246, "每个微米级磁畴内部早已 100% 磁化！但各畴方向乱指，对外净磁矩 = 0", 9.5, MUTED, anchor="middle"))

        # Bottom domain box: Saturated aligned permanent magnet
        els.append(txt(420, 274, "状态 B：充磁后的永磁体 —— 各磁畴统一立正朝右（M 饱和锁定）！", 10.1, GREEN, weight="700"))
        els.append(f'<rect x="420" y="284" width="304" height="84" rx="6" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2.0"/>')
        for r_i in range(2):
            for c_i in range(5):
                ax = 454 + c_i * 58
                ay = 314 + r_i * 34
                els.append(txt(ax, ay, "➔", 15, GREEN, weight="700", anchor="middle"))

        els.append(card(420, 382, 304, 94, rx=7, fill=TEAL_SOFT, stroke=TEAL))
        els.append(txt(432, 402, "🧩 为什么要分成磁畴？（又是为了省外部磁场能！）", 10.1, TEAL, weight="700"))
        els.append(txt(432, 421, "• 如果整根大铁棒合成一个巨型磁畴，周围空间就得撑起庞大的外部", 9.8, BODY))
        els.append(txt(432, 438, "  磁场能 U_B；切成尺寸 >10 μm 的反向小磁畴让磁感线在体内闭环，", 9.8, BODY))
        els.append(txt(432, 455, "  总能量最低！所以普通铁块“身怀绝技却深藏不露”。", 9.8, INK, weight="600"))

        return figure(
            510,
            "玻尔范吕文定理、电子量子自旋海森堡交换与铁磁磁畴结构图解",
            "左栏说明经典物理无法产生永磁性，永磁体源于零电阻损耗的电子内禀自旋与海森堡交换作用；右栏对比普通铁钉内部互相抵消的多磁畴结构与永磁体内部整齐同向锁定的磁畴阵列。",
            els,
        )

    def _build_pulse_charging_hysteresis():
        """SVG 4: Factory pulse magnetizer + Soft iron vs Nd2Fe14B hysteresis loop."""
        els = []
        els.extend(
            header(
                "磁铁那口“原始磁场能”是谁充进去的？钕铁硼凭什么当上现代磁王？",
                "出厂前经历一次毫秒级“雷霆脉冲充磁”，再靠极高矫顽力晶格高墙把磁畴死死钉在岗位上！",
            )
        )

        # Left Card: Factory Capacitor-Bank Pulse Magnetizer
        els.append(card(20, 68, 344, 408))
        els.append(pill(36, 82, "出厂关键工序：高压电容脉冲充磁机", fg=ORANGE, bg=ORANGE_SOFT, w=268, h=22, size=11.0))

        # Schematic of capacitor bank -> thyristor switch -> copper coil around NdFeB blank
        els.append(f'<rect x="44" y="126" width="88" height="72" rx="6" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.8"/>')
        els.append(txt(88, 152, "高压电容组", 10.2, ORANGE, weight="700", anchor="middle"))
        els.append(txt(88, 170, "2000–3000 V", 9.8, INK, weight="700", anchor="middle", cls="mono"))
        els.append(txt(88, 187, "储存数万焦耳", 9.4, MUTED, anchor="middle"))

        els.append(_line(132, 162, 198, 162, stroke=RED, sw=2.4, marker="arr-orange"))
        els.append(txt(165, 152, "万安培脉冲", 9.4, RED, weight="700", anchor="middle"))
        els.append(txt(165, 178, "(几毫秒放电)", 9.2, MUTED, anchor="middle"))

        # Solenoid coil + NdFeB core
        els.append(f'<rect x="204" y="122" width="136" height="80" rx="8" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(f'<rect x="232" y="144" width="80" height="36" rx="4" fill="{PURPLE}" stroke="{INK}" stroke-width="1.5"/>')
        els.append(txt(272, 166, "Nd₂Fe₁₄B", 10.0, "#ffffff", weight="700", anchor="middle", cls="mono"))
        for cx0 in range(218, 332, 18):
            els.append(f'<path d="M {cx0},122 Q {cx0+6},162 {cx0},202" fill="none" stroke="{ORANGE}" stroke-width="2.0"/>')
        els.append(txt(272, 218, "螺线管瞬间爆发 2–3 特斯拉强磁场！", 9.8, BLUE, weight="700", anchor="middle"))

        els.append(card(36, 236, 312, 222, rx=7, fill=SLATE_SOFT, stroke=SLATE))
        els.append(txt(48, 258, "⚡ 算清磁铁一辈子的能量总账：", 10.4, INK, weight="700"))
        els.append(txt(48, 279, "① 刚从烧结炉出来的钕铁硼毛坯其实是【完全没磁性】的！", 9.9, BODY))
        els.append(txt(48, 298, "② 脉冲充磁机电网耗电充进电容，毫秒间轰出 >2.5 T 巨浪，", 9.9, BODY))
        els.append(txt(48, 316, "   强行推平磁畴壁、把所有电子自旋拧向同一个易磁化轴，", 9.9, BODY))
        els.append(txt(48, 334, "   同时替这块磁铁在周围空间建起了那座【外部磁场储能水库】！", 9.9, ORANGE, weight="700"))
        els.append(txt(48, 356, "🏆 1984 佐川真人发现“现代磁王”钕铁硼 (Nd₂Fe₁₄B)：", 10.2, PURPLE, weight="700"))
        els.append(txt(48, 375, "• 稀土钕原子(Nd)提供极陡的磁晶各向异性势垒（防退磁高墙），", 9.8, BODY))
        els.append(txt(48, 392, "  14 颗铁原子(Fe)提供超高饱和磁矩，硼原子(B)锁紧四方晶格；", 9.8, BODY))
        els.append(txt(48, 410, "• 最大磁能积 (BH)_max 实验室纪录高达 474 kJ/m³ (59.5 MGOe)，", 9.8, GREEN, weight="700"))
        els.append(txt(48, 428, "  指甲盖大一块就能轻松吊起自身重量几百倍的大铁砣，直接促成", 9.8, BODY))
        els.append(txt(48, 445, "  新能源汽车驱动电机、风力发电机、耳机与硬盘音圈小型化革命！", 9.8, INK, weight="600"))

        # Right Card: Hysteresis Loop Comparison (Hard NdFeB vs Soft Iron)
        els.append(card(380, 68, 360, 408))
        els.append(pill(396, 82, "硬磁 vs 软磁：一张“磁滞回线”看懂为何不退磁", fg=PURPLE, bg=PURPLE_SOFT, w=316, h=22, size=10.8))

        ox, oy = 560.0, 224.0
        # Axes H (horizontal) & M / J (vertical)
        els.append(_line(408, oy, 712, oy, stroke=INK, sw=1.4, marker="arr-muted"))
        els.append(_line(ox, 336, ox, 118, stroke=INK, sw=1.4, marker="arr-muted"))
        els.append(txt(712, oy - 6, "外磁场 H", 9.6, INK, weight="700", anchor="end"))
        els.append(txt(ox + 8, 126, "磁化强度 J", 9.6, INK, weight="700"))

        # Wide fat loop for Nd2Fe14B (Hard magnet)
        pts_hard = []
        for deg in range(0, 361, 6):
            rad = math.radians(deg)
            # Parametric fat hysteresis loop using tanh-like shaping
            h_val = 112.0 * math.cos(rad)
            j_val = 84.0 * math.tanh(2.4 * math.sin(rad) + 1.3 * math.cos(rad - math.pi / 2))
            # Cleaner exact hysteresis formula: H = H_m cos(t), J = J_s tanh(2.5*(H_m cos(t) +/- H_c)/H_c)
            pts_hard.append((deg, rad))

        upper_hard = []
        lower_hard = []
        upper_soft = []
        lower_soft = []
        for i in range(41):
            h = -1.0 + 2.0 * (i / 40.0)
            hx = ox + h * 124.0
            # Hard magnet: H_c = 0.62
            ju_h = math.tanh(4.2 * (h + 0.62))
            jl_h = math.tanh(4.2 * (h - 0.62))
            upper_hard.append(f"{hx:.1f},{oy - ju_h * 84.0:.1f}")
            lower_hard.append(f"{hx:.1f},{oy - jl_h * 84.0:.1f}")
            # Soft iron: H_c = 0.05
            ju_s = math.tanh(14.0 * (h + 0.045))
            jl_s = math.tanh(14.0 * (h - 0.045))
            upper_soft.append(f"{hx:.1f},{oy - ju_s * 88.0:.1f}")
            lower_soft.append(f"{hx:.1f},{oy - jl_s * 88.0:.1f}")

        hard_poly = " ".join(upper_hard + list(reversed(lower_hard)))
        soft_poly = " ".join(upper_soft + list(reversed(lower_soft)))
        els.append(f'<polygon points="{hard_poly}" fill="{PURPLE_SOFT}" fill-opacity="0.55" stroke="{PURPLE}" stroke-width="2.5"/>')
        els.append(f'<polygon points="{soft_poly}" fill="none" stroke="{TEAL}" stroke-width="2.0" stroke-dasharray="5 3"/>')

        # Key points: Remanence B_r (H=0, top) and Coercivity -H_cJ (J=0, left)
        br_y = oy - math.tanh(4.2 * 0.62) * 84.0
        hc_x = ox - 0.62 * 124.0
        els.append(f'<circle cx="{ox:.1f}" cy="{br_y:.1f}" r="4.8" fill="{PURPLE}"/>')
        els.append(txt(ox + 8, br_y - 4, "剩磁 B_r (~1.4 T，撤掉外场依然满格！)", 9.5, PURPLE, weight="700"))
        els.append(f'<circle cx="{hc_x:.1f}" cy="{oy:.1f}" r="4.8" fill="{RED}"/>')
        els.append(txt(hc_x - 4, oy + 18, "-H_cJ 矫顽力", 9.5, RED, weight="700", anchor="middle"))

        els.append(txt(646, 176, "紫宽框：钕铁硼硬磁", 9.6, PURPLE, weight="700"))
        els.append(txt(638, 286, "绿窄虚线：纯铁软磁", 9.6, TEAL, weight="700"))

        els.append(card(396, 348, 328, 112, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(408, 369, "• 软磁（纯铁钉/硅钢片）：磁滞回线窄如细针，矫顽力极小——外场", 9.8, BODY))
        els.append(txt(408, 387, "  一撤磁畴立刻散架归零（最适合做电磁铁与变压器铁芯）！", 9.8, TEAL, weight="700"))
        els.append(txt(408, 406, "• 硬磁 / 永磁（钕铁硼/钐钴/铁氧体）：回线宽胖如堡垒！撤去充磁", 9.8, BODY))
        els.append(txt(408, 424, "  外场 (H=0) 后稳坐高剩磁 B_r，除非遭遇超强反向磁场 (-H_cJ) 或", 9.8, BODY))
        els.append(txt(408, 442, "  高温，否则被势垒牢牢锁在亚稳态里几十年不掉电！", 9.8, INK, weight="700"))

        return figure(
            494,
            "高压电容脉冲充磁机原理与钕铁硼硬磁对纯铁软磁磁滞回线对比图解",
            "左栏展示烧结钕铁硼毛坯经高压电容脉冲螺线管施加2至3特斯拉强磁场一次性充磁并注入外部磁场能；右栏精确绘制宽胖的钕铁硼硬磁磁滞回线（高剩磁Br与高矫顽力HcJ）与纤细的纯铁软磁回线对比。",
            els,
        )

    def _build_curie_demagnetization():
        """SVG 5: Curie temperature M_s(T) curves & real causes of magnet death."""
        els = []
        els.extend(
            header(
                "“永磁铁”真的永恒不灭吗？一把火烧过“居里温度”，磁王当场变废铁！",
                "吊重物绝不会耗光磁性；真正能杀死永磁体的，是高温热运动、反向强磁场与剧烈敲击。",
            )
        )

        # Left Card: Quantitative M_s(T)/M_0 vs Temperature T (°C)
        els.append(card(20, 68, 412, 398))
        els.append(pill(36, 82, "三大磁性材料自发磁化曲线与居里温度 T_C", fg=RED, bg=RED_SOFT, w=308, h=22, size=10.8))

        gx0, gx1 = 68.0, 404.0
        gy0, gy1 = 316.0, 134.0
        els.append(_line(gx0, gy0, gx1, gy0, stroke=INK, sw=1.4))
        els.append(_line(gx0, gy0, gx0, gy1, stroke=INK, sw=1.4))

        # Plot M(T)/M(0) ≈ (1 - T_K / T_C_K)^0.36 from 0 °C to 1200 °C
        materials = [
            ("钕铁硼 Nd₂Fe₁₄B", 312.0, PURPLE, 2.6, None),
            ("纯铁 Fe", 770.0, BLUE, 2.3, None),
            ("金属钴 Co", 1115.0, TEAL, 2.1, "5 3"),
        ]
        for mname, tc_c, col, sw, dash in materials:
            tc_k = tc_c + 273.15
            pts = []
            for c_temp in range(0, int(tc_c) + 1, 8):
                tk = c_temp + 273.15
                ratio = max(0.0, (1.0 - tk / tc_k) ** 0.36) / ((1.0 - 273.15 / tc_k) ** 0.36)
                px = gx0 + (c_temp / 1200.0) * (gx1 - gx0)
                py = gy0 - ratio * (gy0 - gy1 - 12)
                pts.append(f"{px:.1f},{py:.1f}")
            px_end = gx0 + (tc_c / 1200.0) * (gx1 - gx0)
            pts.append(f"{px_end:.1f},{gy0:.1f}")
            d_attr = f' stroke-dasharray="{dash}"' if dash else ""
            els.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{sw}"{d_attr}/>')
            els.append(f'<circle cx="{px_end:.1f}" cy="{gy0:.1f}" r="4.5" fill="{col}"/>')

        # Ticks on temperature axis
        for c_tick in (0, 312, 600, 770, 1115):
            tx = gx0 + (c_tick / 1200.0) * (gx1 - gx0)
            els.append(_line(tx, gy0, tx, gy0 + 5, stroke=INK, sw=1.2))
            els.append(txt(tx, gy0 + 18, f"{c_tick}°C", 9.2, INK if c_tick in (312, 770, 1115) else MUTED, weight="700" if c_tick in (312, 770, 1115) else None, anchor="middle"))

        els.append(txt(122, 226, "Nd₂Fe₁₄B (T_C=312°C)", 9.5, PURPLE, weight="700"))
        els.append(txt(222, 186, "铁 Fe (T_C=770°C)", 9.5, BLUE, weight="700"))
        els.append(txt(306, 152, "钴 Co (T_C=1115°C)", 9.5, TEAL, weight="700"))
        els.append(txt(gx0 - 8, gy1 + 12, "100%", 9.2, MUTED, anchor="end"))
        els.append(txt(gx0 - 8, gy0 + 3, "0%", 9.2, MUTED, anchor="end"))

        els.append(card(36, 348, 380, 102, rx=7, fill=RED_SOFT, stroke=RED))
        els.append(txt(48, 369, "🔥 1895 皮埃尔·居里发现的临界相变（居里点 T_C）：", 10.2, RED, weight="700"))
        els.append(txt(48, 388, "• 一旦加热跨过 T_C，晶格热振动能量 k_B T 彻底压倒海森堡交换锁扣，", 9.8, BODY))
        els.append(txt(48, 405, "  整齐列队的电子自旋瞬间乱成一团散沙（铁磁态相变为顺磁态）！", 9.8, BODY))
        els.append(txt(48, 423, "• 生活警告：普通 N 牌号钕铁硼磁铁只要用打火机烤或泡进 >80°C 开水，", 9.8, INK, weight="700"))
        els.append(txt(48, 440, "  就会发生不可逆退磁，凉下来也再变不回磁铁了（除非重进充磁机）！", 9.8, RED, weight="700"))

        # Right Card: Three Real Demagnetization Killers vs One Myth
        els.append(card(448, 68, 292, 398))
        els.append(pill(464, 82, "永磁体日常保养与真假退磁榜", fg=AMBER, bg=AMBER_SOFT, w=244, h=22, size=11.0))

        items = [
            ("✅ 辟谣：一直吸重物会吸没劲吗？", "绝不会！静力不做功，吸在铁板上反而帮磁感线形成闭合磁路（古人称“衔铁护磁”），比裸放空气中更不易退磁！", GREEN, GREEN_SOFT),
            ("⚠️ 杀手 1：高温烘烤（头号天敌）", "钕铁硼怕热（常规耐温 80–150°C），电机过载发烫极易退磁；高温航天场景需改用钐钴磁铁（T_C 高达 700–800°C）。", RED, RED_SOFT),
            ("⚠️ 杀手 2：强反向磁场与乱撞敲击", "两块强磁同名极硬怼或拿铁锤猛砸古旧铝镍钴磁钢，剧烈震动会帮磁畴壁翻越势垒滑回混乱抵消态。", ORANGE, ORANGE_SOFT),
            ("⏳ 杀手 3：极其缓慢的热蠕变", "常温下极少数磁畴靠热涨落越过势垒，呈对数规律微弱衰减：现代优质钕铁硼在室温放 30 年磁通损失不到 1%–3%！", SLATE, SLATE_SOFT),
        ]
        for idx, (ititle, idesc, col, bgc) in enumerate(items):
            iy = 118 + idx * 84
            els.append(card(464, iy, 260, 74, rx=7, fill=bgc, stroke=col))
            els.append(txt(474, iy + 18, ititle, 9.9, col, weight="700"))
            # Wrap idesc cleanly into 3 lines (~18 chars each)
            line1 = idesc[:19]
            line2 = idesc[19:38]
            line3 = idesc[38:]
            els.append(txt(474, iy + 36, line1, 9.4, BODY))
            els.append(txt(474, iy + 51, line2, 9.4, BODY))
            els.append(txt(474, iy + 66, line3, 9.4, INK, weight="600"))

        return figure(
            484,
            "铁磁材料居里温度退磁相变曲线与永磁体三大真实退磁原因图解",
            "左栏绘制钕铁硼（312°C）、纯铁（770°C）与钴（1115°C）随温度升高的自发磁化衰减曲线；右栏辟谣“吸重物耗尽磁力”误区，并列出高温、反向磁场敲击与长期热涨落蠕变三大真实退磁机制。",
            els,
        )

    @register(
        "permanent-magnet-energy",
        "永磁体与能量守恒五步图解：静力零做功vs肌肉耗ATP、磁场储能吸铁钉动画与保守闭环、玻尔范吕文定理与量子自旋磁畴、脉冲充磁磁滞回线及居里温度退磁",
        "mechanics_sky",
    )
    def build_permanent_magnet_energy():
        write_svg(SUBDIR, "static-force-zero-work-vs-muscle-atp.svg", _build_static_force_vs_muscle())
        write_svg(SUBDIR, "magnetic-field-energy-nail-snap-cycle.svg", _build_field_energy_cycle())
        write_svg(SUBDIR, "bohr-van-leeuwen-and-quantum-spin-domains.svg", _build_quantum_spin_domains())
        write_svg(SUBDIR, "neodymium-pulse-charging-and-hysteresis.svg", _build_pulse_charging_hysteresis())
        write_svg(SUBDIR, "curie-temperature-and-demagnetization.svg", _build_curie_demagnetization())


_register_permanent_magnet_energy()


def _register_cosmic_scale():
    SUBDIR = "cosmic-scale"
    RED = "#dc2626"
    RED_SOFT = "#fef2f2"
    AMBER = "#d97706"
    AMBER_SOFT = "#fffbeb"
    TEAL = "#0d9488"
    TEAL_SOFT = "#f0fdfa"

    # Physical & cosmological constants (IAU 2012/2015, NASA NSSDCA, Planck 2018 VI)
    AU_KM = 149_597_870.7
    C_KMS = 299_792.458
    JULIAN_YR_S = 365.25 * 86400.0
    LY_KM = C_KMS * JULIAN_YR_S  # 9.4607304725808e12 km
    PC_AU = 648_000.0 / math.pi  # 206264.806247... AU
    PC_LY = (PC_AU * AU_KM) / LY_KM  # 3.261563777... ly
    assert 206_264.8 < PC_AU < 206_264.9
    assert 3.2615 < PC_LY < 3.2616

    def _build_basketball_sun_and_gap():
        """SVG 1: Basketball Sun scale model (1 : 5.7975e9) + 7 planets inside Earth-Moon apogee gap."""
        d_sun_km = 1_391_400.0  # IAU 2015 nominal 2 * 695,700 km
        scale = d_sun_km / 0.00024  # 0.24 m basketball => 5.7975e9
        earth_mm = (12_756.0 / scale) * 1e6  # 2.20 mm
        earth_dist_m = (AU_KM / scale) * 1e3  # 25.80 m
        moon_mm = (3_475.0 / scale) * 1e6  # 0.60 mm
        moon_gap_cm = (384_400.0 / scale) * 1e5  # 6.63 cm
        jup_mm = (142_984.0 / scale) * 1e6  # 24.66 mm
        jup_dist_m = (778_500_000.0 / scale) * 1e3  # 134.28 m
        nep_mm = (49_528.0 / scale) * 1e6  # 8.54 mm
        nep_dist_m = (4_515_000_000.0 / scale) * 1e3  # 778.78 m
        prox_km = (4.2465 * LY_KM) / scale  # 6,931 km
        assert 2.15 < earth_mm < 2.25 and 25.5 < earth_dist_m < 26.1 and 0.55 < moon_mm < 0.65
        assert 6_900.0 < prox_km < 6_960.0

        # NASA NSSDCA equatorial diameters (km)
        planets_7 = [
            ("水星", 4_879, "#94a3b8"),
            ("金星", 12_104, "#f59e0b"),
            ("火星", 6_792, "#ef4444"),
            ("木星", 142_984, "#d97706"),
            ("土星", 120_536, "#eab308"),
            ("天王星", 51_118, "#06b6d4"),
            ("海王星", 49_528, "#3b82f6"),
        ]
        sum_eq_km = sum(p[1] for p in planets_7)  # 387,941 km
        apogee_gap_km = 405_500.0 - (6_378.1 + 1_738.1)  # 397,383.8 km
        mean_gap_km = 384_400.0 - (6_378.1 + 1_738.1)  # 376,283.8 km
        assert sum_eq_km == 387_941
        assert mean_gap_km < sum_eq_km < apogee_gap_km

        els = []
        els.extend(
            header(
                "一、教科书不敢按真实比例印的太阳系：宇宙到底有多“空”？",
                "把直径 139 万公里的太阳缩成 24 cm 标准篮球（缩小 58 亿倍），最近恒星竟远在 6,931 公里之外",
            )
        )

        # Panel A: Basketball Sun Scale Model
        els.append(card(20, 64, 720, 206))
        els.append(pill(34, 74, "A · 1 : 58 亿“篮球太阳”微缩模型（非线性断轴示意真实跨度）", fg=ORANGE, bg=ORANGE_SOFT, w=416))

        y_tr = 152.0
        els.append(f'<line x1="62" y1="{y_tr}" x2="528" y2="{y_tr}" stroke="{SLATE}" stroke-width="1.6"/>')
        els.append(f'<path d="M 532,{y_tr - 9} L 540,{y_tr + 9} M 542,{y_tr - 9} L 550,{y_tr + 9}" stroke="{RED}" stroke-width="1.8" fill="none"/>')
        els.append(f'<line x1="554" y1="{y_tr}" x2="692" y2="{y_tr}" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 3"/>')

        # 1. Basketball Sun at x=68
        els.append('<circle cx="68" cy="152" r="24" fill="#fb923c" stroke="#c2410c" stroke-width="2"/>')
        els.append(txt(68, 156, "太阳", 10.8, "#ffffff", anchor="middle", weight="700"))
        els.append(txt(68, 194, "篮球 Ø 24 cm", 10.8, ORANGE, anchor="middle", weight="700"))
        els.append(txt(68, 212, "起点 0 m", 10.2, MUTED, anchor="middle"))

        # 2. Earth + Moon at x=196
        els.append(f'<circle cx="196" cy="{y_tr}" r="3.2" fill="{BLUE}"/>')
        els.append(f'<circle cx="206" cy="{y_tr - 6}" r="1.6" fill="{SLATE}"/>')
        els.append(txt(196, 124, "地球 Ø 2.2 mm (芝麻)", 10.6, BLUE, anchor="middle", weight="700"))
        els.append(txt(196, 194, f"距球 {earth_dist_m:.1f} m (整座球场)", 10.4, INK, anchor="middle", weight="600"))
        els.append(txt(196, 212, f"月球微尘仅隔 {moon_gap_cm:.1f} cm", 10.0, MUTED, anchor="middle"))

        # 3. Jupiter at x=344
        els.append(f'<circle cx="344" cy="{y_tr}" r="7.5" fill="#d97706" stroke="#92400e" stroke-width="1.3"/>')
        els.append(txt(344, 124, f"木星 Ø {jup_mm / 10:.2f} cm (弹珠)", 10.6, AMBER, anchor="middle", weight="700"))
        els.append(txt(344, 194, f"距球 {jup_dist_m:.0f} m", 10.4, INK, anchor="middle", weight="600"))
        els.append(txt(344, 212, "5.20 AU · 操场对岸", 10.0, MUTED, anchor="middle"))

        # 4. Neptune at x=478
        els.append(f'<circle cx="478" cy="{y_tr}" r="4.5" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.2"/>')
        els.append(txt(478, 124, f"海王星 Ø {nep_mm:.1f} mm (豌豆)", 10.6, BLUE, anchor="middle", weight="700"))
        els.append(txt(478, 194, f"距球 {nep_dist_m:.0f} m", 10.4, INK, anchor="middle", weight="600"))
        els.append(txt(478, 212, "30.18 AU · 八大行星尽头", 10.0, MUTED, anchor="middle"))

        # 5. Proxima Centauri at x=654
        els.append(f'<circle cx="654" cy="{y_tr}" r="6.2" fill="{RED}" stroke="#991b1b" stroke-width="1.4"/>')
        els.append(txt(654, 124, "比邻星 Ø 3.7 cm (红枣)", 10.6, RED, anchor="middle", weight="700"))
        els.append(txt(654, 194, f"距球 {prox_km:,.0f} km！", 10.8, RED, anchor="middle", weight="700"))
        els.append(txt(654, 212, "4.25 光年 · 北京到莫斯科", 10.0, INK, anchor="middle", weight="600"))

        els.append(card(34, 226, 692, 32, rx=6, fill="#f8fafc", stroke=BORDER))
        els.append(
            txt(
                380,
                247,
                "推论：恒星间距 ≈ 恒星直径的 3,000 万倍！45 亿年后银河系与仙女座相撞，数千亿颗恒星彼此几乎“零碰撞”穿堂而过。",
                10.6,
                INK,
                anchor="middle",
                weight="600",
            )
        )

        # Panel B: True-Scale Earth-Moon Apogee Gap Fitting All 7 Other Planets
        els.append(card(20, 282, 720, 290))
        els.append(pill(34, 292, "B · 严格 1 : 1 真实直径比例：地月远地点净空竟能横塞下其余七大行星！", fg=BLUE, bg=BLUE_SOFT, w=472))

        x0 = 86.0
        px_per_km = 580.0 / 405_500.0
        y_cy = 432.0

        x_mean_moon = x0 + 384_400.0 * px_per_km
        x_apo_moon = x0 + 405_500.0 * px_per_km
        r_moon_px = max(2.5, 1_738.1 * px_per_km)
        els.append(f'<line x1="{x_mean_moon:.2f}" y1="326" x2="{x_mean_moon:.2f}" y2="538" stroke="{MUTED}" stroke-width="1.1" stroke-dasharray="4 3"/>')
        els.append(txt(x_mean_moon - 5, 336, "平均月距 38.44万km", 9.8, MUTED, anchor="end"))

        r_earth_px = 6_378.1 * px_per_km
        els.append(f'<circle cx="{x0:.2f}" cy="{y_cy}" r="{r_earth_px:.2f}" fill="#2563eb" stroke="#1e3a8a" stroke-width="1.4"/>')
        els.append(txt(x0 - 15, y_cy + 4, "地球", 10.8, BLUE, anchor="end", weight="700"))

        cur_km = 6_378.1
        # Mode: ("callout", dy, dx_text, anchor) or ("inside_big",) or ("inside_med",)
        label_modes = [
            ("callout", -24, -6, "end"),
            ("callout", -46, -3, "end"),
            ("callout", -68, 0, "middle"),
            ("inside_big",),
            ("inside_big",),
            ("inside_med",),
            ("inside_med",),
        ]
        for (pname, pdiam, pcol), lmode in zip(planets_7, label_modes):
            pr_km = pdiam * 0.5
            pcx = x0 + (cur_km + pr_km) * px_per_km
            pr_px = max(1.8, pr_km * px_per_km)
            els.append(f'<circle cx="{pcx:.2f}" cy="{y_cy}" r="{pr_px:.2f}" fill="{pcol}" fill-opacity="0.88" stroke="#1e293b" stroke-width="0.9"/>')
            if lmode[0] == "inside_big":
                els.append(txt(pcx, y_cy - 3, pname, 11.4, "#ffffff", anchor="middle", weight="700"))
                els.append(txt(pcx, y_cy + 15, f"{pdiam:,} km", 9.8, "#ffffff", anchor="middle", weight="600"))
            elif lmode[0] == "inside_med":
                els.append(txt(pcx, y_cy + 4, pname, 10.2, "#ffffff", anchor="middle", weight="700"))
            else:
                _, dy_lbl, dx_lbl, lanc = lmode
                ly = y_cy + dy_lbl
                els.append(f'<line x1="{pcx:.1f}" y1="{y_cy - pr_px - 1:.1f}" x2="{pcx + dx_lbl:.1f}" y2="{ly + 4:.1f}" stroke="{HAIRLINE}" stroke-width="0.9"/>')
                els.append(txt(pcx + dx_lbl, ly, pname, 9.8, INK, anchor=lanc, weight="700"))
            cur_km += pdiam

        els.append(f'<circle cx="{x_apo_moon:.2f}" cy="{y_cy}" r="{r_moon_px:.2f}" fill="#64748b" stroke="#0f172a" stroke-width="1.2"/>')
        els.append(txt(x_apo_moon + 8, y_cy + 4, "远地点月球", 10.6, INK, weight="700"))

        x_surf_e = x0 + 6_378.1 * px_per_km
        x_end_7 = x0 + cur_km * px_per_km
        x_surf_m = x0 + (405_500.0 - 1_738.1) * px_per_km
        els.append(f'<line x1="{x_surf_e:.1f}" y1="544" x2="{x_end_7:.1f}" y2="544" stroke="{ORANGE}" stroke-width="2.0"/>')
        els.append(f'<line x1="{x_end_7:.1f}" y1="544" x2="{x_surf_m:.1f}" y2="544" stroke="{GREEN}" stroke-width="2.6"/>')
        els.append(
            txt(
                380,
                563,
                f"七大行星赤道直径总和 = {sum_eq_km:,} km（体积均径总和 380,010 km）；远地点地月净空 = 397,384 km，塞完还富余 9,443 km！",
                10.2,
                INK,
                anchor="middle",
                weight="600",
            )
        )

        return figure(
            586,
            "1比58亿篮球太阳微缩模型与地月远地点净空横排塞入其余七大行星真实比例图解",
            "上图将太阳缩为24厘米篮球，展示地球仅2.2毫米位于25.8米外，而最近恒星比邻星远在6931公里外；下图按1比1真实直径比例证明地月远地点表面净空397384公里足以并排容纳其余七大行星（赤道直径总和387941公里）。",
            els,
        )

    def _build_distance_ladder():
        """SVG 2: 4-rung Cosmic Distance Ladder overlap chart + Parsec & Cepheid Period-Luminosity panels."""
        els = []
        els.extend(
            header(
                "二、连太阳系都没飞出去，人类凭什么量准百亿光年？——四级“宇宙量天尺”",
                "没有一把尺子能量遍全宇宙：靠相邻两级在“重叠区”互相校准，把 1 AU 的精度一路接力传到宇宙边缘",
            )
        )

        els.append(card(20, 64, 720, 212))
        els.append(pill(34, 74, "A · 四级测距接力棒与三大重叠校准带（横轴 log₁₀ 距离 / 光年）", fg=BLUE, bg=BLUE_SOFT, w=416))

        lx0, lx1 = 156.0, 716.0
        lmin, lmax = -6.0, 11.0

        def map_lx(lg_ly):
            return lx0 + (lg_ly - lmin) / (lmax - lmin) * (lx1 - lx0)

        y_ax = 244.0
        els.append(f'<line x1="{lx0}" y1="{y_ax}" x2="{lx1}" y2="{y_ax}" stroke="{SLATE}" stroke-width="1.3"/>')
        ticks = [
            (-4.80, "1 AU"),
            (0.0, "1 ly"),
            (2.0, "100 ly"),
            (4.5, "3万 ly"),
            (6.4, "M31"),
            (8.0, "1亿 ly"),
            (10.67, "465亿 ly"),
        ]
        for lgv, tlbl in ticks:
            tx = map_lx(lgv)
            els.append(f'<line x1="{tx:.1f}" y1="108" x2="{tx:.1f}" y2="{y_ax + 4}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="3 3"/>')
            els.append(txt(tx, y_ax + 18, tlbl, 9.8, MUTED, anchor="middle"))

        overlaps = [
            (-4.80, -3.5, "#fef3c7"),
            (2.2, 4.3, "#dcfce7"),
            (6.2, 7.9, "#f3e8ff"),
        ]
        for oa, ob, ocol in overlaps:
            ox0, ox1 = map_lx(oa), map_lx(ob)
            els.append(f'<rect x="{ox0:.1f}" y="106" width="{ox1 - ox0:.1f}" height="134" fill="{ocol}" fill-opacity="0.65"/>')

        rungs = [
            ("① 行星雷达回波", -5.6, -3.4, TEAL, TEAL_SOFT, "金星雷达光速计时，锁死 1 AU 精确米数"),
            ("② 几何三角视差", 0.6, 4.5, BLUE, BLUE_SOFT, "地球 2 AU 轨道基线 · Gaia 测绘 20 亿颗恒星"),
            ("③ 造父变星烛光", 2.2, 8.0, ORANGE, ORANGE_SOFT, "勒维特周光关系 · 哈勃测出仙女座"),
            ("④ Ia超新星+红移", 6.2, 10.67, PURPLE, PURPLE_SOFT, "Ia标准烛光 + BAO声学尺"),
        ]
        for idx, (rname, ra, rb, rfg, rbg, rnote) in enumerate(rungs):
            ry = 112 + idx * 32
            rx_a, rx_b = map_lx(ra), map_lx(rb)
            els.append(txt(148, ry + 15, rname, 10.8, rfg, anchor="end", weight="700"))
            els.append(f'<rect x="{rx_a:.1f}" y="{ry}" width="{rx_b - rx_a:.1f}" height="22" rx="6" fill="{rbg}" stroke="{rfg}" stroke-width="1.4"/>')
            if idx < 2:
                els.append(txt(rx_b + 8, ry + 15, rnote, 10.0, INK, weight="600"))
            else:
                els.append(txt((rx_a + rx_b) * 0.5, ry + 15, rnote, 9.8, INK, anchor="middle", weight="600"))

        # Panel B (Left): Parsec geometry
        els.append(card(20, 288, 350, 206))
        els.append(pill(34, 298, "B · 第 2 级：地球公转基线与“秒差距 (pc)”", fg=BLUE, bg=BLUE_SOFT, w=304))

        els.append('<ellipse cx="88" cy="386" rx="18" ry="36" fill="none" stroke="#93c5fd" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append('<circle cx="88" cy="386" r="7" fill="#f59e0b"/>')
        els.append(txt(62, 390, "太阳", 10.0, AMBER, anchor="end", weight="700"))
        els.append(f'<circle cx="88" cy="350" r="4.2" fill="{BLUE}"/>')
        els.append(f'<circle cx="88" cy="422" r="4.2" fill="{BLUE}"/>')
        els.append(txt(88, 341, "1月地球", 9.8, BLUE, anchor="middle", weight="700"))
        els.append(txt(88, 438, "7月地球", 9.8, BLUE, anchor="middle", weight="700"))

        els.append(f'<line x1="88" y1="350" x2="88" y2="386" stroke="{ORANGE}" stroke-width="2"/>')
        els.append(txt(109, 372, "1 AU", 10.0, ORANGE, weight="700"))

        els.append(f'<line x1="88" y1="350" x2="342" y2="412" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="88" y1="422" x2="342" y2="360" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="88" y1="386" x2="236" y2="386" stroke="{SLATE}" stroke-width="1.1"/>')
        els.append('<circle cx="236" cy="386" r="5.2" fill="#ef4444"/>')
        els.append(txt(236, 370, "近邻恒星", 10.2, RED, anchor="middle", weight="700"))
        els.append(txt(180, 382, "视差角 p", 9.8, INK, anchor="middle", weight="700", halo=True))
        els.append('<line x1="342" y1="344" x2="342" y2="428" stroke="#cbd5e1" stroke-width="2"/>')
        els.append(txt(336, 340, "遥远背景星幕", 9.6, MUTED, anchor="end"))

        els.append(txt(34, 460, "• 定义：p = 1 角秒 (1/3600°) 时，距离 d = 1 pc", 10.4, INK, weight="700"))
        els.append(txt(34, 479, f"• 1 pc = {PC_AU:,.0f} AU = {PC_LY:.4f} 光年（图中角度夸张示意）", 10.0, BODY))

        # Panel C (Right): Cepheid Period-Luminosity Computed Relation
        els.append(card(386, 288, 354, 206))
        els.append(pill(400, 298, "C · 第 3 级：勒维特造父变星“周光关系”", fg=ORANGE, bg=ORANGE_SOFT, w=306))

        px0, px1 = 452.0, 718.0
        py_top, py_bot = 336.0, 432.0

        def map_p(p_days):
            return px0 + (math.log10(p_days) - 0.3) / 1.5 * (px1 - px0)

        def map_l(lg_lum):
            return py_bot - (lg_lum - 2.6) / 2.0 * (py_bot - py_top)

        els.append(f'<rect x="{px0}" y="{py_top}" width="{px1 - px0}" height="{py_bot - py_top}" fill="#f8fafc" stroke="{BORDER}"/>')
        for p_tk in (3, 10, 30, 50):
            xx = map_p(p_tk)
            els.append(f'<line x1="{xx:.1f}" y1="{py_top}" x2="{xx:.1f}" y2="{py_bot}" stroke="#eef2f7"/>')
            els.append(txt(xx, py_bot + 14, f"{p_tk}天", 9.6, MUTED, anchor="middle"))
        for lg_tk, llbl in ((3.0, "10³L☉"), (4.0, "10⁴L☉")):
            yy = map_l(lg_tk)
            els.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="#eef2f7"/>')
            els.append(txt(px0 - 6, yy + 4, llbl, 9.6, MUTED, anchor="end"))

        pts_pl = []
        for k in range(30):
            lgp = 0.40 + 1.32 * k / 29.0
            lgl = 2.59 + 1.104 * lgp
            pts_pl.append(f"{map_p(10 ** lgp):.1f},{map_l(lgl):.1f}")
        els.append(f'<polyline points="{" ".join(pts_pl)}" fill="none" stroke="{ORANGE}" stroke-width="2.4"/>')

        for pd, lbl_c, dx_c, dy_c in ((5.37, "造父四 (5.4天)", 8, 13), (31.4, "M31-V1 (31.4天)", -8, -8)):
            lgl = 2.59 + 1.104 * math.log10(pd)
            cx_p, cy_p = map_p(pd), map_l(lgl)
            els.append(f'<circle cx="{cx_p:.1f}" cy="{cy_p:.1f}" r="4.2" fill="{RED}" stroke="#ffffff" stroke-width="1.2"/>')
            anc = "start" if dx_c > 0 else "end"
            els.append(txt(cx_p + dx_c, cy_p + dy_c, lbl_c, 9.8, RED, anchor=anc, weight="700", halo=True))

        els.append(txt(400, 464, "• 测出脉动周期 P → 读出真实瓦数 L → 对比视亮度 F：", 10.2, INK, weight="700"))
        els.append(txt(400, 482, "  由平方反比律 d = √(L / 4πF) 直接算出星系距离！", 10.2, ORANGE, weight="700"))

        return figure(
            508,
            "宇宙四级测距阶梯重叠校准图、秒差距几何视差原理与造父变星周光关系实算图解",
            "上图按对数光年尺度展示行星雷达、几何视差、造父变星与Ia型超新星四级测距阶梯及其三处重叠校准带；左下演示地球公转基线与秒差距定义；右下绘制造父变星周期-光度关系及哈勃M31-V1标定点。",
            els,
        )

    def _build_logarithmic_cosmic_address():
        """SVG 3: 20-order-of-magnitude Logarithmic Cosmic Address (10^7 m to 10^27 m) with one-shot zoom scan."""
        extra_css = """
  @keyframes cosmicZoomSweep {
    0%   { transform: translateX(0px); opacity: 0.95; }
    12%  { transform: translateX(0px); opacity: 1; }
    88%  { transform: translateX(658px); opacity: 1; }
    100% { transform: translateX(658px); opacity: 0.92; }
  }
  .zoom-scanner {
    animation: cosmicZoomSweep 8.5s cubic-bezier(0.32, 0.04, 0.24, 1) 1 forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .zoom-scanner {
      animation: none !important;
      transform: translateX(658px);
    }
  }"""

        els = []
        els.extend(
            header(
                "三、你的完整“宇宙收货地址”：横跨 20 个数量级的对数标尺与“宏伟的终结”",
                "从地球直径 10⁷ m 一路放大 10²⁰ 倍到 930 亿光年可观测宇宙——为什么超过 3 亿光年后“套娃”突然停止了？",
            )
        )

        els.append(card(20, 64, 720, 178))
        els.append(pill(34, 74, "A · 对数尺度标尺 log₁₀(空间跨度 / 米)：每向右走一格 = 尺度乘以 100 倍", fg=TEAL, bg=TEAL_SOFT, w=478))

        sx0, sx1 = 48.0, 712.0
        ry_bar = 152.0

        def map_lgm(lgm):
            return sx0 + (lgm - 7.0) / 20.0 * (sx1 - sx0)

        x_eog = map_lgm(24.50)
        els.append(f'<rect x="{x_eog:.1f}" y="106" width="{sx1 - x_eog:.1f}" height="82" rx="6" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1" stroke-dasharray="4 3"/>')
        els.append(txt((x_eog + sx1) * 0.5, 118, "宏伟的终结", 9.6, PURPLE, anchor="middle", weight="700"))

        els.append(f'<line x1="{sx0}" y1="{ry_bar}" x2="{sx1}" y2="{ry_bar}" stroke="{INK}" stroke-width="2.2"/>')
        for exp_m in range(7, 28, 2):
            xx = map_lgm(exp_m)
            els.append(f'<line x1="{xx:.1f}" y1="{ry_bar - 6}" x2="{xx:.1f}" y2="{ry_bar + 6}" stroke="{SLATE}" stroke-width="1.2"/>')
            els.append(txt(xx, ry_bar + 20, f"10^{exp_m}", 9.5, MUTED, anchor="middle", cls="mono"))

        landmarks = [
            (math.log10(1.2756e7), "①地球", BLUE, -20),
            (math.log10(2 * AU_KM * 1e3), "②地轨2AU", TEAL, 36),
            (math.log10(4.2465 * LY_KM * 1e3), "③比邻星", ORANGE, -20),
            (math.log10(1e5 * LY_KM * 1e3), "④银河系", BLUE, 36),
            (math.log10(1e7 * LY_KM * 1e3), "⑤本星系群", GREEN, -20),
            (math.log10(5.2e8 * LY_KM * 1e3), "⑥拉尼亚凯亚", ORANGE, 36),
            (math.log10(9.3e10 * LY_KM * 1e3), "⑦可观测视界", PURPLE, -20),
        ]
        assert 7.10 < landmarks[0][0] < 7.12 and 26.94 < landmarks[-1][0] < 26.95
        for lgm, l_name, l_col, dy_l in landmarks:
            lx = map_lgm(lgm)
            els.append(f'<line x1="{lx:.1f}" y1="{ry_bar}" x2="{lx:.1f}" y2="{ry_bar + (dy_l + 5 if dy_l < 0 else dy_l - 12):.1f}" stroke="{l_col}" stroke-width="1.3"/>')
            els.append(f'<circle cx="{lx:.1f}" cy="{ry_bar}" r="4.5" fill="{l_col}" stroke="#ffffff" stroke-width="1.2"/>')
            anc = "start" if lgm < 7.5 else ("end" if lgm > 26.2 else "middle")
            els.append(txt(lx, ry_bar + dy_l, l_name, 10.0, l_col, anchor=anc, weight="700", halo=True))

        x_start = map_lgm(landmarks[0][0])
        els.append(
            f'<g class="zoom-scanner">'
            f'<circle cx="{x_start:.1f}" cy="{ry_bar}" r="10.5" fill="none" stroke="{RED}" stroke-width="2.2" stroke-dasharray="4 2"/>'
            f'<polygon points="{x_start:.1f},{ry_bar - 14} {x_start - 5:.1f},{ry_bar - 22} {x_start + 5:.1f},{ry_bar - 22}" fill="{RED}"/>'
            f'</g>'
        )
        els.append(txt(380, 228, "提示：红色游标单次扫过 20 个数量级后停在可观测视界终点（930 亿光年）；关闭动态效果时直接停在终点。", 9.8, MUTED, anchor="middle"))

        cards_data = [
            (
                "① 地月与太阳系疆域",
                "跨度：1.27万 km → ~2 光年",
                "• 日球层顶 ≈ 120 AU (旅行者闯出点)",
                "• 最外围奥尔特冰彗星云延伸至约",
                "  5万–10万 AU（约 0.8–1.6 光年）",
                TEAL,
                TEAL_SOFT,
            ),
            (
                "② 银河系（棒旋星系家园）",
                "直径 ≈ 10 万光年 (9.5×10²⁰ m)",
                "• 含约 1,000亿–4,000亿颗恒星",
                "• 太阳居猎户支臂，距银心 2.6万 ly",
                "• 绕银心一圈“银河年”≈ 2.3 亿年",
                BLUE,
                BLUE_SOFT,
            ),
            (
                "③ 本星系群（引力束缚小村）",
                "直径 ≈ 1,000 万光年 (~3 Mpc)",
                "• 仙女座 M31 + 银河系 + 三角座 M33",
                "  三大旋涡星系领衔 60+ 矮星系",
                "• 总质量 ≈ 4×10¹² M☉（暗物质占大头）",
                GREEN,
                GREEN_SOFT,
            ),
            (
                "④ 拉尼亚凯亚超星系团",
                "直径 ≈ 5.2 亿光年 (160 Mpc)",
                "• 2014 Tully 团队按本动速度流划定",
                "• 囊括室女座团等约 10 万个大星系",
                "• 如山谷溪流汇聚向“巨引源”盆地",
                ORANGE,
                ORANGE_SOFT,
            ),
            (
                "⑤ 宇宙纤维网与巨型空洞",
                "单泡跨度 ≈ 1.5 亿–13.7 亿光年",
                "• 90% 星系挤在不足 10% 体积的暗物质",
                "  纤维丝与长城上（斯隆长城 13.7亿 ly）",
                "• 中间夹着直径 ~1.5 亿光年的巨型空洞",
                SLATE,
                SLATE_SOFT,
            ),
            (
                "⑥ 宏伟的终结 → 可观测宇宙",
                "均匀阈值 >3.3 亿 ly → 全宽 930 亿 ly",
                "• >3.3 亿光年星系计数严格 N(R)∝R³，",
                "  不再有更高一级套娃（各向同性海绵）",
                "• 平均每 4 m³ 仅摊到约 1 颗普通氢原子！",
                PURPLE,
                PURPLE_SOFT,
            ),
        ]
        cw, ch = 232, 132
        for idx, (ctitle, csub, b1, b2, b3, cfg, cbg) in enumerate(cards_data):
            col = idx % 3
            row = idx // 3
            cx = 20 + col * 244
            cy = 254 + row * 144
            els.append(card(cx, cy, cw, ch, rx=9, fill=cbg, stroke=cfg, sw=1.1))
            els.append(txt(cx + 12, cy + 22, ctitle, 11.2, cfg, weight="700"))
            els.append(txt(cx + 12, cy + 41, csub, 10.0, INK, weight="700"))
            els.append(txt(cx + 12, cy + 64, b1, 10.0, BODY))
            els.append(txt(cx + 12, cy + 84, b2, 10.0, BODY))
            els.append(txt(cx + 12, cy + 104, b3, 10.0, INK, weight="600"))

        return figure(
            546,
            "横跨20个数量级的宇宙收货地址对数标尺、六级大尺度结构与宏伟的终结单次扫描动画图解",
            "上图在对数米标尺上精确标出从地球10^7米到可观测宇宙930亿光年（8.8×10^26米）的七座里程碑与单次扫描游标，标明超过3.3亿光年的宇宙均匀区；下图分六格详解太阳系、银河系、本星系群、拉尼亚凯亚超星系团、宇宙纤维网空洞与宏伟的终结。",
            els,
            extra_css=extra_css,
        )

    def _build_four_cosmic_distances():
        """SVG 4: Numerically integrated 4 cosmological distances in flat LCDM + z~1.6 angular size turnover."""
        om, ol = 0.315, 0.685
        dh_gly = (C_KMS / 67.4) * (PC_LY * 1e6) / 1e9

        def e_z(zv):
            return math.sqrt(om * ((1.0 + zv) ** 3) + ol)

        def integrate_distances(z_target, n_int=400):
            dc = 0.0
            dt = 0.0
            dz = z_target / n_int
            for i in range(n_int):
                zm = (i + 0.5) * dz
                ez = e_z(zm)
                dc += dz / ez
                dt += dz / ((1.0 + zm) * ez)
            dc_gly = dh_gly * dc
            dt_gly = dh_gly * dt
            da_gly = dc_gly / (1.0 + z_target)
            dl_gly = dc_gly * (1.0 + z_target)
            return dt_gly, da_gly, dc_gly, dl_gly

        dt_14, da_14, dc_14, dl_14 = integrate_distances(14.32)
        assert 13.4 < dt_14 < 13.6 and 33.5 < dc_14 < 34.1 and 2.15 < da_14 < 2.26 and 510.0 < dl_14 < 525.0

        els = []
        els.extend(
            header(
                "四、为什么同一个遥远星系会报出“四个距离”？——膨胀宇宙的四把尺子",
                "空间边走边膨胀，把日常重合的四把尺子彻底撕裂；红移 z > 1.6 后，越远的星系在天上看着反而越大！",
            )
        )

        els.append(card(20, 64, 444, 420))
        els.append(pill(34, 74, "A · 平坦 ΛCDM 四种宇宙距离实算曲线（H₀=67.4）", fg=BLUE, bg=BLUE_SOFT, w=368))

        gx0, gx1 = 78.0, 444.0
        gy_top, gy_bot = 116.0, 392.0
        lgz_min, lgz_max = math.log10(0.08), math.log10(20.0)
        lg_yi_min, lg_yi_max = math.log10(8.0), math.log10(8000.0)

        def map_zx(zv):
            return gx0 + (math.log10(zv) - lgz_min) / (lgz_max - lgz_min) * (gx1 - gx0)

        def map_dy(d_yi):
            return gy_bot - (math.log10(d_yi) - lg_yi_min) / (lg_yi_max - lg_yi_min) * (gy_bot - gy_top)

        els.append(f'<rect x="{gx0}" y="{gy_top}" width="{gx1 - gx0}" height="{gy_bot - gy_top}" fill="#f8fafc" stroke="{BORDER}"/>')
        for z_tk in (0.1, 0.5, 1.6, 5, 14.3):
            xx = map_zx(z_tk)
            els.append(f'<line x1="{xx:.1f}" y1="{gy_top}" x2="{xx:.1f}" y2="{gy_bot}" stroke="#eef2f7"/>')
            els.append(txt(xx, gy_bot + 15, f"{z_tk:g}", 9.6, MUTED, anchor="middle", cls="mono"))
        els.append(txt((gx0 + gx1) * 0.5, gy_bot + 33, "光谱红移 z = (λ观测 − λ发出) / λ发出 →", 10.2, SLATE, anchor="middle", weight="600"))

        for d_tk, dlbl in ((10, "10亿"), (50, "50亿"), (138, "138亿"), (465, "465亿"), (5000, "5000亿")):
            yy = map_dy(d_tk)
            els.append(f'<line x1="{gx0}" y1="{yy:.1f}" x2="{gx1}" y2="{yy:.1f}" stroke="#eef2f7"/>')
            els.append(txt(gx0 - 5, yy + 3.5, dlbl, 9.5, MUTED, anchor="end"))

        _, da_pk_g, _, _ = integrate_distances(1.59, n_int=400)
        peak_z = 1.59
        peak_da_yi = da_pk_g * 10.0
        assert 58.0 < peak_da_yi < 59.0

        pts_dt, pts_da, pts_dc, pts_dl = [], [], [], []
        n_pts = 80
        z_samples = sorted([10.0 ** (lgz_min + (lgz_max - lgz_min) * i / n_pts) for i in range(n_pts + 1)] + [1.59])
        for zv in z_samples:
            dt_g, da_g, dc_g, dl_g = integrate_distances(zv, n_int=180)
            dt_yi, da_yi, dc_yi, dl_yi = dt_g * 10.0, da_g * 10.0, dc_g * 10.0, dl_g * 10.0
            xx = map_zx(zv)
            pts_dt.append(f"{xx:.1f},{map_dy(dt_yi):.1f}")
            pts_da.append(f"{xx:.1f},{map_dy(da_yi):.1f}")
            pts_dc.append(f"{xx:.1f},{map_dy(dc_yi):.1f}")
            pts_dl.append(f"{xx:.1f},{map_dy(dl_yi):.1f}")

        els.append(f'<polyline points="{" ".join(pts_dl)}" fill="none" stroke="{PURPLE}" stroke-width="2.2"/>')
        els.append(f'<polyline points="{" ".join(pts_dc)}" fill="none" stroke="{BLUE}" stroke-width="2.3"/>')
        els.append(f'<polyline points="{" ".join(pts_dt)}" fill="none" stroke="{GREEN}" stroke-width="2.0" stroke-dasharray="6 3"/>')
        els.append(f'<polyline points="{" ".join(pts_da)}" fill="none" stroke="{ORANGE}" stroke-width="2.6"/>')

        xz14 = map_zx(14.32)
        els.append(f'<line x1="{xz14:.1f}" y1="{gy_top}" x2="{xz14:.1f}" y2="{gy_bot}" stroke="{RED}" stroke-width="1.2" stroke-dasharray="3 3"/>')
        for val_yi, col_v in ((dl_14 * 10, PURPLE), (dc_14 * 10, BLUE), (dt_14 * 10, GREEN), (da_14 * 10, ORANGE)):
            els.append(f'<circle cx="{xz14:.1f}" cy="{map_dy(val_yi):.1f}" r="3.8" fill="{col_v}" stroke="#ffffff" stroke-width="1.1"/>')

        x_pk, y_pk = map_zx(peak_z), map_dy(peak_da_yi)
        els.append(f'<circle cx="{x_pk:.1f}" cy="{y_pk:.1f}" r="4.5" fill="{RED}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(txt(x_pk - 6, y_pk - 9, f"极值 z≈{peak_z:.2f} ({peak_da_yi:.1f}亿ly)", 9.6, RED, anchor="end", weight="700", halo=True))

        els.append(txt(map_zx(3.8), map_dy(1100), "光度距离 D_L", 10.0, PURPLE, anchor="end", weight="700", halo=True))
        els.append(txt(map_zx(4.8), map_dy(330), "今日共动 D_C", 10.0, BLUE, anchor="end", weight="700", halo=True))
        els.append(txt(map_zx(5.5), map_dy(86), "光行回望 D_T", 10.0, GREEN, anchor="middle", weight="700", halo=True))
        els.append(txt(map_zx(6.5), map_dy(26), "角直径距离 D_A ↓", 10.0, ORANGE, anchor="middle", weight="700", halo=True))

        els.append(
            txt(
                242,
                468,
                f"JWST z=14.32 四值：D_A={da_14 * 10:.1f}亿 · D_T={dt_14 * 10:.0f}亿 · D_C={dc_14 * 10:.0f}亿 · D_L={dl_14 * 10:.0f}亿光年",
                9.8,
                INK,
                anchor="middle",
                weight="700",
            )
        )

        # Panel B: Intuitive Explanation of Angular Turnover
        els.append(card(480, 64, 260, 420))
        els.append(pill(494, 74, "B · 宇宙天然放大镜奇观", fg=ORANGE, bg=ORANGE_SOFT, w=232))

        els.append(card(494, 108, 232, 178, rx=8, fill="#0f172a", stroke="#334155"))
        ox_e, oy_e = 518.0, 200.0
        els.append(f'<circle cx="{ox_e}" cy="{oy_e}" r="5" fill="#38bdf8"/>')
        els.append(f'<text x="{ox_e + 2}" y="{oy_e + 18}" font-size="9.8" fill="#bae6fd" font-weight="700">地球</text>')

        els.append(f'<line x1="{ox_e}" y1="{oy_e}" x2="694" y2="187" stroke="#93c5fd" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="{ox_e}" y1="{oy_e}" x2="694" y2="213" stroke="#93c5fd" stroke-width="1.2" stroke-dasharray="4 3"/>')
        els.append('<ellipse cx="694" cy="200" rx="4" ry="13" fill="#60a5fa" stroke="#bae6fd" stroke-width="1.2"/>')
        els.append('<text x="718" y="172" font-size="9.4" fill="#93c5fd" text-anchor="end">z≈1.6 (发光距58.5亿ly)</text>')
        els.append('<text x="718" y="232" font-size="9.4" fill="#cbd5e1" text-anchor="end">10kpc星系张角最小≈1.2″</text>')

        els.append(f'<line x1="{ox_e}" y1="{oy_e}" x2="588" y2="172" stroke="#fb923c" stroke-width="1.7"/>')
        els.append(f'<line x1="{ox_e}" y1="{oy_e}" x2="588" y2="228" stroke="#fb923c" stroke-width="1.7"/>')
        els.append('<ellipse cx="588" cy="200" rx="5" ry="26" fill="#fb923c" fill-opacity="0.45" stroke="#fdba74" stroke-width="1.5"/>')
        els.append('<text x="610" y="132" font-size="9.6" fill="#fdba74" text-anchor="middle" font-weight="700">z=14.3 发光时仅距 22.1亿ly！</text>')
        els.append('<text x="610" y="268" font-size="9.5" fill="#fed7aa" text-anchor="middle" font-weight="700">同尺寸星系张角反增至≈3.1″</text>')

        els.append(txt(494, 310, "为什么越远看着反而越大？（Hogg 1999）", 10.6, ORANGE, weight="700"))
        els.append(txt(494, 332, "① 日常静态房间里：D_A = D_C = D_L，", 10.0, BODY))
        els.append(txt(494, 351, "   东西越远，视角 θ = 直径 / D 越小；", 10.0, BODY))
        els.append(txt(494, 373, "② 但在膨胀宇宙里，决定天上张角的是", 10.0, BODY))
        els.append(txt(494, 392, "   星系发光那一刻离我们的距离：", 10.0, INK, weight="700"))
        els.append(txt(494, 412, "   D_A = D_C / (1 + z)！", 10.6, RED, weight="700"))
        els.append(txt(494, 434, "③ z > 1.6 后宇宙当时太紧凑，发光点", 10.0, BODY))
        els.append(txt(494, 453, "   反而贴近早期我们，张开大视角定格", 10.0, BODY))
        els.append(txt(494, 472, "   至今——但表面亮度按 (1+z)⁴ 暴跌！", 10.0, PURPLE, weight="700"))

        return figure(
            498,
            "平坦ΛCDM宇宙四种距离随红移演化实算曲线与z大于1.6角直径反转放大镜效应图解",
            "左图精确积分绘制光度距离D_L、共动距离D_C、光行距离D_T与角直径距离D_A曲线，标出z=14.32星系的四个数值及D_A在z≈1.6处的58亿光年折返极值；右图直观解释更遥远星系因发光时距离仅22亿光年而在天空呈现更大视张角。",
            els,
        )

    def _build_observable_vs_whole_universe():
        """SVG 5: Observable horizon vs Entire Universe curvature (Omega_k) + Cosmic Event Horizon & density budget."""
        om, ol = 0.315, 0.685
        dh_gly = (C_KMS / 67.4) * (PC_LY * 1e6) / 1e9
        n_int = 500
        eh_sum = 0.0
        for i in range(n_int):
            am = (i + 0.5) / n_int
            eh_sum += (1.0 / n_int) / math.sqrt(om * (am ** 3) + ol)
        d_eh_gly = dh_gly * eh_sum  # ~16.5 Gly
        assert 16.2 < d_eh_gly < 16.9

        els = []
        els.extend(
            header(
                "五、直径 930 亿光年之外是什么？——视界不等于尽头，给整个宇宙量曲率",
                "可观测宇宙只是光速来得及跑进我们眼睛的“海平线圆圈”；普朗克卫星测得空间平直到千分之二以内",
            )
        )

        # Panel A: Sea-Horizon Overlapping Spheres + 167 Gly Event Horizon
        els.append(card(20, 64, 366, 286))
        els.append(pill(34, 74, f"A · 两个视界：465 亿光年过去 vs {d_eh_gly * 10:.0f} 亿光年未来", fg=BLUE, bg=BLUE_SOFT, w=338))

        els.append(card(34, 108, 338, 178, rx=8, fill="#0f172a", stroke="#334155"))
        for gx in range(54, 360, 38):
            els.append(f'<line x1="{gx}" y1="112" x2="{gx}" y2="282" stroke="#1e293b" stroke-width="0.9"/>')
        for gy in range(126, 282, 36):
            els.append(f'<line x1="38" y1="{gy}" x2="368" y2="{gy}" stroke="#1e293b" stroke-width="0.9"/>')

        els.append('<circle cx="252" cy="196" r="66" fill="#a855f7" fill-opacity="0.14" stroke="#c084fc" stroke-width="1.5" stroke-dasharray="5 3"/>')
        els.append('<circle cx="252" cy="196" r="3.5" fill="#e879f9"/>')
        els.append('<text x="260" y="199" font-size="9.6" fill="#f5d0fe" font-weight="700">外星观测者</text>')
        els.append('<text x="282" y="124" font-size="9.5" fill="#e9d5ff" text-anchor="middle">他的930亿ly视界</text>')

        r_obs_px = 66.0
        r_eh_px = r_obs_px * (d_eh_gly / 46.5)
        els.append(f'<circle cx="144" cy="196" r="{r_obs_px:.1f}" fill="#1d4ed8" fill-opacity="0.22" stroke="#38bdf8" stroke-width="2.0"/>')
        els.append(f'<circle cx="144" cy="196" r="{r_eh_px:.1f}" fill="#f59e0b" fill-opacity="0.22" stroke="#fbbf24" stroke-width="1.6"/>')
        els.append('<circle cx="144" cy="196" r="3.8" fill="#ffffff"/>')
        els.append('<text x="144" y="211" font-size="9.6" fill="#ffffff" text-anchor="middle" font-weight="700">地球</text>')
        els.append('<text x="132" y="124" font-size="9.6" fill="#7dd3fc" text-anchor="middle" font-weight="700">可观测视界 R≈465亿ly</text>')
        els.append(f'<text x="144" y="236" font-size="9.5" fill="#fde047" text-anchor="middle" font-weight="700">事件视界≈{d_eh_gly * 10:.0f}亿ly</text>')
        els.append('<text x="203" y="278" font-size="9.5" fill="#94a3b8" text-anchor="middle">← 视界之外并非悬崖，而是光尚未跑到的同类星海 →</text>')

        els.append(txt(34, 306, "• 过去视界（R≈465亿ly）：大爆炸至今光能到的最大范围；", 10.0, BODY))
        els.append(txt(34, 326, f"• 未来事件视界（R≈{d_eh_gly * 10:.0f}亿ly，z≈1.87）：圈外星系今天", 10.0, RED, weight="700"))
        els.append(txt(34, 343, "  发出的光再也追不上暗能量加速膨胀，永远到不了地球！", 10.0, INK, weight="600"))

        # Panel B: Planck CMB Triangle Curvature Test
        els.append(card(398, 64, 342, 286))
        els.append(pill(412, 74, "B · 普朗克卫星“宇宙大三角”测整体空间曲率", fg=PURPLE, bg=PURPLE_SOFT, w=314))

        geoms = [
            ("① 正曲率闭合 (Ω_k < 0)", "三维超球面 · 有限但无边缘", "大三角内角和 > 180°", 112, ORANGE, ORANGE_SOFT, "+14"),
            ("② 零曲率平直 (Ω_k = 0)", "欧氏平直空间 · 可无限延伸", "大三角内角和 = 180°（实测吻合！）", 184, GREEN, GREEN_SOFT, "0"),
            ("③ 负曲率开放 (Ω_k > 0)", "三维马鞍面 · 空间无限延伸", "大三角内角和 < 180°", 256, BLUE, BLUE_SOFT, "-12"),
        ]
        for gtitle, gsub, gang, gy_c, gfg, gbg, bulge in geoms:
            els.append(card(412, gy_c, 314, 62, rx=8, fill=gbg, stroke=gfg, sw=1.1))
            b_val = int(bulge)
            ax, ay = 450, gy_c + 12
            bx, by = 426, gy_c + 50
            cx_t, cy_t = 474, gy_c + 50
            d_tri = (
                f"M {ax},{ay} "
                f"Q {(ax + bx) / 2 - b_val * 0.4:.1f},{(ay + by) / 2:.1f} {bx},{by} "
                f"Q 450,{by + b_val * 0.45:.1f} {cx_t},{cy_t} "
                f"Q {(ax + cx_t) / 2 + b_val * 0.4:.1f},{(ay + cy_t) / 2:.1f} {ax},{ay}"
            )
            els.append(f'<path d="{d_tri}" fill="#ffffff" fill-opacity="0.7" stroke="{gfg}" stroke-width="1.8"/>')
            els.append(txt(488, gy_c + 21, gtitle, 10.6, gfg, weight="700"))
            els.append(txt(488, gy_c + 39, gsub, 9.9, BODY))
            els.append(txt(488, gy_c + 55, gang, 9.9, INK, weight="700"))

        els.append(txt(412, 338, "Planck 2018 + BAO 实测：Ω_k = 0.0007 ± 0.0019", 10.6, PURPLE, weight="700"))

        # Panel C (Bottom): Whole-Universe Lower Bound & Cosmic Sparsity Bar
        els.append(card(20, 362, 720, 120))
        els.append(pill(34, 372, "C · 终极尺度账本：整个宇宙至少有多大？930 亿光年里到底装了什么？", fg=TEAL, bg=TEAL_SOFT, w=486))

        bx0, bw_tot, by_b = 34.0, 400.0, 406.0
        w_de = bw_tot * 0.685
        w_dm = bw_tot * 0.266
        w_bm = bw_tot * 0.049
        els.append(f'<rect x="{bx0:.1f}" y="{by_b}" width="{w_de:.1f}" height="26" rx="4" fill="#6d28d9"/>')
        els.append(f'<rect x="{bx0 + w_de:.1f}" y="{by_b}" width="{w_dm:.1f}" height="26" fill="#2563eb"/>')
        els.append(f'<rect x="{bx0 + w_de + w_dm:.1f}" y="{by_b}" width="{w_bm:.1f}" height="26" rx="3" fill="#f59e0b"/>')
        els.append(txt(bx0 + w_de * 0.5, by_b + 17, "暗能量 68.5%", 10.4, "#ffffff", anchor="middle", weight="700"))
        els.append(txt(bx0 + w_de + w_dm * 0.5, by_b + 17, "暗物质 26.6%", 10.0, "#ffffff", anchor="middle", weight="700"))
        els.append(txt(bx0 + w_de + w_dm + w_bm + 8, by_b + 17, "普通原子仅 4.9%！", 10.2, AMBER, weight="700"))

        els.append(txt(34, 452, "• 极致空旷：临界密度 ≈ 5.1 质子能量/m³；普通物质平均每 4 立方米才摊到 1 颗氢原子！", 10.1, BODY))
        els.append(txt(34, 471, "• 整体下限：即便宇宙闭合，总体积也 > 251 倍可观测体积（Vardanyan 等 2011；暴胀模型更远超 10⁷⁸ 倍）。", 10.0, INK, weight="600"))

        return figure(
            496,
            "可观测宇宙465亿光年视界与165亿光年事件视界对比、普朗克CMB大三角空间曲率检验及宇宙组分图解",
            "左上对比地球与遥远外星人各自直径930亿光年的重叠可观测视界球及内部半径165亿光年的未来事件视界；右上图解正曲率、零曲率与负曲率空间大三角内角和及普朗克Ω_k=0.0007±0.0019实测；下方展示68.5%暗能量、26.6%暗物质、4.9%普通原子占比与闭合体积超251倍下限。",
            els,
        )

    @register(
        "cosmic-scale",
        "宇宙的大小和尺度五步图解：篮球太阳微缩与地月塞七行星、四级量天尺校准、20数量级对数宇宙地址与宏伟的终结动画、膨胀宇宙四把距离尺子及整体宇宙曲率视界",
        "mechanics_sky",
    )
    def build_cosmic_scale():
        write_svg(SUBDIR, "basketball-sun-and-earth-moon-gap.svg", _build_basketball_sun_and_gap())
        write_svg(SUBDIR, "cosmic-distance-ladder-four-rungs.svg", _build_distance_ladder())
        write_svg(SUBDIR, "logarithmic-cosmic-address-zoom.svg", _build_logarithmic_cosmic_address())
        write_svg(SUBDIR, "four-cosmic-distances-and-angular-turnover.svg", _build_four_cosmic_distances())
        write_svg(SUBDIR, "observable-horizon-vs-whole-universe-curvature.svg", _build_observable_vs_whole_universe())


_register_cosmic_scale()


def _register_stellar_evolution():
    SUBDIR = "stellar-evolution"
    RED = "#dc2626"
    RED_SOFT = "#fef2f2"
    AMBER = "#d97706"
    AMBER_SOFT = "#fffbeb"
    TEAL = "#0d9488"
    TEAL_SOFT = "#f0fdfa"

    # Physical & astronomical constants (IAU 2015 nominal solar/planetary values, OpenStax Astronomy 2e)
    T_SUN_K = 5772.0
    M_JUP_IN_SOLAR = 1.0 / 1047.56  # ~0.0009546 M_sun
    M_DEUT_SOLAR = 13.0 * M_JUP_IN_SOLAR  # ~0.01241 M_sun (IAU brown-dwarf lower threshold)
    M_HBURN_SOLAR = 0.075  # ~78.6 M_J sustained p-p hydrogen fusion threshold
    M_CHANDRA = 1.44  # Solar masses (Chandrasekhar relativistic degenerate limit for mu_e ~ 2)
    M_TOV_MAX = 2.17  # Solar masses (GW170817 Margalit & Metzger 2017 90% upper bound)
    assert 0.012 < M_DEUT_SOLAR < 0.013
    assert 78.0 < (M_HBURN_SOLAR / M_JUP_IN_SOLAR) < 79.0

    def _build_molecular_cloud_and_threshold():
        """SVG 1: Cold GMC Jeans collapse, Virial negative heat capacity, and 13 M_J / 0.075 M_sun thresholds."""
        els = []
        els.extend(
            header(
                "一、恒星为什么偏要在 -260℃ 冰云里诞生？负热容升温与 0.075 M⊙ 点火红线",
                "巨分子云密度暴涨近 10²⁰ 倍：辐射丢掉一半引力能反而越缩越烫，出生质量一锤定下三类天体命运",
            )
        )

        # Panel A: Cold cloud Jeans collapse & Virial Theorem 50/50 split
        els.append(card(20, 64, 720, 232))
        els.append(pill(34, 74, "A · 越冷越易坍缩，越丢热量反而越烫：金斯判据与维里定理“负热容”", fg=BLUE, bg=BLUE_SOFT, w=452))

        # Left half: 3-stage collapse visual (x=34..382)
        # Stage 1: Cold GMC
        els.append('<ellipse cx="86" cy="176" rx="44" ry="34" fill="#dbeafe" stroke="#2563eb" stroke-width="1.6" stroke-dasharray="4 3"/>')
        els.append('<ellipse cx="94" cy="172" rx="26" ry="18" fill="#bfdbfe" opacity="0.8"/>')
        els.append(txt(86, 175, "10–20 K", 10.6, BLUE, anchor="middle", weight="700"))
        els.append(txt(86, 190, "(-258℃)", 9.8, BODY, anchor="middle"))
        els.append(txt(86, 226, "① 巨分子云", 10.6, INK, anchor="middle", weight="700"))
        els.append(txt(86, 242, "跨度几十光年", 9.8, MUTED, anchor="middle"))
        els.append(txt(86, 256, "热气压极弱", 9.8, BLUE, anchor="middle", weight="600"))

        els.append(f'<line x1="136" y1="176" x2="162" y2="176" stroke="{SLATE}" stroke-width="1.8"/>')
        els.append(f'<polygon points="166,176 158,171 158,181" fill="{SLATE}"/>')

        # Stage 2: Contracting dense core
        els.append('<circle cx="206" cy="176" r="28" fill="#fef3c7" stroke="#d97706" stroke-width="1.8"/>')
        els.append('<circle cx="206" cy="176" r="12" fill="#fbbf24"/>')
        for ang in (35, 145, 215, 325):
            rad = math.radians(ang)
            x1 = 206 + 25 * math.cos(rad)
            y1 = 176 + 25 * math.sin(rad)
            x2 = 206 + 14 * math.cos(rad)
            y2 = 176 + 14 * math.sin(rad)
            els.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#b45309" stroke-width="1.5"/>')
        els.append(txt(206, 226, "② 致密云核坍缩", 10.6, INK, anchor="middle", weight="700"))
        els.append(txt(206, 242, "M > 金斯质量 M_J", 9.8, AMBER, anchor="middle", weight="600"))
        els.append(txt(206, 256, "红外光透明散热", 9.8, MUTED, anchor="middle"))

        els.append(f'<line x1="240" y1="176" x2="266" y2="176" stroke="{SLATE}" stroke-width="1.8"/>')
        els.append(f'<polygon points="270,176 262,171 262,181" fill="{SLATE}"/>')

        # Stage 3: Protostellar disk + bipolar jets
        cx3, cy3 = 322, 176
        els.append(f'<polygon points="{cx3-7},{cy3-8} {cx3-16},{cy3-46} {cx3+16},{cy3-46} {cx3+7},{cy3-8}" fill="#bfdbfe" opacity="0.65"/>')
        els.append(f'<polygon points="{cx3-7},{cy3+8} {cx3-16},{cy3+46} {cx3+16},{cy3+46} {cx3+7},{cy3+8}" fill="#bfdbfe" opacity="0.65"/>')
        els.append(f'<line x1="{cx3}" y1="{cy3-10}" x2="{cx3}" y2="{cy3-48}" stroke="{BLUE}" stroke-width="2"/>')
        els.append(f'<line x1="{cx3}" y1="{cy3+10}" x2="{cx3}" y2="{cy3+48}" stroke="{BLUE}" stroke-width="2"/>')
        els.append(f'<ellipse cx="{cx3}" cy="{cy3}" rx="38" ry="9" fill="#fde68a" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(f'<circle cx="{cx3}" cy="{cy3}" r="8" fill="#ef4444" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(txt(cx3, 232, "③ 原恒星盘与两极喷流", 10.6, INK, anchor="middle", weight="700"))
        els.append(txt(cx3, 248, "密度暴涨近 10²⁰ 倍", 9.8, RED, anchor="middle", weight="700"))
        els.append(txt(cx3, 262, "核心冲向千万度", 9.8, MUTED, anchor="middle"))

        # Vertical divider inside Panel A
        els.append(f'<line x1="390" y1="108" x2="390" y2="282" stroke="{HAIRLINE}" stroke-width="1.2" stroke-dasharray="4 3"/>')

        # Right half: Virial theorem 50/50 split bar (x=404..726)
        els.append(txt(404, 122, "维里定理账本（2K + U = 0）：引力释放势能去哪了？", 11.0, INK, weight="700"))
        els.append('<rect x="404" y="134" width="316" height="22" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.2"/>')
        els.append(txt(562, 149, "引力收缩释放势能  |ΔU| = 100%", 10.4, INK, anchor="middle", weight="700"))

        # Split into two 50% bars
        els.append('<rect x="404" y="166" width="154" height="36" rx="5" fill="#eaf4fb" stroke="#1d6fa5" stroke-width="1.5"/>')
        els.append(txt(481, 181, "50% 辐射逃向太空", 10.3, BLUE, anchor="middle", weight="700"))
        els.append(txt(481, 196, "总能量 ΔE = -|ΔU|/2 < 0", 9.8, BODY, anchor="middle"))

        els.append('<rect x="566" y="166" width="154" height="36" rx="5" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/>')
        els.append(txt(643, 181, "50% 留作热动能！", 10.3, RED, anchor="middle", weight="700"))
        els.append(txt(643, 196, "ΔK = +|ΔU|/2 > 0 升温", 9.8, BODY, anchor="middle"))

        els.append('<rect x="404" y="214" width="316" height="66" rx="6" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.3"/>')
        els.append(txt(416, 233, "• 负热容奇观：水壶丢掉热量会变凉，自引力气团丢掉", 10.1, INK, weight="600"))
        els.append(txt(416, 250, "  辐射能却迫使引力进一步深缩，核心反而越缩越烫！", 10.1, ORANGE, weight="700"))
        els.append(txt(416, 268, "• 直到量子简并压刹住收缩，或氢聚变稳稳点火才停下。", 10.0, BODY))

        # Panel B: Logarithmic Birth-Mass Threshold Ruler
        els.append(card(20, 310, 720, 236))
        els.append(pill(34, 320, "B · 出生质量定终身（对数坐标）：为什么木星和褐矮星点不着真正的“恒星之火”？", fg=ORANGE, bg=ORANGE_SOFT, w=504))

        lm_min, lm_max = -3.15, 2.30
        bx0, bx1 = 52.0, 708.0

        def mx(m_sol):
            lm = math.log10(m_sol)
            return bx0 + (lm - lm_min) / (lm_max - lm_min) * (bx1 - bx0)

        x_jup = mx(M_JUP_IN_SOLAR)
        x_deut = mx(M_DEUT_SOLAR)
        x_hburn = mx(M_HBURN_SOLAR)
        x_sun = mx(1.0)
        x_ostar = mx(40.0)
        x_emax = mx(150.0)
        assert bx0 < x_jup < x_deut < x_hburn < x_sun < x_ostar < x_emax < bx1
        assert (x_hburn - x_deut) > 85.0 and (x_sun - x_hburn) > 120.0

        yb, bh = 414.0, 30.0
        # 4 regime segments along the logarithmic mass bar
        els.append(f'<rect x="{bx0:.1f}" y="{yb}" width="{x_deut - bx0:.1f}" height="{bh}" rx="4" fill="#cbd5e1" stroke="#64748b" stroke-width="1.3"/>')
        els.append(f'<rect x="{x_deut:.1f}" y="{yb}" width="{x_hburn - x_deut:.1f}" height="{bh}" fill="#f3e8ff" stroke="{PURPLE}" stroke-width="1.5"/>')
        els.append(f'<rect x="{x_hburn:.1f}" y="{yb}" width="{x_emax - x_hburn:.1f}" height="{bh}" fill="#fef3c7" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(f'<rect x="{x_emax:.1f}" y="{yb}" width="{bx1 - x_emax:.1f}" height="{bh}" rx="3" fill="#fee2e2" stroke="{RED}" stroke-width="1.3" stroke-dasharray="3 2"/>')

        els.append(txt((bx0 + x_deut) / 2, yb + 19, "行星 (<13 M_J)", 10.2, INK, anchor="middle", weight="700"))
        els.append(txt((x_deut + x_hburn) / 2, yb + 19, "褐矮星", 10.3, PURPLE, anchor="middle", weight="700"))
        els.append(txt((x_hburn + x_emax) / 2, yb + 19, "真正的恒星（核心持续氢核聚变：0.075 – ~150 M⊙）", 10.8, ORANGE, anchor="middle", weight="700"))

        # Top callouts (strictly spaced > 160 px apart)
        # 1) Jupiter
        els.append(f'<line x1="{x_jup:.1f}" y1="{yb}" x2="{x_jup:.1f}" y2="386" stroke="{SLATE}" stroke-width="1.5"/>')
        els.append(f'<circle cx="{x_jup:.1f}" cy="{yb}" r="4" fill="{SLATE}"/>')
        els.append(txt(48, 368, "木星 1 M_J", 10.2, INK, weight="700"))
        els.append(txt(48, 382, "(0.00095 M⊙)", 9.8, MUTED))

        # 2) 0.075 M_sun Hydrogen ignition threshold (key highlight!)
        els.append(f'<line x1="{x_hburn:.1f}" y1="{yb - 4}" x2="{x_hburn:.1f}" y2="{yb + bh + 6}" stroke="{RED}" stroke-width="2.4"/>')
        els.append(f'<line x1="{x_hburn:.1f}" y1="{yb - 4}" x2="{x_hburn:.1f}" y2="384" stroke="{RED}" stroke-width="1.8"/>')
        els.append(txt(x_hburn, 366, "★ 氢点火红线 0.075 M⊙ (≈79 M_J)", 10.5, RED, anchor="middle", weight="700"))
        els.append(txt(x_hburn, 381, "核心达 ~1,200万 K 稳烧质子链", 9.8, BODY, anchor="middle"))

        # 3) Massive O-star 40 M_sun
        els.append(f'<line x1="{x_ostar:.1f}" y1="{yb}" x2="{x_ostar:.1f}" y2="386" stroke="#2563eb" stroke-width="1.6"/>')
        els.append(f'<circle cx="{x_ostar:.1f}" cy="{yb}" r="4.2" fill="#2563eb"/>')
        els.append(txt(x_ostar, 368, "O型蓝巨星 40 M⊙", 10.2, BLUE, anchor="middle", weight="700"))
        els.append(txt(x_ostar, 382, "光度 ~30万 L⊙", 9.8, MUTED, anchor="middle"))

        # Bottom callouts (strictly spaced > 150 px apart)
        # 1) 13 M_J Deuterium fusion threshold
        els.append(f'<line x1="{x_deut:.1f}" y1="{yb + bh}" x2="{x_deut:.1f}" y2="466" stroke="{PURPLE}" stroke-width="1.8"/>')
        els.append(txt(x_deut, 481, "氘聚变门槛 13 M_J (0.012 M⊙)", 10.3, PURPLE, anchor="middle", weight="700"))
        els.append(txt(x_deut, 496, "褐矮星短暂烧重氢，简并压提前刹住收缩", 9.8, BODY, anchor="middle"))

        # 2) Sun 1.0 M_sun
        els.append(f'<line x1="{x_sun:.1f}" y1="{yb + bh}" x2="{x_sun:.1f}" y2="466" stroke="{AMBER}" stroke-width="1.8"/>')
        els.append(f'<circle cx="{x_sun:.1f}" cy="{yb + bh}" r="4.5" fill="{AMBER}"/>')
        els.append(txt(x_sun, 481, "太阳 1.0 M⊙ (G2V)", 10.4, ORANGE, anchor="middle", weight="700"))
        els.append(txt(x_sun, 496, "核心 1,570 万 K", 9.8, BODY, anchor="middle"))

        # 3) Upper mass limit ~150 M_sun
        els.append(f'<line x1="{x_emax:.1f}" y1="{yb + bh}" x2="{x_emax:.1f}" y2="466" stroke="{RED}" stroke-width="1.8"/>')
        els.append(txt(724, 481, "质量上限 ~100–200 M⊙", 10.3, RED, anchor="end", weight="700"))
        els.append(txt(724, 496, "猛烈辐射压直接吹飞吸积气体", 9.8, BODY, anchor="end"))

        els.append(txt(34, 530, "注：无论 15 M_J 还是 70 M_J 的褐矮星，在电子简并压支撑下体积几乎都与木星相当，终生缓慢变暗（光谱 L → T → Y）。", 10.0, MUTED))

        return figure(
            560,
            "巨分子云低温坍缩、维里定理负热容升温机制与恒星0.075太阳质量点火红线图解",
            "上半部展示10至20K巨分子云经金斯不稳定性坍缩为原恒星盘与两极喷流，并按维里定理拆解引力势能50%辐射逃逸、50%加热核心的负热容机制；下半部在对数质量轴上标出13倍木星质量氘聚变褐矮星门槛、0.075太阳质量氢聚变恒星红线与100至200太阳质量辐射压上限。",
            els,
        )

    def _build_hr_diagram_and_lifetimes():
        """SVG 2: Computed H-R diagram with Stefan-Boltzmann constant-radius lines, animated 1 M_sun track, & lifetime paradox."""
        els = []
        els.extend(
            header(
                "二、赫罗图（H–R 图）一生轨迹：为什么越庞大的恒星反而越“短命”？",
                "横轴向左升温、纵轴向上增亮：太阳 120 亿年演化动画，对比大质量恒星“挥霍无度”的百万年闪击战",
            )
        )

        # CSS animation for 1 M_sun evolutionary track (1-shot, forwards, prefers-reduced-motion compliant)
        els.append(
            """<style>
  .hr-sun-anim {
    stroke-dasharray: 1400;
    stroke-dashoffset: 1400;
    animation: hrDrawTrack 8.5s cubic-bezier(0.32, 0.04, 0.24, 1) 0.4s forwards;
  }
  .hr-wd-pulse {
    opacity: 0;
    animation: hrShowEnd 0.8s ease-out 8.6s forwards;
  }
  @keyframes hrDrawTrack {
    0% { stroke-dashoffset: 1400; }
    100% { stroke-dashoffset: 0; }
  }
  @keyframes hrShowEnd {
    0% { opacity: 0; }
    100% { opacity: 1; }
  }
  @media (prefers-reduced-motion: reduce) {
    .hr-sun-anim { animation: none !important; stroke-dashoffset: 0 !important; }
    .hr-wd-pulse { animation: none !important; opacity: 1 !important; }
  }
</style>"""
        )

        # Left Panel: H-R Diagram (x=20..508, y=64..582)
        els.append(card(20, 64, 488, 518))
        els.append(pill(34, 74, "A · 赫罗图（左热右冷 · 上亮下暗）与太阳一生轨迹动画", fg=BLUE, bg=BLUE_SOFT, w=386))

        px0, px1 = 76.0, 488.0
        py0, py1 = 114.0, 522.0
        pw, ph = px1 - px0, py1 - py0
        lt_max, lt_min = math.log10(45000.0), math.log10(2400.0)
        ll_min, ll_max = -4.5, 6.3

        def hx(t_k):
            return px0 + (lt_max - math.log10(t_k)) / (lt_max - lt_min) * pw

        def hy(log_l):
            return py1 - (log_l - ll_min) / (ll_max - ll_min) * ph

        # Stefan-Boltzmann exact check: L/L_sun = (R/R_sun)^2 * (T/5772)^4
        def sb_log_l(t_k, r_sol):
            return 2.0 * math.log10(r_sol) + 4.0 * math.log10(t_k / T_SUN_K)

        assert abs(sb_log_l(T_SUN_K, 1.0)) < 1e-12
        assert abs(sb_log_l(T_SUN_K, 100.0) - 4.0) < 1e-12

        # Plot frame background
        els.append(f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="#f8fafc" stroke="{BORDER}" stroke-width="1.2"/>')

        # Horizontal luminosity gridlines
        for lg in (-4, -2, 0, 2, 4, 6):
            yy = hy(lg)
            els.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="#e2e8f0" stroke-width="1"/>')
            lbl = "1" if lg == 0 else f"10^{lg}"
            els.append(txt(px0 - 6, yy + 4, lbl, 9.8, MUTED, anchor="end"))

        # Vertical temperature gridlines (reversed!)
        for tk, t_lbl in ((40000, "40,000"), (20000, "20,000"), (10000, "10,000"), (5772, "5,772"), (3000, "3,000")):
            xx = hx(tk)
            els.append(f'<line x1="{xx:.1f}" y1="{py0}" x2="{xx:.1f}" y2="{py1}" stroke="#e2e8f0" stroke-width="1"/>')
            els.append(txt(xx, py1 + 15, t_lbl, 9.8, MUTED, anchor="middle"))

        # Spectral class header along top of plot box
        for sp_cls, sp_t, sp_col in (
            ("O", 36000, "#2563eb"),
            ("B", 18000, "#3b82f6"),
            ("A", 8800, "#0ea5e9"),
            ("F", 6700, "#0d9488"),
            ("G", 5600, "#d97706"),
            ("K", 4400, "#ea580c"),
            ("M", 2950, "#dc2626"),
        ):
            els.append(txt(hx(sp_t), py0 - 5, sp_cls, 10.2, sp_col, anchor="middle", weight="700"))

        # Constant-radius Stefan-Boltzmann lines clipped to plot box
        for r_sol, r_lbl, t_tag in (
            (0.01, "0.01 R⊙", 27000),
            (0.1, "0.1 R⊙", 28000),
            (1.0, "1 R⊙", 22000),
            (10.0, "10 R⊙", 11000),
            (100.0, "100 R⊙", 6800),
            (1000.0, "1000 R⊙", 5800),
        ):
            pts_r = []
            for i in range(81):
                lt = lt_min + (lt_max - lt_min) * (i / 80.0)
                tk = 10.0 ** lt
                ll = sb_log_l(tk, r_sol)
                if ll_min <= ll <= ll_max:
                    pts_r.append(f"{hx(tk):.1f},{hy(ll):.1f}")
            if len(pts_r) >= 2:
                els.append(f'<polyline points="{" ".join(pts_r)}" fill="none" stroke="#cbd5e1" stroke-width="1.1" stroke-dasharray="4 3"/>')
            ll_tag = sb_log_l(t_tag, r_sol)
            els.append(txt(hx(t_tag), hy(ll_tag) - 4, r_lbl, 9.8, "#64748b", anchor="middle"))

        # Main-Sequence ribbon (ZAMS empirical curve from 40 M_sun to 0.1 M_sun)
        ms_models = [
            (42000, 5.45),
            (30000, 4.45),
            (16000, 2.85),
            (9500, 1.55),
            (7000, 0.65),
            (5772, 0.00),
            (4600, -0.55),
            (3600, -1.45),
            (2800, -2.95),
        ]
        ms_pts = " ".join(f"{hx(t):.1f},{hy(l):.1f}" for t, l in ms_models)
        els.append(f'<polyline points="{ms_pts}" fill="none" stroke="#fde68a" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" opacity="0.65"/>')
        els.append(f'<polyline points="{ms_pts}" fill="none" stroke="#eab308" stroke-width="2.0" stroke-dasharray="3 3" opacity="0.85"/>')
        els.append(txt(hx(11500) - 24, hy(2.05) + 22, "主序星带", 10.4, "#b45309", anchor="middle", weight="700"))

        # Static 25 M_sun Massive Star supergiant track at top
        m25_pts = [
            (37000, 5.05),
            (22000, 5.25),
            (8500, 5.28),
            (3650, 5.30),
        ]
        m25_str = " ".join(f"{hx(t):.1f},{hy(l):.1f}" for t, l in m25_pts)
        els.append(f'<polyline points="{m25_str}" fill="none" stroke="{BLUE}" stroke-width="2.2" stroke-dasharray="6 3"/>')
        els.append(f'<circle cx="{hx(37000):.1f}" cy="{hy(5.05):.1f}" r="4.2" fill="{BLUE}"/>')
        els.append(f'<polygon points="{hx(3650):.1f},{hy(5.30)-6:.1f} {hx(3650)+6:.1f},{hy(5.30)+5:.1f} {hx(3650)-6:.1f},{hy(5.30)+5:.1f}" fill="{RED}"/>')
        els.append(txt(hx(14000), hy(5.30) - 8, "25 M⊙ 超巨星快车道（< 800 万年 → 超新星爆发）", 9.9, BLUE, anchor="middle", weight="700"))

        # 1 M_sun Solar Evolutionary Track (static subtle guide + CSS animated foreground path)
        sun_track = [
            (5772, 0.00),   # ① ZAMS / Sun
            (5150, 0.35),   # Subgiant
            (4600, 0.95),   # Ascending RGB
            (3100, 3.36),   # ② Red Giant Tip (Helium Flash, 2300 L_sun)
            (4800, 1.70),   # ③ Horizontal Clump (He core burning, 50 L_sun)
            (3100, 3.72),   # ④ AGB Tip (5200 L_sun)
            (38000, 3.55),  # ⑤ Planetary Nebula hot core
            (41000, 2.15),  # UV turn-down knee
            (22000, -1.30), # Hot White Dwarf (~0.012 R_sun)
            (7200, -3.35),  # ⑥ Cool White Dwarf
        ]
        sun_xy = [(hx(t), hy(l)) for t, l in sun_track]
        sun_len = sum(
            math.hypot(sun_xy[i + 1][0] - sun_xy[i][0], sun_xy[i + 1][1] - sun_xy[i][1])
            for i in range(len(sun_xy) - 1)
        )
        assert sun_len < 1380.0
        sun_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in sun_xy)
        els.append(f'<path d="{sun_d}" fill="none" stroke="#fdba74" stroke-width="2.0" stroke-dasharray="3 3"/>')
        els.append(f'<path d="{sun_d}" class="hr-sun-anim" fill="none" stroke="{ORANGE}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>')

        # Key milestone dots & well-separated Chinese labels on 1 M_sun track
        p1x, p1y = hx(5772), hy(0.0)
        p2x, p2y = hx(3100), hy(3.36)
        p3x, p3y = hx(4800), hy(1.70)
        p4x, p4y = hx(3100), hy(3.72)
        p5x, p5y = hx(38000), hy(3.55)
        p6x, p6y = hx(7200), hy(-3.35)

        els.append(f'<circle cx="{p1x:.1f}" cy="{p1y:.1f}" r="5" fill="#f59e0b" stroke="#ffffff" stroke-width="1.3"/>')
        els.append(txt(p1x - 10, p1y + 16, "① 太阳主序 (100亿年)", 10.0, INK, anchor="end", weight="700"))

        els.append(f'<circle cx="{p2x:.1f}" cy="{p2y:.1f}" r="4.5" fill="{RED}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(txt(p2x - 28, p2y + 4, "② 红巨星顶·氦闪 →", 9.9, RED, anchor="end", weight="700"))

        els.append(f'<circle cx="{p3x:.1f}" cy="{p3y:.1f}" r="4.2" fill="{AMBER}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(txt(p3x - 8, p3y + 4, "③ 稳烧氦核 (1亿年)", 9.8, AMBER, anchor="end", weight="700"))

        els.append(f'<circle cx="{p4x:.1f}" cy="{p4y:.1f}" r="4.5" fill="{PURPLE}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(txt(p4x - 8, p4y - 7, "④ 渐近巨星支 AGB", 9.9, PURPLE, anchor="end", weight="700"))

        els.append(f'<circle cx="{p5x:.1f}" cy="{p5y:.1f}" r="4.5" fill="{TEAL}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(txt(p5x + 8, p5y - 10, "⑤ 行星状星云裸核", 9.9, TEAL, weight="700"))

        els.append(f'<circle cx="{p6x:.1f}" cy="{p6y:.1f}" r="5.5" class="hr-wd-pulse" fill="none" stroke="{BLUE}" stroke-width="2"/>')
        els.append(f'<circle cx="{p6x:.1f}" cy="{p6y:.1f}" r="4.0" fill="{BLUE}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(txt(p6x - 8, p6y + 16, "⑥ 白矮星冷却弧 (~地球大)", 10.0, BLUE, anchor="middle", weight="700"))

        # Axis titles
        els.append(txt((px0 + px1) / 2, 558, "← 表面有效温度 T_eff (K) 向左升高（蓝热 · 红冷）", 10.4, INK, anchor="middle", weight="700"))
        els.append(f'<text x="34" y="{(py0 + py1) / 2:.1f}" font-size="10.4" font-weight="700" fill="{INK}" text-anchor="middle" transform="rotate(-90 34 {(py0 + py1) / 2:.1f})">光度 L / L⊙（对数刻度）</text>')

        # Right Panel: Main-Sequence Spendthrift Lifetime Paradox (x=520..740, y=64..582)
        els.append(card(520, 64, 220, 518))
        els.append(pill(532, 74, "B · 恒星寿命“挥霍悖论”", fg=ORANGE, bg=ORANGE_SOFT, w=196))

        els.append('<rect x="532" y="108" width="196" height="74" rx="6" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.3"/>')
        els.append(txt(630, 127, "主序星质光关系：L ∝ M^3.5", 10.6, ORANGE, anchor="middle", weight="700"))
        els.append(txt(630, 146, "寿命 τ ∝ 燃料 M / 消耗率 L", 10.0, BODY, anchor="middle"))
        els.append(txt(630, 166, "⇒ τ_主序 ≈ 100亿年 × M^(-2.5)", 10.4, RED, anchor="middle", weight="700"))

        # 5 representative stars from OpenStax Table 22.1 (log bar of lifetime from 1 Myr to 200 Gyr+)
        life_rows = [
            ("O5 蓝巨星 · 40 M⊙", "仅 ~100 万年！", "燃料多40倍，挥霍快30万倍", 0.14, "#2563eb"),
            ("B0 蓝白星 · 16 M⊙", "~1,000 万年", "恐龙灭绝至今足够死6轮", 0.30, "#0284c7"),
            ("A0 白星 · 3.3 M⊙", "~5 亿年", "如天狼星、织女星近亲", 0.52, "#0d9488"),
            ("G2 太阳 · 1.0 M⊙", "~100 亿年", "已稳烧46亿年，正值壮年", 0.74, "#d97706"),
            ("M 红矮星 · 0.4 M⊙", "~2,000 亿年+", "0.1 M⊙更超万亿年，全对流省油", 1.00, "#dc2626"),
        ]
        y_lf = 198
        for title_s, dur_s, sub_s, frac_w, col_s in life_rows:
            els.append(f'<rect x="532" y="{y_lf}" width="196" height="62" rx="6" fill="#f8fafc" stroke="{BORDER}" stroke-width="1.1"/>')
            els.append(txt(540, y_lf + 17, title_s, 10.2, INK, weight="700"))
            els.append(txt(720, y_lf + 17, dur_s, 10.1, col_s, anchor="end", weight="700"))
            els.append(f'<rect x="540" y="{y_lf + 25}" width="{180 * frac_w:.1f}" height="8" rx="4" fill="{col_s}"/>')
            els.append(txt(540, y_lf + 50, sub_s, 9.8, MUTED))
            y_lf += 70

        els.append(txt(532, 562, "奇观：宇宙才138亿岁，红矮星至今零自然死亡！", 9.8, RED, weight="700"))

        return figure(
            596,
            "赫罗图恒星半径等值线、太阳一生演化动画与大质量恒星寿命挥霍悖论对比图",
            "左侧赫罗图按斯特藩-玻尔兹曼定律精确绘出0.01至1000倍太阳半径斜线、主序星带、25倍太阳质量超巨星轨迹，并以单次CSS动画演示1倍太阳质量从主序星经红巨星氦闪、水平支、渐近巨星支与行星状星云裸核最终冷却为白矮星；右侧列出40倍至0.4倍太阳质量的主序寿命反差。",
            els,
        )

    def _build_red_giant_and_planetary_nebula():
        """SVG 3: Core-envelope mirror expansion, degenerate helium flash, planetary nebula, and Sun's 12.3 Gyr timeline."""
        els = []
        els.extend(
            header(
                "三、核心燃料烧光了，恒星为什么不缩小反而暴涨成百倍大的红巨星？",
                "核壳“跷跷板镜像效应”、1 亿度简并氦闪与行星状星云谢幕（类太阳恒星 0.8–8 M⊙ 晚年机制）",
            )
        )

        # Panel A: Three-step mechanism cards
        els.append(card(20, 64, 720, 266))
        els.append(pill(34, 74, "A · 类太阳恒星晚年三部曲：核缩壳胀镜像 → 1 亿度氦闪 → 吹散行星状星云", fg=RED, bg=RED_SOFT, w=486))

        # Subcard 1: Core-Envelope Mirror Effect (x=34..254)
        els.append('<rect x="34" y="106" width="220" height="210" rx="8" fill="#fff7ed" stroke="#fdba74" stroke-width="1.3"/>')
        els.append(txt(144, 125, "① 核缩壳胀“镜像效应”", 10.8, ORANGE, anchor="middle", weight="700"))
        cx1, cy1 = 144, 186
        els.append(f'<circle cx="{cx1}" cy="{cy1}" r="46" fill="#fecaca" fill-opacity="0.55" stroke="{RED}" stroke-width="1.6" stroke-dasharray="4 2"/>')
        els.append(f'<circle cx="{cx1}" cy="{cy1}" r="18" fill="#fde047" stroke="#ca8a04" stroke-width="2.0"/>')
        els.append(f'<circle cx="{cx1}" cy="{cy1}" r="9" fill="#94a3b8" stroke="#334155" stroke-width="1.5"/>')
        # Outward arrows on envelope, inward note on core
        for ang in (25, 155, 205, 335):
            rad = math.radians(ang)
            els.append(f'<line x1="{cx1 + 23*math.cos(rad):.1f}" y1="{cy1 + 23*math.sin(rad):.1f}" x2="{cx1 + 42*math.cos(rad):.1f}" y2="{cy1 + 42*math.sin(rad):.1f}" stroke="{RED}" stroke-width="1.6"/>')
        els.append(txt(cx1, cy1 + 3, "He", 9.8, "#ffffff", anchor="middle", weight="700"))
        els.append(txt(44, 250, "• 中心氦灰停火 → 引力压迫氦核急缩升温", 9.8, INK, weight="600"))
        els.append(txt(44, 267, "• 紧贴核外的薄氢壳被烤烫，聚变功率飙升", 9.8, RED, weight="700"))
        els.append(txt(44, 284, "  上千倍，巨量辐射把外包层吹胀百余倍！", 9.8, BODY))
        els.append(txt(44, 301, "• 表面积暴增摊凉至 ~3,100 K，发红变巨星", 9.8, MUTED))

        # Subcard 2: 10^8 K Helium Flash & AGB (x=268..490)
        els.append('<rect x="268" y="106" width="222" height="210" rx="8" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.3"/>')
        els.append(txt(379, 125, "② 1 亿度“氦闪”与双壳层 AGB", 10.8, RED, anchor="middle", weight="700"))
        cx2, cy2 = 379, 186
        els.append(f'<circle cx="{cx2}" cy="{cy2}" r="46" fill="#fee2e2" stroke="{RED}" stroke-width="1.5"/>')
        els.append(f'<circle cx="{cx2}" cy="{cy2}" r="25" fill="#fef08a" stroke="{AMBER}" stroke-width="1.6"/>')
        els.append(f'<circle cx="{cx2}" cy="{cy2}" r="14" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(txt(cx2, cy2 + 4, "3α!", 9.8, "#ffffff", anchor="middle", weight="700"))
        els.append(txt(278, 250, "• 简并氦核压到 10⁸ K 点燃 3⁴He → ¹²C", 9.8, INK, weight="600"))
        els.append(txt(278, 267, "• 简并压与温度无关 → 升温不膨胀降压，", 9.8, RED, weight="700"))
        els.append(txt(278, 284, "  几分钟热失控“氦闪”（被厚外层闷住不炸）", 9.8, BODY))
        els.append(txt(278, 301, "• 随后稳烧氦1亿年，再入双壳层AGB二次巨胀", 9.8, MUTED))

        # Subcard 3: Planetary Nebula & C-O White Dwarf (x=504..726)
        els.append('<rect x="504" y="106" width="222" height="210" rx="8" fill="#f0fdfa" stroke="#5eead4" stroke-width="1.3"/>')
        els.append(txt(615, 125, "③ 行星状星云与碳氧白矮星", 10.8, TEAL, anchor="middle", weight="700"))
        cx3, cy3 = 615, 186
        els.append(f'<ellipse cx="{cx3}" cy="{cy3}" rx="46" ry="34" fill="#ccfbf1" stroke="{TEAL}" stroke-width="2.0"/>')
        els.append(f'<ellipse cx="{cx3}" cy="{cy3}" rx="30" ry="21" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5"/>')
        els.append(f'<circle cx="{cx3}" cy="{cy3}" r="5.5" fill="#ffffff" stroke="{BLUE}" stroke-width="2.0"/>')
        els.append(txt(514, 250, "• 逃逸速度骤降，热脉动以 20–30 km/s", 9.8, INK, weight="600"))
        els.append(txt(514, 267, "  抛掉 40%–80% 质量（与行星毫无关系！）", 9.8, TEAL, weight="700"))
        els.append(txt(514, 284, "• 裸露超10万K炽热C-O核紫外电离气壳发光", 9.8, BODY))
        els.append(txt(514, 301, "• 几万年后星云散尽，留下地球大小白矮星", 9.8, MUTED))

        # Panel B: Sun's 12.3-Billion-Year Quantitative Timeline (OpenStax Table 22.4)
        els.append(card(20, 344, 720, 200))
        els.append(pill(34, 354, "B · 太阳（1 M⊙）全生命周期时间账本（非线性阶段刻度 · 数据据 OpenStax Table 22.4）", fg=AMBER, bg=AMBER_SOFT, w=538))

        ty = 426.0
        stages = [
            (46, 174, "今日太阳", "46 亿岁", "1 L⊙ · 1 D⊙", "#f59e0b"),
            (174, 304, "主序星终点", "~100–110 亿岁", "核心氢耗尽", "#d97706"),
            (304, 434, "红巨星极盛", "+13 亿年", "2300 L⊙ · 165 D⊙", "#dc2626"),
            (434, 548, "氦核聚变", "+1 亿年", "50 L⊙ · 10 D⊙", "#ea580c"),
            (548, 654, "AGB 二次巨星", "+2,000 万年", "5200 L⊙ · 180 D⊙", "#7c3aed"),
            (654, 716, "白矮星余生", "数十亿年结晶", "~0.54 M⊙ 固态核", "#0284c7"),
        ]
        els.append(f'<line x1="46" y1="{ty}" x2="716" y2="{ty}" stroke="#cbd5e1" stroke-width="4" stroke-linecap="round"/>')
        for idx, (sx0, sx1, s_title, s_time, s_metric, s_col) in enumerate(stages):
            xm = sx0 if idx == 0 else (sx0 + sx1) / 2.0
            if idx > 0:
                els.append(f'<line x1="{sx0}" y1="{ty}" x2="{sx1}" y2="{ty}" stroke="{s_col}" stroke-width="5"/>')
            els.append(f'<circle cx="{xm:.1f}" cy="{ty}" r="5.5" fill="{s_col}" stroke="#ffffff" stroke-width="1.4"/>')
            if idx % 2 == 0:
                els.append(f'<line x1="{xm:.1f}" y1="{ty - 6}" x2="{xm:.1f}" y2="{ty - 20}" stroke="{s_col}" stroke-width="1.4"/>')
                anch = "start" if idx == 0 else "middle"
                els.append(txt(xm, ty - 34, s_title, 10.2, s_col, anchor=anch, weight="700"))
                els.append(txt(xm, ty - 21, f"{s_time} ({s_metric})", 9.8, BODY, anchor=anch))
            else:
                els.append(f'<line x1="{xm:.1f}" y1="{ty + 6}" x2="{xm:.1f}" y2="{ty + 20}" stroke="{s_col}" stroke-width="1.4"/>')
                anch = "end" if idx == len(stages) - 1 else "middle"
                tx_pos = 724 if idx == len(stages) - 1 else xm
                els.append(txt(tx_pos, ty + 34, s_title, 10.2, s_col, anchor=anch, weight="700"))
                els.append(txt(tx_pos, ty + 49, f"{s_time} ({s_metric})", 9.8, BODY, anchor=anch))

        els.append(txt(34, 528, "地球命运节点：180 倍太阳直径（≈ 0.84 AU，叠加潮汐拖拽）将吞没水星与金星，地球表面早已化作岩浆洋。", 10.0, INK, weight="600"))

        return figure(
            558,
            "类太阳恒星红巨星核缩壳胀镜像效应、1亿度简并氦闪、行星状星云与太阳全寿命时间轴图解",
            "上半部分三步剖解惰性氦核收缩烤热氢壳导致外包层膨胀百倍的镜像效应、1亿度简并氦核3α失控氦闪及抛射外层形成行星状星云与碳氧白矮星；下半部列出太阳从46亿岁壮年到红巨星极盛、氦聚变、AGB二次膨胀及白矮星结晶的定量演化节点。",
            els,
        )

    def _build_massive_onion_and_supernova():
        """SVG 4: >8 M_sun 7-layer onion shell cross-section, ~20 M_sun SN 1987A burning countdown, & <1s core collapse."""
        els = []
        els.extend(
            header(
                "四、大质量恒星（>8 M⊙）的死亡冲刺：硅只烧几天，铁核 0.25 秒自由落体！",
                "七层“洋葱核”聚变加速倒计时、铁峰吸能陷阱与 10⁴⁶ W 中微子暴吹散整颗超巨星（II 型超新星）",
            )
        )

        # Panel A: Left concentric onion shells + Right ~20 M_sun (OpenStax Table 23.2) countdown
        els.append(card(20, 64, 720, 274))
        els.append(pill(34, 74, "A · 临终前的七层“洋葱壳”与 ~20 M⊙ 恒星聚变倒计时（据 SN 1987A / OpenStax Table 23.2）", fg=PURPLE, bg=PURPLE_SOFT, w=552))

        # Left: Concentric onion rings centered at (168, 214)
        ox, oy = 158.0, 214.0
        shells = [
            (102, "#dbeafe", "#2563eb", "H 氢包层"),
            (85, "#e0f2fe", "#0284c7", "He 氦"),
            (69, "#dcfce7", "#16a34a", "C 碳"),
            (54, "#fef9c3", "#ca8a04", "Ne 氖"),
            (40, "#ffedd5", "#ea580c", "O 氧"),
            (26, "#fee2e2", "#dc2626", "Si 硅"),
            (13, "#334155", "#0f172a", "Fe"),
        ]
        for rad_s, fill_s, strk_s, _ in shells:
            els.append(f'<circle cx="{ox}" cy="{oy}" r="{rad_s}" fill="{fill_s}" stroke="{strk_s}" stroke-width="1.3"/>')
        els.append(txt(ox, oy + 4, "Fe", 9.8, "#ffffff", anchor="middle", weight="700"))
        # Staggered leader labels on upper-right quadrant of onion
        onion_tags = [
            (ox, oy - 91, "H"),
            (ox, oy - 75, "He"),
            (ox, oy - 60, "C"),
            (ox, oy - 45, "Ne"),
            (ox, oy - 31, "O"),
            (ox, oy - 18, "Si"),
        ]
        for tx_o, ty_o, t_o in onion_tags:
            els.append(txt(tx_o, ty_o + 3, t_o, 9.8, INK, anchor="middle", weight="700"))
        els.append(txt(ox, 326, "非真实比例剖面：中心铁核仅地球大小！", 9.8, MUTED, anchor="middle"))

        # Right: Accelerating burning countdown table/bars (x=282..726)
        # Convert durations to years for exact log10 bar lengths!
        burn_stages = [
            ("氢聚变 H → He", "4,000 万 K", "800 万年", 8.0e6, "#2563eb"),
            ("氦聚变 3He → C, O", "1.9 亿 K", "100 万年", 1.0e6, "#0284c7"),
            ("碳聚变 C → Ne, Mg", "8.7 亿 K", "2,000 年", 2.0e3, "#16a34a"),
            ("氖聚变（光致蜕变）", "16 亿 K", "6 个月", 0.5, "#ca8a04"),
            ("氧聚变 O → Si, S", "20 亿 K", "1 年", 1.0, "#ea580c"),
            ("硅聚变 Si → Fe 族", "33 亿 K", "仅数天！", 3.0 / 365.25, "#dc2626"),
            ("铁核灾难坍缩", "飙至 2,000 亿 K", "仅 0.25 秒！", 0.25 / (365.25 * 86400.0), "#7f1d1d"),
        ]
        # Verify monotonic temperature increase and silicon << carbon << hydrogen
        assert burn_stages[5][3] < 0.02 and burn_stages[6][3] < 1e-7

        lg_lo, lg_hi = -8.5, 7.2
        bx_bar0, bw_max = 430.0, 192.0
        yr0 = 110.0
        for idx, (b_name, b_temp, b_dur, yr_val, b_col) in enumerate(burn_stages):
            yy = yr0 + idx * 31.0
            w_bar = max(6.0, (math.log10(yr_val) - lg_lo) / (lg_hi - lg_lo) * bw_max)
            els.append(txt(282, yy + 13, b_name, 10.0, INK, weight="700"))
            els.append(f'<rect x="{bx_bar0}" y="{yy + 2}" width="{w_bar:.1f}" height="14" rx="3" fill="{b_col}"/>')
            els.append(txt(bx_bar0 + w_bar + 7, yy + 13, f"{b_dur} ({b_temp})", 9.8, b_col if idx >= 5 else BODY, weight="700" if idx >= 5 else "500"))

        # Panel B: 4-step sub-second supernova physics & SN 1987A proof
        els.append(card(20, 352, 720, 218))
        els.append(pill(34, 362, "B · 为什么最稳定的铁核反而引爆宇宙最猛烈灾难？0.25 秒坍缩与 SN 1987A 中微子实证", fg=RED, bg=RED_SOFT, w=554))

        steps_sn = [
            (
                34,
                "① 铁核吸能抽底 (0 s)",
                RED,
                "#fef2f2",
                [
                    "⁵⁶Fe 处于比结合能峰顶，",
                    "再聚变不放热反而吸热！",
                    "高温光子敲碎铁核，高压",
                    "把电子压进质子 p+e⁻→n+ν_e",
                    "简并支架瞬间抽空！",
                ],
            ),
            (
                208,
                "② 0.25c 撞上核硬墙",
                ORANGE,
                "#fff7ed",
                [
                    "地球大铁核在 ~0.25 秒内",
                    "以 7万km/s (0.25c) 砸成",
                    "<20 km 原中子星！密度达",
                    "2–4×10¹⁴ g/cm³（方糖重",
                    "4亿吨），强核力猛烈反弹！",
                ],
            ),
            (
                382,
                "③ 10⁴⁶ W 中微子重启",
                PURPLE,
                "#faf5ff",
                [
                    "反弹激波原本在半途卡壳，",
                    "但核心涌出 10⁵⁸ 颗中微子",
                    "携 99% 引力能（功率超",
                    "10亿个星系总星光！）只需",
                    "吸收 ~1% 即炸碎整颗巨星！",
                ],
            ),
            (
                556,
                "④ SN 1987A 提前报信",
                TEAL,
                "#f0fdfa",
                [
                    "中微子秒穿恒星，激波几",
                    "小时后才冲破星表发光：",
                    "1987年地下探测器提前数",
                    "小时截获19+颗中微子；2024",
                    "韦布望远镜揪出中心中子星！",
                ],
            ),
        ]
        for sx, stitle, scol, sbg, slines in steps_sn:
            els.append(f'<rect x="{sx}" y="396" width="168" height="160" rx="7" fill="{sbg}" stroke="{scol}" stroke-width="1.3"/>')
            els.append(txt(sx + 84, 415, stitle, 10.2, scol, anchor="middle", weight="700"))
            for li, ltxt in enumerate(slines):
                els.append(txt(sx + 9, 437 + li * 21, ltxt, 9.8, INK if li == 4 else BODY, weight="700" if li == 4 else "400"))

        return figure(
            584,
            "大质量恒星七层洋葱核结构、聚变加速倒计时与铁核坍缩II型超新星中微子爆发机制图解",
            "上半部左侧剖解大质量恒星临终前氢、氦、碳、氖、氧、硅包裹地球大小铁核的七层洋葱结构，右侧按SN 1987A实测模型对比从氢聚变800万年到硅聚变仅数天、铁核坍缩仅0.25秒的极端加速；下半部分四步图解铁核电子俘获、四分之一光速坍缩核密度反弹、10的46次方瓦中微子洪流重启激波与SN 1987A实证。",
            els,
        )

    def _build_three_remnants_and_limits():
        """SVG 5: Birth-mass to remnant fate map, 3 stellar corpses, and computed relativistic Chandrasekhar M-R curve."""
        els = []
        els.extend(
            header(
                "五、恒星死后的三具终极遗骸：1.44 与 ~2.2 M⊙ 两道不可逾越的质量极限",
                "白矮星、中子星与黑洞的量子防线对决，以及“越重反而越小”的钱德拉塞卡相对论质径曲线",
            )
        )

        # Panel A: Initial mass -> Remnant map + 3 Remnant cards
        els.append(card(20, 64, 720, 250))
        els.append(pill(34, 74, "A · 初始主序质量（单星近太阳金属丰度）→ 残骸核心质量的三岔路口", fg=TEAL, bg=TEAL_SOFT, w=478))

        # Top initial-mass fate strip
        els.append('<rect x="34" y="104" width="238" height="26" rx="4" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.3"/>')
        els.append('<rect x="276" y="104" width="166" height="26" rx="4" fill="#fef3c7" stroke="#d97706" stroke-width="1.3"/>')
        els.append('<rect x="446" y="104" width="150" height="26" rx="4" fill="#ede9fe" stroke="#6d28d9" stroke-width="1.3"/>')
        els.append('<rect x="600" y="104" width="126" height="26" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.3"/>')

        els.append(txt(153, 121, "初始 0.08–8 M⊙ (~97%恒星) → 白矮星", 9.9, BLUE, anchor="middle", weight="700"))
        els.append(txt(359, 121, "8–20 M⊙ → 中子星", 9.9, ORANGE, anchor="middle", weight="700"))
        els.append(txt(521, 121, "20–140 M⊙ → 黑洞", 9.9, PURPLE, anchor="middle", weight="700"))
        els.append(txt(663, 121, "140–260 M⊙ 炸无残骸", 9.8, RED, anchor="middle", weight="700"))

        # Three side-by-side corpse cards (y=140..302)
        corpses = [
            (
                34,
                "① 白矮星（残核 < 1.44 M⊙）",
                BLUE,
                "#f0f9ff",
                [
                    "• 尺寸：≈ 地球（R ~ 5,000–12,000 km）",
                    "• 密度：~10⁶ g/cm³（1 cm³ ≈ 1 吨）",
                    "• 支撑力：泡利不相容·电子简并压",
                    "• 结局：数十亿年结晶成固态碳氧晶球；",
                    "  双星吸积越 1.44 M⊙ → Ia型超新星全碎！",
                ],
            ),
            (
                268,
                "② 中子星（1.44 ~ 2.17 M⊙）",
                ORANGE,
                "#fffbeb",
                [
                    "• 尺寸：≈ 城市（半径仅 ~11–12 km）",
                    "• 密度：~4×10¹⁴ g/cm³（方糖重4亿吨）",
                    "• 支撑力：中子简并压 + 强核力排斥",
                    "• 特征：守恒缩转成毫秒脉冲星与磁星；",
                    "  双中子星并合炼出宇宙黄金与铂金！",
                ],
            ),
            (
                502,
                "③ 恒星级黑洞（> ~2.2 M⊙）",
                PURPLE,
                "#faf5ff",
                [
                    "• 视界：R_s = 2GM/c² ≈ 3 km × (M/M⊙)",
                    "  （10 M⊙ 黑洞视界半径仅 ~30 km！）",
                    "• 支撑力：彻底归零！强核力也被压垮",
                    "• 本质：引力把时空曲率弯成单向陷阱，",
                    "  事件视界内逃逸速度 > 光速 c。",
                ],
            ),
        ]
        for cx_c, ctitle, ccol, cbg, clines in corpses:
            els.append(f'<rect x="{cx_c}" y="140" width="224" height="162" rx="8" fill="{cbg}" stroke="{ccol}" stroke-width="1.4"/>')
            els.append(txt(cx_c + 112, 160, ctitle, 10.4, ccol, anchor="middle", weight="700"))
            for li, ltxt in enumerate(clines):
                els.append(txt(cx_c + 10, 182 + li * 22, ltxt, 9.8, INK if li == 2 else BODY, weight="700" if li == 2 else "400"))

        # Panel B: Exact Nauenberg-Chandrasekhar Relativistic White-Dwarf Mass-Radius Curve
        els.append(card(20, 328, 720, 226))
        els.append(pill(34, 338, "B · 钱德拉塞卡质径曲线实算：为什么白矮星“越重反而越小”，直到 1.44 M⊙ 归零？", fg=BLUE, bg=BLUE_SOFT, w=532))

        # Exact Nauenberg (1972) analytic relativistic Fermi-gas mass-radius relation (mu_e = 2):
        # R(M) in km, with R_sun = 695,700 km and M_Ch = 1.44 M_sun
        R_SUN_KM = 695_700.0

        def wd_radius_km(m_sol):
            if m_sol >= M_CHANDRA:
                return 0.0
            ratio = m_sol / M_CHANDRA
            # Nauenberg (1972, ApJ 175, 417, Eq. 28): R_0 / mu_e = 0.0225 / 2 R_sun = 0.01125 R_sun (~7,827 km)
            return 0.01125 * R_SUN_KM * ((ratio ** (-2.0 / 3.0) - ratio ** (2.0 / 3.0)) ** 0.5)

        r_04 = wd_radius_km(0.4)
        r_06 = wd_radius_km(0.6)
        r_10 = wd_radius_km(1.0)
        r_135 = wd_radius_km(1.35)
        assert r_04 > r_06 > r_10 > r_135 > 1000.0
        assert 8_000.0 < r_06 < 10_000.0 and 4_500.0 < r_10 < 6_500.0

        gx0, gx1 = 84.0, 446.0
        gy0, gy1 = 378.0, 518.0
        gw, gh = gx1 - gx0, gy1 - gy0

        def wx(m_s):
            return gx0 + (m_s / 1.60) * gw

        def wy(r_km):
            return gy1 - (r_km / 16000.0) * gh

        els.append(f'<rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}" fill="#f8fafc" stroke="{BORDER}" stroke-width="1.2"/>')
        for r_grid in (0, 4000, 8000, 12000, 16000):
            yg = wy(r_grid)
            els.append(f'<line x1="{gx0}" y1="{yg:.1f}" x2="{gx1}" y2="{yg:.1f}" stroke="#e2e8f0" stroke-width="1"/>')
            els.append(txt(gx0 - 6, yg + 4, f"{r_grid:,}", 9.8, MUTED, anchor="end"))

        for m_grid in (0.2, 0.6, 1.0, 1.44):
            xg = wx(m_grid)
            els.append(f'<line x1="{xg:.1f}" y1="{gy0}" x2="{xg:.1f}" y2="{gy1}" stroke="#e2e8f0" stroke-width="1"/>')
            els.append(txt(xg, gy1 + 15, f"{m_grid:g} M⊙", 9.8, RED if m_grid > 1.4 else MUTED, anchor="middle", weight="700" if m_grid > 1.4 else "400"))

        # Earth radius reference line (6,371 km)
        y_earth = wy(6371.0)
        els.append(f'<line x1="{gx0}" y1="{y_earth:.1f}" x2="{gx1}" y2="{y_earth:.1f}" stroke="{GREEN}" stroke-width="1.3" stroke-dasharray="5 3"/>')
        els.append(txt(gx0 + 8, y_earth - 5, "地球半径 6,371 km", 9.8, GREEN, weight="700"))

        # Chandrasekhar vertical wall at 1.44 M_sun
        x_ch = wx(M_CHANDRA)
        els.append(f'<line x1="{x_ch:.1f}" y1="{gy0}" x2="{x_ch:.1f}" y2="{gy1}" stroke="{RED}" stroke-width="2.0" stroke-dasharray="4 2"/>')
        els.append(txt(x_ch - 6, gy0 + 15, "钱德拉塞卡极限 1.44 M⊙", 10.0, RED, anchor="end", weight="700"))

        # Plot M-R curve from 0.22 M_sun to 1.44 M_sun
        mr_pts = []
        for i in range(62):
            mm = 0.22 + (M_CHANDRA - 0.22) * (i / 61.0)
            mr_pts.append(f"{wx(mm):.1f},{wy(wd_radius_km(mm)):.1f}")
        els.append(f'<polyline points="{" ".join(mr_pts)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')

        for m_dot, lbl_dot, anch_d, dx_d, dy_dot in (
            (0.6, "太阳残骸 ~0.54–0.6 M⊙", "start", 8, -7),
            (1.0, "天狼星B ~1.0 M⊙", "end", -10, 14),
            (1.35, "1.35 M⊙ (近月球大)", "end", -12, 13),
        ):
            xd, yd = wx(m_dot), wy(wd_radius_km(m_dot))
            els.append(f'<circle cx="{xd:.1f}" cy="{yd:.1f}" r="4.2" fill="{BLUE}" stroke="#ffffff" stroke-width="1.2"/>')
            els.append(txt(xd + dx_d, yd + dy_dot, lbl_dot, 9.8, INK, anchor=anch_d, weight="600"))

        els.append(txt((gx0 + gx1) / 2, 546, "白矮星质量 M / M⊙", 10.0, INK, anchor="middle", weight="700"))
        els.append(f'<text x="34" y="{(gy0 + gy1) / 2:.1f}" font-size="10.0" font-weight="700" fill="{INK}" text-anchor="middle" transform="rotate(-90 34 {(gy0 + gy1) / 2:.1f})">半径 R (km)</text>')

        # Right physics explanation card (x=462..726)
        els.append('<rect x="462" y="378" width="264" height="162" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.3"/>')
        els.append(txt(474, 398, "19岁船舱里的惊天推导（1930）：", 10.4, ORANGE, weight="700"))
        els.append(txt(474, 419, "1. 低速段：P_简并 ∝ ρ^(5/3) 抗衡引力", 9.9, INK, weight="600"))
        els.append(txt(474, 437, "   ⇒ R ∝ M^(-1/3)：加质量必须把电子", 9.8, BODY))
        els.append(txt(474, 454, "   挤进更小空间抬高动量，越重反而越小！", 9.8, BLUE, weight="700"))
        els.append(txt(474, 475, "2. 相对论危机：电子逼近光速 c 无法再加速，", 9.9, INK, weight="600"))
        els.append(txt(474, 493, "   压强软化为 P ∝ ρ^(4/3)，与引力同阶抵消", 9.8, BODY))
        els.append(txt(474, 511, "   ⇒ 一过 1.44 M⊙，再怎么缩也撑不住！", 9.9, RED, weight="700"))
        els.append(txt(474, 530, "3. 中子星越过 ~2.17 M⊙（TOV极限）同理坍成黑洞。", 9.8, MUTED))

        return figure(
            564,
            "恒星三类死亡遗骸对比与钱德拉塞卡白矮星相对论质量半径反比曲线实算图解",
            "上半部展示初始主序质量通向白矮星、中子星、恒星级黑洞与正负电子对不稳定全毁灭的四条分支，并对比三类致密遗骸的尺寸、密度与量子支撑力；下半部实算白矮星相对论质径曲线，解释非相对论段半径随质量负三分之一次方缩小与1.44倍太阳质量钱德拉塞卡极限归零机制。",
            els,
        )

    @register(
        "stellar-evolution",
        "恒星演化过程五步图解：低温分子云坍缩与0.075太阳质量点火线、赫罗图太阳一生动画与寿命挥霍悖论、红巨星镜像效应与氦闪、大质量洋葱核倒计时与中微子超新星、白矮星中子星黑洞三大遗骸与钱德拉塞卡极限",
        "mechanics_sky",
    )
    def build_stellar_evolution():
        write_svg(SUBDIR, "molecular-cloud-collapse-and-mass-threshold.svg", _build_molecular_cloud_and_threshold())
        write_svg(SUBDIR, "hr-diagram-sun-vs-massive-evolution-tracks.svg", _build_hr_diagram_and_lifetimes())
        write_svg(SUBDIR, "red-giant-mirror-effect-and-planetary-nebula.svg", _build_red_giant_and_planetary_nebula())
        write_svg(SUBDIR, "massive-star-onion-shells-and-core-collapse.svg", _build_massive_onion_and_supernova())
        write_svg(SUBDIR, "three-stellar-corpses-degeneracy-and-limits.svg", _build_three_remnants_and_limits())


_register_stellar_evolution()


def _register_mirror_and_train():
    SUBDIR = "mirror-and-train"
    RED = "#dc2626"
    RED_SOFT = "#fef2f2"
    AMBER = "#b45309"
    AMBER_SOFT = "#fffbeb"
    TEAL = "#0f766e"
    TEAL_SOFT = "#f0fdfa"

    # Quantitative assertions for mirror & railway wheelset physics:
    # 1. Mirror reflection M_z = diag(1, 1, -1), det = -1; 180-deg yaw R_y(pi) = diag(-1, 1, -1), det = +1;
    #    Two perpendicular mirrors M_x * M_z = diag(-1, 1, -1) == R_y(pi), det = +1!
    det_mz = 1 * 1 * (-1)
    det_ry = (-1) * 1 * (-1)
    det_corner2 = (-1) * 1 * (-1)
    assert det_mz == -1 and det_ry == 1 and det_corner2 == 1

    # 2. Curve path difference for 90-deg bend with b0 = 0.75 m: dS = 2 * b0 * (pi/2) = 2.356 m
    b0 = 0.75
    r0 = 0.50
    lam_20 = 0.05   # 1:20 conicity
    lam_40 = 0.025  # 1:40 high-speed conicity
    ds_90 = 2.0 * b0 * (math.pi / 2.0)
    assert abs(ds_90 - 2.35619) < 1e-3

    # 3. Radial curve lateral shift y_R = b0 * r0 / (lam * R): at R = 500 m, lam = 0.05 => y_R = 0.015 m = 15.0 mm
    y_500 = (b0 * r0) / (lam_20 * 500.0)
    assert abs(y_500 - 0.015) < 1e-9

    # 4. Klingel hunting wavelength L_K = 2 * pi * sqrt(b0 * r0 / lam)
    lk_20 = 2.0 * math.pi * math.sqrt((b0 * r0) / lam_20)  # 17.207 m
    lk_40 = 2.0 * math.pi * math.sqrt((b0 * r0) / lam_40)  # 24.335 m
    assert 17.1 < lk_20 < 17.3 and 24.2 < lk_40 < 24.5

    def _line(x1, y1, x2, y2, stroke=HAIRLINE, sw=1.6, dash=None, marker=None, cls=None):
        attrs = [
            f'x1="{x1:.1f}"',
            f'y1="{y1:.1f}"',
            f'x2="{x2:.1f}"',
            f'y2="{y2:.1f}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw}"',
        ]
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        if cls:
            attrs.append(f'class="{cls}"')
        return f'<line {" ".join(attrs)}/>'

    def _poly(pts, stroke, sw=2.2, dash=None, fill="none", cls=None):
        d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        cls_attr = f' class="{cls}"' if cls else ""
        return (
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}{cls_attr}/>'
        )

    # -----------------------------------------------------------------------
    # SVG 1: Mirror Front-Back z-Axis Inversion & Mental Yaw Illusion
    # -----------------------------------------------------------------------
    def _build_mirror_front_back_z():
        els = header(
            "一、镜子根本没分左右！它真正反转的唯一坐标轴是“前后深度 z”",
            "左：东还是东、上还是上，唯独垂直镜面的 z 轴反号 · 右：大脑绕竖轴转身错觉与手性反转（det = -1）",
        )

        # Panel A: Physical Reality (x, y, z) -> (x, y, -z)
        els.append(card(20, 66, 360, 444))
        els.append(pill(32, 78, "A · 光学真相：东仍是东、上仍是上，只翻了前后！", fg=BLUE, bg=BLUE_SOFT, w=336, h=24, size=11.8))

        # Top-down schematic of observer facing mirror at y_mir = 212
        els.append(card(32, 112, 336, 224, rx=8, fill="#f8fafc", stroke=BORDER, sw=1.2))
        # Mirror bar across middle
        els.append(_line(52, 222, 348, 222, stroke=BLUE, sw=4.0))
        for hx in range(60, 346, 18):
            els.append(_line(hx, 222, hx - 8, 212, stroke="#93c5fd", sw=1.3))
        els.append(txt(200, 206, "平面镜 xy 镜面（z = 0）", 11.5, BLUE, "middle", weight="700"))

        # Virtual Image (North of mirror, nose pointing SOUTH back at real person!)
        els.append(card(138, 124, 116, 36, rx=18, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.5, dash="4 3"))
        els.append(txt(196, 146, "镜中虚像 (x, y, -z)", 11.5, ORANGE, "middle", weight="700"))
        # Nose arrow pointing DOWN (+y in SVG = toward mirror = South!)
        els.append(_line(196, 160, 196, 192, stroke=RED, sw=2.4, marker="arr-orange"))
        els.append(txt(208, 182, "鼻尖朝南(-z)", 11.5, RED, weight="700"))
        # West & East hands of virtual image
        els.append(txt(82, 146, "西侧手(-x)", 11.5, SLATE, "middle", weight="600"))
        els.append(txt(320, 146, "东侧手(+x)", 11.5, GREEN, "middle", weight="700"))
        els.append(_line(320, 156, 320, 290, stroke=GREEN, sw=1.5, dash="3 3"))

        # Real Observer (South of mirror, nose pointing NORTH into mirror!)
        els.append(card(138, 286, 116, 36, rx=18, fill=BLUE_SOFT, stroke=BLUE, sw=1.6))
        els.append(txt(196, 308, "真实的你 (x, y, +z)", 11.5, BLUE, "middle", weight="700"))
        # Nose arrow pointing UP (toward mirror = North!)
        els.append(_line(196, 286, 196, 250, stroke=BLUE, sw=2.4, marker="arr-blue"))
        els.append(txt(208, 268, "鼻尖朝北(+z)", 11.5, BLUE, weight="700"))
        els.append(txt(82, 308, "左手在西(-x)", 11.5, SLATE, "middle", weight="600"))
        els.append(txt(320, 308, "右手在东(+x)", 11.5, GREEN, "middle", weight="700"))

        # Side-lying thought experiment box
        els.append(card(32, 348, 336, 148, rx=8, fill=TEAL_SOFT, stroke=TEAL, sw=1.2))
        els.append(txt(44, 370, "费曼一招戳破假象：横躺着照镜子会怎样？", 12.0, TEAL, weight="700"))
        els.append(txt(44, 394, "• 你侧躺在地板上照墙镜：头在左，镜里头仍在左；", 11.5, INK, weight="600"))
        els.append(txt(44, 416, "  右脸朝天花板，镜里右脸依然朝天花板！", 11.5, BODY))
        els.append(txt(44, 440, "• 再站到地板镜上低头看：头在最高处，镜里头反倒", 11.5, BODY))
        els.append(txt(44, 462, "  钻进最深地底——这下居然变成“上下颠倒”了！", 11.5, RED, weight="700"))
        els.append(txt(44, 484, "铁律：镜子永远只翻转垂直镜面的法向轴！", 11.5, TEAL, weight="700"))

        # Panel B: Why Our Brain Blames Left-Right + Chiral Glove Inversion
        els.append(card(394, 66, 346, 444))
        els.append(pill(406, 78, "B · 破案：为什么人类偏偏怪它“左右颠倒”？", fg=PURPLE, bg=PURPLE_SOFT, w=322, h=24, size=11.8))

        # Step 1: Mental Rotation R_y(180)
        els.append(card(406, 112, 322, 184, rx=8, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.2))
        els.append(step_badge(424, 132, 1, fg=PURPLE, bg="#ffffff"))
        els.append(txt(442, 136, "大脑的“绕竖轴转身”默认习惯", 12.0, PURPLE, weight="700"))
        els.append(txt(418, 160, "• 镜子真实干的事：只翻前后 (x, y, z) → (x, y, -z)", 11.5, BLUE, weight="700"))
        els.append(txt(418, 182, "• 大脑拿谁去比对？你默认想象自己绕到镜后，", 11.5, BODY))
        els.append(txt(418, 204, "  【绕头脚竖轴 y 转身 180°】：(x, y, z) → (-x, y, -z)", 11.5, INK, weight="700"))
        els.append(txt(418, 226, "  （绝没人想象自己倒立翻跟头绕腰轴转 180°！）", 11.5, MUTED))
        els.append(txt(418, 250, "• 两者一减：(x, y, -z) 对比 (-x, y, -z) → 只剩 x 反号！", 11.5, RED, weight="700"))
        els.append(txt(418, 272, "• 加之人脸左右对称，大脑便把前后反号栽赃给左右！", 11.5, PURPLE, weight="700"))

        # Step 2: Paper Flip & Glove Chirality (det = -1)
        els.append(card(406, 308, 322, 188, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.2))
        els.append(step_badge(424, 328, 2, fg=ORANGE, bg="#ffffff"))
        els.append(txt(442, 332, "纸片翻面实验 + 右手变左手的拓扑死结", 12.0, ORANGE, weight="700"))
        els.append(txt(418, 356, "• 拿张写字的纸先冲自己，再翻过去照镜子：", 11.5, INK, weight="600"))
        els.append(txt(418, 378, "  绕竖边翻过去 → 字左右反；绕横边翻 → 字上下反！", 11.5, RED, weight="700"))
        els.append(txt(418, 400, "  在透明塑料片上写字直接照，根本不用翻，一分不反！", 11.5, GREEN, weight="700"))
        els.append(txt(418, 426, "• 数学本质：镜像矩阵 det(M) = -1（空间手性反转），", 11.5, INK, weight="700"))
        els.append(txt(418, 448, "  任何三维刚体旋转 det(R) = +1 都转不回去——", 11.5, BODY))
        els.append(txt(418, 470, "  就像右手套唯有“由里往外翻面”才能变成左手套！", 11.5, ORANGE, weight="700"))

        return figure(
            524,
            "平面镜前后z轴反转与大脑绕竖轴转身造成左右颠倒错觉的几何图解",
            "左栏俯视图展示真实观察者面向北照镜时东西手与头脚均不互换，唯独垂直镜面的前后z轴反号；右栏对比镜像变换与绕竖轴180度旋转的坐标差异，结合纸片翻面实验与行列式负一的手性反转阐明左右错觉根源。",
            els,
        )

    # -----------------------------------------------------------------------
    # SVG 2: 90° True Mirror, Apollo Corner-Cube Retroreflector & Wu Parity
    # -----------------------------------------------------------------------
    def _build_corner_mirror_and_parity():
        els = header(
            "二、两面 90° 镜还原别人眼中的真容、阿波罗角反射器与宇宙镜像破缺",
            "左：二次反射 (-1)²=+1 消除左右反像与三面角反射器原路回射 · 右：吴健雄钴-60 实验证伪宇称守恒",
        )

        # Panel A: 90-degree Corner Mirror + 3D Retroreflector
        els.append(card(20, 66, 360, 448))
        els.append(pill(32, 78, "A · 负负得正：90° 双镜“真容镜”与月球角反射器", fg=BLUE, bg=BLUE_SOFT, w=336, h=24, size=11.6))

        # Exact 2D ray trace of 90-degree corner mirror: vertex at (200, 130), arms at +-45 deg!
        # Let Mirror 1 go from (200,130) to (116,214) [normal (1,1)/sqrt2],
        # Mirror 2 go from (200,130) to (284,214) [normal (-1,1)/sqrt2], orthogonal: (1)( -1 ) + (1)(1) = 0!
        # Vertical incoming ray from right eye at x=242, y=248 going UP (0, -1):
        # Hits Mirror 2 at (242, 172) [since y - 130 = x - 200 => y = 172]!
        # Reflects horizontally LEFT (-1, 0) to Mirror 1 at (158, 172) [since y - 130 = 200 - x => x = 158]!
        # Reflects straight DOWN (0, +1) to observer at x=158, y=248! Exact 90-deg reflection geometry!
        els.append(card(32, 112, 336, 198, rx=8, fill="#f8fafc", stroke=BORDER, sw=1.2))
        els.append(_line(200, 126, 114, 212, stroke=BLUE, sw=3.6))
        els.append(_line(200, 126, 286, 212, stroke=BLUE, sw=3.6))
        # Right-angle square symbol at vertex (200, 126) -> points (192,134), (200,142), (208,134)
        els.append(_poly([(192, 134), (200, 142), (208, 134)], stroke=SLATE, sw=1.4))
        els.append(txt(200, 120, "90° 正交双平面镜", 11.5, BLUE, "middle", weight="700"))

        # Exact ray path: (242, 242) -> (242, 168) -> (158, 168) -> (158, 242)
        els.append(_line(242, 242, 242, 168, stroke=ORANGE, sw=2.2))
        els.append(_line(242, 168, 158, 168, stroke=ORANGE, sw=2.2))
        els.append(_line(158, 168, 158, 238, stroke=GREEN, sw=2.2, marker="arr-green"))
        els.append(txt(250, 234, "① 眨右眼光线 ↑", 11.5, ORANGE, weight="700"))
        els.append(txt(150, 234, "↓ ② 对侧回射!", 11.5, GREEN, "end", weight="700"))
        els.append(txt(200, 266, "连翻两次：det = (-1)×(-1) = +1 ≡ 绕竖轴转 180°", 11.5, INK, "middle", weight="700"))
        els.append(txt(200, 290, "看到的正是不反字的衣服与别人眼中真实的你！", 11.5, PURPLE, "middle", weight="700"))

        # 3D Corner-Cube Retroreflector card
        els.append(card(32, 322, 336, 178, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.2))
        els.append(txt(44, 344, "再加第 3 面垂直镜 → 三维角反射器 (x,y,z)→(-x,-y,-z)", 11.6, BLUE, weight="700"))
        els.append(txt(44, 368, "• 无论激光从哪个刁钻角度射入，连弹三次必分毫不差", 11.5, INK, weight="600"))
        els.append(txt(44, 390, "  沿原路平行射回光源（v_out = -v_in）！", 11.5, ORANGE, weight="700"))
        els.append(txt(44, 414, "• 三大硬核应用：① 自行车尾灯与高速路牌夜间反光；", 11.5, BODY))
        els.append(txt(44, 436, "  ② 阿波罗登月留置角反射器，测出月球每年退行 3.8 cm；", 11.5, BODY))
        els.append(txt(44, 458, "  ③ 反面教材：隐身战机严禁出现 90° 机身夹角，", 11.5, RED, weight="700"))
        els.append(txt(44, 480, "     否则会把敌方雷达波原路高亮奉还！", 11.5, BODY))

        # Panel B: Parity Violation (Lee, Yang & Wu Chien-Shiung 1956-1957)
        els.append(card(394, 66, 346, 448))
        els.append(pill(406, 78, "B · 终极追问：物理定律自己分得清镜里和镜外吗？", fg=RED, bg=RED_SOFT, w=322, h=24, size=11.6))

        els.append(card(406, 112, 322, 86, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.1))
        els.append(txt(418, 134, "三大基本力完全“左右盲”（宇称守恒）：", 11.8, GREEN, weight="700"))
        els.append(txt(418, 158, "引力、电磁力与强核力在镜中世界完全合法——", 11.5, BODY))
        els.append(txt(418, 180, "把钟表、行星或电路拍进镜子，造出的机器照常运转。", 11.5, INK, weight="600"))

        # Wu 1956 Co-60 diagram
        els.append(card(406, 210, 322, 196, rx=8, fill="#ffffff", stroke=RED, sw=1.4))
        els.append(txt(567, 232, "1956 圣诞夜惊雷：吴健雄钴-60 极低温实验", 11.8, RED, "middle", weight="700"))

        # Left cylinder: Real Co-60 vs Right cylinder: Mirror Co-60 (vertical mirror at x=567)
        els.append(_line(567, 256, 567, 362, stroke=BLUE, sw=2.4, dash="4 3"))
        els.append(txt(567, 251, "镜像面", 11.5, BLUE, "middle", weight="700"))

        # Real world (left of mirror, cx=484)
        els.append(card(424, 260, 120, 46, rx=10, fill=BLUE_SOFT, stroke=BLUE, sw=1.4))
        els.append(txt(484, 279, "真实 ⁶⁰Co 核", 11.5, BLUE, "middle", weight="700"))
        els.append(txt(484, 297, "电流环 ↺ 逆时针", 11.5, INK, "middle", weight="600"))
        els.append(_line(484, 306, 484, 346, stroke=RED, sw=2.6, marker="arr-orange"))
        els.append(txt(484, 366, "β⁻ 电子大多朝下!", 11.5, RED, "middle", weight="700"))

        # Mirror world (right of mirror, cx=650)
        els.append(card(590, 260, 120, 46, rx=10, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.4, dash="4 3"))
        els.append(txt(650, 279, "镜中 ⁶⁰Co 核", 11.5, ORANGE, "middle", weight="700"))
        els.append(txt(650, 297, "电流环 ↻ 顺时针", 11.5, PURPLE, "middle", weight="700"))
        els.append(_line(650, 306, 650, 346, stroke=RED, sw=2.6, marker="arr-orange"))
        els.append(txt(650, 366, "电子仍朝下(违背!)", 11.5, RED, "middle", weight="700"))

        els.append(txt(567, 394, "旋向反了、电子朝向却不反 ⇒ 镜像世界不存在！", 11.5, INK, "middle", weight="700"))

        # Bottom summary card
        els.append(card(406, 418, 322, 82, rx=8, fill=RED_SOFT, stroke=RED, sw=1.1))
        els.append(txt(418, 440, "• 李政道、杨振宁提出猜想（获 1957 诺奖），吴健雄", 11.5, BODY))
        els.append(txt(418, 462, "  在 <0.01 K 下铁证：【弱核力】天生偏爱“左旋”！", 11.5, RED, weight="700"))
        els.append(txt(418, 484, "  凭此实验，人类终于能通过纯文字教外星人分清左右。", 11.5, INK, weight="600"))

        return figure(
            528,
            "90度正交双镜真容镜、三维角反射器与吴健雄钴60宇称不守恒实验图解",
            "左栏精确追踪光线经90度正交双平面镜二次反射消除手性反转，并说明三维角反射器在阿波罗月球测距与隐身战机中的应用；右栏展示吴健雄1956年极低温钴60弱相互作用β衰变实验如何区分真实世界与镜像世界。",
            els,
        )

    # -----------------------------------------------------------------------
    # SVG 3: Car Differential vs Solid-Axle Train Turning Dilemma
    # -----------------------------------------------------------------------
    def _build_car_diff_vs_train_axle():
        els = header(
            "三、从镜面对称到弯道破缺：没有汽车差速器，焊死在一根铁轴上的火车轮怎么拐弯？",
            "左：90° 弯道内外轨必差 2.36 米与汽车齿轮差速器 · 右：圆柱死轴打滑灾难与“轮缘其实在内侧”真相",
        )

        # Panel A: Curve Path Difference + Car Differential
        els.append(card(20, 66, 360, 440))
        els.append(pill(32, 78, "A · 弯道几何铁律：外轮永远比内轮多跑一截！", fg=BLUE, bg=BLUE_SOFT, w=336, h=24, size=11.8))

        # Concentric quarter-circle track diagram
        cx_c, cy_c = 62.0, 286.0
        for rad, col, sw_r, dsh in [(102, TEAL, 3.0, None), (128, MUTED, 1.3, "4 4"), (154, ORANGE, 3.0, None)]:
            pts = [
                (cx_c + rad * math.cos(math.radians(deg)), cy_c - rad * math.sin(math.radians(deg)))
                for deg in range(0, 91, 5)
            ]
            els.append(_poly(pts, stroke=col, sw=sw_r, dash=dsh))

        els.append(txt(74, 282, "弯心 O", 11.5, INK, weight="700"))
        els.append(_line(cx_c, cy_c, cx_c + 154 * math.cos(math.radians(40)), cy_c - 154 * math.sin(math.radians(40)), stroke=SLATE, sw=1.4))
        els.append(txt(106, 232, "R±b₀", 11.5, SLATE, weight="700"))
        els.append(txt(238, 152, "外轨 S_外 = (R+b₀)θ", 11.5, ORANGE, weight="700"))
        els.append(txt(238, 176, "内轨 S_内 = (R-b₀)θ", 11.5, TEAL, weight="700"))
        els.append(txt(238, 204, "路程差 ΔS = 2b₀θ", 12.0, RED, weight="700"))
        els.append(txt(238, 226, "（与弯道半径 R 无关！）", 11.5, BODY))
        els.append(txt(238, 252, "标准轨距拐 90° 弯：", 11.5, INK, weight="600"))
        els.append(txt(238, 274, "外轮必多走 2.36 米！", 11.8, RED, weight="700"))

        # Car solution box
        els.append(card(32, 312, 336, 178, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.2))
        els.append(txt(44, 334, "汽车的解法：把车轴从中间锯断 + 装齿轮差速器", 11.8, BLUE, weight="700"))
        els.append(txt(44, 358, "• 汽车左右轮胎是等直径圆柱（r_左 = r_右）；", 11.5, BODY))
        els.append(txt(44, 380, "• 唯有靠底盘中央一包精密行星锥齿轮（差速器），允许", 11.5, BODY))
        els.append(txt(44, 402, "  转弯时【外轮转速 ω_外 > 内轮转速 ω_内】才不磨胎。", 11.5, INK, weight="700"))
        els.append(txt(44, 428, "• 但火车一节重载车厢轴重超 20 吨！若锯断车轴塞齿轮：", 11.5, RED, weight="700"))
        els.append(txt(44, 450, "  不仅笨重易碎，还会丧失自动导向能力！", 11.5, BODY))
        els.append(txt(44, 474, "  因此两百年来火车左右轮始终焊死在同一根实心钢轴上！", 11.5, BLUE, weight="700"))

        # Panel B: Two Everyday Misconceptions Debunked
        els.append(card(394, 66, 346, 440))
        els.append(pill(406, 78, "B · 先拆掉两个常见误区：不是圆柱轮，更不靠轮缘硬掰！", fg=RED, bg=RED_SOFT, w=322, h=24, size=11.5))

        # Misconception 1: Cylindrical solid axle
        els.append(card(406, 114, 322, 168, rx=8, fill=RED_SOFT, stroke=RED, sw=1.2))
        els.append(step_badge(424, 134, 1, fg=RED, bg="#ffffff"))
        els.append(txt(442, 138, "误区 ①：若把实心轴做成“平直圆柱轮” ❌", 11.8, RED, weight="700"))
        # Mini schematic of cylindrical wheelset skidding
        els.append(_line(456, 170, 678, 170, stroke=SLATE, sw=5.0))
        els.append(card(444, 150, 20, 40, rx=3, fill="#cbd5e1", stroke=SLATE, sw=1.5))
        els.append(card(670, 150, 20, 40, rx=3, fill="#cbd5e1", stroke=SLATE, sw=1.5))
        els.append(txt(567, 162, "实心钢轴 ω_左 ≡ ω_右", 11.5, INK, "middle", weight="700"))
        els.append(txt(567, 208, "r_左 = r_右 ⇒ 两轮每圈滚过距离死死相等！", 11.5, RED, "middle", weight="700"))
        els.append(txt(418, 230, "• 每拐一个 90° 弯，钢轮就得在钢轨上生生硬搓打滑", 11.5, BODY))
        els.append(txt(418, 252, "  2.36 米！火花四溅、啃毁钢轨，甚至直接爬轨脱线。", 11.5, INK, weight="600"))
        els.append(txt(418, 274, "• 更糟的是直轨稍一偏歪，毫无回正力，一路撞向路基！", 11.5, RED, weight="700"))

        # Misconception 2: Flange steering
        els.append(card(406, 296, 322, 194, rx=8, fill=AMBER_SOFT, stroke=AMBER, sw=1.2))
        els.append(step_badge(424, 316, 2, fg=AMBER, bg="#ffffff"))
        els.append(txt(442, 320, "误区 ②：“靠轮缘卡住钢轨硬拐弯？” ❌", 11.8, AMBER, weight="700"))
        els.append(txt(418, 346, "• 先看位置：火车轮突起的那圈轮缘（Flange）长在", 11.5, BODY))
        els.append(txt(418, 368, "  两根钢轨的【内侧】（绝非外侧！），平时与轨头内侧", 11.5, INK, weight="700"))
        els.append(txt(418, 390, "  留有约 7–10 毫米游隙，正常跑车根本不碰钢轨！", 11.5, BLUE, weight="700"))
        els.append(txt(418, 416, "• 费曼提醒：轮缘只是防脱轨的“最后救命护栏”——", 11.5, AMBER, weight="700"))
        els.append(txt(418, 438, "  一旦轮缘真贴上去硬蹭（如地铁急弯），就会发出", 11.5, BODY))
        els.append(txt(418, 460, "  刺耳欲聋的金属尖啸！日常高速过弯全靠【锥形踏面】", 11.5, GREEN, weight="700"))
        els.append(txt(418, 480, "  在零齿轮条件下自动变径过弯！", 11.5, INK, weight="700"))

        return figure(
            520,
            "弯道内外轨弧长差、汽车差速器与火车实心轮对两大误区对比图解",
            "左栏推导任意半径弯道上外轨比内轨多走2b0乘转角的几何铁律与汽车齿轮差速原理；右栏剖析实心圆柱轮打滑灾难，并澄清火车轮缘位于钢轨内侧且仅作紧急安全护栏的工程事实。",
            els,
        )

    # -----------------------------------------------------------------------
    # SVG 4: Conical Wheelset Self-Steering Geometry (with One-Shot CSS Anim)
    # -----------------------------------------------------------------------
    def _build_conical_wheelset_steering():
        els = header(
            "四、锥形踏面“无齿轮自动变速”：往外横移 15 毫米，死轴瞬间跑出内外差速！",
            "上：内厚外薄 1:20 锥形踏面横移变径截面（含单次横移动画）· 下：纯滚动公式实算与无轮缘过弯极限",
        )

        els.append(
            """<style>
  @keyframes wheelset-shift {
    0%, 16% { transform: translateX(-18px); }
    62%, 100% { transform: translateX(0px); }
  }
  @keyframes radius-callout {
    0%, 35% { opacity: 0.82; }
    68%, 100% { opacity: 1; }
  }
  .ws-shift-anim {
    animation: wheelset-shift 4.2s cubic-bezier(0.22, 0.8, 0.25, 1) 1 forwards;
  }
  .rad-note-anim {
    animation: radius-callout 4.2s ease-out 1 forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .ws-shift-anim, .rad-note-anim {
      animation: none !important;
      transform: none !important;
      opacity: 1 !important;
    }
  }
</style>"""
        )

        # Panel A (Top full-width): Cross-Section of Coned Wheelset Shifting Outward in Left Curve
        els.append(card(20, 66, 720, 260))
        els.append(
            pill(
                32,
                78,
                "A · 迎弯自动变径截面：向左拐弯 → 惯性把轮对往右（外轨）轻推 y_R → 外轮踩粗端、内轮踩细端！",
                fg=BLUE,
                bg=BLUE_SOFT,
                w=696,
                h=24,
                size=11.5,
            )
        )

        # Fixed Rails (Left = Inner Rail at x=212, Right = Outer Rail at x=548)
        for rx_c, r_lbl, r_col in [(212, "左轨（弯道内轨）", TEAL), (548, "右轨（弯道外轨）", ORANGE)]:
            # Rail head + web + foot
            els.append(card(rx_c - 16, 232, 32, 14, rx=4, fill="#64748b", stroke=SLATE, sw=1.4))
            els.append(card(rx_c - 5, 246, 10, 22, rx=1, fill="#94a3b8", stroke=SLATE, sw=1.2))
            els.append(card(rx_c - 24, 268, 48, 10, rx=2, fill="#64748b", stroke=SLATE, sw=1.4))
            els.append(txt(rx_c, 296, r_lbl, 11.5, r_col, "middle", weight="700"))

        els.append(txt(92, 178, "⇐ 弯心在左侧", 12.0, TEAL, "middle", weight="700"))
        els.append(txt(92, 200, "(列车向纸内开)", 11.5, MUTED, "middle"))
        els.append(txt(666, 178, "离心惯性外推 ⇒", 12.0, ORANGE, "middle", weight="700"))
        els.append(txt(666, 200, "横移量 y_R (mm)", 11.5, INK, "middle", weight="700"))

        # Animated Rigid Coned Wheelset Group settled at outward-shifted position (+18px right of rail midpoint!)
        # Rail midpoint = 380; shifted wheelset center = 398!
        # Left wheel spans x = 186..258 (inner flange on RIGHT side of left wheel at x=258..268! Wait:
        # INSIDE of track gauge is BETWEEN the two rails, i.e., x in [212, 548]!
        # YES!! Let's be 1000% geometrically accurate:
        # Track interior (gauge space) is BETWEEN Left Rail (x=212) and Right Rail (x=548)!
        # Therefore:
        # - Left wheel's INNER side (thick cone end + flange!) is on its RIGHT side (around x=254)!
        #   Its OUTER side (thin cone end!) is on its LEFT side (around x=186)!
        #   When wheelset shifts RIGHT (+18px), Left Rail (x=212) contacts Left Wheel closer to its LEFT (thin!) end -> SMALLER radius r_in!
        # - Right wheel's INNER side (thick cone end + flange!) is on its LEFT side (around x=538)!
        #   Its OUTER side (thin cone end!) is on its RIGHT side (around x=606)!
        #   When wheelset shifts RIGHT (+18px), Right Rail (x=548) contacts Right Wheel right next to its LEFT inner shoulder (thick!) -> LARGER radius r_out!
        # DOUBLE CHECK THAT GEOMETRY!
        # Centerd wheelset (shift=0):
        #   Left wheel x = 178..246 (midpoint 212 = Left Rail!), flange at x=246..256 (inside gauge!).
        #   Right wheel x = 514..582 (midpoint 548 = Right Rail!), flange at x=504..514 (inside gauge!).
        # Now shift wheelset RIGHT by +18px (settled state!):
        #   Left wheel x = 196..264, flange at x=264..274 (moved AWAY from Left Rail x=212! Left Rail x=212 now sits near the thin outer edge x=196 -> SMALL radius!).
        #   Right wheel x = 532..600, flange at x=522..532 (moved CLOSER to Right Rail x=548! Right Rail x=548 now sits near the thick inner shoulder x=532 -> LARGE radius!).
        # BINGO!! Look how 100% physically, mechanically, and visually truthful that cross-section is!
        els.append('<g class="ws-shift-anim">')
        # Solid steel axle at y = 174 (connecting left wheel to right wheel)
        els.append(card(184, 168, 428, 12, rx=4, fill="#94a3b8", stroke=SLATE, sw=1.5))
        els.append(txt(398, 158, "同一根实心钢轴（ω_左 = ω_右）", 11.5, INK, "middle", weight="700"))
        els.append(txt(398, 198, "整体向右（外轨）横移 y_R →", 11.5, ORANGE, "middle", weight="700"))

        # Left Wheel (x=196..264): thin on outer left (bottom y=228, top y=120), thick on inner right + inner flange x=264..274
        els.append(
            f'<polygon points="196,120 264,108 264,240 196,228" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>'
        )
        els.append(card(264, 98, 10, 152, rx=4, fill="#bfdbfe", stroke=BLUE, sw=1.6))

        # Right Wheel (x=532..600): inner flange x=522..532 + thick on inner left tapering to thin on outer right
        els.append(card(522, 98, 10, 152, rx=4, fill="#fed7aa", stroke=ORANGE, sw=1.6))
        els.append(
            f'<polygon points="532,108 600,120 600,228 532,240" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.8"/>'
        )
        els.append(txt(398, 126, "← 两轮缘均在轨内侧（留游隙）→", 11.5, PURPLE, "middle", weight="700"))
        els.append("</g>")

        # Contact highlight dots & radius labels at fixed rail positions x=212 and x=548
        els.append('<g class="rad-note-anim">')
        els.append(f'<circle cx="212" cy="231" r="5.2" fill="{TEAL}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(f'<circle cx="548" cy="237" r="5.8" fill="{RED}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(txt(212, 315, "踩外侧细端：r_内 = r₀ - λy_R（一步短）", 11.5, TEAL, "middle", weight="700"))
        els.append(txt(548, 315, "踩内侧粗端：r_外 = r₀ + λy_R（一步长！）", 11.5, RED, "middle", weight="700"))
        els.append("</g>")

        # Panel B (Bottom Left): Pure Rolling Formula & Worked Calculation
        els.append(card(20, 340, 356, 194))
        els.append(pill(32, 352, "B · 纯滚动精确公式与实算：只需横移 15 毫米！", fg=GREEN, bg=GREEN_SOFT, w=332, h=24, size=11.5))
        els.append(txt(34, 392, "• 不打滑条件：(r₀ + λy_R) / (r₀ - λy_R) = (R + b₀) / (R - b₀)", 11.5, INK, weight="700"))
        els.append(txt(34, 416, "• 化简得黄金公式：所需横移 y_R = (b₀ · r₀) / (λ · R)", 11.8, BLUE, weight="700"))
        els.append(txt(34, 442, "• 代入真实列车参数（b₀=0.75 m，r₀=0.50 m，锥度 λ=1/20）：", 11.5, BODY))
        els.append(txt(34, 466, "  过 R=500 m 弯道：y_R = 0.375/25 = 0.015 m = 15 mm！", 11.5, GREEN, weight="700"))
        els.append(txt(34, 490, "• 两轮半径仅差 2λy_R = 1.5 mm，同转一圈就精准补齐弧长差，", 11.5, BODY))
        els.append(txt(34, 512, "  全程零齿轮、零打滑、零轮缘摩擦，丝滑自动拐过弯去！", 11.5, ORANGE, weight="700"))

        # Panel C (Bottom Right): Computed Curve y_R(R) vs Flange Clearance Ceiling
        els.append(card(390, 340, 350, 194))
        els.append(pill(402, 352, "C · 为什么干线悄无声息，地铁急弯却尖叫？", fg=PURPLE, bg=PURPLE_SOFT, w=326, h=24, size=11.5))

        # Mini quantitative chart x in [438..720] (R = 250..2000 m), y in [388..474] (y_R = 0..32 mm)
        gx0, gx1, gy0, gy1 = 438.0, 720.0, 388.0, 474.0
        els.append(_line(gx0, gy1, gx1, gy1, stroke=SLATE, sw=1.4))
        els.append(_line(gx0, gy0, gx0, gy1, stroke=SLATE, sw=1.4))

        def px_r(r_m):
            return gx0 + ((r_m - 250.0) / 1750.0) * (gx1 - gx0)

        def py_mm(mm):
            return gy1 - (min(mm, 32.0) / 32.0) * (gy1 - gy0)

        # Typical ~10 mm flange clearance dashed threshold
        y_clr = py_mm(10.0)
        els.append(_line(gx0, y_clr, gx1, y_clr, stroke=RED, sw=1.4, dash="4 3"))
        els.append(txt(718, y_clr - 6, "轮缘游隙上限 ~10 mm", 11.5, RED, "end", weight="700"))

        # Computed 1:20 curve: y_mm = 1000 * (0.75*0.50)/(0.05*R) = 7500 / R
        pts_y = [(px_r(r_v), py_mm(7500.0 / r_v)) for r_v in range(250, 2001, 35)]
        els.append(_poly(pts_y, stroke=BLUE, sw=2.4))

        # Key dots: R=300m (25mm > 10mm -> flange squeal!) vs R=1000m (7.5mm < 10mm -> pure cone!)
        els.append(f'<circle cx="{px_r(300):.1f}" cy="{py_mm(25.0):.1f}" r="4.2" fill="{RED}"/>')
        els.append(txt(px_r(300) + 8, py_mm(25.0) + 4, "地铁急弯 R=300m (需25mm→撞轮缘尖叫!)", 11.5, RED, weight="700"))

        els.append(f'<circle cx="{px_r(1000):.1f}" cy="{py_mm(7.5):.1f}" r="4.5" fill="{GREEN}"/>')
        els.append(txt(438, 495, "● 绿点：干线 R≥1000 m（横移 ≤7.5 mm，纯锥静音）", 11.5, GREEN, weight="700"))

        els.append(txt(406, 517, "横轴：弯道半径 R (250→2000 m) · 纵轴：所需横移 y_R", 11.5, MUTED))

        return figure(
            548,
            "火车锥形踏面外移变径自动差速截面动画与弯道半径游隙极限实算图",
            "上栏截面精确绘制轮缘位于轨距内侧的内厚外薄1比20锥形轮对，单次动画演示向左转弯时轮对外移使外轮接触大半径、内轮接触小半径；下栏推导纯滚动横移公式并实算弯道半径与10毫米游隙上限的交界。",
            els,
        )

    # -----------------------------------------------------------------------
    # SVG 5: Klingel Hunting Sinusoidal Oscillation & High-Speed Rail Taming
    # -----------------------------------------------------------------------
    def _build_klingel_hunting_and_hsr():
        els = header(
            "五、成也锥面、败也锥面：克林格尔正弦“蛇行运动”与 350 km/h 高铁驯兽术",
            "上：直轨偏心纠偏矫枉过正，实算 1:20 与 1:40 波长曲线 · 下：临界失稳速度与复兴号/新干线三大法宝",
        )

        # Panel A (Top full-width): Exact Klingel Sinusoidal Wave Plot along Straight Track
        els.append(card(20, 66, 720, 224))
        els.append(
            pill(
                32,
                78,
                "A · 克林格尔波长公式 L_K = 2π√(b₀r₀/λ)：直轨上一旦偏心，锥面自回正必然走出正弦波！",
                fg=BLUE,
                bg=BLUE_SOFT,
                w=696,
                h=24,
                size=11.5,
            )
        )

        # Plot x_m in [0..50 m] -> px in [86..712], lateral y in [-8..+8 mm] -> py in [124..232], center y=178
        px0, px1, py_mid, py_amp = 86.0, 712.0, 178.0, 44.0
        # Straight rails & centerline
        els.append(_line(px0, py_mid - 50, px1, py_mid - 50, stroke=SLATE, sw=2.4))
        els.append(_line(px0, py_mid + 50, px1, py_mid + 50, stroke=SLATE, sw=2.4))
        els.append(_line(px0, py_mid, px1, py_mid, stroke=BORDER, sw=1.3, dash="4 4"))
        els.append(txt(54, py_mid - 46, "左轨", 11.5, SLATE, "middle", weight="700"))
        els.append(txt(54, py_mid + 4, "中线", 11.5, MUTED, "middle"))
        els.append(txt(54, py_mid + 54, "右轨", 11.5, SLATE, "middle", weight="700"))

        def x_to_px(xm):
            return px0 + (xm / 50.0) * (px1 - px0)

        # Curve 1: 1:20 ordinary conicity (L_K = 17.21 m)
        pts_20 = [
            (x_to_px(xm), py_mid - py_amp * math.sin(2.0 * math.pi * xm / lk_20))
            for xm in [i * 0.25 for i in range(201)]
        ]
        els.append(_poly(pts_20, stroke=ORANGE, sw=2.5))

        # Curve 2: 1:40 high-speed conicity (L_K = 24.33 m)
        pts_40 = [
            (x_to_px(xm), py_mid - 0.78 * py_amp * math.sin(2.0 * math.pi * xm / lk_40))
            for xm in [i * 0.25 for i in range(201)]
        ]
        els.append(_poly(pts_40, stroke=BLUE, sw=2.5, dash="6 3"))

        # Wavelength bracket for 1:20 from x=0 to x=17.21 m
        x_lk20 = x_to_px(lk_20)
        els.append(_line(px0, 120, x_lk20, 120, stroke=ORANGE, sw=1.8))
        els.append(_line(px0, 115, px0, 125, stroke=ORANGE, sw=1.8))
        els.append(_line(x_lk20, 115, x_lk20, 125, stroke=ORANGE, sw=1.8))
        els.append(txt(0.5 * (px0 + x_lk20), 114, f"1:20 波长 L_K ≈ {lk_20:.1f} m", 11.5, ORANGE, "middle", weight="700"))

        # Legend & axis note at bottom of Panel A
        els.append(txt(42, 254, "橙实线：普速 1:20 锥面（波长 17.2 m，直轨摆动密）", 11.5, ORANGE, weight="700"))
        els.append(txt(406, 254, "蓝虚线：高铁 1:40 缓锥（波长拉长至 24.3 m，摆频降）", 11.5, BLUE, weight="700"))
        els.append(txt(380, 276, "起因：偏左 → 左轮变粗超前右拐回中线 → 回到 y=0 时车头仍斜着（ψ≠0）→ 冲过头偏右，周而复始！", 11.5, INK, "middle", weight="600"))

        # Panel B (Bottom Left): Hunting Critical Speed Crisis
        els.append(card(20, 304, 352, 218))
        els.append(pill(32, 316, "B · 高速噩梦：越过临界速度 v_crit 的蛇行失稳", fg=RED, bg=RED_SOFT, w=328, h=24, size=11.5))
        els.append(txt(34, 358, "• 摆动频率随车速正比飙升：f_K = v / L_K", 11.8, INK, weight="700"))
        els.append(txt(34, 382, "  若 v = 360 km/h (100 m/s) 跑在 17.2 m 波长上：", 11.5, BODY))
        els.append(txt(34, 404, "  轮对每秒钟要左右狂甩近 6 个来回（f_K ≈ 5.8 Hz）！", 11.5, RED, weight="700"))
        els.append(txt(34, 430, "• 低速时：悬挂阻尼吸走能量，正弦摆动几秒就衰减归零；", 11.5, GREEN, weight="600"))
        els.append(txt(34, 454, "• 一旦车速冲破【蛇行临界速度 v_crit】：轮轨蠕滑力反过来", 11.5, RED, weight="700"))
        els.append(txt(34, 476, "  往摆动里泵入能量，振幅失控放大，左右轮缘疯狂撞轨，", 11.5, BODY))
        els.append(txt(34, 498, "  几秒内即可震碎扣件甚至爬轨倾覆！", 11.5, INK, weight="700"))

        # Panel C (Bottom Right): Three Engineering Tricks of 350 km/h High-Speed Rail
        els.append(card(388, 304, 352, 218))
        els.append(pill(400, 316, "C · 350 km/h 高铁怎样同时兼顾“过弯”与“稳跑”？", fg=TEAL, bg=TEAL_SOFT, w=328, h=24, size=11.5))
        els.append(txt(402, 358, "① 削缓等效锥度（如 1:40 磨耗型踏面）：拉长波长 L_K，", 11.5, BLUE, weight="700"))
        els.append(txt(402, 380, "   从源头把蛇行临界速度推高到 400–500 km/h 以上；", 11.5, BODY))
        els.append(txt(402, 406, "② 转向架加装【抗蛇行液压减振器】：像方向盘阻尼器一样", 11.5, TEAL, weight="700"))
        els.append(txt(402, 428, "   专门扼杀高频摇头（yaw），低速过弯慢转却不卡死；", 11.5, BODY))
        els.append(txt(402, 454, "③ 巨型弯道半径 + 外轨超高倾斜：350 km/h 高铁最小弯道", 11.5, PURPLE, weight="700"))
        els.append(txt(402, 476, "   半径达 5000–7000 米，外轨垫高最多 ~175 mm 用重力", 11.5, BODY))
        els.append(txt(402, 498, "   分力抵消离心力，让立起的硬币全程稳如泰山！", 11.5, INK, weight="700"))

        return figure(
            536,
            "克林格尔直轨正弦蛇行波长实算曲线与350公里时速高铁抗蛇行工程图解",
            "上栏实算绘制1比20锥度波长17.2米与1比40缓锥度波长24.3米的正弦蛇行运动轨迹并解释偏心回正过冲机理；下栏剖析高速临界蛇行失稳，并总结削缓锥度、抗蛇行液压减振器与大半径外轨超高三大高铁技术。",
            els,
        )

    @register(
        "mirror-and-train",
        "镜子对称与火车转弯五步图解：平面镜前后z轴反转与手性、90度双镜真容镜与吴健雄宇称破缺、弯道弧长差与实心轮对误区、1比20锥形踏面横移自动差速动画、克林格尔正弦蛇行波长与高铁抗蛇行驯兽术",
        "mechanics_sky",
    )
    def build_mirror_and_train():
        write_svg(SUBDIR, "mirror-front-back-z-axis-and-handedness.svg", _build_mirror_front_back_z())
        write_svg(SUBDIR, "corner-mirror-retroreflector-and-parity-wu.svg", _build_corner_mirror_and_parity())
        write_svg(SUBDIR, "car-differential-vs-solid-axle-train-dilemma.svg", _build_car_diff_vs_train_axle())
        write_svg(SUBDIR, "conical-wheelset-curve-steering-geometry.svg", _build_conical_wheelset_steering())
        write_svg(SUBDIR, "klingel-hunting-oscillation-and-high-speed-rail.svg", _build_klingel_hunting_and_hsr())


_register_mirror_and_train()







