start = "1321131112"

def groupby(string):
    # Like itertools.groupby except does exactly what I want.
    i = iter(string)
    e = next(i, None)
    if e is None:
        return
    m = 1
    for c in i:
        if c != e:
            yield str(m)
            yield e
            m = 0
            e = c
        m += 1
    yield str(m)
    yield e

for i in xrange(50):
    start = groupby(start)
print len(list(start))
