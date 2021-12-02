import blist


def solve(last_marble):
    marbles = blist.blist([0, 1])
    current = 1
    players = [0] * 413
    for i in range(2, last_marble + 1):
        if i % 23 == 0:
            current = (current - 7) % len(marbles)
            players[i % 413] += i + marbles[current]
            del marbles[current]
        else:
            current = (current + 2) % len(marbles)
            marbles.insert(current, i)
    return max(players)


def part1():
    # 413 players; last marble is worth 71082 points
    return solve(71082)


def part2():
    return solve(7108200)


print(part1())
print(part2())
