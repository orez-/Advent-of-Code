import collections
import itertools


file = """
################################
####################.......#####
##################.G.......###.#
##################...G.........#
#############................###
############..............######
############...##......#########
############...G.....#.#########
##..##........G##.........######
##..##.....#.G...........E#..###
##..##.....#.....G......G..E..##
##G............................#
#....G........#####..G.........#
#......#.G...#######..E.......##
#...##..G...#########E.....#####
##...G.#....#########.....######
######G.G...#########..#.#######
######.#...G#########.##########
#####.......#########.##########
#####.GE.....#######..##########
#####.....E...#####...##########
#######....G..........##########
#######..........G..############
######.G............############
#########...........#..#########
############..........##########
############E...E.##...#########
#############.....E..E.#########
##############.........#########
##############...#....##########
###############..#.#############
################################
""".strip().split('\n')


def test_one():
    test_file = """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
    """.strip().split('\n')
    assert part2(list(test_file)) == 4988
    # 29 * 172 = 4988


def test_two():
    test_file = """
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
    """.strip().split('\n')
    assert part2(list(test_file)) == 31284
    # 33 * 948 = 31284


def test_three():
    test_file = """
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
    """.strip().split('\n')
    assert part2(list(test_file)) == 3478
    # 37 * 94 = 3478

def test_four():
    test_file = """
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
    """.strip().split('\n')
    assert part2(list(test_file)) == 6474
    # 39 * 166 = 6474

def test_five():
    test_file = """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
    """.strip().split('\n')
    assert part2(list(test_file)) == 1140
    # 30 * 38 = 1140


class Unit:
    def __init__(self, team, atk=3):
        self.team = team
        self.atk = atk if team == 'E' else 3
        self.health = 200

    @property
    def died(self):
        return self.health <= 0

    def move(self, position, board, units):
        y, x = position
        if any(self.enemies_near(position, units)):
            return position
        next_pos = self._next_pos(position, board, units)
        if not next_pos:
            return position
        del units[position]
        units[next_pos] = self
        return next_pos

    def _next_pos(self, position, board, units):
        """
        Get the coordinate of the next tile to move to.

        Finding next position is _weird_. We need to first identify all
        the closest valid positions, then pick the first one in reading
        order, then figure out the fastest way to get there, preferring
        reading order in case of a tie. This is subtly different from
        doing a BFS with moves in reading order:

        ########
        #.E....#
        #....,.#
        #...,G.#
        #,.,G..#
        #G,....#
        ########

        John Rambelf over here wants to move to one of the commas, but
        doing a simple ordered BFS on this input will see him heading
        left then down to the bottom-left goblin. Instead, we need a
        separate explicit step to identify that we prefer the topmost
        comma.
        """
        # bfs
        seen = {position}
        q = collections.deque([(position, 0)])
        from_ = {}
        answers = set()
        best_moves = None
        while q:
            (y, x), moves = q.popleft()
            if answers and moves > best_moves:
                goal = min(answers)
                while from_[goal] != position:
                    goal = from_[goal]
                return goal

            for oy, ox in [(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)]:
                if board[oy, ox] == '#' or (oy, ox) in seen:
                    continue
                if (oy, ox) in units:
                    if units[oy, ox].team != self.team:
                        answers.add((y, x))
                        best_moves = moves
                    continue
                seen.add((oy, ox))
                q.append(((oy, ox), moves + 1))
                from_[oy, ox] = (y, x)
        if answers:
            goal = min(answers)
            while from_[goal] != position:
                goal = from_[goal]
            return goal

    def enemies_near(self, position, units):
        y, x = position
        return [
            (units[oy, ox].health, oy, ox, units[oy, ox])
            for oy, ox in [(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)]
            if (oy, ox) in units and units[oy, ox].team != self.team
        ]

    def attack(self, position, units):
        surrounding = self.enemies_near(position, units)
        if not surrounding:
            return False
        _, uy, ux, unit = min(surrounding)
        unit.health -= self.atk
        if unit.died:
            del units[uy, ux]
            return True
        return False


def print_board(board, units):
    height = len(file)
    width = len(file[0])
    agg = collections.deque()
    for y in range(height):
        for x in range(width):
            if (y, x) in units:
                agg.append(units[y, x].team)
            else:
                agg.append(board[y, x])
        agg.append('\n')
    print(''.join(agg))


def part1(file):
    units = {
        (y, x): Unit(elem)
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
        if elem in 'EG'
    }
    board = {
        (y, x): elem if elem not in 'EG' else '.'
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
    }
    for i in itertools.count(0):
        for (y, x), unit in sorted(units.items()):
            kill_last = False
            if unit.died:
                continue
            y, x = unit.move((y, x), board, units)
            kill = unit.attack((y, x), units)
            if kill:
                kill_last = True
        if len({unit.team for unit in units.values()}) < 2:
            i += kill_last
            return i * sum(unit.health for unit in units.values())


def prt2(board, units):
    for i in itertools.count(0):
        for (y, x), unit in sorted(units.items()):
            kill_last = False
            if unit.died:
                continue
            y, x = unit.move((y, x), board, units)
            kill = unit.attack((y, x), units)
            if kill and unit.team == 'G':
                return False
            if kill:
                kill_last = True
        if len({unit.team for unit in units.values()}) < 2:
            i += kill_last
            return i * sum(unit.health for unit in units.values())


def part2(file):
    board = {
        (y, x): elem if elem not in 'EG' else '.'
        for y, row in enumerate(file)
        for x, elem in enumerate(row)
    }
    for atk in itertools.count(4):
        units = {
            (y, x): Unit(elem, atk)
            for y, row in enumerate(file)
            for x, elem in enumerate(row)
            if elem in 'EG'
        }
        result = prt2(board, units)
        if result:
            return result


if __name__ == '__main__':
    print(part1(list(file)))
    print(part2(list(file)))
