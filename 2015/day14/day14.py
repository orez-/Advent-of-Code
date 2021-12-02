import re

speeds = """
Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.
Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.
Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.
Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.
Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.
Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.
Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.
Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds.
"""

seconds = 2503


speeds = filter(bool, speeds.split('\n'))
speeds = [
    map(int, r.groups()) for r in (
        re.search(r'\w+ can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.', sp) for sp in speeds)
]

def get_times(seconds):
    for speed, time, rest in speeds:
        cycles, position = divmod(seconds, (time + rest))
        yield cycles * time * speed + min(position, time) * speed

# part 1
# print max(get_times(seconds))

# part 2
scores = [0 for _ in speeds]

for t in xrange(1, seconds + 1):
    times = list(get_times(t))
    score = max(times)
    for i, t in enumerate(times):
        if t == score:
            scores[i] += 1

print max(scores)

