import collections
import time

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
        path.append((x, y, direction))
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


def print_board(px, py, board, path):
    af = '\x1b[38;5;{}m'.format
    ab = '\x1b[48;5;{}m'.format
    clear = '\x1b[0m'
    char_lookup = {None: " ", WALL: "█", OPEN: ".", AIR: "$"}
    path = set((x, y) for x, y, _ in path)

    output = []
    for y in range(-21, 20):
        for x in range(-21, 20):
            color = ""
            if (x, y) in path:
                color = ab(100)
            if (x, y) == (px, py):
                color += af(3)
                char = "@"
            else:
                char = char_lookup[board.get((x, y))]
                if char == ".":
                    color += af(8)
            if color:
                char = f"{color}{char}{clear}"
            output.append(char)
        output.append("\n")
    print("".join(output))
    time.sleep(0.02)


def explore_area(robot):
    board = {(0, 0): OPEN}
    x, y = 0, 0
    outputs = robot.run()
    print_board(x, y, board, [])
    while True:
        path = path_to_next_unknown(x, y, board)
        if not path:
            return board
        for _, _, direction in path:
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
            print_board(x, y, board, path)


def main(memory):
    robot = Tape(memory)
    explore_area(robot)


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, file[0].split(',')))
    main(file)
