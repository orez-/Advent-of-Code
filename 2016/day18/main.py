import sys


INPUT = "...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^.....^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^"
traps = {(0, 0, 1), (1, 0, 0), (0, 1, 1), (1, 1, 0)}


def get_row(row):
    last_input = (1, *row, 1)
    for i in range(1, len(INPUT) + 1):
        x = last_input[i - 1: i + 2]
        yield int(tuple(x) not in traps)


def main(rows):
    last_input = tuple(0 if x == '^' else 1 for x in INPUT)
    total = sum(last_input)

    for q in range(rows - 1):
        last_input = tuple(get_row(last_input))
        total += sum(last_input)

    return total


if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else None

    if part == '1':
        rows = 40
    elif part == '2':
        rows = 400000
    else:
        sys.exit()
    print(main(rows))
