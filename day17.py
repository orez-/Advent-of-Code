import itertools


containers = [11,30,47,31,32,36,3,1,5,3,32,36,15,11,46,26,28,1,19,3]

weight = 150


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


# part 1
# x = 0
# for p in powerset(containers):
#     if sum(p) == weight:
#         x += 1
# print x

# part 2
min_val = 9999999999
t = 0

for p in powerset(containers):
    if sum(p) == weight:
        if len(p) < min_val:
            t = 1
            min_val = len(p)
        elif len(p) == min_val:
            t += 1
print t
