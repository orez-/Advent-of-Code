import collections
import functools
import itertools
import re


def run1(file, num_cards):
    cards = collections.deque(range(num_cards))
    seen = {}

    for i in range(1):
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
                # assert all(c is not None for c in cards)
            elif line.startswith("deal into"):
                cards = collections.deque(reversed(cards))
        # c = tuple(cards)
        # if c in seen:
        #     print(seen[c])
        # seen[c] = i
        # print(".")

    return cards

# CARD
# def cut(num_cards, num, card):
#     return (card - num) % num_cards


# def deal_with(num_cards, num, card):
#     return (num * card) % num_cards


# def deal_into(num_cards, card):
#     return num_cards - 1 - card


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


# NEW POSITION => OLD POSITION
def cut(num_cards, num, new_position):
    return (new_position + num) % num_cards


def deal_with(num_cards, mi_num, new_position):
    # new_pos = (num * old_pos) % num_cards
    # new_pos / num = old_pos
    return (new_position * mi_num) % num_cards


def deal_into(num_cards, new_position):
    return num_cards - 1 - new_position


# def follow_card(file, num_cards, card):
#     seen = {}
#     for i in range(101741582076661):
#         for line in file:
#             if line.startswith("cut"):
#                 [num] = re.search(r"(-?\d+)", line).groups()
#                 num = int(num)
#                 card = (card - num) % num_cards
#             elif line.startswith("deal with"):
#                 [num] = re.search(r"(-?\d+)", line).groups()
#                 num = int(num)
#                 card = (num * card) % num_cards
#             elif line.startswith("deal into"):
#                 card = num_cards - 1 - card
#         print(card)
#         if card in seen:
#             print(seen[card])
#             break
#         seen[card] = i


def compile_instructions(file, num_cards):
    instructions = []

    for line in file:
        if line.startswith("cut"):
            [num] = re.search(r"(-?\d+)", line).groups()
            instructions.append(functools.partial(cut, num_cards, int(num)))
        elif line.startswith("deal with"):
            [num] = re.search(r"(-?\d+)", line).groups()
            instructions.append(functools.partial(deal_with, num_cards, modinv(int(num), num_cards)))
        elif line.startswith("deal into"):
            instructions.append(functools.partial(deal_into, num_cards))

    return instructions[::-1]


# def follow_position(instructions, num_cards, position, iterations=1):
#     seen = {position: 0}
#     for i in range(1, iterations + 1):
#         for action in instructions[::-1]:
#             position = action(position)
#         if position in seen:
#             print(position, i, seen[position])
#             raise Exception()
#         seen[position] = i
#         if not (i % 100000):
#             print(f"{position:>15}", f"{i:>15}")
#     return position

def follow_position(instructions, num_cards, position, iterations=1):
    initial_position = position
    for i in range(1, iterations + 1):
        for action in instructions:
            position = action(position)
        if position == initial_position:
            print("cycle at", i, position)
        if not (i % 1000000):
            print(f"{position:>15}", f"{i:>15}")
    return position


# def follow_card(file, num_cards, card, iterations=1):
#     seen = {card: 0}
#     for i in range(1, iterations + 1):
#         for action in instructions:
#             card = action(card)
#         print(i, card)
#         # print(card)
#         if card in seen:
#             period = i - seen[card]
#             equivalent = iterations % period
#             return next(c for c, ind in seen.items() if ind == equivalent)
#         seen[card] = i
#     return card


def part1(file):
    # return follow_card(file, 10007, 2019)
    # result = run1(file, 10)
    # print(result)

    result = run1(file, 10007)
    return result.index(2019)

    # num_cards = 10007
    # instructions = compile_instructions(file, num_cards)
    # followed = follow_position(instructions, num_cards, 6638)
    # print(followed)
    # num_cards = 10
    # instructions = compile_instructions(file, num_cards)
    # return [follow_position(instructions, num_cards, i) for i in range(10)]


def part2(file):
    print("I didn't solve part 2 originally!")
    print("But this should technically get you the answer if you wait for a very long time.")
    num_cards = 119315717514047
    iterations = 101741582076661
    instructions = compile_instructions(file, num_cards)
    return follow_position(instructions, num_cards, position=2020, iterations=iterations)
    # return (followed * iterations) % num_cards

    # result = follow_card(file, num_cards=num_cards, position=2020, )
    # return result
    # return result.index(2020)
    # tape = Tape.from_file(file, input_values=[2])
    # tape.run()


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
