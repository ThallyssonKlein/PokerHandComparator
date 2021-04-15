from card import Card
from custom_enum import Result


class PokerHand():
    __cards = []
    handTypeNumber = 0
    __definedHand = False

    def getCards(self):
        return self.__cards

    def isRoyalFlush(self, hand):
        cards = hand.getCards()
        suit = cards[0].cardSuit
        for card in cards:
            if not card.cardValue in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                return False
            if card.cardSuit != suit:
                return False
        return True

    def isStraight(self, hand):
        cards = hand.getCards()
        currentValue = cards[0].cardValue
        for i in range(1, len(cards)):
            if currentValue < i:
                currentValue = cards[i].cardValue
            else:
                return False
        return True

    def isStraightFlush(self, hand):
        cards = hand.getCards()
        currentSuit = cards[0].cardSuit
        currentValue = cards[0].cardValue
        for i in range(1, len(cards)):
            if currentValue < i and cards[i].cardSuit == currentSuit:
                currentValue = cards[i].cardValue
                currentSuit = cards[i].cardSuit
            else:
                return False
        return True

    def ofAKind(self, cards, count):
        for i in range(0, len(cards)):
            iCount = 1
            for j in range(i + 1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    iCount += 1
                if iCount == count:
                    return True
        return False

    def isThreeOfAKind(self, hand):
        cards = hand.getCards()
        return self.ofAKind(cards, 3)

    def isFourOfAKind(self, hand):
        cards = hand.getCards()
        return self.ofAKind(cards, 4)

    def isTwoPair(self, hand):
        cards = hand.getCards()
        firstPairValue = None
        for i in range(0, len(cards)):
            for j in range(1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    firstPairValue = cards[i].cardValue

        for i in range(0, len(cards)):
            for j in range(1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue and cards[j].cardValue != firstPairValue:
                    return True
        return False

    def isFullHouse(self, hand):
        cards = hand.getCards()
        hasThree = False
        for i in range(0, len(cards)):
            if not hasThree:
                iCount = 1
                for j in range(i + 1, len(cards)):
                    if cards[i].cardValue == cards[j].cardValue:
                        iCount += 1
                    if iCount == 3:
                        hasThree = True
                        iCount = 0
            else:
                iCount = 1
                for j in range(i + 1, len(cards)):
                    if cards[i].cardValue == cards[j].cardValue:
                        iCount += 1
                    if iCount == 2:
                        return True
        return False

    def isOnePair(self, hand):
        cards = hand.getCards()
        firstPairValue = None
        for i in range(0, len(cards)):
            for j in range(1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    return True
        return False

    def isFlush(self, hand):
        cards = hand.getCards()
        currentSuit = cards[0].cardSuit
        for i in range(1, len(cards)):
            if currentSuit != cards[i].cardSuit:
                return False
            currentSuit = cards[i].cardSuit
        return True

    def winOrLoseHighestCard(self, hand1, hand2):
        valuesHandOne = []
        valuesHandTwo = []

        cards = hand1.getCards()
        for card in cards:
            valuesHandOne.append(card.cardValue)

        cards = hand2.getCards()
        for card in cards:
            valuesHandTwo.append(card.cardValue)

        return max(valuesHandOne) > min(valuesHandTwo)

    def defineHand(self, hand):
        if self.isRoyalFlush(hand):
            hand.handTypeNumber = 10
            return True
        elif self.isStraightFlush(hand):
            hand.handTypeNumber = 9
            return True
        elif self.isFourOfAKind(hand):
            hand.handTypeNumber = 8
            return True
        elif self.isFullHouse(hand):
            hand.handTypeNumber = 7
            return True
        elif self.isFlush(hand):
            hand.handTypeNumber = 6
            return True
        elif self.isStraight(hand):
            hand.handTypeNumber = 5
            return True
        elif self.isThreeOfAKind(hand):
            hand.handTypeNumber = 4
            return True
        elif self.isTwoPair(hand):
            hand.handTypeNumber = 3
            return True
        elif self.isOnePair(hand):
            hand.handTypeNumber = 2
            return True

        return False

    def __init__(self, cardsStr):
        cards = cardsStr.split(' ')

        if len(cards) != 5:
            raise Exception('Invalid number of cards')

        for card in cards:
            self.__cards.append(Card(value=card))

        self.__definedHand = self.defineHand(self)

    def compare_with(self, other):
        definedHand = self.defineHand(other)

        if not self.__definedHand and not definedHand:
            if self.winOrLoseHighestCard(self, other):
                return Result.WIN
            else:
                return Result.LOSS
        elif not self.__definedHand and definedHand:
            return Result.LOSS
        elif self.__definedHand and not definedHand:
            return Result.WIN
        else:
            if self.handTypeNumber > other.handTypeNumber:
                return Result.WIN
            elif self.handTypeNumber < other.handTypeNumber:
                return Result.LOSS
