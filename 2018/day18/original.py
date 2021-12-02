import collections


def around(x, y):
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == dy == 0:
                continue
            yield dx + x, dy + y


def part1(file):
    board = {
        (x, y): tile
        for y, row in enumerate(file)
        for x, tile in enumerate(row)
    }

    for i in range(10):
        new_board = {}
        for (x, y), tile in board.items():
            if tile == '.':
                if sum(
                    board.get(position) == '|'
                    for position in around(x, y)
                ) >= 3:
                    new_board[x, y] = '|'
                else:
                    new_board[x, y] = '.'
            elif tile == '|':
                if sum(
                    board.get(position) == '#'
                    for position in around(x, y)
                ) >= 3:
                    new_board[x, y] = '#'
                else:
                    new_board[x, y] = '|'
            elif tile == '#':
                if set('|#') <= set(
                    board.get(position)
                    for position in around(x, y)
                ):
                    new_board[x, y] = '#'
                else:
                    new_board[x, y] = '.'
            else:
                raise Exception("wat")
        board = new_board

    trees = sum(tile == '|' for tile in board.values())
    lumber = sum(tile == '#' for tile in board.values())
    return trees * lumber


def print_board(board):
    joiner = collections.deque()
    for y in range(50):
        for x in range(50):
            joiner.append(board[x, y])
        joiner.append('\n')
    print(''.join(joiner))


def part2(file):
    board = {
        (x, y): tile
        for y, row in enumerate(file)
        for x, tile in enumerate(row)
    }
    seen = {}

    i = 0
    jump = True
    top = 1000000000
    while i < top:
        new_board = {}
        for (x, y), tile in board.items():
            if tile == '.':
                if sum(
                    board.get(position) == '|'
                    for position in around(x, y)
                ) >= 3:
                    new_board[x, y] = '|'
                else:
                    new_board[x, y] = '.'
            elif tile == '|':
                if sum(
                    board.get(position) == '#'
                    for position in around(x, y)
                ) >= 3:
                    new_board[x, y] = '#'
                else:
                    new_board[x, y] = '|'
            elif tile == '#':
                if set('|#') <= set(
                    board.get(position)
                    for position in around(x, y)
                ):
                    new_board[x, y] = '#'
                else:
                    new_board[x, y] = '.'
            else:
                raise Exception("wat")
        board = new_board
        hashed = tuple(sorted(board.items()))
        if jump and hashed in seen:
            jump = False
            period = i - seen[hashed]
            i = top - ((top - i) % period)
        seen[hashed] = i
        i += 1

    trees = sum(tile == '|' for tile in board.values())
    lumber = sum(tile == '#' for tile in board.values())
    return trees * lumber


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
