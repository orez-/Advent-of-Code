import itertools

HALT = "halt"


class Tape:
    def __init__(self, memory, phase, signal=None):
        self.phase = phase
        self.signal = signal
        self._memory = list(memory)
        self._head_address = 0

    def set_signal(self, signal):
        if self.signal is not None:
            raise Exception(self.signal)
        self.signal = signal

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

    def run_to_output(self):
        while True:
            code = self.head() % 100
            result = opcodes[code](self)
            if result == HALT:
                return None
            elif result is not None:
                return result


def print_tape(tape):
    af = '\x1b[38;5;{}m'.format
    clear = '\x1b[0m'
    display = ", ".join(
        (af(2) if i == tape._head_address else "") + str(num) + clear
        for i, num in enumerate(tape._memory)
    )
    print(f"[{display}]")


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
    if tape.phase is not None:
        tape[reg] = tape.phase
        tape.phase = None
    elif tape.signal is not None:
        tape[reg] = tape.signal
        tape.signal = None
    else:
        raise Exception("?")


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


@register_opcode(99)
def halt(tape):
    return HALT


def part1(memory):
    best_signal = 0
    for order in itertools.permutations(range(5)):
        signal = 0
        for phase in order:
            tape = Tape(memory, phase=phase, signal=signal)
            signal = tape.run_to_output()
        best_signal = max(signal, best_signal)
    return best_signal


def run_feedback_loop(tapes):
    signal = 0
    last_signal = 0
    while True:
        for tape in tapes:
            tape.set_signal(signal)
            signal = tape.run_to_output()
            if signal is None:
                return last_signal
        last_signal = signal


def part2(memory):
    best_signal = 0
    for order in itertools.permutations(range(5, 10)):
        signal = run_feedback_loop([Tape(memory, phase=phase) for phase in order])
        best_signal = max(signal, best_signal)

    return best_signal


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, file[0].split(',')))
    print(part1(list(file)))
    print(part2(list(file)))
