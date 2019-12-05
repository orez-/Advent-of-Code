import json
import re

n = raw_input()

# part 1
# print sum(map(int, re.findall(r'(?:\b|\-)\d+\b', n)))

# part 2
def traverse(obj):
    if isinstance(obj, list):
        return sum(traverse(e) for e in obj)
    if isinstance(obj, dict):
        if 'red' in obj.values():
            return 0
        return sum(traverse(e) for e in obj.values())
    if isinstance(obj, int):
        return obj
    return 0

print traverse(json.loads(n))
