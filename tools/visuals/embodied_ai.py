"""具身智能（GPT-6.2 Astra 指挥机械臂）文章配图生成器。

6 张图：
1. three-paths-overview.svg      三条路径总览：直觉物理 / 仿真地基 / 真机示教，加时间瓶颈
2. ember0-scoreboard.svg         Ember-0 真机榜 19.6%→41.2% 与能力分解（一手数据）
3. sim2real-cad-loop.svg         CAD→物理仿真→策略训练→真机→数字孪生回流闭环
4. icl-knowledge-package.svg     SenseNova 的 ICL 知识包六类内容与 1×/10× 步数预算
5. dual-system-clock.svg         双系统（System 2 慢脑 + System 1 快小脑）+ 世界时钟动画
6. capability-boundaries.svg     四道工程边界（精确接触/柔性/长程/不可逆）与真实数据

所有数值来自已核实的一手来源（OpenAI 公告/系统卡、SenseNova 官方页与 arXiv
2610.22471、XDOF Ember-0 官方博客与排行榜、π0.5 arXiv 2504.16054、NVIDIA
Isaac Sim 官方页），并在 build 时执行断言；比例失真处均在图内标注。
"""

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

SUBDIR = "embodied-ai-three-paths"
RED = "#b34039"  # 本主题专用：失败/边界的警示色（与 algebra_logic 等其他模块一致）

# ---------------------------------------------------------------------------
# 来自一手来源的事实数值（build 时断言）
# ---------------------------------------------------------------------------
SUCCESS_OLD = 19.64  # GPT-6 Astra, Ember-0, XDOF 2026-10 (19.6%)
SUCCESS_NEW = 41.23  # GPT-6.2 Astra, Ember-0, XDOF 2026-11-20 (41.2%)
LATENCY_OLD = 15.01  # GPT-6 Astra 平均决策间隔（秒），XDOF 实测
LATENCY_NEW = 10.16  # GPT-6.2 Astra 平均决策间隔（秒，约 10.2 秒），XDOF 实测
# SenseNova 真机（GPT-6-Astra，8 种机器人平台）分组成功率：分子/分母
REAL_TASKS = [
    ("刚性抓取", 17, 18, BLUE),
    ("柔性物体", 2, 4, ORANGE),
    ("长程移动", 9, 23, PURPLE),
    ("精确插接", 0, 11, RED),
]
# XDOF Ember-0 一手统计与任务对比
DONE_ACCURACY = 57.0   # 模型宣称 done 时任务真完成的比例（早期五模型评测）
TSHIRT_TRIALS, TSHIRT_SUCCESSES = 143, 0
TSHIRT_NEW_NUM, TSHIRT_NEW_DEN = 1, 30
TONG_OLD_SOL = 13.3    # Sol 6.1 用夹子夹面包成功率 (4/30)
TONG_NEW_ASTRA = 90.0  # GPT-6.2 Astra 用夹子夹面包成功率 (27/30)
PLUSH_TASK_SOL = 82.8  # Sol 6.1 拉毛巾取毛绒玩具成功率 (24/29 ≈ 83%)
PLUSH_NEW_ASTRA = 96.7 # GPT-6.2 Astra 拉毛巾取毛绒玩具成功率 (29/30)
# SenseNova harness 消融（GPT-6-Astra，RoboDojo 42 任务均值）
ABLATION = [
    ("π0.5 单独", 6.91, MUTED),
    ("VLA 闭环审核", 25.83, ORANGE),
    ("ICL + VLA", 54.17, GREEN),
]
# 成本（GPT-6-Astra 下 LIBERO-Long++ 10× 步数）
COST_TOKENS_M = 1.0      # 每回合约 1M tokens
COST_MINUTES = 60        # 近 1 小时
COST_USD = 1.0           # 98% 缓存输入，GPT-6-Astra 计价下 1M tokens ≈ 1 USD
FALL_HEIGHT_M = 1.0
G = 9.8


def fall_time(h=FALL_HEIGHT_M, g=G):
    return math.sqrt(2.0 * h / g)


def verify_numbers():
    assert 2.0 < SUCCESS_NEW / SUCCESS_OLD < 2.2  # 41.23/19.64≈2.10，约翻倍
    assert abs((LATENCY_OLD - LATENCY_NEW) / LATENCY_OLD - 0.323) < 0.01  # 约 -32.3%（近三分之一）
    assert 0.44 < fall_time() < 0.46  # 1 米自由落体约 0.45 秒
    assert 22 < LATENCY_NEW / fall_time() < 23  # 思考期间杯子可落地约 22.5 次（约 22 次）
    assert ABLATION[0][1] < ABLATION[1][1] < ABLATION[2][1]
    for _, num, den, _ in REAL_TASKS:
        assert 0 <= num <= den
    assert TSHIRT_SUCCESSES == 0 and TSHIRT_TRIALS > 0
    assert 0 < TSHIRT_NEW_NUM < TSHIRT_NEW_DEN
    assert TONG_OLD_SOL < TONG_NEW_ASTRA
    assert 0 < DONE_ACCURACY < 100


def bar(x, y, w, h, frac, fg, bg=SLATE_SOFT):
    """横向进度条：y 为顶边。"""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.1f}" fill="{bg}"/>']
    if frac > 0:
        fw = max(h, w * frac)
        out.append(f'<rect x="{x}" y="{y}" width="{fw:.1f}" height="{h}" rx="{h/2:.1f}" fill="{fg}"/>')
    return out


# ---------------------------------------------------------------------------
# 图 1：三条路径总览
# ---------------------------------------------------------------------------
def build_three_paths_overview():
    els = header(
        "图 1 · 大模型指挥机械臂，靠的不是一条路，而是三条路加一道坎",
        "统计直觉给计划，仿真地基给训练场，真机示教给最后一厘米；最后还要跨过“世界时钟”这一关",
    )
    paths = [
        (20, "① 直觉物理", "从海量图文与视频里学到\n“看起来会怎样”的统计规律", BLUE, BLUE_SOFT,
         "擅长：看懂场景、拆计划、定空间目标"),
        (264, "② 仿真地基", "CAD / 网格 / 物理引擎\n把“三维世界”变成可训练的环境", GREEN, GREEN_SOFT,
         "擅长：生成数据、反复试错、迁移到真机"),
        (508, "③ 真机示教", "少量真机示范写进上下文\n边看边改、闭环纠错", PURPLE, PURPLE_SOFT,
         "擅长：泛化到新任务、失败后换策略"),
    ]
    for x0, title, sub, col, soft, note in paths:
        els.append(card(x0, 60, 232, 182, fill=CARD_BG, stroke=col))
        els.append(pill(x0 + 16, 74, title, fg=col, bg=soft, w=200, h=24, size=12.5))
        for i, line in enumerate(sub.split("\n")):
            els.append(txt(x0 + 116, 126 + i * 22, line, 12, BODY, "middle"))
        els.append(txt(x0 + 116, 214, note, 11.5, col, "middle", weight="600"))
        els.append(
            f'<path d="M{x0 + 116} 244 L{x0 + 116} 264" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr-muted)"/>'
        )

    els.append(card(20, 268, 720, 60, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(380, 292, "共同终点：把一句自然语言，变成机械臂一串正确的动作", 13.5, INK, "middle", weight="700"))
    els.append(
        txt(380, 313, "但三条路都绕不开第四关——模型思考时，真实世界的时钟不会停（图 5）", 11.5, MUTED, "middle")
    )
    return figure(
        342,
        "大模型指挥机械臂的三条路径与一道时间瓶颈",
        "直觉物理、仿真地基、真机示教三条路径共同支撑大模型控制机械臂，但都受限于思考期间真实世界不停顿的时间瓶颈。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 2：Ember-0 成绩单
# ---------------------------------------------------------------------------
def build_ember0_scoreboard():
    els = header(
        "图 2 · 真机成绩单：翻倍是真的，但“多数任务仍失败”也是真的",
        "左：XDOF Ember-0 双臂真机 16 任务均值（2026-11）；右：SenseNova 对 GPT-6-Astra 的 8 平台实测（2026-10）",
    )
    # 左侧：总成功率对比
    els.append(card(20, 60, 300, 226))
    els.append(txt(36, 84, "Ember-0 总成功率（16 任务均值）", 12.5, INK, weight="700"))
    base_y, max_h = 230, 118
    h_old = max_h * SUCCESS_OLD / 50.0
    h_new = max_h * SUCCESS_NEW / 50.0
    for x, val, h, col, lab in (
        (74, SUCCESS_OLD, h_old, SLATE, "GPT-6 Astra\n2026-10"),
        (198, SUCCESS_NEW, h_new, GREEN, "GPT-6.2 Astra\n2026-11"),
    ):
        els.append(f'<rect x="{x}" y="{base_y - h:.1f}" width="64" height="{h:.1f}" rx="6" fill="{col}"/>')
        els.append(txt(x + 32, base_y - h - 8, f"{val:.1f}%", 13.5, col, "middle", weight="700"))
        for i, line in enumerate(lab.split("\n")):
            els.append(txt(x + 32, base_y + 16 + i * 15, line, 11.5, MUTED, "middle"))
    els.append(txt(170, 274, "约翻倍：19.6% → 41.2%", 11.5, GREEN, "middle", weight="600"))

    # 右侧：SenseNova 真机分组（GPT-6-Astra，8 种机器人平台）
    els.append(card(336, 60, 404, 226))
    els.append(txt(352, 84, "SenseNova 真机分组（GPT-6-Astra）", 12.5, INK, weight="700"))
    for i, (name, num, den, col) in enumerate(REAL_TASKS):
        y = 104 + i * 42
        els.append(txt(352, y + 13, name, 12, BODY, weight="600"))
        els.extend(bar(434, y, 192, 18, num / den, col))
        rate = 100.0 * num / den
        els.append(txt(638, y + 13, f"{num}/{den}（{rate:.0f}%）", 11.5, col, weight="700"))
    els.append(txt(352, 274, "刚性抓取稳；柔性、长程与毫米级插接仍是硬骨头", 11.5, MUTED))

    # 底部三条一手观察
    facts = [
        f"自报 done 真完成仅 {DONE_ACCURACY:.0f}%",
        f"展平 T 恤：前五模型 0/143，6.2 仅 {TSHIRT_NEW_NUM}/{TSHIRT_NEW_DEN}",
        f"思考 {LATENCY_NEW:.1f} 秒 ≈ 杯子落地 22 次",
    ]
    for i, f in enumerate(facts):
        x0 = 20 + i * 244
        els.append(card(x0, 300, 232, 34, fill=SLATE_SOFT, stroke=HAIRLINE))
        els.append(txt(x0 + 116, 322, f, 11.5, INK, "middle", weight="600"))
    return figure(
        348,
        "Ember-0 真机成绩单与 SenseNova 真机分组成功率",
        "XDOF Ember-0 总成功率从GPT-6 Astra（2026年10月）的19.6%提升到GPT-6.2 Astra（2026年11月）的41.2%；SenseNova对GPT-6-Astra在八种真机平台实测中刚性抓取17/18、柔性2/4、长程移动9/23、精确插接0/11；早期五模型宣称done时任务真完成仅57%，展平T恤前五模型0/143而6.2仅1/30。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 3：仿真地基闭环（sim2real）
# ---------------------------------------------------------------------------
def build_sim2real_loop():
    els = header(
        "图 3 · 上一篇的 CAD/CAE 流水线，在这里成了机器人的“训练场”",
        "Isaac Sim 可把 CAD/URDF 转成 USD，赋材质、开物理、配传感器，再生成合成数据训练策略",
    )
    stages = [
        (16, 132, "① 几何", "CAD / URDF\n→ USD 场景", BLUE, BLUE_SOFT),
        (164, 132, "② 物理", "材质·重力\n接触·布料", GREEN, GREEN_SOFT),
        (312, 132, "③ 训练", "合成数据\n强化学习", ORANGE, ORANGE_SOFT),
        (460, 132, "④ 真机", "部署到机器人\n传感器实测", PURPLE, PURPLE_SOFT),
        (608, 136, "⑤ 回流", "数字孪生\n实测修正模型", SLATE, SLATE_SOFT),
    ]
    for x0, w, title, sub, col, soft in stages:
        els.append(card(x0, 60, w, 100, fill=soft, stroke=col))
        els.append(txt(x0 + w / 2, 82, title, 12.5, col, "middle", weight="700"))
        for i, line in enumerate(sub.split("\n")):
            els.append(txt(x0 + w / 2, 106 + i * 20, line, 11.5, BODY, "middle"))
    for x0 in (150, 298, 446, 594):
        els.append(f'<path d="M{x0} 110 L{x0 + 12} 110" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#arr-muted)"/>')

    extra_defs = """
  <marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#6d28d9"/>
  </marker>"""
    els.append(
        f'<path d="M676 162 L676 204 Q676 216 664 216 L94 216 Q82 216 82 204 L82 164" fill="none" '
        f'stroke="{PURPLE}" stroke-width="1.7" stroke-dasharray="5 3" marker-end="url(#arr-purple)"/>'
    )
    els.append(f'<rect x="270" y="203" width="220" height="26" rx="13" fill="{BG}"/>')
    els.append(txt(380, 221, "← 真实数据回流修正仿真模型", 11.5, PURPLE, "middle", weight="700"))

    els.append(txt(20, 254, "呼应上一篇《在电脑里捏出一座桥》：点线面体 → 实体 → 受力 → 数字孪生，", 12, BODY))
    els.append(txt(20, 276, "在机器人这里变成：几何 → 物理 → 策略 → 真机 → 回流。模型不是在背有限元公式，", 12, BODY))
    els.append(txt(20, 298, "而是学会了“调用这套工具链”；显式求解器仍负责给出可信的数值。", 12, BODY))
    return figure(
        314,
        "CAD到真机的仿真训练闭环：与三维物理建模工程闭环同构",
        "CAD或URDF几何转成USD场景，加上材质、重力、接触、布料等物理，生成合成数据训练机器人策略，部署真机后传感器实测数据回流修正模型；这一闭环与三维物理建模的数字孪生闭环结构相同。",
        els,
        extra_defs=extra_defs,
    )


# ---------------------------------------------------------------------------
# 图 4：ICL 知识包与步数预算
# ---------------------------------------------------------------------------
def build_icl_package():
    els = header(
        "图 4 · “没有微调”不等于“没看示范”：ICL 知识包与 10 倍步数预算",
        "SenseNova 评测 GPT-6-Astra 的协议：先研读训练示教写下只读知识包 K，测试时按场景检索适配",
    )
    els.append(card(20, 60, 452, 230))
    els.append(txt(36, 84, "知识包 K 的六类内容（测试前写定、只读）", 12.5, INK, weight="700"))
    items = [
        ("任务指南", "目标·阶段·策略", ".md", BLUE),
        ("运动参考", "轨迹·抓取·相位锚点", ".npz", BLUE),
        ("视觉参考", "示范帧·接触局部", ".png", GREEN),
        ("可执行助手", "正/逆解·检索·动作生成", ".py", GREEN),
        ("检查与恢复", "完成判定·失败修复", ".md/.py", ORANGE),
        ("元数据", "机器人规格·来源·校验", ".md/.py", ORANGE),
    ]
    for i, (name, sub, ext, col) in enumerate(items):
        x0 = 36 + (i % 2) * 218
        y = 100 + (i // 2) * 60
        els.append(card(x0, y, 206, 50, fill=SLATE_SOFT, stroke=HAIRLINE))
        els.append(txt(x0 + 10, y + 19, name, 12, col, weight="700"))
        els.append(txt(x0 + 10, y + 38, f"{sub}  {ext}", 11.5, BODY))

    els.append(card(488, 60, 252, 230))
    els.append(txt(504, 84, "步数预算：1× → 10×", 12.5, INK, weight="700"))
    els.extend(bar(504, 108, 216, 20, 0.1, SLATE))
    els.append(txt(612, 142, "官方 1×：常规步数上限", 11.5, MUTED, "middle"))
    els.extend(bar(504, 166, 216, 20, 1.0, GREEN))
    els.append(txt(612, 200, "放宽到 10×：允许失败后重试", 11.5, GREEN, "middle"))
    els.append(txt(504, 228, "LIBERO / SIMPLE 族成功率 >95%", 12, INK, weight="700"))
    els.append(txt(504, 250, "代价：约 1M tokens、近 1 小时/回合", 11.5, MUTED))
    els.append(txt(504, 268, "（约 98% 缓存输入，折合约 1 美元）", 11.5, MUTED))

    els.append(card(20, 302, 720, 48, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(34, 322, "消融实验（RoboDojo 42 任务）：", 12, INK, weight="700"))
    els.append(txt(238, 322, "π0.5 单独 6.91%  →  闭环审核 25.83%  →  ICL + VLA 54.17%", 12, GREEN, weight="700"))
    els.append(
        txt(34, 341, "接口也有讲究：方向命令 +2.50 分，关节角 −5.84 分，自适应分块 +4.44 分。", 11.5, MUTED)
    )
    return figure(
        364,
        "上下文学习知识包内容与步数预算消融结果",
        "SenseNova对GPT-6-Astra的评测协议中，大模型研读示教后写入六类冻结知识包并在测试时检索适配；把步数预算放宽到10倍可让LIBERO等族成功率超过95%，代价约1M tokens和1小时每回合；消融显示ICL加VLA达54.17%，远高于VLA单独6.91%。",
        els,
    )


# ---------------------------------------------------------------------------
# 图 5：双系统 + 世界时钟动画
# ---------------------------------------------------------------------------
def build_dual_system_clock():
    t_fall = fall_time()
    n_falls = LATENCY_NEW / t_fall
    # 动画：同一时间映射，思考条 3.2s 走完，杯子在 3.2*(t_fall/LATENCY_NEW) 秒内落地
    # DOM 终态直接把实心杯画在地面上，初态用 translateY(-100px) 悬在 h=1.0m 虚线杯处；
    # 这样动画结束后及 prefers-reduced-motion 下杯子均稳稳停在地面，不会越界或弹回空中。
    dur = 3.2
    cup_dur = dur * t_fall / LATENCY_NEW
    delay = 0.8
    drop_px = 100
    y_release = 118
    cup_h = 26
    y_ground = y_release + cup_h + drop_px  # 244
    y_cup_final = y_ground - cup_h          # 218
    assert y_cup_final - drop_px == y_release

    extra_css = f"""
  @keyframes clockBar {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  @keyframes cupDrop {{ from {{ transform: translateY(-{drop_px}px); }} to {{ transform: translateY(0); }} }}
  @keyframes revealText {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  .a-bar {{ transform-box: fill-box; transform-origin: left center;
            animation: clockBar {dur}s linear {delay}s 1 backwards; }}
  .a-cup {{ animation: cupDrop {cup_dur:.3f}s ease-in {delay}s 1 backwards; }}
  .a-land {{ animation: revealText 0.2s ease-out {delay + cup_dur:.3f}s 1 backwards; }}
  .a-txt {{ animation: revealText 0.5s ease-out {delay + dur:.2f}s 1 backwards; }}
  @media (prefers-reduced-motion: reduce) {{
    .a-bar, .a-cup, .a-land, .a-txt {{ animation: none !important; }}
  }}
"""
    els = header(
        f"图 5 · 世界时钟：模型想 {LATENCY_NEW:.1f} 秒，1 米高的杯子早落地约 22 次",
        f"按真实自由落体 t=√(2h/g)：1 米约 {t_fall:.2f} 秒；动画按同一时间比压缩，播放一次停在终态",
    )
    # 左：双系统架构（统一卡片高度 268，内部充足留白）
    els.append(card(20, 64, 300, 268))
    els.append(txt(36, 88, "快慢双系统分工", 12.5, INK, weight="700"))
    layers = [
        (100, "System 2 · 大模型（慢脑）", "看全局、拆计划、纠错（约 10 秒级）", PURPLE, PURPLE_SOFT, 54),
        (162, "System 1 · VLA（如 π0.5）", "视觉-语言-动作，快执行与局部闭环", ORANGE, ORANGE_SOFT, 54),
        (224, "System 0 · 底层运动控制", "关节力矩/速度闭环，毫秒级稳定", GREEN, GREEN_SOFT, 54),
    ]
    for y, title, sub, col, soft, h in layers:
        els.append(card(32, y, 276, h, fill=soft, stroke=col))
        els.append(txt(44, y + 20, title, 12, col, weight="700"))
        els.append(txt(44, y + 40, sub, 11.5, BODY))
    els.append(txt(170, 298, "真机验证：G1 上操作 2/3、行走 3/3 可行，", 11.5, MUTED, "middle"))
    els.append(txt(170, 316, "但约 90% 耗时花在思考，非实时运动控制", 11.5, MUTED, "middle"))

    # 右：世界时钟（与左侧等高 268，所有元素均在卡片内）
    els.append(card(336, 64, 404, 268))
    els.append(txt(352, 88, "模型思考进度条 vs 杯子自由落体", 12.5, INK, weight="700"))
    els.append(txt(352, 111, "释放高度 h = 1.0 m（虚线为 t = 0 s 初态）", 11.5, MUTED))
    els.append(
        f'<line x1="356" y1="{y_release}" x2="720" y2="{y_release}" stroke="{HAIRLINE}" stroke-width="1.4" stroke-dasharray="4 3"/>'
    )
    # 静态初态虚线杯（确保静态阅读与动画结束后仍能看清下落起点）
    els.append(
        f'<rect x="521" y="{y_release}" width="34" height="{cup_h}" rx="4" fill="{BG}" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="3 2"/>'
    )
    els.append(txt(564, y_release + 17, "t = 0 s 脱手", 11.5, MUTED))

    # 地面线
    els.append(f'<line x1="356" y1="{y_ground}" x2="720" y2="{y_ground}" stroke="{SLATE}" stroke-width="2"/>')
    els.append(txt(356, y_ground + 17, "地面（h = 0 m）", 11.5, MUTED))

    # 实心运动杯（DOM 位于地面终态 y_cup_final）
    els.append('<g class="a-cup">')
    els.append(f'<rect x="521" y="{y_cup_final}" width="34" height="{cup_h}" rx="4" fill="{BLUE}"/>')
    els.append(f'<text x="538" y="{y_cup_final + 17}" font-size="11.5" fill="#ffffff" text-anchor="middle">杯</text>')
    els.append("</g>")
    els.append('<g class="a-land">')
    els.append(txt(564, y_ground - 8, f"t ≈ {t_fall:.2f} s 已落地", 11.5, BLUE, weight="600"))
    els.append("</g>")

    # 思考条（终态画满，动画从 0 展开）
    els.append(f'<rect x="356" y="280" width="364" height="14" rx="7" fill="{SLATE_SOFT}"/>')
    els.append('<g class="a-bar">')
    els.append(f'<rect x="356" y="280" width="364" height="14" rx="7" fill="{PURPLE}"/>')
    els.append("</g>")
    els.append(txt(356, 314, "0 s", 11.5, MUTED))
    els.append(txt(538, 314, "单步思考耗时进度", 11.5, PURPLE, "middle"))
    els.append(txt(720, 314, f"{LATENCY_NEW:.1f} s", 11.5, PURPLE, "end", weight="700"))

    # 终态读数（动画结束后出现；reduced-motion 直接显示）
    els.append('<g class="a-txt">')
    els.append(f'<rect x="336" y="64" width="404" height="268" rx="10" fill="none" stroke="{PURPLE}" stroke-width="2"/>')
    els.append(
        txt(538, 182, f"思考 {LATENCY_NEW:.1f} s ÷ 落地 {t_fall:.2f} s ≈ {n_falls:.0f} 次", 12, PURPLE, "middle", weight="700", halo=True)
    )
    els.append("</g>")

    els.append(
        txt(20, 356, "SenseNova 世界时钟公寓原型实测：模型正确判断该关火，但思考耗时让关火晚了约 90 秒，鸡蛋已焦。", 11.5, BODY)
    )
    els.append(
        txt(20, 376, "传统仿真基准会暂停时钟等模型想完；真实世界不会停。这是 41.2% 背后最朴素的一道物理限制。", 11.5, BODY)
    )
    return figure(
        394,
        "快慢双系统架构与世界时钟：10.2秒思考与1米落体对比",
        "大模型作为System2负责慢规划，VLA作为System1快执行，底层System0做毫秒级运动控制；右侧按真实自由落体时间绘制：1米高杯子约0.45秒落地，而GPT-6.2 Astra平均思考约10.2秒，期间杯子可落地约22次。动画播放一次停在地面终态，减少动态效果时直接静态呈现。",
        els,
        extra_css=extra_css,
    )


# ---------------------------------------------------------------------------
# 图 6：四道工程边界
# ---------------------------------------------------------------------------
def build_capability_boundaries():
    els = header(
        "图 6 · 四道边界：为什么“具身胜任”还不等于“实用具身智能”",
        "SenseNova 结论原话：已大体跨过 embodied competence，尚未跨过 practical embodied intelligence",
    )
    rows = [
        (60, "① 精确接触", "插头对孔真机 0/11；Ember-0 拿笔写字仅 5/30（17%）", RED,
         "缺力觉反馈；夹面包 6.2 虽升至 27/30，毫米级盲插仍全败"),
        (124, "② 柔性形变", "展平 T 恤：前五模型 0/143，6.2 首破零也仅 1/30（3.3%）", ORANGE,
         "知道要展开 ≠ 能管住四个角与不断变化的褶皱（打结仅 5/27）"),
        (188, "③ 长程与遗忘", "移动取物 9/23；Ember-0 摆餐具 0/30、倒麦片 0/22", PURPLE,
         "多步长链条里小误差跨阶段累积，后一步常撞乱前一步成果"),
        (252, "④ 不可逆失败", "自报 done 真完成仅 57%；捏碎薯片、煎焦鸡蛋无法重来", BLUE,
         "“画面看着像做完”与满足接触、支撑、时间窗口约束不是一回事"),
    ]
    for y, title, data, col, note in rows:
        els.append(card(20, y, 720, 56, fill=CARD_BG, stroke=HAIRLINE))
        els.append(f'<rect x="20" y="{y}" width="6" height="56" rx="3" fill="{col}"/>')
        els.append(txt(40, y + 22, title, 12.5, col, weight="700"))
        els.append(txt(40, y + 42, note, 11.5, MUTED))
        els.append(txt(404, y + 22, data, 11.5, BODY, weight="600"))

    els.append(card(20, 320, 720, 42, fill=SLATE_SOFT, stroke=HAIRLINE))
    els.append(txt(34, 338, "认识论不变：统计直觉 / 显式仿真 / 真实测量三件事不能混。", 12, INK, weight="700"))
    els.append(txt(34, 356, "模型给缩小范围的假设；真机传感器与人的判断，才是最终裁判。", 11.5, MUTED))
    return figure(
        378,
        "具身智能的四道工程边界与真实实测数据",
        "精确接触、柔性形变、长程遗忘、不可逆失败是具身智能落地的四道边界，图中给出SenseNova与XDOF的一手实测数字；结论是模型给出的假设必须接受真实测量检验。",
        els,
    )


@register(
    "embodied-ai-three-paths",
    "具身智能：三条路径、Ember-0 成绩单、仿真闭环、ICL 知识包、双系统世界时钟与四道工程边界",
    "ai_ml",
)
def build_embodied_ai():
    verify_numbers()
    write_svg(SUBDIR, "three-paths-overview", build_three_paths_overview())
    write_svg(SUBDIR, "ember0-scoreboard", build_ember0_scoreboard())
    write_svg(SUBDIR, "sim2real-cad-loop", build_sim2real_loop())
    write_svg(SUBDIR, "icl-knowledge-package", build_icl_package())
    write_svg(SUBDIR, "dual-system-clock", build_dual_system_clock())
    write_svg(SUBDIR, "capability-boundaries", build_capability_boundaries())
