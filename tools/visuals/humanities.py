"""Humanities, history, and classical literature diagrams for blog posts."""

from html import escape
import math

from .core import (
    BLUE,
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
    card,
    figure,
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

GOLD = "#b45309"
GOLD_SOFT = "#fef3c7"
GOLD_BRIGHT = "#f59e0b"
PLAQUE_BLUE = "#163a5f"
PLAQUE_TEXT = "#fde68a"
CRIMSON = "#9f1239"
CRIMSON_SOFT = "#ffe4e6"


def _line(x1, y1, x2, y2, stroke=HAIRLINE, sw=1.4, dash=None, marker=None, opacity=None):
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


def _register_daguanlou_couplet():
    SUBDIR = "daguanlou-couplet"

    # Exact public-domain 180-character couplet segmented into 20 parallel beats
    SEGS_UP = [
        "五百里滇池", "奔来眼底", "披襟岸帻", "喜茫茫空阔无边",
        "看", "东骧神骏", "西翥灵仪", "北走蜿蜒", "南翔缟素",
        "高人韵士", "何妨选胜登临",
        "趁蟹屿螺洲", "梳裹就风鬟雾鬓", "更蘋天苇地", "点缀些翠羽丹霞",
        "莫辜负", "四围香稻", "万顷晴沙", "九夏芙蓉", "三春杨柳",
    ]
    SEGS_DN = [
        "数千年往事", "注到心头", "把酒凌虚", "叹滚滚英雄谁在",
        "想", "汉习楼船", "唐标铁柱", "宋挥玉斧", "元跨革囊",
        "伟烈丰功", "费尽移山心力",
        "尽珠帘画栋", "卷不及暮雨朝云", "便断碣残碑", "都付与苍烟落照",
        "只赢得", "几杵疏钟", "半江渔火", "两行秋雁", "一枕清霜",
    ]
    assert sum(len(s) for s in SEGS_UP) == 90
    assert sum(len(s) for s in SEGS_DN) == 90
    assert [len(s) for s in SEGS_UP] == [len(s) for s in SEGS_DN]

    def _build_180_architecture_map():
        """SVG 1: 90 + 90 = 180 exact 3-act 20-beat structural & tonal anatomy."""
        act1_len = sum(len(s) for s in SEGS_UP[0:4])    # 5+4+4+7 = 20
        act2a_len = sum(len(s) for s in SEGS_UP[4:9])   # 1+4+4+4+4 = 17
        act2b_len = sum(len(s) for s in SEGS_UP[9:11])  # 4+6 = 10
        act2c_len = sum(len(s) for s in SEGS_UP[11:15]) # 5+7+5+7 = 24
        act3_len = sum(len(s) for s in SEGS_UP[15:20])  # 3+4+4+4+4 = 19
        assert act1_len == 20
        assert act2a_len + act2b_len + act2c_len == 51
        assert act3_len == 19
        assert act1_len + 51 + act3_len == 90

        els = []
        els.extend(
            header(
                "180 字分毫必合：大观楼长联“三幕二十拍”精密对称解剖图",
                "上联 90 字拓空间写实景（喜），下联 90 字贯古今咏兴亡（叹）；20 个分句字数、句式、领字严丝合缝。",
            )
        )

        # Column headers
        els.append(card(20, 62, 720, 34, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(36, 84, "结构分段（字数）", size=11.5, color=SLATE, weight="700"))
        els.append(txt(206, 84, "上联 · 90 字｜空间实景 · 眼底之“喜”", size=12.0, color=BLUE, weight="700"))
        els.append(txt(482, 84, "下联 · 90 字｜时间历史 · 心头之“叹”", size=12.0, color=ORANGE, weight="700"))

        blocks = [
            {
                "y": 104,
                "h": 76,
                "badge": "第一幕",
                "title": "登楼起势（20字）",
                "meta": "5·4·4·7 破题立眼",
                "fg": BLUE,
                "bg": BLUE_SOFT,
                "up_1": "五百里滇池，奔来眼底，",
                "up_2": "披襟岸帻，喜茫茫空阔无边。",
                "dn_1": "数千年往事，注到心头，",
                "dn_2": "把酒凌虚，叹滚滚英雄谁在？",
                "note": "联眼对撞：“奔来眼底·喜”对“注到心头·叹”",
            },
            {
                "y": 188,
                "h": 82,
                "badge": "第二幕A",
                "title": "一字领四方/四朝（17字）",
                "meta": "1字领 + 四组四言排比",
                "fg": GREEN,
                "bg": GREEN_SOFT,
                "up_1": "看：东骧神骏，西翥灵仪，",
                "up_2": "北走蜿蜒，南翔缟素。",
                "dn_1": "想：汉习楼船，唐标铁柱，",
                "dn_2": "宋挥玉斧，元跨革囊。",
                "note": "以“看”摄东西南北四山，以“想”贯汉唐宋元四朝",
            },
            {
                "y": 278,
                "h": 68,
                "badge": "第二幕B",
                "title": "承上转折过渡（10字）",
                "meta": "4·6 蓄势换气",
                "fg": SLATE,
                "bg": SLATE_SOFT,
                "up_1": "高人韵士，何妨选胜登临。",
                "up_2": "",
                "dn_1": "伟烈丰功，费尽移山心力。",
                "dn_2": "",
                "note": "上联邀雅士赏景，下联叹帝王霸业劳神",
            },
            {
                "y": 354,
                "h": 82,
                "badge": "第二幕C",
                "title": "隔句扇面对铺陈（24字）",
                "meta": "5·7 + 5·7 流水偶句",
                "fg": PURPLE,
                "bg": PURPLE_SOFT,
                "up_1": "趁蟹屿螺洲，梳裹就风鬟雾鬓；",
                "up_2": "更蘋天苇地，点缀些翠羽丹霞。",
                "dn_1": "尽珠帘画栋，卷不及暮雨朝云；",
                "dn_2": "便断碣残碑，都付与苍烟落照。",
                "note": "化用王勃《滕王阁序》，浓墨重彩转向荒烟残碑",
            },
            {
                "y": 444,
                "h": 86,
                "badge": "第三幕",
                "title": "三字领四言收束（19字）",
                "meta": "3字领 + 4·4·4·4 余韵",
                "fg": GOLD,
                "bg": GOLD_SOFT,
                "up_1": "莫辜负：四围香稻，万顷晴沙，",
                "up_2": "九夏芙蓉，三春杨柳。（仄收）",
                "dn_1": "只赢得：几杵疏钟，半江渔火，",
                "dn_2": "两行秋雁，一枕清霜。（平收）",
                "note": "数词暗藏机锋：“四·万·九·三”繁华对“几·半·两·一”归零！",
            },
        ]

        for b in blocks:
            by, bh = b["y"], b["h"]
            els.append(card(20, by, 720, bh, rx=9, fill=CARD_BG, stroke=BORDER))
            # Left structural column (x=20..192)
            els.append(pill(32, by + 10, b["badge"], fg=b["fg"], bg=b["bg"], w=74, h=20, size=10.8))
            els.append(txt(32, by + 46, b["title"], size=11.4, color=INK, weight="700"))
            els.append(txt(32, by + 63, b["meta"], size=10.3, color=MUTED))
            els.append(_line(194, by + 8, 194, by + bh - 8, stroke=HAIRLINE, sw=1.0))

            # Middle column: Upper couplet (x=206..466)
            els.append(card(204, by + 8, 260, bh - 26 if b["up_2"] else bh - 28, rx=6, fill="#f8fbff", stroke="#dbeafe"))
            if b["up_2"]:
                els.append(txt(214, by + 26, b["up_1"], size=11.2, color=INK, weight="600"))
                els.append(txt(214, by + 44, b["up_2"], size=11.2, color=BLUE, weight="700"))
            else:
                els.append(txt(214, by + 29, b["up_1"], size=11.4, color=BLUE, weight="700"))

            # Right column: Lower couplet (x=476..732)
            els.append(card(474, by + 8, 256, bh - 26 if b["dn_2"] else bh - 28, rx=6, fill="#fffaf5", stroke="#fed7aa"))
            if b["dn_2"]:
                els.append(txt(484, by + 26, b["dn_1"], size=11.2, color=INK, weight="600"))
                els.append(txt(484, by + 44, b["dn_2"], size=11.2, color=ORANGE, weight="700"))
            else:
                els.append(txt(484, by + 29, b["dn_1"], size=11.4, color=ORANGE, weight="700"))

            # Bottom micro-caption across right two columns
            els.append(txt(206, by + bh - 7, "↳ " + b["note"], size=10.3, color=b["fg"], weight="600"))

        # Bottom summary bar
        els.append(card(20, 538, 720, 32, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        els.append(
            txt(
                380,
                558,
                "字数验算：20（起势）+ 17（四排）+ 10（转折）+ 24（偶句）+ 19（收束）= 90 字/联 × 2 = 180 字整",
                size=11.2,
                color=INK,
                anchor="middle",
                weight="700",
            )
        )

        svg = figure(
            582,
            "大观楼180字长联三幕二十拍结构与声律对称解剖图",
            "将孙髯翁180字大观楼长联拆解为上联90字写景与下联90字咏史两大翼，按第一幕20字登楼起势、第二幕51字中腹铺陈（17字四方对四朝、10字转折、24字扇面对偶句）、第三幕19字四言收束逐行对照，并点明四万九三对几半两一的数词递减机锋。",
            els,
        )
        write_svg(SUBDIR, "couplet-180-architecture-map.svg", svg)

    def _build_dianchi_four_totems_panorama():
        """SVG 2: Schematic spatial panorama of Dianchi & 4 cardinal totem mountains with 1-shot gaze sweep."""
        els = []
        els.extend(
            header(
                "登大观楼看什么？五百里滇池与“东骧·西翥·北走·南翔”四方山势图",
                "上北下南方位示意（非等比例测绘图）：立于草海北滨近华浦大观楼，四面山川与四季湖景尽收眼底。",
            )
        )

        extra_css = """
  @keyframes beamSweep {
    0%   { opacity: 0.18; }
    25%  { opacity: 0.95; }
    100% { opacity: 0.78; }
  }
  @keyframes cardPop {
    0%   { opacity: 0.35; }
    100% { opacity: 1; }
  }
  .gaze-1 { animation: beamSweep 1.6s ease-out 0.1s 1 both; }
  .gaze-2 { animation: beamSweep 1.6s ease-out 1.0s 1 both; }
  .gaze-3 { animation: beamSweep 1.6s ease-out 1.9s 1 both; }
  .gaze-4 { animation: beamSweep 1.6s ease-out 2.8s 1 both; }
  .totem-1 { animation: cardPop 0.9s ease-out 0.2s 1 both; }
  .totem-2 { animation: cardPop 0.9s ease-out 1.1s 1 both; }
  .totem-3 { animation: cardPop 0.9s ease-out 2.0s 1 both; }
  .totem-4 { animation: cardPop 0.9s ease-out 2.9s 1 both; }
  @media (prefers-reduced-motion: reduce) {
    .gaze-1, .gaze-2, .gaze-3, .gaze-4,
    .totem-1, .totem-2, .totem-3, .totem-4 {
      animation: none !important;
      opacity: 1 !important;
    }
  }
"""

        # Main map canvas card
        mx, my, mw, mh = 20, 64, 720, 344
        els.append(card(mx, my, mw, mh, rx=12, fill="#f4f9fd", stroke=BORDER))

        # Compass badge in top-right of map
        els.append(card(mx + mw - 96, my + 12, 82, 46, rx=7, fill=CARD_BG, stroke=BORDER))
        els.append(txt(mx + mw - 55, my + 30, "↑ 北 (N)", size=11.2, color=INK, anchor="middle", weight="700"))
        els.append(txt(mx + mw - 55, my + 48, "方位示意", size=10.2, color=MUTED, anchor="middle"))

        # Dianchi water body (Caohai in north + vast Waihai stretching south)
        els.append(
            '<path d="M278,158 C325,146 410,150 442,176 C474,202 486,252 470,308 '
            'C454,352 396,368 342,360 C294,352 268,312 262,262 C256,214 246,170 278,158 Z" '
            'fill="#dbeafe" stroke="#60a5fa" stroke-width="1.6"/>'
        )
        # Inner Caohai water tint near Daguanlou
        els.append(
            '<ellipse cx="352" cy="184" rx="64" ry="22" fill="#bae6fd" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4 3"/>'
        )
        # Tiny Crab & Snail islets ("蟹屿螺洲")
        els.append('<ellipse cx="322" cy="216" rx="14" ry="6" fill="#bbf7d0" stroke="#16a34a" stroke-width="1"/>')
        els.append('<ellipse cx="392" cy="228" rx="11" ry="5" fill="#bbf7d0" stroke="#16a34a" stroke-width="1"/>')
        els.append(txt(360, 248, "蟹屿螺洲 · 蘋天苇地", size=10.6, color=BLUE, anchor="middle", weight="600", halo=True))
        els.append(txt(368, 274, "五百里滇池（外海）", size=12.2, color="#1e40af", anchor="middle", weight="700", halo=True))
        els.append(txt(368, 293, "海拔约 1886m · 今面积约 309.5 km²", size=10.3, color=SLATE, anchor="middle", halo=True))

        # Daguanlou hub at northern Caohai shore (356, 174)
        hub_x, hub_y = 356, 174

        # 4 Cardinal sightline rays from Daguanlou (animated 1->2->3->4 in order of couplet!)
        els.append(f'<g class="gaze-1">{_line(hub_x + 28, hub_y + 12, 534, 218, stroke=GOLD, sw=2.1, dash="6 4", marker="arr-orange")}</g>')
        els.append(f'<g class="gaze-2">{_line(hub_x - 28, hub_y + 12, 224, 224, stroke=GREEN, sw=2.1, dash="6 4", marker="arr-green")}</g>')
        els.append(f'<g class="gaze-3">{_line(hub_x, hub_y - 18, 356, 128, stroke=PURPLE, sw=2.1, dash="6 4", marker="arr-blue")}</g>')
        els.append(f'<g class="gaze-4">{_line(hub_x + 4, hub_y + 20, 366, 330, stroke=BLUE, sw=2.1, dash="6 4", marker="arr-blue")}</g>')

        # Center pavilion badge: Daguanlou
        els.append(card(hub_x - 62, hub_y - 17, 124, 34, rx=8, fill=PLAQUE_BLUE, stroke=GOLD_BRIGHT, sw=1.8))
        els.append(txt(hub_x, hub_y + 4, "★ 大观楼（近华浦）", size=11.0, color=PLAQUE_TEXT, anchor="middle", weight="700"))

        # ③ North: Changchong / Snake Mountain ("北走蜿蜒")
        els.append('<g class="totem-3">')
        els.append(card(236, 74, 244, 52, rx=8, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.3))
        els.append(txt(248, 94, "③ 北走蜿蜒 → 长虫山（蛇山）", size=11.4, color=PURPLE, weight="700"))
        els.append(txt(248, 113, "北郊山脉如长蛇蜿蜒南下，护卫昆明城垣", size=10.3, color=BODY))
        els.append("</g>")

        # ② West: Biji / Xishan ("西翥灵仪")
        els.append('<g class="totem-2">')
        els.append(card(34, 194, 188, 92, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.4))
        els.append(txt(46, 215, "② 西翥灵仪", size=11.8, color=GREEN, weight="700"))
        els.append(txt(46, 234, "→ 碧鸡山（西山/太华山）", size=10.8, color=INK, weight="700"))
        els.append(txt(46, 253, "隔草海正对大观楼，峰峦", size=10.2, color=BODY))
        els.append(txt(46, 270, "叠翠如凤凰展翅高飞", size=10.2, color=BODY))
        els.append("</g>")

        # ① East: Jinma Mountain ("东骧神骏")
        els.append('<g class="totem-1">')
        els.append(card(538, 194, 188, 92, rx=8, fill=GOLD_SOFT, stroke=GOLD, sw=1.4))
        els.append(txt(550, 215, "① 东骧神骏", size=11.8, color=GOLD, weight="700"))
        els.append(txt(550, 234, "→ 金马山（东郊丘陵）", size=10.8, color=INK, weight="700"))
        els.append(txt(550, 253, "山势起伏奔腾，如神骏", size=10.2, color=BODY))
        els.append(txt(550, 270, "昂首腾骧；与碧鸡相望", size=10.2, color=BODY))
        els.append("</g>")

        # ④ South: Baihe Mountain in Jinning ("南翔缟素")
        els.append('<g class="totem-4">')
        els.append(card(224, 334, 286, 62, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.4))
        els.append(txt(236, 355, "④ 南翔缟素 → 晋宁白鹤山（毗邻古滇国石寨山）", size=11.3, color=BLUE, weight="700"))
        els.append(txt(236, 374, "“缟素”指洁白鹤羽；远眺南岸群峰如白鹤凌波翱翔", size=10.3, color=BODY))
        els.append("</g>")

        # Bottom four-season shore strip ("莫辜负：四围香稻，万顷晴沙，九夏芙蓉，三春杨柳")
        els.append(card(20, 418, 720, 56, rx=9, fill=CARD_BG, stroke=BORDER))
        els.append(txt(34, 440, "收束近景 · 四季风物：", size=11.2, color=INK, weight="700"))
        seasons = [
            (172, "秋 · 四围香稻", "湖滨万亩稻浪", GOLD, GOLD_SOFT),
            (312, "冬 · 万顷晴沙", "水落晴沙浩渺", SLATE, SLATE_SOFT),
            (452, "夏 · 九夏芙蓉", "盛夏荷花映日", CRIMSON, CRIMSON_SOFT),
            (592, "春 · 三春杨柳", "长堤烟柳拂波", GREEN, GREEN_SOFT),
        ]
        for sx, stitle, ssub, sfg, sbg in seasons:
            els.append(card(sx, 425, 132, 42, rx=6, fill=sbg, stroke=sfg, sw=1.0))
            els.append(txt(sx + 66, 443, stitle, size=10.8, color=sfg, anchor="middle", weight="700"))
            els.append(txt(sx + 66, 459, ssub, size=10.0, color=BODY, anchor="middle"))

        svg = figure(
            486,
            "大观楼俯瞰五百里滇池与东西南北四山图腾空间方位图",
            "以滇池北端草海近华浦的大观楼为观察原点，按上联顺序标示①东骧神骏（金马山）、②西翥灵仪（碧鸡山/西山）、③北走蜿蜒（长虫山/蛇山）、④南翔缟素（晋宁白鹤山），中景标出蟹屿螺洲与蘋天苇地，底部归纳四围香稻、万顷晴沙、九夏芙蓉、三春杨柳四季盛景。",
            els,
            extra_css=extra_css,
        )
        write_svg(SUBDIR, "dianchi-four-totems-panorama.svg", svg)

    def _build_four_dynasties_yunnan_epic():
        """SVG 3: 1,400-year historical timeline of the 4 allusions + hidden Ming/Qing coda."""
        els = []
        els.extend(
            header(
                "十六字浓缩一千四百年：下联“汉·唐·宋·元”四大典故与弦外之音",
                "从长安昆明池楼船、滇王金印到忽必烈革囊渡江，再看懂“珠帘画栋”背后不敢明写的清初王府兴亡。",
            )
        )

        eras = [
            {
                "x": 20,
                "y": 64,
                "num": "1",
                "phrase": "汉习楼船",
                "year": "前 120 — 前 109 年",
                "fg": BLUE,
                "bg": BLUE_SOFT,
                "l1": "史实：汉武帝在长安凿“昆明池”，造十余丈",
                "l2": "高楼船操练水军（《史记·平准书》）；元封",
                "l3": "二年发兵临滇，滇王举国降汉，置益州郡。",
                "ev": "铁证：1956 晋宁石寨山出土蛇钮金印“滇王之印”（国博藏）",
            },
            {
                "x": 388,
                "y": 64,
                "num": "2",
                "phrase": "唐标铁柱",
                "year": "707 年（唐景龙元年）",
                "fg": ORANGE,
                "bg": ORANGE_SOFT,
                "l1": "史实：吐蕃在漾濞江架铁索桥联结西洱河诸",
                "l2": "蛮；唐御史唐九征率兵毁铁索城破敌，铸立",
                "l3": "铁柱纪功（后世南诏蒙世隆亦曾重铸铁柱）。",
                "ev": "考据：《新唐书》写作立于“滇池”，实考在今大理弥渡/洱海带",
            },
            {
                "x": 20,
                "y": 222,
                "num": "3",
                "phrase": "宋挥玉斧",
                "year": "965 年（宋乾德三年）",
                "fg": GREEN,
                "bg": GREEN_SOFT,
                "l1": "史实：北宋灭后蜀，宋太祖鉴晚唐桂林戍卒",
                "l2": "之祸，划大渡河与段氏大理国（937–1253，",
                "l3": "历 22 王 317 年）为界，换西南近三百年无战事。",
                "ev": "辨析：北宋仅载“画大渡为境”，“挥玉斧”系南宋文人敷演美谈",
            },
            {
                "x": 388,
                "y": 222,
                "num": "4",
                "phrase": "元跨革囊",
                "year": "1253 — 1274 年",
                "fg": PURPLE,
                "bg": PURPLE_SOFT,
                "l1": "史实：1253 年忽必烈分兵三路穿横断山谷两",
                "l2": "千余里，乘牛羊皮充气“革囊”及竹筏奇袭渡",
                "l3": "过金沙江灭大理（《元史·世祖本纪》）。",
                "ev": "巨变：1274 年建云南行省，全省中心正式从大理迁至昆明！",
            },
        ]

        for e in eras:
            ex, ey = e["x"], e["y"]
            els.append(card(ex, ey, 352, 146, rx=10, fill=CARD_BG, stroke=BORDER))
            els.append(step_badge(ex + 22, ey + 22, e["num"], fg=e["fg"], bg=e["bg"]))
            els.append(txt(ex + 40, ey + 27, e["phrase"], size=13.5, color=e["fg"], weight="700"))
            els.append(pill(ex + 168, ey + 11, e["year"], fg=e["fg"], bg=e["bg"], w=170, h=22, size=10.6))
            els.append(txt(ex + 16, ey + 54, e["l1"], size=10.8, color=BODY))
            els.append(txt(ex + 16, ey + 73, e["l2"], size=10.8, color=BODY))
            els.append(txt(ex + 16, ey + 92, e["l3"], size=10.8, color=BODY))
            els.append(card(ex + 12, ey + 106, 328, 30, rx=6, fill=e["bg"], stroke=e["fg"], sw=0.9))
            els.append(txt(ex + 22, ey + 125, e["ev"], size=10.1, color=INK, weight="600"))

        # Bottom wide card: Why did it stop at Yuan? The hidden Ming/Qing subtext!
        bx, by, bw, bh = 20, 382, 720, 126
        els.append(card(bx, by, bw, bh, rx=10, fill=CRIMSON_SOFT, stroke=CRIMSON, sw=1.4))
        els.append(txt(bx + 18, by + 25, "⑤ 为什么写完元朝突然停笔？—— 藏在“珠帘画栋”里的明清弦外之音", size=12.6, color=CRIMSON, weight="700"))
        els.append(
            txt(
                bx + 18,
                by + 49,
                "• 表面借古：化用唐代王勃《滕王阁序》“画栋朝飞南浦云，珠帘暮卷西山雨”——妙在昆明滇池西岸真有一座西山！",
                size=10.8,
                color=INK,
            )
        )
        els.append(
            txt(
                bx + 18,
                by + 70,
                "• 暗写近事：明代沐英家族镇滇近三百年，清初吴三桂更掏空民力在昆明五华山兴建恢弘王府（僭号周王/洪化），",
                size=10.8,
                color=BODY,
            )
        )
        els.append(
            txt(
                bx + 18,
                by + 91,
                "  旋即灰飞烟灭！乾隆朝文网森严，布衣孙髯翁不着一字提明清，却把帝王霸业一并扫入“苍烟落照、一枕清霜”——",
                size=10.8,
                color=BODY,
            )
        )
        els.append(
            txt(
                bx + 18,
                by + 111,
                "  正因看穿了这层“把正统皇权也归于一空”的锋芒，半个世纪后的云贵总督阮元才会坐立不安、动刀改联！",
                size=10.8,
                color=CRIMSON,
                weight="700",
            )
        )

        svg = figure(
            520,
            "大观楼长联下联汉习楼船唐标铁柱宋挥玉斧元跨革囊四大典故与清代隐笔考据图",
            "分四格考证下联核心历史典故：前120至前109年汉武帝凿昆明池练楼船及晋宁出土滇王之印、707年唐九征毁铁索桥立铁柱、965年宋太祖划大渡河与大理国共存三百年、1253年忽必烈乘牛羊皮革囊渡金沙江并于1274年建云南行省迁省会至昆明；底部揭示珠帘画栋暗涉沐氏与吴三桂五华山王府兴亡的弦外之音。",
            els,
        )
        write_svg(SUBDIR, "four-dynasties-yunnan-epic.svg", svg)

    def _build_sun_ranweng_vs_ruan_yuan_duel():
        """SVG 4: Verbatim textual showdown based on Liang Zhangju's Yinglian conghua & xuhua."""
        els = []
        els.extend(
            header(
                "布衣狂士 vs 两朝帝师：孙髯翁原联与总督阮元“篡改本”交锋实录",
                "据清·梁章钜《楹联丛话·卷七》及《楹联续话》原函校录：一场写进中国文学史的“官印败给民心”。",
            )
        )

        # Two persona header cards
        els.append(card(20, 64, 352, 68, rx=9, fill=BLUE_SOFT, stroke=BLUE, sw=1.4))
        els.append(txt(34, 86, "原作｜孙髯翁（自号“万树梅花一布衣”）", size=12.2, color=BLUE, weight="700"))
        els.append(txt(34, 106, "拒考场搜身终生不仕 · 晚年圆通寺咒蛟台卖卜", size=10.4, color=BODY))
        els.append(txt(34, 122, "视野：站在天地苍生高度，俯视千古帝王霸业", size=10.4, color=INK, weight="600"))

        els.append(card(388, 64, 352, 68, rx=9, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.4))
        els.append(txt(402, 86, "改本｜阮元（体仁阁大学士·道光云贵总督）", size=12.2, color=ORANGE, weight="700"))
        els.append(txt(402, 106, "乾嘉汉学泰斗、封疆大吏 · 另制联板强行悬挂", size=10.4, color=BODY))
        els.append(txt(402, 122, "心态：忌惮“把正统王朝归空”，急于“扶正消逆”", size=10.4, color=INK, weight="600"))

        # Comparison table of 5 decisive alterations
        rows = [
            (
                "登楼胸襟",
                "披襟岸帻，喜茫茫空阔无边",
                "凭栏向远，喜茫茫波浪无边",
                "敞怀推巾的名士狂放 → 规规矩矩扶栏杆看水波",
            ),
            (
                "四方山势",
                "东骧神骏，西翥灵仪，北走蜿蜒，南翔缟素",
                "东骧金马，西翥碧鸡，北倚盘龙，南驯宝象",
                "飞动比拟 → 死板点名；且盘龙江、宝象河把山换成了河！",
            ),
            (
                "湖洲神韵",
                "梳裹就风鬟雾鬓 / 点缀些翠羽丹霞",
                "衬将起苍崖翠壁 / 早收回薄雾残霞",
                "美人梳妆与水鸟丹霞的灵气 → 干瘪生硬的公文布景",
            ),
            (
                "历史定性★",
                "伟烈丰功，费尽移山心力",
                "爨长蒙酋，费尽移山气力",
                "最致命一刀！把汉唐宋元全甩锅给地方土司，保朝廷颜面",
            ),
            (
                "收尾意境",
                "两行秋雁，一枕清霜",
                "两行鸿雁，一片沧桑",
                "刺骨清冷的“清霜”具象 → 空泛套话“一片沧桑”",
            ),
        ]

        y0 = 142
        rh = 50
        for idx, (tag, orig, edit_v, verdict) in enumerate(rows):
            ry = y0 + idx * (rh + 6)
            is_key = "★" in tag
            els.append(card(20, ry, 720, rh, rx=7, fill="#fffdf9" if is_key else CARD_BG, stroke=ORANGE if is_key else BORDER, sw=1.4 if is_key else 1.0))
            els.append(pill(28, ry + 6, tag, fg=CRIMSON if is_key else SLATE, bg=CRIMSON_SOFT if is_key else SLATE_SOFT, w=78, h=19, size=10.2))
            els.append(txt(116, ry + 20, "孙：", size=10.6, color=BLUE, weight="700"))
            els.append(txt(140, ry + 20, orig, size=10.6, color=INK, weight="700"))
            els.append(txt(434, ry + 20, "阮：", size=10.6, color=ORANGE, weight="700"))
            els.append(txt(458, ry + 20, edit_v, size=10.6, color=BODY))
            els.append(txt(116, ry + 40, "评点：" + verdict, size=10.1, color=CRIMSON if is_key else MUTED, weight="600" if is_key else None))

        # Bottom archival quote box: Ruan Yuan's own letter in Yinglian Xuhua + outcome!
        by = 426
        els.append(card(20, by, 720, 74, rx=9, fill=SLATE_SOFT, stroke=SLATE, sw=1.2))
        els.append(txt(34, by + 22, "铁证档案｜阮元致门生梁章钜亲笔信自白（载《楹联续话·胜迹》）：", size=11.2, color=INK, weight="700"))
        els.append(
            txt(
                34,
                by + 43,
                "“孙髯原联，以正统之汉、唐、宋、元伟烈丰功总归一空为主，岂不骎骎乎说到我朝？故改为爨长蒙酋，递到吴三桂等人身上。”",
                size=10.4,
                color=ORANGE,
                weight="600",
            )
        )
        els.append(
            txt(
                34,
                by + 62,
                "结局：昆明士民群起嘲讽（“彼都人士，啧有烦言，旋复撤去”），总督改牌灰溜溜撤下，布衣原联流传至今！",
                size=10.6,
                color=GREEN,
                weight="700",
            )
        )

        svg = figure(
            512,
            "孙髯翁大观楼原联与云贵总督阮元改本五处核心篡改对比及梁章钜楹联续话档案图",
            "依据清代梁章钜《楹联丛话》卷七与《楹联续话》实录，逐条对比孙髯翁原作与云贵总督阮元改本在登楼胸襟、四方山势、湖洲神韵、伟烈丰功改爨长蒙酋、一枕清霜改一片沧桑五处的优劣，并附上阮元自承害怕波及本朝皇权的原信引文及滇人抗议撤牌结局。",
            els,
        )
        write_svg(SUBDIR, "sun-ranweng-vs-ruan-yuan-duel.svg", svg)

    def _build_three_centuries_pavilion_relay():
        """SVG 5: 330-year biography of Daguanlou & the couplet boards (1696 -> 2013)."""
        els = []
        els.extend(
            header(
                "火烧水淹也抹不掉：大观楼与长联木匾的 330 年生死接力",
                "分清“谁建的楼、谁写的词、谁题的现存蓝底金字”——中间隔着一场把原匾烧成灰的战火。",
            )
        )

        # Horizontal timeline spine across 2 rows of 3 cards ( serpentine 1->2->3 / 4->5->6 )
        stages = [
            (
                20, 68, "1690–1696｜康熙", "① 王继文始建两层楼",
                BLUE, BLUE_SOFT,
                "云南巡抚王继文在滇池草海北滨",
                "“近华浦”兴工，建成两层飞檐",
                "观景楼阁，面对太华山定名大观楼。",
            ),
            (
                266, 68, "乾隆年间（18世纪中叶）", "② 孙髯撰联 · 陆树堂首书",
                GREEN, GREEN_SOFT,
                "布衣寒士孙髯翁呕心写下 180 字",
                "长联；昆明名士陆树堂以潇洒行书",
                "手书刻制木匾悬楼，轰动海内。",
            ),
            (
                512, 68, "1828–道光初年", "③ 增建三层 · 阮元改联风波",
                ORANGE, ORANGE_SOFT,
                "道光八年按察使伊里布增修为三层；",
                "总督阮元忌讳联意另悬改本，遭昆",
                "明百姓群嘲抗议，不久撤去改牌。",
            ),
            (
                20, 224, "1857｜咸丰七年", "④ 兵燹焚楼 · 原匾化灰！",
                CRIMSON, CRIMSON_SOFT,
                "咸丰战乱波及昆明省城，大观楼与",
                "悬挂百年的陆树堂行书初刻长联木",
                "匾一同葬身火海，幸联文早已传世！",
            ),
            (
                266, 224, "1866–1883｜同治至光绪", "⑤ 重建三层攒尖顶木楼",
                PURPLE, PURPLE_SOFT,
                "同治五年重建后又遭大水；光绪九",
                "年（1883）再建三层三重檐穿斗木",
                "楼，翼角施云南独有“大刀把”角梁。",
            ),
            (
                512, 224, "1888 至今｜国保文物", "⑥ 赵藩重书蓝底鎏金联",
                GOLD, GOLD_SOFT,
                "光绪十四年总督岑毓英请 38 岁白",
                "族学者赵藩以雄浑楷书重书，刻成",
                "蓝底鎏金抱柱联悬存至今；2013入国保。",
            ),
        ]

        for sx, sy, era, stitle, sfg, sbg, l1, l2, l3 in stages:
            els.append(card(sx, sy, 228, 136, rx=10, fill=CARD_BG, stroke=sfg, sw=1.3))
            els.append(pill(sx + 12, sy + 10, era, fg=sfg, bg=sbg, w=204, h=20, size=10.3))
            els.append(txt(sx + 12, sy + 49, stitle, size=11.8, color=INK, weight="700"))
            els.append(txt(sx + 12, sy + 72, l1, size=10.4, color=BODY))
            els.append(txt(sx + 12, sy + 90, l2, size=10.4, color=BODY))
            els.append(txt(sx + 12, sy + 108, l3, size=10.4, color=BODY))

        # Connectors between cards
        els.append(_line(248, 136, 266, 136, stroke=SLATE, sw=1.8, marker="arr-muted"))
        els.append(_line(494, 136, 512, 136, stroke=SLATE, sw=1.8, marker="arr-muted"))
        els.append(
            '<path d="M626,204 L626,214 L134,214 L134,224" fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#arr-muted)"/>'
        )
        els.append(_line(248, 292, 266, 292, stroke=SLATE, sw=1.8, marker="arr-muted"))
        els.append(_line(494, 292, 512, 292, stroke=SLATE, sw=1.8, marker="arr-muted"))

        # Bottom Easter-egg link between Daguanlou & Chengdu Wuhou Shrine!
        els.append(card(20, 374, 720, 44, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(
            txt(
                380,
                401,
                "冷知识彩蛋：今天大观楼门前写字的那位赵藩（1851–1927），14 年后在成都武侯祠又写下了“能攻心则反侧自消”攻心联！",
                size=10.8,
                color=BLUE,
                anchor="middle",
                weight="700",
            )
        )

        svg = figure(
            430,
            "昆明大观楼建筑与180字长联牌匾从1696年至2013年六阶段历史变迁图",
            "梳理大观楼与长联木匾330年沧桑：1690-1696王继文建两层楼、乾隆孙髯翁撰联陆树堂行书首刻、1828增三层及阮元改联撤牌、1857咸丰战火焚楼毁原匾、1883重建三层大刀把木楼、1888岑毓英请38岁赵藩楷书重刻蓝底鎏金联保存至今并于2013年列入全国重点文物保护单位。",
            els,
        )
        write_svg(SUBDIR, "three-centuries-pavilion-relay.svg", svg)

    def _build_on_site_reading_guide_card():
        """SVG 6: Practical visitor's facade reading order & no-punctuation breathing rhythm card."""
        els = []
        els.extend(
            header(
                "站在大观楼前怎么读不迷路？蓝底金字抱柱联实景读法与断句秘籍",
                "原匾通篇无标点、竖排分列：记住“面门先右后左、末字仄起平收、一字三字领句换气”三条口诀。",
            )
        )

        # Left card: Architectural South Facade & Pillar Order (x=20..368)
        lx, ly, lw, lh = 20, 64, 348, 356
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① 面对临水正门：哪边是上联？按什么顺序读？", size=12.4, color=INK, weight="700"))

        # Stylized 3-tier hip-gable roof + name plaque + two blue-gilt pillar couplet boards
        cx = lx + lw / 2  # 194
        # Tier 3 top roof (pyramid)
        els.append(f'<polygon points="{cx},98 {cx - 56},120 {cx + 56},120" fill="#334155" stroke="{INK}" stroke-width="1.2"/>')
        els.append(f'<rect x="{cx - 38}" y="120" width="76" height="16" fill="#e2e8f0" stroke="{SLATE}"/>')
        # Tier 2 middle roof
        els.append(f'<polygon points="{cx - 54},136 {cx + 54},136 {cx + 82},152 {cx - 82},152" fill="#334155" stroke="{INK}" stroke-width="1.2"/>')
        els.append(f'<rect x="{cx - 60}" y="152" width="120" height="22" fill="#e2e8f0" stroke="{SLATE}"/>')
        # Horizontal plaque "大观楼"
        els.append(card(cx - 34, 155, 68, 16, rx=3, fill=PLAQUE_BLUE, stroke=GOLD_BRIGHT, sw=1.2))
        els.append(txt(cx, 167, "大 观 楼", size=10.5, color=PLAQUE_TEXT, anchor="middle", weight="700"))
        # Tier 1 lower roof with upturned eaves ("大刀把")
        els.append(f'<polygon points="{cx - 80},174 {cx + 80},174 {cx + 118},192 {cx - 118},192" fill="#334155" stroke="{INK}" stroke-width="1.2"/>')

        # Left pillar in viewer's view = WEST pillar = LOWER couplet (下联)!
        wp_x = cx - 94
        els.append(card(wp_x, 194, 58, 164, rx=5, fill=PLAQUE_BLUE, stroke=GOLD_BRIGHT, sw=1.5))
        els.append(txt(wp_x + 29, 212, "西柱·下联", size=10.2, color="#93c5fd", anchor="middle", weight="700"))
        els.append(txt(wp_x + 29, 232, "数千年往事", size=10.2, color=PLAQUE_TEXT, anchor="middle", weight="600"))
        els.append(txt(wp_x + 29, 250, "注到心头…", size=10.2, color=PLAQUE_TEXT, anchor="middle"))
        els.append(txt(wp_x + 29, 270, "想汉习楼船", size=10.2, color=PLAQUE_TEXT, anchor="middle"))
        els.append(txt(wp_x + 29, 290, "……", size=10.2, color=PLAQUE_TEXT, anchor="middle"))
        els.append(txt(wp_x + 29, 310, "两行秋雁", size=10.2, color=PLAQUE_TEXT, anchor="middle"))
        els.append(txt(wp_x + 29, 330, "一枕清霜", size=10.5, color="#fef08a", anchor="middle", weight="700"))
        els.append(txt(wp_x + 29, 350, "末字“霜”平声", size=9.8, color="#86efac", anchor="middle", weight="700"))

        # Center doorway
        els.append(f'<rect x="{cx - 28}" y="216" width="56" height="142" rx="4" fill="#f8fafc" stroke="{BORDER}"/>')
        els.append(txt(cx, 274, "正门", size=11.0, color=MUTED, anchor="middle", weight="600"))
        els.append(txt(cx, 294, "← 后读", size=10.2, color=ORANGE, anchor="middle", weight="700"))
        els.append(txt(cx, 252, "先读 →", size=10.2, color=BLUE, anchor="middle", weight="700"))

        # Right pillar in viewer's view = EAST pillar = UPPER couplet (上联)!
        ep_x = cx + 36
        els.append(card(ep_x, 194, 58, 164, rx=5, fill=PLAQUE_BLUE, stroke=GOLD_BRIGHT, sw=1.5))
        els.append(txt(ep_x + 29, 212, "东柱·上联", size=10.2, color="#93c5fd", anchor="middle", weight="700"))
        els.append(txt(ep_x + 29, 232, "五百里滇池", size=10.2, color=PLAQUE_TEXT, anchor="middle", weight="600"))
        els.append(txt(ep_x + 29, 250, "奔来眼底…", size=10.2, color=PLAQUE_TEXT, anchor="middle"))
        els.append(txt(ep_x + 29, 270, "看东骧神骏", size=10.2, color=PLAQUE_TEXT, anchor="middle"))
        els.append(txt(ep_x + 29, 290, "……", size=10.2, color=PLAQUE_TEXT, anchor="middle"))
        els.append(txt(ep_x + 29, 310, "九夏芙蓉", size=10.2, color=PLAQUE_TEXT, anchor="middle"))
        els.append(txt(ep_x + 29, 330, "三春杨柳", size=10.5, color="#fef08a", anchor="middle", weight="700"))
        els.append(txt(ep_x + 29, 350, "末字“柳”仄声", size=9.8, color="#fda4af", anchor="middle", weight="700"))

        # Bottom tip inside left card
        els.append(txt(cx, 382, "游客视角：右手东柱为上联（先读），左手西柱为下联（后读）", size=10.3, color=INK, anchor="middle", weight="700"))
        els.append(txt(cx, 402, "每块木匾内部竖排亦按传统“自右向左”逐列移目", size=10.2, color=MUTED, anchor="middle"))

        # Right card: Breathing & Rhythm Metronome for unpunctuated text (x=384..740)
        rx, ry, rw, rh = 384, 64, 356, 356
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 16, ry + 24, "② 原匾零标点：五步“领字换气法”当场读通", size=12.4, color=INK, weight="700"))

        beats = [
            ("第 1 拍｜5·4·4·7 破题", BLUE, BLUE_SOFT, "五百里滇池 / 奔来眼底 / 披襟岸帻 / 喜｜茫茫空阔无边"),
            ("第 2 拍｜1字领 4×4 排比", GREEN, GREEN_SOFT, "看（想）｜XXXX · XXXX · XXXX · XXXX（一口气四顿）"),
            ("第 3 拍｜4·6 舒缓换气", SLATE, SLATE_SOFT, "高人韵士（伟烈丰功）/ 何妨选胜登临（费尽移山心力）"),
            ("第 4 拍｜5·7 隔句对 ×2", PURPLE, PURPLE_SOFT, "趁（尽）XXXXX，XX就（不及）XXXX；（更/便 同构）"),
            ("第 5 拍｜3字领 4×4 余音", GOLD, GOLD_SOFT, "莫辜负（只赢得）｜四万九三（几半两一）四组四言慢收！"),
        ]
        for i, (bhead, bfg, bbg, bbody) in enumerate(beats):
            by_i = ry + 38 + i * 54
            els.append(card(rx + 14, by_i, rw - 28, 46, rx=7, fill=bbg, stroke=bfg, sw=1.0))
            els.append(txt(rx + 24, by_i + 18, bhead, size=10.8, color=bfg, weight="700"))
            els.append(txt(rx + 24, by_i + 36, bbody, size=10.1, color=INK))

        # Historical appraisal box at bottom of right card
        els.append(card(rx + 14, ry + 312, rw - 28, 34, rx=6, fill=SLATE_SOFT, stroke=BORDER))
        els.append(
            txt(
                rx + rw / 2,
                ry + 333,
                "毛泽东评点大观楼长联：“从古未有，别创一格！”",
                size=10.8,
                color=INK,
                anchor="middle",
                weight="700",
            )
        )

        svg = figure(
            432,
            "大观楼蓝底鎏金抱柱长联实景左右读序与无标点五步领字断句指南图",
            "左侧立面图展示面向大观楼正门时右手东柱为上联（末字柳仄收）、左手西柱为下联（末字霜平收）的传统读序；右侧提供五步领字换气口诀，帮助读者在原匾无标点情况下按5-4-4-7、一字领四排、4-6过渡、5-7扇面对、三字领四言轻松断句朗读。",
            els,
        )
        write_svg(SUBDIR, "on-site-reading-guide-card.svg", svg)

    @register(
        "daguanlou-couplet",
        "昆明滇池大观楼180字长联：三幕对称解剖、四山方位全景、汉唐宋元史考、孙阮改联交锋、三百年匾额接力与实景读法",
        "humanities",
    )
    def build_daguanlou_couplet():
        _build_180_architecture_map()
        _build_dianchi_four_totems_panorama()
        _build_four_dynasties_yunnan_epic()
        _build_sun_ranweng_vs_ruan_yuan_duel()
        _build_three_centuries_pavilion_relay()
        _build_on_site_reading_guide_card()


def _register_poetry_boom_7080s():
    SUBDIR = "poetry-boom-7080s"

    def _arrow_defs():
        return (
            "<defs>"
            f'<marker id="arr-b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{BLUE}"/></marker>'
            f'<marker id="arr-p" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{PURPLE}"/></marker>'
            f'<marker id="arr-g" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{GREEN}"/></marker>'
            f'<marker id="arr-o" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{GOLD}"/></marker>'
            "</defs>"
        )

    def _build_five_engines_poetry_boom():
        """SVG 1: Five converging historical, linguistic, and media engines behind the 1970s-80s poetry boom."""
        els = [_arrow_defs()]
        els.extend(
            header(
                "为什么七八十年代全中国都在读诗写诗？五大时代齿轮的咬合",
                "并非那代人天生偏爱分行文字，而是压抑已久的个体情感、思想破冰与单一纸媒聚光灯撞在了同一历史窗口。",
            )
        )

        # Central synthesis banner (y=66..126)
        els.append(card(20, 66, 720, 58, rx=10, fill=PLAQUE_BLUE, stroke=GOLD_BRIGHT, sw=1.6))
        els.append(
            txt(
                380,
                90,
                "核心奇观：1979–1980《诗刊》印数飙至 50 万份 · 万人体育馆诗歌朗诵会座无虚席",
                size=12.6,
                color=PLAQUE_TEXT,
                anchor="middle",
                weight="700",
            )
        )
        els.append(
            txt(
                380,
                111,
                "一首新诗发表即可轰动全国、二三十万张读者选票贴邮票寄回编辑部——五大底层动力缺一不可",
                size=10.5,
                color="#cbd5e1",
                anchor="middle",
            )
        )

        # Row 1: Cards 1 & 2 (y=138..244)
        engines_top = [
            (
                20,
                138,
                352,
                104,
                "1",
                BLUE,
                BLUE_SOFT,
                "高压蓄能与体裁优势：煤油灯下最轻便的容器",
                "约1700万上山下乡知青远离故土，宏大口号容不下私人悲欢；",
                "长篇小说难写难藏，十几行短诗3分钟就能手抄、站岗时默诵。",
                "代表现场：食指1968手抄诗、白洋淀诗群、贵州地下创作",
            ),
            (
                388,
                138,
                352,
                104,
                "2",
                CRIMSON,
                CRIMSON_SOFT,
                "社会功能“超载”：替哲学与社会科学冲锋",
                "1978思想解放初期，现代心理学、社会学与法学尚在重建；",
                "诗歌充当思想轻骑兵，率先把主语从集体“我们”换回独立“我”。",
                "代表现场：《回答》《致橡树》引发全民讨论与“美学热”",
            ),
        ]
        # Row 2: Cards 3 & 4 (y=254..360)
        engines_mid = [
            (
                20,
                254,
                352,
                104,
                "3",
                GOLD,
                GOLD_SOFT,
                "隐秘火种：内部“黄皮书”与现代派译诗滋养",
                "60–70年代内部发行的“黄皮书”流转青年手中，打开异域视野；",
                "80年代现代派译诗井喷、1981《九叶集》重现，重接现代诗艺。",
                "代表养分：波德莱尔、艾略特、洛尔迦、聂鲁达、穆旦等",
            ),
            (
                388,
                254,
                352,
                104,
                "4",
                GREEN,
                GREEN_SOFT,
                "单通道媒介聚光灯：没有电视和网络的时代",
                "70年代末家庭电视罕见，流行乐、摇滚与互联网尚未分流；",
                "邮局订刊+书店排队+广播朗诵聚拢了全国青年的精神带宽。",
                "代表规模：《十月》55万册、《诗刊》50万册、万人朗诵会",
            ),
        ]

        for cx, cy, cw, ch, num, fg, bg, title, l1, l2, tag in engines_top + engines_mid:
            els.append(card(cx, cy, cw, ch, rx=9, fill=CARD_BG, stroke=fg, sw=1.3))
            els.append(step_badge(cx + 22, cy + 22, num, fg=fg, bg=bg, r=11))
            els.append(txt(cx + 40, cy + 26, title, size=11.6, color=fg, weight="700"))
            els.append(txt(cx + 14, cy + 49, l1, size=10.1, color=INK))
            els.append(txt(cx + 14, cy + 67, l2, size=10.1, color=INK))
            els.append(card(cx + 12, cy + 77, cw - 24, 20, rx=4, fill=bg, stroke="none"))
            els.append(txt(cx + 20, cy + 91, tag, size=9.6, color=fg, weight="600"))

        # Row 3: Full-width Engine 5 (y=370..452)
        els.append(card(20, 370, 720, 78, rx=9, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.3))
        els.append(step_badge(42, 392, "5", fg=PURPLE, bg="#ffffff", r=11))
        els.append(
            txt(
                60,
                396,
                "组织放大器：1977恢复高考 + 百所大学校园诗社 + 《诗刊》青春诗会 + 民间诗报网络",
                size=11.8,
                color=PURPLE,
                weight="700",
            )
        )
        els.append(
            txt(
                60,
                418,
                "77/78/79级学子带着社会阅历涌入大学，北大五四文学社、复旦诗社、吉大赤子心、武大浪淘沙等社团星罗棋布；",
                size=10.2,
                color=INK,
            )
        )
        els.append(
            txt(
                60,
                436,
                "上连1980年起被誉为“诗坛黄埔军校”的《诗刊》青春诗会，外接1986年两报“现代诗群体大展”（84个民间社团同台亮相）！",
                size=10.2,
                color=INK,
                weight="600",
            )
        )

        svg = figure(
            462,
            "中国七八十年代诗歌兴起的五大核心原因结构图",
            "剖析七八十年代全民读诗写诗的五重耦合动力：知青时期高压蓄能与短诗易手抄的体裁优势、思想解放期文学替哲学社科冲锋的功能超载、内部黄皮书与外国现代诗译介火种、缺乏电视网络的单一纸媒聚光灯效应，以及恢复高考后高校诗社与青春诗会的组织生态网。",
            els,
        )
        write_svg(SUBDIR, "five-engines-poetry-boom.svg", svg)

    def _build_three_waves_timeline():
        """SVG 2: Four-stage evolution timeline from 1968 hand-copied underground notebooks to 1992 media diversion."""
        els = [_arrow_defs()]
        els.extend(
            header(
                "二十五年四重浪：从煤油灯手抄本到八十四个先锋诗群大展（1968–1992）",
                "读懂“地下潜流 → 朦胧诗破冰 → 第三代裂变 → 九十年代分流”，才不会把七八十年代诗歌看成铁板一块。",
            )
        )

        stages = [
            (
                20,
                "第一浪｜1968–1977",
                "地下手抄本潜流期",
                SLATE,
                SLATE_SOFT,
                [
                    ("1968", "食指写《相信未来》等，", "知青在车站与油灯下传抄"),
                    ("70年代初", "白洋淀诗群（芒克、多多", "等）与贵州黄翔秘密探索"),
                    ("1971–78", "内部“黄皮书”重印流转，", "输入现代派陌生化语感"),
                    ("1976.04", "天安门诗歌运动爆发；", "北岛写下《回答》破土"),
                ],
                "手抄本 · 黄皮书 · 自救",
            ),
            (
                202,
                "第二浪｜1978–1983",
                "破冰与全民大论争",
                BLUE,
                BLUE_SOFT,
                [
                    ("1978.12", "北岛、芒克在北京油印", "创办民刊《今天》贴上墙"),
                    ("1979.03", "官刊《诗刊》发《回答》，", "随后选载舒婷《致橡树》"),
                    ("1980.5–8", "谢冕发声护航；《令人气", "闷的“朦胧”》引爆大论争"),
                    ("1980–83", "首届青春诗会召开；“三", "个崛起”论文确立新美学"),
                ],
                "朦胧诗 · 50万印数 · 崛起",
            ),
            (
                384,
                "第三浪｜1984–1989",
                "高校狂飙与第三代裂变",
                PURPLE,
                PURPLE_SOFT,
                [
                    ("1984–85", "高校诗社沸腾；《他们》", "《非非》《海上》等创刊"),
                    ("1985", "《朦胧诗选》热销全国；", "北大编印《新诗潮诗集》"),
                    ("1986.10", "《诗歌报》《深圳青年报》", "联办大展：84社团同亮相"),
                    ("1984–89", "海子、西川抒情长诗与", "口语派、女性诗多元并立"),
                ],
                "校园诗社 · 口语 · 84社团",
            ),
            (
                566,
                "尾声转折｜1990–1992",
                "余晖热销与大众退潮",
                GOLD,
                GOLD_SOFT,
                [
                    ("1990–91", "“汪国真热”风靡校园，成", "大众手抄诗最后怀旧余晖"),
                    ("1991起", "《现代汉诗》《倾向》创", "刊，转向书斋语言精耕"),
                    ("1992后", "市场潮、彩电、港台流行", "歌与摇滚接管大众抒情"),
                    ("90年代中", "诗集常需自费印千册，诗", "卸下超载重担归于纯文学"),
                ],
                "汪国真热 · 分流 · 归纯粹",
            ),
        ]

        # Top arrow spine connecting the 4 stages (y=76)
        for sx, period, sub, fg, bg, items, foot in stages:
            w = 174
            # Stage header pill
            els.append(card(sx, 66, w, 44, rx=8, fill=fg, stroke="none"))
            els.append(txt(sx + w / 2, 84, period, size=10.6, color="#ffffff", anchor="middle", weight="700"))
            els.append(txt(sx + w / 2, 102, sub, size=11.2, color="#fef08a" if fg != GOLD else "#ffffff", anchor="middle", weight="700"))

            # Main body card (y=118..416)
            els.append(card(sx, 118, w, 298, rx=8, fill=CARD_BG, stroke=fg, sw=1.2))
            for idx, (yr, line1, line2) in enumerate(items):
                iy = 134 + idx * 64
                els.append(card(sx + 8, iy, w - 16, 56, rx=5, fill=bg, stroke="none"))
                els.append(txt(sx + 14, iy + 16, yr, size=9.8, color=fg, weight="700"))
                els.append(txt(sx + 14, iy + 33, line1, size=9.5, color=INK))
                if line2:
                    els.append(txt(sx + 14, iy + 48, line2, size=9.5, color=INK))

            # Stage footer tag
            els.append(txt(sx + w / 2, 405, foot, size=9.2, color=fg, anchor="middle", weight="700"))

        # Connectors between stage headers
        for x_gap in (194, 376, 558):
            els.append(_line(x_gap, 88, x_gap + 8, 88, stroke=INK, sw=1.6))

        # Bottom summary strip (y=424..456)
        els.append(card(20, 424, 720, 30, rx=6, fill=SLATE_SOFT, stroke=BORDER))
        els.append(
            txt(
                380,
                444,
                "演进脉络：70年代靠“手抄本”保住真话火种 → 80年代初靠“朦胧诗”唤醒个体尊严 → 80年代中后期向“多元现代汉语”全面裂变",
                size=10.2,
                color=INK,
                anchor="middle",
                weight="600",
            )
        )

        svg = figure(
            466,
            "1968至1992年中国当代诗歌四阶段演进时间轴",
            "按时间顺序梳理四个关键阶段：1968-1977知青地下手抄本与内部黄皮书潜流期，1978-1983《今天》与《诗刊》互动、朦胧诗大论争及三个崛起破冰期，1984-1989高校诗社与1986现代诗群体大展84社团裂变期，以及1990-1992汪国真余晖与大众媒介分流期。",
            els,
        )
        write_svg(SUBDIR, "three-waves-timeline-1968-1992.svg", svg)

    def _build_pronoun_and_imagery_shift():
        """SVG 3: Linguistic & aesthetic X-ray comparing Collective 'We', Misty 'Awakened I', and 3rd-Gen 'Everyday Body'."""
        els = []
        els.extend(
            header(
                "几行诗凭什么让人热泪盈眶？从“高音喇叭”到“觉醒之我”的语言革命",
                "读懂七八十年代诗歌冲击力，最直观的钥匙是看主语代词、核心意象与说话姿态发生了怎样剧烈的翻转。",
            )
        )

        cols = [
            (
                20,
                "旧惯性｜传声筒式的“大我”",
                "60年代末–70年代中主流范式",
                SLATE,
                SLATE_SOFT,
                [
                    ("主语人称", "“我们 / 亿万人民 / 战友”", "个体“小我”必须隐身或作检讨"),
                    ("高频意象", "红日 · 东风 · 战旗 · 炉火", "高度统一的公共政治象征符号库"),
                    ("句式声调", "感叹号密集 · 祈使口号句", "居高临下的广场齐声朗诵腔"),
                    ("情感边界", "只许写昂扬斗志与集体颂歌", "私人孤独、迷惘与爱情被视作小资"),
                    ("读者体验", "被动仰视与跟读，千篇一面", "真实的生活痛感在纸面上找不到出口"),
                ],
            ),
            (
                266,
                "第一变｜归来者与朦胧诗“觉醒之我”",
                "70年代地下潜流 → 1978–1984主潮",
                BLUE,
                BLUE_SOFT,
                [
                    ("主语人称", "独立的“我”与平等的“你”", "个人良知、怀疑权利与独立人格归来"),
                    ("高频意象", "黑夜与眼睛 · 橡树与木棉 · 礁石", "用自然与生命隐喻折射历史创伤与尊严"),
                    ("句式声调", "复调追问 · 通感 · 错位蒙太奇", "沉思、悲悯而富于张力的心灵独白"),
                    ("情感边界", "直面历史伤痕、信仰重建与独立爱情", "拒绝依附攀援，宣告“木棉作为树的形象”"),
                    ("读者体验", "灵魂击穿感：“替我说出了憋十年的话！”", "电台一播有人捏裂收音机，手抄本疯传全国"),
                ],
            ),
            (
                512,
                "第二变｜第三代“日常肉身与口语”",
                "1984–1989先锋裂变期",
                GREEN,
                GREEN_SOFT,
                [
                    ("主语人称", "街头凡人“我 / 他 / 某个人”", "主动走下英雄纪念碑，还原世俗普通人"),
                    ("高频意象", "大雁塔台阶 · 茶馆 · 街道 · 苹果", "剥去崇高光环，直写日常器物与凡俗现场"),
                    ("句式声调", "冷峻口语 · 反讽叙事 · 语感实验", "消解隐喻深度，追求现代汉语自身弹性"),
                    ("情感边界", "调侃宏大叙事、书写都市青年个体经验", "同代还并存海子等“麦地与太阳”神性长诗"),
                    ("读者体验", "大学诗社与民刊圈层狂飙突进", "审美迅速专业化，与大众广场朗诵渐行渐远"),
                ],
            ),
        ]

        for cx, ctitle, csub, fg, bg, rows in cols:
            cw = 228
            els.append(card(cx, 66, cw, 48, rx=8, fill=fg, stroke="none"))
            els.append(txt(cx + cw / 2, 86, ctitle, size=11.0, color="#ffffff", anchor="middle", weight="700"))
            els.append(txt(cx + cw / 2, 104, csub, size=9.6, color="#e2e8f0", anchor="middle"))

            els.append(card(cx, 120, cw, 316, rx=8, fill=CARD_BG, stroke=fg, sw=1.2))
            for r_idx, (r_label, r_main, r_sub) in enumerate(rows):
                ry = 132 + r_idx * 60
                els.append(card(cx + 8, ry, cw - 16, 52, rx=5, fill=bg, stroke="none"))
                els.append(txt(cx + 14, ry + 16, f"【{r_label}】", size=9.5, color=fg, weight="700"))
                els.append(txt(cx + 14, ry + 32, r_main, size=9.8, color=INK, weight="700"))
                els.append(txt(cx + 14, ry + 46, r_sub, size=9.0, color=MUTED))

        svg = figure(
            450,
            "中国七八十年代诗歌三阶段人称、意象与审美姿态对比图",
            "横向对比三种诗歌语言范式：旧式传声筒以集体“我们”和红日战旗口号压抑私人情感；归来者与朦胧诗恢复独立思考的“我”与平等“你”，借黑夜眼睛、橡树木棉等意象击穿千万读者的心灵积郁；80年代中后期第三代诗进一步转向日常口语、反崇高与现代汉语实验。",
            els,
        )
        write_svg(SUBDIR, "pronoun-and-imagery-shift.svg", svg)

    def _build_media_spotlight_print_runs():
        """SVG 4: Quantitative bar chart of 1979-1981 print runs vs 1980/1995 youth attention bandwidth."""
        els = []
        els.extend(
            header(
                "没有电视机和互联网的年代，一本诗刊能印多少册？",
                "左图按真实文献数据等比例绘制1979–1981年峰值印数；右图解释“单通道纸媒聚光灯”如何形成。",
            )
        )

        # Left card: True-to-scale horizontal bar chart (x=20..418, y=66..430)
        lx, ly, lw, lh = 20, 66, 398, 364
        els.append(card(lx, ly, lw, lh))
        els.append(txt(lx + 16, ly + 24, "① 真实史料：80年代初文学/诗歌印数 vs 90年代对比", size=11.6, color=INK, weight="700"))
        els.append(txt(lx + 16, ly + 42, "横轴比例尺：0 — 60 万册（严格按数值线性换算条长）", size=9.6, color=MUTED))

        # Scale: x0 = 166, max_val = 60.0 -> max_w = 198px (3.3 px per 10k copies)
        x0 = lx + 146  # 166
        scale = 3.3  # 60 * 3.3 = 198 -> ends at 364

        # Gridlines for 0, 20, 40, 60 万
        for gv in (0, 20, 40, 60):
            gx = x0 + gv * scale
            els.append(_line(gx, ly + 56, gx, ly + 316, stroke="#e2e8f0", sw=1.0, dash="3 3" if gv > 0 else None))
            els.append(txt(gx, ly + 332, f"{gv}万", size=9.2, color=MUTED, anchor="middle"))

        bars = [
            ("《十月》1981年第1期", "光明日报载王世敏实录", 55.0, BLUE, "55 万册"),
            ("《诗刊》1979–80峰值", "编辑部主任王燕生口述", 50.0, CRIMSON, "50 万册"),
            ("《收获》80年代初均印", "大型文学双月刊代表", 35.0, PURPLE, "约35 万册"),
            ("《诗刊》单次评选选票", "读者贴邮票寄回20–30万", 25.0, GOLD, "约25 万张"),
            ("90年代中期先锋诗集", "如1994昌耀自费预约本", 0.1, SLATE, "0.1 万册(千册)"),
        ]

        for i, (bname, bsrc, val, bcol, blabel) in enumerate(bars):
            by = ly + 66 + i * 50
            bw = max(val * scale, 2.5)
            els.append(txt(x0 - 8, by + 13, bname, size=10.0, color=INK, anchor="end", weight="700"))
            els.append(txt(x0 - 8, by + 27, bsrc, size=8.8, color=MUTED, anchor="end"))
            els.append(f'<rect x="{x0:.1f}" y="{by + 4:.1f}" width="{bw:.1f}" height="22" rx="4" fill="{bcol}"/>')
            els.append(txt(x0 + bw + 6, by + 19, blabel, size=9.8, color=bcol, weight="700"))

        els.append(card(lx + 14, ly + 340, lw - 28, 18, rx=4, fill=SLATE_SOFT, stroke="none"))
        els.append(txt(lx + lw / 2, ly + 353, "注：1本期刊常在宿舍/工厂传阅十余人，实际触达读者远超印数本身", size=9.1, color=INK, anchor="middle"))

        # Right card: Attention Bandwidth Comparison 1980 vs 1995 (x=432..740, y=66..430)
        rx, ry, rw, rh = 432, 66, 308, 364
        els.append(card(rx, ry, rw, rh))
        els.append(txt(rx + 16, ry + 24, "② 青年精神娱乐带宽流向对比", size=11.6, color=INK, weight="700"))

        # Top sub-card: ~1980 Single-Channel Spotlight
        els.append(card(rx + 12, ry + 38, rw - 24, 152, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.2))
        els.append(txt(rx + 22, ry + 58, "1980年前后：单通道超级聚光灯", size=10.8, color=BLUE, weight="700"))
        els.append(txt(rx + 22, ry + 78, "• 电视机：1978全国保有量极少，多为单位公看", size=9.6, color=INK))
        els.append(txt(rx + 22, ry + 95, "• 流行歌：录音机与港台磁带刚刚零星传入", size=9.6, color=INK))
        els.append(txt(rx + 22, ry + 112, "• 网络与影院：零互联网，娱乐选择极度稀缺", size=9.6, color=INK))
        els.append(card(rx + 20, ry + 124, rw - 40, 56, rx=5, fill="#ffffff", stroke=BLUE, sw=0.9))
        els.append(txt(rx + rw / 2, ry + 144, "结果：全社会青年的求知、恋爱与迷惘", size=9.8, color=BLUE, anchor="middle", weight="700"))
        els.append(txt(rx + rw / 2, ry + 162, "高度浓缩在【邮局订诗刊+校园朗诵+手抄本】！", size=9.6, color=INK, anchor="middle", weight="600"))

        # Bottom sub-card: ~1995 Multi-Channel Diversion
        els.append(card(rx + 12, ry + 202, rw - 24, 150, rx=8, fill=GOLD_SOFT, stroke=GOLD, sw=1.2))
        els.append(txt(rx + 22, ry + 222, "1995年前后：多媒介大坝全面开闸", size=10.8, color=GOLD, weight="700"))
        els.append(txt(rx + 22, ry + 242, "• 电视普及：城镇百户彩电超百台，农村逾50台", size=9.6, color=INK))
        els.append(txt(rx + 22, ry + 259, "• 声画分流：港台流行情歌、摇滚、录像厅、KTV", size=9.6, color=INK))
        els.append(txt(rx + 22, ry + 276, "• 阅读分流：金庸武侠、周末报刊、经商社科热书", size=9.6, color=INK))
        els.append(card(rx + 20, ry + 288, rw - 40, 54, rx=5, fill="#ffffff", stroke=GOLD, sw=0.9))
        els.append(txt(rx + rw / 2, ry + 307, "结果：并不是年轻人不再需要浪漫与追问，", size=9.6, color=GOLD, anchor="middle", weight="700"))
        els.append(txt(rx + rw / 2, ry + 325, "而是情绪被流行歌词、影视与新媒介分流了。", size=9.6, color=INK, anchor="middle", weight="600"))

        svg = figure(
            444,
            "1980年代初诗歌与文学期刊发行量实录及媒介注意力分流对比图",
            "左侧条形图按真实史料比例对比1981年《十月》55万册、1979-1980年《诗刊》50万册、《收获》约35万册、《诗刊》读者选票约25万张与1990年代中期自费诗集1000册；右侧对比1980年前后无电视无网络的单一纸媒聚光灯效应与1995年后彩电、流行音乐及大众文化的多渠道分流。",
            els,
        )
        write_svg(SUBDIR, "media-spotlight-print-runs.svg", svg)

    def _build_underground_to_campus_relay():
        """SVG 5: Five-station transmission relay from Yellow-Cover translations & notebooks to 84 modernist groups (with 1-shot accessible CSS animation)."""
        els = [_arrow_defs()]

        # Subtle 1-shot sequential pulse across stations 1 -> 5 (total ~6s, ends cleanly in static full-visibility state)
        anim_style = """<style>
  @keyframes stationGlow {
    0%   { stroke-width: 1.3; filter: none; }
    35%  { stroke-width: 3.0; filter: drop-shadow(0 2px 6px rgba(37,99,235,0.28)); }
    100% { stroke-width: 1.6; filter: none; }
  }
  @keyframes sparkTravel {
    0%   { stroke-dashoffset: 620; opacity: 0.25; }
    15%  { opacity: 1; }
    100% { stroke-dashoffset: 0; opacity: 0.9; }
  }
  .relay-track {
    stroke-dasharray: 620;
    stroke-dashoffset: 0;
    animation: sparkTravel 4.8s ease-out 0.2s 1 both;
  }
  .st-1 { animation: stationGlow 1.1s ease-out 0.1s 1 both; }
  .st-2 { animation: stationGlow 1.1s ease-out 1.1s 1 both; }
  .st-3 { animation: stationGlow 1.1s ease-out 2.1s 1 both; }
  .st-4 { animation: stationGlow 1.1s ease-out 3.1s 1 both; }
  .st-5 { animation: stationGlow 1.2s ease-out 4.1s 1 both; }
  @media (prefers-reduced-motion: reduce) {
    .relay-track, .st-1, .st-2, .st-3, .st-4, .st-5 {
      animation: none !important;
      stroke-dashoffset: 0 !important;
      opacity: 1 !important;
      filter: none !important;
    }
  }
</style>"""
        els.append(anim_style)

        els.extend(
            header(
                "一粒火种怎样燎原全国？新诗潮“五级传播接力网”（1962–1986）",
                "从内部译本与煤油灯手抄本起步，经民刊与官刊罕见共振，最终在大学校园与全国诗报完成裂变。",
            )
        )

        # Serpentine 5-station relay: Top row (Stations 1, 2, 3), Bottom row (Stations 4, 5 wide)
        # Relay connector path behind cards
        els.append(
            f'<path class="relay-track" d="M 130 165 L 380 165 L 630 165 L 630 330 L 220 330" '
            f'fill="none" stroke="{GOLD_BRIGHT}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
        )

        top_stations = [
            (
                20,
                74,
                228,
                172,
                "st-1",
                "1",
                GOLD,
                GOLD_SOFT,
                "源头译介与先驱暗流",
                "1962–78 内部“黄皮书” + 九叶派",
                "• 人文社内部印行《麦田里的守望者》",
                "  《等待戈多》及苏东现代派译作",
                "• 穆旦等40年代现代诗传统暗中存续，",
                "  1981《九叶集》出版完成隔代重逢",
            ),
            (
                266,
                74,
                228,
                172,
                "st-2",
                "2",
                SLATE,
                SLATE_SOFT,
                "知青点手抄本秘密流转",
                "1968–1977 跨省人际传抄网",
                "• 知青探亲、串联在火车站手抄接力",
                "• 食指诗作、白洋淀诗群（芒克、多多、",
                "  根子）打破“假大空”口号垄断",
                "• 证明现代汉语完全能安放真实灵魂",
            ),
            (
                512,
                74,
                228,
                172,
                "st-3",
                "3",
                BLUE,
                BLUE_SOFT,
                "油印民刊 × 国家级官刊破壁",
                "1978–1981 罕见的官民双向共振",
                "• 北岛带油印《今天》去《诗刊》编辑部，",
                "  编辑一页页贴墙阅读并选发《致橡树》",
                "• 《福建文艺》《安徽文学》等地方刊物",
                "  连开专栏，把新诗推向50万级大众视野",
            ),
        ]

        for sx, sy, sw, sh, cls, snum, fg, bg, stitle, sdate, b1, b2, b3, b4 in top_stations:
            els.append(f'<rect class="{cls}" x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="9" fill="{CARD_BG}" stroke="{fg}" stroke-width="1.5"/>')
            els.append(step_badge(sx + 20, sy + 22, snum, fg=fg, bg=bg, r=11))
            els.append(txt(sx + 38, sy + 26, stitle, size=11.2, color=fg, weight="700"))
            els.append(card(sx + 10, sy + 38, sw - 20, 20, rx=4, fill=bg, stroke="none"))
            els.append(txt(sx + 16, sy + 52, sdate, size=9.4, color=fg, weight="700"))
            els.append(txt(sx + 12, sy + 76, b1, size=9.5, color=INK))
            els.append(txt(sx + 12, sy + 94, b2, size=9.5, color=INK))
            els.append(txt(sx + 12, sy + 116, b3, size=9.5, color=INK))
            els.append(txt(sx + 12, sy + 134, b4, size=9.5, color=INK))

        # Arrows between top stations (1->2, 2->3) and down from 3->4
        els.append(_line(248, 160, 264, 160, stroke=BLUE, sw=1.8, marker="arr-b"))
        els.append(_line(494, 160, 510, 160, stroke=BLUE, sw=1.8, marker="arr-b"))
        els.append(_line(626, 246, 626, 266, stroke=PURPLE, sw=1.8, marker="arr-p"))

        # Bottom row: Station 4 (Right: 1977 Gaokao Campus Clubs + Youth Poetry Conference, x=392..740) -> left arrow -> Station 5 (Left: 1986 84-Group Exhibition, x=20..368)
        # Wait: reading left-to-right on bottom row is even cleaner and avoids reverse reading! Let's check: if track goes 626,246 -> down to 256 -> across to 194,256 -> down to 270, then Station 4 is on the LEFT (x=20..368) and Station 5 is on the RIGHT (x=392..740)! That reads naturally Left->Right on BOTH rows!
        # Let's overwrite the track cleanly below by placing Station 4 at Left (x=20..370) and Station 5 at Right (x=390..740)!
        els.pop()  # remove vertical arrow at 626
        # Replace relay-track path with clean Z-shape (Row 1 L->R, diagonal/step down to Row 2 L->R)
        for idx_e, el_str in enumerate(els):
            if 'class="relay-track"' in el_str:
                els[idx_e] = (
                    f'<path class="relay-track" d="M 134 160 L 626 160 L 626 258 L 195 258 L 195 344 L 565 344" '
                    f'fill="none" stroke="{GOLD_BRIGHT}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
                )
                break
        els.append(_line(195, 258, 195, 270, stroke=PURPLE, sw=1.8, marker="arr-p"))
        els.append(_line(370, 348, 388, 348, stroke=GREEN, sw=1.8, marker="arr-g"))

        bottom_stations = [
            (
                20,
                272,
                350,
                148,
                "st-4",
                "4",
                PURPLE,
                PURPLE_SOFT,
                "高考恢复与“高校诗社 + 青春诗会”孵化器",
                "1977恢复高考 · 1980《诗刊》首届青春诗会",
                "• 77/78级学子涌入高校，北大五四文学社、复旦诗社、吉大赤子心等",
                "  数百个校园诗社自办油印诗刊、举办万人级露天与礼堂朗诵会；",
                "• 1980年7月《诗刊》创办“青春诗会”（舒婷、顾城、江河、梁小斌、",
                "  徐敬亚等17人首届入选），形成发现青年诗人的“黄埔军校”。",
            ),
            (
                390,
                272,
                350,
                148,
                "st-5",
                "5",
                GREEN,
                GREEN_SOFT,
                "民间社团井喷与两报“现代诗群体大展”",
                "1985–1986 全国先锋诗歌网络大合流",
                "• 老诗人牛汉主持《中国》、严阵创办《诗歌报》、骆一禾编《十月》",
                "  诗歌栏，与民间《他们》《非非》《海上》形成跨省联动；",
                "• 1986年10月《诗歌报》与《深圳青年报》联办现代诗群体大展，",
                "  一次性集中展示 84 个民间现代诗社团，将诗歌潮推向多元巅峰！",
            ),
        ]

        for sx, sy, sw, sh, cls, snum, fg, bg, stitle, sdate, b1, b2, b3, b4 in bottom_stations:
            els.append(f'<rect class="{cls}" x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="9" fill="{CARD_BG}" stroke="{fg}" stroke-width="1.5"/>')
            els.append(step_badge(sx + 20, sy + 22, snum, fg=fg, bg=bg, r=11))
            els.append(txt(sx + 38, sy + 26, stitle, size=11.4, color=fg, weight="700"))
            els.append(card(sx + 12, sy + 38, sw - 24, 20, rx=4, fill=bg, stroke="none"))
            els.append(txt(sx + 18, sy + 52, sdate, size=9.4, color=fg, weight="700"))
            els.append(txt(sx + 14, sy + 76, b1, size=9.6, color=INK))
            els.append(txt(sx + 14, sy + 94, b2, size=9.6, color=INK))
            els.append(txt(sx + 14, sy + 114, b3, size=9.6, color=INK))
            els.append(txt(sx + 14, sy + 132, b4, size=9.6, color=INK, weight="600"))

        # Accessibility / static-readability note at bottom
        els.append(
            txt(
                380,
                440,
                "注：金色轨迹单次演示火种自①至⑤的传递次序并定格于终态；开启系统“减少动态效果”时自动转为纯静态展示。",
                size=9.4,
                color=MUTED,
                anchor="middle",
            )
        )

        svg = figure(
            454,
            "1962至1986年中国新诗潮从内部译本与地下手抄本到全国高校诗社及现代诗大展的五级传播接力图",
            "按传播次序展示五级接力网络：①内部黄皮书译本与九叶派暗流提供现代语言养分；②知青手抄本跨省秘密流转；③民刊《今天》与官刊《诗刊》及地方文学刊物双向共振破壁；④1977恢复高考后的大学校园诗社与1980《诗刊》青春诗会孵化人才；⑤1986年两报现代诗群体大展汇集84个民间社团。",
            els,
        )
        write_svg(SUBDIR, "underground-to-campus-relay.svg", svg)

    def _build_why_poetry_cooled_1990s():
        """SVG 6: Why the mass poetry fever ebbed in the 1990s — External unloading + Internal specialization."""
        els = [_arrow_defs()]
        els.extend(
            header(
                "九十年代诗歌为什么突然“降温”？不是诗死了，而是卸下了千斤重担",
                "当社会科学恢复、电视与流行音乐普及，诗歌不再替整个社会充当唯一的扩音器与情绪出口。",
            )
        )

        # Left column: External Social & Media Unloading (x=20..370, y=66..356)
        lx, ly, lw, lh = 20, 66, 350, 288
        els.append(card(lx, ly, lw, lh, rx=9, fill=CARD_BG, stroke=BLUE, sw=1.3))
        els.append(card(lx, ly, lw, 40, rx=9, fill=BLUE, stroke="none"))
        els.append(txt(lx + lw / 2, ly + 25, "外部推力｜三大超载职能被专业渠道接管", size=11.4, color="#ffffff", anchor="middle", weight="700"))

        ext_items = [
            ("思想启蒙移交社科", BLUE, BLUE_SOFT, "经济学、法学、社会学、心理学专著大批出版，公众讨论改革与人性不再只能借几行诗隐喻。"),
            ("青春抒情移交声画", GOLD, GOLD_SOFT, "彩电普及、邓丽君与港台流行歌、崔健摇滚、KTV与影视剧，更直接地承接了大众恋爱与伤感。"),
            ("市场化与出版转型", SLATE, SLATE_SOFT, "90年代商品经济潮起、期刊补贴退坡、民刊受限，除“汪国真热”短暂余晖外，纯诗集印数回落。"),
        ]
        for idx, (etitle, efg, ebg, ebody) in enumerate(ext_items):
            ey = ly + 52 + idx * 76
            els.append(card(lx + 12, ey, lw - 24, 66, rx=6, fill=ebg, stroke="none"))
            els.append(txt(lx + 20, ey + 19, f"• {etitle}", size=10.4, color=efg, weight="700"))
            els.append(txt(lx + 20, ey + 38, ebody[:22], size=9.6, color=INK))
            els.append(txt(lx + 20, ey + 54, ebody[22:], size=9.6, color=INK))

        # Right column: Internal Poetic Turn to Craft (x=390..740, y=66..356)
        rx, ry, rw, rh = 390, 66, 350, 288
        els.append(card(rx, ry, rw, rh, rx=9, fill=CARD_BG, stroke=PURPLE, sw=1.3))
        els.append(card(rx, ry, rw, 40, rx=9, fill=PURPLE, stroke="none"))
        els.append(txt(rx + rw / 2, ry + 25, "内部拉力｜诗人主动走下广场，回归语言工坊", size=11.4, color="#ffffff", anchor="middle", weight="700"))

        int_items = [
            ("警惕广场口号与煽情", PURPLE, PURPLE_SOFT, "经历80年代狂飙后，先锋诗人自觉反思宏大代言姿态，转向冷静、节制的“个人化写作”。"),
            ("深耕“现代汉诗”尺度", GREEN, GREEN_SOFT, "《现代汉诗》《倾向》《发现》等刊强调“语言的劳作”、叙事性与智性难度，拒绝迎合通俗朗诵。"),
            ("阅读圈层自然分流", CRIMSON, CRIMSON_SOFT, "如同现代交响乐或纯数学，高密度语言实验提高了阅读门槛，受众从千万大众收缩为专业知音。"),
        ]
        for idx, (ititle, ifg, ibg, ibody) in enumerate(int_items):
            iy = ry + 52 + idx * 76
            els.append(card(rx + 12, iy, rw - 24, 66, rx=6, fill=ibg, stroke="none"))
            els.append(txt(rx + 20, iy + 19, f"• {ititle}", size=10.4, color=ifg, weight="700"))
            els.append(txt(rx + 20, iy + 38, ibody[:22], size=9.6, color=INK))
            els.append(txt(rx + 20, iy + 54, ibody[22:], size=9.6, color=INK))

        # Converging arrows to bottom conclusion banner
        els.append(_line(195, 354, 290, 372, stroke=BLUE, sw=1.6, marker="arr-b"))
        els.append(_line(565, 354, 470, 372, stroke=PURPLE, sw=1.6, marker="arr-p"))

        # Bottom conclusion banner (y=374..432)
        els.append(card(20, 374, 720, 56, rx=9, fill=PLAQUE_BLUE, stroke=GOLD_BRIGHT, sw=1.5))
        els.append(
            txt(
                380,
                397,
                "历史诊断：八十年代全民读诗，是万千时代情绪挤过一道窄门的特殊奇观；",
                size=11.2,
                color=PLAQUE_TEXT,
                anchor="middle",
                weight="700",
            )
        )
        els.append(
            txt(
                380,
                417,
                "九十年代诗歌退居安静角落，恰恰见证了中国社会打开百扇窗户后的多元与成熟。",
                size=10.4,
                color="#cbd5e1",
                anchor="middle",
            )
        )

        svg = figure(
            442,
            "1990年代中国诗歌大众热潮退却的内外双因素结构解析图",
            "从外部社会分流与内部诗学转向两方面解析90年代诗歌降温：外部因社科重建、彩电与流行音乐普及以及市场化转型，接管了诗歌超载的启蒙与大众抒情功能；内部因诗人转向个人化写作与现代汉诗语言深耕，使新诗从广场扩音器回归常态纯文学位置。",
            els,
        )
        write_svg(SUBDIR, "why-poetry-cooled-1990s.svg", svg)

    @register(
        "poetry-boom-7080s",
        "中国七八十年代诗歌兴起原因：五大时代引擎、四浪演进时间轴、人称意象革命、50万印数聚光灯、五级传播接力与90年代退潮解析",
        "humanities",
    )
    def build_poetry_boom_7080s():
        _build_five_engines_poetry_boom()
        _build_three_waves_timeline()
        _build_pronoun_and_imagery_shift()
        _build_media_spotlight_print_runs()
        _build_underground_to_campus_relay()
        _build_why_poetry_cooled_1990s()


def _register_european_name_patterns():
    SUBDIR = "european-name-patterns"

    def _arrow_defs():
        return (
            "<defs>"
            f'<marker id="en-arr-b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{BLUE}"/></marker>'
            f'<marker id="en-arr-o" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{ORANGE}"/></marker>'
            f'<marker id="en-arr-g" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{GREEN}"/></marker>'
            f'<marker id="en-arr-p" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{PURPLE}"/></marker>'
            "</defs>"
        )

    def _build_patronymic_atlas():
        """SVG 1: Four-quadrant European patronymic & regional suffix atlas."""
        els = []
        els.extend(
            header(
                "全欧洲都在喊“某某家的娃”：四大片区父名与族裔词缀速查图",
                "把各国拼写“儿子 / 后代”的后缀排成四宫格，九成陌生欧洲姓氏第一眼就能锁定语系与国别。",
            )
        )

        quads = [
            (
                20,
                64,
                352,
                210,
                "1",
                "北欧日耳曼区｜单 s、双 s 与冰岛活化石",
                BLUE,
                BLUE_SOFT,
                [
                    ("丹麦 / 挪威 -sen", "Eriksen · Sørensen · Ødegaard（配 ø / æ）"),
                    ("瑞典 -sson（双 s）", "Andersson · Johansson + 自然姓 Lindberg"),
                    ("冰岛 -son / -dóttir", "Jónsson(儿) · Jónsdóttir(女) · Jónsbur(中)"),
                    ("关键区分", "冰岛至今不设世袭姓，电话簿按教名排序！"),
                ],
            ),
            (
                388,
                64,
                352,
                210,
                "2",
                "不列颠与凯尔特区｜O'、Mac 与吞音变形",
                GREEN,
                GREEN_SOFT,
                [
                    ("爱尔兰专属 O'", "O'Brien · O'Connor（古爱尔兰语“某之孙”）"),
                    ("苏格兰 / 爱尔兰 Mac", "MacDonald · McGregor（Mc 只是 Mac 缩写）"),
                    ("盎格鲁–诺曼 Fitz-", "Fitzgerald · Fitzroy（古法语 fiz“儿子”）"),
                    ("威尔士 ap 吞音与 -s", "ap Rhys→Price · ap Richard→Pritchard · Jones"),
                ],
            ),
            (
                20,
                288,
                352,
                214,
                "3",
                "斯拉夫四分天下｜看词尾秒辨东南西北",
                PURPLE,
                PURPLE_SOFT,
                [
                    ("俄 / 保 -ov / -ev", "Ivanov（女 Ivanova），俄语中间夹 -ovich"),
                    ("乌克兰 -enko / -uk", "Shevchenko · Mudryk（男女同形，不加 -a）"),
                    ("波兰 / 捷克西支", "波 -ski/-wicz（女 -ska）；捷克女普加 -ová"),
                    ("前南斯拉夫 -ić", "Modrić · Đoković（克/塞/波黑高频，男女不变）"),
                ],
            ),
            (
                388,
                288,
                352,
                214,
                "4",
                "罗曼与爱琴海区｜拉丁尾音与“一尾定一岛”",
                ORANGE,
                ORANGE_SOFT,
                [
                    ("西班牙 -ez vs 葡萄牙 -es", "西 Rodríguez / Pérez ｜ 葡 Rodrigues / Peres"),
                    ("意大利北 -i 南 -o", "中北部多复数 -i（Rossi）· 南部多 -o（Russo）"),
                    ("罗马尼亚 -escu / -eanu", "Popescu（神父之子）· Munteanu（山里人）"),
                    ("希腊半岛岛屿地图", "伯罗奔尼撒 -opoulos · 克里特 -akis · 本都 -idis"),
                ],
            ),
        ]
        assert len(quads) == 4

        for qx, qy, qw, qh, qnum, qtitle, fg, bg, rows in quads:
            assert 20 <= qx and qx + qw <= 740
            els.append(card(qx, qy, qw, qh, rx=9, fill=CARD_BG, stroke=fg, sw=1.4))
            els.append(card(qx, qy, qw, 36, rx=9, fill=bg, stroke="none"))
            els.append(step_badge(qx + 18, qy + 18, qnum, fg=fg, bg="#ffffff", r=10))
            els.append(txt(qx + 35, qy + 23, qtitle, size=11.4, color=fg, weight="700"))

            for idx, (rtag, rdesc) in enumerate(rows):
                ry = qy + 44 + idx * 40
                els.append(card(qx + 10, ry, qw - 20, 34, rx=6, fill="#f8fafc" if idx < 3 else bg, stroke=BORDER if idx < 3 else "none", sw=0.8))
                els.append(txt(qx + 18, ry + 14, rtag, size=10.2, color=fg, weight="700"))
                els.append(txt(qx + 18, ry + 28, rdesc, size=9.9, color=INK))

        svg = figure(
            516,
            "欧洲四大片区父名与族裔姓氏后缀速查图",
            "分四个象限归纳欧洲最具辨识度的父名与地区后缀：①北欧区的丹麦挪威-sen、瑞典双s的-sson与冰岛活态-son/-dóttir/-bur；②凯尔特与英伦区的爱尔兰O'、苏爱共用的Mac/Mc、诺曼Fitz-及威尔士ap吞音；③斯拉夫四支的俄保-ov、乌克兰-enko、波兰-ski、捷克-ová与前南-ić；④罗曼与希腊区的西-ez葡-es、意北-i南-o、罗马尼亚-escu与希腊岛屿后缀。",
            els,
        )
        write_svg(SUBDIR, "patronymic-atlas-europe.svg", svg)

    def _build_iceland_iberian_family_relay():
        """SVG 2: Animated 1-shot kinship relay comparing Iceland's per-generation patronymics vs Spain/Portugal mirrored double surnames."""
        els = [_arrow_defs()]
        anim_css = """<style>
  @keyframes enFlowDraw {
    0%   { stroke-dashoffset: 140; opacity: 0.25; }
    100% { stroke-dashoffset: 0; opacity: 1; }
  }
  @keyframes enCardPop {
    0%   { opacity: 0.28; }
    100% { opacity: 1; }
  }
  .en-flow-1 { stroke-dasharray: 140; stroke-dashoffset: 0; animation: enFlowDraw 1.4s ease-out 0.2s 1 both; }
  .en-flow-2 { stroke-dasharray: 140; stroke-dashoffset: 0; animation: enFlowDraw 1.4s ease-out 1.4s 1 both; }
  .en-kid-1  { animation: enCardPop 1.0s ease-out 1.1s 1 both; }
  .en-kid-2  { animation: enCardPop 1.0s ease-out 2.3s 1 both; }
  @media (prefers-reduced-motion: reduce) {
    .en-flow-1, .en-flow-2, .en-kid-1, .en-kid-2 {
      animation: none !important;
      stroke-dashoffset: 0 !important;
      opacity: 1 !important;
    }
  }
</style>"""
        els.append(anim_css)

        els.extend(
            header(
                "一家四口四个姓 vs 父母双姓大翻转：冰岛与西葡传姓推演图",
                "左图看冰岛如何每代按父母教名重算尾缀；右图对比西班牙与葡萄牙恰好相反的“父姓 / 母姓”排位。",
            )
        )

        # Left Panel: Iceland Personal Names Act No. 45/1996 + 2019 Act No. 80/2019
        lx, ly, lw, lh = 20, 64, 352, 408
        els.append(card(lx, ly, lw, lh, rx=9, fill=CARD_BG, stroke=BLUE, sw=1.4))
        els.append(card(lx, ly, lw, 36, rx=9, fill=BLUE, stroke="none"))
        els.append(txt(lx + lw / 2, ly + 23, "① 冰岛活态父/母名制（第 45/1996 号与 2019 法案）", size=11.0, color="#ffffff", anchor="middle", weight="700"))

        # Parents boxes
        els.append(card(lx + 12, ly + 48, 158, 56, rx=7, fill=BLUE_SOFT, stroke=BLUE, sw=1.1))
        els.append(txt(lx + 20, ly + 66, "父亲（Einar 之子）", size=9.6, color=BLUE, weight="700"))
        els.append(txt(lx + 20, ly + 84, "Jón Einarsson", size=11.0, color=INK, weight="700"))
        els.append(txt(lx + 20, ly + 98, "核心教名：Jón → 属格 Jóns-", size=9.2, color=MUTED))

        els.append(card(lx + 182, ly + 48, 158, 56, rx=7, fill=SLATE_SOFT, stroke=SLATE, sw=1.0))
        els.append(txt(lx + 190, ly + 66, "母亲（婚后不改夫姓！）", size=9.6, color=SLATE, weight="700"))
        els.append(txt(lx + 190, ly + 84, "Sigríður Pálsdóttir", size=10.6, color=INK, weight="700"))
        els.append(txt(lx + 190, ly + 98, "也可取母名属格 Sigríðar-", size=9.2, color=MUTED))

        # Animated connector lines from father's given name Jón down to rule pill & children
        els.append(
            f'<path class="en-flow-1" d="M {lx + 91:.1f} {ly + 104:.1f} L {lx + 91:.1f} {ly + 128:.1f} L {lx + 176:.1f} {ly + 128:.1f} L {lx + 176:.1f} {ly + 144:.1f}" '
            f'fill="none" stroke="{BLUE}" stroke-width="2.0" marker-end="url(#en-arr-b)"/>'
        )
        els.append(card(lx + 24, ly + 146, lw - 48, 28, rx=6, fill=BLUE_SOFT, stroke=BLUE, sw=1.0))
        els.append(txt(lx + lw / 2, ly + 164, "拼合公式：孩子教名 + Jóns（父名属格）+ son / dóttir / bur", size=9.8, color=BLUE, anchor="middle", weight="700"))

        els.append(
            f'<path class="en-flow-2" d="M {lx + 176:.1f} {ly + 174:.1f} L {lx + 176:.1f} {ly + 194:.1f}" '
            f'fill="none" stroke="{BLUE}" stroke-width="2.0" marker-end="url(#en-arr-b)"/>'
        )

        # 3 Children outcomes
        kids = [
            ("儿子（男后缀 -son）", "Ólafur Jónsson", "意为“Jón 的儿子 Ólafur”", BLUE, BLUE_SOFT),
            ("女儿（女后缀 -dóttir）", "Helga Jónsdóttir", "意为“Jón 的女儿 Helga”", PURPLE, PURPLE_SOFT),
            ("中性（2019 新增 -bur）", "Alex Jónsbur", "性别自主法新增“Jón 之孩”", GREEN, GREEN_SOFT),
        ]
        for k_i, (krole, kname, kmean, kfg, kbg) in enumerate(kids):
            ky = ly + 198 + k_i * 44
            els.append(f'<g class="en-kid-1">' + card(lx + 14, ky, lw - 28, 38, rx=6, fill=kbg, stroke=kfg, sw=1.0) + "</g>")
            els.append(txt(lx + 22, ky + 16, krole, size=9.6, color=kfg, weight="700"))
            els.append(txt(lx + 22, ky + 31, kmean, size=9.3, color=MUTED))
            els.append(txt(lx + lw - 22, ky + 24, kname, size=10.8, color=INK, anchor="end", weight="700"))

        # Bottom Iceland takeaway
        els.append(card(lx + 12, ly + 336, lw - 24, 60, rx=7, fill="#f8fafc", stroke=BORDER))
        els.append(txt(lx + 20, ly + 355, "名场面：一家四口出国住店，护照末栏拼写 4 个全不同！", size=9.8, color=CRIMSON, weight="700"))
        els.append(txt(lx + 20, ly + 373, "• 冰岛人不称“Guðmundsdóttir 女士”，直呼教名 Björk（比约克）", size=9.4, color=INK))
        els.append(txt(lx + 20, ly + 389, "• 全国电话簿与花名册一律按【第一个词（教名）】字母排序", size=9.4, color=INK))

        # Right Panel: Iberia Mirror Flip (Spain vs Portugal)
        rx, ry, rw, rh = 388, 64, 352, 408
        els.append(card(rx, ry, rw, rh, rx=9, fill=CARD_BG, stroke=ORANGE, sw=1.4))
        els.append(card(rx, ry, rw, 36, rx=9, fill=ORANGE, stroke="none"))
        els.append(txt(rx + rw / 2, ry + 23, "② 伊比利亚双姓镜像陷阱（西班牙 vs 葡萄牙）", size=11.0, color="#ffffff", anchor="middle", weight="700"))

        # Subcard A: Spain (Father 1st + Mother 1st)
        els.append(card(rx + 12, ry + 46, rw - 24, 170, rx=8, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.1))
        els.append(txt(rx + 22, ry + 65, "西班牙传统顺序：名 + 【父方第1姓】 + 【母方第1姓】", size=10.2, color=ORANGE, weight="700"))
        els.append(txt(rx + 22, ry + 83, "父：Juan Nadal Homar  ＋  母：Ana Parera Femenías", size=9.6, color=INK))
        els.append(
            f'<path class="en-flow-1" d="M {rx + 176:.1f} {ry + 89:.1f} L {rx + 176:.1f} {ry + 107:.1f}" '
            f'fill="none" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#en-arr-o)"/>'
        )
        els.append(f'<g class="en-kid-1">' + card(rx + 20, ry + 110, rw - 40, 44, rx=6, fill="#ffffff", stroke=ORANGE, sw=1.1) + "</g>")
        els.append(txt(rx + rw / 2, ry + 128, "Rafael  ·  Nadal（父姓★）  ·  Parera（母姓）", size=10.6, color=INK, anchor="middle", weight="700"))
        els.append(txt(rx + rw / 2, ry + 145, "日常简称看【倒数第 2 词】→ 纳达尔（Nadal）！", size=9.6, color=ORANGE, anchor="middle", weight="700"))
        els.append(txt(rx + 22, ry + 172, "• 彩蛋：毕加索全名 Pablo Ruiz Picasso，Ruiz 是父姓，", size=9.3, color=INK))
        els.append(txt(rx + 22, ry + 188, "  他嫌 Ruiz 太普通，才挑母亲的意大利裔姓 Picasso 签名！", size=9.3, color=INK))
        els.append(txt(rx + 22, ry + 205, "• 注：2017.6.30 起西《民事登记法》取消父姓自动优先权", size=9.1, color=MUTED))

        # Subcard B: Portugal / Brazil (Mother + Father)
        els.append(card(rx + 12, ry + 226, rw - 24, 170, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.1))
        els.append(txt(rx + 22, ry + 245, "葡萄牙 / 巴西顺序：名 + 【母方姓】 + 【父方主姓】", size=10.2, color=GREEN, weight="700"))
        els.append(txt(rx + 22, ry + 263, "母系姓：dos Santos（排前） ＋ 父系姓：Aveiro（压轴）", size=9.6, color=INK))
        els.append(
            f'<path class="en-flow-2" d="M {rx + 176:.1f} {ry + 269:.1f} L {rx + 176:.1f} {ry + 287:.1f}" '
            f'fill="none" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#en-arr-g)"/>'
        )
        els.append(f'<g class="en-kid-2">' + card(rx + 14, ry + 290, rw - 28, 46, rx=6, fill="#ffffff", stroke=GREEN, sw=1.1) + "</g>")
        els.append(txt(rx + rw / 2, ry + 308, "Cristiano Ronaldo(双名) · dos Santos(母) · Aveiro(父★)", size=9.2, color=INK, anchor="middle", weight="700"))
        els.append(txt(rx + rw / 2, ry + 326, "正式主姓看【最后 1 词】→ 阿维罗（Aveiro）！", size=9.6, color=GREEN, anchor="middle", weight="700"))
        els.append(txt(rx + 22, ry + 354, "• 对比连接词：西语偶尔夹 y（如 Ortega y Gasset），", size=9.3, color=INK))
        els.append(txt(rx + 22, ry + 370, "  葡语常带 de / da / dos / e，且母前父后恰好镜像反转！", size=9.3, color=INK))
        els.append(txt(rx + 22, ry + 387, "• C 罗球衣印 Ronaldo 其实是他教名的第二部分，并非姓氏", size=9.1, color=MUTED))

        els.append(
            txt(
                380,
                488,
                "注：支持动画的浏览器单次演示父/母姓名向下一代拼合的路径并定格于完整终态；开启“减少动态效果”时直接静态呈现。",
                size=9.5,
                color=MUTED,
                anchor="middle",
            )
        )

        svg = figure(
            500,
            "冰岛活态父名母名制与西班牙葡萄牙双姓顺序镜像反转分步对比图",
            "左侧展示冰岛依据1996年《个人姓名法》与2019年《性别自主法》，父亲Jón Einarsson与母亲Sigríður Pálsdóttir的子女分别取Jónsson、Jónsdóttir或Jónsbur，导致一家四口护照末栏各不相同；右侧对比西班牙传统“父姓在前、母姓在后”（如Rafael Nadal Parera主姓Nadal）与葡萄牙“母姓在前、父姓压轴”（如Cristiano Ronaldo dos Santos Aveiro主姓Aveiro）的镜像差异。",
            els,
        )
        write_svg(SUBDIR, "iceland-iberian-family-relay-anim.svg", svg)

    def _build_smith_miller_john_rosetta():
        """SVG 3: Cross-European etymological Rosetta matrix of Blacksmith, Miller, John/Priest, and Appearance surnames."""
        els = []
        els.extend(
            header(
                "半个欧洲都叫“铁匠、磨坊主、约翰和红头发”：八大语区同源对照表",
                "中世纪人口普查与征税造册时，全欧洲村民都在用同四类特征起姓——只是换了不同语言的马甲。",
            )
        )

        # Table header bar
        els.append(card(20, 64, 720, 34, rx=8, fill=PLAQUE_BLUE, stroke="none"))
        cols = [
            (28, "语种 / 代表区", PLAQUE_TEXT),
            (148, "铁匠（打铁铺）", "#93c5fd"),
            (296, "磨坊主（磨面坊）", "#fde68a"),
            (444, "约翰 / 神父之子", "#d8b4fe"),
            (596, "外貌 / 排行高频姓", "#86efac"),
        ]
        for cx, ctitle, ccol in cols:
            els.append(txt(cx, 85, ctitle, size=10.6, color=ccol, weight="700"))

        rows = [
            ("英语（英伦）", "Smith", "Miller", "Johnson · Jones · Evans", "Brown · Reid(红) · Little"),
            ("德语（德奥瑞）", "Schmidt · Schmitt", "Müller（全德第1姓）", "Jansen · Hans", "Klein(小) · Groß · Roth"),
            ("法语（法/比瓦）", "Lefèvre · Faure", "Meunier · Moulin", "Jean · Petitjean", "Petit(小) · Legrand · Roux"),
            ("意大利语", "Ferrari（ferrum 铁！）", "Molinari", "Di Giovanni · Gianni", "Rossi（红发，全意第1姓）"),
            ("西班牙语", "Herrera · Herrero", "Molina · Molinero", "Ibáñez · Juanes", "Delgado(瘦) · Rubio(金)"),
            ("波兰 / 捷克", "Kowalski · Kovář", "Młynarski · Mlynář", "Janowski · Janák", "Nowak(新户) · Černý(黑)"),
            ("俄语 / 罗马尼亚", "俄 Kuznetsov", "俄 Melnikov", "俄 Ivanov · 罗 Popescu", "Belyaev(白) · Chernov"),
            ("匈牙利 / 芬 / 希", "匈 Kovács · 芬 Seppälä", "匈 Molnár", "希 Papadopoulos", "匈 Nagy（大，全匈第1姓）"),
        ]
        assert len(rows) == 8

        y0 = 104
        rh = 36
        for idx, (lang, smith, miller, john, trait) in enumerate(rows):
            ry = y0 + idx * (rh + 4)
            bg_row = "#ffffff" if idx % 2 == 0 else "#f8fafc"
            is_ferrari = idx == 3
            els.append(card(20, ry, 720, rh, rx=6, fill=ORANGE_SOFT if is_ferrari else bg_row, stroke=ORANGE if is_ferrari else BORDER, sw=1.1 if is_ferrari else 0.8))
            els.append(txt(28, ry + 22, lang, size=10.2, color=INK, weight="700"))
            els.append(txt(148, ry + 22, smith, size=10.1, color=ORANGE if is_ferrari else BLUE, weight="700"))
            els.append(txt(296, ry + 22, miller, size=10.0, color=BODY, weight="600" if "第1" in miller else None))
            els.append(txt(444, ry + 22, john, size=9.9, color=PURPLE, weight="600"))
            els.append(txt(596, ry + 22, trait, size=9.8, color=GREEN if "第1" in trait else BODY, weight="700" if "第1" in trait else None))

        # Bottom revelation card
        by = 430
        els.append(card(20, by, 720, 52, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.2))
        els.append(
            txt(
                380,
                by + 21,
                "跨语种破壁彩蛋：超跑法拉利（Ferrari，拉丁语铁匠）、西班牙埃雷拉（Herrera，拉丁语 f→h 音变）、",
                size=10.2,
                color=BLUE,
                anchor="middle",
                weight="700",
            )
        )
        els.append(
            txt(
                380,
                by + 39,
                "波兰科瓦尔斯基（Kowalski）与匈牙利科瓦奇（Kovács），撕掉翻译滤镜后全都是村头打马掌的“老铁师傅（Smith）”！",
                size=10.0,
                color=INK,
                anchor="middle",
                weight="600",
            )
        )

        svg = figure(
            494,
            "欧洲八大语区铁匠、磨坊主、约翰教士与外貌特征同源姓氏对照表",
            "横向对齐英语、德语、法语、意大利语、西班牙语、波兰与捷克语、俄语与罗马尼亚语、匈牙利芬兰希腊语在四大造姓源头上的同源词：如Smith、Schmidt、Lefèvre、Ferrari、Herrera、Kowalski、Kuznetsov、Kovács均意为铁匠；Müller、Miller、Meunier、Molinari、Molnár均意为磨坊主。",
            els,
        )
        write_svg(SUBDIR, "smith-miller-john-rosetta.svg", svg)

    def _build_particles_gender_uralic():
        """SVG 4: High-precision edge cues — von vs van/Van, Lithuanian 3-state marital suffixes, and Uralic outliers."""
        els = []
        els.extend(
            header(
                "介词大小写、女姓看婚否与“姓在前”孤岛：三个一招制敌的高阶细节",
                "为什么贝多芬在维也纳法庭当众尴尬？为什么立陶宛女姓一眼暴露婚否？匈牙利为什么像中文一样姓在前？",
            )
        )

        # Top Left Card: von vs van vs Flemish Van/De + Beethoven 1818
        lx, ly, lw, lh = 20, 64, 352, 232
        els.append(card(lx, ly, lw, lh, rx=9, fill=CARD_BG, stroke=BLUE, sw=1.4))
        els.append(card(lx, ly, lw, 34, rx=9, fill=BLUE, stroke="none"))
        els.append(txt(lx + lw / 2, ly + 22, "① 介词玄机：德 von ≠ 荷 van ≠ 比利时大写 Van", size=10.8, color="#ffffff", anchor="middle", weight="700"))

        p_rows = [
            ("德国 / 奥地利 von", "多为贵族封地头衔：von Bismarck · von Neumann", BLUE_SOFT, BLUE),
            ("荷兰 tussenvoegsel", "纯平民“来自”，连名必小写：Vincent van Gogh", GREEN_SOFT, GREEN),
            ("比利时弗拉芒区", "户籍连名常保留大写：Kevin De Bruyne · Van Rompuy", ORANGE_SOFT, ORANGE),
        ]
        for idx, (ptag, ptxt, pbg, pfg) in enumerate(p_rows):
            py = ly + 42 + idx * 38
            els.append(card(lx + 10, py, lw - 20, 33, rx=5, fill=pbg, stroke="none"))
            els.append(txt(lx + 18, py + 13, ptag, size=9.8, color=pfg, weight="700"))
            els.append(txt(lx + 18, py + 27, ptxt, size=9.5, color=INK))

        els.append(card(lx + 10, ly + 160, lw - 20, 64, rx=6, fill="#fffdf7", stroke=GOLD, sw=1.0))
        els.append(txt(lx + 18, ly + 177, "史料现场｜1818.12.11 贝多芬维也纳法庭破防案：", size=9.7, color=GOLD, weight="700"))
        els.append(txt(lx + 18, ly + 194, "祖籍弗拉芒梅赫伦，van Beethoven 意为“来自甜菜园”；", size=9.3, color=INK))
        els.append(txt(lx + 18, ly + 210, "因拿不出贵族证书，监护权案被贵族法庭踢回平民市政厅！", size=9.3, color=CRIMSON, weight="600"))

        # Top Right Card: Lithuanian 3-state female surnames + Slavic gender endings
        rx, ry, rw, rh = 388, 64, 352, 232
        els.append(card(rx, ry, rw, rh, rx=9, fill=CARD_BG, stroke=CRIMSON, sw=1.4))
        els.append(card(rx, ry, rw, 34, rx=9, fill=CRIMSON, stroke="none"))
        els.append(txt(rx + rw / 2, ry + 22, "② 词尾变形：立陶宛把“未婚/已婚”焊在姓氏尾巴上", size=10.6, color="#ffffff", anchor="middle", weight="700"))

        els.append(txt(rx + 14, ry + 53, "立陶宛同一家族（父/夫姓 Kazlauskas）的三种女姓：", size=9.8, color=INK, weight="700"))
        lt_rows = [
            ("未婚女儿 -aitė/-ytė/-ūtė", "Kazlauskaitė（一眼看出是女儿身）", PURPLE_SOFT, PURPLE),
            ("已婚妻子 -ienė", "Kazlauskienė（传统婚后冠夫姓尾缀）", CRIMSON_SOFT, CRIMSON),
            ("2003 法定中性尾音 -ė", "Kazlauskė（国家语委新增，免透露婚否）", GREEN_SOFT, GREEN),
        ]
        for idx, (ltag, ltxt, lbg, lfg) in enumerate(lt_rows):
            ly_r = ry + 61 + idx * 36
            els.append(card(rx + 10, ly_r, rw - 20, 31, rx=5, fill=lbg, stroke="none"))
            els.append(txt(rx + 18, ly_r + 13, ltag, size=9.6, color=lfg, weight="700"))
            els.append(txt(rx + 18, ly_r + 26, ltxt, size=9.4, color=INK))

        els.append(card(rx + 10, ry + 173, rw - 20, 51, rx=6, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(rx + 18, ry + 190, "斯拉夫女姓对照：俄 Yeltsina · 波兰 Skłodowska", size=9.5, color=INK, weight="700"))
        els.append(txt(rx + 18, ry + 207, "捷克曾强制女姓加 -ová（Nováková），2022 修法准许免加", size=9.3, color=MUTED))

        # Bottom Wide Card: Three Uralic Islands in Indo-European Sea (Hungary, Finland, Estonia)
        bx, by, bw, bh = 20, 310, 720, 184
        els.append(card(bx, by, bw, bh, rx=9, fill=CARD_BG, stroke=GREEN, sw=1.4))
        els.append(card(bx, by, bw, 34, rx=9, fill=GREEN, stroke="none"))
        els.append(txt(bx + bw / 2, by + 22, "③ 印欧语系汪洋里的“乌拉尔语系孤岛”：匈牙利姓在前，芬兰满街 -nen", size=11.0, color="#ffffff", anchor="middle", weight="700"))

        # Left sub-box: Hungary
        els.append(card(bx + 14, by + 44, 338, 128, rx=7, fill=GREEN_SOFT, stroke=GREEN, sw=1.0))
        els.append(txt(bx + 24, by + 63, "匈牙利（Magyar）｜全欧唯一全国“姓在前、名在后”！", size=10.2, color=GREEN, weight="700"))
        els.append(txt(bx + 24, by + 82, "• 语法与中文一致，本土证件/报刊一律【家族姓 + 教名】：", size=9.5, color=INK))
        els.append(txt(bx + 30, by + 100, "Liszt Ferenc（李斯特） · Puskás Ferenc（普斯卡什）", size=9.6, color=INK, weight="700"))
        els.append(txt(bx + 30, by + 118, "Erdős Pál（埃尔德什） · Karikó Katalin（考里科）", size=9.6, color=INK, weight="700"))
        els.append(txt(bx + 24, by + 138, "• 翻译成英法德文时才倒装成 Ferenc Liszt，切勿认反姓氏！", size=9.2, color=MUTED))
        els.append(txt(bx + 24, by + 156, "• 高频姓：Nagy(大) · Kovács(铁匠) · Tóth · Szabó(裁缝)", size=9.3, color=GREEN, weight="600"))

        # Right sub-box: Finland
        els.append(card(bx + 368, by + 44, 338, 128, rx=7, fill=BLUE_SOFT, stroke=BLUE, sw=1.0))
        els.append(txt(bx + 378, by + 63, "芬兰（Suomi）｜超 1/3 国民带着大自然的 -nen 尾巴", size=10.2, color=BLUE, weight="700"))
        els.append(txt(bx + 378, by + 82, "• 1921《姓氏法》定型，民众纷纷把山水草木加 -nen 入户：", size=9.5, color=INK))
        els.append(txt(bx + 384, by + 100, "Virtanen（溪流） · Mäkinen（山丘） · Järvinen（湖泊）", size=9.6, color=INK, weight="700"))
        els.append(txt(bx + 384, by + 118, "Nieminen（半岛） · Korhonen（与 Virtanen 争全国第1）", size=9.6, color=INK, weight="700"))
        els.append(txt(bx + 378, by + 138, "• 西芬兰另常见庄园后缀 -la / -lä：Mäkelä · Mattila", size=9.2, color=MUTED))
        els.append(txt(bx + 378, by + 156, "• 民族浪漫期还掀起把瑞典姓改译芬兰词（如 Kivi“岩石”）", size=9.3, color=BLUE, weight="600"))

        svg = figure(
            508,
            "欧洲姓氏介词大小写区分、立陶宛女姓婚否后缀与乌拉尔语系匈牙利芬兰特例图",
            "左上对比德语贵族von、荷兰平民小写van与比利时常见大写Van/De，并附1818年贝多芬在维也纳贵族法庭承认非贵族的史实；右上解析立陶宛语未婚-aitė、已婚-ienė与2003年新增中性-ė三态女姓及捷克2022年-ová改革；下方展示乌拉尔语系的匈牙利东方姓前名后语序与芬兰超三分之一人口使用的自然地貌后缀-nen。",
            els,
        )
        write_svg(SUBDIR, "particles-gender-and-uralic-outliers.svg", svg)

    def _build_three_second_decoder():
        """SVG 5: Practical 4-step funnel for decoding a European name in 3 seconds + 3 migration/border counterexamples."""
        els = [_arrow_defs()]
        els.extend(
            header(
                "实战速查卡：拿到一个陌生欧洲人名，3 秒钟破译出处的四步漏斗",
                "先抓“一票锁定”的独占特殊字母，再看结构与词尾印章，最后用反例滤镜排除移民与边疆干扰。",
            )
        )

        # Step 1: Diacritics & Digraphs (y=64..186)
        els.append(card(20, 64, 720, 122, rx=9, fill=CARD_BG, stroke=BLUE, sw=1.4))
        els.append(step_badge(38, 84, "1", fg="#ffffff", bg=BLUE, r=11))
        els.append(txt(56, 88, "第 1 步｜扫特殊字母与变音符（最快“一剑封喉”，直接缩到 1–2 国）", size=11.4, color=BLUE, weight="700"))

        chips = [
            (32, 100, "þ · ð", "冰岛（þ 国家级独占）", BLUE, BLUE_SOFT),
            (208, 100, "ø · æ", "丹麦 / 挪威（Ødegaard）", BLUE, BLUE_SOFT),
            (384, 100, "ł · ą · ę · ń · ś · ż", "波兰（Świątek）", PURPLE, PURPLE_SOFT),
            (560, 100, "ř · ů", "捷克（Dvořák 独有 ř）", PURPLE, PURPLE_SOFT),
            (32, 142, "ő · ű + sz · cs · gy", "匈牙利（双长音符 Erdős）", GREEN, GREEN_SOFT),
            (208, 142, "ș · ț · ă", "罗马尼亚（Ceaușescu）", ORANGE, ORANGE_SOFT),
            (384, 142, "ß / å", "ß 德奥 ｜ å 瑞/挪/丹", SLATE, SLATE_SOFT),
            (560, 142, "ñ / ã · õ / ğ · ı", "ñ 西 ｜ ã 葡 ｜ ğ 土耳其", ORANGE, ORANGE_SOFT),
        ]
        for cx, cy, ckey, cval, cfg, cbg in chips:
            els.append(card(cx, cy, 168, 34, rx=6, fill=cbg, stroke="none"))
            els.append(txt(cx + 8, cy + 14, ckey, size=10.0, color=cfg, weight="700"))
            els.append(txt(cx + 8, cy + 28, cval, size=9.2, color=INK))

        # Downward funnel arrows
        els.append(_line(196, 186, 196, 200, stroke=PURPLE, sw=1.6, marker="en-arr-p"))
        els.append(_line(564, 186, 564, 200, stroke=GREEN, sw=1.6, marker="en-arr-g"))

        # Step 2 & Step 3 side-by-side (y=202..342)
        els.append(card(20, 202, 352, 140, rx=9, fill=CARD_BG, stroke=PURPLE, sw=1.3))
        els.append(step_badge(38, 222, "2", fg="#ffffff", bg=PURPLE, r=11))
        els.append(txt(56, 226, "第 2 步｜看名字段数、大小写与语序", size=11.2, color=PURPLE, weight="700"))
        s2 = [
            "• 三段式含 -ovich / -ovna → 俄罗斯 / 白俄罗斯",
            "• 双姓【父+母】→ 西班牙；【母+父(常夹dos/da)】→ 葡萄牙",
            "• 连名小写 van / van der → 荷兰；大写 Van / De → 比利时",
            "• 本土文本把家族姓放第 1 词 → 匈牙利（如 Liszt Ferenc）",
        ]
        for i, line_s in enumerate(s2):
            els.append(txt(32, 250 + i * 22, line_s, size=9.6, color=INK))

        els.append(card(388, 202, 352, 140, rx=9, fill=CARD_BG, stroke=GREEN, sw=1.3))
        els.append(step_badge(406, 222, "3", fg="#ffffff", bg=GREEN, r=11))
        els.append(txt(424, 226, "第 3 步｜对词尾高频“家族印章”", size=11.2, color=GREEN, weight="700"))
        s3 = [
            "• -ić / -vić → 克罗地亚/塞尔维亚/波黑 ｜ -escu → 罗马尼亚",
            "• -nen / -lä → 芬兰 ｜ -sen → 丹/挪 ｜ -sson → 瑞典",
            "• -as / -is / -aitė / -ienė → 立陶宛 ｜ 词尾全挂 -s → 拉脱维亚",
            "• -opoulos / -akis / -idis → 希腊 ｜ -ashvili / -adze → 格鲁吉亚",
        ]
        for i, line_s in enumerate(s3):
            els.append(txt(400, 250 + i * 22, line_s, size=9.6, color=INK))

        els.append(_line(380, 342, 380, 356, stroke=ORANGE, sw=1.8, marker="en-arr-o"))

        # Step 4: Counterexamples Warning Box (y=358..506)
        els.append(card(20, 358, 720, 146, rx=9, fill="#fffaf5", stroke=ORANGE, sw=1.5))
        els.append(step_badge(38, 378, "4", fg="#ffffff", bg=ORANGE, r=11))
        els.append(txt(56, 382, "第 4 步｜必做防坑校验：记住“姓氏语言学祖源 ≠ 当事人现持护照”三大反例！", size=11.2, color=ORANGE, weight="700"))

        warns = [
            (
                32,
                "反例 A · 现代移民与球星二代",
                [
                    "伊布 Ibrahimović 词尾是典型前南 -ić，",
                    "但生于马尔默、代表瑞典出战；",
                    "姆巴佩 Mbappé、齐达内 Zidane",
                    "则折射出法国多元移民史。",
                ],
            ),
            (
                268,
                "反例 B · 千年历史边疆交错带",
                [
                    "法国球星格列兹曼 Griezmann",
                    "来自法德交界的阿尔萨斯；",
                    "意大利网球名将 Jannik Sinner",
                    "生于意北德语区南蒂罗尔！",
                ],
            ),
            (
                504,
                "反例 C · 跨国联姻与王室改姓",
                [
                    "居里夫人 Skłodowska-Curie",
                    "用连字符拼起波兰娘家与法国夫姓；",
                    "英国王室 1917 年弃用德国旧姓，",
                    "直接改姓英伦地名 Windsor（温莎）！",
                ],
            ),
        ]
        for wx, wtitle, wlines in warns:
            els.append(card(wx, 396, 224, 96, rx=7, fill="#ffffff", stroke=BORDER))
            els.append(txt(wx + 10, 415, wtitle, size=9.8, color=CRIMSON, weight="700"))
            for l_idx, wln in enumerate(wlines):
                els.append(txt(wx + 10, 434 + l_idx * 15.5, wln, size=9.1, color=INK))

        svg = figure(
            518,
            "三秒识别陌生欧洲人名来源国的四步漏斗与三大反例警示图",
            "按实战顺序分四步拆解欧洲姓名：①扫视þ/ð、ø/æ、ł、ř、ő/ű、ș/ț、ß等国家特征字母；②检查俄罗斯三段父称、西葡双姓镜像顺序、荷比van大小写及匈牙利姓前名后语序；③核对-ić、-escu、-nen、-opoulos、-aitė等词尾印章；④结合现代移民（如伊布）、边疆交错带（如意大利德语区的辛纳）与王室联姻改姓（如温莎王朝）区分语言祖源与现国籍。",
            els,
        )
        write_svg(SUBDIR, "three-second-surname-decoder.svg", svg)

    @register(
        "european-name-patterns",
        "欧洲姓名国别密码：四大区父名图谱、冰岛与西葡传姓动画、铁匠磨坊主跨语种同源表、介词女姓乌拉尔特例与三秒破译漏斗",
        "humanities",
    )
    def build_european_name_patterns():
        _build_patronymic_atlas()
        _build_iceland_iberian_family_relay()
        _build_smith_miller_john_rosetta()
        _build_particles_gender_uralic()
        _build_three_second_decoder()


def _register_weiqi_intro_rules():
    SUBDIR = "weiqi-intro-rules"
    BOARD_WOOD = "#f5dfa8"
    BOARD_STROKE = "#85581f"
    GRID_INK = "#5c3d14"
    BLACK_STONE = "#18181b"
    WHITE_STONE = "#f8fafc"
    WHITE_EDGE = "#475569"

    def _draw_go_grid(els, x0, y0, n, step, pad=14, stars=()):
        span = (n - 1) * step
        els.append(
            f'<rect x="{x0 - pad:.1f}" y="{y0 - pad:.1f}" width="{span + 2 * pad:.1f}" '
            f'height="{span + 2 * pad:.1f}" rx="6" fill="{BOARD_WOOD}" stroke="{BOARD_STROKE}" stroke-width="1.4"/>'
        )
        for i in range(n):
            sw = 1.25 if i in (0, n - 1) else 0.78
            els.append(_line(x0 + i * step, y0, x0 + i * step, y0 + span, stroke=GRID_INK, sw=sw))
            els.append(_line(x0, y0 + i * step, x0 + span, y0 + i * step, stroke=GRID_INK, sw=sw))
        for sr, sc in stars:
            els.append(f'<circle cx="{x0 + sc * step:.1f}" cy="{y0 + sr * step:.1f}" r="2.5" fill="{GRID_INK}"/>')

    def _stone(cx, cy, r, color, label=None, label_color=None, extra_cls=""):
        cls_attr = f' class="{extra_cls}"' if extra_cls else ""
        if color == "B":
            fill, stroke, sw = BLACK_STONE, "#09090b", 1.0
            lc = label_color or "#ffffff"
        else:
            fill, stroke, sw = WHITE_STONE, WHITE_EDGE, 1.15
            lc = label_color or INK
        out = [f'<g{cls_attr}><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
        if color == "B":
            out.append(f'<circle cx="{cx - r * 0.28:.1f}" cy="{cy - r * 0.28:.1f}" r="{r * 0.22:.1f}" fill="#52525b" opacity="0.65"/>')
        if label is not None:
            out.append(txt(cx, cy + r * 0.34, str(label), size=max(8.6, r * 1.02), color=lc, anchor="middle", weight="700"))
        out.append("</g>")
        return "".join(out)

    def _bfs_group_and_liberties(board, n, r0, c0):
        color = board.get((r0, c0))
        assert color in ("B", "W")
        group = set()
        libs = set()
        stack = [(r0, c0)]
        while stack:
            r, c = stack.pop()
            if (r, c) in group:
                continue
            group.add((r, c))
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    st = board.get((nr, nc))
                    if st is None:
                        libs.add((nr, nc))
                    elif st == color and (nr, nc) not in group:
                        stack.append((nr, nc))
        return group, libs

    def _build_board_geometry_and_zones():
        els = []
        els.extend(
            header(
                "19×19 棋盘的几何密码：361 个交叉点、九星天元与“金角银边草肚皮”",
                "棋子不下在格子里而是落在纵横线交叉点上；围同样 9 目空，中腹所需棋子数整整是角上的 2 倍",
            )
        )

        # Left card: Full 19x19 board
        els.append(card(16, 74, 344, 384))
        els.append(step_badge(32, 92, 1, BLUE, BLUE_SOFT))
        els.append(txt(48, 96, "标准 19 路棋盘：19×19 = 361 点与九星坐标", size=11.4, color=PANEL_TITLE, weight="700"))

        bx, by, bstep = 48, 122, 14.2
        stars_19 = [(r, c) for r in (3, 9, 15) for c in (3, 9, 15)]
        assert len(stars_19) == 9 and 19 * 19 == 361
        _draw_go_grid(els, bx, by, 19, bstep, pad=12, stars=stars_19)

        # Highlight 3rd line (territory) and 4th line (influence) dashed rings lightly
        s3 = 2 * bstep
        w3 = 14 * bstep
        els.append(
            f'<rect x="{bx + s3:.1f}" y="{by + s3:.1f}" width="{w3:.1f}" height="{w3:.1f}" '
            f'fill="none" stroke="{GREEN}" stroke-width="1.2" stroke-dasharray="3.5 2.5" opacity="0.85"/>'
        )
        s4 = 3 * bstep
        w4 = 12 * bstep
        els.append(
            f'<rect x="{bx + s4:.1f}" y="{by + s4:.1f}" width="{w4:.1f}" height="{w4:.1f}" '
            f'fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 2.5" opacity="0.85"/>'
        )

        # Highlight Tianyuan (9,9), San-san (2,2), Hoshi (3,3), Komoku (2,3)
        tx, ty = bx + 9 * bstep, by + 9 * bstep
        els.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="5.2" fill="none" stroke="{CRIMSON}" stroke-width="1.6"/>')
        els.append(txt(tx, ty - 8, "天元(10,10)", size=9.2, color=CRIMSON, anchor="middle", weight="700", halo=True))

        hx, hy = bx + 3 * bstep, by + 3 * bstep
        els.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="4.8" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
        els.append(txt(hx + 7, hy + 12, "星位(4,4)", size=9.0, color=BLUE, weight="700", halo=True))

        sx, sy = bx + 2 * bstep, by + 2 * bstep
        els.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4.2" fill="{GREEN}" opacity="0.9"/>')
        els.append(txt(sx - 4, sy - 7, "三三(3,3)", size=8.8, color=GREEN, weight="700", halo=True))

        # Coordinate ticks along top & left (1, 4, 10, 16, 19)
        for idx in (0, 3, 9, 15, 18):
            els.append(txt(bx + idx * bstep, by - 15, str(idx + 1), size=8.6, color=MUTED, anchor="middle", cls="mono"))
            els.append(txt(bx - 16, by + idx * bstep + 3, str(idx + 1), size=8.6, color=MUTED, anchor="end", cls="mono"))

        els.append(txt(32, 412, "• 绿虚线 = 三线“实地线”（贴地捞空，守角最稳）", size=9.4, color=GREEN, weight="700"))
        els.append(txt(32, 430, "• 蓝虚线 = 四线“外势线”（面向中腹辐射全局影响力）", size=9.4, color=BLUE, weight="700"))
        els.append(txt(32, 447, "• 九星对称排布：四角星 + 四边星 + 正中“天元”", size=9.2, color=MUTED))

        # Right card: Corner vs Side vs Center efficiency
        els.append(card(374, 74, 370, 384))
        els.append(step_badge(390, 92, 2, ORANGE, ORANGE_SOFT))
        els.append(txt(406, 96, "几何铁律：围同样 9 目空，各处要花几颗子？", size=11.4, color=PANEL_TITLE, weight="700"))

        # Three 7x7 mini-boards comparing enclosing 3x3 = 9 empty points!
        cases = [
            (
                390,
                "① 金角：仅需 6 颗子",
                "借 2 条天然盘边",
                "效率 1.50 目/子",
                GREEN,
                GREEN_SOFT,
                # 3x3 empty at rows 0..2, cols 0..2 -> stones at (3,0),(3,1),(3,2) and (0,3),(1,3),(2,3) -> 6 stones!
                [(3, 0), (3, 1), (3, 2), (0, 3), (1, 3), (2, 3)],
                [(r, c) for r in range(3) for c in range(3)],
            ),
            (
                508,
                "② 银边：需要 9 颗子",
                "借 1 条天然盘边",
                "效率 1.00 目/子",
                BLUE,
                BLUE_SOFT,
                # 3x3 empty at rows 0..2, cols 2..4 -> stones at col 1 (0..2), row 3 (2..4), col 5 (0..2) -> 9 stones!
                [(0, 1), (1, 1), (2, 1), (3, 2), (3, 3), (3, 4), (0, 5), (1, 5), (2, 5)],
                [(r, c) for r in range(3) for c in range(2, 5)],
            ),
            (
                626,
                "③ 草肚皮：要 12 颗子",
                "四面漏风无边可借",
                "效率 0.75 目/子",
                ORANGE,
                ORANGE_SOFT,
                # 3x3 empty at rows 2..4, cols 2..4 -> 4 sides * 3 = 12 stones!
                [(1, 2), (1, 3), (1, 4), (5, 2), (5, 3), (5, 4), (2, 1), (3, 1), (4, 1), (2, 5), (3, 5), (4, 5)],
                [(r, c) for r in range(2, 5) for c in range(2, 5)],
            ),
        ]
        expected_counts = [6, 9, 12]
        for idx, (cx0, ctitle, csub, ceff, col, bg, stones, empties) in enumerate(cases):
            assert len(stones) == expected_counts[idx] and len(empties) == 9
            # Verify every empty point is strictly enclosed inside the 7x7 grid by stones + board boundary!
            stone_set = set(stones)
            empty_set = set(empties)
            for er, ec in empty_set:
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = er + dr, ec + dc
                    if 0 <= nr < 7 and 0 <= nc < 7:
                        assert (nr, nc) in empty_set or (nr, nc) in stone_set

            els.append(card(cx0, 112, 106, 214, rx=7, fill=bg, stroke=col))
            els.append(txt(cx0 + 53, 130, ctitle, size=9.6, color=col, anchor="middle", weight="700"))
            ms = 12.2
            mx0 = cx0 + 16.5
            my0 = 148
            _draw_go_grid(els, mx0, my0, 7, ms, pad=7)
            for er, ec in empties:
                ex, ey = mx0 + ec * ms, my0 + er * ms
                els.append(f'<rect x="{ex - 3.1:.1f}" y="{ey - 3.1:.1f}" width="6.2" height="6.2" fill="{col}" opacity="0.88"/>')
            for sr, sc in stones:
                els.append(_stone(mx0 + sc * ms, my0 + sr * ms, 4.9, "B"))
            els.append(txt(cx0 + 53, 248, csub, size=8.9, color=INK, anchor="middle"))
            els.append(pill(cx0 + 9, 258, ceff, fg=col, bg="#ffffff", border=col, w=88, h=22, size=8.8))
            els.append(txt(cx0 + 53, 297, f"围 9 空耗 {len(stones)} 子", size=9.0, color=INK, anchor="middle", weight="700"))
            els.append(txt(cx0 + 53, 314, f"成本比 = {len(stones)/6:.1f}×", size=8.8, color=MUTED, anchor="middle", cls="mono"))

        # Bottom summary box on combinatorics & opening order
        els.append(card(390, 338, 338, 108, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(400, 358, "为什么开局总是“先占角 → 再挂守边 → 最后进中腹”？", size=9.8, color=INK, weight="700"))
        els.append(txt(400, 377, "1. 周长定律：角借两道墙、边借一道墙，中腹围空贵一倍；", size=8.9, color=BODY))
        els.append(txt(400, 395, "2. 做活难度：角部五六子即可做两眼，中腹四面易遭搜根；", size=8.9, color=BODY))
        els.append(txt(400, 413, "3. 组合宇宙：361 点共 3^361 ≈ 1.74×10^172 种涂色，扣去", size=8.9, color=BODY))
        els.append(txt(400, 431, "   无气死形仍有 2.08×10^170 种合法局面（Tromp, 2016）！", size=8.9, color=BLUE, weight="700"))

        svg = figure(
            472,
            "19×19围棋盘361个交叉点坐标与金角银边草肚皮几何效率对比图",
            "左图精确绘制19×19标准围棋盘361个交叉点、九星位与正中天元(10,10)，标出三线实地线与四线外势线；右图用三块7×7局部棋盘严格证明围出同样3×3=9目空时，角部借两条盘边仅需6子（1.50目/子），边部借一条盘边需9子（1.00目/子），中腹四面漏风需12子（0.75目/子）。",
            els,
        )
        write_svg(SUBDIR, "weiqi-board-geometry-and-zones.svg", svg)

    def _build_liberties_capture_and_forbidden_anim():
        els = []
        els.extend(
            header(
                "围棋唯一的生死法则：“气”、横竖连接、提子动画与“禁入 vs 反杀”",
                "整部围棋法典地基只有一句话：棋块紧邻的空交叉点叫“气”，气被堵光（0 气）就必须离开棋盘",
            )
        )

        # Top card: Liberties & connectivity across 4 mini-grids
        els.append(card(16, 74, 728, 174))
        els.append(step_badge(32, 92, 1, BLUE, BLUE_SOFT))
        els.append(txt(48, 96, "先认准“气（Liberties）”：只看上下左右直线相邻空点，斜角相挨不算气、也不算相连！", size=11.2, color=PANEL_TITLE, weight="700"))

        lib_demos = [
            (32, "中腹单子 = 4 口气", {(2, 2): "B"}, (2, 2), 4, "四面畅通最难被围"),
            (208, "边子 3 气 · 角子 2 气", {(0, 0): "B", (0, 3): "W"}, (0, 0), 2, "贴边少1气，缩角天生仅2气"),
            (384, "横竖相连 = 共享 6 气", {(2, 1): "B", (2, 2): "B"}, (2, 1), 6, "连成一块同生共死，气数大增"),
            (560, "斜角尖顶 ≠ 连接！", {(1, 1): "B", (2, 2): "B"}, (1, 1), 4, "两子各自独立算气，可被冲断"),
        ]
        for lx, ltitle, bdict, anchor_pt, exp_libs, lnote in lib_demos:
            grp, libs = _bfs_group_and_liberties(bdict, 5, anchor_pt[0], anchor_pt[1])
            assert len(libs) == exp_libs
            els.append(card(lx, 108, 168, 128, rx=7, fill="#fafaf9", stroke=BORDER))
            els.append(txt(lx + 84, 125, ltitle, size=9.6, color=INK, anchor="middle", weight="700"))
            gx, gy, gs = lx + 48, 138, 17.5
            _draw_go_grid(els, gx, gy, 5, gs, pad=6)
            # If demo 2 also show W's 3 liberties in blue!
            if len(bdict) == 2 and (0, 3) in bdict:
                _, wlibs = _bfs_group_and_liberties(bdict, 5, 0, 3)
                assert len(wlibs) == 3
                for wr, wc in sorted(wlibs):
                    els.append(f'<circle cx="{gx + wc * gs:.1f}" cy="{gy + wr * gs:.1f}" r="3.7" fill="#ffffff" stroke="{BLUE}" stroke-width="1.5"/>')
            for idx_l, (lr, lc) in enumerate(sorted(libs), 1):
                els.append(f'<circle cx="{gx + lc * gs:.1f}" cy="{gy + lr * gs:.1f}" r="4.0" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.5"/>')
                els.append(txt(gx + lc * gs, gy + lr * gs + 2.8, str(idx_l), size=7.8, color=GREEN, anchor="middle", weight="700"))
            for (sr, sc), scol in bdict.items():
                els.append(_stone(gx + sc * gs, gy + sr * gs, 6.4, scol))
            els.append(txt(lx + 84, 226, lnote, size=8.8, color=MUTED, anchor="middle"))

        # Bottom-Left card: One-shot CSS animation of Atari -> Capture
        els.append(card(16, 260, 356, 194))
        els.append(step_badge(32, 278, 2, GREEN, GREEN_SOFT))
        els.append(txt(48, 282, "打吃与提子动画：堵死最后一口气，整块提出棋盘", size=11.0, color=PANEL_TITLE, weight="700"))

        # 5x5 capture board: White at (2,1),(2,2) surrounded by Black at (1,1),(1,2),(3,1),(3,2),(2,0), last liberty at (2,3)
        cap_board = {
            (2, 1): "W",
            (2, 2): "W",
            (1, 1): "B",
            (1, 2): "B",
            (3, 1): "B",
            (3, 2): "B",
            (2, 0): "B",
        }
        w_grp, w_libs = _bfs_group_and_liberties(cap_board, 5, 2, 1)
        assert w_grp == {(2, 1), (2, 2)} and w_libs == {(2, 3)}
        cap_after = dict(cap_board)
        cap_after[(2, 3)] = "B"
        _, w_libs_after = _bfs_group_and_liberties(cap_after, 5, 2, 1)
        assert len(w_libs_after) == 0

        ax, ay, astep = 42, 314, 24.5
        _draw_go_grid(els, ax, ay, 5, astep, pad=9)
        # Static ghost ring on (2,1),(2,2) so after capture fade-out, reader still sees which 2 white stones were lifted!
        for wr, wc in ((2, 1), (2, 2)):
            els.append(
                f'<circle cx="{ax + wc * astep:.1f}" cy="{ay + wr * astep:.1f}" r="8.2" '
                f'fill="none" stroke="{CRIMSON}" stroke-width="1.3" stroke-dasharray="2.5 2"/>'
            )
            els.append(txt(ax + wc * astep, ay + wr * astep + 3.0, "提", size=8.4, color=CRIMSON, anchor="middle", weight="700"))

        # Last liberty marker at (2,3) before Black 6 lands
        lx_last, ly_last = ax + 3 * astep, ay + 2 * astep
        els.append(f'<circle cx="{lx_last:.1f}" cy="{ly_last:.1f}" r="5.2" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')

        # Existing 5 Black stones
        for (sr, sc), scol in cap_board.items():
            if scol == "B":
                els.append(_stone(ax + sc * astep, ay + sr * astep, 8.8, "B"))
        # Animated 2 White stones (fade out after Black 6 lands!)
        for wr, wc in ((2, 1), (2, 2)):
            els.append(_stone(ax + wc * astep, ay + wr * astep, 8.8, "W", extra_cls="wq-captured"))
        # Animated Black move 6 landing at (2,3)
        els.append(_stone(lx_last, ly_last, 8.8, "B", label="6", extra_cls="wq-killer"))

        # Right side of bottom-left card: step explanation + prisoner tray
        els.append(card(168, 302, 190, 88, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(178, 321, "三步看懂提子（单次动画）：", size=9.6, color=GREEN, weight="700"))
        els.append(txt(178, 339, "① 叫吃(打吃)：两白仅剩右端 1 口气；", size=9.0, color=INK))
        els.append(txt(178, 356, "② 紧气：黑 6 落下堵死最后一口气；", size=9.0, color=INK))
        els.append(txt(178, 373, "③ 提子：白棋 0 气立即提走，留 2 空点！", size=9.0, color=INK, weight="700"))

        # Prisoner tray showing captured 2 white stones
        els.append(card(168, 398, 190, 44, rx=7, fill="#f8fafc", stroke=BORDER))
        els.append(txt(178, 424, "黑方提子盒（俘虏）：", size=9.2, color=INK, weight="700"))
        els.append(_stone(306, 420, 7.5, "W", extra_cls="wq-tray"))
        els.append(_stone(326, 420, 7.5, "W", extra_cls="wq-tray"))
        els.append(txt(344, 424, "×2", size=9.4, color=CRIMSON, weight="700", cls="mono"))

        # Bottom-Right card: Suicide forbidden vs Capture-first exception
        els.append(card(386, 260, 358, 194))
        els.append(step_badge(402, 278, 3, CRIMSON, CRIMSON_SOFT))
        els.append(txt(418, 282, "铁律辨析：什么叫“禁入点”？为什么有时又能往虎口里下？", size=10.8, color=PANEL_TITLE, weight="700"))

        # Left sub-panel: Illegal suicide
        els.append(card(400, 298, 162, 144, rx=7, fill=CRIMSON_SOFT, stroke=CRIMSON))
        els.append(txt(481, 315, "✗ 非法禁入点（禁止自杀）", size=9.4, color=CRIMSON, anchor="middle", weight="700"))
        sx1, sy1, ss = 445, 328, 18.0
        _draw_go_grid(els, sx1, sy1, 5, ss, pad=6)
        # White cross around (2,2): (1,2),(3,2),(2,1),(2,3) — each W has 3 outer liberties!
        sui_board = {(1, 2): "W", (3, 2): "W", (2, 1): "W", (2, 3): "W"}
        for wr, wc in sui_board:
            els.append(_stone(sx1 + wc * ss, sy1 + wr * ss, 6.6, "W"))
        # Forbidden X at (2,2)
        fx, fy = sx1 + 2 * ss, sy1 + 2 * ss
        els.append(_line(fx - 4.5, fy - 4.5, fx + 4.5, fy + 4.5, stroke=CRIMSON, sw=2.2))
        els.append(_line(fx - 4.5, fy + 4.5, fx + 4.5, fy - 4.5, stroke=CRIMSON, sw=2.2))
        els.append(txt(481, 418, "白四子外气充足；黑落 × 处", size=8.7, color=INK, anchor="middle"))
        els.append(txt(481, 433, "既提不掉白、自己又 0 气 → 禁手", size=8.7, color=CRIMSON, anchor="middle", weight="700"))

        # Right sub-panel: Legal capture ("提子优先于自杀检查")
        els.append(card(570, 298, 162, 144, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(651, 315, "✓ 合法反杀（先提对手！）", size=9.4, color=GREEN, anchor="middle", weight="700"))
        sx2, sy2 = 615, 328
        _draw_go_grid(els, sx2, sy2, 5, ss, pad=6)
        # Corner 3x3 region: White at (0,1),(1,1),(1,0) surrounds (0,0), while Black at (0,2),(1,2),(2,1),(2,0) leaves White with ONLY (0,0) as its last liberty!
        rev_board = {
            (0, 1): "W",
            (1, 1): "W",
            (1, 0): "W",
            (0, 2): "B",
            (1, 2): "B",
            (2, 1): "B",
            (2, 0): "B",
        }
        w_ring, w_ring_libs = _bfs_group_and_liberties(rev_board, 5, 0, 1)
        assert len(w_ring) == 3 and w_ring_libs == {(0, 0)}
        for (rr, rc), rcol in rev_board.items():
            els.append(_stone(sx2 + rc * ss, sy2 + rr * ss, 6.6, rcol))
        # Star move at (0,0)
        els.append(f'<circle cx="{sx2:.1f}" cy="{sy2:.1f}" r="5.5" fill="{GREEN}" stroke="#ffffff" stroke-width="1.2"/>')
        els.append(txt(sx2, sy2 + 3.0, "1", size=8.2, color="#ffffff", anchor="middle", weight="700"))
        els.append(txt(651, 418, "白三子只剩角上 1 处最后一口气", size=8.7, color=INK, anchor="middle"))
        els.append(txt(651, 433, "黑落 1 先拔光白三子，瞬间获气！", size=8.7, color=GREEN, anchor="middle", weight="700"))

        anim_css = """
  .wq-killer {
    transform-box: fill-box;
    transform-origin: center;
    animation: wqDrop 3.2s ease-out 1 forwards;
  }
  .wq-captured {
    animation: wqFadeOut 3.2s ease-in-out 1 forwards;
  }
  .wq-tray {
    animation: wqTrayIn 3.2s ease-out 1 forwards;
  }
  @keyframes wqDrop {
    0%, 28% { opacity: 0; transform: scale(1.35); }
    42%, 100% { opacity: 1; transform: scale(1); }
  }
  @keyframes wqFadeOut {
    0%, 48% { opacity: 1; }
    68%, 100% { opacity: 0.12; }
  }
  @keyframes wqTrayIn {
    0%, 55% { opacity: 0.18; }
    75%, 100% { opacity: 1; }
  }
  @media (prefers-reduced-motion: reduce) {
    .wq-killer, .wq-tray { animation: none !important; opacity: 1 !important; transform: none !important; }
    .wq-captured { animation: none !important; opacity: 0.15 !important; }
  }"""

        svg = figure(
            468,
            "围棋气与连接定义、打吃提子单次动画及禁入点与反杀特例图解",
            "上排用四块5×5棋盘展示中腹4气、边3气角2气、横竖相连共享6气以及斜角相挨不算相连；左下通过单次CSS动画展示黑6堵死两颗白子最后一口气并将其提入俘虏盒（兼容减少动态效果）；右下对比外气充足时的自杀禁入点与敌方仅剩最后1口气时的合法提子反杀。",
            els,
            extra_css=anim_css,
        )
        write_svg(SUBDIR, "liberties-capture-and-forbidden-anim.svg", svg)

    def _build_two_eyes_seki_and_ko_fight():
        els = []
        els.extend(
            header(
                "从一条“气”规则长出的三大神仙推论：两只真眼永生、双活与打劫",
                "规则书根本不用专门规定“两眼活棋”——只要不能自杀、每手只能下一子，两只独立真眼就天然杀不死",
            )
        )

        # Panel 1 (Top-Left): Two true eyes vs One false eye
        els.append(card(16, 74, 360, 192))
        els.append(step_badge(32, 92, 1, GREEN, GREEN_SOFT))
        els.append(txt(48, 96, "为什么必须“两只真眼”才永生？真眼 vs 假眼", size=11.0, color=PANEL_TITLE, weight="700"))

        # Left 6x5 mini-grid: Corner Black group with TWO separate eyes at (0,0) and (0,2)!
        # Black stones at: (0,1), (1,0), (1,1), (1,2), (1,3), (0,3) -> encloses (0,0)=A and (0,2)=B!
        # Surrounded outside by White at (2,0),(2,1),(2,2),(2,3),(2,4),(1,4),(0,4) so Black has ZERO outer liberties!
        eye_board = {
            (0, 1): "B",
            (1, 0): "B",
            (1, 1): "B",
            (1, 2): "B",
            (1, 3): "B",
            (0, 3): "B",
            (2, 0): "W",
            (2, 1): "W",
            (2, 2): "W",
            (2, 3): "W",
            (2, 4): "W",
            (1, 4): "W",
            (0, 4): "W",
        }
        b_grp, b_libs = _bfs_group_and_liberties(eye_board, 5, 0, 1)
        assert len(b_grp) == 6 and b_libs == {(0, 0), (0, 2)}

        els.append(card(28, 110, 162, 144, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(109, 126, "✓ 两只真眼 A、B = 铁活棋", size=9.3, color=GREEN, anchor="middle", weight="700"))
        ex1, ey1, es = 58, 140, 17.5
        _draw_go_grid(els, ex1, ey1, 5, es, pad=6)
        for (rr, rc), rcol in eye_board.items():
            els.append(_stone(ex1 + rc * es, ey1 + rr * es, 6.4, rcol))
        for lbl_e, ec in (("A", 0), ("B", 2)):
            els.append(f'<circle cx="{ex1 + ec * es:.1f}" cy="{ey1:.1f}" r="5.0" fill="#ffffff" stroke="{GREEN}" stroke-width="1.6"/>')
            els.append(txt(ex1 + ec * es, ey1 + 3.0, lbl_e, size=8.2, color=GREEN, anchor="middle", weight="700"))
        els.append(txt(109, 226, "白填 A 黑剩 B 气；白填 B 黑剩 A 气", size=8.4, color=INK, anchor="middle"))
        els.append(txt(109, 241, "两处对白皆禁入点 → 永远杀不死！", size=8.5, color=GREEN, anchor="middle", weight="700"))

        # Right mini-grid: False eye! Eye at (0,2) has stone (1,2) replaced by White (1,2) & (1,3), leaving Black (0,3) isolated in Atari!
        false_board = {
            (0, 1): "B",
            (1, 0): "B",
            (1, 1): "B",
            (0, 3): "B",
            (1, 2): "W",
            (1, 3): "W",
            (0, 4): "W",
            (2, 0): "W",
            (2, 1): "W",
        }
        _, iso_libs = _bfs_group_and_liberties(false_board, 5, 0, 3)
        assert iso_libs == {(0, 2)}
        els.append(card(198, 110, 166, 144, rx=7, fill=CRIMSON_SOFT, stroke=CRIMSON))
        els.append(txt(281, 126, "✗ 断点未连 = 假眼必死！", size=9.3, color=CRIMSON, anchor="middle", weight="700"))
        ex2, ey2 = 230, 140
        _draw_go_grid(els, ex2, ey2, 5, es, pad=6)
        for (rr, rc), rcol in false_board.items():
            els.append(_stone(ex2 + rc * es, ey2 + rr * es, 6.4, rcol))
        els.append(txt(ex2, ey2 + 3.0, "真", size=8.0, color=GREEN, anchor="middle", weight="700"))
        els.append(f'<circle cx="{ex2 + 2 * es:.1f}" cy="{ey2:.1f}" r="5.2" fill="#ffffff" stroke="{CRIMSON}" stroke-width="1.5"/>')
        els.append(txt(ex2 + 2 * es, ey2 + 3.0, "假", size=8.0, color=CRIMSON, anchor="middle", weight="700"))
        els.append(txt(281, 226, "右上黑一子被卡住只剩“假”处1气", size=8.4, color=INK, anchor="middle"))
        els.append(txt(281, 241, "白可直接提掉它 → 黑只剩1眼净死", size=8.5, color=CRIMSON, anchor="middle", weight="700"))

        # Panel 2 (Top-Right): Seki (Mutual Life / 双活)
        els.append(card(388, 74, 356, 192))
        els.append(step_badge(404, 92, 2, PURPLE, PURPLE_SOFT))
        els.append(txt(420, 96, "双活（Seki）：都没两只眼，凭什么谁都不死？", size=11.0, color=PANEL_TITLE, weight="700"))

        # Exact 5x5 Seki in corner:
        # Black chain: (0,1),(1,1),(2,0) — wait: (2,0) not orthogonal to (1,1). Let's make 100% connected chains!
        # Black 3-stone chain: (0,1),(1,1),(1,0)? If (0,0) and (0,2) are empty? Let's construct cleanly:
        # Row 0..1, Col 0..2 (6 points total inside an outer White/Black wall):
        # Black chain at (0,0),(1,0),(1,1) -> 3 connected B stones!
        # White chain at (0,2),(0,3),(1,3) -> 3 connected W stones!
        # Shared empty points ("公气"): (0,1) and (1,2)!!
        # Outer wall sealing Black & White from outside liberties:
        # Row 2: White at (2,0),(2,1) sealing Black from below; Black at (2,2),(2,3),(2,4),(1,4),(0,4) sealing White from right/below!
        seki_b = {
            # Inner Black 3-stone chain
            (0, 0): "B",
            (1, 0): "B",
            (1, 1): "B",
            # Inner White 3-stone chain
            (0, 2): "W",
            (0, 3): "W",
            (1, 3): "W",
            # Outer White wall below inner Black (has plenty of outer liberties on row 3/4)
            (2, 0): "W",
            (2, 1): "W",
            (3, 0): "W",
            # Outer Black wall around inner White (has plenty of outer liberties on row 3/4)
            (2, 2): "B",
            (2, 3): "B",
            (2, 4): "B",
            (1, 4): "B",
            (0, 4): "B",
        }
        in_b_grp, in_b_libs = _bfs_group_and_liberties(seki_b, 5, 0, 0)
        in_w_grp, in_w_libs = _bfs_group_and_liberties(seki_b, 5, 0, 2)
        assert in_b_grp == {(0, 0), (1, 0), (1, 1)} and in_b_libs == {(0, 1), (1, 2)}
        assert in_w_grp == {(0, 2), (0, 3), (1, 3)} and in_w_libs == {(0, 1), (1, 2)}

        kx, ky, ks = 414, 128, 22.0
        _draw_go_grid(els, kx, ky, 5, ks, pad=8)
        for (rr, rc), rcol in seki_b.items():
            els.append(_stone(kx + rc * ks, ky + rr * ks, 7.8, rcol))
        for pname, (pr, pc) in (("公1", (0, 1)), ("公2", (1, 2))):
            els.append(f'<circle cx="{kx + pc * ks:.1f}" cy="{ky + pr * ks:.1f}" r="6.4" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.6"/>')
            els.append(txt(kx + pc * ks, ky + pr * ks + 2.8, pname, size=7.6, color=PURPLE, anchor="middle", weight="700"))

        els.append(card(526, 114, 206, 138, rx=7, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(535, 133, "博弈死锁（纳什均衡）：", size=9.4, color=PURPLE, weight="700"))
        els.append(txt(535, 152, "• 里圈三黑与三白都无真眼，", size=8.6, color=INK))
        els.append(txt(535, 169, "  恰好共享两口公气(公1、公2)；", size=8.6, color=INK))
        els.append(txt(535, 188, "• 若黑贪心落“公1”紧白气，黑", size=8.6, color=INK))
        els.append(txt(535, 205, "  瞬间只剩“公2”一气被白反提！", size=8.6, color=CRIMSON, weight="700"))
        els.append(txt(535, 224, "• 白先动手同理自毙 → 谁都不填", size=8.6, color=INK))
        els.append(txt(535, 241, "  停手共存，两块都算活棋！", size=8.8, color=PURPLE, weight="700"))

        # Panel 3 (Bottom full-width): Ko fight 4-stage strip
        els.append(card(16, 278, 728, 184))
        els.append(step_badge(32, 296, 3, ORANGE, ORANGE_SOFT))
        els.append(txt(48, 300, "打劫（Ko）与“禁止全局同形”：两张虎口互咬时，为什么不许立刻提回来？", size=11.0, color=PANEL_TITLE, weight="700"))

        # Standard 4x4 Ko shape:
        # Black tiger mouth: (0,1), (1,0), (2,1); White tiger mouth: (0,2), (1,3), (2,2)
        # Before Black captures: White stone at (1,1), empty at (1,2)!
        # Move 1: Black plays (1,2), capturing White (1,1)!
        # Immediate White (1,1) is FORBIDDEN because it recreates exact previous board!
        ko_base = {
            (0, 1): "B",
            (1, 0): "B",
            (2, 1): "B",
            (0, 2): "W",
            (1, 3): "W",
            (2, 2): "W",
        }
        ko_stages = [
            (32, "① 提劫前初始形", ko_base | {(1, 1): "W"}, (1, 2), "黑瞄准虎口准备提一子", BLUE),
            (210, "② 黑 1 提劫！", ko_base | {(1, 2): "B"}, (1, 1), "白子被提，但白禁立即回提×", CRIMSON),
            (388, "③ 寻劫与应劫", ko_base | {(1, 2): "B", (3, 0): "W", (3, 3): "B"}, None, "白2他处造劫材 → 黑3应一手", ORANGE),
            (566, "④ 全局已变：白4回提！", ko_base | {(1, 1): "W", (3, 0): "W", (3, 3): "B"}, (1, 2), "盘面多了2、3两子，合法回提", GREEN),
        ]
        for sx, stitle, sboard, mark_pt, snote, scol in ko_stages:
            els.append(card(sx, 314, 164, 136, rx=7, fill="#fafaf9", stroke=scol))
            els.append(txt(sx + 82, 330, stitle, size=9.3, color=scol, anchor="middle", weight="700"))
            gx, gy, gs = sx + 49, 344, 21.5
            _draw_go_grid(els, gx, gy, 4, gs, pad=6)
            for (rr, rc), rcol in sboard.items():
                lbl = None
                if stitle.startswith("②") and (rr, rc) == (1, 2):
                    lbl = "1"
                elif stitle.startswith("③") and (rr, rc) == (3, 0):
                    lbl = "2"
                elif stitle.startswith("③") and (rr, rc) == (3, 3):
                    lbl = "3"
                elif stitle.startswith("④") and (rr, rc) == (1, 1):
                    lbl = "4"
                els.append(_stone(gx + rc * gs, gy + rr * gs, 7.4, rcol, label=lbl))
            if mark_pt is not None:
                mr, mc = mark_pt
                mx, my = gx + mc * gs, gy + mr * gs
                if stitle.startswith("②"):
                    els.append(_line(mx - 4.5, my - 4.5, mx + 4.5, my + 4.5, stroke=CRIMSON, sw=2.2))
                    els.append(_line(mx - 4.5, my + 4.5, mx + 4.5, my - 4.5, stroke=CRIMSON, sw=2.2))
                else:
                    els.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="4.2" fill="none" stroke="{scol}" stroke-width="1.5" stroke-dasharray="2.5 2"/>')
            els.append(txt(sx + 82, 439, snote, size=8.6, color=INK, anchor="middle"))

        svg = figure(
            476,
            "围棋两只真眼活棋定理、双活纳什均衡与打劫禁止全局同形四步图解",
            "左上对比两只独立真眼（白落任一处皆因另一眼尚存气而构成禁入点，故黑永生）与断点未补的假眼死棋；右上展示双方共享两口公气、谁先动手谁自毙的双活（Seki）均衡；下排四步拆解虎口打劫（Ko）：黑1提劫后白禁止立即回提造成全局同形死循环，须先在别处寻劫（白2、黑3改变全局）后方能白4回提。",
            els,
        )
        write_svg(SUBDIR, "two-eyes-seki-and-ko-fight.svg", svg)

    def _build_chinese_vs_japanese_scoring():
        els = []
        els.extend(
            header(
                "一盘 7×7 终局手把手算胜负：中国“数子法” vs 日韩“数目法”",
                "为什么两边数法完全不同，算出来的胜负却严丝合缝？为什么黑贴 3¾ 子恰好等于黑贴 7.5 目？",
            )
        )

        # Construct an exact 7x7 finished board (49 points):
        # Columns 0..1 = Black territory (2*7 = 14? Wait: let's make an organic curvy boundary!)
        # Let's define each point of 7x7 explicitly and verify every stone's liberties & territory reachability!
        # Let Black occupy a wall of 14 stones enclosing 12 empty points on the left;
        # Let White occupy a wall of 13 stones enclosing 10 empty points on the right;
        # Total = 14 B + 12 B_empty + 13 W + 10 W_empty = 49!
        # Let's lay out row by row (7 rows, cols 0..6):
        # Row 0: . . B W . . .  -> 2 B_emp, 1 B, 1 W, 3 W_emp? Wait let's check totals per row:
        # Suppose B_emp per row (7 rows): [2, 2, 2, 2, 2, 1, 1] -> sum = 12 empty points!
        # Then first B stone per row is at col: [2, 2, 2, 2, 2, 1, 1] (7 B stones on the frontier!)
        # Plus 7 extra B stones inside/reinforcing (e.g. connecting step & realistic battle stones):
        # At row 4 col 2 is B, row 5 col 1 is B -> to connect orthogonally, put B at (5, 2) as well!
        # Wait if B is at (5,2), then (5,1) and (5,2) are both B! Let's write the exact 7x7 grid string and assert everything in Python!
        grid_rows = [
            "..BBW..",  # B_emp:2 (0,1), B:2 (2,3), W:1 (4), W_emp:2 (5,6)
            "..BWW..",  # B_emp:2 (0,1), B:1 (2),   W:2 (3,4), W_emp:2 (5,6)
            ".BBW...",  # B_emp:1 (0),   B:2 (1,2), W:1 (3), W_emp:3 (4,5,6) -> wait (2,4) touches (1,4)=W and (3,4)=W!
            "..BBWW.",  # B_emp:2 (0,1), B:2 (2,3), W:2 (4,5), W_emp:1 (6)
            "..BBW..",  # B_emp:2 (0,1), B:2 (2,3), W:1 (4), W_emp:2 (5,6)
            ".BBWW..",  # B_emp:1 (0),   B:2 (1,2), W:2 (3,4), W_emp:2 (5,6) -> wait W_emp so far: 2+2+3+1+2+2 = 12? Let's tune!
            "..BBWW.",
        ]
        # Let's craft the exact 7 rows so:
        # 1) Every empty '.' region on the left touches ONLY 'B', and its size is 12;
        # 2) Every empty '.' region on the right touches ONLY 'W', and its size is 10;
        # 3) Count('B') == 14, Count('W') == 13 (14 + 12 + 13 + 10 == 49!);
        # 4) Every 'B' group and 'W' group has >= 2 liberties!
        grid_rows = [
            "..BBWW.",  # B_e:2, B:2, W:2, W_e:1
            "..BBW..",  # B_e:2, B:2, W:1, W_e:2
            "..BBW..",  # B_e:2, B:2, W:1, W_e:2
            "..BBWW.",  # B_e:2, B:2, W:2, W_e:1
            ".BBWW..",  # B_e:1, B:2, W:2, W_e:2
            "..BBWW.",  # B_e:2, B:2, W:2, W_e:1
            ".BBWWW.",  # B_e:1, B:2, W:3, W_e:1
        ]
        # Wait let's check every empty point's orthogonal neighbors in grid_rows!
        # In row 4 ".BBWW..", (4,5) has neighbor (3,5)='W', (5,5)='W', (4,4)='W', (4,6)='.'!
        # Wait what about (3,1)='.' above (4,1)='B', and (4,0)='.' left of (4,1)='B' -> only touches B and '.'!
        # What about (1,5)='.' below (0,5)='W'? Touches W and '.'!
        # Let's verify programmatically with strict assertions!
        b_stones = set()
        w_stones = set()
        b_dict = {}
        for r, row in enumerate(grid_rows):
            assert len(row) == 7
            for c, ch in enumerate(row):
                if ch == "B":
                    b_stones.add((r, c))
                    b_dict[(r, c)] = "B"
                elif ch == "W":
                    w_stones.add((r, c))
                    b_dict[(r, c)] = "W"
        assert len(b_stones) == 14 and len(w_stones) == 13

        # Check all stones have liberties >= 2
        for r, c in b_stones | w_stones:
            _, libs = _bfs_group_and_liberties(b_dict, 7, r, c)
            assert len(libs) >= 2

        # Flood-fill empty regions to verify pure territory ownership!
        b_terr = set()
        w_terr = set()
        for r in range(7):
            for c in range(7):
                if (r, c) in b_dict:
                    continue
                # BFS through empty points to see what stone colors are reached
                seen_e = set()
                reached_colors = set()
                st = [(r, c)]
                while st:
                    er, ec = st.pop()
                    if (er, ec) in seen_e:
                        continue
                    seen_e.add((er, ec))
                    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        nr, nc = er + dr, ec + dc
                        if 0 <= nr < 7 and 0 <= nc < 7:
                            if (nr, nc) in b_dict:
                                reached_colors.add(b_dict[(nr, nc)])
                            elif (nr, nc) not in seen_e:
                                st.append((nr, nc))
                assert len(reached_colors) == 1, f"Neutral point found at {(r, c)}: {reached_colors}"
                if "B" in reached_colors:
                    b_terr.add((r, c))
                else:
                    w_terr.add((r, c))

        assert len(b_terr) == 12 and len(w_terr) == 10
        assert len(b_stones) + len(b_terr) + len(w_stones) + len(w_terr) == 49
        # Game history check: 15 moves each (total 30 moves played, 0 passes in main sequence):
        # Black played 15 stones, 1 captured by White -> 14 on board!
        # White played 15 stones, 2 captured by Black -> 13 on board!
        # Chinese Area Score: Black = 14 + 12 = 26, White = 13 + 10 = 23 -> Black - 24.5 = +1.5 stones (diff = +3)!
        # Japanese Territory Score: Black = 12 + 2 prisoners = 14, White = 10 + 1 prisoner = 11 -> diff = +3 points!
        assert (len(b_stones) + len(b_terr)) - (len(w_stones) + len(w_terr)) == 3
        assert (len(b_terr) + 2) - (len(w_terr) + 1) == 3

        # Left card: 7x7 finished board + prisoners
        els.append(card(16, 74, 294, 390))
        els.append(step_badge(32, 92, 1, BLUE, BLUE_SOFT))
        els.append(txt(48, 96, "终局棋盘实况（7×7 共 49 点，单官已收完）", size=10.8, color=PANEL_TITLE, weight="700"))

        gx, gy, gs = 56, 130, 30.0
        _draw_go_grid(els, gx, gy, 7, gs, pad=12, stars=[(3, 3)])
        for idx_e, (er, ec) in enumerate(sorted(b_terr), 1):
            ex, ey = gx + ec * gs, gy + er * gs
            els.append(f'<rect x="{ex - 5.2:.1f}" y="{ey - 5.2:.1f}" width="10.4" height="10.4" rx="2" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.3"/>')
            els.append(txt(ex, ey + 3.0, str(idx_e), size=7.6, color=BLUE, anchor="middle", weight="700", cls="mono"))
        for idx_w, (er, ec) in enumerate(sorted(w_terr), 1):
            ex, ey = gx + ec * gs, gy + er * gs
            els.append(f'<rect x="{ex - 5.2:.1f}" y="{ey - 5.2:.1f}" width="10.4" height="10.4" rx="2" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.3"/>')
            els.append(txt(ex, ey + 3.0, str(idx_w), size=7.6, color=ORANGE, anchor="middle", weight="700", cls="mono"))
        for sr, sc in sorted(b_stones):
            els.append(_stone(gx + sc * gs, gy + sr * gs, 10.6, "B"))
        for sr, sc in sorted(w_stones):
            els.append(_stone(gx + sc * gs, gy + sr * gs, 10.6, "W"))

        # Prisoner trays under 7x7 board
        els.append(card(32, 362, 262, 88, rx=7, fill="#f8fafc", stroke=BORDER))
        els.append(txt(44, 382, "对局记录：黑白各下 15 手（盘面无单官）", size=9.2, color=INK, weight="700"))
        els.append(txt(44, 403, "• 黑方俘虏盒（提掉的白死子）：", size=9.0, color=BODY))
        els.append(_stone(228, 399, 6.8, "W"))
        els.append(_stone(246, 399, 6.8, "W"))
        els.append(txt(262, 403, "2 颗", size=9.0, color=BLUE, weight="700"))
        els.append(txt(44, 426, "• 白方俘虏盒（提掉的黑死子）：", size=9.0, color=BODY))
        els.append(_stone(228, 422, 6.8, "B"))
        els.append(txt(262, 426, "1 颗", size=9.0, color=ORANGE, weight="700"))

        # Right-Top card: Chinese Area Scoring vs Japanese Territory Scoring
        els.append(card(322, 74, 422, 212))
        els.append(step_badge(338, 92, 2, GREEN, GREEN_SOFT))
        els.append(txt(354, 96, "同一盘棋两种数法（先不计贴目）：结果分毫不差！", size=11.0, color=PANEL_TITLE, weight="700"))

        # Sub-card A: Chinese Rules
        els.append(card(336, 112, 192, 160, rx=7, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(432, 130, "中国规则 · 数子法（算占地总面积）", size=9.5, color=BLUE, anchor="middle", weight="700"))
        els.append(txt(346, 150, "口诀：活子 + 围空（俘虏死子不用管）", size=8.8, color=INK, weight="700"))
        els.append(txt(346, 170, "• 黑总子数 = 14 活子 + 12 空 = 26 子", size=8.9, color=BLUE, weight="700"))
        els.append(txt(346, 188, "• 白总子数 = 13 活子 + 10 空 = 23 子", size=8.9, color=BODY))
        els.append(txt(346, 206, "• 棋盘半数（归本数）= 49 ÷ 2 = 24.5", size=8.8, color=MUTED))
        els.append(pill(346, 218, "黑超半数 26-24.5 = +1.5 子", fg=BLUE, bg="#ffffff", border=BLUE, w=172, h=24, size=8.9))
        els.append(txt(432, 258, "（黑白总地盘差 26 - 23 = +3 点）", size=8.6, color=INK, anchor="middle"))

        # Sub-card B: Japanese/Korean Rules
        els.append(card(538, 112, 192, 160, rx=7, fill=GREEN_SOFT, stroke=GREEN))
        els.append(txt(634, 130, "日韩规则 · 数目法（算净围空+俘虏）", size=9.5, color=GREEN, anchor="middle", weight="700"))
        els.append(txt(548, 150, "口诀：围空 + 提子（或死子回填敌空）", size=8.8, color=INK, weight="700"))
        els.append(txt(548, 170, "• 黑总目数 = 12 围空 + 2 俘虏 = 14 目", size=8.9, color=GREEN, weight="700"))
        els.append(txt(548, 188, "• 白总目数 = 10 围空 + 1 俘虏 = 11 目", size=8.9, color=BODY))
        els.append(txt(548, 206, "• 直接相减比谁净目多：14 vs 11", size=8.8, color=MUTED))
        els.append(pill(548, 218, "黑净胜 14 - 11 = +3 目！", fg=GREEN, bg="#ffffff", border=GREEN, w=172, h=24, size=8.9))
        els.append(txt(634, 258, "（1.5 子 × 2 = 3 目，完全等价！）", size=8.6, color=GREEN, anchor="middle", weight="700"))

        # Right-Bottom card: 19x19 Komi formula (3.75 stones == 7.5 points)
        els.append(card(322, 298, 422, 166))
        els.append(step_badge(338, 316, 3, ORANGE, ORANGE_SOFT))
        els.append(txt(354, 320, "秒懂 19 路大赛播报：为什么“黑贴 3¾ 子”就是“黑贴 7.5 目”？", size=10.8, color=PANEL_TITLE, weight="700"))
        els.append(card(338, 334, 390, 42, rx=6, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(
            txt(
                533,
                352,
                "恒等式：黑子 + 白子 = 361  ⇒  黑白差 (黑 - 白) = 2 × (黑 - 180.5)",
                size=9.4,
                color=ORANGE,
                anchor="middle",
                weight="700",
                cls="mono",
            )
        )
        els.append(txt(533, 369, "数子算“单方超半数 (黑 - 180.5)”；数目算“双方净差 (黑 - 白)”，恰好差 2 倍！", size=8.5, color=INK, anchor="middle"))

        els.append(txt(338, 395, "• 中国规则（2002）：黑贴 3¾ 子（3.75 子），过关线 = 180.5 + 3.75 = 184.25 子：", size=8.7, color=BODY))
        els.append(txt(348, 414, "— 黑数 185 子：185 - 184.25 = 黑胜 ¾ 子（×2 即黑胜 1.5 目！）", size=8.9, color=GREEN, weight="700"))
        els.append(txt(348, 432, "— 黑数 184 子：184 - 184.25 = 黑负 ¼ 子，即白胜 ¼ 子（白胜 0.5 目！）", size=8.9, color=CRIMSON, weight="700"))
        els.append(txt(338, 451, "• 日韩规则：现行黑贴 6.5 目；应氏规则：黑贴 8 点（平点白胜，等效 7.5 目）。", size=8.6, color=MUTED))

        svg = figure(
            478,
            "7×7围棋终局数子法与数目法逐点核算及19路黑贴3又4分之3子换算图",
            "左图构造一盘单官收完的7×7终局（黑14活子围12空提2白子，白13活子围10空提1黑子）；右上严格对比中国数子法（黑26子超半数24.5达+1.5子）与日韩数目法（黑14目减白11目净胜+3目），证明1子差等于2目差；右下推导19路361点黑贴3.75子（185子黑胜、184子白胜）与黑贴7.5目的精确2倍关系。",
            els,
        )
        write_svg(SUBDIR, "chinese-vs-japanese-scoring-7x7.svg", svg)

    def _build_history_and_alphago():
        els = []
        els.extend(
            header(
                "两千五百年棋道演进与 AI 破壁：从 17 道石盘、废除座子到 AlphaGo",
                "为什么国际象棋 1997 年就被深蓝攻克，而规则更简单的围棋却让人类顶尖棋手多守了整整 19 年？",
            )
        )

        # Top card: 5 historical milestones
        els.append(card(16, 74, 728, 186))
        els.append(step_badge(32, 92, 1, BLUE, BLUE_SOFT))
        els.append(txt(48, 96, "围棋形制与规则的五次历史定型（史料与考古实物双重印证）", size=11.2, color=PANEL_TITLE, weight="700"))

        milestones = [
            (30, "公元前548年", "先秦文献定名", ["《左传》襄公二十五年", "首载“弈者举棋不定”；", "《孟子》记国手弈秋，", "早期称“弈”后称围棋。"], BLUE, BLUE_SOFT),
            (172, "东汉—魏晋", "17×17 道石棋盘", ["河北望都东汉墓出土", "17道石盘（289点）；", "班固《弈旨》首论棋理，", "《艺经》载纵横十七道。"], GOLD, GOLD_SOFT),
            (314, "南北朝—隋唐", "19×19 道与十决", ["北周《敦煌碁经》载", "“三百六十一道”；安阳", "隋张盛墓(595)出白瓷盘；", "唐王积薪撰《围棋十决》。"], GREEN, GREEN_SOFT),
            (456, "17世纪—20世纪", "废座子·新布局·贴目", ["古棋先摆4颗星位座子；", "江户日本改空盘自由下，", "1933吴清源掀起新布局，", "现代确立先行贴目制。"], PURPLE, PURPLE_SOFT),
            (598, "2016—2017", "AlphaGo 零知识破壁", ["2016 胜李世石(4:1)，", "第37手五路肩冲惊天下；", "2017 Zero 仅凭基本规则", "自博弈 100:0 完胜前代！"], CRIMSON, CRIMSON_SOFT),
        ]
        # Horizontal timeline spine behind cards
        els.append(_line(90, 134, 670, 134, stroke=BORDER, sw=2.2))
        for mx, myear, mtitle, mlines, mcol, mbg in milestones:
            els.append(card(mx, 112, 134, 134, rx=7, fill=mbg, stroke=mcol))
            els.append(pill(mx + 12, 118, myear, fg=mcol, bg="#ffffff", border=mcol, w=110, h=20, size=8.5))
            els.append(txt(mx + 67, 154, mtitle, size=9.5, color=INK, anchor="middle", weight="700"))
            for li, ln in enumerate(mlines):
                els.append(txt(mx + 67, 173 + li * 16, ln, size=8.5, color=BODY, anchor="middle"))

        # Bottom-Left card: Why Chess fell in 1997 while Go held until 2016
        els.append(card(16, 272, 434, 182))
        els.append(step_badge(32, 290, 2, ORANGE, ORANGE_SOFT))
        els.append(txt(48, 294, "计算鸿沟：为什么暴力穷举在围棋面前彻底失效？", size=11.0, color=PANEL_TITLE, weight="700"))

        # Log10 comparison bars:
        # Chess legal states ~10^44, Observable Universe Atoms ~10^80, Go legal states 2.08x10^170!
        bars = [
            ("国际象棋合法局面 (~10^44)", 44, SLATE, "1997“深蓝”靠每秒2亿步α-β剪枝攻克"),
            ("可观测宇宙原子总数 (~10^80)", 80, BLUE, "全宇宙物质颗粒加起来也才80个零"),
            ("19路围棋精确合法局面 (2.08×10^170)", 170.3, CRIMSON, "足足171位十进制数！每步约250种选点"),
        ]
        max_log = 180.0
        for bi, (blabel, blog, bcol, bnote) in enumerate(bars):
            by0 = 316 + bi * 44
            els.append(txt(34, by0, blabel, size=9.2, color=INK, weight="700"))
            bw = (blog / max_log) * 392.0
            els.append(f'<rect x="34" y="{by0 + 6:.1f}" width="396" height="12" rx="6" fill="{SLATE_SOFT}"/>')
            els.append(f'<rect x="34" y="{by0 + 6:.1f}" width="{bw:.1f}" height="12" rx="6" fill="{bcol}"/>')
            els.append(txt(38, by0 + 30, bnote, size=8.5, color=MUTED))

        # Bottom-Right card: AlphaGo's Move 37 & Twin-Network MCTS insight
        els.append(card(462, 272, 282, 182))
        els.append(step_badge(478, 290, 3, GREEN, GREEN_SOFT))
        els.append(txt(494, 294, "AI 怎么看懂围棋？直觉 + 算路 + 第37手", size=10.8, color=PANEL_TITLE, weight="700"))

        # Mini 6x6 right-side slice showing famous fifth-line shoulder hit ("五路肩冲" Move 37 concept)
        mx0, my0, mstep = 476, 322, 18.0
        _draw_go_grid(els, mx0, my0, 6, mstep, pad=7, stars=[(3, 3)])
        # White stone on 4th line (row 3, col 2 from edge -> let's use col 3 as 4th line from right edge col 5: col index 5 is 1st line, col 4 is 2nd, col 3 is 3rd, col 2 is 4th, col 1 is 5th!)
        # Let's place White at (3, 2) [4th line] and Black Move 37 shoulder hit at (2, 1) [5th line!]
        els.append(_stone(mx0 + 2 * mstep, my0 + 2 * mstep, 6.6, "W"))
        els.append(_stone(mx0 + 3 * mstep, my0 + 4 * mstep, 6.6, "W"))
        els.append(_stone(mx0 + 2 * mstep, my0 + 0 * mstep, 6.6, "B"))
        els.append(_stone(mx0 + 1 * mstep, my0 + 1 * mstep, 7.0, "B", label="37", label_color="#fde68a"))
        els.append(f'<circle cx="{mx0 + 1 * mstep:.1f}" cy="{my0 + 1 * mstep:.1f}" r="9.2" fill="none" stroke="{CRIMSON}" stroke-width="1.4" stroke-dasharray="2.5 2"/>')

        els.append(txt(588, 326, "破局三剑客：", size=9.3, color=GREEN, weight="700"))
        els.append(txt(588, 344, "1. 策略网络：像人类棋感，", size=8.6, color=INK))
        els.append(txt(588, 359, "   从250点筛出几步好点；", size=8.6, color=INK))
        els.append(txt(588, 377, "2. 价值网络：不数子力，直", size=8.6, color=INK))
        els.append(txt(588, 392, "   接评估整盘胜率厚薄；", size=8.6, color=INK))
        els.append(txt(588, 410, "3. 树搜索+自博弈：打破", size=8.6, color=INK))
        els.append(txt(588, 425, "   “布局禁下五路”古训，", size=8.6, color=INK))
        els.append(txt(588, 440, "   反哺今天人类职业棋坛！", size=8.6, color=CRIMSON, weight="700"))

        svg = figure(
            468,
            "围棋两千五百年历史演进时间轴与AlphaGo突破10的170次方状态空间图解",
            "上排梳理公元前548年《左传》定名、东汉望都墓17道石盘、北周《敦煌碁经》与隋代张盛墓19道瓷盘、江户废除座子与1933新布局及贴目制、直至2016–2017年AlphaGo与AlphaGo Zero的五次跃迁；左下按对数尺度对比国际象棋(~10^44)、可观测宇宙原子(~10^80)与19路围棋精确合法局面(2.08×10^170)；右下解析策略网络+价值网络+MCTS与著名的五路肩冲第37手。",
            els,
        )
        write_svg(SUBDIR, "weiqi-2500-years-to-alphago.svg", svg)

    @register(
        "weiqi-intro-rules",
        "围棋入门与规则全景：19路棋盘几何效率、气与提子单次动画、两眼双活与打劫推论、7路终局数子vs数目核算及2500年演进与AlphaGo",
        "humanities",
    )
    def build_weiqi_intro_rules():
        _build_board_geometry_and_zones()
        _build_liberties_capture_and_forbidden_anim()
        _build_two_eyes_seki_and_ko_fight()
        _build_chinese_vs_japanese_scoring()
        _build_history_and_alphago()


_register_daguanlou_couplet()
_register_poetry_boom_7080s()
_register_european_name_patterns()
_register_weiqi_intro_rules()


def _register_art_as_generalized_encoding():
    SUBDIR = "art-as-generalized-encoding"

    PURPLE_MARKER = f"""<marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="{PURPLE}"/>
  </marker>"""

    def _build_information_ladder():
        els = []
        els.extend(header(
            "图像是更泛化的文字：从“一匹马”看懂四级广义编码阶梯",
            "左看二维并置图像与一维线性文字的同源对比，右按 ①→④ 看差异痕迹怎样一步步升华为意义",
        ))

        # Left comparison panel: 2D parallel image vs 1D serial text of "a horse"
        els.append(card(24, 68, 252, 364, rx=10, fill=CARD_BG, stroke=BORDER))
        els.append(txt(40, 92, "同一匹“马”的两种编码接口", 12.8, INK, weight="700"))

        # Sub-card A: 2D parallel image matrix + dynamic contour
        els.append(card(38, 106, 224, 134, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(pill(48, 115, "二维图像编码（并置场）", fg=BLUE, bg="#ffffff", w=146, h=22, size=10.2))
        gx, gy, cell = 50, 146, 9
        horse_pixels = {
            (7, 0), (8, 0),
            (6, 1), (7, 1), (8, 1),
            (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
            (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
            (0, 4), (2, 4), (6, 4),
            (2, 5), (5, 5), (7, 5),
            (1, 6), (5, 6), (8, 6),
        }
        els.append(f'<rect x="{gx - 2}" y="{gy - 2}" width="{10 * cell + 4}" height="{7 * cell + 4}" rx="4" fill="#ffffff" stroke="{BORDER}"/>')
        for r in range(7):
            for c in range(10):
                fill = BLUE if (c, r) in horse_pixels else "#f8fafc"
                els.append(
                    f'<rect x="{gx + c * cell}" y="{gy + r * cell}" width="{cell - 1}" height="{cell - 1}" fill="{fill}"/>'
                )
        els.append(txt(154, 162, "空间同时并置", 10.2, INK, weight="700"))
        els.append(txt(154, 181, "一眼给出比例", 10.0, BODY))
        els.append(txt(154, 200, "动势与留白场", 10.0, BODY))
        els.append(txt(48, 229, "长处：保留连续几何拓扑与整体张力", 9.6, MUTED))

        # Sub-card B: 1D linearized discrete text stream
        els.append(card(38, 250, 224, 126, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(pill(48, 259, "一维文字编码（串行流）", fg=PURPLE, bg="#ffffff", w=146, h=22, size=10.2))
        els.append(card(48, 290, 68, 52, rx=6, fill="#ffffff", stroke=PURPLE))
        # Stylized early pictograph strokes of 马
        els.append(
            f'<path d="M68,296 C78,294 88,299 92,307 C84,311 74,311 66,309 '
            f'M74,310 L72,325 M82,310 L82,325 M90,308 L95,324 M64,316 L58,324" '
            f'fill="none" stroke="{PURPLE}" stroke-width="1.8" stroke-linecap="round"/>'
        )
        els.append(txt(82, 338, "象形轮廓", 8.8, MUTED, anchor="middle"))
        els.append(_line(120, 316, 138, 316, stroke=PURPLE, sw=1.6, marker="arr-purple"))
        els.append(card(144, 290, 106, 52, rx=6, fill="#ffffff", stroke=PURPLE))
        els.append(txt(197, 314, "「白 马」", 13.0, PURPLE, weight="700", anchor="middle"))
        els.append(txt(197, 333, "11100111…", 9.2, MUTED, anchor="middle", cls="mono"))
        els.append(txt(48, 364, "长处：离散符号组合、否定与因果推理", 9.6, MUTED))

        els.append(txt(150, 398, "汉字本身就曾从二维图画线性化而来", 10.0, INK, weight="700", anchor="middle"))
        els.append(txt(150, 416, "底层相通：都在用有限差异编码世界关系", 9.6, MUTED, anchor="middle"))

        # Right panel: 4-step generalized encoding ladder
        lanes = [
            (
                1,
                "物理载体与差异痕迹",
                "可观测差异",
                "宣纸墨迹、屏幕像素矩阵、空气声压波、石材凿痕",
                "香农通信层：只要状态有可区分差异，就能充当编码载体",
                BLUE,
                BLUE_SOFT,
                "arr-blue",
            ),
            (
                2,
                "形式模式与知觉张力",
                "并置与节律",
                "边缘轮廓、冷暖对比、疏密比例、留白与运动趋势",
                "格式塔知觉层：眼睛与耳朵主动把零散刺激组织成“力与形”",
                PURPLE,
                PURPLE_SOFT,
                "arr-purple",
            ),
            (
                3,
                "符号指向与语法惯例",
                "编码与约定",
                "肖像相似、光影因果痕迹、词汇语法、透视与和声法则",
                "皮尔士符号层：差异不再只指自身，开始跨向外部对象与概念",
                ORANGE,
                ORANGE_SOFT,
                "arr-orange",
            ),
            (
                4,
                "观者重构与审美顿悟",
                "意义生成层",
                "调动个人记忆、身体经验与文化语境，补全画外之音",
                "艺术发生层：有限符号在解释者心中重新展开为一整个鲜活世界",
                GREEN,
                GREEN_SOFT,
                None,
            ),
        ]
        for idx, (num, title, tag, line1, line2, col, soft, arr) in enumerate(lanes):
            cy_top = 68 + idx * 96
            els.append(card(292, cy_top, 444, 76, rx=9, fill=soft, stroke=col))
            els.append(step_badge(313, cy_top + 22, num, fg=col, bg="#ffffff", r=10.5))
            els.append(txt(331, cy_top + 26, title, 12.4, col, weight="700"))
            els.append(pill(612, cy_top + 11, tag, fg=col, bg="#ffffff", w=110, h=21, size=10.0))
            els.append(txt(331, cy_top + 48, line1, 10.6, INK, weight="600"))
            els.append(txt(331, cy_top + 66, line2, 9.8, MUTED))
            if arr is not None:
                els.append(_line(514, cy_top + 78, 514, cy_top + 92, stroke=col, sw=1.8, marker=arr))

        els.append(card(24, 444, 712, 50, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(40, 464, "核心结论：文字是高度离散化的图像，图像是保留空间并置的广义文字——整个感知世界都在收发编码。", 10.8, INK, weight="700"))
        els.append(txt(40, 483, "香农统计熵只度量第 ① 层符号的不确定性消除；艺术的神奇恰恰诞生在 ①→④ 跨层压缩与重构的跃迁里。", 10.0, MUTED))

        return figure(
            506,
            "同一匹马的图像文字编码对比与四级广义编码阶梯图解",
            "左侧对比二维图像像素场与一维文字串行编码，右侧按 ① 物理痕迹、② 形式模式、③ 符号指向、④ 观者重构展示广义编码阶梯。",
            els,
            extra_defs=PURPLE_MARKER,
        )

    def _build_three_sign_relations():
        els = []
        els.extend(header(
            "图像为什么既像文字又不止于文字？皮尔士符号三角与三重混合编码",
            "先看左栏 ①“符号—对象—解释项”三元闭环，再看右栏 ②③④ 三种指向关系如何在艺术品中叠合",
        ))

        # Left panel: Peirce's triadic sign relation
        els.append(card(24, 68, 248, 342, rx=10, fill=CARD_BG, stroke=BORDER))
        els.append(step_badge(43, 90, 1, fg=PURPLE, bg=PURPLE_SOFT, r=10.0))
        els.append(txt(59, 94, "符号不是死电线：三元闭环", 12.2, INK, weight="700"))

        # Top vertex: Interpretant
        els.append(card(78, 122, 140, 52, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
        els.append(txt(148, 143, "解释项 Interpretant", 10.5, PURPLE, weight="700", anchor="middle"))
        els.append(txt(148, 162, "观者脑中唤起的理解", 9.6, INK, anchor="middle"))

        # Bottom-left vertex: Representamen
        els.append(card(34, 252, 98, 52, rx=8, fill=BLUE_SOFT, stroke=BLUE))
        els.append(txt(83, 273, "符号载体", 10.8, BLUE, weight="700", anchor="middle"))
        els.append(txt(83, 292, "画痕 / 字词", 9.6, INK, anchor="middle"))

        # Bottom-right vertex: Object
        els.append(card(164, 252, 98, 52, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(213, 273, "所指对象", 10.8, ORANGE, weight="700", anchor="middle"))
        els.append(txt(213, 292, "事物 / 经验", 9.6, INK, anchor="middle"))

        # Mediated solid arrows + bottom dashed non-automatic link
        els.append(_line(88, 248, 124, 179, stroke=BLUE, sw=1.8, marker="arr-purple"))
        els.append(_line(172, 178, 207, 247, stroke=PURPLE, sw=1.8, marker="arr-orange"))
        els.append(_line(135, 278, 161, 278, stroke=MUTED, sw=1.5, dash="4 3"))
        els.append(txt(148, 324, "虚线：脱离解释过程，符号无法自动指物", 9.4, MUTED, anchor="middle"))

        els.append(card(36, 338, 224, 60, rx=7, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(148, 357, "皮尔士核心洞见：意义不在颜料里，", 9.8, INK, weight="700", anchor="middle"))
        els.append(txt(148, 375, "而在“符号→解释项→对象”的动态关联中；", 9.5, BODY, anchor="middle"))
        els.append(txt(148, 391, "解释项本身还会成为下一轮思考的新符号。", 9.4, MUTED, anchor="middle"))

        # Right 3 columns: Icon, Index, Symbol
        cols = [
            (
                2,
                "像似符 Icon",
                "靠“结构相似”指向",
                "写实肖像、山水轮廓",
                "几何图示、旋律起伏线",
                ["保留对象的几何拓扑", "或关系同构；跨语言", "门槛低，一眼可认出", "“画的是远山与流水”"],
                BLUE,
                BLUE_SOFT,
            ),
            (
                3,
                "指示符 Index",
                "靠“因果痕迹”指向",
                "狂草飞白、厚涂刀痕",
                "胶片光痕、古陶匠人指印",
                ["与物理事件直接相连：", "枯笔记录手腕疾徐，", "银盐记录当时光子，", "自带“在场真实感”"],
                ORANGE,
                ORANGE_SOFT,
            ),
            (
                4,
                "规约符 Symbol",
                "靠“社会约定”指向",
                "自然语言文字、数学记号",
                "岁寒三友、礼制与圣像色标",
                ["外形与对象无需相似；", "靠文化共同体习得规", "则，可精密表达抽象", "概念、隐喻与反讽"],
                GREEN,
                GREEN_SOFT,
            ),
        ]
        for i, (num, title, rel, ex1, ex2, mech_lines, col, soft) in enumerate(cols):
            x = 286 + i * 154
            els.append(card(x, 68, 142, 342, rx=10, fill=soft, stroke=col))
            els.append(step_badge(x + 18, 90, num, fg=col, bg="#ffffff", r=9.5))
            els.append(txt(x + 33, 94, title, 11.8, col, weight="700"))
            els.append(txt(x + 71, 118, rel, 10.6, INK, weight="700", anchor="middle"))

            # Mini visual illustration canvas
            vx, vy, vw, vh = x + 14, 130, 114, 92
            els.append(card(vx, vy, vw, vh, rx=7, fill="#ffffff", stroke=col))
            if i == 0:
                # Mountain contour + sun + water ripples (structural resemblance)
                els.append(f'<circle cx="{vx + 86}" cy="{vy + 24}" r="9" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.4"/>')
                els.append(
                    f'<path d="M{vx + 10},{vy + 68} L{vx + 38},{vy + 30} L{vx + 58},{vy + 54} '
                    f'L{vx + 80},{vy + 24} L{vx + 104},{vy + 68} Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.8" stroke-linejoin="round"/>'
                )
                els.append(_line(vx + 18, vy + 78, vx + 96, vy + 78, stroke=BLUE, sw=1.3, dash="6 3"))
            elif i == 1:
                # Dynamic calligraphic brush trace + causal motion arrow
                els.append(
                    f'<path d="M{vx + 18},{vy + 70} C{vx + 36},{vy + 26} {vx + 68},{vy + 22} {vx + 96},{vy + 54}" '
                    f'fill="none" stroke="{ORANGE}" stroke-width="5.5" stroke-linecap="round"/>'
                )
                els.append(
                    f'<path d="M{vx + 62},{vy + 34} C{vx + 78},{vy + 34} {vx + 88},{vy + 43} {vx + 99},{vy + 56}" '
                    f'fill="none" stroke="#ffffff" stroke-width="1.6" stroke-dasharray="4 2"/>'
                )
                els.append(_line(vx + 22, vy + 78, vx + 90, vy + 78, stroke=SLATE, sw=1.3, marker="arr-orange"))
                els.append(txt(vx + 57, vy + 20, "运笔速度 → 飞白肌理", 8.8, MUTED, anchor="middle"))
            else:
                # Conventional tokens: text + cultural metaphor equation
                els.append(card(vx + 12, vy + 14, 90, 30, rx=5, fill=GREEN_SOFT, stroke=GREEN))
                els.append(txt(vx + 57, vy + 34, "「梅 / 松 / 竹」", 10.6, GREEN, weight="700", anchor="middle"))
                els.append(txt(vx + 57, vy + 60, "约定俗成 ↓ 文化隐喻", 8.8, MUTED, anchor="middle"))
                els.append(txt(vx + 57, vy + 79, "清高 · 坚韧 · 气节", 9.8, INK, weight="700", anchor="middle"))

            els.append(txt(x + 71, 242, ex1, 9.8, INK, weight="600", anchor="middle"))
            els.append(txt(x + 71, 259, ex2, 9.6, BODY, anchor="middle"))

            els.append(card(x + 10, 274, 122, 124, rx=6, fill="#ffffff", stroke=BORDER))
            els.append(txt(x + 71, 293, "编码机制", 9.8, col, weight="700", anchor="middle"))
            for li, ml in enumerate(mech_lines):
                els.append(txt(x + 71, 314 + li * 19, ml, 9.4, MUTED, anchor="middle"))

        els.append(card(24, 422, 712, 62, rx=8, fill=SLATE_SOFT, stroke=BORDER))
        els.append(txt(40, 444, "真实艺术品几乎都是三重叠合——以一幅水墨寒梅或纪实摄影为例：", 10.8, INK, weight="700"))
        els.append(txt(40, 466, "枝干面容轮廓是像似符（认出物象）＋ 枯笔飞白/快门曝光是指示符（触摸身体与现场）＋ 题诗典故与构图传统是规约符（读出深意）。", 9.9, BODY))

        return figure(
            496,
            "皮尔士符号三角与像似符指示符规约符三重混合编码图解",
            "左侧展示符号载体、所指对象与解释项构成的三元闭环，右侧对比像似符、指示符、规约符的编码机制及艺术作品中的三重叠合。",
            els,
            extra_defs=PURPLE_MARKER,
        )

    def _build_order_complexity():
        els = []
        els.extend(header(
            "为什么“绝对整齐”乏味、“雪花白噪”刺眼？秩序、熵与审美张力的倒 U 曲线",
            "上排对比三种 8×5 编码样本的香农熵与规律度，下排看温特—伯莱恩倒 U 型曲线与伯克霍夫公式的边界",
        ))

        # Helper to render an 8x5 mini grid pattern
        def _grid_sample(gx, gy, active_cells, accent_cells, col):
            out = [f'<rect x="{gx - 2}" y="{gy - 2}" width="76" height="49" rx="4" fill="#ffffff" stroke="{BORDER}"/>']
            for r in range(5):
                for c in range(8):
                    if (c, r) in accent_cells:
                        fill = ORANGE
                    elif (c, r) in active_cells:
                        fill = col
                    else:
                        fill = "#f1f5f9"
                    out.append(f'<rect x="{gx + c * 9}" y="{gy + r * 9}" width="8" height="8" fill="{fill}"/>')
            return "\n".join(out)

        # Sample 1: Strict periodic stripes (20/40 cells, trivial period-2 rule)
        s1_cells = {(c, r) for r in range(5) for c in range(8) if c % 2 == 0}
        # Sample 2: Asymmetric mountain ridge + negative space + single focal sun cell
        s2_cells = {
            (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
            (1, 3), (2, 3), (3, 3), (4, 3),
            (2, 2), (3, 2),
            (2, 1),
        }
        s2_accent = {(6, 1)}
        # Sample 3: Deterministic 50/50 white-noise sample (exact 20/40 = 1.00 bit/cell, low run structure)
        noise_bits = [
            1, 0, 1, 1, 0, 0, 1, 0,
            0, 1, 0, 1, 1, 0, 0, 1,
            1, 1, 0, 0, 1, 0, 1, 0,
            0, 0, 1, 0, 1, 1, 0, 1,
            1, 0, 0, 1, 0, 1, 1, 0,
        ]
        assert sum(noise_bits) == 20 and len(noise_bits) == 40
        s3_cells = {(idx % 8, idx // 8) for idx, bit in enumerate(noise_bits) if bit == 1}

        samples = [
            (24, 1, "机械重复", s1_cells, set(), BLUE, BLUE_SOFT, "统计熵低", "0 意外", "一眼看穿规则，迅速乏味"),
            (190, 2, "秩序×破格", s2_cells, s2_accent, PURPLE, PURPLE_SOFT, "熵值适中", "结构丰富", "留白与焦点并存，张力最高"),
            (356, 3, "随机白噪声", s3_cells, set(), ORANGE, ORANGE_SOFT, "熵 H=1 bit", "有效结构≈0", "差异极多却无规律可抓"),
        ]
        for sx, num, name, cells, acc, col, soft, m1, m2, foot in samples:
            sw = 1.5 if num == 2 else 1.0
            els.append(card(sx, 68, 152, 112, rx=9, fill=soft, stroke=col, sw=sw))
            els.append(step_badge(sx + 16, 85, num, fg=col, bg="#ffffff", r=9.0))
            els.append(txt(sx + 30, 89, name, 11.0, col, weight="700"))
            els.append(_grid_sample(sx + 12, 100, cells, acc, col))
            els.append(txt(sx + 94, 116, m1, 9.4, INK, weight="700"))
            els.append(txt(sx + 94, 136, m2, 9.4, col if num == 2 else MUTED, weight="600"))
            els.append(txt(sx + 76, 168, foot, 9.2, INK if num == 2 else MUTED, weight="600" if num == 2 else None, anchor="middle"))

        # Main Wundt-Berlyne / Effective Complexity Inverted-U Plot
        els.append(card(24, 192, 484, 246, rx=10, fill=CARD_BG, stroke=BORDER))
        px0, py0, pw, ph = 68, 228, 412, 164
        y_axis = py0 + ph  # 392

        # Sweet-spot shaded zone u in [0.33, 0.67]
        sx1 = px0 + 0.33 * pw
        sx2 = px0 + 0.67 * pw
        els.append(f'<rect x="{sx1:.1f}" y="{py0}" width="{sx2 - sx1:.1f}" height="{ph}" rx="6" fill="{PURPLE_SOFT}" opacity="0.6"/>')

        # Axes
        els.append(_line(px0, y_axis, px0 + pw, y_axis, stroke=SLATE, sw=1.5))
        els.append(_line(px0, y_axis, px0, py0 - 6, stroke=SLATE, sw=1.5))
        els.append(txt(px0 - 6, py0 - 14, "审美张力 / 有效复杂度（可习得规律的丰富度）", 10.2, SLATE, weight="700"))

        # Computed inverted-U curve: v(u) = 0.08 + 0.88 * sin(pi * u)^1.35
        def _curve_pt(u):
            v = 0.08 + 0.88 * (math.sin(math.pi * u) ** 1.35)
            return px0 + u * pw, y_axis - v * 154.0

        pts = [_curve_pt(k / 60.0) for k in range(61)]
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        els.append(f'<polyline points="{poly}" fill="none" stroke="{PURPLE}" stroke-width="2.6" stroke-linecap="round"/>')

        # Three landmark points on the curve
        p1x, p1y = _curve_pt(0.12)
        p2x, p2y = _curve_pt(0.50)
        p3x, p3y = _curve_pt(0.88)
        for px, py, col in [(p1x, p1y, BLUE), (p2x, p2y, PURPLE), (p3x, p3y, ORANGE)]:
            els.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6.5" fill="#ffffff" stroke="{col}" stroke-width="2.4"/>')

        els.append(txt(p1x - 28, p1y - 10, "① 太刻板", 10.0, BLUE, weight="700", anchor="middle", halo=True))
        els.append(txt(p2x, p2y + 26, "② 艺术黄金张力甜区", 10.6, PURPLE, weight="700", anchor="middle", halo=True))
        els.append(txt(p2x, p2y + 44, "半熟悉·半陌生（可压缩的新奇）", 9.4, INK, weight="600", anchor="middle", halo=True))
        els.append(txt(p3x + 28, p3y - 10, "③ 太混乱", 10.0, ORANGE, weight="700", anchor="middle", halo=True))

        # X-axis labels cleanly inside card (y_axis=392, card bottom=438)
        els.append(txt(px0 + 4, y_axis + 17, "低熵（死板对称）", 9.4, MUTED))
        els.append(txt(px0 + pw / 2, y_axis + 34, "无序度 / 香农统计熵 H（从完全可预测 → 彻底随机）", 9.8, SLATE, weight="700", anchor="middle"))
        els.append(txt(px0 + pw - 4, y_axis + 17, "高熵（纯白噪声）", 9.4, MUTED, anchor="end"))

        # Right sidebar: Birkhoff M=O/C vs Gell-Mann Effective Complexity + Cultural Shift
        els.append(card(522, 68, 214, 370, rx=10, fill=SLATE_SOFT, stroke=BORDER))
        els.append(step_badge(540, 89, 4, fg=PURPLE, bg="#ffffff", r=9.5))
        els.append(txt(555, 93, "两代数学模型的启发与边界", 11.4, INK, weight="700"))

        els.append(card(534, 108, 190, 102, rx=8, fill="#ffffff", stroke=BORDER))
        els.append(txt(546, 127, "伯克霍夫审美度量（1933）", 10.0, PURPLE, weight="700"))
        els.append(txt(629, 153, "M = O / C", 14.5, PURPLE, weight="700", anchor="middle"))
        els.append(txt(546, 174, "O：对称、重复、比例等秩序", 9.4, INK))
        els.append(txt(546, 193, "C：感知识别结构所耗的努力", 9.4, MUTED))

        els.append(card(534, 220, 190, 102, rx=8, fill="#ffffff", stroke=BORDER))
        els.append(txt(546, 239, "盖尔曼有效复杂度（1996）", 10.0, BLUE, weight="700"))
        els.append(txt(546, 259, "只度量“可提取规律”的丰富度：", 9.4, INK))
        els.append(txt(546, 278, "雪花噪点虽总熵最大，但规律为", 9.4, MUTED))
        els.append(txt(546, 297, "零，故有效复杂度与美感俱归零", 9.4, MUTED))

        els.append(card(534, 332, 190, 94, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
        els.append(txt(546, 351, "为什么公式不能当审美裁判？", 9.9, ORANGE, weight="700"))
        els.append(txt(546, 371, "观者经验会移动横轴位置：初听", 9.3, INK))
        els.append(txt(546, 389, "复调觉乱（偏 ③），听懂对位法", 9.3, INK))
        els.append(txt(546, 407, "后便落回 ② 号高张力峰值区", 9.3, INK))

        els.append(card(24, 450, 712, 50, rx=8, fill=PURPLE_SOFT, stroke="#c4b5fd"))
        els.append(txt(40, 470, "关键区分：香农统计熵衡量“下一格有多难猜”，艺术张力衡量“意外之中藏着多深的秩序”。", 10.8, INK, weight="700"))
        els.append(txt(40, 489, "好作品既不靠机械套路哄睡感知，也不靠纯随机噪声瘫痪理解，而是在熟悉与陌生交界处搭桥。", 9.9, BODY))

        return figure(
            512,
            "三种网格样本对比与秩序熵审美张力倒U型曲线图解",
            "通过机械重复、秩序破格与随机白噪声三种 8×5 样本，配合温特—伯莱恩倒 U 型曲线、伯克霍夫公式与有效复杂度，解释审美张力的来源与个体文化边界。",
            els,
        )

    def _build_compression_prediction():
        els = []
        els.extend(header(
            "艺术为什么是最神奇的压缩？少画十倍细节，反而展开百倍世界",
            "上排按 ①→④ 看“有选择的降维编码 + 观者先验解压”，下排对比工程保真压缩与审美顿悟跃迁",
        ))

        # Top 4-stage pipeline container
        els.append(card(24, 68, 712, 190, rx=10, fill=CARD_BG, stroke=BORDER))
        stages = [
            (
                1,
                "高维原始经验",
                "无限细节流",
                ["山川光影、声响气味", "身体冷暖与时间绵延", "（原始维度近乎无穷）"],
                BLUE,
                BLUE_SOFT,
                "arr-purple",
            ),
            (
                2,
                "审美取舍与留白",
                "关系蒸馏器",
                ["主动舍弃冗余枝蔓", "只抓动势、冲突转折", "与“计白当黑”的缺口"],
                PURPLE,
                PURPLE_SOFT,
                "arr-orange",
            ),
            (
                3,
                "低比特符号载体",
                "作品编码层",
                ["寥寥数笔水墨蝌蚪", "二十八字绝句、和弦", "车座与车把拼成牛头"],
                ORANGE,
                ORANGE_SOFT,
                "arr-green",
            ),
            (
                4,
                "观者先验解压",
                "脑内高维重构",
                ["调动记忆与文化先验", "听见画外“十里蛙声”", "展开一整个精神世界"],
                GREEN,
                GREEN_SOFT,
                None,
            ),
        ]
        for i, (num, title, subtag, lines, col, soft, arr) in enumerate(stages):
            sx = 38 + i * 176  # width 152, gap 24 -> rightmost 566..718
            els.append(card(sx, 82, 152, 144, rx=8, fill=soft, stroke=col))
            els.append(step_badge(sx + 17, 101, num, fg=col, bg="#ffffff", r=9.5))
            els.append(txt(sx + 32, 105, title, 11.2, col, weight="700"))
            els.append(pill(sx + 20, 117, subtag, fg=col, bg="#ffffff", w=112, h=20, size=9.6))
            for li, ln in enumerate(lines):
                els.append(txt(sx + 76, 158 + li * 20, ln, 9.7, INK if li < 2 else MUTED, weight="600" if li == 0 else None, anchor="middle"))
            if arr is not None:
                els.append(_line(sx + 155, 154, sx + 172, 154, stroke=col, sw=1.9, marker=arr))

        els.append(txt(380, 246, "贡布里希“观者的本分”：艺术家故意留出结构缺口，观者用一生经验完成最后一步高倍解码。", 10.2, INK, weight="700", anchor="middle"))

        # Bottom-left: Engineering lossless/perceptual compression
        els.append(card(24, 272, 344, 220, rx=10, fill=SLATE_SOFT, stroke=BORDER))
        els.append(pill(38, 286, "对照 A：工程数据压缩（保真复刻）", fg=SLATE, bg="#ffffff", w=224, h=22, size=10.0))
        els.append(txt(38, 326, "代表：PNG 无损预测 / JPEG 频域余弦量化", 10.5, INK, weight="700"))
        els.append(txt(38, 348, "• 压缩对象：统计重复像素与人眼不敏感高频分量", 9.8, BODY))
        els.append(txt(38, 369, "• 解码准则：所有设备还原出的画面越一致越成功", 9.8, BODY))
        els.append(txt(38, 390, "• 认知影响：只搬运像素，不要求重构观者的世界模型", 9.8, BODY))

        els.append(card(38, 406, 316, 72, rx=7, fill="#ffffff", stroke=BORDER))
        els.append(txt(196, 430, "原图 X (24 MB)  →  码流 (1.2 MB)  →  还原图 X̂", 10.0, BLUE, weight="700", anchor="middle"))
        els.append(txt(196, 452, "优化目标：像素重构误差 d(X, X̂) → 0", 9.6, INK, weight="600", anchor="middle"))
        els.append(txt(196, 470, "（忠实存档，不追求“言外之意”）", 9.2, MUTED, anchor="middle"))

        # Bottom-right: Artistic compression & Schmidhuber compression progress (Aha!)
        els.append(card(382, 272, 354, 220, rx=10, fill=PURPLE_SOFT, stroke="#c4b5fd"))
        els.append(pill(396, 286, "对照 B：艺术压缩与“顿悟压缩跃迁”", fg=PURPLE, bg="#ffffff", w=234, h=22, size=10.0))

        # Mini step-drop plot of subjective description length L(x; C_t)
        els.append(card(396, 316, 326, 98, rx=7, fill="#ffffff", stroke=PURPLE))
        gx0, gy0, gw, gh = 434, 330, 272, 66
        els.append(_line(gx0, gy0 + gh, gx0 + gw, gy0 + gh, stroke=SLATE, sw=1.3))
        els.append(_line(gx0, gy0 + gh, gx0, gy0, stroke=SLATE, sw=1.3))
        els.append(txt(gx0 - 6, gy0 + 10, "描述", 8.8, SLATE, anchor="end"))
        els.append(txt(gx0 - 6, gy0 + 22, "长度", 8.8, SLATE, anchor="end"))
        # Step-drop curve: high plateau L_before -> steep insight drop -> low plateau L_after
        step_pts = [
            (gx0 + 8, gy0 + 16),
            (gx0 + 112, gy0 + 16),
            (gx0 + 132, gy0 + 44),
            (gx0 + 262, gy0 + 44),
        ]
        sp_str = " ".join(f"{x},{y}" for x, y in step_pts)
        els.append(f'<polyline points="{sp_str}" fill="none" stroke="{PURPLE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        els.append(_line(gx0 + 144, gy0 + 17, gx0 + 144, gy0 + 41, stroke=GREEN, sw=1.8, marker="arr-green"))
        els.append(txt(gx0 + 60, gy0 + 11, "顿悟前 L_前（线索零散）", 9.0, ORANGE, weight="700", anchor="middle"))
        els.append(txt(gx0 + 208, gy0 + 27, "ΔL = L_前 − L_后 > 0", 9.8, GREEN, weight="700", anchor="middle"))
        els.append(txt(gx0 + 208, gy0 + 59, "顿悟后 L_后（一通百通）", 9.0, PURPLE, weight="700", anchor="middle"))

        els.append(txt(396, 434, "• 齐白石不画蛙只画溪中蝌蚪；毕加索用旧车座配车把秒变公牛头", 9.6, INK, weight="600"))
        els.append(txt(396, 455, "• 当零散细节突然被一个新结构统摄，主观描述长度瞬间坍缩 ΔL > 0", 9.6, BODY))
        els.append(txt(396, 476, "• 这股“认知压缩率跃升”释放的惊喜与快感，就是审美里的顿悟（Aha!）", 9.6, PURPLE, weight="700"))

        return figure(
            504,
            "艺术四步有损压缩解压流程与顿悟描述长度跃迁对比图解",
            "上排展示高维原始经验经审美取舍、低比特符号载体到观者先验解压的四步流程；下排对比工程像素保真压缩与艺术通过描述长度骤降触发顿悟的机制。",
            els,
            extra_defs=PURPLE_MARKER,
        )

    def _build_art_as_insight_loop():
        css = """
      @keyframes stepReveal {
        0% { opacity: 0.78; }
        50% { opacity: 1; }
        100% { opacity: 1; }
      }
      @keyframes ahaHalo {
        0% { opacity: 0.15; stroke-dashoffset: 28; }
        60% { opacity: 1; stroke-dashoffset: 0; }
        100% { opacity: 0.92; stroke-dashoffset: 0; }
      }
      .cyc-s1 { animation: stepReveal 0.55s ease-out 0.10s 1 both; }
      .cyc-s2 { animation: stepReveal 0.55s ease-out 0.55s 1 both; }
      .cyc-s3 { animation: stepReveal 0.55s ease-out 1.00s 1 both; }
      .cyc-s4 { animation: stepReveal 0.55s ease-out 1.45s 1 both; }
      .aha-halo { stroke-dasharray: 6 4; animation: ahaHalo 1.1s ease-out 1.85s 1 both; }
      @media (prefers-reduced-motion: reduce) {
        .cyc-s1, .cyc-s2, .cyc-s3, .cyc-s4, .aha-halo {
          animation: none !important;
          opacity: 1 !important;
          stroke-dashoffset: 0 !important;
        }
      }"""
        els = []
        els.extend(header(
            "艺术到底是什么？“作品—观者—世界—文化”的四元循环与顿悟闭环",
            "外圈 ①→④ 展示意义如何在四个节点间流转生长，中心展示预测碰撞点亮的顿悟时刻（支持减少动态效果）",
        ))

        cx, cy, r = 380, 244, 72
        # Outer persistent highlight ring + central hub
        els.append(f'<circle cx="{cx}" cy="{cy}" r="81" fill="none" stroke="{PURPLE}" stroke-width="2" class="aha-halo"/>')
        els.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="2.2"/>')
        els.append(txt(cx, cy - 18, "顿悟时刻 Aha!", 15.0, PURPLE, weight="700", anchor="middle"))
        els.append(txt(cx, cy + 5, "旧模型重组 · 误差骤降", 10.0, INK, weight="700", anchor="middle"))
        els.append(txt(cx, cy + 25, "ΔL = L_前 − L_后 > 0", 9.6, PURPLE, weight="600", anchor="middle"))

        # Four corner node cards (w=192, h=86)
        nodes = [
            (36, 82, 1, "作品结构", "凝聚差异、留白与张力", "提供可感知的符号表面", BLUE, BLUE_SOFT, "cyc-s1"),
            (532, 82, 2, "观者解码", "带入记忆、身体与预期", "主动补全并检验旧假设", ORANGE, ORANGE_SOFT, "cyc-s2"),
            (532, 320, 3, "真实世界", "自然万物、历史与生活", "不断提供新经验与反例", GREEN, GREEN_SOFT, "cyc-s3"),
            (36, 320, 4, "文化共同体", "沉淀母语、传统与典故", "划定可共享的解释边界", SLATE, SLATE_SOFT, "cyc-s4"),
        ]
        for nx, ny, num, title, l1, l2, col, soft, cls in nodes:
            els.append(f'<g class="{cls}">')
            els.append(card(nx, ny, 192, 86, rx=10, fill=soft, stroke=col))
            els.append(step_badge(nx + 18, ny + 21, num, fg=col, bg="#ffffff", r=9.5))
            els.append(txt(nx + 34, ny + 25, title, 12.0, col, weight="700"))
            els.append(txt(nx + 16, ny + 50, l1, 10.0, INK, weight="600"))
            els.append(txt(nx + 16, ny + 70, l2, 9.5, MUTED))
            els.append("</g>")

        # Outer clockwise cycle arrows (strictly outside cards)
        els.append(_line(234, 114, 524, 114, stroke=BLUE, sw=1.8, marker="arr-orange"))
        els.append(txt(380, 104, "输出编码线索与意外缺口 →", 9.8, BLUE, weight="600", anchor="middle"))

        els.append(_line(646, 174, 646, 312, stroke=ORANGE, sw=1.8, marker="arr-green"))
        els.append(txt(656, 248, "刷新观看视角", 9.6, ORANGE, weight="600"))

        els.append(_line(524, 374, 236, 374, stroke=GREEN, sw=1.8, marker="arr-muted"))
        els.append(txt(380, 394, "← 生活巨变催生新的表达惯例", 9.8, GREEN, weight="600", anchor="middle"))

        els.append(_line(114, 314, 114, 176, stroke=SLATE, sw=1.8, marker="arr-blue"))
        els.append(txt(124, 248, "提供母题与法则", 9.6, SLATE, weight="600"))

        # Four radial arrows computed precisely from outside card corners to outside r=84
        els.append(_line(232, 170, 304, 206, stroke=BLUE, sw=1.7, dash="4 3", marker="arr-purple"))
        els.append(_line(528, 170, 456, 206, stroke=ORANGE, sw=1.7, dash="4 3", marker="arr-purple"))
        els.append(_line(528, 318, 456, 282, stroke=GREEN, sw=1.7, dash="4 3", marker="arr-purple"))
        els.append(_line(232, 318, 304, 282, stroke=SLATE, sw=1.7, dash="4 3", marker="arr-purple"))

        els.append(card(24, 426, 712, 62, rx=8, fill=PURPLE_SOFT, stroke="#c4b5fd"))
        els.append(txt(40, 448, "一句话回答“艺术到底是什么”：艺术不是锁在玻璃柜里的标准答案，而是一套活的跨层编码装置——", 10.8, INK, weight="700"))
        els.append(txt(40, 470, "它把浩瀚经验压缩成有张力的符号结构，只等某位观者带着人生走来，在解释中轰然展开一整个新世界。", 10.0, BODY))

        return figure(
            500,
            "作品观者真实世界与文化共同体围绕顿悟时刻的意义循环图解",
            "以作品结构、观者解码、真实世界和文化共同体四个节点构成外圈循环，四条径向虚线汇聚到中心顿悟时刻，说明艺术意义在动态解释中生成。",
            els,
            extra_css=css,
            extra_defs=PURPLE_MARKER,
        )

    @register(
        "art-as-generalized-encoding",
        "艺术到底是什么：图像、文字、音乐与建筑作为广义编码、符号解释、秩序复杂度压缩和顿悟循环",
        "humanities",
    )
    def build_art_as_generalized_encoding():
        write_svg(SUBDIR, "information-ladder-and-art.svg", _build_information_ladder())
        write_svg(SUBDIR, "image-text-icon-index-symbol.svg", _build_three_sign_relations())
        write_svg(SUBDIR, "order-complexity-aesthetic-tension.svg", _build_order_complexity())
        write_svg(SUBDIR, "art-compression-and-insight.svg", _build_compression_prediction())
        write_svg(SUBDIR, "art-meaning-cycle-and-aha.svg", _build_art_as_insight_loop())


_register_art_as_generalized_encoding()
