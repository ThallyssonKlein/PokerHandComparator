class Card():
    __value = ''
    cardValue = ''
    cardSuit = ''

    def validate_first_char(first_char):
        return first_char in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    def validate_second_char(second_char):
        return second_char in ['S', 'H', 'D', 'C']
    def __init__(self, value):
        if len(str(value)) == 2 and validate_first_char(value[0]) and validate_second_char(value[1]):
            self.__value = value
            self.cardValue = value[0]
            self.cardSuit = value[1]
        else:
            raise Exception("Invalid value provided for a Card")
