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
    print(top)  # part 1
    req(top, stack, nums)



def req(top, stack, nums):
    guys = stack[top]
    vs = [
        (guy, req(guy, stack, nums))
        for guy in guys
    ]
    multiple = 0
    seen = set()
    for g, v in vs:
        if v in seen:
            multiple = v
        seen.add(v)
    seen.discard(multiple)
    if seen:
        value, = seen
        troublemaker = next(g for g, v in vs if v == value)
        print(nums[troublemaker] - (value - multiple))  # part 2
    return nums[top] + len(vs) * multiple


main()
