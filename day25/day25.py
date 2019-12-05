row = 3010
col = 3019


def get_coord(row, col):
    stripe = row + col - 2

    start = stripe * (stripe + 1) // 2
    return start + col - 1


c = get_coord(3010, 3019)
# Original solution
# num = 20151125
# for _ in range(c):
#     num = (num * 252533) % 33554393
# print(num)

# Better, after the fact solution
def modexp(g, u, p):
   """
   Compute s = (g ^ u) mod p
   args are base, exponent, modulus
   (see Bruce Schneier's book, _Applied Cryptography_ p. 244)
   """
   s = 1
   while u != 0:
      if u & 1:
         s = (s * g) % p
      u >>= 1
      g = (g * g) % p;
   return s


mod = 33554393
print((modexp(252533, c, mod) * 20151125) % mod)
