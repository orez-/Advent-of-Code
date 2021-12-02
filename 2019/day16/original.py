import itertools


def extend(pattern, index):
    result = [
        v for v in pattern
        for _ in range(index + 1)
    ]
    return itertools.cycle(result + [result.pop(0)])


def part1(signal):
    base_pattern = [0, 1, 0, -1]

    for _ in range(100):
        number = []
        for index, _ in enumerate(signal):
            pattern = extend(base_pattern, index)
            total = sum(p * s for p, s in zip(pattern, signal))
            digit = abs(total) % 10
            number.append(digit)
        signal = number
    return ''.join(map(str, signal[:8]))


def part2(signal):
    signal = list(signal) * 10000
    offset = int(''.join(map(str, signal[:7])))

    # Key observations that make this solution possible:
    # - my seven-digit offset is ≥ half the signal length
    # - the pattern is 0, 1, 0, -1.

    # This means:
    # - the digits from `offset` onward can be calculated only by summing all digits
    #     including and following it (pattern of [0] * (offset - 1) + [1] * offset)
    # - we _never_ need to calculate the first `offset` digits, since
    #     they don't factor into the final output
    # - we can perform a rolling sum when calculating digits to save some time
    for _ in range(100):
        number = []
        total = sum(signal[offset:])
        for index, num in enumerate(signal[offset:], offset):
            number.append(total % 10)
            total -= num
        signal[offset:] = number
    return ''.join(map(str, signal[offset:offset+8]))


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, str(file[0])))
    print(part1(list(file)))
    print(part2(list(file)))
