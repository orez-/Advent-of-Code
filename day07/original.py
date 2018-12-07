import itertools


file = """
YL
ND
ZA
FL
HG
IS
MU
RJ
TD
UD
OX
BD
XV
JV
DA
KP
QC
SE
AV
GL
CW
PW
VW
EW
WL
PE
TK
AG
GP
NS
RD
MG
ZL
MT
SL
SW
OJ
ZD
AC
PV
AP
BC
RS
XS
TP
YE
GE
YK
JP
IQ
EL
XJ
TX
MO
KA
DW
HC
FR
BQ
MQ
DS
YI
MK
SG
XL
DV
BX
CL
VL
ZQ
ZH
MS
OC
BA
UV
UA
XG
KC
TS
KG
UB
AE
FV
QA
FQ
JL
OE
OQ
IK
IP
JD
QP
SC
UP
SP
OB
ZF
RV
DL
YT
GC
""".strip().split('\n')


def part1(file):
    req = {key: set() for key in set(''.join(file))}
    word = ""

    for first, second in file:
        req[second].add(first)

    while req:
        _, letter = min((len(v), k) for k, v in req.items())
        del req[letter]
        for value in req.values():
            value.discard(letter)
        word += letter

    return word


def part2(file):
    guys = [[0, None] for _ in range(5)]
    delay = 60

    req = {key: set() for key in set(''.join(file))}

    for first, second in file:
        req[second].add(first)

    for t in itertools.count(0):
        if not req and all(guy[0] <= 0 for guy in guys):
            break
        for guy in guys:
            guy[:1] = [guy[0] - 1]
            # done with work
            if guy[0] <= 0:
                if not req:
                    guy[:] = [0, None]
                    continue
                for value in req.values():
                    value.discard(guy[1])

        for guy in guys:
            # ready for work
            if guy[0] <= 0:
                if not req:
                    continue
                more, letter = min((len(v), k) for k, v in req.items())
                if more:
                    guy[:] = [0, None]
                    continue
                del req[letter]
                guy[:] = [ord(letter) - ord('A') + 1 + delay, letter]
    return t - 1



print(part1(list(file)))
print(part2(list(file)))
