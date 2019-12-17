import itertools

from intcode import Tape


def get_board(file):
    tape = Tape.from_file(file)
    return ''.join(map(chr, tape.run())).strip()


def fetch_path(board):
    width = range(len(board[0]))
    height = range(len(board))
    for y, row in enumerate(board):
        if "^" in row:
            x = row.index("^")
            break

    fx, fy = -1, 0
    path = ["L"]

    while True:
        nx = x + fx
        ny = y + fy
        if nx in width and ny in height and board[ny][nx] == "#":
            path.append("1")
            x, y = nx, ny
        else:
            # 0, -1 => -1, 0
            lx, ly = x + fy, y - fx
            rx, ry = x - fy, y + fx
            if lx in width and ly in height and board[ly][lx] == "#":
                path.extend("L1")
                fx, fy = fy, -fx
                x, y = lx, ly
            elif rx in width and ry in height and board[ry][rx] == "#":
                path.extend("R1")
                fx, fy = -fy, fx
                x, y = rx, ry
            else:
                # done
                return ''.join(path)


# def set_cs(string):
#     start = None
#     walk = iter(enumerate(substring))
#     for start, elem in walk:
#         if elem not in "ABC"
#             break

#     for end, elem in walk:
#         if elem in "ABC":
#             end -= 1
#             break

#     for _ in range(end + 1 - start)[::-1]:


def chunk_to_substrings(string, depth=0):
    REPSTR = "CBA"
    best = 0
    substring = ""
    for length in range(len(string))[::-1]:
        for start in range(len(string) - length + 1):
            substring = string[start: start + length]
            if "A" in substring or "B" in substring or "C" in substring:
                continue
            if not is_legal(substring):
                continue
            potential = string.replace(substring, REPSTR[depth])
            if sum(1 for c in potential if c in "ABC") > 10:
                continue
            print(REPSTR[depth], potential)
            if depth == 2:
                if all(c in "ABC" for c in potential):
                    return potential, get_compressed(substring)
                return False
            else:
                result = chunk_to_substrings(potential, depth+1)
                if result:
                    return (*result, get_compressed(substring))
    return False


# def find_best_substring(string):
#     best = 0
#     substring = ""
#     for i in range(len(string) - 1):
#         for j in range(i + 1, len(string)):
#             if string[j - 1] in "ABC":
#                 break
#             score = string.count(string[i:j]) * (j - i)
#             if score > best:
#                 if not is_legal(string[i:j]):
#                     break
#                 best = score
#                 substring = string[i:j]
#     return substring


def get_compressed(string):
    return ','.join(
        str(sum(1 for _ in ct)) if ch == "1" else ch
        for ch, ct in itertools.groupby(string)
    )


def is_legal(substring):
    return len(get_compressed(substring)) <= 20


def part1(file):
    board = get_board(file)
    board = board.split("\n")

    total = 0
    for y, row in enumerate(board[1:-1], 1):
        for x, elem in enumerate(row[1:-1], 1):
            if elem == board[y-1][x] == board[y+1][x] == board[y][x+1] == board[y][x-1] == "#":
                total += x * y
    return total


def part2(file):
    board = get_board(file)

    tape = Tape.from_file(file)
    tape._memory[0] = 2

    path = fetch_path(board.split("\n"))
    # print(get_compressed(path))

    # substring = chunk_to_substrings(path)
    # print(substring)

    tape.input_extend(
        "A,B,A,B,C,C,B,A,B,C\n"
        "L,12,L,6,L,8,R,6\n"
        "L,8,L,8,R,4,R,6,R,6\n"
        "L,12,R,6,L,8\n"
        "n\n"
    )
    *result, score = tape.run()
    # Program output:
    # print("".join(map(chr, result)))
    return score


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.strip().split('\n')
    print(part1(list(file)))
    print(part2(list(file)))
