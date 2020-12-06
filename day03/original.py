def part1(file):
    x = 0
    t = 0
    for line in file:
        if line[x] == '#':
            t += 1
        x += 3
        x %= len(line)
    return t


def part2(file):
    v = 1
    for s in [1, 3, 5, 7]:
        x = 0
        t = 0
        for line in file:
            if line[x] == '#':
                t += 1
            x += s
            x %= len(line)
        v *= t
    f = iter(file)
    x = 0
    t = 0
    for line in f:
        if line[x] == '#':
            t += 1
        x += 1
        x %= len(line)
        next(f, 0)
    return v * t


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
