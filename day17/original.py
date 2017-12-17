import blist  # https://pypi.python.org/pypi/blist/?


def part1():
    jmp = 337

    pos = 0
    buff = blist.blist([0])
    for i in range(1, 2018):
        pos = ((pos + jmp) % len(buff)) + 1
        buff.insert(pos, i)
    return buff[pos + 1]


def part2():
    # this is a dumb brute-force solution, there are better solutions.
    jmp = 337

    pos = 0
    buff = blist.blist([0])
    for i in range(1, 50000001):
        pos = ((pos + jmp) % len(buff)) + 1
        buff.insert(pos, i)
    return buff[buff.index(0) + 1]


print(part1())
print(part2())  # takes ~106s to run
