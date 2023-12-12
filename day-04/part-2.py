class Card:
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.repetitions = 0

    def __repr__(self):
        return f'Card(value={self.value}, index={self.index}, repetitions={self.repetitions})'

    def find_before_cards(self, cards, received_index):
        result = 0

        for (index, card) in enumerate(cards[0:received_index]):
            if card.value != 0 and card.value + index >= received_index:
                result += card.repetitions

        return result


with open('day-4/part-2.txt') as file:
    cards = []
    index = 0

    for line in file:
        numbers = line.split(': ')[1]
        win_num, my_num = numbers.split('| ')
        win_num = [int(num) for num in win_num.strip().split(' ') if num.isdigit()]
        my_num = [int(num) for num in my_num.strip().split(' ') if num.isdigit()]
        length = len(set(win_num) & set(my_num))

        cards.append(Card(index, length))
        index += 1

    for (i, card) in enumerate(cards):
        if i == 0:
            card.repetitions = 1
        else:
            card.repetitions = card.find_before_cards(cards, i) + 1

    print(sum(card.repetitions for card in cards))