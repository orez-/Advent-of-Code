import collections
import itertools
import re


if __name__ == '__main__':
    # part 1: 7
    # part 2: 12
    registers = {'a': 12, 'b': 0, 'c': 0, 'd': 0}
    with open('input.txt', 'r') as file:
        instructions = list(map(str.strip, file))
        jump = 0
        i = 0
        while i < len(instructions):
            line = instructions[i]
            if line.startswith('cpy'):
                _, x, y = line.split()
                if y not in registers:
                    i += 1
                    continue
                try:
                    registers[y] = int(x)
                except:
                    registers[y] = registers[x]
            elif line.startswith('inc'):
                _, x = line.split()
                registers[x] += 1
            elif line.startswith('dec'):
                _, x = line.split()
                registers[x] -= 1
                if registers[x] < 0:
                    print(x, registers[x])
                    raise Exception("this is probably wrong.")
            elif line.startswith('jnz'):
                # if x is not zero, jump y
                _, x, y = line.split()

                try:
                    r = int(x)
                except:
                    r = registers[x]

                if r:
                    try:
                        y = int(y)
                    except ValueError:
                        y = registers[y]
                    i += y
                    continue
            elif line.startswith('tgl'):
                _, z = line.split()
                try:
                    z = int(z)
                except ValueError:
                    z = registers[z]
                try:
                    instr = instructions[i + z]
                except IndexError:
                    i += 1
                    continue
                print("toggle line", i + z, ':', instr)
                if instr.startswith('inc'):
                    _, q = instr.split()
                    instr = 'dec ' + q
                elif instr.startswith(('dec', 'tgl')):
                    _, q = instr.split()
                    instr = 'inc ' + q
                elif instr.startswith('jnz'):
                    _, x, y = instr.split()
                    instr = 'cpy {} {}'.format(x, y)
                elif instr.startswith('cpy'):
                    _, x, y = instr.split()
                    instr = 'jnz {} {}'.format(x, y)
                else:
                    raise Exception(instr)
                instructions[i + z] = instr
            elif line.startswith('mul'):
                # a += b * c
                _, a, b, c = line.split()
                registers[a] = registers[b] * registers[c]
            elif line.startswith('add'):
                # a += b
                _, b, a = line.split()
                assert registers[b] > 0
                registers[a] += registers[b]
                registers[b] = 0
            elif line.startswith('nop'):
                pass
            else:
                print("SKIPPING", line)
            i += 1
    print(registers['a'])
