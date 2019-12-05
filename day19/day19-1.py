import collections
import re
import sys


transformations = collections.defaultdict(list)
compound = None

for line in sys.stdin:
    match = re.match(r'(\w+) => (\w+)', line)
    if not match:
        compound = line.strip()
    else:
        key, value = match.groups()
        transformations[key].append(value)


def one_replace(base):
    for key, values in transformations.items():
        for match in re.finditer(key, base):
            interpolate = "{}{{}}{}".format(base[:match.start()], base[match.end():])
            for v in values:
                yield interpolate.format(v)

print(len(set(one_replace(compound))))
