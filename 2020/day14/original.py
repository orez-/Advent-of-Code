from itertools import chain, combinations


def part1(file):
    mask_val = {}
    mem = {}
    for line in file:
        if line.startswith('mem'):
            _, n1, n2 = line.split()
            n1 = int(n1)
            n2 = int(n2)
            for n, v in mask_val.items():
                if v == 0:
                    n2 &= ~n
                else:
                    n2 |= n
            mem[n1] = n2
        else:
            mask_val = {}
            _, mask = line.split()
            for i, c in enumerate(mask):
                i = 35 - i
                if c != 'X':
                    mask_val[2 ** i] = int(c)
    return sum(mem.values())


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def part2(file):
    floaters = set()
    floater_mask = 0
    mask_val = 0
    mem = {}
    for line in file:
        if line.startswith('mem'):
            _, n1, n2 = line.split()
            n1 = int(n1)
            n2 = int(n2)
            n1 |= mask_val
            n1 &= ~floater_mask
            for ones in powerset(floaters):
                temp_n1 = n1
                for o in ones:
                    temp_n1 |= o
                mem[temp_n1] = n2
        else:
            mask_val = 0
            floater_mask = 0
            floaters = set()
            _, mask = line.split()
            for i, c in enumerate(mask):
                i = 35 - i
                if c == '1':
                    mask_val |= 2 ** i
                elif c == 'X':
                    floater_mask |= 2 ** i
                    floaters.add(2 ** i)

    return sum(mem.values())


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
