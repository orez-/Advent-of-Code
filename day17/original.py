def neighbors(x, y, z):
    r = (-1, 0, 1)
    for dx in r:
        for dy in r:
            for dz in r:
                if not (dx == dy == dz == 0):
                    yield (x +dx, y+dy, z+dz)


def neighbors4(x, y, z, w):
    r = (-1, 0, 1)
    for dx in r:
        for dy in r:
            for dz in r:
                for dw in r:
                    if not (dx == dy == dz == dw == 0):
                        yield (x +dx, y+dy, z+dz, w+dw)


def part1(file):
    board = {
        (x, y, 0): elem == '#'
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
    }

    for _ in range(6):
        coords = set(
            c
            for x, y, z in board
            for c in neighbors(x, y, z)
        )
        new_board = {}
        for x, y, z in coords:
            elem = board.get((x, y, z), False)
            neighbor_count = sum(1 for c in neighbors(x, y, z) if board.get(c))
            if elem and neighbor_count not in (2, 3):
                elem = False
            elif not elem and neighbor_count == 3:
                elem = True
            new_board[x,y,z] = elem
        board = new_board
    return sum(board.values())


def part2(file):
    board = {
        (x, y, 0, 0): elem == '#'
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
    }

    for _ in range(6):
        coords = set(
            c
            for x, y, z, w in board
            for c in neighbors4(x, y, z, w)
        )
        new_board = {}
        for x, y, z, w in coords:
            elem = board.get((x, y, z, w), False)
            neighbor_count = sum(1 for c in neighbors4(x, y, z, w) if board.get(c))
            if elem and neighbor_count not in (2, 3):
                elem = False
            elif not elem and neighbor_count == 3:
                elem = True
            new_board[x,y,z,w] = elem
        board = new_board
    return sum(board.values())


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
