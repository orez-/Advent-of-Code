import collections
import heapq
import re


Bot = collections.namedtuple('Bot', 'x y z r')
Point = collections.namedtuple('Point', 'x y z')


def get_numbers(line):
    return (int(match.group(0)) for match in re.finditer(r"-?(\d*\.\d+|\d+)", line))


def dist(pt1, pt2):
    """
    Gets the 3d Manhattan Distance (Fifth Element style?) between two points.
    """
    return abs(pt1.x - pt2.x) + abs(pt1.y - pt2.y) + abs(pt1.z - pt2.z)


def halfway(minc, maxc):
    return (maxc - minc) // 2 + minc


def subdivide_range(minr, maxr):
    if maxr.x - minr.x <= 1:
        return
    hx = halfway(minr.x, maxr.x)
    hy = halfway(minr.y, maxr.y)
    hz = halfway(minr.z, maxr.z)
    yield (Point(minr.x, minr.y, minr.z), Point(hx, hy, hz))
    yield (Point(hx + 1, minr.y, minr.z), Point(maxr.x, hy, hz))
    yield (Point(minr.x, hy + 1, minr.z), Point(hx, maxr.y, hz))
    yield (Point(hx + 1, hy + 1, minr.z), Point(maxr.x, maxr.y, hz))
    yield (Point(minr.x, minr.y, hz + 1), Point(hx, hy, maxr.z))
    yield (Point(hx + 1, minr.y, hz + 1), Point(maxr.x, hy, maxr.z))
    yield (Point(minr.x, hy + 1, hz + 1), Point(hx, maxr.y, maxr.z))
    yield (Point(hx + 1, hy + 1, hz + 1), Point(maxr.x, maxr.y, maxr.z))


def range_corners(minr, maxr):
    yield minr
    yield Point(minr.x, minr.y, maxr.z)
    yield Point(minr.x, maxr.y, minr.z)
    yield Point(minr.x, maxr.y, maxr.z)
    yield Point(maxr.x, minr.y, minr.z)
    yield Point(maxr.x, minr.y, maxr.z)
    yield Point(maxr.x, maxr.y, minr.z)
    yield maxr


def in_broad_range(minr, maxr, bot):
    """
    Check if the given bot is in range of any point within the range specified by `minr`, `maxr`.
    """
    # This is the intersection of:
    # +---+   /\
    # |   |  /  \
    # |   |  \  /
    # +---+   \/
    xr = range(minr.x, maxr.x + 1)
    yr = range(minr.y, maxr.y + 1)
    zr = range(minr.z, maxr.z + 1)

    if bot.x in xr:
        if bot.y in yr:
            if bot.z in zr:
                return True
            else:
                return min(abs(bot.z - minr.z), abs(bot.z - maxr.z)) <= bot.r
        else:
            if bot.z in zr:
                return min(abs(bot.y - minr.y), abs(bot.y - maxr.y)) <= bot.r
            else:
                return min(
                    abs(bot.y - minr.y),
                    abs(bot.y - maxr.y),
                ) + min(
                    abs(bot.z - minr.z),
                    abs(bot.z - maxr.z),
                ) <= bot.r

    else:
        if bot.y in yr:
            if bot.z in zr:
                return min(abs(bot.x - minr.x), abs(bot.x - maxr.x)) <= bot.r
            else:
                return min(
                    abs(bot.x - minr.x),
                    abs(bot.x - maxr.x),
                ) + min(
                    abs(bot.z - minr.z),
                    abs(bot.z - maxr.z),
                ) <= bot.r
        else:
            if bot.z in zr:
                return min(
                    abs(bot.x - minr.x),
                    abs(bot.x - maxr.x),
                ) + min(
                    abs(bot.y - minr.y),
                    abs(bot.y - maxr.y),
                ) <= bot.r
            else:
                return any(dist(pt, bot) <= bot.r for pt in range_corners(minr, maxr))


def fuzz_point(pt, bots):
    """
    Check directly around the given point for the point within range of the most bots.

    Err... we have an off-by-one somewhere. Looks like somehow we get the range down to:
    minr = Point(x=56721513, y=49483609, z=54441241)
    maxr = Point(x=56721513, y=49483610, z=54441242)

    Forget solving the issue or being clever: let's just check the immediate area and pick
    whatever works best there.
    """
    points = [
        Point(pt.x + dx, pt.y + dy, pt.z + dz)
        for dx in (0, 1)
        for dy in (0, 1)
        for dz in (0, 1)
    ]
    return max(points, key=lambda p: sum(1 for bot in bots if dist(bot, p) <= bot.r))


def part1(file):
    bots = []
    for line in file:
        bots.append(tuple(get_numbers(line)))

    sx, sy, sz, sr = max(bots, key=lambda bot: bot[3])
    tot = 0
    for x, y, z, r in bots:
        rng = abs(x - sx) + abs(y - sy) + abs(z - sz)
        if rng <= sr:
            tot += 1
    return tot


def part2(file):
    bots = []
    for line in file:
        bots.append(Bot(*get_numbers(line)))

    assert len(bots) == len(set(bots))

    min_range = Point(-200000000, -200000000, -200000000)
    max_range = Point( 200000000,  200000000,  200000000)

    # have to negate for a "max" heap
    # ...it is possible that I am very fortunate that the solution for my input is all positive
    heap = [(-len(bots), min_range, max_range)]

    while heap:
        _, ominr, omaxr = heapq.heappop(heap)

        splits = list(subdivide_range(ominr, omaxr))
        if not splits:
            point = fuzz_point(ominr, bots)
            return sum(map(abs, point))
        for minr, maxr in splits:
            num = sum(1 for bot in bots if in_broad_range(minr, maxr, bot))
            heapq.heappush(heap, (-num, minr, maxr))


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
