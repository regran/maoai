"""Play the card game Mao"""
import cards
import AI

play = True
try:
    numhumans = int(input("Enter number of human players: "))
    numais = int(input("Enter number of new AI players: "))
    numperf = int(input("Enter number of perfect AIs: "))
except ValueError:
    print("A number was expected.")
    play = False
    exit()
if numhumans < 0 or numais < 0 or numperf < 0 or (numhumans + numais + numperf < 2):
    print("That isn't a valid number of players.")
    play = False
    exit()

numplayers = numhumans+numais
cardsinitial = 5
hums = []
aiplayers = []
huminplay = [] #array of booleans re: whether player is in play or skipped
aiinplay = []
#dicts of rules based on rank and suit
rankrules = {'5': "highfive", 'K':"bow", 'Q': "bow", '7':'nice'}
suitrules = {'H': "ily", 'S':"rave", 'D':'sparkly'}
prevmovelab = []
prevmovefeat = []
spare_deck = None
deck = None

def deal(numhum, numai, cardsphand): #The parameters are number human players, number of ai players
    """Initiate a game, asking how many players there are and dealing cards"""
    global hums, aiplayers, huminplay, aiinplay
    global deck, spare_deck
    deck = cards.Deck()
    deck.shuffle()   #make a new deck and shuffle it
    spare_deck = cards.Deck()
    spare_deck.empty()
    for i in range(numhum):
        hums = hums+[cards.Hand()]
        huminplay = huminplay+[(True, 0)]
    for i in range(numai):
        aiplayers = aiplayers+[AI.AIplay(cards.Hand())]
        aiinplay = aiinplay+[(True, 0)]
    for i in range(numperf):
        aiplayers += [AI.AIperf(cards.Hand(), rankrules, suitrules)]
        aiinplay += [(True, 0)]
    for hum in hums:
        for i in range(cardsphand):
            if deck.isempty():
                deck.deck += cards.Deck().deck
            hum.add_card(deck.deal_card())
    for ai in aiplayers:
        for i in range(cardsphand):
            if deck.isempty():
                deck.deck += cards.Deck().deck
            ai.hand.add_card(deck.deal_card())

def turn(player): #input whose turn it is
    """Get input from player about move and process the player's decision based on game rules"""
    global topcard, play
    penalties = 0
    validturn = True
    print(topcard)
    digit = False
    print(player)
    while not digit:
        move = input("Which card will you play? ")
        #player inputs index of card to play and a list of string commands
        if move == "gg ez":        #im allowed to have fun in my code
            print("wow")
            play = False #end the game without errors
            return
        move = move.split()
        if move == []:
            validturn = False
            print("No card was played")
            penalties += 1
            break
        if move[0].isdigit():
            card = int(move[0])
            del move[0]
            digit = True
        else:
            print("A positive integer was expected as your first word. Please try again.")
    else:
        if card >= len(player.cards): #check if index of card in hand
            validturn = False
            penalties += 1
            print("That isn't a card in your hand")
        else:
            s = player.cards[card].suit
            r = player.cards[card].rank
            if topcard.suit != s and topcard.rank != r: #check if valid card played
                validturn = False
                penalties += 1
                print("That isn't a valid card")
            else: #check if special rules were followed
                prevmovefeat.append([s, r]) #store data about card move features
                penalties += checkmoves(player.cards[card], move)
    if validturn:
        spare_deck.add_card(topcard)
        topcard = player.cards[card]
        player.rem_card(player.cards[card])
    penalty(player, penalties)
    if penalties == 1:
        print("You have 1 penalty")
    else:
        print("You have {} penalties".format(penalties))
    print(player)

def checkmoves(card, moves):
    """Check if special rules were followed and return the number of penalties"""
    global prevmovelab
    s = card.suit
    r = card.rank
    pen = 0
    prevmovelab += [moves[:]]
    for i in list(rankrules.keys()):
        if r == i:
            if not(rankrules[i] in moves):
                pen += 1
                print("A special rank action was missed")
            else:
                del moves[moves.index(rankrules[i])]
    for i in list(suitrules.keys()):
        if s == i:
            if not(suitrules[i] in moves):
                pen += 1
                print("A special suit action was missed")
            else:
                del moves[moves.index(suitrules[i])]
    for i in moves:
        pen += 1
        print("Unnecessary action(s)")
#   prevmovelab[-1].append(str(pen))#store data about how many penalties this move
    if pen > 0:
        del prevmovelab[-1]
        del prevmovefeat[-1]
    return pen

def checkturn(ai, moves):
    """Respond appropriately to the AI's actions based on game's rules"""
    global topcard
    top, actions = moves
    penalties = 0
    if top == topcard: #The AI returned the topcard if it has no valid moves
        penalties += 1 #It is penalized if it has no valid card
        print("There was no valid card")
    else: #play a valid card
        prevmovefeat.append([top.suit, top.rank]) #store data about card features
        penalties += checkmoves(top, actions)
        spare_deck.add_card(topcard)
    topcard = top
    penalty(ai.hand, penalties)
    if penalties == 1:
        print("You have 1 penalty")
    else:
        print("You have {} penalties".format(penalties))

def skip(ishum, howlong):
    """control who is skipped for how long"""
    if ishum:
        huminplay[count] = (False, howlong)
    else:
        aiinplay[count] = (False, howlong)

def penalty(who, oops): #input hand and number of penalties
    """Add a card to a player's hand for each penalty"""
    global deck, spare_deck
    for i in range(oops):
        if deck.isempty(): #check if the deck is empty
            deck = spare_deck #either use previously played cards or, if none, add a new deck
            deck.shuffle()
            spare_deck = cards.Deck()
            spare_deck.empty()
            if deck.isempty():
                deck = cards.Deck()
        who.add_card(deck.deal_card())

def reversal(ishum, player): #input True if hum and false if AI, and the player whose turn it is
    """Reverse the order of play at current player"""
    global hums, aiplayers, count, aiinplay, huminplay
    hums = hums[::-1]   #reverse lists
    aiplayers = aiplayers[::-1]
    huminplay = huminplay[::-1]
    aiinplay = aiinplay[::-1]
    if ishum:
        count = hums.index(player)
    else:
        count = aiplayers.index(player)

deal(numhumans, numais, cardsinitial) #start the game by dealing
topcard = deck.deal_card()    #draw a card from the deck
turnnum = 0 #count the number of turns
while play:
    turnnum += 1
    count = 0
    while count < len(hums): #go through the human players and have them go
        if huminplay[count][0]: #skip if not in play
            print("Human Player {}".format(count+1))
            turn(hums[count])
            print()
            if hums[count].isempty():
                print("We have a winner!")
                play = False
            if not play:
                break
        else:
            #keep track of who has been skipped and for how long
            huminplay[count] = (False, huminplay[count][1]-1)
            if huminplay[count][1] == 0:
                huminplay[count] = (True, 0)
        count += 1
    count = 0
    if not play:
        break
    while count < len(aiplayers):
        if aiinplay[count][0]:
            print("AI Player {}".format(count+1))
            checkturn(aiplayers[count], aiplayers[count].turn(topcard, prevmovefeat, prevmovelab))
            print(aiplayers[count].hand)
            print()
            if aiplayers[count].hand.isempty():
                print("GG EZ")
                play = False
                break
        else:
            aiinplay[count] = (False, aiinplay[count][1]-1)
            if aiinplay[count][1] == 0:
                aiinplay[count] = (True, 0)
        count += 1
for i in range(numais):
    aiplayers[i].drawtree()
