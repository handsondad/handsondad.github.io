"""Original, computed teaching figures for heat and Fourier analysis."""
import math
from pathlib import Path
from generate_kepler_newton_visuals import BLUE, RED, GOLD, INK, dot, line, panel, path, save, text

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "fourier"
TAU = 2*math.pi
GRAY = "#7b8fa0"


def rows(x, y, values, size=23, step=38, color=INK):
    return "".join(text(x, y+i*step, value, size, color) for i,value in enumerate(values))


def heading(number, title):
    return text(36, 49, f"{number} {title}", 28)


def write(name, height, title, description, body):
    save(name,height,title,description,body,output_directory=OUT)


def graph(y, fn, scale=55, offset=0, color=BLUE, dash=False, count=1024):
    return path([(92+536*j/count, y-scale*(fn(j/count)-offset)) for j in range(count+1)], color, 3, dash)


def axes(y, label="位置 x：0 → 1 m"):
    return line(88,y,634,y,GRAY,True)+text(92,y+97,label,21)


def heat(x,t):
    return 50+20*math.exp(-.01*TAU**2*t)*math.cos(TAU*x)+10*math.exp(-.01*(3*TAU)**2*t)*math.cos(3*TAU*x)


def amplitude(samples):
    n=len(samples)
    return [abs(sum(v*complex(math.cos(-TAU*k*j/n),math.sin(-TAU*k*j/n)) for j,v in enumerate(samples)))/n*(1 if k in (0,n//2) else 2) for k in range(n//2+1)]


def history():
    body=heading("①","从研究热，到研究各种变化")
    for i,(year,title,detail) in enumerate([
        ("1768","出生于欧塞尔","后来经历教学、远征与行政工作。"),
        ("1795","在巴黎师范学校学习","听过拉格朗日、拉普拉斯与蒙日的课。"),
        ("1807","报告固体中的热传播研究","三角级数与推导的严密性引发争论。"),
        ("1811","扩充论文参加热传播竞赛","获奖肯定与对论证的保留意见并存。"),
        ("1822","《热的解析理论》出版","系统讨论热传播及三角级数方法。"),
    ]):
        y=86+i*125
        body+=panel(y,109)+text(48,y+35,year,25,BLUE)+text(220,y+35,title,24)+text(48,y+82,detail,23)
    body+=rows(36,768,["现代傅里叶分析经过许多人的后续完善。","不是“一个人一次写出了今天所有频谱算法”。"])
    write("history.svg",860,"傅里叶的学习经历与热理论发展路标","1795年学习、1807年报告、1811年参赛与1822年专著出版是不同阶段；现代傅里叶分析由后人持续发展。",body)


def heat_balance():
    body=heading("②","一小段升温，还是降温？看收支")
    body+=rows(36,96,["等间距、同材料、同截面；三处温度：80、60、20 ℃。","只看中间小段：左边流入，右边流出。"])
    body+=panel(179,284)
    for x,value in [(90,80),(290,60),(490,20)]:
        body+=f'<rect x="{x}" y="245" width="140" height="102" fill="#e1edf4" stroke="{INK}" stroke-width="2"/>'
        body+=text(x+70,307,f"{value} ℃",28,INK,"middle")
    body+=line(230,296,282,296,RED,arrow=True)+line(430,296,482,296,RED,arrow=True)
    body+=text(250,220,"流入",24,RED,"middle")+text(450,220,"流出",24,RED,"middle")
    body+=text(48,414,"左温差 20；右温差 40 → 流出更多，中间降温。",23)
    body+=panel(498,266)
    body+=rows(48,545,["① 温度向右下降，热流朝右。","② 傅里叶定律：热流密度 = −导热率 × 温度梯度。","③ 能量守恒：积累 = 流入 − 流出。","合起来：温度随时间的变化，由空间弯曲程度决定。"],23,52)
    body+=rows(36,817,["箭头只标方向，不按长度表示热流大小。","这是一维局部收支示意；热传导定律不是波分解公式。"],22)
    assert 80-2*60+20<0
    write("heat-balance.svg",919,"由傅里叶导热定律和能量守恒理解温度变化","等间距的80、60、20摄氏度三处，右侧温度差大于左侧，流出更多，中段降温。箭头仅示意方向。",body)


def modes():
    body=heading("③","复杂形状，先试着拆成简单波")
    body+=rows(36,95,["把周长 1 m 的细环展开；两端其实是同一点。","这里只选两种空间波，温度单位 ℃。"])
    for y,title,fn,offset,color in [
        (180,"① 一圈一次起伏：20 cos(2πx)",lambda x:20*math.cos(TAU*x),0,BLUE),
        (471,"② 一圈三次起伏：10 cos(6πx)",lambda x:10*math.cos(3*TAU*x),0,RED),
        (762,"③ 50 + ① + ②：初始温度",lambda x:heat(x,0),50,INK),
    ]:
        body+=panel(y,260)+text(48,y+40,title,24,color)
        body+=graph(y+147,fn,2.1,offset,color)+axes(y+147)
        body+=text(650,y+155,str(offset),22,GRAY)
    body+=rows(36,1075,["①②表示相对平均温度的有正有负的分量。","③才是实际温度；相加不表示热在做机械振动。"],23)
    write("mode-sum.svg",1170,"两种空间余弦温差加上平均温度得到初始温度形状","一阶20摄氏度与三阶10摄氏度的余弦温差相加，再加50摄氏度平均值，得到20到80摄氏度的环上温度。三图使用同一温度比例。",body)


def decay():
    body=heading("④","细碎起伏先淡去，平均温度留下")
    body+=rows(36,94,["同一个绝热细环：α = 0.01 m²/s，周长 1 m。","这是人为选定参数的模型，不是某种金属的实测。"],23)
    for i,t in enumerate([0,.5,2,10]):
        y=181+i*228
        a=20*math.exp(-.01*TAU**2*t); b=10*math.exp(-.01*(3*TAU)**2*t)
        body+=panel(y,207)+text(48,y+34,f"t = {t:g} s",24,BLUE)
        body+=text(255,y+34,f"振幅：一阶 {a:.3f}；三阶 {b:.3f} ℃",22)
        body+=graph(y+117,lambda x:heat(x,t),2,50)+line(89,y+117,637,y+117,GRAY,True)
        body+=text(645,y+125,"50",21,GRAY)
        body+=text(92,y+188,"x = 0",20)+text(628,y+188,"1 m（接回起点）",20,INK,"end")
    body+=rows(36,1140,["三阶的指数衰减率是一阶的 9 倍。","各图同一比例；均温保持 50 ℃，不是所有温度降到 0。"],23)
    for t in (0,.5,2,10):
        assert abs(sum(heat(j/2048,t) for j in range(2048))/2048-50)<1e-11
    write("heat-decay.svg",1230,"绝热环上温度随时间变平的四个精确快照","温度由一阶与三阶余弦精确解析解计算，时刻0、0.5、2、10秒；三阶衰减率九倍，平均温度保持50摄氏度。",body)


def orthogonality():
    f=lambda t:math.cos(TAU*8*t)+.5*math.cos(TAU*20*t)
    body=heading("⑤","怎样知道一条波，藏了多少？")
    body+=rows(36,94,["用整整 1 秒观察：g(t) = cos(2π·8t) + ½ cos(2π·20t)。","乘上参考波，再求平均；此处两种频率都走完整周期。"],22)
    for y,title,fn,result,color in [
        (180,"① 原信号：8 Hz 与 20 Hz 相加",f,"",BLUE),
        (463,"② 乘 8 Hz 的余弦",lambda t:f(t)*math.cos(TAU*8*t),"平均 0.500 → 振幅 1.000",RED),
        (746,"③ 乘 20 Hz 的余弦",lambda t:f(t)*math.cos(TAU*20*t),"平均 0.250 → 振幅 0.500",GOLD),
    ]:
        body+=panel(y,254)+text(48,y+37,title,24,color)
        body+=graph(y+125,fn,47,color=color)+line(89,y+125,636,y+125,GRAY,True)
        body+=text(92,y+221,result or "横轴：0 → 1 s；纵轴：信号值（无量纲）。",22)
    body+=rows(36,1060,["不同频率乘积的正负部分，在这段整周期里抵消。","相同余弦平方的平均为 ½，所以这里还要乘 2。"],23)
    for frequency,expected in [(8,.5),(20,.25)]:
        mean=sum(f(j/4096)*math.cos(TAU*frequency*j/4096) for j in range(4096))/4096
        assert math.isclose(mean,expected,abs_tol=1e-12)
    write("frequency-probe.svg",1158,"乘参考余弦并平均提取两个整周期频率的分量","同一信号与8赫兹参考相乘均值0.5，与20赫兹参考相乘均值0.25；还原余弦振幅分别为1与0.5。未知相位时还需要正弦参考。",body)


def continuous():
    body=heading("⑦","周期变长，频率格点怎样变密？")
    body+=rows(36,94,["用高斯 g(t)=exp(−πt²) 的周期化作例子。","时间、频率分别以 1 s、1 Hz 归一化后写数值。","格点 f=n/P；每项权重=exp(−πf²)/P。"],21,33)
    for i,p in enumerate([1,2,4]):
        y=180+i*264; baseline=y+211
        body+=panel(y,243)+text(48,y+37,f"周期 P = {p} s；频率间距 Δf = {1/p:g} Hz",24,BLUE)
        body+=line(92,baseline,628,baseline,GRAY)
        for n in range(-2*p,2*p+1):
            f=n/p; value=math.exp(-math.pi*f*f)/p; x=360+120*f
            body+=line(x,baseline,x,baseline-155*value,BLUE)+dot(x,baseline-155*value,3,BLUE)
        body+=text(105,baseline+25,"−2",19)+text(355,baseline+25,"0",19)+text(600,baseline+25,"2 Hz",19)
    y=989
    body+=panel(y,266)+text(48,y+38,"连续频率用积分，不再只在离散格点相加。",23)
    body+=path([(120+480*j/800,y+217-155*math.exp(-math.pi*(-2+4*j/800)**2)) for j in range(801)])
    body+=line(115,y+217,610,y+217,GRAY)
    body+=text(110,y+244,"−2",19)+text(355,y+244,"0",19)+text(575,y+244,"2 Hz",19)
    body+=rows(36,1309,["上三图纵轴是单项权重；下图纵轴是频谱密度。","权重里含 Δf；不能把不同纵轴当成同一根柱子的高度。"],22)
    for frequency in (0,.25,.5,1,2):
        steps=8192
        h=16/steps
        integral=sum((1 if j in (0,steps) else 4 if j%2 else 2)*
                     math.exp(-math.pi*(-8+j*h)**2)*math.cos(TAU*frequency*(-8+j*h))
                     for j in range(steps+1))*h/3
        assert math.isclose(integral,math.exp(-math.pi*frequency**2),abs_tol=1e-12)
    write("series-to-transform.svg",1405,"由周期化高斯的离散频率权重理解连续傅里叶积分","周期1、2、4秒的频率间距为1、0.5、0.25赫兹，系数为高斯频谱密度乘频率间距；下方曲线显示频谱密度，不把离散权重与连续密度混为一谈。",body)


def phase():
    body=heading("⑥","频率和强弱相同，波形仍会不同")
    body+=rows(36,95,["同样的 8 Hz、20 Hz；只改第二项的相位。","记录 1 s，采样率 128 Hz，共 128 点。"],23)
    for y,phi,label,color in [(180,0,"① 第二项相位 0°",BLUE),(461,math.pi/2,"② 第二项相位 90°",RED)]:
        body+=panel(y,253)+text(48,y+37,label,25,color)
        body+=graph(y+136,lambda t:math.cos(TAU*8*t)+.5*math.cos(TAU*20*t+phi),48,color=color)
        body+=line(90,y+136,635,y+136,GRAY,True)+text(92,y+225,"横轴：0 → 1 s",22)
    body+=panel(742,310)+text(48,783,"③ 两组单边振幅相同：8 Hz → 1；20 Hz → 0.5",23)
    body+=line(110,995,626,995,GRAY)
    for f,a in [(8,1),(20,.5)]:
        x=110+20*f
        body+=line(x,995,x,995-155*a,BLUE)+dot(x,995-155*a,5,BLUE)
        body+=text(x,1029,f"{f} Hz",22,INK,"middle")+text(x+14,990-155*a,f"{a:g}",22)
    body+=rows(36,1106,["这是这两组整周期记录的 DFT 单边振幅，不是完整频谱。","要还原原波形，还得保存相位；复数保存两类信息。"],22)
    for phi in (0,math.pi/2):
        a=amplitude([math.cos(TAU*8*j/128)+.5*math.cos(TAU*20*j/128+phi) for j in range(128)])
        assert abs(a[8]-1)<1e-12 and abs(a[20]-.5)<1e-12
    write("phase-matters.svg",1200,"不同相位的信号可以拥有相同的单边振幅","8赫兹与20赫兹两个余弦信号仅改变20赫兹相位，时域波形不同；一秒128点DFT单边振幅仍为1和0.5，说明幅度图不能替代完整复频谱。",body)


def sampling():
    body=heading("⑧","采样不够快，快波会冒充慢波")
    body+=rows(36,95,["每秒只取 64 个样本：8 Hz 与 56 Hz 余弦可完全混淆。","下图只放大 0 → 0.125 s；圆点是共同样本。"],23)
    body+=panel(181,330)
    for f,color,dash in [(56,RED,True),(8,BLUE,False)]:
        body+=graph(337,lambda u:math.cos(TAU*f*.125*u),85,color=color,dash=dash,count=1600)
    for j in range(9):
        x=92+536*j/8;y=337-85*math.cos(TAU*8*j/64)
        body+=dot(x,y,6,INK)
        assert abs(math.cos(TAU*8*j/64)-math.cos(TAU*56*j/64))<1e-12
    body+=text(92,480,"实线 8 Hz；虚线 56 Hz；圆点无法区分它们。",23)
    body+=panel(550,250)+rows(48,594,["① 快波可以落在同一串样本上：这是混叠。","② 还原带限信号，需要足够采样率及相应条件。","③ 有限记录还有限制：1 s 的 DFT 格点间距为 1 Hz。","多补几个零，不会凭空延长真实观察时间。"],22,49)
    body+=rows(36,856,["这里没有把 56 Hz 降成 8 Hz；是采样信息分不出。","傅里叶分析不是凭空补回未测到的信息。"],23)
    write("sampling-limits.svg",954,"64赫兹采样下8赫兹和56赫兹余弦的混叠","两条连续余弦在每1/64秒的采样点上相等；图放大首0.125秒，共九个采样点。采样率、观察时长和DFT格点都限制分析。",body)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for draw in (history,heat_balance,modes,decay,orthogonality,continuous,phase,sampling):
        draw()
    print("Generated eight original Fourier figures; verified means, coefficients, phase amplitudes and alias samples.")


if __name__=="__main__":
    main()
