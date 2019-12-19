from intcode import Tape


def part1(file):
    tot = 0
    for y in range(50):
        for x in range(50):
            num = get_num(file, x, y)
            tot += num
            # print(end=str(result))
        # print()
    return tot


def get_num(file, x, y):
    tape = Tape.from_file(file, input_values=[x, y])
    [result] = tape.run()
    return result


def part2(file):
    x, y = 11, 12
    while True:
        # print(x, y)
        num = get_num(file, x, y)
        if num and y >= 99:
            if get_num(file, x + 99, y - 99):
                return x * 10000 + y - 99
        if num:
            y += 1
        else:
            x += 1


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
