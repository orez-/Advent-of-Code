import itertools

from intcode import Tape


# debug = print
debug = lambda *args, **kwargs: None


def get_to_command(runner):
    chars = []
    for c in runner:
        c = chr(c)
        chars.append(c)
        if ''.join(chars[-8:]) == "Command?":
            result = ''.join(chars)
            debug(result)
            return result
    rest = ''.join(chars).strip()
    if rest:
        print(rest)


def game_generator(tape):
    runner = tape.run()
    while True:
        cmd = yield get_to_command(runner)
        debug(cmd)
        tape.input_extend(cmd)
        tape.input_extend("\n")


def get_safe_items(room):
    bad = [
        "photons",
        "giant electromagnet",
        "infinite loop",
        "escape pod",
        "molten lava",
    ]

    item_text = room.split("Items here:")
    items = []
    if len(item_text) > 1:
        items = item_text[1].split("\n")

    for item in items:
        if item.startswith("-"):
            item = item.lstrip("- ")
            if item not in bad:
                yield item


def part1(file):
    tape = Tape.from_file(file)
    game = game_generator(tape)

    rooms = {}
    x, y = 0, 0

    opposite = {
        "west": "east",
        "south": "north",
        "north": "south",
        "east": "west",
    }
    without = None
    room = next(game)
    while True:
        name = room.strip().partition("\n")[0]
        if name.startswith("==") and name not in rooms:
            rooms[name] = ({d for d in ("north", "south", "east", "west") if d in room}, without)
            rooms[name][0].discard(without)

        for item in get_safe_items(room):
            game.send(f"take {item}")

        dirs, back = rooms[name]
        if dirs:
            direction = dirs.pop()
            room = game.send(direction)
            without = opposite[direction]
        else:
            if back is None:
                break
            room = game.send(back)

    game.send("north")
    game.send("north")
    game.send("west")
    game.send("north")
    game.send("west")

    all_items = {
        "mutex",
        "polygon",
        "jam",
        "prime number",
        "hologram",
        "semiconductor",
        "monolith",
        "weather machine",
    }
    for mset in powerset(all_items):
        for item in all_items:
            if item in mset:
                game.send(f"take {item}")
            else:
                game.send(f"drop {item}")
        game.send("north")


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        file = file_str.rstrip("\n").split('\n')
    part1(list(file))
