"""冬天树木落叶快慢与松柏常青四重防冻机制（5 图，含冻融气泡栓塞与纹孔塞单次动画）。"""

from __future__ import annotations

import math
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
    txt,
    write_svg,
)

TOPIC = "winter-leaf-strategies"

RED = "#b91c1c"
RED_SOFT = "#fef2f2"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
GOLD = "#ca8a04"
GOLD_SOFT = "#fefce8"
BROWN = "#78350f"
BROWN_SOFT = "#fef3c7"


def verify_winter_leaf_math() -> None:
    """校验哈根-泊肃叶四次方流量比、拉普拉斯临界气泡直径与冻融栓塞阈值。"""
    # 1) 哈根-泊肃叶单管流量正比于 D^4：100 um 阔叶环孔材早材导管 vs 20 um 柏树管胞
    d_vessel = 100.0
    d_tracheid = 20.0
    flow_ratio = (d_vessel / d_tracheid) ** 4
    assert math.isclose(flow_ratio, 625.0, rel_tol=1e-9)

    # 2) 拉普拉斯公式 |Px*| = 4 * sigma / Db
    # 水表面张力 sigma = 0.0728 N/m，木质部负压 Px = -0.5 MPa = -5e5 Pa
    sigma = 0.0728
    px_abs = 5.0e5
    d_bubble_crit_um = (4.0 * sigma / px_abs) * 1e6
    assert 0.55 < d_bubble_crit_um < 0.62  # ~0.5824 um (Pittermann & Sperry 2006)

    # 3) 临界导管/管胞内径阈值：-0.5 MPa 下约 35~44 um；圆柏 <=20 um 安全，落羽杉 ~40 um 栓塞落叶
    d_juniper = 20.0
    d_taxodium = 40.0
    d_ash = 150.0
    assert d_juniper < 35.0 < d_taxodium <= 44.0 < d_ash


# ---------------------------------------------------------------------------
# 图 1：秋冬到开春四类树木留叶率时间曲线（9月 → 次年5月）
# ---------------------------------------------------------------------------
def build_four_speed_phenology_timeline() -> str:
    h = 410
    els: list[str] = []
    els.extend(
        header(
            "同吹一场秋风，四类大树完全不同的“脱衣时刻表”（9月 → 次年5月）",
            "典型趋势示意（非逐树实测数据）：闪电暴落派、磨蹭缓落派、枯而不落钉子户与“暗中轮休”的松柏常青派",
        )
    )

    # 左侧折线坐标区 card(20, 62, 504, 326)
    els.append(card(20, 62, 504, 326))
    els.append(pill(34, 73, "树冠挂叶比例随月份变化曲线（示意图，以华北/温带物候为基准）", BLUE, BLUE_SOFT, w=392, h=22, size=11))

    # 绘图框 x: 74..498 (宽 424, 8 个间隔 * 53 px), y: 112 (100%) .. 312 (0%) (高 200)
    x0, y100, y0 = 74.0, 112.0, 312.0
    dx = 53.0

    def pt(idx: float, pct: float) -> tuple[float, float]:
        return x0 + idx * dx, y0 - (pct / 100.0) * (y0 - y100)

    # 水平网格线与纵轴刻度
    for pct in (0, 25, 50, 75, 100):
        _, gy = pt(0, pct)
        els.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x0 + 8*dx:.1f}" y2="{gy:.1f}" stroke="{HAIRLINE}" stroke-width="1" stroke-dasharray="3,3"/>')
        els.append(txt(66, gy + 4, f"{pct}%", 10.5, MUTED, "end"))

    # 初霜竖向高亮带（11月上旬 idx ≈ 2.25）
    fx, _ = pt(2.25, 0)
    els.append(f'<rect x="{fx - 12:.1f}" y="{y100 - 4:.1f}" width="24" height="{y0 - y100 + 8:.1f}" fill="{BLUE_SOFT}" opacity="0.85"/>')
    els.append(f'<line x1="{fx:.1f}" y1="{y100 - 4:.1f}" x2="{fx:.1f}" y2="{y0:.1f}" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="4,3"/>')
    els.append(txt(fx, y100 - 8, "初霜寒潮 (-3°C)", 10.0, BLUE, "middle", weight="700"))

    # 春季萌芽竖线（4月 idx ≈ 7.0）
    sx, _ = pt(7.0, 0)
    els.append(f'<line x1="{sx:.1f}" y1="{y100 - 4:.1f}" x2="{sx:.1f}" y2="{y0:.1f}" stroke="{GREEN}" stroke-width="1.2" stroke-dasharray="3,3"/>')
    els.append(txt(sx, y100 - 8, "春芽顶落宿叶", 10.0, GREEN, "middle", weight="700"))

    # 横轴月份标签
    months = ["9月", "10月", "11月初", "11月末", "12月", "1月", "2–3月", "4月", "5月"]
    els.append(f'<line x1="{x0}" y1="{y0}" x2="{x0 + 8*dx:.1f}" y2="{y0}" stroke="{SLATE}" stroke-width="1.4"/>')
    for i, m in enumerate(months):
        mx, _ = pt(i, 0)
        els.append(f'<line x1="{mx:.1f}" y1="{y0}" x2="{mx:.1f}" y2="{y0 + 5:.1f}" stroke="{SLATE}" stroke-width="1.2"/>')
        els.append(txt(mx, y0 + 19, m, 10.2, BODY, "middle"))

    # 4 条实算曲线
    # 1) 松树/柏树（常绿分批轮休：秋季仅退掉约 20% 三四年生内侧老针叶，常年保绿 80%~100%）
    pine_pts = [(0, 100), (1, 95), (2, 82), (3, 80), (4, 80), (5, 80), (6, 80), (7, 90), (8, 100)]
    # 2) 栎树/山毛榉（枯而不落 Marcescence：11月叶片枯死停工，但 72%~82% 干叶挂满寒冬，4月新芽顶落后再抽新叶）
    oak_dead = [(2, 88), (3, 82), (4, 78), (5, 76), (6, 72), (7, 14)]
    oak_live_pre = [(0, 100), (1, 96), (2, 88)]
    oak_live_post = [(7, 14), (8, 92)]
    # 3) 垂柳/法桐（慢性渐次落叶：散孔材耐轻霜，从10月拖到12月下旬才落净）
    willow_pts = [(0, 100), (1, 94), (2, 76), (3, 48), (4, 15), (5, 2), (6, 0), (7, 52), (8, 96)]
    # 4) 银杏/白蜡（闪电同步暴落：初霜后 24~48h 内从 92% 断崖跌至 ~0%！）
    ginkgo_pts = [(0, 100), (1, 98), (2.15, 92), (2.45, 3), (3, 0), (4, 0), (5, 0), (6, 0), (7, 36), (8, 94)]

    def poly(pts_list, color, width=2.6, dash=""):
        coords = " ".join(f"{pt(i, p)[0]:.1f},{pt(i, p)[1]:.1f}" for i, p in pts_list)
        d_attr = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{d_attr}/>'

    els.append(poly(pine_pts, GREEN, 2.8))
    els.append(poly(oak_live_pre, BROWN, 2.4))
    els.append(poly(oak_dead, BROWN, 2.6, "6,4"))
    els.append(poly(oak_live_post, BROWN, 2.4))
    els.append(poly(willow_pts, PURPLE, 2.5, "2,4"))
    els.append(poly(ginkgo_pts, ORANGE, 2.8))

    # 曲线原位文字标签（与线条错开无碰撞）
    els.append(txt(312, 143, "④ 松树/柏树（保绿约80%，仅退老针）", 10.2, GREEN, "middle", weight="700", halo=True))
    els.append(txt(332, 176, "③ 栎树/山毛榉（枯叶宿存挂满整冬）", 10.2, BROWN, "middle", weight="700", halo=True))
    els.append(txt(264, 244, "② 垂柳/法桐（拖延2个月）", 10.2, PURPLE, "start", weight="700", halo=True))
    els.append(txt(162, 286, "① 银杏/白蜡（霜后48h清零！）", 10.2, ORANGE, "start", weight="700", halo=True))

    els.append(txt(36, 360, "注：虚线段（③ 栎树 11–4 月）表示叶片已枯黄死亡停止光合，但叶柄未断裂仍挂在枝头；", 10.0, MUTED))
    els.append(txt(36, 376, "南方常绿阔叶树（如香樟）则在 4–5 月新叶展齐时集中换掉旧叶，出现短暂“暮春落叶雨”。", 10.0, MUTED))

    # 右侧四派速读卡 card(536, 62, 204, 326)
    els.append(card(536, 62, 204, 326))
    els.append(txt(548, 84, "四大门派代表树种", 12.5, INK, weight="700"))

    cards_info = [
        (96, "① 闪电清仓派（1–2天）", "银杏、白蜡、核桃、楸树", "全树同步备好离层，等初霜冰晶一劈，24–48h 下起黄金叶雨", ORANGE, ORANGE_SOFT),
        (167, "② 慢性拖延派（1–3个月）", "垂柳、枫香、法桐、女贞", "散孔细管耐轻霜，由内向外分批退场；路灯下还会“熬夜留绿”", PURPLE, PURPLE_SOFT),
        (238, "③ 枯而不落派（宿存整冬）", "蒙古栎/橡树、山毛榉、鹅耳枥", "严寒提前冻停离层酶，留满树干叶当“防鹿啃芽盾”，开春才掉", BROWN, BROWN_SOFT),
        (309, "④ 四季铁甲派（2–5年轮换）", "油松、红松、侧柏、圆柏", "细管胞防冻栓 + 蜡质针叶，并非不掉叶，而是3–5岁老叶错峰退伍", GREEN, GREEN_SOFT),
    ]
    for cy, ct, cs, cd, fg, bg in cards_info:
        els.append(card(546, cy, 184, 65, rx=7, fill=bg, stroke=fg, sw=1.1))
        els.append(txt(554, cy + 16, ct, 10.5, fg, weight="700"))
        els.append(txt(554, cy + 31, cs, 10.0, INK, weight="600"))
        els.append(txt(554, cy + 46, cd[:15], 9.6, BODY))
        els.append(txt(554, cy + 59, cd[15:], 9.6, BODY))

    return figure(
        h,
        "秋冬到次年春季四类树木挂叶比例时间曲线与代表树种",
        "对比银杏白蜡初霜后24至48小时同步暴落、垂柳数周渐次缓落、栎树山毛榉枯而不落宿存整冬以及松柏常绿轮休四条曲线。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 2：叶柄基部“离层三档变速箱”：快掉 vs 慢掉 vs 枯而不落
# ---------------------------------------------------------------------------
def build_abscission_three_gears() -> str:
    h = 402
    els: list[str] = []
    els.extend(
        header(
            "同样长着叶柄“离层剪刀”，为什么银杏一夜秃、垂柳慢慢掉、橡树枯一冬？",
            "秘密全在叶柄根部几层细胞厚的离层区（AZ）：激素退潮节奏、果胶酶进度与霜冻物理劈裂的三档组合",
        )
    )

    cols = [
        (
            20,
            "快档：全冠预装 + 初霜冰劈",
            "代表：银杏、白蜡树（环孔大导管/复叶）",
            ORANGE,
            ORANGE_SOFT,
        ),
        (
            268,
            "慢档：由内向外分批拉闸",
            "代表：垂柳、槭树 + 城市路灯“钉子枝”",
            PURPLE,
            PURPLE_SOFT,
        ),
        (
            516,
            "卡档：低温锁死酶 + 维管硬拽",
            "代表：栎树（橡树）、山毛榉、鹅耳枥",
            BROWN,
            BROWN_SOFT,
        ),
    ]
    for cx, title, sub, fg, bg in cols:
        els.append(card(cx, 64, 224, 320))
        els.append(pill(cx + 10, 74, title, fg, bg, w=204, h=22, size=11))
        els.append(txt(cx + 12, 111, sub, 10.0, MUTED, weight="600"))

    # --- 第 1 栏图示：银杏同步离层 + 冰晶膨胀瞬断 (x=20..244) ---
    els.append(card(32, 122, 200, 120, rx=8, fill="#fffdf7", stroke=BORDER))
    # 树枝竖干
    els.append('<rect x="44" y="132" width="22" height="100" rx="4" fill="#92400e"/>')
    els.append(txt(55, 224, "枝干", 9.8, "#ffffff", "middle", weight="700"))
    # 木栓保护疤（已焊好）
    els.append(f'<rect x="66" y="156" width="8" height="24" rx="2" fill="{BROWN}"/>')
    # 酶软化的离层带 + 蓝色冰晶楔子
    els.append(f'<rect x="75" y="154" width="10" height="28" rx="2" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="2,2"/>')
    els.append(f'<polygon points="80,152 84,168 80,184 76,168" fill="#60a5fa" stroke="{BLUE}" stroke-width="1"/>')
    # 即将脱落的金黄扇形银杏叶柄+叶片
    els.append('<path d="M 88 168 L 128 166 C 148 140, 188 136, 198 158 L 182 168 L 198 180 C 186 200, 148 196, 128 172 Z" fill="#facc15" stroke="#ca8a04" stroke-width="1.5"/>')
    els.append(txt(79, 145, "冰晶撑裂离层", 9.8, BLUE, "middle", weight="700"))
    els.append(txt(154, 212, "日出融冰 → 全树齐落", 9.8, ORANGE, "middle", weight="700"))

    g1_lines = [
        ("① 全树同步待命：", "短日照让全冠叶柄同时", INK),
        ("", "焊好软木疤、果胶酶半溶中胶层；", BODY),
        ("② 暂留黄叶收氮：", "无霜时靠细维管挂住叶；", BODY),
        ("③ 初霜总开关：", "夜冻让离层水结冰胀 9%，", ORANGE),
        ("", "日出冰化，24–48h 哗啦掉光！", ORANGE),
    ]
    y_cur = 260
    for b_txt, n_txt, col in g1_lines:
        line_str = f"{b_txt}{n_txt}"
        els.append(txt(32, y_cur, line_str, 9.8, col, weight="700" if b_txt and col == ORANGE else ("600" if b_txt else None)))
        y_cur += 22

    # --- 第 2 栏图示：垂柳与路灯微气候异步梯度 (x=268..492) ---
    els.append(card(280, 122, 200, 120, rx=8, fill="#faf8ff", stroke=BORDER))
    # 树冠内外+路灯示意
    els.append('<line x1="305" y1="228" x2="305" y2="146" stroke="#78350f" stroke-width="5" stroke-linecap="round"/>')
    els.append('<line x1="305" y1="176" x2="365" y2="148" stroke="#78350f" stroke-width="3"/>')
    els.append('<line x1="305" y1="190" x2="392" y2="184" stroke="#78350f" stroke-width="3"/>')
    # 内膛黄落叶（早掉）
    els.append('<ellipse cx="322" cy="198" rx="10" ry="5" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>')
    els.append(txt(326, 216, "内膛老叶先掉", 9.6, AMBER, "middle", weight="700"))
    # 外梢绿叶（晚掉）
    els.append(f'<ellipse cx="386" cy="182" rx="12" ry="5.5" fill="#4ade80" stroke="{GREEN}" stroke-width="1.2"/>')
    els.append(f'<ellipse cx="364" cy="148" rx="12" ry="5.5" fill="#22c55e" stroke="{GREEN}" stroke-width="1.2"/>')
    # 路灯暖光锥
    els.append('<line x1="446" y1="230" x2="446" y2="140" stroke="#475569" stroke-width="3"/>')
    els.append('<path d="M 446 140 L 424 140" stroke="#475569" stroke-width="3"/>')
    els.append('<polygon points="424,142 382,196 458,196" fill="#fef08a" opacity="0.45"/>')
    els.append('<circle cx="424" cy="142" r="5" fill="#f59e0b"/>')
    els.append(txt(422, 214, "路灯骗过光敏色素", 9.6, PURPLE, "middle", weight="700"))

    g2_lines = [
        ("① 散孔细管耐寒：", "垂柳导管细（30–50 μm）", INK),
        ("", "不怕轻霜，水足可贪恋晚秋阳光；", BODY),
        ("② 树冠分批撤退：", "遮阴内膛老叶先跌先掉，", BODY),
        ("", "向阳外梢叶多赚几周糖分再退；", BODY),
        ("③ 路灯“熬夜枝”：", "夜光谎报长日照拒落叶！", PURPLE),
    ]
    y_cur = 260
    for b_txt, n_txt, col in g2_lines:
        els.append(txt(280, y_cur, f"{b_txt}{n_txt}", 9.8, col, weight="700" if col == PURPLE else ("600" if b_txt else None)))
        y_cur += 22

    # --- 第 3 栏图示：橡树/山毛榉枯而不落 Marcescence (x=516..740) ---
    els.append(card(528, 122, 200, 120, rx=8, fill="#fffbeb", stroke=BORDER))
    # 枝干 + 越冬嫩芽 + 未断开的木质化纤维束拽着枯褐橡树叶
    els.append('<rect x="542" y="132" width="20" height="100" rx="4" fill="#57534e"/>')
    # 腋窝饱满越冬冬芽（受枯叶保护）
    els.append(f'<path d="M 562 162 C 574 146, 584 148, 578 166 Z" fill="#16a34a" stroke="{GREEN}" stroke-width="1.3"/>')
    els.append(txt(596, 146, "越冬嫩芽（受护）", 9.6, GREEN, weight="700"))
    # 未溶断的离层厚壁纤维桥
    els.append(f'<rect x="562" y="172" width="18" height="8" rx="2" fill="{RED_SOFT}" stroke="{RED}" stroke-width="1.3"/>')
    els.append(f'<line x1="560" y1="176" x2="584" y2="176" stroke="{BROWN}" stroke-width="2.6"/>')
    # 波浪缘枯褐橡树叶
    els.append(
        '<path d="M 582 176 C 598 160, 616 168, 630 160 C 646 156, 662 168, 682 164 '
        'C 700 168, 704 186, 684 190 C 664 196, 646 188, 630 194 C 612 190, 598 192, 582 176 Z" '
        'fill="#b45309" fill-opacity="0.82" stroke="#78350f" stroke-width="1.5"/>'
    )
    els.append(txt(640, 180, "苦涩单宁干枯叶", 9.6, "#ffffff", "middle", weight="700"))
    els.append(txt(628, 214, "离层酶冻停，纤维死拽不放！", 9.6, RED, "middle", weight="700"))

    g3_lines = [
        ("① 离层半途急冻：", "深秋降温快，果胶酶未溶", INK),
        ("", "完分离层就冻停，纤维硬拽着；", BODY),
        ("② 防鹿啃芽盾牌：", "多见于幼树与 1–2 m 低枝，", BROWN),
        ("", "苦涩干叶劝退鹿和狍子啃冬芽；", BODY),
        ("③ 春芽顶落化泥：", "4 月新芽膨大顶落旧叶肥土！", GREEN),
    ]
    y_cur = 260
    for b_txt, n_txt, col in g3_lines:
        els.append(txt(528, y_cur, f"{b_txt}{n_txt}", 9.8, col, weight="700" if col in (BROWN, GREEN) else ("600" if b_txt else None)))
        y_cur += 22

    return figure(
        h,
        "叶柄离层三档变速箱：银杏闪电暴落、垂柳分批缓落与橡树枯而不落解剖对比",
        "对比银杏全冠同步预装离层加初霜冰晶劈裂、垂柳散孔材与路灯微气候渐次落叶、橡树山毛榉离层酶冻停保留宿存枯叶护冬芽三种机制。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 3（单次动画）：为什么阔叶树不扔叶子会死？宽导管冻融气栓 vs 松柏细管胞与纹孔塞安全阀
# ---------------------------------------------------------------------------
def build_xylem_bubble_valve_anim() -> str:
    h = 412
    extra_css = """
    @keyframes ice-freeze {
      0%, 12% { opacity: 0; }
      24%, 52% { opacity: 0.88; }
      66%, 100% { opacity: 0; }
    }
    @keyframes big-embolism {
      0%, 20% { transform: scale(0.18); opacity: 0; }
      35%, 55% { transform: scale(0.45); opacity: 0.95; }
      74%, 100% { transform: scale(1); opacity: 0.96; }
    }
    @keyframes tiny-bubble-vanish {
      0%, 20% { opacity: 0; }
      35%, 56% { opacity: 0.95; }
      74%, 100% { opacity: 0.08; }
    }
    @keyframes torus-slam {
      0%, 54% { transform: translateX(0px); }
      72%, 100% { transform: translateX(13px); }
    }
    .ice-sheath {
      animation: ice-freeze 5.6s ease-in-out 1 backwards;
    }
    .embolism-lock {
      transform-box: fill-box;
      transform-origin: center;
      animation: big-embolism 5.6s ease-out 1 backwards;
    }
    .micro-bubble {
      animation: tiny-bubble-vanish 5.6s ease-in-out 1 backwards;
    }
    .torus-disc {
      animation: torus-slam 5.6s cubic-bezier(0.22, 1, 0.36, 1) 1 backwards;
    }
    @media (prefers-reduced-motion: reduce) {
      .ice-sheath { animation: none !important; opacity: 0 !important; }
      .embolism-lock { animation: none !important; transform: scale(1) !important; opacity: 0.96 !important; }
      .micro-bubble { animation: none !important; opacity: 0.08 !important; }
      .torus-disc { animation: none !important; transform: translateX(13px) !important; }
    }
    """
    els: list[str] = []
    els.extend(
        header(
            "为什么阔叶树冬天硬撑不掉叶会死？35–44 微米“冻融气栓生死线”",
            "水结冰会挤出溶解空气！宽导管融冰时气泡在负压下炸成“气锁断流”，松柏细管胞却能把微气泡压回水里",
        )
    )

    # 左栏：阔叶树宽导管 (D = 120 um > 44 um 临界值) card(20, 64, 352, 330)
    els.append(card(20, 64, 352, 330))
    els.append(pill(32, 74, "阔叶树宽导管（内径 60–250 μm）：夏天飙车，冬天爆管！", RED, RED_SOFT, w=328, h=22, size=10.8))

    # 宽导管纵剖图框 (x=34..358, y=106..268)
    els.append(card(34, 106, 324, 162, rx=8, fill="#f8fafc", stroke=BORDER))
    # 导管木质化厚壁 (x=96..256, 宽 160 px 示意 120 um 大口径导管)
    els.append('<rect x="96" y="118" width="160" height="138" rx="6" fill="#dbeafe" stroke="#334155" stroke-width="4"/>')
    # 结冰期向心冰壳（动画阶段 1：结冰挤出空气）
    els.append('<rect class="ice-sheath" x="100" y="122" width="38" height="130" fill="#bae6fd"/>')
    els.append('<rect class="ice-sheath" x="214" y="122" width="38" height="130" fill="#bae6fd"/>')
    # 融冰后负压膨胀填满整根宽导管的致命气栓（终态停留在气栓断流态）
    els.append(
        f'<rect class="embolism-lock" x="104" y="128" width="144" height="118" rx="22" '
        f'fill="{RED_SOFT}" stroke="{RED}" stroke-width="2.4" stroke-dasharray="6,3"/>'
    )
    els.append(txt(176, 174, "致命大气泡栓塞！", 11.5, RED, "middle", weight="700"))
    els.append(txt(176, 194, "气泡 > 0.58 μm 临界值（拉普拉斯）", 10.2, RED, "middle", weight="600"))
    els.append(txt(176, 214, "融冰遇 -0.5 MPa 拉力", 10.0, BODY, "middle"))
    els.append(txt(176, 232, "水柱当场崩断 = 0% 输水", 10.2, RED, "middle", weight="700"))

    # 尺寸标注与阔叶蒸腾拉拽说明
    els.append(txt(42, 145, "宽导管", 10.2, INK, weight="700"))
    els.append(txt(42, 162, "120 μm", 10.5, RED, weight="700"))
    els.append(txt(42, 180, "(>44 μm", 9.8, MUTED))
    els.append(txt(42, 194, "生死线)", 9.8, MUTED))
    els.append(txt(260, 152, "若冬天不扔阔叶：", 9.8, INK, weight="700"))
    els.append(txt(260, 170, "• 叶面抽水拉高负压", 9.5, BODY))
    els.append(txt(260, 187, "• 夜冻+日晒融冰", 9.5, BODY))
    els.append(txt(260, 204, "  血管气锁渴死！", 9.5, RED, weight="700"))
    els.append(txt(260, 224, "• 湿雪挂叶压断树枝", 9.5, BODY))

    # 左下：哈根-泊肃叶四次方定律收益账
    els.append(card(34, 278, 324, 104, rx=8, fill=ORANGE_SOFT, stroke=ORANGE))
    els.append(txt(46, 298, "既然宽管怕冻，干嘛不造细管？—— 四次方流量暴利！", 10.0, ORANGE, weight="700"))
    els.append(txt(46, 319, "• 哈根–泊肃叶定律：单管输水流量 Q ∝ 管径 D⁴", 10.0, INK, weight="600"))
    els.append(txt(46, 338, "• 管径扩宽 5 倍 (20→100 μm)，流量暴涨 5⁴ = 625 倍！", 10.0, RED, weight="700"))
    els.append(txt(46, 357, "• 春夏靠宽管飙车疯长，入冬扔光薄叶“弃车保帅”最赚", 9.8, BODY))
    els.append(txt(46, 374, "• 反证：落羽杉虽是针叶，管胞宽达 40 μm → 秋天照样掉叶", 9.5, AMBER, weight="700"))

    # 右栏：松柏细管胞 (D = 18 um < 35 um) + 具缘纹孔塞 (Torus-margo) 止回阀 card(388, 64, 352, 330)
    els.append(card(388, 64, 352, 330))
    els.append(pill(400, 74, "松柏细管胞（内径 10–30 μm）+ 纹孔塞自动止回阀", GREEN, GREEN_SOFT, w=328, h=22, size=10.8))

    # 右上：细管胞微气泡自动消融 (x=402..726, y=106..226)
    els.append(card(402, 106, 324, 120, rx=8, fill="#f0fdf4", stroke=GREEN))
    # 三根并排细管胞示意（每根宽 28 px 对比左侧 160 px！）
    for tx in (424, 464, 504):
        els.append(f'<rect x="{tx}" y="118" width="28" height="96" rx="5" fill="#dcfce7" stroke="{GREEN}" stroke-width="2.4"/>')
        els.append(f'<line x1="{tx + 14}" y1="206" x2="{tx + 14}" y2="128" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')
        # 结冰析出的极微小气泡（融冰后因表面张力 4*sigma/Db 极高而迅速压扁溶回水里！）
        els.append(f'<circle class="micro-bubble" cx="{tx + 14}" cy="166" r="4.5" fill="#ffffff" stroke="{RED}" stroke-width="1.3"/>')

    els.append(txt(546, 132, "① 管径极细（松≤30 / 柏≤20 μm）", 9.8, GREEN, weight="700"))
    els.append(txt(546, 151, "单根冰量少，析出微气泡极小；", 9.6, BODY))
    els.append(txt(546, 170, "② 表面张力自愈（P = 4σ/D_b）：", 9.8, BLUE, weight="700"))
    els.append(txt(546, 189, "气泡越小内部表面张力越强，", 9.6, BODY))
    els.append(txt(546, 207, "冰一化直接把空气挤溶回水里！", 9.6, GREEN, weight="700"))

    # 右下：具缘纹孔（Torus-margo）单向安全阀放大镜 (x=402..726, y=236..382)
    els.append(card(402, 236, 324, 146, rx=8, fill=BLUE_SOFT, stroke=BLUE))
    els.append(txt(414, 256, "双保险：万一单根管胞进气，具缘纹孔塞（Torus）秒封死！", 10.3, BLUE, weight="700"))

    # 纹孔腔放大解剖框 (x=414..552, y=268..370)
    els.append('<rect x="414" y="268" width="138" height="102" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.2"/>')
    # 左腔：受损进气管胞（0 MPa 大气压）
    els.append(f'<rect x="418" y="272" width="52" height="94" rx="4" fill="{RED_SOFT}"/>')
    els.append(txt(444, 300, "进气废管", 9.5, RED, "middle", weight="700"))
    els.append(txt(444, 316, "(0 MPa)", 9.2, RED, "middle"))
    # 右腔：正常负压输水管胞（-2 MPa 吸力）
    els.append('<rect x="496" y="272" width="52" height="94" rx="4" fill="#dbeafe"/>')
    els.append(txt(522, 300, "健康水管", 9.5, BLUE, "middle", weight="700"))
    els.append(txt(522, 316, "(-2 MPa)", 9.2, BLUE, "middle"))
    # 上下拱形具缘纹孔壁（留出中央纹孔口 y=310..328, x=492）
    els.append('<path d="M 470 272 L 470 308 L 494 308 L 494 272 Z" fill="#475569"/>')
    els.append('<path d="M 470 366 L 470 330 L 494 330 L 494 366 Z" fill="#475569"/>')
    # 弹性纹孔缘（Margo 纤丝）+ 实心纹孔塞（Torus 圆盘：动画向右平移 13px 死死拍在 x=495 纹孔口上！）
    els.append('<g class="torus-disc">')
    els.append(f'<line x1="482" y1="276" x2="482" y2="362" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="3,2"/>')
    els.append(f'<ellipse cx="482" cy="319" rx="4.5" ry="15" fill="{ORANGE}" stroke="#7c2d12" stroke-width="1.4"/>')
    els.append("</g>")
    els.append(txt(483, 358, "纹孔塞封门→", 9.2, ORANGE, "middle", weight="700"))

    # 右侧文字解释纹孔塞动作
    els.append(txt(562, 286, "• 平时居中：水流穿过网状纹孔缘", 9.8, BODY))
    els.append(txt(562, 306, "• 一旦隔壁进气：两侧瞬间产生", 9.8, BODY))
    els.append(txt(562, 324, "  巨大压差，把实心圆盘“纹孔塞”", 9.8, INK, weight="600"))
    els.append(txt(562, 342, "  啪地吸过去死死堵住孔口！", 9.8, ORANGE, weight="700"))
    els.append(txt(562, 363, "• 气泡被永久关禁闭，绝不连累全树", 9.8, GREEN, weight="700"))

    return figure(
        h,
        "阔叶树宽导管冻融气泡栓塞与松柏细管胞及纹孔塞安全阀单次动画对比",
        "单次播放5.6秒冻融过程：左栏120微米宽导管结冰析出大气泡并在融冰负压下膨胀成气栓断流；右栏18微米细管胞微气泡自动消融，且具缘纹孔塞平移封死进气管胞。",
        els,
        extra_css=extra_css,
    )


# ---------------------------------------------------------------------------
# 图 4：松树与柏树零下 30℃ 不掉叶的“四重抗冻黑科技”解剖图
# ---------------------------------------------------------------------------
def build_conifer_four_shields() -> str:
    h = 404
    els: list[str] = []
    els.extend(
        header(
            "零下 30 ℃ 寒风刺骨，松树和柏树凭什么敢挂着绿叶硬扛整个冬天？",
            "从蜡质微缩针叶、防爆管胞、细胞“糖液玻璃化”到类囊体拆垛散热——缺一不可的四重越冬装甲",
        )
    )

    # 中央松针横截面主图卡 card(236, 64, 288, 322) + 左右四块盾牌分卡
    els.append(card(236, 64, 288, 322, fill="#f8fafc", stroke=GREEN, sw=1.4))
    els.append(pill(260, 74, "松针横截面显微装甲（半圆扇形结构示意）", GREEN, GREEN_SOFT, w=240, h=22, size=10.8))

    # 绘制半圆形松针横截面 (中心 380, 218)
    # 1) 最外圈：超厚角质层 + 厚壁下皮层
    els.append(
        f'<path d="M 272 246 C 272 132, 488 132, 488 246 Z" '
        f'fill="#dcfce7" stroke="{GREEN}" stroke-width="5"/>'
    )
    # 蜡质外环光晕
    els.append(
        '<path d="M 267 249 C 267 125, 493 125, 493 249 Z" '
        'fill="none" stroke="#eab308" stroke-width="2.5" stroke-dasharray="5,3"/>'
    )
    # 下陷气孔窝（Sunken stomata）3 处凹槽 + 蜡质塞
    for sx, sy in [(298, 180), (380, 150), (462, 180)]:
        els.append(f'<circle cx="{sx}" cy="{sy}" r="7" fill="#ffffff" stroke="{TEAL}" stroke-width="1.8"/>')
        els.append(f'<circle cx="{sx}" cy="{sy}" r="2.8" fill="#eab308"/>')
    # 褶皱叶肉树脂道（两侧抗冻树脂管）
    for rx_c in (312, 448):
        els.append(f'<circle cx="{rx_c}" cy="218" r="11" fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="1.6"/>')
        els.append(txt(rx_c, 222, "树脂", 8.8, AMBER, "middle", weight="700"))
    # 中央内皮层与细管胞维管束
    els.append(f'<ellipse cx="380" cy="218" rx="42" ry="26" fill="#ffffff" stroke="{BLUE}" stroke-width="2"/>')
    els.append(f'<rect x="358" y="205" width="44" height="12" rx="3" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.2"/>')
    els.append(f'<rect x="358" y="220" width="44" height="11" rx="3" fill="{ORANGE_SOFT}" stroke="{ORANGE}" stroke-width="1.2"/>')
    els.append(txt(380, 214, "细管胞水路", 8.8, BLUE, "middle", weight="700"))
    els.append(txt(380, 229, "韧皮部糖路", 8.8, ORANGE, "middle", weight="700"))

    els.append(txt(380, 128, "黄色虚线：超厚疏水角质蜡质层 + 下陷气孔窝", 9.8, AMBER, "middle", weight="700"))
    els.append(txt(380, 272, "为什么圆滑细针不怕暴雪压枝？", 10.5, INK, "middle", weight="700"))
    els.append(txt(380, 291, "• 针叶窄滑柔韧，积雪到一定重量自动滑落；", 9.8, BODY, "middle"))
    els.append(txt(380, 309, "• 柏树则把叶片缩成紧贴枝条的细小“鳞叶”，", 9.8, BODY, "middle"))
    els.append(txt(380, 327, "  迎风面积与失水率比阔叶再降一个数量级！", 9.8, GREEN, "middle", weight="700"))
    els.append(card(250, 340, 260, 36, rx=6, fill=AMBER_SOFT, stroke=AMBER))
    els.append(txt(380, 362, "冷知识：侧柏冬天变紫褐色不是死，是防晒护目镜！", 9.6, AMBER, "middle", weight="700"))

    # 左上盾牌 ①：微缩蜡质装甲与下陷气孔 card(20, 64, 204, 154)
    els.append(card(20, 64, 204, 154))
    els.append(pill(30, 74, "① 针叶/鳞叶锁水装甲", TEAL, TEAL_SOFT, w=184, h=22, size=10.8))
    s1 = [
        "• 表面积/体积比极小，大幅压缩",
        "  冬季干冷寒风的蒸发窗口；",
        "• 表皮外覆厚蜡质角质层，气孔",
        "  深藏在凹窝里并塞满蜡丝；",
        "• 冬季气孔紧闭，蒸腾失水率仅",
        "  为同面积阔叶的几十分之一！",
    ]
    for i, line in enumerate(s1):
        els.append(txt(30, 114 + i * 17, line, 9.8, GREEN if i == 5 else BODY, weight="700" if i == 5 else None))

    # 左下盾牌 ②：细管胞 + 纹孔塞防栓水路 card(20, 232, 204, 154)
    els.append(card(20, 232, 204, 154))
    els.append(pill(30, 242, "② 微米级防冻爆管胞", BLUE, BLUE_SOFT, w=184, h=22, size=10.8))
    s2 = [
        "• 放弃高流量宽导管，全树采用",
        "  内径 10–30 μm 短细管胞；",
        "• 严守 <35 μm 冻融气栓红线，",
        "  反复结冰融化水柱也不断流；",
        "• 具缘纹孔塞充当百万个微型",
        "  止回阀，把局部气泡锁死隔离。",
    ]
    for i, line in enumerate(s2):
        els.append(txt(30, 282 + i * 17, line, 9.8, BLUE if i == 2 else BODY, weight="700" if i == 2 else None))

    # 右上盾牌 ③：胞内可溶性糖“玻璃化”防冻液 card(536, 64, 204, 154)
    els.append(card(536, 64, 204, 154))
    els.append(pill(546, 74, "③ 细胞“糖液玻璃化”防冻", PURPLE, PURPLE_SOFT, w=184, h=22, size=10.8))
    s3 = [
        "• 入秋淀粉酶把淀粉拆成高浓度",
        "  蔗糖、棉子糖与脯氨酸；",
        "• 严寒时主动把水排到细胞间隙",
        "  结冰，胞内浓缩成黏稠“玻璃态”；",
        "• 绝不结出刺破细胞膜的锋利冰晶，",
        "  针叶耐寒极限达 -28 至 -60 ℃！",
    ]
    for i, line in enumerate(s3):
        els.append(txt(546, 114 + i * 17, line, 9.8, PURPLE if i == 5 else BODY, weight="700" if i == 5 else None))

    # 右下盾牌 ④：类囊体拆垛与持续热耗散 card(536, 232, 204, 154)
    els.append(card(536, 232, 204, 154))
    els.append(pill(546, 242, "④ 叶绿体“拆垛短路散热”", ORANGE, ORANGE_SOFT, w=184, h=22, size=10.8))
    s4 = [
        "• 冬日大晴天最凶险：叶绿素照常",
        "  吸光，但暗反应酶冻僵停工！",
        "• 松针把类囊体基粒“拆垛”混排，",
        "  让 PSII 把过剩光能直接导给 PSI；",
        "• 配合玉米黄质把光能安全化成热",
        "  散掉（Nat. Commun. 2020 实测）！",
    ]
    for i, line in enumerate(s4):
        els.append(txt(546, 282 + i * 17, line, 9.8, ORANGE if i in (3, 4) else BODY, weight="700" if i in (3, 4) else None))

    return figure(
        h,
        "松树与柏树严冬不落叶的四重抗冻生理装甲解剖图",
        "展示松针横截面蜡质层与下陷气孔、细管胞防冻栓水路、细胞内可溶性糖玻璃化防冰晶刺穿以及冬季叶绿体类囊体拆垛直接能量转移热耗散。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 5：叶经济谱（Leaf Economics Spectrum）与“常绿树其实天天在换叶”真相账本
# ---------------------------------------------------------------------------
def build_leaf_economics_spectrum() -> str:
    h = 398
    els: list[str] = []
    els.extend(
        header(
            "终极算账：为什么阔叶树偏爱“半年抛快消叶”，松柏却造“三年耐用品”？",
            "全球植物叶经济谱（Wright 等 Nature）：比叶重（造价）越高，单日回本越慢，就越必须跨冬连用好几年！",
        )
    )

    # 左栏：叶经济谱散点/区间带图 card(20, 64, 412, 316)
    els.append(card(20, 64, 412, 316))
    els.append(pill(34, 74, "叶片单平米干重造价（LMA）vs 叶片服役寿命", BLUE, BLUE_SOFT, w=320, h=22, size=10.8))

    # 坐标区 x: 84..406 (宽 322), y: 116..314 (高 198)
    ax_x0, ax_x1, ax_y0, ax_y1 = 84.0, 406.0, 314.0, 116.0
    els.append(f'<line x1="{ax_x0}" y1="{ax_y0}" x2="{ax_x1}" y2="{ax_y0}" stroke="{SLATE}" stroke-width="1.4"/>')
    els.append(f'<line x1="{ax_x0}" y1="{ax_y0}" x2="{ax_x0}" y2="{ax_y1}" stroke="{SLATE}" stroke-width="1.4"/>')

    # X 轴：比叶重 LMA (0 -> 360 g/m^2)
    for lma in (0, 90, 180, 270, 360):
        lx = ax_x0 + (lma / 360.0) * (ax_x1 - ax_x0)
        els.append(f'<line x1="{lx:.1f}" y1="{ax_y0}" x2="{lx:.1f}" y2="{ax_y0 + 5}" stroke="{SLATE}" stroke-width="1.1"/>')
        els.append(f'<line x1="{lx:.1f}" y1="{ax_y0}" x2="{lx:.1f}" y2="{ax_y1}" stroke="{HAIRLINE}" stroke-width="0.9" stroke-dasharray="3,3"/>')
        els.append(txt(lx, ax_y0 + 18, f"{lma}", 10.0, MUTED, "middle"))
    els.append(txt((ax_x0 + ax_x1) / 2, ax_y0 + 36, "叶片建造成本：比叶重 LMA（g 干重 / m² 叶面积）→ 越右越厚重昂贵", 10.0, INK, "middle", weight="600"))

    # Y 轴：叶片寿命（对数视觉分档：4个月、1年、2.5年、5年+）
    y_ticks = [
        (292, "5–7个月"),
        (242, "1–1.5年"),
        (184, "2–5年"),
        (132, "10–45年"),
    ]
    for ty, tl in y_ticks:
        els.append(f'<line x1="{ax_x0 - 4}" y1="{ty}" x2="{ax_x1}" y2="{ty}" stroke="{HAIRLINE}" stroke-width="0.9" stroke-dasharray="3,3"/>')
        els.append(txt(ax_x0 - 8, ty + 4, tl, 9.8, MUTED, "end"))
    els.append(txt(34, 112, "↑ 叶片寿命", 10.0, INK, weight="700"))

    # 对角趋势走廊带
    els.append(
        '<polygon points="104,302 156,302 396,146 340,126" '
        f'fill="{BLUE_SOFT}" opacity="0.65"/>'
    )

    # 四个代表生态群落圆点
    groups = [
        (138, 288, 13, ORANGE, "① 温带落叶阔叶", "银杏/杨/枫/白蜡 (LMA 45–80)"),
        (178, 282, 10, AMBER, "落叶松/水杉", "薄针叶一年一换 (LMA ~95)"),
        (206, 238, 12, TEAL, "② 南方常绿阔叶", "香樟/桂花/冬青 (暮春换叶)"),
        (296, 180, 14, GREEN, "③ 北方常绿松柏", "油松/红松/侧柏 (LMA 200–320)"),
        (366, 134, 10, PURPLE, "④ 高山狐尾松", "单针可活 30–45 年！"),
    ]
    for gx, gy, gr, gc, gl1, gl2 in groups:
        els.append(f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="{gc}" fill-opacity="0.22" stroke="{gc}" stroke-width="2.2"/>')
        els.append(f'<circle cx="{gx}" cy="{gy}" r="3.5" fill="{gc}"/>')

    els.append(txt(154, 266, "① 落叶阔叶（薄叶高光合，单季回本）", 9.8, ORANGE, weight="700", halo=True))
    els.append(txt(192, 298, "★叛逆彩蛋：落叶松/水杉（薄针叶秋落）", 9.5, AMBER, weight="700", halo=True))
    els.append(txt(222, 234, "② 香樟/冬青（1年1换）", 9.8, TEAL, weight="700", halo=True))
    els.append(txt(234, 162, "③ 松树/柏树（厚针叶连用2–5年回本）", 9.8, GREEN, weight="700", halo=True))
    els.append(txt(244, 132, "④ 狐尾松（极寒贫瘠，寿命30–45年）", 9.6, PURPLE, weight="700", halo=True))

    els.append(txt(36, 369, "规律：暖湿肥沃区 → 薄叶快赚快扔占优；干冷贫瘠区 → 厚针叶跨冬连用占优。", 9.6, MUTED))

    # 右栏：戳破“常绿树一辈子不掉叶”误区 + 三大特殊树种答疑 card(444, 64, 296, 316)
    els.append(card(444, 64, 296, 316))
    els.append(pill(456, 74, "破除误区：常绿树不是不掉叶，是“错峰轮休”！", GREEN, GREEN_SOFT, w=272, h=22, size=10.6))

    # 松树枝条三年叶龄示意图框 (x=456..728, y=104..206)
    els.append(card(456, 104, 272, 102, rx=8, fill="#f8fafc", stroke=BORDER))
    # 横向松枝分三段叶龄
    els.append('<line x1="472" y1="158" x2="706" y2="158" stroke="#78350f" stroke-width="5" stroke-linecap="round"/>')
    els.append('<line x1="550" y1="146" x2="550" y2="170" stroke="#475569" stroke-width="2"/>')
    els.append('<line x1="630" y1="146" x2="630" y2="170" stroke="#475569" stroke-width="2"/>')
    # 左段（3–4岁老松针，泛黄脱落！）
    for nx in (484, 502, 520, 536):
        els.append(f'<line x1="{nx}" y1="156" x2="{nx - 8}" y2="126" stroke="#eab308" stroke-width="2"/>')
        els.append(f'<line x1="{nx}" y1="160" x2="{nx - 6}" y2="188" stroke="#ca8a04" stroke-width="2" stroke-dasharray="4,2"/>')
    els.append(txt(506, 120, "3–4岁老针(秋落)", 9.2, AMBER, "middle", weight="700"))
    # 中段（2岁壮年松针，深绿留守）
    for nx in (564, 582, 600, 616):
        els.append(f'<line x1="{nx}" y1="156" x2="{nx + 4}" y2="124" stroke="{GREEN}" stroke-width="2.2"/>')
        els.append(f'<line x1="{nx}" y1="160" x2="{nx + 4}" y2="188" stroke="{GREEN}" stroke-width="2.2"/>')
    els.append(txt(590, 120, "2岁壮年针(留守)", 9.2, GREEN, "middle", weight="700"))
    # 右段（1岁新生松针，翠绿当家）
    for nx in (644, 662, 680, 696):
        els.append(f'<line x1="{nx}" y1="156" x2="{nx + 10}" y2="126" stroke="#16a34a" stroke-width="2.2"/>')
        els.append(f'<line x1="{nx}" y1="160" x2="{nx + 10}" y2="188" stroke="#16a34a" stroke-width="2.2"/>')
    els.append(txt(676, 120, "1岁新针(主力)", 9.2, "#15803d", "middle", weight="700"))
    els.append(txt(592, 200, "松林地上厚厚一层松针毯，就是每年退休的老员工！", 9.5, BODY, "middle", weight="600"))

    # 右下三条高频疑问速答
    qa = [
        (216, "问1：香樟树冬天绿油油，怎么4月满地掉红黄叶？", "答：亚热带常绿阔叶树选在暮春“新叶上岗日”集中换旧衣！", TEAL),
        (268, "问2：水杉、池杉、落叶松也是针叶，怎么秋天全秃？", "答：水杉/池杉管胞较宽怕冻栓；落叶松在-50℃极寒区干脆造薄针一年一扔！", AMBER),
        (326, "问3：松柏冬天还在做光合作用吗？", "答：0℃以上晴午仍可微弱补碳；严寒冰封期则锁死气孔专心散热保命。", GREEN),
    ]
    for qy, q1, q2, qc in qa:
        els.append(txt(456, qy + 13, q1, 9.8, qc, weight="700"))
        els.append(txt(456, qy + 30, q2[:26], 9.5, BODY))
        if len(q2) > 26:
            els.append(txt(456, qy + 44, q2[26:], 9.5, BODY))

    return figure(
        h,
        "全球植物叶经济谱与松柏错峰轮休换叶机制图解",
        "左栏展示比叶重LMA建造成本与叶片寿命正相关规律，右栏图解松枝1至4年生针叶分批退伍以及香樟暮春换叶、落叶松水杉秋落原因。",
        els,
    )


@register(TOPIC, "秋冬树木落叶快慢、枯而不落与松柏常青四重抗冻机制（5图）", "植物生理·生物物理")
def build() -> list[str]:
    verify_winter_leaf_math()
    files = {
        "four-speed-phenology-timeline.svg": build_four_speed_phenology_timeline(),
        "abscission-three-gears.svg": build_abscission_three_gears(),
        "xylem-bubble-valve-anim.svg": build_xylem_bubble_valve_anim(),
        "conifer-four-shields.svg": build_conifer_four_shields(),
        "leaf-economics-spectrum.svg": build_leaf_economics_spectrum(),
    }
    for name, content in files.items():
        write_svg(TOPIC, name, content)
    return [f"assets/images/{TOPIC}/{name}" for name in files]
