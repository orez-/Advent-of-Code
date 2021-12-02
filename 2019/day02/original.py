def run(file):
    timeout = 0
    i = 0
    while True:
        timeout += 1
        if timeout >= 10000:
            return -1
        if file[i] == 1:
            file[file[i + 3]] = file[file[i + 1]] + file[file[i + 2]]
            i += 4
        elif file[i] == 2:
            file[file[i + 3]] = file[file[i + 1]] * file[file[i + 2]]
            i += 4
        elif file[i] == 99:
            return file[0]
        else:
            raise Exception


def part1(file):
    file[1] = 12
    file[2] = 2
    return run(file)


def part2(file):
    for a in range(100):
        for b in range(100):
            check = list(file)
            check[1] = a
            check[2] = b
            try:
                result = run(check)
                if result == 19690720:
                    return a * 100 + b
            except Exception:
                pass


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    file = list(map(int, file[0].split(',')))
    print(part1(list(file)))
    print(part2(list(file)))
