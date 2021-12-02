def part1(file):
    groups = '\n'.join(file).split('\n\n')
    t = 0
    for g in groups:
        t += len(set(''.join(g.split('\n'))))
    return t


def part2(file):
    groups = '\n'.join(file).split('\n\n')
    t = 0
    for g in groups:
        x = list(map(set, g.split('\n')))
        t += len(set.intersection(*x))
    return t


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
