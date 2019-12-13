import collections
import time

HALT = "halt"


class Tape:
    def __init__(self, memory, input_value=None):
        self.relative_base = 0
        self.input_value = input_value
        self._memory = collections.defaultdict(int, enumerate(memory))
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

        parameters = [self._memory[v] for v in range(head, head + num_parameters)]
        assert len(parameters) == num_parameters

        # Translate parameters to position mode or immediate mode based on the opcode.
        # Do not translate the last parameter when `write=True`.
        for param_idx, param in enumerate(parameters):
            is_write_param = param_idx == num_parameters - 1 and write
            check = 10 ** (param_idx + 2)
            mode_flag = (opcode // check) % 10

            # position mode
            if mode_flag == 0:
                if not is_write_param:
                    parameters[param_idx] = self._memory[param]
            # relative mode
            elif mode_flag == 2:
                if is_write_param:
                    parameters[param_idx] += self.relative_base
                else:
                    parameters[param_idx] = self._memory[param + self.relative_base]

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
            if result is not None:
                yield result


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
    return val


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


@register_opcode(9)
def set_relative_base(tape):
    [first] = tape.grab_parameters(1)
    tape.relative_base += first


@register_opcode(99)
def halt(tape):
    return HALT


def display(board):
    lookup = {
        0: ".",
        1: "#",
        2: "$",
        3: "=",
        4: "o",
        None: " ",
    }
    build = []
    for y in range(0, 25):
        for x in range(0, 100):
            build.append(lookup[board.get((x, y))])
        build.append("\n")
    print(board['score'])
    print(''.join(build))
    time.sleep(0.01)


def visualize(memory):
    memory[0] = 2
    tape = Tape(memory, input_value=0)
    outputs = tape.run()
    tiles = {}
    paddle_x = 17
    for _ in range(35 * 25):
        x = next(outputs)
        y = next(outputs)
        v = next(outputs)
        tiles[x, y] = v

    try:
        while True:
            v = 0
            while v == 0:
                x = next(outputs)
                y = next(outputs)
                v = next(outputs)
                if x == -1:
                    tiles["score"] = v
                else:
                    tiles[x, y] = v

            if v == 4:
                if x < paddle_x:
                    tape.input_value = -1
                    paddle_x -= 1
                elif x > paddle_x:
                    tape.input_value = 1
                    paddle_x += 1
                else:
                    tape.input_value = 0

            display(tiles)
    except StopIteration:
        pass


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, file[0].split(',')))
    visualize(list(file))
