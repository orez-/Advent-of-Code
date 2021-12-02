def part1(file):
    return sum((x // 3) - 2 for x in map(int, file))


def part2(file):
    total = 0
    for amt in map(int, file):
        while amt:
            amt = max((amt // 3) - 2, 0)
            total += amt
    return total


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
