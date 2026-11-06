"""Reproduce straightedge/compass lessons with checked Euclidean geometry."""

import math
from pathlib import Path

from generate_kepler_newton_visuals import BLUE, GOLD, INK, RED, dot, line, panel, path, save, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "compass-geometry"
GRAY = "#9cabba"


def point(center, radius, angle):
    return center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)


def distance(a, b):
    return math.dist(a, b)


def frame(title, captions, drawing, notes):
    body = text(36, 50, title, 29)
    body += text(36, 91, "虚线：辅助圆弧或辅助线　实线：本步重点", 22)
    for step, caption in enumerate(captions):
        top = 120 + step * 520
        body += panel(top, 495)
        body += text(48, top + 42, f"{step + 1}  {caption}", 24)
        body += drawing(step, top)
    bottom = 120 + len(captions) * 520
    for i, note in enumerate(notes):
        body += text(36, bottom + 22 + i * 37, note, 22)
    return bottom + len(notes) * 37 + 35, body


def transform(top, scale=145, cx=360, cy=275):
    return lambda p: (cx + p[0] * scale, top + cy - p[1] * scale)


def segment(project, a, b, color=INK, dash=False):
    return line(*project(a), *project(b), color, dash)


def arc(project, center, radius, start=0, end=2 * math.pi, color=GRAY, dash=True):
    return path([
        project(point(center, radius, start + (end - start) * i / 180))
        for i in range(181)
    ], color, 2 if dash else 3, dash)


def label(project, p, name, dx=12, dy=-10, color=INK):
    x, y = project(p)
    return dot(x, y, 5, color) + text(x + dx, y + dy, name, 23, color)


def write(name, title, captions, drawing, notes):
    height, body = frame(title, captions, drawing, notes)
    save(name, height, title, "；".join(captions + notes), body, output_directory=OUT)


def equilateral():
    a, b = (-.6, 0), (.6, 0)
    c = (0, .6 * math.sqrt(3))

    def draw(step, top):
        p = transform(top)
        body = segment(p, a, b, BLUE)
        body += arc(p, a, 1.2, color=BLUE)
        if step >= 1:
            body += arc(p, b, 1.2, color=GOLD)
            body += label(p, c, "C", color=RED)
        if step == 2:
            body += segment(p, a, c, RED) + segment(p, b, c, RED)
        return body + label(p, a, "A", -30, 24) + label(p, b, "B", 12, 24)

    write("equilateral-steps.svg", "① 两个圆，生出一个等边三角形",
          ["圆心 A，开口 AB，画第一个圆", "圆心 B，同样开口，取上方交点 C", "连接 AC、BC，保留底边 AB"],
          draw, ["C 在两圆上：AC = AB，BC = AB。", "所以三边相等；下方交点也能给出另一个解。"])


def perpendicular():
    a, b = (-.6, 0), (.6, 0)
    c, d = (0, math.sqrt(1 - .6**2)), (0, -math.sqrt(1 - .6**2))

    def draw(step, top):
        p = transform(top)
        body = segment(p, a, b, BLUE)
        if step >= 1:
            body += arc(p, a, 1, color=BLUE) + arc(p, b, 1, color=GOLD)
            body += label(p, c, "C", color=RED) + label(p, d, "D", 12, 24, RED)
        if step == 2:
            body += segment(p, (0, -1.15), (0, 1.15), RED)
            body += label(p, (0, 0), "M", 12, 26, RED)
            body += path([p((0, .1)), p((.1, .1)), p((.1, 0))], RED)
        body += label(p, a, "A", -30, 23) + label(p, b, "B", 12, 23)
        body += text(48, top + 465, ["先有线段 AB；还不知道中点在哪里。",
                                   "两圆同半径，且半径大于 AB 的一半。",
                                   "CD 同时完成两个任务：垂直、平分。"][step], 22)
        return body

    write("perpendicular-bisector.svg", "② 不量长度，也能找到正中间",
          ["给定线段 AB", "分别以 A、B 为圆心，等半径交于 C、D", "连接 C、D，与 AB 相交于 M"],
          draw, ["CA = CB，DA = DB：C、D 都到两端等距。", "CD 是垂直平分线，AM = MB，夹角为直角。"])


def angle_bisector():
    o = (0, 0)
    a, b = point(o, 1, math.radians(15)), point(o, 1, math.radians(95))
    c = point(o, 2 * math.cos(math.radians(40)), math.radians(55))

    def draw(step, top):
        p = transform(top, 145, 225, 357)
        body = segment(p, o, point(o, 1.8, math.radians(15)), INK)
        body += segment(p, o, point(o, 1.8, math.radians(95)), INK)
        body += arc(p, o, 1, 0, math.radians(115), BLUE)
        body += label(p, o, "O", -28, 22)
        body += label(p, a, "A", 12, 24) + label(p, b, "B", -32, -8)
        if step >= 1:
            body += arc(p, a, 1, math.radians(45), math.radians(130), BLUE)
            body += arc(p, b, 1, math.radians(-45), math.radians(35), GOLD)
            body += label(p, c, "C", color=RED)
        if step == 2:
            body += segment(p, o, c, RED)
            body += segment(p, a, c, GRAY, True) + segment(p, b, c, GRAY, True)
            body += text(440, top + 377, "两侧都是 40°", 23, RED)
        return body

    write("angle-bisector.svg", "③ 让一个角，沿正中间打开",
          ["圆心 O 的圆弧，截两边于 A、B", "圆心 A、B，同样开口，取内部交点 C", "连接 OC，得到角平分线"],
          draw, ["OA = OB，AC = BC，OC 是共同边。", "两三角形全等，两个小角相等。", "示例原角为 80°；不需要拿量角器测它。"])


def polygons():
    o = (0, 0)
    hexagon = [point(o, 1, math.pi / 2 - i * math.pi / 3) for i in range(6)]
    square = [point(o, 1, math.pi / 2 - i * math.pi / 2) for i in range(4)]

    def draw(step, top):
        p = transform(top, 140)
        body = arc(p, o, 1)
        body += label(p, o, "O", 10, 25)
        if step == 0:
            body += segment(p, (-1.2, 0), (1.2, 0), BLUE)
            body += segment(p, (0, -1.2), (0, 1.2), BLUE)
            body += path([p(v) for v in square + square[:1]], RED, 4)
            for i, v in enumerate(square):
                body += label(p, v, chr(65 + i), 12, -10)
            body += text(48, top + 465, "两条垂直直径 → 四个等长弦 → 正方形", 22)
        else:
            for i, v in enumerate(hexagon):
                body += label(p, v, str(i + 1), 12, -10)
            if step == 1:
                body += arc(p, hexagon[0], 1, math.radians(-165), math.radians(-15), GOLD)
                body += segment(p, o, hexagon[0], BLUE)
                body += segment(p, hexagon[0], hexagon[1], RED)
                body += path([p(v) for v in hexagon + hexagon[:1]], RED, 4)
                body += text(48, top + 465, "每步取新的圆上交点；六条边都等于半径。", 22)
            else:
                for v in hexagon:
                    start = math.atan2(-v[1], -v[0]) - math.pi / 3
                    body += arc(p, v, 1, start, start + 2 * math.pi / 3, BLUE, False)
                body += text(48, top + 465, "圆心是六个顶点；每瓣由两段圆弧围成。", 22)
        return body

    write("square-hexagon-flower.svg", "④ 一个圆，变出方形、六边形与花瓣",
          ["作垂直直径，连接相邻端点", "圆规开口取半径，沿圆周连续取六点", "用六个顶点作圆心，画圆内的弧"],
          draw, ["六边形的秘诀：圆心与相邻顶点构成等边三角形。", "花瓣是相交圆弧的纹样，不是植物结构的模型。"])


def pentagon():
    o, a, t, m = (0, 0), (1, 0), (0, 1), (.5, 0)
    q = (.5 - math.sqrt(5) / 2, 0)
    vertices = [point(o, 1, math.pi / 2 - i * 2 * math.pi / 5) for i in range(5)]
    side = distance(t, q)

    def draw(step, top):
        p = transform(top, 135)
        body = arc(p, o, 1)
        if step < 3:
            body += segment(p, (-1.25, 0), (1.25, 0), GRAY, True)
            body += segment(p, o, t, BLUE)
        labels = [(o, "O", 10, 24), (a, "A", 12, 24), (t, "T", 12, -10)] if step < 3 else [(t, "1", 12, -10)]
        for v, name, dx, dy in labels:
            body += label(p, v, name, dx, dy)
        if step < 2:
            body += label(p, m, "M", 6, 24)
            body += segment(p, m, t, GOLD)
        if step in [1, 2]:
            body += arc(p, m, distance(m, t), math.atan2(1, -.5), math.pi, GOLD)
            body += label(p, q, "Q", -26, 24, RED)
            body += segment(p, t, q, RED)
        if step == 2:
            body += arc(p, t, side, math.radians(-115), math.radians(-35), GOLD)
            body += path([p(v) for v in vertices + vertices[:1]], RED, 4)
            for i, v in enumerate(vertices[1:], 2):
                body += label(p, v, str(i), 12, -10)
        if step == 3:
            body += path([p(v) for v in vertices + vertices[:1]], GRAY, 2, True)
            body += path([p(vertices[i]) for i in [0, 2, 4, 1, 3, 0]], RED, 4)
            for i, v in enumerate(vertices[1:], 2):
                body += label(p, v, str(i), 12, -10)
        body += text(48, top + 465, ["先作垂直半径 OT、OA，再平分 OA。",
                                   "Q 在 O 左侧；TQ 不是半径，是下一步的边长。",
                                   "开口取 TQ，从 T 起逐次取新的圆上交点。",
                                   "连接顺序：1 → 3 → 5 → 2 → 4 → 1。"][step], 22)
        return body

    write("pentagon-steps.svg", "⑤ 五边形：关键是先找到那条弦",
          ["已知圆心 O，取顶点 T，作 OA 的中点 M", "圆心 M、开口 MT，圆弧交左侧直径于 Q", "开口改为 TQ，沿原圆周截出五个顶点",
           "每次跳过一个顶点，连接成规则五角星"],
          draw, ["这是便于操作的现代构造，不逐字照搬《原本》IV.11。", "TQ² = (5 − √5)/2 × 半径²，对应正五边形的边。"])


def square_root():
    a, c, b = (-1, 0), (-.5, 0), (1, 0)
    d = (-.5, math.sqrt(.75))

    def draw(step, top):
        p = transform(top, 175)
        body = segment(p, a, b, BLUE)
        for v, name, dx in [(a, "A", -25), (c, "C", -12), (b, "B", 12)]:
            body += label(p, v, name, dx, 26)
        body += text(228, top + 350, "a = 1", 23, BLUE)
        body += text(403, top + 350, "b = 3", 23, BLUE)
        if step >= 1:
            body += arc(p, (0, 0), 1, 0, math.pi, BLUE)
            body += segment(p, c, (-.5, 1.1), RED)
            body += label(p, d, "D", color=RED)
            body += path([p((-.5, .1)), p((-.4, .1)), p((-.4, 0))], RED)
        if step == 2:
            body += segment(p, a, d, GRAY, True) + segment(p, b, d, GRAY, True)
            body += text(434, top + 189, "CD = √3", 26, RED)
            body += text(48, top + 450, "CD² = AC × CB = 1 × 3；取 CD 为正方形边。", 22)
        return body

    write("geometric-mean.svg", "⑦ 用一个半圆，把长方形变成等面积方形",
          ["把 a、b 首尾接成 AB，接点记为 C", "以 AB 为直径作半圆，在 C 作垂线交于 D", "CD² = a × b，CD 就是所求方形的边长"],
          draw, ["示例 a = 1、b = 3，所以 CD = √3。", "几何按统一比例绘制；单位可以任意指定。", "长方形能这样化方，不代表圆也能精确化方。"])


def thirds():
    a, b = (-1.3, -.7), (1.3, -.7)
    u = [(-1.3 + .45 * i, -.7 + .55 * i) for i in range(1, 4)]
    divisions = [(-1.3 + 2.6 * i / 3, -.7) for i in [1, 2]]

    def draw(step, top):
        p = transform(top, 150, 360, 285)
        body = segment(p, a, b, BLUE) + segment(p, a, u[-1], INK)
        body += label(p, a, "A", -28, 26) + label(p, b, "B", 12, 26)
        for i, v in enumerate(u, 1):
            body += label(p, v, f"P{i}", -35, -8)
        if step >= 1:
            body += segment(p, u[-1], b, GOLD)
        if step == 2:
            for v, endpoint in zip(u[:2], divisions):
                body += segment(p, v, endpoint, RED)
                body += label(p, endpoint, "X" if v == u[0] else "Y", -7, 27, RED)
        body += text(48, top + 448, ["AP1 = P1P2 = P2P3，用圆规保持开口逐次截取。",
                                   "P3B 是两条平行线的方向参照。",
                                   "过 P1、P2 作平行线，可用连续两次作垂线。"][step], 22)
        return body

    write("segment-thirds.svg", "⑧ 三等分一条线：不用读尺上的数字",
          ["从 A 作一条斜射线，连续截取三段等长", "连接第三个点 P3 与端点 B", "过 P1、P2 作 P3B 的平行线，截 AB"],
          draw, ["相似三角形给出 AX : AB = 1 : 3。", "同样可以分成 5 份、7 份；这不是任意角的三等分。"])


def triangle_centers():
    a, b, c = (-1, -.6), (1, -.6), (-.35, 1.15)
    ab, bc, ca = distance(a, b), distance(b, c), distance(c, a)
    perimeter = ab + bc + ca
    inc = tuple((bc * a[i] + ca * b[i] + ab * c[i]) / perimeter for i in [0, 1])
    rin = inc[1] + .6
    circum = (0, (c[0]**2 + c[1]**2 - 1.36) / (2 * (c[1] + .6)))
    rout = distance(circum, a)

    def draw(step, top):
        p = transform(top, 135)
        body = path([p(v) for v in [a, b, c, a]], INK, 3)
        for v, name, dx, dy in [(a, "A", -25, 25), (b, "B", 12, 25), (c, "C", 10, -10)]:
            body += label(p, v, name, dx, dy)
        if step == 0:
            body += segment(p, (-1.3, -.6), (1.3, -.6), BLUE)
            body += segment(p, (0, -1), (0, 1.5), BLUE, True)
            midpoint = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2)
            direction = (-(c[1] - a[1]), c[0] - a[0])
            endpoints = [tuple(midpoint[i] + t * direction[i] for i in [0, 1]) for t in [-.6, .6]]
            body += segment(p, *endpoints, GOLD, True)
            body += arc(p, circum, rout, color=RED, dash=False)
            body += label(p, circum, "O", 12, 24, RED)
            body += text(48, top + 457, "先取两边的垂直平分线；O 到三顶点等距。", 22)
        else:
            for v in [a, b]:
                delta = (inc[0] - v[0], inc[1] - v[1])
                endpoint = (v[0] + 1.7 * delta[0], v[1] + 1.7 * delta[1])
                body += segment(p, v, endpoint, BLUE, True)
            body += arc(p, inc, rin, color=RED, dash=False)
            body += label(p, inc, "I", 12, -10, RED)
            foot = (inc[0], -.6)
            body += segment(p, inc, foot, GOLD)
            body += text(48, top + 457, "圆规开口取 I 到一边的垂距，不是到顶点的距离。", 22)
        return body

    write("triangle-circles.svg", "⑥ 给三角形配两种完全不同的圆",
          ["垂直平分线相交 → 外接圆", "角平分线相交 → 内切圆"],
          draw, ["外接圆穿过顶点；内切圆与三条边相切。", "两种圆心通常不重合；等边三角形是特殊情况。"])
    return a, b, c, inc, rin, circum, rout


def validate():
    a, b, c = (-.6, 0), (.6, 0), (0, .6 * math.sqrt(3))
    assert all(math.isclose(distance(x, y), 1.2, abs_tol=1e-12) for x, y in [(a, b), (b, c), (c, a)])
    for p in [(0, .8), (0, -.8)]:
        assert math.isclose(distance(p, a), distance(p, b), abs_tol=1e-12)
        assert math.isclose(distance(p, a), 1, abs_tol=1e-12)
    o = (0, 0)
    aa, bb = point(o, 1, math.radians(15)), point(o, 1, math.radians(95))
    cc = point(o, 2 * math.cos(math.radians(40)), math.radians(55))
    assert math.isclose(distance(aa, cc), 1, abs_tol=1e-12)
    assert math.isclose(distance(bb, cc), 1, abs_tol=1e-12)
    for count in [4, 5, 6]:
        vertices = [point(o, 1, math.pi / 2 - 2 * math.pi * i / count) for i in range(count)]
        expected = 2 * math.sin(math.pi / count)
        for i in range(count):
            assert math.isclose(distance(vertices[i], vertices[(i + 1) % count]), expected, abs_tol=1e-12)
        if count == 6:
            assert math.isclose(expected, 1, abs_tol=1e-12)
        if count == 5:
            assert math.isclose(distance(vertices[0], vertices[2]) / expected, (1 + math.sqrt(5)) / 2, abs_tol=1e-12)
    q = (.5 - math.sqrt(5) / 2, 0)
    side = distance((0, 1), q)
    assert math.isclose(side, 2 * math.sin(math.pi / 5), abs_tol=1e-12)
    assert math.isclose(side**2, (5 - math.sqrt(5)) / 2, abs_tol=1e-12)
    assert math.isclose(distance(q, (.5, 0)), distance((0, 1), (.5, 0)), abs_tol=1e-12)
    a, c, b, d = (-1, 0), (-.5, 0), (1, 0), (-.5, math.sqrt(.75))
    assert math.isclose(distance(c, d)**2, distance(a, c) * distance(c, b), abs_tol=1e-12)
    assert math.isclose(distance((0, 0), d), 1, abs_tol=1e-12)
    assert math.isclose((d[0] - a[0]) * (d[0] - b[0]) + d[1]**2, 0, abs_tol=1e-12)
    a, b = (-1.3, -.7), (1.3, -.7)
    for i in [1, 2]:
        start = (-1.3 + .45 * i, -.7 + .55 * i)
        end = (-1.3 + 2.6 * i / 3, -.7)
        last = (-1.3 + .45 * 3, -.7 + .55 * 3)
        u, v = (end[0] - start[0], end[1] - start[1]), (b[0] - last[0], b[1] - last[1])
        assert abs(u[0] * v[1] - u[1] * v[0]) < 1e-12
        assert math.isclose(distance(a, end) / distance(a, b), i / 3, abs_tol=1e-12)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    validate()
    for drawing in [equilateral, perpendicular, angle_bisector, polygons, pentagon, square_root, thirds]:
        drawing()
    a, b, c, inc, rin, circum, rout = triangle_centers()
    for p in [a, b, c]:
        assert math.isclose(distance(p, circum), rout, abs_tol=1e-12)
    for p, q in [(a, b), (b, c), (c, a)]:
        cross = abs((q[0] - p[0]) * (inc[1] - p[1]) - (q[1] - p[1]) * (inc[0] - p[0]))
        assert math.isclose(cross / distance(p, q), rin, abs_tol=1e-12)
    print("Generated eight SVGs; equal lengths, angles, polygon closure, parallelism, roots and tangencies verified.")
