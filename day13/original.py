import collections
import functools
import hashlib
import itertools
import math
import re


def part1(file):
    could_depart = 1001938
    cs = []
    for c in file[0].split(','):
        if c == 'x':
            continue
        c = int(c)
        cs.append(c)

    for i in itertools.count(could_depart):
        for c in cs:
            if i % c == 0:
                return c * (i - could_depart)


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def part2(file):
    cs = []
    for i, c in enumerate(file[0].split(',')):
        if c == 'x':
            continue
        c = int(c)
        cs.append((i, c))

    cs = iter(cs)
    start, lcm_value = next(cs)
    for i, c in cs:
        for t in itertools.count(0):
            t = t * lcm_value + start
            if (t + i) % c == 0:
                start = t
                lcm_value = lcm(lcm_value, c)
                break
    return start


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
