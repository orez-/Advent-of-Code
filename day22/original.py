import functools
import heapq
import typing


DEPTH = 11739
TARGET = (11, 718)


class Frame(typing.NamedTuple):
    fscore: int
    time: int
    x: int
    y: int
    item: int

    @property
    def seen(self):
        return (self.x, self.y, self.item)


def estimate(x, y):
    return abs(TARGET[0] - x) + abs(TARGET[1] - y)


TERRAIN_TO_ITEMS = {
    0: {0, 1},
    1: {1, 2},
    2: {2, 0},
}


def get_neighbors(current):
    [other_item] = TERRAIN_TO_ITEMS[terrain(current.x, current.y)] - {current.item}
    swap_time = current.time + 7
    est = estimate(current.x, current.y)
    yield Frame(est + swap_time, swap_time, current.x, current.y, other_item)

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        x = current.x + dx
        y = current.y + dy
        if x < 0 or y < 0:
            continue
        if current.item not in TERRAIN_TO_ITEMS[terrain(x, y)]:
            continue
        yield Frame(estimate(x, y) + current.time + 1, current.time + 1, x, y, current.item)


@functools.lru_cache(None)
def geo_index(x, y):
    if (x, y) in [(0, 0), TARGET]:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion(x - 1, y) * erosion(x, y - 1)


@functools.lru_cache(None)
def erosion(x, y):
    result = ((geo_index(x, y) + DEPTH) % 20183)
    return result


def terrain(x, y):
    return erosion(x, y) % 3


def part1():
    total = 0
    X, Y = TARGET
    for x in range(X + 1):
        for y in range(Y + 1):
            total += terrain(x, y)
    return total


def part2():
    # torch, gear, neither
    # terrain 0 item 0 or 1
    # terrain 1 item 1 or 2
    # terrain 2 item 2 or 0
    heap = [Frame(estimate(0, 0), 0, 0, 0, 0)]
    seen = set()
    path = {}
    while heap:
        current = heapq.heappop(heap)
        if (current.x, current.y, current.item) == (*TARGET, 0):
            me = current
            while me in path:
                print(me)
                me = path[me]
            print(me)
            return current.time
        seen.add(current.seen)

        for frame in get_neighbors(current):
            if frame.seen in seen:
                continue

            indx = next((
                i for i, h in enumerate(heap)
                if frame.seen == h.seen
            ), None)
            if indx is None:
                heapq.heappush(heap, frame)
                path[frame] = current
            elif heap[indx].time > frame.time:
                heap[indx] = frame
                path[frame] = current
                heapq.heapify(heap)


if __name__ == '__main__':
    print(part1())
    print(part2())
