import collections
import itertools
import re

import hashlib


VALUE = "yjdafjpo"
triple_hashes = collections.deque()

keep = []

# gotta do a little sorting: the order you have isn't necessarily in order.
if __name__ == '__main__':
    important = None
    for i in itertools.count():
        while triple_hashes and triple_hashes[0][0] + 1000 < i:
            triple_hashes.popleft()

        hsh = VALUE + str(i)
        for _ in range(2017):
            hsh = hashlib.md5(hsh.encode('utf8').lower()).hexdigest()

        m = re.search(r'(.)\1\1', hsh)
        if m:
            m_val = m.group(1)

            for m in re.finditer(r'(.)\1\1\1\1', hsh):
                num = m.group(1)
                print("5", num, hsh)
                new_keep = [
                    (i, value)
                    for i, value in triple_hashes
                    if value == num
                ]

                print('\n'.join(map(str, new_keep)))

                keep += new_keep

                triple_hashes = collections.deque(
                    (i, value)
                    for i, value in triple_hashes
                    if value != num
                )

                if len(keep) >= 64:
                    print("!!!", keep[63])

            triple_hashes.append((i, m_val))
