from enum import Enum

class Suit(Enum):
    CLUBS, DIAMONDS, HEARTS, SPADES = 'clubs', 'diamonds', 'hearts', 'spades'

class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def getSuit(self):
        return self.suit
    
    def getValue(self):
        return self.value
    
    def printCard(self):
        print(self.getSuit(), self.getValue())

class Hand():
    def __init__(self):
        self.score = 0
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)
        if card.getValue() == 1:
            self.score += 11 if self.score <= 21 else 1
        else :
            self.score += card.getValue()
        print('Score:', self.score)
    
    def getScore(self):
        return self.score
    
    def getCards(self):
        return self.cards
    
    def print(self):
        for card in self.getCards():
            print(card.getSuit(), card.getValue())