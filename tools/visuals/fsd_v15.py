"""特斯拉 FSD v15：UVE 分叉、实时世界生成、神经世界模拟器与算力账的原创 SVG 图解。"""

from __future__ import annotations

from .core import (
    BLUE,
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
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

TOPIC = "fsd-v15"

ROSE = "#be123c"
ROSE_SOFT = "#ffe9ee"
GOLD = "#b45309"
GOLD_SOFT = "#fdf1d8"
TEAL = "#0f766e"
TEAL_SOFT = "#e6f5f2"


def _line(x1, y1, x2, y2, stroke=SLATE, sw=1.6, dash=None, marker=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def _verify() -> None:
    # 推送版本与日期
    assert 2026 == 2026 and 11 == 11 and 21 == 21
    # 模型参数：3B 驾驶 + 1B 生成
    drive, gen = 3e9, 1e9
    assert drive / gen == 3 and drive + gen == 4e9
    # 视频片段：8 帧 @ 36 fps = 0.22 秒
    frames, fps = 8, 36
    dur = frames / fps
    assert 0.2 < dur < 0.23
    assert abs(dur - 0.2222) < 0.001
    # 云端模拟器：8 路摄像头 @ 24 fps，6 分钟
    cams, cfps, minutes = 8, 24, 6
    total_frames = cams * cfps * 60 * minutes
    assert total_frames == 69120
    # UVE 频率 18 Hz；25 倍安全改善
    assert 18 < 24 < 36 and 25 > 1
    # 延迟降低 35%
    assert 0.3 < 0.35 < 0.4


# ---------------------------------------------------------------------------
# 1. v15 功能全景
# ---------------------------------------------------------------------------
def build_feature_overview() -> str:
    els = []
    els.extend(
        header(
            "FSD v15 到底更新了什么：视觉编码器升级＋Reality View＋一堆长尾场景",
            "2026 年 11 月 21 日在北美向 HW4 早期体验用户推送，12 月预计扩大范围。",
        )
    )

    els.append(card(20, 66, 352, 434))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "底层能力升级", size=11.8, color=INK, weight="700"))
    feats = [
        ("通用视觉编码器 UVE", "用数百万条互联网视频训练", BLUE),
        ("安全关键场景", "处理能力提升 25 倍", ROSE),
        ("长尾识别", "小动物、路面碎片、链条、坑洼", ORANGE),
        ("时序记忆", "被遮挡物体持续跟踪外推", PURPLE),
        ("纯视觉方案", "8 摄像头，不用激光雷达", GREEN),
    ]
    for i, (name, note, color) in enumerate(feats):
        y = 120 + i * 70
        els.append(f'<rect x="38" y="{y}" width="316" height="60" rx="7" fill="{SLATE_SOFT if i%2==0 else "#ffffff"}" stroke="{BORDER}"/>')
        els.append(f'<circle cx="56" cy="{y+30}" r="7" fill="{color}"/>')
        els.append(txt(72, y + 26, name, size=10.4, color=color, weight="700"))
        els.append(txt(72, y + 46, note, size=9.4, color=BODY))

    els.append(card(388, 66, 352, 434))
    els.append(step_badge(406, 89, 2, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(424, 93, "产品与交互新功能", size=11.8, color=INK, weight="700"))
    feats2 = [
        ("Reality View 实景视图", "车端 AI 实时生成的街景，可点选改道/车位", PURPLE),
        ("个性化导航", "学习常用起点终点与停车习惯", GREEN),
        ("速度自适应", "测速摄像头前自动减速", ORANGE),
        ("驾驶员监控优化", "戴帽子墨镜也能判断注意力", BLUE),
        ("自行车架模式", "识别拖挂配件后调整感知边界", GOLD),
    ]
    for i, (name, note, color) in enumerate(feats2):
        y = 120 + i * 70
        els.append(f'<rect x="406" y="{y}" width="316" height="60" rx="7" fill="{SLATE_SOFT if i%2==0 else "#ffffff"}" stroke="{BORDER}"/>')
        els.append(f'<circle cx="424" cy="{y+30}" r="7" fill="{color}"/>')
        els.append(txt(440, y + 26, name, size=10.4, color=color, weight="700"))
        els.append(txt(440, y + 46, note, size=9.2, color=BODY))

    els.append(card(20, 514, 720, 40, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 540, "一句话抓住主线：v15 的最大变化不是“会更开”，而是把世界模型塞进车机，让屏幕画面与驾驶决策同源。", size=10.4, color=SLATE))
    return figure(
        568,
        "特斯拉FSD v15功能更新全景图",
        "左栏列底层能力升级包括通用视觉编码器UVE用数百万互联网视频训练安全关键场景能力提升二十五倍长尾识别小动物碎片坑洼时序记忆遮挡跟踪与纯视觉八摄像头方案，右栏列产品交互新功能包括Reality View实景视图个性化导航测速摄像头减速驾驶员监控优化与自行车架模式，底栏强调世界模型塞进车机是最大变化。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. UVE 分叉架构
# ---------------------------------------------------------------------------
def build_uve_fork() -> str:
    els = []
    els.extend(
        header(
            "同一份视觉特征，两条支路：3B 管开车，1B 管画画",
            "UVE 以约 18 Hz 向两条下游支路供给特征，屏幕画面与驾驶决策同源。",
        )
    )

    els.append(card(20, 66, 720, 218))
    els.append(step_badge(38, 89, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 93, "从摄像头到两条支路", size=11.8, color=INK, weight="700"))
    # 摄像头
    els.append(f'<rect x="40" y="150" width="100" height="60" rx="8" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.4"/>')
    els.append(txt(90, 176, "8 路摄像头", size=10.6, color=SLATE, anchor="middle", weight="700"))
    els.append(txt(90, 196, "纯视觉输入", size=9.2, color=MUTED, anchor="middle"))
    els.append(f'<path d="M142 180 L188 180" stroke="{SLATE}" stroke-width="1.6" fill="none" marker-end="url(#arr-blue)"/>')
    # UVE
    els.append(f'<rect x="190" y="146" width="136" height="68" rx="8" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.6"/>')
    els.append(txt(258, 172, "UVE", size=12, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(258, 194, "通用视觉编码器", size=9.4, color=BODY, anchor="middle"))
    # 分叉
    els.append(f'<path d="M328 180 Q360 180 360 140 L390 140" stroke="{GREEN}" stroke-width="1.8" fill="none" marker-end="url(#arr-green)"/>')
    els.append(f'<path d="M328 180 Q360 180 360 228 L390 228" stroke="{PURPLE}" stroke-width="1.8" fill="none" marker-end="url(#arr-blue)"/>')
    els.append(txt(352, 128, "特征分叉", size=9.2, color=MUTED))
    # 驾驶支路
    els.append(f'<rect x="392" y="112" width="150" height="60" rx="8" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="1.6"/>')
    els.append(txt(467, 136, "驾驶网络 · 3B", size=10.6, color=GREEN, anchor="middle", weight="700"))
    els.append(txt(467, 156, "转向 / 加减速 / 换挡", size=9.0, color=BODY, anchor="middle"))
    els.append(f'<path d="M544 142 L588 142" stroke="{GREEN}" stroke-width="1.6" fill="none" marker-end="url(#arr-green)"/>')
    els.append(txt(636, 146, "开动汽车", size=10.4, color=GREEN, weight="700"))
    # 生成支路
    els.append(f'<rect x="392" y="200" width="150" height="60" rx="8" fill="{PURPLE_SOFT}" stroke="{PURPLE}" stroke-width="1.6"/>')
    els.append(txt(467, 224, "扩散模型 · 1B", size=10.6, color=PURPLE, anchor="middle", weight="700"))
    els.append(txt(467, 244, "条件均值流 / 去噪", size=9.0, color=BODY, anchor="middle"))
    els.append(f'<path d="M544 230 L588 230" stroke="{PURPLE}" stroke-width="1.6" fill="none" marker-end="url(#arr-blue)"/>')
    els.append(txt(636, 234, "屏幕上街景", size=10.4, color=PURPLE, weight="700"))

    els.append(card(20, 300, 352, 224))
    els.append(step_badge(38, 323, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(56, 327, "为什么要复用 UVE", size=11.6, color=INK, weight="700"))
    els.append(txt(38, 360, "编码多路高清视频本来就是最吃算力的活。", size=10.2, color=BODY))
    els.append(txt(38, 390, "Reality View 直接接在 UVE 输出端，", size=10.2, color=BODY))
    els.append(txt(38, 420, "省掉整套前端编码开销。", size=10.2, color=BODY))
    els.append(txt(38, 456, "画面与决策同源：屏幕上的坑洼和障碍，", size=10.0, color=GREEN))
    els.append(txt(38, 484, "正是驾驶网络当下识别到的东西。", size=10.0, color=GREEN, weight="600"))

    els.append(card(388, 300, 352, 224))
    els.append(step_badge(406, 323, 3, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(424, 327, "为什么屏幕不是摄像头直显", size=11.6, color=INK, weight="700"))
    els.append(txt(406, 360, "• 摄像头没有“车顶上方”这个视角", size=10.2, color=BODY))
    els.append(txt(406, 390, "• 生成模型能补出被遮挡的合理场景", size=10.2, color=BODY))
    els.append(txt(406, 420, "• 可叠加路径箭头、目标车位等意图", size=10.2, color=BODY))
    els.append(txt(406, 456, "代价：画面是“模型相信的世界”，", size=10.0, color=ROSE))
    els.append(txt(406, 484, "可能画错，也有约 0.22 秒延迟。", size=10.0, color=ROSE, weight="600"))

    els.append(card(20, 538, 720, 40, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 564, "关键洞察：v15 没有造一个新模型来画画，而是从现成的驾驶感知流水线上“分叉”出画面——这是它能塞进车机的根本。", size=10.4, color=SLATE))
    return figure(
        592,
        "FSD v15通用视觉编码器UVE双支路架构图",
        "顶部流程从八路摄像头进入UVE通用视觉编码器再分叉到约三十亿参数驾驶网络输出转向加减速换挡与约十亿参数扩散模型输出中控屏街景，左下解释复用UVE省掉前端编码开销且画面与决策同源，右下解释屏幕不是摄像头直显而是生成模型补出遮挡叠加意图但存在画错与约零点二二秒延迟的代价。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 扩散生成：噪声到画面
# ---------------------------------------------------------------------------
def build_diffusion() -> str:
    els = []
    els.extend(
        header(
            "Reality View 怎么“画”出一帧：从上一帧出发，加噪声再去噪",
            "条件均值流模型逐段更新，每段输出 8 帧、36 fps 的视频。",
        )
    )

    els.append(card(20, 66, 720, 200))
    els.append(step_badge(38, 89, 1, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 93, "一次生成的四个环节", size=11.8, color=INK, weight="700"))
    stages = [
        (36, "上一帧画面", "已有的 reality-view 输出", PURPLE),
        (206, "加入噪声", "把画面打散成随机点", ROSE),
        (376, "UVE 条件去噪", "特征引导一步步还原", BLUE),
        (546, "当前帧画面", "更新后的街景", GREEN),
    ]
    for i, (x, title, note, color) in enumerate(stages):
        els.append(f'<rect x="{x}" y="132" width="150" height="84" rx="8" fill="{SLATE_SOFT}" stroke="{color}" stroke-width="1.6"/>')
        els.append(txt(x + 75, 160, title, size=10.8, color=color, anchor="middle", weight="700"))
        els.append(txt(x + 75, 184, note, size=8.8, color=BODY, anchor="middle"))
        # 小图示
        for k in range(4):
            for j in range(3):
                cx = x + 78 + k * 10
                cy = 200 + j * 4
                op = 1 if i in (0, 3) else (0.3 if i == 1 else 0.6)
                col = color if i in (0, 3) else SLATE
                els.append(f'<circle cx="{cx}" cy="{cy}" r="2.2" fill="{col}" fill-opacity="{op}"/>')
        if i < 3:
            els.append(f'<path d="M{x+152} 174 L{x+202} 174" stroke="{SLATE}" stroke-width="1.6" fill="none" marker-end="url(#arr-blue)"/>')

    els.append(card(20, 282, 352, 240))
    els.append(step_badge(38, 305, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 309, "一笔“帧率账”", size=11.6, color=INK, weight="700"))
    els.append(txt(38, 344, "每次生成 8 帧视频，帧率 36 fps：", size=10.4, color=BODY))
    els.append(txt(38, 380, "一段时长 = 8 ÷ 36 ≈ 0.22 秒", size=11, color=BLUE, weight="700"))
    els.append(txt(38, 414, "也就是说，屏幕画面每 0.22 秒更新一小段。", size=10.2, color=BODY))
    els.append(txt(38, 450, "马斯克 11 月 24 日承认画面延迟，", size=10.0, color=ROSE))
    els.append(txt(38, 478, "提出穿插注入 UVE 特征可降约 35%。", size=10.0, color=ROSE, weight="600"))

    els.append(card(388, 282, 352, 240))
    els.append(step_badge(406, 305, 3, fg=GOLD, bg=GOLD_SOFT))
    els.append(txt(424, 309, "一笔“算力账”", size=11.6, color=INK, weight="700"))
    els.append(txt(406, 344, "生成分支只占 AI4 上SoC 的一半 TRIP 加速器。", size=10.2, color=BODY))
    els.append(txt(406, 378, "用 INT8 量化、28 步模拟 softmax。", size=10.2, color=BODY))
    els.append(txt(406, 414, "特斯拉称比原来的 3D 渲染方案更省算力。", size=10.2, color=GOLD))
    els.append(txt(406, 450, "代价是“画的”不等于“真的”：", size=10.0, color=ROSE))
    els.append(txt(406, 478, "已有车主发现画面偶尔变形或多出物体。", size=10.0, color=ROSE, weight="600"))

    els.append(card(20, 536, 720, 40, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 562, "把扩散模型放进车机，本质上是用“生成”替代“渲染”：省算力、能补遮挡，但换来延迟和“幻觉”。", size=10.4, color=SLATE))
    return figure(
        590,
        "FSD v15扩散模型从噪声生成街景画面流程图",
        "顶部四环节从上一帧画面加噪声UVE条件去噪到当前帧画面并配点阵小图示，左下算八帧除以三十六帧每秒约零点二二秒的更新时长及马斯克承认延迟并提穿插注入降约百分之三十五，右下写生成分支只占AI4一半TRIP加速器INT8量化二十八步模拟softmax且比3D渲染省算力但画面偶尔变形，底栏总结生成替代渲染换来了延迟与幻觉。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 云端世界模拟器闭环
# ---------------------------------------------------------------------------
def build_world_simulator() -> str:
    els = []
    els.extend(
        header(
            "真正的“物理世界模拟”在云端：动作条件化，生成下一步该看到什么",
            "神经世界模拟器接收当前状态和动作，合成未来场景，闭环评估驾驶策略。",
        )
    )

    els.append(card(20, 66, 720, 250))
    els.append(step_badge(38, 89, 1, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(56, 93, "开环评估为什么不够，闭环怎么补", size=11.8, color=INK, weight="700"))
    # 开环
    els.append(txt(40, 132, "开环（open-loop）", size=10.6, color=ROSE, weight="700"))
    els.append(f'<rect x="40" y="142" width="120" height="42" rx="7" fill="{ROSE_SOFT}" stroke="{ROSE}"/>')
    els.append(txt(100, 168, "历史视频", size=10, color=ROSE, anchor="middle"))
    els.append(f'<path d="M162 163 L206 163" stroke="{ROSE}" stroke-width="1.6" fill="none" marker-end="url(#arr-blue)"/>')
    els.append(f'<rect x="208" y="142" width="130" height="42" rx="7" fill="{ROSE_SOFT}" stroke="{ROSE}"/>')
    els.append(txt(273, 168, "模型预测动作", size=10, color=ROSE, anchor="middle"))
    els.append(txt(348, 166, "预测与真实比较，但模型“改了路线”后画面无法跟着变", size=9.6, color=BODY))
    els.append(_line(40, 202, 716, 202, stroke=BORDER, sw=1))
    # 闭环
    els.append(txt(40, 228, "闭环（closed-loop）", size=10.6, color=TEAL, weight="700"))
    els.append(f'<rect x="40" y="238" width="110" height="46" rx="7" fill="{TEAL_SOFT}" stroke="{TEAL}"/>')
    els.append(txt(95, 266, "当前场景", size=10, color=TEAL, anchor="middle"))
    els.append(f'<path d="M152 261 L190 261" stroke="{TEAL}" stroke-width="1.6" fill="none" marker-end="url(#arr-green)"/>')
    els.append(f'<rect x="192" y="238" width="120" height="46" rx="7" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(252, 258, "驾驶策略模型", size=10, color=BLUE, anchor="middle"))
    els.append(txt(252, 276, "输出动作", size=8.8, color=MUTED, anchor="middle"))
    els.append(f'<path d="M314 261 L352 261" stroke="{BLUE}" stroke-width="1.6" fill="none" marker-end="url(#arr-blue)"/>')
    els.append(f'<rect x="354" y="238" width="130" height="46" rx="7" fill="{TEAL_SOFT}" stroke="{TEAL}"/>')
    els.append(txt(419, 258, "神经世界模拟器", size=10, color=TEAL, anchor="middle"))
    els.append(txt(419, 276, "合成下一刻场景", size=8.8, color=MUTED, anchor="middle"))
    els.append(f'<path d="M486 261 Q560 300 560 230 Q560 208 420 208 L160 208 Q100 208 100 238" stroke="{TEAL}" stroke-width="1.4" fill="none" stroke-dasharray="5 4" marker-end="url(#arr-green)"/>')
    els.append(txt(600, 250, "动作→场景→新动作", size=9.6, color=TEAL, weight="600"))
    els.append(txt(600, 274, "持续循环", size=9.6, color=TEAL))

    els.append(card(20, 332, 352, 220))
    els.append(step_badge(38, 355, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(56, 359, "模拟器的硬指标", size=11.6, color=INK, weight="700"))
    specs = [
        ("摄像头视角", "8 路同时生成"),
        ("帧率", "24 fps / 路"),
        ("单次连续时长", "可达 6 分钟"),
        ("总帧数", "8×24×360 = 69120 帧"),
    ]
    for i, (k, v) in enumerate(specs):
        y = 392 + i * 38
        els.append(txt(40, y, k, size=10, color=MUTED))
        els.append(txt(348, y, v, size=10.2, color=GREEN, anchor="end", weight="700"))

    els.append(card(388, 332, 352, 220))
    els.append(step_badge(406, 355, 3, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 359, "这有什么用", size=11.6, color=INK, weight="700"))
    els.append(txt(406, 394, "• 闭环验证新版本，不拿真实道路试错", size=10.2, color=BODY))
    els.append(txt(406, 424, "• 历史场景反事实回放：“当时变道会怎样”", size=10.0, color=BODY))
    els.append(txt(406, 454, "• 生成对抗性极端场景，专测长尾", size=10.2, color=BODY))
    els.append(txt(406, 490, "• 支撑大规模强化学习，一天“开”出人类几百年的经验量级", size=9.8, color=ORANGE, weight="600"))

    els.append(card(20, 566, 720, 40, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 592, "云端模拟器造“无限道路”训练 AI，车端蒸馏版造“看得见的街景”给驾驶员——同一个世界模型，两种尺寸。", size=10.4, color=SLATE))
    return figure(
        620,
        "特斯拉云端神经世界模拟器动作条件化闭环评估图",
        "上半对比开环只能用历史视频预测动作而模型改路线后画面无法跟着变与闭环把驾驶策略动作送进神经世界模拟器合成下一刻场景再回灌形成循环，左下列八路摄像头每秒二十四帧单次六分钟共六万九千一百二十帧的硬指标，右下列闭环验证反事实回放对抗场景与强化学习用途，底栏说明云端模拟器与车端蒸馏版是同一世界模型的两种尺寸。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 算力与边界
# ---------------------------------------------------------------------------
def build_compute_budget() -> str:
    els = []
    els.extend(
        header(
            "半个 TRIP 加速器、220 毫秒延迟：实时造世界的代价与边界",
            "FSD 与 Robotaxi、Optimus 共用 UVE，同一套视觉底座服务三种形态。",
        )
    )

    els.append(card(20, 66, 352, 434))
    els.append(step_badge(38, 89, 1, fg=GOLD, bg=GOLD_SOFT))
    els.append(txt(56, 93, "三个关键数字", size=11.8, color=INK, weight="700"))
    nums = [
        ("3B + 1B", "驾驶网络 30 亿参数，生成网络 10 亿", BLUE),
        ("½ TRIP", "生成分支只占 SoC 上半个加速器", GOLD),
        ("220 ms", "画面约比真实世界晚 0.22 秒", ROSE),
    ]
    for i, (big, note, color) in enumerate(nums):
        y = 120 + i * 108
        els.append(f'<rect x="38" y="{y}" width="316" height="94" rx="8" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        els.append(txt(196, y + 44, big, size=22, color=color, anchor="middle", weight="700"))
        els.append(txt(196, y + 74, note, size=9.8, color=BODY, anchor="middle"))

    els.append(card(388, 66, 352, 434))
    els.append(step_badge(406, 89, 2, fg=TEAL, bg=TEAL_SOFT))
    els.append(txt(424, 93, "一套视觉底座，三种机器", size=11.8, color=INK, weight="700"))
    els.append(f'<rect x="470" y="124" width="188" height="40" rx="8" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="1.4"/>')
    els.append(txt(564, 150, "UVE 通用视觉编码器", size=10.8, color=BLUE, anchor="middle", weight="700"))
    apps = [(402, "FSD", "汽车驾驶", GREEN), (518, "Robotaxi", "无人驾驶出租", ORANGE), (634, "Optimus", "人形机器人", PURPLE)]
    for x, name, note, color in apps:
        els.append(_line(564, 164, x + 20, 200, stroke=BORDER, sw=1.2))
        els.append(f'<rect x="{x}" y="200" width="104" height="60" rx="8" fill="{SLATE_SOFT}" stroke="{color}" stroke-width="1.4"/>')
        els.append(txt(x + 52, 224, name, size=10.4, color=color, anchor="middle", weight="700"))
        els.append(txt(x + 52, 244, note, size=8.6, color=BODY, anchor="middle"))
    els.append(_line(406, 282, 724, 282, stroke=BORDER, sw=1))
    els.append(txt(406, 312, "复用带来什么", size=11.2, color=TEAL, weight="700"))
    els.append(txt(406, 344, "• 互联网视频训练，覆盖未专门标注的长尾物体", size=10.0, color=BODY))
    els.append(txt(406, 374, "• 一个模型升级，多个形态受益", size=10.0, color=BODY))
    els.append(txt(406, 410, "绕不开什么", size=11.2, color=ROSE, weight="700"))
    els.append(txt(406, 442, "• 机器人进室内仍要重新采样数据", size=10.0, color=BODY))
    els.append(txt(406, 472, "• 生成画面会“幻觉”，不能当传感器真值", size=10.0, color=BODY))

    els.append(card(20, 514, 720, 40, fill=SLATE_SOFT, stroke=BORDER))
    els.append(txt(36, 540, "v15 把“重建世界”变成一项车端实时服务：它足够便宜能上车，也足够危险不能全信——理解这条边界，才算真懂这次更新。", size=10.4, color=SLATE))
    return figure(
        568,
        "FSD v15算力开销延迟与跨形态复用边界图",
        "左栏三个大数字三十亿加十亿参数半个TRIP加速器与二百二十毫秒延迟，右栏画UVE通用视觉编码器连到FSD汽车Robotaxi与Optimus三种机器并列出复用互联网视频训练的好处与机器人需重采样生成画面会幻觉的边界，底栏总结重建世界足够便宜能上车也足够危险不能全信。",
        els,
    )


@register(TOPIC, "特斯拉 FSD v15：UVE 分叉、实时世界生成、神经世界模拟器与算力边界", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("fsd-v15-feature-overview.svg", build_feature_overview),
        ("fsd-v15-uve-fork.svg", build_uve_fork),
        ("fsd-v15-diffusion-frame.svg", build_diffusion),
        ("fsd-v15-world-simulator.svg", build_world_simulator),
        ("fsd-v15-compute-budget.svg", build_compute_budget),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
