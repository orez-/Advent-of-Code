discs = [
    (13, 1),
    (19, 10),
    (3, 2),
    (7, 1),
    (5, 3),
    (17, 5),
    (11, 0),  # Part 2
]
prod = (
    13 * 19 * 3 * 7 * 5 * 17
    * 11  # part 2
)

for i in range(prod):
    for t, (slots, current) in enumerate(discs, 1):
        if (i + current + t) % slots:
            break
    else:
        print(i)
