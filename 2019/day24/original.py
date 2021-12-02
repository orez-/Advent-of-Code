def part1(file):
    board = {
        (x, y): elem == "#"
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
    }
    seen = {frozenset(board.items())}
    while True:
        new_board = dict(board)
        for (x, y), elem in board.items():
            total = 0
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx = x + dx
                ny = y + dy
                total += board.get((nx, ny), 0)
            if elem == 1:
                if total != 1:
                    new_board[x, y] = 0
            else:
                if total in (1, 2):
                    new_board[x, y] = 1
        hash_ = frozenset(new_board.items())
        if hash_ in seen:
            width = 5
            height = 5
            total = 0
            power = 1
            for y in range(width):
                for x in range(height):
                    total += new_board[x, y] * power
                    power <<= 1
            return total
        seen.add(hash_)
        board = new_board


def surrounding(x, y, d):
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nx = x + dx
        ny = y + dy
        if nx < 0:
            yield 1, 2, d + 1
        elif ny < 0:
            yield 2, 1, d + 1
        elif nx > 4:
            yield 3, 2, d + 1
        elif ny > 4:
            yield 2, 3, d + 1
        elif (nx, ny) == (2, 2):
            if dx:
                small_x = 0 if dx == 1 else 4
                for sy in range(5):
                    yield small_x, sy, d - 1
            else:
                small_y = 0 if dy == 1 else 4
                for sx in range(5):
                    yield sx, small_y, d - 1
        else:
            yield nx, ny, d


def part2(file):
    board = {
        (x, y): elem == "#"
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
    }
    board = {(x, y, 0): v for (x, y), v in board.items()}
    del board[2, 2, 0]

    for _ in range(200):
        to_check = {
            (sx, sy, sd)
            for x, y, d in board
            for sx, sy, sd in surrounding(x, y, d)
        }
        new_board = dict(board)
        for x, y, d in to_check:
            total = 0
            for coord in surrounding(x, y, d):
                total += board.get(coord, 0)
            if board.get((x, y, d), 0) == 1:
                if total != 1:
                    new_board[x, y, d] = 0
            else:
                if total in (1, 2):
                    new_board[x, y, d] = 1
        board = new_board
    return sum(1 for bug in board.values() if bug)


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
