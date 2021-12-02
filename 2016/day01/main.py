import sys


def navigate(commands):
    position = [0, 0]
    direction = [0, -1]
    for cmd in commands:
        turn = cmd[0]
        dist = int(cmd[1:])

        direction[turn == 'L'] *= -1
        direction = direction[::-1]

        position[0] += direction[0] * dist
        position[1] += direction[1] * dist

    return position


def yield_path(commands):
    position = [0, 0]
    direction = [0, -1]
    for cmd in commands:
        turn = cmd[0]
        dist = int(cmd[1:])

        direction[turn == 'L'] *= -1
        direction = direction[::-1]

        for i in range(1, dist + 1):
            yield (
                position[0] + direction[0] * i,
                position[1] + direction[1] * i,
            )
        position[0] += direction[0] * dist
        position[1] += direction[1] * dist


def get_repeat_position(commands):
    spots = {(0, 0)}
    for pos in yield_path(commands):
        if pos in spots:
            return pos
        spots.add(pos)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        commands = f.read().split(', ')

    part = sys.argv[1] if len(sys.argv) > 1 else None

    if part == '1':
        # Part 1
        pos = navigate(commands)
        print(sum(map(abs, pos)))

    elif part == '2':
        # Part 2
        pos = get_repeat_position(commands)
        print(sum(map(abs, pos)))
