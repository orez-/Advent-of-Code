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


def part1(file):
    regs = [0] * 6
    ip = 5
    while 0 <= regs[ip] < len(file):
        line = file[regs[ip]]
        opcode, a, b, c = line.split()
        a, b, c = map(int, (a, b, c))
        regs[c] = globals()[opcode](regs, a, b)  # gross!
        regs[ip] += 1
    return regs[0]


def part2():
    a = 0
    d = 10551425
    e = 1

    b = 1
    while True:
        if d % b == 0:
            a += b
        b += 1
        if d < b:
            return a


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2())
