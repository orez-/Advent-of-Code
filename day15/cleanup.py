import collections

from intcode import Tape


WALL = 0
OPEN = 1
AIR = 2

# north (1), south (2), west (3), and east (4).
DIRECTIONS = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}


def rebuild_path(x, y, back):
    path = []
    while (x, y) in back:
        x, y, direction = back[x, y]
        path.append(direction)
    return path[::-1]


def path_to_next_unknown(x, y, board):
    """
    Return the path of directions to walk to the next unexplored area.

    If there are no more reachable unexplored areas `None` is returned.
    """
    queue = collections.deque([(x, y)])
    seen = {(x, y)}
    back = {}
    while queue:
        px, py = queue.popleft()
        if (px, py) not in board:
            return rebuild_path(px, py, back)
        for direction, (dx, dy) in DIRECTIONS.items():
            dx += px
            dy += py
            if (dx, dy) in seen:
                continue
            if board.get((dx, dy)) == WALL:
                continue
            seen.add((dx, dy))
            back[dx, dy] = (px, py, direction)
            queue.append((dx, dy))
    return None


def steps_to_air(board):
    queue = collections.deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        px, py, distance = queue.popleft()
        if board[px, py] == AIR:
            return distance

        for dx, dy in DIRECTIONS.values():
            dx += px
            dy += py
            if (dx, dy) in seen:
                continue
            if board[dx, dy] == WALL:
                continue
            seen.add((dx, dy))
            queue.append((dx, dy, distance + 1))
    raise Exception("Couldn't find a path to the oxygen system")


def steps_from(pos, board):
    """Get the distance to the farthest spot from `pos`."""
    queue = collections.deque([(*pos, 0)])
    seen = {pos}
    while queue:
        px, py, distance = queue.popleft()
        for dx, dy in DIRECTIONS.values():
            dx += px
            dy += py
            if (dx, dy) in seen:
                continue
            if board[dx, dy] == WALL:
                continue
            seen.add((dx, dy))
            queue.append((dx, dy, distance + 1))
    return distance


def explore_area(robot):
    board = {(0, 0): OPEN}
    x, y = 0, 0
    outputs = robot.run()
    while True:
        path = path_to_next_unknown(x, y, board)
        if not path:
            return board
        for direction in path:
            robot.input_value = direction
            dx, dy = DIRECTIONS[direction]
            nx, ny = x + dx, y + dy
            result = next(outputs)

            # 0: The repair droid hit a wall. Its position has not changed.
            # 1: The repair droid has moved one step in the requested direction.
            # 2: The repair droid has moved one step in the requested direction;
            #    its new position is the location of the oxygen system.
            board[nx, ny] = result
            if result:
                x, y = nx, ny


def part1(memory):
    robot = Tape(memory)
    board = explore_area(robot)
    return steps_to_air(board)


def part2(memory):
    robot = Tape(memory)
    board = explore_area(robot)
    air = next(coord for coord, tile in board.items() if tile == AIR)
    return steps_from(air, board)


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, file[0].split(',')))
    print(part1(list(file)))
    print(part2(list(file)))
