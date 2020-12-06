import re


def regroup(file):
    # oops this could've just been `split('\n\n')`, huh?
    f = iter(file)
    x = []
    for line in f:
        if not line:
            yield x
            x = []
            continue
        x.append(line)
    yield x


def part1(file):
    fields = [
        "byr:",
        "iyr:",
        "eyr:",
        "hgt:",
        "hcl:",
        "ecl:",
        "pid:",
    ]

    t = 0
    for passport in regroup(file):
        d = '\n'.join(passport)
        for f in fields:
            if f not in d:
                break
        else:
            t += 1
    return t


def byr(v):
    # (Birth Year) - four digits; at least 1920 and at most 2002.
    return '1920' <= v <= '2002'

def iyr(v):
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    return '2010' <= v <= '2020'

def eyr(v):
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    return '2020' <= v <= '2030'

def hgt(v):
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    m = re.fullmatch(r"(\d+)(cm|in)", v)
    if not m:
        return False
    num, unit = m.groups()
    num = int(num)
    if unit == 'cm':
        return 150 <= num <= 193
    else:
        return 59 <= num <= 76

def hcl(v):
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    return bool(re.fullmatch(r'#[0-9a-f]{6}', v))

def ecl(v):
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    return v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def pid(v):
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    return re.fullmatch(r'\d{9}', v)


def part2(file):
    fields = [
        ("byr:", byr),
        ("iyr:", iyr),
        ("eyr:", eyr),
        ("hgt:", hgt),
        ("hcl:", hcl),
        ("ecl:", ecl),
        ("pid:", pid),
    ]

    t = 0
    for passport in regroup(file):
        d = '\n'.join(passport)
        for f, fn in fields:
            if f not in d:
                break
            i = d.index(f) + 4
            s = d[i:].split()
            if not s:
                break
            value = s[0]
            if not fn(value):
                break
        else:
            t += 1
    return t


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
