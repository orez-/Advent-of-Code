import collections
import itertools
import re


def run_asm(a):
    registers = {'a': a, 'b': 0, 'c': 0, 'd': 0}
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
        elif line.startswith('out'):
            _, y = line.split()
            try:
                y = int(y)
            except ValueError:
                y = registers[y]
            yield y
        else:
            print("SKIPPING", line)
        i += 1
    # print(registers['a'])


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        instructions = list(map(str.strip, file))
    comp = [0, 1, 0, 1, 0, 1, 0, 1]
    for i in itertools.count(1):
        slce = list(itertools.islice(run_asm(i), len(comp)))

        if i % 10 == 0:
            print(i, slce)
        if slce == comp:
            print("\n\n\n\n!!!", i, slce, "\n\n\n\n")
