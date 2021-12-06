import collections
import sys

ages = collections.Counter(map(int, sys.stdin.read().split(',')))
queue = collections.deque()

DAYS = 80 if sys.argv[1] == 'part1' else 256

for i in range(DAYS):
    count = ages[i % 7]
    queue.append(((i + 2) % 7, count))
    if len(queue) == 3:
        k, v = queue.popleft()
        ages[k] += v

for k, v in queue:
    ages[k] += v

print(sum(ages.values()))
