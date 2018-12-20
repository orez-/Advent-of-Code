import collections

# ^>v<
up = 1
right = 2
down = 4
left = 8

Frame = collections.namedtuple('Frame', 'ends, on_pop')

lookup = {
    0: ' ',
    1: '│',
    2: '─',
    3: '└',
    4: '│',
    5: '│',
    6: '┌',
    7: '├',
    8: '─',
    9: '┘',
    10: '─',
    11: '┴',
    12: '┐',
    13: '┤',
    14: '┬',
    15: '┼',
}


def print_board(board):
    if not board:
        return
    ymin = min(y for y, x in board)
    ymax = max(y for y, x in board)
    xmin = min(x for y, x in board)
    xmax = max(x for y, x in board)

    joiner = collections.deque()
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            joiner.append(lookup[board.get((y, x), 0)])
        joiner.append('\n')
    print(''.join(joiner))


def get_board(file):
    # y, x
    board = collections.defaultdict(int)
    all_ends = {(0, 0)}
    stack = collections.deque([Frame(all_ends, set())])
    for i, c in enumerate(file):
        if c == '(':
            stack.append(Frame(set(all_ends), set()))
        elif c == '|':
            # Need to keep working from the top of the stack,
            # but need to track the branch we're on when we pop this.
            stack[-1].on_pop.update(all_ends)
            all_ends = stack[-1].ends
        elif c == ')':
            # Track the branch we're on, but pop the stack
            all_ends.update(stack[-1].on_pop)
            stack.pop()
        elif c == 'N':
            for y, x in all_ends:
                board[y, x] |= up
                board[y - 1, x] |= down
            all_ends = {(y - 1, x) for y, x in all_ends}
        elif c == 'S':
            for y, x in all_ends:
                board[y, x] |= down
                board[y + 1, x] |= up
            all_ends = {(y + 1, x) for y, x in all_ends}
        elif c == 'E':
            for y, x in all_ends:
                board[y, x] |= right
                board[y, x + 1] |= left
            all_ends = {(y, x + 1) for y, x in all_ends}
        elif c == 'W':
            for y, x in all_ends:
                board[y, x] |= left
                board[y, x - 1] |= right
            all_ends = {(y, x - 1) for y, x in all_ends}
        elif c not in '^$':
            print("?", c)
    return board


def part1(board):
    start = (0, 0)
    queue = collections.deque([(start, 0)])
    seen = {start}

    maxdist = 0

    while queue:
        (y, x), distance = queue.popleft()
        maxdist = max(maxdist, distance)
        room = board[y, x]

        for d, dy, dx in [(up, -1, 0), (right, 0, 1), (down, 1, 0), (left, 0, -1)]:
            if room | d != room:
                continue

            pos = (y + dy, x + dx)
            if pos in seen:
                continue
            queue.append((pos, distance + 1))
            seen.add(pos)
    return maxdist


def part2(file):
    num = 0
    start = (0, 0)
    queue = collections.deque([(start, 0)])
    seen = {start}

    while queue:
        (y, x), distance = queue.popleft()
        if distance >= 1000:
            num += 1
        room = board[y, x]

        for d, dy, dx in [(up, -1, 0), (right, 0, 1), (down, 1, 0), (left, 0, -1)]:
            if room | d != room:
                continue

            pos = (y + dy, x + dx)
            if pos in seen:
                continue
            queue.append((pos, distance + 1))
            seen.add(pos)
    return num


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().strip('^$')
    board = get_board(file)
    # print_board(board)
    print(part1(board))
    print(part2(board))
