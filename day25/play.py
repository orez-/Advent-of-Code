from intcode import Tape


def part1(file):
    tape = Tape.from_file(file)
    go = tape.run()
    coll = []
    for x in go:
        x = chr(x)
        coll.append(x)
        if ''.join(coll[-8:]) == "Command?":
            print(''.join(coll))
            result = input("> ") + "\n"
            tape.input_extend(result)
    print(''.join(coll))


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    part1(list(file))
