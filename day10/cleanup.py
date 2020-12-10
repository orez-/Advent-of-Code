import collections


def part1(file):
    joltages = sorted(map(int, file))
    threes = 1
    ones = 0
    for j1, j2 in zip([0] + joltages, joltages):
        if j2 - j1 == 3:
            threes += 1
        elif j2 - j1 == 1:
            ones += 1
    return ones * threes


def part2(file):
    joltages = sorted(map(int, file))
    ways = {0: 1}

    for j in joltages:
        ways[j] = ways.get(j - 1, 0) + ways.get(j - 2, 0) + ways.get(j - 3, 0)
    return ways[joltages[-1]]


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
