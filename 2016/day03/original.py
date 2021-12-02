import sys


if __name__ == '__main__':
    # part = sys.argv[1] if len(sys.argv) > 1 else None

    # if part == '1':
    #     pass
    # elif part == '2':
    #     pass
    # else:
    #     sys.exit()

    # with open('input.txt', 'r') as file:
    #     x = 0
    #     for line in file:
    #         a, b, c = sorted(map(int, line.strip().split()))
    #         if a + b > c:
    #             x += 1
    #     print(x)

    with open('input.txt', 'r') as file:
        x = 0
        try:
            while True:
                a1, a2, a3 = map(int, next(file).strip().split())
                b1, b2, b3 = map(int, next(file).strip().split())
                c1, c2, c3 = map(int, next(file).strip().split())

                a1, b1, c1 = sorted([a1, b1, c1])
                a2, b2, c2 = sorted([a2, b2, c2])
                a3, b3, c3 = sorted([a3, b3, c3])

                if a1 + b1 > c1:
                    x += 1

                if a2 + b2 > c2:
                    x += 1

                if a3 + b3 > c3:
                    x += 1
        except StopIteration:
            pass
        print(x)
