# TODAY SUCKED DON'T LOOK AT THIS CODE

import collections
import functools
import itertools
import operator
import sys

weights = list(reversed(list(int(line.strip()) for line in sys.stdin)))
goal = sum(weights) // 4


prod = lambda p: functools.reduce(operator.mul, p, 1)

def smallest_ways(weights, goal, offset=0):
    weights = list(weights)
    q = collections.deque([(goal, 0, [])])
    while q:
        goal, offset, lst = q.popleft()

        for i, w in enumerate(itertools.islice(weights, offset, None), offset + 1):
            if w < goal:
                q.append((goal - w, i, lst + [w]))
            elif w == goal:
                yield lst + [w]

# PART 1

# smallest = float('inf')
# min_qe = float('inf')
# for way in smallest_ways(weights, goal):
#     if any(smallest_ways(list(set(weights) - set(way)), goal)):
#         if len(way) < smallest:
#             smallest = len(way)
#             print(way)
#             min_qe = prod(way)
#             print(min_qe)
#         elif len(way) == smallest:
#             qe = prod(way)
#             if qe < min_qe:
#                 print(qe)
#                 min_qe = qe

# PART 2
smallest = float('inf')
min_qe = float('inf')
for way in smallest_ways(weights, goal):
    subweights = set(weights) - set(way)
    for way2 in smallest_ways(subweights, goal):
        if any(smallest_ways(subweights - set(way2), goal)):
            if len(way) < smallest:
                smallest = len(way)
                print(way)
                min_qe = prod(way)
                print(min_qe)
            elif len(way) == smallest:
                qe = prod(way)
                if qe < min_qe:
                    print(qe)
                    min_qe = qe

