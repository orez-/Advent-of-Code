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


reverse_transform = sorted((
    (value, key)
    for key, values in transformations.items()
    for value in values
), key=lambda k_v: -len(k_v[0]))


dead_end = set()
def go(base, s=0):
    if base == 'e':
        return s
    if base in dead_end:
        return False

    print(len(dead_end), base)
    for k, v in reverse_transform:
        for match in re.finditer(k, base):
            interpolate = "{}{}{}".format(base[:match.start()], v, base[match.end():])
            result = go(interpolate, s + 1)
            if result:
                return result
            break
    dead_end.add(base)

print(go(compound))
