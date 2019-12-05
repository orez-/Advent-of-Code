import itertools

boss = {
    'hp': 103,
    'damage': 9,
    'armor': 2,
}

player_health = 100

# cost, damage, armor
weapons = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
]

armor = [
    (0, 0, 0),  # potentially no armor
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
]

rings = [
    (0, 0, 0),  # potentially only one ring
    (20, 0, 1),
    (25, 1, 0),
    (40, 0, 2),
    (50, 2, 0),
    (80, 0, 3),
    (100, 3, 0),
]

def fight(p1, p2):
    p1_damage = max(p1['damage'] - p2['armor'], 1)
    p2_damage = max(p2['damage'] - p1['armor'], 1)
    p1_turns, m = divmod(p2['hp'], p1_damage)
    p1_turns += bool(m)
    p2_turns, m = divmod(p1['hp'], p2_damage)
    p2_turns += bool(m)
    return p1_turns <= p2_turns


def equipment_iter(reverse=False):
    # 5 * 6 * 21
    ring_options = [[(0, 0, 0), (0, 0, 0)]] + list(itertools.combinations(rings, 2))
    armor_options = sorted(
        itertools.product(weapons, armor, ring_options),
        key=lambda w_a_rr: w_a_rr[0][0] + w_a_rr[1][0] + w_a_rr[2][0][0] + w_a_rr[2][1][0],
        reverse=reverse,
    )
    for w, a, (r1, r2) in armor_options:
        yield map(sum, zip(w, a, r1, r2))

# part 1
# for cost, damage, armor in equipment_iter():
#     player = {
#         'hp': player_health,
#         'damage': damage,
#         'armor': armor,
#     }
#     if fight(player, boss):
#         print(cost)
#         break

# part 2
for cost, damage, armor in equipment_iter(reverse=True):
    player = {
        'hp': player_health,
        'damage': damage,
        'armor': armor,
    }
    if not fight(player, boss):
        print(cost)
        break
