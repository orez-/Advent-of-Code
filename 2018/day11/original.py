def part1():
    grid = {}
    serial = 6878
    for x in range(1, 301):
        rack_id = x + 10
        for y in range(1, 301):
            power = (rack_id * y + serial) * rack_id
            digit = ((power // 100) % 10) - 5
            grid[x, y] = digit

    most = -1000
    most_num = None
    for x in range(1, 301 - 3):
        for y in range(1, 301 - 3):
            total = 0
            for dx in range(3):
                for dy in range(3):
                    total += grid[x + dx, y + dy]
            if total > most:
                most = total
                most_num = (x, y)
    return most_num



def part2():
    # This is a bad solution!
    # There's gotta be something cool and dynamic program-y to do here.
    SIZE = 301
    grid = {}
    serial = 6878
    for x in range(1, SIZE):
        rack_id = x + 10
        for y in range(1, SIZE):
            power = (rack_id * y + serial) * rack_id
            digit = ((power // 100) % 10) - 5
            grid[x, y] = digit

    most = -1000
    most_num = None
    for x in range(1, SIZE):
        for y in range(1, SIZE):
            total = 0
            for size in range(1, SIZE + 1 - max(x, y)):
                for d in range(size):
                    total += grid[x + d, y + size - 1]
                for d in range(size -  1):
                    total += grid[x + size - 1, y + d]
                if total > most:
                    most = total
                    most_num = (x, y, size)
    return most_num


print(part1())
print(part2())
