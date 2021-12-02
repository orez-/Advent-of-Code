import collections
import dataclasses
import heapq


@dataclasses.dataclass
class Board:
    walls: set
    doors: dict
    keys: dict
    robots: tuple

    @classmethod
    def from_file(cls, file):
        return cls(
            walls={
                (x, y)
                for y, row in enumerate(file)
                for x, elem in enumerate(row)
                if elem == "#"
            },
            doors={
                (x, y): elem.lower()
                for y, row in enumerate(file)
                for x, elem in enumerate(row)
                if elem.lower() != elem
            },
            keys={
                (x, y): elem
                for y, row in enumerate(file)
                for x, elem in enumerate(row)
                if elem.upper() != elem
            },
            robots=tuple(
                (x, y)
                for y, row in enumerate(file)
                for x, elem in enumerate(row)
                if elem == "@"
            ),
        )


@dataclasses.dataclass
class Path:
    destination: str
    doors: frozenset
    keys: frozenset
    distance: int

    def __repr__(self):
        return (
            f"Path({self.destination!r}, {''.join(self.doors).upper()!r}, "
            f"{''.join(self.keys)!r}, {self.distance})"
        )


@dataclasses.dataclass(frozen=True)
class State:
    keys: frozenset
    robots: tuple

    @classmethod
    def new(cls, num_robots):
        return State(
            keys=frozenset(),
            robots=tuple(range(num_robots))
        )

    def next_states(self, paths):
        for robot_id, position in enumerate(self.robots):
            for path in paths[position]:
                if path.destination in self.keys or not (path.doors <= self.keys):
                    continue
                robots = list(self.robots)
                robots[robot_id] = path.destination
                yield State(
                    keys=self.keys | path.keys,
                    robots=tuple(robots),
                ), path.distance

    def is_solved(self):
        # TODO: don't hardcode 26 :(
        return len(self.keys) == 26

    def __lt__(self, other):
        # This isn't important, it just has to be total orderable, somehow.
        return str(self.robots) < str(other.robots)


def simplify_paths(board):
    paths = {}

    for (kx, ky), key in board.keys.items():
        paths[key] = list(get_key_paths(kx, ky, board))

    for robot_id, (x, y) in enumerate(board.robots):
        paths[robot_id] = list(get_key_paths(x, y, board))

    return paths


def get_key_paths(kx, ky, board):
    queue = collections.deque([(kx, ky, 0, frozenset(), frozenset())])
    seen = {(kx, ky)} | board.walls

    while queue:
        x, y, steps, seen_doors, seen_keys = queue.popleft()
        if (x, y) in board.keys and (x, y) != (kx, ky):
            yield Path(
                destination=board.keys[x, y],
                doors=seen_doors,
                keys=seen_keys,
                distance=steps,
            )
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = x + dx
            ny = y + dy
            if (nx, ny) in seen:
                continue
            seen.add((nx, ny))
            if (nx, ny) in board.doors:
                seen_doors |= {board.doors[nx, ny]}
            if (nx, ny) in board.keys:
                seen_keys |= {board.keys[nx, ny]}
            queue.append((nx, ny, steps + 1, seen_doors, seen_keys))


def dijkstra_search(start, paths):
    closedset = set()
    open_queue = [(0, start)]
    open_set = {start}

    g_score = {start: 0}

    while open_queue:
        f_s, current = heapq.heappop(open_queue)
        open_set.discard(current)
        if current.is_solved():
            return g_score[current]

        closedset.add(current)
        for neighbor, steps in current.next_states(paths):
            if neighbor in closedset:
                continue
            tentative_g = g_score[current] + steps

            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                # XXX: This seems really wrong to me
                if neighbor not in open_set:
                    heapq.heappush(open_queue, (g_score[neighbor], neighbor))


def part1(file):
    board = Board.from_file(file)
    paths = simplify_paths(board)
    state = State.new(num_robots=len(board.robots))

    return dijkstra_search(state, paths)


def part2(file):
    file[39] = list(file[39])
    file[39][39:42] = "@#@"
    file[40] = list(file[40])
    file[40][39:42] = "###"
    file[41] = list(file[41])
    file[41][39:42] = "@#@"

    board = Board.from_file(file)
    paths = simplify_paths(board)
    state = State.new(num_robots=len(board.robots))

    return dijkstra_search(state, paths)


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
