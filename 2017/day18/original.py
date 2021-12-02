import collections


def getval(regs, val):
    try:
        return int(val)
    except:
        return regs[val]


def part1(file):
    regs = collections.Counter()
    lastsound = 0
    i = 0
    while i < len(file):
        line = file[i]
        cmd, *rest = line.split()
        if cmd == 'snd':
            x, = rest
            lastsound = getval(regs, x)
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
            if getval(regs, x):
                return lastsound
        elif cmd == 'jgz':
            x, y = rest
            if getval(regs, x) > 0:
                i += getval(regs, y)
                continue
        else:
            raise Exception(line)
        i += 1


def part2(file):
    s = 0

    regs1 = collections.Counter()
    regs2 = collections.Counter({'p': 1})  # it took me 20 minutes to write this line
    i = 0
    j = 0

    q1 = collections.deque()
    q2 = collections.deque()

    lock = 0
    ln = len(file)
    while lock != 3:
        lock = 0
        if i < ln:
            line = file[i]
            cmd, *rest = line.split()
            if cmd == 'snd':
                x, = rest
                q2.append(getval(regs1, x))
                i += 1
            elif cmd == 'set':
                x, y = rest
                regs1[x] = getval(regs1, y)
                i += 1
            elif cmd == 'add':
                x, y = rest
                regs1[x] += getval(regs1, y)
                i += 1
            elif cmd == 'mul':
                x, y = rest
                regs1[x] *= getval(regs1, y)
                i += 1
            elif cmd == 'mod':
                x, y = rest
                regs1[x] %= getval(regs1, y)
                i += 1
            elif cmd == 'rcv':
                x, = rest
                if q1:
                    regs1[x] = q1.popleft()
                    i += 1
                else:
                    lock |= 1
            elif cmd == 'jgz':
                x, y = rest
                if getval(regs1, x) > 0:
                    i += getval(regs1, y)
                else:
                    i += 1
            else:
                raise Exception(line)
        else:
            lock |= 1

        if j < ln:
            line = file[j]
            cmd, *rest = line.split()
            if cmd == 'snd':
                x, = rest
                q1.append(getval(regs2, x))
                j += 1
                s += 1
            elif cmd == 'set':
                x, y = rest
                regs2[x] = getval(regs2, y)
                j += 1
            elif cmd == 'add':
                x, y = rest
                regs2[x] += getval(regs2, y)
                j += 1
            elif cmd == 'mul':
                x, y = rest
                regs2[x] *= getval(regs2, y)
                j += 1
            elif cmd == 'mod':
                x, y = rest
                regs2[x] %= getval(regs2, y)
                j += 1
            elif cmd == 'rcv':
                x, = rest
                if q2:
                    regs2[x] = q2.popleft()
                    j += 1
                else:
                    lock |= 2
            elif cmd == 'jgz':
                x, y = rest
                if getval(regs2, x) > 0:
                    j += getval(regs2, y)
                else:
                    j += 1
            else:
                raise Exception(line)
        else:
            lock |= 2
    return s


if __name__ == '__main__':
    with open('file.txt', 'r') as f:
        file = list(f)
    print(part1(file))
    print(part2(file))
