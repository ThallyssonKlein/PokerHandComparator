from card import Card
from custom_enum import Result


class PokerHand():
    cards = []
    handTypeNumber = 0
    definedHand = False

    def getCards(self):
        return self.cards

    def isRoyalFlush(self, hand):
        cards = hand.getCards()
        suit = cards[0].cardSuit
        for card in cards:
            if not card.cardValue in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                return False
            if card.cardSuit != suit:
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
                    return True, cards[i].cardValue
        return False, None
    
    def isFourOfAKind(self, hand):
        cards = hand.getCards()
        return self.ofAKind(cards, 4)
    
    def isFullHouse(self, hand):
        cards = hand.getCards()
        hasThree = False
        threeValue = None
        for i in range(0, len(cards)):
            if not hasThree:
                iCount = 1
                for j in range(i + 1, len(cards)):
                    if cards[i].cardValue == cards[j].cardValue:
                        iCount += 1
                    if iCount == 3:
                        hasThree = True
                        threeValue = cards[i].cardValue
                        iCount = 0
            else:
                iCount = 1
                for j in range(i + 1, len(cards)):
                    if cards[i].cardValue == cards[j].cardValue:
                        iCount += 1
                    if iCount == 2:
                        return True, threeValue
        return False, None

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
            if currentValue < i:
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
        for i in range(0, len(cards)):
            for j in range(1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    firstPairValue = cards[i].cardValue

        for i in range(0, len(cards)):
            for j in range(1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue and cards[j].cardValue != firstPairValue:
                    return True, cards[i].cardValue, firstPairValue
        return False

    def isOnePair(self, hand):
        cards = hand.getCards()
        firstPairValue = None
        for i in range(0, len(cards)):
            for j in range(1, len(cards)):
                if cards[i].cardValue == cards[j].cardValue:
                    return True, cards[j].cardValue
        return False

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
        fourOfAKindResult, secondResult1 = self.isFourOfAKind(hand)
        threeOfAKindResult, secondResult2 = self.isThreeOfAKind(hand)
        fullHouseResult, secondResult3 = self.isFullHouse(hand)
        isTwoPair, secondResult4, thirdResult = self.isTwoPair(hand)
        isOnPair, secondResult5 = self.isOnePair(hand)

        if self.isRoyalFlush(hand):
            hand.handTypeNumber = 10
            return True
        elif self.isStraightFlush(hand):
            hand.handTypeNumber = 9
            return True
        elif fourOfAKindResult:
            hand.handTypeNumber = 8
            return True, secondResult1
        elif fullHouseResult:
            hand.handTypeNumber = 7
            return True, secondResult2
        elif self.isFlush(hand):
            hand.handTypeNumber = 6
            return True
        elif self.isStraight(hand):
            hand.handTypeNumber = 5
            return True
        elif threeOfAKindResult:
            hand.handTypeNumber = 4
            return True, secondResult3
        elif isTwoPair:
            hand.handTypeNumber = 3
            return True, secondResult4, thirdResult
        elif isOnePair:
            hand.handTypeNumber = 2
            return True, secondResult5

        return False

    def __init__(self, cardsStr):
        cards = cardsStr.split(' ')

        if len(cards) != 5:
            raise Exception('Invalid number of cards')

        tmpArray = []
        for card in cards:
            tmpArray.append(Card(value=card))
        self.cards = tmpArray


    def commonTie(self, secondResultFirstHand, secondResultSecondHand):
        if max(firstHandValues) > max(secondHandValues):
            return Result.WIN
        else:
            return Result.LOSS
            
    def highCard(self, valuesHandOne, valuesHandTwo):
        if max(valuesHandOne) > max(valuesHandTwo):
            return Result.WIN
        else:
            return Result.LOSS
    
    def compare_with(self, other):
        self.definedHand, secondResultFirstHand, thirdResultFirstHand = self.defineHand(self)
        definedHand, secondResultSecondHand, thirdResultSecondHand = self.defineHand(other)

        if not self.definedHand and not definedHand:
            if self.winOrLoseHighestCard(self, other):
                return Result.WIN
            else:
                return Result.LOSS
        elif not self.definedHand and definedHand:
            return Result.LOSS
        elif self.definedHand and not definedHand:
            return Result.WIN
        else:
            if self.handTypeNumber > other.handTypeNumber:
                return Result.WIN
            elif self.handTypeNumber < other.handTypeNumber:
                return Result.LOSS
            elif self.handTypeNumber == other.handTypeNumber:
                firstHandValues = []
                secondHandValues = []

                for card in self.getCards():
                    firstHandValues.append(card.cardValue)
                for card in other.getCards():
                    firstHandValues.append(card.cardValue)
                
                if self.handTypeNumber == 2:
                    if secondResultFirstHand > secondResultSecondHand:
                        return Result.WIN
                    elif secondResultFirstHand == secondResultSecondHand:
                        firstHandValuesWithoutPair = firstHandValues
                        firstHandValuesWithoutPair.remove(secondResultFirstHand)

                        secondHandValuesWithoutPair = secondHandValues
                        secondHandValuesWithoutPair.remove(secondResultSecondHand)

                        if max(firstHandValuesWithoutPair) > max(secondHandValuesWithoutPair):
                            return Result.WIN
                        elif max(firstHandValuesWithoutPair) == max(secondHandValuesWithoutPair):
                            firstHandValuesWithoutPair.remove(max(firstHandValuesWithoutPair))
                            secondHandValuesWithoutPair.remove(max(secondHandValuesWithoutPair))

                            if max(firstHandValuesWithoutPair) > max(secondHandValuesWithoutPair):
                                return Result.WIN
                            elif max(firstHandValuesWithoutPair) == max(secondHandValuesWithoutPair):
                                firstHandValuesWithoutPair.remove(max(firstHandValuesWithoutPair))
                                secondHandValuesWithoutPair.remove(max(secondHandValuesWithoutPair))
                            
                                if max(firstHandValuesWithoutPair) > max(secondHandValuesWithoutPair):
                                    return Result.WIN
                                else:
                                    return Result.LOSS
                            else:
                                return Result.LOSS
                        else:
                            return Result.LOSS
                    else:
                        return Result.LOSS
                elif self.handTypeNumber == 3:
                    print('Entrou no 3')
                    firstPairFirstHand = secondResultFirstHand
                    secondPairFirstHand = thirdResultFirstHand
                    print(firstPairFirstHand)
                    print(secondPairFirstHand)

                    firstPairSecondHand = secondResultSecondHand
                    secondPairSecondHand = thirdResultSecondHand
                    print(firstPairSecondHand)
                    print(secondPairSecondHand)
                    
                    if max(firstPairFirstHand, secondPairFirstHand) > max(firstPairSecondHand, secondPairSecondHand):
                        return Result.WIN
                    elif max(firstPairFirstHand, secondPairFirstHand) == max(firstPairSecondHand, secondPairSecondHand):
                        print('Entrou no elif')
                        if min(firstPairFirstHand, secondPairFirstHand) > min(firstPairSecondHand, secondPairSecondHand):
                            return Result.WIN
                        else:
                            print('Entrou no primeiro else')
                            fifthFirstHand = None
                            fifthSecondHand = None

                            for value in firstHandValues:
                                if value != firstPairFirstHand and value != secondPairFirstHand:
                                    fifthFirstHand = value
                            
                            for value in secondHandValues:
                                if value != firstPairSecondHand and value != secondPairSecondHand:
                                    fifthSecondHand = value
                            
                            if fifthFirstHand > fifthSecondHand:
                                return Result.WIN
                            else:
                                print('Entrou no segundo else')
                                return Result.LOSS
                    else:
                        print('Entrou no terceiro else')
                        return Result.LOSS
                elif self.handTypeNumber == 4:
                    return commonTie(secondResultFirstHand, secondResultSecondHand)
                elif self.handTypeNumber == 5:
                    return highCard(valuesHandOne, valuesHandTwo)
                elif self.handTypeNumber == 6:
                    return highCard(valuesHandOne, valuesHandTwo)
                elif self.handTypeNumber == 7:
                    return commonTie(secondResultFirstHand, secondResultSecondHand)
                elif self.handTypeNumber == 8:
                    return commonTie(secondResultFirstHand, secondResultSecondHand)
                elif self.handTypeNumber == 9:
                    return highCard(valuesHandOne, valuesHandTwo)
                elif self.handTypeNumber == 10:
                    return Result.WIN
