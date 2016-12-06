import hashlib
import sys

puzz_input = 'abbhdwsy'

if __name__ == '__main__':
    # x = 0
    # pw = ''
    # while len(pw) < 8:
    #     num = hashlib.md5('{}{}'.format(puzz_input, x).encode('utf8')).hexdigest()
    #     if num.startswith('00000'):
    #         pw += num[5]
    #         print(num[5])
    #     x += 1
    # print(pw)
    # part = sys.argv[1] if len(sys.argv) > 1 else None


    x = 0
    pw = [None] * 8
    while any(n is None for n in pw):
        num = hashlib.md5('{}{}'.format(puzz_input, x).encode('utf8')).hexdigest()
        if num.startswith('00000'):
            i = int(num[5], 16)
            if i < len(pw) and pw[i] is None:
                pw[i] = num[6]
                print(pw)
            # pw += num[5]
            # print(num[5])
        x += 1
    print(pw)
