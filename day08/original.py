import re


def main(file):
    # rectAxB
    # rotate row y=A by B
    # rotate row x=A by B
    strips = [
        [0 for _ in range(50)]
        for _ in range(6)
    ]
    for line in file:
        m = re.match(r'rect (\d+)x(\d+)', line)
        if m:
            wide, tall = map(int, m.groups())
            for y in range(tall):
                for x in range(wide):
                    strips[y][x] = 1
        else:
            coord, row, amt = re.match(r'rotate \w+ (x|y)=(\d+) by (\d+)', line).groups()
            row, amt = int(row), int(amt)
            if coord == 'x':
                strips = list(map(list, zip(*strips)))
            strips[row] = strips[row][-amt:] + strips[row][:-amt]
            if coord == 'x':
                strips = list(map(list, zip(*strips)))
    # PART 1
    # return sum(map(sum, strips))

    # PART 2
    for line in strips:
        print(''.join('#' if c else ' ' for c in line))



if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        main(file)
