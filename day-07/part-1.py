from pprint import pp

from dataclasses import dataclass
from collections import Counter
from collections import defaultdict
from itertools import chain


@dataclass
class Hand:
    cards: list
    bid: int

    def type(self):
        c = Counter(self.cards)

        if len(c) == 1:
            return 'five_kind'

        if len(c) == 2:
            if c.most_common(1)[0][1] == 4:
                return 'four_kind'

            if c.most_common(1)[0][1] == 3:
                return 'full_house'

        if len(c) == 3:
            if c.most_common(1)[0][1] == 3:
                return 'three_kind'

            if c.most_common(1)[0][1] == 2:
                return 'two_pair'

        if len(c) == 4:
            return 'one_pair'

        return 'high_card'

    def sort_key(self):
        return ''.join(chr(i) for i in self.cards)


def parse_card(line):
    hand, bid = line.split(' ')

    int_hand = []
    cards_values = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11,
        'T': 10
    }

    for c in hand:
        if c in cards_values:
            card_value = cards_values[c]
        else:
            card_value = int(c)

        int_hand.append(card_value)

    return Hand(cards=int_hand, bid=int(bid))


with open('input.txt') as f:
    lines = f.read().splitlines()

hands = []
for line in lines:
    hands.append(parse_card(line))

groups = defaultdict(list)
for hand in hands:
    groups[hand.type()].append(hand)

for k, v in groups.items():
    v.sort(key=lambda x: x.sort_key())

hands = chain(
    groups['high_card'],
    groups['one_pair'],
    groups['two_pair'],
    groups['three_kind'],
    groups['full_house'],
    groups['four_kind'],
    groups['five_kind']
)

total = sum(hand.bid * (idx + 1) for idx, hand in enumerate(hands))
pp(total)