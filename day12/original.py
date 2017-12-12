# heyyy fortunately I already had this implementation lying around.
import disjoint_set


def main(file):
    dj = disjoint_set.DisjointSet()
    for line in file:
        one, _, *rest = line.split()
        rest = [r.strip(',') for r in rest]

        for r in rest:
            dj.union(one, r)
    print(sum(1 for _ in dj.find_group('0')))
    print(len(dj))


with open('input.txt', 'r') as file:
    main(file)
