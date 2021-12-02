import collections
import hashlib
import itertools
import re


def main1(num_elves):
    d = collections.deque(range(1, num_elves + 1))
    while len(d) > 1:
        d.rotate(-1)
        d.popleft()
    print(d[0])


# def main2(num_elves):
#     d = list(range(1, num_elves + 1))
#     i = 0
#     while len(d) > 1:
#         to_kill = (i + len(d) // 2) % len(d)
#         print(i, d[to_kill], d)
#         del d[to_kill]
#         if to_kill < i:
#             i -= 1
#         i = (i + 1) % len(d)
#     print(d[i])


# def main2(num_elves):
#     d = collections.deque(range(1, num_elves + 1))
#     while len(d) > 1:
#         if len(d) % 10000 == 0:
#             print(len(d))
#         del d[len(d) // 2]
#         d.rotate(-1)
#     print(d[0])


# 3, 5, 1, 4, 2
def main2(num_elves):
    d = collections.deque(range(1, num_elves + 1))
    d.rotate(num_elves // 2 + 1)
    rotAmt = 0
    while len(d) > 1:
        d.popleft()
        rotAmt = -1 if rotAmt == 0 else 0
        d.rotate(rotAmt)
    print(d[0])


# main2(5)
# main2(31)

main1(3004953)
main2(3004953)
