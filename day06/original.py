file = tuple(int(x) for x in """
4   10  4   1   8   4   9   14  5   1   14  15  0   15  3   5
""".strip().split())

# file = (0, 2, 7, 0)


def main(file):
    seen = {}
    mutable = list(file)
    while file not in seen:
        seen[file] = len(seen)
        ln = len(mutable)
        i, e = max(enumerate(mutable), key=lambda x: x[1])
        mutable[i] = 0
        while e:
            i = (i + 1) % ln
            mutable[i] += 1
            e -= 1
        file = tuple(mutable)
    print(len(seen))  # part 1
    print(len(seen) - seen[file])  # part 2


main(file)

