import sys

board = [list(row.strip()) for row in sys.stdin]
print

def surrounding(r, c, board):
    for y in (-1, 0, 1):
        for x in (-1, 0, 1):
            if x == y == 0:
                continue
            if 0 <= r + y < len(board) and 0 <= c + x < len(board[0]):
                yield board[r + y][c + x]


for _ in range(100):
    board = [
        [
            '#' if sum(
                s == '#'
                for s in surrounding(r, c, board)
            ) in {3, 3 - (elem == '#')} else '.'
            for c, elem in enumerate(row)
        ]
        for r, row in enumerate(board)
    ]
    # print '\n'.join(''.join(row) for row in board)
    # print
    board[0][0] = '#'
    board[-1][0] = '#'
    board[0][-1] = '#'
    board[-1][-1] = '#'

print(sum(
    e == '#'
    for row in board
    for e in row
))
