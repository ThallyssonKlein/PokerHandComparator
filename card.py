class Card():
    cardValue = ''
    cardSuit = ''

    def validate_first_char(self, first_char):
        return first_char in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def validate_second_char(self, second_char):
        return second_char in ['S', 'H', 'D', 'C']

    def __init__(self, value):
        switcher = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'T': 10,
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }

        if len(str(value)) == 2 and self.validate_first_char(value[0]) and self.validate_second_char(value[1]):
            self.cardValue = switcher.get(value[0])
            self.cardSuit = value[1]
        else:
            raise Exception("Invalid value provided for a Card")
