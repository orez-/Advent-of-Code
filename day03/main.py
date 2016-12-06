import sys


def format_line(line):
    return map(int, line.strip().split())


def cols(file):
    for lines in zip(file, file, file):
        yield from zip(*lines)


if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else None

    with open('input.txt', 'r') as file:
        file = map(format_line, file)

        if part == '2':
            file = cols(file)
        elif part != '1':
            sys.exit()

        file = map(sorted, file)
        print(sum(1 for a, b, c in file if a + b > c))
