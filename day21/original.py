def part1():
    d = e = 0  # we factored out the rest of the registers!!
    ds = set()
    while 1:
        d = e | 65536
        if d in ds:
            break
        ds.add(d)
        e = 16098955
        while 1:
            e += d & 255
            e = e & 16777215
            e *= 65899
            e = e & 16777215
            if 256 > d:
                return e
                # if a == e:
                #     return a
                # break
            d //= 256


def part2():
    d = e = 0  # we factored out the rest of the registers!!
    ds = set()
    last = None
    while 1:
        d = e | 65536
        if d in ds:
            break
        ds.add(d)
        e = 16098955
        while 1:
            e += d & 255
            e = e & 16777215
            e *= 65899
            e = e & 16777215
            if 256 > d:
                last = e
                # if a == e:
                #     return a
                break
            d //= 256
    return last


if __name__ == '__main__':
    print(part1())
    print(part2())
