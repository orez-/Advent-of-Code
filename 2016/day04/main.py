import collections
import sys


def get_rooms(file):
    for line in file:
        *words, last = line.split('-')
        num, checksum = last.strip('\n]').split('[')
        yield words, checksum, int(num)


def filter_checksum_rooms(rooms):
    for words, checksum, num in rooms:
        all_letters = ''.join(words)

        counter = collections.Counter(all_letters)

        # If the count of the current letter is the same as the next best count
        valid_checksum = all(
            counter[letter] == best_count
            for letter, (_, best_count)
            in zip(checksum, counter.most_common(5))
        )

        if valid_checksum:
            yield words, checksum, num


def decipher_words(rooms):
    for words, _, num in rooms:
        yield '-'.join(
            ''.join(
                chr((ord(char) - ord('a') + num) % 26 + ord('a'))
                for char in word
            )
            for word in words
        ), num


if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else None

    with open('input.txt', 'r') as file:
        rooms = get_rooms(file)

        if part == '1':
            rooms = filter_checksum_rooms(rooms)
            print(sum(num for _, _, num in rooms))
        elif part == '2':
            rooms = filter_checksum_rooms(rooms)
            for code, num in decipher_words(rooms):
                if 'north' in code:
                    print(code, num)
        elif part == 'rooms':
            for code, num in sorted(decipher_words(rooms), key=lambda kv: kv[1]):
                print(num, '-', code)
        elif part == 'analyze':
            common_words = collections.Counter(
                word
                for code, _ in decipher_words(rooms)
                for word in code.split('-')
            ).most_common()

            for word, count in common_words:
                print(word, count)
