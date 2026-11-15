"""Original paleographic SVG diagrams for '公' and '私' and extended Chinese characters."""

from . import core
from .core import (
    BG,
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

SUBDIR = "gong-si-characters"

# Warm paleographic accents
BONE_BG = "#fdf8ee"
BONE_BORDER = "#dfc7a7"
BONE_INK = "#853212"

BRONZE_BG = "#edf7f4"
BRONZE_BORDER = "#9bc9be"
BRONZE_INK = "#0f5246"

SEAL_BG = "#fef2f2"
SEAL_BORDER = "#f2b6b6"
SEAL_INK = "#991b1b"

GOLD = "#b45309"
GOLD_SOFT = "#fef3c7"


def _glyph_plate(x, y, w, h, bg=BONE_BG, border=BONE_BORDER):
    """Render an archaeological rubbing / seal plate with subtle corner ticks."""
    cx = x + w / 2
    cy = y + h / 2
    return "\n".join(
        [
            card(x, y, w, h, rx=10, fill=bg, stroke=border, sw=1.3),
            f'<line x1="{cx:.1f}" y1="{y + 6}" x2="{cx:.1f}" y2="{y + h - 6}" '
            f'stroke="{border}" stroke-width="0.8" stroke-dasharray="3 3" opacity="0.55"/>',
            f'<line x1="{x + 6}" y1="{cy:.1f}" x2="{x + w - 6}" y2="{cy:.1f}" '
            f'stroke="{border}" stroke-width="0.8" stroke-dasharray="3 3" opacity="0.55"/>',
        ]
    )


def build_gong_evolution_anim() -> str:
    """1-shot animated timeline of 公 from Shang oracle bone to modern script + two-layer reading."""
    extra_css = """
  @keyframes stageReveal {
    0% { opacity: 0.18; transform: translateY(5px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  @keyframes ringHighlight {
    0%, 35% { stroke-opacity: 0; }
    55% { stroke-opacity: 0.95; }
    100% { stroke-opacity: 0.85; }
  }
  .g-st1 { opacity: 0.18; animation: stageReveal 0.85s ease-out 0.15s forwards; }
  .g-st2 { opacity: 0.18; animation: stageReveal 0.85s ease-out 1.45s forwards; }
  .g-st3 { opacity: 0.18; animation: stageReveal 0.85s ease-out 2.85s forwards; }
  .g-st4 { opacity: 0.18; animation: stageReveal 0.85s ease-out 4.25s forwards; }
  .g-st5 { opacity: 0.18; animation: stageReveal 0.95s ease-out 5.55s forwards; }
  .morph-ring { stroke-opacity: 0; animation: ringHighlight 6.4s ease-out 0s forwards; }
  @media (prefers-reduced-motion: reduce) {
    .g-st1, .g-st2, .g-st3, .g-st4, .g-st5 {
      animation: none !important;
      opacity: 1 !important;
      transform: none !important;
    }
    .morph-ring {
      animation: none !important;
      stroke-opacity: 0.85 !important;
    }
  }"""

    el = []
    el.extend(
        header(
            "“公”字三千年变形记：从当众平分器物，到“背私为公”的哲理反转",
            "先看商周下方闭合的“口/瓮” → 再看战国秦篆开口讹变成“厶” → 分清考古初形与诸子哲理重解",
        )
    )

    # Four timeline cards: x=24, 206, 388, 570 (w=162, gap=20)
    stages = [
        (24, "g-st1", "1", "商代甲骨文", "约前13—前11世纪", BONE_BG, BONE_BORDER, BONE_INK),
        (206, "g-st2", "2", "西周金文", "毛公鼎·约前9世纪", BRONZE_BG, BRONZE_BORDER, BRONZE_INK),
        (388, "g-st3", "3", "战国简·秦小篆", "约前4—前3世纪", SEAL_BG, SEAL_BORDER, SEAL_INK),
        (570, "g-st4", "4", "汉隶至现代楷书", "汉代定型沿用至今", SLATE_SOFT, BORDER, INK),
    ]

    for x, cls, num, title_s, era_s, p_bg, p_bd, p_ink in stages:
        grp = [f'<g class="{cls}">']
        grp.append(card(x, 66, 162, 228, rx=10, fill=CARD_BG, stroke=BORDER, sw=1.1))
        grp.append(step_badge(x + 20, 86, num, fg=p_ink, bg=p_bg, r=10))
        grp.append(txt(x + 36, 90, title_s, size=13, color=INK, weight="700"))
        grp.append(txt(x + 16, 110, era_s, size=11, color=MUTED))
        grp.append(_glyph_plate(x + 25, 120, 112, 98, bg=p_bg, border=p_bd))
        grp.append("</g>")
        el.append("\n".join(grp))

    # Stage 1 Oracle Bone glyph (center x=105, y=169): 八 parting + square-round 口/凵 pot mouth
    el.append(
        f"""<g class="g-st1">
  <path d="M 94,134 Q 84,151 67,163 M 116,134 Q 126,151 143,163"
        fill="none" stroke="{BONE_INK}" stroke-width="3.8" stroke-linecap="round"/>
  <path d="M 83,172 L 127,172 L 124,203 L 86,203 Z"
        fill="none" stroke="{BLUE}" stroke-width="3.6" stroke-linejoin="round"/>
  {txt(105, 237, "上“八”：向两侧分开", size=11.5, color=BODY, anchor="middle", weight="600")}
  {txt(105, 256, "下“口/瓮”：宗邑或圆器", size=11.5, color=BLUE, anchor="middle", weight="600")}
  {txt(105, 276, "初义：当众平分共有物", size=11, color=MUTED, anchor="middle")}
</g>"""
    )

    # Stage 2 Western Zhou Bronze glyph (center x=287, y=169): thick cast 八 + round-belly 口 cauldron
    el.append(
        f"""<g class="g-st2">
  <path d="M 275,133 C 268,149 257,160 245,166 M 299,133 C 306,149 317,160 329,166"
        fill="none" stroke="{BRONZE_INK}" stroke-width="5.6" stroke-linecap="round"/>
  <path d="M 266,173 L 308,173 L 306,193 C 305,204 297,207 287,207 C 277,207 269,204 268,193 Z"
        fill="none" stroke="{BRONZE_INK}" stroke-width="5.0" stroke-linejoin="round"/>
  {txt(287, 237, "厚重青铜铭文铸造", size=11.5, color=BODY, anchor="middle", weight="600")}
  {txt(287, 256, "下方依然是闭合圆口", size=11.5, color=GREEN, anchor="middle", weight="600")}
  {txt(287, 276, "引申：公室·王公尊称", size=11, color=MUTED, anchor="middle")}
</g>"""
    )

    # Stage 3 Qin Small Seal glyph (center x=469, y=169): 八 + coiled 厶 (broken open from 口!)
    el.append(
        f"""<g class="g-st3">
  <path d="M 456,132 C 452,150 442,162 428,168 M 482,132 C 486,150 496,162 510,168"
        fill="none" stroke="{SEAL_INK}" stroke-width="3.8" stroke-linecap="round"/>
  <path d="M 468,171 C 446,175 444,203 468,205 C 488,206 495,192 483,181"
        fill="none" stroke="{ORANGE}" stroke-width="4.0" stroke-linecap="round"/>
  <circle class="morph-ring" cx="469" cy="189" r="24" fill="none"
          stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="4 3"/>
  {txt(469, 237, "圆口快写开口盘曲", size=11.5, color=BODY, anchor="middle", weight="600")}
  {txt(469, 256, "与“厶（私）”撞脸！", size=11.5, color=ORANGE, anchor="middle", weight="700")}
  {txt(469, 276, "触发韩非子哲理新解", size=11, color=MUTED, anchor="middle")}
</g>"""
    )

    # Stage 4 Regular Script glyph (center x=651, y=169): crisp vector strokes of modern 公
    el.append(
        f"""<g class="g-st4">
  <path d="M 639,136 C 632,151 621,163 609,171 M 661,134 C 670,150 681,162 694,170"
        fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>
  <path d="M 649,167 L 630,198 L 668,195"
        fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 661,184 L 675,204"
        fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>
  {txt(651, 237, "隶变拉直为撇折加点", size=11.5, color=BODY, anchor="middle", weight="600")}
  {txt(651, 256, "“八 + 厶”字形定格", size=11.5, color=INK, anchor="middle", weight="600")}
  {txt(651, 276, "公平·公共·天下为公", size=11, color=MUTED, anchor="middle")}
</g>"""
    )

    # Connecting arrows between timeline cards
    for ax in (188, 370, 552):
        el.append(
            f'<line x1="{ax}" y1="169" x2="{ax + 16}" y2="169" '
            f'stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>'
        )

    # Bottom dual comparison panels (y=310..508)
    el.append(
        f"""<g class="g-st5">
  {card(24, 310, 356, 196, rx=10, fill=BLUE_SOFT, stroke=BLUE, sw=1.2)}
  {pill(38, 322, "第一层：商周甲骨金文考古实证", fg=BLUE, bg=CARD_BG, w=214, h=22, size=11.5)}
  {txt(38, 364, "“八”是分开的象形（加刀是“分”，分牛是“半”）：", size=11.8, color=INK, weight="600")}
  {txt(38, 388, "• 高鸿缙“平分说”：上“八（分）”+ 下“口（器物）”，", size=11.5, color=BODY)}
  {txt(50, 408, "画的是氏族成员把猎物或粮食当众平均分配。", size=11.5, color=BODY)}
  {txt(38, 432, "• 朱芳圃“大口瓮说”：象宽口圆腹陶瓮（瓮的初文），", size=11.5, color=BODY)}
  {txt(50, 452, "因聚落共饮共食假借为公共、公平与宗族长老。", size=11.5, color=BODY)}
  {txt(38, 480, "结论：造字之初，下面那个圈真不是“自私”的私！", size=11.5, color=BLUE, weight="700")}

  {card(396, 310, 340, 196, rx=10, fill=ORANGE_SOFT, stroke=ORANGE, sw=1.2)}
  {pill(410, 322, "第二层：战国秦汉思想家哲理重解", fg=ORANGE, bg=CARD_BG, w=224, h=22, size=11.5)}
  {txt(410, 364, "战国时下方圆口演变成“厶”，恰被哲人借题发挥：", size=11.8, color=INK, weight="600")}
  {txt(410, 388, "• 《韩非子·五蠹》：“自环者谓之私，背私谓之公。”", size=11.5, color=BODY)}
  {txt(410, 412, "• 东汉许慎《说文》：“公，平分也。从八从厶，", size=11.5, color=BODY)}
  {txt(422, 432, "八犹背也。”（用小篆字形将两说巧妙缝合）", size=11.5, color=BODY)}
  {txt(410, 458, "价值：虽非甲骨初义，却成就了汉字史上最精彩", size=11.5, color=BODY)}
  {txt(410, 480, "的一次“美丽误会”，让公私对立深入文化血脉。", size=11.5, color=ORANGE, weight="700")}
</g>"""
    )

    return figure(
        522,
        "“公”字三千年字形演变与双层释读图解",
        "展示商代甲骨文、西周金文、战国秦篆到现代楷书中“公”字的演变，对比甲骨金文平分器物本义与韩非子“背私为公”哲理重解。",
        el,
        extra_css=extra_css,
    )


def build_si_grain_and_field() -> str:
    """Step-by-step anatomy of 厶 + 禾 = 私 and the Western Zhou 공田/私田 context."""
    el = []
    el.extend(
        header(
            "“私”字拆解：为什么在画圈自守的“厶”旁，偏偏要加一株谷穗“禾”？",
            "先认左栏“厶”的画圈指事 → 再看中栏“禾”的垂穗象形 → 右栏回到《诗经》公田与私田现场",
        )
    )

    # Left card: 厶 (x=24..242, w=218)
    el.append(card(24, 68, 218, 304, rx=10))
    el.append(step_badge(44, 88, "1", fg=ORANGE, bg=ORANGE_SOFT, r=10))
    el.append(txt(60, 92, "初文“厶”（上古音 *sil）", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(53, 106, 160, 108, bg=SEAL_BG, border=SEAL_BORDER))
    # Coiled self-loop 厶 vector drawing
    el.append(
        f"""<path d="M 136,125 C 102,128 96,178 130,188 C 160,196 172,168 150,151"
      fill="none" stroke="{SEAL_INK}" stroke-width="4.5" stroke-linecap="round"/>
<circle cx="133" cy="160" r="3.5" fill="{ORANGE}"/>
<path d="M 157,145 L 148,150 L 154,158" fill="none" stroke="{SEAL_INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>"""
    )
    el.append(txt(40, 234, "• 楚简小篆像一笔回环自绕", size=11.5, color=BODY, weight="600"))
    el.append(txt(40, 256, "• 韩非：“自环者谓之私”", size=11.5, color=BODY))
    el.append(txt(40, 278, "• 它就是“私”最早的本字", size=11.5, color=ORANGE, weight="600"))
    el.append(txt(40, 304, "• 现代活化石：注音符号 ㄙ", size=11.5, color=BLUE, weight="600"))
    el.append(txt(50, 324, "与日语片假名 ム 皆源于此", size=11.2, color=MUTED))
    el.append(txt(40, 350, "• 另有一说象农具“耜”端头", size=11, color=MUTED))

    # Plus sign between card 1 and card 2 (x=255)
    el.append(
        f'<circle cx="255" cy="160" r="11" fill="{SLATE_SOFT}" stroke="{BORDER}"/>\n'
        + txt(255, 165, "+", size=15, color=SLATE, anchor="middle", weight="700")
    )

    # Middle card: 禾 (x=268..486, w=218)
    el.append(card(268, 68, 218, 304, rx=10))
    el.append(step_badge(288, 88, "2", fg=GOLD, bg=GOLD_SOFT, r=10))
    el.append(txt(304, 92, "意符“禾”（沉甸甸谷穗）", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(297, 106, 160, 108, bg=BONE_BG, border=BONE_BORDER))
    # Oracle-bone / Bronze 禾 vector drawing (drooping ear + stem + leaves + roots)
    el.append(
        f"""<path d="M 380,200 L 380,136 C 380,124 366,120 348,131"
      fill="none" stroke="{BONE_INK}" stroke-width="3.8" stroke-linecap="round"/>
<path d="M 353,124 L 344,132 L 356,136" fill="none" stroke="{GOLD}" stroke-width="3.0" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="358" cy="123" r="2.6" fill="{GOLD}"/>
<circle cx="366" cy="121" r="2.6" fill="{GOLD}"/>
<path d="M 356,156 Q 380,148 404,156" fill="none" stroke="{BONE_INK}" stroke-width="3.4" stroke-linecap="round"/>
<path d="M 380,176 L 360,198 M 380,176 L 400,198" fill="none" stroke="{BONE_INK}" stroke-width="3.2" stroke-linecap="round"/>"""
    )
    el.append(txt(284, 234, "• 顶部弯垂：熟透的粟（小米）穗", size=11.5, color=BODY, weight="600"))
    el.append(txt(284, 256, "• 中部舒展：禾叶与挺立禾秆", size=11.5, color=BODY))
    el.append(txt(284, 278, "• 底部散开：扎入黄土的根须", size=11.5, color=BODY))
    el.append(txt(284, 304, "• 北方旱作农业最核心的口粮", size=11.5, color=GOLD, weight="600"))
    el.append(txt(284, 326, "• 谷熟一岁：人背禾就是“年”", size=11.2, color=MUTED))
    el.append(txt(284, 350, "• 交纳余粮：禾加兑就是“税”", size=11.2, color=MUTED))

    # Arrow sign between card 2 and card 3 (x=499)
    el.append(
        f'<circle cx="499" cy="160" r="11" fill="{BLUE_SOFT}" stroke="{BLUE}"/>\n'
        + txt(499, 164, "→", size=13, color=BLUE, anchor="middle", weight="700")
    )

    # Right card: 私 & 井田 (x=512..736, w=224)
    el.append(card(512, 68, 224, 304, rx=10))
    el.append(step_badge(532, 88, "3", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(548, 92, "合体“私”（自家田里的禾）", size=13, color=INK, weight="700"))
    # Mini 3x3 Jingtian (井田) diagram inside x=540..708, y=106..214
    el.append(card(540, 106, 168, 108, rx=8, fill=GREEN_SOFT, stroke=GREEN, sw=1.1))
    # 3x3 cells: x=548, 598, 648 (w=48 each), y=112, 144, 176 (h=30 each)
    for r_idx in range(3):
        for c_idx in range(3):
            cx_cell = 548 + c_idx * 50
            cy_cell = 112 + r_idx * 32
            if r_idx == 1 and c_idx == 1:
                el.append(card(cx_cell, cy_cell, 48, 30, rx=4, fill=BLUE_SOFT, stroke=BLUE, sw=1.4))
                el.append(txt(cx_cell + 24, cy_cell + 19, "公田", size=11, color=BLUE, anchor="middle", weight="700"))
            else:
                el.append(card(cx_cell, cy_cell, 48, 30, rx=4, fill=CARD_BG, stroke=BRONZE_BORDER, sw=1))
                el.append(txt(cx_cell + 24, cy_cell + 19, "私", size=10.5, color=GREEN, anchor="middle", weight="600"))

    el.append(txt(526, 234, "• 《诗经·小雅·大田》名句：", size=11.5, color=BODY, weight="600"))
    el.append(txt(534, 255, "“雨我公田，遂及我私”", size=11.8, color=GREEN, weight="700"))
    el.append(txt(526, 278, "• 《说文》：“私，禾也。从禾", size=11.5, color=BODY))
    el.append(txt(536, 298, "厶声，北道名禾主人曰私主人”", size=11.2, color=BODY))
    el.append(txt(526, 324, "• 归自家的庄稼→个人、私密", size=11.5, color=INK, weight="600"))
    el.append(txt(526, 350, "• 久借不还，“厶”退居成偏旁", size=11.2, color=MUTED))

    # Bottom takeaway strip (y=388..498)
    el.append(card(24, 388, 712, 112, rx=10, fill=SLATE_SOFT, stroke=BORDER, sw=1.1))
    el.append(txt(40, 412, "顺着一株“禾”长出的中国农耕词汇树（抽象概念都扎根在泥土与谷穗里）：", size=12.5, color=INK, weight="700"))

    chips = [
        (40, "私 = 禾 + 厶", "自家粮仓的庄稼", ORANGE, ORANGE_SOFT),
        (214, "年 = 禾 + 人", "人背熟禾，谷熟一岁", GOLD, GOLD_SOFT),
        (388, "和 = 禾 + 口", "仓廪有粮，言谈调顺", GREEN, GREEN_SOFT),
        (562, "利 = 禾 + 刀", "挥镰割禾，锋快有收", BLUE, BLUE_SOFT),
    ]
    for cx_chip, head_s, sub_s, fg_c, bg_c in chips:
        el.append(card(cx_chip, 426, 160, 60, rx=8, fill=CARD_BG, stroke=fg_c, sw=1))
        el.append(pill(cx_chip + 10, 434, head_s, fg=fg_c, bg=bg_c, w=140, h=20, size=11.2))
        el.append(txt(cx_chip + 80, 474, sub_s, size=11, color=BODY, anchor="middle"))

    return figure(
        516,
        "“厶”与“禾”合体为“私”及农耕字族图解",
        "拆解初文厶、象形字禾与合体字私的造字逻辑，结合西周公田与私田制度及禾部关联字年、和、利说明汉字从农耕经验生发抽象概念的过程。",
        el,
    )


def build_harvest_hands_grid() -> str:
    """2x2 paleographic action cinema: 秉, 兼, 力, 男."""
    el = []
    el.extend(
        header(
            "田间手脚连环画：抓一棵禾是“秉”，抓两棵是“兼”，扶耒翻田就是“男”",
            "看清古文字里的“右手（又）”抓了几株庄稼、“农田（田）”旁立着什么农具，四个常用字秒懂",
        )
    )

    # Card 1: 秉 (x=24..370, y=68..276)
    el.append(card(24, 68, 346, 208, rx=10))
    el.append(step_badge(42, 88, "1", fg=GOLD, bg=GOLD_SOFT, r=10))
    el.append(txt(58, 92, "秉（bǐng）：一只手握住一株禾", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(40, 106, 114, 152, bg=BONE_BG, border=BONE_BORDER))
    # Glyph 秉: single 禾 + hand 又 gripping middle
    el.append(
        f"""<path d="M 97,240 L 97,132 C 97,120 84,116 68,127"
      fill="none" stroke="{BONE_INK}" stroke-width="3.8" stroke-linecap="round"/>
<path d="M 73,148 Q 97,140 121,148" fill="none" stroke="{BONE_INK}" stroke-width="3.3" stroke-linecap="round"/>
<path d="M 97,212 L 79,236 M 97,212 L 115,236" fill="none" stroke="{BONE_INK}" stroke-width="3.1" stroke-linecap="round"/>
<path d="M 134,196 L 112,182 L 88,182 M 112,182 L 90,171 M 112,182 L 91,193"
      fill="none" stroke="{ORANGE}" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/>"""
    )
    el.append(txt(168, 124, "构件：禾（一株谷）+ 又（右手）", size=11.8, color=GOLD, weight="700"))
    el.append(txt(168, 149, "• 《诗经》：“彼有遗秉”", size=11.5, color=BODY))
    el.append(txt(168, 173, "• 本义：手攥一把禾（古量词）", size=11.5, color=BODY))
    el.append(txt(168, 197, "• 引申：秉持 · 秉公 · 秉烛夜游", size=11.5, color=INK, weight="600"))
    el.append(txt(168, 223, "• 把原则像谷穗一样攥紧在手心，", size=11.2, color=MUTED))
    el.append(txt(178, 243, "就是“秉公办理”最生动的画面！", size=11.2, color=MUTED))

    # Card 2: 兼 (x=390..736, y=68..276)
    el.append(card(390, 68, 346, 208, rx=10))
    el.append(step_badge(408, 88, "2", fg=ORANGE, bg=ORANGE_SOFT, r=10))
    el.append(txt(424, 92, "兼（jiān）：一只手同时抓两株禾！", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(406, 106, 114, 152, bg=BONE_BG, border=BONE_BORDER))
    # Glyph 兼: two parallel 禾 stalks + one hand 又 spanning across both!
    el.append(
        f"""<path d="M 446,240 L 446,134 C 446,123 436,119 423,128"
      fill="none" stroke="{BONE_INK}" stroke-width="3.5" stroke-linecap="round"/>
<path d="M 430,148 Q 446,142 460,148" fill="none" stroke="{BONE_INK}" stroke-width="3.0" stroke-linecap="round"/>
<path d="M 446,214 L 434,236 M 446,214 L 456,236" fill="none" stroke="{BONE_INK}" stroke-width="2.8" stroke-linecap="round"/>
<path d="M 480,240 L 480,134 C 480,123 470,119 458,128"
      fill="none" stroke="{BONE_INK}" stroke-width="3.5" stroke-linecap="round"/>
<path d="M 465,148 Q 480,142 496,148" fill="none" stroke="{BONE_INK}" stroke-width="3.0" stroke-linecap="round"/>
<path d="M 480,214 L 469,236 M 480,214 L 492,236" fill="none" stroke="{BONE_INK}" stroke-width="2.8" stroke-linecap="round"/>
<path d="M 508,198 L 488,182 L 438,182 M 488,182 L 440,171 M 488,182 L 440,193"
      fill="none" stroke="{ORANGE}" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/>"""
    )
    el.append(txt(534, 124, "构件：秝（二禾并列）+ 又（手）", size=11.8, color=ORANGE, weight="700"))
    el.append(txt(534, 149, "• 《说文》：“兼，并也。持二禾”", size=11.5, color=BODY))
    el.append(txt(534, 173, "• 对比：“秉持一禾，兼持二禾”", size=11.5, color=BODY, weight="600"))
    el.append(txt(534, 197, "• 引申：兼顾 · 兼职 · 兼听则明", size=11.5, color=INK, weight="600"))
    el.append(txt(534, 223, "• 今天“兼”字头顶两点和中间两竖，", size=11.2, color=MUTED))
    el.append(txt(544, 243, "正是当年并排立着的两棵庄稼！", size=11.2, color=MUTED))

    # Card 3: 力 (x=24..370, y=292..500)
    el.append(card(24, 292, 346, 208, rx=10))
    el.append(step_badge(42, 312, "3", fg=BLUE, bg=BLUE_SOFT, r=10))
    el.append(txt(58, 316, "力（lì）：破土翻地的尖头木农具", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(40, 330, 114, 152, bg=BRONZE_BG, border=BRONZE_BORDER))
    # Glyph 力: ancient wooden plow 耒 with foot crossbar and curved digging tine
    el.append(
        f"""<path d="M 105,346 L 88,458" fill="none" stroke="{BRONZE_INK}" stroke-width="4.4" stroke-linecap="round"/>
<path d="M 72,388 L 122,388 L 116,442 C 114,454 106,458 98,452"
      fill="none" stroke="{BLUE}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>"""
    )
    el.append(txt(168, 348, "考古释读：带踏横的翻土木耒", size=11.8, color=BLUE, weight="700"))
    el.append(txt(168, 373, "• 徐中舒考证甲骨“力”象耒耜形", size=11.5, color=BODY))
    el.append(txt(168, 396, "• （《说文》旧说象人筋脉之形）", size=11.2, color=MUTED))
    el.append(txt(168, 420, "• 脚踩横木刺破板结土最耗体力", size=11.5, color=BODY))
    el.append(txt(168, 444, "• 引申：力气 · 戮力 · 量力而行", size=11.5, color=INK, weight="600"))
    el.append(txt(168, 468, "• 加口吆喝助威，就是“加”字！", size=11.2, color=BLUE, weight="600"))

    # Card 4: 男 (x=390..736, y=292..500)
    el.append(card(390, 292, 346, 208, rx=10))
    el.append(step_badge(408, 312, "4", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(424, 316, "男（nán）：把“力”插进阡陌“田”畴", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(406, 330, 114, 152, bg=BRONZE_BG, border=BRONZE_BORDER))
    # Glyph 男: Oracle/Bronze 田 beside 力
    el.append(
        f"""<rect x="418" y="362" width="44" height="54" rx="4" fill="none" stroke="{GREEN}" stroke-width="3.6"/>
<line x1="440" y1="362" x2="440" y2="416" stroke="{GREEN}" stroke-width="3.2"/>
<line x1="418" y1="389" x2="462" y2="389" stroke="{GREEN}" stroke-width="3.2"/>
<path d="M 490,352 L 477,454" fill="none" stroke="{BRONZE_INK}" stroke-width="3.8" stroke-linecap="round"/>
<path d="M 469,388 L 506,388 L 501,440 C 499,450 492,453 486,447"
      fill="none" stroke="{BLUE}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>"""
    )
    el.append(txt(534, 348, "构件：田（农田）+ 力（耒耕）", size=11.8, color=GREEN, weight="700"))
    el.append(txt(534, 373, "• 《说文》：“言男用力於田也”", size=11.5, color=BODY))
    el.append(txt(534, 397, "• 甲骨金文多作左右并排（田+力）", size=11.5, color=BODY))
    el.append(txt(534, 421, "• 如实记录早期农耕重体力分工", size=11.5, color=BODY))
    el.append(txt(534, 445, "• 西周亦用作五等爵“公侯伯子男”", size=11.5, color=INK, weight="600"))
    el.append(txt(534, 468, "• 守土治田之职，与农事一脉相承", size=11.2, color=MUTED))

    return figure(
        516,
        "秉、兼、力、男四字古文字动作拆解图",
        "通过甲骨金文构件对比展示一只手握一禾为秉、握二禾为兼，翻土木耒为力，扶耒耕田为男的造字画面。",
        el,
    )


def build_dinner_table_cinema() -> str:
    """Three snapshots around one steaming grain vessel 皀: 即, 既, 飨/卿."""
    el = []
    el.extend(
        header(
            "饭桌上的时间微电影：围着同一碗香米饭（皀），古人拍下了三张快照",
            "先认清正中盛满熟饭的高足食簋“皀” → 再看碗边跪坐的人朝哪边转头，秒懂将来、完成与共餐礼仪",
        )
    )

    # Top legend bar explaining 皀 (x=90..670, y=64..104)
    el.append(card(70, 64, 620, 40, rx=20, fill=GOLD_SOFT, stroke=GOLD, sw=1.1))
    el.append(
        txt(
            380,
            89,
            "核心道具“皀（bī / xiāng）”：甲骨金文像高足食簋里堆尖的热米饭（白米飘香，正是“香”字源头）",
            size=11.8,
            color=INK,
            anchor="middle",
            weight="600",
        )
    )

    def _food_vessel(cx, cy):
        """Draw steaming round food vessel 皀 centered at (cx, cy)."""
        return f"""<path d="M {cx - 20},{cy - 6} Q {cx},{cy - 28} {cx + 20},{cy - 6} Z" fill="{GOLD_SOFT}" stroke="{GOLD}" stroke-width="2.8" stroke-linejoin="round"/>
<path d="M {cx - 22},{cy - 6} L {cx + 22},{cy - 6} L {cx + 17},{cy + 16} Q {cx},{cy + 24} {cx - 17},{cy + 16} Z" fill="none" stroke="{BONE_INK}" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M {cx},{cy + 20} L {cx},{cy + 36} M {cx - 16},{cy + 36} L {cx + 16},{cy + 36}" fill="none" stroke="{BONE_INK}" stroke-width="3.4" stroke-linecap="round"/>
<path d="M {cx - 7},{cy - 30} Q {cx - 11},{cy - 38} {cx - 5},{cy - 44} M {cx + 7},{cy - 30} Q {cx + 3},{cy - 38} {cx + 9},{cy - 44}" fill="none" stroke="{ORANGE}" stroke-width="2.0" stroke-linecap="round"/>"""

    # Card 1: 即 (x=24..248, y=118..496)
    el.append(card(24, 118, 224, 378, rx=10))
    el.append(step_badge(44, 138, "1", fg=BLUE, bg=BLUE_SOFT, r=10))
    el.append(txt(60, 142, "第一幕：即（凑近开吃）", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(42, 156, 188, 138, bg=BONE_BG, border=BONE_BORDER))
    el.append(_food_vessel(96, 232))
    # Kneeling person facing LEFT (toward bowl at x=96)
    el.append(
        f"""<circle cx="164" cy="188" r="10" fill="none" stroke="{BLUE}" stroke-width="3.4"/>
<path d="M 154,188 L 146,188" stroke="{BLUE}" stroke-width="3.0" stroke-linecap="round"/>
<path d="M 166,198 C 166,222 162,240 150,252 L 178,258" fill="none" stroke="{BLUE}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 162,212 L 136,218" fill="none" stroke="{BLUE}" stroke-width="3.4" stroke-linecap="round"/>
<path d="M 142,174 L 122,174" fill="none" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-orange)"/>"""
    )
    el.append(txt(40, 318, "• 镜头：人跪坐在食簋旁，面朝", size=11.5, color=BODY, weight="600"))
    el.append(txt(50, 338, "热气腾腾的米饭俯身伸手就食", size=11.5, color=BODY))
    el.append(txt(40, 364, "• 空间→时间：靠近饭碗，马上", size=11.5, color=BLUE, weight="600"))
    el.append(txt(50, 384, "要开动 → 即将 · 立即 · 即刻", size=11.5, color=BLUE, weight="600"))
    el.append(txt(40, 412, "• 若即若离：好像凑近又像走开", size=11.2, color=BODY))
    el.append(txt(40, 436, "• 即位：走近尊位坐下主持大礼", size=11.2, color=BODY))
    el.append(txt(40, 464, "• 楷书左旁不是“艮”，正是饭碗！", size=11, color=MUTED))

    # Card 2: 既 (x=268..492, y=118..496)
    el.append(card(268, 118, 224, 378, rx=10))
    el.append(step_badge(288, 138, "2", fg=ORANGE, bg=ORANGE_SOFT, r=10))
    el.append(txt(304, 142, "第二幕：既（吃饱扭头）", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(286, 156, 188, 138, bg=BONE_BG, border=BONE_BORDER))
    el.append(_food_vessel(336, 232))
    # Kneeling person with head turned RIGHT (away from bowl) + open mouth burping!
    el.append(
        f"""<path d="M 404,180 C 414,176 424,182 424,188 L 413,192 L 424,197 C 420,203 408,202 404,196 Z"
      fill="none" stroke="{ORANGE}" stroke-width="3.2" stroke-linejoin="round"/>
<path d="M 408,200 C 408,224 404,240 392,252 L 420,258" fill="none" stroke="{ORANGE}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 406,214 L 388,224" fill="none" stroke="{ORANGE}" stroke-width="3.2" stroke-linecap="round"/>
<path d="M 432,188 Q 442,183 448,186 M 433,195 Q 443,197 449,194" fill="none" stroke="{ORANGE}" stroke-width="2.0" stroke-linecap="round"/>"""
    )
    el.append(txt(284, 318, "• 镜头：米饭吃完，人把脸背过", size=11.5, color=BODY, weight="600"))
    el.append(txt(294, 338, "去张嘴打了个心满意足的饱嗝", size=11.5, color=BODY))
    el.append(txt(284, 364, "• 动作→时间：这顿饭吃完了 →", size=11.5, color=ORANGE, weight="600"))
    el.append(txt(294, 384, "已经 · 既然 · 既往不咎", size=11.5, color=ORANGE, weight="600"))
    el.append(txt(284, 412, "• 天文“日食既”：太阳被月亮彻", size=11.2, color=BODY))
    el.append(txt(294, 432, "底“吃光”的食甚全食时刻！", size=11.2, color=BODY))
    el.append(txt(284, 464, "• 一转头，就造出了汉语完成时", size=11, color=MUTED))

    # Card 3: 飨 / 卿 / 乡 (x=512..736, y=118..496)
    el.append(card(512, 118, 224, 378, rx=10))
    el.append(step_badge(532, 138, "3", fg=GREEN, bg=GREEN_SOFT, r=10))
    el.append(txt(548, 142, "第三幕：飨·卿（对坐共食）", size=13, color=INK, weight="700"))
    el.append(_glyph_plate(530, 156, 188, 138, bg=BRONZE_BG, border=BRONZE_BORDER))
    el.append(_food_vessel(624, 234))
    # Two kneeling figures facing EACH OTHER across center vessel x=624
    el.append(
        f"""<circle cx="566" cy="190" r="9" fill="none" stroke="{BRONZE_INK}" stroke-width="3.2"/>
<path d="M 564,200 C 564,222 568,240 578,252 L 552,258" fill="none" stroke="{BRONZE_INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 568,213 L 590,219" fill="none" stroke="{BRONZE_INK}" stroke-width="3.2" stroke-linecap="round"/>
<circle cx="682" cy="190" r="9" fill="none" stroke="{BRONZE_INK}" stroke-width="3.2"/>
<path d="M 684,200 C 684,222 680,240 670,252 L 696,258" fill="none" stroke="{BRONZE_INK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 680,213 L 658,219" fill="none" stroke="{BRONZE_INK}" stroke-width="3.2" stroke-linecap="round"/>"""
    )
    el.append(txt(528, 318, "• 镜头：宾主二人隔着盛满美馔", size=11.5, color=BODY, weight="600"))
    el.append(txt(538, 338, "的食簋促膝对坐、隆重共餐", size=11.5, color=BODY))
    el.append(txt(528, 364, "• 一幅画面分化出三个高频字：", size=11.5, color=GREEN, weight="600"))
    el.append(txt(538, 386, "1. 飨（xiǎng）：设宴款待宾客", size=11.2, color=BODY))
    el.append(txt(538, 408, "2. 乡（xiāng）：共食的同族聚落", size=11.2, color=BODY))
    el.append(txt(538, 430, "3. 卿（qīng）：能与君王同席共餐", size=11.2, color=INK, weight="600"))
    el.append(txt(552, 450, "的最高执政大臣（公卿大夫）！", size=11.2, color=GREEN, weight="700"))

    return figure(
        514,
        "即、既、飨（卿）围绕食器皀的三幕动作图解",
        "展示甲骨金文中以盛饭食器皀为中心，单人凑近就食为即、吃饱转头为既、双人对坐共食分化出飨、乡、卿三字的演变关系。",
        el,
    )


def build_plot_twists_wu_fa_jia() -> str:
    """Three famous character plot-twists: 武, 灋(法), 家."""
    el = []
    el.extend(
        header(
            "三大汉字反转现场：楚庄王改写的“武”、丢掉神兽的“法”，与屋下的“豕”",
            "把流传最广的经典佳话与甲骨金文证据摆在一起，看懂哲理升华、神兽断案与上古谐音",
        )
    )

    # Row 1: 武 (y=68..202, h=134)
    el.append(card(24, 68, 712, 134, rx=10))
    el.append(_glyph_plate(38, 80, 108, 110, bg=BONE_BG, border=BONE_BORDER))
    # Oracle-bone 武: halberd 戈 on top/right + 3-toed foot 止 below!
    el.append(
        f"""<path d="M 98,90 L 98,150 M 68,108 L 122,102 M 112,103 L 126,116 M 98,95 L 112,89"
      fill="none" stroke="{BONE_INK}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 64,174 L 98,174 M 76,174 L 76,154 M 64,160 L 64,174 M 89,158 L 89,174"
      fill="none" stroke="{ORANGE}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>"""
    )
    el.append(pill(162, 80, "反转 ① 武（戈 + 止）", fg=ORANGE, bg=ORANGE_SOFT, w=156, h=22, size=11.5))
    el.append(txt(330, 96, "到底是“制止战争”，还是“扛戈出征”？", size=12.5, color=INK, weight="700"))
    el.append(txt(162, 124, "• 经典哲理佳话（前597年）：楚庄王在《左传·宣公十二年》提出“夫文，止戈为武”，", size=11.5, color=BODY))
    el.append(txt(172, 145, "把“止”解作止息兵祸，赋予了“武”保大定功、安民和众的崇高反战境界。", size=11.5, color=BODY))
    el.append(txt(162, 171, "• 甲骨金文实证：“止”是脚趾“趾”的本字（步、走、征皆从它）！“戈+止”造字初义其实是", size=11.5, color=ORANGE, weight="600"))
    el.append(txt(172, 191, "士兵扛着长戈迈步出征——楚庄王明知兵戈残酷，故意借字形完成了一次伟大的价值重塑。", size=11.5, color=INK, weight="600"))

    # Row 2: 灋 -> 法 (y=214..348, h=134)
    el.append(card(24, 214, 712, 134, rx=10))
    el.append(_glyph_plate(38, 226, 108, 110, bg=BRONZE_BG, border=BRONZE_BORDER))
    # Bronze/Seal 灋: water 氵 left + single-horned unicorn 廌 top-right + 去 bottom-right
    el.append(
        f"""<path d="M 54,244 Q 60,256 53,268 M 50,278 Q 57,292 50,306 M 63,262 Q 68,278 62,296"
      fill="none" stroke="{BLUE}" stroke-width="3.2" stroke-linecap="round"/>
<path d="M 96,248 L 114,234 M 84,254 Q 104,244 122,256 Q 126,268 108,272 L 86,272 Q 82,262 84,254 Z"
      fill="none" stroke="{BRONZE_INK}" stroke-width="3.0" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 90,272 L 86,286 M 114,272 L 118,286" stroke="{BRONZE_INK}" stroke-width="2.8" stroke-linecap="round"/>
<path d="M 84,298 L 122,298 M 103,288 L 103,308 M 90,322 L 104,308 L 118,322 L 90,322"
      fill="none" stroke="{PURPLE}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>"""
    )
    el.append(pill(162, 226, "反转 ② 灋 → 法", fg=BLUE, bg=BLUE_SOFT, w=142, h=22, size=11.5))
    el.append(txt(316, 242, "被简化省掉的12笔里，藏着断案独角神兽“廌（獬豸）”！", size=12.5, color=INK, weight="700"))
    el.append(txt(162, 270, "• 古体“灋”的三重密码（晚商作册般铜鼋、西周大盂鼎已见）：《说文》解作“平之如水，从水；", size=11.5, color=BODY))
    el.append(txt(172, 291, "廌，所以触不直者；去之，从去”——水平面代表公平，独角兽顶翻理亏撒谎之人并将其驱逐。", size=11.5, color=BODY))
    el.append(txt(162, 317, "• 隶变留下的理性骨架：秦汉文书嫌画神兽太慢，省去“廌”只留“氵+ 去”，神判色彩悄然退场，", size=11.5, color=BLUE, weight="600"))
    el.append(txt(172, 337, "但“端平一碗水（氵）”与“祛除邪曲（去）”的法治内核一直留到了今天（荐举的“薦”也从廌）。", size=11.5, color=INK, weight="600"))

    # Row 3: 家 (y=360..494, h=134)
    el.append(card(24, 360, 712, 134, rx=10))
    el.append(_glyph_plate(38, 372, 108, 110, bg=SEAL_BG, border=SEAL_BORDER))
    # Oracle-bone 家: roof 宀 + male boar 𢑓/豭 inside!
    el.append(
        f"""<path d="M 92,382 L 92,392 M 54,412 L 54,394 L 130,394 L 130,412"
      fill="none" stroke="{SEAL_INK}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 72,420 Q 96,412 114,424 Q 120,438 106,454 L 82,454 Q 72,440 72,420 Z"
      fill="none" stroke="{GOLD}" stroke-width="3.2" stroke-linejoin="round"/>
<path d="M 72,424 L 62,418 M 82,454 L 76,470 M 106,454 L 112,470 M 116,434 L 126,440 M 92,438 L 99,445"
      fill="none" stroke="{GOLD}" stroke-width="3.0" stroke-linecap="round"/>"""
    )
    el.append(pill(162, 372, "反转 ③ 家（宀 + 豕/豭）", fg=PURPLE, bg=PURPLE_SOFT, w=176, h=22, size=11.5))
    el.append(txt(350, 388, "屋顶下画头猪，不只是农家养猪，更是3000年前的谐音梗！", size=12.5, color=INK, weight="700"))
    el.append(txt(162, 416, "• 传统生活与祭祀说：有遮风避雨的房屋（宀），蓄养或献祭珍贵的猪牲（豕），标志着定居宗族。", size=11.5, color=BODY))
    el.append(txt(162, 442, "• 甲骨声训铁证：甲骨文屋下画的特指公猪“𢑓/豭”（上古拟音 *kraː），与“家（*kraː）”同音！", size=11.5, color=PURPLE, weight="600"))
    el.append(txt(172, 463, "古文字学家（姚萱等）指出：它既绘室内祭祀，更借“豭”精准标音，后来笔画简化才与普通“豕”混同。", size=11.5, color=INK, weight="600"))

    return figure(
        512,
        "武、灋（法）、家三字哲理重解与考古字源对比图",
        "对比楚庄王止戈为武与甲骨文荷戈迈步、古体灋字水廌去三构件与今字法、以及家字屋下公猪豭兼具祭祀与上古音*kraː表音功能的三组汉字故事。",
        el,
    )


@register("gong-si-characters", "公与私及趣味象形会意汉字演变图解", "humanities")
def build_all() -> list[str]:
    specs = [
        ("gong-evolution-and-twist-anim.svg", build_gong_evolution_anim()),
        ("si-grain-and-private-field.svg", build_si_grain_and_field()),
        ("harvest-hands-bing-jian-li-nan.svg", build_harvest_hands_grid()),
        ("dinner-table-ji-ji-xiang-qing.svg", build_dinner_table_cinema()),
        ("classic-plot-twists-wu-fa-jia.svg", build_plot_twists_wu_fa_jia()),
    ]
    written = []
    for fname, svg_text in specs:
        write_svg(SUBDIR, fname, svg_text)
        written.append(f"assets/images/{SUBDIR}/{fname}")
    return written
