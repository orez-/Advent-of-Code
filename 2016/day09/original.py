import re


def part1(line):
    build_str = ""
    while line:
        next_id = re.match(r'(.*?)\((\d+)x(\d+)\)', line)
        if not next_id:
            break
        start, to_take, repeat = next_id.groups()
        build_str += start
        to_take, repeat = int(to_take), int(repeat)
        chrs = line[next_id.end():next_id.end() + to_take]
        build_str += chrs * repeat
        line = line[next_id.end() + to_take:]
    build_str += line
    return len(build_str)


def part2(line):
    amt = 0
    while line:
        next_id = re.match(r'(.*?)\((\d+)x(\d+)\)', line)
        if not next_id:
            break
        start, to_take, repeat = next_id.groups()
        to_take, repeat = int(to_take), int(repeat)
        amt += len(start)
        amt += part2(line[next_id.end():next_id.end() + to_take]) * repeat
        line = line[next_id.end() + to_take:]
    amt += len(line)
    return amt


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        line = next(file).strip()
        print(part1(line))
        print(part2(line))
