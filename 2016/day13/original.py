import collections
import itertools
import re


NUMBER = 1358

class Maze:
    def __init__(self):
        self._maze = {}

    def __getitem__(self, coord):
        if coord not in self._maze:
            x, y = coord
            n = (x*x + 3*x + 2*x*y + y + y*y) + NUMBER
            n = sum(1 for i in bin(n) if i == '1') % 2
            self._maze[coord] = n
        return self._maze[coord]


def bfs(maze, start, end):
    seen = set()
    q = collections.deque([(start, 0)])
    while q:
        (x, y), moves = q.popleft()

        if moves >= 50:
            continue
        # if (x, y) == end:
        #     return moves

        for spot in [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]:
            x, y = spot
            if spot not in seen and x >= 0 and y >= 0:
                if not maze[spot]:
                    seen.add(spot)
                    q.append((spot, moves + 1))
    return len(seen)

if __name__ == '__main__':
    m = Maze()
    print(bfs(m, (1, 1), (31, 39)))
