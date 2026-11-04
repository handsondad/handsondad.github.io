"""Reproduce the original reading diagrams used by the historical blog posts."""

from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "archive-guides"
OUT.mkdir(parents=True, exist_ok=True)


def text(x, y, value, size=23, anchor="start", color="#16324f"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
        f'fill="{color}">{escape(value)}</text>'
    )


def arrow(x1, y1, x2, y2, index=0, color="#177e89", animated=True):
    line = (
        f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" '
        'stroke-width="4" marker-end="url(#arrow)"/>'
    )
    if animated:
        line += (
            f'<path class="trace" style="animation-delay:{index}s" '
            f'd="M{x1},{y1} L{x2},{y2}" pathLength="1" fill="none" '
            'stroke="#e18c20" stroke-width="5"/>'
        )
    return line


def save(name, title, description, body, height=540):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {height}" '
        'role="img" aria-labelledby="title desc" lang="zh-CN">'
        f'<title id="title">{escape(title)}</title>'
        f'<desc id="desc">{escape(description)}</desc>'
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
        'refX="7" refY="3" orient="auto" markerUnits="userSpaceOnUse">'
        '<path d="M0,0 L7,3 L0,6" fill="none" stroke="#177e89" stroke-width="2"/>'
        '</marker></defs>'
        '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}'
        '.trace{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1s linear both}'
        '@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}'
        '@media(prefers-reduced-motion:reduce){.trace{animation:none}}'
        '</style>'
        f'<rect width="720" height="{height}" rx="16" fill="#f7fafc"/>'
        + text(30, 43, title, 28)
        + body
        + '</svg>\n'
    )
    ET.fromstring(svg)
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


def cards(name, title, description, rows, footer, animate=False):
    body = ""
    for i, (heading, detail) in enumerate(rows):
        y = 75 + i * 120
        body += (
            f'<rect x="30" y="{y}" width="660" height="90" rx="12" '
            'fill="#eaf3f8" stroke="#bed2df"/>'
            + text(48, y + 34, heading, 25)
            + text(48, y + 66, detail, 21)
        )
        if i < len(rows) - 1:
            body += arrow(360, y + 95, 360, y + 115, i, animated=animate)
    height = 115 + len(rows) * 120
    body += text(30, height - 23, footer, 19)
    save(name, title, description, body, height)


def main():
    body = (
        '<path d="M180,255 L530,245 L555,261 L395,278 L270,274 Z" '
        'fill="#bed2df" stroke="#16324f" stroke-width="3"/>'
        '<path d="M325,260 L277,302 L385,271" fill="#8bb4cc"/>'
        + arrow(360, 232, 360, 95, animated=False)
        + arrow(360, 292, 360, 429, animated=False)
        + arrow(535, 260, 675, 260, animated=False)
        + arrow(185, 260, 45, 260, animated=False)
        + text(380, 120, "升力", 25)
        + text(380, 415, "重力", 25)
        + text(570, 236, "推力", 25)
        + text(55, 236, "阻力", 25)
        + text(30, 475, "平直匀速飞行：升力 = 重力，推力 = 阻力", 24)
        + text(30, 510, "示意：升力垂直来流；滑翔时受力方向不同。", 20)
    )
    save("flight-forces", "飞机不是被一股神秘力量托起来的", "平直匀速飞行时的四力平衡示意，箭头不表示实际力值。", body)

    cards("sun-energy", "一缕阳光，经历两种不同的旅程",
          "核心聚变释放能量，能量经辐射区和对流区到光球，再经真空约499秒到地球。非等比例，动画不是实际速度。",
          [("① 核心：氢聚变成氦", "质量差对应能量；不是煤炭在燃烧"),
           ("② 内部：辐射输运 → 对流输运", "吸收、再发射与散射；不是同一光子的履历"),
           ("③ 光球 → 地球：约 8 分 19 秒", "离开太阳后，穿过约 1.496 亿千米")],
          "箭头依次描出一次；时间和距离均非等比例。", True)

    cards("earth-habitable", "宜居不是集齐勋章，就自动长出生命",
          "液态水、化学原料和能量供给是研究已知生命的线索，宜居条件不等于生命起源的充分条件。",
          [("线索一：液态水与合适的环境", "温度和压力一起决定水能否长期保持液态"),
           ("线索二：原料与可利用的能量", "碳等元素 + 阳光或化学反应提供的能量"),
           ("开放问题：生命最初怎样出现？", "地球提供了实例，但还没有完整起源答案")],
          "这是阅读层次，不是先后发生的三步，也不是概率计算。")

    cards("photosynthesis", "叶子有两份账：能量账与碳账",
          "光反应利用光和水产生氧气、ATP、NADPH；卡尔文循环每固定3个二氧化碳净产1个三碳G3P，消耗9ATP和6NADPH。",
          [("① 光反应｜类囊体膜", "光 + 水 → 氧气；同时形成 ATP、NADPH"),
           ("② 卡尔文循环｜叶绿体基质", "3 CO₂ + 9 ATP + 6 NADPH → 净产 1 G3P"),
           ("③ 碳去了哪里？", "3 个碳 → 1 个三碳 G3P → 糖及其他有机物")],
          "第二行省略辅产物；是物料摘要，不是完整化学方程式。", True)

    cards("respiration", "跟着 6 个碳，走完细胞里的拆包之旅",
          "一分子葡萄糖经糖酵解变成两个三碳丙酮酸，再变成两个二碳乙酰辅酶A并释放两个二氧化碳；循环再释放四个二氧化碳。",
          [("① 糖酵解｜细胞质基质", "6 碳 → 2 × 3 碳丙酮酸；净得 2 ATP"),
           ("② 丙酮酸氧化 → 三羧酸循环", "2 × 3 碳 → 2 × 2 碳 + 2 CO₂ → 再释 4 CO₂"),
           ("③ 电子传递链 → ATP 合酶", "氧气最终接电子形成水；大部分 ATP 在此形成")],
          "按每分子葡萄糖计；第三步的电子来自前面各步。", True)

    body = ""
    for i, (heading, upper, lower, pump, back) in enumerate([
        ("叶绿体｜类囊体膜", "类囊体腔：H⁺积累", "叶绿体基质", "基质 → 腔", "腔 → 基质"),
        ("线粒体｜内膜", "膜间隙：H⁺积累", "线粒体基质", "基质 → 膜间隙", "膜间隙 → 基质"),
    ]):
        y = 85 + i * 285
        body += text(30, y, heading, 26)
        body += f'<rect x="30" y="{y+12}" width="660" height="180" rx="8" fill="#eaf3f8"/>'
        body += f'<rect x="30" y="{y+94}" width="660" height="12" fill="#bed2df"/>'
        body += text(45, y + 44, upper, 22)
        body += text(45, y + 176, lower, 22)
        for x in range(360, 660, 45):
            body += text(x, y + 57, "H⁺", 22)
        body += f'<rect x="520" y="{y+84}" width="30" height="48" rx="8" fill="#8bb4cc"/>'
        body += arrow(290, y + 147, 290, y + 64, 2 * i)
        body += arrow(535, y + 64, 535, y + 147, 2 * i + 1)
        body += text(45, y + 235, "建立梯度：" + pump, 22)
        body += text(360, y + 235, "合成 ATP：" + back, 21)
        body += text(555, y + 140, "ATP 合酶", 22)
    body += text(30, 660, "H⁺示意，不表示实际浓度；两套膜系统并不相同。", 21)
    save("proton-gradient", "相似的能量办法，不同的膜与空间",
         "上图为叶绿体，氢离子在类囊体腔积累，经ATP合酶回流基质。下图为线粒体，氢离子在膜间隙积累，经ATP合酶回流线粒体基质。两者方向按各自空间定义，箭头时长不代表生物速率。",
         body, 690)

    lunar = 12 * 29.5306
    solar = 365.2422
    deficit = solar - lunar
    assert abs(deficit - 10.875) < 0.00001
    assert abs(235 * 29.5306 - 19 * solar) < 0.09
    body = text(30, 100, "12 个平均朔望月", 25)
    body += f'<rect x="30" y="120" width="{lunar * 1.7:.3f}" height="55" rx="8" fill="#66a8c0"/>'
    body += text(48, 156, f"{lunar:.4f} 天", 25, color="#fff")
    body += text(30, 225, "1 个平均回归年", 25)
    body += f'<rect x="30" y="245" width="{solar * 1.7:.3f}" height="55" rx="8" fill="#177e89"/>'
    body += text(48, 281, f"{solar:.4f} 天", 25, color="#fff")
    body += text(30, 355, f"每年约差 {deficit:.3f} 天，差距会逐年累积。", 25)
    body += text(30, 410, "闰月补的是“月”，公历闰年补的是“日”。", 24)
    body += text(30, 465, "柱长按天数计算；19 年 7 闰只是近似协调。", 21)
    save("calendar", "太阳和月亮，并没有把时钟对齐", "平均12个朔望月354.3672天，回归年365.2422天，差10.875天。柱长使用相同比例。", body, 500)

    cards("computer", "按下 A，屏幕为什么会出现 A？",
          "简化的键盘输入、程序处理与显示过程。字符A的Unicode码点为65，八位二进制表示是01000001，但键盘事件本身并不直接发送这个字符编码。",
          [("① 输入：键盘产生按键事件", "系统结合键盘布局、修饰键和输入法解释"),
           ("② 处理：程序更新文本与内存", "A 的码点是 65；8 位写作 01000001"),
           ("③ 输出：字体字形被绘制成像素", "编码不是字的照片；显示还需要字形和布局")],
          "逻辑层示意：省略硬件中断、缓存和图形渲染细节。", True)
    assert int("01000001", 2) == ord("A")
    assert 6 == 2 * 3 == 2 * 2 + 2 == 2 + 4
    assert 3 + 3 * 5 == 6 * 3 == 3 + 5 * 3
    assert 490 < 149_597_870.7 / 299_792.458 < 510

    cards("parent-pause", "不必立刻成为完美父母",
          "给照护者的非诊断性自我提醒：先确保孩子安全，再辨认自己的感受，必要时寻求支持。这不是固定发展阶段。",
          [("停一下：先照顾安全", "累了可以求助；不要把忍到极限当作责任"),
           ("说具体：看见当下", "“我现在很疲惫”，比“我不是好父母”更准确"),
           ("做一件小事：给关系留空间", "陪伴、休息、轮换照护，都可以是下一步")],
          "这是自我提醒，不是心理评估或治疗方法。")

    cards("ai-evidence", "遇到一句 AI 预言，先分清它是哪一层",
          "区分观察、预测和个人选择：具体模型表现需要测试，未来预测带有条件，个人选择涉及价值判断。",
          [("① 观察：这次真的发生了什么？", "具体模型、具体任务、可复查的输入和结果"),
           ("② 推断：成立需要哪些条件？", "从一次成功，不能跳到“所有工作都会消失”"),
           ("③ 选择：我们愿意怎样使用？", "让工具扩展尝试，而不是替我们承担责任")],
          "每向下一层，都要补一层理由；这不是历史时间线。")
    cards("ai-limits", "三种“做不到”，不要混成一句话",
          "逻辑不可判定、现实资源不足、现有模型表现差是不同限制。标准量子计算不消除不可判定性。",
          [("逻辑边界：不存在包办全部情况的算法", "停机问题：不能对任意程序与输入都正确判定"),
           ("资源边界：理论可算，现实未必算得动", "密码学安全要写清假设、攻击模型与资源"),
           ("当前能力：这个模型这一次没做好", "可通过更好的模型、工具和验证改善")],
          "三类限制不是包含关系，也不是性能排行榜。")

    guides = [
        ("play", "十个网站，不如完成一次共同探索",
         [("先选：今晚只解决一个小问题", "故事 → 讲结局；天气 → 比两个城市"),
          ("再做：给孩子一个能动手的任务", "JRMF 摆一题；植物建模改一个参数"),
          ("最后：关掉网页，带走一个作品", "一张图、一段复述，或明天去公园的问题")],
         "年龄只是选题建议；账号、收费和隐私需家长先检查。"),
        ("parenting", "育儿信息，不按星级选，按问题选",
         [("健康与发展担忧 → 儿保或儿科", "带上具体观察；网络清单不能替代专业评估"),
          ("日常陪伴怎么做 → 可信机构指南", "先选一条适合家庭的建议，而非下载十张量表"),
          ("理念怎么讨论 → 书籍与家人对话", "经典书也有时代局限；安全建议以现行指南为准")],
         "这是信息分流，不是诊断流程；紧急情况应及时就医。"),
        ("science", "把模拟器玩成一场小实验",
         [("① 先猜：投射角越大，落点越远？", "先写下猜测；在相同条件下比较"),
          ("② 再改：只改变一个变量", "理想无空气阻力、同高落地时比较 30°/45°/60°"),
          ("③ 最后解释：模型省略了什么？", "现实有风、阻力和不同的起落高度")],
         "可在 oPhysics 选投射运动；先确认模拟的假设。"),
        ("ai", "AI 小实验：先猜边界，再看训练",
         [("① 选数据：圆环还是螺旋？", "TensorFlow Playground 有预设数据，不必手绘"),
          ("② 做比较：只改变一项设置", "固定数据与其他参数，比较训练和测试误差"),
          ("③ 找边界：训练好，不等于处处好", "多试几次随机初始化；不上传儿童个人资料")],
         "模型图展示数值计算，不是读取机器的主观想法。"),
        ("coding", "编程第一课：让角色走出一个正方形",
         [("① 预测：走一步，再转 90°", "Scratch：移动 50 步，右转 90 度"),
          ("② 重复：把两条积木重复 4 次", "先在纸上画路线，再让角色验证"),
          ("③ 调试：如果改成 3 次或 5 次？", "观察终点与朝向；错误也是一条线索")],
         "积木数值是示例；先复位位置和方向再比较。"),
        ("nature", "从“软件说像”到“我有证据”",
         [("① 观察：先记录，不惊扰", "外形、时间、环境；远距离拍照"),
          ("② 比对：识别结果只是候选", "找两项可见特征；不确定就保留不确定"),
          ("③ 分享：保护生物，也保护孩子", "隐藏住宅学校位置；不公开敏感物种坐标")],
         "不捕捉、不投喂、不用鸟声诱鸟；不要凭识别结果食用。"),
        ("arts", "看一件文物，也能像侦探办案",
         [("① 先看图：只描述你真的看见的", "颜色、形状、材料；暂时不猜故事"),
          ("② 再读著录：把猜测和记录对照", "年代、用途、出处；区分事实与推测"),
          ("③ 留一个问题：换一件作品比较", "同样是瓶子，不同时期为什么长得不同？")],
         "馆藏总数不等于全部高清公开；下载复用须看授权。"),
        ("world", "资源地图：按今天的问题入场",
         [("想解释一个现象 → 科学与数学", "PhET / OpenStax / GeoGebra：先猜再验证"),
          ("想完成一个作品 → 编程与艺术", "Scratch / 博物馆藏品：做一件小作品"),
          ("想查一条信息 → 百科与机构", "找原始出处、日期和适用条件，不只看排名")],
         "导航不是质量保证；免费阅读不等于免费课程或转载权。"),
    ]
    for name, title, rows, footer in guides:
        cards(f"guide-{name}", title, "；".join(h + "：" + d for h, d in rows), rows, footer)

    print(f"Generated {len(list(OUT.glob('*.svg')))} original archive diagrams.")


if __name__ == "__main__":
    main()
