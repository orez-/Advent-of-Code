def part1(file):
    total = 0
    for line in file:
        range_, char, string = line.split()
        low, high = map(int, range_.split('-'))
        char = char.rstrip(':')
        count = string.count(char)
        if low <= count <= high:
            total += 1
    return total


def part2(file):
    total = 0
    for line in file:
        range_, char, string = line.split()
        low, high = map(int, range_.split('-'))
        char = char.rstrip(':')
        one = string[low-1:low] == char
        other = string[high-1:high] == char
        if one != other:
            total += 1
    return total


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
