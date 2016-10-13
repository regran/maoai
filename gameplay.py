import cards
import AI

numhumans=int(input("Enter number of human players: "))
numais=int(input("Enter number of AI players: "))
numplayers=numhumans+numais
cardsinitial=5
hums=[]
aiplayers=[]
play=True


def deal(numhum, numai, cardsphand): #The parameters are number human players, number of ai players
    global hums, aiplayers
    global deck
    deck=cards.Deck()
    deck.shuffle()   #make a new deck and shuffle it
    for i in range(numhum):
        hums=hums+[cards.Hand()]
    for i in range(numai):
        aiplayers=aiplayers+[AI.AIplay(cards.Hand())]
    for hum in hums:
        for i in range(cardsphand):
            hum.add_card(deck.deal_card())
    for ai in aiplayers:
        for i in range(cardsphand):
            ai.hand.add_card(deck.deal_card())

def turn(player): #input whose turn it is
    global topcard    
    validturn=True
    print(topcard)
    print(player)
    move=int(input("Which card will you play? "))
    if(move<len(player.cards) and (topcard.suit==player.cards[move].suit or topcard.rank==player.cards[move].rank)):
        validturn=True
    else:
        validturn=False
    if(validturn):
        topcard=player.cards[move]
        player.rem_card(player.cards[move])
    else:
        penalty(player,1)
    print(player)

def penalty(who, oops): #input hand and number of penalties
    for i in range(oops):
        who.add_card(deck.deal_card())

def reversal(ishum, player): #input True if hum and false if AI, and the player whose turn it is
    global hums, aiplayers,count,hums, aiplayers
    hums=hums[::-1]
    aiplayers=aiplayers[::-1]
    if(ishum):
        count=hums.index(player)
    else:
        count=aiplayers.index(player)
deal(numhumans, numais,cardsinitial)
topcard=deck.deal_card()
while(play):
    count=0
    while(count<len(hums)):
        turn(hums[count])
        count+=1
    count=0
    while(count<len(aiplayers)):
        played=aiplayers[count].turn(topcard)
        if(played==topcard):
            penalty(aiplayers[count].hand, 1)
        topcard=played
        print(aiplayers[count].hand)
        count+=1
