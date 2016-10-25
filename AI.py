
class AIplay:
    def __init__(self, h): #initialize ai with a hand
        self.hand=h

    def turn(self, topcard):
        validturn=True
        print(topcard)
        print(self.hand)
        actions=[]
        for card in self.hand.cards:
            if(card.rank==topcard.rank or card.suit==topcard.suit):
                self.hand.rem_card(card)
                topcard=card
                break
        else:
            validturn=False

        return topcard, actions
