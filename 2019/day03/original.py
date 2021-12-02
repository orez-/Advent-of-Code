def intersection(hline, vline):
    vx, vyr = vline
    hxr, hy = hline

    if not (vx in hxr and hy in vyr):
        return float("inf")

    if vx == hy == 0:
        return float("inf")
    return abs(vx) + abs(hy)


def get_lines(commands):
    smallest = float("inf")
    vlines = []
    hlines = []
    x, y = 0, 0
    for c in commands:
        dirr = c[0]
        amt = int(c[1:])
        if dirr == "R":
            hline = (range(x, x + amt + 1), y)
            hlines.append(hline)
            x += amt
        if dirr == "L":
            x -= amt
            hline = (range(x, x + amt + 1), y)
            hlines.append(hline)
        if dirr == "U":
            y -= amt
            vline = x, range(y, y + amt + 1)
            vlines.append(vline)
        if dirr == "D":
            vline = x, range(y, y + amt + 1)
            vlines.append(vline)
            y += amt
    return vlines, hlines


def get_lines2(commands):
    get = {}
    x, y = 0, 0
    total = 0
    for c in commands:
        dirr = c[0]
        amt = int(c[1:])
        if dirr == "R":
            for i in range(1, amt + 1):
                if (x + i, y) not in get:
                    get[x + i, y] = total + i
            x += amt
        if dirr == "L":
            for i in range(1, amt + 1):
                if (x - i, y) not in get:
                    get[x - i, y] = total + i
            x -= amt
        if dirr == "U":
            for i in range(1, amt + 1):
                if (x, y - i) not in get:
                    get[x, y - i] = total + i
            y -= amt
        if dirr == "D":
            for i in range(1, amt + 1):
                if (x, y + i) not in get:
                    get[x, y + i] = total + i
            y += amt
        total += amt
    return get


def part1(file):
    vlines1, hlines1 = get_lines(file[0].split(','))
    vlines2, hlines2 = get_lines(file[1].split(','))

    smallest = float("inf")
    for v in vlines1:
        for h in hlines2:
            smallest = min(smallest, intersection(h, v))
    for v in vlines2:
        for h in hlines1:
            smallest = min(smallest, intersection(h, v))
    return smallest


def part2(file):
    one = get_lines2(file[0].split(','))
    two = get_lines2(file[1].split(','))

    check = one.keys() & two.keys()
    return min(one[c] + two[c] for c in check)


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
