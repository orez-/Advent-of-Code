import itertools

from intcode import Tape


# debug = print
debug = lambda *args, **kwargs: None


def get_to_command(go, input_value=""):
    coll = []
    for c in go:
        c = chr(c)
        coll.append(c)
        if ''.join(coll[-8:]) == "Command?":
            return ''.join(coll)
    rest = ''.join(coll).strip()
    if rest:
        print(rest)


def part1(file):
    tape = Tape.from_file(file)
    go = tape.run()
    rooms = {}
    x, y = 0, 0

    bad = [
        "photons",
        "giant electromagnet",
        "infinite loop",
        "escape pod",
        "molten lava",
    ]
    opposite = {
        "west": "east",
        "south": "north",
        "north": "south",
        "east": "west",
    }
    without = None
    while True:
        room = get_to_command(go)
        name = room.strip().partition("\n")[0]
        if name.startswith("==") and name not in rooms:
            rooms[name] = ({d for d in ("north", "south", "east", "west") if d in room}, without)
            rooms[name][0].discard(without)
        debug(room)
        item_text = room.split("Items here:")
        items = []
        if len(item_text) > 1:
            items = item_text[1].split("\n")

        for i in items:
            if i.startswith("-"):
                i = i.lstrip("- ")
                if i in bad:
                    continue
                cmd = "take " + i + "\n"
                debug(cmd)
                tape.input_extend(cmd)
                get_to_command(go)
        else:
            dirs, back = rooms[name]
            if dirs:
                direction = dirs.pop()
                debug(direction)
                tape.input_extend(f"{direction}\n")
                without = opposite[direction]
            else:
                if back is None:
                    break
                tape.input_extend(f"{back}\n")

    tape.input_extend("north\nnorth\nwest\nnorth\nwest\n")
    for _ in range(5):
        debug(get_to_command(go))

    all_items = [
        "mutex",
        "polygon",
        "jam",
        "prime number",
        "hologram",
        "semiconductor",
        "monolith",
        "weather machine",
    ]
    for mset in powerset(all_items):
        count = len(all_items) + len(mset) + 1
        tape.input_extend(''.join(f"drop {i}\n" for i in all_items))
        tape.input_extend(''.join(f"take {i}\n" for i in mset))
        tape.input_extend("north\n")

        for _ in range(count):
            room = get_to_command(go)
            debug(room)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    part1(list(file))
