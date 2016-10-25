import cards
import AI

numhumans=int(input("Enter number of human players: "))
numais=int(input("Enter number of AI players: "))
numplayers=numhumans+numais
cardsinitial=5
hums=[]
aiplayers=[]
play=True
huminplay=[] #array of booleans re: whether player is in play or skipped
aiinplay=[]

rankrules={'5': "highfive", 'K':"bow", 'Q': "bow"} #dict of rules based on rank and suit
suitrules={'H': "ily"}

def deal(numhum, numai, cardsphand): #The parameters are number human players, number of ai players
    global hums, aiplayers, huminplay, aiinplay
    global deck
    deck=cards.Deck()
    deck.shuffle()   #make a new deck and shuffle it
    for i in range(numhum):
        hums=hums+[cards.Hand()]
        huminplay=huminplay+[(True,0)]
    for i in range(numai):
        aiplayers=aiplayers+[AI.AIplay(cards.Hand())]
        aiinplay=aiinplay+[(True,0)]
    for hum in hums:
        for i in range(cardsphand):
            hum.add_card(deck.deal_card())
    for ai in aiplayers:
        for i in range(cardsphand):
            ai.hand.add_card(deck.deal_card())

def turn(player): #input whose turn it is
    global topcard, play, suitrules, rankrules  
    penalties=0
    validturn=True
    print(topcard)
    print(player)
    move=input("Which card will you play? ") #player inputs index of card to play and a list of string commands
    if(move=="gg ez"):        #im allowed to have fun in my code
        print("wow")
        play=False #end the game without errors
        return
    move=move.split()
    card=int(move[0])
    del move[0]
    if(card>=len(player.cards)): #if the index is larger than the number of cards, it is not right
        validturn=False
        penalties+=1
        print("That isn't a card in your hand")

    else:
        s=player.cards[card].suit
        r=player.cards[card].rank
        if(topcard.suit!=s and topcard.rank!=r): #check if valid card played
            validturn=False
            penalties+=1
            print("That isn't a valid card")
        else: #check if special rules were followed
            penalties+=checkmoves(player.cards[card], move)
    if(validturn):
        topcard=player.cards[card]
        player.rem_card(player.cards[card])
    penalty(player,penalties)
    if(penalties==1):
        print("You have 1 penalty")
    else:
        print("You have {} penalties".format(penalties))
    print(player)

def checkmoves(card, moves): #Check if special rules were followed and return the number of penalties
    global suitrules, rankrules
    s=card.suit
    r=card.rank
    pen=0
    for i in list(rankrules.keys()):
        if(r==i):
            if(not(rankrules[i] in moves)):
                pen+=1
                print("A special rank action was missed")
            else:
                del moves[moves.index(rankrules[i])]
    for i in list (suitrules.keys()):
        if(s==i):
            if(not(suitrules[i] in moves)):
                pen+=1
                print("A special suit action was missed")
            else:
                del moves[moves.index(suitrules[i])]
    for i in moves:
            pen+=1
            print("Unnecessary action(s)")
    return pen

def checkturn(ai, moves): #Respond appropriately to the AI's actions
    global topcard, suitrules, rankrules
    top, actions = moves
    penalties=0
    if(top==topcard): #The AI returns the topcard if it has no valid moves, and otherwise plays a valid card
        penalties+=1 #It is penalized if it has no valid card
        print("There was no valid card")
    else:
        penalties+=checkmoves(top, actions)    
    topcard=top
    penalty(ai.hand, penalties)
    if(penalties==1):
        print("You have 1 penalty")
    else:
        print("You have {} penalties".format(penalties))

def skip(ishum, howlong): #controls who is skipped for how long
    global count, huminplay, aiinplay
    if(ishum):
        huminplay[count]=(False, howlong)
    else:
        aiinplay[count]=(False, howlong)



def penalty(who, oops): #input hand and number of penalties
    for i in range(oops):
        who.add_card(deck.deal_card())

def reversal(ishum, player): #input True if hum and false if AI, and the player whose turn it is to reverse order of play
    global hums, aiplayers, count
    hums=hums[::-1]
    aiplayers=aiplayers[::-1]
    huminplay=aiinplay[::-1]
    aiinplay=aiinplay[::-1]
    if(ishum):
        count=hums.index(player)
    else:
        count=aiplayers.index(player)



deal(numhumans, numais,cardsinitial) #start the game by dealing
topcard=deck.deal_card()    #draw a card from the deck
turnnum=0
while(play):
    turnnum+=1
    count=0
    while(count<len(hums)): #go through the human players and have them go
        if(huminplay[count][0]): #skip if not in play
            turn(hums[count])
            if(not play):
                break
        else:
            huminplay[count]=(False, huminplay[count][1]-1) #keep track of who has been skipped and for how long
            if(huminplay[count][1]==0):
                huminplay[count]=(True,0)
        count+=1
    count=0
    if(not play):
        break
    while(count<len(aiplayers)): 
        if(aiinplay[count][0]):
            checkturn(aiplayers[count], aiplayers[count].turn(topcard))
            print(aiplayers[count].hand)
        else:
            aiinplay[count]=(False, aiinplay[count][1]-1)
            if(aiinplay[count][1]==0):
                aiinplay[count]=(True,0)
        count+=1
