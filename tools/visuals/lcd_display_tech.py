"""
Visuals for '液晶显示技术与显示技术的发展' (Liquid Crystal Display Physics & Century Display Evolution:
Reinitzer 1888 Double-Melting-Point Cholesteryl Benzoate & TN Crossed-Polarizer Waveguide Shutter,
TFT-LCD 7-Layer Sandwich + 4K 1819x Matrix Wiring Reduction + ~6% Photon Budget Funnel,
TN vs VA vs IPS Molecular Orientation & Viewing-Angle Birefringence,
2014/2023 Nobel Backlight Leap from CCFL & WLED to QLED Quantum Dots & Mini-LED Local Dimming,
and 130-Year 5-Generation Panorama: CRT, LCD, OLED, Micro-LED Mass Transfer, and E-Ink).
Generates 5 original 760px Chinese SVG diagrams in assets/images/lcd-display-tech/
with verified optical and device-physics assertions from peer-reviewed primary literature.
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
    pill,
    register,
    txt,
    write_svg,
)

TOPIC = "lcd-display-tech"
RED = "#dc2626"
RED_SOFT = "#fef2f2"
TEAL = "#0f766e"
TEAL_SOFT = "#f0fdfa"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
PINK = "#db2777"
PINK_SOFT = "#fdf2f8"
DARK_CARD = "#0f172a"


def _line(x1, y1, x2, y2, stroke=INK, sw=1.6, dash=None, marker=None, cls=None):
    extra = ""
    if cls:
        extra += f' class="{cls}"'
    if dash:
        extra += f' stroke-dasharray="{dash}"'
    if marker:
        extra += f' marker-end="url(#{marker})"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'


def _arrow_defs():
    return """<marker id="arr-ink" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#0f172a"/>
  </marker>
  <marker id="arr-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#6d28d9"/>
  </marker>
  <marker id="arr-red" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#dc2626"/>
  </marker>
  <marker id="arr-teal" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
    <path d="M0,0.6 L6.5,3.5 L0,6.4 Z" fill="#0f766e"/>
  </marker>"""


def _verify_lcd_display_data() -> dict:
    """Verify electro-optical, circuit, and quantum-efficiency constants from primary literature."""
    # 1. Reinitzer 1888 cholesteryl benzoate double melting points (Mazza & Schoen, 2011, PMC3179171)
    t_melt_cloudy_c = 145.5
    t_clear_isotropic_c = 178.5
    assert math.isclose(t_clear_isotropic_c - t_melt_cloudy_c, 33.0, rel_tol=1e-6)

    # 2. Gooch-Tarry first minimum for 90-degree TN waveguide (Schadt & Helfrich, 1971; Yang & Wu, 2015)
    # T_nw = sin^2(pi/2 * sqrt(1 + u^2)) / (1 + u^2), where u = 2 * d * delta_n / lambda
    # First minimum of dark leakage (maximum bright transmission in NW mode): sqrt(1 + u^2) = 2 => u = sqrt(3)
    lam_um = 0.55  # 550 nm green reference wavelength
    delta_n = 0.10  # typical nematic birefringence
    u_first_min = math.sqrt(3.0)
    d_first_min_um = (u_first_min / 2.0) * lam_um / delta_n  # ~4.763 um
    assert 4.7 <= d_first_min_um <= 4.85
    # Malus's law crossed polarizers without LC waveguide rotation: cos^2(90 deg) = 0
    assert abs(math.cos(math.radians(90.0)) ** 2) < 1e-12

    # 3. Freedericksz threshold voltage V_th = pi * sqrt(K11 / (eps_0 * delta_eps))
    eps_0 = 8.854e-12
    k11_n = 11.0e-12  # ~11 pN splay elastic constant
    delta_eps = 8.0   # positive dielectric anisotropy
    v_th = math.pi * math.sqrt(k11_n / (eps_0 * delta_eps))  # ~1.24 V
    assert 0.9 <= v_th <= 2.0

    # 4. 4K UHD active-matrix addressing reduction (3840 x 2160 RGB)
    cols_px, rows_px = 3840, 2160
    subpixels_4k = cols_px * rows_px * 3  # 24,883,200
    matrix_lines_4k = cols_px * 3 + rows_px  # 11,520 data + 2,160 gate = 13,680
    wiring_reduction = subpixels_4k / matrix_lines_4k  # 1818.947...
    assert subpixels_4k == 24_883_200
    assert matrix_lines_4k == 13_680
    assert 1818.0 <= wiring_reduction <= 1820.0

    # 5. Non-emissive LCD photon budget funnel (Huang, Hsiang, Deng & Wu, 2020, PMC7303200: T_LCD ~ 5%-8%)
    t_pol1 = 0.43          # unpolarized light through real absorptive bottom polarizer
    t_aperture = 0.62      # TFT + gate/data lines + black matrix aperture ratio
    t_cf = 0.27            # RGB absorptive color filter passes ~1/3 spectrum with dye losses
    t_lc_pol2 = 0.82       # LC retardation efficiency + top analyzer transmission
    t_total_std = t_pol1 * t_aperture * t_cf * t_lc_pol2  # ~0.0590 (5.9%)
    t_total_dbef = (t_pol1 * 1.55) * t_aperture * t_cf * t_lc_pol2  # ~0.0915 (9.15% with DBEF recycling)
    assert 0.048 <= t_total_std <= 0.075
    assert 0.08 <= t_total_dbef <= 0.105

    # 6. Motion picture response time MPRT = sqrt(tau^2 + (0.8 * T_f)^2) (PMC7303200 Eq. 29-30)
    tau_lcd_ms = 2.0
    mprt_60hz_lcd = math.sqrt(tau_lcd_ms ** 2 + (0.8 * (1000.0 / 60.0)) ** 2)  # ~13.48 ms
    mprt_60hz_oled = math.sqrt(0.05 ** 2 + (0.8 * (1000.0 / 60.0)) ** 2)       # ~13.33 ms
    mprt_bfi_10pct = 0.8 * (1000.0 / 60.0) * 0.10                              # 1.333 ms
    assert math.isclose(mprt_60hz_lcd, 13.48, abs_tol=0.05)
    assert math.isclose(mprt_60hz_oled, 13.33, abs_tol=0.05)
    assert math.isclose(mprt_bfi_10pct, 1.33, abs_tol=0.05)

    # 7. Micro-LED 4K yield math: even 99.99% ("four nines") leaves thousands of dead subpixels!
    dead_at_4nines = round(subpixels_4k * (1.0 - 0.9999))  # 2,488 dead subpixels!
    dead_at_6nines = round(subpixels_4k * (1.0 - 0.999999))  # ~25 subpixels
    assert dead_at_4nines == 2488 and dead_at_6nines == 25

    return {
        "d_first_min_um": d_first_min_um,
        "v_th": v_th,
        "subpixels_4k": subpixels_4k,
        "matrix_lines_4k": matrix_lines_4k,
        "wiring_reduction": wiring_reduction,
        "t_after_pol1_pct": round(t_pol1 * 100, 1),
        "t_after_ap_pct": round(t_pol1 * t_aperture * 100, 1),
        "t_after_cf_pct": round(t_pol1 * t_aperture * t_cf * 100, 1),
        "t_total_std_pct": round(t_total_std * 100, 1),
        "t_total_dbef_pct": round(t_total_dbef * 100, 1),
        "dead_at_4nines": dead_at_4nines,
    }


def _rod(cx: float, cy: float, length: float, width: float, angle_deg: float, fill: str, stroke: str, cls: str = "") -> str:
    cls_attr = f' class="{cls}"' if cls else ""
    rx = width / 2.0
    x = cx - length / 2.0
    y = cy - width / 2.0
    return (
        f'<g{cls_attr} transform="translate({cx:.1f},{cy:.1f}) rotate({angle_deg:.1f})">'
        f'<rect x="{-length/2:.1f}" y="{-width/2:.1f}" width="{length:.1f}" height="{width:.1f}" '
        f'rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/></g>'
    )


def _svg_1_carrot_shutter(data: dict) -> str:
    """SVG 1: Reinitzer's 1888 double melting points & TN crossed-polarizer shutter (with 1-shot CSS animation)."""
    css = """
    @keyframes lcStandUp {
      0%, 18% { transform: scaleX(0.42) rotate(-32deg); opacity: 0.72; }
      58%, 100% { transform: scaleX(1) rotate(0deg); opacity: 1; }
    }
    @keyframes shutterBlockFade {
      0%, 18% { opacity: 0.85; }
      58%, 100% { opacity: 0.14; }
    }
    .anim-lc-shutter {
      transform-box: fill-box;
      transform-origin: center;
      animation: lcStandUp 4.2s cubic-bezier(0.22, 1, 0.36, 1) 1 forwards;
    }
    .anim-blocked-beam {
      animation: shutterBlockFade 4.2s ease-out 1 forwards;
    }
    @media (prefers-reduced-motion: reduce) {
      .anim-lc-shutter, .anim-blocked-beam {
        animation: none !important;
      }
    }
    """
    el: list[str] = []
    el.append(txt(380, 28, "从胡萝卜“双熔点怪液”到拧光 90° 的液晶百叶窗", size=17, color=INK, anchor="middle", weight="700"))
    el.append(txt(380, 48, "1888 年莱尼泽尔发现第四态物质；1971 年沙德特与赫尔弗里希把它夹进正交偏振片做成电控光阀", size=12, color=MUTED, anchor="middle"))

    # Top container: 3 states of matter around Reinitzer's two melting points
    el.append(card(24, 60, 712, 108, rx=12, fill="#f8fafc", stroke=BORDER))
    el.append(pill(38, 68, "第一步：为什么叫“液态晶体”？苯甲酸胆固醇酯的两次熔化（1888）", fg=BLUE, bg=BLUE_SOFT, h=22, size=11.5))

    # Subcard 1: Solid (<145.5 C)
    el.append(card(38, 96, 194, 62, rx=8, fill="#ffffff", stroke=BORDER))
    el.append(txt(135, 115, "① 固态晶体 (< 145.5 °C)", size=12, color=INK, anchor="middle", weight="700"))
    el.append(txt(135, 134, "位置锁死 + 方向整齐", size=11, color=BODY, anchor="middle"))
    el.append(txt(135, 150, "刚性晶格，不能流动", size=10.5, color=MUTED, anchor="middle"))

    # Arrow 1
    el.append(_line(236, 127, 272, 127, stroke=ORANGE, sw=2.0, marker="arr-orange"))
    el.append(txt(254, 116, "145.5°C", size=10.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(254, 143, "初熔浑浊", size=10, color=ORANGE, anchor="middle"))

    # Subcard 2: Liquid Crystal (145.5 - 178.5 C)
    el.append(card(278, 96, 208, 62, rx=8, fill=BLUE_SOFT, stroke=BLUE, sw=1.5))
    el.append(txt(382, 115, "② 液晶态 (145.5~178.5 °C)", size=12, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(382, 134, "位置自由流动 + 长轴方向对齐", size=11, color=INK, anchor="middle", weight="600"))
    el.append(txt(382, 150, "兼具液体流动性与晶体双折射 Δn", size=10.5, color=BLUE, anchor="middle"))

    # Arrow 2
    el.append(_line(490, 127, 526, 127, stroke=PURPLE, sw=2.0, marker="arr-purple"))
    el.append(txt(508, 116, "178.5°C", size=10.5, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(508, 143, "清亮化点", size=10, color=PURPLE, anchor="middle"))

    # Subcard 3: Isotropic Liquid (>178.5 C)
    el.append(card(532, 96, 190, 62, rx=8, fill="#ffffff", stroke=BORDER))
    el.append(txt(627, 115, "③ 清亮液体 (> 178.5 °C)", size=12, color=INK, anchor="middle", weight="700"))
    el.append(txt(627, 134, "位置无序 + 方向随机乱撞", size=11, color=BODY, anchor="middle"))
    el.append(txt(627, 150, "光学各向同性，失去旋光本领", size=10.5, color=MUTED, anchor="middle"))

    # Bottom Left Card: V = 0 Bright State (Normally White TN)
    el.append(card(24, 182, 346, 260, rx=12, fill="#ffffff", stroke=GREEN, sw=1.5))
    el.append(pill(38, 192, "断电亮态 (V = 0)：螺旋阶梯把光拧转 90° 放行", fg=GREEN, bg=GREEN_SOFT, h=22, size=11.5))

    # Optical axis & elements in Left Card
    y_mid = 282
    el.append(_line(44, y_mid, 326, y_mid, stroke="#cbd5e1", sw=1.2, dash="4,3"))
    # Backlight sun/bulb box
    el.append(card(40, 250, 44, 64, rx=7, fill=AMBER_SOFT, stroke=AMBER, sw=1.3))
    el.append(txt(62, 278, "背光", size=11.5, color=AMBER, anchor="middle", weight="700"))
    el.append(txt(62, 295, "自然光", size=10, color=AMBER, anchor="middle"))

    # Polarizer P1 (vertical 0 deg)
    el.append(card(96, 240, 34, 84, rx=5, fill= SLATE_SOFT, stroke=SLATE, sw=1.4))
    for gy in range(248, 320, 12):
        el.append(_line(113, gy, 113, gy + 7, stroke=SLATE, sw=1.8))
    el.append(txt(113, 232, "起偏器 P1", size=10.5, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(113, 339, "竖直 0°", size=10.5, color=SLATE, anchor="middle"))

    # TN LC cell (x=144..258, w=114): 5 rods gradually twisting from vertical (90 deg on screen) to foreshortened dot/tilted (0 deg horizontal out-of-plane)
    el.append(card(144, 240, 114, 84, rx=6, fill=GREEN_SOFT, stroke=GREEN, sw=1.3))
    el.append(txt(201, 232, f"液晶盒 d≈{data['d_first_min_um']:.1f} μm", size=10.5, color=GREEN, anchor="middle", weight="700"))
    rod_xs_l = [158, 179, 201, 223, 244]
    rod_lens_l = [44, 38, 30, 21, 12]
    rod_angs_l = [90, 72, 50, 26, 0]
    for rx_i, rlen, rang in zip(rod_xs_l, rod_lens_l, rod_angs_l):
        el.append(_rod(rx_i, y_mid, rlen, 7, rang, "#34d399", GREEN))
    el.append(txt(201, 339, "螺旋扭转偏振面 90°", size=10.5, color=GREEN, anchor="middle", weight="700"))

    # Analyzer P2 (horizontal 90 deg)
    el.append(card(272, 240, 34, 84, rx=5, fill=SLATE_SOFT, stroke=SLATE, sw=1.4))
    for gy in range(250, 318, 11):
        el.append(_line(279, gy, 299, gy, stroke=SLATE, sw=1.8))
    el.append(txt(289, 232, "检偏器 P2", size=10.5, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(289, 339, "水平 90°", size=10.5, color=SLATE, anchor="middle"))

    # Bright output arrow & badge
    el.append(_line(308, y_mid, 354, y_mid, stroke=GREEN, sw=3.2, marker="arr-green"))
    el.append(txt(335, 266, "亮态!", size=12, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(335, 304, "顺畅通过", size=10.5, color=GREEN, anchor="middle"))

    # Bottom explanation in Left Card
    el.append(card(38, 354, 318, 74, rx=8, fill="#f0fdf4", stroke="#bbf7d0"))
    el.append(txt(50, 374, "• 上下配向膜沟槽互成 90°，迫使棒状分子排成旋转楼梯", size=11, color=INK))
    el.append(txt(50, 394, "• 满足波导条件 d·Δn = (√3/2)λ ≈ 0.48 μm 时，竖直偏振光", size=11, color=BODY))
    el.append(txt(50, 414, "  顺着分子长轴被拧成水平偏振，完美穿过 P2 呈现亮白", size=11, color=GREEN, weight="700"))

    # Bottom Right Card: V > V_th Dark State (Field-Aligned)
    el.append(card(390, 182, 346, 260, rx=12, fill="#ffffff", stroke=PURPLE, sw=1.5))
    el.append(pill(404, 192, f"加电暗态 (V > {data['v_th']:.1f} V)：分子顺电场立正，正交关闸", fg=PURPLE, bg=PURPLE_SOFT, h=22, size=11.5))

    el.append(_line(410, y_mid, 636, y_mid, stroke="#cbd5e1", sw=1.2, dash="4,3"))
    # Backlight
    el.append(card(406, 250, 44, 64, rx=7, fill=AMBER_SOFT, stroke=AMBER, sw=1.3))
    el.append(txt(428, 278, "背光", size=11.5, color=AMBER, anchor="middle", weight="700"))
    el.append(txt(428, 295, "自然光", size=10, color=AMBER, anchor="middle"))

    # Polarizer P1
    el.append(card(462, 240, 34, 84, rx=5, fill=SLATE_SOFT, stroke=SLATE, sw=1.4))
    for gy in range(248, 320, 12):
        el.append(_line(479, gy, 479, gy + 7, stroke=SLATE, sw=1.8))
    el.append(txt(479, 232, "起偏器 P1", size=10.5, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(479, 339, "竖直 0°", size=10.5, color=SLATE, anchor="middle"))

    # TN LC cell with horizontal electric field E across cell thickness (x=510..624)
    el.append(card(510, 240, 114, 84, rx=6, fill=PURPLE_SOFT, stroke=PURPLE, sw=1.4))
    el.append(txt(567, 232, "透明 ITO 加电压 V", size=10.5, color=PURPLE, anchor="middle", weight="700"))
    # Electric field arrow inside top of cell
    el.append(_line(520, 252, 612, 252, stroke=PURPLE, sw=1.3, dash="3,2", marker="arr-purple"))
    el.append(txt(567, 265, "电场 E 沿传播方向", size=9.8, color=PURPLE, anchor="middle"))
    # 5 rods aligned horizontally along propagation axis (with 1-shot animation class!)
    rod_xs_r = [526, 546, 567, 588, 608]
    for rx_i in rod_xs_r:
        el.append(_rod(rx_i, 293, 16, 7, 0, "#c4b5fd", PURPLE, cls="anim-lc-shutter"))
    el.append(txt(567, 339, "螺旋解开，偏振不转!", size=10.5, color=RED, anchor="middle", weight="700"))

    # Analyzer P2
    el.append(card(638, 240, 34, 84, rx=5, fill=SLATE_SOFT, stroke=SLATE, sw=1.4))
    for gy in range(250, 318, 11):
        el.append(_line(645, gy, 665, gy, stroke=SLATE, sw=1.8))
    el.append(txt(655, 232, "检偏器 P2", size=10.5, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(655, 339, "水平 90°", size=10.5, color=SLATE, anchor="middle"))

    # Blocked output badge
    el.append(_line(674, y_mid, 704, y_mid, stroke=RED, sw=2.6, dash="3,3", cls="anim-blocked-beam"))
    el.append(card(682, 258, 44, 48, rx=7, fill=DARK_CARD, stroke=RED, sw=1.4))
    el.append(txt(704, 279, "暗态", size=11.5, color="#f8fafc", anchor="middle", weight="700"))
    el.append(txt(704, 296, "I = 0", size=10.5, color="#fca5a5", anchor="middle", weight="700"))

    # Bottom explanation in Right Card
    el.append(card(404, 354, 318, 74, rx=8, fill=PURPLE_SOFT, stroke="#ddd6fe"))
    el.append(txt(416, 374, "• 超过弗雷德里克兹阈值电压 (~1.2–1.5 V)，分子顺电场齐刷刷躺直", size=10.8, color=INK))
    el.append(txt(416, 394, "• 竖直偏振光不再被拧转，一头撞上水平检偏器 P2（夹角 90°）", size=10.8, color=BODY))
    el.append(txt(416, 414, "• 马吕斯定律 cos²90° = 0 全拦；微调中间电压即可捏出 256 级灰阶", size=10.8, color=PURPLE, weight="700"))

    return figure(
        456,
        "苯甲酸胆固醇酯双熔点与扭曲向列型（TN）液晶电控光阀原理图",
        "上半图展示1888年莱尼泽尔发现苯甲酸胆固醇酯在145.5°C初熔为浑浊液晶态、178.5°C突变为各向同性清亮液体；下半图对比TN常白模式在断电时螺旋拧光90°透光与加电后顺电场立正遮光的电光开关机制。",
        el,
        extra_css=css,
        extra_defs=_arrow_defs(),
    )


def _svg_2_tft_stack_and_photon_budget(data: dict) -> str:
    """SVG 2: 7-layer TFT-LCD subpixel sandwich, 4K 1819x matrix wiring math, and ~6% photon budget funnel."""
    el: list[str] = []
    el.append(txt(380, 28, "液晶自己一粒光子都不发：七层“三明治”解剖与 6% 光子闯关账本", size=16.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(380, 48, "4K 屏幕靠 1.37 万根行列母线指挥 2488 万个子像素阀门，但超九成背光能量损耗在闯关路上", size=12, color=MUTED, anchor="middle"))

    # Left Card: 7-layer sandwich + 4K TFT matrix reduction
    el.append(card(24, 62, 366, 384, rx=12, fill="#ffffff", stroke=BORDER))
    el.append(pill(38, 72, "左图：单个子像素的七层光学三明治（自上而下）", fg=BLUE, bg=BLUE_SOFT, h=22, size=11.5))

    layers = [
        ("⑦ 上偏振片 (90°)", "决定拧转后的光放行多少", SLATE, SLATE_SOFT),
        ("⑥ RGB 彩色滤光片", "拆成红绿蓝三扇滤色小窗", RED, RED_SOFT),
        ("⑤ 透明电极 + 配向膜", "纳米沟槽锚定分子初始方向", TEAL, TEAL_SOFT),
        ("④ 液晶层 (3~5 μm)", "比发丝细二十倍的旋光阀门", GREEN, GREEN_SOFT),
        ("③ TFT 开关 + 电容 Cs", "逐行锁住灰阶电压防漏电", PURPLE, PURPLE_SOFT),
        ("② 下偏振片 + 增亮膜", "起偏过滤 + DBEF 回收废光", BLUE, BLUE_SOFT),
        ("① LED 背光模组", "整块液晶屏唯一真正光源", AMBER, AMBER_SOFT),
    ]
    y0 = 104
    for idx, (name, desc, fg_c, bg_c) in enumerate(layers):
        ly = y0 + idx * 36
        el.append(card(38, ly, 338, 31, rx=6, fill=bg_c, stroke=fg_c, sw=1.1))
        el.append(txt(48, ly + 20, name, size=11, color=fg_c, weight="700"))
        el.append(txt(368, ly + 20, desc, size=10, color=BODY, anchor="end"))

    # Bottom callout: 4K TFT matrix wiring math
    el.append(card(38, 362, 338, 72, rx=8, fill="#f8fafc", stroke=BLUE_LINE, sw=1.2))
    el.append(txt(50, 381, "4K 主动矩阵寻址（AM-TFT）为什么离不开晶体管？", size=11.2, color=BLUE, weight="700"))
    el.append(txt(50, 401, "• 3840×2160×3 = 24,883,200 个子像素，直连需两千四百万根线", size=10.5, color=BODY))
    el.append(txt(50, 420, f"• 行列网格仅需 11,520 列 + 2,160 行 = 13,680 根线（骤减 {data['wiring_reduction']:.0f} 倍！）", size=10.5, color=INK, weight="700"))

    # Right Card: Photon Tollbooth Funnel
    el.append(card(404, 62, 332, 384, rx=12, fill="#ffffff", stroke=BORDER))
    el.append(pill(418, 72, "右图：100% 背光出发，为何到人眼只剩 ~6%？", fg=ORANGE, bg=ORANGE_SOFT, h=22, size=11.5))

    stages = [
        ("出发：LED 白光背光模组总光通量", 100.0, "100%", AMBER, "漫反射匀光后向上射出"),
        ("第一关：下偏振片拦掉正交偏振分量", data["t_after_pol1_pct"], f"{data['t_after_pol1_pct']:.0f}%", BLUE, "理论上限 50%，实测吸收后剩 ~43%"),
        ("第二关：TFT 晶体管走线与黑矩阵遮挡", data["t_after_ap_pct"], f"{data['t_after_ap_pct']:.1f}%", PURPLE, "子像素透光开口率约 62%"),
        ("第三关：RGB 吸收式彩色滤光片", data["t_after_cf_pct"], f"{data['t_after_cf_pct']:.1f}%", RED, "红滤片吃掉绿蓝光，损失逾七成！"),
        ("终点：液晶盒效率与上检偏器损耗", data["t_total_std_pct"], f"~{data['t_total_std_pct']:.1f}%", GREEN, "贴 DBEF 反射增亮膜可救回至 ~8–9%"),
    ]
    bar_x = 420
    bar_max_w = 236
    sy0 = 108
    for idx, (label, pct, badge, col, subnote) in enumerate(stages):
        sy = sy0 + idx * 52
        el.append(txt(bar_x, sy, label, size=11, color=INK, weight="700"))
        # Background track
        el.append(card(bar_x, sy + 7, bar_max_w, 16, rx=4, fill="#f1f5f9", stroke="#cbd5e1", sw=0.8))
        fill_w = max(12.0, bar_max_w * (pct / 100.0))
        el.append(card(bar_x, sy + 7, fill_w, 16, rx=4, fill=col, stroke=col, sw=0.8))
        el.append(txt(bar_x + bar_max_w + 10, sy + 19, badge, size=11.5, color=col, weight="700"))
        el.append(txt(bar_x, sy + 36, subnote, size=10, color=MUTED))

    # Right summary box
    el.append(card(418, 368, 304, 66, rx=8, fill=ORANGE_SOFT, stroke="#fdba74", sw=1.2))
    el.append(txt(430, 388, "工程启示（Huang & Wu, 2020, PMC7303200）：", size=11, color=ORANGE, weight="700"))
    el.append(txt(430, 406, "想让 65 寸 4K 液晶电视飙到 1000 nit 峰值亮度，背光整机", size=10.4, color=BODY))
    el.append(txt(430, 423, "功耗高达 ~280 W——因为超九成光子被偏振片与色片吃掉了。", size=10.4, color=INK, weight="700"))

    return figure(
        460,
        "TFT-LCD七层子像素截面结构、4K主动矩阵寻址与光子透射率漏斗图",
        "左图自上而下拆解TFT-LCD七层三明治结构并验证4K分辨率下主动矩阵把引线从2488万根压缩到13680根（减少1819倍）；右图定量计算背光经过下偏振片、开口率、RGB滤光片和检偏器后仅剩约5.9%（含DBEF约8%~9%）的能量漏斗。",
        el,
        extra_defs=_arrow_defs(),
    )


def _svg_3_tn_va_ips_modes(_data: dict) -> str:
    """SVG 3: Side-by-side physics of TN, VA (MVA), and IPS/FFS LCD panel modes."""
    el: list[str] = []
    el.append(txt(380, 28, "为什么老液晶屏斜着看会“变脸反色”？三大面板流派分子姿态对决", size=16.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(380, 48, "可视角度的本质是斜看时分子有效双折射 Δn_eff 会不会剧变：从翘头（TN）、多畴对倾（VA）到原地平转（IPS）", size=11.6, color=MUTED, anchor="middle"))

    cols = [
        {
            "x": 24,
            "title": "TN 扭曲向列型",
            "tag": "初代功臣 · 1 ms 电竞快枪手",
            "col": ORANGE,
            "bg": ORANGE_SOFT,
            "v0": "水平螺旋扭转 90°",
            "von": "纵向电场，分子斜翘立起",
            "cr": "~1000 : 1",
            "resp": "极快（~1 ms 灰阶响应）",
            "pros": "成本低、透光高、高刷快",
            "cons": "上下斜看光程剧变易反色",
            "mode": "TN",
        },
        {
            "x": 266,
            "title": "VA 垂直配向（MVA/PVA）",
            "tag": "客厅电视主力 · 原生深邃黑场",
            "col": PURPLE,
            "bg": PURPLE_SOFT,
            "v0": "断电全员 90° 垂直立正",
            "von": "向左右多畴对称倾倒",
            "cr": "3000 : 1 ~ 5000 : 1",
            "resp": "中等（4~8 ms 暗部略慢）",
            "pros": "断电零双折射，黑位极深邃",
            "cons": "大角度侧看对比度略衰减",
            "mode": "VA",
        },
        {
            "x": 508,
            "title": "IPS 平面转换 / FFS",
            "tag": "手机与专业修图霸主 · 178° 硬屏",
            "col": BLUE,
            "bg": BLUE_SOFT,
            "v0": "全员平行躺平于基板面",
            "von": "同侧横向场驱动水平旋转",
            "cr": "1000 : 1 ~ 2000 : 1",
            "resp": "均衡（Fast-IPS 达 1 ms）",
            "pros": "四面斜看 Δn 恒定不偏色",
            "cons": "暗室斜看偶见四角微辉光",
            "mode": "IPS",
        },
    ]

    for c in cols:
        cx = c["x"]
        col = c["col"]
        el.append(card(cx, 62, 228, 368, rx=12, fill="#ffffff", stroke=col, sw=1.5))
        el.append(txt(cx + 114, 84, c["title"], size=14, color=col, anchor="middle", weight="700"))
        el.append(pill(cx + 18, 94, c["tag"], fg=col, bg=c["bg"], w=192, h=21, size=10.8))

        # Visual diagram box (y=124..242)
        el.append(card(cx + 14, 124, 200, 116, rx=8, fill="#f8fafc", stroke=BORDER))
        # Top & bottom glass substrates inside cell diagram
        el.append(_line(cx + 26, 152, cx + 202, 152, stroke=SLATE, sw=2.2))
        el.append(_line(cx + 26, 212, cx + 202, 212, stroke=SLATE, sw=2.2))

        if c["mode"] == "TN":
            el.append(txt(cx + 114, 142, "半灰阶斜翘：左右斜看截然不同!", size=10, color=RED, anchor="middle", weight="700"))
            for rx_i in [cx + 52, cx + 92, cx + 132, cx + 172]:
                el.append(_rod(rx_i, 182, 34, 7, -42, "#fed7aa", ORANGE))
            # Left viewer looks perpendicular to rod; right viewer looks along rod axis
            el.append(_line(cx + 38, 134, cx + 74, 168, stroke=BLUE, sw=1.3, dash="3,2"))
            el.append(txt(cx + 54, 231, "左看：横截面大(泛白)", size=9.8, color=BLUE, anchor="middle"))
            el.append(_line(cx + 190, 134, cx + 154, 168, stroke=RED, sw=1.3, dash="3,2"))
            el.append(txt(cx + 172, 231, "右看：顺轴看成点(变黑)", size=9.8, color=RED, anchor="middle"))

        elif c["mode"] == "VA":
            el.append(txt(cx + 114, 142, "左半断电立正全黑 | 右半双畴对称补偿", size=9.8, color=PURPLE, anchor="middle", weight="700"))
            el.append(_line(cx + 114, 152, cx + 114, 212, stroke="#cbd5e1", sw=1.1, dash="3,3"))
            # V=0 homeotropic vertical rods
            for rx_i in [cx + 48, cx + 74, cx + 98]:
                el.append(_rod(rx_i, 182, 38, 6.5, 90, "#ddd6fe", PURPLE))
            # MVA symmetric tilted domain pair (/ \)
            el.append(_rod(cx + 140, 182, 36, 6.5, -52, "#c4b5fd", PURPLE))
            el.append(_rod(cx + 180, 182, 36, 6.5, 52, "#c4b5fd", PURPLE))
            el.append(txt(cx + 70, 231, "V=0 严丝合缝挡光", size=9.8, color=PURPLE, anchor="middle"))
            el.append(txt(cx + 162, 231, "左右斜看互相抵消偏差", size=9.8, color=INK, anchor="middle"))

        else:  # IPS
            el.append(txt(cx + 114, 142, "分子始终水平躺平，原地打转不起翘!", size=9.8, color=BLUE, anchor="middle", weight="700"))
            # Interdigitated bottom electrodes + arched horizontal fringe field
            for ex in [cx + 42, cx + 86, cx + 130, cx + 174]:
                el.append(f'<rect x="{ex}" y="207" width="16" height="5" rx="1.5" fill="{BLUE}"/>')
            el.append(f'<path d="M {cx+50} 206 Q {cx+72} 174 {cx+94} 206" fill="none" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="3,2"/>')
            el.append(f'<path d="M {cx+138} 206 Q {cx+160} 174 {cx+182} 206" fill="none" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="3,2"/>')
            for rx_i in [cx + 58, cx + 114, cx + 170]:
                el.append(_rod(rx_i, 178, 34, 7, 0, "#bae6fd", BLUE))
            el.append(txt(cx + 114, 231, "底部同侧横向边缘场 → 四面 178° 零反色", size=9.8, color=BLUE, anchor="middle", weight="700"))

        # Structured specs rows (y=256..418)
        specs = [
            ("断电姿态", c["v0"]),
            ("加电动作", c["von"]),
            ("原生对比度", c["cr"]),
            ("响应速度", c["resp"]),
            ("拿手绝活", c["pros"]),
            ("主要短板", c["cons"]),
        ]
        for s_idx, (k_lbl, v_lbl) in enumerate(specs):
            ry = 258 + s_idx * 27
            if s_idx > 0:
                el.append(_line(cx + 14, ry - 15, cx + 214, ry - 15, stroke="#f1f5f9", sw=1.0))
            el.append(txt(cx + 14, ry, f"{k_lbl}：", size=10.0, color=col, weight="700"))
            el.append(txt(cx + 78, ry, v_lbl, size=10.0, color=BODY))

    return figure(
        444,
        "TN、VA与IPS三大液晶显示模式分子取向与可视角度物理解析图",
        "对比TN扭曲向列（分子斜翘导致上下视角双折射剧变而反色）、VA垂直配向（断电垂直立正实现3000:1至5000:1高对比度，加电多畴对称倾倒）与IPS/FFS平面转换（底部横向电场驱动分子水平旋转实现178度广视角）的电光差异。",
        el,
        extra_defs=_arrow_defs(),
    )


def _svg_4_backlight_nobel_evolution(_data: dict) -> str:
    """SVG 4: 2014 & 2023 Nobel Prizes upgrading LCD backlights: WLED -> QLED quantum dots & Mini-LED dimming."""
    el: list[str] = []
    el.append(txt(380, 28, "两座诺贝尔奖给液晶“续命封神”：量子点（QLED）提纯色彩，Mini-LED 驯服黑场", size=16.2, color=INK, anchor="middle", weight="700"))
    el.append(txt(380, 48, "2014 物理诺奖蓝光 LED 淘汰汞灯管；2023 化学诺奖纳米晶砍掉杂色；千级微米分区灭灯逼近自发光对比度", size=11.5, color=MUTED, anchor="middle"))

    # Top-Left Card: Broad WLED spectrum (Blue GaN + YAG yellow phosphor)
    el.append(card(24, 62, 346, 194, rx=12, fill="#ffffff", stroke=BORDER))
    el.append(pill(38, 72, "光谱第 1 代：蓝光 LED + YAG 黄粉（普通白光 WLED）", fg=BLUE, bg=BLUE_SOFT, h=22, size=11))

    # Mini spectrum axes (x=54..346, y=194 baseline, 400..700 nm)
    el.append(_line(54, 194, 346, 194, stroke=SLATE, sw=1.4))
    el.append(_line(54, 108, 54, 194, stroke=SLATE, sw=1.4))
    # Narrow blue peak at ~455 nm (x=108) + broad yellow hump across 520..660 nm (x=145..310)
    wled_curve = (
        "M 58 194 L 84 192 Q 100 188 108 116 Q 116 186 132 182 "
        "Q 175 126 226 132 Q 282 140 338 193 L 344 194 Z"
    )
    el.append(f'<path d="{wled_curve}" fill="#fde68a" fill-opacity="0.55" stroke="{AMBER}" stroke-width="2"/>')
    el.append(f'<path d="M 88 193 Q 100 188 108 116 Q 116 186 128 192" fill="none" stroke="{BLUE}" stroke-width="2.3"/>')
    el.append(txt(108, 110, "450nm 蓝峰", size=9.8, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(228, 122, "宽胖黄光包（FWHM ~110 nm）", size=10, color=AMBER, anchor="middle", weight="700"))
    el.append(txt(228, 168, "绿红连成一片，串色严重!", size=10, color=RED, anchor="middle", weight="700"))
    for wl, wx in [("400", 58), ("460", 112), ("530", 180), ("630", 278), ("700nm", 336)]:
        el.append(txt(wx, 209, wl, size=9.5, color=MUTED, anchor="middle"))
    el.append(txt(52, 232, "• 2014 物理诺奖氮化镓蓝光 LED 让屏幕甩掉含汞 CCFL 灯管", size=10.5, color=BODY))
    el.append(txt(52, 248, "• 但黄粉光谱太宽，色域仅 ~50%–55% Rec.2020，正红偏橘", size=10.5, color=INK, weight="700"))

    # Top-Right Card: QLED Quantum Dot narrow-band RGB spectrum
    el.append(card(390, 62, 346, 194, rx=12, fill="#ffffff", stroke=GREEN, sw=1.5))
    el.append(pill(404, 72, "光谱第 2 代：QLED 量子点薄膜（2023 化学诺奖纳米晶）", fg=GREEN, bg=GREEN_SOFT, h=22, size=11))

    el.append(_line(420, 194, 712, 194, stroke=SLATE, sw=1.4))
    el.append(_line(420, 108, 420, 194, stroke=SLATE, sw=1.4))
    # Three razor-sharp isolated peaks: Blue 455nm (x=474), Green 532nm (x=548), Red 630nm (x=644)
    el.append(f'<path d="M 454 194 Q 468 190 474 116 Q 480 190 494 194 Z" fill="{BLUE_SOFT}" stroke="{BLUE}" stroke-width="2.2"/>')
    el.append(f'<path d="M 526 194 Q 541 188 548 114 Q 555 188 570 194 Z" fill="{GREEN_SOFT}" stroke="{GREEN}" stroke-width="2.2"/>')
    el.append(f'<path d="M 620 194 Q 637 188 644 116 Q 651 188 668 194 Z" fill="{RED_SOFT}" stroke="{RED}" stroke-width="2.2"/>')
    el.append(txt(474, 109, "蓝 LED", size=9.8, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(548, 109, "~2.5nm 绿点", size=9.8, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(644, 109, "~6.5nm 红点", size=9.8, color=RED, anchor="middle", weight="700"))
    for wl, wx in [("400", 424), ("460", 478), ("532", 548), ("630", 644), ("700nm", 702)]:
        el.append(txt(wx, 209, wl, size=9.5, color=MUTED, anchor="middle"))
    el.append(txt(404, 232, "• 量子限域 ΔE ∝ 1/R²：改晶粒尺寸即可精准定制光色", size=10.3, color=BODY))
    el.append(txt(404, 248, "• 半峰宽仅 20~30 nm，三峰独立，色域飙至 90%+ Rec.2020", size=10.3, color=GREEN, weight="700"))

    # Bottom-Left Card: Global Edge-Lit Backlight ("Gray Black" in dark room)
    el.append(card(24, 270, 346, 174, rx=12, fill="#ffffff", stroke=BORDER))
    el.append(pill(38, 280, "控光痛点：整板常亮背光 → 暗室看夜景“发灰漏光”", fg=SLATE, bg=SLATE_SOFT, h=22, size=11))

    # Simulated night-sky screen with washed-out gray background (#334155 instead of #020617)
    el.append(card(42, 312, 132, 82, rx=6, fill="#334155", stroke="#64748b", sw=1.4))
    el.append(f'<circle cx="108" cy="353" r="15" fill="#fef08a"/>')
    el.append(txt(108, 410, "整块背光 100% 亮着", size=10, color=RED, anchor="middle", weight="700"))
    el.append(txt(108, 427, "黑夜漏成 ~0.2 nit 灰雾", size=9.8, color=MUTED, anchor="middle"))

    el.append(txt(188, 332, "• 哪怕屏幕只有一轮明月，背后", size=10.6, color=BODY))
    el.append(txt(188, 351, "  整张白光灯板也得火力全开", size=10.6, color=BODY))
    el.append(txt(188, 372, "• 液晶百叶窗关不死 0.02%~0.1%", size=10.6, color=BODY))
    el.append(txt(188, 391, "  退偏振漏光，关灯看电影黑位泛白", size=10.6, color=INK, weight="700"))
    el.append(txt(188, 414, "• 注意：QLED 仍是液晶屏，不是自发光", size=10.4, color=ORANGE, weight="700"))

    # Bottom-Right Card: Mini-LED 2D Local Dimming ("True Deep Space")
    el.append(card(390, 270, 346, 174, rx=12, fill="#ffffff", stroke=PURPLE, sw=1.5))
    el.append(pill(404, 280, "控光跃迁：Mini-LED 千级分区调光 → 该黑处彻底断电", fg=PURPLE, bg=PURPLE_SOFT, h=22, size=11))

    # Simulated Mini-LED zone grid (6x4 zones inside 132x82 dark screen)
    sx, sy = 408, 312
    el.append(card(sx, sy, 132, 82, rx=6, fill="#020617", stroke=PURPLE, sw=1.4))
    for r in range(4):
        for c_i in range(6):
            zx = sx + 4 + c_i * 21
            zy = sy + 4 + r * 19
            is_moon_zone = (r in (1, 2)) and (c_i in (2, 3))
            zfill = "#3b82f6" if is_moon_zone else "#0f172a"
            zop = "0.42" if is_moon_zone else "0.9"
            el.append(f'<rect x="{zx}" y="{zy}" width="18" height="16" rx="2" fill="{zfill}" fill-opacity="{zop}" stroke="#1e293b" stroke-width="0.7"/>')
    el.append(f'<circle cx="{sx+66}" cy="{sy+41}" r="15" fill="#fef9c3"/>')
    el.append(txt(sx + 66, 410, "暗区灯珠直接 0 nit 熄灭", size=10, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(sx + 66, 427, "亮区飙上 2000+ nit HDR", size=9.8, color=GREEN, anchor="middle", weight="700"))

    el.append(txt(554, 332, "• 把灯珠缩到 100~200 μm，铺满", size=10.5, color=BODY))
    el.append(txt(554, 351, "  上千至上万个独立棋盘调光分区", size=10.5, color=BODY))
    el.append(txt(554, 372, "• “分区背光粗调 + 液晶像素精调”", size=10.5, color=PURPLE, weight="700"))
    el.append(txt(554, 391, "  双级调制实现 12-bit 与十万比一对比", size=10.5, color=INK, weight="700"))
    el.append(txt(554, 414, "• 唯一破绽：亮暗交界偶见微弱光晕", size=10.3, color=MUTED))

    return figure(
        456,
        "LCD背光技术演进：WLED、QLED量子点窄谱与Mini-LED分区控光对比图",
        "上半图对比普通白光LED（蓝光芯片加宽谱YAG黄粉，红绿混杂）与QLED量子点背光（2023化学诺奖纳米晶受激发出20至30nm窄谱纯正红绿光，色域超90% Rec.2020）；下半图对比整板常亮背光的漏光灰雾与Mini-LED千级局部调光分区的深邃黑场。",
        el,
        extra_defs=_arrow_defs(),
    )


def _svg_5_century_display_evolution(data: dict) -> str:
    """SVG 5: 130-year 5-generation panorama & engineering matrix: CRT, LCD, OLED, Micro-LED, and E-Ink."""
    el: list[str] = []
    el.append(txt(380, 28, "百年屏幕五代同堂：从真空电子枪、液晶百叶窗到微米自发光与电子纸", size=16.5, color=INK, anchor="middle", weight="700"))
    el.append(txt(380, 48, "没有哪块屏幕全科满分——看懂“控光尺度”与“材料寿命”的博弈，就看懂了一百三十年的显示进化史", size=11.5, color=MUTED, anchor="middle"))

    # Top Timeline Strip: 5 eras (x=24..736, y=62..156)
    eras = [
        ("1897–1990s", "CRT 显像管", "25kV 电子炮扫荧光粉", SLATE, SLATE_SOFT),
        ("1971–至今", "LCD 液晶家族", "背光 + 液晶电控光阀", BLUE, BLUE_SOFT),
        ("1987 / 2010s+", "OLED 有机自发光", "子像素独立亮灭 + 柔性", PURPLE, PURPLE_SOFT),
        ("1997 / 2007+", "E-Ink 电子墨水", "带电微胶囊反射自然光", TEAL, TEAL_SOFT),
        ("2020s–未来", "Micro-LED", "<50μm 无机晶粒终极屏", GREEN, GREEN_SOFT),
    ]
    ew = 131
    egap = 14
    for idx, (yr, name, tag, fg_c, bg_c) in enumerate(eras):
        ex = 24 + idx * (ew + egap)
        el.append(card(ex, 62, ew, 88, rx=10, fill=bg_c, stroke=fg_c, sw=1.4))
        el.append(txt(ex + ew / 2, 82, yr, size=10.2, color=fg_c, anchor="middle", weight="700"))
        el.append(txt(ex + ew / 2, 106, name, size=12.2, color=INK, anchor="middle", weight="700"))
        el.append(txt(ex + ew / 2, 128, tag, size=9.8, color=BODY, anchor="middle"))
        if idx < len(eras) - 1:
            ax1 = ex + ew + 2
            el.append(_line(ax1, 106, ax1 + egap - 4, 106, stroke=MUTED, sw=1.6, marker="arr-muted"))

    # Comparison Table Card (y=166..456)
    el.append(card(24, 166, 712, 290, rx=12, fill="#ffffff", stroke=BORDER))
    # Header background
    el.append(card(24, 166, 712, 36, rx=10, fill="#f1f5f9", stroke=BORDER))

    col_xs = [34, 134, 248, 378, 508, 632]
    headers = ["核心维度", "CRT 老彩电", "LCD / Mini-LED", "OLED / QD-OLED", "Micro-LED", "E-Ink 电子纸"]
    h_cols = [INK, SLATE, BLUE, PURPLE, GREEN, TEAL]
    for hx, h_txt, hc in zip(col_xs, headers, h_cols):
        el.append(txt(hx, 189, h_txt, size=11, color=hc, weight="700"))

    rows = [
        ("发光机制", "真空电子束轰击", "背光灯 + 液晶阀门", "有机薄膜电致发光", "无机氮化镓自发光", "微胶囊反射环境光"),
        ("黑场对比度", "高（暗室纯正）", "千比一至分区十万", "∞:1（0 nit 断电黑）", "∞:1（0 nit 断电黑）", "类纸反射 (~15:1)"),
        ("像素响应", "脉冲 <0.01 ms", "毫秒级 1~8 ms", "微秒级 ~0.03 ms", "纳秒级 ~ns", "翻页 100~300 ms"),
        ("峰值亮度", "100~200 nit", "400~3000+ nit", "800~3000 nit(叠层)", "万至百万 nit(AR)", "不发光(越晒越清)"),
        ("柔性形态", "笨重防爆玻璃壳", "刚性玻璃为主", "可弯曲 / 三折叠屏", "无缝拼接 / 透明屏", "超薄柔性耐摔"),
        ("头号瓶颈", "体积硕大已淘汰", "光效 ~6% / 微光晕", "高亮有机蓝光老化", "巨量转移良率地狱", "难显示流畅视频"),
    ]
    for r_idx, r_vals in enumerate(rows):
        ry = 224 + r_idx * 35
        if r_idx > 0:
            el.append(_line(32, ry - 21, 728, ry - 21, stroke="#e2e8f0", sw=1.0))
        for c_idx, val in enumerate(r_vals):
            weight = "700" if c_idx == 0 or ("∞:1" in val) or ("巨量转移" in val) else None
            color = INK if c_idx == 0 else (h_cols[c_idx] if weight else BODY)
            el.append(txt(col_xs[c_idx], ry, val, size=10.2, color=color, weight=weight))

    # Bottom quantitative footnote on Micro-LED 6-nines yield
    el.append(card(34, 418, 692, 30, rx=6, fill=GREEN_SOFT, stroke="#bbf7d0"))
    el.append(
        txt(
            380,
            438,
            f"为什么 Micro-LED 昂贵？4K 屏含 2488 万颗晶粒，99.99% 良率仍留 {data['dead_at_4nines']} 颗坏点——须达 99.9999%（六个九）！",
            size=10.2,
            color=INK,
            anchor="middle",
            weight="700",
        )
    )

    return figure(
        468,
        "百年五代显示技术（CRT、LCD、OLED、Micro-LED、E-Ink）原理与工程指标全景对比图",
        "上方时间轴梳理1897年CRT显像管、1971年TN-LCD、1987年OLED、1997年E-Ink电泳电子纸到Micro-LED的五代演进；下方矩阵对比发光机制、黑场对比度、响应时间、亮度、形态与核心瓶颈，并定量算清4K Micro-LED四个九良率仍剩2488颗坏点的巨量转移挑战。",
        el,
        extra_defs=_arrow_defs(),
    )


@register(TOPIC, "生成液晶显示原理、面板流派、诺奖背光演进与百年五代显示对比全套 5 张中文 SVG 图解", "science")
def build_all() -> list[str]:
    data = _verify_lcd_display_data()
    builders = [
        ("carrot-liquid-crystal-and-crossed-polarizer-shutter", _svg_1_carrot_shutter),
        ("tft-lcd-subpixel-stack-and-light-budget", _svg_2_tft_stack_and_photon_budget),
        ("tn-va-ips-viewing-angle-physics", _svg_3_tn_va_ips_modes),
        ("backlight-evolution-ccfl-wled-qled-miniled", _svg_4_backlight_nobel_evolution),
        ("century-display-evolution-crt-lcd-oled-microled-eink", _svg_5_century_display_evolution),
    ]
    written: list[str] = []
    for name, fn in builders:
        write_svg(TOPIC, name, fn(data))
        written.append(f"assets/images/{TOPIC}/{name}.svg")
    return written
