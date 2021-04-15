from card import Card
from enum import Enum


class PokerHand():
    __cards = []
    handTypeNumber = 0
    Options = Enum('Options', 'WIN LOSS SPLITS_THE_POT')

    def getCards(self):
        return self.__cards

    def __init__(self, cardsStr):
        cards = cardsStr.split(' ')

        if len(cards) != 5:
            raise Exception('Invalid number of cards')

        for card in cards:
            self.__cards.append(Card(value=card))

        defineHand(self)

    def defineHand(self, hand):
        if isRoyalFlush(hand):
            hand.handTypeNumber = 10
        elif isStraightFlush(hand):
            hand.handTypeNumber = 9

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

    def isFourOfAKind(self):
        pass

    def isTwoPair(self):
        pass

    def isFullHouse(self):
        pass

    def isOnePair(self):
        pass

    def compare_with(self, other):
