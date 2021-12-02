import collections


def part1(file):
    orb = collections.defaultdict(list)
    for line in file:
        orbited, orbits = line.split(")")
        orb[orbited].append(orbits)

    tot = 0
    for k in orb:
        stack = collections.deque([k])
        while stack:
            t = stack.pop()
            if t in orb:
                tot += len(orb[t])
                stack.extend(orb[t])

    return tot


def part2(file):
    orb = collections.defaultdict(list)
    for line in file:
        orbited, orbits = line.split(")")
        orb[orbited].append(orbits)
        orb[orbits].append(orbited)

    # you => "DRN"
    # san => "C5D"
    # This is specific to my input. Sorry!
    queue = collections.deque([("DRN", 0)])
    GOAL = "C5D"
    seen = set()
    while queue:
        t, d = queue.popleft()
        if t in seen:
            continue
        seen.add(t)
        if t == GOAL:
            return d
        queue.extend((p, d + 1) for p in orb[t])


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
