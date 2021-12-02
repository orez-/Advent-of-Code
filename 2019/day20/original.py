import collections


def get_label(file, x, y):
    label_pos = None
    other_chr = None
    width = range(max(map(len, file)))
    height = range(len(file))
    for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        nx = x + dx
        ny = y + dy
        if ny in height and nx in range(len(file[ny])):
            if file[ny][nx] == ".":
                label_pos = (nx, ny)
            elif file[ny][nx] not in "#. ":
                other_chr = file[ny][nx]
    if label_pos:
        assert other_chr, (x, y)
        return frozenset(file[y][x] + other_chr), label_pos
    return None


def search1(start, goal, board):
    queue = collections.deque([(*start, 0)])
    seen = set()

    while queue:
        x, y, steps = queue.popleft()
        if (x, y) == goal:
            return steps

        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            nx = x + dx
            ny = y + dy

            if (nx, ny) in seen or not board.get((nx, ny)):
                continue

            seen.add((nx, ny))
            queue.append((nx, ny, steps + 1))

        if isinstance(board.get((x, y)), tuple):
            nx, ny = board[x, y]
            if (nx, ny) not in seen:
                queue.append((nx, ny, steps + 1))


def search2(start, goal, board):
    # print("goin from", start, "to", goal)
    queue = collections.deque([(*start, 0, 0)])
    seen = {(*start, 0)}
    best = {}

    path = {}

    while queue:
        x, y, steps, depth = queue.popleft()
        # print(x, y, steps, depth)
        if (x, y) == goal and depth == 0:
            my_path = [(x, y, depth)]
            while (x, y, depth) in path:
                x, y, depth = path[x, y, depth]
                my_path.append((x, y, depth))
            return steps, my_path

        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            nx = x + dx
            ny = y + dy

            # if (nx, ny) in best and best[nx, ny] < depth:
            #     print("skipping", (nx, ny), ", i was here at depth", best[nx, ny], "(currently", depth, ")")
            #     continue
            if (nx, ny, depth) in seen or not board.get((nx, ny)):
                continue

            # if depth != 0:
            #     best[nx, ny] = depth
            seen.add((nx, ny, depth))
            queue.append((nx, ny, steps + 1, depth))
            path[nx, ny, depth] = (x, y, depth)

        if isinstance(board.get((x, y)), tuple):
            nx, ny, dd = board[x, y]
            ndepth = depth + dd
            if ndepth < 0:
                continue
            # if (nx, ny) in best and best[nx, ny] < ndepth:
            #     print("skipping", (nx, ny), ", i was here at depth", best[nx, ny], "(currently", ndepth, ")")
            #     continue
            if (nx, ny, ndepth) not in seen:
                # print("!", nx, ny, depth, dd)
                # if ndepth != 0:
                #     best[nx, ny] = ndepth
                seen.add((nx, ny, ndepth))
                # print(dd, ndepth)
                queue.append((nx, ny, steps + 1, ndepth))
                path[nx, ny, ndepth] = (x, y, depth)
    raise Exception("shit")


def print_board(file, coord):
    ab = '\x1b[48;5;{}m'.format
    clear = '\x1b[0m'
    display = "\n".join(
        ''.join(
            (f"{ab(2)}@{clear}" if (x, y) == coord else elem)
            for x, elem in enumerate(row)
        )
        for y, row in enumerate(file)
    )
    print(display)


def part1(file):
    board = {}
    labels = collections.defaultdict(set)
    for y, row in enumerate(file):
        for x, elem in enumerate(row):
            if elem in "#.":
                board[x, y] = elem == "."
            elif elem == " ":
                continue
            else:
                # print(elem)
                label = get_label(file, x, y)
                if label:
                    label, pos = label
                    labels[label].add(pos)
                board[x, y] = False

    for label, value in labels.items():
        if len(value) == 2:
            (pos1, pos2) = value
            board[pos1] = pos2
            board[pos2] = pos1

    return search1(labels[frozenset("A")].pop(), labels[frozenset("Z")].pop(), board)


def part2(file):
    INNER = range(30, 100)
    board = {}
    labels = collections.defaultdict(set)
    for y, row in enumerate(file):
        for x, elem in enumerate(row):
            if elem in "#.":
                board[x, y] = elem == "."
            elif elem == " ":
                continue
            else:
                label = get_label(file, x, y)
                if label:
                    label, pos = label
                    labels[label].add(pos)
                board[x, y] = False

    for label, value in labels.items():
        if len(value) == 2:
            (x1, y1), (x2, y2) = value
            r2, r1 = (-1, 1) if x1 in INNER and y1 in INNER else (1, -1)
            board[x1, y1] = (x2, y2, r1)
            board[x2, y2] = (x1, y1, r2)

    steps, path = search2(labels[frozenset("A")].pop(), labels[frozenset("Z")].pop(), board)
    # for x, y, depth in path:
    #     print(depth)
    #     print_board(file, (x, y))
        # input()
    return steps


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
