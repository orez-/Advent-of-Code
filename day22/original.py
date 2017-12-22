import collections


file = """
#..#...##.#.###.#.#.#...#
.####....#..##.#.##....##
...#..#.#.#......##..#..#
##.####.#.##........#...#
##.#....##..#.####.###...
#..#..###...#.#..##..###.
.##.##..#.####.#.#.....##
#....#......######...#...
..#.#.##.#..#...##.#.####
#.#..#.....#..####.#.#.##
...##.#..##.###.###......
###..#.####.#..#####..#..
...##.##.#.###.#..##.#.##
.####.#.##.#####.##.##..#
#.##.#...##.#.###.###..#.
..#.#..#..#..##..###...##
##.##.#..#.###....###..##
.#...###..#####.#..#.#.##
....##..####.##...#..#.##
#..#..###..#..###...#..##
.##.#.###..####.#.#..##.#
..###.#....#...###...##.#
.#...##.##.####...##.####
###.#.#.####.##.###..#...
#.#######.#######..##.#.#
""".strip().split('\n')


def part1(file):
    dx = 0
    dy = -1
    nodes = collections.defaultdict(bool, {
        (x, y): elem == '#'
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
    })
    x = len(file[0]) // 2
    y = len(file) // 2

    b = 0

    for _ in range(10000):
        node = nodes[x, y]

        if node:
            dx, dy = -dy, dx
        else:
            b += 1
            dx, dy = dy, -dx

        nodes[x, y] = not node
        x += dx
        y += dy

    return b


def part2(file):
    dx = 0
    dy = -1
    nodes = collections.defaultdict(int, {
        (x, y): int(elem == '#') * 2
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
    })
    x = len(file[0]) // 2
    y = len(file) // 2

    b = 0

    for _ in range(10000000):
        node = nodes[x, y]

        if node == 0:
            dx, dy = dy, -dx  # left
        elif node == 1:
            b += 1
        elif node == 2:
            dx, dy = -dy, dx  # right
        elif node == 3:
            dx, dy = -dx, -dy


        nodes[x, y] = (node + 1) % 4
        x += dx
        y += dy

    return b


print(part1(file))
print(part2(file))  # ~4 seconds w/ pypy, ~9 cpython
