import collections
import hashlib


INPUT = "njfxhljp"
OPEN = set('bcdef')
DIRS = 'UDLR'



def bfs(maze):
    max_ = 0
    q = collections.deque([(maze, (0, 0), 0)])
    while q:
        maze, (x, y), moves = q.popleft()

        if (x, y) == (3, 3):
            # PART 1
            return maze[len(INPUT):]
            # PART 2
            # if moves > max_:
            #     max_ = moves
            #     print(moves)
            # continue

        move_options = hashlib.md5(maze.encode('utf8')).hexdigest()[:4]
        # up, down, left, and right

        for i, spot in enumerate([(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]):
            x, y = spot
            if 0 <= x < 4 and 0 <= y < 4 and move_options[i] in OPEN:
                q.append((maze + DIRS[i], (x, y), moves + 1))


print(bfs(INPUT))
