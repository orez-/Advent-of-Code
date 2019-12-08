def part1(file):
    file = iter(file[0])

    layers = []

    try:
        while True:
            layer = [next(file) for r in range(25 * 6)]
            layers.append(layer)
    except StopIteration:
        pass

    _, layer = min((layer.count("0"), layer) for layer in layers)
    return layer.count("1") * layer.count("2")


def first_guy(x):
    for y in x:
        if y in "01":
            return y
    return 2


def part2(file):
    file = iter(file[0])

    layers = []

    try:
        while True:
            layer = [next(file) for r in range(25 * 6)]
            layers.append(layer)
    except StopIteration:
        pass

    # 0 is black, 1 is white, and 2 is transparent.
    image = (first_guy(x) for x in zip(*layers))
    for y in range(6):
        for x in range(25):
            print(end=" " if next(image) == "0" else "#")
        print()


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    part2(list(file))
