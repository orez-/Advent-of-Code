gen_a = 16807
gen_b = 48271
div = 2147483647
mask = 2 ** 16 - 1


def do_while(fn):
    yield
    while fn():
        yield


def part1():
    ga = 512
    gb = 191
    total = 0
    for i in range(40_000_000):
        ga *= gen_a
        ga %= div
        gb *= gen_b
        gb %= div
        if ga & mask == gb & mask:
            total += 1
    print(total)


def part2():
    ga = 512
    gb = 191
    total = 0
    for i in range(5_000_000):
        for _ in do_while(lambda: ga % 4 != 0):
            ga *= gen_a
            ga %= div
        for _ in do_while(lambda: gb % 8 != 0):
            gb *= gen_b
            gb %= div
        if ga & mask == gb & mask:
            total += 1
    print(total)


# Today is Very Slow!
part1()  # ~34s
part2()  # ~46s
