import sys


def navigate_keypad(keypad, start, directions):
    num = ""
    x, y = start
    for line in directions:
        for char in line:
            tx, ty = x, y
            if char == 'U':
                ty = y - 1
            if char == 'R':
                tx = x + 1
            if char == 'D':
                ty = y + 1
            if char == 'L':
                tx = x - 1

            if keypad[ty][tx] != ' ':
                x = tx
                y = ty

        num += keypad[y][x]
    return num


if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else None

    if part == '1':
        keypad = [
            '     ',
            ' 123 ',
            ' 456 ',
            ' 789 ',
            '     ',
        ]
        start = 2, 2
    elif part == '2':
        keypad = [
            '       ',
            '   1   ',
            '  234  ',
            ' 56789 ',
            '  ABC  ',
            '   D   ',
            '       ',
        ]
        start = 1, 3
    else:
        sys.exit()

    with open('input.txt', 'r') as file:
        print(navigate_keypad(keypad, start, file))
