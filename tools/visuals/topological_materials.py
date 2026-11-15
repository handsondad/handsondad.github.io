"""
Visuals for '通俗介绍拓扑电子材料（凝聚态物理的突破）'
(Accessible & Rigorous Visual Guide to Topological Electronic Materials:
1. Topology Intuition [Bun g=0 / Bagel-Mug g=1 / Pretzel g=2] & Exact Quantum Hall Resistance Steps [R_K = 25,812.807 Ω / ν],
2. Ordinary Wire Pinball Scattering vs Topological Spin-Momentum-Locked Highway & QAHE 1-Way Edge [1-shot CSS animation],
3. How Heavy Atoms Tie a 'Möbius Knot' in Electron Bands: BHZ Band Inversion & Bulk-Boundary Dirac Cone,
4. The Three Flagship Families: 3D Topological Insulators, Magnetic QAHE, and Weyl Semimetals with Open 'Fermi Arcs',
5. The 2019 Nature Census Shockwave [8,056 / 39,519 Non-Magnetic Materials] & Honest Engineering Bottlenecks vs Silicon Chips).

Generates 5 original 760px Chinese SVG diagrams in assets/images/topological-materials/
with verified SI quantum constants, BHZ dispersion curves, and Nature 2019 catalogue assertions.
"""
from __future__ import annotations

import math

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
    header,
    pill,
    register,
    step_badge,
    txt,
    write_svg,
)

TOPIC = "topological-materials"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#d97706"
AMBER_SOFT = "#fffbeb"


def _line(x1, y1, x2, y2, stroke=INK, sw=1.6, dash=None, marker=None, cls=None):
    extra = ""
    if cls:
        extra += f' class="{cls}"'
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    )


def _markers() -> str:
    return f"""
    <marker id="arr-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{RED}"/>
    </marker>
    <marker id="arr-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{PURPLE}"/>
    </marker>
    <marker id="arr-slate" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{SLATE}"/>
    </marker>
    """


# ---------------------------------------------------------------------------
# 1. Coffee Cup / Donut Genus & Exact Quantum Hall Plateaus (760 x 505)
# ---------------------------------------------------------------------------
def build_coffee_cup_and_qhe() -> str:
    # Exact 2019 SI constants
    h_planck = 6.62607015e-34
    e_charge = 1.602176634e-19
    r_klitzing = h_planck / (e_charge ** 2)
    assert abs(r_klitzing - 25812.8074593) < 1e-4

    W, H = 760, 505
    els = header(
        "什么是“拓扑保护”？从面包洞数到十亿分之一精度的量子台阶",
        "连续揉捏改不了整数“洞数” g —— 电子波函数的拓扑数 C 同样锁死了霍尔电阻台阶（2016 诺奖核心）",
    )

    # Left Card: Genus g = 0, 1, 2
    els.append(card(16, 68, 350, 420, fill="#ffffff"))
    els.append(step_badge(36, 92, 1, BLUE))
    els.append(txt(56, 97, "数学直觉：橡皮泥怎么捏，“洞数”都是整数", size=12.4, weight="700", color=BLUE))

    # Row g = 0: Bun / Sphere
    els.append('<rect x="30" y="114" width="322" height="84" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')
    els.append('<ellipse cx="78" cy="156" rx="30" ry="22" fill="#fde68a" stroke="#d97706" stroke-width="2"/>')
    els.append('<path d="M 60 152 Q 78 140 96 152" fill="none" stroke="#b45309" stroke-width="1.6"/>')
    els.append(txt(124, 142, "圆面包 / 实心球：洞数 g = 0", size=11.0, weight="700", color=INK))
    els.append(txt(124, 162, "压扁成盘子、捏成碗，只要不戳破，", size=9.9, color=SLATE))
    els.append(txt(124, 180, "洞数永远等于 0（绝不会冒出 0.3 个洞！）", size=9.9, color=AMBER, weight="600"))

    # Row g = 1: Bagel <-> Coffee Mug
    els.append('<rect x="30" y="208" width="322" height="96" rx="10" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.4"/>')
    # Bagel
    els.append('<circle cx="62" cy="256" r="22" fill="#fed7aa" stroke="#ea580c" stroke-width="2"/>')
    els.append('<circle cx="62" cy="256" r="8" fill="#eff6ff" stroke="#ea580c" stroke-width="2"/>')
    els.append(txt(100, 260, "⇄", size=15.0, weight="700", color=BLUE, anchor="middle"))
    # Mug (cup body + handle with 1 hole)
    els.append('<rect x="116" y="238" width="26" height="34" rx="4" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="1.8"/>')
    els.append('<path d="M 142 244 C 156 244, 156 266, 142 266" fill="none" stroke="#1d4ed8" stroke-width="3.2"/>')
    els.append(txt(166, 236, "甜甜圈 ⇄ 马克杯：g = 1", size=11.0, weight="700", color=BLUE))
    els.append(txt(166, 256, "杯身凹陷能慢慢抚平，唯独杯把", size=9.9, color=SLATE))
    els.append(txt(166, 274, "上的 1 个洞跟甜甜圈拓扑等价！", size=9.9, color=BLUE, weight="600"))
    els.append(txt(166, 292, "想变 g=0？除非暴力撕裂杯把！", size=9.8, color=RED, weight="700"))

    # Row g = 2: Double-hole pretzel
    els.append('<rect x="30" y="314" width="322" height="82" rx="10" fill="#f5f3ff" stroke="#c4b5fd" stroke-width="1.2"/>')
    els.append('<rect x="42" y="334" width="68" height="40" rx="18" fill="#ddd6fe" stroke="#7c3aed" stroke-width="2"/>')
    els.append('<circle cx="62" cy="354" r="7.5" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.8"/>')
    els.append('<circle cx="90" cy="354" r="7.5" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.8"/>')
    els.append(txt(124, 344, "双孔椒盐卷饼 / 眼镜框：g = 2", size=11.0, weight="700", color=PURPLE))
    els.append(txt(124, 364, "局部凹凸曲率千变万化，但高斯-博内", size=9.9, color=SLATE))
    els.append(txt(124, 382, "全局曲率积分永远锁死整数 2 − 2g！", size=9.9, color=PURPLE, weight="600"))

    # Bottom bridge box in left card
    els.append('<rect x="30" y="406" width="322" height="68" rx="9" fill="#0f172a"/>')
    els.append(txt(191, 428, "索利斯（Thouless, 1982）的天才跨界：", size=10.5, weight="700", color="#fbbf24", anchor="middle"))
    els.append(txt(191, 448, "晶体里电子波函数在动量空间也拧着整数“陈数” C！", size=9.9, color="#f8fafc", anchor="middle"))
    els.append(txt(191, 465, "杂质、形变就像捏橡皮泥，只要能隙不关，C 一步不跳！", size=9.8, color="#93c5fd", anchor="middle"))

    # Right Card: Exact Quantum Hall Effect Staircase (von Klitzing 1980)
    els.append(card(382, 68, 362, 420, fill="#ffffff"))
    els.append(step_badge(402, 92, 2, GREEN, GREEN_SOFT))
    els.append(txt(422, 97, "物理奇迹：无视杂质的“量子霍尔电阻阶梯”", size=12.4, weight="700", color=GREEN))

    # Plot box: B-field on X (from 2 T to 14 T), R_xy on Y (0 to 28 kΩ)
    px0, py0, pw, ph = 436, 132, 286, 224
    els.append(f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')

    def bx(b_tesla: float) -> float:
        return px0 + (b_tesla - 2.0) / 12.0 * pw

    def ry(r_kohm: float) -> float:
        return py0 + ph - (r_kohm / 28.5) * ph

    # Horizontal dashed grid at exact R_K / nu for nu = 1, 2, 3, 4
    plateaus = [
        (1, r_klitzing / 1000.0, 10.6, 13.6, "ν=1 (C=1): 25.813 kΩ"),
        (2, r_klitzing / 2000.0, 5.8, 7.8, "ν=2 (C=2): 12.906 kΩ"),
        (3, r_klitzing / 3000.0, 3.9, 4.9, "ν=3 (C=3): 8.604 kΩ"),
        (4, r_klitzing / 4000.0, 2.8, 3.4, "ν=4 (C=4): 6.453 kΩ"),
    ]
    for nu, rk_val, _, _, _ in plateaus:
        yy = ry(rk_val)
        els.append(_line(px0, yy, px0 + pw, yy, stroke="#e2e8f0", sw=1.1, dash="4,3"))
        els.append(txt(px0 - 6, yy + 3.5, f"{rk_val:.1f}", size=9.8, color=MUTED, anchor="end"))

    els.append(txt(px0 - 8, py0 - 8, "霍尔电阻 R_xy (kΩ)", size=10.0, color=INK, weight="700"))
    els.append(txt(px0 + pw / 2, py0 + ph + 30, "外加磁场强度 B (特斯拉 T) →", size=10.2, color=INK, anchor="middle", weight="700"))
    for b_tick in [2, 5, 8, 11, 14]:
        tx = bx(b_tick)
        els.append(_line(tx, py0 + ph, tx, py0 + ph + 4, stroke=SLATE, sw=1.2))
        els.append(txt(tx, py0 + ph + 14, f"{b_tick}", size=9.8, color=MUTED, anchor="middle"))

    # Classical straight Hall line (dashed slate)
    els.append(_line(bx(2.0), ry(2.0 * 2.15), bx(13.2), ry(13.2 * 2.15), stroke="#94a3b8", sw=1.5, dash="5,4"))
    els.append(txt(bx(9.2), ry(25.2), "经典直线预期", size=9.8, color=MUTED, anchor="end"))

    # Quantum Hall quantized staircase curve
    pts_qhe = [(bx(2.0), ry(4.3)), (bx(2.8), ry(r_klitzing / 4000.0)), (bx(3.4), ry(r_klitzing / 4000.0)),
               (bx(3.9), ry(r_klitzing / 3000.0)), (bx(4.9), ry(r_klitzing / 3000.0)),
               (bx(5.8), ry(r_klitzing / 2000.0)), (bx(7.8), ry(r_klitzing / 2000.0)),
               (bx(10.6), ry(r_klitzing / 1000.0)), (bx(13.8), ry(r_klitzing / 1000.0))]
    d_qhe = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts_qhe)
    els.append(f'<path d="{d_qhe}" fill="none" stroke="{RED}" stroke-width="3.0" stroke-linejoin="round"/>')

    # Longitudinal resistance R_xx (green spikes at transitions, ZERO on plateaus!)
    rxx_pts = []
    for i in range(121):
        b_v = 2.0 + 12.0 * (i / 120.0)
        # Peaks only at transition midpoints: 2.5, 3.65, 5.35, 9.2
        val = (
            2.6 * math.exp(-((b_v - 2.55) / 0.20) ** 2)
            + 3.2 * math.exp(-((b_v - 3.65) / 0.22) ** 2)
            + 4.0 * math.exp(-((b_v - 5.35) / 0.30) ** 2)
            + 5.2 * math.exp(-((b_v - 9.20) / 0.55) ** 2)
        )
        rxx_pts.append(f"{bx(b_v):.1f},{ry(val):.1f}")
    els.append(f'<polyline points="{" ".join(rxx_pts)}" fill="none" stroke="{GREEN}" stroke-width="2.1"/>')
    els.append(txt(bx(12.2), ry(1.6), "纵向电阻 R_xx → 0（无耗散！）", size=9.9, color=GREEN, anchor="middle", weight="700"))

    # Plateau callout labels (carefully spaced vertically!)
    els.append(txt(bx(12.1), ry(r_klitzing / 1000.0) - 9, "C=1: 25,812.8 Ω", size=10.2, color=RED, anchor="middle", weight="700"))
    els.append(txt(bx(6.8), ry(r_klitzing / 2000.0) - 9, "C=2: 12,906.4 Ω", size=10.0, color=RED, anchor="middle", weight="700"))
    els.append(txt(bx(4.4), ry(r_klitzing / 3000.0) - 10, "C=3", size=9.8, color=RED, anchor="middle", weight="700"))

    # Bottom takeaway in right card
    els.append('<rect x="398" y="400" width="330" height="74" rx="9" fill="#f0fdf4" stroke="#86efac" stroke-width="1.3"/>')
    els.append(txt(563, 421, "冯·克利青（1980 发现 / 1985 诺奖）：R_H = h / (C·e²)", size=10.4, weight="700", color=GREEN, anchor="middle"))
    els.append(txt(563, 441, "哪怕芯片脏一点、形状歪一点，台阶精度仍达 10⁻⁹！", size=10.0, color=INK, anchor="middle"))
    els.append(txt(563, 460, "2019 年起，25,812.807 Ω 直接成为国际“欧姆”量子基准。", size=9.9, color=TEAL, anchor="middle", weight="600"))

    return figure(
        H,
        "拓扑不变量洞数与量子霍尔效应精确电阻台阶图",
        "左图对比球面g=0、甜甜圈与马克杯g=1、双孔卷饼g=2在连续形变下洞数不变；右图绘制量子霍尔效应在ν=1,2,3,4处的精确电阻平台25812.8/ν欧姆及纵向电阻归零现象。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 2. Ordinary Wire Pinball vs Spin-Momentum-Locked Highway (760 x 515, animated)
# ---------------------------------------------------------------------------
def build_topological_highway() -> str:
    W, H = 760, 515
    anim_css = """
      @keyframes glideAround {
        0%   { stroke-dashoffset: 260; }
        100% { stroke-dashoffset: 0; }
      }
      @keyframes bounceBack {
        0%   { stroke-dashoffset: 180; }
        100% { stroke-dashoffset: 0; }
      }
      .anim-glide {
        stroke-dasharray: 260;
        stroke-dashoffset: 0;
        animation: glideAround 2.8s ease-out 1 forwards;
      }
      .anim-bounce {
        stroke-dasharray: 180;
        stroke-dashoffset: 0;
        animation: bounceBack 2.2s ease-out 1 forwards;
      }
      @media (prefers-reduced-motion: reduce) {
        .anim-glide, .anim-bounce {
          animation: none !important;
          stroke-dashoffset: 0 !important;
        }
      }
    """
    els = header(
        "为什么叫它“内绝缘、外导电的电子防弹衣”？三种导电车道大比拼",
        "普通铜线像弹珠台乱撞发热；拓扑绝缘体表面“自旋锁死方向”；量子反常霍尔干脆拆掉逆行道！",
    )

    # Band 1: Ordinary Conductor (Pinball scattering)
    els.append(card(16, 68, 728, 126, fill="#fff7ed"))
    els.append(step_badge(36, 92, 1, ORANGE, ORANGE_SOFT))
    els.append(txt(56, 97, "普通金属导体（如铜线）：全员挤在内部跑，撞上杂质就 180° 弹回发热", size=12.2, weight="700", color=ORANGE))

    els.append('<rect x="36" y="110" width="430" height="68" rx="8" fill="#ffedd5" stroke="#fdba74" stroke-width="1.4"/>')
    # Impurities (stones)
    for ix, iy in [(150, 134), (255, 154), (350, 132)]:
        els.append(f'<circle cx="{ix}" cy="{iy}" r="11" fill="#9a3412"/>')
        els.append(txt(ix, iy + 4, "杂", size=9.8, color="#ffffff", anchor="middle", weight="700"))
    # Pinball bounce path
    els.append('<path class="anim-bounce" d="M 54 136 L 136 134 L 88 164 M 170 156 L 242 154 L 198 122 M 274 134 L 336 132 L 296 164" fill="none" stroke="#dc2626" stroke-width="2.4" marker-end="url(#arr-red)"/>')
    els.append(txt(486, 132, "• 去程与返程混在同一条路，随时掉头背散射", size=10.3, color=INK))
    els.append(txt(486, 153, "• 每次乱撞都把电能变成晶格振动（焦耳热 I²R）", size=10.3, color=RED, weight="700"))
    els.append(txt(486, 173, "• 芯片越做越薄，表面粗糙散射让发热雪上加霜", size=10.0, color=SLATE))

    # Band 2: 3D/2D Topological Insulator (Spin-momentum locking!)
    els.append(card(16, 206, 728, 162, fill="#eff6ff"))
    els.append(step_badge(36, 230, 2, BLUE))
    els.append(txt(56, 235, "拓扑绝缘体（如硒化铋 Bi₂Se₃）：内部彻底绝缘，边界“自旋-动量锁死”绕过杂质！", size=12.2, weight="700", color=BLUE))

    # Material slab with top highway, insulating bulk, bottom highway
    els.append('<rect x="36" y="250" width="430" height="102" rx="10" fill="#e2e8f0" stroke="#64748b" stroke-width="1.5"/>')
    els.append(txt(251, 308, "体态内部：绝缘禁区（带隙 ≈ 0.30 eV，室温电子钻不进去）", size=10.2, color=SLATE, anchor="middle", weight="700"))

    # Defect bump on top edge
    els.append('<circle cx="246" cy="264" r="13" fill="#475569"/>')
    els.append(txt(246, 268, "杂", size=9.8, color="#ffffff", anchor="middle", weight="700"))

    # Rightward spin-up lane (blue smooth bypass over/around bump!)
    els.append('<path class="anim-glide" d="M 52 260 L 214 260 Q 246 294 278 260 L 444 260" fill="none" stroke="#1d4ed8" stroke-width="3.0" marker-end="url(#arr-blue)"/>')
    els.append(txt(134, 255, "右行道：只准自旋 ↑", size=9.9, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(364, 255, "绕过杂质继续前进 ↑", size=9.9, color=BLUE, anchor="middle", weight="700"))

    # Leftward spin-down lane (dashed purple on bottom / opposite spin)
    els.append(_line(444, 340, 56, 340, stroke=PURPLE, sw=2.3, dash="6,4", marker="arr-purple"))
    els.append(txt(251, 334, "反向车道：只准自旋 ↓（时间反演伙伴）", size=9.8, color=PURPLE, anchor="middle", weight="600"))

    els.append(txt(486, 268, "• 交规铁律：往右跑必须自旋 ↑，往左跑必须自旋 ↓", size=10.2, color=BLUE, weight="700"))
    els.append(txt(486, 290, "• 撞见非磁性杂质想 180° 掉头？必须把 ↑ 翻成 ↓！", size=10.1, color=INK))
    els.append(txt(486, 312, "• 普通灰尘没有磁性翻不动自旋 → 180° 背散射率 = 0！", size=10.1, color=GREEN, weight="700"))
    els.append(txt(486, 334, "• 哪怕切掉一块角，新表面自动长出导电高速公路", size=10.0, color=SLATE))

    # Band 3: Magnetic TI / Quantum Anomalous Hall (Chiral 1-way highway!)
    els.append(card(16, 380, 728, 120, fill="#f0fdf4"))
    els.append(step_badge(36, 404, 3, GREEN, GREEN_SOFT))
    els.append(txt(56, 409, "磁性拓扑绝缘体（量子反常霍尔效应 QAHE，薛其坤、常翠祖团队 2013 首测）：纯单向零电阻车道！", size=11.9, weight="700", color=GREEN))

    els.append('<rect x="36" y="424" width="430" height="62" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>')
    els.append(txt(251, 460, "磁性体态绝缘（无需外加巨型磁铁！内部磁性自动清退逆行道）", size=10.0, color=TEAL, anchor="middle", weight="700"))
    # Top edge -> right only; Bottom edge -> left only!
    els.append(_line(52, 432, 444, 432, stroke=GREEN, sw=3.0, marker="arr-green"))
    els.append(_line(444, 478, 52, 478, stroke=GREEN, sw=3.0, marker="arr-green"))
    els.append(txt(251, 444, "上边缘只向右 →", size=9.8, color=GREEN, anchor="middle", weight="700"))
    els.append(txt(251, 474, "← 下边缘只向左", size=9.8, color=GREEN, anchor="middle", weight="700"))

    els.append(txt(486, 440, "• 掺入铬(Cr)磁性原子打破时间反演，删掉一半车道", size=10.1, color=INK))
    els.append(txt(486, 462, "• 上边缘连逆行车道都没修，电子想拐弯掉头都没路！", size=10.1, color=GREEN, weight="700"))
    els.append(txt(486, 483, "• 零外磁场下实现 R_xy = h/e²、纵向无耗散传输", size=10.0, color=TEAL, weight="600"))

    return figure(
        H,
        "普通金属铜线与拓扑绝缘体及量子反常霍尔边缘导电通道对比图",
        "第一栏普通铜线电子遇杂质发生180度散射发热；第二栏拓扑绝缘体内部绝缘、表面自旋-动量锁定，电子遇非磁性杂质自动绕行；第三栏磁性拓扑绝缘体实现单向手性无耗散边缘通道。",
        els,
        extra_css=anim_css,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 3. Band Inversion 'Möbius Knot' & Bulk-Boundary Dirac Cone (760 x 500)
# ---------------------------------------------------------------------------
def build_band_inversion() -> str:
    # Exact BHZ 1D dispersion slice: E_+(k) = +sqrt((M + |B|*k^2)^2 + A^2 * k^2)
    # Normal insulator: M > 0 (M and +|B|*k^2 have SAME sign -> monotonic parabola, no inversion)
    # Inverted TI:      M < 0 (M + |B|*k^2 changes sign at k = sqrt(|M/B|) -> camelback SOC gap!)
    def bhz_e(k: float, m_val: float, b_abs: float = 1.0, a_val: float = 0.50) -> float:
        return math.sqrt((m_val + b_abs * k * k) ** 2 + (a_val * k) ** 2)

    e_norm_0 = bhz_e(0.0, 0.55)
    e_inv_0 = bhz_e(0.0, -0.55)
    e_inv_off = bhz_e(0.65, -0.55)
    assert abs(e_norm_0 - 0.55) < 1e-9 and e_inv_off < e_inv_0

    W, H = 760, 500
    els = header(
        "电子能带怎么“打死结”？重原子自旋-轨道耦合与能带反转三步曲",
        "当内部“拧过半圈”的反转能带撞上外部普通真空，交界面能隙必须归零，长出擦不掉的狄拉克锥！",
    )

    # Panel 1: Normal Insulator (M > 0, Paper cylinder)
    els.append(card(16, 68, 232, 414, fill="#ffffff"))
    els.append(step_badge(34, 92, 1, SLATE, "#f1f5f9"))
    els.append(txt(54, 97, "普通绝缘体 (M > 0)", size=12.0, weight="700", color=INK))
    els.append(txt(132, 118, "如食盐、石英、外部真空", size=10.0, color=MUTED, anchor="middle"))

    # Plot 1 box
    x1, y1, w1, h1 = 36, 134, 192, 184
    els.append(f'<rect x="{x1}" y="{y1}" width="{w1}" height="{h1}" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')
    cy1 = y1 + h1 / 2
    els.append(_line(x1 + 10, cy1, x1 + w1 - 10, cy1, stroke="#cbd5e1", sw=1.1, dash="4,3"))

    up_norm, lo_norm = [], []
    for i in range(61):
        kv = -1.0 + 2.0 * (i / 60.0)
        ev = bhz_e(kv, 0.42, b_abs=0.72, a_val=0.45)
        px = x1 + 16 + (kv + 1.0) / 2.0 * (w1 - 32)
        up_norm.append(f"{px:.1f},{cy1 - ev * 48:.1f}")
        lo_norm.append(f"{px:.1f},{cy1 + ev * 48:.1f}")
    els.append(f'<polyline points="{" ".join(up_norm)}" fill="none" stroke="{BLUE}" stroke-width="2.8"/>')
    els.append(f'<polyline points="{" ".join(lo_norm)}" fill="none" stroke="{ORANGE}" stroke-width="2.8"/>')
    els.append(txt(x1 + w1 / 2, y1 + 22, "导带在上（p 态，蓝色）", size=9.9, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(x1 + w1 / 2, cy1 + 4, "绝缘带隙 E_g > 0", size=9.8, color=SLATE, anchor="middle", weight="600"))
    els.append(txt(x1 + w1 / 2, y1 + h1 - 12, "价带在下（s 态，橙色）", size=9.9, color=ORANGE, anchor="middle", weight="700"))

    # Untwisted paper loop icon + caption
    els.append('<ellipse cx="132" cy="358" rx="46" ry="16" fill="none" stroke="#64748b" stroke-width="3.2"/>')
    els.append(txt(132, 396, "像“没拧过的普通纸环”", size=10.5, weight="700", color=SLATE, anchor="middle"))
    els.append(txt(132, 418, "拓扑不变量 ν₀ = 0（平庸态）", size=10.0, color=INK, anchor="middle"))
    els.append(txt(132, 440, "上下能带各司其职，", size=9.9, color=MUTED, anchor="middle"))
    els.append(txt(132, 458, "体内和表面都不导电。", size=9.9, color=MUTED, anchor="middle"))

    # Panel 2: Heavy-Element SOC Band Inversion (M < 0, Möbius twist!)
    els.append(card(264, 68, 232, 414, fill="#eff6ff"))
    els.append(step_badge(282, 92, 2, BLUE))
    els.append(txt(302, 97, "重元素能带反转 (M < 0)", size=12.0, weight="700", color=BLUE))
    els.append(txt(380, 118, "铋(Bi, Z=83)、碲(Te)、汞(Hg)", size=10.0, color=BLUE, anchor="middle", weight="600"))

    x2, y2, w2, h2 = 284, 134, 192, 184
    els.append(f'<rect x="{x2}" y="{y2}" width="{w2}" height="{h2}" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.3"/>')
    cy2 = y2 + h2 / 2
    els.append(_line(x2 + 10, cy2, x2 + w2 - 10, cy2, stroke="#cbd5e1", sw=1.1, dash="4,3"))

    up_inv, lo_inv = [], []
    for i in range(61):
        kv = -1.1 + 2.2 * (i / 60.0)
        ev = bhz_e(kv, -0.52, b_abs=1.05, a_val=0.42)
        px = x2 + 16 + (kv + 1.1) / 2.2 * (w2 - 32)
        up_inv.append(f"{px:.1f},{cy2 - ev * 52:.1f}")
        lo_inv.append(f"{px:.1f},{cy2 + ev * 52:.1f}")
    els.append(f'<polyline points="{" ".join(up_inv)}" fill="none" stroke="{BLUE}" stroke-width="2.8"/>')
    els.append(f'<polyline points="{" ".join(lo_inv)}" fill="none" stroke="{ORANGE}" stroke-width="2.8"/>')
    # Highlight inverted character right at k = 0!
    els.append(f'<circle cx="{x2 + w2/2:.1f}" cy="{cy2 - 0.52 * 52:.1f}" r="5.5" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.5"/>')
    els.append(f'<circle cx="{x2 + w2/2:.1f}" cy="{cy2 + 0.52 * 52:.1f}" r="5.5" fill="{BLUE}" stroke="#ffffff" stroke-width="1.5"/>')
    els.append(txt(x2 + w2 / 2, y2 + 22, "中心 k=0 处：橙色反超到顶！", size=9.8, color=ORANGE, anchor="middle", weight="700"))
    els.append(txt(x2 + w2 / 2, cy2 + 4, "SOC 重开体能隙 ≈ 0.3 eV", size=9.8, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(x2 + w2 / 2, y2 + h2 - 12, "中心 k=0 处：蓝色下沉到底！", size=9.8, color=BLUE, anchor="middle", weight="700"))

    # Möbius figure-8 twisted ribbon icon
    els.append('<path d="M 332 358 C 332 338, 366 338, 380 358 C 394 378, 428 378, 428 358 C 428 338, 394 338, 380 358 C 366 378, 332 378, 332 358 Z" fill="none" stroke="#1d4ed8" stroke-width="3.0"/>')
    els.append(txt(380, 396, "像“拧半圈粘合的莫比乌斯环”", size=10.5, weight="700", color=BLUE, anchor="middle"))
    els.append(txt(380, 418, "拓扑不变量 ν₀ = 1（非平庸态！）", size=10.0, color=RED, anchor="middle", weight="700"))
    els.append(txt(380, 440, "相对论级自旋-轨道耦合(SOC)", size=9.9, color=SLATE, anchor="middle"))
    els.append(txt(380, 458, "把导带与价带在体内拧成死结。", size=9.9, color=SLATE, anchor="middle"))

    # Panel 3: Bulk-Boundary Correspondence -> Gapless Dirac Cone at Interface!
    els.append(card(512, 68, 232, 414, fill="#f0fdf4"))
    els.append(step_badge(530, 92, 3, GREEN, GREEN_SOFT))
    els.append(txt(550, 97, "交界处必长“狄拉克锥”", size=12.0, weight="700", color=GREEN))
    els.append(txt(628, 118, "体-边对应：ν₀ 从 1 变 0 必过零点", size=9.9, color=TEAL, anchor="middle", weight="600"))

    x3, y3, w3, h3 = 532, 134, 192, 184
    els.append(f'<rect x="{x3}" y="{y3}" width="{w3}" height="{h3}" rx="8" fill="#ffffff" stroke="#86efac" stroke-width="1.3"/>')
    cy3 = y3 + h3 / 2
    cx3 = x3 + w3 / 2
    # Shaded bulk conduction and valence continua
    els.append(f'<polygon points="{x3+18},{y3+14} {x3+w3-18},{y3+14} {cx3},{cy3-30}" fill="#dbeafe" opacity="0.85"/>')
    els.append(f'<polygon points="{x3+18},{y3+h3-14} {x3+w3-18},{y3+h3-14} {cx3},{cy3+30}" fill="#ffedd5" opacity="0.85"/>')
    # Crisscrossing red & green topological surface Dirac lines E = +- hbar v_F k!
    els.append(_line(x3 + 26, cy3 + 62, x3 + w3 - 26, cy3 - 62, stroke=RED, sw=2.8))
    els.append(_line(x3 + 26, cy3 - 62, x3 + w3 - 26, cy3 + 62, stroke=GREEN, sw=2.8))
    els.append(f'<circle cx="{cx3:.1f}" cy="{cy3:.1f}" r="4.8" fill="{RED}" stroke="#ffffff" stroke-width="1.4"/>')
    els.append(txt(cx3, y3 + 28, "体导带", size=9.8, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(cx3 + 44, cy3 + 4, "狄拉克点", size=9.9, color=RED, anchor="middle", weight="700"))
    els.append(txt(cx3, y3 + h3 - 20, "体价带", size=9.8, color=ORANGE, anchor="middle", weight="700"))

    els.append(txt(628, 344, "表面态色散：E(k) = ±ℏv_F |k|", size=10.6, weight="700", color=GREEN, anchor="middle"))
    els.append(txt(628, 368, "想从体内 ν₀=1 跨到空气 ν₀=0，", size=10.0, color=INK, anchor="middle"))
    els.append(txt(628, 388, "能隙 M 必须在边界穿过 M=0！", size=10.0, color=RED, anchor="middle", weight="700"))
    els.append(txt(628, 412, "电子在表面像无质量光子一样飞驰，", size=9.9, color=SLATE, anchor="middle"))
    els.append(txt(628, 432, "这就是角分辨光电子谱(ARPES)", size=9.9, color=SLATE, anchor="middle"))
    els.append(txt(628, 452, "直接拍到的“X 形”铁证！", size=10.0, color=TEAL, anchor="middle", weight="700"))

    return figure(
        H,
        "重元素自旋轨道耦合驱动能带反转与体边对应表面狄拉克锥形成图",
        "第一栏普通绝缘体导带在上价带在下如未扭转纸环(ν0=0)；第二栏重元素自旋轨道耦合使能带在k=0处上下反转如莫比乌斯环(ν0=1)；第三栏在晶体与真空边界处能隙闭合形成线性X形表面狄拉克锥。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 4. Three Flagship Families: TI, QAHE, and Weyl Semimetal Fermi Arcs (760 x 505)
# ---------------------------------------------------------------------------
def build_family_portrait() -> str:
    W, H = 760, 505
    els = header(
        "拓扑电子材料“三剑客”家族图谱：绝缘体、单向磁性膜与外尔半金属",
        "从表面狄拉克锥、零磁场单行道，到体内藏着“动量磁单极子”、表面长出半截“费米弧”的砷化钽",
    )

    # Column 1: 3D Topological Insulator
    els.append(card(16, 68, 232, 420, fill="#eff6ff"))
    els.append(pill(32, 82, "家族 ①：拓扑绝缘体", fg="#ffffff", bg=BLUE, w=160))
    els.append(txt(132, 124, "代表：HgTe、Bi₂Se₃、Bi₂Te₃", size=10.4, weight="700", color=INK, anchor="middle"))
    els.append(txt(132, 143, "（2006–2009 理论预言与实验证实）", size=9.8, color=MUTED, anchor="middle"))

    # Visual: 3D block with 2D Dirac cone on top surface
    els.append('<rect x="44" y="160" width="176" height="128" rx="10" fill="#ffffff" stroke="#93c5fd" stroke-width="1.4"/>')
    # Upper and lower cone triangles
    els.append('<polygon points="132,224 94,174 170,174" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="1.8"/>')
    els.append('<polygon points="132,224 94,274 170,274" fill="#fed7aa" stroke="#ea580c" stroke-width="1.8"/>')
    els.append('<ellipse cx="132" cy="174" rx="38" ry="8" fill="#dbeafe" stroke="#1d4ed8" stroke-width="1.5"/>')
    els.append('<ellipse cx="132" cy="274" rx="38" ry="8" fill="#ffedd5" stroke="#ea580c" stroke-width="1.5"/>')
    els.append(txt(132, 228, "闭合圆费米面", size=9.8, color=BLUE, anchor="middle", weight="700"))

    els.append(txt(34, 314, "• 体内：标准绝缘体（有完整带隙）", size=10.0, color=INK))
    els.append(txt(34, 338, "• 表面：二维无能隙狄拉克金属态", size=10.0, color=BLUE, weight="700"))
    els.append(txt(34, 362, "• 保护神：时间反演对称性（怕磁铁）", size=10.0, color=INK))
    els.append(txt(34, 386, "• 温度门槛：Bi₂Se₃ 带隙 0.3 eV，", size=10.0, color=SLATE))
    els.append(txt(44, 405, "室温（300 K）就能拍到拓扑表面态！", size=10.0, color=GREEN, weight="700"))
    els.append('<rect x="32" y="424" width="200" height="48" rx="8" fill="#dbeafe"/>')
    els.append(txt(132, 444, "拿手绝活：高效率自旋轨道矩", size=10.0, weight="700", color=BLUE, anchor="middle"))
    els.append(txt(132, 462, "翻转磁存储比特（SOT-MRAM）", size=9.8, color=INK, anchor="middle"))

    # Column 2: Magnetic TI / QAHE
    els.append(card(264, 68, 232, 420, fill="#f0fdf4"))
    els.append(pill(280, 82, "家族 ②：磁性拓扑绝缘体", fg="#ffffff", bg=GREEN, w=180))
    els.append(txt(380, 124, "代表：Cr-(Bi,Sb)₂Te₃、MnBi₂Te₄", size=10.3, weight="700", color=INK, anchor="middle"))
    els.append(txt(380, 143, "（2013 清华薛其坤团队首测 QAHE）", size=9.8, color=MUTED, anchor="middle"))

    # Visual: Gapped surface cone + 1D chiral perimeter loop
    els.append('<rect x="292" y="160" width="176" height="128" rx="10" fill="#ffffff" stroke="#86efac" stroke-width="1.4"/>')
    els.append('<rect x="316" y="186" width="128" height="76" rx="8" fill="#dcfce7" stroke="#16a34a" stroke-width="2.2"/>')
    els.append(_line(324, 180, 436, 180, stroke=RED, sw=2.6, marker="arr-red"))
    els.append(_line(450, 192, 450, 256, stroke=RED, sw=2.6, marker="arr-red"))
    els.append(_line(436, 268, 324, 268, stroke=RED, sw=2.6, marker="arr-red"))
    els.append(_line(310, 256, 310, 192, stroke=RED, sw=2.6, marker="arr-red"))
    els.append(txt(380, 221, "上下表面也打开能隙", size=9.9, color=TEAL, anchor="middle", weight="700"))
    els.append(txt(380, 239, "只剩一维侧边单行道！", size=9.9, color=RED, anchor="middle", weight="700"))

    els.append(txt(282, 314, "• 体内与上下表面：全部绝缘！", size=10.0, color=INK))
    els.append(txt(282, 338, "• 唯独薄膜一维侧边：零损耗单行道", size=10.0, color=GREEN, weight="700"))
    els.append(txt(282, 362, "• 保护神：非零陈数 C = ±1（自带磁性）", size=10.0, color=INK))
    els.append(txt(282, 386, "• 温度门槛：摆脱数万高斯大磁铁，", size=10.0, color=SLATE))
    els.append(txt(292, 405, "但目前仍需极低温（~0.03–数 K）", size=10.0, color=AMBER, weight="700"))
    els.append('<rect x="280" y="424" width="200" height="48" rx="8" fill="#dcfce7"/>')
    els.append(txt(380, 444, "拿手绝活：桌面级量子电阻基准", size=10.0, weight="700", color=GREEN, anchor="middle"))
    els.append(txt(380, 462, "与未来无耗散拓扑互连线", size=9.8, color=INK, anchor="middle"))

    # Column 3: Topological Weyl Semimetal (TaAs, 2015)
    els.append(card(512, 68, 232, 420, fill="#f5f3ff"))
    els.append(pill(528, 82, "家族 ③：拓扑外尔半金属", fg="#ffffff", bg=PURPLE, w=180))
    els.append(txt(628, 124, "代表：砷化钽 TaAs、NbAs、Co₃Sn₂S₂", size=10.1, weight="700", color=INK, anchor="middle"))
    els.append(txt(628, 143, "（2015 中科院物理所与普林斯顿发现）", size=9.8, color=MUTED, anchor="middle"))

    # Visual: 3D slab showing bulk +1 / -1 Weyl node pair + open Fermi arc on top surface!
    els.append('<rect x="540" y="160" width="176" height="128" rx="10" fill="#ffffff" stroke="#c4b5fd" stroke-width="1.4"/>')
    # Top surface parallelogram
    els.append('<polygon points="562,196 676,196 696,172 582,172" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.4"/>')
    # Bulk Weyl nodes W+ and W-
    els.append('<circle cx="596" cy="242" r="9" fill="#dc2626"/>')
    els.append(txt(596, 246, "+1", size=9.8, color="#ffffff", anchor="middle", weight="700"))
    els.append('<circle cx="662" cy="242" r="9" fill="#1d4ed8"/>')
    els.append(txt(662, 246, "−1", size=9.8, color="#ffffff", anchor="middle", weight="700"))
    # Dashed projection lines to top surface + OPEN curved Fermi Arc!
    els.append(_line(596, 232, 596, 184, stroke=RED, sw=1.3, dash="3,3"))
    els.append(_line(662, 232, 662, 184, stroke=BLUE, sw=1.3, dash="3,3"))
    els.append('<path d="M 596 184 Q 629 168 662 184" fill="none" stroke="#7c3aed" stroke-width="3.2"/>')
    els.append('<circle cx="596" cy="184" r="3.8" fill="#dc2626"/>')
    els.append('<circle cx="662" cy="184" r="3.8" fill="#1d4ed8"/>')
    els.append(txt(629, 214, "表面“费米弧”（半截开弧！）", size=9.8, color=PURPLE, anchor="middle", weight="700"))
    els.append(txt(629, 272, "体内成对“外尔点”（手性 ±1）", size=9.8, color=INK, anchor="middle", weight="700"))

    els.append(txt(530, 314, "• 体内不是绝缘体，而是三维半金属！", size=10.0, color=INK))
    els.append(txt(530, 338, "• 导带价带成对点接触：动量磁单极子", size=10.0, color=PURPLE, weight="700"))
    els.append(txt(530, 362, "• 表面奇观：不闭合的“费米弧”连起两点", size=10.0, color=INK))
    els.append(txt(530, 386, "• 磁场平行电场时出现“手性反常”，", size=10.0, color=SLATE))
    els.append(txt(540, 405, "电阻非但不升反而暴跌（负磁阻）！", size=10.0, color=RED, weight="700"))
    els.append('<rect x="528" y="424" width="200" height="48" rx="8" fill="#ede9fe"/>')
    els.append(txt(628, 444, "拿手绝活：超高迁移率宽谱光电", size=10.0, weight="700", color=PURPLE, anchor="middle"))
    els.append(txt(628, 462, "探测、拓扑催化与手性电子学", size=9.8, color=INK, anchor="middle"))

    return figure(
        H,
        "拓扑绝缘体与量子反常霍尔磁性薄膜及拓扑外尔半金属三大家族对比图",
        "左栏展示三维拓扑绝缘体体内有带隙而表面有闭合狄拉克锥；中栏展示磁性拓扑绝缘体上下表面开隙仅留一维无耗散边缘态；右栏展示拓扑外尔半金属体内成对手性外尔点与表面半截不闭合费米弧。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 5. 2019 Nature Census Shockwave & Honest Silicon Bottlenecks (760 x 500)
# ---------------------------------------------------------------------------
def build_census_and_reality() -> str:
    # Exact verified numbers from Zhang, Fang, Weng, Fang et al., Nature 566, 475-479 (2019), arXiv:1807.08756:
    total_scanned = 39519
    n_tsm = 5005   # Topological semimetals
    n_ti = 1814    # Topological insulators
    n_tci = 1237   # Topological crystalline insulators
    n_topo = n_tsm + n_ti + n_tci
    assert n_topo == 8056
    pct_topo = 100.0 * n_topo / total_scanned  # 20.385% (and ~27% in stoichiometric filtered ICSD!)
    assert 20.3 < pct_topo < 20.5

    W, H = 760, 500
    els = header(
        "颠覆教科书的大普查：自然界超两成晶体带拓扑！为何还没换掉硅芯片？",
        "2019《Nature》三篇背靠背论文筛遍数万种晶体；同时看清走向日常手机芯片的三道真实工程门槛",
    )

    # Left Card: 2019 Nature High-Throughput Topological Catalogue
    els.append(card(16, 68, 354, 414, fill="#ffffff"))
    els.append(step_badge(36, 92, 1, BLUE))
    els.append(txt(56, 97, "2019 大反转：拓扑材料根本不是“稀有怪胎”！", size=12.0, weight="700", color=BLUE))
    els.append(txt(36, 121, "过去靠人工逐个算陈数，十年只找到寥寥十几种；", size=10.0, color=SLATE))
    els.append(txt(36, 140, "2019 年“对称性指标 / 拓扑量子化学”全库自动普查：", size=10.0, color=INK, weight="600"))

    # Exact proportional bar for 39,519 scanned materials (Zhang et al., Nature 2019)
    bx0, by0, bw_tot, bh = 36, 162, 314, 34
    w_tsm = bw_tot * (n_tsm / total_scanned)
    w_ti = bw_tot * (n_ti / total_scanned)
    w_tci = bw_tot * (n_tci / total_scanned)
    w_triv = bw_tot - (w_tsm + w_ti + w_tci)

    els.append(f'<rect x="{bx0:.1f}" y="{by0}" width="{w_tsm:.1f}" height="{bh}" fill="{PURPLE}"/>')
    els.append(f'<rect x="{bx0 + w_tsm:.1f}" y="{by0}" width="{w_ti:.1f}" height="{bh}" fill="{BLUE}"/>')
    els.append(f'<rect x="{bx0 + w_tsm + w_ti:.1f}" y="{by0}" width="{w_tci:.1f}" height="{bh}" fill="{GREEN}"/>')
    els.append(f'<rect x="{bx0 + w_tsm + w_ti + w_tci:.1f}" y="{by0}" width="{w_triv:.1f}" height="{bh}" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1"/>')
    els.append(txt(bx0 + (w_tsm + w_ti + w_tci) / 2, by0 - 7, "8,056 种拓扑材料 (20.4%)", size=9.9, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(bx0 + w_tsm + w_ti + w_tci + w_triv / 2, by0 + 22, "普通平庸晶体 31,463 种 (79.6%)", size=9.9, color=SLATE, anchor="middle", weight="600"))

    # Breakdown rows
    rows = [
        (PURPLE, "拓扑半金属 (TSM)", "5,005 种 (12.7%)", "外尔 / 狄拉克 / 节线半金属"),
        (BLUE, "拓扑绝缘体 (TI)", "1,814 种 (4.6%)", "强/弱 Z₂ 自旋锁定绝缘体"),
        (GREEN, "拓扑晶体绝缘体 (TCI)", "1,237 种 (3.1%)", "受镜面/旋转晶体对称性保护"),
    ]
    for idx, (col, name, cnt, desc) in enumerate(rows):
        ry = 212 + idx * 48
        els.append(f'<rect x="36" y="{ry}" width="314" height="40" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.1"/>')
        els.append(f'<circle cx="52" cy="{ry + 20}" r="6" fill="{col}"/>')
        els.append(txt(66, ry + 17, f"{name}：{cnt}", size=10.2, weight="700", color=INK))
        els.append(txt(66, ry + 33, desc, size=9.8, color=MUTED))

    # Bottom surprise box
    els.append('<rect x="36" y="362" width="314" height="104" rx="9" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.3"/>')
    els.append(txt(193, 384, "连身边的老熟人都有“隐藏拓扑身份证”！", size=10.6, weight="700", color=BLUE, anchor="middle"))
    els.append(txt(193, 405, "• 另一组筛查 26,938 种化学计量晶体（Vergniory 等）", size=9.9, color=INK, anchor="middle"))
    els.append(txt(193, 424, "  发现超 24%–27% 天然晶体具有拓扑电子结构！", size=9.9, color=RED, anchor="middle", weight="700"))
    els.append(txt(193, 444, "• 连黄金(Au)表面态、单质铋(Bi)都带拓扑印记；", size=9.9, color=SLATE, anchor="middle"))
    els.append(txt(193, 460, "  全球公开数据库已上线，输入化学式即可一键查验。", size=9.8, color=TEAL, anchor="middle", weight="600"))

    # Right Card: Honest Engineering Bottlenecks & Real-World Frontier
    els.append(card(386, 68, 358, 414, fill="#ffffff"))
    els.append(step_badge(406, 92, 2, ORANGE, ORANGE_SOFT))
    els.append(txt(426, 97, "冷静祛魅：距离替代手机硅芯片差哪三步？", size=12.0, weight="700", color=ORANGE))

    hurdles = [
        (
            "门槛 ①：三维表面只禁 180° 掉头，不禁斜向拐弯",
            "三维拓扑绝缘体表面是二维平面：虽严格禁止 180° 背散射，",
            "但电子仍能偏转 60°、90° 散射，室温下并非零电阻超导体！",
            "#fff7ed",
            "#fdba74",
            ORANGE,
        ),
        (
            "门槛 ②：体态空位漏电 + 单行道困在极低温",
            "真实 Bi₂Se₃ 晶体常含硒空位导致内部漏电；而真正零耗散单行",
            "道的量子反常霍尔效应(QAHE)目前仍需几开尔文极低温。",
            "#fef2f2",
            "#fca5a5",
            RED,
        ),
        (
            "门槛 ③：“关不断”难做数字开关 + 严谨证伪纠偏",
            "晶体管算 0 和 1 必须能彻底关断电流，拓扑边缘偏偏关不断！",
            "同时马约拉纳拓扑量子计算曾历经 2021《Nature》撤稿自纠。",
            "#f8fafc",
            "#cbd5e1",
            SLATE,
        ),
    ]
    for idx, (h_title, l1, l2, bg, bd, col) in enumerate(hurdles):
        hy = 114 + idx * 92
        els.append(f'<rect x="402" y="{hy}" width="326" height="82" rx="9" fill="{bg}" stroke="{bd}" stroke-width="1.3"/>')
        els.append(txt(414, hy + 22, h_title, size=10.5, weight="700", color=col))
        els.append(txt(414, hy + 44, l1, size=9.9, color=INK))
        els.append(txt(414, hy + 64, l2, size=9.9, color=SLATE))

    # Bottom already-landed applications bar
    els.append('<rect x="402" y="394" width="326" height="72" rx="9" fill="#0f172a"/>')
    els.append(txt(565, 415, "已经率先落地的三大硬核战场：", size=10.4, weight="700", color="#4ade80", anchor="middle"))
    els.append(txt(565, 436, "① 国际量子电阻基准  ② 低功耗自旋存储 (SOT-MRAM)", size=9.9, color="#f8fafc", anchor="middle"))
    els.append(txt(565, 455, "③ 宽波段红外光电探测与纳米互连线抗散射材料", size=9.9, color="#93c5fd", anchor="middle"))

    return figure(
        H,
        "2019自然杂志拓扑电子材料大普查数据与商业芯片工程门槛对比图",
        "左栏展示2019年Nature对39519种非磁性晶体的自动普查结果，发现8056种(20.4%)为拓扑材料（含5005种拓扑半金属、1814种拓扑绝缘体、1237种拓扑晶体绝缘体）；右栏解析三维斜散射、低温门槛与开关比三大工程挑战及已落地应用。",
        els,
        extra_defs=_markers(),
    )


@register(TOPIC, "physics", "拓扑电子材料通俗图解（5张760px原创SVG）")
def build_all() -> None:
    builders = [
        ("coffee-cup-donut-and-quantum-hall-steps.svg", build_coffee_cup_and_qhe),
        ("ordinary-wire-vs-topological-highway.svg", build_topological_highway),
        ("band-inversion-mobius-knot.svg", build_band_inversion),
        ("family-portrait-ti-qahe-weyl-semimetal.svg", build_family_portrait),
        ("nature-2019-catalogue-and-chip-reality.svg", build_census_and_reality),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
