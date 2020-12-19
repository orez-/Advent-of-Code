def matches(rules, rule, string):
    x = rules[rule]
    if isinstance(x, str):
        if string.startswith(x):
            return string[len(x):]
        else:
            return
    for rs in x:
        m = string
        for r in rs:
            m = matches(rules, r, m)
            if m is None:
                break
        else:
            return m


def matches2(rules, rule, string):
    rule_sets = rules[rule]
    if isinstance(rule_sets, str):
        if string.startswith(rule_sets):
            yield string[len(rule_sets):]
        return

    for rs in rule_sets:
        ms = [string]
        nms = []
        for r in rs:
            for m in ms:
                nms.extend(matches2(rules, r, m))
            ms = nms
            nms = []
        yield from ms


def part1(file1, file2):
    mapper = {}
    for line in file1:
        left, right = line.split(': ')
        if right.startswith('"'):
            mapper[left] = right.strip('"')
        else:
            splits = right.split(' | ')
            if len(splits) == 1:
                rulez = splits[0].split()
                mapper[left] = [rulez]
            if len(splits) == 2:
                rulez1 = splits[0].split()
                rulez2 = splits[1].split()
                mapper[left] = [rulez1, rulez2]

    rule = mapper['0']
    total = 0
    for line in file2:
        if matches(mapper, '0', line) == '':
            total += 1
    return total


def part2(file1, file2):
    mapper = {}
    for line in file1:
        left, right = line.split(': ')
        if right.startswith('"'):
            mapper[left] = right.strip('"')
        else:
            splits = right.split(' | ')
            if len(splits) == 1:
                rulez = splits[0].split()
                mapper[left] = [rulez]
            if len(splits) == 2:
                rulez1 = splits[0].split()
                rulez2 = splits[1].split()
                mapper[left] = [rulez1, rulez2]

    mapper['8'] = [['42'], ['42', '8']]
    mapper['11'] = [['42', '31'], ['42', '11', '31']]

    total = 0
    for line in file2:
        if any(m == '' for m in matches2(mapper, '0', line)):
            total += 1
    return total


def main():
    with open('file.txt') as f:
        file_str1, file_str2 = f.read().split('\n\n')
        file1 = file_str1.rstrip("\n").split('\n')
        file2 = file_str2.rstrip("\n").split('\n')
    print(part1(list(file1), list(file2)))
    print(part2(list(file1), list(file2)))


if __name__ == '__main__':
    main()
