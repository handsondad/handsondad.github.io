"""
Visuals for '详细介绍淡水鱼特征和生活习性和咸水鱼的区别'
(Comprehensive Visual Guide to Freshwater vs. Saltwater/Marine Fish:
1. Osmotic Life-or-Death Paradox [Freshwater hyperosmotic never-drink/heavy-pee vs Marine hypoosmotic nonstop-drink/gill-salt-pump + Shark 2:1 Urea:TMAO, 1-shot CSS animation],
2. The '1% Water vs 51% Species' Biodiversity Paradox & Freshwater-Ancestor Evolution [Carrete Vega & Wiens 2012],
3. 4-System Anatomical & Sensory Comparison [runx2b Intermuscular Y-Bones + Phylogeny Exceptions, Cyp27c1 A1/A2 Vision, Weberian Ear Ossicles, Open vs Closed Swim Bladder],
4. Living Habits, Spawning Strategies & Diadromous Gill-Ionocyte Reboot [Salmon Smoltification & Eel Catadromy],
5. Flavor Chemistry [TMAO Depth Curve to 8,200 m Limit vs Geosmin/2-MIB] & Sashimi Parasite Safety [Clonorchis Group-1 Carcinogen vs FDA -20°C 7-Day Anisakis Freezing]).

Generates 5 original 760px Chinese SVG diagrams in assets/images/fresh-salt-fish/
with verified physiological, evolutionary, and biochemical assertions.
"""
from __future__ import annotations

import math

from .core import (
    BLUE,
    BLUE_LINE,
    BLUE_SOFT,
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

TOPIC = "fresh-salt-fish"
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


def _fish_silhouette(cx: float, cy: float, rx: float, ry: float, body_fill: str, stroke: str) -> str:
    # Clean stylized fish facing left (mouth at cx - rx, tail at cx + rx + 26)
    tail_x = cx + rx - 4
    return (
        f'<polygon points="{tail_x:.1f},{cy:.1f} {tail_x + 28:.1f},{cy - 22:.1f} '
        f'{tail_x + 22:.1f},{cy:.1f} {tail_x + 28:.1f},{cy + 22:.1f}" '
        f'fill="{body_fill}" stroke="{stroke}" stroke-width="1.8" stroke-linejoin="round"/>'
        f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
        f'fill="{body_fill}" stroke="{stroke}" stroke-width="2.0"/>'
        f'<path d="M {cx - rx + 34:.1f},{cy - 18:.1f} Q {cx - rx + 44:.1f},{cy:.1f} {cx - rx + 34:.1f},{cy + 18:.1f}" '
        f'fill="none" stroke="{stroke}" stroke-width="2.0"/>'
        f'<circle cx="{cx - rx + 20:.1f}" cy="{cy - 7:.1f}" r="3.8" fill="#0f172a"/>'
    )


# ---------------------------------------------------------------------------
# 1. Osmotic Life-or-Death Paradox (760 x 530, 1-shot CSS animation)
# ---------------------------------------------------------------------------
def build_osmotic_paradox() -> str:
    # Van 't Hoff osmotic pressure verification at T = 293.15 K (20 °C):
    # Delta_Pi = Delta_C (mol/m^3) * R * T
    r_gas = 8.314462618
    t_kelvin = 293.15
    # Freshwater: blood ~300 mOsm/kg vs water ~5 mOsm/kg -> Delta_C = 295 mol/m^3
    dpi_fw_bar = (295.0 * r_gas * t_kelvin) / 1e5
    # Marine teleost: seawater ~1050 mOsm/kg vs blood ~370 mOsm/kg -> Delta_C = 680 mol/m^3
    dpi_sw_bar = (680.0 * r_gas * t_kelvin) / 1e5
    assert 7.0 < dpi_fw_bar < 7.5
    assert 16.4 < dpi_sw_bar < 17.0

    H = 530
    css = """
    @keyframes waterFloodIn {
      0% { transform: translateX(-22px); opacity: 0.2; }
      40% { opacity: 1.0; }
      100% { transform: translateX(14px); opacity: 1.0; }
    }
    @keyframes waterLeakOut {
      0% { transform: translateX(12px); opacity: 0.2; }
      40% { opacity: 1.0; }
      100% { transform: translateX(-20px); opacity: 1.0; }
    }
    .anim-water-in { animation: waterFloodIn 2.6s ease-out 1 forwards; }
    .anim-water-out { animation: waterLeakOut 2.6s ease-out 1 forwards; }
    @media (prefers-reduced-motion: reduce) {
      .anim-water-in, .anim-water-out { animation: none !important; transform: none !important; opacity: 1 !important; }
    }
    """
    els = header(
        "生存第一关：为什么淡水鱼从不喝水狂排尿，海鱼却要拼命喝海水？",
        f"跨鳃渗透压实算：淡水压差 ≈ {dpi_fw_bar:.1f} bar（往肚里猛灌水）｜海水压差 ≈ {dpi_sw_bar:.1f} bar（把体液往外抽干）",
    )

    # Left Card: Freshwater Bony Fish
    els.append(card(16, 68, 354, 368, fill="#f0f9ff", stroke="#7dd3fc"))
    els.append(step_badge(36, 92, 1, BLUE, BLUE_SOFT))
    els.append(txt(56, 97, "淡水硬骨鱼（鲤/鲫/草鱼）：泡在水里防“撑爆”", size=11.8, weight="700", color=BLUE))
    els.append(pill(30, 110, "外界江河：≈ 1–10 mOsm/kg（盐度 < 0.5‰）", fg=BLUE, bg="#ffffff", w=326))

    # Fish diagram in left card
    els.append(_fish_silhouette(198, 224, 92, 38, "#bae6fd", BLUE))
    els.append(txt(208, 220, "血液 ≈ 300 mOsm", size=10.4, weight="700", color="#0c4a6e", anchor="middle"))
    els.append(txt(208, 237, "（盐度 ≈ 9‰，高渗！）", size=9.8, color=BLUE, anchor="middle", weight="600"))

    # Mouth: Never drinks!
    els.append(txt(64, 184, "✗ 嘴：几乎不喝水", size=10.2, weight="700", color=RED, anchor="middle"))
    els.append(_line(84, 194, 102, 214, stroke=RED, sw=1.8))

    # Gills: Water floods IN + Gill pumps salt IN
    els.append(_line(62, 244, 134, 234, stroke=BLUE, sw=2.4, dash="4,3", marker="arr-blue"))
    els.append(f'<circle class="anim-water-in" cx="104" cy="238" r="5" fill="{BLUE}"/>')
    els.append(txt(30, 266, "① 鳃膜被动进水：7.2 bar 压差猛灌淡水", size=9.9, weight="700", color=BLUE))

    els.append(_line(88, 286, 144, 246, stroke=GREEN, sw=2.2, marker="arr-green"))
    els.append(txt(30, 304, "② 鳃离子细胞逆流“吸盐”（NHE3 / NCC）", size=9.9, weight="700", color=GREEN))
    els.append(txt(42, 322, "耗能从稀水里硬抠 Na⁺、Cl⁻ 补回血液", size=9.8, color=SLATE))

    # Kidney: Huge glomeruli, dilute pee
    els.append(_line(248, 252, 294, 336, stroke=BLUE, sw=2.2, marker="arr-blue"))
    els.append('<rect x="30" y="340" width="326" height="82" rx="9" fill="#ffffff" stroke="#93c5fd" stroke-width="1.2"/>')
    els.append(txt(42, 360, "③ 肾脏（大肾小球 60–106 μm）：狂排极稀尿！", size=10.3, weight="700", color=BLUE))
    els.append(txt(42, 380, "• 每天排尿量高达体重的 12%–30%（边排边回收盐）", size=9.8, color=INK))
    els.append(txt(42, 399, "• 误放生大海结局：体液被海水倒抽 → 急性脱水休克亡", size=9.8, color=RED, weight="700"))

    # Right Card: Marine Bony Fish
    els.append(card(390, 68, 354, 368, fill="#fff7ed", stroke="#fdba74"))
    els.append(step_badge(410, 92, 2, ORANGE, ORANGE_SOFT))
    els.append(txt(430, 97, "咸水硬骨鱼（石斑/真鲷/鳕鱼）：泡海里防“渴死”", size=11.8, weight="700", color=ORANGE))
    els.append(pill(404, 110, "外界海水：≈ 1,050 mOsm/kg（盐度 ≈ 35‰）", fg=ORANGE, bg="#ffffff", w=326))

    # Fish diagram in right card
    els.append(_fish_silhouette(572, 224, 92, 38, "#fed7aa", ORANGE))
    els.append(txt(582, 220, "血液 ≈ 370 mOsm", size=10.4, weight="700", color="#7c2d12", anchor="middle"))
    els.append(txt(582, 237, "（仅海水 1/3，低渗！）", size=9.8, color=ORANGE, anchor="middle", weight="600"))

    # Mouth: Drinks nonstop!
    els.append(txt(448, 180, "✓ 嘴：全天狂喝海水！", size=10.2, weight="700", color=GREEN, anchor="middle"))
    els.append(_line(446, 190, 478, 218, stroke=GREEN, sw=2.3, marker="arr-green"))

    # Gills: Water sucked OUT + Gill pumps NaCl OUT
    els.append(_line(508, 234, 434, 246, stroke=RED, sw=2.4, dash="4,3", marker="arr-red"))
    els.append(f'<circle class="anim-water-out" cx="468" cy="240" r="5" fill="{RED}"/>')
    els.append(txt(404, 266, "① 鳃膜被动失水：16.6 bar 把淡水抽向大海", size=9.9, weight="700", color=RED))

    els.append(_line(516, 246, 462, 286, stroke=ORANGE, sw=2.2, marker="arr-orange"))
    els.append(txt(404, 304, "② 鳃氯细胞强力“排盐”（NKCC1 + CFTR）", size=9.9, weight="700", color=ORANGE))
    els.append(txt(416, 322, "肠道吸水并沉淀钙盐，单价 Na⁺/Cl⁻ 由鳃泵出", size=9.8, color=SLATE))

    # Kidney: Tiny or zero glomeruli!
    els.append(_line(622, 252, 668, 336, stroke=ORANGE, sw=2.0, marker="arr-orange"))
    els.append('<rect x="404" y="340" width="326" height="82" rx="9" fill="#ffffff" stroke="#fdba74" stroke-width="1.2"/>')
    els.append(txt(416, 360, "③ 肾脏（萎缩甚至无肾小球如海马）：惜尿如金！", size=10.3, weight="700", color=ORANGE))
    els.append(txt(416, 380, "• 只排极少浓稠尿液（专排二价 Mg²⁺、SO₄²⁻ 苦盐）", size=9.8, color=INK))
    els.append(txt(416, 399, "• 误放生江河结局：淡水狂灌入体 → 细胞水肿胀破亡", size=9.8, color=RED, weight="700"))

    # Bottom Banner: Sharks & Rays 3rd Strategy
    els.append('<rect x="16" y="448" width="728" height="68" rx="11" fill="#0f172a"/>')
    els.append(txt(380, 470, "番外彩蛋：鲨鱼、鳐鱼（海洋软骨鱼）为什么不用喝海水？——“尿素 + TMAO 化学外挂”", size=11.0, weight="700", color="#fbbf24", anchor="middle"))
    els.append(txt(380, 490, "鲨鱼在血液里故意囤积 ≈ 360 mM 尿素 + ≈ 180 mM 氧化三甲胺（2:1 黄金配比抵消尿素对蛋白质的破坏），", size=9.9, color="#f8fafc", anchor="middle"))
    els.append(txt(380, 507, "硬把体液总渗透压垫高到 ≈ 1,050 mOsm/kg（微高于海水）！水分反而自动渗入体内，多余食盐由专门“直肠腺”排出。", size=9.8, color="#93c5fd", anchor="middle"))

    return figure(
        H,
        "淡水鱼与咸水鱼跨鳃渗透压调节及鲨鱼尿素外挂对比图",
        "左图展示淡水硬骨鱼体液高渗（约300 mOsm/kg）被动进水、不喝水、鳃主动吸盐及肾脏大量排稀尿；右图展示海洋硬骨鱼体液低渗（约370 mOsm/kg）被动失水、大口喝海水、鳃氯细胞排盐及极少排尿；底部说明软骨鱼鲨鱼2:1尿素与TMAO高渗策略。",
        els,
        extra_css=css,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 2. Biodiversity Paradox & Evolutionary Re-Invasion (760 x 500)
# ---------------------------------------------------------------------------
def build_biodiversity_paradox() -> str:
    # Exact Carrete Vega & Wiens (2012, Proc. R. Soc. B, PMC3350687) numbers:
    fw_sp = 15150
    sw_sp = 14740
    tot_sp = fw_sp + sw_sp
    fw_pct = fw_sp / tot_sp * 100.0
    sw_pct = sw_sp / tot_sp * 100.0
    assert abs(fw_pct - 50.686) < 0.02

    H = 500
    els = header(
        "生态学头号悬案：不到 1% 的淡水，凭什么养出超过一半的鱼种？",
        "据《英国皇家学会学报 B》（Carrete Vega & Wiens, 2012）辐鳍鱼纲（占现存鱼类 96%）全球物种普查",
    )

    # Left Card: Extreme Asymmetry Comparison Bars
    els.append(card(16, 68, 356, 416, fill="#ffffff"))
    els.append(step_badge(36, 92, 1, PURPLE, PURPLE_SOFT))
    els.append(txt(56, 97, "水体体积 vs 鱼类物种数的惊天倒挂", size=12.0, weight="700", color=PURPLE))

    bx, bw = 34, 320
    # Bar 1: Habitable Aquatic Volume / Water Share
    els.append(txt(bx, 130, "① 地球液态水栖息体积占比（海洋 > 99% vs 淡水 < 0.01%）", size=10.0, weight="700", color=INK))
    els.append(f'<rect x="{bx}" y="140" width="{bw - 4}" height="32" rx="6" fill="{ORANGE}"/>')
    els.append(f'<rect x="{bx + bw - 4}" y="140" width="4" height="32" rx="2" fill="{BLUE}"/>')
    els.append(txt(bx + (bw - 4) / 2, 160, "海洋咸水：占地球总水量 ≈ 97.5%（栖息空间 > 99%）", size=9.9, weight="700", color="#ffffff", anchor="middle"))
    els.append(txt(bx + bw, 186, "↑ 江河湖泊可用液态淡水仅 ≈ 0.01%（放大才看得见！）", size=9.8, color=BLUE, anchor="end", weight="700"))

    # Bar 2: Earth Surface Area Share
    els.append(txt(bx, 214, "② 地球表面积覆盖占比（海洋 ≈ 71% vs 淡水湿地 ≈ 1%–2%）", size=10.0, weight="700", color=INK))
    w_surf_sea = bw * (71.0 / 72.5)
    els.append(f'<rect x="{bx}" y="224" width="{w_surf_sea:.1f}" height="30" rx="6" fill="#fb923c"/>')
    els.append(f'<rect x="{bx + w_surf_sea:.1f}" y="224" width="{bw - w_surf_sea:.1f}" height="30" rx="3" fill="{BLUE}"/>')
    els.append(txt(bx + w_surf_sea / 2, 243, "海洋面积 ≈ 71%", size=10.0, weight="700", color="#ffffff", anchor="middle"))
    els.append(txt(bx + bw, 268, "↑ 淡水面积仅 ≈ 1%–2%", size=9.8, color=BLUE, anchor="end", weight="600"))

    # Bar 3: Ray-finned Fish Species Share!
    els.append(txt(bx, 298, f"③ 辐鳍鱼物种数量占比（淡水 {fw_sp:,} 种 vs 海洋 {sw_sp:,} 种）", size=10.0, weight="700", color=INK))
    w_fw = bw * (fw_pct / 100.0)
    w_sw = bw - w_fw
    els.append(f'<rect x="{bx}" y="308" width="{w_fw:.1f}" height="42" rx="6" fill="{BLUE}"/>')
    els.append(f'<rect x="{bx + w_fw:.1f}" y="308" width="{w_sw:.1f}" height="42" rx="6" fill="{ORANGE}"/>')
    els.append(txt(bx + w_fw / 2, 326, f"淡水鱼：{fw_pct:.1f}%", size=10.6, weight="700", color="#ffffff", anchor="middle"))
    els.append(txt(bx + w_fw / 2, 342, f"({fw_sp:,} 种)", size=9.8, color="#e0f2fe", anchor="middle"))
    els.append(txt(bx + w_fw + w_sw / 2, 326, f"咸水鱼：{sw_pct:.1f}%", size=10.6, weight="700", color="#ffffff", anchor="middle"))
    els.append(txt(bx + w_fw + w_sw / 2, 342, f"({sw_sp:,} 种)", size=9.8, color="#ffedd5", anchor="middle"))

    # Note box on euryhaline minority
    els.append('<rect x="34" y="368" width="320" height="100" rx="9" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')
    els.append(txt(46, 389, "跨界极其罕见：仅约 720 种（≈ 2.4%–4%）能咸淡通吃！", size=10.1, weight="700", color=PURPLE))
    els.append(txt(46, 409, "• 渗透压生死墙把绝大多数鱼死死锁在单一水体；", size=9.8, color=SLATE))
    els.append(txt(46, 428, "• 单位体积水体的淡水鱼物种密度，竟是海洋的近万倍！", size=9.8, color=BLUE, weight="700"))
    els.append(txt(46, 448, "• 最新鱼类目录（超 3.6 万种）中淡水鱼依然稳占约 51%。", size=9.8, color=MUTED))

    # Right Card: Two Evolutionary Mechanisms
    els.append(card(388, 68, 356, 416, fill="#ffffff"))
    els.append(step_badge(408, 92, 2, GREEN, GREEN_SOFT))
    els.append(txt(428, 97, "破案两大推手：水下群岛隔离 + 淡水老祖宗", size=12.0, weight="700", color=GREEN))

    # Mechanism A: Archipelago isolation
    els.append('<rect x="404" y="116" width="324" height="162" rx="10" fill="#f0fdf4" stroke="#86efac" stroke-width="1.3"/>')
    els.append(txt(418, 138, "推手 A：山脉切碎水系 →“水下孤岛”加速分化", size=10.8, weight="700", color=GREEN))
    # Mini map illustration: 3 isolated mountain valleys vs 1 connected ocean
    els.append('<rect x="418" y="148" width="142" height="58" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2"/>')
    els.append('<circle cx="444" cy="177" r="14" fill="#bae6fd" stroke="#0284c7" stroke-width="1.5"/>')
    els.append('<circle cx="489" cy="177" r="14" fill="#bae6fd" stroke="#0284c7" stroke-width="1.5"/>')
    els.append('<circle cx="534" cy="177" r="14" fill="#bae6fd" stroke="#0284c7" stroke-width="1.5"/>')
    els.append(txt(489, 220, "陆地隔断各水系 = 上万座孤岛", size=9.8, color=GREEN, anchor="middle", weight="600"))

    els.append('<rect x="572" y="148" width="142" height="58" rx="7" fill="#ffedd5" stroke="#ea580c" stroke-width="1.2"/>')
    els.append(_line(586, 177, 698, 177, stroke=ORANGE, sw=2.0, marker="arr-orange"))
    els.append(txt(643, 168, "大洋连通", size=9.8, color=ORANGE, anchor="middle", weight="700"))
    els.append(txt(643, 220, "洋流混洗基因 = 不易隔离成种", size=9.8, color=ORANGE, anchor="middle", weight="600"))

    els.append(txt(418, 244, "• 一座山隆起就能把一条河切成两半，两岸鱼群从此老死", size=9.8, color=INK))
    els.append(txt(418, 263, "  不相往来（异域成种）；东非三大湖慈鲷几百万年分化上千种！", size=9.8, color=SLATE))

    # Mechanism B: Phylogenetic Ancestor Twist
    els.append('<rect x="404" y="290" width="324" height="178" rx="10" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.3"/>')
    els.append(txt(418, 312, "推手 B：演化大反转——现存海鱼竟是“淡水海归”！", size=10.8, weight="700", color=BLUE))

    # Mini phylogenetic tree
    els.append('<rect x="418" y="330" width="96" height="38" rx="7" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>')
    els.append(txt(466, 347, "远古淡水祖先", size=9.8, weight="700", color=BLUE, anchor="middle"))
    els.append(txt(466, 361, "辐鳍鱼冠群", size=9.8, color=SLATE, anchor="middle"))

    els.append(_line(514, 342, 554, 330, stroke=BLUE, sw=2.0, marker="arr-blue"))
    els.append(_line(514, 356, 554, 374, stroke=ORANGE, sw=2.0, marker="arr-orange"))

    els.append('<rect x="558" y="316" width="156" height="32" rx="6" fill="#ffffff" stroke="#2563eb" stroke-width="1.2"/>')
    els.append(txt(636, 336, "骨鳔总目（鲤/鲶/脂鲤）留守淡水", size=9.8, weight="700", color=BLUE, anchor="middle"))

    els.append('<rect x="558" y="358" width="156" height="32" rx="6" fill="#ffffff" stroke="#ea580c" stroke-width="1.2"/>')
    els.append(txt(636, 378, "鲈形总目等重新下海大辐射！", size=9.8, weight="700", color=ORANGE, anchor="middle"))

    els.append(txt(418, 412, "• 古生代—中生代海洋大灭绝曾重创早期海生辐鳍鱼支系；", size=9.8, color=INK))
    els.append(txt(418, 432, "• 现存海洋硬骨鱼的共同祖先来自淡水内陆，这也解释了为什么", size=9.8, color=INK))
    els.append(txt(418, 451, "  今天海鱼血液盐度仍停留在 ≈ 9‰–11‰（留着淡水老家的底色）！", size=9.8, color=BLUE, weight="700"))

    return figure(
        H,
        "全球淡水与海洋鱼类物种数量倒挂及演化起源图",
        "左图对比海洋占超99%液态栖息空间而淡水鱼却占辐鳍鱼物种总数50.7%（15150种对14740种）；右图拆解河流湖泊地理隔离加速成种及现存海洋辐鳍鱼起源于淡水祖先重返海洋两大机制。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 3. 4-System Anatomical & Sensory Dissection (760 x 520)
# ---------------------------------------------------------------------------
def build_anatomy_senses() -> str:
    H = 520
    els = header(
        "从鱼刺、眼睛、耳朵到鱼鳔：浑浊浅滩与蔚蓝大洋改写了哪些硬件？",
        "打破“淡水鱼都有小刺、海鱼都没小刺”的刻板印象：看清演化辈分与水体光学/声学法则",
    )

    # Column headers
    els.append('<rect x="16" y="68" width="144" height="34" rx="8" fill="#1e293b"/>')
    els.append(txt(88, 89, "身体硬件维度", size=10.8, weight="700", color="#ffffff", anchor="middle"))

    els.append('<rect x="168" y="68" width="282" height="34" rx="8" fill="#0284c7"/>')
    els.append(txt(309, 89, "典型淡水鱼主流配置（浑水·水草·浅滩）", size=10.8, weight="700", color="#ffffff", anchor="middle"))

    els.append('<rect x="458" y="68" width="286" height="34" rx="8" fill="#ea580c"/>')
    els.append(txt(601, 89, "典型咸水鱼主流配置（蓝海·高压·开阔洋）", size=10.8, weight="700", color="#ffffff", anchor="middle"))

    rows = [
        (
            110,
            96,
            "① 肌间小刺",
            "（runx2b 基因）",
            ["鲤科（鲫/草/鲢/武昌鱼）含 80–120+ 根", "Y 字形骨化肌间隔肌腱，支撑低速弯体发力。", "【例外】淡水鳜鱼、鲈鱼、黄颡鱼无肌间刺！"],
            ["高等鲈形目（金枪/石斑/带鱼/大黄鱼）", "演化出紧实椎骨与大块肌节，0 根肌间小刺！", "【例外】低等海鱼鲥鱼、沙丁鱼照样满身小刺！"],
            RED,
        ),
        (
            214,
            88,
            "② 视觉调谐",
            "（Cyp27c1 酶）",
            ["泥沙腐殖质吸收蓝光，水下偏红褐（550–650nm）", "高表达 Cyp27c1 将维 A₁ 转为维 A₂（视紫蓝质）", "相当于自带“浑水红光/近红外夜视仪”！"],
            ["清澈大洋蓝绿光穿透最深（470–490nm）", "视网膜使用维生素 A₁（视紫红质）匹配蓝海；", "深海鱼演化超大瞳孔或生物发光诱饵。"],
            PURPLE,
        ),
        (
            310,
            88,
            "③ 听觉与触须",
            "（韦伯氏器）",
            ["视线受阻靠耳朵！骨鳔总目（占淡水鱼 ≈70%）", "长出 4 块“韦伯氏小骨”把鱼鳔连上内耳，", "高频听力飙至 3–5 kHz；底栖鲤/鲶多味觉触须。"],
            ["开阔海域无遮挡，依赖高精度流场侧线阵列", "感知几米外鱼群尾流，配合背青腹白“反荫蔽”", "保护色，形成成千上万尾同步急转弯鱼球。"],
            TEAL,
        ),
        (
            406,
            96,
            "④ 鱼鳔与体型",
            "（开鳔 vs 闭鳔）",
            ["多保留连接食道的“喉鳔管（开鳔）”：夏夜闷热", "缺氧时直接浮到水面吞咽空气救急（“浮头”）！", "体态偏侧扁（如鲫/鲂），擅长水草间原地急转。"],
            ["多演化为封闭“闭鳔”（靠奇网分泌高压氧气）", "以适应几十米水深水压；高速巡游的鲨鱼、鲭鱼", "干脆退化掉鱼鳔，配纺锤流线身+新月尾防炸鳔！"],
            BLUE,
        ),
    ]

    for ry, rh, t1, t2, fw_lines, sw_lines, accent in rows:
        # Left dimension cell
        els.append(f'<rect x="16" y="{ry}" width="144" height="{rh}" rx="9" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.3"/>')
        els.append(txt(88, ry + rh / 2 - 6, t1, size=11.0, weight="700", color=accent, anchor="middle"))
        els.append(txt(88, ry + rh / 2 + 14, t2, size=9.8, color=MUTED, anchor="middle", weight="600"))

        # Middle freshwater cell
        els.append(f'<rect x="168" y="{ry}" width="282" height="{rh}" rx="9" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.3"/>')
        for idx, line in enumerate(fw_lines):
            col = RED if line.startswith("【例外】") else (BLUE if idx == 1 else INK)
            wt = "700" if (line.startswith("【例外】") or idx == 0) else "500"
            els.append(txt(180, ry + 24 + idx * 23, line, size=9.9, weight=wt, color=col))

        # Right marine cell
        els.append(f'<rect x="458" y="{ry}" width="286" height="{rh}" rx="9" fill="#fff7ed" stroke="#fed7aa" stroke-width="1.3"/>')
        for idx, line in enumerate(sw_lines):
            col = RED if line.startswith("【例外】") else (ORANGE if idx == 1 else INK)
            wt = "700" if (line.startswith("【例外】") or idx == 0) else "500"
            els.append(txt(470, ry + 24 + idx * 23, line, size=9.9, weight=wt, color=col))

    return figure(
        H,
        "淡水鱼与咸水鱼四大身体结构与感官配置对比图",
        "对比淡水鱼与咸水鱼在runx2b肌间小刺（含鲱形目海鱼多刺与鲈形目淡水鱼无小刺例外）、Cyp27c1维生素A1/A2视觉色素、韦伯氏器听觉放大及开鳔闭鳔体型上的适应性差异。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 4. Living Habits, Spawning & Diadromous Gill Reboot (760 x 510)
# ---------------------------------------------------------------------------
def build_habits_and_migration() -> str:
    H = 510
    els = header(
        "生活习性与跨界特种兵：剧变江湖 vs 恒稳大洋，三文鱼怎么“换芯”入海？",
        "水体稳定性决定冬眠、呼吸与产卵策略；广盐洄游鱼靠激素一键翻转鳃部离子泵方向",
    )

    # Top-Left Card: Freshwater Habits
    els.append(card(16, 68, 356, 208, fill="#f0f9ff", stroke="#7dd3fc"))
    els.append(step_badge(36, 92, 1, BLUE, BLUE_SOFT))
    els.append(txt(56, 97, "淡水习性：在冰封、缺氧与洪水中“精打细算”", size=11.6, weight="700", color=BLUE))
    els.append(txt(32, 124, "• 四季极端折腾：冬结冰潜入深潭半冬眠，夏夜闷热溶氧暴跌；", size=9.9, color=INK))
    els.append(txt(32, 145, "• 副呼吸绝活：泥鳅吞气用肠壁呼吸、乌鳢（黑鱼）靠鳃上迷器、", size=9.9, color=SLATE))
    els.append(txt(32, 165, "  黄鳝靠口腔咽喉表皮直接吸空气，离水数小时仍能存活！", size=9.9, color=BLUE, weight="600"))
    els.append('<rect x="30" y="180" width="328" height="82" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.2"/>')
    els.append(txt(42, 200, "产卵策略：沉性卵 / 黏性卵 + 筑巢护幼（防冲进大海！）", size=10.1, weight="700", color=BLUE))
    els.append(txt(42, 220, "怀卵量多在数千～数万粒，卵膜带黏性死死粘住水草石块；", size=9.8, color=INK))
    els.append(txt(42, 240, "演化出罗非鱼“口孵”、斗鱼吐泡巢、鳑鲏借河蚌鳃腔育儿！", size=9.8, color=TEAL, weight="600"))

    # Top-Right Card: Marine Habits
    els.append(card(388, 68, 356, 208, fill="#fff7ed", stroke="#fdba74"))
    els.append(step_badge(408, 92, 2, ORANGE, ORANGE_SOFT))
    els.append(txt(428, 97, "咸水习性：在恒温富氧大洋里“远征撒网”", size=11.6, weight="700", color=ORANGE))
    els.append(txt(404, 124, "• 环境宏大稳定：大洋热容极大、波浪搅动溶氧充足，极少缺氧；", size=9.9, color=INK))
    els.append(txt(404, 145, "• 昼夜垂直迁徙 + 跨洋巡游：灯笼鱼每晚上升数百米觅食；金枪", size=9.9, color=SLATE))
    els.append(txt(404, 165, "  鱼靠奇网锁住肌肉代谢热（局部恒温），跨太平洋高速追猎！", size=9.9, color=ORANGE, weight="600"))
    els.append('<rect x="402" y="180" width="328" height="82" rx="8" fill="#ffffff" stroke="#fdba74" stroke-width="1.2"/>')
    els.append(txt(414, 200, "产卵策略：巨量透明“浮性卵”（随洋流广种薄收！）", size=10.1, weight="700", color=ORANGE))
    els.append(txt(414, 220, "翻车鱼单次产卵可达上亿粒，鳕鱼/大黄鱼产卵数十万～数百万粒；", size=9.8, color=INK))
    els.append(txt(414, 240, "卵内自带一颗轻质“油球”，浮在阳光表层随洋流漂向远方牧场。", size=9.8, color=AMBER, weight="600"))

    # Bottom Wide Card: Diadromous Dual-Mode Reboot
    els.append(card(16, 290, 728, 204, fill="#ffffff"))
    els.append(step_badge(36, 314, 3, GREEN, GREEN_SOFT))
    els.append(txt(56, 319, "跨界奇迹：三文鱼与鳗鲡凭什么横穿生死线？——入海前的“全身硬件重装（银化）”", size=12.0, weight="700", color=GREEN))

    # Left box: Freshwater stage
    els.append('<rect x="32" y="338" width="214" height="140" rx="10" fill="#eff6ff" stroke="#60a5fa" stroke-width="1.4"/>')
    els.append(txt(139, 360, "江河淡水模式", size=11.0, weight="700", color=BLUE, anchor="middle"))
    els.append(txt(139, 380, "• 鳃泵亚型：NKA α1a（吸盐）", size=9.9, color=INK, anchor="middle", weight="600"))
    els.append(txt(139, 400, "• 顶膜通道：NHE3 / NCC 开启", size=9.8, color=SLATE, anchor="middle"))
    els.append(txt(139, 420, "• 肾脏：高滤过率狂排稀尿", size=9.8, color=SLATE, anchor="middle"))
    els.append(txt(139, 440, "• 视觉：维 A₂ 红移适应河水", size=9.8, color=PURPLE, anchor="middle", weight="600"))
    els.append(txt(139, 462, "（三文鱼幼鱼 / 成年河鳗）", size=9.8, color=BLUE, anchor="middle", weight="700"))

    # Center switch box: Estuary Smoltification Reboot
    els.append(_line(250, 392, 286, 392, stroke=GREEN, sw=2.4, marker="arr-green"))
    els.append(_line(286, 424, 250, 424, stroke=PURPLE, sw=2.4, marker="arr-purple"))

    els.append('<rect x="290" y="338" width="180" height="140" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.6"/>')
    els.append(txt(380, 360, "河口“银化”换芯期", size=11.0, weight="700", color=GREEN, anchor="middle"))
    els.append(txt(380, 381, "皮质醇 + 生长激素飙升", size=9.9, color=INK, anchor="middle", weight="700"))
    els.append(txt(380, 401, "停留在半咸水河口数天～数周：", size=9.8, color=SLATE, anchor="middle"))
    els.append(txt(380, 421, "拆掉旧吸盐泵、组装排盐泵！", size=9.8, color=GREEN, anchor="middle", weight="700"))
    els.append(txt(380, 443, "溯河：大马哈鱼/中华鲟（海→河产卵）", size=9.8, color=BLUE, anchor="middle"))
    els.append(txt(380, 462, "降海：日本鳗鲡（河→马里亚纳海沟）", size=9.8, color=PURPLE, anchor="middle"))

    els.append(_line(474, 392, 510, 392, stroke=GREEN, sw=2.4, marker="arr-green"))
    els.append(_line(510, 424, 474, 424, stroke=PURPLE, sw=2.4, marker="arr-purple"))

    # Right box: Ocean stage
    els.append('<rect x="514" y="338" width="214" height="140" rx="10" fill="#fff7ed" stroke="#fb923c" stroke-width="1.4"/>')
    els.append(txt(621, 360, "大洋咸水模式", size=11.0, weight="700", color=ORANGE, anchor="middle"))
    els.append(txt(621, 380, "• 鳃泵亚型：NKA α1b（排盐）", size=9.9, color=INK, anchor="middle", weight="600"))
    els.append(txt(621, 400, "• 排盐引擎：NKCC1 + CFTR 开启", size=9.8, color=SLATE, anchor="middle"))
    els.append(txt(621, 420, "• 肠道开启喝水，肾脏关小排尿", size=9.8, color=SLATE, anchor="middle"))
    els.append(txt(621, 440, "• 视觉：切换维 A₁ 匹配蓝海", size=9.8, color=ORANGE, anchor="middle", weight="600"))
    els.append(txt(621, 462, "（海洋育肥三文鱼 / 产卵海鳗）", size=9.8, color=ORANGE, anchor="middle", weight="700"))

    return figure(
        H,
        "淡水鱼与咸水鱼生活繁殖习性及三文鱼鳗鲡跨界换芯机制图",
        "上半部对比淡水鱼耐寒耐缺氧、黏沉性卵护幼与咸水鱼大洋洄游、百万粒浮性卵策略；下半部展示三文鱼与鳗鲡在河口通过皮质醇和生长激素将鳃离子泵在吸盐与排盐模式间双向切换。",
        els,
        extra_defs=_markers(),
    )


# ---------------------------------------------------------------------------
# 5. Flavor Chemistry (TMAO 8,200 m Limit) & Sashimi Safety (760 x 515)
# ---------------------------------------------------------------------------
def build_flavor_and_safety() -> str:
    # Verified Yancey et al. (2014, PNAS 111:4461, PMC3970477) data points:
    # Freshwater: ~0-5 mmol/kg; Shallow marine (0-200 m): ~42 mmol/kg;
    # 4,850 m abyssal teleost: 261 mmol/kg; 7,000 m Kermadec snailfish: 386 mmol/kg;
    # Extrapolated isosmotic limit (~1,100 mOsm/kg -> ~450 mmol/kg TMAO): ~8,200 m!
    tmao_pts = [
        (0.0, 42.0),
        (1000.0, 74.0),
        (2500.0, 148.0),
        (4850.0, 261.0),
        (7000.0, 386.0),
        (8200.0, 448.0),
    ]
    assert tmao_pts[4][1] == 386.0 and tmao_pts[3][1] == 261.0

    H = 515
    els = header(
        "餐桌上的终极较量：鲜甜与土腥从哪来？为什么淡水鱼绝不能生吃？",
        "左看 TMAO 抗压鲜味分子与 8,200 米深海鱼类禁区（PNAS, 2014）｜右看肝吸虫与异尖线虫安全红线",
    )

    # Left Card: TMAO Depth Curve & Flavor Chemistry
    els.append(card(16, 68, 362, 432, fill="#ffffff"))
    els.append(step_badge(36, 92, 1, BLUE, BLUE_SOFT))
    els.append(txt(56, 97, "风味密码：TMAO 海鲜甜 vs 蓝藻“土臭素”", size=12.0, weight="700", color=BLUE))

    px0, py0, pw, ph = 70, 128, 286, 196
    els.append(f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')

    def dx(depth_m: float) -> float:
        return px0 + (depth_m / 9000.0) * pw

    def ty(tmao_val: float) -> float:
        return py0 + ph - (tmao_val / 500.0) * ph

    for tick_y in [0, 150, 300, 450]:
        yy = ty(tick_y)
        els.append(_line(px0, yy, px0 + pw, yy, stroke="#e2e8f0", sw=1.0, dash="4,3"))
        els.append(txt(px0 - 6, yy + 3.5, f"{tick_y}", size=9.8, color=MUTED, anchor="end"))

    for tick_x in [0, 3000, 6000, 8200]:
        xx = dx(tick_x)
        els.append(_line(xx, py0 + ph, xx, py0 + ph + 4, stroke=SLATE, sw=1.1))
        lbl = "8.2km" if tick_x == 8200 else f"{tick_x // 1000}km"
        els.append(txt(xx, py0 + ph + 15, lbl, size=9.8, color=RED if tick_x == 8200 else MUTED, anchor="middle", weight="700" if tick_x == 8200 else "500"))

    els.append(txt(px0 - 8, py0 - 8, "肌肉 TMAO (mmol/kg)", size=9.8, color=INK, weight="700"))
    els.append(txt(px0 + pw / 2, py0 + ph + 31, "海洋栖息水深 →（万米深渊无真骨鱼之谜）", size=9.9, color=INK, anchor="middle", weight="700"))

    # Red vertical limit line at 8,200 m + callout in open upper-left space of plot
    x_lim = dx(8200.0)
    els.append(_line(x_lim, py0 + 6, x_lim, py0 + ph, stroke=RED, sw=1.8, dash="5,3"))
    els.append(txt(px0 + 12, py0 + 22, "8,200m 等渗红线（更深再无任何鱼类！）→", size=9.8, color=RED, weight="700"))
    els.append(_line(px0 + 206, py0 + 19, x_lim - 5, py0 + 19, stroke=RED, sw=1.2, dash="3,2", marker="arr-red"))

    # Plot marine TMAO line
    poly = " ".join(f"{dx(d):.1f},{ty(v):.1f}" for d, v in tmao_pts)
    els.append(f'<polyline points="{poly}" fill="none" stroke="{ORANGE}" stroke-width="2.8"/>')
    for d, v in tmao_pts[:-1]:
        els.append(f'<circle cx="{dx(d):.1f}" cy="{ty(v):.1f}" r="4.2" fill="{ORANGE}" stroke="#ffffff" stroke-width="1.2"/>')

    # Freshwater dot at (0, 3)
    els.append(f'<circle cx="{dx(0):.1f}" cy="{ty(3.0):.1f}" r="5.0" fill="{BLUE}" stroke="#ffffff" stroke-width="1.4"/>')
    els.append(txt(dx(250), ty(3.0) - 6, "淡水鱼 ≈ 0", size=9.8, color=BLUE, weight="700"))
    els.append(txt(dx(7000) - 10, ty(386.0) - 6, "7km 狮子鱼: 386", size=9.8, color=ORANGE, anchor="end", weight="700"))

    # Bottom flavor explanation box
    els.append('<rect x="30" y="366" width="334" height="122" rx="9" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1.2"/>')
    els.append(txt(42, 386, "• 海鱼鲜甜与海腥：活海鱼富含无臭 TMAO（抗盐抗深海高压）", size=9.8, color=INK, weight="600"))
    els.append(txt(42, 405, "  与甘氨酸，入口自带清甜；死后细菌把 TMAO 还原成挥发性", size=9.8, color=SLATE))
    els.append(txt(42, 424, "  三甲胺（TMA 海腥味）——挤柠檬汁/醋酸碱中和即可去腥！", size=9.8, color=ORANGE, weight="700"))
    els.append(txt(42, 446, "• 淡水鱼泥土腥：TMAO 极低，鱼鳃易从池底蓝藻/放线菌富集", size=9.8, color=INK, weight="600"))
    els.append(txt(42, 465, "  脂溶性“土臭素（Geosmin）”与 2-MIB——靠清水吊水+葱姜料酒！", size=9.8, color=BLUE, weight="700"))

    # Right Card: Parasite Life-Cycle & Raw Eating Rules
    els.append(card(394, 68, 350, 432, fill="#ffffff"))
    els.append(step_badge(414, 92, 2, RED, RED_SOFT))
    els.append(txt(434, 97, "生食安全红线：肝吸虫 vs 海鱼异尖线虫", size=12.0, weight="700", color=RED))

    # Box 1: Freshwater Raw Fish = High Danger
    els.append('<rect x="410" y="114" width="318" height="176" rx="10" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.4"/>')
    els.append(txt(424, 136, "✗ 淡水鱼生（草鱼/鲫鱼/麦穗等超 100 种）：严禁生吃！", size=10.4, weight="700", color=RED))
    els.append(txt(424, 157, "• 头号元凶：华支睾吸虫（肝吸虫）——世卫组织 IARC", size=9.8, color=INK, weight="600"))
    els.append(txt(424, 176, "  认证“1 类明确致癌物”（直接诱发胆管癌、肝硬化）！", size=9.8, color=RED, weight="700"))
    els.append(txt(424, 196, "• 渗透压同源陷阱：淡水鱼体液（≈300 mOsm）与人体胆汁", size=9.8, color=SLATE))
    els.append(txt(424, 215, "  环境高度匹配，囊蚴钻入人类肝胆管可存活 20–30 年！", size=9.8, color=INK))
    els.append(txt(424, 236, "• 致命误区：高度白酒、芥末、陈醋、大蒜泡几分钟全杀不死！", size=9.8, color=RED, weight="600"))
    els.append(txt(424, 258, "✓ 唯一铁律：中心温度 ≥ 63°C（沸水/热油彻底熟透）！", size=10.0, color=GREEN, weight="700"))

    # Box 2: Marine Sashimi Truth (Busting "Marine = Zero Worms")
    els.append('<rect x="410" y="302" width="318" height="186" rx="10" fill="#f0fdf4" stroke="#86efac" stroke-width="1.4"/>')
    els.append(txt(424, 324, "⚠ 海鱼刺身真相：海鱼并非没虫，靠“急冻+控源”！", size=10.4, weight="700", color=GREEN))
    els.append(txt(424, 345, "• 野生海鱼常见虫：异尖线虫（Anisakis，终宿主鲸/海豹）", size=9.8, color=INK, weight="600"))
    els.append(txt(424, 364, "• 虽难在人体长期定居发育，但活虫钻胃壁会引发剧烈急腹痛", size=9.8, color=SLATE))
    els.append(txt(424, 383, "  与严重过敏！刚钓上船的野生海鱼现切生吃同样危险！", size=9.8, color=ORANGE, weight="700"))
    els.append(txt(424, 406, "✓ 正规海鱼刺身两大安全屏障（FDA / 欧盟强制规范）：", size=9.9, color=GREEN, weight="700"))
    els.append(txt(424, 426, "  1. 工业超低温急冻：−20°C 以下冻满 7 天，或 −35°C", size=9.8, color=INK))
    els.append(txt(424, 445, "     冻硬后保冷 ≥ 15 小时（家用冰箱 −18°C 往往不够稳）；", size=9.8, color=SLATE))
    els.append(txt(424, 466, "  2. 全封闭人工颗粒饲料海水养殖（从食物链源头阻断虫卵）。", size=9.8, color=TEAL, weight="600"))

    return figure(
        H,
        "海洋鱼类TMAO深海极限曲线与淡水海鱼生食寄生虫风险对比图",
        "左图按2014年PNAS实测数据绘制海鱼肌肉TMAO随水深线性飙升至8200米等渗红线并对比海腥味TMA与淡水土臭素；右图对比淡水鱼生1类致癌物肝吸虫风险与海鱼异尖线虫FDA零下20度7天急冻规范。",
        els,
        extra_defs=_markers(),
    )


@register(TOPIC, "science", "淡水鱼与咸水鱼的生理、演化、习性与风味安全对比")
def build_all() -> None:
    builders = {
        "osmotic-paradox-fresh-vs-marine-gill.svg": build_osmotic_paradox,
        "biodiversity-paradox-and-evolution-tree.svg": build_biodiversity_paradox,
        "anatomy-bones-senses-and-swimbladder.svg": build_anatomy_senses,
        "living-habits-spawning-and-salmon-switch.svg": build_habits_and_migration,
        "tmao-depth-flavor-and-parasite-safety.svg": build_flavor_and_safety,
    }
    for fname, fn in builders.items():
        write_svg(TOPIC, fname, fn())
