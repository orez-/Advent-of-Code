import collections

from intcode import Tape


OPEN = 1
WALL = 2
AIR = 3


def next_unknown(x, y, walls):
    queue = collections.deque([(x, y)])
    seen = set(queue)
    back = {}
    while queue:
        px, py = queue.popleft()
        # print(px, py, walls)
        # print((px, py) not in walls)
        if (px, py) not in walls:
            # print("go to", px, py)
            while (px, py) in back:
                # print("via", back[px, py])
                px, py, d = back[px, py]
            return d
        for dx, dy, d in [(0, -1, 1), (0, 1, 2), (-1, 0, 3), (1, 0, 4)]:
            dx += px
            dy += py
            if (dx, dy) in seen:
                continue
            if (dx, dy) in walls and walls[dx, dy] == WALL:
                continue
            seen.add((dx, dy))
            back[dx, dy] = (px, py, d)
            queue.append((dx, dy))
    # print("done")
    return None


def steps_to_air(walls):
    queue = collections.deque([(0, 0, 0)])
    seen = set(queue)
    while queue:
        px, py, d = queue.popleft()
        if walls[px, py] == AIR:
            return d

        for dx, dy, _ in [(0, -1, 1), (0, 1, 2), (-1, 0, 3), (1, 0, 4)]:
            dx += px
            dy += py
            if (dx, dy) in seen:
                continue
            if walls[dx, dy] == WALL:
                continue
            seen.add((dx, dy))
            queue.append((dx, dy, d + 1))
    raise Exception("!?")


def part1(memory):
    dirs = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
    # 0: The repair droid hit a wall. Its position has not changed.
    # 1: The repair droid has moved one step in the requested direction.
    # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.

    # north (1), south (2), west (3), and east (4).

    # Accept a movement command via an input instruction.
    # Send the movement command to the repair droid.
    # Wait for the repair droid to finish the movement operation.
    # Report on the status of the repair droid via an output instruction.

    walls = collections.defaultdict(int)
    walls[0, 0] = OPEN

    tape = Tape(memory)
    x, y = 0, 0
    outputs = tape.run()
    while True:
        direction = next_unknown(x, y, walls)
        # print(direction)
        if not direction:
            return steps_to_air(walls)
        tape.input_value = direction
        nx, ny = map(sum, zip(dirs[direction], (x, y)))
        # print("going to", nx, ny, direction)
        result = next(outputs)
        if result == 0:
            # print("bonk")
            # print(walls[nx, ny])
            walls[nx, ny] = WALL
        elif result == 1:
            walls[nx, ny] = OPEN
            x, y = nx, ny
        else:
            walls[nx, ny] = AIR
            x, y = nx, ny


def steps_from(pos, walls):
    """Get the distance to the farthest spot from `pos`."""
    queue = collections.deque([(*pos, 0)])
    seen = {pos}
    biggest = 0
    while queue:
        px, py, d = queue.popleft()
        biggest = max(biggest, d)
        for dx, dy, _ in [(0, -1, 1), (0, 1, 2), (-1, 0, 3), (1, 0, 4)]:
            dx += px
            dy += py
            if (dx, dy) in seen:
                continue
            if walls[dx, dy] == WALL:
                continue
            seen.add((dx, dy))
            queue.append((dx, dy, d + 1))
    return biggest


def part2(memory):
    dirs = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
    # 0: The repair droid hit a wall. Its position has not changed.
    # 1: The repair droid has moved one step in the requested direction.
    # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.

    # north (1), south (2), west (3), and east (4).

    # Accept a movement command via an input instruction.
    # Send the movement command to the repair droid.
    # Wait for the repair droid to finish the movement operation.
    # Report on the status of the repair droid via an output instruction.

    walls = collections.defaultdict(int)
    walls[0, 0] = OPEN

    tape = Tape(memory)
    x, y = 0, 0
    outputs = tape.run()
    while True:
        direction = next_unknown(x, y, walls)
        # print(direction)
        if not direction:
            # pprint.pprint(walls)
            air = next(k for k, v in walls.items() if v == AIR)
            return steps_from(air, walls)
        tape.input_value = direction
        nx, ny = map(sum, zip(dirs[direction], (x, y)))
        # print("going to", nx, ny, direction)
        result = next(outputs)
        if result == 0:
            # print("bonk")
            # print(walls[nx, ny])
            walls[nx, ny] = WALL
        elif result == 1:
            walls[nx, ny] = OPEN
            x, y = nx, ny
        else:
            walls[nx, ny] = AIR
            x, y = nx, ny


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, file[0].split(',')))
    print(part1(list(file)))
    print(part2(list(file)))
