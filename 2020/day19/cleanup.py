def matches(rules, rule, string):
    return any(m == '' for m in match_helper(rules, rule, string))


def match_helper(rules, rule, string):
    rule_sets = rules[rule]
    if isinstance(rule_sets, str):
        if string.startswith(rule_sets):
            yield string[len(rule_sets):]
        return

    for rs in rule_sets:
        suffixes = [string]
        new_suffixes = []
        for rule in rs:
            for m in suffixes:
                new_suffixes.extend(match_helper(rules, rule, m))
            suffixes = new_suffixes
            new_suffixes = []
        yield from suffixes


def parse_rules(file1):
    rules = {}
    for line in file1:
        left, right = line.split(': ')
        if right.startswith('"'):
            rules[left] = right.strip('"')
        else:
            rule_sets = right.split(' | ')
            rules[left] = [rule_set.split() for rule_set in rule_sets]
    return rules


def part1(file1, file2):
    rules = parse_rules(file1)
    return sum(1 for line in file2 if matches(rules, '0', line))


def part2(file1, file2):
    rules = parse_rules(file1)
    rules['8'] = [['42'], ['42', '8']]
    rules['11'] = [['42', '31'], ['42', '11', '31']]

    return sum(1 for line in file2 if matches(rules, '0', line))


def main():
    with open('file.txt') as f:
        file_str1, file_str2 = f.read().split('\n\n')
        file1 = file_str1.rstrip("\n").split('\n')
        file2 = file_str2.rstrip("\n").split('\n')
    print(part1(list(file1), list(file2)))
    print(part2(list(file1), list(file2)))


if __name__ == '__main__':
    main()
