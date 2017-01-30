"""Play the card game Mao"""
import cards
import AI
import pygame
import math
import time
import pygame.freetype
import eztext, guielem
import threading
pygame.init()

red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0
black = 0, 0, 0
white = 0, 0, 0
bg = 14, 144, 14 #background color
play = True
updatedareas = []
pfont = pygame.font.SysFont('roboto', 50)
font = pygame.freetype.SysFont('roboto', 50)
smallfont = pygame.freetype.SysFont('roboto', 30)
clock = pygame.time.Clock()
jokefont = pygame.freetype.SysFont('comicsans', 100)

def quit():
    global play
    while play:
        clock.tick(30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            play = False
            pygame.quit()
            exit()

t=threading.Thread(target=quit)
t.setDaemon(True)
t.start()

def eprompt(p):
    global updatedareas
    eraser = pygame.Surface((p.rect.width, p.rect.height))
    eraser.blit(cards.screen, p.image.get_rect())
    draw = False
    while(not draw):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                draw = True
                play = False
                exit()
        draw = p.drawP(cards.screen,events)
        updatedareas += [p.rect]
        pygame.display.update(updatedareas)
        updatedareas = []
    updatedareas += [cards.screen.blit(eraser, p.rect)]
    pygame.display.update(updatedareas)
    updatedareas = []
   

def gettext(textlist, rect, numonly=False):
    global updatedareas
    if numonly:
        rest='01234567890'
    else: rest='\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~\''
    words = True
    lineheight = pfont.size(textlist[0])[1]
    lh = rect.y - (lineheight*(len(textlist))/2)
    eraser = pygame.Surface((rect.width, lineheight))
    eraser.fill(bg)
    inps=[]
    for text in textlist:
        txtbx = eztext.Input(x=rect.x, y=lh, maxlength=rect.width, color=black, restricted=rest,font=pfont, prompt=text)  
        val = None
        while val == None:
            clock.tick(30)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    play = False
                    return
            val = txtbx.update(events)
            cards.screen.blit(eraser, (txtbx.x, txtbx.y))
            txtbx.draw(cards.screen)
            updatedareas += [eraser.get_rect(x=txtbx.x, y=txtbx.y)]
            pygame.display.update(updatedareas)
            updatedareas = []
        inps += [val]    
        lh += lineheight 
    eraser = pygame.Surface((rect.width, lineheight*len(textlist)))
    eraser.fill(bg)
    updatedareas += [cards.screen.blit(eraser,(rect.x, lh-lineheight*len(textlist)))]
    pygame.display.update(updatedareas)
    updatedareas = []
    return inps

        

cards.screen.fill(bg)
pygame.display.update()
numhumans, numais, numperf = map(lambda x: int(x), gettext(["Enter number of human players: ", "Enter number of new AI players: ", "Enter number of perfect AIs: "], cards.screen.get_rect(x=cards.width/5, y=cards.height/2), True))


if numhumans + numais + numperf < 2:
    eprompt(guielem.ButtonPrompt("That isn't a valid number of players. Think about what a sad and lonely person you are. ", cards.width/2, cards.height/2, cards.width/3, cards.height/5, "Exit"))
    play = False
    exit()

#dicts of default rules based on rank and suit
rankrules = {'5': "highfive", 'King':"bow", 'Queen': "bow", '7':'nice'}
suitrules = {'Hearts': "ily", 'Spades':"rave", 'Diamonds':'sparkly'}

    

numplayers = numhumans+numais
cardsinitial = 5
hums = []
aiplayers = []
huminplay = [] #array of booleans re: whether player is in play or skipped
aiinplay = []
prevmovelab = []
prevmovefeat = []
spare_deck = None
deck = None
deckpos = (cards.width/2-cards.medCARDW/2-100, cards.height/2-cards.medCARDH/2)
handpos = (100, 900) 

lines = []
colors = []
prevrec = pygame.Rect(cards.width*7/10, 150+cards.smallCARDH, cards.width*3/10, handpos[1]-50-150-cards.smallCARDH)
def previously(newtext, color=black):
    global lines, updatedareas, colors
    back = pygame.Surface((prevrec.width, prevrec.height+20))
    back.fill((170, 90, 0))
    newl = guielem.wrapline(smallfont, newtext, prevrec)
    for n in newl:
        colors += [color]
    lines += newl
    lineheight = smallfont.get_sized_glyph_height()
    lh = 0
    eraser = pygame.Surface((prevrec.width, prevrec.height))
    eraser.fill(bg)
    updatedareas += [cards.screen.blit(back, (prevrec.x, prevrec.y-20))]
    while len(lines)*lineheight>prevrec.height:
        lines = lines[1:]
        colors = colors[1:]
    for l in range(len(lines)):
        smallfont.render_to(cards.screen, (prevrec.x, prevrec.y + lh), lines[l], fgcolor=colors[l])
        lh += lineheight
    pygame.display.update(updatedareas)
    updatedareas = []


def deal(numhum, numai, cardsphand): #The parameters are number human players, number of ai players
    """Initiate a game, asking how many players there are and dealing cards"""
    global hums, aiplayers, huminplay, aiinplay
    global deck, spare_deck
    deck = cards.Deck(pos=deckpos)
    deck.shuffle()   #make a new deck and shuffle it
    spare_deck = cards.Deck(pos=deckpos)
    spare_deck.empty()
    for i in range(numhum):
        hums = hums+[cards.Hand(pos=handpos)]
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
            ai.hand.add_card(deck.deal_card(), True)

def playerstatus(player=None):
    """Display number of cards held by other players at top"""
    global updatedareas
    i = 0
    for ai in aiplayers:
        ai.hand.rect.x = handpos[0] + i*(cards.smallCARDW+50)
        ai.hand.rect.y = 100
        updatedareas += [cards.screen.blit(cards.cardback, ai.hand.rect)]
        rec = font.get_rect(str(ai.hand.numcard)) 
        if rec.width > cards.smallCARDW:
            rec=smallfont.get_rect(str(ai.hand.numcard))
            smallfont.render_to(cards.screen, (handpos[0]+cards.smallCARDW/2-rec.width/2+i*(cards.smallCARDW+50), 100+cards.smallCARDH/2-rec.height/2), None, fgcolor=black)
        else: font.render_to(cards.screen, (handpos[0]+cards.smallCARDW/2-rec.width/2+i*(cards.smallCARDW+50), 100+cards.smallCARDH/2-rec.height/2), None, fgcolor=black)
        i += 1
    for hum in hums:
        if hum == player:
            continue
        updatedareas += [cards.screen.blit(cards.cardback, (handpos[0]+i*(cards.smallCARDW+50), 100))]
        rec = font.get_rect(str(hum.numcard))
        if rec.width>cards.smallCARDW:
            rec=smallfont.get_rect(str(hum.numcard))
            smallfont.render_to(cards.screen, (handpos[0]+cards.smallCARDW/2-rec.width/2+i*(cards.smallCARDW+50), 100+cards.smallCARDH/2-rec.height/2), None, fgcolor=black)
        else: font.render_to(cards.screen, (handpos[0]+cards.smallCARDW/2-rec.width/2+i*(cards.smallCARDW+50), 100+cards.smallCARDH/2-rec.height/2), None, fgcolor=black)
        i += 1
    eraser = pygame.Surface((cards.width, cards.smallCARDH))
    eraser.fill(bg)
    updatedareas += [cards.screen.blit(eraser, (handpos[0]+i*(cards.smallCARDW+50), 100))]
    pygame.display.update(updatedareas)
    updatedareas = []
    

def cardselect(player):
    global updatedareas
    while True:
        events = pygame.event.get()
        for e in events:
            down = not e.type==pygame.MOUSEBUTTONDOWN
            #check arrows and break if one was clicked
            if DownArrow.is_clicked(down):
                if player.index < len(player.hands)-1: player.index += 1
                else: player.index = 0
                updatedareas += [cards.screen.blit(player.image[player.index], player.rect)]
                updatedareas += [font.render_to(cards.screen, (player.rect.x+cards.CARDW*6*6/5, player.rect.y+90), str(player.index+1) + "/" + str(len(player.hands)), fgcolor=(255,158,0))]
                
            elif UpArrow.is_clicked(down):
                if player.index>0: player.index += -1
                else: player.index = len(player.hands) -1
                updatedareas += [cards.screen.blit(player.image[player.index], player.rect)]
                updatedareas += [font.render_to(cards.screen, (player.rect.x+cards.CARDW*6*6/5, player.rect.y+90), str(player.index+1) + "/" + str(len(player.hands)), fgcolor=(255,158,0))]
            updatedareas += [DownArrow.drawA(cards.screen)]
            updatedareas += [UpArrow.drawA(cards.screen)]
            pygame.display.update(updatedareas)
            updatedareas = []
            for c in player.hands[player.index]:
                if c.is_clicked(down):
                    return c
            if deck.is_clicked(down):
                return deck

def turn(player): #input whose turn it is
    """Get input from player about move and process the player's decision based on game rules"""
    global topcard, play, updatedareas
    penalties = 0
    validturn = True
    updatedareas += [cards.screen.blit(topcard.image, (deckpos[0]+200, deckpos[1]))]
    digit = False
    player.index = 0
    updatedareas += [cards.screen.blit(player.image[player.index], player.rect)] #HANDYHAND
    updatedareas += [DownArrow.drawA(cards.screen)]
    updatedareas += [UpArrow.drawA(cards.screen)]
    updatedareas += [font.render_to(cards.screen, (player.rect.x+cards.CARDW*6*6/5, player.rect.y+90), str(player.index+1) + "/" + str(len(player.hands)), fgcolor=(255,158,0))]
    playerstatus(player)
    pygame.event.clear()
    card = cardselect(player)
    if card == deck or (topcard.suit != card.suit and topcard.rank != card.rank): #check if valid card played
        validturn = False
        deck.is_clicked(False, False)
        penalties += 1
        previously("Invalid card")
    else: #check if special rules were followed
        [move] = gettext(["Special actions: "], pygame.Rect(handpos[0], (deckpos[1]+handpos[1]+cards.CARDH)/2, cards.width-prevrec.width-handpos[0], deckpos[1]-handpos[1]))
        if move == "gg ez":        #im allowed to have fun in my code
            cards.screen.fill(bg)
            jokefont.render_to(cards.screen, (cards.width/2, cards.height/2), "wow", fgcolor=red)
            pygame.display.flip()
            play = False #end the game without errors
            time.sleep(5)
            exit()
        move = move.split()
        prevmovefeat.append([card.suit, card.rank]) #store data about card move features
        previously("Actions: {}".format(move))
        penalties += checkmoves(card, move)
    if validturn:
        spare_deck.add_card(topcard)
        topcard = card.toMed()
        player.rem_card(card)
        previously("Played {}".format(card))
    updatedareas += [cards.screen.blit(topcard.image, (deckpos[0]+200, deckpos[1]))]
    penalty(player, penalties)
    if penalties == 1:
        previously("1 penalty")
    else:
        previously("{} penalties".format(penalties))




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
            else:
                del moves[moves.index(rankrules[i])]
    for i in list(suitrules.keys()):
        if s == i:
            if not(suitrules[i] in moves):
                pen += 1
            else:
                del moves[moves.index(suitrules[i])]
    for i in moves:
        pen += 1
    if pen > 0:
        del prevmovelab[-1]
        del prevmovefeat[-1]
    return pen

def checkturn(ai, moves):
    """Respond appropriately to the AI's actions based on game's rules"""
    global topcard, updatedareas
    top, actions = moves
    penalties = 0
    if top == topcard: #The AI returned the topcard if it has no valid moves
        penalties += 1 #It is penalized if it has no valid card
        previously("Had no valid card")
    else: #play a valid card
        previously("Played {}".format(top))
        previously("Actions: {}".format(actions))
        prevmovefeat.append([top.suit, top.rank]) #store data about card features
        cut(ai.hand, top, -1)
        updatedareas += [cards.screen.blit(top.image, (deckpos[0]+200, deckpos[1]))]
        playerstatus()
        penalties += checkmoves(top, actions)
        spare_deck.add_card(topcard)
    topcard = top.toMed()
    penalty(ai.hand, penalties)
    if penalties == 1:
        previously("1 penalty")
    else:
        previously("{} penalties".format(penalties))

def skip(ishum, howlong):
    """control who is skipped for how long"""
    if ishum:
        huminplay[count] = (False, howlong)
    else:
        aiinplay[count] = (False, howlong)

def penalty(who, oops): #input hand and number of penalties
    """Add a card to a player's hand for each penalty"""
    global deck, spare_deck, updatedareas
    for i in range(oops):
        if deck.isempty(): #check if the deck is empty
            deck = spare_deck #either use previously played cards or, if none, add a new deck
            deck.shuffle()
            spare_deck = cards.Deck(pos=deckpos)
            spare_deck.empty()
            if deck.isempty():
                deck = cards.Deck(pos=deckpos)
        c = (deck.deal_card())
        c.toBig()
        if who.rect.y == 100: #check if AI
            c.flip()
        else:
            updatedareas += [cards.screen.blit(eraser, (handpos[0]-5, handpos[1]-18))]
            updatedareas += [cards.screen.blit(who.image[who.index], who.rect)]
            updatedareas += [font.render_to(cards.screen, (who.rect.x+cards.CARDW*6*6/5, who.rect.y+90), str(who.index+1) + "/" + str(len(who.hands)), fgcolor=(255,158,0))]
        cut(who, c)
        if who.rect.y == 100:
            c.flip() #so AI will play card flipped correctly
            who.add_card(c, True)
        else: 
            who.add_card(c)
            updatedareas += [cards.screen.blit(who.image[who.index], who.rect)]
            updatedareas += [font.render_to(cards.screen, (who.rect.x+cards.CARDW*6*6/5, who.rect.y+90), str(who.index+1) + "/" + str(len(who.hands)), fgcolor=(255,158,0))]
        playerstatus(who)

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
topcard = deck.deal_card().toMed()    #draw a card from the deck
turnnum = 0 #count the number of turns
updatedareas += [cards.screen.blit(deck.image, deck.rect)]
pygame.display.update(updatedareas)
updatedareas = []


def cut(player, card, mult=1):
    """Move card from deck to player's hand"""
    global updatedareas
    if mult == 1: #card being dealt
        cardrect = deck.rect.copy()
        goal = (player.rect.x+player.posempty[player.index][0], player.rect.y+player.posempty[player.index][1])
    else: #AI playing card
        goal = (deckpos[0]+200, deckpos[1])
        cardrect = player.rect.copy()
        card.toMed()
    pygame.display.update(updatedareas)
    updatedareas = []
    speed = [(goal[0]-cardrect.x), (goal[1]-cardrect.y)]
    speed = [speed[0]/math.sqrt(math.pow(speed[0],2)+math.pow(speed[1],2))*20, speed[1]/math.sqrt(math.pow(speed[0],2)+math.pow(speed[1],2))*20]
    eraser = pygame.Surface((cards.CARDW, cards.CARDH))
    eraser.fill(bg)
    prevdisty = abs(cardrect.y - goal[1])
    prevdistx = abs(cardrect.x - goal[0])
    while(prevdisty >= abs(cardrect.y - goal[1]) and prevdistx >= abs(cardrect.x - goal[0])):
        pygame.event.pump()
        pygame.event.clear()
        clock.tick(90)
        eraser.blit(cards.screen, (0, 0), (cardrect.x, cardrect.y, cards.CARDW, cards.CARDH))
        updatedareas += [cards.screen.blit(card.image, cardrect)]
        pygame.display.update(updatedareas)
        updatedareas = []
        updatedareas += [cards.screen.blit(eraser, cardrect)]
        prevdisty = abs(cardrect.y - goal[1])
        prevdistx = abs(cardrect.x - goal[0])
        cardrect = cardrect.move(speed)

eraser = pygame.Surface((cards.width+10, cards.CARDH+20))
eraser.fill(bg)
UpArrow = guielem.Arrow((0,handpos[1]), True)
DownArrow = guielem.Arrow((0, handpos[1]+90), False)
previously("GLHF")
while play:
    turnnum += 1
    count = 0
    while count < len(hums): #go through the human players and have them go
        if huminplay[count][0]: #skip if not in play
            previously("Human Player {}".format(count+1), (255, 255, 255))
            turn(hums[count])
            updatedareas += [cards.screen.blit(eraser, (handpos[0]-5, handpos[1]-18))]
            cards.screen.blit(hums[count].image[hums[count].index], hums[count].rect) #HANDYHAND
            updatedareas += [font.render_to(cards.screen, (hums[count].rect.x+cards.CARDW*6*6/5, hums[count].rect.y+90), str(hums[count].index+1) + "/" + str(len(hums[count].hands)), fgcolor=(255,158,0))]
            pygame.display.update(updatedareas)
            updatedareas = []
            if hums[count].isempty():
                eprompt(guielem.ButtonPrompt("Congratulations! We have a winner!", cards.width/2, cards.height/2, cards.width/3, cards.height/5, "Yay!"))
                play = False
            if not play:
                break
        else:
            #keep track of who has been skipped and for how long
            huminplay[count] = (False, huminplay[count][1]-1)
            if huminplay[count][1] == 0:
                huminplay[count] = (True, 0)
        count += 1
        time.sleep(1)
    count = 0
    if not play:
        break
    while count < len(aiplayers):
        updatedareas += [cards.screen.blit(eraser, (0, handpos[1]-18))]
        if aiinplay[count][0]:
            previously("AI Player {}".format(count+1), (255, 255, 255))
            playerstatus()
            checkturn(aiplayers[count], aiplayers[count].turn(topcard, prevmovefeat, prevmovelab))
            updatedareas += [cards.screen.blit(topcard.image, (deckpos[0]+200, deckpos[1]))]
            if aiplayers[count].hand.isempty():
                eprompt(guielem.ButtonPrompt("AI Player {}: GG EZ".format(count+1), cards.width/2, cards.height/2, cards.width/3, cards.height/5, "GG"))
                play = False
                break
            time.sleep(1) #pause between turns
        else:
            aiinplay[count] = (False, aiinplay[count][1]-1)
            if aiinplay[count][1] == 0:
                aiinplay[count] = (True, 0)
        count += 1
        
