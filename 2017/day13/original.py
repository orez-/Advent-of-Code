import itertools


file = """
0: 5
1: 2
2: 3
4: 4
6: 6
8: 4
10: 6
12: 10
14: 6
16: 8
18: 6
20: 9
22: 8
24: 8
26: 8
28: 12
30: 12
32: 8
34: 8
36: 12
38: 14
40: 12
42: 10
44: 14
46: 12
48: 12
50: 24
52: 14
54: 12
56: 12
58: 14
60: 12
62: 14
64: 12
66: 14
68: 14
72: 14
74: 14
80: 14
82: 14
86: 14
90: 18
92: 17
""".strip().split('\n')
# depth, range

def part1(file):
    scanners = dict(
        map(int, line.split(': '))
        for line in file
    )

    # 2 -> 2
    # 3 -> 4
    # 4 -> 6

    sev = 0
    for i in range(93):
        if i not in scanners:
            continue
        r = scanners[i]
        if i % (r * 2 - 2) == 0:
            sev += i * r
    print(sev)


def part2(file):
    scanners = dict(
        map(int, line.split(': '))
        for line in file
    )

    for k, v in scanners.items():
        scanners[k] = v * 2 - 2

    for d in itertools.count(0):
        for key, value in scanners.items():
            if (key + d) % value == 0:
                break
        else:
            print(d)
            break


part1(file)
part2(file)  # takes ~3 seconds
