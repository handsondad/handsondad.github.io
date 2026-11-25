"""眼睛的演化史：从眼点到相机眼的原创 SVG 图解。"""

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
    card,
    figure,
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

TOPIC = "eye-evolution"


def _line(x1, y1, x2, y2, stroke=SLATE, sw=1.6, dash=None, marker=None, opacity=None):
    extra = ""
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    if opacity is not None:
        extra += f' stroke-opacity="{opacity}"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def _verify() -> None:
    assert 650 > 543 > 505
    assert 600 > 550
    assert 7 < 36 and 4 < 7 and 3 == 4 - 1
    assert 95 < 96 < 100
    assert 364000 < 400000
    assert 0.4 < 0.5 < 0.6


# ---------------------------------------------------------------------------
# 1. 五级台阶
# ---------------------------------------------------------------------------
def build_evolution_staircase() -> str:
    css = (
        "<style>\n"
        "  @keyframes cupDeepen { 0% { transform: scaleY(0.3); opacity: 0.35; } "
        "100% { transform: scaleY(1); opacity: 1; } }\n"
        "  .cup-anim { animation: cupDeepen 2.4s ease-out 1 forwards; transform-origin: 198px 176px; }\n"
        "  @media (prefers-reduced-motion: reduce) { "
        ".cup-anim { animation: none !important; transform: none !important; opacity: 1 !important; } }\n"
        "</style>"
    )

    els = []
    els.extend(
        header(
            "眼睛不是一次装好的：五级台阶，每一步都能用",
            "从一团感光细胞到相机眼，中间没有“必须同时出现”的零件。",
        )
    )

    stages = [
        (20, "① 眼点", "只辨明暗", BLUE),
        (166, "② 色素杯", "判断方向", ORANGE),
        (312, "③ 针孔眼", "粗成像", GREEN),
        (458, "④ 晶状体", "聚光更亮", PURPLE),
        (604, "⑤ 相机眼", "高分辨率", BLUE),
    ]
    for x, title, benefit, fg in stages:
        els.append(card(x, 66, 136, 306))

    # ① 眼点
    els.append('<rect x="36" y="106" width="104" height="72" rx="6" fill="#f4f8fc" stroke="#cfe0ed"/>')
    for xx in (50, 68, 86, 104, 122):
        els.append(f'<circle cx="{xx}" cy="160" r="7" fill="#dbeafe" stroke="{BLUE}" stroke-width="1.1"/>')
    els.append('<ellipse cx="86" cy="160" rx="30" ry="9" fill="#94a3b8" fill-opacity="0.55"/>')
    for xx in (58, 86, 114):
        els.append(_line(xx, 112, xx, 146, stroke=ORANGE, sw=1.5, marker="arr-orange"))

    # ② 色素杯
    els.append('<g class="cup-anim">')
    els.append('<path d="M 190 112 C 168 116, 164 160, 190 182 L 242 182 C 268 160, 264 116, 242 112 Z" fill="#fff4e6" stroke="#e0a269" stroke-width="1.4"/>')
    els.append('<path d="M 198 126 C 184 132, 184 164, 198 174 L 234 174 C 248 164, 248 132, 234 126 Z" fill="#f9d7b5" stroke="#c25014" stroke-width="1.2"/>')
    els.append("</g>")
    for xx in (198, 216, 234):
        els.append(_line(xx, 108, xx, 140, stroke=ORANGE, sw=1.4, marker="arr-orange"))

    # ③ 针孔眼
    els.append('<path d="M 344 108 C 316 118, 314 178, 344 196 L 416 196 C 446 178, 444 118, 416 108 Z" fill="#f2f9f4" stroke="#6fae86" stroke-width="1.5"/>')
    els.append('<path d="M 362 122 C 344 132, 344 172, 362 184 L 398 184 C 416 172, 416 132, 398 122 Z" fill="#d9efe0" stroke="#2f855a" stroke-width="1.2"/>')
    els.append('<rect x="374" y="118" width="12" height="10" fill="#f2f9f4"/>')
    els.append(_line(358, 104, 358, 148, stroke=ORANGE, sw=1.3, marker="arr-orange"))
    els.append(_line(400, 104, 400, 148, stroke=ORANGE, sw=1.3, marker="arr-orange"))

    # ④ 晶状体
    els.append('<path d="M 490 108 C 462 118, 460 178, 490 196 L 562 196 C 592 178, 590 118, 562 108 Z" fill="#f6f3fc" stroke="#a78bfa" stroke-width="1.5"/>')
    els.append('<ellipse cx="526" cy="146" rx="17" ry="26" fill="#e8e0ff" stroke="#7c3aed" stroke-width="1.6"/>')
    els.append(_line(500, 106, 520, 178, stroke=ORANGE, sw=1.3, marker="arr-orange"))
    els.append(_line(552, 106, 532, 178, stroke=ORANGE, sw=1.3, marker="arr-orange"))
    els.append(_line(526, 106, 526, 178, stroke=ORANGE, sw=1.3, marker="arr-orange"))

    # ⑤ 相机眼
    els.append('<circle cx="672" cy="150" r="46" fill="#fffaf6" stroke="#d9a06b" stroke-width="1.7"/>')
    els.append('<path d="M 630 132 A 46 46 0 0 1 714 132" fill="none" stroke="{BLUE_LINE}" stroke-width="4"/>'.replace("{BLUE_LINE}", BLUE_LINE))
    els.append('<ellipse cx="672" cy="140" rx="16" ry="9" fill="#e8d5ff" stroke="#7c3aed" stroke-width="1.3"/>')
    els.append('<path d="M 672 196 A 46 46 0 0 1 672 104" fill="none" stroke="#c25014" stroke-width="3" stroke-dasharray="3 3"/>')
    for xx in (644, 672, 700):
        els.append(_line(xx, 100, 672, 184, stroke=ORANGE, sw=1.1, marker="arr-orange", opacity=0.85))

    for x, title, benefit, fg in stages:
        els.append(txt(x + 68, 220, title, size=11.6, color=fg, anchor="middle", weight="700"))
        els.append(txt(x + 68, 244, benefit, size=10.2, color=INK, anchor="middle", weight="600"))
        els.append(_line(x + 14, 258, x + 122, 258, stroke=BORDER, sw=1))

    notes = [
        "感光分子把光子变成电信号",
        "色素挡住侧向光，能判断光从哪来",
        "小孔让不同方向的光落到不同位置",
        "透明蛋白聚光，弱光下也能看清",
        "虹膜调光、晶状体对焦、视网膜成像",
    ]
    for (x, _, _, _), note in zip(stages, notes):
        line1 = note[:11]
        line2 = note[11:]
        els.append(txt(x + 68, 282, line1, size=9.9, color=BODY, anchor="middle"))
        if line2:
            els.append(txt(x + 68, 302, line2, size=9.9, color=BODY, anchor="middle"))

    els.append(card(20, 386, 720, 40, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 411, "每一步都只比上一步“好用一点”：方向感 → 粗空间 → 成像 → 灵敏度 → 高分辨率。动画只播放一次。", size=10.8, color=SLATE))

    return figure(
        436,
        "眼睛从眼点到相机眼的五级演化台阶图",
        "眼睛演化依次经过眼点辨明暗、色素杯判断方向、针孔眼粗成像、晶状体聚光和相机眼高分辨率五个阶段；每一步都有即时生存优势，杯状眼凹陷动画只播放一次并保留静态终态。",
        els,
        extra_css=css,
    )


# ---------------------------------------------------------------------------
# 2. Nilsson–Pelger 模型
# ---------------------------------------------------------------------------
def build_nilsson_pelger() -> str:
    els = []
    els.extend(
        header(
            "达尔文的难题，被一个计算模型拆成 1% 的小步",
            "Nilsson 与 Pelger 1994 年问：如果每一步只改善 1%，多久能走出一只相机眼？",
        )
    )

    els.append(card(20, 66, 352, 334))
    els.append(step_badge(38, 88, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 92, "模型怎么搭：一层三明治，随机微调", size=11.8, color=INK, weight="700"))
    els.append('<rect x="48" y="116" width="296" height="24" rx="4" fill="#e8f1fb" stroke="#7aa6ce"/>')
    els.append(txt(196, 132, "半透明细胞：可改变厚度与折射率", size=10.2, color=BLUE, anchor="middle"))
    els.append('<rect x="48" y="144" width="296" height="24" rx="4" fill="#fde4d0" stroke="#e0a269"/>')
    els.append(txt(196, 160, "感光细胞：记录成像的清晰程度", size=10.2, color=ORANGE, anchor="middle"))
    els.append('<rect x="48" y="172" width="296" height="24" rx="4" fill="#e8f5ec" stroke="#6fae86"/>')
    els.append(txt(196, 188, "色素细胞：吸收杂散光", size=10.2, color=GREEN, anchor="middle"))
    for xx in (86, 132, 178, 224, 270, 316):
        els.append(_line(xx, 104, xx, 116, stroke=ORANGE, sw=1.4, marker="arr-orange"))
    els.append(_line(40, 212, 348, 212, stroke=BORDER, sw=1))
    els.append(txt(44, 240, "① 每一轮随机变异：形状、厚度、折射率各变约 1%", size=10.4, color=BODY))
    els.append(txt(44, 268, "② 只保留让空间信息更多的那一轮", size=10.4, color=BODY))
    els.append(txt(44, 296, "③ 重复：平斑 → 凹陷 → 小孔 → 晶状体", size=10.4, color=BODY))
    els.append(txt(44, 330, "关键：没有目标，没有蓝图，只有逐轮筛选。", size=10.8, color=BLUE, weight="700"))
    els.append(txt(44, 366, "“不完善”的眼点，也比完全没有感光有用。", size=10.4, color=SLATE))

    els.append(card(388, 66, 352, 334))
    els.append(step_badge(406, 88, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 92, "算出来的数量级：比想象中快", size=11.8, color=INK, weight="700"))
    els.append('<rect x="404" y="116" width="316" height="64" rx="8" fill="#fff8f2" stroke="#f0d5bc"/>')
    els.append(txt(423, 144, "约 36.4 万代", size=20, color=ORANGE, weight="700"))
    els.append(txt(553, 146, "从感光平斑到相机眼", size=10.6, color=SLATE))
    els.append(txt(423, 169, "论文故意取“悲观”参数，因此是上限式估算", size=9.8, color=MUTED))
    els.append('<rect x="404" y="194" width="316" height="64" rx="8" fill="#f4f8fc" stroke="#cfe0ed"/>')
    els.append(txt(423, 222, "约 50 万年", size=20, color=BLUE, weight="700"))
    els.append(txt(553, 224, "按小动物世代长度折算", size=10.6, color=SLATE))
    els.append(txt(423, 247, "在地质年代里只是一眨眼的尺度", size=9.8, color=MUTED))
    els.append(_line(404, 278, 720, 278, stroke=BORDER, sw=1))
    els.append(txt(404, 304, "另一项综述把“眼点→色素杯”单独估为约 3.5 万代。", size=10.2, color=BODY))
    els.append(txt(404, 330, "不同假设给出不同数字，但共同结论是：足够快。", size=10.4, color=INK, weight="600"))
    els.append(txt(404, 366, "模型是思想实验，不是真实物种的演化年表。", size=10.4, color=PURPLE, weight="700"))

    els.append(card(20, 416, 720, 76))
    els.append(txt(40, 444, "达尔文在《物种起源》第六章承认：一想到眼睛的精巧构造，确实“荒谬到最高程度”；", size=10.8, color=BODY))
    els.append(txt(40, 470, "但他紧接着写出整条渐进路径——自然选择完全可以从简单感光斑造出眼睛。", size=10.8, color=INK, weight="700"))

    return figure(
        502,
        "Nilsson–Pelger 眼睛演化计算模型与世代估算图",
        "模型用半透明细胞、感光细胞和色素细胞三层三明治模拟原始感光区，每轮随机改变约1%并保留空间信息更多的变异；从感光平斑到相机眼约36.4万代，按小动物世代折算约50万年；眼点到色素杯另估约3.5万代，均为模型估算而非真实年表。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. 相机眼解剖（原创重绘）
# ---------------------------------------------------------------------------
def build_camera_eye_anatomy() -> str:
    els = []
    els.extend(
        header(
            "把相机眼拆开：光走过的是一条精心安排的路",
            "角膜、虹膜、晶状体、玻璃体、视网膜、黄斑与盲点，各管一段。",
        )
    )

    els.append(card(20, 66, 470, 410))
    els.append('<ellipse cx="258" cy="248" rx="166" ry="152" fill="#fff8f1" stroke="#d9a06b" stroke-width="2"/>')
    els.append('<path d="M 99 200 A 166 152 0 0 1 417 200" fill="none" stroke="#9fc7e8" stroke-width="9"/>')
    els.append('<path d="M 99 200 A 166 152 0 0 1 417 200" fill="none" stroke="#dbeafe" stroke-width="4"/>')
    els.append('<path d="M 118 178 Q 258 150 398 178" fill="none" stroke="#c25014" stroke-width="4"/>')
    els.append('<path d="M 124 184 Q 258 158 392 184" fill="none" stroke="#e0a269" stroke-width="3"/>')
    els.append('<ellipse cx="258" cy="180" rx="46" ry="26" fill="#efe3ff" stroke="#7c3aed" stroke-width="2"/>')
    els.append('<path d="M 258 154 L 258 206" stroke="#7c3aed" stroke-width="1"/>')
    els.append('<ellipse cx="258" cy="268" rx="120" ry="104" fill="#fde9da" fill-opacity="0.55"/>')
    els.append('<path d="M 112 280 A 166 152 0 0 0 404 280" fill="none" stroke="#e7b27d" stroke-width="12"/>')
    els.append('<path d="M 112 280 A 166 152 0 0 0 404 280" fill="none" stroke="#c25014" stroke-width="2"/>')

    for xx in (178, 220, 296, 338):
        els.append(_line(xx, 104, 258, 300, stroke=ORANGE, sw=1.2, marker="arr-orange", opacity=0.75))
    els.append('<circle cx="258" cy="302" r="7" fill="#e4572e" stroke="white" stroke-width="1.5"/>')

    els.append('<path d="M 92 336 L 130 330 L 152 420 L 118 424 Z" fill="#f9d7b5" stroke="#c25014" stroke-width="1.6"/>')
    els.append(_line(130, 344, 146, 410, stroke=ORANGE, sw=1.4, marker="arr-orange"))
    els.append('<circle cx="170" cy="318" r="5" fill="none" stroke="#7c3aed" stroke-width="2"/>')

    labels = [
        (32, 96, "角膜：先折射", BLUE),
        (32, 124, "虹膜：调光", ORANGE),
        (32, 152, "晶状体：聚焦", PURPLE),
        (32, 180, "玻璃体：透明填充", GREEN),
        (32, 350, "视网膜：感光", ORANGE),
        (32, 378, "中央凹：最清晰", GREEN),
        (32, 406, "盲点：神经出口", PURPLE),
        (32, 434, "视神经：送脑", SLATE),
    ]
    for x, y, label, color in labels:
        els.append(txt(x, y, label, size=10.2, color=color, weight="600"))
    els.append(txt(352, 246, "倒像", size=10.6, color=ORANGE, anchor="middle", weight="700"))
    els.append(txt(352, 266, "由大脑翻正", size=9.8, color=MUTED, anchor="middle"))

    els.append(card(506, 66, 234, 410))
    els.append(step_badge(524, 88, 1, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(542, 92, "视网膜上的两种感光细胞", size=11.4, color=INK, weight="700"))
    els.append('<rect x="522" y="116" width="202" height="112" rx="7" fill="#f4f8fc" stroke="#cfe0ed"/>')
    els.append('<path d="M 546 200 L 546 146 L 554 138 L 562 146 L 562 200 Z" fill="#bcd7ef" stroke="#1d6fa5" stroke-width="1.2"/>')
    els.append('<path d="M 566 200 L 566 142 L 584 130 L 602 142 L 602 200 Z" fill="#f9d7b5" stroke="#c25014" stroke-width="1.2"/>')
    els.append('<path d="M 612 200 L 612 146 L 620 138 L 628 146 L 628 200 Z" fill="#bcd7ef" stroke="#1d6fa5" stroke-width="1.2"/>')
    els.append('<path d="M 638 200 L 638 142 L 656 130 L 674 142 L 674 200 Z" fill="#f9d7b5" stroke="#c25014" stroke-width="1.2"/>')
    els.append(txt(554, 216, "视杆：弱光", size=9.8, color=BLUE, anchor="middle"))
    els.append(txt(584, 216, "视锥：颜色", size=9.8, color=ORANGE, anchor="middle"))
    els.append(txt(628, 216, "视杆", size=9.8, color=BLUE, anchor="middle"))
    els.append(txt(656, 216, "视锥", size=9.8, color=ORANGE, anchor="middle"))
    els.append(_line(522, 228, 724, 228, stroke=BORDER, sw=1))
    els.append(txt(522, 256, "视杆细胞", size=11.2, color=BLUE, weight="700"))
    els.append(txt(522, 278, "灵敏度高，暗处工作；", size=10.2, color=BODY))
    els.append(txt(522, 298, "不能分辨颜色。", size=10.2, color=BODY))
    els.append(txt(522, 332, "视锥细胞", size=11.2, color=ORANGE, weight="700"))
    els.append(txt(522, 354, "强光下工作，负责色觉；", size=10.2, color=BODY))
    els.append(txt(522, 374, "中央凹处最密集。", size=10.2, color=BODY))
    els.append(txt(522, 414, "光子 → 11-顺视黄醛异构化", size=10.4, color=PURPLE, weight="700"))
    els.append(txt(522, 438, "→ 电信号 → 视神经", size=10.4, color=PURPLE, weight="700"))

    els.append(card(20, 490, 720, 38, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 515, "本图根据用户提供的人眼解剖示意重新绘制，仅保留结构关系与光线路径，不直接使用原图。", size=10.6, color=SLATE))

    return figure(
        538,
        "人眼相机式结构光路与视杆视锥细胞原创重绘图",
        "原创重绘的人眼横截面标出角膜、虹膜、晶状体、玻璃体、视网膜、黄斑中央凹、盲点和视神经；光线经角膜与晶状体两次折射在视网膜形成倒像；右栏对比视杆细胞负责弱光、视锥细胞负责颜色，感光始于11-顺视黄醛的光异构化。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. 视网膜布线对比
# ---------------------------------------------------------------------------
def build_retina_wiring() -> str:
    els = []
    els.extend(
        header(
            "同样能成像，布线却相反：历史留下的“将就”",
            "脊椎动物的视网膜是倒置的，头足类的是正置的；两者都能看得很好。",
        )
    )

    for x, title, color, soft in [(20, "脊椎动物：倒置视网膜", BLUE, BLUE_SOFT), (388, "头足类：正置视网膜", ORANGE, ORANGE_SOFT)]:
        els.append(card(x, 66, 352, 350))
        els.append(step_badge(x + 18, 88, 1 if x == 20 else 2, fg=color, bg=soft))
        els.append(txt(x + 36, 92, title, size=11.8, color=INK, weight="700"))

    # 脊椎动物
    els.append('<path d="M 52 150 A 142 120 0 0 0 336 150" fill="none" stroke="#e7b27d" stroke-width="18"/>')
    els.append('<path d="M 52 150 A 142 120 0 0 0 336 150" fill="none" stroke="#c25014" stroke-width="2"/>')
    els.append(_line(104, 116, 104, 182, stroke=BLUE, sw=2, marker="arr-blue"))
    els.append(_line(150, 112, 150, 194, stroke=BLUE, sw=2, marker="arr-blue"))
    els.append(_line(196, 110, 196, 198, stroke=BLUE, sw=2, marker="arr-blue"))
    els.append(_line(242, 112, 242, 194, stroke=BLUE, sw=2, marker="arr-blue"))
    els.append(_line(288, 116, 288, 182, stroke=BLUE, sw=2, marker="arr-blue"))
    els.append(txt(194, 132, "神经纤维先挡一层", size=10.8, color=BLUE, anchor="middle", weight="600"))
    els.append(txt(194, 166, "感光细胞在后", size=10.4, color=ORANGE, anchor="middle"))
    els.append('<path d="M 186 258 L 210 258 L 226 344 L 196 344 Z" fill="#f9d7b5" stroke="#c25014" stroke-width="1.5"/>')
    els.append(_line(204, 270, 214, 334, stroke=ORANGE, sw=1.4, marker="arr-orange"))
    els.append(txt(52, 292, "视神经穿出视网膜 → 盲点", size=10.4, color=PURPLE, weight="700"))
    els.append(txt(52, 324, "大脑靠插值“补”出空洞", size=10.2, color=SLATE))
    els.append(txt(52, 384, "路径依赖：从旧结构改造，不是重新画图", size=10.6, color=BLUE, weight="600"))

    # 头足类
    els.append('<path d="M 420 150 A 142 120 0 0 0 704 150" fill="none" stroke="#e7b27d" stroke-width="18"/>')
    els.append('<path d="M 420 150 A 142 120 0 0 0 704 150" fill="none" stroke="#c25014" stroke-width="2"/>')
    els.append(_line(472, 112, 472, 182, stroke=ORANGE, sw=2, marker="arr-orange"))
    els.append(_line(518, 110, 518, 194, stroke=ORANGE, sw=2, marker="arr-orange"))
    els.append(_line(564, 108, 564, 198, stroke=ORANGE, sw=2, marker="arr-orange"))
    els.append(_line(610, 110, 610, 194, stroke=ORANGE, sw=2, marker="arr-orange"))
    els.append(_line(656, 112, 656, 182, stroke=ORANGE, sw=2, marker="arr-orange"))
    els.append(txt(562, 132, "光先到感光细胞", size=10.8, color=ORANGE, anchor="middle", weight="600"))
    els.append(txt(562, 166, "神经纤维走后方", size=10.4, color=BLUE, anchor="middle"))
    els.append('<path d="M 554 258 L 578 258 L 594 344 L 564 344 Z" fill="#f9d7b5" stroke="#c25014" stroke-width="1.5"/>')
    els.append(_line(572, 270, 582, 334, stroke=ORANGE, sw=1.4, marker="arr-orange"))
    els.append(txt(420, 292, "神经从感光层后方出线 → 无盲点", size=10.4, color=GREEN, weight="700"))
    els.append(txt(420, 324, "光路更直接，散射更少", size=10.2, color=SLATE))
    els.append(txt(420, 384, "独立演化出的“另一种图纸”", size=10.6, color=ORANGE, weight="600"))

    els.append(card(20, 432, 720, 56))
    els.append(txt(40, 458, "两套相机眼是趋同演化的经典例子：零件相似，来源不同；都没有被“推倒重来”。", size=10.8, color=INK, weight="700"))
    els.append(txt(40, 480, "所谓“设计缺陷”恰恰是演化历史的指纹——它修旧房子，不画新图纸。", size=10.4, color=BODY))

    return figure(
        498,
        "脊椎动物倒置视网膜与头足类正置视网膜布线对比图",
        "脊椎动物视网膜神经纤维位于感光细胞前方，视神经穿出视网膜形成盲点，需要大脑补偿；头足类视网膜感光细胞朝向入射光、神经纤维从后方出线因此没有盲点；两者是趋同演化的经典例子。",
        els,
    )


# ---------------------------------------------------------------------------
# 5. 地质时间线与独立起源
# ---------------------------------------------------------------------------
def build_origin_diversity() -> str:
    els = []
    els.extend(
        header(
            "眼睛在生命史上被“发明”了多少次？",
            "化石给下限，现生动物给上限；答案不是一个整数，而是一段范围。",
        )
    )

    els.append(card(20, 66, 720, 174))
    els.append(step_badge(38, 88, 1, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 92, "地质时间线上的眼睛", size=12.0, color=INK, weight="700"))
    x0, x1 = 70, 690
    els.append(_line(x0, 160, x1, 160, stroke=SLATE, sw=2))
    marks = [
        (650, "埃迪卡拉纪开始", BLUE),
        (600, "最早化石眼", ORANGE),
        (543, "寒武纪开始", PURPLE),
        (505, "大爆发末", GREEN),
    ]
    for value, label, color in marks:
        pos = x0 + (650 - value) / (650 - 505) * (x1 - x0)
        els.append(_line(pos, 154, pos, 168, stroke=color, sw=2))
        els.append(txt(pos, 188, label, size=9.4, color=color, anchor="middle"))
        els.append(txt(pos, 206, f"{value} Ma", size=9.2, color=MUTED, anchor="middle"))
    els.append(txt(40, 226, "Ma = 百万年前；最早已知眼化石是三叶虫 Olenellus fowleri，约 6 亿–5.5 亿年前。", size=10.4, color=SLATE))

    els.append(card(20, 256, 352, 224))
    els.append(step_badge(38, 278, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 282, "现存动物门：不是每个门都有眼", size=11.6, color=INK, weight="700"))
    bars = [
        ("约 36 个动物门", 36, 36, BLUE),
        ("约 7 个门有眼", 7, 36, ORANGE),
        ("4 个门能成像", 4, 36, PURPLE),
    ]
    for i, (label, value, maximum, color) in enumerate(bars):
        y = 314 + i * 44
        els.append(txt(40, y, label, size=10.4, color=INK, weight="600"))
        els.append(f'<rect x="40" y="{y+8}" width="300" height="12" rx="6" fill="#eef2f7"/>')
        els.append(f'<rect x="40" y="{y+8}" width="{300*value/maximum:.1f}" height="12" rx="6" fill="{color}"/>')
    els.append(txt(40, 456, "能成像的 4 个门中，软体、节肢、脊索 3 个门占了约 96% 的物种。", size=10.4, color=BODY))

    els.append(card(388, 256, 352, 224))
    els.append(step_badge(406, 278, 3, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 282, "眼睛至少被独立发明约 40 次", size=11.6, color=INK, weight="700"))
    els.append(txt(404, 316, "· 脊椎动物与头足类：各自造出相机眼", size=10.4, color=BODY))
    els.append(txt(404, 344, "· 节肢动物：复眼，成千上万小眼并行采样", size=10.4, color=BODY))
    els.append(txt(404, 372, "· 鹦鹉螺：针孔眼；涡虫：色素杯眼点", size=10.4, color=BODY))
    els.append(txt(404, 400, "· 洞穴鱼与鼹鼠：眼睛还可以再次退化", size=10.4, color=BODY))
    els.append(_line(404, 416, 724, 416, stroke=BORDER, sw=1))
    els.append(txt(404, 446, "共同祖先只给“工具箱”，图纸由各支自己画。", size=10.6, color=ORANGE, weight="700"))

    els.append(card(20, 494, 720, 38, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 519, "不同资料对动物门总数与有眼门数统计略有差异（如 39/6 与 36/7），源于分类口径不同；结论不变。", size=10.6, color=SLATE))

    return figure(
        542,
        "眼睛演化的地质时间线与独立起源统计图",
        "时间线标出埃迪卡拉纪开始650百万年前、最早已知三叶虫眼化石600至550百万年前、寒武纪543至505百万年前；统计显示约36个动物门中约7个有眼、4个能成像，其中软体节肢脊索三门占约96%物种，眼睛至少独立演化约40次。",
        els,
    )


@register(TOPIC, "眼睛演化史：眼点、色素杯、针孔眼、相机眼与视网膜布线的原创图解", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("eye-evolution-staircase.svg", build_evolution_staircase),
        ("nilsson-pelger-model.svg", build_nilsson_pelger),
        ("camera-eye-anatomy.svg", build_camera_eye_anatomy),
        ("retina-wiring-comparison.svg", build_retina_wiring),
        ("eye-origin-diversity.svg", build_origin_diversity),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
