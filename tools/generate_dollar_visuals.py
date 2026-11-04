"""Original reading aids, deliberately not banknote or Great Seal facsimiles."""

from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "dollar-reading"
INK, BLUE, GREEN, GOLD = "#18364b", "#21699a", "#176d5b", "#92530a"
PALE, SAND = "#e7f0f8", "#faf0dd"
YEARS = [1782, 1935, 1955, 1956, 1957, 1963]
ROMAN_PARTS = [("M", 1000), ("D", 500), ("CC", 200), ("L", 50),
               ("XX", 20), ("V", 5), ("I", 1)]


def text(x, y, value, size=25, color=INK, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}">{escape(str(value))}</text>')


def rect(x, y, w, h, fill=PALE, radius=10):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="#adc2d1" stroke-width="2"/>')


def path(d, color=BLUE, width=3, fill="none"):
    return f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill}"/>'


def save(name, title, description, body, height):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="0 0 720 {height}" role="img" aria-labelledby="title desc" lang="zh-CN">'
           f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
           '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}</style>'
           f'<rect width="720" height="{height}" rx="16" fill="#fafcfe"/>'
           + text(28, 48, title, 30) + body + '</svg>\n')
    root = ET.fromstring(svg)
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


if __name__ == "__main__":
    reverse_map()
    many_to_one()
    pyramid()
    history()
    front()
    assert len(list(OUT.glob("*.svg"))) == 5
    print("Generated 5 original dollar-reading diagrams; counts and Roman year verified.")
