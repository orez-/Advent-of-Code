# Messin around with a solution with a faster runtime.
# Biggest changes are precalculating the visible seats and omitting
# the non-seat positions from the board dict.

import itertools


class Board(dict):
    @classmethod
    def from_file(cls, file):
        # empty L, occupied #
        self = cls({
            (x, y): elem == '#'
            for y, row in enumerate(file)
            for x, elem in enumerate(row)
            if elem != '.'
        })
        self.width = len(file[0])
        self.height = len(file)
        return self

    def clone(self):
        board = Board(self)
        board.visible_seats = self.visible_seats
        board.width = self.width
        board.height = self.height
        return board

    def calculate_visible_seats(self):
        self.visible_seats = {
            (x, y): list(visible_around(self, x, y))
            for x, y in self.keys()
        }

    def calculate_nearby_seats(self):
        self.visible_seats = {
            (x, y): list(around(self, x, y))
            for x, y in self.keys()
        }

    def seen_around(self, x, y):
        return sum(
            1 for cx, cy in self.visible_seats[x, y]
            if self[cx, cy]
        )


def around(seats, x, y):
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == dy == 0:
                continue
            if (x + dx, y + dy) in seats:
                yield x + dx, y + dy


def visible_around(seats, x, y):
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == dy == 0:
                continue
            for dd in itertools.count(1):
                cx = x + dx * dd
                cy = y + dy * dd
                if not (cx in range(seats.width) and cy in range(seats.height)):
                    break
                if (cx, cy) in seats:
                    yield cx, cy
                    break


def simulate(file, visibility_method, *, vacate_threshold):
    seats = Board.from_file(file)
    visibility_method(seats)
    progress = True
    while progress:
        new_seats = seats.clone()
        progress = False
        for (x, y), e in seats.items():
            if not e and seats.seen_around(x, y) == 0:
                e = True
                progress = True
            elif e and seats.seen_around(x, y) >= vacate_threshold:
                e = False
                progress = True
            new_seats[x, y] = e
        seats = new_seats
    return sum(1 for s in seats.values() if s)


def part1(file):
    return simulate(file, Board.calculate_nearby_seats, vacate_threshold=4)


def part2(file):
    return simulate(file, Board.calculate_visible_seats, vacate_threshold=5)


def main():
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    print(part1(list(file)))
    print(part2(list(file)))


if __name__ == '__main__':
    main()
