import collections

with open('input.txt', 'r') as f:
    sum_ = 0
    for line in f:
        *letters, last = line.split('-')

        num, checksum = last.strip('\n]').split('[')
        all_letters = ''.join(letters)

        count = collections.Counter(all_letters)
        common = iter(count.most_common(5))

        for c in checksum:
            _, best_count = next(common)
            if count[c] != best_count:
                break

        else:
            num = int(num)
            sum_ += num

            modnum = num % 26
            code = '-'.join(
                ''.join(chr((ord(c) - ord('a') + modnum) % 26 + ord('a')) for c in chrs)
                for chrs in letters
            )
            print(code, num)

    print(sum_)
