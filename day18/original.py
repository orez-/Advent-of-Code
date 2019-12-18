import collections
import dataclasses
import heapq
import functools

from frozendict import frozendict


def apply(fn):
    def decorator(inner_fn):
        @functools.wraps(inner_fn)
        def anon(*args, **kwargs):
            return fn(inner_fn(*args, **kwargs))
        return anon
    return decorator


@dataclasses.dataclass(frozen=True)
class Board:
    walls: frozendict = dataclasses.field(compare=False)
    doors: frozendict
    keys: frozendict
    collected_keys: frozenset
    robots: tuple

    @classmethod
    def from_file(cls, file):
        return cls(
            walls=frozendict({
                (x, y): elem == "#"
                for y, row in enumerate(file)
                for x, elem in enumerate(row)
            }),
            doors=frozendict({
                (x, y): elem.lower()
                for y, row in enumerate(file)
                for x, elem in enumerate(row)
                if elem.lower() != elem
            }),
            keys=frozendict({
                (x, y): elem
                for y, row in enumerate(file)
                for x, elem in enumerate(row)
                if elem.upper() != elem
            }),
            collected_keys=frozenset(),
            robots=tuple(
                (x, y)
                for y, row in enumerate(file)
                for x, elem in enumerate(row)
                if elem == "@"
            ),
        )

    def is_solved(self):
        return not self.keys

    def move_to(self, robot_id, x, y):
        # assumes the robot could move there
        keys = self.keys
        collected_keys = self.collected_keys
        if (x, y) in self.keys:
            key = self.keys[x, y]
            keys = frozendict({k: v for k, v in keys.items() if k != (x, y)})
            collected_keys |= {key}

        robots = list(self.robots)
        robots[robot_id] = (x, y)

        return Board(
            walls=self.walls,
            doors=self.doors,
            keys=keys,
            collected_keys=collected_keys,
            robots=tuple(robots),
        )

    def impassible(self, x, y):
        if self.walls.get((x, y)):
            return True
        door = self.doors.get((x, y))
        return door and door not in self.collected_keys

    @functools.lru_cache()
    @apply(list)
    def next_goals(self):
        for robot_id, (x, y) in enumerate(self.robots):
            queue = collections.deque([(x, y, 0)])
            seen = {(x, y)}

            while queue:
                x, y, steps = queue.popleft()
                if (x, y) in self.keys:
                    yield self.move_to(robot_id, x, y), steps
                    continue
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx = x + dx
                    ny = y + dy
                    if (nx, ny) in seen or self.impassible(nx, ny):
                        continue
                    seen.add((nx, ny))
                    queue.append((nx, ny, steps + 1))

    def heuristic_estimate(self):
        return len(self.keys)

    def __repr__(self):
        return f"Board(keys={list(self.collected_keys)})"

    def __lt__(self, other):
        # This isn't important, it just has to be total orderable, somehow.
        return self.robots < other.robots


def draw_board(board):
    af = '\x1b[38;5;{}m'.format
    clear = '\x1b[0m'

    xs = [x for x, _ in board.walls]
    ys = [y for _, y in board.walls]
    left = min(xs)
    right = max(xs)
    top = min(ys)
    bottom = max(ys)

    output = []
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if (x, y) in board.robots:
                output.append("@")
            elif (x, y) in board.doors and board.doors[x, y] not in board.collected_keys:
                output.append(board.doors[x, y].upper())
            elif (x, y) in board.keys:
                output.append(board.keys[x, y])
            else:
                output.append(af(8) + (".#"[board.walls[x, y]]) + clear)
        output.append("\n")
    print(''.join(output))


def search(start, steps=0):
    closedset = set()
    open_queue = [(start.heuristic_estimate(), start)]
    open_set = {start}

    g_score = {start: 0}
    f_score = {start: start.heuristic_estimate()}

    while open_queue:
        f_s, current = heapq.heappop(open_queue)
        open_set.discard(current)
        if current.is_solved():
            return g_score[current]

        closedset.add(current)
        for neighbor, steps in current.next_goals():
            if neighbor in closedset or neighbor.heuristic_estimate() == float("inf"):
                continue
            tentative_g = g_score[current] + steps

            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                f_score[neighbor] = g_score[neighbor] + neighbor.heuristic_estimate()
                if neighbor not in open_set:
                    heapq.heappush(open_queue, (f_score[neighbor], neighbor))


def part1(file):
    # Part 1 took 5m31s to run!!
    board = Board.from_file(file)
    # draw_board(board)

    return search(board)


def part2(file):
    # Part 2 took 6m47s to run!!!!
    file[39] = list(file[39])
    file[39][39:42] = "@#@"
    file[40] = list(file[40])
    file[40][39:42] = "###"
    file[41] = list(file[41])
    file[41][39:42] = "@#@"

    board = Board.from_file(file)
    # draw_board(board)

    return search(board)


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
