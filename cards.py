"""contains classes for cards, a hand of cards, and a deck of cards for a card game"""
import random, pygame
import copy
pygame.init()
#global variables for cards
SUITS = ('Diamonds', 'Hearts', 'Clubs', 'Spades')
VALUES = {'Ace':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
          '10':10, 'Jack':10, 'Queen':10, 'King':10}
RANKS = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')

CARD = CARDW, CARDH = 225, 315
smallCARD = smallCARDW, smallCARDH = 112, 157
medCARD = medCARDW, medCARDH = 150, 210
HANDW = 1800
size = width, height = [1920, 1080]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mao Card Game")
smallcards = pygame.image.load("cardimages_small.png").convert()
medcards = pygame.image.load("cardimages_med.png").convert()
cards = pygame.image.load("cardimages.png").convert() #load image of cards
cardback = pygame.image.load("cardback_small.png").convert()
d = pygame.image.load("cardback_med.png").convert()
bg = 14, 144, 14 #background color

class Card(pygame.sprite.Sprite):
    """Store a suit and rank for a traditional playing card"""
    def __init__(self, suit=None, rank=None, pos=(0,0), med=False):
        pygame.sprite.Sprite.__init__(self)
        self.cardback = cardback
        if (suit in SUITS) and (rank in RANKS): #make sure suit and rank are valid
            self.suit = suit
            self.rank = rank
            self.card = pygame.Surface(CARD) #get a specific card from sheet of cards
            self.cardmed = pygame.Surface(medCARD)
            self.cardsmall = pygame.Surface(smallCARD)
            self.card.blit(cards, (0, 0), (RANKS.index(self.rank)*CARDW, SUITS.index(self.suit)*CARDH, CARDW, CARDH))
            self.cardmed.blit(medcards, (0, 0), (RANKS.index(self.rank)*medCARDW, SUITS.index(self.suit)*medCARDH, medCARDW, medCARDH))
            self.cardsmall.blit(smallcards, (0, 0), (RANKS.index(self.rank)*smallCARDW, SUITS.index(self.suit)*smallCARDH, smallCARDW, smallCARDH))
           #self.cardimage = pygame.transform.scale(card, (75, 105))
            self.cardimage = self.card
            if med:
                self.cardimage = self.cardmed
            self.image = self.cardimage
            self.rect = self.image.get_rect(x=pos[0], y=pos[1]) #get rekt
            self.back = False
            self.clicked = False

        else:
            self.image = self.cardimage = self.cardback
            self.back = True
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)
        self.rect = self.image.get_rect()
        self.isback = False

    def toBig(self):
        self.cardimage = self.card
        self.image = self.cardimage
        self.rect = self.image.get_rect(x=self.rect.x, y=self.rect.y)
        return self

    def toMed(self):
        self.cardimage = self.cardmed
        self.image = self.cardimage
        self.rect = self.image.get_rect(x=self.rect.x, y=self.rect.y)
        return self

    def toSmall(self):
        self.cardimage = self.cardsmall
        self.image = self.cardimage
        self.rect = self.image.get_rect(x=self.rect.x, y=self.rect.y)
        return self

    def is_clicked(self, up=True, checkpos=True):
        hovrect = copy.deepcopy(self.rect)
        hovrect.y = hovrect.y-15
        updates = []
        eraser = pygame.Surface((self.rect.width+8, self.rect.height+5))
        eraser.fill(bg)
        click = pygame.mouse.get_pressed()[0]
        if checkpos: pos=self.rect.collidepoint(pygame.mouse.get_pos())
        else: pos = False
        newclick = pos and self.clicked and not click
        if pos and not up: #button pressed down
            pygame.draw.rect(screen, (227, 193, 13), hovrect, 3)
            updates += [hovrect]
            pygame.display.update(updates)
            updates = []
            self.clicked = True

        elif pos and not click: #mouseover
            updates += [screen.blit(eraser, (self.rect.x-4, self.rect.y-3))]
            updates += [screen.blit(self.image, hovrect)]
            pygame.display.update(updates)
            updates = []
            self.clicked = False
            
        elif not (click or pos): #mouse released and not hovering
            self.clicked = False
            updates += [screen.blit(eraser, (hovrect.x-4, hovrect.y-3))]
            updates += [screen.blit(self.image, self.rect)]
            pygame.display.update(updates)
            updates = []
            
        return newclick  #mouse released on pressed button



    def flip(self):
        if not self.isback:
            self.image = cardback
            self.isback = True
        else:
            self.image = self.cardimage
            self.isback = False
        self.rect = self.image.get_rect()

    def __str__(self):
        return self.rank+' of '+self.suit

    def get_suit(self): #return suit of card
        return self.suit

    def get_rank(self): #return rank of card
        return self.rank

class Hand():
    """A hand of cards held by a player"""
    def __init__(self, pos=(0,0)): #create empty hand
        self.hands = [[]]
        self.index = 0
        self.numcard = 0
        self.image = [pygame.Surface((HANDW, CARDH))]
        self.image[0].fill((14, 144, 14))
        self.rect = self.image[0].get_rect(x=pos[0], y=pos[1])
        self.posempty = [(0, 0)]

    def __str__(self):
        ans = " "
        for i in self.hands:
            for j in i:
                ans += str(j)+", "
        return "Hand contains: " + ans # return a string representation of a hand

    def add_card(self, card, AI=False):
        """Add a card to the hand"""
        for hand in range(len(self.hands)): #find a hand with an empty spot
            if len(self.hands[hand]) < 6:
                self.hands[hand].append(card) #add a card object to the hand
                self.image[hand].blit(card.image, self.posempty[hand])
                card.rect.x = self.rect.x + self.posempty[hand][0]
                card.rect.y = self.rect.y + self.posempty[hand][1]
                if not AI:
                    self.posempty[hand] = (self.posempty[hand][0]+CARDW*6/5, 0)
                break
        else:
            self.hands.append([card])
            card.rect.x = self.rect.x
            card.rect.y = self.rect.y
            if not AI:
                self.posempty += [(CARDW*6/5, 0)]
            else:
                self.posempty += [(0,0)]
            new = pygame.Surface((HANDW, CARDH))
            new.fill((14, 144, 14))
            new.blit(card.image, (0,0))
            self.image += [new]
        self.numcard += 1
        print(self)
        print(self.hands)

    def rem_card(self, card, AI=False):
        """Remove a card from the hand"""
        i = self.hands[self.index].index(card)
        self.image[self.index].blit(self.image[self.index], (i*CARDW*6/5, 0), 
                       ((i+1)*CARDW*6/5, 0, HANDW - (i+1)*CARDW*6/5, CARDH))
        for l in self.hands[self.index][i:]:
            l.rect.x = l.rect.x-CARDW*6/5
        self.hands[self.index].remove(card)
        print(self)
        self.numcard += -1
        if self.hands[self.index] == []:
            self.hands.remove(self.hands[self.index])
            self.image.remove(self.image[self.index])
            self.posempty.remove(self.posempty[self.index])
        elif not AI:
            self.posempty[self.index] = (self.posempty[self.index][0]-CARDW*6/5, 0)

    def isempty(self):
        """Check if the hand is empty"""
        return self.numcard == 0

class Deck(Card):
    """A traditional deck of playing cards (without jokers)"""
    def __init__(self, pos=(0,0)):
        self.deck = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)
        self.image = d
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.clicked = False

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


