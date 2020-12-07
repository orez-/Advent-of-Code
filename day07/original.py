import collections
import functools
import re


def part1(file):
    upwards = collections.defaultdict(list)
    for line in file:
        container, *rest = [r.group(0) for r in re.finditer(r"(\d )?[a-z ]+ bag", line)]
        for r in rest:
            n, _, color = r.partition(' ')
            upwards[color].append(container)

    queue = collections.deque(['shiny gold bag'])
    seen = set()
    while queue:
        t = queue.popleft()
        if t not in upwards:
            continue
        for n in upwards[t]:
            if n in seen:
                continue
            seen.add(n)
            queue.append(n)
    return len(seen)


rules = {}

def part2(file):
    global rules
    for line in file:
        if 'no other' in line:
            container = re.match(r'(.+?)s contain', line).group(1)
            rules[container] = collections.Counter()
            continue
        container, *rest = [r.group(0) for r in re.finditer(r"(\d )?[a-z ]+ bag", line)]
        c = collections.Counter()
        for r in rest:
            n, _, color = r.partition(' ')
            c[color] = int(n)
        rules[container] = c

    return how_many('shiny gold bag') - 1


@functools.lru_cache()
def how_many(container):
    owned = rules[container]

    total = sum(
        how_many(c) * num
        for c, num in owned.items()
    )

    return total + 1


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
