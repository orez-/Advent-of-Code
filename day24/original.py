import collections
import itertools
import hashlib
import re


class Squad:
    def __init__(self, units, hp, weak, immune, dmg, atk_type, initiative, team):
        self.units = units
        self.hp = hp
        self.weak = weak
        self.immune = immune
        self.dmg = dmg
        self.atk_type = atk_type
        self.initiative = initiative
        self.team = team

    @property
    def effective_power(self):
        return self.units * self.dmg

    def attack_damage(self, target):
        if self.atk_type in target.immune:
            return 0
        if self.atk_type in target.weak:
            return self.effective_power * 2
        return self.effective_power

    def hit(self, damage):
        """Returns killed, units lost"""
        units = damage // self.hp
        self.units -= units
        return (self.units <= 0, units)

    def target_score(self, target):
        return (self.attack_damage(target), target.effective_power, target.initiative)

    def __eq__(self, other):
        return self.initiative == other.initiative

    def __hash__(self):
        return hash(self.initiative)

    def __repr__(self):
        return f"{self.team}({self.initiative}, units={self.units})"


def get_digits(line):
    return (int(match.group(0)) for match in re.finditer(r"\d+", line))


def get_squads(file, team, bonus=0):
    for line in file:
        digs = tuple(get_digits(line))
        if not digs:
            continue
        units, hp, dmg, initiative = tuple(get_digits(line))
        atk_type = re.search(r'(\w+) damage', line).group(1)
        match = re.search(r'weak to (\w+(?:, \w+)?)', line)
        weak = match.group(1).split(', ') if match else []
        match = re.search(r'immune to (\w+(?:, \w+)?)', line)
        immune = match.group(1).split(', ') if match else []
        yield Squad(units, hp, weak, immune, dmg + bonus, atk_type, initiative, team)


def part1(immune_sys_file, infect_sys_file):
    immune_sys = set(get_squads(immune_sys_file, 'Immune'))
    infect_sys = set(get_squads(infect_sys_file, 'Infect'))

    while True:
        immune_priority = sorted(immune_sys, key=lambda im: (im.effective_power, im.initiative), reverse=True)
        imm_targets = set(immune_sys)
        infect_priority = sorted(infect_sys, key=lambda im: (im.effective_power, im.initiative), reverse=True)
        inf_targets = set(infect_sys)

        # Target selection
        targets = []
        for imm in immune_priority:
            try:
                inf_trg = max((
                    inf for inf in inf_targets
                    if imm.attack_damage(inf)
                ), key=lambda inf: imm.target_score(inf))
            except ValueError:
                continue
            targets.append((imm, inf_trg))
            inf_targets.discard(inf_trg)

        for inf in infect_priority:
            try:
                imm_trg = max((
                    imm for imm in imm_targets
                    if inf.attack_damage(imm)
                ), key=lambda imm: inf.target_score(imm))
            except ValueError:
                continue
            targets.append((inf, imm_trg))
            imm_targets.discard(imm_trg)

        # Attack
        targets = sorted(targets, key=lambda elem: elem[0].initiative, reverse=True)
        for atkr, defr in targets:
            if atkr not in immune_sys and atkr not in infect_sys:
                continue
            dmg = atkr.attack_damage(defr)
            if defr.hit(dmg)[0]:  # killed
                immune_sys.discard(defr)
                infect_sys.discard(defr)

        if not immune_sys or not infect_sys:
            return sum(i.units for i in immune_sys | infect_sys)


def part2(immune_sys_file, infect_sys_file):
    for bonus in itertools.count(187):
        immune_sys = set(get_squads(immune_sys_file, 'Immune', bonus=bonus))
        infect_sys = set(get_squads(infect_sys_file, 'Infect'))

        while True:
            immune_priority = sorted(immune_sys, key=lambda im: (im.effective_power, im.initiative), reverse=True)
            imm_targets = set(immune_sys)
            infect_priority = sorted(infect_sys, key=lambda im: (im.effective_power, im.initiative), reverse=True)
            inf_targets = set(infect_sys)

            # Target selection
            targets = []
            for imm in immune_priority:
                try:
                    inf_trg = max((
                        inf for inf in inf_targets
                        if imm.attack_damage(inf)
                    ), key=lambda inf: imm.target_score(inf))
                except ValueError:
                    continue
                targets.append((imm, inf_trg))
                inf_targets.discard(inf_trg)

            for inf in infect_priority:
                try:
                    imm_trg = max((
                        imm for imm in imm_targets
                        if inf.attack_damage(imm)
                    ), key=lambda imm: inf.target_score(imm))
                except ValueError:
                    continue
                targets.append((inf, imm_trg))
                imm_targets.discard(imm_trg)

            # Attack
            targets = sorted(targets, key=lambda elem: elem[0].initiative, reverse=True)
            did_damage = False
            for atkr, defr in targets:
                if atkr not in immune_sys and atkr not in infect_sys:
                    continue
                dmg = atkr.attack_damage(defr)
                killed, lost = defr.hit(dmg)
                if killed:  # killed
                    immune_sys.discard(defr)
                    infect_sys.discard(defr)
                if lost:
                    did_damage = True

            if not did_damage:
                break
            if not immune_sys:
                break
            if not infect_sys:
                return sum(i.units for i in immune_sys)



if __name__ == '__main__':
    with open('file.txt') as f:
        file_str = f.read()
        imm_str, inf_str = file_str.split('\n\n')
        immune_sys = imm_str.strip().split('\n')
        infect_sys = inf_str.strip().split('\n')
    print(part1(list(immune_sys), list(infect_sys)))
    print(part2(list(immune_sys), list(infect_sys)))
