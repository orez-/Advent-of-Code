import re


def main():
    with open('input.txt', 'r') as f:
        file = list(f)
    stack = {}
    nums = {}
    seen = set()
    for line in file:
        name, num, guys = re.match(r"(\w+) +\((\d+)\)(?: +-> +((?:\w+, )*\w+))?", line).groups()
        if guys:
            guys = list(map(str.strip, guys.split(',')))
        else:
            guys = []
        nums[name] = int(num)
        stack[name] = guys
        seen.update(guys)
    top, = stack.keys() - seen
    print(top)
    print(req(top, stack, nums))



def req(top, stack, nums):
    guys = stack[top]
    vs = [
        req(guy, stack, nums)
        for guy in guys
    ]
    if not all(v == vs[0] for v in vs):
        # honestly i did the math myself from this data to get the answer.
        # that's kind of unsatisfying, so original_cleanup.py has similarly messy code
        # that actually finds a solution.
        print(top, nums[top], vs, guys)
    return nums[top] + sum(vs)


main()
