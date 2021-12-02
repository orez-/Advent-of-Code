import itertools
import re


def get_digits(line):
    return (int(match.group(0)) for match in re.finditer(r"-?\d+", line))


def combine(guy1, guy2):
    total = []
    for g1, g2 in zip(guy1, guy2):
        total.append( list(map(sum, zip(g1, g2))) )
    return total


def part1(file):
    planets = list(map(list, map(get_digits, file)))
    velocities = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for _ in range(1000):
        updates = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for a, b in itertools.permutations(range(4), r=2):
            updates[a] = list(map(sum, zip([
                (0 if va == vb else
                (1 if va < vb else -1))
                for va, vb in zip(planets[a], planets[b])
            ], updates[a])))
        velocities = combine(velocities, updates)
        planets = combine(velocities, planets)
    potential = [sum([abs(c) for c in vs]) for vs in planets]
    kinetic = [sum([abs(c) for c in vs]) for vs in velocities]
    return sum([p * k for p, k in zip(potential, kinetic)])


def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)


def part2(file):
    planets = list(map(list, map(get_digits, file)))
    velocities = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    goalx = tuple(v[0] for v in velocities), tuple(v[0] for v in planets)
    goaly = tuple(v[1] for v in velocities), tuple(v[1] for v in planets)
    goalz = tuple(v[2] for v in velocities), tuple(v[2] for v in planets)

    xper = yper = zper = None

    for i in itertools.count(1):
        updates = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for a, b in itertools.permutations(range(4), r=2):
            updates[a] = list(map(sum, zip([
                (0 if va == vb else
                (1 if va < vb else -1))
                for va, vb in zip(planets[a], planets[b])
            ], updates[a])))
        velocities = combine(velocities, updates)
        planets = combine(velocities, planets)

        keyx = tuple(v[0] for v in velocities), tuple(v[0] for v in planets)
        keyy = tuple(v[1] for v in velocities), tuple(v[1] for v in planets)
        keyz = tuple(v[2] for v in velocities), tuple(v[2] for v in planets)

        if keyx == goalx and not xper:
            xper = i
        if keyy == goaly and not yper:
            yper = i
        if keyz == goalz and not zper:
            zper = i
        if xper and yper and zper:
            break

    return int(lcm(lcm(xper, yper), zper))


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
