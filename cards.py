import random
#global variables for cards
SUITS = ('C', 'S', 'H', 'D')
card_dict= {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
RANKS=card_dict.keys()

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

    def __str__(self):
        return self.rank+':'+self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object
    def __str__(self):
        ans = " "
        for i in self.cards:
            ans +=str(i)+", "
        return "Hand contains: " + ans # return a string representation of a hand
             
    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def rem_card(self, card):
        self.cards.remove(card)
    
    def isempty(self):
        return self.cards==[]

   
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)
    def shuffle(self):
        # add cards back to deck and shuffle
        random.shuffle(self.deck)	# use random.shuffle() to shuffle the deck

    def deal_card(self):
        return self.deck.pop()
        # deal a card object from the deck
    
    def __str__(self):
        ans = " "
        for card in self.deck:
            ans += str(card)
        return "Deck contains" + ans	# return a string representing the deck

    def isempty(self):
        return self.deck==[]


