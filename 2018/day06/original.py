import collections
import re


def get_digits(line):
    return (int(match[0]) for match in re.finditer(r"\d+", line))


file = """
300, 90
300, 60
176, 327
108, 204
297, 303
101, 236
70, 102
336, 153
260, 265
228, 221
119, 267
310, 302
291, 164
190, 202
298, 228
292, 262
53, 251
176, 64
170, 160
71, 42
314, 51
71, 88
319, 150
192, 322
270, 88
165, 203
262, 340
301, 327
135, 324
97, 250
161, 231
305, 344
295, 213
320, 219
172, 269
151, 150
215, 128
167, 102
158, 138
307, 353
358, 335
163, 329
234, 147
58, 298
228, 50
151, 334
108, 176
335, 235
296, 263
80, 233
""".strip().split('\n')


def part1(file):
    coords = list(map(tuple, map(get_digits, file)))
    spots = {}
    # Define the bounds of the area we care about.
    # We define these as one past the farthest coordinate in each direction
    # Anything more than that is "infinite" and we don't care
    minx = min(x for x, y in coords) - 1
    maxx = max(x for x, y in coords) + 1
    miny = min(y for x, y in coords) - 1
    maxy = max(y for x, y in coords) + 1

    # Create the map of closest coordinates to each spot
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            closest_coord = None
            closest_num = float('inf')
            for cx, cy in coords:
                dist = abs(x - cx) + abs(y - cy)
                if dist < closest_num:
                    closest_num = dist
                    closest_coord = (cx, cy)
                elif dist == closest_num:
                    closest_coord = None
            spots[x, y] = closest_coord

    # disqualify all closest-coordinates on the edge of the map (since they're infinite)
    dqd = set()
    for x in range(minx, maxx + 1):
        dqd.add(spots[x, miny])
        dqd.add(spots[x, maxy])

    for y in range(miny, maxy + 1):
        dqd.add(spots[minx, y])
        dqd.add(spots[maxx, y])

    # apply disqualifications
    coun = collections.Counter(spots.values())
    coun.pop(None, None)
    for q in dqd:
        coun.pop(q, dqd)

    ((key, size),) = coun.most_common(1)
    return size


def part2(file):
    coords = list(map(tuple, map(get_digits, file)))
    minx = min(x for x, y in coords) - 1
    maxx = max(x for x, y in coords) + 1
    miny = min(y for x, y in coords) - 1
    maxy = max(y for x, y in coords) + 1
    c = 0
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            s = sum(
                abs(x - cx) + abs(y - cy)
                for cx, cy in coords
            )
            if s <= 10000:
                c += 1
    return c


print(part1(list(file)))
print(part2(list(file)))
