import re


def get_digits(line):
    return (int(match.group(0)) for match in re.finditer(r"-?\d+", line))


def dist(coord1, coord2):
    return sum(abs(c1 - c2) for c1, c2 in zip(coord1, coord2))


def part1(file):
    consts = {
        frozenset([tuple(get_digits(line))])
        for line in file
    }
    for const1 in frozenset(consts):
        eaten = set()
        if const1 in eaten:
            continue
        new = const1
        for star1 in const1:
            for const2 in frozenset(consts):
                if const1 == const2:
                    continue
                for star2 in const2:
                    if dist(star1, star2) <= 3:
                        new |= const2
                        consts.discard(const2)
                        eaten.add(const1)
                        eaten.add(const2)
                        break
        consts.discard(const1)
        consts.add(new)
    return len(consts)


def part2(file):
    return "Merry xmas"


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
