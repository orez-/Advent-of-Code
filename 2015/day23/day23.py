import re
import sys


registers = {'a': 0, 'b': 0}

text_instructions = [
    re.match(r'(\w+) ([+-]?\w+)(?:, ([+-]\d+))?', inst).groups()
    for inst in sys.stdin
]

def instructions(text_instructions):
    offset = 0
    while True:
        if offset < 0:
            return
        for i, inst in enumerate(text_instructions[offset:], offset):
            offset = yield inst
            if offset is not None:
                yield
                offset += i
                break
        else:
            break

def run():
    inst = instructions(text_instructions)

    for cmd, arg1, arg2 in inst:
        if cmd == 'hlf':
            registers[arg1] //= 2
        elif cmd == 'tpl':
            registers[arg1] *= 3
        elif cmd == 'inc':
            registers[arg1] += 1
        elif cmd == 'jmp':
            inst.send(int(arg1))
        elif cmd == 'jie':
            if registers[arg1] % 2 == 0:
                inst.send(int(arg2))
        elif cmd == 'jio':
            if registers[arg1] == 1:
                inst.send(int(arg2))

run()
print(registers['b'])
