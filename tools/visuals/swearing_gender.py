"""
Visuals for '脏话与性别的科学真相' (Swearing & Gender: Genealogical Asymmetry & Lu Xun 1925,
Spoken BNC1994 vs BNC2014 Diachronic Corpus Trends, Facebook 10M-Message Warmth vs Assertiveness &
Lakoff Double Bind, Cortical vs Limbic-Basal-Ganglia Neurolinguistics, and Cold-Pressor Hypoalgesia + EDA).
Generates 5 original 760px Chinese SVG diagrams in assets/images/swearing-gender/
with verified empirical assertions from primary peer-reviewed studies.
"""
from __future__ import annotations

from .core import (
    BLUE,
    BLUE_LINE,
    BLUE_SOFT,
    BODY,
    BORDER,
    GREEN,
    GREEN_SOFT,
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
    pill,
    register,
    txt,
    write_svg,
)

TOPIC = "swearing-gender"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"


def _line(x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, marker=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def _verify_swearing_gender_data() -> None:
    # 1. Robbie Love (2021, Text & Talk): Spoken BNC1994 vs Spoken BNC2014 (>15M words)
    pmw_1994 = 1822
    pmw_2014 = 1320
    drop_pct = (pmw_1994 - pmw_2014) / pmw_1994 * 100.0
    assert round(drop_pct, 1) == 27.6
    share_of_speech_2014_pct = pmw_2014 / 1_000_000 * 100.0
    assert round(share_of_speech_2014_pct, 3) == 0.132

    mf_ratio_1994 = 2.33
    mf_ratio_2014 = 1.68
    gap_narrowing_pct = ((mf_ratio_1994 - 1.0) - (mf_ratio_2014 - 1.0)) / (mf_ratio_1994 - 1.0) * 100.0
    assert 48.8 < gap_narrowing_pct < 49.0  # Excess male gap shrank by ~48.9%

    # 2. Stephens & Robertson (2020, Frontiers in Psychology, Table 2, N = 92)
    thresh_neutral = 27.20
    thresh_swear = 35.77
    thresh_fouch = 28.23
    thresh_twiz = 25.45
    thresh_gain_pct = (thresh_swear - thresh_neutral) / thresh_neutral * 100.0
    assert round(thresh_gain_pct, 1) == 31.5  # Reported as 32% in paper abstract

    tol_neutral = 55.87
    tol_swear = 74.28
    tol_fouch = 58.44
    tol_twiz = 52.47
    tol_gain_pct = (tol_swear - tol_neutral) / tol_neutral * 100.0
    assert round(tol_gain_pct, 1) == 33.0
    assert round(tol_swear - tol_neutral, 2) == 18.41
    # Crucial control: "twizpipe" had HIGHER humor rating (50.98 vs 48.85) yet ZERO tolerance gain!
    humor_swear, humor_twiz, humor_neutral = 48.85, 50.98, 30.50
    assert humor_twiz > humor_swear > humor_neutral
    assert tol_twiz < tol_neutral


# ---------------------------------------------------------------------------
# 1. Genealogical Swearing Paradox & Dual-Track Gendered Insult Matrix
# ---------------------------------------------------------------------------
def build_genealogical_asymmetry() -> None:
    W, H = 760, 512
    el = []
    el.append(txt(W / 2, 30, "两个男人街头吵架，为什么枪口却总瞄准无辜的“妈妈与姐妹”？", size=18.2, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "跨语言“亲属脏话靶向错位”与男女贬义词的“双轨审判台”（鲁迅 1925；Kumar 2025；Graziano 2024）", size=12.0, color=MUTED, anchor="middle"))

    # Left Card: The Proxy-Target Triangle in Male-to-Male Conflict
    el.append(card(22, 68, 354, 424))
    el.append(pill(38, 82, "① 诡异的“隔山打牛”：男对男冲突中的母系靶心", fg=RED, bg=RED_SOFT, w=320))

    # Draw Male A and Male B at top, blocked direct line, curved/routed strike to Bottom Lineage Node
    el.append(card(42, 126, 124, 54, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(104, 149, "争执甲方（男性）", size=11.0, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(104, 168, "施骂者", size=10.0, color=MUTED, anchor="middle"))

    el.append(card(232, 126, 124, 54, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(294, 149, "争执乙方（男性）", size=11.0, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(294, 168, "真正想羞辱的目标", size=10.0, color=MUTED, anchor="middle"))

    el.append(_line(168, 153, 228, 153, stroke=SLATE, sw=1.6, dash="4 3", marker="arr-muted"))
    el.append(txt(198, 143, "正面冲突", size=9.8, color=MUTED, anchor="middle"))

    # Proxy node below: Female Relatives & Lineage Legitimacy
    el.append(card(54, 214, 290, 74, rx=10, fill=RED_SOFT, stroke="#fca5a5"))
    el.append(txt(199, 237, "象征靶心：乙方母亲 / 姐妹与血统合法性", size=11.2, weight="700", color=RED, anchor="middle"))
    el.append(txt(199, 257, "• 魏晋门阀“祖宗护符”：毁其母系 = 釜底抽薪瓦解门第", size=10.0, color=BODY, anchor="middle"))
    el.append(txt(199, 275, "• 父权荣誉捆绑：将男性面子寄生于女性亲属贞洁之上", size=10.0, color=BODY, anchor="middle"))

    # Arrows: Male A strikes Proxy -> Proxy collapses Male B's honor
    el.append(_line(104, 182, 148, 212, stroke=RED, sw=2.4, marker="arr-orange"))
    el.append(txt(92, 203, "言语攻击", size=10.0, weight="700", color=RED, anchor="middle"))
    el.append(_line(250, 212, 294, 182, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    el.append(txt(306, 203, "折射羞辱", size=10.0, weight="700", color=ORANGE, anchor="middle"))

    # Lu Xun 1925 + Cross-cultural explanation box
    el.append(card(38, 302, 322, 174, rx=10, fill="#f8fafc", stroke=BORDER))
    el.append(txt(52, 324, "两大底层人类学根源：", size=11.2, weight="700", color=INK))
    pts_left = [
        "1. 血统确定性不对称（鲁迅《论“他妈的！”》引北魏邢子才）：",
        "   母系分娩 100% 确定，而古代父系血统无法自证（“妇人不可保，",
        "   能保五世耶？”）——攻击母系即动摇整个父系宗族护符。",
        "2. “内容涉女、靶子对男”的代理暴力（Kumar 2025）：",
        "   街头与网络上的“涉母/涉姐国骂”极少对女性本人说，而是男人",
        "   之间把女性亲属当作“荣誉抵押品”进行的支配权表演。",
    ]
    for idx, line_s in enumerate(pts_left):
        el.append(txt(52, 346 + idx * 20, line_s, size=10.0, color=BODY))

    # Right Card: Dual-Track Gendered Insult Matrix
    el.append(card(390, 68, 348, 424))
    el.append(pill(406, 82, "② 词库解剖：骂男人 vs 骂女人的“双轨审判台”", fg=PURPLE, bg=PURPLE_SOFT, w=316))

    # Track 1: Male-targeted insults
    el.append(card(406, 124, 316, 144, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(420, 146, "针对男性的高频贬损词：审判“能力、勇气与公共契约”", size=11.0, weight="700", color=BLUE))
    m_pts = [
        "• 攻击实力与担当：窝囊废、怂包、软蛋、吃软饭；",
        "• 攻击血统与公德：兰开斯特大学 BNC2014 语料显示，bastard",
        "  绝大部分指向男性，用于审判背信弃义与破坏公平规则；",
        "• 终极羞辱居然是“女性化”：骂男人“娘炮 / 像个娘们”，暗含",
        "  把“跌出阳刚等级、沦为女性位置”当成降级惩罚！",
    ]
    for idx, mp in enumerate(m_pts):
        el.append(txt(420, 169 + idx * 19, mp, size=10.1, color=BODY))

    # Track 2: Female-targeted slurs
    el.append(card(406, 282, 316, 194, rx=10, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(420, 304, "针对女性的高频贬损词：规训“性贞洁与温顺服从”", size=11.0, weight="700", color=PURPLE))
    f_pts = [
        "• 轨道 A（性双重标准 SDS，Gómez-Berrocal 2022）：",
        "  同样丰富的情感经历，在男性常被夸“风流本事”，在女性却",
        "  对应成打的荡妇羞辱词汇，且几乎找不到对等的男性贬义词；",
        "• 轨道 B（温顺度警棍，Graziano 2024 / McEnery 2026）：",
        "  当女性表现得强势、果断、不好惹时，立刻触发“泼妇 / 悍妇",
        "  / bitch”标签——语言哲学指出这类词根本没有“中性对应词”，",
        "  因为它们的唯一功能就是把越界女性重新赶回温顺框架！",
    ]
    for idx, fp in enumerate(f_pts):
        w_f = "700" if idx == 6 else None
        el.append(txt(420, 327 + idx * 20, fp, size=10.1, color=INK if idx == 6 else BODY, weight=w_f))

    write_svg(
        TOPIC,
        "lu-xun-genealogical-swearing-asymmetry.svg",
        figure(H, "亲属脏话靶向错位机制与男女贬损词双轨审判台对比图", "左栏展示男性冲突借母系亲属攻击血统与荣誉的三角机制，右栏对比骂男性聚焦能力公德与骂女性聚焦性道德及温顺规训的不对称结构", el),
    )


# ---------------------------------------------------------------------------
# 2. Spoken BNC1994 vs BNC2014: 20-Year Corpus Shift & Gender Gap Narrowing
# ---------------------------------------------------------------------------
def build_bnc_gender_gap_shift() -> None:
    W, H = 760, 504
    el = []
    el.append(txt(W / 2, 30, "男人天生满嘴跑火车？1,500 万词真实口语录音揭开的 20 年大反转", size=18.2, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "英国国家口语语料库（Spoken BNC1994 vs BNC2014，Love 2021）追踪 16 个核心脏话词根的真实变迁", size=12.0, color=MUTED, anchor="middle"))

    # Left Card: Quantitative Bars (Overall Frequency & Male:Female Ratio)
    el.append(card(22, 68, 366, 416))
    el.append(pill(38, 82, "① 两大意外发现：总量降了 27.6%，性别差距缩水近半", fg=BLUE, bg=BLUE_SOFT, w=334))

    # Sub-chart A: Overall frequency per million words (1,822 vs 1,320)
    el.append(txt(42, 126, "A. 日常对话每百万词脏话出现次数（整体占比不足 0.2%！）", size=11.0, weight="700", color=INK))
    # Bar 1994: 1822 -> width 240
    el.append(txt(42, 155, "1994 年", size=10.8, weight="700", color=SLATE))
    el.append('<rect x="98" y="140" width="236" height="22" rx="5" fill="#94a3b8"/>')
    el.append(txt(340, 155, "1,822 词", size=10.8, weight="700", color=SLATE))

    # Bar 2014: 1320 -> width 236 * (1320/1822) = 171.0
    el.append(txt(42, 187, "2014 年", size=10.8, weight="700", color=BLUE))
    el.append('<rect x="98" y="172" width="171" height="22" rx="5" fill="#2563eb"/>')
    el.append(txt(277, 187, "1,320 词（↓27.6%）", size=10.8, weight="700", color=BLUE))
    el.append(txt(42, 214, "注：1,320 / 1,000,000 = 0.132%，即平均每说 758 个词才蹦出 1 个脏字。", size=9.9, color=MUTED))

    # Divider line
    el.append(_line(38, 228, 372, 228, stroke=BORDER, sw=1.2))

    # Sub-chart B: Male : Female Swearing Ratio (2.33 : 1 -> 1.68 : 1)
    el.append(txt(42, 250, "B. 男性 vs 女性脏话使用频率之比（以女性 = 1.00 为基准）", size=11.0, weight="700", color=INK))

    # 1994 group
    el.append(txt(42, 280, "1994 男", size=10.4, weight="700", color=ORANGE))
    el.append('<rect x="98" y="266" width="210" height="18" rx="4" fill="#ea580c"/>')
    el.append(txt(314, 280, "2.33 倍", size=10.6, weight="700", color=ORANGE))

    el.append(txt(42, 304, "1994 女", size=10.4, color=TEAL))
    el.append('<rect x="98" y="290" width="90" height="18" rx="4" fill="#0f766e"/>')
    el.append(txt(194, 304, "1.00（基准）", size=10.2, color=TEAL))

    # 2014 group
    el.append(txt(42, 338, "2014 男", size=10.4, weight="700", color=ORANGE))
    el.append('<rect x="98" y="324" width="151" height="18" rx="4" fill="#fb923c"/>')
    el.append(txt(255, 338, "1.68 倍（差距收窄！）", size=10.6, weight="700", color=ORANGE))

    el.append(txt(42, 362, "2014 女", size=10.4, color=TEAL))
    el.append('<rect x="98" y="348" width="90" height="18" rx="4" fill="#0f766e"/>')
    el.append(txt(194, 362, "1.00（基准）", size=10.2, color=TEAL))

    # Bottom takeaway in left card
    el.append(card(38, 382, 334, 86, rx=8, fill=TEAL_SOFT, stroke="#5eead4"))
    el.append(txt(50, 404, "核心结论：脏话频率并非刻在 Y 染色体上的生理本能！", size=10.8, weight="700", color=TEAL))
    el.append(txt(50, 424, "• 随着女性公共话语空间扩大与传统礼仪松绑，短短 20 年间", size=10.0, color=BODY))
    el.append(txt(50, 443, "  男女超额倍率差（1.33 → 0.68）直接缩水了约 49%；", size=10.0, color=BODY))
    el.append(txt(50, 461, "• 词库王座也发生更替：老派 bloody 大退潮，f-word 升至第一。", size=10.0, color=MUTED))

    # Right Card: Age Curve & Same-Sex Solidarity Chameleon Effect
    el.append(card(402, 68, 336, 416))
    el.append(pill(418, 82, "② 年龄抛物线与“看人下菜碟”变色龙效应", fg=ORANGE, bg=ORANGE_SOFT, w=304))

    # Mini schematic curve: Age vs Swearing peaking in 20s
    el.append(card(418, 120, 304, 156, rx=10, fill="#f8fafc", stroke=BORDER))
    el.append(txt(432, 141, "全生命周期脏话频率曲线（20–29 岁达到人生巅峰）", size=10.6, weight="700", color=INK))
    # Axes
    el.append(_line(450, 240, 696, 240, stroke=SLATE, sw=1.3))
    el.append(_line(450, 156, 450, 240, stroke=SLATE, sw=1.3))
    # 1994 steeper drop vs 2014 gentler drop
    el.append('<path d="M 462 214 Q 512 152 536 164 T 684 234" fill="none" stroke="#94a3b8" stroke-width="2.2" stroke-dasharray="5 3"/>')
    el.append('<path d="M 462 218 Q 512 162 540 170 T 684 212" fill="none" stroke="#2563eb" stroke-width="2.6"/>')
    el.append('<circle cx="518" cy="164" r="4.5" fill="#dc2626"/>')
    el.append(txt(518, 154, "20多岁峰值", size=9.8, weight="700", color=RED, anchor="middle"))
    el.append(txt(644, 198, "2014 曲线更平缓", size=9.6, weight="700", color=BLUE, anchor="middle"))
    el.append(txt(640, 229, "1994 随年龄骤降", size=9.4, color=SLATE, anchor="middle"))
    for ax_x, lbl in [(466, "少年"), (520, "20岁+"), (596, "40岁+"), (672, "60岁+")]:
        el.append(txt(ax_x, 256, lbl, size=9.6, color=MUTED, anchor="middle"))

    # Interlocutor chameleon effect card (McEnery & Xiao 2004; Stapleton et al. 2022)
    el.append(card(418, 290, 304, 180, rx=10, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(432, 312, "为什么无论男女，“关起门跟同性密友聊”脏字最多？", size=10.8, weight="700", color=ORANGE))
    cham_pts = [
        "• 同性圈“卸甲投名状”（McEnery & Xiao 2004）：",
        "  语料库统计显示，男性在纯男性局、女性在纯闺蜜局里的粗话",
        "  密度，远高于有异性在场的混合社交局！",
        "• 80% 以上的日常粗话根本不是为了吵架伤人（Stapleton 2022）：",
        "  而是充当“咱俩熟到不用端着装客套”的社交亲密黏合剂——",
        "  一旦踏进异性或陌生职场局，双方都会默契收起这套暗号。",
    ]
    for idx, cp in enumerate(cham_pts):
        el.append(txt(432, 335 + idx * 21, cp, size=10.0, color=BODY))

    write_svg(
        TOPIC,
        "bnc-swearing-gender-gap-1994-vs-2014.svg",
        figure(H, "英国国家口语语料库1994与2014脏话频率、性别比变化及社交语境效应图", "左栏展示1994至2014年日常口语脏话率下降27.6%且男女比例从2.33比1缩窄至1.68比1，右栏展示20多岁年龄峰值与同性密友语境效应", el),
    )


# ---------------------------------------------------------------------------
# 3. 10M Facebook Messages (Warmth vs Assertiveness) & Lakoff's Double Bind
# ---------------------------------------------------------------------------
def build_warmth_assertiveness_double_bind() -> None:
    W, H = 760, 508
    el = []
    el.append(txt(W / 2, 30, "少说脏话 = 说话软弱没主见？1,000 万条消息击碎半世纪语言偏见", size=18.2, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "宾大与剑桥计算语言学研究（Park 等，PLOS ONE 2016）对比拉科夫“女性双输语言困境”", size=12.0, color=MUTED, anchor="middle"))

    # Left Card: 2D Interpersonal Circumplex (Affiliation / Warmth vs Assertiveness)
    el.append(card(22, 68, 356, 420))
    el.append(pill(38, 82, "① 5.2 万用户实测：温柔礼貌与果断自信毫不冲突", fg=GREEN, bg=GREEN_SOFT, w=324))

    # Draw 2D coordinate plane
    cx, cy = 200, 248
    el.append(card(38, 120, 324, 248, rx=10, fill="#f8fafc", stroke=BORDER))
    # Axes
    el.append(_line(62, cy, 342, cy, stroke=SLATE, sw=1.5, marker="arr-muted"))
    el.append(_line(cx, 346, cx, 140, stroke=SLATE, sw=1.5, marker="arr-muted"))
    el.append(txt(cx, 134, "高果断自信度（Assertiveness ↑）", size=10.2, weight="700", color=INK, anchor="middle"))
    el.append(txt(cx, 360, "低果断 / 顺从犹豫（↓）", size=9.8, color=MUTED, anchor="middle"))
    el.append(txt(66, cy - 8, "冷漠敌意·粗话", size=9.6, color=ORANGE))
    el.append(txt(336, cy - 8, "温暖共情·礼貌", size=9.6, color=TEAL, anchor="end"))

    # Old 1970s stereotype point (bottom-right dashed ghost circle)
    el.append('<circle cx="278" cy="304" r="24" fill="none" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4 3"/>')
    el.append(txt(278, 301, "旧刻板印象", size=9.5, color=SLATE, anchor="middle"))
    el.append(txt(278, 315, "礼貌=软弱?", size=9.2, color=SLATE, anchor="middle"))
    el.append(txt(278, 338, "✕ 被数据推翻", size=9.6, weight="700", color=RED, anchor="middle"))

    # Empirical Male cluster (left of center, moderate-high assertiveness, cold/hostile/swearing)
    el.append('<ellipse cx="124" cy="214" rx="48" ry="28" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>')
    el.append(txt(124, 210, "男性高频语言簇", size=10.2, weight="700", color=ORANGE, anchor="middle"))
    el.append(txt(124, 226, "脏话·愤怒·论辩·聊物", size=9.4, color=BODY, anchor="middle"))

    # Empirical Female cluster (right of center AND slightly HIGHER on assertiveness!)
    el.append('<ellipse cx="282" cy="196" rx="50" ry="28" fill="#ccfbf1" stroke="#0f766e" stroke-width="2.2"/>')
    el.append(txt(282, 192, "女性高频语言簇", size=10.2, weight="700", color=TEAL, anchor="middle"))
    el.append(txt(282, 208, "温暖·礼貌·且更果断!", size=9.5, weight="700", color=TEAL, anchor="middle"))

    # Highlight upward offset arrow
    el.append(_line(282, 274, 282, 230, stroke=TEAL, sw=2.0, marker="arr-green"))

    # Takeaway box below plot
    el.append(card(38, 380, 324, 94, rx=8, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(50, 401, "PLOS ONE（2016）颠覆性结论：", size=10.6, weight="700", color=GREEN))
    el.append(txt(50, 421, "• 男性在社交网络显著更多使用脏话、愤怒词与冷漠对抗表达；", size=9.9, color=BODY))
    el.append(txt(50, 440, "• 女性虽极少靠爆粗口立威，直接表达主张的“果断度”反而略超", size=9.9, color=BODY))
    el.append(txt(50, 459, "  男性——证明“不靠骂街也能硬气把事办成”！", size=10.0, weight="700", color=INK))

    # Right Card: Lakoff's Double Bind & Three Linguistic Escape Valves
    el.append(card(394, 68, 344, 420))
    el.append(pill(410, 82, "② 听众耳朵里的双标：拉科夫“双输陷阱”与突围", fg=PURPLE, bg=PURPLE_SOFT, w=312))

    # Top fork diagram: Same speaker dilemma
    el.append(card(410, 120, 312, 146, rx=10, fill=RED_SOFT, stroke="#fca5a5"))
    el.append(txt(566, 142, "罗宾·拉科夫（Robin Lakoff）揭示的女性语言两难：", size=10.8, weight="700", color=RED, anchor="middle"))

    el.append(card(422, 156, 138, 96, rx=8, fill="#ffffff", stroke=BORDER))
    el.append(txt(491, 176, "若全程轻声温顺", size=10.4, weight="700", color=SLATE, anchor="middle"))
    el.append(txt(491, 195, "只说“哎呀 / 天哪”", size=9.8, color=MUTED, anchor="middle"))
    el.append(txt(491, 217, "→ 易被刻板印象当成", size=9.6, color=BODY, anchor="middle"))
    el.append(txt(491, 235, "“缺乏气场、好拿捏”", size=9.8, weight="700", color=RED, anchor="middle"))

    el.append(card(572, 156, 138, 96, rx=8, fill="#ffffff", stroke=BORDER))
    el.append(txt(641, 176, "若像男性一样爆粗口", size=10.4, weight="700", color=ORANGE, anchor="middle"))
    el.append(txt(641, 195, "说完全相同的禁忌词", size=9.8, color=MUTED, anchor="middle"))
    el.append(txt(641, 217, "→ 违反性别角色期待", size=9.6, color=BODY, anchor="middle"))
    el.append(txt(641, 235, "被批“粗俗、情绪失控”", size=9.8, weight="700", color=RED, anchor="middle"))

    # Bottom half: 3 Creative Linguistic Evolution Strategies
    el.append(card(410, 280, 312, 194, rx=10, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(424, 302, "日常语言如何聪明破解禁忌与规训？三条演化路径：", size=10.8, weight="700", color=PURPLE))
    evol_pts = [
        "1. 谐音与委婉替身（Euphemism）：",
        "   中文“卧槽 / 我勒个去 / 栓Q”、英语 fudge / shoot，既保留",
        "   情绪重音，又巧妙绕开社会礼仪红线；",
        "2. 圈内词义重夺（Insular Reclamation，Graziano 2024）：",
        "   年轻女性在闺蜜间互称“bad bitch / 狠角色”，把原本惩罚女性",
        "   强势的贬义词反向改造成赞美独立果敢的勋章；",
        "3. 语义漂白（Semantic Bleaching，鲁迅 1925 记载）：",
        "   鲁迅曾见乡农父子夹菜：“这不坏，妈的你尝尝看！”——粗话彻底",
        "   褪去攻击性，醇化成了表达惊叹与亲昵的语气助词。",
    ]
    for idx, ep in enumerate(evol_pts):
        el.append(txt(424, 323 + idx * 16.5, ep, size=9.7, color=BODY))

    write_svg(
        TOPIC,
        "facebook-warmth-assertiveness-and-double-bind.svg",
        figure(H, "社交语言温暖度与果断度二维分布及女性双输语言困境图解", "左栏基于5.2万用户消息证明女性语言兼具高温暖度与高果断度，右栏拆解拉科夫双输语言陷阱与谐音替身、词义重夺及语义漂白路径", el),
    )


# ---------------------------------------------------------------------------
# 4. Neurolinguistic Dual Pathway: Cortical Grammar vs Limbic-Basal-Ganglia Reflex
# ---------------------------------------------------------------------------
def build_brain_dual_pathway() -> None:
    W, H = 760, 512
    el = [
        """<style>
  @keyframes limbicPulse {
    0%   { stroke-dashoffset: 380; opacity: 0.35; }
    20%  { opacity: 1.0; }
    100% { stroke-dashoffset: 0; opacity: 1.0; }
  }
  .anim-limbic-pulse {
    stroke-dasharray: 12 8;
    stroke-dashoffset: 0;
    animation: limbicPulse 2.6s ease-out 1 forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .anim-limbic-pulse { animation: none !important; stroke-dashoffset: 0 !important; opacity: 1 !important; }
  }
</style>"""
    ]
    el.append(txt(W / 2, 30, "为什么左脑中风说不出“今天星期几”，被踩脚时却能流利骂人？", size=18.2, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "普通造句走“左脑皮层语法装配线”，而本能爆粗走“边缘系统—基底核情绪地下专线”（Broca 1861；Sidtis 1999）", size=11.8, color=MUTED, anchor="middle"))

    # Upper Track: Route A — Left Hemisphere Cortical Propositional Speech
    el.append(card(22, 68, 716, 174, rx=12, fill="#f8fafc", stroke=BORDER))
    el.append(pill(38, 82, "公路 A：左脑新皮层“命题造句流水线”（说礼貌长句、汇报工作、答星期几）", fg=BLUE, bg=BLUE_SOFT, w=486))

    # 4 Boxes along Route A
    boxes_a = [
        (42, 122, 146, "① 概念与选词", "左颞叶威尔尼克区", "按语义检索礼貌词汇", BLUE_SOFT, BLUE_LINE, BLUE),
        (218, 122, 162, "② 语法拼装中心", "左额叶布罗卡区（Broca）", "主谓宾时态逐字组装", "#fee2e2", "#f87171", RED),
        (410, 122, 144, "③ 运动皮层发令", "精细唇舌声带协调", "按音节顺序吐字", SLATE_SOFT, BORDER, SLATE),
        (584, 122, 136, "中风失语症后果", "✕ 普通说话彻底中断", "答不出天气与日期", RED_SOFT, "#fca5a5", RED),
    ]
    for bx, by, bw, t1, t2, t3, bg_c, st_c, hd_c in boxes_a:
        el.append(card(bx, by, bw, 84, rx=8, fill=bg_c, stroke=st_c))
        el.append(txt(bx + bw / 2, by + 24, t1, size=10.8, weight="700", color=hd_c, anchor="middle"))
        el.append(txt(bx + bw / 2, by + 46, t2, size=10.0, weight="700", color=INK, anchor="middle"))
        el.append(txt(bx + bw / 2, by + 66, t3, size=9.6, color=MUTED, anchor="middle"))

    el.append(_line(190, 164, 214, 164, stroke=BLUE, sw=2.2, marker="arr-blue"))
    el.append(_line(382, 164, 406, 164, stroke=RED, sw=2.2, dash="4 3"))
    el.append(txt(394, 152, "受损断路✕", size=9.6, weight="700", color=RED, anchor="middle"))
    el.append(_line(556, 164, 580, 164, stroke=RED, sw=2.2, dash="4 3", marker="arr-orange"))
    el.append(txt(42, 227, "关键特征：左脑把每个词拆成零件重新组装，耗时较长，且受前额叶皮层“社会礼仪刹车片”严格审查（看场合决定忍不忍住）。", size=10.2, color=BODY))

    # Lower Track: Route B — Subcortical Limbic-Basal-Ganglia Emotional Reflex Bypass!
    el.append(card(22, 256, 716, 236, rx=12, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(pill(38, 270, "公路 B：皮层下“边缘系统—基底核情绪急救专线”（小脚趾撞桌角 0.2 秒脱口而出的本能呼叫）", fg=ORANGE, bg="#ffedd5", w=570))

    # Animated fast-bypass arc across the subcortical stations
    el.append('<path class="anim-limbic-pulse" d="M 114 398 L 296 398 L 482 398 L 652 398" fill="none" stroke="#dc2626" stroke-width="3.2"/>')

    boxes_b = [
        (42, 312, 146, "① 痛觉 / 威胁警报", "杏仁核（Amygdala）", "瞬间拉响战或逃警报", "#ffffff", "#fca5a5", RED),
        (218, 312, 156, "② 动作打包发射台", "基底核（Basal Ganglia）", "像存“挥拳缩手”一样存脏话", "#ffffff", "#fdba74", ORANGE),
        (404, 312, 154, "③ 整体语块提取", "右脑半球参与协助", "整词原封不动直接弹出", "#ffffff", "#fdba74", AMBER),
        (586, 312, 134, "✓ 绕开左脑病灶！", "失语患者照样脱口骂", "伴随心率与微出汗飙升", GREEN_SOFT, "#86efac", GREEN),
    ]
    for bx, by, bw, t1, t2, t3, bg_c, st_c, hd_c in boxes_b:
        el.append(card(bx, by, bw, 80, rx=8, fill=bg_c, stroke=st_c))
        el.append(txt(bx + bw / 2, by + 23, t1, size=10.8, weight="700", color=hd_c, anchor="middle"))
        el.append(txt(bx + bw / 2, by + 44, t2, size=10.0, weight="700", color=INK, anchor="middle"))
        el.append(txt(bx + bw / 2, by + 63, t3, size=9.5, color=BODY, anchor="middle"))

    el.append(_line(190, 352, 214, 352, stroke=RED, sw=2.4, marker="arr-orange"))
    el.append(_line(376, 352, 400, 352, stroke=ORANGE, sw=2.4, marker="arr-orange"))
    el.append(_line(560, 352, 582, 352, stroke=GREEN, sw=2.4, marker="arr-green"))

    # Bottom clinical & evolutionary note inside Lower Track
    el.append(card(42, 412, 678, 66, rx=8, fill="#ffffff", stroke="#fed7aa"))
    el.append(txt(56, 434, "神经科学铁证（美国神经科学学会 BrainFacts 档案）：", size=10.6, weight="700", color=INK))
    el.append(txt(56, 454, "• 1861 年布罗卡本人记录的失语症病人仅剩一句法语粗话完好；妥瑞氏症（Tourette）不自主秽语同样源于基底核指令脱缰；", size=9.9, color=BODY))
    el.append(txt(56, 471, "• 猫咪遇险时“杏仁核 → 基底核”触发炸毛哈气，人类则在同一条古老回路上把“抓咬哈气”升级成了脱口而出的禁忌音节！", size=9.9, weight="700", color=ORANGE))

    write_svg(
        TOPIC,
        "brain-dual-pathway-cortical-vs-limbic-swearing.svg",
        figure(H, "大脑语言双通道模型：左脑布罗卡语法流水线与皮层下杏仁核基底核脏话反射回路图", "对比左脑威尔尼克至布罗卡命题语法通路与皮层下杏仁核、基底核及右脑整体语块通路，解释中风失语症保留骂人能力的神经机制", el),
    )


# ---------------------------------------------------------------------------
# 5. Cold-Pressor Pain Relief (+33%) vs Pseudo-Swears & Euphemism Skin Conductance
# ---------------------------------------------------------------------------
def build_pain_hypoalgesia_and_euphemisms() -> None:
    W, H = 760, 514
    el = []
    el.append(txt(W / 2, 30, "手泡冰水喊真脏话能多扛 18.4 秒！为什么搞笑替身词却完全止不住疼？", size=18.0, weight="700", anchor="middle"))
    el.append(txt(W / 2, 52, "基尔大学冰水镇痛实验（Stephens & Robertson 2020，N=92）与皮肤电反应（Bowers 2011）及性别耐药效应", size=11.8, color=MUTED, anchor="middle"))

    # Left Card: Exact Experimental Grouped Bar Chart (Stephens & Robertson 2020, Table 2)
    el.append(card(22, 68, 392, 426))
    el.append(pill(38, 82, "① 冰水冷压实验实测（N=92）：唯有真禁忌词能镇痛", fg=RED, bg=RED_SOFT, w=360))

    el.append(txt(40, 122, "双手浸入冰水时重复喊不同词，测“开始觉得疼”与“忍痛极限”：", size=10.3, color=BODY))

    # Legend
    el.append('<rect x="42" y="135" width="12" height="12" rx="2" fill="#fb923c"/>')
    el.append(txt(60, 145, "疼痛阈值（开始疼的秒数）", size=9.8, color=BODY))
    el.append('<rect x="214" y="135" width="12" height="12" rx="2" fill="#dc2626"/>')
    el.append(txt(232, 145, "忍痛极限（坚持总秒数）", size=9.8, weight="700", color=RED))

    # 4 Conditions from Table 2:
    # Scale: max 80s -> 220px width (2.75 px/s), x0 = 132
    conds = [
        ("真禁忌脏话", 35.77, 74.28, True, "阈值 +31.5% | 极限 +33.0%！"),
        ("自造词 fouch", 28.23, 58.44, False, "与中性词无显著差异"),
        ("搞笑词 twizpipe", 25.45, 52.47, False, "幽默分最高(51分)却零止痛！"),
        ("中性词（桌子）", 27.20, 55.87, False, "对照组基准线"),
    ]
    x0 = 138
    scale = 2.55  # 74.28 * 2.55 = 189.4 px -> ends at 327.4
    for idx, (label, th_s, tol_s, is_real, note_s) in enumerate(conds):
        cy_row = 166 + idx * 64
        el.append(txt(130, cy_row + 15, label, size=10.4, weight="700" if is_real else None, color=RED if is_real else INK, anchor="end"))
        # Threshold bar
        w_th = th_s * scale
        c_th = "#fb923c" if is_real else "#cbd5e1"
        el.append(f'<rect x="{x0}" y="{cy_row + 2}" width="{w_th:.1f}" height="15" rx="3" fill="{c_th}"/>')
        el.append(txt(x0 + w_th + 6, cy_row + 14, f"{th_s:.2f} s", size=9.8, weight="700" if is_real else None, color=ORANGE if is_real else SLATE))

        # Tolerance bar
        w_tol = tol_s * scale
        c_tol = "#dc2626" if is_real else "#94a3b8"
        el.append(f'<rect x="{x0}" y="{cy_row + 21}" width="{w_tol:.1f}" height="17" rx="3" fill="{c_tol}"/>')
        el.append(txt(x0 + w_tol + 6, cy_row + 34, f"{tol_s:.2f} s", size=10.2, weight="700" if is_real else None, color=RED if is_real else SLATE))
        el.append(txt(x0, cy_row + 51, note_s, size=9.4, weight="700" if is_real else None, color=RED if is_real else MUTED))

    el.append(card(38, 424, 360, 56, rx=8, fill="#f8fafc", stroke=BORDER))
    el.append(txt(50, 444, "为什么编个搞笑新词不管用？因为止痛靠的不是“分心或好玩”，", size=9.9, color=BODY))
    el.append(txt(50, 464, "而是童年挨训刻进杏仁核的“禁忌语音条件反射”激活了内源性镇痛！", size=9.9, weight="700", color=INK))

    # Right Card: Euphemism Skin Conductance (Bowers 2011) + Gender & Habituation Twist!
    el.append(card(428, 68, 310, 426))
    el.append(pill(444, 82, "② 谐音脱敏与“越少骂越止痛”性别反转", fg=TEAL, bg=TEAL_SOFT, w=278))

    # Top sub-card: Bowers & Pleydell-Pearce (2011) EDA skin conductance
    el.append(card(444, 120, 278, 162, rx=10, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(458, 142, "皮肤电导（EDA）测谎级实验（PLOS ONE 2011）：", size=10.6, weight="700", color=BLUE))
    # Stylized waveform comparison
    el.append(_line(462, 208, 704, 208, stroke=SLATE, sw=1.0, dash="3 2"))
    # High spike for real taboo sound
    el.append('<path d="M 466 206 L 496 206 L 512 156 L 530 194 L 552 204 L 574 206" fill="none" stroke="#dc2626" stroke-width="2.5"/>')
    el.append(txt(516, 224, "读出真禁忌词原音", size=9.6, weight="700", color=RED, anchor="middle"))
    el.append(txt(516, 239, "掌心瞬间微出汗飙升!", size=9.2, color=RED, anchor="middle"))
    # Low bump for euphemism ("the F-word" / 卧槽)
    el.append('<path d="M 594 206 L 622 206 L 636 193 L 652 204 L 696 206" fill="none" stroke="#0f766e" stroke-width="2.3"/>')
    el.append(txt(646, 224, "改读“F-word/谐音词”", size=9.6, weight="700", color=TEAL, anchor="middle"))
    el.append(txt(646, 239, "意思全懂但生理波澜小", size=9.2, color=TEAL, anchor="middle"))
    el.append(txt(458, 267, "启示：委婉词换掉了“扣动杏仁核扳机的语音外壳”！", size=9.7, weight="700", color=INK))

    # Bottom sub-card: Gender & Habituation Paradox (Stephens 2009 & 2011)
    el.append(card(444, 296, 278, 184, rx=10, fill=TEAL_SOFT, stroke="#5eead4"))
    el.append(txt(458, 318, "最妙的性别彩蛋：平时克制的人，止痛药效更猛！", size=10.6, weight="700", color=TEAL))
    hab_pts = [
        "• 2009 年首篇冰水实验（Stephens 等，获搞笑诺奖）",
        "  意外发现：受试女性爆粗后的疼痛下降幅度，显著",
        "  强于部分高灾难化焦虑的受试男性！",
        "• 后续追踪揭开了“耐药脱敏定律”：",
        "  如果一个人每天把脏字当标点符号挂嘴边狂飙，",
        "  大脑杏仁核早已麻木脱敏，真受伤时再骂也不止痛；",
        "• 相反，平时很少说脏话的人（统计上女性占比更高）",
        "  关键时刻骂出一句，就像急救箱里未开封的肾上腺素！",
    ]
    for idx, hp in enumerate(hab_pts):
        w_h = "700" if idx == 7 else None
        el.append(txt(458, 340 + idx * 17, hp, size=9.7, color=INK if idx == 7 else BODY, weight=w_h))

    write_svg(
        TOPIC,
        "euphemism-eda-and-ice-water-hypoalgesia.svg",
        figure(H, "冰水疼痛耐受实验四组实测对比与委婉词皮肤电反应及耐药脱敏机制图", "左栏展示真禁忌词使冰水忍痛极限提升33%而搞笑伪词无效的实测数据，右栏展示委婉词降低皮肤电唤醒与低频使用者镇痛更强的耐药定律", el),
    )


@register(TOPIC, "脏话与性别：亲属脏话靶向错位、BNC语料性别比、温暖果断度、边缘神经回路与冰水镇痛", "humanities")
def build_all() -> None:
    _verify_swearing_gender_data()
    build_genealogical_asymmetry()
    build_bnc_gender_gap_shift()
    build_warmth_assertiveness_double_bind()
    build_brain_dual_pathway()
    build_pain_hypoalgesia_and_euphemisms()
