import re
# class RowSection(object):

class Row(object):
    def __init__(self, size):
        self.sections = [(0, size - 1, 0)]

    def get_section_bounds(self, start, end):
        var = 0
        for i, section in enumerate(self.sections):
            if var == 0 and section[1] >= start:
                start_index = i
                var = 1
            if var == 1 and section[1] >= end:
                return start_index, i
        raise Exception(start, end, self.sections)

    def _replace_section(self, start, end, new_area):
        a_ind, z_ind = self.get_section_bounds(start, end)

        start_sec = self.sections[a_ind]
        end_sec = self.sections[z_ind]

        # subdivide starting section
        if start_sec[0] != start:
            # Merge
            if start_sec[2] == new_area[0][2]:
                new_area[0] = start_sec[0], new_area[0][1], new_area[0][2]
            # cut
            else:
                new_area.insert(0, (start_sec[0], start - 1, start_sec[2]))
        # match starting section exactly, and previous can merge
        elif a_ind != 0 and self.sections[a_ind - 1][2] == new_area[0][2]:
            new_area[0] = self.sections[a_ind - 1][0], new_area[0][1], new_area[0][2]
            a_ind -= 1

        # subdivide ending section
        if end_sec[2] != end:
            # merge
            if end_sec[2] == new_area[-1][2]:
                new_area[-1] = new_area[-1][0], end_sec[1], new_area[-1][2]
            # cut
            else:
                new_area.append((end + 1, end_sec[1], end_sec[2]))
        # match ending area exactly, and next can merge
        elif z_ind != len(self.sections) - 1 and self.subsections[z_ind + 1][2] == new_area[-1][2]:
            new_area[-1] = new_area[-1][0], self.sections[z_ind + 1][1], new_area[-1][2]
            z_ind += 1
        self.sections[a_ind:z_ind+1] = new_area
        # assert all(e + 1 == s for (_, e, _), (s, _, _) in zip(self.sections, self.sections[1:])), self.sections
        # assert self.sections[0][0] == 0, self.sections
        # assert self.sections[-1][1] == 999, self.sections

    def off(self, start, end):
        self._replace_section(start, end, [(start, end, 0)])

    def on(self, start, end):
        self._replace_section(start, end, [(start, end, 1)])

    def toggle(self, start, end):
        a_ind, z_ind = self.get_section_bounds(start, end)
        subsections = self.sections[a_ind:z_ind+1]
        subsections[0] = (start, subsections[0][1], subsections[0][2])
        subsections[-1] = (subsections[-1][0], end, subsections[-1][2])
        subsections = [(s[0], s[1], not s[2]) for s in subsections]
        self._replace_section(start, end, subsections)

    def __repr__(self):
        return str(self.sections)

    def __str__(self):
        return ''.join(('#' if s[2] else '.') * (s[1] + 1 - s[0]) for s in self.sections)


board = [Row(1000) for _ in xrange(1000)]

commands = {
    'toggle': Row.toggle,
    'turn on': Row.on,
    'turn off': Row.off,
}

try:
    while 1:
        line = raw_input().strip()
        if not line:
            break
        match = re.match(r"(toggle|turn off|turn on) (\d+),(\d+) through (\d+),(\d+)", line)
        command, sx, sy, ex, ey = match.groups()
        command = commands[command]
        sx, sy, ex, ey = map(int, (sx, sy, ex, ey))
        for row in board[sy:ey + 1]:
            command(row, sx, ex)
except EOFError:
    pass

print sum(
    s[1] + 1 - s[0]
    for line in board
    for s in line.sections
    if s[2]
)
