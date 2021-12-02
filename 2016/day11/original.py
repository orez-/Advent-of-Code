import collections
import heapq
import itertools
import re


def valid_floor(floor):
    for c in floor:
        if c and c.endswith('m') and (c[:2] + 'g' not in floor) and any(q and q[-1] == 'g' for q in floor):
            return False
    return True


class State:
    def __init__(self, floors, floor, moves, prev=None):
        self.floors = floors
        self.floor = floor
        self.moves = moves
        self.prev = prev

        self._sym = None

    def next_states(self):
        all_items = set(self.floors[self.floor] + [None])
        for one, two in itertools.combinations(all_items, 2):
            left_behind = all_items - {one, two}
            if not valid_floor(left_behind):
                continue

            for next_floor in (self.floor - 1, self.floor + 1):
                # in-bounds
                if 0 <= next_floor < len(self.floors):
                    new_floors = list(map(list, self.floors))
                    new_floors[self.floor] = list(left_behind - {None})
                    new_floors[next_floor].extend({one, two} - {None})
                    if not valid_floor(new_floors[next_floor]):
                        continue

                    yield State(
                        floors=new_floors,
                        floor=next_floor,
                        moves=self.moves + 1,
                        prev=self,
                    )

    def key(self):
        return self.moves + sum(4 - i for i, elems in enumerate(self.floors) for _ in elems)

    def symmetry_value(self):
        if not self._sym:
            _lookup = {
                e: i
                for i, floor in enumerate(self.floors)
                for e in floor
            }
            self._sym = collections.Counter(
                (e_floor, _lookup[e[:2] + 'm'])
                for e, e_floor in _lookup.items()
                if e.endswith('g')
            )
        return self._sym

    def __eq__(self, other):
        return (
            # list(map(set, self.floors)) == list(map(set, other.floors)) and
            self.symmetry_value() == other.symmetry_value() and
            self.floor == other.floor
        )

    def __lt__(self, other):
        return self.moves < other.moves

    def __hash__(self):
        return hash((
            frozenset(self.symmetry_value().items()),
            self.floor,
        ))

    def __repr__(self):
        return '{}\nmoves {}\n'.format(
            '\n'.join(str(floor) + (" <" if self.floor == i else "") for i, floor in enumerate(self.floors)),
            self.moves,
        )


def bfs():
    highest = 0

    floors = [
        # ["prg", "prm"],
        ["prg", "prm", "elg", "elm", "dig", "dim"],
        ["cog", "cug", "rug", "plg"],
        ["com", "cum", "rum", "plm"],
        [],
    ]
    total = sum(map(len, floors))

    st = State(
        floors=floors,
        floor=0,
        moves=0,
    )
    seen = set()
    q = [(st.key(), st)]

    while q:
        _, t = heapq.heappop(q)
        if t.moves > highest:
            print(t.moves)
            highest = t.moves

        if len(t.floors[3]) == total:
            moves = t.moves
            print("=========\n=========\n=========\n")
            while t:
                print(t)
                t = t.prev
            return moves

        for st in t.next_states():
            if st not in seen:
                seen.add(st)
                heapq.heappush(q, (st.key(), st))


if __name__ == '__main__':
    print(bfs())
