import itertools

def get_valid_passwords():
    for letters in itertools.product('abcdefghjkmnpqrstuvwxyz', repeat=8):
        doubles = set(
            a for a, b in
            zip(letters, letters[1:])
            if a == b
        )
        if len(doubles) > 1 and any(
            ord(a) + 2 == ord(b) + 1 == ord(c)
            for a, b, c in
            zip(letters, letters[1:], letters[2:])
        ):
            yield ''.join(letters)

for pw in get_valid_passwords():
    print(pw)
