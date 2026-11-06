"""Generate six original, numerically checked calculus and orbit diagrams."""

import math
from pathlib import Path

from generate_kepler_newton_visuals import (
    BLUE, GOLD, INK, RED, dot, line, panel, path, save, text,
)


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "calculus-gravity"
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


if __name__ == "__main__":
    main()
