import collections


def getval(regs, val):
    try:
        return int(val)
    except:
        return regs[val]


def run(file, regs):
    s = 0
    i = 0

    ln = len(file)
    while i < ln:
        line = file[i]
        cmd, *rest = line.split()
        if cmd == 'snd':
            x, = rest
            yield getval(regs, x)
        elif cmd == 'set':
            x, y = rest
            regs[x] = getval(regs, y)
        elif cmd == 'add':
            x, y = rest
            regs[x] += getval(regs, y)
        elif cmd == 'mul':
            x, y = rest
            regs[x] *= getval(regs, y)
        elif cmd == 'mod':
            x, y = rest
            regs[x] %= getval(regs, y)
        elif cmd == 'rcv':
            x, = rest
            regs[x] = yield 'rcv'
        elif cmd == 'jgz':
            x, y = rest
            if getval(regs, x) > 0:
                i += getval(regs, y)
                continue
        else:
            raise Exception(line)
        i += 1
    return s


def part2(file):
    r0 = run(file, collections.Counter())
    r1 = run(file, collections.Counter('p'))

    q0 = collections.deque()
    q1 = collections.deque()

    v0 = next(r0)
    v1 = next(r1)
    s = 0
    # Only checks for deadlocks, but fortunately that's the thing that happens.
    while not (v0 == 'rcv' and v1 == 'rcv' and not q0 and not q1):
        if v0 == 'rcv':
            if q0:
                v0 = r0.send(q0.popleft())
        else:
            q1.append(v0)
            v0 = next(r0)

        if v1 == 'rcv':
            if q1:
                v1 = r1.send(q1.popleft())
        else:
            s += 1
            q0.append(v1)
            v1 = next(r1)
    return s


if __name__ == '__main__':
    with open('file.txt', 'r') as f:
        file = list(f)
    print(part2(file))
