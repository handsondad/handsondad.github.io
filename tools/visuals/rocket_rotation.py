"""Original 760px Chinese SVG diagrams for the Rocket Launch & Rotation post."""

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
    register,
    step_badge,
    txt,
    write_svg,
)

SUBDIR = "rocket-rotation"

R_EQ_M = 6_378_137.0
T_SID_S = 86_164.0905
V_EQ = 2.0 * math.pi * R_EQ_M / T_SID_S  # 465.10 m/s


def _v_lat(lat_deg: float) -> float:
    return V_EQ * math.cos(math.radians(lat_deg))


def _verify_rocket_rotation_math():
    """Verify Earth spin speeds, Tsiolkovsky mass ratios, launch azimuths, inertia flip, and Yo-Yo de-spin."""
    # 1. Equatorial linear rotation velocity & spaceport latitudes
    assert 465.0 < V_EQ < 465.2
    v_kourou = _v_lat(5.236)
    v_wenchang = _v_lat(19.614)
    v_cape = _v_lat(28.562)
    v_jiuquan = _v_lat(40.960)
    v_baikonur = _v_lat(45.965)
    v_palmachim = _v_lat(31.898)
    assert 463.0 < v_kourou < 463.3
    assert 438.0 < v_wenchang < 438.3
    assert 408.4 < v_cape < 408.8
    assert 351.0 < v_jiuquan < 351.4
    assert 323.2 < v_baikonur < 323.5
    assert 86.5 < (v_wenchang - v_jiuquan) < 87.2
    # Israel retrograde penalty vs prograde at 31.9°N: 2 * v_palmachim ≈ 790 m/s
    assert 789.5 < 2.0 * v_palmachim < 790.5

    # 2. Tsiolkovsky Rocket Equation advantage (ve = 3200 m/s, dv_base = 9300 m/s vs 9300 - 438 m/s)
    ve = 3200.0
    mr_no_spin = math.exp(9300.0 / ve)
    mr_wenchang = math.exp((9300.0 - v_wenchang) / ve)
    dry_gain_pct = (mr_no_spin / mr_wenchang - 1.0) * 100.0
    assert 18.2 < mr_no_spin < 18.4 and 15.9 < mr_wenchang < 16.0
    assert 14.5 < dry_gain_pct < 14.8

    # 3. Spherical launch azimuth formula sin(beta) = cos(i) / cos(phi)
    # ISS inclination 51.64° from Cape Canaveral 28.56° -> beta ≈ 44.99° (NE) or 135.01° (SE)
    sin_beta_iss = math.cos(math.radians(51.64)) / math.cos(math.radians(28.56))
    beta_iss = math.degrees(math.asin(sin_beta_iss))
    assert 44.9 < beta_iss < 45.1

    # 4. Explorer 1 flat-spin energy dissipation (L conserved, E = L^2 / (2 I))
    # Pencil cylinder L=2.05 m, R=0.076 m: I_spin = 0.5*m*R^2, I_trans = m*(L^2/12 + R^2/4)
    l_exp, r_exp = 2.05, 0.076
    ratio_i = (l_exp**2 / 12.0 + r_exp**2 / 4.0) / (0.5 * r_exp**2)
    assert 120.0 < ratio_i < 123.0  # E_rot drops by >120x when flipping to flat spin!

    # 5. Yo-Yo De-spin exact law: omega(theta)/omega0 = (K - theta^2)/(K + theta^2), K = I/(2 m R^2) + 1
    m_sc, r_sc, m_wt = 200.0, 0.5, 1.0
    i_sc = 0.5 * m_sc * r_sc**2  # 25 kg*m^2
    k_val = i_sc / (2.0 * m_wt * r_sc**2) + 1.0  # 51.0
    theta_stop = math.sqrt(k_val)
    cord_len = r_sc * theta_stop  # 3.5707 m
    omega0 = 2.0 * math.pi * (60.0 / 60.0)  # 60 rpm = 2*pi rad/s
    t_stop = theta_stop / omega0  # 1.1366 s
    assert abs(k_val - 51.0) < 1e-9
    assert 3.570 < cord_len < 3.572
    assert 1.136 < t_stop < 1.138


def _defs_arrows():
    return """
    <marker id="arr-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#1d6fa5"/>
    </marker>
    <marker id="arr-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#c25014"/>
    </marker>
    <marker id="arr-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#18794e"/>
    </marker>
    <marker id="arr-p" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">
      <path d="M0,1 L9,5 L0,9 z" fill="#6d28d9"/>
    </marker>
    """


def _box(x, y, w, h, fill=SLATE_SOFT, stroke=BORDER, rx=8):
    return card(x, y, w, h, rx=rx, fill=fill, stroke=stroke, sw=1)


def _build_earth_spin_slingshot():
    """Fig 1: Earth's rotation linear speed v(phi) = 465.1 * cos(phi) across famous spaceports + Tsiolkovsky payoff."""
    H = 532
    el = [
        *header(
            "第一重旋转：借地球自转的“免费弹弓”——为什么文昌比酒泉天生多赚 87 m/s？",
            "先看左栏全球五大发射场随纬度余弦衰减的初始东向线速度 → 再看右栏齐奥尔科夫斯基公式如何把小速度放大成大载荷",
        )
    ]

    # Left panel: Spaceport v(phi) = 465.1 cos(phi) comparison
    el.append(card(22, 68, 418, 446))
    el.append(step_badge(42, 92, 1, BLUE, BLUE_SOFT))
    el.append(txt(62, 97, "地球自西向东转：站在赤道不动已超 1.36 倍音速！", size=12.2, color=INK, weight="700"))
    el.append(txt(42, 117, "各纬度东向初始线速度 v(φ) = 465.1 × cos φ（单位：m/s）", size=10.5, color=MUTED))

    ports = [
        ("赤道理想极限 (0.0°)", 465.1, "1,674 km/h（理论满额弹弓）", PURPLE),
        ("法属圭亚那库鲁 (5.2°N)", 463.2, "欧空局王牌港，吃满 99.6% 红利", GREEN),
        ("中国海南文昌 (19.6°N)", 438.1, "长征五号母港，比酒泉多送 87 m/s！", ORANGE),
        ("美国卡纳维拉尔角 (28.5°N)", 408.6, "阿波罗与猎鹰主力港（87.9%）", BLUE),
        ("中国甘肃酒泉 (41.0°N)", 351.2, "内陆高纬载人港（75.5%）", BLUE),
        ("哈萨克拜科努尔 (46.0°N)", 323.3, "苏联早期高纬港（仅剩 69.5%）", SLATE),
    ]
    bx0, bmax = 194.0, 224.0
    for idx, (pname, vval, pnote, pcol) in enumerate(ports):
        yy = 148 + idx * 54
        el.append(txt(38, yy + 14, pname, size=10.8, color=INK, weight="700"))
        el.append(f'<rect x="{bx0}" y="{yy}" width="{bmax}" height="20" rx="6" fill="{SLATE_SOFT}" stroke="{BORDER}"/>')
        bw = (vval / 480.0) * bmax
        el.append(f'<rect x="{bx0}" y="{yy}" width="{bw:.1f}" height="20" rx="6" fill="{pcol}" opacity="0.88"/>')
        el.append(txt(bx0 + 8, yy + 14, f"{vval:.0f} m/s", size=10.5, color="#ffffff", weight="700"))
        el.append(txt(bx0, yy + 35, pnote, size=10.5, color=BODY))

    el.append(_box(38, 468, 386, 32, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(231, 489, "注：北极点 cos 90° = 0（原地自转线速度为 0，半点顺风车也蹭不到）", size=10.5, color=BLUE, anchor="middle", weight="700"))

    # Right panel: Why 438 m/s matters — Tsiolkovsky exponential leverage + GEO plane-change bonus!
    el.append(card(454, 68, 284, 446))
    el.append(step_badge(474, 92, 2, ORANGE, ORANGE_SOFT))
    el.append(txt(494, 97, "才省 400 多米/秒，凭啥省出几吨载荷？", size=11.8, color=INK, weight="700"))
    el.append(txt(474, 117, "火箭方程的“指数暴政”＋赤道变轨双杀红利", size=10.5, color=MUTED))

    el.append(_box(470, 136, 252, 166, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(596, 158, "第一重暴击：燃料也要烧燃料推着飞！", size=11.0, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(596, 182, "入轨总需求 Δv ≈ 9,300 m/s", size=11.2, color=INK, anchor="middle", weight="700"))
    el.append(txt(484, 206, "● 无自转借力：质量比 m₀/mf ≈ 18.3", size=10.5, color=BODY))
    el.append(txt(484, 226, "● 文昌顺风东射：质量比降至 ≈ 16.0", size=10.5, color=ORANGE, weight="700"))
    el.append(txt(484, 248, "→ 同样起飞总重，入轨干重提升约 +14.7%！", size=10.5, color=INK, weight="700"))
    el.append(txt(484, 269, "因为被省掉的是最底层要托举全箭的燃料，", size=10.5, color=MUTED))
    el.append(txt(484, 288, "每少带 1 吨末级燃料，起飞少装十几吨！", size=10.5, color=MUTED))

    el.append(_box(470, 316, 252, 182, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(596, 338, "第二重暴击：地球静止轨道（GEO）倾角税", size=11.0, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(484, 362, "静止通信卫星必须悬在 0° 赤道正上空。", size=10.5, color=BODY))
    el.append(txt(484, 383, "发射场纬度 φ 越高，入轨轨道面越歪，", size=10.5, color=BODY))
    el.append(txt(484, 404, "在远地点强行把轨道“掰平”需额外消耗：", size=10.5, color=BODY))
    el.append(txt(596, 428, "Δv_掰平 = 2 v sin(Δi / 2)", size=11.2, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(484, 452, "库鲁（5.2°）几乎不用掰弯；而西昌/卡角", size=10.5, color=INK))
    el.append(txt(484, 471, "转向文昌后，GTO 运力直接暴增 15%–25%！", size=10.6, color=GREEN, weight="700"))

    write_svg(
        SUBDIR,
        "earth-spin-slingshot-latitude-spaceports.svg",
        figure(
            H,
            "全球主流航天发射场地球自转线速度对比与齐奥尔科夫斯基载荷增益图",
            "左栏按纬度余弦公式对比赤道、库鲁、文昌、卡纳维拉尔角、酒泉与拜科努尔的东向自转线速度，右栏解析火箭方程指数放大效应与赤道静止轨道倾角变轨节省原理。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_azimuth_and_retrograde():
    """Fig 2: Prograde East vs Sun-Synchronous Polar vs Israel's Retrograde Westward Shavit launch."""
    H = 520
    el = [
        *header(
            "方向博弈：既然往东打最省油，为什么有些火箭偏偏往极地甚至往西“逆行”？",
            "先看左图球面发射方位角定律 → 再看右栏三种经典航向：顺风东射、98° 太阳同步极轨与以色列向西硬刚",
        )
    ]

    # Left panel: Globe schematic showing Eastward spin + 3 launch trajectories
    el.append(card(22, 68, 352, 434))
    el.append(step_badge(42, 92, 1, BLUE, BLUE_SOFT))
    el.append(txt(62, 97, "地球大转盘上的三条截然不同航线", size=12.2, color=INK, weight="700"))
    el.append(txt(42, 117, "球面三角铁律：sin β = cos i / cos φ（i 为轨道倾角）", size=10.5, color=MUTED))

    gx, gy, gr = 198, 266, 112
    el.append(f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="#eff6ff" stroke="{BLUE}" stroke-width="2"/>')
    # Equator & latitude grid lines
    el.append(f'<ellipse cx="{gx}" cy="{gy}" rx="{gr}" ry="30" fill="none" stroke="{BLUE_LINE}" stroke-width="1.5" stroke-dasharray="5,4"/>')
    el.append(f'<line x1="{gx}" y1="{gy-gr-14}" x2="{gx}" y2="{gy+gr+14}" stroke="{SLATE}" stroke-width="1.4" stroke-dasharray="4,4"/>')
    el.append(txt(gx, gy - gr - 20, "北极 N (90°)", size=10.5, color=SLATE, anchor="middle", weight="700"))
    el.append(txt(gx + gr - 6, gy + 16, "赤道 0°", size=10.5, color=BLUE, anchor="end", weight="700", halo=True))

    # Big Earth eastward spin arrow along equator
    el.append(f'<path d="M {gx-62},{gy+22} Q {gx},{gy+36} {gx+66},{gy+20}" fill="none" stroke="{BLUE}" stroke-width="2.6" marker-end="url(#arr-b)"/>')
    el.append(txt(gx, gy + 48, "地球自西向东转 (+v_地)", size=10.6, color=BLUE, anchor="middle", weight="700", halo=True))

    # Launch point P at mid-northern latitude (gx - 18, gy - 34)
    lx, ly = gx - 18, gy - 34
    el.append(f'<circle cx="{lx}" cy="{ly}" r="5.5" fill="{INK}"/>')

    # Path 1: Prograde East/NE (Green)
    el.append(f'<path d="M {lx},{ly} Q {lx+66},{ly-28} {gx+106},{gy-56}" fill="none" stroke="{GREEN}" stroke-width="3" marker-end="url(#arr-g)"/>')
    el.append(txt(gx + 68, gy - 72, "① 顺行东射", size=10.8, color=GREEN, weight="700", halo=True))

    # Path 2: Sun-synchronous slightly west of North (Purple, i ≈ 98°)
    el.append(f'<path d="M {lx},{ly} Q {lx-14},{ly-56} {gx-38},{gy-110}" fill="none" stroke="{PURPLE}" stroke-width="2.8" marker-end="url(#arr-p)"/>')
    el.append(txt(gx - 78, gy - 98, "② 太阳同步极轨", size=10.6, color=PURPLE, weight="700", halo=True))

    # Path 3: Retrograde Westward (Orange, i ≈ 143°)
    el.append(f'<path d="M {lx},{ly} Q {lx-58},{ly-14} {gx-112},{gy-18}" fill="none" stroke="{ORANGE}" stroke-width="2.8" marker-end="url(#arr-o)"/>')
    el.append(txt(gx - 88, gy - 2, "③ 逆行西射", size=10.8, color=ORANGE, weight="700", halo=True))

    el.append(_box(38, 408, 320, 80, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(198, 430, "几何硬约束（为什么拜科努尔打不了低倾角）：", size=10.8, color=INK, anchor="middle", weight="700"))
    el.append(txt(198, 451, "因为 |sin β| ≤ 1 ⇒ cos i ≤ cos φ ⇒ 轨道倾角 i ≥ 发射场纬度 φ！", size=10.5, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(198, 471, "所以国际空间站定在 51.6° 倾角，只为照顾高纬度的俄罗斯火箭。", size=10.5, color=BODY, anchor="middle"))

    # Right panel: 3 Scenario Breakdown Cards
    el.append(card(388, 68, 350, 434))
    el.append(step_badge(408, 92, 2, ORANGE, ORANGE_SOFT))
    el.append(txt(428, 97, "三种发射航向的得失总账", size=12.2, color=INK, weight="700"))

    cards_r = [
        (
            116, 112, GREEN_SOFT, "#86efac", GREEN,
            "① 顺行东射（倾角 0°–90°）：占全球发射 70% 以上",
            "顺着地球自转起飞（朝东或东北/东南），白捡 +300 至",
            "+465 m/s 线速度；天宫、国际空间站与通信卫星均用此法。",
        ),
        (
            242, 118, PURPLE_SOFT, "#d8b4fe", PURPLE,
            "② 太阳同步轨道（倾角 96°–98°）：遥感卫星最爱",
            "故意朝“正北/正南偏西一点”打，反消地球东向初速。",
            "妙处：借赤道隆起引力矩让轨道面每天东进 0.9856°，",
            "抵消公转，每天固定地方时（如 10:30）飞过同一城市！",
        ),
        (
            374, 114, ORANGE_SOFT, "#fdba74", ORANGE,
            "③ 极端反例：以色列“沙维特”向西逆射（倾角 143°）",
            "基地（31.9°N）东边全是邻国，残骸绝不能往东掉！",
            "被迫朝地中海向西硬打：先抹平 395 m/s 再反向加速，",
            "里外里多亏约 790 m/s，有效运力直接腰斩近一半！",
        ),
    ]
    for cy, ch, cfill, cstr, ccol, ct, l1, *rest in cards_r:
        el.append(_box(404, cy, 318, ch, fill=cfill, stroke=cstr))
        el.append(txt(416, cy + 22, ct, size=10.8, color=ccol, weight="700"))
        el.append(txt(416, cy + 44, l1, size=10.5, color=INK))
        for idx_l, ln in enumerate(rest):
            el.append(txt(416, cy + 64 + idx_l * 20, ln, size=10.5, color=BODY))

    write_svg(
        SUBDIR,
        "prograde-polar-retrograde-azimuth-law.svg",
        figure(
            H,
            "火箭顺行东射、太阳同步极轨与逆行西射方位角对比图",
            "左栏展示球面发射方位角定律与三条典型入轨航向，右栏对比顺风东射、利用赤道隆起进动的98度太阳同步轨道以及以色列为避开邻国向地中海逆风西射损失790米每秒速度的极端案例。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_roll_program_and_gravity_turn():
    """Fig 3: Roll Program (T+8..20s) + Zero-AoA Gravity Turn (with 1-shot flight attitude animation)."""
    H = 536
    extra_css = """
    @keyframes trajectoryDraw {
      0% { stroke-dashoffset: 460; }
      100% { stroke-dashoffset: 0; }
    }
    .anim-traj {
      stroke-dasharray: 460;
      stroke-dashoffset: 0;
      animation: trajectoryDraw 3.2s ease-out 1 both;
    }
    @media (prefers-reduced-motion: reduce) {
      .anim-traj {
        animation: none !important;
        stroke-dashoffset: 0 !important;
      }
    }
    """

    el = [
        *header(
            "第二重旋转：火箭刚离塔架几秒钟，为什么突然在半空“自己拧一下腰”？",
            "先看左栏滚转程序（Roll Program）如何对齐水泥发射台与目标轨道面 → 再看右栏零攻角重力转弯（含单次轨迹动画）",
        )
    ]

    # Left panel: Why Roll Program exists (Fixed concrete launchpad vs mission azimuth + Principal Axes)
    el.append(card(22, 68, 336, 450))
    el.append(step_badge(42, 92, 1, PURPLE, PURPLE_SOFT))
    el.append(txt(62, 97, "滚转程序：不动水泥塔架，半空拧身瞄准！", size=11.8, color=INK, weight="700"))
    el.append(txt(42, 117, "绕纵轴（Roll Axis）自转特定角度，对准目标方位角 β", size=10.5, color=MUTED))

    # Top schematic: Top-down compass showing fixed pad (90° E) rolling to 40.88° NE (Saturn V SA-513 Skylab 1!)
    cx, cy = 190, 214
    el.append(f'<circle cx="{cx}" cy="{cy}" r="66" fill="{SLATE_SOFT}" stroke="{BORDER}" stroke-width="1.5"/>')
    el.append(f'<line x1="{cx}" y1="{cy-72}" x2="{cx}" y2="{cy+72}" stroke="#cbd5e1" stroke-width="1"/>')
    el.append(f'<line x1="{cx-72}" y1="{cy}" x2="{cx+72}" y2="{cy}" stroke="#cbd5e1" stroke-width="1"/>')
    el.append(txt(cx, cy - 76, "北 0°", size=10.5, color=MUTED, anchor="middle"))
    el.append(txt(cx + 80, cy + 4, "东 90°", size=10.5, color=MUTED))

    # Initial pad orientation vector (pointing 90° East)
    el.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+56}" y2="{cy}" stroke="{SLATE}" stroke-width="2.6" stroke-dasharray="5,3"/>')
    # Rolled flight azimuth vector (40.88° East of North -> dx = 58*sin(40.88)=38, dy = -58*cos(40.88)=-44)
    el.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+38}" y2="{cy-44}" stroke="{PURPLE}" stroke-width="3" marker-end="url(#arr-p)"/>')
    # Curved roll arc from East (0 rad) to -49.1°
    el.append(f'<path d="M {cx+38},{cy} A 38,38 0 0,0 {cx+25},{cy-29}" fill="none" stroke="{ORANGE}" stroke-width="2.2" marker-end="url(#arr-o)"/>')
    el.append(txt(cx + 46, cy - 16, "拧转 49.1°", size=10.5, color=ORANGE, weight="700", halo=True))
    el.append(txt(cx, cy + 88, "真实案例：土星五号 SA-513（天空实验室1号，NASA 1973）", size=10.5, color=INK, anchor="middle", weight="700"))
    el.append(txt(cx, cy + 106, "塔架固定朝正东 90°，离塔后滚转 49.12° 对准 40.88° 航向！", size=10.5, color=MUTED, anchor="middle"))

    el.append(_box(38, 336, 304, 166, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(52, 358, "为什么不在地上就把火箭转好再摆上去？三大工程原因：", size=10.6, color=PURPLE, weight="700"))
    el.append(txt(52, 380, "① 脐带塔、导流槽与加注摆臂是万吨钢筋水泥浇死的，", size=10.5, color=INK))
    el.append(txt(64, 399, "而每次任务的倾角甚至发射窗口每分钟方位角都在变；", size=10.5, color=BODY))
    el.append(txt(52, 421, "② 先对准俯仰平面，随后只需单轴低头（Pitch）就能入轨；", size=10.5, color=INK))
    el.append(txt(52, 443, "③ 航天飞机等有翼/载人器滚转成“头朝下倒飞”，既减轻机翼", size=10.5, color=INK))
    el.append(txt(64, 462, "气动载荷，又让机腹天线无遮挡对准地面测控站，还能看清地平线！", size=10.5, color=BODY))

    # Right panel: Gravity Turn sequence (Liftoff -> Roll Program -> Pitch-over -> Max-Q zero-AoA -> Horizontal 7.8 km/s)
    el.append(card(372, 68, 366, 450))
    el.append(step_badge(392, 92, 2, BLUE, BLUE_SOFT))
    el.append(txt(412, 97, "拧完腰立刻“低头弯腰”：零攻角重力转弯", size=12.0, color=INK, weight="700"))
    el.append(txt(392, 117, "入轨 80% 以上能量花在“水平加速到 7.8 km/s”，而非单纯爬高！", size=10.5, color=MUTED))

    # Trajectory plot box [396..720] x [144..382]
    tx0, ty0 = 424.0, 378.0
    el.append(f'<line x1="{tx0-12}" y1="{ty0}" x2="718" y2="{ty0}" stroke="{SLATE}" stroke-width="2"/>')
    el.append(txt(570, ty0 + 18, "水平下航程距离（数百至上千公里）→", size=10.5, color=MUTED, anchor="middle"))
    # Atmosphere layer band
    el.append(f'<rect x="{tx0}" y="{ty0-92}" width="290" height="92" fill="#e0f2fe" opacity="0.55"/>')
    el.append(txt(712, ty0 - 12, "稠密低层大气带", size=10.5, color=BLUE, anchor="end"))

    # Smooth gravity turn curve from (436, 378) vertical -> curving smoothly to horizontal at (706, 168)
    traj_d = "M 436,378 L 436,336 C 438,266 492,196 706,168"
    el.append(f'<path d="{traj_d}" fill="none" stroke="{BLUE}" stroke-width="3.4" class="anim-traj" marker-end="url(#arr-b)"/>')

    # 4 Milestone callout dots along the curve
    milestones = [
        (436, 344, "① T+10s 越塔滚转程序", ORANGE, 450, 350),
        (454, 292, "② 程序俯仰（轻点低头 2°–3°）", PURPLE, 470, 298),
        (498, 242, "③ Max-Q 最大动压（攻角 α≈0° 防折断！）", BLUE, 514, 248),
        (666, 171, "④ 近水平狂飙至 7.8 km/s 入轨", GREEN, 532, 156),
    ]
    for mx, my, mlbl, mcol, lx_t, ly_t in milestones:
        el.append(f'<circle cx="{mx}" cy="{my}" r="5" fill="{mcol}" stroke="#ffffff" stroke-width="1.5"/>')
        el.append(txt(lx_t, ly_t, mlbl, size=10.5, color=mcol, weight="700", halo=True))

    el.append(_box(390, 408, 330, 94, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(555, 430, "为什么绝不能“竖直飞到 400 km 再直角拐弯”？", size=10.8, color=BLUE, anchor="middle", weight="700"))
    el.append(txt(404, 451, "● 竖直硬顶重力悬停最费油（重力损耗 g·t 最大）；", size=10.5, color=INK))
    el.append(txt(404, 471, "● 薄壁箭体像易拉罐：竖着顶力极结实，但在超音速区若侧着", size=10.5, color=BODY))
    el.append(txt(416, 490, "大角度硬掰（攻角 α 过大），狂暴侧风会瞬间把火箭拦腰折断！", size=10.5, color=ORANGE, weight="700"))

    write_svg(
        SUBDIR,
        "roll-program-and-gravity-turn-sequence.svg",
        figure(
            H,
            "火箭起飞滚转程序方位对齐与零攻角重力转弯飞行时序图",
            "左栏图解土星五号从90度东向固定发射台滚转49.1度对准目标轨道方位角的原理，右栏展示越塔滚转、程序俯仰、最大动压零攻角穿越至7.8公里每秒水平入轨的重力转弯全过程。",
            el,
            extra_css=extra_css,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_spin_vs_3axis_tvc():
    """Fig 4: Spin Stabilization (averaging thrust offset + gyro stiffness) vs 3-Axis Gimbaled TVC (liquid slosh & Gemini 8)."""
    H = 528
    el = [
        *header(
            "第三重旋转：为什么探空火箭像步枪子弹一样狂转，而载人火箭却拼死“禁转”？",
            "左看自旋稳定如何靠“每分钟 60–750 转”抹平固体发动机偏心 → 右看液体晃动与阿姆斯特朗双子座 8 号惊魂时刻",
        )
    ]

    # Left card: Spin Stabilization
    el.append(card(22, 68, 352, 442))
    el.append(_box(38, 82, 320, 28, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(198, 101, "自旋稳定派（Spin Stabilization）：无控固推的省钱神技", size=11.4, color=GREEN, anchor="middle", weight="700"))

    # Schematic of spinning solid stage with slight canted fins / spin motors averaging nozzle error
    rx, ry = 198, 198
    el.append(f'<rect x="{rx-18}" y="{ry-58}" width="36" height="96" rx="8" fill="#dcfce7" stroke="{GREEN}" stroke-width="2"/>')
    el.append(f'<polygon points="{rx-18},{ry-58} {rx},{ry-86} {rx+18},{ry-58}" fill="{GREEN}"/>')
    # Canted fins
    el.append(f'<polygon points="{rx-18},{ry+14} {rx-38},{ry+38} {rx-18},{ry+36}" fill="{GREEN}" opacity="0.8"/>')
    el.append(f'<polygon points="{rx+18},{ry+14} {rx+38},{ry+38} {rx+18},{ry+36}" fill="{GREEN}" opacity="0.8"/>')
    # Spin loop around body
    el.append(f'<ellipse cx="{rx}" cy="{ry-10}" rx="48" ry="14" fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-dasharray="5,3"/>')
    el.append(txt(rx + 56, ry - 6, "ω = 60–750 rpm", size=10.6, color=ORANGE, weight="700"))
    # Slight crooked exhaust vector swept into symmetric cone!
    el.append(f'<polygon points="{rx},{ry+38} {rx-26},{ry+78} {rx+26},{ry+78}" fill="#ffedd5" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="3,3"/>')
    el.append(txt(rx, ry + 94, "喷管哪怕歪 0.3°，转一圈侧向力也刚好正负抵消！", size=10.5, color=ORANGE, anchor="middle", weight="700"))

    el.append(_box(38, 306, 320, 188, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(52, 328, "● 两大物理法宝：", size=10.8, color=INK, weight="700"))
    el.append(txt(62, 349, "1. 陀螺定轴性（L = I·ω 越大，外力矩越掰不动指向）；", size=10.5, color=BODY))
    el.append(txt(62, 369, "2. 推力偏心积分归零（省掉昂贵沉重的液压伺服电脑！）。", size=10.5, color=BODY))
    el.append(txt(52, 394, "● 真实服役明星：", size=10.8, color=GREEN, weight="700"))
    el.append(txt(62, 415, "• 气象/探空火箭（尾翼微斜几度，靠迎面气流自动吹转）；", size=10.5, color=BODY))
    el.append(txt(62, 435, "• 1958 探险者 1 号上面级旋转桶（电机预旋至 750 rpm）；", size=10.5, color=BODY))
    el.append(txt(62, 455, "• 新视野号冥王星探测器第三级 Star-48B（约 62 rpm）；", size=10.5, color=BODY))
    el.append(txt(62, 475, "• SpaceX 星链卫星堆叠体：末级慢速自旋后松开拉杆像飞盘撒开！", size=10.5, color=INK, weight="700"))

    # Right card: 3-Axis TVC Active Stabilization (Why liquid & crewed rockets FORBID continuous spin!)
    el.append(card(386, 68, 352, 442))
    el.append(_box(402, 82, 320, 28, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(562, 101, "三轴主动稳定派（3-Axis TVC）：液体大火箭与载人标配", size=11.4, color=BLUE, anchor="middle", weight="700"))

    # Schematic: Liquid tank centrifugal wall climbing + Gimbaled nozzle swiveling
    tx_c, ty_c = 502, 196
    el.append(f'<rect x="{tx_c-22}" y="{ty_c-58}" width="44" height="92" rx="8" fill="#eff6ff" stroke="{BLUE}" stroke-width="2"/>')
    # Liquid fuel flung to side walls leaving hollow air core over bottom drain!
    el.append(f'<path d="M {tx_c-20},{ty_c-28} L {tx_c-20},{ty_c+32} L {tx_c-7},{ty_c+32} Q {tx_c-10},{ty_c} {tx_c-20},{ty_c-28} Z" fill="#60a5fa"/>')
    el.append(f'<path d="M {tx_c+20},{ty_c-28} L {tx_c+20},{ty_c+32} L {tx_c+7},{ty_c+32} Q {tx_c+10},{ty_c} {tx_c+20},{ty_c-28} Z" fill="#60a5fa"/>')
    el.append(txt(tx_c, ty_c + 48, "若狂转：液氧离心贴壁", size=10.5, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(tx_c, ty_c + 65, "底部抽液口直接吸空断火！", size=10.5, color=ORANGE, anchor="middle"))

    # Right mini schematic inside right card: Gimbaled TVC nozzle
    gx_c, gy_c = 642, 196
    el.append(f'<rect x="{gx_c-16}" y="{gy_c-58}" width="32" height="84" rx="6" fill="{SLATE_SOFT}" stroke="{SLATE}" stroke-width="1.8"/>')
    el.append(f'<circle cx="{gx_c}" cy="{gy_c-16}" r="4" fill="{INK}"/>')
    el.append(txt(gx_c + 22, gy_c - 12, "CG 质心", size=10.5, color=INK))
    # Tilted gimbal nozzle
    el.append(f'<polygon points="{gx_c-5},{gy_c+26} {gx_c+5},{gy_c+26} {gx_c+16},{gy_c+48} {gx_c+2},{gy_c+52}" fill="{BLUE}"/>')
    el.append(f'<line x1="{gx_c+9}" y1="{gy_c+50}" x2="{gx_c+20}" y2="{gy_c+76}" stroke="{ORANGE}" stroke-width="2.6" marker-end="url(#arr-o)"/>')
    el.append(txt(gx_c, gy_c + 92, "万向节摆动喷管锁死三轴", size=10.5, color=BLUE, anchor="middle", weight="700"))

    el.append(_box(402, 306, 320, 188, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(416, 328, "● 为什么液体火箭与载人飞船严禁持续自旋？", size=10.8, color=BLUE, weight="700"))
    el.append(txt(426, 349, "1. 几百吨液氧煤油一旦旋转晃动，离心吸空＋谐振能撕裂箭体；", size=10.5, color=INK))
    el.append(txt(426, 369, "2. 人类前庭与脑供血承受不住高速滚转！", size=10.5, color=INK, weight="700"))
    el.append(txt(416, 395, "● 1966 年 3 月 16 日《双子座 8 号》生死 25 分钟（NASA 史实）：", size=10.6, color=ORANGE, weight="700"))
    el.append(txt(426, 416, "完成人类首次太空对接后，8 号姿态喷管短路卡死常开，", size=10.5, color=BODY))
    el.append(txt(426, 436, "飞船失控狂转飙至 1 圈/秒（60 rpm）！指令长尼尔·阿姆斯特朗", size=10.5, color=INK, weight="700"))
    el.append(txt(426, 456, "在眩晕黑视边缘果断关停主姿态系统、启用再入反推火箭才刹住，", size=10.5, color=BODY))
    el.append(txt(426, 476, "这次教科书级临危不乱直接让他被选为阿波罗 11 号登月第一人！", size=10.5, color=BLUE, weight="700"))

    write_svg(
        SUBDIR,
        "spin-stabilization-vs-3axis-tvc.svg",
        figure(
            H,
            "自旋稳定火箭与三轴推力矢量控制火箭原理对比及双子座8号失控案例图",
            "左栏展示自旋稳定通过陀螺刚度与推力偏心抵消稳定固体上面级和星链释放，右栏解析液体推进剂离心吸空风险、万向节摆动喷管原理及阿姆斯特朗双子座8号每秒1转紧急制动事件。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_explorer1_flat_spin():
    """Fig 5: Explorer 1 (1958) flat-spin catastrophe — why flexible whip antennas flipped a 750-rpm pencil 90 degrees!"""
    H = 516
    el = [
        *header(
            "改写教科书的太空翻车：1958 年美国首颗卫星“探险者 1 号”为什么自己横过来翻跟头？",
            "角动量 L 严格守恒，但柔性天线甩动摩擦偷走了动能 E = L²/(2I) → 铅笔形卫星被迫翻成转动惯量最大的“螺旋桨扁平自旋”！",
        )
    ]

    # Left card: Initial state — Pencil spinning around minimum-inertia long axis at 750 rpm
    el.append(card(22, 68, 344, 344))
    el.append(_box(38, 82, 312, 28, fill=BLUE_SOFT, stroke=BLUE_LINE))
    el.append(txt(194, 101, "入轨初态：绕细长轴（最小惯量 I_min）每分钟转 750 圈", size=11.0, color=BLUE, anchor="middle", weight="700"))

    # Horizontal pencil satellite pointing along flight path with 4 whip antennas flexing
    px, py = 194, 198
    el.append(f'<line x1="{px-130}" y1="{py}" x2="{px+136}" y2="{py}" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="5,4" marker-end="url(#arr-b)"/>')
    el.append(txt(px + 132, py - 10, "角动量 L 方向", size=10.5, color=BLUE, anchor="end", weight="700"))
    # Slender pencil body (2.05m x 0.15m)
    el.append(f'<rect x="{px-78}" y="{py-9}" width="144" height="18" rx="4" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    el.append(f'<polygon points="{px+66},{py-9} {px+92},{py} {px+66},{py+9}" fill="{BLUE}"/>')
    # 4 flexible whip antennas curving slightly (energy dissipation!)
    el.append(f'<path d="M {px+10},{py-9} Q {px+4},{py-44} {px-10},{py-62}" fill="none" stroke="{ORANGE}" stroke-width="2.2"/>')
    el.append(f'<path d="M {px+10},{py+9} Q {px+4},{py+44} {px-10},{py+62}" fill="none" stroke="{ORANGE}" stroke-width="2.2"/>')
    el.append(txt(px + 66, py - 46, "4 根柔性鞭状天线", size=10.5, color=ORANGE, weight="700"))
    el.append(txt(px + 66, py - 28, "微晃生热 ΔE < 0！", size=10.5, color=ORANGE, weight="700"))

    el.append(_box(38, 286, 312, 110, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(52, 309, "● 细铅笔几何账：长 2.05 m，直径仅 0.15 m", size=10.6, color=INK, weight="700"))
    el.append(txt(52, 331, "● 绕细长轴转动惯量极小（I_min），横向翻滚惯量大 120 倍！", size=10.5, color=BODY))
    el.append(txt(52, 353, "● 致命盲区：当年冯·布劳恩与 JPL 团队按“纯刚体欧拉方程”", size=10.5, color=BODY))
    el.append(txt(64, 372, "计算认为绕最小轴自旋稳定，忽略了弹性天线的内摩擦耗能！", size=10.5, color=ORANGE, weight="700"))

    # Right card: Final state (~90 min later!) — 90° flipped "Flat Spin" cartwheeling around I_max!
    el.append(card(380, 68, 358, 344))
    el.append(_box(396, 82, 326, 28, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(559, 101, "仅飞一圈后终态：翻转 90° 变成“电风扇扁平翻滚”（I_max）！", size=10.8, color=ORANGE, anchor="middle", weight="700"))

    fx, fy = 559, 198
    # L vector STILL points strictly right (conserved!)
    el.append(f'<line x1="{fx-132}" y1="{fy}" x2="{fx+142}" y2="{fy}" stroke="{BLUE}" stroke-width="2.2" stroke-dasharray="5,4" marker-end="url(#arr-b)"/>')
    el.append(txt(fx + 138, fy - 10, "L 方向纹丝不动！", size=10.5, color=BLUE, anchor="end", weight="700"))
    # Swept propeller circle
    el.append(f'<ellipse cx="{fx}" cy="{fy}" rx="28" ry="68" fill="#ffedd5" opacity="0.55" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="4,3"/>')
    # Pencil body now vertical (perpendicular to L!), tumbling end-over-end!
    el.append(f'<rect x="{fx-8}" y="{fy-58}" width="16" height="116" rx="4" fill="#fed7aa" stroke="{ORANGE}" stroke-width="2"/>')
    el.append(f'<polygon points="{fx-8},{fy-58} {fx},{fy-76} {fx+8},{fy-58}" fill="{ORANGE}"/>')
    el.append(txt(fx - 44, fy - 52, "像竹蜻蜓/电扇叶", size=10.5, color=ORANGE, anchor="end", weight="700"))
    el.append(txt(fx - 44, fy - 34, "横着翻跟头！", size=10.5, color=ORANGE, anchor="end", weight="700"))

    el.append(_box(396, 286, 326, 110, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(559, 310, "一行公式破案：E_转 = L² / (2·I)", size=11.6, color=ORANGE, anchor="middle", weight="700"))
    el.append(txt(410, 333, "太空中无外力矩 ⇒ 角动量 L 铁打不变；", size=10.5, color=INK, weight="700"))
    el.append(txt(410, 353, "天线甩动与液体晃动耗散动能 ⇒ E_转 不断减小；", size=10.5, color=BODY))
    el.append(txt(410, 373, "分子 L² 不变而 E_转 要变小 ⇒ 分母 I 必须涨到最大的 I_max！", size=10.5, color=ORANGE, weight="700"))

    # Bottom golden rule banner
    el.append(card(22, 424, 716, 78, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(380, 448, "航天器姿态动力学“最大轴铁律”（Major-Axis Rule）：", size=11.4, color=GREEN, anchor="middle", weight="700"))
    el.append(txt(380, 470, "存在任何内部能量耗散（天线颤振、燃料晃动）时，唯有绕“最大转动惯量轴（扁圆盘轴）”的自旋才是永久稳定的！", size=10.6, color=INK, anchor="middle", weight="700"))
    el.append(txt(380, 490, "这就是为什么后来的自旋稳定通信卫星全都造得像“矮胖大圆鼓”，而细长火箭若要自旋必须加装主动章动阻尼器。", size=10.5, color=BODY, anchor="middle"))

    write_svg(
        SUBDIR,
        "explorer1-flat-spin-inertia-trap.svg",
        figure(
            H,
            "1958年探险者1号柔性天线耗能引发扁平自旋失稳与最大转动惯量法则图",
            "左栏展示探险者1号细长箭体绕最小转动惯量轴750转每分自旋及鞭状天线耗能，右栏用E等于L平方除以2I证明角动量守恒下动能损耗必然迫使卫星翻转90度进入最大惯量轴扁平翻滚。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


def _build_yoyo_despin():
    """Fig 6: NASA Yo-Yo De-spin Mechanism — exact curve omega(theta)/omega0 = (K - theta^2)/(K + theta^2) stopping 60 rpm in 1.14 s!"""
    H = 528
    el = [
        *header(
            "第四重旋转：在没有空气的真空里，两颗 1 公斤小铁球如何 1 秒刹停 200 公斤飞船？",
            "NASA“溜溜球减旋机构（Yo-Yo De-spin）”：不烧一滴推进剂，靠钢索甩开暴涨转动惯量，把全身角动量一把抽干！",
        )
    ]

    # Left panel: 3-stage geometric unwinding diagram
    el.append(card(22, 68, 348, 442))
    el.append(step_badge(42, 92, 1, BLUE, BLUE_SOFT))
    el.append(txt(62, 97, "三步无燃料急刹动作分解（俯视图）", size=12.0, color=INK, weight="700"))
    el.append(txt(42, 117, "类似花样滑冰运动员突然把双臂伸长 7 倍并脱手甩出！", size=10.5, color=MUTED))

    # Stage A (top)
    el.append(_box(38, 134, 316, 108, fill=SLATE_SOFT, stroke=BORDER))
    el.append(txt(50, 154, "① 解锁前：钢索紧缠腰部，探测器 60 rpm 高速自旋", size=10.6, color=INK, weight="700"))
    el.append(f'<circle cx="114" cy="198" r="24" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    el.append(f'<circle cx="90" cy="198" r="4.5" fill="{ORANGE}"/>')
    el.append(f'<circle cx="138" cy="198" r="4.5" fill="{ORANGE}"/>')
    el.append(txt(160, 192, "飞船 M = 200 kg, R = 0.5 m", size=10.5, color=BODY))
    el.append(txt(160, 212, "配重锤 2 × 1 kg（仅占总重 1%！）", size=10.5, color=ORANGE, weight="700"))

    # Stage B (middle)
    el.append(_box(38, 254, 316, 116, fill=ORANGE_SOFT, stroke="#fdba74"))
    el.append(txt(50, 274, "② 甩开中：离心力拉出切向钢索，配重惯量 m·r² 暴涨", size=10.6, color=ORANGE, weight="700"))
    cx_b, cy_b = 114, 322
    el.append(f'<circle cx="{cx_b}" cy="{cy_b}" r="20" fill="#dbeafe" stroke="{BLUE}" stroke-width="2"/>')
    # Symmetric tangent cords unwinding!
    el.append(f'<line x1="{cx_b}" y1="{cy_b-20}" x2="{cx_b-56}" y2="{cy_b-20}" stroke="{ORANGE}" stroke-width="2"/>')
    el.append(f'<circle cx="{cx_b-56}" cy="{cy_b-20}" r="5" fill="{ORANGE}"/>')
    el.append(f'<line x1="{cx_b}" y1="{cy_b+20}" x2="{cx_b+56}" y2="{cy_b+20}" stroke="{ORANGE}" stroke-width="2"/>')
    el.append(f'<circle cx="{cx_b+56}" cy="{cy_b+20}" r="5" fill="{ORANGE}"/>')
    el.append(txt(184, 314, "钢索张力对舱体施加反向制动力矩，", size=10.5, color=INK))
    el.append(txt(184, 334, "角动量源源不断抽进两颗小铁球！", size=10.5, color=ORANGE, weight="700"))

    # Stage C (bottom)
    el.append(_box(38, 382, 316, 112, fill=GREEN_SOFT, stroke="#86efac"))
    el.append(txt(50, 402, "③ 精准脱钩：钢索走到底（3.57 m）自动滑脱飞走！", size=10.6, color=GREEN, weight="700"))
    cx_c, cy_c = 114, 450
    el.append(f'<circle cx="{cx_c}" cy="{cy_c}" r="20" fill="#dcfce7" stroke="{GREEN}" stroke-width="2.2"/>')
    el.append(txt(cx_c, cy_c + 4, "0 rpm", size=10.5, color=GREEN, anchor="middle", weight="700"))
    el.append(f'<circle cx="{cx_c-62}" cy="{cy_c-26}" r="4.5" fill="{ORANGE}"/>')
    el.append(f'<line x1="{cx_c-62}" y1="{cy_c-26}" x2="{cx_c-82}" y2="{cy_c-26}" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-o)"/>')
    el.append(f'<circle cx="{cx_c+62}" cy="{cy_c+26}" r="4.5" fill="{ORANGE}"/>')
    el.append(f'<line x1="{cx_c+62}" y1="{cy_c+26}" x2="{cx_c+82}" y2="{cy_c+26}" stroke="{ORANGE}" stroke-width="1.8" marker-end="url(#arr-o)"/>')
    el.append(txt(198, 444, "两颗铁球揣走 100% 角动量远去，", size=10.5, color=INK))
    el.append(txt(198, 464, "200 kg 探测器仅 1.14 秒稳稳停住！", size=10.5, color=GREEN, weight="700"))

    # Right panel: Exact analytical curve omega(theta)/omega0 = (K - theta^2)/(K + theta^2) for K = 51!
    el.append(card(384, 68, 354, 442))
    el.append(step_badge(404, 92, 2, PURPLE, PURPLE_SOFT))
    el.append(txt(424, 97, "精确解析解曲线：ω(θ)/ω₀ = (K − θ²)/(K + θ²)", size=11.6, color=INK, weight="700"))
    el.append(txt(404, 117, "算例参数 K = I/(2mR²) + 1 = 51，零转速点 θ* = √51 ≈ 7.14 弧度", size=10.5, color=MUTED))

    # Plot x: cord length l = R*theta from 0 to 4.2 m (notice overshoot to negative spin if not released at 3.57 m!)
    px0, px1 = 442.0, 718.0
    py_top, py_bot = 152.0, 386.0  # y from +1.05 down to -0.25!
    k_val = 51.0
    r_sc = 0.5

    def map_x(cord_m):
        return px0 + (cord_m / 4.2) * (px1 - px0)

    def map_y(ratio):
        # ratio in [-0.25, +1.05]
        return py_bot - ((ratio - (-0.25)) / 1.30) * (py_bot - py_top)

    y_zero = map_y(0.0)
    for r_tick, lbl_y in [(1.0, "+100% (60 rpm)"), (0.5, "+50% (30 rpm)"), (0.0, "0 rpm 刹停线"), (-0.2, "-20% 反转！")]:
        yy = map_y(r_tick)
        col_g = GREEN if r_tick == 0.0 else "#e2e8f0"
        sw_g = "1.8" if r_tick == 0.0 else "1"
        dash = ' stroke-dasharray="5,3"' if r_tick == 0.0 else ""
        el.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="{col_g}" stroke-width="{sw_g}"{dash}/>')
        el.append(txt(px0 - 6, yy + 4, lbl_y.split()[0], size=10.5, color=GREEN if r_tick == 0.0 else MUTED, anchor="end", weight="700" if r_tick == 0.0 else None))

    for l_tick in [0.0, 1.0, 2.0, 3.0, 4.0]:
        xx = map_x(l_tick)
        el.append(f'<line x1="{xx:.1f}" y1="{py_top}" x2="{xx:.1f}" y2="{py_bot}" stroke="#f1f5f9" stroke-width="1"/>')
        el.append(txt(xx, py_bot + 18, f"{l_tick:.0f}m", size=10.5, color=MUTED, anchor="middle"))

    el.append(f'<line x1="{px0}" y1="{py_top}" x2="{px0}" y2="{py_bot}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(f'<line x1="{px0}" y1="{py_bot}" x2="{px1}" y2="{py_bot}" stroke="{SLATE}" stroke-width="1.5"/>')
    el.append(txt((px0 + px1) / 2, py_bot + 36, "放出的钢索长度 ℓ = R·θ（米）", size=10.5, color=BODY, anchor="middle"))

    # Exact curve up to l_stop = 3.571 m (solid purple) + overshoot if not unhooked (dashed orange)!
    l_stop = r_sc * math.sqrt(k_val)
    pts_main = []
    for i in range(41):
        lm = (i / 40.0) * l_stop
        th = lm / r_sc
        rw = (k_val - th**2) / (k_val + th**2)
        pts_main.append(f"{map_x(lm):.1f},{map_y(rw):.1f}")
    el.append(f'<polyline points="{" ".join(pts_main)}" fill="none" stroke="{PURPLE}" stroke-width="3"/>')

    pts_over = []
    for i in range(16):
        lm = l_stop + (i / 15.0) * (4.2 - l_stop)
        th = lm / r_sc
        rw = (k_val - th**2) / (k_val + th**2)
        pts_over.append(f"{map_x(lm):.1f},{map_y(rw):.1f}")
    el.append(f'<polyline points="{" ".join(pts_over)}" fill="none" stroke="{ORANGE}" stroke-width="2.4" stroke-dasharray="5,3"/>')

    x_st = map_x(l_stop)
    el.append(f'<circle cx="{x_st:.1f}" cy="{y_zero:.1f}" r="6" fill="{GREEN}" stroke="#ffffff" stroke-width="1.8"/>')
    el.append(txt(x_st - 8, y_zero - 12, "ℓ* = 3.57 m 脱钩点（耗时 1.14 s！）", size=10.5, color=GREEN, anchor="end", weight="700", halo=True))
    el.append(txt(px1 - 4, map_y(-0.18) + 16, "若不脱钩甚至能倒转！", size=10.5, color=ORANGE, anchor="end", weight="700", halo=True))

    el.append(_box(400, 434, 322, 62, fill=PURPLE_SOFT, stroke="#d8b4fe"))
    el.append(txt(561, 456, "代表作：火星探路者号、黎明号、新视野号第三级", size=10.6, color=PURPLE, anchor="middle", weight="700"))
    el.append(txt(561, 477, "与全球数千枚探空火箭——纯牛顿力学的极致浪漫！", size=10.5, color=INK, anchor="middle"))

    write_svg(
        SUBDIR,
        "yoyo-despin-angular-momentum-brake.svg",
        figure(
            H,
            "NASA溜溜球减旋机构角动量转移三步原理与转速衰减精确曲线图",
            "左栏分三步图解两颗1公斤配重锤沿切向甩出3.57米钢索抽干200公斤飞船60转每分自旋的过程，右栏绘制精确解析解曲线并标出1.14秒零转速脱钩点与过放反转区。",
            el,
            extra_defs=_defs_arrows(),
        ),
    )


@register(
    "rocket-rotation",
    "Rocket launch & rotation: Earth spin slingshot, launch azimuth & retrograde, roll program & gravity turn, spin vs 3-axis TVC, Explorer 1 flat-spin & Yo-Yo de-spin",
    "physics",
)
def build_rocket_rotation():
    _verify_rocket_rotation_math()
    _build_earth_spin_slingshot()
    _build_azimuth_and_retrograde()
    _build_roll_program_and_gravity_turn()
    _build_spin_vs_3axis_tvc()
    _build_explorer1_flat_spin()
    _build_yoyo_despin()
