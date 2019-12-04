"""
Original implementation I had in mind for this.

I gotta remember to start with the simple solution on these.
It's faster to implement and to debug.
"""

def intersection1(hline, vline):
    vx, vyr, _ = vline
    hxr, hy, _ = hline

    # No intersection
    if not (vx in hxr and hy in vyr):
        return float("inf")

    return abs(vx) + abs(hy)


def intersection2(hline, vline):
    vx, vyr, vt = vline
    hxr, hy, ht = hline

    # No intersection
    if not (vx in hxr and hy in vyr):
        return float("inf")

    xcost = abs(vx - hxr.start) + ht
    ycost = abs(hy - vyr.start) + vt
    return xcost + ycost


def get_lines(commands):
    vlines = []
    hlines = []
    x, y = 0, 0
    total = 0
    for c in commands:
        dirr = c[0]
        amt = int(c[1:])
        if dirr == "R":
            hline = range(x, x + amt + 1), y, total
            hlines.append(hline)
            x += amt
        if dirr == "L":
            x -= amt
            hline = range(x, x + amt + 1)[::-1], y, total
            hlines.append(hline)
        if dirr == "U":
            y -= amt
            vline = x, range(y, y + amt + 1)[::-1], total
            vlines.append(vline)
        if dirr == "D":
            vline = x, range(y, y + amt + 1), total
            vlines.append(vline)
            y += amt
        total += amt
    return vlines, hlines


def part1(file):
    vlines1, hlines1 = get_lines(file[0].split(','))
    vlines2, hlines2 = get_lines(file[1].split(','))

    return min(
        intersection1(hline, vline)
        for vlines, hlines in [(vlines1, hlines2), (vlines2, hlines1)]
        for vline in vlines
        for hline in hlines
    )


def part2(file):
    vlines1, hlines1 = get_lines(file[0].split(','))
    vlines2, hlines2 = get_lines(file[1].split(','))

    return min(
        intersection2(hline, vline)
        for vlines, hlines in [(vlines1, hlines2), (vlines2, hlines1)]
        for vline in vlines
        for hline in hlines
    )


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
