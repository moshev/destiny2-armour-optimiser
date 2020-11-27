# one per line in the form
# name of armor
# type mobility resilience recovery discipline intellect strength exotic?
# type is one of the letters h g c l for helmet gauntlets chest leg
# exotic? is a single letter y if the armor is exotic, otherwise nothing
# e.g.
# Eye of Another World
# h 8 6 15 9 7 13 y
# Hood of the Great Hunt
# h 6 9 16 6 11 20
# Name collisions are allowed and will be disambiguated
# by automatically appending an increasing integer
# empty lines and lines starting with # are ignored
armor_data='''
# helmets

Eye of Another World
h 8 6 15 9 7 13 y
Nezarec's Sin
h 2 21 7 6 14 7 y
Skull of Dire Ahamkara
h 16 3 14 9 6 15 y
Felwinter's Helm
h 6 14 10 14 6 9 y
The Stag
h 11 2 22 7 9 13 y
Apotheosis Veil
h 20 3 9 2 21 8 y

Hood of the Great Hunt
h 6 9 16 6 6 20
Simulator Hood
h 7 7 13 14 2 12
Sovereign Hood
h 8 7 17 9 2 16
Seventh Seraph Hood
h 12 7 8 10 9 8
Crystocrene Hood
h 13 9 6 6 11 7
Tesseract Trace IV
h 9 11 12 6 17 9
Tesseract Trace IV
h 17 6 2 2 19 6
Anti-Extinction Hood
h 8 13 6 8 10 9
Seventh Seraph Hood
h 14 2 10 6 15 7
Tesseract Trace IV
h 8 12 8 10 7 13

# gauntlets

Karnstein Armlets
g 16 15 3 6 19 2 y
Winter's Guile
g 6 15 10 14 15 2 y
Aeon Soul
g 6 20 8 7 6 16 y
Getaway Artist
g 6 11 17 8 11 9 y

Anti-Extinction Gloves
g 18 2 6 6 2 16
Seventh Seraph Gloves
g 15 6 9 13 9 7
Calamity Rig Gloves
g 2 21 8 25 2 2
Crystocrene Gloves
g 12 2 11 7 6 12
Crystocrene Gloves
g 13 7 7 8 13 6
Philomath Gloves
g 6 13 9 10 6 14
Philomath Gloves
g 2 2 22 10 7 7
Tesseract Trace IV
g 10 9 10 13 6 12
Insight Vikti Gloves
g 2 16 13 9 13 7
Anti-Extinction Gloves
g 14 8 6 6 7 13

# chest armours

Stormdancer's Brace
c 12 6 6 6 12 6 y
Sanguine Alchemy
c 2 7 25 12 2 15 y
Chromatic Fire
c 8 13 9 10 14 7 y
Phoenix Protocol
c 9 8 15 9 12 6 y

Robes of the Great Hunt
c 14 8 8 12 9 7
Sovereign Robes
c 13 9 7 6 15 9
Iron Truage Vestments
c 7 15 8 8 6 15
Seventh Seraph Robes
c 6 2 16 2 16 6
Robes of the Great Hunt
c 16 6 8 9 12 8
Crystocrene Robes
c 8 16 2 23 6 2
Crystocrene Robes
c 15 2 10 6 6 13
Crystocrene Robes
c 2 10 13 9 6 13
Cinder Pinion Robes
c 16 6 9 10 2 19
Tesseract Trace IV
c 6 10 13 12 14 7
Philomath Robes
c 16 2 7 9 6 10
Calamity Rig Robes
c 14 14 2 9 8 13
Tesseract Trace IV
c 6 7 11 7 20 2
Insight Vikti Robes
c 18 7 2 6 12 6

# leg armours

Geomag Stabilizers
l 2 9 15 2 16 16 y
Transverse Steps
l 14 12 7 18 9 2 y
Promethium Spur
l 2 17 12 24 2 6 y

Simulator Legs
l 2 18 7 16 2 8
Sovereign Legs
l 6 12 7 2 7 19
Sovereign Legs
l 2 2 26 16 12 2
Phobos Warden Boots
l 13 13 2 13 12 6
Philomath Boots
l 2 19 6 14 6 7
Philomath Boots
l 7 7 13 2 20 7
Tesseract Trace IV
l 19 2 10 17 7 2
Simulator Legs
l 11 2 13 2 18 6
Wild Hunt Boots
l 9 8 10 7 19 2
Seventh Seraph Boots
l 17 2 6 2 17 7
Sovereign Legs
l 2 18 7 7 6 12
Philomath Boots
l 13 12 2 13 6 6
'''


import collections
import itertools


Armor = collections.namedtuple('Armor', ['name', 'slot', 'mob', 'res', 'rec', 'dis', 'int', 'str', 'exotic'])


def next_line(il):
    while True:
        result = next(il).strip()
        if result and result[0] != '#':
            return result


def parse_iter(il):
    '''
    il - iterator over a list of lines
    returns a dict of slot to list of items
    '''
    seen = dict()
    result = dict()
    for debug_index in itertools.count():
        try:
            name = next_line(il)
            spec = next_line(il)
        except StopIteration:
            break
        try:
            spec = spec.split()
            for i in range(6):
                spec[i+1] = int(spec[i+1])
            slot = spec[0]
            if slot not in result:
                result[slot] = []
            key = (slot, name)
            if key in seen:
                # we've seen this name in this slot, append number
                firstidx, count = seen[key]
                if count == 1:
                    # if this is the second item with this name, must edit first one to also have a number (1)
                    first = list(result[slot][firstidx])
                    first[0] += ' (1)'
                    result[slot][firstidx] = Armor(*first)
                count += 1
                name += ' (' + str(count) + ')'
                seen[key] = (firstidx, count)
            else:
                firstidx = len(result[slot])
                seen[key] = (firstidx, 1)
            if len(spec) == 7:
                # not exotic, append
                spec.append(False)
            else:
                # convert to bool
                spec[7] = (spec[7] == 'y')
            result[slot].append(Armor(name, *spec))
        except:
            print('Error parsing line {}, name = {}'.format(debug_index, name))
            import traceback
            traceback.print_exc()
            return None
    return result


def find_best(armors, compare):
    '''
    armors - dict of slot to list of Armor
    compare - comparator function, like strcmp
    return - list of all best combinations
    '''
    best = None
    all_combos = itertools.product(*(armors[slot] for slot in armors))
    for combo_tuple in all_combos:
        if sum(piece.exotic for piece in combo_tuple) > 1:
            # not valid, can't have two or manyer exotics
            continue
        combo = {piece.slot: piece for piece in combo_tuple}
        if best is None:
            best = [combo]
        else:
            cmp = compare(best[0], combo)
            if cmp == 0:
                best.append(combo)
            elif cmp > 0:
                best = [combo]
    return best


def print_combo(combo):
    print(' ' * 32, 'mob', 'res', 'rec', 'dis', 'int', 'str')
    data_template = '{0:32s} {2:3d} {3:3d} {4:3d} {5:3d} {6:3d} {7:3d}'
    for slot in 'hgcl':
        piece = combo[slot]
        print(data_template.format(*piece))
    print(data_template.format(
        'total',
        None,
        *(sum(piece[idx] for piece in combo.values()) for idx in range(2, 8))
    ))


def score_total(combo):
    return sum(sum(piece[2:8]) for piece in combo.values())


def score_effective_total(combo):
    return sum(sum(piece[i] for piece in combo.values()) // 10 for i in range(2, 8))


def score_max_waste(combo):
    return -max(sum(piece[i] for piece in combo.values()) % 5 for i in range(2, 8))


def score_total_waste(combo):
    return -sum(sum(piece[i] for piece in combo.values()) % 5 for i in range(2, 8))


def score_has_exotic(combo):
    return any(piece.exotic for piece in combo.values())


def score_no_exotic(combo):
    return all(not piece.exotic for piece in combo.values())


def make_score_require(slot, name):
    '''
    return - a scoring function that returns if the combo has the named piece in the slot
    '''
    def score_has_piece(combo):
        return combo[slot].name.startswith(name)
    return score_has_piece


def compare_by(*scores):
    def compare(a, b):
        for score in scores:
            sa = score(a)
            sb = score(b)
            res = sb - sa
            if res != 0:
                return res
        return 0
    return compare


a = parse_iter(iter(armor_data.split('\n')))

b1 = find_best(a, compare_by(score_effective_total))
#b1 = find_best(a, compare_by(make_score_require('h', 'Hood of the Great'), make_score_require('c', 'Robes of the Great'), score_effective_total))
b1 = sorted(b1, key=score_total_waste)
print('Best overall:')
for b in b1: print_combo(b)

b2 = find_best(a, compare_by(make_score_require('c', 'Phoenix Protocol'), score_effective_total))
print()
print('Best with Phoenix Protocol:')
for b in b2: print_combo(b)
