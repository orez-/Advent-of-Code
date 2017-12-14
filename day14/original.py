import collections
import itertools


inpu = 'oundnydw'


def search(full_map, start, seen):
    q = collections.deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            dx += x
            dy += y
            if 0 <= dx < 128 and 0 <= dy < 128 and (dx, dy) not in seen and full_map[dy][dx] == '1':
                seen.add((dx, dy))
                q.append((dx, dy))

def main():
    s = 0
    full_map = []
    for line in range(0, 128):
        value = hashit(f'{inpu}-{line}')
        # print(value)
        q = ''.join(
            f'{int(v, 16):0>4b}'
            for v in value
        )
        s += q.count('1')
        full_map.append(q)
    print(s)  # part 1

    seen = set()
    total = 0
    for y, row in enumerate(full_map):
        for x, elem in enumerate(row):
            if elem == '1' and (x, y) not in seen:
                search(full_map, (x, y), seen)
                total += 1
    print(total)  # part 2


def hashit(lengths):
    LN = 256
    start = list(range(LN))
    lengths = list(map(ord, lengths))
    lengths += [17, 31, 73, 47, 23]
    pos = 0
    skip = 0
    for _ in range(64):
        for ln in lengths:
            back = max(0, pos - LN)
            back2 = max(0, pos + ln - LN)
            st = start[pos: pos + ln] + start[back: back2]
            st = st[::-1]

            top = LN - pos
            if top < 0:
                top = 999

            start[pos: pos + ln] = st[:top]
            start[back: back2] = st[top:]

            pos += ln + skip
            skip += 1
            pos %= LN

    agg = []
    for i in range(0, 256, 16):
        a = 0
        for c in start[i: i + 16]:
            a ^= c
        agg.append(a)
    return ''.join(f'{a:0>2x}' for a in agg)


main()
