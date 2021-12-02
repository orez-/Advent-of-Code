def part1(file):
    # Action N means to move north by the given value.
    # Action S means to move south by the given value.
    # Action E means to move east by the given value.
    # Action W means to move west by the given value.
    # Action L means to turn left the given number of degrees.
    # Action R means to turn right the given number of degrees.
    # Action F means to move forward by the given value in the direction the ship is currently facing.
    fx, fy = 1, 0
    x, y = 0, 0
    for line in file:
        cmd = line[0]
        num = int(line[1:])
        if cmd == 'N':
            y -= num
        elif cmd == 'S':
            y += num
        elif cmd == 'W':
            x -= num
        elif cmd == 'E':
            x += num
        elif cmd == 'L':
            assert num % 90 == 0
            while num > 0:
                fx, fy = fy, -fx
                num -= 90
        elif cmd == 'R':
            assert num % 90 == 0
            while num > 0:
                fx, fy = -fy, fx
                num -= 90
        elif cmd == 'F':
            x += fx * num
            y += fy * num
    return abs(x) + abs(y)



def part2(file):
    # Action N means to move the waypoint north by the given value.
    # Action S means to move the waypoint south by the given value.
    # Action E means to move the waypoint east by the given value.
    # Action W means to move the waypoint west by the given value.
    # Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
    # Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
    # Action F means to move forward to the waypoint a number of times equal to the given value.

    wx, wy = 10, -1
    x, y = 0, 0
    for line in file:
        cmd = line[0]
        num = int(line[1:])
        if cmd == 'N':
            wy -= num
        elif cmd == 'S':
            wy += num
        elif cmd == 'W':
            wx -= num
        elif cmd == 'E':
            wx += num
        elif cmd == 'L':
            assert num % 90 == 0
            while num > 0:
                wx, wy = wy, -wx
                num -= 90
        elif cmd == 'R':
            assert num % 90 == 0
            while num > 0:
                wx, wy = -wy, wx
                num -= 90
        elif cmd == 'F':
            x += wx * num
            y += wy * num
    return abs(x) + abs(y)


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
