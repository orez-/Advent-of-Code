import itertools

def product(iterable):
    iterable = iter(iterable)
    total = next(iterable)
    for e in iterable:
        total *= e
    return total


def nice_colors():
    af = '\x1b[38;5;{}m{{}}\x1b[0m'
    color_codes = [161, 209, 185, 106, 72, 62, 132, 203, 214, 71, 67, 97]
    return itertools.cycle(map(lambda x: x.format, map(af.format, color_codes)))


def convert_solve_for(fn):
    def anon(self, possibilities, value=None, /, *, min=None, max=None):
        if ((min is None) is not (max is None)) or ((min is None) is (value is None)):
            raise TypeError("expected either one positional value or both `min` and `max`")
        if value is not None:
            min = value
            max = value
        return fn(self, possibilities, min=min, max=max)
    return anon


class Expr:
    def __init__(self, var):
        self.var = var
        self.min = -float("inf")
        self.max = float("inf")

    def try_mod(self, other):
        return self

    def try_div(self, other):
        num = other.value
        if self.min // num == self.max // num:
            return IntExpr(self.min // num)
        return None

    def __mul__(self, other):
        if self == 0 or other == 0:
            return IntExpr(0)
        if other == 1:
            return self
        if self == 1:
            return other
        return MulExpr.new(self, other)

    __rmul__ = __mul__

    def __add__(self, other):
        if self == 0:
            return other
        if other == 0:
            return self
        return AddExpr.new(self, other)

    __radd__ = __add__

    def __mod__(self, other):
        if other == 1:
            return IntExpr(0)
        if self.max <= other.min:
            return self
        return ModExpr(self, other)

    def __floordiv__(self, other):
        if other == 1:
            return self
        return Expr(f"({self!r} // {other})")

    def __matmul__(self, other):
        if self.max < other.min or other.max < self.min:
            return [IntExpr(0)]
        if self.min == self.max == other.min == other.max:
            return [IntExpr(1)]
        return [
            AssumptionExpr(IntExpr(1), EqExpr(self, other)),
            AssumptionExpr(IntExpr(0), NeqExpr(self, other)),
        ]

    __rmatmul__ = __matmul__

    def __repr__(self):
        return self.var

    def top_print(self):
        return repr(self)

    @convert_solve_for
    def solve_for(self, possibilities, *, min, max):
        pass
        breakpoint()


class AssumptionExpr(Expr):
    def __init__(self, value, assumption):
        self.value = value
        self.assumption = assumption

    @property
    def min(self):
        return self.value.min

    @property
    def max(self):
        return self.value.max

    def __repr__(self):
        return f"[{self.value}]"


class EqExpr(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.min = 0
        self.max = 1

    def __matmul__(self, other):
        if other == 0:
            return [NeqExpr(self.a, self.b)]
        return super().__matmul__(other)

    def __repr__(self):
        return f"({self.a} == {self.b})"

    def top_print(self):
        return f"({self.a.top_print()} == {self.b.top_print()})"


class NeqExpr(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.min = 0
        self.max = 1

    def __matmul__(self, other):
        if other == 0:
            return [EqExpr(self.a, self.b)]
        return super().__matmul__(other)

    def __repr__(self):
        return f"({self.a} ≠ {self.b})"

    def top_print(self):
        return f"({self.a.top_print()} ≠ {self.b.top_print()})"


class MulExpr(Expr):
    def __init__(self):
        self.terms = []
        self.constant = 1
        self.min = -float('inf')
        self.max = float('inf')

    @classmethod
    def new(cls, a, b):
        self = cls()
        for c in [a, b]:
            if type(c) == IntExpr:
                self.constant *= c.value
            elif type(c) == MulExpr:
                self.terms.extend(c.terms)
                self.constant *= c.constant
            else:
                self.terms.append(c)
        self.min = product(t.min for t in self.terms) * self.constant
        self.max = product(t.max for t in self.terms) * self.constant
        return self

    def try_mod(self, other):
        if self.constant % other == 0:
            return IntExpr(0)
        return self

    def try_div(self, other):
        num = other.value
        if self.constant == num and len(self.terms) == 1:
            return self.terms[0]
        if self.constant % num == 0:
            e = MulExpr()
            e.constant = self.constant // num
            e.terms = self.terms
            e.min = self.min // num
            e.max = self.max // num
            return e
        return super().try_div(other)

    def __repr__(self):
        terms = ' * '.join(map(repr, self.terms))
        if self.constant != 1:
            terms = f"{terms} * {self.constant}"
        return f"({terms})"

    def top_print(self):
        colors = nice_colors()
        terms = ' * '.join(next(colors)(repr(term)) for term in self.terms)
        if self.constant != 1:
            terms = f"{terms} * {next(colors)(self.constant)}"
        return f"({terms})"

    @convert_solve_for
    def solve_for(self, possibilities, *, min, max):
        if min == max == 0:
            def anon(term):
                maybe = set(possibilities)
                term.solve_for(possibilities, 0)
                return maybe
            possibilities &= set.union(*map(anon, self.terms))


class Unit(Expr):
    def __init__(self, var):
        self.var = var
        self.min = 1
        self.max = 9

    @convert_solve_for
    def solve_for(self, possibilities, *, min, max):
        for p in range(1, 10):
            if not (min <= p <= max):
                possibilities.discard((self.var, p))


class IntExpr(Expr):
    def __init__(self, value):
        self.value = value
        self.min = value
        self.max = value

    def __eq__(self, value):
        if type(value) == int:
            return value == self.value
        return NotImplemented

    def __mod__(self, other):
        if type(other) == IntExpr:
            return IntExpr(self.value % other.value)
        return super().__mod__(other)

    def __add__(self, other):
        if type(other) == IntExpr:
            return IntExpr(self.value + other.value)
        return super().__add__(other)

    def __mul__(self, other):
        if type(other) == IntExpr:
            return IntExpr(self.value * other.value)
        return super().__mul__(other)

    def __repr__(self):
        return str(self.value)


class DivExpr(Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.min = a.min // b.value
        self.max = a.max // b.value

    def __repr__(self):
        return f"({self.a} // {self.b})"

    def top_print(self):
        return f"({self.a.top_print()} // {self.b.top_print()})"

    @convert_solve_for
    def solve_for(self, possibilities, *, min, max):
        ...


class ModExpr(Expr):
    def __init__(self, a, b):
        assert type(b) == IntExpr
        print(a.min, a.max)
        num = b.value
        nd, nm = divmod(a.min, num)
        xd, xm = divmod(a.max, num)
        self.min = 0
        self.max = b.value - 1
        if nd == xd:
            self.min = nm
            self.max = xm
        self.a = a
        self.b = b

    def __repr__(self):
        return f"({self.a} % {self.b})"

    def top_print(self):
        return f"({self.a.top_print()} % {self.b.top_print()})"


class AddExpr(Expr):
    def __init__(self):
        self.terms = []
        self.constant = 0
        self.min = -float('inf')
        self.max = float('inf')

    @classmethod
    def new(cls, a, b):
        self = cls()
        for c in [a, b]:
            if type(c) == IntExpr:
                self.constant += c.value
            elif type(c) == AddExpr:
                self.terms.extend(c.terms)
                self.constant += c.constant
            else:
                self.terms.append(c)
        self.min = sum(t.min for t in self.terms) + self.constant
        self.max = sum(t.max for t in self.terms) + self.constant
        return self

    def __mul__(self, other):
        if other == 0:
            return IntExpr(0)
        if other == 1:
            return self
        if type(other) == IntExpr:
            result = AddExpr()
            result.terms = [term * other for term in self.terms]
            result.constant = self.constant * other.value
            result.min = self.min * other.value
            result.max = self.max * other.value
            return result
        return super().__mul__(other)

    def __mod__(self, other):
        num = other.value
        result = IntExpr(self.constant % num)
        for term in self.terms:
            result += term.try_mod(num)
        if 0 <= result.min and result.max < num:
            return result
        return ModExpr(result, other)

    def __floordiv__(self, other):
        if other == 1:
            return self
        num = other.value
        divisible = IntExpr(0)
        not_divisible = IntExpr(0)
        if self.constant % num == 0:
            divisible += IntExpr(self.constant // num)
        else:
            not_divisible += IntExpr(self.constant)
        for term in self.terms:
            div = term.try_div(other)
            if div is None:
                not_divisible += term
            else:
                divisible += div
        if not_divisible == 0:
            return divisible
        shot = not_divisible.try_div(other)
        if shot:
            return divisible + shot
        return divisible + DivExpr(not_divisible, other)

    def __repr__(self):
        terms = ' + '.join(map(repr, self.terms))
        if self.constant:
            terms = f"{terms} + {self.constant}"
        return f"({terms})"

    def top_print(self):
        colors = nice_colors()
        terms = ' + '.join(next(colors)(repr(term)) for term in self.terms)
        if self.constant:
            terms = f"{terms} + {next(colors)(self.constant)}"
        return f"({terms})"

    @convert_solve_for
    def solve_for(self, possibilities, *, min, max):
        if min == max == self.min:
            for term in self.terms:
                term.solve_for(possibilities, min)


class Monad:
    def __init__(self):
        self.constraints = []
        self.regs = {'w': IntExpr(0), 'x': IntExpr(0), 'y': IntExpr(0), 'z': IntExpr(0)}
        self.var = ord('a')
        self.vars = []

    def parse(self, var):
        try:
            return IntExpr(int(var))
        except:
            return self.regs[var]

    def inp(self, a):
        self.regs[a] = Unit(chr(self.var))
        self.vars.append(chr(self.var))
        self.var += 1
        return [self]

    def add(self, a, b):
        self.regs[a] += self.parse(b)
        return [self]

    def mul(self, a, b):
        self.regs[a] *= self.parse(b)
        return [self]

    def div(self, a, b):
        self.regs[a] //= self.parse(b)
        return [self]

    def mod(self, a, b):
        self.regs[a] %= self.parse(b)
        return [self]

    def eql(self, a, b):
        results = self.regs[a] @ self.parse(b)
        answers = []
        for result in results:
            new = self.clone()
            new.regs[a] = result
            if type(result) == AssumptionExpr:
                new.constraints.append(result.assumption)
            answers.append(new)
        return answers

    def clone(self):
        new = Monad()
        new.regs = dict(self.regs)
        new.constraints = list(self.constraints)
        new.var = self.var
        new.vars = self.vars[:]
        return new

    def __repr__(self):
        results = []
        for k in 'wxyz':
            v = self.regs[k]
            results.append(f"{k} [{v.min}..{v.max}]: {v.top_print()}")
        return '\n'.join(results)


import sys
def main():
    monads = [Monad()]
    stop = int(sys.argv[1]) if len(sys.argv) > 1 else float("inf")
    with open("file.txt", "r") as file:
        for i, line in list(enumerate(file)):
            cmd, *args = line.strip().split(" ")
            print(f"{i} [{line.strip()}]")
            new_monads = []
            for monad in monads:
                new_monads.extend(getattr(monad, cmd)(*args))
            monads = new_monads
            for monad in monads:
                print(monad, end="\n\n")
            if i >= stop:
                if input() == "?":
                    breakpoint()
            else:
                print()

        monads = [monad for monad in monads if monad.regs['z'].min <= 0]
        print("Possibilities:")
        for monad in monads:
            print(f"Assuming {'; '.join(c.top_print() for c in monad.constraints)}")
            print(monad)

main()
