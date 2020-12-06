def part1(file):
    x = []
    for line in file:
        line = line.replace('F', '0')
        line = line.replace('B', '1')
        line = line.replace('L', '0')
        line = line.replace('R', '1')
        v = int(line, 2)
        x.append(v)
    return max(x)


def part2(file):
    x = []
    for line in file:
        line = line.replace('F', '0')
        line = line.replace('B', '1')
        line = line.replace('L', '0')
        line = line.replace('R', '1')
        v = int(line, 2)
        x.append(v)
    return set(range(0, 0b1111111111)) - set(x)


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
