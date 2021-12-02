import re


def get_digits(line):
    return (int(match[0]) for match in re.finditer(r"\d+", line))


def addr(regs, a, b):
    return regs[a] + regs[b]


def addi(regs, a, b):
    return regs[a] + b


def mulr(regs, a, b):
    return regs[a] * regs[b]


def muli(regs, a, b):
    return regs[a] * b


def banr(regs, a, b):
    return regs[a] & regs[b]


def bani(regs, a, b):
    return regs[a] & b


def borr(regs, a, b):
    return regs[a] | regs[b]


def bori(regs, a, b):
    return regs[a] | b


def setr(regs, a, b):
    return regs[a]


def seti(regs, a, b):
    return a


def gtir(regs, a, b):
    return int(a > regs[b])


def gtri(regs, a, b):
    return int(regs[a] > b)


def gtrr(regs, a, b):
    return int(regs[a] > regs[b])


def eqir(regs, a, b):
    return int(a == regs[b])


def eqri(regs, a, b):
    return int(regs[a] == b)


def eqrr(regs, a, b):
    return int(regs[a] == regs[b])


fns = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]


def part1(samples):
    total = 0
    for section in samples:
        before, (inst, a, b, c), after = map(list, map(get_digits, section.split('\n')))
        possible = set()
        for fn in fns:
            regs = list(before)
            regs[c] = fn(regs, a, b)
            if regs == after:
                possible.add(fn)
        if len(possible) >= 3:
            total += 1

    return total


def part2(samples, program):
    possible = [set(fns) for _ in range(16)]

    for section in samples:
        before, (inst, a, b, c), after = map(list, map(get_digits, section.split('\n')))
        for fn in set(possible[inst]):
            regs = list(before)
            regs[c] = fn(regs, a, b)
            if regs != after:
                possible[inst].discard(fn)

    instructions = {}
    progress = True
    while progress:
        progress = False
        for i, pos_fns in enumerate(possible):
            if len(pos_fns) == 1:
                progress = True
                fn, = pos_fns
                instructions[i] = fn
                for them in possible:
                    them.discard(fn)

    regs = [0, 0, 0, 0]
    for line in program:
        opcode, a, b, c = get_digits(line)
        regs[c] = instructions[opcode](regs, a, b)

    return regs[0]


def main():
    with open('samples.txt') as file:
        samples = file.read().strip().split('\n\n')
    with open('program.txt') as file:
        program = file.read().strip().split('\n')
    print(part1(samples))
    print(part2(samples, program))


if __name__ == '__main__':
    main()
