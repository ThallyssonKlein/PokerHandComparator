from card import Card
from custom_enum import Result


class PokerHand():
    cards = []
    handScore = 0
    definedHand = False
    number1 = None
    number2 = None

    def getCards(self):
        return self.cards
    def getCardsAsArray(self):
        forReturn = []
        for card in self.cards:
            forReturn.append(card.cardValue)
        return forReturn

    def isRoyalFlush(self, hand):
        cards = hand.getCards()
        value = cards[0].cardValue
        suit = cards[0].cardSuit
        for i in range(1, len(cards)):
            card = cards[i]
            if card.cardSuit != suit or card.cardValue not in [10,11,12,13,14] or card.cardValue == value:
                return False
            else:
                value = card.cardValue
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
                    self.number1 = cards[i].cardValue
                    return True
        return False
    
    def isFourOfAKind(self, hand):
        cards = hand.getCards()
        return self.ofAKind(cards, 4)
    
    def isFullHouse(self, hand):
        cards = hand.getCards()
        hasThree = False
        threeValue = None
        for i in range(0, len(cards)):
            iCount = 1
            for j in range(i + 1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    iCount += 1
                if iCount == 3:
                    hasThree = True
                    threeValue = cards[i].cardValue
                    iCount = 0
        if threeValue:
            for i in range(0, len(cards)):
                iCount = 1
                for j in range(i + 1, len(cards)):
                    if cards[i].cardValue == cards[j].cardValue and cards[i].cardValue != threeValue:
                        iCount += 1
                    if iCount == 2:
                        self.number1 = threeValue
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
    
    def isStraight(self, hand):
        cards = hand.getCards()
        currentValue = cards[0].cardValue
        for i in range(1, len(cards)):
            if currentValue < cards[i].cardValue:
                currentValue = cards[i].cardValue
            else:
                return False
        return True

    def isThreeOfAKind(self, hand):
        cards = hand.getCards()
        return self.ofAKind(cards, 3)

    def isTwoPair(self, hand):
        cards = hand.getCards()
        firstPairValue = None
        doQuit = False
        for i in range(0, len(cards)):
            if doQuit:
                break
            for j in range(i + 1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    firstPairValue = cards[i].cardValue
                    doQuit = True
                    break

        for i in range(0, len(cards)):
            for j in range(i + 1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue and cards[i].cardValue != firstPairValue:
                    self.number1 = cards[i].cardValue
                    self.number2 = firstPairValue
                    return True
        return False

    def isOnePair(self, hand):
        cards = hand.getCards()
        firstPairValue = None
        for i in range(0, len(cards)):
            for j in range(i + 1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    self.number1 = cards[j].cardValue
                    return True
        return False

    def __init__(self, cardsStr):
        cards = cardsStr.split(' ')

        if len(cards) != 5:
            raise Exception('Invalid number of cards')

        tmpArray = []
        for card in cards:
            tmpArray.append(Card(value=card))
        self.cards = tmpArray

        if self.isRoyalFlush(self):
            self.handScore = 9
        elif self.isStraightFlush(self):
            self.handScore = 8
        elif self.isFourOfAKind(self):
            self.handScore = 7
        elif self.isFullHouse(self):
            self.handScore = 6
        elif self.isFlush(self):
            self.handScore = 5
        elif self.isStraight(self):
            self.handScore = 4
        elif self.isThreeOfAKind(self):
            self.handScore = 3
        elif self.isTwoPair(self):
            self.handScore = 2
        elif self.isOnePair(self):
            self.handScore = 1


    def commonTie(self, firstHandValues, secondHandValues):
        if max(firstHandValues) > max(secondHandValues):
            return Result.WIN
        else:
            return Result.LOSS
    
    def compare_with(self, other):
        firstHandValues = self.getCardsAsArray()
        secondHandValues = other.getCardsAsArray()

        if self.handScore > other.handScore:
            return Result.WIN
        elif self.handScore < other.handScore:
            return Result.LOSS
        else:
            if self.handScore == 8 or self.handScore == 5 or self.handScore == 4:
                return self.commonTie(firstHandValues, secondHandValues)
            elif self.handScore == 7 or self.handScore == 6 or self.handScore == 3:
                if self.number1 > other.number1:
                    return Result.WIN
                else:
                    return Result.LOSS
            elif self.handScore == 2:
                firstPairFirstHand = self.number1
                secondPairFirstHand = self.number2

                firstPairSecondHand = other.number1
                secondPairSecondHand = other.number2

                if firstPairFirstHand > firstPairSecondHand:
                    return Result.WIN
                elif firstPairFirstHand < firstPairSecondHand:
                    return Result.LOSS
                else:
                    if secondPairFirstHand > secondPairSecondHand:
                        return Result.WIN
                    elif secondPairFirstHand < secondPairSecondHand:
                        return Result.LOSS
                    else:
                        firstHandValues.remove(firstPairFirstHand)
                        firstHandValues.remove(secondPairFirstHand)

                        secondHandValues.remove(firstPairSecondHand)
                        secondHandValues.remove(secondPairSecondHand)

                        if firstHandValues[0] > secondHandValues[0]:
                            return Result.WIN
                        else:
                            return Result.LOSS
            elif self.handScore == 1:
                if self.number1 > other.number1:
                    return Result.WIN
                elif self.number1 < other.number1:
                    return Result.LOSS
                else:
                    for i in range(0, 2):
                        firstHandValues.remove(self.number1)
                        secondHandValues.remove(other.number1)

                    
                    for i in range(0, 3):
                        if max(firstHandValues) > max(secondHandValues):
                            return Result.WIN
                        elif max(firstHandValues) < max(secondHandValues):
                            return Result.LOSS
                        else:
                            firstHandValues.remove(max(firstHandValues))
                            secondHandValues.remove(max(secondHandValues))
            else:
                return self.commonTie(firstHandValues, secondHandValues)


