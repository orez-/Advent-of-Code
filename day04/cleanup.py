"""
Basically identical to `original.py`, just everything's named better
and we only `str`ify the password once.
"""

import collections
import re


RANGE = range(367479, 893698 + 1)


def part1():
    num_matches = 0
    for password in RANGE:
        password = str(password)
        if re.search(r"(\d)\1", password) and list(password) == sorted(password):
            num_matches += 1
    return num_matches


def part2():
    num_matches = 0
    for password in RANGE:
        password = str(password)
        digit_count = collections.Counter(password)
        has_exactly_double = any(count == 2 for count in digit_count.values())
        if has_exactly_double and list(password) == sorted(password):
            num_matches += 1
    return num_matches


if __name__ == '__main__':
    print(part1())
    print(part2())
