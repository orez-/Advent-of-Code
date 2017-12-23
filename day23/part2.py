def go():
    a = 1
    b = c = d = e = f = g = h = 0


    b = 65  # set b 65
    c = b  # set c b
    if a == 0: # jnz a 2
        # jnz 1 5
        b -= 100000
        c = b
        c += 17000
    else:
        b *= 100  # mul b 100
    while 1:
        f = 1  # set f 1
        d = 2  # set d 2
        while 1:
            e = 2  # set e 2
            while 1:
                # g = d  # set g d
                # mul g e
                # g -= b  # sub g b
                if e * d - b == 0:  # jnz g 2
                    f = 0  # set f 0
                e -= 1  # sub e -1
                # g = e - b  # set g e
                # g -= b  # sub g b
                if e - b == 0:
                    break  # jnz g -8
            d -= 1  # sub d -1
            g = d  # set g d
            g -= b  # sub g b
            if d - b == 0:
                break
        # jnz g -13
        if f == 0:  # jnz f 2
            h += 1 # sub h -1
        g = b  # set g b
        g -= c  # sub g c
        if g == 0:  # jnz g 2
            return h  # jnz 1 3
        b -= 17  # sub b -17
        # jnz 1 -23


print(go())
