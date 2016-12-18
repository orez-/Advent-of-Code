INPUT = "...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^.....^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^"
# ROWS = 40
ROWS = 400000


def main():
    traps = {(1, 1, 0), (0, 1, 1), (1, 0, 0), (0, 0, 1)}

    last_input = [1 if x == '^' else 0 for x in INPUT]
    total = sum(1 for x in last_input if x == 0)

    # print(last_input)
    for q in range(ROWS - 1):
        new_row = []
        for i, _ in enumerate(last_input):
            x = last_input[max(0, i - 1): i + 2]
            if i == 0:
                x = [0] + x
            if len(x) < 3:
                x = x + [0]

            if tuple(x) in traps:
                new_row.append(1)
            else:
                total += 1
                new_row.append(0)
        last_input = new_row

    print(total)

main()
