"""Original weaving diagrams; binary masks mean warp above weft, not colour."""

from pathlib import Path
import xml.etree.ElementTree as ET

from generate_kepler_newton_visuals import (
    BLUE, GOLD, INK, RED, dot, line, panel, path, save, text,
)


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "loom-history"
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


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for draw in [interlacing, weaving_cycle, weave_structures, stored_shafts,
                 needle_hooks, cards_to_cloth, development_tracks, modern_weaving]:
        draw()
    validate()
