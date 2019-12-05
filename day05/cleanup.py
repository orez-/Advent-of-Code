HALT = "halt"


class Tape:
    def __init__(self, memory, input_value=None):
        self.input_value = input_value
        self._memory = memory
        self._head_address = 0

    def head(self):
        return self._memory[self._head_address]

    def grab_parameters(self, num_parameters, *, write=False):
        """
        Return the next `num_parameters` opcodes from the head (skipping the current opcode),
        and advance the head past them.

        If the last parameter is the register to write the output to, pass `write=True`.
        This will return the last register without converting it.
        """
        opcode = self.head()
        head = self._head_address + 1
        self.jump_abs(head + num_parameters)

        parameters = self._memory[head : head + num_parameters]

        # Translate parameters to position mode or immediate mode based on the opcode.
        # Do not translate the last parameter when `write=True`.
        for param_idx, param in enumerate(parameters[: num_parameters - write]):
            check = 10 ** (param_idx + 2)
            mode_flag = (opcode // check) % 10

            # position mode
            if not mode_flag:
                parameters[param_idx] = self._memory[param]

        return parameters

    def jump_abs(self, address):
        self._head_address = address

    def __getitem__(self, address):
        return self._memory[address]

    def __setitem__(self, address, value):
        self._memory[address] = value

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
    left, right, output_reg = tape.grab_parameters(3, write=True)
    tape[output_reg] = left + right


@register_opcode(2)
def multiply(tape):
    left, right, output_reg = tape.grab_parameters(3, write=True)
    tape[output_reg] = left * right


@register_opcode(3)
def input_(tape):
    [reg] = tape.grab_parameters(1, write=True)
    tape[reg] = tape.input_value


@register_opcode(4)
def output_value(tape):
    [val] = tape.grab_parameters(1)
    print(val)


@register_opcode(5)
def jump_if_true(tape):
    condition, jump = tape.grab_parameters(2)

    if condition:
        tape.jump_abs(jump)


@register_opcode(6)
def jump_if_false(tape):
    condition, jump = tape.grab_parameters(2)

    if not condition:
        tape.jump_abs(jump)


@register_opcode(7)
def less_than(tape):
    first, second, output = tape.grab_parameters(3, write=True)
    tape[output] = int(first < second)


@register_opcode(8)
def equals(tape):
    first, second, output = tape.grab_parameters(3, write=True)
    tape[output] = int(first == second)


@register_opcode(99)
def halt(tape):
    return HALT


def part1(memory):
    tape = Tape(memory, input_value=1)
    tape.run()


def part2(memory):
    tape = Tape(memory, input_value=5)
    tape.run()


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, file[0].split(',')))
    part1(list(file))
    part2(list(file))
