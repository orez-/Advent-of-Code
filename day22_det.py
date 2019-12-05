import collections
import functools
import heapq


def mana(amt):
    def decorator(fn):
        @functools.wraps(fn)
        def anon(self, other):
            self.mana -= amt
            self.total_mana += amt
            return fn(self, other)
        anon.mana = amt
        return anon
    return decorator


def tick(player, boss):
    if player.hp <= 0:
        raise Lose

    if 'poison' in player.effects:
        boss.hp -= 3
    if 'recharge' in player.effects:
        player.mana += 101
    player.effects -= decrease

    if boss.hp <= 0:
        raise Win


class Boss(object):
    def __init__(self, hp):
        self.hp = hp
        self.damage = 9

    def clone(self):
        return Boss(self.hp)

    def attack(self, other):
        defense = 7 if 'shield' in other.effects else 0
        other.hp -= self.damage - defense


class Player(object):
    def __init__(self, hp):
        self.hp = hp
        self.mana = 500 # player only
        self.effects = collections.Counter()

        self.total_mana = 0

    def clone(self):
        pl = Player(self.hp)
        pl.mana = self.mana
        pl.total_mana = self.total_mana
        pl.effects = collections.Counter(self.effects)
        return pl

    @mana(53)
    def magic_missile(self, other):
        other.hp -= 4

    @mana(73)
    def drain(self, other):
        other.hp -= 2
        self.hp += 2

    @mana(113)
    def shield(self, other):
        self.effects['shield'] = 6

    @mana(173)
    def poison(self, other):
        self.effects['poison'] = 6

    @mana(229)
    def recharge(self, other):
        self.effects['recharge'] = 5

    def spell_choices(self):
        spells = [
            Player.magic_missile,
            Player.drain,
            Player.shield,
            Player.poison,
            Player.recharge,
        ]
        return [
            sp for sp in spells
            if sp.__name__ not in self.effects and sp.mana <= self.mana
        ]

    def __lt__(self, other):  # ugh
        return (self.total_mana, id(self)) < (other.total_mana, id(other))


decrease = collections.Counter({'shield': 1, 'poison': 1, 'recharge': 1})


class GameOver(Exception):
    pass

class Win(GameOver):
    pass

class Lose(GameOver):
    pass


def search():
    starting_player = Player(50)
    starting_boss = Boss(51)

    q = [(starting_player, starting_boss)]
    first = True  # ugh

    while q:
        pl, bs = heapq.heappop(q)

        if first:
            first = False
        else:
            try:
                tick(pl, bs)
                bs.attack(pl)
                tick(pl, bs)
            except Win:
                return pl.total_mana
            except Lose:
                continue

        # pl.hp -= 1  # part 2
        for spell in pl.spell_choices():
            player = pl.clone()
            boss = bs.clone()

            spell(player, boss)
            heapq.heappush(q, (player, boss))

print(search())
