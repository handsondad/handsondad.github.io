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

    def fig_smile_brain_reward():
        # Strathearn et al. (2008, Pediatrics, N=28 first-time mothers fMRI): own-happy > own-neutral > own-sad in nigrostriatal dopamine reward areas
        # Addyman (2018, Goldsmiths Baby Laughter Survey, N=390 parents): ~70% laugh out loud at Peekaboo, ~2x funnier than prop gags
        peekaboo_pct = 70.0
        assert 65.0 <= peekaboo_pct <= 75.0

        els = header(
            "为什么宝宝一笑大人就“满血复活”？杜氏微笑解剖、多巴胺回路与婴儿幽默排行榜",
            "左图结合杜氏微笑（Duchenne Smile）与 Strathearn（2008）fMRI 研究；右图展示伦敦大学金史密斯学院婴儿笑声调查。",
        )
        # Left card: Duchenne smile + fMRI dopamine reward
        els.append(card(20, 62, 356, 256))
        els.append(txt(36, 85, "① 弯成月牙的眼睛 + 大脑多巴胺“充电宝”", 12.4, INK, weight="700"))

        # Stylized smiling baby face diagram on top-left
        fcx, fcy = 92, 146
        els.append(f'<circle cx="{fcx}" cy="{fcy}" r="36" fill="#fff7ed" stroke="{ORANGE}" stroke-width="1.6"/>')
        # Crescent eyes (orbicularis oculi)
        els.append(f'<path d="M{fcx - 18},{fcy - 6} Q{fcx - 11},{fcy - 14} {fcx - 4},{fcy - 6}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
        els.append(f'<path d="M{fcx + 4},{fcy - 6} Q{fcx + 11},{fcy - 14} {fcx + 18},{fcy - 6}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
        # Rosy cheeks + wide smile (zygomaticus major)
        els.append(f'<circle cx="{fcx - 19}" cy="{fcy + 5}" r="5" fill="#fda4af" opacity="0.55"/>')
        els.append(f'<circle cx="{fcx + 19}" cy="{fcy + 5}" r="5" fill="#fda4af" opacity="0.55"/>')
        els.append(f'<path d="M{fcx - 13},{fcy + 8} Q{fcx},{fcy + 22} {fcx + 13},{fcy + 8}" fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-linecap="round"/>')

        els.append(txt(144, 122, "• 眼轮匝肌收缩 → 眼睛弯成两道月牙", 10.6, BLUE, weight="700"))
        els.append(txt(144, 142, "  （很难靠意志假装的“杜氏真笑”标志）", 10.2, MUTED))
        els.append(txt(144, 164, "• 颧大肌上提 → 嘴角翘起发出社交邀请", 10.6, ORANGE, weight="700"))

        els.append(card(36, 196, 324, 108, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(48, 216, "Strathearn 等（2008，Pediatrics）脑成像发现：", 11.0, BLUE, weight="700"))
        els.append(txt(48, 237, "• 28 位新手妈妈看自家 5–10 月龄宝宝照片时：", 10.4, BODY))
        els.append(txt(48, 256, "• 唯有“开心笑脸”特异性点亮黑质—纹状体多巴胺奖赏区", 10.4, INK, weight="700"))
        els.append(txt(48, 275, "  （开心 > 平静 > 哭泣），从生理层面帮疲惫父母“回血”！", 10.3, BODY))

        # Right card: Goldsmiths Baby Laughter Project (Addyman)
        els.append(card(388, 62, 352, 256))
        els.append(txt(404, 85, "② 什么最能逗笑宝宝？（伦敦大学 390 家庭实测）", 12.2, INK, weight="700"))

        games = [
            ("双手躲猫猫（Peekaboo）", 70, GREEN, "冠军！纯眼神全神贯注连接"),
            ("挠痒痒 / 身体轻触游戏", 52, BLUE, "触觉预期与悬念感"),
            ("把杯子顶在头上装傻", 38, ORANGE, "温和打破日常规则的反差"),
            ("拿猫咪玩偶学小狗“汪汪”", 34, PURPLE, "概念错位（大一点更爱笑）"),
        ]
        for idx, (gname, pct, col, note) in enumerate(games):
            ry = 104 + idx * 42
            els.append(txt(404, ry + 11, gname, 10.6, INK, weight="600"))
            bw = (pct / 80.0) * 188.0
            els.append(f'<rect x="404" y="{ry + 17}" width="{bw:.1f}" height="12" rx="6" fill="{col}" opacity="0.85"/>')
            els.append(txt(404 + bw + 6, ry + 27, f"~{pct}%  {note}", 9.8, MUTED))

        els.append(card(404, 274, 320, 32, rx=6, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(564, 294, "Addyman 核心结论：逗笑宝宝的秘诀不是道具，是 100% 在场的专注！", 10.2, GREEN, "middle", weight="700"))

        return figure(
            334,
            "杜氏微笑肌肉特征与父母多巴胺奖赏回路及婴儿笑声排行榜",
            "左图解析眼轮匝肌与颧大肌共同构成的杜氏真笑及2008年Pediatrics脑成像发现的多巴胺奖赏激活；右图展示伦敦大学金史密斯学院婴儿笑声项目中躲猫猫约70%放声大笑率。",
            els,
        )

    def fig_proto_conversation_rhythm():
        els = header(
            "开口说话前，宝宝早就懂“聊天节奏”了：乒乓式留白对话 vs 连珠炮式抢话",
            "把每一次微笑和“啊—哦”当成一拍音乐：大人留出 1–2 秒空白，宝宝才会把下一球发回来。",
        )
        # Top track: Healthy Turn-Taking ("Proto-conversation")
        els.append(card(20, 62, 720, 118))
        els.append(txt(36, 84, "① 健康的“原初对话（Proto-conversation）”：一发一回，中间留出等待空白", 12.2, GREEN, weight="700"))
        t0, sc = 56, 76.0  # 0..8.5 seconds across 646px
        els.append(f'<line x1="{t0}" y1="138" x2="{t0 + 8.5 * sc:.1f}" y2="138" stroke="{HAIRLINE}" stroke-width="1.4"/>')
        turns_good = [
            (0.15, 1.15, "宝宝：凝视+笑", ORANGE, ORANGE_SOFT),
            (1.35, 2.65, "爸妈：“醒啦！”", BLUE, BLUE_SOFT),
            (2.85, 4.25, "留白 1.5s 等他接", GREEN, GREEN_SOFT),
            (4.45, 5.55, "宝宝：“啊—咕！”", ORANGE, ORANGE_SOFT),
            (5.75, 7.05, "爸妈模仿回应", BLUE, BLUE_SOFT),
            (7.25, 8.35, "宝宝咯咯大笑!", ORANGE, ORANGE_SOFT),
        ]
        for s0, s1, lbl, col, bg in turns_good:
            x0, w = t0 + s0 * sc, (s1 - s0) * sc
            els.append(f'<rect x="{x0:.1f}" y="102" width="{w:.1f}" height="28" rx="6" fill="{bg}" stroke="{col}" stroke-width="1.4"/>')
            els.append(txt(x0 + w / 2, 120, lbl, 10.0, col, "middle", weight="700"))
        els.append(txt(36, 164, "效果：宝宝发现“我的声音和笑容能改变大人的反应！” → 轮流对话与语言神经回路高速连线。", 10.5, BODY))

        # Bottom track: Overwhelming Adult Monologue
        els.append(card(20, 192, 720, 112))
        els.append(txt(36, 214, "② 成人“播音员式连珠炮”：全程塞满无留白 → 宝宝过载扭头断开连接", 12.2, ORANGE, weight="700"))
        els.append(f'<line x1="{t0}" y1="264" x2="{t0 + 8.5 * sc:.1f}" y2="264" stroke="{HAIRLINE}" stroke-width="1.4"/>')
        els.append(f'<rect x="{t0 + 0.2 * sc:.1f}" y="230" width="{5.8 * sc:.1f}" height="28" rx="6" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.4"/>')
        els.append(txt(t0 + 3.1 * sc, 248, "大人连问：“看这是啥？红球！圆不圆？跟爸爸念球球！怎么不笑呀？看镜头！”", 10.1, ORANGE, "middle", weight="600"))
        els.append(f'<rect x="{t0 + 6.2 * sc:.1f}" y="230" width="{2.1 * sc:.1f}" height="28" rx="6" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.3"/>')
        els.append(txt(t0 + 7.25 * sc, 248, "宝宝：扭头/打哈欠避开", 10.1, SLATE, "middle", weight="700"))
        els.append(txt(36, 288, "提醒：宝宝移开视线不是“不理人”，而是大脑在给自己降温减负——停下来安静抱抱就是最好回应。", 10.5, MUTED))

        return figure(
            320,
            "婴儿原初对话轮流留白节拍与成人连珠炮单向输出对比",
            "上图展示0至8.5秒内宝宝发球、父母回应、留白1.5秒等待宝宝再发声的良性对话节拍；下图对比成人连续发问无留白导致婴儿感官过载移开视线。",
            els,
        )

    def fig_thelen_stepping_buoyancy():
        # Esther Thelen, Fisher & Ridley-Johnson (1984, Infant Behavior and Development, 7(4), 479-493)
        els = header(
            "为什么出生会“踏步”的宝宝两个月大突然不迈腿了？Thelen 经典水缸浮力实验",
            "1984 年发展心理学家 Esther Thelen 用三个巧妙对照证明：不是大脑指令退化了，是小胖腿长太快了！",
        )
        cols = [
            (
                20,
                "① 谜题：2 个月踏步“消失”",
                SLATE,
                SLATE_SOFT,
                [
                    "• 刚出生扶着腋下脚沾地，宝宝会",
                    "  像模像样交替迈步（踏步反射）",
                    "• 到约 2 个月大，突然迈不动了！",
                    "• 旧教科书误以为：大脑皮层抑制",
                    "  了低级反射，得等近一岁重学。",
                    "• Thelen 发现：长胖最快的宝宝，",
                    "  踏步消失得最早！难道是腿太沉？",
                ],
            ),
            (
                264,
                "② 验证一：脚踝绑小沙袋",
                ORANGE,
                ORANGE_SOFT,
                [
                    "• 给原本还能欢快踏步的 1 月龄",
                    "  瘦宝宝，脚踝贴上几克安全配重",
                    "  （模拟 2 月龄长出的大腿脂肪）",
                    "• 结果：原本能迈步的宝宝，当场",
                    "  也抬不起腿、步数骤减！",
                    "→ 证明腿部重量与肌力的比例，",
                    "  直接卡住了动作表现！",
                ],
            ),
            (
                508,
                "③ 验证二：放进温水缸借浮力!",
                GREEN,
                GREEN_SOFT,
                [
                    "• 把已经“不会踏步”的胖乎乎",
                    "  宝宝抱进齐腰深的温暖水缸里",
                    "• 水的浮力刚一托起沉甸甸的小胖",
                    "  腿，奇迹出现了——",
                    "• 消失的交替踏步当场满血复活！",
                    "→ 大脑根本没忘！只是等肌肉力量",
                    "  慢慢追上体重，动作自然水到渠成。",
                ],
            ),
        ]
        for cx, ctitle, col, bg, lines in cols:
            els.append(card(cx, 62, 232, 244, fill="#ffffff", stroke=BORDER))
            els.append(card(cx + 12, 74, 208, 30, rx=7, fill=bg, stroke=col))
            els.append(txt(cx + 116, 94, ctitle, 11.4, col, "middle", weight="700"))
            for i, ln in enumerate(lines):
                is_hi = ln.startswith("→") or "满血复活" in ln
                els.append(txt(cx + 14, 128 + i * 24, ln, 10.4, col if is_hi else BODY, weight="700" if is_hi else None))

        return figure(
            322,
            "Thelen婴儿踏步反射消失与温水浮力恢复三步实验图解",
            "三栏重现1984年Esther Thelen经典实验：2月龄踏步消失与体重增长相关、瘦婴儿脚踝加配重踏步减少、胖婴儿入温水借浮力立即恢复踏步，说明动作发育是神经、肌肉、体重与环境的动力系统协同。",
            els,
        )

    def fig_sleep_and_language_iceberg():
        # Left: Henderson et al. (2010, Pediatrics, N=75 videosomnography + diaries, Criterion 3: 22:00-06:00 unbroken):
        # 1m ~5%, 3m ~32%, 5m ~52% (>50% milestone!), 9m ~68%, 12m: 54/75 = 72.0% met, 21/75 = 28.0% STILL NOT MET!
        met_12m = (75 - 21) / 75.0 * 100.0
        unmet_12m = 21 / 75.0 * 100.0
        assert abs(met_12m - 72.0) < 1e-9 and abs(unmet_12m - 28.0) < 1e-9

        els = header(
            "最磨人的两件大事：为什么满周岁还有近三成健康宝宝夜醒？为什么“听懂”远早于“开口”？",
            "左图据 Pediatrics（2010）实测绘出整夜觉达标曲线；右图展示“水下理解词库”托起“水上开口爆发”的语言冰山。",
        )
        # Left card: Henderson 2010 Sleep curve (x=20, w=362)
        els.append(card(20, 62, 362, 256))
        els.append(txt(36, 85, "① 睡整觉实测（22:00–06:00 连续不醒比例）", 12.2, INK, weight="700"))
        ox, oy, pw, ph = 68, 256, 286.0, 142.0
        els.append(f'<line x1="{ox}" y1="{oy - ph}" x2="{ox}" y2="{oy}" stroke="{SLATE}" stroke-width="1.3"/>')
        els.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + pw}" y2="{oy}" stroke="{SLATE}" stroke-width="1.3"/>')
        for pct_y in (0, 50, 100):
            yy = oy - (pct_y / 100.0) * ph
            els.append(f'<line x1="{ox}" y1="{yy:.1f}" x2="{ox + pw}" y2="{yy:.1f}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
            els.append(txt(ox - 6, yy + 4, f"{pct_y}%", 9.8, MUTED, "end"))

        pts_sleep = [(1, 6), (2, 18), (3, 35), (4, 46), (5, 53), (6, 58), (9, 67), (12, 72)]
        poly = []
        for m, p in pts_sleep:
            px = ox + ((m - 1) / 11.0) * pw
            py = oy - (p / 100.0) * ph
            poly.append(f"{px:.1f},{py:.1f}")
        els.append(f'<polyline points="{" ".join(poly)}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>')
        for m in (1, 3, 5, 9, 12):
            px = ox + ((m - 1) / 11.0) * pw
            els.append(txt(px, oy + 15, f"{m}月", 9.8, MUTED, "middle"))
        # Highlight 12m = 72% (meaning 28% = 21/75 still wake!)
        x12, y12 = ox + pw, oy - 0.72 * ph
        els.append(f'<circle cx="{x12:.1f}" cy="{y12:.1f}" r="4.5" fill="{ORANGE}" stroke="#fff" stroke-width="1.2"/>')
        els.append(txt(x12 - 6, y12 - 10, "12月龄：72% 达标（仍有 28% 健康宝宝夜醒！）", 10.0, ORANGE, "end", weight="700", halo=True))
        els.append(txt(36, 296, "来源：Henderson 等（2010，N=75 红外录像校验）——夜醒≠睡眠故障！", 10.0, MUTED))

        # Right card: Receptive vs Expressive Vocabulary Iceberg (x=394, w=346)
        els.append(card(394, 62, 346, 256))
        els.append(txt(410, 85, "② 语言发育的“冰山定律”：先攒水下，再冒水面", 12.2, INK, weight="700"))
        # Waterline at y=162
        els.append(f'<rect x="410" y="162" width="314" height="108" rx="8" fill="{BLUE_SOFT}"/>')
        els.append(f'<line x1="410" y1="162" x2="724" y2="162" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="5 3"/>')
        els.append(txt(718, 155, "水面：外人听得见的“开口说”", 9.8, ORANGE, "end", weight="700"))
        # Tip above water
        els.append(f'<polygon points="530,162 594,162 562,116" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(txt(486, 134, "表达词汇（说得出）", 10.5, ORANGE, "end", weight="700"))
        els.append(txt(486, 150, "12月仅几词 → 18–24月爆发", 9.8, BODY, "end"))
        # Huge base below water
        els.append(f'<polygon points="518,164 606,164 656,258 468,258" fill="#bfdbfe" stroke="{BLUE}" stroke-width="1.6"/>')
        els.append(txt(562, 196, "水下巨型底座：理解词汇（听得懂）", 11.0, BLUE, "middle", weight="700"))
        els.append(txt(562, 217, "• 8–12月：还不会说，已听懂几十个日常词与手势", 10.1, INK, "middle"))
        els.append(txt(562, 236, "• 约 14 月：常能听懂 50–100+ 词，嘴上只蹦几个词", 10.1, INK, "middle"))
        els.append(txt(410, 294, "观察重点：先看他能不能听懂指认、眼神交流，不只数会背几个词！", 10.1, GREEN, weight="700"))

        return figure(
            334,
            "婴儿周岁整夜觉达标比例曲线与语言理解表达冰山模型",
            "左图依据2010年Pediatrics纵向研究展示1至12月龄22点至早6点连续睡眠比例（满12月仍有28%健康婴儿未达标）；右图用冰山模型对比水下庞大理解词汇与水上延迟爆发的口语表达词汇。",
            els,
        )

    def fig_kuhl_live_vs_video():
        # Exact data from Kuhl, Tsao & Liu (2003, PNAS 100(15): 9096-9101, PMC166444):
        # Live Mandarin: 65.7% (SE 2.40), English Control: 56.7% (SE 2.29)
        # Mandarin DVD AV & Audio-only: no learning, statistically indistinguishable from English Control (~58.0% / ~54.5%, P > 0.10; < Live P < 0.01)
        live_m = 65.7
        ctrl_e = 56.7
        assert live_m - ctrl_e == 9.0

        els = header(
            "顶级期刊实验：为什么再高清的早教视频，也替代不了真人在身边讲 15 分钟绘本？",
            "华盛顿大学 Patricia Kuhl 团队（2003，PNAS）对 9 月龄婴儿的普通话语音辨别对照实验。",
        )
        # Left card: Bar chart of Kuhl 2003 PNAS (x=20, w=390)
        els.append(card(20, 62, 390, 256))
        els.append(txt(36, 85, "① 同样听 12 次普通话故事，谁真正学会了辨音？", 12.2, INK, weight="700"))
        ox, oy, pw, ph = 66, 256, 322.0, 140.0
        els.append(f'<line x1="{ox}" y1="{oy - ph}" x2="{ox}" y2="{oy}" stroke="{SLATE}" stroke-width="1.3"/>')
        els.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + pw}" y2="{oy}" stroke="{SLATE}" stroke-width="1.3"/>')
        # Y scale from 50% (random chance!) to 70%
        for py_val in (50, 55, 60, 65, 70):
            yy = oy - ((py_val - 50.0) / 20.0) * ph
            els.append(f'<line x1="{ox}" y1="{yy:.1f}" x2="{ox + pw}" y2="{yy:.1f}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
            els.append(txt(ox - 6, yy + 4, f"{py_val}%", 9.8, MUTED, "end"))

        bars = [
            ("真人面对面共读", 65.7, GREEN, "65.7%（追平台北母语宝宝！）"),
            ("高清电视录像 DVD", 58.0, ORANGE, "无显著学习（与对照无差异）"),
            ("纯音频播放", 54.8, SLATE, "无显著学习（接近盲猜 50%）"),
            ("纯英语对照组", 56.7, BLUE, "56.7%（未接触普通话基线）"),
        ]
        for i, (blbl, bval, bcol, btag) in enumerate(bars):
            bx = ox + 16 + i * 76
            bh = ((bval - 50.0) / 20.0) * ph
            by = oy - bh
            els.append(f'<rect x="{bx}" y="{by:.1f}" width="46" height="{bh:.1f}" rx="5" fill="{bcol}" opacity="0.85"/>')
            els.append(txt(bx + 23, by - 7, f"{bval:.1f}%" if i in (0, 3) else "无提升", 10.2, bcol, "middle", weight="700"))
            els.append(txt(bx + 23, oy + 16, blbl[:4], 9.8, INK, "middle", weight="600"))
            els.append(txt(bx + 23, oy + 30, blbl[4:], 9.5, MUTED, "middle"))

        els.append(txt(36, 304, "注：50% 为随机转头基线；电视组听到的音节数（4.99万）甚至比真人组（3.31万）还多！", 9.8, MUTED))

        # Right card: Social Gating mechanism (x=422, w=318)
        els.append(card(422, 62, 318, 256))
        els.append(txt(438, 85, "② 为什么录播失灵？“社交门控”假说", 12.2, INK, weight="700"))

        els.append(card(438, 102, 286, 94, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(450, 122, "真人互动：共同注意（Joint Attention）开锁", 11.0, GREEN, weight="700"))
        els.append(txt(450, 143, "• 大人说“小火车”时低头看玩具，宝宝顺着大人的", 10.3, BODY))
        els.append(txt(450, 161, "  视线锁定目标 → 声音与实物瞬间精准绑定！", 10.3, BODY))
        els.append(txt(450, 180, "• 眼神回应点亮社交唤醒度（专注分高达 3.53/5）", 10.3, INK, weight="700"))

        els.append(card(438, 206, 286, 98, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(450, 226, "屏幕播放：没有回应的“单向像素墙”", 11.0, ORANGE, weight="700"))
        els.append(txt(450, 247, "• 屏幕里的人不会等宝宝看过来再开口，也不会顺着", 10.3, BODY))
        els.append(txt(450, 265, "  宝宝的手指回应（音频组专注分跌至 1.48/5）", 10.3, BODY))
        els.append(txt(450, 284, "→ 早期语言与认知的大门，钥匙握在活生生的人手里！", 10.2, ORANGE, weight="700"))

        return figure(
            334,
            "Kuhl婴儿外语语音学习真人互动对比高清视频实验结果与社交门控机制",
            "左图绘制2003年PNAS实验数据：9月龄美国婴儿经12次真人普通话互动后辨音准确率达65.7%显著高于英语对照56.7%，而高清DVD视频组与纯音频组均无学习效果；右图解释共同注意与社交门控机制。",
            els,
        )

    def fig_desirable_difficulty_retention():
        # Roediger & Karpicke (2006, Psychological Science, 17(3), 249-255, Exp 1 prose recall):
        # Study-Study (repeated passive reading): 5-min test = 81%, 2-day = 54%, 1-week = 42%
        # Study-Test (active retrieval without answer): 5-min test = 75%, 2-day = 68%, 1-week = 56%
        ss = [(0, 81), (1, 54), (2, 42)]
        st = [(0, 75), (1, 68), (2, 56)]
        assert ss[0][1] > st[0][1] and st[2][1] > ss[2][1]  # Exact crossover!

        els = header(
            "为什么 AI“秒给答案”越顺滑，大脑反而忘得越快？合意困难与记忆反转曲线",
            "据 Roediger & Karpicke（2006，Psychological Science）经典实验绘制：省力重读 vs 费力回想。",
        )
        # Left card: Crossover retention curve (x=20, w=380)
        els.append(card(20, 62, 380, 254))
        els.append(txt(36, 85, "① 5 分钟后的“学会错觉” vs 一周后的“真本事”", 12.2, INK, weight="700"))
        ox, oy, pw, ph = 72, 254, 294.0, 140.0
        els.append(f'<line x1="{ox}" y1="{oy - ph}" x2="{ox}" y2="{oy}" stroke="{SLATE}" stroke-width="1.3"/>')
        els.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + pw}" y2="{oy}" stroke="{SLATE}" stroke-width="1.3"/>')
        for yv in (30, 50, 70, 90):
            yy = oy - ((yv - 30.0) / 60.0) * ph
            els.append(f'<line x1="{ox}" y1="{yy:.1f}" x2="{ox + pw}" y2="{yy:.1f}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')
            els.append(txt(ox - 6, yy + 4, f"{yv}%", 9.8, MUTED, "end"))

        xs = [ox + 24, ox + pw * 0.5, ox + pw - 24]
        xlbls = ["5 分钟后测", "2 天后测", "1 周后测"]
        for xi, xl in zip(xs, xlbls):
            els.append(txt(xi, oy + 18, xl, 10.2, INK, "middle", weight="600"))

        def pts_str(arr):
            return " ".join(f"{xs[i]:.1f},{oy - ((v - 30.0) / 60.0) * ph:.1f}" for i, v in arr)

        els.append(f'<polyline points="{pts_str(ss)}" fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-dasharray="5 3"/>')
        els.append(f'<polyline points="{pts_str(st)}" fill="none" stroke="{GREEN}" stroke-width="2.5"/>')
        for i, v in ss:
            yy = oy - ((v - 30.0) / 60.0) * ph
            els.append(f'<circle cx="{xs[i]:.1f}" cy="{yy:.1f}" r="4" fill="{ORANGE}"/>')
            els.append(txt(xs[i] + (10 if i else 0), yy + (-8 if i == 0 else 15), f"{v}%", 10.0, ORANGE, "middle", weight="700"))
        for i, v in st:
            yy = oy - ((v - 30.0) / 60.0) * ph
            els.append(f'<circle cx="{xs[i]:.1f}" cy="{yy:.1f}" r="4.5" fill="{GREEN}"/>')
            els.append(txt(xs[i], yy + (16 if i == 0 else -9), f"{v}%", 10.2, GREEN, "middle", weight="700"))

        els.append(txt(240, 126, "主动费力回想组（一周仍留存 56%！）", 10.2, GREEN, "middle", weight="700", halo=True))
        els.append(txt(256, 224, "顺滑反复看答案组（掉到 42%）", 10.2, ORANGE, "middle", weight="700", halo=True))
        els.append(txt(36, 298, "反转真相：反复看答案组考前自信心更高，一周后却忘掉近一半！", 10.0, MUTED))

        # Right card: Desirable Difficulty workflow at home (x=412, w=328)
        els.append(card(412, 62, 328, 254))
        els.append(txt(428, 85, "② 给家庭加一点“合意困难（Desirable Difficulty）”", 11.8, INK, weight="700"))
        cards_r = [
            (102, ORANGE, ORANGE_SOFT, "警惕“流畅性错觉（Fluency Illusion）”", "看着 AI 秒写出的漂亮解析连连点头：“看懂了！”", "其实只调用了短期识别，没在脑中刻下提取路径。"),
            (176, BLUE, BLUE_SOFT, "第一步：合上书/关掉屏幕“硬憋三分钟”", "先用自己的歪扭画图或大白话猜一遍、讲给爸妈听；", "哪怕猜错了，卡壳本身就在给神经元涂“助焊剂”！"),
            (250, GREEN, GREEN_SOFT, "第二步：再用工具对照，找“我漏了哪一步”", "把 AI 从“替身枪手”降级成“对答案时的陪练”，", "亲手合上书重讲一遍才算真正装进自己脑子里。"),
        ]
        for cy_r, col, bg, h_txt, l1, l2 in cards_r:
            els.append(card(428, cy_r, 296, 62, rx=8, fill=bg, stroke=col))
            els.append(txt(440, cy_r + 18, h_txt, 10.8, col, weight="700"))
            els.append(txt(440, cy_r + 36, l1, 10.1, BODY))
            els.append(txt(440, cy_r + 52, l2, 10.1, BODY))

        return figure(
            332,
            "被动重读与主动检索记忆留存反转曲线及AI时代合意困难学习法",
            "左图依据2006年Roediger与Karpicke实验绘出5分钟后被动重读81%略高但一周后主动检索56%大幅反超被动重读42%的交叉曲线；右图给出避免AI流畅性错觉的三步家庭实践。",
            els,
        )

    for fname, content in (
        ("prenatal-senses", fig_prenatal_senses()),
        ("baby-perspective", fig_baby_perspective()),
        ("emotion-repair-loop", fig_emotion_repair_loop()),
        ("smile-serve-return", fig_smile_serve_return()),
        ("smile-brain-reward", fig_smile_brain_reward()),
        ("proto-conversation-rhythm", fig_proto_conversation_rhythm()),
        ("who-motor-windows", fig_who_motor_windows()),
        ("thelen-stepping-buoyancy", fig_thelen_stepping_buoyancy()),
        ("sleep-and-language-iceberg", fig_sleep_and_language_iceberg()),
        ("child-24h-executive", fig_child_24h_executive()),
        ("kuhl-live-vs-video", fig_kuhl_live_vs_video()),
        ("desirable-difficulty-retention", fig_desirable_difficulty_retention()),
        ("wing-lift-stall", fig_wing_lift_stall()),
        ("newton-cannon-orbits", fig_newton_cannon_orbits()),
        ("sun-mass-thermostat", fig_sun_mass_thermostat()),
        ("photon-random-walk", fig_photon_random_walk()),
        ("lunar-leap-zhongqi", fig_lunar_leap_zhongqi()),
        ("synodic-fullmoon-16", fig_synodic_fullmoon_16()),
    ):
        write_svg(SUB, fname, content)
    print("Generated 18 early-curiosity SVGs; all WHO, PNAS, Pediatrics, orbital, nuclear, and calendar assertions passed.")

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

def _register_flight_and_sun():
    import math

    import re

    import xml.etree.ElementTree as ET

    from html import escape

    from .core import BG, BLUE, BLUE_LINE, BLUE_SOFT, BODY, BORDER, CARD_BG, GREEN, GREEN_SOFT, HAIRLINE, IMAGES_ROOT, INK, LABEL_SIZE, MUTED, NOTE_SIZE, ORANGE, ORANGE_SOFT, PANEL_TITLE, PURPLE, PURPLE_SOFT, REPO_ROOT, SLATE, SLATE_SOFT, SUB_SIZE, TITLE_SIZE, WIDTH, audit_all_svgs, card, figure, header, pill, register, std_defs, step_badge, txt, write_svg

    RED = "#b91c1c"

    RED_SOFT = "#fef2f2"

    GOLD = "#b45309"

    GOLD_SOFT = "#fffbeb"

    def _poly(pts, stroke=BLUE, sw=2.2, fill="none", dash=None, cls=None, extra=""):
        pts_s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d_attr = f' stroke-dasharray="{dash}"' if dash else ""
        c_attr = f' class="{cls}"' if cls else ""
        ex = f" {extra.strip()}" if extra.strip() else ""
        return (
            f'<polyline points="{pts_s}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{d_attr}{c_attr}{ex}/>'
        )

    def _naca_cambered_pts(x0, y0, chord, alpha_deg=6.5, m=0.05, p=0.4, t=0.13, n=60):
        """Compute NACA 4-digit cambered airfoil polygon rotated by angle of attack alpha_deg."""
        upper = []
        lower = []
        rad = math.radians(alpha_deg)
        ca, sa = math.cos(rad), math.sin(rad)

        for i in range(n + 1):
            beta = math.pi * i / n
            xc = 0.5 * (1.0 - math.cos(beta))
            yt = 5.0 * t * (
                0.2969 * math.sqrt(max(xc, 0.0))
                - 0.1260 * xc
                - 0.3516 * xc**2
                + 0.2843 * xc**3
                - 0.1036 * xc**4
            )
            if xc < p:
                yc = (m / p**2) * (2 * p * xc - xc**2)
                dyc = (2 * m / p**2) * (p - xc)
            else:
                yc = (m / (1 - p) ** 2) * ((1 - 2 * p) + 2 * p * xc - xc**2)
                dyc = (2 * m / (1 - p) ** 2) * (p - xc)
            th = math.atan(dyc)
            xu, yu = xc - yt * math.sin(th), yc + yt * math.cos(th)
            xl, yl = xc + yt * math.sin(th), yc - yt * math.cos(th)

            # Rotate around quarter-chord (0.25, 0) in screen coords (y down, nose up means leading edge higher -> y smaller)
            def _rot(px, py):
                dx = px - 0.25
                dy = py
                rx = 0.25 + dx * ca + dy * sa
                ry = -dx * sa + dy * ca
                return x0 + rx * chord, y0 - ry * chord

            upper.append(_rot(xu, yu))
            lower.append(_rot(xl, yl))

        pts = upper + list(reversed(lower[1:-1]))
        return pts, upper, lower

    @register("flight-physics", "飞行物理：等时间谬误辟谣、升力速度高度权衡、直升机反扭矩与跨尺度飞行图谱", "mechanics_sky")
    def build_flight_physics():
        subdir = "flight-physics"

        # -----------------------------------------------------------------------
        # 1. equal-transit-myth.svg
        # -----------------------------------------------------------------------
        def build_equal_transit():
            els = []
            els += header(
                "升力第一大误区：机翼上下的空气，根本不会“约好在尾缘重逢”！",
                "左图拆解流传最广的“等时间谬误”；右图按风洞脉冲烟流还原上快下慢的真实错位与尾流下洗。",
            )

            # Left card: Myth
            lx, ly, lw, lh = 20, 62, 348, 294
            els.append(card(lx, ly, lw, lh))
            els.append(pill(lx + 14, ly + 12, "× 课本常见误传：等时间假设", fg=RED, bg=RED_SOFT, w=206, h=22, size=11.5))

            foil_l, up_l, lo_l = _naca_cambered_pts(lx + 78, ly + 132, 186, alpha_deg=4.0, m=0.06, p=0.38, t=0.14)
            foil_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in foil_l) + " Z"

            # Myth streamlines (falsely paired vertically at trailing edge)
            s_up_myth = [(lx + 24, ly + 124), (lx + 74, ly + 122)]
            for k in [10, 22, 36, 48, 60]:
                s_up_myth.append((up_l[k][0], up_l[k][1] - 11))
            s_up_myth.append((lx + 328, ly + 138))

            s_lo_myth = [(lx + 24, ly + 136), (lx + 74, ly + 136)]
            for k in [12, 26, 40, 52, 60]:
                s_lo_myth.append((lo_l[k][0], lo_l[k][1] + 10))
            s_lo_myth.append((lx + 328, ly + 148))

            els.append(_poly(s_up_myth, stroke=ORANGE, sw=2.0, dash="5 3"))
            els.append(_poly(s_lo_myth, stroke=BLUE, sw=2.0, dash="5 3"))
            els.append(f'<path d="{foil_d}" fill="#cbd5e1" stroke="{SLATE}" stroke-width="1.6"/>')

            # Paired dots A1-B1 (front) and A4-B4 (falsely meeting at tail)
            pair_x_front = lx + 48
            pair_x_tail = lx + 286
            els.append(f'<line x1="{pair_x_front}" y1="{ly + 123}" x2="{pair_x_front}" y2="{ly + 136}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="2 2"/>')
            els.append(f'<circle cx="{pair_x_front}" cy="{ly + 123}" r="4.2" fill="{ORANGE}"/>')
            els.append(f'<circle cx="{pair_x_front}" cy="{ly + 136}" r="4.2" fill="{BLUE}"/>')
            els.append(txt(pair_x_front, ly + 111, "同时出发", size=10.5, color=SLATE, anchor="middle"))

            els.append(f'<line x1="{pair_x_tail}" y1="{ly + 137}" x2="{pair_x_tail}" y2="{ly + 148}" stroke="{RED}" stroke-width="1.5"/>')
            els.append(f'<circle cx="{pair_x_tail}" cy="{ly + 137}" r="4.5" fill="{ORANGE}"/>')
            els.append(f'<circle cx="{pair_x_tail}" cy="{ly + 148}" r="4.5" fill="{BLUE}"/>')
            els.append(txt(pair_x_tail, ly + 123, "假想“同时到尾缘”？", size=10.5, color=RED, anchor="middle", weight="700", halo=True))
            els.append(txt(lx + 172, ly + 86, "误以为：上弧线长一点 → 必须刚好赶上？", size=10.8, color=RED, anchor="middle", weight="600"))

            # Three fatal flaws box
            els.append(card(lx + 14, ly + 178, lw - 28, 104, rx=8, fill=RED_SOFT, stroke="#fecaca"))
            els.append(txt(lx + 26, ly + 198, "三大反例直接推翻“等时间说”：", size=11.2, color=RED, weight="700"))
            els.append(txt(lx + 26, ly + 219, "1. 纸飞机与莱特兄弟薄翼上下一样长，照样飞；", size=10.6, color=BODY))
            els.append(txt(lx + 26, ly + 239, "2. 特技飞机倒扣飞行（长弧在下），靠迎角照样托住；", size=10.6, color=BODY))
            els.append(txt(lx + 26, ly + 259, "3. 按路径差算出的流速差太小，连实测升力零头都不够！", size=10.6, color=BODY))

            # Right card: Real wind-tunnel flow
            rx, ry, rw, rh = 380, 62, 360, 294
            els.append(card(rx, ry, rw, rh))
            els.append(pill(rx + 14, ry + 12, "✓ 真实风洞烟流：上方远超前 + 尾流下偏", fg=GREEN, bg=GREEN_SOFT, w=254, h=22, size=11.5))

            foil_r, up_r, lo_r = _naca_cambered_pts(rx + 74, ry + 126, 178, alpha_deg=7.5, m=0.055, p=0.38, t=0.135)
            foil_rd = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in foil_r) + " Z"

            # Low-pressure suction halo above wing & high-pressure cushion below
            els.append(f'<ellipse cx="{rx + 148}" cy="{ry + 100}" rx="68" ry="18" fill="{BLUE_SOFT}" opacity="0.85"/>')
            els.append(f'<ellipse cx="{rx + 158}" cy="{ry + 144}" rx="62" ry="13" fill="{ORANGE_SOFT}" opacity="0.85"/>')

            # Computed circulation velocity shift: upper parcel traverses chord in ~0.62*T0, lower in ~1.18*T0
            t_upper_ratio = 0.62
            t_lower_ratio = 1.18
            assert t_upper_ratio < 0.75 * t_lower_ratio

            s_up_real = [(rx + 18, ry + 118), (rx + 66, ry + 114)]
            for k in [8, 18, 30, 44, 56, 60]:
                s_up_real.append((up_r[k][0], up_r[k][1] - 10))
            s_up_real += [(rx + 286, ry + 145), (rx + 336, ry + 162)]

            s_lo_real = [(rx + 18, ry + 131), (rx + 66, ry + 132)]
            for k in [12, 26, 40, 52, 60]:
                s_lo_real.append((lo_r[k][0], lo_r[k][1] + 10))
            s_lo_real += [(rx + 286, ry + 157), (rx + 336, ry + 173)]

            els.append(_poly(s_up_real, stroke=BLUE, sw=2.3))
            els.append(_poly(s_lo_real, stroke=ORANGE, sw=2.1))
            els.append(
                f'<polyline class="smoke-trace" pathLength="1" points="'
                + " ".join(f"{x:.1f},{y:.1f}" for x, y in s_up_real)
                + f'" fill="none" stroke="{GREEN}" stroke-width="2.8" stroke-linecap="round"/>'
            )
            els.append(f'<path d="{foil_rd}" fill="#94a3b8" stroke="{INK}" stroke-width="1.7"/>')

            # Show same-timestamp smoke pulse positions:
            # Start pair t0
            els.append(f'<circle cx="{rx + 38}" cy="{ry + 116}" r="4.2" fill="{BLUE}"/>')
            els.append(f'<circle cx="{rx + 38}" cy="{ry + 131}" r="4.2" fill="{ORANGE}"/>')
            els.append(txt(rx + 38, ry + 104, "t₀ 同发", size=10.2, color=SLATE, anchor="middle"))

            # Later timestamp t1: upper parcel is ALREADY well past trailing edge (x=rx+302, y=ry+151),
            # while lower parcel is still at ~75% chord under wing (x=rx+206, y=ry+146)!
            ux1, uy1 = rx + 302, ry + 151
            bx1, by1 = rx + 204, ry + 145
            els.append(f'<circle cx="{ux1}" cy="{uy1}" r="5.0" fill="{BLUE}" stroke="#fff" stroke-width="1.2"/>')
            els.append(f'<circle cx="{bx1}" cy="{by1}" r="5.0" fill="{ORANGE}" stroke="#fff" stroke-width="1.2"/>')
            els.append(f'<line x1="{bx1}" y1="{by1}" x2="{ux1}" y2="{uy1}" stroke="{GREEN}" stroke-width="1.3" stroke-dasharray="3 3"/>')
            els.append(txt(ux1 - 4, uy1 - 12, "t₁ 上方早冲过尾缘！", size=10.5, color=BLUE, anchor="end", weight="700", halo=True))
            els.append(txt(bx1 - 6, by1 + 18, "t₁ 下方还在半路", size=10.3, color=ORANGE, anchor="middle", weight="600", halo=True))

            # Pressure & Lift labels
            els.append(txt(rx + 150, ry + 84, "低压吸力区 (流速大, p上 < p∞)", size=10.5, color=BLUE, anchor="middle", weight="700", halo=True))
            els.append(
                f'<line x1="{rx + 152}" y1="{ry + 118}" x2="{rx + 152}" y2="{ry + 62}" '
                f'stroke="{GREEN}" stroke-width="2.6" marker-end="url(#arr-green)"/>'
            )
            els.append(txt(rx + 160, ry + 68, "升力 L", size=11.2, color=GREEN, weight="700", halo=True))

            # Downwash arrow at wake
            els.append(
                f'<line x1="{rx + 326}" y1="{ry + 128}" x2="{rx + 326}" y2="{ry + 168}" '
                f'stroke="{ORANGE}" stroke-width="2.0" marker-end="url(#arr-orange)"/>'
            )
            els.append(txt(rx + 318, ry + 122, "下洗 Δv_y", size=10.3, color=ORANGE, anchor="end", weight="700", halo=True))

            # Equivalence summary box
            els.append(card(rx + 14, ry + 178, rw - 28, 104, rx=8, fill=GREEN_SOFT, stroke="#bbf7d0"))
            els.append(txt(rx + 26, ry + 198, "两种解释不是死对头，而是同一流场的两本账：", size=11.2, color=GREEN, weight="700"))
            els.append(txt(rx + 26, ry + 219, "• 压强账（伯努利）：上翼面低压吸起 + 下翼面高压托起；", size=10.5, color=BODY))
            els.append(txt(rx + 26, ry + 239, "• 动量账（牛顿）：机翼把空气向下偏转 (F = ṁΔv_y)，", size=10.5, color=BODY))
            els.append(txt(rx + 36, ry + 259, "空气反过来把机翼往上顶——数学积分严格相等！", size=10.5, color=INK, weight="600"))

            css = """
      .smoke-trace {
        stroke-dasharray: 1;
        stroke-dashoffset: 0;
        animation: smokeRun 1.8s ease-out 1 both;
      }
      @keyframes smokeRun {
        from { stroke-dashoffset: 1; opacity: 0.35; }
        to { stroke-dashoffset: 0; opacity: 0.9; }
      }
      @media (prefers-reduced-motion: reduce) {
        .smoke-trace { animation: none; }
      }"""

            svg = figure(
                372,
                "升力等时间谬误辟谣与真实风洞烟流下洗机理",
                "左图展示错误的等时间重逢假设及三大反例；右图展示真实风洞脉冲烟流中上表面气流提前越过尾缘、上下压强差与尾流向下偏转的等价关系。",
                els,
                extra_css=css,
            )
            write_svg(subdir, "equal-transit-myth.svg", svg)

        # -----------------------------------------------------------------------
        # 2. lift-speed-altitude.svg
        # -----------------------------------------------------------------------
        def build_lift_speed_altitude():
            # Exact aerodynamics model: 260-ton widebody (A350/B777 class, m=260,000 kg -> W = 2.5506 MN, S=440 m^2)
            g = 9.81
            mass_kg = 260_000.0
            W_MN = mass_kg * g / 1e6  # 2.5506 MN

            rho_0 = 1.225   # sea level kg/m^3
            rho_11 = 0.364  # 11 km ISA tropopause kg/m^3

            # Three configurations: (rho, S, CL)
            cfg_flap = (rho_0, 510.0, 1.60)    # Takeoff/landing slats + flaps extended
            cfg_clean0 = (rho_0, 440.0, 0.80)  # Sea-level clean wing (no flaps)
            cfg_cruise = (rho_11, 440.0, 0.55) # 11 km cruise (Mach ~0.82)

            def v_req_kmh(rho, S, CL):
                v_ms = math.sqrt(2.0 * (W_MN * 1e6) / (rho * S * CL))
                return v_ms * 3.6

            v_flap = v_req_kmh(*cfg_flap)
            v_clean0 = v_req_kmh(*cfg_clean0)
            v_cruise = v_req_kmh(*cfg_cruise)

            assert 250.0 < v_flap < 268.0, f"Unexpected v_flap={v_flap}"
            assert 385.0 < v_clean0 < 410.0, f"Unexpected v_clean0={v_clean0}"
            assert 855.0 < v_cruise < 878.0, f"Unexpected v_cruise={v_cruise}"

            # Parasitic drag at cruise speed 866 km/h (CD0 = 0.017, S = 440 m^2)
            v_c_ms = v_cruise / 3.6
            CD0 = 0.017
            D_sea_kN = 0.5 * rho_0 * v_c_ms**2 * 440.0 * CD0 / 1e3
            D_11k_kN = 0.5 * rho_11 * v_c_ms**2 * 440.0 * CD0 / 1e3
            drag_ratio = D_11k_kN / D_sea_kN
            assert abs(drag_ratio - rho_11 / rho_0) < 1e-6

            els = []
            els += header(
                "升力公式 L = ½ρv²SC_L 实战账本：为什么起飞要放襟翼，巡航要爬上万米高空？",
                "以 260 吨宽体客机（翼面积 440 m²，重力 W ≈ 255 万牛）精确计算二次方升力曲线与万米减阻收益。",
            )

            # Left card: Quadratic Lift vs Speed chart
            lx, ly, lw, lh = 20, 62, 412, 292
            els.append(card(lx, ly, lw, lh))
            els.append(txt(lx + 16, ly + 23, "① 速度平方律：三种构型跨过“离地生死线 (L = W)”", size=12.6, color=INK, weight="700"))

            px0, py0 = lx + 56, ly + 244  # plot origin (v=0, L=0)
            pw, ph = 334.0, 174.0         # v in [0, 960 km/h], L in [0, 3.6 MN]
            v_max, L_max = 960.0, 3.60

            def map_pt(v_kmh, L_mn):
                x = px0 + (v_kmh / v_max) * pw
                y = py0 - (L_mn / L_max) * ph
                return x, y

            # Grid & Weight threshold line
            for v_tick in [0, 250, 500, 750, 950]:
                gx, _ = map_pt(v_tick, 0)
                els.append(f'<line x1="{gx:.1f}" y1="{py0 - ph:.1f}" x2="{gx:.1f}" y2="{py0:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
                els.append(txt(gx, py0 + 16, f"{v_tick}", size=10.2, color=MUTED, anchor="middle", cls="mono"))

            for L_tick in [0.0, 1.0, 2.0, 3.0]:
                _, gy = map_pt(0, L_tick)
                els.append(f'<line x1="{px0:.1f}" y1="{gy:.1f}" x2="{px0 + pw:.1f}" y2="{gy:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
                els.append(txt(px0 - 8, gy + 4, f"{L_tick:.0f}", size=10.2, color=MUTED, anchor="end", cls="mono"))

            # Axes
            els.append(f'<line x1="{px0:.1f}" y1="{py0 - ph:.1f}" x2="{px0:.1f}" y2="{py0:.1f}" stroke="{SLATE}" stroke-width="1.3"/>')
            els.append(f'<line x1="{px0:.1f}" y1="{py0:.1f}" x2="{px0 + pw:.1f}" y2="{py0:.1f}" stroke="{SLATE}" stroke-width="1.3"/>')
            els.append(txt(px0 + pw / 2, py0 + 34, "真空速 v (km/h)", size=10.8, color=BODY, anchor="middle", weight="600"))
            els.append(txt(lx + 14, py0 - ph / 2 - 4, "升力", size=10.5, color=BODY, weight="600"))
            els.append(txt(lx + 14, py0 - ph / 2 + 11, "(MN)", size=9.8, color=MUTED, cls="mono"))

            # Weight threshold horizontal line W = 2.55 MN
            _, wy = map_pt(0, W_MN)
            els.append(f'<line x1="{px0:.1f}" y1="{wy:.1f}" x2="{px0 + pw:.1f}" y2="{wy:.1f}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="5 4"/>')
            els.append(txt(px0 + pw - 4, wy - 9, f"平飞门槛 L = W = {W_MN:.2f} MN", size=10.1, color=RED, anchor="end", weight="700", halo=True))

            # Plot 3 quadratic curves clipped at L_max
            def build_curve(rho, S, CL, stroke, dash=None):
                pts = []
                for step in range(0, 193):
                    vk = step * 5.0
                    vms = vk / 3.6
                    L_val = 0.5 * rho * vms**2 * S * CL / 1e6
                    if L_val <= L_max:
                        pts.append(map_pt(vk, L_val))
                    else:
                        v_cap = math.sqrt(2.0 * L_max * 1e6 / (rho * S * CL)) * 3.6
                        pts.append(map_pt(v_cap, L_max))
                        break
                return _poly(pts, stroke=stroke, sw=2.3, dash=dash)

            els.append(build_curve(*cfg_flap, GREEN))
            els.append(build_curve(*cfg_clean0, ORANGE, dash="5 3"))
            els.append(build_curve(*cfg_cruise, BLUE))

            # Mark the 3 intersection points with L = W
            xf, yf = map_pt(v_flap, W_MN)
            xc0, yc0 = map_pt(v_clean0, W_MN)
            xcr, ycr = map_pt(v_cruise, W_MN)

            for cx, cy, col in [(xf, yf, GREEN), (xc0, yc0, ORANGE), (xcr, ycr, BLUE)]:
                els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.6" fill="{col}" stroke="#fff" stroke-width="1.3"/>')

            els.append(txt(xf - 6, yf - 9, f"放襟翼 {v_flap:.0f}", size=10.2, color=GREEN, anchor="end", weight="700", halo=True))
            els.append(txt(xc0 + 7, yc0 + 17, f"光洁翼 {v_clean0:.0f}", size=10.1, color=ORANGE, anchor="start", weight="700", halo=True))
            els.append(txt(xcr - 6, ycr + 17, f"巡航 {v_cruise:.0f} km/h", size=10.2, color=BLUE, anchor="end", weight="700", halo=True))

            # Curve labels near lower part
            els.append(txt(px0 + 42, py0 - 82, "海平面+放襟翼", size=10.0, color=GREEN, weight="600", halo=True))
            els.append(txt(px0 + 216, py0 - 52, "11 km 平流层底 (ρ≈0.30ρ₀)", size=10.0, color=BLUE, weight="600", halo=True))

            # Right card: Flaps + High-altitude drag trade-off
            rx, ry, rw, rh = 444, 62, 296, 292
            els.append(card(rx, ry, rw, rh))
            els.append(txt(rx + 14, ry + 23, "② 襟翼变形记 & 万米高空省油账", size=12.6, color=INK, weight="700"))

            # Top sub-box: Flaps at takeoff/landing
            els.append(card(rx + 14, ry + 38, rw - 28, 108, rx=8, fill=GREEN_SOFT, stroke="#bbf7d0"))
            els.append(txt(rx + 24, ry + 58, "起降慢飞：伸出前缘缝翼 + 后缘襟翼", size=11.0, color=GREEN, weight="700"))
            els.append(txt(rx + 24, ry + 78, "• 机翼面积 S 扩大 (440 → 510 m²)，弯度暴增", size=10.4, color=BODY))
            els.append(txt(rx + 24, ry + 97, "• 升力系数 C_L 翻倍 (0.80 → 1.60)", size=10.4, color=BODY))
            els.append(txt(rx + 24, ry + 116, f"• 离地速度从 {v_clean0:.0f} 降到 {v_flap:.0f} km/h，跑道够用！", size=10.4, color=INK, weight="600"))
            els.append(txt(rx + 24, ry + 135, "（代价：阻力也大，起飞爬升后必须收回）", size=10.0, color=MUTED))

            # Bottom sub-box: Why cruise at 11 km?
            els.append(card(rx + 14, ry + 156, rw - 28, 124, rx=8, fill=BLUE_SOFT, stroke=BLUE_LINE))
            els.append(txt(rx + 24, ry + 176, f"巡航快飞：同以 {v_cruise:.0f} km/h 飞，阻力差多少？", size=10.8, color=BLUE, weight="700"))

            # Horizontal bar comparison of parasitic drag D0
            bar_max_w = 130.0
            w_sea = bar_max_w
            w_11k = bar_max_w * (D_11k_kN / D_sea_kN)
            els.append(txt(rx + 24, ry + 200, "海平面硬飞", size=10.2, color=SLATE))
            els.append(f'<rect x="{rx + 88}" y="{ry + 189}" width="{w_sea:.1f}" height="13" rx="4" fill="{ORANGE}"/>')
            els.append(txt(rx + 88 + w_sea + 6, ry + 200, f"{D_sea_kN:.0f} kN", size=10.2, color=ORANGE, weight="700", cls="mono"))

            els.append(txt(rx + 24, ry + 223, "11 km 高空", size=10.2, color=BLUE, weight="600"))
            els.append(f'<rect x="{rx + 88}" y="{ry + 212}" width="{w_11k:.1f}" height="13" rx="4" fill="{BLUE}"/>')
            els.append(txt(rx + 88 + w_11k + 6, ry + 223, f"{D_11k_kN:.0f} kN (-70%!)", size=10.2, color=BLUE, weight="700", cls="mono"))

            els.append(txt(rx + 24, ry + 248, "• 万米空气密度 ρ 仅海平面的 30%，废阻砍掉七成", size=10.3, color=BODY))
            els.append(txt(rx + 24, ry + 267, "• 用高速度 v² 补回稀薄 ρ，既快又省燃油！", size=10.3, color=INK, weight="600"))

            svg = figure(
                368,
                "升力公式速度平方曲线与客机襟翼及万米巡航减阻原理",
                f"左图计算280吨客机在放襟翼({v_flap:.0f} km/h)、海平面光洁翼({v_clean0:.0f} km/h)与11千米高空({v_cruise:.0f} km/h)的二次方升力曲线；右图对比海平面与11千米巡航寄生阻力({D_sea_kN:.0f} kN vs {D_11k_kN:.0f} kN)。",
                els,
            )
            write_svg(subdir, "lift-speed-altitude.svg", svg)

        # -----------------------------------------------------------------------
        # 3. helicopter-torque-balance.svg
        # -----------------------------------------------------------------------
        def build_helicopter_torque():
            # Exact torque balance: P = 900 kW, Omega = 30 rad/s -> tau = 30,000 N·m
            power_W = 900_000.0
            omega_rads = 30.0
            tau_Nm = power_W / omega_rads  # 30,000 N·m
            lever_m = 6.0
            T_tail_N = tau_Nm / lever_m    # 5,000 N
            assert abs(tau_Nm - T_tail_N * lever_m) < 1e-6

            els = []
            els += header(
                "直升机为什么非要拖一根“小尾巴”？角动量守恒与反扭矩平衡（俯视图）",
                "主旋翼被发动机拧着逆时针转时，机身必然受到等大反向的顺时针反作用力矩！",
            )

            # Left card: Without tail rotor (spins out of control)
            lx, ly, lw, lh = 20, 62, 336, 286
            els.append(card(lx, ly, lw, lh))
            els.append(pill(lx + 14, ly + 12, "① 假如拆掉尾桨：机身原地打转！", fg=RED, bg=RED_SOFT, w=222, h=22, size=11.5))

            cx1, cy1 = lx + 168, ly + 132
            # Main rotor disc
            els.append(f'<circle cx="{cx1}" cy="{cy1}" r="66" fill="{BLUE_SOFT}" stroke="{BLUE_LINE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
            # Fuselage top-down teardrop + broken tail
            els.append(f'<ellipse cx="{cx1}" cy="{cy1}" rx="18" ry="34" fill="#cbd5e1" stroke="{SLATE}" stroke-width="1.6"/>')
            els.append(f'<rect x="{cx1 - 4}" y="{cy1 + 30}" width="8" height="44" rx="3" fill="#cbd5e1" stroke="{SLATE}" stroke-width="1.4"/>')
            els.append(txt(cx1 + 14, cy1 + 72, "× 无尾桨侧推", size=10.3, color=RED, weight="700"))

            # Four rotor blades
            for ang in [25, 115, 205, 295]:
                r_rad = math.radians(ang)
                bx = cx1 + 62 * math.cos(r_rad)
                by = cy1 - 62 * math.sin(r_rad)
                els.append(f'<line x1="{cx1}" y1="{cy1}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{BLUE}" stroke-width="3.2" stroke-linecap="round"/>')
            els.append(f'<circle cx="{cx1}" cy="{cy1}" r="5.5" fill="{INK}"/>')

            # CCW arc for main rotor (outer)
            els.append(
                f'<path d="M {cx1 + 52:.1f},{cy1 - 52:.1f} A 73,73 0 0,0 {cx1 - 52:.1f},{cy1 - 52:.1f}" '
                f'fill="none" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#arr-blue)"/>'
            )
            els.append(txt(cx1, cy1 - 78, "主旋翼逆时针转 (+L_旋翼)", size=10.6, color=BLUE, anchor="middle", weight="700", halo=True))

            # CW reaction arc on fuselage (inner)
            els.append(
                f'<path d="M {cx1 - 28:.1f},{cy1 - 12:.1f} A 30,30 0 0,1 {cx1 + 28:.1f},{cy1 - 12:.1f}" '
                f'fill="none" stroke="{RED}" stroke-width="2.4" marker-end="url(#arr-orange)"/>'
            )
            els.append(txt(cx1 + 36, cy1 + 4, "机身顺时针狂转！", size=10.5, color=RED, weight="700", halo=True))

            els.append(card(lx + 14, ly + 218, lw - 28, 56, rx=8, fill=RED_SOFT, stroke="#fecaca"))
            els.append(txt(lx + 26, ly + 239, "• 孤立系统总角动量守恒：发动机拧旋翼向左转，", size=10.4, color=BODY))
            els.append(txt(lx + 26, ly + 259, "  旋翼轴就拧机身向右转（牛顿第三定律旋转版）！", size=10.4, color=RED, weight="600"))

            # Right card: Tail rotor lever arm + Coaxial solution
            rx, ry, rw, rh = 368, 62, 372, 286
            els.append(card(rx, ry, rw, rh))
            els.append(pill(rx + 14, ry + 12, "② 尾桨长力臂抵消 vs 共轴反桨对消", fg=GREEN, bg=GREEN_SOFT, w=244, h=22, size=11.5))

            cx2, cy2 = rx + 114, ry + 118
            tail_y = cy2 + 86  # lever arm d = 6.0 m scaled to 86 px

            els.append(f'<circle cx="{cx2}" cy="{cy2}" r="56" fill="{BLUE_SOFT}" stroke="{BLUE_LINE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
            # Fuselage + long tail boom
            els.append(f'<ellipse cx="{cx2}" cy="{cy2}" rx="16" ry="30" fill="#cbd5e1" stroke="{SLATE}" stroke-width="1.6"/>')
            els.append(f'<rect x="{cx2 - 4}" y="{cy2 + 26}" width="8" height="64" rx="3" fill="#94a3b8" stroke="{SLATE}" stroke-width="1.5"/>')

            for ang in [25, 115, 205, 295]:
                r_rad = math.radians(ang)
                bx = cx2 + 52 * math.cos(r_rad)
                by = cy2 - 52 * math.sin(r_rad)
                els.append(f'<line x1="{cx2}" y1="{cy2}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{BLUE}" stroke-width="3.0" stroke-linecap="round"/>')
            els.append(f'<circle cx="{cx2}" cy="{cy2}" r="5" fill="{INK}"/>')

            # CW reaction torque on hub
            els.append(
                f'<path d="M {cx2 - 23:.1f},{cy2 - 10:.1f} A 25,25 0 0,1 {cx2 + 23:.1f},{cy2 - 10:.1f}" '
                f'fill="none" stroke="{ORANGE}" stroke-width="2.1" marker-end="url(#arr-orange)"/>'
            )
            els.append(txt(cx2, cy2 - 64, "反扭矩 τ_反 = 30 kN·m", size=10.3, color=ORANGE, anchor="middle", weight="700", halo=True))

            # Tail rotor on side of boom + Thrust arrow to the right (creating CCW torque around cx2,cy2!
            # Wait: let's check vector cross product!
            # Screen coords: +x right, +y down.
            # Main rotor spins CCW: from +x (right) toward -y (up).
            # Fuselage reaction torque spins CW: nose (up, -y) goes right (+x), so tail (down, +y) goes LEFT (-x)!
            # Therefore, to STOP the tail from swinging LEFT, the tail rotor must push the tail boom to the RIGHT (+x), producing CCW torque!)
            # Let's verify: r_tail = (0, +d). F_tail = (+T, 0). Torque around hub: nose goes left, tail goes right = CCW! Exact!
            els.append(f'<line x1="{cx2 - 10}" y1="{tail_y - 11}" x2="{cx2 - 10}" y2="{tail_y + 11}" stroke="{GREEN}" stroke-width="3.4" stroke-linecap="round"/>')
            els.append(
                f'<line x1="{cx2 + 4}" y1="{tail_y}" x2="{cx2 + 62}" y2="{tail_y}" '
                f'stroke="{GREEN}" stroke-width="2.6" marker-end="url(#arr-green)"/>'
            )
            els.append(txt(cx2 + 34, tail_y - 8, f"尾桨推力 T={T_tail_N / 1000:.0f}kN", size=10.0, color=GREEN, anchor="middle", weight="700", halo=True))

            # Lever arm dimension line on left of tail boom
            els.append(f'<line x1="{cx2 - 26}" y1="{cy2}" x2="{cx2 - 26}" y2="{tail_y}" stroke="{SLATE}" stroke-width="1.2"/>')
            els.append(f'<line x1="{cx2 - 31}" y1="{cy2}" x2="{cx2 - 21}" y2="{cy2}" stroke="{SLATE}" stroke-width="1.2"/>')
            els.append(f'<line x1="{cx2 - 31}" y1="{tail_y}" x2="{cx2 - 21}" y2="{tail_y}" stroke="{SLATE}" stroke-width="1.2"/>')
            els.append(txt(cx2 - 34, (cy2 + tail_y) / 2 + 4, f"力臂 d={lever_m:.0f}m", size=10.0, color=SLATE, anchor="end", weight="600"))

            # Right-side explanation & Coaxial alternative box
            bx0 = rx + 206
            els.append(card(bx0, ry + 48, 152, 108, rx=8, fill=GREEN_SOFT, stroke="#bbf7d0"))
            els.append(txt(bx0 + 10, ry + 68, "杠杆以小博大：", size=10.8, color=GREEN, weight="700"))
            els.append(txt(bx0 + 10, ry + 88, "T × d = 5 kN × 6 m", size=10.2, color=INK, weight="600", cls="mono"))
            els.append(txt(bx0 + 10, ry + 106, "= 30 kN·m = τ_反", size=10.2, color=GREEN, weight="700", cls="mono"))
            els.append(txt(bx0 + 10, ry + 126, "净力矩 Στ = 0，机头稳稳", size=10.0, color=BODY))
            els.append(txt(bx0 + 10, ry + 143, "锁住航向（脚蹬调尾桨距）", size=10.0, color=MUTED))

            # Coaxial / tandem inset
            els.append(card(bx0, ry + 166, 152, 108, rx=8, fill=PURPLE_SOFT, stroke="#ddd6fe"))
            els.append(txt(bx0 + 10, ry + 186, "不用尾桨？双旋翼对消！", size=10.6, color=PURPLE, weight="700"))
            els.append(txt(bx0 + 10, ry + 206, "• 共轴双桨 / 纵列支奴干", size=10.1, color=BODY))
            els.append(txt(bx0 + 10, ry + 225, "• 四轴无人机：2正转+2反转", size=10.1, color=BODY))
            els.append(txt(bx0 + 10, ry + 245, "• (+L) + (-L) = 0，反扭矩", size=10.1, color=PURPLE, weight="600"))
            els.append(txt(bx0 + 10, ry + 262, "  在机身上内部互相抵消！", size=10.0, color=BODY))

            els.append(txt(rx + 18, ry + 242, "俯视：主桨逆转 → 机尾本想左甩，", size=10.0, color=SLATE))
            els.append(txt(rx + 18, ry + 260, "尾桨向右推尾梁，逆时针扳平！", size=10.0, color=INK, weight="600"))

            svg = figure(
                364,
                "直升机反扭矩机理与尾桨力矩平衡俯视图",
                f"左图展示无尾桨时主旋翼逆时针旋转引发机身顺时针失控自旋；右图按P=900kW、Ω=30rad/s计算30kN·m反扭矩由6米尾梁末端5kN尾桨侧推力精确平衡，并对比双旋翼与四轴无人机对消方案。",
                els,
            )
            write_svg(subdir, "helicopter-torque-balance.svg", svg)

        # -----------------------------------------------------------------------
        # 4. flight-regimes-map.svg
        # -----------------------------------------------------------------------
        def build_flight_regimes():
            # Exact Mach 2.0 wavefront envelope geometry: sin(mu) = 1 / M = 0.5 -> mu = 30.0 deg!
            M_sup = 2.0
            mu_rad = math.asin(1.0 / M_sup)
            mu_deg = math.degrees(mu_rad)
            assert abs(mu_deg - 30.0) < 1e-9

            els = []
            els += header(
                "横跨七个数量级的“飞行全图谱”：从昆虫前缘涡、马赫锥到真空轨道",
                "空气从“像糖浆一样黏”到“来不及让路撞出激波”，再到彻底消失——每跨一级都得换一套物理武器。",
            )

            # Top row: 4 atmospheric & space regime cards across 720px (x=20..740)
            cards_spec = [
                (
                    "① 昆虫悬停",
                    "Re ~ 10²–10⁴ | 1–5 m/s",
                    PURPLE,
                    PURPLE_SOFT,
                    ["空气相对像糖浆般黏稠", "大迎角高频拍翼卷出稳定", "【前缘涡 LEV】吸住上翼面"],
                ),
                (
                    "② 飞鸟扑翼/滑翔",
                    "Re ~ 10⁴–10⁵ | 10–25 m/s",
                    GREEN,
                    GREEN_SOFT,
                    ["下拍展羽同时造升力+推力", "上抬折翼漏气减小负功", "信天翁借海面风切变白嫖能量"],
                ),
                (
                    "③ 亚/跨声速客机",
                    "M ≈ 0.80–0.85 | ~870 km/h",
                    BLUE,
                    BLUE_SOFT,
                    ["贴体流线 + 30°–35° 后掠翼", "推迟机翼局部激波暴涨", "兼顾高巡航速度与低波阻"],
                ),
                (
                    "④ 真空火箭与卫星",
                    "ρ → 0 | v ≥ 7.9 km/s",
                    ORANGE,
                    ORANGE_SOFT,
                    ["无空气 → 机翼升力归零", "火箭自带氧化剂向后喷气推进", "入轨后关机靠万有引力自由落体"],
                ),
            ]

            cw = 171
            gap = 12
            for idx, (ctitle, csub, fg, bg, bullets) in enumerate(cards_spec):
                cx = 20 + idx * (cw + gap)
                cy = 62
                els.append(card(cx, cy, cw, 128, rx=9, fill=CARD_BG, stroke=BORDER))
                els.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="28" rx="9" fill="{bg}"/>')
                els.append(txt(cx + 10, cy + 19, ctitle, size=11.5, color=fg, weight="700"))
                els.append(txt(cx + 10, cy + 44, csub, size=9.8, color=MUTED, cls="mono"))
                for bi, bline in enumerate(bullets):
                    els.append(txt(cx + 10, cy + 66 + bi * 19, bline, size=10.2, color=BODY))

            # Bottom wide panel: Subsonic vs Supersonic Mach 2.0 exact wavefront cone + Transonic wave drag curve
            by, bh = 202, 168
            els.append(card(20, by, 720, bh))
            els.append(txt(36, by + 23, "⑤ 为什么会有“声障”与音爆？声波跑不过飞机时，叠出 sin μ = 1/M 的马赫锥！", size=12.4, color=INK, weight="700"))

            # Sub-diagram A (left): Subsonic M = 0.6 (nested non-crossing circles, disturbances warn air ahead!)
            sx_tip, sy_mid = 138.0, by + 99.0
            els.append(txt(124, by + 46, "亚声速 (M=0.6)：声波超前报信", size=10.4, color=BLUE, anchor="middle", weight="600"))
            v_sub_px = 8.4   # per dt
            a_px = 14.0      # speed of sound per dt -> M = 8.4/14.0 = 0.6
            for step in [1, 2, 3]:
                cx_s = sx_tip - v_sub_px * step
                r_s = a_px * step
                assert cx_s + r_s > sx_tip
                els.append(f'<circle cx="{cx_s:.1f}" cy="{sy_mid:.1f}" r="{r_s:.1f}" fill="none" stroke="{BLUE_LINE}" stroke-width="1.3"/>')
            els.append(f'<circle cx="{sx_tip:.1f}" cy="{sy_mid:.1f}" r="4.0" fill="{BLUE}"/>')
            els.append(txt(124, by + 157, "前方空气提前让路，无激波", size=10.1, color=SLATE, anchor="middle"))

            # Divider
            els.append(f'<line x1="226" y1="{by + 36}" x2="226" y2="{by + 158}" stroke="{BORDER}" stroke-width="1"/>')

            # Sub-diagram B (middle): Supersonic M = 2.0 (mu = 30.0 deg exact tangent Mach cone!)
            mx_tip, my_mid = 432.0, by + 99.0
            els.append(txt(350, by + 46, "超声速 (M=2.0)：把声波甩在身后", size=10.4, color=RED, anchor="middle", weight="700"))
            v_sup_px = 19.0  # per dt
            a_sup_px = 9.5   # M = 19.0 / 9.5 = 2.0
            for step in [1, 2, 3, 4]:
                cx_m = mx_tip - v_sup_px * step
                r_m = a_sup_px * step
                d_dist = mx_tip - cx_m
                assert abs(d_dist * math.sin(mu_rad) - r_m) < 1e-9
                els.append(f'<circle cx="{cx_m:.1f}" cy="{my_mid:.1f}" r="{r_m:.1f}" fill="none" stroke="#fca5a5" stroke-width="1.3"/>')
                els.append(f'<circle cx="{cx_m:.1f}" cy="{my_mid:.1f}" r="1.8" fill="{MUTED}"/>')

            # Cone envelope lines of length L_cone = 88 px backward from nose (88 * sin30 = 44 px half-height!)
            L_cone = 88.0
            x_back = mx_tip - L_cone * math.cos(mu_rad)
            y_top = my_mid - L_cone * math.sin(mu_rad)
            y_bot = my_mid + L_cone * math.sin(mu_rad)
            els.append(f'<line x1="{mx_tip:.1f}" y1="{my_mid:.1f}" x2="{x_back:.1f}" y2="{y_top:.1f}" stroke="{RED}" stroke-width="2.2"/>')
            els.append(f'<line x1="{mx_tip:.1f}" y1="{my_mid:.1f}" x2="{x_back:.1f}" y2="{y_bot:.1f}" stroke="{RED}" stroke-width="2.2"/>')
            els.append(f'<line x1="{mx_tip - 94:.1f}" y1="{my_mid:.1f}" x2="{mx_tip + 14:.1f}" y2="{my_mid:.1f}" stroke="{SLATE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
            els.append(f'<polygon points="{mx_tip + 6:.1f},{my_mid:.1f} {mx_tip - 9:.1f},{my_mid - 4.5:.1f} {mx_tip - 9:.1f},{my_mid + 4.5:.1f}" fill="{RED}"/>')
            els.append(txt(mx_tip - 54, my_mid - 8, "μ = 30°", size=10.2, color=RED, weight="700", halo=True))
            els.append(txt(350, by + 157, "sin μ = a/v = 1/M（激波扫地即音爆！）", size=10.1, color=RED, anchor="middle", weight="600"))

            # Divider
            els.append(f'<line x1="474" y1="{by + 36}" x2="474" y2="{by + 158}" stroke="{BORDER}" stroke-width="1"/>')

            # Sub-diagram C (right): Transonic wave drag spike around M = 1
            els.append(txt(606, by + 48, "跨声速波阻墙 (M ≈ 0.8–1.2)", size=10.5, color=ORANGE, anchor="middle", weight="700"))
            dx0, dy0, dw, dh = 508.0, by + 122.0, 202.0, 62.0
            els.append(f'<line x1="{dx0}" y1="{dy0 - dh}" x2="{dx0}" y2="{dy0}" stroke="{SLATE}" stroke-width="1.2"/>')
            els.append(f'<line x1="{dx0}" y1="{dy0}" x2="{dx0 + dw}" y2="{dy0}" stroke="{SLATE}" stroke-width="1.2"/>')
            # Mach 1 dashed vertical line
            m1_x = dx0 + (1.0 / 2.2) * dw
            els.append(f'<line x1="{m1_x:.1f}" y1="{dy0 - dh}" x2="{m1_x:.1f}" y2="{dy0}" stroke="{RED}" stroke-width="1.2" stroke-dasharray="3 3"/>')
            els.append(txt(m1_x, dy0 + 13, "M = 1", size=9.6, color=RED, anchor="middle", weight="700", cls="mono"))
            els.append(txt(dx0 + 18, dy0 + 13, "0.4", size=9.5, color=MUTED, anchor="middle", cls="mono"))
            els.append(txt(dx0 + dw - 14, dy0 + 13, "2.0", size=9.5, color=MUTED, anchor="middle", cls="mono"))

            drag_pts = []
            for i in range(60):
                m_val = 0.2 + 2.0 * (i / 59.0)
                cd_norm = 0.22 + 0.72 * math.exp(-((m_val - 1.03) / 0.19) ** 2) + (0.18 / math.sqrt(max(m_val**2 - 0.85, 0.25)) if m_val > 1.05 else 0.0)
                cd_norm = min(cd_norm, 0.96)
                drag_pts.append((dx0 + (m_val / 2.2) * dw, dy0 - cd_norm * dh))
            els.append(_poly(drag_pts, stroke=ORANGE, sw=2.3))
            els.append(txt(dx0 - 6, dy0 - dh / 2 + 4, "C_D", size=9.6, color=BODY, anchor="end", weight="600", cls="mono"))
            els.append(txt(m1_x + 12, dy0 - dh + 14, "激波暴增！", size=10.0, color=ORANGE, weight="700", halo=True))
            els.append(txt(606, by + 156, "尖头 + 后掠翼专治这道阻力峰", size=10.1, color=SLATE, anchor="middle"))

            svg = figure(
                384,
                "跨尺度飞行物理图谱与超声速马赫锥激波几何",
                "上方对比昆虫前缘涡、飞鸟非对称扑翼与动态翱翔、亚声速后掠翼客机及真空火箭卫星四类机制；下方精确绘制M=0.6亚声速声波前传、M=2.0超声速30度马赫锥包络与M=1跨声速波阻峰值。",
                els,
            )
            write_svg(subdir, "flight-regimes-map.svg", svg)

        build_equal_transit()
        build_lift_speed_altitude()
        build_helicopter_torque()
        build_flight_regimes()

    @register("sun-light", "太阳发光之谜：开尔文寿命危机、伽莫夫量子隧穿峰、夫琅禾费光谱与中微子破案", "science_tech")
    def build_sun_light():
        subdir = "sun-light"

        # -----------------------------------------------------------------------
        # 1. kelvin-coal-vs-fusion.svg
        # -----------------------------------------------------------------------
        def build_kelvin_lifespan():
            # Exact astronomical constants (IAU 2015 nominal solar values)
            G = 6.67430e-11
            c = 2.99792458e8
            M_sun = 1.98847e30
            R_sun = 6.957e8
            L_sun = 3.828e26
            sec_per_yr = 365.25 * 86400.0

            # 1) Chemical combustion: stoichiometric carbon + O2 (C + O2 -> CO2 releases 393.5 kJ per 44 g total reactants = 8.94e6 J/kg;
            # even generous coal/hydrocarbon + O2 ~ 1.0e7 J/kg -> ~1,650-5,000 yr; let's compute exact stoichiometric C+O2 = 8.94 MJ/kg -> 1,472 yr,
            # and pure coal energy if O2 ignored ~ 30 MJ/kg -> 4,940 yr! Let's note ~1,500-5,000 yr, plotting ~3,000 yr midpoint!)
            e_chem_jkg = 1.8e7  # representative ~18 MJ/kg (~3,000 yr)
            t_coal_yr = (M_sun * e_chem_jkg) / L_sun / sec_per_yr
            assert 1400.0 < t_coal_yr < 5500.0

            # 2) Kelvin-Helmholtz gravitational contraction: t_KH = G M^2 / (R L) (or 3/4 to 1 * GM^2/RL)
            t_kh_yr = (G * M_sun**2 / (R_sun * L_sun)) / sec_per_yr  # ~3.13e7 yr (~3100万年)
            assert 2.0e7 < t_kh_yr < 3.5e7

            # 3) Solar system radiometric age: 4.54e9 yr
            t_earth_yr = 4.54e9

            # 4) Core H -> He nuclear fusion: core ~10% of M_sun fuses with 0.0071 mass defect
            f_core = 0.10
            eps_fusion = 0.0071
            e_fusion_jkg = eps_fusion * c**2  # 6.38e14 J/kg!
            t_fusion_yr = (f_core * M_sun * e_fusion_jkg) / L_sun / sec_per_yr  # ~1.05e10 yr (~100亿年)
            assert 9.5e9 < t_fusion_yr < 1.15e10

            els = []
            els += header(
                "十九世纪最大科学悬案：如果太阳烧煤或靠引力收缩，它早就熄火了！",
                "按太阳真实质量 1.99×10³⁰ kg 与光度 3.83×10²⁶ W 核算对数寿命尺——差出整整七个数量级。",
            )

            # Main card
            els.append(card(20, 62, 720, 286))
            els.append(txt(38, 86, "对数时间尺（10³ 年 → 10¹¹ 年）：每往右走一格，寿命翻 10 倍！", size=12.4, color=INK, weight="700"))

            # Log axis from log10(t) = 3.0 to 11.0
            ax0, ax1 = 198.0, 706.0
            aw = ax1 - ax0

            def map_logx(yr):
                lg = math.log10(yr)
                return ax0 + ((lg - 3.0) / 8.0) * aw

            # Vertical grid lines for 10^3 .. 10^11 using crisp SVG superscript tspans
            for exp_i in range(3, 12):
                gx = ax0 + ((exp_i - 3.0) / 8.0) * aw
                els.append(f'<line x1="{gx:.1f}" y1="104" x2="{gx:.1f}" y2="262" stroke="{SLATE_SOFT}" stroke-width="1.2"/>')
                els.append(
                    f'<text x="{gx:.1f}" y="280" font-size="10.2" fill="{MUTED}" text-anchor="middle">'
                    f'10<tspan dy="-4" font-size="7.8">{exp_i}</tspan><tspan dy="4">年</tspan></text>'
                )

            els.append(f'<line x1="{ax0:.1f}" y1="262" x2="{ax1:.1f}" y2="262" stroke="{SLATE}" stroke-width="1.3"/>')

            # Geological / Darwin reality threshold vertical line at 4.54e9 yr
            x_geo = map_logx(t_earth_yr)
            els.append(f'<line x1="{x_geo:.1f}" y1="100" x2="{x_geo:.1f}" y2="262" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="5 3"/>')
            els.append(txt(x_geo - 6, 113, "地球与陨石实测年龄 ≈ 45.4 亿年（生命演化铁证！）", size=10.4, color=BLUE, anchor="end", weight="700", halo=True))

            # Three horizontal log bars
            bars = [
                (
                    "① 整颗太阳烧煤+氧气",
                    "化学键能 ~10⁷ J/kg",
                    t_coal_yr,
                    RED,
                    RED_SOFT,
                    "仅够烧约 1,500–5,000 年（金字塔刚建好就灭了！）",
                    128,
                ),
                (
                    "② 开尔文引力收缩",
                    "t_KH = GM²/(RL)",
                    t_kh_yr,
                    ORANGE,
                    ORANGE_SOFT,
                    f"最多约 {t_kh_yr / 1e7:.0f}000 万年（比地球年龄短 150 倍！）",
                    176,
                ),
                (
                    "③ 核心氢聚变成氦",
                    "E = 0.0071 mc²",
                    t_fusion_yr,
                    GREEN,
                    GREEN_SOFT,
                    f"主序星寿命约 {t_fusion_yr / 1e8:.0f} 亿年 ✓（如今 46 亿岁正值壮年）",
                    224,
                ),
            ]

            for btitle, bsub, t_val, col, bg_col, note_s, by in bars:
                els.append(txt(36, by + 11, btitle, size=11.2, color=INK, weight="700"))
                els.append(txt(36, by + 27, bsub, size=9.8, color=MUTED, cls="mono"))
                bx_end = map_logx(t_val)
                bw = max(10.0, bx_end - ax0)
                els.append(f'<rect x="{ax0:.1f}" y="{by + 2}" width="{bw:.1f}" height="22" rx="5" fill="{bg_col}" stroke="{col}" stroke-width="1.5"/>')
                els.append(f'<circle cx="{bx_end:.1f}" cy="{by + 13}" r="4.2" fill="{col}"/>')
                if t_val < 1e9:
                    els.append(txt(bx_end + 10, by + 17, note_s, size=10.4, color=col, weight="700", halo=True))
                else:
                    els.append(txt(ax0 + 12, by + 17, note_s, size=10.4, color=GREEN, weight="700"))

            # Bottom energy-density callout banner
            els.append(card(36, 294, 688, 42, rx=8, fill=SLATE_SOFT, stroke=BORDER))
            els.append(
                txt(
                    380,
                    320,
                    "根源差距：化学燃烧只挪动外层电子（~10⁷ J/kg），核聚变重组原子核（6.4×10¹⁴ J/kg）——同重燃料能量高出数千万倍！",
                    size=10.8,
                    color=INK,
                    anchor="middle",
                    weight="600",
                )
            )

            svg = figure(
                364,
                "太阳能源寿命对数对比：化学烧煤、开尔文引力收缩与氢核聚变",
                f"按太阳质量与光度精确计算三种能源寿命：化学燃烧仅数千年、开尔文-亥姆霍兹引力收缩约{t_kh_yr/1e7:.1f}千万年（远小于地球45.4亿年年龄），唯有氢核聚变可达约100亿年。",
                els,
            )
            write_svg(subdir, "kelvin-coal-vs-fusion.svg", svg)

        # -----------------------------------------------------------------------
        # 2. gamow-quantum-tunneling.svg
        # -----------------------------------------------------------------------
        def build_gamow_tunneling():
            # Exact solar-core Gamow peak calculation at T = 1.5e7 K
            kB_eV_K = 8.617333262e-5
            T_core = 1.5e7
            kBT_keV = kB_eV_K * T_core / 1e3  # 1.2926 keV
            # Gamow energy E_G = 2 * mu * c^2 * (pi * alpha * Z1 * Z2)^2
            mp_keV = 938_272.088
            mu_keV = 0.5 * mp_keV
            alpha_em = 1.0 / 137.035999
            E_G_keV = 2.0 * mu_keV * (math.pi * alpha_em) ** 2  # 493.12 keV
            E0_keV = (E_G_keV * kBT_keV**2 / 4.0) ** (1.0 / 3.0)  # 5.905 keV!

            assert 1.28 < kBT_keV < 1.31
            assert 490.0 < E_G_keV < 496.0
            assert 5.85 < E0_keV < 5.96

            els = []
            els += header(
                "1500 万度其实“不够热”！伽莫夫量子隧穿怎样帮质子钻过千倍电斥力高墙？",
                f"核心热能 k_BT ≈ {kBT_keV:.1f} keV 比库仑势垒 (~1,000 keV) 矮近千倍；全靠量子波穿墙与 E₀ ≈ {E0_keV:.1f} keV 伽莫夫峰！",
            )

            # Left card: Coulomb barrier V(r) vs Nuclear well + Quantum wave tunneling
            lx, ly, lw, lh = 20, 62, 348, 292
            els.append(card(lx, ly, lw, lh))
            els.append(txt(lx + 16, ly + 23, "① 空间势能墙 V(r)：经典弹珠 100% 被弹回", size=12.4, color=INK, weight="700"))

            ox, oy = lx + 52.0, ly + 224.0  # r=0, V=0 baseline (well goes below oy to oy+40)
            pw_l, ph_l = 274.0, 118.0       # r in [0, 10 fm]

            # Strong-force nuclear potential well for r < r0 = 1.8 fm (drawn schematic radial scale, labeled clearly)
            r0_px = ox + 46.0
            els.append(f'<rect x="{ox:.1f}" y="{oy - ph_l:.1f}" width="46.0" height="{ph_l + 36:.1f}" fill="{GREEN_SOFT}" opacity="0.75"/>')
            els.append(f'<line x1="{ox:.1f}" y1="{oy - ph_l - 6:.1f}" x2="{ox:.1f}" y2="{oy + 38:.1f}" stroke="{SLATE}" stroke-width="1.3"/>')
            els.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ox + pw_l:.1f}" y2="{oy:.1f}" stroke="{SLATE}" stroke-width="1.2"/>')

            # Coulomb curve V(r) = V_peak * (r0 / r) for r >= r0
            coulomb_pts = [(ox, oy + 34.0), (r0_px, oy + 34.0), (r0_px, oy - ph_l)]
            for i in range(1, 65):
                frac = i / 64.0
                rx_p = r0_px + frac * (pw_l - 46.0)
                r_ratio = 1.0 + frac * 5.2
                vy_p = oy - (ph_l / r_ratio)
                coulomb_pts.append((rx_p, vy_p))
            els.append(_poly(coulomb_pts, stroke=ORANGE, sw=2.4))

            # Peak annotation (~1000 keV = 1 MeV)
            els.append(f'<circle cx="{r0_px:.1f}" cy="{oy - ph_l:.1f}" r="4.0" fill="{ORANGE}"/>')
            els.append(txt(r0_px + 8, oy - ph_l + 6, "库仑斥力峰 ≈ 1,000 keV (1 MeV)", size=10.4, color=ORANGE, weight="700", halo=True))
            els.append(txt(ox + 23, oy + 26, "强核力深井", size=9.6, color=GREEN, anchor="middle", weight="700"))

            # Proton Gamow/thermal energy level near bottom (exaggerated slightly for visibility, explicitly noted!)
            wy = oy - 22.0
            els.append(f'<line x1="{ox:.1f}" y1="{wy:.1f}" x2="{ox + pw_l:.1f}" y2="{wy:.1f}" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
            els.append(txt(ox + pw_l - 4, wy + 14, f"质子热能 k_BT ≈ {kBT_keV:.1f} keV（纵轴局部放大）", size=9.6, color=BLUE, anchor="end", weight="600", halo=True))

            # Quantum wave: oscillating outside (right), exponentially decaying through barrier, small oscillation inside nuclear well!
            turn_x = ox + 216.0
            wave_pts = []
            for i in range(96):
                wx = ox + pw_l - i * (pw_l / 95.0)
                if wx >= turn_x:
                    amp = 7.5
                    wy_p = wy - amp * math.sin((wx - turn_x) * 0.28)
                elif wx >= r0_px:
                    decay = math.exp(-2.1 * (turn_x - wx) / (turn_x - r0_px))
                    wy_p = wy - 7.5 * decay
                else:
                    amp = 7.5 * math.exp(-2.1)
                    wy_p = wy - amp * math.sin((r0_px - wx) * 0.45)
                wave_pts.append((wx, wy_p))
            els.append(_poly(wave_pts, stroke=PURPLE, sw=2.1))
            els.append(txt(ox + 156, wy - 20, "量子物质波“穿墙”渗入！", size=10.2, color=PURPLE, anchor="middle", weight="700", halo=True))
            els.append(txt(ox + pw_l / 2 + 12, oy + 50, "两颗质子中心间距 r（费米 fm 尺度，非等比例示意）", size=10.0, color=MUTED, anchor="middle"))

            # Right card: Computed Gamow Peak over E in [0.5, 16] keV
            rx, ry, rw, rh = 380, 62, 360, 292
            els.append(card(rx, ry, rw, rh))
            els.append(txt(rx + 16, ry + 23, f"② 能量妥协窗口：算出伽莫夫峰 E₀ ≈ {E0_keV:.1f} keV", size=12.4, color=INK, weight="700"))

            gx0, gy0 = rx + 46.0, ry + 236.0
            gw, gh = 292.0, 146.0
            E_max = 16.0

            def map_e(E_val, y_norm):
                return gx0 + (E_val / E_max) * gw, gy0 - y_norm * gh

            # Grid & ticks
            for e_tick in [0, 4, 8, 12, 16]:
                tx, _ = map_e(e_tick, 0)
                els.append(f'<line x1="{tx:.1f}" y1="{gy0 - gh:.1f}" x2="{tx:.1f}" y2="{gy0:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
                els.append(txt(tx, gy0 + 15, f"{e_tick}", size=10.0, color=MUTED, anchor="middle", cls="mono"))

            els.append(f'<line x1="{gx0:.1f}" y1="{gy0 - gh:.1f}" x2="{gx0:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.3"/>')
            els.append(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx0 + gw:.1f}" y2="{gy0:.1f}" stroke="{SLATE}" stroke-width="1.3"/>')

            # Compute exact normalized curves
            es = [0.35 + (E_max - 0.35) * i / 120.0 for i in range(121)]
            mb_raw = [math.exp(-e / kBT_keV) for e in es]
            tun_raw = [math.exp(-math.sqrt(E_G_keV / e)) for e in es]
            prod_raw = [math.exp(-e / kBT_keV - math.sqrt(E_G_keV / e)) for e in es]

            mb_max = max(mb_raw)
            tun_max = max(tun_raw)
            prod_max = max(prod_raw)

            mb_pts = [map_e(e, v / mb_max) for e, v in zip(es, mb_raw)]
            tun_pts = [map_e(e, v / tun_max) for e, v in zip(es, tun_raw)]
            prod_pts = [map_e(e, 0.92 * (v / prod_max)) for e, v in zip(es, prod_raw)]

            # Shaded polygon under Gamow peak
            poly_fill = f"{gx0:.1f},{gy0:.1f} " + " ".join(f"{x:.1f},{y:.1f}" for x, y in prod_pts) + f" {gx0 + gw:.1f},{gy0:.1f}"
            els.append(f'<polygon points="{poly_fill}" fill="{GREEN_SOFT}" opacity="0.85"/>')

            els.append(_poly(mb_pts, stroke=BLUE, sw=2.0, dash="5 3"))
            els.append(_poly(tun_pts, stroke=PURPLE, sw=2.0, dash="5 3"))
            els.append(_poly(prod_pts, stroke=GREEN, sw=2.6))

            # Peak marker at E0_keV
            px_peak, py_peak = map_e(E0_keV, 0.92)
            els.append(f'<line x1="{px_peak:.1f}" y1="{py_peak:.1f}" x2="{px_peak:.1f}" y2="{gy0:.1f}" stroke="{GREEN}" stroke-width="1.3" stroke-dasharray="3 3"/>')
            els.append(f'<circle cx="{px_peak:.1f}" cy="{py_peak:.1f}" r="4.6" fill="{GREEN}" stroke="#fff" stroke-width="1.3"/>')
            els.append(txt(px_peak + 8, py_peak + 4, f"伽莫夫峰 E₀ ≈ {E0_keV:.1f} keV", size=10.5, color=GREEN, weight="700", halo=True))

            # Curve legends
            els.append(txt(gx0 + 10, gy0 - 96, "热分布 e^(-E/kT)", size=9.8, color=BLUE, weight="600", halo=True))
            els.append(txt(gx0 + gw - 6, gy0 - 96, "隧穿率 e^(-√(E_G/E))", size=9.8, color=PURPLE, anchor="end", weight="600", halo=True))
            els.append(txt(gx0 + gw / 2, gy0 + 32, "质子相对动能 E (keV) —— 聚变全靠高速尾端这撮“幸运儿”！", size=10.0, color=BODY, anchor="middle", weight="600"))
            els.append(txt(rx + 16, gy0 + 48, "注：两条虚线各自按自身最大值归一化，绿色实线为两者相乘的有效聚变窗口。", size=9.6, color=MUTED))

            svg = figure(
                370,
                "太阳核心质子库仑势垒量子隧穿与伽莫夫峰精确计算图",
                f"左图对比约1000 keV库仑静电斥力势垒与k_BT≈{kBT_keV:.1f} keV质子热运动及量子物质波隧穿；右图由麦克斯韦分布与隧穿因子相乘精确算出E0≈{E0_keV:.1f} keV伽莫夫有效聚变窗口。",
                els,
            )
            write_svg(subdir, "gamow-quantum-tunneling.svg", svg)

        # -----------------------------------------------------------------------
        # 3. solar-spectrum-fraunhofer.svg
        # -----------------------------------------------------------------------
        def build_solar_spectrum():
            # Exact Planck blackbody B_lambda(lambda, T=5772 K)
            T_eff = 5772.0
            h_pl = 6.62607015e-34
            c_lt = 2.99792458e8
            k_B = 1.380649e-23
            b_wien_nmK = 2.897771955e6
            lam_peak_nm = b_wien_nmK / T_eff  # 502.04 nm!
            assert abs(lam_peak_nm - 502.04) < 0.2

            # Rayleigh scattering ratio: 450 nm blue vs 650 nm red
            rayleigh_ratio = (650.0 / 450.0) ** 4  # 4.354
            assert 4.3 < rayleigh_ratio < 4.4

            def planck_rel(lam_nm):
                lam_m = lam_nm * 1e-9
                x = (h_pl * c_lt) / (lam_m * k_B * T_eff)
                val = 1.0 / ((lam_m**5) * (math.exp(x) - 1.0))
                return val

            peak_val = planck_rel(lam_peak_nm)

            els = []
            els += header(
                "没去太阳挖一勺，怎么知道它有氢和氦？5772 K 光谱密码与夫琅禾费暗线",
                f"左图绘制 5772 K 普朗克黑体辐射曲线（峰值 {lam_peak_nm:.0f} nm）与元素条形码；右图揭晓蓝天白日与红霞之谜。",
            )

            # Left card: Spectrum + Fraunhofer barcode
            lx, ly, lw, lh = 20, 62, 434, 294
            els.append(card(lx, ly, lw, lh))
            els.append(txt(lx + 16, ly + 23, f"① 阳光的黑体底座 (5772 K) 与夫琅禾费吸收暗线", size=12.4, color=INK, weight="700"))

            sx0, sy0 = lx + 48.0, ly + 198.0
            sw_p, sh_p = 364.0, 114.0
            lam_min, lam_max = 180.0, 1650.0

            def map_lam(lnm, y_norm):
                return sx0 + ((lnm - lam_min) / (lam_max - lam_min)) * sw_p, sy0 - y_norm * sh_p

            # Visible band shading (380..750 nm)
            vx1, _ = map_lam(380.0, 0)
            vx2, _ = map_lam(750.0, 0)
            vis_defs = """
      <linearGradient id="vis-rainbow" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.28"/>
        <stop offset="22%" stop-color="#2563eb" stop-opacity="0.28"/>
        <stop offset="45%" stop-color="#10b981" stop-opacity="0.28"/>
        <stop offset="68%" stop-color="#eab308" stop-opacity="0.30"/>
        <stop offset="100%" stop-color="#ef4444" stop-opacity="0.28"/>
      </linearGradient>
      <linearGradient id="barcode-rainbow" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#6d28d9"/>
        <stop offset="22%" stop-color="#2563eb"/>
        <stop offset="46%" stop-color="#16a34a"/>
        <stop offset="70%" stop-color="#eab308"/>
        <stop offset="84%" stop-color="#f97316"/>
        <stop offset="100%" stop-color="#dc2626"/>
      </linearGradient>"""

            els.append(f'<rect x="{vx1:.1f}" y="{sy0 - sh_p:.1f}" width="{vx2 - vx1:.1f}" height="{sh_p:.1f}" fill="url(#vis-rainbow)"/>')

            # Wavelength ticks
            for lt in [200, 500, 800, 1200, 1600]:
                tx, _ = map_lam(lt, 0)
                els.append(f'<line x1="{tx:.1f}" y1="{sy0 - sh_p:.1f}" x2="{tx:.1f}" y2="{sy0:.1f}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
                els.append(txt(tx, sy0 + 14, f"{lt}", size=9.6, color=MUTED, anchor="middle", cls="mono"))

            els.append(f'<line x1="{sx0:.1f}" y1="{sy0 - sh_p:.1f}" x2="{sx0:.1f}" y2="{sy0:.1f}" stroke="{SLATE}" stroke-width="1.3"/>')
            els.append(f'<line x1="{sx0:.1f}" y1="{sy0:.1f}" x2="{sx0 + sw_p:.1f}" y2="{sy0:.1f}" stroke="{SLATE}" stroke-width="1.3"/>')
            els.append(txt(sx0 + 16, sy0 - 44, "紫外", size=9.6, color=PURPLE, anchor="middle", weight="600", halo=True))
            els.append(txt((vx1 + vx2) / 2, sy0 - 16, "可见光", size=9.8, color=INK, anchor="middle", weight="700", halo=True))
            els.append(txt(sx0 + 266, sy0 - 38, "红外辐射（热量主力）", size=9.8, color=ORANGE, anchor="middle", weight="600", halo=True))
            els.append(txt(sx0 + sw_p / 2 + 40, sy0 + 28, "波长 λ (nm)", size=9.8, color=BODY, anchor="middle", weight="600"))

            # Planck curve with subtle absorption notches at key Fraunhofer lines
            fraunhofer = [
                (393.4, "Ca K", 0.16),
                (434.0, "Hγ", 0.12),
                (486.1, "Hβ", 0.15),
                (589.3, "Na D", 0.13),
                (656.3, "Hα", 0.18),
            ]
            spec_pts = []
            for i in range(180):
                lnm = lam_min + (lam_max - lam_min) * (i / 179.0)
                yn = planck_rel(lnm) / peak_val
                for fl_lam, _, depth in fraunhofer:
                    yn *= 1.0 - depth * math.exp(-((lnm - fl_lam) / 7.5) ** 2)
                spec_pts.append(map_lam(lnm, yn * 0.90))
            els.append(_poly(spec_pts, stroke=INK, sw=2.1))

            # Wien peak marker at 502 nm
            px_w, py_w = map_lam(lam_peak_nm, 0.90)
            els.append(f'<circle cx="{px_w:.1f}" cy="{py_w:.1f}" r="4.2" fill="{GREEN}" stroke="#fff" stroke-width="1.2"/>')
            els.append(txt(px_w + 10, py_w + 3, f"维恩峰值 λ_max ≈ {lam_peak_nm:.0f} nm (蓝绿)", size=10.1, color=GREEN, weight="700", halo=True))

            # Zoomed Visible Fraunhofer Barcode Strip at bottom of left card (380..700 nm across width 374px!)
            bx0, by_bar, bw_bar, bh_bar = lx + 30.0, ly + 250.0, 374.0, 19.0
            els.append(txt(lx + 30, by_bar - 6, "放大可见光条形码（1814 夫琅禾费暗线 / 1925 佩恩证出氢占 >90%）：", size=9.8, color=INK, weight="600"))
            els.append(f'<rect x="{bx0:.1f}" y="{by_bar:.1f}" width="{bw_bar:.1f}" height="{bh_bar:.1f}" rx="4" fill="url(#barcode-rainbow)" stroke="{SLATE}" stroke-width="1"/>')

            barcode_lines = [
                (393.4, "Ca K", "#0f172a", 2.2),
                (396.8, "", "#0f172a", 1.8),
                (410.2, "", "#0f172a", 1.5),
                (434.0, "Hγ", "#0f172a", 1.7),
                (486.1, "Hβ(氢)", "#0f172a", 2.2),
                (517.5, "", "#0f172a", 1.5),
                (587.6, "He(1868氦)", "#fef08a", 2.2),
                (589.3, "Na", "#0f172a", 2.0),
                (656.3, "Hα(氢)", "#0f172a", 2.5),
            ]
            for bl_nm, bl_lbl, bl_col, bl_sw in barcode_lines:
                lx_b = bx0 + ((bl_nm - 380.0) / (700.0 - 380.0)) * bw_bar
                els.append(f'<line x1="{lx_b:.1f}" y1="{by_bar + 1:.1f}" x2="{lx_b:.1f}" y2="{by_bar + bh_bar - 1:.1f}" stroke="{bl_col}" stroke-width="{bl_sw}"/>')
                if bl_lbl:
                    dy_lbl = by_bar + bh_bar + 14
                    if "He" in bl_lbl:
                        els.append(txt(lx_b - 6, dy_lbl, bl_lbl, size=9.4, color=GOLD, anchor="end", weight="700"))
                    elif bl_lbl == "Na":
                        els.append(txt(lx_b + 6, dy_lbl, "Na D", size=9.4, color=SLATE, anchor="start", weight="600"))
                    else:
                        els.append(txt(lx_b, dy_lbl, bl_lbl, size=9.5, color=INK, anchor="middle", weight="600"))

            # Right card: Why isn't the Sun green? Space white vs Blue sky vs Crimson sunset
            rx, ry, rw, rh = 466, 62, 274, 294
            els.append(card(rx, ry, rw, rh))
            els.append(txt(rx + 14, ry + 23, "② 峰值在绿光，太阳为啥不发绿？", size=12.2, color=INK, weight="700"))

            stages = [
                (
                    "太空看太阳：纯白色！",
                    SLATE,
                    SLATE_SOFT,
                    [
                        "5772 K 黑体曲线宽平，红绿蓝",
                        "光子齐备，合成纯正白光。",
                    ],
                ),
                (
                    f"正午地面：瑞利散射 ∝ 1/λ⁴",
                    BLUE,
                    BLUE_SOFT,
                    [
                        f"450nm 蓝光散射是红光的 {rayleigh_ratio:.1f} 倍！",
                        "蓝光染蓝天空，直射光微偏暖黄。",
                    ],
                ),
                (
                    "日出日落：斜穿十余倍大气",
                    ORANGE,
                    ORANGE_SOFT,
                    [
                        "斜穿厚大气，蓝绿光几乎散尽，",
                        "只剩波长最长的金橙与绯红透出！",
                    ],
                ),
            ]
            for si, (stitle, sfg, sbg, slines) in enumerate(stages):
                sy_c = ry + 38 + si * 82
                els.append(card(rx + 14, sy_c, rw - 28, 74, rx=8, fill=sbg, stroke=sfg, sw=1))
                els.append(txt(rx + 24, sy_c + 19, stitle, size=10.7, color=sfg, weight="700"))
                els.append(txt(rx + 24, sy_c + 39, slines[0], size=9.9, color=BODY))
                els.append(txt(rx + 24, sy_c + 56, slines[1], size=9.9, color=BODY))

            svg = figure(
                372,
                "太阳5772K黑体光谱、夫琅禾费吸收暗线与瑞利散射变色原理",
                f"左图计算5772K普朗克黑体辐射曲线（维恩峰值约{lam_peak_nm:.0f}nm）并标出氢Hα/Hβ、钙K、钠D暗线与1868年日食发现的氦D3线；右图解释太空纯白阳光与地面瑞利1/λ⁴散射导致的蓝天及红日落。",
                els,
                extra_defs=vis_defs,
            )
            write_svg(subdir, "solar-spectrum-fraunhofer.svg", svg)

        # -----------------------------------------------------------------------
        # 4. neutrino-oscillation-mystery.svg
        # -----------------------------------------------------------------------
        def build_neutrino_mystery():
            # Exact flux check: L_sun = 3.828e26 W; 26.73 MeV = 4.2826e-12 J produces 2 electron neutrinos!
            # Wait: 4p -> 4He + 2 e+ + 2 nu_e releases 26.73 MeV (~26.15 MeV thermal + ~0.58 MeV carried by 2 pp neutrinos).
            # Let's check exact total solar neutrino flux at 1 AU (d = 1.49598e11 m):
            E_pair_J = 26.73e6 * 1.602176634e-19
            nu_rate_s = 2.0 * (3.828e26 / E_pair_J)  # ~1.79e38 neutrinos/sec emitted by Sun!
            area_1au_cm2 = 4.0 * math.pi * (1.4959787e13) ** 2
            flux_cm2_s = nu_rate_s / area_1au_cm2    # ~6.36e10 cm^-2 s^-1!
            assert 6.0e10 < flux_cm2_s < 6.8e10

            davis_frac = 0.34
            sno_nue = 0.34
            sno_numutau = 0.66
            assert abs((sno_nue + sno_numutau) - 1.00) < 1e-9

            els = []
            els += header(
                "困扰物理学界 30 年的“太阳中微子失踪案”：不是太阳熄火，是半路变脸！",
                "1970 年戴维斯在地下金矿只抓到预测值 1/3 的电子中微子；2001 年 SNO 重水实验揪出另外 2/3 的“马甲”。",
            )

            # Top wide card: Sun -> 1.5亿 km quantum flavor oscillation -> Underground detectors
            els.append(card(20, 62, 720, 146))
            els.append(txt(36, 85, "① 跨越 1.496 亿千米的量子“变脸”之旅（中微子振荡证明中微子具有微小非零质量！）", size=12.2, color=INK, weight="700"))

            # Sun core on left
            scx, scy = 82.0, 144.0
            els.append(f'<circle cx="{scx}" cy="{scy}" r="34" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
            els.append(f'<circle cx="{scx}" cy="{scy}" r="16" fill="#fdba74"/>')
            els.append(txt(scx, scy + 4, "太阳核心", size=10.2, color=INK, anchor="middle", weight="700"))
            els.append(txt(scx, scy + 50, "100% 纯 ν_e 出发", size=10.2, color=ORANGE, anchor="middle", weight="700"))

            # Oscillation curves from x=130 to x=586
            ox0, ox1 = 132.0, 584.0
            oy_mid = 142.0
            amp_o = 34.0

            nue_pts = []
            numu_pts = []
            for i in range(140):
                u = i / 139.0
                xx = ox0 + u * (ox1 - ox0)
                # Damped-to-average / coherent oscillation schematic settling near 1/3 vs 2/3 arrival mixture
                p_e = 0.34 + 0.66 * math.cos(u * 3.5 * math.pi) ** 2 * math.exp(-1.6 * u)
                p_mt = 1.0 - p_e
                nue_pts.append((xx, oy_mid + amp_o * (0.5 - p_e)))
                numu_pts.append((xx, oy_mid + amp_o * (0.5 - p_mt)))

            els.append(f'<line x1="{ox0}" y1="{oy_mid}" x2="{ox1}" y2="{oy_mid}" stroke="{SLATE_SOFT}" stroke-width="1.2" stroke-dasharray="4 3"/>')
            els.append(_poly(numu_pts, stroke=PURPLE, sw=2.1, dash="5 3"))
            els.append(_poly(nue_pts, stroke=BLUE, sw=2.5, cls="nu-wave"))

            els.append(txt(245, 108, "电子中微子 ν_e 比例跌落", size=10.2, color=BLUE, weight="700", halo=True))
            els.append(txt(425, 108, "变身缪子 ν_μ + 陶子 ν_τ (~2/3)", size=10.2, color=PURPLE, weight="700", halo=True))
            els.append(txt((ox0 + ox1) / 2, 194, f"2.3 秒直穿太阳 → 约 8 分 19 秒抵地（每秒约 {flux_cm2_s / 1e10:.1f}×10¹⁰ 颗穿过每平方厘米指甲盖！）", size=10.2, color=SLATE, anchor="middle"))

            # Earth underground mine target on right
            ecx, ecy = 656.0, 142.0
            els.append(f'<circle cx="{ecx}" cy="{ecy}" r="34" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
            els.append(txt(ecx, ecy - 3, "地球深矿井", size=10.2, color=BLUE, anchor="middle", weight="700"))
            els.append(txt(ecx, ecy + 13, "(1.5–2 km 深)", size=9.6, color=SLATE, anchor="middle"))
            els.append(txt(ecx, ecy + 50, "挡住宇宙线干扰", size=10.0, color=MUTED, anchor="middle"))

            # Bottom two comparison cards: Homestake (1970, 2002 Nobel) vs SNO (2001, 2015 Nobel)
            els.append(card(20, 220, 352, 140))
            els.append(pill(34, 232, "② 1970 戴维斯金矿实验（2002 诺奖）", fg=ORANGE, bg=ORANGE_SOFT, w=248, h=22, size=11.2))
            els.append(txt(34, 272, "• 615 吨四氯乙烯干洗剂：ν_e + ³⁷Cl → ³⁷Ar + e⁻", size=10.3, color=BODY))
            els.append(txt(34, 292, "• 盲区：阈值只认【电子中微子 ν_e】，对 ν_μ/ν_τ 全盲！", size=10.3, color=RED, weight="600"))

            # Bar 1: 34% caught, 66% "missing"
            b1x, b1y, b1w = 34.0, 308.0, 316.0
            els.append(f'<rect x="{b1x}" y="{b1y}" width="{b1w}" height="20" rx="5" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
            els.append(f'<rect x="{b1x}" y="{b1y}" width="{b1w * davis_frac:.1f}" height="20" rx="5" fill="{BLUE}"/>')
            els.append(txt(b1x + 10, b1y + 14, "实测 ~34% ν_e", size=10.0, color="#ffffff", weight="700"))
            els.append(txt(b1x + b1w * davis_frac + 14, b1y + 14, "？另外 66% 神秘失踪！", size=10.0, color=RED, weight="700"))
            els.append(txt(34, 347, "整整一个月才从几百吨液体里数出十几颗氩原子！", size=9.8, color=MUTED))

            els.append(card(384, 220, 356, 140))
            els.append(pill(398, 232, "③ 2001 加拿大 SNO 重水破案（2015 诺奖）", fg=GREEN, bg=GREEN_SOFT, w=272, h=22, size=11.2))
            els.append(txt(398, 272, "• 1,000 吨重水 (D₂O) 丙烯酸球 + 9,600 只光电倍增管", size=10.3, color=BODY))
            els.append(txt(398, 292, "• 氘核中性流反应对【全部三味 ν_e+ν_μ+ν_τ】一视同仁！", size=10.3, color=GREEN, weight="600"))

            # Bar 2: 34% nu_e + 66% nu_mu/tau = 100%!
            b2x, b2y, b2w = 398.0, 308.0, 322.0
            w_e = b2w * sno_nue
            w_mt = b2w * sno_numutau
            els.append(f'<rect x="{b2x:.1f}" y="{b2y}" width="{w_e:.1f}" height="20" rx="4" fill="{BLUE}"/>')
            els.append(f'<rect x="{b2x + w_e:.1f}" y="{b2y}" width="{w_mt:.1f}" height="20" rx="4" fill="{PURPLE}"/>')
            els.append(txt(b2x + 8, b2y + 14, "34% ν_e", size=10.0, color="#ffffff", weight="700"))
            els.append(txt(b2x + w_e + 12, b2y + 14, "+ 66% (ν_μ + ν_τ) = 100% 吻合！", size=10.0, color="#ffffff", weight="700"))
            els.append(txt(398, 347, "真相大白：太阳聚变分秒未停，贝特标准太阳模型大获全胜！", size=9.8, color=INK, weight="600"))

            css = """
      .nu-wave {
        stroke-dasharray: 900;
        stroke-dashoffset: 0;
        animation: nuDraw 1.8s ease-out 1 both;
      }
      @keyframes nuDraw {
        from { stroke-dashoffset: 900; }
        to { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .nu-wave { animation: none; }
      }"""

            svg = figure(
                376,
                "太阳中微子失踪案与三味量子振荡破案全图",
                f"上图展示太阳核心100%电子中微子在1.496亿千米飞行中振荡为约1/3电子中微子与2/3缪子/陶子中微子（地球通量约{flux_cm2_s/1e10:.1f}×10¹⁰ cm⁻²s⁻¹）；下图对比1970年戴维斯四氯乙烯实验仅测出34%与2001年SNO重水实验测齐100%三味总量。",
                els,
                extra_css=css,
            )
            write_svg(subdir, "neutrino-oscillation-mystery.svg", svg)

        build_kelvin_lifespan()
        build_gamow_tunneling()
        build_solar_spectrum()
        build_neutrino_mystery()

    def _verify_generated_layout():
        """Static text bounding-box & canvas margin check on our 8 newly built SVGs."""
        targets = [
            IMAGES_ROOT / "flight-physics" / "equal-transit-myth.svg",
            IMAGES_ROOT / "flight-physics" / "lift-speed-altitude.svg",
            IMAGES_ROOT / "flight-physics" / "helicopter-torque-balance.svg",
            IMAGES_ROOT / "flight-physics" / "flight-regimes-map.svg",
            IMAGES_ROOT / "sun-light" / "kelvin-coal-vs-fusion.svg",
            IMAGES_ROOT / "sun-light" / "gamow-quantum-tunneling.svg",
            IMAGES_ROOT / "sun-light" / "solar-spectrum-fraunhofer.svg",
            IMAGES_ROOT / "sun-light" / "neutrino-oscillation-mystery.svg",
        ]
        ns = "{http://www.w3.org/2000/svg}"
        for p in targets:
            assert p.exists(), f"Missing SVG: {p}"
            root = ET.parse(p).getroot()
            w = float(root.attrib["width"])
            h = float(root.attrib["height"])
            assert w == 760.0, f"Expected width=760 in {p}, got {w}"
            boxes = []
            for el in root.iter(f"{ns}text"):
                tx = float(el.attrib["x"])
                ty = float(el.attrib["y"])
                fs = float(el.attrib.get("font-size", "12"))
                anch = el.attrib.get("text-anchor", "start")
                s = "".join(el.itertext())
                est_w = sum(fs * (1.02 if ord(ch) > 127 else 0.58) for ch in s)
                if anch == "middle":
                    x0, x1 = tx - est_w / 2, tx + est_w / 2
                elif anch == "end":
                    x0, x1 = tx - est_w, tx
                else:
                    x0, x1 = tx, tx + est_w
                y0, y1 = ty - fs * 0.82, ty + fs * 0.22
                assert x0 >= 4.0 and x1 <= w - 4.0, f"Text '{s}' out of horizontal bounds [{x0:.1f}, {x1:.1f}] in {p.name}"
                assert y0 >= 4.0 and y1 <= h - 4.0, f"Text '{s}' out of vertical bounds [{y0:.1f}, {y1:.1f}] in {p.name}"
                for ox0, oy0, ox1, oy1, os_txt in boxes:
                    ix = min(x1, ox1) - max(x0, ox0)
                    iy = min(y1, oy1) - max(y0, oy0)
                    if ix > 3.0 and iy > 2.5:
                        raise AssertionError(
                            f"Text overlap in {p.name}: '{s}' ({x0:.1f},{y0:.1f}-{x1:.1f},{y1:.1f}) vs '{os_txt}' ({ox0:.1f},{oy0:.1f}-{ox1:.1f},{oy1:.1f})"
                        )
                boxes.append((x0, y0, x1, y1, s))
        print(f"All {len(targets)} newly generated SVGs passed bounding-box & margin verification!")


_register_flight_and_sun()


def _register_baby_science():
    import math

    from html import escape

    from .core import (
        BG,
        BLUE,
        BLUE_LINE,
        BLUE_SOFT,
        BODY,
        BORDER,
        CARD_BG,
        GREEN,
        GREEN_SOFT,
        HAIRLINE,
        INK,
        LABEL_SIZE,
        MUTED,
        NOTE_SIZE,
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

    SUBDIR = "baby-science"

    def _line(x1, y1, x2, y2, stroke=BORDER, sw=1.2, dash=None, marker=None, opacity=None):
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
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        return f'<line {" ".join(attrs)}/>'

    def _polyline(pts, stroke=BLUE, sw=2.4, fill="none", dash=None, opacity=None, trace=False):
        d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' opacity="{opacity}"' if opacity is not None else ""
        tr = ' pathLength="1" class="trace-line"' if (trace and not dash) else ""
        return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{extra}{op}{tr}/>'

    TRACE_CSS = """
      .trace-line {
        stroke-dasharray: 1;
        stroke-dashoffset: 0;
        animation: drawLine 1.4s ease-out 1 both;
      }
      @keyframes drawLine {
        from { stroke-dashoffset: 1; }
        to { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .trace-line { animation: none; }
      }"""

    def _build_womb_sound_flavor():
        """Post 1 SVG 1: Uterine acoustic dB low-pass attenuation + DeCasper & Mennella experiments."""
        els = []
        els.extend(
            header(
                "子宫里的声学与风味实验室：宝宝隔着肚皮到底记住了什么？",
                "左图据 Querleu (1988) 与 Gerhardt & Abrams (2000) 绘制声衰减趋势；右图拆解两项产前记忆经典实验。",
            )
        )

        # Left card: Uterine low-pass filter curve across log10(f)
        lx, ly, lw, lh = 20, 64, 352, 332
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① 腹壁与羊水的低通滤波（100–4000 Hz）", size=PANEL_TITLE, color=INK, weight="700"))

        px0, px1 = lx + 50, lx + lw - 22  # 70 .. 350 (width 280)
        py0, py1 = ly + 56, ly + 216      # 120 .. 280 (height 160), 0 dB at py0, -32 dB at py1
        f_min, f_max = 80.0, 4500.0

        def fx(freq):
            return px0 + (math.log10(freq) - math.log10(f_min)) / (math.log10(f_max) - math.log10(f_min)) * (px1 - px0)

        def dy(db_loss):
            # db_loss in [0, 32] where 0 = top (no loss), 32 = bottom (-32 dB)
            return py0 + (db_loss / 32.0) * (py1 - py0)

        # Smooth logistic-log acoustic attenuation model anchored to Querleu 1988 / Gerhardt & Abrams 2000:
        # ~3.5 dB at 100 Hz, ~5.0 dB at 250 Hz, ~8.0 dB at 500 Hz, ~14.5 dB at 1000 Hz, ~26.5 dB at 4000 Hz
        def ut_loss(freq):
            u = math.log10(freq)
            return 2.6 + 27.4 / (1.0 + math.exp(-3.15 * (u - 3.08)))

        assert 3.0 <= ut_loss(100) <= 4.5
        assert 6.5 <= ut_loss(500) <= 10.5
        assert 13.0 <= ut_loss(1000) <= 16.5
        assert 24.5 <= ut_loss(4000) <= 29.0
        assert ut_loss(100) < ut_loss(300) < ut_loss(1000) < ut_loss(4000)

        # Shaded passband (100-300 Hz) and muffled high-freq band (1000-4000 Hz)
        x_100, x_300, x_1000, x_4000 = fx(100), fx(300), fx(1000), fx(4000)
        els.append(
            f'<rect x="{x_100:.1f}" y="{py0:.1f}" width="{x_300 - x_100:.1f}" height="{py1 - py0:.1f}" '
            f'fill="{GREEN_SOFT}" opacity="0.75"/>'
        )
        els.append(
            f'<rect x="{x_1000:.1f}" y="{py0:.1f}" width="{x_4000 - x_1000:.1f}" height="{py1 - py0:.1f}" '
            f'fill="{ORANGE_SOFT}" opacity="0.65"/>'
        )

        # Grid lines
        for db in (0, 10, 20, 30):
            yy = dy(db)
            els.append(_line(px0, yy, px1, yy, stroke=BORDER if db > 0 else SLATE, sw=1.0, dash="3 3" if db > 0 else None))
            lbl = "0 dB" if db == 0 else f"-{db}"
            els.append(txt(px0 - 6, yy + 4, lbl, size=10.5, color=MUTED, anchor="end", cls="mono"))

        for freq, flbl in [(100, "100Hz"), (300, "300Hz"), (1000, "1kHz"), (4000, "4kHz")]:
            xx = fx(freq)
            els.append(_line(xx, py0, xx, py1, stroke=HAIRLINE, sw=0.9, dash="2 3"))
            els.append(txt(xx, py1 + 16, flbl, size=10.5, color=MUTED, anchor="middle", cls="mono"))

        els.append(_line(px0, py0, px0, py1, stroke=SLATE, sw=1.2))
        els.append(_line(px0, py1, px1, py1, stroke=SLATE, sw=1.2))

        # Sample curve
        freqs = [f_min * ((f_max / f_min) ** (i / 80.0)) for i in range(81)]
        pts = [(fx(f), dy(ut_loss(f))) for f in freqs]
        els.append(_polyline(pts, stroke=BLUE, sw=2.8, trace=True))

        # Anchor points
        for f_pt, col in [(120, GREEN), (250, GREEN), (500, BLUE), (1000, ORANGE), (4000, ORANGE)]:
            cx, cy = fx(f_pt), dy(ut_loss(f_pt))
            els.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{col}" stroke="#ffffff" stroke-width="1.3"/>')

        els.append(txt((x_100 + x_300) / 2, py0 + 96, "低频穿透窗", size=10.8, color=GREEN, anchor="middle", weight="700", halo=True))
        els.append(txt((x_100 + x_300) / 2, py0 + 112, "嗓音基频/语调", size=10.2, color=GREEN, anchor="middle", halo=True))
        els.append(txt((x_100 + x_300) / 2, py0 + 127, "仅衰减 3–5 dB", size=10.0, color=BODY, anchor="middle", halo=True))

        els.append(txt((x_1000 + x_4000) / 2, py0 + 22, "高频大幅闷住", size=10.8, color=ORANGE, anchor="middle", weight="700", halo=True))
        els.append(txt((x_1000 + x_4000) / 2, py0 + 37, "清辅音 s / t / f", size=10.2, color=ORANGE, anchor="middle", halo=True))
        els.append(txt((x_1000 + x_4000) / 2, py0 + 52, "衰减 15–30 dB", size=10.0, color=BODY, anchor="middle", halo=True))

        els.append(txt((px0 + px1) / 2, py1 + 33, "声音频率（对数刻度）", size=10.8, color=SLATE, anchor="middle"))

        # Bottom takeaway inside left card
        els.append(card(lx + 14, ly + 256, lw - 28, 62, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(lx + 26, ly + 276, "妈妈胸腔骨传导 + 低频透射 = 听清“旋律节拍”", size=11.2, color=BLUE, weight="700"))
        els.append(txt(lx + 26, ly + 294, "• 胎儿记住的是语调起伏，不是背单词或变音乐神童", size=10.5, color=BODY))
        els.append(txt(lx + 26, ly + 310, "• 切勿把耳机/喇叭紧贴肚皮开大音量，自然聊天最安全", size=10.5, color=ORANGE, weight="600"))

        # Right card: Two landmark prenatal learning experiments
        rx, ry, rw, rh = 388, 64, 352, 332
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 16, ry + 24, "② 刚出生不会说话，科学家怎么测“产前记忆”？", size=PANEL_TITLE, color=INK, weight="700"))

        # Sub-card A: DeCasper & Fifer (1980) + DeCasper & Spence (1986)
        els.append(card(rx + 14, ry + 38, rw - 28, 136, rx=8, fill= SLATE_SOFT, stroke=BORDER))
        els.append(pill(rx + 24, ry + 48, "实验 A · 听觉韵律", fg=BLUE, bg=BLUE_SOFT, w=116, h=20, size=11))
        els.append(txt(rx + 148, ry + 62, "DeCasper 压力传感奶嘴实验", size=11.8, color=INK, weight="700"))
        els.append(txt(rx + 24, ry + 84, "装置：无营养安抚奶嘴连气压传感器，出生 <72 小时新生儿", size=10.5, color=BODY))
        els.append(txt(rx + 24, ry + 100, "可通过改变“吸吮停顿节律”自主切换耳机里的两段录音：", size=10.5, color=BODY))

        # Mini two-row outcome bars in Sub-card A
        els.append(card(rx + 24, ry + 110, rw - 48, 54, rx=6, fill=CARD_BG, stroke=HAIRLINE))
        els.append(txt(rx + 32, ry + 128, "1980 Science：", size=10.4, color=BLUE, weight="700"))
        els.append(txt(rx + 114, ry + 128, "妈妈声音 vs 陌生女性 → 主动吸吮选妈妈", size=10.2, color=BODY))
        els.append(txt(rx + 32, ry + 148, "1986 童谣实验：", size=10.4, color=PURPLE, weight="700"))
        els.append(txt(rx + 114, ry + 148, "孕末6周读童谣，换陌生人朗读仍偏爱！", size=10.2, color=BODY))

        # Sub-card B: Mennella et al. (2001) Carrot Juice RCT
        els.append(card(rx + 14, ry + 186, rw - 28, 132, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(pill(rx + 24, ry + 196, "实验 B · 羊水风味", fg=ORANGE, bg="#ffffff", w=110, h=20, size=10.6))
        els.append(txt(rx + 142, ry + 210, "Mennella 胡萝卜汁实验 (2001)", size=11.3, color=INK, weight="700"))
        els.append(txt(rx + 24, ry + 231, "孕晚期连喝 3 周胡萝卜汁 → 风味进入羊水被胎儿吞咽，", size=10.3, color=BODY))
        els.append(txt(rx + 24, ry + 247, "提前尝到“妈妈餐桌的味道”（对照白水组未接触）。", size=10.3, color=BODY))

        # Quantitative bar schematic of negative facial expressions at weaning (~5.5-6m)
        els.append(card(rx + 24, ry + 257, rw - 48, 52, rx=6, fill=CARD_BG, stroke=HAIRLINE))
        els.append(txt(rx + 34, ry + 275, "初添胡萝卜米糊皱眉抗拒：", size=10.4, color=SLATE, weight="600"))
        # Control bar vs Prenatal carrot bar (schematic proportional representation of Mennella 2001 Fig 1: ~5.4 vs ~3.4 negative faces)
        els.append(txt(rx + 34, ry + 295, "孕期白水组", size=10.2, color=MUTED))
        els.append(f'<rect x="{rx + 96}" y="{ry + 285}" width="78" height="11" rx="3" fill="{SLATE}" opacity="0.55"/>')
        els.append(txt(rx + 186, ry + 295, "孕期胡萝卜组", size=10.2, color=GREEN, weight="700"))
        els.append(f'<rect x="{rx + 256}" y="{ry + 285}" width="46" height="11" rx="3" fill="{GREEN}"/>')
        els.append(txt(rx + 306, ry + 295, "更少!", size=10.2, color=GREEN, weight="700"))

        svg = figure(
            412,
            "子宫声学低通滤波曲线与产前听觉风味学习经典实验图解",
            "左图展示100至4000赫兹声音穿过腹壁与羊水的分贝衰减曲线，100至300赫兹语调基频仅衰减3至5分贝而高频大幅衰减；右图拆解DeCasper压力奶嘴童谣实验与Mennella胡萝卜汁羊水风味实验。",
            els,
            extra_css=TRACE_CSS,
        )
        write_svg(SUBDIR, "womb-sound-flavor-lab.svg", svg)

    def _build_parental_brain_transition():
        """Post 1 SVG 2: Maternal & paternal brain neuroplasticity + normal mixed emotions vs >=2-week screening."""
        els = []
        els.extend(
            header(
                "准父母的大脑也在“备产”：神经可塑性重塑与围产期情绪支持边界",
                "左图综合纵向脑成像证据（Hoekzema 2017; Martínez-García 2023）；右图区分常见情绪波动与 ≥2 周求助信号。",
            )
        )

        # Left panel: Dual neuroplasticity timeline
        lx, ly, lw, lh = 20, 64, 352, 324
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① “父母脑”不是天生满级，而是生物+实战重塑", size=PANEL_TITLE, color=INK, weight="700"))

        # Timeline axis
        tx0, tx1, ty = lx + 36, lx + lw - 30, ly + 56
        els.append(_line(tx0, ty, tx1, ty, stroke=BLUE, sw=2.0, marker="arr-blue"))
        stages = [(0.0, "孕期"), (0.36, "分娩/初生"), (0.68, "产后6月"), (0.96, "产后2年+")]
        for frac, slbl in stages:
            sx = tx0 + frac * (tx1 - tx0)
            els.append(f'<circle cx="{sx:.1f}" cy="{ty:.1f}" r="3.8" fill="{CARD_BG}" stroke="{BLUE}" stroke-width="1.8"/>')
            els.append(txt(sx, ty - 9, slbl, size=10.2, color=SLATE, anchor="middle", weight="600"))

        # Maternal card
        els.append(card(lx + 14, ly + 72, lw - 28, 114, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(pill(lx + 24, ly + 82, "妈妈大脑 · 激素与妊娠驱动", fg=PURPLE, bg="#ffffff", w=164, h=20, size=10.8))
        els.append(txt(lx + 24, ly + 118, "• Hoekzema 等（2017, Nature Neuroscience）纵向 MRI：", size=10.5, color=INK, weight="700"))
        els.append(txt(lx + 24, ly + 136, "  社会认知网络（内侧前额叶/颞顶区）灰质体积发生高度一致", size=10.4, color=BODY))
        els.append(txt(lx + 24, ly + 152, "  的“突触修剪精简”——不是变笨，而是提高读懂宝宝表情", size=10.4, color=BODY))
        els.append(txt(lx + 24, ly + 168, "  与哭声信号的效率，预测产后依恋质量并持续至少 2 年。", size=10.4, color=PURPLE, weight="600"))

        # Paternal card
        els.append(card(lx + 14, ly + 198, lw - 28, 114, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(pill(lx + 24, ly + 208, "爸爸大脑 · 实战带娃点亮", fg=BLUE, bg="#ffffff", w=156, h=20, size=10.8))
        els.append(txt(lx + 24, ly + 244, "• Martínez-García（2023）与 Abraham 等（2014, PNAS）：", size=10.5, color=INK, weight="700"))
        els.append(txt(lx + 24, ly + 262, "  新手爸爸默认网络与视觉皮层同样出现结构可塑性精简；", size=10.4, color=BODY))
        els.append(txt(lx + 24, ly + 278, "  直接换尿布、哄睡、陪玩时间越长，杏仁核与颞上沟（STS）", size=10.4, color=BODY))
        els.append(txt(lx + 24, ly + 294, "  共情回路连接越强——“默契奶爸”是亲手带出来的！", size=10.4, color=BLUE, weight="600"))

        # Right panel: Normal ambivalence / Baby blues vs >=2-week clinical help-seeking
        rx, ry, rw, rh = 388, 64, 352, 324
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 16, ry + 24, "② 心理过渡光谱：接纳矛盾感受 vs 识别预警线", size=PANEL_TITLE, color=INK, weight="700"))

        # Zone 1: Normal fluctuations
        els.append(card(rx + 14, ry + 40, rw - 28, 118, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(step_badge(rx + 32, ry + 58, "✓", fg=GREEN, bg="#ffffff", r=9.5))
        els.append(txt(rx + 48, ry + 62, "常见适应波动（可与伴侣坦诚倾诉分担）", size=11.5, color=GREEN, weight="700"))
        els.append(txt(rx + 26, ry + 84, "• 孕期矛盾感：既满怀期待挑小衣服，又半夜担心“生活失控”", size=10.4, color=BODY))
        els.append(txt(rx + 26, ry + 102, "• 产后短暂低落（Baby Blues）：产后 3–5 天激素骤降+缺觉，", size=10.4, color=BODY))
        els.append(txt(rx + 26, ry + 120, "  易流泪、脆弱敏感，通常在 1–2 周内随休息与支持自然缓和", size=10.4, color=BODY))
        els.append(txt(rx + 26, ry + 140, "• 应对：用“三行沟通表”把模糊焦虑变成具体可分担的小事", size=10.4, color=GREEN, weight="600"))

        # Zone 2: >=2-week screening boundary (WHO / ACOG / Paulson 2010 JAMA)
        els.append(card(rx + 14, ry + 170, rw - 28, 142, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(step_badge(rx + 32, ry + 188, "!", fg=ORANGE, bg="#ffffff", r=9.5))
        els.append(txt(rx + 48, ry + 192, "专业求助分水岭：症状持续 ≥ 2 周或影响功能", size=11.5, color=ORANGE, weight="700"))
        els.append(txt(rx + 26, ry + 214, "• 并非罕见：约 10%–13% 孕产妇（WHO）与约 10.4% 新手爸", size=10.2, color=INK, weight="600"))
        els.append(txt(rx + 26, ry + 231, "  （Paulson 2010 JAMA 荟萃分析）经历围产期抑郁或焦虑", size=10.2, color=BODY))
        els.append(txt(rx + 26, ry + 249, "• 信号：持续两周以上情绪麻木低落、对一切丧失兴趣、即使", size=10.2, color=BODY))
        els.append(txt(rx + 26, ry + 266, "  有人替班仍彻夜难眠、强烈自责，或闪过伤己/伤婴念头", size=10.2, color=BODY))
        els.append(txt(rx + 26, ry + 286, "• 行动：产检/产后门诊主动做 EPDS 量表筛查，科学干预可治", size=10.2, color=ORANGE, weight="700"))

        svg = figure(
            404,
            "准父母大脑神经可塑性时间轴与围产期情绪筛查边界图",
            "左图展示妈妈在妊娠激素驱动下的社会认知灰质修剪与爸爸在直接育儿经验驱动下的共情网络增强；右图对比常见孕产期情绪波动与持续两周以上的围产期抑郁焦虑筛查信号。",
            els,
        )
        write_svg(SUBDIR, "parental-brain-transition.svg", svg)

    def _build_infant_vision_stages():
        """Post 2 SVG 1: 4-panel computed infant visual acuity, contrast, color & stereo progression (0-12m)."""
        els = []
        els.extend(
            header(
                "一岁以内的视觉升级之路：从 20/400 柔焦黑白，到立体彩色世界",
                "综合美国视光学会（AOA）与眼科视锐度里程碑（AAO EyeWiki / Norcia & Tyler）按比例绘制视觉示意。",
            )
        )

        extra_defs = """
      <filter id="vblur-0m" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3.4"/>
      </filter>
      <filter id="vblur-2m" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="1.8"/>
      </filter>
      <filter id="vblur-6m" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="0.7"/>
      </filter>
      <clipPath id="vport-0"><rect x="32" y="102" width="146" height="92" rx="8"/></clipPath>
      <clipPath id="vport-1"><rect x="215" y="102" width="146" height="92" rx="8"/></clipPath>
      <clipPath id="vport-2"><rect x="398" y="102" width="146" height="92" rx="8"/></clipPath>
      <clipPath id="vport-3"><rect x="581" y="102" width="146" height="92" rx="8"/></clipPath>"""

        stages = [
            {
                "idx": 0,
                "age": "0–1 个月",
                "snellen": "约 20/400",
                "ratio": 20.0 / 400.0,
                "filt": ' filter="url(#vblur-0m)"',
                "bg": "#e2e8f0",
                "skin": "#cbd5e1",
                "cheek": "#cbd5e1",
                "ball1": "#94a3b8",
                "ball2": "#64748b",
                "accent": SLATE,
                "line1": "焦距仅 20–25 cm",
                "line2": "柔和色彩糊成一片，唯独",
                "line3": "黑白高对比轮廓与人脸发际",
                "line4": "最醒目（非故意不理人）",
            },
            {
                "idx": 1,
                "age": "2–3 个月",
                "snellen": "约 20/200",
                "ratio": 20.0 / 200.0,
                "filt": ' filter="url(#vblur-2m)"',
                "bg": "#eef2f6",
                "skin": "#e5cbb8",
                "cheek": "#dda79c",
                "ball1": "#bf7a6b",
                "ball2": "#7b9eb8",
                "accent": BLUE,
                "line1": "双眼协同追视起步",
                "line2": "从偶发斗鸡眼过渡到两眼",
                "line3": "组队锁定爸妈眼睛与口型，",
                "line4": "开始顺滑追随移动玩具",
            },
            {
                "idx": 2,
                "age": "5–8 个月",
                "snellen": "约 20/120",
                "ratio": 20.0 / 120.0,
                "filt": ' filter="url(#vblur-6m)"',
                "bg": "#eaf4fb",
                "skin": "#f6d2b8",
                "cheek": "#f29b8e",
                "ball1": "#e0523c",
                "ball2": "#2589bd",
                "accent": ORANGE,
                "line1": "彩色视觉 + 3D 深度感",
                "line2": "约 5 月龄双眼视差合成立体",
                "line3": "景深（AOA），色彩饱和清",
                "line4": "晰，支撑精准伸手与爬行",
            },
            {
                "idx": 3,
                "age": "9–12 个月",
                "snellen": "约 20/60",
                "ratio": 20.0 / 60.0,
                "filt": "",
                "bg": "#e7f6ee",
                "skin": "#f8d5bb",
                "cheek": "#f48c7f",
                "ball1": "#e04832",
                "ball2": "#1d6fa5",
                "accent": GREEN,
                "line1": "精细捏取与远近预判",
                "line2": "看清地毯碎屑与绘本细节，",
                "line3": "拇食指对捏（Pincer），",
                "line4": "约 2 岁趋近成人 20/20",
            },
        ]

        assert stages[0]["ratio"] < stages[1]["ratio"] < stages[2]["ratio"] < stages[3]["ratio"]

        cw, gap = 171, 12
        cy_card, ch_card = 64, 228
        for s in stages:
            i = s["idx"]
            cx = 20 + i * (cw + gap)
            els.append(card(cx, cy_card, cw, ch_card, stroke=s["accent"] if i >= 2 else BORDER, sw=1.2 if i >= 2 else 1))
            els.append(txt(cx + 12, cy_card + 21, s["age"], size=12.2, color=INK, weight="700"))
            els.append(pill(cx + cw - 76, cy_card + 7, s["snellen"], fg=s["accent"], bg=SLATE_SOFT, w=66, h=19, size=10.2))

            # Simulated scene viewport (146 x 92) at (cx+12, 102)
            vx, vy, vw, vh = cx + 12, 102, 146, 92
            els.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="8" fill="{s["bg"]}" stroke="{HAIRLINE}"/>')

            # Scene inside clipPath: parent smiling face + high-contrast stripes on left + colorful toy ball on right
            fcx, fcy = vx + 72, vy + 50
            scene = [
                f'<g clip-path="url(#vport-{i})">',
                f'  <g{s["filt"]}>',
                # High-contrast black-and-white grating strip on left (visible even under newborn blur!)
                f'    <rect x="{vx + 6}" y="{vy + 12}" width="24" height="68" fill="#ffffff"/>',
                f'    <rect x="{vx + 6}" y="{vy + 12}" width="24" height="14" fill="#0f172a"/>',
                f'    <rect x="{vx + 6}" y="{vy + 40}" width="24" height="14" fill="#0f172a"/>',
                f'    <rect x="{vx + 6}" y="{vy + 66}" width="24" height="14" fill="#0f172a"/>',
                # Parent hair + face
                f'    <circle cx="{fcx}" cy="{fcy - 4}" r="28" fill="#1e293b"/>',
                f'    <circle cx="{fcx}" cy="{fcy + 2}" r="23" fill="{s["skin"]}"/>',
                f'    <circle cx="{fcx - 8}" cy="{fcy - 2}" r="2.8" fill="#0f172a"/>',
                f'    <circle cx="{fcx + 8}" cy="{fcy - 2}" r="2.8" fill="#0f172a"/>',
                f'    <circle cx="{fcx - 13}" cy="{fcy + 6}" r="4" fill="{s["cheek"]}" opacity="0.65"/>',
                f'    <circle cx="{fcx + 13}" cy="{fcy + 6}" r="4" fill="{s["cheek"]}" opacity="0.65"/>',
                f'    <path d="M{fcx - 8},{fcy + 8} Q{fcx},{fcy + 16} {fcx + 8},{fcy + 8}" fill="none" stroke="#0f172a" stroke-width="2.2" stroke-linecap="round"/>',
                # Colorful dual-tone toy ball on right
                f'    <circle cx="{vx + 122}" cy="{vy + 60}" r="14" fill="{s["ball1"]}"/>',
                f'    <path d="M{vx + 110},{vy + 54} Q{vx + 122},{vy + 66} {vx + 134},{vy + 54}" fill="none" stroke="{s["ball2"]}" stroke-width="4"/>',
                "  </g>",
            ]
            if i >= 2:
                # Stereo depth badge in corner once binocular depth turns on at ~5m
                scene.append(f'  <rect x="{vx + 104}" y="{vy + 8}" width="36" height="16" rx="4" fill="#ffffff" opacity="0.9"/>')
                scene.append(f'  <text x="{vx + 122}" y="{vy + 19.5}" font-size="9.8" fill="{s["accent"]}" text-anchor="middle" font-weight="700">3D景深</text>')
            scene.append("</g>")
            els.append("\n".join(scene))
            els.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="8" fill="none" stroke="{HAIRLINE}"/>')

            els.append(txt(cx + 12, 213, s["line1"], size=11.2, color=s["accent"], weight="700"))
            els.append(txt(cx + 12, 232, s["line2"], size=10.4, color=BODY))
            els.append(txt(cx + 12, 248, s["line3"], size=10.4, color=BODY))
            els.append(txt(cx + 12, 264, s["line4"], size=10.4, color=MUTED))

        # Bottom quantitative acuity bar (0m -> 24m relative spatial resolution = 20 / denom)
        bx, by, bw, bh = 20, 304, 720, 96
        els.append(card(bx, by, bw, bh))
        els.append(txt(bx + 16, by + 22, "⑤ 空间分辨率量化演进（以成人 20/20 标准视力 = 100% 计）与儿保就医红线", size=12.4, color=INK, weight="700"))

        milestones = [
            ("初生", "20/400", 0.05, SLATE, SLATE_SOFT),
            ("4个月", "20/200", 0.10, BLUE, BLUE_SOFT),
            ("6个月", "20/120", 0.167, ORANGE, ORANGE_SOFT),
            ("1岁", "20/60", 0.333, GREEN, GREEN_SOFT),
            ("2岁", "20/20", 1.00, PURPLE, PURPLE_SOFT),
        ]
        col_x0, col_step = bx + 20, 86
        max_bar_h = 34.0
        base_y = by + 72
        els.append(_line(col_x0 - 4, base_y, col_x0 + 4 * col_step + 68, base_y, stroke=HAIRLINE, sw=1.1))
        for idx_m, (m_age, m_sn, mval, mcol, mbg) in enumerate(milestones):
            cx_m = col_x0 + idx_m * col_step
            bh_m = max(3.0, mval * max_bar_h)
            els.append(f'<rect x="{cx_m + 14:.1f}" y="{base_y - bh_m:.1f}" width="36" height="{bh_m:.1f}" rx="3" fill="{mbg}" stroke="{mcol}" stroke-width="1.3"/>')
            els.append(txt(cx_m + 32, base_y - bh_m - 4, f"{mval * 100:.0f}%", size=9.8, color=mcol, anchor="middle", weight="700", cls="mono"))
            els.append(txt(cx_m + 32, base_y + 15, f"{m_age} {m_sn}", size=9.6, color=BODY, anchor="middle"))

        # Clinical red-flag box on right side of bottom strip
        els.append(card(bx + 464, by + 14, 242, 70, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(bx + 476, by + 33, "儿保眼科及时就诊信号（AOA）：", size=10.8, color=ORANGE, weight="700"))
        els.append(txt(bx + 476, by + 51, "• 3–4月后仍不追视，或单/双眼恒定斜视", size=10.2, color=BODY))
        els.append(txt(bx + 476, by + 68, "• 瞳孔出现白色反光、畏光流泪或红肿分泌物", size=10.2, color=BODY))

        svg = figure(
            416,
            "0至12个月婴儿视锐度、对比度、色彩与立体深度知觉四阶段演进图",
            "上方四张卡片按20/400、20/200、20/120、20/60视锐度比例展示新生儿至1岁视觉清晰度、黑白条纹敏感度、彩色与立体景深开启过程；下方给出相对成人20/20分辨率比例轴与AOA眼科就医信号。",
            els,
            extra_defs=extra_defs,
        )
        write_svg(SUBDIR, "infant-vision-stages.svg", svg)

    def _build_lantern_vs_spotlight():
        """Post 2 SVG 2: Gopnik Lantern vs Spotlight attention + Baillargeon 1985 Violation-of-Expectation data."""
        els = []
        els.extend(
            header(
                "婴儿不是“低配版大人”：灯笼意识广角采数 vs 直觉物理学家实验",
                "左图对比 Gopnik（2009）注意模型；右图绘制 Baillargeon 等（1985）5 月龄遮挡物理实验实测时长。",
            )
        )

        # Left panel: Adult Spotlight vs Baby Lantern
        lx, ly, lw, lh = 20, 64, 352, 332
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① 探照灯意识 vs 灯笼意识（Gopnik 2009）", size=PANEL_TITLE, color=INK, weight="700"))

        # Top box: Adult Spotlight
        els.append(card(lx + 14, ly + 38, lw - 28, 134, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(lx + 26, ly + 58, "成人：探照灯注意（Spotlight）", size=11.6, color=SLATE, weight="700"))
        # Narrow spotlight beam from (lx+58, ly+114) toward target at (lx+210, ly+104)
        ax, ay = lx + 56, ly + 114
        els.append(f'<polygon points="{ax},{ay} {lx + 214},{ly + 82} {lx + 214},{ly + 132}" fill="#fde68a" opacity="0.55"/>')
        els.append(f'<circle cx="{ax}" cy="{ay}" r="14" fill="{CARD_BG}" stroke="{SLATE}" stroke-width="1.8"/>')
        els.append(txt(ax, ay + 4, "成人", size=10.2, color=SLATE, anchor="middle", weight="700"))
        # Target in beam
        els.append(card(lx + 206, ly + 91, 114, 32, rx=6, fill=CARD_BG, stroke=ORANGE, sw=1.4))
        els.append(txt(lx + 263, ly + 111, "唯一目标：赶时间", size=10.6, color=ORANGE, anchor="middle", weight="700"))
        # Ignored background stimuli (faded)
        els.append(txt(lx + 112, ly + 78, "× 树叶光斑（屏蔽）", size=10.0, color="#94a3b8"))
        els.append(txt(lx + 112, ly + 154, "× 桌角反光（屏蔽）", size=10.0, color="#94a3b8"))
        els.append(txt(lx + 228, ly + 154, "前额叶强抑制过滤", size=10.2, color=SLATE, weight="600"))

        # Bottom box: Infant Lantern Consciousness (360 deg radial waves)
        els.append(card(lx + 14, ly + 182, lw - 28, 140, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(lx + 26, ly + 202, "婴儿：灯笼意识（Lantern Consciousness）", size=11.6, color=BLUE, weight="700"))
        bcx, bcy = lx + 176, ly + 258
        for r_ring, op in [(52, 0.22), (36, 0.35), (21, 0.55)]:
            els.append(f'<circle cx="{bcx}" cy="{bcy}" r="{r_ring}" fill="#bae6fd" stroke="{BLUE}" stroke-width="1" stroke-dasharray="3 3" opacity="{op + 0.3}"/>')
        els.append(f'<circle cx="{bcx}" cy="{bcy}" r="14" fill="#fef08a" stroke="{ORANGE}" stroke-width="1.8"/>')
        els.append(txt(bcx, bcy + 4, "宝宝", size=10.2, color=INK, anchor="middle", weight="700"))

        # 4 radial sensory nodes around the lantern
        nodes = [
            (bcx - 108, bcy - 26, "光影与边缘统计"),
            (bcx + 108, bcy - 26, "唇舌高分辨触觉"),
            (bcx - 108, bcy + 30, "语音节拍与重音"),
            (bcx + 108, bcy + 30, "因果与遮挡规律"),
        ]
        for nx, ny, nlbl in nodes:
            els.append(txt(nx, ny, nlbl, size=10.2, color=INK, anchor="middle", weight="600", halo=True))
        els.append(txt(bcx, ly + 312, "前额叶过滤尚未锁死 → 360° 全景吸收环境规律", size=10.3, color=BLUE, anchor="middle", weight="600"))

        # Right panel: Baillargeon, Spelke & Wasserman (1985) Drawbridge Violation-of-Expectation
        rx, ry, rw, rh = 388, 64, 352, 332
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 16, ry + 24, "② 违反预期实验：5 月龄直觉物理学家", size=PANEL_TITLE, color=INK, weight="700"))

        # Top schematic: Possible (112 deg stop) vs Impossible (180 deg pass-through)
        els.append(card(rx + 14, ry + 38, rw - 28, 126, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(rx + 26, ry + 57, "Baillargeon 等（1985, Cognition）吊桥挡板实验：", size=10.8, color=INK, weight="700"))

        # Left mini-scene: Possible event (screen stops at 112 deg against solid block)
        s1_cx, s1_cy = rx + 96, ry + 132
        els.append(_line(s1_cx - 56, s1_cy, s1_cx + 52, s1_cy, stroke=SLATE, sw=1.8))
        # Hidden solid block behind pivot
        els.append(f'<rect x="{s1_cx + 12}" y="{s1_cy - 28}" width="22" height="28" rx="3" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append(txt(s1_cx + 23, s1_cy - 11, "木块", size=9.5, color=ORANGE, anchor="middle", weight="700"))
        # Drawbridge rotated 112 deg from left (-180 deg) -> angle from +x is 180 - 112 = 68 deg
        ang_pos = math.radians(68)
        els.append(_line(s1_cx, s1_cy, s1_cx + 42 * math.cos(ang_pos), s1_cy - 42 * math.sin(ang_pos), stroke=BLUE, sw=3.2))
        els.append(f'<circle cx="{s1_cx}" cy="{s1_cy}" r="3.5" fill="{INK}"/>')
        els.append(txt(s1_cx - 4, ry + 80, "A 可能：112° 被挡停", size=10.2, color=BLUE, anchor="middle", weight="700"))
        els.append(txt(s1_cx - 4, s1_cy + 18, "符合“固体不可穿透”", size=9.8, color=MUTED, anchor="middle"))

        # Right mini-scene: Impossible event (screen rotates full 180 deg flat right through ghost block!)
        s2_cx, s2_cy = rx + 254, ry + 132
        els.append(_line(s2_cx - 52, s2_cy, s2_cx + 56, s2_cy, stroke=SLATE, sw=1.8))
        els.append(f'<rect x="{s2_cx + 12}" y="{s2_cy - 28}" width="22" height="28" rx="3" fill="none" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="3 2"/>')
        els.append(_line(s2_cx, s2_cy - 2, s2_cx + 46, s2_cy - 2, stroke=PURPLE, sw=3.4))
        els.append(f'<path d="M{s2_cx - 32},{s2_cy - 6} A34,34 0 0,1 {s2_cx + 34},{s2_cy - 6}" fill="none" stroke="{PURPLE}" stroke-width="1.3" stroke-dasharray="3 2" marker-end="url(#arr-muted)"/>')
        els.append(f'<circle cx="{s2_cx}" cy="{s2_cy}" r="3.5" fill="{INK}"/>')
        els.append(txt(s2_cx + 2, ry + 80, "B 不可能：180° 穿模!", size=10.2, color=PURPLE, anchor="middle", weight="700"))
        els.append(txt(s2_cx + 2, s2_cy + 18, "木块暗中移走，似被穿过", size=9.8, color=MUTED, anchor="middle"))

        # Quantitative bar chart: 25.11s vs 33.07s
        t_possible = 25.11
        t_impossible = 33.07
        pct_longer = (t_impossible - t_possible) / t_possible * 100.0
        assert abs(pct_longer - 31.7005) < 0.05

        els.append(card(rx + 14, ry + 176, rw - 28, 144, rx=8, fill=CARD_BG, stroke=BORDER))
        els.append(txt(rx + 26, ry + 197, "5 月龄婴儿平均注视时长（单位：秒）", size=11.4, color=INK, weight="700"))

        max_s = 40.0
        bx0, bmax_w = rx + 104, 150.0
        w_pos = (t_possible / max_s) * bmax_w
        w_imp = (t_impossible / max_s) * bmax_w

        # Bar 1: Possible
        els.append(txt(rx + 26, ry + 225, "可能事件", size=10.8, color=BODY, weight="600"))
        els.append(f'<rect x="{bx0}" y="{ry + 212}" width="{w_pos:.1f}" height="18" rx="4" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.2"/>')
        els.append(txt(bx0 + w_pos + 6, ry + 225, f"{t_possible:.2f} s", size=10.8, color=BLUE, weight="700", cls="mono"))

        # Bar 2: Impossible
        els.append(txt(rx + 26, ry + 255, "不可能事件", size=10.8, color=PURPLE, weight="700"))
        els.append(f'<rect x="{bx0}" y="{ry + 242}" width="{w_imp:.1f}" height="18" rx="4" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.5"/>')
        els.append(txt(bx0 + w_imp + 6, ry + 255, f"{t_impossible:.2f} s (+{pct_longer:.1f}%)", size=10.6, color=PURPLE, weight="700", cls="mono"))

        els.append(txt(rx + 26, ry + 283, "• 遇到“穿模 Bug”多盯约 8 秒：证明无需等会伸手掀布，", size=10.3, color=BODY))
        els.append(txt(rx + 26, ry + 300, "  5 月龄宝宝脑中已记住隐藏物体并具备固体物理预期！", size=10.3, color=GREEN, weight="700"))

        svg = figure(
            412,
            "婴儿灯笼意识与成人探照灯注意对比及Baillargeon直觉物理实验数据图",
            "左图对比成人前额叶抑制下的窄束探照灯注意与婴儿360度全景接收规律的灯笼意识；右图展示Baillargeon等1985年吊桥遮挡实验，5月龄婴儿对不可能穿模事件平均注视33.07秒，显著高于可能事件的25.11秒。",
            els,
        )
        write_svg(SUBDIR, "lantern-vs-spotlight-mind.svg", svg)

    def _build_sleep_amygdala_brake():
        """Post 3 SVG 1: Yoo et al. 2007 Current Biology (+60% amygdala, mPFC disconnect) + Co-regulation curves."""
        els = []
        els.extend(
            header(
                "缺觉不是脾气差：睡眠剥夺下的“杏仁核飙升 + 刹车断联”与共同调节",
                "左图据 Yoo, Walker 等（2007, Current Biology）fMRI 数据绘制；右图展示神经共同调节机制。",
            )
        )

        # Left panel: Yoo et al. 2007 fMRI quantitative breakdown
        lx, ly, lw, lh = 20, 64, 352, 332
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① 缺觉大脑发生了什么？（Yoo 等 2007）", size=PANEL_TITLE, color=INK, weight="700"))

        # Top two side-by-side circuit boxes
        # Box 1: Rested brain (n=12)
        els.append(card(lx + 14, ly + 38, 156, 118, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(lx + 92, ly + 56, "睡眠充足组（n=12）", size=10.8, color=GREEN, anchor="middle", weight="700"))
        els.append(card(lx + 28, ly + 66, 128, 28, rx=6, fill=CARD_BG, stroke=GREEN, sw=1.3))
        els.append(txt(lx + 92, ly + 84, "mPFC 内侧前额叶", size=10.2, color=INK, anchor="middle", weight="600"))
        els.append(_line(lx + 92, ly + 94, lx + 92, ly + 114, stroke=GREEN, sw=2.6, marker="arr-green"))
        els.append(txt(lx + 100, ly + 108, "强抑制连接", size=9.6, color=GREEN, weight="700"))
        els.append(card(lx + 34, ly + 118, 116, 28, rx=14, fill=CARD_BG, stroke=SLATE))
        els.append(txt(lx + 92, ly + 136, "杏仁核：受控 1.0×", size=10.0, color=BODY, anchor="middle", weight="600"))

        # Box 2: Sleep-deprived brain (n=14, ~35h awake)
        els.append(card(lx + 182, ly + 38, 156, 118, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(lx + 260, ly + 56, "睡眠剥夺组（n=14）", size=10.8, color=ORANGE, anchor="middle", weight="700"))
        els.append(card(lx + 196, ly + 66, 128, 28, rx=6, fill=CARD_BG, stroke=MUTED, dash="4 2"))
        els.append(txt(lx + 260, ly + 84, "mPFC 刹车断联", size=10.2, color=MUTED, anchor="middle", weight="600"))
        els.append(_line(lx + 260, ly + 94, lx + 260, ly + 114, stroke=ORANGE, sw=1.6, dash="3 3"))
        els.append(txt(lx + 260, ly + 109, "✕", size=12, color=ORANGE, anchor="middle", weight="700"))
        els.append(card(lx + 194, ly + 118, 132, 28, rx=14, fill="#fee2e2", stroke=ORANGE, sw=1.6))
        els.append(txt(lx + 260, ly + 136, "杏仁核飙升 +60%！", size=10.2, color=ORANGE, anchor="middle", weight="700"))

        # Quantitative bar comparison below
        els.append(card(lx + 14, ly + 168, lw - 28, 152, rx=8, fill=CARD_BG, stroke=BORDER))
        els.append(txt(lx + 26, ly + 188, "面对负性刺激时杏仁核 fMRI 反应对比：", size=11.0, color=INK, weight="700"))

        base_w = 105.0
        dep_w = base_w * 1.60  # Exact +60% intensity surge reported in Yoo et al. 2007
        assert abs(dep_w / base_w - 1.60) < 1e-9

        els.append(txt(lx + 26, ly + 214, "充足睡眠基准", size=10.4, color=SLATE, weight="600"))
        els.append(f'<rect x="{lx + 114}" y="{ly + 202}" width="{base_w:.1f}" height="16" rx="4" fill="{GREEN_SOFT}" stroke="{GREEN}"/>')
        els.append(txt(lx + 114 + base_w + 6, ly + 214, "100% (1.0×)", size=10.4, color=GREEN, weight="700", cls="mono"))

        els.append(txt(lx + 26, ly + 240, "缺觉过载状态", size=10.4, color=ORANGE, weight="700"))
        els.append(f'<rect x="{lx + 114}" y="{ly + 228}" width="{dep_w:.1f}" height="16" rx="4" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append(txt(lx + 114 + dep_w + 6, ly + 240, "+60%", size=10.8, color=ORANGE, weight="700", cls="mono"))

        els.append(txt(lx + 26, ly + 266, "• 激活体积同步扩大 +35%；叠加婴儿啼哭（300–3000 Hz", size=10.2, color=BODY))
        els.append(txt(lx + 26, ly + 283, "  粗糙声学调制，100–200 ms 唤醒脑岛与杏仁核），", size=10.2, color=BODY))
        els.append(txt(lx + 26, ly + 300, "  深夜“一秒冒火”是神经电路过载，不是你不爱孩子！", size=10.3, color=ORANGE, weight="700"))

        # Right panel: Co-regulation (Why adult must put on oxygen mask first)
        rx, ry, rw, rh = 388, 64, 352, 332
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 16, ry + 24, "② 共同调节：大人是宝宝的“外接前额叶”", size=PANEL_TITLE, color=INK, weight="700"))

        # Computed autonomic arousal wave plot
        gx0, gx1 = rx + 42, rx + rw - 20
        gy_top, gy_bot = ry + 48, ry + 188
        els.append(f'<rect x="{gx0}" y="{gy_top}" width="{gx1 - gx0}" height="{gy_bot - gy_top}" rx="6" fill="{SLATE_SOFT}" stroke="{HAIRLINE}"/>')
        els.append(txt(rx + 16, (gy_top + gy_bot) / 2 + 4, "唤醒", size=10.2, color=MUTED))
        els.append(_line(gx0, gy_bot - 26, gx1, gy_bot - 26, stroke=GREEN, sw=1.0, dash="3 3"))

        # Escalation curve (dashed orange) vs Co-regulation damped curve (solid blue & green)
        pts_esc = []
        pts_adult = []
        pts_baby = []
        for i in range(61):
            t = i / 60.0  # 0 .. 1
            xx = gx0 + t * (gx1 - gx0)
            # Escalating mutual distress if caregiver yells/panics
            esc_val = min(0.92, 0.50 + 0.42 * t + 0.04 * math.sin(16 * t))
            pts_esc.append((xx, gy_bot - esc_val * (gy_bot - gy_top)))

            # Adult pauses & labels emotion at t=0.18 -> smooth autonomic drop
            if t <= 0.18:
                ad_val = 0.56 + 0.50 * t
            else:
                ad_peak = 0.56 + 0.50 * 0.18
                ad_val = 0.18 + (ad_peak - 0.18) * math.exp(-5.0 * (t - 0.18))
            pts_adult.append((xx, gy_bot - ad_val * (gy_bot - gy_top)))

            # Baby's nervous system entrains smoothly to steady adult with slight lag
            if t <= 0.26:
                bb_val = 0.78 + 0.04 * math.sin(12 * t)
            else:
                bb_peak = 0.78 + 0.04 * math.sin(12 * 0.26)
                bb_val = 0.21 + (bb_peak - 0.21) * math.exp(-3.8 * (t - 0.26))
            pts_baby.append((xx, gy_bot - bb_val * (gy_bot - gy_top)))

        assert pts_adult[-1][1] > pts_adult[10][1]  # Lower arousal (larger y) at end
        assert pts_baby[-1][1] > pts_baby[10][1]

        els.append(_polyline(pts_esc, stroke=ORANGE, sw=1.8, dash="5 4", opacity=0.85))
        els.append(_polyline(pts_baby, stroke=BLUE, sw=2.3, trace=True))
        els.append(_polyline(pts_adult, stroke=GREEN, sw=2.5, trace=True))

        # Event marker at t=0.18 ("安全放床暂停 + 情绪命名")
        mx_pause = gx0 + 0.18 * (gx1 - gx0)
        els.append(_line(mx_pause, gy_top + 4, mx_pause, gy_bot - 4, stroke=INK, sw=1.1, dash="2 2"))
        els.append(txt(mx_pause + 5, gy_top + 15, "暂停+情绪命名", size=9.8, color=INK, weight="700", halo=True))

        els.append(txt(gx1 - 6, gy_top + 33, "失控互激（正反馈）", size=9.8, color=ORANGE, anchor="end", weight="600", halo=True))
        els.append(txt(gx0 + 156, gy_top + 74, "宝宝随大人平复", size=9.8, color=BLUE, weight="700", halo=True))
        els.append(txt(gx0 + 62, gy_bot - 36, "大人呼吸先稳", size=9.8, color=GREEN, weight="700", halo=True))
        els.append(txt(gx1 - 6, gy_bot - 8, "平稳安全基线", size=9.6, color=GREEN, anchor="end", halo=True))

        # 3-step explanation box below graph
        els.append(card(rx + 14, ry + 200, rw - 28, 120, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(rx + 26, ry + 220, "为什么不能指望婴儿“自己冷静反省”？", size=11.0, color=BLUE, weight="700"))
        els.append(txt(rx + 26, ry + 240, "1. 婴幼儿前额叶—边缘髓鞘化远未成熟，没有独立刹车片；", size=10.3, color=BODY))
        els.append(txt(rx + 26, ry + 258, "2. 必须借用照护者平稳的心跳、怀抱与慢语速完成“共同调节”；", size=10.3, color=BODY))
        els.append(txt(rx + 26, ry + 276, "3. 氧气面罩原则：快失控时先把宝宝放安全婴儿床，大人先降", size=10.3, color=BODY))
        els.append(txt(rx + 26, ry + 294, "   温（Lieberman 2007 情绪命名法），绝不带怒气摇晃婴儿！", size=10.3, color=GREEN, weight="700"))

        svg = figure(
            412,
            "睡眠剥夺导致杏仁核反应飙升60%及亲子神经共同调节机制图",
            "左图根据Yoo等2007年Current Biology研究展示睡眠剥夺使内侧前额叶刹车断联、杏仁核对负性刺激反应增强60%；右图通过唤醒曲线对比失控正反馈与大人先降温再带动宝宝平复的共同调节过程。",
            els,
            extra_css=TRACE_CSS,
        )
        write_svg(SUBDIR, "sleep-amygdala-brake.svg", svg)

    def _build_tronick_30_70_repair():
        """Post 3 SVG 2: Tronick & Gianino (1986) / Provenzi (2018) ~30% synchrony vs ~70% mismatch + repair."""
        els = []
        els.extend(
            header(
                "特罗尼克“30 / 70 定律”：健康亲子互动，70% 时间都在错拍与修复",
                "基于 Tronick & Gianino（1986）及 Provenzi 等（2018）健康母婴面对面微观编码统计。",
            )
        )

        # Top wide card: 60-second computed dyadic interaction state ribbon
        tx, ty, tw, th = 20, 64, 720, 152
        els.append(card(tx, ty, tw, th))
        els.append(txt(tx + 16, ty + 24, "① 典型健康亲子互动的 60 秒微观切片（同步总计 18s = 30%，错拍与修复 42s = 70%）", size=PANEL_TITLE, color=INK, weight="700"))

        # Exact segments (start_s, end_s, state, short_label)
        # Sync = 8 + 10 = 18s (30.0%)
        # Mismatch = 11 + 15 = 26s (43.3%)
        # Repair = 6 + 10 = 16s (26.7%) -> Mismatch + Repair = 42s (70.0%)
        segments = [
            (0, 8, "sync", "对视微笑 (8s)"),
            (8, 19, "mismatch", "宝宝扭头歇气·大人仍逗 (11s)"),
            (19, 25, "repair", "停手等待 (6s)"),
            (25, 35, "sync", "转回咯咯笑 (10s)"),
            (35, 50, "mismatch", "大人疲惫慢半拍·语气急 (15s)"),
            (50, 60, "repair", "温和抱起安抚重连 (10s)"),
        ]
        sync_s = sum(b - a for a, b, st, _ in segments if st == "sync")
        mis_s = sum(b - a for a, b, st, _ in segments if st in ("mismatch", "repair"))
        assert sync_s == 18 and mis_s == 42
        assert abs(sync_s / 60.0 - 0.30) < 1e-9
        assert abs(mis_s / 60.0 - 0.70) < 1e-9

        rx0, rw_bar = tx + 24, tw - 48  # 672px wide -> 11.2 px per second
        ry_bar, rh_bar = ty + 54, 42
        style_map = {
            "sync": (BLUE_SOFT, BLUE, "同频"),
            "mismatch": (ORANGE_SOFT, ORANGE, "错拍"),
            "repair": (GREEN_SOFT, GREEN, "修复"),
        }

        for idx_s, (s0, s1, st, slbl) in enumerate(segments):
            sx = rx0 + (s0 / 60.0) * rw_bar
            sw_seg = ((s1 - s0) / 60.0) * rw_bar
            bg_c, fg_c, tag = style_map[st]
            els.append(f'<rect x="{sx:.1f}" y="{ry_bar}" width="{sw_seg:.1f}" height="{rh_bar}" rx="5" fill="{bg_c}" stroke="{fg_c}" stroke-width="1.4"/>')
            els.append(txt(sx + sw_seg / 2, ry_bar + 17, tag, size=10.8, color=fg_c, anchor="middle", weight="700"))
            els.append(txt(sx + sw_seg / 2, ry_bar + 33, f"{s0}–{s1}s", size=9.8, color=SLATE, anchor="middle", cls="mono"))
            # Alternating caption above/below bar so labels never collide!
            cap_y = ry_bar - 8 if idx_s % 2 == 0 else ry_bar + rh_bar + 18
            els.append(txt(sx + sw_seg / 2, cap_y, slbl, size=10.0, color=BODY, anchor="middle"))

        # Time ticks at bottom of top card
        els.append(txt(tx + 24, ty + 138, "图例：蓝框 = 协调同频（30%） | 橙框 = 短暂错拍失调 + 绿框 = 主动修复（合计 70%，健康常态！）", size=10.5, color=MUTED))

        # Bottom-left card: Quantitative 30/70 proportion vs Still-Face un-repaired rupture
        blx, bly, blw, blh = 20, 228, 352, 162
        els.append(card(blx, bly, blw, blh))
        els.append(txt(blx + 16, bly + 24, "② 实验室量化真相：完美同频只是幻觉", size=PANEL_TITLE, color=INK, weight="700"))

        # Stacked 100% bar (30% vs 70%)
        sb_x, sb_y, sb_w, sb_h = blx + 16, bly + 40, blw - 32, 28
        w30 = sb_w * 0.30
        w70 = sb_w * 0.70
        els.append(f'<rect x="{sb_x}" y="{sb_y}" width="{w30:.1f}" height="{sb_h}" rx="5" fill="{BLUE}" />')
        els.append(f'<rect x="{sb_x + w30 + 3:.1f}" y="{sb_y}" width="{w70 - 3:.1f}" height="{sb_h}" rx="5" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.4"/>')
        els.append(txt(sb_x + w30 / 2, sb_y + 18, "同频 ~30%", size=11.0, color="#ffffff", anchor="middle", weight="700"))
        els.append(txt(sb_x + w30 + w70 / 2, sb_y + 18, "短暂失调 + 及时修复 ~70%", size=11.0, color=GREEN, anchor="middle", weight="700"))

        els.append(txt(blx + 16, bly + 90, "• 哪怕最温柔敏感的妈妈，也有约 70% 时间没对上节拍", size=10.5, color=BODY))
        els.append(txt(blx + 16, bly + 109, "• 真正伤人的不是“偶尔急躁/没听懂”，而是像“静止脸实验”", size=10.5, color=BODY))
        els.append(txt(blx + 16, bly + 127, "  那样长期冷漠、持续无回应且从不修复（慢性毒性压力）", size=10.5, color=ORANGE, weight="600"))
        els.append(txt(blx + 16, bly + 146, "• “60分够好父母 + 可靠修复”远胜紧绷的“100分表演”", size=10.5, color=BLUE, weight="700"))

        # Bottom-right card: What babies learn from thousands of micro-repairs
        brx, bry, brw, brh = 388, 228, 352, 162
        els.append(card(brx, bry, brw, brh))
        els.append(txt(brx + 16, bry + 24, "③ 上千次“小修复”教给宝宝哪三样底层能力？", size=PANEL_TITLE, color=INK, weight="700"))

        lessons = [
            ("1", BLUE, BLUE_SOFT, "习得掌控感：我的哭声和眼神有用，能把爸妈唤回来"),
            ("2", GREEN, GREEN_SOFT, "情绪复原力：短暂的不舒服不会天塌，难过可以熬过去"),
            ("3", PURPLE, PURPLE_SOFT, "安全依恋底色：关系不怕小磕碰，我们总能重新连接"),
        ]
        for idx_l, (num_s, fg_l, bg_l, text_l) in enumerate(lessons):
            yy = bry + 50 + idx_l * 38
            els.append(step_badge(brx + 28, yy - 4, num_s, fg=fg_l, bg=bg_l, r=10))
            els.append(txt(brx + 46, yy, text_l, size=10.7, color=BODY, weight="600" if idx_l == 2 else None))

        svg = figure(
            406,
            "Tronick母婴互动30%同频与70%失调修复比例时间序列及依恋意义图",
            "上图用60秒时间轴展示健康亲子互动中18秒同频（30%）与42秒错拍及修复（70%）的交替过程；左下图对比30/70比例与慢性未修复失调；右下图总结微修复带来的掌控感、情绪复原力与安全依恋。",
            els,
        )
        write_svg(SUBDIR, "tronick-30-70-repair.svg", svg)

    @register("baby-science", "孕期宫内感官、婴儿视角认知实验与照护者睡眠情绪脑科学图解", "science_tech")
    def build_baby_science():
        _build_womb_sound_flavor()
        _build_parental_brain_transition()
        _build_infant_vision_stages()
        _build_lantern_vs_spotlight()
        _build_sleep_amygdala_brake()
        _build_tronick_30_70_repair()


_register_baby_science()


def _register_earth_and_photo():
    import math

    from html import escape

    from .core import (
        BG,
        BLUE,
        BLUE_LINE,
        BLUE_SOFT,
        BODY,
        BORDER,
        CARD_BG,
        GREEN,
        GREEN_SOFT,
        HAIRLINE,
        INK,
        LABEL_SIZE,
        MUTED,
        NOTE_SIZE,
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

    EARTH_DIR = "earth-life"

    PHOTO_DIR = "photo-science"

    SIGMA = 5.670374419e-8  # Stefan-Boltzmann constant W/(m^2 K^4)

    def _line(x1, y1, x2, y2, stroke=BORDER, sw=1.2, dash=None, marker=None, opacity=None):
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
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        return f'<line {" ".join(attrs)}/>'

    def _polyline(pts, stroke=BLUE, sw=2.4, fill="none", dash=None, opacity=None, trace=False):
        d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' opacity="{opacity}"' if opacity is not None else ""
        tr = ' pathLength="1" class="trace-line"' if (trace and not dash) else ""
        return (
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}{op}{tr}/>'
        )

    def _area_under(pts, y_base, fill, opacity=0.14):
        d = (
            f"M {pts[0][0]:.2f},{y_base:.2f} L "
            + " L ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
            + f" L {pts[-1][0]:.2f},{y_base:.2f} Z"
        )
        return f'<path d="{d}" fill="{fill}" opacity="{opacity}"/>'

    TRACE_CSS = """
      .trace-line {
        stroke-dasharray: 1;
        stroke-dashoffset: 0;
        animation: drawLine 1.3s ease-out 1 both;
      }
      @keyframes drawLine {
        from { stroke-dashoffset: 1; }
        to { stroke-dashoffset: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .trace-line { animation: none; }
      }"""

    def _eq_temp_c(solar_flux_w_m2, bond_albedo):
        t_k = ((1.0 - bond_albedo) * solar_flux_w_m2 / (4.0 * SIGMA)) ** 0.25
        return t_k - 273.15

    def _build_venus_earth_mars_energy():
        """Earth SVG 1: Quantitative radiative equilibrium T_eq vs actual T_surf across Venus, Earth, Mars."""
        # Verify Stefan-Boltzmann radiative equilibrium temperatures:
        # Venus: S=2601.3 W/m^2, classical Bond albedo A=0.747 (~0.75) -> -41.0°C (NASA A=0.77 -> -46.6°C)
        # Earth: S=1361.0 W/m^2, Bond albedo A=0.30 -> -18.6°C (rounded -18°C; 254.6 K ~ 255 K)
        # Mars:  S=586.2 W/m^2,  Bond albedo A=0.25 -> -63.4°C (rounded -63°C; 209.8 K)
        t_eq_venus = _eq_temp_c(2601.3, 0.747)
        t_eq_earth = _eq_temp_c(1361.0, 0.300)
        t_eq_mars = _eq_temp_c(586.2, 0.250)
        assert -42.0 <= t_eq_venus <= -40.5
        assert -19.2 <= t_eq_earth <= -18.0
        assert -64.0 <= t_eq_mars <= -62.8

        els = []
        els.extend(
            header(
                "三颗岩石邻居的温度账本：无温室辐射平衡温度 T_eq 对比真实地表均温",
                "按 σT_eq⁴ = (1−A)S/4 计算等效黑体辐射温度，对比 NASA 行星档案实测全球平均表面温度。",
            )
        )

        # Top main card
        cx, cy, cw, ch = 20, 64, 720, 260
        els.append(card(cx, cy, cw, ch))
        els.append(
            txt(
                cx + 16,
                cy + 24,
                "① 辐射平衡起点（蓝圆点）→ 温室效应加成 → 真实地表均温（实心终点）",
                size=PANEL_TITLE,
                color=INK,
                weight="700",
            )
        )

        x0, x1 = 176.0, 712.0  # -100°C to +500°C -> 536px for 600°C
        t_min, t_max = -100.0, 500.0

        def tx(tc):
            return x0 + (tc - t_min) / (t_max - t_min) * (x1 - x0)

        y_top, y_bot = cy + 52, cy + 226

        # 1 bar liquid water zone (0°C to 100°C)
        wx0, wx1 = tx(0.0), tx(100.0)
        els.append(
            f'<rect x="{wx0:.1f}" y="{y_top:.1f}" width="{wx1 - wx0:.1f}" height="{y_bot - y_top:.1f}" '
            f'fill="{BLUE_SOFT}" stroke="{BLUE_LINE}" stroke-width="1" stroke-dasharray="3 3" opacity="0.85"/>'
        )
        els.append(
            txt(
                (wx0 + wx1) / 2,
                y_top - 6,
                "1 bar 液态水窗口 (0~100°C)",
                size=10.5,
                color=BLUE,
                anchor="middle",
                weight="700",
            )
        )

        # Grid lines & axis ticks
        for tick in (-100, 0, 100, 200, 300, 400, 500):
            xx = tx(tick)
            els.append(_line(xx, y_top, xx, y_bot, stroke=HAIRLINE if tick != 0 else BLUE, sw=1.0, dash="3 3"))
            lbl = f"+{tick}°C" if tick > 0 else f"{tick}°C"
            els.append(txt(xx, y_bot + 18, lbl, size=10.5, color=MUTED, anchor="middle", cls="mono"))

        els.append(_line(x0, y_bot, x1, y_bot, stroke=SLATE, sw=1.2))

        planets = [
            {
                "name": "金星 Venus",
                "meta": "0.72 AU｜92 bar",
                "teq": -41.0,
                "tsurf": 464.0,
                "y": cy + 88,
                "color": ORANGE,
                "soft": ORANGE_SOFT,
                "delta_lbl": "ΔT ≈ +505°C 失控温室效应（浓云反射 ~75% 阳光，厚重 CO₂ 锁死红外热）",
            },
            {
                "name": "地球 Earth",
                "meta": "1.00 AU｜1.01 bar",
                "teq": -18.0,
                "tsurf": 15.0,
                "y": cy + 148,
                "color": GREEN,
                "soft": GREEN_SOFT,
                "delta_lbl": "ΔT ≈ +33°C 天然温室暖被（把冰封地球托进液态水带！）",
            },
            {
                "name": "火星 Mars",
                "meta": "1.52 AU｜0.006 bar",
                "teq": -63.0,
                "tsurf": -60.0,
                "y": cy + 204,
                "color": PURPLE,
                "soft": PURPLE_SOFT,
                "delta_lbl": "ΔT ≈ +3°C 大气太薄（气压 ~610 Pa 卡在水的三相点）",
            },
        ]

        for p in planets:
            yy = p["y"]
            xe = tx(p["teq"])
            xs = tx(p["tsurf"])
            assert xe < xs
            # Row guide line
            els.append(_line(x0, yy, x1, yy, stroke=BORDER, sw=0.8))
            # Left planet label
            els.append(txt(cx + 16, yy - 3, p["name"], size=12.5, color=INK, weight="700"))
            els.append(txt(cx + 16, yy + 14, p["meta"], size=10.3, color=MUTED, cls="mono"))

            # Warming span bar + arrow
            bar_h = 12
            els.append(
                f'<rect x="{xe:.1f}" y="{yy - bar_h / 2:.1f}" width="{max(4.0, xs - xe):.1f}" height="{bar_h}" '
                f'rx="6" fill="{p["color"]}" opacity="0.24"/>'
            )
            if xs - xe > 16:
                marker_id = "arr-orange" if p["color"] == ORANGE else "arr-green"
                els.append(_line(xe + 6, yy, xs - 8, yy, stroke=p["color"], sw=2.2, marker=marker_id))

            # T_eq open circle & T_surf filled circle
            els.append(f'<circle cx="{xe:.1f}" cy="{yy:.1f}" r="5.5" fill="#ffffff" stroke="{BLUE}" stroke-width="2.2"/>')
            els.append(f'<circle cx="{xs:.1f}" cy="{yy:.1f}" r="6.0" fill="{p["color"]}" stroke="#ffffff" stroke-width="1.4"/>')

            # Labels carefully placed without any collision
            if p["name"].startswith("金星"):
                els.append(txt(xe - 8, yy + 4, "-41°C", size=10.8, color=BLUE, anchor="end", weight="700", cls="mono", halo=True))
                els.append(txt(xs, yy - 11, "+464°C", size=11.0, color=ORANGE, anchor="middle", weight="700", cls="mono", halo=True))
                els.append(txt((xe + xs) / 2 + 12, yy - 12, p["delta_lbl"], size=10.5, color=ORANGE, anchor="middle", weight="600", halo=True))
            elif p["name"].startswith("地球"):
                els.append(txt(xe - 8, yy + 4, "-18°C", size=10.8, color=BLUE, anchor="end", weight="700", cls="mono", halo=True))
                els.append(txt(xs + 9, yy - 8, "+15°C", size=11.0, color=GREEN, anchor="start", weight="700", cls="mono", halo=True))
                els.append(txt(xs + 56, yy - 8, p["delta_lbl"], size=10.8, color=GREEN, anchor="start", weight="600", halo=True))
            else:
                els.append(txt(xe - 8, yy + 4, "-63°C", size=10.8, color=BLUE, anchor="end", weight="700", cls="mono", halo=True))
                els.append(txt(xs + 9, yy + 4, "-60°C", size=11.0, color=PURPLE, anchor="start", weight="700", cls="mono", halo=True))
                els.append(txt(xs + 56, yy + 4, p["delta_lbl"], size=10.6, color=BODY, anchor="start", halo=True))

        # Bottom two insight cards
        by, bh = 336, 92
        els.append(card(20, by, 352, bh))
        els.append(txt(36, by + 22, "② 反直觉真相：金星的辐射起点比地球还冷！", size=12.5, color=INK, weight="700"))
        els.append(txt(36, by + 43, "• 金星太阳辐射虽是地球 1.91 倍，但浓云反照率高达 0.75~0.77", size=10.6, color=BODY))
        els.append(txt(36, by + 61, "  （NASA 新表取 0.77 时 T_eq 约 -46°C），绝大部分阳光被直接弹回；", size=10.6, color=BODY))
        els.append(txt(36, by + 79, "• 真正把它烤到 464°C（比水星均温 167°C 更烫）的是 92 bar CO₂！", size=10.6, color=ORANGE, weight="700"))

        els.append(card(388, by, 352, bh))
        els.append(txt(404, by + 22, "③ 科学边界：这笔账究竟隔离了什么变量？", size=12.5, color=INK, weight="700"))
        els.append(txt(404, by + 43, "• 公式沿用各行星当前邦德反照率 A（已包含现有云层与冰盖贡献）；", size=10.6, color=BODY))
        els.append(txt(404, by + 61, "• 若真抽干地球空气，云和冰也会改变反照率；但对比 T_eq 与 T_surf", size=10.6, color=BODY))
        els.append(txt(404, by + 79, "  恰好定量拎出大气红外“保温被”的净贡献：地球约 +33°C。", size=10.6, color=BLUE, weight="700"))

        svg = figure(
            442,
            "金星、地球与火星的辐射平衡温度与真实地表平均温度定量对比图",
            "在同一摄氏温标（-100°C至+500°C）上对比三颗岩石行星的无温室等效辐射平衡温度与实测地表均温：金星从约-41°C飙升至+464°C，地球从-18°C升至+15°C落入液态水窗口，火星从-63°C仅升至约-60°C。",
            els,
        )
        write_svg(EARTH_DIR, "venus-earth-mars-energy.svg", svg)

    def _build_silicate_weathering_thermostat():
        """Earth SVG 2: Faint Young Sun solar luminosity curve + carbonate-silicate weathering thermostat + Snowball escape."""
        els = []
        els.extend(
            header(
                "暗淡年轻太阳悖论：40 亿年前阳光弱近三成，地球靠什么没冻成死冰球？",
                "左图据恒星演化公式绘制太阳光度增长与古海洋证据；右图拆解硅酸盐风化负反馈及“雪球地球”火山逃逸。",
            )
        )

        # Left panel: Faint Young Sun curve
        lx, ly, lw, lh = 20, 64, 344, 368
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① 太阳变亮曲线 vs 早期液态水铁证", size=PANEL_TITLE, color=INK, weight="700"))

        px0, px1 = lx + 48, lx + lw - 20  # 68 .. 344 (276px), time from 4.5 Ga ago -> 0 Ga (today)
        py0, py1 = ly + 52, ly + 226      # L/L0 from 1.05 (top) down to 0.65 (bottom)

        def gx(t_ga_ago):
            return px0 + (4.5 - t_ga_ago) / 4.5 * (px1 - px0)

        def gy(lum_ratio):
            return py1 - (lum_ratio - 0.65) / (1.05 - 0.65) * (py1 - py0)

        # Gough (1981) solar luminosity formula: L(t)/L0 = 1 / (1 + 0.4 * (t_ago / 4.57))
        def solar_lum(t_ga_ago):
            return 1.0 / (1.0 + 0.4 * (t_ga_ago / 4.57))

        assert 0.71 <= solar_lum(4.5) <= 0.73
        assert 0.735 <= solar_lum(4.0) <= 0.75
        assert abs(solar_lum(0.0) - 1.0) < 1e-9

        # Shaded "Faint Sun freeze zone if modern CO2" (4.5 to ~2.0 Ga ago, L < ~0.85 L0)
        x_freeze_end = gx(1.9)
        els.append(
            f'<rect x="{px0:.1f}" y="{py0:.1f}" width="{x_freeze_end - px0:.1f}" height="{py1 - py0:.1f}" '
            f'fill="{BLUE_SOFT}" opacity="0.72"/>'
        )
        els.append(txt((px0 + x_freeze_end) / 2, py0 + 15, "若仅靠现代温室气体", size=10.2, color=BLUE, anchor="middle", weight="600"))
        els.append(txt((px0 + x_freeze_end) / 2, py0 + 29, "全球均温将跌破 0°C 冰点", size=10.2, color=BLUE, anchor="middle"))

        # Grid lines
        for lr, lbl in [(0.70, "70%"), (0.80, "80%"), (0.90, "90%"), (1.00, "100%")]:
            yy = gy(lr)
            els.append(_line(px0, yy, px1, yy, stroke=HAIRLINE, sw=0.9, dash="3 3"))
            els.append(txt(px0 - 6, yy + 4, lbl, size=10.3, color=MUTED, anchor="end", cls="mono"))

        for ga, glbl in [(4.5, "45亿年前"), (3.0, "30亿"), (1.5, "15亿"), (0.0, "今天")]:
            xx = gx(ga)
            els.append(_line(xx, py0, xx, py1, stroke=HAIRLINE, sw=0.9, dash="2 3"))
            els.append(txt(xx, py1 + 16, glbl, size=10.2, color=MUTED, anchor="middle"))

        els.append(_line(px0, py0, px0, py1, stroke=SLATE, sw=1.2))
        els.append(_line(px0, py1, px1, py1, stroke=SLATE, sw=1.2))

        pts_lum = [(gx(4.5 - 4.5 * i / 60.0), gy(solar_lum(4.5 - 4.5 * i / 60.0))) for i in range(61)]
        els.append(_polyline(pts_lum, stroke=ORANGE, sw=2.8, trace=True))
        els.append(txt(gx(1.05), gy(solar_lum(1.05)) - 10, "太阳光度 L/L₀", size=10.8, color=ORANGE, anchor="middle", weight="700", halo=True))

        # Geological liquid-water markers at 4.4 Ga (Jack Hills zircon) and 3.7 Ga (pillow lavas / Isua)
        x44, y44 = gx(4.4), gy(solar_lum(4.4))
        x37, y37 = gx(3.7), gy(solar_lum(3.7))
        els.append(f'<circle cx="{x44:.1f}" cy="{y44:.1f}" r="5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(f'<circle cx="{x37:.1f}" cy="{y37:.1f}" r="5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.4"/>')
        els.append(_line(x44, y44 - 6, x44 + 8, y44 - 36, stroke=GREEN, sw=1.2))
        els.append(txt(x44 + 4, y44 - 40, "4.4 Ga 杰克山锆石", size=10.2, color=GREEN, weight="700", halo=True))
        els.append(_line(x37, y37 + 6, x37 + 16, y37 + 22, stroke=GREEN, sw=1.2))
        els.append(txt(x37 + 6, y37 + 34, "3.8~3.5 Ga 枕状熔岩/古海洋", size=10.2, color=GREEN, weight="700", halo=True))

        # Bottom explanation inside Left Card
        els.append(card(lx + 14, ly + 252, lw - 28, 102, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(lx + 24, ly + 272, "萨根与马伦（1972）揭开的矛盾与解答：", size=11.2, color=GREEN, weight="700"))
        els.append(txt(lx + 24, ly + 291, "• 恒星核聚变使太阳核心平均分子量增大，每十亿年变亮约 7%–9%；", size=10.3, color=BODY))
        els.append(txt(lx + 24, ly + 309, "• 40 亿年前光度仅 ~74%，却有液态海！靠的是早期更高浓度的", size=10.3, color=BODY))
        els.append(txt(lx + 24, ly + 327, "  CO₂、CH₄ 等温室气体，以及深色海洋较低的反照率。", size=10.3, color=INK, weight="600"))

        # Right panel: Carbonate-silicate thermostat + Snowball Earth escape
        rx, ry, rw, rh = 380, 64, 360, 368
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 16, ry + 24, "② 碳酸盐—硅酸盐风化反馈（百万年尺度）", size=PANEL_TITLE, color=INK, weight="700"))

        # 2x2 feedback loop boxes inside top portion of right card
        bw, bh_n = 150, 56
        bx_l, bx_r = rx + 16, rx + 194
        by_t, by_b = ry + 42, ry + 132

        # Node 1 (Top-Left): Volcano CO2 input
        els.append(card(bx_l, by_t, bw, bh_n, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.3))
        els.append(txt(bx_l + bw / 2, by_t + 23, "火山与变质脱气", size=11.2, color=ORANGE, anchor="middle", weight="700"))
        els.append(txt(bx_l + bw / 2, by_t + 42, "持续向大气补充 CO₂", size=10.2, color=BODY, anchor="middle"))

        # Node 2 (Top-Right): Warm & wet -> fast silicate weathering
        els.append(card(bx_r, by_t, bw, bh_n, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.3))
        els.append(txt(bx_r + bw / 2, by_t + 23, "偏暖多雨：风化加速", size=11.2, color=GREEN, anchor="middle", weight="700"))
        els.append(txt(bx_r + bw / 2, by_t + 42, "雨水+CO₂ 蚀解硅酸盐岩", size=10.2, color=BODY, anchor="middle"))

        # Node 3 (Bottom-Right): Carbonate burial
        els.append(card(bx_r, by_b, bw, bh_n, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.3))
        els.append(txt(bx_r + bw / 2, by_b + 23, "入海沉积锁碳降温", size=11.2, color=BLUE, anchor="middle", weight="700"))
        els.append(txt(bx_r + bw / 2, by_b + 42, "Ca²⁺+HCO₃⁻ → CaCO₃ 埋藏", size=10.0, color=BODY, anchor="middle", cls="mono"))

        # Node 4 (Bottom-Left): Cold & dry -> weathering slows -> CO2 builds up
        els.append(card(bx_l, by_b, bw, bh_n, rx=8, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.3))
        els.append(txt(bx_l + bw / 2, by_b + 23, "偏冷少雨：风化刹车", size=11.2, color=PURPLE, anchor="middle", weight="700"))
        els.append(txt(bx_l + bw / 2, by_b + 42, "消耗减慢 → CO₂ 重新攒高", size=10.2, color=BODY, anchor="middle"))

        # Connecting arrows clockwise: TL -> TR -> BR -> BL -> TL
        els.append(_line(bx_l + bw + 3, by_t + 28, bx_r - 5, by_t + 28, stroke=ORANGE, sw=1.8, marker="arr-orange"))
        els.append(_line(bx_r + bw / 2, by_t + bh_n + 3, bx_r + bw / 2, by_b - 5, stroke=GREEN, sw=1.8, marker="arr-green"))
        els.append(_line(bx_r - 3, by_b + 28, bx_l + bw + 5, by_b + 28, stroke=BLUE, sw=1.8, marker="arr-blue"))
        els.append(_line(bx_l + bw / 2, by_b - 3, bx_l + bw / 2, by_t + bh_n + 5, stroke=SLATE, sw=1.8, marker="arr-muted"))
        els.append(txt(rx + rw / 2, by_t + bh_n + 21, "负反馈稳定器", size=10.2, color=SLATE, anchor="middle", weight="700", halo=True))

        # Net geochemical equation strip
        els.append(
            txt(
                rx + rw / 2,
                ry + 210,
                "净反应简式：CaSiO₃（硅酸盐岩）+ CO₂ ⇌ CaCO₃（石灰岩）+ SiO₂",
                size=10.5,
                color=INK,
                anchor="middle",
                weight="600",
            )
        )

        # Snowball Earth box + modern warning
        els.append(card(rx + 14, ry + 224, rw - 28, 130, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(rx + 24, ry + 244, "③ 当恒温器暂时失控：“雪球地球”怎样脱困？", size=11.2, color=ORANGE, weight="700"))
        els.append(txt(rx + 24, ry + 264, "• 约 7.2–6.35 亿年前冰雪反照率正反馈使冰盖推进至低纬；", size=10.0, color=BODY))
        els.append(txt(rx + 24, ry + 282, "• 冰层隔绝雨水与岩石，风化近停，但火山仍持续喷出 CO₂；", size=10.0, color=BODY))
        els.append(txt(rx + 24, ry + 300, "• 数百万年攒出超强温室融穿冰壳，留下厚层“盖帽碳酸盐岩”！", size=10.0, color=BODY))
        els.append(txt(rx + 24, ry + 320, "• 警示：该调节耗时百万年，绝来不及抵消现代百年快速排碳！", size=10.0, color=INK, weight="700"))

        svg = figure(
            446,
            "暗淡年轻太阳悖论、碳酸盐—硅酸盐风化地质恒温器与雪球地球逃逸机制图",
            "左图按恒星演化模型绘制45亿年来太阳光度从约72%升至100%的曲线，并标注44亿年杰克山锆石与38-35亿年枕状熔岩液态水证据；右图展示火山脱气、硅酸盐风化、碳酸盐沉积构成的负反馈闭环，以及雪球地球火山CO2累积逃逸与百万年时间尺度边界。",
            els,
            extra_css=TRACE_CSS,
        )
        write_svg(EARTH_DIR, "silicate-weathering-thermostat.svg", svg)

    def _kell_water_density(temp_c):
        """Kell (1975) / NIST equation for density of air-free liquid water at 1 atm (g/cm^3), valid 0-40°C."""
        t = float(temp_c)
        num = (
            999.83952
            + 16.945176 * t
            - 7.9870401e-3 * (t ** 2)
            - 46.170461e-6 * (t ** 3)
            + 105.56302e-9 * (t ** 4)
            - 280.54253e-12 * (t ** 5)
        )
        den = 1.0 + 16.879850e-3 * t
        return (num / den) / 1000.0

    def _build_water_ice_carbon_silicon():
        """Earth SVG 3: Water 4°C density anomaly & floating ice + Carbon CO2 gas vs Silicon SiO2 solid quartz."""
        rho_0 = _kell_water_density(0.0)
        rho_4 = _kell_water_density(3.984)
        rho_20 = _kell_water_density(20.0)
        rho_ice = 0.9168
        assert abs(rho_0 - 0.99984) < 1e-4
        assert abs(rho_4 - 0.99997) < 1e-4
        assert abs(rho_20 - 0.99821) < 1e-4
        assert rho_4 > rho_0 > rho_20 > rho_ice

        els = []
        els.extend(
            header(
                "水与碳的分子偏爱：为什么冰浮在水面护住生命，而硅很难顶替碳？",
                "左图据 Kell (1975) 与 NIST 物性表绘制液态水 4°C 密度峰值与浮冰效应；右图对比碳与硅的化学键和氧化物。",
            )
        )

        # Left panel: Water density anomaly + winter lake cross-section
        lx, ly, lw, lh = 20, 64, 352, 356
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① 水的反常膨胀：4°C 最重，结冰反轻 8.3%", size=PANEL_TITLE, color=INK, weight="700"))

        # Top plot: zoomed liquid water curve 0..24°C (0.9970 to 1.0002 g/cm^3)
        px0, px1 = lx + 62, lx + lw - 20  # 82 .. 352 (270px)
        py0, py1 = ly + 48, ly + 172      # 112 .. 236 (124px)
        r_min, r_max = 0.9970, 1.0003

        def wx(tc):
            return px0 + (tc / 24.0) * (px1 - px0)

        def wy(rho):
            return py1 - (rho - r_min) / (r_max - r_min) * (py1 - py0)

        for rv, rlbl in [(0.9975, "0.9975"), (0.9985, "0.9985"), (0.9995, "0.9995"), (1.0000, "1.0000")]:
            yy = wy(rv)
            els.append(_line(px0, yy, px1, yy, stroke=HAIRLINE, sw=0.9, dash="3 3"))
            els.append(txt(px0 - 6, yy + 4, rlbl, size=9.8, color=MUTED, anchor="end", cls="mono"))

        for tv in (0, 4, 10, 16, 24):
            xx = wx(tv)
            els.append(_line(xx, py0, xx, py1, stroke=HAIRLINE if tv != 4 else BLUE_LINE, sw=0.9, dash="2 3"))
            els.append(txt(xx, py1 + 15, f"{tv}°C", size=10.0, color=BLUE if tv == 4 else MUTED, anchor="middle", weight="700" if tv == 4 else None, cls="mono"))

        els.append(_line(px0, py0, px0, py1, stroke=SLATE, sw=1.2))
        els.append(_line(px0, py1, px1, py1, stroke=SLATE, sw=1.2))

        pts_w = [(wx(24.0 * i / 80.0), wy(_kell_water_density(24.0 * i / 80.0))) for i in range(81)]
        els.append(_area_under(pts_w, py1, BLUE, opacity=0.12))
        els.append(_polyline(pts_w, stroke=BLUE, sw=2.6, trace=True))

        x_peak, y_peak = wx(3.984), wy(rho_4)
        els.append(f'<circle cx="{x_peak:.1f}" cy="{y_peak:.1f}" r="4.8" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.3"/>')
        els.append(txt(x_peak + 10, y_peak + 3, "峰值 4°C: 1.0000 g/cm³", size=10.3, color=ORANGE, weight="700", halo=True))
        els.append(txt(wx(18.0), wy(_kell_water_density(18.0)) - 9, "液态水密度曲线(放大纵轴)", size=9.8, color=BLUE, anchor="middle", halo=True))

        # Bottom half of left panel: Winter lake cross-section + Ice Ih 0.917 g/cm^3
        lk_x, lk_y, lk_w, lk_h = lx + 16, ly + 200, lw - 32, 140
        els.append(card(lk_x, lk_y, lk_w, lk_h, rx=8, fill="#f8fbff", stroke=BLUE_LINE))
        # Top floating ice layer
        els.append(
            f'<rect x="{lk_x + 10}" y="{lk_y + 12}" width="{lk_w - 20}" height="34" rx="5" '
            f'fill="#e0f2fe" stroke="{BLUE}" stroke-width="1.4"/>'
        )
        els.append(
            txt(
                lk_x + lk_w / 2,
                lk_y + 33,
                "0°C 六方冰层：0.917 g/cm³（氢键撑开空笼，浮于水面隔寒）",
                size=10.2,
                color=INK,
                anchor="middle",
                weight="700",
            )
        )
        # Deeper 4°C liquid water refuge
        els.append(
            f'<rect x="{lk_x + 10}" y="{lk_y + 52}" width="{lk_w - 20}" height="76" rx="5" '
            f'fill="{BLUE_SOFT}" stroke="none"/>'
        )
        els.append(txt(lk_x + 20, lk_y + 74, "• 0~4°C 水体：越接近 4°C 越重，自动下沉到湖底与深海", size=10.2, color=BODY))
        els.append(txt(lk_x + 20, lk_y + 94, "• 若冰和多数固体一样比液态重：冰会沉底、水体自下而上冻实！", size=10.2, color=ORANGE, weight="600"))
        els.append(txt(lk_x + 20, lk_y + 114, "• 4°C 液态深水层（1.000 g/cm³）：严冬与冰期水生生命的避难所", size=10.2, color=GREEN, weight="700"))

        # Right panel: Carbon vs Silicon
        rx, ry, rw, rh = 388, 64, 352, 356
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 16, ry + 24, "② 周期表同族对决：为什么是碳（₆C）不是硅（₁₄Si）？", size=PANEL_TITLE, color=INK, weight="700"))

        # Carbon card
        els.append(card(rx + 16, ry + 42, rw - 32, 134, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.3))
        els.append(pill(rx + 28, ry + 52, "₆C 碳｜第2周期·4个共价键", fg=GREEN, bg="#ffffff", w=182, h=22, size=11.0))
        els.append(txt(rx + 28, ry + 92, "• C–C 键能 ≈ 346 kJ/mol（与 C–O、C–H 相近）：", size=10.3, color=INK, weight="600"))
        els.append(txt(rx + 28, ry + 110, "  既牢靠搭出长链、环与双键，又可在酶促下温和拆装。", size=10.0, color=BODY))
        els.append(txt(rx + 28, ry + 131, "• 氧化产物 CO₂（独立小分子）：常温是可溶气体！", size=10.3, color=GREEN, weight="700"))
        els.append(txt(rx + 28, ry + 149, "  碳能在大气、海洋、叶片与细胞间全行星自由流转。", size=10.0, color=BODY))

        # Silicon card
        els.append(card(rx + 16, ry + 188, rw - 32, 134, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.3))
        els.append(pill(rx + 28, ry + 198, "₁₄Si 硅｜地壳质量远多于碳", fg=ORANGE, bg="#ffffff", w=182, h=22, size=11.0))
        els.append(txt(rx + 28, ry + 238, "• Si–Si 键仅 ≈ 222 kJ/mol，Si–O 高达 ≈ 452：", size=10.3, color=INK, weight="600"))
        els.append(txt(rx + 28, ry + 256, "  难成稳定双键；硅氢链遇水和氧易断裂并锁死成硅氧键。", size=10.0, color=BODY))
        els.append(txt(rx + 28, ry + 277, "• 氧化产物 SiO₂（三维网状晶体）：是石英砂岩石！", size=10.3, color=ORANGE, weight="700"))
        els.append(txt(rx + 28, ry + 295, "  不溶于水也没法随呼吸排出——总不能呼气吐一把沙子。", size=10.0, color=BODY))

        # Caveat note at bottom of right panel
        els.append(txt(rx + 16, ry + 341, "注：解释有水有氧环境碳的优势，不排除极端环境异质化学。", size=9.9, color=MUTED))

        svg = figure(
            434,
            "液态水4摄氏度最大密度反常膨胀曲线与碳硅元素成键及氧化物对比图",
            "左图按Kell(1975)公式精确绘制0至24°C液态水密度曲线（在约4°C达1.0000 g/cm³峰值），对比0°C六方冰0.917 g/cm³浮于水面的护生机制；右图对比第14族碳（C-C键稳定、CO2为可溶气体）与硅（Si-O锁死、SiO2为石英固体）的分子差异。",
            els,
            extra_css=TRACE_CSS,
        )
        write_svg(EARTH_DIR, "water-ice-carbon-silicon.svg", svg)

    def _build_endosymbiosis_leap():
        """Earth SVG 4: Margulis Serial Endosymbiotic Theory — archaeal host + mitochondria + chloroplast."""
        els = []
        els.extend(
            header(
                "内共生大跃迁：生命为何当了十多亿年微生物，才跨向复杂动植物？",
                "琳·马古利斯（1967）内共生学说与现代基因组学证据：两次改变地球生命能量预算的“细胞合体”。",
            )
        )

        # Top 3-stage evolutionary flow card
        tx, ty, tw, th = 20, 64, 720, 224
        els.append(card(tx, ty, tw, th))
        els.append(txt(tx + 16, ty + 24, "① 从原核独霸到复杂真核生物的两次关键内共生事件", size=PANEL_TITLE, color=INK, weight="700"))

        # 3 stage columns inside top card
        cw_s, ch_s = 212, 168
        sx1, sx2, sx3 = tx + 16, tx + 254, tx + 492
        sy = ty + 40

        # Stage 1: Prokaryotic world (>3.5 Ga to ~2.0 Ga)
        els.append(card(sx1, sy, cw_s, ch_s, rx=9, fill=SLATE_SOFT, stroke=BORDER))
        els.append(step_badge(sx1 + 20, sy + 20, "1", fg=SLATE, bg="#ffffff", r=10))
        els.append(txt(sx1 + 36, sy + 24, "漫长的原核时代", size=12.0, color=INK, weight="700"))
        els.append(txt(sx1 + 16, sy + 43, "约 35+ 亿年至 20 亿年前", size=10.2, color=MUTED, cls="mono"))
        # Mini cells schematic
        els.append(f'<ellipse cx="{sx1 + 64}" cy="{sy + 86}" rx="38" ry="24" fill="#ffffff" stroke="{PURPLE}" stroke-width="1.8"/>')
        els.append(txt(sx1 + 64, sy + 90, "古菌宿主", size=10.5, color=PURPLE, anchor="middle", weight="700"))
        els.append(f'<ellipse cx="{sx1 + 154}" cy="{sy + 72}" rx="28" ry="14" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append(txt(sx1 + 154, sy + 76, "α-变形菌", size=9.8, color=ORANGE, anchor="middle", weight="600"))
        els.append(f'<ellipse cx="{sx1 + 154}" cy="{sy + 104}" rx="28" ry="14" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.5"/>')
        els.append(txt(sx1 + 154, sy + 108, "蓝细菌", size=9.8, color=GREEN, anchor="middle", weight="600"))
        els.append(txt(sx1 + 14, sy + 138, "瓶颈：原核仅靠外膜产能，细", size=10.1, color=BODY))
        els.append(txt(sx1 + 14, sy + 155, "胞一旦变大，表面积/体积骤降！", size=10.1, color=BODY, weight="600"))

        # Arrow 1 -> 2
        els.append(_line(sx1 + cw_s + 4, sy + ch_s / 2, sx2 - 6, sy + ch_s / 2, stroke=ORANGE, sw=2.0, marker="arr-orange"))

        # Stage 2: First Endosymbiosis -> Mitochondria (Eukaryotes: Animals, Fungi, Protists)
        els.append(card(sx2, sy, cw_s, ch_s, rx=9, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(step_badge(sx2 + 20, sy + 20, "2", fg=ORANGE, bg="#ffffff", r=10))
        els.append(txt(sx2 + 36, sy + 24, "第一次合体：线粒体", size=12.0, color=ORANGE, weight="700"))
        els.append(txt(sx2 + 16, sy + 43, "约 20~18 亿年前真核共祖", size=10.2, color=MUTED, cls="mono"))
        # Host cell containing nucleus + mitochondria
        els.append(f'<ellipse cx="{sx2 + 106}" cy="{sy + 86}" rx="68" ry="30" fill="#ffffff" stroke="{PURPLE}" stroke-width="1.8"/>')
        els.append(f'<circle cx="{sx2 + 72}" cy="{sy + 86}" r="16" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.2" stroke-dasharray="3 2"/>')
        els.append(txt(sx2 + 72, sy + 90, "核DNA", size=9.6, color=PURPLE, anchor="middle", weight="700"))
        els.append(f'<ellipse cx="{sx2 + 132}" cy="{sy + 77}" rx="22" ry="9" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append(f'<ellipse cx="{sx2 + 132}" cy="{sy + 97}" rx="22" ry="9" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
        els.append(txt(sx2 + 132, sy + 80, "线粒体", size=9.2, color=ORANGE, anchor="middle", weight="700"))
        els.append(txt(sx2 + 14, sy + 138, "突破：成百上千个内膜发电站，", size=10.1, color=BODY))
        els.append(txt(sx2 + 14, sy + 155, "解锁庞大基因组 → 动物与真菌等", size=10.1, color=ORANGE, weight="700"))

        # Arrow 2 -> 3
        els.append(_line(sx2 + cw_s + 4, sy + ch_s / 2, sx3 - 6, sy + ch_s / 2, stroke=GREEN, sw=2.0, marker="arr-green"))

        # Stage 3: Second Endosymbiosis -> Chloroplast (Algae & Plants)
        els.append(card(sx3, sy, cw_s, ch_s, rx=9, fill=GREEN_SOFT, stroke=GREEN))
        els.append(step_badge(sx3 + 20, sy + 20, "3", fg=GREEN, bg="#ffffff", r=10))
        els.append(txt(sx3 + 36, sy + 24, "第二次合体：叶绿体", size=12.0, color=GREEN, weight="700"))
        els.append(txt(sx3 + 16, sy + 43, "有线粒体的真核再纳蓝细菌", size=10.2, color=MUTED))
        # Plant ancestor cell containing nucleus + mitochondrion + chloroplast
        els.append(f'<ellipse cx="{sx3 + 106}" cy="{sy + 86}" rx="72" ry="30" fill="#ffffff" stroke="{GREEN}" stroke-width="1.8"/>')
        els.append(f'<circle cx="{sx3 + 64}" cy="{sy + 86}" r="14" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.2"/>')
        els.append(txt(sx3 + 64, sy + 90, "核", size=9.6, color=PURPLE, anchor="middle", weight="700"))
        els.append(f'<ellipse cx="{sx3 + 106}" cy="{sy + 76}" rx="18" ry="8" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.4"/>')
        els.append(txt(sx3 + 106, sy + 79, "线", size=9.0, color=ORANGE, anchor="middle", weight="700"))
        els.append(f'<ellipse cx="{sx3 + 140}" cy="{sy + 92}" rx="25" ry="12" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
        els.append(txt(sx3 + 140, sy + 96, "叶绿体", size=9.5, color=GREEN, anchor="middle", weight="700"))
        els.append(txt(sx3 + 14, sy + 138, "双引擎：自备太阳能叶绿体 +", size=10.1, color=BODY))
        els.append(txt(sx3 + 14, sy + 155, "呼吸线粒体 → 藻类与陆生植物！", size=10.1, color=GREEN, weight="700"))

        # Bottom evidence card
        bx, by, bw, bh = 20, 300, 720, 126
        els.append(card(bx, by, bw, bh))
        els.append(txt(bx + 16, by + 24, "② 为什么科学界从质疑转向公认？留在每个真核细胞里的四大“细菌指纹”", size=PANEL_TITLE, color=INK, weight="700"))

        evidences = [
            ("环状独立基因组", ("自带环状 DNA，序列分别", "归属 α-变形菌与蓝细菌"), BLUE, BLUE_SOFT),
            ("细菌型 70S 核糖体", ("内部翻译机器与细菌一致，", "异于真核细胞质的 80S"), GREEN, GREEN_SOFT),
            ("双层膜与跨膜质子泵", ("保留内外双膜拓扑，靠膜", "电子传递与 ATP 合酶供能"), ORANGE, ORANGE_SOFT),
            ("只能二分裂增殖", ("细胞无法从零组装它们，", "只能由原有细胞器分裂传承"), PURPLE, PURPLE_SOFT),
        ]
        for idx, (etitle, (ed1, ed2), efg, ebg) in enumerate(evidences):
            ex = bx + 16 + idx * 174
            ey = by + 38
            els.append(card(ex, ey, 164, 74, rx=7, fill=ebg, stroke=efg, sw=1.1))
            els.append(txt(ex + 10, ey + 20, etitle, size=11.0, color=efg, weight="700"))
            els.append(txt(ex + 10, ey + 41, ed1, size=10.0, color=BODY))
            els.append(txt(ex + 10, ey + 58, ed2, size=10.0, color=BODY))

        svg = figure(
            440,
            "琳·马古利斯内共生学说两步细胞融合路径与四大分子生物学证据图",
            "展示生命从原核生物跨向复杂真核生物的两次关键内共生：古菌宿主先与好氧α-变形菌共生演化出线粒体（解锁多细胞复杂基因组能量预算），随后一支真核谱系再纳入光合蓝细菌演化出叶绿体；下方列出环状DNA、70S核糖体、双层膜质子梯度和二分裂增殖四大证据。",
            els,
        )
        write_svg(EARTH_DIR, "endosymbiosis-leap.svg", svg)

    def _build_helmont_engelmann_ruben():
        """Photo SVG 1: 3-column historical detective gallery (1648 Helmont, 1882 Engelmann, 1941 Ruben-Kamen)."""
        # Exact Helmont willow masses (Ortus Medicinae 1648):
        # Shoot: 5 lb (~2.27 kg) -> 169 lb 3 oz (~76.74 kg), delta = +74.47 kg
        # Dried soil: 200 lb (~90.72 kg) -> 199 lb 14 oz (~90.66 kg), loss = 2 oz (~0.057 kg = 57 g)
        willow_gain_kg = 76.74 - 2.27
        soil_loss_kg = 0.0567
        assert willow_gain_kg / soil_loss_kg > 1300.0  # Willow gained >1300x the soil mass lost!

        els = []
        els.extend(
            header(
                "三百年光合侦探史：大树靠吃什么长高？氧气又是从谁身上拆下来的？",
                "三座里程碑实验：1648 柳树称重排土 → 1882 棱镜细菌寻光 → 1941 重氧同位素锁定水裂解。",
            )
        )

        col_w, col_h = 232, 310
        cy = 64
        x1, x2, x3 = 20, 264, 508

        # --- Column 1: 1648 Helmont ---
        els.append(card(x1, cy, col_w, col_h))
        els.append(step_badge(x1 + 22, cy + 22, "1", fg=GREEN, bg=GREEN_SOFT, r=10))
        els.append(txt(x1 + 38, cy + 26, "1648 海尔蒙特柳树实验", size=12.5, color=INK, weight="700"))
        els.append(txt(x1 + 16, cy + 46, "只浇雨水五年，烘干泥土前后称重", size=10.3, color=MUTED))

        # Quantitative bar comparison inside Col 1
        bx0, bw_max = x1 + 18, 132.0
        w_init = (2.27 / 90.72) * bw_max
        w_final = (76.74 / 90.72) * bw_max
        s_init = bw_max
        s_final = (90.66 / 90.72) * bw_max

        els.append(txt(bx0, cy + 72, "柳树质量（+74.5 kg，暴涨 33 倍）", size=10.4, color=GREEN, weight="700"))
        els.append(f'<rect x="{bx0}" y="{cy + 80}" width="{max(4.0, w_init):.1f}" height="12" rx="3" fill="{GREEN_SOFT}" stroke="{GREEN}"/>')
        els.append(txt(bx0 + w_init + 6, cy + 90, "初：2.27 kg (5磅)", size=9.8, color=MUTED, cls="mono"))
        els.append(f'<rect x="{bx0}" y="{cy + 98}" width="{w_final:.1f}" height="14" rx="3" fill="{GREEN}"/>')
        els.append(txt(bx0 + w_final + 6, cy + 109, "5年后：76.8 kg", size=10.0, color=GREEN, weight="700", cls="mono"))

        els.append(txt(bx0, cy + 136, "干土质量（仅少 57 g ≈ 2 盎司！）", size=10.4, color=ORANGE, weight="700"))
        els.append(f'<rect x="{bx0}" y="{cy + 144}" width="{s_init:.1f}" height="12" rx="3" fill="{ORANGE_SOFT}" stroke="{ORANGE}"/>')
        els.append(txt(bx0 + s_init + 6, cy + 154, "90.72 kg", size=9.8, color=MUTED, cls="mono"))
        els.append(f'<rect x="{bx0}" y="{cy + 162}" width="{s_final:.1f}" height="12" rx="3" fill="{ORANGE}" opacity="0.78"/>')
        els.append(txt(bx0 + s_final + 6, cy + 172, "90.66 kg", size=9.8, color=ORANGE, weight="700", cls="mono"))

        els.append(card(x1 + 14, cy + 190, col_w - 28, 106, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(x1 + 24, cy + 210, "• 突破：首次用定量天平证伪“植物", size=10.1, color=BODY))
        els.append(txt(x1 + 24, cy + 227, "  吃泥土长肉”的古希腊直觉！", size=10.1, color=INK, weight="600"))
        els.append(txt(x1 + 24, cy + 246, "• 美丽的误判：他以为 74.5 kg 全是", size=10.1, color=BODY))
        els.append(txt(x1 + 24, cy + 263, "  水变的，当时人类还不认识空气里", size=10.1, color=BODY))
        els.append(txt(x1 + 24, cy + 280, "  看不见的碳源 CO₂。", size=10.1, color=GREEN, weight="700"))

        # --- Column 2: 1882 Engelmann ---
        els.append(card(x2, cy, col_w, col_h))
        els.append(step_badge(x2 + 22, cy + 22, "2", fg=BLUE, bg=BLUE_SOFT, r=10))
        els.append(txt(x2 + 38, cy + 26, "1882 恩格尔曼棱镜寻氧", size=12.5, color=INK, weight="700"))
        els.append(txt(x2 + 16, cy + 46, "三棱镜分光投射丝状绿藻+好氧细菌", size=10.3, color=MUTED))

        # Computed bacterial clustering curve across 400..700 nm
        ex0, ex1 = x2 + 20, x2 + col_w - 20  # 192px wide
        ey_top, ey_alg = cy + 72, cy + 146

        def bact_density(wl):
            blue_pk = 0.95 * math.exp(-(((wl - 445.0) / 26.0) ** 2))
            red_pk = 0.90 * math.exp(-(((wl - 660.0) / 22.0) ** 2))
            return 0.06 + blue_pk + red_pk

        assert bact_density(445) > 0.90 and bact_density(660) > 0.85 and bact_density(540) < 0.12

        pts_bact = []
        for i in range(61):
            wl = 400.0 + 300.0 * i / 60.0
            xx = ex0 + (i / 60.0) * (ex1 - ex0)
            yy = ey_alg - bact_density(wl) * (ey_alg - ey_top)
            pts_bact.append((xx, yy))

        els.append(_area_under(pts_bact, ey_alg, BLUE, opacity=0.18))
        els.append(_polyline(pts_bact, stroke=BLUE, sw=2.3, trace=True))
        # Algal filament bar + rainbow spectral segments
        els.append(f'<rect x="{ex0}" y="{ey_alg}" width="{ex1 - ex0}" height="11" rx="4" fill="#86efac" stroke="{GREEN}" stroke-width="1.2"/>')
        els.append(txt((ex0 + ex1) / 2, ey_alg + 9, "丝状绿藻（水绵 / 刚毛藻）", size=8.8, color=INK, anchor="middle", weight="600"))

        spec_bands = [
            (400, 450, "#6d28d9"),
            (450, 495, "#2563eb"),
            (495, 565, "#16a34a"),
            (565, 595, "#eab308"),
            (595, 630, "#f97316"),
            (630, 700, "#dc2626"),
        ]
        for w0, w1, scol in spec_bands:
            sx = ex0 + (w0 - 400.0) / 300.0 * (ex1 - ex0)
            sw_b = (w1 - w0) / 300.0 * (ex1 - ex0)
            els.append(f'<rect x="{sx:.1f}" y="{ey_alg + 14}" width="{sw_b:.1f}" height="6" fill="{scol}"/>')

        els.append(txt(ex0 + 28, ey_top + 4, "蓝紫光簇拥", size=9.8, color=BLUE, anchor="middle", weight="700", halo=True))
        els.append(txt((ex0 + ex1) / 2, ey_alg - 12, "绿光冷清", size=9.6, color=MUTED, anchor="middle", halo=True))
        els.append(txt(ex1 - 28, ey_top + 6, "红光簇拥", size=9.8, color=ORANGE, anchor="middle", weight="700", halo=True))
        els.append(txt(ex0, ey_alg + 32, "400nm", size=9.5, color=MUTED, cls="mono"))
        els.append(txt((ex0 + ex1) / 2, ey_alg + 32, "550nm", size=9.5, color=MUTED, anchor="middle", cls="mono"))
        els.append(txt(ex1, ey_alg + 32, "700nm", size=9.5, color=MUTED, anchor="end", cls="mono"))

        els.append(card(x2 + 14, cy + 190, col_w - 28, 106, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(x2 + 24, cy + 210, "• 巧思：没有现代电极，就让好氧细", size=10.1, color=BODY))
        els.append(txt(x2 + 24, cy + 227, "  菌充当“活体氧气传感器”！", size=10.1, color=INK, weight="600"))
        els.append(txt(x2 + 24, cy + 246, "• 结论：细菌密集围在蓝紫光与红光", size=10.1, color=BODY))
        els.append(txt(x2 + 24, cy + 263, "  区，证明叶绿素主要吃这两段光产", size=10.1, color=BODY))
        els.append(txt(x2 + 24, cy + 280, "  氧，而对绿光吸收最少。", size=10.1, color=BLUE, weight="700"))

        # --- Column 3: 1941 Ruben & Kamen ---
        els.append(card(x3, cy, col_w, col_h))
        els.append(step_badge(x3 + 22, cy + 22, "3", fg=ORANGE, bg=ORANGE_SOFT, r=10))
        els.append(txt(x3 + 38, cy + 26, "1941 鲁宾与卡门重氧追踪", size=12.5, color=INK, weight="700"))
        els.append(txt(x3 + 16, cy + 46, "用同位素 ¹⁸O 给水或 CO₂ 挂“车牌”", size=10.3, color=MUTED))

        # Group A vs Group B boxes (use SVG <tspan> superscripts so 18O / 16O render crisp in all fonts!)
        els.append(card(x3 + 14, cy + 62, col_w - 28, 54, rx=7, fill="#fff7ed", stroke=ORANGE, sw=1.3))
        els.append(txt(x3 + 24, cy + 81, "实验甲组（标记水中的重氧）：", size=10.3, color=ORANGE, weight="700"))
        els.append(
            f'<text x="{x3 + 24}" y="{cy + 103}" font-size="11.0" fill="{INK}" font-weight="700">'
            f'H<tspan dy="3" font-size="8.5">2</tspan><tspan dy="-7" font-size="8.5" fill="{ORANGE}">18</tspan>'
            f'<tspan dy="4">O + CO</tspan><tspan dy="3" font-size="8.5">2</tspan>'
            f'<tspan dy="-3">  →  释放 </tspan><tspan dy="-4" font-size="8.5" fill="{ORANGE}">18</tspan>'
            f'<tspan dy="4" fill="{ORANGE}">O</tspan><tspan dy="3" font-size="8.5" fill="{ORANGE}">2</tspan>'
            f'<tspan dy="-3" fill="{ORANGE}"> !</tspan></text>'
        )

        els.append(card(x3 + 14, cy + 124, col_w - 28, 54, rx=7, fill=SLATE_SOFT, stroke=BORDER, sw=1.2))
        els.append(txt(x3 + 24, cy + 143, "实验乙组（标记二氧化碳重氧）：", size=10.3, color=SLATE, weight="700"))
        els.append(
            f'<text x="{x3 + 24}" y="{cy + 165}" font-size="11.0" fill="{BODY}" font-weight="600">'
            f'H<tspan dy="3" font-size="8.5">2</tspan><tspan dy="-3">O + C</tspan>'
            f'<tspan dy="-4" font-size="8.5" fill="{BLUE}">18</tspan><tspan dy="4">O</tspan>'
            f'<tspan dy="3" font-size="8.5">2</tspan><tspan dy="-3">  →  释放普通 </tspan>'
            f'<tspan dy="-4" font-size="8.5">16</tspan><tspan dy="4">O</tspan><tspan dy="3" font-size="8.5">2</tspan></text>'
        )

        els.append(card(x3 + 14, cy + 190, col_w - 28, 106, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(x3 + 24, cy + 210, "• 一锤定音：你我呼吸的 O₂ 全部来", size=10.1, color=BODY))
        els.append(txt(x3 + 24, cy + 227, "  自光系统裂解水，而非拆开 CO₂！", size=10.1, color=ORANGE, weight="700"))
        els.append(txt(x3 + 24, cy + 246, "• 接续拼图：1950s 卡尔文团队再用", size=10.1, color=BODY))
        els.append(txt(x3 + 24, cy + 263, "  放射性 ¹⁴CO₂ 与“棒棒糖”藻瓶，", size=10.1, color=BODY))
        els.append(txt(x3 + 24, cy + 280, "  追清碳变糖路径（1961 诺奖）。", size=10.1, color=INK, weight="600"))

        # Bottom timeline strip
        els.append(card(20, 386, 720, 38, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(
            txt(
                380,
                410,
                "接力链：1648 排土 → 1771/1779 阳光+绿叶净气 → 1882 红蓝光谱 → 1941 重氧证水裂解 → 1950s 卡尔文追碳循环",
                size=10.3,
                color=INK,
                anchor="middle",
                weight="600",
            )
        )

        svg = figure(
            438,
            "光合作用三百年三大经典实验图解：海尔蒙特柳树、恩格尔曼棱镜好氧细菌与鲁宾卡门重氧同位素",
            "三栏并列展示：1648年海尔蒙特五年柳树增重74.5千克而土壤仅减57克；1882年恩格尔曼用棱镜分光照射丝状绿藻，好氧细菌聚集在430-460nm蓝紫光与650-670nm红光区；1941年鲁宾与卡门用H2-18O和C-18O2对比证明光合释放的氧气来自水裂解。",
            els,
            extra_css=TRACE_CSS,
        )
        write_svg(PHOTO_DIR, "helmont-engelmann-ruben.svg", svg)

    def _chl_a_abs(wl):
        """Analytical diethyl-ether reference absorption profile for Chlorophyll a (peaks ~430 nm, ~662 nm)."""
        return (
            0.42 * math.exp(-(((wl - 410.0) / 18.0) ** 2))
            + 0.94 * math.exp(-(((wl - 430.0) / 14.0) ** 2))
            + 0.05
            + 0.14 * math.exp(-(((wl - 616.0) / 16.0) ** 2))
            + 0.78 * math.exp(-(((wl - 662.0) / 12.5) ** 2))
        )

    def _chl_b_abs(wl):
        """Analytical diethyl-ether reference absorption profile for Chlorophyll b (peaks ~453 nm, ~642 nm)."""
        return (
            0.25 * math.exp(-(((wl - 430.0) / 18.0) ** 2))
            + 0.88 * math.exp(-(((wl - 453.0) / 15.0) ** 2))
            + 0.04
            + 0.11 * math.exp(-(((wl - 595.0) / 16.0) ** 2))
            + 0.48 * math.exp(-(((wl - 642.0) / 13.0) ** 2))
        )

    def _carot_abs(wl):
        """Analytical reference absorption profile for beta-carotene / carotenoids (peaks ~448, 476 nm; zero in red)."""
        if wl > 535.0:
            return 0.02 * math.exp(-(((wl - 535.0) / 12.0) ** 2))
        return (
            0.34 * math.exp(-(((wl - 424.0) / 15.0) ** 2))
            + 0.62 * math.exp(-(((wl - 450.0) / 14.0) ** 2))
            + 0.56 * math.exp(-(((wl - 478.0) / 13.0) ** 2))
        )

    def _build_chlorophyll_spectrum_autumn():
        """Photo SVG 2: Computed Chl a, Chl b, Carotenoid 400-700nm curves + green window + autumn nitrogen recycling."""
        # Verify peaks & green valley
        assert _chl_a_abs(430) > 0.95 and _chl_a_abs(662) > 0.80 and _chl_a_abs(535) < 0.08
        assert _chl_b_abs(453) > 0.88 and _chl_b_abs(642) > 0.50 and _chl_b_abs(535) < 0.07
        assert _carot_abs(452) > 0.62 and _carot_abs(600) < 0.01

        els = []
        els.extend(
            header(
                "叶子为什么偏偏是绿色而不是全黑？光合色素光谱与秋叶变色之谜",
                "左图绘制叶绿素 a、叶绿素 b 与类胡萝卜素可见光吸收曲线（乙醚提取参考峰）；右图解析绿光透射与秋叶氮回收。",
            )
        )

        # Left panel: Quantitative 400-700 nm absorption spectrum
        lx, ly, lw, lh = 20, 64, 436, 358
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① 三类叶片色素吸收光谱（400–700 nm）", size=PANEL_TITLE, color=INK, weight="700"))

        px0, px1 = lx + 48, lx + lw - 20  # 68 .. 436 (368px)
        py0, py1 = ly + 56, ly + 258      # 120 .. 322 (202px), norm absorbance 0..1.08

        def sx(wl):
            return px0 + (wl - 400.0) / 300.0 * (px1 - px0)

        def sy(ab):
            return py1 - (min(ab, 1.08) / 1.08) * (py1 - py0)

        # Shaded 500-560 nm Green reflectance & deep-leaf transmission window
        gx0, gx1 = sx(500.0), sx(560.0)
        els.append(
            f'<rect x="{gx0:.1f}" y="{py0:.1f}" width="{gx1 - gx0:.1f}" height="{py1 - py0:.1f}" '
            f'fill="{GREEN_SOFT}" opacity="0.80"/>'
        )
        els.append(txt((gx0 + gx1) / 2, py0 + 52, "500–560 nm", size=10.0, color=GREEN, anchor="middle", weight="700", cls="mono"))
        els.append(txt((gx0 + gx1) / 2, py0 + 68, "绿光低吸收窗", size=10.2, color=GREEN, anchor="middle", weight="700"))
        els.append(txt((gx0 + gx1) / 2, py0 + 84, "反射呈绿 +", size=9.8, color=BODY, anchor="middle"))
        els.append(txt((gx0 + gx1) / 2, py0 + 98, "透入下层叶肉", size=9.8, color=BODY, anchor="middle"))

        # Grid lines
        for yv, ylbl in [(0.0, "0"), (0.5, "0.5"), (1.0, "1.0")]:
            yy = sy(yv)
            els.append(_line(px0, yy, px1, yy, stroke=HAIRLINE, sw=0.9, dash="3 3"))
            els.append(txt(px0 - 6, yy + 4, ylbl, size=10.0, color=MUTED, anchor="end", cls="mono"))

        for wl in (400, 450, 500, 550, 600, 650, 700):
            xx = sx(wl)
            els.append(_line(xx, py0, xx, py1, stroke=HAIRLINE, sw=0.8, dash="2 3"))
            els.append(txt(xx, py1 + 24, str(wl), size=10.0, color=MUTED, anchor="middle", cls="mono"))

        els.append(_line(px0, py0, px0, py1, stroke=SLATE, sw=1.2))
        els.append(_line(px0, py1, px1, py1, stroke=SLATE, sw=1.2))

        # Visible wavelength color strip directly under X-axis
        bands = [
            (400, 440, "#7c3aed"),
            (440, 490, "#2563eb"),
            (490, 565, "#16a34a"),
            (565, 590, "#eab308"),
            (590, 625, "#f97316"),
            (625, 700, "#dc2626"),
        ]
        for w0, w1, col in bands:
            els.append(
                f'<rect x="{sx(w0):.1f}" y="{py1 + 3:.1f}" width="{sx(w1) - sx(w0):.1f}" height="7" fill="{col}" opacity="0.88"/>'
            )

        wls = [400.0 + 300.0 * i / 120.0 for i in range(121)]
        pts_a = [(sx(w), sy(_chl_a_abs(w))) for w in wls]
        pts_b = [(sx(w), sy(_chl_b_abs(w))) for w in wls]
        pts_c = [(sx(w), sy(_carot_abs(w))) for w in wls]

        els.append(_polyline(pts_c, stroke=ORANGE, sw=2.1, dash="3 3"))
        els.append(_polyline(pts_b, stroke=BLUE, sw=2.2, dash="7 4"))
        els.append(_polyline(pts_a, stroke=GREEN, sw=2.6, trace=True))

        # Peak callouts (carefully spaced!)
        els.append(txt(sx(430) - 4, sy(_chl_a_abs(430)) - 7, "Chl a 430nm", size=10.0, color=GREEN, anchor="middle", weight="700", halo=True))
        els.append(txt(sx(453) + 10, sy(_chl_b_abs(453)) - 4, "Chl b 453nm", size=10.0, color=BLUE, anchor="start", weight="700", halo=True))
        els.append(txt(sx(482) + 8, sy(_carot_abs(478)) + 16, "类胡萝卜素", size=9.8, color=ORANGE, anchor="start", weight="700", halo=True))
        els.append(txt(sx(642) - 8, sy(_chl_b_abs(642)) - 8, "642nm", size=9.8, color=BLUE, anchor="end", weight="700", halo=True))
        els.append(txt(sx(662), sy(_chl_a_abs(662)) - 8, "662nm", size=10.0, color=GREEN, anchor="middle", weight="700", halo=True))

        # Legend & in-vivo note inside bottom of Left Panel
        ly_leg = ly + 296
        els.append(_line(lx + 18, ly_leg, lx + 42, ly_leg, stroke=GREEN, sw=2.6))
        els.append(txt(lx + 47, ly_leg + 4, "叶绿素 a（主反应中心+天线）", size=10.2, color=INK, weight="600"))
        els.append(_line(lx + 226, ly_leg, lx + 250, ly_leg, stroke=BLUE, sw=2.2, dash="6 3"))
        els.append(txt(lx + 255, ly_leg + 4, "叶绿素 b（拓宽蓝/橙红吸光带）", size=10.2, color=INK))
        els.append(_line(lx + 18, ly_leg + 20, lx + 42, ly_leg + 20, stroke=ORANGE, sw=2.1, dash="3 3"))
        els.append(txt(lx + 47, ly_leg + 24, "类胡萝卜素（吸蓝紫光 + 耗散过剩强光防灼伤）", size=10.2, color=INK))
        els.append(txt(lx + 18, ly_leg + 44, "注：活体蛋白结合态峰值较有机溶剂略红移约 10–20 nm（如反应中心 P680、P700）。", size=9.8, color=MUTED))

        # Right panel: Why not black + Why autumn leaves turn yellow/red
        rx, ry, rw, rh = 472, 64, 268, 358
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 14, ry + 24, "② 叶片光学与秋叶回收账", size=PANEL_TITLE, color=INK, weight="700"))

        # Top sub-card: Why not black?
        els.append(card(rx + 12, ry + 38, rw - 24, 148, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(rx + 22, ry + 58, "全黑吸光 100% 岂不更划算？", size=11.2, color=GREEN, weight="700"))
        els.append(txt(rx + 22, ry + 78, "1. 深层接力：上表层叶绿素吃掉红", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 94, "   蓝光，绿光穿透更深喂饱下层细", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 110, "   胞（整片厚叶绿光吸收其实不低）", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 128, "2. 正午防烧伤：强光远超固碳酶速", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 144, "   率上限，全黑会导致高热蒸腾与", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 160, "   活性氧光氧化损伤！", size=10.0, color=INK, weight="600"))

        # Bottom sub-card: Autumn yellow & red
        els.append(card(rx + 12, ry + 198, rw - 24, 146, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(rx + 22, ry + 218, "秋天树叶为什么变黄、变红？", size=11.2, color=ORANGE, weight="700"))
        els.append(txt(rx + 22, ry + 238, "• 变黄（揭底色）：叶绿素含宝贵的", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 254, "  氮(N)和镁，落叶前树主动拆解叶", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 270, "  绿素运回枝干过冬，露出原本就在", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 286, "  的类胡萝卜素金黄色！", size=10.0, color=INK, weight="600"))
        els.append(txt(rx + 22, ry + 306, "• 变红（打遮阳伞）：枫树等新合成", size=10.0, color=BODY))
        els.append(txt(rx + 22, ry + 322, "  花青素挡住秋日寒光，掩护氮撤退", size=10.0, color=ORANGE, weight="700"))

        svg = figure(
            436,
            "叶绿素a、叶绿素b与类胡萝卜素可见光吸收光谱、绿光透射窗口及秋叶氮回收机制图",
            "左图精确绘制400至700nm波长范围内叶绿素a（430nm、662nm双峰）、叶绿素b（453nm、642nm双峰）与类胡萝卜素（450-480nm蓝紫吸收）的吸收曲线及500-560nm绿光窗口；右图解释全黑叶片的光抑制风险、绿光深层透射优势，以及秋季拆解叶绿素回收氮素露出类胡萝卜素黄底与新合成花青素变红的原理。",
            els,
            extra_css=TRACE_CSS,
        )
        write_svg(PHOTO_DIR, "chlorophyll-spectrum-autumn.svg", svg)

    def _build_z_scheme_redox():
        """Photo SVG 3: Quantitative Z-scheme redox potential ladder (pH 7 E0' from +1.20V P680 to -1.25V P700*)."""
        els = []
        els.extend(
            header(
                "光合作用“Z 字形”能量阶梯：两颗光子怎样把水的电子送上高能山顶？",
                "纵轴为 pH 7 标准氧化还原电位 E₀'（越往上电位越负、电子自由能越高）；实线为线性电子流。",
            )
        )

        cx, cy, cw, ch = 20, 64, 720, 382
        els.append(card(cx, cy, cw, ch))
        els.append(txt(cx + 16, cy + 24, "① 为什么单靠一颗可见光子不够既裂解水（+0.82 V）又还原 NADP⁺（-0.32 V）？", size=PANEL_TITLE, color=INK, weight="700"))

        # Y-axis mapping E0' in [-1.4 V, +1.4 V] -> [y_top=126, y_bot=406] (280px for 2.8V = 100 px/V)
        px0, px1 = 96.0, 712.0
        y_top, y_bot = 126.0, 406.0

        def ey(volt):
            # -1.4V at y_top, +1.4V at y_bot
            return y_top + (volt - (-1.4)) / 2.8 * (y_bot - y_top)

        assert ey(-1.25) < ey(-0.32) < ey(0.0) < ey(0.82) < ey(1.20)

        for v in (-1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2):
            yy = ey(v)
            els.append(_line(px0, yy, px1, yy, stroke=HAIRLINE if v != 0.0 else SLATE, sw=0.9, dash="3 3"))
            vlbl = f"{v:+.1f} V" if v != 0.0 else " 0.0 V"
            els.append(txt(px0 - 8, yy + 4, vlbl, size=10.2, color=MUTED, anchor="end", cls="mono"))

        els.append(_line(px0, y_top, px0, y_bot, stroke=SLATE, sw=1.3))
        els.append(txt(px0 - 8, y_top - 8, "高能还原 ↑", size=10.0, color=BLUE, anchor="end", weight="700"))
        els.append(txt(px0 - 8, y_bot + 16, "低能强氧化 ↓", size=10.0, color=ORANGE, anchor="end", weight="700"))

        # Key redox nodes (x, E0'_V, short_tag, sub_note, color)
        n_h2o = (140.0, 0.82)
        n_p680 = (226.0, 1.20)
        n_p680s = (226.0, -0.80)
        n_pq = (308.0, 0.00)
        n_cyt = (374.0, 0.12)
        n_pc = (434.0, 0.37)
        n_p700 = (488.0, 0.43)
        n_p700s = (488.0, -1.25)
        n_fd = (576.0, -0.43)
        n_nadph = (666.0, -0.32)

        pts_z = [
            (n_h2o[0], ey(n_h2o[1])),
            (n_p680[0], ey(n_p680[1])),
            (n_p680s[0], ey(n_p680s[1])),
            (n_pq[0], ey(n_pq[1])),
            (n_cyt[0], ey(n_cyt[1])),
            (n_pc[0], ey(n_pc[1])),
            (n_p700[0], ey(n_p700[1])),
            (n_p700s[0], ey(n_p700s[1])),
            (n_fd[0], ey(n_fd[1])),
            (n_nadph[0], ey(n_nadph[1])),
        ]

        # Highlight the two vertical photon jumps in bright gold/green and electron cascade in blue
        els.append(_line(pts_z[0][0], pts_z[0][1], pts_z[1][0], pts_z[1][1], stroke=BLUE, sw=2.3, marker="arr-blue"))
        els.append(_line(pts_z[1][0], pts_z[1][1] - 6, pts_z[2][0], pts_z[2][1] + 8, stroke=ORANGE, sw=3.0, marker="arr-orange"))
        els.append(_polyline(pts_z[2:7], stroke=BLUE, sw=2.4, trace=True))
        els.append(_line(pts_z[6][0], pts_z[6][1] - 6, pts_z[7][0], pts_z[7][1] + 8, stroke=GREEN, sw=3.0, marker="arr-green"))
        els.append(_polyline(pts_z[7:], stroke=BLUE, sw=2.4, trace=True))

        # Cyclic electron flow dashed arc from Fd back to Cyt b6f
        fx, fy = pts_z[8]
        cx_b, cy_b = pts_z[4]
        els.append(
            f'<path d="M {fx - 6:.1f},{fy - 6:.1f} Q {(fx + cx_b) / 2 - 20:.1f},{fy - 58:.1f} {cx_b:.1f},{cy_b - 10:.1f}" '
            f'fill="none" stroke="{PURPLE}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#arr-muted)"/>'
        )
        els.append(txt((fx + cx_b) / 2 - 22, fy - 42, "循环电子流（补产 ATP）", size=9.8, color=PURPLE, anchor="middle", weight="600", halo=True))

        # Node circles and crisp non-overlapping labels
        nodes_meta = [
            (n_h2o, BLUE, "2H₂O → O₂+4H⁺", "+0.82 V（放氧复合体）", "above-left"),
            (n_p680, ORANGE, "PSII: P680⁺", "+1.20 V（生物界最强氧化剂！）", "below"),
            (n_p680s, ORANGE, "P680* 激发态", "约 -0.80 V", "above"),
            (n_pq, SLATE, "PQ", "", "above"),
            (n_cyt, GREEN, "Cyt b₆f", "泵 H⁺ 入腔产 ATP", "below-left"),
            (n_pc, SLATE, "PC", "", "above"),
            (n_p700, GREEN, "PSI: P700⁺", "+0.43 V", "below-left"),
            (n_p700s, GREEN, "P700* (-1.25 V)", "", "above"),
            (n_fd, BLUE, "Fd", "-0.43 V", "above"),
            (n_nadph, BLUE, "NADPH", "-0.32 V（送往卡尔文循环）", "below-right"),
        ]
        for (nx, nv), col, title_s, sub_s, pos in nodes_meta:
            ny = ey(nv)
            els.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="5.5" fill="{col}" stroke="#ffffff" stroke-width="1.4"/>')
            if pos == "above":
                els.append(txt(nx, ny - 10, title_s, size=10.5, color=col, anchor="middle", weight="700", halo=True))
                if sub_s:
                    els.append(txt(nx, ny - 24, sub_s, size=9.6, color=MUTED, anchor="middle", cls="mono", halo=True))
            elif pos == "below":
                els.append(txt(nx, ny + 18, title_s, size=10.5, color=col, anchor="middle", weight="700", halo=True))
                if sub_s:
                    els.append(txt(nx, ny + 32, sub_s, size=9.6, color=BODY, anchor="middle", halo=True))
            elif pos == "above-left":
                els.append(txt(nx - 24, ny - 24, title_s, size=10.4, color=INK, anchor="start", weight="700", halo=True))
                els.append(txt(nx - 24, ny - 10, sub_s, size=9.6, color=BLUE, anchor="start", halo=True))
            elif pos == "below-left":
                els.append(txt(nx - 6, ny + 18, title_s, size=10.4, color=col, anchor="end", weight="700", halo=True))
                els.append(txt(nx - 6, ny + 32, sub_s, size=9.6, color=col, anchor="end", weight="600", halo=True))
            elif pos == "below-right":
                els.append(txt(nx, ny + 18, title_s, size=11.0, color=BLUE, anchor="middle", weight="700", halo=True))
                els.append(txt(nx - 8, ny + 33, sub_s, size=9.6, color=BODY, anchor="end", halo=True))

        # Photon jump badges on the two vertical risers
        els.append(pill(144, ey(0.22), "光子① 680nm", fg=ORANGE, bg=ORANGE_SOFT, w=74, h=20, size=10.0))
        els.append(pill(406, ey(-0.45), "光子② 700nm", fg=GREEN, bg=GREEN_SOFT, w=74, h=20, size=10.0))

        # Bottom-right thermodynamic summary card inside main plot
        els.append(card(520, 314, 198, 118, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(532, 334, "热力学收支硬核点：", size=11.0, color=BLUE, weight="700"))
        els.append(txt(532, 353, "• 净逆坡：+0.82 V → -0.32 V", size=10.0, color=INK, weight="600", cls="mono"))
        els.append(txt(532, 370, "  （ΔE₀' = -1.14 V，绝不会自发发生）", size=9.8, color=BODY))
        els.append(txt(532, 388, "• 两次光激发接力 + 中段顺坡产 ATP", size=9.9, color=BODY))
        els.append(txt(532, 406, "• 裂解 2H₂O 传 4e⁻ 放 1O₂，至少", size=9.9, color=BODY))
        els.append(txt(532, 422, "  需吸收 8 颗光子（4 + 4）！", size=10.0, color=GREEN, weight="700"))

        svg = figure(
            460,
            "光合作用Z字形标准氧化还原电位阶梯图（PSII P680裂解水、细胞色素b6f质子泵与PSI P700生成NADPH）",
            "以pH 7标准氧化还原电位E0'为纵轴（-1.4V至+1.4V），定量展示水的电子（+0.82V）被地球最强生物氧化剂P680+（+1.20V）夺取后，经680nm光子激发至P680*（-0.80V），顺传递链经Cyt b6f泵质子产ATP到达P700（+0.43V），再经700nm光子二次激发至P700*（-1.25V），最终经铁氧还蛋白生成NADPH（-0.32V），同时标出循环电子流。",
            els,
            extra_css=TRACE_CSS,
        )
        write_svg(PHOTO_DIR, "z-scheme-redox.svg", svg)

    def _build_c3_c4_cam_pumps():
        """Photo SVG 4: Rubisco bottleneck + C3 direct vs C4 Kranz spatial vs CAM night/day temporal CO2 pumps."""
        els = []
        els.extend(
            header(
                "地球上最慢、最多的酶 Rubisco，与 C3、C4、CAM 三套供碳方案",
                "卡尔文循环是共同终点；区别在于要不要花额外能量，在空间或时间上给 Rubisco 建立“CO₂ 增压舱”。",
            )
        )

        # Top banner card: Rubisco's ancient evolutionary dilemma
        els.append(card(20, 64, 720, 74, rx=9, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.2))
        els.append(txt(36, 86, "① 共同瓶颈：Rubisco 酶的“远古胎记”（占 C3 叶片可溶性蛋白 30%–50%，地球丰度第一酶）", size=12.0, color=ORANGE, weight="700"))
        els.append(txt(36, 106, "• 奇慢无比：每个活性位点每秒仅固定约 3–10 个 CO₂（普通酶常达上千至十万次），植物只好靠“酶海战术”堆数量！", size=10.1, color=BODY))
        els.append(txt(36, 124, "• 会认错人：诞生于远古高 CO₂ 缺氧海；如今大气 O₂ 占 21% 而 CO₂ 仅 ~0.042%，酷热关小气孔时 O₂ 抢位引发光呼吸。", size=10.1, color=INK, weight="600"))

        col_w, col_h = 232, 282
        cy = 150
        x1, x2, x3 = 20, 264, 508

        # --- Column 1: C3 ---
        els.append(card(x1, cy, col_w, col_h))
        els.append(txt(x1 + 16, cy + 24, "② C3 植物｜单室直通", size=13.0, color=BLUE, weight="700"))
        els.append(pill(x1 + 16, cy + 34, "水稻 · 小麦 · 大豆 · 树木", fg=BLUE, bg=BLUE_SOFT, w=176, h=20, size=10.2))

        # Single mesophyll cell schematic
        els.append(card(x1 + 16, cy + 64, col_w - 32, 118, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(x1 + col_w / 2, cy + 84, "叶肉细胞（白天开气孔）", size=10.8, color=BLUE, anchor="middle", weight="700"))
        els.append(txt(x1 + col_w / 2, cy + 106, "CO₂（与 21% O₂ 同室竞争）", size=10.0, color=BODY, anchor="middle"))
        els.append(_line(x1 + col_w / 2, cy + 112, x1 + col_w / 2, cy + 128, stroke=BLUE, sw=1.8, marker="arr-blue"))
        els.append(txt(x1 + col_w / 2, cy + 144, "Rubisco → 三碳 3-PGA", size=10.6, color=INK, anchor="middle", weight="700"))
        els.append(txt(x1 + col_w / 2, cy + 164, "（酷热干旱时易发光呼吸失碳）", size=9.8, color=ORANGE, anchor="middle", weight="600"))

        els.append(txt(x1 + 16, cy + 204, "• 优点：温凉湿润时免交额外泵碳", size=10.2, color=BODY))
        els.append(txt(x1 + 16, cy + 221, "  能量税，量子效率反而更高！", size=10.2, color=GREEN, weight="600"))
        els.append(txt(x1 + 16, cy + 241, "• 弱点：高温强光关小气孔保水时，", size=10.2, color=BODY))
        els.append(txt(x1 + 16, cy + 258, "  叶内缺 CO₂，光呼吸损耗大增。", size=10.2, color=BODY))

        # --- Column 2: C4 ---
        els.append(card(x2, cy, col_w, col_h))
        els.append(txt(x2 + 16, cy + 24, "③ C4 植物｜空间双室增压", size=13.0, color=GREEN, weight="700"))
        els.append(pill(x2 + 16, cy + 34, "玉米 · 甘蔗 · 高粱 · 小米", fg=GREEN, bg=GREEN_SOFT, w=176, h=20, size=10.2))

        # Outer mesophyll + inner bundle-sheath schematic (Kranz anatomy)
        els.append(card(x2 + 16, cy + 64, col_w - 32, 52, rx=7, fill="#f0fdf4", stroke=GREEN))
        els.append(txt(x2 + col_w / 2, cy + 82, "外室·叶肉细胞：PEP 羧化酶", size=10.3, color=GREEN, anchor="middle", weight="700"))
        els.append(txt(x2 + col_w / 2, cy + 99, "不理 O₂，专抓 CO₂ 制成四碳酸", size=9.8, color=BODY, anchor="middle"))

        els.append(_line(x2 + col_w / 2, cy + 116, x2 + col_w / 2, cy + 128, stroke=GREEN, sw=2.0, marker="arr-green"))

        els.append(card(x2 + 16, cy + 130, col_w - 32, 52, rx=7, fill=GREEN_SOFT, stroke=GREEN, sw=1.6))
        els.append(txt(x2 + col_w / 2, cy + 148, "内室·维管束鞘（厚壁少氧）", size=10.3, color=INK, anchor="middle", weight="700"))
        els.append(txt(x2 + col_w / 2, cy + 165, "脱羧释放高浓 CO₂ 喂饱 Rubisco！", size=9.8, color=GREEN, anchor="middle", weight="700"))

        els.append(txt(x2 + 16, cy + 204, "• 空间换效率：“花环结构”两套细", size=10.2, color=BODY))
        els.append(txt(x2 + 16, cy + 221, "  胞接力，把光呼吸压到极低水平。", size=10.2, color=GREEN, weight="600"))
        els.append(txt(x2 + 16, cy + 241, "• 代价：每泵 1 个 CO₂ 需多花约", size=10.2, color=BODY))
        els.append(txt(x2 + 16, cy + 258, "  2 ATP，在烈日高温草原最划算！", size=10.2, color=BODY))

        # --- Column 3: CAM ---
        els.append(card(x3, cy, col_w, col_h))
        els.append(txt(x3 + 16, cy + 24, "④ CAM 植物｜昼夜错峰储碳", size=13.0, color=PURPLE, weight="700"))
        els.append(pill(x3 + 16, cy + 34, "仙人掌 · 菠萝 · 龙舌兰 · 多肉", fg=PURPLE, bg=PURPLE_SOFT, w=188, h=20, size=10.2))

        # Night vs Day inside same cell
        els.append(card(x3 + 16, cy + 64, col_w - 32, 52, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(x3 + col_w / 2, cy + 82, "夜晚凉爽｜打开气孔吸气", size=10.3, color=PURPLE, anchor="middle", weight="700"))
        els.append(txt(x3 + col_w / 2, cy + 99, "CO₂ → 制成苹果酸锁进大液泡", size=9.8, color=BODY, anchor="middle"))

        els.append(_line(x3 + col_w / 2, cy + 116, x3 + col_w / 2, cy + 128, stroke=SLATE, sw=1.8, marker="arr-muted"))

        els.append(card(x3 + 16, cy + 130, col_w - 32, 52, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(x3 + col_w / 2, cy + 148, "白天暴晒｜紧闭气孔防失水", size=10.3, color=ORANGE, anchor="middle", weight="700"))
        els.append(txt(x3 + col_w / 2, cy + 165, "液泡放 CO₂ + 光反应跑卡尔文循环", size=9.8, color=INK, anchor="middle", weight="600"))

        els.append(txt(x3 + 16, cy + 204, "• 时间换生存：同一细胞分夜班囤货", size=10.2, color=BODY))
        els.append(txt(x3 + 16, cy + 221, "  与白班造糖，水分利用效率冠绝陆地", size=10.2, color=PURPLE, weight="600"))
        els.append(txt(x3 + 16, cy + 241, "• 代价：受液泡储酸容量上限约束，", size=10.2, color=BODY))
        els.append(txt(x3 + 16, cy + 258, "  总体生长较慢，专精荒漠与附生。", size=10.2, color=BODY))

        svg = figure(
            446,
            "Rubisco酶动力学瓶颈与C3、C4空间双室增压、CAM昼夜错峰储碳机制对比图",
            "顶部概述Rubisco低周转率（每秒约3-10个分子）与O2竞争导致光呼吸的演化背景；下方三栏对比C3植物（水稻小麦叶肉细胞直通）、C4植物（玉米甘蔗叶肉PEP羧化酶与维管束鞘细胞空间接力浓缩CO2）及CAM植物（仙人掌菠萝夜间开气孔存苹果酸入液泡、白天闭气孔释放CO2固碳）。",
            els,
        )
        write_svg(PHOTO_DIR, "c3-c4-cam-pumps.svg", svg)

    @register("earth-life", "地球宜居辐射平衡、硅酸盐风化恒温器、水碳分子化学与内共生跃迁图解", "science_tech")
    def build_earth_life():
        _build_venus_earth_mars_energy()
        _build_silicate_weathering_thermostat()
        _build_water_ice_carbon_silicon()
        _build_endosymbiosis_leap()

    @register("photo-science", "光合作用百年实验史、叶绿素吸收光谱、Z字形电位阶梯与C3/C4/CAM浓缩泵图解", "science_tech")
    def build_photo_science():
        _build_helmont_engelmann_ruben()
        _build_chlorophyll_spectrum_autumn()
        _build_z_scheme_redox()
        _build_c3_c4_cam_pumps()


_register_earth_and_photo()


def _register_resp_and_comp():
    import math

    from .core import (
        BLUE,
        BLUE_LINE,
        BLUE_SOFT,
        BODY,
        BORDER,
        CARD_BG,
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

    RED = "#b91c1c"

    RED_SOFT = "#fef2f2"

    AMBER = "#b45309"

    AMBER_SOFT = "#fffbeb"

    def _build_bonfire_vs_staircase():
        """SVG 1: 1-step combustion (-2870 kJ/mol) vs enzymatic staircase + fat-loss mass balance."""
        dg_total = 2870.0  # kJ/mol released on complete glucose oxidation
        atp_count = 32
        dg_atp_std = 30.5  # kJ/mol standard state
        std_eff = (atp_count * dg_atp_std) / dg_total
        assert 0.335 < std_eff < 0.345

        # Meerman & Brown (2014, BMJ 349:g7257): C55H104O6 + 78 O2 -> 55 CO2 + 52 H2O
        m_c, m_h, m_o = 12.011, 1.008, 15.999
        mw_fat = 55 * m_c + 104 * m_h + 6 * m_o
        mw_o2 = 78 * (2 * m_o)
        mw_co2 = 55 * (m_c + 2 * m_o)
        mw_h2o = 52 * (2 * m_h + m_o)

        # Atom & mass conservation checks
        assert 55 == 55 and 104 == 52 * 2 and (6 + 78 * 2) == (55 * 2 + 52)
        assert math.isclose(mw_fat + mw_o2, mw_co2 + mw_h2o, rel_tol=1e-9)

        fat_kg = 10.0
        o2_kg = fat_kg * mw_o2 / mw_fat
        co2_kg = fat_kg * mw_co2 / mw_fat
        h2o_kg = fat_kg * mw_h2o / mw_fat
        assert 28.9 < o2_kg < 29.1 and 28.0 < co2_kg < 28.2 and 10.8 < h2o_kg < 11.0

        # Partition of the 10 kg fat's own atoms (4 of 6 O atoms to CO2, 2 of 6 O atoms to H2O)
        fat_to_co2_frac = (55 * m_c + 4 * m_o) / mw_fat
        fat_to_h2o_frac = (104 * m_h + 2 * m_o) / mw_fat
        assert math.isclose(fat_to_co2_frac + fat_to_h2o_frac, 1.0, abs_tol=1e-9)
        assert 0.840 < fat_to_co2_frac < 0.843  # 84.1% -> 8.4 kg CO2
        assert 0.157 < fat_to_h2o_frac < 0.160  # 15.9% -> 1.6 kg H2O

        els = header(
            "为什么细胞不直接“烧糖”？—— 多步能量阶梯与“减掉 10 kg 脂肪去哪了”",
            "左：ΔG°′ ≈ −2870 kJ/mol 经多步酶促截留为 30–32 ATP；右：Meerman & Brown (2014) 减脂原子去向实算",
        )

        # ---------------- Left Panel: Bonfire vs Enzymatic Staircase ----------------
        els.append(card(20, 62, 362, 372))
        els.append(txt(34, 85, "① 一步篝火暴燃 vs 20+ 步酶促能量阶梯", PANEL_TITLE, INK, weight="700"))
        els.append(txt(34, 104, "起终点相同（C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O），路径决定生死", 10.6, MUTED))

        y_top, y_bot = 136.0, 326.0
        # Top reactant line & bottom product line
        els.append(f'<line x1="36" y1="{y_top}" x2="366" y2="{y_top}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="4 3"/>')
        els.append(txt(38, y_top - 7, "高自由能起点：1 葡萄糖 + 6 O₂ (0 kJ)", 10.5, BLUE, weight="700"))

        els.append(f'<line x1="36" y1="{y_bot}" x2="366" y2="{y_bot}" stroke="{SLATE}" stroke-width="1.5"/>')
        els.append(txt(38, y_bot + 16, "低自由能终点：6 CO₂ + 6 H₂O (ΔG°′ ≈ −2870 kJ/mol)", 10.4, SLATE, weight="700"))

        # Left sub-route: 1-step direct combustion
        cx_burn = 88.0
        els.append(
            f'<line x1="{cx_burn}" y1="{y_top + 4}" x2="{cx_burn}" y2="{y_bot - 8}" '
            f'stroke="{RED}" stroke-width="3.2" marker-end="url(#arr-orange)"/>'
        )
        els.append(card(38, 194, 104, 68, rx=7, fill=RED_SOFT, stroke=RED))
        els.append(txt(90, 213, "体外一步燃烧", 10.8, RED, "middle", weight="700"))
        els.append(txt(90, 231, "100% 化作热与光", 10.3, BODY, "middle"))
        els.append(txt(90, 248, "0 ATP（烫熟细胞）", 10.3, RED, "middle", weight="700"))

        # Divider between sub-routes
        els.append(f'<line x1="154" y1="142" x2="154" y2="320" stroke="{BORDER}" stroke-width="1"/>')

        # Right sub-route: Computed 10-step enzymatic staircase from (166, y_top) to (356, y_bot)
        step_fracs = [0.06, 0.12, 0.19, 0.27, 0.36, 0.48, 0.61, 0.74, 0.87, 1.00]
        sx0, sx1 = 166.0, 356.0
        n_st = len(step_fracs)
        dx = (sx1 - sx0) / n_st
        stair_pts = [f"M{sx0:.1f},{y_top:.1f}"]
        cur_x = sx0
        atp_marks = []
        for idx, frac in enumerate(step_fracs):
            ny = y_top + frac * (y_bot - y_top)
            nx = cur_x + dx
            stair_pts.append(f"V{ny:.1f} H{nx:.1f}")
            if idx in (1, 4, 6, 8):
                atp_marks.append((cur_x + dx * 0.5, ny))
            cur_x = nx
        els.append(f'<path d="{" ".join(stair_pts)}" fill="none" stroke="{GREEN}" stroke-width="2.4"/>')

        for mx, my in atp_marks:
            els.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3.4" fill="{GREEN}"/>')

        els.append(card(206, 148, 158, 56, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(285, 167, "体内 20+ 步酶促温和阶梯", 10.8, GREEN, "middle", weight="700"))
        els.append(txt(285, 184, "截留 ~34%–40% → 30–32 ATP", 10.3, BODY, "middle", weight="600"))
        els.append(txt(285, 198, "余 ~60% 温和散热维持 37°C", 10.2, MUTED, "middle"))

        els.append(txt(166, 286, "糖酵解 → 柠檬酸循环", 10.2, GREEN, weight="600"))
        els.append(txt(166, 302, "→ 呼吸链多级传递", 10.2, GREEN, weight="600"))

        # Daily ATP turnover callout at bottom of left panel
        els.append(card(34, 354, 334, 66, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(46, 373, "惊人的周转账：全身仅存 ~50–100 g ATP，日产却等同体重！", 10.7, BLUE, weight="700"))
        els.append(txt(46, 391, "成人每日消耗约 2000 kcal，需拆装合成约 50–70 kg ATP；", 10.3, BODY))
        els.append(txt(46, 408, "相当于每一颗 ATP 分子每天被“花掉再充满” 500–1000 次。", 10.3, BODY))

        # ---------------- Right Panel: Where Does 10 kg Fat Go? ----------------
        els.append(card(394, 62, 346, 372))
        els.append(txt(408, 85, "② 减掉 10 kg 脂肪去了哪？（质量守恒账）", PANEL_TITLE, INK, weight="700"))
        els.append(txt(408, 104, "平均人体甘油三酯：C₅₅H₁₀₄O₆ + 78 O₂ → 55 CO₂ + 52 H₂O", 10.5, MUTED))

        # Sub-box A: Total stoichiometry 10 kg fat + 29 kg O2 = 39 kg -> 28 kg CO2 + 11 kg H2O
        els.append(card(408, 118, 318, 96, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(420, 137, "总反应质量账（输入 39 kg = 输出 39 kg）：", 10.8, INK, weight="700"))

        bar_x, bar_w = 420.0, 294.0
        total_mass = fat_kg + o2_kg
        w_fat = bar_w * (fat_kg / total_mass)
        w_o2 = bar_w - w_fat
        els.append(f'<rect x="{bar_x}" y="146" width="{w_fat:.1f}" height="20" rx="3" fill="{ORANGE}"/>')
        els.append(f'<rect x="{bar_x + w_fat:.1f}" y="146" width="{w_o2:.1f}" height="20" rx="3" fill="{BLUE}"/>')
        els.append(txt(bar_x + w_fat / 2, 160, "脂肪 10kg", 10.1, "#ffffff", "middle", weight="700"))
        els.append(txt(bar_x + w_fat + w_o2 / 2, 160, f"吸入 O₂ {o2_kg:.0f}kg", 10.2, "#ffffff", "middle", weight="700"))

        w_co2 = bar_w * (co2_kg / total_mass)
        w_h2o = bar_w - w_co2
        els.append(f'<rect x="{bar_x}" y="180" width="{w_co2:.1f}" height="20" rx="3" fill="{PURPLE}"/>')
        els.append(f'<rect x="{bar_x + w_co2:.1f}" y="180" width="{w_h2o:.1f}" height="20" rx="3" fill="{GREEN}"/>')
        els.append(txt(bar_x + w_co2 / 2, 194, f"呼出 CO₂ {co2_kg:.0f}kg", 10.2, "#ffffff", "middle", weight="700"))
        els.append(txt(bar_x + w_co2 + w_h2o / 2, 194, f"水 {h2o_kg:.0f}kg", 10.1, "#ffffff", "middle", weight="700"))
        els.append(txt(567, 176, "↓ 经线粒体氧化重组 ↓", 9.8, MUTED, "middle"))

        # Sub-box B: Tracing ONLY the 10 kg of fat atoms (84% CO2 via lungs, 16% H2O)
        els.append(card(408, 226, 318, 114, rx=8, fill="#ffffff", stroke=BLUE))
        els.append(txt(420, 246, "单追那 10.0 kg 脂肪自身原子的最终去向：", 10.9, BLUE, weight="700"))

        w_f_co2 = bar_w * fat_to_co2_frac
        w_f_h2o = bar_w - w_f_co2
        els.append(f'<rect x="{bar_x}" y="258" width="{w_f_co2:.1f}" height="26" rx="4" fill="{BLUE}"/>')
        els.append(f'<rect x="{bar_x + w_f_co2:.1f}" y="258" width="{w_f_h2o:.1f}" height="26" rx="4" fill="{GREEN}"/>')
        els.append(txt(bar_x + w_f_co2 / 2, 275, "84%（8.4 kg）变成 CO₂", 10.8, "#ffffff", "middle", weight="700"))
        els.append(txt(bar_x + w_f_co2 + w_f_h2o / 2, 275, "16%", 10.4, "#ffffff", "middle", weight="700"))

        els.append(txt(420, 305, "• 8.4 kg（84%）：由肺部随每一次呼气排入空气！", 10.5, BLUE, weight="700"))
        els.append(txt(420, 324, "• 1.6 kg（16%）：变成 H₂O，随尿液、汗液、呼吸等排出。", 10.5, GREEN, weight="600"))

        # Sub-box C: Misconception warning
        els.append(card(408, 354, 318, 66, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(420, 373, "两个必破误区（超半数受访专业人士曾答错）：", 10.7, ORANGE, weight="700"))
        els.append(txt(420, 391, "1. 肉不会“直接变成热量消失”（化学反应原子质量守恒）；", 10.2, BODY))
        els.append(txt(420, 408, "2. 原地猛喘气不减肥——必须靠运动/基础代谢先拆开脂肪！", 10.2, BODY))

        return figure(
            448,
            "葡萄糖多步酶促自由能阶梯与10千克脂肪氧化去向质量守恒图",
            "左图对比葡萄糖体外一步燃烧释放2870千焦每摩尔全部化作热光与体内20余步酶促反应捕获30至32颗ATP并说明每日50至70千克ATP周转；右图按Meerman与Brown 2014年化学计量算清10千克脂肪加29千克氧气生成28千克二氧化碳和11千克水，其中脂肪自身质量84%经肺呼出、16%成水排出。",
            els,
        )

    def _build_atp_synthase_rotary():
        """SVG 2: F0F1-ATP synthase rotary turbine + 120° binding-change wheel + UCP1 shunt."""
        step_deg = 360.0 / 3.0
        assert math.isclose(step_deg, 120.0)
        # Mammalian c8 ring: 8 H+ per 360° turn -> 8/3 ≈ 2.67 H+ per ATP (plus ~1 H+ Pi/ADP transport ≈ 3.67)
        h_per_atp_catalytic = 8.0 / 3.0
        assert 2.66 < h_per_atp_catalytic < 2.68

        els = header(
            "自然界最小的旋转水轮机：F₀F₁-ATP 合酶的 120° 步进催化与棕色脂肪产热旁路",
            "左：跨膜 H⁺ 驱动 c 环与 γ 轴旋转；右上：Boyer 结合变化机制与 1997 荧光实拍；右下：UCP1 御寒分流",
        )

        # ---------------- Left Panel: Cross-section of F0F1-ATP Synthase ----------------
        els.append(card(20, 62, 412, 380))
        els.append(txt(34, 85, "① F₀F₁-ATP 合酶纵切示意（高约 20 nm，转速可达 ~100+ 圈/秒）", PANEL_TITLE, INK, weight="700"))

        # Top Compartment: Intermembrane Space (high [H+])
        els.append(card(34, 98, 384, 52, rx=7, fill=ORANGE_SOFT, stroke="#fdba74"))
        els.append(txt(46, 118, "线粒体膜间隙（高 H⁺ 浓度 · 正电势侧）", 10.8, ORANGE, weight="700"))
        els.append(txt(46, 136, "呼吸链复合体 I、III、IV 持续泵入质子，蓄起质子动力势", 10.2, MUTED))
        for hx in (312, 344, 376, 400):
            els.append(f'<circle cx="{hx}" cy="118" r="8.5" fill="#ffffff" stroke="{ORANGE}" stroke-width="1.2"/>')
            els.append(txt(hx, 122, "H⁺", 9.6, ORANGE, "middle", weight="700"))

        # Middle Band: Inner Mitochondrial Membrane (y=156..216)
        mem_y1, mem_y2 = 156.0, 216.0
        els.append(f'<rect x="34" y="{mem_y1}" width="384" height="60" rx="4" fill="#f8fafc" stroke="{HAIRLINE}"/>')
        # Draw phospholipid head dots on left and right flanking regions
        for lx in range(44, 114, 14):
            els.append(f'<circle cx="{lx}" cy="{mem_y1 + 6}" r="4.2" fill="#94a3b8"/>')
            els.append(f'<circle cx="{lx}" cy="{mem_y2 - 6}" r="4.2" fill="#94a3b8"/>')
            els.append(f'<line x1="{lx}" y1="{mem_y1 + 10}" x2="{lx}" y2="{mem_y2 - 10}" stroke="#cbd5e1" stroke-width="1.2"/>')
        for rx in range(324, 412, 14):
            els.append(f'<circle cx="{rx}" cy="{mem_y1 + 6}" r="4.2" fill="#94a3b8"/>')
            els.append(f'<circle cx="{rx}" cy="{mem_y2 - 6}" r="4.2" fill="#94a3b8"/>')
            els.append(f'<line x1="{rx}" y1="{mem_y1 + 10}" x2="{rx}" y2="{mem_y2 - 10}" stroke="#cbd5e1" stroke-width="1.2"/>')
        els.append(txt(42, 190, "线粒体", 10.1, SLATE, weight="600", halo=True))
        els.append(txt(42, 204, "内膜", 10.1, SLATE, weight="600", halo=True))

        # Subunit a (stator proton half-channels, x=118..168)
        els.append(card(118, 152, 50, 68, rx=8, fill=SLATE_SOFT, stroke=SLATE, sw=1.4))
        els.append(txt(143, 183, "a 亚基", 10.5, SLATE, "middle", weight="700"))
        els.append(txt(143, 198, "半通道", 9.8, MUTED, "middle"))

        # F0 c-ring rotor (x=172..268, y=150..222)
        els.append(card(172, 150, 96, 72, rx=12, fill=BLUE_SOFT, stroke=BLUE, sw=1.8))
        for cx_sub in (186, 206, 226, 246):
            els.append(f'<rect x="{cx_sub - 7}" y="156" width="14" height="60" rx="5" fill="#bfdbfe" stroke="{BLUE}" stroke-width="1"/>')
        els.append(txt(220, 184, "F₀ 转子 c 环", 10.8, BLUE, "middle", weight="700", halo=True))
        els.append(txt(220, 200, "(c₈–c₁₅ 旋转鼓)", 9.8, BLUE, "middle", weight="600", halo=True))

        # H+ entry -> ride c-ring -> exit into matrix path
        els.append(
            f'<path d="M142,138 V174 H182" fill="none" stroke="{ORANGE}" stroke-width="2.0" marker-end="url(#arr-orange)"/>'
        )
        els.append(
            f'<path d="M164,200 V242" fill="none" stroke="{ORANGE}" stroke-width="2.0" marker-end="url(#arr-orange)"/>'
        )
        els.append(txt(126, 254, "H⁺ 顺梯度入基质", 10.2, ORANGE, "middle", weight="700"))

        # Peripheral stator stalk b2 + OSCP (x=284..306, clamping F1 head!)
        els.append(f'<path d="M168,164 H295 V322 H280" fill="none" stroke="{SLATE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" opacity="0.28"/>')
        els.append(f'<path d="M168,164 H295 V322 H280" fill="none" stroke="{SLATE}" stroke-width="2.0" stroke-linejoin="round"/>')
        els.append(txt(354, 256, "外周静子柄 (b₂)", 10.4, SLATE, "middle", weight="700"))
        els.append(txt(354, 272, "锁住 α₃β₃ 防跟转", 10.0, MUTED, "middle"))

        # Central asymmetric gamma shaft (x=208..232, y=222..326)
        els.append(f'<polygon points="210,222 230,222 235,318 214,328" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.8"/>')
        els.append(txt(221, 260, "γ轴", 10.5, PURPLE, "middle", weight="700"))
        # Rotation arrow around shaft
        els.append(
            f'<path d="M196,242 Q220,252 244,242" fill="none" stroke="{PURPLE}" stroke-width="2.0" marker-end="url(#arr-blue)"/>'
        )

        # F1 alpha3-beta3 catalytic head (y=282..366)
        els.append(card(146, 284, 58, 78, rx=16, fill=GREEN_SOFT, stroke=GREEN, sw=1.6))
        els.append(card(236, 284, 58, 78, rx=16, fill=GREEN_SOFT, stroke=GREEN, sw=1.6))
        els.append(card(192, 296, 56, 72, rx=14, fill="#dcfce7", stroke=GREEN, sw=1.8))
        els.append(txt(175, 322, "β 催化", 10.4, GREEN, "middle", weight="700"))
        els.append(txt(175, 338, "亚基", 10.2, GREEN, "middle"))
        els.append(txt(220, 336, "F₁ 头", 10.8, INK, "middle", weight="700"))
        els.append(txt(220, 352, "(α₃β₃)", 10.0, GREEN, "middle", weight="700"))
        els.append(txt(265, 322, "α 结构", 10.4, SLATE, "middle", weight="700"))
        els.append(txt(265, 338, "亚基", 10.2, SLATE, "middle"))

        # ADP + Pi -> ATP reaction arrows at F1 head
        els.append(txt(80, 316, "ADP + Pi", 10.6, BODY, "middle", weight="700"))
        els.append(f'<path d="M112,314 H142" fill="none" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#arr-green)"/>')
        els.append(f'<path d="M298,342 H334" fill="none" stroke="{GREEN}" stroke-width="2.0" marker-end="url(#arr-green)"/>')
        els.append(pill(338, 330, "ATP!", fg=GREEN, bg=GREEN_SOFT, w=58, h=22, size=11.0))

        # Bottom Matrix summary inside Left Panel
        els.append(txt(44, 392, "线粒体基质（低 H⁺ 浓度侧）：γ 凸轮每转 360° 顶开 3 个 β 亚基 → 产 3 颗 ATP", 10.4, INK, weight="600"))
        els.append(txt(44, 412, "1974 年 Racker 与 Stoeckenius 将细菌紫膜质子泵与牛 ATP 合酶装入人造脂泡，", 10.2, MUTED))
        els.append(txt(44, 428, "在无呼吸链条件下靠光照造出 ATP，一锤定音证实 Mitchell 化学渗透学说！", 10.2, MUTED))

        # ---------------- Top-Right Panel: Top-Down 120° Binding Change & Actin Proof ----------------
        els.append(card(444, 62, 296, 198))
        els.append(txt(458, 85, "② 俯视 α₃β₃：120° 步进与单分子实拍", PANEL_TITLE, INK, weight="700"))

        wcx, wcy = 508.0, 166.0
        subunits = [
            (90, "β-O", GREEN, GREEN_SOFT),
            (30, "α", SLATE, SLATE_SOFT),
            (-30, "β-L", BLUE, BLUE_SOFT),
            (-90, "α", SLATE, SLATE_SOFT),
            (-150, "β-T", ORANGE, ORANGE_SOFT),
            (150, "α", SLATE, SLATE_SOFT),
        ]
        for ang, sym, scol, sbg in subunits:
            rad = math.radians(ang)
            sx = wcx + 32.0 * math.cos(rad)
            sy = wcy - 32.0 * math.sin(rad)
            r_s = 15.5 if sym.startswith("β") else 12.5
            els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r_s}" fill="{sbg}" stroke="{scol}" stroke-width="1.5"/>')
            els.append(txt(sx, sy + 3.8, sym, 9.8, scol, "middle", weight="700"))

        # Central asymmetric gamma cam + fluorescent actin filament (Noji et al. 1997)
        els.append(f'<polygon points="{wcx},{wcy - 13} {wcx + 9},{wcy + 8} {wcx - 9},{wcy + 8}" fill="{PURPLE}" opacity="0.9"/>')
        els.append(txt(wcx, wcy + 4.5, "γ", 9.6, "#ffffff", "middle", weight="700"))
        # Fluorescent actin rod attached to gamma pointing up-left to avoid right text column completely
        els.append(f'<line x1="{wcx}" y1="{wcy - 9}" x2="{wcx - 44}" y2="{wcy - 48}" stroke="#e11d48" stroke-width="3.0" stroke-linecap="round"/>')
        els.append(
            f'<path d="M{wcx - 38},{wcy - 44} A52,52 0 0,1 {wcx + 34},{wcy - 44}" '
            f'fill="none" stroke="#e11d48" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#arr-orange)"/>'
        )
        els.append(txt(wcx, wcy - 55, "120° 步进旋转", 9.8, "#be123c", "middle", weight="700"))

        els.append(txt(578, 114, "Boyer 三态交替：", 10.4, INK, weight="700"))
        els.append(txt(578, 131, "• 耗能关键在顶开 β 释放", 9.9, BODY))
        els.append(txt(578, 147, "  紧绑的 ATP，而非成键！", 9.9, GREEN, weight="700"))
        els.append(txt(578, 172, "1997 吉田贤右 / 野地博行：", 10.2, "#be123c", weight="700"))
        els.append(txt(578, 189, "在 γ 轴粘上 ~1 μm 荧光", 9.9, BODY))
        els.append(txt(578, 205, "肌动蛋白棒，显微镜下亲眼", 9.9, BODY))
        els.append(txt(578, 221, "拍到 120° 分步旋转！", 9.9, "#be123c", weight="700"))
        els.append(txt(458, 247, "注：分离的 F₁ 水解 ATP 可反转；完整合酶顺质子流造 ATP", 9.8, MUTED))

        # ---------------- Bottom-Right Panel: Brown Fat UCP1 Thermogenic Shunt ----------------
        els.append(card(444, 272, 296, 170))
        els.append(txt(458, 295, "③ 棕色脂肪“可控漏电”：UCP1 御寒暖气阀", PANEL_TITLE, INK, weight="700"))

        # Schematic mini-membrane comparing ATP synthase vs UCP1
        els.append(card(458, 310, 268, 62, rx=7, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(470, 329, "常规路线：H⁺ → ATP 合酶 → 势能存进 ATP", 10.4, BLUE, weight="600"))
        els.append(txt(470, 350, "御寒旁路：H⁺ → 解偶联蛋白 UCP1（产热素）", 10.5, ORANGE, weight="700"))
        els.append(txt(470, 366, "          绕开合酶直返基质 → 100% 化作体温！", 10.4, RED, weight="700"))

        els.append(txt(458, 392, "• 新生婴儿不会打寒颤，颈背部富含棕色脂肪保命；", 10.2, BODY))
        els.append(txt(458, 410, "• 冬眠熊/旱獭靠 UCP1 非战栗产热苏醒；因富含含铁", 10.2, BODY))
        els.append(txt(458, 427, "  细胞色素的密集线粒体，组织肉眼呈棕褐色。", 10.2, MUTED))

        return figure(
            456,
            "F0F1-ATP合酶纳米分子水轮机纵切结构与120度步进催化及UCP1产热旁路图",
            "左图展示线粒体膜间隙质子顺电化学梯度经a亚基半通道驱动F0转子c环与中央不对称γ轴旋转，在外周静子柄b2固定下顶开F1头α3β3亚基每圈合成3颗ATP；右上俯视图展示Boyer三态循环与1997年荧光肌动蛋白丝120度步进实拍；右下展示棕色脂肪UCP1质子分流非战栗产热机制。",
            els,
        )

    def _build_sprint_vs_marathon_fuel():
        """SVG 3: Computed Gastin (2001) three-system relative energy contribution curves."""
        def _shares(t_sec):
            # Smooth continuous physiological model calibrated to Gastin (2001, Sports Med 31:725-741)
            w_pcr = 96.0 * math.exp(-t_sec / 13.5) + 2.0 * math.exp(-t_sec / 130.0)
            w_gly = 62.0 * (1.0 - math.exp(-((t_sec / 7.5) ** 1.3))) * math.exp(-t_sec / 92.0) + 0.8 * math.exp(
                -t_sec / 2500.0
            )
            w_aer = 2.4 + 36.2 * (1.0 - math.exp(-t_sec / 52.0))
            tot = w_pcr + w_gly + w_aer
            return (100.0 * w_pcr / tot, 100.0 * w_gly / tot, 100.0 * w_aer / tot)

        # Critical physiological assertions against Gastin (2001) benchmarks
        s2 = _shares(2.0)
        s10 = _shares(10.0)
        s30 = _shares(30.0)
        s75 = _shares(75.0)
        s7200 = _shares(7200.0)
        assert s2[0] > 80.0 and s2[2] < 6.0
        assert 44.0 < s10[0] < 54.0 and 38.0 < s10[1] < 46.0 and 7.0 < s10[2] < 12.0
        assert s30[1] > s30[0] and s30[1] > s30[2]  # Glycolysis peaks around 20–45s
        assert 48.0 < s75[2] < 52.0  # ~75s equal aerobic/anaerobic crossover!
        assert s7200[2] > 99.0

        # Find exact 50% aerobic crossover time via bisection
        lo, hi = 50.0, 110.0
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            if _shares(mid)[2] < 50.0:
                lo = mid
            else:
                hi = mid
        t_cross = 0.5 * (lo + hi)
        assert 70.0 <= t_cross <= 80.0

        els = header(
            "从 10 秒飞人到 2 小时马拉松：人体三大供能系统的平滑接力曲线",
            "实测表明三套系统在起跑第 1 秒便同时启动，并非“先耗尽前一个才开后一个”；约 75 秒处有氧追平无氧",
        )

        els.append(card(20, 62, 720, 250))
        els.append(
            txt(
                36,
                85,
                "① 全力运动持续时间 vs 瞬时供能相对占比（%，对数时间轴 1 秒 → 2 小时，据 Gastin 2001 模型）",
                PANEL_TITLE,
                INK,
                weight="700",
            )
        )

        gx, gy, gw, gh = 68.0, 266.0, 644.0, 154.0
        log_min, log_max = 0.0, math.log10(7200.0)

        def _tx(t_s):
            return gx + ((math.log10(t_s) - log_min) / (log_max - log_min)) * gw

        def _ty(pct):
            return gy - (pct / 100.0) * gh

        # Horizontal percentage gridlines
        for pct in (0, 25, 50, 75, 100):
            py = _ty(pct)
            is_50 = pct == 50
            scol = "#cbd5e1" if is_50 else SLATE_SOFT
            dash = ' stroke-dasharray="4 3"' if is_50 else ""
            els.append(f'<line x1="{gx}" y1="{py:.1f}" x2="{gx + gw}" y2="{py:.1f}" stroke="{scol}" stroke-width="1.1"{dash}/>')
            els.append(txt(gx - 8, py + 4, f"{pct}%", 10.4, MUTED, "end"))

        # X-axis time ticks & sport benchmarks
        ticks = [
            (1, "1s"),
            (3, "3s"),
            (10, "10s(百米)"),
            (30, "30s(400m)"),
            (75, "75s(800m)"),
            (240, "4min(1500m)"),
            (1200, "20min"),
            (7200, "2h(马拉松)"),
        ]
        for t_val, t_lbl in ticks:
            px = _tx(t_val)
            els.append(f'<line x1="{px:.1f}" y1="{gy - gh}" x2="{px:.1f}" y2="{gy}" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(px, gy + 17, t_lbl, 10.2, INK if t_val in (10, 75, 7200) else MUTED, "middle", weight="700" if t_val in (10, 75, 7200) else None))

        els.append(f'<path d="M{gx},{gy - gh} V{gy} H{gx + gw}" fill="none" stroke="#94a3b8" stroke-width="1.3"/>')

        # Sample 140 log-spaced points and assert exact 100% sum everywhere
        n_pts = 140
        pts_pcr, pts_gly, pts_aer = [], [], []
        for i in range(n_pts + 1):
            lv = log_min + (log_max - log_min) * (i / n_pts)
            tv = 10.0 ** lv
            p1, p2, p3 = _shares(tv)
            assert math.isclose(p1 + p2 + p3, 100.0, abs_tol=1e-9)
            px = _tx(tv)
            pts_pcr.append((px, _ty(p1)))
            pts_gly.append((px, _ty(p2)))
            pts_aer.append((px, _ty(p3)))

        def _to_path(pts):
            return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

        # Curves with distinct colors + stroke patterns for colorblind accessibility
        els.append(f'<path d="{_to_path(pts_pcr)}" fill="none" stroke="{ORANGE}" stroke-width="2.7"/>')
        els.append(f'<path d="{_to_path(pts_gly)}" fill="none" stroke="{PURPLE}" stroke-width="2.5" stroke-dasharray="7 4"/>')
        els.append(f'<path d="{_to_path(pts_aer)}" fill="none" stroke="{BLUE}" stroke-width="2.8"/>')

        # Highlight 75s 50%-50% crossover point
        cx_75, cy_50 = _tx(t_cross), _ty(50.0)
        els.append(f'<line x1="{cx_75:.1f}" y1="{gy - gh}" x2="{cx_75:.1f}" y2="{gy}" stroke="{GREEN}" stroke-width="1.4" stroke-dasharray="4 3"/>')
        els.append(f'<circle cx="{cx_75:.1f}" cy="{cy_50:.1f}" r="5.2" fill="{GREEN}" stroke="#ffffff" stroke-width="1.5"/>')
        els.append(txt(cx_75 + 8, cy_50 - 7, f"≈{t_cross:.0f}s 交叉点：有氧 50% = 无氧合 50%", 10.5, GREEN, "start", weight="700", halo=True))

        # Direct curve labels placed in clean open regions
        els.append(txt(_tx(2.2), _ty(85), "① 磷酸原 (ATP-PCr，实线)", 10.8, ORANGE, "start", weight="700", halo=True))
        els.append(txt(_tx(28), _ty(70), "② 无氧糖酵解 (虚线)", 10.8, PURPLE, "middle", weight="700", halo=True))
        els.append(txt(_tx(900), _ty(91), "③ 有氧氧化磷酸化 (实线，长跑 >98%)", 10.8, BLUE, "middle", weight="700", halo=True))

        els.append(txt(36, 300, "注：纵轴为各时刻瞬时功率占比（三曲线之和恒为 100%）；个体训练水平与配速会使交叉点在 60–90 秒间微移。", 10.2, MUTED))

        # ---------------- Bottom 3 Summary Cards ----------------
        cards_info = [
            (
                20,
                "① 磷酸原系统（0–10 秒霸主）",
                ORANGE,
                ORANGE_SOFT,
                "磷酸肌酸一步把磷酸基交给 ADP，",
                "无需氧气、功率最高，但库存仅够",
                "博尔特百米冲刺或举重抓举数秒。",
            ),
            (
                266,
                "② 无氧糖酵解（10–90 秒峰值）",
                PURPLE,
                PURPLE_SOFT,
                "每分子葡萄糖快产 2 ATP，靠丙酮",
                "酸变乳酸再生 NAD⁺；乳酸可被心肝",
                "回收利用，并非次日肌肉酸痛元凶。",
            ),
            (
                512,
                "③ 有氧呼吸（>75 秒绝对主力）",
                BLUE,
                BLUE_SOFT,
                "线粒体动用糖原与脂肪彻底氧化，",
                "单分子糖产 30–32 ATP、脂肪更高；",
                "功率受摄氧量限制，却能续航数小时。",
            ),
        ]
        for cx_c, ctitle, ccol, cbg, l1, l2, l3 in cards_info:
            els.append(card(cx_c, 324, 228, 96, rx=8, fill=cbg, stroke=ccol))
            els.append(txt(cx_c + 12, 344, ctitle, 11.0, ccol, weight="700"))
            els.append(txt(cx_c + 12, 365, l1, 10.3, BODY))
            els.append(txt(cx_c + 12, 383, l2, 10.3, BODY))
            els.append(txt(cx_c + 12, 401, l3, 10.3, BODY))

        return figure(
            432,
            "人体三大供能系统随全力运动时间变化的瞬时功率贡献曲线图",
            "基于Gastin 2001运动生理学模型在对数时间轴上绘出1秒至2小时内磷酸原系统、无氧糖酵解与有氧氧化磷酸化的相对供能占比，三曲线之和恒为100%，并在约75秒处标出有氧与无氧各占50%的交叉点。",
            els,
        )

    @register("resp-motor", "细胞呼吸与生物能量：多步自由能阶梯、减脂碳氧去向、ATP合酶旋转涡轮与运动供能曲线", "science_tech")
    def build_resp_motor():
        write_svg("resp-motor", "bonfire-vs-staircase.svg", _build_bonfire_vs_staircase())
        write_svg("resp-motor", "atp-synthase-rotary.svg", _build_atp_synthase_rotary())
        write_svg("resp-motor", "sprint-vs-marathon-fuel.svg", _build_sprint_vs_marathon_fuel())

    def _build_shannon_switches_to_gates():
        """SVG 1: Claude Shannon's 1937 bridge: Series=AND, Parallel=OR, Complementary=NOT + Universal NAND."""
        def _nand(a, b):
            return 1 - (a & b)

        # Verify functional completeness of NAND across all Boolean inputs
        for a in (0, 1):
            assert _nand(a, a) == (1 - a)  # NOT
            for b in (0, 1):
                not_nand = _nand(_nand(a, b), _nand(a, b))
                assert not_nand == (a & b)  # AND
                de_morgan_or = _nand(_nand(a, a), _nand(b, b))
                assert de_morgan_or == (a | b)  # OR
                t1 = _nand(a, b)
                xor_4nand = _nand(_nand(a, t1), _nand(b, t1))
                assert xor_4nand == (a ^ b)  # XOR from 4 NANDs!

        els = header(
            "香农 1937 硕士论文的破壁一跃：笨电流如何靠开关连接“学会逻辑”？",
            "把布尔代数 (1854) 变成电路拓扑：串联=与(AND)，并联=或(OR)，互补拉高拉低=非(NOT)，万用积木=与非门(NAND)",
        )

        # ---------------- Column 1: Series Switches = AND ----------------
        els.append(card(20, 62, 232, 266))
        els.append(txt(34, 85, "① 串联开关 = 与门 (AND)", PANEL_TITLE, BLUE, weight="700"))
        els.append(txt(34, 103, "两道桥都放下，电流才能过河", 10.4, MUTED))

        # Schematic box
        els.append(card(32, 112, 208, 86, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        wy = 156.0
        els.append(txt(40, wy - 14, "+V(1)", 9.8, BLUE, weight="700", cls="mono"))
        els.append(f'<line x1="42" y1="{wy}" x2="78" y2="{wy}" stroke="{BLUE}" stroke-width="2.2"/>')
        # Switch A
        els.append(f'<circle cx="78" cy="{wy}" r="3" fill="{BLUE}"/>')
        els.append(f'<line x1="78" y1="{wy}" x2="106" y2="{wy - 14}" stroke="{ORANGE}" stroke-width="2.2"/>')
        els.append(f'<circle cx="110" cy="{wy}" r="3" fill="{BLUE}"/>')
        els.append(txt(94, wy - 20, "开关 A", 10.2, ORANGE, "middle", weight="700"))
        els.append(f'<line x1="110" y1="{wy}" x2="136" y2="{wy}" stroke="{BLUE}" stroke-width="2.2"/>')
        # Switch B
        els.append(f'<circle cx="136" cy="{wy}" r="3" fill="{BLUE}"/>')
        els.append(f'<line x1="136" y1="{wy}" x2="164" y2="{wy - 14}" stroke="{ORANGE}" stroke-width="2.2"/>')
        els.append(f'<circle cx="168" cy="{wy}" r="3" fill="{BLUE}"/>')
        els.append(txt(152, wy - 20, "开关 B", 10.2, ORANGE, "middle", weight="700"))
        els.append(f'<line x1="168" y1="{wy}" x2="206" y2="{wy}" stroke="{BLUE}" stroke-width="2.2"/>')
        els.append(f'<circle cx="214" cy="{wy}" r="9" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
        els.append(txt(214, wy + 4, "Y", 10.4, BLUE, "middle", weight="700", cls="mono"))
        els.append(txt(136, 190, "Y = A · B（全 1 才为 1）", 10.2, INK, "middle", weight="600"))

        # Truth table for AND
        els.append(txt(56, 216, "A", 10.4, MUTED, "middle", weight="700", cls="mono"))
        els.append(txt(116, 216, "B", 10.4, MUTED, "middle", weight="700", cls="mono"))
        els.append(txt(190, 216, "输出 Y", 10.4, BLUE, "middle", weight="700"))
        for idx, (a, b) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            ry = 224 + idx * 23
            y_out = a & b
            if y_out:
                els.append(f'<rect x="34" y="{ry}" width="204" height="20" rx="4" fill="{BLUE_SOFT}"/>')
            els.append(txt(56, ry + 14, str(a), 10.6, BODY, "middle", cls="mono"))
            els.append(txt(116, ry + 14, str(b), 10.6, BODY, "middle", cls="mono"))
            els.append(txt(190, ry + 14, str(y_out), 10.8, BLUE if y_out else MUTED, "middle", weight="700", cls="mono"))

        # ---------------- Column 2: Parallel Switches = OR ----------------
        els.append(card(264, 62, 232, 266))
        els.append(txt(278, 85, "② 并联开关 = 或门 (OR)", PANEL_TITLE, GREEN, weight="700"))
        els.append(txt(278, 103, "上下任通一路，信号即可抵达", 10.4, MUTED))

        els.append(card(276, 112, 208, 86, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(284, 152, "+V", 9.8, GREEN, weight="700", cls="mono"))
        els.append(f'<line x1="298" y1="154" x2="318" y2="154" stroke="{GREEN}" stroke-width="2.2"/>')
        els.append(f'<line x1="318" y1="134" x2="318" y2="174" stroke="{GREEN}" stroke-width="2.0"/>')
        # Top branch A
        els.append(f'<line x1="318" y1="134" x2="346" y2="134" stroke="{GREEN}" stroke-width="2.0"/>')
        els.append(f'<circle cx="346" cy="134" r="2.8" fill="{GREEN}"/>')
        els.append(f'<line x1="346" y1="134" x2="374" y2="123" stroke="{ORANGE}" stroke-width="2.0"/>')
        els.append(f'<circle cx="378" cy="134" r="2.8" fill="{GREEN}"/>')
        els.append(txt(362, 121, "A", 10.0, ORANGE, "middle", weight="700", cls="mono"))
        els.append(f'<line x1="378" y1="134" x2="404" y2="134" stroke="{GREEN}" stroke-width="2.0"/>')
        # Bottom branch B
        els.append(f'<line x1="318" y1="174" x2="346" y2="174" stroke="{GREEN}" stroke-width="2.0"/>')
        els.append(f'<circle cx="346" cy="174" r="2.8" fill="{GREEN}"/>')
        els.append(f'<line x1="346" y1="174" x2="374" y2="163" stroke="{ORANGE}" stroke-width="2.0"/>')
        els.append(f'<circle cx="378" cy="174" r="2.8" fill="{GREEN}"/>')
        els.append(txt(362, 162, "B", 10.0, ORANGE, "middle", weight="700", cls="mono"))
        els.append(f'<line x1="378" y1="174" x2="404" y2="174" stroke="{GREEN}" stroke-width="2.0"/>')
        # Merge to Y
        els.append(f'<line x1="404" y1="134" x2="404" y2="174" stroke="{GREEN}" stroke-width="2.0"/>')
        els.append(f'<line x1="404" y1="154" x2="446" y2="154" stroke="{GREEN}" stroke-width="2.2"/>')
        els.append(f'<circle cx="456" cy="154" r="9" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
        els.append(txt(456, 158, "Y", 10.4, GREEN, "middle", weight="700", cls="mono"))
        els.append(txt(380, 192, "Y = A + B（有 1 即为 1）", 10.2, INK, "middle", weight="600"))

        # Truth table for OR
        els.append(txt(300, 216, "A", 10.4, MUTED, "middle", weight="700", cls="mono"))
        els.append(txt(360, 216, "B", 10.4, MUTED, "middle", weight="700", cls="mono"))
        els.append(txt(434, 216, "输出 Y", 10.4, GREEN, "middle", weight="700"))
        for idx, (a, b) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            ry = 224 + idx * 23
            y_out = a | b
            if y_out:
                els.append(f'<rect x="278" y="{ry}" width="204" height="20" rx="4" fill="{GREEN_SOFT}"/>')
            els.append(txt(300, ry + 14, str(a), 10.6, BODY, "middle", cls="mono"))
            els.append(txt(360, ry + 14, str(b), 10.6, BODY, "middle", cls="mono"))
            els.append(txt(434, ry + 14, str(y_out), 10.8, GREEN if y_out else MUTED, "middle", weight="700", cls="mono"))

        # ---------------- Column 3: Complementary Pull-up/Pull-down = NOT ----------------
        els.append(card(508, 62, 232, 266))
        els.append(txt(522, 85, "③ 互补上下拉 = 非门 (NOT)", PANEL_TITLE, ORANGE, weight="700"))
        els.append(txt(522, 103, "CMOS 反相器：上通下断或上断下通", 10.4, MUTED))

        els.append(card(520, 112, 208, 112, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        # VDD top -> PMOS pull-up -> node Y -> NMOS pull-down -> GND
        els.append(txt(618, 126, "VDD (高电平 1)", 9.8, BLUE, "middle", weight="700", cls="mono"))
        els.append(f'<line x1="618" y1="130" x2="618" y2="144" stroke="{BLUE}" stroke-width="2.0"/>')
        els.append(card(586, 144, 64, 20, rx=4, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(618, 158, "A=0 导通", 9.8, BLUE, "middle", weight="700"))
        els.append(f'<line x1="618" y1="164" x2="618" y2="180" stroke="{INK}" stroke-width="2.0"/>')
        # Output Y tap to right
        els.append(f'<line x1="618" y1="172" x2="684" y2="172" stroke="{ORANGE}" stroke-width="2.2"/>')
        els.append(f'<circle cx="696" cy="172" r="9" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.6"/>')
        els.append(txt(696, 176, "Y", 10.4, ORANGE, "middle", weight="700", cls="mono"))
        # Input A label on left
        els.append(txt(544, 176, "输入 A", 10.2, INK, "start", weight="700"))
        els.append(card(586, 180, 64, 20, rx=4, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(618, 194, "A=1 导通", 9.8, ORANGE, "middle", weight="700"))
        els.append(f'<line x1="618" y1="200" x2="618" y2="210" stroke="{SLATE}" stroke-width="2.0"/>')
        els.append(txt(618, 220, "GND (低电平 0)", 9.8, SLATE, "middle", weight="700", cls="mono"))

        # Truth table for NOT + CMOS low-power note
        els.append(txt(556, 244, "输入 A", 10.4, MUTED, "middle", weight="700"))
        els.append(txt(668, 244, "输出 Y = ¬A", 10.4, ORANGE, "middle", weight="700"))
        for idx, a in enumerate((0, 1)):
            ry = 252 + idx * 24
            y_out = 1 - a
            els.append(f'<rect x="522" y="{ry}" width="204" height="20" rx="4" fill="{ORANGE_SOFT if y_out else SLATE_SOFT}"/>')
            els.append(txt(556, ry + 14, str(a), 10.8, BODY, "middle", weight="700", cls="mono"))
            els.append(txt(668, ry + 14, str(y_out), 10.8, ORANGE if y_out else SLATE, "middle", weight="700", cls="mono"))
        els.append(txt(624, 316, "静态无直通电流，百亿晶体管不烧毁！", 10.0, MUTED, "middle"))

        # ---------------- Bottom Banner: Universal NAND Gate ----------------
        els.append(card(20, 340, 720, 96))
        els.append(txt(36, 363, "④ 万用积木“与非门（NAND）”：只靠一种门，就能拼出世上一切数字电路！", PANEL_TITLE, PURPLE, weight="700"))

        els.append(card(36, 374, 346, 50, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(46, 393, "• NOT(A)=NAND(A,A)   • AND(A,B)=NOT(NAND(A,B))", 10.0, INK, cls="mono"))
        els.append(txt(46, 413, "• OR(A,B)=NAND(NOT(A), NOT(B))（德摩根定律）", 10.1, PURPLE, weight="700"))

        # Mini 4-NAND XOR schematic box on right
        els.append(card(396, 374, 330, 50, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(408, 393, "半加器核心“异或门 XOR”也只需 4 个 NAND 门：", 10.3, BLUE, weight="700"))
        els.append(txt(408, 413, "t = NAND(A,B) → XOR = NAND(NAND(A,t), NAND(B,t))", 9.9, BODY, cls="mono"))

        return figure(
            448,
            "香农1937继电器开关逻辑映射图：串联与门、并联或门、CMOS互补非门与万用与非门",
            "三列电路分别展示两开关串联构成与门AND、两开关并联构成或门OR、上下拉互补开关构成CMOS非门NOT及其完整真值表；底部展示功能完备的与非门NAND如何单独组合出NOT、AND、OR及4门异或XOR。",
            els,
        )

    def _build_twos_complement_rgb():
        """SVG 2: Left 4-bit two's complement clock wheel; Right 24-bit RGB subpixel 16.77M colors."""
        # Verify 4-bit two's complement modular arithmetic: 5 + (-3) = 5 + 13 = 18 ≡ 2 (mod 16)
        pos_5 = 0b0101
        neg_3 = 0b1101  # 16 - 3 = 13
        assert (~0b0011 & 0xF) + 1 == neg_3
        assert (pos_5 + neg_3) & 0xF == 0b0010
        assert (0b1111 + 0b0001) & 0xF == 0b0000

        # Verify 24-bit color & 1080p@60Hz uncompressed frame bandwidth
        n_colors = 256 ** 3
        assert n_colors == 16_777_216
        bytes_per_frame = 1920 * 1080 * 3
        mb_per_sec_60hz = (bytes_per_frame * 60) / 1_000_000.0
        assert math.isclose(mb_per_sec_60hz, 373.248, abs_tol=0.01)

        els = header(
            "比特的两种身份：左用“补码圆盘”把减法变加法，右用“三原色字节”调出 1677 万色",
            "同一串 0 和 1 没有天生含义：按二进制补码解释可省掉减法器；按 24 位 RGB 解释可点亮屏幕像素",
        )

        # ---------------- Left Panel: 4-Bit Two's Complement Wheel ----------------
        els.append(card(20, 62, 366, 380))
        els.append(txt(34, 85, "① 4 位补码时钟轮：为什么 1111 是 −1？", PANEL_TITLE, INK, weight="700"))
        els.append(txt(34, 103, "像里程表满 16 归零：倒退 3 格 ≡ 顺时针往前走 13 格！", 10.4, MUTED))

        # Top corner legend badges cleanly outside the wheel
        els.append(pill(34, 112, "左半 MSB=1 (−8..−1)", fg=ORANGE, bg=ORANGE_SOFT, w=128, h=20, size=9.6))
        els.append(pill(242, 112, "右半 MSB=0 (0..+7)", fg=BLUE, bg=BLUE_SOFT, w=128, h=20, size=9.6))

        wcx, wcy = 202.0, 238.0
        r_ring = 76.0
        els.append(f'<circle cx="{wcx}" cy="{wcy}" r="{r_ring}" fill="#f8fafc" stroke="{BORDER}" stroke-width="1.5"/>')
        els.append(f'<line x1="{wcx}" y1="{wcy - r_ring - 6}" x2="{wcx}" y2="{wcy + r_ring + 6}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3 3"/>')

        for k in range(16):
            ang_deg = 90.0 - k * 22.5
            rad = math.radians(ang_deg)
            signed_v = k if k < 8 else k - 16
            bits = f"{k:04b}"
            is_neg = signed_v < 0
            col = ORANGE if is_neg else BLUE

            px = wcx + r_ring * math.cos(rad)
            py = wcy - r_ring * math.sin(rad)
            r_dot = 4.6 if k in (0, 2, 5, 13, 15) else 3.0
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_dot}" fill="{col}"/>')

            # Outer binary label
            ox = wcx + (r_ring + 24.0) * math.cos(rad)
            oy = wcy - (r_ring + 19.5) * math.sin(rad) + 3.5
            wt = "700" if k in (0, 2, 5, 13, 15) else None
            els.append(txt(ox, oy, bits, 9.6, col, "middle", weight=wt, cls="mono"))

            # Inner signed decimal label
            ix = wcx + (r_ring - 18.0) * math.cos(rad)
            iy = wcy - (r_ring - 18.0) * math.sin(rad) + 3.5
            s_lbl = f"+{signed_v}" if signed_v > 0 else str(signed_v)
            els.append(txt(ix, iy, s_lbl, 9.7, INK if wt else MUTED, "middle", weight=wt))

        # Compact center formula inside wheel (well clear of r_ring - 18 = 58px!)
        els.append(txt(wcx, wcy + 4, "5 − 3 = +2", 10.2, GREEN, "middle", weight="700"))

        # Highlight arc from +5 (k=5, ang=-22.5°) back 3 steps to +2 (k=2, ang=45°)
        a5, a2 = math.radians(90 - 5 * 22.5), math.radians(90 - 2 * 22.5)
        x5, y5 = wcx + (r_ring - 33) * math.cos(a5), wcy - (r_ring - 33) * math.sin(a5)
        x2, y2 = wcx + (r_ring - 33) * math.cos(a2), wcy - (r_ring - 33) * math.sin(a2)
        els.append(
            f'<path d="M{x5:.1f},{y5:.1f} A43,43 0 0,0 {x2:.1f},{y2:.1f}" '
            f'fill="none" stroke="{GREEN}" stroke-width="2.0" marker-end="url(#arr-green)"/>'
        )

        # Bottom explanation box inside Left Panel
        els.append(card(34, 352, 338, 78, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(44, 371, "减法变加法：5 − 3 = 5 + (−3)  [反码+1：0011→1101]", 10.0, BLUE, weight="700"))
        els.append(txt(44, 390, "0101(+5) + 1101(−3) = [1]0010 → 丢进位得 0010(+2)！", 9.8, INK, weight="600", cls="mono"))
        els.append(txt(44, 409, "注：0.1+0.2≠0.3 是 IEEE 754 浮点二进制循环小数截断所致。", 9.8, MUTED))

        # ---------------- Right Panel: 24-Bit RGB Subpixel Mixing ----------------
        els.append(card(398, 62, 342, 380))
        els.append(txt(412, 85, "② 24 位真彩色：3 个字节点亮 1 颗像素", PANEL_TITLE, INK, weight="700"))
        els.append(txt(412, 103, "每颗像素内藏 R、G、B 三根发光子像素条（0–255 级亮度）", 10.4, MUTED))

        # Subpixel zoom box + mixed color swatch (#FF881A = rgb(255, 136, 26))
        els.append(card(412, 116, 314, 128, rx=8, fill="#0f172a", stroke=SLATE))
        els.append(txt(424, 135, "单颗像素放大镜（三根并排子像素）：", 10.3, "#e2e8f0", weight="700"))

        sub_specs = [
            (428, "R红", "255", "#ef4444", 1.00),
            (482, "G绿", "136", "#22c55e", 136 / 255.0),
            (536, "B蓝", "26", "#3b82f6", 26 / 255.0),
        ]
        for sx, slbl, sval, scol, s_op in sub_specs:
            els.append(f'<rect x="{sx}" y="144" width="34" height="62" rx="4" fill="#1e293b" stroke="#475569"/>')
            fill_h = max(8.0, 58.0 * s_op)
            els.append(
                f'<rect x="{sx + 2}" y="{144 + 60 - fill_h:.1f}" width="30" height="{fill_h:.1f}" rx="3" fill="{scol}"/>'
            )
            els.append(txt(sx + 17, 220, slbl, 9.6, "#cbd5e1", "middle", weight="600"))
            els.append(txt(sx + 17, 234, sval, 9.8, "#ffffff", "middle", weight="700", cls="mono"))

        # Arrow to fused human perception swatch
        els.append(txt(588, 180, "→", 15, "#e2e8f0", "middle", weight="700"))
        els.append(f'<rect x="604" y="144" width="110" height="62" rx="8" fill="#ff881a" stroke="#ffffff" stroke-width="1.8"/>')
        els.append(txt(659, 173, "人眼融合感知", 10.5, "#0f172a", "middle", weight="700"))
        els.append(txt(659, 191, "#FF881A 暖橙", 10.1, "#0f172a", "middle", weight="700", cls="mono"))
        els.append(txt(659, 227, "远看融成一点色光", 9.7, "#cbd5e1", "middle"))

        # 3-byte bit layout table
        els.append(card(412, 254, 314, 84, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(424, 274, "24-bit 编码账：256 × 256 × 256 = 16,777,216 种颜色", 10.6, INK, weight="700"))
        els.append(pill(424, 284, "R: 11111111 (255)", fg=RED, bg=RED_SOFT, w=98, h=22, size=9.8))
        els.append(pill(526, 284, "G: 10001000 (136)", fg=GREEN, bg=GREEN_SOFT, w=98, h=22, size=9.8))
        els.append(pill(628, 284, "B: 00011010 (26)", fg=BLUE, bg=BLUE_SOFT, w=90, h=22, size=9.8))
        els.append(txt(424, 326, "若再加 8 位透明度 Alpha (RGBA)，每像素恰占 4 字节 (32 bit)。", 9.8, MUTED))

        # Frame buffer throughput reality check
        els.append(card(412, 352, 314, 78, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(424, 371, "算一算显卡有多忙（1920×1080 屏幕 @ 60 Hz）：", 10.6, PURPLE, weight="700"))
        els.append(txt(424, 390, "• 单帧画面 = 207.36 万像素 × 3 B ≈ 6.22 MB 数据；", 10.2, BODY))
        els.append(txt(424, 408, "• 每秒刷新 60 帧（每帧仅 16.7 ms）→ 需吞吐 373.2 MB/s！", 10.2, PURPLE, weight="700"))

        return figure(
            456,
            "4位二进制补码时钟圆盘加减统一原理与24位RGB子像素1677万色合成图",
            "左图用16格4位二进制时钟轮演示负数补码与5减3等价于0101加1101自然溢出得0010，使同一套加法器兼做减法；右图拆解单颗像素内红255、绿136、蓝26三根子像素合成暖橙色#FF881A，并实算24位16777216色及1080p 60帧每秒373.2MB吞吐量。",
            els,
        )

    def _build_cpu_memory_time_scale():
        """SVG 3: Log-scale latency pyramid scaling 1 CPU cycle (0.25 ns @ 4 GHz) -> 1 human second."""
        cycle_ns = 0.25  # 4.0 GHz clock period
        scale_to_human_s = 1.0 / cycle_ns  # 4.0e9x magnification (0.25 ns -> 1.0 s)
        assert math.isclose(cycle_ns * scale_to_human_s, 1.0)

        tiers = [
            ("CPU 寄存器", 0.25, "1 秒", "低头看一眼手里的笔", "< 1 KB", BLUE, BLUE_SOFT),
            ("L1 高速缓存", 1.0, "4 秒", "伸手拿桌角草稿纸", "32–64 KB", BLUE, BLUE_SOFT),
            ("L2 高速缓存", 3.5, "14 秒", "起身去书架抽一本书", "0.5–2 MB", GREEN, GREEN_SOFT),
            ("L3 共享缓存", 12.0, "48 秒", "去隔壁房间翻资料", "16–64 MB", GREEN, GREEN_SOFT),
            ("DDR5 主内存", 80.0, "5 分 20 秒", "下楼去便利店买水", "16–64 GB", ORANGE, ORANGE_SOFT),
            ("NVMe 固态盘", 25_000.0, "≈ 1.2 天", "坐高铁去外地次日回", "1–4 TB", PURPLE, PURPLE_SOFT),
            ("HDD 机械硬盘", 8_000_000.0, "≈ 1 年", "徒步环球一年才回来", "4–20 TB", RED, RED_SOFT),
        ]

        # Verify exact scaling mathematics for every row
        assert math.isclose(tiers[4][1] * scale_to_human_s, 320.0)  # 5m 20s
        assert 27.7 < (tiers[5][1] * scale_to_human_s) / 3600.0 < 27.9  # 27.8 hours
        assert 370.0 < (tiers[6][1] * scale_to_human_s) / 86400.0 < 371.0  # 370.4 days

        els = header(
            "为什么 4 GHz 的 CPU 离不开缓存？—— 把 1 个时钟周期放大成“人类 1 秒”",
            "若 CPU 算一次（0.25 ns）等于你眨眼 1 秒，等一次内存就像下楼买水花 5 分钟，读一次固态盘要等一天多！",
        )

        els.append(card(20, 62, 720, 274))
        els.append(
            txt(
                36,
                85,
                "① 存储层次延迟对数尺（横轴 log₁₀ 真实纳秒；右侧为同步放大 4×10⁹ 倍后的人类体感时间）",
                PANEL_TITLE,
                INK,
                weight="700",
            )
        )

        bx0, bw = 128.0, 256.0
        log_lo, log_hi = math.log10(0.1), math.log10(10_000_000.0)  # -1 to +7 (8 decades)

        def _lx(ns_val):
            return bx0 + ((math.log10(ns_val) - log_lo) / (log_hi - log_lo)) * bw

        # Vertical log10 decade gridlines (every 2 decades + 1ns/100ns for clean wide tick spacing!)
        decade_ticks = [
            (0.1, "0.1ns"),
            (1.0, "1ns"),
            (10.0, "10ns"),
            (100.0, "100ns"),
            (1e4, "10μs"),
            (1e6, "1ms"),
            (1e7, "10ms"),
        ]
        for d_ns, d_lbl in decade_ticks:
            dx = _lx(d_ns)
            els.append(f'<line x1="{dx:.1f}" y1="98" x2="{dx:.1f}" y2="302" stroke="{SLATE_SOFT}" stroke-width="1"/>')
            els.append(txt(dx, 318, d_lbl, 9.6, MUTED, "middle", cls="mono"))

        # Column headers on right
        els.append(txt(400, 104, "真实延迟", 10.3, MUTED, "start", weight="700"))
        els.append(txt(468, 104, "放大后人类体感", 10.3, INK, "start", weight="700"))
        els.append(txt(724, 104, "典型容量", 10.3, MUTED, "end", weight="700"))

        for idx, (name, ns_v, h_str, metaphor, cap_str, col, bg_col) in enumerate(tiers):
            ry = 114 + idx * 27
            bar_end = _lx(ns_v)
            bar_w = max(8.0, bar_end - bx0)
            if idx in (4, 5):
                els.append(f'<rect x="30" y="{ry - 2}" width="698" height="23" rx="4" fill="{bg_col}" opacity="0.55"/>')

            els.append(txt(36, ry + 14, name, 10.6, col if idx >= 4 else INK, weight="700"))
            els.append(f'<rect x="{bx0:.1f}" y="{ry + 2}" width="{bar_w:.1f}" height="14" rx="3" fill="{col}"/>')

            ns_disp = f"{ns_v:g} ns" if ns_v < 1000 else (f"{ns_v / 1000:g} μs" if ns_v < 1e6 else f"{ns_v / 1e6:g} ms")
            els.append(txt(400, ry + 14, ns_disp, 10.1, BODY, cls="mono"))
            els.append(txt(468, ry + 14, f"{h_str} · {metaphor}", 10.2, col if idx >= 4 else BODY, weight="700" if idx >= 4 else None))
            els.append(txt(724, ry + 14, cap_str, 10.0, MUTED, "end", cls="mono"))

        # ---------------- Bottom Insight Cards ----------------
        els.append(card(20, 348, 354, 82, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(34, 368, "② 为什么不把整块硬盘都做成 L1 缓存那么快？", 11.0, BLUE, weight="700"))
        els.append(txt(34, 388, "物理与面积铁律：高速缓存 SRAM 约需 6 颗晶体管存 1 bit，", 10.3, BODY))
        els.append(txt(34, 406, "且信号走线多几毫米都会增加延迟；越快就注定越小、越贵。", 10.3, BODY))

        els.append(card(386, 348, 354, 82, rx=8, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(400, 368, "③ 缓存为什么能猜中 90%+ 的下一步？（局部性原理）", 11.0, GREEN, weight="700"))
        els.append(txt(400, 388, "• 时间局部性：循环里刚用过的变量，下一秒往往还要用；", 10.3, BODY))
        els.append(txt(400, 406, "• 空间局部性：读地址 [20] 时，顺手把隔壁一整行 64B 搬上桌！", 10.3, BODY))

        return figure(
            442,
            "4GHz处理器存储金字塔延迟对数标尺与人类时间尺度换算图",
            "将CPU一个时钟周期0.25纳秒放大40亿倍映射为人类1秒：寄存器1秒、L1缓存4秒、L2缓存14秒、L3缓存48秒、DDR5主内存5分20秒、NVMe固态硬盘1.2天、机械硬盘寻道约1年，直观解释为何现代计算机必须采用多级缓存与局部性预取。",
            els,
        )

    @register("comp-arch", "计算机底层原理：香农继电器开关门、二进制补码圆盘与RGB子像素、CPU存储层次人类时间尺度", "science_tech")
    def build_comp_arch():
        write_svg("comp-arch", "shannon-switches-to-gates.svg", _build_shannon_switches_to_gates())
        write_svg("comp-arch", "twos-complement-rgb.svg", _build_twos_complement_rgb())
        write_svg("comp-arch", "cpu-memory-time-scale.svg", _build_cpu_memory_time_scale())


_register_resp_and_comp()
