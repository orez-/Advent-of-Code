def part1(file):
    file = list(map(int, file))
    for num1 in file:
        for num2 in file:
            if num1 + num2 == 2020:
                return num1 * num2


def part2(file):
    file = list(map(int, file))
    for num1 in file:
        for num2 in file:
            for num3 in file:
                if num1 + num2 + num3 == 2020:
                    return num1 * num2 * num3


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
