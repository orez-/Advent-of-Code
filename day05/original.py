HALT = "halt"
INPUT = None


class Tape:
    def __init__(self, memory):
        self.memory = memory
        self.head_address = 0

    def head(self):
        return self.memory[self.head_address]

    def grab_parameters(self, num_parameters):
        """
        Return the next `num_parameters` opcodes from the head (AND the current opcode),
        and advance the head past them.
        """
        head = self.head_address
        self.jump_abs(head + num_parameters + 1)
        return self.memory[head : head + num_parameters + 1]

    def jump_abs(self, address):
        self.head_address = address

    def __getitem__(self, address):
        return self.memory[address]

    def __setitem__(self, address, value):
        self.memory[address] = value

    def run(self):
        while True:
            code = self.head() % 100
            result = opcodes[code](self)
            if result == HALT:
                return


opcodes = {}


def register_opcode(code):
    def decorator(fn):
        opcodes[code] = fn

    return decorator


@register_opcode(1)
def add(tape):
    opcode, left_reg, right_reg, output_reg = tape.grab_parameters(3)
    left = left_reg if (opcode // 100) % 10 else tape[left_reg]
    right = right_reg if opcode >= 1000 else tape[right_reg]
    tape[output_reg] = left + right


@register_opcode(2)
def multiply(tape):
    opcode, left_reg, right_reg, output_reg = tape.grab_parameters(3)
    left = left_reg if (opcode // 100) % 10 else tape[left_reg]
    right = right_reg if opcode >= 1000 else tape[right_reg]
    tape[output_reg] = left * right


@register_opcode(3)
def input_(tape):
    opcode, reg = tape.grab_parameters(1)
    tape[reg] = INPUT


@register_opcode(4)
def output(tape):
    opcode, val = tape.grab_parameters(1)
    val = val if opcode >= 100 else tape[val]
    print(val)


@register_opcode(5)
def jump_if_true(tape):
    opcode, condition, jump = tape.grab_parameters(2)
    if not ((opcode // 100) % 10):
        condition = tape[condition]
    if opcode < 1000:
        jump = tape[jump]

    if condition:
        tape.jump_abs(jump)


@register_opcode(6)
def jump_if_false(tape):
    opcode, condition, jump = tape.grab_parameters(2)
    if not ((opcode // 100) % 10):
        condition = tape[condition]
    if opcode < 1000:
        jump = tape[jump]

    if not condition:
        tape.jump_abs(jump)


@register_opcode(7)
def less_than(tape):
    opcode, first, second, third = tape.grab_parameters(3)
    if not ((opcode // 100) % 10):
        first = tape[first]
    if opcode < 1000:
        second = tape[second]

    tape[third] = int(first < second)


@register_opcode(8)
def equals(tape):
    opcode, first, second, third = tape.grab_parameters(3)
    if not ((opcode // 100) % 10):
        first = tape[first]
    if opcode < 1000:
        second = tape[second]

    tape[third] = int(first == second)


@register_opcode(99)
def halt(tape):
    return HALT


def part1(memory):
    global INPUT
    INPUT = 1
    tape = Tape(memory)
    tape.run()


def part2(memory):
    global INPUT
    INPUT = 5
    tape = Tape(memory)
    tape.run()


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, file[0].split(',')))
    part1(list(file))
    part2(list(file))
