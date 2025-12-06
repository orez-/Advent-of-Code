import functools
import sys

def split(list_):
    out = []
    for elem in list_:
        if elem:
            out.append(elem)
        else:
            yield out
            out = []
    yield out

*nums, ops = (line.rstrip('\n') for line in sys.stdin.readlines())
ops = ops.split()[::-1]
eqns = [''.join(n).strip() for n in zip(*nums)][::-1]
eqns = split(eqns)

out = sum(
    functools.reduce(int.__add__ if op == '+' else int.__mul__, map(int, nums))
    for op, nums in zip(ops, eqns)
)
print(out)
