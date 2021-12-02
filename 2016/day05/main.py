import hashlib
import itertools
import sys


def hash_stream(puzzle_input):
    for i in itertools.count():
        value = '{}{}'.format(puzzle_input, i).encode('utf8')
        hex_hash = hashlib.md5(value).hexdigest()
        if hex_hash.startswith('00000'):
            yield hex_hash[5:7]


def part1(puzzle_input):
    password = ''
    for num, _ in hash_stream(puzzle_input):
        password += num
        if len(password) == 8:
            break
    return password


def part2(puzzle_input):
    missing_nums = set(range(8))
    password = [None] * 8
    stream = hash_stream(puzzle_input)

    while missing_nums:
        position, value = next(stream)
        position = int(position, 16)
        if position in missing_nums:
            missing_nums.discard(position)
            password[position] = value
            print(password)
    return ''.join(password)


if __name__ == '__main__':
    puzzle_input = 'abbhdwsy'
    part = sys.argv[1] if len(sys.argv) > 1 else None

    if part == '1':
        print(part1(puzzle_input))
    elif part == '2':
        print(part2(puzzle_input))
