LOOPS = 633601

def part1():
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    while len(recipes) < LOOPS + 10:
        recipes += list(map(int, str(recipes[elf1] + recipes[elf2])))
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)

    return ''.join(map(str, recipes[LOOPS:LOOPS+10]))


def part2():
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    loops = list(map(int, str(LOOPS)))
    ln = len(loops)
    while True:
        more = list(map(int, str(recipes[elf1] + recipes[elf2])))
        recipes += more
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)

        if recipes[-ln:] == loops:
            return len(recipes) - ln
        if recipes[-ln - 1:-1] == loops:
            return len(recipes) - ln - 1


print(part1())
print(part2())
