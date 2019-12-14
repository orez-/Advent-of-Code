import collections
import math
import re


def part1(file):
    recipes = {}
    for line in file:
        *reagents, product = re.finditer(r"(\d+) ([A-Z]+)", line)
        recipes[product[2]] = (reagents, product)
    # print(recipes.keys())

    return run(1, recipes)


def run(num, recipes):
    queue = collections.deque([(num, "FUEL")])
    excess = collections.defaultdict(int)
    ore = 0
    while queue:
        product_needed_amt, product_name = queue.popleft()
        if product_name == "ORE":
            ore += product_needed_amt
            continue

        reagents, product = recipes[product_name]
        # print("making", product_needed_amt, product_name)
        # print("from", reagents)
        # print("have", excess[product_name])
        product_needed_amt -= excess[product_name]
        # print("gotta make", product_needed_amt)
        recipe_creates_amt = int(product[1])
        batches = math.ceil(product_needed_amt / recipe_creates_amt)
        # print("batches", batches)
        excess[product_name] = (batches * recipe_creates_amt) - product_needed_amt
        # print(excess)
        for match in reagents:
            needed = int(match[1]) * batches
            if needed:
                queue.append((needed, match[2]))
        # print()
    return ore


def part2(file):
    recipes = {}
    for line in file:
        *reagents, product = re.finditer(r"(\d+) ([A-Z]+)", line)
        recipes[product[2]] = (reagents, product)

    ore = 0
    fuel = 3125000
    while True:
        needed_ore = run(fuel + 1, recipes)
        # print(needed_ore, fuel)
        if needed_ore > 1000000000000:
            return fuel
        fuel += 1


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
