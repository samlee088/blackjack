from enum import Enum
import random
from abc import ABC, abstractmethod


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


print, draw, shuffle

class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in Suit:
            for value in range(1, 14):
                self.cards.append(Card(suit, min(value, 10)))

    def print(self):
        for card in self.cards:
            card.print()
    
    def draw(self):
        return self.cards.pop()
    
    def shuffle(self):
        for i in range(len(self.cards)):
            j = random.randint(0, 51)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]


class Player:
    def __init__(self, hand):
        self.hand = hand

    def getHand(self):
        return self.hand
    
    def clearHand(self):
        self.hand = Hand()

    def addCard(self, card):
        self.hand.addCard(card)

    @abstractmethod
    def makeMove(self):
        pass


class UserPlayer(Player):
    def __init__(self, balance, hand):
        super().__init__(hand)
        self.balance = balance

    def getBalance(self):
        return self.balance
    
    def placeBet(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient Funds")
        self.balance -= amount
        return amount
    
    def receiveWinnings(self, amount):
        self.balance += amount

    def makeMove(self):
        if self.getHand().getScore()>21:
            return False
        move = input("Draw card? [y/n]")
        return move == 'y'
    
class Dealer(Player):
    def __init__(self, hand):
        super().__init__(hand)
        self.targetScore = 17

    def updateTargetScore(self, score):
        self.targetScore = score
    
    def makeMove(self):
        return self.getHand().getScore() < self.targetScore

class GameRound:
    def __init__(self, player, dealer, deck):
        self.player = player
        self.dealer = dealer
        self.deck = deck
    
    def getBetUser(self):
        amount = int(input("Enter a bet amount: "))
        return amount
    
    def dealInitialCards(self):
        for i in range(2):
            self.player.addCard(self.deck.draw())
            self.player.addCard(self.deck.draw())
        print('Player hand: ')
        self._player.getHand().print()
        dealerCard = self._dealer.getHand().getCards()[0]
        print("Dealer's first card: ")
        dealerCard.print()
    
    def cleanupRound(self):
        self.player.clearHand()
        self.dealer.clearHand()
        print("Player balance: ", self.player.getBalance())

    def play(self):
        self.deck.shuffle()

        if self.player.getBalance() <= 0:
            print('Player has no more money =)')
            return
        userBet = self.getBetUser()
        self.player.placeBet(userBet)

        self.dealInitialCards()

        # User makes moves
        while self.player.makeMove():
            drawnCard = self.deck.draw()
            print('Player draws', drawnCard.getSuit(), drawnCard.getValue())
            self.player.addCard(drawnCard)
            print('Player score: ', self.player.getHand().getScore())

        if self.player.getHand().getScore() > 21:
            print("Player busts!")
            self.cleanupRound()
            return
        
        # Dealer makes moves
        while self.dealer.makeMove():
            self.dealer.addCard(self.deck.draw())

        # Determine winner
        if self.dealer.getHand().getScore() > 21 or self.player.getHand().getScore() > self.dealer.getHand().getScore():
            print('Player Wins!')
            self.player.receiveWinnings(userBet * 2)
        elif self.dealer.getHand().getScore() > self.player.getHand().getScore():
            print('Player loses')
        else:
            print("Game ends in a draw")
            self.player.receiveWinnings(userBet)
        self.cleanupRound()

player = UserPlayer(10000, Hand())
dealer = Dealer(Hand())
while player.getBalance > 0:
    gameRound = GameRound(player, dealer, Deck()).play()