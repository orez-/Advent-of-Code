import collections
import re


def part1():
    x = 0
    for i in range(367479, 893698 + 1):
        if re.search(r"(\d)\1", str(i)) and list(str(i)) == sorted(str(i)):
            x += 1
    return x


def part2():
    x = 0
    for i in range(367479, 893698 + 1):
        y = collections.Counter(str(i))
        has = any(z == 2 for z in y.values())
        if has and list(str(i)) == sorted(str(i)):
            x += 1
    return x


if __name__ == '__main__':
    print(part1())
    print(part2())
