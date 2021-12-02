import collections


file = """
set b 65
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23
""".strip().split('\n')


def getval(regs, val):
    try:
        return int(val)
    except:
        return regs[val]


def main(file):
    regs = collections.Counter()
    i = 0
    c = 0
    while i < len(file):
        line = file[i]
        cmd, *rest = line.split()
        if cmd == 'set':
            x, y = rest
            regs[x] = getval(regs, y)
        elif cmd == 'add':
            x, y = rest
            regs[x] += getval(regs, y)
        elif cmd == 'sub':
            x, y = rest
            regs[x] -= getval(regs, y)
        elif cmd == 'mul':
            c += 1
            x, y = rest
            regs[x] *= getval(regs, y)
        elif cmd == 'jnz':
            x, y = rest
            if getval(regs, x) != 0:
                i += getval(regs, y)
                continue
        else:
            raise Exception(line)
        i += 1
    return c


print(main(file))
