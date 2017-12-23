import bisect
import itertools


class PrimeGenerator(object):
    """
    Hey check out this crappy prime generator I made a while back. Pretty handy.
    """
    def __init__(self):
        self._gen = self._gen_fn()
        next(self._gen)

    def primes_below(self, num):
        if self._primes[-1] < num:
            for p in self._gen:
                if p >= num:
                    return self._primes[:]
        return self._primes[:bisect.bisect(self._primes, num)]

    def nth_prime(self, n):
        diff = n - len(self._primes) + 1
        if diff >= 0:
            for _ in itertools.izip(xrange(diff), self._gen):
                pass
        return self._primes[n]

    def __contains__(self, value):
        self.primes_below(value + 1)
        # TODO: bisect
        return value in self._primes

    def _gen_fn(self):
        self._primes = [2]
        yield 2
        for i in itertools.count(3):
            for p in self._primes:
                if p * p > i:
                    self._primes.append(i)
                    yield i
                    break
                if i % p == 0:
                    break


def crappy_is_composite(b):
    for d in range(2, b):
        for e in range(2, b):
            if e * d == b:  # jnz g 2
                return True
    return False


def main():
    pg = PrimeGenerator()

    a = 1
    b = 6500 + 100000  # set b 65
    c = b + 17000  # set c b
    d = f = h = 0

    while 1:
        f = 1  # set f 1
        # if crappy_is_composite(b):  # jnz f 2
        if b not in pg:
            h += 1 # sub h -1
        if b == c:  # jnz g 2
            return h  # jnz 1 3
        b += 17  # sub b -17


print(main())
