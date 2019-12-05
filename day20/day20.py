import collections
import functools
import itertools
import operator

inp = 33100000


def factors(n):
    return set(functools.reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def primes_generator():
    known_primes = collections.deque([2])
    yield 2
    for num in itertools.count(3, 2):
        for prime in known_primes:
            if prime * prime > num:
                known_primes.append(num)
                yield num
                break
            if num % prime == 0:
                break


def prod(iterable):
    return functools.reduce(operator.mul, iterable, 1)


# part 1 (with optimizations)
prime_gen = primes_generator()
prime_list = collections.deque()
last_val = 1
while True:
    prime_list.append(next(prime_gen))
    val = prod(prime_list)
    num = sum(factors(val)) * 10
    if num >= inp:
        break
    last_val = val

# part 1 (no optimizations)
# last_val = 1
for house in itertools.count(last_val):
    num = sum(factors(house)) * 10
    if num > inp:
        print(house)
        break

# part 2
# for house in itertools.count(1):
#     fs = factors(house)
#     fs = (f for f in fs if house / f <= 50)
#     num = sum(fs) * 11
#     if house % 10000 == 0:
#         print(house, num)
#     if num > inp:
#         print(house)
#         break
