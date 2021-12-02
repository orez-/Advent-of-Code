import itertools


def part1(num):
    direction = -1
    count = 1
    x = 0
    y = 0
    i = 1
    while i <= num:
        for _ in range(count):
            i += 1
            x += direction
            if i == num:
                return x, y
        for _ in range(count):
            i += 1
            y += direction
            if i == num:
                return x, y
        direction *= -1
        count += 1


def part2(num):
    direction = -1
    count = 1
    x = 0
    y = 0
    i = 1
    guide = {(0, 0): 1}
    while i <= num:
        for _ in range(count):
            x += direction
            guide[x, y] = sum(
                guide[dx, dy]
                for dx in range(x - 1, x + 2)
                for dy in range(y - 1, y + 2)
                if (dx, dy) in guide
            )
            if guide[x, y] >= num:
                return guide[x, y]
        for _ in range(count):
            y += direction
            guide[x, y] = sum(
                guide[dx, dy]
                for dx in range(x - 1, x + 2)
                for dy in range(y - 1, y + 2)
                if (dx, dy) in guide
            )
            if guide[x, y] >= num:
                return guide[x, y]
        direction *= -1
        count += 1


def generate_map():
    # this sure didn't pan out
    nums = itertools.count(2)
    dumb = [[1]]
    while True:
        next_chunk = list(itertools.islice(nums, len(dumb[0])))
        dumb = list(zip(*dumb[::-1], next_chunk[::-1]))
        if num in next_chunk:
            print(dumb)  # so, what now?
            break


num = 368078

x, y = part1(num)
print(abs(x) + abs(y))
print(part2(num))
