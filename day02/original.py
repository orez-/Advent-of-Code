# keypad = ['123', '456', '789']

# pos = [0, 0]
# num = ''
# with open('input.txt', 'r') as f:
#     for line in f:
#         for char in line:
#             if char == 'U':
#                 pos[1] = max(0, pos[1] - 1)
#             if char == 'R':
#                 pos[0] = min(2, pos[0] + 1)
#             if char == 'D':
#                 pos[1] = min(2, pos[1] + 1)
#             if char == 'L':
#                 pos[0] = max(0, pos[0] - 1)
#         num += keypad[pos[1]][pos[0]]
# print(num)


keypad = [
    '       ',
    '   1   ',
    '  234  ',
    ' 56789 ',
    '  ABC  ',
    '   D   ',
    '       ',
]
x, y = 1, 3
num = ''
with open('input.txt', 'r') as f:
    for line in f:
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

        print(y, x)
        num += keypad[y][x]
print(repr(num))
