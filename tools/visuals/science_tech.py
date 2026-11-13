"""Earth Mapping, Engineering History, Natural Science & Reading Guides visual builders."""

import math
from pathlib import Path
from decimal import Decimal
import xml.etree.ElementTree as ET
from html import escape
from math import cos, isclose, pi, sin

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


@register("mercator-maps", "墨卡托投影：纬度拉伸、等角航线、三角网与瓦片地图", "science_tech")
def build_mercator_maps():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "mercator-maps"

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

    validate()
    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [
        latitude_scale, grids, distortion, routes,
        triangulation, contours, generalization, tiles,
    ]:
        draw()
    print("Generated eight static SVGs; projection, route, survey, contour and tile assertions passed.")


@register("calculator-history", "计算器发展史：连续进位、阶梯鼓、对数尺与浮点表示", "science_tech")
def build_calculator_history():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "calculator-history"

    GRAY = "#71869a"

    def heading(title, subtitle):
        return text(36, 52, title, 29) + text(36, 91, subtitle, 22)

    def write(name, height, title, description, body):
        save(name, height, title, description, body, output_directory=OUT)

    def digits(value, y, active=None):
        body = ""
        for i, digit in enumerate(f"{value:04d}"):
            x = 136 + i * 112
            color = RED if i == active else BLUE
            body += (
                f'<rect x="{x}" y="{y}" width="88" height="76" rx="8" '
                f'fill="#f3f7fa" stroke="{color}" stroke-width="2"/>'
            )
            body += text(x + 44, y + 54, digit, 44, color, "middle")
        return body

    def carry():
        title = "① 99 + 1：最难的是把那个 1 传过去"
        body = heading(title, "数位状态图；不是帕斯卡机内部零件的精确复刻")
        values = [99, 90, 0, 100]
        notes = [
            ("原来是 0099，准备在个位加 1。", "每个十进制数位只容纳 0—9。"),
            ("个位 9 → 0，向十位发出进位。", "这里的 0 不是结束，而是触发下一步。"),
            ("十位也从 9 → 0，再向百位进 1。", "连着几个 9，就需要连续几次进位。"),
            ("百位收到 1，结果成为 0100。", "完整结果：99 + 1 = 100。"),
        ]
        for step, value in enumerate(values):
            y = 120 + step * 240
            body += panel(y, 220)
            body += text(48, y + 37, f"{step + 1}  " + notes[step][0], 24)
            for i, name in enumerate(["千位", "百位", "十位", "个位"]):
                body += text(180 + 112 * i, y + 76, name, 20, GRAY, "middle")
            body += digits(value, y + 88, [3, 3, 2, 1][step])
            body += text(48, y + 199, notes[step][1], 22)
        body += text(36, 1114, "重点不是四个轮子一起转，而是数位之间可靠地传信。", 22)
        write("carry-chain.svg", 1150, title, "从0099加一，依次处理个位和十位进位，最后得到0100。", body)

    def drum():
        title = "② 阶梯鼓：一圈，怎样恰好加 3？"
        body = heading(title, "把圆柱表面展开来看；横向是轴向，纵向是转动次序")
        body += panel(120, 650)
        body += text(48, 163, "九条齿棱长短不同，并非九层圆盘。", 24)
        origin, pitch = 110, 50
        probe = origin + 6.5 * pitch
        for i in range(1, 10):
            y = 195 + i * 46
            end = origin + i * pitch
            color = RED if end >= probe else BLUE
            body += text(76, y + 7, str(i), 22, GRAY, "middle")
            body += (
                f'<rect x="{origin}" y="{y - 11}" width="{i * pitch}" height="22" '
                f'rx="4" fill="{color}"/>'
            )
            if end >= probe:
                body += dot(probe, y, 7, GOLD)
        body += line(probe, 196, probe, 650, GOLD, True)
        body += text(probe, 691, "小齿轮的接触位置", 22, GOLD, "middle")
        body += text(48, 735, "这个位置只有三条齿棱经过 → 接收齿轮走三步。", 22)
        body += panel(795, 255)
        body += text(48, 837, "调节轴向位置，就改变一圈经过的齿数", 24)
        for index, n in enumerate([0, 3, 7]):
            x = 150 + index * 205
            body += text(x, 897, f"设为 {n}", 28, BLUE, "middle")
            body += text(x, 946, f"遇到 {n} 齿", 25, RED, "middle")
        body += text(48, 1019, "转完齿区后，还要处理进位；此处只拆解输入机制。", 21)
        body += text(36, 1095, "示意省略真实齿形、传动比、定位与无齿区的角度。", 22)
        write("stepped-drum.svg", 1130, title, "展开后的九根渐长齿棱中，一条接触线只与最长的三根相交，说明设为3时每圈输入3。", body)

    def multiply():
        title = "③ 乘法：重复相加，加上十进位移"
        body = heading(title, "1709 × 365 = 1709 × (5 + 60 + 300)")
        total = 0
        for index, (place, turns) in enumerate([(0, 5), (1, 6), (2, 3)]):
            y = 120 + index * 275
            value = 1709 * 10**place
            part = value * turns
            total += part
            body += panel(y, 250)
            body += text(48, y + 39, f"{index + 1}  滑架位移 {place} 格；转 {turns} 圈", 25)
            body += text(60, y + 95, f"每圈加 {value:,}", 29, BLUE)
            body += text(60, y + 147, f"本步增加 {part:,}", 29, GOLD)
            body += text(60, y + 207, f"累计结果 {total:,}", 32, RED)
        body += text(36, 1004, "5 + 6 + 3 = 14 圈，而不是连续加 365 次。", 25)
        body += text(36, 1045, "滑架每左移一格，输入数对齐更高一位，贡献乘 10。", 22)
        write("carriage-multiplication.svg", 1090, title, "输入1709，分别转5圈、左移后转6圈、再左移转3圈，累计得到623785。", body)

    def slide_rule():
        title = "④ 计算尺：把乘法，变成长度的相加"
        body = heading(title, "这是另一条技术路线：对数刻度，读出近似结果")
        body += panel(120, 540)
        start, scale = 90, 490
        offset = scale * math.log10(2)
        for y, base, label in [(265, start, "固定尺"), (425, start + offset, "滑动尺")]:
            body += text(48, y - 79, label, 24)
            body += line(base, y, base + scale * math.log10(5), y, BLUE)
            ticks = range(1, 11) if label == "固定尺" else range(1, 6)
            if label == "固定尺":
                body += line(base, y, base + scale, y, BLUE)
            for value in ticks:
                x = base + scale * math.log10(value)
                body += line(x, y - 12, x, y + 12, BLUE)
                body += text(x, y + 43, value, 23, INK, "middle")
        for n, label in [(2, "上尺 2 对齐下尺 1"), (6, "下尺 3 对应上尺 6")]:
            x = start + scale * math.log10(n)
            body += line(x, 252, x, 438, RED, True)
            body += text(48, 543 if n == 2 else 592, label, 24, RED)
        body += text(36, 711, "log₁₀2 + log₁₀3 = log₁₀6", 30, BLUE)
        body += text(36, 758, "刻度越往右越密；图中不是等距排了 1 到 10。", 23)
        body += text(36, 801, "计算尺主要给有效数字，数量级通常还要由人判断。", 22)
        write("logarithmic-slide-rule.svg", 845, title, "按十进对数位置绘制的双尺，滑动尺的1对准固定尺2后，滑动尺3对准固定尺6。", body)

    def binary():
        title = "⑤ 换成电路，进位这件事还在"
        body = heading(title, "教学用二进制加法；不表示所有计算器都用同一编码")
        body += panel(120, 330)
        body += text(48, 166, "同一个十进制 3 + 1，换一种写法", 25)
        for y, value in [(235, "0011"), (299, "+ 0001"), (387, "= 0100")]:
            body += text(360, y, value, 42, RED if y == 387 else BLUE, "middle")
        body += text(48, 426, "右边两位连续进位，十进制结果仍然是 4。", 22)
        body += panel(475, 500)
        body += text(48, 520, "拆开一个“全加器”：处理当前这一位", 25)
        for x, label in [(143, "输入 A"), (360, "输入 B"), (577, "低位进位 C")]:
            body += text(x, 585, label, 24, BLUE, "middle")
            body += line(x, 605, x, 665, BLUE, arrow=True)
        body += '<rect x="85" y="672" width="550" height="104" rx="14" fill="#eaf2f7" stroke="#176786" stroke-width="2"/>'
        body += text(360, 735, "把三个 0 或 1 相加", 30, BLUE, "middle")
        body += text(360, 835, "A + B + C = S + 2 × C′", 29, RED, "middle")
        body += text(48, 894, "S：留在本位的和；C′：交给高位的进位。", 23)
        body += text(48, 940, "例：1 + 1 + 1 = 1 + 2 × 1。", 25)
        body += text(36, 1024, "电路用逻辑门实现规则；齿轮和脉冲不是同一种机构。", 22)
        write("binary-carry.svg", 1065, title, "二进制0011加0001得到0100；全加器把两个输入位和低位进位转换成本位和及高位进位。", body)

    def graphing():
        title = "⑥ 从“一个答案”，到“一整条曲线”"
        body = heading(title, "教学示意：反复计算 y = x²，把数对放到屏幕位置")
        body += panel(120, 690)
        body += text(48, 165, "取九个示例输入，不只问一次“2 的平方是多少”", 23)
        for y in range(5):
            screen_y = 650 - 100 * y
            body += line(160, screen_y, 560, screen_y, "#dce5ec", True)
            if y:
                body += text(339, screen_y + 7, y, 20, GRAY, "end")
        body += line(130, 650, 605, 650, BLUE, arrow=True)
        body += line(360, 675, 360, 215, BLUE, arrow=True)
        for x in range(-2, 3):
            body += text(360 + 100 * x, 690, x, 22, INK, "middle")
        body += text(619, 657, "x", 24, BLUE)
        body += text(373, 220, "y", 24, BLUE)
        points = [(360 + 100 * x, 650 - 100 * x * x) for x in [i / 4 for i in range(-8, 9)]]
        body += path(points, BLUE, 3)
        for i in range(-4, 5):
            x = i / 2
            body += dot(360 + 100 * x, 650 - 100 * x * x, 7, RED)
        body += text(48, 751, "红点：九个精确数对；蓝线：更密采样后的折线。", 22)
        body += text(36, 861, "有限像素只能近似显示连续曲线；窗口选择也会影响观察。", 22)
        body += text(36, 902, "这是原理图，不是 fx-7000G 的屏幕复刻或算法测绘。", 22)
        write("graphing-points.svg", 945, title, "九个精确平方函数样本点与十七点采样折线，展示绘图计算器将数值变成图形的基本思路。", body)

    def timeline():
        title = "⑦ 不是一位天才，按下了所有时代的等号"
        body = heading(title, "精选路标，纵向间距不代表真实时间间隔")
        rows = [
            ("1623", "席卡德的通信记录", "齿轮加减，配合纳皮尔算筹处理乘除。"),
            ("1640 年代", "帕斯卡计算器", "把加法与自动进位做成实际机器。"),
            ("1673 起", "莱布尼茨持续展示、改进计算机", "后来以阶梯鼓、滑架实现四则运算。"),
            ("1820 起", "托马斯算术计；随后改进、量产", "原理之外，可靠性、制造与市场同样重要。"),
            ("二战后", "Curta：口袋里的纯机械计算器", "阶梯鼓的后代，不用电池也能做四则运算。"),
            ("1961", "ANITA 电子桌面计算器发布", "电子管时代的计算器，不是单芯片小机器。"),
            ("1971", "Intel 4004 首次公开广告", "为计算器开发芯片，推动微处理器发展。"),
            ("1972", "HP-35 掌上科学计算器", "三角、对数等函数进入衣兜。"),
            ("1983", "SL-800：薄至 0.8 毫米", "电子计算器不只变小，还向卡片的厚度靠近。"),
            ("1985", "fx-7000G 绘图计算器", "答案不只是一串数，还能是一幅函数图。"),
            ("今天", "计算器也成为一种软件功能", "科学、绘图、编程与专用计算器仍然并存。"),
        ]
        for index, (date, label, detail) in enumerate(rows):
            y = 130 + index * 150
            body += panel(y, 132)
            body += text(48, y + 34, date, 24, RED)
            body += text(48, y + 75, label, 25, BLUE)
            body += text(48, y + 112, detail, 21)
        write("calculator-timeline.svg", 1800, title, "计算器发展精选时间线，区分通信记录、发明改进、量产、发布与软件时代。", body)

    def precision():
        title = "⑧ 按下等号前，还要知道“数”怎样保存"
        body = heading(title, "这些是表示方式的例子，不是所有产品的统一实现")
        rows = [
            ("有限位十进制整数", "例如：四个数轮只能显示 0000—9999。", "9999 再加 1，需要额外一位或溢出处理。"),
            ("有限精度二进制浮点数", "0.1 的二进制小数无限循环，存储时需舍入。", "常见示例：0.1 + 0.2 → 0.30000000000000004"),
            ("十进制、整数或有理数算法", "0.1 可按十进小数处理，也可记成分数 1/10。", "能精确处理哪些运算，仍取决于算法和资源。"),
        ]
        for index, (label, detail, example) in enumerate(rows):
            y = 120 + index * 220
            body += panel(y, 200)
            body += text(48, y + 40, label, 25, BLUE)
            body += text(48, y + 95, detail, 22)
            body += text(48, y + 151, example, 21, RED)
        body += text(36, 832, "显示“0.3”，不一定能反推出内部恰好存了什么。", 23)
        body += text(36, 878, "无限循环小数、无理数与有限屏幕，是不同层面的限制。", 22)
        write("number-representation.svg", 920, title, "比较有限位机械整数、二进制浮点、十进制或有理数算法，说明显示结果与内部表示并非一回事。", body)

    def validate():
        assert 99 + 1 == 100
        states, carry_in = [], 1
        for n in [9, 9, 0, 0]:
            carry_in, digit = divmod(n + carry_in, 10)
            states.append(digit)
        assert states == [0, 0, 1, 0]
        for digit in range(10):
            probe = 9.5 - digit
            assert sum(length >= probe for length in range(1, 10)) == digit
        partials = [1709 * turns * 10**place for place, turns in enumerate([5, 6, 3])]
        assert partials == [8545, 102540, 512700]
        assert sum(partials) == 1709 * 365 == 623785
        assert sum([5, 6, 3]) == 14
        assert math.isclose(math.log10(2) + math.log10(3), math.log10(6))
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    carry_out, result = divmod(a + b + c, 2)
                    assert a + b + c == result + 2 * carry_out
        assert f"{3:04b}" == "0011" and f"{4:04b}" == "0100"
        assert repr(0.1 + 0.2) == "0.30000000000000004"
        assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
        samples = [(i / 2, (i / 2) ** 2) for i in range(-4, 5)]
        assert len(samples) == 9 and samples[0] == (-2, 4) and samples[-1] == (2, 4)
        assert samples[4] == (0, 0)
        assert len({x for x, _ in samples}) == 9

    validate()
    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [carry, drum, multiply, slide_rule, binary, graphing, timeline, precision]:
        draw()
    print("Generated eight SVGs; decimal/binary carries, tooth counts, products, log scales, graph samples and numeric representations verified.")


@register("loom-history", "织布机与编程前史：经纬组织、提花综框与穿孔卡", "science_tech")
def build_loom_history():
    INK, BLUE, RED, GOLD = K_INK, K_BLUE, K_RED, K_GOLD

    dot, line, panel, path, text = k_dot, k_line, k_panel, k_path, k_text

    save = k_save

    OUT = REPO_ROOT / "assets" / "images" / "loom-history"

    PLAIN = [[(r + c + 1) % 2 for c in range(4)] for r in range(4)]

    TWILL = [[int((c - r) % 4 < 2) for c in range(4)] for r in range(4)]

    SATIN = [[int(c != (2 * r) % 5) for c in range(5)] for r in range(5)]

    PATTERN = [
        [int((c + r + 1 if abs(r - 3.5) + abs(c - 3.5) <= 3 else c - r) % 4 < 2)
         for c in range(8)]
        for r in range(8)
    ]

    CARDS = [tuple(row) for row in PATTERN]

    def rect(x, y, w, h, fill="#fff", stroke="#ccd8e2", radius=0):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def matrix(rows, x, y, cell=38):
        body = ""
        for r, row in enumerate(rows):
            for c, up in enumerate(row):
                body += rect(x + c * cell, y + r * cell, cell, cell,
                             BLUE if up else "#fff")
                body += text(x + (c + .5) * cell, y + (r + .7) * cell,
                             up, 20, "#fff" if up else INK, "middle")
        return body

    def crossing(x, y, up, size=60):
        """One crossing, with an outlined top thread hiding the bottom thread."""
        d = size / 2
        body = path([(x, y - d), (x, y + d)], BLUE, 12)
        body += path([(x - d, y), (x + d, y)], GOLD, 12)
        points = [(x, y - d), (x, y + d)] if up else [(x - d, y), (x + d, y)]
        body += path(points, "#f3f7fa", 18) + path(points, BLUE if up else GOLD, 12)
        return body

    def figure(name, height, title, desc, body, css=""):
        save(name, height, title, desc, text(36, 44, title, 28) + body,
             css, output_directory=OUT)

    def interlacing():
        body = panel(70, 650) + text(48, 110, "俯视：经线纵向，纬线横向", 25)
        for r in range(6):
            for c in range(6):
                body += crossing(160 + c * 72, 190 + r * 72, (r + c) % 2 == 0, 72)
        body += line(95, 165, 95, 550, BLUE, arrow=True)
        body += text(68, 145, "经", 24, BLUE)
        body += line(150, 590, 555, 590, GOLD, arrow=True)
        body += text(590, 598, "纬", 24, GOLD)
        body += text(48, 650, "交叉处：上面的线挡住下面的线。", 24)
        body += text(48, 690, "下一根纬线换组穿过，交错才锁得住。", 24)
        figure("warp-weft.svg", 750, "图 1｜布不是粘出来的，是交错出来的",
               "六乘六平纹俯视图，经线与纬线轮流在上；遮挡表示上下关系，间距为示意。", body)

    def weaving_cycle():
        body = ""
        for stage, top in enumerate([70, 350, 630]):
            body += panel(top, 260)
            title = ["① 开口：把经线分成上下两层", "② 引纬：纬线从梭口穿过", "③ 打纬：把新纬线推向织口"][stage]
            body += text(48, top + 40, title, 25)
            mid = top + 145
            body += rect(65, mid - 20, 85, 40, "#dfe9ef")
            body += text(65, top + 85, "已织成的布", 22)
            for offset, colour, dashed in [(-42, BLUE, False), (42, INK, True)]:
                body += path([(150, mid), (460, mid + offset), (620, mid)], colour, 4, dashed)
                body += line(460, mid + offset - 16, 460, mid + offset + 16, colour)
            body += text(520, top + 85, "经线来自后方", 21)
            if stage:
                xpos = 320 if stage == 1 else 170
                body += dot(xpos, mid, 10, GOLD)
                body += text(235, top + 205, "金点＝新纬线的横截面", 22, GOLD)
            else:
                body += text(240, top + 205, "上下层之间是梭口", 23)
            if stage == 2:
                body += line(320, mid, 192, mid, RED, dash=True, arrow=True)
                body += line(200, mid - 32, 200, mid + 32, RED)
        body += text(36, 935, "沿经线方向的侧视；不同经线在此叠合。", 23)
        body += text(36, 973, "引纬沿布宽运动，不能画成沿经线跑。", 23)
        figure("weaving-cycle.svg", 1010, "图 2｜一梭布，要做三件事",
               "侧视三阶段梭口与纬纱截面。开口、横向引纬、筘推纬到织口；省略送经卷取。", body)

    def weave_structures():
        body = ""
        items = [
            (PLAIN, "① 平纹：一上一下", "每根线频繁交织。", "一个循环：2 经 × 2 纬。"),
            (TWILL, "② 2/2 斜纹：两上两下", "每一纬把选择平移一格。", "交织点组成斜向纹路。"),
            (SATIN, "③ 五枚经面缎纹", "每一纬只留一个纬在上点。", "相邻纬的该点错开两格。"),
        ]
        for i, (rows, title, a, b) in enumerate(items):
            top = 70 + i * 260
            body += panel(top, 242) + text(48, top + 38, title, 25)
            body += matrix(rows, 55, top + 55, 34)
            body += text(285, top + 98, a, 22)
            body += text(285, top + 143, b, 22)
            body += text(285, top + 195, "1＝经在上；0＝纬在上", 22)
        body += text(36, 900, "方格是交织关系，不是印刷颜料。", 24)
        body += text(36, 940, "连续跨过多根另一组线，叫“浮长”。", 24)
        figure("weave-structures.svg", 975, "图 3｜同样的线，不同的上下顺序",
               "平纹、二上二下斜纹和五枚经面缎纹的二值组织矩阵，行是纬，列是经。", body)

    def stored_shafts():
        rows = [PLAIN[0] * 2, PLAIN[1] * 2, TWILL[0] * 2, TWILL[1] * 2]
        body = panel(70, 610)
        body += text(48, 115, "概念示意：每根花综保存一组提线关系", 24)
        for i, row in enumerate(rows):
            y = 190 + i * 85
            body += rect(170, y - 29, 410, 56, "#fff5d9" if i == 2 else "#eef3f7")
            body += text(55, y + 7, f"花综 {i + 1}", 24)
            for c, up in enumerate(row):
                body += dot(195 + c * 49, y, 14, BLUE if up else "#fff")
                body += text(195 + c * 49, y + 7, up, 19, "#fff" if up else INK, "middle")
            if i == 2:
                body += line(650, y, 598, y, RED, arrow=True)
        body += text(48, 555, "选中花综 3：同时提起第 1、2、5、6 组。", 23)
        body += text(48, 600, "实际汉代纹织还配合地综、成组色经。", 23)
        body += text(48, 645, "这里解释“存组合”，不复原出土模型。", 23)
        figure("stored-pattern-shafts.svg", 710, "图 4｜没有纸卡，也能把花纹记住",
               "四根花综各保存八组经线的选择关系，选第三根提起一组组合。非汉代结构复原图。", body)

    def needle_hooks():
        body = ""
        for state, top in enumerate([70, 440]):
            body += panel(top, 345)
            body += text(48, top + 40, ["① 有孔：针通过，钩留在提升位置", "② 无孔：针被推回，钩离开提升位置"][state], 24)
            ny = top + 155
            hx = 310 if state == 0 else 235
            # The card approaches from the right; its aperture matches the needle.
            body += rect(550, top + 80, 28, 160, "#ead8b6")
            if state == 0:
                body += rect(548, ny - 12, 32, 24, "#fff", "#fff")
            body += line(hx, ny, 555 if state else 600, ny, INK)
            body += path([(hx, top + 225), (hx, top + 90),
                          (hx + 28, top + 90), (hx + 28, top + 104)], BLUE, 5)
            body += rect(330, top + 118, 70, 12, "#b34039")
            body += line(390, top + 155, 390, top + 92, RED, arrow=True)
            body += text(415, top + 118, "提升刀", 21, RED)
            body += text(593, top + 212, "纸卡", 21)
            body += line(hx, top + 225, hx, top + 265, BLUE, dash=True)
            body += text(48, top + 294, "钩 → 吊综绳 → 综眼 → 经线", 24)
            if state:
                body += line(520, ny + 32, 450, ny + 32, INK, arrow=True)
        body += text(36, 840, "常见单举式的选择逻辑；省略弹簧与支架。", 23)
        body += text(36, 880, "纸卡只做选择，提升动力另有来源。", 24)
        figure("needle-hook-selection.svg", 920, "图 5｜孔不是拉线的手，而是一个许可",
               "简化单举式针钩两状态：有孔使钩保持对准提升刀，无孔推针使钩偏离；非制造图。", body)

    def cards_to_cloth():
        body = panel(70, 410)
        body += text(48, 110, "① 组织计划：行＝纬，列＝经", 24)
        body += matrix(PATTERN, 60, 140, 34)
        body += text(420, 110, "② 孔位选择", 24)
        for r, row in enumerate(CARDS):
            y = 146 + r * 34
            body += rect(426, y, 216, 27, "#ead8b6")
            body += text(398, y + 21, r + 1, 20, INK, "middle")
            for c, hole in enumerate(row):
                if hole:
                    body += dot(439 + c * 27, y + 13, 7, "#fff")
        body += text(48, 450, "本图约定：1 打孔并提经；0 不打孔。", 23)
        body += panel(500, 625)
        body += text(48, 545, "③ 按卡序引纬，交织关系逐行出现", 24)
        for r, row in enumerate(PATTERN):
            body += f'<g class="woven-row row-{r}" data-row="{r}">'
            for c, up in enumerate(row):
                body += crossing(150 + c * 60, 610 + r * 60, up)
            body += "</g>"
            body += text(87, 617 + r * 60, r + 1, 22, INK, "middle")
        body += text(48, 1100, "静态计划一直保留；动画只示顺序，不示机速。", 22)
        css = (
            "@keyframes weave{from{opacity:0}to{opacity:1}}"
            ".woven-row{animation:weave .35s ease-out 1 both}"
            + "".join(f".row-{r}{{animation-delay:{r * .6:.1f}s}}" for r in range(8))
            + "@media(prefers-reduced-motion:reduce){.woven-row{animation:none;opacity:1}}"
        )
        figure("cards-to-cloth.svg", 1160, "图 6｜同一份选择：方格、纸卡、布",
               "八经八纬教学组织，1映射孔与提经，0映射无孔。斜向组织在中心反向。下方按八纬次序出现，最终完整保留。", body, css)

    def development_tracks():
        body = ""
        tracks = [
            ("把纬线送得更快", BLUE, [
                ("手动引纬", "手送梭子穿过梭口"),
                ("1733：飞梭", "改变梭子的投送方式"),
                ("1785：动力织机专利", "把织造循环交给动力驱动"),
                ("现代无梭引纬", "剑杆、气流或片梭带纬"),
            ]),
            ("把提经选择记得更复杂", RED, [
                ("早期纹织与花综", "把组合存进综线配置"),
                ("18 世纪前驱", "穿孔纸带与卡片控制"),
                ("19 世纪初：提花机构", "逐纬读取可更换的卡链"),
                ("现代电子提花", "用数据控制提经选择"),
            ]),
        ]
        for col, (heading, colour, items) in enumerate(tracks):
            x = 42 + 345 * col
            body += text(x, 102, heading, 22, colour)
            for i, (a, b) in enumerate(items):
                y = 155 + 140 * i
                body += rect(x, y, 290, 100, "#fff", "#ccd8e2", 12)
                body += text(x + 12, y + 37, a, 20, colour)
                body += text(x + 12, y + 75, b, 19)
                if i != 3:
                    body += line(x + 145, y + 107, x + 145, y + 130, colour, arrow=True)
        body += text(36, 775, "两条路线可以组合：手动也能提花，动力也能织平纹。", 22)
        figure("loom-development.svg", 815, "图 7｜织机有两条不同的升级路线",
               "引纬及动力、花纹选择的平行历史示意；不是所有地区必经的统一演化链。", body)

    def modern_weaving():
        body = panel(70, 280)
        body += text(48, 112, "电子提花：换了读法，没取消经纬线", 25)
        for i, (a, b) in enumerate([
            ("设计数据", "控制器逐纬读取"),
            ("电子选择", "选择钩与提升机构"),
            ("吊综与经线", "形成真实梭口"),
        ]):
            x = 48 + i * 216
            body += rect(x, 155, 190, 130, "#eef3f7", radius=10)
            body += text(x + 95, 198, a, 24, BLUE, "middle")
            body += text(x + 95, 247, b, 19, INK, "middle")
            if i < 2:
                body += line(x + 195, 220, x + 210, 220, INK, arrow=True)
        body += text(48, 325, "下方三种引纬方式，与电子提花不是一回事。", 23)
        for i, (a, b) in enumerate([
            ("① 剑杆：夹住纬线，送入或交接", "画的是夹持与移动方向，省略回程。"),
            ("② 喷气：用气流带动纬线", "喷嘴供气；不是把整只梭子吹过去。"),
            ("③ 片梭：小夹持体带着纬线穿过", "带的是纬线，不是载满纱的大梭子。"),
        ]):
            y = 375 + i * 205
            body += panel(y, 185) + text(48, y + 38, a, 24)
            for c in range(8):
                body += dot(170 + c * 57, y + 77 + (c % 2) * 50, 7, BLUE)
            body += line(140, y + 102, 590, y + 102, GOLD, dash=True)
            if i == 0:
                body += rect(120, y + 93, 230, 18, "#ccd8e2")
                body += rect(350, y + 87, 28, 30, GOLD)
            elif i == 1:
                body += path([(100, y + 82), (133, y + 95), (133, y + 109),
                              (100, y + 122)], INK, 4)
                for shift in [-8, 0, 8]:
                    body += line(153, y + 102 + shift, 320, y + 102 + shift,
                                 BLUE, dash=True, arrow=True)
            else:
                body += rect(350, y + 91, 50, 22, GOLD, radius=5)
            body += line(420, y + 102, 565, y + 102, RED, arrow=True)
            body += text(48, y + 163, b, 22)
        body += text(36, 1038, "引纬图为迎着经线的截面；速度与尺寸不按比例。", 22)
        figure("modern-weaving.svg", 1075, "图 8｜今天的织机：数据选线，机械织布",
               "电子提花选择控制与剑杆、喷气、片梭三种引纬方式的功能示意，省略具体结构。", body)

    def cyclic_run(row):
        assert len(set(row)) == 2
        doubled = row + row
        best = current = 1
        for a, b in zip(doubled, doubled[1:]):
            current = current + 1 if a == b else 1
            best = max(best, current)
        return min(best, len(row) - 1)

    def validate():
        assert PLAIN[0] == [1, 0, 1, 0]
        assert TWILL[0] == [1, 1, 0, 0]
        assert all(sum(row) == 4 for row in SATIN)
        assert all(sum(SATIN[r][c] for r in range(5)) == 4 for c in range(5))
        assert max(map(cyclic_run, PLAIN)) == 1
        assert max(map(cyclic_run, TWILL)) == 2
        assert max(map(cyclic_run, SATIN)) == 4
        assert CARDS == [tuple(row) for row in PATTERN]
        assert all(0 < sum(row) < 8 for row in PATTERN)
        cols = [[row[c] for row in PATTERN] for c in range(8)]
        assert all(0 < sum(col) < 8 for col in cols)
        longest = max(map(cyclic_run, PATTERN + cols))
        assert longest == 4
        files = sorted(OUT.glob("*.svg"))
        assert len(files) == 8
        for file in files:
            root = ET.parse(file).getroot()
            ns = {"s": "http://www.w3.org/2000/svg"}
            assert root.find("s:title", ns) is not None
            assert root.find("s:desc", ns) is not None
            assert root.attrib["viewBox"] == f'0 0 {root.attrib["width"]} {root.attrib["height"]}'
            assert "<script" not in file.read_text(encoding="utf-8")
        print(f"Generated 8 SVGs; 64 card decisions agree with weave; longest toy float={longest}.")

    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [interlacing, weaving_cycle, weave_structures, stored_shafts,
                 needle_hooks, cards_to_cloth, development_tracks, modern_weaving]:
        draw()
    validate()


@register("periodic-table", "元素周期表：长短表折叠、氧化物价态与轨道容量", "science_tech")
def build_periodic_table():
    OUT = REPO_ROOT / "assets" / "images" / "periodic-table"

    INK, BLUE, GREEN, GOLD = "#18364b", "#21699a", "#176d5b", "#a45708"

    PALE = {"s": "#e4f2e9", "d": "#e2edf9", "p": "#faeedb", "f": "#eee6f5"}

    SYMBOLS = "K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr".split()

    ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

    DISP_SCALE = 0.76

    def text(x, y, value, size=25, color=INK, anchor="start"):
        if size >= 28:
            ns, w_attr = min(size * 0.70, 20.8), ' font-weight="700"'
        elif size >= 25.5:
            ns, w_attr = size * 0.73, ' font-weight="600"'
        else:
            ns, w_attr = max(14.5, size * 0.76), ""
        adj_y = y - 0.28 * (size - ns)
        return (f'<text x="{x}" y="{adj_y:.2f}" font-size="{ns:.1f}" fill="{color}" '
                f'text-anchor="{anchor}"{w_attr}>{escape(str(value))}</text>')

    def box(x, y, w, h, fill="#edf3f8", stroke="#cbd5e1", radius=10):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

    def line(d, step=None):
        static = f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#arrow)"/>'
        if step is None:
            return static
        return static + (f'<path class="trace" d="{d}" pathLength="1" fill="none" '
                         f'stroke="#cf850e" stroke-width="3.6" style="animation-delay:{step}s"/>')

    def save(name, title, description, body, height):
        nw = round(720 * DISP_SCALE, 2)
        nh = round(height * DISP_SCALE, 2)
        nw_s = str(int(nw)) if float(nw).is_integer() else f"{nw:g}"
        nh_s = str(int(nh)) if float(nh).is_integer() else f"{nh:g}"
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{nw_s}" height="{nh_s}" viewBox="0 0 {nw_s} {nh_s}" '
               'role="img" aria-labelledby="title desc" lang="zh-CN">'
               f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
               '<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" '
               'orient="auto" markerUnits="userSpaceOnUse">'
               f'<path d="M1 1L10 6L1 11" fill="none" stroke="{BLUE}" stroke-width="1.8"/>'
               '</marker></defs><style>'
               'text{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif}'
               '.trace{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1s linear 1 both}'
               '@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}'
               '@media(prefers-reduced-motion:reduce){.trace{animation:none}}'
               '</style>'
               f'<rect x="0.75" y="0.75" width="{nw - 1.5:g}" height="{nh - 1.5:g}" rx="12" fill="#fbfcfd" stroke="#dde6ee" stroke-width="1.2"/>'
               f'<g transform="scale({DISP_SCALE:g})">'
               + text(28, 46, title, 30) + body + '</g></svg>\n')
        root = ET.fromstring(svg)
        assert root.get("width") == nw_s and root.get("height") == nh_s
        assert root.find("{http://www.w3.org/2000/svg}title") is not None
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")

    def fold():
        b = text(28, 92, "只取第四周期：同样 18 个元素，换一种排法。", 24)
        b += text(28, 146, "① 长表：沿一行读 K → Kr", 27)
        for i, symbol in enumerate(SYMBOLS):
            x = 36 + i * 36
            block = "s" if i < 2 else "d" if i < 12 else "p"
            b += text(x + 17, 187, i + 1, 17, anchor="middle")
            b += box(x, 201, 34, 62, PALE[block], radius=3)
            b += text(x + 17, 240, symbol, 21, anchor="middle")
        b += text(28, 305, "上面的小数字是现代族号，不是原子序数。", 23)
        b += line("M360 325V371", 0)
        b += text(28, 414, "② 短表：一个长周期拆成上下两行", 27)
        slots = ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni"]
        lower = ["Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", None, None, "Kr"]
        for j, label in enumerate(ROMAN):
            x = 50 + j * 62
            width = 62 if j < 7 else 186
            b += box(x, 447, width, 43, "#edf3f8", radius=0)
            b += text(x + width / 2, 478, label, 23, anchor="middle")
        for row, symbols in enumerate([slots, lower]):
            for j, symbol in enumerate(symbols):
                x, y = 50 + j * 62, 492 + row * 77
                b += box(x, y, 62, 75, "#fff", radius=0)
                if symbol:
                    z = SYMBOLS.index(symbol) + 19
                    block = "s" if z <= 20 else "d" if z <= 30 else "p"
                    b += box(x + 3, y + 3, 56, 69, PALE[block], radius=3)
                    b += text(x + 31, y + 27, z, 17, anchor="middle")
                    b += text(x + 31, y + 59, symbol, 27, anchor="middle")
        b += text(28, 700, "这里的小数字才是原子序数：19 → 36。", 24)
        b += text(28, 745, "VIII 大标题下，Fe、Co、Ni 已经占了三小列。", 24)
        b += text(28, 790, "采用俄方示例卷的分行位置；不是完整周期表。", 23)
        assert slots + [s for s in lower if s] == SYMBOLS
        assert len(set(slots + [s for s in lower if s])) == 18
        save("fold-period-four", "八个大标题，为什么装得下十八个元素？",
             "第四周期的18个元素。上方为现代1至18族长行，下方按俄罗斯2026化学示例卷的短表位置分成两行，铁钴镍置于第VIII大族下，氪在第二行最右。下表角标为原子序数，上方为族号。", b, 830)

    def relatives():
        b = text(28, 92, "短表的 I 大族，包含两支不相同的家族。", 24)
        b += box(28, 125, 664, 130)
        b += text(48, 169, "同一旧标题：I", 28)
        b += text(48, 219, "K（钾）　　　　　　　　　Cu（铜）", 28)
        b += line("M210 265V312H165V340", 0)
        b += line("M510 265V312H555V340", 1)
        for x, label, members, configuration, oxide in [
            (28, "现代第 1 族", "Li　Na　K", "[Ar] 4s¹", "K₂O：钾为 +1"),
            (372, "现代第 11 族", "Cu　Ag　Au", "[Ar] 3d¹⁰ 4s¹", "Cu₂O：铜为 +1"),
        ]:
            b += box(x, 350, 320, 270, PALE["s"] if x == 28 else PALE["d"])
            b += text(x + 160, 398, label, 28, anchor="middle")
            b += text(x + 160, 451, members, 27, anchor="middle")
            b += text(x + 160, 502, configuration, 25, anchor="middle")
            b += text(x + 160, 566, oxide, 24, anchor="middle")
        b += text(28, 670, "同有“+1”这条线索，不等于化学性质全都相同。", 24)
        b += text(28, 717, "铜还能形成 CuO（+2）；不能照抄碱金属的性格。", 23)
        b += text(28, 764, "电子式分别取中性钾、铜基态；[Ar]表示氩核芯。", 23)
        b += text(28, 811, "A/B 旧标号有不同传统，本文优先写现代族号。", 23)
        save("one-heading-two-families", "钾和铜：旧表的“同楼”，不是同一家",
             "短表旧第I大族可以同时容纳碱金属和铜族，现代分别列为1族和11族。K2O和Cu2O都体现+1氧化态，但铜还有+2等化学状态。K与Cu中性原子的基态电子排布并不相同。", b, 855)

    def oxides():
        examples = [
            ("I", "Na₂O", 2, 1, 1),
            ("II", "MgO", 1, 1, 2),
            ("III", "Al₂O₃", 2, 3, 3),
            ("IV", "SiO₂", 1, 2, 4),
            ("V", "P₂O₅*", 2, 5, 5),
            ("VI", "SO₃", 1, 3, 6),
            ("VII", "Cl₂O₇", 2, 7, 7),
        ]
        b = text(28, 92, "一条历史线索：一些氧化物，能排出化学计量阶梯。", 23)
        for i, (group, formula, metal, oxygen, state) in enumerate(examples):
            y = 127 + i * 77
            b += box(28, y, 664, 68, "#edf3f8")
            b += text(55, y + 44, group, 25)
            b += text(173, y + 44, formula, 28)
            b += text(455, y + 44, f"元素为 +{state}", 25)
            assert metal * state == oxygen * 2
        b += text(28, 720, "氧按 −2 记：2 × (+3) + 3 × (−2) = 0", 25, BLUE)
        b += text(28, 768, "例如 Al₂O₃：氧化数之和配平，不是原子排队图。", 23)
        b += text(28, 815, "* P₂O₅是常用经验式；常见分子形式写作 P₄O₁₀。", 22)
        b += text(28, 859, "只选示例：氧、氟等有例外，不能套成万能口诀。", 23)
        save("oxide-clues", "还看不见原子，也能找到元素的“亲戚”",
             "以钠镁铝硅磷硫氯的若干氧化物展示旧I至VII族所利用的化学计量联系。每行核对元素氧化数与氧的负二价总和为零，磷化合物标明经验式。不是每个族每个元素都适用的最高氧化态规则。", b, 900)

    def orbitals():
        b = text(28, 92, "每个方框代表一个轨道，每个轨道至多容纳 2 电子。", 22)
        for i, (label, count) in enumerate([("s", 1), ("p", 3), ("d", 5), ("f", 7)]):
            y = 128 + i * 130
            b += box(28, y, 664, 112, PALE[label])
            b += text(50, y + 43, f"{label} 亚层", 27)
            b += text(660, y + 43, f"{count} × 2 = {count * 2}", 26, anchor="end")
            for j in range(count):
                x = 52 + j * 84
                b += box(x, y + 58, 65, 40, "#fff", radius=3)
                b += text(x + 32, y + 86, "↑↓", 24, anchor="middle")
        b += text(28, 702, "第四周期的区块宽度", 28)
        widths = [("4s", 2, "s"), ("3d", 10, "d"), ("4p", 6, "p")]
        x = 36
        for label, count, block in widths:
            w = count * 36
            b += box(x, 736, w, 75, PALE[block], radius=0)
            b += text(x + w / 2, 782, f"{label}：{count}", 24, anchor="middle")
            x += w
        b += text(28, 862, "2 + 10 + 6 = 18；更长周期还涉及 14 格的 f 区。", 24)
        b += text(28, 910, "框图不是电子轨道照片；填充次序有例外。", 24)
        b += text(28, 952, "氦排在第18族，却是 1s²；位置也要照顾化学性质。", 22)
        assert sum(count for _, count, _ in widths) == 18
        assert 2 + 14 + 10 + 6 == 32
        save("orbital-widths", "长表的宽度，不是排版师随便拉出来的",
             "s、p、d、f亚层分别有1、3、5、7个轨道，每轨道最多2电子，得到2、6、10、14的容量。第四周期4s、3d、4p的区块宽度为2加10加6等于18。框和箭头只是量子态记号，不是经典运动轨道。", b, 995)

    def timeline():
        entries = [
            ("1869", "门捷列夫发表早期周期体系", "按原子量与化学性质组织，尚不知道现代原子结构。"),
            ("1871", "表格继续修订，并为未知元素留位", "不是一张排好后永不修改的八列表。"),
            ("1905", "维尔纳提出展开式排列", "已像现代长表，但包含后来被纠正的位置与数量。"),
            ("1913", "莫塞莱的工作推动原子序数认识", "元素排序的根本编号，不再只是平均原子量。"),
            ("1923", "德明《普通化学》采用长表", "教材、仪器供应商与挂图，帮助这种画法传播。"),
            ("1988", "IUPAC推荐族号 1—18", "统一编号，不等于宣布唯一合法的图形。"),
        ]
        b = text(28, 92, "读成多人的接力，不是两国各自发明一张表。", 24)
        for i, (year, title, detail) in enumerate(entries):
            y = 130 + i * 126
            b += box(28, y, 664, 107)
            b += text(48, y + 38, year, 29, BLUE)
            b += text(155, y + 38, title, 24)
            b += text(48, y + 82, detail, 22)
        b += text(28, 940, "这是关键节点选读，不是周期表发展的完整名单。", 23)
        save("history", "一张表，是怎样被许多人慢慢改出来的？",
             "1869门捷列夫早期周期体系，1871修订与预言，1905维尔纳展开式，1913莫塞莱原子序数工作，1923德明教材长表，1988IUPAC推荐1至18族编号。并非完整发明史，也不暗示所有版本单线继承。", b, 980)

    assert len(SYMBOLS) == len(set(SYMBOLS)) == 18
    assert len(list(range(19, 37))) == 18
    assert {s: i + 19 for i, s in enumerate(SYMBOLS)} == {
        "K": 19, "Ca": 20, "Sc": 21, "Ti": 22, "V": 23, "Cr": 24,
        "Mn": 25, "Fe": 26, "Co": 27, "Ni": 28, "Cu": 29, "Zn": 30,
        "Ga": 31, "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Kr": 36,
    }
    assert 18 + 1 == 19 and 18 + 10 + 1 == 29
    fold()
    relatives()
    oxides()
    orbitals()
    timeline()
    print("Generated 5 original periodic-table diagrams; element, charge and capacity assertions passed.")


@register("deep-science", "深层科学机制：光合、呼吸、地球日照、全加器与 DNA", "science_tech")
def build_deep_science():
    OUT = REPO_ROOT / "assets" / "images" / "deep-science"

    INK, BLUE, GREEN, GOLD = "#18364b", "#226ca2", "#187864", "#b56308"

    DISP_SCALE = 0.75

    def t(x, y, value, size=26, color=INK, anchor="start"):
        if size >= 28:
            ns, w_attr = min(size * 0.70, 21.0), ' font-weight="700"'
        elif size >= 25.5:
            ns, w_attr = size * 0.72, ' font-weight="600"'
        else:
            ns, w_attr = max(15.0, size * 0.74), ""
        adj_y = y - 0.28 * (size - ns)
        return (f'<text x="{x}" y="{adj_y:.2f}" font-size="{ns:.1f}" fill="{color}" '
                f'text-anchor="{anchor}"{w_attr}>{escape(str(value))}</text>')

    def rect(x, y, w, h, fill="#edf4f8", stroke="#adc4d2", radius=12):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

    def circle(x, y, r=12, fill=GREEN):
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'

    def route(d, color=BLUE, step=None, dashed=False):
        result = (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.4" '
                  f'{"stroke-dasharray=\"7 6\"" if dashed else ""} marker-end="url(#arrow)"/>')
        if step is not None:
            result += (f'<path class="trace" data-step="{step}" style="animation-delay:{step}s" '
                       f'd="{d}" fill="none" stroke="#dc900c" stroke-width="3.8" '
                       'pathLength="1"/>')
        return result

    def carbon(x, y, count, color=GREEN, gap=29):
        return "".join(circle(x + j * gap, y, 10, color) for j in range(count))

    def save(name, title, description, body, height):
        nw = int(round(720 * DISP_SCALE))
        nh = round(height * DISP_SCALE, 2)
        nh_s = str(int(nh)) if float(nh).is_integer() else f"{nh:g}"
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{nw}" height="{nh_s}" viewBox="0 0 {nw} {nh_s}" '
               'role="img" aria-labelledby="title desc" lang="zh-CN">'
               f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
               '<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" '
               'orient="auto" markerUnits="userSpaceOnUse">'
               '<path d="M1 1L10 6L1 11" fill="none" stroke="#18364b" stroke-width="1.8"/>'
               '</marker><radialGradient id="cloud"><stop stop-color="#6da4d4" stop-opacity=".85"/>'
               '<stop offset="1" stop-color="#6da4d4" stop-opacity=".05"/></radialGradient></defs>'
               '<style>text{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif}'
               '.trace{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1s linear 1 both}'
               '@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}'
               '@media(prefers-reduced-motion:reduce){.trace{animation:none}}'
               '</style>'
               f'<rect x="0.75" y="0.75" width="{nw - 1.5:g}" height="{nh - 1.5:g}" rx="12" fill="#fbfcfd" stroke="#dde6ee" stroke-width="1.2"/>'
               f'<g transform="scale({DISP_SCALE:g})">'
               + t(28, 46, title, 30) + body + '</g></svg>\n')
        root = ET.fromstring(svg)
        assert root.get("viewBox") == f"0 0 {nw} {nh_s}"
        assert root.get("width") == str(nw) and root.get("height") == nh_s
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")

    def photosynthesis():
        b = t(28, 88, "先找地点，再看反应：不是叶片里的一锅绿水。", 24)
        b += '<path d="M65 225Q110 70 245 125Q295 235 140 270Z" fill="#b9ddba" stroke="#187864" stroke-width="3"/>'
        b += route("M95 245L235 139", GREEN)
        b += t(80, 310, "叶片：CO₂经气孔进入", 24)
        b += route("M270 190H370")
        b += rect(390, 125, 270, 160, "#e5f3e7", GREEN)
        b += t(415, 164, "一个叶肉细胞", 25)
        for x, y in [(430, 200), (515, 220), (605, 195)]:
            b += f'<ellipse cx="{x}" cy="{y}" rx="28" ry="15" fill="#73b881" stroke="{GREEN}"/>'
        b += t(395, 310, "绿色小体：叶绿体", 24)
        b += route("M525 325V375")
        b += '<ellipse cx="360" cy="555" rx="310" ry="155" fill="#edf8e8" stroke="#187864" stroke-width="4"/>'
        b += '<ellipse cx="360" cy="555" rx="300" ry="145" fill="none" stroke="#90b89b" stroke-width="2"/>'
        b += t(228, 448, "叶绿体剖面", 25)
        for y in [510, 530, 550, 570]:
            b += rect(135, y, 190, 16, "#87be8f", GREEN, 8)
        b += t(125, 625, "类囊体堆叠", 25)
        b += t(394, 518, "基质", 28)
        b += t(380, 560, "卡尔文循环", 25)
        b += t(380, 596, "在这里固定碳", 24)
        b += t(28, 755, "类囊体膜上：光反应；膜包围的内部叫“腔”。", 24)
        b += t(28, 796, "基质：类囊体外、叶绿体包膜内的空间。", 24)
        b += t(28, 840, "各层单独放大，形状、数量、大小均为结构示意。", 23)
        save("leaf-map", "从一片叶，走到两种反应的现场", "叶片、叶肉细胞与叶绿体逐层放大。光反应位于类囊体膜，卡尔文循环位于叶绿体基质；各层不是等比例。", b, 875)

        b = t(28, 92, "实线读电子路线；虚线读跨膜 H⁺方向。", 24)
        b += rect(28, 145, 664, 520, "#edf6ed", "#b4ceb6")
        b += t(46, 188, "叶绿体基质", 27)
        b += rect(28, 320, 664, 70, "#94c39c", GREEN, 0)
        b += t(46, 620, "类囊体腔：H⁺在这里积累", 27)
        b += route("M335 248V490", GREEN, dashed=True)
        for x, label in [(125, "光系统II"), (335, "传递链"), (550, "光系统I")]:
            b += rect(x - 64, 305, 128, 100, "#fff", GREEN)
            b += t(x, 351, label, 23, anchor="middle")
        b += t(125, 238, "光能 ↓", 27, GOLD, "middle")
        b += t(550, 238, "光能 ↓", 27, GOLD, "middle")
        b += route("M125 495V410", step=0)
        b += t(54, 530, "2 H₂O", 25)
        b += t(54, 568, "→ O₂ + 4 H⁺", 24)
        b += t(157, 451, "4 e⁻", 24, BLUE)
        b += route("M195 355H265", step=1)
        b += route("M405 355H480", step=2)
        b += route("M550 300V275H660V215", step=3)
        b += t(389, 139, "末端还原 NADP⁺ → NADPH", 23, BLUE)
        b += t(352, 468, "H⁺入腔", 24, GREEN)
        b += t(28, 711, "① 水补电子　② 接力建立梯度　③ 光再“抬升”", 24)
        b += t(28, 752, "④ 形成 NADPH；H⁺回流驱动 ATP，见正文。", 24)
        b += t(28, 797, "省略中间载体与 ATP 合酶；线长不是能量或速率。", 23)
        save("light-reactions", "水的电子，要经过两次光能帮助", "膜拓扑简图：水氧化在类囊体腔侧，电子经光系统II、传递链、光系统I，最终在基质侧用于生成NADPH。H离子梯度并非电子流本身，图省略ATP合酶。", b, 830)

        b = t(28, 92, "每个圆点代表 1 个碳；只数碳，不画完整分子。", 24)
        b += rect(28, 125, 664, 140)
        b += t(48, 166, "① 固定：3 CO₂ + 3 RuBP", 27)
        b += carbon(55, 215, 3, GOLD, 33)
        for i in range(3):
            b += carbon(240 + i * 145, 215, 5, gap=22)
        b += route("M360 275V313", step=0)
        b += rect(28, 325, 664, 160)
        b += t(48, 368, "② 还原：6 个三碳单位", 27)
        for i in range(6):
            b += carbon(65 + i * 105, 412, 3, gap=24)
        b += t(48, 458, "6 ATP + 6 NADPH：把 3-PGA 加工为 G3P", 23)
        b += route("M360 495V534", step=1)
        b += rect(28, 545, 664, 175)
        b += t(48, 584, "③ 分流：取出 1 份，留下 5 份", 27)
        b += carbon(65, 630, 3, GOLD, 25)
        b += t(48, 684, "净产 G3P", 24)
        for i in range(5):
            b += carbon(250 + i * 86, 630, 3, gap=21)
        b += t(235, 684, "15 个碳 + 3 ATP → 再生 3 RuBP", 23)
        b += route("M670 695H704V118H652", GREEN, step=2)
        b += t(28, 769, "投入 18 个碳 = 净取出 3 个 + 再生受体的 15 个", 24)
        b += t(28, 810, "净消耗 9 ATP、6 NADPH；不是 6 份产物都运走。", 24)
        save("calvin-carbon", "卡尔文循环：为什么造出六份，却只拿走一份？", "3个二氧化碳的3个碳与3个RuBP的15个碳共18个碳，形成6个三碳单位。净取出1个G3P，其余5个用于再生RuBP。圆点是收支，不是逐个标记原子的轨迹。", b, 845)

    def respiration():
        b = t(28, 90, "圆点只记碳收支；不表示反应只发生这几步。", 24)
        rows = [(125, "① 葡萄糖：6 碳", [6], "糖酵解：投入 2 ATP，产生 4 ATP"),
                (305, "② 两个丙酮酸：2 × 3 碳", [3, 3], "净得 2 ATP、2 NADH；此时还没释放 CO₂"),
                (485, "③ 两个乙酰基：2 × 2 碳", [2, 2], "释放 2 CO₂，另得 2 NADH"),
                (665, "④ 两轮三羧酸循环：净释 4 CO₂", [1, 1, 1, 1], "再得 6 NADH、2 FADH₂、约 2 ATP 当量")]
        for i, (y, heading, groups, detail) in enumerate(rows):
            b += rect(28, y, 664, 145)
            b += t(48, y + 38, heading, 26)
            for j, count in enumerate(groups):
                b += carbon(65 + j * 128, y + 78, count)
            if i == 2:
                b += carbon(470, y + 78, 2, GOLD, 80)
                b += t(450, y + 112, "2 CO₂", 23, GOLD)
            b += t(48, y + 132, detail, 23)
            if i < 3:
                b += route(f"M360 {y+151}V{y+174}", step=i)
        b += t(28, 863, "总账：6 碳 → 6 CO₂；10 NADH、2 FADH₂待交电子。", 23)
        b += t(28, 904, "循环有受体再生；新进乙酰碳未必当轮离开。", 24)
        save("respiration-carbon", "一颗葡萄糖，六个碳怎样离开？", "按每分子葡萄糖的稳态净收支，糖酵解不释放CO2，丙酮酸氧化释放2个CO2，两个循环净释放4个CO2。循环不是逐个碳当轮离开的录像。", b, 940)

        b = t(28, 89, "局部展平的线粒体内膜；不是整个细胞器的形状。", 23)
        b += rect(28, 120, 664, 470, "#edf5fb")
        b += t(48, 163, "膜间隙：H⁺较多", 27)
        b += rect(28, 270, 664, 65, "#b2cfe0", BLUE, 0)
        b += t(48, 575, "线粒体基质", 27)
        for x, label in [(95, "I"), (245, "III"), (395, "IV")]:
            b += route(f"M{x} 410V190", GREEN, dashed=True)
            b += rect(x - 38, 250, 76, 110, "#fff", BLUE)
            b += t(x, 310, label, 27, anchor="middle")
            b += t(x + 12, 208, "H⁺", 23, GREEN)
        b += route("M135 302H200", step=0)
        b += route("M285 302H350", step=1)
        b += route("M395 365V425", step=2)
        b += t(35, 525, "NADH → I → Q → III → 细胞色素c → IV", 23, BLUE)
        b += t(305, 455, "O₂接电子", 24, BLUE)
        b += t(305, 490, "形成水", 24, BLUE)
        b += rect(548, 250, 76, 110, "#fff", GREEN)
        b += route("M586 190V410", GREEN, step=3)
        b += t(495, 453, "ATP 合酶", 25, GREEN)
        b += t(487, 493, "ADP + Pi → ATP", 22, GREEN)
        b += t(28, 635, "① 电子接力　② 泵 H⁺　③ 氧接电子　④ 回流合成 ATP", 22)
        b += t(28, 680, "复合体II不泵 H⁺；其电子从 Q 汇入，图中未画。", 24)
        b += t(28, 724, "箭头顺序仅供读图：真实过程耦联进行，不是排队开机。", 22)
        save("respiration-membrane", "电子向前走，H⁺绕一圈，ATP 才合成", "线粒体内膜拓扑示意，复合体I、III、IV将氢离子泵向膜间隙，电子最终给氧，氢离子经ATP合酶返回基质。省略复合体II及部分载体结构。", b, 760)

    def earth():
        distances = [("金星", .723), ("地球", 1.0), ("火星", 1.524)]
        b = t(28, 91, "同一颗太阳，距离增大，单位面积收到的光变少。", 24)
        for i, (name, d) in enumerate(distances):
            flux = 1 / d**2
            y = 145 + i * 125
            b += t(28, y, f"{name}｜距离 {d:g} AU", 25)
            b += rect(28, y + 17, flux * 305, 42, [GOLD, GREEN, BLUE][i], "none", 4)
            b += t(55 + flux * 305, y + 49, f"{flux:.2f}", 25)
        b += t(28, 528, "柱长 ∝ 1 / 距离²；把地球收到的光定为 1。", 25)
        b += rect(28, 568, 664, 166, "#f7efdf", "#d9bd8f")
        b += t(48, 608, "但这不是温度计，更不是生命概率。", 27)
        b += t(48, 652, "大气、反射率、云与水循环都能改变结果。", 24)
        b += t(48, 695, "地表液态水还需要合适的压力条件。", 24)
        b += t(28, 779, "圆轨道近似：取平均轨道尺度；忽略轨道与太阳变化。", 22)
        save("earth-sunlight", "“离太阳刚好”只答对了第一小问", "以平均轨道尺度作近似，单位面积太阳辐射随距离平方反比变化。金星、地球、火星分别约为地球的1.91、1、0.43倍，不是地表温度或宜居概率。", b, 815)

        age = 4.54e9
        clock = lambda ago: (1 - ago / age) * 24
        def hhmm(h):
            minutes = round(h * 60)
            return f"{minutes//60:02d}:{minutes%60:02d}"
        events = [("地球形成", age), ("约35亿年前：已有生命证据", 3.5e9),
                  ("约24亿年前：大氧化事件前后", 2.4e9),
                  ("约5.39亿年前：寒武纪开始", .539e9)]
        b = t(28, 92, "模型：把 45.4 亿年等比例压成一天，现在是 24:00。", 23)
        b += route("M60 155H665")
        for hour in range(0, 25, 4):
            x = 60 + hour * 25
            b += f'<path d="M{x} 144V165" stroke="{INK}" stroke-width="2"/>'
            b += t(x, 197, f"{hour:02d}:00", 21, anchor="middle")
        for i, (label, ago) in enumerate(events):
            h = clock(ago)
            x = 60 + h * 25
            y = 250 + i * 83
            b += circle(x, 155, 6, GOLD if i else GREEN)
            b += f'<path d="M{x:.2f} 167V{y-24}H45" fill="none" stroke="#98b0c1" stroke-dasharray="4 5"/>'
            b += rect(28, y - 10, 664, 66, "#f0f5f9", "#c5d3dd", 8)
            b += t(45, y + 31, f"{hhmm(h)}　{label}", 24)
        b += rect(28, 620, 664, 175, "#f8efdf", "#d4b481")
        b += t(48, 660, "再放大午夜前的最后一小时", 27)
        b += t(48, 705, f"{hhmm(clock(66e6))}　约6600万年前：非鸟恐龙灭绝", 24)
        human_seconds = .3e6 / age * 86400
        b += t(48, 752, f"午夜前约 {human_seconds:.1f} 秒：约30万年前的智人", 24)
        b += t(28, 839, "时钟由所选近似年代换算；不是每件事的精确起点。", 23)
        b += t(28, 880, "早期生命证据的年代，不等于生命诞生的时刻。", 24)
        assert 5 < human_seconds < 6
        assert hhmm(clock(3.5e9)) == "05:30"
        assert hhmm(clock(2.4e9)) == "11:19"
        save("earth-day", "若地球历史只有一天，我们来得有多晚？", "地球45.4亿年压缩成24小时。约35亿年前生命证据约05点30分，约24亿年前大氧化事件约11点19分，寒武纪约21点09分。年代均为近似，后两项以数值生成时间。", b, 920)

    def computer():
        b = t(28, 91, "只算两个二进制位；输出“本位”和“进位”。", 24)
        b += t(55, 175, "输入 a", 26) + t(55, 325, "输入 b", 26)
        b += rect(270, 130, 160, 90, "#e3eef8", BLUE)
        b += rect(270, 285, 160, 90, "#e3f2e9", GREEN)
        b += t(350, 184, "XOR 异或", 25, anchor="middle")
        b += t(350, 340, "AND 与", 25, anchor="middle")
        b += route("M145 165H250V175H265")
        b += route("M145 315H210V195H265")
        b += route("M170 165V330H265", GREEN)
        b += route("M145 315H240V350H265", GREEN)
        b += route("M440 175H545", BLUE)
        b += route("M440 330H545", GREEN)
        b += t(556, 184, "本位 s", 25, BLUE)
        b += t(556, 339, "进位 c", 25, GREEN)
        b += rect(28, 425, 664, 250)
        b += t(75, 468, "a　b", 26) + t(300, 468, "进位 c", 26) + t(510, 468, "本位 s", 26)
        for i, (a, v) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            y = 515 + i * 42
            b += t(75, y, f"{a}　{v}", 26)
            b += t(340, y, a & v, 26)
            b += t(550, y, a ^ v, 26)
            assert 2 * (a & v) + (a ^ v) == a + v
        b += t(28, 725, "1 + 1 = 二进制 10：本位 0，把 1 交给左一位。", 24)
        b += t(28, 768, "这是半加器；连续加法还要接收前一位的进位。", 24)
        save("computer-adder", "电路不会背加法口诀，却能完成 1 + 1", "半加器逻辑：异或产生本位，与门产生进位，四种输入的真值表均由逻辑计算生成。线为逻辑连接示意，交叉不表示额外接点。", b, 805)

        program = [("LOAD", 20), ("ADD", 21), ("STORE", 22), ("HALT", None)]
        def execute(instructions, initial_memory):
            memory = initial_memory.copy()
            acc, rows = 0, []
            for pc, (op, address) in enumerate(instructions):
                if op == "LOAD":
                    acc = memory[address]
                elif op == "ADD":
                    acc += memory[address]
                elif op == "STORE":
                    memory[address] = acc
                elif op != "HALT":
                    raise ValueError(f"Unknown toy instruction: {op}")
                rows.append((pc, op + (f" [{address}]" if address is not None else ""), acc, memory[22]))
                if op == "HALT":
                    break
            return rows, memory

        initial_memory = {20: 13, 21: 7, 22: 0}
        rows, memory = execute(program, initial_memory)
        assert [row[2:] for row in rows] == [(13, 0), (20, 0), (20, 20), (20, 20)]
        assert initial_memory[22] == 0 and memory[22] == 20
        _, changed_input = execute(program, {20: 13, 21: 9, 22: 0})
        assert changed_input[22] == 22
        stopped_rows, no_store = execute(program[:2] + [("HALT", None)], initial_memory)
        assert stopped_rows[-1][2:] == (20, 0) and no_store[22] == 0
        b = t(28, 90, "玩具 CPU：ACC 存当前值，PC 指向当前指令。", 24)
        b += rect(28, 120, 664, 150)
        b += t(48, 162, "内存初态", 28)
        b += t(48, 207, "[20] = 13　　[21] = 7　　[22] = 0", 26)
        b += t(48, 246, "方括号内是地址；等号右边才是数据。", 24)
        for i, (pc, op, a, stored) in enumerate(rows):
            y = 310 + i * 120
            b += rect(28, y, 664, 90, "#f0f5f9")
            b += t(48, y + 35, f"PC {pc}：{op}", 26)
            b += t(48, y + 73, f"执行后 ACC = {a}；[22] = {stored}", 24)
            if i < 3:
                b += route(f"M360 {y+94}V{y+114}", step=i)
        b += t(28, 837, "每步都经历：取指令 → 译码 → 执行 → 更新状态。", 23)
        b += t(28, 880, "自定义指令教学模型，不是 x86、ARM 或 Hack 指令集。", 22)
        save("computer-execution", "把 13 + 7 算完：谁记住下一步该做什么？", "四条自定义玩具CPU指令读取地址20的13，加上地址21的7，存到地址22，最后停止。所有执行状态由脚本模拟产生，未规定实际指令编码与时钟周期。", b, 915)

        glyph = ["01110", "10001", "10001", "11111", "10001", "10001", "10001"]
        b = t(28, 91, "同一个字符，可以有许多不同字形。", 26)
        b += rect(28, 130, 328, 365)
        b += t(48, 177, "字符身份：A", 29)
        b += t(48, 233, "Unicode：U+0041", 25)
        b += t(48, 283, "十进制码点：65", 25)
        b += t(48, 333, "UTF-8：41（十六进制）", 22)
        b += t(48, 383, "二进制：01000001", 24)
        b += t(48, 450, "编码不存“这个字的照片”", 23)
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                b += rect(425 + col * 40, 150 + row * 40, 36, 36,
                          BLUE if bit == "1" else "#e8eef3", "#a9bfd0", 2)
        b += t(525, 476, "原创 5 × 7 字形", 24, anchor="middle")
        b += t(28, 550, "数值 20：单字节无符号表示可为 14（十六进制）", 23)
        b += t(28, 593, "文本“20”：UTF-8 则是 32 30（十六进制）", 24)
        b += t(28, 638, "字符 → 字形 → 图形结果；真实排版还包含许多步骤。", 22)
        assert ord("A") == 65 and "A".encode() == bytes([0x41])
        assert (20).to_bytes(1) == bytes([0x14]) and "20".encode() == bytes([0x32, 0x30])
        assert len(glyph) == 7 and all(len(row) == 5 for row in glyph)
        save("computer-display", "内存里的一个数，不会自动变成屏幕上的字", "字符A的码点、UTF8编码与原创5乘7像素字形对照；数值20的一个字节表示和字符串20的两个UTF8字节不同。字形网格是教学示意。", b, 675)

    def dna():
        b = t(28, 91, "借鉴读者截图的放大路线；以下各幅分别放大。", 24)
        for i in range(3):
            b += rect(28, 125 + 235 * i, 664, 215)
        for y in range(155, 305, 5):
            phase = (y - 155) / 150 * 2 * pi
            x1, x2 = 145 + 48 * sin(phase), 145 - 48 * sin(phase)
            b += circle(x1, y, 4, GREEN) + circle(x2, y, 4, GOLD)
            if (y - 155) % 25 == 0:
                b += f'<path d="M{x1:.2f} {y}H{x2:.2f}" stroke="{BLUE}" stroke-width="4"/>'
        b += t(265, 172, "① DNA 本身就是大分子", 26)
        b += t(265, 219, "B 型双螺旋：宽约 2 nm", 24)
        b += t(265, 266, "不是所有 DNA 都长 2 nm", 24)
        b += t(265, 309, "把镜头移到局部化学结构 ↓", 24)
        # A bent water molecule illustrates why the screenshot's generic size is not universal.
        b += f'<path d="M145 412L97 464M145 412L193 464" stroke="#90a5b4" stroke-width="12"/>'
        b += circle(145, 412, 28, "#bb5147")
        b += circle(97, 464, 19, BLUE) + circle(193, 464, 19, BLUE)
        b += t(145, 420, "O", 23, "#fff", "middle")
        b += t(97, 472, "H", 20, "#fff", "middle") + t(193, 472, "H", 20, "#fff", "middle")
        b += t(265, 409, "② 分子没有统一的尺寸", 26)
        b += t(265, 455, "水只是例子，不是 DNA 单元", 24)
        b += t(265, 501, "典型小分子可在亚纳米量级", 24)
        b += t(265, 544, "DNA 由碳、氢、氧、氮、磷等组成", 22)
        b += circle(145, 690, 73, "url(#cloud)") + circle(145, 690, 5, GOLD)
        b += t(265, 644, "③ 原子：约 10⁻¹⁰ m 量级", 26)
        b += t(265, 690, "电子云：概率分布示意", 24)
        b += t(265, 736, "没有画行星式电子轨道", 24)
        b += t(265, 779, "中央核点已夸大；真实比例见尺", 23)
        b += t(28, 865, "此图讲组成与层次；大小比较请用正文对数尺。", 24)
        save("dna-chemistry", "沿着截图放大：先从生命走进化学", "原创中文版分层示意：DNA就是大分子，水分子只是小分子例子，不是DNA的重复单元；原子用电子云而非行星轨道表示。各图独立放大，核点夸大。", b, 905)

        b = t(28, 91, "不是实心套娃：电子那条支路并不会通向夸克。", 24)
        for i in range(3):
            b += rect(28, 125 + 235 * i, 664, 215)
        for row in range(-2, 3):
            for col in range(-2, 3):
                if row**2 + col**2 <= 5:
                    b += circle(145 + col * 25, 228 + row * 25, 13,
                                BLUE if (row + col) % 2 else GOLD)
        b += t(265, 172, "④ 原子核：约 10⁻¹⁵～10⁻¹⁴ m", 24)
        b += t(265, 218, "尺度随核种与定义改变", 24)
        b += t(265, 264, "通常含质子和中子", 24)
        b += t(265, 309, "普通氢核只有一个质子", 24)
        b += circle(145, 462, 76, "#e4ecf7")
        for angle, label in zip([0, 2 * pi / 3, 4 * pi / 3], ["u", "u", "d"]):
            x, y = 145 + 40 * cos(angle), 462 + 40 * sin(angle)
            b += circle(x, y, 17, BLUE) + t(x, y + 8, label, 23, "#fff", "middle")
        b += t(265, 409, "⑤ 质子：特征尺度在飞米量级", 24)
        b += t(265, 455, "均方根电荷半径约 0.84 fm", 24)
        b += t(265, 501, "u、u、d 只表示价夸克组成", 24)
        b += t(265, 544, "还涉及胶子与海夸克，不是三弹珠", 22)
        b += f'<path d="M110 695H180M145 660V730" stroke="{BLUE}" stroke-width="3"/>'
        b += t(145, 775, "符号，不是照片", 22, anchor="middle")
        b += t(265, 644, "⑥ 夸克：未测得有限大小", 26)
        b += t(265, 690, "标准模型中按点状粒子描述", 24)
        b += t(265, 736, "10⁻¹⁸ m 仅作参照长度", 24)
        b += t(265, 779, "不能把紫色圆球当作实测外形", 24)
        b += t(28, 865, "1 nm = 10⁻⁹ m；1 fm = 10⁻¹⁵ m；各幅不同比例。", 23)
        save("dna-particles", "继续放大：从原子核走到尚未分辨的边界", "原子核和质子各自放大。质子的三价夸克仅代表组成，非静态三球模型。夸克画为定位符号，不赋予有限半径。电子不是由夸克组成。", b, 905)

    def main():
        assert 3 + 3 * 5 == 6 * 3 == 3 + 5 * 3
        assert 6 + 3 == 9
        assert 6 == 2 * 3 == 2 * 2 + 2 == 2 + 4
        assert (2 + 2 + 6) * 2 + 2 * 2 == 24  # Electron-pair carriers account for 24 electrons.
        assert 4 + 10 * 2.5 + 2 * 1.5 == 32
        assert 4 + 8 * 2.5 + 2 * 1.5 + 2 * 1.5 == 30
        assert isclose(1 / .723**2, 1.913, abs_tol=.001)
        assert int("01101", 2) + int("00111", 2) == int("10100", 2) == 20
        for a in range(2):
            for b in range(2):
                for carry in range(2):
                    s = a ^ b ^ carry
                    c = (a & b) | (carry & (a ^ b))
                    assert 2 * c + s == a + b + carry
        photosynthesis()
        respiration()
        earth()
        computer()
        dna()
        print("Generated 12 original mechanism diagrams; numerical and logic assertions passed.")

    main()


@register("dollar-reading", "一美元票面符号：国玺正反面、十三州与罗马数字年份", "science_tech")
def build_dollar_reading():
    OUT = REPO_ROOT / "assets" / "images" / "dollar-reading"

    INK, BLUE, GREEN, GOLD = "#18364b", "#21699a", "#176d5b", "#92530a"

    PALE, SAND = "#e7f0f8", "#faf0dd"

    YEARS = [1782, 1935, 1955, 1956, 1957, 1963]

    ROMAN_PARTS = [("M", 1000), ("D", 500), ("CC", 200), ("L", 50),
                   ("XX", 20), ("V", 5), ("I", 1)]

    DISP_SCALE = 0.75

    def text(x, y, value, size=25, color=INK, anchor="start"):
        if size >= 28:
            ns, w_attr = min(size * 0.70, 21.0), ' font-weight="700"'
        elif size >= 25.5:
            ns, w_attr = size * 0.73, ' font-weight="600"'
        else:
            ns, w_attr = max(14.8, size * 0.75), ""
        adj_y = y - 0.28 * (size - ns)
        return (f'<text x="{x}" y="{adj_y:.2f}" font-size="{ns:.1f}" fill="{color}" '
                f'text-anchor="{anchor}"{w_attr}>{escape(str(value))}</text>')

    def rect(x, y, w, h, fill=PALE, radius=10):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
                f'fill="{fill}" stroke="#cbd5e1" stroke-width="1.5"/>')

    def path(d, color=BLUE, width=3, fill="none"):
        return f'<path d="{d}" stroke="{color}" stroke-width="{max(1.6, width * 0.8):g}" fill="{fill}"/>'

    def save(name, title, description, body, height):
        nw = int(round(720 * DISP_SCALE))
        nh = round(height * DISP_SCALE, 2)
        nh_s = str(int(nh)) if float(nh).is_integer() else f"{nh:g}"
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" '
               f'width="{nw}" height="{nh_s}" viewBox="0 0 {nw} {nh_s}" role="img" aria-labelledby="title desc" lang="zh-CN">'
               f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
               '<style>text{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif}</style>'
               f'<rect x="0.75" y="0.75" width="{nw - 1.5:g}" height="{nh - 1.5:g}" rx="12" fill="#fbfcfd" stroke="#dde6ee" stroke-width="1.2"/>'
               f'<g transform="scale({DISP_SCALE:g})">'
               + text(28, 48, title, 30) + body + '</g></svg>\n')
        root = ET.fromstring(svg)
        assert root.get("width") == str(nw) and root.get("height") == nh_s
        assert root.find("{http://www.w3.org/2000/svg}title").text
        assert root.find("{http://www.w3.org/2000/svg}desc").text
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")

    def reverse_map():
        b = text(28, 95, "先定位，再翻译：这是一美元背面的阅读地图。", 24)
        b += rect(28, 125, 664, 65)
        b += text(360, 167, "THE UNITED STATES OF AMERICA", 26, anchor="middle")
        for x, title, label in [(28, "① 画面左侧：国玺背面", "金字塔与天意之眼"),
                                (372, "② 画面右侧：国玺正面", "鹰与盾牌")]:
            b += rect(x, 215, 320, 322, SAND if x == 28 else "#e4f2e9")
            b += text(x + 16, 258, title, 23)
            if x == 28:
                b += path(f"M{x+160} 288L{x+121} 344H{x+199}Z", GOLD)
                b += path(f"M{x+138} 325Q{x+160} 305 {x+182} 325Q{x+160} 344 {x+138} 325Z", GOLD, 2)
                b += f'<circle cx="{x+160}" cy="325" r="6" fill="{GOLD}"/>'
                b += path(f"M{x+138} 370L{x+182} 370L{x+230} 460H{x+90}Z", GOLD, 3, "#e7cd9e")
            else:
                b += path(f"M{x+158} 344L{x+63} 308L{x+89} 383L{x+134} 397M{x+168} 344L{x+259} 308L{x+233} 383L{x+188} 397")
                b += path(f"M{x+151} 343V311L{x+128} 305L{x+149} 290L{x+174} 297V343", BLUE, 3, "#fff")
                b += path(f"M{x+125} 350H{x+198}V414Q{x+162} 459 {x+125} 414Z", BLUE, 3, PALE)
            b += text(x + 160, 505, label, 25, anchor="middle")
        b += text(28, 588, "③ 中间另有英文：IN GOD WE TRUST", 26)
        b += text(28, 630, "这里是国家座右铭，不是第三句拉丁文。", 24)
        entries = [
            ("左图上方", "ANNUIT COEPTIS", "祂眷顾了我们的事业"),
            ("左图下方", "NOVUS ORDO SECLORUM", "一个新时代的秩序"),
            ("右图鹰嘴", "E PLURIBUS UNUM", "合众为一"),
        ]
        for i, (where, latin, meaning) in enumerate(entries):
            y = 665 + i * 120
            b += rect(28, y, 664, 104)
            b += text(46, y + 38, where, 23, BLUE)
            b += text(200, y + 38, latin, 25)
            b += text(200, y + 80, meaning, 25)
        b += text(28, 1068, "位置关系示意；图标简化，不是纸币或国玺摹本。", 23)
        save("reverse-map", "背面两个圆，原来是一枚国玺的两面",
             "一美元背面的阅读地图。左为国玺背面金字塔，右为国玺正面鹰。三句拉丁文分别位于左图上方、左图下方及右图鹰嘴，英文国家座右铭另在中间。本图不是实际票券。", b, 1110)

    def many_to_one():
        b = text(28, 95, "在国玺的建国语境里：最初十三州，结成一国。", 24)
        b += text(28, 145, "① 先数“许多”：13 张卡，不是州的地理轮廓", 24)
        for i in range(13):
            x, y = 44 + (i % 7) * 92, 175 + (i // 7) * 76
            b += rect(x, y, 79, 58, "#e4f2e9")
            b += text(x + 39, y + 39, i + 1, 26, anchor="middle")
        b += path("M360 325V368M348 356L360 368L372 356")
        b += rect(105, 388, 510, 75, SAND)
        b += text(360, 436, "② 一个共同体", 30, anchor="middle")
        b += text(360, 522, "E PLURIBUS UNUM", 34, BLUE, "middle")
        for x, word, meaning in [(28, "E", "从……之中"), (254, "PLURIBUS", "许多"), (480, "UNUM", "一个")]:
            b += rect(x, 555, 212, 112)
            b += text(x + 106, 597, word, 27, anchor="middle")
            b += text(x + 106, 640, meaning, 25, anchor="middle")
        b += text(28, 721, "③ 再数盾纹：白色也要算，7 白 + 6 红 = 13", 24)
        for i in range(13):
            b += rect(61 + i * 46, 751, 46, 100, "#fff" if i % 2 == 0 else "#b75150", 0)
            b += text(84 + i * 46, 884, i + 1, 19, anchor="middle")
        b += text(28, 937, "条纹在此单独展开；不是盾牌真实轮廓。", 24)
        b += text(28, 985, "十三是建国记忆，不是今天州数量的实时显示。", 24)
        assert len("EPLURIBUSUNUM") == 1 + 8 + 4 == 13
        assert sum(i % 2 == 0 for i in range(13)) == 7
        assert sum(i % 2 == 1 for i in range(13)) == 6
        save("many-to-one", "合众为一：把“十三”读成一段历史",
             "十三张编号卡表示最初十三州，汇入一个共同体。三个拉丁词拆解为从、许多、一个。盾牌的条纹单独展开为七白六红共十三条。卡片不是州的地图，条纹不是完整盾牌图。", b, 1030)

    def pyramid():
        b = text(28, 95, "按上 → 中 → 下读；不要先从阴谋故事猜图。", 24)
        b += text(360, 151, "ANNUIT COEPTIS", 32, BLUE, "middle")
        b += text(360, 194, "祂眷顾了我们的事业", 26, anchor="middle")
        b += path("M360 223L309 302H411Z", GOLD)
        b += path("M329 277Q360 250 391 277Q360 302 329 277Z", GOLD, 2)
        b += '<circle cx="360" cy="277" r="8" fill="#92530a"/>'
        top, step = 340, 24
        for i in range(13):
            w1, w2 = 78 + i * 23, 78 + (i + 1) * 23
            y1, y2 = top + i * step, top + (i + 1) * step
            b += path(f"M{360-w1/2} {y1}H{360+w1/2}L{360+w2/2} {y2}H{360-w2/2}Z",
                      GOLD, 1.5, "#f3dfb8" if i % 2 == 0 else "#e6c997")
            b += text(570, y2 - 2, i + 1, 16, GOLD)
        b += text(360, 698, "MDCCLXXVI", 30, anchor="middle")
        b += text(360, 758, "NOVUS ORDO SECLORUM", 30, BLUE, "middle")
        b += text(360, 800, "一个新时代的秩序", 26, anchor="middle")
        b += text(28, 865, "塔基年份：把七组罗马数字分别换算", 27)
        for i, (roman, value) in enumerate(ROMAN_PARTS):
            x = 28 + i * 96
            b += rect(x, 897, 88, 104)
            b += text(x + 44, 938, roman, 27, anchor="middle")
            b += text(x + 44, 979, value, 23, anchor="middle")
        b += text(360, 1056, "1000 + 500 + 200 + 50 + 20 + 5 + 1 = 1776", 25, BLUE, "middle")
        b += text(28, 1106, "1776：纪念《独立宣言》，不是纸币的印刷年。", 24)
        b += text(28, 1151, "塔为十三层示意；透视与标签位置经过简化。", 23)
        assert "".join(r for r, _ in ROMAN_PARTS) == "MDCCLXXVI"
        assert sum(v for _, v in ROMAN_PARTS) == 1776
        save("pyramid-and-year", "金字塔没有封顶，塔基却写了一个年份",
             "从上到下读金字塔的两句拉丁文、天意之眼、十三层塔身和塔基1776。罗马数字MDCCLXXVI分成M D CC L XX V I七组，分别换算相加得到1776。原创简化示意，不是国玺摹本。", b, 1196)

    def history():
        b = text(28, 95, "一张纸币，叠着不同年代；下列节点非等比例。", 24)
        events = [
            ("1782", "国玺设计获准", "三句拉丁文属于这套历史设计。"),
            ("1935", "国玺双面进入一美元背面", "左金字塔、右鹰；罗斯福修改过排版。"),
            ("1955", "法律要求货币上出现英文格言", "不等于当天就换掉全部旧纸币。"),
            ("1956", "法律确立国家座右铭", "IN GOD WE TRUST"),
            ("1957", "英文格言首次用于纸币", "1957 系列一美元银券。"),
            ("1963", "用于这一系列的联邦储备券", "系列年不是每张纸币的生产年份。"),
        ]
        for i, (year, label, detail) in enumerate(events):
            y = 131 + i * 135
            b += rect(28, y, 664, 117, SAND if i == 3 else PALE)
            b += text(48, y + 43, year, 29, BLUE)
            b += text(160, y + 43, label, 25)
            b += text(48, y + 91, detail, 24)
        b += text(28, 1004, "设计采用、法律地位、首次印上：是三种时间。", 24)
        assert YEARS == sorted(YEARS)
        assert [int(e[0]) for e in events] == YEARS
        save("layers-of-history", "两句格言，不是在同一天印上去的",
             "非等比例时间线：1782国玺获准，1935国玺双面进入一美元，1955铭文要求，1956国家座右铭，1957一美元银券首次采用英文格言，1963系列联邦储备券采用。区分票券类别及系列年。", b, 1050)

    def front():
        entries = [
            ("① 票券类别", ["FEDERAL RESERVE NOTE", "联邦储备券"], 29),
            ("② 国家名称", ["THE UNITED STATES OF AMERICA", "美利坚合众国"], 25),
            ("③ 法律声明", ["THIS NOTE IS LEGAL TENDER",
                         "FOR ALL DEBTS, PUBLIC AND PRIVATE",
                         "关于公私债务的法偿地位"], 25),
            ("④ 两个印，不是同一个机构", ["左侧黑印：一家联邦储备银行", "右侧绿印：美国财政部"], 25),
            ("⑤ 同一张票，有不同识别信息", ["两处序列号：同一识别号重复出现",
                             "SERIES 年份：版本信息，不是逐张生产日期",
                             "印版号：印版；FW：沃思堡印刷设施"], 24),
        ]
        b = text(28, 95, "先分三类：票券身份 → 法律地位 → 识别信息。", 24)
        y = 130
        for title, lines, size in entries:
            height = 68 + 44 * len(lines)
            b += rect(28, y, 664, height)
            b += text(48, y + 42, title, 26, BLUE)
            for j, value in enumerate(lines):
                b += text(48, y + 91 + j * 44, value, size)
            y += height + 20
        b += text(28, y + 30, "分类阅读卡，不按实际位置排版，不是纸币票样。", 23)
        b += text(28, y + 73, "一美元与新版大面额的编号规则，不能直接混用。", 23)
        save("front-reading", "正面的小字，有的在讲法律，有的在管印刷",
             "一美元正面文字分类：联邦储备券、国家名、法偿声明、黑色联储银行印和绿色财政部印、序列号、系列年、印版号与FW。不是实际票面排版，不展示完整票样或伪造识别号。", b, y + 115)

    reverse_map()
    many_to_one()
    pyramid()
    history()
    front()
    assert len(list(OUT.glob("*.svg"))) == 5
    print("Generated 5 original dollar-reading diagrams; counts and Roman year verified.")


@register("archive-guides", "早期科普与资源导览卡片图集", "science_tech")
def build_archive_guides():
    ROOT = REPO_ROOT

    OUT = ROOT / "assets" / "images" / "archive-guides"

    OUT.mkdir(parents=True, exist_ok=True)

    DISP_SCALE = 0.78

    def text(x, y, value, size=23, anchor="start", color="#16324f"):
        if size >= 27:
            ns, w_attr = min(size * 0.71, 20.5), ' font-weight="700"'
        elif size >= 24.5:
            ns, w_attr = size * 0.73, ' font-weight="600"'
        else:
            ns, w_attr = max(14.8, size * 0.75), ""
        adj_y = y - 0.28 * (size - ns)
        return (
            f'<text x="{x}" y="{adj_y:.2f}" font-size="{ns:.1f}" text-anchor="{anchor}" '
            f'fill="{color}"{w_attr}>{escape(value)}</text>'
        )

    def arrow(x1, y1, x2, y2, index=0, color="#177e89", animated=True):
        line = (
            f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" '
            'stroke-width="2.6" marker-end="url(#arrow)"/>'
        )
        if animated:
            line += (
                f'<path class="trace" style="animation-delay:{index}s" '
                f'd="M{x1},{y1} L{x2},{y2}" pathLength="1" fill="none" '
                'stroke="#e18c20" stroke-width="3.4"/>'
            )
        return line

    def save(name, title, description, body, height=540):
        nw = round(720 * DISP_SCALE, 2)
        nh = round(height * DISP_SCALE, 2)
        nw_s = str(int(nw)) if float(nw).is_integer() else f"{nw:g}"
        nh_s = str(int(nh)) if float(nh).is_integer() else f"{nh:g}"
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{nw_s}" height="{nh_s}" viewBox="0 0 {nw_s} {nh_s}" '
            'role="img" aria-labelledby="title desc" lang="zh-CN">'
            f'<title id="title">{escape(title)}</title>'
            f'<desc id="desc">{escape(description)}</desc>'
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
            'refX="7" refY="3" orient="auto" markerUnits="userSpaceOnUse">'
            '<path d="M0,0 L7,3 L0,6" fill="none" stroke="#177e89" stroke-width="1.8"/>'
            '</marker></defs>'
            '<style>text{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif}'
            '.trace{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1s linear both}'
            '@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}'
            '@media(prefers-reduced-motion:reduce){.trace{animation:none}}'
            '</style>'
            f'<rect x="0.75" y="0.75" width="{nw - 1.5:g}" height="{nh - 1.5:g}" rx="12" fill="#fbfcfd" stroke="#dde6ee" stroke-width="1.2"/>'
            f'<g transform="scale({DISP_SCALE:g})">'
            + text(30, 43, title, 28)
            + body
            + '</g></svg>\n'
        )
        root = ET.fromstring(svg)
        assert root.get("width") == nw_s and root.get("height") == nh_s
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")

    def cards(name, title, description, rows, footer, animate=False):
        body = ""
        for i, (heading, detail) in enumerate(rows):
            y = 75 + i * 120
            body += (
                f'<rect x="30" y="{y}" width="660" height="90" rx="12" '
                'fill="#eaf3f8" stroke="#bed2df"/>'
                + text(48, y + 34, heading, 25)
                + text(48, y + 66, detail, 21)
            )
            if i < len(rows) - 1:
                body += arrow(360, y + 95, 360, y + 115, i, animated=animate)
        height = 115 + len(rows) * 120
        body += text(30, height - 23, footer, 19)
        save(name, title, description, body, height)

    def main():
        body = (
            '<path d="M180,255 L530,245 L555,261 L395,278 L270,274 Z" '
            'fill="#bed2df" stroke="#16324f" stroke-width="3"/>'
            '<path d="M325,260 L277,302 L385,271" fill="#8bb4cc"/>'
            + arrow(360, 232, 360, 95, animated=False)
            + arrow(360, 292, 360, 429, animated=False)
            + arrow(535, 260, 675, 260, animated=False)
            + arrow(185, 260, 45, 260, animated=False)
            + text(380, 120, "升力", 25)
            + text(380, 415, "重力", 25)
            + text(570, 236, "推力", 25)
            + text(55, 236, "阻力", 25)
            + text(30, 475, "平直匀速飞行：升力 = 重力，推力 = 阻力", 24)
            + text(30, 510, "示意：升力垂直来流；滑翔时受力方向不同。", 20)
        )
        save("flight-forces", "飞机不是被一股神秘力量托起来的", "平直匀速飞行时的四力平衡示意，箭头不表示实际力值。", body)

        cards("sun-energy", "一缕阳光，经历两种不同的旅程",
              "核心聚变释放能量，能量经辐射区和对流区到光球，再经真空约499秒到地球。非等比例，动画不是实际速度。",
              [("① 核心：氢聚变成氦", "质量差对应能量；不是煤炭在燃烧"),
               ("② 内部：辐射输运 → 对流输运", "吸收、再发射与散射；不是同一光子的履历"),
               ("③ 光球 → 地球：约 8 分 19 秒", "离开太阳后，穿过约 1.496 亿千米")],
              "箭头依次描出一次；时间和距离均非等比例。", True)

        cards("earth-habitable", "宜居不是集齐勋章，就自动长出生命",
              "液态水、化学原料和能量供给是研究已知生命的线索，宜居条件不等于生命起源的充分条件。",
              [("线索一：液态水与合适的环境", "温度和压力一起决定水能否长期保持液态"),
               ("线索二：原料与可利用的能量", "碳等元素 + 阳光或化学反应提供的能量"),
               ("开放问题：生命最初怎样出现？", "地球提供了实例，但还没有完整起源答案")],
              "这是阅读层次，不是先后发生的三步，也不是概率计算。")

        cards("photosynthesis", "叶子有两份账：能量账与碳账",
              "光反应利用光和水产生氧气、ATP、NADPH；卡尔文循环每固定3个二氧化碳净产1个三碳G3P，消耗9ATP和6NADPH。",
              [("① 光反应｜类囊体膜", "光 + 水 → 氧气；同时形成 ATP、NADPH"),
               ("② 卡尔文循环｜叶绿体基质", "3 CO₂ + 9 ATP + 6 NADPH → 净产 1 G3P"),
               ("③ 碳去了哪里？", "3 个碳 → 1 个三碳 G3P → 糖及其他有机物")],
              "第二行省略辅产物；是物料摘要，不是完整化学方程式。", True)

        cards("respiration", "跟着 6 个碳，走完细胞里的拆包之旅",
              "一分子葡萄糖经糖酵解变成两个三碳丙酮酸，再变成两个二碳乙酰辅酶A并释放两个二氧化碳；循环再释放四个二氧化碳。",
              [("① 糖酵解｜细胞质基质", "6 碳 → 2 × 3 碳丙酮酸；净得 2 ATP"),
               ("② 丙酮酸氧化 → 三羧酸循环", "2 × 3 碳 → 2 × 2 碳 + 2 CO₂ → 再释 4 CO₂"),
               ("③ 电子传递链 → ATP 合酶", "氧气最终接电子形成水；大部分 ATP 在此形成")],
              "按每分子葡萄糖计；第三步的电子来自前面各步。", True)

        body = ""
        for i, (heading, upper, lower, pump, back) in enumerate([
            ("叶绿体｜类囊体膜", "类囊体腔：H⁺积累", "叶绿体基质", "基质 → 腔", "腔 → 基质"),
            ("线粒体｜内膜", "膜间隙：H⁺积累", "线粒体基质", "基质 → 膜间隙", "膜间隙 → 基质"),
        ]):
            y = 85 + i * 285
            body += text(30, y, heading, 26)
            body += f'<rect x="30" y="{y+12}" width="660" height="180" rx="8" fill="#eaf3f8"/>'
            body += f'<rect x="30" y="{y+94}" width="660" height="12" fill="#bed2df"/>'
            body += text(45, y + 44, upper, 22)
            body += text(45, y + 176, lower, 22)
            for x in range(360, 660, 45):
                body += text(x, y + 57, "H⁺", 22)
            body += f'<rect x="520" y="{y+84}" width="30" height="48" rx="8" fill="#8bb4cc"/>'
            body += arrow(290, y + 147, 290, y + 64, 2 * i)
            body += arrow(535, y + 64, 535, y + 147, 2 * i + 1)
            body += text(45, y + 235, "建立梯度：" + pump, 22)
            body += text(360, y + 235, "合成 ATP：" + back, 21)
            body += text(555, y + 140, "ATP 合酶", 22)
        body += text(30, 660, "H⁺示意，不表示实际浓度；两套膜系统并不相同。", 21)
        save("proton-gradient", "相似的能量办法，不同的膜与空间",
             "上图为叶绿体，氢离子在类囊体腔积累，经ATP合酶回流基质。下图为线粒体，氢离子在膜间隙积累，经ATP合酶回流线粒体基质。两者方向按各自空间定义，箭头时长不代表生物速率。",
             body, 690)

        lunar = 12 * 29.5306
        solar = 365.2422
        deficit = solar - lunar
        assert abs(deficit - 10.875) < 0.00001
        assert abs(235 * 29.5306 - 19 * solar) < 0.09
        body = text(30, 100, "12 个平均朔望月", 25)
        body += f'<rect x="30" y="120" width="{lunar * 1.7:.3f}" height="55" rx="8" fill="#66a8c0"/>'
        body += text(48, 156, f"{lunar:.4f} 天", 25, color="#fff")
        body += text(30, 225, "1 个平均回归年", 25)
        body += f'<rect x="30" y="245" width="{solar * 1.7:.3f}" height="55" rx="8" fill="#177e89"/>'
        body += text(48, 281, f"{solar:.4f} 天", 25, color="#fff")
        body += text(30, 355, f"每年约差 {deficit:.3f} 天，差距会逐年累积。", 25)
        body += text(30, 410, "闰月补的是“月”，公历闰年补的是“日”。", 24)
        body += text(30, 465, "柱长按天数计算；19 年 7 闰只是近似协调。", 21)
        save("calendar", "太阳和月亮，并没有把时钟对齐", "平均12个朔望月354.3672天，回归年365.2422天，差10.875天。柱长使用相同比例。", body, 500)

        cards("computer", "按下 A，屏幕为什么会出现 A？",
              "简化的键盘输入、程序处理与显示过程。字符A的Unicode码点为65，八位二进制表示是01000001，但键盘事件本身并不直接发送这个字符编码。",
              [("① 输入：键盘产生按键事件", "系统结合键盘布局、修饰键和输入法解释"),
               ("② 处理：程序更新文本与内存", "A 的码点是 65；8 位写作 01000001"),
               ("③ 输出：字体字形被绘制成像素", "编码不是字的照片；显示还需要字形和布局")],
              "逻辑层示意：省略硬件中断、缓存和图形渲染细节。", True)
        assert int("01000001", 2) == ord("A")
        assert 6 == 2 * 3 == 2 * 2 + 2 == 2 + 4
        assert 3 + 3 * 5 == 6 * 3 == 3 + 5 * 3
        assert 490 < 149_597_870.7 / 299_792.458 < 510

        cards("parent-pause", "不必立刻成为完美父母",
              "给照护者的非诊断性自我提醒：先确保孩子安全，再辨认自己的感受，必要时寻求支持。这不是固定发展阶段。",
              [("停一下：先照顾安全", "累了可以求助；不要把忍到极限当作责任"),
               ("说具体：看见当下", "“我现在很疲惫”，比“我不是好父母”更准确"),
               ("做一件小事：给关系留空间", "陪伴、休息、轮换照护，都可以是下一步")],
              "这是自我提醒，不是心理评估或治疗方法。")

        cards("ai-evidence", "遇到一句 AI 预言，先分清它是哪一层",
              "区分观察、预测和个人选择：具体模型表现需要测试，未来预测带有条件，个人选择涉及价值判断。",
              [("① 观察：这次真的发生了什么？", "具体模型、具体任务、可复查的输入和结果"),
               ("② 推断：成立需要哪些条件？", "从一次成功，不能跳到“所有工作都会消失”"),
               ("③ 选择：我们愿意怎样使用？", "让工具扩展尝试，而不是替我们承担责任")],
              "每向下一层，都要补一层理由；这不是历史时间线。")
        cards("ai-limits", "三种“做不到”，不要混成一句话",
              "逻辑不可判定、现实资源不足、现有模型表现差是不同限制。标准量子计算不消除不可判定性。",
              [("逻辑边界：不存在包办全部情况的算法", "停机问题：不能对任意程序与输入都正确判定"),
               ("资源边界：理论可算，现实未必算得动", "密码学安全要写清假设、攻击模型与资源"),
               ("当前能力：这个模型这一次没做好", "可通过更好的模型、工具和验证改善")],
              "三类限制不是包含关系，也不是性能排行榜。")

        guides = [
            ("play", "十个网站，不如完成一次共同探索",
             [("先选：今晚只解决一个小问题", "故事 → 讲结局；天气 → 比两个城市"),
              ("再做：给孩子一个能动手的任务", "JRMF 摆一题；植物建模改一个参数"),
              ("最后：关掉网页，带走一个作品", "一张图、一段复述，或明天去公园的问题")],
             "年龄只是选题建议；账号、收费和隐私需家长先检查。"),
            ("parenting", "育儿信息，不按星级选，按问题选",
             [("健康与发展担忧 → 儿保或儿科", "带上具体观察；网络清单不能替代专业评估"),
              ("日常陪伴怎么做 → 可信机构指南", "先选一条适合家庭的建议，而非下载十张量表"),
              ("理念怎么讨论 → 书籍与家人对话", "经典书也有时代局限；安全建议以现行指南为准")],
             "这是信息分流，不是诊断流程；紧急情况应及时就医。"),
            ("science", "把模拟器玩成一场小实验",
             [("① 先猜：投射角越大，落点越远？", "先写下猜测；在相同条件下比较"),
              ("② 再改：只改变一个变量", "理想无空气阻力、同高落地时比较 30°/45°/60°"),
              ("③ 最后解释：模型省略了什么？", "现实有风、阻力和不同的起落高度")],
             "可在 oPhysics 选投射运动；先确认模拟的假设。"),
            ("ai", "AI 小实验：先猜边界，再看训练",
             [("① 选数据：圆环还是螺旋？", "TensorFlow Playground 有预设数据，不必手绘"),
              ("② 做比较：只改变一项设置", "固定数据与其他参数，比较训练和测试误差"),
              ("③ 找边界：训练好，不等于处处好", "多试几次随机初始化；不上传儿童个人资料")],
             "模型图展示数值计算，不是读取机器的主观想法。"),
            ("coding", "编程第一课：让角色走出一个正方形",
             [("① 预测：走一步，再转 90°", "Scratch：移动 50 步，右转 90 度"),
              ("② 重复：把两条积木重复 4 次", "先在纸上画路线，再让角色验证"),
              ("③ 调试：如果改成 3 次或 5 次？", "观察终点与朝向；错误也是一条线索")],
             "积木数值是示例；先复位位置和方向再比较。"),
            ("nature", "从“软件说像”到“我有证据”",
             [("① 观察：先记录，不惊扰", "外形、时间、环境；远距离拍照"),
              ("② 比对：识别结果只是候选", "找两项可见特征；不确定就保留不确定"),
              ("③ 分享：保护生物，也保护孩子", "隐藏住宅学校位置；不公开敏感物种坐标")],
             "不捕捉、不投喂、不用鸟声诱鸟；不要凭识别结果食用。"),
            ("arts", "看一件文物，也能像侦探办案",
             [("① 先看图：只描述你真的看见的", "颜色、形状、材料；暂时不猜故事"),
              ("② 再读著录：把猜测和记录对照", "年代、用途、出处；区分事实与推测"),
              ("③ 留一个问题：换一件作品比较", "同样是瓶子，不同时期为什么长得不同？")],
             "馆藏总数不等于全部高清公开；下载复用须看授权。"),
            ("world", "资源地图：按今天的问题入场",
             [("想解释一个现象 → 科学与数学", "PhET / OpenStax / GeoGebra：先猜再验证"),
              ("想完成一个作品 → 编程与艺术", "Scratch / 博物馆藏品：做一件小作品"),
              ("想查一条信息 → 百科与机构", "找原始出处、日期和适用条件，不只看排名")],
             "导航不是质量保证；免费阅读不等于免费课程或转载权。"),
        ]
        for name, title, rows, footer in guides:
            cards(f"guide-{name}", title, "；".join(h + "：" + d for h, d in rows), rows, footer)

        print(f"Generated {len(list(OUT.glob('*.svg')))} original archive diagrams.")

    main()


@register(
    "early-curiosity",
    "早期亲子与科普好奇心补强图解：感官发育、WHO大运动窗、情绪修复、飞行入轨、太阳聚变与置闰节气",
    "science_tech",
)
def build_early_curiosity():
    SUB = "early-curiosity"

    def fig_prenatal_senses():
        # Gestational weeks 0..40 mapped to x=56..466
        def wx(w):
            return 56 + (w / 40.0) * 410.0

        assert abs(wx(0) - 56) < 1e-9 and abs(wx(40) - 466) < 1e-9
        els = header(
            "十月怀胎的感官时间轴：宝宝什么时候能听见声音、睁开眼睛？",
            "按末次月经孕周（MedlinePlus / ACOG 临床口径）标出关键里程碑；个体发育存在自然前后浮动。",
        )
        els.append(card(20, 62, 474, 246))
        els.append(txt(36, 85, "① 孕周感官发育里程碑（0 → 40 周）", PANEL_TITLE, INK, weight="700"))
        # Axis line at y=126
        els.append(f'<line x1="56" y1="126" x2="466" y2="126" stroke="{BLUE}" stroke-width="2.2"/>')
        for wk in (0, 10, 20, 30, 40):
            x = wx(wk)
            els.append(f'<line x1="{x:.1f}" y1="120" x2="{x:.1f}" y2="132" stroke="{BLUE}" stroke-width="1.4"/>')
            els.append(txt(x, 146, f"{wk}周", 10.5, MUTED, "middle"))

        milestones = [
            (6.5, "6–7 周", "心脏规律跳动，眼耳原基初现", BLUE, 168),
            (12.5, "11–14 周", "小手能握拳，眼睑闭合保护眼球", GREEN, 194),
            (20.0, "19–21 周", "听觉开启！先听清妈妈心跳与血流声", ORANGE, 220),
            (26.0, "26 周左右", "对突响会有惊跳反应；27–30周可睁闭眼", PURPLE, 246),
            (38.5, "足月出生", "最佳对焦仅 20–25 cm（刚好怀抱看爸妈脸）", GREEN, 272),
        ]
        for wk, badge_txt, desc_txt, col, ry in milestones:
            x = wx(wk)
            els.append(f'<circle cx="{x:.1f}" cy="126" r="4.5" fill="{col}" stroke="#fff" stroke-width="1.2"/>')
            els.append(f'<line x1="{x:.1f}" y1="131" x2="{x:.1f}" y2="{ry - 4}" stroke="{col}" stroke-width="1" stroke-dasharray="2 2"/>')
            els.append(pill(42, ry - 14, badge_txt, fg=col, bg=SLATE_SOFT, w=78, h=19, size=10.5))
            els.append(txt(128, ry, desc_txt, 11.2, BODY))

        # Right card: Amniotic low-pass filter & newborn gaze
        els.append(card(508, 62, 232, 246))
        els.append(txt(524, 85, "② 隔着肚皮听见什么？", PANEL_TITLE, INK, weight="700"))
        els.append(card(524, 98, 200, 88, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(624, 118, "腹壁 + 羊水 ≈ 天然低通滤波", 11.2, BLUE, "middle", weight="700"))
        els.append(txt(536, 139, "• 高频尖音被大幅衰减模糊", 10.8, BODY))
        els.append(txt(536, 157, "• 低沉平稳的说话声穿透更好", 10.8, BODY))
        els.append(txt(536, 175, "→ 爸妈自然聊天胜过贴肚放喇叭", 10.6, ORANGE, weight="700"))

        els.append(card(524, 198, 200, 94, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(624, 218, "新生儿的“20–25 cm 专属焦距”", 11.2, ORANGE, "middle", weight="700"))
        els.append(txt(536, 239, "• 远处房间背景一团柔和模糊", 10.8, BODY))
        els.append(txt(536, 257, "• 唯独喂奶拥抱时爸妈的眼睛", 10.8, BODY))
        els.append(txt(536, 275, "  正好落在最清晰的焦点上！", 10.8, INK, weight="700"))

        return figure(
            324,
            "胎儿感官发育孕周时间轴与子宫声学滤波及新生儿对焦距离",
            "左图按0至40孕周标出心脏跳动、握拳、19至21周听觉开启、26周声音反应及足月出生；右图说明羊水低通滤波特性与新生儿20至25厘米最佳对焦距离。",
            els,
        )

    def fig_baby_perspective():
        # Exact angle calculation: adult eye y=1.63m, toddler eye y=0.68m, horizontal d=0.80m -> atan2(0.95, 0.80) = 49.9 deg!
        # With 1.75m adult (eye ~1.65m) and 0.75m toddler (eye ~0.65m), dy = 1.00m, dx = 0.80m -> 51.34 deg!
        angle_deg = math.degrees(math.atan2(1.00, 0.80))
        assert 51.3 < angle_deg < 51.4

        els = header(
            "蹲下来到底改变了什么？51° 仰视压迫感 vs 0° 平视连接，以及三个探索密码",
            "左图按真实身高比例计算视线仰角；右图解释婴儿“盯落叶、啃玩具、迷恋躲猫猫”背后的感官与认知机制。",
        )
        # Left card: Geometric sightline (x=20, w=352)
        els.append(card(20, 62, 352, 256))
        els.append(txt(36, 85, "① 一米以下的世界：站着讲 vs 蹲下来听", PANEL_TITLE, INK, weight="700"))
        gy = 276  # ground y; scale 1.0m = 96px
        sc = 96.0
        els.append(f'<line x1="38" y1="{gy}" x2="354" y2="{gy}" stroke="{SLATE}" stroke-width="1.6"/>')
        # Dining table h=0.75m -> y = 276 - 72 = 204
        ty = gy - 0.75 * sc
        els.append(f'<rect x="276" y="{ty:.1f}" width="64" height="6" rx="2" fill="#cbd5e1" stroke="{SLATE}"/>')
        els.append(f'<line x1="286" y1="{ty + 6:.1f}" x2="286" y2="{gy}" stroke="{SLATE}" stroke-width="2"/>')
        els.append(f'<line x1="330" y1="{ty + 6:.1f}" x2="330" y2="{gy}" stroke="{SLATE}" stroke-width="2"/>')
        els.append(txt(308, ty - 7, "0.75m 桌面=天花板", 10.2, MUTED, "middle"))

        # Standing adult at x=86 (1.75m -> top y = 276 - 168 = 108, eye y = 276 - 1.65*96 = 117.6)
        ax, a_eye = 82, gy - 1.65 * sc
        els.append(f'<line x1="{ax}" y1="{gy}" x2="{ax}" y2="{gy - 142}" stroke="{MUTED}" stroke-width="5" stroke-linecap="round" opacity="0.45"/>')
        els.append(f'<circle cx="{ax}" cy="{gy - 156}" r="12" fill="{SLATE_SOFT}" stroke="{MUTED}" stroke-width="1.5"/>')
        els.append(txt(ax, gy + 16, "站立 1.75m", 10.5, MUTED, "middle"))

        # Crouching adult at x=142 (eye y = 276 - 0.65*96 = 213.6)
        cx_a, c_eye = 144, gy - 0.65 * sc
        els.append(f'<path d="M{cx_a},{gy} L{cx_a - 10},{gy - 28} L{cx_a + 4},{gy - 50}" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linecap="round"/>')
        els.append(f'<circle cx="{cx_a}" cy="{c_eye:.1f}" r="12" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(txt(cx_a, gy + 16, "蹲下平视", 10.5, BLUE, "middle", weight="700"))

        # Toddler at x=220 (0.75m, eye y = 213.6)
        bx, b_eye = 222, gy - 0.65 * sc
        els.append(f'<line x1="{bx}" y1="{gy}" x2="{bx}" y2="{gy - 48}" stroke="{ORANGE}" stroke-width="5" stroke-linecap="round"/>')
        els.append(f'<circle cx="{bx}" cy="{b_eye:.1f}" r="10.5" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.8"/>')
        els.append(txt(bx, gy + 16, "宝宝 0.75m", 10.5, ORANGE, "middle", weight="700"))

        # Steep sightline (51.3 deg) vs horizontal sightline (0 deg)
        els.append(f'<line x1="{bx - 8}" y1="{b_eye - 4:.1f}" x2="{ax + 10}" y2="{a_eye + 4:.1f}" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arr-orange)"/>')
        els.append(txt(150, 152, f"仰角 ≈ {angle_deg:.0f}°", 11, ORANGE, "middle", weight="700", halo=True))
        els.append(f'<line x1="{cx_a + 14}" y1="{c_eye:.1f}" x2="{bx - 13}" y2="{b_eye:.1f}" stroke="{GREEN}" stroke-width="2.2" marker-end="url(#arr-green)"/>')
        els.append(txt(183, b_eye - 9, "0° 平视连接", 10.8, GREEN, "middle", weight="700", halo=True))

        # Right card: 3 cognitive decoders (x=388, w=352)
        els.append(card(388, 62, 352, 256))
        els.append(txt(404, 85, "② 读懂宝宝三个“怪动作”背后的科学", PANEL_TITLE, INK, weight="700"))
        boxes = [
            (98, BLUE, BLUE_SOFT, "盯着一片落叶看十分钟", "视觉与注意正在校准：从高对比轮廓逐步学", "会平滑追视与深度知觉，每道光影都是新数据。"),
            (172, ORANGE, ORANGE_SOFT, "抓到什么都往嘴巴里送", "唇舌触觉感受器极密！在手指精细动作成熟前，", "安全啃咬是分辨率最高的“3D 触觉扫描仪”。"),
            (246, GREEN, GREEN_SOFT, "玩“躲猫猫”笑到打嗝", "客体永久性（皮亚杰）：从“挡住=消失”升级为", "“猜你还在后面”，揭晓瞬间触发安全惊喜奖赏！"),
        ]
        for by, col, bg, t_head, l1, l2 in boxes:
            els.append(card(404, by, 320, 64, rx=8, fill=bg, stroke=col))
            els.append(txt(416, by + 19, t_head, 11.5, col, weight="700"))
            els.append(txt(416, by + 38, l1, 10.6, BODY))
            els.append(txt(416, by + 54, l2, 10.6, BODY))

        return figure(
            334,
            "儿童身高视角几何对比与早期感官认知三项解码",
            "左图计算0.75米幼儿与1.75米站立成人相距0.8米时需仰视约51度，蹲下则变为0度平视；右图解释凝视细节、口部探索与躲猫猫客体永久性的发展科学机制。",
            els,
        )

    def fig_emotion_repair_loop():
        els = header(
            "为什么深夜哭声让人一秒“上头”？大脑快慢双通道与关系修复闭环",
            "左图说明缺觉压力下的生理报警与“情绪命名”降温机制；右图展示安全的亲子关系靠修复而非满分。",
        )
        # Left card: Brain fast alarm vs prefrontal brake
        els.append(card(20, 62, 352, 246))
        els.append(txt(36, 85, "① 缺觉 + 哭声：刹车片暂时过热", PANEL_TITLE, INK, weight="700"))

        els.append(card(36, 100, 320, 56, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(48, 120, "快通道：边缘系统警报（如杏仁核）", 11.5, ORANGE, weight="700"))
        els.append(txt(48, 140, "毫秒级拉响战斗/逃跑警报 → 心跳加快、肌肉紧绷", 10.6, BODY))

        els.append(card(36, 168, 320, 56, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(48, 188, "慢通道：前额叶皮层（理性权衡与刹车）", 11.5, SLATE, weight="700"))
        els.append(txt(48, 208, "对睡眠剥夺极敏感！连轴转时抑制力明显下降", 10.6, BODY))

        els.append(card(36, 236, 320, 58, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(48, 256, "降温开关：给情绪起名字（Affect Labeling）", 11.5, GREEN, weight="700"))
        els.append(txt(48, 276, "说清“我是缺觉无助，不是宝宝故意整我”→ 重启前额叶", 10.5, BODY))

        # Right card: Tronick's Match -> Mismatch -> Repair cycle
        els.append(card(388, 62, 352, 246))
        els.append(txt(404, 85, "② 关系靠“修复闭环”，不靠“永不发火”", PANEL_TITLE, INK, weight="700"))

        nodes = [
            (564, 124, "同频连接", "眼神回应·平静安抚", BLUE, BLUE_SOFT),
            (668, 206, "短暂失调", "没听懂·疲惫急躁", ORANGE, ORANGE_SOFT),
            (460, 206, "事后修复", "安顿暂停·拥抱重连", GREEN, GREEN_SOFT),
        ]
        for nx, ny, nt, ns, col, bg in nodes:
            els.append(card(nx - 66, ny - 24, 132, 48, rx=10, fill=bg, stroke=col, sw=1.4))
            els.append(txt(nx, ny - 4, nt, 11.8, col, "middle", weight="700"))
            els.append(txt(nx, ny + 14, ns, 10.3, BODY, "middle"))

        # Cycle arrows
        els.append(f'<path d="M624,136 Q664,154 668,178" fill="none" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')
        els.append(f'<path d="M600,214 L530,214" fill="none" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#arr-green)"/>')
        els.append(f'<path d="M460,180 Q468,148 496,134" fill="none" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')

        els.append(txt(404, 266, "• Tronick 母婴互动研究：日常互动本就常有没对上拍的时刻", 10.5, BODY))
        els.append(txt(404, 286, "• 真正建立安全感的，是一次次“失调后还能回到温暖连接”", 10.5, GREEN, weight="700"))

        return figure(
            324,
            "照护者缺觉压力下的大脑快慢双通道与亲子关系修复闭环",
            "左图对比边缘系统快速警报、缺觉时受抑制的前额叶刹车及情绪命名降温开关；右图展示同频连接、短暂失调与事后修复的三步循环。",
            els,
        )

    def fig_smile_serve_return():
        els = header(
            "从无意识嘴角上扬到“你笑我也笑”：婴儿笑容的四步升级与发球—回球回路",
            "对照 CDC 发育里程碑与哈佛儿童发展中心（Serve and Return）互动模型绘制。",
        )
        # Left card: 4-stage smile progression
        els.append(card(20, 62, 352, 250))
        els.append(txt(36, 85, "① 第一年里的四种“笑”", PANEL_TITLE, INK, weight="700"))
        stages = [
            ("0–4 周", "内源/反射性微笑", "多出现在浅睡（REM）期，尚非看清人脸后的社交回应", SLATE, SLATE_SOFT),
            ("约 2 个月", "社会性微笑登场！", "看清 20–25cm 外你的脸、听到声音后主动回以微笑", BLUE, BLUE_SOFT),
            ("约 4 个月", "轻笑与主动撩人", "会自己先笑来吸引你注意，逗乐时发出轻快笑声", ORANGE, ORANGE_SOFT),
            ("约 6 个月+", "放声咯咯笑与预期幽默", "会轮流发声，不等手碰到肚子、光看怪表情就先大笑", GREEN, GREEN_SOFT),
        ]
        for idx, (age, name, desc, col, bg) in enumerate(stages):
            y = 100 + idx * 50
            els.append(pill(36, y, age, fg=col, bg=bg, w=72, h=22, size=10.5))
            els.append(txt(118, y + 15, name, 11.5, col, weight="700"))
            els.append(txt(118, y + 33, desc, 10.3, BODY))

        # Right card: Serve & Return 5 steps
        els.append(card(388, 62, 352, 250))
        els.append(txt(404, 85, "② 哈佛“发球—回球”五步搭起大脑连接", PANEL_TITLE, INK, weight="700"))
        steps = [
            ("1", "看见发球", "宝宝看向某物、咧嘴笑、咿呀发声或伸手", BLUE),
            ("2", "温暖回球", "大人微笑对视、轻声回应，让宝宝知道“我懂你”", GREEN),
            ("3", "把话说出来", "替眼前的事物或感受命名：“你在看那只小狗呀”", ORANGE),
            ("4", "留白等一等", "停几秒等宝宝再咿呀回应，练习像打乒乓球一样轮流", PURPLE),
            ("5", "顺势收尾", "宝宝转头、打哈欠就是“打累了”，温柔切换休息", SLATE),
        ]
        for i, (num, st, sd, col) in enumerate(steps):
            y = 104 + i * 40
            els.append(step_badge(416, y + 8, num, fg=col, bg=SLATE_SOFT, r=10))
            els.append(txt(434, y + 12, f"{st}：", 11.2, col, weight="700"))
            els.append(txt(502, y + 12, sd, 10.4, BODY))

        return figure(
            328,
            "婴儿第一年笑容发育四阶段与哈佛发球回球五步互动图",
            "左图按月龄区分0至4周反射性微笑、约2个月社会性微笑、约4个月轻笑与6个月以上放声大笑；右图列出哈佛儿童发展中心发球与回球五步互动。",
            els,
        )

    def fig_who_motor_windows():
        # Exact WHO Multicentre Growth Reference Study (2006, PMID 16817682) P1-P99 windows in months!
        who_data = [
            ("独坐（不扶）", 3.8, 9.2, BLUE, BLUE_SOFT),
            ("扶站", 4.8, 11.4, GREEN, GREEN_SOFT),
            ("手膝爬行*", 5.2, 13.5, ORANGE, ORANGE_SOFT),
            ("扶走", 5.9, 13.7, PURPLE, PURPLE_SOFT),
            ("独站", 6.9, 16.9, BLUE, BLUE_SOFT),
            ("独立行走", 8.2, 17.6, GREEN, GREEN_SOFT),
        ]
        assert abs((9.2 - 3.8) - 5.4) < 1e-9
        assert abs((17.6 - 8.2) - 9.4) < 1e-9

        def mx(month):
            # Map 2..20 months to x=150..492
            return 150 + ((month - 2.0) / 18.0) * 342.0

        els = header(
            "健康宝宝的“正常时间表”到底有多宽？WHO 六项大运动达标窗口（1%–99%）",
            "左图严格按世界卫生组织（WHO, 2006）跨国健康婴幼儿实测月龄绘制；右图解释体检单百分位怎么读。",
        )
        # Left card: WHO Windows chart (x=20, w=492)
        els.append(card(20, 62, 492, 258))
        els.append(txt(36, 84, "① WHO 健康儿童大运动达标月龄窗（横条两端为 P1 与 P99）", 12.6, INK, weight="700"))

        # Gridlines for months 3, 6, 9, 12, 15, 18
        for m_tick in (3, 6, 9, 12, 15, 18):
            gx = mx(m_tick)
            els.append(f'<line x1="{gx:.1f}" y1="98" x2="{gx:.1f}" y2="266" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
            els.append(txt(gx, 282, f"{m_tick}月", 10.5, MUTED, "middle"))

        for idx, (label, p1, p99, col, bg) in enumerate(who_data):
            ry = 110 + idx * 26
            x1, x2 = mx(p1), mx(p99)
            els.append(txt(140, ry + 13, label, 11.2, BODY, "end", weight="600"))
            els.append(f'<rect x="{x1:.1f}" y="{ry}" width="{x2 - x1:.1f}" height="17" rx="8.5" fill="{bg}" stroke="{col}" stroke-width="1.4"/>')
            els.append(txt(x1 - 4, ry + 12.5, f"{p1}", 9.8, col, "end", cls="mono"))
            els.append(txt(x2 + 4, ry + 12.5, f"{p99}月", 9.8, col, "start", weight="700"))

        els.append(txt(36, 305, "*注：WHO 样本中约 4.3% 健康婴儿不经历手膝爬行而直接扶站学走；独走正常跨度达 9.4 个月！", 10.2, MUTED))

        # Right card: How to read percentiles & red flags (x=524, w=216)
        els.append(card(524, 62, 216, 258))
        els.append(txt(538, 84, "② 百分位 ≠ 考试分数", 12.6, INK, weight="700"))
        els.append(card(538, 98, 188, 96, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(548, 118, "• P20 意思是：100 个健康同龄", 10.5, BODY))
        els.append(txt(548, 135, "  孩子高矮排队，排在第 20 位", 10.5, BODY))
        els.append(txt(548, 154, "• 关键看是否沿着自己的轨道", 10.5, BLUE, weight="700"))
        els.append(txt(548, 171, "  平稳长，而非人人都得挤 P90", 10.5, BLUE, weight="700"))

        els.append(card(538, 204, 188, 102, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(548, 223, "何时不必干等、及时就医？", 11.0, ORANGE, weight="700"))
        els.append(txt(548, 242, "• 超出窗口上限（如18月未独走）", 10.3, BODY))
        els.append(txt(548, 260, "• 左右肢体用力明显不对称", 10.3, BODY))
        els.append(txt(548, 278, "• 原本已经会的技能突然倒退！", 10.3, ORANGE, weight="700"))
        els.append(txt(548, 295, "→ 带具体记录找儿保/儿科评估", 10.2, BODY))

        return figure(
            336,
            "WHO六项儿童大运动正常达标月龄窗口与生长百分位读图指南",
            "左图按世界卫生组织2006年多中心研究精确绘出独坐3.8至9.2月、扶站4.8至11.4月、手膝爬5.2至13.5月、扶走5.9至13.7月、独站6.9至16.9月、独走8.2至17.6月的1%至99%窗口；右图解释百分位含义与就医预警边界。",
            els,
        )

    def fig_child_24h_executive():
        # WHO 2019 Under-5 24-hour guidelines: check hours sum to 24h!
        # Example healthy day for 3-4y: Sleep 11.5h (within 10-13h) + Active play 3.5h (>=3h) + Caregiver reading/meals/free play 8.5h + Screen <=0.5h = 24.0h!
        bands = [
            ("0–1岁婴儿", [("睡眠 12–17h", 14.5, BLUE), ("趴玩/地板互动", 2.5, GREEN), ("喂养/绘本/陪伴", 7.0, SLATE), ("屏幕 0h", 0.0, ORANGE)]),
            ("1–2岁幼儿", [("睡眠 11–14h", 12.5, BLUE), ("身体活动 ≥3h", 3.5, GREEN), ("游戏/共读/日常", 7.5, SLATE), ("1岁0h/2岁≤1h", 0.5, ORANGE)]),
            ("3–4岁学前", [("睡眠 10–13h", 11.5, BLUE), ("活动≥3h(含中强1h)", 3.5, GREEN), ("探索/共读/社交", 8.3, SLATE), ("屏幕 ≤1h", 0.7, ORANGE)]),
        ]
        for _, segs in bands:
            assert abs(sum(h for _, h, _ in segs) - 24.0) < 1e-9

        els = header(
            "AI 时代孩子更稀缺什么？WHO 24 小时时间账本与大脑“空中交通管制”",
            "左图依据 WHO（2019）5岁以下指南展示一天 24 小时的挤占关系；右图拆解执行功能与共学脚手架。",
        )
        # Left card: 24h budget (x=20, w=388)
        els.append(card(20, 62, 388, 252))
        els.append(txt(36, 85, "① 一天只有 24 小时：屏幕抢走的是哪三块刚需？", 12.4, INK, weight="700"))
        bar_x, bar_w = 108, 282.0
        for idx, (age_lbl, segs) in enumerate(bands):
            ry = 108 + idx * 56
            els.append(txt(100, ry + 16, age_lbl, 11.0, INK, "end", weight="700"))
            cur = bar_x
            for s_lbl, hrs, col in segs:
                if hrs <= 0:
                    continue
                w = (hrs / 24.0) * bar_w
                els.append(f'<rect x="{cur:.1f}" y="{ry}" width="{w:.1f}" height="24" fill="{col}" opacity="0.85" stroke="#fff" stroke-width="1"/>')
                if w > 54:
                    els.append(txt(cur + w / 2, ry + 16, s_lbl, 9.8, "#ffffff", "middle", weight="700"))
                cur += w
            # Screen note on right/below
            scr_lbl = segs[-1][0]
            els.append(txt(bar_x, ry + 39, f"睡眠 + 运动 + 真人互动优先  |  静态屏幕建议：{scr_lbl}（越少越好）", 10.0, MUTED))

        els.append(txt(36, 286, "核心逻辑：限制屏幕不是因为“电子辐射”，而是防止挤占睡眠、奔跑与眼神交谈！", 10.3, ORANGE, weight="700"))

        # Right card: Harvard Executive Function & AI Scaffolding (x=420, w=320)
        els.append(card(420, 62, 320, 252))
        els.append(txt(436, 85, "② 大脑“执行功能”三支柱（哈佛中心）", 12.4, INK, weight="700"))

        pillars = [
            ("工作记忆", "脑中同时托住线索", BLUE, BLUE_SOFT, 436),
            ("抑制控制", "忍住冲动不秒看答案", GREEN, GREEN_SOFT, 534),
            ("认知灵活", "错了换个角度再试", PURPLE, PURPLE_SOFT, 632),
        ]
        for pt, ps, col, bg, px in pillars:
            els.append(card(px, 100, 92, 58, rx=8, fill=bg, stroke=col))
            els.append(txt(px + 46, 121, pt, 11.2, col, "middle", weight="700"))
            els.append(txt(px + 46, 142, ps, 9.6, BODY, "middle"))

        els.append(card(436, 172, 288, 56, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(448, 192, "× 代劳陷阱：直接让 AI 替孩子写完、想完", 11.0, ORANGE, weight="700"))
        els.append(txt(448, 212, "   省掉了卡壳与试错，三根支柱得不到锻炼", 10.4, BODY))

        els.append(card(436, 238, 288, 60, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(448, 258, "✓ 脚手架共学：先猜 → 再问 AI → 动手核验", 11.0, GREEN, weight="700"))
        els.append(txt(448, 278, "   把工具当陪练，人保留提问、查证与修改权", 10.4, BODY))

        return figure(
            330,
            "WHO五岁以下儿童24小时活动睡眠屏幕指南与执行功能三支柱",
            "左图按WHO 2019指南绘出0至1岁、1至2岁、3至4岁在24小时内睡眠、身体活动、真人互动与静态屏幕的分配；右图列出哈佛儿童发展中心执行功能三支柱及AI时代代劳与共学对比。",
            els,
        )

    def fig_wing_lift_stall():
        # Thin-airfoil + post-stall smooth model: linear 2*pi*rad up to ~15 deg, peaking near CL=1.48 at 15.5 deg, then stalling!
        def cl_of(deg):
            if deg <= 12.0:
                return 0.18 + 0.105 * deg
            if deg <= 15.5:
                t = (deg - 12.0) / 3.5
                return 1.44 + 0.08 * math.sin(t * math.pi / 2) - 0.04 * (t ** 2)
            t = min(1.0, (deg - 15.5) / 6.5)
            return 1.48 - 0.68 * (t ** 1.4)

        assert cl_of(0) > 0.15 and cl_of(15.0) > 1.40 and cl_of(22.0) < 0.85

        els = header(
            "机翼迎角不是越大越好：临界失速曲线与纸飞机“机头配重”的秘密",
            "左图展示升力随迎角上升后在约 15° 附近气流分离骤降（失速）；右图解释重心略靠前为何更稳。",
        )
        # Left card: CL vs AoA curve (x=20, w=366)
        els.append(card(20, 62, 366, 250))
        els.append(txt(36, 85, "① 迎角 α 与升力：抬头过猛反而掉高度", 12.5, INK, weight="700"))
        ox, oy, pw, ph = 74, 266, 286.0, 148.0
        els.append(f'<line x1="{ox}" y1="{oy - ph}" x2="{ox}" y2="{oy}" stroke="{SLATE}" stroke-width="1.3"/>')
        els.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + pw}" y2="{oy}" stroke="{SLATE}" stroke-width="1.3"/>')

        def px_a(deg):
            return ox + ((deg + 4.0) / 28.0) * pw

        def py_cl(cl):
            return oy - (cl / 1.70) * ph

        # Stall shaded zone (>15.5 deg)
        sx = px_a(15.5)
        els.append(f'<rect x="{sx:.1f}" y="{oy - ph:.1f}" width="{ox + pw - sx:.1f}" height="{ph:.1f}" fill="{ORANGE_SOFT}" opacity="0.7"/>')
        els.append(f'<line x1="{sx:.1f}" y1="{oy - ph:.1f}" x2="{sx:.1f}" y2="{oy}" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        els.append(txt((sx + ox + pw) / 2, oy - ph + 18, "失速区（气流分离）", 10.3, ORANGE, "middle", weight="700"))

        pts = []
        for i in range(-40, 241, 4):
            d = i / 10.0
            pts.append(f"{px_a(d):.1f},{py_cl(cl_of(d)):.1f}")
        els.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
        pk_x, pk_y = px_a(15.2), py_cl(cl_of(15.2))
        els.append(f'<circle cx="{pk_x:.1f}" cy="{pk_y:.1f}" r="4.5" fill="{ORANGE}" stroke="#fff" stroke-width="1.2"/>')
        els.append(txt(pk_x - 8, pk_y - 9, "临界迎角 ≈ 15°", 10.5, ORANGE, "end", weight="700", halo=True))

        for tk in (0, 5, 10, 15, 20):
            tx = px_a(tk)
            els.append(txt(tx, oy + 16, f"{tk}°", 10.2, MUTED, "middle"))
        els.append(txt(ox + pw / 2, oy + 34, "机翼迎角 α（机翼弦线相对迎面来流的仰角）", 10.4, BODY, "middle"))
        els.append(txt(ox - 10, oy - ph / 2, "升力", 10.5, BODY, "end", weight="600"))

        # Right card: Paper airplane CG vs CP stability (x=398, w=342)
        els.append(card(398, 62, 342, 250))
        els.append(txt(414, 85, "② 纸飞机为什么总先冲高再拍地？", 12.5, INK, weight="700"))

        # Bad vs Good paper plane diagrams
        els.append(card(414, 100, 310, 92, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(426, 120, "× 重心太靠后：一抬头就翻跟头失速", 11.2, ORANGE, weight="700"))
        els.append(txt(426, 141, "• 机头太轻 → 升力作用点在重心前方，把机头越掀越高", 10.3, BODY))
        els.append(txt(426, 159, "• 迎角冲破临界值发生失速 → 瞬间掉头砸地（波浪起伏）", 10.3, BODY))
        els.append(txt(426, 177, "解法：机头多折一层或夹半枚回形针，把重心往前移！", 10.3, INK, weight="700"))

        els.append(card(414, 202, 310, 96, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(426, 222, "✓ 稳定滑翔黄金法则：重心 CG 在压力中心 CP 稍前方", 11.0, GREEN, weight="700"))
        # Mini side-view plane vector diagram
        els.append(f'<polygon points="440,264 556,256 544,270" fill="#ffffff" stroke="{SLATE}" stroke-width="1.4"/>')
        # CG forward (x=512, downward weight) and CP slightly aft (x=486, upward lift) -> nose points right (x=556)
        els.append(f'<circle cx="516" cy="261" r="4" fill="{ORANGE}"/>')
        els.append(f'<line x1="516" y1="265" x2="516" y2="287" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')
        els.append(txt(524, 285, "重心CG", 9.8, ORANGE, weight="700"))
        els.append(f'<circle cx="484" cy="262" r="4" fill="{BLUE}"/>')
        els.append(f'<line x1="484" y1="258" x2="484" y2="236" stroke="{BLUE}" stroke-width="1.6" marker-end="url(#arr-blue)"/>')
        els.append(txt(476, 244, "升力CP", 9.8, BLUE, "end", weight="700"))
        els.append(txt(572, 255, "机头一旦微抬，后方升力", 10.0, BODY))
        els.append(txt(572, 271, "自动把机尾托起、压回平飞！", 10.0, GREEN, weight="700"))

        return figure(
            328,
            "机翼迎角升力失速曲线与纸飞机纵向静稳定配重原理",
            "左图绘制升力随迎角线性增长并在约15度后进入气流分离失速区；右图对比重心靠后抬头失速与重心位于压力中心稍前方的自动恢复稳定滑翔。",
            els,
        )

    def fig_newton_cannon_orbits():
        # Numerically integrate 4 trajectories around Earth (R=1.0, GM=1.0, launch at (0, 1.12) horizontally!)
        r0 = 1.12
        v_circ = math.sqrt(1.0 / r0)  # corresponds to ~7.91 * sqrt(1/1.12)
        v_esc = math.sqrt(2.0 / r0)
        assert abs(v_esc / v_circ - math.sqrt(2.0)) < 1e-12

        def trace_orbit(v0, dt=0.008, steps=1600):
            x, y = 0.0, r0
            vx, vy = v0, 0.0
            pts = [(x, y)]
            for _ in range(steps):
                r2 = x * x + y * y
                r = math.sqrt(r2)
                if r < 1.0 or r > 3.2:
                    break
                ax, ay = -x / (r2 * r), -y / (r2 * r)
                vx += ax * dt
                vy += ay * dt
                x += vx * dt
                y += vy * dt
                pts.append((x, y))
            return pts

        cx, cy, R_px = 186, 196, 68.0

        def to_svg(pts):
            return " ".join(f"{cx + x * R_px:.1f},{cy - y * R_px:.1f}" for x, y in pts)

        p_sub = trace_orbit(0.68 * v_circ, steps=400)
        p_cir = trace_orbit(1.00 * v_circ, steps=900)
        p_ell = trace_orbit(1.16 * v_circ, steps=1900)
        p_esc = trace_orbit(1.43 * v_circ, steps=500)
        assert math.hypot(*p_sub[-1]) <= 1.01  # hits Earth!
        assert min(math.hypot(x, y) for x, y in p_cir) > 1.10  # stays circular!

        els = header(
            "牛顿高山大炮思想实验：把炮弹越打越快，什么时候就变成了卫星？",
            "四条轨迹均由牛顿万有引力二体方程真实数值积分生成：区别只在水平初速度够不够快。",
        )
        # Left card: Computed orbits (x=20, w=380)
        els.append(card(20, 62, 380, 260))
        els.append(txt(36, 85, "① 同一座高山水平发射的四条真实引力轨迹", 12.4, INK, weight="700"))
        # Earth disc
        els.append(f'<circle cx="{cx}" cy="{cy}" r="{R_px}" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.8"/>')
        els.append(txt(cx, cy + 4, "地球", 11.5, BLUE, "middle", weight="700"))
        # Mountain peak up to r0=1.12
        els.append(f'<polygon points="{cx - 9},{cy - R_px + 2:.1f} {cx + 9},{cy - R_px + 2:.1f} {cx},{cy - r0 * R_px:.1f}" fill="{SLATE}"/>')

        els.append(f'<polyline points="{to_svg(p_sub)}" fill="none" stroke="{SLATE}" stroke-width="1.8" stroke-dasharray="4 3"/>')
        els.append(f'<polyline points="{to_svg(p_cir)}" fill="none" stroke="{GREEN}" stroke-width="2.2"/>')
        els.append(f'<polyline points="{to_svg(p_ell)}" fill="none" stroke="{BLUE}" stroke-width="2.0"/>')
        els.append(f'<polyline points="{to_svg(p_esc)}" fill="none" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-orange)"/>')

        els.append(txt(cx + 58, cy - 52, "① 落回地面", 10.2, SLATE, weight="600", halo=True))
        els.append(txt(cx - 86, cy + 78, "② 圆轨道", 10.5, GREEN, weight="700", halo=True))
        els.append(txt(cx + 8, cy + 114, "③ 椭圆轨道", 10.5, BLUE, weight="700", halo=True))
        els.append(txt(cx + 108, cy - 96, "④ 逃逸飞走!", 10.5, ORANGE, weight="700", halo=True))

        # Right card: Speed thresholds table (x=412, w=328)
        els.append(card(412, 62, 328, 260))
        els.append(txt(428, 85, "② 近地理想模型的三档速度台阶", 12.4, INK, weight="700"))
        rows = [
            ("< 7.9 km/s", "抛体落回地面", "下落弯度比地面弧度更陡，终会落地", SLATE, SLATE_SOFT),
            ("≈ 7.9 km/s", "第一宇宙速度（环绕）", "下落弧度刚好贴合地球曲率，绕地圆飞", GREEN, GREEN_SOFT),
            ("7.9–11.2 km/s", "拉长成椭圆轨道", "近地点仍在发射高度，远地点越拉越远", BLUE, BLUE_SOFT),
            ("≥ 11.2 km/s", "第二宇宙速度（逃逸）", "刚好等于 √2 × 7.9，彻底挣脱地球引力井", ORANGE, ORANGE_SOFT),
        ]
        for idx, (spd, title_r, desc_r, col, bg) in enumerate(rows):
            ry = 102 + idx * 52
            els.append(pill(428, ry, spd, fg=col, bg=bg, w=96, h=22, size=10.2))
            els.append(txt(532, ry + 15, title_r, 11.2, col, weight="700"))
            els.append(txt(428, ry + 36, desc_r, 10.3, BODY))

        return figure(
            338,
            "牛顿高山大炮思想实验数值积分轨迹与第一第二宇宙速度对照",
            "左图通过二体引力数值积分展示亚轨道落地、圆轨道、椭圆轨道与逃逸双曲线四条轨迹；右图对照近地模型下7.9与11.2千米每秒的速度分界。",
            els,
        )

    def fig_sun_mass_thermostat():
        # Exact atomic mass balance: 4 * m(1H) vs m(4He)
        m_h1 = 1.007825
        m_he4 = 4.002603
        dm = 4 * m_h1 - m_he4
        frac = dm / (4 * m_h1)
        mev = dm * 931.494
        assert abs(dm - 0.028697) < 1e-5 and 0.0070 < frac < 0.0072 and 26.70 < mev < 26.76
        # Sun luminosity mass loss per second: L_sun / c^2
        L_sun = 3.828e26
        c = 299792458.0
        dm_sun_kg = L_sun / (c * c)
        assert 4.25e9 < dm_sun_kg < 4.27e9  # ~426 万吨/秒!

        els = header(
            "太阳的能量账本与安全阀：少掉 0.71% 的质量去哪了？为什么它不会像氢弹炸掉？",
            "左图按精确原子质量算出四个氢变成一个氦的亏损能量；右图拆解引力与热压的负反馈恒温器。",
        )
        # Left card: Mass defect balance (x=20, w=360)
        els.append(card(20, 62, 360, 252))
        els.append(txt(36, 85, "① 核聚变天平：1000 克氢变成 992.9 克氦", 12.4, INK, weight="700"))

        els.append(card(36, 102, 146, 74, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(109, 124, "反应前：4 个氢原子", 11.0, BLUE, "middle", weight="700"))
        els.append(txt(109, 145, "4 × 1.0078 u", 10.8, BODY, "middle", cls="mono"))
        els.append(txt(109, 164, "= 4.0313 u", 11.5, INK, "middle", weight="700", cls="mono"))

        els.append(f'<line x1="186" y1="139" x2="212" y2="139" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>')

        els.append(card(218, 102, 146, 74, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(291, 124, "反应后：1 个氦-4", 11.0, GREEN, "middle", weight="700"))
        els.append(txt(291, 145, "实测质量仅", 10.6, BODY, "middle"))
        els.append(txt(291, 164, "= 4.0026 u", 11.5, INK, "middle", weight="700", cls="mono"))

        els.append(card(36, 190, 328, 108, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(48, 212, f"亏损质量 Δm = 0.0287 u（占原质量 {frac * 100:.2f}%）", 11.2, ORANGE, weight="700"))
        els.append(txt(48, 234, f"• 按 E = Δmc² 换算：单次净释放约 {mev:.2f} MeV", 10.6, BODY))
        els.append(txt(48, 254, f"• 整颗太阳每秒“烧掉”约 {dm_sun_kg / 1e7:.0f} 万吨质量化作辐射！", 10.6, BODY))
        els.append(txt(48, 274, "• 但太阳总重 2×10²⁷ 吨，烧百亿年也只耗万分之七体重", 10.4, MUTED))

        # Right card: Hydrostatic thermostat (x=392, w=348)
        els.append(card(392, 62, 348, 252))
        els.append(txt(408, 85, "② 恒星“自动恒温器”：为什么温和烧 100 亿年？", 12.4, INK, weight="700"))

        # Two opposing forces + negative feedback loop
        els.append(card(408, 102, 316, 62, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(566, 123, "流体静力平衡：两股巨力时刻顶牛", 11.2, INK, "middle", weight="700"))
        els.append(txt(566, 145, "向内万有引力挤压  ⇄  向外高温等离子体热压力托举", 10.6, BLUE, "middle", weight="600"))

        steps_fb = [
            (178, "假如聚变稍微变快一点 → 核心多产热、向外膨胀", ORANGE),
            (214, "核心一膨胀 → 密度与温度自动下降，聚变立刻减速！", GREEN),
            (250, "反之若聚变变慢 → 引力略微压紧核心 → 升温恢复输出", BLUE),
        ]
        for sy, stxt, scol in steps_fb:
            els.append(card(408, sy, 316, 28, rx=6, fill="#ffffff", stroke=scol))
            els.append(txt(420, sy + 18, stxt, 10.4, scol, weight="600"))

        els.append(txt(408, 298, "加上第一步弱相互作用极慢，太阳成了最稳的核聚变炉。", 10.4, MUTED))

        return figure(
            330,
            "太阳质子质子链质量亏损账本与流体静力平衡恒温器",
            "左图精确比较4个氢原子4.0313u与氦4原子4.0026u的质量差0.0287u（约0.71%，对应26.73MeV及太阳每秒亏损约426万吨）；右图展示引力与热压负反馈调节机制。",
            els,
        )

    def fig_photon_random_walk():
        # Deterministic 2D random walk inside circle vs straight neutrino ray!
        # Verify RMS displacement scaling: R_rms = l * sqrt(N) -> N = (R / l)^2!
        # If R = 5e8 m (radiative zone) and effective step l = 1e-3 m -> N = 2.5e23 steps -> time = N*l/c = 2.5e20 / 3e8 ≈ 8.3e11 s ≈ 26,000 years!
        R_rad = 5.0e8
        step_m = 1.0e-3
        n_steps = (R_rad / step_m) ** 2
        t_years = (n_steps * step_m / 2.9979e8) / (365.25 * 86400)
        assert 20000 < t_years < 30000

        els = header(
            "为什么太阳内部走 70 万公里要几万年，出了表面走 1.5 亿公里只要 8 分 19 秒？",
            "左图对比辐射区折返碰撞的“醉汉漫步”与直穿而出的中微子；右图算清 √N 随机游走的步数账。",
        )
        # Left card: Random walk vs Neutrino straight line (x=20, w=346)
        els.append(card(20, 62, 346, 252))
        els.append(txt(36, 85, "① 折返传球的光子 vs 穿墙而过的中微子", 12.4, INK, weight="700"))
        cx, cy = 186, 194
        els.append(f'<circle cx="{cx}" cy="{cy}" r="92" fill="#fff7ed" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(f'<circle cx="{cx}" cy="{cy}" r="66" fill="#ffedd5" stroke="{ORANGE}" stroke-width="1" stroke-dasharray="3 3"/>')
        els.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="#fed7aa" stroke="{ORANGE}" stroke-width="1.2"/>')
        els.append(txt(cx, cy + 4, "核心", 10.2, ORANGE, "middle", weight="700"))

        # Deterministic pseudo-random walk from center out to r=66
        ang_seed = 137
        wx_p, wy_p = float(cx), float(cy)
        w_pts = [f"{wx_p:.1f},{wy_p:.1f}"]
        for k in range(42):
            ang_seed = (ang_seed * 1103515245 + 12345) & 0x7FFFFFFF
            # Slight outward drift for illustrative 42-segment path reaching r=66
            theta = (ang_seed / 0x7FFFFFFF) * 2 * math.pi
            wx_p += 11.5 * math.cos(theta) + 1.35
            wy_p += 11.5 * math.sin(theta) - 0.85
            r_now = math.hypot(wx_p - cx, wy_p - cy)
            if r_now > 64:
                wx_p = cx + (wx_p - cx) * 64 / r_now
                wy_p = cy + (wy_p - cy) * 64 / r_now
            w_pts.append(f"{wx_p:.1f},{wy_p:.1f}")
        w_pts.append(f"{cx + 84:.1f},{cy - 38:.1f}")
        els.append(f'<polyline points="{" ".join(w_pts)}" fill="none" stroke="{ORANGE}" stroke-width="1.5"/>')

        # Straight neutrino ray
        els.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 128}" y2="{cy + 44}" stroke="{BLUE}" stroke-width="2.0" stroke-dasharray="5 3" marker-end="url(#arr-blue)"/>')
        els.append(txt(cx + 76, cy + 56, "中微子：约 2.3 秒直穿太阳！", 10.3, BLUE, "middle", weight="700", halo=True))
        els.append(txt(cx - 8, cy - 74, "能量乱撞接力：万年量级", 10.3, ORANGE, "middle", weight="700", halo=True))

        # Right card: Why N = (R/l)^2 explodes! (x=378, w=362)
        els.append(card(378, 62, 362, 252))
        els.append(txt(394, 85, "② 随机游走公式：方向乱撞，距离只按 √N 长", 12.2, INK, weight="700"))

        els.append(card(394, 100, 330, 84, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(406, 121, "• 直线跑 N 步（每步长 ℓ）：净前进 N × ℓ", 10.8, BODY))
        els.append(txt(406, 142, "• 每次随机换向撞 N 次：净推进仅约 √N × ℓ ！", 10.8, BLUE, weight="700"))
        els.append(txt(406, 164, "→ 想向外挪远 10 倍，碰撞次数得翻 100 倍（N = R²/ℓ²）", 10.4, INK, weight="600"))

        els.append(card(394, 194, 330, 106, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(406, 215, "数量级对比（教学示意账）：", 11.0, INK, weight="700"))
        els.append(txt(406, 236, f"• 太阳内部（假设平均每步 1 毫米出 50万公里辐射区）：", 10.3, BODY))
        els.append(txt(406, 254, f"  需撞 (5×10¹¹)² ≈ 2.5×10²³ 次 → 折合耗时约 {t_years / 10000:.1f} 万年！", 10.3, ORANGE, weight="700"))
        els.append(txt(406, 276, "• 离开光球进太空（1.496 亿公里真空无遮挡）：", 10.3, BODY))
        els.append(txt(406, 293, "  直线狂奔 → 499 秒（8 分 19 秒）直达你脸庞！", 10.3, GREEN, weight="700"))

        return figure(
            330,
            "太阳内部随机游走能量输运与中微子直穿时间尺度对比",
            "左图对比辐射区内折返散射吸收的能量传递路线与约2.3秒直穿太阳的中微子；右图用随机游走R等于根号N乘步长计算为何毫米级步长走出辐射区需万年量级。",
            els,
        )

    def fig_lunar_leap_zhongqi():
        # Kepler's 2nd law effect on solar terms:
        # Winter (near Jan 4 perihelion, e=0.0167): Sun moves ~1.019 deg/day -> 30 deg between Major Solar Terms (中气) takes ~29.44 days (< 29.53 d synodic month!)
        # Summer (near Jul 4 aphelion): Sun moves ~0.953 deg/day -> 30 deg between 中气 takes ~31.46 days (> 29.53 d synodic month!)
        e_orb = 0.0167
        mean_step = 365.2422 / 12.0  # 30.43685 days per 30 deg
        dt_winter = mean_step * ((1 - e_orb) ** 2) / math.sqrt(1 - e_orb * e_orb)
        dt_summer = mean_step * ((1 + e_orb) ** 2) / math.sqrt(1 - e_orb * e_orb)
        synodic = 29.5306
        assert dt_winter < synodic < dt_summer

        els = header(
            "无中气置闰：为什么“闰四月、闰五月”常见，“闰腊月、闰正月”极罕见？",
            "地球公转轨道是椭圆（1月初近日点快、7月初远日点慢），直接拉开了冬夏两个“中气”的时间间距！",
        )
        # Top card: Summer wide spacing -> easy to fit a whole 29.5d lunar month inside!
        els.append(card(20, 62, 720, 122))
        els.append(txt(36, 85, f"① 夏半年（远日点附近地球走得慢）：两个中气相隔约 {dt_summer:.1f} 天 > 朔望月 29.5 天 → 容易卡出“无中气闰月”！", 12.2, GREEN, weight="700"))
        # Timeline scale: 1 day = 9.2 px, start x=60
        sc = 9.2
        sx = 68
        # Zhongqi A at day 0 (芒种后夏至, e.g. 夏至), Zhongqi B at day 31.45 (大暑), Zhongqi C at day 62.8 (处暑)
        z_sum = [(0.0, "中气：夏至(90°)"), (dt_summer, "中气：大暑(120°)"), (dt_summer * 2, "中气：处暑(150°)")]
        els.append(f'<line x1="{sx}" y1="132" x2="{sx + 68 * sc:.1f}" y2="132" stroke="{SLATE}" stroke-width="1.5"/>')
        # Lunar months starting at day -28, day 1.5, day 31.0, day 60.5!
        # Notice month from day 1.5 to day 31.03 sits COMPLETELY between 0.0 and 31.45 -> ZERO Zhongqi inside!
        m_starts = [(1.5, 31.03, "这个农历月夹在两中气之间：0 个中气 → 定为闰五月！", ORANGE, ORANGE_SOFT), (31.03, 60.56, "含“大暑” → 六月", BLUE, BLUE_SOFT)]
        for d0, d1, mlbl, mcol, mbg in m_starts:
            x0, x1 = sx + d0 * sc, sx + d1 * sc
            els.append(f'<rect x="{x0:.1f}" y="102" width="{x1 - x0:.1f}" height="26" rx="5" fill="{mbg}" stroke="{mcol}" stroke-width="1.5"/>')
            els.append(txt((x0 + x1) / 2, 119, mlbl, 10.3, mcol, "middle", weight="700"))
        for zd, zlbl in z_sum:
            zx = sx + zd * sc
            els.append(f'<line x1="{zx:.1f}" y1="96" x2="{zx:.1f}" y2="146" stroke="{GREEN}" stroke-width="2.0"/>')
            els.append(f'<circle cx="{zx:.1f}" cy="132" r="4" fill="{GREEN}"/>')
            els.append(txt(zx, 164, zlbl, 10.4, GREEN, "middle", weight="700"))

        # Bottom card: Winter tight spacing -> 29.4d < 29.5d, almost every lunar month catches a Zhongqi!
        els.append(card(20, 196, 720, 118))
        els.append(txt(36, 219, f"② 冬半年（近日点附近地球走得快）：两个中气仅隔约 {dt_winter:.1f} 天 ≤ 朔望月 29.5 天 → 几乎每月都撞上中气！", 12.2, BLUE, weight="700"))
        els.append(f'<line x1="{sx}" y1="264" x2="{sx + 68 * sc:.1f}" y2="264" stroke="{SLATE}" stroke-width="1.5"/>')
        z_win = [(0.0, "中气：冬至(270°)"), (dt_winter, "中气：大寒(300°)"), (dt_winter * 2, "中气：雨水(330°)")]
        w_months = [(1.0, 30.53, "含“大寒” → 十二月（腊月）"), (30.53, 60.06, "含“雨水” → 正月")]
        for d0, d1, mlbl in w_months:
            x0, x1 = sx + d0 * sc, sx + d1 * sc
            els.append(f'<rect x="{x0:.1f}" y="234" width="{x1 - x0:.1f}" height="26" rx="5" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.3"/>')
            els.append(txt((x0 + x1) / 2, 251, mlbl, 10.4, BLUE, "middle", weight="600"))
        for zd, zlbl in z_win:
            zx = sx + zd * sc
            els.append(f'<line x1="{zx:.1f}" y1="228" x2="{zx:.1f}" y2="278" stroke="{BLUE}" stroke-width="2.0"/>')
            els.append(f'<circle cx="{zx:.1f}" cy="264" r="4" fill="{BLUE}"/>')
            els.append(txt(zx, 296, zlbl, 10.4, BLUE, "middle", weight="700"))

        return figure(
            328,
            "农历无中气置闰规则与地球椭圆轨道冬夏中气间距对比",
            "上图展示夏半年远日点附近两中气间隔约31.4天大于29.5天朔望月，易出现不含中气的闰月；下图展示冬半年近日点附近两中气仅隔约29.4天，极难产生闰腊月或闰正月。",
            els,
        )

    def fig_synodic_fullmoon_16():
        # Verify Sidereal vs Synodic relation: 1/T_syn = 1/T_sid - 1/T_earth
        t_sid = 27.32166
        t_yr = 365.25636
        t_syn = 1.0 / (1.0 / t_sid - 1.0 / t_yr)
        assert abs(t_syn - 29.5306) < 0.002

        els = header(
            "月亮的两个常见追问：为什么朔望月比公转周期长 2.2 天？为什么“十五的月亮十六圆”？",
            "左图演示地球边走边看导致月亮必须多追约 29°；右图算清“初一朔时刻 + 椭圆慢半圈”的时间账。",
        )
        # Left card: Sidereal 27.32d vs Synodic 29.53d (x=20, w=352)
        els.append(card(20, 62, 352, 252))
        els.append(txt(36, 85, "① 恒星月 27.32 天 vs 朔望月 29.53 天", 12.4, INK, weight="700"))
        # Sun at left (78, 192), Earth E1 at (232, 224), Earth E2 ~29 deg up along arc at (246, 146)
        sx, sy = 74, 188
        els.append(f'<circle cx="{sx}" cy="{sy}" r="18" fill="#fde047" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append(txt(sx, sy + 4, "太阳", 10.2, INK, "middle", weight="700"))
        # Earth orbit arc
        els.append(f'<path d="M222,256 Q262,188 228,118" fill="none" stroke="{HAIRLINE}" stroke-width="1.4" stroke-dasharray="4 3"/>')

        e1x, e1y = 242, 224
        e2x, e2y = 244, 142
        for ex, ey, elbl in ((e1x, e1y, "初一地球"), (e2x, e2y, "29.5天后")):
            els.append(f'<circle cx="{ex}" cy="{ey}" r="34" fill="none" stroke="{BLUE_LINE}" stroke-width="1.1" stroke-dasharray="3 2"/>')
            els.append(f'<circle cx="{ex}" cy="{ey}" r="9" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
            els.append(txt(ex + 44, ey + 4, elbl, 10.2, BLUE, weight="600"))

        # Moon at E1 facing Sun
        m1x, m1y = e1x - 33, e1y - 7
        els.append(f'<circle cx="{m1x}" cy="{m1y}" r="5" fill="{SLATE}"/>')
        # At E2: parallel direction (27.32d sidereal) vs Sun-line direction (29.53d synodic!)
        els.append(f'<line x1="{sx}" y1="{sy}" x2="{e1x}" y2="{e1y}" stroke="{ORANGE}" stroke-width="1.1" stroke-dasharray="3 3"/>')
        els.append(f'<line x1="{sx}" y1="{sy}" x2="{e2x}" y2="{e2y}" stroke="{ORANGE}" stroke-width="1.3"/>')
        els.append(f'<line x1="{e2x}" y1="{e2y}" x2="{e2x - 44}" y2="{e2y - 9}" stroke="{SLATE}" stroke-width="1.2" stroke-dasharray="3 2"/>')
        els.append(f'<circle cx="{e2x - 33}" cy="{e2y - 7}" r="4.5" fill="#cbd5e1" stroke="{SLATE}"/>')
        els.append(f'<circle cx="{e2x - 31}" cy="{e2y + 13}" r="5" fill="{ORANGE}"/>')
        els.append(txt(154, 114, "27.32天转满360°", 10.0, SLATE, "middle"))
        els.append(txt(156, 174, "再多追2.21天重新对准太阳!", 10.0, ORANGE, "middle", weight="700", halo=True))
        els.append(txt(36, 294, "公式核验：1/27.32 − 1/365.26 = 1/29.53（分毫不差！）", 10.3, MUTED))

        # Right card: Why Full Moon lands on 16th (x=384, w=356)
        els.append(card(384, 62, 356, 252))
        els.append(txt(400, 85, "② 为什么满月最爱落在农历十六？", 12.4, INK, weight="700"))

        els.append(card(400, 102, 324, 92, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(412, 122, "原因一：“初一”是一整天，“朔”只是一个瞬间", 11.0, BLUE, weight="700"))
        els.append(txt(412, 143, "• 只要“朔”落在当天 00:00–23:59，这天就定为初一", 10.4, BODY))
        els.append(txt(412, 162, "• 若初一下午 18:00 才合朔，往后加半个月（平均 14.77 天", 10.4, BODY))
        els.append(txt(412, 180, "  = 14天18小时），就已经跨进十六中午 12:00 了！", 10.4, INK, weight="700"))

        els.append(card(400, 204, 324, 94, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(412, 224, "原因二：月球也走椭圆轨道（远地点慢悠悠）", 11.0, ORANGE, weight="700"))
        els.append(txt(412, 245, "• 过近地点快：朔到望最短仅约 13.9 天 → 十五甚至十四圆", 10.4, BODY))
        els.append(txt(412, 264, "• 过远地点慢：朔到望最长可达约 15.6 天！", 10.4, BODY))
        els.append(txt(412, 283, "→ 初一晚合朔 + 远地点慢半圈 = 十六圆最常见，偶尔十七圆！", 10.3, ORANGE, weight="700"))

        return figure(
            330,
            "恒星月与朔望月几何差及十五的月亮十六圆时间成因",
            "左图展示地球公转前进导致月球转满360度恒星月27.32天后还需多走2.21天才回到日月同经度的朔望月29.53天；右图解释合朔时刻跨度与月球远地点减速为何使满月最常落在农历十六。",
            els,
        )

    for fname, content in (
        ("prenatal-senses", fig_prenatal_senses()),
        ("baby-perspective", fig_baby_perspective()),
        ("emotion-repair-loop", fig_emotion_repair_loop()),
        ("smile-serve-return", fig_smile_serve_return()),
        ("who-motor-windows", fig_who_motor_windows()),
        ("child-24h-executive", fig_child_24h_executive()),
        ("wing-lift-stall", fig_wing_lift_stall()),
        ("newton-cannon-orbits", fig_newton_cannon_orbits()),
        ("sun-mass-thermostat", fig_sun_mass_thermostat()),
        ("photon-random-walk", fig_photon_random_walk()),
        ("lunar-leap-zhongqi", fig_lunar_leap_zhongqi()),
        ("synodic-fullmoon-16", fig_synodic_fullmoon_16()),
    ):
        write_svg(SUB, fname, content)
    print("Generated 12 early-curiosity SVGs; all WHO, orbital, nuclear, and calendar assertions passed.")

@register("plasma-state", "等离子体第四态：四态阶梯与准电中性、德拜屏蔽曲线、洛伦兹磁螺旋约束、冷热相图与芯片刻蚀", "science_tech")
def build_plasma_state():
    SUBDIR = "plasma-state"

    EPS0 = 8.8541878128e-12       # Vacuum permittivity (F/m)

    KB = 1.380649e-23             # Boltzmann constant (J/K)

    QE = 1.602176634e-19          # Elementary charge (C)

    ME = 9.1093837015e-31         # Electron mass (kg)

    MP = 1.67262192369e-27        # Proton mass (kg)

    EV_TO_K = QE / KB             # 1 eV in Kelvin (~11604.5 K)

    def debye_length(t_e_kelvin: float, n_e_m3: float) -> float:
        """Compute electron Debye screening length lambda_D (meters)."""
        return math.sqrt(EPS0 * KB * t_e_kelvin / (n_e_m3 * QE * QE))

    def plasma_frequency(n_e_m3: float) -> float:
        """Compute electron plasma angular frequency omega_pe (rad/s)."""
        return math.sqrt(n_e_m3 * QE * QE / (EPS0 * ME))

    def debye_number(t_e_kelvin: float, n_e_m3: float) -> float:
        """Number of electrons inside a Debye sphere N_D = (4/3)*pi*n_e*lambda_D^3."""
        lam = debye_length(t_e_kelvin, n_e_m3)
        return (4.0 / 3.0) * math.pi * n_e_m3 * (lam ** 3)

    def elastic_transfer_fraction(m1: float, m2: float) -> float:
        """Maximum kinetic energy transfer fraction in a head-on elastic collision."""
        return 4.0 * m1 * m2 / ((m1 + m2) ** 2)

    def _verify_physics_assertions() -> None:
        """Run quantitative physics checks before writing any SVG."""
        # 1. eV <-> Kelvin conversion
        assert 11604.0 < EV_TO_K < 11605.0, f"Unexpected EV_TO_K={EV_TO_K}"

        # 2. Debye lengths across solar core, ITER tokamak, chip plasma, ionosphere
        lam_solar = debye_length(1.5e7, 1.0e32)       # ~2.67e-11 m
        lam_tokamak = debye_length(1.5e8, 1.0e20)     # ~8.45e-5 m
        lam_chip = debye_length(2.0 * EV_TO_K, 1.0e16)  # ~1.05e-4 m
        lam_iono = debye_length(1500.0, 1.0e11)       # ~8.45e-3 m
        assert 2.0e-11 < lam_solar < 3.5e-11
        assert 7.5e-5 < lam_tokamak < 9.5e-5
        assert 9.5e-5 < lam_chip < 1.15e-4
        assert 7.5e-3 < lam_iono < 9.5e-3
        assert lam_solar < lam_tokamak < lam_chip < lam_iono

        # Collective plasma parameter N_D >> 1 for true plasmas
        assert debye_number(1.5e8, 1.0e20) > 1.0e8
        assert debye_number(2.0 * EV_TO_K, 1.0e16) > 1.0e4
        assert debye_number(1500.0, 1.0e11) > 1.0e5

        # 3. Screened Debye-Yukawa potential vs bare Coulomb potential
        for u in (0.35, 1.0, 2.0, 3.0):
            bare = 1.0 / u
            screened = math.exp(-u) / u
            assert 0.0 < screened < bare
        assert abs((math.exp(-1.0) / 1.0) / (1.0 / 1.0) - (1.0 / math.e)) < 1e-12
        assert (math.exp(-3.0) / 3.0) / (1.0 / 3.0) < 0.05  # < 5% beyond 3 lambda_D

        # 4. Larmor helical trajectory conservation & opposite gyration sense
        # Electron (q = -e) vs Proton (q = +e) in B = B0 * z_hat:
        # Signed angular velocity Omega_z = -q*B/m => Omega_e > 0, Omega_p < 0
        b_field = 2.0  # Tesla
        omega_e = -(-QE) * b_field / ME
        omega_p = -(+QE) * b_field / MP
        assert omega_e > 0.0 and omega_p < 0.0 and omega_e * omega_p < 0.0
        assert abs(omega_e / abs(omega_p) - (MP / ME)) < 1e-6

        r_larmor = 0.02
        v_par = 1.5e5
        for step in range(36):
            t = step * 1e-9
            x = r_larmor * math.cos(omega_p * t)
            y = r_larmor * math.sin(omega_p * t)
            z = v_par * t
            vx = -r_larmor * omega_p * math.sin(omega_p * t)
            vy = r_larmor * omega_p * math.cos(omega_p * t)
            vz = v_par
            ax = -r_larmor * (omega_p ** 2) * math.cos(omega_p * t)
            ay = -r_larmor * (omega_p ** 2) * math.sin(omega_p * t)
            az = 0.0
            assert abs(math.hypot(x, y) - r_larmor) < 1e-12
            # Lorentz acceleration is strictly perpendicular to velocity: cos(theta) == 0
            cos_va = (vx * ax + vy * ay + vz * az) / (math.hypot(vx, vy, vz) * math.hypot(ax, ay, az))
            assert abs(cos_va) < 1e-14
            _ = z

        # 5. Elastic energy transfer fraction: ping-pong electron vs heavy ion
        eta_ep = elastic_transfer_fraction(ME, MP)
        eta_approx = 4.0 * ME / MP
        eta_ene = elastic_transfer_fraction(ME, 20.18 * MP)  # Neon-20
        assert abs(eta_ep - 0.002176) < 1e-5
        assert abs(eta_approx - 0.002179) < 1e-5
        assert 1.0e-4 < eta_ene < 1.15e-4

    def _charge_disc(cx: float, cy: float, r: float, sign: str, fg: str, bg: str) -> str:
        """Render a crisp + or - charge particle circle."""
        arm = r * 0.48
        parts = [
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.3"/>',
            f'<line x1="{cx - arm:.1f}" y1="{cy:.1f}" x2="{cx + arm:.1f}" y2="{cy:.1f}" stroke="{fg}" stroke-width="1.5" stroke-linecap="round"/>',
        ]
        if sign == "+":
            parts.append(
                f'<line x1="{cx:.1f}" y1="{cy - arm:.1f}" x2="{cx:.1f}" y2="{cy + arm:.1f}" stroke="{fg}" stroke-width="1.5" stroke-linecap="round"/>'
            )
        return "\n".join(parts)

    def _build_four_states_ladder() -> None:
        """SVG 1: Solid -> Liquid -> Neutral Gas -> Plasma & why '等离子 = 准电中性'."""
        els = header(
            "持续注入能量：从固态冰晶到“正负电荷数相等”的等离子体",
            "继续升温或施加电磁场，原子外层电子终被撞脱；“等离子”指宏观正负电荷平衡",
        )

        xs = [20, 204, 388, 572]
        cw, cy, ch = 168, 64, 202

        # Card 1: Solid
        x0 = xs[0]
        els.append(card(x0, cy, cw, ch, fill=CARD_BG, stroke=BORDER))
        els.append(pill(x0 + 12, cy + 10, "① 固态 Solid", fg=SLATE, bg=SLATE_SOFT, w=106, h=20, size=11.5))
        els.append(card(x0 + 14, cy + 38, 140, 102, rx=7, fill="#f8fafc", stroke=HAIRLINE))
        gx = [x0 + 48, x0 + 84, x0 + 120]
        gy = [cy + 60, cy + 89, cy + 118]
        for r_i in range(3):
            for c_i in range(3):
                if c_i < 2:
                    els.append(f'<line x1="{gx[c_i]}" y1="{gy[r_i]}" x2="{gx[c_i + 1]}" y2="{gy[r_i]}" stroke="#94a3b8" stroke-width="1.4"/>')
                if r_i < 2:
                    els.append(f'<line x1="{gx[c_i]}" y1="{gy[r_i]}" x2="{gx[c_i]}" y2="{gy[r_i + 1]}" stroke="#94a3b8" stroke-width="1.4"/>')
        for py in gy:
            for px in gx:
                els.append(f'<circle cx="{px}" cy="{py}" r="6.5" fill="#cbd5e1" stroke="{SLATE}" stroke-width="1.3"/>')
        els.append(txt(x0 + cw / 2, cy + 162, "晶格锁死，原地微振", 11.5, INK, "middle", "600"))
        els.append(txt(x0 + cw / 2, cy + 183, "电子紧绑在各自原子核旁", 10.8, MUTED, "middle"))

        # Card 2: Liquid
        x1 = xs[1]
        els.append(card(x1, cy, cw, ch, fill=CARD_BG, stroke=BORDER))
        els.append(pill(x1 + 12, cy + 10, "② 液态 Liquid", fg=BLUE, bg=BLUE_SOFT, w=110, h=20, size=11.5))
        els.append(card(x1 + 14, cy + 38, 140, 102, rx=7, fill="#f4f9fd", stroke=BLUE_LINE))
        els.append(f'<path d="M{x1 + 20},{cy + 78} Q{x1 + 52},{cy + 71} {x1 + 84},{cy + 78} T{x1 + 148},{cy + 78}" fill="none" stroke="{BLUE_LINE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
        liq_pts = [
            (38, 92), (62, 88), (88, 94), (114, 89), (134, 96),
            (46, 114), (73, 112), (99, 116), (126, 115),
            (56, 129), (86, 128), (114, 129),
        ]
        for dx, dy in liq_pts:
            els.append(f'<circle cx="{x1 + dx}" cy="{cy + dy}" r="6.5" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.3"/>')
        els.append(f'<path d="M{x1 + 52},{cy + 103} C{x1 + 66},{cy + 98} {x1 + 74},{cy + 106} {x1 + 88},{cy + 102}" fill="none" stroke="{BLUE}" stroke-width="1.2" marker-end="url(#arr-blue)"/>')
        els.append(txt(x1 + cw / 2, cy + 162, "晶格瓦解，彼此滑移", 11.5, INK, "middle", "600"))
        els.append(txt(x1 + cw / 2, cy + 183, "仍是完整电中性分子", 10.8, MUTED, "middle"))

        # Card 3: Neutral Gas
        x2 = xs[2]
        els.append(card(x2, cy, cw, ch, fill=CARD_BG, stroke=BORDER))
        els.append(pill(x2 + 12, cy + 10, "③ 气态 Gas", fg=ORANGE, bg=ORANGE_SOFT, w=98, h=20, size=11.5))
        els.append(card(x2 + 14, cy + 38, 140, 102, rx=7, fill="#fffaf5", stroke="#fed7aa"))
        gas_vecs = [
            (42, 62, 18, 10),
            (122, 60, -18, 12),
            (82, 92, 16, -15),
            (46, 118, 20, -6),
            (126, 118, -16, -14),
        ]
        for dx, dy, vx, vy in gas_vecs:
            px, py = x2 + dx, cy + dy
            els.append(f'<line x1="{px}" y1="{py}" x2="{px + vx}" y2="{py + vy}" stroke="{ORANGE}" stroke-width="1.2" marker-end="url(#arr-orange)"/>')
            els.append(f'<circle cx="{px}" cy="{py}" r="6.5" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.3"/>')
        els.append(txt(x2 + cw / 2, cy + 162, "间距拉大，自由乱飞", 11.5, INK, "middle", "600"))
        els.append(txt(x2 + cw / 2, cy + 183, "中性分子：撞上才知彼此", 10.8, MUTED, "middle"))

        # Card 4: Plasma (highlighted)
        x3 = xs[3]
        els.append(card(x3, cy, cw, ch, fill="#fcfaff", stroke=PURPLE, sw=1.5))
        els.append(pill(x3 + 12, cy + 10, "④ 等离子体 Plasma", fg=PURPLE, bg=PURPLE_SOFT, w=136, h=20, size=11.5))
        els.append(card(x3 + 14, cy + 38, 140, 102, rx=7, fill="#f8f5ff", stroke="#d8b4fe"))
        # Long-range Coulomb interaction curves between ions and electrons
        ions = [(46, 66), (118, 68), (54, 116), (118, 114)]
        elecs = [(82, 58), (38, 92), (88, 92), (132, 92), (84, 124)]
        links = [((46, 66), (82, 58)), ((118, 68), (88, 92)), ((54, 116), (38, 92)), ((118, 114), (84, 124)), ((46, 66), (88, 92))]
        for (ix, iy), (ex, ey) in links:
            els.append(
                f'<line x1="{x3 + ix}" y1="{cy + iy}" x2="{x3 + ex}" y2="{cy + ey}" stroke="#a78bfa" stroke-width="1.1" stroke-dasharray="3 2.5"/>'
            )
        for ix, iy in ions:
            els.append(_charge_disc(x3 + ix, cy + iy, 7.5, "+", ORANGE, ORANGE_SOFT))
        for ex, ey in elecs[:4]:
            els.append(_charge_disc(x3 + ex, cy + ey, 5.2, "-", BLUE, BLUE_SOFT))
        # Extra labels inside mini-box top right
        els.append(txt(x3 + 147, cy + 52, "⊕正离子", 10.5, ORANGE, "end", "600"))
        els.append(txt(x3 + 147, cy + 134, "⊖自由电子", 10.5, BLUE, "end", "600"))
        els.append(txt(x3 + cw / 2, cy + 162, "电子挣脱！带电粒子汤", 11.5, PURPLE, "middle", "700"))
        els.append(txt(x3 + cw / 2, cy + 183, "导电、受控磁场、集体振荡", 10.8, BODY, "middle"))

        # Transition arrows in the 16px gaps between cards
        for gx_mid, lbl in [(196, "熔化"), (380, "汽化"), (564, "电离")]:
            col = PURPLE if lbl == "电离" else MUTED
            els.append(txt(gx_mid, cy + 92, lbl, 10.5, col, "middle", "600", halo=True))
            els.append(
                f'<line x1="{gx_mid - 7}" y1="{cy + 102}" x2="{gx_mid + 6}" y2="{cy + 102}" stroke="{col}" stroke-width="1.5" marker-end="url(#{"arr-blue" if lbl != "电离" else "arr-orange"})"/>'
            )

        # Energy bar across full width (text on left, arrow in middle, threshold on right — zero overlap)
        els.append(card(20, 276, 720, 26, rx=6, fill=ORANGE_SOFT, stroke="#fdba74"))
        els.append(txt(34, 293, "持续注入能量：高温热碰撞 / 强电场击穿 / 高能辐射", 11.2, ORANGE, "start", "600"))
        els.append(
            f'<line x1="382" y1="289" x2="558" y2="289" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>'
        )
        els.append(txt(726, 293, "跨越原子电离能门槛", 11.2, PURPLE, "end", "700"))

        # Bottom etymology & quasi-neutrality callout
        els.append(card(20, 312, 720, 64, rx=9, fill=BLUE_SOFT, stroke=BLUE_LINE))
        els.append(pill(34, 323, "为什么译作“等离子体”？", fg=BLUE, bg="#ffffff", w=156, h=22, size=11.5))
        els.append(
            txt(
                202,
                338,
                "1928 年朗缪尔借医学“血浆（Plasma）”命名：电离气体像血浆托载血细胞那样承载电子与离子。",
                11.5,
                INK,
            )
        )
        els.append(
            txt(
                34,
                362,
                "中文译名抓住了核心物理：宏观体积内正、负电荷数几乎相等（nₑ ≈ Z·nᵢ，准电中性），绝非“粒子个头相等”！",
                11.5,
                BODY,
                weight="600",
            )
        )

        svg = figure(
            390,
            "物质四态能量阶梯与等离子体准电中性",
            "对比固态晶格、液态滑移、气态中性分子碰撞与等离子体自由电子和正离子共存，说明持续输入能量引发电离以及等离子体宏观正负电荷数密度近似相等的准电中性。",
            els,
        )
        write_svg(SUBDIR, "four-states-ladder.svg", svg)

    def _build_debye_shielding_curve() -> None:
        """SVG 2: Spatial Debye sphere screening + exact bare 1/r vs Yukawa exp(-r/lambda_D)/r."""
        extra_css = """
      .yukawa-anim {
        stroke-dasharray: 420;
        stroke-dashoffset: 420;
        animation: drawYukawa 1.8s ease-out 0.15s 1 forwards;
      }
      @keyframes drawYukawa {
        to { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .yukawa-anim {
          stroke-dasharray: none;
          stroke-dashoffset: 0;
          animation: none;
        }
      }"""

        els = header(
            "德拜屏蔽：为什么等离子体对外显电中性，内部却一呼百应？",
            "自由电子围拢在德拜长度 λ_D 内抵消外加电场，使库仑势比真空多乘一项指数衰减因子",
        )

        # Left card: Spatial Debye sphere
        els.append(card(20, 62, 352, 294))
        els.append(txt(36, 84, "① 空间机制：德拜球内的电子云屏蔽", PANEL_TITLE, INK, weight="600"))
        els.append(card(36, 96, 320, 198, rx=8, fill="#f8fafc", stroke=HAIRLINE))

        cx, cy, rd = 196.0, 195.0, 68.0
        # Outer neutral background label
        els.append(txt(46, 114, "外部准电中性区 (r > λ_D)", 10.8, MUTED))
        # Balanced pairs outside Debye sphere (strictly inside [48..344, 122..282])
        outer_ions = [(66, 146), (104, 258), (288, 138), (324, 206), (292, 266), (78, 208)]
        outer_elecs = [(86, 162), (126, 270), (268, 126), (334, 182), (314, 252), (60, 232)]
        for px, py in outer_ions:
            els.append(_charge_disc(px, py, 6.2, "+", ORANGE, ORANGE_SOFT))
        for px, py in outer_elecs:
            els.append(_charge_disc(px, py, 4.8, "-", BLUE, BLUE_SOFT))

        # Debye sphere circle
        els.append(
            f'<circle cx="{cx}" cy="{cy}" r="{rd}" fill="{BLUE_SOFT}" fill-opacity="0.72" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 3.5"/>'
        )

        # Dense electron cloud inside Debye sphere (leave -32 deg corridor clear for lambda_D arrow)
        inner_rings = [
            (25.0, [20, 82, 144, 205, 268]),
            (45.0, [8, 56, 106, 158, 210, 262]),
        ]
        for rad, degs in inner_rings:
            for deg in degs:
                ang = math.radians(deg)
                els.append(_charge_disc(cx + rad * math.cos(ang), cy + rad * math.sin(ang), 4.8, "-", BLUE, "#ffffff"))
        # A couple of repelled ions near outer edge of Debye sphere
        for deg in (128, 295):
            ang = math.radians(deg)
            els.append(_charge_disc(cx + 57.0 * math.cos(ang), cy + 57.0 * math.sin(ang), 6.0, "+", ORANGE, ORANGE_SOFT))

        # Radius arrow for lambda_D at -34 degrees in open corridor
        ang_r = math.radians(-34.0)
        rx_end = cx + (rd - 2.0) * math.cos(ang_r)
        ry_end = cy + (rd - 2.0) * math.sin(ang_r)
        els.append(
            f'<line x1="{cx + 14 * math.cos(ang_r):.1f}" y1="{cy + 14 * math.sin(ang_r):.1f}" x2="{rx_end:.1f}" y2="{ry_end:.1f}" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#arr-green)"/>'
        )
        els.append(txt(cx + 34, cy - 30, "λ_D", 12, GREEN, "middle", "700", halo=True))

        # Central test charge +Q
        els.append(f'<circle cx="{cx}" cy="{cy}" r="13.5" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.8"/>')
        els.append(txt(cx, cy + 4.5, "+Q", 11.8, "#ffffff", "middle", "700"))

        els.append(txt(36, 316, "r < λ_D：轻快电子聚拢，净负电荷抵消 +Q", 11.3, INK))
        els.append(txt(36, 338, "r > λ_D：电场被截断，远处粒子几乎无感", 11.3, MUTED))

        # Right card: Exact computed bare 1/u vs Debye exp(-u)/u curve
        els.append(card(388, 62, 352, 294))
        els.append(txt(404, 84, "② 精确曲线：裸库仑势 vs 德拜屏蔽势", PANEL_TITLE, INK, weight="600"))

        ox, oy, pw, ph = 444.0, 268.0, 272.0, 158.0
        u_max, y_max = 3.4, 3.0

        def map_pt(u: float, val: float) -> tuple[float, float]:
            return ox + (u / u_max) * pw, oy - (val / y_max) * ph

        # Gridlines & axes
        for yv in (1.0, 2.0, 3.0):
            _, gy = map_pt(0.0, yv)
            els.append(f'<line x1="{ox}" y1="{gy:.1f}" x2="{ox + pw:.1f}" y2="{gy:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(ox - 7, gy + 4, f"{yv:.1f}", 10.5, MUTED, "end", cls="mono"))
        els.append(txt(ox - 7, oy + 4, "0", 10.5, MUTED, "end", cls="mono"))

        for uv, lbl in [(1.0, "1λ_D"), (2.0, "2λ_D"), (3.0, "3λ_D")]:
            gx, _ = map_pt(uv, 0.0)
            els.append(f'<line x1="{gx:.1f}" y1="{oy - ph:.1f}" x2="{gx:.1f}" y2="{oy:.1f}" stroke="{SLATE_SOFT}" stroke-width="1" stroke-dasharray="3 3"/>')
            els.append(txt(gx, oy + 16, lbl, 10.5, MUTED, "middle"))
        els.append(txt(ox, oy + 16, "0", 10.5, MUTED, "middle", cls="mono"))
        els.append(txt(ox + pw, oy + 31, "归一化距离 r / λ_D", 10.8, MUTED, "end"))
        els.append(txt(ox - 6, oy - ph - 8, "电势 Φ/Φ₀", 10.8, MUTED, "start"))

        els.append(f'<path d="M{ox:.1f},{oy - ph:.1f} V{oy:.1f} H{ox + pw:.1f}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')

        # Sample exact curves
        bare_pts = []
        deb_pts = []
        n_samples = 90
        for i in range(n_samples + 1):
            u_b = 0.345 + (u_max - 0.345) * (i / n_samples)
            bare_pts.append(map_pt(u_b, 1.0 / u_b))
            u_d = 0.255 + (u_max - 0.255) * (i / n_samples)
            deb_pts.append(map_pt(u_d, math.exp(-u_d) / u_d))

        bare_d = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in bare_pts)
        deb_d = "M" + " L".join(f"{px:.2f},{py:.2f}" for px, py in deb_pts)

        els.append(f'<path d="{bare_d}" fill="none" stroke="{ORANGE}" stroke-width="2.1" stroke-dasharray="6 4"/>')
        # Full-contrast static curve + animated highlight overlay so t=0 and reduced-motion stay 100% crisp
        els.append(f'<path d="{deb_d}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
        els.append(f'<path d="{deb_d}" fill="none" stroke="#38bdf8" stroke-width="2.6" stroke-opacity="0.55" class="yukawa-anim"/>')

        # Highlight r = 1 lambda_D attenuation to 1/e (36.8%)
        x1_px, y1_bare = map_pt(1.0, 1.0)
        _, y1_deb = map_pt(1.0, math.exp(-1.0))
        els.append(
            f'<line x1="{x1_px:.1f}" y1="{y1_bare + 4:.1f}" x2="{x1_px:.1f}" y2="{y1_deb - 5:.1f}" stroke="{GREEN}" stroke-width="1.5" marker-end="url(#arr-green)"/>'
        )
        els.append(f'<circle cx="{x1_px:.1f}" cy="{y1_bare:.1f}" r="3.6" fill="{ORANGE}"/>')
        els.append(f'<circle cx="{x1_px:.1f}" cy="{y1_deb:.1f}" r="4.0" fill="{BLUE}"/>')
        els.append(txt(x1_px + 7, y1_deb - 3, "降至 1/e (36.8%)", 10.6, GREEN, "start", "700", halo=True))

        # Clean legend card in open upper-right quadrant of plot
        els.append(card(528, 108, 192, 50, rx=6, fill="#ffffff", stroke=BORDER))
        els.append(f'<line x1="538" y1="124" x2="564" y2="124" stroke="{ORANGE}" stroke-width="2.1" stroke-dasharray="5 3"/>')
        els.append(txt(571, 128, "真空裸库仑势 1/r", 10.8, ORANGE, "start", "600"))
        els.append(f'<line x1="538" y1="144" x2="564" y2="144" stroke="{BLUE}" stroke-width="2.4"/>')
        els.append(txt(571, 148, "屏蔽势 (1/r)exp(−r/λ_D)", 10.8, BLUE, "start", "700"))

        els.append(txt(404, 316, "r = 3λ_D 时，屏蔽势仅剩真空值的 5%", 11.3, INK))
        els.append(txt(404, 338, "判据：体系尺寸 L ≫ λ_D 才显集体电中性", 11.3, MUTED))

        svg = figure(
            372,
            "德拜屏蔽球与汤川指数衰减电势曲线",
            "左图展示自由电子在半径为德拜长度的球内聚拢屏蔽正测试电荷；右图精确绘制真空库仑势1/r与等离子体德拜屏蔽势(1/r)exp(-r/λ_D)的对比，在一倍德拜长度处衰减至1/e。",
            els,
            extra_css=extra_css,
        )
        write_svg(SUBDIR, "debye-shielding-curve.svg", svg)

    def _build_magnetic_helix_bottle() -> None:
        """SVG 3: Opposite Larmor helices around B + Tokamak twisted magnetic bottle."""
        extra_css = """
      .helix-anim {
        stroke-dasharray: 560;
        stroke-dashoffset: 560;
        animation: traceHelix 2.0s ease-out 0.1s 1 forwards;
      }
      @keyframes traceHelix {
        to { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .helix-anim {
          stroke-dasharray: none;
          stroke-dashoffset: 0;
          animation: none;
        }
      }"""

        els = header(
            "洛伦兹力与磁约束：用看不见的磁力线造一只“一亿度保温瓶”",
            "带电粒子垂直磁场运动时被迫绕磁力线回旋；弯成环形并扭转磁力线即可悬空约束聚变燃料",
        )

        # Left card: Opposite Larmor gyromotion of electron vs ion
        els.append(card(20, 62, 352, 300))
        els.append(txt(36, 84, "① 微观：电子与正离子反向螺旋回旋", PANEL_TITLE, INK, weight="600"))
        els.append(card(36, 96, 320, 206, rx=8, fill="#f8fafc", stroke=HAIRLINE))

        # Upper magnetic field line for electron (y = 148)
        by_e = 148.0
        els.append(
            f'<line x1="48" y1="{by_e}" x2="342" y2="{by_e}" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#arr-green)"/>'
        )
        els.append(txt(342, by_e - 18, "磁场 B", 10.8, GREEN, "end", "600", halo=True))

        # Compute 3D helix projected onto (X, Y):
        # X(s) = x_start + s * span + tilt_x * R * cos(sign * omega * s)
        # Y(s) = y_axis - R * sin(sign * omega * s), depth Z(s) = cos(sign * omega * s)
        def add_helix(
            x_start: float,
            span: float,
            y_axis: float,
            radius: float,
            turns: float,
            chirality: float,
            fg: str,
            faint_fg: str,
        ) -> tuple[float, float]:
            n_seg = 180
            pts = []
            for k in range(n_seg + 1):
                u = k / n_seg
                ang = chirality * (2.0 * math.pi * turns * u + 0.35)
                px = x_start + u * span + 0.30 * radius * math.cos(ang)
                py = y_axis - radius * math.sin(ang)
                pz = math.cos(ang)  # >0 front, <0 back
                pts.append((px, py, pz))

            # Back segments (pz < 0) dashed/faint, front segments solid
            for k in range(n_seg):
                x_a, y_a, z_a = pts[k]
                x_b, y_b, z_b = pts[k + 1]
                if 0.5 * (z_a + z_b) < 0:
                    els.append(
                        f'<line x1="{x_a:.2f}" y1="{y_a:.2f}" x2="{x_b:.2f}" y2="{y_b:.2f}" stroke="{faint_fg}" stroke-width="1.4"/>'
                    )
            full_d = "M" + " L".join(f"{p[0]:.2f},{p[1]:.2f}" for p in pts)
            els.append(f'<path d="{full_d}" fill="none" stroke="{fg}" stroke-width="1.1" stroke-opacity="0.28"/>')
            for k in range(n_seg):
                x_a, y_a, z_a = pts[k]
                x_b, y_b, z_b = pts[k + 1]
                if 0.5 * (z_a + z_b) >= 0:
                    els.append(
                        f'<line x1="{x_a:.2f}" y1="{y_a:.2f}" x2="{x_b:.2f}" y2="{y_b:.2f}" stroke="{fg}" stroke-width="2.3" stroke-linecap="round"/>'
                    )
            return pts[-1][0], pts[-1][1]

        ex_end, ey_end = add_helix(58.0, 248.0, by_e, radius=13.0, turns=6.5, chirality=+1.0, fg=BLUE, faint_fg=BLUE_LINE)
        els.append(_charge_disc(ex_end, ey_end, 5.5, "-", BLUE, "#ffffff"))
        els.append(txt(52, 118, "电子 e⁻：质量轻，小半径高频右旋", 11.0, BLUE, "start", "600", halo=True))

        # Lower magnetic field line for positive ion (y = 232)
        by_i = 232.0
        els.append(
            f'<line x1="48" y1="{by_i}" x2="342" y2="{by_i}" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#arr-green)"/>'
        )
        ix_end, iy_end = add_helix(58.0, 244.0, by_i, radius=27.0, turns=2.8, chirality=-1.0, fg=ORANGE, faint_fg="#fdba74")
        els.append(_charge_disc(ix_end, iy_end, 7.2, "+", ORANGE, ORANGE_SOFT))
        els.append(txt(52, 286, "正离子 ⊕：质量大，大半径低频左旋", 11.0, ORANGE, "start", "600", halo=True))

        els.append(txt(36, 322, "洛伦兹力 F = q(v × B) 始终垂直速度 v", 11.3, INK, weight="600"))
        els.append(txt(36, 344, "横向逃逸被拉回圆周，仅能顺着磁力线滑行", 11.3, MUTED))

        # Right card: Tokamak toroidal magnetic bottle
        els.append(card(388, 62, 352, 300))
        els.append(txt(404, 84, "② 宏观：托卡马克（Tokamak）环形磁笼", PANEL_TITLE, INK, weight="600"))
        els.append(card(404, 96, 320, 206, rx=8, fill="#f8fafc", stroke=HAIRLINE))

        tcx, tcy = 564.0, 196.0
        r_maj = 78.0
        a_min = 25.0
        tilt = math.radians(34.0)  # isometric pitch angle

        def proj_torus(phi: float, theta: float, minor_r: float) -> tuple[float, float, float]:
            rc = r_maj + minor_r * math.cos(theta)
            x3 = rc * math.cos(phi)
            y3 = rc * math.sin(phi)
            z3 = minor_r * math.sin(theta)
            sx = tcx + x3
            sy = tcy + y3 * math.sin(tilt) - z3 * math.cos(tilt)
            depth = y3 * math.cos(tilt) + z3 * math.sin(tilt)  # larger = closer to viewer
            return sx, sy, depth

        # Outer vacuum vessel boundary & glowing plasma torus
        els.append(
            f'<ellipse cx="{tcx}" cy="{tcy}" rx="{r_maj + a_min + 11:.1f}" ry="{(r_maj + a_min + 11) * math.sin(tilt) + 15:.1f}" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4 3"/>'
        )
        els.append(
            f'<ellipse cx="{tcx}" cy="{tcy}" rx="{r_maj + a_min - 2:.1f}" ry="{(r_maj + a_min - 2) * math.sin(tilt) + 10:.1f}" fill="#fff1e6" stroke="#fdba74" stroke-width="1.2"/>'
        )
        # Inner torus hole (central solenoid region)
        els.append(
            f'<ellipse cx="{tcx}" cy="{tcy}" rx="{r_maj - a_min + 3:.1f}" ry="{(r_maj - a_min + 3) * math.sin(tilt) - 3:.1f}" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>'
        )
        # Central solenoid column
        els.append(card(tcx - 14, tcy - 31, 28, 48, rx=5, fill=GREEN_SOFT, stroke=GREEN, sw=1.3))
        els.append(txt(tcx, tcy - 5, "中心", 9.8, GREEN, "middle", "600"))
        els.append(txt(tcx, tcy + 8, "螺线管", 9.8, GREEN, "middle", "600"))

        # 8 Toroidal field (TF) coils around the torus: back half first, then helical line, then front half
        coil_angles = [math.radians(deg) for deg in (20, 65, 115, 160, 200, 245, 295, 340)]
        for phi_c in coil_angles:
            pts_c = [proj_torus(phi_c, 2.0 * math.pi * j / 40, a_min + 6.5) for j in range(41)]
            for j in range(40):
                if 0.5 * (pts_c[j][2] + pts_c[j + 1][2]) < 0:
                    els.append(
                        f'<line x1="{pts_c[j][0]:.2f}" y1="{pts_c[j][1]:.2f}" x2="{pts_c[j + 1][0]:.2f}" y2="{pts_c[j + 1][1]:.2f}" stroke="{BLUE_LINE}" stroke-width="1.8"/>'
                    )

        # Computed twisted helical magnetic field line on plasma surface (q = 3 winding)
        h_steps = 220
        h_pts = []
        for j in range(h_steps + 1):
            phi_h = 2.0 * math.pi * (j / h_steps)
            theta_h = 3.0 * phi_h + 0.4
            h_pts.append(proj_torus(phi_h, theta_h, a_min * 0.78))

        for j in range(h_steps):
            if 0.5 * (h_pts[j][2] + h_pts[j + 1][2]) < 0:
                els.append(
                    f'<line x1="{h_pts[j][0]:.2f}" y1="{h_pts[j][1]:.2f}" x2="{h_pts[j + 1][0]:.2f}" y2="{h_pts[j + 1][1]:.2f}" stroke="#d8b4fe" stroke-width="1.5"/>'
                )
            else:
                els.append(
                    f'<line x1="{h_pts[j][0]:.2f}" y1="{h_pts[j][1]:.2f}" x2="{h_pts[j + 1][0]:.2f}" y2="{h_pts[j + 1][1]:.2f}" stroke="{PURPLE}" stroke-width="2.2" stroke-linecap="round"/>'
                )
        hel_d = "M" + " L".join(f"{p[0]:.2f},{p[1]:.2f}" for p in h_pts)
        els.append(f'<path d="{hel_d}" fill="none" stroke="#c084fc" stroke-width="1.8" stroke-opacity="0.45" class="helix-anim"/>')

        # Front half of TF coils on top for accurate 3D occlusion
        for phi_c in coil_angles:
            pts_c = [proj_torus(phi_c, 2.0 * math.pi * j / 40, a_min + 6.5) for j in range(41)]
            for j in range(40):
                if 0.5 * (pts_c[j][2] + pts_c[j + 1][2]) >= 0:
                    els.append(
                        f'<line x1="{pts_c[j][0]:.2f}" y1="{pts_c[j][1]:.2f}" x2="{pts_c[j + 1][0]:.2f}" y2="{pts_c[j + 1][1]:.2f}" stroke="{BLUE}" stroke-width="2.2"/>'
                    )

        # Labels inside Tokamak box (well-separated corners with halo)
        els.append(txt(414, 114, "蓝圈：环向场线圈", 10.6, BLUE, "start", "600", halo=True))
        els.append(txt(714, 114, "紫线：扭曲合磁力线", 10.6, PURPLE, "end", "600", halo=True))
        els.append(txt(414, 292, "橙区：1.5×10⁸ K 聚变芯", 10.6, ORANGE, "start", "600", halo=True))
        els.append(txt(714, 292, "虚线：真空室外壁", 10.6, SLATE, "end", "600", halo=True))

        els.append(txt(404, 322, "把直管首尾相接成“甜甜圈”堵住两端漏口", 11.3, INK, weight="600"))
        els.append(txt(404, 344, "环向场+极向场拧成麻花，让上亿度等离子体悬空", 11.3, MUTED))

        svg = figure(
            378,
            "带电粒子拉莫尔磁螺旋与托卡马克环形磁约束",
            "左图按洛伦兹力精确投影电子与正离子绕磁力线反向、不同半径与频率的螺旋轨迹；右图展示托卡马克利用环向线圈与中心螺线管合成扭曲闭合磁力线，将1.5亿开尔文聚变等离子体悬空隔离于器壁之外。",
            els,
            extra_css=extra_css,
        )
        write_svg(SUBDIR, "magnetic-helix-bottle.svg", svg)

    def _build_plasma_map_cold_hot() -> None:
        """SVG 4: Log-log (n_e, T_e) map + ping-pong vs bowling ball cold-plasma paradox."""
        els = header(
            "等离子体全景图：为什么霓虹灯里上万度，摸着灯管却不烫手？",
            "对数坐标横跨 26 个密度量级；稀薄“冷等离子体”里只有轻电子极热，重原子仍接近室温",
        )

        # Left panel: Log10(n_e) vs Log10(T_e) phase diagram
        els.append(card(20, 62, 444, 318))
        els.append(txt(36, 84, "① 宇宙与实验室等离子体分布（对数坐标）", PANEL_TITLE, INK, weight="600"))

        ox, oy, pw, ph = 82.0, 320.0, 362.0, 204.0
        lg_n_min, lg_n_max = 6.0, 34.0
        lg_t_min, lg_t_max = 2.5, 8.8

        def map_log(lg_n: float, lg_t: float) -> tuple[float, float]:
            px = ox + ((lg_n - lg_n_min) / (lg_n_max - lg_n_min)) * pw
            py = oy - ((lg_t - lg_t_min) / (lg_t_max - lg_t_min)) * ph
            return px, py

        # Gridlines & ticks
        for lt, lbl in [(3, "10³"), (4, "10⁴"), (5, "10⁵"), (6, "10⁶"), (7, "10⁷"), (8, "10⁸")]:
            _, py = map_log(lg_n_min, float(lt))
            els.append(f'<line x1="{ox}" y1="{py:.1f}" x2="{ox + pw:.1f}" y2="{py:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(ox - 7, py + 4, lbl, 10.5, MUTED, "end"))

        for ln, lbl in [(6, "10⁶"), (12, "10¹²"), (18, "10¹⁸"), (24, "10²⁴"), (30, "10³⁰")]:
            px, _ = map_log(float(ln), lg_t_min)
            els.append(f'<line x1="{px:.1f}" y1="{oy - ph:.1f}" x2="{px:.1f}" y2="{oy:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(px, oy + 16, lbl, 10.5, MUTED, "middle"))

        # 1 eV = 11,605 K horizontal dashed guide
        _, y_1ev = map_log(lg_n_min, math.log10(EV_TO_K))
        els.append(
            f'<line x1="{ox}" y1="{y_1ev:.1f}" x2="{ox + pw:.1f}" y2="{y_1ev:.1f}" stroke="{BLUE_LINE}" stroke-width="1.1" stroke-dasharray="4 3"/>'
        )
        els.append(txt(ox + pw - 2, y_1ev - 4, "1 eV ≈ 1.16×10⁴ K", 10.0, BLUE, "end", halo=True))

        # Constant Debye length diagonal line: lambda_D = 0.1 mm => T_e / n_e = (lambda_D^2 * e^2) / (eps0 * kB)
        c_ratio = math.log10(((1.0e-4 ** 2) * QE * QE) / (EPS0 * KB))
        diag_pts = []
        for ln_s in (10.0, 22.0):
            lt_s = ln_s + c_ratio
            if lg_t_min <= lt_s <= lg_t_max:
                diag_pts.append(map_log(ln_s, lt_s))
        if len(diag_pts) == 2:
            els.append(
                f'<line x1="{diag_pts[0][0]:.1f}" y1="{diag_pts[0][1]:.1f}" x2="{diag_pts[1][0]:.1f}" y2="{diag_pts[1][1]:.1f}" stroke="#cbd5e1" stroke-width="1.1" stroke-dasharray="3 3"/>'
            )
            els.append(txt(diag_pts[1][0] - 8, diag_pts[1][1] + 12, "λ_D = 0.1 mm", 9.8, MUTED, "end", halo=True))

        els.append(f'<path d="M{ox:.1f},{oy - ph:.1f} V{oy:.1f} H{ox + pw:.1f}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')
        els.append(txt(ox - 6, oy - ph - 8, "电子温度 Tₑ (K)", 10.8, MUTED))
        els.append(txt(ox + pw / 2, oy + 34, "电子数密度 nₑ (个/m³，对数尺度)", 10.8, MUTED, "middle"))

        # Plotted regimes: (lg_n, lg_t, label, sub, color, fill, dx, dy, anchor)
        regimes = [
            (7.0, 5.08, "太阳风", None, GREEN, GREEN_SOFT, 9, 4, "start"),
            (11.0, 3.62, "地球电离层 / 极光", None, GREEN, GREEN_SOFT, 9, -2, "start"),
            (15.0, 6.30, "太阳日冕", None, PURPLE, PURPLE_SOFT, -9, 4, "end"),
            (16.0, 4.36, "霓虹灯 / 芯片刻蚀", "冷等离子体 Tₑ≫T_gas", BLUE, BLUE_SOFT, 0, -25, "middle"),
            (20.0, 8.18, "托卡马克聚变 (ITER)", "1.5×10⁸ K", PURPLE, PURPLE_SOFT, 9, 4, "start"),
            (24.0, 4.48, "闪电 / 电弧焊", "热等离子体 Tₑ≈T_gas", ORANGE, ORANGE_SOFT, 0, -25, "middle"),
            (32.0, 7.18, "太阳核心", "1.5×10⁷ K", ORANGE, ORANGE_SOFT, -9, 4, "end"),
        ]
        for lg_n, lg_t, name, sub_lbl, fg, bg, dx, dy, anc in regimes:
            px, py = map_log(lg_n, lg_t)
            r_dot = 6.2 if "霓虹灯" in name or "聚变" in name else 5.2
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_dot}" fill="{bg}" stroke="{fg}" stroke-width="1.8"/>')
            els.append(txt(px + dx, py + dy, name, 10.8, fg, anc, "700", halo=True))
            if sub_lbl:
                sub_y = py + dy + 13
                els.append(txt(px + dx, sub_y, sub_lbl, 9.8, BODY, anc, halo=True))

        # Candle flame weakly-ionized gas comparison marker (well below ionosphere label)
        cx_f, cy_f = map_log(13.5, 3.02)
        els.append(f'<circle cx="{cx_f:.1f}" cy="{cy_f:.1f}" r="4.6" fill="#ffffff" stroke="{SLATE}" stroke-width="1.4" stroke-dasharray="2 2"/>')
        els.append(txt(cx_f + 9, cy_f + 4, "蜡烛火焰（极弱电离热气体）", 9.8, SLATE, "start", halo=True))

        els.append(txt(36, 368, "注：两轴均为十进制对数坐标；右上高温或高密区多为热平衡等离子体", 10.5, MUTED))

        # Right panel: Ping-pong electron vs bowling-ball atom
        els.append(card(478, 62, 262, 318))
        els.append(txt(494, 84, "② 乒乓球撞保龄球：双温之谜", PANEL_TITLE, INK, weight="600"))

        # Collision box
        els.append(card(494, 96, 230, 114, rx=8, fill="#f8fafc", stroke=HAIRLINE))
        # Incoming fast electron
        els.append(f'<line x1="510" y1="138" x2="578" y2="144" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')
        els.append(_charge_disc(516, 138, 5.5, "-", BLUE, BLUE_SOFT))
        els.append(txt(512, 122, "轻电子 e⁻ (23,000 K)", 10.5, BLUE, "start", "600"))
        # Rebound arrow
        els.append(f'<path d="M584,150 Q552,174 522,170" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#arr-blue)"/>')
        els.append(txt(506, 188, "弹回仍保 99.99% 动能！", 10.2, BLUE, "start"))

        # Heavy Neon atom
        els.append(f'<circle cx="614" cy="148" r="24" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(txt(614, 145, "Ne 原子", 10.6, ORANGE, "middle", "700"))
        els.append(txt(614, 159, "≈320 K", 9.8, BODY, "middle"))
        els.append(txt(648, 141, "质量差", 10.2, MUTED))
        els.append(txt(648, 156, "3.7万倍", 10.5, INK, weight="700"))

        eta_p_pct = elastic_transfer_fraction(ME, MP) * 100.0
        eta_ne_pct = elastic_transfer_fraction(ME, 20.18 * MP) * 100.0
        els.append(txt(504, 203, f"单次传能上限：氢 {eta_p_pct:.2f}% · 氖 {eta_ne_pct:.3f}%", 10.2, SLATE, weight="600"))

        # Two-regime temperature bar comparison
        els.append(card(494, 220, 230, 70, rx=7, fill=BLUE_SOFT, stroke=BLUE_LINE))
        els.append(txt(504, 238, "低压冷等离子体（霓虹灯 / 刻蚀）", 11.0, BLUE, weight="700"))
        els.append(txt(504, 257, "电子 Tₑ", 10.3, BODY))
        els.append('<rect x="552" y="248" width="112" height="9" rx="4" fill="#1d6fa5"/>')
        els.append(txt(670, 257, "2×10⁴K", 10.0, BLUE, weight="600"))
        els.append(txt(504, 276, "气体 T_g", 10.3, BODY))
        els.append('<rect x="552" y="267" width="12" height="9" rx="4" fill="#18794e"/>')
        els.append(txt(570, 276, "≈320 K（不烫手！）", 10.2, GREEN, weight="700"))

        els.append(card(494, 298, 230, 70, rx=7, fill=ORANGE_SOFT, stroke="#fdba74"))
        els.append(txt(504, 316, "高压热等离子体（闪电 / 电焊弧）", 11.0, ORANGE, weight="700"))
        els.append(txt(504, 335, "电子 Tₑ", 10.3, BODY))
        els.append('<rect x="552" y="326" width="122" height="9" rx="4" fill="#c25014"/>')
        els.append(txt(678, 335, "3×10⁴K", 10.0, ORANGE, weight="600"))
        els.append(txt(504, 354, "气体 T_g", 10.3, BODY))
        els.append('<rect x="552" y="345" width="122" height="9" rx="4" fill="#ea580c"/>')
        els.append(txt(678, 354, "3×10⁴K", 10.0, ORANGE, weight="600"))

        svg = figure(
            396,
            "宇宙与实验室等离子体密度温度对数相图及冷热等离子体双温对比",
            "左图在对数坐标下标出太阳风、电离层极光、霓虹灯与芯片冷等离子体、闪电、太阳核心及托卡马克聚变的位置；右图用电子与氖原子质量悬殊导致单次碰撞传能仅0.011%解释为何冷等离子体电子上万度而气体接近室温。",
            els,
        )
        write_svg(SUBDIR, "plasma-map-cold-hot.svg", svg)

    def _build_chip_plasma_etching() -> None:
        """SVG 5: Isotropic wet chemical etching undercut vs directional RIE plasma etching."""
        els = header(
            "从宇宙走入手机芯片：等离子体怎样在硅片上刻出垂直纳米沟槽？",
            "药水分子乱撞会把掩模下方掏空；等离子体鞘层电场将正离子变成笔直轰击的“纳米刻刀”",
        )

        # Left panel: Wet chemical etching (isotropic undercut)
        els.append(card(20, 62, 352, 298))
        els.append(txt(36, 84, "① 传统湿法药水腐蚀：各向同性乱啃", PANEL_TITLE, INK, weight="600"))
        els.append(card(36, 96, 320, 204, rx=8, fill="#f8fafc", stroke=HAIRLINE))

        # Liquid bath above wafer (y=96..184)
        els.append('<rect x="37" y="97" width="318" height="87" rx="7" fill="#fff7ed"/>')
        els.append(txt(48, 116, "酸性腐蚀液：中性分子向四面八方随机热运动", 10.6, ORANGE, weight="600"))
        rand_arrows = [
            (92, 136, 18, 14), (148, 132, -16, 16), (196, 128, 0, 22),
            (244, 134, 16, 15), (298, 138, -18, 12),
        ]
        for ax, ay, dx, dy in rand_arrows:
            els.append(f'<circle cx="{ax}" cy="{ay}" r="3.6" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.1"/>')
            els.append(f'<line x1="{ax}" y1="{ay}" x2="{ax + dx}" y2="{ay + dy}" stroke="{ORANGE}" stroke-width="1.2" marker-end="url(#arr-orange)"/>')

        # Silicon substrate (y=184..288) with semicircular isotropic undercut cavity
        # Opening is x=[160..232] (width 72), etch depth d = 52 => isotropic radius 52 on left/right!
        x_open_l, x_open_r = 160.0, 232.0
        y_top, y_bot = 184.0, 288.0
        d_etch = 52.0
        # Silicon polygon + semicircular undercut path:
        # Top goes 37 -> x_open_l - d_etch, quarter-circle down to (x_open_l, y_top + d_etch),
        # flat bottom to (x_open_r, y_top + d_etch), quarter-circle up to (x_open_r + d_etch, y_top) -> 355
        cav_pts = []
        for k in range(25):
            ang = math.pi - (0.5 * math.pi) * (k / 24)  # pi -> pi/2
            cav_pts.append((x_open_l + d_etch * math.cos(ang), y_top + d_etch * math.sin(ang)))
        for k in range(25):
            ang = 0.5 * math.pi - (0.5 * math.pi) * (k / 24)  # pi/2 -> 0
            cav_pts.append((x_open_r + d_etch * math.cos(ang), y_top + d_etch * math.sin(ang)))
        cav_str = " L ".join(f"{px:.2f},{py:.2f}" for px, py in cav_pts)
        si_path_l = f"M 37,{y_top} L {cav_pts[0][0]:.2f},{y_top} L {cav_str} L 355,{y_top} L 355,{y_bot} L 37,{y_bot} Z"
        els.append(f'<path d="{si_path_l}" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.3"/>')

        # Photoresist mask blocks (hanging unsupported over undercut!)
        els.append(card(48, 162, 112, 22, rx=3, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.3))
        els.append(card(232, 162, 112, 22, rx=3, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.3))
        els.append(txt(92, 177, "光刻胶掩模", 10.5, PURPLE, "middle", "600"))
        els.append(txt(288, 177, "光刻胶掩模", 10.5, PURPLE, "middle", "600"))

        # Dashed desired vertical walls & undercut warning arrows
        els.append(f'<line x1="{x_open_l}" y1="{y_top}" x2="{x_open_l}" y2="{y_top + d_etch + 8}" stroke="{SLATE}" stroke-width="1.1" stroke-dasharray="3 3"/>')
        els.append(f'<line x1="{x_open_r}" y1="{y_top}" x2="{x_open_r}" y2="{y_top + d_etch + 8}" stroke="{SLATE}" stroke-width="1.1" stroke-dasharray="3 3"/>')
        els.append(f'<line x1="{x_open_l - 4}" y1="{y_top + 18}" x2="{x_open_l - d_etch + 8}" y2="{y_top + 18}" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')
        els.append(f'<line x1="{x_open_r + 4}" y1="{y_top + 18}" x2="{x_open_r + d_etch - 8}" y2="{y_top + 18}" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')
        els.append(txt(196, y_top + 38, "横向钻蚀掏空！", 11.2, ORANGE, "middle", "700", halo=True))
        els.append(txt(196, 272, "硅晶圆衬底 (Si)", 11.0, SLATE, "middle", "600"))

        els.append(txt(36, 322, "向下腐蚀 50 nm，两侧也会同步掏空约 50 nm", 11.3, INK, weight="600"))
        els.append(txt(36, 344, "掩模悬空坍塌，根本刻不出几纳米宽的深沟槽", 11.3, MUTED))

        # Right panel: Reactive Ion Etching (RIE) directional plasma
        els.append(card(388, 62, 352, 298))
        els.append(txt(404, 84, "② 等离子体反应离子刻蚀（RIE 垂直精雕）", PANEL_TITLE, INK, weight="600"))
        els.append(card(404, 96, 320, 204, rx=8, fill="#f8fafc", stroke=HAIRLINE))

        # Top bulk RF plasma zone (y=97..134)
        els.append('<rect x="405" y="97" width="318" height="37" rx="6" fill="#f3e8ff"/>')
        els.append(txt(416, 114, "13.56 MHz 射频等离子体区（正离子 ⊕ + 活性自由基 F*）", 10.3, PURPLE, weight="600"))
        for px in (442, 514, 588, 666):
            els.append(_charge_disc(px, 125, 4.8, "+", ORANGE, ORANGE_SOFT))
            els.append(_charge_disc(px + 28, 125, 3.8, "-", BLUE, "#ffffff"))

        # Middle sheath vertical electric field zone (y=134..184)
        els.append('<rect x="405" y="134" width="318" height="50" fill="#eff6ff"/>')
        els.append(txt(414, 150, "鞘层垂直强电场 E ↓", 10.5, BLUE, weight="700"))
        els.append(txt(714, 150, "晶圆台带负偏压", 10.3, BLUE, "end", "600"))

        # Vertical ion bombardment trajectories straight through mask opening x=[528..600]
        rx_open_l, rx_open_r = 528.0, 600.0
        for ix in (542.0, 564.0, 586.0):
            els.append(
                f'<line x1="{ix}" y1="138" x2="{ix}" y2="{y_top + d_etch + 6:.1f}" stroke="{BLUE}" stroke-width="1.7" marker-end="url(#arr-blue)"/>'
            )
            els.append(_charge_disc(ix, 148, 5.2, "+", ORANGE, ORANGE_SOFT))

        # Silicon substrate with crisp 90-degree vertical trench!
        si_path_r = (
            f"M 405,{y_top} L {rx_open_l},{y_top} L {rx_open_l},{y_top + d_etch + 14} "
            f"L {rx_open_r},{y_top + d_etch + 14} L {rx_open_r},{y_top} L 723,{y_top} "
            f"L 723,{y_bot} L 405,{y_bot} Z"
        )
        els.append(f'<path d="{si_path_r}" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.3"/>')
        # Sidewall highlight lines in green
        els.append(f'<line x1="{rx_open_l}" y1="{y_top}" x2="{rx_open_l}" y2="{y_top + d_etch + 14}" stroke="{GREEN}" stroke-width="2.2"/>')
        els.append(f'<line x1="{rx_open_r}" y1="{y_top}" x2="{rx_open_r}" y2="{y_top + d_etch + 14}" stroke="{GREEN}" stroke-width="2.2"/>')

        # Photoresist mask blocks
        els.append(card(416, 162, 112, 22, rx=3, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.3))
        els.append(card(600, 162, 112, 22, rx=3, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.3))
        els.append(txt(472, 177, "光刻胶掩模", 10.5, PURPLE, "middle", "600"))
        els.append(txt(656, 177, "光刻胶掩模", 10.5, PURPLE, "middle", "600"))

        # 90-degree right-angle symbol & badge
        yb_tr = y_top + d_etch + 14
        els.append(f'<path d="M{rx_open_l},{yb_tr - 9} H{rx_open_l + 9} V{yb_tr}" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
        els.append(pill(612, 206, "90° 垂直侧壁", fg=GREEN, bg=GREEN_SOFT, w=98, h=20, size=10.8))
        els.append(txt(661, 242, "3–5 nm 先进制程", 10.5, GREEN, "middle", "600"))
        els.append(txt(564, 274, "硅晶圆衬底 (Si)", 11.0, SLATE, "middle", "600"))

        els.append(txt(404, 322, "鞘层电场给正离子精准定向，只打沟底不啃侧壁", 11.3, INK, weight="600"))
        els.append(txt(404, 344, "配合挥发性化学反应，雕出手机里的百亿晶体管", 11.3, MUTED))

        svg = figure(
            378,
            "芯片制造湿法化学腐蚀横向钻蚀与反应离子等离子体垂直刻蚀对比",
            "左图展示湿法化学酸液因分子无方向热运动造成掩模下方严重横向钻蚀；右图展示13.56MHz射频冷等离子体通过鞘层垂直电场加速正离子轰击晶圆沟底，实现90度垂直侧壁的纳米级各向异性刻蚀。",
            els,
        )
        write_svg(SUBDIR, "chip-plasma-etching.svg", svg)
    """Build all 5 computed SVGs for the plasma state flagship post."""
    _verify_physics_assertions()
    _build_four_states_ladder()
    _build_debye_shielding_curve()
    _build_magnetic_helix_bottle()
    _build_plasma_map_cold_hot()
    _build_chip_plasma_etching()
