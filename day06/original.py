import collections

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        letters = [collections.Counter() for _ in range(8)]
        for line in file:
            for i, letter in enumerate(line.strip()):
                letters[i][letter] += 1

        for c in letters:
            # print(c.most_common()[0][0], end='')  # part 1
            print(c.most_common()[-1][0], end='')  # part 2
        print()
