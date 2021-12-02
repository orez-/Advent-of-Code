import collections
import itertools
import math
import time


def seen_asteroids(file, x, y):
    slopes = {
        math.atan2(y - ay, x - ax)
        for ay, row in enumerate(file)
        for ax, elem in enumerate(row)
        if elem == "#" and (ay, ax) != (y, x)
    }
    return len(slopes)


def print_em(board, x, y, kx=None, ky=None):
    af = '\x1b[38;5;{}m'.format
    clear = '\x1b[0m'
    c = []
    for cy, row in enumerate(board):
        for cx, elem in enumerate(row):
            if cx == x and cy == y:
                c.append(af(2))
                c.append(elem)
                c.append(clear)
            elif kx == cx and ky == cy:
                c.append(af(1))
                c.append("*")
                c.append(clear)
            else:
                c.append(elem)
        c.append("\n")
    print("".join(c))
    time.sleep(0.05)


def find_busiest(file):
    _, y, x = max(
        (seen_asteroids(file, x, y), y, x)
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
        if elem == "#"
    )
    return y, x


def visualize(file):
    killmap = list(map(list, file))

    y, x = find_busiest(file)

    angles = collections.defaultdict(list)
    for ay, row in enumerate(file):
        for ax, elem in enumerate(row):
            if elem == "#" and (ay, ax) != (y, x):
                angles[math.atan2(x - ax, ay - y)].append((abs(ay - y + ax - x), ay, ax))
    for v in angles.values():
        v.sort()

    # jesus.
    if math.pi in angles:
        angles[-math.pi] = angles[math.pi]
        del angles[math.pi]
    poss = itertools.cycle(sorted(angles.items()))
    print_em(killmap, x, y)
    for _ in range("".join(file).count("#") - 1):
        find = None
        while not find:
            _, shot = next(poss)
            if shot:
                find = shot.pop(0)
        _, ky, kx = find
        killmap[ky][kx] = "."
        print_em(killmap, x, y, kx, ky)
    print_em(killmap, x, y)


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    visualize(list(file))
