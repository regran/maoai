"""contains classes for cards, a hand of cards, and a deck of cards for a card game"""
import random
#global variables for cards
SUITS = ('C', 'S', 'H', 'D')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
          'T':10, 'J':10, 'Q':10, 'K':10}
RANKS = VALUES.keys()

class Card:
    """Store a suit and rank for a traditional playing card"""
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS): #make sure suit and rank are valid
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.rank+':'+self.suit

    def get_suit(self): #return suit of card
        return self.suit

    def get_rank(self): #return rank of card
        return self.rank

class Hand:
    """A hand of cards held by a player"""
    def __init__(self): #create empty hand
        self.cards = []

    def __str__(self):
        ans = " "
        for i in self.cards:
            ans += str(i)+", "
        return "Hand contains: " + ans # return a string representation of a hand

    def add_card(self, card):
        """Add a card to the hand"""
        self.cards.append(card)	# add a card object to a hand

    def rem_card(self, card):
        """Remvoe a card from the hand"""
        self.cards.remove(card)

    def isempty(self):
        """Check if the hand is empty"""
        return self.cards == []

class Deck:
    """A traditional deck of playing cards (without jokers)"""
    def __init__(self):
        self.deck = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)

    def shuffle(self):
        """Shuffle the cards in the deck"""
        random.shuffle(self.deck)

    def deal_card(self):
        """Deal a card object from the deck"""
        return self.deck.pop()

    def __str__(self):
        ans = " "
        for card in self.deck:
            ans += str(card)
        return "Deck contains" + ans	# return a string representing the deck

    def empty(self):
        """Remove all cards from the deck"""
        self.deck = []

    def add_card(self, card):
        """Add a card to the deck"""
        self.deck.append(card)

    def isempty(self):
        """Check if the deck is empty"""
        return self.deck == []


