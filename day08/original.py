def part1(file):
    acc = 0
    i = 0
    seen = set()
    while True:
        if i in seen:
            return acc
        seen.add(i)
        if i == len(file):
            raise Exception(f"this one {acc}")
        elif i > len(file):
            return
        line = file[i]
        cmd, _, num = line.partition(' ')
        num = int(num)
        if cmd == 'acc':
            acc += num
            i += 1
        elif cmd == 'jmp':
            i += num
        elif cmd == 'nop':
            i += 1


def part2(file):
    for i, line in enumerate(file):
        cmd, _, num = line.partition(' ')
        if cmd == 'jmp':
            clone = list(file)
            clone[i] = f"nop {num}"
            part1(clone)
        elif cmd == 'nop':
            clone = list(file)
            clone[i] = f"jmp {num}"
            part1(clone)


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
