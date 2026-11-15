"""Original 760px Chinese SVG diagrams for the Greek Tragedy post."""

import math
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
    MUTED,
    ORANGE,
    ORANGE_SOFT,
    PURPLE,
    PURPLE_SOFT,
    SLATE,
    SLATE_SOFT,
    WIDTH,
    card,
    figure,
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "greek-tragedy"


def _verify_greek_tragedy_math():
    """Programmatically verify numerical, structural, and historical invariants."""
    # 1. Pairwise dialogue channels among (k speaking actors + 1 chorus leader)
    # Stage 0 (dithyramb, k=0): 0 actor-to-anyone dialogue channels
    # Stage 1 (k=1): C(2, 2) = 1 channel (Actor 1 <-> Chorus leader)
    # Stage 2 (k=2): C(3, 2) = 3 channels (A1-A2, A1-Chorus, A2-Chorus)
    # Stage 3 (k=3): C(4, 2) = 6 channels (A1-A2, A1-A3, A2-A3, + 3 with Chorus)
    channels = [0 if k == 0 else math.comb(k + 1, 2) for k in range(4)]
    assert channels == [0, 1, 3, 6], f"Unexpected channel progression: {channels}"

    # 2. City Dionysia tragic tetralogy competition structure
    poets = 3
    tragedies_per_poet = 3
    satyr_per_poet = 1
    plays_per_day = tragedies_per_poet + satyr_per_poet
    total_plays = poets * plays_per_day
    assert plays_per_day == 4 and total_plays == 12

    # 3. Epidaurus seating geometry (34 lower rows + 21 upper rows = 55 rows)
    lower_rows, upper_rows = 34, 21
    assert lower_rows + upper_rows == 55
    ratio = lower_rows / upper_rows
    assert abs(ratio - 1.6190476) < 1e-5

    # 4. Extant manuscripts arithmetic:
    # Aeschylus 7 + Sophocles 7 + Euripides 19 (18 tragedies + 1 satyr play Cyclops) = 33
    aeschylus_extant = 7
    sophocles_extant = 7
    euripides_tragedies = 18
    euripides_satyr = 1
    euripides_extant = euripides_tragedies + euripides_satyr
    total_extant = aeschylus_extant + sophocles_extant + euripides_extant
    assert euripides_extant == 19 and total_extant == 33

    # Transmission streams: 24 Byzantine school select plays (7 + 7 + 10) + 9 alphabetic plays = 33
    byzantine_select = 7 + 7 + 10
    euripides_alphabetic = 9
    assert byzantine_select == 24
    assert byzantine_select + euripides_alphabetic == total_extant


def _build_evolution_svg():
    el = []
    el.extend(
        header(
            "从酒神合唱到三演员交锋：希腊悲剧怎样一步步“长”出戏剧冲突？",
            "每增加 1 名演员，台上对话通道按组合数 C(n+1, 2) 跃升（含歌队长）；底部附“山羊之歌”词源三假说",
        )
    )

    stages = [
        {
            "num": "1",
            "title": "酒神颂齐唱",
            "era": "前 7—前 6 世纪",
            "fg": SLATE,
            "bg": SLATE_SOFT,
            "actors": 0,
            "stat1": "演员 0 人｜歌队 50 人",
            "stat2": "对话通道：0 条",
            "lines": [
                "纯第三人称集体吟唱：",
                "“大家听，酒神当年……”",
                "只有叙事赞歌，尚无角色",
            ],
        },
        {
            "num": "2",
            "title": "第 1 位演员跨出",
            "era": "约前 534 年·泰斯庇斯",
            "fg": BLUE,
            "bg": BLUE_SOFT,
            "actors": 1,
            "stat1": "演员 1 人｜歌队长应答",
            "stat2": "对话通道：1 条",
            "lines": [
                "首创“应答者”戴面具：",
                "“我就是酒神本人！”",
                "后台换面具可分饰多角",
            ],
        },
        {
            "num": "3",
            "title": "第 2 位演员登场",
            "era": "前 5 世纪初·埃斯库罗斯",
            "fg": ORANGE,
            "bg": ORANGE_SOFT,
            "actors": 2,
            "stat1": "演员 2 人｜歌队 12 人",
            "stat2": "对话通道：3 条",
            "lines": [
                "两角色首次当面交锋！",
                "《诗学》：对话自此取代",
                "合唱跃升为全剧重心",
            ],
        },
        {
            "num": "4",
            "title": "第 3 位演员与景画",
            "era": "前 460 年代·索福克勒斯",
            "fg": GREEN,
            "bg": GREEN_SOFT,
            "actors": 3,
            "stat1": "演员 3 人｜歌队 15 人",
            "stat2": "对话通道：6 条",
            "lines": [
                "实现争辩＋旁听＋反讽",
                "定型“三演员铁律”：仅",
                "3 男演员分饰全剧角色",
            ],
        },
    ]

    cw = 169
    gap = 12
    y0 = 66
    ch = 336

    for idx, st in enumerate(stages):
        x = 24 + idx * (cw + gap)
        cx = x + cw / 2
        el.append(card(x, y0, cw, ch, stroke=st["fg"] if idx >= 2 else BORDER, sw=1.2 if idx >= 2 else 1))
        el.append(step_badge(x + 20, y0 + 22, st["num"], fg=st["fg"], bg=st["bg"]))
        el.append(txt(x + 37, y0 + 26, st["title"], size=13, color=INK, weight="700"))
        el.append(txt(cx, y0 + 46, st["era"], size=11, color=MUTED, anchor="middle"))

        # Stage diagram box
        bx, by, bw, bh = x + 11, y0 + 58, cw - 22, 122
        el.append(card(bx, by, bw, bh, rx=8, fill="#f8fafc", stroke=HAIRLINE))

        mcx, mcy = bx + bw / 2, by + bh / 2
        if st["actors"] == 0:
            # 12 chorus dots on circle around altar
            el.append(f'<circle cx="{mcx:.1f}" cy="{mcy:.1f}" r="36" fill="none" stroke="{HAIRLINE}" stroke-dasharray="3 3"/>')
            for k in range(12):
                ang = 2 * math.pi * k / 12
                px = mcx + 36 * math.cos(ang)
                py = mcy + 36 * math.sin(ang)
                el.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.2" fill="{SLATE}"/>')
            el.append(f'<circle cx="{mcx:.1f}" cy="{mcy:.1f}" r="9" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.2"/>')
            el.append(txt(mcx, mcy + 3.5, "坛", size=10, color=ORANGE, anchor="middle", weight="700"))
        elif st["actors"] == 1:
            ax, ay = bx + 34, mcy
            kx, ky = bx + bw - 38, mcy
            el.append(f'<line x1="{ax + 14:.1f}" y1="{ay:.1f}" x2="{kx - 16:.1f}" y2="{ky:.1f}" stroke="{BLUE}" stroke-width="2"/>')
            # Chorus arc behind chorus leader
            for dy in (-26, -13, 13, 26):
                el.append(f'<circle cx="{kx + 18:.1f}" cy="{ky + dy:.1f}" r="3.6" fill="{SLATE}"/>')
            el.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="13" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
            el.append(txt(ax, ay + 4, "A1", size=11, color=BLUE, anchor="middle", weight="700"))
            el.append(f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="13" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.3"/>')
            el.append(txt(kx, ky + 4, "歌", size=11, color=SLATE, anchor="middle", weight="700"))
            el.append(txt((ax + kx) / 2, ay - 12, "一问一答", size=10.5, color=BLUE, anchor="middle", weight="600"))
        elif st["actors"] == 2:
            a1x, a1y = mcx - 38, by + 38
            a2x, a2y = mcx + 38, by + 38
            kx, ky = mcx, by + 94
            el.append(f'<line x1="{a1x:.1f}" y1="{a1y:.1f}" x2="{kx:.1f}" y2="{ky:.1f}" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
            el.append(f'<line x1="{a2x:.1f}" y1="{a2y:.1f}" x2="{kx:.1f}" y2="{ky:.1f}" stroke="{SLATE}" stroke-width="1.3" stroke-dasharray="4 3"/>')
            el.append(f'<line x1="{a1x + 13:.1f}" y1="{a1y:.1f}" x2="{a2x - 13:.1f}" y2="{a2y:.1f}" stroke="{ORANGE}" stroke-width="2.4"/>')
            for px, py, lbl, fg, bg in [
                (a1x, a1y, "A1", ORANGE, ORANGE_SOFT),
                (a2x, a2y, "A2", ORANGE, ORANGE_SOFT),
                (kx, ky, "歌", SLATE, SLATE_SOFT),
            ]:
                el.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="12.5" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>')
                el.append(txt(px, py + 4, lbl, size=10.5, color=fg, anchor="middle", weight="700"))
            el.append(txt(mcx, a1y - 16, "正面冲突", size=10.5, color=ORANGE, anchor="middle", weight="700"))
        else:
            pts = [
                (mcx - 42, by + 32, "A1", GREEN, GREEN_SOFT),
                (mcx + 42, by + 32, "A2", GREEN, GREEN_SOFT),
                (mcx - 32, by + 92, "A3", BLUE, BLUE_SOFT),
                (mcx + 32, by + 92, "歌", SLATE, SLATE_SOFT),
            ]
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    is_actor_pair = i < 3 and j < 3
                    col = GREEN if is_actor_pair else HAIRLINE
                    sw = "1.9" if is_actor_pair else "1.2"
                    dash = "" if is_actor_pair else ' stroke-dasharray="3 3"'
                    el.append(
                        f'<line x1="{pts[i][0]:.1f}" y1="{pts[i][1]:.1f}" '
                        f'x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}" '
                        f'stroke="{col}" stroke-width="{sw}"{dash}/>'
                    )
            for px, py, lbl, fg, bg in pts:
                el.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="12" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>')
                el.append(txt(px, py + 4, lbl, size=10.5, color=fg, anchor="middle", weight="700"))

        el.append(pill(x + 12, y0 + 190, st["stat1"], fg=st["fg"], bg=st["bg"], w=cw - 24, h=22, size=11))
        el.append(txt(cx, y0 + 230, st["stat2"], size=12, color=st["fg"], anchor="middle", weight="700"))
        for li, line in enumerate(st["lines"]):
            el.append(txt(cx, y0 + 256 + li * 22, line, size=11.2, color=BODY, anchor="middle"))

    # Bottom etymology panel
    ey, eh = 416, 126
    el.append(card(24, ey, 712, eh, fill="#fffdf9", stroke=ORANGE, sw=1.1))
    el.append(
        txt(
            40,
            ey + 24,
            "词源悬案：为什么“悲剧（Tragōidia）”字面意思是“公山羊（tragos）之歌（ōidē）”？学界三大假说并存：",
            size=12.2,
            color=INK,
            weight="700",
        )
    )
    hyps = [
        ("① 奖品／祭品说（古典传统）", "早期合唱竞赛以活山羊为奖品，", "或开演前绕坛宰杀公山羊献祭酒神", ORANGE, ORANGE_SOFT),
        ("② 羊人侍从说（《诗学》线索）", "歌队曾披羊皮扮酒神随从萨堤尔，", "从诙谐歌舞逐渐蜕变为严肃悲剧", BLUE, BLUE_SOFT),
        ("③ 少年变声说（温克勒现代假说）", "雅典青年受训兵组成歌队，变声期", "破音在古希腊语中称“像山羊叫”", PURPLE, PURPLE_SOFT),
    ]
    for hi, (htitle, h1, h2, hfg, hbg) in enumerate(hyps):
        hx = 38 + hi * 231
        el.append(card(hx, ey + 36, 222, 78, rx=8, fill=hbg, stroke=hfg, sw=0.9))
        el.append(txt(hx + 111, ey + 56, htitle, size=11.5, color=hfg, anchor="middle", weight="700"))
        el.append(txt(hx + 111, ey + 78, h1, size=11, color=BODY, anchor="middle"))
        el.append(txt(hx + 111, ey + 98, h2, size=11, color=BODY, anchor="middle"))

    svg = figure(
        556,
        "古希腊悲剧从酒神合唱到三演员戏剧的演化与词源三假说",
        "展示古希腊悲剧从50人酒神颂合唱（0名演员）经泰斯庇斯第1演员、埃斯库罗斯第2演员到索福克勒斯第3演员的对话通道倍增过程，以及山羊之歌词源的三种学术假说。",
        el,
    )
    write_svg(SUBDIR, "dionysus-to-three-actors-evolution.svg", svg)


def _build_city_dionysia_svg():
    el = []
    el.extend(
        header(
            "不只是看戏，更是全城民主大审视：雅典“城邦酒神节”运作与竞赛机制",
            "每年早春航海季（3 月底—4 月初）全城停工：执政官选本、富豪包歌队、穷人领津贴、十部落抽签定冠军",
        )
    )

    # Left panel: Civic governance & funding
    el.append(card(24, 66, 350, 448))
    el.append(txt(42, 92, "一、谁选戏、谁出钱、谁打分？（城邦公事四环）", size=13.5, color=INK, weight="700"))

    steps = [
        (
            "1",
            "名年执政官选拔（提前半年“授予歌队”）",
            "最高行政官审读剧本提纲，选定 3 位悲剧诗人入围；",
            "落选即无缘当年大节（名家索福克勒斯亦须申报）。",
            BLUE,
            BLUE_SOFT,
        ),
        (
            "2",
            "歌队资助人制度（Choregia 富豪公益义务）",
            "指定 3 位富豪公民自费承担 12–15 名公民歌队员数月",
            "食宿、排练与华服（前 472 年青年伯里克利资助《波斯人》）。",
            ORANGE,
            ORANGE_SOFT,
        ),
        (
            "3",
            "观剧津贴（Theorika 全民入场保障）",
            "门票约 2 欧博尔（相当于劳工日薪），城邦向贫困公民",
            "发放津贴，让上万公民共同在剧场审视伦理与政治。",
            GREEN,
            GREEN_SOFT,
        ),
        (
            "4",
            "十部落双层抽签评委（防贿赂机制）",
            "10 个部落各抽 1 名评委投票密封；执政官终场随机只",
            "抽出 5 票计分定胜负——一半归民意，一半留给神意。",
            PURPLE,
            PURPLE_SOFT,
        ),
    ]
    for i, (num, stitle, l1, l2, fg, bg) in enumerate(steps):
        sy = 108 + i * 98
        el.append(card(40, sy, 318, 84, rx=8, fill="#f8fafc", stroke=fg, sw=1))
        el.append(step_badge(58, sy + 22, num, fg=fg, bg=bg, r=9.5))
        el.append(txt(74, sy + 26, stitle, size=12, color=fg, weight="700"))
        el.append(txt(50, sy + 50, l1, size=11.2, color=BODY))
        el.append(txt(50, sy + 70, l2, size=11.2, color=BODY))
        if i < 3:
            el.append(f'<line x1="199" y1="{sy + 84}" x2="199" y2="{sy + 98}" stroke="{MUTED}" stroke-width="1.3" marker-end="url(#arr-muted)"/>')

    # Right panel: Festival schedule & 3+1 tetralogy
    el.append(card(388, 66, 348, 448))
    el.append(txt(406, 92, "二、早春赛程与“3 悲 + 1 羊”四联剧配方", size=13.5, color=INK, weight="700"))

    # Pre-play civic ceremony box
    el.append(card(404, 108, 316, 104, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1))
    el.append(txt(418, 130, "正赛前奏：全城迎神游行 ＋ 帝国政治大秀", size=12, color=BLUE, weight="700"))
    el.append(txt(418, 152, "• 迎酒神木像夜游入场 ＋ 10 部落千人酒神颂合唱赛", size=11.2, color=BODY))
    el.append(txt(418, 174, "• 剧场中央公开陈列盟邦贡银、表彰城邦功臣", size=11.2, color=BODY))
    el.append(txt(418, 196, "• 阵亡将士遗孤满 18 岁获赠全套铠甲，列队巡场", size=11.2, color=BODY))

    # 3 competition days box
    el.append(card(404, 224, 316, 214, rx=8, fill="#ffffff", stroke=ORANGE, sw=1.2))
    el.append(txt(418, 246, "连续 3 个悲剧竞赛日：每位诗人独占 1 整天！", size=12, color=ORANGE, weight="700"))

    day_rows = [
        ("清晨 ① 悲剧一", "铺陈神话困局与家族／城邦裂痕", BLUE, BLUE_SOFT),
        ("上午 ② 悲剧二", "冲突激化，英雄一步步逼近临界点", BLUE, BLUE_SOFT),
        ("午后 ③ 悲剧三", "终局审判或毁灭（三部合称三联剧）", BLUE, BLUE_SOFT),
        ("傍晚 ④ 萨堤尔剧", "半人半羊歌队荒诞嬉闹，释放悲伤！", ORANGE, ORANGE_SOFT),
    ]
    for ri, (tag, desc_txt, rfg, rbg) in enumerate(day_rows):
        ry = 262 + ri * 34
        el.append(pill(416, ry, tag, fg=rfg, bg=rbg, w=116, h=24, size=11))
        el.append(txt(540, ry + 16, desc_txt, size=11.2, color=BODY))

    el.append(f'<line x1="418" y1="404" x2="706" y2="404" stroke="{HAIRLINE}" stroke-width="1"/>')
    el.append(
        txt(
            562,
            425,
            "3 天正赛总计：3 位诗人 × 4 部戏 = 12 部大戏连演",
            size=11.5,
            color=INK,
            anchor="middle",
            weight="700",
        )
    )

    # Victory inscription box
    el.append(card(404, 450, 316, 50, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1))
    el.append(txt(562, 471, "终场荣耀：获胜资助人与诗人同刻大理石《胜利名录》", size=11.3, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(562, 491, "头戴常春藤花冠，其声望在雅典堪比奥林匹克夺冠", size=11, color=BODY, anchor="middle"))

    svg = figure(
        530,
        "雅典城邦酒神节五天运作与四联剧竞赛机制图解",
        "左栏展示名年执政官选拔、富豪歌队资助人制度、观剧津贴与十部落双层抽签评委；右栏展示开场公民政治仪式与连续三天每位诗人上演三部悲剧加一部萨堤尔剧的赛制。",
        el,
    )
    write_svg(SUBDIR, "athens-city-dionysia-civic-machine.svg", svg)


def _wedge_path(cx, cy, r_in, r_out, deg_start, deg_end):
    """Build SVG path for a semicircular theater seating ring."""
    a1 = math.radians(deg_start)
    a2 = math.radians(deg_end)
    x1_out, y1_out = cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)
    x2_out, y2_out = cx + r_out * math.cos(a2), cy + r_out * math.sin(a2)
    x2_in, y2_in = cx + r_in * math.cos(a2), cy + r_in * math.sin(a2)
    x1_in, y1_in = cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)
    large_arc = 1 if abs(deg_end - deg_start) > 180 else 0
    return (
        f"M {x1_out:.1f} {y1_out:.1f} "
        f"A {r_out} {r_out} 0 {large_arc} 1 {x2_out:.1f} {y2_out:.1f} "
        f"L {x2_in:.1f} {y2_in:.1f} "
        f"A {r_in} {r_in} 0 {large_arc} 0 {x1_in:.1f} {y1_in:.1f} Z"
    )


def _build_theater_architecture_svg():
    el = []
    el.extend(
        header(
            "没有扩音器，一万四千人怎么听清台词？古希腊露天剧场空间与三大机关",
            "左：依山开凿的半圆扇形声学剧场平面（按埃皮达鲁斯 34+21=55 排比例）；右：面具、推车与吊车",
        )
    )

    # Left panel: Spatial floor plan
    el.append(card(24, 66, 388, 466))
    el.append(txt(42, 92, "一、露天剧场空间布局（俯视平面构造）", size=13.5, color=INK, weight="700"))

    cx, cy = 218, 274
    # Upper seating tier (21 rows): angles 192 deg to 348 deg (opening upward in SVG y<cy)
    # Note in SVG y-down coordinates: 192 deg is slightly below left horizontal, going clockwise through 270 (top) to 348 (slightly below right horizontal) -> span = 156? Wait: 192 -> 270 -> 348 is 156 deg; 168 -> 270 -> 372 (12 deg) is 204 deg (>180 deg wraparound!).
    deg_s, deg_e = 168, 372
    el.append(f'<path d="{_wedge_path(cx, cy, 108, 146, deg_s, deg_e)}" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.2"/>')
    el.append(f'<path d="{_wedge_path(cx, cy, 56, 100, deg_s, deg_e)}" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.3"/>')

    # Radial stairways (klimakes)
    for deg in range(186, 360, 28):
        rad = math.radians(deg)
        x_in, y_in = cx + 56 * math.cos(rad), cy + 56 * math.sin(rad)
        x_out, y_out = cx + 146 * math.cos(rad), cy + 146 * math.sin(rad)
        el.append(f'<line x1="{x_in:.1f}" y1="{y_in:.1f}" x2="{x_out:.1f}" y2="{y_out:.1f}" stroke="#ffffff" stroke-width="1.4"/>')

    # Labels on seating tiers (with white halo so radial lines never obscure characters)
    el.append(txt(cx, cy - 122, "上层看台 Epitheatron（21 排）", size=11.2, color=SLATE, anchor="middle", weight="700", halo=True))
    el.append(txt(cx, cy - 76, "下层看台 Theatron（34 排，“观看之所”）", size=11.5, color=BLUE, anchor="middle", weight="700", halo=True))

    # Central Orchestra & Altar
    el.append(f'<circle cx="{cx}" cy="{cy}" r="42" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
    el.append(txt(cx, cy - 16, "乐池 Orchestra", size=11.2, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(cx, cy + 20, "12–15 人歌队歌舞", size=10.2, color=BODY, anchor="middle"))
    el.append(f'<circle cx="{cx}" cy="{cy + 1}" r="5" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.2"/>')

    # Side entrances (Parodoi)
    el.append(card(54, cy + 32, 92, 24, rx=5, fill="#fff7ed", stroke=ORANGE, sw=1))
    el.append(txt(100, cy + 48, "左通道 Parodos", size=10.5, color=ORANGE, anchor="middle", weight="600"))
    el.append(card(290, cy + 32, 92, 24, rx=5, fill="#fff7ed", stroke=ORANGE, sw=1))
    el.append(txt(336, cy + 48, "右通道 Parodos", size=10.5, color=ORANGE, anchor="middle", weight="600"))

    # Proskenion & Skene
    el.append(card(126, cy + 62, 184, 22, rx=4, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.1))
    el.append(txt(cx, cy + 77, "台口演区 Proskenion（3 演员交锋）", size=10.8, color=ORANGE, anchor="middle", weight="700"))
    el.append(card(116, cy + 86, 204, 34, rx=6, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.2))
    el.append(txt(cx, cy + 107, "景屋 Skene（换面具后台＋宫殿立面＋平顶神坛）", size=10.8, color=PURPLE, anchor="middle", weight="700"))

    # Acoustics & archaeology note box
    el.append(card(38, 412, 360, 106, rx=8, fill="#f8fafc", stroke=HAIRLINE))
    el.append(txt(50, 433, "考古与声学真相：", size=11.8, color=INK, weight="700"))
    el.append(txt(50, 454, "• 雅典酒神剧场前 5 世纪初为木看台与近梯形乐池，前 4 世纪改石阶；", size=10.8, color=BODY))
    el.append(txt(50, 474, "• 埃皮达鲁斯（前 4 世纪）55 排石阶容约 1.4 万人，石灰岩座位呈波纹", size=10.8, color=BODY))
    el.append(txt(50, 494, "  结构：滤除人群低频嗡鸣，把演员高频辅音清晰反射到顶排。", size=10.8, color=BODY))

    # Right panel: Three stagecraft technologies
    el.append(card(426, 66, 310, 466))
    el.append(txt(444, 92, "二、三大舞台黑科技", size=13.5, color=INK, weight="700"))

    # Tech 1: Mask
    el.append(card(442, 108, 278, 122, rx=8, fill="#f8fafc", stroke=BLUE, sw=1))
    # Mask icon
    el.append(f'<ellipse cx="474" cy="168" rx="18" ry="23" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.5"/>')
    el.append(f'<circle cx="467" cy="161" r="2.6" fill="{BLUE}"/><circle cx="481" cy="161" r="2.6" fill="{BLUE}"/>')
    el.append(f'<path d="M466,179 Q474,171 482,179" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    el.append(txt(504, 130, "① 亚麻面具（Prosopon）", size=12, color=BLUE, weight="700"))
    el.append(txt(504, 152, "• 夸张五官轮廓，百米外一眼辨角色", size=11, color=BODY))
    el.append(txt(504, 173, "• 3 男演员秒换男女老少 6–10 角", size=11, color=BODY))
    el.append(txt(504, 194, "• 纠偏：古典面具嘴孔适中，主要靠", size=10.8, color=MUTED))
    el.append(txt(504, 212, "  剧场声学而非“喇叭嘴”扩音", size=10.8, color=MUTED))

    # Tech 2: Ekkyklema
    el.append(card(442, 244, 278, 130, rx=8, fill="#f8fafc", stroke=ORANGE, sw=1))
    el.append(f'<rect x="454" y="298" width="40" height="14" rx="3" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.5"/>')
    el.append(f'<circle cx="463" cy="317" r="5" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(f'<circle cx="485" cy="317" r="5" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>')
    el.append(f'<line x1="458" y1="291" x2="490" y2="291" stroke="{ORANGE}" stroke-width="2" marker-end="url(#arr-orange)"/>')
    el.append(txt(504, 266, "② 滑轮推车（Ekkyklema）", size=12, color=ORANGE, weight="700"))
    el.append(txt(504, 288, "• 舞台禁忌：几乎不当众演砍杀动作", size=11, color=BODY))
    el.append(txt(504, 309, "• 惨案在门后发生，先闻惨叫，再开", size=11, color=BODY))
    el.append(txt(504, 330, "  景屋大门推出木台亮出室内尸骸", size=11, color=BODY))
    el.append(txt(504, 351, "  （如《阿伽门农》浴缸弑王场面）", size=10.8, color=MUTED))

    # Tech 3: Mechane
    el.append(card(442, 388, 278, 128, rx=8, fill="#f8fafc", stroke=PURPLE, sw=1))
    el.append(f'<line x1="460" y1="494" x2="460" y2="424" stroke="{PURPLE}" stroke-width="2.2"/>')
    el.append(f'<line x1="460" y1="424" x2="490" y2="416" stroke="{PURPLE}" stroke-width="2.2"/>')
    el.append(f'<line x1="488" y1="417" x2="488" y2="446" stroke="{PURPLE}" stroke-width="1.3" stroke-dasharray="3 2"/>')
    el.append(f'<circle cx="488" cy="456" r="10" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.4"/>')
    el.append(txt(488, 460, "神", size=10, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(506, 410, "③ 起重吊车（Mechane）", size=12, color=PURPLE, weight="700"))
    el.append(txt(506, 432, "• 悬臂绳索把神明或英雄吊飞至景屋", size=11, color=BODY))
    el.append(txt(506, 453, "  半空（如美狄亚乘太阳龙车升空）", size=11, color=BODY))
    el.append(txt(506, 474, "• 拉丁成语 Deus ex machina：", size=11, color=PURPLE, weight="600"))
    el.append(txt(506, 494, "  “机械降神”强行收场即源于此机", size=10.8, color=MUTED))

    svg = figure(
        548,
        "古希腊露天剧场空间平面构造与三大舞台机关解剖图",
        "左侧按埃皮达鲁斯34加21排比例展示看台、乐池、侧道与景屋的声学空间关系；右侧解析亚麻面具、展示室内惨案的滑轮推车与衍生出机械降神一词的起重吊车。",
        el,
    )
    write_svg(SUBDIR, "greek-theater-architecture-and-stagecraft.svg", svg)


def _build_tragedians_and_survival_svg():
    el = []
    el.extend(
        header(
            "三大巨匠写下近三百部戏，为何今天只剩 33 部完整剧本？",
            "上：公元前 5 世纪三代悲剧家的精神接力；下：历经两千四百年传抄的“双通道”手稿幸存漏斗",
        )
    )

    masters = [
        {
            "name": "埃斯库罗斯 Aeschylus",
            "meta": "约前 525—前 456｜夺冠 13 次",
            "fg": BLUE,
            "bg": BLUE_SOFT,
            "role": "身份：马拉松与萨拉米斯海战老兵",
            "count": "传世：7 部 / 约 70–90 部",
            "craft": "革新：第 2 演员，宏大连贯三联剧",
            "soul1": "母题：神义宇宙秩序、家族血仇如何",
            "soul2": "走入公民法庭（《俄瑞斯忒亚》）",
        },
        {
            "name": "索福克勒斯 Sophocles",
            "meta": "约前 496—前 406｜夺冠约 24 次",
            "fg": GREEN,
            "bg": GREEN_SOFT,
            "role": "身份：雅典将军、司库（从未排第 3）",
            "count": "传世：7 部 / 约 123 部",
            "craft": "革新：第 3 演员与景画，单剧独立",
            "soul1": "母题：孤傲高贵的英雄直面认知盲区",
            "soul2": "与命运铁律（《俄狄浦斯王》）",
        },
        {
            "name": "欧里庇得斯 Euripides",
            "meta": "约前 485—前 406｜夺冠仅 5 次",
            "fg": ORANGE,
            "bg": ORANGE_SOFT,
            "role": "身份：质疑传统的哲人（死后最红）",
            "count": "传世：19 部 / 约 90 部（含 1 羊）",
            "craft": "革新：心理写实、平民口吻、论辩戏",
            "soul1": "母题：替女性与战俘发声，解剖极端",
            "soul2": "激情与非理性（《美狄亚》）",
        },
    ]

    mw, mgap = 228, 14
    for i, m in enumerate(masters):
        mx = 24 + i * (mw + mgap)
        el.append(card(mx, 66, mw, 232, stroke=m["fg"], sw=1.2))
        el.append(txt(mx + 14, 91, m["name"], size=13, color=m["fg"], weight="700"))
        el.append(pill(mx + 14, 102, m["meta"], fg=m["fg"], bg=m["bg"], w=mw - 28, h=22, size=10.8))
        el.append(txt(mx + 14, 145, m["role"], size=11.2, color=BODY))
        el.append(txt(mx + 14, 168, m["count"], size=11.5, color=INK, weight="700"))
        el.append(txt(mx + 14, 191, m["craft"], size=11.2, color=BODY))
        el.append(f'<line x1="{mx + 14}" y1="205" x2="{mx + mw - 14}" y2="205" stroke="{HAIRLINE}" stroke-width="1"/>')
        el.append(txt(mx + 14, 227, m["soul1"], size=11.2, color=BODY))
        el.append(txt(mx + 14, 249, m["soul2"], size=11.2, color=BODY))
        el.append(txt(mx + 14, 278, f"代表存世率：约 {round((7 if i < 2 else 19) / (80 if i == 0 else (123 if i == 1 else 90)) * 100)}%", size=10.8, color=MUTED))

    # Bottom survival funnel
    el.append(card(24, 312, 712, 232))
    el.append(txt(42, 338, "手稿幸存漏斗：为什么欧里庇得斯生前夺冠最少，传世剧本（19 部）反倒比前两位之和还多？", size=12.8, color=INK, weight="700"))

    # Stage 1
    el.append(card(40, 360, 138, 134, rx=8, fill=SLATE_SOFT, stroke=SLATE))
    el.append(txt(109, 383, "① 雅典首演总库", size=11.5, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(109, 416, "1,000+ 部", size=18, color=INK, anchor="middle", weight="700"))
    el.append(txt(109, 442, "三大师合写约 300 部", size=10.8, color=BODY, anchor="middle"))
    el.append(txt(109, 462, "多数剧本仅演一场", size=10.8, color=MUTED, anchor="middle"))
    el.append(txt(109, 480, "莎草纸极易霉烂散佚", size=10.8, color=MUTED, anchor="middle"))

    el.append(f'<line x1="178" y1="427" x2="198" y2="427" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')

    # Stage 2
    el.append(card(202, 360, 146, 134, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(275, 383, "② 国家官本与馆藏", size=11.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(275, 416, "约 220 卷", size=17, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(275, 442, "前 330 吕库古存官本", size=10.8, color=BODY, anchor="middle"))
    el.append(txt(275, 462, "防演员篡改台词，后归", size=10.8, color=BODY, anchor="middle"))
    el.append(txt(275, 480, "亚历山大图书馆整编", size=10.8, color=BODY, anchor="middle"))

    # Split arrows to 3A and 3B
    el.append(f'<path d="M348,412 L370,392" fill="none" stroke="{BLUE}" stroke-width="1.6" marker-end="url(#arr-blue)"/>')
    el.append(f'<path d="M348,442 L370,464" fill="none" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#arr-orange)"/>')

    # Stage 3A: Byzantine select plays
    el.append(card(374, 354, 192, 68, rx=8, fill="#f0f9ff", stroke=BLUE))
    el.append(txt(470, 375, "通道 A：拜占庭学校“精选教材本”", size=11.2, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(470, 395, "埃 7 ＋ 索 7 ＋ 欧 10 ＝ 24 部", size=11.5, color=INK, anchor="middle", weight="700"))
    el.append(txt(470, 413, "附教学评注，师生世代抄写得以保全", size=10.5, color=MUTED, anchor="middle"))

    # Stage 3B: Alphabetic plays
    el.append(card(374, 432, 192, 68, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    el.append(txt(470, 453, "通道 B：欧氏“字母顺序全集残卷”", size=11.2, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(470, 473, "奇迹幸存希腊字母 Ε–Κ 卷 ＝ 9 部", size=11.5, color=INK, anchor="middle", weight="700"))
    el.append(txt(470, 491, "含唯一完整萨堤尔剧《独目巨人》！", size=10.5, color=ORANGE, anchor="middle", weight="600"))

    # Merge arrows to Stage 4
    el.append(f'<path d="M566,392 L586,412" fill="none" stroke="{GREEN}" stroke-width="1.6" marker-end="url(#arr-green)"/>')
    el.append(f'<path d="M566,464 L586,442" fill="none" stroke="{GREEN}" stroke-width="1.6" marker-end="url(#arr-green)"/>')

    # Stage 4: Extant 33
    el.append(card(590, 360, 130, 134, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.4))
    el.append(txt(655, 383, "④ 今日传世全本", size=11.5, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(655, 418, "33 部", size=20, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(655, 444, "24 + 9 汇合", size=11, color=INK, anchor="middle", weight="700"))
    el.append(txt(655, 464, "32 悲剧 ＋ 1 羊人剧", size=10.6, color=BODY, anchor="middle"))
    el.append(txt(655, 482, "人类戏剧无价遗产", size=10.6, color=MUTED, anchor="middle"))

    el.append(
        txt(
            42,
            528,
            "学术限定：《被缚的普罗米修斯》（归埃氏）与《瑞索斯》（归欧氏）现代学界多推断为后人托名之作，但均计入这 33 部古希腊存世剧本。",
            size=10.8,
            color=MUTED,
        )
    )

    svg = figure(
        558,
        "古希腊三大悲剧家对比与33部传世剧本手稿幸存漏斗图",
        "上方对比埃斯库罗斯、索福克勒斯与欧里庇得斯的生平、夺冠次数、舞台革新与精神母题；下方展示从上千部首演剧目经国家定本到24部拜占庭精选本加9部欧里庇得斯字母残卷共33部存世剧本的流传过程。",
        el,
    )
    write_svg(SUBDIR, "three-tragedians-and-33-surviving-plays.svg", svg)


def _build_poetics_oedipus_svg():
    extra_css = """
  .arc-trace {
    stroke-dasharray: 760;
    stroke-dashoffset: 760;
    animation: drawArc 4.8s ease-in-out 0.25s 1 forwards;
  }
  .apex-ring {
    transform-box: fill-box;
    transform-origin: center;
    opacity: 0;
    animation: apexPulse 1.4s ease-out 3.2s 1 forwards;
  }
  @keyframes drawArc {
    to { stroke-dashoffset: 0; }
  }
  @keyframes apexPulse {
    0% { opacity: 0.9; transform: scale(0.7); }
    100% { opacity: 0.35; transform: scale(1.65); }
  }
  @media (prefers-reduced-motion: reduce) {
    .arc-trace {
      animation: none;
      stroke-dashoffset: 0;
    }
    .apex-ring {
      animation: none;
      opacity: 0.35;
    }
  }"""

    el = []
    el.extend(
        header(
            "为什么《俄狄浦斯王》被亚里士多德奉为满分模板？《诗学》悲剧动力学曲线",
            "顶级悲剧不写“恶人遭报应”，而写高贵者在认知盲区（Hamartia）中亲手推倒查清真相的多米诺骨牌",
        )
    )

    # Upper plot chart card
    el.append(card(24, 66, 712, 300))
    # Axes & horizontal guide lines
    x_left, x_right = 88, 708
    y_high, y_mid, y_low = 122, 210, 302
    for gy, glbl in [(y_high, "顺境／威望"), (y_mid, "追查临界"), (y_low, "崩塌／真相")]:
        el.append(f'<line x1="{x_left}" y1="{gy}" x2="{x_right}" y2="{gy}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="4 4"/>')
        el.append(txt(x_left - 8, gy + 4, glbl, size=10.8, color=MUTED, anchor="end"))

    # Quantitative structural bands along bottom of plot
    parts = [
        (96, 184, "开场白 Prologue"),
        (190, 278, "进场歌 Parodos"),
        (284, 464, "第 1–3 场与合唱歌"),
        (470, 588, "第 4 场：高潮奇点"),
        (594, 704, "退场歌 Exodos"),
    ]
    for px1, px2, plbl in parts:
        el.append(card(px1, 324, px2 - px1, 26, rx=5, fill=SLATE_SOFT, stroke=HAIRLINE))
        el.append(txt((px1 + px2) / 2, 341, plbl, size=10.5, color=SLATE, anchor="middle", weight="600"))

    # Plot curve: (124,152) -> (276,140) -> (446,128) -> sharp reversal plunge -> (536,268) -> (656,296)
    curve_d = "M 124 152 C 180 150, 224 143, 276 140 C 340 136, 404 120, 446 128 C 482 135, 502 226, 536 268 C 568 295, 612 296, 656 296"
    # Static base guide (ensures full static legibility before/without animation)
    el.append(f'<path d="{curve_d}" fill="none" stroke="{BLUE_LINE}" stroke-width="2.2" stroke-dasharray="5 4"/>')
    # Animated foreground trace
    el.append(f'<path d="{curve_d}" class="arc-trace" fill="none" stroke="{ORANGE}" stroke-width="3.4" stroke-linecap="round"/>')

    # Pulse ring at climax node (536, 268)
    el.append(f'<circle cx="536" cy="268" r="14" class="apex-ring" fill="none" stroke="{ORANGE}" stroke-width="2.2"/>')

    nodes = [
        (124, 152, "1", BLUE, BLUE_SOFT, 132, 184, "middle", "救城明君立誓追凶", "刚正果敢，浑然不知凶手是谁"),
        (276, 140, "2", BLUE, BLUE_SOFT, 282, 172, "middle", "悲剧性过失 Hamartia", "急躁多疑，怒斥先知与内兄"),
        (446, 128, "3", PURPLE, PURPLE_SOFT, 418, 86, "middle", "虚假安心（戏剧反讽顶点）", "闻科林斯养父病逝，以为神谕失效"),
        (536, 268, "4", ORANGE, ORANGE_SOFT, 526, 206, "middle", "突转＋发现同刻引爆！", "牧人对质：报喜瞬间翻转为弑父娶母真相"),
        (656, 296, "5", GREEN, GREEN_SOFT, 636, 250, "middle", "苦难 Pathos → 净化 Katharsis", "刺目流放，激起观众怜悯与恐惧"),
    ]
    for nx, ny, num, nfg, nbg, tx, ty, anc, t1, t2 in nodes:
        el.append(step_badge(nx, ny, num, fg=nfg, bg=nbg, r=10))
        el.append(txt(tx, ty, t1, size=11.3, color=nfg, anchor=anc, weight="700", halo=True))
        el.append(txt(tx, ty + 17, t2, size=10.5, color=BODY, anchor=anc, halo=True))

    # Bottom two cards: Hamartia vs Katharsis scholarly debate
    el.append(card(24, 380, 350, 130, stroke=BLUE))
    el.append(txt(40, 404, "《诗学》第 13 章：为什么主角不能是圣人或恶棍？", size=12.2, color=BLUE, weight="700"))
    el.append(txt(40, 427, "• 完人无辜遭殃 → 观众只觉残忍反感，毫无悲剧感；", size=11, color=BODY))
    el.append(txt(40, 449, "• 恶棍由盛转衰 → 虽大快人心，却无“怜悯与恐惧”；", size=11, color=BODY))
    el.append(txt(40, 471, "• 唯有声望崇高却带认知盲区／误判（Hamartia）者坠落，", size=11, color=BODY))
    el.append(txt(40, 493, "  才令人怜其本非邪恶、惧凡人皆难逃认知局限。", size=11, color=INK, weight="600"))

    el.append(card(388, 380, 348, 130, stroke=GREEN))
    el.append(txt(404, 404, "学界百年公案：“净化（Katharsis）”到底指什么？", size=12.2, color=GREEN, weight="700"))
    el.append(txt(404, 427, "亚里士多德全书未给定义，现代研究主要分三大流派：", size=10.8, color=MUTED))
    el.append(txt(404, 449, "① 医学排泄说（伯奈斯）：如泻药排毒般宣泄积压情绪；", size=11, color=BODY))
    el.append(txt(404, 471, "② 伦理陶冶说（莱辛／扬科）：把过度悲惧调校到适度；", size=11, color=BODY))
    el.append(txt(404, 493, "③ 认知澄明说（努斯鲍姆）：在安全距离看清人类命运处境。", size=11, color=BODY))

    svg = figure(
        524,
        "亚里士多德《诗学》悲剧动力学曲线与《俄狄浦斯王》结构解剖",
        "以索福克勒斯《俄狄浦斯王》为例，绘制开场白、进场歌、场与合唱歌、高潮突转与发现同刻引爆直至退场歌净化的戏剧张力曲线，并对比悲剧性过失与净化的三种现代学术解释。",
        el,
        extra_css=extra_css,
    )
    write_svg(SUBDIR, "aristotle-poetics-oedipus-arc.svg", svg)


def _build_legacy_svg():
    el = []
    el.extend(
        header(
            "雅典战败后悲剧“死”了吗？从城邦祭礼转型到两千四百年的四次重生",
            "前 404 年终结的是“古典原创黄金期”；悲剧随后化身经典重演、欧洲歌剧火种与现代心理学母题",
        )
    )

    # Top panel: 4th century BCE transition + Nietzsche vs Classics historiography
    el.append(card(24, 66, 712, 194))
    el.append(txt(42, 91, "一、公元前 4 世纪大转折：黄金时代为何谢幕？（历史制度变迁 vs 哲学美学假说）", size=13.2, color=INK, weight="700"))

    el.append(card(40, 104, 426, 142, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    el.append(txt(54, 126, "历史与剧场机制真相：不是突然消亡，而是转型“国际经典”", size=11.8, color=BLUE, weight="700"))
    el.append(txt(54, 148, "• 前 406 年欧、索二圣同年离世；前 404 年雅典在伯罗奔尼撒战争战败；", size=11, color=BODY))
    el.append(txt(54, 170, "• 前 386 年制度拐点：酒神节增设“旧剧重演”，新剧难敌死去大师经典；", size=11, color=BODY))
    el.append(txt(54, 192, "• 剧场从“城邦民主神学思辨”转向巡回明星演员炫技（欧氏成头号巨星）；", size=11, color=BODY))
    el.append(txt(54, 214, "• 公共政治退潮后，聚焦市民婚恋与家务的米南德“新喜剧”成为舞台主流。", size=11, color=BODY))
    el.append(txt(54, 234, "  （注：前 4 世纪阿伽通首创纯虚构剧情悲剧，但后世未入学校精选本而失传）", size=10.3, color=MUTED))

    el.append(card(480, 104, 240, 142, rx=8, fill=PURPLE_SOFT, stroke=PURPLE))
    el.append(txt(494, 126, "尼采 1872《悲剧的诞生》视角", size=11.8, color=PURPLE, weight="700"))
    el.append(txt(494, 149, "• 提炼“酒神精神（音乐狂醉）”与", size=11, color=BODY))
    el.append(txt(494, 170, "  “日神精神（梦境造型）”二元合力；", size=11, color=BODY))
    el.append(txt(494, 191, "• 认为“苏格拉底理性＋欧里庇得斯”", size=11, color=BODY))
    el.append(txt(494, 212, "  杀死悲剧——属深刻哲学洞见，但", size=11, color=BODY))
    el.append(txt(494, 233, "  现代古典学强调城邦转型才是主因。", size=10.6, color=PURPLE, weight="600"))

    # Bottom panel: 4 rebirth milestones
    el.append(card(24, 274, 712, 232))
    el.append(txt(42, 300, "二、跨越两千四百年的四次“借壳重生”时间轴", size=13.2, color=INK, weight="700"))

    # Horizontal timeline spine
    el.append(f'<line x1="88" y1="326" x2="672" y2="326" stroke="{BLUE}" stroke-width="2.2"/>')

    eras = [
        (
            "1",
            "古罗马与拜占庭传抄",
            "前 1 世纪—15 世纪",
            BLUE,
            BLUE_SOFT,
            [
                "罗马塞内卡改成室内",
                "诵读的血腥修辞悲剧；",
                "拜占庭学者守护希腊",
                "抄本西传文艺复兴欧洲",
            ],
        ),
        (
            "2",
            "美丽误会催生“歌剧”",
            "1590 年代·佛罗伦萨",
            ORANGE,
            ORANGE_SOFT,
            [
                "卡梅拉塔文人社试图",
                "复原古希腊“全剧配乐",
                "吟唱”，意外发明现代",
                "歌剧《达芙妮》等名作",
            ],
        ),
        (
            "3",
            "近代欧洲悲剧双峰",
            "17 世纪·英法舞台",
            GREEN,
            GREEN_SOFT,
            [
                "莎士比亚借塞内卡传统",
                "写就四大悲剧；法国拉",
                "辛直承欧里庇得斯写出",
                "古典主义巅峰《费德尔》",
            ],
        ),
        (
            "4",
            "现代心理与全球剧场",
            "20 世纪至今",
            PURPLE,
            PURPLE_SOFT,
            [
                "弗洛伊德借索氏剧命名",
                "“俄狄浦斯情结”；阿努",
                "伊二战改编《安提戈涅》",
                "反抗强权，全球常演不衰",
            ],
        ),
    ]

    ew, egap = 162, 14
    for i, (num, etitle, edate, efg, ebg, elines) in enumerate(eras):
        ex = 36 + i * (ew + egap)
        ecx = ex + ew / 2
        el.append(step_badge(ecx, 326, num, fg=efg, bg=ebg, r=10.5))
        el.append(card(ex, 344, ew, 146, rx=8, fill="#f8fafc", stroke=efg, sw=1.1))
        el.append(txt(ecx, 366, etitle, size=11.6, color=efg, anchor="middle", weight="700"))
        el.append(txt(ecx, 384, edate, size=10.4, color=MUTED, anchor="middle"))
        for li, ln in enumerate(elines):
            el.append(txt(ecx, 408 + li * 20, ln, size=10.8, color=BODY, anchor="middle"))

    svg = figure(
        520,
        "古希腊悲剧在公元前4世纪的制度转型与两千四百年文化传承时间轴",
        "上方对比公元前404年雅典战败及前386年旧剧重演制度带来的历史转型与尼采《悲剧的诞生》日神酒神哲学视角；下方展示古罗马拜占庭传抄、1590年代佛罗伦萨复原古剧意外发明歌剧、莎士比亚与拉辛近代双峰、以及现代心理学与全球重演四次重生。",
        el,
    )
    write_svg(SUBDIR, "decline-transformation-and-legacy.svg", svg)


@register("greek-tragedy", "Origin, civic mechanics, stagecraft, 33 manuscripts, Poetics, and legacy of Greek tragedy", "humanities")
def build_greek_tragedy():
    _verify_greek_tragedy_math()
    _build_evolution_svg()
    _build_city_dionysia_svg()
    _build_theater_architecture_svg()
    _build_tragedians_and_survival_svg()
    _build_poetics_oedipus_svg()
    _build_legacy_svg()
