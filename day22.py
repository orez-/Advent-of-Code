import collections
import functools
import random


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


class Player(object):
    def __init__(self, hp):
        self.hp = hp
        self.mana = 500 # player only
        self.damage = 9  # boss only
        self.effects = collections.Counter()

        self.total_mana = 0

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
            self.magic_missile,
            self.drain,
            self.shield,
            self.poison,
            self.recharge,
        ]
        return [
            sp for sp in spells
            if sp.__name__ not in self.effects and sp.mana <= self.mana
        ]

    def tick(self, other):
        if self.hp <= 0:
            raise Lose

        if 'poison' in self.effects:
            other.hp -= 3
        if 'recharge' in self.effects:
            self.mana += 101
        self.effects -= decrease

        if other.hp <= 0:
            raise Win

    def attack(self, other):
        defense = 7 if 'shield' in other.effects else 0
        other.hp -= self.damage - defense


decrease = collections.Counter({'shield': 1, 'poison': 1, 'recharge': 1})


class GameOver(Exception):
    pass

class Win(GameOver):
    pass

class Lose(GameOver):
    pass


def fight():
    player = Player(50)
    boss = Player(51)
    try:
        while True:
            # player.hp -= 1  # part 2
            choices = player.spell_choices()
            if not choices:
                raise Lose
            random.choice(choices)(boss)
            player.tick(boss)
            boss.attack(player)
            player.tick(boss)
    except GameOver as result:
        if type(result) == Win:
            return player.total_mana


best_mana = 999999
while True:
    result = fight()
    if result and result < best_mana:
        best_mana = result
        print(best_mana)
