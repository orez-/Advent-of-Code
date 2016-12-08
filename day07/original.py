"""
This is sincere poop-butt garbage I was tired shut up

Don't look at this please. Included for completeness.
"""

import collections


def get():
    # # part1
    # with open('input.txt', 'r') as file:
    #     for line in file:
    #         queue = []
    #         in_brack = False
    #         yes = False
    #         for c in line.strip():
    #             if c == '[':
    #                 in_brack = True
    #             if c == ']':
    #                 in_brack = False
    #             queue += [c]
    #             if len(queue) > 4:
    #                 queue.pop(0)
    #             if queue == queue[::-1] and len(queue) == 4 and queue[0] != queue[1]:
    #                 print(line, queue, in_brack)
    #                 if in_brack:
    #                     break
    #                 yes = True
    #         else:
    #             if yes:
    #                 yield line

    # # part 2
    with open('input.txt', 'r') as file:
        for line in file:
            babs = collections.defaultdict(int)
            queue = []
            in_brack = False
            yes = False
            for c in line.strip():
                if c == '[':
                    in_brack = True
                if c == ']':
                    in_brack = False
                queue += [c]
                if len(queue) > 3:
                    queue.pop(0)
                if queue == queue[::-1] and len(queue) == 3 and queue[0] != queue[1]:
                    # print(line, queue, in_brack)
                    if in_brack:
                        babs[tuple(queue[1:])] |= 2
                    else:
                        babs[tuple(queue[:2])] |= 1
            if babs:
                print(line, babs)
            if any(v == 3 for v in babs.values()):
                yield line

if __name__ == '__main__':
    # print(get())
    print(sum(1 for _ in get()))
