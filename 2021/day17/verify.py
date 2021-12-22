import math

af = '\x1b[38;5;{}m{}\x1b[0m'


def de_geo(x):
    return ((8 * x + 1) ** 0.5 - 1) / 2


def one_x(x, time, left, right, c):
    nums = list(range(x - time + 1, x + 1))
    total = sum(nums)
    color = c[left <= total <= right]
    print(af.format(color, f"{x} {total} {nums}"))


def check_x(time, left=201, right=230):
    ldx = (left / time) + (time / 2)
    rdx = (right / time) + (time / 2)
    ldxi = math.ceil(ldx - 0.5)
    rdxi = math.floor(rdx - 0.5)
    print(ldx, rdx)
    one_x(ldxi - 1, time, left, right, "21")
    for x in range(ldxi, rdxi + 1):
        one_x(x, time, left, right, "12")
    one_x(rdxi + 1, time, left, right, "21")
    return rdxi - ldxi + 1


for i in range(1, 23):
    print(i)
    print(check_x(i), "\n")
