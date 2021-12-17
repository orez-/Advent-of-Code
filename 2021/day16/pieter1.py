class Piet:
    def __init__(self, stdin=""):
        self.stack = []
        self.dp = (1, 0)
        self.cc_left = True
        self.stdin = iter(stdin)

    def __repr__(self):
        return f"Piet({self.stack})"

    def push(self, num, force=False):
        if num <= 0 and not force:
            raise ValueError("unrepresentable")
        self.stack.append(num)

    def pop(self):
        self.stack.pop()

    def add(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b + a)

    def subtract(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b - a)

    def multiply(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b * a)

    def divide(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b // a)

    def mod(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b % a)

    def not_(self):
        a = self.stack.pop()
        self.stack.append(int(not a))

    def greater(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(int(b > a))

    def pointer(self):
        a = self.stack.pop()
        for _ in range(a % 4):
            x, y = self.dp
            self.dp = (-y, x)
        return a % 4  # pseudocode convenience

    def switch(self):
        a = self.stack.pop()
        if a % 2:
            self.cc_left ^= True

    def duplicate(self):
        self.stack.append(self.stack[-1])

    def roll(self):
        a = self.stack.pop()
        b = self.stack.pop()
        focus = self.stack[-b:]
        a %= len(focus)
        self.stack[-b:] = focus[-a:] + focus[:-a]

    def in_number(self):
        raise NotImplementedError
        # n = next(self.stdin)
        # self.stack.append(int(num))

    def in_char(self):
        n = next(self.stdin, None)
        # If no input is waiting on STDIN, this is an error and the command is ignored
        if n is not None:
            self.stack.append(ord(n))

    def out_number(self):
        a = self.stack.pop()
        # print(end=str(a))
        print(a)

    def out_char(self):
        a = self.stack.pop()
        print(end=chr(a))


class Print:
    def __init__(self, enabled=True):
        self.enabled = enabled

    def __call__(self, /, *args, **kwargs):
        if self.enabled:
            print(*args, **kwargs)


def main(stdin):
    print = Print(enabled=False)
    p = Piet(stdin)
    # Populate the bitstream.
    p.push(1)
    p.not_()
    p.duplicate()
    p.push(1)
    p.push(1)
    print(p, " # 0, total, shft, shft\n")
    while True:
        print("--")
        # hex to int: c - (c // 58) * 7 - 48
        p.push(1)
        p.not_()
        p.in_char()
        p.duplicate()
        p.duplicate()
        p.not_()
        if p.pointer():
            break

        p.push(58)
        p.divide()
        p.push(7)
        p.multiply()
        p.subtract()
        p.push(48)
        p.subtract()
        p.add()  # destroy extra duplicate from eofcheck

        # split into bits and add to bitstream
        # 🖼🔂 don't actually for-loop this, this is for pseudocode sanity
        for mask in [8, 4, 2, 1]:  # total += shft * (hexit // mask); hexit %= mask; shft *= 2
            p.duplicate()
            p.push(mask)
            p.divide()  # a = hexit // mask
            print(p, " # 0, total, shft, shft, hexit, bit")
            p.push(3)
            p.push(2)
            p.roll()
            print(p, " # 0, total, shft, hexit, bit, shft")
            p.multiply()  # b = shft * a
            p.push(4)
            p.push(3)
            p.roll()
            p.add()  # total += b
            print(p, " # 0, shft, hexit, total")
            p.push(3)
            p.push(2)
            p.roll()
            p.push(2)
            p.multiply()  # shft *= 2
            print(p, " # 0, hexit, total, shft")
            p.duplicate()
            p.push(4)
            p.push(3)
            p.roll()
            p.push(mask)
            p.mod()  # hexit %= mask
            print(p, " # 0, total, shft, shft, hexit")
            print()
        p.pop()  # 🖼 can just not maintain `hexit` in the last unrolled loop
    p.pop()
    p.pop()
    p.pop()
    p.pop()

    # And now we have encoded the input as a single integer,
    # which we can start poppin bits off of.
    print.enabled = True
    print(p, " # [init] total, stream")
    while True:
        # Add version id
        for x in [4, 2, 1]:  # 🖼🔂
            p.duplicate()
            p.push(2)
            p.mod()
            p.push(x)     # } 🖼 skip these two for x=1
            p.multiply()  # }
            p.push(3)
            p.push(2)
            p.roll()
            p.add()
            p.push(2)
            p.push(1)
            p.roll()
            p.push(2)
            p.divide()
        print(p, " # [post-version] total, stream")

        # Check packet type for literals
        p.duplicate()
        p.push(8)
        p.divide()
        p.push(2)
        p.push(1)
        p.roll()
        p.push(8)
        p.mod()
        p.push(1)  # 001 -> 100
        p.subtract()
        p.not_()
        if not p.pointer():  # if p != 4 start again from the top
            # this part is going to SUUUUCK in part 2
            # but for now we can ignore most of it! 🙃
            print(p, " # [type operator] total, stream")
            p.duplicate()
            p.push(2)
            p.mod()
            if p.pointer():
                print(1)
                p.push(4096)  # 🖼 64 * 64
                p.divide()
            else:
                print(0)
                p.push(65536)  # 🖼 256 * 256
                p.divide()
            print(p, " # [burn header] total, stream")
            continue
        # Otherwise we're seeking through an integer!
        print(p, " # [type literal] total, stream")
        while True:
            p.duplicate()
            p.push(32)
            p.divide()
            p.push(2)
            p.push(1)
            p.roll()
            p.push(2)
            p.mod()

            print(p, " # [literal iteral] total, stream, repeat?")
            if not p.pointer():  # break unless repeat
                break
        p.duplicate()
        p.not_()
        if p.pointer():  # break if the stream is empty
            break
    p.pop()
    p.out_number()


def main2(stdin):
    total = 0
    mult = 1
    for n in stdin:
        bits = int(f"{int(n, 16):0>4b}"[::-1], 2)
        total += bits * mult
        mult <<= 4
    print(total)

# p = Piet("0123456789ABCDEF")
# input_line = "20546718027401204FE775D747A5AD3C3CCEEB24CC01CA4DFF2593378D645708A56D5BD704CC0110C469BEF2A4929689D1006AF600AC942B0BA0C942B0BA24F9DA8023377E5AC7535084BC6A4020D4C73DB78F005A52BBEEA441255B42995A300AA59C27086618A686E71240005A8C73D4CF0AC40169C739584BE2E40157D0025533770940695FE982486C802DD9DC56F9F07580291C64AAAC402435802E00087C1E8250440010A8C705A3ACA112001AF251B2C9009A92D8EBA6006A0200F4228F50E80010D8A7052280003AD31D658A9231AA34E50FC8010694089F41000C6A73F4EDFB6C9CC3E97AF5C61A10095FE00B80021B13E3D41600042E13C6E8912D4176002BE6B060001F74AE72C7314CEAD3AB14D184DE62EB03880208893C008042C91D8F9801726CEE00BCBDDEE3F18045348F34293E09329B24568014DCADB2DD33AEF66273DA45300567ED827A00B8657B2E42FD3795ECB90BF4C1C0289D0695A6B07F30B93ACB35FBFA6C2A007A01898005CD2801A60058013968048EB010D6803DE000E1C6006B00B9CC028D8008DC401DD9006146005980168009E1801B37E02200C9B0012A998BACB2EC8E3D0FC8262C1009D00008644F8510F0401B825182380803506A12421200CB677011E00AC8C6DA2E918DB454401976802F29AA324A6A8C12B3FD978004EB30076194278BE600C44289B05C8010B8FF1A6239802F3F0FFF7511D0056364B4B18B034BDFB7173004740111007230C5A8B6000874498E30A27BF92B3007A786A51027D7540209A04821279D41AA6B54C15CBB4CC3648E8325B490401CD4DAFE004D932792708F3D4F769E28500BE5AF4949766DC24BB5A2C4DC3FC3B9486A7A0D2008EA7B659A00B4B8ACA8D90056FA00ACBCAA272F2A8A4FB51802929D46A00D58401F8631863700021513219C11200996C01099FBBCE6285106"
# input_line = "EE00D40C823060"
# input_line = "38006F45291200"
# input_line = "8A004A801A8002F478"  # => 16
# input_line = "620080001611562C8802118E34"  # => 12
# input_line = "C0015000016115A2E0802F182340"  # => 23
# input_line = "A0016C880162017C3686B18A3D4780"  # => 31
# input_line = "D2FE28"
# main(input_line)
main(input())
