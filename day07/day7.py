import re

class Circuit(object):
    def __init__(self):
        self._context = {}

    def __getitem__(self, name):
        try:
            return int(name)
        except:
            pass
        if name not in self._context:
            raise KeyError
        if not isinstance(self._context[name], int):
            self._context[name] = self._context[name]()
        return self._context[name]

    def __setitem__(self, name, value):
        self._context[name] = value

    def _assign(self, value, assign):
        self[assign] = lambda: self[value]

    def _and(self, left, right, assign):
        self[assign] = lambda: self[left] & self[right]

    def _or(self, left, right, assign):
        self[assign] = lambda: self[left] | self[right]

    def _lshift(self, left, right, assign):
        self[assign] = lambda: self[left] << int(right)

    def _rshift(self, left, right, assign):
        self[assign] = lambda: self[left] >> int(right)

    def _not(self, value, assign):
        self[assign] = lambda: ~self[value] & 65535


commands = [
    (r"([\da-z]+) -> ([a-z]+)", Circuit._assign),
    (r"([\da-z]+) AND ([\da-z]+) -> ([a-z]+)", Circuit._and),
    (r"([\da-z]+) OR ([\da-z]+) -> ([a-z]+)", Circuit._or),
    (r"([\da-z]+) LSHIFT (\d+) -> ([a-z]+)", Circuit._lshift),
    (r"([\da-z]+) RSHIFT (\d+) -> ([a-z]+)", Circuit._rshift),
    (r"NOT ([\da-z]+) -> ([a-z]+)", Circuit._not),
]

circuit = Circuit()
try:
    while True:
        line = raw_input()
        for regex, method in commands:
            match = re.match(regex, line)
            if match:
                method(circuit, *match.groups())
                break
        else:
            raise Exception(line)
except EOFError:
    pass
circuit['b'] = 46065
print circuit['a']
