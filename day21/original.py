from intcode import Tape


def part1(file):
    program = (
        "NOT C J\n"
        "AND D J\n"
        "NOT A T\n"
        "OR T J\n"
        "WALK\n"
    )
    # not C and D OR not A
    tape = Tape.from_file(file)
    tape.input_extend(program)
    # print(''.join(map(chr, tape.run())))
    return list(tape.run())[-1]


def part2(file):
    program = (
        "NOT C J\n"
        "AND D J\n"
        "AND H J\n"
        "NOT B T\n"
        "AND D T\n"
        "OR T J\n"
        "NOT A T\n"
        "OR T J\n"
        "RUN\n"
    )

    # ((not C and D) AND H) OR (not B and D) OR not A
    tape = Tape.from_file(file)
    tape.input_extend(program)
    # print(''.join(map(chr, tape.run())))
    return list(tape.run())[-1]


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
