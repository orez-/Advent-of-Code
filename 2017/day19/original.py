def get(file, y, x):
    if y < 0 or x < 0:
        return ' '
    try:
        return file[y][x]
    except:
        return ' '


def main(file):
    dx = 0
    dy = 1
    x = file[0].index('|')
    y = 0
    word = []
    s = 0
    while True:
        spot = get(file, y, x)
        if spot == ' ':
            print(''.join(word))  # part 1
            print(s)  # part 2
            return
        if spot not in '-|+':
            word.append(spot)
        elif spot == '+':
            if get(file, y + dy, x + dx) != '|-'[bool(dx)]:
                if get(file, y + dx, x + dy) != ' ':
                    dx, dy = dy, dx
                elif get(file, y - dx, x - dy) != ' ':
                    dx, dy = -dy, -dx
                else:
                    raise Exception('whuh oh')
        x += dx
        y += dy
        s += 1


if __name__ == '__main__':
    with open('file.txt', 'r') as f:
        fi = list(map(str.rstrip, f))
    main(fi)
