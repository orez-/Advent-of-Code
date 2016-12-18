def get_data(a):
    b = a
    b = b[::-1]
    b = b.replace('1', 'z').replace('0', '1').replace('z', '0')

    return "{}0{}".format(a, b)


def get_checksum(data):
    for one, two in zip(data[::2], data[1::2]):
        if one == two:
            yield "1"
        else:
            yield "0"


def main(desired_length):
    data = "10011111011011001"

    while len(data) < desired_length:
        data = get_data(data)
    data = data[:desired_length]

    while True:
        data = ''.join(get_checksum(data))
        if len(data) % 2:
            break

    return data


# print(main(272))  # part 1
print(main(35651584))  # part 2
