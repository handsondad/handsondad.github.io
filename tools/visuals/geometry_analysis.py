"""Geometry, Projective Geometry, Calculus & Fourier Analysis visual builders."""

import math
from pathlib import Path
from fractions import Fraction
import cmath
from html import escape
import xml.etree.ElementTree as ET

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


@register("compass-geometry", "尺规作图：基本作图、正五边形与三角形圆心", "geometry_analysis")
def build_compass_geometry():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "compass-geometry"

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


@register("monge", "蒙日画法几何：三视图对齐、实长与剖视", "geometry_analysis")
def build_monge():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "monge"

    GRAY = "#8b9cab"

    def heading(number, title):
        return text(36, 49, f"{number} {title}", 29)

    def rows(x, y, values, size=23, step=39, color=INK):
        return "".join(text(x, y + i * step, value, size, color) for i, value in enumerate(values))

    def write(name, height, title, description, body):
        save(name, height, title, description, body, output_directory=OUT)

    def rect(x, y, width, height, fill="none", stroke=INK, weight=3):
        return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" stroke="{stroke}" stroke-width="{weight}"/>'

    def polygon(points, fill="#e1edf4", stroke=INK):
        return f'<polygon points="{" ".join(f"{x:.4f},{y:.4f}" for x,y in points)}" fill="{fill}" stroke="{stroke}" stroke-width="2.5" stroke-linejoin="round"/>'

    def profile(depth=20):
        assert 10 <= depth <= 30
        return [(0, 0), (40, 0), (40, 36), (40-depth, 36), (40-depth, 12), (0, 12)]

    def vertices(depth=20):
        return [(x, y, z) for x in (0, 60) for y, z in profile(depth)]

    def camera(yaw=-55, elevation=30):
        a, e = math.radians(yaw), math.radians(elevation)
        return ((-math.sin(a), math.cos(a), 0),
                (-math.cos(a)*math.sin(e), -math.sin(a)*math.sin(e), math.cos(e)),
                (math.cos(a)*math.cos(e), math.sin(a)*math.cos(e), math.sin(e)))

    def dot3(a, b):
        return sum(x*y for x, y in zip(a, b))

    def project(point, yaw=-55, elevation=30):
        right, up, _ = camera(yaw, elevation)
        p = tuple(v-c for v, c in zip(point, (30, 20, 18)))
        return dot3(p, right), -dot3(p, up)

    def scene(depth=20, cx=360, cy=280, scale=5):
        points = vertices(depth)
        _, _, normal = camera()
        faces = [([0, 1, 2, 3, 4, 5], (-1, 0, 0), "#d8e6ef"),
                 ([6, 7, 8, 9, 10, 11], (1, 0, 0), "#b7cfdf")]
        yz = profile(depth)
        for i, (y, z) in enumerate(yz):
            j = (i+1) % 6
            yn, zn = yz[j]
            faces.append(([i, i+6, j+6, j], (0, zn-z, y-yn),
                          "#e4eff5" if zn == z else "#c9dde9"))
        visible = [f for f in faces if dot3(f[1], normal) > 1e-8]
        visible.sort(key=lambda f: sum(dot3(points[i], normal) for i in f[0])/len(f[0]))
        body = ""
        for ids, _, fill in visible:
            body += polygon([(cx+scale*project(points[i])[0], cy+scale*project(points[i])[1]) for i in ids], fill)
        return body

    def front(ox, oy, scale=4, color=INK):
        return rect(ox, oy-36*scale, 60*scale, 36*scale, stroke=color) + line(ox, oy-12*scale, ox+60*scale, oy-12*scale, color)

    def top(ox, oy, scale=4, depth=20):
        return rect(ox, oy, 60*scale, 40*scale) + line(ox, oy+depth*scale, ox+60*scale, oy+depth*scale)

    def left(ox, oy, scale=4, depth=20):
        return polygon([(ox+(40-y)*scale, oy-z*scale) for y, z in profile(depth)], "none")

    def dim_horizontal(x1, x2, y, label, extension_y):
        mid = (x1+x2)/2
        body = line(x1, extension_y, x1, y+7, GRAY) + line(x2, extension_y, x2, y+7, GRAY)
        body += line(x1, y, x2, y, BLUE)
        body += path([(x1+8, y-4), (x1, y), (x1+8, y+4)], BLUE, 2)
        body += path([(x2-8, y-4), (x2, y), (x2-8, y+4)], BLUE, 2)
        body += rect(mid-23, y-14, 46, 28, "#f3f7fa", "none", 0) + text(mid, y+8, label, 23, BLUE, "middle")
        return body

    def dim_vertical(x, y1, y2, label, extension_x):
        body = line(extension_x, y1, x+7, y1, GRAY) + line(extension_x, y2, x+7, y2, GRAY)
        body += line(x, y1, x, y2, BLUE)
        body += path([(x-4, y1+8), (x, y1), (x+4, y1+8)], BLUE, 2)
        body += path([(x-4, y2-8), (x, y2), (x+4, y2-8)], BLUE, 2)
        body += text(x-10, (y1+y2)/2+8, label, 23, BLUE, "end")
        return body

    def history():
        body = heading("①", "蒙日把空间问题变成可教的办法")
        for i, (year, title, detail) in enumerate([
            ("蒙日以前", "工匠、建筑与工程传统", "投影和空间作图已有长期积累。"),
            ("1765 起", "梅济耶尔工程学校", "蒙日从绘图工作走向空间几何方法。"),
            ("1794—1795", "工程教育与师范讲课", "把画法几何组织成可系统传授的课程。"),
            ("1799", "《画法几何》出版", "根据师范学校讲课内容整理。"),
            ("此后", "工程制图与数字模型", "投影之外，再加入尺寸、公差与制造信息。"),
        ]):
            y = 84+i*126
            body += panel(y, 110) + text(48, y+35, year, 23, BLUE)
            body += text(249, y+35, title, 24) + text(48, y+83, detail, 23)
        body += rows(36, 771, ["不是“蒙日一个人发明了所有机械制图规则”。", "他的重要贡献，是把表示与空间求解连成系统。"], 23)
        write("history.svg", 860, "蒙日与画法几何的历史路标", "从早期工程传统、1765年绘图工作，到1794至1795年教育实践、1799年著作出版及后续工程表达的发展。", body)

    def ambiguity():
        body = heading("②", "正面看一样，零件却可以不同")
        body += text(36, 94, "两个台阶块：总长 60、总深 40、总高 36，底厚 12。", 23)
        body += panel(124, 314) + text(48, 166, "同一个主视图", 25, BLUE)
        body += front(180, 395, 4.5)
        body += text(491, 306, "总高 36", 23) + text(491, 357, "底厚 12", 23)
        body += scene(20, 205, 640, 3.8) + scene(10, 525, 640, 3.8)
        body += text(205, 477, "A：高台深 20", 24, BLUE, "middle")
        body += text(525, 477, "B：高台深 10", 24, RED, "middle")
        body += rows(36, 827, ["观察方向沿深度：位置不同的台阶前沿重叠了。", "这里只说明主视图有歧义；不是透视图或正式零件图。"], 23)
        assert vertices(20) != vertices(10)
        assert set((x, z) for x, _, z in vertices(20)) == set((x, z) for x, _, z in vertices(10))
        write("one-view-two-parts.svg", 922, "相同主视图不能唯一确定台阶深度", "两个尺寸相同而高台深度为20和10毫米的块，在主视图中都有相同外框和底厚分界线；轴测辅助图显示不同三维形状。", body)

    def point_views():
        body = heading("③", "每张正投影，暂时放下一项坐标")
        body += rows(36, 92, ["约定：x 向右，y 向后，z 向上。单位：mm。", "空间中的 P = (30, 20, 25)，三个坐标都要保存。"], 23)
        for i, (title, values, labels) in enumerate([
            ("主视：保留 x、z", (30, 25), ("x", "z")),
            ("俯视：保留 x、y", (30, 20), ("x", "y")),
            ("左视：保留 y、z", (20, 25), ("y", "z")),
        ]):
            yy = 175+i*254
            body += panel(yy, 233) + text(48, yy+37, title, 25, BLUE)
            ox, oy, scale = (360 if i == 2 else 134), yy+199, 4
            direction = -1 if i == 2 else 1
            body += line(ox, oy, ox+direction*234, oy, INK, arrow=True) + line(ox, oy, ox, yy+62, INK, arrow=True)
            px, py = ox+direction*values[0]*scale, oy-values[1]*scale
            body += line(px, oy, px, py, GRAY, True) + line(ox, py, px, py, GRAY, True) + dot(px, py, 7, RED)
            body += text(px+12, py-9, "P", 23, RED)
            body += text(ox+direction*243, oy+8, labels[0], 22) + text(ox-10, yy+67, labels[1], 22, INK, "end")
            body += rows(433, yy+106, [f"{labels[0]} = {values[0]}", f"{labels[1]} = {values[1]}"], 24, 48)
        body += rows(36, 984, ["这里分开展示坐标，不是三视图的纸面布置。", "对应关系正确时，不同投影能把丢掉的信息补回来。"], 23)
        write("point-projections.svg", 1075, "点的三个正投影分别保存两项坐标", "空间点30、20、25的主投影保留x和z，水平投影保留x和y，侧投影保留y和z；此图单独展示坐标，不表示工程视图排布。", body)

    def three_views():
        body = heading("④", "一套三视图，不是三张随便摆的画")
        body += rows(36, 93, ["本图用第一角画法：俯视在下，左视在右。", "仍是 A 块；各视图使用同一比例，单位 mm。"], 23)
        body += text(90, 185, "主视图：长 × 高", 24, BLUE)
        body += text(444, 185, "左视图：深 × 高", 24, BLUE)
        body += front(90, 380) + left(450, 380)
        body += text(90, 446, "俯视图：长 × 深", 24, BLUE) + top(90, 480)
        for x in (90, 330):
            body += line(x, 387, x, 410, GRAY, True) + line(x, 457, x, 473, GRAY, True)
        for z in (0, 12, 36):
            body += line(337, 380-z*4, 443, 380-z*4, GRAY, True)
        body += dot(330, 236, 7, RED) + text(343, 229, "P", 22, RED)
        body += dot(530, 236, 7, RED) + text(541, 229, "P", 22, RED)
        body += dot(330, 560, 7, RED) + text(343, 554, "P", 22, RED)
        body += rows(408, 524, ["P = (60, 20, 36)", "三个 P 是同一角点。", "高台在俯视上半部；", "左视中，高台在左。"], 21, 37)
        body += panel(692, 172)
        body += rows(48, 734, ["长对正：主视、俯视的 x 位置对应。", "高平齐：主视、左视的 z 高度对应。", "宽相等：俯视、左视保存同一段深度。"], 24, 48)
        body += text(36, 909, "虚线是本图的投影辅助线，不是零件的不可见棱边。", 22)
        write("aligned-three-views.svg", 952, "第一角画法下台阶块的三视图与同一角点", "前视长高图、下方俯视长深图、右方左视深高图按同一比例对齐。高台位于物体后半部；所选点60、20、36在三图一一对应。", body)

    def conventions():
        body = heading("⑤", "左视图，到底放左边还是右边？")
        for y, title, order, positions in [
            (90, "第一角画法", "观察者 → 物体 → 投影面",
             [("主视", 205, 200), ("左视", 435, 200), ("俯视", 205, 300)]),
            (510, "第三角画法", "观察者 → 投影面 → 物体",
             [("主视", 330, 770), ("左视", 100, 770), ("俯视", 330, 670)]),
        ]:
            body += panel(y, 393) + text(48, y+42, title, 26, BLUE)
            body += text(48, y+88, order, 24)
            for value, x, top_y in positions:
                body += rect(x, top_y, 170, 72, "#edf4f8", "#9aafbe", 2)
                body += text(x+85, top_y+45, value, 25, INK, "middle")
            body += text(48, y+363, "视图名称由观察方向决定，不由纸面左右决定。", 22)
        body += rows(36, 956, ["两套都可以正确表达；不要在同一套图中混用。", "这是排布示意，不是标准投影法符号。"], 23)
        write("first-third-angle.svg", 1050, "第一角与第三角画法的主俯左视图排布", "第一角俯视位于主视下方、左视在右；第三角俯视在上、左视在左。视图方向名称不因纸面位置变化；此图不绘标准投影符号。", body)

    def true_length():
        body = heading("⑥", "看着短了，不等于零件真的短了")
        body += rows(36, 93, ["一条空间线段：Δx = 30，Δy = 40，Δz = 20。", "正投影只留下两个分量；以下坐标长度单位 mm。"], 23)
        for y, title, a, b, label in [
            (180, "① 主视投影", 30, 20, f"√(30²+20²) ≈ {math.hypot(30,20):.2f}"),
            (456, "② 俯视投影", 30, 40, "√(30²+40²) = 50"),
            (824, "③ 以水平投影为底，再加入高度差", 50, 20, f"真长 = √(50²+20²) ≈ {math.sqrt(2900):.2f}"),
        ]:
            height = 326 if y == 456 else 255
            body += panel(y, height) + text(48, y+39, title, 24, BLUE)
            scale = 4 if y != 456 else 4.5
            ox, oy = 100, y+height-42
            body += path([(ox, oy), (ox+a*scale, oy), (ox+a*scale, oy-b*scale)], GRAY, 2, True)
            body += line(ox, oy, ox+a*scale, oy-b*scale, RED)
            body += text(ox+a*scale/2, oy+30, a, 21, INK, "middle")
            body += text(ox+a*scale+12, oy-b*scale/2+6, b, 21)
            body += text(352, y+height/2+13, label, 21)
        body += rows(36, 1126, ["换到与线段平行的投影面，才能直接看到真长。", "这个直角三角形是求真长的构造，不是零件又多了一条边。"], 23)
        assert math.hypot(50,20) == math.sqrt(30**2+40**2+20**2)
        write("true-length.svg", 1220, "用投影分量构造空间线段的真长", "空间线段三个分量为30、40、20毫米，前视长度约36.06、水平投影50；以50和20构造直角三角形得到真长约53.85毫米。", body)

    def section():
        body = heading("⑦", "剖开不是破坏零件，是把孔说清楚")
        body += text(36, 93, "换一个零件：轴套长 40，外径 30，贯通孔直径 16。", 23)
        body += panel(126, 303) + text(48, 166, "① 外部主视：孔藏在里面", 25, BLUE)
        ox, oy, s = 110, 285, 6
        body += rect(ox, oy-15*s, 40*s, 30*s)
        for z in (-8, 8):
            body += line(ox, oy-z*s, ox+40*s, oy-z*s, GRAY, True)
        body += f'<path d="M88,{oy} H374" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="14 4 2 4"/>'
        body += rows(405, 233, ["粗实线：可见轮廓", "短虚线：孔的暗线", "细点画线：轴线"], 21, 48)
        body += panel(459, 319) + text(48, 499, "② 看端面：A—A 剖切平面通过轴线", 25, BLUE)
        cx, cy = 232, 646
        for r in (90, 48):
            body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="3"/>'
        body += f'<path d="M{cx},{cy-113} V{cy+113}" stroke="{RED}" stroke-width="3" stroke-dasharray="19 5 3 5"/>'
        for yy in (cy-111, cy+111):
            body += line(cx, yy, cx+52, yy, RED, arrow=True)
            body += text(cx-19, yy+7, "A", 22, RED, "end")
        body += rows(405, 604, ["想象沿红线所指", "平面剖开，移去", "朝观察者的半边。"], 22, 42)
        body += panel(808, 324) + text(48, 850, "③ A—A 轴向全剖视：材料画细剖面线，孔留白", 23, BLUE)
        ox, oy = 110, 993
        body += '<defs><pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M-3,3L3,-3M0,12L12,0M9,15L15,9" stroke="#718a9f" stroke-width="1"/></pattern></defs>'
        for lo, hi in ((8,15),(-15,-8)):
            body += rect(ox, oy-hi*s, 40*s, (hi-lo)*s, "url(#hatch)")
        for xx in (ox, ox+40*s):
            body += line(xx, oy-8*s, xx, oy+8*s, INK)
        body += f'<path d="M88,{oy} H374" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="14 4 2 4"/>'
        body += rows(410, 937, ["上下两带是材料。", "中间空白是贯通孔。", "剖面线不是阴影。"], 22, 45)
        body += rows(36, 1181, ["本例剖切通过轴线；剖视不改变原来零件。", "断面只画切到的形状；剖视还表达剖切面后方可见结构。"], 22)
        assert 40*(30-16) == 560
        write("section-and-hole.svg", 1273, "轴套的隐藏线、剖切位置与轴向全剖视", "40毫米长、外径30、孔径16的轴套，外部看孔用短虚线；端面A-A切过轴线，轴向剖视只有上下材料带画剖面线，孔中留白。", body)

    def dimensions():
        body = heading("⑧", "画出形状，还不等于能制造")
        body += text(36, 92, "A 块的名义几何：单位 mm；本图不指定打印比例。", 23)
        body += front(130, 320, 4)
        body += dim_horizontal(130, 370, 366, "60", 328)
        body += dim_vertical(89, 176, 320, "36", 122)
        body += text(138, 139, "主视", 24, BLUE)
        body += left(420, 320, 4)
        body += dim_horizontal(420, 580, 366, "40", 328)
        body += dim_horizontal(420, 500, 140, "20", 169)
        body += dim_vertical(642, 272, 320, "12", 588)
        body += text(430, 416, "左视（深度方向）", 23, BLUE)
        body += panel(462, 345) + text(48, 505, "配合的另一道题：允许做成多大？", 25)
        body += rows(48, 556, ["孔直径：10.000 ～ 10.020 mm", "轴直径： 9.970 ～  9.990 mm"], 25, 50)
        body += rows(48, 684, ["最小直径间隙：10.000 − 9.990 = 0.010 mm", "最大直径间隙：10.020 − 9.970 = 0.050 mm"], 23, 49, BLUE)
        body += rows(36, 859, ["这是尺寸区间的算术例子，不指定某个标准配合代号。", "材料、表面与几何公差等尚未给全，不能直接投产。", "比例与缩放改变纸上长度，不改变标注所规定的数值。"], 22)
        assert math.isclose(10-9.990,.010,abs_tol=1e-12)
        assert math.isclose(10.020-9.970,.050,abs_tol=1e-12)
        write("dimensions-and-fit.svg", 1003, "台阶块的五个独立名义尺寸和尺寸区间的间隙计算", "台阶块总长60、总深40、总高36、高台深20、底厚12毫米；另以孔轴区间说明直径间隙0.010至0.050毫米，不是完整制造图。", body)

    def check_geometry():
        for depth in (10,20,30):
            yz = profile(depth)
            area = sum(yz[i][0]*yz[(i+1)%6][1]-yz[(i+1)%6][0]*yz[i][1] for i in range(6))/2
            assert area == 40*12+depth*24
            for p in vertices(depth):
                for yaw in range(-180,181,30):
                    for el in (0,30,90):
                        right, up, normal = camera(yaw,el)
                        assert math.isclose(dot3(right,right),1,abs_tol=1e-12)
                        assert math.isclose(dot3(up,normal),0,abs_tol=1e-12)
                        for q in vertices(depth):
                            assert math.dist(project(p,yaw,el),project(q,yaw,el)) <= math.dist(p,q)+1e-10
        print("Projection bases, length bounds, stepped profiles, hole section and fit intervals verified.")

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        check_geometry()
        for draw in (history, ambiguity, point_views, three_views, conventions, true_length, section, dimensions):
            draw()
        print("Eight original Monge/engineering-drawing SVGs generated.")

    main()


@register("poncelet", "彭赛列射影几何：无穷远点、交比、对偶与闭合定理", "geometry_analysis")
def build_poncelet():
    OUT = REPO_ROOT / "assets" / "images" / "poncelet"

    def ray_hit(origin, pt, q0, direction):
        vx, vy = pt[0] - origin[0], pt[1] - origin[1]
        det = vx * (-direction[1]) - vy * (-direction[0])
        rx, ry = q0[0] - origin[0], q0[1] - origin[1]
        t = (rx * (-direction[1]) - ry * (-direction[0])) / det
        s = (vx * ry - vy * rx) / det
        return (origin[0] + t * vx, origin[1] + t * vy), s

    def shadow_vanishing():
        # Left panel: exact midpoint M of AB fails to stay midpoint after central projection!
        origin = (142.0, 96.0)
        a_top, m_top, b_top = (108.0, 154.0), (153.0, 154.0), (198.0, 154.0)
        assert abs(math.dist(a_top, m_top) - math.dist(m_top, b_top)) < 1e-9  # AM = MB = 45
        q0, dvec = (48.0, 214.0), (288.0, 62.0)
        ap, sa = ray_hit(origin, a_top, q0, dvec)
        mp, sm = ray_hit(origin, m_top, q0, dvec)
        bp, sb = ray_hit(origin, b_top, q0, dvec)
        assert all(48 <= pt[0] <= 346 and pt[1] <= 284 for pt in (ap, mp, bp))
        am_shadow = math.dist(ap, mp)
        mb_shadow = math.dist(mp, bp)
        ratio_shadow = mb_shadow / am_shadow
        assert ratio_shadow > 1.32  # M' is decidedly NOT the midpoint of A'B'!

        els = header(
            "手电筒照下去，欧氏几何坏了哪两条？中点不再居中，平行线交于一点",
            "中心投影下，不仅线段长度改变，连“两段之比 1:1”都保不住；而地面平行线会在画布地平线上交于“无穷远点”。",
        )

        # Left panel: Midpoint fails
        els.append(card(20, 62, 348, 262))
        els.append(txt(36, 84, "① 尺子正中点 M，投成影子后偏心了！", 13, INK, weight="600"))
        els.append(f'<line x1="82" y1="154" x2="226" y2="154" stroke="{BLUE}" stroke-width="2.0"/>')
        els.append(
            f'<line x1="{q0[0]:.1f}" y1="{q0[1]:.1f}" x2="{q0[0] + dvec[0]:.1f}" y2="{q0[1] + dvec[1]:.1f}" '
            f'stroke="{INK}" stroke-width="2.0"/>'
        )
        for pt_t, pt_b, lbl_t, lbl_b in ((a_top, ap, "A", "A'"), (m_top, mp, "M", "M'"), (b_top, bp, "B", "B'")):
            col = ORANGE if lbl_t == "M" else BLUE
            els.append(
                f'<line x1="{origin[0]}" y1="{origin[1]}" x2="{pt_b[0]:.1f}" y2="{pt_b[1]:.1f}" '
                f'stroke="{col}" stroke-width="1.3" stroke-dasharray="4 3"/>'
            )
            els.append(f'<circle cx="{pt_t[0]:.1f}" cy="{pt_t[1]:.1f}" r="4" fill="{col}"/>')
            els.append(f'<circle cx="{pt_b[0]:.1f}" cy="{pt_b[1]:.1f}" r="4" fill="{col}"/>')
            els.append(txt(pt_t[0] + 3, pt_t[1] - 8, lbl_t, 12, col, weight="700", halo=True))
            els.append(txt(pt_b[0] - 2, pt_b[1] + 16, lbl_b, 12, col, "middle", weight="700", halo=True))

        els.append(f'<circle cx="{origin[0]}" cy="{origin[1]}" r="5" fill="{ORANGE}"/>')
        els.append(txt(origin[0] + 10, origin[1] + 4, "光源 O", 12, ORANGE, weight="600"))
        els.append(txt(130, 148, "45", 11, BLUE, "middle", halo=True))
        els.append(txt(175, 148, "45", 11, BLUE, "middle", halo=True))
        els.append(
            txt(
                36,
                310,
                f"原尺 AM : MB = 1 : 1；斜影 A'M' : M'B' ≈ 1 : {ratio_shadow:.2f}（不再等分）",
                11.3,
                MUTED,
            )
        )

        # Right panel: Parallel rails -> Vanishing point (point at infinity)
        els.append(card(382, 62, 358, 262))
        els.append(txt(398, 84, "② 平行铁轨的归宿：添上“无穷远点” P∞", 13, INK, weight="600"))
        vx, vy = 562, 134  # Horizon vanishing point
        els.append(f'<line x1="404" y1="{vy}" x2="720" y2="{vy}" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="5 3"/>')
        els.append(txt(718, vy + 16, "地平线（无穷远直线）", 10.8, BLUE, "end"))

        rail_l = (434, 274)
        rail_r = (690, 274)
        els.append(f'<line x1="{rail_l[0]}" y1="{rail_l[1]}" x2="{vx}" y2="{vy}" stroke="{INK}" stroke-width="2.2"/>')
        els.append(f'<line x1="{rail_r[0]}" y1="{rail_r[1]}" x2="{vx}" y2="{vy}" stroke="{INK}" stroke-width="2.2"/>')
        # Perspective sleepers (ties): spacing shrinks harmonically as 1/(k+1)!
        for k in range(1, 7):
            u = 1.0 - 1.0 / (0.65 * k + 0.35)
            y_tie = rail_l[1] + u * (vy - rail_l[1])
            xl = rail_l[0] + u * (vx - rail_l[0])
            xr = rail_r[0] + u * (vx - rail_r[0])
            els.append(f'<line x1="{xl:.1f}" y1="{y_tie:.1f}" x2="{xr:.1f}" y2="{y_tie:.1f}" stroke="{MUTED}" stroke-width="1.4"/>')

        els.append(f'<circle cx="{vx}" cy="{vy}" r="5.5" fill="{ORANGE}"/>')
        els.append(txt(vx, vy - 11, "P∞（无穷远交点）", 12, ORANGE, "middle", weight="700", halo=True))
        els.append(txt(398, 294, "• 欧氏几何里得加备注：“两直线相交，平行除外”", 11.3, BODY))
        els.append(txt(398, 312, "• 射影平面补上 P∞ 后：任何两条不同直线都必交于唯一一点！", 11.3, GREEN, weight="600"))

        return figure(
            340,
            "投影打破中点等分与平行铁轨交于无穷远点",
            "左图演示光源O将水平尺上的等分点AM=MB投影到斜面上后A'M'与M'B'不再相等；右图演示平行铁轨与等距枕木在透视投影下汇聚于地平线上的无穷远点P∞。",
            els,
        )

    def cross_ratio(a, b, c, d):
        return ((c - a) * (d - b)) / ((c - b) * (d - a))

    def projection():
        origin = (196.0, 96.0)
        xs = [138.0, 173.0, 213.0, 273.0]  # gaps: 35, 40, 60 (7:8:12) -> CR = 25/18
        top_y = 172.0
        q0, direction = (52.0, 268.0), (298.0, -34.0)
        top = [(x, top_y) for x in xs]
        bottom_s, bottom = [], []
        for pt in top:
            hit, s = ray_hit(origin, pt, q0, direction)
            assert 55 <= hit[0] <= 346 and hit[1] <= 268
            bottom.append(hit)
            bottom_s.append(s)

        cr_top = cross_ratio(*xs)
        cr_bottom = cross_ratio(*bottom_s)
        assert abs(cr_top - 25 / 18) < 1e-12
        assert abs(cr_top - cr_bottom) < 1e-12
        # Also verify via ray angles! sin(AOC)*sin(BOD) / (sin(BOC)*sin(AOD))
        ang = [math.atan2(pt[1] - origin[1], pt[0] - origin[0]) for pt in top]
        cr_angles = (math.sin(ang[2] - ang[0]) * math.sin(ang[3] - ang[1])) / (
            math.sin(ang[2] - ang[1]) * math.sin(ang[3] - ang[0])
        )
        assert abs(abs(cr_angles) - cr_top) < 1e-12

        gaps_top = [xs[i + 1] - xs[i] for i in range(3)]
        length = math.hypot(*direction)
        gaps_bottom = [(bottom_s[i + 1] - bottom_s[i]) * length for i in range(3)]

        els = header(
            "长度和单比都变了，为什么四个点的“交比”却稳如泰山？",
            "秘密不在尺子上，而在光源 O 发出的四束光线夹角里——三角形面积一除，所有到 O 的距离全约掉了。",
        )

        # Left card: Geometry
        els.append(card(20, 62, 356, 276))
        els.append(txt(36, 84, "① 上下两截线的间距全变了，交比却分毫不差", 12.8, INK, weight="600"))
        # Soft shaded triangle OAC to hint the area proof
        els.append(
            f'<polygon points="{origin[0]},{origin[1]} {top[0][0]},{top[0][1]} {top[2][0]},{top[2][1]}" '
            f'fill="{BLUE_SOFT}" fill-opacity="0.55"/>'
        )
        els.append(f'<line x1="56" y1="{top_y}" x2="336" y2="{top_y}" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(
            f'<line x1="{q0[0]}" y1="{q0[1]}" x2="{q0[0] + direction[0]}" y2="{q0[1] + direction[1]}" '
            f'stroke="{INK}" stroke-width="1.8"/>'
        )
        for (px, py), (qx, qy), name in zip(top, bottom, "ABCD"):
            els.append(
                f'<line x1="{origin[0]}" y1="{origin[1]}" x2="{qx:.1f}" y2="{qy:.1f}" '
                f'stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="4 3"/>'
            )
            els.append(f'<circle cx="{px}" cy="{py}" r="3.8" fill="{BLUE}"/>')
            els.append(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="3.8" fill="{INK}"/>')
            els.append(txt(px - 2, py - 9, name, 12, BLUE, "middle", weight="700", halo=True))
            els.append(txt(qx + 2, qy + 17, name + "'", 12, INK, "middle", weight="700", halo=True))

        els.append(f'<circle cx="{origin[0]}" cy="{origin[1]}" r="4.8" fill="{ORANGE}"/>')
        els.append(txt(origin[0] + 9, origin[1] + 4, "O", 12.5, ORANGE, weight="700"))
        els.append(
            txt(
                36,
                306,
                f"上间距 {gaps_top[0]:.0f}:{gaps_top[1]:.0f}:{gaps_top[2]:.0f}  →  下间距 {gaps_bottom[0]:.0f}:{gaps_bottom[1]:.0f}:{gaps_bottom[2]:.0f}",
                11.3,
                MUTED,
            )
        )
        els.append(txt(36, 324, f"交比均为 25/18 ≈ {cr_top:.4f}", 11.8, GREEN, weight="700"))

        # Right card: 4-step area cancellation visual walkthrough
        els.append(card(390, 62, 350, 276))
        els.append(txt(406, 84, "② 五行初等几何看懂：为什么它必然不变？", 12.8, INK, weight="600"))
        steps = [
            ("第 1 步：同高三角形面积比 = 底边比", "AC / BC  =  S(△OAC) / S(△OBC)", BLUE_SOFT, BLUE),
            ("第 2 步：换用两边夹角面积公式 ½·a·b·sinθ", "S(△OAC) = ½ · OA · OC · sin∠AOC", SLATE_SOFT, BODY),
            ("第 3 步：把 (AC·BD)/(BC·AD) 四个面积相除", "分子分母里的 ½ 与 OA, OB, OC, OD 全部上下约光！", ORANGE_SOFT, ORANGE),
            ("第 4 步：化简结果只剩四束光线的夹角正弦", "(sin∠AOC · sin∠BOD) / (sin∠BOC · sin∠AOD)", GREEN_SOFT, GREEN),
        ]
        for i, (st_head, st_eq, bg_c, fg_c) in enumerate(steps):
            sy = 98 + i * 51
            els.append(card(406, sy, 318, 43, rx=7, fill=bg_c, stroke=fg_c if i in (0, 2, 3) else BORDER))
            els.append(txt(418, sy + 16, st_head, 11.3, INK, weight="600"))
            els.append(txt(418, sy + 34, st_eq, 11.3, fg_c, weight="600" if i >= 2 else None))

        els.append(txt(406, 322, "⇒ 既然只取决于光线夹角，底下斜线怎么摆都改不了交比！", 11.3, GREEN, weight="600"))

        return figure(
            354,
            "交比投影不变性与三角形面积约分原理",
            "左侧展示四点A、B、C、D经点O投影到斜线后相邻间距比改变但交比同为25/18；右侧分四步展示利用同高三角形面积与正弦面积公式约去OA、OB、OC、OD的过程。",
            els,
        )

    def line_circle(p, angle, radius):
        ux, uy = math.cos(angle), math.sin(angle)
        b = p[0] * ux + p[1] * uy
        c = p[0] ** 2 + p[1] ** 2 - radius**2
        disc = b * b - c
        assert disc > 0
        root = math.sqrt(disc)
        return [(p[0] + t * ux, p[1] + t * uy) for t in (-b - root, -b + root)]

    def chord_panel(x0, title, scale, p, angles, power_expected, note):
        cx, cy, radius = x0 + 174, 198, 5
        els = [
            card(x0, 62, 352, 266),
            txt(x0 + 16, 84, title, 13, INK, weight="600"),
            f'<circle cx="{cx}" cy="{cy}" r="{radius * scale}" fill="{BLUE_SOFT}" fill-opacity="0.55" stroke="{BLUE}" stroke-width="1.8"/>',
            f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{MUTED}"/>',
            txt(cx - 6, cy + 14, "O", 11, MUTED, "end"),
        ]
        pair_names = (("A", "B"), ("C", "D"))
        for idx, (angle, color, (n1, n2)) in enumerate(zip(angles, (ORANGE, GREEN), pair_names)):
            a, b = line_circle(p, angle, radius)
            pa, pb = math.dist(p, a), math.dist(p, b)
            assert abs(pa * pb - power_expected) < 1e-9
            inside = math.dist(a, b) > max(pa, pb) - 1e-9
            ends = (a, b) if inside else (p, a if pa > pb else b)
            dash = ' stroke-dasharray="5 3"' if idx == 1 else ""
            els.append(
                f'<line x1="{cx + ends[0][0] * scale:.1f}" y1="{cy - ends[0][1] * scale:.1f}" '
                f'x2="{cx + ends[1][0] * scale:.1f}" y2="{cy - ends[1][1] * scale:.1f}" '
                f'stroke="{color}" stroke-width="1.8"{dash}/>'
            )
            for q, lbl in ((a, n1), (b, n2)):
                qx, qy = cx + q[0] * scale, cy - q[1] * scale
                ox = (qx - cx) / (radius * scale) * 14
                oy = (qy - cy) / (radius * scale) * 14
                els.append(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="3.6" fill="{color}"/>')
                els.append(txt(qx + ox, qy + oy + 4, lbl, 11.5, color, "middle", weight="700", halo=True))

        px, py = cx + p[0] * scale, cy - p[1] * scale
        els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.8" fill="{INK}"/>')
        els.append(txt(px + 8, py + 16, "P", 12.5, INK, weight="700", halo=True))
        els.append(pill(x0 + 16, 294, note, fg=BLUE if power_expected == 21 else ORANGE, bg=BLUE_SOFT if power_expected == 21 else ORANGE_SOFT, w=320, h=22, size=11.5))
        return els

    def continuity():
        els = header(
            "彭赛列的“连续性原理”：当点 P 从圆内一路走出圆外，定律并没有断掉",
            "圆半径 R = 5。无论过 P 画哪条线，两交点到 P 的距离乘积始终等于 |R² − OP²|（相交弦定理 ↔ 割线定理）。",
        )
        els += chord_panel(
            20,
            "① P 在圆内（OP = 2）：相交弦定理",
            16.5,
            (2.0, 0.0),
            (math.radians(52), math.radians(132)),
            21,
            "PA × PB = PC × PD = 5² − 2² = 21",
        )
        away = math.pi
        els += chord_panel(
            388,
            "② P 移到圆外（OP = 7）：自动变成割线定理",
            16.5,
            (7.0, 0.0),
            (away - math.radians(13), away + math.radians(22)),
            24,
            "PA × PB = PC × PD = 7² − 5² = 24",
        )
        return figure(
            344,
            "相交弦定理与割线定理的连续过渡",
            "左图点P在半径5的圆内距圆心2，两条弦满足PA·PB=PC·PD=21；右图点P移至圆外距圆心7，两条割线仍满足PA·PB=PC·PD=24。",
            els,
        )

    def pole_polar():
        # Circle r = 68 centered at (0,0). Pole P = (128, 0) -> Polar line x = r^2 / 128 = 36.125.
        # Choose Q = (36.125, 76) on P's polar -> Q's polar is 36.125*x + 76*y = r^2, which passes through P=(128,0)!
        r = 62.0
        px_m = 122.0
        x_polar = r * r / px_m
        t_y = math.sqrt(r * r - x_polar * x_polar)
        q_pt = (x_polar, 82.0)
        # Verify La Hire reciprocity: P=(px_m, 0) satisfies q_pt[0]*x + q_pt[1]*y = r^2!
        assert abs(q_pt[0] * px_m + q_pt[1] * 0.0 - r * r) < 1e-9

        els = header(
            "极点与极线：把“点”翻译成“线”，一条定理瞬间买一送一（对偶原理）",
            "给定一个基准圆，平面上每个圆外点 P 都唯一对应一条切点弦 p（极线）；反过来每条线也唯一对应一个极点。",
        )

        # Left panel: Geometric construction of Pole P <-> Polar line p & La Hire reciprocity
        els.append(card(20, 62, 376, 274))
        els.append(txt(36, 84, "① 怎么找极线？过 P 作两条切线，连起两个切点", 12.8, INK, weight="600"))
        cx, cy = 154.0, 210.0
        els.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BLUE_SOFT}" fill-opacity="0.5" stroke="{BLUE}" stroke-width="1.8"/>')
        # Tangents from P to T1, T2
        P_svg = (cx + px_m, cy)
        T1_svg = (cx + x_polar, cy - t_y)
        T2_svg = (cx + x_polar, cy + t_y)
        Q_svg = (cx + q_pt[0], cy - q_pt[1])
        els.append(f'<line x1="{P_svg[0]:.1f}" y1="{P_svg[1]:.1f}" x2="{T1_svg[0]:.1f}" y2="{T1_svg[1]:.1f}" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="{P_svg[0]:.1f}" y1="{P_svg[1]:.1f}" x2="{T2_svg[0]:.1f}" y2="{T2_svg[1]:.1f}" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        # Polar line p (vertical x = cx + x_polar)
        els.append(f'<line x1="{cx + x_polar:.1f}" y1="112" x2="{cx + x_polar:.1f}" y2="298" stroke="{ORANGE}" stroke-width="2.2"/>')
        # Q's polar line q: q_pt[0]*x + q_pt[1]*y = r^2 -> passes through P=(px_m, 0)
        x_left = -68.0
        y_left = (r * r - q_pt[0] * x_left) / q_pt[1]
        els.append(
            f'<line x1="{cx + x_left:.1f}" y1="{cy - y_left:.1f}" x2="{cx + px_m + 22:.1f}" '
            f'y2="{cy - (r * r - q_pt[0] * (px_m + 22)) / q_pt[1]:.1f}" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="5 3"/>'
        )

        for sx, sy, lbl, col, dx, dy in (
            (P_svg[0], P_svg[1], "极点 P", ORANGE, 6, 17),
            (T1_svg[0], T1_svg[1], "T₁", BLUE, -18, -4),
            (T2_svg[0], T2_svg[1], "T₂", BLUE, -18, 13),
            (Q_svg[0], Q_svg[1], "Q（在p上）", GREEN, 8, -2),
        ):
            els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4" fill="{col}"/>')
            els.append(txt(sx + dx, sy + dy, lbl, 11.5, col, weight="700", halo=True))
        els.append(txt(cx + x_polar + 8, 294, "P 的极线 p", 11.5, ORANGE, weight="700", halo=True))
        els.append(txt(42, cy - y_left - 6, "Q 的极线 q（必过 P）", 11, GREEN, weight="600", halo=True))
        els.append(txt(36, 320, "奇妙互换：只要点 Q 落在 p 上，Q 的极线 q 就一定反过来穿过 P", 11.2, MUTED))

        # Right panel: The Duality Dictionary
        els.append(card(410, 62, 330, 274))
        els.append(txt(426, 84, "② 射影几何“翻译词典”：点 ↔ 线互换", 12.8, INK, weight="600"))
        rows = [
            ("左半本词典（原命题）", "右半本词典（对偶命题）", SLATE_SOFT, INK),
            ("一个点 P", "一条直线 p", "#ffffff", BODY),
            ("两点连成一条线", "两线交于一个点", "#ffffff", BODY),
            ("三点共线", "三线共点", BLUE_SOFT, BLUE),
            ("圆内接六边形（帕斯卡）", "圆外切六边形（布里昂雄）", GREEN_SOFT, GREEN),
        ]
        for idx, (l_txt, r_txt, bg_c, fg_c) in enumerate(rows):
            ry = 100 + idx * 36
            els.append(card(426, ry, 298, 30, rx=6, fill=bg_c, stroke=BORDER))
            els.append(txt(436, ry + 19, l_txt, 11.2, fg_c, weight="600" if idx in (0, 3, 4) else None))
            els.append(txt(578, ry + 19, "⇄  " + r_txt, 11.2, fg_c, weight="600" if idx in (0, 3, 4) else None))

        els.append(txt(426, 298, "证出左边一条定理，按词典逐词替换，右边定理自动成立——", 11.3, BODY))
        els.append(txt(426, 317, "这就是彭赛列与热尔岗争论并共同奠定的“对偶原理”。", 11.3, ORANGE, weight="600"))

        return figure(
            352,
            "极点极线构造与射影几何点线对偶词典",
            "左图过圆外点P作切线得切点弦p（极线），并在p上取点Q展示Q的极线q必穿过P；右图列出点与线、连线与交点、帕斯卡内接六边形与布里昂雄外切六边形的对偶翻译表。",
            els,
        )

    def step_vertex(v, r_out, r_in, d_shift, sign=1):
        wx, wy = d_shift - v[0], 0.0 - v[1]
        alpha = math.asin(r_in / math.hypot(wx, wy))
        angle = math.atan2(wy, wx) + sign * alpha
        ux, uy = math.cos(angle), math.sin(angle)
        t = -2 * (v[0] * ux + v[1] * uy)
        return (v[0] + t * ux, v[1] + t * uy)

    def bounce_chain(start_angle, r_out, r_in, d_shift, steps=3):
        pts_b = [(r_out * math.cos(start_angle), r_out * math.sin(start_angle))]
        # Pick sign so first step goes clockwise/nicely
        for sign in (-1, 1):
            cand = [pts_b[0]]
            for _ in range(steps):
                cand.append(step_vertex(cand[-1], r_out, r_in, d_shift, sign=sign))
            if abs( d_shift - r_out ) > 0:
                if math.dist(cand[0], cand[-1]) < 1e-7:
                    return cand
        # For non-closing case just use sign = -1
        cand = [pts_b[0]]
        for _ in range(steps):
            cand.append(step_vertex(cand[-1], r_out, r_in, d_shift, sign=-1))
        return cand

    def porism():
        r_out, r_in = 98.0, 39.2  # R = 98, r = 39.2 -> d_euler = sqrt(98^2 - 2*98*39.2) = sqrt(1920.8) ≈ 43.8269
        d_euler = math.sqrt(r_out**2 - 2 * r_out * r_in)
        d_wrong = 20.0  # Does NOT satisfy Euler's formula!

        bad_chain = bounce_chain(math.radians(108), r_out, r_in, d_wrong, 3)
        assert math.dist(bad_chain[0], bad_chain[3]) > 25.0  # Misses closure by a huge gap!

        good_a = bounce_chain(math.radians(106), r_out, r_in, d_euler, 3)
        good_b = bounce_chain(math.radians(212), r_out, r_in, d_euler, 3)
        assert math.dist(good_a[0], good_a[3]) < 1e-8
        assert math.dist(good_b[0], good_b[3]) < 1e-8
        # Verify tangency to inner circle
        for p, q in zip(good_a[:3], good_a[1:]):
            dist_center = abs((q[0] - p[0]) * (0 - p[1]) - (d_euler - p[0]) * (q[1] - p[1])) / math.dist(p, q)
            assert abs(dist_center - r_in) < 1e-8

        anim_css = """
      .trace-a {
        stroke-dasharray: 560;
        stroke-dashoffset: 560;
        animation: drawTri 2.2s ease-out 0.1s 1 forwards;
      }
      @keyframes drawTri {
        to { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .trace-a { animation: none; stroke-dashoffset: 0; }
      }"""

        els = header(
            "彭赛列闭合定理：随便画两圆合不上；一旦合上一次，换任何起点都能合上！",
            "规则：从外圆起点出发作内圆切线，撞到外圆再折返作下一条切线。连走 3 步，能不能回到起点？",
        )

        # Left panel: Wrong circle pair -> FAILS to close
        els.append(card(20, 62, 352, 298))
        els.append(txt(36, 84, "① 随便摆两圆（d = 20）：走三步留出大缺口", 12.8, INK, weight="600"))
        cx1, cy1 = 196.0, 204.0
        els.append(f'<circle cx="{cx1}" cy="{cy1}" r="92" fill="none" stroke="{HAIRLINE}" stroke-width="1.6"/>')
        sc = 92.0 / r_out
        els.append(f'<circle cx="{cx1 + d_wrong * sc:.1f}" cy="{cy1}" r="{r_in * sc:.1f}" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
        b_pts = " ".join(f"{cx1 + x * sc:.1f},{cy1 - y * sc:.1f}" for x, y in bad_chain)
        els.append(f'<polyline points="{b_pts}" fill="none" stroke="{ORANGE}" stroke-width="1.9"/>')
        for idx, (x, y) in enumerate(bad_chain):
            px, py = cx1 + x * sc, cy1 - y * sc
            lbl = f"A{idx}" if idx < 3 else "A₃≠A₀"
            ox = (x / r_out) * 14
            oy = -(y / r_out) * 13
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.8" fill="{ORANGE if idx in (0, 3) else BODY}"/>')
            els.append(txt(px + ox, py + oy + 4, lbl, 11, ORANGE if idx == 3 else INK, "middle", weight="700", halo=True))
        els.append(pill(36, 324, "d² ≠ R² − 2Rr：终点 A₃ 错开起点，无法闭合", fg=ORANGE, bg=ORANGE_SOFT, w=320, h=22, size=11.3))

        # Right panel: Euler pair -> CLOSES from EVERY starting point!
        els.append(card(388, 62, 352, 298))
        els.append(txt(404, 84, "② 满足 d² = R² − 2Rr：换任何起点都精准咬合！", 12.8, INK, weight="600"))
        cx2, cy2 = 564.0, 204.0
        els.append(f'<circle cx="{cx2}" cy="{cy2}" r="92" fill="none" stroke="{HAIRLINE}" stroke-width="1.6"/>')
        els.append(f'<circle cx="{cx2 + d_euler * sc:.1f}" cy="{cy2}" r="{r_in * sc:.1f}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')

        # Second starting point B1..B3 (dashed green, always static reference)
        pts_b2 = " ".join(f"{cx2 + x * sc:.1f},{cy2 - y * sc:.1f}" for x, y in good_b[:3])
        els.append(f'<polygon points="{pts_b2}" fill="none" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="5 3"/>')
        for idx, (x, y) in enumerate(good_b[:3]):
            px, py = cx2 + x * sc, cy2 - y * sc
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.4" fill="{GREEN}"/>')
            els.append(txt(px + (x / r_out) * 14, py - (y / r_out) * 13 + 4, f"B{idx + 1}", 10.5, GREEN, "middle", weight="600", halo=True))

        # Primary starting point A1..A3 (solid blue, animated trace once + clear underlay)
        pts_a = " ".join(f"{cx2 + x * sc:.1f},{cy2 - y * sc:.1f}" for x, y in good_a)
        els.append(f'<polyline points="{pts_a}" fill="none" stroke="{BLUE}" stroke-opacity="0.55" stroke-width="1.8"/>')
        els.append(f'<polyline class="trace-a" points="{pts_a}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
        for idx, (x, y) in enumerate(good_a[:3]):
            px, py = cx2 + x * sc, cy2 - y * sc
            lbl = "A₁(闭合)" if idx == 0 else f"A{idx + 1}"
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.0" fill="{BLUE}"/>')
            els.append(txt(px + (x / r_out) * 15, py - (y / r_out) * 13 + 4, lbl, 11, BLUE, "middle", weight="700", halo=True))

        els.append(pill(404, 324, "蓝实线 A₁A₂A₃ 与绿虚线 B₁B₂B₃ 全部三步合拢", fg=BLUE, bg=BLUE_SOFT, w=320, h=22, size=11.3))

        return figure(
            376,
            "彭赛列闭合定理：不闭合反例与任意起点闭合对比",
            "左图圆心距d=20不满足欧拉条件，从A0出发作三次切线后A3与A0明显错开；右图满足d²=R²−2Rr，实线A1A2A3与虚线B1B2B3从不同起点出发均精确三步闭合。",
            els,
            extra_css=anim_css,
        )

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        for name, content in (
            ("shadow-vanishing", shadow_vanishing()),
            ("cross-ratio", projection()),
            ("chord-secant", continuity()),
            ("pole-polar", pole_polar()),
            ("poncelet-porism", porism()),
        ):
            (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
            print(f"Wrote {name}.svg")

    main()


@register("calculus-foundations", "微积分基础：割线极限、矩形和、基本定理与偏导", "geometry_analysis")
def build_calculus_foundations():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "calculus-foundations"

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

    main()


@register("cauchy", "柯西与分析严格化：误差窄带、柯西列与复变留数", "geometry_analysis")
def build_cauchy():
    OUT = REPO_ROOT / "assets" / "images" / "cauchy"

    def calculus_crisis():
        # Verify damped sequence a_n = 2 + (-0.68)^n enters band |a_n - 2| < 0.22 permanently for n >= 4
        eps = 0.22
        seq = [2.0 + (-0.68) ** k for k in range(1, 10)]
        assert abs(seq[2] - 2.0) > eps and all(abs(v - 2.0) < eps for v in seq[3:])

        els = header(
            "微积分当年闯了什么祸？从“零的鬼魂”到柯西的“任意窄带挑战”",
            "早期微积分一会儿拿 Δx 当非零分母，一会儿又令 Δx=0 抹掉；柯西改用“无限逼近到比任何给定误差都小”立下规矩。",
        )

        # Left panel: Berkeley's critique & Grandi's paradox
        els.append(card(20, 62, 356, 266))
        els.append(txt(36, 84, "① 18 世纪的尴尬：它到底是不是 0？", 13, INK, weight="600"))

        els.append(card(36, 98, 324, 114, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(48, 118, "求 y = x² 切线斜率时的“双重标准”：", 11.8, INK, weight="600"))
        els.append(txt(48, 140, "第1步：((x+Δx)² − x²) / Δx = 2x + Δx", 11.5, BODY))
        els.append(txt(62, 158, "↳ 能放进分母约分，前提是 Δx ≠ 0！", 11.2, ORANGE, weight="600"))
        els.append(txt(48, 179, "第2步：直接擦掉尾巴，宣布斜率 = 2x", 11.5, BODY))
        els.append(txt(62, 197, "↳ 转头又当 Δx = 0！（贝克莱嘲讽：已死量的鬼魂）", 11.2, ORANGE, weight="600"))

        els.append(card(36, 222, 324, 90, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(48, 242, "无穷级数乱加括号的车祸：1 − 1 + 1 − 1 + … = ？", 11.8, INK, weight="600"))
        els.append(txt(48, 263, "• (1−1) + (1−1) + … = 0", 11.3, BODY))
        els.append(txt(48, 282, "• 1 − (1−1) − (1−1) − … = 1    （同一个式子三个答案！）", 11.3, BODY))
        els.append(txt(48, 301, "⇒ 不先定义什么叫“收敛”，无穷求和根本没法算。", 11.2, MUTED))

        # Right panel: Cauchy's Limit Band (epsilon strip)
        els.append(card(390, 62, 350, 266))
        els.append(txt(406, 84, "② 柯西的极限法则：永不除以 0，只看能否锁进窄带", 13, INK, weight="600"))

        ox, oy_mid = 434.0, 196.0
        w_plot = 282.0
        y_scale = 82.0  # 1 unit = 82px around L=2.0
        band_half = eps * y_scale

        # Target epsilon band
        els.append(
            f'<rect x="{ox}" y="{oy_mid - band_half:.1f}" width="{w_plot}" height="{2 * band_half:.1f}" '
            f'fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1" stroke-dasharray="4 3"/>'
        )
        els.append(f'<line x1="{ox}" y1="{oy_mid}" x2="{ox + w_plot}" y2="{oy_mid}" stroke="{GREEN}" stroke-width="1.6"/>')
        els.append(txt(ox - 6, oy_mid + 4, "L", 12, GREEN, "end", weight="700"))
        els.append(txt(ox + w_plot - 4, oy_mid - band_half - 5, "你任意指定窄带 L ± ε", 10.8, GREEN, "end", weight="600"))

        # Cutoff N=4 vertical line
        x_n4 = ox + 3 * (w_plot / 9.2) + 18
        els.append(f'<line x1="{x_n4:.1f}" y1="112" x2="{x_n4:.1f}" y2="268" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="3 3"/>')
        els.append(txt(x_n4 + 5, 124, "从这一步往后，全关进窄带里！", 10.8, BLUE, weight="600"))

        pts_seq = []
        for idx, val in enumerate(seq):
            px = ox + idx * (w_plot / 9.2) + 14
            py = oy_mid - (val - 2.0) * y_scale
            pts_seq.append((px, py))
        poly_s = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts_seq)
        els.append(f'<polyline points="{poly_s}" fill="none" stroke="{HAIRLINE}" stroke-width="1.4"/>')
        for idx, (px, py) in enumerate(pts_seq):
            in_band = idx >= 3
            els.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.0" '
                f'fill="{GREEN if in_band else ORANGE}"/>'
            )

        els.append(txt(406, 290, "柯西的改造：Δx 只是一个不断变小、以 0 为极限的变量，", 11.3, BODY))
        els.append(txt(406, 309, "全程保持 Δx ≠ 0；只要差值能小于任意给定的正数，极限就是 2x！", 11.3, GREEN, weight="600"))

        return figure(
            344,
            "微积分基础危机与柯西极限窄带思想",
            "左图展示早期求导中Δx先作非零除数后又置零的矛盾及1−1+1−1级数歧义；右图展示序列从某步起永远落入任意窄误差带L±ε的柯西极限思想。",
            els,
        )

    def newton_terms(count):
        xs = [Fraction(1)]
        for _ in range(count - 1):
            xs.append((xs[-1] + 2 / xs[-1]) / 2)
        return xs

    def sequence():
        xs = newton_terms(6)
        assert xs[1] == Fraction(3, 2) and xs[2] == Fraction(17, 12) and xs[3] == Fraction(577, 408)
        gaps = [abs(xs[i + 1] - xs[i]) for i in range(5)]
        assert all(gaps[i + 1] < gaps[i] for i in range(4))
        assert all(x * x != 2 for x in xs)
        assert abs(float(xs[-1]) - math.sqrt(2)) < 1e-11

        els = header(
            "柯西列的巧思：面积为 2 的长方形越压越方，在数轴上挤向一个“分数空洞”",
            "左边解释迭代公式怎么来的；右边展示：哪怕有理数世界里没有 √2 这个终点，单看项与项越挤越近也能判定收敛趋势。",
        )

        # Left panel: Area-2 rectangles averaging into a sqrt(2) x sqrt(2) square!
        els.append(card(20, 62, 344, 278))
        els.append(txt(36, 84, "① 公式哪来的？把面积=2 的长方形两边取平均", 12.6, INK, weight="600"))

        # Step 1: 1 x 2 rectangle (scale 44px per unit)
        sc = 42.0
        els.append(f'<rect x="48" y="114" width="{1.0 * sc:.1f}" height="{2.0 * sc:.1f}" rx="3" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append(txt(48 + 0.5 * sc, 114 + 2.0 * sc + 16, "宽 x₁ = 1", 11, ORANGE, "middle", weight="600"))
        els.append(txt(48 + 1.0 * sc + 6, 114 + 1.0 * sc + 4, "高 2/1=2", 11, ORANGE))

        els.append(f'<line x1="142" y1="156" x2="174" y2="156" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')
        els.append(txt(158, 148, "取平均", 10.5, MUTED, "middle"))

        # Step 2: 1.5 x 1.333 rectangle vs dashed sqrt(2) square
        rx2, ry2 = 188.0, 128.0
        els.append(
            f'<rect x="{rx2}" y="{ry2}" width="{1.5 * sc:.1f}" height="{(4/3) * sc:.1f}" rx="3" '
            f'fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>'
        )
        sq_s = math.sqrt(2) * sc
        els.append(
            f'<rect x="{rx2}" y="{ry2 + (4/3)*sc - sq_s:.1f}" width="{sq_s:.1f}" height="{sq_s:.1f}" '
            f'fill="none" stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="4 3"/>'
        )
        els.append(txt(rx2 + 0.75 * sc, ry2 + (4 / 3) * sc + 16, "宽 x₂ = 3/2 = 1.5", 11, BLUE, "middle", weight="600"))
        els.append(txt(rx2 + 1.5 * sc + 6, ry2 + 0.67 * sc + 4, "高 4/3", 11, BLUE))
        els.append(txt(rx2 + 30, ry2 - 8, "绿虚线：理想正方形 √2", 10.5, GREEN, "middle"))

        els.append(card(36, 224, 312, 102, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(48, 244, "再取一次平均，每一项都仍是纯粹的分数：", 11.3, INK, weight="600"))
        els.append(txt(48, 264, "• x₁ = 1/1 = 1.000000", 11.2, BODY, cls="mono"))
        els.append(txt(48, 282, "• x₂ = 3/2 = 1.500000      （与 x₁ 差 0.5）", 11.2, BODY, cls="mono"))
        els.append(txt(48, 300, "• x₃ = 17/12 ≈ 1.416667    （与 x₂ 差 0.083）", 11.2, BODY, cls="mono"))
        els.append(txt(48, 318, "• x₄ = 577/408 ≈ 1.414216  （与 x₃ 差 0.0025）", 11.2, BLUE, weight="600", cls="mono"))

        # Right panel: Number line + Magnifying zoom showing the rational "hole" at sqrt(2)!
        els.append(card(378, 62, 362, 278))
        els.append(txt(394, 84, "② 数轴放大看：所有分数都在往同一个位置聚拢", 12.6, INK, weight="600"))

        # Top macro number line [1.0, 1.6]
        nl_x0, nl_w, nl_y = 406.0, 306.0, 134.0
        def NX(val):
            return nl_x0 + (val - 1.0) / 0.6 * nl_w

        els.append(f'<line x1="{nl_x0}" y1="{nl_y}" x2="{nl_x0 + nl_w}" y2="{nl_y}" stroke="{INK}" stroke-width="1.6"/>')
        for tv in (1.0, 1.2, 1.4, 1.6):
            els.append(f'<line x1="{NX(tv):.1f}" y1="{nl_y - 4}" x2="{NX(tv):.1f}" y2="{nl_y + 4}" stroke="{MUTED}" stroke-width="1.2"/>')
            els.append(txt(NX(tv), nl_y + 17, f"{tv:.1f}", 10.5, MUTED, "middle"))

        for lbl, val, col, dy in (("x₁=1", 1.0, BODY, -10), ("x₃", 17 / 12, BLUE, -10), ("x₂=1.5", 1.5, BODY, -10)):
            els.append(f'<circle cx="{NX(val):.1f}" cy="{nl_y}" r="4" fill="{col}"/>')
            els.append(txt(NX(val), nl_y + dy, lbl, 11, col, "middle", weight="700"))
        # Hollow circle at sqrt(2)
        s2 = math.sqrt(2)
        els.append(f'<circle cx="{NX(s2):.1f}" cy="{nl_y}" r="4.8" fill="#ffffff" stroke="{ORANGE}" stroke-width="2"/>')

        # Zoom trapezoid from [1.4135, 1.4172] into bottom zoom box
        zx0, zw, zy = 398.0, 322.0, 198.0
        els.append(
            f'<polygon points="{NX(1.411):.1f},{nl_y + 6} {NX(1.422):.1f},{nl_y + 6} {zx0 + zw},{zy} {zx0},{zy}" '
            f'fill="{ORANGE_SOFT}" fill-opacity="0.45" stroke="{ORANGE}" stroke-width="1" stroke-dasharray="3 3"/>'
        )
        els.append(card(zx0, zy, zw, 82, rx=8, fill="#ffffff", stroke=ORANGE, sw=1.3))
        els.append(txt(zx0 + 12, zy + 18, "放大 150 倍看区间 [1.4138, 1.4170]：", 11.2, ORANGE, weight="600"))

        zy_line = zy + 48.0
        def ZX(val):
            return zx0 + 20 + (val - 1.4138) / (1.4170 - 1.4138) * (zw - 40)

        els.append(f'<line x1="{zx0 + 16}" y1="{zy_line}" x2="{zx0 + zw - 16}" y2="{zy_line}" stroke="{INK}" stroke-width="1.6"/>')
        # x3, x4, x5 and hollow hole at sqrt(2)
        els.append(f'<circle cx="{ZX(17/12):.1f}" cy="{zy_line}" r="4" fill="{BLUE}"/>')
        els.append(txt(ZX(17 / 12) - 4, zy_line - 9, "x₃≈1.4167", 10.8, BLUE, "end", weight="600"))

        els.append(f'<circle cx="{ZX(577/408):.1f}" cy="{zy_line}" r="4" fill="{BLUE}"/>')
        els.append(txt(ZX(577 / 408) + 8, zy_line + 18, "x₄≈1.414216", 10.8, BLUE, "start", weight="600"))

        # Hollow hole at sqrt(2)
        els.append(f'<circle cx="{ZX(s2):.1f}" cy="{zy_line}" r="5.5" fill="#ffffff" stroke="{ORANGE}" stroke-width="2.2"/>')
        els.append(txt(ZX(s2) - 2, zy_line - 10, "√2（无理数空洞）", 10.8, ORANGE, "middle", weight="700"))

        els.append(txt(394, 303, "哪怕先不知道 √2 是谁，只要项与项彼此无限贴近，就叫【柯西列】；", 11.2, BODY))
        els.append(txt(394, 322, "把所有这类“分数空洞”全部填实，有理数就升级成了完备的【实数】！", 11.2, GREEN, weight="600"))

        return figure(
            356,
            "求根号 2 的长方形取平均法与柯西列数轴放大图",
            "左图展示面积为2的长方形两边取平均一步步逼近正方形，给出x1到x4的精确分数；右图在数轴上放大150倍展示分数项挤向根号2处的有理数空洞。",
            els,
        )

    def contour_integral(a, radius=1.0, n=4000):
        total = 0
        for k in range(n):
            t = 2 * math.pi * k / n
            z = radius * cmath.exp(1j * t)
            dz = 1j * z * (2 * math.pi / n)
            total += dz / (z - a)
        return total

    def residue():
        inside, outside = 0.25 + 0.15j, 1.55 + 0j
        v_in, v_out = contour_integral(inside), contour_integral(outside)
        assert abs(v_in - 2j * math.pi) < 1e-9
        assert abs(v_out) < 1e-9
        # Verify max swing angle for outside = 1.55: asin(1 / 1.55) ≈ 40.18 deg, returns to 0!
        max_swing = math.degrees(math.asin(1.0 / outside.real))
        assert 39.0 < max_swing < 41.5

        els = header(
            "围线积分 ∮ dz/(z − a) 为什么只看“圈里还是圈外”？用视线转角一眼看懂！",
            "把奇点 a 当作观察者，z 是沿蓝圈逆时针跑的人。dz/(z−a) 累加的虚部，恰好是“观察者转头盯住人”扫过的净角度！",
        )

        # Left panel: a inside -> full 360 deg = 2pi rad turn!
        els.append(card(20, 62, 352, 286))
        els.append(txt(36, 84, "① 奇点 a 在圈内：脖子跟着转满整整一圈（+360°）", 12.6, INK, weight="600"))
        cx1, cy1, r = 196.0, 198.0, 78.0
        ax1, ay1 = cx1 + inside.real * r, cy1 - inside.imag * r
        els.append(f'<circle cx="{cx1}" cy="{cy1}" r="{r}" fill="{BLUE_SOFT}" fill-opacity="0.48" stroke="{BLUE}" stroke-width="1.9"/>')
        # CCW arrow on top of circle
        els.append(f'<path d="M{cx1 + 8},{cy1 - r} L{cx1 - 2},{cy1 - r}" fill="none" stroke="{BLUE}" stroke-width="2" marker-end="url(#arr-blue)"/>')
        # 4 sight-lines from a to walkers on circle
        for deg_w in (15, 105, 195, 285):
            rad_w = math.radians(deg_w)
            wx, wy = cx1 + r * math.cos(rad_w), cy1 - r * math.sin(rad_w)
            els.append(f'<line x1="{ax1:.1f}" y1="{ay1:.1f}" x2="{wx:.1f}" y2="{wy:.1f}" stroke="{ORANGE}" stroke-width="1.2" stroke-dasharray="3 3"/>')
            els.append(f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="3.2" fill="{BLUE}"/>')
        # Small full-turn arc around a
        els.append(
            f'<path d="M{ax1 + 20:.1f},{ay1:.1f} A20,20 0 1,0 {ax1 + 19.2:.1f},{ay1 + 5.5:.1f}" '
            f'fill="none" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>'
        )
        els.append(f'<circle cx="{ax1:.1f}" cy="{ay1:.1f}" r="4.8" fill="{ORANGE}"/>')
        els.append(txt(ax1 - 6, ay1 + 16, "a", 12.5, ORANGE, "end", weight="700", halo=True))
        els.append(txt(ax1 + 25, ay1 - 8, "净转 +2π", 11, ORANGE, weight="700", halo=True))
        els.append(txt(36, 300, "跑完一圈回到起点：距离 ln r 抵消为 0，角度净增 2π 弧度", 11.2, BODY))
        els.append(pill(36, 314, "∮ dz/(z − a) = 0 + i · (2π) = 2πi（与圈的形状无关！）", fg=ORANGE, bg=ORANGE_SOFT, w=320, h=22, size=11.2))

        # Right panel: a outside -> swings left +40 deg then right -40 deg = 0 net turn!
        els.append(card(388, 62, 352, 286))
        els.append(txt(404, 84, "② 奇点 a 在圈外：歪头过去又摆回来，净转角 = 0°", 12.6, INK, weight="600"))
        cx2, cy2, r2 = 508.0, 198.0, 70.0
        ax2, ay2 = cx2 + outside.real * r2, cy2
        els.append(f'<circle cx="{cx2}" cy="{cy2}" r="{r2}" fill="{BLUE_SOFT}" fill-opacity="0.48" stroke="{BLUE}" stroke-width="1.9"/>')
        els.append(f'<path d="M{cx2 + 8},{cy2 - r2} L{cx2 - 2},{cy2 - r2}" fill="none" stroke="{BLUE}" stroke-width="2" marker-end="url(#arr-blue)"/>')

        # Upper and lower tangent sightlines from outside point a!
        sin_a = r2 / (ax2 - cx2)
        cos_a = math.sqrt(1 - sin_a * sin_a)
        # Tangent points on circle: cx2 + r2*sin_a, cy2 +- r2*cos_a
        tx = cx2 + r2 * sin_a
        ty_top = cy2 - r2 * cos_a
        ty_bot = cy2 + r2 * cos_a
        els.append(f'<line x1="{ax2:.1f}" y1="{ay2:.1f}" x2="{tx:.1f}" y2="{ty_top:.1f}" stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="{ax2:.1f}" y1="{ay2:.1f}" x2="{tx:.1f}" y2="{ty_bot:.1f}" stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(f'<line x1="{ax2:.1f}" y1="{ay2:.1f}" x2="{cx2 - r2:.1f}" y2="{cy2:.1f}" stroke="{HAIRLINE}" stroke-width="1.1"/>')
        # Wedge arc near ax2 showing +40 deg / -40 deg cancel
        arc_r = 38.0
        els.append(
            f'<path d="M{ax2 - arc_r * cos_a:.1f},{ay2 - arc_r * sin_a:.1f} '
            f'A{arc_r},{arc_r} 0 0,0 {ax2 - arc_r * cos_a:.1f},{ay2 + arc_r * sin_a:.1f}" '
            f'fill="none" stroke="{GREEN}" stroke-width="1.6"/>'
        )
        els.append(txt(ax2 - 46, ay2 - 18, f"+{max_swing:.0f}°", 10.8, GREEN, "end", weight="600", halo=True))
        els.append(txt(ax2 - 46, ay2 + 26, f"−{max_swing:.0f}°", 10.8, GREEN, "end", weight="600", halo=True))
        els.append(f'<circle cx="{ax2:.1f}" cy="{ay2:.1f}" r="4.8" fill="{ORANGE}"/>')
        els.append(txt(ax2 + 9, ay2 + 5, "a（圈外）", 12, ORANGE, weight="700", halo=True))

        els.append(txt(404, 300, f"视线最多偏转 ±{max_swing:.0f}° 就折返，走满一圈净转角严格为 0", 11.2, BODY))
        els.append(pill(404, 314, "∮ dz/(z − a) = 0（圈外奇点对围线积分零贡献！）", fg=GREEN, bg=GREEN_SOFT, w=320, h=22, size=11.2))

        return figure(
            364,
            "柯西围线积分与留数的视线转角直觉",
            "左图奇点a在圆内，观察视线随逆时针路径转满一圈净增2π弧度，积分为2πi；右图奇点a在圆外，视线上下摆动约40度后回到原方向，净转角为0，积分为0。",
            els,
        )

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        for name, content in (
            ("calculus-crisis", calculus_crisis()),
            ("cauchy-sequence", sequence()),
            ("residue-circle", residue()),
        ):
            (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
            print(f"Wrote {name}.svg")
        _build_cauchy_extensions()

    main()


@register("variations", "变分法：泛函扰动、折射驻值、悬链约束与作用量", "geometry_analysis")
def build_variations():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "variations"

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

    main()


@register("fourier", "傅里叶分析：热收支、模态叠加、衰减与采样边界", "geometry_analysis")
def build_fourier():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "fourier"

    TAU = 2*math.pi

    GRAY = "#7b8fa0"

    def rows(x, y, values, size=23, step=38, color=INK):
        return "".join(text(x, y+i*step, value, size, color) for i,value in enumerate(values))

    def heading(number, title):
        return text(36, 49, f"{number} {title}", 28)

    def write(name, height, title, description, body):
        save(name,height,title,description,body,output_directory=OUT)

    def graph(y, fn, scale=55, offset=0, color=BLUE, dash=False, count=1024):
        return path([(92+536*j/count, y-scale*(fn(j/count)-offset)) for j in range(count+1)], color, 3, dash)

    def axes(y, label="位置 x：0 → 1 m"):
        return line(88,y,634,y,GRAY,True)+text(92,y+97,label,21)

    def heat(x,t):
        return 50+20*math.exp(-.01*TAU**2*t)*math.cos(TAU*x)+10*math.exp(-.01*(3*TAU)**2*t)*math.cos(3*TAU*x)

    def amplitude(samples):
        n=len(samples)
        return [abs(sum(v*complex(math.cos(-TAU*k*j/n),math.sin(-TAU*k*j/n)) for j,v in enumerate(samples)))/n*(1 if k in (0,n//2) else 2) for k in range(n//2+1)]

    def history():
        body=heading("①","从研究热，到研究各种变化")
        for i,(year,title,detail) in enumerate([
            ("1768","出生于欧塞尔","后来经历教学、远征与行政工作。"),
            ("1795","在巴黎师范学校学习","听过拉格朗日、拉普拉斯与蒙日的课。"),
            ("1807","报告固体中的热传播研究","三角级数与推导的严密性引发争论。"),
            ("1811","扩充论文参加热传播竞赛","获奖肯定与对论证的保留意见并存。"),
            ("1822","《热的解析理论》出版","系统讨论热传播及三角级数方法。"),
        ]):
            y=86+i*125
            body+=panel(y,109)+text(48,y+35,year,25,BLUE)+text(220,y+35,title,24)+text(48,y+82,detail,23)
        body+=rows(36,768,["现代傅里叶分析经过许多人的后续完善。","不是“一个人一次写出了今天所有频谱算法”。"])
        write("history.svg",860,"傅里叶的学习经历与热理论发展路标","1795年学习、1807年报告、1811年参赛与1822年专著出版是不同阶段；现代傅里叶分析由后人持续发展。",body)

    def heat_balance():
        body=heading("②","一小段升温，还是降温？看收支")
        body+=rows(36,96,["等间距、同材料、同截面；三处温度：80、60、20 ℃。","只看中间小段：左边流入，右边流出。"])
        body+=panel(179,284)
        for x,value in [(90,80),(290,60),(490,20)]:
            body+=f'<rect x="{x}" y="245" width="140" height="102" fill="#e1edf4" stroke="{INK}" stroke-width="2"/>'
            body+=text(x+70,307,f"{value} ℃",28,INK,"middle")
        body+=line(230,296,282,296,RED,arrow=True)+line(430,296,482,296,RED,arrow=True)
        body+=text(250,220,"流入",24,RED,"middle")+text(450,220,"流出",24,RED,"middle")
        body+=text(48,414,"左温差 20；右温差 40 → 流出更多，中间降温。",23)
        body+=panel(498,266)
        body+=rows(48,545,["① 温度向右下降，热流朝右。","② 傅里叶定律：热流密度 = −导热率 × 温度梯度。","③ 能量守恒：积累 = 流入 − 流出。","合起来：温度随时间的变化，由空间弯曲程度决定。"],23,52)
        body+=rows(36,817,["箭头只标方向，不按长度表示热流大小。","这是一维局部收支示意；热传导定律不是波分解公式。"],22)
        assert 80-2*60+20<0
        write("heat-balance.svg",919,"由傅里叶导热定律和能量守恒理解温度变化","等间距的80、60、20摄氏度三处，右侧温度差大于左侧，流出更多，中段降温。箭头仅示意方向。",body)

    def modes():
        body=heading("③","复杂形状，先试着拆成简单波")
        body+=rows(36,95,["把周长 1 m 的细环展开；两端其实是同一点。","这里只选两种空间波，温度单位 ℃。"])
        for y,title,fn,offset,color in [
            (180,"① 一圈一次起伏：20 cos(2πx)",lambda x:20*math.cos(TAU*x),0,BLUE),
            (471,"② 一圈三次起伏：10 cos(6πx)",lambda x:10*math.cos(3*TAU*x),0,RED),
            (762,"③ 50 + ① + ②：初始温度",lambda x:heat(x,0),50,INK),
        ]:
            body+=panel(y,260)+text(48,y+40,title,24,color)
            body+=graph(y+147,fn,2.1,offset,color)+axes(y+147)
            body+=text(650,y+155,str(offset),22,GRAY)
        body+=rows(36,1075,["①②表示相对平均温度的有正有负的分量。","③才是实际温度；相加不表示热在做机械振动。"],23)
        write("mode-sum.svg",1170,"两种空间余弦温差加上平均温度得到初始温度形状","一阶20摄氏度与三阶10摄氏度的余弦温差相加，再加50摄氏度平均值，得到20到80摄氏度的环上温度。三图使用同一温度比例。",body)

    def decay():
        body=heading("④","细碎起伏先淡去，平均温度留下")
        body+=rows(36,94,["同一个绝热细环：α = 0.01 m²/s，周长 1 m。","这是人为选定参数的模型，不是某种金属的实测。"],23)
        for i,t in enumerate([0,.5,2,10]):
            y=181+i*228
            a=20*math.exp(-.01*TAU**2*t); b=10*math.exp(-.01*(3*TAU)**2*t)
            body+=panel(y,207)+text(48,y+34,f"t = {t:g} s",24,BLUE)
            body+=text(255,y+34,f"振幅：一阶 {a:.3f}；三阶 {b:.3f} ℃",22)
            body+=graph(y+117,lambda x:heat(x,t),2,50)+line(89,y+117,637,y+117,GRAY,True)
            body+=text(645,y+125,"50",21,GRAY)
            body+=text(92,y+188,"x = 0",20)+text(628,y+188,"1 m（接回起点）",20,INK,"end")
        body+=rows(36,1140,["三阶的指数衰减率是一阶的 9 倍。","各图同一比例；均温保持 50 ℃，不是所有温度降到 0。"],23)
        for t in (0,.5,2,10):
            assert abs(sum(heat(j/2048,t) for j in range(2048))/2048-50)<1e-11
        write("heat-decay.svg",1230,"绝热环上温度随时间变平的四个精确快照","温度由一阶与三阶余弦精确解析解计算，时刻0、0.5、2、10秒；三阶衰减率九倍，平均温度保持50摄氏度。",body)

    def orthogonality():
        f=lambda t:math.cos(TAU*8*t)+.5*math.cos(TAU*20*t)
        body=heading("⑤","怎样知道一条波，藏了多少？")
        body+=rows(36,94,["用整整 1 秒观察：g(t) = cos(2π·8t) + ½ cos(2π·20t)。","乘上参考波，再求平均；此处两种频率都走完整周期。"],22)
        for y,title,fn,result,color in [
            (180,"① 原信号：8 Hz 与 20 Hz 相加",f,"",BLUE),
            (463,"② 乘 8 Hz 的余弦",lambda t:f(t)*math.cos(TAU*8*t),"平均 0.500 → 振幅 1.000",RED),
            (746,"③ 乘 20 Hz 的余弦",lambda t:f(t)*math.cos(TAU*20*t),"平均 0.250 → 振幅 0.500",GOLD),
        ]:
            body+=panel(y,254)+text(48,y+37,title,24,color)
            body+=graph(y+125,fn,47,color=color)+line(89,y+125,636,y+125,GRAY,True)
            body+=text(92,y+221,result or "横轴：0 → 1 s；纵轴：信号值（无量纲）。",22)
        body+=rows(36,1060,["不同频率乘积的正负部分，在这段整周期里抵消。","相同余弦平方的平均为 ½，所以这里还要乘 2。"],23)
        for frequency,expected in [(8,.5),(20,.25)]:
            mean=sum(f(j/4096)*math.cos(TAU*frequency*j/4096) for j in range(4096))/4096
            assert math.isclose(mean,expected,abs_tol=1e-12)
        write("frequency-probe.svg",1158,"乘参考余弦并平均提取两个整周期频率的分量","同一信号与8赫兹参考相乘均值0.5，与20赫兹参考相乘均值0.25；还原余弦振幅分别为1与0.5。未知相位时还需要正弦参考。",body)

    def continuous():
        body=heading("⑦","周期变长，频率格点怎样变密？")
        body+=rows(36,94,["用高斯 g(t)=exp(−πt²) 的周期化作例子。","时间、频率分别以 1 s、1 Hz 归一化后写数值。","格点 f=n/P；每项权重=exp(−πf²)/P。"],21,33)
        for i,p in enumerate([1,2,4]):
            y=180+i*264; baseline=y+211
            body+=panel(y,243)+text(48,y+37,f"周期 P = {p} s；频率间距 Δf = {1/p:g} Hz",24,BLUE)
            body+=line(92,baseline,628,baseline,GRAY)
            for n in range(-2*p,2*p+1):
                f=n/p; value=math.exp(-math.pi*f*f)/p; x=360+120*f
                body+=line(x,baseline,x,baseline-155*value,BLUE)+dot(x,baseline-155*value,3,BLUE)
            body+=text(105,baseline+25,"−2",19)+text(355,baseline+25,"0",19)+text(600,baseline+25,"2 Hz",19)
        y=989
        body+=panel(y,266)+text(48,y+38,"连续频率用积分，不再只在离散格点相加。",23)
        body+=path([(120+480*j/800,y+217-155*math.exp(-math.pi*(-2+4*j/800)**2)) for j in range(801)])
        body+=line(115,y+217,610,y+217,GRAY)
        body+=text(110,y+244,"−2",19)+text(355,y+244,"0",19)+text(575,y+244,"2 Hz",19)
        body+=rows(36,1309,["上三图纵轴是单项权重；下图纵轴是频谱密度。","权重里含 Δf；不能把不同纵轴当成同一根柱子的高度。"],22)
        for frequency in (0,.25,.5,1,2):
            steps=8192
            h=16/steps
            integral=sum((1 if j in (0,steps) else 4 if j%2 else 2)*
                         math.exp(-math.pi*(-8+j*h)**2)*math.cos(TAU*frequency*(-8+j*h))
                         for j in range(steps+1))*h/3
            assert math.isclose(integral,math.exp(-math.pi*frequency**2),abs_tol=1e-12)
        write("series-to-transform.svg",1405,"由周期化高斯的离散频率权重理解连续傅里叶积分","周期1、2、4秒的频率间距为1、0.5、0.25赫兹，系数为高斯频谱密度乘频率间距；下方曲线显示频谱密度，不把离散权重与连续密度混为一谈。",body)

    def phase():
        body=heading("⑥","频率和强弱相同，波形仍会不同")
        body+=rows(36,95,["同样的 8 Hz、20 Hz；只改第二项的相位。","记录 1 s，采样率 128 Hz，共 128 点。"],23)
        for y,phi,label,color in [(180,0,"① 第二项相位 0°",BLUE),(461,math.pi/2,"② 第二项相位 90°",RED)]:
            body+=panel(y,253)+text(48,y+37,label,25,color)
            body+=graph(y+136,lambda t:math.cos(TAU*8*t)+.5*math.cos(TAU*20*t+phi),48,color=color)
            body+=line(90,y+136,635,y+136,GRAY,True)+text(92,y+225,"横轴：0 → 1 s",22)
        body+=panel(742,310)+text(48,783,"③ 两组单边振幅相同：8 Hz → 1；20 Hz → 0.5",23)
        body+=line(110,995,626,995,GRAY)
        for f,a in [(8,1),(20,.5)]:
            x=110+20*f
            body+=line(x,995,x,995-155*a,BLUE)+dot(x,995-155*a,5,BLUE)
            body+=text(x,1029,f"{f} Hz",22,INK,"middle")+text(x+14,990-155*a,f"{a:g}",22)
        body+=rows(36,1106,["这是这两组整周期记录的 DFT 单边振幅，不是完整频谱。","要还原原波形，还得保存相位；复数保存两类信息。"],22)
        for phi in (0,math.pi/2):
            a=amplitude([math.cos(TAU*8*j/128)+.5*math.cos(TAU*20*j/128+phi) for j in range(128)])
            assert abs(a[8]-1)<1e-12 and abs(a[20]-.5)<1e-12
        write("phase-matters.svg",1200,"不同相位的信号可以拥有相同的单边振幅","8赫兹与20赫兹两个余弦信号仅改变20赫兹相位，时域波形不同；一秒128点DFT单边振幅仍为1和0.5，说明幅度图不能替代完整复频谱。",body)

    def sampling():
        body=heading("⑧","采样不够快，快波会冒充慢波")
        body+=rows(36,95,["每秒只取 64 个样本：8 Hz 与 56 Hz 余弦可完全混淆。","下图只放大 0 → 0.125 s；圆点是共同样本。"],23)
        body+=panel(181,330)
        for f,color,dash in [(56,RED,True),(8,BLUE,False)]:
            body+=graph(337,lambda u:math.cos(TAU*f*.125*u),85,color=color,dash=dash,count=1600)
        for j in range(9):
            x=92+536*j/8;y=337-85*math.cos(TAU*8*j/64)
            body+=dot(x,y,6,INK)
            assert abs(math.cos(TAU*8*j/64)-math.cos(TAU*56*j/64))<1e-12
        body+=text(92,480,"实线 8 Hz；虚线 56 Hz；圆点无法区分它们。",23)
        body+=panel(550,250)+rows(48,594,["① 快波可以落在同一串样本上：这是混叠。","② 还原带限信号，需要足够采样率及相应条件。","③ 有限记录还有限制：1 s 的 DFT 格点间距为 1 Hz。","多补几个零，不会凭空延长真实观察时间。"],22,49)
        body+=rows(36,856,["这里没有把 56 Hz 降成 8 Hz；是采样信息分不出。","傅里叶分析不是凭空补回未测到的信息。"],23)
        write("sampling-limits.svg",954,"64赫兹采样下8赫兹和56赫兹余弦的混叠","两条连续余弦在每1/64秒的采样点上相等；图放大首0.125秒，共九个采样点。采样率、观察时长和DFT格点都限制分析。",body)

    def main():
        OUT.mkdir(parents=True,exist_ok=True)
        for draw in (history,heat_balance,modes,decay,orthogonality,continuous,phase,sampling):
            draw()
        print("Generated eight original Fourier figures; verified means, coefficients, phase amplitudes and alias samples.")

    main()


@register("bernoulli", "伯努利家族：家谱、等角螺线、大数定律与流体能量", "geometry_analysis")
def build_bernoulli():
    INK, MUTED, BLUE, ORANGE = K_INK, K_MUTED, K_BLUE, K_ORANGE

    text, document = k_text, b_document

    OUT = REPO_ROOT / "assets" / "images" / "bernoulli"

    def node(x, y, name, dates, number=None):
        width = 684 - x
        color = BLUE if number else "#8798a6"
        heading = f"{number} {name}" if number else name
        return [
            f'<rect x="{x}" y="{y}" width="{width}" height="82" rx="14" '
            f'fill="{"#fff" if number else "#e8eef2"}" stroke="{color}" stroke-width="2"/>',
            text(x + 18, y + 31, heading, 28, BLUE if number else MUTED),
            text(x + 18, y + 68, dates, 23, MUTED),
        ]

    def connector(path):
        return f'<path d="{path}" fill="none" stroke="#738a9c" stroke-width="3"/>'

    def family_tree():
        elements = [
            text(36, 48, "八位数学家，三代亲缘", 32),
            text(36, 84, "沿线往下读；向右缩进一级，是下一代。", 24, MUTED),
            connector("M54 202V691M54 311H88M54 421H88M54 691H88"),
            connector("M122 462V531H156"),
            connector("M122 732V1021M122 801H156M122 911H156M122 1021H156"),
            connector("M190 1062V1241M190 1131H224M190 1241H224"),
        ]
        elements += node(36, 120, "尼古拉斯：经营香料生意的父亲", "1623—1708；灰框不计入八位数学家")
        people = [
            (88, 270, "雅各布一世", "1655—1705；约翰的哥哥", "①"),
            (88, 380, "尼古拉斯：两位数学家之间的兄弟", "1662—1716；尼古拉斯一世之父", None),
            (156, 490, "尼古拉斯一世", "1687—1759；丹尼尔的堂兄", "③"),
            (88, 650, "约翰一世", "1667—1748；以下三人为他的儿子", "②"),
            (156, 760, "尼古拉斯二世", "1695—1726；丹尼尔的哥哥", "④"),
            (156, 870, "丹尼尔", "1700—1782；研究流体与风险", "⑤"),
            (156, 980, "约翰二世", "1710—1790；以下两人为他的儿子", "⑥"),
            (224, 1090, "约翰三世", "1744—1807；丹尼尔的侄子", "⑦"),
            (224, 1200, "雅各布二世", "1759—1789；约翰三世的弟弟", "⑧"),
        ]
        assert {p[4] for p in people if p[4]} == set("①②③④⑤⑥⑦⑧")
        for person in people:
            elements += node(*person)
        elements += [
            text(36, 1330, "只列连接这八位所需的关系，并非全部子女名单。", 24, MUTED),
            text(36, 1365, "同名人物用“一世、二世、三世”区分。", 24, MUTED),
        ]
        return document(
            1400,
            "伯努利家族八位数学家的亲缘图",
            "灰框父亲有雅各布、尼古拉斯、约翰三个儿子。中间一支有尼古拉斯一世；"
            "约翰一世的三个数学家儿子是尼古拉斯二世、丹尼尔、约翰二世。"
            "约翰二世的两个儿子是约翰三世与雅各布二世。",
            elements,
        )

    def spiral_path(radius, scale, cy):
        points = []
        for i in range(1001):
            theta = 4 * math.pi * i / 1000
            r = scale * radius(theta)
            x, y = 310 + r * math.cos(theta), cy - r * math.sin(theta)
            points.append(f"{'M' if i == 0 else 'L'}{x:.3f},{y:.3f}")
        return " ".join(points)

    def spiral_comparison():
        arch = lambda theta: 1 + 2 * theta / math.pi
        logarithmic = lambda theta: 2 ** (theta / (2 * math.pi))
        for turn, expected in enumerate((1, 5, 9)):
            assert math.isclose(arch(turn * 2 * math.pi), expected)
        for turn, expected in enumerate((1, 2, 4)):
            assert math.isclose(logarithmic(turn * 2 * math.pi), expected)
        for theta in (0, 0.3, 1, 4):
            assert math.isclose(logarithmic(theta + 2 * math.pi), 2 * logarithmic(theta))
        elements = [
            text(36, 48, "墓碑上，差的是哪一条螺线？", 32),
            text(36, 86, "沿同一条向右的射线，比较每绕一圈的半径。", 24, MUTED),
        ]
        panels = [
            (125, 365, "① 阿基米德螺线：每圈加相同长度", arch, 20, (1, 5, 9),
             "半径 1 → 5 → 9：每圈都加 4。", "构造：r = 1 + 2θ/π"),
            (635, 875, "② 对数螺线：每圈乘相同倍数", logarithmic, 45, (1, 2, 4),
             "半径 1 → 2 → 4：每圈都乘 2。", "构造：r = 2 的 θ/(2π) 次方"),
        ]
        for top, cy, title, radius, scale, values, conclusion, formula in panels:
            elements += [
                f'<rect x="24" y="{top}" width="672" height="480" rx="18" '
                'fill="#fff" stroke="#c9d6df" stroke-width="2"/>',
                text(44, top + 39, title, 26),
                text(44, top + 72, formula, 22, MUTED),
                f'<path d="{spiral_path(radius, scale, cy)}" fill="none" '
                f'stroke="{BLUE}" stroke-width="3.5"/>',
                f'<path d="M310 {cy}H520" fill="none" stroke="#687f90" '
                'stroke-width="2" stroke-dasharray="6 5"/>',
                f'<circle cx="310" cy="{cy}" r="4" fill="{INK}"/>',
                text(280, cy + 33, "中心", 20, MUTED, "middle"),
            ]
            for value in values:
                x = 310 + value * scale
                elements += [
                    f'<circle cx="{x}" cy="{cy}" r="5.5" fill="#ad4f16" '
                    'stroke="#fff" stroke-width="2"/>',
                    text(x, cy + 33, str(value), 24, "#ad4f16", "middle"),
                ]
            elements += [text(44, top + 443, conclusion, 26)]
        elements += [
            text(36, 1152, "两图分别缩放；半径无单位，只画有限两圈。", 24, MUTED),
            text(36, 1186, "原创数学示意，不是墓碑曲线的描摹。", 24, MUTED),
        ]
        return document(
            1220,
            "阿基米德螺线与对数螺线的两圈比较",
            "上图半径每圈加四，沿向右射线三次交点半径为一、五、九；"
            "下图半径每圈乘二，对应一、二、四。曲线按方程计算，两图分别缩放。",
            elements,
        )

    def large_numbers():
        elements = [
            text(36, 48, "次数增多，比例怎样变得可靠？", 32),
            text(36, 86, "独立、公平硬币：统计所有可能结果，不抽样模拟。", 24, MUTED),
        ]
        expected = (0.75390625, 0.05688793364098079, 2.7284641560660184e-10)
        labels = ("75.390625%", "约 5.689%", "约 2.73 × 10⁻¹⁰（概率值）")
        for index, n in enumerate((10, 100, 1000)):
            top = 120 + 300 * index
            probabilities = [math.comb(n, k) / 2**n for k in range(n + 1)]
            tail = [k for k in range(n + 1) if abs(10 * k - 5 * n) >= n]
            probability = sum(math.comb(n, k) for k in tail) / 2**n
            assert math.isclose(sum(probabilities), 1, abs_tol=1e-14)
            assert math.isclose(probability, expected[index], rel_tol=1e-13)
            elements += [
                f'<rect x="24" y="{top}" width="672" height="282" rx="16" '
                'fill="#fff" stroke="#c9d6df"/>',
                text(44, top + 36, f"抛 {n} 次", 28),
                text(44, top + 76, f"至少偏离 10 个百分点：{labels[index]}", 24, ORANGE),
                text(150, top + 121, "计入左端", 21, MUTED, "middle"),
                text(570, top + 121, "计入右端", 21, MUTED, "middle"),
            ]
            peak = max(probabilities)
            for k, p in enumerate(probabilities):
                x = 90 + 540 * k / n
                height = 100 * p / peak
                width = min(26, 540 / n * 0.85)
                elements.append(
                    f'<rect x="{x-width/2:.4f}" y="{top+230-height:.4f}" '
                    f'width="{width:.4f}" height="{height:.6g}" '
                    f'fill="{ORANGE if k in tail else BLUE}"/>'
                )
            for fraction in (0, 0.4, 0.5, 0.6, 1):
                x = 90 + 540 * fraction
                elements.append(text(x, top + 264, f"{fraction:.0%}", 22, MUTED, "middle"))
            for fraction in (0.4, 0.6):
                x = 90 + 540 * fraction
                elements.append(
                    f'<path d="M{x} {top+130}V{top+235}" stroke="{ORANGE}" '
                    'stroke-width="1.5" stroke-dasharray="4 4"/>'
                )
            elements.append(f'<path d="M75 {top+230}H645" stroke="{MUTED}"/>')
        elements += [
            text(36, 1054, "横轴：正面比例；每根柱：该比例的概率。", 24, MUTED),
            text(36, 1092, "三图纵轴分别缩放；虚线边界及外侧均计入。", 24, MUTED),
        ]
        return document(
            1120, "公平硬币正面比例的精确二项分布",
            "分别计算十、一百、一千次独立公平抛掷的全部二项概率。"
            "正面比例不高于百分之四十或不低于百分之六十的合计概率随次数增加大幅下降。"
            "三图横轴同尺度，柱高分别归一化到各自峰值，不能跨图比较高度。",
            elements,
        )

    def orthogonal_trajectories():
        px, py = 1, 1
        tangent = (1, -1)
        assert px * tangent[0] + py * tangent[1] == 0
        assert math.isclose(px**2 + py**2, 2)
        elements = [
            text(36, 48, "正交轨线：每次相交，都成直角", 32),
            text(36, 86, "教学例子：同心圆，与过圆心的直线。", 24, MUTED),
            '<rect x="24" y="115" width="672" height="520" rx="18" fill="#fff" stroke="#c9d6df"/>',
            f'<path d="M120 405H550M330 600V195" stroke="#c5d0d9" stroke-width="2"/>',
            text(564, 413, "x", 24, MUTED),
            text(330, 177, "y", 24, MUTED, "middle"),
            text(310, 438, "O", 23, MUTED, "middle"),
        ]
        for angle in (0, math.pi / 4, math.pi / 2, 3 * math.pi / 4):
            dx, dy = 190 * math.cos(angle), 190 * math.sin(angle)
            elements.append(
                f'<path d="M{330-dx:.4f} {405+dy:.4f}L{330+dx:.4f} {405-dy:.4f}" '
                f'stroke="{ORANGE}" stroke-width="2" stroke-dasharray="7 6"/>'
            )
        for radius in (60, 100, 100 * math.sqrt(2), 180):
            elements.append(
                f'<circle cx="330" cy="405" r="{radius:.4f}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>'
            )
        elements += [
            f'<path d="M390 265L470 345" stroke="{INK}" stroke-width="3"/>',
            f'<path d="M418 317L430 329L442 317" fill="none" stroke="{INK}" stroke-width="2.5"/>',
            f'<circle cx="430" cy="305" r="6" fill="{INK}"/>',
            text(500, 298, "P(1,1)", 25),
            text(500, 336, "切线 ⟂ 半径", 23),
            text(44, 680, "① 先选一条圆：x² + y² = C。", 26),
            text(44, 724, "② 再选过圆心的直线；在交点看切线方向。", 26),
            text(44, 768, "③ P 点：圆的斜率 −1，直线斜率 +1。", 26),
            text(36, 830, "横纵轴同尺度、坐标无量纲；不是历史论文复刻。", 24, MUTED),
        ]
        return document(
            865, "同心圆与过圆心直线的正交轨线示例",
            "蓝色实线为同心圆，棕色虚线为过圆心直线。"
            "点一逗号一处的半径方向与圆切线方向点积为零；直角用折线标记。"
            "此图解释轨线问题，不复刻尼古拉斯二世的双曲线论文。",
            elements,
        )

    def fluid_energy():
        density, area1, area2, speed1 = 1000, 2e-4, 1e-4, 1
        flow = area1 * speed1
        speed2 = flow / area2
        pressure1 = 100000
        kinetic1 = density * speed1**2 / 2
        kinetic2 = density * speed2**2 / 2
        pressure2 = pressure1 + kinetic1 - kinetic2
        assert math.isclose(flow * 1000, 0.2)
        assert speed2 == 2 and pressure1 - pressure2 == 1500
        assert pressure1 + kinetic1 == pressure2 + kinetic2 == 100500
        elements = [
            text(36, 48, "水变快了，能量从哪里来？", 32),
            text(36, 86, "水密度 1000 kg/m³；以下数值为教学构造。", 24, MUTED),
            '<rect x="24" y="115" width="672" height="162" rx="16" fill="#fff" stroke="#c9d6df"/>',
            text(44, 156, "① 先核对：每秒进出的水一样多", 28),
            text(44, 201, "2 cm² × 1 m/s = 1 cm² × 2 m/s", 26),
            text(44, 244, "两边流量都是 0.2 L/s。", 26, BLUE),
            text(36, 318, "② 截面变小，水流加快（管形示意）", 28),
            f'<path d="M70 355H290L460 380H650V480H460L290 505H70" '
            f'fill="#e1f0f5" stroke="{BLUE}" stroke-width="4"/>',
            f'<path d="M110 430H260M495 430H615" stroke="{ORANGE}" stroke-width="5"/>',
            f'<path d="M260 430L244 421V439ZM615 430L599 421V439Z" fill="{ORANGE}"/>',
            text(200, 547, "截面①：2 cm²", 26, INK, "middle"),
            text(525, 547, "截面②：1 cm²", 26, INK, "middle"),
            text(200, 589, "速度：1 m/s", 26, BLUE, "middle"),
            text(525, 589, "速度：2 m/s", 26, BLUE, "middle"),
            text(200, 631, "压力：100 kPa", 26, ORANGE, "middle"),
            text(525, 631, "压力：98.5 kPa", 26, ORANGE, "middle"),
            '<rect x="24" y="662" width="672" height="206" rx="16" fill="#fff" stroke="#c9d6df"/>',
            text(44, 704, "③ 核对：压力 + 动能密度", 28),
            text(44, 748, "①侧：100000 + 500 = 100500 Pa", 26),
            text(44, 792, "②侧：98500 + 2000 = 100500 Pa", 26),
            text(44, 836, "动能项多 1500 Pa，压力项少 1500 Pa。", 26, BLUE),
            text(36, 910, "水平、稳态、不可压缩、无损耗；同一流线、无外加功。", 23, MUTED),
        ]
        return document(
            945, "水平水管的流量守恒与伯努利能量核对",
            "截面积二平方厘米、速度每秒一米，与截面积一平方厘米、速度每秒二米的流量相同。"
            "在图注所述理想条件下，压力从一百千帕降到九十八点五千帕，"
            "两侧压力加动能密度均为十万零五百帕。管形不按实际截面比例绘制。",
            elements,
        )

    def string_modes():
        length, wave_speed = 1, 100
        frequency1 = wave_speed / (2 * length)
        frequency3 = 3 * frequency1
        assert frequency1 == 50 and frequency3 == 150

        def first(x):
            return math.sin(math.pi * x)

        def third(x):
            return 0.35 * math.sin(3 * math.pi * x)

        for x in (0, 1):
            assert abs(first(x)) < 1e-14 and abs(third(x)) < 1e-14
        for x in (1 / 3, 2 / 3):
            assert abs(third(x)) < 1e-14
        assert math.isclose(third(0.5), -0.35)
        elements = [
            text(36, 48, "一根琴弦，叠加几种简单运动", 32),
            text(36, 86, "同一时刻、同一位置相加；三图采用相同位移比例。", 24, MUTED),
        ]
        panels = [
            (f"① 第一振型：f₁ = {frequency1:g} Hz", "振幅 1 mm；两端不动，中间一个波腹。", first),
            (f"② 第三振型：f₃ = {frequency3:g} Hz", "振幅 0.35 mm；还有两个内部节点。", third),
            ("③ 两者叠加：不是单一的正弦形状", "逐点相加，而不是把两根弦接起来。", lambda x: first(x) + third(x)),
        ]
        for index, (heading, caption, shape) in enumerate(panels):
            top = 120 + 290 * index
            baseline = top + 174
            elements += [
                f'<rect x="24" y="{top}" width="672" height="268" rx="16" fill="#fff" stroke="#c9d6df"/>',
                text(44, top + 38, heading, 27),
                text(44, top + 78, caption, 24, MUTED),
                f'<path d="M90 {baseline}H630" stroke="#8798a6" stroke-dasharray="6 5"/>',
            ]
            points = [
                (90 + 540 * i / 600, baseline - 55 * shape(i / 600))
                for i in range(601)
            ]
            path = " ".join(
                f"{'M' if i == 0 else 'L'}{x:.4f},{y:.4f}"
                for i, (x, y) in enumerate(points)
            )
            elements.append(f'<path d="{path}" fill="none" stroke="{BLUE}" stroke-width="3.5"/>')
            for x in (90, 630):
                elements.append(f'<circle cx="{x}" cy="{baseline}" r="5" fill="{INK}"/>')
            for x, label in ((90, "0 m"), (360, "沿弦位置"), (630, "1 m")):
                elements.append(text(x, baseline + 55, label, 22, MUTED, "middle"))
            if index == 1:
                for x in (270, 450):
                    elements += [
                        f'<circle cx="{x}" cy="{baseline}" r="5" fill="{ORANGE}"/>',
                        text(x, baseline + 55, "节点", 22, ORANGE, "middle"),
                    ]
        elements += [
            text(36, 1037, "理想均匀张紧弦、两端固定、小振幅；f₃ = 3f₁。", 24, MUTED),
            text(36, 1076, "位移单位为 mm；横纵单位不同，外形非实物比例。", 24, MUTED),
        ]
        return document(
            1110, "第一与第三弦振型在同一时刻的叠加",
            "一米长的理想弦，第一振型振幅一毫米、频率五十赫兹；"
            "第三振型振幅零点三五毫米、频率一百五十赫兹，有两个内部节点。"
            "下图逐点相加，展示复杂形状如何由简单振型组成；不表现时间演变。",
            elements,
        )

    def recurring_decimal():
        remainder = 1
        steps = []
        for index in range(6):
            digit, new_remainder = divmod(remainder * 10, 7)
            steps.append((index + 1, remainder, digit, new_remainder))
            remainder = new_remainder
        assert remainder == 1
        assert "".join(str(step[2]) for step in steps) == "142857"
        assert all(1 <= step[3] <= 6 for step in steps)
        assert 142857 * 7 == 999999
        elements = [
            text(36, 48, "循环小数：为什么会回到起点？", 32),
            text(36, 86, "每一步：原余数乘 10，再除以 7。", 24, MUTED),
            text(36, 130, "从 1 ÷ 7 的余数 1 开始往下读。", 26),
            '<rect x="24" y="155" width="672" height="520" rx="16" fill="#fff" stroke="#c9d6df"/>',
        ]
        for x, heading in ((80, "步骤"), (235, "原余数 × 10"), (435, "商的这一位"), (605, "新余数")):
            elements.append(text(x, 191, heading, 23, MUTED, "middle"))
        for index, old, digit, new in steps:
            y = 240 + 78 * (index - 1)
            if index == 6:
                elements.append(f'<rect x="38" y="{y-36}" width="644" height="60" rx="10" fill="#e1f0f5"/>')
            for x, label in ((80, str(index)), (235, f"{old} × 10"), (435, str(digit)), (605, str(new))):
                elements.append(text(x, y, label, 28, BLUE if x == 435 else INK, "middle"))
        elements += [
            text(36, 719, "余数回到 1 → 后面的步骤与数字原样重复。", 26),
            text(36, 765, "得到：0.142857142857…，周期为 6。", 28, BLUE),
            text(36, 816, "教学例子，不声称该小数由约翰三世发现。", 24, MUTED),
        ]
        return document(
            850, "一除以七的六步余数循环",
            "每步从旧余数乘十后除以七，依次得到数字一四二八五七；"
            "新余数依次为三、二、六、四、五、一，回到起点，所以循环重现。",
            elements,
        )

    def main():
        OUT.mkdir(parents=True, exist_ok=True)
        for name, content in (
            ("bernoulli-family-tree.svg", family_tree()),
            ("spiral-comparison.svg", spiral_comparison()),
            ("large-numbers.svg", large_numbers()),
            ("orthogonal-trajectories.svg", orthogonal_trajectories()),
            ("fluid-energy.svg", fluid_energy()),
            ("string-modes.svg", string_modes()),
            ("recurring-decimal.svg", recurring_decimal()),
        ):
            ET.fromstring(content)
            (OUT / name).write_text(content, encoding="utf-8")
            print(f"Wrote {name}")

    main()


# ---------------------------------------------------------------------------
# Cauchy Residue Integral & Uniform Convergence Extensions + Pascal & Eudoxus
# ---------------------------------------------------------------------------
def _build_cauchy_extensions():
    def build_semicircle_residue_eval():
        # Numerical verification of contour integral for f(z) = 1 / (1 + z^2)
        R = 6.0
        n_steps = 4000
        # Real segment [-R, R]
        dx = (2.0 * R) / n_steps
        real_integral = sum(1.0 / (1.0 + (-R + (i + 0.5) * dx) ** 2) for i in range(n_steps)) * dx
        # Upper semicircle z = R * exp(i * theta), theta in [0, pi]
        dtheta = math.pi / n_steps
        arc_integral = 0j
        for i in range(n_steps):
            th = (i + 0.5) * dtheta
            z = R * complex(math.cos(th), math.sin(th))
            dz = 1j * z * dtheta
            arc_integral += dz / (1.0 + z * z)
        total_contour = real_integral + arc_integral
        assert abs(total_contour - math.pi) < 1e-6, f"Contour mismatch: {total_contour}"
        arc_bound = math.pi * R / (R * R - 1.0)
        assert abs(arc_integral) <= arc_bound + 1e-9

        el = []
        el += header(
            "用柯西留数定理秒杀实数反常积分：∫₋∞^∞ dx/(1+x²) = π",
            "不求反正切原函数，借上半复平面 D 形闭合围线包住唯一奇点 z = i，三步直接读出答案",
        )

        # Left panel: Complex plane D-contour
        el.append(card(20, 66, 356, 314))
        el.append(txt(36, 90, "上半复平面闭合围线 C_R", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(236, 74, "只包住 z = +i", fg=ORANGE, bg=ORANGE_SOFT, w=126, h=22, size=11.5))

        cx, cy = 192.0, 248.0
        rad = 108.0

        # Shaded D-contour interior
        el.append(
            f'<path d="M {cx - rad:.1f},{cy:.1f} L {cx + rad:.1f},{cy:.1f} '
            f'A {rad:.1f},{rad:.1f} 0 0 0 {cx - rad:.1f},{cy:.1f} Z" '
            f'fill="{BLUE_SOFT}" fill-opacity="0.58" stroke="none"/>'
        )

        # Axes: Re z and Im z
        el.append(
            f'<line x1="40" y1="{cy:.1f}" x2="356" y2="{cy:.1f}" '
            f'stroke="{SLATE}" stroke-width="1.3" marker-end="url(#arr-muted)"/>'
        )
        el.append(
            f'<line x1="{cx:.1f}" y1="336" x2="{cx:.1f}" y2="112" '
            f'stroke="{SLATE}" stroke-width="1.3" marker-end="url(#arr-muted)"/>'
        )
        el.append(txt(354, cy - 8, "实轴 Re", size=11.5, color=MUTED, anchor="end"))
        el.append(txt(cx + 8, 120, "虚轴 Im", size=11.5, color=MUTED))

        # Real segment [-R, R] highlighted in BLUE with forward arrows
        el.append(
            f'<line x1="{cx - rad:.1f}" y1="{cy:.1f}" x2="{cx - 18:.1f}" y2="{cy:.1f}" '
            f'stroke="{BLUE}" stroke-width="3.0" marker-end="url(#arr-blue)"/>'
        )
        el.append(
            f'<line x1="{cx - 22:.1f}" y1="{cy:.1f}" x2="{cx + rad:.1f}" y2="{cy:.1f}" '
            f'stroke="{BLUE}" stroke-width="3.0"/>'
        )
        el.append(
            f'<line x1="{cx + 20:.1f}" y1="{cy:.1f}" x2="{cx + 56:.1f}" y2="{cy:.1f}" '
            f'stroke="{BLUE}" stroke-width="3.0" marker-end="url(#arr-blue)"/>'
        )

        # Semicircle arc Gamma_R in PURPLE (counterclockwise from +R to -R)
        th_mid = math.radians(60)
        mx = cx + rad * math.cos(th_mid)
        my = cy - rad * math.sin(th_mid)
        el.append(
            f'<path d="M {cx + rad:.1f},{cy:.1f} A {rad:.1f},{rad:.1f} 0 0 0 {mx:.1f},{my:.1f}" '
            f'fill="none" stroke="{PURPLE}" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#arr-purple)"/>'
        )
        el.append(
            f'<path d="M {mx:.1f},{my:.1f} A {rad:.1f},{rad:.1f} 0 0 0 {cx - rad:.1f},{cy:.1f}" '
            f'fill="none" stroke="{PURPLE}" stroke-width="2.5" stroke-dasharray="6 4"/>'
        )

        # Radial arrow showing R -> inf
        th_r = math.radians(132)
        rx_end = cx + rad * math.cos(th_r)
        ry_end = cy - rad * math.sin(th_r)
        el.append(
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{rx_end:.1f}" y2="{ry_end:.1f}" '
            f'stroke="{PURPLE}" stroke-width="1.4" stroke-dasharray="3 3"/>'
        )
        el.append(txt(cx - 54, cy - 40, "半径 R → ∞", size=11.5, color=PURPLE, anchor="middle", weight="600", halo=True))
        el.append(txt(cx + 84, cy - 88, "上半圆弧 Γ_R", size=12, color=PURPLE, anchor="middle", weight="600", halo=True))

        # Ticks -R, 0, +R
        for tx, lbl in [(cx - rad, "-R"), (cx, "0"), (cx + rad, "+R")]:
            el.append(f'<circle cx="{tx:.1f}" cy="{cy:.1f}" r="3.2" fill="{INK}"/>')
            offset_x = -8 if lbl == "0" else 0
            el.append(txt(tx + offset_x, cy + 19, lbl, size=12, color=INK, anchor="middle", weight="600"))

        # Enclosed pole z = +i
        py_pos = cy - 50.0
        el.append(
            f'<path d="M {cx + 16:.1f},{py_pos:.1f} A 16,16 0 1 0 {cx + 11.3:.1f},{py_pos + 11.3:.1f}" '
            f'fill="none" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>'
        )
        el.append(f'<circle cx="{cx:.1f}" cy="{py_pos:.1f}" r="5.5" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')
        el.append(txt(cx + 22, py_pos - 3, "圈内奇点 z = +i", size=12, color=ORANGE, weight="700", halo=True))
        el.append(txt(cx + 22, py_pos + 14, "留数 Res = 1/(2i)", size=11.5, color=BODY, halo=True))

        # Excluded pole z = -i below real axis
        py_neg = cy + 50.0
        el.append(
            f'<circle cx="{cx:.1f}" cy="{py_neg:.1f}" r="5.2" fill="#ffffff" '
            f'stroke="{MUTED}" stroke-width="1.8" stroke-dasharray="2.5 2"/>'
        )
        el.append(txt(cx + 13, py_neg + 4, "圈外奇点 z = -i（不计入）", size=11.5, color=MUTED))

        el.append(
            txt(
                198,
                364,
                "实轴段 [-R, R]（蓝）与半圆弧 Γ_R（紫）围成 D 形圈",
                size=11.5,
                color=MUTED,
                anchor="middle",
            )
        )

        # Right panel: 3-step residue ledger
        el.append(card(390, 66, 350, 314))
        el.append(txt(408, 90, "三步算清整圈账本（无需原函数）", size=PANEL_TITLE, color=INK, weight="700"))

        # Step 1 card
        el.append(card(404, 104, 322, 70, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE, sw=1))
        el.append(step_badge(422, 122, 1, fg=BLUE, bg="#ffffff"))
        el.append(txt(440, 126, "把实轴积分嵌入闭合围线", size=12.5, color=BLUE, weight="700"))
        el.append(txt(418, 147, "∮_C f(z)dz = ∫₋R^R dx/(1+x²) + ∫_Γ f(z)dz", size=11.5, color=INK, cls="mono"))
        el.append(txt(418, 165, "1+z² = (z-i)(z+i)，上半平面仅包住 z = i", size=11.5, color=BODY))

        # Step 2 card
        el.append(card(404, 184, 322, 76, rx=8, fill=PURPLE_SOFT, stroke=PURPLE, sw=1))
        el.append(step_badge(422, 202, 2, fg=PURPLE, bg="#ffffff"))
        el.append(txt(440, 206, "估界证明：半圆弧贡献随 R → ∞ 归零", size=12.5, color=PURPLE, weight="700"))
        el.append(txt(418, 227, "|z| = R 时 |1+z²| ≥ R²-1，半圆弧长 = πR", size=11.5, color=BODY))
        el.append(txt(418, 247, "|∫_Γ| ≤ πR/(R²-1) → 0（分母 R² 压倒分子 R）", size=11.5, color=INK, weight="600"))

        # Step 3 card
        el.append(card(404, 270, 322, 96, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.2))
        el.append(step_badge(422, 288, 3, fg=GREEN, bg="#ffffff"))
        el.append(txt(440, 292, "留数定理一锤定音", size=12.5, color=GREEN, weight="700"))
        el.append(txt(418, 313, "Res(i) = 1/(z+i)|_{z=i} = 1/(2i)", size=11.5, color=INK, cls="mono"))
        el.append(txt(418, 333, "整圈积分 = 2πi × 1/(2i) = π（与 R 无关）", size=11.5, color=BODY))
        el.append(txt(418, 354, "令 R → ∞：∫₋∞^∞ dx/(1+x²) = π - 0 = π", size=12, color=GREEN, weight="700"))

        extra_defs = f"""
        <marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
          <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{PURPLE}"/>
        </marker>
        """

        svg = figure(
            396,
            "用柯西留数定理计算实数反常积分 dx/(1+x²) 等于 π",
            "左图展示上半复平面半径为 R 的 D 形闭合围线包住奇点 z=i 并排除 z=-i；右图分三步展示围线拆分、半圆弧积分按 πR/(R²-1) 趋于零，以及留数 2πi 乘 1/(2i) 得到 π。",
            el,
            extra_defs=extra_defs,
        )
        write_svg("cauchy", "semicircle-residue-eval.svg", svg)


    def partial_sawtooth(x, n_terms):
        return sum(((-1) ** (k + 1)) * math.sin(k * x) / k for k in range(1, n_terms + 1))


    def build_pointwise_vs_uniform_sum():
        # Numerical checks on S_N(x) = sum_{k=1}^N (-1)^{k+1} sin(k x) / k
        for n_chk in (1, 3, 15, 80):
            assert abs(partial_sawtooth(math.pi, n_chk)) < 1e-12
        assert abs(partial_sawtooth(1.2, 400) - 0.6) < 5e-3
        assert abs(partial_sawtooth(4.5, 400) - (4.5 - 2 * math.pi) / 2) < 5e-3

        el = []
        el += header(
            "柯西 1821 年的疏忽与阿贝尔反例：光滑正弦波怎样叠出垂直断崖？",
            "S_N(x) = Σ (-1)^(k+1) sin(kx)/k 的每一项都处处连续，但无穷和在 x = π 处从 +π/2 骤降到 -π/2",
        )

        # Left panel: Fourier sawtooth partial sums plot on [0, 2*pi]
        el.append(card(20, 66, 430, 322))
        el.append(txt(38, 90, "部分和 S₁, S₃, S₁₅ 逼近锯齿断崖（x ∈ [0, 2π]）", size=PANEL_TITLE, color=INK, weight="700"))

        px0, px1 = 66.0, 426.0
        py_mid = 232.0
        y_scale = 58.0  # 1 unit in y = 58px; pi/2 (~1.571) = 91.1px

        def sx(xv):
            return px0 + (xv / (2.0 * math.pi)) * (px1 - px0)

        def sy(yv):
            return py_mid - yv * y_scale

        # Horizontal gridlines at +pi/2, 0, -pi/2
        y_top = sy(math.pi / 2)
        y_bot = sy(-math.pi / 2)
        x_pi = sx(math.pi)

        el.append(f'<line x1="{px0:.1f}" y1="{y_top:.1f}" x2="{px1:.1f}" y2="{y_top:.1f}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="4 4"/>')
        el.append(f'<line x1="{px0:.1f}" y1="{y_bot:.1f}" x2="{px1:.1f}" y2="{y_bot:.1f}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="4 4"/>')
        el.append(f'<line x1="{px0:.1f}" y1="{py_mid:.1f}" x2="{px1 + 8:.1f}" y2="{py_mid:.1f}" stroke="{SLATE}" stroke-width="1.2" marker-end="url(#arr-muted)"/>')
        el.append(f'<line x1="{px0:.1f}" y1="344" x2="{px0:.1f}" y2="118" stroke="{SLATE}" stroke-width="1.2" marker-end="url(#arr-muted)"/>')

        # Y ticks
        el.append(txt(px0 - 7, y_top + 4, "+π/2", size=11.5, color=GREEN, anchor="end", weight="600"))
        el.append(txt(px0 - 7, py_mid + 4, "0", size=11.5, color=MUTED, anchor="end"))
        el.append(txt(px0 - 7, y_bot + 4, "-π/2", size=11.5, color=GREEN, anchor="end", weight="600"))

        # X ticks
        for xv, xlbl in [(0.0, "0"), (math.pi / 2, "π/2"), (math.pi, "π"), (1.5 * math.pi, "3π/2"), (2.0 * math.pi, "2π")]:
            tx = sx(xv)
            el.append(f'<line x1="{tx:.1f}" y1="{py_mid - 3:.1f}" x2="{tx:.1f}" y2="{py_mid + 3:.1f}" stroke="{SLATE}" stroke-width="1.2"/>')
            ly = py_mid + 18 if xv != math.pi else py_mid + 21
            col = ORANGE if xv == math.pi else MUTED
            wt = "700" if xv == math.pi else None
            if xv == math.pi:
                el.append(txt(tx - 12, ly, "π", size=12, color=col, anchor="middle", weight=wt, halo=True))
            else:
                el.append(txt(tx, ly, xlbl, size=11.5, color=col, anchor="middle", weight=wt))

        # Vertical cliff highlight band around x = pi
        el.append(
            f'<rect x="{x_pi - 10:.1f}" y="{y_top - 8:.1f}" width="20" height="{y_bot - y_top + 16:.1f}" '
            f'rx="6" fill="{ORANGE_SOFT}" fill-opacity="0.65" stroke="none"/>'
        )
        el.append(
            f'<line x1="{x_pi:.1f}" y1="{y_top:.1f}" x2="{x_pi:.1f}" y2="{y_bot:.1f}" '
            f'stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="4 3"/>'
        )

        # Exact limiting sawtooth segments: y = x/2 on [0, pi), and y = (x - 2*pi)/2 on (pi, 2*pi]
        el.append(
            f'<line x1="{sx(0):.1f}" y1="{sy(0):.1f}" x2="{sx(math.pi - 0.02):.1f}" y2="{sy((math.pi - 0.02)/2):.1f}" '
            f'stroke="{GREEN}" stroke-width="2.0" stroke-dasharray="6 4"/>'
        )
        el.append(
            f'<line x1="{sx(math.pi + 0.02):.1f}" y1="{sy((math.pi + 0.02 - 2*math.pi)/2):.1f}" x2="{sx(2*math.pi):.1f}" y2="{sy(0):.1f}" '
            f'stroke="{GREEN}" stroke-width="2.0" stroke-dasharray="6 4"/>'
        )

        # Partial sum polylines: S_1, S_3, S_15
        n_pts = 360
        for n_terms, stroke_col, sw, op in [
            (1, "#94a3b8", "1.6", "0.95"),
            (3, BLUE, "2.0", "0.95"),
            (15, ORANGE, "2.5", "1.0"),
        ]:
            pts = []
            for i in range(n_pts + 1):
                xv = (2.0 * math.pi * i) / n_pts
                yv = partial_sawtooth(xv, n_terms)
                pts.append(f"{sx(xv):.2f},{sy(yv):.2f}")
            el.append(
                f'<polyline points="{" ".join(pts)}" fill="none" stroke="{stroke_col}" '
                f'stroke-width="{sw}" stroke-opacity="{op}" stroke-linejoin="round"/>'
            )

        # Open circles at jump endpoints (pi, +pi/2) and (pi, -pi/2), solid dot at (pi, 0)
        el.append(f'<circle cx="{x_pi:.1f}" cy="{y_top:.1f}" r="4.5" fill="#ffffff" stroke="{GREEN}" stroke-width="2"/>')
        el.append(f'<circle cx="{x_pi:.1f}" cy="{y_bot:.1f}" r="4.5" fill="#ffffff" stroke="{GREEN}" stroke-width="2"/>')
        el.append(f'<circle cx="{x_pi:.1f}" cy="{py_mid:.1f}" r="4.8" fill="{INK}" stroke="#ffffff" stroke-width="1.5"/>')

        # Clean non-overlapping curve & jump callouts
        el.append(txt(sx(1.15), sy(0.58) - 12, "极限斜线 x/2", size=11.5, color=GREEN, anchor="middle", weight="600", halo=True))
        el.append(txt(x_pi + 14, y_top + 4, "左极限 +π/2", size=11.5, color=GREEN, weight="600", halo=True))
        el.append(txt(x_pi - 14, y_bot + 4, "右极限 -π/2", size=11.5, color=GREEN, anchor="end", weight="600", halo=True))
        el.append(txt(x_pi + 13, py_mid - 7, "S_N(π) = 0 恒成立", size=11.5, color=INK, weight="700", halo=True))

        # Legend row at bottom of left panel
        ly_leg = 368
        el.append(f'<line x1="42" y1="{ly_leg - 4}" x2="64" y2="{ly_leg - 4}" stroke="#94a3b8" stroke-width="2"/>')
        el.append(txt(69, ly_leg, "S₁ (1项)", size=11.5, color=MUTED))
        el.append(f'<line x1="132" y1="{ly_leg - 4}" x2="154" y2="{ly_leg - 4}" stroke="{BLUE}" stroke-width="2.2"/>')
        el.append(txt(159, ly_leg, "S₃ (3项)", size=11.5, color=BLUE, weight="600"))
        el.append(f'<line x1="222" y1="{ly_leg - 4}" x2="244" y2="{ly_leg - 4}" stroke="{ORANGE}" stroke-width="2.6"/>')
        el.append(txt(249, ly_leg, "S₁₅ (15项陡崖)", size=11.5, color=ORANGE, weight="700"))
        el.append(f'<line x1="350" y1="{ly_leg - 4}" x2="372" y2="{ly_leg - 4}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 3"/>')
        el.append(txt(377, ly_leg, "无穷极限", size=11.5, color=GREEN, weight="600"))

        # Right panel: 3 historical & mathematical stages
        el.append(card(464, 66, 276, 322))
        el.append(txt(482, 90, "为什么光滑波会叠出断崖？", size=PANEL_TITLE, color=INK, weight="700"))

        # Box 1
        el.append(card(478, 104, 248, 82, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1))
        el.append(step_badge(496, 124, 1, fg=ORANGE, bg="#ffffff"))
        el.append(txt(514, 128, "1821 柯西的隐蔽滑步", size=12.5, color=ORANGE, weight="700"))
        el.append(txt(490, 149, "柯西证明“连续函数之和仍连续”时，", size=11.5, color=BODY))
        el.append(txt(490, 168, "默认同一个项数 N 能同时按住所有 x。", size=11.5, color=INK, weight="600"))

        # Box 2
        el.append(card(478, 196, 248, 86, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE, sw=1))
        el.append(step_badge(496, 216, 2, fg=BLUE, bg="#ffffff"))
        el.append(txt(514, 220, "1826 阿贝尔的锯齿波反例", size=12.5, color=BLUE, weight="700"))
        el.append(txt(490, 241, "x 越靠近 π，每项 sin(kx) 越微弱；", size=11.5, color=BODY))
        el.append(txt(490, 260, "想追近 +π/2，所需项数 N(x) → ∞，", size=11.5, color=BODY))
        el.append(txt(490, 276, "断崖旁总有“还没收敛到位”的滞后点！", size=11.5, color=INK, weight="600"))

        # Box 3
        el.append(card(478, 292, 248, 84, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.2))
        el.append(step_badge(496, 312, 3, fg=GREEN, bg="#ffffff"))
        el.append(txt(514, 316, "魏尔斯特拉斯补齐：一致收敛", size=12.5, color=GREEN, weight="700"))
        el.append(txt(490, 337, "• 逐点收敛：先定 x，再找 N(ε, x)", size=11.5, color=BODY))
        el.append(txt(490, 356, "• 一致收敛：同一个 N(ε) 通吃全体 x", size=11.5, color=GREEN, weight="700"))
        el.append(txt(490, 371, "唯有“齐步进窄带”才保住极限连续！", size=11, color=INK))

        svg = figure(
            404,
            "柯西 1821 年连续性定理疏忽与阿贝尔 1826 年傅里叶锯齿波反例（逐点收敛与一致收敛对比）",
            "左图精确绘制交错正弦级数前 1、3、15 项部分和在 [0, 2π] 上逼近锯齿线并在 x=π 处形成 ±π/2 跳跃间断；右图分三步解释柯西 1821 年漏掉项数 N 对 x 的依赖、阿贝尔反例机制及魏尔斯特拉斯一致收敛判据。",
            el,
        )
        write_svg("cauchy", "pointwise-vs-uniform-sum.svg", svg)

    build_semicircle_residue_eval()
    build_pointwise_vs_uniform_sum()


def _projective_and_eudoxus_suite():
    RED = "#c81e3a"
    RED_SOFT = "#fde8ec"
    TEAL = "#0f766e"
    TEAL_SOFT = "#e6f7f5"
    AMBER = "#b45309"
    AMBER_SOFT = "#fef3c7"


    # ---------------------------------------------------------------------------
    # Exact 2D & 3D Projective Geometry Helpers
    # ---------------------------------------------------------------------------
    def line_inter(p1, p2, p3, p4):
        """Exact intersection of line p1-p2 and line p3-p4."""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        assert abs(den) > 1e-11, f"Near-parallel lines: {p1}-{p2} and {p3}-{p4}"
        c1 = x1 * y2 - y1 * x2
        c2 = x3 * y4 - y3 * x4
        px = (c1 * (x3 - x4) - (x1 - x2) * c2) / den
        py = (c1 * (y3 - y4) - (y1 - y2) * c2) / den
        return (px, py)


    def collinear_det(p1, p2, p3):
        """Signed 2x area determinant of (p1, p2, p3)."""
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


    def signed_ratio(a, b, c):
        """Signed directed ratio (a -> b) / (b -> c) for collinear points a, b, c."""
        assert abs(collinear_det(a, b, c)) < 1e-8
        dx, dy = c[0] - b[0], c[1] - b[1]
        if abs(dx) >= abs(dy):
            return (b[0] - a[0]) / dx
        return (b[1] - a[1]) / dy


    def span_line(pts, pad=14.0, box=None):
        """Return endpoints covering all given collinear points plus padding, optionally clipped to box."""
        p0 = pts[0]
        p1 = max(pts[1:], key=lambda q: math.dist(p0, q))
        ux = (p1[0] - p0[0]) / math.dist(p0, p1)
        uy = (p1[1] - p0[1]) / math.dist(p0, p1)
        ts = [(q[0] - p0[0]) * ux + (q[1] - p0[1]) * uy for q in pts]
        tmin, tmax = min(ts) - pad, max(ts) + pad
        if box is not None:
            bx0, by0, bx1, by1 = box
            lo, hi = -1e9, 1e9
            for coord, u, bmin, bmax in ((p0[0], ux, bx0, bx1), (p0[1], uy, by0, by1)):
                if abs(u) > 1e-9:
                    t1, t2 = (bmin - coord) / u, (bmax - coord) / u
                    lo = max(lo, min(t1, t2))
                    hi = min(hi, max(t1, t2))
            tmin = max(tmin, lo)
            tmax = min(tmax, hi)
        return (p0[0] + tmin * ux, p0[1] + tmin * uy), (p0[0] + tmax * ux, p0[1] + tmax * uy)


    def seg_svg(p1, p2, color=SLATE, sw=1.8, dash=None, opacity=None, marker_end=None):
        attrs = [
            f'x1="{p1[0]:.2f}"',
            f'y1="{p1[1]:.2f}"',
            f'x2="{p2[0]:.2f}"',
            f'y2="{p2[1]:.2f}"',
            f'stroke="{color}"',
            f'stroke-width="{sw}"',
            'stroke-linecap="round"',
        ]
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'stroke-opacity="{opacity}"')
        if marker_end:
            attrs.append(f'marker-end="url(#{marker_end})"')
        return f'<line {" ".join(attrs)}/>'


    def dot_svg(p, r=4.2, fill=CARD_BG, stroke=INK, sw=1.8):
        return (
            f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )


    def poly_svg(pts, fill="none", stroke=SLATE, sw=1.5, fill_opacity=None, dash=None, closed=True):
        coords = " ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in pts)
        cmd = f"M {coords} Z" if closed else "M " + " L ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in pts)
        attrs = [f'd="{cmd}"', f'fill="{fill}"', f'stroke="{stroke}"', f'stroke-width="{sw}"', 'stroke-linejoin="round"']
        if fill_opacity is not None:
            attrs.append(f'fill-opacity="{fill_opacity}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        return f'<path {" ".join(attrs)}/>'


    # ---------------------------------------------------------------------------
    # 1. Pascal Menelaus + Power-of-a-Point + 3D Conic Projection SVG
    # ---------------------------------------------------------------------------
    def build_pascal_menelaus_proof():
        # Exact unit-circle star hexagon configuration with wide separation among all 12 points
        degs = [101.3, 279.7, 232.1, 350.2, 137.1, 189.7]
        rads = [math.radians(d) for d in degs]
        pts_u = [(math.cos(a), math.sin(a)) for a in rads]
        A, B, C, D, E, F = pts_u
        for p in pts_u:
            assert abs(math.hypot(p[0], p[1]) - 1.0) < 1e-12

        # Reference triangle UVW formed by alternating edges AB (1), CD (3), EF (5)
        U = line_inter(A, B, C, D)  # AB cap CD
        V = line_inter(C, D, E, F)  # CD cap EF
        W = line_inter(E, F, A, B)  # EF cap AB

        # Pascal intersections of opposite edges
        P = line_inter(A, B, D, E)  # AB cap DE (on side WU)
        Q = line_inter(B, C, E, F)  # BC cap EF (on side VW)
        R = line_inter(C, D, F, A)  # CD cap FA (on side UV)

        # Verify Menelaus on Delta UVW for the 3 remaining edges DE, BC, FA
        m_pde = signed_ratio(W, P, U) * signed_ratio(U, D, V) * signed_ratio(V, E, W)
        m_bcq = signed_ratio(W, B, U) * signed_ratio(U, C, V) * signed_ratio(V, Q, W)
        m_arf = signed_ratio(W, A, U) * signed_ratio(U, R, V) * signed_ratio(V, F, W)
        assert abs(m_pde + 1.0) < 1e-9, f"Menelaus PDE failed: {m_pde}"
        assert abs(m_bcq + 1.0) < 1e-9, f"Menelaus BCQ failed: {m_bcq}"
        assert abs(m_arf + 1.0) < 1e-9, f"Menelaus ARF failed: {m_arf}"

        # Verify Power of a Point at U, V, W (signed directed products)
        def dprod(o, p1, p2):
            # signed scalar product along line through o
            dx1, dy1 = p1[0] - o[0], p1[1] - o[1]
            dx2, dy2 = p2[0] - o[0], p2[1] - o[1]
            return dx1 * dx2 + dy1 * dy2

        pow_U1, pow_U2 = dprod(U, A, B), dprod(U, C, D)
        pow_V1, pow_V2 = dprod(V, C, D), dprod(V, E, F)
        pow_W1, pow_W2 = dprod(W, E, F), dprod(W, A, B)
        assert abs(pow_U1 / pow_U2 - 1.0) < 1e-9
        assert abs(pow_V1 / pow_V2 - 1.0) < 1e-9
        assert abs(pow_W1 / pow_W2 - 1.0) < 1e-9

        # Verify Converse of Menelaus & collinearity of P, Q, R
        m_pqr = signed_ratio(W, P, U) * signed_ratio(U, R, V) * signed_ratio(V, Q, W)
        assert abs(m_pqr + 1.0) < 1e-9
        assert abs(collinear_det(P, Q, R)) < 1e-9

        # Map Left Panel coordinates cleanly into card (20, 66, 392, 356)
        # World span: x in [-1.72, +1.00], y in [-1.22, +1.91] -> flip y for SVG!
        scale_l = 86.0
        cx_l, cy_l = 248.0, 266.0

        def map_l(pt):
            return (cx_l + pt[0] * scale_l, cy_l - pt[1] * scale_l)

        Al, Bl, Cl, Dl, El_p, Fl = [map_l(p) for p in (A, B, C, D, E, F)]
        Ul, Vl, Wl = [map_l(p) for p in (U, V, W)]
        Pl, Ql, Rl = [map_l(p) for p in (P, Q, R)]
        assert abs(collinear_det(Pl, Ql, Rl)) < 1e-6

        el = []
        el += header(
            "初等几何四步证完帕斯卡定理：基准三角形 + 圆幂约分 + 中心投影",
            "先在圆上借 ΔUVW 连用三次梅涅劳斯定理并用圆幂成对消去 12 段弦长，再用一束中心投影推广到任意圆锥曲线",
        )

        # ---- Left Card: Circle Proof ----
        el.append(card(20, 66, 392, 358))
        el.append(txt(34, 89, "①–③ 圆上证明：ΔUVW 与圆幂相消", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(284, 73, "12 段弦长全约掉", fg=BLUE, bg=BLUE_SOFT, w=116, h=22, size=11.5))

        # Shaded reference triangle UVW
        el.append(poly_svg([Ul, Vl, Wl], fill=BLUE_SOFT, stroke=BLUE, sw=2.1, fill_opacity=0.42))

        # Circle O
        el.append(
            f'<circle cx="{cx_l:.2f}" cy="{cy_l:.2f}" r="{scale_l:.2f}" '
            f'fill="none" stroke="{SLATE}" stroke-width="1.8"/>'
        )

        lbox = (30.0, 102.0, 402.0, 412.0)
        # Alternating carrier lines (sides of UVW): AB -> WU, CD -> UV, EF -> VW
        for pts_col in ([Wl, Al, Pl, Ul, Bl], [Vl, Rl, Cl, Ul, Dl], [Wl, El_p, Fl, Ql, Vl]):
            s0, s1 = span_line(pts_col, pad=8.0, box=lbox)
            el.append(seg_svg(s0, s1, color=BLUE, sw=1.7, opacity=0.85))

        # Three transversal edges: DE (orange -> P), BC (green -> Q), FA (purple -> R)
        for pts_tr, col in (
            ([Dl, Pl, El_p], ORANGE),
            ([Bl, Cl, Ql], GREEN),
            ([Fl, Al, Rl], PURPLE),
        ):
            s0, s1 = span_line(pts_tr, pad=9.0, box=lbox)
            el.append(seg_svg(s0, s1, color=col, sw=1.9, dash="5 3"))

        # Red Pascal line through P, Q, R
        p0, p1 = span_line([Pl, Ql, Rl], pad=18.0, box=lbox)
        el.append(seg_svg(p0, p1, color=RED, sw=2.7))

        # Draw vertices A..F (circle points)
        for pt in (Al, Bl, Cl, Dl, El_p, Fl):
            el.append(dot_svg(pt, r=4.0, fill=CARD_BG, stroke=INK, sw=1.8))

        # Draw vertices U, V, W (reference triangle)
        for pt in (Ul, Vl, Wl):
            el.append(dot_svg(pt, r=4.6, fill=BLUE, stroke=CARD_BG, sw=1.6))

        # Draw Pascal points P, Q, R
        for pt, col in ((Pl, ORANGE), (Ql, GREEN), (Rl, PURPLE)):
            el.append(dot_svg(pt, r=5.0, fill=col, stroke=CARD_BG, sw=1.8))

        # Carefully placed non-overlapping labels in Left Panel
        lbl_l = [
            (Al[0] + 10, Al[1] - 4, "A", INK, "start", "700"),
            (Bl[0] + 9, Bl[1] + 12, "B", INK, "start", "700"),
            (Cl[0] - 4, Cl[1] + 17, "C", INK, "middle", "700"),
            (Dl[0] + 9, Dl[1] + 5, "D", INK, "start", "700"),
            (El_p[0] - 11, El_p[1] - 5, "E", INK, "end", "700"),
            (Fl[0] - 11, Fl[1] - 4, "F", INK, "end", "700"),
            (Ul[0] + 10, Ul[1] + 3, "U", BLUE, "start", "700"),
            (Vl[0] + 4, Vl[1] + 18, "V", BLUE, "start", "700"),
            (Wl[0] + 10, Wl[1] + 5, "W", BLUE, "start", "700"),
            (Pl[0] + 10, Pl[1] + 4, "P", ORANGE, "start", "700"),
            (Ql[0] - 10, Ql[1] - 7, "Q", GREEN, "end", "700"),
            (Rl[0] - 9, Rl[1] - 7, "R", PURPLE, "end", "700"),
        ]
        for lx, ly, s, col, anc, wt in lbl_l:
            el.append(txt(lx, ly, s, size=12, color=col, anchor=anc, weight=wt, halo=True))

        el.append(txt(56, 398, "红线：帕斯卡线 P–Q–R", size=11.5, color=RED, weight="700", halo=True))
        el.append(txt(244, 413, "蓝框：基准三角形 ΔUVW", size=11.5, color=BLUE, weight="600"))

        # ---- Right Card: 3D Central Projection (Step 4) ----
        el.append(card(424, 66, 316, 358))
        el.append(txt(438, 89, "④ 中心投影：圆一键变圆锥曲线", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(634, 73, "射影保共线", fg=PURPLE, bg=PURPLE_SOFT, w=94, h=22, size=11.5))

        # Exact 3D central projection from apex S = (0, 0, 3.4)
        # Upper horizontal plane z = 1.85 carries a circle of radius r0 = 0.56
        # Lower tilted plane z = 0.22 * x + 0.14 * y + 0.35 cuts the cone in a genuine non-circular ellipse!
        S3 = (0.0, 0.0, 3.40)
        z_top = 1.85
        r_top = 0.58

        def proj_to_tilted(x, y, z):
            # Ray S + t * (P - S) meets z_plane = 0.22*X + 0.14*Y + 0.35
            dx, dy, dz = x - S3[0], y - S3[1], z - S3[2]
            # S_z + t*dz = 0.22*(S_x + t*dx) + 0.14*(S_y + t*dy) + 0.35
            num = 0.22 * S3[0] + 0.14 * S3[1] + 0.35 - S3[2]
            den = dz - 0.22 * dx - 0.14 * dy
            t = num / den
            return (S3[0] + t * dx, S3[1] + t * dy, S3[2] + t * dz)

        def cam2d(pt3):
            # Clean axonometric projection to Right Panel SVG coordinates
            x, y, z = pt3
            sx = 582.0 + (x * 100.0 - y * 42.0)
            sy = 338.0 - (z * 66.0 + y * 22.0 + x * 6.0)
            return (sx, sy)

        S2 = cam2d(S3)

        # Plane polygons: pi_1 (upper plane z = z_top) and pi_2 (lower tilted plane)
        pi1_corners_3d = [(-0.92, -0.82, z_top), (0.92, -0.82, z_top), (0.92, 0.82, z_top), (-0.92, 0.82, z_top)]
        pi2_corners_3d = [
            (x, y, 0.22 * x + 0.14 * y + 0.35)
            for (x, y) in [(-1.18, -1.02), (1.18, -1.02), (1.18, 1.02), (-1.18, 1.02)]
        ]
        el.append(poly_svg([cam2d(q) for q in pi2_corners_3d], fill=PURPLE_SOFT, stroke=PURPLE, sw=1.2, fill_opacity=0.36))
        el.append(poly_svg([cam2d(q) for q in pi1_corners_3d], fill=BLUE_SOFT, stroke=BLUE, sw=1.2, fill_opacity=0.45))

        # Sample circle on pi_1 and exact projected conic on pi_2
        circ_3d = [
            (r_top * math.cos(2 * math.pi * i / 72), r_top * math.sin(2 * math.pi * i / 72), z_top)
            for i in range(73)
        ]
        conic_3d = [proj_to_tilted(*q) for q in circ_3d]
        el.append(poly_svg([cam2d(q) for q in conic_3d], fill="none", stroke=PURPLE, sw=2.1, closed=False))
        el.append(poly_svg([cam2d(q) for q in circ_3d], fill="none", stroke=BLUE, sw=1.9, closed=False))

        # Cone silhouette generators from S to left/right tangents
        for idx in (0, 36):
            el.append(seg_svg(S2, cam2d(conic_3d[idx]), color=HAIRLINE, sw=1.2, dash="4 3"))

        # Pick 3 collinear points P0, Q0, R0 on pi_1 and project them to P', Q', R' on pi_2
        P0_3 = (-0.52, -0.22, z_top)
        R0_3 = (0.56, 0.18, z_top)
        Q0_3 = (0.5 * (P0_3[0] + R0_3[0]), 0.5 * (P0_3[1] + R0_3[1]), z_top)
        Pp_3 = proj_to_tilted(*P0_3)
        Qp_3 = proj_to_tilted(*Q0_3)
        Rp_3 = proj_to_tilted(*R0_3)

        P0_2, Q0_2, R0_2 = cam2d(P0_3), cam2d(Q0_3), cam2d(R0_3)
        Pp_2, Qp_2, Rp_2 = cam2d(Pp_3), cam2d(Qp_3), cam2d(Rp_3)
        assert abs(collinear_det(P0_2, Q0_2, R0_2)) < 1e-9
        assert abs(collinear_det(Pp_2, Qp_2, Rp_2)) < 1e-9

        # Shaded light-fan plane S - P' - R' showing straight line maps to straight line!
        el.append(poly_svg([S2, Pp_2, Rp_2], fill=RED_SOFT, stroke="none", sw=0, fill_opacity=0.35))
        for src, dst in ((P0_2, Pp_2), (Q0_2, Qp_2), (R0_2, Rp_2)):
            el.append(seg_svg(S2, dst, color=ORANGE, sw=1.25, dash="3 3"))
        el.append(seg_svg(P0_2, R0_2, color=RED, sw=2.1))
        el.append(seg_svg(Pp_2, Rp_2, color=RED, sw=2.5))

        for pt in (P0_2, Q0_2, R0_2):
            el.append(dot_svg(pt, r=3.3, fill=RED, stroke=CARD_BG, sw=1.2))
        for pt in (Pp_2, Qp_2, Rp_2):
            el.append(dot_svg(pt, r=3.8, fill=RED, stroke=CARD_BG, sw=1.4))
        el.append(dot_svg(S2, r=5.0, fill=ORANGE, stroke=CARD_BG, sw=1.8))

        el.append(txt(S2[0] + 10, S2[1] + 4, "投影中心 S（光源）", size=11.5, color=ORANGE, weight="700", halo=True))
        el.append(txt(442, 184, "平面 π₁：圆与 P,Q,R", size=11.5, color=BLUE, weight="700", halo=True))
        el.append(txt(442, 304, "截面 π₂：一般圆锥曲线", size=11.5, color=PURPLE, weight="700", halo=True))
        el.append(txt(Pp_2[0] - 8, Pp_2[1] + 15, "P'", size=11.5, color=RED, anchor="end", weight="700", halo=True))
        el.append(txt(Qp_2[0], Qp_2[1] + 16, "Q'", size=11.5, color=RED, anchor="middle", weight="700", halo=True))
        el.append(txt(Rp_2[0] + 8, Rp_2[1] + 14, "R'", size=11.5, color=RED, anchor="start", weight="700", halo=True))
        el.append(txt(438, 396, "三束视线张成同一平面 SPQR", size=11.5, color=BODY, weight="600"))
        el.append(txt(438, 413, "与斜面 π₂ 的交线必是直线 P'Q'R'！", size=11.5, color=RED, weight="700"))

        # ---- Bottom Card: 4-Step Proof Ledger ----
        el.append(card(20, 436, 720, 108, fill=CARD_BG))
        steps = [
            (36, "1", BLUE, BLUE_SOFT, "搭基准 ΔUVW", "隔开取边 AB、CD、EF", "两两相交围出 ΔUVW"),
            (212, "2", ORANGE, ORANGE_SOFT, "三次梅涅劳斯", "拿截线 DE、BC、FA", "各切 ΔUVW 三边写连乘"),
            (388, "3", GREEN, GREEN_SOFT, "圆幂成对约分", "UA·UB=UC·UD 等三组", "12 段弦全消，剩乘积=-1"),
            (564, "4", PURPLE, PURPLE_SOFT, "投影保结合性", "点在线上、线线相交不变", "圆的结论通杀一切圆锥曲线"),
        ]
        for sx, num, fg, bg, stitle, l1, l2 in steps:
            if sx > 36:
                el.append(seg_svg((sx - 10, 452), (sx - 10, 530), color=BORDER, sw=1.0))
            el.append(step_badge(sx + 11, 461, num, fg=fg, bg=bg, r=10))
            el.append(txt(sx + 27, 465, stitle, size=12.5, color=INK, weight="700"))
            el.append(txt(sx + 4, 492, l1, size=11.2, color=BODY))
            el.append(txt(sx + 4, 512, l2, size=11.2, color=MUTED))

        svg = figure(
            558,
            "帕斯卡定理的初等证明与中心投影推广",
            "左图在圆上取隔开的三条边AB、CD、EF构造基准三角形UVW，对截线DE、BC、FA使用三次梅涅劳斯定理并由圆幂定理消去十二段割线长，证得P、Q、R共线；右图由光源S作三维中心投影，把圆与帕斯卡线映射到任意倾斜平面上的圆锥曲线与直线P'Q'R'。",
            el,
        )
        write_svg("pascal", "pascal-menelaus-proof.svg", svg)
        return svg


    # ---------------------------------------------------------------------------
    # 2. Pappus's Hexagon Theorem (Degenerate Two-Line Conic) SVG
    # ---------------------------------------------------------------------------
    def build_pappus_two_lines():
        # Line l1: top gently tilted line; Line l2: bottom gently tilted line
        O_meet = (-40.0, 224.0)
        ang1 = math.radians(-10.5)
        ang2 = math.radians(11.5)

        def pt_on(ang, t):
            return (O_meet[0] + t * math.cos(ang), O_meet[1] + t * math.sin(ang))

        A = pt_on(ang1, 125.0)
        B = pt_on(ang1, 255.0)
        C = pt_on(ang1, 405.0)

        a = pt_on(ang2, 115.0)
        b = pt_on(ang2, 268.0)
        c = pt_on(ang2, 422.0)

        assert abs(collinear_det(A, B, C)) < 1e-9
        assert abs(collinear_det(a, b, c)) < 1e-9

        # Hexagon A -> b -> C -> a -> B -> c -> A
        P = line_inter(A, b, a, B)
        Q = line_inter(B, c, b, C)
        R = line_inter(C, a, c, A)
        assert abs(collinear_det(P, Q, R)) < 1e-8, f"Pappus collinearity failed: {collinear_det(P, Q, R)}"

        el = []
        el += header(
            "帕普斯六边形定理（公元 4 世纪）：当圆锥曲线退化成两条直线",
            "上直线取 A, B, C，下直线取 a, b, c；三组十字交叉连线的交点 P, Q, R 照样排成一条直线！",
        )

        # Left Card: Main Pappus configuration
        el.append(card(20, 66, 444, 372))
        el.append(txt(36, 90, "两条直线 ℓ₁ ∪ ℓ₂ 上的交替六边形 A–b–C–a–B–c", size=PANEL_TITLE, color=INK, weight="700"))

        l1_s, l1_e = pt_on(ang1, 78.0), pt_on(ang1, 458.0)
        l2_s, l2_e = pt_on(ang2, 74.0), pt_on(ang2, 462.0)
        el.append(seg_svg(l1_s, l1_e, color=SLATE, sw=2.4))
        el.append(seg_svg(l2_s, l2_e, color=SLATE, sw=2.4))
        el.append(txt(l1_e[0] + 6, l1_e[1] + 4, "ℓ₁", size=12.5, color=SLATE, weight="700"))
        el.append(txt(l2_e[0] + 6, l2_e[1] + 5, "ℓ₂", size=12.5, color=SLATE, weight="700"))

        # Cross-join pairs
        # Pair 1 (ORANGE): Ab and aB -> P
        el.append(seg_svg(A, b, color=ORANGE, sw=2.1))
        el.append(seg_svg(a, B, color=ORANGE, sw=2.1))
        # Pair 2 (BLUE): Bc and bC -> Q
        el.append(seg_svg(B, c, color=BLUE, sw=2.1))
        el.append(seg_svg(b, C, color=BLUE, sw=2.1))
        # Pair 3 (PURPLE): Ca and cA -> R
        el.append(seg_svg(C, a, color=PURPLE, sw=1.9, dash="6 3"))
        el.append(seg_svg(c, A, color=PURPLE, sw=1.9, dash="6 3"))

        # Red Pappus line through P, Q, R
        p_s, p_e = span_line([P, Q, R], pad=44.0, box=(34.0, 110.0, 448.0, 390.0))
        el.append(seg_svg(p_s, p_e, color=RED, sw=2.8))
        el.append(txt(p_e[0] - 2, p_e[1] + 22, "帕普斯线", size=12, color=RED, anchor="end", weight="700", halo=True))

        # Points on l1 and l2
        for pt, nm in ((A, "A"), (B, "B"), (C, "C")):
            el.append(dot_svg(pt, r=4.6, fill=CARD_BG, stroke=INK, sw=2.0))
            el.append(txt(pt[0], pt[1] - 11, nm, size=12.5, color=INK, anchor="middle", weight="700", halo=True))
        for pt, nm in ((a, "a"), (b, "b"), (c, "c")):
            el.append(dot_svg(pt, r=4.6, fill=CARD_BG, stroke=INK, sw=2.0))
            el.append(txt(pt[0], pt[1] + 20, nm, size=12.5, color=INK, anchor="middle", weight="700", halo=True))

        # Intersection points P, Q, R
        el.append(dot_svg(P, r=5.2, fill=ORANGE, stroke=CARD_BG, sw=1.8))
        el.append(dot_svg(Q, r=5.2, fill=BLUE, stroke=CARD_BG, sw=1.8))
        el.append(dot_svg(R, r=5.2, fill=PURPLE, stroke=CARD_BG, sw=1.8))
        el.append(txt(P[0] - 11, P[1] - 8, "P", size=12.5, color=ORANGE, anchor="end", weight="700", halo=True))
        el.append(txt(Q[0] + 12, Q[1] - 8, "Q", size=12.5, color=BLUE, anchor="start", weight="700", halo=True))
        el.append(txt(R[0] + 2, R[1] - 12, "R", size=12.5, color=PURPLE, anchor="middle", weight="700", halo=True))

        # Bottom caption strip inside Left Card
        el.append(card(34, 392, 416, 34, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        el.append(
            txt(
                242,
                413,
                "注意禁令：连线必须在 ℓ₁ 与 ℓ₂ 之间来回跳，不能沿同一直线连 AB 或 ab",
                size=11.3,
                color=BODY,
                anchor="middle",
                weight="600",
            )
        )

        # Right Top Card: Why two lines = degenerate conic?
        el.append(card(478, 66, 262, 178))
        el.append(txt(494, 89, "为什么两条直线算圆锥曲线？", size=PANEL_TITLE, color=INK, weight="700"))

        # Mini double-cone cut right through apex
        cx_c, cy_c = 542.0, 156.0
        el.append(poly_svg([(cx_c - 34, cy_c - 44), (cx_c + 34, cy_c - 44), (cx_c, cy_c)], fill=BLUE_SOFT, stroke=SLATE, sw=1.2, fill_opacity=0.55))
        el.append(poly_svg([(cx_c - 34, cy_c + 44), (cx_c + 34, cy_c + 44), (cx_c, cy_c)], fill=BLUE_SOFT, stroke=SLATE, sw=1.2, fill_opacity=0.55))
        el.append(f'<ellipse cx="{cx_c:.1f}" cy="{cy_c - 44:.1f}" rx="34" ry="7.5" fill="{CARD_BG}" stroke="{SLATE}" stroke-width="1.2"/>')
        el.append(f'<ellipse cx="{cx_c:.1f}" cy="{cy_c + 44:.1f}" rx="34" ry="7.5" fill="none" stroke="{SLATE}" stroke-width="1.2"/>')
        # Cutting plane passing through apex -> two red/purple generator lines!
        el.append(seg_svg((cx_c - 26, cy_c - 44), (cx_c + 26, cy_c + 44), color=RED, sw=2.3))
        el.append(seg_svg((cx_c + 26, cy_c - 44), (cx_c - 26, cy_c + 44), color=RED, sw=2.3))
        el.append(dot_svg((cx_c, cy_c), r=3.6, fill=RED, stroke=CARD_BG, sw=1.2))

        el.append(txt(592, 118, "截面恰好穿过锥顶：", size=11.5, color=INK, weight="700"))
        el.append(txt(592, 138, "双曲线 xy = ε 在 ε → 0", size=11.3, color=BODY))
        el.append(txt(592, 157, "时退化为 xy = 0，即两", size=11.3, color=BODY))
        el.append(txt(592, 176, "条相交直线 L₁·L₂ = 0！", size=11.3, color=RED, weight="600"))
        el.append(txt(494, 226, "二次方程总家族天然包含“直线对”", size=11.2, color=MUTED))

        # Right Bottom Card: Cross-join recipe & Hilbert's insight
        el.append(card(478, 256, 262, 182))
        el.append(txt(494, 279, "三组十字交叉对边账单", size=PANEL_TITLE, color=INK, weight="700"))

        rows = [
            (304, ORANGE, ORANGE_SOFT, "① 橙组", "Ab ∩ aB = P"),
            (334, BLUE, BLUE_SOFT, "② 蓝组", "Bc ∩ bC = Q"),
            (364, PURPLE, PURPLE_SOFT, "③ 紫组", "Ca ∩ cA = R"),
        ]
        for ry, fg, bg, tag, expr in rows:
            el.append(pill(494, ry - 15, tag, fg=fg, bg=bg, w=68, h=21, size=11.3))
            el.append(txt(574, ry, expr, size=12, color=INK, weight="700", cls="mono"))

        el.append(seg_svg((494, 384), (724, 384), color=BORDER, sw=1.0))
        el.append(txt(494, 404, "希尔伯特《几何基础》揭示：", size=11.3, color=INK, weight="700"))
        el.append(txt(494, 423, "帕普斯定理 ⇔ 坐标域乘法交换律 ab=ba", size=11.1, color=PURPLE, weight="600"))

        svg = figure(
            452,
            "帕普斯六边形定理：退化圆锥曲线（两条直线）上的共线定理",
            "左图在直线l1上取A、B、C，在直线l2上取a、b、c，按A-b-C-a-B-c-A连接后，三组十字交叉对边Ab与aB、Bc与bC、Ca与cA分别交于P、Q、R，三点严格共线于红色帕普斯线；右图展示平面切过双圆锥顶点得到两条相交直线的退化二次曲线机制。",
            el,
        )
        write_svg("pascal", "pappus-two-lines.svg", svg)
        return svg


    # ---------------------------------------------------------------------------
    # 3. Brianchon's Dual Theorem & Straightedge-Only Conic Construction SVG
    # ---------------------------------------------------------------------------
    def build_brianchon_dual():
        el = []
        el += header(
            "射影对偶与无圆规作图：布利安桑外切六边形 + 单靠直尺画圆锥曲线",
            "左：点线互换后“三点共线”对偶成“三线共点”；右：已知 5 个点，不用圆规也不用方程，纯靠直尺描出整条椭圆！",
        )

        # ---- Left Panel: Brianchon's Circumscribed Hexagon ----
        el.append(card(20, 66, 354, 388))
        el.append(txt(36, 89, "布利安桑定理（1806）：外切六边形", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(264, 73, "三对角线共点", fg=ORANGE, bg=ORANGE_SOFT, w=96, h=22, size=11.3))

        # Ellipse centered at (196, 240) with rx=104, ry=74
        cx_b, cy_b = 196.0, 242.0
        rx_b, ry_b = 102.0, 72.0

        # Deliberately asymmetric tangent parameters so Brianchon point B != ellipse center O!
        t_degs = [14.0, 66.0, 148.0, 212.0, 256.0, 326.0]
        ts = [math.radians(d) for d in t_degs]

        def tan_pt(t):
            return (cx_b + rx_b * math.cos(t), cy_b - ry_b * math.sin(t))

        def tan_inter(t1, t2):
            # In local coords (x/rx) cos t + (y/ry) sin t = 1, with y_svg = cy - y
            a1, b1 = math.cos(t1) / rx_b, math.sin(t1) / ry_b
            a2, b2 = math.cos(t2) / rx_b, math.sin(t2) / ry_b
            det = a1 * b2 - a2 * b1
            lx = (b2 - b1) / det
            ly = (a1 - a2) / det
            return (cx_b + lx, cy_b - ly)

        T_pts = [tan_pt(t) for t in ts]
        V_pts = [tan_inter(ts[i], ts[(i + 1) % 6]) for i in range(6)]
        # Verify tangency: each T_pts[i] lies on segment V_{i-1} -- V_i!
        for i in range(6):
            assert abs(collinear_det(V_pts[(i - 1) % 6], T_pts[i], V_pts[i])) < 1e-6

        # Three opposite-vertex diagonals: V1-V4, V2-V5, V3-V6
        B12 = line_inter(V_pts[0], V_pts[3], V_pts[1], V_pts[4])
        B23 = line_inter(V_pts[1], V_pts[4], V_pts[2], V_pts[5])
        B31 = line_inter(V_pts[2], V_pts[5], V_pts[0], V_pts[3])
        assert math.dist(B12, B23) < 1e-8 and math.dist(B23, B31) < 1e-8
        B_pt = B12
        assert math.dist(B_pt, (cx_b, cy_b)) > 8.0  # Distinct from center O!

        # Draw ellipse
        el.append(
            f'<ellipse cx="{cx_b:.1f}" cy="{cy_b:.1f}" rx="{rx_b:.1f}" ry="{ry_b:.1f}" '
            f'fill="{BLUE_SOFT}" fill-opacity="0.38" stroke="{BLUE}" stroke-width="2.1"/>'
        )

        # Circumscribed hexagon edges (tangent segments extended slightly)
        el.append(poly_svg(V_pts, fill="none", stroke=SLATE, sw=2.1))
        for tp in T_pts:
            el.append(dot_svg(tp, r=3.1, fill=BLUE, stroke=CARD_BG, sw=1.2))

        # Three main diagonals meeting at Brianchon point B
        diag_cols = [(0, 3, ORANGE), (1, 4, GREEN), (2, 5, PURPLE)]
        for i, j, col in diag_cols:
            el.append(seg_svg(V_pts[i], V_pts[j], color=col, sw=2.2))

        # Mark ellipse center O faintly vs Brianchon point B prominently
        el.append(dot_svg((cx_b, cy_b), r=2.8, fill=MUTED, stroke=CARD_BG, sw=1.0))
        el.append(txt(cx_b - 7, cy_b + 15, "中心O", size=11, color=MUTED, anchor="end", halo=True))

        el.append(dot_svg(B_pt, r=5.6, fill=RED, stroke=CARD_BG, sw=1.8))
        el.append(txt(B_pt[0] + 10, B_pt[1] + 5, "B（布利安桑点）", size=12, color=RED, weight="700", halo=True))

        v_offsets = [
            (8, -6, "start"),
            (-6, -8, "end"),
            (-8, 4, "end"),
            (-6, 15, "end"),
            (6, 16, "start"),
            (8, 5, "start"),
        ]
        for idx, (vp, (dx, dy, anc)) in enumerate(zip(V_pts, v_offsets), 1):
            el.append(dot_svg(vp, r=4.2, fill=CARD_BG, stroke=INK, sw=1.8))
            el.append(txt(vp[0] + dx, vp[1] + dy, f"V{idx}", size=11.8, color=INK, anchor=anc, weight="700", halo=True))

        # Duality footer inside Left Panel
        el.append(card(34, 376, 326, 64, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        el.append(txt(46, 396, "射影对偶字典：曲线上的点 ↔ 曲线的切线", size=11.4, color=INK, weight="700"))
        el.append(txt(46, 415, "内接六边形对边交点共线 ↔ 外切六边形对顶点连线共点", size=11.1, color=BODY))
        el.append(txt(46, 432, "注意：共点 B 一般不与椭圆中心 O 重合！", size=11.0, color=RED, weight="600"))

        # ---- Right Panel: Pure Straightedge 5-Points -> 6th-Point Construction ----
        el.append(card(386, 66, 354, 388))
        el.append(txt(402, 89, "五点定圆锥曲线：只用直尺找第 6 点", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(640, 73, "零圆规作图", fg=GREEN, bg=GREEN_SOFT, w=86, h=22, size=11.3))

        cx_r, cy_r = 564.0, 228.0
        rx_r, ry_r = 110.0, 76.0
        base_degs = [28.5, 90.9, 136.1, 170.1, 201.9, 321.0]
        perm = (0, 2, 5, 1, 4, 3)

        def ell_r(deg):
            th = math.radians(deg)
            return (cx_r + rx_r * math.cos(th), cy_r - ry_r * math.sin(th))

        # Known 5 points A1..A5; A6 will be constructed purely via line intersections!
        A1, A2, A3, A4, A5, A6_true = [ell_r(base_degs[i]) for i in perm]

        # Straightedge construction along chosen ray r passing through A1 (in direction of A6_true):
        # Step 1: P = A1A2 cap A4A5 (both lines connect known points!)
        P_c = line_inter(A1, A2, A4, A5)
        # Step 2: R = A3A4 cap r (since ray r IS the future side A6A1!)
        R_c = line_inter(A3, A4, A1, A6_true)
        # Step 3: Draw Pascal line p = PR, intersect with known line A2A3 to get Q!
        Q_c = line_inter(P_c, R_c, A2, A3)
        # Step 4: Draw QA5 to meet ray r at the exact 6th conic point A6!
        A6_constructed = line_inter(Q_c, A5, A1, A6_true)

        assert math.dist(A6_constructed, A6_true) < 1e-8
        norm_eq = ((A6_constructed[0] - cx_r) / rx_r) ** 2 + ((A6_constructed[1] - cy_r) / ry_r) ** 2
        assert abs(norm_eq - 1.0) < 1e-9

        # Also verify degenerate limit A6 -> A1 constructs exact tangent at A1!
        t1_rad = math.radians(base_degs[perm[0]])
        # Tangent vector at A1 in SVG coords: (-rx sin t, -ry cos t)
        A1_tan_dir = (A1[0] - rx_r * math.sin(t1_rad), A1[1] - ry_r * math.cos(t1_rad))
        Q_tan = line_inter(A2, A3, A5, A1)
        R_tan = line_inter(P_c, Q_tan, A3, A4)
        assert abs(collinear_det(A1, A1_tan_dir, R_tan)) < 1e-6

        rbox = (396.0, 104.0, 730.0, 344.0)
        # Faint target ellipse (dashed) showing the curve traced out as ray r sweeps!
        el.append(
            f'<ellipse cx="{cx_r:.1f}" cy="{cy_r:.1f}" rx="{rx_r:.1f}" ry="{ry_r:.1f}" '
            f'fill="none" stroke="{HAIRLINE}" stroke-width="1.6" stroke-dasharray="5 4"/>'
        )

        # Known segments: A1A2, A2A3, A3A4, A4A5
        for u, v in ((A1, A2), (A2, A3), (A3, A4), (A4, A5)):
            el.append(seg_svg(u, v, color=SLATE, sw=1.7))
        # Extensions to P, Q, R
        el.append(seg_svg(A4, P_c, color=ORANGE, sw=1.4, dash="4 3"))
        el.append(seg_svg(A1, P_c, color=ORANGE, sw=1.4, dash="4 3"))
        el.append(seg_svg(A3, R_c, color=PURPLE, sw=1.4, dash="4 3"))
        el.append(seg_svg(A2, Q_c, color=BLUE, sw=1.4, dash="4 3"))

        # Chosen ray r through A1 (green)
        r_s, r_e = span_line([A1, R_c, A6_constructed], pad=16.0, box=rbox)
        el.append(seg_svg(r_s, r_e, color=GREEN, sw=2.1))

        # Pascal line PRQ (red)
        p_s, p_e = span_line([P_c, Q_c, R_c], pad=16.0, box=rbox)
        el.append(seg_svg(p_s, p_e, color=RED, sw=2.3))

        # Final closing line QA5 -> A6 (blue-green highlight)
        q_s, q_e = span_line([Q_c, A5, A6_constructed], pad=10.0, box=rbox)
        el.append(seg_svg(q_s, q_e, color=BLUE, sw=2.0, dash="5 3"))

        # Draw 5 given points A1..A5 (blue solid) and newly found A6 (green star/bullseye)
        a_lbls = [
            (A1, "A₁", 9, -6, "start"),
            (A2, "A₂", -9, -5, "end"),
            (A3, "A₃", 9, 12, "start"),
            (A4, "A₄", 0, -10, "middle"),
            (A5, "A₅", -9, 12, "end"),
        ]
        for pt, nm, dx, dy, anc in a_lbls:
            el.append(dot_svg(pt, r=4.3, fill=BLUE, stroke=CARD_BG, sw=1.6))
            el.append(txt(pt[0] + dx, pt[1] + dy, nm, size=11.8, color=BLUE, anchor=anc, weight="700", halo=True))

        # Constructed intersections P, R, Q
        el.append(dot_svg(P_c, r=4.2, fill=ORANGE, stroke=CARD_BG, sw=1.5))
        el.append(txt(P_c[0] + 8, P_c[1] - 5, "P", size=11.8, color=ORANGE, weight="700", halo=True))
        el.append(dot_svg(R_c, r=4.2, fill=PURPLE, stroke=CARD_BG, sw=1.5))
        el.append(txt(R_c[0] + 8, R_c[1] + 4, "R", size=11.8, color=PURPLE, weight="700", halo=True))
        el.append(dot_svg(Q_c, r=4.2, fill=RED, stroke=CARD_BG, sw=1.5))
        el.append(txt(Q_c[0] - 8, Q_c[1] - 6, "Q", size=11.8, color=RED, anchor="end", weight="700", halo=True))

        # Target 6th point A6!
        el.append(f'<circle cx="{A6_constructed[0]:.2f}" cy="{A6_constructed[1]:.2f}" r="7.5" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
        el.append(dot_svg(A6_constructed, r=4.4, fill=GREEN, stroke=CARD_BG, sw=1.5))
        el.append(txt(A6_constructed[0] - 10, A6_constructed[1] - 8, "新点 A₆！", size=12, color=GREEN, anchor="end", weight="700", halo=True))

        # Step-by-step straightedge recipe box
        el.append(card(400, 344, 326, 96, rx=7, fill=GREEN_SOFT, stroke=GREEN, sw=1))
        el.append(txt(412, 363, "纯直尺四步口诀（已知 A₁…A₅，过 A₁ 任画绿线 r）：", size=11.4, color=INK, weight="700"))
        el.append(txt(412, 382, "1. 求 P = A₁A₂ ∩ A₄A₅，求 R = A₃A₄ ∩ r", size=11.2, color=BODY))
        el.append(txt(412, 400, "2. 连红线 PR（帕斯卡线），交 A₂A₃ 得 Q", size=11.2, color=BODY))
        el.append(txt(412, 418, "3. 连 QA₅ 交绿线 r ⇒ 精准命中曲线上第 6 点 A₆！", size=11.2, color=GREEN, weight="700"))
        el.append(txt(412, 434, "（若令 A₆→A₁ 合并，同法直接画出 A₁ 处的精确切线！）", size=11.0, color=MUTED))

        svg = figure(
            468,
            "布利安桑对偶定理与五点纯直尺作圆锥曲线",
            "左图展示椭圆外切六边形V1V2V3V4V5V6的三条主对角线V1V4、V2V5、V3V6精确共点于布利安桑点B（不同于椭圆中心O）；右图展示已知圆锥曲线上五点A1至A5，过A1任作直线r，仅用直尺依次求P、R、帕斯卡线PR、交点Q及QA5与r的交点，即可精确作出曲线上第六点A6。",
            el,
        )
        write_svg("pascal", "brianchon-dual.svg", svg)
        return svg


    # ---------------------------------------------------------------------------
    # 4. Square Incommensurability: Geometric Folding vs Parity Contradiction SVG
    # ---------------------------------------------------------------------------
    def build_square_incommensurable():
        # Exact geometric folding coordinates on isosceles right triangle ABC
        # Right angle at B = (0, 0), A = (0, 1), C = (1, 0) in math coords
        # Hypotenuse AC has length sqrt(2). Fold AB onto AC along angle bisector AD:
        # E on AC at distance 1 from A => E = (1/sqrt(2), 1 - 1/sqrt(2))
        # D on BC => BD = tan(22.5 deg) = sqrt(2) - 1, so D = (sqrt(2) - 1, 0)
        s0 = 1.0
        d0 = math.sqrt(2.0)
        s1 = d0 - s0  # sqrt(2) - 1
        d1 = 2 * s0 - d0  # 2 - sqrt(2)
        s2 = d1 - s1  # 3 - 2*sqrt(2)
        d2 = 2 * s1 - d1  # 3*sqrt(2) - 4
        assert abs(d1 / s1 - d0 / s0) < 1e-12
        assert abs(d2 / s2 - d0 / s0) < 1e-12

        # Euclidean anthyphairesis quotients of (d0, s0) -> [1; 2, 2, 2, 2]
        x_val, y_val = d0, s0
        quotients = []
        for _ in range(5):
            q_int = int(math.floor(x_val / y_val + 1e-12))
            quotients.append(q_int)
            x_val, y_val = y_val, x_val - q_int * y_val
        assert quotients == [1, 2, 2, 2, 2]

        # Map math (0..1, 0..1) to Left Panel SVG
        ox, oy = 56.0, 326.0
        L = 216.0

        def m_tri(mx, my):
            return (ox + mx * L, oy - my * L)

        A_pt = m_tri(0.0, 1.0)
        B_pt = m_tri(0.0, 0.0)
        C_pt = m_tri(1.0, 0.0)
        D_pt = m_tri(s1, 0.0)
        E_pt = m_tri(1.0 / d0, 1.0 - 1.0 / d0)
        # Check perpendicularity DE perp AC and lengths!
        assert abs(math.dist(A_pt, E_pt) - L) < 1e-9
        assert abs(math.dist(B_pt, D_pt) - math.dist(D_pt, E_pt)) < 1e-9
        assert abs(math.dist(D_pt, E_pt) - math.dist(E_pt, C_pt)) < 1e-9

        # Second fold inside Delta DEC (right angle at E, legs ED and EC of length s1, hyp DC of length d1):
        # Fold ED onto DC from vertex D: E2 on DC at distance s1 from D => C - E2 has length d1 - s1 = s2!
        # Wait: E2 on BC: D is at x = s1, so E2 is at x = s1 + s1 = 2*s1 = 2*sqrt(2) - 2!
        # And D2 on EC at distance s2 from E2: since angle C = 45 deg, D2 E2 perp BC!
        E2_pt = m_tri(s1 + s1, 0.0)
        D2_math_x = 1.0 - s2
        D2_math_y = s2
        D2_pt = m_tri(D2_math_x, D2_math_y)
        assert abs(math.dist(E2_pt, C_pt) / L - s2) < 1e-9
        assert abs(math.dist(D2_pt, E2_pt) / L - s2) < 1e-9
        assert abs(math.dist(D2_pt, C_pt) / L - d2) < 1e-9

        el = []
        el += header(
            "为什么正方形的对角线与边长“不可公度”？几何无限折叠 vs 奇偶反证法",
            "不是尺子刻度不够细，而是根本不存在能把边长 s 与对角线 d 同时量成整数份的共同长度单位 u",
        )

        # ---- Left Card: Geometric Folding (Anthyphairesis) ----
        el.append(card(20, 66, 376, 396))
        el.append(txt(36, 89, "方法一：把边折向对角线（几何辗转相减）", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(296, 73, "永远折不完", fg=BLUE, bg=BLUE_SOFT, w=86, h=22, size=11.3))

        # Ghost upper-right half of the square so reader sees ABC is half of the unit square!
        TopR_pt = m_tri(1.0, 1.0)
        el.append(poly_svg([A_pt, TopR_pt, C_pt], fill="none", stroke=HAIRLINE, sw=1.2, dash="5 4", closed=False))
        el.append(txt(TopR_pt[0] - 6, TopR_pt[1] + 16, "正方形另一半", size=11, color=MUTED, anchor="end"))

        # Main triangle ABC
        el.append(poly_svg([A_pt, B_pt, C_pt], fill=BLUE_SOFT, stroke=BLUE, sw=2.1, fill_opacity=0.35))
        # First smaller isosceles right triangle DEC (orange highlight)
        el.append(poly_svg([D_pt, E_pt, C_pt], fill=ORANGE_SOFT, stroke=ORANGE, sw=2.1, fill_opacity=0.72))
        # Second even smaller isosceles right triangle D2 E2 C (purple highlight)
        el.append(poly_svg([D_pt, D2_pt, C_pt], fill="none", stroke="none", sw=0))
        el.append(poly_svg([D2_pt, E2_pt, C_pt], fill=PURPLE_SOFT, stroke=PURPLE, sw=1.8, fill_opacity=0.85))

        # Right-angle markers at B and E
        el.append(poly_svg([(ox, oy - 12), (ox + 12, oy - 12), (ox + 12, oy)], fill="none", stroke=BLUE, sw=1.3, closed=False))
        # Right angle at E (between EA and ED)
        ux_ea = (A_pt[0] - E_pt[0]) / math.dist(A_pt, E_pt)
        uy_ea = (A_pt[1] - E_pt[1]) / math.dist(A_pt, E_pt)
        ux_ed = (D_pt[0] - E_pt[0]) / math.dist(D_pt, E_pt)
        uy_ed = (D_pt[1] - E_pt[1]) / math.dist(D_pt, E_pt)
        ra = 9.5
        el.append(
            poly_svg(
                [
                    (E_pt[0] + ra * ux_ea, E_pt[1] + ra * uy_ea),
                    (E_pt[0] + ra * (ux_ea + ux_ed), E_pt[1] + ra * (uy_ea + uy_ed)),
                    (E_pt[0] + ra * ux_ed, E_pt[1] + ra * uy_ed),
                ],
                fill="none",
                stroke=ORANGE,
                sw=1.3,
                closed=False,
            )
        )

        # Fold line AD and circular swing arc from B to E centered at A (radius = L)!
        el.append(seg_svg(A_pt, D_pt, color=BLUE, sw=1.6, dash="5 3"))
        el.append(
            f'<path d="M {B_pt[0]:.2f},{B_pt[1]:.2f} A {L:.2f},{L:.2f} 0 0 0 {E_pt[0]:.2f},{E_pt[1]:.2f}" '
            f'fill="none" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#arr-green)"/>'
        )

        # Vertices & clear labels
        for pt in (A_pt, B_pt, C_pt):
            el.append(dot_svg(pt, r=4.0, fill=CARD_BG, stroke=BLUE, sw=1.8))
        el.append(dot_svg(D_pt, r=4.0, fill=ORANGE, stroke=CARD_BG, sw=1.5))
        el.append(dot_svg(E_pt, r=4.0, fill=ORANGE, stroke=CARD_BG, sw=1.5))
        el.append(dot_svg(D2_pt, r=3.2, fill=PURPLE, stroke=CARD_BG, sw=1.2))
        el.append(dot_svg(E2_pt, r=3.2, fill=PURPLE, stroke=CARD_BG, sw=1.2))

        el.append(txt(A_pt[0] - 10, A_pt[1] + 5, "A", size=12.5, color=INK, anchor="end", weight="700"))
        el.append(txt(B_pt[0] - 10, B_pt[1] + 5, "B", size=12.5, color=INK, anchor="end", weight="700"))
        el.append(txt(C_pt[0] + 9, C_pt[1] + 5, "C", size=12.5, color=INK, weight="700"))
        el.append(txt(D_pt[0] - 4, D_pt[1] + 18, "D", size=12, color=ORANGE, anchor="middle", weight="700"))
        el.append(txt(E_pt[0] + 10, E_pt[1] - 5, "E", size=12, color=ORANGE, weight="700", halo=True))
        el.append(txt(E2_pt[0] + 4, E2_pt[1] + 18, "E₂", size=11.5, color=PURPLE, anchor="middle", weight="700"))

        # Segment length annotations
        el.append(txt(ox - 12, (A_pt[1] + B_pt[1]) / 2 + 4, "s", size=12.5, color=BLUE, anchor="end", weight="700"))
        el.append(txt(ox + 72, oy - 134, "AE = s", size=11.8, color=GREEN, weight="700", halo=True))
        el.append(txt(E_pt[0] + 44, E_pt[1] + 34, "余边 EC = d − s", size=11.5, color=ORANGE, weight="700", halo=True))
        el.append(txt((D_pt[0] + C_pt[0]) / 2 - 12, oy + 34, "新斜边 DC = 2s − d", size=11.5, color=ORANGE, anchor="middle", weight="700"))

        # Bottom recurrence summary inside Left Card
        el.append(card(34, 370, 348, 80, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        el.append(txt(46, 389, "折叠递推：小等腰直角 ΔDEC 满足 s₁ = d−s，d₁ = 2s−d", size=11.3, color=INK, weight="700"))
        el.append(txt(46, 408, "若有共同单位 u 使 s,d 为整数份，余量将产出无穷递降正整数！", size=11.1, color=BODY))
        el.append(txt(46, 427, "辗转相减商序列：[1; 2, 2, 2, …] ⇒ √2 = 1 + 1/(2 + 1/(2 + …))", size=11.1, color=PURPLE, weight="600"))

        # ---- Right Card: Parity Contradiction p^2 = 2q^2 ----
        el.append(card(408, 66, 332, 396))
        el.append(txt(424, 89, "方法二：奇偶性反证法（p² = 2q²）", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(642, 73, "互质却全偶", fg=ORANGE, bg=ORANGE_SOFT, w=86, h=22, size=11.3))

        # Visual area equation: p x p square (divided into 4 k x k quadrants) = two q x q squares
        # Left square: p = 2k, size 76x76 at (432, 114)
        el.append(card(432, 114, 76, 76, rx=3, fill=BLUE_SOFT, stroke=BLUE, sw=2.0))
        el.append(seg_svg((470, 114), (470, 190), color=BLUE, sw=1.3, dash="4 3"))
        el.append(seg_svg((432, 152), (508, 152), color=BLUE, sw=1.3, dash="4 3"))
        el.append(txt(451, 137, "k²", size=11.5, color=BLUE, anchor="middle", weight="700"))
        el.append(txt(489, 137, "k²", size=11.5, color=BLUE, anchor="middle", weight="700"))
        el.append(txt(451, 175, "k²", size=11.5, color=BLUE, anchor="middle", weight="700"))
        el.append(txt(489, 175, "k²", size=11.5, color=BLUE, anchor="middle", weight="700"))
        el.append(txt(470, 207, "p² = (2k)² = 4k²", size=11.5, color=BLUE, anchor="middle", weight="700"))

        el.append(txt(530, 158, "=", size=15, color=INK, anchor="middle", weight="700"))

        # Two q x q squares of side 54 (~76/sqrt(2)) at (554, 125) and (622, 125)
        el.append(card(554, 125, 54, 54, rx=3, fill=ORANGE_SOFT, stroke=ORANGE, sw=2.0))
        el.append(txt(581, 156, "q²", size=12, color=ORANGE, anchor="middle", weight="700"))
        el.append(txt(619, 157, "+", size=13, color=INK, anchor="middle", weight="700"))
        el.append(card(630, 125, 54, 54, rx=3, fill=ORANGE_SOFT, stroke=ORANGE, sw=2.0))
        el.append(txt(657, 156, "q²", size=12, color=ORANGE, anchor="middle", weight="700"))
        el.append(txt(619, 207, "2q²（两块 q×q）", size=11.5, color=ORANGE, anchor="middle", weight="700"))

        # Four logical domino cards stacked cleanly without overlap
        chain = [
            (224, "1", BLUE, BLUE_SOFT, "先约到最简分数：设 d/s = p/q，gcd(p, q) = 1"),
            (272, "2", ORANGE, ORANGE_SOFT, "平方得 p² = 2q² ⇒ p² 是偶数 ⇒ p = 2k 必为偶数"),
            (320, "3", GREEN, GREEN_SOFT, "代入 4k² = 2q² ⇒ q² = 2k² ⇒ q = 2m 也必为偶数！"),
            (368, "4", PURPLE, PURPLE_SOFT, "矛盾爆破：p, q 都能被 2 整除，与“互质无公因子”冲突！"),
        ]
        for cy_box, bnum, fg, bg, line_txt in chain:
            el.append(card(424, cy_box, 300, 38, rx=7, fill=CARD_BG, stroke=BORDER))
            el.append(step_badge(442, cy_box + 19, bnum, fg=fg, bg=bg, r=9.5))
            el.append(txt(458, cy_box + 23, line_txt, size=11.2, color=INK, weight="600"))

        el.append(card(424, 416, 300, 34, rx=7, fill=RED_SOFT, stroke=RED, sw=1))
        el.append(txt(574, 437, "结论：不存在任何有理数 p/q 满足 (p/q)² = 2", size=11.5, color=RED, anchor="middle", weight="700"))

        svg = figure(
            476,
            "正方形对角线与边长不可公度的两种严格证明",
            "左图把边长AB=s折到对角线AC=d上得到AE=s与余段EC=d-s，构造出更小的等腰直角三角形DEC（直角边d-s、斜边2s-d），无限自相似折叠对应连分数[1;2,2,2,...]；右图用面积4k²=2q²展示p²=2q²导致p与q同为偶数，与最简分数互质假设矛盾。",
            el,
        )
        write_svg("eudoxus", "square-incommensurable.svg", svg)
        return svg


    # ---------------------------------------------------------------------------
    # 5. Eudoxus Rational Sieve (Definition V.5 & Nested Pell Intervals) SVG
    # ---------------------------------------------------------------------------
    def build_eudoxus_rational_sieve():
        # Probe fractions r = p/q from continued fraction convergents of sqrt(2):
        # (p, q) in [(1, 1), (3, 2), (7, 5), (17, 12), (41, 29)]
        # In Eudoxus's test m*A ? n*B: to compare A/B against p/q, take m = q, n = p!
        # Because q*A ? p*B <=> A/B ? p/q <=> 2*q^2 ? p^2!
        probes = [
            (1, 1, "[1/1, +∞)"),
            (3, 2, "[1/1, 3/2]"),
            (7, 5, "[7/5, 3/2]"),
            (17, 12, "[7/5, 17/12]"),
            (41, 29, "[41/29, 17/12]"),
        ]
        rt2 = math.sqrt(2.0)
        for p, q, _ in probes:
            m, n = q, p
            lhs_sq = 2 * m * m
            rhs_sq = n * n
            assert abs(lhs_sq - rhs_sq) == 1  # Exact Pell convergent!
            assert (lhs_sq > rhs_sq) == (rt2 > Fraction(p, q))

        el = []
        el += header(
            "欧多克斯“有理数筛子”（《几何原本》定义 V.5）：整数倍同步拷问",
            "不用写出 √2，只拿正整数倍 mA 与 nB、mC 与 nD 逐轮比大小；所有有理数筛孔回答一致 ⇔ A:B = C:D",
        )

        # ---- Top Card: Step-by-step Comparison Table ----
        el.append(card(20, 66, 720, 232))
        el.append(txt(36, 90, "两组正方形同步过筛：小正方形 (A=d₁, B=s₁) vs 大正方形 (C=d₂, D=s₂)", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(572, 73, "mA ≷ nB ⇔ mC ≷ nD", fg=BLUE, bg=BLUE_SOFT, w=154, h=22, size=11.3))

        # Table header row
        el.append(card(34, 102, 692, 28, rx=5, fill=SLATE_SOFT, stroke=BORDER))
        cols_x = [46, 152, 282, 424, 574]
        headers_t = ["有理探针 n/m", "取倍数 (m, n)", "整数平方核验 2m² vs n²", "两组比赛同步判决", "夹出的有理区间"]
        for cx_h, ht in zip(cols_x, headers_t):
            el.append(txt(cx_h, 120, ht, size=11.5, color=INK, weight="700"))

        for idx, (p, q, bracket_s) in enumerate(probes):
            m, n = q, p
            ry = 148 + idx * 29
            if idx % 2 == 1:
                el.append(f'<rect x="34" y="{ry - 17}" width="692" height="27" fill="{BG}"/>')
            lhs = 2 * m * m
            rhs = n * n
            gt = lhs > rhs
            sym = ">" if gt else "<"
            col = BLUE if gt else ORANGE
            tag = f"{p}/{q} ≈ {p / q:.4f}" if q > 1 else "1/1 = 1.0000"
            el.append(txt(cols_x[0], ry, tag, size=11.5, color=INK, weight="600", cls="mono"))
            el.append(txt(cols_x[1], ry, f"m={m}, n={n}", size=11.5, color=BODY, cls="mono"))
            el.append(txt(cols_x[2], ry, f"{lhs} {sym} {rhs}（差 {lhs - rhs:+d}）", size=11.5, color=col, weight="700", cls="mono"))
            el.append(txt(cols_x[3], ry, f"{m}A {sym} {n}B  且  {m}C {sym} {n}D", size=11.5, color=col, weight="700", cls="mono"))
            el.append(txt(cols_x[4], ry, bracket_s, size=11.5, color=GREEN if idx >= 2 else SLATE, weight="700", cls="mono"))

        # ---- Bottom Card: Nested Interval Funnel on Number Line ----
        el.append(card(20, 310, 720, 214))
        el.append(txt(36, 334, "有理区间层层收口：[1, 3/2] ⊃ [7/5, 3/2] ⊃ [7/5, 17/12] ⊃ [41/29, 17/12]", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(592, 317, "永无平局却唯一锁定", fg=GREEN, bg=GREEN_SOFT, w=134, h=22, size=11.3))

        # Left sub-axis: [0.96, 1.54] mapped to x in [52, 412]
        ax0, ax1 = 52.0, 412.0
        vmin, vmax = 0.96, 1.54

        def map_main(v):
            return ax0 + (v - vmin) / (vmax - vmin) * (ax1 - ax0)

        y_axis = 468.0
        el.append(seg_svg((ax0, y_axis), (ax1, y_axis), color=SLATE, sw=1.8))

        # Exact target vertical line at sqrt(2)
        x_rt2 = map_main(rt2)
        el.append(seg_svg((x_rt2, 354), (x_rt2, y_axis + 8), color=RED, sw=2.0, dash="4 3"))
        el.append(txt(x_rt2, 351, "A:B = √2", size=11.5, color=RED, anchor="middle", weight="700"))

        # Nested horizontal bars above the main axis
        bars = [
            (366, 1.0, 1.5, "第 1–2 筛：[1, 3/2]，宽 0.500", BLUE_SOFT, BLUE),
            (396, 1.4, 1.5, "第 3 筛：[7/5, 3/2]，宽 0.100", GREEN_SOFT, GREEN),
            (426, 1.4, 17.0 / 12.0, "第 4 筛：[7/5, 17/12]，宽 0.0167", PURPLE_SOFT, PURPLE),
        ]
        for by, lo, hi, blabel, bfill, bstroke in bars:
            xlo, xhi = map_main(lo), map_main(hi)
            assert xlo < x_rt2 < xhi
            el.append(card(round(xlo, 2), by, round(xhi - xlo, 2), 18, rx=4, fill=bfill, stroke=bstroke, sw=1.5))
            if hi - lo < 0.15:
                el.append(txt(xlo - 8, by + 13, blabel, size=11.2, color=bstroke, anchor="end", weight="600"))
            else:
                el.append(txt((xlo + xhi) / 2, by + 13, blabel, size=11.2, color=INK, anchor="middle", weight="600"))

        # Ticks on main axis: 1/1, 7/5, 3/2
        for val, lbl, col, dy in ((1.0, "1/1", BLUE, 20), (1.4, "7/5 (1.4)", BLUE, 20), (1.5, "3/2 (1.5)", ORANGE, 20)):
            xv = map_main(val)
            el.append(seg_svg((xv, y_axis - 5), (xv, y_axis + 5), color=col, sw=1.8))
            el.append(txt(xv, y_axis + dy, lbl, size=11.3, color=col, anchor="middle", weight="700"))

        el.append(txt(232, 510, "宏观数轴窗口 [0.96, 1.54]", size=11.2, color=MUTED, anchor="middle"))

        # Right subcard: Magnified zoom [1.4125, 1.4175] showing [41/29, 17/12]!
        el.append(card(436, 352, 290, 158, rx=8, fill=BG, stroke=BORDER, dash="4 3"))
        el.append(txt(581, 372, "局部放大镜 [1.4125, 1.4175]", size=12, color=INK, anchor="middle", weight="700"))

        zx0, zx1 = 456.0, 706.0
        zmin, zmax = 1.4125, 1.4175

        def map_zoom(v):
            return zx0 + (v - zmin) / (zmax - zmin) * (zx1 - zx0)

        zy = 446.0
        x_41_29 = map_zoom(41.0 / 29.0)
        x_17_12 = map_zoom(17.0 / 12.0)
        z_rt2 = map_zoom(rt2)
        assert zx0 < x_41_29 < z_rt2 < x_17_12 < zx1

        el.append(card(round(x_41_29, 2), 404, round(x_17_12 - x_41_29, 2), 22, rx=4, fill=GREEN_SOFT, stroke=GREEN, sw=1.6))
        el.append(txt((x_41_29 + x_17_12) / 2, 419, "宽仅 1/348 ≈ 0.0029", size=11.1, color=GREEN, anchor="middle", weight="700"))

        el.append(seg_svg((zx0, zy), (zx1, zy), color=SLATE, sw=1.8))
        el.append(seg_svg((z_rt2, 384), (z_rt2, zy + 8), color=RED, sw=2.1, dash="4 3"))
        el.append(dot_svg((z_rt2, zy), r=4.2, fill=CARD_BG, stroke=RED, sw=2.0))
        el.append(txt(z_rt2, 396, "√2 ≈ 1.41421", size=11.2, color=RED, anchor="middle", weight="700", halo=True))

        el.append(dot_svg((x_41_29, zy), r=4.2, fill=BLUE, stroke=CARD_BG, sw=1.5))
        el.append(txt(x_41_29, zy + 20, "41/29", size=11.3, color=BLUE, anchor="middle", weight="700"))
        el.append(txt(x_41_29, zy + 35, "1.4138", size=11, color=MUTED, anchor="middle", cls="mono"))

        el.append(dot_svg((x_17_12, zy), r=4.2, fill=ORANGE, stroke=CARD_BG, sw=1.5))
        el.append(txt(x_17_12, zy + 20, "17/12", size=11.3, color=ORANGE, anchor="middle", weight="700"))
        el.append(txt(x_17_12, zy + 35, "1.4167", size=11, color=MUTED, anchor="middle", cls="mono"))

        svg = figure(
            538,
            "欧多克斯比例定义V.5的有理数筛子与渐进分数区间套",
            "上图按佩尔渐进分数1/1、3/2、7/5、17/12、41/29依次检验整数倍mA与nB、mC与nD的大小关系，2m²与n²仅相差±1且两组正方形判决完全同步；下图在数轴与局部放大镜上展示有理区间[1,3/2]⊃[7/5,3/2]⊃[7/5,17/12]⊃[41/29,17/12]层层收口锁定√2。",
            el,
        )
        write_svg("eudoxus", "eudoxus-rational-sieve.svg", svg)
        return svg


    # ---------------------------------------------------------------------------
    # 6. Dedekind Cut Line, Archimedean Axiom & Cauchy Sequence Bridge SVG
    # ---------------------------------------------------------------------------
    def build_dedekind_cut_line():
        rt2 = math.sqrt(2.0)
        # Verify Dedekind cut class memberships and Cauchy width shrinkage
        left_rats = [Fraction(1, 1), Fraction(7, 5), Fraction(41, 29), Fraction(239, 169)]
        right_rats = [Fraction(2, 1), Fraction(3, 2), Fraction(17, 12), Fraction(99, 70)]
        for q in left_rats:
            assert q * q < 2
        for q in right_rats:
            assert q * q > 2
        widths = [float(b - a) for a, b in zip(left_rats, right_rats)]
        assert widths[-1] < 0.0003 and all(widths[i + 1] < widths[i] for i in range(len(widths) - 1))

        el = []
        el += header(
            "戴德金分割（1872）：从“比较有理数”到“把切口本身定义为实数”",
            "对比有理切口 3/2 与无理针眼缺口 √2，并看清阿基米德公理与柯西基本列如何共同织出完备实数轴 ℝ",
        )

        x_left, x_right = 56.0, 704.0

        def map_cut(v, vmin=0.60, vmax=2.15):
            return x_left + (v - vmin) / (vmax - vmin) * (x_right - x_left)

        # ---- Panel 1: Rational Cut at 3/2 ----
        el.append(card(20, 66, 720, 128))
        el.append(txt(36, 89, "对照一：有理数切口（以 3/2 为例）——右集合自带最小有理数端点", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(562, 73, "已有现成有理数 3/2", fg=SLATE, bg=SLATE_SOFT, w=162, h=22, size=11.3))

        y1 = 142.0
        xc_rat = map_cut(1.5)
        # Left ray L_{3/2} in BLUE, Right ray U_{3/2} in ORANGE
        el.append(seg_svg((x_left, y1), (xc_rat - 5, y1), color=BLUE, sw=3.2))
        el.append(seg_svg((xc_rat, y1), (x_right, y1), color=ORANGE, sw=3.2))
        el.append(seg_svg((xc_rat, 106), (xc_rat, 178), color=SLATE, sw=1.5, dash="4 3"))

        # Open circle on Left (no max in L), Solid dot on Right (min U = 3/2!)
        el.append(dot_svg((xc_rat - 8, y1), r=4.5, fill=CARD_BG, stroke=BLUE, sw=2.0))
        el.append(dot_svg((xc_rat, y1), r=5.2, fill=ORANGE, stroke=CARD_BG, sw=1.6))

        el.append(txt(206, 124, "左集 L = { q ∈ ℚ : q < 3/2 }（无最大数）", size=11.5, color=BLUE, anchor="middle", weight="700"))
        el.append(txt(548, 124, "右集 U = { q ∈ ℚ : q ≥ 3/2 }（有最小数 min U = 3/2！）", size=11.5, color=ORANGE, anchor="middle", weight="700"))

        for v, s in ((1.0, "1"), (1.25, "5/4"), (1.5, "3/2（实心归 U）"), (1.75, "7/4"), (2.0, "2")):
            xv = map_cut(v)
            el.append(seg_svg((xv, y1 - 4), (xv, y1 + 4), color=SLATE, sw=1.4))
            el.append(txt(xv, y1 + 22, s, size=11.2, color=ORANGE if v == 1.5 else MUTED, anchor="middle", weight="700" if v == 1.5 else None))

        # ---- Panel 2: Irrational Cut at sqrt(2) Pinhole Gap ----
        el.append(card(20, 206, 720, 166))
        el.append(txt(36, 229, "对照二：无理数切口（q² < 2 与 q² > 2）——有理数轴 ℚ 在此露出“针眼缺口”！", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(pill(550, 213, "令切口 (L, U) ≡ √2 ∈ ℝ", fg=RED, bg=RED_SOFT, w=174, h=22, size=11.3))

        y2 = 294.0
        xc_irr = map_cut(rt2)
        el.append(seg_svg((x_left, y2), (xc_irr - 7, y2), color=BLUE, sw=3.4))
        el.append(seg_svg((xc_irr + 7, y2), (x_right, y2), color=ORANGE, sw=3.4))

        # Scissors / cut line through the pinhole gap
        el.append(seg_svg((xc_irr, 246), (xc_irr, 344), color=RED, sw=2.0, dash="4 3"))
        # Pinhole gap ring in Q
        el.append(dot_svg((xc_irr, y2), r=5.6, fill=CARD_BG, stroke=RED, sw=2.2))

        el.append(txt(196, 266, "L = { q<0 或 q²<2 }：无最大有理数！", size=11.5, color=BLUE, anchor="middle", weight="700"))
        el.append(txt(556, 266, "U = { q>0 且 q²>2 }：也无最小有理数！", size=11.5, color=ORANGE, anchor="middle", weight="700"))
        el.append(txt(xc_irr, 252, "ℚ 中空缺针眼，ℝ 补上 sup L = √2", size=11.3, color=RED, anchor="middle", weight="700", halo=True))

        # Sample rational points crowding toward the pinhole from left and right
        crowd_pts = [
            (0.8, "4/5", BLUE, 20),
            (1.0, "1", BLUE, 20),
            (1.25, "5/4", BLUE, 20),
            (1.4, "7/5", BLUE, -12),
            (17.0 / 12.0, "17/12", ORANGE, 36),
            (1.5, "3/2", ORANGE, -12),
            (1.75, "7/4", ORANGE, 20),
            (2.0, "2", ORANGE, 20),
        ]
        for v, s, col, dy in crowd_pts:
            xv = map_cut(v)
            el.append(dot_svg((xv, y2), r=3.2, fill=col, stroke=CARD_BG, sw=1.1))
            el.append(txt(xv, y2 + dy, s, size=11.1, color=col, anchor="middle", weight="600"))

        el.append(
            txt(
                380,
                356,
                "完备性本质：有理数虽然稠密却遍布“无端点切口”；实数轴 ℝ 让每一个戴德金分割都拥有最小上界 sup L",
                size=11.3,
                color=BODY,
                anchor="middle",
                weight="600",
            )
        )

        # ---- Panel 3: Two Bridges — Archimedean Axiom + Cauchy Sequences ----
        el.append(card(20, 384, 352, 138))
        el.append(txt(36, 407, "地基防线：阿基米德公理排除非零无穷小", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(txt(36, 431, "若存在正无穷小 ε > 0（满足对一切正整数 m 都有", size=11.3, color=BODY))
        el.append(txt(36, 450, "m·ε < 1），则 1 与 1+ε 之间插不进任何有理数 n/m，", size=11.3, color=BODY))
        el.append(txt(36, 469, "两数会共用同一个有理数分割！", size=11.3, color=ORANGE, weight="700"))
        el.append(card(36, 480, 320, 30, rx=6, fill=BLUE_SOFT, stroke=BLUE, sw=1))
        el.append(txt(196, 499, "阿基米德性质：∃m 使 m(y−x) > 1 ⇒ 必有 n/m 隔开 x, y", size=11.1, color=BLUE, anchor="middle", weight="700"))

        el.append(card(388, 384, 352, 138))
        el.append(txt(404, 407, "殊途同归：从两侧夹逼走向柯西基本列", size=PANEL_TITLE, color=INK, weight="700"))
        el.append(txt(404, 431, "从左集 L 挑递增有理数 aₖ = 1, 7/5, 41/29, 239/169, …", size=11.3, color=BODY))
        el.append(txt(404, 450, "项间距离 |aⱼ − aₖ| → 0，构成有理“柯西序列”，", size=11.3, color=BODY))
        el.append(txt(404, 469, "在 ℚ 内无家可归，在 ℝ 内收敛向同一极限 √2！", size=11.3, color=GREEN, weight="700"))
        el.append(card(404, 480, 320, 30, rx=6, fill=GREEN_SOFT, stroke=GREEN, sw=1))
        el.append(txt(564, 499, "戴德金分割完备化 ⇔ 康托尔—柯西序列完备化（同构）", size=11.1, color=GREEN, anchor="middle", weight="700"))

        svg = figure(
            536,
            "戴德金分割、阿基米德公理与柯西基本列的实数完备化图解",
            "上图展示有理切口3/2的右集U自带最小数3/2；中图展示无理切口q²<2与q²>2在有理数轴Q上留出针眼缺口，戴德金将切口本身定义为√2从而实现最小上界完备性；下图左栏说明阿基米德公理排除非零无穷小以保证有理数能隔开不同实数，右栏连接康托尔-柯西序列构造。",
            el,
        )
        write_svg("eudoxus", "dedekind-cut-line.svg", svg)
        return svg


    # ---------------------------------------------------------------------------
    # Strict Automated Text-Overlap & UX Auditor
    # ---------------------------------------------------------------------------
    def estimate_text_width(s, font_size):
        w = 0.0
        for ch in s:
            if ord(ch) > 127:
                w += 0.96 * font_size
            elif ch in "il.,:;!|' ":
                w += 0.34 * font_size
            else:
                w += 0.58 * font_size
        return w


    def assert_no_text_overlaps(svg_str, name):
        root = ET.fromstring(svg_str)
        ns = "{http://www.w3.org/2000/svg}"
        boxes = []
        for t in root.iter(f"{ns}text"):
            content = "".join(t.itertext()).strip()
            if not content:
                continue
            x = float(t.attrib["x"])
            y = float(t.attrib["y"])
            sz = float(t.attrib.get("font-size", "12"))
            anc = t.attrib.get("text-anchor", "start")
            tw = estimate_text_width(content, sz)
            if anc == "middle":
                x0, x1 = x - tw / 2.0, x + tw / 2.0
            elif anc == "end":
                x0, x1 = x - tw, x
            else:
                x0, x1 = x, x + tw
            y0, y1 = y - 0.80 * sz, y + 0.18 * sz
            assert 2.0 <= x0 and x1 <= WIDTH - 2.0, f"[{name}] Text out of horizontal bounds: '{content}' ({x0:.1f}..{x1:.1f})"
            boxes.append((x0, y0, x1, y1, content))

        for i in range(len(boxes)):
            ax0, ay0, ax1, ay1, sa = boxes[i]
            for j in range(i + 1, len(boxes)):
                bx0, by0, bx1, by1, sb = boxes[j]
                ix = min(ax1, bx1) - max(ax0, bx0)
                iy = min(ay1, by1) - max(ay0, by0)
                if ix > 2.5 and iy > 2.0:
                    raise AssertionError(
                        f"[{name}] Text overlap ({ix:.1f}x{iy:.1f}px) between '{sa}' and '{sb}'"
                    )

    return {
        "pascal": (
            ("pascal-menelaus-proof.svg", build_pascal_menelaus_proof),
            ("pappus-two-lines.svg", build_pappus_two_lines),
            ("brianchon-dual.svg", build_brianchon_dual),
        ),
        "eudoxus": (
            ("square-incommensurable.svg", build_square_incommensurable),
            ("eudoxus-rational-sieve.svg", build_eudoxus_rational_sieve),
            ("dedekind-cut-line.svg", build_dedekind_cut_line),
        ),
        "audit_overlap": assert_no_text_overlaps,
    }


@register("pascal-hexagon", "帕斯卡神秘六边形：梅涅劳斯与圆幂证明、帕普斯退化与布利安桑对偶", "geometry_analysis")
def build_pascal_hexagon():
    suite = _projective_and_eudoxus_suite()
    for fname, fn in suite["pascal"]:
        svg = fn()
        suite["audit_overlap"](svg, fname)


@register("eudoxus-cuts", "欧多克斯比例论与戴德金分割：正方形不可公度、有理筛子与实数完备化", "geometry_analysis")
def build_eudoxus_cuts():
    suite = _projective_and_eudoxus_suite()
    for fname, fn in suite["eudoxus"]:
        svg = fn()
        suite["audit_overlap"](svg, fname)
