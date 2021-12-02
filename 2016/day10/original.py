import collections
import itertools
import re

give = re.compile(r'bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)')
goes = re.compile(r'value (\d+) goes to bot (\d+)')


def main(file):
    file = list(file)
    bots = collections.defaultdict(list)
    output = {}
    for line in file:
        match = goes.match(line)
        if match:
            value, bot = map(int, match.groups())
            bots[bot].append(value)


    progress = True
    while progress:
        progress = False
        for line in file:
            match = give.match(line)
            if match:
                gives, low_bucket, low_num, high_bucket, high_num = match.groups()
                gives, low_num, high_num = map(int, (gives, low_num, high_num))

                if len(bots[gives]) != 2:
                    continue
                progress = True
                low, high = sorted(bots[gives])
                if (low, high) == (17, 61):
                    print(gives)
                if low_bucket == 'output':
                    output[low_num] = low
                else:
                    bots[low_num].append(low)


                if high_bucket == 'output':
                    output[high_num] = high
                else:
                    bots[high_num].append(high)
                del bots[gives]

    print(output[0] * output[1] * output[2])


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        main(file)
