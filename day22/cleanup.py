import collections
import re


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def simplify_instruction_undo(file, num_cards):
    # ax + b mod num_cards
    a = 1
    b = 0
    for line in file[::-1]:
        if line.startswith("cut"):
            [num] = re.search(r"(-?\d+)", line).groups()
            b += int(num)
        elif line.startswith("deal with"):
            [num] = re.search(r"(-?\d+)", line).groups()
            mi = modinv(int(num), num_cards)
            a *= mi
            b *= mi
        elif line.startswith("deal into"):
            a *= -1
            b *= -1
            b -= 1
    return a, b


def part1(file):
    num_cards = 10007
    cards = collections.deque(range(num_cards))

    for line in file:
        if line.startswith("cut"):
            [num] = re.search(r"(-?\d+)", line).groups()
            num = int(num)
            cards.rotate(-num)
        elif line.startswith("deal with"):
            [num] = re.search(r"(-?\d+)", line).groups()
            num = int(num)
            index = 0
            deal = [None for _ in cards]
            while cards:
                deal[index] = cards.popleft()
                index = (index + num) % len(deal)
            cards = collections.deque(deal)
        elif line.startswith("deal into"):
            cards = collections.deque(reversed(cards))
    return cards.index(2019)


def part2(file):
    num_cards = 119315717514047
    iterations = 101741582076661
    position = 2020
    a, b = simplify_instruction_undo(file, num_cards)

    # (a(a(ax + b) + b) + b)
    # (a((a2x + ab)+ b) + b)
    # (((a3x + a2b + ab)+ b)
    # a3x + b(a2 + a + 1)
    apow = pow(a, iterations, num_cards)
    # ageom_series = (1 - pow(a, n)) / (1 - a)
    ageom_series = (pow(a, iterations, num_cards) - 1) * modinv(a - 1, num_cards)
    return (apow * position + b * ageom_series) % num_cards


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
