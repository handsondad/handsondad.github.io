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


_register_daguanlou_couplet()
_register_poetry_boom_7080s()
_register_european_name_patterns()
