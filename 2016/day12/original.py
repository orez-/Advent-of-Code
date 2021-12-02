import collections
import itertools
import re


if __name__ == '__main__':
    registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    with open('input.txt', 'r') as file:
        instructions = list(file)
        jump = 0
        while True:
            for i, line in enumerate(instructions[jump:], jump):
                line = line.strip()
                if line.startswith('cp'):
                    _, x, y = line.split()
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
                elif line.startswith('jnz'):
                    _, x, y = line.split()

                    try:
                        r = int(x)
                    except:
                        r = registers[x]

                    if r:
                        y = int(y)
                        jump = i + y
                        break
            else:
                break
    print(registers['a'])
