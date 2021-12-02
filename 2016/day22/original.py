import collections
import heapq
import itertools
import re


class Board:
    def __init__(self, nodes, moves=0):
        self.moves = moves
        self.nodes = nodes

    def heuristic_estimate(self):
        return next(
            node.x + node.y for node in self.nodes.values()
            if node.winner
        )

    def neighbors(self):
        # move node to next_node
        for node in self.nodes.values():
            x = node.x
            y = node.y
            for spot in [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]:
                next_node = self.nodes.get(spot)
                if not next_node:
                    continue
                if node.used and node.used <= next_node.avail:
                    nodes = dict(self.nodes.items())
                    nodes[node.x, node.y] = Node(
                        winner=False,
                        x=node.x,
                        y=node.y,
                        size=node.size,
                        used=0,
                        avail=node.size,
                        perc=0,
                    )
                    nodes[next_node.x, next_node.y] = Node(
                        winner=node.winner,
                        x=next_node.x,
                        y=next_node.y,
                        size=next_node.size,
                        used=next_node.used + node.used,
                        avail=next_node.size - (next_node.used + node.used),
                        perc=0,
                    )
                    yield Board(nodes, self.moves + 1)

    def __lt__(self, other):
        return False


def astar_solve(start):
    closedset = set()
    openset = [(start.heuristic_estimate(), start)]

    g_score = {start: 0}
    f_score = {start: start.heuristic_estimate()}

    best = 0

    while openset:
        f_s, current = heapq.heappop(openset)
        if current.nodes[0, 0].winner:
            return current.moves

        if current.moves > best:
            best = current.moves
            print(current.moves)

        closedset.add(current)
        for neighbor in current.neighbors():
            # if neighbor in closedset or neighbor.heuristic_estimate() == float("inf"):
            #     continue
            tentative_g = g_score[current] + 1

            neighbor_not_in = (neighbor.heuristic_estimate(), neighbor) not in openset
            if neighbor_not_in or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = g_score[neighbor] + neighbor.heuristic_estimate()
                if neighbor_not_in:
                    heapq.heappush(openset, (neighbor.heuristic_estimate(), neighbor))





def bfs(maze):
    deeper = 0
    q = collections.deque([(maze, 0)])
    while q:
        maze, moves = q.popleft()

        if moves > deeper:
            deeper = moves
            print(deeper)

        if maze.nodes[0, 0].winner:
            return moves

        for board in maze.neighbors():
            q.append((board, moves + 1))


Node = collections.namedtuple("Node", "winner, x, y, size, used, avail, perc")


def viable(a, b):
    return (
        a.used != 0 and
        a != b and
        a.used <= b.avail
    )


def main1(file):
    nodes = set()
    for line in file:
        match = re.match(r"/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%", line)
        nodes.add(Node(False, *map(int, match.groups())))

    return sum(
        1
        for a, b in itertools.product(nodes, repeat=2)
        if viable(a, b)
    )


def main2(file):
    nodes = get_nodes(file)
    board = Board({
        (node.x, node.y): node
        for node in nodes
    })
    return astar_solve(board)


def get_nodes(file):
    nodes = []
    for line in file:
        match = re.match(r"/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%", line)
        node = Node(False, *map(int, match.groups()))

        # FOR DEBUG
        if node.x == 33 and node.y == 0:
            node = Node(True, *map(int, match.groups()))
        nodes.append(node)
    return nodes


def print_it(file):
    nodes = get_nodes(file)
    for node in nodes:
        if node.y == 0:
            print()
        print('{}/{}'.format(node.used, node.size), end='\t')


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        print(main2(file))
        # print_it(file)
