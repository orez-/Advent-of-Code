def get_seat_ids(file):
    for line in file:
        line = line.replace('F', '0')
        line = line.replace('B', '1')
        line = line.replace('L', '0')
        line = line.replace('R', '1')
        yield int(line, 2)


def part1(file):
    return max(get_seat_ids(file))


def part2(file):
    seat_ids = set(get_seat_ids(file))
    for x in range(128 * 8):
        if x - 1 in seat_ids and x + 1 in seat_ids and x not in seat_ids:
            return x


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
