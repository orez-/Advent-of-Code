from intcode import Tape


def part1(file):
    tapes = [
        Tape.from_file(file, input_values=[i])
        for i in range(50)
    ]
    while True:
        for i, tape in enumerate(tapes):
            result_iter = tape.run()
            dest = next(result_iter, -1)
            if dest == -1:
                continue
            x = next(result_iter)
            y = next(result_iter)
            if dest == 255:
                return y
            tapes[dest].input_extend([x, y])


def part2(file):
    tapes = [
        Tape.from_file(file, input_values=[i])
        for i in range(50)
    ]
    nat = None
    seen = set()
    did = True
    while True:
        for i, tape in enumerate(tapes):
            result_iter = tape.run()
            dest = next(result_iter, -1)
            if dest == -1:
                continue
            did = True
            x = next(result_iter)
            y = next(result_iter)
            if dest == 255:
                nat = (x, y)
                continue
            tapes[dest].input_extend([x, y])
        if not did:
            _, y = nat
            if y in seen:
                return y
            seen.add(y)
            tapes[0].input_extend(nat)
        did = False


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
