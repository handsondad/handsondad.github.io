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


