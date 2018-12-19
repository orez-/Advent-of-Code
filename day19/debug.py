# Not a valid python file, but easier to read with syntax highlighting

d = 10551425
 # 0: jmp 16
 1: b = 1
 2: c = 1
 # 3: e = b * c
 # 4: e = d == e
 if b * c == d:
    a += b
 # 5: jmp +e
 # 6: jmp +1
 # 7: a += b
 8: c += 1
 # 9: e = c > d
 9: if d >= c:
    jmp 2
# 10: jmp +e
# 11: jmp 2
12: b += 1
# 13: e = b > d
13: if d < b:
    quit
# 14: jmp +e
# 15: jmp 1
# 16: I *= I

FIRST TIME SETUP:
d = 836
# 17: d += 2
# 18: d *= d
# 19: d *= 19
# 20: d *= 11
e = 189
# 21: e += 8
# 22: e *= 22
# 23: e += 13
24: d += e
# 25: jmp +a
# 26: jmp 0
e = 10550400
# 27: e = 27
# 28: e *= 28
# 39: e += 29
# 30: e *= 30
# 31: e *= 14
# 32: e *= 32
33: d += e
34: a = 0
35: jmp 0
