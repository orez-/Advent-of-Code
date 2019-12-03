def main1(file):
    ranges = set()
    for line in file:
        start, end = map(int, line.strip().split('-'))
        ranges.add(range(start, end + 1))

    print(ranges)
    ran = iter(sorted(ranges, key=lambda r: r.start))
    cur_ran = next(ran)
    print(cur_ran)
    i = 0
    while True:
        if i % 1000 == 0:
            print(i, '...')
        print(cur_ran)
        if i in cur_ran:
            i = cur_ran.stop
            stop = cur_ran.stop
            while cur_ran.stop <= stop:
                cur_ran = next(ran)
        else:
            return i


def main2(file):
    ranges = set()
    for line in file:
        start, end = map(int, line.strip().split('-'))
        ranges.add(range(start, end + 1))

    print(ranges)
    ran = iter(sorted(ranges, key=lambda r: r.start))
    cur_ran = next(ran)
    print(cur_ran)
    i = 0
    total = 0
    try:
        while True:
            if i % 1000 == 0:
                print(i, '...')
            print(cur_ran)
            i = cur_ran.stop
            stop = cur_ran.stop
            while cur_ran.stop <= stop:
                cur_ran = next(ran)
            total += max(0, cur_ran.start - i)
    except StopIteration:
        return total


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        # print(main1(file))
        print(main2(file))
