import collections


file = """
#.#.# => #
..#.# => .
.#.## => #
.##.. => .
##... => #
##..# => #
#.##. => #
.#..# => #
.#### => .
....# => .
#.... => .
#.### => .
###.# => #
.#.#. => .
#...# => .
.#... => #
##.#. => #
#..## => #
..##. => .
####. => #
.###. => .
##### => .
#.#.. => .
...#. => .
..#.. => .
###.. => #
#..#. => .
.##.# => .
..... => .
##.## => #
..### => #
...## => #
""".strip().split('\n')


def part1(file):
    leftmost = 0
    start = tuple("##.#...#.#.#....###.#.#....##.#...##.##.###..#.##.###..####.#..##..#.##..#.......####.#.#..#....##.#")
    trans = dict(
        line.split(' => ')
        for line in file
    )
    trans = {tuple(key): value for key, value in trans.items()}
    for j in range(20):
        next_go = collections.deque()
        if trans[tuple('...') + start[0:2]] == '#':
            next_go.append('#')
            leftmost -= 1
        next_go.append(trans[tuple('..') + start[0:3]])
        next_go.append(trans[tuple('.') + start[0:4]])
        for i, c in enumerate(start):
            slc = start[i:i+5]
            while len(slc) < 5:
                slc += ('.',)
            next_go.append(trans[slc])
        while next_go[-1] == '.':
            next_go.pop()
        while next_go[0] == '.':
            next_go.popleft()
            leftmost += 1
        start = tuple(next_go)
    return sum(
        i for i, c in enumerate(start, leftmost)
        if c == '#'
    )


def part2(file):
    # Watching the output for a while, the pattern converges!
    start = '#..#..#..#..#..#..#....#..#....#....#..#....#..#..#..#..#..#..#....#....#..#..#..#..#..#....#..#..#....#..#....#..#....#..#..#..#..#..#..#..#..#..#..#..#....#..#..#..#....#'
    leftmost = 50000000000 - 72
    return sum(
        i for i, c in enumerate(start, leftmost)
        if c == '#'
    )


print(part1(list(file)))
print(part2(list(file)))
