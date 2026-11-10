"""Original descriptive-geometry teaching figures, not production drawings."""

import math
from pathlib import Path

from generate_kepler_newton_visuals import BLUE, GOLD, INK, RED, dot, line, panel, path, save, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "monge"
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


if __name__ == "__main__":
    main()
