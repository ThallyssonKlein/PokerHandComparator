from card import Card
from enum import Enum


class PokerHand():
    __cards = []
    handTypeNumber = 0
    Options = Enum('Options', 'WIN LOSS SPLITS_THE_POT')

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

    def isThreeOfAKind(self):
        pass

    def isFourOfAKind(self, hand):
        cards = hand.getCards()
        for i in range(0, len(cards)):
            iCount = 1
            for j in range(i + 1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    iCount += 1
                if iCount == 4:
                    return True
        return False

    def isTwoPair(self):
        pass

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

    def isOnePair(self):
        pass

    def isFlush(self, hand):
        cards = hand.getCards()
        currentSuit = cards[0].cardSuit
        for i in range(1, len(cards)):
            if currentSuit != cards[i].cardSuit:
                return False
            currentSuit = cards[i].cardSuit
        return True

    def isHighCard(self, hand):
        pass

    def defineHand(self, hand):
        if isRoyalFlush(hand):
            hand.handTypeNumber = 10
        elif isStraightFlush(hand):
            hand.handTypeNumber = 9
        elif isFullHouse(hand):
            hand.handTypeNumber = 8

    def __init__(self, cardsStr):
        cards = cardsStr.split(' ')

        if len(cards) != 5:
            raise Exception('Invalid number of cards')

        for card in cards:
            self.__cards.append(Card(value=card))

        defineHand(self)

    def compare_with(self, other):
        pass
