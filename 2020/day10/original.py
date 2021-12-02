import collections


def part1(file):
    js = sorted(map(int, file))
    three = 1
    one = 1
    for j1, j2 in zip(js, js[1:]):
        if j2 - j1 == 3:
            three += 1
        elif j2 - j1 == 1:
            one += 1
    return one * three


def part2(file):
    js = sorted(map(int, file))
    ways = {0: 1}
    trailing = collections.deque([0], maxlen=3)

    for j in js:
        while trailing[0] + 3 < j:
            trailing.popleft()
        total = 0
        for t in trailing:
            total += ways[t]
        ways[j] = total
        trailing.append(j)
    return ways[js[-1]]


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
