import collections
import hashlib
import itertools
import re


def do_the_rotate(word, letter):
    a = word.index(letter)
    if a >= 4:
        a += 1
    word = collections.deque(word)
    word.rotate(a + 1)
    return list(word)


def main1(file, word):
    word = list(word)
    for line in file:
        line = line.strip()
        m = re.match(r'swap position (\d+) with position (\d+)', line)
        if m:
            a, b = map(int, m.groups())
            word[a], word[b] = word[b], word[a]
            continue

        m = re.match(r'swap letter (\w+) with letter (\w+)', line)
        if m:
            aw, bw = m.groups()
            a = word.index(aw)
            b = word.index(bw)
            word[a], word[b] = word[b], word[a]
            continue

        m = re.match(r'rotate (left|right) (\d+) steps?', line)
        if m:
            dr, num = m.groups()
            num = int(num) % len(word)
            if dr == 'left':
                num = -num
            word = collections.deque(word)
            word.rotate(num)
            word = list(word)
            continue

        m = re.match(r'rotate based on position of letter (\w)', line)
        if m:
            aw, = m.groups()
            a = word.index(aw)
            if a >= 4:
                a += 1
            word = collections.deque(word)
            word.rotate(a + 1)
            word = list(word)
            continue

        m = re.match(r'reverse positions? (\d+) through (\d+)', line)
        if m:
            a, b = map(int, m.groups())
            word[a:b+1] = reversed(word[a:b+1])
            continue

        m = re.match(r'move position (\d+) to position (\d+)', line)
        if m:
            a, b = map(int, m.groups())
            aw = word[a]
            del word[a]
            word.insert(b, aw)

    return ''.join(word)


def main2(file, word):
    word = list(word)
    for line in list(file)[::-1]:
        line = line.strip()
        m = re.match(r'swap position (\d+) with position (\d+)', line)
        if m:
            a, b = map(int, m.groups())
            word[a], word[b] = word[b], word[a]
            continue

        m = re.match(r'swap letter (\w+) with letter (\w+)', line)
        if m:
            aw, bw = m.groups()
            a = word.index(aw)
            b = word.index(bw)
            word[a], word[b] = word[b], word[a]
            continue

        m = re.match(r'rotate (left|right) (\d+) steps?', line)
        if m:
            dr, num = m.groups()
            num = int(num) % len(word)
            if dr == 'right':
                num = -num
            word = collections.deque(word)
            word.rotate(num)
            word = list(word)
            continue

        m = re.match(r'rotate based on position of letter (\w)', line)
        if m:
            aw, = m.groups()
            d = collections.deque(word)
            while True:
                if do_the_rotate(d, aw) == word:
                    word = list(d)
                    break
                d.rotate(-1)
            continue

        m = re.match(r'reverse positions? (\d+) through (\d+)', line)
        if m:
            a, b = map(int, m.groups())
            word[a:b+1] = reversed(word[a:b+1])
            continue

        m = re.match(r'move position (\d+) to position (\d+)', line)
        if m:
            a, b = map(int, m.groups())
            bw = word[b]
            del word[b]
            word.insert(a, bw)
    return ''.join(word)



if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        print(main1(file, "abcdefgh"))


    # with open('example.txt', 'r') as file:
    #     print(main1(file, "abcde"))


    # print("---")

    with open('input.txt', 'r') as file:
        print(main2(file, "fbgdceah"))


    # with open('example.txt', 'r') as file:
    #     print(main2(file, "decab"))
