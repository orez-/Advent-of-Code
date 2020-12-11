import itertools


def around(seats, x, y):
    total = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == dy == 0:
                continue
            if seats.get((x + dx, y + dy)) == '#':
                total += 1
    return total


def seen_around(seats, x, y, width, height):
    total = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == dy == 0:
                continue
            for dd in itertools.count(1):
                cx = x + dx * dd
                cy = y + dy * dd
                if not (cx in range(width) and cy in range(height)):
                    break
                if seats[cx, cy] == '#':
                    total += 1
                    break
                if seats[cx, cy] == 'L':
                    break
    return total


def part1(file):
    # empty L, occupied #
    seats = {(x, y): e for y, row in enumerate(file) for x, e in enumerate(row)}
    p = 1
    while p:
        new_seats = dict()
        p = 0
        for (x, y), e in seats.items():
            if e == 'L' and around(seats, x, y) == 0:
                e = '#'
                p = 1
            elif e == '#' and around(seats, x, y) >= 4:
                e = 'L'
                p = 1
            new_seats[x, y] = e
        seats = new_seats
    return sum(1 for s in seats.values() if s == '#')


def part2(file):
    # empty L, occupied #
    height = len(file)
    width = len(file[0])
    seats = {(x, y): e for y, row in enumerate(file) for x, e in enumerate(row)}
    p = 1
    while p:
        new_seats = dict()
        p = 0
        for (x, y), e in seats.items():
            if e == 'L' and seen_around(seats, x, y, width, height) == 0:
                e = '#'
                p = 1
            elif e == '#' and seen_around(seats, x, y, width, height) >= 5:
                e = 'L'
                p = 1
            new_seats[x, y] = e
        seats = new_seats
    return sum(1 for s in seats.values() if s == '#')


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
