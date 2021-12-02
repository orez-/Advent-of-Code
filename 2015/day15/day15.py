import functools
import itertools
import more_itertools
import re

ingredients = filter(bool, """
Sprinkles: capacity 5, durability -1, flavor 0, texture 0, calories 5
PeanutButter: capacity -1, durability 3, flavor 0, texture 0, calories 1
Frosting: capacity 0, durability -1, flavor 4, texture 0, calories 6
Sugar: capacity -1, durability 0, flavor 0, texture 2, calories 8
""".split('\n'))

r = r'\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)'

stats = [
    list(map(int, re.match(r, line).groups()))
    for line in ingredients
]

def product(x, y):
    return x * y

def distributions(num, total):
    values = [0 for _ in range(num - 1)]
    while True:
        rest = total - sum(values)
        yield (rest, *values)
        if rest == 0:
            pos = next(i for i, v in enumerate(values) if v)
            if pos == len(values) - 1:
                return
            values[pos] = 0
            values[pos + 1] += 1
        else:
            values[0] += 1


def nutritional_value(amount, unit_value):
    return itertools.starmap(product, zip(itertools.repeat(amount), unit_value))

def strip_calories(dist):
    *rest, calories = zip(*itertools.starmap(nutritional_value, zip(dist, stats)))
    if sum(calories) == 500:
        yield from rest

print(max(
    functools.reduce(product, (
        max(0, sum(ingredient_score))
        for ingredient_score
        in strip_calories(dist)
    ), 1)
    for dist in distributions(4, 100)
))


# part 1
# print(max(
#     functools.reduce(product, (
#         max(0, sum(ingredient_score))
#         for ingredient_score
#         in zip(*itertools.starmap(nutritional_value, zip(dist, stats)))
#     ), 1)
#     for dist in distributions(4, 100)
# ))
