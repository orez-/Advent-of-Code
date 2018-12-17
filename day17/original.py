import collections
import re


def get_digits(line):
    return (int(match[0]) for match in re.finditer(r"\d+", line))


af = '\x1b[38;5;{}m{}\x1b[0m'.format

def print_board(board, hilite=None):
    output = collections.deque()
    if hilite:
        _, y = hilite
    else:
        y = max(y for (x, y), tile in board.items() if tile in '|~')
    y_min = y - 20
    y_max = y + 5
    x_min = min(x for x, y in board)
    x_max = max(x for x, y in board)
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            tile = board.get((x, y), '.')
            if hilite == (x, y):
                output.append(af(1, tile))
            else:
                output.append(tile)
        output.append('\n')
    output.append('\n\n\n\n\n-~-')
    print(''.join(output))


def test_data():
    file = """
..............
............#.
.#..#.......#.
.#..#..#......
.#..#..#......
.#.....#......
.#.....#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...
    """.strip().split('\n')
    board = {}
    for y, line in enumerate(file):
        for x, elem in enumerate(line, 494):
            if elem == '.':
                continue
            board[x, y] = elem
    return board


def run_water(file):
    board = {}
    for line in file:
        coords = get_digits(line)
        if line.startswith('x'):
            x, ymin, ymax = coords
            for y in range(ymin, ymax + 1):
                board[x, y] = '#'
        else:
            y, xmin, xmax = coords
            for x in range(xmin, xmax + 1):
                board[x, y] = '#'

    # board = test_data()
    y_min = min(y for x, y in board)
    y_max = max(y for x, y in board)

    board[500, 0] = '|'
    sources = collections.deque([(500, 0)])
    while sources:
        x, y = sources.pop()
        down = y + 1
        if down > y_max:
            break
        fall = board.get((x, down))
        # Pool on ground and standing water
        if fall in tuple('#~'):
            left = x
            fill_left = True
            while True:
                left -= 1
                if board.get((left, y)) == '#':
                    left += 1
                    break
                elif board.get((left, y)) == '~':
                    break

                if board.get((left, down)) not in tuple('#~'):
                    fill_left = False
                    break

            right = x
            fill_right = True
            while True:
                right += 1
                # Hit a wall
                if board.get((right, y)) == '#':
                    right -= 1
                    break
                # uh shouldn't hit water?
                elif board.get((right, y)) == '~':
                    break

                # can fall
                if board.get((right, down)) not in tuple('#~'):
                    fill_right = False
                    break

            if fill_left and fill_right:
                for ox in range(left, right + 1):
                    board[ox, y] = '~'
                sources.append((x, y - 1))
            else:
                for ox in range(left, right + 1):
                    board[ox, y] = '|'
                if not fill_right:
                    sources.append((right, y))
                if not fill_left:
                    sources.append((left, y))

        elif fall is None:
            while down <= y_max and board.get((x, down)) is None:
                board[x, down] = '|'
                down += 1
            if down <= y_max and board[x, down] in '#~':
                sources.append((x, down - 1))
        elif fall != '|':
            print("yo what", fall)
    return board, y_min, y_max


def part1(board, y_min, y_max):
    return sum(
        tile in '|~' and y_min <= y <= y_max
        for (x, y), tile in board.items()
    )


def part2(board, y_min, y_max):
    return sum(
        tile == '~' and y_min <= y <= y_max
        for (x, y), tile in board.items()
    )


def main():
    with open('file.txt') as f:
        file = list(f)
    board, y_min, y_max = run_water(file)
    print(part1(board, y_min, y_max))
    print(part2(board, y_min, y_max))


if __name__ == '__main__':
    main()
