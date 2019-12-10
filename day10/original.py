import collections
import itertools
import math


def seen_asteroids(file, x, y):
    slopes = {
        math.atan2(y - ay, x - ax)
        for ay, row in enumerate(file)
        for ax, elem in enumerate(row)
        if elem == "#" and (ay, ax) != (y, x)
    }
    return len(slopes)


def part1(file):
    best = 0
    for y, row in enumerate(file):
        for x, elem in enumerate(row):
            cur = 0
            if elem == ".":
                continue
            cur = seen_asteroids(file, x, y)
            best = max(cur, best)
    return best


def print_em(board, x, y):
    af = '\x1b[38;5;{}m'.format
    c = []
    for cy, row in enumerate(board):
        for cx, elem in enumerate(row):
            if cx == x and cy == y:
                c.append(af(5))
                c.append(elem)
                c.append('\x1b[0m')
            else:
                c.append(elem)
        c.append("\n")
    print("".join(c))


def part2(file):
    killmap = list(map(list, file))

    best = 0
    p = None
    for y, row in enumerate(file):
        for x, elem in enumerate(row):
            cur = 0
            if elem == ".":
                continue
            cur = seen_asteroids(file, x, y)
            if cur > best:
                best = cur
                p = y, x
    y, x = p

    foo = collections.defaultdict(list)
    for ay, row in enumerate(file):
        for ax, elem in enumerate(row):
            if elem == "#" and (ay, ax) != (y, x):
                foo[math.atan2(x - ax, ay - y)].append((abs(ay - y + ax - x), ay, ax))
    for v in foo.values():
        v.sort()

    # jesus.
    if math.pi in foo:
        foo[-math.pi] = foo[math.pi]
        del foo[math.pi]
    poss = itertools.cycle(sorted(foo.items()))
    # print_em(killmap, x, y)
    for _ in range(200):
        find = None
        while not find:
            _, shot = next(poss)
            if shot:
                find = shot.pop(0)
        _, ky, kx = find
        killmap[ky][kx] = "."
        # print_em(killmap, x, y)
    _, y, x = find
    return x * 100 + y


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
