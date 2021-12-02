import collections
import itertools
import re
import sys

rules = collections.defaultdict(dict)
r = re.compile(r"(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+)")
for line in sys.stdin:
    actor, direction, amount, against = r.match(line).groups()
    rules[actor][against] = int(amount) * (1 if direction == 'gain' else -1)

rules['me'] = collections.defaultdict(int)

def perms():
    for choice in itertools.permutations(rules):
        yield zip(choice, choice[1:] + choice[:1])

print max(
    sum(
        rules[l].get(r, 0)
        for left, right in ring
        for l, r in ((left, right), (right, left))
    ) for ring in perms()
)
