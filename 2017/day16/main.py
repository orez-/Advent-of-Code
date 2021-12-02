import collections
import itertools


def dance(pos, file):
    for line in file:
        first = line[0]
        line = line[1:]
        if first == 's':
            num = int(line)
            pos[:] = pos[-num:] + pos[:-num]
        elif first == 'x':
            a, b = map(int, line.split('/'))
            pos[a], pos[b] = pos[b], pos[a]
        elif first == 'p':
            a, b = line.split('/')
            ai = pos.index(a)
            bi = pos.index(b)
            pos[ai], pos[bi] = pos[bi], pos[ai]
    return ''.join(pos)


def part1(file):
    return ''.join(dance(list('abcdefghijklmnop'), file))


def part2(file):
    s = 'abcdefghijklmnop'
    pos = list(s)
    seen = collections.deque([s])
    for i in itertools.count(1):
        res = dance(pos, file)
        if res == s:
            return seen[1_000_000_000 % i]
        else:
            seen.append(res)


if __name__ == '__main__':
    with open('file.txt', 'r') as f:
        file = f.read().strip().split(',')

    print(part1(file))
    print(part2(file))
