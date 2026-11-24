"""集装箱编码与商品编码体系：ISO 6346、HS、GTIN、ISBN、VIN 原创图解。"""

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

TOPIC = "commodity-codes"

LETTER_VALUES = {}
_v = 10
for _ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    if _v in (11, 22, 33):
        _v += 1
    LETTER_VALUES[_ch] = _v
    _v += 1


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


def container_check_digit(first10: str) -> int:
    total = 0
    for idx, ch in enumerate(first10):
        value = int(ch) if ch.isdigit() else LETTER_VALUES[ch]
        total += value * (2**idx)
    remainder = total % 11
    return 0 if remainder == 10 else remainder


def container_products(first10: str):
    out = []
    for idx, ch in enumerate(first10):
        value = int(ch) if ch.isdigit() else LETTER_VALUES[ch]
        weight = 2**idx
        out.append((ch, value, weight, value * weight))
    return out, sum(p[-1] for p in out)


def ean13_check_digit(body12: str) -> int:
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(body12))
    return (10 - total % 10) % 10


L_CODE = [
    "0001101", "0011001", "0010011", "0111101", "0100011",
    "0110001", "0101111", "0111011", "0110111", "0001011",
]
G_CODE = [
    "0100111", "0110011", "0011011", "0100001", "0011101",
    "0111001", "0000101", "0010001", "0001001", "0010111",
]
R_CODE = [
    "1110010", "1100110", "1101100", "1000010", "1011100",
    "1001110", "1010000", "1000100", "1001000", "1110100",
]
PARITY = [
    "LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG",
    "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL",
]


def ean13_modules(digits13: str) -> str:
    modules = "101"
    parity = PARITY[int(digits13[0])]
    for i in range(1, 7):
        table = L_CODE if parity[i - 1] == "L" else G_CODE
        modules += table[int(digits13[i])]
    modules += "01010"
    for ch in digits13[7:13]:
        modules += R_CODE[int(ch)]
    modules += "101"
    return modules


def _verify() -> None:
    assert LETTER_VALUES["A"] == 10 and LETTER_VALUES["B"] == 12
    assert LETTER_VALUES["K"] == 21 and LETTER_VALUES["L"] == 23
    assert LETTER_VALUES["U"] == 32 and LETTER_VALUES["V"] == 34
    assert LETTER_VALUES["Z"] == 38
    assert container_check_digit("BICU123456") == 5
    assert container_check_digit("CSQU305438") == 3
    assert container_check_digit("MSKU388110") == 7
    assert container_check_digit("SUDU307007") == 9
    assert ean13_check_digit("930123456789") == 7
    assert ean13_check_digit("690123456789") == 2
    assert len(ean13_modules("6901234567892")) == 95

    # ISO 6346：模 11 的素数性质 + 2 的幂权重，任何单位错与相邻换位都能抓住。
    for a in range(10):
        for b in range(10):
            if a == b:
                continue
            for i in range(10):
                assert (a - b) * (2**i) % 11 != 0

    # GTIN 的 1/3 权重会漏掉约 11% 的相邻换位（差为 5 的十种有序组合）。
    missed = [(a, b) for a in range(10) for b in range(10) if a != b and 2 * (a - b) % 10 == 0]
    assert len(missed) == 10
    assert abs(len(missed) / 90 - 0.1111) < 1e-3

    # NHTSA 官方示例：加权和 351，余 10 写作 X。
    assert sum([8, 28, 48, 35, 16, 12, 18, 10, 18, 56, 0, 24, 10, 28, 24, 16]) == 351
    assert 351 % 11 == 10


# ---------------------------------------------------------------------------
# 1. 集装箱号的解剖图
# ---------------------------------------------------------------------------
def build_container_anatomy() -> str:
    els = []
    els.extend(
        header(
            "集装箱的 11 位身份证：每一段都有主人",
            "箱主代号、设备类别、顺序号、校验位——连最后一位的方框都有讲究。",
        )
    )

    els.append(card(20, 66, 720, 190))
    els.append(txt(40, 94, "ISO 6346 识别标记示例", size=12.2, color=INK, weight="700"))
    segments = [
        (40, 150, 172, "BIC", "箱主代号（3 位字母）", "向 BIC 注册，全球唯一", BLUE, BLUE_SOFT),
        (218, 150, 76, "U", "设备类别（1 位）", "U 箱 / J 设备 / Z 底盘", ORANGE, ORANGE_SOFT),
        (300, 150, 212, "123456", "顺序号（6 位数字）", "箱主编制，不足补 0", GREEN, GREEN_SOFT),
        (518, 150, 92, "5", "校验位（1 位）", "前 10 位算出，常加框", PURPLE, PURPLE_SOFT),
    ]
    for x, y, w, value, title, note, fg, soft in segments:
        els.append(f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="6" fill="{soft}" stroke="{fg}" stroke-width="1.3"/>')
        els.append(txt(x + w / 2, y + 33, value, size=21 if w > 100 else 19, color=fg, anchor="middle", weight="700"))
        els.append(txt(x + w / 2, y + 68, title, size=10.8, color=INK, anchor="middle", weight="600"))
        els.append(txt(x + w / 2, y + 88, note, size=9.6, color=MUTED, anchor="middle"))
    els.append(txt(40, 126, "BICU 123456 5", size=13.5, color=SLATE, anchor="start"))
    els.append(txt(706, 126, "共 11 个字符", size=11.2, color=SLATE, anchor="end", weight="600"))

    els.append(card(20, 270, 352, 196))
    els.append(step_badge(38, 292, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 296, "箱主代号：先注册，才敢刷漆", size=12.0, color=INK, weight="700"))
    els.append(txt(38, 324, "• 前 3 位字母（如 BIC、MSU、COS）由箱主", size=10.4, color=BODY))
    els.append(txt(38, 345, "  向 BIC 登记；第 4 位字母说明设备种类。", size=10.4, color=BODY))
    els.append(txt(38, 370, "• 同一个箱子在门板、侧板、顶板上都刷同一串号，", size=10.4, color=BODY))
    els.append(txt(38, 391, "  码头、堆场、船公司靠它跨系统对上号。", size=10.4, color=BODY))
    els.append(txt(38, 420, "BIC 国际箱主代号登记册自 1970 年起发布。", size=10.2, color=BLUE, weight="600"))
    els.append(txt(38, 446, "校验位正确 ≠ 这个箱子真的存在。", size=10.4, color=ORANGE, weight="700"))

    els.append(card(388, 270, 352, 196))
    els.append(step_badge(406, 292, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(424, 296, "尺寸类型码：另外 4 位字符", size=12.0, color=INK, weight="700"))
    els.append(txt(404, 326, "第 1 位：长度    第 2 位：高度／宽度", size=10.6, color=INK, weight="600"))
    els.append(txt(404, 348, "第 3–4 位：箱型与版本（G1=通用箱）", size=10.4, color=SLATE))
    els.append(pill(404, 366, "22G1 → 20 英尺普通箱", fg=BLUE, bg=BLUE_SOFT, w=150, h=24, size=10.4))
    els.append(txt(562, 383, "高 8 英尺 6 英寸（2591 mm）", size=10.0, color=SLATE))
    els.append(pill(404, 402, "45G1 → 40 英尺高箱", fg=ORANGE, bg=ORANGE_SOFT, w=150, h=24, size=10.4))
    els.append(txt(562, 419, "高 9 英尺 6 英寸（2896 mm）", size=10.0, color=SLATE))
    els.append(txt(404, 446, "号码说明“是谁的箱子”，类型码说明“怎样的箱子”。", size=10.4, color=GREEN, weight="600"))

    els.append(card(20, 480, 720, 36, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 504, "1956 年现代集装箱运输起步；1968 年前后 ISO 推出统一标志，随后形成 ISO 6346。", size=10.6, color=SLATE))

    return figure(
        526,
        "ISO 6346 集装箱号与尺寸类型码解剖图",
        "11位集装箱号由3位注册箱主代号、1位设备类别字母U或J或Z、6位顺序号和1位校验位组成，尺寸类型码另占4位，例如22G1表示20英尺普通箱，45G1表示40英尺高箱；校验位正确只说明号码内部自洽，并不证明箱子真实存在。",
        els,
    )


# ---------------------------------------------------------------------------
# 2. 校验位对决：模 11 与模 10
# ---------------------------------------------------------------------------
def build_check_digit_duel() -> str:
    products, total = container_products("BICU123456")
    assert total == 5494
    cd = container_check_digit("BICU123456")
    assert cd == 5

    els = []
    els.extend(
        header(
            "最后一位不是装饰：两种模数，两套防错逻辑",
            "集装箱用模 11 + 2 的幂；商品条码用模 10 + 1/3 交替权重。",
        )
    )

    els.append(card(20, 66, 352, 326))
    els.append(step_badge(38, 88, 1, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(56, 92, "集装箱：BICU 123456 → 5", size=11.8, color=INK, weight="700"))
    x0, step = 80, 28
    chars = [p[0] for p in products]
    vals = [str(p[1]) for p in products]
    weights = [str(p[2]) for p in products]
    prods = [str(p[3]) for p in products]
    for row_idx, row in enumerate([chars, vals, weights, prods]):
        y = 124 + row_idx * 30
        for i, v in enumerate(row):
            els.append(txt(x0 + i * step, y, v, size=9.0 if row_idx == 3 else 10.0, anchor="middle",
                           color=[INK, BLUE, SLATE, ORANGE][row_idx], weight="700" if row_idx in (0, 3) else None))
    els.append(txt(40, 124, "字符", size=9.8, color=MUTED))
    els.append(txt(40, 154, "数值", size=9.8, color=MUTED))
    els.append(txt(40, 184, "权重", size=9.8, color=MUTED))
    els.append(txt(40, 214, "乘积", size=9.8, color=MUTED))
    els.append(_line(36, 260, 356, 260, stroke=BORDER, sw=1))
    els.append(txt(40, 300, "字母值从 A=10 起算，跳过 11 的倍数", size=10.0, color=SLATE))
    els.append(txt(40, 330, "权重依次是 1、2、4、…、512（2 的幂）", size=10.0, color=SLATE))
    els.append(txt(40, 374, f"Σ = {total}；5494 mod 11 = {cd}", size=11.6, color=ORANGE, weight="700"))

    els.append(card(388, 66, 352, 326))
    els.append(step_badge(406, 88, 2, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(424, 92, "商品条码：930123456789 → 7", size=11.8, color=INK, weight="700"))
    body = "930123456789"
    x1, step2 = 436, 25
    for row_idx, row in enumerate([list(body), ["1" if i % 2 == 0 else "3" for i in range(12)],
                                   [str(int(d) * (1 if i % 2 == 0 else 3)) for i, d in enumerate(body)]]):
        y = 132 + row_idx * 32
        for i, v in enumerate(row):
            els.append(txt(x1 + i * step2, y, v, size=10.6 if row_idx < 2 else 9.8, anchor="middle",
                           color=[INK, BLUE, GREEN][row_idx], weight="700" if row_idx == 0 else None))
    els.append(txt(400, 132, "数字", size=9.8, color=MUTED))
    els.append(txt(400, 164, "权重", size=9.8, color=MUTED))
    els.append(txt(400, 196, "乘积", size=9.8, color=MUTED))
    els.append(_line(400, 262, 724, 262, stroke=BORDER, sw=1))
    els.append(txt(404, 300, "从左往右权重 1、3 交替，正好是模 10 的简便写法", size=10.0, color=SLATE))
    els.append(txt(404, 330, "校验位把加权和补到下一个整十", size=10.0, color=SLATE))
    els.append(txt(404, 374, "Σ = 113；下个整十是 120 ⇒ 校验位 7", size=11.2, color=BLUE, weight="700"))

    els.append(card(20, 408, 720, 118))
    els.append(txt(40, 434, "防错能力：为什么一个用素数 11，一个用十进制？", size=12.0, color=INK, weight="700"))
    els.append(txt(40, 462, "ISO 6346：2 的幂与 11 互素，单位错与相邻换位必被抓住；", size=10.6, color=ORANGE, weight="600"))
    els.append(txt(40, 484, "但字母值 A=10 与 K=21 相差 11，单字母替换可能漏网；余数 10 又被写成 0。", size=10.4, color=SLATE))
    els.append(txt(400, 462, "GTIN：1/3 权重抓所有单位错，但漏掉约 11% 的相邻换位", size=10.6, color=BLUE, weight="600"))
    els.append(txt(400, 484, "（两数相差 5 时 2×5≡0 mod 10），性价比高、适合人工抄写。", size=10.4, color=SLATE))
    els.append(txt(40, 510, "校验位只能发现“号码内部不一致”，不能证明货物、车辆或箱子真实存在。", size=10.4, color=PURPLE, weight="700"))

    return figure(
        538,
        "ISO 6346 模 11 校验位与 GTIN 模 10 校验位计算对决图",
        "左侧用BICU123456演示集装箱校验位：字母按A为10且跳过11的倍数换算，前10位依次乘1至512的2的幂，总和5494除以11余5；右侧用930123456789演示GTIN校验位：交替乘1和3得113，下一个整十为120故校验位7；底部比较两者的检错能力与盲区。",
        els,
    )


# ---------------------------------------------------------------------------
# 3. HS 编码层级
# ---------------------------------------------------------------------------
def build_hs_hierarchy() -> str:
    assert "851762"[:2] == "85" and "851762"[:4] == "8517"
    els = []
    els.extend(
        header(
            "HS 编码：前 6 位全球通用，后面才轮到各国",
            "同一台智能手机，在 200 多个经济体报关时写下的前 6 位完全一样。",
        )
    )

    els.append(card(20, 66, 352, 388))
    els.append(step_badge(38, 88, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 92, "六位数字，三层含义", size=12.0, color=INK, weight="700"))
    layers = [
        ("85", "章（Chapter）", "电机、电气设备及其零件", BLUE, BLUE_SOFT, 108),
        ("17", "目（Heading）", "电话机、数据传输设备", ORANGE, ORANGE_SOFT, 186),
        ("62", "子目（Subheading）", "接收、转换与传输数据的设备", GREEN, GREEN_SOFT, 264),
    ]
    for code, label, desc, fg, soft, y in layers:
        els.append(f'<rect x="38" y="{y}" width="64" height="58" rx="7" fill="{soft}" stroke="{fg}" stroke-width="1.4"/>')
        els.append(txt(70, y + 39, code, size=20, color=fg, anchor="middle", weight="700"))
        els.append(txt(116, y + 24, label, size=11.4, color=INK, weight="700"))
        els.append(txt(116, y + 45, desc, size=9.8, color=SLATE))
    els.append(txt(40, 348, "合起来：8517.62", size=13.0, color=INK, weight="700"))
    els.append(txt(40, 375, "HS 按材料与功能分类，不按品牌分类。", size=10.4, color=BODY))
    els.append(txt(40, 400, "第 77 章在国际目录中留空备用。", size=10.0, color=MUTED))

    els.append(card(388, 66, 352, 388))
    els.append(step_badge(406, 88, 2, fg=ORANGE, bg=ORANGE_SOFT))
    els.append(txt(424, 92, "中国的 6 → 8 → 10 位扩展", size=12.0, color=INK, weight="700"))
    els.append(f'<rect x="404" y="120" width="90" height="34" rx="5" fill="{BLUE_SOFT}" stroke="{BLUE}"/>')
    els.append(txt(449, 143, "851762", size=12.0, color=BLUE, anchor="middle", weight="700"))
    els.append(txt(506, 143, "国际统一 6 位", size=10.6, color=SLATE))
    els.append(f'<rect x="404" y="172" width="126" height="34" rx="5" fill="{ORANGE_SOFT}" stroke="{ORANGE}"/>')
    els.append(txt(467, 195, "851762XX", size=12.0, color=ORANGE, anchor="middle", weight="700"))
    els.append(txt(542, 195, "8 位税则号列", size=10.6, color=SLATE))
    els.append(f'<rect x="404" y="224" width="166" height="34" rx="5" fill="{GREEN_SOFT}" stroke="{GREEN}"/>')
    els.append(txt(487, 247, "851762XXXX", size=12.0, color=GREEN, anchor="middle", weight="700"))
    els.append(txt(582, 247, "10 位商品编号", size=10.6, color=SLATE))
    els.append(_line(404, 282, 724, 282, stroke=BORDER, sw=1))
    els.append(txt(404, 308, "• 第 7、8 位：我国自主编制的本国子目", size=10.4, color=BODY))
    els.append(txt(404, 332, "• 第 9、10 位：监管与统计进一步拆分", size=10.4, color=BODY))
    els.append(txt(404, 360, "• 我国 1992 年起全面采用 HS", size=10.4, color=BODY))
    els.append(txt(404, 388, "• WCO 每 4–6 年修订一次（HS 2022 为现行版本）", size=10.2, color=SLATE))
    els.append(txt(404, 420, "全球 21 类 97 章，5000 多个商品组。", size=10.8, color=ORANGE, weight="700"))

    els.append(card(20, 470, 720, 36, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 494, "国际贸易中超过 98% 的货物按 HS 归类；它决定关税、监管条件与贸易统计口径。", size=10.6, color=SLATE))

    return figure(
        516,
        "HS 编码六位层级与中国八位十位扩展图",
        "HS编码前两位是章、三四位是目、五六位是子目，例如851762；我国1992年起采用HS，在6位国际编码基础上增设本国子目形成8位税则号列，实际申报再用10位商品编号；WCO称HS含5000多个商品组，覆盖全球98%以上货物贸易。",
        els,
    )


# ---------------------------------------------------------------------------
# 4. EAN-13 条码与 ISBN
# ---------------------------------------------------------------------------
def build_ean13_barcode() -> str:
    digits = "6901234567892"
    body = digits[:12]
    check = ean13_check_digit(body)
    assert check == 2
    modules = ean13_modules(digits)
    assert len(modules) == 95 and modules.startswith("101") and modules.endswith("101")

    css = (
        "<style>\n"
        "  @keyframes scanSweep { 0% { transform: translateX(0); opacity: 0.25; } "
        "100% { transform: translateX(202px); opacity: 1; } }\n"
        "  .scan-line { animation: scanSweep 2.6s ease-in-out 1 forwards; }\n"
        "  @media (prefers-reduced-motion: reduce) { "
        ".scan-line { animation: none !important; transform: none !important; opacity: 1 !important; } }\n"
        "</style>"
    )

    els = []
    els.extend(
        header(
            "EAN-13 条码：前缀 690 不是“成分密码”",
            "扫码器读的是条空宽度，数字只是给人看的；前缀只说明在哪里申请。",
        )
    )

    els.append(card(20, 66, 352, 386))
    els.append(step_badge(38, 88, 1, fg=BLUE, bg=BLUE_SOFT))
    els.append(txt(56, 92, "按 EAN-13 规则逐模块画出的真实条码", size=11.6, color=INK, weight="700"))
    x, bar_w = 42, 2
    for i, bit in enumerate(modules):
        if bit == "1":
            guard = i < 3 or 45 <= i < 50 or i >= 92
            height = 104 if guard else 92
            els.append(
                f'<rect x="{x + i * bar_w}" y="{132 - (height - 92) / 2}" width="{bar_w}" height="{height}" '
                f'fill="{INK}"/>'
            )
    els.append('<g class="scan-line">')
    els.append(_line(42, 122, 42, 246, stroke=ORANGE, sw=2))
    els.append("</g>")
    els.append(txt(142, 262, digits, size=15.0, color=INK, anchor="middle", weight="700"))
    els.append(txt(142, 288, "95 个模块 · 左右各 10 个静区", size=10.4, color=SLATE, anchor="middle"))
    els.append(txt(38, 326, "前 3 位 690：GS1 分配给中国的国家前缀", size=10.4, color=BLUE, weight="600"))
    els.append(txt(38, 351, "中间厂商代码 + 商品项目代码由编码组织与厂商分配", size=10.2, color=SLATE))
    els.append(txt(38, 380, "“690 表示含激素、691 含铅汞”是谣言：", size=10.4, color=ORANGE, weight="700"))
    els.append(txt(38, 404, "前缀只表示条码申请地，与成分、产地无必然关系。", size=10.2, color=BODY))
    els.append(txt(38, 434, "ISBN-13 以 978/979 开头，沿用同一套 GTIN 校验算法。", size=10.4, color=PURPLE, weight="600"))

    els.append(card(388, 66, 352, 386))
    els.append(step_badge(406, 88, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(424, 92, "校验位：把加权和补到整十", size=12.0, color=INK, weight="700"))
    d12 = list(body)
    x1, step = 436, 25
    for row_idx, row in enumerate([d12, ["1" if i % 2 == 0 else "3" for i in range(12)],
                                   [str(int(d) * (1 if i % 2 == 0 else 3)) for i, d in enumerate(d12)]]):
        y = 132 + row_idx * 32
        for i, v in enumerate(row):
            els.append(txt(x1 + i * step, y, v, size=10.8 if row_idx < 2 else 9.8, anchor="middle",
                           color=[INK, BLUE, GREEN][row_idx], weight="700" if row_idx == 0 else None))
    els.append(txt(400, 132, "数字", size=9.8, color=MUTED))
    els.append(txt(400, 164, "权重", size=9.8, color=MUTED))
    els.append(txt(400, 196, "乘积", size=9.8, color=MUTED))
    els.append(_line(400, 262, 724, 262, stroke=BORDER, sw=1))
    els.append(txt(404, 286, "从左往右权重 1、3、1、3……", size=10.2, color=SLATE))
    els.append(txt(404, 314, "校验位 = 10 − (Σ mod 10)，若整除则写 0", size=10.2, color=SLATE))
    els.append(txt(404, 354, "加权和 = 128 ⇒ 下一个整十是 130", size=11.0, color=GREEN, weight="700"))
    els.append(txt(404, 382, "校验位 = 130 − 128 = 2", size=11.6, color=INK, weight="700"))
    els.append(_line(404, 398, 724, 398, stroke=BORDER, sw=1))
    els.append(txt(404, 424, "完整 GTIN-13：6901234567892", size=11.4, color=PURPLE, weight="700"))
    els.append(txt(404, 448, "ISBN-13、EAN-13、GTIN-13 是同一族编码。", size=10.2, color=SLATE))

    els.append(card(20, 466, 720, 36, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 490, "图中条码按 EAN-13 的 L/G/R 编码表逐模块计算生成，非示意图；扫描线动画只播放一次。", size=10.6, color=SLATE))

    return figure(
        512,
        "EAN-13 商品条码结构、校验位与 ISBN 关系图",
        "以6901234567892为例，条码按EAN-13的L/G/R编码表生成95个模块；前12位交替乘1和3得128，补到130得校验位2；前缀690只是GS1分配给中国的国家代码，与商品成分无关，ISBN-13以978或979开头沿用同一校验算法。",
        els,
        extra_css=css,
    )


# ---------------------------------------------------------------------------
# 5. VIN 与一物多码
# ---------------------------------------------------------------------------
def build_vin_ecosystem() -> str:
    els = []
    els.extend(
        header(
            "VIN：17 位里藏着出生年份，第 9 位也在防手滑",
            "一辆车、一只箱、一件商品各有各的码：认准“识别对象”才不会串线。",
        )
    )

    els.append(card(20, 66, 720, 176))
    els.append(txt(40, 94, "VIN 示例：1M8GDM9AXKP042788", size=12.2, color=INK, weight="700"))
    vin = "1M8GDM9AXKP042788"
    groups = [(0, 3, "WMI 世界制造厂识别", BLUE, BLUE_SOFT),
              (3, 5, "VDS 车辆特征", ORANGE, ORANGE_SOFT),
              (8, 1, "校验位", PURPLE, PURPLE_SOFT),
              (9, 8, "VIS 车辆指示", GREEN, GREEN_SOFT)]
    x0 = 40
    for i, ch in enumerate(vin):
        fg, soft = SLATE, "#f1f5f9"
        for start, length, _, gfg, gsoft in groups:
            if start <= i < start + length:
                fg, soft = gfg, gsoft
        xx = x0 + i * 39
        els.append(f'<rect x="{xx}" y="112" width="34" height="34" rx="4" fill="{soft}" stroke="{fg}" stroke-width="1.1"/>')
        els.append(txt(xx + 17, 136, ch, size=12.0, color=fg, anchor="middle", weight="700"))
        els.append(txt(xx + 17, 160, str(i + 1), size=8.6, color=MUTED, anchor="middle"))
    els.append(txt(40, 192, "第 10 位 = 车型年份；第 11 位 = 装配工厂；第 12–17 位 = 生产序号", size=10.6, color=SLATE))
    els.append(txt(40, 222, "VIN 中不准出现字母 I、O、Q，避免与数字 1、0 混淆。", size=10.6, color=BODY))

    els.append(card(20, 258, 352, 206))
    els.append(step_badge(38, 280, 1, fg=PURPLE, bg=PURPLE_SOFT))
    els.append(txt(56, 284, "第 9 位 X 是怎么算出来的？", size=11.8, color=INK, weight="700"))
    els.append(txt(38, 314, "权重：8 7 6 5 4 3 2 10 | 0 | 9 8 7 6 5 4 3 2", size=10.6, color=PURPLE, weight="600"))
    els.append(txt(38, 342, "字母换算：A=1 … H=8，J=1，K=2，L=3，M=4 …", size=10.2, color=SLATE))
    els.append(txt(38, 370, "把除第 9 位外的 16 个字符按位加权求和：", size=10.4, color=BODY))
    els.append(txt(38, 398, "Σ = 351；351 ÷ 11 = 31 余 10", size=11.2, color=INK, weight="700"))
    els.append(txt(38, 426, "余 10 写作 X ⇒ 校验位 X（NHTSA 官方算例）", size=11.0, color=PURPLE, weight="700"))

    els.append(card(388, 258, 352, 206))
    els.append(step_badge(406, 280, 2, fg=GREEN, bg=GREEN_SOFT))
    els.append(txt(424, 284, "一物多码：各管各的一段路", size=11.8, color=INK, weight="700"))
    rows = [
        ("集装箱号", "识别一只箱子", "ISO 6346 / BIC"),
        ("HS 编码", "识别商品类别", "WCO / 各国海关"),
        ("GTIN 条码", "识别一个贸易项目", "GS1 / 各国编码组织"),
        ("ISBN", "识别一种出版物", "国际 ISBN 机构"),
        ("VIN", "识别一辆车", "ISO 3779 / 各国监管"),
    ]
    for i, (name, target, owner) in enumerate(rows):
        y = 310 + i * 28
        els.append(txt(404, y, name, size=10.6, color=INK, weight="700"))
        els.append(txt(500, y, target, size=10.2, color=BODY))
        els.append(txt(650, y, owner, size=9.8, color=MUTED))
        els.append(_line(404, y + 6, 724, y + 6, stroke=BORDER, sw=1))
    els.append(txt(404, 454, "编码的对象不同，校验算法也不能互换。", size=10.6, color=GREEN, weight="700"))

    els.append(card(20, 478, 720, 36, fill="#f1f5f9", stroke=BORDER))
    els.append(txt(36, 502, "从左到右：箱子是谁的、货是什么、商品是哪一款、书是哪一版、车是哪一台。", size=10.6, color=SLATE))

    return figure(
        524,
        "VIN 结构、校验位算例与常见编码对象对照图",
        "VIN共17位，前3位世界制造厂识别，4至8位车辆特征，第9位是校验位，10至17位含车型年份、工厂与生产序号；按NHTSA权重8到2计算，示例中加权和351除以11余10故校验位写作X；图右对照集装箱号、HS、GTIN、ISBN与VIN各自识别的对象。",
        els,
    )


@register(TOPIC, "集装箱编码与商品编码体系：ISO 6346、HS、GTIN、ISBN、VIN 原创图解", "science_tech")
def build_all() -> None:
    _verify()
    builders = [
        ("container-number-anatomy.svg", build_container_anatomy),
        ("check-digit-mod11-vs-mod10.svg", build_check_digit_duel),
        ("hs-code-hierarchy.svg", build_hs_hierarchy),
        ("ean13-barcode-anatomy.svg", build_ean13_barcode),
        ("vin-and-code-ecosystem.svg", build_vin_ecosystem),
    ]
    for fname, fn in builders:
        write_svg(TOPIC, fname, fn())
