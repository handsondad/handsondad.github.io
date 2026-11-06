"""Generate original cartography diagrams and verify their teaching models."""

import math
from pathlib import Path

from generate_kepler_newton_visuals import (
    BLUE, GOLD, INK, RED, dot, line, panel, path, save, text,
)


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "mercator-maps"
R = 6371.0
GRID = "#c0d0db"


def radians(degrees):
    return math.radians(degrees)


def mercator_y(latitude):
    phi = radians(latitude)
    return math.asinh(math.tan(phi))


def circle(x, y, radius, color=BLUE, fill="none", width=3):
    return (
        f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius:.3f}" '
        f'fill="{fill}" stroke="{color}" stroke-width="{width}"/>'
    )


def rectangle(x, y, width, height, fill="#fff", stroke=GRID):
    return (
        f'<rect x="{x:.3f}" y="{y:.3f}" width="{width:.3f}" '
        f'height="{height:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    )


def output(name, height, title, description, body):
    save(name, height, title, description, body, output_directory=OUT)


def latitude_scale():
    body = text(36, 52, "① 越往北，同样一度经度越短", 29)
    body += text(36, 92, "先看地球侧面：纬度圈的半径不是都一样", 23)
    body += panel(118, 410)
    cx, cy, radius = 345, 310, 150
    body += circle(cx, cy, radius, INK, "#eaf3f7")
    body += line(cx, cy - radius, cx, cy + radius, GRID, True)
    body += line(cx - radius, cy, cx + radius, cy, BLUE)
    phi = radians(60)
    x, y = cx + radius * math.cos(phi), cy - radius * math.sin(phi)
    body += line(cx - radius * math.cos(phi), y, x, y, RED)
    body += line(cx, cy, x, y, RED)
    body += path([
        (cx + 48 * math.cos(t), cy - 48 * math.sin(t))
        for t in [phi * i / 40 for i in range(41)]
    ], GOLD)
    body += text(405, 289, "60°", 24, RED)
    body += text(532, cy + 8, "赤道", 24, BLUE)
    body += text(442, y - 15, "北纬 60°", 24, RED)
    body += dot(cx, cy, color=INK) + text(306, 378, "球心", 22)
    body += text(66, 499, "红线长 = 蓝线长 × cos 60° = 一半", 24)
    body += panel(552, 228)
    for row, (lat, length, color) in enumerate([
        (0, 111.2, BLUE), (60, 55.6, RED),
    ]):
        yy = 604 + row * 73
        body += text(54, yy, f"{lat}° 纬度", 23, color)
        body += line(210, yy - 8, 210 + 3 * length, yy - 8, color)
        body += text(560, yy, f"{length:.1f} km", 23, color)
    body += text(54, 753, "球形模型 R = 6371 km；沿纬线跨过 1° 经度", 22)
    body += text(36, 820, "如果地图把各纬度的一度经度都画成同样宽，", 23)
    body += text(36, 856, "北纬 60° 的东西方向，就已经被放大了两倍。", 23)
    output(
        "latitude-scale.svg", 892, "纬度圈与东西方向的长度",
        "球体侧面截面显示北纬60度的纬度圈半径是赤道的一半。"
        "半径6371千米的球形模型中，一度经度沿纬线分别约111.2和55.6千米。",
        body,
    )


def grids():
    body = text(36, 52, "② 横向拉宽以后，纵向也要补偿", 29)
    body += text(36, 92, "先看同一个地面小圆，再看整张经纬网", 24)
    for top, label, rx, ry, color, first, second in [
        (116, "地面小圆", 22, 22, INK, "参考尺寸：横向 1，纵向 1", "放在北纬 60° 附近"),
        (300, "A  只补横向", 44, 22, BLUE, "东西 ×2，南北 ×1", "圆变扁：局部角度被改变"),
        (484, "B  再补纵向", 44, 44, RED, "东西 ×2，南北 ×2", "仍是圆：局部角度保住了"),
    ]:
        body += panel(top, 166)
        body += text(50, top + 37, label, 24, color)
        body += (
            f'<ellipse cx="172" cy="{top + 103}" rx="{rx}" ry="{ry}" '
            f'fill="#e8f1f5" stroke="{color}" stroke-width="3"/>'
        )
        body += line(172 - rx, top + 103, 172 + rx, top + 103, color)
        body += line(172, top + 103 - ry, 172, top + 103 + ry, color)
        body += text(282, top + 86, first, 25, color)
        body += text(282, top + 128, second, 23)
    body += text(36, 695, "小圆是局部极限示意；大圆范围不能直接套 ×2。", 22)
    body += text(36, 738, "再看全图：同一赤道尺度，经度 ±180°，纬度 ±75°", 22)
    for index, (top, mercator) in enumerate([(802, False), (1190, True)]):
        width, left = 568, 104
        scale = width / (2 * math.pi)
        height = 2 * scale * (mercator_y(75) if mercator else radians(75))
        project = (
            (lambda latitude: top + height / 2
             - mercator_y(latitude) / mercator_y(75) * height / 2)
            if mercator else
            (lambda latitude: top + height / 2 - latitude / 75 * height / 2)
        )
        body += text(36, top - 20, (
            "A  等间距纬线：高纬地区的小图形会变扁"
            if index == 0 else "B  墨卡托纬线：越靠两极，间距越大"
        ), 24, BLUE if index == 0 else RED)
        body += rectangle(left, top, width, height, "#fff")
        for lon in range(-180, 181, 60):
            xx = left + (lon + 180) / 360 * width
            body += line(xx, top, xx, top + height, GRID)
        for lat in range(-60, 61, 15):
            yy = project(lat)
            body += line(left, yy, left + width, yy, RED if lat == 60 else GRID)
            if lat in [-60, -30, 0, 30, 60]:
                body += text(91, yy + 7, f"{lat}°", 21, RED if lat == 60 else INK, "end")
        for lon, label in [(-180, "180°西"), (0, "0°"), (180, "180°东")]:
            xx = left + (lon + 180) / 360 * width
            body += text(xx, top + height + 32, label, 21, INK, "middle")
    body += text(36, 1657, "两条红线都标 60°，不是两条航线或拉伸方向。", 23)
    body += text(36, 1694, "看灰色横线：下图越靠两极，相邻纬线越远。", 23)
    body += text(36, 1731, "这里是数学示意，不是 1569 年古地图的复制。", 22)
    output(
        "grid-stretch.svg", 1770, "同一个地面小圆的拉伸与两种经纬网",
        "先把北纬60度附近的同一个地面微小圆作为参考，"
        "等距经纬网投影中横向倍率2、纵向倍率1，变为扁椭圆；"
        "墨卡托中两个方向倍率均为2，仍为圆。形状用局部线性近似并放大展示。"
        "再以同样范围和赤道尺度比较等经纬间距与球面墨卡托投影，"
        "经线等距，墨卡托纬线间距随纬度升高而增大。纬度截断于正负75度。",
        body,
    )


def distortion():
    body = text(36, 52, "③ 形状保住了，面积却付出了代价", 29)
    body += text(36, 92, "同样的地面小圆，在不同纬度的局部放大倍数", 23)
    for i, latitude in enumerate([0, 30, 60]):
        top = 122 + i * 236
        scale = 1 / math.cos(radians(latitude))
        body += panel(top, 214)
        body += circle(162, top + 106, 28 * scale, BLUE, "#ddecf3")
        body += line(162 - 28 * scale, top + 106, 162 + 28 * scale, top + 106, BLUE)
        body += text(260, top + 55, f"纬度 {latitude}°", 26)
        body += text(260, top + 105, f"长度倍率  k = {scale:.3f}", 24, BLUE)
        body += text(260, top + 152, f"面积倍率  k² = {scale**2:.3f}", 24, RED)
    body += text(36, 881, "在 60°：横向 ×2，纵向 ×2，面积就是 ×4。", 23)
    body += text(36, 920, "小圆仍是圆，但它不再代表相同的纸上面积。", 23)
    body += text(36, 959, "局部极限示意；不是把整个国家统一缩放。", 22)
    output(
        "distortion-budget.svg", 997, "墨卡托投影的局部长度和面积失真",
        "三个同样大小的地面小圆分别在0、30、60度纬度，"
        "图上半径按正割纬度放大，面积倍率为长度倍率的平方。"
        "这是微小区域的局部近似，不是有限国家轮廓。",
        body,
    )


def unit_vector(longitude, latitude):
    lon, lat = radians(longitude), radians(latitude)
    return math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)


def great_circle_points(count=240):
    a, b = unit_vector(-60, 40), unit_vector(60, 40)
    omega = math.acos(sum(x * y for x, y in zip(a, b)))
    result = []
    for i in range(count + 1):
        fraction = i / count
        wa = math.sin((1 - fraction) * omega) / math.sin(omega)
        wb = math.sin(fraction * omega) / math.sin(omega)
        vector = tuple(wa * x + wb * y for x, y in zip(a, b))
        assert math.isclose(sum(x * x for x in vector), 1, abs_tol=1e-12)
        lon = math.degrees(math.atan2(vector[1], vector[0]))
        lat = math.degrees(math.asin(vector[2]))
        result.append((lon, lat))
    return result, omega * R


def routes():
    points, shortest = great_circle_points()
    rhumb = R * math.cos(radians(40)) * radians(120)
    body = text(36, 52, "④ 地图上的直线，不一定是最短路", 29)
    body += text(36, 92, "教学航线：A（西经 60°，北纬 40°）", 23)
    body += text(36, 128, "　　　　　B（东经 60°，北纬 40°）", 23)
    left, top, width = 98, 182, 574
    scale = width / radians(150)
    height = scale * (mercator_y(70) - mercator_y(20))

    def project(lon, lat):
        return (
            left + (lon + 75) / 150 * width,
            top + (mercator_y(70) - mercator_y(lat))
            / (mercator_y(70) - mercator_y(20)) * height,
        )

    body += rectangle(left, top, width, height)
    for latitude in range(20, 71, 10):
        yy = project(0, latitude)[1]
        body += line(left, yy, left + width, yy, GRID)
        body += text(86, yy + 6, f"{latitude}°", 21, INK, "end")
    for longitude in range(-60, 61, 30):
        xx = project(longitude, 20)[0]
        body += line(xx, top, xx, top + height, GRID)
        body += text(xx, top + height + 30, f"{longitude}°", 21, INK, "middle")
    a, b = project(-60, 40), project(60, 40)
    body += line(*a, *b, RED, True)
    body += path([project(*p) for p in points], BLUE, 4)
    for index in [0, 60, 120, 180, 240]:
        body += dot(*project(*points[index]), r=6, color=BLUE)
    body += dot(*a, color=INK) + dot(*b, color=INK)
    body += text(a[0] - 18, a[1] + 37, "A", 25)
    body += text(b[0] + 9, b[1] + 37, "B", 25)
    body += text(385, project(0, points[120][1])[1] - 18, "最高约 59.21°N", 22, BLUE, "middle")
    body += panel(560, 244)
    body += line(50, 611, 104, 611, RED, True)
    body += text(122, 618, f"恒向线：一直向东，约 {rhumb:,.0f} km", 24, RED)
    body += line(50, 669, 104, 669, BLUE)
    body += text(122, 676, f"大圆短弧：航向改变，约 {shortest:,.0f} km", 24, BLUE)
    body += text(52, 737, f"这一次，恒向线多走了约 {rhumb - shortest:.0f} km。", 24)
    body += text(52, 777, "球形地球、无障碍；不是实际航班或航海建议。", 22)
    body += text(36, 848, "蓝色圆点等分大圆弧长，不表示船的实测位置。", 23)
    output(
        "rhumb-great-circle.svg", 886, "恒向线与大圆最短路",
        "同在北纬40度、经度相差120度的两点。"
        "墨卡托图上水平虚线为向东的恒向线，实线为向北弯的大圆短弧。"
        "按半径6371千米的球形模型计算长度，约10222与9243千米。",
        body,
    )


def triangulation():
    a, b, c = (105, 536), (575, 536), (293, 160)
    alpha, beta = math.atan2(80, 40), math.atan2(80, 60)
    body = text(36, 52, "⑤ 不必走到山顶，也能测出它在哪", 29)
    body += text(36, 92, "平坦局部教学模型：先测基线，再测两个角", 23)
    body += panel(116, 491)
    body += path([a, c, b, a], BLUE)
    body += line(c[0], c[1], c[0], a[1], GRID, True)
    for origin, angle, direction in [(a, alpha, 1), (b, beta, -1)]:
        body += path([
            (origin[0] + direction * 62 * math.cos(angle * i / 40),
             origin[1] - 62 * math.sin(angle * i / 40))
            for i in range(41)
        ], GOLD)
    for point, label, dx, dy in [(a, "A", -34, 6), (b, "B", 14, 6), (c, "C 山顶", 18, -9)]:
        body += dot(*point, color=INK) + text(point[0] + dx, point[1] + dy, label, 24)
    body += text(138, 478, f"α ≈ {math.degrees(alpha):.2f}°", 23, GOLD)
    body += text(391, 478, f"β ≈ {math.degrees(beta):.2f}°", 23, GOLD)
    body += text(340, 582, "基线 AB = 100 m", 24, BLUE, "middle")
    body += text(117, 348, "AC ≈", 22, BLUE, "middle")
    body += text(117, 380, "89.44 m", 22, BLUE, "middle")
    body += text(343, 379, "垂距", 22)
    body += text(343, 412, "80 m", 22)
    body += panel(635, 214)
    body += text(50, 681, "先看底边：只把 AB 的长度量出来。", 24)
    body += text(50, 734, "再看两角：两条视线决定 C 的位置。", 24)
    body += text(50, 787, "最后接网：换一条已知边，继续测下一点。", 24)
    body += text(36, 895, "真实测量还要处理地形、曲率、折射和观测误差。", 23)
    output(
        "triangulation.svg", 936, "基线与两个角决定第三点",
        "教学坐标A为0,0，B为100,0，C为40,80米。"
        "底角约63.43与53.13度，AC约89.44米。"
        "画图与计算使用同一比例；实际测量还需误差与地球曲率处理。",
        body,
    )


def contours():
    body = text(36, 52, "⑥ 山的高度，怎样变成一圈圈线", 29)
    body += text(36, 92, "原创光滑山丘模型：山顶 100 m，非实测地形", 23)
    body += panel(116, 374)
    left, top, width, height = 80, 165, 566, 267
    project = lambda x, z: (left + (x + 150) / 300 * width, top + height - z / 100 * height)
    profile = [(x, 100 * math.exp(-(x / 80) ** 2)) for x in range(-150, 151)]
    body += path([project(*p) for p in profile], BLUE, 4)
    body += line(left, top + height, left + width, top + height, INK)
    for elevation in [20, 40, 60, 80]:
        xx = 80 * math.sqrt(-math.log(elevation / 100))
        yy = project(0, elevation)[1]
        body += line(left, yy, left + width, yy, GRID, True)
        body += text(66, yy + 6, str(elevation), 21, INK, "end")
        body += dot(*project(-xx, elevation), color=RED)
        body += dot(*project(xx, elevation), color=RED)
    body += text(99, 154, "剖面：同一高度，找到两侧交点", 23)
    body += text(340, 467, "剖面纵向放大约 1.42 倍；左右距离同尺度", 22, INK, "middle")
    body += panel(517, 465)
    body += text(52, 562, "俯视：把所有同高点连起来", 24)
    cx, cy, scale = 360, 773, 1.7
    for elevation, angle in [(20, -35), (40, -15), (60, 25), (80, 65)]:
        radius = 80 * math.sqrt(-math.log(elevation / 100))
        body += circle(cx, cy, radius * scale, GOLD)
        label_x = cx + radius * scale * math.cos(radians(angle))
        label_y = cy - radius * scale * math.sin(radians(angle))
        body += dot(label_x, label_y, 3, GOLD)
        body += rectangle(label_x + 7, label_y - 20, 57, 31, "#fff", "#fff")
        body += text(label_x + 10, label_y + 7, f"{elevation} m", 22, GOLD)
    body += dot(cx, cy, color=BLUE) + text(cx, cy - 17, "100 m", 22, BLUE, "middle")
    body += text(52, 964, "等高距固定为 20 m；线距由山的坡形决定。", 22)
    body += text(36, 1027, "同样爬升 20 m，平面距离越短，坡就越陡。", 23)
    output(
        "contour-hill.svg", 1068, "山丘剖面与等高线",
        "山丘高度为100乘以exp(-(x平方+y平方)/80平方)米，"
        "等高线为半径80乘以sqrt(-ln(h/100))米的圆。"
        "对应20、40、60、80米高度，剖面交点与俯视圆来自同一模型。"
        "剖面纵向相对于横向放大约1.42倍，俯视图两个方向使用同一尺度。",
        body,
    )


def generalization():
    river = [(0, 215), (70, 197), (150, 211), (245, 162), (295, 169), (360, 137), (450, 150), (568, 80)]
    road = [(0, 68), (110, 78), (225, 73), (327, 91), (448, 72), (568, 68)]
    branch = [(225, 73), (245, 162), (272, 270)]
    houses = [(60, 42), (97, 42), (148, 94), (184, 104), (287, 56), (335, 115), (376, 94), (465, 35)]
    body = text(36, 52, "⑦ 地图不是照片：它必须选择", 29)
    body += text(36, 92, "同一虚构小镇：比较细节与概览的表达方式", 23)
    for index, top in enumerate([160, 581]):
        left = 76
        body += text(36, top - 22, (
            "A  细节表达：小路、建筑、河道弯曲都保留"
            if index == 0 else "B  概览表达：保留连接，减少细碎信息"
        ), 24)
        body += rectangle(left, top, 568, 285, "#fff")
        translate = lambda coords: [(left + x, top + y) for x, y in coords]
        selected = river if index == 0 else [river[i] for i in [0, 2, 3, 5, 7]]
        body += path(translate(selected), BLUE, 5 if index == 0 else 7)
        body += path(translate(road), RED, 4 if index == 0 else 7)
        body += path(translate(branch), RED, 4 if index == 0 else 7)
        bridge = translate([branch[1]])[0]
        body += rectangle(bridge[0] - 9, bridge[1] - 8, 18, 16, "#fff", INK)
        if index == 0:
            for x, y in houses:
                body += rectangle(left + x, top + y, 20, 15, "#e9e0cd", GOLD)
            body += path(translate([(97, 49), (97, 78)]), GOLD, 2, True)
            body += path(translate([(345, 122), (330, 91)]), GOLD, 2, True)
        else:
            body += dot(left + 305, top + 75, 11, INK)
            body += text(left + 305, top + 40, "小镇", 25, INK, "middle")
        body += text(left + 404, top + 244, "河流", 22, BLUE)
        body += text(left + 404, top + 37, "主路", 22, RED)
        body += text(left + 286, top + 202, "桥", 22)
    body += text(36, 923, "可省掉细节，但不能把桥画到没有路的地方。", 23)
    body += text(36, 962, "两图为方便比较而同框，不表示相同制图比例尺。", 22)
    output(
        "map-generalization.svg", 1001, "制图综合与连接关系",
        "同一虚构小镇的细节与概览版本，减少小路和建筑，简化河道，"
        "但两版保留相同主路、支路和位于道路河流交点的桥。"
        "两个窗口同框仅为对比，不表示相同实体比例尺。",
        body,
    )


def tiles():
    body = text(36, 52, "⑧ 手机没下载整张世界地图", 29)
    body += text(36, 92, "它通常只取当前视野附近所需的地图瓦片", 23)
    for level, top in enumerate([162, 530, 898]):
        count = 2**level
        body += text(36, top - 24, f"层级 z = {level}：{count} × {count} = {count**2} 块", 25)
        size, left = 254, 68
        cell = size / count
        for row in range(count):
            for column in range(count):
                fill = "#e4edf3" if (row + column) % 2 == 0 else "#fff"
                if row == 0 and column == count - 1:
                    fill = "#f5d89b"
                body += rectangle(left + column * cell, top + row * cell, cell, cell, fill)
        body += text(361, top + 58, "整幅像素宽度", 23)
        body += text(361, top + 104, f"256 × 2^{level} = {256 * count} px", 24, BLUE)
        body += text(361, top + 168, "每块仍是", 23)
        body += text(361, top + 208, "256 × 256 px", 24)
    body += text(36, 1218, "示例：常见的 256 像素栅格瓦片金字塔。", 23)
    body += text(36, 1257, "不是所有服务都同尺寸；也有矢量瓦片。", 23)
    body += text(36, 1296, "黄色只标出一块示例瓦片，不表示下载时序。", 22)
    output(
        "web-tiles.svg", 1337, "地图瓦片金字塔",
        "层级0、1、2的瓦片网格分别为1、4、16块。"
        "每块256像素，整个世界图像宽度分别为256、512、1024像素。"
        "这是常见栅格瓦片模型而非所有服务的统一标准。",
        body,
    )


def validate():
    assert math.isclose(mercator_y(0), 0, abs_tol=1e-15)
    assert math.isclose(mercator_y(45), math.log(1 + math.sqrt(2)), abs_tol=1e-14)
    for latitude in [-75, -60, -30, 0, 30, 60, 75]:
        assert math.isclose(mercator_y(-latitude), -mercator_y(latitude), abs_tol=1e-14)
        phi = radians(latitude)
        epsilon = 1e-6
        derivative = (
            math.asinh(math.tan(phi + epsilon))
            - math.asinh(math.tan(phi - epsilon))
        ) / (2 * epsilon)
        assert math.isclose(derivative, 1 / math.cos(phi), rel_tol=1e-8)
    assert math.isclose(1 / math.cos(radians(60)) ** 2, 4, abs_tol=1e-12)
    reference_radius = 22
    east_scale = 1 / math.cos(radians(60))
    assert math.isclose(reference_radius * east_scale, 44, abs_tol=1e-12)
    assert math.isclose((reference_radius * east_scale) / reference_radius, 2, abs_tol=1e-12)
    assert math.isclose((reference_radius * east_scale) / (reference_radius * east_scale), 1)
    assert mercator_y(75) - mercator_y(60) > mercator_y(15) - mercator_y(0)
    assert math.isclose(math.degrees(math.atan(math.sinh(math.pi))), 85.0511287798066, abs_tol=1e-12)
    points, shortest = great_circle_points()
    assert math.dist(points[0], (-60, 40)) < 1e-12
    assert math.dist(points[-1], (60, 40)) < 1e-12
    assert math.isclose(points[120][1], 59.21026697116785, abs_tol=1e-12)
    assert round(shortest) == 9243
    rhumb = R * math.cos(radians(40)) * radians(120)
    assert round(rhumb) == 10222 and shortest < rhumb
    scale = 568 / (2 * math.pi)
    assert scale * mercator_y(60) > scale * radians(60)
    assert math.isclose(
        (scale * mercator_y(.0001)) / (scale * radians(.0001)),
        1, rel_tol=1e-11,
    )
    a, b = math.atan2(80, 40), math.atan2(80, 60)
    ac = 100 * math.sin(b) / math.sin(a + b)
    assert math.isclose(ac, math.hypot(40, 80), abs_tol=1e-12)
    assert math.isclose(ac * math.sin(a), 80, abs_tol=1e-12)
    for elevation in [20, 40, 60, 80]:
        radius = 80 * math.sqrt(-math.log(elevation / 100))
        assert math.isclose(100 * math.exp(-(radius / 80) ** 2), elevation, abs_tol=1e-12)
    for level in range(0, 21):
        assert (2**level) ** 2 == 4**level
        assert 256 * (2**level) == 2 ** (level + 8)
    assert 0.01 * 25000 == 250
    assert 0.01 * 1000000 == 10000


if __name__ == "__main__":
    validate()
    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [
        latitude_scale, grids, distortion, routes,
        triangulation, contours, generalization, tiles,
    ]:
        draw()
    print("Generated eight static SVGs; projection, route, survey, contour and tile assertions passed.")
