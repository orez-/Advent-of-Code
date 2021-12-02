discs = [
    (13, 1),
    (19, 10),
    (3, 2),
    (7, 1),
    (5, 3),
    (17, 5),
    (11, 0),  # Part 2
]

prod = 1
for i, (slots, offset) in enumerate(discs):
    discs[i] = (slots, i + offset + 1)
    prod *= slots

step, offset = max(discs, key=lambda item: item[0])

for i in range(-offset % step, prod, step):
    if not any((i + current) % slots for slots, current in discs):
        print(i)
        break
