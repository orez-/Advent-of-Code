import collections


file = """
31/13
34/4
49/49
23/37
47/45
32/4
12/35
37/30
41/48
0/47
32/30
12/5
37/31
7/41
10/28
35/4
28/35
20/29
32/20
31/43
48/14
10/11
27/6
9/24
8/28
45/48
8/1
16/19
45/45
0/4
29/33
2/5
33/9
11/7
32/10
44/1
40/32
2/45
16/16
1/18
38/36
34/24
39/44
32/37
26/46
25/33
9/10
0/29
38/8
33/33
49/19
18/20
49/39
18/39
26/13
19/32
""".strip().split('\n')


def part1(start):
    q = collections.deque([(0, start, 0)])
    while q:
        nxt, pins, ttl = q.popleft()

        p = 0
        for (k1, k2), v in pins.items():
            if not v:
                continue
            if k1 == nxt:
                p = 1
                tmp = collections.Counter(pins)
                tmp[k2, k1] -= 1
                tmp[k1, k2] -= 1
                q.append((k2, tmp, ttl + k2 + k1))
        if not p:
            yield ttl


def part2(start):
    q = collections.deque([(0, start, 0, 0)])
    while q:
        nxt, pins, ttl, ll = q.popleft()

        p = 0
        for (k1, k2), v in pins.items():
            if not v:
                continue
            if k1 == nxt:
                p = 1
                tmp = collections.Counter(pins)
                tmp[k2, k1] -= 1
                tmp[k1, k2] -= 1
                q.append((k2, tmp, ttl + k2 + k1, ll + 1))
        if not p:
            yield ll, ttl


def main(file):
    pins = collections.Counter()
    for line in file:
        x, y = map(int, line.split('/'))
        pins[x, y] += 1
        pins[y, x] += 1

    # Both parts run in ~21s total in pypy (double that for cpython)
    # This is the wrong data structure for the job, but it got the job done.
    print(max(part1(pins)))
    print(max(part2(pins))[1])


main(file)
