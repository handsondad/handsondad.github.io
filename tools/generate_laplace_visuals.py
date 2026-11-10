"""Original Laplace diagrams; synthetic Newtonian model, not an ephemeris."""

import math
from pathlib import Path

from generate_kepler_newton_visuals import BLUE, GOLD, INK, RED, dot, line, panel, path, save, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "laplace"
GM = 1.32712440041279419e20 * (365.25 * 86400) ** 2 / 149597870700 ** 3
MASS = (1, 126712764.1 / 1.32712440041279419e11, 37940584.8418 / 1.32712440041279419e11)
RADII = (5.202887, 9.53667594)
NJ = 3034.90371757 / 36000
NS = 1222.11494724 / 36000
BEAT = 1 / abs(2 * NJ - 5 * NS)


def write(name, height, title, description, body, css=""):
    save(name, height, title, description, body, css, output_directory=OUT)


def heading(number, title):
    return text(36, 49, f"{number} {title}", 29)


def rows(x, y, values, size=23, step=36, color=INK):
    return "".join(text(x, y + i * step, value, size, color) for i, value in enumerate(values))


def initial(factor):
    masses = [MASS[0], MASS[1] * factor, MASS[2] * factor]
    state = [[0., 0., 0., 0.]]
    for radius, angle, mass in zip(RADII, (0, math.pi / 3), masses[1:]):
        speed = math.sqrt(GM * (1 + mass) / radius)
        state.append([radius * math.cos(angle), radius * math.sin(angle),
                      -speed * math.sin(angle), speed * math.cos(angle)])
    for k in range(4):
        mean = sum(m * p[k] for m, p in zip(masses, state)) / sum(masses)
        for p in state:
            p[k] -= mean
    return masses, state


def accelerations(state, masses):
    a = [[0., 0.] for _ in state]
    for i in range(3):
        for j in range(i + 1, 3):
            dx, dy = state[j][0] - state[i][0], state[j][1] - state[i][1]
            r = math.hypot(dx, dy)
            assert r > .1, "Teaching model encountered a close approach"
            for k, delta in enumerate((dx, dy)):
                a[i][k] += GM * masses[j] * delta / r ** 3
                a[j][k] -= GM * masses[i] * delta / r ** 3
    return a


def energy(state, masses):
    value = sum(m * (p[2] ** 2 + p[3] ** 2) / 2 for m, p in zip(masses, state))
    for i in range(3):
        for j in range(i + 1, 3):
            value -= GM * masses[i] * masses[j] / math.dist(state[i][:2], state[j][:2])
    return value


def simulate(factor=1, dt=.0025):
    masses, state = initial(factor)
    e0 = energy(state, masses)
    a = accelerations(state, masses)
    frames, max_error = [], 0
    count = round(120 / dt)
    stride = round(.5 / dt)
    for step in range(count + 1):
        if step % stride == 0:
            t = step * dt
            dx, dy = state[1][0] - state[0][0], state[1][1] - state[0][1]
            phase = math.atan2(dy, dx) - math.sqrt(GM * (1 + masses[1]) / RADII[0] ** 3) * t
            residual = math.atan2(math.sin(phase), math.cos(phase)) * 180 / math.pi
            frames.append((t, dx, dy, residual))
            max_error = max(max_error, abs((energy(state, masses) - e0) / e0))
        if step == count:
            break
        for p, force in zip(state, a):
            for k in range(2):
                p[k] += p[k + 2] * dt + force[k] * dt ** 2 / 2
                p[k + 2] += force[k] * dt / 2
        a = accelerations(state, masses)
        for p, force in zip(state, a):
            for k in range(2):
                p[k + 2] += force[k] * dt / 2
    assert max_error < 2e-6
    for k in range(4):
        assert abs(sum(m * p[k] for m, p in zip(masses, state))) < 1e-10
    return frames, max_error


def history():
    body = heading("①", "一条引力定律，为什么需要几代人？")
    entries = [
        ("1687", "牛顿", "给出运动定律与万有引力。"),
        ("18 世纪", "欧拉、拉格朗日等", "发展分析方法与摄动计算。"),
        ("1780 年代", "拉普拉斯", "解释木星、土星的长周期偏差。"),
        ("1799 起", "《天体力学》", "前两卷出版，全书共五卷。"),
        ("19 世纪末", "庞加莱", "揭示三体问题远比想象复杂。"),
        ("今天", "观测与数值积分", "精密星历与长期统计研究并行。"),
    ]
    for i, (year, name, detail) in enumerate(entries):
        y = 85 + i * 120
        body += panel(y, 103)
        body += text(48, y + 34, year, 24, BLUE)
        body += text(242, y + 34, name, 25)
        body += text(48, y + 77, detail, 23)
    body += text(36, 842, "年份是研究与出版路标，不是一人接替一人的完整名单。", 22)
    write("history.svg", 880, "从牛顿到现代星历的天体力学路标",
          "六个历史路标说明拉普拉斯连接牛顿引力、分析计算与可检验的天文预报；并未证明永远稳定。", body)


def differential():
    body = heading("②", "土星拉木星，也拉着太阳")
    body += rows(36, 91, ["只看日心位置时，要扣除太阳本身的加速度。", "下面采用同一直线上的构型，距离按比例画。"], 23)
    scale, ox, y = 53, 90, 300
    jx, sx = ox + scale * RADII[0], ox + scale * RADII[1]
    body += line(ox, y, sx, y, "#a2b4c2", True)
    body += dot(ox, y, 15, GOLD) + dot(jx, y, 11, BLUE) + dot(sx, y, 12, RED)
    body += text(ox, 348, "太阳", 24, INK, "middle")
    body += text(jx, 348, "木星 J", 24, INK, "middle")
    body += text(sx, 348, "土星 S", 24, INK, "middle")
    a_sun = GM * MASS[2] / RADII[1] ** 2
    a_jup = GM * MASS[2] / (RADII[1] - RADII[0]) ** 2
    ratio = a_jup / a_sun
    body += line(ox, 238, ox + 32, 238, RED, arrow=True)
    body += line(jx, 238, jx + 32 * ratio, 238, RED, arrow=True)
    body += text(36, 197, "土星引起的加速度：1 份", 22)
    body += text(345, 197, f"加速度：{ratio:.2f} 份", 22)
    body += panel(400, 257)
    body += rows(48, 443, ["① 木星确实被土星向右拉。", "② 太阳也被土星向右拉，但加速度较小。", "③ 木星相对太阳的额外加速度＝两者之差。"], 24, 48)
    body += text(48, 624, "图中红箭头表示加速度，长度按同一倍率绘制。", 22)
    body += text(36, 706, "不是所有“行星受到的力”，都能直接当日心方程的项。", 22)
    assert 4.8 < ratio < 4.9
    write("relative-pull.svg", 750, "日心摄动需要直接项和间接项",
          f"共线教学构型中，土星对木星的加速度约为对太阳的{ratio:.2f}倍；两者都向土星，日心额外加速度为差。", body)


def residuals(data):
    body = heading("③", "椭圆是起点，偏差才是线索")
    body += rows(36, 91, ["同一组人工初始位置与速度，积分 120 年。", "比较：三体木星方向 − 独立二体基线方向。"], 23)
    ox, oy, sx, sy = 100, 230, 4.5, 32
    body += line(ox, 565, 655, 565, INK, arrow=True)
    body += line(ox, 565, ox, 190, INK, arrow=True)
    for val in (-10, -8, -6, -4, -2, 0):
        yy = oy - val * sy
        body += line(ox, yy, 640, yy, "#d5dfe6", True)
        body += text(83, yy + 7, val, 21, INK, "end")
    for t in (0, 40, 80, 120):
        body += text(ox + t * sx, 605, t, 21, INK, "middle")
    body += text(116, 199, "方向偏差 / 度", 22)
    body += text(574, 636, "时间 / 年", 22)
    for factor, color in [(10, GOLD), (1, BLUE)]:
        body += path([(ox + t * sx, oy - v * sy) for t, _, _, v in data[factor]], color, 3, factor == 10)
    body += panel(662, 159)
    body += rows(48, 702, ["蓝实线：采用真实数量级的行星质量。", "金虚线：两颗行星质量都乘 10，方便比较。", "相同坐标轴；不是实测误差，也不是当前星历。"], 23, 43)
    write("perturbation-residual.svg", 855, "三体积分相对独立二体基线的方向偏差",
          "采用人工共面近圆初值；太阳也参与运动。横轴0至120年，纵轴木星方向偏差，真实质量与十倍行星质量用同一尺度比较。", body)


def resonance():
    tj, ts = 1 / NJ, 1 / NS
    body = heading("④", "快钟差一点，慢拍慢很多")
    body += rows(36, 91, ["冻结频率的教学模型，不是逐年精密星历。", f"木星 5 圈：{5*tj:.2f} 年；土星 2 圈：{2*ts:.2f} 年。"], 23)
    for y, count, duration, color, label in [(210, 5, tj, BLUE, "木星"), (310, 2, ts, RED, "土星")]:
        body += text(36, y + 7, label, 23)
        for i in range(count):
            xx = 118 + i * duration * 8
            body += f'<rect x="{xx:.3f}" y="{y-20}" width="{duration*8:.3f}" height="40" fill="{color}" opacity=".13" stroke="{color}" stroke-width="2"/>'
            body += text(xx + duration * 4, y + 8, i + 1, 21, color, "middle")
    body += text(36, 389, "少量的节拍差，累积成约 883 年的慢相位一圈。", 23)
    ox, oy, width, amp = 90, 585, 550, 108
    body += line(ox, oy, 655, oy, INK, arrow=True)
    body += line(ox, oy + 130, ox, oy - 145, INK, arrow=True)
    body += path([(ox + width * i / 320, oy - amp * math.cos(4 * math.pi * i / 320)) for i in range(321)])
    for i in range(3):
        body += text(ox + width * i / 2, 757, f"{i*BEAT:.0f}", 22, INK, "middle")
    body += text(36, 438, "只画 cos(2λJ − 5λS)，振幅人为定为 1。", 23)
    body += text(37, oy - amp + 8, "+1", 22)
    body += text(37, oy + amp + 8, "−1", 22)
    body += text(529, 797, "时间 / 年", 22)
    keyframes = []
    for i in range(161):
        f = i / 160
        keyframes.append(f"{f*100:.5f}%{{transform:translate({width*f:.4f}px,{-amp*math.cos(4*math.pi*f):.4f}px)}}")
    body += f'<g transform="translate({ox},{oy})"><circle class="beat-dot" r="8" fill="{RED}"/></g>'
    body += rows(36, 850, ["红点用 8 秒走完两次慢拍，结束后保留完整曲线。", "这不是木星位置曲线，也没有算出真实摄动振幅。"], 22)
    css = f".beat-dot{{transform:translate({width}px,{-amp}px);animation:slow-beat 8s linear 1}}"
    css += "@keyframes slow-beat{" + "".join(keyframes) + "}"
    css += "@media(prefers-reduced-motion:reduce){.beat-dot{animation:none}}"
    assert 880 < BEAT < 890
    write("near-resonance.svg", 943, "木星土星近五比二关系与慢相位",
          "两种公转频率接近整数比，二倍木星平均角与五倍土星平均角之差变化缓慢。蓝线是单位振幅余弦示意，不是历史大不等式的完整解。", body, css)


def potential():
    body = heading("⑤", "引力势不为零，拉普拉斯和却可以为零")
    body += rows(36, 91, ["球对称天体外部：把距离和势都无量纲化。", "本图令 GM = 1，横轴 r 从 1 到 4，不画内部。"], 23)
    ox, oy = 90, 245
    body += line(ox, oy, 650, oy, INK, arrow=True)
    body += line(ox, 513, ox, 190, INK, arrow=True)
    body += path([(ox + (r - 1) * 170, oy + 230 / r) for r in [1 + i * 3 / 240 for i in range(241)]], BLUE)
    for r in (1, 2, 3, 4):
        body += text(ox + (r - 1) * 170, 224, r, 22, INK, "middle")
    body += text(632, 224, "r", 22)
    body += text(124, 524, "Φ = −1/r；引力指向势下降的方向。", 24, BLUE)
    body += text(46, 482, "−1", 22) + text(35, 310, "−0.25", 19)
    body += panel(568, 260)
    body += rows(48, 611, ["看 P = (1, 0, 0)，不在中心质量上：", "三个方向的势曲率分别是 −2、+1、+1。", "加起来为 0；但势 Φ = −1，引力大小为 1。", "“没有当地质量”不等于“没有远方的引力”。"], 24, 53)
    body += text(36, 874, "完整三维函数：Φ(x,y,z) = −1 / √(x²+y²+z²)。", 23)
    def phi(x, y, z):
        return -1 / math.sqrt(x*x+y*y+z*z)
    h = .0001
    second = [(phi(1+h, 0, 0)-2*phi(1, 0, 0)+phi(1-h, 0, 0))/h**2,
              (phi(1, h, 0)-2*phi(1, 0, 0)+phi(1, -h, 0))/h**2]
    assert abs(second[0] + 2) < 1e-6 and abs(second[1] - 1) < 1e-6
    write("potential.svg", 920, "引力势和真空中的拉普拉斯方程",
          "曲线为天体外部负一除以r的势。无量纲点P处三个坐标二阶偏导为负二、正一、正一，和为零但势与引力均不为零。", body)


def predictions():
    body = heading("⑥", "预报不是只把方程往后算")
    for i, (title, detail) in enumerate([
        ("① 观测", "测角、测距、航天器无线电数据。"),
        ("② 建模", "质量、引力、相对论修正等。"),
        ("③ 积分与拟合", "调整初值和参数，让模型贴近观测。"),
        ("④ 检查残差", "区分测量噪声、数值误差、遗漏的物理。"),
        ("⑤ 预报并再检验", "给出适用时段，继续接受新观测挑战。"),
    ]):
        y = 85 + i * 114
        body += panel(y, 99) + text(48, y + 35, title, 26, BLUE)
        body += text(48, y + 77, detail, 23)
    body += rows(36, 704, ["能预报一段时间 ≠ 证明永远稳定。", "存在长期混沌 ≠ 明天就会发生行星碰撞。", "规律确定 ≠ 有限精度的初值能预知无限未来。"], 24, 51)
    write("prediction-and-limits.svg", 885, "从观测到预报的天体力学工作链",
          "五步连接观测、物理模型、积分拟合、残差和新预报，并区别短期精度、长期稳定性与混沌。", body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = {}
    for factor in (1, 10):
        frames, error = simulate(factor)
        finer, _ = simulate(factor, .00125)
        finer2, _ = simulate(factor, .000625)
        coarse_error = math.dist(frames[-1][1:3], finer[-1][1:3])
        fine_error = math.dist(finer[-1][1:3], finer2[-1][1:3])
        assert 3.8 < coarse_error / fine_error < 4.2
        assert coarse_error < .0002
        data[factor] = frames
        print(f"mass x{factor}: final residual {frames[-1][3]:.9f} deg; energy error {error:.3g}; convergence {coarse_error/fine_error:.3f}")
    history()
    differential()
    residuals(data)
    resonance()
    potential()
    predictions()
    print(f"Slow-phase period: {BEAT:.9f} years; six SVGs generated.")


if __name__ == "__main__":
    main()
