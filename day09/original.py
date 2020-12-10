import collections


def part1(file):
    queue = collections.deque(maxlen=25)
    file = iter(map(int, file))
    for _ in range(25):
        queue.append(next(file))

    for x in file:
        for q in queue:
            if x - q in queue:
                break
        else:
            return x
        queue.append(x)


def part2(file):
    file = list(map(int, file))
    goal = 26134589
    start = 0
    for end, num in enumerate(file, 1):
        goal -= num
        while goal < 0:
            goal += file[start]
            start += 1
        if goal == 0:
            return min(file[start:end]) + max(file[start:end])


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
