import itertools
import re
import sys

towns = set()
distances = {}

for line in sys.stdin.readlines():
    town1, town2, distance = re.match(r'(\w+) to (\w+) = (\d+)', line).groups()
    towns.add(town1)
    towns.add(town2)
    town1, town2 = sorted((town1, town2))
    distances[(town1, town2)] = int(distance)

options = []
for order in itertools.permutations(towns):
    path = zip(order, order[1:])
    options.append(sum(
        distances[tuple(sorted((town1, town2)))]
        for town1, town2 in path
    ))
print max(options)
