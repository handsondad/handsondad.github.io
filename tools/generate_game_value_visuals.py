"""Generate original game-theory diagrams and check the constructions."""

import math
from itertools import combinations
from pathlib import Path
import xml.etree.ElementTree as ET

from generate_bernoulli_visuals import BLUE, INK, MUTED, ORANGE, document, text


OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "game-value"
WIN_FILL = "#d9eef5"
LOSS_FILL = "#f8e6d4"
LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def panel(x, y, width, height):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16" '
        'fill="#fff" stroke="#c9d6df" stroke-width="2"/>'
    )


def winner(board):
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return 0


def ttt_value(board, turn, memo):
    found = winner(board)
    if found == 1:
        return 1
    if found == 2:
        return -1
    if all(board):
        return 0
    key = (board, turn)
    if key in memo:
        return memo[key]
    scores = []
    for index, cell in enumerate(board):
        if cell:
            continue
        nxt = list(board)
        nxt[index] = turn
        scores.append(ttt_value(tuple(nxt), 3 - turn, memo))
    result = max(scores) if turn == 1 else min(scores)
    memo[key] = result
    return result


def count_games(board=(0,) * 9, turn=1):
    found = winner(board)
    if found == 1:
        return 1, 0, 0
    if found == 2:
        return 0, 1, 0
    if all(board):
        return 0, 0, 1
    wins = draws = losses = 0
    for index, cell in enumerate(board):
        if cell:
            continue
        nxt = list(board)
        nxt[index] = turn
        w, l, d = count_games(tuple(nxt), 3 - turn)
        wins += w
        losses += l
        draws += d
    return wins, losses, draws


def reachable_positions():
    seen = set()

    def walk(board, turn):
        seen.add(board)
        if winner(board) or all(board):
            return
        for index, cell in enumerate(board):
            if cell:
                continue
            nxt = list(board)
            nxt[index] = turn
            walk(tuple(nxt), 3 - turn)

    walk((0,) * 9, 1)
    return seen


def choose_ttt(memo):
    chosen = None
    for cross_cells in combinations(range(9), 3):
        remaining = [cell for cell in range(9) if cell not in cross_cells]
        for circle_cells in combinations(remaining, 3):
            board_list = [0] * 9
            for cell in cross_cells:
                board_list[cell] = 1
            for cell in circle_cells:
                board_list[cell] = 2
            board = tuple(board_list)
            if winner(board) or ttt_value(board, 1, memo) != 0:
                continue
            traps, safe = [], []
            for index, cell in enumerate(board):
                if cell:
                    continue
                nxt = list(board)
                nxt[index] = 1
                nxt_t = tuple(nxt)
                if winner(nxt_t) == 1:
                    continue
                score = ttt_value(nxt_t, 2, memo)
                if score == 0:
                    safe.append(index)
                elif score == -1:
                    for reply, mark in enumerate(nxt):
                        if mark:
                            continue
                        answered = list(nxt)
                        answered[reply] = 2
                        if winner(tuple(answered)) == 2:
                            traps.append((index, reply))
                            break
            if traps and safe:
                candidate = (board, traps[0], safe[0])
                if chosen is None or candidate < chosen:
                    chosen = candidate
    if chosen is None:
        raise RuntimeError("no illustrative tic-tac-toe position")
    return chosen


def subtraction_loss(n, memo):
    if n in memo:
        return memo[n]
    if n == 0:
        memo[n] = True
        return True
    loss = all(not subtraction_loss(n - take, memo) for take in (1, 2, 3) if take <= n)
    memo[n] = loss
    return loss


def two_pile_loss(a, b, memo):
    key = (a, b) if a <= b else (b, a)
    if key in memo:
        return memo[key]
    if a == 0 and b == 0:
        memo[key] = True
        return True
    loss = True
    for take in range(1, a + 1):
        if two_pile_loss(a - take, b, memo):
            loss = False
            break
    if loss:
        for take in range(1, b + 1):
            if two_pile_loss(a, b - take, memo):
                loss = False
                break
    memo[key] = loss
    return loss


def nim_loss(heaps, memo):
    key = tuple(sorted(heaps))
    if key in memo:
        return memo[key]
    if all(heap == 0 for heap in heaps):
        memo[key] = True
        return True
    loss = True
    for index, heap in enumerate(heaps):
        for left in range(heap):
            nxt = list(heaps)
            nxt[index] = left
            if nim_loss(nxt, memo):
                loss = False
                break
        if not loss:
            break
    memo[key] = loss
    return loss


def xor_move(heaps):
    total = 0
    for heap in heaps:
        total ^= heap
    moves = []
    if total == 0:
        return moves
    for index, heap in enumerate(heaps):
        target = heap ^ total
        if target < heap:
            nxt = list(heaps)
            nxt[index] = target
            moves.append(tuple(nxt))
    return moves


def bite(pos, i, j):
    return frozenset(cell for cell in pos if not (cell[0] >= i and cell[1] >= j))


def rectangle(rows, cols):
    return frozenset((r, c) for r in range(rows) for c in range(cols))


def ell(n):
    return frozenset({(r, 0) for r in range(n)} | {(0, c) for c in range(n)})


def chomp_win(pos, memo):
    if pos in memo:
        return memo[pos]
    win = False
    for i, j in pos:
        if (i, j) == (0, 0):
            continue
        if not chomp_win(bite(pos, i, j), memo):
            win = True
            break
    memo[pos] = win
    return win


def mirror_defends(n):
    def holds(pos):
        if pos == frozenset({(0, 0)}):
            return True
        for i, j in pos:
            if (i, j) == (0, 0):
                continue
            after = bite(pos, i, j)
            reply = (j, i)
            if reply not in after:
                return False
            if not holds(bite(after, reply[0], reply[1])):
                return False
        return True

    return holds(ell(n))


def solve_games():
    sub_memo = {}
    for n in range(51):
        assert subtraction_loss(n, sub_memo) == (n % 4 == 0)
        if n % 4:
            good = n % 4
            assert all(
                subtraction_loss(n - take, sub_memo) == (take == good)
                for take in (1, 2, 3) if take <= n
            )
    assert subtraction_loss(50, sub_memo) is False and 50 % 4 == 2

    pile_memo = {}
    for a in range(9):
        for b in range(9):
            assert two_pile_loss(a, b, pile_memo) == (a == b)
    assert two_pile_loss(5, 2, pile_memo) is False
    assert two_pile_loss(2, 2, pile_memo) is True
    assert two_pile_loss(1, 2, pile_memo) is False
    assert two_pile_loss(1, 1, pile_memo) is True

    nim_memo = {}
    for a in range(9):
        for b in range(9):
            for c in range(9):
                heaps = (a, b, c)
                assert nim_loss(heaps, nim_memo) == ((a ^ b ^ c) == 0)
                moves = xor_move(heaps)
                if a ^ b ^ c == 0:
                    assert moves == []
                else:
                    assert moves
                    assert all(x ^ y ^ z == 0 for x, y, z in moves)
                    assert all(nim_loss(move, nim_memo) for move in moves)
    assert (9 ^ 5 ^ 12) == 0
    assert xor_move((3, 4, 5)) == [(1, 4, 5)]
    assert (1 ^ 4 ^ 5) == 0

    memo = {}
    assert ttt_value((0,) * 9, 1, memo) == 0
    x_wins, o_wins, draws = count_games()
    assert (x_wins, o_wins, draws) == (131184, 77904, 46080)
    assert x_wins + o_wins + draws == 255168
    positions = reachable_positions()
    assert len(positions) == 5478
    lesson = choose_ttt(memo)
    board, (trap, reply), safe = lesson
    assert ttt_value(board, 1, memo) == 0
    trap_board = list(board)
    trap_board[trap] = 1
    answered = list(trap_board)
    answered[reply] = 2
    assert winner(tuple(answered)) == 2
    safe_board = list(board)
    safe_board[safe] = 1
    assert ttt_value(tuple(safe_board), 2, memo) == 0

    chomp_memo = {}
    assert chomp_win(rectangle(1, 1), chomp_memo) is False
    for n in (2, 3, 4):
        assert chomp_win(rectangle(n, n), chomp_memo) is True
        assert chomp_win(ell(n), chomp_memo) is False
        assert mirror_defends(n)
        assert bite(rectangle(n, n), 1, 1) == ell(n)
    corner = bite(rectangle(3, 3), 2, 2)
    assert chomp_win(corner, chomp_memo) is True
    assert bite(corner, 1, 1) == ell(3)
    winning_23 = []
    start_23 = rectangle(2, 3)
    for cell in sorted(start_23):
        if cell == (0, 0):
            continue
        if not chomp_win(bite(start_23, *cell), chomp_memo):
            winning_23.append(cell)
    assert winning_23 == [(1, 2)]

    tree = ("max", (("min", (5, 6)), ("min", (3, 7)), ("min", (4, 9))))
    assert minimax(tree, True) == 5
    seen = []
    assert alphabeta(tree, -10**9, 10**9, True, seen) == 5
    assert seen == [5, 6, 3, 4]
    worse = ("max", (("min", (5, 6)), ("min", (7, 3)), ("min", (4, 9))))
    seen_worse = []
    assert alphabeta(worse, -10**9, 10**9, True, seen_worse) == 5
    assert seen_worse == [5, 6, 7, 3, 4]

    pair = 30 * 30
    assert 10**2 < pair < 10**3
    assert 118.1 < 80 * math.log10(30) < 118.2
    assert 123.5 < 80 * math.log10(35) < 123.6
    assert 359.6 < 150 * math.log10(250) < 359.7
    year = 365.25 * 24 * 3600
    shannon_years = 10**120 * 10**(-6) / year
    assert 10**106 < shannon_years < 10**107
    position_log = (
        sum(math.log10(i) for i in range(1, 65))
        - sum(math.log10(i) for i in range(1, 33))
        - 2 * sum(math.log10(i) for i in range(1, 9))
        - 6 * math.log10(2)
    )
    assert 42 < position_log < 43
    legal_go = int(
        "208168199381979984699478633344862770286522453884530548425639456820927419612738015378525648451698519643907259916015628128546089888314427129715319317557736620397247064840935"
    )
    assert len(str(legal_go)) == 171
    assert math.isclose(legal_go / 10**170, 2.081681994, rel_tol=1e-9)
    assert 0.011 < legal_go / 3**361 < 0.013

    return {
        "lesson": lesson,
        "winning_23": winning_23,
        "shannon_years": shannon_years,
        "position_log": position_log,
        "positions": len(positions),
    }


def minimax(node, maximizing):
    if isinstance(node, int):
        return node
    _, children = node
    scores = [minimax(child, not maximizing) for child in children]
    return max(scores) if maximizing else min(scores)


def alphabeta(node, alpha, beta, maximizing, seen):
    if isinstance(node, int):
        seen.append(node)
        return node
    _, children = node
    if maximizing:
        value = -10**9
        for child in children:
            value = max(value, alphabeta(child, alpha, beta, False, seen))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    value = 10**9
    for child in children:
        value = min(value, alphabeta(child, alpha, beta, True, seen))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value


def candy_row():
    labels = []
    for n in range(9):
        if n % 4 == 0:
            labels.append((n, True, "无好手"))
        else:
            labels.append((n, False, f"拿{n % 4}"))
    xs = [28 + n * 76 for n in range(9)]
    frames = []
    for n in range(9):
        start = 100 * n / 9
        stop = 100 * (n + 0.78) / 9
        dx = xs[n] - xs[0]
        frames.append(f"{start:.2f}%{{opacity:1;transform:translateX({dx}px)}}")
        frames.append(f"{stop:.2f}%{{opacity:1;transform:translateX({dx}px)}}")
    frames.append(f"100%{{opacity:0;transform:translateX({xs[-1] - xs[0]}px)}}")
    elements = [
        text(36, 48, "从 0 颗往回标：谁赢已经写在格里", 32),
        text(36, 88, "实线格轮到的人必胜；虚线格必败。橙框只提示倒推次序。", 24, MUTED),
        (
            "<style>.walker{opacity:0;animation:walk 9s linear 1}"
            f"@keyframes walk{{{''.join(frames)}}}"
            "@media(prefers-reduced-motion:reduce){.walker{animation:none;opacity:0}}"
            "</style>"
        ),
    ]
    for n, (count, loss, action) in enumerate(labels):
        x = xs[n]
        elements += [
            (
                f'<rect x="{x}" y="132" width="68" height="160" rx="12" '
                f'fill="{LOSS_FILL if loss else WIN_FILL}" '
                f'stroke="{ORANGE if loss else BLUE}" stroke-width="2" '
                + ('stroke-dasharray="5 4"' if loss else "")
                + "/>"
            ),
            text(x + 34, 168, str(count), 28, INK, "middle"),
            text(x + 34, 206, "必败" if loss else "必胜", 22, ORANGE if loss else BLUE, "middle"),
            text(x + 34, 248, action, 16, MUTED, "middle"),
        ]
    elements.append(
        f'<rect class="walker" x="{xs[0]}" y="128" width="68" height="168" rx="12" '
        f'fill="none" stroke="{ORANGE}" stroke-width="5"/>'
    )
    elements += [
        text(36, 338, "倒推方向：先定 0，再看哪一步能把对方留在虚线格。", 24),
        (
            f'<path d="M48 362H668" fill="none" stroke="{BLUE}" stroke-width="3" '
            'marker-end="url(#arrow)"/>'
        ),
        (
            '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="8" refY="4" '
            f'orient="auto"><path d="M0 0L10 4L0 8Z" fill="{BLUE}"/></marker></defs>'
        ),
        text(36, 408, "0、4、8 必败。核到 50：50＝4×12＋2，只能拿 2。", 24),
        text(36, 448, "拿错数量会离开这个节拍，对方就能把你留回虚线格。", 24, MUTED),
    ]
    return document(
        490,
        "单堆拿糖从零颗倒推到八颗",
        "零到八颗糖，每次可拿一到三颗，拿走最后一颗的人获胜。"
        "零、四、八是轮到的人必败；其余格唯一的必胜拿法是拿到四的倍数。"
        "高亮框从零走到八，播放一次后消失。减少动态效果时不显示高亮，格子与文字保持完整。",
        elements,
    )


def two_piles():
    elements = [
        text(36, 48, "两堆一样多，轮到的人必败", 32),
        text(36, 88, "行是乙堆，列是甲堆。格里先写甲，再写乙。", 24, MUTED),
    ]
    origin_x, origin_y, size = 168, 148, 78
    for a in range(6):
        elements.append(text(origin_x + a * size + size / 2, 136, str(a), 22, MUTED, "middle"))
        elements.append(text(148, origin_y + a * size + 46, str(a), 22, MUTED, "middle"))
        for b in range(6):
            loss = a == b
            x = origin_x + a * size
            y = origin_y + b * size
            elements += [
                (
                    f'<rect x="{x + 4}" y="{y + 4}" width="70" height="70" rx="8" '
                    f'fill="{LOSS_FILL if loss else WIN_FILL}" '
                    f'stroke="{ORANGE if loss else BLUE}" stroke-width="2" '
                    + ('stroke-dasharray="5 4"' if loss else "")
                    + "/>"
                ),
                text(x + 39, y + 34, f"{a},{b}", 18, MUTED, "middle"),
                text(x + 39, y + 60, "必败" if loss else "必胜", 20, ORANGE if loss else BLUE, "middle"),
            ]
    elements += [
        text(36, 118, "甲", 22, BLUE),
        text(36, 390, "乙", 22, ORANGE),
        panel(24, 650, 672, 188),
        text(44, 692, "例：甲 5、乙 2。先手从甲堆拿 3，留下 2 与 2。", 26),
        text(44, 736, "后手若从甲堆拿 1，变成 1 与 2。", 26),
        text(44, 780, "先手再从乙堆拿 1，回到 1 与 1。", 26, BLUE),
        text(44, 818, "后手每次打破相等，先手就把它补回。", 24, MUTED),
    ]
    return document(
        870,
        "两堆拿糖的胜负网格",
        "甲堆和乙堆各从零到五。每次只能在同一堆拿走至少一颗。"
        "两堆数量相同的六格是轮到的人必败，其余由倒推得到必胜。"
        "下方例子从五比二拿到二比二，再从一比二补回一比一。",
        elements,
    )


def three_piles():
    rows = ((9, (1, 0, 0, 1)), (5, (0, 1, 0, 1)), (12, (1, 1, 0, 0)))
    next_rows = ((1, (0, 0, 1)), (4, (1, 0, 0)), (5, (1, 0, 1)))
    elements = [
        text(36, 48, "三堆不再能靠左右模仿", 32),
        text(36, 88, "把颗数写成二进制，竖着加，不进位。", 24, MUTED),
        panel(24, 112, 672, 300),
        text(44, 156, "① 9、5、12：每一竖列都是偶数", 28),
    ]
    elements += bit_table(70, 186, rows, ("8", "4", "2", "1"), True)
    elements += [
        panel(24, 432, 672, 360),
        text(44, 476, "② 3、4、5：有一列是奇数，必胜", 28),
        text(44, 514, "唯一能改回全偶的走法：把 3 拿成 1。", 24, BLUE),
    ]
    elements += bit_table(70, 540, ((3, (0, 1, 1)), (4, (1, 0, 0)), (5, (1, 0, 1))), ("4", "2", "1"), False)
    elements += bit_table(390, 540, next_rows, ("4", "2", "1"), True)
    elements += [
        text(70, 760, "改之前", 22, ORANGE),
        text(390, 760, "改成 1、4、5", 22, BLUE),
    ]
    return document(
        830,
        "三堆糖的二进制不进位加法",
        "九、五、十二写成二进制后，每一竖列的一的个数都是偶数，是必败组合。"
        "三、四、五有一列是奇数。把三改成一后，一、四、五的每一列重新变成偶数。"
        "在所有合法拿法中，这一步是唯一走到偶数组合的走法。",
        elements,
    )


def bit_table(x, y, rows, headers, even):
    elements = []
    columns = [x + 86 + index * 42 for index in range(len(headers))]
    for index, header in enumerate(headers):
        elements.append(text(columns[index], y, header, 20, MUTED, "middle"))
    for index, (count, bits) in enumerate(rows):
        yy = y + 44 + index * 40
        elements.append(text(x, yy, str(count), 24, INK))
        for bit_index, bit in enumerate(bits):
            elements.append(text(columns[bit_index], yy, str(bit), 24, INK, "middle"))
    label = "每一列都是偶数：必败" if even else "2 那一列是奇数：必胜"
    color = ORANGE if even else BLUE
    elements.append(text(x, y + 44 + len(rows) * 40 + 16, label, 22, color))
    return elements


def tic_tac_toe(lesson):
    board, (trap, reply), safe = lesson
    assert board == (0, 0, 0, 1, 2, 2, 2, 1, 1)
    assert (trap, reply, safe) == (0, 2, 2)
    trap_board = list(board)
    trap_board[trap] = 1
    answered = list(trap_board)
    answered[reply] = 2
    safe_board = list(board)
    safe_board[safe] = 1

    def draw(board_state, x, y, highlight):
        size = 62
        parts = []
        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                px = x + col * size
                py = y + row * size
                fill = "#fff7ea" if index in highlight else "#fff"
                stroke = ORANGE if index in highlight else BLUE
                parts.append(
                    f'<rect x="{px}" y="{py}" width="56" height="56" rx="8" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
                )
                mark = {0: "", 1: "×", 2: "○"}[board_state[index]]
                if mark:
                    parts.append(text(px + 28, py + 40, mark, 32, INK, "middle"))
        return parts

    elements = [
        text(36, 48, "同一盘棋：一步送掉，一步守和", 32),
        text(36, 88, "× 先手，○ 后手。中盘两枚橙格有先后。", 24, MUTED),
        panel(24, 120, 210, 360),
        panel(254, 120, 210, 360),
        panel(484, 120, 212, 360),
        text(129, 158, "现在", 26, INK, "middle"),
        text(359, 158, "陷阱", 26, ORANGE, "middle"),
        text(590, 158, "守和", 26, BLUE, "middle"),
    ]
    elements += draw(board, 48, 184, set())
    elements += draw(answered, 278, 184, {trap, reply})
    elements += draw(tuple(safe_board), 508, 184, {safe})
    elements += [
        text(129, 400, "轮到 ×", 22, MUTED, "middle"),
        text(129, 434, "整盘值：和", 22, BLUE, "middle"),
        text(359, 400, "叉先下左上", 20, ORANGE, "middle"),
        text(359, 434, "圈再下右上即胜", 20, ORANGE, "middle"),
        text(590, 400, "三个空位里", 20, BLUE, "middle"),
        text(590, 434, "只有右上能守和", 20, BLUE, "middle"),
        text(36, 528, "正中空位也会输，只是圈不能马上连成，图里没有展开。", 24),
        text(36, 570, "右盘之后仍是和棋。空棋盘用同一套搜索，结果也是和棋。", 24, MUTED),
    ]
    return document(
        620,
        "井字棋里一步陷阱和一步守和",
        "三盘井字棋。左盘轮到画叉，完整搜索的值是和棋。"
        "中盘里叉先占左上，圈立刻占右上，沿对角线连成三子。"
        "右盘改占右上，是三个空位里唯一仍为和棋的选择；上边中间那格也会输，图中没有展开。",
        elements,
    )


def chocolate():
    def squares(origin_x, origin_y, removed):
        parts = []
        for row in range(2, -1, -1):
            for col in range(3):
                x = origin_x + col * 46
                y = origin_y + (2 - row) * 46
                if (row, col) in removed:
                    parts.append(
                        f'<rect x="{x}" y="{y}" width="42" height="42" rx="6" '
                        'fill="#eef3f6" stroke="#9aabb8" stroke-width="2" stroke-dasharray="4 4"/>'
                    )
                    continue
                poison = (row, col) == (0, 0)
                parts.append(
                    f'<rect x="{x}" y="{y}" width="42" height="42" rx="6" '
                    f'fill="{"#6e4a3a" if poison else "#e1b07a"}" stroke="#8a5a2b" stroke-width="2"/>'
                )
                if poison:
                    parts.append(text(x + 21, y + 29, "毒", 20, "#fff", "middle"))
        return parts

    gone_corner = {(2, 2)}
    gone_ell = {(1, 1), (2, 1), (1, 2), (2, 2)}
    gone_reply = gone_ell | {(2, 0), (0, 2)}
    elements = [
        text(36, 48, "3×3：试探的一口，不是该下的一口", 32),
        text(36, 88, "毒在左下。咬掉一格及其右上。虚线＝已吃掉。", 24, MUTED),
        panel(24, 112, 672, 250),
        text(44, 150, "① 只吃右上角", 26),
        text(44, 188, "对方再吃中心", 26),
        text(44, 226, "剩下的 L 轮到你", 26, ORANGE),
        text(44, 270, "这一口会输。", 26, ORANGE),
        text(44, 312, "开局时你就能直接吃成右边这样。", 22, MUTED),
        panel(24, 382, 672, 250),
        text(44, 420, "② 第一口就留下 L", 26, BLUE),
        text(44, 458, "对方吃底边右端", 26),
        text(44, 496, "你吃左边上端", 26, BLUE),
        text(44, 540, "两臂恢复一样长。", 26, BLUE),
        text(44, 584, "吃哪一臂，就咬另一臂。", 22, MUTED),
    ]
    elements += squares(400, 140, gone_corner)
    elements += squares(560, 140, gone_ell)
    elements += squares(400, 410, gone_ell)
    elements += squares(560, 410, gone_reply)
    elements += [
        text(467, 318, "吃完右上角", 20, MUTED, "middle"),
        text(627, 318, "变成 L", 20, ORANGE, "middle"),
        text(467, 588, "你留下的 L", 20, BLUE, "middle"),
        text(627, 588, "补回对称", 20, BLUE, "middle"),
        text(36, 670, "存在性证明只说第一口存在，不指出是哪一口。", 24),
        text(36, 708, "3×3 的第一口是吃掉中心及其右上。2×3 却是只吃右上角。", 24, MUTED),
    ]
    return document(
        750,
        "三乘三有毒巧克力的试探与镜像",
        "毒块在左下角。只吃掉右上角后，对方可以吃掉中心及其右上方，留下 L，使先手落入必败。"
        "先手应自己先吃成这个 L。对方再吃底边右端时，先手吃掉左边上端，两臂恢复等长。"
        "虚线格表示已经吃掉。二乘三的唯一必胜第一口是只吃右上角；在三乘三上，这一口会输。",
        elements,
    )


def alpha_beta():
    def box(cx, cy, width, height, line1, line2, fill, stroke, dashed=False):
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        return [
            (
                f'<rect x="{cx - width / 2}" y="{cy - height / 2}" width="{width}" height="{height}" '
                f'rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>'
            ),
            text(cx, cy - 8, line1, 20, INK, "middle"),
            text(cx, cy + 20, line2, 18, INK, "middle"),
        ]

    def edge(x1, y1, x2, y2, pruned=False):
        color = "#9aabb8" if pruned else BLUE
        dash = ' stroke-dasharray="6 4"' if pruned else ""
        return (
            f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" '
            f'stroke-width="2"{dash}/>'
        )

    elements = [
        text(36, 48, "分数已经够用，旁边的树枝可以不看", 32),
        text(36, 88, "先手要高分，后手要低分。灰虚线是这一次序下没读的叶子。", 23, MUTED),
    ]
    root = (360, 168)
    mins = ((140, 318), (360, 318), (580, 318))
    leaves = (
        ((100, 500, "5", "①"), (180, 500, "6", "②")),
        ((320, 500, "3", "③"), (420, 500, "7", "不看")),
        ((540, 500, "4", "④"), (660, 500, "9", "不看")),
    )
    for (cx, cy), pairs in zip(mins, leaves):
        elements.append(edge(root[0], root[1] + 32, cx, cy - 32))
        for lx, ly, _, tag in pairs:
            elements.append(edge(cx, cy + 32, lx, ly - 28, pruned=(tag == "不看")))
    elements += box(*root, 150, 64, "先手", "结果：5", WIN_FILL, BLUE)
    for (cx, cy), caption in zip(mins, ("会选 5", "最多 3", "最多 4")):
        elements += box(cx, cy, 120, 64, "后手", caption, "#fff", BLUE)
    for pairs in leaves:
        for lx, ly, value, tag in pairs:
            pruned = tag == "不看"
            elements += box(
                lx, ly, 72, 56, value, tag,
                "#eef3f6" if pruned else WIN_FILL,
                "#9aabb8" if pruned else BLUE,
                dashed=pruned,
            )
    elements += [
        text(36, 580, "① 左支看完，先手已经能保证 5。", 24),
        text(36, 618, "② 中支一看到 3，就比 5 差，7 不必再读。", 24),
        text(36, 656, "③ 右支一看到 4，同样不超过 5，9 不必再读。", 24),
        text(36, 704, "若中支改成先看 7，7 会被读到；根上的结果仍是 5。", 24, BLUE),
        text(36, 748, "灰格上的 7 和 9 是为了核对才写上的，搜索本身没有读取。", 22, MUTED),
    ]
    return document(
        800,
        "一个六片叶子的极小化极大剪枝",
        "先手选择三支后手局面。按左、中、右的次序，搜索读到五、六、三、四，"
        "在看到三和四之后分别停住，不读七和九。根的分数是五。"
        "把中支改成先看七，会多读一片叶子，根仍是五。叶子是估分，不是终局胜负。",
        elements,
    )


def main():
    report = solve_games()
    board, (trap, reply), safe = report["lesson"]
    OUT.mkdir(parents=True, exist_ok=True)
    pictures = (
        ("candy-row", candy_row()),
        ("two-piles", two_piles()),
        ("three-piles", three_piles()),
        ("tic-tac-toe", tic_tac_toe(report["lesson"])),
        ("chocolate", chocolate()),
        ("alpha-beta", alpha_beta()),
    )
    for name, content in pictures:
        ET.fromstring(content)
        root = ET.fromstring(content)
        assert root.get("width") == "720"
        assert root.get("viewBox") == f'0 0 720 {root.get("height")}'
        assert root.find("{http://www.w3.org/2000/svg}title") is not None or root.find("title") is not None
        (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
        print(f"Wrote {name}.svg")
    print("ttt", "".join("X" if cell == 1 else "O" if cell == 2 else "." for cell in board))
    print("trap", trap, "reply", reply, "safe", safe)
    print("positions", report["positions"])
    print("shannon_years", report["shannon_years"])
    print("position_log", report["position_log"])
    print("winning_23", report["winning_23"])


if __name__ == "__main__":
    main()
