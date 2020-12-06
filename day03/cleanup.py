def trees_hit(terrain, run, fall=1):
    x = 0
    t = 0
    for line in terrain[::fall]:
        if line[x] == '#':
            t += 1
        x += run
        x %= len(line)
    return t


def part1(file):
    return trees_hit(file, run=3)


def part2(file):
    return (
        trees_hit(file, run=1) *
        trees_hit(file, run=3) *
        trees_hit(file, run=5) *
        trees_hit(file, run=7) *
        trees_hit(file, run=1, fall=2)
    )


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
