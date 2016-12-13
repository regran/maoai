"""contains classes for cards, a hand of cards, and a deck of cards for a card game"""
import random, pygame
pygame.init()
#global variables for cards
SUITS = ('C', 'S', 'H', 'D')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
          'T':10, 'J':10, 'Q':10, 'K':10}
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')

CARDH = 98
CARDW = 73
HANDW = 1800
size = width, height = 1890, 1080
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mao Card Game")
cards = pygame.image.load("card_images.png").convert() #load image of cards
cardback = pygame.image.load("card_back.png").convert()


class Card(pygame.sprite.Sprite):
    """Store a suit and rank for a traditional playing card"""
    def __init__(self, suit, rank, pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.cardback = pygame.image.load("card_back.png").convert()
        if (suit in SUITS) and (rank in RANKS): #make sure suit and rank are valid
            self.suit = suit
            self.rank = rank
            card = pygame.Surface((CARDW, CARDH)) #get a specific card from sheet of cards
            card.blit(cards, (0, 0), (RANKS.index(self.rank)*CARDW, SUITS.index(self.suit)*CARDH, CARDW, CARDH))
            self.cardimage = card
            self.image = self.cardimage
            self.rect = self.image.get_rect(x=pos[0], y=pos[1]) #get rekt
            self.back = False

        else:
            self.image = self.cardimage = self.cardback
            self.back = True
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)
        self.rect = self.image.get_rect()
        self.isback = False

    def flip(self):
        if not self.isback:
            self.image = cardback
            self.isback = True
        else:
            self.image = self.cardimage
            self.isback = False
        self.rect = self.image.get_rect()

    def __str__(self):
        return self.rank+':'+self.suit

    def get_suit(self): #return suit of card
        return self.suit

    def get_rank(self): #return rank of card
        return self.rank

class Hand(pygame.sprite.Sprite):
    """A hand of cards held by a player"""
    def __init__(self, pos=(0,0)): #create empty hand
        self.cards = []
        self.numcard = 0
        self.image = pygame.Surface((HANDW, CARDH))
        self.image.fill((14, 144, 14))
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.posempty = (0, 0)

    def __str__(self):
        ans = " "
        for i in self.cards:
            ans += str(i)+", "
        return "Hand contains: " + ans # return a string representation of a hand

    def add_card(self, card):
        """Add a card to the hand"""
        self.cards.append(card)	# add a card object to a hand
        self.numcard += 1
        self.image.blit(card.image, self.posempty)
        card.rect.x = self.rect.x + self.posempty[0]
        card.rect.y = self.rect.y + self.posempty[1]
        self.posempty = (self.posempty[0]+CARDW/3, 0)

    def rem_card(self, card):
        """Remove a card from the hand"""
        self.image.blit(self.image, ((self.cards.index(card))*CARDW/3, 0), 
                       ((self.cards.index(card)+1)*CARDW/3, 0, HANDW - (self.cards.index(card)+2)*CARDW/3, CARDH))
        if self.cards.index(card) == len(self.cards)-1:
            self.image.blit(self.cards[self.numcard-2].image, ((self.numcard-2)*CARDW/3, 0))
        self.cards.remove(card)
        self.numcard += -1
        self.posempty = (self.posempty[0]-CARDW/3, 0)

    def isempty(self):
        """Check if the hand is empty"""
        return self.cards == []

class Deck(pygame.sprite.Sprite):
    """A traditional deck of playing cards (without jokers)"""
    def __init__(self, pos=(0,0)):
        self.deck = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)
        self.image = cardback
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])

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


