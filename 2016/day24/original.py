import collections
import itertools


def bfs(maze, start, end):
    q = collections.deque([(start, 0)])
    seen = set()
    while q:
        (x, y), moves = q.popleft()

        if (x, y) == end:
            return moves

        for spot in [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]:
            x, y = spot
            if spot not in seen and maze[y][x] != '#':
                seen.add(spot)
                q.append((spot, moves + 1))


def get_nums(board):
    for y, row in enumerate(board):
        for x, e in enumerate(row):
            if e.isdigit():
                yield e, ((x, y), {})


def main(file):
    board = [
        list(line.strip())
        for line in file
    ]

    nums = dict(get_nums(board))

    for one, other in itertools.combinations(nums.items(), r=2):
        num1, (coord1, d1) = one
        num2, (coord2, d2) = other
        d1[num2] = d2[num1] = bfs(board, coord1, coord2)

    zero = nums.pop('0')

    return min(get_path_lengths(nums))


def get_path_lengths(nums):
    for perms in itertools.permutations(nums):
        total = 0
        last = '0'
        for spot in perms:
            total += nums[spot][1][last]
            last = spot

        # part 2
        total += nums[last][1]['0']
        yield total


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        print(main(file))
