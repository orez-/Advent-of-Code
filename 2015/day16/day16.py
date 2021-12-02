import re
import sys


sues = [
    dict(m.groups() for m in re.finditer(r"(\w+): (\d+)", line))
    for line in sys.stdin
]

facts = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

# part 1
# for i, sue in enumerate(sues, 1):
#     if all(facts[stat] == int(amount) for stat, amount in sue.items()):
#         print(i)
#         break

def retroencabulate(stat_amount):
    stat, amount = stat_amount
    amount = int(amount)
    if stat in {'cats', 'trees'}:
        return facts[stat] < amount
    if stat in {'pomeranians', 'goldfish'}:
        return facts[stat] > amount
    return facts[stat] == amount

print(next(
    i for i, sue in enumerate(sues, 1)
    if all(map(retroencabulate, sue.items()))
))
