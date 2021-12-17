import contextlib

@contextlib.contextmanager
def block():
    class Break(Exception):
        pass
    try:
        yield Break
    except Break:
        pass

class Piet:
    def __init__(self, stdin=""):
        self.stack = []
        self.dp = (1, 0)
        self.cc_left = True
        self.stdin = iter(stdin)

    def __repr__(self):
        # Bottom of the stack is always the same empty frame.
        # It's easiest to initialize it first, but it's only used
        # at the very very end.
        # It's more noise to debug around; just omit it.
        return f"- {self.stack[5:]}"

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
        if b > len(self.stack):
            raise IndexError()
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
    # Populate an empty frame for a final combo
    p.push(10)
    p.push(1)
    p.not_()
    p.duplicate()
    p.duplicate()
    p.duplicate()
    # Populate the bitstream.
    p.duplicate()
    # p.push(1)
    # p.not_()

    p.push(1)
    p.push(1)
    print(p, " # total, shft, shft\n")
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
            print(p, " # total, shft, shft, hexit, bit")
            p.push(3)
            p.push(2)
            p.roll()
            print(p, " # total, shft, hexit, bit, shft")
            p.multiply()  # b = shft * a
            p.push(4)
            p.push(3)
            p.roll()
            p.add()  # total += b
            print(p, " # shft, hexit, total")
            p.push(3)
            p.push(2)
            p.roll()
            p.push(2)
            p.multiply()  # shft *= 2
            print(p, " # hexit, total, shft")
            p.duplicate()
            p.push(4)
            p.push(3)
            p.roll()
            p.push(mask)
            p.mod()  # hexit %= mask
            print(p, " # total, shft, shft, hexit")
            print()
        p.pop()  # 🖼 can just not maintain `hexit` in the last unrolled loop
    p.pop()
    p.pop()
    p.pop()
    p.pop()

    # And now we have encoded the input as a single integer,
    # which we can start poppin bits off of.
    print.enabled = True
    print(p, " # [init] stream")
    while True:
        # Skip version id
        p.push(8)
        p.divide()

        # Check packet type for literals
        p.duplicate()
        p.push(8)
        p.divide()
        p.push(2)
        p.push(1)
        p.roll()
        p.push(8)
        p.mod()
        p.duplicate()
        p.push(1)  # 001 -> 100
        p.subtract()
        p.not_()
        if not p.pointer():  # if p != 4 check the other operators
            print("\n[Operator]")
            print(p, " # [type operator] stream, op")
            p.push(2)
            p.push(1)
            p.roll()
            p.duplicate()
            p.push(2)
            p.divide()
            p.push(2)
            p.push(1)
            p.roll()
            p.push(2)
            p.mod()
            print(p, " # [?] ..., op, stream, length_type_id")
            if p.pointer():  # length type id 1 (sub-packet count)
                p.push(1)
                p.not_()
                p.push(2)
                p.push(1)
                p.roll()
                print(p, " # [start] ..., op, #subpacket, stream")
                for i in range(11)[::-1]:
                    p.duplicate()
                    p.push(2)
                    p.mod()
                    p.push(1 << i)  # 🖼😬
                    p.multiply()
                    p.push(3)
                    p.push(2)
                    p.roll()
                    p.add()
                    p.push(2)
                    p.push(1)
                    p.roll()
                    p.push(2)
                    p.divide()
                print(p, " # [ugh]")
                p.push(1)
                p.not_()  # sub-bits
                p.push(18)  # packet len  XXX: 17? 18? 3 + 3 + 1 + 11, right?
                p.push(1)
                p.push(2)
                p.subtract()  # agg
                # p.push(1)
                # p.not_()
                p.push(4)
                p.push(3)
                p.roll()
                print(p, " # [yo] ...[op, reqd_subpackets, reqd_bits, bits, agg], stream")
            else:  # length type id 0 (sub-bit count)
                p.push(1)
                p.not_()  # reqd_subpackets
                p.duplicate()  # reqd_bits
                p.push(3)
                p.push(2)
                p.roll()
                print(p, " # [start] ..., op, #reqd_subpackets, #reqd_bits, stream")
                for i in range(15)[::-1]:
                    p.duplicate()
                    p.push(2)
                    p.mod()
                    p.push(1 << i)  # 🖼😬
                    p.multiply()
                    p.push(3)
                    p.push(2)
                    p.roll()
                    p.add()
                    p.push(2)
                    p.push(1)
                    p.roll()
                    p.push(2)
                    p.divide()
                print(p, "[augh] ..., [op, reqd_subpackets, reqd_bits] stream")

                p.push(22)  # packet len
                p.push(1)
                p.push(2)
                p.subtract()  # agg
                p.push(3)
                p.push(2)
                p.roll()
                print(p, " # [yoo] ...[op, reqd_subpackets, reqd_bits, bits, agg], stream")
            print(p, " # [operator init'd]")
            continue
        p.pop()
        # Otherwise we're seeking through an integer!
        # p.push(1)  # shft
        p.push(1)  # total
        p.not_()
        p.push(6)  # #bits
        print("\n[Literal]")
        print(p, " # [type literal] ..., stream, total, #bits")

        while True:
            p.push(5)  # bits += 5
            p.add()
            p.push(3)  # pull stream to front
            p.push(2)
            p.roll()
            p.duplicate()  # read a bit off it
            p.push(2)
            p.mod()
            print(p, " # [repeat bit]  ..., total, #bits, stream, repeat?")
            p.push(4)
            p.push(1)
            p.roll()
            print(p, " # [hide repeat] ..., repeat?, total, #bits, stream")
            p.push(2)
            p.divide()
            for x in [8, 4, 2, 1]:  # 🖼🔂
                p.duplicate()
                p.push(2)
                p.mod()
                p.push(x)
                p.multiply()
                print(p, f" # [got {x} bit] ..., repeat?, total, #bits, stream, {x}")
                p.push(4)
                p.push(3)
                p.roll()
                p.add()
                p.push(3)
                p.push(1)
                p.roll()
                print(p, f" # [added {x}!] ..., repeat?, total, #bits, stream")
                p.push(2)
                p.divide()

            p.push(4)
            p.push(3)
            p.roll()
            if not p.pointer():
                break
            print(p, " # [oof] total, #bits, stream")
            p.push(3)  # multiply our total by 16,
            p.push(2)  # since we got more digits coming
            p.roll()
            p.push(16)
            p.multiply()
            p.push(3)
            p.push(2)
            p.roll()
            print(p, " [one set of digits down. we go again]\n")

        print(p, " # [literal done] ..., total, #bits, stream")
        # time to apply this to the outer operator o_o

        while True:
            print("\n[Literal Application]")
            print(p, " # [here goes] ..., [packet], [value, bits], stream")
            # Check agg for -1. If so, just assign.
            p.push(4)
            p.push(3)
            p.roll()
            p.duplicate()
            p.push(1)
            p.add()
            p.not_()
            with block() as end:
                if p.pointer():
                    p.pop()
                    raise end
                print(p, " # [yoof] [op, reqd_packets, reqd_bits, tot_bits], [value, bits], stream, agg")
                p.push(4)
                p.push(3)
                p.roll()
                p.push(8)  # copy `op` to the end
                p.push(7)
                p.roll()
                p.duplicate()
                p.push(9)
                p.push(1)
                p.roll()
                print(p, " # [time to match on last] [op, reqd_packets, reqd_bits, tot_bits], bits, stream, agg, value, op")
                p.duplicate()
                p.push(6)  # `max`
                p.subtract()
                p.not_()
                if p.pointer():
                    p.pop()
                    p.duplicate()
                    p.push(3)
                    p.push(2)
                    p.roll()
                    p.duplicate()
                    print(p, "-")
                    p.push(2)
                    print(p, "-")
                    p.push(4)
                    p.push(2)
                    p.roll()
                    print(p, "~")
                    p.greater()
                    p.roll()
                    print(p, "!?")
                    p.push(4)
                    p.push(1)
                    p.roll()
                    p.pop()
                    print(p, ".")
                    raise end
                p.duplicate()
                p.push(2)  # `min`
                p.subtract()
                p.not_()
                if p.pointer():
                    p.pop()
                    p.duplicate()
                    p.push(3)
                    p.push(2)
                    p.roll()
                    p.duplicate()
                    print(p, "-")
                    p.push(2)
                    print(p, "-")
                    p.push(4)
                    p.push(2)
                    p.roll()
                    print(p, "~")
                    p.push(2)
                    p.push(1)
                    p.roll()
                    p.greater()
                    p.roll()
                    print(p, "!?")
                    p.push(4)
                    p.push(1)
                    p.roll()
                    p.pop()
                    print(p, ".")
                    raise end
                p.duplicate()
                p.push(5)  # `greater`
                p.subtract()
                p.not_()
                if p.pointer():
                    p.pop()
                    p.greater()
                    print(p)
                    p.push(3)
                    p.push(1)
                    p.roll()
                    print(p, ".")
                    raise end
                p.duplicate()
                p.push(3)  # `less`
                p.subtract()
                p.not_()
                if p.pointer():
                    p.pop()
                    p.push(2)
                    p.push(1)
                    p.roll()
                    p.greater()
                    print(p)
                    p.push(3)
                    p.push(1)
                    p.roll()
                    print(p, ".")
                    raise end
                p.duplicate()
                p.push(7)  # `equal`
                p.subtract()
                p.not_()
                if p.pointer():
                    p.pop()
                    p.subtract()
                    p.not_()
                    print(p)
                    p.push(3)
                    p.push(1)
                    p.roll()
                    print(p, ".")
                    raise end
                p.duplicate()
                p.not_()  # `add`
                if p.pointer():
                    p.pop()
                    p.add()
                    p.push(3)
                    p.push(1)
                    p.roll()
                    print(p, ".")
                    raise end
                p.duplicate()
                p.push(4)  # `mult`
                p.subtract()
                p.not_()
                if p.pointer():
                    p.pop()
                    p.multiply()
                    p.push(3)
                    p.push(1)
                    p.roll()
                    print(p, ".")
                    raise end
                if p.stack[-1] != 10:  # XXX
                    raise NotImplementedError(f"you gotta do the other operators {p.stack[-1]}")
                p.pop()
                p.out_number()
                return
            print(p, " # [operator applied] ..., [op, reqd_packets, reqd_bits, tot_bits, agg], [bits] [stream]")
            p.push(6)
            p.push(5)
            p.roll()
            p.push(1)
            p.subtract()  # #packets -= 1
            p.duplicate()
            p.push(7)
            p.push(1)
            p.roll()
            p.not_()
            p.push(3)
            p.push(2)
            p.roll()
            p.duplicate()
            p.push(6)
            p.push(5)
            p.roll()
            p.add()  # increase bits total
            p.push(5)
            p.push(1)
            p.roll()
            print(p, " [bout to drop reqd bits]")
            p.push(6)
            p.push(5)
            p.roll()
            p.push(2)
            p.push(1)
            p.roll()
            p.subtract()  # reduce bits req'd
            p.duplicate()
            p.push(6)
            p.push(1)
            p.roll()
            p.not_()  # bits complete
            p.add()  # done?
            print(p, "~? [op_packet], stream, done?")

            if not p.pointer():
                break

            print("\n[Op Crush]")
            p.push(6)
            p.push(3)
            p.roll()
            p.pop()  # burn `reqd_bits`
            p.pop()  # burn `reqd_packets`
            p.pop()  # burn `op`
            p.push(3)
            p.push(2)
            p.roll()
            p.push(2)
            p.push(1)
            p.roll()
            print(p, " # [crushed!] ...[value, bits], stream")

        # XXX: probably fine to skip this
        # p.duplicate()
        # p.not_()
        # if p.pointer():  # break if the stream is empty
        #     break
    raise Exception("unreachable")
    # p.pop()
    # p.out_number()


# input_line = "C200B40A82"  # 1 + 2
# input_line = "04005AC33890"  # 6 * 9  (bitmode)
# input_line = "880086C3E88112"  # min(7, 8, 9)  (bitmode)
# input_line = "CE00C43D881120"  # max(7, 8, 9)
# input_line = "F600B42582"  # 4 > 3
# input_line = "20546718027401204FE775D747A5AD3C3CCEEB24CC01CA4DFF2593378D645708A56D5BD704CC0110C469BEF2A4929689D1006AF600AC942B0BA0C942B0BA24F9DA8023377E5AC7535084BC6A4020D4C73DB78F005A52BBEEA441255B42995A300AA59C27086618A686E71240005A8C73D4CF0AC40169C739584BE2E40157D0025533770940695FE982486C802DD9DC56F9F07580291C64AAAC402435802E00087C1E8250440010A8C705A3ACA112001AF251B2C9009A92D8EBA6006A0200F4228F50E80010D8A7052280003AD31D658A9231AA34E50FC8010694089F41000C6A73F4EDFB6C9CC3E97AF5C61A10095FE00B80021B13E3D41600042E13C6E8912D4176002BE6B060001F74AE72C7314CEAD3AB14D184DE62EB03880208893C008042C91D8F9801726CEE00BCBDDEE3F18045348F34293E09329B24568014DCADB2DD33AEF66273DA45300567ED827A00B8657B2E42FD3795ECB90BF4C1C0289D0695A6B07F30B93ACB35FBFA6C2A007A01898005CD2801A60058013968048EB010D6803DE000E1C6006B00B9CC028D8008DC401DD9006146005980168009E1801B37E02200C9B0012A998BACB2EC8E3D0FC8262C1009D00008644F8510F0401B825182380803506A12421200CB677011E00AC8C6DA2E918DB454401976802F29AA324A6A8C12B3FD978004EB30076194278BE600C44289B05C8010B8FF1A6239802F3F0FFF7511D0056364B4B18B034BDFB7173004740111007230C5A8B6000874498E30A27BF92B3007A786A51027D7540209A04821279D41AA6B54C15CBB4CC3648E8325B490401CD4DAFE004D932792708F3D4F769E28500BE5AF4949766DC24BB5A2C4DC3FC3B9486A7A0D2008EA7B659A00B4B8ACA8D90056FA00ACBCAA272F2A8A4FB51802929D46A00D58401F8631863700021513219C11200996C01099FBBCE6285106"
# input_line = "9C0141080250320F1802104A08"  # 1 + 3 = 2 * 2
# input_line = "9C005AC2F8F0"  # 5 = 15
# input_line = "F600BC2D8F"  # 5 > 15
# input_line = "D8005AC2A8F0"  # 5 < 15
# input_line = "F14"  # 10
# input_line = "D2FE28"  # 2021
# main(input_line)
main(input())
